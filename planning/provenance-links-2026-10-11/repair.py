"""Delivery metadata repair only; preserve the frozen candidate and scientific bytes."""
import csv, hashlib, io, json, zipfile
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
REL = WORK.relative_to(ROOT).as_posix()
OLD = ROOT/'data/processed/presubmission-release-candidate-v1/fungallink-presubmission-release-v1.zip'
DEST = ROOT/'data/processed/presubmission-release-candidate-v2'
def digest(b): return hashlib.sha256(b).hexdigest()
def readrows(p):
    return list(csv.DictReader((ROOT/p).open(encoding='utf-8-sig', newline=''), delimiter='\t'))
def writejson(p,x): p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def writetsv(p,rows,fields=None):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)

def main():
    request=json.loads((WORK/'link-request.json').read_text())
    results=json.loads((WORK/'link-results.json').read_text())
    for r in results['results']:
        if 'X-Amz-' in r.get('final_url',''):
            u=urlsplit(r['final_url']);r['final_url']=urlunsplit((u.scheme,u.netloc,u.path,'',''))
            r['redirect_note']='Transient signed redirect query removed; use the stable request URL.'
    writejson(WORK/'link-results.json',results)
    assert len(results['results'])==6 and all(r['matches_retained_bytes'] and r['http_status']==200 for r in results['results'])
    links={r['workspace_path']:r for r in request['links']}
    manifest='data/manifests/release-evidence-v1.tsv'
    rows=readrows(manifest); changed=0
    for r in rows:
        if r['workspace_path'] not in links: continue
        src=links[r['workspace_path']];r['source_url']=src['source_url']
        if r['disposition']=='omit':r['disposition']='retrieve'
        r['note'] += '; direct_locator_kind='+src['link_kind']+'; retained_locator_record='+src['locator_record']
        r['reason']='Source route recovered from retained records. '+('Exact file locator; see retrieval checks for verification scope.' if src['link_kind']=='exact_file' else 'Parent source or article landing page; not an exact-byte locator for the local derivative.')
        changed+=1
    writetsv(ROOT/manifest,rows)
    trace=[];assertions=0
    with zipfile.ZipFile(OLD) as z:
        oldman=json.loads(z.read('REVIEW-MANIFEST.json'))
        names=set(oldman['files'])
        golds={n:json.loads(z.read(n)) for n in names if n.endswith('/benchmark.json')}
        readiness=list(csv.DictReader(io.StringIO(z.read('data/curated/relationship-readiness-v1.tsv').decode('utf-8-sig')),delimiter='\t'))
        for r in readiness:
            for field in ['evidence_packet','current_decision','supersession']:
                for ref in r[field].split(';'):
                    ref=ref.strip()
                    if ref.startswith(('docs/','protocol/','data/','planning/')):assert ref in names,(r['relationship_id'],ref)
            targets=[]
            if r['input_state']=='complete':
                for name,gold in golds.items():
                    for q in gold.get('queries',[]):
                        if q['query_id']==r['evaluation_query_view'] and r['evaluation_target_key'] in q.get('products',{}).get(r['relationship_id'],[]):targets.append(name)
                assert targets,r['relationship_id']
                check='exact_query_relationship_target_join'
            elif r['input_state']=='partial':
                for name in names:
                    if name.endswith('/evaluation.json'):
                        obj=json.loads(z.read(name))
                        if obj.get('target_id')==r['evaluation_target_key']:targets.append(name)
                assert targets,r['relationship_id']
                check='target_id_in_partial_diagnostic; not_complete_benchmark'
            else:
                assert r['evaluation_target_key']=='not_applicable'
                check='source_experiment_only; executable_input_gap'
            trace.append({k:r[k] for k in ['relationship_id','product','query_id','evaluation_query_view','source_target_key','evaluation_target_key','input_state','evidence_packet','current_decision','supersession','source_locator','uncertainty']} | {'evaluation_record':';'.join(sorted(targets)),'mechanical_check':check})
        historical=readrows('data/raw/sources/caesar-2023/historical-label-strain-assembly-crosswalk-2026-09-20.tsv')
        population=list(csv.DictReader(io.StringIO(z.read('data/curated/caesar-source-gcf-population-2026-10-03.tsv').decode('utf-8-sig')),delimiter='\t'))
        for r in population:
            for snap in json.loads(r['historical_bridge_rows_json'] or '[]'):
                n=snap['physical_tsv_row'];actual=historical[n-2]
                assert {k:v for k,v in snap.items() if k!='physical_tsv_row'}==actual,(n,snap)
                assertions+=1
    tracepath='data/manifests/relationship-traceability-v1.tsv'
    writetsv(ROOT/tracepath,trace)
    audit={'checked_utc':datetime.now(timezone.utc).isoformat(),'scope':'Record joins and source-byte retrieval, not biological re-adjudication or scientific reproduction','relationships':len(trace),'complete_exact_query_target_joins':sum(r['input_state']=='complete' for r in trace),'partial_target_joins':sum(r['input_state']=='partial' for r in trace),'source_only_input_missing':sum(r['input_state']=='missing' for r in trace),'packaged_population_rows':len(population),'embedded_historical_row_occurrences_matching_retained_original':assertions,'direct_locator_records':len(links),'manifest_occurrences_updated':changed,'six_primary_files_downloaded_with_matching_hashes':True,'historical_mapping_limit':'Exact retained assertions verified, not independent public validation of original author workbook.'}
    writejson(WORK/'mapping-audit.json',audit)
    # Only these delivery records may replace bytes in the old package.
    replacements={manifest,'docs/release/release-map-v1.md'}
    additions={tracepath,'docs/release/mapping-traceability-v1.md',REL+'/link-request.json',REL+'/link-results.json',REL+'/mapping-audit.json',REL+'/repair.py'}
    DEST.mkdir(exist_ok=True)
    archive=DEST/'fungallink-presubmission-release-v2.zip'
    assert not archive.exists(),'Never overwrite an existing candidate'
    files={}
    with zipfile.ZipFile(OLD) as src,zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as dst:
        for name in sorted(names|additions):
            b=(ROOT/name).read_bytes() if name in replacements|additions else src.read(name)
            dst.writestr(name,b);files[name]={'bytes':len(b),'sha256':digest(b)}
        newman={**oldman,'scope':'Private v2 provenance-link delivery correction; scientific payloads unchanged from v1.','files':files}
        dst.writestr('REVIEW-MANIFEST.json',json.dumps(newman,indent=2)+'\n')
    with zipfile.ZipFile(archive) as check:
        for name,meta in files.items():assert digest(check.read(name))==meta['sha256']
    unchanged=[n for n in names if files[n]==oldman['files'][n]]
    assert set(names)-set(unchanged)<=replacements
    receipt={'status':'passed','created_utc':datetime.now(timezone.utc).isoformat(),'archive':archive.relative_to(ROOT).as_posix(),'bytes':archive.stat().st_size,'sha256':digest(archive.read_bytes()),'payloads':len(files),'inherited_payloads_byte_identical':len(unchanged),'changed_inherited_paths':sorted(names-set(unchanged)),'new_paths':sorted(additions-names),'prior_archive_sha256':digest(OLD.read_bytes()),'validation':'Every ZIP payload read and hashed. Exact query/target joins checked. Scientific reruns not performed: all prior scientific payloads unchanged.','mapping_audit':REL+'/mapping-audit.json'}
    writejson(DEST/'build-receipt.json',receipt)
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
