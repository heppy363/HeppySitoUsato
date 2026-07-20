import random
from enum import Enum

import httpx
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator


class TimeoutSettings(BaseModel):
    connect: float = Field(default=5.0, gt=0)
    read: float = Field(default=10.0, gt=0)
    write: float = Field(default=10.0, gt=0)
    pool: float = Field(default=5.0, gt=0)

    model_config = ConfigDict(frozen=True)

    def to_httpx_timeout(self) -> httpx.Timeout:
        return httpx.Timeout(
            connect=self.connect,
            read=self.read,
            write=self.write,
            pool=self.pool,
        )


class ConnectionLimitsSettings(BaseModel):
    max_connections: int = Field(default=20, gt=0)
    max_keepalive_connections: int = Field(default=10, ge=0)
    keepalive_expiry: float = Field(default=30.0, gt=0)

    model_config = ConfigDict(frozen=True)

    def to_httpx_limits(self) -> httpx.Limits:
        return httpx.Limits(
            max_connections=self.max_connections,
            max_keepalive_connections=self.max_keepalive_connections,
            keepalive_expiry=self.keepalive_expiry,
        )


class RetrySettings(BaseModel):
    max_attempts: int = Field(default=3, ge=1)
    backoff_seconds: float = Field(default=0.5, ge=0)
    jitter_seconds: float = Field(default=0.1, ge=0)

    model_config = ConfigDict(frozen=True)

    def get_delay(self, retry_number: int) -> float:
        base_delay = self.backoff_seconds * retry_number
        if self.jitter_seconds == 0:
            return base_delay
        return base_delay + random.uniform(0, self.jitter_seconds)


class ProxyStrategy(str, Enum):
    DIRECT = "direct"
    DATACENTER = "datacenter"
    RESIDENTIAL = "residential"
    TOR = "tor"


class ProxySettings(BaseModel):
    strategy: ProxyStrategy = ProxyStrategy.DIRECT
    url: str | None = None
    username: str | None = Field(default=None, min_length=1)
    password: SecretStr | None = None

    model_config = ConfigDict(frozen=True)

    @field_validator("url", "username", mode="before")
    @classmethod
    def normalize_optional_string(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @model_validator(mode="after")
    def validate_strategy(self) -> "ProxySettings":
        if self.password is not None and self.username is None:
            raise ValueError("proxy password requires a proxy username")

        if self.strategy is ProxyStrategy.DIRECT:
            if self.url is not None or self.username is not None or self.password is not None:
                raise ValueError("direct proxy strategy cannot define proxy url or credentials")
            return self

        if self.url is None:
            raise ValueError(f"{self.strategy.value} proxy strategy requires a proxy url")

        return self


class NetworkSettings(BaseModel):
    http2: bool = True
    verify_ssl: bool = True
    user_agent: str = Field(default="HeppySitoUsato/0.1.0", min_length=1)
    proxy: ProxySettings = Field(default_factory=ProxySettings)
    timeout: TimeoutSettings = Field(default_factory=TimeoutSettings)
    connections: ConnectionLimitsSettings = Field(default_factory=ConnectionLimitsSettings)
    retry: RetrySettings = Field(default_factory=RetrySettings)

    model_config = ConfigDict(frozen=True)

    @property
    def proxy_strategy(self) -> ProxyStrategy:
        return self.proxy.strategy

    @property
    def proxy_url(self) -> str | None:
        return self.proxy.url

    def default_headers(self) -> dict[str, str]:
        return {"User-Agent": self.user_agent}
