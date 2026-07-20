import httpx
import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.network.client import HttpxNetworkClient
from app.network.config import NetworkSettings, ProxySettings, ProxyStrategy, RetrySettings
from app.network.exceptions import (
    NetworkConfigurationError,
    NetworkHTTPStatusError,
    NetworkTimeoutError,
    NetworkTransportError,
)
from app.network.models import HTTPMethod, NetworkRequest
from app.network.proxy import (
    DatacenterProxyProvider,
    DirectProxyProvider,
    ResidentialProxyProvider,
    TorProxyProvider,
    build_proxy_provider,
)


def test_settings_build_network_settings_uses_backend_values() -> None:
    settings = Settings(
        network_http2=False,
        network_verify_ssl=False,
        network_user_agent="test-agent/1.0",
        network_timeout_connect=1.5,
        network_timeout_read=2.5,
        network_timeout_write=3.5,
        network_timeout_pool=4.5,
        network_max_connections=50,
        network_max_keepalive_connections=25,
        network_keepalive_expiry=12.0,
        network_retry_max_attempts=4,
        network_retry_backoff_seconds=0.25,
        network_retry_jitter_seconds=0.0,
        network_proxy_strategy=ProxyStrategy.DATACENTER,
        network_proxy_url="http://proxy.internal:8080",
        network_proxy_username="proxy-user",
        network_proxy_password="proxy-password",
    )

    network_settings = settings.build_network_settings()

    assert network_settings.http2 is False
    assert network_settings.verify_ssl is False
    assert network_settings.user_agent == "test-agent/1.0"
    assert network_settings.proxy.strategy is ProxyStrategy.DATACENTER
    assert network_settings.proxy_url == "http://proxy.internal:8080"
    assert network_settings.proxy.username == "proxy-user"
    assert network_settings.proxy.password is not None
    assert network_settings.proxy.password.get_secret_value() == "proxy-password"
    assert network_settings.timeout.connect == 1.5
    assert network_settings.timeout.read == 2.5
    assert network_settings.timeout.write == 3.5
    assert network_settings.timeout.pool == 4.5
    assert network_settings.connections.max_connections == 50
    assert network_settings.connections.max_keepalive_connections == 25
    assert network_settings.connections.keepalive_expiry == 12.0
    assert network_settings.retry.max_attempts == 4
    assert network_settings.retry.backoff_seconds == 0.25
    assert network_settings.retry.jitter_seconds == 0.0


def test_network_request_rejects_content_and_json_body_together() -> None:
    with pytest.raises(ValidationError):
        NetworkRequest(
            method=HTTPMethod.POST,
            url="https://example.com/items",
            content=b"raw-body",
            json_body={"raw": False},
        )


def test_proxy_settings_reject_direct_strategy_with_proxy_url() -> None:
    with pytest.raises(ValidationError):
        ProxySettings(strategy=ProxyStrategy.DIRECT, url="http://proxy.internal:8080")


def test_build_proxy_provider_returns_typed_provider_with_credentials() -> None:
    provider = build_proxy_provider(
        ProxySettings(
            strategy=ProxyStrategy.RESIDENTIAL,
            url="http://proxy.internal:8080",
            username="proxy-user",
            password="proxy-password",
        )
    )

    assert isinstance(provider, ResidentialProxyProvider)
    assert provider.get_proxy_url() == "http://proxy-user:proxy-password@proxy.internal:8080"
    assert provider.safe_label() == "residential://proxy.internal:8080"


@pytest.mark.parametrize(
    ("strategy", "provider_type"),
    [
        (ProxyStrategy.DATACENTER, DatacenterProxyProvider),
        (ProxyStrategy.TOR, TorProxyProvider),
    ],
)
def test_build_proxy_provider_supports_multiple_proxy_strategies(
    strategy: ProxyStrategy,
    provider_type: type[DatacenterProxyProvider] | type[TorProxyProvider],
) -> None:
    provider = build_proxy_provider(
        ProxySettings(strategy=strategy, url="http://proxy.internal:8080")
    )

    assert isinstance(provider, provider_type)


@pytest.mark.asyncio
async def test_httpx_network_client_retries_timeout_and_keeps_default_headers() -> None:
    attempts = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise httpx.ReadTimeout("simulated timeout", request=request)

        assert request.headers["User-Agent"] == "heppy-tests/1.0"
        return httpx.Response(200, json={"ok": True}, request=request)

    client = HttpxNetworkClient(
        NetworkSettings(
            user_agent="heppy-tests/1.0",
            retry=RetrySettings(max_attempts=2, backoff_seconds=0.0, jitter_seconds=0.0),
        ),
        transport=httpx.MockTransport(handler),
    )

    response = await client.request(
        NetworkRequest(method=HTTPMethod.GET, url="https://example.com/items")
    )

    await client.aclose()

    assert attempts == 2
    assert response.json() == {"ok": True}


@pytest.mark.asyncio
async def test_httpx_network_client_uses_resolved_direct_proxy_provider() -> None:
    client = HttpxNetworkClient(
        NetworkSettings(),
        transport=httpx.MockTransport(lambda request: None),
    )

    assert isinstance(client.proxy_provider, DirectProxyProvider)

    await client.aclose()


def test_httpx_network_client_rejects_ambiguous_proxy_credentials() -> None:
    with pytest.raises(NetworkConfigurationError):
        HttpxNetworkClient(
            NetworkSettings(
                proxy=ProxySettings(
                    strategy=ProxyStrategy.DATACENTER,
                    url="http://embedded:secret@proxy.internal:8080",
                    username="override-user",
                )
            )
        )


@pytest.mark.asyncio
async def test_httpx_network_client_maps_proxy_unavailability_to_transport_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ProxyError("proxy unavailable", request=request)

    client = HttpxNetworkClient(
        NetworkSettings(
            proxy=ProxySettings(
                strategy=ProxyStrategy.DATACENTER,
                url="http://proxy.internal:8080",
            ),
            retry=RetrySettings(max_attempts=1, backoff_seconds=0.0, jitter_seconds=0.0),
        ),
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(NetworkTransportError):
        await client.request(NetworkRequest(method=HTTPMethod.GET, url="https://example.com/up"))

    await client.aclose()


@pytest.mark.asyncio
async def test_httpx_network_client_maps_http_status_errors() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="service unavailable", request=request)

    client = HttpxNetworkClient(
        NetworkSettings(),
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(NetworkHTTPStatusError) as exc_info:
        await client.request(NetworkRequest(method=HTTPMethod.GET, url="https://example.com/up"))

    await client.aclose()

    error = exc_info.value
    assert error.status_code == 503
    assert error.response_text == "service unavailable"


@pytest.mark.asyncio
async def test_httpx_network_client_raises_timeout_when_retries_are_exhausted() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("simulated timeout", request=request)

    client = HttpxNetworkClient(
        NetworkSettings(
            retry=RetrySettings(max_attempts=2, backoff_seconds=0.0, jitter_seconds=0.0)
        ),
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(NetworkTimeoutError):
        await client.request(NetworkRequest(method=HTTPMethod.GET, url="https://example.com/slow"))

    await client.aclose()
