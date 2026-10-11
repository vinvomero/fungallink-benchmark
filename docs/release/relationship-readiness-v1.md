# Relationship readiness, version 1

Prepared 11 October 2026 from retained project records. [relationship-readiness-v1.tsv](../../data/curated/relationship-readiness-v1.tsv) is a derived release view. The [label ledger](../../data/curated/label-evidence.tsv) remains the authority for biological admission. Frozen task manifests remain the authority for scored query views, candidate pools and gold.

The table contains 30 relationships and 16 ledger query identities: 20 directly supported and 10 reference-supported. Eleven relationships have complete evaluated coverage across seven query views; two have partial diagnostics; 17 have no usable benchmark inputs. Complete coverage describes the declared evaluated task, not eligibility for every method. Nine of the complete relationships also occur in the fixed five-query phylogeny comparison; the two family-view extensions do not.

| Current input state | Relationships | Meaning |
|---|---:|---|
| complete | 11 | Saved full-pool deterministic evaluations, each with 9,339 candidates |
| partial | 2 | Completed spectral-class diagnostic with unavailable candidates retained |
| missing | 17 | FAC/HEx full expression-screen pool or required native joins unavailable |

The 6-MSA diagnostic scores 291 of 1,249 candidates; its target rank is 95–291 among scored candidates and 95–1,249 over the full pool. Ilicicolin H scores 89 of 98, with target bounds 16–21 and 16–30 respectively. These ranks must not be pooled with complete evaluations. Unknown relationships remain unlabeled, and distinct products within one query are not independent pathways.

## Derivation and joins

Join the derived view to the ledger and the [human review packet](../../manuscript/scientific-review-v1.tsv) by `relationship_id`. `query_id` is the unchanged ledger identity; `evaluation_query_view` identifies a separately frozen method representation. The acetylaszonalenin named-core BGC maps to `source:DMAT_34`; emericellamide A maps to `source:HRPKS_71`. These are declared BGC-to-GCF transformations, not new biological queries. The remaining five complete views retain their source GCF identity. All complete views share the conservative `caesar2023:source-selected-set-v1` analysis group. A group is not a claim that all rows belong to one pathway.

The only ledger edit appends the dated [8 October supersession](../../protocol/decisions/2026-10-08-acetylaszonalenin-family-source-correction.md) to acetylaszonalenin's existing alternative-locus cell. It makes the historical publisher-family exclusion visibly superseded while retaining the original text. The named-core identity, biological label, contamination flag and unknown locus-specific status are unchanged. Earlier packets and frozen ledger copies remain historical evidence.

Current input status comes from `data/interim/admitted-input-coverage-2026-10-09/all-admitted-relationships.tsv`, checked against frozen gold and completed diagnostic JSON. Its older next-action prose is not copied: the phylogeny comparison has since completed. Admission-time ledger readiness strings are not current task status.

No evidence row has been newly checked by a human through this packet. Historical admission provenance is retained separately from the pending final review. Delegated assistant curation is not recorded as personal author review.

## Field dictionary

TSV uses UTF-8 and one row per relationship. There are no blank cells. `unknown` means a value is not established; `not_applicable` means the field has no declared value for this task; `not_adjudicated` preserves an unresolved grouping; `pending` names work awaiting a human or final assembly. Semicolons separate file lists. Pipe characters inside identifiers belong to those identifiers and must not be used as general delimiters.

The source mapping below covers every column. Ledger fields are addressed by the row's `relationship_id`; frozen gold is addressed by query and product key. Source locators preserve the ledger's existing page, panel, table, workbook cell and acquisition descriptions. A locator's presence is not a claim that this revision reinspected its underlying experiment.

