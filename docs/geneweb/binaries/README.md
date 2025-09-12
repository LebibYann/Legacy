# GeneWeb Binaries Documentation Index

This directory contains per-binary technical documentation extracted from source code in `bin/` and related modules under `lib/`.

| Binary | Purpose |
|--------|---------|
| [`gwd`](gwd.md) | HTTP daemon serving GeneWeb databases (auth, plugins, templates, workers). |
| [`gwc`](gwc.md) | Compiler/linker: `.gw` / `.gwo` sources → `.gwb` database. |
| [`consang`](consang.md) | Recompute consanguinity (inbreeding) coefficients. |
| [`connex`](connex.md) | Analyze & optionally prune connected family components (branches). |
| [`gwfixbase`](gwfixbase.md) | Integrity checker & automatic repair (parents, unions, UTF‑8, keys, witnesses). |
| [`ged2gwb`](ged2gwb.md) | GEDCOM importer → GeneWeb database. |
| [`gwb2ged`](gwb2ged.md) | GeneWeb database exporter → GEDCOM (reuses `gwexport` selectors). |
| [`gwexport`](gwexport.md) | Generic selection/export engine (ancestors, descendants, surnames, censorship). |
| [`gwgc`](gwgc.md) | Garbage collector (removes orphaned persons/families/strings). |
| [`gwu`](gwu.md) | Export database to textual `.gw` / `gwplus` format (roundtrip with `gwc`). |
| [`gwdiff`](gwdiff.md) | Structural diff between two databases (persons/families fields). |
| [`cache_files`](cache_files.md) | Build gzip caches (names, places, titles, sources) for faster UI search. |
| [`update_nldb`](update_nldb.md) | Rebuild Notes Links DataBase (NLDB) & link frequency cache. |
| [`setup`](setup.md) | Web-based configuration/import/maintenance wizard invoked from `gwd`. |

Each file (`<binary>.md`) includes: purpose, internal architecture notes, CLI options, implementation highlights, usage examples, related tools, and (where relevant) performance & safety considerations.

Suggested reading order for newcomers:
1. `gwc.md` (how a database is built)
2. `gwd.md` (serving & runtime architecture)
3. `gwexport.md` (selection logic powering other exporters)
4. Import/export pair: `ged2gwb.md` / `gwb2ged.md`
5. Maintenance: `gwfixbase.md`, `consang.md`, `gwgc.md`, `cache_files.md`, `update_nldb.md`
6. Analysis & tooling: `connex.md`, `gwdiff.md`
7. Roundtrip textual workflow: `gwu.md`
8. Admin UI: `setup.md`

Adjacently useful improvements (not yet implemented here):
- Diagrams (request flow, plugin loading sequence, selection pipeline).
- Cross-reference index of OCaml modules → binaries that use them.
- Quick cheat sheet of common operational sequences (e.g., import pipeline: ged2gwb → gwfixbase → consang → cache_files → update_nldb).
