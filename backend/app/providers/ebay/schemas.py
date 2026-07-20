from datetime import datetime

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, field_validator


class EbayPrice(BaseModel):
    value: str = Field(min_length=1)
    currency: str = Field(default="EUR", min_length=3, max_length=3)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        normalized = value.strip().upper()
        if len(normalized) != 3:
            raise ValueError("currency must be a 3-letter code")
        return normalized


class EbayImage(BaseModel):
    image_url: AnyUrl

    model_config = ConfigDict(extra="forbid", frozen=True)


class EbaySeller(BaseModel):
    username: str | None = None
    feedback_percentage: float | None = Field(default=None, ge=0, le=100)

    model_config = ConfigDict(extra="forbid", frozen=True)


class EbayItemLocation(BaseModel):
    city: str | None = None
    country: str | None = None

    model_config = ConfigDict(extra="forbid", frozen=True)


class EbaySearchItem(BaseModel):
    item_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    item_web_url: AnyUrl
    price: EbayPrice
    image: EbayImage | None = None
    seller: EbaySeller | None = None
    item_location: EbayItemLocation | None = None
    short_description: str | None = None
    condition: str | None = None
    item_creation_date: datetime | None = None

    model_config = ConfigDict(extra="forbid", frozen=True)


class EbaySearchResponse(BaseModel):
    items: list[EbaySearchItem] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid", frozen=True)
