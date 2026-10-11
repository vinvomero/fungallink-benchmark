"""Compare repeated uniform random rankings with exact all-tied expectations."""
import argparse
import copy
import json
import math
import os
from pathlib import Path
import tempfile
import time

try:
    from .run_baselines import run_baseline, seed_payload, IDENTITIES, _json_object
    from .evaluate_rankings import evaluate
except ImportError:  # Direct script execution.
    from run_baselines import run_baseline, seed_payload, IDENTITIES, _json_object
    from evaluate_rankings import evaluate


VERSION = '0.1.0'


class _Moments:
    def __init__(self):
        self.n = 0
        self.mean = 0.0
        self.m2 = 0.0

    def add(self, value):
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)

    def report(self, exact):
        sd = math.sqrt(max(0.0, self.m2) / (self.n - 1))
        return dict(mean=self.mean, sample_sd=sd, mcse=sd / math.sqrt(self.n),
                    exact_expectation=exact, difference_from_exact=self.mean - exact)


def _complete(report):
    failures = [q['query_id'] for q in report['queries'] if q['status'] != 'valid_output']
    if failures:
        raise ValueError('random control requires complete valid rankings for every query: ' + ', '.join(failures))


def evaluate_random(inputs, benchmark, *, run_id, seed=20260930, initial_repeats=10000,
                    tolerance=.001, max_repeats=None, cutoffs=(1, 10, 100)):
    """Estimate ranking variability with online moments and adaptive doubling.

    The separate benchmark is passed only to the evaluator. Every reported
    overall/group metric must meet the MCSE tolerance. A supplied repeat cap
    returns precision_not_achieved if it prevents reaching that tolerance.
    """
    started = time.perf_counter()
    if type(initial_repeats) is not int or initial_repeats < 2:
        raise ValueError('initial_repeats must be an integer of at least 2')
    if isinstance(tolerance, bool) or not isinstance(tolerance, (float, int)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError('tolerance must be finite and positive')
    if max_repeats is not None and (type(max_repeats) is not int or max_repeats < initial_repeats):
        raise ValueError('max_repeats must be an integer at least initial_repeats')
    cutoffs = tuple(cutoffs)
    # The public runner validates every supplied table once, including fields
    # random ranking doesn't need. Never hide malformed data by projecting first.
    first = run_baseline(inputs, 'uniform_random', run_id=run_id, seed=seed, repeat_index=0)
    first_report = evaluate(benchmark, first, cutoffs=cutoffs)
    _complete(first_report)
    gold = {q['query_id']: q for q in benchmark['queries']}
    if set(gold) != {q['query_id'] for q in inputs['queries']}:
        raise ValueError('input query membership does not match benchmark')
    for query in inputs['queries']:
        target = gold[query['query_id']]
        if query['cohort_id'] != target['cohort_id']:
            raise ValueError(f"query {query['query_id']}: cohort membership does not match benchmark")
        if set(inputs['candidate_pools'][query['candidate_pool_id']]) != set(target['candidate_ids']):
            raise ValueError(f"query {query['query_id']}: candidate membership does not match benchmark")
    # Uniform ranking needs IDs alone. Public validation still runs for each
    # projected input; omitting cohort matrices avoids repeated table scans.
    random_inputs = dict(schema_version=inputs['schema_version'], **{k: inputs[k] for k in IDENTITIES},
                         candidate_pools=inputs['candidate_pools'], cohorts={c: {} for c in inputs['cohorts']},
                         queries=[{k: q[k] for k in ('query_id', 'cohort_id', 'candidate_pool_id')} for q in inputs['queries']])
    tied = copy.deepcopy(first)
    tied.update(method_id='exact_uniform_expectation', run_id=run_id + ':exact')
    for output in tied['outputs']:
        for row in output['scores']:
            row['score'] = 0
    exact = evaluate(benchmark, tied, cutoffs=cutoffs)
    _complete(exact)
    exact_aggregates = [exact['summary'], *exact['groups']]
    moments = [{name: _Moments() for name in aggregate['end_to_end']['metrics']} for aggregate in exact_aggregates]

    completed = 0
    target = initial_repeats
    checkpoints = []
    while True:
        while completed < target:
            if completed == 0:
                report = first_report
            else:
                run = run_baseline(random_inputs, 'uniform_random', run_id=run_id,
                                   seed=seed, repeat_index=completed)
                report = evaluate(benchmark, run, cutoffs=cutoffs)
                _complete(report)
            for stats, aggregate in zip(moments, [report['summary'], *report['groups']]):
                for name, value in aggregate['end_to_end']['metrics'].items():
                    stats[name].add(value)
            completed += 1
        summaries = []
        for stats, aggregate in zip(moments, exact_aggregates):
            summaries.append(dict(query_count=aggregate['query_count'],
                                  metrics={name: moment.report(aggregate['end_to_end']['metrics'][name])
                                           for name, moment in stats.items()}))
        precision = max(s['mcse'] for a in summaries for s in a['metrics'].values())
        checkpoints.append(dict(repeats=completed, max_mcse=precision))
        if precision <= tolerance or (max_repeats is not None and completed >= max_repeats):
            break
        target = completed * 2
        if max_repeats is not None:
            target = min(target, max_repeats)

    summaries[0].update(group_count=exact['summary']['group_count'],
                        group_cohort_count=exact['summary']['group_cohort_count'])
    for summary, group in zip(summaries[1:], exact['groups']):
        summary.update({key: group[key] for key in ('group_id', 'cohort_count', 'cohort_ids', 'query_ids')})
    seed_rows = []
    for output in first['outputs']:
        seed_rows.append(dict(query_id=output['query_id'], first_derived_seed=output['audit']['derived_seed'],
                              payload_template=seed_payload(inputs, output, seed, '{repeat_index}')))
    return dict(schema_version='1', **{k: inputs[k] for k in IDENTITIES}, run_id=run_id,
                method_id='uniform_random', method_version=first['method_version'], driver_version=VERSION,
                status='precision_achieved' if precision <= tolerance else 'precision_not_achieved',
                repeats=completed, initial_repeats=initial_repeats, max_repeats=max_repeats,
                tolerance=tolerance, achieved_precision=precision, checkpoints=checkpoints,
                cutoffs=exact['cutoffs'], overall=summaries[0], groups=summaries[1:],
                exact_queries=[{key: q[key] for key in ('query_id', 'group_id', 'cohort_id', 'pool_size',
                                                       'product_count', 'effective_cutoffs', 'metrics')}
                               for q in exact['queries']],
                pool_sizes=exact['summary']['pool_sizes'], capped_query_counts=exact['summary']['capped_query_counts'],
                weighting='query mean within group/cohort; equal cohort mean within group; equal group mean overall',
                variability='sample SD across random rankings; MCSE is SD/sqrt(repeats), not biological group uncertainty',
                seeds=dict(master_seed=seed, repeat_index_start=0, repeat_index_stop_exclusive=completed,
                           derivation=first['parameters']['seed_derivation'],
                           encoding='UTF-8 JSON array; ensure_ascii=False; separators=(comma,colon); SHA-256 digest as big-endian integer',
                           candidate_order=first['parameters']['candidate_order'],
                           generator=first['parameters']['generator'], queries=seed_rows),
                implementation=first['implementation'], elapsed_seconds=time.perf_counter() - started)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', required=True, type=Path)
    parser.add_argument('--benchmark', required=True, type=Path)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--seed', type=int, default=20260930)
    parser.add_argument('--initial-repeats', type=int, default=10000)
    parser.add_argument('--tolerance', type=float, default=.001)
    parser.add_argument('--max-repeats', type=int)
    args = parser.parse_args()
    try:
        inputs = json.loads(args.inputs.read_text(encoding='utf-8'), object_pairs_hook=_json_object)
        benchmark = json.loads(args.benchmark.read_text(encoding='utf-8'), object_pairs_hook=_json_object)
        result = evaluate_random(inputs, benchmark, run_id=args.run_id, seed=args.seed,
                                 initial_repeats=args.initial_repeats, tolerance=args.tolerance,
                                 max_repeats=args.max_repeats)
        serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=args.output.parent,
                                             prefix=f'.{args.output.name}.', suffix='.tmp', delete=False) as report:
                temporary = Path(report.name)
                report.write(serialized)
            os.replace(temporary, args.output)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'random evaluation error: {exc}\n')
    if result['status'] != 'precision_achieved':
        parser.exit(3, 'random evaluation: repeat cap reached before requested precision\n')


if __name__ == '__main__':
    main()
