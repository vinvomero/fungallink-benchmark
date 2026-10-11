# Exact-product evidence follow-up

Reviewed 2026-10-02 against the [canonical plan](../plans/2026-09-30-2052-benchmark-paper-plan.md) and [benchmark contract](../../protocol/benchmark-contract.md). This bounded follow-up covers five existing relationships. It closes the missing biochemical core-product evidence for acetylaszonalenin. It does not admit any relationship or change the evidence rules. The other four exact-product gaps remain open.

Requested route: `gpt-6-astra / medium`. No serving-side receipt was exposed to this worker; actual model and effort remain unverified. Humanizer rules were applied. Earlier packets supply the retained source chemistry and sample joins; the new findings below concern primary reference evidence.

## Griseofulvin congeners

The previously uninspected [Cacho 2013 supplement](https://stacks.cdc.gov/view/cdc/29769/cdc_29769_DS25.pdf), retained NIHMS522449-supplement-1_si_001.pdf, has 61 pages. Table S10 (18S) gives compound 13's drawing, mass and UV information, without an NMR assignment table. Table S12 (20S) gives compound 15's drawing and NMR assignments. Both drawings retain the aromatic substitution pattern previously found to differ from Caesar's 6-O products. In the supplement's own numbering, Table S12 assigns the aromatic methoxy correlation to C3 and leaves C5 unmethylated. This supports the published connectivity; it supplies no correction that swaps those substituents. Figure S28 (52S) was inspected as the accompanying HSQC/HMBC panel, without claiming a fresh independent structural elucidation. There is no demonstrated 6-O identity established by this inspection.

Thus `caesar2023:relationship:9` (feature 6346) and `caesar2023:relationship:10` (feature 2824) remain provisional. They cannot inherit exact-product reference evidence through the abbreviated desmethyl names. Reopening needs an exact-product assignment or documented primary-source correction, followed by the sampled-member correspondence required in the prior packet.

For `caesar2023:relationship:12` (feature 208), newly inspected indexed primary text from [Chooi 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2884005/), Results subsection on the two essential PKSs, calls compound 3 dechlorogriseofulvin and says its NMR comparison used both parent griseofulvin and the Jarvis epidechlorogriseofulvin reference. Citing an epi comparison spectrum does not itself identify the observed product as epi. The paper continues to assign compound 3 as ordinary dechlorogriseofulvin. Table S3 itself was not inspected. The [ANU repository record](https://openresearch-repository.anu.edu.au/items/8b050150-91a4-43ac-9fb4-e75ed978a4aa) lists its PDF as restricted until 2037; direct publisher access also failed. This is a primary-text result inspected through its search index, not newly accessed complete publisher text. The exact epi reference-product gap remains open. Reopen with an explicit stereochemical assignment connecting the reference experiment to the epi product, rather than treating the cited comparison or a database list as that assignment.

## Acetylaszonalenin

The earlier assessment stopped at Ames 2010. [Gao et al. 2012, DOI 10.1038/nchembio.1047](https://www.nature.com/articles/nchembio.1047), adds experimental core-product evidence. The [Harvard author manuscript](https://dash.harvard.edu/bitstreams/7312037c-dbd3-6bd4-e053-0100007fdf3b/download) was retrieved and inspected directly: PDF page 4, printed manuscript page 3, Results on reconstitution, reports the core product against an authentic standard; PDF page 5, printed page 4, reports its stereochemical comparison. Figures 3c and 4a are on PDF pages 16 and 17. These are demonstrated product outcomes. Uncertainty over the detailed cyclization mechanism does not make the observed product hypothetical.

Together with the already established exact final-product evidence in [Yin et al. 2009](https://doi.org/10.1074/jbc.M807606200), this closes the previously missing biochemical reference-chain step for `caesar2023:corrected:5`, feature 2127. The earlier assertion that only an early core activity was experimentally supported is superseded. A special class for partially characterized pathways is no longer needed to address that specific gap. This is evidence assembled across studies, not a claim of native whole-locus perturbation or a single complete-pathway experiment.

The relationship still awaits the corrected sampled-locus correspondence and relevant ambiguity assessment. Recommend ordinary reference-supported reassessment when those documentary connections are established; retain provisional status meanwhile. Neither the historical DMAT_34 assignment nor a direct experimental claim about the Caesar culture follows from this correction.

A newly inspected [Lu and Liu D22 abstract](https://ir.cnu.edu.tw/bitstream/310902800/31388/1/D22.pdf), page 1, mentions a deletion background in a different species. Its indexed text does not establish the needed native reference-to-exact-product conclusion for this sample. It is not the basis for closing the gap.

## Emericellamide B

The new candidate was the primary study [Identification of Secondary Metabolites from Aspergillus pachycristatus by Untargeted UPLC-ESI-HRMS/MS and Genome Mining](https://pmc.ncbi.nlm.nih.gov/articles/PMC7071103/). Its indexed Table 1 lists emericellamides A, C/D, E, F, G and H, without B; Table 3 describes inferred clusters. It therefore adds neither exact-B identification in that study nor an experimental exact-B reference assignment. Direct PMC access returned a browser challenge, so this inspection is limited to indexed primary tables and their accompanying text.

`caesar2023:relationship:7`, feature 5402, remains provisional source recovery. The already sufficient Caesar chemistry stays separate from this reference-evidence failure. Reopening still requires exact-B experimental reference support or a documented alternative assignment argument that exceeds the A/C-F evidence. No negative label follows from this unsuccessful search.

## Records and checks

The [companion TSV](../../data/curated/exact-product-gap-resolution-2026-10-02.tsv) contains five unique original review keys, prior gaps, newly inspected sources, findings, explicit gap-closure flags and reopening records. Its `gap_closed` field refers only to the named reference-evidence gap, not overall admission. Four values are false and acetylaszonalenin's is true. Chemistry, sampled correspondence, method inputs and scientific signoff remain distinct.

Retained scratch PDFs are under `data/interim/exact-product-gap-resolution/`. Cacho SI SHA-256: `2c909408443ced4601e091a57d784a4c103ab193c0ddeb11ecdd820f2b8f6070`. Gao author manuscript SHA-256: `6426feeb5c1c6733df25baa71ccf8ac9950ecc7939162c4996ddbabd2e0d00a1`. The Harvard copy includes a repository cover sheet, which explains the one-page offset from manuscript pagination. Public locators and hashes identify the versions; ignored scratch is not a release dependency.

No admissions, query counts, pathway counts, spectral readiness, method versions or candidate universes changed. No sequences, engineering procedures or production instructions were extracted into the deliverables. These remain exposed, source-selected retrospective cases.
