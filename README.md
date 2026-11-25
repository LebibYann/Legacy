# GeneWeb modernization: from OCaml to Python and Svelte

[GeneWeb](https://github.com/geneweb/geneweb) is a genealogy application written in OCaml since the 1990s. This project starts replacing it with a **FastAPI** back end and **SvelteKit** front ends, **without switching the old engine off**: a proxy serves the pages that have been rewritten and falls back to the original GeneWeb for all the others.

<p align="center">
  <img src="assets/readme/backoffice_home.png" width="760" alt="Administration home page rewritten in SvelteKit, with the GeneWeb logo, links to consult, save, create and configure family trees, and a language selector">
  <br><em>The administration home page, rewritten in SvelteKit. Most of its links still open the OCaml pages.</em>
</p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Svelte](https://img.shields.io/badge/Svelte-FF3E00?style=for-the-badge&logo=svelte&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![OCaml](https://img.shields.io/badge/OCaml-EC6813?style=for-the-badge&logo=ocaml&logoColor=white)

## Features

- **Fallback proxy**: each request goes to the new front end first, then to the OCaml server when the new one does not answer or returns an error such as 404
- **Database API**: list, create and delete GeneWeb databases, with HTTP Basic authentication on writes
- **`.gwb` connector**: manages databases in the original format through the GeneWeb binaries. Person and family operations, through GEDCOM, are written but not functional yet (see [Project status](#project-status))
- **Backoffice**: home page and database list in SvelteKit, in 8 languages
- **Relational model**: SQLAlchemy models and an Alembic migration for 10 PostgreSQL tables, ready for a later move out of `.gwb` files
- **Tests at each level**: OCaml engine, binaries, back end, front end and end-to-end

## Screenshots

| Rewritten page (SvelteKit and the new API) | Original page (OCaml), served through the proxy |
|---|---|
| ![List of databases](assets/readme/database_list.png) | ![Home page of a family tree with 482 individuals](assets/readme/legacy_tree.png) |

## Architecture

```mermaid
flowchart TB
    Browser(["Browser"])
    Nginx["<b>nginx</b><br/>ports 2316 and 2317, HTTPS"]

    subgraph backend["Back end (FastAPI)"]
        Auth["Basic auth<br/>port 2316 only"]
        Proxy["Fallback proxy"]
        Api["REST API, under /api"]
        Conn["DBConnector"]
        Legacy["LegacyDB provider"]
        PgP["PostgresProvider<br/>skeleton"]
    end

    Back["Backoffice<br/>SvelteKit"]
    Old["Original GeneWeb, OCaml<br/>gwsetup and gwd"]
    Gwb[(".gwb files")]
    Pg[("PostgreSQL")]

    Browser --> Nginx --> Auth --> Proxy
    Proxy -->|"/api"| Api
    Proxy -->|"1. rewritten pages"| Back
    Proxy -->|"2. everything else"| Old
    Api --> Conn --> Legacy
    Conn -.-> PgP
    Legacy -->|"GeneWeb binaries"| Gwb
    Old --> Gwb
    PgP -.-> Pg
```

The new API and the OCaml servers share the same `.gwb` files, so a database created on one side is visible on the other. Pages can then be moved one at a time:

```mermaid
sequenceDiagram
    participant B as Browser
    participant P as Fallback proxy
    participant S as Backoffice (SvelteKit)
    participant O as gwsetup (OCaml)
    B->>P: GET /list
    P->>S: GET /list
    S-->>P: 200
    P-->>B: rewritten page
    B->>P: GET /gwsetup?v=merge.htm
    P->>S: GET /gwsetup?v=merge.htm
    S-->>P: 404
    P->>O: GET /gwsetup?v=merge.htm
    O-->>P: 200
    P-->>B: original page
```

Genealogical data goes through one interface, `DatabaseProvider`, with two implementations: `LegacyDB` for `.gwb` files, and a PostgreSQL one that is still to be written.

```
new_geneweb/
  backend/            FastAPI API, proxy, persistence, Alembic migration
  backoffice/         SvelteKit administration front end
  frontend/           SvelteKit public front end (scaffold)
  database_schemas/   SQL tables and their documentation
nginx/                reverse proxy, HTTPS or HTTP
geneweb/              original OCaml source code
geneweb_docker/       Docker image of the original GeneWeb
tests/functional/     pytest suite for the OCaml binaries
tests/end-to-end/     Playwright tests, for the original and the new pages
docs/geneweb/         documentation of the original code
.github/workflows/    CI for each component
```

## Run

Requires Docker with Compose. The first build compiles GeneWeb from its sources.

```bash
docker compose up --build
```

| Address | Content |
|---|---|
| `https://localhost:2316` | Administration, with the credentials set in `docker-compose.yml` |
| `https://localhost:2317` | Family trees |
| `https://localhost:2317/api/docs` | Swagger documentation of the API |

The certificate is self-signed. For plain HTTP, add `-f docker-compose.yml -f compose.http.yml` after `docker compose`. See [nginx/README.md](nginx/README.md) for trusted certificates.

| Method | Route, under `/api` | State |
|---|---|---|
| GET, POST | `/bases` | Works on `.gwb` databases |
| DELETE | `/bases/{base_name}` | Works on `.gwb` databases |
| POST, GET, DELETE | `/bases/{base_id}/individuals` | Contract only, fixed answers |
| POST, PUT, PATCH, GET, DELETE | `/bases/{base_id}/families` | Contract only, fixed answers |

## Tests

Requires Python 3.13 with Poetry, Node.js 20 or later, and opam with OCaml 4.14.1. The back end tests call the OCaml binaries, so build the engine first.

```bash
# Original engine: build and unit tests
cd geneweb
opam install . --deps-only --with-test
ocaml ./configure.ml && make distrib
dune runtest

# Functional tests of the OCaml binaries (needs pytest)
cp -r distribution/gw ../tests/functional/binaries
cd .. && python3 -m pytest tests/functional

# Back end: lint, types and tests
cd new_geneweb/backend
poetry install --no-root
export DATABASE_URL=postgresql+asyncpg://user:password@localhost/geneweb
export BACKOFFICE_USERNAME=admin BACKOFFICE_PASSWORD=admin
GW=$(realpath ../../geneweb/distribution/gw)
export GWB_PATH=$(mktemp -d) GWC_BIN=$GW/gwc GWB2GED_BIN=$GW/gwb2ged GED2GWB_BIN=$GW/ged2gwb
poetry run ruff check . && poetry run mypy app/
poetry run pytest

# Backoffice: unit tests and build
cd ../backoffice
npm ci
npm run test:unit -- --run
npm run build
```

The end-to-end tests need a running stack: see [tests/end-to-end/Readme.md](tests/end-to-end/Readme.md).

## Project status

This is a school project, kept as it was delivered. The migration is at its beginning, and the code has these known limits:

- the family and individual routes validate their input but do not store anything yet, and they require no authentication
- the `.gwb` connector runs `gwb2ged` and `ged2gwb` in the wrong folder, so it cannot load persons and families from a real database. Its unit tests mock these binaries
- PostgreSQL holds the schema only: genealogical data stays in `.gwb` files, and the `DATABASE_URL` in `docker-compose.yml` has a `schema` parameter that `asyncpg` rejects
- the public front end is an empty scaffold, disabled in `docker-compose.yml`
- an invalid or duplicate database name returns a 500 error
- the default credentials are for local use only
- the Docker network uses `173.20.0.0/16`, which is not a private range
- the end-to-end workflow refers to a `docker-compose.dev.yml` file that is now `compose.dev.yml`
- `npm run check` reports type errors in the backoffice, in generated message code and tests

## Documentation

- [docs/geneweb/](docs/geneweb/README.md): how the original code works (architecture, storage format, algorithms, binaries)
- [new_geneweb/README.md](new_geneweb/README.md): target architecture
- [new_geneweb/backend/](new_geneweb/backend/README.md), [backoffice/](new_geneweb/backoffice/README.md), [database_schemas/](new_geneweb/database_schemas/README.md): component guides
- [TESTING.md](TESTING.md): testing strategy
- [CONTRIBUTING.md](CONTRIBUTING.md): workflow and commit convention

Some of these documents describe earlier stages or planned features.

## Team

Epitech team project (September 2025 to February 2026):

- [Yann Lebib](https://github.com/LebibYann): back end foundation, API contract, SvelteKit scaffolds, tests of the OCaml binaries, CI
- [Lenny Vigeon](https://github.com/Linnchoeuh): documentation of the original code, database design, backoffice pages, fallback proxy, authentication, nginx, Docker, CI and end-to-end tests
- [Mardochée Zossoungbo](https://github.com/itsmardochee): database connector, `.gwb` and PostgreSQL providers, SQLAlchemy models, migration and scripts, back end tests
- [Enzo Pfeiffer](https://github.com/diouck01): setup of the original project, test policy and plan, first end-to-end tests

The `geneweb/` folder is the work of the [GeneWeb project](https://github.com/geneweb/geneweb) and is distributed under the GPL-2.0: see [geneweb/LICENSE](geneweb/LICENSE).

## My contribution

Several branches were squashed on merge, so some commits group the work of several people: the commit `feat: functionnal hybrid modernized app`, under my name, merges the work of the whole team. My own part, from the commits:

- **Tests of the original engine**: a pytest suite that runs the OCaml binaries on a sample family tree (import, export, comparison, repair), and the first CI workflows for OCaml unit and functional tests
- **Back end foundation**: FastAPI project structure, settings, async SQLAlchemy and Alembic setup, Docker image and Compose service, pre-commit hooks, linting and type checking, CI workflow
- **API contract**: first version of the base, family and individual routes, with their Pydantic schemas, service layer, tests and Swagger documentation. Lenny and Mardochée then connected the base routes to the `.gwb` files
- **Database schema**: child, individual event and family event tables
- **SvelteKit scaffolds**: backoffice and public front end with TypeScript, Tailwind CSS, accessibility linting and Lighthouse CI, their Dockerfiles and CI workflows. The backoffice pages were written by Lenny
- **Guides**: root contributing guide, and README and contributing guides for the back end and both front ends
