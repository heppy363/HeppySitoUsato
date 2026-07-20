from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.network.config import (
    ConnectionLimitsSettings,
    NetworkSettings,
    ProxySettings,
    ProxyStrategy,
    RetrySettings,
    TimeoutSettings,
)


class Settings(BaseSettings):
    app_name: str = "HeppySitoUsato API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+asyncpg://heppysito:change_me@localhost:5432/heppysitousato"
    network_http2: bool = True
    network_verify_ssl: bool = True
    network_user_agent: str = "HeppySitoUsato/0.1.0"
    network_timeout_connect: float = 5.0
    network_timeout_read: float = 10.0
    network_timeout_write: float = 10.0
    network_timeout_pool: float = 5.0
    network_max_connections: int = 20
    network_max_keepalive_connections: int = 10
    network_keepalive_expiry: float = 30.0
    network_retry_max_attempts: int = 3
    network_retry_backoff_seconds: float = 0.5
    network_retry_jitter_seconds: float = 0.1
    network_proxy_strategy: ProxyStrategy = ProxyStrategy.DIRECT
    network_proxy_url: str | None = None
    network_proxy_username: str | None = None
    network_proxy_password: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="BACKEND_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def build_network_settings(self) -> NetworkSettings:
        return NetworkSettings(
            http2=self.network_http2,
            verify_ssl=self.network_verify_ssl,
            user_agent=self.network_user_agent,
            proxy=ProxySettings(
                strategy=self.network_proxy_strategy,
                url=self.network_proxy_url,
                username=self.network_proxy_username,
                password=self.network_proxy_password,
            ),
            timeout=TimeoutSettings(
                connect=self.network_timeout_connect,
                read=self.network_timeout_read,
                write=self.network_timeout_write,
                pool=self.network_timeout_pool,
            ),
            connections=ConnectionLimitsSettings(
                max_connections=self.network_max_connections,
                max_keepalive_connections=self.network_max_keepalive_connections,
                keepalive_expiry=self.network_keepalive_expiry,
            ),
            retry=RetrySettings(
                max_attempts=self.network_retry_max_attempts,
                backoff_seconds=self.network_retry_backoff_seconds,
                jitter_seconds=self.network_retry_jitter_seconds,
            ),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
