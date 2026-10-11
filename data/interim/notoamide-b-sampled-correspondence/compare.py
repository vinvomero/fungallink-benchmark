from pathlib import Path
import zipfile,hashlib,re,json,platform
from bs4 import BeautifulSoup
import bs4,Bio
from Bio import Align
from Bio.Align import substitution_matrices
p=Path('data/interim/notoamide-b-sampled-correspondence')
z=Path('data/raw/sources/caesar-2023/41589_2023_1276_MOESM3_ESM.zip')
with zipfile.ZipFile(z) as f:raw=f.read('Supplementary Data 1/NRPS_66.html')
s=BeautifulSoup(raw,'html.parser');records={};roster=[]
for d in s.find_all('div',style='margin-bottom: 50px; display: flex; flex-direction: column'):
 labels=[b.text for b in d.find_all('b')];key=labels[0] if labels[1]=='MIBiG' else labels[1]
 roster.append(dict(labels=labels,protein_count=len(d.find_all('polygon'))))
 if key not in ['BGC0000818.1','BGC0001084.1','FMGX0011']:continue
 records[key]=[dict(id=q['id'],sequence=re.search(r"openBlast\('([^']+)'\)",q['onclick']).group(1),points=q['points'],annotation=q.title.text,index=i+1) for i,q in enumerate(d.find_all('polygon'))]
a=Align.PairwiseAligner(mode='global',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-10,extend_gap_score=-0.5)
rows=[]
for ref in ['BGC0000818.1','BGC0001084.1']:
 for r in records[ref]:
  scores=[a.score(r['sequence'],q['sequence']) for q in records['FMGX0011']];best=max(scores);ix=scores.index(best);q=records['FMGX0011'][ix];al=a.align(r['sequence'],q['sequence'])[0];x,y=al[0],al[1]
  pairs=sum(i!='-' and j!='-' for i,j in zip(x,y));matches=sum(i==j and i!='-' for i,j in zip(x,y))
  rows.append(dict(reference=ref,reference_id=r['id'],sample_id=q['id'],reference_index=r['index'],sample_index=q['index'],reference_length=len(r['sequence']),sample_length=len(q['sequence']),paired_residues=pairs,matches=matches,identity_pct=100*matches/pairs,reference_coverage_pct=100*pairs/len(r['sequence']),sample_coverage_pct=100*pairs/len(q['sequence']),alignment_columns=len(x),score=best,second_best_score=sorted(scores)[-2],best_ties=scores.count(best),reference_sha256=hashlib.sha256(r['sequence'].encode()).hexdigest(),sample_sha256=hashlib.sha256(q['sequence'].encode()).hexdigest()))
result=dict(python=platform.python_version(),biopython=Bio.__version__,beautifulsoup=bs4.__version__,zip_sha256=hashlib.sha256(z.read_bytes()).hexdigest(),member_sha256=hashlib.sha256(raw).hexdigest(),roster=roster,rows=rows)
(p/'comparison.json').write_text(json.dumps(result,indent=2))
(p/'selected-records.json').write_text(json.dumps(records,indent=2))
for r in rows:print(r['reference_id'],r['sample_id'],r['reference_length'],r['sample_length'],round(r['identity_pct'],2),round(r['reference_coverage_pct'],2),round(r['sample_coverage_pct'],2))
