# Chrysogine and aspernidine A evidence review

Reviewed 2026-10-01 against the canonical benchmark plan. This bounded review covers two existing Caesar inventory rows. It records proposed evidence classes, not formal label admission or human scientific signoff. It adds no independent-query count. Requested route: gpt-6-astra with medium reasoning. Dispatch was accepted, but no serving-side model/effort receipt was available.

The review used the original workbook and selected GCF archive, the actual supplementary PDF, and primary-paper evidence at the level of published evidence types. No sequences, experimental procedures, or production instructions were retrieved or developed.

## Source checks

Both IDs occur exactly once in workbook Sheet1, and each ID has the expected exact name. The independent XML check covered the complete sheet, not an assumed ID-to-row offset.

| Inventory relationship | Feature | Exact workbook name | Excel row | m/z | RT, minutes |
| --- | --- | --- | --- | --- | --- |
| caesar2023:relationship:19 | 5496 | chrysogine | 5504 | 191.0807346 | 1.109425538 |
| caesar2023:relationship:25 | 3485 | aspernidine A | 3493 | 400.2468231 | 4.344825287 |

Workbook row 1 describes a filtered measured peak-height matrix and links its acquisition filenames to MassIVE MSV000089848. A name and feature-ID match establishes the historical measured-target join. It does not independently re-identify the compound or supply a feature-to-native-MS/MS-scan join.

The caption on physical PDF page 20, printed page 19, defines Type I and II as high-confidence authenticated-standard matches through the respective in-house databases, using MS2 patterns, retention times, m/z and/or UV spectra. Type III uses public GNPS experimental spectra and is medium confidence. Type IV uses in silico matching only and is putative. Those chemical tiers are separate from biological evidence classes. The per-product image panels were also checked visually against fresh renders of the actual PDF: chrysogine on physical page 24 (printed page 23) explicitly says Type IV; aspernidine A on physical page 22 (printed page 21) explicitly says Type II. These agree with the inventory. Annotated representative spectra establish the reported identification route, not an independent re-identification or native-scan join.

## Chrysogine

Caesar inventory row 19 associates feature 5496 with NRPS_49, reference BGC0001545, source cutoff 60, and chemical tier IV. Supplementary Table 4 on physical PDF page 10 confirms the feature, product, family and reference association and reports 3/10 family-bearing strains with the metabolite.

