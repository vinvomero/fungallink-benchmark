# Eight remaining reference appraisals

Review begun 2026-10-01 and resumed 2026-10-02 after interruption. The filename preserves the assigned work-unit date. Source panels and the initial literature checks were inspected on 2026-10-01; workbook values, archive identifier counts and final citation checks were completed on 2026-10-02. Requested route: gpt-6-astra, medium reasoning. No serving-side receipt is available to verify the actual model or effort.

These are proposals for eight existing Caesar relationships, not admissions or scientific signoff. All remain provisional at the present source-GCF-to-exact-product scope. Published reference evidence is stronger for some cases than others; unfinished correspondence checks must not be described as an absence of published experiments. No independent pathway count is assigned. The three notoamide rows share one source family, and emericellamide B shares its family with the separately reviewed A.

## Records checked

The review follows the canonical `docs/plans/2026-09-30-2052-benchmark-paper-plan.md`. It uses `research_audit/source-inventory.json`, the original Caesar workbook and GCF ZIP, and the actual supplementary PDF held as the extensionless `data/raw/sources/metadata/caesar-supplement-cdn`. Their registered SHA-256 values are respectively:

- Workbook: `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb`.
- GCF ZIP: `0cef389310eccd261255e51919e7fe5f1f772cc73be2b0d42e0f5f8e30245a54`.
- Supplementary PDF: `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108`.

The workbook was read directly, matching identifiers across Sheet1 rather than assuming row offsets. Each requested identifier occurred once. These are historical measured targets; the numerical values do not establish a native-scan join or independently identify a compound.

| Feature | Exact workbook name | Excel row | m/z | RT, min |
| --- | --- | --- | --- | --- |
| 1701 | tryprostatin b | 1709 | 352.2014287 | 3.270614798 |
| 5402 | emericellamide B | 5410 | 652.4700284 | 5.595361836 |
| 128 | mycophenolic acid | 136 | 321.1340594 | 3.344826098 |
| 1673 | notoamide A | 1681 | 464.2167731 | 3.500740183 |
| 9213 | notoamide | 9221 | 448.2228017 | 3.446772474 |
| 4182 | notoamide E4 | 4190 | 434.2405295 | 4.089944518 |
| 1764 | fellutamide B | 1772 | 556.3738629 | 3.605707407 |
| 1761 | terrequinone A | 1769 | 491.2371248 | 5.607095726 |

