# Acetylaszonalenin corrected-core correspondence

Reviewed 3 October 2026 under the [canonical plan](../plans/2026-09-30-2052-benchmark-paper-plan.md) and [benchmark contract](../../protocol/benchmark-contract.md). Recommend ordinary **reference-supported** review for `caesar2023:corrected:5`, the named ana core linked to feature 2127. The reference-coordinate gap is closed: the old published interval, current scaffold interval and versioned MIBiG core are exactly equal across 12,765 nucleotides. This is a decision-ready recommendation, not admission or scientific signoff.

Requested route: `gpt-6-astra / medium`; no serving-side receipt was exposed, so actual model and effort remain unverified. Humanizer rules were applied. The original relationship key is `caesar2023:relationship:5`. No extra query, pathway group or accepted label is created by these checks.

The [2 October product-evidence review](exact-product-gap-resolution-2026-10-02.md) supersedes the earlier missing-core-product objection: Gao 2012 plus Yin 2009 supports the biochemical reference chain. The present work addresses correspondence, not another demand for a native perturbation experiment. MIBiG still labels entry quality questionable and completeness unknown; the recommendation rests on the inspected primary evidence chain plus this correspondence check, rather than treating the database label as experimental proof.

## What now matches

Downloaded only the two bounded NCBI intervals and the versioned MIBiG GenBank record. [AAKE03000024.1:130585–143349](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=AAKE03000024.1&seq_start=130585&seq_stop=143349&rettype=gbwithparts&retmode=text) and [DS027698.1:2428387–2441151](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=DS027698.1&seq_start=2428387&seq_stop=2441151&rettype=gbwithparts&retmode=text) both contain 12,765 nt. Full strings match, as does the corresponding core extracted from [BGC0000293.3](https://mibig.secondarymetabolites.org/repository/BGC0000293.3/BGC0000293.gbk). There are 12,765 identical positions out of 12,765 compared positions, with 100% coverage of both bounded intervals. The coordinate offset is +2,297,802; this crosswalk applies to this interval only.

All accession coordinates below are one-based inclusive. Python slices were zero-based half-open. MIBiG's downloaded 47,132-nt record includes flanks; its core is the slice `[20000:32765]`, not the whole record. The core nucleotide SHA-256, computed over uppercase bases without whitespace, is `b95028df97bdb6aabec9b37c7640a8834c9409841765481496e42f33587f1da6`.

| Gene | Protein accession | DS027698.1 CDS span | Strand | Equal residues / compared residues | Reference and sampled coverage |
|---|---|---|---|---|---|
| NFIA_055290 | EAW16180.1 | 2428387–2435518 | − | 2359 / 2359 | 100% / 100% |
| NFIA_055300 | EAW16181.1 | 2437444–2438808 | + | 437 / 437 | 100% / 100% |
| NFIA_055310 | EAW16182.1 | 2439622–2441151 | + | 509 / 509 | 100% / 100% |

Gene order, orientation and CDS coordinates agree after translating MIBiG's local coordinates. Full annotated protein strings match at 100% identity. Independently extracting and translating each sampled CDS reproduces its annotated protein. The old bounded record contains no CDS annotations; its exact nucleotide identity supports the coordinate crosswalk, not an independently annotated protein comparison. MIBiG and DS027698.1 share the underlying GenBank annotation. These checks establish record consistency and locus identity, not independent resequencing of the Caesar stock.

No local alignment or similarity cutoff was used. Python 3.13.5 and Biopython 1.88 performed whole-string equality, positional match counts and CDS retranslation. Equality and positional checks agreed. Each percentage uses the full sequence length shown in the table; stop codons are excluded from protein lengths. The [companion TSV](../../data/curated/acetylaszonalenin-sampled-correspondence-2026-10-03.tsv) retains every denominator and protein checksum. Its three rows describe one relationship.

## Strain, assembly and measurement chain

The freshly retrieved [ATCC 1020 record](https://www.atcc.org/products/1020) lists NRRL 181 and CBS 544.65 together. Caesar's source mapping assigns the CBS 544.65 acquisitions to GCA_000149645.3. The version-specific [NCBI assembly report](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/149/645/GCA_000149645.3_ASM14964v3/GCA_000149645.3_ASM14964v3_assembly_report.txt) names strain NRRL 181, assembly ASM14964v3, BioSample SAMN02953637 and scaffold DS027698.1. Its RefSeq counterpart is GCF_000149645.2, with the report asserting identical GenBank and RefSeq assemblies. No accession update or culture substitution is made here.

The report, retrieved 2026-10-03, also states `Excluded from RefSeq: contaminated` and `Assembly anomaly: contaminated`. Its assembly date is 2006-12-14; that date does not establish when either flag was added. The old contig record describes removals in September 2010 and suppression of 214 sequences in June 2022. Neither retrieved bounded record nor assembly report identifies this core as the contaminated sequence. Locus-specific contamination status is therefore unknown. The flag prevents a clean-assembly claim; it does not erase the observed nucleotide equality. Reviewer acceptance of this versioned locus despite that assembly-level flag remains explicit.

These collection and source joins support a reference transfer to the named sampled strain. They do not authenticate the experimental stock or show that a modern assembly was sequenced from Caesar's culture.

The [existing source receipt](first-three-source-checks.json) pins the Tier I feature 2127 to Sheet1 row 2135: EI, EJ and EK are the CBS544_65 Cheerios, Oats and Rice acquisitions. Peak heights are 1,130,000,000; 639,000,000; and 1,130,000,000, respectively, at source m/z 416.2000372 and retention time 3.664442544 min. This check reuses that documented workbook inspection, not a new chemical adjudication. Three conditions remain one strain and one proposed pathway association. The canonical sample crosswalk still carries pending biological-sample review flags; this packet does not rewrite them.

## Scope of the recommendation

Retain the three-gene named core as the BGC query. The historical wrong DMAT_34 region at DS027698.1:778075–809148 is disjoint from the corrected interval. This is the concrete competing-assignment check supported here. The retained antiSMASH 8.0.4 region004 context encloses the core but also contains a neighboring terpene component; its broader boundaries and historical family 20 are not equivalent to this named core. Neither DMAT_34 nor a new core GCF roster is admitted.

No assembly-wide alternative-locus search was performed. Exact identity to the characterized reference, the collection-strain correspondence, and source chemistry support the proposed reference association without claiming exclusive biosynthesis. The reviewer should decide whether rejection of the known wrong region is sufficient competing-locus assessment for this narrow transfer, and record that criterion before using it across cases. If exhaustive or broader alternative-locus checks are required, that specific requirement remains open. No claim of all-member production, genomic absence or unique product origin follows from this packet.

The decision can therefore be recorded as: accept the coordinate and annotation correspondence; consider ordinary reference-supported admission of the corrected named-core BGC to historical feature 2127, conditional on scientific acceptance of the scoped ambiguity check and assembly-quality caveat. No special partially characterized pathway class is needed for the superseded product-chain gap. Keep reference evidence, biological eligibility and method readiness separate: candidate/sample release freezing and a portable query package remain input work; native feature-to-scan membership remains unresolved and blocks spectral use only. Public labels, MIBiG and earlier correction work make this exposed retrospective material.

## Verification custody

Scratch files are in `data/interim/acetylaszonalenin-sampled-correspondence/`: `source_manifest.json` records URLs, retrieval date, byte counts and hashes; `verify.py` reproduces comparisons; `verification.json` and `protein_comparison.tsv` hold numerical results. Scratch retention is local, not a release dependency. Source reuse terms still apply. No raw sequences are reproduced in this packet.

| Retrieved file | SHA-256 |
|---|---|
| old_core.gbk | `2070d1e28049c08051f4b29803f9018544eca34f2f4a56dace47a5b9d584ad72` |
| sampled_core.gbk | `8c16a36258f4a56a51988d45487bfe0e17ff8fce436614631150a2d90dd08810` |
| mibig.gbk | `d7a1c8ecac30c09c24d7712fc47156e652ffcb26fe82c504c99d8ba50cdcf91b` |
| assembly_report.txt | `dc8c1808cbb7696b3df8b0bc8317d80c0dc522a9cc13489c0eea647c5d65e2a8` |
| atcc.html | `db0e15036f5e08239285ada879cc82360e9b9ff913316753fb867de1b1ac6363` |

The scratch numerical table SHA-256 is `a6bc49999748d7e019fbd86d2216cd1c50ba3a61adc55c36944b78c4501f3bc7`. Failed preliminary access through the web renderer did not supply evidence: ATCC was retrieved through a direct HTTP request; an initial incorrectly named ASM14964v1 assembly-report URL returned 404, after which the FTP listing supplied the correct ASM14964v3 path. A dataset-report endpoint returned an empty JSON object and was not used. The cited version-specific report and bounded records are the evidence actually inspected.
