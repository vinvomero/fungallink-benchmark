# Reproduction stages and task exposure, version 1

This guide covers saved numerical reproduction for 11 completely evaluated relationships and two partial diagnostics. Seventeen admitted FAC/HEx relationships lack usable expression-screen inputs and have no advertised ranking workflow. Biological admission does not imply that a method can run.

The [stage matrix](reproduction-stages-v1.tsv) gives inputs, archive members or retrieval records, exact retained commands, environments, expected comparisons, recorded timings and exclusions. The [task/exposure table](../../data/manifests/task-exposure-v1.tsv) joins every admitted relationship to its ledger query and evaluated view. Both are derived release records; the ledger, protocols and frozen scientific files remain authoritative. Historical candidate-only, pending-tree and non-admission wording in frozen manifests records their creation state and does not override current admissions or completed runs.

## Choose a starting point

For the 11 complete relationships, extract the [core numerical archive](../../data/processed/core-numerical-candidate-v1-2026-10-11/fungallink-core-numerical-private-v1.zip) into a fresh directory and run from its root:

```text
python -I -S -B expanded/reproduce.py --all-rosters
python -I -S -B emericellamide/reproduce.py --all-rosters
python -I -S -B acetylaszonalenin/reproduce.py --all-rosters
```

The first command covers nine relationships across five query views. The extensions add one relationship and one view each. Four deterministic controls, version 0.1.0, run on 18 frozen rosters: global prevalence, prevalence difference, raw Metcalf and standardized Metcalf. They use no learned training assets. The 18 rosters are overlapping sensitivity populations, not folds or independent replicates. The original [receipt](../../data/processed/core-numerical-candidate-v1-2026-10-11/reproduction.json) records 216 matching method/roster combinations in 253.861 seconds under CPython 3.13.5. Omit `--all-rosters` for the documented primary-roster check. Monte Carlo is outside this replay.

The seven complete query views share one conservative source-selected analysis group, `caesar2023:source-selected-set-v1`. This grouping does not assert that they are one biological pathway. Keep the two family extensions separate from the five-query summary. In particular, the acetylaszonalenin ledger query is the named reference core; `source:DMAT_34` is its separate evaluated family view. The [8 October correction](../../protocol/decisions/2026-10-08-acetylaszonalenin-family-source-correction.md) governs that distinction. Emericellamide uses the separate `source:HRPKS_71` evaluation view.

For either partial diagnostic, restore the [spectral archive](../../data/processed/spectral-release-candidate-v1-2026-10-11/fungallink-spectral-private-candidate-v1.zip), including its `workspace/` hierarchy. Restore the hash-pinned table using the [existing retrieval recipe](npclassscore-dependency-route-2026-10-11.md), then use the documented command:

```text
python -I scripts/verify_saved_spectral_diagnostics.py --root <restored-workspace>
```

Run from the restored workspace where `scripts/` resides; replace `<restored-workspace>` with its path. This single verifier checks both diagnostics. They remain separate results:

| Diagnostic | Scored / full pool | Scored-only target rank interval | Full-pool conservative interval |
|---|---:|---:|---:|
| 6-MSA | 291 / 1,249 | 95–291 | 95–1,249 |
| Ilicicolin H | 89 / 98 | 16–21 | 16–30 |

These are tied-rank intervals, not uncertainty intervals from independent samples. Unavailable candidates remain in the full pool. Never combine conditional scored-only ranks with complete rankings. Ninety Trichoderma spectra received predictions, but an unknown class leaves only 89 usable linking scores. Saved-class arithmetic reproduced all 1,347 candidate records, comprising 380 scores and 967 unavailable records; [receipt](../../data/interim/spectral-arithmetic-reproduction-2026-10-11/receipt.json). It did not repeat Spec2Class inference. NPClassScore kernel version 1.0.0 uses the pinned NPLinker 1.2.0/MIBiG 2.0 table; predictor revisions and weight hashes remain in the per-run records. Weight-specific predictor training overlap remains unknown. The similarity companion records bounded stable-ID membership checks against declared retained reference files; those checks do not establish model-training membership. Genomic classes are reference-informed, so this is not blind sequence prediction.

