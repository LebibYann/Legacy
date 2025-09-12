# Code Architecture (Legacy GeneWeb)

This document drills deeper than the high-level overview, mapping major source files to responsibilities and showing how binaries compose them.

## Module Categories

| Category | Purpose | Representative Modules |
|----------|---------|------------------------|
| Data Access & Persistence | Read/write array segments; patch, sync, locking. | `Geneweb_db.Driver`, `Db_gc` |
| Core Domain | Person/family manipulation, dates, events, history. | `date*`, `event`, `history*`, `difference` |
| Integrity & Repair | Detect/patch inconsistencies. | `fixbase`, `check*`, `fixbase` (patch constructors) |
| Selection / Traversal | Ancestors, descendants, parentship, search. | `advSearchOk*`, `alln*`, `dag*`, `gwexport` helpers |
| Export / Import | GEDCOM parsing, .gw compilation/export. | `ged2gwb`, `gwc` (with `Gwcomp`), `gwu`, `gwb2ged` |
| Analysis Tools | Diff, connectivity, consanguinity. | `difference`, `connex`, `ConsangAll` |
| Web Layer | HTTP parsing, templating, auth, plugins. | `gwd`, `Templ`, `robot`, `config` |
| Internationalization | Lexicon load/merge, language aliasing. | Lexicon logic inside `gwd`, plugin assets |
| Caching & Indexes | Names/places caches; NLDB; occurrence keys. | `cache_files`, `update_nldb`, `hasher`, `Fixbase.fix_key` |
| Utilities | Hashing, string ops, common helpers. | `hutil`, `hasher`, `Mutil` (if present) |

## Binary to Module Dependency (Indicative)

```
[gwd] --> Driver, config, Templ, hasher, lexicon loaders, plugins, Gwexport (selection for some views)
[gwc] --> Gwcomp (parser), Driver, Fixbase (optional), Consang (if -cg), ProgrBar
[gwu] --> Gwexport (selection), Driver, GwuLib
[gwb2ged] --> Gwexport, Gwb2gedLib, Driver
[ged2gwb] --> charset converters (ansel), Driver, Fixbase (post-run via user), date parsing
[gwfixbase] --> Fixbase, Driver, ProgrBar
[consang] --> ConsangAll, Driver
[connex] --> Driver (graph via families/persons arrays), selection helpers
[gwdiff] --> difference, Driver
[cache_files] --> Driver, ProgrBar
[update_nldb] --> NotesLinks, Driver
[gwgc] --> Db_gc, Driver
[setup] --> parameter builders, lexicon, shells out to other binaries
```

## Typical Call Chains

### Person Page (HTTP)
`gwd` → parse request → resolve base → (Driver.get_person) → compute relationships (selection funcs) → `Templ` render.

### Consanguinity
`consang` → load arrays (`-fast` preloads) → `ConsangAll.compute` → patch persons with coefficients → `Driver.sync`.

### Connectivity
`connex` → BFS/DFS over families: father/mother → child unions → accumulate component → (optional) deletion patches.

### Diff
`gwdiff` → pairwise person/family match by key/occ → compare significant fields → accumulate messages → print grouped diff.

## Global Refs / Config Patterns

Many binaries follow pattern:
```
let opt_flag = ref false
let opt_value = ref default
let speclist = [ "-flag", Arg.Set opt_flag, "..."; "-value", Arg.Set_int opt_value, "..." ]
```
Then after `Arg.parse`, logic reads these refs. This legacy pattern hampers reusability; future refactor: create a record `t` populated by a pure option parser.

## Error Handling

- Predominantly exceptions (`failwith`, custom) caught at top-level to print message then `exit 2`.
- Limited granularity: different IO / parse errors often conflated.
- Recommendation: introduce result types for import/export; map to structured exit codes.

## Locking Strategy

- File-based locks under base dir (e.g., `gwd.lck`).
- Most write tools acquire lock unless `-nolock`.
- Lock misuse (skipping) can corrupt arrays if concurrent writers run.

## Performance Hotspots

| Area | Impact | Mitigation |
|------|--------|------------|
| Consanguinity (graph traversal) | O(n * a) where a = average ancestors depth | Incremental mode; `-fast` arrays in memory. |
| GEDCOM import | Large file streaming & allocation | Stream parser; consider chunked decoding improvements. |
| Selection (deep ancestors/descendants) | BFS expansions | Marker bitsets reused; ensure no repeated allocations. |
| Diff on large bases | Quadratic matching risk if ambiguous keys | Key-based initial indexing; report ambiguities early. |
| NLDB update | Many small string scans | Potential optimization: batch regex / Aho–Corasick (future). |

## Modernization Roadmap (Excerpt)

1. Pure configuration records for binaries.
2. Extract persistence interface; add property tests.
3. Replace ad-hoc progress bars with unified reporter.
4. Introduce structured logging (levels + context).
5. Add CI tests for import/export roundtrip idempotence.

See also: `algorithms/` and `formats/` documents.
