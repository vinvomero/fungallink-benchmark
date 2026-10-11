import copy
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.run_baselines import METHODS, run_baseline, main
from scripts.evaluate_rankings import evaluate

FIXTURES = Path(__file__).parent / 'fixtures' / 'baselines'


def fixture():
    return json.loads((FIXTURES / 'inputs.json').read_text(encoding='utf-8'))


def scores(run, index=0):
    return {r['candidate_id']: r['score'] for r in run['outputs'][index]['scores']}


class BaselineTests(unittest.TestCase):
    def run_method(self, method, inputs=None, **kwargs):
        return run_baseline(fixture() if inputs is None else inputs, method, run_id='test', **kwargs)

    def test_hand_worked_orientation_and_controls(self):
        # g=[1,1,0,0], a=[1,0,1,0], b=[1,1,0,0], c=[0,0,1,0].
        self.assertEqual(scores(self.run_method('metcalf_raw')), {'a': 1, 'b': 22, 'c': -9, 'd': 2})
        self.assertEqual(scores(self.run_method('prevalence_difference')), {'a': 0, 'b': 1, 'c': -.5, 'd': 0})
        self.assertEqual(scores(self.run_method('global_prevalence')), {'a': .5, 'b': .5, 'c': .25, 'd': 0})
        self.assertEqual(scores(self.run_method('global_abundance')), {'a': 4, 'b': 3, 'c': 2, 'd': 0})
        raw = self.run_method('metcalf_raw')['outputs'][0]['audit']['candidates']['c']
        self.assertEqual([raw[k] for k in ('n11', 'n01', 'n10', 'n00')], [0, 1, 2, 1])

    def test_standardization_against_exhaustive_fixed_size_subsets(self):
        # Independent enumeration uses four table-cell weights, no closed-form moments.
        for n in range(2, 8):
            strains = [f's{i}' for i in range(n)]
            for g in range(1, n):
                genome = [int(i < g) for i in range(n)]
                for m in range(n + 1):
                    subsets = list(itertools.combinations(range(n), m))
                    values = [sum({(1, 1): 10, (0, 1): -10, (1, 0): 0, (0, 0): 1}[(genome[i], int(i in subset))] for i in range(n)) for subset in subsets]
                    mean = sum(values) / len(values)
                    variance = sum((v - mean) ** 2 for v in values) / len(values)
                    inputs = fixture()
                    inputs['candidate_pools'] = {'pool': ['x']}
                    inputs['cohorts'] = {'cohort': {'strain_ids': strains, 'feature_presence': {'x': dict.fromkeys(strains, 0)}}}
                    inputs['queries'] = [{'query_id': 'q1', 'cohort_id': 'cohort', 'candidate_pool_id': 'pool', 'eligible_strain_ids': strains, 'genomic_presence': dict(zip(strains, genome))}]
                    for subset, raw in zip(subsets, values):
                        inputs['cohorts']['cohort']['feature_presence']['x'] = {s: int(i in subset) for i, s in enumerate(strains)}
                        out = self.run_method('metcalf_standardized', inputs)['outputs'][0]
                        audit = out['audit']['candidates']['x']
                        self.assertAlmostEqual(audit['null_mean'], mean, places=11)
                        self.assertAlmostEqual(audit['null_variance'], variance, places=10)
                        self.assertAlmostEqual(out['scores'][0]['score'], (raw - mean) / math.sqrt(variance) if variance else 0, places=11)
                        self.assertEqual(audit['zero_variance'], variance == 0)

    def test_order_invariance_and_no_mutation(self):
        inputs = fixture()
        before = copy.deepcopy(inputs)
        shuffled = copy.deepcopy(inputs)
        shuffled['queries'].reverse()
        for ids in shuffled['candidate_pools'].values():
            ids.reverse()
        for query in shuffled['queries']:
            query['eligible_strain_ids'].reverse()
            query['genomic_presence'] = dict(reversed(list(query['genomic_presence'].items())))
        for cohort in shuffled['cohorts'].values():
            cohort['strain_ids'].reverse()
            for key in ('feature_presence', 'normalized_abundance'):
                cohort[key] = {c: dict(reversed(list(v.items()))) for c, v in reversed(list(cohort[key].items()))}
        for method in METHODS:
            self.assertEqual(self.run_method(method, inputs), self.run_method(method, shuffled))
        self.assertEqual(inputs, before)

    def test_random_is_complete_reproducible_per_query_and_repeat(self):
        inputs = fixture()
        first = self.run_method('uniform_random', inputs, seed=20260930, repeat_index=7)
        self.assertEqual(first['outputs'][0]['audit']['derived_seed'],
                         '112697006274383315512640905900552126492411698824490737725297660868761688535464')
        self.assertEqual(scores(first), {'a': 3, 'b': 1, 'c': 4, 'd': 2})
        self.assertEqual(first, self.run_method('uniform_random', inputs, seed=20260930, repeat_index=7))
        for output in first['outputs']:
            self.assertEqual(set(scores({'outputs': [output]})), {'a', 'b', 'c', 'd'})
            self.assertEqual(sorted(r['score'] for r in output['scores']), [1, 2, 3, 4])
        lone = copy.deepcopy(inputs)
        lone['queries'] = lone['queries'][1:]
        self.assertEqual(first['outputs'][1], self.run_method('uniform_random', lone, seed=20260930, repeat_index=7)['outputs'][0])
        second = self.run_method('uniform_random', inputs, seed=20260930, repeat_index=8)
        self.assertNotEqual(first['outputs'][0]['audit']['derived_seed'], second['outputs'][0]['audit']['derived_seed'])
        self.assertNotEqual(first['outputs'][0]['audit']['derived_seed'], first['outputs'][1]['audit']['derived_seed'])
        self.assertIn('python_version', first['implementation'])
        self.assertEqual(first['parameters']['repeat_index'], 7)

    def test_global_controls_ignore_genomic_presence(self):
        inputs = fixture()
        for method in ('global_prevalence', 'global_abundance', 'uniform_random'):
            before = self.run_method(method, inputs)
            changed = copy.deepcopy(inputs)
            for q in changed['queries']:
                q['genomic_presence'] = None
            self.assertEqual(before, self.run_method(method, changed))

    def test_required_inputs_only_determine_readiness(self):
        for method, needed in [('global_prevalence', 'feature_presence'), ('global_abundance', 'normalized_abundance')]:
            inputs = fixture()
            inputs['queries'][0].pop('genomic_presence')
            inputs['cohorts']['cohort'].pop('normalized_abundance' if needed == 'feature_presence' else 'feature_presence')
            self.assertEqual(self.run_method(method, inputs)['outputs'][0]['status'], 'ok')
        inputs = fixture()
        inputs['cohorts'] = {'cohort': {}}
        for q in inputs['queries']:
            q.pop('eligible_strain_ids')
            q.pop('genomic_presence')
        self.assertTrue(all(o['status'] == 'ok' for o in self.run_method('uniform_random', inputs)['outputs']))
        self.assertEqual(self.run_method('global_prevalence', inputs)['outputs'][0]['status'], 'input_unavailable')

    def test_missing_null_cells_never_become_absence_or_partial_output(self):
        for value in ('missing', None):
            for field, methods in [('feature_presence', ('global_prevalence', 'prevalence_difference', 'metcalf_raw', 'metcalf_standardized')), ('normalized_abundance', ('global_abundance',))]:
                inputs = fixture()
                if value == 'missing':
                    del inputs['cohorts']['cohort'][field]['b']['s1']
                else:
                    inputs['cohorts']['cohort'][field]['b']['s1'] = value
                for method in methods:
                    output = self.run_method(method, inputs)['outputs'][0]
                    self.assertEqual(output['status'], 'input_unavailable')
                    self.assertNotIn('scores', output)
                    self.assertIn('s1', output['reason'])
        inputs = fixture()
        inputs['queries'][0]['genomic_presence']['s1'] = None
        run = self.run_method('metcalf_raw', inputs)
        self.assertEqual([o['status'] for o in run['outputs']], ['input_unavailable', 'ok'])

    def test_degenerate_vectors_and_denominators(self):
        for g in (0, 1):
            inputs = fixture()
            inputs['queries'][0]['genomic_presence'] = dict.fromkeys(['s1', 's2', 's3', 's4'], g)
            for method in ('prevalence_difference', 'metcalf_standardized'):
                output = self.run_method(method, inputs)['outputs'][0]
                self.assertEqual(output['status'], 'abstention')
                self.assertNotIn('scores', output)
            self.assertEqual(self.run_method('metcalf_raw', inputs)['outputs'][0]['status'], 'ok')
        out = self.run_method('metcalf_standardized')['outputs'][0]
        self.assertEqual(scores({'outputs': [out]})['d'], 0)
        self.assertTrue(out['audit']['candidates']['d']['zero_variance'])
        inputs = fixture()
        inputs['queries'][0]['eligible_strain_ids'] = []
        for method in METHODS:
            self.assertEqual(self.run_method(method, inputs)['outputs'][0]['status'], 'ok' if method == 'uniform_random' else 'input_unavailable')

    def test_one_strain_and_large_finite_abundance(self):
        inputs = fixture()
        inputs['queries'][0]['eligible_strain_ids'] = ['s1']
        self.assertEqual(scores(self.run_method('metcalf_raw', inputs)), {'a': 10, 'b': 10, 'c': 0, 'd': 0})
        self.assertEqual(self.run_method('metcalf_standardized', inputs)['outputs'][0]['status'], 'abstention')
        inputs = fixture()
        inputs['cohorts']['cohort']['normalized_abundance']['a'] = dict.fromkeys(inputs['cohorts']['cohort']['strain_ids'], sys.float_info.max)
        self.assertEqual(scores(self.run_method('global_abundance', inputs))['a'], sys.float_info.max)

    def test_missing_tables_candidates_and_genomic_cells(self):
        for mutate in (
            lambda d: d['cohorts']['cohort'].pop('feature_presence'),
            lambda d: d['cohorts']['cohort'].update(feature_presence=None),
            lambda d: d['cohorts']['cohort']['feature_presence'].pop('a'),
            lambda d: d['cohorts']['cohort']['feature_presence'].update(a=None),
            lambda d: d['queries'][0]['genomic_presence'].pop('s1'),
        ):
            inputs = fixture()
            mutate(inputs)
            output = self.run_method('metcalf_raw', inputs)['outputs'][0]
            self.assertEqual(output['status'], 'input_unavailable')
            self.assertNotIn('scores', output)

    def test_malformed_input_rejected(self):
        changes = [
            lambda d: d['candidate_pools']['pool'].append('a'),
            lambda d: d['candidate_pools'].update(pool=[]),
            lambda d: d['queries'].append(copy.deepcopy(d['queries'][0])),
            lambda d: d['queries'][0].update(cohort_id='unknown'),
            lambda d: d['queries'][0].update(candidate_pool_id='unknown'),
            lambda d: d['queries'][0].update(eligible_strain_ids=['s1', 's1']),
            lambda d: d['queries'][0].update(eligible_strain_ids=['unknown']),
            lambda d: d['queries'][0].update(products={'gold': ['a']}),
            lambda d: d['cohorts']['cohort']['feature_presence']['a'].update(s1=2),
            lambda d: d['cohorts']['cohort']['feature_presence']['a'].update(unknown=1),
            lambda d: d['cohorts']['cohort']['feature_presence'].update(unknown={'s1': 1}),
            lambda d: d['cohorts']['cohort']['normalized_abundance'].update(a=[]),
            lambda d: d['queries'][0].update(genomic_presence={'s1': 'unknown'}),
        ]
        for change in changes:
            inputs = fixture()
            change(inputs)
            with self.assertRaises(ValueError):
                self.run_method('uniform_random', inputs)
        for value in (-1, float('nan'), float('inf'), True, '2'):
            inputs = fixture()
            inputs['cohorts']['cohort']['normalized_abundance']['a']['s1'] = value
            with self.assertRaises(ValueError):
                self.run_method('global_abundance', inputs)
        for kwargs in ({'seed': True}, {'repeat_index': -1}, {'repeat_index': 1.5}):
            with self.assertRaises(ValueError):
                self.run_method('uniform_random', **kwargs)

    def test_evaluator_integration_uses_separate_shuffled_multi_product_gold(self):
        gold = json.loads((FIXTURES / 'benchmark.json').read_text(encoding='utf-8'))
        for method in METHODS:
            result = evaluate(gold, self.run_method(method), cutoffs=(1, 2, 4))
            self.assertEqual(result['summary']['status_counts']['valid_output'], 2)
        result = evaluate(gold, self.run_method('metcalf_raw'), cutoffs=(1, 2, 4))
        self.assertEqual(result['queries'][0]['metrics']['all_products@2'], 1)
        self.assertEqual(result['queries'][0]['metrics']['product_recovery@1'], .5)

    def test_cli_atomic_replacement_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'run.json'
            dest.write_text('old', encoding='utf-8')
            command = [sys.executable, '-S', 'scripts/run_baselines.py', '--inputs', str(FIXTURES / 'inputs.json'), '--method', 'metcalf_raw', '--run-id', 'cli', '--output', str(dest)]
            done = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(json.loads(dest.read_text())['run_id'], 'cli')
            self.assertEqual(list(Path(directory).iterdir()), [dest])
            bad = Path(directory) / 'bad.json'
            bad.write_text('{"queries": [], "queries": []}', encoding='utf-8')
            command[command.index('--inputs') + 1] = str(bad)
            before = dest.read_bytes()
            done = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(done.returncode, 2)
            self.assertIn('duplicate JSON', done.stderr)
            self.assertEqual(dest.read_bytes(), before)

    def test_failed_replacement_preserves_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'run.json'
            dest.write_bytes(b'previous')
            argv = ['run_baselines.py', '--inputs', str(FIXTURES / 'inputs.json'), '--method', 'uniform_random', '--run-id', 'cli', '--output', str(dest)]
            with patch.object(sys, 'argv', argv), patch('scripts.run_baselines.os.replace', side_effect=OSError('injected')):
                with self.assertRaises(SystemExit) as raised:
                    main()
            self.assertEqual(raised.exception.code, 2)
            self.assertEqual(dest.read_bytes(), b'previous')
            self.assertEqual(list(Path(directory).iterdir()), [dest])


if __name__ == '__main__':
    unittest.main()
