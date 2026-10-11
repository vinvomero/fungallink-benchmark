"""Package frozen numerical inputs and predictions for private reproduction."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'data/processed/core-numerical-candidate-v1-2026-10-11'
METHODS = ['global_prevalence', 'prevalence_difference', 'metcalf_raw', 'metcalf_standardized']
WORKER = '''import hashlib,json,sys
from pathlib import Path
p=Path(__file__).resolve().parent
sys.path.insert(0,str(p/'code'))
from run_baselines import run_baseline
from evaluate_rankings import evaluate
from project_roster import project,encoded
read=lambda f:json.loads(f.read_bytes())
inventory=read(p.parent/'MANIFEST.json')['files']
for name,record in inventory.items():
 if name.startswith(p.name+'/'):
  if hashlib.sha256((p.parent/name).read_bytes()).hexdigest()!=record['sha256']:
   raise ValueError('Input changed: '+name)
common=read(p/'inputs.json');gold=read(p/'benchmark.json');rosters=read(p/'rosters.json')['rosters']
all_rosters='--all-rosters' in sys.argv
checks=[]
for rid,r in rosters.items():
 if not all_rosters and rid!='draft_all_source_observations':continue
 inputs=project(common,r['observation_ids'])
 if hashlib.sha256(encoded(inputs)).hexdigest()!=r['derived_input_sha256']:raise ValueError('Projection mismatch')
 for method in ['global_prevalence','prevalence_difference','metcalf_raw','metcalf_standardized']:
  stem=rid+'--'+method
  expected=read(p/'expected'/(stem+'--rankings.json'))
  ranking=run_baseline(inputs,method,run_id=expected['run_id'])
  if ranking!=expected:raise ValueError('Ranking mismatch: '+stem)
  report=evaluate(gold,ranking)
  if report!=read(p/'expected'/(stem+'--evaluation.json')):raise ValueError('Evaluation mismatch: '+stem)
  checks.append(stem)
print(json.dumps({'status':'passed','track':p.name,'runs':len(checks),'checks':checks,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'python':sys.version,'scope':'Same-host numerical replay from frozen inputs; no raw processing or biological adjudication.'}))
'''


def build():
    if OUTPUT.exists():
        raise FileExistsError('Preserve existing candidate; select a new version')
    payloads = {}
    records = {}

    def add(destination, source, expected=None):
        raw = (ROOT/source).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if expected and sha != expected:
            raise ValueError('Frozen file changed: '+source)
        payloads[destination] = raw
        records[destination] = dict(source=source, sha256=sha, bytes=len(raw))

    initial = 'data/processed/source-selected-gcf-analysis-v1'
    expanded = 'data/processed/source-selected-gcf-expanded-labels-v2'
    for track in ['expanded', 'emericellamide', 'acetylaszonalenin']:
        base = initial if track == 'expanded' else f'data/processed/{track}-gcf-extension-v1'
        manifest = json.loads((ROOT/base/'manifest.json').read_bytes())
        for name, rec in manifest['files'].items():
            source = ROOT/base/name.replace('\\','/')
            if hashlib.sha256(source.read_bytes()).hexdigest() != (rec['sha256'] if isinstance(rec,dict) else rec):
                raise ValueError('Manifest member changed: '+str(source))
        add(track+'/inputs.json',base+'/inputs.json')
        add(track+'/rosters.json',base+'/rosters.json')
        gold_base = expanded+'/gold' if track=='expanded' else base
        add(track+'/benchmark.json',gold_base+'/benchmark.json')
        if track=='expanded':
            newer=json.loads((ROOT/expanded/'manifest.json').read_bytes())
            if records[track+'/benchmark.json']['sha256'] != newer['gold_sha256']:
                raise ValueError('Expanded gold changed')
        for module in ['run_baselines.py','evaluate_rankings.py','project_roster.py']:
            source=base+'/snapshots/'+module
            if track=='expanded':
                source=base+('/'+module if module=='project_roster.py' else '/snapshots/scripts/'+module)
            add(track+'/code/'+module,source)
        rosters=json.loads(payloads[track+'/rosters.json'])['rosters']
        for rid in rosters:
            for method in METHODS:
                stem=rid+'--'+method
                for kind in ['rankings','evaluation']:
                    result_base=expanded if track=='expanded' and kind=='evaluation' else base
                    add(track+'/expected/'+stem+'--'+kind+'.json',result_base+'-results/'+stem+'--'+kind+'.json')
        payloads[track+'/reproduce.py']=WORKER.encode('utf-8')
    for name in ['docs/release/source-provenance-addendum-2026-10-07.md',
                 'docs/release/extension-rights-addendum-2026-10-08.md',
                 'docs/release/proposed-licenses.md',
                 'data/manifests/core-release-scope-draft-2026-10-11.tsv']:
        add(name,name)
    payloads['README.md']='''# Private core numerical candidate

This candidate reproduces the deterministic numerical stages for 11 evaluated relationships: nine products in the expanded five-query comparison, plus the two separately reported family-view extensions. These seven query views belong to one conservative analysis group. They are not seven independent pathway discoveries. The broader project has 30 biological admissions across 16 query identities.

Files are selected from frozen sources with original bytes preserved and a source-to-package map in MANIFEST.json. Each track includes its inputs, declared 18 rosters, gold, exact method/evaluator code and 72 ranking/evaluation pairs. Expanded gold uses the unchanged original five-query rankings. No original source snapshot was altered.

Extract into a new directory. Python standard library is sufficient. From the extracted root run:

```
python -I -S -B expanded/reproduce.py
python -I -S -B emericellamide/reproduce.py
python -I -S -B acetylaszonalenin/reproduce.py
```

Each command verifies hashes, projects the primary roster and compares complete ranking/evaluation objects. Append `--all-rosters` to check all 18 rosters. Scripts read scientific data and print results without writing back into the package. Files with conflicting hashes fail. Do not use Python optimization flags that suppress assertions inside retained source code.

This is a private numerical reproduction candidate, not an authorized public dataset or public source-reconstruction route. The publisher workbook/archive and historical author-workbook mapping remain provenance dependencies. The sample maps were project-generated reconciliations incorporating author clarification; their origin is not unknown. See the included provenance and rights addenda. No original-contribution license is applied. Selecting arrays for this private package does not resolve the underlying public release basis.

The package starts from frozen numerical inputs. It does not reproduce raw feature processing, biological curation, historical mapping derivation, spectral inference, Monte Carlo simulations or the separate phylogeny comparison. Those stages remain in the main project's records. Same-host automated replay is not independent researcher validation.
'''.encode('utf-8')
    for name,raw in payloads.items():
        records.setdefault(name,dict(source='Generated packaging wrapper',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
    payloads['MANIFEST.json']=(json.dumps(dict(status='private_candidate',files=records),indent=2)+'\n').encode('utf-8')
    OUTPUT.mkdir(parents=True)
    archive=OUTPUT/'fungallink-core-numerical-private-v1.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,raw in sorted(payloads.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,raw)
    with zipfile.ZipFile(archive) as z:
        if set(z.namelist())!=set(payloads):raise ValueError('Archive membership differs')
        for name,raw in payloads.items():
            if z.read(name)!=raw:raise ValueError('Archive bytes differ: '+name)
    receipt=dict(status='built_and_verified',utc=datetime.now(timezone.utc).isoformat(),command=[sys.executable,'scripts/build_core_numerical_candidate.py'],archive=str(archive.relative_to(ROOT)),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),bytes=archive.stat().st_size,members=len(payloads),tracks=3,rosters_per_track=18,method_runs=216,scope='Private packaging integrity; execution is checked separately')
    (OUTPUT/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    build()
