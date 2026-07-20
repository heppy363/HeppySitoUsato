# OBIETTIVI E ROADMAP DI SVILUPPO

## Visione del Progetto

Realizzare una piattaforma web centralizzata per la ricerca di annunci usati provenienti da più marketplace.

L'utente inserisce una query testuale (es. "RTX 3090") e il sistema interroga simultaneamente più provider esterni restituendo risultati unificati, normalizzati e ordinabili tramite un'interfaccia moderna e responsive.

L'architettura deve essere progettata per essere estendibile, resiliente e facilmente manutenibile.

---

# Obiettivi Principali

## Ricerca Aggregata

Supportare inizialmente:

* Subito
* eBay
* Wallapop
* Vinted

L'architettura dovrà consentire l'aggiunta futura di nuovi provider senza modifiche sostanziali al core applicativo.

---

## Normalizzazione Dati

Tutti i risultati devono essere convertiti in un formato comune.

Ogni provider dovrà restituire:

```json
{
  "id": "",
  "title": "",
  "price": 0,
  "currency": "EUR",
  "location": "",
  "platform": "",
  "url": "",
  "image": "",
  "published_at": ""
}
```

---

## Esperienza Utente

L'utente deve poter:

* cercare prodotti
* filtrare per piattaforma
* filtrare per prezzo
* ordinare per rilevanza
* ordinare per prezzo
* ordinare per data

---

# Macro Area 1 - Infrastruttura

## Step 1

Configurazione Docker Compose.

Servizi:

* frontend
* backend
* redis
* postgres
* worker
* monitoring
* proxy layer

---

## Step 2

Configurazione volumi persistenti:

* PostgreSQL
* Redis
* sviluppo backend
* sviluppo frontend

---

# Macro Area 2 - Core Backend

## Step 3

Implementare il modulo di networking asincrono basato su:

* httpx
* HTTP/2
* gestione proxy
* retry automatici
* timeout
* rate limiting interno

---

## Step 4

Implementare il sistema Provider.

Ogni marketplace deve essere isolato in un modulo indipendente.

Non utilizzare il termine Scraper.

Utilizzare Provider.

Esempi:

* EbayProvider
* SubitoProvider
* WallapopProvider
* VintedProvider

---

## Step 5

Implementare il motore di aggregazione.

Responsabilità:

* esecuzione parallela
* raccolta risultati
* gestione errori
* normalizzazione dati
* ranking

---

## Step 6

Implementare Redis Cache.

Obiettivi:

* ridurre richieste duplicate
* ridurre carico sui provider
* migliorare velocità risposta

TTL iniziale:

5 minuti

---

## Step 7

Implementare PostgreSQL.

Funzionalità future:

* utenti
* preferiti
* cronologia
* statistiche
* notifiche

---

# Macro Area 3 - API

## Step 8

Creare API REST FastAPI.

Endpoint iniziali:

GET /health

GET /search

---

## Step 9

Integrare documentazione automatica:

* Swagger
* OpenAPI

---

## Step 10

Implementare SSE o WebSocket per aggiornamento progressivo dei risultati.

---

# Macro Area 4 - Worker e Job

## Step 11

Implementare coda asincrona.

Tecnologie consentite:

* ARQ
* Celery

---

## Step 12

Implementare task schedulati:

* aggiornamento cache
* pulizia dati
* monitoraggio provider

---

# Macro Area 5 - Frontend

## Step 13

Configurazione Vue 3.

---

## Step 14

Configurazione Pinia.

---

## Step 15

Configurazione TanStack Query.

---

## Step 16

Sviluppo componenti UI.

* Search Bar
* Filters
* Result Grid
* Product Card

---

## Step 17

Ottimizzazione Mobile First.

---

# Macro Area 6 - Qualità

## Step 18

Test Unitari.

* pytest
* pytest-asyncio

---

## Step 19

Test di integrazione.

---

## Step 20

Monitoring e osservabilità.

* Prometheus
* Grafana
