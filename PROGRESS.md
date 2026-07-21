# PROGRESSO E TRACCIAMENTO DEL PROGETTO

## Scopo del Documento

Questo documento rappresenta la fonte ufficiale per il monitoraggio dello stato di avanzamento del progetto.

Deve consentire di confrontare continuamente:

* requisiti iniziali;
* roadmap prevista;
* funzionalità implementate;
* funzionalità mancanti;
* modifiche tecniche effettuate;
* test eseguiti;
* problemi rilevati;
* decisioni architetturali;
* deviazioni rispetto ai documenti originali.

Codex deve aggiornare questo file al termine di ogni micro-modifica.

Il documento non deve descrivere attività future come se fossero già state completate.

Ogni stato deve essere supportato da codice realmente presente e, quando possibile, da test eseguiti con successo.

---

# 1. Documenti di Riferimento

Lo stato del progetto deve essere confrontato con i seguenti documenti:

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`

In caso di conflitto, Codex deve segnalarlo nella sezione:

```text
Deviazioni e Incongruenze
```

Codex non deve modificare silenziosamente i requisiti.

---

# 2. Regole di Aggiornamento

Codex deve aggiornare questo documento dopo ogni attività che comporti almeno una delle seguenti modifiche:

* creazione di un nuovo file;
* modifica di codice applicativo;
* modifica di configurazioni;
* aggiunta o rimozione di dipendenze;
* aggiunta di un servizio Docker;
* introduzione di un endpoint;
* modifica di un modello dati;
* introduzione di un provider;
* aggiunta di test;
* modifica dello schema del database;
* modifica della cache;
* modifica del frontend;
* correzione di un bug;
* modifica dell'architettura;
* modifica delle variabili d'ambiente;
* aggiornamento della documentazione.

Codex non deve aggiornare lo stato di una voce come completato se:

* il codice non è presente;
* il codice è incompleto;
* i test non sono stati eseguiti;
* l'esecuzione ha generato errori;
* manca una dipendenza necessaria;
* la funzionalità è stata soltanto simulata;
* sono presenti blocchi esterni non risolti.

---

# 3. Legenda degli Stati

Utilizzare esclusivamente i seguenti stati.

| Stato           | Significato                                         |
| --------------- | --------------------------------------------------- |
| `NON INIZIATO`  | Nessuna implementazione presente                    |
| `ANALISI`       | Requisiti e struttura in fase di analisi            |
| `IN SVILUPPO`   | Implementazione iniziata ma non completa            |
| `BLOCCATO`      | Attività non completabile a causa di un impedimento |
| `DA VERIFICARE` | Codice presente ma verifica incompleta              |
| `COMPLETATO`    | Codice implementato e verificato                    |
| `DA MIGLIORARE` | Funzionalità operativa ma con limiti noti           |
| `DEPRECATO`     | Componente ancora presente ma da rimuovere          |
| `RIMOSSO`       | Componente eliminato dal progetto                   |

---

# 4. Stato Generale del Progetto

## Stato Corrente

```text
IN SVILUPPO
```

## Fase Corrente

```text
Ordinamento finale iniziale dei risultati aggregati
```

## Percentuale Indicativa

```text
68%
```

La percentuale è indicativa e non deve essere calcolata esclusivamente sul numero di file creati.

Deve riflettere il completamento reale delle macro aree previste nella roadmap.

## Ultimo Aggiornamento

```text
Data: 2026-07-21
Responsabile: Codex
Attivita: Introduzione dell'ordinamento finale deterministico dei risultati aggregati dopo ranking e filtri
```

## Prossimo Passo Approvato

```text
Generare le prime metriche dell'Aggregation Engine.
```

Codex non deve iniziare automaticamente attività successive oltre il prossimo passo approvato.

---

# 5. Riepilogo Macro Aree

| Macro Area              | Stato        | Avanzamento | Note                              |
| ----------------------- | ------------ | ----------: | --------------------------------- |
| Infrastruttura e Docker | IN SVILUPPO  |         45% | Dockerfile backend/frontend allineati, avvio stack da completare |
| Configurazione Backend  | IN SVILUPPO  |         95% | Poetry, lockfile, struttura FastAPI, lifecycle applicativo, registry provider runtime, primi contratti di aggregazione con esecuzione parallela, modelli normalizzati validati e configurazione eBay ufficiale |
| Network Layer           | IN SVILUPPO  |         79% | Client condiviso, configurazione proxy astratta, lifecycle con chiusura verificata e test mockati presenti; restano da definire i contratti marketplace |
| Marketplace Provider    | IN SVILUPPO  |         72% | Contratto comune, `ProviderRegistry` runtime, `EbayProvider` con factory runtime, adapter mockato, adapter Browse API ufficiale e test presenti; verifica live ancora assente |
| Aggregation Engine      | IN SVILUPPO  |         72% | Contratto registry-backed presente con selezione provider, `asyncio.gather`, isolamento dei fallimenti, raccolta di risultati parziali, deduplicazione per `(platform, external_id)`, primo merge conservativo, ranking euristico iniziale, primi filtri prezzo e ordinamento finale deterministico; metriche ancora assenti |
| Cache Redis             | NON INIZIATO |          0% | Solo servizio Docker, cache applicativa assente |
| PostgreSQL e Migrazioni | NON INIZIATO |          0% | Solo servizio Docker, ORM e Alembic assenti |
| Worker e Code           | NON INIZIATO |          0% | Solo placeholder Docker, tecnologia non selezionata |
| API FastAPI             | NON INIZIATO |          0% | Nessun endpoint presente          |
| Streaming Risultati     | NON INIZIATO |          0% | SSE o WebSocket non definiti      |
| Frontend Vue            | IN SVILUPPO  |         50% | Vite, struttura Vue e immagine Docker inizializzati |
| State Management        | IN SVILUPPO  |         15% | Pinia configurato con store iniziale |
| Server State            | IN SVILUPPO  |         15% | TanStack Query configurato con query client base |
| Interfaccia Grafica     | IN SVILUPPO  |         10% | Shell UI iniziale presente, feature di ricerca assenti |
| Testing                 | IN SVILUPPO  |         78% | Test backend, network layer, lifecycle applicativo, `ProviderRegistry`, aggregazione parallela con errore parziale, deduplicazione, merge iniziale, ranking euristico, filtri prezzo, ordinamento finale e validazione modelli con primo provider concreto e adapter ufficiale presenti |
| Monitoring              | IN SVILUPPO  |         10% | Servizi base presenti, metriche e dashboard da implementare |
| Sicurezza               | NON INIZIATO |          0% | Controlli non implementati        |
| Documentazione          | IN SVILUPPO  |         99% | Documenti principali verificati, variabili eBay documentate e progresso aggiornato |

---

# 6. Tracciamento della Roadmap

## Macro Area 1 - Configurazione Infrastruttura

### Step 1 - Docker Compose

**Stato:** `DA VERIFICARE`

#### Requisiti

* [x] Creare `docker-compose.yml`
* [x] Utilizzare una versione compatibile con Docker Compose moderno
* [x] Configurare rete interna bridge
* [x] Configurare servizio backend
* [x] Configurare servizio frontend
* [x] Configurare Redis
* [x] Configurare PostgreSQL
* [x] Configurare worker
* [x] Configurare proxy layer
* [x] Configurare Prometheus
* [x] Configurare Grafana
* [x] Aggiungere healthcheck
* [x] Evitare esposizione di porte non necessarie
* [x] Configurare volumi persistenti
* [x] Configurare variabili d'ambiente
* [ ] Verificare avvio completo dello stack

#### File Previsti

```text
docker-compose.yml
.env.example
docker/
```

#### Test Previsti

```bash
docker compose config
docker compose up --build
docker compose ps
```

#### Evidenze

```text
File creati: `docker-compose.yml`, `.env.example`, `.gitignore`, `docker/`, `backend/`, `frontend/`
Servizi configurati: backend, frontend, redis, postgres, worker, proxy, prometheus, grafana
Placeholder introdotti: backend, frontend, worker e proxy per consentire la validazione iniziale dello stack
Verifica eseguita: `docker compose config` superato
Blocco attuale: `docker compose up --build -d` non completabile per daemon Docker locale non disponibile
Aggiornamento successivo: i Dockerfile di backend e frontend sono ora collegati agli ambienti applicativi reali
```

---

### Step 2 - Ambienti Backend e Frontend

**Stato:** `DA VERIFICARE`

#### Requisiti Backend

* [x] Python 3.11
* [x] Poetry
* [x] `pyproject.toml`
* [x] Lockfile Poetry
* [x] FastAPI
* [x] Uvicorn
* [x] Pydantic
* [x] Configurazione linting
* [x] Configurazione formatting
* [x] Struttura modulare iniziale

#### Requisiti Frontend

* [x] Vue 3
* [x] Vite
* [x] Composition API
* [x] `<script setup>`
* [x] Pinia
* [x] TanStack Vue Query
* [x] Tailwind CSS
* [x] Struttura modulare iniziale

#### Evidenze

```text
Backend creato con `pyproject.toml`, `poetry.lock`, struttura `app/` modulare e test iniziale in `tests/test_app.py`
Frontend creato con `package.json`, `package-lock.json`, Vite, Vue 3, Pinia, TanStack Query, Tailwind e struttura `src/`
Verifiche riuscite: `poetry check`, `poetry run python -c "from app.main import create_app..."`, `poetry run ruff check . --no-cache`, `poetry run ruff format --check . --no-cache`, `npm exec vite build -- --configLoader runner`, `docker compose config`
Vincoli emersi: Python 3.11 non disponibile come runtime host locale, ma disponibile nell'immagine Docker del backend
Aggiornamenti successivi: i Dockerfile `docker/backend` e `docker/frontend` sono stati allineati agli ambienti applicativi e il test backend ora termina correttamente con `pytest`
```

---

# 7. Core Backend e Network Layer

## Step 3 - Network Client Centralizzato

**Stato:** `COMPLETATO`

#### Requisiti

* [x] Creare interfaccia del network client
* [x] Utilizzare `httpx.AsyncClient`
* [x] Supportare HTTP/2 quando compatibile
* [x] Configurare timeout espliciti
* [x] Configurare limiti di connessione
* [x] Gestire proxy intercambiabili
* [x] Gestire retry controllati
* [x] Gestire jitter configurabile
* [x] Gestire header comuni
* [x] Gestire cookie
* [x] Gestire logging strutturato
* [x] Gestire chiusura del client
* [x] Gestire errori HTTP
* [x] Gestire errori di rete
* [x] Evitare configurazioni hardcoded
* [x] Aggiungere test con richieste mockate

#### File Previsti

```text
backend/app/network/
├── client.py
├── config.py
├── exceptions.py
└── models.py
```

#### Evidenze

```text
File creati: `backend/app/network/client.py`, `backend/app/network/config.py`, `backend/app/network/exceptions.py`, `backend/app/network/models.py`, `backend/app/network/proxy.py`, `backend/tests/test_network.py`
File modificati: `backend/app/core/config.py`, `backend/app/network/__init__.py`, `.env.example`, `backend/README.md`
Contratti introdotti: `NetworkClient`, `HttpxNetworkClient`, `NetworkSettings`, `ProxyProvider`, `ProxySettings`, `NetworkRequest` e gerarchia `NetworkError`
Coperture incluse: timeout espliciti, limiti di connessione, retry con backoff e jitter, header comuni, cookie, mapping errori HTTP/trasporto, strategie proxy `direct`/`datacenter`/`residential`/`tor`, credenziali proxy via variabili d'ambiente e fallback a HTTP/1.1 quando `h2` non e disponibile
Verifiche riuscite: `poetry check`, `poetry run pytest tests/test_app.py tests/test_network.py -q`, `poetry run ruff check . --no-cache`, `poetry run ruff format --check . --no-cache`
```

---

## Proxy Provider

**Stato:** `COMPLETATO`

#### Requisiti

* [x] Definire interfaccia `ProxyProvider`
* [x] Implementare configurazione diretta
* [x] Implementare configurazione Tor opzionale
* [x] Prevedere provider datacenter
* [x] Prevedere provider residential
* [x] Gestire credenziali tramite variabili d'ambiente
* [x] Non vincolare il backend a una sola tecnologia
* [x] Gestire proxy non disponibile
* [x] Aggiungere test unitari

#### Evidenze

```text
File creato: `backend/app/network/proxy.py`
File modificati: `backend/app/network/config.py`, `backend/app/network/client.py`, `backend/app/network/__init__.py`, `backend/app/core/config.py`, `backend/tests/test_network.py`, `.env.example`, `backend/README.md`
Contratti introdotti: `ProxyProvider`, `DirectProxyProvider`, `DatacenterProxyProvider`, `ResidentialProxyProvider`, `TorProxyProvider`, `ProxySettings`, `ProxyStrategy`
Verifiche riuscite: test di risoluzione provider, credenziali, configurazione diretta e mapping della non disponibilita del proxy verso `NetworkTransportError`
```

#### Nota di Conformità

Il proxy layer deve essere utilizzato nel rispetto:

* dei termini di servizio;
* dei limiti di frequenza;
* delle API ufficiali disponibili;
* delle normative applicabili;
* delle autorizzazioni di accesso.

Non devono essere implementate tecniche per superare autenticazione, CAPTCHA, paywall o controlli di accesso.

---

# 8. Marketplace Provider

## Interfaccia Comune

**Stato:** `COMPLETATO`

#### Requisiti

* [x] Definire `MarketplaceProvider`
* [x] Definire metodo asincrono `search`
* [x] Definire modelli di input
* [x] Definire modelli di output
* [x] Definire eccezioni comuni
* [x] Definire stato del provider
* [x] Definire timeout specifico
* [x] Definire normalizzazione
* [x] Definire mapping degli errori
* [x] Aggiungere test del contratto

#### Evidenze

```text
File creati: `backend/app/providers/base.py`, `backend/app/providers/models.py`, `backend/app/providers/exceptions.py`, `backend/tests/test_providers.py`
File modificati: `backend/app/providers/__init__.py`, `backend/README.md`
Contratti introdotti: `MarketplaceProvider`, `SearchRequest`, `SearchResult`, `ProviderMetadata`, `ProviderStatus` e gerarchia `ProviderError`
Coperture incluse: metodo asincrono `search`, normalizzazione, validazione provider, timeout specifico via `TimeoutSettings`, mapping degli errori di rete e test del contratto con provider dummy
Verifiche riuscite: `poetry check`, `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py -q`, `poetry run ruff check . --no-cache`, `poetry run ruff format --check . --no-cache`
```

---

## eBay Provider

**Stato:** `DA VERIFICARE`

* [x] Valutare API ufficiali disponibili
* [x] Definire autenticazione quando necessaria
* [x] Implementare ricerca
* [x] Normalizzare risultati
* [x] Gestire paginazione
* [x] Gestire errori
* [x] Gestire risultati incompleti
* [x] Aggiungere mock
* [x] Aggiungere test

#### Evidenze

```text
File creati: `backend/app/providers/ebay/__init__.py`, `backend/app/providers/ebay/schemas.py`, `backend/app/providers/ebay/mapper.py`, `backend/app/providers/ebay/exceptions.py`, `backend/app/providers/ebay/provider.py`, `backend/app/providers/ebay/adapter.py`, `backend/app/providers/ebay/config.py`, `backend/app/providers/ebay/auth.py`, `backend/app/providers/ebay/factory.py`, `backend/app/providers/registry.py`, `backend/tests/test_ebay_provider.py`
File modificati: `backend/app/core/config.py`, `backend/app/main.py`, `backend/app/network/client.py`, `.env.example`, `backend/app/providers/__init__.py`, `backend/tests/test_app.py`, `backend/tests/test_providers.py`, `backend/README.md`
Componenti introdotti: `ProviderRegistry`, `EbayProvider`, `EbaySearchAdapter`, `MockEbaySearchAdapter`, `EbayBrowseApiSearchAdapter`, `EbayBrowseApiSettings`, `EbayAccessTokenProvider`, `StaticEbayAccessTokenProvider`, `ClientCredentialsEbayAccessTokenProvider`, `build_ebay_provider`, `maybe_build_ebay_provider`, wiring runtime in `app.state` e schemi raw `EbaySearchItem`/`EbaySearchResponse` con risposte ufficiali Browse API/OAuth
Verifiche riuscite: valutazione della Browse API ufficiale eBay, autenticazione OAuth applicativa via client credentials o token statico, mapping normalizzato, gestione degli errori di rete, gestione di payload incompleti, ricerca tramite adapter mockato, ricerca tramite adapter ufficiale con header `Authorization` e `X-EBAY-C-MARKETPLACE-ID`, costruzione runtime di `EbayProvider` da `Settings`, riuso di un solo `NetworkClient` condiviso nel lifespan FastAPI e registry condiviso dei provider runtime
Limite aperto: l'integrazione eBay resta verificata solo tramite test locali e mock, quindi manca ancora una verifica live con credenziali e accesso effettivo all'API.
```

---

## Subito Provider

**Stato:** `IN SVILUPPO`

* [ ] Verificare modalità di accesso consentite
* [ ] Individuare una sorgente dati stabile e autorizzata
* [ ] Implementare ricerca
* [ ] Normalizzare risultati
* [ ] Gestire paginazione
* [ ] Gestire errori
* [ ] Gestire risultati incompleti
* [ ] Aggiungere mock
* [ ] Aggiungere test

---

## Wallapop Provider

**Stato:** `NON INIZIATO`

* [ ] Verificare modalità di accesso consentite
* [ ] Individuare una sorgente dati stabile e autorizzata
* [ ] Implementare ricerca
* [ ] Normalizzare risultati
* [ ] Gestire paginazione
* [ ] Gestire errori
* [ ] Gestire risultati incompleti
* [ ] Aggiungere mock
* [ ] Aggiungere test

---

## Vinted Provider

**Stato:** `NON INIZIATO`

* [ ] Verificare modalità di accesso consentite
* [ ] Individuare una sorgente dati stabile e autorizzata
* [ ] Implementare ricerca
* [ ] Normalizzare risultati
* [ ] Gestire paginazione
* [ ] Gestire errori
* [ ] Gestire risultati incompleti
* [ ] Aggiungere mock
* [ ] Aggiungere test

---

# 9. Modelli Normalizzati

**Stato:** `DA MIGLIORARE`

## Modello Risultato Previsto

```json
{
  "id": "string",
  "external_id": "string",
  "title": "string",
  "description": "string|null",
  "price": 0,
  "currency": "EUR",
  "platform": "string",
  "location": "string|null",
  "url": "string",
  "image_url": "string|null",
  "seller_name": "string|null",
  "seller_rating": 0,
  "condition": "string|null",
  "published_at": "datetime|null",
  "collected_at": "datetime",
  "relevance_score": 0
}
```

## Requisiti

* [x] Modello Pydantic definito
* [x] Validazione URL
* [x] Validazione valuta
* [x] Validazione prezzo
* [x] Campi opzionali coerenti
* [x] Timestamp normalizzati
* [ ] Mapping per ogni provider
* [x] Test dei dati validi
* [x] Test dei dati incompleti
* [x] Test dei dati non validi

#### Evidenze

```text
Il modello `SearchResult` e stato introdotto in `backend/app/providers/models.py` come contratto condiviso iniziale dei provider.
Sono presenti validazioni su URL, valuta, prezzo, campi testuali, identificativi e `relevance_score`, piu normalizzazione dei timestamp `published_at` e `collected_at` verso UTC.
I test coprono dati validi, incompleti e non validi. Resta aperto il mapping specifico per provider concreti.
```

---

# 10. Aggregation Engine

**Stato:** `IN SVILUPPO`

## Requisiti

* [x] Eseguire provider in parallelo
* [x] Utilizzare `asyncio.gather`
* [x] Isolare i fallimenti
* [x] Raccogliere risposte parziali
* [x] Eliminare duplicati
* [x] Normalizzare risultati
* [x] Applicare ranking
* [x] Applicare filtri
* [x] Applicare ordinamento
* [ ] Generare metriche
* [x] Aggiungere test di concorrenza
* [x] Aggiungere test di errore parziale

## Comportamento Atteso

```text
Il fallimento di un provider non deve causare il fallimento degli altri provider.
```

#### Evidenze

```text
File creati: `backend/app/services/aggregation.py`, `backend/app/services/ranking.py`, `backend/tests/test_aggregation.py`
File modificati: `backend/app/services/__init__.py`, `backend/app/main.py`, `backend/tests/test_app.py`, `backend/tests/test_providers.py`, `backend/README.md`
Componenti introdotti: `AggregationRequest`, `AggregationResponse`, `AggregationProviderFailure`, `AggregationService`, `RegistryAggregationService`, `AggregationProviderSelectionError`, `RankingService` e `HeuristicRankingService`
Verifiche riuscite: normalizzazione e deduplicazione dei platform target, selezione dei provider registrati, esecuzione parallela via `asyncio.gather`, isolamento dei fallimenti, raccolta di risultati parziali, deduplicazione della risposta aggregata per `(platform, external_id)`, primo merge conservativo dei campi piu informativi, ranking iniziale basato su query, freschezza, completezza e prezzo, primi filtri prezzo tramite `min_price` e `max_price` e ordinamento finale deterministico per rilevanza, freschezza, raccolta, prezzo e chiavi stabili
Limite aperto: il contratto di aggregazione non genera ancora metriche della risposta.
```

---

# 11. Ranking Engine

**Stato:** `IN SVILUPPO`

## Criteri Previsti

* [x] Corrispondenza con la query
* [x] Corrispondenza esatta nel titolo
* [x] Freschezza dell'annuncio
* [x] Completezza dei dati
* [x] Prezzo
* [ ] Affidabilità del venditore, quando disponibile
* [ ] Penalizzazione dei risultati non pertinenti
* [x] Ordinamento deterministico

## Test Previsti

* [x] Titolo esatto prima di titolo parziale
* [ ] Risultato recente prima di risultato vecchio, a parità di rilevanza
* [x] Risultato incompleto penalizzato
* [x] Ordinamento stabile
* [x] Nessun punteggio fuori intervallo

#### Evidenze

```text
Il ranking iniziale e implementato in `backend/app/services/ranking.py` tramite `RankingService` e `HeuristicRankingService`.
Lo score finale arricchisce `SearchResult.relevance_score` e viene poi usato dall'Aggregation Engine per un ordinamento finale deterministico basato su rilevanza, freschezza, raccolta, prezzo e chiavi stabili.
I test coprono punteggi nel range [0, 1], titolo esatto sopra titolo parziale, risultato recente e completo sopra risultato vecchio e incompleto, preservazione di un punteggio provider gia piu alto e ordinamento stabile del risultato finale.
```

---

# 12. Cache Redis

**Stato:** `NON INIZIATO`

## Requisiti

* [ ] Configurare Redis
* [ ] Definire cache service
* [ ] Normalizzare chiavi
* [ ] Includere query e filtri nella chiave
* [ ] Impostare TTL
* [ ] Gestire cache hit
* [ ] Gestire cache miss
* [ ] Gestire Redis non disponibile
* [ ] Evitare blocco dell'intera ricerca
* [ ] Serializzare modelli normalizzati
* [ ] Aggiungere metriche cache
* [ ] Aggiungere test

## Configurazione Iniziale

```text
TTL previsto: 300 secondi
```

---

# 13. PostgreSQL e Alembic

**Stato:** `NON INIZIATO`

## Requisiti

* [ ] Configurare PostgreSQL 16
* [ ] Configurare SQLAlchemy 2.x
* [ ] Configurare sessioni asincrone
* [ ] Configurare Alembic
* [ ] Definire prima migrazione
* [ ] Configurare healthcheck
* [ ] Gestire connessioni
* [ ] Aggiungere test di integrazione

## Modelli Futuri

I seguenti modelli devono essere implementati soltanto quando richiesti:

* utenti;
* preferiti;
* cronologia;
* alert;
* notifiche;
* statistiche.

Non devono essere create tabelle inutilizzate anticipatamente.

---

# 14. Worker e Queue

**Stato:** `NON INIZIATO`

## Tecnologia da Selezionare

```text
ARQ oppure Celery
```

## Requisiti

* [ ] Selezionare tecnologia
* [ ] Documentare la decisione
* [ ] Configurare worker
* [ ] Collegare Redis
* [ ] Implementare retry
* [ ] Implementare timeout
* [ ] Implementare task idempotenti
* [ ] Gestire errori
* [ ] Implementare healthcheck
* [ ] Aggiungere test
* [ ] Documentare comandi di avvio

---

# 15. API FastAPI

**Stato:** `NON INIZIATO`

## Endpoint Health

```text
GET /health
```

* [ ] Endpoint creato
* [ ] Response model creato
* [ ] Stato backend verificato
* [ ] Stato Redis verificato
* [ ] Stato database verificato
* [ ] Test presente

## Endpoint Search

```text
GET /search
```

* [ ] Endpoint creato
* [ ] Query validata
* [ ] Lunghezza minima definita
* [ ] Lunghezza massima definita
* [ ] Filtri validati
* [ ] Ordinamento validato
* [ ] Response model definito
* [ ] Error response definita
* [ ] Rate limiting configurato
* [ ] Documentazione OpenAPI aggiornata
* [ ] Test presente

## Streaming

```text
GET /search/stream
```

* [ ] Tecnologia scelta tra SSE e WebSocket
* [ ] Contratto dei messaggi definito
* [ ] Risultati progressivi supportati
* [ ] Errori parziali supportati
* [ ] Chiusura connessione gestita
* [ ] Test presente

---

# 16. Frontend Vue

**Stato:** `NON INIZIATO`

## Setup

* [ ] Vue 3
* [ ] Vite
* [ ] JavaScript moderno
* [ ] `<script setup>`
* [ ] Tailwind CSS
* [ ] Dark mode
* [ ] Pinia
* [ ] TanStack Vue Query
* [ ] Configurazione API base URL
* [ ] Variabili d'ambiente documentate

## Componenti

* [ ] `SearchBar.vue`
* [ ] `SearchFilters.vue`
* [ ] `PlatformFilter.vue`
* [ ] `PriceFilter.vue`
* [ ] `SortSelector.vue`
* [ ] `ProductCard.vue`
* [ ] `ProductGrid.vue`
* [ ] `SearchStatus.vue`
* [ ] `LoadingState.vue`
* [ ] `ErrorState.vue`
* [ ] `EmptyState.vue`

## Stati da Gestire

* [ ] Stato iniziale
* [ ] Caricamento
* [ ] Risultati parziali
* [ ] Risultati completi
* [ ] Nessun risultato
* [ ] Errore parziale
* [ ] Errore completo
* [ ] Provider non disponibile
* [ ] Connessione interrotta

---

# 17. State Management

## Pinia

**Stato:** `NON INIZIATO`

* [ ] Store filtri
* [ ] Store preferenze UI
* [ ] Store ordinamento
* [ ] Store piattaforme attive
* [ ] Persistenza opzionale delle preferenze
* [ ] Nessuna duplicazione della cache HTTP

## TanStack Query

**Stato:** `NON INIZIATO`

* [ ] Query di ricerca
* [ ] Gestione cache
* [ ] Gestione loading
* [ ] Gestione errori
* [ ] Retry configurato
* [ ] Refetch configurato
* [ ] Invalidazione cache
* [ ] Test dei composable

---

# 18. Testing

**Stato:** `NON INIZIATO`

## Backend

* [ ] `pytest`
* [ ] `pytest-asyncio`
* [ ] Test unitari
* [ ] Test di integrazione
* [ ] Mock HTTP
* [ ] Fixture provider
* [ ] Test cache
* [ ] Test database
* [ ] Test API
* [ ] Test worker
* [ ] Test errori
* [ ] Coverage configurata

## Frontend

* [ ] Framework test selezionato
* [ ] Test componenti
* [ ] Test Pinia
* [ ] Test composable
* [ ] Mock API
* [ ] Test loading
* [ ] Test error
* [ ] Test empty state
* [ ] Test filtri
* [ ] Test ordinamento

## End-to-End

* [ ] Strumento E2E selezionato
* [ ] Ambiente di test definito
* [ ] Ricerca simulata
* [ ] Filtri verificati
* [ ] Errori verificati
* [ ] Mobile layout verificato

---

# 19. Monitoring e Osservabilità

**Stato:** `NON INIZIATO`

## Prometheus

* [ ] Servizio configurato
* [ ] Endpoint metriche configurato
* [ ] Request count
* [ ] Response time
* [ ] Error rate
* [ ] Provider failures
* [ ] Provider latency
* [ ] Cache hit rate
* [ ] Queue size
* [ ] Worker failures

## Grafana

* [ ] Servizio configurato
* [ ] Datasource Prometheus
* [ ] Dashboard backend
* [ ] Dashboard provider
* [ ] Dashboard cache
* [ ] Dashboard worker
* [ ] Persistenza configurata

## Logging

* [ ] Logging strutturato
* [ ] Request ID
* [ ] Provider name
* [ ] Durata richiesta
* [ ] Tipo errore
* [ ] Nessun segreto nei log

---

# 20. Sicurezza

**Stato:** `NON INIZIATO`

* [ ] Input validation
* [ ] Query length limit
* [ ] Rate limiting
* [ ] Timeout
* [ ] Secret management
* [ ] `.env.example`
* [ ] `.env` ignorato
* [ ] Nessuna credenziale hardcoded
* [ ] Nessun token nei log
* [ ] Validazione URL esterni
* [ ] Validazione immagini remote
* [ ] Controllo CORS
* [ ] Dipendenze bloccate
* [ ] Container non-root dove possibile
* [ ] Porte ridotte al minimo
* [ ] Errori interni non esposti
* [ ] Verifica termini di servizio dei provider
* [ ] Verifica modalità di raccolta dati

---

# 21. Requisiti Non Funzionali

## Prestazioni

* [ ] Richieste concorrenti
* [ ] Cache attiva
* [ ] Timeout definiti
* [ ] Limiti di connessione
* [ ] Rendering frontend ottimizzato
* [ ] Liste lunghe gestite efficientemente
* [ ] Immagini lazy-loaded

## Affidabilità

* [ ] Errori provider isolati
* [ ] Redis non è un punto singolo di fallimento
* [ ] Database non blocca la ricerca pubblica quando non necessario
* [ ] Worker idempotenti
* [ ] Retry limitati
* [ ] Graceful shutdown
* [ ] Healthcheck funzionanti

## Manutenibilità

* [ ] File modulari
* [ ] Type hints
* [ ] Interfacce definite
* [ ] Test presenti
* [ ] Documentazione aggiornata
* [ ] Naming coerente
* [ ] Dipendenze motivate
* [ ] Nessun codice duplicato rilevante

---

# 22. Matrice Requisiti-Implementazione

Questa tabella deve collegare ogni requisito ai file reali che lo implementano.

| ID      | Requisito                       | Documento di Origine   | File Implementazione | File Test       | Stato        |
| ------- | ------------------------------- | ---------------------- | -------------------- | --------------- | ------------ |
| REQ-001 | Docker Compose completo         | OBIETTIVI_E_ROADMAP.md | `docker-compose.yml`, `.env.example`, `.dockerignore`, `docker/backend/Dockerfile`, `docker/frontend/Dockerfile`, `docker/` | Non presente    | DA VERIFICARE |
| REQ-002 | Backend Python 3.11 con Poetry  | STACK_E_TECNOLOGIE.md  | `backend/pyproject.toml`, `backend/poetry.lock`, `backend/app/main.py`, `backend/app/core/config.py`, `docker/backend/Dockerfile` | `backend/tests/test_app.py` | DA VERIFICARE |
| REQ-003 | Frontend Vue 3 con Vite         | STACK_E_TECNOLOGIE.md  | `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.js`, `frontend/src/`, `docker/frontend/Dockerfile` | Non presente    | DA VERIFICARE |
| REQ-004 | Interfaccia MarketplaceProvider | ARCHITETTURA.md        | Non presente         | Non presente    | NON INIZIATO |
| REQ-005 | Network client asincrono        | OBIETTIVI_E_ROADMAP.md | `backend/app/network/client.py`, `backend/app/network/config.py`, `backend/app/network/models.py`, `backend/app/network/exceptions.py`, `backend/app/core/config.py` | `backend/tests/test_network.py` | IN SVILUPPO  |
| REQ-006 | Proxy provider astratto         | ARCHITETTURA.md        | Non presente         | Non presente    | NON INIZIATO |
| REQ-007 | Normalizzazione risultati       | OBIETTIVI_E_ROADMAP.md | Non presente         | Non presente    | NON INIZIATO |
| REQ-008 | Aggregazione concorrente        | OBIETTIVI_E_ROADMAP.md | Non presente         | Non presente    | NON INIZIATO |
| REQ-009 | Ranking risultati               | ARCHITETTURA.md        | Non presente         | Non presente    | NON INIZIATO |
| REQ-010 | Redis cache                     | STACK_E_TECNOLOGIE.md  | Non presente         | Non presente    | NON INIZIATO |
| REQ-011 | PostgreSQL e Alembic            | STACK_E_TECNOLOGIE.md  | Non presente         | Non presente    | NON INIZIATO |
| REQ-012 | Worker asincrono                | OBIETTIVI_E_ROADMAP.md | Non presente         | Non presente    | NON INIZIATO |
| REQ-013 | Endpoint `/health`              | OBIETTIVI_E_ROADMAP.md | Non presente         | Non presente    | NON INIZIATO |
| REQ-014 | Endpoint `/search`              | OBIETTIVI_E_ROADMAP.md | Non presente         | Non presente    | NON INIZIATO |
| REQ-015 | Streaming progressivo           | ARCHITETTURA.md        | Non presente         | Non presente    | NON INIZIATO |
| REQ-016 | Pinia                           | STACK_E_TECNOLOGIE.md  | `frontend/package.json`, `frontend/src/main.js`, `frontend/src/stores/search-filters.js` | Non presente    | IN SVILUPPO  |
| REQ-017 | TanStack Query                  | STACK_E_TECNOLOGIE.md  | `frontend/package.json`, `frontend/src/main.js`, `frontend/src/utils/query-client.js` | Non presente    | IN SVILUPPO  |
| REQ-018 | Tailwind dark mode              | STACK_E_TECNOLOGIE.md  | `frontend/tailwind.config.js`, `frontend/src/style.css`, `frontend/src/components/AppShell.vue` | Non presente    | IN SVILUPPO  |
| REQ-019 | Test backend                    | RUOLI_E_STANDARD.md    | `backend/tests/test_app.py`, `backend/tests/test_network.py`, `backend/tests/conftest.py`, `backend/pyproject.toml` | `backend/tests/test_app.py`, `backend/tests/test_network.py` | IN SVILUPPO  |
| REQ-020 | Test frontend                   | RUOLI_E_STANDARD.md    | Non presente         | Non presente    | NON INIZIATO |
| REQ-021 | Prometheus                      | ARCHITETTURA.md        | `docker-compose.yml`, `docker/prometheus/prometheus.yml` | Non presente    | IN SVILUPPO  |
| REQ-022 | Grafana                         | ARCHITETTURA.md        | `docker-compose.yml`, `docker/grafana/provisioning/datasources/prometheus.yml` | Non presente    | IN SVILUPPO  |
| REQ-023 | Rate limiting                   | CODEX_WORKFLOW.md      | Non presente         | Non presente    | NON INIZIATO |
| REQ-024 | Logging strutturato             | RUOLI_E_STANDARD.md    | `backend/app/network/client.py` | `backend/tests/test_network.py` | IN SVILUPPO  |
| REQ-025 | Documentazione aggiornata       | CODEX_WORKFLOW.md      | `PROGRESS.md`, `backend/README.md`, `.env.example` | Non applicabile | IN SVILUPPO  |

Codex deve aggiungere nuove righe quando emergono nuovi requisiti approvati.

Codex non deve eliminare una riga senza documentarne il motivo nel registro delle modifiche.

---

# 23. Decisioni Architetturali

Ogni decisione tecnica rilevante deve essere registrata.

## ADR-001 - Utilizzo del Termine Provider

**Stato:** `APPROVATA`

**Decisione:**

Utilizzare il termine `Provider` invece di `Scraper`.

**Motivazione:**

Ogni marketplace può essere interrogato tramite API ufficiale, endpoint JSON, GraphQL, HTML o browser automation. Il termine Provider rappresenta meglio l'astrazione.

**Conseguenze:**

* interfaccia comune;
* implementazioni indipendenti;
* maggiore estendibilità;
* minore accoppiamento.

---

## ADR-002 - Proxy Layer Astratto

**Stato:** `APPROVATA`

**Decisione:**

Il backend non deve dipendere direttamente da Tor o da un singolo provider proxy.

**Motivazione:**

La strategia di rete può cambiare nel tempo e deve essere sostituibile senza modificare i marketplace provider.

**Conseguenze:**

* introduzione di `ProxyProvider`;
* configurazione tramite variabili d'ambiente;
* implementazioni intercambiabili;
* test semplificati.

---

## ADR-003 - Redis per Cache e Supporto Worker

**Stato:** `APPROVATA`

**Decisione:**

Utilizzare Redis per la cache delle ricerche e come supporto alla coda asincrona.

**Motivazione:**

Ridurre richieste duplicate, migliorare le prestazioni e supportare task distribuiti.

---

## ADR-004 - PostgreSQL come Database Primario

**Stato:** `APPROVATA`

**Decisione:**

Utilizzare PostgreSQL 16 con SQLAlchemy 2.x e Alembic.

**Motivazione:**

Supportare funzionalità future quali utenti, preferiti, cronologia e alert.

---

## ADR-005 - TanStack Query per Server State

**Stato:** `APPROVATA`

**Decisione:**

Le chiamate HTTP e la relativa cache nel frontend devono essere gestite da TanStack Query.

**Motivazione:**

Evitare duplicazione della logica in Pinia e standardizzare loading, errori, retry e refetch.

---

## ADR-006 - HTTP/2 opzionale con fallback esplicito

**Stato:** `APPROVATA`

**Decisione:**

Il network layer deve abilitare HTTP/2 solo quando l'ambiente supporta la dipendenza opzionale richiesta da `httpx`, con fallback esplicito a HTTP/1.1 negli altri casi.

**Motivazione:**

Mantenere il contratto del client coerente con la roadmap senza introdurre un blocco artificiale nei test o negli ambienti locali privi di `h2`.

**Conseguenze:**

* configurazione `BACKEND_NETWORK_HTTP2`;
* degradazione controllata a HTTP/1.1;
* nessun fallimento in avvio dovuto alla sola mancanza della dipendenza opzionale.

---

# 24. Deviazioni e Incongruenze

Questa sezione deve contenere qualsiasi differenza tra requisiti e implementazione.

## Formato Obbligatorio

```text
ID:
Data:
Requisito originale:
Implementazione attuale:
Motivazione:
Impatto:
Decisione richiesta:
Stato:
```

## Registro Corrente

```text
Nessuna deviazione registrata.
```

---

# 25. Problemi Aperti

| ID        | Problema                                         | Gravità | Componente | Stato  | Azione Prevista                 |
| --------- | ------------------------------------------------ | ------- | ---------- | ------ | ------------------------------- |
| ISSUE-001 | Tecnologia worker non ancora scelta              | MEDIA   | Backend    | APERTO | Confrontare ARQ e Celery        |
| ISSUE-002 | Tecnologia streaming non ancora scelta           | MEDIA   | API        | APERTO | Confrontare SSE e WebSocket     |
| ISSUE-003 | Modalità di accesso ai marketplace da verificare | ALTA    | Provider   | APERTO | Valutare API e condizioni d'uso |
| ISSUE-004 | Strategia proxy di produzione non definita       | MEDIA   | Network    | APERTO | Definire `ProxyProvider` e integrarlo nel client condiviso |
| ISSUE-005 | Daemon Docker locale non disponibile per `compose up` | MEDIA   | DevOps     | APERTO | Ripetere il test con Docker Desktop attivo |
| ISSUE-006 | `pytest` backend bloccato in fase di collection nell'ambiente locale | MEDIA   | Testing    | RISOLTO | Disabilitato `cacheprovider` e stabilizzato il path dei test con `conftest.py` |

---

# 26. Debito Tecnico

| ID      | Descrizione                             | Origine | Priorità | Stato |
| ------- | --------------------------------------- | ------- | -------- | ----- |
| Nessuno | Nessun debito tecnico ancora registrato | -       | -        | -     |

Codex deve aggiungere una voce quando introduce consapevolmente una soluzione temporanea.

Non deve nascondere soluzioni provvisorie.

---

# 27. Test Eseguiti

Ogni esecuzione di test rilevante deve essere registrata.

## Formato

```text
Data:
Comando:
Ambiente:
Risultato:
Test superati:
Test falliti:
Note:
```

## Registro Corrente

```text
Data: 2026-07-12
Comando: docker compose config
Ambiente: locale, con `DOCKER_CONFIG` temporaneo in `.docker-tmp`
Risultato: SUPERATO
Test superati: validazione sintattica di servizi, reti, volumi e variabili di default
Test falliti: Nessuno
Note: la configurazione Compose risolve correttamente anche in assenza di un file `.env` reale.

