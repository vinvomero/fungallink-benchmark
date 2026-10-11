# Historical inclusion count

The old 338-acquisition count can be reproduced from the retained inclusion ledger. The supplied map has 337 acquisition stems with genome accessions. One NRRL2393 rerun is absent from the workbook, leaving 336 workbook acquisitions. The historical pipeline included two more acquisitions after correcting strain labels: **337 - 1 + 2 = 338**.

Every currently mapped, accession-bearing workbook acquisition was included in that ledger. The two additions are the entire difference.

| Historical sample | Workbook column | Workbook strain | Supplied map strain | Historical resolved strain |
|---|---:|---|---|---|
| sample_0189 | 193 | NRRL13627 | NRRL 136277 | NRRL 13627 |
| sample_0320 | 324 | NRRL62501 | NRRL 60501 | NRRL 62501 |

Both supplied-map records have an empty genome accession and the resolution `no_genome_in_this_corpus`. Their historical inclusion explains a processing decision; it does not verify either strain correction. FungalLink v2 preserves the raw labels and leaves both biological identities pending review. No alias or benchmark membership was adopted from this accounting.

The source is `terralabv2`, `output/p3-custody-successor-2026-09-22/samples.parquet`, SHA-256 `68d82ae547234849cbc8c8b981f04bb2b7c10dd9e3917ad7649a731c12eedbf3`. It was read without modifying the neighboring project. The [machine-readable receipt](../../data/manifests/historical-inclusion-reconciliation.json) contains both complete historical rows, the corresponding current mapping fields, source sizes and hashes, and the excluded rerun's exact stem.

The receipt is portable. Re-extracting it requires the retained historical ledger; running the new reconciliation does not. These counts concern acquisitions, not independent strains or genomes. Vin Vomero is the research lead; no outside reviewer has adjudicated these identities.
