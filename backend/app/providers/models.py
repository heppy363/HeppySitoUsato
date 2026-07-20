from datetime import UTC, datetime
from enum import Enum

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, field_validator

from app.network.config import TimeoutSettings


class ProviderStatus(str, Enum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    DISABLED = "disabled"


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=120)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @field_validator("query", mode="before")
    @classmethod
    def normalize_query(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("query cannot be blank")
        return normalized


class SearchResult(BaseModel):
    id: str = Field(min_length=1)
    external_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    platform: str = Field(min_length=1)
    location: str | None = None
    url: AnyUrl
    image_url: AnyUrl | None = None
    seller_name: str | None = None
    seller_rating: float | None = Field(default=None, ge=0)
    condition: str | None = None
    published_at: datetime | None = None
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 3:
            raise ValueError("currency must be a 3-letter code")
        return normalized

    @field_validator("title", "platform", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("text fields cannot be blank")
        return normalized


class ProviderMetadata(BaseModel):
    name: str = Field(min_length=1)
    platform: str = Field(min_length=1)
    status: ProviderStatus = ProviderStatus.ACTIVE
    default_timeout: TimeoutSettings | None = None
    supports_pagination: bool = True
    max_page_size: int = Field(default=100, ge=1, le=100)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @field_validator("name", "platform", mode="before")
    @classmethod
    def normalize_identity_fields(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider identity fields cannot be blank")
        return normalized
