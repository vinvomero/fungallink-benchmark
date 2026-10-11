# Remaining chemical admission dispositions

Reviewed 2026-10-02. Eight of the fifteen remaining detailed candidates have enough published chemical evidence and an exact historical feature join to close this bounded feature-only chemistry review. Seven exact-product gates remain open: six have insufficient reviewed identification evidence, and one has an unresolved E4/E name bridge. No biological label is admitted. These counts describe relationships, not independent pathways or eligible queries.

The companion [TSV](../../data/curated/remaining-chemical-admission-2026-10-02.tsv) retains all fifteen source relationship and feature IDs. It excludes the original acetylaszonalenin, emericellamide A, and pestalamide B cases and the eight measurement-only records. The canonical [plan](../plans/2026-09-30-2052-benchmark-paper-plan.md) and [contract](../../protocol/benchmark-contract.md) remain unchanged: the objective is a comparative measured-feature benchmark and paper.

## Decisions

`sufficient_for_feature_only` means the existing evidence supports the source-named historical feature at its recorded chemical resolution. It is an automated curator disposition, not chemical signoff or final admission. It does not establish additional stereochemical, isotope, or structural precision.

| Relationship | Product | Feature | Decision | Reason |
| --- | --- | --- | --- | --- |
| 4 | tryprostatin B | 1701 | insufficient_exact_product | Capitalization is harmless; the reviewed computational fragment assignment does not establish an exact structure or stereochemistry. |
| 7 | emericellamide B | 5402 | sufficient_for_feature_only | B has its own Type II panel and an exact named workbook target. Chemistry does not depend on transferring A's evidence. |
| 8 | monacolin K | 1633 | insufficient_exact_product | The public-spectrum annotation remains plausible, but the library record and match evidence needed to judge exact identity are absent from the reviewed material. |
| 9 | 6-O-desmethyldechlorogriseofulvin | 6346 | sufficient_for_feature_only | The exact named target and Type I panel support source chemistry. Mapping this positional structure to a separate experimental reference remains a different question. |
| 10 | 6-O-desmethylgriseofulvin | 2824 | sufficient_for_feature_only | The exact named target and Type I panel support source chemistry; no reference-compound numbering equivalence is inferred. |
| 12 | epidechlorgriseofulvin | 208 | sufficient_for_feature_only | Table 4 explicitly links the source name to feature 208, the workbook agrees, and the Type I panel names Epidechlorogriseofulvin. The spelling variation does not establish a competing identity. No external stereochemical equivalence is assigned. |
| 13 | griseofulvin | 2854 | sufficient_for_feature_only | Exact named target, Type I panel, and the previously reviewed standard/extract comparison support source chemistry. |
| 14 | mycophenolic acid | 128 | insufficient_exact_product | The named public-spectrum match lacks its original match record for an exact-identity judgment. The tentative annotation is not declared wrong. |
| 19 | chrysogine | 5496 | insufficient_exact_product | The historical feature has only the reviewed putative computational assignment; reference-product identity does not authenticate this measurement. |
| 20 | notoamide A | 1673 | insufficient_exact_product | The putative assignment lacks reviewed evidence distinguishing the exact congener and stereochemical claim. B's standard does not settle A. |
| 21 | notoamide B | 9213 | sufficient_for_feature_only | Table 4 explicitly associates B with feature 9213. That ID joins the workbook row named notoamide; the Type I B panel and previously reviewed Figure 2h support the source-named congener. No enantiomer is assigned. |
| 22 | notoamide E4 | 4182 | unresolved_name_bridge | Table/workbook E4 and panel/standard E remain different source strings. No synonym, isotope interpretation, or footnote correction is inferred. |
| 23 | fellutamide B | 1764 | sufficient_for_feature_only | Exact named target and a distinct Type II panel support the authenticated-standard evidence route. |
| 24 | terrequinone A | 1761 | insufficient_exact_product | The panel explicitly says Type IV; its computational assignment does not independently establish this historical product identity. |
| 25 | aspernidine A | 3485 | sufficient_for_feature_only | Exact named target and a distinct Type II panel support the authenticated-standard evidence route. |

