"""Reproduce retained-representation similarity; never change benchmark labels or scores."""
import argparse
import csv
import hashlib
import importlib.metadata as metadata
import inspect
import itertools
import json
import math
import re
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from Bio import Align, SeqIO
from Bio.Align import substitution_matrices
from lxml import html
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator, rdMolDescriptors

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/processed/similarity-independence-v1'
RECEIPT = ROOT / 'planning/similarity-independence-work-2026-10-11'
ZIP = 'data/raw/sources/caesar-2023/41589_2023_1276_MOESM3_ESM.zip'
TABLE = 'data/interim/admitted-input-coverage-2026-10-09/spec2class/MIBiG2.0_compounds_with_AS_BGC_CF_NPC_classes.txt'
ROSETTA = 'data/interim/admitted-input-coverage-2026-10-09/matched_mibig_gnps_update.csv'
BACKBONE = ['data/curated/relationship-readiness-v1.tsv', 'data/curated/label-evidence.tsv',
            'data/manifests/relationship-traceability-v1.tsv', 'data/manifests/task-exposure-v1.tsv']
FAMILIES = ['DMAT_34', 'HRPKS_71', 'NRPSPKS_85', 'TERPENE_40', 'NRPSLIKE_59', 'NRPKS_18', 'NRPS_66']
PARAMETERS = {'chemical': {'radius': 2, 'bits': 2048, 'bond_types': True, 'chirality': False, 'flags': [.7, .9]},
              'genomic': {'matrix': 'BLOSUM62', 'mode': 'global', 'open_gap_score': -10, 'extend_gap_score': -.5,
                          'terminal_gaps': 'same_as_internal', 'tie_rule': 'first_library_optimal_path', 'coverage': .8, 'identity_flags': [.7, .9]},
              'spectral': {'tolerance_Da': .02, 'mz_power': 0, 'intensity_power': 1, 'min_mz': 10,
                           'precursor_exclusion_Da': 1, 'relative_intensity': .01, 'transform': 'sqrt_then_L2',
                           'minimum_matches': 6, 'flags': [.7, .9]}}
INPUTS = {}
PRIMARY_OUTPUTS = ['structures.tsv', 'chemical-pairs.tsv', 'spectra.tsv', 'spectral-pairs.tsv',
                   'gcf-members.tsv', 'proteins.tsv', 'genomic-pairs.tsv', 'genomic-locus-pairs.tsv']
ANCHOR_OUTPUTS = ['anchor-members.tsv', 'anchor-proteins.tsv', 'anchor-genomic-pairs.tsv']
# Final enrichment changes only these primary fields. Numerical values and IDs stay guarded.
ENRICHED_FIELDS = {'structures.tsv': {'reason'}, 'spectra.tsv': {'native_scan', 'collision_energy'},
                   'spectral-pairs.tsv': {'exact_native_scan_equal', 'metadata_stratum'}}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source(path):
    p = ROOT / path
    INPUTS[str(path).replace('\\', '/')] = sha(p.read_bytes())
    return p


def read_tsv(path):
    with source(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(name, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fields, delimiter='\t', lineterminator='\n', extrasaction='raise')
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, (dict, list)) else v for k, v in r.items()})


def contract_id():
    paths = BACKBONE + ['protocol/similarity-independence-v1.md', 'docs/plans/2026-10-11-1704-similarity-independence-plan.md']
    hashes = {p: sha(source(p).read_bytes()) for p in paths}
    return sha(json.dumps({'inputs': hashes, 'parameters': PARAMETERS}, sort_keys=True).encode())


def output_projection(path, fields=None):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        fields = fields or [k for k in reader.fieldnames if k not in ENRICHED_FIELDS.get(path.name, set())]
        if not set(fields).issubset(reader.fieldnames):
            raise ValueError('Required output columns missing: ' + str(path))
        values = [[r[k] for k in fields] for r in reader]
    return {'fields': fields, 'rows': len(values), 'sha256': sha(json.dumps(values, separators=(',', ':')).encode())}


def stage_output_receipts(names):
    return {(OUT / name).relative_to(ROOT).as_posix(): output_projection(OUT / name) for name in names}


def bit_tanimoto(a, b):
    return len(a & b) / len(a | b) if a | b else 1.


def ambiguity_range(values):
    return (min(values), max(values)) if values else (None, None)


