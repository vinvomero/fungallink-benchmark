from pathlib import Path
import json, hashlib
from Bio import SeqIO
p=Path(__file__).resolve().parent
r=SeqIO.read(p/'fac.gb','genbank')
rows=[]
for f in r.features:
 if f.type=='CDS' and f.qualifiers.get('gene',[''])[0] in ['FAC38_35','FAC38_36']:
  protein=str(f.extract(r.seq).translate(to_stop=True))
  assert protein==f.qualifiers['translation'][0]
  rows.append(dict(gene=f.qualifiers['gene'][0],start=int(f.location.start)+1,end=int(f.location.end),strand=f.location.strand,protein_id=f.qualifiers['protein_id'][0],protein_length=len(protein),translation_match=True))
assert len(rows)==2
start=min(x['start'] for x in rows);end=max(x['end'] for x in rows)
assert (start,end)==(92115,102627)
seq=str(r.seq[start-1:end]).upper()
(p/'query-envelope.fna').write_text('>'+r.id+':'+str(start)+'-'+str(end)+'|gene-envelope-v1\n'+seq+'\n')
audit=dict(accession=r.id,record_length=len(r.seq),genes=rows,query_start=start,query_end=end,query_length=len(seq),sequence_sha256=hashlib.sha256(seq.encode()).hexdigest(),genbank_sha256=hashlib.sha256((p/'fac.gb').read_bytes()).hexdigest(),scope='Deposited tested-gene envelope; no whole-genome exclusivity or native input activation')
(p/'query-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit))
