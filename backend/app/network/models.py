from enum import Enum
from typing import Any

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, model_validator

from app.network.config import TimeoutSettings


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class NetworkRequest(BaseModel):
    method: HTTPMethod
    url: AnyUrl
    params: dict[str, str | int | float | bool] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)
    cookies: dict[str, str] = Field(default_factory=dict)
    content: bytes | None = None
    json_body: Any | None = None
    follow_redirects: bool = False
    raise_for_status: bool = True
    retry_on_failure: bool = True
    timeout: TimeoutSettings | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_payload(self) -> "NetworkRequest":
        if self.content is not None and self.json_body is not None:
            raise ValueError("content and json_body cannot be used together")
        return self
