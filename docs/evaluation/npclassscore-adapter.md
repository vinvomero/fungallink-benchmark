# NPClassScore threshold-tiered Metcalf adapter

This separately authored adapter ranks every measured-feature candidate by `(class_score > 0.25, standardized_Metcalf_score)`, descending. The class score only selects a tier. It never orders candidates within that tier. Distinct tuples become dense ordinal scores starting at 1; identical tuples remain tied. Canonical candidate IDs determine serialization order only.

The adapter was written from the public [kernel](npclassscore-kernel.md), [baseline](baseline-methods.md), and [evaluator](ranking-evaluator.md) documentation, the kernel manifest, and the original synthetic class table. Its author did not read the kernel, baseline runner, evaluator implementation, or their tests. The adapter imports only the public kernel functions. Its own tests import the evaluator API and supply gold separately. This is an interface-usability demonstration within Phase 4, not another independent substantive method or a fungal validation result.

## Run the synthetic fixture

From the repository root, with Python's standard library:

```powershell
python -S -m unittest tests.test_npclassscore_adapter -v
python -S examples/npclassscore_adapter.py --inputs tests/fixtures/npclassscore/adapter-inputs.json --metcalf-run tests/fixtures/npclassscore/metcalf-run.json --class-table tests/fixtures/npclassscore/class-table.tsv --run-id synthetic-npclass-1 --output npclass-run.json
python -S scripts/evaluate_rankings.py --benchmark tests/fixtures/npclassscore/benchmark.json --run npclass-run.json --output npclass-evaluation.json
```

The Python API is `adapt(inputs, metcalf_run, table, *, run_id)`. Load `table` through `scripts.npclassscore.load_class_table`. Pass a complete precomputed standardized-Metcalf run; the adapter neither imports nor runs a baseline implementation. The output follows the evaluator's run interface and uses method ID `npclassscore_threshold_tiered_metcalf_strict`, version `1`.

## Input schema 1

The root accepts exactly `schema_version` (string `"1"`), `track_id`, `query_type`, `candidate_universe_id`, `candidate_pools`, `queries`, `cohorts`, `expected_class_table_sha256`, and `provenance`. All are required. Query type is `BGC` or `GCF`. Identity fields must match the supplied Metcalf run exactly. Candidate pools contain nonempty lists of unique canonical IDs. IDs are case-sensitive and used literally.

Each query has required `query_id`, `cohort_id`, and `candidate_pool_id`, plus optional `genomic_classes`. Each referenced pool and cohort must exist; query IDs are unique. Genomic annotations follow the kernel's named-level dictionary contract. Each cohort accepts only optional `features`, a dictionary keyed by declared candidate ID. Each feature record accepts only `spectrum_id` and `spectral_classes`. The nominated spectrum ID identifies the supplied class prediction's representative spectrum. There is no spectral selection, predictor invocation, or feature aggregation here.

Absent/null feature tables, records, spectrum IDs, or annotation dictionaries mean unavailable observations. Genomic class lists may be empty; spectral class terms may be null. Supplied non-null values must follow the kernel's types and level names. Empty strings, wrong types, unknown fields, undeclared candidate IDs, and duplicate JSON object keys are errors. Gold fields such as `products` and `targets` are excluded from the annotation schema at every level.

`provenance` contains exactly four nonempty strings: `genomic_classes`, `spectral_class_predictions`, `feature_spectrum_joins`, and `class_reference_exposure`. Describe the actual annotation source/version, prediction pipeline/training source, join provenance, and reference overlap respectively. An explicit `unknown` exposure is accepted. The adapter echoes these declarations; it does not certify their scientific validity. Fixture declarations state that the classes, spectrum joins, and Metcalf scores are invented.

The expected lowercase SHA-256 must match the loaded table's actual-byte digest before scoring. The fixture pins its synthetic table; `.gitattributes` preserves its LF bytes on checkout. For production, use the reference-asset pin in [the kernel manifest](../../data/manifests/npclassscore-method.json), not the synthetic pin. The adapter output records actual and expected hashes, byte size, kernel variant/version, fixed threshold, provenance, and source Metcalf run metadata. Choosing a scientifically appropriate asset remains a release decision.

## Complete pools and unavailable inputs

The supplied Metcalf run must identify `metcalf_standardized`, a nonempty method version and run ID, and `score_direction: "higher"`. It must contain every query exactly once. Each `ok` query must contain finite numeric scores for every candidate exactly once. Partial scores, duplicates, unknown IDs, wrong identities, and malformed values raise `ValueError` before class scoring starts. Existing `abstention`, `input_unavailable`, and `execution_failure` statuses propagate with their nonempty reasons and no scores; class scoring is marked unattempted for these queries.

Each Metcalf output may include `cohort_id` and `candidate_pool_id`. Every supplied identity must match the input query with that `query_id`, even if another pool contains identical candidate IDs. These checks precede status and score validation and also apply to non-output statuses. Outputs that omit these optional fields remain valid.

For valid Metcalf outputs, every candidate gets a class audit, including kernel pair evidence, unknown terms, nominated spectrum ID, and source Metcalf score. Missing spectrum joins or unusable class results make the entire query `input_unavailable`, with no ranking. The audit retains the full pool and candidate-specific reasons. It does not shrink pools or substitute zero. Known class pairs with zero observed counts and a positive denominator remain valid scores, and an all-fail tier still produces a complete Metcalf ranking.

No shared-strain filter or Metcalf cutoff is applied. The upstream workflow filters links above 0.25 rather than returning this full ranking and may retain links with missing class information by default. This adaptation reinserts the failed-threshold tier and requires complete class coverage. The named-ontology kernel also includes ontology index zero and treats unknown vocabulary as unavailable. Supplied annotations bypass upstream class conversions and GCF aggregation. These differences rule out a claim of full upstream workflow equivalence.

The CLI exits 0 when it writes a run, including runs with unavailable queries. Invalid input or file errors exit 2. It serializes first, writes and closes a temporary file beside the destination, then replaces the destination atomically. Write or replacement failure preserves an existing report and attempts temporary-file cleanup. This is not a power-loss durability guarantee. Programming exceptions are not converted into scientific failure statuses.

## Verification record

Before the adapter existed, `python -S -m unittest tests.test_npclassscore_adapter -v` failed with `ModuleNotFoundError: No module named 'examples'`. The focused tests then passed. They cover the exact 0.25 boundary, 0.75 pass, passing low Metcalf scores above failing high scores, ties, class magnitude excluded from secondary ordering, all-fail ranking, valid empirical zero versus unknown vocabulary, full missing-input audits, source failure propagation, malformed runs and annotations, order invariance, input immutability, duplicate JSON keys, CLI operation, replacement failure, and actual evaluator integration with separate multi-product gold.

The published APIs were sufficient. The kernel manifest supplied its exact variant/version, which the interface prose did not identify as an adapter metadata constant. No dependency implementation inspection was needed.

Requested route: `gpt-6-astra` with `medium` reasoning. No serving-side model/effort receipt was exposed to this worker. No biological label was admitted, predictor installed, or real-data experiment run. A general adapter framework, retries, fallbacks, class conversions, and GCF aggregation were considered outside this bounded unit and were not built.
