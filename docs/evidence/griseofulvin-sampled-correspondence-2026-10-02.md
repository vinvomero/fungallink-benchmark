# Parent griseofulvin sampled-member correspondence

Started 2026-10-02; completed 2026-10-03 (America/New_York). The filenames retain the start date. The final top-score uniqueness check and report corrections were performed on 2026-10-03; source retrieval dates remain those recorded in the source registry. Recommend `caesar2023:relationship:13`, `source:NRPKS_18` to feature `2854`, as **reference-supported at source-GCF resolution**, pending scientific review. This closes the missing reference-to-represented-member connection using the publisher's embedded protein sequences. It does not establish direct experimental support in the sampled culture, intact function of every annotated protein, or production by every family member. No admission ledger or authoritative count changed.

The decisive member is `FMGX0099 / scaffold_2.region001`, carrying `jgi.p_Penla1` annotations. Its thirteen corresponding reference-region proteins occur consecutively in reversed reference order. Seven match exactly over their full lengths. The remaining matches are close, but the P450 annotation is shorter and its function remains unverified. This limitation belongs in the released evidence scope; the evidence is sufficient for a transferred family-level positive without pretending the sampled locus was experimentally tested.

Requested route: `gpt-6-astra` / `medium`. No serving-side receipt was exposed; actual model and effort remain unverified. This is an automated curator recommendation under the canonical plan and benchmark contract, not scientific signoff.

## Public source chain

The original publisher archive is [Caesar Supplementary Data 1](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM3_ESM.zip), member `Supplementary Data 1/NRPKS_18.html`. Its `FMGX0099` block explicitly contains `scaffold_2.region001` and seventeen `jgi.p_Penla1_*` protein annotations. The assembly/project token therefore comes from the same public source block as the family membership, rather than a species-name inference or a private culture alias list.

Caesar Supplementary Table 2, actual PDF page 5 (printed page 4), explicitly assigns *P. lanosocoeruleum*, ATCC 48919, project `Penla1`, source JGI. This row was re-read from the retained [publisher supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM1_ESM.pdf). It supplies a documentary source assertion connecting the assembly token to the sampled culture. It does not independently authenticate a culture or make ATCC 48919 identical to experimental strain IBT 5753. JGI's indexed [Penla1 project title](https://myco-lb.jgi.doe.gov/Penla1/Penla1.home.html) agrees, although a fresh direct browser fetch returned HTTP 403. That page is corroboration, not a required dependency.

The [published feature workbook](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM4_ESM.xlsx), Sheet1 row 2862, has feature ID `2854` and name `griseofulvin`. Columns CJ, CK and CL identify ATCC48919 in header row 6, Cheerios/Oats/Rice in row 7, and the matching acquisition stems in row 8. Their feature-2854 peak heights are respectively 3,490,000,000, 3,130,000,000 and 2,890,000,000. These are nonzero source-reported measurements in the represented source culture. No new normalization, detection threshold or independent confirmation is implied, and the three conditions are not independent genomes. The earlier Type I chemistry appraisal stands. The NRRL 1786 chemistry illustration is not used as sampled-locus provenance.

