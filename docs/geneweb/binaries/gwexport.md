# gwexport – Selective GeneWeb base exporter (generic backend)

`gwexport` produces textual exports (mostly genealogy oriented plain text) with flexible selection filters (ancestors, descendants, censored living persons, surnames subsets, parentship sets, pictures). Other binaries (`gwb2ged`, `gwu`) reuse its selection logic.

## Option summary (from `gwexport.ml`)

| Option | Arg | Description |
|--------|-----|-------------|
| -a | <N> | Ascendant generations of root keys (see `-key`). |
| -ad | <N> | Ascendants AND their descendants (bounded) of root keys. |
| -key | <KEY> | Root person key (may repeat). Format: `FirstName.occ SURNAME`. |
| -c | <NUM> | Censor persons born less than NUM years ago unless Public; cascades to spouses + descendants. -1 triggers visibility-based restriction mode. |
| -charset | <ASCII|ANSEL|ANSI|UTF-8> | Output charset (default UTF-8). |
| -d | <N> | Descendant generations of root keys. Negative store used internally for desc depth. |
| -mem | (flag) | Save memory (slower). |
| -nn | (flag) | Suppress database notes (base/global). |
| -nnn | (flag) | Suppress all notes (implies -nn). |
| -nopicture | (flag) | Do not extract individual picture data. |
| -o | <FILE> | Output file (default stdout). |
| -parentship | (flag) | Select persons involved in parentship computation between pairs defined by successive `-key` options (interpreted as descendant, then ancestor). |
| -picture-path | (flag) | Output only picture path entries. |
| -s | <SURNAME> | Select this surname; repeat for union of surnames. |
| -source | <SRC> | Replace individuals/families sources with SRC (removes event sources). |
| -v | (flag) | Verbose (progress messages). |

The tool does not itself generate GEDCOM; use `gwb2ged` for GEDCOM output. It’s mainly a selection + formatting engine feeding other exporters or custom downstream processing.

## Selection model

The exported set = persons & families accepted by combined filters:

1. Start with empty set.
2. Add roots from `-key` arguments and optional directly supplied IPER list (none by default).
3. If `-a` / `-d` / `-ad` populate ancestors / descendants breadth-limited; algorithms implemented in `select_asc`, `Util.select_desc`, `select_ascdesc` merging results into marker sets.
4. If surnames specified: union with those whose father or mother (family) or personal surname matches (case-insensitive normalized).
5. If `-parentship`: interpret `-key` pairs as (descendant, ancestor) and compute intersection of descendant’s ancestors and ancestor’s descendants building path families.
6. Censorship (if `-c` positive) marks persons younger than threshold (current_year - c) & cascades to families; `-c -1` uses base visibility rather than date threshold.
7. Remove censored persons/families from selection.

Functions build boolean selectors `(iper -> bool)` and `(ifam -> bool)` returned to caller. Exporter iterates arrays and serializes fields according to `gwexport_opts` (notes suppression, charset conversion with mapping functions matching chosen charset, etc.).

## Censorship details

`Is_censored_person` compares birth year (converted via `Date.cdate_to_dmy_opt`) with threshold; if birth year >= threshold and access not `Public`, person is censored; their spouses and descendants propagate censorship. Marker bits (int flags) track censorship for persons & families.

## Notes suppression flags

- `-nn` removes base/global notes but keeps personal/family notes.
- `-nnn` removes all notes (implies `-nn`). Implementation checks `no_notes` variant.

## Parentship mode

Given pairs of keys (A,B) where A is descendant and B ancestor candidate, it returns the intersection of ancestor set of A and descendant set of B, along with families uniting those persons. Useful for computing bloodline links.

## Source override

If `-source SRC` provided, replaces individual/family sources and deletes event sources (sanitizing provenance in published views).

## Output structure

Plain textual lines; when extracting pictures (`-picture-path`) each line likely contains a mapping from person key to image path (implementation dependent). Charset conversion performed at final emission stage.

## Typical usage examples

Export 4 generations of ancestors + all their descendants (2 generations):
```
gwexport -key "Jane.0 DOE" -a 4 -ad 2 base > subset.txt
```

Export only surname CLARK (uncensored) to ANSI charset without notes:
```
gwexport -s CLARK -nn -charset ANSI base > clark.txt
```

Parentship individuals between two lines:
```
gwexport -parentship -key "Child.0 LINE1" -key "Ancestor.0 LINE2" base
```

Export public subset censoring last 90 years:
```
gwexport -c 90 base > public.txt
```

## Related

- `gwb2ged` – GEDCOM output using these selectors.
- `gwu` – .gw textual export (also uses selectors).
- `cache_files` – produce caches for autocompletion after selection operations.

