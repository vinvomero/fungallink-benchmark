# QM6a ilicicolin reference correspondence

Date: 2026-10-07. Requested CE Work route: gpt-6-astra / medium. Actual serving model and effort are unverified. Automated curation and a separate host computation are not human scientific review.

The supplied RUT C-30-labeled nucleotide window matches the public QM6a reference exactly. A defensible sequence-defined reference query is **GCA_000167675.2, GL985060.1:21098..51701 (+), 30,604 nt**. Both coordinates are 1-based and inclusive. The sequence SHA-256 is `759c315a5e2a32176fd1ca1d4ef261f70c2b55af4c143dfe82a2b91e4bef5d62`, identical to the Burger et al. supplementary GBK sequence. This resolves the reference sequence correspondence; it does not authenticate the experimental mutant genomes or settle gene models.

The reference window includes two flanking annotated genes as well as the ilicicolin region. Its boundaries reproduce the published comparison window and are not claimed to be experimentally established minimal BGC boundaries. The native annotation was retained unchanged in the derived GBK.

## Public records and exact sequence check

Exact JGI identifiers from the earlier appraisal led to NCBI protein records linked to scaffold GL985060.1. Their `coded_by` qualifiers and JGI cross-references place TriliA, B, C, E, and the older R model on this scaffold. The [NCBI assembly record](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_000167675.2/) and downloaded assembly report identify strain QM6a, BioSample SAMN02746107, BioProject PRJNA15571, submitter DOE Joint Genome Institute, and the paired RefSeq assembly GCF_000167675.1. GenBank and RefSeq assemblies are reported identical. No authenticated JGI session was needed.

An exact whole-window search, comparing uppercase nucleotide strings on both strands of all 77 assembly records (33,395,713 nt), found only GL985060.1:21098..51701. Identity and query coverage are both 100%; there are zero substitutions or gaps across 30,604 bases. The FASTA is softmasked, so comparisons normalized letter case. A separate host parser obtained the same unique match, recorded in `host-exact-sequence-verification.json`. These searches exclude another exact full-length copy only. They do not exclude shorter or diverged biosynthetic loci.

Reference downloads were modest: genomic FASTA 10,602,580 compressed bytes, protein FASTA 2,801,681 compressed bytes, plus one annotated scaffold and metadata. The source files and reproducible comparison script are in `data/raw/trichoderma-qm6a-correspondence-2026-10-07/`.

## Gene models remain a separate issue

| Role | QM6a locus tag | QM6a protein | Parent interval and strand | Protein length |
|---|---|---|---|---:|
| upstream context | TRIREDRAFT_105224 | EGR50061.1 | 21098..22286 (+) | 344 |
| upstream context | TRIREDRAFT_120872 | EGR50062.1 | 24260..25273 (+) | 320 |
| TriliA | TRIREDRAFT_58285 | EGR50286.1 / XP_006963788.1 | 25618..37773 (-) | 3812 |
| TriliB | TRIREDRAFT_58289 | EGR50063.1 / XP_006963601.1 | 39622..40764 (+) | 350 |
| TriliE | TRIREDRAFT_76204 | EGR50287.1 / XP_006963789.1 | 41344..42694 (-) | 401 |
| TriliC | TRIREDRAFT_58953 | EGR50064.1 / XP_006963602.1 | 45910..47423 (+) | 449 |
| old TriliR model | TRIREDRAFT_72993 | EGR50288.1 / XP_006963790.1 | 49338..50726 (-) | 462 |

Intervals span introns where present; exact exon locations are retained in the source and derived GBK and in `native-qm6a-members.tsv`. TriliD has no CDS annotation in this older QM6a record. Projecting the published RUT C-30 feature ETS03596.1 through the exact nucleotide match places its genomic span at 44040..45025 (-). This is a projected source feature, not a newly verified QM6a transcript model. The article supplies RutC30 JGI ID 75073 for D but no older QM6a identifier.

The source's extended TriliR is stronger evidence than the old native model: supplementary FASTA `QM6a_chrlev_110738cd` is identical to the reverse complement of GL985060.1:49338..51701, and its 787-aa protein is identical to supplied ETS03598.1 and `RutC30_74475_protein`. Thus the source's long R model is sequence-supported at the QM6a locus. The experimental `triliR_w/o_NotI` sequence carries the paper's intentional alteration and is not identical to the unmodified reference coding sequence. The derived GBK does not silently replace the native 462-aa annotation with this curated model.

Protein differences elsewhere must not be described as strain sequence divergence when the entire genomic window is identical. They reflect differing supplied translations/gene models, whose correctness has not been independently adjudicated.

## Protein comparison and bounded alternatives

All 9,115 proteins in the official GenBank proteome were ranked by shared distinct amino-acid 5-mers for each of the eight supplied RUT C-30 proteins. The top three candidates per query were aligned globally using Biopython PairwiseAligner, BLOSUM62, gap open -10, gap extension -0.5. This is a bounded heuristic screen, not an exhaustive BLAST homology search. All 24 alignments, including weak alternative hits, are recorded in `protein-comparison.tsv`.

| Supplied protein | Best screened QM6a protein | Identical / paired residues | Supplied protein coverage | QM6a protein coverage |
|---|---|---:|---:|---:|
| ETS03591.1 | EGR50061.1 | 344 / 344 | 100% | 100% |
| ETS03592.1 | EGR50062.1 | 304 / 304 | 100% | 95.00% |
| ETS03593.1 (A) | EGR50286.1 | 3808 / 3812 | 94.36% | 100% |
| ETS03594.1 (B) | EGR50063.1 | 350 / 350 | 100% | 100% |
| ETS03595.1 (E) | EGR50287.1 | 397 / 401 | 97.33% | 100% |
| ETS03596.1 (D) | no credible annotated counterpart in this bounded screen | weak top candidate has only 4 shared 5-mers | unresolved | unresolved |
| ETS03597.1 (C) | EGR50064.1 | 448 / 449 | 86.18% | 100% |
| ETS03598.1 (R) | EGR50288.1 | 462 / 462 | 58.70% | 100% |

Coverage here means residues paired to a residue, divided by that sequence's full length. Identity among paired residues differs from identity across all gapped alignment columns; both are provided in the TSV. For example, A has 99.90% identity among paired residues but only 94.26% identity across all 4,040 alignment columns. Reporting only the former would conceal the annotation discrepancy. D's unrelated weak top candidate is not accepted as a homolog.

## Use in the benchmark

The locus can now be represented by the retained QM6a reference nucleotide window. Experimental provenance remains the QM6a derivative panel in Burger et al., including the Δmus53 control, OETriliR and its deletions. Reference equality to the supplied comparison window supports locus correspondence; it does not establish every engineered culture's complete genome sequence.

Methods that need complete protein/gene annotations still require a declared, reviewed model set, especially for D and the A/C/E discrepancies. A nucleotide-only query can use the saved sequence with this limitation stated. The previous appraisal's unresolved feature joins are unchanged: this work creates no metabolite feature IDs, admits no labels, and supplies no evidence that K's exact feature or structural ambiguity has been resolved.

The next missing annotation record is a source-supported full QM6a TriliD transcript/protein model with splice boundaries, followed by a consistent model choice for A/C/E. Do not repeat genome retrieval or full-window matching to answer that question; the versioned records, exact coordinates, and protein comparisons are already retained.
