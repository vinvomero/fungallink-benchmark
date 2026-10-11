# Public metadata retrieval before correspondence

Checked 7 October 2026. The proposed email was too broad. Public files resolve much of the sample-label request; no email has been sent.

## Retrieved and reconstructed

Fresh anonymous FTPS listings and submission parameter XML were retrieved from the official MassIVE service for MSV000089848 and MSV000081097. Plain FTP required TLS, so the successful connection used FTP_TLS. Receipts, hashes and exact URLs are under data/raw/public-metadata-recheck-2026-10-07/. The raw parameter XML is retained privately; only file-mapping fields were exported for analysis, not submission account fields.

MSV000089848 provides 357 upload-file mappings in params.xml. The public publisher workbook already supplies strain and medium labels in rows 6 and 7 and acquisition filenames in row 8. Joining these public sources resolves 356 of 362 workbook columns: 345 exact filename stems and 11 unique case-insensitive matches. Six columns have no matching original upload record: ATCC48694 and NRRL1061, each in Cheerios, Oats and Rice. One repository upload has no workbook column (NRRL2393 Cheerios rerun). This is a source-label join, not proof of genome or culture identity.

The saved public-source table is data/curated/caesar-public-acquisition-labels-2026-10-07.tsv. All 362 workbook strain/media/header fields were independently compared against the existing crosswalk and agree. No supplied sample map was an input to reconstruction. This removes the need to request a complete acquisition-to-strain/media map. It does not independently establish the assembly fields supplied by the old map or resolve the FMGX-to-study identity bridge. Frozen numerical inputs and biological labels are unchanged.

The FAC submission XML contains 12 upload mappings, matching raw filenames labelled aculeatus, terreus and wentii with four numbered files each. The accessible current listing contains the raw files and parameters, not an XCMS CSV/workbook or an explicit FAC-construct/control map. The journal methods already describe processing, so a generic processing-settings request is unnecessary. This inspection does not prove that no other public deposit exists or that filenames alone establish donor strain identities.

Both official MassIVE landing records state CC0 for deposited data. Do not ask permission to reuse those deposited files. That statement does not authenticate separately supplied historical files or change publisher-supplement terms.

## Remaining bounded request

Ask only for a public locator for the source GCF display/FMGX identity crosswalk (public strain-to-assembly information is already in Supplementary Table 2), clarification of the six unmatched workbook acquisitions if useful, and the original full FAC processed matrix plus construct/sample and published-target-to-row mappings. If records are supplied privately, ask their attribution/reuse terms. The full FAC matrix is the strongest remaining reason for correspondence. No claim of web-wide nonexistence is made.

## Access limits

The ccms_peak entries were advertised by FTPS as file-like pointers; normal retrieval and directory listing returned permission-denied errors. No access-control bypass was attempted. Cached public file manifests still describe converted files. Nature and PMC web views returned an identity redirect or challenge during this check; Europe PMC XML requests returned HTTP 500. Retained primary manuscript/supplement copies were reused for already established information instead of treating those access failures as evidence of absent data.

Primary web records: https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=a217f4ab6ba04103a71c6d4859538493 and https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=60eb7c82896a4df9bf8e80309382cfaf . Publisher workbook: DOI 10.1038/s41589-023-01276-8, Supplementary Data 2, retained SHA-256 4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb. FAC methods: DOI 10.1038/nchembio.2408. No email or new biological experiment was performed.