def structure_identity(smiles, source_key):
    if not smiles:
        return {'status': 'unavailable', 'chiral_eligible': False}
    mol = Chem.MolFromSmiles(smiles)
    if mol is None or len(Chem.GetMolFrags(mol)) != 1:
        return {'status': 'invalid_or_multicomponent', 'chiral_eligible': False}
    key = Chem.MolToInchiKey(mol)
    return {'status': 'supported_connectivity' if key.split('-')[0] == source_key.split('-')[0] else 'conflicting_connectivity',
            'computed_key': key, 'stereo_layer_agrees': key == source_key,
            'chiral_eligible': False, 'chiral_reason': 'Source-level stereochemical adjudication not available for this mapping set'}


def cache_signature():
    return {'parameters': PARAMETERS['genomic'], 'biopython': metadata.version('biopython'),
            'alignment_implementation_sha256': sha(inspect.getsource(align_proteins).encode()),
            'epsilon': 1e-6, 'cache_schema': 1}


def validate_cache(path, signature):
    sidecar = path.with_suffix('.metadata.json')
    if path.exists() and path.stat().st_size:
        if not sidecar.exists():
            raise ValueError('Nonempty cache lacks proven settings: ' + str(path))
        saved = json.loads(sidecar.read_text())
        if saved.get('signature') != signature:
            raise ValueError('Cache settings or alignment implementation changed: ' + str(path))
    else:
        sidecar.write_text(json.dumps({'signature': signature}, indent=2) + '\n')


def align_proteins(a, b):
    aligner = Align.PairwiseAligner()
    aligner.mode = 'global'
    aligner.substitution_matrix = substitution_matrices.load('BLOSUM62')
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -.5
    alignments = aligner.align(a, b)
    aln = alignments[0]
    try:
        ties = len(alignments)
    except OverflowError:
        ties = 'overflow'
    aa, bb = str(aln[0]), str(aln[1])
    paired = sum(x != '-' and y != '-' for x, y in zip(aa, bb))
    same = sum(x == y and x != '-' for x, y in zip(aa, bb))
    return {'identity': same / paired if paired else None, 'coverage_a': paired / len(a), 'coverage_b': paired / len(b),
            'identical': same, 'paired': paired, 'length_a': len(a), 'length_b': len(b), 'score': aln.score,
            'optimal_alignment_paths': ties, 'exact_equal': a == b, 'sequence_sha256_a': sha(a.encode()), 'sequence_sha256_b': sha(b.encode())}


def preprocess_peaks(peaks, precursor):
    good = [(float(m), float(i)) for m, i in peaks if math.isfinite(m) and math.isfinite(i) and m >= 10 and i > 0
            and (precursor is None or abs(m - precursor) > 1)]
    if not good:
        return np.array([], dtype=float), np.array([], dtype=float)
    threshold = max(i for _, i in good) * .01
    good = sorted((m, i) for m, i in good if i >= threshold)
    mz = np.array([m for m, _ in good], dtype=float)
    intensity = np.sqrt(np.array([i for _, i in good], dtype=float))
    return mz, intensity / np.linalg.norm(intensity)


def cosine_pair(a, b):
    from matchms import Spectrum
    from matchms.similarity import CosineHungarian
    scorer = CosineHungarian(tolerance=.02, mz_power=0., intensity_power=1.)
    x = scorer.pair(Spectrum(a[0], a[1], metadata={}, metadata_harmonization=False),
                    Spectrum(b[0], b[1], metadata={}, metadata_harmonization=False))
    return float(x['score']), int(x['matches'])


def domain_role(title):
    # Only directly displayed biosynthetic domains define comparable roles.
    pks = 'ketoacyl-synt' in title or 'Ketoacyl-synt' in title
    nrps = 'Condensation' in title and 'AMP-binding' in title
    if pks and nrps:
        return 'PKS_NRPS_hybrid'
    if pks:
        return 'PKS'
    if nrps:
        return 'NRPS'
    for token, role in [('Trp_DMAT', 'DMAT'), ('Terpene_synth', 'terpene_synthase'), ('Polyprenyl_synt', 'prenyl_synthase')]:
        if token in title:
            return role
    return 'unclassified'


