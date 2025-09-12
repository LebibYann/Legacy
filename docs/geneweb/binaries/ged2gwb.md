# ged2gwb – GEDCOM (.ged) to GeneWeb database importer

`ged2gwb` parses a GEDCOM file and produces a GeneWeb database (`.gwb`). It maps GEDCOM records (INDI, FAM, SOUR, NOTE, OBJE, etc.) into GeneWeb persons, families, events, notes, media references, and sources, applying numerous normalization heuristics.

The implementation (`ged2gwb.ml`, ~3k LOC) performs a streaming parse using OCaml streams, constructing intermediate `record` trees (fields: `rlab`, `rval`, `rcont`, `rsons`, `rpos`) then converting them to GeneWeb internal structures.

## Key internal types

| Type | Meaning |
|------|---------|
| `person`, `family`, `union`, `ascend`, `descend`, `couple` | GeneWeb typed nodes parameterized with integer indexes (converted later to persistent arrays). |
| `record` | Parsed GEDCOM logical line with label, value, continuation text, children, original position. |
| `charset` | Input charset enumeration (`Ansel`, `Ansi`, `Ascii`, `Msdos`, `MacIntosh`, `Utf8`). Determines conversion path to UTF‑8 (`utf8_of_string`). |
| `case` | For surname case normalization: `NoCase|LowerCase|UpperCase`. |
| `month_number_dates` | Controls numeric month parsing heuristics (day/month vs month/day). |

## Parsing pipeline

1. Raw file opened; lines consumed via custom stream parsers (`get_ident`, `get_to_eoln`, `skip_eol` etc.), counting lines (`line_cnt`).
2. GEDCOM level numbers drive recursive descent (`get_lev`) producing tree of `record` nodes (sons in `rsons`).
3. Character set detection: HEAD record’s `CHAR` tag influences `charset` (converted by `ascii_of_msdos`, `ascii_of_macintosh`, Ansel mapping, or pass‑through for UTF‑8).
4. Name processing: optional splitting of first/public names, case transformations (`lowercase_first_names`, `case_surnames`, `extract_first_names`, `extract_public_names`).
5. Date normalization: interprets TEXT into GeneWeb `Date.dmy` with negative year handling heuristics (`try_negative_dates`, `no_negative_dates`), approximate qualifiers (ABT, BEF, AFT), ranges, `month_number_dates` reinterpretation.
6. Building internal tables of individuals / families, assigning indices, handling cross references (@I1@ etc.).
7. Alive/deceased inference using year thresholds (`alive_years`, `dead_years`).
8. Source / note linking; unrecognized tags optionally concatenated into notes if `untreated_in_notes`.
9. Relation / marriage status mapping (`relation_status`).
10. Final commit: open (or create) base with driver, allocate arrays, persist structures, run optional consistency check (`do_check`) or skip with `-nocheck` (if provided—option name inferred; see below).

## Important options (selection – see top‐level refs)

| Variable / CLI (typical) | Purpose |
|--------------------------|---------|
| -lowercase_first_names | Convert first names to lowercase except initial capital rules. |
| -track_ged2gw_id | Store original GEDCOM IDs into notes/keys for traceability. |
| -case_surnames [upper|lower|none] | Force surname case. |
| -extract_first_names | Split composite name fields into first names list. |
| -no_extract_public_names (inverse) | Control extraction of public/display names. |
| -charset <ANSel|ANSI|ASCII|UTF-8|MSDOS|MAC> | Override autodetected charset. |
| -alive_years <N> / -dead_years <N> | Threshold heuristics for living status inference. |
| -try_negative_dates / -no_negative_dates | Interpret years like 0030 as 30 AD vs possibly BC (negative). |
| -month_number_dates <MonthDay|DayMonth|None> | How to disambiguate numeric dates. |
| -no_public_if_titles | If person has titles, mark as non public unless explicit flag. |
| -first_names_brackets <(char)(char)> | Extract content inside brackets as first names alias. |
| -untreated_in_notes | Append unknown tags to notes rather than drop. |
| -default_source <SRC> | Apply default source to persons/families missing one. |
| -relation_status <Married|Engaged|...> | Default union status when unspecified. |
| -nopicture | Skip picture extraction. |
| -nocheck | Skip post-import database consistency check. |
| -particles <FILE> | Custom particles list for name splitting. |

Names of some flags may differ slightly; consult `ged2gwb` help output (`-help`) for authoritative list (the code defines refs; CLI binding near end of file associates them).

## Character set conversion

`utf8_of_string` selects appropriate transform to produce internal UTF‑8. Special cases:
- ANSEL mapping through `Ansel.to_iso_8859_1` then to UTF‑8.
- MSDOS / Mac extended code pages converted through mapping tables in `ascii_of_msdos` / `ascii_of_macintosh`.

## Error reporting

`print_location` prints current file & line; parsing errors raise exceptions after contextual print. Invalid structure (e.g., unexpected level transitions) typically abort import; use upstream GEDCOM validation first.

## Usage examples

Basic import:
```
ged2gwb mytree.ged
```

Force charset and surname uppercasing:
```
ged2gwb -charset ANSI -case_surnames upper tree.ged
```

Track GED IDs; treat unknown tags as notes:
```
ged2gwb -track_ged2gw_id -untreated_in_notes file.ged
```

Disable picture processing, skip consistency check for speed:
```
ged2gwb -nopicture -nocheck large.ged
```

## Post import

Run `gwfixbase` then `consang` and possibly `cache_files` for derivative data (names, places) indexes.

## Related

- `gwb2ged` exports back to GEDCOM.
- `gwu` exports to GeneWeb textual `.gw` format (roundtrip with `gwc`).

