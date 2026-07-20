from collections.abc import Mapping
from typing import Any

import pytest
from pydantic import ValidationError

from app.network.config import TimeoutSettings
from app.network.exceptions import NetworkHTTPStatusError, NetworkTimeoutError
from app.providers import MarketplaceProvider, ProviderMetadata, ProviderResponseError
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
        id="provider:item-1",
        external_id="item-1",
        title="RTX 3090 Founders Edition",
        price=999.0,
        currency="eur",
        platform="ebay",
        url="https://example.com/items/item-1",
    )

    assert result.currency == "EUR"
    assert result.relevance_score == 0.0
    assert result.collected_at.tzinfo is not None


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


@pytest.mark.asyncio
async def test_marketplace_provider_contract_returns_normalized_results() -> None:
    provider = DummyMarketplaceProvider()

    status = await provider.validate()
    results = await provider.search(SearchRequest(query="RTX 3090"))

    assert status is ProviderStatus.ACTIVE
    assert provider.metadata.name == "DummyProvider"
    assert results[0].platform == "dummy"
    assert results[0].currency == "EUR"
