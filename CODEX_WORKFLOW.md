# PATTERN OPERATIVO DI SVILUPPO PER CODEX

## Scopo del Documento

Questo documento definisce il metodo di lavoro obbligatorio che Codex deve seguire durante lo sviluppo del progetto.

Codex non deve limitarsi a generare codice funzionante, ma deve operare in modo incrementale, verificabile, modulare e coerente con l'architettura definita nei file di progetto.

Il codice deve essere sviluppato attraverso modifiche piccole, isolate e facilmente controllabili.

---

# 1. Documenti Obbligatori da Leggere

Prima di generare, modificare o eliminare qualsiasi file, Codex deve leggere e considerare almeno i seguenti documenti:

* `OBIETTIVI_E_ROADMAP.md`
* `STACK_E_TECNOLOGIE.md`
* `RUOLI_E_STANDARD.md`
* `ARCHITETTURA.md`
* `CODEX_WORKFLOW.md`

Questi file rappresentano la fonte principale delle decisioni architetturali e tecniche.

Codex non deve introdurre tecnologie, librerie, convenzioni o pattern in contrasto con tali documenti.

In caso di conflitto tra il codice esistente e la documentazione, Codex deve:

1. identificare il conflitto;
2. descriverlo chiaramente;
3. applicare la soluzione più coerente con la documentazione;
4. evitare modifiche collaterali non richieste.

---

# 2. Analisi Prima della Modifica

Prima di modificare il codice, Codex deve analizzare:

* struttura delle cartelle;
* file coinvolti;
* dipendenze utilizzate;
* moduli collegati;
* test esistenti;
* configurazioni Docker;
* variabili d'ambiente;
* possibili effetti collaterali.

Codex non deve modificare un file senza aver verificato come viene utilizzato dal resto del progetto.

Prima di iniziare una modifica deve essere in grado di rispondere internamente alle seguenti domande:

* Qual è l'obiettivo preciso?
* Quali file devono essere modificati?
* Quali file non devono essere toccati?
* Quali dipendenze vengono coinvolte?
* Esistono test relativi alla funzionalità?
* La modifica rispetta l'architettura?
* La modifica può essere suddivisa in passi più piccoli?

---

# 3. Sviluppo Incrementale

Codex deve lavorare attraverso micro-modifiche.

Una micro-modifica deve avere:

* un solo obiettivo principale;
* un numero limitato di file coinvolti;
* un comportamento chiaramente verificabile;
* nessuna rifattorizzazione non richiesta;
* nessuna modifica estetica non necessaria.

Esempi di micro-modifica corretta:

* aggiungere un modello Pydantic;
* creare un'interfaccia astratta;
* aggiungere un endpoint;
* integrare un singolo provider;
* aggiungere un test;
* configurare un singolo servizio Docker;
* aggiungere una singola variabile d'ambiente;
* correggere una specifica gestione degli errori.

Esempi di modifica troppo ampia:

* implementare backend, frontend e infrastruttura in un unico passaggio;
* riscrivere più moduli senza necessità;
* sostituire una libreria in tutto il progetto senza richiesta;
* modificare struttura, naming e comportamento contemporaneamente;
* introdurre più funzionalità indipendenti nella stessa modifica.

Se una richiesta è molto ampia, Codex deve suddividerla in fasi logiche e lavorare su una fase alla volta.

---

# 4. Ordine Obbligatorio di Implementazione

Per ogni funzionalità, Codex deve seguire questo ordine:

1. analisi dei requisiti;
2. individuazione dei file coinvolti;
3. definizione dei modelli dati;
4. definizione delle interfacce;
5. implementazione minima;
6. gestione degli errori;
7. test;
8. verifica della compatibilità;
9. aggiornamento della documentazione;
10. riepilogo delle modifiche.

Codex non deve iniziare dall'interfaccia grafica se il contratto API non è stato ancora definito.

Codex non deve implementare un provider prima che siano disponibili:

* interfaccia comune;
* modelli normalizzati;
* client di rete;
* gestione errori;
* configurazione proxy.

---

# 5. Regola della Modifica Minima

Codex deve applicare esclusivamente le modifiche necessarie a completare l'obiettivo corrente.

Non deve:

* rinominare file non coinvolti;
* cambiare stile del codice esistente senza necessità;
* modificare formattazione globale;
* aggiornare librerie non coinvolte;
* cambiare naming già valido;
* spostare cartelle senza motivo;
* riscrivere componenti funzionanti;
* introdurre astrazioni premature.

