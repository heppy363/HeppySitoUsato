from app.network.exceptions import (
    NetworkConfigurationError,
    NetworkError,
    NetworkHTTPStatusError,
    NetworkTimeoutError,
    NetworkTransportError,
)


class ProviderError(Exception):
    def __init__(self, message: str, *, provider_name: str, platform: str) -> None:
        super().__init__(message)
        self.provider_name = provider_name
        self.platform = platform


class ProviderConfigurationError(ProviderError):
    pass


class ProviderUnavailableError(ProviderError):
    pass


class ProviderResponseError(ProviderError):
    pass


class ProviderParseError(ProviderError):
    pass


def map_network_error(
    *,
    provider_name: str,
    platform: str,
    error: NetworkError,
) -> ProviderError:
    if isinstance(error, NetworkConfigurationError):
        return ProviderConfigurationError(
            f"{provider_name} is misconfigured: {error}",
            provider_name=provider_name,
            platform=platform,
        )

    if isinstance(error, NetworkTimeoutError | NetworkTransportError):
        return ProviderUnavailableError(
            f"{provider_name} is temporarily unavailable: {error}",
            provider_name=provider_name,
            platform=platform,
        )

    if isinstance(error, NetworkHTTPStatusError):
        return ProviderResponseError(
            f"{provider_name} returned an invalid HTTP response: {error}",
            provider_name=provider_name,
            platform=platform,
        )

    return ProviderError(
        f"{provider_name} failed because of a network error: {error}",
        provider_name=provider_name,
        platform=platform,
    )
