from base64 import b64encode

import httpx
import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.network import HTTPMethod, NetworkClient, NetworkRequest
from app.network.exceptions import NetworkTimeoutError
from app.providers.ebay import (
    ClientCredentialsEbayAccessTokenProvider,
    EbayApiEnvironment,
    EbayBrowseApiSearchAdapter,
    EbayBrowseApiSettings,
    EbayParseError,
    EbayProvider,
    EbayResultMapper,
    EbaySearchAdapter,
    EbaySearchItem,
    EbaySearchResponse,
    EbayUnavailableError,
    MockEbaySearchAdapter,
    StaticEbayAccessTokenProvider,
)
from app.providers.models import ProviderStatus, SearchRequest


class RecordingNetworkClient(NetworkClient):
    def __init__(self, responses: list[httpx.Response]) -> None:
        self.requests: list[NetworkRequest] = []
        self._responses = responses

    async def request(self, request: NetworkRequest) -> httpx.Response:
        self.requests.append(request)
        return self._responses[len(self.requests) - 1]

    async def aclose(self) -> None:
        return None


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
async def test_ebay_provider_search_maps_adapter_results() -> None:
    adapter = MockEbaySearchAdapter(
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

    provider = EbayProvider(search_adapter=adapter)

    status = await provider.validate()
    results = await provider.search(SearchRequest(query="RTX 3090"))

    assert status is ProviderStatus.ACTIVE
    assert provider.metadata.platform == "ebay"
    assert len(results) == 1
    assert results[0].title == "RTX 3090 Founders Edition"


def test_ebay_provider_normalize_rejects_invalid_payload() -> None:
    provider = EbayProvider(search_adapter=MockEbaySearchAdapter(items=[]))

    with pytest.raises(EbayParseError):
        provider.normalize({"item_id": "missing-fields"})


@pytest.mark.asyncio
async def test_ebay_provider_maps_network_timeout_to_unavailable_error() -> None:
    class TimeoutAdapter(EbaySearchAdapter):
        async def search(self, request: SearchRequest) -> EbaySearchResponse:
            raise NetworkTimeoutError(
                "GET https://api.ebay.example timed out",
                method="GET",
                url="https://api.ebay.example",
            )

    provider = EbayProvider(search_adapter=TimeoutAdapter())

    with pytest.raises(EbayUnavailableError):
        await provider.search(SearchRequest(query="RTX 3090"))


@pytest.mark.asyncio
async def test_mock_ebay_search_adapter_supports_pagination() -> None:
    adapter = MockEbaySearchAdapter(
        items=[
            EbaySearchItem.model_validate(
                {
                    "item_id": f"v1|{index}|0",
                    "title": f"Item {index}",
                    "item_web_url": f"https://www.ebay.com/itm/{index}",
                    "price": {"value": "10.00", "currency": "EUR"},
                }
            )
            for index in range(1, 6)
        ]
    )

    second_page = await adapter.search(SearchRequest(query="gpu", page=2, page_size=2))
    provider = EbayProvider(search_adapter=adapter)
    provider_results = await provider.search(SearchRequest(query="gpu", page=2, page_size=2))

    assert second_page.page == 2
    assert second_page.page_size == 2
    assert second_page.total == 5
    assert second_page.has_next is True
    assert [item.item_id for item in second_page.items] == ["v1|3|0", "v1|4|0"]
    assert [item.external_id for item in provider_results] == ["v1|3|0", "v1|4|0"]


def test_ebay_browse_api_settings_require_authentication_inputs() -> None:
    with pytest.raises(ValidationError):
        EbayBrowseApiSettings()


def test_settings_expose_ebay_browse_api_configuration() -> None:
    settings = Settings(
        ebay_api_environment="sandbox",
        ebay_api_marketplace_id="EBAY_DE",
        ebay_api_scope="scope:test",
        ebay_api_access_token="static-token",
    )

    assert settings.ebay_api_environment == "sandbox"
    assert settings.ebay_api_marketplace_id == "EBAY_DE"
    assert settings.ebay_api_scope == "scope:test"
    assert settings.ebay_api_access_token == "static-token"


@pytest.mark.asyncio
async def test_client_credentials_token_provider_requests_and_caches_application_token() -> None:
    settings = EbayBrowseApiSettings(
        environment=EbayApiEnvironment.SANDBOX,
        marketplace_id="EBAY_IT",
        client_id="client-id",
        client_secret="client-secret",
    )
    network_client = RecordingNetworkClient(
        responses=[
            httpx.Response(
                200,
                json={
                    "access_token": "oauth-token-123",
                    "expires_in": 7200,
                    "token_type": "Application Access Token",
                },
            )
        ]
    )
    token_provider = ClientCredentialsEbayAccessTokenProvider(
        network_client=network_client,
        settings=settings,
    )

    first_token = await token_provider.get_access_token()
    second_token = await token_provider.get_access_token()

    assert first_token == "oauth-token-123"
    assert second_token == "oauth-token-123"
    assert len(network_client.requests) == 1

    token_request = network_client.requests[0]
    assert token_request.method is HTTPMethod.POST
    assert str(token_request.url) == settings.oauth_token_url
    assert token_request.headers["Accept"] == "application/json"
    assert token_request.headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert token_request.headers["Authorization"] == (
        f"Basic {b64encode(b'client-id:client-secret').decode('ascii')}"
    )
    assert token_request.content == (
        b"grant_type=client_credentials&scope=https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope"
    )


@pytest.mark.asyncio
async def test_browse_api_search_adapter_uses_official_headers_and_pagination() -> None:
    settings = EbayBrowseApiSettings(
        environment=EbayApiEnvironment.PRODUCTION,
        marketplace_id="EBAY_IT",
        access_token="static-token",
    )
    network_client = RecordingNetworkClient(
        responses=[
            httpx.Response(
                200,
                json={
                    "itemSummaries": [
                        {
                            "itemId": "v1|3|0",
                            "title": "RTX 3090 Founders Edition",
                            "itemWebUrl": "https://www.ebay.com/itm/3",
                            "price": {"value": "899.99", "currency": "EUR"},
                            "image": {"imageUrl": "https://i.ebayimg.com/images/item.jpg"},
                            "seller": {
                                "username": "trusted-seller",
                                "feedbackPercentage": "99.8",
                            },
                            "itemLocation": {"city": "Milan", "country": "IT"},
                            "shortDescription": "GPU usata in buone condizioni",
                            "condition": "Used",
                            "itemCreationDate": "2026-07-20T10:15:00Z",
                        }
                    ],
                    "limit": 2,
                    "offset": 2,
                    "total": 5,
                    "next": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=RTX%203090&limit=2&offset=4",
                },
            )
        ]
    )
    adapter = EbayBrowseApiSearchAdapter(
        network_client=network_client,
        settings=settings,
        access_token_provider=StaticEbayAccessTokenProvider("static-token"),
    )

    result = await adapter.search(SearchRequest(query="RTX 3090", page=2, page_size=2))

    assert result.page == 2
    assert result.page_size == 2
    assert result.total == 5
    assert result.has_next is True
    assert [item.item_id for item in result.items] == ["v1|3|0"]

    search_request = network_client.requests[0]
    assert search_request.method is HTTPMethod.GET
    assert str(search_request.url) == settings.browse_search_url
    assert search_request.params == {
        "q": "RTX 3090",
        "limit": 2,
        "offset": 2,
        "fieldgroups": "EXTENDED",
    }
    assert search_request.headers["Authorization"] == "Bearer static-token"
    assert search_request.headers["X-EBAY-C-MARKETPLACE-ID"] == "EBAY_IT"