For saved phylogenetic fits, extract the [phylogeny archive](../../data/processed/phylogeny-audit-candidate-v1-2026-10-11/fungallink-phylogeny-audit-private-v1.tar.gz) to Linux-local storage. Allow at least 2 GB free space. Use the environment pinned by [phylogeny-linux-explicit.txt](environment/phylogeny-linux-explicit.txt), with [package metadata](environment/phylogeny-linux-environment.json). The passed reconstruction used CPython 3.12.15, GCC 15.3.0, x86_64 WSL2 Linux and glibc 2.43. From the extracted root:

```text
python -S -B scripts/check_phylogeny_recovery_completion.py --root . --output terminal-audit.json
python -S -B scripts/export_phylogeny_paper_tables.py --root . --output reviewer-tables
```

Use new output paths. The exporter repeats the audit before writing 30 query rows, 54 product rows and six method summaries; those output-row counts are not counts of independent queries. The [retained verification](../../data/processed/phylogeny-audit-candidate-v1-2026-10-11/verification.json) checked 116,782 copied files and all 7,290 pair patterns, including 24 recovered pairs. Audit runtime was 19.66 seconds. The Windows equality failure, 0.9807294200365735 versus 0.9807294200365736, remains retained. Do not weaken equality to claim cross-platform exactness.

## What replay establishes

Saved numerical replay checks deterministic arithmetic, identities, input hashes, candidate restoration and evaluation. Raw-to-fit replication would also require source acquisition, raw LC-MS processing, sequence annotation, predictor inference, marker recovery, alignment, tree estimation and native optimization. Those stages have separate historical records in the matrix; they were not repeated for this revision. A copied native command containing historical absolute paths is provenance, not a portable launch instruction. `unavailable` in the command column means no portable command is advertised at this boundary. It does not claim that retained local scientific records are absent. Unrecorded runtimes remain unrecorded.

Phylogenetic results are conditional on the fixed tree/model and matched observation population. Preserve the 65/66 composition-test failures, LG+F+G4 unpartitioned model, midpoint rooting, lack of support resampling, retrospective optimizer recovery and 24 recovered pairs. Numerical agreement establishes neither phylogenetic adequacy nor global optimizer convergence. A broader method or biological claim would require separately planned robustness work.

All tasks are retrospective: no independent held-out test. Caesar family selection and clustering thresholds were source-informed; known references and historical rankings were exposed. Shared-query and pathway labels are carried from the ledger, including `not_adjudicated`. Genomic correspondence, chemical structure similarity and spectral/adduct redundancy are separate concepts. The task table preserves correspondence evidence and known shared groups. The [similarity companion](similarity-independence-v1.md) adds ten chemical pairs from five supported structures, 3,575 compatible core-protein comparisons and 46,290 within-pool spectral comparisons. Twenty-five relationships lack supported structures, and missing spectra or incompatible comparisons remain unavailable. These bounded matrices do not establish chemical diversity for the full inventory or an independent holdout. Distinct feature IDs do not establish distinct chemical structures, and unknown links are not negative labels.

## Table fields and verification scope

In the task table, `relationship_id` is the ledger join key. `ledger_query_id`, `shared_query_group`, `pathway_group`, `prior_exposure` and `genomic_relatedness` come from the corresponding ledger fields. `task_query_view` and `task_version` identify the frozen evaluation representation. Candidate/scored counts come from frozen manifests and diagnostic evaluations. Method versions and assets come from the named method manifests and predictor runs. Semicolon-separated `source_records` and `method_manifest` fields are repository-relative paths; pipe-separated `method_ids` list related workflows rather than independent approaches. Ledger query IDs can themselves contain pipes and must be treated as opaque strings. `not_applicable`, `not_adjudicated`, `not_assessed` and `unknown` are explicit states, not zero values.

Stage-table `archive_or_retrieval` uses `archive::member` for an archive member or member directory. Commands marked historical are not executed by the release smoke checks. Environment locks describe a tested numerical environment; they do not bundle native executables, raw data or predictor weights. Timings are retained observations, not new measurements or resource guarantees.

The presubmission audit already passed 216 core replays and 188 tests with two skips. This revision checks changed records and references only. Same-host reproduction is not independent researcher validation, human biological review or proof of an anonymous external download route. Release remains private; final human scientific review and authorized download-only verification remain outstanding.
