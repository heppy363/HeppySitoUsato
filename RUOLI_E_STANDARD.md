# RUOLI E STANDARD DI SVILUPPO

## Senior Backend Engineer

Responsabilità:

* FastAPI
* asyncio
* httpx
* SQLAlchemy
* Redis
* PostgreSQL

Regole:

* type hints obbligatori
* codice completamente asincrono dove possibile
* gestione errori centralizzata
* logging strutturato

---

## Frontend Architect

Responsabilità:

* Vue 3
* Pinia
* TanStack Query
* Tailwind

Regole:

* Composition API obbligatoria
* script setup obbligatorio
* componenti piccoli e riutilizzabili
* separazione tra UI e stato

---

## DevOps Engineer

Responsabilità:

* Docker
* Docker Compose
* Networking
* Monitoring
* CI/CD

Regole:

* container isolati
* healthcheck obbligatori
* immagini leggere
* multi-stage build

---

# Standard Generali

## Modularità

Nessun file monolitico.

Ogni responsabilità deve essere isolata.

---

## Testing

Ogni modulo critico deve essere testabile.

---

## Logging

Utilizzare logging strutturato.

Livelli:

* INFO
* WARNING
* ERROR

---

## Error Handling

Il fallimento di un provider non deve bloccare l'intera ricerca.

---

## Naming

Utilizzare Provider e non Scraper.

Esempio:

SubitoProvider

Non:

SubitoScraper
