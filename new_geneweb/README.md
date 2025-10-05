# New Python-Based Architecture Overview

```mermaid
---
config:
  layout: elk
---
flowchart TD
    %% =========================================
    %% Title
    %% =========================================
    %% Geneweb modernized version architecture

    %% =========================================
    %% Frontends
    %% =========================================
      FrontGWSetup["🧱 GeneWeb Backoffice Frontend (gwsetup) - Svelte 5<br/>(IP restricted)"]:::webapp
      FrontGW["🧱 GeneWeb Frontend - Svelte 5"]:::webapp

    %% =========================================
    %% Backend
    %% =========================================
    subgraph BACK["Backend - Python 3"]
        subgraph API["REST API Layer - FastAPI"]
            REND["🔒 Restricted Endpoints<br/>(IP restricted)"]:::controller
            OEND["🌐 Open Endpoints"]:::controller
        end

        LOGIC["🧠 Domain Layer<br/>Logic & recalculation"]:::logic

        subgraph PERSISTENCE["Persistence Layer"]
            REPO["📦 Repository"]:::repo
            ORM["🧩 SQLAlchemy (ORM)"]:::orm
        end
    end

    %% =========================================
    %% External components
    %% =========================================
    DB[("🗄️ Genealogy Database - PostgreSQL<br/>Replaces .gwb database")]:::db
    PLUGINS["⚙️ Plugins"]:::plugin
    ENV["🧾 .env<br/>Configuration"]:::config

    %% =========================================
    %% Relationships
    %% =========================================
    BACK --> PLUGINS:::arrowtext
    BACK --> ENV:::arrowtext

    OEND -.-> REND
    FrontGW --> OEND:::http
    FrontGWSetup --> REND:::http

    API --> LOGIC
    LOGIC --> REPO
    API --> REPO
    REPO --> ORM
    ORM --> DB

    %% =========================================
    %% Styles
    %% =========================================
    classDef webapp fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1;
    classDef controller fill:#fff3e0,stroke:#f57c00,color:#e65100;
    classDef logic fill:#e8f5e9,stroke:#43a047,color:#1b5e20;
    classDef repo fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef orm fill:#f3e5f5,stroke:#8e24aa,color:#4a148c;
    classDef db fill:#e0f7fa,stroke:#00838f,color:#004d40;
    classDef plugin fill:#fce4ec,stroke:#c2185b,color:#880e4f;
    classDef config fill:#f9fbe7,stroke:#9e9d24,color:#827717;

    classDef arrowtext stroke-width:0px,stroke-dasharray:3,3,color:#555,font-size:11px;
    classDef http stroke-dasharray:5 5,stroke:#90a4ae,color:#455a64,font-size:11px;
```

## Purpose
Modernize GeneWeb by replacing monolithic OCaml binaries with a service-oriented Python stack (FastAPI + SQLAlchemy) while preserving feature parity (gw / gwsetup) and enabling incremental migration of legacy operations (conversion, export, consanguinity calculation, utilities) into maintained, testable modules and API endpoints.

## High-Level Goals
- Single unified HTTP API for both public (read) and restricted (admin/maintenance) operations.
- Database-backed persistence (PostgreSQL) replacing opaque array-based .gwb storage, with a compatibility import/export layer.
- Pluggable data processing tasks (former binaries) exposed via REST or background jobs.
- Clear separation of concerns: Presentation (Svelte frontends) / API layer / Domain services / Data access.
- Extensibility via a controlled plugin system without compromising core integrity or security.

## Component Breakdown
### Frontends
- Open Svelte frontend (`gw` replacement): public browsing & search.
- Config/Admin Svelte frontend (`gwsetup` replacement): maintenance, imports, index rebuilds, permission management.
Both communicate exclusively through the HTTP API (no direct DB or filesystem access).

