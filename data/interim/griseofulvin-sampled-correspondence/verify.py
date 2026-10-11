from pathlib import Path
import json
from Bio import Align
from Bio.Align import substitution_matrices
root=Path('data/interim/griseofulvin-sampled-correspondence'); d=json.loads((root/'selected-records.json').read_text()); c=json.loads((root/'comparison.json').read_text())
a=Align.PairwiseAligner(mode='global',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-10,extend_gap_score=-0.5)
def strand(p):
 vals=list(map(float,p.replace(' ',',').split(','))); v=list(zip(vals[::2],vals[1::2])); return '+' if v[3][0]>v[2][0] else '-'
for r in c['rows'][4:17]:
 x=next(q for q in d['reference'] if q['id']==r['reference_id']); y=next(q for q in d['sample'] if q['id']==r['sample_id']); best=max(d['reference'],key=lambda q:a.score(y['sequence'],q['sequence']))
 print(r['reference_id'], r['sample_id'],'pairs',r['paired_residues'],'match',r['matches'],'cols',r['alignment_columns'],'score',r['score'],'second',r['second_best_score'],'reciprocal',best['id']==r['reference_id'],'direction',strand(x['points']),strand(y['points']))
print('exact',sum(r['exact'] for r in c['rows'][4:17]))

