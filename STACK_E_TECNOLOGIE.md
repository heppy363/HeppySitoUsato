# STACK TECNOLOGICO

## Backend

### Linguaggio

Python 3.11

### Package Manager

Poetry

### Framework

FastAPI

### ASGI Server

Uvicorn

### Data Validation

Pydantic

### ORM

SQLAlchemy 2.x

### Migration

Alembic

### HTTP Client

httpx

### Browser Automation Fallback

Playwright

### Async Jobs

ARQ oppure Celery

---

# Database

## Primario

PostgreSQL 16

## Cache

Redis

---

# Frontend

## Framework

Vue 3

## Build Tool

Vite

## State Management

Pinia

## Server State

TanStack Query

## Styling

TailwindCSS

## Component Syntax

Composition API

<script setup>

---

# Monitoring

## Metrics

Prometheus

## Dashboard

Grafana

---

# Containerizzazione

Docker

Docker Compose

---

# Networking

## Proxy Layer

Architettura astratta basata su provider.

Implementazioni supportate:

- TorProvider
- ResidentialProvider
- DatacenterProvider
- DirectProvider

Il backend non deve dipendere da una specifica soluzione proxy.

Ogni provider di rete deve implementare la stessa interfaccia comune.
