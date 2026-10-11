# Initial private source-selected GCF analysis package

`data/processed/source-selected-gcf-analysis-v1` is frozen for the initial private retrospective comparison through the external [host freeze record](../../data/processed/source-selected-gcf-analysis-v1-results/freeze.json), approved on 7 October 2026 at 12:42:57 UTC. That record sets `scoring_ready: true` for the exact manifest hash below. The package remains immutable: its internal candidate state and `scoring_ready: false` preserve its creation history. Read the package together with the external activation record.

The host adopted the [operational decision](../../protocol/source-selected-gcf-analysis-decision-2026-10-07.md) under user-authorized execution; this records no new human statistical review or biological admission. Analysis execution is underway, not complete. The reusable benchmark and paper remain unfinished.

The package fixes 9,339 candidates, five queries, six products and one conservative analysis group. Pestalamides A and B remain two products within `source:NRPSPKS_85`. It preserves all 18 overlapping observation rosters: the primary 105 observations, three-media 102, eight assembly-representative choices of 102, and their eight three-media restrictions of 99. These observations are not established independent genomes. Source-roster nonmembership is not verified genomic absence.

`inputs.json` and the separate `benchmark.json` carry the new track identity `source-selected-gcf-analysis-v1`. Original draft inputs, gold and manifests remain byte-for-byte snapshots under `snapshots/`; the original draft directories were not changed. Label and admission tables, groups, rosters, protocols, source manifests, code and host verification receipts are copied there too. Pending or excluded links stay unlabeled.

## Fixed roster inputs

One common input avoids storing 18 large copies. `rosters.json` lists each exact sorted observation set and the SHA256 and byte count of its actual serialized projection. `project_roster.py` retains the complete candidate pool, restricts cohort vectors and query membership to the roster, and sets every query's eligible observations to that same list. It serializes with sorted JSON keys, compact comma/colon separators, ASCII escapes, UTF-8 and one final LF. The script checks both common-input and derived-input hashes before writing, and refuses to write inside the fixed package or overwrite an existing output.

The following commands illustrate execution from the repository root. The host freeze is now in place; use unused output paths when reproducing these steps:

```powershell
$release = 'data/processed/source-selected-gcf-analysis-v1'
$run = 'data/processed/source-selected-gcf-analysis-v1-results'
New-Item -ItemType Directory -Path $run
python "$release/project_roster.py" --roster draft_all_source_observations --output "$run/primary-inputs.json"
python "$release/snapshots/scripts/run_baselines.py" --inputs "$run/primary-inputs.json" --method prevalence_difference --run-id source-selected-gcf-analysis-v1:primary:prevalence_difference --output "$run/primary-prevalence_difference.json"
python "$release/snapshots/scripts/evaluate_rankings.py" --benchmark "$release/benchmark.json" --run "$run/primary-prevalence_difference.json" --output "$run/primary-prevalence_difference-evaluation.json"
```

Materialize and validate each roster before inspecting scores. Run the four deterministic methods (`global_prevalence`, `prevalence_difference`, `metcalf_raw`, `metcalf_standardized`) on every roster. The frozen manifest declares unavailable methods and sensitivities, exposure, common eligibility, metrics and failure conventions.

Descriptive evidence stratification is available from the existing labels: one directly supported pestalamide query with two products, and four reference-supported queries with four products. Summarize their existing per-query evaluations without rerunning methods. Both strata share the same conservative analysis group; these counts do not support independent-group inference.

Uniform random uses the same candidate IDs, seed fields, gold and groups across every roster. Its seed excludes roster and run ID. After confirming the manifest's equality conditions for all inputs, compute the repeated-random result once and report its applicability to every roster:

```powershell
python "$release/snapshots/scripts/evaluate_random.py" --inputs "$run/primary-inputs.json" --benchmark "$release/benchmark.json" --run-id source-selected-gcf-analysis-v1:shared-random --seed 20260930 --initial-repeats 1000 --max-repeats 10000 --tolerance 0.001 --output "$run/shared-random.json"
```

This retains exact expectations and adaptive doubling. Exit code 3 means the repeat cap prevented the requested precision; retain the output and report `precision_not_achieved`. Monte Carlo variation does not measure biological uncertainty. With one conservative group, no biological bootstrap, confidence interval or significant-winner claim is supported.

## Integrity and reproduction

The build produced 123 hashed payload files plus the manifest, totaling 89,128,545 bytes after the host's pre-score correction to label-stratification availability. `source-integrity.json` records successful before/after hashes for all 115 source files and exact snapshot equality. The build checked every packaged payload hash and computed all 18 projected-input hashes without scoring. Existing host verification receipts were copied, not replaced with new biological-validation claims.

Manifest SHA256: `db5c9a653e873adf1c19781086ed287d65cb8836cad9a7f3bd1b6c6d33a04c84`.

`manifest.json` hashes every package file except itself. Host verification was pending at package creation. The host subsequently verified all 123 payload files, independently derived and checked all 18 projection hashes, confirmed exact original-input and gold equality except for the track identity, checked the labels, and verified shared random seed payloads. No scores were inspected before the freeze. This is computational integrity verification, not independent biological validation.

The external freeze record activates manifest SHA256 `db5c9a653e873adf1c19781086ed287d65cb8836cad9a7f3bd1b6c6d33a04c84` without changing any package file. Keep that receipt and analysis outputs outside the package. A portable verifier can reproduce the recorded checks against the same immutable bytes.

`build_recipe.py` is the finite packaging recipe. Rebuilding requires the recorded source snapshot versions and a nonexistent output directory:

```powershell
python "$release/build_recipe.py" --repo . --output data/processed/source-selected-gcf-analysis-v1-rebuild
```

Timestamps and the runtime record can differ on rebuild; compare copied source payloads and derived roster hashes. Baseline, evaluation, random and projection execution use Python's standard library. The environment record captures the Python runtime and installed builder dependency, while `snapshots/requirements.txt` pins `openpyxl==3.1.5` for source rebuilding. The host supplied revision `5d3dec4`; code hashes identify the copied implementation. Requested worker route was `gpt-6-astra / medium`; no serving-side receipt was exposed.

No rankings were generated or inspected during packaging. Keep this release private.
