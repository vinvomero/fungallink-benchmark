"""Build Figures 1, 2, 4 and 5 from retained inputs. No scoring or network access.

Run: python manuscript/figures/benchmark-figure-set-2026-10-07.py
Figure 3 is the unchanged initial-comparison-2026-10-07 figure.
"""
import csv
import hashlib
import json
import platform
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIMARY = 'draft_all_source_observations'
METHODS = [('global_prevalence', 'Global prevalence'),
           ('prevalence_difference', 'Prevalence difference'),
           ('metcalf_raw', 'Raw Metcalf'),
           ('metcalf_standardized', 'Standardized Metcalf')]
COLORS = ['#636363', '#0072B2', '#009E73', '#CC79A7']
SOURCES = {}
OUTPUTS = []
DATA = {}

def source(path):
    p = ROOT / path
    SOURCES[path] = hashlib.sha256(p.read_bytes()).hexdigest()
    return p

def read_json(path):
    return json.loads(source(path).read_text(encoding='utf-8-sig'))

def read_tsv(path):
    return list(csv.DictReader(source(path).open(encoding='utf-8-sig'), delimiter='\t'))

def save(fig, name):
    for ext in ['svg', 'pdf', 'png']:
        p = HERE / f'{name}.{ext}'
        fig.savefig(p, dpi=220, facecolor='white', bbox_inches='tight')
        OUTPUTS.append(p)
    plt.close(fig)

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
    'axes.spines.top':False, 'axes.spines.right':False,
    'pdf.fonttype':42, 'svg.fonttype':'none',
    'svg.hashsalt':'fungallink-figure-set-2026-10-07'})
ledger = read_tsv('data/curated/label-evidence.tsv')
gold = read_json('data/processed/source-selected-gcf-expanded-labels-v2/gold/benchmark.json')
rows = read_tsv('manuscript/expanded-label-results-2026-10-07.tsv')
gqueries = {q['query_id']:q for q in gold['queries']}
scored_ids = {p for q in gold['queries'] for p in q['products']}
by_id = {r['relationship_id']:r for r in ledger}
assert len(ledger)==30 and len({r['query_id'] for r in ledger})==16
assert len(gqueries)==5 and len(scored_ids)==9
assert all(len(q['candidate_ids'])==9339 for q in gold['queries'])
assert len({q['group_id'] for q in gold['queries']})==1
assert Counter(r['proposed_evidence_class'] for r in ledger)=={'directly-supported':20,'reference-supported':10}
assert scored_ids <= by_id.keys()

# Figure 1: schematic arrows describe information access, not causal evidence.
fig, ax = plt.subplots(figsize=(11.5,6.3))
ax.set(xlim=(0,12), ylim=(0,7)); ax.axis('off')
def box(x,y,w,h,text,color='#EDF3F6'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.08',
                 facecolor=color,edgecolor='#6C777D',linewidth=1))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=9)
def arrow(a,b,dashed=False):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#47555D',
                'lw':1.5,'linestyle':'--' if dashed else '-'})
ax.text(0,6.8,'Task and provenance',fontsize=16,weight='bold')
box(.1,4.5,2.5,1.1,'Strain and assembly\nVersioned identifiers\nSource correspondence')
box(3.2,4.5,2.5,1.1,'Query definition\nBGC locus or GCF roster\nCurrent scored track: GCF')
box(.1,2.55,2.5,1.1,'Cultures and LC-MS\nAcquisition crosswalk\nHistorical measured features')
box(3.2,2.55,2.5,1.1,'Full candidate pool\n9,339 measured features\nUnnamed candidates retained')
box(6.4,3.5,2.1,1.5,'Method inputs\nQuery membership\nFeature presence\nObservation roster')
box(9.25,3.5,2.45,1.5,'Ranked candidates\nScores and exact ties\nCoverage and status')
box(6.4,.7,2.1,1.25,'Curated gold\nEvidence-supported\nquery-target links','#F7EEE0')
box(9.25,.7,2.45,1.25,'Evaluator\nKnown-positive retrieval\nAny-hit and all-products','#E7F1E9')
arrow((2.7,5.05),(3.1,5.05)); arrow((2.7,3.1),(3.1,3.1))
arrow((5.8,5.05),(6.3,4.65)); arrow((5.8,3.1),(6.3,3.8))
arrow((8.6,4.25),(9.15,4.25)); arrow((10.45,3.4),(10.45,2.05))
arrow((8.6,1.33),(9.15,1.33),True)
ax.text(7.45,2.25,'Evaluation-only channel',ha='center',fontsize=9,color='#815A24')
ax.text(.1,1.55,'Record separately',weight='bold',fontsize=11)
ax.text(.1,.95,'Evidence strength  |  Biological eligibility\nMethod-input readiness  |  Prior exposure',linespacing=1.6)
ax.text(.1,.05,'Gold is withheld from method input objects. Historical source selection remains exposed; this is retrospective evaluation.',fontsize=9)
save(fig,'figure1-task-provenance')

