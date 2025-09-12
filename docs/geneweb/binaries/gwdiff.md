# gwdiff – Structural diff between two GeneWeb databases

`gwdiff` compares two GeneWeb bases (persons & families) and reports differences in core genealogical data: names, sex, birth/death (dates & places), marriage/divorce info, children lists, spouses, occupation. Output can be plain text or HTML-ish link markup when `-html` specified (internally links to `gwd` via constructed URLs using provided `-root` prefix and port assumptions).

## Difference categories (messages)

| Message | Trigger |
|---------|---------|
| BirthDate / DeathDate | Date or status mismatch (precision, interval, or value). |
| BirthPlace / DeathPlace / MarriagePlace | Place field differs. |
| MarriageDate / Divorce | Marriage or divorce info mismatch. |
| FirstName / Surname | Normalized naming differs. |
| Sex | Gender mismatch. |
| Occupation | Occupation text differs. |
| ParentsMissing | Parents present in one DB but not the other. |
| ChildMissing | A child present only in one family. |
| Children | Ambiguous children matching (multiple potential matches). |
| SpouseMissing | Spouse present only in one family record. |
| Spouses | Multiple spouse ambiguities. |
| BadChild | Unable to isolate a unique matching child across DBs. |

The program attempts to match entities by keys / occurrence (first name, surname, occurrence number). For each matched person or family, it accumulates `messages` and prints grouped result sets.

## Core functions

| Function | Role |
|----------|------|
| `person_string` | Formats person (Name.occ SURNAME) fallback to (#iper). |
| `person_link` | Wraps in HTML anchor if `-html` active. |
| `print_p_messages` / `print_f_messages` | Emit grouped difference lines. |
| `dmy_to_sdn_range_l` / `compatible_sdn` | Date range compatibility logic (supports approximate, before/after, between, OR-year). |
| Name compatibility | Case-insensitive match & alias lists (`compatible_names`). |

## Options (excerpt)

| Option | Meaning |
|--------|---------|
| -html | Enable HTML link output (anchors). |
| -root <PATH> | URL root/prefix for constructing links (e.g. `http://site/`). |
| -cr <STR> | Line terminator override (default newline). |

Two positional arguments: `<base1> <base2>` (paths with or without `.gwb`).

## Usage examples

Simple diff:
```
gwdiff baseA baseB
```

HTML diff with custom root path (embedding links opening in targets base1/base2 frames):
```
gwdiff -html -root http://localhost:2317/ baseA baseB > diff.html
```

Custom CR (carriage return) for Windows-friendly output:
```
gwdiff -cr "\r\n" baseA baseB > diff.txt
```

## Interpreting ambiguous results

Messages like `Children` or `Spouses` indicate that automated matching couldn’t establish a one-to-one mapping (e.g., duplicate names, missing occurrences). Manual inspection needed; consider exporting `.gw` and reconciling before re‑running.

## Performance considerations

Loads required arrays (persons, families) from both bases; complexity grows with number of families, but matching attempts to short-circuit once all comparable fields processed.

## Related

- `connex` for branch pruning (run before diff to remove noisy isolates).
- `gwfixbase` to repair inconsistencies first, reducing false positives in diff.

