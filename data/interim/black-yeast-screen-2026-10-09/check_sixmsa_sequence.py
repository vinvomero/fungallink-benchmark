from Bio import SeqIO
from pathlib import Path
import gzip,json,hashlib,datetime,platform
p=Path('data/interim/black-yeast-screen-2026-10-09');ref=SeqIO.read(p/'BGC0001276.3.gbk','genbank');features=[f for f in ref.features if f.type=='CDS' and 'translation' in f.qualifiers];print([(f.qualifiers.get('protein_id'),len(f.qualifiers['translation'][0])) for f in features]);assert len(features)==1
protein=features[0].qualifiers['translation'][0];hits=[];n=0;length=0
with gzip.open(p/'GCA_060307435.1_ASM6030743v1_genomic.fna.gz','rt') as handle:
 for r in SeqIO.parse(handle,'fasta'):
  n+=1;length+=len(r)
  for strand,seq in [(1,r.seq),(-1,r.seq.reverse_complement())]:
   for frame in range(3):
    translated=str(seq[frame:len(seq)-(len(seq)-frame)%3].translate())
    start=translated.find(protein)
    while start!=-1:
     a=frame+3*start;b=a+3*len(protein);lo,hi=(a,b) if strand==1 else (len(seq)-b,len(seq)-a)
     hits.append({'scaffold':r.id,'start_0based':lo,'end_exclusive':hi,'strand':strand,'protein_exact_full_length':True,'amino_acids':len(protein)})
     start=translated.find(protein,start+1)
rec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Exact full reference-protein substring search in all six translated reading frames; no fuzzy homology or gene prediction.','reference':'BGC0001276.3','protein_id':features[0].qualifiers.get('protein_id'),'reference_sha256':hashlib.sha256((p/'BGC0001276.3.gbk').read_bytes()).hexdigest(),'assembly':'GCA_060307435.1','assembly_file_sha256':hashlib.sha256((p/'GCA_060307435.1_ASM6030743v1_genomic.fna.gz').read_bytes()).hexdigest(),'scaffolds_scanned':n,'bases_scanned':length,'hits':hits,'limitations':'Exact sequence correspondence alone does not establish chemical identity, feature mapping, complete pathway sufficiency or experimental uniqueness. Diverged or interrupted matches are not excluded.','python':platform.python_version()}
(p/'sixmsa-exact-protein-scan.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
