import unittest
import tempfile
import json
from pathlib import Path
from scripts.finalize_similarity_independence import components, trichoderma_disposition, validate_prerequisite, method_version_fields
from scripts.similarity_independence import sha


class DependenceTests(unittest.TestCase):
    def test_exposure_versions_distinguish_execution_and_reference(self):
        task = {'method_ids': 'global_prevalence|metcalf_raw', 'method_version': '0.1.0'}
        manifest = {'implementation_version': '1.0.0', 'upstream': {'version': '1.2.0'}}
        self.assertEqual(method_version_fields('metcalf_raw', task, manifest)['method_version'], '0.1.0')
        self.assertEqual(method_version_fields('NPClassScore', task, manifest)['method_version'], '1.0.0')
        self.assertEqual(method_version_fields('NPClassScore', task, manifest)['upstream_method_version'], '1.2.0')
        self.assertEqual(method_version_fields('Rosetta_reference_only', task, manifest)['method_version'], 'not_applicable_reference_only')
        self.assertEqual(method_version_fields('Spec2Class', task, manifest)['method_version'], 'unknown')

    def test_components_require_edges_and_preserve_isolates(self):
        self.assertEqual(components(['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'c')]), [('a', 'b', 'c'), ('d',)])
        self.assertEqual(components(['a', 'b'], []), [('a',), ('b',)])

    def test_screen_rank_does_not_promote_rejected_trilid_hit(self):
        self.assertEqual(trichoderma_disposition('ETS03596.1', 'EGR44444.1'), 'rejected_weak_search_candidate_not_correspondence')
        self.assertEqual(trichoderma_disposition('ETS03598.1', 'EGR50288.1'), 'old_partial_gene_model; source_extended_model_separately_supported')
        self.assertEqual(trichoderma_disposition('ETS03593.1', 'EGR50286.1'), 'accepted_locus_gene_model_correspondence; annotation_discrepancy_retained')

    def test_pending_altered_missing_prerequisites_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'input').write_text('frozen')
            (root / 'pairs.tsv').write_text('id\tscore\tnote\na\t0.5\traw\n')
            record = {'status': 'running', 'contract_id': 'run1', 'inputs': {'input': sha(b'frozen')},
                      'stage_outputs': {'pairs.tsv': {'fields': ['id', 'score'], 'rows': 1,
                          'sha256': sha(json.dumps([['a', '0.5']], separators=(',', ':')).encode())}}}
            with self.assertRaises(ValueError):
                validate_prerequisite(record, root, 'run1', {'pairs.tsv'})
            record['status'] = 'complete'
            validate_prerequisite(record, root, 'run1', {'pairs.tsv'})
            (root / 'pairs.tsv').write_text('id\tscore\tnote\na\t0.5\tenriched\n')
            validate_prerequisite(record, root, 'run1', {'pairs.tsv'})
            with self.assertRaises(ValueError):
                validate_prerequisite(record, root, 'different_run', {'pairs.tsv'})
            (root / 'pairs.tsv').write_text('id\tscore\tnote\na\t0.9\tenriched\n')
            with self.assertRaises(ValueError):
                validate_prerequisite(record, root, 'run1', {'pairs.tsv'})
            (root / 'pairs.tsv').unlink()
            with self.assertRaises(ValueError):
                validate_prerequisite(record, root, 'run1', {'pairs.tsv'})


if __name__ == '__main__':
    unittest.main()
