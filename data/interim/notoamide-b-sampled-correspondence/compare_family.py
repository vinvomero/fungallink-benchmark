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
 records[key]=[dict(id=q['id'],sequence=re.search(r"openBlast\('([^']+)'\)",q['onclick']).group(1),points=q['points'],annotation=q.title.text,index=i+1) for i,q in enumerate(d.find_all('polygon'))]
a=Align.PairwiseAligner(mode='global',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-10,extend_gap_score=-0.5)
rows=[];all_scores=[]
for sample in sorted(k for k in records if k.startswith('FMGX')):
 for ref in ['BGC0000818.1','BGC0001084.1']:
  for r in records[ref]:
   scores=[a.score(r['sequence'],q['sequence']) for q in records[sample]]
   all_scores.extend(dict(sample=sample,reference=ref,reference_id=r['id'],sample_id=q['id'],score=score) for q,score in zip(records[sample],scores))
   best=max(scores);ix=scores.index(best);q=records[sample][ix];al=a.align(r['sequence'],q['sequence'])[0];x,y=al[0],al[1]
   pairs=sum(i!='-' and j!='-' for i,j in zip(x,y));matches=sum(i==j and i!='-' for i,j in zip(x,y))
   rows.append(dict(sample=sample,reference=ref,reference_id=r['id'],sample_id=q['id'],reference_index=r['index'],sample_index=q['index'],reference_length=len(r['sequence']),sample_length=len(q['sequence']),paired_residues=pairs,matches=matches,identity_pct=100*matches/pairs,reference_coverage_pct=100*pairs/len(r['sequence']),sample_coverage_pct=100*pairs/len(q['sequence']),alignment_columns=len(x),score=best,reference_self_score=a.score(r['sequence'],r['sequence']),second_best_score=sorted(scores)[-2],best_ties=scores.count(best),reference_sha256=hashlib.sha256(r['sequence'].encode()).hexdigest(),sample_sha256=hashlib.sha256(q['sequence'].encode()).hexdigest()))
result=dict(python=platform.python_version(),biopython=Bio.__version__,beautifulsoup=bs4.__version__,zip_sha256=hashlib.sha256(z.read_bytes()).hexdigest(),member_sha256=hashlib.sha256(raw).hexdigest(),roster=roster,rows=rows,all_scores=all_scores)
(p/'family-comparison.json').write_text(json.dumps(result,indent=2))
(p/'family-records.json').write_text(json.dumps(records,indent=2))
for sample in sorted(k for k in records if k.startswith('FMGX')):
 selected=[r for r in rows if r['sample']==sample and r['reference']=='BGC0000818.1' and r['reference_index']<=10]
 print(sample,'core mean normalized score',sum(r['score']/r['reference_self_score'] for r in selected)/len(selected),'indices',[r['sample_index'] for r in selected],'identity',[round(r['identity_pct'],1) for r in selected],'refcov',[round(r['reference_coverage_pct'],1) for r in selected])
