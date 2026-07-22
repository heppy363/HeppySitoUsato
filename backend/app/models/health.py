from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class HealthCheckStatus(str, Enum):
    UP = "up"
    DOWN = "down"


class HealthResponseStatus(str, Enum):
    OK = "ok"
    DEGRADED = "degraded"


class DependencyHealth(BaseModel):
    status: HealthCheckStatus
    detail: str | None = None

    model_config = ConfigDict(extra="forbid", frozen=True)

    @property
    def is_up(self) -> bool:
        return self.status == HealthCheckStatus.UP


class HealthChecks(BaseModel):
    backend: DependencyHealth
    redis: DependencyHealth
    database: DependencyHealth

    model_config = ConfigDict(extra="forbid", frozen=True)


class HealthResponse(BaseModel):
    status: HealthResponseStatus
    app: str = Field(min_length=1)
    version: str = Field(min_length=1)
    environment: str = Field(min_length=1)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    checks: HealthChecks

    model_config = ConfigDict(extra="forbid", frozen=True)

    @property
    def is_healthy(self) -> bool:
        return self.status == HealthResponseStatus.OK
