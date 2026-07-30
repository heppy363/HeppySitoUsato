from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.database import DatabaseSessionManager
from app.main import create_app
from app.network import HttpxNetworkClient
from app.providers import EbayProvider, ProviderRegistry
from app.services import (
    CachedAggregationService,
    RedisSearchCache,
    RegistryAggregationService,
    RuntimeHealthService,
    SlidingWindowRateLimiter,
)


def test_create_app_uses_expected_metadata() -> None:
    app = create_app()

    assert app.title == "HeppySitoUsato API"
    assert app.version == "0.1.0"


def test_create_app_registers_shared_services_and_closes_runtime_clients(monkeypatch) -> None:
    app = create_app(Settings(ebay_api_access_token="static-token"))

    with TestClient(app):
        cache_close_mock = AsyncMock()
        database_dispose_mock = AsyncMock()
        monkeypatch.setattr(app.state.search_cache, "aclose", cache_close_mock)
        monkeypatch.setattr(app.state.database, "dispose", database_dispose_mock)
        assert isinstance(app.state.network_client, HttpxNetworkClient)
        assert isinstance(app.state.providers, ProviderRegistry)
        assert isinstance(app.state.registry_aggregation_service, RegistryAggregationService)
        assert isinstance(app.state.search_cache, RedisSearchCache)
        assert isinstance(app.state.database, DatabaseSessionManager)
        assert isinstance(app.state.aggregation_service, CachedAggregationService)
        assert isinstance(app.state.search_rate_limiter, SlidingWindowRateLimiter)
        assert isinstance(app.state.health_service, RuntimeHealthService)
        assert app.state.aggregation_service.provider_registry is app.state.providers
        assert (
            app.state.aggregation_service.aggregation_service
            is app.state.registry_aggregation_service
        )
        assert app.state.aggregation_service.search_cache is app.state.search_cache
        assert app.state.health_service.provider_registry is app.state.providers
        assert app.state.health_service.aggregation_service is app.state.aggregation_service
        assert app.state.health_service.database is app.state.database
        assert isinstance(app.state.ebay_provider, EbayProvider)
        assert app.state.providers["ebay"] is app.state.ebay_provider
        assert app.state.providers.get("ebay") is app.state.ebay_provider
        assert app.state.providers.platforms == ("ebay",)
        assert app.state.network_client.is_closed is False

    assert app.state.network_client.is_closed is True
    cache_close_mock.assert_awaited_once_with()
    database_dispose_mock.assert_awaited_once_with()


def test_create_app_skips_ebay_provider_when_runtime_auth_is_missing() -> None:
    app = create_app(Settings())

    with TestClient(app):
        assert isinstance(app.state.network_client, HttpxNetworkClient)
        assert app.state.ebay_provider is None
        assert isinstance(app.state.providers, ProviderRegistry)
        assert isinstance(app.state.registry_aggregation_service, RegistryAggregationService)
        assert isinstance(app.state.search_cache, RedisSearchCache)
        assert isinstance(app.state.database, DatabaseSessionManager)
        assert isinstance(app.state.aggregation_service, CachedAggregationService)
        assert isinstance(app.state.health_service, RuntimeHealthService)
        assert app.state.aggregation_service.provider_registry is app.state.providers
        assert app.state.health_service.provider_registry is app.state.providers
        assert len(app.state.providers) == 0
