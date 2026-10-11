# Caesar source feature export

`scripts/build_caesar_features.py` exports the publisher workbook and the reconciled sample crosswalk as portable source data. It retains every feature row, including unnamed candidates, and every acquisition column, including blanks and unmapped acquisitions. This is a prerequisite to an analytical release. Export completeness establishes neither label eligibility nor method readiness.

Install the repository requirements, then run:

```powershell
python scripts/build_caesar_features.py --workbook data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx --crosswalk data/curated/sample-crosswalk.tsv --output-dir data/processed/caesar-feature-source-v1
python -m unittest discover -s tests -p test_build_caesar_features.py -v
```

All three paths are explicit. The script uses the standard library and the existing `openpyxl` dependency. It needs no neighboring checkout or machine-specific configuration. Output paths in the manifest are relative filenames; inputs are identified by role, byte count and SHA-256, without local paths or timestamps. Rerunning unchanged inputs with the same generator and runtime produces identical output bytes. Git attributes keep the hashed generator in LF form across checkouts.

## Files and identifiers

| File | Contents |
|---|---|
| `features.tsv` | Candidate ID, worksheet name, physical source row number, and the four original metadata fields |
| `abundances.tsv` | Candidate ID followed by one column per workbook acquisition ID |
| `acquisitions.tsv` | Every crosswalk field and record, preserving mapping status, role, uncertainty and provenance |
| `manifest.json` | Input hashes and sizes, generator hash/version, Python and openpyxl versions, output hashes/counts, source layout and validation report |

The first worksheet has acquisition strain labels in row 6, growth conditions in row 7, and headers in row 8. Columns A through D are exactly `row ID`, `row m/z`, `row retention time`, and `row identity`. Features begin at row 9; acquisition abundances begin at column E. The exporter recomputes the worksheet's physical row and column extent before reading headers or features, so understated dimensions stored in the XLSX cannot truncate the export. Metadata names and scalar values are copied, with missing metadata represented by an empty field. Integral numeric values use decimal integer text. Source workbook bytes remain the authority for cell formatting and original numeric representation.

Candidate IDs are `caesar2023:feature:` followed by the UTF-8 percent-encoded source `row ID`. They depend on the source identifier, not physical row position, annotation, mass or retention time. The physical row number is retained separately. IDs must be unique and nonempty, without surrounding whitespace. The exporter preserves workbook row order.

Acquisition columns follow workbook column order. Each joins exactly one crosswalk record by worksheet, column letter, column number and header; strain and medium must also agree. The acquisition ID must match the existing SHA-256 derivation from the exact source stem. The stem must match the workbook filename stem, allowing casefold equality only for a declared `case_alias`. Duplicate or unknown IDs, repeated columns and mismatches fail. Map-only acquisitions follow the workbook acquisitions in metadata, sorted by acquisition ID. They have no invented abundance column and must have empty workbook coordinates.

Missing abundance cells remain empty TSV fields. Observed zero is written as `0`. All observed abundances must be finite, nonnegative numeric cells. Numeric strings, Boolean values, spreadsheet errors and formulas are rejected. The workbook is opened with formulas visible, so a formula without a cached result cannot silently become a missing measurement. No imputation occurs.

The source workbook already reports filtering in its introductory note. This exporter adds no filtering, thresholding, normalization, aggregation, annotation-based selection or scientific admission. It does not turn unresolved links into negatives or acquisition counts into independent sample counts. The published 9,301-feature count is recorded separately from the observed row count, with the discrepancy explicitly unresolved.

## Failure and verification

All source validation and file construction finish in a temporary sibling directory before publication. Invalid input produces no new export bundle and leaves an existing bundle untouched. Output files are replaced individually, with the manifest last; this is not a filesystem transaction. Consumers must verify manifest hashes before using a bundle after an interrupted write.

The fixture tests exercise shuffled source IDs and crosswalk order, missing versus zero abundance, retained blanks and unnamed features, map-only records, malformed joins, invalid numerical values, formulas, deterministic CLI reruns and output hashes. They check understated worksheet dimensions and declared case aliases, including acquisition ID preservation. Invalid rebuilding and changed input fingerprints must leave a previous bundle unchanged. An injected publication failure checks that the previous manifest's hashes detect a mixed bundle after one file has been replaced. Real-data execution counts belong in the separate execution receipt, rather than being inferred from these fixtures.

Replicate handling, presence rules, normalized assembly inputs, BGC/GCF universes, reviewed positive sets and release admission remain separate work. This exporter does not implement them.
