# update_nldb – Notes Links DataBase (NLDB) updater

Scans all note sources in a GeneWeb database (global base notes, wizard notes, misc notes directory, individual / family / event notes) to extract internal links to other persons or note pages, updating an auxiliary link index (NLDB) and a cache of link frequencies.

Used to accelerate features like backlink navigation, counting references to individuals from notes, or listing pages referencing a person.

## Process overview

1. Determine base directory (`bdir`) ensuring `.gwb` suffix.
2. Enumerate note sources:
	- Base notes (`Driver.base_notes_read base ""`).
	- Wizard notes directory (`wiznotes` under base) – each `*.txt` file.
	- Misc notes: recursive traversal of `notes` directory; nested directories produce hierarchical page names joined by `NotesLinks.char_dir_sep`.
	- Individual notes: loops every person gathering: main notes, occupation, birth/baptism/death/burial notes & sources, person events notes/sources, title notes.
	- Family notes: for each family marriage/divorce events notes/sources.
3. For each textual blob run `notes_links` which calls `NotesLinks.misc_notes_link` incrementally scanning for tokens:
	- Page links (`WLpage`): add page reference.
	- Person links (`WLperson`): record (key, position) and update frequency counter.
	- Wizard links (`WLwizard`) and other neutral tokens.
4. Build an in-memory list `db` of page entries (`NLDB.PgNotes`, `PgWizard wizid`, `PgMisc path`, `PgPerson iper ...` etc.) using `NotesLinks.add_in_db` deduplicating.
5. Maintain / increment `cache_linked_pages` hashtable counting occurrences per person key; later serialized into `notes/cache_linked_pages_name` via `save_cache_linked_pages`.

## Options

| Option | Meaning |
|--------|---------|
| -bd <DIR> | Base directory (root where bases reside). |
| -debug | Verbose debugging (prints persons as processed). |

Positional argument: base path/name.

## Output

Progress printed to stderr with section headers:
```
--- database notes
--- wizard notes
<wizid>...
--- misc notes
path/to/page...
--- individual notes
--- family notes
```

Errors in reading individual files produce warnings; processing continues.

## Internal structures

| Structure | Purpose |
|-----------|---------|
| `cache_linked_pages_t` | Hashtbl (person key -> occurrence count). |
| `NotesLinks.WL*` variants | Token classification for link extraction. |
| `NLDB.lnTxt` / `lnPos` | Captured snippet text + position index within page. |

## Performance tips

- For large bases disable debug for speed.
- Run after bulk note imports or wiki edits to refresh link counts.

## Related tools

- `cache_files` – different cache (names/places) not overlapping with NLDB.
- `gwd` – uses NLDB for note link expansion in UI (backlinks, related persons).

