from Bio import SeqIO
from pathlib import Path
import gzip,json,collections
p=Path('data/interim/black-yeast-screen-2026-10-09');r=SeqIO.read(p/'BGC0001276.3.gbk','genbank');protein=next(f.qualifiers['translation'][0] for f in r.features if f.type=='CDS');seeds=[(i,protein[i:i+20]) for i in range(0,len(protein)-19,100)];hits=[]
with gzip.open(p/'GCA_060307435.1_ASM6030743v1_genomic.fna.gz','rt') as h:
 for rec in SeqIO.parse(h,'fasta'):
  for strand,seq in [(1,rec.seq),(-1,rec.seq.reverse_complement())]:
   for frame in range(3):
    t=str(seq[frame:len(seq)-(len(seq)-frame)%3].translate())
    for q,s in seeds:
     start=t.find(s)
     while start!=-1:
      hits.append({'scaffold':rec.id,'strand':strand,'frame':frame,'query_aa_start':q,'target_aa_start':start,'implied_query_start_nt':frame+3*(start-q)})
      start=t.find(s,start+1)
(p/'sixmsa-anchor-scan.json').write_text(json.dumps({'seed_length':20,'seed_step':100,'seed_count':len(seeds),'hits':hits,'status':'diagnostic only; not an identity or functional validation'},indent=2)+'\n')
counts=collections.Counter((x['scaffold'],x['strand'],x['frame'],x['implied_query_start_nt']) for x in hits)
print(counts.most_common(8))
