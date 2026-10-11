# Caesar source observations and presence specification

Prepared 2026-10-02 under the [canonical plan](../docs/plans/2026-09-30-2052-benchmark-paper-plan.md), [benchmark contract](benchmark-contract.md), and [analysis plan](analysis-plan.md). This is a concrete preprocessing specification for a source-retrospective, feature-only pilot. It does not freeze the genome-linked cohort, establish biological identity, or amend scientific label dispositions. No rankings or positive-set performance were used to choose these rules.

The implementation unit was dispatched with requested model `gpt-6-astra`, reasoning effort `medium`. No serving-side model/effort receipt was exposed. Humanizer was applied to the written specification.

## What the source supports

The publisher workbook, `data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx`, contains one sheet. Its introductory note describes peak heights, with strain labels in row 6, growth medium in row 7, and acquisition names in row 8. It reports prior noise filtering below 1e5, a blank-to-extract mean ratio filter above 80%, and removal of ions whose average relative standard deviation in the subset with triplicate injections exceeded 40%. These are inherited processing claims; this inspection did not independently reproduce those filters. The note supports the existence of technical injections somewhere in the dataset, not a verified culture/extraction/replicate assignment for every repeated acquisition.

The cached primary article, `research_audit/Caesar-main.txt`, section “Correlation of metabolomics and genomics datasets,” lines 632–650, describes maximum intensity across the three conditions and a detection threshold of at least 1 × 10^7. It also describes random zero replacement and a minimum-two-strain feature filter. This pilot retains the threshold and any-condition interpretation, but does not reproduce those latter steps. All 9,339 exported features remain candidates, including features below threshold everywhere. This is a declared retrospective adaptation, not an exact recreation of the published analysis. The published 9,301-feature count remains unresolved.

The workbook supplies source peak heights, not a verified normalized abundance matrix. No scaling, background subtraction, new blank filter, or normalization is introduced here. The global normalized-abundance baseline remains unavailable until a justified normalization is specified. Presence-based controls do not require an invented normalization.

## Observation ledger

[caesar-observation-groups-2026-10-02.tsv](../data/curated/caesar-observation-groups-2026-10-02.tsv) partitions every crosswalk acquisition exactly once. Each measured row uses the exact pair `(workbook_strain, workbook_medium)`. No trimming, spacing repair, capitalization repair, collection-code inference, or source-map alias replaces that pair. The composite key is a source observation group, not a biological strain ID.

Array-valued TSV fields are JSON arrays in matching acquisition order. They retain exact acquisition IDs, source stems, workbook columns, roles, join statuses, mapping statuses, raw map labels, and raw map accession assertions. A separate map-only ledger row has empty workbook label and medium, with `record_scope=map_only_no_workbook_group`; it is not an invented observation. Eligibility refers only to using a measured source group for feature preprocessing. None of these rows establishes genome-linked eligibility.

| Accounting item | Count |
|---|---:|
| Crosswalk records, each represented once | 363 |
| Workbook acquisition columns | 362 |
| Biological-sample workbook acquisitions | 351 |
| Exact biological label/medium groups | 337 |
| Literal biological workbook labels | 116 |
| Literal labels with all three media | 108 |
| Blank acquisitions in four label/medium groups | 11 |
| Map-only record without measurements | 1 |
| Total ledger rows, including exclusions | 342 |

Seven biological groups contain three acquisitions: ATCC10419/Oats, ATCC10490/Rice, ATCC16872/Cheerios, NRRL1938/Rice, NRRL4902/Rice, NRRL5920/Rice, and NRRL89/Oats. The other 330 biological groups each contain one. These are multiple acquisitions within a literal group, not demonstrated independent cultures or duplicate files. The mzML/mzXML representation pairs in the mapping already refer to one acquisition each; they never increase these counts.

Condition coverage is uneven. ATCC 38873 has Cheerios; ATCC38873 has Oats and Rice. ATCC 96836 has Cheerios and Oats; ATCC96836 has Rice. NRRL2393 has Oats and Rice; NRRL4539 has Cheerios and Rice; NRRL4593 has Oats; NRRL89 has Cheerios and Oats. Spelling similarity does not authorize merging those labels. In particular, 116 literals are not 116 verified strains or independent genomes.

Six workbook-only acquisitions, the three media each for ATCC48694 and NRRL1061, remain eligible for source feature preprocessing. Their missing sample-map joins still prevent an inferred genome linkage. The six source-inferred mappings for ATCC 38873/ATCC38873 and CBS 101.740 retain their uncertainty. Other exact filename joins also remain source assertions rather than verified sample identities.

