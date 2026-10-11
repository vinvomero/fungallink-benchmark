# Approved-query input metadata, 2 October 2026

This pass closes public acquisition-label metadata for the approved pestalamide B GCF query (feature 810) and emericellamide A BGC query (feature 8468). The [ten-row metadata table](../../data/curated/approved-query-inputs-2026-10-02.tsv) contains nine pestalamide source members and one emericellamide acquisition group. It does not change the biological decisions or the original crosswalk, roster, evidence, or readiness ledgers.

Requested route: `gpt-6-astra`, `medium` reasoning. The native agent route accepted the request; no serving-side receipt was exposed. Humanizer was applied. The skill's referenced `references/signs-of-ai-writing.md` file was absent; the available SKILL.md rules were applied.

The public workbook and deposit manifest independently support all 30 candidate acquisitions: 27 for pestalamide and three for emericellamide. Each has two deposited format representations, giving 60 filenames, not 60 independent acquisitions. Five pestalamide member mappings, covering 15 acquisitions, and the emericellamide group, covering three, now have publicly traceable study-label-to-assembly metadata suitable for packaging. Four pestalamide member rows still need source provenance. Neither complete query is ready for scoring.

## What the public sources establish

The publisher workbook's Sheet1 rows 6, 7, and 8 explicitly supply strain, growth condition, and acquisition filename. All selected cells were checked against the existing crosswalk. Each exact filename stem was then checked against both its mzML and mzXML entries in the retained MassIVE file manifest. This recheck uses public study assertions rather than treating a successful join to the supplied sample map as proof of its provenance.

That distinction changes the status of the three CBS 101.740 columns DN, DO, and DP. Their filenames contain a species shorthand, but workbook row 6 explicitly says `CBS 101.740`. No inference from species or counts is needed to recover their study label. Supplementary Table 2 explicitly associates that label with GCA_001889945.1. The original crosswalk's `inferred` state remains untouched; the new table records the stronger metadata evidence separately. This is documentary traceability, not independent confirmation of the historical culture's identity.

| Source member or group | Assembly or namespace | Public mapping result |
|---|---|---|
| FMGX0077 / CBS 134.48 | GCA_001890745.1 | Three acquisitions; study label agrees with deposited identity |
| FMGX0067 / ATCC 13157 | GCA_003344505.1 | Three acquisitions; study label agrees with deposited identity |
| FMGX0056 / ATCC 10864 | GCA_001715265.1 | Three acquisitions; study label agrees with deposited identity |
| FMGX0052 / CBS 113.46 | GCA_000230395.2 | Three acquisitions; Table 2 explicitly co-lists ATCC 1015 and CBS 113.46 |
| FMGX0018 / CBS 101.740 | GCA_001889945.1 | Three acquisitions; workbook explicitly supplies the strain missing from the filenames |
| FMGX0055 / ATCC 64048 | GCA_001741885.1 | Three public acquisition labels; deposited strain A1 remains discrepant |
| FMGX0053 / ATCC 13490 | GCA_003344705.1 | Three public acquisition labels; deposited ATCC 13496 remains discrepant |
| FMGX0057 and FMGX0054 | Aspni_NRRL3 | Each retains the same six candidate acquisitions from ATCC 9029 and ATCC 64974; orientation unresolved |
| ATCC 38163 / FGSC A4 | GCA_000011425.1 | Three acquisitions; source assembly assertion and explicit catalog alias confirmed |

Supplementary Table 2, PDF pages 4–5 (printed pages 3–4), was visually rechecked. Its co-listing of ATCC 1015 and CBS 113.46 is a study-reported alias; no new culture-collection verification is claimed. Whitespace and the punctuation in CBS 101.740 are lexical normalizations only.

