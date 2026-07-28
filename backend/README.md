# HeppySitoUsato Backend

Backend FastAPI inizializzato come base del progetto.

## Stato attuale

Il backend include:

* bootstrap FastAPI con settings centralizzati;
* endpoint `GET /health` con response model tipizzato e stato HTTP coerente (`200` quando backend, Redis e database sono operativi; `503` in caso di stato degradato);
* endpoint `GET /search` con validazione della query, paginazione, selezione piattaforme, filtri prezzo, primo parametro `sort` configurabile (`relevance`, `price_asc`), rate limiting per client configurabile, risposta aggregata tipizzata, errori `400` e `429` e schema OpenAPI generato automaticamente;
* package `app/network/` con contratto `NetworkClient`, implementazione `HttpxNetworkClient`, modelli di richiesta e gerarchia di errori;
* package `app/providers/` con contratto `MarketplaceProvider`, modelli condivisi di ricerca, registry runtime dei provider e mapping degli errori provider;
* package `app/services/` con il primo contratto dell'Aggregation Engine sopra `ProviderRegistry`, basato su `AggregationRequest`, `AggregationResponse`, `AggregationMetrics`, `RegistryAggregationService`, `RankingService` e `SearchSortOption`, con esecuzione parallela iniziale via `asyncio.gather`, deduplicazione per `(platform, external_id)`, primo merge conservativo, ranking euristico iniziale, primi filtri prezzo, ordinamento finale deterministico con modalita configurabile iniziale (`relevance`, `price_asc`) e metriche iniziali di provider, pipeline e durata della ricerca aggregata, oltre a `RuntimeHealthService` per i controlli di backend, Redis e database;
* package `app/providers/ebay/` con struttura concreta del provider, adapter mockato e adapter ufficiale `Browse API`, autenticazione OAuth applicativa e mapper verso `SearchResult`;
* lifespan FastAPI che costruisce un solo `HttpxNetworkClient` condiviso, registra `RuntimeHealthService` e registra `EbayProvider` in un `ProviderRegistry` esposto in `app.state` quando la configurazione eBay e disponibile;
* configurazione `BACKEND_NETWORK_*` per timeout, limiti di connessione, retry, HTTP/2 opzionale e strategia proxy tipizzata (`direct`, `datacenter`, `residential`, `tor`);
* configurazione `BACKEND_EBAY_API_*` per ambiente (`production` o `sandbox`), marketplace, scope OAuth e credenziali/token dell'integrazione eBay;
* configurazione `BACKEND_SEARCH_RATE_LIMIT_*` per il limite dedicato in-memory e per singola istanza di `GET /search`;
* test backend, health endpoint, search endpoint e network layer basati su `httpx.MockTransport` e fixture locali.

## Verifica locale

```bash
poetry check
poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py tests/test_health.py tests/test_search.py -q
poetry run ruff check . --no-cache
poetry run ruff format --check . --no-cache
```

## Nota operativa

Il controllo database di `GET /health` restituisce `driver_not_installed` se il driver `asyncpg` non e disponibile nell'ambiente locale o se la macro area PostgreSQL non e ancora stata completata.
