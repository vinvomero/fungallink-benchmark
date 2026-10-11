# HEx measured-data supplement inventory

Screen date: 2026-10-07. Study: Harvey et al., 2018, DOI [10.1126/sciadv.aar5459](https://doi.org/10.1126/sciadv.aar5459), PMC5895447. This bounded source review supports the canonical benchmark plan; it makes no label admissions.

The HEx supplements are publicly retrievable through the [BioStudies institutional API](https://www.ebi.ac.uk/biostudies/api/v1/studies/S-EPMC5895447). Earlier browser failures did not establish that the files were unavailable. All four files listed by that API were retrieved successfully. They provide locus and expression-strain metadata, plasmid sequences, selected LC-MS chromatograms, and compound characterization. No complete numeric measured-feature matrix, stable feature-ID table, acquisition crosswalk, or feature-to-MS/MS export was found in this deposit.

HEx therefore remains a source of experimental pathway-product evidence with unresolved method-input readiness. It is not ready as a native-fungal co-occurrence cohort. These measurements come from engineered Saccharomyces cerevisiae hosts, not the native fungi whose genomes supplied the loci.

## Recovered files

Files are retained under `data/raw/hex-measured-data-screen-2026-10-07/`. `provenance.tsv` records URLs, byte counts, and SHA-256 hashes; `retrievals.jsonl` retains the successful HTTP receipts. The prior article XML and text in `data/raw/expression-dataset-screen-2026-10-07/` were reused, not fetched again.

| File | Bytes | Inspected content |
|---|---:|---|
| aar5459_SM.pdf | 12,002,579 | 72-page supplement: text, figures S1-S6 and S8-S79, tables S1-S21 |
| aar5459_FigS7.pdf | 189,533 | One-page PKS phylogenetic tree; not measured metabolomics data |
| aar5459_DatafileS1.zip | 534,336 | One GenBank file, 2,060,980 uncompressed bytes, containing 78 LOCUS records; engineered plasmids and related constructs |
| supp_4_4_eaar5459__index.html | 10,733 | Publisher supplement index preserved by Europe PMC/BioStudies; lists the same three content files |

The 78 records are not independent fungal genomes or supported queries. No bulk spectra or genomes were downloaded. Source files remain private project inputs; public accessibility alone does not settle redistribution rights.

The host separately checked the four retrieved file sizes and hashes, the single GenBank ZIP member, 78 unique LOCUS records, and 72 main-PDF pages. Its receipt is `data/raw/hex-measured-data-screen-2026-10-07/host-verification.json`. This verifies the retrieved inventory, not biological sequence correspondence or label validity.

## What can be joined

Table S8, PDF pages 22-23, maps PKS1-PKS28 and TC1-TC13 to native accession strings, coordinates, and engineered plasmid names. PKS3's native accession is printed as deposition pending. Accession versions and coordinate conventions still need verification before sequence-defined query construction.

Table S10, PDF pages 26-29, maps expression strain numbers to host background, cluster, and plasmid names. Table S9 contains annotation abbreviations, despite the main methods' reference to S9 for production strains. The main article Table 1 includes DHZ and IDT controls; its 43 total and 24 productive entries differ in scope from the abstract's 41 cryptic clusters and 22 producing detectable compounds. Neither pair is an admitted-query count.

Figures S8-S24, PDF pages 30-39, identify 17 PKS expression-strain comparisons. Their exact cluster, strain, figure, and page locators are retained in the companion TSV. Figure S8, visually inspected, shows PKS1 from Coniothyrium sporulosum in strain 132 against control 137, with mode-specific EIC panels such as ESI+ m/z 455.1813, 422.1792, and 421.1759. Table S8 links PKS1 to KV441552, coordinates 530394-546723. This is a traceable published experimental connection, but the plotted masses and retention axes are not stable feature identifiers or an acquisition join. They also do not establish that every panel is a different compound.

Table S5, PDF page 20, lists ten ion masses/formulas used to integrate sesquiterpenoid titers for Fig. 2B. It is a selected ion list, not a feature-by-sample matrix. Tables S11-S21 and NMR figures characterize compounds 6-16; compound numbers and structures cannot substitute for a measured-feature candidate universe.

## Candidate universe and gaps

The supplement, pages 9-10, describes several thousand XCMS features, followed by manual inspection of high-ranking signals. It gives no exact full candidate count or roster. The main methods say top 100 features by fold change and P value; the supplement says top 50 hits when sorted by both. These descriptions need reconciliation if reconstructing the source's selection procedure. Selected chromatograms cannot define an unbiased full ranking pool.

The expression experiment offers perturbational evidence: features were assessed in production strains against empty-vector controls, with three biological replicates. Unresolved or undetected products are not negative biochemical labels. Native fungal presence/absence vectors cannot be inferred from these engineered yeast measurements, and replicate cultures do not add independent fungal genomes.

Several sequence joins also need attention. Visual checks of S8 and S10 confirmed PKS1/PKS2 plasmids ending in `-2.2` in S8 and the archive but `-2.1` in S10. S8 names `pCHKU42.3-2.2` for PKS16, absent from the archive LOCUS list. S8 names `pCHKU62.3-2.2` for PKS18, while S10 lists no third plasmid and the archive has no matching LOCUS record. S10 repeats the second plasmid in the PKS8 diploid row. These are source inconsistencies, not corrections made by this screen.

Admission and input readiness remain separate:

- Biological evidence: experimental heterologous expression and selected chemical characterization are available; individual relationships still need adjudication at their supported chemical resolution.
- Feature-only ranking inputs: unresolved. Required are the full feature roster, numeric abundance/presence matrix, samples and controls, preprocessing provenance, and positive-to-feature joins.
- Spectral inputs: unresolved. No exported MS/MS records and validated feature-spectrum membership were found in the inspected deposit.
- Native co-occurrence compatibility: not supplied by this study design. An expression-host comparison would require an explicitly declared task and suitable methods, not silent pooling with native cohorts.

Stop this source screen here. Reopen HEx input acquisition if an existing processed XCMS export or deposited raw-data manifest is located, with stable sample identities and a route from the published EICs to released features. A full source-faithful reconstruction would need its own authorized work unit. No correspondence, experiments, engineering, or benchmark admissions occurred.

Requested route: `gpt-6-astra`, reasoning `medium`. This subagent dispatch was accepted under that requested route; no serving-side receipt is exposed, so actual serving model/effort is unverified. Humanizer rules were applied; its referenced extended guide is absent from the installed skill directory. PDF reading used the PDF skill, text extraction, and visual checks of the relevant join tables and example chromatogram.