Data: 2026-07-12
Comando: docker compose up --build -d
Ambiente: locale, con `DOCKER_CONFIG` temporaneo in `.docker-tmp`
Risultato: FALLITO
Test superati: Nessuno
Test falliti: avvio completo dello stack
Note: il daemon Docker locale non risulta disponibile (`//./pipe/docker_engine` assente).

Data: 2026-07-12
Comando: poetry check
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: validazione metadata Poetry del backend
Test falliti: Nessuno
Note: dopo l'aggiornamento del `pyproject.toml` il controllo termina con `All set!`.

Data: 2026-07-12
Comando: poetry run python -c "from app.main import create_app; app = create_app(); print(app.title)"
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: import applicazione FastAPI e costruzione dell'istanza
Test falliti: Nessuno
Note: l'applicazione viene inizializzata correttamente con i settings prefissati `BACKEND_`.

Data: 2026-07-12
Comando: poetry run pytest tests/test_app.py -vv -s
Ambiente: locale, directory `backend/`
Risultato: FALLITO
Test superati: import manuale del modulo di test riuscito separatamente
Test falliti: esecuzione `pytest` del test backend
Note: il runner resta bloccato in fase di `collecting ...` anche con plugin async disabilitati.

Data: 2026-07-12
Comando: poetry run ruff check . --no-cache
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: controllo lint backend
Test falliti: Nessuno
Note: usata l'opzione `--no-cache` per evitare problemi locali sulla cache Ruff.

