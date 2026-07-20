"""Marketplace providers package."""

from app.providers.base import MarketplaceProvider
from app.providers.ebay import (
    ClientCredentialsEbayAccessTokenProvider,
    EbayBrowseApiSearchAdapter,
    EbayBrowseApiSettings,
    EbayProvider,
    EbayResultMapper,
    MockEbaySearchAdapter,
    StaticEbayAccessTokenProvider,
    build_ebay_provider,
    maybe_build_ebay_provider,
)
from app.providers.exceptions import (
    ProviderConfigurationError,
    ProviderError,
    ProviderParseError,
    ProviderResponseError,
    ProviderUnavailableError,
    map_network_error,
)
from app.providers.models import ProviderMetadata, ProviderStatus, SearchRequest, SearchResult
from app.providers.registry import ProviderRegistry

__all__ = [
    "ClientCredentialsEbayAccessTokenProvider",
    "EbayBrowseApiSearchAdapter",
    "EbayBrowseApiSettings",
    "EbayProvider",
    "EbayResultMapper",
    "MarketplaceProvider",
    "MockEbaySearchAdapter",
    "ProviderConfigurationError",
    "ProviderError",
    "ProviderMetadata",
    "ProviderParseError",
    "ProviderRegistry",
    "ProviderResponseError",
    "ProviderStatus",
    "ProviderUnavailableError",
    "SearchRequest",
    "SearchResult",
    "StaticEbayAccessTokenProvider",
    "build_ebay_provider",
    "maybe_build_ebay_provider",
    "map_network_error",
]
