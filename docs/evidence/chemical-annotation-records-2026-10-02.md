# Historical chemical annotation records

Reviewed 2026-10-02. This bounded review covers only monacolin K feature 1633, mycophenolic acid feature 128, and the notoamide E4/E label for feature 4182. It follows the canonical benchmark plan and the preceding remaining-chemical-admission review. The companion TSV has three rows.

Supplementary Table 5 supplies a previously overlooked explicit assertion: linkage 22, metabolite ID 4182, **notoamide E**, on actual PDF page 12, printed page 11. A fresh text extraction and page render confirm the row. The source-named E target has a feature-ID bridge to the E Type I panel in Supplementary Figure 1 (actual page 20, second panel) and the E standard/extract comparison in Figure 2i (actual page 26). Both existing page images were freshly inspected. This supports a proposed corrected E target for feature-only chemistry within the existing relationship, not an additional case or independent query.

The workbook at Sheet1, physical row 4190, and Supplementary Table 4 still say `notoamide E4`. Those strings are retained. This review does not authenticate E4, declare it a synonym of E, identify an isotope convention, or assign an enantiomer. The explicit E assertion makes a corrected source-named E target supportable; it does not explain why the conflicting E4 string appears. The previous E4 identity remains unvalidated. No exact-E4 reference evidence is transferred to E.

The original library match records for monacolin K and mycophenolic acid were not recovered. Their existing insufficient-exact-product dispositions remain unchanged. This does not disprove either annotation or require an authenticated standard for every feature.

## What was inspected

The original workbook was read with row-8 headers. Each requested feature ID occurs once: 1633 at physical row 1641 (`monacolin K`), 128 at row 136 (`mycophenolic acid`), and 4182 at row 4190 (`notoamide E4`). Its first four columns are row ID, m/z, retention time, and identity; the remaining columns are peak heights. It contains one sheet and no separate match-results sheet. Mass or retention time was not used to infer a feature-to-scan join.

The retained supplementary PDF was searched across all pages for these names, exact feature IDs, GNPS references, and embedded URLs. Its only embedded URI is the article DOI. Table 5 explicitly pairs the three IDs with their names, including E for 4182. The source's Type III panels and prior packets establish the reported public-spectrum route for monacolin K and mycophenolic acid; they do not provide the missing library accessions and feature-specific match results. No generic GNPS reference-compound entry was substituted for a historical result.

Fresh public MassIVE requests inspected the file manifest, linked-reanalysis endpoint, and the only non-spectrum file in the listed deposit, `ccms_parameters/params.xml`. The manifest lists 715 file representations: 357 in `ccms_peak`, 357 in `peak`, and one parameter file. These are not 714 spectra or independent acquisitions. No processed annotation export appears in that inspected listing. The reanalysis response contains an empty `massivereanalyses` array. The parameter XML describes the deposit workflow `MASSIVE-COMPLETE` version 1.3.2 and its deposit task, not a historical molecular-networking result task. Its file references and parameter names yielded no separate match-export locator. These findings describe the inspected routes only; they do not prove that no annotation export exists elsewhere or in nonpublic material.

Focused web searches used the article DOI with GNPS, MSV000089848 with GNPS/task, Caesar plus monacolin and the GNPS task URL, and the literal E4/4182 pair. They supplied the deposit and primary article locators but no historical match-export task. Opening PMC returned a browser check. A Europe PMC full-text XML request returned HTTP 500. The retained main-paper text was inspected for the chemical annotation and data-availability passages: it describes GNPS use and the MassIVE accession but gives no task-specific match export there. General method thresholds cannot stand in for the individual observed matches. No further broad literature search was undertaken.

## Exact records still needed

For feature 1633, recover the original monacolin K/lovastatin library match export or equivalent existing identification record that names the historical feature, the GNPS library accession/version, and its observed match evidence. For feature 128, recover the corresponding mycophenolic acid record. A historical GNPS result-task URL, if available, would locate the original export. If an export uses network nodes or scan IDs instead of workbook row IDs, it also needs the existing provenance mapping that ties those identifiers to the feature. A new search result or mass/retention-time resemblance cannot reconstruct that mapping.

For 4182, source-named E now has an explicit published join. An existing annotation-history or correction record explaining the workbook/Table 4 E4 text would resolve the remaining provenance discrepancy, but it is not necessary to invent such an explanation to preserve Table 5's E assertion.

Historical native MS/MS membership remains unestablished here and is a separate spectral-readiness issue. No universal scan-join gate has been added to feature-only chemistry. Biological admission, sample correspondence, candidate-universe freezing, and human signoff remain unchanged. No sequence, pathway, production, or experimental work was performed.

## Source provenance

All new payloads are ignored under `data/interim/chemical-annotation-records/`. Successful responses were retrieved on 2026-10-02; hashes below describe those exact responses. Existing publisher files were inspected on that date and retain their 2026-10-01 registry retrieval date.

| Payload | Locator | Bytes | SHA-256 / status |
| --- | --- | --- | --- |
| `massive-files.html` | [source](https://massive.ucsd.edu/ProteoSAFe/dataset_files.jsp?task=a217f4ab6ba04103a71c6d4859538493) | 323874 | `639ca41263b26fd745ae74bbd999b46aa6f1a2a370a7b59258b689e58cca5938` |
| `massive-reanalyses.json` | [source](https://massive.ucsd.edu/ProteoSAFe/MassiveServlet?function=reanalysis&task=a217f4ab6ba04103a71c6d4859538493) | 27 | `6dcdc5283afc4ef3a6dc6f276fe747226661626a9f6e4c2a9190097a2a3d30e3` |
| `params.xml` | [source](https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?file=f.MSV000089848/ccms_parameters/params.xml) | 56382 | `48e5f61ca5750bc0c5c017715a25cedfdea01286e78784d44551aab06396376b` |
| `article.xml` | [source](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10313767/fullTextXML) | not retrieved | `HTTP Error 500: ` |
| `data/raw/sources/metadata/caesar-supplement-cdn` | [publisher](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM1_ESM.pdf) | 5911348 | `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108` |
| `data/raw/sources/caesar-2023/41589_2023_1276_MOESM4_ESM.xlsx` | [publisher](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM4_ESM.xlsx) | 19251141 | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |

The newly rendered page 12 is a local inspection aid, not a second source. The original PDF provides its evidence identity. The public deposit is [MSV000089848](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=a217f4ab6ba04103a71c6d4859538493). The primary article is [Caesar et al. 2023](https://doi.org/10.1038/s41589-023-01276-8).

## Unsent author-query draft

We are reviewing the published chemical feature annotations in your 2023 study. Could you point us to the existing GNPS result task or library-match export for monacolin K, feature 1633, and mycophenolic acid, feature 128? The records we need are the original library accession/version, match result, and the existing mapping to those workbook feature IDs if the export uses different identifiers. We also found feature 4182 named notoamide E in Supplementary Table 5 but notoamide E4 in Table 4 and the workbook. Is there an existing annotation-history or correction record explaining that difference? We are requesting existing records only.

This draft has not been sent. No correspondence or public release was performed. The review is agent-authored with no scientific signoff. Requested worker route: `gpt-6-astra` / `medium`; no serving-side receipt was available to confirm the actual model or effort.
