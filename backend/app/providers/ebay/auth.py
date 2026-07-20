from abc import ABC, abstractmethod
from base64 import b64encode
from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

from pydantic import SecretStr, ValidationError

from app.network import HTTPMethod, NetworkClient, NetworkRequest
from app.providers.ebay.config import EbayBrowseApiSettings
from app.providers.ebay.exceptions import EbayParseError
from app.providers.ebay.schemas import EbayOAuthTokenResponse


class EbayAccessTokenProvider(ABC):
    @abstractmethod
    async def get_access_token(self) -> str:
        raise NotImplementedError


class StaticEbayAccessTokenProvider(EbayAccessTokenProvider):
    def __init__(self, access_token: str | SecretStr) -> None:
        token_value = (
            access_token.get_secret_value() if isinstance(access_token, SecretStr) else access_token
        ).strip()
        if not token_value:
            raise ValueError("eBay access token cannot be blank")

        self._access_token = token_value

    async def get_access_token(self) -> str:
        return self._access_token


class ClientCredentialsEbayAccessTokenProvider(EbayAccessTokenProvider):
    def __init__(
        self,
        *,
        network_client: NetworkClient,
        settings: EbayBrowseApiSettings,
        refresh_skew_seconds: int = 60,
    ) -> None:
        if settings.client_id is None or settings.client_secret is None:
            raise ValueError("eBay client credentials are required for client credentials flow")

        self._network_client = network_client
        self._settings = settings
        self._refresh_skew_seconds = refresh_skew_seconds
        self._cached_token: str | None = None
        self._expires_at: datetime | None = None

    async def get_access_token(self) -> str:
        now = datetime.now(UTC)
        if (
            self._cached_token is not None
            and self._expires_at is not None
            and now < self._expires_at
        ):
            return self._cached_token

        response = await self._network_client.request(
            NetworkRequest(
                method=HTTPMethod.POST,
                url=self._settings.oauth_token_url,
                headers={
                    "Authorization": f"Basic {self._build_basic_authorization()}",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
                content=urlencode(
                    {
                        "grant_type": "client_credentials",
                        "scope": self._settings.oauth_scope,
                    }
                ).encode(),
            )
        )

        try:
            token_payload = EbayOAuthTokenResponse.model_validate_json(response.text)
        except ValidationError as exc:
            raise EbayParseError(
                f"EbayProvider returned an invalid OAuth token payload: {exc}",
                provider_name="EbayProvider",
                platform="ebay",
            ) from exc

        self._cached_token = token_payload.access_token
        self._expires_at = now + timedelta(
            seconds=max(token_payload.expires_in - self._refresh_skew_seconds, 0)
        )
        return self._cached_token

    def _build_basic_authorization(self) -> str:
        client_secret = self._settings.client_secret
        if self._settings.client_id is None or client_secret is None:
            raise ValueError("eBay client credentials are not configured")

        raw_credentials = (
            f"{self._settings.client_id}:{client_secret.get_secret_value()}"
        ).encode()
        return b64encode(raw_credentials).decode("ascii")
