from abc import ABC, abstractmethod

from pydantic import ValidationError

from app.network import HTTPMethod, NetworkClient, NetworkRequest
from app.providers.ebay.auth import EbayAccessTokenProvider
from app.providers.ebay.config import EbayBrowseApiSettings
from app.providers.ebay.exceptions import EbayParseError
from app.providers.ebay.schemas import (
    EbayBrowseApiSearchResponse,
    EbaySearchItem,
    EbaySearchResponse,
)
from app.providers.models import SearchRequest


class EbaySearchAdapter(ABC):
    @abstractmethod
    async def search(self, request: SearchRequest) -> EbaySearchResponse:
        raise NotImplementedError


class MockEbaySearchAdapter(EbaySearchAdapter):
    def __init__(self, items: list[EbaySearchItem]) -> None:
        self._items = items

    async def search(self, request: SearchRequest) -> EbaySearchResponse:
        start_index = (request.page - 1) * request.page_size
        end_index = start_index + request.page_size
        page_items = self._items[start_index:end_index]

        return EbaySearchResponse(
            items=page_items,
            page=request.page,
            page_size=request.page_size,
            total=len(self._items),
            has_next=end_index < len(self._items),
        )


class EbayBrowseApiSearchAdapter(EbaySearchAdapter):
    def __init__(
        self,
        *,
        network_client: NetworkClient,
        settings: EbayBrowseApiSettings,
        access_token_provider: EbayAccessTokenProvider,
    ) -> None:
        self._network_client = network_client
        self._settings = settings
        self._access_token_provider = access_token_provider

    async def search(self, request: SearchRequest) -> EbaySearchResponse:
        access_token = await self._access_token_provider.get_access_token()
        offset = (request.page - 1) * request.page_size

        response = await self._network_client.request(
            NetworkRequest(
                method=HTTPMethod.GET,
                url=self._settings.browse_search_url,
                params={
                    "q": request.query,
                    "limit": request.page_size,
                    "offset": offset,
                    "fieldgroups": "EXTENDED",
                },
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                    "X-EBAY-C-MARKETPLACE-ID": self._settings.marketplace_id,
                },
            )
        )

        try:
            payload = EbayBrowseApiSearchResponse.model_validate(response.json())
        except ValidationError as exc:
            raise EbayParseError(
                f"EbayProvider returned an invalid Browse API payload: {exc}",
                provider_name="EbayProvider",
                platform="ebay",
            ) from exc

        return EbaySearchResponse(
            items=payload.item_summaries,
            page=request.page,
            page_size=payload.limit,
            total=payload.total,
            has_next=payload.next_page is not None,
        )
