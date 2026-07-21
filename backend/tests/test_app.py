from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.network import HttpxNetworkClient
from app.providers import EbayProvider, ProviderRegistry
from app.services import RegistryAggregationService


def test_create_app_uses_expected_metadata() -> None:
    app = create_app()

    assert app.title == "HeppySitoUsato API"
    assert app.version == "0.1.0"


def test_create_app_registers_shared_network_client_and_ebay_provider_when_configured() -> None:
    app = create_app(Settings(ebay_api_access_token="static-token"))

    with TestClient(app):
        assert isinstance(app.state.network_client, HttpxNetworkClient)
        assert isinstance(app.state.providers, ProviderRegistry)
        assert isinstance(app.state.aggregation_service, RegistryAggregationService)
        assert app.state.aggregation_service.provider_registry is app.state.providers
        assert isinstance(app.state.ebay_provider, EbayProvider)
        assert app.state.providers["ebay"] is app.state.ebay_provider
        assert app.state.providers.get("ebay") is app.state.ebay_provider
        assert app.state.providers.platforms == ("ebay",)
        assert app.state.network_client.is_closed is False

    assert app.state.network_client.is_closed is True


def test_create_app_skips_ebay_provider_when_runtime_auth_is_missing() -> None:
    app = create_app(Settings())

    with TestClient(app):
        assert isinstance(app.state.network_client, HttpxNetworkClient)
        assert app.state.ebay_provider is None
        assert isinstance(app.state.providers, ProviderRegistry)
        assert isinstance(app.state.aggregation_service, RegistryAggregationService)
        assert app.state.aggregation_service.provider_registry is app.state.providers
        assert len(app.state.providers) == 0
