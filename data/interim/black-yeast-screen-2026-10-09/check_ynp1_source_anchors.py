"""Read-only source-anchor audit; does not infer a producer relationship."""
from pathlib import Path
import collections, datetime, gzip, hashlib, json, platform
from Bio import SeqIO
from Bio.Seq import Seq

P = Path(__file__).resolve().parent
assembly = P / 'GCA_059994315.1_ASM5999431v1_genomic.gbff.gz'
# Published supplementary primer table; retain names and orientation.
anchors = {
    'PR_YNP284': 'ATGTCTCCAATGAAACCTGAGAAG',
    'PR_YNP285': 'CATAGTATCGCCGTCGTCGG',
    'PR_YNP289': 'CGTCGCTCCAGTGCCTGC',
    'PR_YNP293': 'CTAAGATCCCTTCTCTCCCATATAAGG',
}
with gzip.open(assembly, 'rt') as stream:
    records = list(SeqIO.parse(stream, 'genbank'))
hits = []
for record in records:
    for strand, seq in [(1, str(record.seq)), (-1, str(record.seq.reverse_complement()))]:
        matches = {}
        for name, primer in anchors.items():
            target = primer if name == 'PR_YNP284' else str(Seq(primer).reverse_complement())
            offsets = []
            start = seq.find(target)
            while start >= 0:
                offsets.append(start)
                start = seq.find(target, start + 1)
            matches[name] = offsets
        if any(matches.values()):
            item = dict(scaffold=record.id, strand=strand,
                        offsets_in_oriented_scaffold_0based=matches)
            if all(len(v) == 1 for v in matches.values()):
                a = matches['PR_YNP284'][0]
                b = matches['PR_YNP293'][0] + len(anchors['PR_YNP293'])
                if a < matches['PR_YNP285'][0] < matches['PR_YNP289'][0] < b:
                    nt = seq[a:b]
                    aa = str(Seq(nt).translate()) if len(nt) % 3 == 0 else ''
                    lo, hi = (a, b) if strand == 1 else (len(seq)-b, len(seq)-a)
                    item['source_bounded_candidate'] = dict(
                        start_0based=lo, end_exclusive=hi, nucleotides=len(nt),
                        starts_atg=nt.startswith('ATG'), terminal_stop=aa.endswith('*'),
                        internal_stops=aa[:-1].count('*'), amino_acids_excluding_stop=len(aa.rstrip('*')),
                        nt_sha256=hashlib.sha256(nt.encode()).hexdigest())
                    if aa and aa.endswith('*') and '*' not in aa[:-1]:
                        (P/'ynp1-adne1-candidate.fna').write_text(
                            f'>{record.id}:{lo+1}-{hi}|strand={strand}|source-primer-bounded-unadmitted\n{nt}\n')
            hits.append(item)
additional = []
for gene, scaffold, first, last, primer_ids in [
    ('adnE2', 'JBXVST010000033.1', 'GTTTGCCCATCTAGAAATCGC', 'CTACTTGTAGAACGCAATCTTCACTCC', ['PR_YNP347','PR_YNP346']),
    ('adnE3-original-fusion', 'JBXVST010000016.1', 'GGCTGCTATACCTCCCACTC', 'AGACTTTGCGTCTCTTGACGAG', ['PR_YNP344','PR_YNP345']),
]:
    # Source USER tails are excluded; boundaries below come from observed bases.
    record = next(r for r in records if r.id == scaffold)
    seq = str(record.seq.reverse_complement())
    end_anchor = str(Seq(last).reverse_complement())
    assert seq.count(first) == seq.count(end_anchor) == 1
    start = seq.index(first) - 2
    anchor_end = seq.index(end_anchor) + len(end_anchor)
    assert seq[start:start+3] == 'ATG'
    remaining = seq[start:]
    translation = str(Seq(remaining[:len(remaining)//3*3]).translate())
    first_stop = translation.find('*')
    assert first_stop >= 0
    end = start + 3*(first_stop+1)
    # Explicit small endpoint difference, not unrestricted gene prediction.
    assert 0 <= end-anchor_end <= 2
    nt = seq[start:end]
    lo, hi = len(seq)-end, len(seq)-start
    name = f'ynp1-{gene}-candidate.fna'
    (P/name).write_text(f'>{scaffold}:{lo+1}-{hi}|strand=-1|source-primer-bounded-unadmitted\n{nt}\n')
    additional.append(dict(gene=gene, scaffold=scaffold, strand=-1, primer_ids=primer_ids,
        start_0based=lo, end_exclusive=hi, nucleotides=len(nt), amino_acids=first_stop,
        terminal_stop=nt[-3:], stop_bases_beyond_reverse_anchor=end-anchor_end,
        ambiguous_bases=sum(b not in 'ACGT' for b in nt),
        nt_sha256=hashlib.sha256(nt.encode()).hexdigest(), output=name,
        limitation='Observed CDS candidate in nonproducing POP4; two terminal bases for original adnE3 lie beyond the reverse-primer anchor. Shared ancestry is not direct producer sequencing.'))
result = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    assembly='GCA_059994315.1', assembly_sha256=hashlib.sha256(assembly.read_bytes()).hexdigest(),
    command='python data/interim/black-yeast-screen-2026-10-09/check_ynp1_source_anchors.py',
    python=platform.python_version(), status='completed',
    input_source='Published Supplementary Table11 primer IDs PR_YNP284/285/289/293; original PDF retained',
    records=len(records), bases=sum(len(r) for r in records),
    feature_counts=dict(collections.Counter(f.type for r in records for f in r.features)),
    hits=hits, additional_candidates=additional,
    limitations='Exact primer anchors and intact translation do not independently validate gene identity, producer sequence identity or a measured-product linkage. Retain source fusion, not corrected genes.')
(P/'ynp1-source-anchor-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
