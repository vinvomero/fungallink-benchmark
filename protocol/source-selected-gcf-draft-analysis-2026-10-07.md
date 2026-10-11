# Proposed analysis of the source-selected GCF draft

Prepared 7 October 2026 under the [canonical plan](../docs/plans/2026-09-30-2052-benchmark-paper-plan.md), [benchmark contract](benchmark-contract.md) and [analysis plan](analysis-plan.md). Status: proposed, not frozen or authorized for scoring. This note records existing sensitivity rosters and the decisions needed to use them. It changes no biological admission, numerical input or existing protocol.

Requested implementation route: `gpt-6-astra / medium`. No serving-side model/effort receipt was available to this unit; actual service is unverified. The humanizer skill was applied.

The canonical plan permits a source-selected retrospective comparison as part of the reusable benchmark. Its interpretation must be stated before scoring: retrieval using deposited family membership and measured source observations. It cannot silently replace the core contract's stronger genomic-presence semantics or a reconstructed-family release. Evidence strength, biological admission and method-input readiness remain separate decisions.

The [numerical draft](../docs/data/source-gcf-inputs.md) contains 9,339 candidates and five GCF queries, with six admitted GCF-product relationships. Pestalamides A and B belong to one `source:NRPSPKS_85` query. The [evaluator-side pool receipt](../data/interim/source-gcf-host-expected/gold-pool-audit.json) records all six targets inside the candidate pool. The two admitted BGC relationships belong to their separate track; the combined eight relationships and seven queries are not this analysis's denominator. Five GCF identifiers also do not establish five independent pathway groups.

## What the existing rosters vary

The [population ledger](../data/curated/caesar-source-gcf-population-2026-10-03.tsv) contains 116 rows: 105 proposed shared source-study observations and 11 withheld rows. The [sensitivity table](../data/curated/caesar-source-gcf-sensitivity-rosters-2026-10-03.tsv) contains 18 proposed rosters, totaling 1,815 rows. Every entry is marked `proposed_not_frozen`.

| Existing roster IDs | Number of rosters | Observations per roster | Proposed use |
|---|---:|---:|---|
| `draft_all_source_observations` | 1 | 105 | Full source-observation reference analysis |
| `draft_three_media_only` | 1 | 102 | Restrict to recorded Cheerios, Oats and Rice coverage |
| `draft_assembly_representative_01` through `_08` | 8 | 102 | Each choice of one observation from each of three dependency pairs |
| The same eight IDs with `_three_media` appended | 8 | 99 | Intersect each representative roster with complete three-media coverage |

The three-media roster excludes `source-study:caesar-table2-008` (NRRL 4539; Cheerios/Rice), `-065` (NRRL 2393; Oats/Rice) and `-073` (NRRL 89, ATCC 10065; Cheerios/Oats). These exclusions equalize recorded medium coverage only. They do not establish equal culture replication or measurement quality.

The [dependence census](../data/interim/source-gcf-host-expected/dependence-census.json) identifies these pairs from retained metadata:

| Dependency group | Source-study row suffixes | Culture labels | Assembly assertions |
|---|---|---|---|
| `acc:Aspni_NRRL3` | 043, 046 | ATCC 9029; ATCC 64974 | Both `Aspni_NRRL3` |
| `asm:000002715` | 020, 021 | ATCC 1007; CBS 513.65 | `GCF_000002715.2`; `GCA_000002715.1` |
| `asm:001890905` | 005, 006 | ATCC 16872; CBS 172-66 | Both `GCA_001890905.1` |

All five membership states agree within each pair. In query order NRPSPKS_85, TERPENE_40, NRPSLIKE_59, NRPKS_18 and NRPS_66, the Aspni pair has `(1,0,0,0,0)` and the other pairs have `(0,0,0,0,0)`. Aspni's display-label orientation remains unresolved. The GenBank/RefSeq grouping is inherited metadata, not a newly verified accession equivalence.

The eight representative choices enumerate all `2^3` ways to retain one row per pair. Their purpose is to expose sensitivity to those retained observations, whose measured profiles can differ despite matching membership vectors. Keep the original culture and condition records. Neither choosing representatives nor subtracting three rows proves 102 independent genomes, resolves culture identity or removes every possible dependency.

If adopted, report all 18 analyses with their roster IDs and denominators, including unavailable outputs. Show each of the eight representative choices and their range; don't choose the best retrieval result as the primary analysis. These are overlapping sensitivity analyses, not 18 independent experiments. The proposed full-roster reference analysis still needs an attributed observation-policy decision.

## Membership and measurement meaning

