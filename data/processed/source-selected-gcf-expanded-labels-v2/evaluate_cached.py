"""Evaluate the declared expanded gold against unchanged, frozen cached rankings."""
import csv
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
RELEASE = Path(__file__).resolve().parent
OLD = ROOT / 'data/processed/source-selected-gcf-analysis-v1'
CACHE = ROOT / 'data/processed/source-selected-gcf-analysis-v1-results'
OUT = ROOT / 'data/processed/source-selected-gcf-expanded-labels-v2-results'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, obj):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, sort_keys=True, separators=(',', ':'), allow_nan=False)
        f.write('\n')


def main():
    assert (RELEASE / 'analysis-amendment.json').exists()
    OUT.mkdir(exist_ok=False)
    snapshot = RELEASE / 'snapshots'
    snapshot.mkdir(exist_ok=False)
    sources = ['data/curated/label-evidence.tsv',
               'protocol/decisions/2026-10-07-delegated-admission-dispositions.md',
               'data/curated/source-gcf-analysis-groups-2026-10-07.tsv',
               'scripts/build_source_gcf_evaluation.py', 'scripts/build_candidate_bundle.py',
               'scripts/build_source_observations.py', 'scripts/evaluate_rankings.py', 'scripts/run_baselines.py']
    for name in sources:
        dest = snapshot / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    old_manifest = json.loads((OLD / 'manifest.json').read_bytes())
    freeze = json.loads((CACHE / 'freeze.json').read_bytes())
    assert digest(OLD / 'manifest.json') == freeze['release_manifest_sha256']
    old_files_before = {str(p.relative_to(ROOT)): digest(p) for d in [OLD, CACHE] for p in d.rglob('*') if p.is_file()}
    for name, info in old_manifest['files'].items():
        assert digest(OLD / name) == info['sha256'], name
    gold = json.loads((RELEASE / 'gold/benchmark.json').read_bytes())
    original = json.loads((OLD / 'benchmark.json').read_bytes())
    for key in ('track_id', 'query_type', 'candidate_universe_id'):
        assert gold[key] == original[key]
    oq = {q['query_id']: q for q in original['queries']}
    assert set(oq) == {q['query_id'] for q in gold['queries']}
    for q in gold['queries']:
        before = oq[q['query_id']]
        assert {k:v for k,v in q.items() if k!='products'} == {k:v for k,v in before.items() if k!='products'}
        assert all(q['products'][k] == v for k,v in before['products'].items())
    assert sorted(len(q['products']) for q in gold['queries']) == [1,1,1,2,4]
    sys.path.insert(0, str(OLD / 'snapshots/scripts'))
    from evaluate_rankings import evaluate
    spec = importlib.util.spec_from_file_location('projection', OLD / 'project_roster.py')
    pr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pr)
    common = json.loads((OLD / 'inputs.json').read_bytes())
    rosters = json.loads((OLD / 'rosters.json').read_bytes())['rosters']
    for rid, rs in rosters.items():
        assert hashlib.sha256(pr.encoded(pr.project(common, rs['observation_ids']))).hexdigest() == rs['derived_input_sha256']
    expected_files = {x['path']: x['sha256'] for x in json.loads((CACHE/'execution-complete.json').read_bytes())['outputs']}
    ranking_paths = sorted(CACHE.glob('*--rankings.json'))
    assert len(ranking_paths) == 72
    rankings = {p.name:digest(p) for p in ranking_paths}
    assert all(expected_files[n] == h for n,h in rankings.items())
    save(RELEASE/'manifest.json', dict(release_id=RELEASE.name, positive_set_version='approved-nine-relationships-v2',
        track_id=gold['track_id'], track_identity_reason='Semantic task unchanged for exact cached ranking reuse; gold version and hash differ explicitly.',
        candidate_count=9339,query_count=5,product_count=9,group_count=1,roster_count=18,
        amendment_sha256=digest(RELEASE/'analysis-amendment.json'),gold_sha256=digest(RELEASE/'gold/benchmark.json'),
        original_manifest_sha256=freeze['release_manifest_sha256'], original_inputs_sha256=digest(OLD/'inputs.json'),
        rosters_sha256=digest(OLD/'rosters.json'), evaluator_sha256=digest(OLD/'snapshots/scripts/evaluate_rankings.py'),
        method_code_sha256=digest(OLD/'snapshots/scripts/run_baselines.py'), cached_rankings=rankings,
        files={str(p.relative_to(RELEASE)):digest(p) for p in RELEASE.rglob('*') if p.is_file()},
        activation='Private amendment after identity/hash verification; evaluation only, no new method scores.',
        random='Exact expectations only; no Monte Carlo execution or inherited MC statistics.'))
    save(OUT/'execution-start.json', dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
         recipe_sha256=digest(Path(__file__)),manifest_sha256=digest(RELEASE/'manifest.json'),python=sys.version))
    start=time.perf_counter()
    summaries=[]
    flat=[]
    def add_rows(roster,method,queries,overall,observations):
        def put(scope,query_id,selected,metrics):
            flat.append(dict(release_id=RELEASE.name,roster=roster,observations=observations,method=method,scope=scope,
                query_id=query_id,queries=len(selected),products=sum(len(q['products']) for q in selected),
                candidates=9339,coverage=1.0,**metrics))
        put('overall','',queries,overall)
        for q in queries:put('query',q['query_id'],[q],q['metrics'])
        for label, selected in [('directly-supported',[q for q in queries if q['query_id']=='source:NRPSPKS_85']),
                                ('reference-supported',[q for q in queries if q['query_id']!='source:NRPSPKS_85'])]:
            metrics={k:math.fsum(q['metrics'][k] for q in selected)/len(selected) for k in overall}
            put(label,'',selected,metrics)
    for path in ranking_paths:
        run=json.loads(path.read_bytes())
        roster,method=path.name.removesuffix('--rankings.json').split('--')
        assert method in old_manifest['methods'] and run['method_version']==old_manifest['method_version']
        assert run['method_id']==method and run['score_direction']=='higher'
        report=evaluate(gold,run)
        assert report['summary']['coverage']==1.0 and report['summary']['valid_query_count']==5
        save(OUT/path.name.replace('--rankings','--evaluation'),report)
        summaries.append(dict(roster=roster,method=method,source_ranking_sha256=rankings[path.name],summary=report['summary']))
        add_rows(roster,method,report['queries'],report['summary']['end_to_end']['metrics'],len(rosters[roster]['observation_ids']))
    save(OUT/'deterministic-summary.json',summaries)
    random_queries=[]
    for q in gold['queries']:
        n=len(q['candidate_ids']);p=len(q['products']);assert all(len(v)==1 for v in q['products'].values())
        denominator=math.comb(n,p)
        metrics={'rr':math.fsum(math.comb(n-u,p-1)/denominator/u for u in range(1,n-p+2))}
        for k in [1,10,100]:
            metrics['hit@'+str(k)]=1-math.comb(n-k,p)/denominator
            metrics['product_recovery@'+str(k)]=k/n
            metrics['all_products@'+str(k)]=math.comb(k,p)/denominator if k>=p else 0.0
        random_queries.append(dict(query_id=q['query_id'],products=q['products'],metrics=metrics))
    overall={k:math.fsum(q['metrics'][k] for q in random_queries)/5 for k in random_queries[0]['metrics']}
    save(OUT/'exact-random.json',dict(method='Closed-form sampling without replacement, singleton distinct product targets; arithmetic means over five queries.',
        formulas={'hit':'1-C(N-k,p)/C(N,p)','product_recovery':'k/N','all_products':'C(k,p)/C(N,p), zero if k<p','rr':'sum_u C(N-u,p-1)/(C(N,p)*u)'},
        queries=random_queries,overall_metrics=overall,applies_to_rosters=sorted(rosters),monte_carlo_run=False))
    for rid,rs in rosters.items():add_rows(rid,'uniform_random_exact',random_queries,overall,len(rs['observation_ids']))
    table=ROOT/'manuscript/expanded-label-results-2026-10-07.tsv'
    with table.open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(flat[0]),delimiter='\t');writer.writeheader();writer.writerows(flat)
    assert all(digest(ROOT/p)==h for p,h in old_files_before.items())
    save(OUT/'validation.json',dict(status='passed',queries=5,products=9,candidates=9339,rosters=18,deterministic_evaluations=72,
        cached_rankings_unchanged=72,old_files_preserved=len(old_files_before),old_files_before_sha256=old_files_before,
        full_coverage_all_runs=True,score_recomputations=0,monte_carlo_runs=0,projected_input_hashes_verified=18,
        previous_products_preserved=True,added_positive_ids=['caesar2023:relationship:22','caesar2023:pst:1950','caesar2023:pst:895'],
        elapsed_seconds=time.perf_counter()-start,table_rows=len(flat),table_sha256=digest(table),
        outputs={p.name:digest(p) for p in OUT.iterdir() if p.is_file()}))
    print(json.dumps({'status':'passed','evaluations':72,'table_rows':len(flat),'exact_random':overall,'elapsed_seconds':time.perf_counter()-start},indent=2))


if __name__=='__main__':
    main()
