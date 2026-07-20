# HeppySitoUsato Backend

Backend FastAPI inizializzato come base del progetto.

## Stato attuale

Il backend include:

* bootstrap FastAPI con settings centralizzati;
* package `app/network/` con contratto `NetworkClient`, implementazione `HttpxNetworkClient`, modelli di richiesta e gerarchia di errori;
* package `app/providers/` con contratto `MarketplaceProvider`, modelli condivisi di ricerca, registry runtime dei provider e mapping degli errori provider;
* package `app/providers/ebay/` con struttura concreta del provider, adapter mockato e adapter ufficiale `Browse API`, autenticazione OAuth applicativa e mapper verso `SearchResult`;
* lifespan FastAPI che costruisce un solo `HttpxNetworkClient` condiviso e registra `EbayProvider` in un `ProviderRegistry` esposto in `app.state` quando la configurazione eBay e disponibile;
* configurazione `BACKEND_NETWORK_*` per timeout, limiti di connessione, retry, HTTP/2 opzionale e strategia proxy tipizzata (`direct`, `datacenter`, `residential`, `tor`);
* configurazione `BACKEND_EBAY_API_*` per ambiente (`production` o `sandbox`), marketplace, scope OAuth e credenziali/token dell'integrazione eBay;
* test backend e test del network layer basati su `httpx.MockTransport`.

## Verifica locale

```bash
poetry check
poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q
poetry run ruff check . --no-cache
poetry run ruff format --check . --no-cache
```
