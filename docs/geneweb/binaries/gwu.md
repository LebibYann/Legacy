# gwu – Export GeneWeb database to textual .gw (and gwplus) format

`gwu` exports a database to GeneWeb source format (`.gw` or extended `gwplus`), enabling roundtrip editing and reimport with `gwc`. It supports splitting output into multiple files, isolating subtrees, and backward compatibility mode.

## Features

| Feature | Description |
|---------|-------------|
| gwplus vs legacy | Default emits `gwplus` header (extended fields). `-old_gw` forces legacy format compatibility (< 7.00). |
| Isolation sets | `-isolated` plus selection restricts to persons not connected to others outside selection. |
| File splitting | `-odir` writes each logical group / person file to directory rather than a single stream. |
| Separation groups | `-sep` person+anc/desc groups dumped to stdout instead of file (useful for manual inspection). |
| Group limit | `-sep_limit` threshold for reconnecting small isolated groups to stdout instead of own file. |
| Include all notes_d | `-all_files` ensures even files without wiki links in notes_d are embedded in export. |
| Raw output | `-raw` disables automatic UTF-8 encoding line. |

The exporter reuses `gwexport` selection layer; any of its filters (ancestors, descendants, surnames, censorship, keys) can be provided before `gwu` specific flags.

## Options (specific)

| Option | Arg | Meaning |
|--------|-----|---------|
| -odir | <DIR> | Output directory for per-file export. |
| -isolated | (flag) | Export only isolated persons (works only when exporting entire DB). |
| -old_gw | (flag) | Use old format (omit extended fields). |
| -raw | (flag) | Do not prepend encoding or gwplus lines; output raw text. |
| -sep | <FirstName.num Surname> | Separate this person’s connected subtree (ancestors + descendants sharing surname); may repeat. |
| -sep_only_file | <FILE> | With -sep, only separate groups appearing in given file. |
| -sep_limit | <N> | Size threshold for auto-redirecting small groups to stdout. Default from `GwuLib.sep_limit`. |
| -all_files | (flag) | Include all notes_d files (even without wiki links). |

All `gwexport` options (see `gwexport.md`) are also available.

## Internal steps

1. Parse args, build `Gwexport.gwexport_opts`.
2. Load arrays needed (ascends, strings, optionally unions/couples/descends unless `mem` optimization chosen).
3. Determine output stream(s): either single `oc` from opts.Gwexport.oc or multiple based on `-odir` & per source file logic (tracked in `src_oc_ht`).
4. Prepare free occurrences (`GwuLib.prepare_free_occ`) so keys for new persons remain consistent and duplicates avoided in separated groups.
5. Write header: `encoding: utf-8` then `gwplus` (unless `-raw` / `-old_gw`).
6. Traverse selected persons/families; output persons with events, notes, unions, witnesses; optionally group splitting rules adjust destination.
7. Close all open file channels.

## Examples

Export whole base to one file:
```
gwu base > base.gw
```

Export ancestors 5 generations of a root person to directory (one file per original source):
```
gwu -key "Alice.0 MARTIN" -a 5 -odir out_dir base
```

Separate two lineages for manual merge review:
```
gwu -odir export -sep "John.0 DOE" -sep "Mary.0 SMITH" base > separated_groups.txt
```

Legacy format for older GeneWeb:
```
gwu -old_gw base > legacy_format.gw
```

## Related

- `gwc` – recompiles exported `.gw` back into a database.
- `gwb2ged` / `ged2gwb` – alternative interop with GEDCOM.

