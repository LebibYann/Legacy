# setup – Web-based configuration and maintenance wizard

`setup` is an HTTP CGI-style helper launched by `gwd` (when `-setup_link` enabled) to provide interactive administrative tasks via a browser. It generates HTML pages (localized) that allow:

- Creating a new database (base name, initial wizard/friend passwords).
- Importing data: GEDCOM (`ged2gwb`), GeneWeb text (.gw via `gwc`), merging multiple sources.
- Launching maintenance utilities (`gwfixbase`, `consang`, `connex`, `cache_files`, `update_nldb`, `gwgc`).
- Adjusting configuration parameters: languages, lexicon additions, display defaults.
- Generating command line equivalents (shows reproducible commands assembled from form state).

The code (`setup.ml` ~2000 LOC) acts as a mini framework: parses query parameters, constructs environment lists, manipulates them (add/remove flags), and prints templated HTML with status messages.

## Architecture overview

Key elements:

| Component | Role |
|-----------|------|
| `printer_conf` | Output configuration mapping to HTTP primitives. |
| Environment list `(string * string) list` | Stores form field key/value pairs representing pending command options. |
| Lexicon hashtable | Localization strings loaded per selected language (with fallback). |
| Parameter builders (`parameters`, `parameters_1/2/3`) | Assemble command lines for different tools (gwc, connex, gwdiff, etc.) based on submitted fields. |
| Page rendering helpers (`header`, `trailer`, `header_no_page_title`) | Standard layout with version footer and logo. |
| Utility functions (`strip_spaces`, `create_env`, `list_replace`, `selected`) | Parse & mutate environment safely. |
| Security filters | Only whitelisted option keys accepted; suspicious values sanitized (e.g. quoted). |

## Request flow

1. Read QUERY_STRING / POST body (depending on invocation) into environment list of key/value pairs (already URL-decoded via `decode`).
2. Determine action (e.g., build command, run import) from presence of specific keys (like `opt`, `anon`, form button names).
3. Compose command line string using one of the `parameters_*` functions depending on selected tool.
4. If execution requested, spawn the underlying command (e.g., `gwc`) capturing output; else present a preview page with clickable command examples.
5. Render localized HTML wrapping results, forms for subsequent actions.

## Parameter builder strategies

Different tools require slightly different key interpretations (e.g., sequence of numbered args, multi-valued flags). The builders:

- `parameters`: generic (e.g., for `gwc`), supports numbered repetition using a trailing digit and quoting strings.
- `parameters_1`: specialized for `connex` (branch analysis) building `-gwd_p`, `-del`, `-cnt` etc., handling output file redirection.
- `parameters_2`: used for diff or multi-base operations (e.g., `gwdiff`) mapping `anon1`, `anon2`, etc.
- `parameters_3`: simpler flags toggle builder (e.g., for `cache_files`, `consang`).

The environment uses suffix conventions (e.g., `_` for position, `1` for numbered sequences) to detect multi occurrence form inputs.

## Language & lexicon

Loads selected language lexicon plus fallback tokens; unknown terms displayed in brackets `[token]`. `lang_param` key influences the `lang` field of config; `alias_lang` logic reused from `gwd` (via common modules) to fallback to base language variants.

## Generated command examples

Displayed to help admins replicate an operation from shell. Example built string:
```
gwc -o family -sep source1.gw -bnotes merge source2.gw
```

## File & path handling

`slashify` / `slashify_linux_dos` normalize paths between Windows and Unix. For security reasons untrusted inputs are quoted and sanitized.

## Safety / Security considerations

- Ensure `setup` exposure is restricted (only enable `-setup_link` behind authentication) because it can launch write operations.
- Options not recognized are ignored; no raw shell injection (arguments are individually quoted via `stringify`). Still, treat base path & user uploads carefully.
- After running import/maintenance tasks, data integrity should be validated with `gwfixbase` (already accessible through UI).

## Typical workflow

1. Enable setup link when starting `gwd`: `gwd -setup_link ...`
2. Visit `http://server:port/setup` (actual path may include prefix) as wizard user.
3. Fill create/import form (upload GEDCOM or reference `.gw` sources on server file system).
4. Click “Preview command” to inspect CLI equivalent, then “Run”.
5. After completion, follow wizard-suggested actions (compute consanguinity, generate caches, rebuild notes links).

## Related binaries orchestrated

- `gwc` (compile/import)
- `ged2gwb` (GEDCOM import path through gwc wrappers) – sometimes direct call.
- `gwfixbase`, `consang`, `cache_files`, `update_nldb`, `connex`, `gwdiff`

## Limitations

- Does not expose every low-level option of underlying tools (keeps UI manageable).
- Long-running tasks are synchronous; for very large bases prefer CLI scripts.

---

For deeper internals refer to comments within `setup.ml` where environment keys correspond to form field names.

