from pathlib import Path
import io,zipfile,json,hashlib,warnings
from Bio import SeqIO
from Bio import BiopythonWarning
warnings.simplefilter('ignore',BiopythonWarning)
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent
archive=root/'data/raw/hex-measured-data-screen-2026-10-07/aar5459_DatafileS1.zip'
with zipfile.ZipFile(archive) as z: records=list(SeqIO.parse(io.StringIO(z.read(z.namelist()[0]).decode()),'genbank'))
import sys
case=sys.argv[1]
prefix={'PKS15':'pCHKU39.','PKS23':'pCHSU70.'}[case]
selected=[r for r in records if r.name.startswith(prefix)]
assert len(selected)==2
frames={r.name:[str(strand[offset:].translate()) for strand in [r.seq,r.seq.reverse_complement()] for offset in range(3)] for r in selected}
r=SeqIO.read(out/(case+'.gb'),'genbank');rows=[]
for f in r.features:
 if f.type!='CDS':continue
 protein=f.qualifiers.get('translation',[''])[0]
 matches=[name for name,ff in frames.items() if protein and any(protein in frame for frame in ff)]
 rows.append(dict(locus=f.qualifiers.get('locus_tag'),protein_id=f.qualifiers.get('protein_id'),length=len(protein),full_length_exact_plasmid_matches=matches,partial_location=('<' in str(f.location) or '>' in str(f.location))))
receipt=dict(native_record=r.id,native_interval_length=len(r.seq),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),plasmids=[dict(name=x.name,length=len(x.seq),sequence_sha256=hashlib.sha256(str(x.seq).encode()).hexdigest()) for x in selected],genes=rows,exact_match_genes=sum(bool(x['full_length_exact_plasmid_matches']) for x in rows),total_genes=len(rows),scope='Read-only exact protein containment audit; missing matches do not prove gene absence; no sequence design or admission')
(out/(case+'-correspondence-audit.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
