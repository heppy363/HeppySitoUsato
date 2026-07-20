"""Network layer package."""

from app.network.client import HttpxNetworkClient, NetworkClient
from app.network.config import (
    ConnectionLimitsSettings,
    NetworkSettings,
    ProxySettings,
    ProxyStrategy,
    RetrySettings,
    TimeoutSettings,
)
from app.network.exceptions import (
    NetworkConfigurationError,
    NetworkError,
    NetworkHTTPStatusError,
    NetworkTimeoutError,
    NetworkTransportError,
)
from app.network.models import HTTPMethod, NetworkRequest
from app.network.proxy import (
    DatacenterProxyProvider,
    DirectProxyProvider,
    ProxyProvider,
    ResidentialProxyProvider,
    TorProxyProvider,
    build_proxy_provider,
)

__all__ = [
    "ConnectionLimitsSettings",
    "DatacenterProxyProvider",
    "DirectProxyProvider",
    "HTTPMethod",
    "HttpxNetworkClient",
    "NetworkClient",
    "NetworkConfigurationError",
    "NetworkError",
    "NetworkHTTPStatusError",
    "NetworkRequest",
    "NetworkSettings",
    "NetworkTimeoutError",
    "NetworkTransportError",
    "ProxyProvider",
    "ProxySettings",
    "ProxyStrategy",
    "ResidentialProxyProvider",
    "RetrySettings",
    "TorProxyProvider",
    "TimeoutSettings",
    "build_proxy_provider",
]
