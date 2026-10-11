"""Build a new private candidate from v2; never overwrite a frozen ZIP."""
from pathlib import Path
import csv, hashlib, json, posixpath, re, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
REL = WORK.relative_to(ROOT).as_posix()
OLD = ROOT/'data/processed/presubmission-release-candidate-v2/fungallink-presubmission-release-v2.zip'
DEST = ROOT/'data/processed/presubmission-release-candidate-v3'
ARCHIVE = DEST/'fungallink-presubmission-release-v3.zip'
SIM = 'data/processed/similarity-independence-v1/'
RENDER = 'manuscript/similarity-integration-render-2026-10-11/'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(path, obj): path.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')

assert not ARCHIVE.exists(), 'Never overwrite a versioned archive'
manifest = json.loads((ROOT/SIM/'manifest.json').read_text())
replacements = {
    'manuscript/benchmark-paper-review.md', 'manuscript/benchmark-paper-review.docx',
    'manuscript/benchmark-paper-review.pdf', 'manuscript/Supplementary-Methods.md',
    'manuscript/claim-evidence.tsv',
    'docs/release/reproduction-stages-v1.md', 'docs/release/release-map-v1.md'}
additions = set(manifest['inputs']) | set(manifest['outputs']) | {
    SIM+'manifest.json', 'docs/evaluation/similarity-independence-v1.md',
    'manuscript/benchmark-paper-review-claim-map.json',
    'docs/release/similarity-independence-v1.md', 'data/manifests/similarity-input-disposition-v1.tsv',
    REL+'/integrate.py', REL+'/authoring-receipt.json', REL+'/build-v3.py', REL+'/payload-delta.json',
    REL+'/check-render.py', REL+'/host-render-review.json', REL+'/link-check.json',
    'data/processed/source-selected-gcf-analysis-v1/inputs.json',
    'data/processed/source-selected-gcf-analysis-v1-results/clean-deterministic-rerun.json',
    RENDER+'render.py', RENDER+'export.ps1', RENDER+'rasterize.py',
    RENDER+'authoring-receipt.json', RENDER+'methods-authoring-receipt.json',
    RENDER+'render-receipt.json', RENDER+'methods-render-receipt.json', RENDER+'final-manifest.json',
    RENDER+'Supplementary-Methods.docx', RENDER+'Supplementary-Methods.pdf',
    'README-SIMILARITY-V3.md'}
# Retain exact successful, failed, correction and install records plus resumable caches.
additions |= {p.relative_to(ROOT).as_posix() for p in (ROOT/'planning/similarity-independence-work-2026-10-11').iterdir() if p.is_file()}
for name, expected in {**manifest['inputs'], **manifest['outputs']}.items():
    assert sha((ROOT/name).read_bytes()) == expected, name
assert sha((ROOT/'docs/evaluation/similarity-independence-v1.md').read_bytes()) == manifest['report']['sha256']
source_manifest=json.loads((ROOT/'data/processed/source-selected-gcf-analysis-v1/manifest.json').read_text())
assert sha((ROOT/'data/processed/source-selected-gcf-analysis-v1/inputs.json').read_bytes()) == source_manifest['files']['inputs.json']['sha256']

