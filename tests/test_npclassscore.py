from pathlib import Path
import hashlib
import json
import tempfile
import unittest

from scripts.npclassscore import load_class_table, score_classes

FIXTURE = Path(__file__).parent / 'fixtures' / 'npclassscore' / 'class-table.tsv'


class NPClassScoreTests(unittest.TestCase):
    def table_from_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'table.tsv'
            path.write_text(text, encoding='utf-8')
            return load_class_table(path)

    def test_hand_counted_forward_denominator(self):
        table = load_class_table(FIXTURE)
        result = score_classes(table, {'mibig_classes': ['b1']}, {'npc_class': 'm1'})
        self.assertEqual(result['score'], 3 / 4)
        self.assertEqual(result['pairs'][0]['count'], 3)
        self.assertEqual(result['pairs'][0]['denominator'], 4)
        self.assertEqual(score_classes(table, {'mibig_classes': ['b1']}, {'npc_class': 'm2'})['score'], 1 / 4)

    def test_metadata_compound_repetition_and_subclasses(self):
        table = load_class_table(FIXTURE)
        self.assertEqual(table.metadata['compound_rows'], 10)
        self.assertEqual(table.metadata['source_sha256'], hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        self.assertEqual(table.counts['class:subclass']['npc_class']['b1:s1'], {'m1': 3, 'm2': 1})
        self.assertEqual(table.counts['mibig_classes']['npc_class']['b2'], {'m1': 2, 'm2': 4})
        self.assertEqual(table.metadata['pair_totals']['mibig_classes']['npc_class'], 10)
        json.dumps(table.metadata)

    def test_maximum_across_named_ontologies_including_first(self):
        table = load_class_table(FIXTURE)
        result = score_classes(table, {'mibig_classes': ['b1'], 'as_classes': ['a2']},
                               {'npc_class': 'm1', 'cf_kingdom': 'k'})
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(len(result['pairs']), 4)
        self.assertIn(1 / 3, [pair['score'] for pair in result['pairs']])
        json.dumps(result)

    def test_known_zero_unknown_and_missing_are_distinct(self):
        table = load_class_table(FIXTURE)
        zero = score_classes(table, {'mibig_classes': ['b1']}, {'npc_pathway': 'p2'})
        self.assertEqual((zero['status'], zero['score']), ('ok', 0.0))
        for genomic, spectral, reason in [
            ({'mibig_classes': ['b1', 'unknown']}, {'npc_class': 'm1'}, 'unknown_vocabulary'),
            ({'mibig_classes': ['b1']}, {'npc_class': 'unknown', 'cf_kingdom': 'k'}, 'unknown_vocabulary'),
            ({}, {'npc_class': 'm1'}, 'missing_genomic_classes'),
            ({'as_classes': []}, {}, 'missing_genomic_classes'),
            ({'mibig_classes': ['b1']}, {'npc_class': None}, 'missing_spectral_classes'),
        ]:
            with self.subTest(reason=reason, genomic=genomic, spectral=spectral):
                result = score_classes(table, genomic, spectral)
                self.assertEqual((result['status'], result['reason']), ('input_unavailable', reason))
                self.assertNotIn('score', result)

    def test_known_terms_without_shared_denominator(self):
        lines = FIXTURE.read_text().splitlines()
        cells = lines[1].split('\t')
        cells[0], cells[1], cells[2] = 'BGC3_a', 'b3:', 'a3'
        cells[5:] = [''] * 9
        table = self.table_from_text('\n'.join(lines + ['\t'.join(cells)]) + '\n')
        result = score_classes(table, {'mibig_classes': ['b3']}, {'npc_class': 'm1'})
        self.assertEqual(result['reason'], 'no_usable_class_pairs')
        self.assertEqual(result['skipped_pairs'][0]['reason'], 'missing_denominator')
        usable = score_classes(table, {'mibig_classes': ['b3', 'b1']}, {'npc_class': 'm1'})
        self.assertEqual(usable['score'], .75)

    def test_row_column_and_input_order_do_not_change_scores(self):
        lines = [line.split('\t') for line in FIXTURE.read_text().splitlines()]
        shuffled = '\n'.join('\t'.join(reversed(row)) for row in [lines[0]] + list(reversed(lines[1:])))
        table = self.table_from_text(shuffled)
        original = load_class_table(FIXTURE)
        first = score_classes(original, {'mibig_classes': ['b1', 'b2']}, {'npc_class': 'm2'})
        second = score_classes(table, {'mibig_classes': ['b2', 'b1', 'b1']}, {'npc_class': 'm2'})
        self.assertEqual(first['pairs'], second['pairs'])
        self.assertEqual(first['score'], 2 / 3)

    def test_hybrid_alkaloid_and_cartesian_multilabel_counts(self):
        lines = FIXTURE.read_text().splitlines()
        cells = lines[1].split('\t')
        cells[1], cells[2], cells[10] = 'Polyketide:Other,NRP:,Alkaloid:', 'a1,a2', 'm1; m2'
        table = self.table_from_text(lines[0] + '\n' + '\t'.join(cells) + '\n')
        self.assertEqual(table.metadata['vocabulary']['mibig_classes'], ['Other', 'PKS-NRP_Hybrids'])
        for level, term in [('mibig_classes', 'Other'), ('mibig_classes', 'PKS-NRP_Hybrids'), ('as_classes', 'a1'), ('as_classes', 'a2')]:
            self.assertEqual(table.counts[level]['npc_class'][term], {'m1': 1, 'm2': 1})
        self.assertEqual(table.metadata['pair_totals']['mibig_classes']['npc_class'], 4)

    def test_repeated_reference_terms_preserve_cartesian_multiplicity(self):
        lines = FIXTURE.read_text().splitlines()
        headers = lines[0].split('\t')
        repeated = dict(zip(headers, lines[1].split('\t')))
        repeated.update(as_classes='a1,a1', npc_class='m1; m1; m2')
        singleton = dict(repeated, compound_name='BGC1_b', as_classes='a1', npc_class='m2')
        text = '\n'.join([lines[0]] + [
            '\t'.join(row[column] for column in headers)
            for row in (repeated, singleton)
        ]) + '\n'
        table = self.table_from_text(text)

        # The first row contributes four a1/m1 and two a1/m2 pairs;
        # the second adds one a1/m2 pair, giving seven pairs in total.
        result = score_classes(table, {'as_classes': ['a1']}, {'npc_class': 'm1'})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(len(result['pairs']), 1)
        self.assertEqual(result['pairs'][0]['count'], 4)
        self.assertEqual(result['pairs'][0]['denominator'], 7)
        self.assertEqual(result['pairs'][0]['score'], 4 / 7)
        self.assertEqual(result['score'], 4 / 7)

    def test_invalid_inputs_raise(self):
        table = load_class_table(FIXTURE)
        for genomic, spectral in [({'bigscape_class': ['b1']}, {}), ({'class:subclass': ['b1:s1']}, {}),
                                  ({}, {'wrong': 'm1'}), ({'mibig_classes': 'b1'}, {}),
                                  ({'mibig_classes': [None]}, {}), ({}, {'npc_class': ['m1']}),
                                  ({}, {'npc_class': ''}), (None, {})]:
            with self.subTest(genomic=genomic, spectral=spectral), self.assertRaises(ValueError):
                score_classes(table, genomic, spectral)

    def test_malformed_tables_and_duplicate_identifiers_raise(self):
        text = FIXTURE.read_text()
        lines = text.splitlines()
        for malformed in ['', lines[0] + '\n', text + lines[1] + '\n',
                          text.replace('b1:s1', 'b1'), text.replace('a1', 'a1,'),
                          text.replace('npc_class', 'npc_pathway'), lines[0] + '\nshort\n']:
            with self.subTest(text=malformed[:70]), self.assertRaises(ValueError):
                self.table_from_text(malformed)


if __name__ == '__main__':
    unittest.main()
