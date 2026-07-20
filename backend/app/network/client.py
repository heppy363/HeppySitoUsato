import asyncio
import logging
import time
from abc import ABC, abstractmethod

import httpx

from app.network.config import NetworkSettings
from app.network.exceptions import (
    NetworkConfigurationError,
    NetworkError,
    NetworkHTTPStatusError,
    NetworkTimeoutError,
    NetworkTransportError,
)
from app.network.models import NetworkRequest
from app.network.proxy import ProxyProvider, build_proxy_provider


class NetworkClient(ABC):
    @abstractmethod
    async def request(self, request: NetworkRequest) -> httpx.Response:
        raise NotImplementedError

    @abstractmethod
    async def aclose(self) -> None:
        raise NotImplementedError


class HttpxNetworkClient(NetworkClient):
    def __init__(
        self,
        settings: NetworkSettings,
        *,
        proxy_provider: ProxyProvider | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._settings = settings
        self._logger = logging.getLogger("app.network.client")
        http2_enabled = self._resolve_http2_support(settings)
        proxy_label = settings.proxy_strategy.value
        try:
            self._proxy_provider = proxy_provider or build_proxy_provider(settings.proxy)
            proxy_url = self._proxy_provider.get_proxy_url()
            proxy_label = self._proxy_provider.safe_label()
            self._client = httpx.AsyncClient(
                headers=settings.default_headers(),
                http2=http2_enabled,
                limits=settings.connections.to_httpx_limits(),
                proxy=proxy_url,
                timeout=settings.timeout.to_httpx_timeout(),
                transport=transport,
                trust_env=False,
                verify=settings.verify_ssl,
            )
        except (TypeError, ValueError) as exc:
            raise NetworkConfigurationError(
                "Invalid network client configuration",
                method="CONFIG",
                url=proxy_label,
            ) from exc

    async def request(self, request: NetworkRequest) -> httpx.Response:
        started_at = time.monotonic()
        last_error: NetworkError | None = None

        for attempt in range(1, self._settings.retry.max_attempts + 1):
            try:
                response = await self._client.request(
                    method=request.method.value,
                    url=str(request.url),
                    params=request.params or None,
                    headers=request.headers or None,
                    cookies=request.cookies or None,
                    content=request.content,
                    json=request.json_body,
                    follow_redirects=request.follow_redirects,
                    timeout=(
                        request.timeout.to_httpx_timeout()
                        if request.timeout is not None
                        else self._settings.timeout.to_httpx_timeout()
                    ),
                )
                if request.raise_for_status:
                    response.raise_for_status()

                self._logger.info(
                    "network request completed",
                    extra={
                        "method": request.method.value,
                        "url": str(request.url),
                        "status_code": response.status_code,
                        "duration_ms": self._duration_ms(started_at),
                        "attempt": attempt,
                    },
                )
                return response
            except httpx.TimeoutException as exc:
                last_error = NetworkTimeoutError(
                    f"{request.method.value} {request.url} timed out",
                    method=request.method.value,
                    url=str(request.url),
                )
                if not self._should_retry(request, attempt):
                    self._log_failure(request, started_at, last_error, attempt)
                    raise last_error from exc
            except httpx.HTTPStatusError as exc:
                error = NetworkHTTPStatusError.from_httpx(request, exc.response)
                self._log_failure(request, started_at, error, attempt)
                raise error from exc
            except httpx.HTTPError as exc:
                last_error = NetworkTransportError(
                    f"{request.method.value} {request.url} failed: {exc}",
                    method=request.method.value,
                    url=str(request.url),
                )
                if not self._should_retry(request, attempt):
                    self._log_failure(request, started_at, last_error, attempt)
                    raise last_error from exc

            await asyncio.sleep(self._settings.retry.get_delay(attempt))

        if last_error is None:
            raise NetworkTransportError(
                f"{request.method.value} {request.url} failed without a mapped error",
                method=request.method.value,
                url=str(request.url),
            )

        self._log_failure(request, started_at, last_error, self._settings.retry.max_attempts)
        raise last_error

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "HttpxNetworkClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    @property
    def proxy_provider(self) -> ProxyProvider:
        return self._proxy_provider

    def _should_retry(self, request: NetworkRequest, attempt: int) -> bool:
        return request.retry_on_failure and attempt < self._settings.retry.max_attempts

    def _log_failure(
        self,
        request: NetworkRequest,
        started_at: float,
        error: Exception,
        attempt: int,
    ) -> None:
        self._logger.warning(
            "network request failed",
            extra={
                "method": request.method.value,
                "url": str(request.url),
                "duration_ms": self._duration_ms(started_at),
                "attempt": attempt,
                "error_type": error.__class__.__name__,
            },
        )

    @staticmethod
    def _duration_ms(started_at: float) -> int:
        return int((time.monotonic() - started_at) * 1000)

    def _resolve_http2_support(self, settings: NetworkSettings) -> bool:
        if not settings.http2:
            return False

        try:
            import h2  # noqa: F401
        except ImportError:
            self._logger.warning(
                "http2 requested but optional dependency is unavailable; falling back to http1",
                extra={"requested_http2": True},
            )
            return False

        return True
