# Acetylaszonalenin retrospective family-view extension

Public documentation copy prepared 13 October 2026 from the retained dated report. Its numerical tables and historical analysis below are unchanged. Dated inventory totals and private-candidate status describe the original analysis, not the current release.

Current scope is [data 1.0.0](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0) and [preprint 1.0.2](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.2): 30 relationships across 16 biological query identities, with 11 complete for the declared co-occurrence workflows, two partial diagnostics and 17 missing analytical inputs. The journal revision is an unpublished candidate. Accountable human scientific review remains pending.

For public replay, use the data ZIP and [current reproduction guide](../docs/release/reproduction-stages-v1.md). Frozen component archives retain historical filenames. Commands below record the original construction/verification route; use the packaged public replay for reproduction. Original author workbooks and correspondence are excluded. Historical integration-check filenames refer to private editorial records, not public prerequisites.

## Historical report

Completed 8 October 2026. This evaluates the already-admitted corrected acetylaszonalenin relationship through source family DMAT_34. Across the original nine-target comparison and two separate extensions, 11 of 15 admitted relationships have evaluated coverage through seven query views. The biological ledger remains 15 relationships across 11 query identities. Alternative views do not add biological positives.

The frozen primary input has 105 observations, three documentary family members and 102 roster nonmembers. All four version-0.1.0 workflows ranked the same 9,339 candidates on all 18 overlapping rosters. Target feature 2127 represents relationship caesar2023:corrected:5. The source family was selected and frozen before these scores; earlier analyses were already known.

## Primary roster results

| Workflow | Target rank interval | Expected reciprocal rank | Hit@10 | Hit@100 |
|---|---:|---:|---:|---:|
| global_prevalence | 1389–2431 | 0.000537 | 0.000000 | 0.000000 |
| prevalence_difference | 2–2 | 0.500000 | 1.000000 | 1.000000 |
| metcalf_raw | 92–92 | 0.010870 | 0.000000 | 1.000000 |
| metcalf_standardized | 2–2 | 0.500000 | 1.000000 | 1.000000 |

Uniform-random exact expectations are reciprocal rank 0.001041, hit@10 0.001071 and hit@100 0.010708. No Monte Carlo rerun was needed. Singleton any-hit and product-recovery metrics coincide.

## Roster sensitivity

- global_prevalence: hit@10 0.000000–0.000000; hit@100 0.000000–0.000000.
- metcalf_raw: hit@10 0.000000–0.000000; hit@100 1.000000–1.000000.
- metcalf_standardized: hit@10 1.000000–1.000000; hit@100 1.000000–1.000000.
- prevalence_difference: hit@10 1.000000–1.000000; hit@100 1.000000–1.000000.

All 72 runs completed in 214.89 seconds. Separate contingency arithmetic checked 672,408 scores and independent singleton tie calculations checked 720 metric cells; all agreed within 1e-12. Manifest and completion-output hashes matched. This checks numerical consistency on the same host, not independent biological validation.

These overlapping rosters are not independent replicates. Source-selected families, one conservative analysis group, prior exposure, the assembly contamination flag and unknown locus-specific contamination status remain limitations. Roster nonmembership is not demonstrated genome-wide absence. Exact core-protein correspondence does not prove complete historical-region identity or production by every family member.

The dated correction explicitly supersedes the old family-exclusion interpretation, whose coordinates came from successor annotation numbering. Original evidence and frozen analyses are preserved. The original five-query phylogeny comparison is unchanged.

The main review Markdown/Word/PDF now include this extension; see `acetylaszonalenin-integration-verification-2026-10-08.json`. Private ZIP v2 remains the preserved ten-relationship version. Four admitted relationships remain unevaluated: ilicicolin H and the three FAC-MS relationships.

Reproduce only in a separate restored copy: `python -B data/processed/acetylaszonalenin-gcf-extension-v1/run_extension.py`; the runner refuses an existing results directory. Verify cached results with `python -B scripts/verify_acetylaszonalenin_extension.py`.

Evidence: [source correction](../protocol/decisions/2026-10-08-acetylaszonalenin-family-source-correction.md), [frozen manifest](../data/processed/acetylaszonalenin-gcf-extension-v1/manifest.json), [completion](../data/processed/acetylaszonalenin-gcf-extension-v1-results/execution-complete.json), [numerical verification](../data/processed/acetylaszonalenin-gcf-extension-v1-results/independent-numerical-verification.json), [results table](../data/processed/acetylaszonalenin-gcf-extension-v1-results/results.tsv).
