from abc import ABC, abstractmethod
from urllib.parse import quote, urlsplit, urlunsplit

from app.network.config import ProxySettings, ProxyStrategy


class ProxyProvider(ABC):
    @property
    @abstractmethod
    def strategy(self) -> ProxyStrategy:
        raise NotImplementedError

    @abstractmethod
    def get_proxy_url(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def safe_label(self) -> str:
        raise NotImplementedError


class DirectProxyProvider(ProxyProvider):
    @property
    def strategy(self) -> ProxyStrategy:
        return ProxyStrategy.DIRECT

    def get_proxy_url(self) -> str | None:
        return None

    def safe_label(self) -> str:
        return self.strategy.value


class StaticProxyProvider(ProxyProvider):
    def __init__(self, settings: ProxySettings) -> None:
        self._settings = settings

    @property
    def strategy(self) -> ProxyStrategy:
        return self._settings.strategy

    def get_proxy_url(self) -> str | None:
        if self._settings.url is None:
            raise ValueError(f"{self.strategy.value} proxy strategy requires a proxy url")

        parsed = urlsplit(self._settings.url)
        if not parsed.scheme or not parsed.hostname:
            raise ValueError("proxy url must include scheme and host")

        if (parsed.username is not None or parsed.password is not None) and (
            self._settings.username is not None or self._settings.password is not None
        ):
            raise ValueError("proxy credentials are ambiguous between url and dedicated fields")

        if self._settings.username is None:
            return self._settings.url

        userinfo = quote(self._settings.username, safe="")
        if self._settings.password is not None:
            password = self._settings.password.get_secret_value()
            userinfo = f"{userinfo}:{quote(password, safe='')}"

        netloc = f"{userinfo}@{parsed.hostname}"
        if parsed.port is not None:
            netloc = f"{netloc}:{parsed.port}"

        return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))

    def safe_label(self) -> str:
        if self._settings.url is None:
            return self.strategy.value

        parsed = urlsplit(self._settings.url)
        host = parsed.hostname or "configured-proxy"
        if parsed.port is not None:
            host = f"{host}:{parsed.port}"

        return f"{self.strategy.value}://{host}"


class DatacenterProxyProvider(StaticProxyProvider):
    pass


class ResidentialProxyProvider(StaticProxyProvider):
    pass


class TorProxyProvider(StaticProxyProvider):
    pass


def build_proxy_provider(settings: ProxySettings) -> ProxyProvider:
    if settings.strategy is ProxyStrategy.DIRECT:
        return DirectProxyProvider()

    provider_map = {
        ProxyStrategy.DATACENTER: DatacenterProxyProvider,
        ProxyStrategy.RESIDENTIAL: ResidentialProxyProvider,
        ProxyStrategy.TOR: TorProxyProvider,
    }
    return provider_map[settings.strategy](settings)
