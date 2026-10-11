"""Plot manuscript figures from saved records only; no scientific analysis is rerun."""
from pathlib import Path
import csv,json,hashlib,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Patch
from matplotlib.colors import LinearSegmentedColormap
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'manuscript/final-2026-10-11'
F=OUT/'figures'; D=OUT/'figure-data'; inputs={}
def read(path):
 p=ROOT/path; inputs[path]=hashlib.sha256(p.read_bytes()).hexdigest(); shutil.copy2(p,D/p.name)
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
TEAL='#087F8C'; NAVY='#17364D'; OCHRE='#B68129'; GRAY='#DCE3E7'; INK='#23343E'; MUTED='#5C6C76'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.labelcolor':INK,'text.color':INK,'xtick.color':MUTED,'ytick.color':INK,'svg.fonttype':'none','pdf.fonttype':42,'savefig.facecolor':'white'})
def save(fig,name):
 for ext in ['svg','pdf','png']:fig.savefig(F/f'{name}.{ext}',dpi=300,bbox_inches='tight',pad_inches=.18)
 plt.close(fig)
def panel(ax,label,title):ax.text(0,1.12,label,transform=ax.transAxes,fontweight='bold',fontsize=13,color=NAVY);ax.text(.085,1.12,title,transform=ax.transAxes,fontsize=12,color=NAVY)
# Figure 1: full data flow, compact enough for a journal-width plate.
fig,ax=plt.subplots(figsize=(10,5.5));ax.set(xlim=(0,10),ylim=(0,5.5));ax.axis('off')
def box(x,y,w,h,title,body,c=TEAL):
 ax.add_patch(Rectangle((x,y),w,h,facecolor='white',edgecolor=c,lw=1.2))
 ax.text(x+.17,y+h-.23,title,fontsize=11,fontweight='bold',color=c,va='top')
 ax.text(x+.17,y+h-.68,body,fontsize=9.5,va='top',linespacing=1.55,color=INK)
def arrow(a,b,c=TEAL):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,lw=1.3,color=c,connectionstyle='arc3'))
box(.05,3.60,2.85,1.55,'Genomic query','Sequence-defined BGC\nor GCF member roster\nAssembly and locus records')
box(.05,1.55,2.85,1.55,'Measured candidates','LC-MS feature table\nSample-to-acquisition links\nUnnamed features retained')
box(3.6,2.6,2.75,1.55,'Linking workflow','Fixed inputs and samples\nOne score per candidate\nExplicit output status',NAVY)
box(7.05,2.6,2.85,1.55,'Retrieval evaluation','Ties and multiple products\nHit and product recovery\nCoverage and missing outputs',NAVY)
box(3.6,.25,6.3,1.40,'Qualified evidence','Query-target links at the supported chemical resolution\nDirect or reference-supported evidence; separate evaluation inputs',OCHRE)
arrow((2.9,4.2),(3.6,3.7));arrow((2.9,2.2),(3.6,3.0));arrow((6.35,3.35),(7.05,3.35),NAVY);arrow((8.4,1.65),(8.4,2.6),OCHRE)
ax.text(5.05,4.52,'COMPLETE CAESAR EVALUATIONS',ha='center',fontsize=9,color=MUTED)
ax.text(5.05,4.98,'7 query views  ·  9,339 candidates',ha='center',fontsize=13,color=NAVY)
ax.text(.07,.65,'Unknown links\nremain unlabeled',fontsize=10,color=MUTED,linespacing=1.5)
save(fig,'Figure-1')
# Figure 2: same relationship denominator in two panels; query counts explicit.
rows=read('data/curated/relationship-readiness-v1.tsv')
cohorts=['caesar2023','facms2017','hex2018','burger2025_trichoderma','blackyeast2026']; labels=['Caesar','FAC-MS','HEx','Trichoderma','Black-yeast study']
summary=[]
for co,label in zip(cohorts,labels):
 rr=[r for r in rows if r['cohort']==co]
 summary.append({'cohort':label,'relationships':len(rr),'queries':len({r['query_id'] for r in rr}),**{s:sum(r['input_state']==s for r in rr) for s in ['complete','partial','missing']},'direct':sum('direct' in r['evidence_class'] for r in rr),'reference':sum('reference' in r['evidence_class'] for r in rr)})
assert sum(r['complete'] for r in summary)==11
with (D/'cohort-counts.tsv').open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=summary[0],delimiter='\t');w.writeheader();w.writerows(summary)
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4.9),gridspec_kw={'width_ratios':[1,1.12]});fig.subplots_adjust(left=.18,right=.97,top=.80,bottom=.18,wspace=.27)
y=np.arange(5)
for ax,fields,colors in [(ax1,['direct','reference'],[NAVY,OCHRE]),(ax2,['complete','partial','missing'],[TEAL,OCHRE,GRAY])]:
 left=np.zeros(5)
 for key,color in zip(fields,colors):
  vals=np.array([s[key] for s in summary]); ax.barh(y,vals,left=left,height=.52,color=color)
  for i,v in enumerate(vals):
   if v:ax.text(left[i]+v/2,i,str(v),ha='center',va='center',color=INK if color==GRAY else 'white',fontsize=10,fontweight='bold')
  left+=vals
 ax.set(xlim=(0,16),xticks=[0,5,10,15],xlabel='Relationships',ylim=(4.65,-.65));ax.grid(axis='x',color='#edf0f2',lw=.7);ax.set_axisbelow(True);ax.tick_params(length=0)
