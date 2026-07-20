from datetime import datetime

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, field_validator


class EbayPrice(BaseModel):
    value: str = Field(min_length=1)
    currency: str = Field(default="EUR", min_length=3, max_length=3)

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 3:
            raise ValueError("currency must be a 3-letter code")
        return normalized


class EbayImage(BaseModel):
    image_url: AnyUrl = Field(alias="imageUrl")

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class EbaySeller(BaseModel):
    username: str | None = None
    feedback_percentage: float | None = Field(
        default=None,
        alias="feedbackPercentage",
        ge=0,
        le=100,
    )

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class EbayItemLocation(BaseModel):
    city: str | None = None
    country: str | None = None

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class EbaySearchItem(BaseModel):
    item_id: str = Field(min_length=1, alias="itemId")
    title: str = Field(min_length=1)
    item_web_url: AnyUrl = Field(alias="itemWebUrl")
    price: EbayPrice
    image: EbayImage | None = None
    seller: EbaySeller | None = None
    item_location: EbayItemLocation | None = Field(default=None, alias="itemLocation")
    short_description: str | None = Field(default=None, alias="shortDescription")
    condition: str | None = None
    item_creation_date: datetime | None = Field(default=None, alias="itemCreationDate")

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class EbaySearchResponse(BaseModel):
    items: list[EbaySearchItem] = Field(default_factory=list)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)
    total: int = Field(default=0, ge=0)
    has_next: bool = False

    model_config = ConfigDict(extra="forbid", frozen=True)


class EbayBrowseApiSearchResponse(BaseModel):
    item_summaries: list[EbaySearchItem] = Field(
        default_factory=list,
        alias="itemSummaries",
    )
    limit: int = Field(default=25, ge=1)
    offset: int = Field(default=0, ge=0)
    total: int = Field(default=0, ge=0)
    next_page: str | None = Field(default=None, alias="next")

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class EbayOAuthTokenResponse(BaseModel):
    access_token: str = Field(min_length=1)
    expires_in: int = Field(gt=0)
    token_type: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid", frozen=True)
