from pathlib import Path
import csv,json,hashlib,re
p=Path('data/interim/notoamide-b-sampled-correspondence');d=json.loads((p/'family-comparison.json').read_text());rows=list(csv.DictReader(open('data/curated/notoamide-b-sampled-correspondence-2026-10-03.tsv'),delimiter='\t'));core=[r for r in rows if r['sampled_label']=='FMGX0064' and r['reference']=='BGC0000818.1' and int(r['reference_index'])<=10]
for key in ['identity_pct','reference_coverage_pct','sample_coverage_pct']:print(key,min(float(r[key]) for r in core),max(float(r[key]) for r in core))
assert len(rows)==259 and len(d['all_scores'])==3626
assert len(set((r['sampled_label'],r['reference_id']) for r in rows))==259
assert len(set(r['sampled_label'] for r in rows))==7
assert all(r['reciprocal_best_within_reference_drawing']=='True' for r in core)
assert all(int(r['best_ties'])==1 for r in core)
for r in rows:
 assert abs(float(r['identity_pct'])-100*int(r['matches'])/int(r['paired_residues']))<1e-9
 assert abs(float(r['reference_coverage_pct'])-100*int(r['paired_residues'])/int(r['reference_length']))<1e-9
 assert abs(float(r['sample_coverage_pct'])-100*int(r['paired_residues'])/int(r['sample_length']))<1e-9
feature=json.loads((p/'feature-family-check.json').read_text());assert feature['feature_id']==9213 and [feature['values'][c] for c in ['JF','JG','JH']]==[35800000,28100000,88300000]
receipts=[{'date':'2026-10-03','url':'https://mycocosm.jgi.doe.gov/Asposti1/Asposti1.home.html','access':'web_open_indexed_official_page_success;local_requests_403','finding':'Asposti1 v1.0 home names sequenced strain Aspergillus ostianus CBS103.07','web_ref':'turn139view0','local_http_response':'Asposti1.html'}, {'date':'2026-10-03','url':'https://www.jcm.riken.jp/cgi-bin/jcm/jcm_number?JCM=1959','access':'web_open_and_local_requests_200','finding':'JCM collection alias list connects CBS103.07 and NRRL420','local_http_response':'jcm1959.html'}, {'date':'2026-10-03','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3511817/','access':'indexed_primary_text_search_success;direct_open_challenge','finding':'Proposed locus-pathway account; partial experimental early-step support, inferred intervening assignments','web_ref':'turn142search0'}, {'date':'2026-10-03','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC7483341/','access':'indexed_primary_text_search_success;direct_open_challenge','finding':'Product-specific biochemical reaction support; not full native-pathway causal validation','web_ref':'turn134search4'}]
(p/'source-receipts.json').write_text(json.dumps(receipts,indent=2))
files=[p/'compare_family.py',p/'write_family.py',p/'family-comparison.json',p/'family-records.json',p/'assembly-report.json',p/'VTSW01000173.metadata.txt',p/'Asposti1.html',p/'jcm1959.html',p/'feature-family-check.json',p/'source-receipts.json',Path('data/curated/caesar-study-roster-2026-10-02.tsv'),Path('data/interim/caesar-census-review/BGC0000818.html')]
(p/'hashes.json').write_text(json.dumps({str(f).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2))
doc=Path('docs/evidence/notoamide-b-sampled-correspondence-2026-10-03.md');txt=doc.read_text()
for target in re.findall(r'\]\(([^)]+)\)',txt):
 if not target.startswith('http'):assert (doc.parent/target).resolve().exists(),target
checks={'tsv_rows':259,'unique_member_reference_pairs':259,'reference_proteins':37,'displayed_sample_proteins':98,'cross_record_scores':3626,'member_count':7,'FMGX0064_reciprocal_core_records':10,'feature9213_NRRL420_values_verified':True,'formula_checks':'all259_pass','local_markdown_links':'pass','note_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),'tsv_sha256':hashlib.sha256(Path('data/curated/notoamide-b-sampled-correspondence-2026-10-03.tsv').read_bytes()).hexdigest()}
(p/'verification.json').write_text(json.dumps(checks,indent=2));print(checks)
