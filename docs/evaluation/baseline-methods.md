# Baseline methods

The local runner implements the baseline controls proposed in the [analysis plan](../../protocol/analysis-plan.md) and Phase 4 of the [canonical project plan](../plans/2026-09-30-2052-benchmark-paper-plan.md). These six workflows include simple controls and related Metcalf variants. They do not establish six independent substantive linking approaches. Every implementation is named and versioned in the [method manifest](../../data/manifests/baseline-methods.json).

No biological release was scored during this unit. The supplied fixtures contain invented IDs and values; their gold answers are a separate file.

## Run the synthetic example

Use Python's standard library from the repository root. The output directory must already exist.

```powershell
python -S -m unittest tests.test_run_baselines -v
python -S scripts/run_baselines.py --inputs tests/fixtures/baselines/inputs.json --method metcalf_raw --run-id synthetic-metcalf-1 --output baseline-run.json
python -S scripts/evaluate_rankings.py --benchmark tests/fixtures/baselines/benchmark.json --run baseline-run.json --output baseline-evaluation.json
python -S scripts/run_baselines.py --inputs tests/fixtures/baselines/inputs.json --method uniform_random --seed 20260930 --repeat-index 7 --run-id synthetic-random-7 --output random-run.json
```

The Python API is `run_baseline(inputs, method_id, *, run_id, seed=20260930, repeat_index=0)` in `scripts/run_baselines.py`. It returns one run using the [ranking evaluator's interface](ranking-evaluator.md), with method version, run ID, track/query-type/universe identities, parameters, Python implementation/version, and per-query audit records. It doesn't mutate the input. Call `evaluate(benchmark, run)` with the separate benchmark object to calculate retrieval metrics.

The CLI serializes the complete result before writing a temporary file beside the destination, closes that file, then uses `os.replace`. Failed writes or replacements preserve an existing destination; temporary-file cleanup is attempted. This does not guarantee durability after power loss, and abrupt termination or failed cleanup can leave a temporary file. Exit 0 means a run was written, including runs with unavailable or abstaining queries. Malformed inputs, duplicate JSON keys and file errors exit 2. Inspect output statuses before interpreting an exit code as scoring coverage.

## Input schema 1

The root accepts exactly `schema_version`, `track_id`, `query_type`, `candidate_universe_id`, `candidate_pools`, `cohorts`, and `queries`. Use string `"1"` for the schema version. Identity fields and map keys are nonempty strings; IDs are used literally without alias normalization. Unknown fields are errors, including biological gold fields. The method API never takes a benchmark or positive-target file.

A minimal random-control input is:

```json
{
  "schema_version": "1",
  "track_id": "synthetic-feature",
  "query_type": "GCF",
  "candidate_universe_id": "example-v1",
  "candidate_pools": {"pool1": ["feature-a", "feature-b"]},
  "cohorts": {"cohort1": {}},
  "queries": [{
    "query_id": "query1",
    "cohort_id": "cohort1",
    "candidate_pool_id": "pool1"
  }]
}
```

Each candidate pool is a nonempty list of unique canonical feature IDs. Every query refers to an existing pool and cohort. Query IDs must be unique, and the query list must be nonempty. Reusing a pool or cohort never duplicates its tables per query.

A cohort may supply `strain_ids`, `feature_presence`, and `normalized_abundance`. The tables map candidate ID to a strain-ID-to-value object. Values are binary integers 0/1 for presence and finite nonnegative numbers for abundance. Booleans and string placeholders are not numeric values. Abundance must already be normalized under its released preprocessing specification; this runner applies no detection threshold, scaling across samples, imputation or replicate aggregation. The arithmetic mean uses numerical scaling internally to avoid overflow of a sum of large finite values; it does not change the input normalization.

A query may supply `eligible_strain_ids` and `genomic_presence`, the latter also a strain-ID-to-binary-integer map. Eligible IDs must be unique. If the optional cohort `strain_ids` roster is supplied, it constrains every supplied table/vector key and each query's eligible strains. Candidate keys in cohort tables must belong to a declared pool. Rows for candidates outside the query's pool and strains outside its eligible set are not used in that query's score. The roster may be omitted when explicit table keys and eligible IDs already provide the strain identities; this sacrifices the independent roster membership check. It does not authorize inferred strain matches.

Absent or null tables, vectors and cells represent unavailable observations. An omitted/null eligible-strain list, or an empty one, is unavailable for a method that needs strains. No method turns an unknown into 0, removes a candidate with missing input, or reduces the eligible-strain denominator. Presence and abundance can have different readiness. Structurally malformed supplied fields fail validation even when a selected method does not use them; missing scientific values affect only methods that need them.

All non-random workflows require complete values across every candidate in the query's pool and every eligible strain. The co-occurrence workflows also need complete genomic presence. Required-input completeness is checked before degenerate-vector abstention, so a query with both missing feature observations and an invariant genome is `input_unavailable`.

## Scores and audit fields

Higher scores rank first. Score rows are serialized in canonical candidate-ID order, with exact ties preserved. The evaluator supplies tie-aware retrieval credit; the runner adds no candidate-ID tiebreak score.

| Method ID | Score | Required scientific inputs |
|---|---|---|
| `uniform_random` | Unique descending integer scores assigned by a seeded permutation | Candidate IDs only |
| `global_prevalence` | Fraction of eligible strains with feature presence 1 | Eligible strains and feature presence |
| `global_abundance` | Mean normalized abundance over eligible strains | Eligible strains and normalized abundance |
| `prevalence_difference` | Feature prevalence among genomic-positive strains minus that among genomic-negative strains | Eligible strains, genomic and feature presence |
| `metcalf_raw` | `10*n11 - 10*n01 + 0*n10 + n00` | Eligible strains, genomic and feature presence |
| `metcalf_standardized` | Raw score centered and divided by its fixed-margin null standard deviation | Same as raw Metcalf |

For Metcalf, the first contingency-table index is genomic presence; the second is feature presence. With N eligible strains, g genomic positives, m feature positives and o overlapping positives:

```text
raw = 21*o + N - g - 11*m
E(raw) = 21*g*m/N + N - g - 11*m
Var(raw) = 441*g*m*(N-g)*(N-m) / (N*N*(N-1))   for N > 1
```

The implementation uses an equivalent product of bounded ratios for variance and a centered overlap for the standardized score. It records the four contingency counts, feature-positive count and raw score. Standardized output adds null mean, null variance and an exact `zero_variance` flag. Query audit records hold N and both genomic denominators. Global prevalence records its numerator and denominator; global abundance records its denominator.

`prevalence_difference` abstains with `zero_genomic_denominator` when either genomic group is empty. `metcalf_standardized` abstains with `invariant_genomic_presence` when g is 0 or N, including N=1. Otherwise a feature with m=0 or m=N receives neutral score 0 with `zero_variance: true`. Raw Metcalf may score all of these vectors, retaining their contingency counts. Missing required fields yield `input_unavailable` with a `missing_required_input:` reason naming the first affected field/cell in sorted order. Non-output rows have no `scores`. The runner does not invent numerical fallbacks or catch programming errors as scientific abstentions.

## Source relationship

The weights and fixed-margin null follow sections 2.1 and 2.2 of the [NPLinker paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008920). The reference implementation is [NPLinker v2.0.3, pinned commit 1a4603b9171b1a8e1d791cfc4b358bf51f3cfb87](https://github.com/NPLinker/nplinker/blob/1a4603b9171b1a8e1d791cfc4b358bf51f3cfb87/src/nplinker/scoring/metcalf_scoring.py). Exact retrieved source, unit-test and license hashes are in the manifest. This local code was independently written; it does not vendor, import or execute NPLinker.

This is a measured-feature formula adaptation. It does not reproduce the upstream family construction, data loading, preprocessing or linking workflow. The upstream code uses metabolomic presence as p1, genomic presence as p2, weights `(10, -10, 0, 1)`, and a score cutoff. Our complete rankings use no cutoff. Upstream replaces variance below 1e-9 with 1 before square rooting; this adaptation handles exact invariant feature vectors explicitly and abstains for invariant genomic vectors. The latter deliberately differs from upstream neutral zero scores. Formula agreement on synthetic cases does not establish full NPLinker equivalence.

No pretrained assets or reference database records enter these methods. Source-code references are implementation evidence, not biological inputs. Study selection and prior exposure still belong in the release manifests; these controls do not restore blindness to retrospective data.

## Random repeat contract

Each call produces one permutation per query at the requested repeat index. A stable per-query integer seed is the unsigned big-endian value of the SHA256 digest of this ordered array serialized as UTF-8 JSON with `ensure_ascii=False` and separators `(',', ':')`:

```text
["fungallink-baseline-random-v1", seed, repeat_index,
 track_id, query_type, candidate_universe_id,
 cohort_id, candidate_pool_id, query_id]
```

The base seed is any integer; the repeat index is a nonnegative integer. After sorting candidate IDs with Python string ordering, the runner constructs a fresh `random.Random(derived_seed)` and calls `shuffle`. It assigns pool-size through 1 in permutation order. The derived seed is stored as a decimal string to preserve all 256 bits across JSON consumers; the base seed, repeat index, digest specification, generator, Python implementation/version and random-state version are recorded in the run. Reordering inputs or adding/removing other queries cannot change a query's permutation. Pool/release IDs must refer to immutable content. Reproduce with the recorded Python implementation/version because the shuffle implementation is not pinned independently from Python.

The [repeated random control](random-controls.md) uses this per-repeat ranking primitive to report exact expectations, repeated means, standard deviations and Monte Carlo error checks. Biological group uncertainty is a separate analysis.

## Verification record

Before the implementation file existed, `python -S -m unittest tests.test_run_baselines -v` exited 1 with `ModuleNotFoundError: No module named 'scripts.run_baselines'`. The same command passed all 14 tests on 2026-10-01 using Python 3.13.5.

The tests enumerate fixed-size feature subsets for N=2 through 7, independently tally the four cell weights, and compare empirical null means, variances and standardized scores. Other checks cover asymmetric hand calculations; stable random seeds and complete permutations; query, strain and candidate order invariance; controls with genomic inputs removed; missing/null fields and cells; zero denominators and invariant vectors; N=1; finite abundance large enough to overflow a naive sum; malformed IDs and values; and multi-product evaluator integration through separate, shuffled gold. CLI checks cover successful replacement, duplicate-key rejection, and an injected replacement failure preserving existing bytes without leaving a temporary file.

The host also compared the public runner with the two inspected static function bodies `_calc_raw_score` and `_calc_mean_std` extracted from the pinned upstream source. All 494 raw-score cases matched exactly. The 406 standardized outputs agreed within 9.33e-15 absolute difference (tolerance 1e-10); the other 88 cases produced the declared invariant-genome abstentions. All 56 invariant-feature cases received flagged zero scores. The [verification receipt](../../tests/fixtures/baselines/upstream-parity-receipt.json) records Python 3.13.5, NumPy 2.4.6, pandas 3.0.5 and SciPy 1.18.0 for that separate host check. These packages are not runner or test-suite dependencies. The receipt is evidence of the host check, not a test oracle.

Requested implementation route: `gpt-6-astra` with `medium` reasoning. No serving-side model/effort receipt was exposed to this worker. No real-data experiment, biological label admission, protocol freeze, learned-method adapter, installation or external publication was performed. A general plugin framework, automatic missing-data fallback and within-run retry system were considered unnecessary for this bounded interface and were not built.
