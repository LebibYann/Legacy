# connex – Connected components (branch) analysis & pruning tool

Analyzes genealogical connectivity within a GeneWeb database, identifying connected components of families/persons (branches) and providing statistics, optional HTML/wiki styled output, and interactive deletion of small isolated branches.

## Core concepts

Connectivity is computed over the bipartite graph (persons ↔ families). For a given family id `ifam`, the set of connected families includes:
- The family itself.
- Families sharing spouses/parents through father/mother lines.
- Families reachable via children (their unions) recursively.

Functions:
- `connected_families base ifam cpl`: BFS/DFS building list of families reachable from the union (father+mother) ignoring duplicates.
- `neighbourgs base ifam`: extends connectivity by including parents' families and children's families.
- Aggregation of branch size, printing and optional deletion.

Deletion logic (when prompted) removes unions and resets parent links for involved persons (`effective_del`).

## Options

| Option | Arg | Meaning |
|--------|-----|---------|
| -gwd_p | <PORT> | Port for generating HTML links to gwd (default 2317). |
| -server | <HOST> | Host for generated links (default 127.0.0.1). |
| -a | (flag) | Show all components (not only min-sized). |
| -s | (flag) | Produce statistics summary of component sizes. |
| -d | <INT> | Detailed listing for components of this exact size (prints every family). |
| -i | <FILE> | Ignore components whose origin file equals FILE (repeatable). |
| -bf | (flag) | Group by origin families files (override `ignore_files`). |
| -del | <INT> | Ask for deleting branches of size <= N (interactive confirmations). |
| -cnt | <INT> | Auto-delete up to CNT branches meeting `-del` criterion without per-branch prompt (first CNT positive confirmations). |
| -exact | (flag) | With `-del`, only size == N (not <=). |
| -o | <FILE> | Also echo plain text branch listings to FILE (stderr duplication). |

The mandatory positional argument is the base path/name.

## Output styles

Without `-o` output is HTML-like wiki markup (using double bracket links). With `-o`, concise plain text is also sent to stderr (facilitating script parsing) while stdout retains HTML/wiki.

Each printed component shows: origin file name and branch size; if detailed or first family, lists father/mother pairs and optionally links to gwd person pages.

## Deletion algorithm

When `-del N` specified, after computing a branch size `nb` that matches condition (<= N or == N with `-exact`):
1. If `-cnt` still positive: auto-confirm; else prompt user `Delete that branch (y/N)?`.
2. On confirmation, iterate families; for each remove children parent links and unions: `kill_family`, `kill_parents`, `Driver.delete_family`.
3. Commit patches at end (`Driver.commit_patches`).

## Examples

List statistics only:
```
connex -s base.gwb
```

Show all components <= minimum size (default behavior shows smallest sizes):
```
connex -a base
```

Interactive pruning of very small branches (size <= 3):
```
connex -del 3 base
```

Automatically delete first 10 branches of size exactly 2:
```
connex -del 2 -exact -cnt 10 base
```

Ignore imported file segments from `import2.txt` and `legacy.txt`:
```
connex -i import2.txt -i legacy.txt base
```

## Safety notes

Deletion is destructive; ensure you have backups or run under VCS. After deletions, run `gwfixbase` and optionally `cache_files` to rebuild derived structures.

## Related tools

- `gwfixbase` for integrity repair after pruning.
- `gwc` for initial creation (connectedness often reflects source segmentation).

