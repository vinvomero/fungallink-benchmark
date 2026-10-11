"""Repeated random controls checked against permutations and public runner draws."""
import copy
import itertools
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.evaluate_random import evaluate_random, main
from scripts.evaluate_rankings import evaluate
from scripts.run_baselines import run_baseline


def fixture():
    identity = dict(track_id='feature', query_type='GCF', candidate_universe_id='tiny')
    inputs = dict(schema_version='1', **identity, candidate_pools={'pool': list('abcd')},
                  cohorts={'c1': {}, 'c2': {}}, queries=[])
    benchmark = dict(**identity, queries=[])
    for qid, group, cohort, products in [('q1', 'g1', 'c1', {'p1': ['a'], 'p2': ['b']}),
                                          ('q2', 'g1', 'c1', {'p': ['c']}),
                                          ('q3', 'g1', 'c2', {'p': ['a', 'b']}),
                                          ('q4', 'g2', 'c1', {'p': ['d']})]:
        inputs['queries'].append(dict(query_id=qid, cohort_id=cohort, candidate_pool_id='pool'))
        benchmark['queries'].append(dict(query_id=qid, group_id=group, cohort_id=cohort,
                                         candidate_ids=list('abcd'), products=products))
    return inputs, benchmark


class RandomControlTests(unittest.TestCase):
    def test_exact_expectations_match_exhaustive_permutations(self):
        inputs, benchmark = fixture()
        inputs['queries'] = inputs['queries'][:1]
        benchmark['queries'] = benchmark['queries'][:1]
        result = evaluate_random(inputs, benchmark, run_id='exact', initial_repeats=4, tolerance=1, cutoffs=(1, 2))
        exact = result['overall']['metrics']
        self.assertAlmostEqual(exact['rr']['exact_expectation'], 13 / 18)
        self.assertEqual(exact['hit@1']['exact_expectation'], .5)
        values = []
        for order in itertools.permutations('abcd'):
            ranks = [order.index(c) + 1 for c in 'ab']
            values.append(dict(rr=1/min(ranks), **{'hit@2': float(min(ranks) <= 2),
                           'product_recovery@2': sum(r <= 2 for r in ranks)/2,
                           'all_products@2': float(max(ranks) <= 2)}))
        for metric in values[0]:
            self.assertAlmostEqual(exact[metric]['exact_expectation'], statistics.mean(v[metric] for v in values))

    def test_online_moments_match_independent_public_runs_and_weighting(self):
        inputs, benchmark = fixture()
        result = evaluate_random(inputs, benchmark, run_id='moments', initial_repeats=32, tolerance=1)
        draws = [evaluate(benchmark, run_baseline(inputs, 'uniform_random', run_id='oracle', repeat_index=i)) for i in range(32)]
        for aggregate, extract in [(result['overall'], lambda d: d['summary'])] + [
                (g, lambda d, gid=g['group_id']: next(x for x in d['groups'] if x['group_id'] == gid)) for g in result['groups']]:
            for name, stats in aggregate['metrics'].items():
                values = [extract(d)['end_to_end']['metrics'][name] for d in draws]
                self.assertAlmostEqual(stats['mean'], statistics.mean(values))
                self.assertAlmostEqual(stats['sample_sd'], statistics.stdev(values))
                self.assertAlmostEqual(stats['mcse'], statistics.stdev(values)/math.sqrt(32))
                self.assertAlmostEqual(stats['difference_from_exact'], stats['mean']-stats['exact_expectation'])
        self.assertEqual(result['overall']['query_count'], 4)
        # g1 averages the c1 two-query mean and c2 mean; g2 has one query.
        self.assertAlmostEqual(result['overall']['metrics']['hit@1']['exact_expectation'], (.375 + .5)/4 + .25/2)

    def test_adaptive_doubling_uses_actual_precision_for_every_group(self):
        inputs, benchmark = fixture()
        tolerance = .08
        n = 8
        while True:
            draws = [evaluate(benchmark, run_baseline(inputs, 'uniform_random', run_id='oracle', repeat_index=i)) for i in range(n)]
            worst = max(statistics.stdev([d['groups'][j]['end_to_end']['metrics'][k] for d in draws])/math.sqrt(n)
                        for j in range(2) for k in draws[0]['groups'][0]['end_to_end']['metrics'])
            if worst <= tolerance:
                break
            n *= 2
        self.assertGreater(n, 8)
        result = evaluate_random(inputs, benchmark, run_id='adaptive', initial_repeats=8, tolerance=tolerance)
        self.assertEqual(result['repeats'], n)
        self.assertEqual(result['status'], 'precision_achieved')
        self.assertAlmostEqual(result['achieved_precision'], worst)
        capped = evaluate_random(inputs, benchmark, run_id='capped', initial_repeats=8, tolerance=.0001, max_repeats=11)
        self.assertEqual(capped['repeats'], 11)
        self.assertEqual(capped['status'], 'precision_not_achieved')

    def test_order_seed_manifest_and_no_mutation(self):
        inputs, benchmark = fixture()
        before = copy.deepcopy((inputs, benchmark))
        a = evaluate_random(inputs, benchmark, run_id='stable', initial_repeats=8, tolerance=1)
        self.assertEqual((inputs, benchmark), before)
        inputs['queries'].reverse()
        inputs['candidate_pools']['pool'].reverse()
        benchmark['queries'].reverse()
        b = evaluate_random(inputs, benchmark, run_id='stable', initial_repeats=8, tolerance=1)
        a.pop('elapsed_seconds'); b.pop('elapsed_seconds')
        self.assertEqual(a, b)
        import hashlib
        import random
        for row in a['seeds']['queries']:
            for repeat in (0, 7):
                payload = row['payload_template'].copy()
                payload[2] = repeat
                seed = int.from_bytes(hashlib.sha256(json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode()).digest(), 'big')
                ordering = sorted('abcd')
                random.Random(seed).shuffle(ordering)
                run = run_baseline(inputs, 'uniform_random', run_id='replay', repeat_index=repeat)
                out = next(o for o in run['outputs'] if o['query_id'] == row['query_id'])
                self.assertEqual(str(seed), out['audit']['derived_seed'])
                self.assertEqual(ordering, [s['candidate_id'] for s in sorted(out['scores'], key=lambda x: -x['score'])])

    def test_membership_and_malformed_inputs_rejected_before_repeat_loop(self):
        for change in ('missing_query', 'extra_query', 'candidate', 'cohort', 'identity', 'malformed_table'):
            inputs, benchmark = fixture()
            if change == 'missing_query': inputs['queries'].pop()
            if change == 'extra_query': benchmark['queries'].pop()
            if change == 'candidate': inputs['candidate_pools']['pool'].pop()
            if change == 'cohort': inputs['queries'][0]['cohort_id'] = 'c2'
            if change == 'identity': benchmark['track_id'] = 'other'
            if change == 'malformed_table': inputs['cohorts']['c1']['feature_presence'] = {'a': {'strain': 2}}
            with self.subTest(change=change), patch('scripts.evaluate_random.run_baseline', wraps=run_baseline) as runner:
                with self.assertRaises(ValueError):
                    evaluate_random(inputs, benchmark, run_id='bad', initial_repeats=10)
                self.assertLessEqual(runner.call_count, 1)

    def test_method_boundary_is_gold_free_and_projects_only_after_validation(self):
        inputs, benchmark = fixture()
        inputs['cohorts']['c1']['normalized_abundance'] = {'a': {'strain': 42}}
        seen = []
        def capture(supplied, *args, **kwargs):
            seen.append(copy.deepcopy(supplied))
            return run_baseline(supplied, *args, **kwargs)
        with patch('scripts.evaluate_random.run_baseline', side_effect=capture):
            evaluate_random(inputs, benchmark, run_id='boundary', initial_repeats=4, tolerance=1)
        self.assertEqual(seen[0], inputs)
        for supplied in seen:
            self.assertFalse(any('products' in q or 'group_id' in q for q in supplied['queries']))
        self.assertTrue(all(c == {} for supplied in seen[1:] for c in supplied['cohorts'].values()))

    def test_invalid_precision_settings_rejected(self):
        for kwargs in (dict(initial_repeats=1), dict(initial_repeats=True), dict(tolerance=0),
                       dict(tolerance=float('nan')), dict(tolerance=True), dict(max_repeats=3)):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                evaluate_random(*fixture(), run_id='invalid', **kwargs)

    def test_execution_failure_after_first_draw_rejects_report(self):
        inputs, benchmark = fixture()

        def fail_second_draw(supplied, *args, **kwargs):
            run = run_baseline(supplied, *args, **kwargs)
            if kwargs['repeat_index'] == 1:
                output = next(o for o in run['outputs'] if o['query_id'] == 'q3')
                output.update(status='execution_failure', reason='injected failure')
                output.pop('scores')
            return run

        with patch('scripts.evaluate_random.run_baseline', side_effect=fail_second_draw) as runner:
            with self.assertRaisesRegex(ValueError, 'complete valid rankings.*q3'):
                evaluate_random(inputs, benchmark, run_id='failed-draw', initial_repeats=4, tolerance=1)
        self.assertEqual([call.kwargs['repeat_index'] for call in runner.call_args_list], [0, 1])

    def test_cli_atomic_output_and_nonconvergence_exit(self):
        inputs, benchmark = fixture()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'inputs.json').write_text(json.dumps(inputs))
            (root/'benchmark.json').write_text(json.dumps(benchmark))
            args = [sys.executable, 'scripts/evaluate_random.py', '--inputs', str(root/'inputs.json'),
                    '--benchmark', str(root/'benchmark.json'), '--run-id', 'cli', '--output', str(root/'out.json'),
                    '--initial-repeats', '8', '--max-repeats', '8', '--tolerance', '.0001']
            run = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(run.returncode, 3, run.stderr)
            self.assertEqual(json.loads((root/'out.json').read_text())['status'], 'precision_not_achieved')
            old = (root/'out.json').read_bytes()
            (root/'inputs.json').write_text('{}')
            run = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual((root/'out.json').read_bytes(), old)
            self.assertFalse(list(root.glob('*.tmp')))

    def test_failed_replacement_preserves_destination_and_cleans_temporary_file(self):
        inputs, benchmark = fixture()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'inputs.json').write_text(json.dumps(inputs), encoding='utf-8')
            (root/'benchmark.json').write_text(json.dumps(benchmark), encoding='utf-8')
            dest = root/'out.json'
            dest.write_bytes(b'previous report\r\n')
            argv = ['evaluate_random.py', '--inputs', str(root/'inputs.json'),
                    '--benchmark', str(root/'benchmark.json'), '--run-id', 'cli', '--output', str(dest),
                    '--initial-repeats', '2', '--tolerance', '1']
            temporary_paths = []

            def fail_replace(source, destination):
                temporary_paths.append(Path(source))
                self.assertEqual(destination, dest)
                self.assertEqual(Path(source).parent, root)
                self.assertEqual(json.loads(Path(source).read_text(encoding='utf-8'))['run_id'], 'cli')
                raise OSError('injected replacement failure')

            with patch.object(sys, 'argv', argv), patch('scripts.evaluate_random.os.replace', side_effect=fail_replace) as replace:
                with self.assertRaises(SystemExit) as raised:
                    main()
            replace.assert_called_once()
            self.assertEqual(raised.exception.code, 2)
            self.assertEqual(dest.read_bytes(), b'previous report\r\n')
            self.assertFalse(temporary_paths[0].exists())
            self.assertEqual(set(root.iterdir()), {root/'inputs.json', root/'benchmark.json', dest})


if __name__ == '__main__':
    unittest.main()
