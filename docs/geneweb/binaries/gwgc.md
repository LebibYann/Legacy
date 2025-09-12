# gwgc – GeneWeb database garbage collector

`gwgc` performs a garbage collection pass over a GeneWeb database, identifying orphaned persons, families, and unused strings, optionally committing removals unless `--dry-run` is specified.

Internally calls `Gwdb_gc.gc ~dry_run base` (in `Geneweb_db.Db_gc`) which returns triple lists `(persons, families, strings)` removed or targeted. After completion it prints counts:

```
<base>:
	nb of persons: <n>
	nb of families: <n>
	nb of strings: <n>
```

## Usage

```
gwgc [--dry-run] <base_path>
```

If `<base_path>` has `.gwb` suffix it is used directly; else suffix is inferred. The tool acquires a lock (`gwb.lck`) to prevent concurrent modifications.

## Options

| Option | Meaning |
|--------|---------|
| --dry-run | Do not commit changes; just report potential garbage. |

## Typical scenario

Run after large deletions (e.g., via `connex -del` or manual edits) to reclaim storage and clean orphaned strings.

## Safety

Always start with `--dry-run` to verify scope; once satisfied, rerun without the flag.

## Related

- `gwfixbase` repairs links which may reduce garbage.
- `cache_files` should be regenerated after GC for search caches accuracy.