def extract_gcf():
    members, proteins = [], []
    z = zipfile.ZipFile(source(ZIP))
    for family in FAMILIES:
        member_path = 'Supplementary Data 1/' + family + '.html'
        blob = z.read(member_path)
        doc = html.fromstring(blob)
        for n, svg in enumerate(doc.xpath('//svg')):
            block = svg.getparent()
            labels = block.xpath('./div/b/text()')
            mid = family + ':' + str(n)
            member = {'member_id': mid, 'family': family, 'source_labels': '|'.join(labels), 'source_path': ZIP,
                      'archive_member': member_path, 'member_sha256': sha(blob), 'member_kind': 'reference' if any('MIBiG' in s for s in labels) else 'sampled',
                      'representation_scope': 'source_displayed_locus', 'completeness': 'displayed_proteins; biological_cluster_completeness_unknown'}
            count = 0
            for order, polygon in enumerate(svg.xpath('./polygon[@onclick]')):
                hit = re.search(r"openBlast\('([^']+)'\)", polygon.get('onclick', ''))
                if not hit:
                    continue
                sequence = hit.group(1).strip().rstrip('*')
                title = polygon.findtext('title', '')
                proteins.append({'protein_id': mid + ':' + str(order), 'member_id': mid, 'family': family,
                                 'source_protein_id': polygon.get('id', ''), 'order': order, 'annotation': title,
                                 'role': domain_role(title), 'sequence': sequence, 'sequence_sha256': sha(sequence.encode()),
                                 'length': len(sequence), 'source_path': ZIP, 'source_locator': member_path + '#' + '|'.join(labels)})
                count += 1
            member['protein_count'] = count
            members.append(member)
    return members, proteins


def make_structures(relationships):
    table = read_tsv(TABLE)
    records = {r['compound_name']: r for r in table}
    mapping = {
        'caesar2023:corrected:5': ('BGC0000293_acetylaszonalenin', 'docs/evidence/acetylaszonalenin-sampled-correspondence-2026-10-03.md'),
        'caesar2023:relationship:6': ('BGC0001290_emericellamide A', 'docs/evidence/emericellamide-a.md'),
        'caesar2023:relationship:13': ('BGC0000070_griseofulvin', 'docs/evidence/griseofulvin-review-2026-10-01.md'),
        'caesar2023:relationship:23': ('BGC0001399_fellutamide B', 'docs/evidence/remaining-reference-appraisals-2026-10-01.md'),
        'caesar2023:relationship:25': ('BGC0001722_aspernidine A', 'docs/evidence/chrysogine-aspernidine-review-2026-10-01.md'),
    }
    structures, mols = [], {}
    for r in relationships:
        rid = r['relationship_id']
        row = {'relationship_id': rid, 'query_id': r['query_id'], 'product': r['product'], 'structure_id': rid + ':structure',
               'alternative_set': '', 'mapping_status': 'unavailable', 'original_text': '', 'canonical_isomeric_smiles': '',
               'computed_inchikey': '', 'source_inchikey': '', 'connectivity_key': '', 'formula': '',
               'formula_check': 'unavailable_source_formula', 'stereochemistry': 'unknown', 'chiral_sensitivity_eligible': False,
               'source_path': TABLE, 'source_locator': '', 'mapping_rationale': '', 'reviewer': 'Codex automated source crosswalk; human scientific review pending',
               'reason': 'No retained machine-readable structure with verified source-specific crosswalk; reopen on exact source structure/identifier evidence'}
        if rid in mapping:
            key, evidence = mapping[rid]
            source(evidence)
            t = records[key]
            mol = Chem.MolFromSmiles(t['smiles'])
            identity_check = structure_identity(t['smiles'], t['inchi_key'])
            row.update(original_text=t['smiles'], source_inchikey=t['inchi_key'], source_locator=key + ';' + evidence,
                       mapping_rationale='Admitted target source panel and experimental reference BGC identifier in evidence packet; exact BGC+compound row in pinned class table')
            if identity_check['status'] == 'invalid_or_multicomponent':
                row.update(mapping_status='invalid', reason='RDKit parse/single-component failure')
            else:
                inchikey = Chem.MolToInchiKey(mol)
                if identity_check['status'] == 'conflicting_connectivity':
                    row.update(mapping_status='ambiguous_set', reason='Source InChIKey and SMILES connectivity disagree; no primary structure')
                else:
                    row.update(mapping_status='supported', canonical_isomeric_smiles=Chem.MolToSmiles(mol, isomericSmiles=True),
                               computed_inchikey=inchikey, connectivity_key=inchikey.split('-')[0], formula=rdMolDescriptors.CalcMolFormula(mol),
                               stereochemistry='SMILES assigned stereo retained; source key stereo layer differs' if inchikey != t['inchi_key'] else 'source key consistent; source-level stereo review pending',
                               reason='Connectivity supported; no independent chemical adjudication. Chiral sensitivity withheld until source stereo reconciliation')
                    mols[rid] = mol
        structures.append(row)
    fpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048, includeChirality=False, useBondTypes=True)
    fps = {k: fpgen.GetFingerprint(v) for k, v in mols.items()}
    pairs = []
    for a, b in itertools.combinations(sorted(relationships, key=lambda r: r['relationship_id']), 2):
        ai, bi = a['relationship_id'], b['relationship_id']
        row = {'relationship_a': ai, 'relationship_b': bi, 'structure_a': ai + ':structure', 'structure_b': bi + ':structure',
               'scenario': 'supported_primary', 'fingerprint': 'Morgan_binary_radius2_2048_bondtypes_chiralityfalse',
               'tanimoto': None, 'exact_isomeric_equal': None, 'range_min': None, 'range_max': None,
               'flag_0_7': None, 'flag_0_9': None, 'status': 'unavailable', 'reason': 'one_or_both_structures_unavailable'}
        if ai in mols and bi in mols:
            score = DataStructs.TanimotoSimilarity(fps[ai], fps[bi])
            assert abs(score - bit_tanimoto(set(fps[ai].GetOnBits()), set(fps[bi].GetOnBits()))) < 1e-12
            row.update(tanimoto=score, exact_isomeric_equal=Chem.MolToSmiles(mols[ai]) == Chem.MolToSmiles(mols[bi]),
                       range_min=score, range_max=score, flag_0_7=score >= .7, flag_0_9=score >= .9, status='computed', reason='')
        pairs.append(row)
    write_tsv('structures.tsv', structures)
    write_tsv('chemical-pairs.tsv', pairs)
    return structures, pairs