Data: 2026-07-12
Comando: poetry run ruff format --check . --no-cache
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: verifica formattazione backend
Test falliti: Nessuno
Note: tutti i file backend risultano già formattati.

Data: 2026-07-12
Comando: npm exec vite build -- --configLoader runner
Ambiente: locale, directory `frontend/`
Risultato: SUPERATO
Test superati: build frontend con Vite
Test falliti: Nessuno
Note: usato `--configLoader runner` e permessi estesi per superare i limiti locali di scrittura temporanea/output.

Data: 2026-07-12
Comando: docker compose config
Ambiente: locale, con `DOCKER_CONFIG` temporaneo in `.docker-tmp`
Risultato: SUPERATO
Test superati: validazione della configurazione Compose dopo l'allineamento dei Dockerfile e dei volumi frontend
Test falliti: Nessuno
Note: confermati il volume `frontend_node_modules`, i nuovi healthcheck e i percorsi dei Dockerfile applicativi.

Data: 2026-07-12
Comando: poetry run python -m pytest tests/test_app.py -q
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: esecuzione e terminazione pulita del test backend iniziale
Test falliti: Nessuno
Note: la disattivazione del `cacheprovider` in pytest evita l'hang finale del processo.

Data: 2026-07-12
Comando: poetry run pytest tests/test_app.py -q
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: esecuzione del wrapper Poetry per pytest
Test falliti: Nessuno
Note: aggiunto `backend/tests/conftest.py` per garantire la risoluzione del package `app`.

