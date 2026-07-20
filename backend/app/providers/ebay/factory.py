import logging

from pydantic import ValidationError

from app.core.config import Settings
from app.network import NetworkClient
from app.providers.ebay.adapter import EbayBrowseApiSearchAdapter
from app.providers.ebay.auth import (
    ClientCredentialsEbayAccessTokenProvider,
    EbayAccessTokenProvider,
    StaticEbayAccessTokenProvider,
)
from app.providers.ebay.config import EbayBrowseApiSettings
from app.providers.ebay.provider import EbayProvider

logger = logging.getLogger("app.providers.ebay.factory")


def build_ebay_access_token_provider(
    *,
    settings: EbayBrowseApiSettings,
    network_client: NetworkClient,
) -> EbayAccessTokenProvider:
    if settings.access_token is not None:
        return StaticEbayAccessTokenProvider(settings.access_token)

    return ClientCredentialsEbayAccessTokenProvider(
        network_client=network_client,
        settings=settings,
    )


def build_ebay_provider(
    *,
    settings: Settings,
    network_client: NetworkClient,
) -> EbayProvider:
    ebay_settings = settings.build_ebay_browse_api_settings()
    access_token_provider = build_ebay_access_token_provider(
        settings=ebay_settings,
        network_client=network_client,
    )
    search_adapter = EbayBrowseApiSearchAdapter(
        network_client=network_client,
        settings=ebay_settings,
        access_token_provider=access_token_provider,
    )
    return EbayProvider(search_adapter=search_adapter)


def maybe_build_ebay_provider(
    *,
    settings: Settings,
    network_client: NetworkClient,
) -> EbayProvider | None:
    try:
        return build_ebay_provider(settings=settings, network_client=network_client)
    except (ValidationError, ValueError) as exc:
        logger.info(
            "ebay provider is not configured for runtime use",
            extra={
                "provider": "ebay",
                "error_type": exc.__class__.__name__,
            },
        )
        return None
