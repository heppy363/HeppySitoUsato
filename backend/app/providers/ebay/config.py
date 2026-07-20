from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


class EbayApiEnvironment(str, Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"


class EbayBrowseApiSettings(BaseModel):
    environment: EbayApiEnvironment = EbayApiEnvironment.PRODUCTION
    marketplace_id: str = Field(default="EBAY_IT", min_length=1)
    oauth_scope: str = Field(
        default="https://api.ebay.com/oauth/api_scope",
        min_length=1,
    )
    client_id: str | None = None
    client_secret: SecretStr | None = None
    access_token: SecretStr | None = None

    model_config = ConfigDict(extra="forbid", frozen=True)

    @model_validator(mode="after")
    def validate_authentication_inputs(self) -> "EbayBrowseApiSettings":
        has_static_token = self.access_token is not None and bool(
            self.access_token.get_secret_value().strip()
        )
        has_client_credentials = bool(self.client_id and self.client_id.strip()) and (
            self.client_secret is not None and bool(self.client_secret.get_secret_value().strip())
        )

        if not has_static_token and not has_client_credentials:
            raise ValueError(
                "Provide BACKEND_EBAY_API_ACCESS_TOKEN or both BACKEND_EBAY_API_CLIENT_ID "
                "and BACKEND_EBAY_API_CLIENT_SECRET"
            )

        return self

    @property
    def rest_base_url(self) -> str:
        if self.environment is EbayApiEnvironment.SANDBOX:
            return "https://api.sandbox.ebay.com"
        return "https://api.ebay.com"

    @property
    def oauth_token_url(self) -> str:
        return f"{self.rest_base_url}/identity/v1/oauth2/token"

    @property
    def browse_search_url(self) -> str:
        return f"{self.rest_base_url}/buy/browse/v1/item_summary/search"
