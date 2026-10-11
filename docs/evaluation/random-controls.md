# Repeated uniform random control

`scripts/evaluate_random.py` compares uniform random rankings with exact expected retrieval. It takes the [baseline input contract](baseline-methods.md) and a separate evaluator benchmark. Labels never enter `run_baselines.run_baseline`.

```powershell
python scripts/evaluate_random.py --inputs inputs.json --benchmark benchmark.json --run-id random-v1 --output random-report.json
```

The draft software defaults follow the proposed [analysis plan](../../protocol/analysis-plan.md): seed 20260930, 10,000 initial repeats, and maximum Monte Carlo standard error (MCSE) of 0.001. These settings do not freeze the scientific protocol. Each repeat uses the public uniform random runner and evaluator. One additional evaluation with every candidate tied gives the exact uniform-permutation expectation, including multiple products and capped cutoffs.

Every query must match the benchmark's cohort and complete candidate membership. Identity mismatches, missing queries and incomplete rankings raise an error before the repeat loop. The runner validates all supplied inputs once; subsequent calls receive only the same query, cohort and candidate-pool IDs. This avoids scanning unused strain matrices at every repeat while retaining the public runner's seed contract. Input objects are not changed.

## What the report measures

The report contains all evaluator retrieval metrics for the overall population and each pathway group. It first averages queries within each group/cohort, then cohorts within each group, then groups equally overall. Each metric contains the repeated mean, sample standard deviation (`sample_sd`, denominator R−1), `mcse = sample_sd / sqrt(R)`, exact expectation, and signed mean-minus-exact difference. Online moments retain one run at a time rather than all rankings.

After a batch, the driver checks every reported overall and group metric. If any MCSE exceeds the tolerance, it doubles the completed repeat total and continues with the next unused repeat index. `checkpoints` records each check. `achieved_precision` is the largest final MCSE. The difference from the exact expectation is reported separately; it isn't the stopping criterion.

`exact_queries` contains exact expectations only, with pool sizes, product counts and effective cutoffs. It contains no simulated per-query means or MCSE estimates. Cohort-level repeated summaries are not reported. Query and cohort memberships remain available in the group entries and exact query rows.

The standard deviation describes variability across random rankings of these fixed inputs. MCSE estimates the simulation mean's precision; a tiny custom initial batch can miss rare events and underestimate it. Neither is a confidence interval for biological pathway groups, and this driver does not perform a group bootstrap. A small MCSE does not establish that the benchmark has many independent biological units.

## Reproducing the draws

The report records Python implementation/version, baseline and driver versions, random state version, generator, master seed, elapsed wall time and the completed repeat interval `[0, repeats)`. Each query has a `payload_template` and its first derived seed. To reconstruct any repeat seed, replace the template's third element with that integer repeat index, serialize with `json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')`, take its SHA-256 digest, and convert with `int.from_bytes(digest, 'big')`. This compact seed manifest specifies every query/repeat seed without storing an unbounded list.

The digest includes the track, query type, candidate universe, cohort, pool and query IDs. Run IDs and input row order do not affect draws. For each query, sort canonical candidate IDs and shuffle with `random.Random(derived_seed).shuffle`. Reproduction requires the recorded runtime and runner behavior. The report omits raw rankings; the public baseline runner can regenerate any repeat.

## API and bounded runs

```python
from scripts.evaluate_random import evaluate_random

report = evaluate_random(inputs, benchmark, run_id='random-v1')
```

The API accepts `seed`, `initial_repeats`, `tolerance`, `max_repeats` and evaluator `cutoffs`. The CLI exposes the first four, retaining evaluator default cutoffs 1, 10 and 100. Initial repeats must be at least two; tolerance must be finite and positive. An optional cap must be at least the initial repeat count. There is no default cap.

For a bounded smoke run, use `--initial-repeats 32 --max-repeats 64`. If the cap cuts through the next doubling batch, the driver stops at the cap and still reports all completed draws. A capped result receives `precision_not_achieved` unless every aggregate meets the tolerance. CLI exit code 0 means precision achieved, 3 means the report was saved but precision was not achieved, and 2 means input or output failure. An invalid input preserves any previous output. Successful report writes use atomic replacement.

These synthetic tests exercise the implementation:

```powershell
python -S -m unittest tests.test_evaluate_random -v
```

They check exhaustive four-candidate expectations, public-run repeat means and sample variation, unequal cohort membership, actual adaptive doubling, capped failure, stable seed replay, input separation and the CLI. They provide software evidence; no real benchmark run or biological validation is claimed.
