"""Strict threshold-tiered NPClassScore adapter using documented public APIs."""

import argparse
import copy
import json
import math
import os
from pathlib import Path
import sys
import tempfile

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.npclassscore import load_class_table, score_classes

METHOD_ID = 'npclassscore_threshold_tiered_metcalf_strict'
METHOD_VERSION = '1'
THRESHOLD = 0.25
IDENTITIES = ('track_id', 'query_type', 'candidate_universe_id')
PROVENANCE = ('genomic_classes', 'spectral_class_predictions', 'feature_spectrum_joins', 'class_reference_exposure')


def _string(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name} must be a nonempty string')
    return value


def _object(value, allowed, required, name):
    if not isinstance(value, dict) or set(value) - set(allowed) or set(required) - set(value):
        raise ValueError(f'{name} has malformed, missing, or unknown fields')


def _ids(value, name):
    if not isinstance(value, list) or not value:
        raise ValueError(f'{name} must be a nonempty ID list')
    for item in value:
        _string(item, name)
    if len(set(value)) != len(value):
        raise ValueError(f'{name} has duplicate IDs')


def _classes(value, levels, genomic):
    if value is None:
        return {}
    _object(value, levels, (), 'classes')
    for terms in value.values():
        if genomic:
            if not isinstance(terms, list):
                raise ValueError('genomic class values must be lists')
        else:
            terms = [] if terms is None else [terms]
        for term in terms:
            _string(term, 'class term')
            if term != term.strip():
                raise ValueError('class terms must be trimmed')
    return value


def _validate(inputs, baseline, table):
    required = {'schema_version', *IDENTITIES, 'candidate_pools', 'queries', 'cohorts', 'provenance', 'expected_class_table_sha256'}
    _object(inputs, required, required, 'inputs')
    if inputs['schema_version'] != '1' or inputs['query_type'] not in ('BGC', 'GCF'):
        raise ValueError('unsupported schema_version or query_type')
    for key in IDENTITIES:
        _string(inputs[key], key)
    digest = inputs['expected_class_table_sha256']
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
        raise ValueError('expected_class_table_sha256 must be a lowercase SHA-256 digest')
    if digest != table.metadata['source_sha256']:
        raise ValueError('class table digest does not match expected pin')
    _object(inputs['provenance'], PROVENANCE, PROVENANCE, 'provenance')
    for name, value in inputs['provenance'].items():
        _string(value, name)
    pools = inputs['candidate_pools']
    cohorts = inputs['cohorts']
    if not isinstance(pools, dict) or not pools or not isinstance(cohorts, dict) or not cohorts:
        raise ValueError('candidate_pools and cohorts must be nonempty objects')
    candidates = set()
    for pool_id, pool in pools.items():
        _string(pool_id, 'pool ID')
        _ids(pool, 'candidate pool')
        candidates.update(pool)
    for cohort_id, cohort in cohorts.items():
        _string(cohort_id, 'cohort ID')
        _object(cohort, ('features',), (), 'cohort')
        features = cohort.get('features')
        if features is None:
            continue
        if not isinstance(features, dict):
            raise ValueError('features must be an object')
        for candidate, feature in features.items():
            if candidate not in candidates:
                raise ValueError('unknown feature ID')
            if feature is None:
                continue
            _object(feature, ('spectrum_id', 'spectral_classes'), (), 'feature')
            if feature.get('spectrum_id') is not None:
                _string(feature['spectrum_id'], 'spectrum ID')
            _classes(feature.get('spectral_classes'), table.metadata['chemical_levels'], False)
    queries = inputs['queries']
    if not isinstance(queries, list) or not queries:
        raise ValueError('queries must be a nonempty list')
    by_id = {}
    for query in queries:
        fields = ('query_id', 'cohort_id', 'candidate_pool_id')
        _object(query, (*fields, 'genomic_classes'), fields, 'query')
        for key in fields:
            _string(query[key], key)
        qid = query['query_id']
        if qid in by_id or query['cohort_id'] not in cohorts or query['candidate_pool_id'] not in pools:
            raise ValueError('duplicate query or unknown pool/cohort ID')
        _classes(query.get('genomic_classes'), table.metadata['genomic_levels'], True)
        by_id[qid] = query
    if not isinstance(baseline, dict):
        raise ValueError('Metcalf run must be an object')
    for key in ('method_id', 'method_version', 'run_id', *IDENTITIES, 'score_direction'):
        _string(baseline.get(key), key)
    if baseline['method_id'] != 'metcalf_standardized' or baseline['score_direction'] != 'higher':
        raise ValueError('requires standardized Metcalf with higher scores first')
    if any(baseline[key] != inputs[key] for key in IDENTITIES):
        raise ValueError('Metcalf run identity mismatch')
    outputs = baseline.get('outputs')
    if not isinstance(outputs, list):
        raise ValueError('Metcalf outputs must be a list')
    source = {}
    for output in outputs:
        if not isinstance(output, dict):
            raise ValueError('Metcalf output must be an object')
        qid = _string(output.get('query_id'), 'query ID')
        if qid not in by_id or qid in source:
            raise ValueError('unknown or duplicate Metcalf query ID')
        for key in ('cohort_id', 'candidate_pool_id'):
            if key in output and output[key] != by_id[qid][key]:
                raise ValueError(f'Metcalf output {key} mismatch for query {qid}')
        status = output.get('status')
        if status in ('abstention', 'input_unavailable', 'execution_failure'):
            _string(output.get('reason'), 'non-output reason')
            if 'scores' in output:
                raise ValueError('non-output must omit scores')
        elif status == 'ok':
            scores = output.get('scores')
            if not isinstance(scores, list):
                raise ValueError('scores must be a list')
            seen = set()
            pool = set(pools[by_id[qid]['candidate_pool_id']])
            for row in scores:
                _object(row, ('candidate_id', 'score'), ('candidate_id', 'score'), 'score row')
                cid = _string(row['candidate_id'], 'candidate ID')
                score = row['score']
                if cid not in pool or cid in seen:
                    raise ValueError('unknown or duplicate Metcalf candidate ID')
                if type(score) not in (int, float) or (isinstance(score, float) and not math.isfinite(score)):
                    raise ValueError('Metcalf score must be finite numeric value')
                seen.add(cid)
            if seen != pool:
                raise ValueError('partial Metcalf candidate scores')
        else:
            raise ValueError('unsupported Metcalf output status')
        source[qid] = output
    if set(source) != set(by_id):
        raise ValueError('missing Metcalf query output')
    return by_id, source


