import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from examples.npclassscore_adapter import adapt, main
from scripts.npclassscore import load_class_table
from scripts.evaluate_rankings import evaluate

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / 'tests/fixtures/npclassscore'


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.inputs = json.loads((FIX / 'adapter-inputs.json').read_text())
        self.baseline = json.loads((FIX / 'metcalf-run.json').read_text())
        self.table = load_class_table(FIX / 'class-table.tsv')

    def run_adapter(self):
        return adapt(self.inputs, self.baseline, self.table, run_id='test')

    def test_hand_ranks_coverage_and_evaluator(self):
        run = self.run_adapter()
        outputs = {q['query_id']: q for q in run['outputs']}
        good = outputs['q-complete']
        self.assertEqual(good['scores'], [
            {'candidate_id': 'a', 'score': 2},
            {'candidate_id': 'b', 'score': 1},
            {'candidate_id': 'c', 'score': 2},
            {'candidate_id': 'd', 'score': 3}])
        audit = {r['candidate_id']: r for r in good['audit']['candidates']}
        self.assertEqual(audit['b']['class_result']['score'], .25)
        self.assertFalse(audit['b']['passes_threshold'])
        self.assertEqual(audit['a']['class_result']['score'], .75)
        missing = outputs['q-missing']
        self.assertEqual(missing['status'], 'input_unavailable')
        self.assertNotIn('scores', missing)
        self.assertEqual(len(missing['audit']['candidates']), 4)
        report = evaluate(json.loads((FIX / 'benchmark.json').read_text()), run, cutoffs=(1, 2))
        self.assertEqual(report['summary']['status_counts']['valid_output'], 1)
        metrics = report['queries'][0]['metrics']
        self.assertEqual(metrics['rr'], 1)
        self.assertEqual(metrics['hit@1'], 1)
        self.assertEqual(metrics['product_recovery@1'], .5)
        self.assertEqual(metrics['all_products@1'], 0)
        self.assertEqual(metrics['all_products@2'], 1)
        self.assertEqual(report['summary']['end_to_end']['metrics']['rr'], .5)
        self.assertEqual(report['summary']['conditional']['metrics']['rr'], 1)

    def test_query_id_joins_use_each_query_classes(self):
        self.inputs['cohorts']['missing'] = copy.deepcopy(self.inputs['cohorts']['complete'])
        self.inputs['queries'][0]['genomic_classes'] = {'mibig_classes': ['b2']}
        outputs = {q['query_id']: q for q in self.run_adapter()['outputs']}
        complete = {r['candidate_id']: r['score'] for r in outputs['q-complete']['scores']}
        other = {r['candidate_id']: r['score'] for r in outputs['q-missing']['scores']}
        self.assertEqual(complete, {'a': 2, 'b': 1, 'c': 2, 'd': 3})
        self.assertEqual(other, {'a': 1, 'b': 3, 'c': 1, 'd': 2})
        evidence = {r['candidate_id']: r['class_result']['score'] for r in outputs['q-missing']['audit']['candidates']}
        self.assertEqual(evidence['a'], 1 / 3)
        self.assertEqual(evidence['b'], 2 / 3)

    def test_class_magnitude_is_not_secondary_order_and_errors_propagate(self):
        self.inputs['cohorts']['complete']['features']['c']['spectral_classes'] = {'npc_pathway': 'p1'}
        output = self.run_adapter()['outputs'][0]
        scores = {r['candidate_id']: r['score'] for r in output['scores']}
        self.assertEqual(scores['a'], scores['c'])
        with patch('examples.npclassscore_adapter.score_classes', side_effect=RuntimeError('bug')):
            with self.assertRaises(RuntimeError):
                self.run_adapter()

    def test_no_mutation_and_order_invariance(self):
        original = copy.deepcopy((self.inputs, self.baseline))
        first = self.run_adapter()
        self.assertEqual((self.inputs, self.baseline), original)
        self.inputs['queries'].reverse()
        for pool in self.inputs['candidate_pools'].values():
            pool.reverse()
        self.baseline['outputs'].reverse()
        for output in self.baseline['outputs']:
            output['scores'].reverse()
        self.assertEqual(first, self.run_adapter())

    def test_unknown_versus_zero_and_all_fail(self):
        features = self.inputs['cohorts']['complete']['features']
        for record in features.values():
            record['spectral_classes'] = {'npc_pathway': 'p2'}
        output = self.run_adapter()['outputs'][0]
        self.assertEqual(output['status'], 'ok')
        self.assertTrue(all(c['class_result']['score'] == 0 for c in output['audit']['candidates']))
        self.assertEqual(dict((r['candidate_id'], r['score']) for r in output['scores']),
                         {'a': 1, 'b': 3, 'c': 1, 'd': 2})
        features['a']['spectral_classes']['npc_pathway'] = 'unknown'
        self.assertEqual(self.run_adapter()['outputs'][0]['status'], 'input_unavailable')

    def test_baseline_nonoutput_propagation(self):
        for status in ('abstention', 'input_unavailable', 'execution_failure'):
            self.baseline['outputs'][1] = {'query_id': 'q-complete', 'status': status, 'reason': 'source reason'}
            output = self.run_adapter()['outputs'][0]
            self.assertEqual((output['status'], output['reason']), (status, 'source reason'))
            self.assertNotIn('scores', output)

    def test_optional_source_identities_match_each_query_or_are_omitted(self):
        expected = self.run_adapter()
        queries = {query['query_id']: query for query in self.inputs['queries']}
        for fields in (('cohort_id',), ('candidate_pool_id',), ('cohort_id', 'candidate_pool_id')):
            with self.subTest(fields=fields):
                baseline = copy.deepcopy(self.baseline)
                for output in baseline['outputs']:
                    output.update({field: queries[output['query_id']][field] for field in fields})
                self.assertEqual(adapt(self.inputs, baseline, self.table, run_id='test'), expected)

    def test_reject_conflicting_source_identities_before_status_or_scores(self):
        # A different declared pool can contain identical IDs and still be the wrong pool.
        self.inputs['candidate_pools']['other-pool'] = list(self.inputs['candidate_pools']['pool'])
        for field, wrong in (('cohort_id', 'missing'), ('candidate_pool_id', 'other-pool')):
            for status in ('ok', 'abstention', 'input_unavailable', 'execution_failure', 'invalid'):
                with self.subTest(field=field, status=status):
                    baseline = copy.deepcopy(self.baseline)
                    output = next(row for row in baseline['outputs'] if row['query_id'] == 'q-complete')
                    output.update(cohort_id='complete', candidate_pool_id='pool', status=status)
                    output[field] = wrong
                    if status != 'ok':
                        output.pop('scores')
                        output['reason'] = 'source reason'
                    with patch('examples.npclassscore_adapter.score_classes') as scorer:
                        with self.assertRaisesRegex(ValueError, f'Metcalf output {field} mismatch'):
                            adapt(self.inputs, baseline, self.table, run_id='test')
                        scorer.assert_not_called()
            with self.subTest(field=field, malformed_scores=True):
                baseline = copy.deepcopy(self.baseline)
                output = next(row for row in baseline['outputs'] if row['query_id'] == 'q-complete')
                output.update({field: wrong, 'scores': None})
                with self.assertRaisesRegex(ValueError, f'Metcalf output {field} mismatch'):
                    adapt(self.inputs, baseline, self.table, run_id='test')

    def test_missing_feature_records_and_tables_retain_full_audit(self):
        original = copy.deepcopy(self.inputs)
        for case in ('absent_record', 'null_record', 'absent_table', 'null_table'):
            with self.subTest(case=case):
                self.inputs = copy.deepcopy(original)
                cohort = self.inputs['cohorts']['complete']
                if case == 'absent_record':
                    del cohort['features']['a']
                elif case == 'null_record':
                    cohort['features']['a'] = None
                elif case == 'absent_table':
                    del cohort['features']
                else:
                    cohort['features'] = None
                output = next(row for row in self.run_adapter()['outputs'] if row['query_id'] == 'q-complete')
                self.assertEqual((output['status'], output['reason']),
                                 ('input_unavailable', 'incomplete_class_coverage'))
                self.assertNotIn('scores', output)
                audit = output['audit']
                self.assertEqual(audit['candidate_ids'], ['a', 'b', 'c', 'd'])
                candidates = {row['candidate_id']: row for row in audit['candidates']}
                self.assertEqual(sorted(candidates), ['a', 'b', 'c', 'd'])
                missing = ['a'] if case.endswith('record') else ['a', 'b', 'c', 'd']
                self.assertEqual(audit['class_coverage'],
                                 {'usable_candidates': 4 - len(missing), 'total_candidates': 4})
                for cid in missing:
                    self.assertEqual((candidates[cid]['status'], candidates[cid]['reason']),
                                     ('input_unavailable', 'missing_spectrum_join'))
                    self.assertIsNone(candidates[cid]['spectrum_id'])
                self.assertEqual({cid: row['metcalf_score'] for cid, row in candidates.items()},
                                 {'a': -2, 'b': 100, 'c': -2, 'd': 0})

    def test_reject_malformed_inputs_and_runs(self):
        original = copy.deepcopy((self.inputs, self.baseline))
        mutations = [
            lambda: self.inputs.update(products={}),
            lambda: self.inputs.update(query_type='spectrum'),
            lambda: self.inputs.update(expected_class_table_sha256='0' * 64),
            lambda: self.inputs['queries'][0].update(genomic_classes=[]),
            lambda: self.inputs['cohorts']['complete']['features']['a'].update(spectrum_id=7),
            lambda: self.inputs['cohorts']['complete']['features'].update(unknown={}),
            lambda: self.inputs['provenance'].update(genomic_classes=''),
            lambda: self.baseline.update(track_id='other'),
            lambda: self.baseline.update(method_id='metcalf_raw'),
            lambda: self.baseline.update(score_direction='lower'),
            lambda: self.baseline['outputs'].pop(),
            lambda: self.baseline['outputs'].append(copy.deepcopy(self.baseline['outputs'][0])),
            lambda: self.baseline['outputs'][0]['scores'].pop(),
            lambda: self.baseline['outputs'][0]['scores'][0].update(score=True),
            lambda: self.baseline['outputs'][0]['scores'][0].update(score=float('inf')),
            lambda: self.baseline['outputs'][0]['scores'][0].update(candidate_id='unknown'),
            lambda: self.baseline['outputs'][0]['scores'].append(copy.deepcopy(self.baseline['outputs'][0]['scores'][0])),
        ]
        for mutation in mutations:
            self.inputs, self.baseline = copy.deepcopy(original)
            mutation()
            with self.assertRaises(ValueError):
                self.run_adapter()

    def test_cli_and_atomic_replace_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'run.json'
            args = ['--inputs', str(FIX / 'adapter-inputs.json'), '--metcalf-run', str(FIX / 'metcalf-run.json'),
                    '--class-table', str(FIX / 'class-table.tsv'), '--run-id', 'cli', '--output', str(output)]
            result = subprocess.run([sys.executable, '-S', str(ROOT / 'examples/npclassscore_adapter.py'), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            old = output.read_bytes()
            with patch('examples.npclassscore_adapter.os.replace', side_effect=OSError('injected')):
                self.assertEqual(main(args), 2)
            self.assertEqual(output.read_bytes(), old)
            self.assertEqual(list(Path(tmp).iterdir()), [output])
            bad = Path(tmp) / 'bad.json'
            bad.write_text('{"schema_version":"1","schema_version":"1"}')
            args[1] = str(bad)
            self.assertEqual(main(args), 2)
            self.assertEqual(output.read_bytes(), old)


if __name__ == '__main__':
    unittest.main()