| Fields | Source and interpretation |
|---|---|
| `relationship_id`, `cohort`, `product`, `query_type`, `query_id`, `pathway_group`, `admission_status` | Same-named ledger fields, copied without scientific changes |
| `query_representation_version` | Explicit version suffix in ledger query identity where present; otherwise points to the ledger identity and packet for detailed bounds/version |
| `evaluation_query_view`, `evaluation_version` | Query ID and package directory from the three frozen core gold files, or ledger query and completed diagnostic package for partial cases; no evaluation asserted for missing cases |
| `query_view_transform`, `query_view_transform_source` | Named declaration derived from frozen gold, the Oct8 acetylaszonalenin correction, or emericellamide `analysis-amendment.json`; partial cases use the reference-informed genomic/spectral-class diagnostic |
| `shared_query_group` | Exact ledger `query_id`, for counting products sharing a biological query |
| `analysis_group` | Complete Caesar tasks use their recorded conservative shared source-cohort group; other group independence is `not_adjudicated` |
| `experimental_context` | Curator summary of ledger cohort, strain, experimental anchor and transfer fields; distinguishes native measurement, engineered native background and heterologous expression |
| `experimental_anchor` | Ledger `reference_pathway_evidence`, including direct experiments where applicable |
| `source_locator` | Ledger `chemical_identity_evidence` and `measured_target_evidence` together; retained source-specific locators and limitations |
| `reference_transfer_basis` | Ledger `sampled_locus_correspondence`; direct rows still carry their correspondence evidence and do not thereby become reference-supported |
| `source_target_key` | Ledger `source_feature_id`; panel and numbered-product keys are not native feature IDs |
| `evaluation_target_key` | Frozen gold target ID(s), or completed diagnostic `target_id`; missing cases have no invented evaluation join |
| `target_identity_resolution` | Ledger `source_chemical_tier` and `chemical_identity_evidence`; retains putative names, unresolved isomers and source conflicts |
| `uncertainty` | Ledger `alternative_loci_status` and `remaining_scientific_decision`; includes the current acetylaszonalenin supersession |
| `evidence_class` | Ledger `proposed_evidence_class`; separate from chemistry tier and readiness |
| `current_decision` | Decision paths retained in ledger admission provenance/source checks, plus applicable representation declaration; does not replace the original admission |
| `supersession` | Oct8 acetylaszonalenin correction for that row; `not_applicable` means no added supersession in this derivation |
| `input_state`, `retained_coverage_status` | Normalized complete/partial/missing state and unchanged status code from the 30-row coverage report |
| `candidate_count` | Frozen query candidate list length or diagnostic JSON `candidate_count`; `unknown` for missing pools |
| `input_scope`, `target_sample_join_status` | Coverage report `candidate_pool` and `target_and_sample_joins` |
| `global_prevalence_eligibility`, `prevalence_difference_eligibility`, `metcalf_raw_eligibility`, `metcalf_standardized_eligibility`, `core_method_reason` | Complete core methods from frozen tasks; partial diagnostics have no approved cross-genome co-occurrence task; FAC/HEx inputs are unavailable |
| `bayestraits3_directed_lrt_eligibility`, `bayestraits3_reason` | Frozen phylogeny gold membership and completed v2 summary; eligibility is conditional on its fixed tree/model and matched population |
| `npclassscore_eligibility`, `npclassscore_reason` | Completed partial diagnostic outputs and coverage; no complete-pool spectral/class eligibility is claimed elsewhere |
| `method_readiness_sources` | Existing coverage/evaluation files supporting those method states; includes completed phylogeny summary where applicable |
| `evidence_packet`, `source_records`, `ledger_source` | Ledger packet; deduplicated ledger and coverage source paths plus current decisions; explicit authoritative row locator |
| `historical_admission_provenance` | Ledger `human_reviewer` copied as historical provenance, including assistant-curation qualifications |
| `review_status`, `reviewer`, `review_date` | Newly initialized final-review fields, all explicitly pending |

Method status `eligible_complete` describes the four saved deterministic workflows, `eligible_partial_diagnostic` describes the two NPClassScore diagnostics, and `eligible_complete_fixed_tree_model` describes the conditional phylogeny comparison. `not_in_frozen_phylogeny_task` and `not_evaluated_in_this_task` are scope exclusions, not low scores. `unavailable_inputs` is not a failed biological label. Method versions and execution commands belong to task/exposure and reproduction manifests; this table does not claim exhaustive compatibility with every possible method.

## Human review packet

`manuscript/scientific-review-v1.tsv` has the same 30 relationship IDs. It provides source packets/locators, current decisions, recorded uncertainty and a row-specific review focus. Priority rows cover acetylaszonalenin, notoamide E, griseofulvin, pestalamide E/F, FAC/HEx boundaries and both partial diagnostics. Standard rows still require review.

The human reviewer fills `source_checked`, `judgment`, `uncertainty_or_disagreement`, `required_correction`, `reviewer`, `review_date` and `review_status` after checking the cited sources. Use an ISO date (YYYY-MM-DD), identify the actual reviewer, and retain disagreement rather than forcing agreement. `affected_release_identity` names the planned candidate; its archive hash remains pending assembly. `affected_records` identifies records to update if review requires a correction. Pending cells are not endorsements.

Verification is recorded in [evidence-verification.json](../../planning/presubmission-revision-work-2026-10-11/evidence-verification.json). It checks counts, exact IDs, frozen mappings, local source-file existence and the single ledger-cell append. It does not validate the scientific judgments or establish permission to distribute third-party source files.
