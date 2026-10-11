# Paired method comparisons

`scripts/compare_rankings.py` evaluates two raw run envelopes against the same benchmark and reports method A minus method B. It calls the public `evaluate` function for both runs. Saved summary reports aren't accepted as inputs. Candidate-universe and track mismatches fail through the evaluator's existing validation.

```powershell
python scripts/compare_rankings.py --benchmark benchmark.json --run-a method-a.json --run-b method-b.json --output comparison.json
```

The Python API is `compare(benchmark, run_a, run_b, cutoffs=(1, 10, 100), predeclared_subset=None)`. Inputs use the evaluator's existing benchmark and run schemas. Neither input is changed. The CLI uses default cutoffs and writes a complete JSON report through a temporary file in the destination directory, then replaces the destination.

The primary comparison includes every benchmark query. Abstention, unavailable inputs, execution failures and invalid outputs receive zero end-to-end retrieval credit, with their status counts retained separately inside `evaluations`. Zero credit describes workflow delivery; it doesn't turn unknown candidates into biological negatives.

Query metrics are averaged within each group/cohort. Those cohort means are averaged within each pathway group, and pathway groups receive equal weight. Repeated groups across cohorts remain a single resampling unit. The comparison uses the evaluator's group means directly; it doesn't flatten query rows or average the methods' separate conditional populations.

Each bootstrap replicate samples as many pathway groups as the benchmark contains, with replacement. The same sampled groups contribute to both methods and every metric. The report includes each group's scores and differences, query and cohort membership, group counts, tied-group counts, interval widths, and leave-one-group-out estimates. Positive differences favor A for these retrieval metrics.

Software defaults are 10,000 draws, seed 20260930, and percentile 95% intervals. Percentiles interpolate linearly at `(draws - 1) * probability` in sorted replicates. The report records the Python version and `random.Random` generator. These defaults implement the proposed analysis settings; they don't establish a scientific freeze. For each metric, the report compares percentile endpoints from the first 5,000 draws with the second 5,000 and gives their maximum absolute difference. This Monte Carlo diagnostic has no pass threshold and doesn't establish sampling validity.

With one pathway group, the across-group interval and the leave-one-group-out estimate are `not_estimable`, with null values. No bootstrap draws run in that case. All intervals are labeled descriptive and conditional on the observed cohorts, candidate pools and curated labels. Few groups can yield discrete or unstable intervals. Group independence still needs a biological judgment; neither a narrow interval nor a fixed group-count threshold establishes broad superiority.

## Declared common inputs

An optional `--predeclared-subset subset.json` adds a separate comparison while retaining the full primary result. The file contains an input-eligibility declaration made before inspecting method outputs:

```json
{
  "name": "shared spectrum-ready inputs",
  "provenance": "input-manifest-v1, declared before method runs",
  "query_ids": ["query-1", "query-2"]
}
```

The API accepts the same object as `predeclared_subset`. IDs must be unique and present in the benchmark. The supplied provenance is recorded; the software cannot establish when it was written. Subset calculations reevaluate the raw runs on that query membership and retain failures. The report lists excluded query IDs and groups, and recalculates the query/cohort/group hierarchy within the declared subset. An empty list reports `not_estimable`, zero membership counts and null estimates; the full primary comparison remains available.

`paired_valid_diagnostic` separately compares the intersection of queries with valid outputs from both methods, after reevaluating that shared membership. It lists omitted queries and groups and reports an empty intersection as `not_estimable`. This outcome-dependent diagnostic has no bootstrap interval and cannot replace the full or declared common-input comparison. The included evaluator reports also retain individual conditional summaries for inspection, but those different denominators must not be subtracted as a paired comparison.

This unit doesn't calculate cohort-specific comparisons, alternate grouping sensitivities, multiplicity adjustments, or significance claims.

Tests use synthetic rankings only. They check unequal query/cohort counts, zero credit for failures, paired covariance, shared draws across metrics, one-group behavior, declared and diagnostic subset membership, empty intersections, reproducibility, and CLI output handling. They provide no empirical evidence about fungal methods or group independence.
