# gwb2ged – GeneWeb database to GEDCOM exporter

Exports a GeneWeb database (`.gwb`) to a GEDCOM file, optionally including internal GeneWeb indexes. Uses shared selection logic from `gwexport` allowing partial exports (specific ancestors/descendants, surname filters, censorship, etc.). Final rendering is performed by `Gwb2gedLib.gwb2ged`.

## Flow

1. Parse CLI arguments building `Gwexport.gwexport_opts` (`gwexport` provides options like `-a`, `-d`, `-c`, `-key`, `-s`, `-charset`, `-nn`, `-nopicture`, etc.).
2. Additional `-indexes` flag toggles emission of GeneWeb internal index records (non standard GEDCOM extensions – for internal roundtrip / debugging).
3. Load base (`Driver.with_database`).
4. Build selection filters `select = Gwexport.select base opts []` (filters persons/families by constraints).
5. Call `Gwb2gedLib.gwb2ged base !with_indexes !opts select` to output GEDCOM text to chosen destination (stdout or `-o` file from gwexport options).

## Additional flag

| Option | Meaning |
|--------|---------|
| -indexes | Include index (xref) segments aiding later reconstruction (non standard). |

All other options are those of `gwexport` (see `gwexport.md`).

## Selection examples

Export 5 generations of ascendants of a root key:
```
gwb2ged -key "John.0 DOE" -a 5 base
```

Export descendants only (3 gens) of multiple roots, omit notes:
```
gwb2ged -key "Alice.0 SMITH" -key "Bob.0 SMITH" -d 3 -nn base
```

Censor last 100 years, restrict to surname MARTIN:
```
gwb2ged -c 100 -s MARTIN base
```

Include indexes:
```
gwb2ged -indexes base > exported.ged
```

## Charset handling

Inherits `-charset` from `gwexport` (default UTF-8). Other options toggle notes inclusion, pictures, selection by surnames, etc.

## Related

- `ged2gwb` reverse direction importer.
- `gwexport` for alternative export formats / content control.