Data: 2026-07-15
Comando: poetry check
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: validazione metadata Poetry dopo l'introduzione del network layer
Test falliti: Nessuno
Note: nessuna dipendenza aggiuntiva richiesta per i contratti iniziali di rete.

Data: 2026-07-15
Comando: poetry run pytest tests/test_app.py tests/test_network.py -q
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: creazione app FastAPI, parsing dei settings di rete, validazione `NetworkRequest`, retry, mapping timeout e mapping errori HTTP del client condiviso
Test falliti: Nessuno
Note: le richieste esterne sono state simulate con `httpx.MockTransport`.

Data: 2026-07-15
Comando: poetry run ruff check . --no-cache
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: lint del backend dopo l'introduzione del package `app/network`
Test falliti: Nessuno
Note: confermata la coerenza degli import e delle convenzioni del nuovo layer di rete.

Data: 2026-07-15
Comando: poetry run ruff format --check . --no-cache
Ambiente: locale, directory `backend/`
Risultato: SUPERATO
Test superati: verifica formattazione backend dopo l'aggiunta dei test di rete
Test falliti: Nessuno
Note: la scrittura diretta della cache Ruff resta non affidabile nell'ambiente locale, ma il controllo in sola lettura termina correttamente.
```

---

# 28. Comandi Verificati

Questa sezione deve contenere soltanto comandi realmente eseguiti con successo.

| Comando                  | Stato | Data       | Note |
| ------------------------ | ----- | ---------- | ---- |
| `rg --files -g "*.md"`   | OK    | 2026-07-15 | Verificati i documenti Markdown del progetto |
| `docker compose version` | OK    | 2026-07-12 | Docker Compose disponibile nell'ambiente locale |
| `docker compose config`  | OK    | 2026-07-12 | Configurazione valida anche dopo l'allineamento dei Dockerfile |
| `poetry --version`       | OK    | 2026-07-12 | Poetry disponibile nell'ambiente locale |
| `node --version`         | OK    | 2026-07-12 | Node.js disponibile nell'ambiente locale |
| `npm --version`          | OK    | 2026-07-12 | npm disponibile nell'ambiente locale |
| `poetry lock`            | OK    | 2026-07-12 | `poetry.lock` generato e aggiornato |
| `npm install --package-lock-only --ignore-scripts` | OK | 2026-07-12 | `package-lock.json` generato |
| `poetry install --with dev --no-root` | OK | 2026-07-12 | Dipendenze backend installate da lockfile |
| `npm install --ignore-scripts` | OK | 2026-07-12 | Dipendenze frontend installate |
| `poetry check`           | OK    | 2026-07-12 | Metadata backend verificati |
| `poetry run python -c "from app.main import create_app; app = create_app(); print(app.title)"` | OK | 2026-07-12 | Inizializzazione backend verificata |
| `poetry run python -m pytest tests/test_app.py -q` | OK | 2026-07-12 | Test backend eseguito e terminato correttamente |
| `poetry run pytest tests/test_app.py -q` | OK | 2026-07-12 | Wrapper Poetry per pytest funzionante |
| `poetry run pytest tests/test_app.py tests/test_network.py -q` | OK | 2026-07-15 | Test backend e network layer condiviso superati |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo l'integrazione del proxy layer |
| `poetry run pytest tests/test_app.py tests/test_network.py -q` | OK | 2026-07-20 | Test backend e network layer con `ProxyProvider` superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo l'aggiunta del modulo proxy |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo l'integrazione proxy |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo l'introduzione del contratto `MarketplaceProvider` |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py -q` | OK | 2026-07-20 | Test backend, network layer e contratto provider superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo l'aggiunta del package `app/providers` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo il contratto provider |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo il completamento di `SearchResult` |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py -q` | OK | 2026-07-20 | Test backend, network e validazione `SearchResult` superati |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo l'introduzione dell'adapter di ricerca di `EbayProvider` |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` | OK | 2026-07-20 | Test backend, provider condivisi e `EbayProvider` con adapter e paginazione mockata superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo l'estensione di `EbayProvider` con adapter e paginazione |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo l'estensione di `EbayProvider` con adapter e paginazione |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo l'introduzione della Browse API ufficiale e dell'autenticazione OAuth di `EbayProvider` |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` | OK | 2026-07-20 | Test backend, provider condivisi e `EbayProvider` con adapter Browse API ufficiale superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo la configurazione OAuth e Browse API di `EbayProvider` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo la configurazione OAuth e Browse API di `EbayProvider` |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo il wiring runtime di `EbayProvider` nel lifespan FastAPI |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` | OK | 2026-07-20 | Test backend, lifecycle applicativo e wiring runtime di `EbayProvider` superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo la factory runtime e la registrazione in `app.state` di `EbayProvider` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo la factory runtime e la registrazione in `app.state` di `EbayProvider` |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo l'introduzione di `ProviderRegistry` |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` | OK | 2026-07-20 | Test backend, registry provider runtime e wiring lifecycle superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo l'introduzione di `ProviderRegistry` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo l'introduzione di `ProviderRegistry` |
| `poetry check`           | OK    | 2026-07-21 | Metadata backend verificati dopo il primo contratto dell'Aggregation Engine |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` | OK | 2026-07-21 | Test backend, contratto di aggregazione e registry-backed selection superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-21 | Lint backend superato dopo l'introduzione di `RegistryAggregationService` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-21 | Formattazione backend verificata dopo l'introduzione di `RegistryAggregationService` |
| `poetry check`           | OK    | 2026-07-21 | Metadata backend verificati dopo l'esecuzione parallela iniziale dell'Aggregation Engine |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` | OK | 2026-07-21 | Test backend, aggregazione parallela e raccolta di errori parziali superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-21 | Lint backend superato dopo `asyncio.gather` e `AggregationResponse` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-21 | Formattazione backend verificata dopo `asyncio.gather` e `AggregationResponse` |
| `poetry check`           | OK    | 2026-07-21 | Metadata backend verificati dopo la deduplicazione della risposta aggregata |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` | OK | 2026-07-21 | Test backend, deduplicazione per piattaforma e merge iniziale dei risultati aggregati superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-21 | Lint backend superato dopo il merge conservativo di `SearchResult` nell'Aggregation Engine |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-21 | Formattazione backend verificata dopo la normalizzazione della risposta aggregata |
| `poetry check`           | OK    | 2026-07-21 | Metadata backend verificati dopo l'introduzione di `RankingService` nell'Aggregation Engine |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` | OK | 2026-07-21 | Test backend, ranking euristico iniziale e preservazione dei punteggi provider superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-21 | Lint backend superato dopo l'aggiunta di `HeuristicRankingService` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-21 | Formattazione backend verificata dopo i test del ranking iniziale |
| `poetry check`           | OK    | 2026-07-21 | Metadata backend verificati dopo l'introduzione dei filtri prezzo nell'Aggregation Engine |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` | OK | 2026-07-21 | Test backend, filtro prezzo aggregato e validazione del range prezzi superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-21 | Lint backend superato dopo `min_price` e `max_price` in `AggregationRequest` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-21 | Formattazione backend verificata dopo i test dei filtri aggregati |
| `poetry check`           | OK    | 2026-07-21 | Metadata backend verificati dopo l'introduzione dell'ordinamento finale nell'Aggregation Engine |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` | OK | 2026-07-21 | Test backend, ordinamento finale deterministico e stabilita dei risultati aggregati superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-21 | Lint backend superato dopo l'ordinamento finale dei risultati aggregati |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-21 | Formattazione backend verificata dopo i test dell'ordinamento aggregato |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo l'estensione delle validazioni di `SearchResult` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo i nuovi test del modello |
| `poetry check`           | OK    | 2026-07-20 | Metadata backend verificati dopo l'introduzione di `EbayProvider` |
| `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` | OK | 2026-07-20 | Test backend, provider condivisi e struttura iniziale `EbayProvider` superati |
| `poetry run ruff check . --no-cache` | OK | 2026-07-20 | Lint backend superato dopo l'aggiunta del package `app/providers/ebay` |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-20 | Formattazione backend verificata dopo i test del provider eBay |
| `poetry run ruff check . --no-cache` | OK | 2026-07-12 | Lint backend superato |
| `poetry run ruff format --check . --no-cache` | OK | 2026-07-12 | Formattazione backend verificata |
| `npm exec vite build -- --configLoader runner` | OK | 2026-07-12 | Build frontend completata |

