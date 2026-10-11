# Ranking evaluator

This implementation covers a bounded part of Phase 4 of the [project plan](../plans/2026-09-30-2052-benchmark-paper-plan.md): complete ranking validation, tie-aware retrieval metrics, and hierarchical summaries. It uses synthetic fixtures. It does not admit biological labels, freeze the analysis protocol, or report benchmark results.

The Python standard library is sufficient. From the repository root:

```powershell
python -m unittest tests.test_evaluate_rankings -v
python scripts/evaluate_rankings.py --benchmark tests/fixtures/evaluator/benchmark.json --run tests/fixtures/evaluator/run.json --output ranking-example.json
```

The output directory must exist. The CLI serializes JSON first, writes a temporary file in that directory, and closes it before atomically replacing the named destination with `os.replace`. A write, flush, close, or replacement failure leaves an existing report intact; the CLI attempts to remove the temporary file on failure. Cleanup can itself fail if the filesystem refuses deletion, and abrupt process termination can leave a temporary file. This is an atomic replacement, not a power-loss durability guarantee: the CLI doesn't synchronize file or directory contents to storage. It exits 0 when a report was produced, including a report with invalid query outputs. Invalid gold, invalid run identities, unknown or duplicate query IDs, malformed JSON, and file errors exit 2. Inspect `summary.status_counts` before interpreting a successful CLI exit as successful method execution.

## Separate gold and method output

`evaluate(benchmark, run, cutoffs=(1, 10, 100))` in `scripts/evaluate_rankings.py` returns a JSON-compatible dictionary. It doesn't mutate its inputs. The Python API accepts other distinct positive integer cutoffs for fixture checks; the CLI uses 1, 10 and 100.

A benchmark is one comparison population with nonempty string identities:

```json
{
  "track_id": "synthetic-feature",
  "query_type": "GCF",
  "candidate_universe_id": "synthetic-four-v1",
  "queries": [{
    "query_id": "q1",
    "group_id": "group1",
    "cohort_id": "cohort1",
    "candidate_ids": ["a", "b", "c", "d"],
    "products": {"product1": ["a"], "product2": ["b"]}
  }]
}
```

Each query needs a nonempty candidate set and at least one nonempty product target set wholly inside that candidate set. Candidate lists may differ between queries, but all belong to the identified release. Candidate, query and product IDs are canonical, case-sensitive strings. There is no alias normalization. Duplicate candidate IDs or duplicate IDs within a product are rejected. All product sets must be disjoint: adjudicate an ambiguous feature into one target before scoring. Multiple distinct measured ions of one product go in that product's target list; they aren't independent products.

The method receives candidate IDs and permitted method inputs separately. Keep this benchmark object, which contains gold targets, out of method inputs. The evaluator consumes an independently prepared method run:

```json
{
  "method_id": "synthetic-all-tied",
  "method_version": "1",
  "run_id": "example-1",
  "track_id": "synthetic-feature",
  "query_type": "GCF",
  "candidate_universe_id": "synthetic-four-v1",
  "score_direction": "higher",
  "outputs": [{
    "query_id": "q1",
    "status": "ok",
    "scores": [
      {"candidate_id": "c", "score": 0},
      {"candidate_id": "a", "score": 0},
      {"candidate_id": "d", "score": 0},
      {"candidate_id": "b", "score": 0}
    ]
  }]
}
```

Method/run IDs and version identify the whole run; the surrounding query object supplies the query ID for each score row. Scores therefore inherit those IDs instead of repeating them. Track, query type and candidate-universe identities must exactly match the benchmark. A run has one score direction, `higher` or `lower`. Scores must be finite JSON numbers, excluding booleans and numeric strings. Equal parsed numeric values tie; no tolerance or rounding is applied. Python integers retain their exact values; JSON fractional/exponent numbers use Python's binary floating-point parsing. An adapter needing different precision must serialize scores according to its declared method convention before evaluation.

An `ok` query must return each candidate exactly once. Unknown IDs, duplicate IDs, missing candidates, malformed score rows and nonfinite scores produce `invalid_output` with a reason for that query. A missing query output also produces `invalid_output`; partial rankings are never completed by the evaluator. Unknown or duplicate query IDs invalidate the run envelope and raise `ValueError`, because they don't define a unique output for the frozen query population. Duplicate JSON object keys are rejected by the CLI rather than silently overwritten.

An explicit non-output has one of these forms and must omit `scores`:

```json
{"query_id": "q1", "status": "abstention", "reason": "no genomic variation"}
```

`input_unavailable` and `execution_failure` use the same structure. Reasons must be nonempty strings. These statuses remain distinct from `invalid_output`. `valid_output` and `invalid_output` are evaluator result statuses, not adapter input statuses. This interface evaluates a declared runnable method; whole-method unavailability belongs in the method roster, outside this ranking report.

## Tie expectations and bounds

All reported retrieval scores average over uniform permutations within each equal-score block. Candidates in different blocks keep their order. Let the first block containing a target have `a` candidates above it, `t` tied candidates and `p` targets. For cutoff `k`, cap it at the query's pool size and set `r = min(t, max(0, k-a))`:

```text
hit@k = 1 - choose(t-p, r) / choose(t, r)
rr = sum over u=1..t-p+1 of choose(t-u, p-1) / choose(t,p) / (a+u)
first-positive rank bounds = [a+1, a+t-p+1]
```

