from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.database import DatabaseSessionManager
from app.main import create_app
from app.models.health import (
    DependencyHealth,
    HealthChecks,
    HealthCheckStatus,
    HealthResponse,
    HealthResponseStatus,
)
from app.network import HttpxNetworkClient
from app.providers import ProviderRegistry
from app.services import RegistryAggregationService, RuntimeHealthService


class FakeRedisClient:
    def __init__(self, ping_result: Exception | bool = True) -> None:
        self._ping_result = ping_result
        self.closed = False

    async def ping(self) -> bool:
        if isinstance(self._ping_result, Exception):
            raise self._ping_result
        return bool(self._ping_result)

    async def aclose(self) -> None:
        self.closed = True


def build_health_response(status: HealthResponseStatus) -> HealthResponse:
    return HealthResponse(
        status=status,
        app="HeppySitoUsato API",
        version="0.1.0",
        environment="development",
        checked_at=datetime(2026, 7, 22, tzinfo=UTC),
        checks=HealthChecks(
            backend=DependencyHealth(status=HealthCheckStatus.UP),
            redis=DependencyHealth(
                status=(
                    HealthCheckStatus.UP
                    if status == HealthResponseStatus.OK
                    else HealthCheckStatus.DOWN
                ),
                detail=None if status == HealthResponseStatus.OK else "connection_error",
            ),
            database=DependencyHealth(status=HealthCheckStatus.UP),
        ),
    )


def build_runtime_health_service() -> tuple[
    RuntimeHealthService,
    HttpxNetworkClient,
    DatabaseSessionManager,
]:
    settings = Settings()
    network_client = HttpxNetworkClient(settings.build_network_settings())
    provider_registry = ProviderRegistry()
    aggregation_service = RegistryAggregationService(provider_registry)
    database = MagicMock(spec=DatabaseSessionManager)
    database.check_connection = AsyncMock()
    service = RuntimeHealthService(
        settings=settings,
        network_client=network_client,
        provider_registry=provider_registry,
        aggregation_service=aggregation_service,
        database=database,
        check_timeout_seconds=0.1,
    )
    return service, network_client, database


def test_health_endpoint_returns_200_when_all_checks_are_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_app()

    with TestClient(app) as client:
        monkeypatch.setattr(
            app.state.health_service,
            "get_health",
            AsyncMock(return_value=build_health_response(HealthResponseStatus.OK)),
        )
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "HeppySitoUsato API",
        "version": "0.1.0",
        "environment": "development",
        "checked_at": "2026-07-22T00:00:00Z",
        "checks": {
            "backend": {"status": "up", "detail": None},
            "redis": {"status": "up", "detail": None},
            "database": {"status": "up", "detail": None},
        },
    }


def test_health_endpoint_returns_503_when_a_dependency_is_down(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = create_app()

    with TestClient(app) as client:
        monkeypatch.setattr(
            app.state.health_service,
            "get_health",
            AsyncMock(return_value=build_health_response(HealthResponseStatus.DEGRADED)),
        )
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["status"] == "degraded"
    assert response.json()["checks"]["redis"] == {
        "status": "down",
        "detail": "connection_error",
    }


@pytest.mark.asyncio
async def test_runtime_health_service_reports_all_checks_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, network_client, database = build_runtime_health_service()
    fake_redis = FakeRedisClient()
    monkeypatch.setattr(
        "app.services.health.redis_from_url",
        lambda *_args, **_kwargs: fake_redis,
    )

    try:
        response = await service.get_health()
    finally:
        await network_client.aclose()

    assert response.is_healthy is True
    assert response.status == HealthResponseStatus.OK
    assert response.checks.backend.status == HealthCheckStatus.UP
    assert response.checks.redis.status == HealthCheckStatus.UP
    assert response.checks.database.status == HealthCheckStatus.UP
    assert fake_redis.closed is True
    database.check_connection.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_runtime_health_service_reports_backend_down_when_network_client_is_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, network_client, _database = build_runtime_health_service()
    fake_redis = FakeRedisClient()
    monkeypatch.setattr(
        "app.services.health.redis_from_url",
        lambda *_args, **_kwargs: fake_redis,
    )

    await network_client.aclose()
    response = await service.get_health()

    assert response.is_healthy is False
    assert response.status == HealthResponseStatus.DEGRADED
    assert response.checks.backend == DependencyHealth(
        status=HealthCheckStatus.DOWN,
        detail="network_client_closed",
    )


@pytest.mark.asyncio
async def test_runtime_health_service_reports_database_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, network_client, database = build_runtime_health_service()
    fake_redis = FakeRedisClient()
    monkeypatch.setattr(
        "app.services.health.redis_from_url",
        lambda *_args, **_kwargs: fake_redis,
    )
    database.check_connection.side_effect = OSError("database unavailable")

    try:
        response = await service.get_health()
    finally:
        await network_client.aclose()

    assert response.is_healthy is False
    assert response.checks.database == DependencyHealth(
        status=HealthCheckStatus.DOWN,
        detail="connection_error",
    )
