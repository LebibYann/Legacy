# GeneWeb python port

This readme will introduce the geneweb migration project

## Migration: Legacy OCaml (Caml) to Python Tooling

Some auxiliary scripts and future automation may move to Python while core performance‑critical genealogy logic remains in OCaml. This section outlines the migration approach.

Goals:
* Preserve proven OCaml algorithms (graph traversal, consanguinity, relationship calculus).
* Allow rapid scripting, data munging, and integration tasks in Python.
* Maintain a stable RPC / CLI boundary so existing deployments continue to work.

Strategy:
1. Identify candidates for Python re‑implementation: standalone one‑shot tools, data export filters, reporting, simple format converters where performance is not critical.
2. Define clear boundaries: OCaml keeps internal database representation, indexing, caching, and heavy computations; Python consumes exposed JSON/RPC endpoints or CLI outputs.
3. Add thin adapters instead of duplicating logic. Prefer: gwd RPC → Python client library → user scripts.
4. Introduce a `python/` directory (when first Python module lands) with its own `pyproject.toml` or `requirements.txt` and tests.
5. Data exchange format: JSON (UTF‑8). Avoid bespoke text parsing; if an endpoint lacks JSON today, add a parallel `--json` or `?fmt=json` flag.
6. Testing: mirror a small golden dataset; assert parity between OCaml tool output and Python rewrite before deprecating the former.
7. Gradual deprecation: mark legacy OCaml helper with `@deprecated` note in its help text once the Python version reaches feature parity; remove only after two minor releases.

Interfacing Options (choose case‑by‑case):
* Process boundary (preferred): Python `subprocess` calls existing binaries with `--json` output.
* HTTP/RPC: Python client queries running `gwd` for dynamic data.
* FFI (last resort): Use `pyml` or C stubs only if zero‑copy access gives measurable win (benchmark first).

Commit Tagging for Migration:
* `feat(python):` new Python module/tool.
* `refactor(lib):` extracted logic to make it callable from both sides.
* `chore(build):` added Python packaging / CI wiring.
* `docs(migration):` updates to this section.

Readiness Checklist for Each Migrated Tool:
* Parity test added (`tests/python_parity/` suggested path).
* Benchmark (if performance relevant) shows <10% regression or justified.
* Documentation updated (usage examples in root or `python/README.md`).
* Release notes mention availability + any flags changed.

Open Questions (track via issues):
* Standard authentication handshake for Python client to authenticated endpoints.
* Unified schema definition (e.g., JSON Schema or OpenAPI) auto‑generated from OCaml types.
* Packaging strategy (single `geneweb-tools` PyPI package vs multiple).

If you plan a Python migration PR: open an issue labeled `migration` describing scope, boundary, expected gains, and deprecation timeline.

## Running the docker

To run the Docker containers for the New Geneweb project, you can use the provided `docker-compose.yml` file at the root of this project. Make sure you have Docker and Docker Compose installed on your machine.

Here's how to start it:
```bash
docker compose up --build
```
Alternatively if you want to run it in development mode, you can use:
```bash
docker compose --profile="dev" up --build
```

## Documentation
* Main OCaml project README (build, usage, links): [`geneweb/README.md`](geneweb/README.md)
* Community wiki: https://geneweb.tuxfamily.org/
* Colab demo / quick exploration: `geneweb/geneweb_colab.ipynb`
* Contributor guide: `geneweb/CONTRIBUTING.md`

## Commit Convention

We use a lightweight variant of Conventional Commits to keep history and changelog generation coherent.

Format:

```
<type>(<scope>): <short summary>

[optional body]
[optional footer(s)]
```

Rules:
* Use lowercase type; imperative mood in summary ("add support", "fix crash", "refactor parser").
* Keep summary ≤ 72 chars; wrap body at ~100 chars.
* Reference issues with `Refs: #123` or close them with `Closes: #123` in footers.
* Multiple scopes allowed: `feat(lib,templates): ...` (keep to ≤2 when possible).
* Breaking changes: add `!` after type or scope and a `BREAKING CHANGE:` footer explaining migration.

Accepted types:
* `feat` – new user or API feature
* `fix` – bug fix
* `perf` – performance optimization
* `refactor` – code change without feature/bug impact
* `docs` – documentation only (README, guides, comments)
* `test` – add or adjust tests
* `build` – build system, opam/dune adjustments
* `ci` – continuous integration / workflows
* `chore` – maintenance (dependencies, scripts) with no code impact
* `style` – formatting, whitespace (no logic changes)
* `i18n` – translations or lexicon updates
* `templates` – template/UI layer changes
* `plugins` – plugin additions or modifications

Common scopes:
`core`, `lib`, `ui`, `server`, `api`, `templates`, `plugins`, `build`, `deps`, `docs`, `i18n`, `tests`.

Examples:
```
feat(server): add PDF/HTML document route m=DOC
fix(lib): guard cousin cache when base has single individual
perf(core): reduce consanguinity computation allocations
refactor(templates): extract carousel component logic
docs(readme): add commit convention section
feat(lib)!: switch default archival format to gwplus
BREAKING CHANGE: old .gw output requires flag -old_gw to export legacy format.
```

Commit Hygiene:
* One logical change per commit; split large refactors.
* Run `make fmt` and relevant tests/bench (where available) before pushing.
* Avoid committing generated artifacts (build outputs, temporary caches).