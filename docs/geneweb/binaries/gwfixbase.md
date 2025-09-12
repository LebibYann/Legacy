# gwfixbase – Database integrity checker / automatic repair utility

`gwfixbase` scans a GeneWeb database for structural inconsistencies and optionally applies automatic corrective patches (unless `-dry-run`). It addresses cross‑references between persons and families, parent/child linkage, witness references, marriage/divorce events coherence, duplicate unions, broken UTF‑8 sequences, inconsistent NBDS (Name/Birth/Death/Sex) data, and duplicate computed keys.

## High level flow (see `gwfixbase.ml`)

1. Parse CLI options, set verbosity & fast mode.
2. Open database via `Driver.with_database` and gather counts.
3. If no specific fix flags provided, enable the full default set.
4. For each selected check/fix category call wrapper `aux` producing progress bar and optionally detailed patch log.
5. Unless `-dry-run`, commit patches then rebuild indexes & sync.
6. Optionally dump persons list (sorted by name head) to stdout or file.

## Checks / Fix categories

Mapping from user flags to underlying `Fixbase` functions (patch constructors enumerated in code):

| Flag | Function | Purpose / Sample patch constructors |
|------|----------|-------------------------------------|
| -families-parents | `check_families_parents` | Ensure each family’s stored father/mother have matching unions referencing that family; add or fix missing parent entries. |
| -families-children | `check_families_children` | Children array matches each child’s parents; add/remove child entries. |
| -persons-parents | `check_persons_parents` | Person ascends record references an existing family; add missing ascends or clear invalid ones. |
| -persons-families | `check_persons_families` | Unions array for each person references consistent families; remove duplicate / dangling unions. |
| -persons-NBDS | `check_NBDS` | Normalize person name/birth/death/sex event coherence, fix missing union arrays; produces `Fix_NBDS` patches. |
| -pevents-witnesses | `check_pevents_witnesses` | Validate witnesses in personal events exist / are linked. |
| -fevents-witnesses | `check_fevents_witnesses` | Same for family events. |
| -marriage-divorce | `fix_marriage_divorce` | Reconcile marriage & divorce event pairs, ensure chronology, patch inconsistent flags. |
| -invalid-utf8 | `fix_utf8_sequence` | Repair invalid UTF‑8 in text fields (notes, names) replacing or updating encoded strings. |
| -person-key | `fix_key` | Recompute & update person free occurrences / duplicated keys. |

Additional patch constructors (examples):
- `Fix_AddedUnion`, `Fix_RemovedUnion`, `Fix_RemovedDuplicateUnion`
- `Fix_AddedParents`, `Fix_ParentDeleted`
- `Fix_AddedChild`
- `Fix_AddedRelatedFromPevent` / `Fix_AddedRelatedFromFevent`
- `Fix_MarriageDivorce`
- `Fix_MissingSpouse`
- `Fix_WrongUTF8Encoding`
- `Fix_UpdatedOcc`

## Options

| Option | Meaning |
|--------|---------|
| -dry-run | Do not commit changes (report only). |
| -q / -qq | Reduce verbosity (progress bars suppressed when very quiet). |
| -fast | Load persons & strings arrays for performance (higher RAM). |
| -families-parents | Enable that fix only (combine with others). |
| -families-children | Enable that fix. |
| -persons-parents | Enable. |
| -persons-families | Enable. |
| -persons-NBDS | Enable NBDS check (NB: code label mismatch: sets `p_parents` erroneously—review upstream). |
| -pevents-witnesses | Enable. |
| -fevents-witnesses | Enable. |
| -marriage-divorce | Enable marriage/divorce fix. |
| -person-key | Enable duplicate key / occ fix. |
| -invalid-utf8 | Enable UTF‑8 repair. |
| -index | Force index rebuild even if no patches. (Automatically implied by any fix.) |
| -dump | Dump person list (designation) after fixes. |
| -o <FILE> | Send dump output to file instead of stdout. |

If none of the specific fix flags are provided, the program sets all fix flags to true (full repair pass).

## Verbosity & reporting

- Verbosity >=1 prints section titles + progress bar (`ProgrBar`).
- Verbosity >=2 (default) prints each patch textual description (via `string_of_patch`).

## Exit & safety

Back up your database directory before running with patch committing. Use `-dry-run` first to review the number and types of suggested changes.

## Sample usage

Full repair with report only:
```
gwfixbase -dry-run mybase.gwb
```

Fix only family/parent relationships and UTF‑8 issues:
```
gwfixbase -families-parents -persons-parents -invalid-utf8 mybase
```

Dump list of persons after full fix:
```
gwfixbase -dump -o persons.txt base
```

Quiet reindex & marriage fix only:
```
gwfixbase -marriage-divorce -q base
```

## Related tools

- `consang` recomputes consanguinity after structural fixes.
- `cache_files` regenerate caches after significant name/title changes.

