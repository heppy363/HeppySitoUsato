from app.providers import MarketplaceProvider, ProviderRegistry
from app.services.aggregation import (
    AggregationRequest,
    AggregationResponse,
    AggregationService,
)
from app.services.cache import SearchCache, SearchCacheError
from app.services.ranking import RankingService


class CachedAggregationService(AggregationService):
    def __init__(
        self,
        aggregation_service: AggregationService,
        search_cache: SearchCache,
        *,
        ttl_seconds: int,
    ) -> None:
        if ttl_seconds < 1:
            raise ValueError("ttl_seconds must be greater than zero")

        self._aggregation_service = aggregation_service
        self._search_cache = search_cache
        self._ttl_seconds = ttl_seconds

    @property
    def provider_registry(self) -> ProviderRegistry:
        return self._aggregation_service.provider_registry

    @property
    def ranking_service(self) -> RankingService:
        return self._aggregation_service.ranking_service

    @property
    def aggregation_service(self) -> AggregationService:
        return self._aggregation_service

    @property
    def search_cache(self) -> SearchCache:
        return self._search_cache

    def select_providers(self, request: AggregationRequest) -> tuple[MarketplaceProvider, ...]:
        return self._aggregation_service.select_providers(request)

    async def search(self, request: AggregationRequest) -> AggregationResponse:
        try:
            cached_response = await self._search_cache.get(request)
        except SearchCacheError:
            cached_response = None

        if cached_response is not None:
            return cached_response

        response = await self._aggregation_service.search(request)

        try:
            await self._search_cache.set(
                request,
                response,
                ttl_seconds=self._ttl_seconds,
            )
        except SearchCacheError:
            pass

        return response
