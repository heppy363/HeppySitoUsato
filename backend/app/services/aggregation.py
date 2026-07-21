import asyncio
from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.providers import (
    MarketplaceProvider,
    ProviderError,
    ProviderRegistry,
    SearchRequest,
    SearchResult,
)
from app.services.ranking import HeuristicRankingService, RankingService


class AggregationRequest(BaseModel):
    search: SearchRequest
    platforms: tuple[str, ...] | None = Field(default=None)
    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @field_validator("platforms", mode="before")
    @classmethod
    def normalize_platforms(cls, value: Iterable[str] | None) -> tuple[str, ...] | None:
        if value is None:
            return None

        normalized_platforms: list[str] = []
        for platform in value:
            normalized = platform.strip().lower()
            if not normalized:
                continue
            if normalized not in normalized_platforms:
                normalized_platforms.append(normalized)

        return tuple(normalized_platforms) or None

    @model_validator(mode="after")
    def validate_price_range(self) -> "AggregationRequest":
        if self.min_price is not None and self.max_price is not None:
            if self.min_price > self.max_price:
                raise ValueError("min_price cannot be greater than max_price")
        return self


class AggregationError(Exception):
    pass


class AggregationProviderSelectionError(AggregationError):
    def __init__(self, unknown_platforms: tuple[str, ...]) -> None:
        platforms_label = ", ".join(unknown_platforms)
        super().__init__(f"Unknown provider platforms requested: {platforms_label}")
        self.unknown_platforms = unknown_platforms


class AggregationProviderFailure(BaseModel):
    provider_name: str = Field(min_length=1)
    platform: str = Field(min_length=1)
    error_type: str = Field(min_length=1)
    message: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid", frozen=True)


class AggregationResponse(BaseModel):
    results: tuple[SearchResult, ...] = Field(default_factory=tuple)
    failures: tuple[AggregationProviderFailure, ...] = Field(default_factory=tuple)

    model_config = ConfigDict(extra="forbid", frozen=True)


class AggregationService(ABC):
    @property
    @abstractmethod
    def provider_registry(self) -> ProviderRegistry:
        raise NotImplementedError

    @property
    @abstractmethod
    def ranking_service(self) -> RankingService:
        raise NotImplementedError

    @abstractmethod
    def select_providers(self, request: AggregationRequest) -> tuple[MarketplaceProvider, ...]:
        raise NotImplementedError

    @abstractmethod
    async def search(self, request: AggregationRequest) -> AggregationResponse:
        raise NotImplementedError