### API Layer (FastAPI)
- `API1` (Open endpoints): read-only or low-risk operations (search persons, view trees, events, titles, relationships, media, exports of public data).
- `API2` (Restricted endpoints): mutation, administrative tasks, importing GEDCOM, generating exports, running compute-heavy tools (consanguinity, diff, database maintenance). Optional IP filtering + token/JWT auth.
- Background task integration (FastAPI + worker, e.g. Celery / RQ) planned for long-running jobs (imports, recomputation) to avoid blocking requests.

### Data Processing Module (`DP`)
Encapsulates migrated logic of legacy binaries:
- `consang`: consanguinity calculations.
- `ged2gwb` / `gwb2ged`: bidirectional GEDCOM conversion (internally now DB <-> GEDCOM, with optional intermediate in-memory .gwb adapter for backward compatibility).
- `gwu`: update / maintenance utilities (index rebuild, caches, cleanup) turned into idempotent service functions.
- Future: diffing (gwdiff), export variants (gwexport), lineage graphing.

### DB Connector (`DBS`)
- SQLAlchemy ORM + repository/service abstractions.
- Centralizes session lifecycle, transactions, and retry/backoff strategies.
- Provides a boundary to implement future multi-tenancy (schema-per-base or row-level scoping) and soft deletes/auditing.

### PostgreSQL Store (`DBP`)
- Canonical persisted state.
- Transitional support: import existing `.gwb` data into normalized schema (see `database_schemas/`).
- Potential event sourcing or change audit tables added later for provenance.

### Configuration (`ENV`)
- `.env` or environment variables control DB URL, plugin directory, security toggles, worker backend, rate limits, logging level.
- Configuration validated at startup (e.g. Pydantic Settings) to fail fast.

### Plugins (`PLUG`)
- Discovery via entry points or directory scanning.
- Strict contract: register routes (namespaced), or provide data processors; no direct DB schema mutations without migration registration.
- Isolation guidelines: minimal shared state, dependency injection for services, input/output validation.

## Request Lifecycle (Typical Read)
1. Frontend issues HTTP request to open endpoint.
2. FastAPI router validates params (Pydantic models).
3. Service layer composes repositories (SQLAlchemy queries) / applies domain logic.
4. Response serialized (JSON) with hypermedia/style conventions (e.g. stable IDs, pagination, ETag for caching).
5. Optional caching layer (future) short-circuits hot reads.

## Legacy Binary Migration Strategy
| Legacy Binary | New Form | Notes |
|---------------|----------|-------|
| gw / gwc (read) | API1 endpoints | Aggregated under resource controllers |
| gwsetup | API2 endpoints + Admin UI | IP restriction applied |
| ged2gwb | Import service + background task | Streams GEDCOM -> staging -> normalized tables |
| gwb2ged | Export service | Query -> assemble GEDCOM with consistent ordering |
| gwu | Maintenance endpoints | Idempotent operations (rebuild indexes, recalc metrics) |
| consang | Analysis service | Precomputes metrics, stores derived stats tables |
| gwexport | Export profiles | Could map to templated serializers |
| gwdiff | Comparison service | Planned: structural diff between versions / bases |

## Data Layer Strategy
- Start with pragmatic denormalized fields (textual place, source, notes) to accelerate migration; refactor into dedicated tables iteratively.
- Use integer-coded enums initially (documented in `database_schemas/README.md`) then migrate to FK lookup tables once stabilized.
- Consistency enforcement: database constraints + service invariant checks (e.g. no circular parentage, chronological sanity for life events).

## Security & Access Control
- Split open vs restricted routers
- Mandatory IP allowlist for sensitive operations (import/export, system maintenance)

## Related Documentation
- [Legacy storage format](../docs/geneweb/architecture/storage-format.md)
- [Enumerations & schema](./database_schemas/README.md)
- [Consanguinity algorithm deep-dive](../docs/geneweb/algorithms/consanguinity.md)

## Change Log
- 2025-09-12: Added architecture explanation sections below diagram.