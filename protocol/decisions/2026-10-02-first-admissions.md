# First researcher-led biological admissions

Decision date: 2026-10-02. Research lead and scientific reviewer: Vin Vomero, through explicit answers in the current user conversation. This is researcher-led review, not independent external review. The agent records the decisions and checks ledger consistency; it does not supply the scientific approval. Requested work route: `gpt-6-astra` / `medium`. No serving-side receipt was exposed, so actual model and effort are unverified.

These decisions implement the evidence rules in the [benchmark contract](../benchmark-contract.md) and [canonical plan](../../docs/plans/2026-09-30-2052-benchmark-paper-plan.md). They admit two biological relationships. They do not admit scoring queries or freeze analytical inputs. This case-specific criterion was adopted before any biological comparative results. Existing fixture tests and the synthetic-query format smoke check are software checks, not biological comparison results.

## Recorded questions and answers

Question 1, exactly as presented:

> Do you accept pestalamide B as a directly supported GCF-to-feature relationship? The published experiment supports a member of the source family, and feature 810 is traceable. This does not claim every family member produces it or that its release inputs are finished.

Vin Vomero's answer: **Accept the classification**

Decision: admit `caesar2023:pst:810` as directly supported at GCF-to-feature resolution, source family `NRPSPKS_85`, measured feature `810`. Direct evidence applies to the experimentally represented CBS 101.740 member. The nine displayed source members are neither nine independently admitted queries nor nine proven producers. This decision does not admit a separate exact-BGC query.

Question 2, exactly as presented:

> For emericellamide A, do you accept reference-supported classification for known-reference retrieval? Published reference experiments, authenticated-standard chemistry and exact protein correspondence support the link; the complete released annotation has no exact duplicate. Diverged or unannotated alternatives remain unexcluded. This would adopt that scoped evidence criterion, not claim exclusive biosynthesis.

Vin Vomero's answer: **Accept with the stated limits**

Decision: admit `caesar2023:relationship:6` as reference-supported at BGC-to-feature resolution, the recorded source locus `HRPKS_71|BN001307.1.region009|FMGX0049`, measured feature `8468`. For this known-reference retrieval case, experimental reference support, authenticated-standard named-feature chemistry, the recorded full-length exact protein correspondence and organization, and the completed exact-reference duplicate check are sufficient. The complete released protein annotation contains no second exact reference copy. Diverged alternatives, unannotated coding sequences, and the 63 CDS records without released proteins remain outside that check. This is not a claim of exclusive biosynthesis or a universal similarity threshold. Applying a criterion to another case requires its own recorded review; no automatic transfer to emericellamide B is authorized.

## Evidence provenance and retained limits

The [first-three assessment](../../docs/evidence/first-three-admission-decisions-2026-10-02.md), [pestalamide packet](../../docs/evidence/pestalamide-b.md), [emericellamide packet](../../docs/evidence/emericellamide-a.md), and [source-check receipt](../../docs/evidence/first-three-source-checks.json) contain the published experiment, chemistry, strain correspondence, and workbook evidence used for these decisions. The publisher workbook's recorded SHA-256 is `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb`. Feature 810 is Sheet1 row 818; feature 8468 is row 8476. Those are historical measured-feature joins, not validated native-spectrum joins.

The [competing-locus report](../../docs/evidence/emericellamide-competing-locus-review-2026-10-02.md) and [five-row result table](../../data/curated/emericellamide-competing-locus-review-2026-10-02.tsv) record one full-length exact match per retained reference among 10,534 released annotated proteins. The report retains source versions, hashes, annotation scope, and the prior sequence-comparison provenance. This decision uses those existing checks; no biological or genetic analysis was rerun. The named-product/isomer caveat remains as recorded in the first-three assessment.

Both cases retain source-selection and known-reference exposure. Their intended use is retrospective known-reference retrieval, not blind discovery or unfamiliar-pathway generalization. No independent pathway-group or chemical-diversity count is established here.

## Effect on the current ledgers

The current [label ledger](../../data/curated/label-evidence.tsv) and [capacity table](../../data/curated/benchmark-capacity-2026-10-02.tsv) record two admitted biological relationships: one directly supported GCF relationship and one reference-supported BGC relationship. Acetylaszonalenin remains pending; no feature-4182 E4-to-E correction is approved by these answers. Other unresolved cases remain unlabeled, not negative controls.

Capacity data dictionary: `admitted_relationship=1` records researcher-approved biological evidence. `core_GCF_admitted_query` and `BGC_admitted_query` count admitted scoring queries with the required frozen query inputs and remain zero. `executable_released_query` and `spectral_ready_query` also remain zero. Existing input-status columns, candidate readiness, historical feature status and analytical-release status are unchanged. Biological class is recorded in `recommendation`, with the decision and attribution in `scientific_signoff` and `biological_record`.

Pestalamide B still needs a versioned family roster, public sample/assembly mappings and clustering provenance. Emericellamide A still needs a sequence-defined query package with pinned boundaries and provenance. Shared preprocessing, sample eligibility, candidate/positive manifests and allowed method inputs remain unfrozen. Native-spectrum joins remain unresolved.

This decision supersedes the pending human decisions for these two relationships and the pending emericellamide case-specific review criterion in the earlier packets and gap register. Those dated records and the earlier review index remain unchanged as historical evidence. It does not supersede any other scientific decision. No comparative rerun is required because no biological comparative result preceded this decision; future runs must use a frozen release that cites it.
