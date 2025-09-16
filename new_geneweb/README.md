# New Python-Based Architecture Overview

```mermaid
---
config:
  layout: elk
---
flowchart TD
 subgraph Frontends["Frontends"]
        F1["**Open frontend**<br><br>Front svelte base (gw)<br>Same behaviour and feature as gw"]
        F2["**Front svelte config (gwsetup)**<br><br>Same behaviour and feature as gwsetup"]
  end
 subgraph API["API (Framework FAST API)"]
        API1["**Open endpoints**<br><br>Same behaviour and feature as gw"]
        API2["**Restricted endpoints (IP restricted)**<br><br>Same behaviour and feature as gwsetup<br>New endpoints to replace binaries:<br>• gwc<br>• gwb2ged<br>• ged2gwb<br>• etc..."]
  end
 subgraph DB["DB Connector (Encapsulation)"]
        DBS["DB Connector (SQLAlchemy)"]
  end
 subgraph Backend_Python["Backend Python (gw/gwsetup)"]
        API
        DP["**Data processing**<br><br>consang<br>ged2gwb<br>gwb2ged<br>gwu"]
        DB
  end
    ENV["env file<br>to set parameters"] --> Backend_Python
    PLUG["Plugins"] --> Backend_Python
    F1 <--> API1
    F2 <--> API2
    API --> DP
    DP <--> DB
    DBS --> DB
    DBP["DB postgre (.gwb)"] <--> DBS
    API1 <--> DB
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
| gwsetup | API2 endpoints + Admin UI | Auth & IP restriction applied |
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
- Split open vs restricted routers; enforce authentication/authorization middleware on restricted routes.
- Optional IP allowlist for sensitive operations (import/export, system maintenance) as defense-in-depth.
- Input validation & size limits (upload GEDCOM, media attachments) to mitigate resource exhaustion.
- Planned rate limiting + audit logging of administrative actions.

## Observability
- Structured logging (JSON) with correlation IDs per request.
- Metrics (Prometheus): request latency, DB query counts, background job durations.
- Tracing (OpenTelemetry) optional for complex import/export flows.

## Deployment & Scaling
- Stateless API layer (horizontal scale with load balancer).
- Background workers scaled separately for CPU-heavy tasks (consanguinity, diff, import parsing).
- PostgreSQL vertical scaling + read replicas (future) for heavy read patterns.
- Plugin hot-reload optional in development; disabled in production for determinism.

## Extensibility Principles
- Stable public API versioning (`/api/v1/...`).
- Backward-compatible schema migrations (Liquibase/Alembic) with downgrade scripts where feasible.
- Domain services expose pure functions for core transforms -> easier unit testing.

## Future Enhancements
- GraphQL overlay for richer client queries (optional).
- WebSocket channels for long-running job progress updates (imports, consang recalculation).
- Caching layer (Redis) for high-traffic endpoints (e.g. person detail, ancestry views).
- Fine-grained authorization (role/permission matrix) beyond current open/restricted split.
- Incremental adoption of event sourcing for auditing critical mutations.

## Related Documentation
- Legacy storage format: `../docs/geneweb/architecture/storage-format.md`
- Enumerations & schema: `./database_schemas/README.md`
- Consanguinity algorithm deep-dive: `../docs/geneweb/algorithms/consanguinity.md`

## Change Log
- 2025-09-12: Added architecture explanation sections below diagram.