# Figure 2: audited inventory, deliberately no invented screening denominator.
groups=[('caesar2023','GCF','Caesar 2023 · GCF'),('caesar2023','BGC','Caesar 2023 · BGC'),
        ('burger2025_trichoderma','BGC','Burger 2025 · BGC'),('facms2017','BGC','FAC-MS 2017/18 · BGC'),('hex2018','BGC','HEx 2018 · BGC'),('blackyeast2026','BGC','Expression 2026 · CDS')]
inventory=[]
for c,t,label in groups:
    rr=[r for r in ledger if r['cohort']==c and r['query_type']==t]
    inventory.append(dict(label=label,relationships=len(rr),query_identities=len({r['query_id'] for r in rr}),
        direct=sum(r['proposed_evidence_class']=='directly-supported' for r in rr),
        reference=sum(r['proposed_evidence_class']=='reference-supported' for r in rr),
        scored=sum(r['relationship_id'] in scored_ids for r in rr)))
DATA['inventory']=inventory
fig, axes=plt.subplots(1,2,figsize=(11.5,6),sharey=True)
fig.subplots_adjust(left=.19,right=.98,top=.76,bottom=.26,wspace=.18)
for i,r in enumerate(inventory):
    axes[0].barh(i,r['direct'],color='#0072B2',height=.6)
    axes[0].barh(i,r['reference'],left=r['direct'],color='#E69F00',height=.6)
    axes[1].barh(i,r['scored'],color='#009E73',height=.6)
    axes[1].barh(i,r['relationships']-r['scored'],left=r['scored'],color='#D0D2D3',height=.6)
    for ax in axes: ax.text(r['relationships']+.12,i,str(r['relationships']),va='center')
