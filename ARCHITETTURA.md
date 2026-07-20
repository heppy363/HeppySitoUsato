# ARCHITETTURA DEL SISTEMA

## Panoramica

```text
Frontend
    │
    ▼
FastAPI API Gateway
    │
    ├────────────── Redis Cache
    │
    ├────────────── PostgreSQL
    │
    ├────────────── Worker Queue
    │
    ▼
Aggregation Engine
    │
    ├────────────── SubitoProvider
    ├────────────── EbayProvider
    ├────────────── WallapopProvider
    └────────────── VintedProvider
```

---

# Flusso di Ricerca

```text
Utente
   │
   ▼
Frontend
   │
   ▼
GET /search
   │
   ▼
Redis Cache Check
   │
   ├── HIT
   │      ▼
   │   Risposta
   │
   └── MISS
          ▼
Aggregation Engine
          ▼
Provider Multipli
          ▼
Normalizzazione
          ▼
Ranking
          ▼
Cache
          ▼
Risposta
```

---

# Provider Architecture

```text
MarketplaceProvider
        │
        ├── SubitoProvider
        ├── EbayProvider
        ├── WallapopProvider
        └── VintedProvider
```

Ogni provider implementa:

* search()
* normalize()
* validate()

---

# Network Layer

```text
ProxyProvider
     │
     ├── TorProvider
     ├── ResidentialProvider
     ├── DatacenterProvider
     └── DirectProvider
```

Il sistema non deve dipendere da un singolo metodo di uscita verso Internet.

---

# Ranking Engine

Punteggio basato su:

* rilevanza query
* prezzo
* freschezza annuncio
* qualità dati

---

# Monitoring

Prometheus raccoglie:

* response time
* cache hit rate
* provider failures
* request count

Grafana visualizza dashboard operative.

---

# Scalabilità

Ogni componente deve poter essere scalato indipendentemente.

Esempio:

* più worker
* più provider
* più istanze backend

senza modifiche architetturali significative.