ax1.set_yticks(y,labels);ax2.set_yticks(y,['']*5)
panel(ax1,'a','Evidence class');panel(ax2,'b','Evaluation coverage')
ax2.text(1.06,1.02,'Queries',transform=ax2.transAxes,ha='center',fontsize=9,color=MUTED)
for i,s in enumerate(summary):ax2.text(17.1,i,str(s['queries']),ha='center',va='center',fontsize=11,color=NAVY,clip_on=False)
ax1.legend(handles=[Patch(color=NAVY,label='Direct'),Patch(color=OCHRE,label='Reference-supported')],loc='upper left',bbox_to_anchor=(-.02,-.18),frameon=False,fontsize=9)
ax2.legend(handles=[Patch(color=TEAL,label='Complete'),Patch(color=OCHRE,label='Partial'),Patch(color=GRAY,label='Missing inputs')],loc='upper left',bbox_to_anchor=(-.02,-.18),frameon=False,fontsize=9,ncol=2)
fig.text(.18,.95,'30 relationships  ·  16 biological query identities',fontsize=14,color=NAVY)
save(fig,'Figure-2')
# Figure 3: retain unavailable denominator, show only observed chemical cells.
structures=read('data/processed/similarity-independence-v1/structures.tsv'); pairs=read('data/processed/similarity-independence-v1/chemical-pairs.tsv')
ss=[s for s in structures if s['mapping_status']=='supported']; ids=[s['relationship_id'] for s in ss]; names=[s['product'][0].upper()+s['product'][1:] for s in ss]
mat=np.full((5,5),np.nan)
for r in pairs:
 if r['tanimoto'] and r['relationship_a'] in ids and r['relationship_b'] in ids:
  i,j=ids.index(r['relationship_a']),ids.index(r['relationship_b']);mat[i,j]=mat[j,i]=float(r['tanimoto'])
assert np.isfinite(mat).sum()==20
fig=plt.figure(figsize=(10,5.55));gs=fig.add_gridspec(1,2,width_ratios=[1.12,1],left=.18,right=.98,top=.80,bottom=.22,wspace=.45);ax=fig.add_subplot(gs[0]);ax2=fig.add_subplot(gs[1])
cm=LinearSegmentedColormap.from_list('connectivity',['#F2F7F7','#80B6BC',TEAL]);cm.set_bad('#F1F3F4');im=ax.imshow(mat,vmin=0,vmax=.16,cmap=cm)
ax.set_xticks(range(5),names,rotation=45,ha='right',fontsize=8.5);ax.set_yticks(range(5),names,fontsize=8.5);ax.tick_params(length=0)
for i in range(5):
 for j in range(5):
  if np.isfinite(mat[i,j]):ax.text(j,i,f'{mat[i,j]:.3f}',ha='center',va='center',fontsize=9,color='white' if mat[i,j]>.095 else INK)
cb=fig.colorbar(im,ax=ax,orientation='horizontal',fraction=.04,pad=.33,ticks=[0,.08,.16]);cb.set_label('Morgan Tanimoto similarity',fontsize=9)
panel(ax,'a','Supported chemical pairs');ax2.axis('off');panel(ax2,'b','Comparison scope')
for yy,title,value,note in [(1.0,'CHEMICAL','10 / 435 relationship pairs','5 supported structures; 25 unavailable'),(.64,'GENOMIC','3,575 / 10,516 core pair records','Compatible annotated roles only'),(.28,'SPECTRAL','46,290 within-pool pairs','93 at cosine ≥0.7 and ≥6 matched peaks\n51 at cosine ≥0.9 and ≥6 matched peaks')]:
 ax2.text(0,yy,title,transform=ax2.transAxes,color=TEAL,fontsize=9,fontweight='bold',va='top');ax2.text(0,yy-.08,value,transform=ax2.transAxes,color=NAVY,fontsize=12,va='top');ax2.text(0,yy-.18,note,transform=ax2.transAxes,color=MUTED,fontsize=9,va='top',linespacing=1.6)
fig.text(.18,.95,'Similarity is measurable only for retained representations',fontsize=14,color=NAVY)
save(fig,'Figure-3')
# Existing supporting plates are scientific plots from frozen data, retained without changing values.
for new,old in [('Figure-S1','initial-comparison-2026-10-07'),('Figure-S2','figure4-expanded-sensitivity'),('Figure-S3','figure5-product-retrieval')]:
 for ext in ['svg','pdf']:
  src=ROOT/'manuscript/figures'/f'{old}.{ext}';shutil.copy2(src,F/f'{new}.{ext}');inputs[str(src.relative_to(ROOT))]=hashlib.sha256(src.read_bytes()).hexdigest()
for name in ['benchmark-figure-set-2026-10-07.py','initial-comparison-2026-10-07.py']:
 shutil.copy2(ROOT/'manuscript/figures'/name,OUT/'production'/('original-'+name))
manifest={'inputs':inputs,'new_figures':['Figure-1','Figure-2','Figure-3'],'retained_supporting_plates':['Figure-S1','Figure-S2','Figure-S3'],'scientific_recomputation':False,'aggregation':'Figure 2 counts rows and unique query IDs in saved readiness table; Figure 3 reads saved chemical similarities.','outputs':{str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in F.iterdir()}}
(OUT/'figure-data/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(summary,indent=2))

