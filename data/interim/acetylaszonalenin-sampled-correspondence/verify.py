from pathlib import Path
from Bio import SeqIO
import Bio,sys,hashlib,json,csv
p=Path(__file__).resolve().parent
sha=lambda x: hashlib.sha256(x).hexdigest()
old=SeqIO.read(p/'old_core.gbk','genbank'); sampled=SeqIO.read(p/'sampled_core.gbk','genbank'); ref=SeqIO.read(p/'mibig.gbk','genbank')
a=str(old.seq);b=str(sampled.seq);c=str(ref.seq[20000:32765])
assert len(a)==len(b)==len(c)==12765 and a==b==c
assert len(set(zip(a,b,c)))==len(set(a)) and all(x==y==z for x,y,z in zip(a,b,c))
rows=[]
for f in sampled.features:
 if f.type!='CDS':continue
 tag=f.qualifiers['locus_tag'][0];rf=next(g for g in ref.features if g.type=='CDS' and g.qualifiers.get('locus_tag')==[tag])
 x=f.qualifiers['translation'][0];y=rf.qualifiers['translation'][0]
 assert x==y
 derived=str(f.extract(sampled.seq).translate(to_stop=True));assert derived==x
 assert int(rf.location.start)-20000==int(f.location.start) and int(rf.location.end)-20000==int(f.location.end) and rf.location.strand==f.location.strand
 rows.append(dict(locus_tag=tag,protein_id=f.qualifiers['protein_id'][0],start_1based=2428387+int(f.location.start),end_1based=2428386+int(f.location.end),strand=f.location.strand,reference_length_aa=len(y),sampled_length_aa=len(x),matching_residues=sum(i==j for i,j in zip(x,y)),alignment_columns=len(x),identity_percent=100,reference_coverage_percent=100,sampled_coverage_percent=100,translation_sha256=sha(x.encode()),cds_retranslation_equal=True))
with (p/'protein_comparison.tsv').open('w',newline='',encoding='utf-8') as o:
 w=csv.DictWriter(o,fieldnames=list(rows[0]),delimiter='	');w.writeheader();w.writerows(rows)
receipt=dict(date='2026-10-03',python=sys.version,biopython=Bio.__version__,method='Full string equality and position-by-position comparison; no local alignment, no threshold, no search; independent CDS extraction/retranslation checks',coordinate_convention='One-based inclusive for accession intervals; Python zero-based half-open internally',nucleotide_matches=12765,nucleotide_alignment_columns=12765,old_coverage_percent=100,sampled_coverage_percent=100,mibig_core_coverage_percent=100,core_nt_sha256=sha(a.encode()),offset=2428387-130585,proteins=rows,input_sha256={n:sha((p/n).read_bytes()) for n in ['old_core.gbk','sampled_core.gbk','mibig.gbk','assembly_report.txt','atcc.html']},output_table_sha256=sha((p/'protein_comparison.tsv').read_bytes()),limitations=['Same underlying GenBank annotation, not independent resequencing or independent protein alignment evidence.','Old core has no CDS annotations; its nucleotide identity transfers current annotations only.','Assembly-wide competing-locus search not performed.'])
(p/'verification.json').write_text(json.dumps(receipt,indent=2)+chr(10),encoding='utf-8')
print(json.dumps(receipt,indent=2))