Non inserire comandi soltanto ipotizzati.

---

# 29. File Presenti e Stato

| File                     | Scopo                        | Stato    | Ultima Verifica              |
| ------------------------ | ---------------------------- | -------- | ---------------------------- |
| `OBIETTIVI_E_ROADMAP.md` | Definizione obiettivi e fasi | PRESENTE | Verificato il 2026-07-20 |
| `STACK_E_TECNOLOGIE.md`  | Tecnologie vincolanti        | PRESENTE | Verificato il 2026-07-20 |
| `RUOLI_E_STANDARD.md`    | Ruoli e standard tecnici     | PRESENTE | Verificato il 2026-07-20 |
| `ARCHITETTURA.md`        | Architettura del sistema     | PRESENTE | Verificato il 2026-07-20 |
| `CODEX_WORKFLOW.md`      | Metodo operativo di Codex    | PRESENTE | Verificato il 2026-07-20 |
| `PROGRESS.md`            | Stato e tracciamento         | PRESENTE | Aggiornato il 2026-07-20 |

Codex deve sostituire `Da verificare nel repository` dopo aver verificato la presenza reale dei file.

---

# 30. Registro delle Modifiche

Ogni micro-modifica deve generare una nuova voce.

## Formato Obbligatorio

```text
## YYYY-MM-DD - Titolo breve

### Obiettivo

Descrizione della micro-modifica.

### Requisiti Coinvolti

- REQ-XXX
- REQ-YYY

### File Analizzati

- file
- file

### File Creati

- file

### File Modificati

- file

### File Eliminati

- Nessuno

### Implementazione

Descrizione tecnica sintetica.

### Test Eseguiti

- comando
- risultato

### Stato Finale

COMPLETATO | DA VERIFICARE | BLOCCATO | DA MIGLIORARE

### Problemi Rilevati

Descrizione oppure `Nessuno`.

### Prossimo Passo

Una sola attività successiva.
```

---

## YYYY-MM-DD - Creazione del registro di avanzamento

### Obiettivo

Creare il documento centrale per confrontare requisiti, implementazione e stato del progetto.

