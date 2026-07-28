import hashlib
import json
import logging
from abc import ABC, abstractmethod

from pydantic import ValidationError
from redis.asyncio import Redis
from redis.asyncio import from_url as redis_from_url
from redis.exceptions import RedisError

from app.services.aggregation import AggregationRequest, AggregationResponse


class SearchCacheError(Exception):
    pass


class SearchCacheUnavailableError(SearchCacheError):
    pass


class SearchCacheSerializationError(SearchCacheError):
    pass


class SearchCacheKeyBuilder:
    _prefix = "search:v1"

    def build(self, request: AggregationRequest) -> str:
        payload = request.model_dump(mode="json")
        serialized = json.dumps(
            payload,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return f"{self._prefix}:{digest}"


class SearchCache(ABC):
    @property
    @abstractmethod
    def key_builder(self) -> SearchCacheKeyBuilder:
        raise NotImplementedError

    @abstractmethod
    async def get(self, request: AggregationRequest) -> AggregationResponse | None:
        raise NotImplementedError

    @abstractmethod
    async def set(
        self,
        request: AggregationRequest,
        response: AggregationResponse,
        *,
        ttl_seconds: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def aclose(self) -> None:
        raise NotImplementedError


class RedisSearchCache(SearchCache):
    def __init__(
        self,
        redis_client: Redis,
        *,
        key_builder: SearchCacheKeyBuilder | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._redis_client = redis_client
        self._key_builder = key_builder or SearchCacheKeyBuilder()
        self._logger = logger or logging.getLogger(__name__)

    @classmethod
    def from_url(
        cls,
        redis_url: str,
        *,
        key_builder: SearchCacheKeyBuilder | None = None,
        logger: logging.Logger | None = None,
    ) -> "RedisSearchCache":
        redis_client = redis_from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        return cls(
            redis_client,
            key_builder=key_builder,
            logger=logger,
        )

    @property
    def key_builder(self) -> SearchCacheKeyBuilder:
        return self._key_builder

    async def get(self, request: AggregationRequest) -> AggregationResponse | None:
        cache_key = self._key_builder.build(request)
        try:
            cached_payload = await self._redis_client.get(cache_key)
        except (RedisError, OSError) as exc:
            self._log_failure("get", cache_key, exc)
            return None

        if cached_payload is None:
            return None

        try:
            return AggregationResponse.model_validate_json(cached_payload)
        except (ValidationError, ValueError, TypeError) as exc:
            self._log_failure("deserialize", cache_key, exc)
            return None

    async def set(
        self,
        request: AggregationRequest,
        response: AggregationResponse,
        *,
        ttl_seconds: int,
    ) -> None:
        if ttl_seconds < 1:
            raise ValueError("ttl_seconds must be greater than zero")

        cache_key = self._key_builder.build(request)
        try:
            serialized_response = response.model_dump_json()
        except (ValueError, TypeError) as exc:
            self._log_failure("serialize", cache_key, exc)
            return

        try:
            await self._redis_client.set(
                cache_key,
                serialized_response,
                ex=ttl_seconds,
            )
        except (RedisError, OSError) as exc:
            self._log_failure("set", cache_key, exc)

    async def aclose(self) -> None:
        try:
            await self._redis_client.aclose()
        except (RedisError, OSError) as exc:
            self._log_failure("close", "not_applicable", exc)

    def _log_failure(self, operation: str, cache_key: str, error: Exception) -> None:
        self._logger.warning(
            "search_cache_operation_failed",
            extra={
                "cache_operation": operation,
                "cache_key": cache_key,
                "error_type": error.__class__.__name__,
            },
        )
