from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from app.network.config import TimeoutSettings
from app.network.exceptions import NetworkError
from app.providers.base import MarketplaceProvider
from app.providers.ebay.adapter import EbaySearchAdapter
from app.providers.ebay.exceptions import EbayParseError, map_ebay_network_error
from app.providers.ebay.mapper import EbayResultMapper
from app.providers.ebay.schemas import EbaySearchItem
from app.providers.models import ProviderMetadata, ProviderStatus, SearchRequest, SearchResult


class EbayProvider(MarketplaceProvider):
    def __init__(
        self,
        *,
        search_adapter: EbaySearchAdapter,
        mapper: EbayResultMapper | None = None,
        default_timeout: TimeoutSettings | None = None,
    ) -> None:
        self._search_adapter = search_adapter
        self._mapper = mapper or EbayResultMapper()
        self._metadata = ProviderMetadata(
            name="EbayProvider",
            platform="ebay",
            default_timeout=default_timeout
            or TimeoutSettings(connect=3.0, read=8.0, write=8.0, pool=3.0),
        )

    @property
    def metadata(self) -> ProviderMetadata:
        return self._metadata

    @property
    def search_adapter(self) -> EbaySearchAdapter:
        return self._search_adapter

    async def search(self, request: SearchRequest) -> list[SearchResult]:
        try:
            raw_results = await self._search_adapter.search(request)
        except NetworkError as exc:
            raise map_ebay_network_error(exc) from exc

        return [self.normalize(item) for item in raw_results.items]

    def normalize(self, raw_item: Mapping[str, Any] | EbaySearchItem) -> SearchResult:
        try:
            item = (
                raw_item
                if isinstance(raw_item, EbaySearchItem)
                else EbaySearchItem.model_validate(raw_item)
            )
        except ValidationError as exc:
            raise EbayParseError(
                f"EbayProvider returned an invalid item payload: {exc}",
                provider_name=self.metadata.name,
                platform=self.metadata.platform,
            ) from exc

        return self._mapper.map_item(item)

    async def validate(self) -> ProviderStatus:
        return ProviderStatus.ACTIVE
