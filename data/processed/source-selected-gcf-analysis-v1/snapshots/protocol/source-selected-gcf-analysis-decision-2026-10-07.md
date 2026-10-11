# Initial private source-selected GCF analysis decision

Prepared 7 October 2026 for host adoption under the [canonical plan](../docs/plans/2026-09-30-2052-benchmark-paper-plan.md), [benchmark contract](benchmark-contract.md) and [analysis plan](analysis-plan.md). Status: automated operational proposal, awaiting host verification and adoption in the analytical manifest. This document does not supply human scientific approval, change researcher-approved admissions, or declare an analysis freeze complete. Requested route: `gpt-6-astra / medium`; no serving-side receipt was exposed, so actual service is unverified. The humanizer skill was applied.

Proceed with an initial private retrospective comparison using the existing approved GCF snapshot. Keep the reusable benchmark, broader method comparison, cohort expansion and paper as the project objective. Completing this analysis will not complete that objective.

## Population and interpretation

Retain all 9,339 measured candidates, 105 source-study observations, five GCF queries and six approved GCF-product relationships. Pestalamides A and B share `source:NRPSPKS_85`. The two approved BGC relationships remain outside this track. New admission recommendations pending researcher disposition stay excluded and unlabeled in this snapshot; they do not delay packaging the existing approved set. Preserve their candidates in the full pool. Any later admission produces a new positive-set/release version.

For this source-selected comparison, interpret membership `1` as inclusion in the deposited family roster through the recorded display-to-study mapping, and `0` as covered nonmembership in that same roster. The enumerated families are `NRPSPKS_85`, `TERPENE_40`, `NRPSLIKE_59`, `NRPKS_18` and `NRPS_66`. The coverage basis is the [population ledger](../data/curated/caesar-source-gcf-population-2026-10-03.tsv), its recorded source-family rosters and mapping decisions, and the [numerical input provenance](../docs/data/source-gcf-inputs.md). Only the 105 included observations with known states for every query enter the comparison. Eleven withheld rows and the unallocated NRPSLIKE_59 member FMGX0070 retain their unresolved status.

This is a scoped adjustment to the contract's genomic-zero rule: the binary predictor is deposited roster membership, not verified whole-genome presence/absence. The local prevalence-difference and Metcalf workflows may compare these roster categories as declared source-selected adaptations. A method requiring verified genomic absence remains input-unavailable. Do not call this a reconstructed-family release, a complete genomic search or completion of the core genomic-presence contract.

The observational unit is the retained source-study observation, not a proven independent strain or genome. Preserve the existing within-condition medians and recorded condition unions, maximum condition height, and any-condition detection at 10,000,000. Presence is one if any required condition is detected, zero only if every required condition is observed below threshold, and missing otherwise. Heights remain raw. This separately documented historical aggregation uses the contract's allowance for source processing that cannot support its default biological hierarchy.

Predeclare every roster in the [existing sensitivity table](../data/curated/caesar-source-gcf-sensitivity-rosters-2026-10-03.tsv):

| Roster | Role | Observations |
|---|---|---:|
| `draft_all_source_observations` | Primary | 105 |
| `draft_three_media_only` | Recorded three-media coverage | 102 |
| `draft_assembly_representative_01` through `_08` | All eight choices across three dependency pairs | 102 each |
| Those eight IDs with `_three_media` appended | Representative choices restricted to three media | 99 each |

These are 18 overlapping analyses, including the primary. Report every roster, denominator and unavailable output. Keep the candidate pool and gold fixed across rosters. Do not select the best representative choice. The [draft analysis note](source-selected-gcf-draft-analysis-2026-10-07.md) records the unresolved Aspni orientation and inherited accession relationship; representative selection does not resolve either or prove genome independence.

## Grouping, methods and reporting

Assign all five queries to `caesar2023:source-selected-set-v1` using the [group table](../data/curated/source-gcf-analysis-groups-2026-10-07.tsv). This is a conservative analysis group for a shared cohort and source-selection history, not an assertion that all queries represent one biological pathway. Cross-query independence has not been established. Per-query results are primary descriptive evidence; the existing query-within-cohort/group averaging gives a descriptive set mean.

