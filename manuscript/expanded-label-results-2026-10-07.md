# Expanded positive-set analysis

Public documentation copy prepared 13 October 2026 from the retained dated report. Its numerical tables and historical analysis below are unchanged. Dated inventory totals and private-candidate status describe the original analysis, not the current release.

Current scope is [data 1.0.0](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0) and [preprint 1.0.2](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.2): 30 relationships across 16 biological query identities, with 11 complete for the declared co-occurrence workflows, two partial diagnostics and 17 missing analytical inputs. The journal revision is an unpublished candidate. Accountable human scientific review remains pending.

For public replay, use the data ZIP and [current reproduction guide](../docs/release/reproduction-stages-v1.md). Frozen component archives retain historical filenames. Commands below record the original construction/verification route; use the packaged public replay for reproduction. Original author workbooks and correspondence are excluded. Historical integration-check filenames refer to private editorial records, not public prerequisites.

## Historical report

The private amendment `source-selected-gcf-expanded-labels-v2` evaluates nine supported product or measured-feature targets across the same five GCF queries and all 9,339 candidates. It adds corrected source-named notoamide E (feature 4182) and the structure-putative pestalamide E/F-associated features (1950/895). The source:NRPS_66 query now has two targets, source:NRPSPKS_85 has four, and the other three queries retain one each. These are nine supported targets at their declared chemical resolutions, not nine fully elucidated structures.

The [attributed amendment](../data/processed/source-selected-gcf-expanded-labels-v2/analysis-amendment.json) was recorded before inspecting the added targets' ranks. Admissions rest on the [retained-evidence decision](../protocol/decisions/2026-10-07-delegated-admission-dispositions.md). The original six-product results had already been viewed; this is a source-selected retrospective extension, not a blind prospective test. H and FAC cases are excluded.

## Cached scores and new gold

The existing gold builder joined the canonical ledger to unchanged query inputs and the existing conservative group table. It included nine GCF relationships and excluded six BGC relationships. The [new gold and selection audit](../data/processed/source-selected-gcf-expanded-labels-v2/gold/benchmark.json) preserve every original positive and every candidate/query/group field. The [release manifest](../data/processed/source-selected-gcf-expanded-labels-v2/manifest.json) identifies the new positive-set version and hash, the original input and method/evaluator hashes, and every reused ranking hash. The semantic track ID remains `source-selected-gcf-analysis-v1` to permit exact cached-score reuse; the new release and gold version are explicit.

All 72 original ranking files were reused byte-for-byte, with unchanged scores, method parameters and implementation version 0.1.0. The frozen evaluator produced new evaluation files for four deterministic workflows across all 18 original rosters. Every query had complete coverage, so conditional and end-to-end summaries coincide. Verification preserved all 285 files in the original package/results directories and checked all 18 roster input projections. No scoring function was rerun. The builder's internal draft flags remain historical construction fields; the separate attributed amendment authorizes only this verified private evaluation.

## Primary results

Expected metrics use uniform ordering within exact score ties. MRR averages reciprocal rank of the first target; product recovery averages distinct-target recovery within each query, then across queries. All-products measures joint recovery of every target. Values below use the primary 105-observation roster. Random values are exact expectations rounded for display.

| Workflow | Hit@1 | Hit@10 | Hit@100 | MRR | Product recovery@10 | All products@10 | Product recovery@100 | All products@100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| global_prevalence | 0.000000 | 0.000000 | 0.000000 | 0.001107 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| uniform_random_exact | 0.000193 | 0.001926 | 0.019116 | 0.001674 | 0.001071 | 0.000643 | 0.010708 | 0.006447 |
| prevalence_difference | 0.000000 | 0.487302 | 1.000000 | 0.132674 | 0.353968 | 0.242857 | 0.900000 | 0.800000 |
| metcalf_raw | 0.050397 | 0.853968 | 1.000000 | 0.252240 | 0.603968 | 0.453968 | 0.966667 | 0.933333 |
| metcalf_standardized | 0.014286 | 0.615079 | 1.000000 | 0.192873 | 0.477579 | 0.365079 | 0.915000 | 0.803846 |

