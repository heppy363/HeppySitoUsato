from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.providers import SearchRequest, SearchResult
from app.services.aggregation import (
    AggregationMetrics,
    AggregationProviderFailure,
    AggregationRequest,
    AggregationResponse,
)


class SearchQueryParams(BaseModel):
    query: str = Field(min_length=1, max_length=120)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)
    platforms: list[str] | None = None
    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @field_validator("query", mode="before")
    @classmethod
    def normalize_query(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("query cannot be blank")
        return normalized

    @model_validator(mode="after")
    def validate_price_range(self) -> "SearchQueryParams":
        if self.min_price is not None and self.max_price is not None:
            if self.min_price > self.max_price:
                raise ValueError("min_price cannot be greater than max_price")
        return self

    def to_aggregation_request(self) -> AggregationRequest:
        return AggregationRequest(
            search=SearchRequest(
                query=self.query,
                page=self.page,
                page_size=self.page_size,
            ),
            platforms=self.platforms,
            min_price=self.min_price,
            max_price=self.max_price,
        )


class SearchErrorCode(str, Enum):
    UNKNOWN_PLATFORM = "unknown_platform"


class SearchErrorResponse(BaseModel):
    error_code: SearchErrorCode
    detail: str = Field(min_length=1)
    unknown_platforms: tuple[str, ...] = Field(default_factory=tuple)

    model_config = ConfigDict(extra="forbid", frozen=True)


class SearchResponse(BaseModel):
    results: tuple[SearchResult, ...] = Field(default_factory=tuple)
    failures: tuple[AggregationProviderFailure, ...] = Field(default_factory=tuple)
    metrics: AggregationMetrics = Field(default_factory=AggregationMetrics)

    model_config = ConfigDict(extra="forbid", frozen=True)

    @classmethod
    def from_aggregation_response(cls, response: AggregationResponse) -> "SearchResponse":
        return cls(
            results=response.results,
            failures=response.failures,
            metrics=response.metrics,
        )
