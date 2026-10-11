# 6-MSA-associated measured product: expression-locus admission

Admit one directly supported historical relationship under Vin Vomero's delegated curator authority. The query is the deposited expression CDS `JBXSGV010000118.1:86-5497|expressed-cds-v1`, including its stop codon, in assembly GCA_060307435.1. The target is the 6-MSA-associated measured product in Supplementary Figure 5A of [Gadar-Lopez et al.](https://doi.org/10.1038/s41589-026-02282-2). Curated identifier `suppfig5:A:6MSA-associated-product` denotes that source panel, not a native feature ID.

## Experimental and chemical scope

The published supplement shows the producing S. cerevisiae POP4 sample against its control, with a named 6-MSA signal and fragmentation panel. Its caption describes consistency with prior fragmentation analysis. Table 10 lists the expressed atX6MSA construct for strain sYNP14092. The measurement workbook MOESM8, sheet `Sup_5A`, names acquisition `20231206_Ac-C18_NEG_UMETAB420_14092_EXT_SC_6MSA_C2.mzML` in A2. Figure 5A was visually inspected on PDF page 9, printed page 8.

This admission concerns a measured product with a putative 6-methylsalicylic acid name. It does not claim an authenticated-standard comparison, NMR confirmation, exact-structure gold, native A. terreus production or pathway sufficiency outside the expression host. The support applies to this expression locus and sampled context. Do not turn the four host panels or replicate assemblies into four new pathways.

## Specimen and sequence bridge

BioSample SAMN57313188 explicitly records sample name `sYNP14092_SC-POP4-6MSA-14092`; its strain matches Table 10. The BioProject listing and the independently retrieved NCBI assembly report join it to GCA_060307435.1, WGS JBXSGV01. The complete retained FASTA contains 182 scaffolds and 11,535,592 bases, agreeing with the assembly report.

The cited reference is MIBiG BGC0001276; version 3 carries protein BAA20102.2. Exact six-frame containment found no full-length identical protein. A diagnostic scan of 18 spaced 20-residue anchors placed all 18 at one consistent offset on JBXSGV010000118.1. Direct translation of the resulting 1,803-residue interval differs at one position: reference S1332, assembly F1332. The interval begins with ATG and is followed by TGA. Preserve this difference; it is not an exact reference match and has not been functionally interpreted.

The admitted query is the observed deposited CDS, not a homology transfer that silently substitutes the reference sequence. Experimental support comes from the source's expression/measurement evidence. No whole-genome uniqueness claim follows from the bounded scans, and host contributions remain possible. MIBiG's questionable-quality/unknown-completeness flags prevent treating its annotation alone as validation.

## Readiness and audit

The MassIVE inventory has one raw file with the acquisition's exact stem in its Supplementary Figure 5 directory. The raw/mzML conversion and native scan join are not independently verified. No complete all-feature candidate pool is available, and no scoring or spectral readiness is activated.

Retained evidence is in `data/interim/black-yeast-screen-2026-10-09/`: `biosamples.xml`, `biosample-aliases.json`, `bioproject-assembly-map.json`, `sixmsa-assembly-report.json`, the compressed assembly, `BGC0001276.3.gbk`, sequence-check scripts and three scan receipts, `figure5.png`, source workbooks, `acquisition-locators.json` and `retrievals.jsonl`. `sixmsa-admission-integrity.json` records ledger preservation and query hashes.

A separate Table 10 accession conflict affects sYNP19203: the supplement assigns JBXVTA000000000, whereas the project assigns JBXSGS000000000. That disputed row is not used for this admission. The monacolin J gaps remain unresolved.

Counts become 28 relationships / 16 query identities, with 18 directly supported and ten reference-supported. Evaluated coverage stays eleven. The current manuscript remains the historical 27-label version until explicitly integrated. Reopen for contradictory source evidence, changed deposited sequence, a failed specimen alias, or new evidence altering the chemical resolution. Assistant-curated judgment is not independent human validation.
