# Proposed shared population for five source-selected GCFs

The [population table](../../data/curated/caesar-source-gcf-population-2026-10-03.tsv) provides explicit `1`, `0`, or `unknown` membership states for the five admitted source-selected GCF queries. It proposes the same 105 source-study observation identities for every query, covering 106 existing literal-label observations and 326 acquisitions. These counts describe retained source records, not independent strains or genomes. Eleven further rows remain withheld with unknown membership states.

This is an internal input proposal under the [canonical plan](../plans/2026-09-30-2052-benchmark-paper-plan.md), [benchmark contract](../../protocol/benchmark-contract.md), and [source-observation specification](../../protocol/caesar-source-observations-2026-10-02.md). It changes no biological admission or readiness decision. The two admitted BGC queries remain separate. Requested route: `gpt-6-astra / medium`; no serving-side receipt was exposed, so actual model and effort remain unverified. Humanizer was applied.

## Coverage and zero semantics

The cached [Caesar primary manuscript](../../research_audit/Caesar-main.txt), “Correlation of metabolomics and genomics datasets,” lines 632–650, describes a GCF matrix across 110 strains. Supplementary Table 2 supplies 110 source-study rows. The retained 146-row historical crosswalk links 108 distinct display labels to 108 of those rows using an exact assembly assertion and normalized collection identifier or explicit table alias. Of those 108 rows, 107 have measurements and two carry retained identity conflicts. That leaves 105 proposed source-study observations. The [study roster](caesar-study-roster-2026-10-02.md) preserves the original labels, aliases and conflicts.

The full deposited archive contains 29 HTML family records and 81 distinct sampled display labels. Their historical mappings cover 78 study rows. Thirty other mapped study rows do not occur in any of these selected family displays; one has no measurements, and the remaining 29 belong in the proposed shared population. Restricting the denominator to the union of selected-family members would condition cohort inclusion on appearing in those selected families. The 29 family displays are not a complete reconstruction of the cohort's genomic universe.

For this source-selected proposal, `1` means that the observation's mapped source display identity belongs to the fixed deposited family roster. `0` means that the covered display identity is absent from that roster. Coverage requires the documented source-study cohort and an exact display-to-study identity bridge, not species resemblance or appearance in another selected family. These are source-index membership states, not new sequence calls or proof of biological genomic absence. In particular, a zero does not exclude another unassigned locus, an unresolved alias, or a producer outside the declared source display identity. The unallocated FMGX0070 member remains unallocated; its unknown culture is never converted into a measured negative.

The crosswalk originated from historical author-workbook material. Every table row preserves its physical crosswalk line and complete row snapshot. Public annotation namespace corroboration is recorded where present, but the crosswalk-dependent cohort coverage must not be represented as wholly public provenance. Source selection, known-reference exposure and unknown historical clustering-run details remain disclosed. This proposal is suitable for internal preparation; it does not settle public reuse rights or release approval.

| Query | Full sampled display roster | Source-membership 1 | Source-membership 0 | Unknown rows | Proposed known denominator |
|---|---:|---:|---:|---:|---:|
| NRPSPKS_85 | 9 | 7 | 98 | 11 | 105 |
| TERPENE_40 | 11 | 11 | 94 | 11 | 105 |
| NRPSLIKE_59 | 12 | 11 | 94 | 11 | 105 |
| NRPKS_18 | 10 | 10 | 95 | 11 | 105 |
| NRPS_66 | 7 | 7 | 98 | 11 | 105 |

The table contains all 110 study rows and the six nonblank workbook labels without a study-row match, giving 116 rows. Of these, 114 have measurements. Together they account for all 116 existing nonblank literal-label observations and 351 biological-sample acquisitions exactly once. Blank controls and the map-only record have no biological observation row. The coincidence between 116 table rows and 116 literal labels is not a one-to-one mapping: two study rows have no measurements, and two measured study rows each contain two spacing variants.

The withheld rows are ATCC 96836, which lacks the required display-identity bridge; W1 and ATCC MYA409, which lack workbook observations; ATCC13490 and ATCC64048, which retain source identity conflicts; and the six unmatched literals ATCC48694, Kabbage_A.brassicicola, NRRL1061, NRRL4593, NRRL4904 and NRRL66628. All five membership fields are `unknown` on these rows. The historical NRRL66628 label lacks an assembly/study-row bridge; its name alone does not establish covered cohort identity.

## The Aspni_NRRL3 pair

Use the ATCC9029 and ATCC64974 observation union at GCF-set scope without assigning individual orientations to FMGX0054 and FMGX0057. This is a proposed input decision, not a correction to the [per-member eligibility review](seven-admitted-member-eligibility-2026-10-03.md).

