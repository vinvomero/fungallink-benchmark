from pathlib import Path
import zipfile,hashlib,re,json
from bs4 import BeautifulSoup
from Bio import Align
from Bio.Align import substitution_matrices
import Bio
root=Path('data/interim/griseofulvin-sampled-correspondence')
z=Path('data/raw/sources/caesar-2023/41589_2023_1276_MOESM3_ESM.zip')
with zipfile.ZipFile(z) as f: raw=f.read('Supplementary Data 1/NRPKS_18.html')
s=BeautifulSoup(raw,'html.parser')
records={}
for d in s.find_all('div',style='margin-bottom: 50px; display: flex; flex-direction: column'):
 labels=[b.text for b in d.find_all('b')]
 if not any(x in labels for x in ['BGC0000070.1','FMGX0099']): continue
 key='reference' if 'BGC0000070.1' in labels else 'sample'
 records[key]=[dict(id=p['id'],sequence=re.search(r"openBlast\('([^']+)'\)",p['onclick']).group(1),points=p['points'],annotation=p.title.text) for p in d.find_all('polygon')]
(root/'selected-records.json').write_text(json.dumps(records,indent=2))
a=Align.PairwiseAligner(mode='global',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-10,extend_gap_score=-0.5)
rows=[]
for r in records['reference']:
 scores=[a.score(r['sequence'],q['sequence']) for q in records['sample']]
 ix=max(range(len(scores)),key=scores.__getitem__); q=records['sample'][ix]
 al=a.align(r['sequence'],q['sequence'])[0]; x,y=al[0],al[1]
 pairs=sum(i!='-' and j!='-' for i,j in zip(x,y)); matches=sum(i==j and i!='-' for i,j in zip(x,y))
 rows.append(dict(reference_id=r['id'],sample_id=q['id'],reference_length=len(r['sequence']),sample_length=len(q['sequence']),paired_residues=pairs,matches=matches,identity_pct=100*matches/pairs,reference_coverage_pct=100*pairs/len(r['sequence']),sample_coverage_pct=100*pairs/len(q['sequence']),alignment_columns=len(x),score=scores[ix],second_best_score=sorted(scores)[-2],exact=r['sequence']==q['sequence'],reference_sha256=hashlib.sha256(r['sequence'].encode()).hexdigest(),sample_sha256=hashlib.sha256(q['sequence'].encode()).hexdigest()))
(root/'comparison.json').write_text(json.dumps(dict(biopython=Bio.__version__,zip_sha256=hashlib.sha256(z.read_bytes()).hexdigest(),member_sha256=hashlib.sha256(raw).hexdigest(),rows=rows),indent=2))
for r in rows: print(r['reference_id'],r['sample_id'],r['reference_length'],r['sample_length'],round(r['identity_pct'],3),round(r['reference_coverage_pct'],3),round(r['sample_coverage_pct'],3),r['exact'])