def adapt(inputs, metcalf_run, table, *, run_id):
    """Return a complete evaluator run; malformed supplied inputs raise ValueError."""
    _string(run_id, 'run_id')
    queries, source = _validate(inputs, metcalf_run, table)
    run = {key: inputs[key] for key in IDENTITIES}
    run.update(method_id=METHOD_ID, method_version=METHOD_VERSION, run_id=run_id,
               score_direction='higher', provenance=copy.deepcopy(inputs['provenance']),
               parameters={'threshold': THRESHOLD, 'threshold_operator': '>', 'ranking': 'dense ordinal of (passes_threshold, standardized_metcalf_score)'},
               class_table={'expected_sha256': inputs['expected_class_table_sha256'], 'source_sha256': table.metadata['source_sha256'], 'source_size_bytes': table.metadata['source_size_bytes']},
               kernel={'variant_id': 'npclassscore_named_ontology_strict_v1', 'version': '1.0.0'},
               source_metcalf=copy.deepcopy({k: v for k, v in metcalf_run.items() if k != 'outputs'}), outputs=[])
    for qid in sorted(queries):
        query = queries[qid]
        pool = sorted(inputs['candidate_pools'][query['candidate_pool_id']])
        baseline = source[qid]
        output = {'query_id': qid, 'status': baseline['status'], 'audit': {'candidate_ids': pool, 'candidate_pool_id': query['candidate_pool_id'], 'cohort_id': query['cohort_id']}}
        if baseline['status'] != 'ok':
            output['reason'] = baseline['reason']
            output['audit']['class_scoring'] = 'not_attempted_source_nonoutput'
            run['outputs'].append(output)
            continue
        metcalf = {r['candidate_id']: r['score'] for r in baseline['scores']}
        features = inputs['cohorts'][query['cohort_id']].get('features') or {}
        audit = []
        tuples = {}
        for cid in pool:
            feature = features.get(cid) or {}
            spectrum = feature.get('spectrum_id')
            result = score_classes(table, query.get('genomic_classes') or {}, feature.get('spectral_classes') or {})
            record = {'candidate_id': cid, 'spectrum_id': spectrum, 'class_result': result, 'metcalf_score': metcalf[cid]}
            if spectrum is None:
                record.update(status='input_unavailable', reason='missing_spectrum_join')
            elif result['status'] != 'ok':
                record.update(status='input_unavailable', reason=result['reason'])
            else:
                passed = result['score'] > THRESHOLD
                record.update(status='ok', passes_threshold=passed)
                tuples[cid] = (passed, metcalf[cid])
            audit.append(record)
        output['audit'].update(candidates=audit, class_coverage={'usable_candidates': len(tuples), 'total_candidates': len(pool)})
        if len(tuples) != len(pool):
            output.update(status='input_unavailable', reason='incomplete_class_coverage')
        else:
            ordinal = {value: index + 1 for index, value in enumerate(sorted(set(tuples.values())))}
            output['scores'] = [{'candidate_id': cid, 'score': ordinal[tuples[cid]]} for cid in pool]
        run['outputs'].append(output)
    return run


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def _read_json(path):
    with open(path, encoding='utf-8') as stream:
        return json.load(stream, object_pairs_hook=_unique_object)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('inputs', 'metcalf-run', 'class-table', 'run-id', 'output'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args(argv)
    temporary = None
    try:
        run = adapt(_read_json(args.inputs), _read_json(args.metcalf_run), load_class_table(args.class_table), run_id=args.run_id)
        payload = json.dumps(run, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
        destination = Path(args.output)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent, prefix=destination.name + '.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
        os.replace(temporary, destination)
        temporary = None
    except (ValueError, OSError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except OSError:
                pass
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
