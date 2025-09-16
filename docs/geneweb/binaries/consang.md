# consang – Consanguinity (inbreeding coefficient) recomputation tool

`consang` recomputes and stores consanguinity (inbreeding) coefficients for all persons/families of an existing GeneWeb database. It can run incrementally (default) or from scratch, optionally loading full arrays into memory for speed.

## Algorithm overview

Delegates to `ConsangAll.compute` after loading database structures using `Geneweb_db.Driver` (persons, families, ascends, unions, couples, descends, strings arrays when `-fast`). It performs a topological traversal of the ancestry graph; if a cycle is detected (person is their own ancestor) it raises `Consang.TopologicalSortError` – the tool reports and exits with code 2.

If computation succeeds it flushes patched structures via `Driver.sync` (writing updated consanguinity values back to disk).

## Options

| Option | Meaning |
|--------|---------|
| -q | Quiet (verbosity=1) – suppress non-essential progress messages. |
| -qq | Very quiet (verbosity=0) – also disables `Mutil.verbose`. |
| -fast | Load full arrays (persons/families/ascends/unions/couples/descends/strings) for faster random access; higher RAM usage. |
| -scratch | Recompute from scratch ignoring existing cached values. |
| -mem | Save memory (slower rewrites) – passes through to `Outbase.save_mem`. |
| -nolock | Skip database locking (unsafe if concurrent writers). |

Invocation format:
```
consang [options] <path/to/base(.gwb)>
```

Base path may be with or without `.gwb` extension; the program sets base directory with `Secure.set_base_dir (Filename.dirname fname)` then operates on that base.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success, database updated if changes. |
| 2 | Fatal error (missing argument, cycle detected, IO/lock error). |

## Sample usage

Recompute incrementally:
```
consang mybase.gwb
```

Full recomputation with performance trade-off (fast RAM intensive):
```
consang -fast -scratch mybase.gwb
```

Quiet cron job:
```
consang -qq -fast /srv/gw/bases/family
```

## Related

- `gwc -cg` can compute consanguinity at creation time.
- `gwfixbase` repairs structural issues that could otherwise cause cycles.

