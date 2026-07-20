import httpx

from app.network.models import NetworkRequest


class NetworkError(Exception):
    def __init__(self, message: str, *, method: str, url: str) -> None:
        super().__init__(message)
        self.method = method
        self.url = url


class NetworkConfigurationError(NetworkError):
    pass


class NetworkTimeoutError(NetworkError):
    pass


class NetworkTransportError(NetworkError):
    pass


class NetworkHTTPStatusError(NetworkError):
    def __init__(
        self,
        message: str,
        *,
        method: str,
        url: str,
        status_code: int,
        response_text: str,
    ) -> None:
        super().__init__(message, method=method, url=url)
        self.status_code = status_code
        self.response_text = response_text

    @classmethod
    def from_httpx(
        cls,
        request: NetworkRequest,
        response: httpx.Response,
    ) -> "NetworkHTTPStatusError":
        return cls(
            f"{request.method.value} {request.url} returned HTTP {response.status_code}",
            method=request.method.value,
            url=str(request.url),
            status_code=response.status_code,
            response_text=response.text,
        )
