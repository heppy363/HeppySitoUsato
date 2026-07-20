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
Proxy provider del network layer centrale
```

## Percentuale Indicativa

```text
32%
```

La percentuale è indicativa e non deve essere calcolata esclusivamente sul numero di file creati.

Deve riflettere il completamento reale delle macro aree previste nella roadmap.

## Ultimo Aggiornamento

```text
Data: 2026-07-20
Responsabile: Codex
Attivita: Integrazione di ProxyProvider e strategie proxy tipizzate nel network layer
```

## Prossimo Passo Approvato

```text
Definire l'interfaccia comune MarketplaceProvider.
```

Codex non deve iniziare automaticamente attività successive oltre il prossimo passo approvato.

---

# 5. Riepilogo Macro Aree

| Macro Area              | Stato        | Avanzamento | Note                              |
| ----------------------- | ------------ | ----------: | --------------------------------- |
| Infrastruttura e Docker | IN SVILUPPO  |         45% | Dockerfile backend/frontend allineati, avvio stack da completare |
| Configurazione Backend  | IN SVILUPPO  |         80% | Poetry, lockfile, struttura FastAPI, test backend e settings di rete con strategie proxy tipizzate |
| Network Layer           | IN SVILUPPO  |         75% | Client condiviso, configurazione proxy astratta e test mockati presenti; restano da definire i contratti marketplace |
| Marketplace Provider    | NON INIZIATO |          0% | Nessun provider implementato      |
| Aggregation Engine      | NON INIZIATO |          0% | Nessuna logica di aggregazione    |
| Cache Redis             | NON INIZIATO |          0% | Solo servizio Docker, cache applicativa assente |
| PostgreSQL e Migrazioni | NON INIZIATO |          0% | Solo servizio Docker, ORM e Alembic assenti |
| Worker e Code           | NON INIZIATO |          0% | Solo placeholder Docker, tecnologia non selezionata |
| API FastAPI             | NON INIZIATO |          0% | Nessun endpoint presente          |
| Streaming Risultati     | NON INIZIATO |          0% | SSE o WebSocket non definiti      |
| Frontend Vue            | IN SVILUPPO  |         50% | Vite, struttura Vue e immagine Docker inizializzati |
| State Management        | IN SVILUPPO  |         15% | Pinia configurato con store iniziale |
| Server State            | IN SVILUPPO  |         15% | TanStack Query configurato con query client base |
| Interfaccia Grafica     | IN SVILUPPO  |         10% | Shell UI iniziale presente, feature di ricerca assenti |
| Testing                 | IN SVILUPPO  |         30% | Test backend e network layer con MockTransport; copertura proxy ora inclusa ma ancora minima |
| Monitoring              | IN SVILUPPO  |         10% | Servizi base presenti, metriche e dashboard da implementare |
| Sicurezza               | NON INIZIATO |          0% | Controlli non implementati        |
| Documentazione          | IN SVILUPPO  |         95% | Documenti principali verificati e progresso aggiornato |

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

**Stato:** `NON INIZIATO`

#### Requisiti

* [ ] Definire `MarketplaceProvider`
* [ ] Definire metodo asincrono `search`
* [ ] Definire modelli di input
* [ ] Definire modelli di output
* [ ] Definire eccezioni comuni
* [ ] Definire stato del provider
* [ ] Definire timeout specifico
* [ ] Definire normalizzazione
* [ ] Definire mapping degli errori
* [ ] Aggiungere test del contratto

---

## eBay Provider

**Stato:** `NON INIZIATO`

* [ ] Valutare API ufficiali disponibili
* [ ] Definire autenticazione quando necessaria
* [ ] Implementare ricerca
* [ ] Normalizzare risultati
* [ ] Gestire paginazione
* [ ] Gestire errori
* [ ] Gestire risultati incompleti
* [ ] Aggiungere mock
* [ ] Aggiungere test

---

## Subito Provider

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

**Stato:** `NON INIZIATO`

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

* [ ] Modello Pydantic definito
* [ ] Validazione URL
* [ ] Validazione valuta
* [ ] Validazione prezzo
* [ ] Campi opzionali coerenti
* [ ] Timestamp normalizzati
* [ ] Mapping per ogni provider
* [ ] Test dei dati validi
* [ ] Test dei dati incompleti
* [ ] Test dei dati non validi

---

# 10. Aggregation Engine

**Stato:** `NON INIZIATO`

## Requisiti

* [ ] Eseguire provider in parallelo
* [ ] Utilizzare `asyncio.gather`
* [ ] Isolare i fallimenti
* [ ] Raccogliere risposte parziali
* [ ] Eliminare duplicati
* [ ] Normalizzare risultati
* [ ] Applicare ranking
* [ ] Applicare filtri
* [ ] Applicare ordinamento
* [ ] Generare metriche
* [ ] Aggiungere test di concorrenza
* [ ] Aggiungere test di errore parziale

## Comportamento Atteso

```text
Il fallimento di un provider non deve causare il fallimento degli altri provider.
```

---

# 11. Ranking Engine

**Stato:** `NON INIZIATO`

## Criteri Previsti

* [ ] Corrispondenza con la query
* [ ] Corrispondenza esatta nel titolo
* [ ] Freschezza dell'annuncio
* [ ] Completezza dei dati
* [ ] Prezzo
* [ ] Affidabilità del venditore, quando disponibile
* [ ] Penalizzazione dei risultati non pertinenti
* [ ] Ordinamento deterministico

## Test Previsti

* [ ] Titolo esatto prima di titolo parziale
* [ ] Risultato recente prima di risultato vecchio, a parità di rilevanza
* [ ] Risultato incompleto penalizzato
* [ ] Ordinamento stabile
* [ ] Nessun punteggio fuori intervallo

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