axes[0].set_yticks(range(len(inventory)),[f"{r['label']}\n{r['query_identities']} query " + ('identity' if r['query_identities']==1 else 'identities') for r in inventory])
axes[0].invert_yaxis()
for ax in axes:
    limit = 2 * ((max(r['relationships'] for r in inventory) + 2) // 2)
    ax.set(xlim=(0,limit),xticks=range(0,limit+1,2),xlabel='Admitted relationships')
    ax.grid(axis='x',alpha=.15); ax.set_axisbelow(True)
axes[0].set_title('A  Relationship evidence',loc='left')
axes[1].set_title('B  Expanded comparison coverage',loc='left')
axes[0].legend(handles=[Line2D([0],[0],color='#0072B2',lw=8,label='Direct'),Line2D([0],[0],color='#E69F00',lw=8,label='Reference')],loc='lower left',bbox_to_anchor=(0,-.36),ncol=2,frameon=False)
axes[1].legend(handles=[Line2D([0],[0],color='#009E73',lw=8,label='Scored'),Line2D([0],[0],color='#D0D2D3',lw=8,label='Unscored')],loc='lower left',bbox_to_anchor=(0,-.36),ncol=2,frameon=False)
fig.suptitle('Audited inventory: 30 relationships, 16 query identities',x=.02,ha='left',fontsize=15,weight='bold')
fig.text(.02,.84,'Twenty direct and ten reference-supported relationships. This is inventory coverage, not a screening flow.',fontsize=10)
fig.text(.02,.035,'Scored subset: nine targets in five GCF queries, all in one conservative analysis group.\nQuery identities and named pathway annotations are not counts of independent pathway groups.',fontsize=10)
save(fig,'figure2-curation-coverage')

# Figure 4: each of the 18 overlapping rosters remains visible.
allmethods=METHODS+[('uniform_random_exact','Uniform random (exact)')]
overall=[r for r in rows if r['scope']=='overall']
assert len(overall)==90 and len({r['roster'] for r in overall})==18
random_exact=read_json('data/processed/source-selected-gcf-expanded-labels-v2-results/exact-random.json')
for r in overall:
    assert int(r['queries'])==5 and int(r['products'])==9 and int(r['candidates'])==9339
    assert float(r['coverage'])==1
    if r['method']=='uniform_random_exact':
        original=random_exact['overall_metrics']
    else:
        ev=read_json(f"data/processed/source-selected-gcf-expanded-labels-v2-results/{r['roster']}--{r['method']}--evaluation.json")
        assert ev['summary']['group_count']==1 and ev['summary']['coverage']==1
        original=ev['summary']['end_to_end']['metrics']
    for metric in ['hit@10','all_products@100']:
        assert abs(float(r[metric])-original[metric])<1e-12
metrics=[('hit@10','A  Expected any-hit@10'),('all_products@100','B  Expected all-products@100')]
DATA['roster_sensitivity']=[]
fig,axes=plt.subplots(1,2,figsize=(11.5,6),sharey=True)
fig.subplots_adjust(left=.23,right=.98,top=.75,bottom=.27,wspace=.16)
for i,(method,label) in enumerate(allmethods):
    rr=sorted([r for r in overall if r['method']==method],key=lambda r:r['roster'])
    assert len(rr)==18
    for ax,(metric,title) in zip(axes,metrics):
        vals=[float(r[metric]) for r in rr]
        primary=next(float(r[metric]) for r in rr if r['roster']==PRIMARY)
        ax.plot([min(vals),max(vals)],[i,i],color='#B8C0C3',lw=1.2,zorder=1)
        for j,r in enumerate(rr):
            if r['roster']!=PRIMARY: ax.plot(float(r[metric]),i+(j-8.5)*.018,'o',ms=4,color='#6D858F',alpha=.7)
        ax.plot(primary,i,'D',ms=7,color='#0072B2',zorder=4)
        DATA['roster_sensitivity'].append({'method':method,'metric':metric,'primary':primary,'minimum':min(vals),'maximum':max(vals),'rosters':[{ 'roster':r['roster'],'value':float(r[metric])} for r in rr]})
        ax.set_title(title,loc='left'); ax.set(xlim=(-.025,1.025),xlabel='Expected fraction of queries')
        ax.grid(axis='x',alpha=.18)
axes[0].set_yticks(range(5),[label for _,label in allmethods]); axes[0].invert_yaxis()
fig.suptitle('Expanded targets under 18 observation rosters',x=.02,ha='left',fontsize=15,weight='bold')
fig.text(.02,.83,'Five GCF queries · nine targets · full 9,339-candidate pool · complete output coverage',fontsize=10)
fig.legend(handles=[Line2D([0],[0],marker='D',color='#0072B2',ls='',label='Primary: 105 observations'),Line2D([0],[0],marker='o',color='#6D858F',ls='',label='Other overlapping rosters: 99 or 102 observations')],loc='lower left',bbox_to_anchor=(.02,.10),ncol=2,frameon=False)
fig.text(.02,.025,'Dots show roster-specific estimates; lines show their ranges, not confidence intervals.\nSource-selected families and prior label exposure are shared across rosters; their effects are not isolated here.',fontsize=10)
save(fig,'figure4-expanded-sensitivity')

# Figure 5: recompute each singleton target's exact score-tie position.
oldgold=read_json('data/processed/source-selected-gcf-analysis-v1/benchmark.json')
oldids={p for q in oldgold['queries'] for p in q['products']}
target_ids=sorted(scored_ids,key=lambda p:(by_id[p]['query_id'],int(by_id[p]['source_feature_id'])))
rankdata=[]
for method,label in METHODS:
    ranks=read_json(f'data/processed/source-selected-gcf-analysis-v1-results/{PRIMARY}--{method}--rankings.json')
    evaluated=read_json(f'data/processed/source-selected-gcf-expanded-labels-v2-results/{PRIMARY}--{method}--evaluation.json')
    assert ranks['score_direction']=='higher' and ranks['method_version']=='0.1.0'
    outputs={o['query_id']:o for o in ranks['outputs']}
    eq={q['query_id']:q for q in evaluated['queries']}
    for pid in target_ids:
        row=by_id[pid]; qid=row['query_id']; q=gqueries[qid]
        scores={s['candidate_id']:s['score'] for s in outputs[qid]['scores']}
        assert len(scores)==9339 and set(scores)==set(q['candidate_ids'])
        assert len(q['products'][pid])==1
        cid=q['products'][pid][0]; score=scores[cid]
        greater=sum(v>score for v in scores.values()); tied=sum(v==score for v in scores.values())
        best,worst=greater+1,greater+tied
        assert eq[qid]['products'][pid]['first_target_rank']=={'best':best,'worst':worst}
        for k in [1,10,100]:
            hit=max(0,min(tied,k-greater))/tied
            assert abs(hit-eq[qid]['products'][pid]['hit'][str(k)])<1e-12
        rankdata.append(dict(method=method,product_id=pid,query_id=qid,candidate_id=cid,
             score=score,greater_score_count=greater,tied_score_count=tied,best=best,worst=worst,
             newly_admitted=pid not in oldids))
DATA['target_rank_intervals']=rankdata
fig,axes=plt.subplots(1,4,figsize=(14,6.3),sharey=True)
fig.subplots_adjust(left=.29,right=.985,top=.71,bottom=.19,wspace=.16)
for ax,(method,label),color in zip(axes,METHODS,COLORS):
    for i,pid in enumerate(target_ids):
        r=next(r for r in rankdata if r['method']==method and r['product_id']==pid)
        if r['newly_admitted']: ax.axhspan(i-.45,i+.45,color='#FFF4D6',zorder=0)
        ax.plot([r['best'],r['worst']],[i,i],color=color,lw=4,solid_capstyle='round')
        ax.plot([r['best'],r['worst']],[i,i],'|',color=color,ms=9)
        ax.text((r['best']*r['worst'])**.5,i-.18,f"{r['best']}–{r['worst']}",ha='center',fontsize=7,color='#333333')
    for cutoff in [10,100]: ax.axvline(cutoff,color='#A6A6A6',lw=.8,ls=':',zorder=0)
    ax.set(xscale='log',xlim=(.8,14000),xticks=[1,10,100,1000,10000],xlabel='Rank (log scale)')
    ax.set_xticklabels(['1','10','100','1k','10k'])
    ax.set_title(label.replace(' ','\n',1),fontsize=10)
labels=[]
for pid in target_ids:
    r=by_id[pid]
    name=r['product'].replace('-associated feature (structure putative)','-associated feature*')
    labels.append(f"{name}  [feature {r['source_feature_id']}]\n{r['query_id'].replace('source:','')}" + ('  · added' if pid not in oldids else ''))
axes[0].set_yticks(range(9),labels,fontsize=9); axes[0].invert_yaxis()
fig.suptitle('Target-level retrieval: exact score-tie intervals',x=.02,ha='left',fontsize=16,weight='bold')
fig.text(.02,.87,'Primary roster, 105 observations. Four local deterministic workflows, implementation 0.1.0.',fontsize=10)
fig.text(.02,.81,'Yellow rows: three added targets. Repeated query IDs identify shared queries, including pst (NRPSPKS_85) and not (NRPS_66).',fontsize=10)
fig.text(.02,.045,'* Pestalamide E/F structures remain putative; each associated measured feature is the evaluated target.\nIntervals are best–worst positions within exact score ties, not biological uncertainty. Nine targets share five queries and one analysis group.',fontsize=10)
save(fig,'figure5-product-retrieval')

receipt={'schema_version':1,'generated_by':Path(__file__).name,
 'route':{'requested_model':'not_requested_this_turn','requested_reasoning':'not_requested_this_turn','actual_serving_receipt':'unavailable'},
 'python':platform.python_version(),'matplotlib':matplotlib.__version__,
 'input_sha256':SOURCES,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'plotted_data':DATA,'checks':{'ledger_relationships':30,'ledger_query_identities':16,
 'direct_relationships':20,'reference_relationships':10,'expanded_queries':5,'expanded_targets':9,
 'candidate_pool':9339,'conservative_analysis_groups':1,'rosters':18,
 'target_method_intervals_recomputed_and_verified':len(rankdata),'roster_method_summaries_crosschecked':len(overall),'scoring_recomputations':0,
 'formats_generated':['svg','pdf','png'],'existing_figure3_modified':False},
 'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUTPUTS}}
(HERE/'figure-set-verification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt['checks'],indent=2))
