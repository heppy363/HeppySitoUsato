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
* cache applicativa con contratto `SearchCache`, implementazione `RedisSearchCache`, serializzazione tipizzata di `AggregationResponse`, chiavi deterministiche versionate, TTL esplicito e comportamento fail-open, integrata tramite `CachedAggregationService` prima e dopo l'esecuzione dei provider, con metriche per hit, miss ed errori nella risposta aggregata;
* package `app/database/` con configurazione SQLAlchemy 2.x asincrona, engine condiviso, factory `async_sessionmaker`, context manager di sessione con rollback degli errori e chiusura deterministica, metadata ORM condiviso con naming convention stabile e helper per Alembic;
* struttura `migrations/` con `alembic.ini`, environment asincrono e directory `versions/` pronta per le revision future senza introdurre tabelle applicative premature;
* package `app/providers/ebay/` con struttura concreta del provider, adapter mockato e adapter ufficiale `Browse API`, autenticazione OAuth applicativa e mapper verso `SearchResult`;
* lifespan FastAPI che costruisce e chiude un solo `HttpxNetworkClient`, un solo `RedisSearchCache` e un solo `DatabaseSessionManager` condivisi, registra `RuntimeHealthService` e registra `EbayProvider` in un `ProviderRegistry` esposto in `app.state` quando la configurazione eBay e disponibile;
* configurazione `BACKEND_NETWORK_*` per timeout, limiti di connessione, retry, HTTP/2 opzionale e strategia proxy tipizzata (`direct`, `datacenter`, `residential`, `tor`);
* configurazione `BACKEND_EBAY_API_*` per ambiente (`production` o `sandbox`), marketplace, scope OAuth e credenziali/token dell'integrazione eBay;
* configurazione `BACKEND_SEARCH_RATE_LIMIT_*` per il limite dedicato in-memory e per singola istanza di `GET /search`;
* configurazione `BACKEND_SEARCH_CACHE_TTL_SECONDS` con TTL iniziale di 300 secondi per la futura implementazione Redis;
* configurazione `BACKEND_DATABASE_*` per URL asincrona, logging SQL e verifica preventiva delle connessioni;
* test backend, health endpoint, sessioni database, search endpoint e network layer basati su mock e fixture locali;
* test di integrazione Docker-gated che avviano PostgreSQL 16 in un progetto Compose isolato e verificano sia `DatabaseSessionManager.check_connection()` sia `alembic upgrade head` senza creare tabelle applicative nel database pubblico.

## Verifica locale

```bash
poetry check
poetry run pytest tests/test_alembic.py tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py tests/test_health.py tests/test_search.py tests/test_rate_limit.py tests/test_cache.py tests/test_database.py -q
poetry run ruff check . --no-cache
poetry run ruff format --check . --no-cache
```

## Verifica integrazione Docker

```powershell
$env:RUN_DOCKER_INTEGRATION_TESTS="1"
poetry run pytest tests/test_database_integration.py -q
```

Questi test richiedono Docker Desktop o un daemon Docker equivalente attivo; in caso contrario vengono saltati con una motivazione esplicita.

## Nota operativa

Il controllo database di `GET /health` usa l'engine condiviso e resta degradato finche il servizio PostgreSQL non e raggiungibile. Alembic e configurato in modalita asincrona sopra il metadata condiviso; i test di integrazione Docker verificano la connettivita live e l'esecuzione di `upgrade head`, ma la prima revisione applicativa resta volutamente assente.