The eight closed chemistry gates leave other eligibility work intact. In particular, the 6-O congeners' unresolved reference-structure mapping is not solved by their strong source chemistry, and emericellamide B's chemical identification does not establish an exact-B pathway assignment. Those questions were not re-adjudicated here.

The feature-ID bridge is decisive for notoamide B: Table 4 names both B and 9213, so the generic workbook string does not create a missing feature join. No different-feature or different-sample conflict was established in the reviewed records. Its source-named B disposition leaves enantiomer identity unspecified. Likewise, feature 208 is traceable through Table 4 and the workbook to the source Type I panel; the spelling variation alone is not evidence of a different product. Any equivalence to an external structural record or reference experimental epimer remains unestablished. These two decisions correct the initial draft, which incorrectly made more precise workbook naming or external structural normalization a condition of source-named feature eligibility. The E4/E distinction remains material and unresolved.

For the six `insufficient_exact_product` decisions, the evidence remains tentative or incomplete, not disproven. No rule that all Type III or IV annotations must fail was added. Monacolin K and mycophenolic acid need their case-specific library identification records or equivalent existing chemical evidence before this review can assess exact-product alternatives. No universal score cutoff or authenticated-standard requirement is imposed. For the four computational assignments, the reviewed material contains no independent identification of the historical feature at the exact claimed resolution. The TSV states specific evidence that would reopen each case. All seven open records remain unlabeled, never negative controls.

## What was checked in this pass

The existing dated index and its chemistry/reference packets supplied the prior appraisals. This pass freshly inspected the existing page PNGs for actual supplement pages 20 through 24 under `data/interim/host-therapeutic-review/`. Those images show the caption and each of the fifteen product panels. Panel ordinals in the TSV count from the top of the page. Figure 2d, 2h, and 2i are cited through the existing reviewed packets only; they were not freshly inspected here. No raw spectrum was independently interpreted.

The original workbook was read directly with its row-8 headers, and all fifteen requested `row ID` values were found once. Physical rows, exact name strings, m/z, and retention time agreed with the processed feature export used to populate the TSV. That export is a format crosscheck, not independent chemical validation. A fresh text read of Supplementary Table 4 confirmed the identifier associations and page locators: linkages 4 through 22 used here occur on actual PDF page 10, printed 9; linkages 23 through 25 occur on actual PDF page 11, printed 10.

The Figure 1 caption on actual PDF page 20 defines Types I and II as in-house authenticated-standard routes using MS2 patterns, retention times, m/z and/or UV data. It does not establish that every modality was used for every product. Type II pages show representative spectra, not paired standard traces for each target. The eight closures accept that published evidence route at the source-named feature resolution; they do not fabricate missing acquisition metadata.

The source table-to-workbook join uses explicit feature IDs. Panel name agreement is not a native-scan join. Historical native MS/MS membership remains unestablished for all fifteen records in this review and is a spectral-readiness issue, not a universal feature-only gate. Figure 2 and workbook retention times are not assumed to come from the same acquisition. Sample crosswalks and the candidate universe remain unfrozen.

## Source identities and review limits

Source: Caesar et al., [2023 article](https://doi.org/10.1038/s41589-023-01276-8), retained workbook and supplement. No new web research was needed for these existing records.

| Source | Recorded SHA-256 |
| --- | --- |
| `data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx` | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |
| `data/raw/sources/metadata/caesar-supplement-cdn` | `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108` |

The new TSV was checked for exact fifteen-row membership, unique relationship and feature IDs, retained source names and chemical tiers, consistent decision counts, and absence of biological admissions. Requested worker route: `gpt-6-astra` with `medium` reasoning; no serving-side receipt was available to verify the actual model and effort. This is an agent-authored evidence disposition with no scientific signoff or independent validation. No sequence analysis, new pathway mapping, method run, protocol change, correspondence, or public release was performed.