The [Caesar supplement](https://doi.org/10.1038/s41589-023-01276-8), physical PDF page 20 (printed 19), defines Types I and II as high-confidence authenticated-standard routes from different in-house databases. Type III uses public experimental GNPS spectra; Type IV is putative in silico matching. Fresh renders of pages 22–26 were visually inspected. The report retains the word Type for these chemical routes, distinct from biological evidence classes.

Archive inspection was limited to family and strain identifiers. In `Supplementary Data 1/<family>.html`, the distinct FMGX identifiers and versioned references give source-family membership provenance, not a new homology analysis. Counts below are archive identifiers, not admitted loci or independent queries.

| Source family | Versioned references present | Distinct archive FMGX IDs | Table-reported strains | Result |
| --- | --- | --- | --- | --- |
| DMAT_33 | BGC0000356.1 | 2 | 2 | Counts agree |
| HRPKS_71 | BGC0001290.1 | 19 | 19 | Counts agree |
| NRPKS_41 | BGC0000104.1; BGC0001360.1; BGC0001677.1 | 2 | 2 | Counts agree; table cites BGC0001677 |
| NRPS_66 | BGC0000818.1; BGC0001084.1 | 7 | 7 | Counts agree; table cites BGC0000818 |
| NRPSLIKE_59 | BGC0001399.1 | 12 | 11 | Scored-population difference unresolved |
| NRPSLIKE_66 | BGC0000442.1 | 8 | 7 | Scored-population difference unresolved |

The complete identifier lists are retained in the companion TSV. Source cutoffs are inherited historical family-selection metadata. They are not sequence-identity percentages or curator-set acceptance thresholds. Quantitative locus correspondence, competing-locus checks, full strain aliases and scored-population membership are not established by this pass.

## Tryprostatin B, feature 1701

The source assigns DMAT_33 at cutoff 65 to BGC0000356. Physical PDF page 23 explicitly labels the product Type IV. [Maiya et al. (2009), abstract](https://doi.org/10.1016/j.fgb.2009.01.003), PMID 19373974, reports exact-product heterologous-expression evidence. That supports an experimentally established reference product; it is not merely a name inferred from a database entry. The reviewed publication was verified through its primary PubMed record, without extracting production instructions.

Disposition: provisional. The decisive measured-chemistry limit is the putative Type IV assignment. A reference-supported proposal would require stronger deposited or published identification of historical feature 1701 and justified correspondence for the sampled query. Existing experimental reference evidence does not authenticate this historical feature.

## Emericellamide B, feature 5402

The source assigns HRPKS_71 at cutoff 70 to BGC0001290. Physical PDF page 22 gives B its own Type II panel. [Oh et al. (2007)](https://doi.org/10.1021/np060381f), PMID 17323993, is the primary isolation and structure report for A and B. It supports B as a distinct chemical product, not a specific sampled query-to-product assignment.

The focused check of [Chiang et al. (2008), Results and Figures 1–2](https://pmc.ncbi.nlm.nih.gov/articles/PMC2494592/), DOI 10.1016/j.chembiol.2008.05.010, is decisive: the genetically linked products are A and C–F. B is not among them. This is an actual limitation of that cited experiment, not an uninspected section. The full-length match reported in the separate A packet cannot establish B by analogy.

Disposition: provisional despite strong source chemistry. Reopen with exact-B experimental pathway evidence applicable to a represented reference or another explicit, scientifically justified product-assignment argument. This bounded search did not establish that no such publication exists anywhere. Neither a new wet-lab experiment nor outside review is automatically required.

## Mycophenolic acid, feature 128

NRPKS_41 at cutoff 70 cites BGC0001677; the archive also contains two other reference records. Physical PDF page 23 says Type III. [Gillot et al. (2017), abstract](https://doi.org/10.1016/j.fm.2016.10.013), PMID 27889155, reports genetic perturbation linked to reduced exact-product measurements, with LC-Q-TOF/MS and expression measurements. The primary abstract therefore provides experimental reference support. Its experimental and genome-reference strains are not interchangeable with the Caesar sampled strains without a crosswalk.

Disposition: provisional, with a plausible reference-supported route after sampled/reference correspondence and the scope of the medium-confidence historical chemical assignment are adjudicated. The gap is the transfer and measured-identity decision, not a lack of published reference experiments. No source-positive culture is automatically required to undergo a new perturbation.

## Notoamides A and B

Both rows cite NRPS_66, cutoff 60, and BGC0000818. The archive includes two reference records, so the table's single accession must not be mistaken for the entire family. [Kato et al. (2007)](https://doi.org/10.1002/anie.200604381), PMID 17304611, provides primary isolation/structure evidence for the named compounds. [Li et al. (2012), abstract](https://doi.org/10.1039/c2md20029e), PMID 23213353, reports comparative pathway analysis with proposed assignments and ongoing biochemical work. That wording is not evidence that every named congener was experimentally established at every sampled locus. Full-text access in this pass was incomplete, so uninspected product-specific details remain unknown.

For A, feature 1673 has an explicit Type IV panel on physical PDF page 24. Its historical identity remains putative. The focused literature check did not establish an exact-A terminal-product experiment sufficient to replace that uncertainty. Keep it provisional; reopen with stronger feature identification and an exact-product reference appraisal tied to the declared query. B's evidence must not be transferred to A merely because the names and family overlap.

For B, the workbook says only `notoamide`, while the inventory says B. This is a literal name mismatch. Physical PDF page 26, Supplementary Figure 2h, explicitly labels both the authenticated standard and the A. amoenus NRRL 236 comparison as notoamide B, with the same reported retention time within that figure. It supports the source's intended B assignment; it does not establish an additional chiral measurement or a native-scan-to-feature join. [Fraley et al. (2020), Figure 1 and PubMed figure caption](https://pubmed.ncbi.nlm.nih.gov/32246875/), DOI 10.1002/cbic.202000004, supplies exact-B biochemical product-assay evidence against standards, including separate enantiomer labels. That is stronger than treating a generic family reference as support for B.

B remains provisional pending the explicit figure-to-workbook/sample correspondence and sampled-family/reference appraisal. It has a credible reference-supported route without new experimental work. Do not silently assign an enantiomer to feature 9213.

## Notoamide E4, feature 4182

The workbook and inventory name E4. But physical PDF page 26, Supplementary Figure 2i, says notoamide E for both the standard and A. westerdijkiae ATCC 22947 comparison. The panel's Type I route does not resolve that name conflict. Retention times from different analytical displays are not an identity conversion rule.

[Tsukamoto et al. (2009)](https://doi.org/10.1021/ja810029b), PMCID PMC2671082, is a relevant exact-name reference: its indexed primary text identifies E2–E4 as distinct metabolites in an isotope-incorporation study. This is evidence that E4 is a distinct reported product, not permission to treat E and E4 as synonyms. The full text could not be re-inspected reliably after the initial indexed result: PMC returned a browser challenge, Europe PMC XML returned HTTP 500, and the focused PDF retrieval timed out. Accordingly, the exact E4 incorporation result and query-specific pathway assignment are not marked verified here.

Disposition: provisional with unresolved chemical identity. Reopen first with the deposited structure/standard annotation that connects feature 4182 to E or E4, then appraise the correct exact-product reference. A biological assignment cannot repair a contradictory chemical label. No negative label is created.

## Fellutamide B and terrequinone A

Fellutamide B feature 1764 is Type II on physical PDF page 22. NRPSLIKE_59, cutoff 75, contains BGC0001399.1. [Yeh et al. (2016), abstract](https://doi.org/10.1021/acschembio.6b00213), PMID 27294372, reports experimental activation with exact-product identification. This is direct evidence for the reference system. The archive contains 12 sampled identifiers, while the table reports 11; no member has been discarded to make those totals agree. Proposed class remains provisional. Reference-supported treatment is plausible after the reference-to-sampled correspondence and source scoring population are resolved.

Terrequinone A feature 1761 is Type IV on physical PDF page 23. NRPSLIKE_66, cutoff 75, contains BGC0000442.1. [Balibar et al. (2007), abstract](https://doi.org/10.1038/nchembio.2007.20), PMID 17704773, reports complete biochemical reconstitution of the exact reference product. Reference evidence is therefore experimental and product-specific. Nevertheless, a putative historical identification and the archive's 8-versus-table's-7 population difference remain. Keep this case provisional. Stronger measured-feature identification, a declared scoring population and query correspondence would reopen a reference-supported proposal.

## Limits and closure

This completes one bounded source review and focused resolution pass for each case. The paired TSV separates exact-product experimental support, chemical confidence, family membership and method readiness. Native-scan links, released sequence inputs, full candidate universes and method versions are unknown or unfrozen; no method run was performed. The workbook's historical feature pool must not be represented as a newly frozen release.

All cases carry source-selection and known-reference exposure: these are retrospective development examples selected in a published correlation workflow. Cached current MIBiG pages served as reference indexes only; historical archive versions remain explicit. No unresolved candidate becomes a negative label, and no provisional row increases an accepted-label or independent-query count. A researcher-led disposition can proceed from documented evidence; an external reviewer is not a prerequisite invented by this review.