class RegistryAggregationService(AggregationService):
    def __init__(
        self,
        provider_registry: ProviderRegistry,
        ranking_service: RankingService | None = None,
    ) -> None:
        self._provider_registry = provider_registry
        self._ranking_service = ranking_service or HeuristicRankingService()

    @property
    def provider_registry(self) -> ProviderRegistry:
        return self._provider_registry

    @property
    def ranking_service(self) -> RankingService:
        return self._ranking_service

    def select_providers(self, request: AggregationRequest) -> tuple[MarketplaceProvider, ...]:
        if request.platforms is None:
            return self._provider_registry.all()

        selected_providers: list[MarketplaceProvider] = []
        unknown_platforms: list[str] = []

        for platform in request.platforms:
            provider = self._provider_registry.get(platform)
            if provider is None:
                unknown_platforms.append(platform)
                continue
            selected_providers.append(provider)

        if unknown_platforms:
            raise AggregationProviderSelectionError(tuple(unknown_platforms))

        return tuple(selected_providers)

    async def search(self, request: AggregationRequest) -> AggregationResponse:
        providers = self.select_providers(request)
        executions = await asyncio.gather(
            *(provider.search(request.search) for provider in providers),
            return_exceptions=True,
        )

        results: list[SearchResult] = []
        failures: list[AggregationProviderFailure] = []

        for provider, execution in zip(providers, executions, strict=True):
            if isinstance(execution, Exception):
                failures.append(self._build_failure(provider, execution))
                continue

            results.extend(execution)

        normalized_results = self._normalize_results(results)
        filtered_results = self._filter_results(request, normalized_results)
        ranked_results = self._ranking_service.rank(request.search, filtered_results)
        ordered_results = self._order_results(ranked_results)

        return AggregationResponse(results=ordered_results, failures=tuple(failures))

    @staticmethod
    def _build_failure(
        provider: MarketplaceProvider,
        error: Exception,
    ) -> AggregationProviderFailure:
        if isinstance(error, ProviderError):
            provider_name = error.provider_name
            platform = error.platform
        else:
            provider_name = provider.metadata.name
            platform = provider.metadata.platform

        return AggregationProviderFailure(
            provider_name=provider_name,
            platform=platform,
            error_type=error.__class__.__name__,
            message=str(error),
        )

    @classmethod
    def _normalize_results(cls, results: Iterable[SearchResult]) -> tuple[SearchResult, ...]:
        merged_results: dict[tuple[str, str], SearchResult] = {}
        ordered_keys: list[tuple[str, str]] = []

        for result in results:
            key = cls._result_key(result)
            existing = merged_results.get(key)
            if existing is None:
                merged_results[key] = result
                ordered_keys.append(key)
                continue

            merged_results[key] = cls._merge_results(existing, result)

        return tuple(merged_results[key] for key in ordered_keys)

    @staticmethod
    def _filter_results(
        request: AggregationRequest,
        results: Iterable[SearchResult],
    ) -> tuple[SearchResult, ...]:
        filtered_results: list[SearchResult] = []

        for result in results:
            if request.min_price is not None and result.price < request.min_price:
                continue
            if request.max_price is not None and result.price > request.max_price:
                continue
            filtered_results.append(result)

        return tuple(filtered_results)

    @classmethod
    def _order_results(cls, results: Iterable[SearchResult]) -> tuple[SearchResult, ...]:
        return tuple(sorted(results, key=cls._result_sort_key))

    @staticmethod
    def _result_sort_key(result: SearchResult) -> tuple[float, int, float, float, float, str, str]:
        published_present = 0 if result.published_at is not None else 1
        published_timestamp = (
            -result.published_at.timestamp() if result.published_at is not None else 0.0
        )
        collected_timestamp = -result.collected_at.timestamp()

        return (
            -result.relevance_score,
            published_present,
            published_timestamp,
            collected_timestamp,
            result.price,
            result.platform,
            result.external_id,
        )

    @staticmethod
    def _result_key(result: SearchResult) -> tuple[str, str]:
        return (result.platform, result.external_id)

    @classmethod
    def _merge_results(cls, current: SearchResult, incoming: SearchResult) -> SearchResult:
        return current.model_copy(
            update={
                "title": cls._prefer_longer_text(current.title, incoming.title),
                "description": cls._prefer_longer_text(
                    current.description,
                    incoming.description,
                ),
                "location": cls._prefer_longer_text(current.location, incoming.location),
                "image_url": current.image_url or incoming.image_url,
                "seller_name": cls._prefer_longer_text(
                    current.seller_name,
                    incoming.seller_name,
                ),
                "seller_rating": cls._prefer_highest_number(
                    current.seller_rating,
                    incoming.seller_rating,
                ),
                "condition": cls._prefer_longer_text(current.condition, incoming.condition),
                "published_at": cls._prefer_earliest_datetime(
                    current.published_at,
                    incoming.published_at,
                ),
                "collected_at": cls._prefer_latest_datetime(
                    current.collected_at,
                    incoming.collected_at,
                ),
                "relevance_score": max(current.relevance_score, incoming.relevance_score),
            }
        )

    @staticmethod
    def _prefer_longer_text(current: str | None, incoming: str | None) -> str | None:
        if current is None:
            return incoming
        if incoming is None:
            return current
        if len(incoming) > len(current):
            return incoming
        return current

    @staticmethod
    def _prefer_highest_number(
        current: float | None,
        incoming: float | None,
    ) -> float | None:
        if current is None:
            return incoming
        if incoming is None:
            return current
        return max(current, incoming)

    @staticmethod
    def _prefer_earliest_datetime(
        current: datetime | None,
        incoming: datetime | None,
    ) -> datetime | None:
        if current is None:
            return incoming
        if incoming is None:
            return current
        return min(current, incoming)

    @staticmethod
    def _prefer_latest_datetime(current: datetime, incoming: datetime) -> datetime:
        return max(current, incoming)