The source reference block is labeled `BGC0000070.1`. The current [versioned BGC0000070.5 record](https://mibig.secondarymetabolites.org/repository/BGC0000070.5/index.html) identifies reference accession GU574478.1 and connects the protein identifiers to the annotated griseofulvin region. Current metadata supplies annotation names and reference strands, not replacement sequence input. The source's historical `.1` label is preserved. Existing primary experimental support for parent griseofulvin from Chooi 2010 and Cacho 2013 is retained from the earlier packets. Chooi's PMC page returned a browser challenge during this check; no fresh reading of its full text is claimed. Cacho's retained manuscript was available locally; its reference-pathway evidence is not a new experiment on Penla1.

## Bounded sequence comparison

Both input sequence sets were recovered from `onclick="openBlast(...)"` attributes in the original archive member, restricted to its griseofulvin reference block and the selected FMGX0099 block. No other reference block was analyzed. No genome was downloaded.

Python 3.13.5 and Biopython 1.88 `Align.PairwiseAligner` performed global protein alignment with BLOSUM62, gap opening -10 and gap extension -0.5, including terminal gaps. All 21 displayed reference proteins were scored against all 17 displayed sampled proteins. For each reference, the highest-scoring sampled sequence was aligned; the reciprocal highest score was checked against the same 21-protein reference set. The thirteen reference-region proteins below have distinct reciprocal best matches. The 2026-10-03 follow-up counted entries attaining the maximum score in both directions: each of all thirteen comparisons has exactly one top-scoring counterpart. This tests score uniqueness rather than relying on deterministic selection among ties; it does not assert uniqueness of an optimal alignment path. Flanking best scores are not treated as evidence of homology merely because an argmax exists.

Identity is identical residue pairs divided by aligned columns containing a residue in both sequences. Reference and sample coverage use that same paired-residue count divided by the respective full input length. Gap-containing columns are excluded from the identity denominator and reduce the appropriate coverage. These are protein alignment measurements, not nucleotide identity, full-region coverage, or the source's domain cutoff. The TSV preserves integer counts, total alignment columns, both lengths, unrounded percentages, scores and per-sequence SHA-256 hashes.

| Reference protein | Sampled annotation suffix | Reference/sample length | Identical/paired | Identity % | Reference/sample coverage % |
|---|---|---:|---:|---:|---:|
| GsfR2 (ADI24952.1) | 378867 | 415/415 | 415/415 | 100.000 | 100.000/100.000 |
| GsfK (ADI24951.1) | 433044 | 251/251 | 251/251 | 100.000 | 100.000/100.000 |
| GsfR1 (ADI24950.1) | 378866 | 688/744 | 688/688 | 100.000 | 100.000/92.473 |
| GsfJ (ADI24949.1) | 378865 | 554/558 | 553/553 | 100.000 | 99.819/99.104 |
| GsfI (ADI24948.1) | 378864 | 533/533 | 533/533 | 100.000 | 100.000/100.000 |
| GsfA (ADI24953.1) | 378863 | 1790/1790 | 1789/1790 | 99.944 | 100.000/100.000 |
| GsfB (ADI24954.1) | 368588 | 419/419 | 419/419 | 100.000 | 100.000/100.000 |
| GsfC (ADI24955.1) | 378861 | 396/396 | 396/396 | 100.000 | 100.000/100.000 |
| GsfD (ADI24956.1) | 378860 | 378/395 | 377/378 | 99.735 | 100.000/95.696 |
| GsfE (ADI24957.1) | 378859 | 377/377 | 377/377 | 100.000 | 100.000/100.000 |
| GsfF (ADI24958.2) | 320757 | 504/462 | 449/462 | 97.186 | 91.667/100.000 |
| GsfG (ADI24959.1) | 395808 | 299/308 | 296/296 | 100.000 | 98.997/96.104 |
| GsfH (ADI24960.1) | 320609 | 237/237 | 237/237 | 100.000 | 100.000/100.000 |

All sample IDs in the table have prefix `jgi.p_Penla1_`. The thirteen matches occupy sampled annotation ordinals 14 through 2 when followed in reference order. Their strands agree with reversal of the current reference strand annotations. The source reference SVG draws all reference arrows forward, contradicting the strand metadata for several reference records; it was not used to establish relative strand conservation. Sample SVG directions and current versioned reference strand fields were checked instead. This preserves the distinction between gene order in the historical drawing and reliable strand metadata.

GsfF is the main limitation: 449 identical pairs among 462 paired residues, from a 504-residue reference and 462-residue sampled annotation. That is 97.186% paired identity, 91.667% reference coverage and 100% sample coverage, not a full-length exact match. The records do not resolve whether the discrepancy reflects gene prediction, sequence variation or a functionally incomplete protein. GsfD and several accessory annotations also differ in length. No gene model was repaired and no functional activity was inferred from an alignment alone.

## Alternative explanations and recommendation scope

This comparison discriminates one coherent sampled griseofulvin-like locus from similarity in a single shared domain: every one of the thirteen reference-region proteins has a distinct reciprocal best match in the bounded comparison, with conserved contiguous ordering. The source reports measured parent griseofulvin in the corresponding ATCC48919 samples. Taken together with the experimental reference evidence, those observations justify reference transfer for the source GCF-to-measured-feature task. No arbitrary universal identity threshold is introduced.

The competing-locus assessment is deliberately local: 21 reference-region versus 17 sampled-region proteins, with second-best scores recorded. It does not establish that Penla1 has no additional related locus, exclude another contributor to the measured product, or establish completeness of the genome. Family membership supplies the declared query roster, while the selected member supplies the explicit correspondence anchor. Neither a genomewide absence claim nor direct causal assignment to ATCC48919 is part of this recommendation. An experimentally established reference pathway, multi-protein sampled correspondence and supported measured target meet a stronger standard than source correlation alone, despite the unresolved functional completeness of one annotation.

Retain all ten source sampled members and distinguish inserted references from sampled members. The other nine sampled loci were not compared here, so this recommendation must not become an all-member production claim or justify a narrowed single-member query without a separately declared query definition. The other inserted anchor supplies no griseofulvin evidence and was excluded. No congener relationship is upgraded. Parent griseofulvin remains one pathway group, with at most one additional reviewed source-GCF positive from this packet.

The family was selected under Caesar's exposed domain-network procedure; its cutoff 70 is not 70% full-length identity. The alignment does not make this a blind or unfamiliar-pathway benchmark. Method-input readiness still requires the declared roster, sample crosswalk and full 9,339-feature candidate pool in the frozen release. Spectral joins remain a separate input requirement. Unresolved candidates remain unlabeled.

## Repeatability and verification

To repeat the calculation, read only the two named blocks from the archive member, extract protein IDs and their embedded amino-acid strings, and apply the alignment specification above to the 21-by-17 comparison. Retain the thirteen reference IDs listed in the TSV, verify distinct reciprocal matches and their reversed contiguous sample ordinals, then recompute the integer identity/coverage counts and sequence hashes. The selected strings, calculation scripts and verification JSON, including `top-score-uniqueness-2026-10-03.json`, are ignored scratch under `data/interim/griseofulvin-sampled-correspondence/`; the public archive and saved numerical ledger are the portable evidence dependencies. This is evidence-analysis code, with no engineering or production instructions.

The first numerical attempt hit an OpenBLAS allocation error; rerunning with `OPENBLAS_NUM_THREADS=1` completed. Verification confirmed thirteen unique reference IDs, thirteen unique sampled IDs, seven exact full-length matches, reciprocal matches, reversed contiguous ordering and strand agreement against the stated metadata. The source-association inventory has exactly the griseofulvin/2854/NRPKS_18 relationship key used here; the workbook row and culture columns were checked directly. No fresh wet-lab evidence, external review or admission approval is claimed.

| Artifact | SHA-256 |
|---|---|
| Publisher ZIP | `0cef389310eccd261255e51919e7fe5f1f772cc73be2b0d42e0f5f8e30245a54` |
| Original NRPKS_18 archive member | `c662bd2e7da63410bc1ea06a6613b9a393b1894f41880dbcf5bbf16f981efc03` |
| Publisher supplement | `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108` |
| Publisher workbook | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |
| Accompanying 13-row TSV | `21f57b625ca15720e48637092e553c83e2fd9c27431b2a308b96eed586d6d39b` |

Earlier evidence packets remain historical records of the previously open gap. This packet supplies new sampled correspondence; scientific review should assess the stated transfer scope and shorter annotation before adopting the recommendation.

