import pytest

from app.network.exceptions import NetworkTimeoutError
from app.providers.ebay import (
    EbayParseError,
    EbayProvider,
    EbayResultMapper,
    EbaySearchItem,
    EbaySearchResponse,
    EbayUnavailableError,
)
from app.providers.models import ProviderStatus, SearchRequest


def test_ebay_result_mapper_maps_raw_item_to_search_result() -> None:
    mapper = EbayResultMapper()
    item = EbaySearchItem.model_validate(
        {
            "item_id": "v1|1234567890|0",
            "title": "RTX 3090 Founders Edition",
            "item_web_url": "https://www.ebay.com/itm/1234567890",
            "price": {"value": "899.99", "currency": "eur"},
            "image": {"image_url": "https://i.ebayimg.com/images/item.jpg"},
            "seller": {"username": "trusted-seller", "feedback_percentage": 99.8},
            "item_location": {"city": "Milan", "country": "IT"},
            "short_description": "GPU usata in buone condizioni",
            "condition": "Used",
            "item_creation_date": "2026-07-20T10:15:00Z",
        }
    )

    result = mapper.map_item(item)

    assert result.id == "ebay:v1|1234567890|0"
    assert result.external_id == "v1|1234567890|0"
    assert result.price == 899.99
    assert result.currency == "EUR"
    assert result.platform == "ebay"
    assert result.location == "Milan, IT"
    assert result.seller_name == "trusted-seller"
    assert result.seller_rating == 99.8


@pytest.mark.asyncio
async def test_ebay_provider_search_maps_executor_results() -> None:
    async def executor(request: SearchRequest) -> EbaySearchResponse:
        assert request.query == "RTX 3090"
        return EbaySearchResponse(
            items=[
                EbaySearchItem.model_validate(
                    {
                        "item_id": "v1|1234567890|0",
                        "title": "RTX 3090 Founders Edition",
                        "item_web_url": "https://www.ebay.com/itm/1234567890",
                        "price": {"value": "899.99", "currency": "EUR"},
                    }
                )
            ]
        )

    provider = EbayProvider(search_executor=executor)

    status = await provider.validate()
    results = await provider.search(SearchRequest(query="RTX 3090"))

    assert status is ProviderStatus.ACTIVE
    assert provider.metadata.platform == "ebay"
    assert len(results) == 1
    assert results[0].title == "RTX 3090 Founders Edition"


def test_ebay_provider_normalize_rejects_invalid_payload() -> None:
    async def executor(_: SearchRequest) -> list[EbaySearchItem]:
        return []

    provider = EbayProvider(search_executor=executor)

    with pytest.raises(EbayParseError):
        provider.normalize({"item_id": "missing-fields"})


@pytest.mark.asyncio
async def test_ebay_provider_maps_network_timeout_to_unavailable_error() -> None:
    async def executor(_: SearchRequest) -> list[EbaySearchItem]:
        raise NetworkTimeoutError(
            "GET https://api.ebay.example timed out",
            method="GET",
            url="https://api.ebay.example",
        )

    provider = EbayProvider(search_executor=executor)

    with pytest.raises(EbayUnavailableError):
        await provider.search(SearchRequest(query="RTX 3090"))
