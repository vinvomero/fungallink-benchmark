from pathlib import Path
import json
from Bio import Align
from Bio.Align import substitution_matrices
root=Path('data/interim/griseofulvin-sampled-correspondence')
d=json.loads((root/'selected-records.json').read_text()); c=json.loads((root/'comparison.json').read_text())
a=Align.PairwiseAligner(mode='global',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-10,extend_gap_score=-0.5)
rows=[]
for r in c['rows'][4:17]:
 x=next(q for q in d['reference'] if q['id']==r['reference_id']); y=next(q for q in d['sample'] if q['id']==r['sample_id'])
 forward=[(q['id'],a.score(x['sequence'],q['sequence'])) for q in d['sample']]
 reverse=[(q['id'],a.score(y['sequence'],q['sequence'])) for q in d['reference']]
 fmax=max(s for _,s in forward); rmax=max(s for _,s in reverse)
 fw=[i for i,s in forward if s==fmax]; rw=[i for i,s in reverse if s==rmax]
 assert fw==[y['id']] and rw==[x['id']]
 rows.append(dict(reference_id=x['id'],sample_id=y['id'],forward_top_score_count=len(fw),reverse_top_score_count=len(rw),forward_margin=fmax-sorted(s for _,s in forward)[-2],reverse_margin=rmax-sorted(s for _,s in reverse)[-2]))
(root/'top-score-uniqueness-2026-10-03.json').write_text(json.dumps(dict(check_date='2026-10-03',all_13_unique_top_scores_both_directions=True,rows=rows),indent=2))
print('All thirteen top scores unique in both directions; minimum forward and reverse margins:', min(r['forward_margin'] for r in rows),min(r['reverse_margin'] for r in rows))
p=Path('docs/evidence/griseofulvin-sampled-correspondence-2026-10-02.md'); t=p.read_text(encoding='utf-8-sig')
t=t.replace('Reviewed 2026-10-02.', 'Started 2026-10-02; completed 2026-10-03 (America/New_York). The filenames retain the start date. The final top-score uniqueness check and report corrections were performed on 2026-10-03; source retrieval dates remain those recorded in the source registry.')
t=t.replace('committed numerical ledger','saved numerical ledger')
t=t.replace('The thirteen reference-region proteins below have distinct reciprocal best matches.', 'The thirteen reference-region proteins below have distinct reciprocal best matches. The 2026-10-03 follow-up counted entries attaining the maximum score in both directions: each of all thirteen comparisons has exactly one top-scoring counterpart. This tests score uniqueness rather than relying on deterministic selection among ties; it does not assert uniqueness of an optimal alignment path.')
t=t.replace('and verification JSON are ignored scratch','and verification JSON, including `top-score-uniqueness-2026-10-03.json`, are ignored scratch')
p.write_text(t,encoding='utf-8')
