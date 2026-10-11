from Bio import SeqIO, Align
from Bio.Align import substitution_matrices
from pathlib import Path
import gzip,json,csv,hashlib
p=Path('data/raw/trichoderma-qm6a-correspondence-2026-10-07'); q=SeqIO.read('data/raw/trichoderma-evidence-2026-10-07/13068_2025_2628_MOESM4_ESM.gbk','genbank'); s=SeqIO.read(p/'qm6a-GL985060.1.gb','genbank')
genome=list(SeqIO.parse(gzip.open(p/'GCA_000167675.2_v2.0_genomic.fna.gz','rt'),'fasta')); proteins=list(SeqIO.parse(gzip.open(p/'GCA_000167675.2_v2.0_protein.faa.gz','rt'),'fasta'))
hits=[]
for rec in genome:
 for strand,seq in [('+',str(q.seq)),('-',str(q.seq.reverse_complement()))]:
  start=0
  while True:
   i=str(rec.seq).upper().find(seq.upper(),start)
   if i<0:break
   hits.append({'accession':rec.id,'start_1based':i+1,'end_1based':i+len(seq),'strand':strand});start=i+1
subset=s[21097:51701]; subset.id='GL985060.1';subset.name='QM6a_ilicicolin';subset.description='QM6a reference source window GL985060.1:21098..51701; retains native annotation, not an experimental mutant assembly';subset.annotations['molecule_type']='DNA';subset.annotations['comment']='Derived from official GL985060.1 with 1-based closed parent coordinates 21098..51701. Native gene models retained; missing triliD and short triliR model not corrected.'
SeqIO.write(subset,p/'qm6a-ilicicolin-reference-window.gbk','genbank');SeqIO.write(subset,p/'qm6a-ilicicolin-reference-window.fasta','fasta')
aligner=Align.PairwiseAligner();aligner.mode='global';aligner.substitution_matrix=substitution_matrices.load('BLOSUM62');aligner.open_gap_score=-10;aligner.extend_gap_score=-0.5
stats=[]
for qf in [f for f in q.features if f.type=='CDS']:
 a=qf.qualifiers['translation'][0]; kq={a[i:i+5] for i in range(len(a)-4)}
 ranked=sorted(((len(kq & {str(b.seq)[i:i+5] for i in range(len(b)-4)}),b) for b in proteins),key=lambda v:v[0],reverse=True)[:3]
 for rank,(common,b) in enumerate(ranked,1):
  al=aligner.align(a,str(b.seq))[0]; cols=al.indices; pairs=[(i,j) for i,j in zip(cols[0],cols[1]) if i>=0 and j>=0]; ident=sum(a[i]==str(b.seq)[j] for i,j in pairs)
  stats.append({'query_protein':qf.qualifiers['protein_id'][0],'query_length':len(a),'rank_by_shared_distinct_5mers':rank,'shared_5mers':common,'target_protein':b.id,'target_length':len(b),'identical_residues':ident,'paired_residues':len(pairs),'alignment_columns':al.shape[1],'identity_paired_percent':100*ident/len(pairs),'identity_all_columns_percent':100*ident/al.shape[1],'query_paired_coverage_percent':100*len(pairs)/len(a),'target_paired_coverage_percent':100*len(pairs)/len(b),'global_alignment_score':al.score})
with (p/'protein-comparison.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=stats[0],delimiter='\t');w.writeheader();w.writerows(stats)
result={'assembly':'GCA_000167675.2','scaffolds_searched':len(genome),'genome_nt':sum(len(r) for r in genome),'proteins_screened':len(proteins),'query_nt':len(q),'exact_nucleotide_hits':hits,'query_nt_sha256':hashlib.sha256(str(q.seq).encode()).hexdigest(),'protein_search_method':'Rank entire proteome by shared distinct amino-acid 5-mers; global BLOSUM62 alignment of top three per query, gap open -10 extend -0.5; bounded heuristic alternatives, not exhaustive homology exclusion','annotation_warning':'Native QM6a annotation lacks triliD and uses short triliR; source RUT-C30 models differ despite identical DNA'}
(p/'comparison-summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print('\n'.join(str(x) for x in stats if x['rank_by_shared_distinct_5mers']==1))
