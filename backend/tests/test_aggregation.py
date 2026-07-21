import asyncio
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

import pytest

from app.network.config import TimeoutSettings
from app.providers import (
    MarketplaceProvider,
    ProviderMetadata,
    ProviderRegistry,
    ProviderUnavailableError,
)
from app.providers.models import ProviderStatus, SearchRequest, SearchResult
from app.services import (
    AggregationProviderFailure,
    AggregationProviderSelectionError,
    AggregationRequest,
    AggregationResponse,
    RegistryAggregationService,
)


class AggregationDummyProvider(MarketplaceProvider):
    def __init__(self, *, platform: str) -> None:
        self._metadata = ProviderMetadata(
            name=f"{platform.title()}Provider",
            platform=platform,
            default_timeout=TimeoutSettings(connect=1.0, read=2.0, write=2.0, pool=1.0),
        )

    @property
    def metadata(self) -> ProviderMetadata:
        return self._metadata

    async def search(self, request: SearchRequest) -> list[SearchResult]:
        return [
            SearchResult(
                id=f"{self.metadata.platform}:1",
                external_id="1",
                title=request.query,
                price=100.0,
                currency="EUR",
                platform=self.metadata.platform,
                url="https://example.com/items/1",
            )
        ]

    def normalize(self, raw_item: Mapping[str, Any]) -> SearchResult:
        return SearchResult(**raw_item)

    async def validate(self) -> ProviderStatus:
        return ProviderStatus.ACTIVE


class ParallelObservationState:
    def __init__(self) -> None:
        self.active = 0
        self.max_active = 0
        self.ready = asyncio.Event()


class ParallelAggregationDummyProvider(AggregationDummyProvider):
    def __init__(self, *, platform: str, state: ParallelObservationState) -> None:
        super().__init__(platform=platform)
        self._state = state

    async def search(self, request: SearchRequest) -> list[SearchResult]:
        self._state.active += 1
        self._state.max_active = max(self._state.max_active, self._state.active)
        if self._state.active >= 2:
            self._state.ready.set()

        await asyncio.wait_for(self._state.ready.wait(), timeout=0.2)
        await asyncio.sleep(0)
        self._state.active -= 1
        return await super().search(request)


class FailingAggregationDummyProvider(AggregationDummyProvider):
    async def search(self, request: SearchRequest) -> list[SearchResult]:
        raise ProviderUnavailableError(
            f"{self.metadata.name} is temporarily unavailable",
            provider_name=self.metadata.name,
            platform=self.metadata.platform,
        )


class ResultSetAggregationDummyProvider(AggregationDummyProvider):
    def __init__(self, *, platform: str, results: list[SearchResult]) -> None:
        super().__init__(platform=platform)
        self._results = results

    async def search(self, request: SearchRequest) -> list[SearchResult]:
        return list(self._results)


def test_aggregation_request_normalizes_and_deduplicates_platforms() -> None:
    request = AggregationRequest(
        search=SearchRequest(query="RTX 3090"),
        platforms=[" ebay ", "subito", "EBAY", "   "],
    )

    assert request.platforms == ("ebay", "subito")


def test_registry_aggregation_service_selects_all_registered_providers_by_default() -> None:
    ebay_provider = AggregationDummyProvider(platform="ebay")
    subito_provider = AggregationDummyProvider(platform="subito")
    service = RegistryAggregationService(ProviderRegistry([ebay_provider, subito_provider]))

    selected = service.select_providers(AggregationRequest(search=SearchRequest(query="RTX 3090")))

    assert selected == (ebay_provider, subito_provider)


def test_registry_aggregation_service_selects_requested_platforms_in_declared_order() -> None:
    ebay_provider = AggregationDummyProvider(platform="ebay")
    subito_provider = AggregationDummyProvider(platform="subito")
    service = RegistryAggregationService(ProviderRegistry([ebay_provider, subito_provider]))

    selected = service.select_providers(
        AggregationRequest(
            search=SearchRequest(query="RTX 3090"),
            platforms=("subito", "ebay"),
        )
    )

    assert selected == (subito_provider, ebay_provider)


def test_registry_aggregation_service_rejects_unknown_platforms() -> None:
    service = RegistryAggregationService(
        ProviderRegistry([AggregationDummyProvider(platform="ebay")])
    )

    with pytest.raises(AggregationProviderSelectionError) as exc_info:
        service.select_providers(
            AggregationRequest(
                search=SearchRequest(query="RTX 3090"),
                platforms=("ebay", "wallapop"),
            )
        )

    assert exc_info.value.unknown_platforms == ("wallapop",)


@pytest.mark.asyncio
async def test_registry_aggregation_service_executes_selected_providers_in_parallel() -> None:
    state = ParallelObservationState()
    service = RegistryAggregationService(
        ProviderRegistry(
            [
                ParallelAggregationDummyProvider(platform="ebay", state=state),
                ParallelAggregationDummyProvider(platform="subito", state=state),
            ]
        )
    )

    response = await service.search(AggregationRequest(search=SearchRequest(query="RTX 3090")))

    assert isinstance(response, AggregationResponse)
    assert len(response.results) == 2
    assert response.failures == ()
    assert state.max_active == 2