The implementation computes hit credit with integer combinatorial counts. RR uses a recurrence for the same first-positive probability mass and `math.fsum`; it never substitutes the reciprocal of a mean rank. JSON metrics are floating-point approximations to these analytic expectations, not arbitrary-precision rational outputs. The RR recurrence costs O(t) per target set; probabilities far below floating-point range may underflow without changing a representable score materially.

`product_recovery@k` is the average hit credit across distinct product target sets within that query. `all_products@k` is the joint probability that every product is recovered. For its boundary block, discard products already recovered above the cutoff and let `p_j` count boundary candidates for each remaining product. Count size-r subsets with the coefficient of `x^r` in:

```text
(1+x)^other * product_j ((1+x)^p_j - 1)
```

Divide by `choose(t,r)`. This polynomial counting uses integer arithmetic and O(J r²) arithmetic operations in the worst case, with O(r) working storage. Here J is the number of remaining products and r is the selected portion of the boundary block. Products missing from that block get zero all-products credit; an empty remaining set gets one. When every remaining product occurs in a fully selected boundary block (`r == t`), expectation and both bounds are one, so the evaluator skips polynomial counting. With CLI cutoffs, r never exceeds 100. Sorting scores costs O(N log N).

Each valid query reports any-hit and RR bounds plus per-product first-target rank bounds and expected RR. Binary all-products bounds describe feasible whole permutations: best credit is one exactly when every remaining product is present and r can select at least one of each; worst credit is one exactly when every remaining product is unavoidable among r selected candidates. Bounds are pointwise by metric/cutoff, not claims that one ordering jointly attains every reported bound. No bounds on average product recovery are supplied.

The all-tied four-candidate fixture with two singleton products yields hit@1 = 1/2, hit@2 = 5/6, RR = 13/18, product recovery@2 = 1/2 and all-products@2 = 1/6. Tests also enumerate all permutations consistent with 48 tiny score/product configurations and compare expected values and feasible any/all/RR bounds at four cutoffs.

## Reading the report

The report repeats run identities and lists per-query pool sizes, product counts, effective cutoffs, output statuses and reasons. For valid rankings, `metrics`, `metric_bounds`, `first_positive_rank` and `products` contain retrieval results. Those fields are null for non-outputs: their ranks weren't observed.

Aggregation averages queries within each pathway-group/cohort pair, then cohort means within each pathway group, then group means with equal group weight. `cohorts` therefore contains group/cohort pairs, not a pooled study score. Each record lists membership IDs and counts so repeated groups across cohorts remain visible. Products are already averaged inside query metrics before this hierarchy.

`conditional` uses valid outputs only. A cohort or group without any valid output has null conditional metrics and `estimability: "not_estimable"`; it is omitted when averaging its parent's conditional metrics. This is an outcome-dependent diagnostic. Counts of covered groups and cohorts expose those omissions. `end_to_end` retains every query and assigns zero retrieval credit to all four non-output statuses. That zero records failure to deliver retrieval, not a target rank or a biological negative.

Every aggregation level includes plain query status counts/rates and `coverage` (valid queries divided by all queries). `hierarchical_status_rates` and `hierarchical_coverage` follow the same cohort-then-group weighting as end-to-end scores. At the overall level, `group_coverage` is the fraction of pathway groups with at least one valid output. `summary.pool_sizes` and `summary.capped_query_counts` report all eligible queries, including failures.

## Implementation evidence and limits

The first test run, before the evaluator existed, was `python -m unittest tests.test_evaluate_rankings -v`. It exited 1 with `ModuleNotFoundError: No module named 'scripts.evaluate_rankings'`. Tests now cover the hand calculations, independent exhaustive permutations, shuffled candidate and query IDs, grouped ions, reversed score direction, exact equality, cutoff-spanning ties, non-output statuses, malformed/partial outputs, invalid gold/envelopes, duplicate JSON keys, unequal cohort/group sizes, empty conditional estimates, and the file-based CLI fixture.

The focused command `python -S -m unittest tests.test_evaluate_rankings -v` passed all 18 tests on 2026-10-01. The added checks distinguish scores on non-outputs from empty reasons, verify conditional means with unequal covered cohorts and groups, and exercise fully selected boundary blocks both with and without a product below the cutoff. A 9,339-candidate all-tied API fixture with three singleton products checks full-pool recovery without a timing assertion.

Before the report-write fix, a regression through `main()` wrote and flushed 17 characters to a real existing destination, then injected an `OSError` at the file-write boundary. It failed because those characters replaced the previous report. That test now passes. A separate injected replacement failure preserves the previous bytes and removes the completed temporary report; the subprocess CLI test also checks successful replacement of an existing report. Both failure tests check for leftover temporary files.

The review's validated pre-fix timing for the 9,339-candidate fixture at cutoff 9,339 was 5.020 seconds. After the full-boundary shortcut, a separate API smoke check with reversed score rows completed in 0.011601 seconds at that cutoff and 0.011390 seconds at the default cutoffs. These are local scale checks, not portable timing guarantees or biological benchmark results. The independent exhaustive permutation tests still cover all 48 tiny score/product configurations at four cutoffs.

The requested implementation route was `gpt-6-astra` with `medium` reasoning. No serving-side model/effort receipt was exposed to this worker.

This unit does not implement bootstrap intervals, baselines, paired method contrasts, common-subset construction, exposure stratification, resource measurements, adapters, or real-data experiments. Release manifests must supply scientifically reviewed eligibility, provenance and exposure records. The evaluator validates the supplied scoring population's structure; it can't verify those scientific decisions or establish that unresolved candidates are negatives.
