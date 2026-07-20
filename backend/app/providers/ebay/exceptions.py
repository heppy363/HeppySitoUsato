from app.network.exceptions import NetworkError
from app.providers.exceptions import (
    ProviderParseError,
    ProviderResponseError,
    ProviderUnavailableError,
    map_network_error,
)


class EbayUnavailableError(ProviderUnavailableError):
    pass


class EbayResponseError(ProviderResponseError):
    pass


class EbayParseError(ProviderParseError):
    pass


def map_ebay_network_error(error: NetworkError) -> ProviderUnavailableError | ProviderResponseError:
    mapped_error = map_network_error(
        provider_name="EbayProvider",
        platform="ebay",
        error=error,
    )

    if isinstance(mapped_error, ProviderUnavailableError):
        return EbayUnavailableError(
            str(mapped_error),
            provider_name=mapped_error.provider_name,
            platform=mapped_error.platform,
        )

    return EbayResponseError(
        str(mapped_error),
        provider_name=mapped_error.provider_name,
        platform=mapped_error.platform,
    )