The three query-dependent workflows retain their initial primary any-hit and MRR values, but recovery of every supported target is lower under the expanded positive set. Thus unchanged early retrieval does not imply complete recovery of the newly admitted targets. The old six-product claim that all query-dependent workflows recover every product by rank 100 does not apply to this expanded set.

## Evidence strata and roster sensitivity

The directly supported stratum is one pst query with four measured targets, including the two putative structures. The reference-supported stratum comprises four queries and five targets, including notoamide E. Both remain subsets of one conservative analysis group. The TSV includes all per-query and evidence-stratum values for every roster and workflow, including exact random expectations.

| Workflow | Primary direct hit@10 | Primary reference hit@10 | Across-roster hit@10 min–max | Across-roster all products@100 min–max |
|---|---:|---:|---|---|
| global_prevalence | 0.000000 | 0.000000 | 0.000000–0.000000 | 0.000000–0.000000 |
| uniform_random_exact | 0.004277 | 0.001338 | 0.001926–0.001926 | 0.006447–0.006447 |
| prevalence_difference | 0.222222 | 0.553571 | 0.465079–0.590476 | 0.800000–0.807973 |
| metcalf_raw | 1.000000 | 0.817460 | 0.767857–0.853968 | 0.753471–0.933333 |
| metcalf_standardized | 0.250000 | 0.706349 | 0.577579–0.697243 | 0.800000–1.000000 |

The rosters remain the primary 105 observations, three-media 102, eight assembly-representative 102-observation choices, and their eight three-media restrictions of 99. They overlap and are not independent replicates. Neither their ranges nor within-score tie bounds are biological confidence intervals. Source-roster nonmembership remains documentary, not verified genomic absence. No significance, method superiority or unseen-pathway claim is made.

## Exact random control and reproducibility

No new Monte Carlo run was performed, and the initial six-product Monte Carlo statistics are not reused. For N candidates and p distinct singleton product targets, exact any-hit is 1−C(N−k,p)/C(N,p), mean product recovery is k/N, and all-products probability is C(k,p)/C(N,p), or zero when k<p. Expected reciprocal rank sums C(N−u,p−1)/[C(N,p)u] over u=1,…,N−p+1. The [exact-random record](../data/processed/source-selected-gcf-expanded-labels-v2-results/exact-random.json) retains formulas and per-query expectations. Its roster invariance follows from unchanged candidate and positive sets, not from a new independence assumption.

The [recorded recipe](../data/processed/source-selected-gcf-expanded-labels-v2/evaluate_cached.py) performs identity, projected-input, cached-ranking and preservation checks before and after evaluation. Run it only in a restored copy with a fresh results directory and without its previously generated snapshots/manifest, because it refuses to overwrite those outputs. Rebuild gold with the existing `scripts/build_source_gcf_evaluation.py` using the snapshotted ledger/group table and original frozen inputs. The numerical evaluation depends on the original frozen evaluator and cached ranking files. Those are hashed dependencies, not duplicated or synthesized score files.

The [validation receipt](../data/processed/source-selected-gcf-expanded-labels-v2-results/validation.json) records 72 successful evaluations, full coverage, 18 verified projections, zero scoring recomputations, zero Monte Carlo runs and unchanged original artifacts. The [720-row result table](expanded-label-results-2026-10-07.tsv) contains overall, five per-query, and two evidence-stratum summaries for each of five workflows across 18 rosters. Full evaluator JSON files preserve product-specific ranks, exact tie bounds and status fields. Execution time is recorded in the receipt and is evaluation/export cost, not a new method benchmark.

Requested route: gpt-6-astra / medium; actual serving receipt unavailable. This remains a private analysis amendment. No original analysis, H/FAC scoring activation, public release or submission was performed.