### Requisiti Coinvolti

* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`

### File Creati

* `PROGRESS.md`

### File Modificati

* Nessuno

### File Eliminati

* Nessuno

### Implementazione

Definito il sistema di tracciamento composto da:

* stati standardizzati;
* checklist della roadmap;
* matrice requisiti-implementazione;
* decisioni architetturali;
* problemi aperti;
* debito tecnico;
* test eseguiti;
* registro modifiche;
* prossimo passo approvato.

### Test Eseguiti

```text
Nessun test applicativo richiesto.
```

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Il repository non è stato ancora verificato.
```

### Prossimo Passo

```text
Verificare la presenza dei documenti nel repository e inizializzare la struttura Docker.
```

---

## 2026-07-12 - Inizializzazione Docker Compose di base

### Obiettivo

Creare la struttura iniziale del repository per l'infrastruttura Docker Compose e verificare la presenza dei documenti guida.

### Requisiti Coinvolti

* REQ-001
* REQ-021
* REQ-022
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`

### File Creati

* `.env.example`
* `.gitignore`
* `docker-compose.yml`
* `backend/.gitkeep`
* `frontend/.gitkeep`
* `docker/backend/Dockerfile`
* `docker/backend/placeholder_app.py`
* `docker/frontend/Dockerfile`
* `docker/frontend/server.mjs`
* `docker/worker/Dockerfile`
* `docker/worker/worker.py`
* `docker/proxy/Dockerfile`
* `docker/proxy/proxy_placeholder.py`
* `docker/prometheus/prometheus.yml`
* `docker/grafana/provisioning/datasources/prometheus.yml`

### File Modificati

* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Inizializzata un'ossatura `docker-compose` con rete bridge, volumi persistenti, servizi placeholder per backend, frontend, worker e proxy, più configurazioni base per Redis, PostgreSQL, Prometheus e Grafana. Aggiunti default alle variabili d'ambiente per consentire la validazione del compose anche senza un file `.env` reale.

### Test Eseguiti

* `docker compose config` - superato
* `docker compose up --build -d` - fallito per daemon Docker non disponibile

### Stato Finale

```text
DA VERIFICARE
```

### Problemi Rilevati

```text
Il daemon Docker locale non è disponibile, quindi l'avvio completo dello stack non è stato verificabile.
```

### Prossimo Passo

```text
Inizializzare gli ambienti backend e frontend del repository.
```

---

## 2026-07-12 - Bootstrap ambienti backend e frontend

### Obiettivo

Inizializzare gli ambienti applicativi di backend e frontend con manifest, lockfile, struttura modulare e verifiche locali essenziali.

### Requisiti Coinvolti

* REQ-002
* REQ-003
* REQ-016
* REQ-017
* REQ-018
* REQ-019
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `docker-compose.yml`
* `.env.example`

### File Creati

* `backend/pyproject.toml`
* `backend/poetry.lock`
* `backend/README.md`
* `backend/app/__init__.py`
* `backend/app/main.py`
* `backend/app/api/__init__.py`
* `backend/app/api/router.py`
* `backend/app/core/__init__.py`
* `backend/app/core/config.py`
* `backend/app/models/__init__.py`
* `backend/app/network/__init__.py`
* `backend/app/providers/__init__.py`
* `backend/app/repositories/__init__.py`
* `backend/app/services/__init__.py`
* `backend/app/workers/__init__.py`
* `backend/tests/test_app.py`
* `frontend/package.json`
* `frontend/package-lock.json`
* `frontend/index.html`
* `frontend/vite.config.js`
* `frontend/postcss.config.js`
* `frontend/tailwind.config.js`
* `frontend/src/main.js`
* `frontend/src/App.vue`
* `frontend/src/style.css`
* `frontend/src/api/client.js`
* `frontend/src/components/AppShell.vue`
* `frontend/src/composables/useAppShell.js`
* `frontend/src/models/search-result.js`
* `frontend/src/stores/search-filters.js`
* `frontend/src/utils/query-client.js`
* `frontend/src/views/HomeView.vue`

### File Modificati

* `.env.example`
* `docker-compose.yml`
* `PROGRESS.md`

### File Eliminati

* `backend/.gitkeep`
* `frontend/.gitkeep`

### Implementazione

Configurati backend e frontend come ambienti reali di sviluppo: Poetry con stack FastAPI nel backend, Vite con Vue 3, Pinia, TanStack Query e Tailwind nel frontend. Aggiunti lockfile, struttura modulare coerente con l'architettura, configurazioni minime di qualità backend e una shell UI iniziale. Introdotto inoltre un prefisso `BACKEND_` nei settings per evitare collisioni con variabili d'ambiente globali del sistema host.

### Test Eseguiti

* `poetry lock` - superato
* `npm install --package-lock-only --ignore-scripts` - superato
* `poetry install --with dev --no-root` - superato
* `npm install --ignore-scripts` - superato
* `poetry check` - superato
* `poetry run python -c "from app.main import create_app; app = create_app(); print(app.title)"` - superato
* `poetry run pytest tests/test_app.py -vv -s` - fallito per blocco in collection
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato
* `npm exec vite build -- --configLoader runner` - superato
* `docker compose config` - superato

### Stato Finale

```text
DA VERIFICARE
```

### Problemi Rilevati

```text
Il runtime Python 3.11 non è disponibile sul sistema host locale e `pytest` resta bloccato in fase di collection nell'ambiente corrente. Inoltre i Dockerfile di backend e frontend non sono ancora allineati ai nuovi ambienti applicativi.
```

### Prossimo Passo

```text
Allineare i Dockerfile di backend e frontend agli ambienti appena inizializzati.
```

---

## 2026-07-12 - Allineamento Dockerfile applicativi

### Obiettivo

Collegare i servizi Docker di backend e frontend agli ambienti applicativi reali già presenti nel repository.

### Requisiti Coinvolti

* REQ-001
* REQ-002
* REQ-003
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `docker-compose.yml`
* `docker/backend/Dockerfile`
* `docker/frontend/Dockerfile`
* `backend/pyproject.toml`
* `frontend/package.json`

### File Creati

* `.dockerignore`

### File Modificati

* `docker/backend/Dockerfile`
* `docker/frontend/Dockerfile`
* `docker-compose.yml`
* `PROGRESS.md`

### File Eliminati

* `docker/backend/placeholder_app.py`
* `docker/frontend/server.mjs`

### Implementazione

Sostituiti i Dockerfile placeholder con configurazioni che usano davvero Poetry, Uvicorn, npm e Vite. Aggiornato `docker-compose.yml` per usare healthcheck coerenti con FastAPI e Vite e aggiunto un volume dedicato a `frontend/node_modules` per evitare conflitti con il bind mount del sorgente. Introdotto `.dockerignore` per ridurre il contesto di build ed escludere artefatti locali.

### Test Eseguiti

* `docker compose config` - superato

### Stato Finale

```text
DA VERIFICARE
```

### Problemi Rilevati

```text
L'avvio completo dello stack Docker resta non verificabile finché il daemon locale non è disponibile. Inoltre il blocco di `pytest` nel backend è ancora aperto e impedisce di chiudere con verifica piena lo step degli ambienti.
```

### Prossimo Passo

```text
Isolare il blocco di `pytest` nel backend e ripristinare l'esecuzione del test iniziale.
```

---

## 2026-07-12 - Ripristino esecuzione pytest backend

### Obiettivo

Eliminare il blocco del runner `pytest` nel backend e ripristinare un comando di test locale che termini correttamente.

### Requisiti Coinvolti

* REQ-019
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/pyproject.toml`
* `backend/tests/test_app.py`

### File Creati

* `backend/tests/conftest.py`

### File Modificati

* `backend/pyproject.toml`
* `.gitignore`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Identificata la causa del blocco nella fase finale del plugin `_pytest.cacheprovider`, che rimaneva appeso durante il salvataggio della cache di sessione. Disabilitato quindi il `cacheprovider` tramite `addopts` nel `pyproject.toml` e aggiunto un `conftest.py` minimo per garantire la risoluzione del package `app` anche quando il test è lanciato tramite `poetry run pytest`.

### Test Eseguiti

* `poetry check` - superato
* `poetry run python -m pytest tests/test_app.py -q` - superato
* `poetry run pytest tests/test_app.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato
* `docker compose config` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Nessuno
```

### Prossimo Passo

```text
Definire configurazione e contratti iniziali del network layer centrale.
```

---

## 2026-07-15 - Contratti iniziali del network layer

### Obiettivo

Definire configurazione, contratto condiviso e test iniziali del network layer backend senza introdurre ancora il `ProxyProvider` astratto.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `.env.example`
* `backend/README.md`
* `backend/pyproject.toml`
* `backend/app/core/config.py`
* `backend/app/main.py`
* `backend/app/api/router.py`
* `backend/app/network/__init__.py`
* `backend/tests/test_app.py`
* `backend/tests/conftest.py`

### File Creati

* `backend/app/network/client.py`
* `backend/app/network/config.py`
* `backend/app/network/exceptions.py`
* `backend/app/network/models.py`
* `backend/tests/test_network.py`

### File Modificati

* `.env.example`
* `backend/README.md`
* `backend/app/core/config.py`
* `backend/app/network/__init__.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotto un network layer backend con configurazione centralizzata ricavata dai `Settings`, contratto `NetworkClient`, implementazione `HttpxNetworkClient`, modelli tipizzati di richiesta, gerarchia di errori dedicata e retry controllato con backoff e jitter. Il client usa `httpx.AsyncClient`, supporta header comuni, cookie, timeout espliciti, limiti di connessione, logging con campi strutturati e fallback automatico a HTTP/1.1 quando il supporto opzionale HTTP/2 non e disponibile nell'ambiente.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Manca ancora l'astrazione `ProxyProvider`: il network layer accetta una `proxy_url` configurabile ma non seleziona ancora strategie proxy intercambiabili.
```

### Prossimo Passo

```text
Definire l'interfaccia `ProxyProvider` e integrarla nel client condiviso.
```

---

## 2026-07-20 - Integrazione di ProxyProvider nel network layer

### Obiettivo

Introdurre una strategia proxy astratta e tipizzata nel backend, integrandola nel client di rete condiviso con test e configurazione documentata.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `.env.example`
* `backend/README.md`
* `backend/pyproject.toml`
* `backend/app/core/config.py`
* `backend/app/network/__init__.py`
* `backend/app/network/client.py`
* `backend/app/network/config.py`
* `backend/tests/test_network.py`

### File Creati

* `backend/app/network/proxy.py`

### File Modificati

* `.env.example`
* `backend/README.md`
* `backend/app/core/config.py`
* `backend/app/network/__init__.py`
* `backend/app/network/client.py`
* `backend/app/network/config.py`
* `backend/tests/test_network.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotti `ProxyProvider` e i provider concreti minimi `DirectProxyProvider`, `DatacenterProxyProvider`, `ResidentialProxyProvider` e `TorProxyProvider`, con configurazione tipizzata `ProxySettings` e `ProxyStrategy`. `HttpxNetworkClient` risolve ora la strategia proxy tramite astrazione dedicata, supporta credenziali via variabili d'ambiente separate e continua a mappare gli errori di trasporto senza esporre dettagli sensibili. Aggiornati inoltre export del package, README backend, `.env.example` e test unitari del network layer.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Nessuno
```