with zipfile.ZipFile(OLD) as src:
    prior=json.loads(src.read('REVIEW-MANIFEST.json')); names=set(prior['files'])
    for name in names:
        assert sha(src.read(name))==prior['files'][name]['sha256'], name
    assert replacements <= names
    # A manifest input already inherited must agree exactly with that frozen snapshot.
    for name in additions & names:
        assert sha((ROOT/name).read_bytes())==prior['files'][name]['sha256'], name
    rows=[]
    for name, digest in sorted(manifest['inputs'].items()):
        rows.append({'input_path':name,'sha256':digest,'bytes':(ROOT/name).stat().st_size,
                     'disposition':'bundled_inherited' if name in names else 'bundled_new',
                     'archive_member':name,'retrieval_locator':'not_required_for_saved_companion_stage',
                     'role':'manifest_consumed_input','scope':'Similarity stages; does not imply raw processing or predictor inference replay'})
    p=ROOT/'data/manifests/similarity-input-disposition-v1.tsv'
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    delta={'prior_archive':OLD.relative_to(ROOT).as_posix(),'prior_archive_sha256':sha(OLD.read_bytes()),
           'changed_inherited_paths':sorted(replacements),'new_paths':sorted(additions-names),
           'protected_scope':'Every other inherited payload, including all scientific data, scores, evaluation outputs, quantitative comparison tables, figures and nested archives',
           'scientific_runs_repeated':False,'prior_replay_evidence':'Reused only for unchanged inherited numerical payloads; new similarity outputs retain their original completed-run receipts.'}
    dump(WORK/'payload-delta.json',delta)
    (ROOT/'README-SIMILARITY-V3.md').write_text('''# Private FungalLink candidate v3

This version integrates the completed representation-limited similarity analysis into the main manuscript and Supplementary Methods. Read `docs/release/release-map-v1.md` and `docs/release/similarity-independence-v1.md` first. The result remains 30 relationships/16 query identities, with 11 complete, two partial and 17 missing input states. One conservative complete-analysis group remains; no independent holdout or complete model-training overlap assessment is established.

Current main files are `manuscript/benchmark-paper-review.md`, `.docx` and `.pdf`. Current Supplementary Methods are `manuscript/Supplementary-Methods.md` and `manuscript/similarity-integration-render-2026-10-11/Supplementary-Methods.docx`/`.pdf`. The dated `manuscript/data-descriptor-render-2026-10-11/` files and old generation receipts are retained historical snapshots; their hashes describe that earlier rendering. Comparative results and all three quantitative tables are unchanged. The new render manifest identifies the current sources and outputs.

`REVIEW-MANIFEST.json` hashes every outer payload. Run `python scripts/verify_private_review_archive.py <path-to-v3.zip>` before extraction. `planning/similarity-manuscript-integration-2026-10-11/payload-delta.json` lists changed inherited files and additions against v2. Every other inherited payload is byte-identical, including four nested archives. Keep nested archives in separate extraction roots.

All 76 manifest-consumed similarity inputs are bundled at the exact paths in `data/manifests/similarity-input-disposition-v1.tsv`, together with the completed tables, three scripts, protocol, caches, stage receipts and environment/install records. Installation receipts describe the original environment; they are not a claim of a newly tested portable lock. The dictionary separates saved companion-stage inputs from raw processing and predictor inference dependencies. No analytical jobs were rerun to build this candidate. Prior numerical replay evidence is reused only for unchanged inherited science.

This archive remains private. It has no public accession or verified anonymous download route. Accountable human scientific review, final release selection and explicit authorization for external sharing remain pending. Package checks verify records and bytes, not biological correctness.
''',encoding='utf-8')
    all_names=names|additions
    # Check local Markdown links introduced by this unit; historical inherited links keep their prior scope.
    links=[]
    for name in sorted(replacements|{'docs/release/similarity-independence-v1.md','README-SIMILARITY-V3.md'}):
        if not name.endswith('.md'):continue
        text=(ROOT/name).read_text(encoding='utf-8-sig')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('http:','https:','mailto:','#')):continue
            path=posixpath.normpath(posixpath.join(posixpath.dirname(name),target.split('#')[0]))
            if path not in all_names:
                # Directory links are satisfied by their packaged descendants.
                exists=any(n.startswith(path.rstrip('/')+'/') for n in all_names)
            else: exists=True
            links.append({'source':name,'target':path,'packaged':exists})
    dump(WORK/'link-check.json',{'links':links,'missing':[x for x in links if not x['packaged']],
                               'scope':'Local Markdown destinations in current edited documents; no external retrieval'})
    assert not [x for x in links if not x['packaged']], 'Every edited-document local Markdown link must resolve'
    DEST.mkdir(parents=True,exist_ok=True)
    files={}
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as dst:
        for name in sorted(all_names):
            b=(ROOT/name).read_bytes() if name in replacements or name not in names else src.read(name)
            dst.writestr(name,b);files[name]={'bytes':len(b),'sha256':sha(b)}
        dst.writestr('REVIEW-MANIFEST.json',json.dumps({**prior,'scope':'Private v3 similarity manuscript integration; unchanged inherited scientific payloads from v2. Current render paths and historical snapshots distinguished in README-SIMILARITY-V3.md.','files':files},indent=2)+'\n')
    changed=[name for name in names if files[name]!=prior['files'][name]]
    assert set(changed)==replacements
with zipfile.ZipFile(ARCHIVE) as z:
    assert len(z.namelist())==len(files)+1
    for name, record in files.items():
        b=z.read(name);assert len(b)==record['bytes'] and sha(b)==record['sha256'],name
receipt={'status':'passed','created_utc':datetime.now(timezone.utc).isoformat(),
         'archive':ARCHIVE.relative_to(ROOT).as_posix(),'bytes':ARCHIVE.stat().st_size,'sha256':sha(ARCHIVE.read_bytes()),
         'payloads':len(files),'inherited_payloads_byte_identical':len(names)-len(changed),
         'changed_inherited_paths':sorted(changed),'new_paths':sorted(additions-names),
         'prior_archive_sha256':sha(OLD.read_bytes()),'similarity_manifest_consumed_inputs_bundled':len(rows),
         'similarity_outputs_unchanged':len(manifest['outputs']),'scientific_reruns':False,
         'new_local_similarity_links_missing':0,'inherited_document_links_not_in_outer_archive':sum(not x['packaged'] for x in links),
         'validation':'All prior and new outer payload hashes and sizes checked; frozen inherited science unchanged. No scientific or external download replay.',
         'route':{'requested':'gpt-6-astra/medium','actual_serving_receipt':'unavailable'}}
dump(DEST/'build-receipt.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k not in ['new_paths','changed_inherited_paths']},indent=2))
