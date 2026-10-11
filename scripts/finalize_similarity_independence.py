"""Join similarity outputs to typed dependence and bounded retained-asset exposure."""
import csv
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from scripts import similarity_independence as s


def components(nodes, edges):
    parent = {x: x for x in nodes}
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = root(a), root(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    groups = defaultdict(list)
    for n in nodes:
        groups[root(n)].append(n)
    return sorted(tuple(sorted(v)) for v in groups.values())


def results(name):
    return s.read_tsv('data/processed/similarity-independence-v1/' + name)


def validate_prerequisite(record, root, contract, required_outputs):
    if record.get('status') != 'complete' or record.get('contract_id') != contract:
        raise ValueError('Prerequisite incomplete or belongs to a different scientific contract')
    if not record.get('inputs') or set(record.get('stage_outputs', {})) != set(required_outputs):
        raise ValueError('Prerequisite lacks the required input/output receipt set')
    for path, digest in record['inputs'].items():
        asset = root / path
        if not asset.is_file() or s.sha(asset.read_bytes()) != digest:
            raise ValueError('Missing or changed prerequisite input: ' + path)
    for path, expected in record['stage_outputs'].items():
        asset = root / path
        if not asset.is_file():
            raise ValueError('Missing prerequisite output: ' + path)
        if s.output_projection(asset, expected['fields']) != expected:
            raise ValueError('Changed prerequisite numerical/identity output: ' + path)


def preflight():
    contract = s.contract_id()
    required = [('run-all.json', s.PRIMARY_OUTPUTS), ('run-anchors.json', s.ANCHOR_OUTPUTS)]
    checked = []
    for name, outputs in required:
        path = s.RECEIPT / name
        record = json.loads(path.read_text())
        validate_prerequisite(record, s.ROOT, contract, {(s.OUT / f).relative_to(s.ROOT).as_posix() for f in outputs})
        checked.append((path, record))
    if checked[1][1].get('parent_run_all_sha256') != s.sha(checked[0][0].read_bytes()):
        raise ValueError('Anchor receipt is not attached to the current primary run receipt')
    return checked


def dependencies(relationships, chemical, spectral):
    edges = []
    def add(a, b, kind, source, status='established', namespace='relationship', reason=''):
        edges.append({'edge_id': 'dep:' + str(len(edges) + 1), 'endpoint_a': a, 'endpoint_b': b,
                      'endpoint_namespace': namespace, 'edge_type': kind, 'source': source, 'certainty': status,
                      'rule_version': 'similarity-independence-v1', 'grouping_applicability': 'relationship_scenarios' if namespace == 'relationship' else 'measurement_or_sequence_context_only', 'reason': reason})
    for a, b in itertools.combinations(relationships, 2):
        ai, bi = a['relationship_id'], b['relationship_id']
        if a['query_id'] == b['query_id']:
            add(ai, bi, 'identical_query', s.BACKBONE[0])
        if a['pathway_group'] == b['pathway_group'] and a['pathway_group'] != 'not_adjudicated':
            add(ai, bi, 'curated_shared_pathway', s.BACKBONE[0])
        if ':AtFAC9J20:' in ai and ':AtFAC9J20:' in bi:
            add(ai, bi, 'shared_construct_host', 'docs/evidence/fac9j20-query-appraisal-2026-10-07.md', reason='Three locus envelopes; shared construct and host context, not one pathway')
        if a['cohort'] == b['cohort']:
            add(ai, bi, 'shared_study_candidate_design', s.BACKBONE[0], reason='Design dependence; no chemical identity implied')
    eligibility = s.read_tsv('data/curated/seven-admitted-member-eligibility-2026-10-03.tsv')
    s.source('data/curated/caesar-observation-groups-2026-10-02.tsv')
    acquisitions = defaultdict(set)
    for row in eligibility:
        acquisitions[row['relationship_id']].update(json.loads(row['candidate_acquisition_ids_json']))
    for a, b in itertools.combinations(sorted(acquisitions), 2):
        overlap = acquisitions[a] & acquisitions[b]
        if overlap:
            add(a, b, 'shared_source_observation', 'data/curated/seven-admitted-member-eligibility-2026-10-03.tsv',
                status='documented_candidate_join', reason=str(len(overlap)) + ' shared exact acquisition IDs; candidate observation scope, not independently authenticated biological samples')
    for r in chemical:
        if r['status'] == 'computed' and float(r['tanimoto']) >= .7:
            add(r['relationship_a'], r['relationship_b'], 'chemical_resemblance_0_7', 'chemical-pairs.tsv', 'descriptive_similarity')
    for r in spectral:
        if r['flag_0_7_6peaks'] == 'True':
            add(r['spectrum_a'], r['spectrum_b'], 'spectral_resemblance_0_7_6peaks', 'spectral-pairs.tsv', 'descriptive_similarity', 'spectrum')
    return edges, add


def spectral_provenance(spectra, spectral, add):
    trbase = 'data/processed/trichoderma-network-candidate-v1/provenance/'
    aliases = {x['candidate_id']: x['source_mgf_feature_id'] for x in s.read_tsv(trbase + 'candidate-aliases.tsv')}
    tr = s.read_tsv(trbase + 'processing/native-fragment-membership.tsv')
    by = s.read_tsv('data/processed/blackyeast-sixmsa-candidate-v1/provenance/native-memberships.tsv')
    tr_selected_path = trbase + 'processing/selected-native-spectrum-check.json'
    by_selected_path = 'data/raw/blackyeast-sixmsa-inputs-2026-10-09/selected-native-spectrum-check.json'
    tr_selected = {r['feature_id']: r for r in json.loads(s.source(tr_selected_path).read_text())}
    by_selected = {r['feature_id']: r for r in json.loads(s.source(by_selected_path).read_text())}
    native = defaultdict(set)
    energy = defaultdict(set)
    for r in tr:
        native['tr:' + r['feature_id']].add(r['acquisition'] + '|' + r['native_frame_id'])
        energy['tr:' + r['feature_id']].add(r['collision_energy'])
    for r in by:
        native[r['candidate_id']].add(r['sample_id'] + '|' + r['native_spectrum_id'])
    details = []
    lookup = {}
    for r in spectra:
        key = 'tr:' + aliases[r['feature_id']] if r['feature_id'].startswith('FLTR') else r['feature_id']
        scans = native[key]
        lookup[r['spectrum_id']] = scans
        selected = tr_selected[aliases[r['feature_id']]] if key.startswith('tr:') else by_selected[str(int(r['feature_id'].split('-C')[1]))]
        selected_event = selected['acquisition'] + '|' + str(selected.get('native_frame_id', selected.get('native_spectrum_id')))
        ce = [str(selected['collision_energy'])]
        r['native_scan'] = selected_event
        r['collision_energy'] = str(selected['collision_energy'])
        details.append({'spectrum_id': r['spectrum_id'], 'feature_id': r['feature_id'], 'pool': r['pool'],
                        'native_events': sorted(scans), 'native_event_count': len(scans), 'collision_energy_values': ce,
                        'selected_export_native_event': selected_event, 'selected_event_source': tr_selected_path if key.startswith('tr:') else by_selected_path,
                        'collision_energy_unit': 'not_recorded_in_consumed_receipt', 'instrument': 'unknown_in_consumed_membership_table', 'source_path': trbase + 'processing/native-fragment-membership.tsv' if key.startswith('tr:') else 'data/processed/blackyeast-sixmsa-candidate-v1/provenance/native-memberships.tsv',
                        'scope': 'selected unmerged native event verified by retained peak-rounding check; all feature memberships also retained'})
    details_map = {x['spectrum_id']: x for x in details}
    for r in spectral:
        a, b = r['spectrum_a'], r['spectrum_b']
        overlap = lookup[a] & lookup[b] if r['pool_a'] == r['pool_b'] else set()
        r['shared_native_event_count'] = len(overlap)
        r['exact_native_scan_equal'] = details_map[a]['selected_export_native_event'] == details_map[b]['selected_export_native_event']
        r['collision_energy_a'] = details_map[a]['collision_energy_values']
        r['collision_energy_b'] = details_map[b]['collision_energy_values']
        r['metadata_stratum'] = ('same_pool' if r['pool_a'] == r['pool_b'] else 'opposite_polarity') + ';instrument_unknown;selected_collision_energy=' + '/'.join(details_map[a]['collision_energy_values'] + details_map[b]['collision_energy_values'])
        if overlap:
            add(a, b, 'shared_native_acquisition_event', details_map[a]['source_path'], 'established', 'spectrum', 'Shared native events=' + str(len(overlap)) + '; does not establish biological identity')
    s.write_tsv('spectral-provenance.tsv', details)
    s.write_tsv('spectral-pairs.tsv', spectral)
    s.write_tsv('spectra.tsv', spectra)
    return details


def grouping(relationships, edges):
    scenarios = {
        'query_pathway': {'identical_query', 'curated_shared_pathway'},
        'construct_context': {'identical_query', 'curated_shared_pathway', 'shared_construct_host'},
        'conservative_design': {'identical_query', 'curated_shared_pathway', 'shared_construct_host', 'shared_study_candidate_design', 'shared_source_observation'},
        'similarity_sensitivity_0_7': {'identical_query', 'curated_shared_pathway', 'shared_construct_host', 'shared_study_candidate_design', 'shared_source_observation', 'chemical_resemblance_0_7', 'shared_exact_core_sequence'},
        'similarity_sensitivity_0_9': {'identical_query', 'curated_shared_pathway', 'shared_construct_host', 'shared_study_candidate_design', 'shared_source_observation', 'chemical_resemblance_0_9', 'shared_exact_core_sequence', 'genomic_core_resemblance_90_80'},
    }
    scenarios['similarity_sensitivity_0_7'].add('genomic_core_resemblance_70_80')
    nodes = sorted(r['relationship_id'] for r in relationships)
    by_id = {r['relationship_id']: r for r in relationships}
    rows, summary = [], []
    for scenario, kinds in scenarios.items():
        ee = [e for e in edges if e['endpoint_namespace'] == 'relationship' and e['edge_type'] in kinds and e['endpoint_a'] in by_id and e['endpoint_b'] in by_id]
        groups = components(nodes, [(e['endpoint_a'], e['endpoint_b']) for e in ee])
        complete = []
        for n, group in enumerate(groups, 1):
            gid = scenario + ':' + str(n)
            gr = [by_id[x] for x in group]
            if any(x['input_state'] == 'complete' for x in gr):
                complete.append(gid)
            counts = {'relationships': len(gr), 'unique_queries': len({x['query_id'] for x in gr}),
                      'adjudicated_pathway_groups': len({x['pathway_group'] for x in gr if x['pathway_group'] != 'not_adjudicated'}),
                      'complete_relationships': sum(x['input_state'] == 'complete' for x in gr),
                      'partial_relationships': sum(x['input_state'] == 'partial' for x in gr),
                      'missing_relationships': sum(x['input_state'] == 'missing' for x in gr)}
            causes = [e['edge_id'] for e in ee if e['endpoint_a'] in group and e['endpoint_b'] in group]
            for r in gr:
                rows.append({'scenario': scenario, 'edge_rules': '|'.join(sorted(kinds)), 'group_id': gid, 'relationship_id': r['relationship_id'],
                             'query_id': r['query_id'], 'pathway_group': r['pathway_group'], 'input_state': r['input_state'], 'counts': counts,
                             'merger_edges': causes, 'unresolved_edges': 'Missing representations and source/weight exposure unresolved',
                             'parent_frozen_group': r['analysis_group'], 'split_feasibility': 'not_established',
                             'reason': 'Descriptive grouping only; no positive scientific justification to split the frozen complete-analysis group; remaining groups lack complete evaluated inputs'})
        summary.append({'scenario': scenario, 'components': len(groups), 'components_with_complete_relationships': len(complete),
                        'relationships': 30, 'queries': 16, 'authoritative_complete_analysis_groups': 1, 'holdout_established': False})
    s.write_tsv('group-scenarios.tsv', rows)
    s.write_tsv('group-summary.tsv', summary)
    return summary


def method_version_fields(method, task, npmanifest):
    if method == 'Rosetta_reference_only':
        return {'method_version': 'not_applicable_reference_only', 'method_version_source': 'No Rosetta method was executed', 'upstream_method_version': 'unknown'}
    if method == 'NPClassScore' or method == npmanifest.get('method_id'):
        return {'method_version': npmanifest.get('implementation_version', 'unknown'),
                'method_version_source': 'data/manifests/npclassscore-method.json#implementation_version',
                'upstream_method_version': npmanifest.get('upstream', {}).get('version', 'unknown')}
    if method in task.get('method_ids', '').split('|'):
        return {'method_version': task.get('method_version') or 'unknown',
                'method_version_source': s.BACKBONE[3] + '#method_version', 'upstream_method_version': 'unknown'}
    return {'method_version': 'unknown', 'method_version_source': 'No named method release version in consumed execution record; exact code/weight hashes retained',
            'upstream_method_version': 'unknown'}


def exposure(relationships, structures):
    tasks = {r['relationship_id']: r for r in s.read_tsv(s.BACKBONE[3])}
    table = s.read_tsv(s.TABLE)
    refids = {r['compound_name'].split('_', 1)[0] for r in table}
    with s.source(s.ROSETTA).open(encoding='utf-8-sig', newline='') as f:
        rosetta = list(csv.DictReader(f))
    rosids = {r['mibig_id'] for r in rosetta}
    by_id = {r['relationship_id']: r for r in structures}
    npmanifest = json.loads(s.source('data/manifests/npclassscore-method.json').read_text())
    model_versions = {}
    for name in ['binary_models', 'binary_models_negative_mode', 'SVM_model', 'SVM_model_negative_mode']:
        path = 'data/interim/admitted-input-coverage-2026-10-09/spec2class/' + name + '-manifest.json'
        manifest = json.loads(s.source(path).read_text())
        model_versions[name] = (manifest.get('sha') or 'unknown', path)
    rows = []
    def add(r, method, layer, asset, status, match, completeness, universe, reason, run='not_executed_reference_audit', asset_hash=None):
        version, version_source = 'unknown', 'No semantic asset version in consumed record; asset SHA256 retained separately'
        if asset == s.TABLE:
            version = npmanifest['reference_asset']['reference_database']
            version_source = 'data/manifests/npclassscore-method.json#reference_asset.reference_database'
        elif asset == s.BACKBONE[3]:
            version, version_source = 'task-exposure-v1', 'explicit versioned table filename'
        elif asset.startswith('data/manifests/') and (s.ROOT / asset).is_file():
            manifest = json.loads(s.source(asset).read_text())
            version = 'manifest_schema=' + str(manifest.get('schema_version', 'unknown'))
            version_source = asset + '#schema_version'
        elif method == 'Spec2Class' and ('.pt' in asset or '.sav' in asset):
            name = 'SVM_model' if '.sav' in asset else 'binary_models'
            if 'negative' in asset or 'negative' in run:
                name += '_negative_mode'
            revision, locator = model_versions[name]
            version, version_source = 'repository_revision=' + revision, locator + '#sha; executed content hash is recorded separately'
        rows.append({'relationship_id': r['relationship_id'], 'method': method, 'run': run, 'method_layer': layer,
                     **method_version_fields(method, tasks[r['relationship_id']], npmanifest),
                     'execution_scope': 'reference_only' if layer == 'public_reference_membership' else 'not_applicable' if method == 'not_applicable' else 'executed_task_or_predictor_record',
                     'asset': asset, 'asset_version': version, 'asset_version_source': version_source,
                     'asset_sha256': asset_hash or s.INPUTS.get(asset, ''), 'searched_universe': universe, 'roster_completeness': completeness,
                     'matching_rule': match, 'status': status, 'reason': reason, 'source_locator': tasks[r['relationship_id']]['source_records']})
    for p in ['data/manifests/baseline-methods.json', 'data/manifests/phylogeny-method.json', 'data/manifests/npclassscore-method.json', 'data/manifests/npclassscore-adapter.json']:
        s.source(p)
    for r in relationships:
        task = tasks[r['relationship_id']]
        for method in task['method_ids'].split('|'):
            add(r, method, 'source_label_selection', s.BACKBONE[3], 'confirmed_overlap', 'explicit task exposure statement', 'task_record', '30 admitted relationship task records', task['prior_exposure'], task['task_version'])
            if method in {'global_prevalence', 'prevalence_difference', 'metcalf_raw', 'metcalf_standardized'}:
                add(r, method, 'learned_training', 'data/manifests/baseline-methods.json', 'not_applicable', 'no_learned_training', 'not_applicable', 'deterministic implementation', 'Retrospective source selection remains exposed', task['task_version'])
        st = by_id[r['relationship_id']]
        hit = re.search(r'BGC\d{7}', st['source_locator'])
        bgc = hit.group() if hit else None
        for method, asset, ids, universe in [('NPClassScore', s.TABLE, refids, 'all 2112 rows of pinned bundled class table'),
                                               ('Rosetta_reference_only', s.ROSETTA, rosids, str(len(rosetta)) + ' retained mapping rows; no executed Rosetta experiment')]:
            status = 'confirmed_overlap' if bgc in ids else 'partial_roster_no_match' if bgc else 'unknown'
            add(r, method, 'public_reference_membership', asset, status, 'exact_unversioned_BGC_ID=' + (bgc or 'unavailable_supported_ID'),
                'complete_declared_file; incomplete_relative_to_all_public_references', universe,
                'BGC identifier membership only; not exact accession-version sequence equality and not model-training evidence')
    assets = []
    for rid, runpath in [('burger2025:ilicicolin:H', 'data/processed/trichoderma-spec2class-positive-v1-attempt2/run.json'),
                         ('blackyeast2026:sixmsa:POP4', 'data/processed/blackyeast-sixmsa-spec2class-negative-v1-attempt2/run.json')]:
        run = json.loads(s.source(runpath).read_text())
        r = next(r for r in relationships if r['relationship_id'] == rid)
        hashes = {}
        for key, value in run.items():
            if isinstance(value, dict) and ('hash' in key or 'weight' in key):
                hashes.update({k: v for k, v in value.items() if isinstance(v, str) and re.fullmatch(r'[a-f0-9]{64}', v) and ('.pt' in k or '.sav' in k)})
        for asset, digest in hashes.items():
            assets.append({'relationship_id': rid, 'asset': asset, 'asset_sha256': digest, 'source_run': runpath, 'hash_basis': 'actual executed run receipt; no new weight download'})
            add(r, 'Spec2Class', 'weight_specific_training', asset, 'unknown', 'no complete weight-specific training roster retained', 'unavailable',
                'Weight hash identifies asset only; examples and Rosetta mappings excluded as training substitutes', 'No training-membership claim', runpath, digest)
        if not hashes:
            add(r, 'Spec2Class', 'weight_specific_training', runpath, 'unknown', 'weight-specific roster unavailable', 'unavailable', 'actual executed run receipt', 'No training-membership claim', runpath)
    s.write_tsv('exposure.tsv', rows)
    s.write_tsv('executed-model-assets.tsv', assets, ['relationship_id', 'asset', 'asset_sha256', 'source_run', 'hash_basis'])
    return rows


def representations(relationships, structures, spectra, members, anchors, proteins):
    rows = []
    st = {r['relationship_id']: r for r in structures}
    for r in relationships:
        view = r['evaluation_query_view'].removeprefix('source:')
        mm = [m for m in members if m['family'] == view]
        aa = [m for m in anchors if m['source_labels'] == r['query_id']]
        for m in mm + aa:
            rows.append({'relationship_id': r['relationship_id'], 'query_id': r['query_id'], 'member_id': m['member_id'], 'representation_kind': 'genomic',
                         'source_path': m['source_path'], 'source_sha256': s.sha((s.ROOT / m['source_path']).read_bytes()),
                         'boundaries_or_identifier': m['source_labels'], 'completeness': m['completeness'], 'status': 'available',
                         'reason': 'accepted_scope_only; reference/sample/construct distinctions retained', 'evidence_locator': r['evidence_packet']})
        if not (mm or aa):
            raise ValueError('Missing genomic accounting ' + r['relationship_id'])
        sr = st[r['relationship_id']]
        rows.append({'relationship_id': r['relationship_id'], 'query_id': r['query_id'], 'member_id': sr['structure_id'], 'representation_kind': 'chemical',
                     'source_path': sr['source_path'], 'source_sha256': s.sha((s.ROOT / sr['source_path']).read_bytes()),
                     'boundaries_or_identifier': sr['source_locator'], 'completeness': sr['stereochemistry'], 'status': sr['mapping_status'], 'reason': sr['reason'], 'evidence_locator': r['evidence_packet']})
        ss = [x for x in spectra if x['feature_id'] == r['evaluation_target_key']]
        rows.append({'relationship_id': r['relationship_id'], 'query_id': r['query_id'], 'member_id': '|'.join(x['spectrum_id'] for x in ss), 'representation_kind': 'target_spectral',
                     'source_path': '|'.join(x['source_path'] for x in ss), 'source_sha256': '|'.join(x['source_sha256'] for x in ss),
                     'boundaries_or_identifier': r['evaluation_target_key'], 'completeness': 'native_join' if ss else 'unavailable',
                     'status': 'available' if ss else 'unavailable', 'reason': '' if ss else 'No established native target join; no mass/RT bridge inferred', 'evidence_locator': r['evidence_packet']})
    s.write_tsv('representations.tsv', rows)
    # Every protein, including excluded noncore records, has explicit comparison eligibility.
    eligibility = [{'protein_id': p['protein_id'], 'member_id': p['member_id'], 'role': p['role'],
                    'status': 'eligible_compatible_role_pairs' if p['role'] != 'unclassified' and p['sequence'] else 'not_comparable',
                    'reason': '' if p['role'] != 'unclassified' and p['sequence'] else 'No compatible core role from retained annotation; no whole-cluster dissimilarity claim'} for p in proteins]
    s.write_tsv('genomic-eligibility.tsv', eligibility)
    return rows


def trichoderma_disposition(query, target):
    accepted = {'ETS03591.1': 'EGR50061.1', 'ETS03592.1': 'EGR50062.1', 'ETS03593.1': 'EGR50286.1',
                'ETS03594.1': 'EGR50063.1', 'ETS03595.1': 'EGR50287.1', 'ETS03597.1': 'EGR50064.1', 'ETS03598.1': 'EGR50288.1'}
    if accepted.get(query) != target:
        return 'rejected_weak_search_candidate_not_correspondence'
    if query == 'ETS03598.1':
        return 'old_partial_gene_model; source_extended_model_separately_supported'
    return 'accepted_locus_gene_model_correspondence; annotation_discrepancy_retained'


def reuse_correspondence():
    rows = []
    for path in ['data/curated/griseofulvin-sampled-correspondence-2026-10-02.tsv', 'data/curated/notoamide-b-sampled-correspondence-2026-10-03.tsv']:
        for r in s.read_tsv(path):
            assert abs(float(r['identity_pct']) - int(r['matches']) / int(r['paired_residues']) * 100) < 1e-8
            assert abs(float(r['reference_coverage_pct']) - int(r['paired_residues']) / int(r['reference_length']) * 100) < 1e-8
            assert abs(float(r['sample_coverage_pct']) - int(r['paired_residues']) / int(r['sample_length']) * 100) < 1e-8
            rows.append({'source': path, 'relationship_id': r['relationship_id'], 'protein_a': r['reference_id'], 'protein_b': r['sample_id'],
                         'sequence_sha256_a': r['reference_sha256'], 'sequence_sha256_b': r['sample_sha256'], 'identity': float(r['identity_pct']) / 100,
                         'coverage_a': float(r['reference_coverage_pct']) / 100, 'coverage_b': float(r['sample_coverage_pct']) / 100,
                         'score': r['score'], 'method': r['method'], 'status': 'reused_saved_correspondence; integer_arithmetic_checked'})
    for r in s.read_tsv('data/curated/acetylaszonalenin-sampled-correspondence-2026-10-03.tsv'):
        rows.append({'source': 'data/curated/acetylaszonalenin-sampled-correspondence-2026-10-03.tsv', 'relationship_id': r['review_key'],
                     'protein_a': r['protein_id'], 'protein_b': r['locus_tag'], 'sequence_sha256_a': r['translation_sha256'], 'sequence_sha256_b': r['translation_sha256'],
                     'identity': 1., 'coverage_a': 1., 'coverage_b': 1., 'score': None, 'method': r['comparison_method'], 'status': 'reused_exact_correspondence'})
    trich_packet = 'docs/evidence/trichoderma-qm6a-correspondence-2026-10-07.md'
    s.source(trich_packet)
    rejected = []
    for r in s.read_tsv('data/raw/trichoderma-qm6a-correspondence-2026-10-07/protein-comparison.tsv'):
        if r['rank_by_shared_distinct_5mers'] == '1':
            disposition = trichoderma_disposition(r['query_protein'], r['target_protein'])
            record = {'source': 'data/raw/trichoderma-qm6a-correspondence-2026-10-07/protein-comparison.tsv', 'relationship_id': 'burger2025:ilicicolin:H',
                         'protein_a': r['query_protein'], 'protein_b': r['target_protein'], 'sequence_sha256_a': '', 'sequence_sha256_b': '',
                         'identity': float(r['identity_paired_percent']) / 100, 'coverage_a': float(r['query_paired_coverage_percent']) / 100,
                         'coverage_b': float(r['target_paired_coverage_percent']) / 100, 'score': r['global_alignment_score'],
                         'method': 'retained bounded shared-5mer screen followed by global alignment; source packet decides correspondence',
                         'status': disposition, 'source_packet': trich_packet, 'source_packet_sha256': s.INPUTS[trich_packet],
                         'hash_scope': 'sequence hashes absent from this comparison table; record not substituted into alignment cache'}
            (rejected if disposition.startswith('rejected') else rows).append(record)
    s.write_tsv('reused-correspondence.tsv', rows)
    s.write_tsv('rejected-sequence-search-candidates.tsv', rejected)
    return rows


def structure_dispositions(relationships, structures):
    table = s.read_tsv(s.TABLE)
    with s.source(s.ROSETTA).open(encoding='utf-8-sig', newline='') as handle:
        ros = list(csv.DictReader(handle))
    attempts = []
    by_id = {r['relationship_id']: r for r in relationships}
    for row in structures:
        r = by_id[row['relationship_id']]
        packet = r['evidence_packet']
        if (s.ROOT / packet).is_file():
            s.source(packet)
        aliases = [r['product'].lower().split('-associated')[0].split(' (')[0]]
        if r['relationship_id'] == 'hex2018:PKS15:compound3':
            aliases = ['orsellinic acid']
        if r['relationship_id'] == 'blackyeast2026:sixmsa:POP4':
            aliases = ['6-methylsalicylic acid', '6-methylsalicylic-acid']
        if 'benzomalvin A/D' == r['product']:
            aliases = ['benzomalvin A', 'benzomalvin D']
        hits = []
        for candidate in table:
            name = candidate['compound_name'].split('_', 1)[1]
            if name.lower() in [x.lower() for x in aliases]:
                hits.append({'source': s.TABLE, 'id': candidate['compound_name'], 'text': candidate['smiles']})
        for candidate in ros:
            if candidate['mibig_name'].lower() in [x.lower() for x in aliases]:
                hits.append({'source': s.ROSETTA, 'id': candidate['mibig_id'] + ':' + candidate['mibig_name'], 'text': candidate['mibig_smiles']})
        reason = row['reason']
        if row['mapping_status'] == 'unavailable':
            reason = ('Named candidate representation exists, but retained source packet has no verified structure-ID crosswalk; name equality rejected. '
                      if hits else 'No exact-target structure row in either named retained table; related congener names are not substitutes. ')
            if 'putative' in r['product'] or 'proposed' in r['product']:
                reason += 'Target structure remains proposed/putative; no resolved machine-readable scenario representation. '
            if 'A/D' in r['product'] or 'regioisomer' in r['product'] or 'mixture' in r['product']:
                reason += 'Alternative or mixture scope unresolved; no selected best assignment. '
            reason += 'Reopen for exact source-supported structure crosswalk or checked drawing transcription.'
            row['reason'] = reason
        attempts.append({'relationship_id': r['relationship_id'], 'aliases_searched': aliases, 'candidate_records': hits,
                         'source_packet': packet, 'mapping_status': row['mapping_status'], 'reason': reason,
                         'search_scope': 'two plan-named retained machine-readable tables and existing evidence packet; no external retrieval'})
    s.write_tsv('structure-mapping-attempts.tsv', attempts)
    s.write_tsv('structures.tsv', structures)
    return attempts


def genomic_summary(genomic):
    groups = defaultdict(list)
    for r in genomic:
        if r['status'] == 'computed':
            groups[tuple(sorted((r['family_a'], r['family_b'])))].append(r)
    rows = []
    for (a, b), pairs in sorted(groups.items()):
        vals = sorted(float(r['identity']) for r in pairs)
        rows.append({'family_a': a, 'family_b': b, 'comparison': 'within' if a == b else 'between', 'compatible_protein_pairs': len(pairs),
                     'represented_member_pairs': len({tuple(sorted((r['member_a'], r['member_b']))) for r in pairs}),
                     'identity_min': vals[0], 'identity_median': __import__('statistics').median(vals), 'identity_max': vals[-1],
                     'qualifies_70_80': sum(r.get('qualifies_70_80') == 'True' for r in pairs), 'qualifies_90_80': sum(r.get('qualifies_90_80') == 'True' for r in pairs),
                     'exact_duplicate_protein_pairs': sum(r.get('exact_equal') == 'True' for r in pairs),
                     'scope': 'source_annotated_compatible_cores; not whole_cluster; repeated proteins and reference anchors retained'})
    s.write_tsv('genomic-family-summary.tsv', rows)
    return rows


def reciprocal_and_loci(genomic, members):
    best = defaultdict(lambda: -float('inf'))
    grouped = defaultdict(list)
    for r in genomic:
        grouped[tuple(sorted((r['member_a'], r['member_b'])))].append(r)
        if r['status'] == 'computed':
            for p, other in [(r['protein_a'], r['member_b']), (r['protein_b'], r['member_a'])]:
                best[p, other] = max(best[p, other], float(r['score']))
    for r in genomic:
        r['reciprocal_best_tie'] = r['status'] == 'computed' and float(r['score']) == best[r['protein_a'], r['member_b']] and float(r['score']) == best[r['protein_b'], r['member_a']]
    loci = []
    for a, b in itertools.combinations(sorted(members, key=lambda m: m['member_id']), 2):
        rr = [r for r in grouped[a['member_id'], b['member_id']] if r['status'] == 'computed']
        row = {'member_a': a['member_id'], 'member_b': b['member_id'], 'family_a': a['family'], 'family_b': b['family'],
               'annotated_proteins_a': a['protein_count'], 'annotated_proteins_b': b['protein_count'], 'compatible_core_pairs': len(rr),
               'status': 'core_only' if rr else 'unavailable_no_compatible_annotated_core',
               'reason': 'Fractions are lower bounds using compatible annotated cores; unclassified proteins are unassessed'}
        for threshold in [70, 90]:
            qualified = [r for r in rr if r['reciprocal_best_tie'] and r['qualifies_' + str(threshold) + '_80'] == 'True']
            ai = {r['protein_a'] if r['member_a'] == a['member_id'] else r['protein_b'] for r in qualified}
            bi = {r['protein_b'] if r['member_b'] == b['member_id'] else r['protein_a'] for r in qualified}
            row['annotated_fraction_a_' + str(threshold)] = len(ai) / int(a['protein_count']) if int(a['protein_count']) else None
            row['annotated_fraction_b_' + str(threshold)] = len(bi) / int(b['protein_count']) if int(b['protein_count']) else None
            row['reciprocal_order_pairs_' + str(threshold)] = [[r['order_a'], r['order_b']] if r['member_a'] == a['member_id'] else [r['order_b'], r['order_a']] for r in qualified]
        loci.append(row)
    s.write_tsv('all-genomic-pairs.tsv', genomic)
    s.write_tsv('all-genomic-locus-pairs.tsv', loci)
    return loci


def heatmap(relationships, chemical):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    n = len(relationships)
    idx = {r['relationship_id']: i for i, r in enumerate(relationships)}
    matrix = np.full((n, n), np.nan)
    for r in chemical:
        if r['status'] == 'computed':
            i, j = idx[r['relationship_a']], idx[r['relationship_b']]
            matrix[i, j] = matrix[j, i] = float(r['tanimoto'])
            matrix[i, i] = matrix[j, j] = 1
    fig, ax = plt.subplots(figsize=(12, 10))
    cmap = plt.get_cmap('viridis').copy()
    cmap.set_bad('#d6d6d6')
    im = ax.imshow(matrix, vmin=0, vmax=1, cmap=cmap)
    labels = [r['product'][:32] for r in relationships]
    ax.set_xticks(range(n), labels, rotation=90, fontsize=6)
    ax.set_yticks(range(n), labels, fontsize=6)
    ax.set_title('Supported structure Tanimoto; grey = unavailable')
    fig.colorbar(im, ax=ax, shrink=.65)
    fig.tight_layout()
    fig.savefig(s.OUT / 'chemical-heatmap.png', dpi=180)
    plt.close(fig)


def main():
    # All completion, lineage and scientific output checks precede any enrichment write.
    prerequisites = preflight()
    relationships = s.read_tsv(s.BACKBONE[0])
    chemical, spectral, spectra, structures = (results(n) for n in ['chemical-pairs.tsv', 'spectral-pairs.tsv', 'spectra.tsv', 'structures.tsv'])
    structure_dispositions(relationships, structures)
    members, anchors, proteins, anchor_proteins = (results(n) for n in ['gcf-members.tsv', 'anchor-members.tsv', 'proteins.tsv', 'anchor-proteins.tsv'])
    genomic = results('genomic-pairs.tsv') + results('anchor-genomic-pairs.tsv')
    edges, add = dependencies(relationships, chemical, spectral)
    details = spectral_provenance(spectra, spectral, add)
    family_to_relations = defaultdict(list)
    for r in relationships:
        family_to_relations[r['evaluation_query_view'].removeprefix('source:')].append(r['relationship_id'])
        family_to_relations['anchor:' + r['query_id']].append(r['relationship_id'])
    for r in genomic:
        if r.get('qualifies_70_80') == 'True':
            aa = family_to_relations[r['member_a']] if r['member_a'].startswith('anchor:') else family_to_relations[r['family_a']]
            bb = family_to_relations[r['member_b']] if r['member_b'].startswith('anchor:') else family_to_relations[r['family_b']]
            for a, b in itertools.product(aa, bb):
                if a != b:
                    a, b = sorted((a, b))
                    add(a, b, 'genomic_core_resemblance_70_80', 'genomic-pairs.tsv;anchor-genomic-pairs.tsv', 'plausible_dependence_sequence_only',
                        reason=r['protein_a'] + '|' + r['protein_b'] + '; compatible core screen only, not established pathway equivalence')
                    if r.get('qualifies_90_80') == 'True':
                        add(a, b, 'genomic_core_resemblance_90_80', 'genomic-pairs.tsv;anchor-genomic-pairs.tsv', 'plausible_dependence_sequence_only',
                            reason=r['protein_a'] + '|' + r['protein_b'] + '; compatible core screen only, not established pathway equivalence')
        if r.get('exact_equal') == 'True':
            add(r['protein_a'], r['protein_b'], 'exact_core_sequence', 'genomic-pairs.tsv;anchor-genomic-pairs.tsv', 'established_sequence_only', 'protein', 'Exact protein equality does not prove shared pathway or product')
            aa = family_to_relations[r['member_a']] if r['member_a'].startswith('anchor:') else family_to_relations[r['family_a']]
            bb = family_to_relations[r['member_b']] if r['member_b'].startswith('anchor:') else family_to_relations[r['family_b']]
            for a, b in itertools.product(aa, bb):
                if a < b:
                    add(a, b, 'shared_exact_core_sequence', 'genomic-pairs.tsv;anchor-genomic-pairs.tsv', 'plausible_dependence_sequence_only',
                        reason=r['protein_a'] + '|' + r['protein_b'] + '; family member protein equality only; not biological pathway equivalence')
                elif b < a:
                    add(b, a, 'shared_exact_core_sequence', 'genomic-pairs.tsv;anchor-genomic-pairs.tsv', 'plausible_dependence_sequence_only',
                        reason=r['protein_a'] + '|' + r['protein_b'] + '; family member protein equality only; not biological pathway equivalence')
    groups = grouping(relationships, edges)
    exposed = exposure(relationships, structures)
    reps = representations(relationships, structures, spectra, members, anchors, proteins + anchor_proteins)
    reused = reuse_correspondence()
    families = genomic_summary(genomic)
    loci = reciprocal_and_loci(genomic, members + anchors)
    s.write_tsv('dependence-edges.tsv', edges)
    heatmap(relationships, chemical)
    expected = {'chemical': 435, 'spectral': 72771, 'relationships': 30, 'queries': 16}
    assert len(chemical) == expected['chemical'] and len(spectral) == expected['spectral']
    assert {r['relationship_id'] for r in reps} == {r['relationship_id'] for r in relationships}
    for rows, a, b, metric in [(chemical, 'relationship_a', 'relationship_b', 'tanimoto'), (spectral, 'spectrum_a', 'spectrum_b', 'cosine')]:
        assert len({(r[a], r[b]) for r in rows}) == len(rows)
        assert all(r[a] < r[b] for r in rows)
        assert all((r[metric] == '') == (r['status'] != 'computed') for r in rows)
    summary = {'relationships': 30, 'queries': 16, 'input_states': dict(Counter(r['input_state'] for r in relationships)),
               'supported_structures': sum(r['mapping_status'] == 'supported' for r in structures), 'chemical_computed': sum(r['status'] == 'computed' for r in chemical),
               'spectra': len(spectra), 'spectral_computed': sum(r['status'] == 'computed' for r in spectral),
               'spectral_flags_07': sum(r['flag_0_7_6peaks'] == 'True' for r in spectral), 'spectral_flags_09': sum(r['flag_0_9_6peaks'] == 'True' for r in spectral),
               'gcf_members': len(members), 'gcf_proteins': len(proteins), 'anchor_members': len(anchors), 'anchor_proteins': len(anchor_proteins),
               'genomic_pairs': len(genomic), 'genomic_computed': sum(r['status'] == 'computed' for r in genomic),
               'dependence_edges': len(edges), 'group_scenarios': groups, 'exposure_rows': len(exposed), 'reused_correspondence_rows': len(reused)}
    (s.OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    report = f'''# Similarity and dependence in the retained benchmark

Analysis completed 11 October 2026 under `protocol/similarity-independence-v1.md`. This companion analysis preserves 30 admitted relationships, 16 query identities and coverage of 11 complete, two partial and 17 missing. No labels, retrieval scores, frozen groups or release ZIPs changed.

Five source-specific BGC/product crosswalks support machine-readable connectivity representations: acetylaszonalenin, emericellamide A, griseofulvin, fellutamide B and aspernidine A. All ten eligible pairs were computed; the other 425 relationship pairs are unavailable. Their Morgan Tanimoto values range from {min(float(r['tanimoto']) for r in chemical if r['status']=='computed'):.4f} to {max(float(r['tanimoto']) for r in chemical if r['status']=='computed'):.4f}; none reaches 0.7. This sparse subset cannot establish that the entire benchmark is chemically diverse. Source keys omit stereochemical distinctions present in supplied SMILES, so chiral sensitivity is withheld pending source-level reconciliation. Formula strings were calculated; independent source formula checks are unavailable. No source drawings were transcribed, no proposed valactamide structures were invented and benzomalvin A/D remains an unresolved set without machine-readable alternatives.

![Chemical similarity matrix](../../data/processed/similarity-independence-v1/chemical-heatmap.png)

The genomic analysis covers all {len(members)} displayed members and {len(proteins)} proteins in seven source-selected GCFs, plus {len(anchors)} accepted locus/construct/CDS anchors containing {len(anchor_proteins)} annotated proteins. Of {len(genomic)} cross-member core pair records, {summary['genomic_computed']} have compatible source-annotated roles and numerical alignments. Incompatible roles remain null. The family summary gives within/between distributions, represented member-pair counts, extremes and identity/coverage screens. Reciprocal best ties and gene order are retained across bounded member pairs, including accepted anchors. Fractions use all displayed annotated proteins as denominators but only source-annotated cores in the numerator, so they are lower bounds on qualifying protein content, not estimates of whole-cluster similarity. Unclassified proteins cannot establish dissimilarity. Reference intervals, construct envelopes, native/reference windows and single CDS are labeled separately; sequence similarity does not validate a biological link. Saved griseofulvin, notoamide, acetylaszonalenin and Trichoderma correspondence records are reused with their original scope. Integer identity/coverage arithmetic was checked independently where retained.

All 91 Trichoderma and 291 black-yeast native joined exports survived preprocessing. There are 4,095 and 42,195 within-pool pairs respectively, totaling 46,290. The 26,481 cross-pool pairs are excluded because explicit native-export charges are positive and negative respectively. {summary['spectral_flags_07']} pairs meet cosine >=0.7 with at least six matched peaks; {summary['spectral_flags_09']} meet 0.9. These are resemblance flags, not new chemical assignments. Native event memberships, selected unmerged scan IDs and source collision-energy values (20 for Trichoderma; 40 for black yeast, units not recorded in the consumed receipts) are retained in `spectral-provenance.tsv`; unknown instrument/energy fields stay unknown. Shared source events are recorded separately from exact peak-list duplication. The selected exported scans are verified against retained native peak-rounding receipts. None supplies historical Caesar native joins. The remaining seven Trichoderma and 958 black-yeast candidate spectra remain unavailable.

Eight valactamide relationships share one query and four benzomalvin relationships share another. Their three AtFAC9J20 locus envelopes share a construct/host context but are not one pathway. Typed edges preserve this distinction. The grouping tables include query/pathway, construct-context, conservative-design and similarity sensitivity scenarios. Each row prints its merger edge IDs and frozen parent group. `not_adjudicated` is never treated as evidence of a shared or distinct pathway. Exact acquisition IDs come from the retained observation/member eligibility ledgers, without inferring independent cultures from assembly strings.

The conservative design scenario has {next(g['components'] for g in groups if g['scenario']=='conservative_design')} components, only {next(g['components_with_complete_relationships'] for g in groups if g['scenario']=='conservative_design')} containing complete evaluated relationships. These are grouping scenarios, not independent replicates. A future grouped holdout is not established: the one frozen complete-analysis group remains intact, and other components lack complete evaluated inputs. Between-group uncertainty cannot be estimated from that single complete group.

The exposure table separates source/label selection, exact unversioned BGC membership in declared public-reference files and weight-specific training membership. It records deterministic method version 0.1.0, strict NPClassScore implementation 1.0.0 and its inspected upstream NPLinker 1.2.0 separately. Asset versions identify the MIBiG 2.0 table or retained model-repository revisions; missing semantic versions stay unknown. The five supported structure crosswalks supply bounded stable-ID checks. The complete pinned class-table file is not a complete training roster; Rosetta's mapping is reference context and no Rosetta experiment was run. Actual positive/negative Spec2Class execution receipts identify the consumed weight hashes, while their weight-specific training membership remains unknown. Deterministic controls have no learned training set but retain retrospective source-selection exposure. No no-match status means unexposed.

Software checks cover all 30 IDs, 435 chemical relationship pairs, 72,771 spectral pairs, null-versus-zero values, pair ordering, exact duplicate fixtures, an independent bit intersection/union fixture, hand-counted alignment arithmetic, a cosine fixture of 0.48, sparse-peak filtering and alternative-set ranges. Repeated fixture results and input hashes are recorded in the work receipts. Automated checks do not replace chemical or biological review; that review remains pending. The analysis provides no new evidence that an unresolved genome-product link is false.

Reproduction: use the recorded environment, then run `python scripts/similarity_independence.py --stage all`, `python -m scripts.similarity_locus_anchors`, and `python -m scripts.finalize_similarity_independence`. Existing alignment caches are resumable only under the frozen settings and sequence hashes. Results and exact consumed-input hashes are in `data/processed/similarity-independence-v1/manifest.json`.
'''
    report_path = s.ROOT / 'docs/evaluation/similarity-independence-v1.md'
    report_path.write_text(report, encoding='utf-8')
    inputs = {}
    environments = {}
    stage_receipts = []
    for path, run in prerequisites:
        inputs.update(run.get('inputs', {}))
        stage_receipts.append({'path': path.relative_to(s.ROOT).as_posix(), 'sha256': s.sha(path.read_bytes()),
                               'status': run.get('status'), 'executed_runner_sha256': run.get('inputs', {}).get('scripts/similarity_independence.py'),
                               'output_hash_scope': 'intermediate outputs at that stage; metadata enrichment and review fixes may supersede them'})
        if 'environment' in run:
            environments[path.name] = run['environment']
    inputs.update({p: h for p, h in s.INPUTS.items() if not p.startswith('data/processed/similarity-independence-v1/')})
    for path in ['scripts/similarity_independence.py', 'scripts/similarity_locus_anchors.py', 'scripts/finalize_similarity_independence.py', 'tests/test_similarity_independence.py', 'tests/test_similarity_dependence.py',
                 'planning/similarity-independence-work-2026-10-11/executed-runner-before-cache-guard.py',
                 'planning/similarity-independence-work-2026-10-11/alignment-cache.metadata.json', 'planning/similarity-independence-work-2026-10-11/anchor-alignment-cache.metadata.json',
                 'planning/similarity-independence-work-2026-10-11/alignment-settings.txt']:
        inputs[path] = s.sha((s.ROOT / path).read_bytes())
    changed = [p for p, h in inputs.items() if s.sha((s.ROOT / p).read_bytes()) != h]
    assert not changed, changed
    manifest = {'schema_version': 1, 'status': 'complete_with_representation_limits', 'created_utc': datetime.now(timezone.utc).isoformat(),
                'command': sys.argv, 'parameters': s.PARAMETERS, 'environment': environments, 'inputs': inputs, 'summary': summary,
                'stage_receipts': stage_receipts, 'execution_history': 'Original executed runner preserved; cache guard added after completed compute with explicit verified migration. Final output hashes below are authoritative for enriched results.',
                'outputs': {p.relative_to(s.ROOT).as_posix(): s.sha(p.read_bytes()) for p in s.OUT.iterdir() if p.is_file() and p.name != 'manifest.json'},
                'report': {'path': str(report_path.relative_to(s.ROOT)), 'sha256': s.sha(report_path.read_bytes())},
                'failures': [], 'limitations': ['25 structures unavailable', 'source_stereochemistry_review_pending', 'noncore_roles_unclassified', 'no complete weight-specific training roster', 'no new independent holdout'],
                'protected_inputs_unchanged': True, 'scientific_review': 'pending; automated checks only'}
    (s.OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