### Prossimo Passo

```text
Definire l'interfaccia comune `MarketplaceProvider`.
```

---

## 2026-07-20 - Contratto comune MarketplaceProvider

### Obiettivo

Definire il contratto condiviso dei marketplace provider con modelli tipizzati, gerarchia di errori e test del comportamento minimo atteso.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/providers/__init__.py`
* `backend/app/models/__init__.py`
* `backend/tests/test_app.py`

### File Creati

* `backend/app/providers/base.py`
* `backend/app/providers/models.py`
* `backend/app/providers/exceptions.py`
* `backend/tests/test_providers.py`

### File Modificati

* `backend/README.md`
* `backend/app/providers/__init__.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotti il contratto astratto `MarketplaceProvider`, i modelli condivisi `SearchRequest`, `SearchResult`, `ProviderMetadata` e `ProviderStatus`, piu una gerarchia di errori provider con helper di mapping dagli errori del network layer. Il contratto espone i metodi `search`, `normalize` e `validate`, mantiene il timeout specifico a livello metadata tramite `TimeoutSettings` e resta indipendente dai provider concreti.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
I modelli normalizzati condivisi sono stati avviati dentro il contratto provider, ma la sezione dedicata ai modelli resta ancora incompleta per timestamp, test negativi e mapping specifici per provider concreti.
```

### Prossimo Passo

```text
Completare il modello normalizzato condiviso `SearchResult` e i relativi test di validazione.
```

---

## 2026-07-20 - Validazione del modello normalizzato SearchResult

### Obiettivo

Completare la validazione condivisa di `SearchResult`, normalizzando i timestamp e aggiungendo test per dati incompleti e non validi.

### Requisiti Coinvolti

* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/app/providers/models.py`
* `backend/tests/test_providers.py`
* `backend/app/providers/base.py`

### File Creati

* Nessuno

### File Modificati

* `backend/app/providers/models.py`
* `backend/tests/test_providers.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Estese le validazioni di `SearchResult` con normalizzazione degli identificativi, pulizia dei campi testuali opzionali e conversione di `published_at` e `collected_at` a timestamp timezone-aware in UTC. I test ora coprono dati validi, campi opzionali incompleti, timestamp normalizzati e payload non validi per valuta, prezzo, rilevanza e URL.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Resta ancora aperto il mapping specifico di `SearchResult` per i provider concreti.
```

### Prossimo Passo

```text
Definire il mapping normalizzato del primo provider concreto, iniziando dalla struttura di `EbayProvider`.
```

---

## 2026-07-20 - Struttura iniziale di EbayProvider

### Obiettivo

Introdurre la prima struttura concreta di `EbayProvider` con schema raw, mapper normalizzato e test, senza inventare ancora integrazioni reali verso endpoint esterni.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/app/providers/__init__.py`
* `backend/app/providers/exceptions.py`
* `backend/app/providers/models.py`
* `backend/tests/test_providers.py`
* `backend/README.md`

### File Creati

* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/schemas.py`
* `backend/app/providers/ebay/mapper.py`
* `backend/app/providers/ebay/exceptions.py`
* `backend/app/providers/ebay/provider.py`
* `backend/tests/test_ebay_provider.py`

### File Modificati

* `backend/app/providers/__init__.py`
* `backend/README.md`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotto un package `app/providers/ebay/` con schema raw tipizzato, mapper verso `SearchResult`, errori specifici e un `EbayProvider` concreto basato su executor iniettato. Questa struttura consente di testare ricerca, normalizzazione ed error handling senza dichiarare verificata una integrazione eBay reale non ancora definita.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
L'adapter reale di `EbayProvider` verso una API o sorgente ufficiale eBay non e ancora definito, quindi autenticazione, paginazione e ricerca reale restano aperte.
```

### Prossimo Passo

```text
Definire l'adapter di ricerca di `EbayProvider` verso una sorgente ufficiale o mockata stabile.
```

---

## 2026-07-20 - Adapter di ricerca e paginazione di EbayProvider

### Obiettivo

Introdurre un adapter di ricerca stabile per `EbayProvider` e chiudere il supporto verificabile a ricerca e paginazione senza dichiarare integrata una sorgente eBay ufficiale non ancora validata.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/app/providers/__init__.py`
* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/schemas.py`
* `backend/app/providers/ebay/provider.py`
* `backend/tests/test_ebay_provider.py`
* `backend/README.md`

### File Creati

* `backend/app/providers/ebay/adapter.py`

### File Modificati

* `backend/app/providers/__init__.py`
* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/schemas.py`
* `backend/app/providers/ebay/provider.py`
* `backend/tests/test_ebay_provider.py`
* `backend/README.md`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

`EbayProvider` e stato riallineato su un contratto esplicito `EbaySearchAdapter`, con un `MockEbaySearchAdapter` stabile che supporta ricerca asincrona e paginazione tramite `page` e `page_size`. Gli schemi raw ora includono i metadati di paginazione e i test coprono sia il mapping dei risultati sia il comportamento paginato dell'adapter mockato.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
La sorgente ufficiale o autorizzata per `EbayProvider` non e ancora stata selezionata, quindi restano aperte la verifica delle API disponibili e la definizione dell'autenticazione eventualmente richiesta.
```

### Prossimo Passo

```text
Valutare una sorgente ufficiale o autorizzata per `EbayProvider` e definire l'autenticazione necessaria.
```

---

## 2026-07-20 - Browse API ufficiale e autenticazione OAuth di EbayProvider

### Obiettivo

Valutare una sorgente eBay ufficiale e autorizzata, definire l'autenticazione richiesta e introdurre un adapter concreto verificabile senza dipendere da chiamate live non autorizzate.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `.env.example`
* `backend/README.md`
* `backend/app/core/config.py`
* `backend/app/network/client.py`
* `backend/app/network/models.py`
* `backend/app/providers/__init__.py`
* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/adapter.py`
* `backend/app/providers/ebay/provider.py`
* `backend/app/providers/ebay/schemas.py`
* `backend/tests/test_ebay_provider.py`

### File Creati

* `backend/app/providers/ebay/config.py`
* `backend/app/providers/ebay/auth.py`

### File Modificati

* `.env.example`
* `backend/README.md`
* `backend/app/core/config.py`
* `backend/app/providers/__init__.py`
* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/adapter.py`
* `backend/app/providers/ebay/schemas.py`
* `backend/tests/test_ebay_provider.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Valutata la `Browse API` ufficiale di eBay come sorgente coerente per la ricerca e introdotti `EbayBrowseApiSettings`, `EbayBrowseApiSearchAdapter` e il contratto `EbayAccessTokenProvider`. L'autenticazione e stata definita tramite token applicativo OAuth con client credentials, mantenendo anche un provider statico per ambienti controllati o token pre-generati; i test verificano richiesta token, caching locale, header obbligatori, marketplace header e mapping della risposta ufficiale verso gli schemi normalizzati interni.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
La Browse API e l'autenticazione OAuth sono state definite e testate localmente con mock, ma l'integrazione non e ancora verificata contro eBay live per assenza di credenziali e approvazione runtime nel repository.
```

### Prossimo Passo

```text
Integrare la costruzione di `EbayProvider` reale dai settings centralizzati e dal `NetworkClient` condiviso.
```

---

## 2026-07-20 - Wiring runtime di EbayProvider con NetworkClient condiviso

### Obiettivo

Integrare la costruzione runtime di `EbayProvider` dai settings centralizzati e collegarla al `NetworkClient` condiviso del backend, senza introdurre ancora endpoint o aggregazione.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/core/config.py`
* `backend/app/main.py`
* `backend/app/network/client.py`
* `backend/app/providers/__init__.py`
* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/adapter.py`
* `backend/app/providers/ebay/provider.py`
* `backend/tests/test_app.py`
* `backend/tests/test_ebay_provider.py`

### File Creati

* `backend/app/providers/ebay/factory.py`

### File Modificati

* `backend/README.md`
* `backend/app/core/config.py`
* `backend/app/main.py`
* `backend/app/network/client.py`
* `backend/app/providers/__init__.py`
* `backend/app/providers/ebay/__init__.py`
* `backend/app/providers/ebay/adapter.py`
* `backend/app/providers/ebay/provider.py`
* `backend/tests/test_app.py`
* `backend/tests/test_ebay_provider.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotta una factory runtime per `EbayProvider` che costruisce `EbayBrowseApiSettings`, seleziona automaticamente `StaticEbayAccessTokenProvider` o `ClientCredentialsEbayAccessTokenProvider` e collega il provider a un `EbayBrowseApiSearchAdapter` basato sul `NetworkClient` condiviso. Il `lifespan` di FastAPI crea ora un solo `HttpxNetworkClient`, lo espone in `app.state`, registra `EbayProvider` quando la configurazione eBay e disponibile e ne verifica la chiusura corretta a fine ciclo applicativo.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Il wiring runtime e verificato localmente, ma la registrazione di `EbayProvider` resta condizionata alla presenza di configurazione eBay valida e manca ancora una prova live contro eBay reale.
```

### Prossimo Passo

```text
Introdurre un registry condiviso dei provider runtime da riutilizzare nel futuro Aggregation Engine.
```

---

## 2026-07-20 - Registry condiviso dei provider runtime

### Obiettivo

Introdurre un contratto riusabile per i provider runtime caricati all'avvio, sostituendo il dizionario locale nel lifecycle FastAPI con un registry esplicito.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/main.py`
* `backend/app/providers/__init__.py`
* `backend/app/providers/base.py`
* `backend/tests/test_app.py`
* `backend/tests/test_providers.py`

### File Creati

* `backend/app/providers/registry.py`

### File Modificati

* `backend/README.md`
* `backend/app/main.py`
* `backend/app/providers/__init__.py`
* `backend/tests/test_app.py`
* `backend/tests/test_providers.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotto `ProviderRegistry` come contenitore tipizzato dei provider runtime, con metodi minimi per `register`, `get`, `items`, `all`, `platforms` e supporto agli accessi indicizzati. Il `lifespan` FastAPI usa ora il registry come `app.state.providers`, mantenendo il wiring già presente di `EbayProvider` ma rendendolo riusabile dal futuro Aggregation Engine senza dipendere da un dizionario ad hoc.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Il registry runtime e verificato solo con il primo provider concreto (`EbayProvider`); l'uso concorrente con provider multipli verra verificato quando iniziera l'Aggregation Engine.
```

### Prossimo Passo

```text
Introdurre il primo contratto del futuro Aggregation Engine sopra il `ProviderRegistry`.
```

---

## 2026-07-21 - Primo contratto dell'Aggregation Engine sopra ProviderRegistry

### Obiettivo

