# GeneWeb Architecture Overview

This document gives a high-level map of the legacy GeneWeb code base to orient new maintainers.

## Layered View

```
+---------------------------------------------------------------+
|                User Interfaces / Integrations                |
|  gwd (HTTP) | setup (wizard) | CLI binaries (gwc, gwu, ...)   |
+---------------------------+-----------------------------------+
|            Application Services (Selection, Export, Fix)      |
| gwexport  consang  gwfixbase  connex  gwdiff  update_nldb     |
+---------------------------+-----------------------------------+
|                Core Domain & Utilities (lib/*.ml)             |
| Persons/Families model, Dates, Notes, Keys, Selection, Diff   |
+---------------------------+-----------------------------------+
|                 Persistence (Geneweb_db.Driver)               |
| Array files (.gwb)  Locking  Patch/Sync  Caches (names, NLDB) |
+---------------------------+-----------------------------------+
|                  System (OS, FS, Dynlink)                     |
```

## Primary Concepts

| Concept | Description | Key Modules |
|---------|-------------|-------------|
| Person / Family | Core genealogical entities stored as indexed arrays. | `person` record in generated code, accessors via `Geneweb_db.Driver` |
| Unions / Ascends / Descends | Relationship arrays tying persons to families and traversal. | `Driver` (arrays), selection algorithms in `gwexport` |
| Notes & Sources | Textual annotations and provenance. | `notes`, `update_nldb`, `NotesLinks` |
| Keys & Occurrences | Stable textual identifiers (FirstName.occ SURNAME). | `Fixbase`, key generation utilities |
| Lexicon / i18n | Localized strings & templates. | `Templ`, lexicon loaders in `gwd` |
| Plugins | Dynamically loaded feature extensions. | `gwd` (Dynlink + MD5 guard) |
| Selection | Ancestors/descendants/censorship/parentship filtering. | `gwexport` |
| Consanguinity | Inbreeding coefficient computation. | `ConsangAll` |
| Diff | Structural comparison of two bases. | `gwdiff` + `difference.ml` |
| Connectivity | Branch/component analysis. | `connex` |
| Integrity Fixing | Automatic repair of link and encoding issues. | `gwfixbase` + `fixbase.ml` |
| Garbage Collection | Removal of unreachable entities/strings. | `gwgc` + `Db_gc` |

## Execution Paths

### Import (GEDCOM)
`ged2gwb` → parse stream → build in-memory tables → write `.gwb` arrays via Driver → (optional) `gwfixbase` → `consang` → `cache_files` → `update_nldb` → serve with `gwd`.

### Import (GeneWeb textual)
`gwc` (compile .gw to .gwo → link to .gwb) → same post steps.

### Request Handling (`gwd`)
1. Accept socket / CGI stdin.
2. Parse HTTP, detect base & action.
3. Load lexicon + base config.
4. Auth (public/friend/wizard).
5. Dispatch (person page, family page, search, plugin, setup link).
6. Render template (Templ) → send response.

### Maintenance
`gwfixbase`, `consang`, `cache_files`, `update_nldb`, `gwgc`, `connex`, `gwdiff` each open the base (locking unless bypassed) and operate on arrays via Driver patch/sync.

## Data Flow Snapshot

```
 GEDCOM/.gw --> Importer (ged2gwb/gwc)
        |        (build arrays)
        v
   .gwb directory (persons, families, relations, strings)
        |  (read-only queries)
        +--> gwd (HTTP) -> templates -> HTML
        |\
        | +-> gwexport -> (gwu/gwb2ged)
        | +-> gwdiff / connex / gwfixbase / consang
        | +-> cache_files / update_nldb (aux caches)
```

## Global State & Legacy Notes
- Many binaries rely on global refs for CLI option state (mutable; not thread-safe inside same process beyond intended usage).
- Driver exposes low-level arrays; invariants are enforced by repair utilities rather than strict types.
- Text encoding: internal UTF-8; legacy import paths still have charset conversion branches.

## Modernization Opportunities
- Encapsulate mutable global flags behind modules returning pure configs.
- Abstract persistence behind a stable interface enabling alternate storage backends (DB, JSON, etc.).
- Add property tests for date parsing, key uniqueness, selection closure.

See also: `architecture/storage-format.md`, `architecture/data-model.md`.