The two source-study rows both carry the exact Aspni_NRRL3 assembly assertion. Both display labels belong to NRPSPKS_85, and both are absent from the other four queried family rosters. Therefore either orientation gives the same vector, `(1, 0, 0, 0, 0)`, in the order used in the table above. Each culture row retains the two-label candidate set, its three acquisitions, and `unresolved_pair_orientation_not_needed_for_five_GCF_states`. Their six-acquisition union is counted once. Neither per-member mapping is marked resolved.

The cultures are not merged automatically. Their shared assembly group is retained because two measured culture records do not establish two independent genomes. The same caution applies to ATCC16872 and CBS172-66, which share the printed GCA_001890905.1 assertion, and to ATCC1007 and CBS513.65, which share an inherited assembly group across different GenBank/RefSeq assertions. The latter group is historical metadata, not a newly verified accession equivalence. The proposed denominator of 105 is a source-observation denominator; a release must retain these dependencies and cannot describe it as 105 independent genomes.

The other pestalamide conflicts are different. ATCC13490 versus ATCC13496 and A1 versus A1/83 concern the identity of the measured material, so set-level orientation invariance does not resolve them. They remain withheld. NRPSLIKE_59's FMGX0070 has no usable study identity key. Its full source member record is preserved, without guessing that it explains the twelve-member versus eleven-scored-strain difference.

## From this ledger to common numerical inputs

The next input-construction unit can use `proposed_shared_population=true` as the proposed shared column roster and the five explicit state fields as its source-membership matrix. The `unknown_mask_json` and per-query denominator fields make exclusions visible. It must carry the full family rosters and the unresolved member records alongside the matrix; extracting 105 columns does not delete members from a query definition.

For measured inputs, use each row's exact condition and acquisition IDs. The existing condition matrices already apply the declared median across acquisitions within each literal-label/medium group. Preserve those medians; do not average label-level maxima or pool all media and take a new median. The included ATCC 38873/ATCC38873 spacing pair belongs to one explicit source-study row and has disjoint recorded media. Union its condition records, then apply the source specification across conditions: maximum condition median for the height summary and any-condition detection for presence, with the existing missing-value rules. The withheld ATCC 96836 spacing pair likewise remains grouped in metadata but contributes no proposed matrix column. No numerical values were combined in this unit.

Thus a numerical build needs the retained all-candidate condition height/presence matrices, this proposed observation roster, and a manifest naming the source-selected membership semantics and assembly-dependence limits. Candidate features must remain the full declared pool. No product names, gold feature IDs, positive sets or scores enter this population table. Applying the proposal does not by itself freeze the analytical release, complete a sequence-defined BGC package, or establish native spectrum membership.

## Provenance and checks

Each population row records the study table's PDF page and row, literal source text, historical crosswalk row, existing member-eligibility row locators, public annotation namespace corroboration, and exact archive member hashes. Complete sampled rosters for all five queried families are embedded in `complete_GCF_sampled_rosters_json`; inserted references remain outside those sampled rosters. Both inherited assembly groups and exact shared assembly assertions remain visible.

The following retained files supplied the evidence. SHA-256 hashes and byte sizes for all eight are embedded in every row, allowing the table to identify its input versions without a neighboring repository:

- `data/curated/caesar-study-roster-2026-10-02.tsv`
- `data/raw/sources/caesar-2023/historical-label-strain-assembly-crosswalk-2026-09-20.tsv`
- `data/curated/seven-admitted-member-eligibility-2026-10-03.tsv`
- `data/processed/caesar-source-observations-v1/labels.tsv`
- `data/processed/caesar-source-observations-v1/conditions.tsv`
- `data/raw/sources/caesar-2023/41589_2023_1276_MOESM3_ESM.zip`
- `research_audit/Caesar-main.txt`
- `data/raw/sources/metadata/caesar-supplement-cdn`

Checks confirmed 116 unique population keys, exact coverage of all 116 literal observation IDs and 351 acquisitions, preservation of the 49 GCF member labels, agreement with the prior eligibility ledger, and 105 known observations for each query. The pair's state vector is invariant to orientation. All eight input fingerprints were recomputed, and the canonical biological ledger was unchanged. The host independently checked the row keys, denominators, state counts and eight input fingerprints. These are metadata checks, not scientific validation of culture identity.

The table's SHA-256 is `38f797694322680d5c46b79fcd50311fa5055bda2b9614ee90e2480d924b065a`. The scratch metadata builder and receipt are under `data/interim/caesar-source-gcf-population/`. No downloads, sequence extraction, method runs, comparative scores, production-code changes or release freeze were performed.