Introdurre il primo contratto riusabile dell'Aggregation Engine sopra `ProviderRegistry`, iniziando dalla selezione e validazione dei provider target senza implementare ancora l'esecuzione parallela.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/main.py`
* `backend/app/providers/base.py`
* `backend/app/providers/registry.py`
* `backend/app/services/__init__.py`
* `backend/tests/test_app.py`
* `backend/tests/test_providers.py`

### File Creati

* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`

### File Modificati

* `backend/README.md`
* `backend/app/main.py`
* `backend/app/services/__init__.py`
* `backend/tests/test_app.py`
* `backend/tests/test_providers.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotti `AggregationRequest`, `AggregationService`, `RegistryAggregationService` e `AggregationProviderSelectionError` come primo contratto dell'Aggregation Engine sopra `ProviderRegistry`. Il servizio normalizza i platform target, seleziona i provider registrati in ordine dichiarato, rifiuta platform sconosciute e viene esposto nel lifecycle FastAPI tramite `app.state.aggregation_service`, pronto per essere esteso con esecuzione parallela e raccolta dei risultati.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Il contratto di aggregazione e verificato solo per la selezione dei provider target; l'esecuzione concorrente e la raccolta di errori parziali restano ancora da implementare.
```

### Prossimo Passo

```text
Implementare l'esecuzione parallela dei provider tramite `asyncio.gather` mantenendo isolamento dei fallimenti.
```

---

## 2026-07-21 - Esecuzione parallela iniziale dell'Aggregation Engine

### Obiettivo

Implementare l'esecuzione parallela dei provider selezionati tramite `asyncio.gather`, mantenendo isolamento dei fallimenti e raccolta di risultati parziali senza introdurre ancora deduplicazione o ranking.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/main.py`
* `backend/app/services/aggregation.py`
* `backend/app/services/__init__.py`
* `backend/tests/test_app.py`
* `backend/tests/test_aggregation.py`

### File Creati

* Nessuno

### File Modificati

* `backend/README.md`
* `backend/app/services/aggregation.py`
* `backend/app/services/__init__.py`
* `backend/tests/test_aggregation.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

`RegistryAggregationService` esegue ora le ricerche dei provider selezionati in parallelo tramite `asyncio.gather(return_exceptions=True)`, serializza i fallimenti in `AggregationProviderFailure` e restituisce una `AggregationResponse` con risultati e errori parziali. I test verificano sia l'effettiva concorrenza osservabile sia il fatto che il fallimento di un provider non blocchi gli altri.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
L'Aggregation Engine raccoglie gia risultati parziali, ma non esegue ancora deduplicazione, merge, ranking, filtri o ordinamento della risposta aggregata.
```

### Prossimo Passo

```text
Normalizzare la risposta aggregata introducendo deduplicazione e primo merge dei risultati.
```

---

## 2026-07-21 - Deduplicazione e primo merge della risposta aggregata

### Obiettivo

Normalizzare la risposta dell'Aggregation Engine eliminando i duplicati sicuri e introducendo un primo merge conservativo dei campi dei risultati aggregati.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/providers/models.py`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`

### File Creati

* Nessuno

### File Modificati

* `backend/README.md`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

`RegistryAggregationService` normalizza ora i risultati finali deduplicandoli per coppia `(platform, external_id)` e applica un primo merge conservativo dei campi complementari. Il merge mantiene l'ordine di prima occorrenza, arricchisce testi e metadati opzionali quando disponibili, conserva il `collected_at` piu recente, il `published_at` piu antico e il `relevance_score` massimo, senza introdurre ancora ranking, filtri o ordinamento.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
La normalizzazione aggregata e ora presente, ma manca ancora un ranking esplicito dei risultati e non sono ancora gestiti filtri, ordinamento e metriche.
```

### Prossimo Passo

```text
Applicare un ranking iniziale ai risultati aggregati normalizzati.
```

---

## 2026-07-21 - Ranking iniziale dei risultati aggregati

### Obiettivo

Introdurre un ranking iniziale dei risultati aggregati normalizzati, mantenendo separato il calcolo del punteggio dall'ordinamento finale della risposta.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/services/__init__.py`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`

### File Creati

* `backend/app/services/ranking.py`

### File Modificati

* `backend/README.md`
* `backend/app/services/__init__.py`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

Introdotti `RankingService` e `HeuristicRankingService` come contratto e implementazione iniziale del ranking. `RegistryAggregationService` applica ora il ranking dopo la normalizzazione dei risultati, aggiornando `SearchResult.relevance_score` con uno score euristico basato su match della query, freschezza dell'annuncio, completezza minima del dato e prezzo relativo nel set aggregato, senza riordinare ancora la risposta finale.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
Il ranking iniziale e presente, ma mancano ancora i filtri applicativi, l'ordinamento finale della risposta e le metriche dell'Aggregation Engine.
```

### Prossimo Passo

```text
Applicare i primi filtri ai risultati aggregati normalizzati.
```

---

## 2026-07-21 - Filtri iniziali dei risultati aggregati

### Obiettivo

Introdurre i primi filtri applicativi nell'Aggregation Engine sopra risultati gia normalizzati, mantenendo il perimetro minimo sui filtri prezzo.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/providers/models.py`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`

### File Creati

* Nessuno

### File Modificati

* `backend/README.md`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

`AggregationRequest` supporta ora `min_price` e `max_price` con validazione del range. `RegistryAggregationService` applica i primi filtri prezzo dopo la normalizzazione dei risultati aggregati e prima del ranking, cosi i punteggi vengono calcolati solo sul sottoinsieme effettivamente restituito all'utente. Il filtro piattaforma continua a essere gestito a monte tramite selezione dei provider target.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
I primi filtri prezzo sono presenti, ma mancano ancora l'ordinamento finale della risposta aggregata e le metriche dell'Aggregation Engine.
```

### Prossimo Passo

```text
Applicare il primo ordinamento finale dei risultati aggregati.
```

---

## 2026-07-21 - Ordinamento finale iniziale dei risultati aggregati

### Obiettivo

Introdurre un ordinamento finale deterministico dei risultati aggregati, mantenendo separato l'ordinamento dal ranking e dai futuri criteri configurabili.

### Requisiti Coinvolti

* REQ-005
* REQ-019
* REQ-024
* REQ-025

### File Analizzati

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`
* `PROGRESS.md`
* `backend/README.md`
* `backend/app/services/aggregation.py`
* `backend/app/services/ranking.py`
* `backend/tests/test_aggregation.py`

### File Creati

* Nessuno

### File Modificati

* `backend/README.md`
* `backend/app/services/aggregation.py`
* `backend/tests/test_aggregation.py`
* `PROGRESS.md`

### File Eliminati

* Nessuno

### Implementazione

`RegistryAggregationService` applica ora un ordinamento finale deterministico dopo ranking e filtri. L'ordinamento privilegia `relevance_score`, presenza e freschezza di `published_at`, `collected_at`, prezzo e chiavi stabili (`platform`, `external_id`), cosi la risposta aggregata resta prevedibile anche a parita di punteggio.

### Test Eseguiti

* `poetry check` - superato
* `poetry run pytest tests/test_app.py tests/test_network.py tests/test_providers.py tests/test_ebay_provider.py tests/test_aggregation.py -q` - superato
* `poetry run ruff check . --no-cache` - superato
* `poetry run ruff format --check . --no-cache` - superato

### Stato Finale

```text
COMPLETATO
```

### Problemi Rilevati

```text
L'ordinamento finale deterministico e presente, ma mancano ancora le metriche dell'Aggregation Engine e future modalita di ordinamento configurabili per l'utente.
```

### Prossimo Passo

```text
Generare le prime metriche dell'Aggregation Engine.
```

---

# 31. Confronto Finale con i Requisiti

Prima di dichiarare completata una macro area, Codex deve compilare questa sezione.

## Funzionalità Valutata

```text
Nome della funzionalità
```

## Requisiti Previsti

* [ ] Requisito 1
* [ ] Requisito 2
* [ ] Requisito 3

## Implementazione Presente

```text
Descrizione dei file e dei comportamenti realmente presenti.
```

## Differenze

```text
Nessuna differenza oppure descrizione precisa.
```

## Test di Conformità

```text
Comandi e risultati.
```

## Esito

```text
CONFORME
PARZIALMENTE CONFORME
NON CONFORME
NON VERIFICABILE
```

## Azioni Correttive

```text
Nessuna oppure attività necessarie.
```

---

# 32. Definition of Done della Macro Area

Una macro area può essere segnata come `COMPLETATO` soltanto quando:

* tutti i requisiti obbligatori sono implementati;
* i file previsti sono presenti;
* i test pertinenti esistono;
* i test passano;
* linting e formattazione passano;
* le configurazioni sono documentate;
* non sono presenti blocchi critici;
* le deviazioni sono state approvate;
* la matrice requisiti-implementazione è aggiornata;
* il registro modifiche è aggiornato;
* la documentazione riflette il codice reale.

---

# 33. Istruzione Operativa per Codex

Codex deve applicare la seguente procedura al termine di ogni micro-modifica:

```text
1. Leggere lo stato corrente in PROGRESS.md.
2. Individuare il requisito coinvolto.
3. Eseguire la micro-modifica.
4. Eseguire i test pertinenti.
5. Aggiornare la checklist relativa.
6. Aggiornare la matrice requisiti-implementazione.
7. Aggiornare lo stato della macro area.
8. Registrare test e comandi realmente eseguiti.
9. Registrare eventuali problemi, deviazioni o debito tecnico.
10. Aggiungere una voce al registro delle modifiche.
11. Indicare un solo prossimo passo.
12. Fermarsi senza iniziare automaticamente il passo successivo.
```

---

# 34. Prompt per Aggiornare il Progresso

```text
Prima di iniziare, leggi tutti i file Markdown del progetto e controlla lo stato corrente in PROGRESS.md.

Implementa esclusivamente la micro-modifica richiesta.

Al termine:

1. confronta il risultato con i requisiti presenti nei documenti;
2. aggiorna lo stato della voce coinvolta in PROGRESS.md;
3. aggiorna la matrice requisiti-implementazione;
4. registra i file analizzati, creati, modificati o eliminati;
5. registra soltanto i test e i comandi realmente eseguiti;
6. segnala eventuali deviazioni, problemi o debito tecnico;
7. aggiorna la percentuale della macro area soltanto se giustificata;
8. aggiungi una voce al registro delle modifiche;
9. indica un solo prossimo passo coerente con la roadmap;
10. non dichiarare completata una funzionalità non verificata;
11. non iniziare automaticamente il passo successivo.
```

---

# 35. Regola Finale

`PROGRESS.md` deve descrivere sempre lo stato reale del repository.

In caso di dubbio, Codex deve utilizzare lo stato:

```text
DA VERIFICARE
```

e non:

```text
COMPLETATO
```

Il codice rappresenta la realtà implementativa.

I documenti rappresentano i requisiti.

`PROGRESS.md` rappresenta il confronto verificato tra i due.
