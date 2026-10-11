"""Materialize one predeclared roster; verify its locked bytes before writing."""
import argparse
import hashlib
import json
from pathlib import Path

def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n').encode('utf-8')

def project(common, observations):
    keep = set(observations)
    result = dict(common)
    result['cohorts'] = {}
    for cid, cohort in common['cohorts'].items():
        selected = dict(cohort)
        selected['strain_ids'] = list(observations)
        for field in ('feature_presence', 'normalized_abundance'):
            if cohort.get(field) is not None:
                selected[field] = {candidate: {sid: cell for sid, cell in vector.items() if sid in keep}
                                   for candidate, vector in cohort[field].items()}
        result['cohorts'][cid] = selected
    result['queries'] = []
    for query in common['queries']:
        selected = dict(query)
        selected['eligible_strain_ids'] = list(observations)
        selected['genomic_presence'] = {sid: cell for sid, cell in query['genomic_presence'].items() if sid in keep}
        result['queries'].append(selected)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roster', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if args.output.resolve().is_relative_to(root):
        parser.error('Write derived inputs outside this fixed package.')
    common_bytes = (root / 'inputs.json').read_bytes()
    specifications = json.loads((root / 'rosters.json').read_bytes())
    assert hashlib.sha256(common_bytes).hexdigest() == specifications['common_input_sha256']
    roster = specifications['rosters'][args.roster]
    payload = encoded(project(json.loads(common_bytes), roster['observation_ids']))
    assert len(payload) == roster['derived_input_bytes']
    assert hashlib.sha256(payload).hexdigest() == roster['derived_input_sha256']
    with args.output.open('xb') as handle:
        handle.write(payload)
    print(json.dumps({'roster': args.roster, 'sha256': roster['derived_input_sha256'], 'bytes': len(payload)}))

if __name__ == '__main__':
    main()
