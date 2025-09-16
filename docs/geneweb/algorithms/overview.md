# Algorithms Overview

Summaries of key algorithms implemented in the legacy GeneWeb code base.

## 1. Selection (Ancestors / Descendants / Parentship)

Implemented primarily in `gwexport`.

- Ancestors: BFS/DFS upward via ascends (person → family → parents). Generation depth limited by `-a` or `-ad` (combined with descendant pass).
- Descendants: Layered traversal building queue from root persons' unions and children; generation limit `-d`.
- Ascendants + Descendants (`-ad`): Collect ancestors up to A, then for every collected ancestor gather D descendant generations.
- Parentship: Given pairs (childKey, ancestorKey) compute intersection: ancestors(child) ∩ descendants(ancestor). Families along connecting paths are included.
- Censorship: Markers set for persons younger than threshold (current_year - c) or visibility restricted; cascades to families and related persons.

Data structures: marker bit arrays for persons and families (int flags), BFS queues (lists / arrays). Complexity: O(V + E) for each traversal where V = persons, E = family links, bounded by generation cutoffs.

## 2. Consanguinity

In `ConsangAll.compute` (used by `consang` and optionally `gwc -cg`).

- Performs topological ordering of ancestry graph; detects cycles (raises `TopologicalSortError`).
- Inbreeding coefficient F computed using classical formula: probability alleles identical by descent via common ancestors.
- Memoization: dynamic programming over person indices; if parents unknown F=0; else combine parental contributions.
- Complexity: roughly O(n * a) where a = average number of ancestors visited.

## 3. Connectivity (Branches)

`connex` builds connected components of families in bipartite graph (persons ↔ families).

Algorithm outline:
1. For each unvisited family, BFS over: parents' other families + children's families.
2. Collect all families (and implicit persons) forming a branch; compute size.
3. Apply filters (ignore by file, size thresholds). Optional deletion iterates families removing relations.
Complexity: O(F + R) where F families, R total relation edges.

## 4. Diff (Structural)

`gwdiff` compares two bases:
- Match persons by textual key (FirstName.occ Surname). Occurrence adjustments attempt uniqueness; ambiguities flagged.
- For matched persons/families compare fields: names, dates (via `dmy_to_sdn_range_l` conversion to range of serial day numbers), places, occupation, sex, marriage/divorce status, child/spouse lists.
- Ambiguous children/spouses produce special messages (e.g., `Children`, `Spouses`).
Complexity: O(n log n) for initial indexing + linear pass; worst-case near O(n^2) only under extreme ambiguity.

## 5. Garbage Collection

`gwgc`:
- Finds unreachable persons/families/strings (strings no longer referenced) using reference counts / traversal from root arrays.
- Produces lists to delete; optionally commits.

## 6. Integrity Repair

`gwfixbase` orchestrates multiple passes:
- Parent/child consistency: ensure families and persons reciprocally reference each other.
- Missing unions: add or remove duplicates.
- Witness references: ensure witness persons exist and back-link is coherent.
- Marriage/divorce coherence: reconcile event pairs, chronological sanity.
- UTF-8 repair: scan text fields for invalid byte sequences; rewrite.
- Key fix: recompute occurrences to avoid collisions; patch keys.
Each pass yields patch constructors (applied then persisted). Complexity near linear in number of persons/families.

## 7. Notes Links Extraction (NLDB)

`update_nldb` tokenizes note text scanning for patterns referencing pages/persons (custom lightweight parser). Maintains frequency counts, outputs link index.

## 8. Cache Generation

`cache_files` gathers unique field strings (names, places, titles, occupations, sources) into sets using hash tables; sorts & gzip-compresses for deterministic, fast autocomplete.

## 9. Date Normalization

In `ged2gwb` and shared date utilities: parse GEDCOM date variations, qualifiers (ABT/BEF/AFT), ranges, about/estimated, convert to DMY and to serial day numbers for comparisons (Julian/Gregorian transitions not deeply modeled in legacy version).

## 10. Key / Occurrence Management

Person key = FirstName(s).occ SURNAME; `occ` is ordinal among persons with identical normalized first+surname tuple.
- On import/link, if collision detected increment occ until unique.
- `gwfixbase` can retroactively adjust occurrences maintaining referential stability by patching arrays (consumers rely on key strings, not ordinal iper indices).

---
See also specific deeper docs (`algorithms/consanguinity.md`, `algorithms/diffing.md`) to be added if needed.
