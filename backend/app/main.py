from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import Settings, get_settings
from app.network import HttpxNetworkClient
from app.providers import maybe_build_ebay_provider


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        network_client = HttpxNetworkClient(app_settings.build_network_settings())
        app.state.network_client = network_client
        app.state.providers = {}
        app.state.ebay_provider = maybe_build_ebay_provider(
            settings=app_settings,
            network_client=network_client,
        )
        if app.state.ebay_provider is not None:
            app.state.providers["ebay"] = app.state.ebay_provider

        try:
            yield
        finally:
            await network_client.aclose()

    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        debug=app_settings.debug,
        lifespan=lifespan,
    )
    app.state.settings = app_settings
    app.include_router(api_router)
    return app


app = create_app()