Ogni modifica deve ridurre al minimo il rischio di regressioni.

---

# 6. Divieto di Codice Monolitico

Codex non deve creare file eccessivamente grandi o con responsabilità multiple.

Ogni file deve avere uno scopo chiaro.

Esempio backend:

```text
backend/app/
├── api/
├── core/
├── models/
├── providers/
├── network/
├── services/
├── repositories/
├── workers/
└── tests/
```

Esempio frontend:

```text
frontend/src/
├── api/
├── components/
├── composables/
├── stores/
├── views/
├── models/
├── utils/
└── assets/
```

La logica di business non deve essere inserita direttamente:

* nei router FastAPI;
* nei componenti Vue;
* nei file di configurazione;
* negli script di avvio.

---

# 7. Contratti Prima delle Implementazioni

Prima di implementare un modulo concreto, Codex deve definire il relativo contratto.

Esempi:

* `MarketplaceProvider`;
* `ProxyProvider`;
* `SearchResult`;
* `SearchRequest`;
* `SearchResponse`;
* `ProviderError`;
* `NetworkClient`;
* `RankingService`.

Le implementazioni concrete devono dipendere da interfacce stabili.

Esempio:

```python
from abc import ABC, abstractmethod

class MarketplaceProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> list["SearchResult"]:
        raise NotImplementedError
```

Codex deve evitare dipendenze dirette tra componenti concreti quando è possibile usare un'interfaccia.

---

# 8. Backend: Regole Operative

Il backend deve rispettare le seguenti regole:

* usare Python 3.11;
* usare Poetry;
* usare type hints;
* usare `async` e `await` per operazioni di rete;
* usare Pydantic per input e output;
* usare SQLAlchemy 2.x per il database;
* usare Alembic per le migrazioni;
* usare Redis per cache e code;
* usare `httpx.AsyncClient`;
* usare timeout espliciti;
* usare logging strutturato;
* gestire eccezioni specifiche;
* non usare eccezioni generiche senza necessità;
* non bloccare l'event loop;
* non inserire logica applicativa nei router.

I router FastAPI devono:

* validare gli input;
* chiamare i servizi;
* restituire risposte tipizzate;
* non contenere logica di scraping;
* non accedere direttamente al database;
* non gestire direttamente il proxy.

---

# 9. Provider Marketplace

Ogni marketplace deve essere implementato in un modulo indipendente.

Struttura consigliata:

```text
providers/
├── base.py
├── ebay/
│   ├── provider.py
│   ├── schemas.py
│   ├── mapper.py
│   └── exceptions.py
├── subito/
├── wallapop/
└── vinted/
```

Ogni provider deve:

* implementare l'interfaccia comune;
* restituire dati normalizzati;
* isolare i modelli specifici della piattaforma;
* gestire timeout;
* gestire errori HTTP;
* gestire risposte incomplete;
* non propagare errori non controllati;
* non bloccare gli altri provider;
* non conoscere il frontend;
* non conoscere i router FastAPI.

Il fallimento di un provider non deve causare il fallimento dell'intera ricerca.

---

# 10. Network Layer

Tutte le richieste verso servizi esterni devono passare attraverso il network layer centralizzato.

I provider non devono creare autonomamente client HTTP non configurati.

Il network layer deve gestire:

* timeout;
* proxy;
* retry;
* jitter;
* header;
* cookie;
* limiti di connessione;
* logging;
* codici di errore;
* chiusura corretta dei client.

Le configurazioni di rete non devono essere hardcoded.

Devono essere lette da:

* variabili d'ambiente;
* file di configurazione;
* modelli Pydantic Settings.

Le strategie di proxy devono essere intercambiabili.

---

# 11. Cache Redis

Prima di interrogare i provider, Codex deve verificare se esiste un risultato valido in cache.

La chiave di cache deve essere deterministica e normalizzata.

Esempio concettuale:

```text
search:{query_normalizzata}:{filtri}:{ordinamento}
```

Codex deve:

* normalizzare la query;
* impostare un TTL;
* evitare cache infinite;
* gestire Redis non disponibile;
* non bloccare la ricerca in caso di errore cache;
* serializzare dati attraverso modelli definiti.

La cache deve migliorare il sistema, non diventare un punto singolo di fallimento.

---

# 12. Database e Migrazioni

Ogni modifica allo schema del database deve essere accompagnata da una migrazione Alembic.

Codex non deve modificare manualmente il database in modo non riproducibile.

Per ogni nuovo modello deve verificare:

