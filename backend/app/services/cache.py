import hashlib
import json
from abc import ABC, abstractmethod

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
