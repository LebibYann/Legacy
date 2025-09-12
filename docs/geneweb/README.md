# GeneWeb Legacy Documentation Hub

This hub indexes the added documentation for the legacy GeneWeb code in this repository. Use it as an entry point.

## Quick Start Paths

| Goal | Start Here | Then Look At |
|------|------------|--------------|
| Understand overall system | [architecture/overview.md](architecture/overview.md) | [architecture/code-architecture.md](architecture/code-architecture.md) |
| Learn binary tools | [binaries/README.md](binaries/README.md) | Individual binary docs (same folder) |
| Explore data & storage | [formats/overview.md](formats/overview.md) | (Future) detailed format specs |
| See core algorithms | [algorithms/overview.md](algorithms/overview.md) | Binary docs for specifics |
| Run maintenance after import | [binaries/ged2gwb.md](binaries/ged2gwb.md) | [binaries/gwfixbase.md](binaries/gwfixbase.md), [binaries/consang.md](binaries/consang.md), [binaries/cache_files.md](binaries/cache_files.md), [binaries/update_nldb.md](binaries/update_nldb.md) |
| Export / migrate data | [binaries/gwc.md](binaries/gwc.md) | [binaries/gwb2ged.md](binaries/gwb2ged.md), [binaries/gwu.md](binaries/gwu.md) |
| Investigate differences | [binaries/gwdiff.md](binaries/gwdiff.md) | [algorithms/overview.md](algorithms/overview.md) (diff section) |
| Prune / clean database | [binaries/connex.md](binaries/connex.md) | [binaries/gwgc.md](binaries/gwgc.md), [binaries/gwfixbase.md](binaries/gwfixbase.md) |
| Deep storage layout | [architecture/storage-format.md](architecture/storage-format.md) | [formats/overview.md](formats/overview.md) |
| Consanguinity math | [algorithms/consanguinity.md](algorithms/consanguinity.md) | [binaries/consang.md](binaries/consang.md) |
| NLDB schema & links | [formats/nldb.md](formats/nldb.md) | [binaries/update_nldb.md](binaries/update_nldb.md) |
| Security hardening | [operations/security.md](operations/security.md) | [binaries/gwd.md](binaries/gwd.md) |

## Directory Map

```
/docs/geneweb
  README.md               (this file)
  architecture/           (system & code structure)
  algorithms/             (high-level algorithm summaries)
  binaries/               (per-binary deep dives)
  formats/                (on-disk & auxiliary format descriptions)
```

## Suggested Learning Sequence

1. Architecture overview: big picture components.
2. Binary index: see what each executable does.
3. Algorithms: internal mechanics of selection, consanguinity, diff, etc.
4. Formats: how data is persisted and cached.
5. Specific binary docs when you need option/implementation details.

## Common Maintenance Workflow

```
1. Import: ged2gwb (or gwc for .gw)
2. Repair: gwfixbase (dry-run first)
3. Compute: consang
4. Build caches: cache_files -all
5. Build NLDB: update_nldb
6. Serve: gwd (optionally with setup link disabled in production)
7. Analyze (optional): connex / gwdiff / gwgc
```


## Contributing Updates

When adding new docs under `docs/geneweb/`:
1. Keep filenames lowercase with hyphens.
2. Link them here under appropriate sections.
3. Prefer concise tables + diagrams (ASCII or PlantUML) before long prose.
4. Cross-link binary docs instead of duplicating option tables.

## Quick Links

- Server (`gwd`): `binaries/gwd.md`
- Compiler (`gwc`): `binaries/gwc.md`
- Import GEDCOM: `binaries/ged2gwb.md`
- Export GEDCOM: `binaries/gwb2ged.md`
- Text Export: `binaries/gwu.md`
- Integrity Repair: `binaries/gwfixbase.md`
- Consanguinity: `binaries/consang.md`
- Selection Engine: `binaries/gwexport.md`
- Caches: `binaries/cache_files.md`
- NLDB Update: `binaries/update_nldb.md`
- Diff: `binaries/gwdiff.md`
- Connectivity: `binaries/connex.md`
- Garbage Collection: `binaries/gwgc.md`
- Setup Wizard: `binaries/setup.md`

---
This is a living index; expand it as deeper docs are introduced.