def parse_mgf(path):
    spectra = []
    for block in source(path).read_text().split('BEGIN IONS')[1:]:
        meta, peaks = {}, []
        for line in block.split('END IONS')[0].splitlines():
            if '=' in line:
                k, v = line.split('=', 1)
                meta[k] = v
            elif line.strip():
                mz, intensity = line.split()[:2]
                peaks.append((float(mz), float(intensity)))
        spectra.append((meta, peaks))
    return spectra


def spectral_analysis():
    spectra, processed = [], {}
    for pool in ['trichoderma-network-candidate-v1', 'blackyeast-sixmsa-candidate-v1']:
        base = 'data/processed/' + pool + '/method_inputs/'
        joins = {r['spectrum_id']: r for r in read_tsv(base + 'spectra.tsv')}
        for meta, peaks in parse_mgf(base + 'spectra.mgf'):
            sid = meta['TITLE']
            join = joins[sid]
            assert join['candidate_id'] == meta['FEATURE_ID']
            precursor = float(meta['PEPMASS'].split()[0]) if 'PEPMASS' in meta else None
            mz, intensities = preprocess_peaks(peaks, precursor)
            processed[sid] = (mz, intensities)
            charge = meta.get('CHARGE', 'unknown')
            spectra.append({'spectrum_id': sid, 'feature_id': join['candidate_id'], 'pool': pool,
                            'source_path': base + 'spectra.mgf', 'source_sha256': INPUTS[base + 'spectra.mgf'],
                            'precursor_mz': precursor, 'charge': charge, 'polarity': '+' if charge.endswith('+') else '-' if charge.endswith('-') else 'unknown',
                            'polarity_source': 'explicit signed native-export CHARGE', 'rt_seconds': meta.get('RTINSECONDS', 'unknown'),
                            'collision_energy': meta.get('COLLISIONENERGY', 'unknown'), 'instrument': meta.get('INSTRUMENT', 'unknown'),
                            'native_scan': meta.get('SCANS', 'unknown'), 'peaks_before': len(peaks), 'peaks_after': len(mz),
                            'canonical_original_peaks_sha256': sha(json.dumps(sorted(peaks), separators=(',', ':')).encode()),
                            'status': 'usable' if len(mz) else 'empty_after_preprocessing'})
    from matchms import Spectrum
    from matchms.similarity import CosineHungarian
    prepared = {k: Spectrum(x, y, metadata={}, metadata_harmonization=False) for k, (x, y) in processed.items() if len(x)}
    scorer = CosineHungarian(tolerance=.02, mz_power=0., intensity_power=1.)
    rows = []
    for a, b in itertools.combinations(sorted(spectra, key=lambda s: s['spectrum_id']), 2):
        ai, bi = a['spectrum_id'], b['spectrum_id']
        compatible = a['pool'] == b['pool'] or (a['charge'] != 'unknown' and a['polarity'] != 'unknown' and a['charge'] == b['charge'] and a['polarity'] == b['polarity'])
        row = {'spectrum_a': ai, 'spectrum_b': bi, 'feature_a': a['feature_id'], 'feature_b': b['feature_id'], 'pool_a': a['pool'], 'pool_b': b['pool'],
               'metadata_stratum': a['polarity'] + '/' + b['polarity'] + ';collision_energy_unknown;instrument_unknown',
               'peaks_a_before': a['peaks_before'], 'peaks_a_after': a['peaks_after'], 'peaks_b_before': b['peaks_before'], 'peaks_b_after': b['peaks_after'],
               'cosine': None, 'matched_peaks': None, 'exact_peak_list_equal': a['canonical_original_peaks_sha256'] == b['canonical_original_peaks_sha256'],
               'exact_native_scan_equal': None, 'flag_0_7_6peaks': None, 'flag_0_9_6peaks': None,
               'status': 'excluded', 'reason': 'cross_pool_incompatible_or_unknown_polarity_charge'}
        if compatible and ai in prepared and bi in prepared:
            result = scorer.pair(prepared[ai], prepared[bi])
            score, matches = float(result['score']), int(result['matches'])
            row.update(cosine=score, matched_peaks=matches, flag_0_7_6peaks=score >= .7 and matches >= 6,
                       flag_0_9_6peaks=score >= .9 and matches >= 6, status='computed', reason='')
        elif compatible:
            row['reason'] = 'empty_after_preprocessing'
        rows.append(row)
    write_tsv('spectra.tsv', spectra)
    write_tsv('spectral-pairs.tsv', rows)
    return spectra, rows


