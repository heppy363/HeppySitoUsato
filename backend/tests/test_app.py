from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.network import HttpxNetworkClient
from app.providers import EbayProvider


def test_create_app_uses_expected_metadata() -> None:
    app = create_app()

    assert app.title == "HeppySitoUsato API"
    assert app.version == "0.1.0"


def test_create_app_registers_shared_network_client_and_ebay_provider_when_configured() -> None:
    app = create_app(Settings(ebay_api_access_token="static-token"))

    with TestClient(app):
        assert isinstance(app.state.network_client, HttpxNetworkClient)
        assert isinstance(app.state.ebay_provider, EbayProvider)
        assert app.state.providers["ebay"] is app.state.ebay_provider
        assert app.state.network_client.is_closed is False

    assert app.state.network_client.is_closed is True


def test_create_app_skips_ebay_provider_when_runtime_auth_is_missing() -> None:
    app = create_app(Settings())

    with TestClient(app):
        assert isinstance(app.state.network_client, HttpxNetworkClient)
        assert app.state.ebay_provider is None
        assert app.state.providers == {}