* chiave primaria;
* indici;
* vincoli;
* relazioni;
* tipi corretti;
* campi nullable;
* valori di default;
* timestamp.

Codex non deve creare tabelle inutilizzate solo per possibili funzionalità future.

Le funzionalità future devono essere previste architetturalmente, ma implementate solo quando richieste.

---

# 13. Frontend: Regole Operative

Il frontend deve rispettare:

* Vue 3;
* Vite;
* Composition API;
* `<script setup>`;
* Pinia;
* TanStack Vue Query;
* Tailwind CSS;
* componenti piccoli;
* separazione tra stato remoto e stato locale.

TanStack Query deve gestire:

* richieste API;
* cache server-side nel browser;
* stato di caricamento;
* stato di errore;
* retry;
* refetch.

Pinia deve gestire:

* filtri;
* preferenze UI;
* stato condiviso del client;
* ordinamento;
* selezione delle piattaforme.

Pinia non deve duplicare la cache delle chiamate HTTP gestita da TanStack Query.

---

# 14. Componenti Vue

Ogni componente deve avere una sola responsabilità principale.

Esempio:

```text
components/
├── SearchBar.vue
├── SearchFilters.vue
├── PlatformFilter.vue
├── PriceFilter.vue
├── ProductCard.vue
├── ProductGrid.vue
├── SearchStatus.vue
└── EmptyState.vue
```

I componenti presentazionali devono ricevere dati attraverso props ed emettere eventi.

La logica di accesso alle API deve essere inserita in:

* composable;
* servizi API;
* query dedicate.

Non deve essere duplicata tra componenti.

---

# 15. Gestione degli Errori

Codex deve prevedere gli errori prima di considerare completa una funzionalità.

Devono essere gestiti almeno:

* timeout;
* connessione rifiutata;
* proxy non disponibile;
* provider non disponibile;
* risposta non valida;
* dati mancanti;
* errore di parsing;
* errore Redis;
* errore PostgreSQL;
* errore del worker;
* input utente non valido;
* risposta parziale.

Gli errori interni non devono esporre:

* stack trace;
* credenziali;
* token;
* URL privati;
* configurazioni sensibili.

Le risposte API devono essere coerenti e tipizzate.

---

# 16. Logging

Codex deve utilizzare logging strutturato e non utilizzare `print` nel codice applicativo.

Ogni log deve includere, quando disponibile:

* request ID;
* provider;
* query;
* durata;
* stato;
* tipo di errore.

Non devono essere registrati:

* password;
* cookie sensibili;
* token;
* credenziali proxy;
* dati personali non necessari.

Livelli di log:

* `DEBUG`: dettagli di sviluppo;
* `INFO`: flussi applicativi principali;
* `WARNING`: errori recuperabili;
* `ERROR`: errori che impediscono una parte del flusso;
* `CRITICAL`: errori infrastrutturali gravi.

---

# 17. Testing Obbligatorio

Ogni modifica funzionale deve includere test adeguati.

Backend:

* `pytest`;
* `pytest-asyncio`;
* test unitari;
* test di integrazione;
* mock delle richieste esterne;
* test degli errori;
* test dei modelli Pydantic.

Frontend:

* test dei componenti;
* test degli store;
* test dei composable;
* test delle chiamate API mockate;
* test degli stati loading, error e vuoto.

Codex deve evitare test che dipendono direttamente da marketplace reali.

Le richieste esterne devono essere simulate nei test.

---

# 18. Test Prima del Completamento

Prima di considerare conclusa una modifica, Codex deve:

1. eseguire i test coinvolti;
2. verificare il type checking;
3. verificare il linting;
4. verificare la formattazione;
5. verificare l'avvio del modulo;
6. verificare che Docker Compose resti valido;
7. verificare che le variabili d'ambiente siano documentate;
8. verificare che non siano presenti segreti nel codice.

Una modifica non è completa se il codice è stato scritto ma non verificato.

---

# 19. Dipendenze

Codex non deve aggiungere una dipendenza senza una motivazione tecnica concreta.

Prima di aggiungere una libreria deve verificare:

* se il problema può essere risolto con dipendenze già presenti;
* se la libreria è mantenuta;
* se è compatibile con lo stack;
* se introduce dipendenze pesanti;
* se ha impatto sulla sicurezza;
* se richiede configurazioni aggiuntive.

Per il backend:

* modificare `pyproject.toml`;
* aggiornare il lockfile Poetry;
* non creare `requirements.txt`;
* non usare `pip install` come soluzione permanente.

