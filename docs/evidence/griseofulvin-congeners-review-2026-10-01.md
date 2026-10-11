# Griseofulvin congener evidence appraisal

Reviewed 2026-10-01. All three relationships remain provisional and outside headline evaluation. This bounded source review admits no biological labels and supplies no human signoff. It keeps the source's strong chemical calls separate from exact-product pathway evidence and sampled-family correspondence.

## Source feature checks

[Caesar et al. (2023)](https://doi.org/10.1038/s41589-023-01276-8), Supplementary Table 4, PDF page 10 (printed 9), assigns these relationships to `NRPKS_18`, reference `BGC0000070`, at cutoff 70. The workbook is `data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx`, `Sheet1`; its headers are on Excel row 8. Each source feature ID occurs exactly once and its stored name agrees exactly with the source table.

| Relationship | Source product spelling | Feature ID | Excel row | m/z | Retention time |
|---|---|---|---|---|---|
| 9 | 6-O-desmethyldechlorogriseofulvin | 6346 | 6354 | 305.1035735 | 2.225560154 |
| 10 | 6-O-desmethylgriseofulvin | 2824 | 2832 | 339.0605193 | 3.52319058 |
| 12 | epidechlorgriseofulvin | 208 | 216 | 319.1190331 | 3.042472022 |

The join is by ID, with name agreement as a check. Mass and retention time did not determine the join. The source's expression counts are respectively 1/10, 3/10, and 6/10; these describe associations within its family and do not count independent pathways.

Supplementary Figure 1, PDF page 21 (printed 20), was inspected visually. It contains a named Type I panel for each of the three products. The caption on PDF page 20 (printed 19) defines Types I and II as in-house authenticated-standard comparisons using MS2 patterns, retention time, m/z, and/or UV spectra, with high confidence. The caption does not say that every modality was used for every compound. These observations verify the reported evidence route and presence of product-specific panels; they are not independent spectrum interpretation, stereochemical adjudication, or a feature-to-native-scan join.

## Product-specific published evidence

For 6-O-desmethyldechlorogriseofulvin, [Shang et al. (2012), DOI 10.1002/cbdv.201100216](https://research-repository.uwa.edu.au/en/publications/diverse-secondary-metabolites-produced-by-marine-derived-fungus-n/), reports isolation of this exact named compound from *Nigrospora* sp. MA75, spectroscopic structure elucidation, and CD-based absolute-configuration evidence. The abstract was checked through the authors' institutional record and PubMed search result, PMID 22782879. This supports published occurrence and chemical identity, not a BGC assignment in the Caesar cohort.

For 6-O-desmethylgriseofulvin, [Ronnest et al. (2010), DOI 10.1016/j.tetlet.2010.08.095](https://backend.orbit.dtu.dk/ws/files/52202819/978_87_91494_00_0_Mads_Holger_R_nnest.pdf), reports single-crystal X-ray confirmation of this named structure. [The 2023 primary isolation paper, DOI 10.3390/ijms242316568](https://pmc.ncbi.nlm.nih.gov/articles/PMC10706121/), identifies its compound 9 by HRESIMS/NMR comparison in a fungal co-culture. These are compound-specific chemical observations. Neither establishes which sampled Caesar locus produced feature 2824; a co-culture occurrence alone cannot resolve organism or locus provenance.

[Cacho et al. (2013), DOI 10.1021/cb400541z](https://stacks.cdc.gov/view/cdc/29769/cdc_29769_DS1.pdf), reports experimental pathway evidence for compounds called desmethyl-dechlorogriseofulvin (13) and desmethylgriseofulvin (15) in the *P. aethiopicum* reference pathway. Scheme 1, author-manuscript PDF page 13, and Figure 4, page 19, were visually checked. The drawings in Scheme 1 appear to place the free aromatic OH differently from the two 6-O panels in Caesar Figure 1. A scientific structure/numbering crosswalk is therefore unresolved. The shared shortened names and matching nominal masses do not justify transferring this experimental evidence to the two exact 6-O targets. This is a recorded mapping concern, not a definitive correction to either paper.

For source-spelled epidechlorgriseofulvin, literature uses epidechlorogriseofulvin. [Jarvis et al. (1996), DOI 10.1021/np960395t](https://stacks.cdc.gov/view/cdc/205803/cdc_205803_DS1.pdf), identifies epidechlorogriseofulvin as compound 2b and reports X-ray-based stereochemical characterization on page 554. Only the target compound's chemical evidence is used here. This establishes an independently published epimer identity, not its reference-pathway assignment or the spelling/structure crosswalk for feature 208.

[MIBiG BGC0000070.5](https://mibig.secondarymetabolites.org/repository/BGC0000070.5/index.html), inspected 2026-10-01, lists epidechlorogriseofulvin and cites the 2010 and 2013 reference papers. Its quality field is `questionable`. However, [Chooi et al. (2010), PMID 20534346](https://pubmed.ncbi.nlm.nih.gov/20534346/), calls the relevant reference congener dechlorogriseofulvin in the abstract, and Cacho's main text calls its compound 2 dechlorogriseofulvin. Those names do not establish the epi stereoisomer. Reconciliation requires the primary structural evidence and compound numbering, rather than reliance on the database product list. The source table's unversioned reference ID remains unchanged; version .5 is the later record inspected for this review.

## Disposition and reopening criteria

For relationship 9, reopen with a reviewed mapping of the exact 6-O-dechloro structure to congener-specific experimental pathway evidence, then a reviewed correspondence to a sampled `NRPKS_18` member. The Shang isolation report alone does not fill either connection.

For relationship 10, resolve the 6-O substitution pattern against the reference experimental compounds, then establish the sampled-member connection. Parent griseofulvin evidence and exact-mass agreement cannot settle this positional-isomer question.

For relationship 12, reconcile the source spelling and drawn stereoisomer with the MIBiG entry and cited primary compound identities; document experimental support for the exact epi product and its sampled-family correspondence. Occurrence of the epimer in another fungus does not establish that connection.

For every row, sampled-locus identity/coverage, relevant gene content and organization, and competing-locus review remain unestablished in this packet. No missing connection is converted into a negative label. Propose grouping all three with parent griseofulvin under one shared griseofulvin pathway group for dependence control. This is a grouping proposal, not a finalized count of independent eligible queries.

Historical feature-abundance input is present. Release readiness still requires the family roster, sample/genome crosswalk, and declared candidate universe; historical feature-to-MS/MS scan membership remains unresolved. Source-selected associations and known reference/product identities constitute prior exposure. No method version or new model result is introduced here.

## Provenance and limits

Workbook SHA-256: `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb`. Supplement `data/raw/sources/metadata/caesar-supplement-cdn` SHA-256: `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108`. Local review images and the Cacho author manuscript are ignored scratch files in `data/interim/griseofulvin-congeners/`; Caesar's rendered page is also available in `data/interim/host-therapeutic-review/page-21.png`.

This was one source review and one focused literature/structure resolution attempt. The unresolved cases receive specific reopening criteria above rather than an open-ended search. No source chemical tier was downgraded. No biological admission, scientific signoff, independent validation, or final pathway count is claimed. Requested route: `gpt-6-astra` / `medium`; the task was dispatched on that route, but no serving-side model/effort receipt was available to this worker.
