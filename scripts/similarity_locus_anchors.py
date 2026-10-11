"""Accepted bounded loci alongside source-family members; no new correspondence claims."""
import itertools
import json
import re
import time
from collections import Counter
from Bio import SeqIO
from scripts import similarity_independence as s


def extract():
    relationships = s.read_tsv(s.BACKBONE[0])
    members, proteins = [], []
    unique = {r['query_id']: r for r in relationships}
    for query, r in unique.items():
        if query.startswith('source:') or query.startswith('HRPKS_71'):
            continue
        scope = 'accepted_bounded_locus'
        offset = 0
        if query.startswith('BGC0000293'):
            path = 'data/interim/acetylaszonalenin-sampled-correspondence/sampled_core.gbk'
            start, end = 0, 12765
            scope = 'sampled_named_core'
        elif query.startswith('KX449366'):
            path = 'data/raw/fac9j20-query-appraisal-2026-10-07/KX449366.1.gb'
            start, end = map(int, re.search(r':(\d+)-(\d+)', query).groups())
            start -= 1
            scope = 'construct_gene_envelope'
        elif query.startswith('NW_017962991'):
            path = 'data/interim/acu-dioxomorpholine-fac-review-2026-10-08/reference-scaffold.gb'
            start, end = 92288, 104578
            scope = 'reference_gene_envelope'
        elif query.startswith('MT376588'):
            path = 'data/interim/terreazepine-fac-review-2026-10-08/fac.gb'
            start, end = 92114, 102627
            scope = 'construct_gene_envelope'
        elif query.startswith('KN839868'):
            path = 'data/interim/hex-pks17-review-2026-10-08/native-interval.gb'
            start, end = 0, 44895
            scope = 'reference_interval'
        elif query.startswith('AWSO01000045'):
            path = 'data/interim/hex-pks15-pks23-review-2026-10-08/PKS15.gb'
            start, end = 0, 24132
            scope = 'reference_interval'
        elif query.startswith('GCA_000167675'):
            path = 'data/raw/trichoderma-qm6a-correspondence-2026-10-07/qm6a-ilicicolin-reference-window.gbk'
            start, end = 0, 30604
            scope = 'QM6a_reference_window_not_engineered_strain_genome'
        elif query.startswith('JBXSGV'):
            path = 'data/processed/blackyeast-sixmsa-candidate-v1/method_inputs/query.fasta'
            record = SeqIO.read(s.source(path), 'fasta')
            translated = str(record.seq.translate()).rstrip('*')
            assert '*' not in translated and len(translated) == 1803
            mid = 'anchor:' + query
            members.append({'member_id': mid, 'family': 'anchor_sixmsa', 'source_labels': query, 'source_path': path,
                            'member_kind': 'expressed_CDS', 'representation_scope': 'single_CDS', 'protein_count': 1,
                            'completeness': 'single_CDS_only; not_complete_cluster', 'sequence_sha256': s.sha(str(record.seq).encode())})
            proteins.append({'protein_id': mid + ':0', 'member_id': mid, 'family': 'anchor_sixmsa', 'source_protein_id': record.id,
                             'order': 0, 'annotation': 'source-supported 6MSA synthase; observed CDS translated without alteration',
                             'role': 'PKS', 'sequence': translated, 'sequence_sha256': s.sha(translated.encode()), 'length': len(translated),
                             'source_path': path, 'source_locator': 'docs/evidence/black-yeast-sixmsa-admission-2026-10-09.md'})
            s.source('data/interim/black-yeast-screen-2026-10-09/sixmsa-correspondence.json')
            continue
        else:
            raise ValueError('Unaccounted query ' + query)
        record = SeqIO.read(s.source(path), 'genbank')
        assert end <= len(record.seq), (query, end, len(record.seq))
        mid = 'anchor:' + query
        selected = [f for f in record.features if f.type == 'CDS' and int(f.location.start) >= start and int(f.location.end) <= end]
        member = {'member_id': mid, 'family': 'anchor_' + r['pathway_group'], 'source_labels': query, 'source_path': path,
                  'member_kind': scope, 'representation_scope': scope, 'protein_count': len(selected),
                  'completeness': 'accepted_boundary_only; biological_cluster_completeness_not_assumed',
                  'sequence_sha256': s.sha(str(record.seq[start:end]).encode()), 'bounds_0based_halfopen': [start, end]}
        members.append(member)
        for order, f in enumerate(selected):
            annotation = ' '.join(f.qualifiers.get('product', []))
            sequence = ''.join(f.qualifiers.get('translation', [])).rstrip('*')
            name = '|'.join(f.qualifiers.get('protein_id', f.qualifiers.get('locus_tag', ['unnamed'])))
            lower = annotation.lower()
            pks = 'polyketide synthase' in lower
            nrps = 'peptide synthetase' in lower or 'peptide synthase' in lower or 'nonribosomal' in lower or 'non-ribosomal' in lower
            role = 'PKS_NRPS_hybrid' if pks and nrps else 'PKS' if pks else 'NRPS' if nrps else 'prenyl_synthase' if 'isoprenoid synthase' in lower else 'unclassified'
            proteins.append({'protein_id': mid + ':' + str(order), 'member_id': mid, 'family': member['family'], 'source_protein_id': name,
                             'order': order, 'annotation': annotation, 'role': role, 'sequence': sequence, 'sequence_sha256': s.sha(sequence.encode()) if sequence else '',
                             'length': len(sequence), 'source_path': path, 'source_locator': str(f.location), 'status': 'available' if sequence else 'translation_unavailable'})
    return members, proteins


