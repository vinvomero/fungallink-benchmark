# Emericellamide A competing-locus review

Checked 2 October 2026. Automated evidence review only; no scientific sign-off or formal admission. Requested route: `gpt-6-astra / medium`. No serving-side model/effort receipt is available.

Each of the five retained reference protein sequences has exactly one full-length exact match among all 10,534 proteins in the public GenBank annotation for *Aspergillus nidulans* FGSC A4, assembly GCA_000011425.1 (ASM1142v1). All five matches belong to the previously identified BN001307.1 locus. There is no second annotated copy of the exact reference cassette in this annotation.

This resolves duplicate exact-reference ambiguity for the source locus. It does not establish that a diverged or unannotated locus cannot produce emericellamide A. The broader competing-locus requirement in [the benchmark contract](../../protocol/benchmark-contract.md) remains open unless the researcher records why this source-specific ambiguity check is sufficient for the proposed transferred association. That decision must precede cross-case use; this review does not change the protocol.

The proposed association remains emericellamide A, feature 8468, HRPKS_71 / FMGX0049, ATCC 38163. The retained [case packet](emericellamide-a.md) supplies the strain alias, published chemistry, measured-feature join and the experimentally supported reference. This check adds no chemical evidence and makes no claim for emericellamide B. The five reference records include a dispensable hypothetical protein; they are not five experimentally necessary genes.

## What was checked

The starting input was [first-three-source-checks.json](first-three-source-checks.json), SHA-256 `e060f9e87191f6a1772bd18c07fb482f27f6c90bed18c997f401938c94200faf`. Its five full-length reference sequence hashes were already tied to source HTML and MIBiG BGC0001290.4. That comparison was not rerun. For provenance, the retained MIBiG GenBank hash is `ae461b418993f199272cb911cf56605642b161580fa7b13315dabf7fa093727b`, and the source HRPKS_71 HTML hash is `dbf05efdc8d60c2393af056814e63862abc7fa767aa8134e1845a1e50681ccf8`.

The new search used the complete released protein FASTA and feature table from the NCBI assembly directory. Python 3.13.5 decompressed the FASTA, split records at the FASTA header marker, retained each accession, concatenated its sequence lines without headers or line breaks, and calculated SHA-256 over the resulting case-preserved sequence string. Every record was compared with the five retained hashes. No alignment cutoff, substring match, similarity threshold or product-name filter was used. Equality of full-sequence hashes is the exact-identity test; no sequence content is included in this report.

The FASTA contains 10,534 records with 10,534 distinct protein accessions. Its accession set exactly equals the feature table's 10,534 `CDS / with_protein` accessions. These cover all eight assembly chromosomes. The table contains another 63 CDS records without a corresponding protein in this released FASTA; those records were not searched as translated sequences. This is complete coverage of the released protein annotation, not of every possible coding sequence in the genome.

| Reference protein | Length, aa | Exact matches | Matched locus tag |
|---|---:|---:|---|
| CBF87069.1 | 6,919 | 1 | ANIA_02545 |
| CBF87071.1 | 164 | 1 | ANIA_02546 |
| CBF87072.1 | 2,534 | 1 | ANIA_02547 |
| CBF87074.1 | 479 | 1 | ANIA_02548 |
| CBF87076.1 | 565 | 1 | ANIA_02549 |

All hits map to chromosome VII, BN001307.1, at the reference locus already recorded in the case packet. This independently confirms the annotation location of each exact match. Historical region numbers remain annotation-specific: the case packet's source region009 and retained antiSMASH 8.0.4 region011 denote the same mapped locus, whereas the successor region009 is a different locus. The new check does not depend on either region number.

## Source and artifact receipts

Files were retrieved from NCBI on 2026-10-02, at approximately 22:57 UTC. The assembly report identifies Eurofungbase as submitter, FGSC A4 as strain, SAMEA2272224 as BioSample, and a full chromosome-level assembly released 2009-09-24. It reports GCA_000011425.1 and GCF_000011425.1 as identical assemblies. This search uses GenBank proteins only; the RefSeq synonym is not an extra genome or an independently searched annotation.

| Retrieved file | Bytes | SHA-256 | HTTP Last-Modified |
|---|---:|---|---|
| [GCA_000011425.1_ASM1142v1_protein.faa.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/011/425/GCA_000011425.1_ASM1142v1/GCA_000011425.1_ASM1142v1_protein.faa.gz) | 3318621 | `64dbd3f5111fd57e4aa947035877a32b6d65fcaea08f4c865851bea4fa7779fc` | Thu, 16 Jun 2016 07:33:20 GMT |
| [GCA_000011425.1_ASM1142v1_feature_table.txt.gz](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/011/425/GCA_000011425.1_ASM1142v1/GCA_000011425.1_ASM1142v1_feature_table.txt.gz) | 612030 | `4e1e14cc4d3caa364f83e6e606698e8631da7db9848badcf226a7778999c03fc` | Sun, 24 Dec 2017 03:36:49 GMT |
| [GCA_000011425.1_ASM1142v1_assembly_report.txt](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/011/425/GCA_000011425.1_ASM1142v1/GCA_000011425.1_ASM1142v1_assembly_report.txt) | 1832 | `f0e37b0314b237c450f74d2a5a3e3b6c556709102b870134c5686ad094c84943` | Sat, 19 Oct 2024 03:25:31 GMT |
| [md5checksums.txt](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/011/425/GCA_000011425.1_ASM1142v1/md5checksums.txt) | 1263 | `10666a6b292069bebe391f2c74ea4d71251cb5f7ae7c34ddb534cc973f6d1d2c` | Thu, 19 Jun 2025 05:14:38 GMT |
| [annotation_hashes.txt](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/011/425/GCA_000011425.1_ASM1142v1/annotation_hashes.txt) | 410 | `99beb1f6ebc51fb9a8b4e919a300d8e719c32741e053c9649f31d29a5dd98505` | Thu, 19 Jun 2025 05:14:38 GMT |

The protein FASTA, feature table and assembly report each pass the downloaded NCBI MD5 manifest. The manifest itself is retained and hashed; its authenticity was not independently signed. The annotation hash record reports features last changed 2015-03-04, locations last changed 2014-11-05, and protein names last changed 2016-06-16. File timestamps differ from these annotation dates and are retained separately. Reuse context: publicly downloadable NCBI/INSDC assembly data; this check does not assign a new license or authorize public deposition.

The [five-row result table](../../data/curated/emericellamide-competing-locus-review-2026-10-02.tsv) retains per-reference hashes and all exact-match counts. Its SHA-256 is `04b8a086f38d1011d76f635e1691a660acdc57df811ec04feecedc5ae5789c11`. Downloaded payloads, HTTP/source receipts and the count/metadata checks are retained in ignored `data/interim/emericellamide-competitor-review/`; no new reusable analysis code was added. A rerun needs only the versioned files above, their verified hashes, the prior five reference hashes, and the stated parsing/comparison procedure.

The exact remaining dependency is a recorded biology-review criterion for competing loci in this reference-supported case. If it requires detection of diverged alternatives, a separately scoped homology and organization assessment is still needed under criteria chosen before interpreting those alternatives. The present result cannot supply that conclusion. Chemical-resolution review, GCF roster readiness and native-spectrum membership remain separate decisions documented in the case packet.
