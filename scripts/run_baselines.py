"""Run declared, label-free baseline controls over shared strain-level tables."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import tempfile


VERSION = '0.1.0'
METHODS = ('uniform_random', 'global_prevalence', 'global_abundance',
           'prevalence_difference', 'metcalf_raw', 'metcalf_standardized')
IDENTITIES = ('track_id', 'query_type', 'candidate_universe_id')


def _id(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{field} must be a nonempty canonical ID')
    return value


def _object(value, field, allowed=None):
    if not isinstance(value, dict):
        raise ValueError(f'{field} must be an object')
    for key in value:
        _id(key, field + ' key')
    if allowed is not None and set(value) - set(allowed):
        raise ValueError(f'{field}: unknown fields {sorted(set(value) - set(allowed))}')
    return value


def _ids(value, field, nonempty=False):
    if not isinstance(value, list):
        raise ValueError(f'{field} must be a list')
    for item in value:
        _id(item, field)
    if len(set(value)) != len(value) or (nonempty and not value):
        raise ValueError(f'{field} must contain unique IDs' + (' and be nonempty' if nonempty else ''))
    return set(value)


def _vector(value, field, strains, abundance=False):
    if value is None:
        return
    _object(value, field)
    if strains is not None and set(value) - strains:
        raise ValueError(f'{field} contains strains outside cohort roster')
    for strain, cell in value.items():
        if cell is None:
            continue
        if abundance:
            if isinstance(cell, bool) or not isinstance(cell, (int, float)) or cell < 0:
                raise ValueError(f'{field}/{strain} must be finite nonnegative abundance or null')
            try:
                finite = math.isfinite(cell)
            except OverflowError:
                finite = False
            if not finite:
                raise ValueError(f'{field}/{strain} must be finite nonnegative abundance or null')
        elif type(cell) is not int or cell not in (0, 1):
            raise ValueError(f'{field}/{strain} must be integer binary 0/1 or null')


def _validate(inputs):
    _object(inputs, 'inputs', ('schema_version', *IDENTITIES, 'candidate_pools', 'cohorts', 'queries'))
    if inputs.get('schema_version') != '1':
        raise ValueError('input schema_version must be "1"')
    for key in IDENTITIES:
        _id(inputs.get(key), key)
    pools = _object(inputs.get('candidate_pools'), 'candidate_pools')
    all_candidates = set()
    for pool, ids in pools.items():
        all_candidates.update(_ids(ids, f'candidate_pools/{pool}', nonempty=True))
    cohorts = _object(inputs.get('cohorts'), 'cohorts')
    rosters = {}
    for cid, cohort in cohorts.items():
        _object(cohort, f'cohort/{cid}', ('strain_ids', 'feature_presence', 'normalized_abundance'))
        roster = cohort.get('strain_ids')
        rosters[cid] = None if roster is None else _ids(roster, f'cohort/{cid}/strain_ids')
        for field in ('feature_presence', 'normalized_abundance'):
            table = cohort.get(field)
            if table is None:
                continue
            _object(table, f'cohort/{cid}/{field}')
            if set(table) - all_candidates:
                raise ValueError(f'cohort/{cid}/{field} contains candidates outside declared pools')
            for candidate, vector in table.items():
                _vector(vector, f'{cid}/{field}/{candidate}', rosters[cid], field == 'normalized_abundance')
    queries = inputs.get('queries')
    if not isinstance(queries, list) or not queries:
        raise ValueError('queries must be a nonempty list')
    seen = set()
    for query in queries:
        _object(query, 'query', ('query_id', 'cohort_id', 'candidate_pool_id', 'eligible_strain_ids', 'genomic_presence'))
        qid = _id(query.get('query_id'), 'query_id')
        if qid in seen:
            raise ValueError(f'duplicate query ID: {qid}')
        seen.add(qid)
        cid = _id(query.get('cohort_id'), 'cohort_id')
        pool = _id(query.get('candidate_pool_id'), 'candidate_pool_id')
        if cid not in cohorts or pool not in pools:
            raise ValueError(f'{qid} references an unknown cohort or candidate pool')
        eligible = query.get('eligible_strain_ids')
        if eligible is not None:
            eligible = _ids(eligible, f'{qid}/eligible_strain_ids')
            if rosters[cid] is not None and eligible - rosters[cid]:
                raise ValueError(f'{qid} eligible strains outside cohort roster')
        _vector(query.get('genomic_presence'), f'{qid}/genomic_presence', rosters[cid])


def _available_vector(vector, strains, field):
    if vector is None:
        return None, f'missing_required_input: {field}'
    missing = [s for s in strains if vector.get(s) is None]
    if missing:
        return None, f'missing_required_input: {field}/{missing[0]}'
    return [vector[s] for s in strains], None


def seed_payload(inputs, query, seed, repeat_index):
    """Return the ordered v1 seed fields for hashing or manifest replay.

    Callers supply validated input/query identities and an integer seed.
    repeat_index is an integer for hashing; manifests may use '{repeat_index}'.
    """
    return ['fungallink-baseline-random-v1', seed, repeat_index,
            *[inputs[k] for k in IDENTITIES], query['cohort_id'],
            query['candidate_pool_id'], query['query_id']]


def _random_seed(inputs, query, seed, repeat_index):
    # Canonical JSON array avoids concatenation ambiguity and process hash state.
    payload = seed_payload(inputs, query, seed, repeat_index)
    encoded = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return int.from_bytes(hashlib.sha256(encoded).digest(), 'big')


def _query(inputs, query, method_id, seed, repeat_index):
    candidates = sorted(inputs['candidate_pools'][query['candidate_pool_id']])
    out = {key: query[key] for key in ('query_id', 'cohort_id', 'candidate_pool_id')}
    audit = {}
    out['audit'] = audit

    def unavailable(reason, status='input_unavailable'):
        out.update(status=status, reason=reason)
        return out

    if method_id == 'uniform_random':
        derived_seed = _random_seed(inputs, query, seed, repeat_index)
        permutation = candidates.copy()
        random.Random(derived_seed).shuffle(permutation)
        values = {candidate: len(permutation) - i for i, candidate in enumerate(permutation)}
        audit.update(derived_seed=str(derived_seed), repeat_index=repeat_index)
    else:
        strains = sorted(query.get('eligible_strain_ids') or [])
        n = len(strains)
        audit['eligible_strain_count'] = n
        if not n:
            return unavailable('missing_required_input: nonempty eligible_strain_ids')
        cohort = inputs['cohorts'][query['cohort_id']]
        genome = None
        if method_id in ('prevalence_difference', 'metcalf_raw', 'metcalf_standardized'):
            genome, reason = _available_vector(query.get('genomic_presence'), strains, 'genomic_presence')
            if reason:
                return unavailable(reason)
            g = sum(genome)
            audit.update(genomic_positive_count=g, genomic_negative_count=n - g)
        field = 'normalized_abundance' if method_id == 'global_abundance' else 'feature_presence'
        table = cohort.get(field)
        if table is None:
            return unavailable(f'missing_required_input: {field}')
        # Check the entire frozen pool before scoring; never shrink a pool or denominator.
        vectors = {}
        for candidate in candidates:
            vector, reason = _available_vector(table.get(candidate), strains, f'{field}/{candidate}')
            if reason:
                return unavailable(reason)
            vectors[candidate] = vector
        if genome is not None and g in (0, n):
            if method_id == 'prevalence_difference':
                return unavailable('zero_genomic_denominator', 'abstention')
            if method_id == 'metcalf_standardized':
                return unavailable('invariant_genomic_presence', 'abstention')
        values = {}
        audit['candidates'] = {}
        for candidate, vector in vectors.items():
            details = {}
            if method_id == 'global_abundance':
                # Scaling keeps finite nonnegative inputs from overflowing a sum.
                scale = max(vector)
                value = scale * (math.fsum(v / scale for v in vector) / n) if scale else 0.0
                details['denominator'] = n
            elif method_id == 'global_prevalence':
                value = sum(vector) / n
                details.update(feature_positive_count=sum(vector), denominator=n)
            else:
                m = sum(vector)
                overlap = sum(a * b for a, b in zip(genome, vector))
                n11, n01, n10, n00 = overlap, m - overlap, g - overlap, n - g - m + overlap
                details.update(n11=n11, n01=n01, n10=n10, n00=n00,
                               feature_positive_count=m)
                if method_id == 'prevalence_difference':
                    value = n11 / g - n01 / (n - g)
                else:
                    raw = 10 * n11 - 10 * n01 + n00
                    details['raw_score'] = raw
                    if method_id == 'metcalf_raw':
                        value = raw
                    else:
                        expected_overlap = g * (m / n)
                        mean = 21 * expected_overlap + n - g - 11 * m
                        variance = 441 * g * (m / n) * ((n - g) / n) * ((n - m) / (n - 1))
                        zero_variance = m in (0, n)
                        value = 0.0 if zero_variance else 21 * (overlap - expected_overlap) / math.sqrt(variance)
                        details.update(null_mean=mean, null_variance=variance, zero_variance=zero_variance)
            values[candidate] = value
            audit['candidates'][candidate] = details
    out.update(status='ok', scores=[{'candidate_id': candidate, 'score': values[candidate]} for candidate in candidates])
    return out


def run_baseline(inputs, method_id, *, run_id, seed=20260930, repeat_index=0):
    """Return one complete evaluator run, without reading gold or mutating inputs.

    Missing scientific inputs yield input_unavailable; malformed supplied data
    raise ValueError. Seed/repeat apply only to uniform_random.
    """
    _validate(inputs)
    if method_id not in METHODS:
        raise ValueError(f'unknown method_id: {method_id}')
    _id(run_id, 'run_id')
    if type(seed) is not int or type(repeat_index) is not int or repeat_index < 0:
        raise ValueError('seed must be an integer; repeat_index must be a nonnegative integer')
    parameters = {'preprocessing': 'none; abundance supplied normalized', 'score_cutoff': None}
    if method_id == 'uniform_random':
        parameters.update(seed=seed, repeat_index=repeat_index, seed_derivation='sha256-canonical-json-array-v1',
                          candidate_order='sorted canonical IDs', generator='random.Random.shuffle')
    if method_id.startswith('metcalf_'):
        parameters['weights_genomic_first'] = {'n11': 10, 'n01': -10, 'n10': 0, 'n00': 1}
    if method_id == 'metcalf_standardized':
        parameters.update(null='fixed-margin hypergeometric overlap', invariant_genome='abstention', invariant_feature='zero_with_flag')
    return {'schema_version': '1', **{key: inputs[key] for key in IDENTITIES},
            'method_id': method_id, 'method_version': VERSION, 'run_id': run_id,
            'score_direction': 'higher', 'parameters': parameters,
            'implementation': {'name': 'FungalLink local baselines', 'version': VERSION,
                               'python_implementation': platform.python_implementation(),
                               'python_version': platform.python_version(),
                               'random_state_version': random.Random.VERSION},
            'outputs': [_query(inputs, query, method_id, seed, repeat_index)
                        for query in sorted(inputs['queries'], key=lambda q: q['query_id'])]}


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON object key: {key}')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', required=True, type=Path)
    parser.add_argument('--method', required=True, choices=METHODS)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--seed', type=int, default=20260930)
    parser.add_argument('--repeat-index', type=int, default=0)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        inputs = json.loads(args.inputs.read_text(encoding='utf-8'), object_pairs_hook=_json_object)
        result = run_baseline(inputs, args.method, run_id=args.run_id, seed=args.seed, repeat_index=args.repeat_index)
        serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=args.output.parent,
                                             prefix=f'.{args.output.name}.', suffix='.tmp', delete=False) as report:
                temporary = Path(report.name)
                report.write(serialized)
            os.replace(temporary, args.output)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'baseline error: {exc}\n')


if __name__ == '__main__':
    main()