def main():
    s.OUT.mkdir(exist_ok=True, parents=True)
    s.RECEIPT.mkdir(exist_ok=True, parents=True)
    primary_path = s.RECEIPT / 'run-all.json'
    primary = json.loads(primary_path.read_text())
    contract = s.contract_id()
    if primary.get('status') != 'complete' or primary.get('contract_id') != contract:
        raise ValueError('Anchors require a completed primary run under the current contract')
    parent_hash = s.sha(primary_path.read_bytes())
    s.source('scripts/similarity_locus_anchors.py')
    s.source('scripts/similarity_independence.py')
    (s.RECEIPT / 'run-anchors.json').write_text(json.dumps({'status': 'running', 'contract_id': contract, 'parent_run_all_sha256': parent_hash}))
    members, proteins = extract()
    s.write_tsv('anchor-members.tsv', members)
    s.write_tsv('anchor-proteins.tsv', proteins)
    gm, gp = s.extract_gcf()
    cores = [p for p in proteins + gp if p['role'] != 'unclassified' and p['sequence']]
    rows = []
    cache = {}
    cachepath = s.RECEIPT / 'anchor-alignment-cache.jsonl'
    s.validate_cache(cachepath, s.cache_signature())
    if cachepath.exists():
        for line in cachepath.read_text().splitlines():
            obj = json.loads(line)
            cache[tuple(obj['key'])] = obj['value']
    with cachepath.open('a', encoding='utf-8') as f:
        for a, b in itertools.combinations(sorted(cores, key=lambda p: p['protein_id']), 2):
            if not (a['member_id'].startswith('anchor:') or b['member_id'].startswith('anchor:')) or a['member_id'] == b['member_id']:
                continue
            row = {'protein_a': a['protein_id'], 'protein_b': b['protein_id'], 'member_a': a['member_id'], 'member_b': b['member_id'],
                   'family_a': a['family'], 'family_b': b['family'], 'role_a': a['role'], 'role_b': b['role'], 'order_a': a['order'], 'order_b': b['order'],
                   'representation_scope': 'accepted_anchor_to_represented_core', 'status': 'not_comparable', 'reason': 'incompatible_annotated_roles',
                   'identity': None, 'coverage_a': None, 'coverage_b': None, 'score': None}
            if a['role'] == b['role']:
                key = a['sequence_sha256'], b['sequence_sha256']
                if key not in cache:
                    cache[key] = s.align_proteins(a['sequence'], b['sequence'])
                    f.write(json.dumps({'key': key, 'value': cache[key]}) + '\n')
                    f.flush()
                row.update(cache[key], status='computed', reason='')
                row['qualifies_70_80'] = row['identity'] >= .7 and min(row['coverage_a'], row['coverage_b']) >= .8
                row['qualifies_90_80'] = row['identity'] >= .9 and min(row['coverage_a'], row['coverage_b']) >= .8
            rows.append(row)
    s.write_tsv('anchor-genomic-pairs.tsv', rows)
    if s.sha(primary_path.read_bytes()) != parent_hash:
        raise ValueError('Primary receipt changed during anchor run')
    (s.RECEIPT / 'run-anchors.json').write_text(json.dumps({'status': 'complete', 'inputs': s.INPUTS,
        'contract_id': contract, 'parent_run_all_sha256': parent_hash, 'stage_outputs': s.stage_output_receipts(s.ANCHOR_OUTPUTS),
        'members': len(members), 'proteins': len(proteins), 'role_counts': Counter(p['role'] for p in proteins),
        'pairs': len(rows), 'computed': sum(r['status'] == 'computed' for r in rows), 'command': 'python -m scripts.similarity_locus_anchors'}, indent=2))
    print('anchors complete', len(members), Counter(p['role'] for p in proteins), flush=True)


if __name__ == '__main__':
    main()
