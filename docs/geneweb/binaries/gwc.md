# gwc – GeneWeb compiler (from .gw / .gwo to .gwb database)

`gwc` compiles GeneWeb source genealogy files (`.gw`) into binary object files (`.gwo`), then links them into a persistent GeneWeb database directory (`<name>.gwb`). It can also merge or adjust multiple pre‑compiled `.gwo` inputs, compute consanguinity arrays, and apply base notes merging strategies.

Workflow:

1. For each `.gw` input: parse & compile to `<file>.gwo` unless already a `.gwo`.
2. Resolve output base name (`-o` or derived from last input) and initialize base directory structure (`GWPARAM.init`, create `<bname>.gwb`).
3. Link phase: iterate over families in each `.gwo` using `next_family_fun_templ` streaming function; unify persons, families, and notes according to options (separation, notes merge strategy, id shift).
4. Optionally compute consanguinity matrix (`-cg`) and statistics.
5. Optionally delete intermediate `.gwo` files (`-gwo`).

## Input file kinds

- `.gw`: textual GeneWeb source (persons, families, notes) – compiled first.
- `.gwo`: compiled object (marshall’d `Gwcomp.gw_syntax` values) – linked directly.

## Notes merge strategies (`-bnotes` per file)

Value applies only to the *next* file parsed then resets to default `merge`:

- `merge` (default): concatenate base notes.
- `erase`: replace current base notes with the file’s notes.
- `first`: ignore (drop) if base already has notes.
- `drop`: discard notes from that file.

## Person number shifting (`-sh`)

Adds an integer offset to person internal numbers for subsequent files (avoid collisions when concatenating separately numbered sources).

## Separate persons (`-sep`)

Marks all persons of the next file as “separate” (no linking by key with previous persons); resets after applying to that one file.

## Options (from `speclist` in `gwc.ml`)

| Option | Arg | Meaning |
|--------|-----|---------|
| -bd | <DIR> | Base directory root (where `bases`/ is). Default `.` if omitted. |
| -bnotes | <MODE> | Notes merge mode for next file (`drop|erase|first|merge`). |
| -c | (flag) | Compile only (stop after generating `.gwo`, no base build). |
| -cg | (flag) | Compute consanguinity (sets `Db1link.do_consang`). |
| -ds | <STR> | Default source string for persons/families missing one. |
| -f | (flag) | Force: remove existing database if it exists before writing. |
| -gwo | (flag) | Delete `.gwo` files after successful base creation. |
| -mem | (flag) | Save memory (slower) during linking. |
| -nc | (flag) | Disable consistency check (`Db1link.do_check`). |
| -nofail | (flag) | Continue (no failure exit) on recoverable errors. |
| -nolock | (flag) | Do not lock database during build (unsafe with concurrent use). |
| -nopicture | (flag) | Do not build associative picture structures. |
| -o | <NAME> | Output database name (without `.gwb` extension). Required if multiple input files. |
| -particles | <FILE> | Custom particles file (surname particles). |
| -q | (flag) | Quiet (clears `Gwcomp.verbose`). |
| -reorg | (flag) | Reorganization mode (affects internal storage / indexes). |
| -rgpd | <DIR> | RGPD directory (activates RGPD mode if exists). |
| -sep | (flag) | Apply person separation to next file only. |
| -sh | <INT> | Shift ids in next file by INT. |
| -stats | (flag) | Print statistics after linking. |
| -v | (flag) | Verbose (progress / dots / bar depending on number of files). |

Mutually influential flags: `-q` overrides `-v`; absence of any debug options yields minimal output.

## Multi‑file control variables

The tool stores a list `files` with tuples `(filename, separate, bnotes, shift)` snapshotting the state of transient flags for each input. After each file token, transient flags (`separate`, `bnotes`, `shift`) are reset to defaults for the next specification.

## Linking iterator `next_family_fun_templ`

Builds a closure returning successive `Gwcomp.gw_syntax` units across multiple `.gwo` streams. Auto‑opens next file, updates `fi` (Db1link linking info) with per‑file capture: current source filename, separation flag, notes strategy, and shift offset; clears local name hashtable between files.

Progress feedback varies: dots for <60 files, progress bar for larger sets (`ProgrBar`).

## Consanguinity

When `-cg` set, `db1link.do_consang` triggers runtime consanguinity computations after linking using genealogical graph arrays; expensive on large bases.

## Error handling

Compilation phase wraps each `.gw` with a try/with to report line number (`Gwcomp.line_cnt`). Fatal errors cause termination with non‑zero exit. When `-nofail`, some errors become warnings.

Base name validation uses `Mutil.good_name` (alphanumeric and `-` only); else exit.

## Typical usages

Compile a single source file:
```
gwc mytree.gw
```

Merge multiple sources with separate ids and custom notes strategy, output as `global`:
```
gwc -o global -sep source1.gw -bnotes erase source2.gw -sh 5000 source3.gw
```

Compute consanguinity and statistics:
```
gwc -cg -stats -o familydb data1.gw data2.gw
```

Compile only (produce .gwo without building database):
```
gwc -c sample.gw
```

Force overwrite existing base, quiet mode:
```
gwc -f -q -o rebuild tree.gw
```

## Output

Creates `<bname>.gwb` directory with internal binary segment files, plus a generated default configuration file (`<bname>.gwf`). Optionally removes intermediate `.gwo` if `-gwo`.

## Related

- `ged2gwb` alternative importer from GEDCOM.
- `gwfixbase` integrity fixes after creation.
- `gwd` serves compiled database.

