# Public-data search before FAC and HEx correspondence

Completed 9 October 2026. No emails sent. **No complete feature table or sample-to-acquisition crosswalk was recovered, and no new benchmark relationship was admitted.** The ledger remains at 27 relationships across 15 query identities, with 11 relationships evaluated. This sprint recovered additional source files and narrowed the remaining requests.

The user explicitly requested a new public-data sprint before correspondence. This reopens the acquisition search under that authorization, not because the earlier evidence disappeared. The search used repository APIs, a public code repository, Addgene records, and the original HEx preprint supplements in addition to web search. Frozen labels, inputs, scores and protocols were not changed.

## Files recovered and what they establish

All paths below are relative to `data/interim/pre-correspondence-sprint-2026-10-09/` unless stated otherwise.

| Source | Recovered material | What it answers | What remains unresolved |
|---|---|---|---|
| [MassIVE MSV000082097](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082097) | `MSV000082097/benzomalvin_A,D_ms2.mgf`, parameters and complete file inventory | A public deposit describes a benzomalvin A/D spectrum from AtFAC9J20. The downloaded MGF contains one spectrum. | No abundance matrix, full acquisition or sample crosswalk. Its sample description conflicts with that of an identical file in the second deposit. |
| [MassIVE MSV000082100](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000082100) | `MSV000082100/benzomalvin_A,D_ms2.mgf`, parameters and complete file inventory | A second deposit describes benzomalvin A/D from A. terreus. | The MGF is byte-identical to MSV000082097. These are one distinct file, not independent observations. |
| [Benzomalvin follow-up supplement](https://acs.figshare.com/articles/journal_contribution/6002381) | `benz-followup-si.pdf`, three pages; repository metadata and text extraction | Table S1 identifies the linear tripeptide as compound 3, formula C24H23N3O4, source exact mass 417.1689. | No native feature-row identifier, sample-intensity table or acquisition map. This is supplemental characterization, not a candidate universe. |
| [HEx preprint supplements](https://www.biorxiv.org/content/10.1101/247940v1.supplementary-material) | `247940-1.pdf` (81 pages) and `247940-3.zip` | Provides the earlier tables and sequence archive for a version check. | The archive's uncompressed GenBank payload is byte-identical to the published one. The earlier tables also contain the PKS1 version discrepancy and the named third PKS16 construct. They do not correct the gaps. |
| [HEx Addgene collection](https://www.addgene.org/browse/article/28193299/) | Article inventory and [110672](https://www.addgene.org/110672/), [110673](https://www.addgene.org/110673/) pages | The collection lists 48 plasmids. The two PKS16 entries explicitly describe its PKS and tailoring-gene constructs. | No third PKS16 entry was found in this collection. Sequence downloads require login and were not retrieved. The public metadata does not establish equivalence to the missing record. |
| [Caesar FAC-scoring repository](https://github.com/lindsaycaesar/FAC-scoring) | Tree, branch and blob metadata; `FAC Score code.py` | The inspected master tree contains one Python file, including a CSV import and group-based scoring code. | No dataset is included in that tree. The code names a local development CSV and a Cladonia output; it does not establish that these are the 2017 source exports. The code was read, not executed. |

The two MGF files are each 28,233 bytes with SHA-256 `5ec531a6b83e7ddd7da9da749fba1810d349697f7ebc28c32b638050725b4222`. They contain one `BEGIN IONS` / `END IONS` block, a scan-1 title, retention time 2725.20078 seconds and a precursor header of 382.066741943359. That precursor header is not silently substituted for a chemically verified mass. The files remain source material, not activated benchmark spectral inputs. Both deposits have an empty statistics file, rather than a feature matrix. See `spectral-file-audit.json` and the two deposit inventories.

The preprint and published ZIP files differ as archives, but both contain exactly the same 2,060,980-byte GenBank payload, SHA-256 `6e3bfe142db6eac8b1622cd9900ab6dd511fb326533b2b55e35b35106291b240`. The payload contains 78 records. Preprint PDF pages 30, 34 and 35 retain the PKS1 -2.2/-2.1 and PKS16 third-record questions. See `hex-preprint-sequence-comparison.json` and `hex-preprint-table-locations.json`. No reference-protein comparison was rerun.

## Search coverage and limits

Before searching, I checked CURRENT_STATE, the canonical plan, source-reuse index, artifact and question records, the 76,799-row file inventory, prior FAC/HEx search requests, existing supplements and deposit inventories. The old MSV000081097 raw files were not downloaded again. Its 12 species-labelled acquisitions still cannot be assumed to cover the 56-FAC expression screen.

This sprint retained 36 exact web queries in `search-1.json` through `search-9.json`, plus a separate Firecrawl query receipt. Some queries returned irrelevant name/acronym matches; those were not used as evidence. Repository requests and their outcomes are in `retrieval-request-1.json` through `retrieval-request-8.json` and `retrievals.jsonl`.

- MassIVE's native API returned all 304 title matches for FAC, all 63 for fungal, 19 for HEx and 18 for heterologous. Exact product/title searches and uploader searches followed. The two uploader filters were checked against the returned user IDs: kdclevenger returned MSV000081097; mtrobey returned MSV000082097 and MSV000082100. No full expression table was found in these identified deposits. Other fungal datasets in the broad results are leads for a separate expansion task, not admissions or substitutes for these cohorts.
- Figshare's exact benzomalvin title search found the three-page supplement. The HEx phrase search returned no records. DataCite returned 38 DOI records referencing the HEx paper, all with the relation `References`; these describe other studies' supplements, not a HEx data deposit. The FAC DOI relation query and the HEx title query returned zero records. These metadata searches depend on depositors' indexing.
- OmicsDI DOI searches returned no matches; title/subject searches recovered the known HEx and FAC BioStudies literature records and unrelated studies. No additional HEx or FAC measured-data accession was established. This includes searching an index that covers metabolomics repositories, not an exhaustive direct inspection of every repository.
- Zenodo's first request failed because unauthenticated page size was limited to 25. The corrected `aar5459` request succeeded and returned zero records. GitHub's HEx/fungal repository search returned zero; FAC-MS returned 515 matches, of which the first 100 were inspected. Caesar's FAC-scoring repository was the relevant lead followed. This was not an exhaustive GitHub code search.
- Direct bioRxiv HTTP requests returned 429 HTML, not XML or article content. Normal browser navigation succeeded, exposed three supplement links, and downloaded the relevant PDF and sequence ZIP. The separate Figure S7 phylogeny was not downloaded because it did not address the missing data or construct records. No access challenge was bypassed.

An empty search result is not evidence that data do not exist. The completed sprint establishes the checked routes and files, not worldwide absence.

## Changes to the unsent requests

The [FAC draft](kelleher-combined-request-2026-10-07.md) now acknowledges the two spectral deposits and the follow-up supplement. It asks for the complete expression-screen feature exports, construct/sample mapping and target-row joins, plus clarification of the duplicated spectrum's origin. It does not ask for a spectrum we already downloaded or for the recovered Caesar genome-label bridge.

The [HEx draft](hex-data-request-2026-10-08.md) now states that the original preprint archive was also checked and that Addgene supplies the two known PKS16 entries. It retains the requests for full XCMS tables, sample/target joins and an explanation or corrected record for the actual construct discrepancies.

Both requests remain justified as locator requests. Neither should claim that the authors failed to deposit data. No new experiments or reprocessing are requested.

**Next action:** review the revised unsent drafts. Author correspondence requires Vin's authorization. Resume acquisition if a new exact locator, author response or corrected record appears; use this receipt instead of repeating these searches. Benchmark admissions and scoring remain unchanged.