Per il frontend:

* modificare `package.json`;
* aggiornare il lockfile;
* non aggiungere pacchetti ridondanti.

---

# 20. Docker

Ogni servizio Docker deve avere:

* nome chiaro;
* rete definita;
* healthcheck;
* variabili d'ambiente;
* volumi quando necessari;
* policy di restart coerente;
* dipendenze esplicite;
* immagine o build riproducibile.

Codex deve evitare:

* immagini eccessivamente grandi;
* esecuzione come root quando non necessaria;
* segreti dentro Dockerfile;
* porte esposte senza motivo;
* dipendenze implicite;
* utilizzo di `latest` in produzione.

Le immagini di produzione devono utilizzare build multi-stage quando possibile.

---

# 21. Variabili d'Ambiente

Le configurazioni devono essere separate dal codice.

Codex deve mantenere almeno:

```text
.env.example
```

Il file `.env.example` deve contenere:

* tutte le chiavi richieste;
* valori di esempio non sensibili;
* descrizioni brevi quando necessarie.

Il file `.env` reale non deve essere incluso nel repository.

Nessun segreto deve essere hardcoded.

---

# 22. Sicurezza

Codex deve applicare il principio del minimo privilegio.

Deve inoltre:

* validare tutti gli input;
* limitare la lunghezza delle query;
* applicare rate limiting;
* evitare injection;
* non fidarsi dei dati dei provider;
* sanificare URL e contenuti;
* validare le immagini remote;
* proteggere endpoint amministrativi;
* non esporre configurazioni interne;
* usare dipendenze aggiornate e compatibili.

Le pratiche di raccolta dati devono rispettare:

* termini di servizio;
* robots.txt quando applicabile;
* limiti di frequenza;
* normativa vigente;
* accesso a dati pubblicamente disponibili;
* eventuali API ufficiali disponibili.

Codex non deve implementare tecniche finalizzate ad aggirare autenticazione, CAPTCHA, paywall, controlli di accesso o protezioni che impediscano l'accesso a contenuti non autorizzati.

---

# 23. Refactoring

Codex può effettuare refactoring solo quando:

* è necessario per implementare la funzionalità;
* riduce duplicazione reale;
* migliora testabilità;
* corregge una violazione architetturale;
* non modifica il comportamento pubblico senza richiesta.

Il refactoring deve essere separato dalla nuova funzionalità quando possibile.

Non devono essere mescolati nella stessa modifica:

* nuova funzionalità;
* rinomina globale;
* ristrutturazione completa;
* aggiornamento di dipendenze;
* cambiamento di stile.

---

# 24. Aggiornamento della Documentazione

Codex deve aggiornare la documentazione quando modifica:

* comandi di avvio;
* variabili d'ambiente;
* endpoint;
* struttura delle cartelle;
* dipendenze;
* servizi Docker;
* modelli dati;
* flussi applicativi;
* architettura.

La documentazione deve riflettere lo stato reale del progetto.

Non devono esistere istruzioni non più valide.

---

# 25. Formato delle Risposte di Codex

Per ogni modifica, Codex deve produrre una risposta strutturata nel seguente modo.

## Obiettivo

Descrizione sintetica della modifica.

## File Analizzati

Elenco dei file letti prima dell'intervento.

## File Modificati

Elenco dei file modificati, creati o eliminati.

## Modifiche Applicate

Descrizione tecnica delle modifiche.

## Test Eseguiti

Comandi eseguiti e risultato.

## Problemi Rilevati

Eventuali limiti, errori o incompatibilità.

## Prossimo Passo Consigliato

Una sola attività successiva, coerente con la roadmap.

Codex non deve dichiarare che una funzionalità è completata se non ha potuto verificarla.

---

# 26. Divieto di Codice Incompleto

Codex non deve generare:

```text
TODO
```

al posto di codice richiesto.

Non deve utilizzare:

```text
implementare qui
```

oppure:

```text
resto del codice
```

oppure:

```text
...
```

per omettere parti necessarie.

I file generati devono essere completi e utilizzabili.

Un `TODO` è ammesso solo quando rappresenta esplicitamente una funzionalità futura non inclusa nell'obiettivo corrente.

---

# 27. Divieto di Modifiche Silenziose

Codex deve dichiarare ogni modifica rilevante.

Non deve:

