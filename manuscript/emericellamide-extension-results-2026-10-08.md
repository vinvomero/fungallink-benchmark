# Emericellamide retrospective family-view extension

Public documentation copy prepared 13 October 2026 from the retained dated report. Its numerical tables and historical analysis below are unchanged. Dated inventory totals and private-candidate status describe the original analysis, not the current release.

Current scope is [data 1.0.0](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0) and [preprint 1.0.2](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.2): 30 relationships across 16 biological query identities, with 11 complete for the declared co-occurrence workflows, two partial diagnostics and 17 missing analytical inputs. The journal revision is an unpublished candidate. Accountable human scientific review remains pending.

For public replay, use the data ZIP and [current reproduction guide](../docs/release/reproduction-stages-v1.md). Frozen component archives retain historical filenames. Commands below record the original construction/verification route; use the packaged public replay for reproduction. Original author workbooks and correspondence are excluded. Historical integration-check filenames refer to private editorial records, not public prerequisites.

## Historical report

Completed 8 October 2026. This separate extension evaluates the already-admitted emericellamide A relationship through its fixed source HRPKS_71 family. It adds evaluated coverage, not a new biological relationship. Across the original nine-target analysis and this extension, 10 of 15 admitted relationships have now been evaluated through six query views. The underlying biological inventory remains 15 relationships across 11 query identities. Do not count the BGC and family representations twice.

The original five-query comparison and running phylogeny workflow remain unchanged. Their nine-target scope still applies. The main Markdown/Word/PDF review copies now include this separate extension; the existing private ZIP still predates it. See `emericellamide-integration-verification-2026-10-08.json`.

## Frozen analysis

The amendment, inputs, gold, 18 roster specifications, method/evaluator snapshots and 12-file freeze are in `data/processed/emericellamide-gcf-extension-v1/`. Four local workflows (version 0.1.0) each ranked all 9,339 candidates for all 18 rosters. The primary roster has 105 observations: 19 documentary family members and 86 roster nonmembers. The target is source feature 8468, and gold remains separate from method inputs.

This is a retrospective, reference-supported alternative query view. Earlier five-query results were known, but this view was frozen before its scores were computed. The family is broad and was not revised using performance. Its source roster does not establish genomic absence or production by every member. Historical source selection, private mapping provenance and one conservative analysis group still apply.

## Primary roster results

| Workflow | Target rank interval | Expected reciprocal rank | Hit@10 | Hit@100 |
|---|---:|---:|---:|---:|
| global_prevalence | 414–485 | 0.002229 | 0.000000 | 0.000000 |
| prevalence_difference | 13–15 | 0.071673 | 0.000000 | 1.000000 |
| metcalf_raw | 27–29 | 0.035745 | 0.000000 | 1.000000 |
| metcalf_standardized | 15–17 | 0.062663 | 0.000000 | 1.000000 |

Uniform-random exact expectations are reciprocal rank 0.001041, hit@10 0.001071 and hit@100 0.010708. No new Monte Carlo simulation was run. With one singleton target, any-hit, product recovery and all-products recovery coincide.

## Roster sensitivity and verification

- global_prevalence: hit@10 0.000000–0.000000; hit@100 0.000000–0.000000.
- metcalf_raw: hit@10 0.000000–0.000000; hit@100 1.000000–1.000000.
- metcalf_standardized: hit@10 0.000000–0.000000; hit@100 1.000000–1.000000.
- prevalence_difference: hit@10 0.000000–0.000000; hit@100 1.000000–1.000000.

All 72 outputs have complete candidate coverage. The 18 overlapping rosters are sensitivities, not independent replicates. No significant winner or broader generalization claim follows.

Execution took 117.48 seconds. A separate verifier reconstructed contingency scores from frozen feature and membership inputs and checked 672,408 scores, then independently calculated singleton tie intervals and 720 metric cells. All matched within 1e-12. An initial verifier formula incorrectly gave query-only cells weight −1; the recorded frozen specification gives weight zero. The verifier was corrected to that specification; no method scores or inputs were changed. This is numerical verification on the same host, not independent biological validation.

Reproduction in a separate restored copy: `python -B data/processed/emericellamide-gcf-extension-v1/run_extension.py`. The runner refuses an existing results directory. Check results using `python -B scripts/verify_emericellamide_extension.py`. Do not overwrite canonical results.

Evidence: [projection](../docs/data/emericellamide-gcf-projection-2026-10-08.md), [frozen manifest](../data/processed/emericellamide-gcf-extension-v1/manifest.json), [completion receipt](../data/processed/emericellamide-gcf-extension-v1-results/execution-complete.json), [numerical verification](../data/processed/emericellamide-gcf-extension-v1-results/independent-numerical-verification.json), [90-row results table](../data/processed/emericellamide-gcf-extension-v1-results/results.tsv).