For emericellamide, Table 2 explicitly assigns ATCC 38163 to GCA_000011425.1. The fresh [NCBI assembly report](https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_000011425.1/dataset_report) identifies the deposited strain as FGSC A4, and the [FGSC A4 catalog record](https://www.fgsc.net/strain_detail.php?id=4) explicitly lists ATCC 38163 as an alternate strain number. BY, BZ, and CA are the public workbook columns, with Cheerios, Oats, and Rice respectively. The public metadata chain therefore supports the acquisition group's use of that assembly. The literal FMGX0049-to-culture bridge retains its historical provenance from the existing evidence packet; this review does not relabel it as a new public crosswalk. Exact BGC input packaging remains a separate step, and HRPKS_71 remains family context rather than a replacement for the approved BGC query.

## Family provenance recovered and still missing

Supplementary Figure 9, PDF page 33 (printed page 32), explicitly states that the final hybrid NRPS-PKS dataset used cutoff 65. The caption and panel d were visually inspected. This recovers the published class setting relevant to `NRPSPKS_85` / `HYBRID_85`; the number 85 in the family name is not the cutoff. The source's `NRPSPKS_85|MIXED_142` labels are preserved. The cutoff cannot be transferred to the MIXED label without its own source assertion.

The [primary paper's indexed Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC10313767/) describe similarity based on shared protein domains and sequence identity, with a cited prior method. They identify antiSMASH 6.0 as the detection version. This does not identify a clustering implementation release. A metadata keyword check of the selected HTML found no clustering version, threshold, cutoff, or generated-run header; its XML 1.0 declaration is a document-format version. The archive contains 29 selected HTML files and no separate run manifest. The exact clustering implementation/version and a run-specific assertion binding this deposited family to the published setting remain unresolved. The new table separates `published_class_cutoff=65` from `exact_family_run_manifest_status=unresolved_no_run_metadata_in_deposited_html`.

Source selection and parameter choice remain prior exposure for a retrospective benchmark. A source-selected family is not a complete reconstructed family universe.

## Bounded discrepancy check

One targeted public catalog check was made for the previously documented A1/ATCC 64048 and ATCC 13490/13496 conflicts. Direct retrievals of the [64048 catalog page](https://www.atcc.org/products/64048) and [13490 catalog page](https://www.atcc.org/products/13490) timed out. The indexed primary [ATCC 13490 product sheet](https://www.atcc.org/api/pdf/product-sheet?id=13490) identifies Poria cocos, while the indexed [13496 catalog entry](https://www.atcc.org/products/13496) identifies Aspergillus niger. These support the existing discrepancy; they do not establish which culture the study measured. No response hash is claimed for indexed text or failed requests. No new alias resolved either conflict.

The local supplement/archive metadata check also found no orientation for FMGX0057 versus FMGX0054. Both retain ATCC 9029 and ATCC 64974 as candidates. Equal member counts, shared display content, and shared genome namespace do not justify choosing an orientation. The bounded check stops here. Reopening those four rows requires an explicit source identity assertion or releasable provenance that resolves the conflict.

## Recheck record and schema

The TSV is UTF-8 with a header and ten uniquely keyed rows. `query_type` separates GCF and BGC. Pipe-separated acquisition IDs, columns, strains, conditions, and headers are ordered together. `massive_file_descriptors` holds both format-specific files for each acquisition, in acquisition order; the file entries themselves are manifest locators, not new downloads. Shared candidate sets intentionally occur in both unresolved FMGX rows and must be deduplicated before counting acquisitions.

`public_acquisition_label_status` concerns workbook labels and deposited filenames. `source_to_acquisition_status` asks whether the source member can be connected to those labels without a retained identity conflict. `metadata_readiness` means the documentary mapping is ready for packaging, not that a biological culture has been independently authenticated. `method_input_readiness` retains the remaining query-specific input work. Unresolved fields use explicit text rather than empty values; alias URL/hash fields are blank when no new external alias record was used. The new metadata table does not supply a scientific sign-off, native-scan join, or negative labels.

| Retained source or response | SHA-256 |
|---|---|
| [Publisher supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM1_ESM.pdf) | `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108` |
| [Publisher selected-family archive](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM3_ESM.zip) | `0cef389310eccd261255e51919e7fe5f1f772cc73be2b0d42e0f5f8e30245a54` |
| [Publisher feature workbook](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM4_ESM.xlsx) | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |
| Parsed [MassIVE depositor file manifest](https://massive.ucsd.edu/ProteoSAFe/dataset_files.jsp?task=a217f4ab6ba04103a71c6d4859538493) | `b03068e551c30835cd091a62088bb6597c5dd4a9dc66d9549156de12f0705f40` |
| Input sample-crosswalk.tsv | `69553d85647cc92784ebf49db50da46098da976b44c2bcf3edd15f286b2db79e` |
| Input pestalamide-source-members.tsv | `c90a5490355a3be0f52102b5e13f1c967b8c68eb57ba78ad458dea57ee85ebb3` |
| Fresh NCBI GCA_000011425.1 dataset report, 2 October 2026 | `5821f5d20926086d21b5814911b22c65885af3e947f256f6d4b4e9779b266df5` |
| Fresh FGSC A4 HTML, 2 October 2026 | `0b49da134aa460a7a7b64fbbf2646fcb83f582213afb3242634b85616c3e35de` |

The pestalamide assembly metadata URLs and hashes are carried forward from the nine-member roster; those seven NCBI assembly memberships were not newly revalidated here. Fresh response bytes, source-check receipts, and the rendered Figure 9 page are in ignored `data/interim/approved-query-inputs/`. PMC direct access returned a browser challenge, the Europe PMC full-text endpoint returned HTTP 500, and Nature's accessible page did not expose the needed methods. No version was inferred from these access failures.

Verification found ten unique metadata keys, all 30 public workbook joins, and all 60 exact deposit filenames. Six rows have usable mapping metadata: five pestalamide members plus the emericellamide acquisition group. Four pestalamide rows remain unresolved, spanning 12 distinct candidate acquisitions. These are metadata counts, not independently validated strains or new benchmark queries. The next input step is to resolve those source identities and freeze the declared GCF input scope; the BGC query separately needs its exact locus package and analytical release freeze.