A source membership `1` means that the mapped source display identity appears in the fixed deposited GCF roster. A `0` means covered nonmembership in that roster. The [population proposal](../docs/data/caesar-source-gcf-population-2026-10-03.md) documents cohort coverage and the display-to-study bridge. It does not establish biological genomic absence, rule out another locus, or reconstruct a complete BGC/GCF universe. The eleven withheld rows retain unknown membership; the unallocated NRPSLIKE_59 member FMGX0070 remains unresolved.

The benchmark contract reserves genomic `0` for absence supported by a sufficiently complete declared search. Before running a source-selected workflow, record a dated interpretation that names the enumerated roster, coverage basis, permitted comparison and limitations. A method whose assumptions need verified genomic absence remains input-unavailable until those requirements are met. Do not relabel source zeros merely because the baseline interface accepts them.

The [source-observation specification](caesar-source-observations-2026-10-02.md) retains within-condition medians, maximum condition height and any-condition detection at the source threshold of 10,000,000, with explicit missing-value rules. Raw heights are not normalized abundance. The 105-column draft preserves that aggregation, including unions of recorded conditions for explicit source aliases. The rosters select observations; they do not create a new normalization or pool acquisitions across media.

## Decisions needed before scoring

The [release-gap audit](../docs/data/source-gcf-release-gap-audit-2026-10-03.md) remains open. Complete these finite items and record the attributed decisions before comparative results are inspected:

| Decision or artifact | Required content |
|---|---|
| Track interpretation and observation policy | Approve or revise the source-nonmembership scope, common observation roster and all proposed dependence/media sensitivities. Preserve stronger core absence rules. Record whether prior ranks informed any choice. |
| Evaluator package and pathway groups | Separate positives from method inputs; put both pestalamide products under one query; preserve evidence-supported aliases and unresolved candidates as unlabeled. Attribute scientific dispositions and grouping rationale, including a coarser-group sensitivity if needed. Settle outstanding admission decisions before hashing the release ledger. |
| Measurement and method eligibility | Freeze the declared presence adaptation and missingness rules. Keep global normalized abundance unavailable until justified normalization exists. Require validated spectra and permitted classes for methods that use them; the strict NPClassScore adapter requires these for its complete pool. Record actual method/code/asset versions, parameters, failures and common eligible populations. Resolve a second substantive approach through compatible inputs or named adapter work; two Metcalf variants do not supply it. |
| Exposure record | Carry source-selected thresholds, historical rank exposure, known-reference use and unknown historical clustering details into every run manifest. Record each method's training/reference overlap and unknown exposure. Caesar remains retrospective; these rosters create no unseen-pathway claim. |
| Evaluation freeze and reproducibility | Freeze candidate/positive/group/roster hashes, metrics, tie handling, seeds, status rules and sensitivity availability under the existing analysis plan. Verify required evaluator fixtures and portable reconstruction from registered inputs. Keep author-workbook crosswalk provenance explicit and resolve redistribution terms before any authorized public release. |

For an adopted analysis, retain all 9,339 candidates unless a separately named, documented candidate release is approved. Apply the analysis plan's known-positive hit rates at 1, 10 and 100, expected reciprocal rank, product recovery, coverage and failure reporting. Estimate uncertainty at adjudicated pathway-group level, with per-query results and leave-one-group-out sensitivity. Few groups limit inference; extra media, candidate features and roster variants cannot expand the independent test count. Unknown measured candidates are not biological negatives.

## Local verification on 7 October

Read-only checks recomputed both TSV hashes and matched the [sensitivity receipt](../data/interim/source-gcf-host-expected/sensitivity-roster-receipt.json):

| File | SHA-256 |
|---|---|
| `caesar-source-gcf-population-2026-10-03.tsv` | `38f797694322680d5c46b79fcd50311fa5055bda2b9614ee90e2480d924b065a` |
| `caesar-source-gcf-sensitivity-rosters-2026-10-03.tsv` | `6621d68824e4f9362305693eda932b2982c881bc22e6f3651d7a9e863da52ab4` |

The checks confirmed unique roster/observation pairs, exact inclusion of the 105 population IDs, the 102 complete-media IDs, all eight distinct representative sets, and their eight 99-observation intersections. Every roster row carries the current population hash. All three dependency pairs have matching five-state vectors. The included membership-1 counts are 7, 11, 11, 10 and 7 in the query order above; all 105 included observations have known states for each query. The local candidate table contains 9,339 rows.

These checks verify metadata and set construction. They do not validate culture identity, genomic absence, biological independence or scientific admissions. No scoring, release freeze or new scientific sign-off was performed for this note.
