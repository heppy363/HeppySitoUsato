import asyncio
from abc import ABC, abstractmethod

from redis.asyncio import from_url as redis_from_url
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import Settings
from app.models.health import (
    DependencyHealth,
    HealthChecks,
    HealthCheckStatus,
    HealthResponse,
    HealthResponseStatus,
)
from app.network import HttpxNetworkClient
from app.providers import ProviderRegistry
from app.services.aggregation import RegistryAggregationService


class HealthService(ABC):
    @abstractmethod
    async def get_health(self) -> HealthResponse:
        raise NotImplementedError


class RuntimeHealthService(HealthService):
    def __init__(
        self,
        settings: Settings,
        network_client: HttpxNetworkClient,
        provider_registry: ProviderRegistry,
        aggregation_service: RegistryAggregationService,
        check_timeout_seconds: float = 1.0,
    ) -> None:
        self.settings = settings
        self.network_client = network_client
        self.provider_registry = provider_registry
        self.aggregation_service = aggregation_service
        self.check_timeout_seconds = check_timeout_seconds

    async def get_health(self) -> HealthResponse:
        backend_check, redis_check, database_check = await asyncio.gather(
            self._check_backend(),
            self._check_redis(),
            self._check_database(),
        )
        overall_status = (
            HealthResponseStatus.OK
            if backend_check.is_up and redis_check.is_up and database_check.is_up
            else HealthResponseStatus.DEGRADED
        )
        return HealthResponse(
            status=overall_status,
            app=self.settings.app_name,
            version=self.settings.app_version,
            environment=self.settings.app_env,
            checks=HealthChecks(
                backend=backend_check,
                redis=redis_check,
                database=database_check,
            ),
        )

    async def _check_backend(self) -> DependencyHealth:
        if self.network_client.is_closed:
            return DependencyHealth(
                status=HealthCheckStatus.DOWN,
                detail="network_client_closed",
            )

        if self.aggregation_service.provider_registry is not self.provider_registry:
            return DependencyHealth(
                status=HealthCheckStatus.DOWN,
                detail="provider_registry_mismatch",
            )

        return DependencyHealth(status=HealthCheckStatus.UP)

    async def _check_redis(self) -> DependencyHealth:
        redis_client = redis_from_url(
            self.settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=self.check_timeout_seconds,
            socket_timeout=self.check_timeout_seconds,
        )
        try:
            await asyncio.wait_for(redis_client.ping(), timeout=self.check_timeout_seconds)
        except TimeoutError:
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="timeout")
        except (RedisError, OSError):
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="connection_error")
        except Exception:
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="unexpected_error")
        finally:
            await redis_client.aclose()

        return DependencyHealth(status=HealthCheckStatus.UP)

    async def _check_database(self) -> DependencyHealth:
        try:
            engine = create_async_engine(self.settings.database_url)
        except ModuleNotFoundError:
            return DependencyHealth(
                status=HealthCheckStatus.DOWN,
                detail="driver_not_installed",
            )
        except (SQLAlchemyError, ValueError):
            return DependencyHealth(
                status=HealthCheckStatus.DOWN,
                detail="configuration_error",
            )
        except Exception:
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="unexpected_error")

        try:
            async with asyncio.timeout(self.check_timeout_seconds):
                async with engine.connect() as connection:
                    await connection.execute(text("SELECT 1"))
        except TimeoutError:
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="timeout")
        except ModuleNotFoundError:
            return DependencyHealth(
                status=HealthCheckStatus.DOWN,
                detail="driver_not_installed",
            )
        except (SQLAlchemyError, OSError):
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="connection_error")
        except Exception:
            return DependencyHealth(status=HealthCheckStatus.DOWN, detail="unexpected_error")
        finally:
            await engine.dispose()

        return DependencyHealth(status=HealthCheckStatus.UP)