@pytest.mark.asyncio
async def test_registry_aggregation_service_collects_partial_results_when_one_provider_fails() -> (
    None
):
    ebay_provider = AggregationDummyProvider(platform="ebay")
    failing_provider = FailingAggregationDummyProvider(platform="subito")
    service = RegistryAggregationService(ProviderRegistry([ebay_provider, failing_provider]))

    response = await service.search(AggregationRequest(search=SearchRequest(query="RTX 3090")))

    assert response.results == (
        SearchResult(
            id="ebay:1",
            external_id="1",
            title="RTX 3090",
            price=100.0,
            currency="EUR",
            platform="ebay",
            url="https://example.com/items/1",
        ),
    )
    assert response.failures == (
        AggregationProviderFailure(
            provider_name="SubitoProvider",
            platform="subito",
            error_type="ProviderUnavailableError",
            message="SubitoProvider is temporarily unavailable",
        ),
    )


@pytest.mark.asyncio
async def test_registry_aggregation_service_deduplicates_and_merges_results() -> None:
    collected_base = datetime(2026, 7, 21, 9, 0, tzinfo=UTC)
    collected_enriched = datetime(2026, 7, 21, 11, 30, tzinfo=UTC)
    published_base = datetime(2026, 7, 20, 15, 0, tzinfo=UTC)
    published_enriched = datetime(2026, 7, 19, 8, 30, tzinfo=UTC)
    service = RegistryAggregationService(
        ProviderRegistry(
            [
                ResultSetAggregationDummyProvider(
                    platform="ebay",
                    results=[
                        SearchResult(
                            id="ebay:1",
                            external_id="1",
                            title="RTX 3090",
                            price=100.0,
                            currency="EUR",
                            platform="ebay",
                            url="https://example.com/items/1",
                            published_at=published_base,
                            collected_at=collected_base,
                            relevance_score=0.4,
                        ),
                        SearchResult(
                            id="ebay:1",
                            external_id="1",
                            title="NVIDIA RTX 3090 Founders Edition",
                            description="Scheda video completa di scatola originale",
                            price=100.0,
                            currency="EUR",
                            platform="ebay",
                            location="Milano",
                            url="https://example.com/items/1",
                            image_url="https://example.com/items/1.jpg",
                            seller_name="Mario Rossi",
                            seller_rating=4.9,
                            condition="Usato garantito",
                            published_at=published_enriched,
                            collected_at=collected_enriched,
                            relevance_score=0.8,
                        ),
                    ],
                )
            ]
        )
    )

    response = await service.search(AggregationRequest(search=SearchRequest(query="RTX 3090")))

    assert response.failures == ()
    assert response.results == (
        SearchResult(
            id="ebay:1",
            external_id="1",
            title="NVIDIA RTX 3090 Founders Edition",
            description="Scheda video completa di scatola originale",
            price=100.0,
            currency="EUR",
            platform="ebay",
            location="Milano",
            url="https://example.com/items/1",
            image_url="https://example.com/items/1.jpg",
            seller_name="Mario Rossi",
            seller_rating=4.9,
            condition="Usato garantito",
            published_at=published_enriched,
            collected_at=collected_enriched,
            relevance_score=0.8,
        ),
    )


@pytest.mark.asyncio
async def test_registry_aggregation_service_keeps_results_separate_across_platforms() -> None:
    service = RegistryAggregationService(
        ProviderRegistry(
            [
                ResultSetAggregationDummyProvider(
                    platform="ebay",
                    results=[
                        SearchResult(
                            id="ebay:1",
                            external_id="shared-1",
                            title="RTX 3090 eBay",
                            price=100.0,
                            currency="EUR",
                            platform="ebay",
                            url="https://example.com/ebay/items/1",
                        )
                    ],
                ),
                ResultSetAggregationDummyProvider(
                    platform="subito",
                    results=[
                        SearchResult(
                            id="subito:1",
                            external_id="shared-1",
                            title="RTX 3090 Subito",
                            price=100.0,
                            currency="EUR",
                            platform="subito",
                            url="https://example.com/subito/items/1",
                        )
                    ],
                ),
            ]
        )
    )

    response = await service.search(AggregationRequest(search=SearchRequest(query="RTX 3090")))

    assert response.failures == ()
    assert response.results == (
        SearchResult(
            id="ebay:1",
            external_id="shared-1",
            title="RTX 3090 eBay",
            price=100.0,
            currency="EUR",
            platform="ebay",
            url="https://example.com/ebay/items/1",
        ),
        SearchResult(
            id="subito:1",
            external_id="shared-1",
            title="RTX 3090 Subito",
            price=100.0,
            currency="EUR",
            platform="subito",
            url="https://example.com/subito/items/1",
        ),
    )
