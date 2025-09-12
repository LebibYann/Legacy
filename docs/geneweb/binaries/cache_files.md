# cache_files – Build compressed (gzip) search/autocomplete caches

Generates `.cache.gz` files (name, place, title, etc.) for faster UI autocompletion and search expansion in `gwd`. Caches are base + field specific and stored under `etc/<base>/cache/`.

## Fields / switches

| Flag | Field (internal) | Contents |
|------|------------------|----------|
| -fn | `fnames` | First names (primary). |
| -sn | `surnames` | Surnames (primary). |
| -al | `aliases` | Person aliases list. |
| -pu | `pub_names` | Public/display names. |
| -qu | `qualifiers` | Qualifiers (prefixes, nobiliary particles?). |
| -pl | `places` | All event places (birth, baptism, death, burial, marriage). |
| -fna | (modifier) | Include first name aliases. |
| -sna | (modifier) | Include surname aliases. |
| -es | `estates` | Estate places associated with titles. |
| -ti | `titles` | Title identifiers. |
| -oc | `occupations` | Occupation strings. |
| -so | `sources` | Person, events, family sources. |
| -all | (meta) | Generate all supported caches (implies alias inclusion). |
| -prog | (flag) | Show progress bars for each generated cache. |

All caches: one entry per unique string (deduplicated via `Driver.Istr.Table`).

## File naming

`<base>_<field>.cache.gz` written to `etc/<base>/cache/` (directory created if missing). The uncompressed logical name listed in summary output; each line in file is a single UTF‑8 string.

## Implementation notes

- Iterates persons/families; uses markers for progress (`ProgrBar`).
- Places: enumerates birth, baptism, death, burial (person) and marriage (family) places.
- Names gather per person then optional alias expansions depending on `-fna` / `-sna`.
- Sources includes person event sources, family event sources.
- Sorted lexicographically before writing for deterministic diffs.

## Output summary example

```
Generating cache(s) compressed with gzip
<path>/etc/base/cache/base_places.cache.gz    10234 places    1.23 s
<path>/etc/base/cache/base_fnames.cache.gz     4567 fnames    0.42 s
... Total duration: 0 min 03.10 s
```

## Usage examples

Generate all caches with progress:
```
cache_files -all -prog base
```

Only names (with aliases) and places:
```
cache_files -fn -fna -sn -sna -pl base
```

Only titles and estates:
```
cache_files -ti -es base
```

## Performance

`-all` may be I/O intensive on large bases; run after large imports or structural repairs. Regeneration not needed after pure view changes.

## Related tools

- `gwd` consumes caches for faster UI queries.
- `gwfixbase` may change names => regenerate caches.

