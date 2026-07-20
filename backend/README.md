# HeppySitoUsato Backend

Backend FastAPI inizializzato come base del progetto.

## Stato attuale

Il backend include:

* bootstrap FastAPI con settings centralizzati;
* package `app/network/` con contratto `NetworkClient`, implementazione `HttpxNetworkClient`, modelli di richiesta e gerarchia di errori;
* package `app/providers/` con contratto `MarketplaceProvider`, modelli condivisi di ricerca e mapping degli errori provider;
* configurazione `BACKEND_NETWORK_*` per timeout, limiti di connessione, retry, HTTP/2 opzionale e strategia proxy tipizzata (`direct`, `datacenter`, `residential`, `tor`);
* test backend e test del network layer basati su `httpx.MockTransport`.

## Verifica locale

```bash
poetry check
poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py -q
poetry run ruff check . --no-cache
poetry run ruff format --check . --no-cache
```