[Wollenberg et al. (2017)](https://doi.org/10.1021/acs.jnatprod.6b00822) report genetic perturbation evidence linking the reference pathway to chrysogine in Fusarium graminearum. The primary abstract explicitly reports loss of the exact product after pathway disruption. This is experimental reference-pathway support, not merely a database prediction. Review here used the primary abstract preserved in the Europe PMC metadata response, not a full-text chemical reappraisal. The cached MIBiG page identifies the reference organism as F. graminearum PH-1, but the database is an index to the primary evidence, not its replacement.

The archive member `Supplementary Data 1/NRPS_49.html` contains BGC0001545.1 and 11 distinct sampled strain identifiers: FMGX0017, FMGX0021, FMGX0029, FMGX0059, FMGX0066, FMGX0099, FMGX0112, FMGX0120, FMGX0123, FMGX0125 and FMGX0127. It is direct evidence of source-assigned family membership. Its 11 sampled IDs do not match the source table's denominator of 10. The archive does not itself explain which member was excluded from the scoring population; this review does not invent an explanation. It also does not report quantitative sampled-locus identity/coverage or a competing-locus analysis.

Proposed class: **provisional** for the precise named-product relationship. Two distinct limits remain: the historical measured chemistry is putative, and reference-to-sampled correspondence has not been justified to the plan's locus-transfer standard. Resolving family membership alone cannot upgrade Tier IV chemistry. Reopen with published or deposited evidence that identifies feature 5496 at the claimed product resolution and resolves the scored membership census; a locus-level version also needs the planned correspondence evidence. No new wet-lab experiment or outside reviewer is required merely to reopen the record.

## Aspernidine A

Inventory row 25 associates feature 3485 with TERPENE_40, reference BGC0001722, source cutoff 70 and chemical tier II. Supplementary Table 4 on physical PDF page 11 reports the association with 2/11 family-bearing strains. The same page also reports feature 3485 with NRPKS_38 and 2/12 strains. These are overlapping source-family views of one reference pathway and one measured target; counting them as independent pathway examples would be wrong.

[Yaegashi et al. (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3713076/) provide product-specific reference evidence: proton and carbon NMR identified aspernidine A, and pathway perturbation with LC/MS readout established its cluster association. This supports aspernidine A itself. No support is inherited from another aspernidine congener. The primary full-text result was accessible through the web search index after direct PMC access returned a browser challenge; the review records only the evidence types and exact product conclusion.

The selected archive's `TERPENE_40.html` includes BGC0001722.1 and 11 sampled strain IDs: FMGX0012, FMGX0016, FMGX0031, FMGX0043, FMGX0048, FMGX0049, FMGX0050, FMGX0051, FMGX0061, FMGX0069 and FMGX0071. The FMGX0049 entry is BN001306.1.region007, which shares the reference assembly accession given in the MIBiG record for Aspergillus nidulans FGSC A4. This is affirmative assembly-level provenance for source membership, but an assembly-accession match does not by itself establish that the sampled locus and strain are the experimentally tested objects. The reference record and sampled entry are distinct objects in the archive.

`NRPKS_38.html` includes the same reference and FMGX0049 entry but contains 12 sampled strain IDs. Ten IDs overlap TERPENE_40; FMGX0023 and FMGX0078 occur only in NRPKS_38, and FMGX0016 only in TERPENE_40. The reference entry itself carries both family identifiers. The source family name TERPENE_40 therefore does not, by itself, contradict the reference pathway's polyketide classification. It also cannot justify treating every member as a proven producer.

The focused primary provenance check found that the study explicitly discusses the genome-sequenced FGSC A4 background, earlier non-detection in that background, and subsequent reference experiments in a mutant background. This supports the reference-study context. It does not supply an explicit crosswalk to Caesar's FMGX0049 historical culture. The archive places a sampled region on the same assembly as the reference, but this review has not established the plan's full sampled-locus correspondence or ruled out competing loci. That is a concrete provenance limit after inspection, not a demand for new experiments.

Proposed class: **provisional pending sampled-locus correspondence**. Strong product-specific reference evidence and source Tier II chemistry make this a reference-supported candidate if the sampled-locus link is resolved under the plan. Direct support is only a conditional future outcome if evidence establishes an experimentally represented sampled member. The current class is not direct. Query packaging must declare TERPENE_40 versus an explicitly documented alternative and must not count NRPKS_38 as an independent pathway. Reopen on an auditable strain/locus crosswalk, appropriate locus correspondence and competing-locus checks; no additional wet-lab work or external reviewer is imposed as a prerequisite.

A cached current MIBiG page also lists an unrelated inorganic-chemistry article among BGC0001722's references. That citation was not used. The usable primary reference is PMID 23706169, DOI 10.1021/ol401187b. Both cached MIBiG entries carry a questionable-quality flag and unknown completeness; the primary evidence and versioned source artifact, not that flag alone, determine the proposed classes.

## Readiness and exposure

The historical named-feature joins are verified for both rows. Method-input readiness remains separate: no frozen candidate universe, released abundance-query object, or validated historical native-scan/MS2 join was produced by this review. Spectral incompleteness is not a biological-label exclusion rule. Each feature belongs to the historical 9,339-feature measured table; that does not establish a new frozen release.

Caesar labels informed source-family threshold selection. Both records remain public-development or retrospective source-recovery examples, with MIBiG/reference exposure and source correlation disclosed. Source cutoffs 60 and 70 are provenance, not newly tuned parameters or independently validated optimal choices. Additional learned-method exposure is unknown until the method manifest is audited. Unresolved candidates remain unlabeled, never negative controls.

The bounded review is complete. Chrysogine stays outside a proposed precise-product main comparison; aspernidine A remains provisional with a reference-supported outcome possible after the stated provenance check, not an admitted row in the authoritative evidence ledger.

## Reproducible artifact identities

| Local source | SHA-256 |
| --- | --- |
| data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx | 4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb |
| data/raw/sources/caesar-2023/41589_2023_1276_MOESM3_ESM.zip | 0cef389310eccd261255e51919e7fe5f1f772cc73be2b0d42e0f5f8e30245a54 |
| data/raw/sources/metadata/caesar-supplement-cdn | 259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108 |

Primary source: [Caesar et al.](https://doi.org/10.1038/s41589-023-01276-8). Local supporting metadata: `data/interim/caesar-census-review/pmid-28708398.json`, `pmid-23706169.json`, `BGC0001545.html` and `BGC0001722.html`. Fresh PDF page renders, scratch extracts and the exact-name/unique-ID verification result are in ignored `data/interim/chrysogine-aspernidine/`. No external correspondence, publication, Git operation or authoritative label-ledger edit was made.
