# Chemical identification and measurement review

Source review began 2026-10-01; the terrequinone A label and final validation were completed on 2026-10-02. The filename retains the original review date. Requested execution route: `gpt-6-astra`, reasoning `medium`. No serving receipt is available to confirm the actual model or effort.

This record covers exactly the 16 entries marked `inventory_only_not_re_adjudicated` in the dated review index. The accompanying TSV records workbook identity, physical row, source chemical tier, visually checked figure locator, evidence route, and unresolved measurement questions. Every row has `review_stage=measurement_only_not_biological_adjudication`. No admission decision is made here.

The original publisher workbook was read directly, using its `row ID` values rather than worksheet positions as feature identifiers. All 16 targets were found once. Their names, physical rows, mass values, and retention-time values agreed with the processed feature export. The workbook is the authority for this check; the export is a crosscheck.

The supplement's image panels were rendered and read visually on actual PDF pages 20 through 26, corresponding to printed pages 19 through 25. Text extraction alone omits their labels. Panel ordinals in the TSV count from the top of the specified page; Figure 2 uses its printed panel letters.

## Findings that affect interpretation

The visually checked Figure 1 labels comprise four Type I, four Type II, three Type III, and five Type IV entries. These are counts of reviewed measurement records, not independent experimental queries or accepted labels. The caption defines Types I and II as authenticated-standard routes through in-house resources, Type III as comparison with public experimental spectra, and Type IV as putative in-silico assignments. A drawn structure beside a spectrum does not establish unique structure or stereochemistry.

Roquefortine C and D are labeled **Type III** in Figure 1 on actual PDF page 23, panels 2 and 3. Both are **IV** in the existing inventory. The TSV preserves the inventory tier separately from the verified panel label. This review does not resolve the discrepancy by choosing a more favorable tier.

Terrequinone A on that page, panel 5, reads **Type IV Dereplication**. A higher-resolution crop confirmed the label on 2026-10-02. The final TSV records IV; an earlier working interpretation that the panel lacked a label was incorrect.

Two workbook names need separate treatment:

- Feature 9213, physical row 9221, is `notoamide` in the workbook. Figure 1 names notoamide B, and Figure 2h shows a paired standard/extract comparison for that name. The generic workbook string is preserved; the figure does not by itself resolve the workbook's congener specificity.
- Feature 4182, physical row 4190, is `notoamide E4` in the workbook and inventory. Figures 1 and 2i name notoamide E. E4 has not been declared a synonym of E. An explicit source annotation is needed to settle that difference.

Feature 1701 uses `tryprostatin b` in the workbook and `tryprostatin B` elsewhere. This is a capitalization difference, distinct from the congener questions above.

Figure 2 provides paired standard/extract spectra for four names in this review: meleagrin (2a), alternariol (2c), notoamide B (2h), and notoamide E (2i). Other reviewed panels show representative spectra and their source tier. The Type II route should not be rewritten as though a paired standard trace had been displayed for each entry here.

## What the record establishes

The workbook establishes an exact target ID, name string, and physical row. The figures establish what chemical-identification evidence the publisher presents for a product name. Their displayed panels do not print the workbook feature IDs or native scan identifiers. Name and mass agreement alone is not a scan-level join, and this review did not manufacture one.

A historical feature-only target join can still be supported by an explicit published target table and the named workbook feature. Recovering scan identifiers is a follow-up for spectral reproducibility and method readiness, not a new universal requirement for feature-only label eligibility. The `next_measurement_evidence` field states this distinction. Exact-congener ambiguity remains a chemical-resolution question even when a feature is traceable.

The specific follow-ups are existing annotation records that explain the two name differences, the source records that reconcile the roquefortine tiers, and the original spectral-match records where reproducible spectral inputs are needed. Type IV assignments remain putative; this review does not promote them through plausible mass or fragment agreement.

## Sources and checks

The publisher source is the Caesar et al. supplement accompanying [the 2023 article](https://www.nature.com/articles/s41589-023-01276-8). Local source files used:

- `data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx`, Sheet1; SHA-256 `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb`.
- `data/raw/sources/metadata/caesar-supplement-cdn`, Supplementary Figures 1 and 2; SHA-256 `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108`.
- `data/curated/evidence-review-index-2026-10-01.tsv` selects the 16 rows; `data/curated/source-association-inventory.tsv` supplies the retained inventory tier and product string.
- `data/processed/caesar-feature-source-v1/features.tsv` supplies the independent file-format crosscheck, not an independent scientific validation.

Final checks confirm 16 unique source relationships, 16 unique feature IDs, exact membership in the inventory-only subset, physical workbook rows, unchanged source names, and the required review-stage value. The scratch reader and rendered images remain under ignored `data/interim/remaining-measurement-review/`. This was one bounded source review by an automated curator, not an independent chemical validation.
