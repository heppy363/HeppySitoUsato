from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from app.providers.models import ProviderMetadata, ProviderStatus, SearchRequest, SearchResult


class MarketplaceProvider(ABC):
    @property
    @abstractmethod
    def metadata(self) -> ProviderMetadata:
        raise NotImplementedError

    @abstractmethod
    async def search(self, request: SearchRequest) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, raw_item: Mapping[str, Any]) -> SearchResult:
        raise NotImplementedError

    @abstractmethod
    async def validate(self) -> ProviderStatus:
        raise NotImplementedError
