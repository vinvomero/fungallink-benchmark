import unittest
import tempfile
import json
import csv
from pathlib import Path
from unittest.mock import patch
from scripts import similarity_independence as similarity
import numpy as np
from scripts.similarity_independence import preprocess_peaks, align_proteins, bit_tanimoto, ambiguity_range, cosine_pair, validate_cache, structure_identity


class SimilarityTests(unittest.TestCase):
    def test_retained_structure_output_contract(self):
        relationships = similarity.read_tsv(similarity.BACKBONE[0])
        with tempfile.TemporaryDirectory() as tmp, patch.object(similarity, 'OUT', Path(tmp)):
            similarity.make_structures(relationships)
            with (Path(tmp) / 'structures.tsv').open() as handle:
                structures = list(csv.DictReader(handle, delimiter='\t'))
            with (Path(tmp) / 'chemical-pairs.tsv').open() as handle:
                pairs = list(csv.DictReader(handle, delimiter='\t'))
            self.assertEqual(len(structures), 30)
            self.assertEqual(sum(r['mapping_status'] == 'supported' for r in structures), 5)
            self.assertEqual(len(pairs), 435)
            self.assertEqual(sum(r['status'] == 'computed' for r in pairs), 10)
            self.assertEqual(sum(r['tanimoto'] == '' for r in pairs), 425)
            self.assertTrue(all(r['tanimoto'] == '' for r in pairs if r['status'] == 'unavailable'))

    def test_hand_counted_bit_intersection(self):
        self.assertEqual(bit_tanimoto({1, 2, 3}, {2, 3, 4, 5}), 2 / 5)

    def test_alignment_arithmetic(self):
        x = align_proteins('ACDE', 'ACDF')
        self.assertEqual((x['identical'], x['paired']), (3, 4))
        self.assertEqual(x['identity'], .75)
        self.assertEqual(x['coverage_a'], 1)
        self.assertEqual(x['coverage_b'], 1)
        self.assertEqual(x['score'], 16)
        self.assertFalse(x['exact_equal'])
        self.assertTrue(align_proteins('ACDE', 'ACDE')['exact_equal'])

    def test_peak_rules_and_sparse(self):
        mz, intensity = preprocess_peaks([(5, 100), (20, 100), (30, 25), (40, .1), (99.5, 80), (50, -1)], 100)
        np.testing.assert_array_equal(mz, [20, 30])
        np.testing.assert_allclose(intensity, np.array([2, 1]) / np.sqrt(5))
        self.assertEqual(len(preprocess_peaks([(5, 1)], None)[0]), 0)

    def test_independent_cosine(self):
        a = (np.array([20., 30.]), np.array([.6, .8]))
        b = (np.array([20., 40.]), np.array([.8, .6]))
        score, matched = cosine_pair(a, b)
        self.assertAlmostEqual(score, .48)
        self.assertEqual(matched, 1)
        self.assertEqual(cosine_pair(a, a), (1., 2))
        self.assertEqual(cosine_pair(a, b), cosine_pair(b, a))

    def test_ambiguity_preserves_range(self):
        self.assertEqual(ambiguity_range([.2, .9, .4]), (.2, .9))
        self.assertEqual(ambiguity_range([]), (None, None))

    def test_cache_rejects_unproven_or_changed_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / 'cache.jsonl'
            cache.write_text('{"retained":"alignment"}\n')
            with self.assertRaises(ValueError):
                validate_cache(cache, {'settings': 'v1'})
            cache.with_suffix('.metadata.json').write_text(json.dumps({'signature': {'settings': 'v1'}}))
            validate_cache(cache, {'settings': 'v1'})
            with self.assertRaises(ValueError):
                validate_cache(cache, {'settings': 'v2'})

    def test_structure_parse_connectivity_and_stereo_disagreement(self):
        good = structure_identity('CCO', 'LFQSCWFLJHTTHZ-UHFFFAOYSA-N')
        self.assertEqual(good['status'], 'supported_connectivity')
        self.assertEqual(structure_identity('CCO', 'VNWKTOKETHGBQD-UHFFFAOYSA-N')['status'], 'conflicting_connectivity')
        self.assertEqual(structure_identity('CCO.[Na+]', '')['status'], 'invalid_or_multicomponent')
        self.assertEqual(structure_identity('', '')['status'], 'unavailable')
        self.assertFalse(structure_identity('N[C@@H](C)C(=O)O', 'QNAYBMKLOCPYGJ-UHFFFAOYSA-N')['chiral_eligible'])


if __name__ == '__main__':
    unittest.main()
