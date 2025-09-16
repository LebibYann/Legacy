# NLDB (Notes Links Database)

Documentation of the auxiliary link index built by `update_nldb` to accelerate note/person linkage features.

## Purpose

Provide efficient reverse lookup:
- Which pages link to a given person key?
- What person links are embedded in a note page?
- Frequency of references (for relevance ranking / badges).

## Source Inputs

1. Base (global) notes (`notes/` root pages).
2. Wizard notes (`wiznotes/`).
3. Misc nested notes under `notes/` subdirectories (hierarchical path).
4. Person-scoped notes: main notes field, occupation notes, event notes (birth, baptism, death, burial), title notes.
5. Family event notes: marriage/divorce events.
6. Event and person/family sources (if textual links allowed).

## Tokenization

`notes_links` scans text producing tokens (variants in `NotesLinks`):
- `WLperson key` — person key link.
- `WLpage page_path` — internal page link.
- `WLwizard wizid` — wizard page reference.
- Other tokens ignored for NLDB.

Simple pattern matching (custom parser) rather than full markdown/HTML parsing, relying on GeneWeb's note link syntax.

## Data Model (Conceptual)

| Entity | Fields | Notes |
|--------|--------|-------|
| PageEntry | page_id (stable string), kind (Notes|Wizard|Misc|Person|Family), person_if_any, family_if_any | Distinguish origin for filtering. |
| Link | page_id, target_person_key, snippet (optional), position | Position = occurrence index in page text. |
| FrequencyCache | person_key → integer count | Sum of all link occurrences across pages. |

Serialized format is legacy custom (not JSON); loaded by scanning file(s) when `update_nldb` runs.

## Files Produced

| Path | Content |
|------|---------|
| `notes/cache_linked_pages_name` | Serialized frequency hashtable (person key → count). |
| (internal DB structure) | In-memory only; rebuilt on each `update_nldb` run. |

## Invalidation Rules

Run `update_nldb` after:
- Editing any note page under `notes/` or `wiznotes/`.
- Import adding/modifying notes (GEDCOM, .gw import).
- Running `gwfixbase` if it changes keys (occ adjustments) — must recompute because person keys changed.

## Performance Characteristics

- Linear scan over all notes & persons/families.
- Token extraction per note: O(L) where L = text length.
- Memory dominated by accumulating link occurrences before writing frequency cache.

## Potential Enhancements

| Idea | Benefit | Complexity |
|------|---------|------------|
| Incremental update (track modified timestamps) | Faster on small edits | Medium (need per-page metadata) |
| Persistent page→links index (serialized) | Avoid full rebuild | Medium/High |
| Rich parser supporting nested markup | More accurate link detection | High |
| Ranking using TF-IDF style weighting | Improved relevance ordering | Medium |

## Troubleshooting

| Issue | Cause | Remedy |
|-------|-------|--------|
| Zero references for known person | NLDB stale | Run `update_nldb`.
| References count seems low | Duplicate pages overwritten or skipped | Verify page unique IDs; check note syntax. |
| New note not counted | Saved in wrong directory or naming mismatch | Ensure under `notes/` or `wiznotes/` and properly linked. |

## Interaction with Caches

Independent of `cache_files` (autocomplete). Both may be run in any order after imports, but run NLDB last if keys possibly changed.

See also: `formats/overview.md`, `binaries/update_nldb.md`.