* eliminare file senza segnalarlo;
* cambiare API pubbliche senza segnalarlo;
* modificare nomi di variabili d'ambiente senza segnalarlo;
* cambiare struttura del database senza migrazione;
* cambiare dipendenze senza motivazione;
* modificare configurazioni Docker senza descrizione.

---

# 28. Gestione dei Problemi Esterni

Se una funzionalità dipende da:

* API non documentate;
* endpoint instabili;
* credenziali mancanti;
* provider non raggiungibile;
* dati non disponibili;
* servizio esterno a pagamento;
* comportamento non verificabile;

Codex deve:

1. isolare il problema;
2. implementare il contratto e la struttura necessaria;
3. creare mock o fixture per i test;
4. documentare il limite;
5. non inventare risposte o endpoint;
6. non dichiarare il modulo funzionante senza verifica.

---

# 29. Pattern di Commit Consigliato

Ogni modifica deve essere sufficientemente piccola da poter essere rappresentata da un singolo commit coerente.

Formato consigliato:

```text
feat: aggiunge modello normalizzato dei risultati
fix: gestisce timeout del provider eBay
refactor: estrae il client HTTP condiviso
test: aggiunge test del motore di ranking
docs: aggiorna configurazione Redis
chore: configura linting backend
```

Un commit non deve includere funzionalità indipendenti.

---

# 30. Definition of Done

Una funzionalità può essere considerata completa solo se:

* rispetta i documenti del progetto;
* il codice è completo;
* il codice è modulare;
* i tipi sono definiti;
* gli errori sono gestiti;
* i test sono presenti;
* i test passano;
* il linting passa;
* la formattazione è corretta;
* la configurazione è aggiornata;
* la documentazione è aggiornata;
* non sono presenti segreti;
* non sono state introdotte regressioni note;
* Docker continua ad avviarsi;
* il comportamento è verificabile.

---

# 31. Ciclo Operativo Obbligatorio

Codex deve seguire questo ciclo per ogni attività:

```text
LEGGI
  ↓
ANALIZZA
  ↓
PIANIFICA
  ↓
MODIFICA POCO
  ↓
TESTA
  ↓
CORREGGI
  ↓
DOCUMENTA
  ↓
RIEPILOGA
```

Al termine del ciclo, Codex deve fermarsi.

Non deve iniziare automaticamente una nuova macro-funzionalità non richiesta.

---

# 32. Prompt Operativo Principale

Il seguente prompt può essere utilizzato come istruzione iniziale per Codex:

```text
Prima di modificare il progetto, leggi integralmente i file OBIETTIVI_E_ROADMAP.md, STACK_E_TECNOLOGIE.md, RUOLI_E_STANDARD.md, ARCHITETTURA.md e CODEX_WORKFLOW.md.

Analizza il codice esistente e individua esclusivamente i file necessari per completare l'obiettivo corrente.

Lavora attraverso micro-modifiche, mantenendo ogni intervento isolato, testabile e coerente con l'architettura.

Non eseguire rifattorizzazioni non richieste, non introdurre nuove dipendenze senza motivazione e non modificare file non coinvolti.

Genera sempre codice completo, tipizzato, modulare e privo di parti omesse.

Dopo ogni modifica, esegui i test pertinenti, verifica linting, formattazione e compatibilità con Docker.

Aggiorna la documentazione quando vengono modificati endpoint, dipendenze, configurazioni, variabili d'ambiente o struttura del progetto.

Al termine, indica obiettivo, file analizzati, file modificati, test eseguiti, problemi rilevati e un solo prossimo passo consigliato.
```

---

# 33. Prompt per una Singola Micro-Modifica

```text
Leggi prima tutti i file Markdown di progetto.

Implementa esclusivamente la seguente modifica:

[DESCRIZIONE DELLA MODIFICA]

Non modificare funzionalità non coinvolte.

Prima di scrivere codice:
1. individua i file necessari;
2. verifica le dipendenze;
3. verifica i test esistenti;
4. definisci il cambiamento minimo.

Dopo la modifica:
1. esegui i test pertinenti;
2. esegui linting e formattazione;
3. aggiorna la documentazione necessaria;
4. riepiloga i file modificati;
5. segnala chiaramente ciò che non è stato possibile verificare.

Non iniziare la modifica successiva.
```

---

# 34. Regola Finale

Codex deve privilegiare sempre:

```text
correttezza > velocità
semplicità > complessità
modularità > codice monolitico
testabilità > scorciatoie
chiarezza > astrazioni premature
micro-modifiche > grandi riscritture
```

Ogni decisione tecnica deve essere coerente con questi principi.
