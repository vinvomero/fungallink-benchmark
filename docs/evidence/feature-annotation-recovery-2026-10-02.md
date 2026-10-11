# Recovery of five historical chemical annotations

Reviewed 2026-10-02 under the canonical benchmark plan and contract. The companion TSV preserves features 148, 535, 1633, 128 and 4902. This chemical-evidence review adds no admitted relationships and provides no scientific signoff.

The new public-record routes recovered the publisher article, its complete supplemental-link list, the PMC BioC manuscript, the publisher Reporting Summary and the depositor's indexed GNPS user page. None supplied an individual identification record for these five features. This is a bounded retrieval result, not evidence that the annotations are false or that records do not exist elsewhere.

The roquefortine disposition needs a narrower reason than the earlier packet gave. The IV/III discrepancy is an unresolved source inconsistency. It does not itself disprove either identity. Both panels explicitly claim Type III identification; the missing item is the underlying feature-specific public-library comparison, including its accession and observed result. Resolving the tier wording without recovering stronger identity evidence would not close that gap. Conversely, sufficient existing identity evidence would allow chemistry review to proceed while preserving the tier discrepancy as a provenance note.

## What the new routes established

The direct [publisher article](https://www.nature.com/articles/s41589-023-01276-8) request succeeded even though the web browsing service encountered an identity-provider redirect. Its supplemental links identify four assets: Supplementary Information, Reporting Summary, Supplementary Data 1 (the previously catalogued archive), and Supplementary Data 2 (the previously inspected feature workbook). The inspected links contain no additional annotation table, processed spectral export or historical GNPS result-task link. The archive was not reinterpreted as chemical-identification evidence.

The [PMC BioC manuscript](https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC10313767/unicode) was recovered successfully. Its chemistry methods distinguish public experimental-spectrum comparisons from tentative assignments using predicted fragmentation. The latter do not establish exact identity merely because several fragments are compatible. Its data-availability passage points back to the known deposit and workbook, with no separate match-export locator. Method-wide acceptance criteria do not report the actual result for an individual feature.

The [Reporting Summary](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM2_ESM.pdf) was newly retrieved and both pages were inspected visually. Page 1 records MZmine 2.53 and a GNPS portal availability date of March 15, 2022. That date is useful historical context, not a GNPS job timestamp or library version. Its data section again names the existing deposit and processed peak list; neither page provides feature-specific identification results.

The publicly indexed [GNPS depositor page](https://gnps.ucsd.edu/ProteoSAFe/user/summary.jsp?user=lkcaesar) was retrieved directly after the browser service timed out. Its embedded dataset table contains four public deposits, including MSV000089848. The matching entry uses the known deposit task, not a molecular-networking result task. A further task string in the page belongs to the site's generic user-network display; it is not evidence of this study's chemistry analysis. The page is not a census of every job run by the depositor, so its contents cannot prove that no relevant job exists.

Focused indexed searches used the article identifier, the manuscript identifier, the study title, the deposit accession, the depositor username and GNPS-domain restrictions. They located these primary-source routes but no usable historical feature-specific match record. No old MassIVE manifest, reanalysis or parameter endpoint was requested again. No new spectrum search or raw-file reprocessing was performed.

## Five finite dispositions

| Feature | Source name | Evidence retained | Disposition and exact reopening record |
| --- | --- | --- | --- |
| 148 | roquefortine C | Table 5 name-ID bridge; Figure 1 Type III panel; inventory IV retained | Unresolved exact-product chemistry. Recover original individual library comparison with accession/version and observed match evidence tied to 148. A tier correction alone is insufficient. |
| 535 | roquefortine D | Table 5 name-ID bridge; Figure 1 Type III panel; inventory IV retained | Same bounded disposition, independently for 535. C's evidence cannot establish D. |
| 1633 | monacolin K | Published name-ID bridge and reported public-spectrum route | Recover existing individual identification record for 1633, including the reference identity and observed comparison. A generic lovastatin library entry is not this historical result. |
| 128 | mycophenolic acid | Table 5 name-ID bridge; Figure 1 Type III panel | Recover original feature-specific public-library match record for 128. The displayed annotated experimental spectrum supports the reported assignment but lacks the comparison record needed to appraise alternatives. |
| 4902 | rubropunctatine | Table 5 name-ID bridge; Figure 1 Type IV panel | Retain putative chemistry. Reopen with an existing authenticated-standard or independent structural-identification record tied to 4902 that distinguishes the exact product from compatible alternatives. |

The Type III panels display annotated experimental spectra, not a paired reference comparison with a library accession, match result or explicit alternative-candidate assessment. Fresh visual inspection covered actual supplement page 23, panels 1 through 3, and page 24, panel 1. These observations do not establish a particular alternative identity. The broader alternative that remains unresolved is a structurally compatible annotation that those displayed records alone do not distinguish. Rubropunctatine's spelling is preserved; using the literature spelling rubropunctatin to find a reference would not authenticate feature 4902.

All five retain a published named-feature bridge. Recovering a feature-specific identification record does not universally require a native-scan join for feature-only chemistry. An identifier crosswalk is needed only when the recovered record uses a different namespace. Native MS/MS membership remains a separate spectral-input question. Biological eligibility and human review are also separate and unchanged. Unresolved features are not negative labels.

This focused recovery attempt is closed with five unresolved exact-product dispositions. Reopen it on receipt of the named existing records, not by repeating broad endpoint searches. A separate raw-reprocessing effort would create new feature identities and would require its own target re-establishment.

## Access and source preservation

The alternate PMC manuscript-supplement URL returned a browser-check HTML page with HTTP 200, not a PDF. The PMC OA endpoint returned HTTP 404. Those are access failures, separate from the content gaps found in the successfully inspected publisher and manuscript records. The already retained publisher supplementary PDF remained available for inspection.

All newly downloaded payloads remain ignored under `data/interim/feature-annotation-recovery/`, with exact URLs, response sizes, content types and SHA-256 values in `retrievals.json`. Response dates follow the requested review date, 2026-10-02. No source license was changed or inferred from public accessibility. Publisher rights remain pending release review under the existing source registry; BioC and GNPS responses are retained as supplied, not relicensed.

| Successfully retrieved payload | Bytes | SHA-256 |
| --- | --- | --- |
| Publisher HTML | 420066 | `0bdbb9a754e287ea621655256cb25e63108535cb86bf57ff4d4a09c227cc9842` |
| PMC BioC XML | 113653 | `b507fb31770451e358060fe63c8dd42718b553351a84d9ae4e0d7dd6c0523701` |
| Reporting Summary PDF | 1037026 | `bb06be115438c7119bd5111f3ccc0c7aaf193838d1a0c9ece3868b0254329f69` |
| GNPS depositor HTML | 24860 | `fe6e19bbc1a7d3b60eab16276ff06adbbf7ac2e201faa038334f60f775672a88` |

The original supplement is [publisher Supplementary Information](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM1_ESM.pdf), SHA-256 `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108`. Its Table 5 on actual page 12 supplies the previously established feature-ID bridge. Freshly inspected source representations do not create independent evidence or independent queries.

## Unsent request for existing records

We are reviewing five chemical annotations from the 2023 study: roquefortine C (148), roquefortine D (535), monacolin K (1633), mycophenolic acid (128), and rubropunctatine (4902). Could you point us to the original identification records or GNPS result task for these features? For public-library assignments, we need the library accession/version and observed match result, together with an existing feature-ID crosswalk if the export uses node or scan identifiers. For 4902, is there an existing standard comparison or independent structural-identification record beyond the published Type IV fragment interpretation? The roquefortine panels say Type III while the retained inventory records IV; an existing annotation-history record explaining that difference would also help. We are requesting existing records only.

This request has not been sent. No external correspondence, public release, biological mapping or experimental work was performed. Validation confirms five unique expected feature IDs and zero main pairs added. Requested worker route: `gpt-6-astra` / `medium`; no serving-side receipt was exposed to verify actual model or effort.
