from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from app.network.config import TimeoutSettings
from app.network.exceptions import NetworkHTTPStatusError, NetworkTimeoutError
from app.providers import (
    MarketplaceProvider,
    ProviderMetadata,
    ProviderRegistry,
    ProviderResponseError,
)
from app.providers.exceptions import ProviderUnavailableError, map_network_error
from app.providers.models import ProviderStatus, SearchRequest, SearchResult


class DummyMarketplaceProvider(MarketplaceProvider):
    def __init__(self) -> None:
        self._metadata = ProviderMetadata(
            name="DummyProvider",
            platform="dummy",
            default_timeout=TimeoutSettings(connect=1.0, read=2.0, write=2.0, pool=1.0),
        )

    @property
    def metadata(self) -> ProviderMetadata:
        return self._metadata

    async def search(self, request: SearchRequest) -> list[SearchResult]:
        return [
            self.normalize(
                {
                    "id": f"dummy-{request.page}",
                    "external_id": "external-1",
                    "title": request.query,
                    "price": 199.99,
                    "currency": "eur",
                    "platform": self.metadata.platform,
                    "url": "https://example.com/items/external-1",
                }
            )
        ]

    def normalize(self, raw_item: Mapping[str, Any]) -> SearchResult:
        return SearchResult(**raw_item)

    async def validate(self) -> ProviderStatus:
        return ProviderStatus.ACTIVE


def test_search_request_normalizes_query_whitespace() -> None:
    request = SearchRequest(query="   rtx   3090   ", page=2)

    assert request.query == "rtx 3090"
    assert request.page == 2
    assert request.page_size == 25


def test_search_request_rejects_blank_query() -> None:
    with pytest.raises(ValidationError):
        SearchRequest(query="   ")


def test_search_result_normalizes_currency_and_defaults_timestamp() -> None:
    result = SearchResult(
        id=" provider:item-1 ",
        external_id=" item-1 ",
        title="RTX 3090 Founders Edition",
        price=999.0,
        currency="eur",
        platform="ebay",
        url="https://example.com/items/item-1",
    )

    assert result.id == "provider:item-1"
    assert result.external_id == "item-1"
    assert result.currency == "EUR"
    assert result.relevance_score == 0.0
    assert result.collected_at.tzinfo == UTC


def test_search_result_normalizes_timestamps_to_utc() -> None:
    result = SearchResult(
        id="provider:item-1",
        external_id="item-1",
        title="RTX 3090 Founders Edition",
        price=999.0,
        currency="EUR",
        platform="ebay",
        url="https://example.com/items/item-1",
        published_at="2026-07-20T10:30:00+02:00",
        collected_at=datetime(2026, 7, 20, 9, 0, 0),
    )

    assert result.published_at == datetime(2026, 7, 20, 8, 30, 0, tzinfo=UTC)
    assert result.collected_at == datetime(2026, 7, 20, 9, 0, 0, tzinfo=UTC)


def test_search_result_allows_incomplete_optional_fields() -> None:
    result = SearchResult(
        id="provider:item-2",
        external_id="item-2",
        title="Used GPU",
        price=450.0,
        currency="EUR",
        platform="subito",
        url="https://example.com/items/item-2",
        description="   ",
        location="  ",
        seller_name="   ",
        condition=" ",
    )

    assert result.description is None
    assert result.location is None
    assert result.seller_name is None
    assert result.condition is None


@pytest.mark.parametrize(
    ("payload", "field_name"),
    [
        (
            {
                "id": "provider:item-1",
                "external_id": "item-1",
                "title": "RTX 3090",
                "price": 999.0,
                "currency": "EU",
                "platform": "ebay",
                "url": "https://example.com/items/item-1",
            },
            "currency",
        ),
        (
            {
                "id": "provider:item-1",
                "external_id": "item-1",
                "title": "RTX 3090",
                "price": -1.0,
                "currency": "EUR",
                "platform": "ebay",
                "url": "https://example.com/items/item-1",
            },
            "price",
        ),
        (
            {
                "id": "provider:item-1",
                "external_id": "item-1",
                "title": "RTX 3090",
                "price": 999.0,
                "currency": "EUR",
                "platform": "ebay",
                "url": "https://example.com/items/item-1",
                "relevance_score": 1.5,
            },
            "relevance_score",
        ),
        (
            {
                "id": "provider:item-1",
                "external_id": "item-1",
                "title": "RTX 3090",
                "price": 999.0,
                "currency": "EUR",
                "platform": "ebay",
                "url": "not-a-url",
            },
            "url",
        ),
    ],
)
def test_search_result_rejects_invalid_payloads(
    payload: dict[str, object],
    field_name: str,
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        SearchResult(**payload)

    assert field_name in str(exc_info.value)


def test_map_network_error_maps_timeout_to_provider_unavailable() -> None:
    error = map_network_error(
        provider_name="DummyProvider",
        platform="dummy",
        error=NetworkTimeoutError(
            "GET https://example.com timed out",
            method="GET",
            url="https://example.com",
        ),
    )

    assert isinstance(error, ProviderUnavailableError)


def test_map_network_error_maps_http_status_to_provider_response_error() -> None:
    error = map_network_error(
        provider_name="DummyProvider",
        platform="dummy",
        error=NetworkHTTPStatusError(
            "GET https://example.com returned HTTP 503",
            method="GET",
            url="https://example.com",
            status_code=503,
            response_text="service unavailable",
        ),
    )

    assert isinstance(error, ProviderResponseError)


def test_provider_registry_registers_and_returns_provider_by_platform() -> None:
    registry = ProviderRegistry()
    provider = DummyMarketplaceProvider()

    registry.register(provider)

    assert len(registry) == 1
    assert registry.get("dummy") is provider
    assert registry["dummy"] is provider
    assert registry.platforms == ("dummy",)
    assert registry.all() == (provider,)
    assert registry.items() == (("dummy", provider),)


def test_provider_registry_can_be_initialized_with_existing_providers() -> None:
    provider = DummyMarketplaceProvider()

    registry = ProviderRegistry([provider])

    assert "dummy" in registry
    assert tuple(registry) == (provider,)


@pytest.mark.asyncio
async def test_marketplace_provider_contract_returns_normalized_results() -> None:
    provider = DummyMarketplaceProvider()

    status = await provider.validate()
    results = await provider.search(SearchRequest(query="RTX 3090"))

    assert status is ProviderStatus.ACTIVE
    assert provider.metadata.name == "DummyProvider"
    assert results[0].platform == "dummy"
    assert results[0].currency == "EUR"