With one group, between-group biological uncertainty is not estimable. Do not bootstrap queries, report biological confidence intervals, claim five independent pathways or infer a significant winner. Leave-one-group-out has no remaining group and is unavailable. If shown, leave-one-query values are descriptive influence checks only.

Use `uniform_random`, `global_prevalence`, `prevalence_difference`, `metcalf_raw` and `metcalf_standardized` with the definitions and failure conventions in the [baseline method manifest](../data/manifests/baseline-methods.json). The two Metcalf workflows are related variants, not two substantive approaches. Preserve complete rankings, exact score ties, higher-is-better direction, invariant-vector behavior and missing-input statuses. Freeze actual implementation/dependency hashes after integration verification. The common intended population is all five queries on the same observations within each roster; input validation must confirm it before scores are inspected.

Global normalized abundance is unavailable because only raw heights exist. NPClassScore is unavailable because validated spectra and permitted classes do not cover the full candidate pool. A phylogeny-aware workflow/control is unavailable with the current tree and dependency inputs; do not invent exchangeability blocks. Record other sensitivities as unavailable where their required data do not exist. A second compatible substantive approach and broader method coverage remain unfinished benchmark work.

Retain the evaluator's expected known-positive hit@1, @10 and @100, expected reciprocal rank, distinct-product and all-products recovery, tie bounds, coverage and status reporting. Report pool sizes and effective cutoffs. Show conditional and end-to-end results with their denominators; zero credit for a runnable workflow's failed output means failure to deliver retrieval, not a biological negative. Entirely unavailable methods receive reasons rather than invented ranks. Unknown candidates remain unlabeled.

Use exact uniform-random expectations and the existing repeated-random driver with seed `20260930`, initial repeats `1000`, MCSE tolerance `0.001` and maximum repeats `10000`, retaining its adaptive doubling. This is an explicit pre-result amendment to the analysis plan's 10,000 starting repeats and uncapped escalation. Apply it to all roster runs. Report repeats, checkpoints, achieved MCSE and `precision_not_achieved` if the cap prevents meeting tolerance. Exact expectations remain available; Monte Carlo variability is not biological uncertainty. Record measured runtime and resources; no runtime estimate is established here.

No rankings were generated or inspected in preparing this decision. Historical rank exposure remains. Every run must carry source-informed family selection and clustering thresholds, known-reference use, historical rank inspection, unknown clustering implementation/run provenance and author-workbook crosswalk provenance. Local methods' lack of learned training does not remove that exposure. No unseen-pathway claim follows from this analysis.

## Host completion before the first score

1. Verify the evaluator package against the approved snapshot: five exact query IDs, six supported products, pestalamide grouping, supported aliases, full candidate membership and the separate group table. Retain excluded/pending relationships as unlabeled and preserve the attributed researcher decisions.
2. Pass evaluator fixtures and real-data integration checks, including complete candidate/query joins, no gold in method inputs, exact roster sets, valid presence/membership states and reconstruction from registered inputs without neighboring repositories. Passing code tests does not validate biology.
3. Assign a new analytical release identity. Preserve `source-selected-gcf-to-feature-draft-v1` and its existing not-ready manifest as input provenance; do not silently rewrite it as a frozen release. Identify each roster's derived method inputs and the shared candidate and positive-set versions.
4. Publish a private immutable package and manifest before score execution. Hash the verified inputs, candidate pool, positive sets, admission snapshot, group table, all rosters, method/evaluator/driver code, dependency versions and this adopted decision. Record seeds, random limits, exposure, unavailable methods/sensitivities, test receipts, adopter and timestamp. This later manifest supplies the freeze; this proposal supplies no fabricated hashes or completed-freeze claim.

There is no additional biological admission decision required for the existing approved snapshot. Integration or provenance mismatches require a concrete repair before scoring. Public release, external correspondence, data deposition and manuscript submission still require the user's authorization.
