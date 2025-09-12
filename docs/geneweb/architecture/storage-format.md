# Storage Format (Legacy .gwb)

Deep dive into the on-disk representation of a GeneWeb database directory (`<base>.gwb`). This is reverse-engineered overview; refer to source for absolute truth.

## Directory Skeleton

```
<base>.gwb/
  persons/        (person array segments or flat file in older layouts)
  families/
  ascends/
  descends/
  unions/
  couples/
  strings/        (interned strings pool)
  etc/            (*.gwf config, lexicons, particles)
  notes/          (public note pages)
  wiznotes/       (wizard-only note pages)
  images/         (binary media)
  cache/          (*_*.cache.gz autocomplete/search caches)
  cnt/            (counters, gwd_private.txt secret)
```

Some historical versions use flat files (`persons.gw?`) instead of subdirectories. The `Driver` abstracts this; tools should avoid assuming exact filenames.

## Core Arrays

| Logical Array | Purpose | Access Pattern |
|---------------|---------|----------------|
| persons | Fixed-length person records storing indices into `strings` and relation arrays. | Random by index (iper). |
| families | Family records (father, mother ipers; child list offsets). | Random by index (ifam). |
| ascends | Parent family reference for each person (or sentinel). | Single lookup. |
| unions | For each person, list of family ids where person is spouse. | Iteration for traversal. |
| descends | Children list per family. | Iteration. |
| couples | Normalized person-pair abstraction to speed certain queries. | Optional, derived. |
| strings | Pool of unique immutable strings (names, places, notes fragments). | Append & reference. |

All arrays use integer indices (0-based) referenced transitively; invariants enforced externally (repair tools).

## Record Structure (Conceptual)

A person record conceptually contains:
- Offsets/ids for: primary first name(s), surname, public name, qualifiers.
- Sex flag.
- Birth/death events: date structure (packed ints) + place string id + source id + note id.
- Occupation string id(s).
- Pointers: index into unions array, ascends entry.
- Flags: visibility/public, living status, computed consanguinity.

Family record conceptually contains:
- Father iper, mother iper (or sentinel like -1).
- Children (offset into descends/child count).
- Marriage/divorce events: date/place/source/note ids.

Exact binary layout purposely undocumented here (subject to change); rely on high-level Driver operations.

## String Pool

- De-duplicates recurring tokens (names, places, sources) reducing disk footprint.
- Garbage collection (`gwgc`) removes unreferenced strings by rebuilding or compacting (depending on implementation version).

## Locking Files

- A lock file (e.g., `gwd.lck` or similar) placed within base signals active mutation.
- Tools respect `-nolock` to bypass (unsafe). Always lock for write operations (imports, fixes, cache rebuilds).

## Caches Directory

Files named `<base>_<field>.cache.gz`. See `formats/overview.md` or `cache_files.md` for field enumeration. Regenerated as a whole or selectively; stale caches do not corrupt data but degrade search performance.

## NLDB Artifacts

Under `notes/` additional serialized structures may appear (link frequency cache). Detailed in `formats/nldb.md`.

## Secret / Counters

`cnt/gwd_private.txt` contains random secret used in HTTP digest auth nonce computation. Deleting regenerates and invalidates active sessions.

## Integrity & Repair Flow

1. Import creates base arrays.
2. `gwfixbase` patches inconsistent indices (parents/children, unions, witnesses).
3. `consang` populates inbreeding coefficients (optional).
4. `cache_files` builds search caches.
5. `update_nldb` indexes note links.

## Versioning Considerations

- Structural changes historically handled by recompiling/importing rather than live migration scripts.
- Backups should be directory-level (rsync/tar). For safe restore, ensure process not running to avoid partial writes.

## Guidelines for Tool Authors

- Use `Geneweb_db.Driver` API; do not parse binary segment files directly.
- Always lock before mutating.
- After batch mutations, call sync/commit functions once (avoid repeated partial sync).
- Run `gwfixbase -dry-run` on experimental tooling outputs to verify structural integrity.

See also: `architecture/overview.md`, `formats/overview.md`.