The 11 blanks are retained only as control records. Five have no stated medium, and two each have Rice, Oats, and Cheerios. The map-only NRRL 2393 rerun has no workbook intensity column. Neither blanks nor that rerun contribute a biological source observation, a zero-valued measurement, or a condition opportunity. No new blank subtraction is justified by this ledger.

## Rule to implement for the retrospective pilot

For feature `f`, exact literal label `s`, and recorded medium `m`, define `H(f,s,m)` as the median of source peak heights across all workbook acquisitions in that group. A singleton is unchanged. Use the ordinary median, averaging the two middle values if a later source version has an even group size. This median is an operational aggregation choice consistent with the contract's proposed replicate handling; it does not assert that those acquisitions share a verified extraction or culture. Keep group sizes visible.

Set condition presence to `1` when `H >= 10000000`, otherwise `0`. Equality is included. Do not call the resulting `0` a proven biological absence: it means the source signal did not meet this detection rule. Measured zeros remain measured zeros.

For the source label summary, take the maximum of `H` over that literal label's recorded media. Label-level presence is any condition present. Each literal label contributes at most one descriptive presence observation, and media do not add independent genomic observations. The condition-level table remains available. The maximum is an unnormalized source-height summary and cannot be passed off as the analysis plan's normalized-abundance control.

Missing values must stay explicit. If a group has any missing acquisition value for a feature, its median and condition presence are missing; do not silently change the acquisition denominator. Label presence is `1` if any condition is detected, `0` if every recorded condition is observed and below threshold, and missing otherwise. A medium absent from the recorded roster is unmeasured, not zero; the primary retrospective summary describes the sampled conditions only. This bundle has no missing abundance cells, so the missing-value rule does not alter its present values. If a later version introduces missing values, a complete-ranking workflow needs an explicit input-eligibility or fallback amendment before scoring.

Predeclare two checks on aggregation without selecting a variant on retrieval performance: restrict descriptive coverage to the 108 literal labels with all three media for equal recorded condition opportunity; and compare median-within-group detection with any-acquisition detection for the seven repeated groups. The latter changes opportunity and is a sensitivity, not permission to choose whichever rule gives stronger recoveries. Both retain all 9,339 candidates. Neither resolves biological identity or establishes an independent-strain denominator.

## Decisions and remaining limits

Preserving all candidates, retaining zeros, refusing zero imputation, separating blanks and map-only records, and keeping unresolved identities out of asserted genome-linked comparisons follow the existing contract. Exact literal grouping, explicit exclusions, and inclusive threshold application are routine source rules. The median is a stated pilot analysis choice rather than a discovered replicate hierarchy. These choices can be prepared and checked before label review.

Scientific release approval still needs an attributed sample/genome roster and decisions about biological aliases, culture/replicate identity, and the applicability of this retrospective aggregation to that roster. Any altered detection or blank rule must be justified from source/QC evidence before comparative ranks are seen. A normalized-abundance workflow requires its own justified preprocessing. Scientific query-label signoff is a separate decision and does not settle these method-input requirements. This document neither grants nor reverses label approvals recorded elsewhere.

Until the roster is supported, label-level prevalence is a descriptive source statistic. The ledger alone cannot supply genome presence, absence, Metcalf inputs, or a headline sample count. The benchmark objective remains a comparative genome-to-measured-feature evaluation; this preparation makes one input layer concrete.

## Checks and fingerprints

The bounded check on 2026-10-02 verified every exported file against the existing bundle manifest and confirmed that exported acquisition metadata is byte-identical to the crosswalk. The abundance file has 9,339 unique candidate IDs and 362 distinct acquisition columns, matching the measured crosswalk records. All 3,380,718 cells are finite nonnegative numbers: 2,415,267 are observed zero, none are missing, and 240 equal exactly 10,000,000. The threshold boundary therefore matters. Every acquisition appears once in the ledger, and its measured-column counts sum to 362. These are source integrity checks, not scientific validation.

| Artifact | SHA-256 |
|---|---|
| Publisher workbook | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |
| Sample crosswalk / exported acquisitions | `69553d85647cc92784ebf49db50da46098da976b44c2bcf3edd15f286b2db79e` |
| Source export manifest | `53e74e1f5161ec7af038a5a9e8adbc033cc245db6b5e6625272c6258053eae15` |
| Cached primary article text | `32d5a1ce1ee07821af0fa5e385152f7fc0363341077feecdc72e6b6f7d17d86b` |
| Observation ledger | `70c74e3b0dbdcd5a1cc5dcd81bed59cb301036b0c7b109740bc9301cb2266e0c` |

The article citation and source provenance remain in the existing source registry and research audit. The ignored local check receipt is `data/interim/source-observation-spec/checks.json`; the counts and fingerprints above preserve its conclusions in this tracked specification. No reusable implementation, scores, rankings, new downloads, or changes to source inputs were made in this unit.