def genomic_analysis(members, proteins):
    write_tsv('gcf-members.tsv', members)
    write_tsv('proteins.tsv', proteins)
    core = [p for p in proteins if p['role'] != 'unclassified']
    # Cache exact sequence pairs: repeated member/reference strings need no repeated alignments.
    cache_path = RECEIPT / 'alignment-cache.jsonl'
    validate_cache(cache_path, cache_signature())
    cache = {}
    if cache_path.exists():
        for line in cache_path.read_text().splitlines():
            x = json.loads(line)
            cache[tuple(x['key'])] = x['value']
    rows, started = [], time.time()
    with cache_path.open('a', encoding='utf-8') as receipt:
        for a, b in itertools.combinations(sorted(core, key=lambda x: x['protein_id']), 2):
            if a['member_id'] == b['member_id']:
                continue
            row = {'protein_a': a['protein_id'], 'protein_b': b['protein_id'], 'member_a': a['member_id'], 'member_b': b['member_id'],
                   'family_a': a['family'], 'family_b': b['family'], 'representation_scope': 'source_displayed_core_protein',
                   'role_a': a['role'], 'role_b': b['role'], 'order_a': a['order'], 'order_b': b['order'],
                   'identity': None, 'coverage_a': None, 'coverage_b': None, 'score': None,
                   'status': 'not_comparable', 'reason': 'incompatible_source_annotated_biosynthetic_roles'}
            if a['role'] == b['role']:
                key = (a['sequence_sha256'], b['sequence_sha256'])
                if key not in cache:
                    cache[key] = align_proteins(a['sequence'], b['sequence'])
                    receipt.write(json.dumps({'key': key, 'value': cache[key]}) + '\n')
                    receipt.flush()
                    if len(cache) % 50 == 0:
                        print('alignments', len(cache), 'seconds', round(time.time() - started), flush=True)
                result = cache[key]
                row.update(result, status='computed', reason='')
                row['qualifies_70_80'] = result['identity'] >= .7 and min(result['coverage_a'], result['coverage_b']) >= .8
                row['qualifies_90_80'] = result['identity'] >= .9 and min(result['coverage_a'], result['coverage_b']) >= .8
            rows.append(row)
    # Reciprocal best ties are scoped to each member pair and role, never across the population.
    best = defaultdict(lambda: -float('inf'))
    for r in rows:
        if r['status'] == 'computed':
            for p, other in [(r['protein_a'], r['member_b']), (r['protein_b'], r['member_a'])]:
                best[p, other] = max(best[p, other], r['score'])
    for r in rows:
        r['reciprocal_best_tie'] = r['status'] == 'computed' and r['score'] == best[r['protein_a'], r['member_b']] and r['score'] == best[r['protein_b'], r['member_a']]
    write_tsv('genomic-pairs.tsv', rows)
    locus_rows = []
    by_pair = defaultdict(list)
    for r in rows:
        by_pair[tuple(sorted((r['member_a'], r['member_b'])))].append(r)
    for a, b in itertools.combinations(sorted(members, key=lambda x: x['member_id']), 2):
        rr = by_pair[a['member_id'], b['member_id']]
        computed = [x for x in rr if x['status'] == 'computed']
        row = {'member_a': a['member_id'], 'member_b': b['member_id'], 'family_a': a['family'], 'family_b': b['family'],
               'all_annotated_proteins_a': a['protein_count'], 'all_annotated_proteins_b': b['protein_count'],
               'compatible_core_pairs': len(computed), 'identity_min': min((x['identity'] for x in computed), default=None),
               'identity_max': max((x['identity'] for x in computed), default=None),
               'status': 'core_only_comparison' if computed else 'unavailable_no_compatible_annotated_core',
               'interpretation': 'Unclassified/noncore proteins unassessed; no whole_cluster_dissimilarity_claim'}
        for threshold in [70, 90]:
            qualified = [x for x in computed if x['reciprocal_best_tie'] and x['qualifies_' + str(threshold) + '_80']]
            ids_a = {x['protein_a'] if x['member_a'] == a['member_id'] else x['protein_b'] for x in qualified}
            ids_b = {x['protein_b'] if x['member_b'] == b['member_id'] else x['protein_a'] for x in qualified}
            row['annotated_fraction_a_' + str(threshold)] = len(ids_a) / a['protein_count'] if a['protein_count'] else None
            row['annotated_fraction_b_' + str(threshold)] = len(ids_b) / b['protein_count'] if b['protein_count'] else None
            row['reciprocal_order_pairs_' + str(threshold)] = [[x['order_a'], x['order_b']] for x in qualified]
        locus_rows.append(row)
    write_tsv('genomic-locus-pairs.tsv', locus_rows)
    return rows, locus_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inspect', action='store_true')
    parser.add_argument('--stage', choices=['chemical', 'spectral', 'genomic', 'all'], default='all')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    RECEIPT.mkdir(parents=True, exist_ok=True)
    relationships = read_tsv(BACKBONE[0])
    for p in BACKBONE[1:] + ['protocol/similarity-independence-v1.md', 'docs/plans/2026-10-11-1704-similarity-independence-plan.md', 'scripts/similarity_independence.py']:
        source(p)
    assert len(relationships) == 30 and len({r['query_id'] for r in relationships}) == 16
    members, proteins = extract_gcf()
    if args.inspect:
        print(json.dumps({'members': len(members), 'proteins': len(proteins), 'roles': Counter(p['role'] for p in proteins),
                          'unique_core_sequences_by_role': {role: len({p['sequence'] for p in proteins if p['role'] == role}) for role in sorted({p['role'] for p in proteins})}}, indent=2))
        return
    (RECEIPT / 'parameters.json').write_text(json.dumps(PARAMETERS, indent=2) + '\n')
    source('planning/similarity-independence-work-2026-10-11/parameters.json')
    environment = {'python': sys.version, 'executable': sys.executable, 'packages': {}}
    for package in ['rdkit', 'biopython', 'matchms', 'numpy', 'scipy', 'lxml']:
        d = metadata.distribution(package)
        environment['packages'][package] = {'version': d.version, 'RECORD_sha256': sha((d.read_text('RECORD') or '').encode())}
    (RECEIPT / ('run-' + args.stage + '.json')).write_text(json.dumps({'started': datetime.now(timezone.utc).isoformat(), 'command': sys.argv,
        'environment': environment, 'inputs_before': INPUTS, 'parameters': PARAMETERS, 'status': 'running'}, indent=2))
    if args.stage in ['chemical', 'all']:
        make_structures(relationships)
    if args.stage in ['spectral', 'all']:
        spectral_analysis()
    if args.stage in ['genomic', 'all']:
        genomic_analysis(members, proteins)
    assert all(sha((ROOT / p).read_bytes()) == digest for p, digest in INPUTS.items())
    (RECEIPT / ('run-' + args.stage + '.json')).write_text(json.dumps({'finished': datetime.now(timezone.utc).isoformat(), 'command': sys.argv,
        'environment': environment, 'inputs': INPUTS, 'parameters': PARAMETERS, 'status': 'complete', 'contract_id': contract_id(),
        'stage_outputs': stage_output_receipts(PRIMARY_OUTPUTS) if args.stage == 'all' else {},
        'outputs': {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in OUT.glob('*.tsv')}}, indent=2))
    print('Completed', args.stage, flush=True)


if __name__ == '__main__':
    main()
