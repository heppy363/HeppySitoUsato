from collections.abc import Iterable, Iterator

from app.providers.base import MarketplaceProvider


class ProviderRegistry:
    def __init__(self, providers: Iterable[MarketplaceProvider] | None = None) -> None:
        self._providers: dict[str, MarketplaceProvider] = {}
        for provider in providers or ():
            self.register(provider)

    def register(self, provider: MarketplaceProvider) -> None:
        platform = provider.metadata.platform
        self._providers[platform] = provider

    def get(self, platform: str) -> MarketplaceProvider | None:
        return self._providers.get(platform)

    def all(self) -> tuple[MarketplaceProvider, ...]:
        return tuple(self._providers.values())

    def items(self) -> tuple[tuple[str, MarketplaceProvider], ...]:
        return tuple(self._providers.items())

    @property
    def platforms(self) -> tuple[str, ...]:
        return tuple(self._providers.keys())

    def __contains__(self, platform: str) -> bool:
        return platform in self._providers

    def __getitem__(self, platform: str) -> MarketplaceProvider:
        return self._providers[platform]

    def __iter__(self) -> Iterator[MarketplaceProvider]:
        return iter(self._providers.values())

    def __len__(self) -> int:
        return len(self._providers)
