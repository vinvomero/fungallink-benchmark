# Caesar study roster, 2 October 2026

The [roster](../../data/curated/caesar-study-roster-2026-10-02.tsv) accounts for every row of Supplementary Table 2 and every workbook strain label. It contains 110 source-study rows and seven unmatched workbook-label rows, including the blank control. This is a documentary cohort census. It does not approve biological labels, establish historical culture identity independently, or freeze an analytical release.

Requested route: `gpt-6-astra`, `medium` reasoning. The parent dispatched this knowledge-work unit through that route; no serving-side model/effort receipt was exposed to this unit. The complete canonical benchmark plan was read, including the identifier and observational-unit requirements in Phases 1 and 3. Humanizer rules were applied; its referenced `references/signs-of-ai-writing.md` file is absent from the installed skill.

## What was joined

[Supplementary Table 2](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM1_ESM.pdf) occupies PDF pages 4, 5, and 6, printed pages 3, 4, and 5. The pages contain 38, 43, and 29 data rows respectively. All three rendered pages were visually checked against the retained text extraction. The table supplies organism, strain label, accession or genome namespace, and repository. Its accession strings remain exactly as printed: versioned GCA/GCF values, unversioned WGS project strings, and JGI namespaces are separate kinds of assertion. The printed `JCBI`, taxonomic spellings, and `ATCC 13490` are preserved.

The [publisher workbook](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM4_ESM.xlsx), Sheet1 rows 6, 7, and 8, supplies the strain label, condition, and acquisition header. Every one of its 362 acquisition columns was checked against the existing crosswalk. Blank Excel condition cells are represented as empty strings. The observation-group ledger independently reproduced the crosswalk's label-condition acquisition counts.

The deterministic joining rule removes spaces and punctuation and compares letters without case, while retaining every collection code, letter, and numeric digit. For example, `CBS 172-66` matches `CBS172.66`; a species name cannot substitute for a strain identifier. Comma-separated strain numbers in a single Table 2 row are explicit source co-listings and are recorded as source aliases. No external alias was needed to obtain the cohort-wide counts. Raw labels and source row text remain available beside the normalized join result.

## Reconciliation

| Population | Count |
|---|---:|
| Table 2 source-study rows | 110 |
| Workbook nonblank literal strain labels | 116 |
| Workbook literal blank label | 1 |
| Table 2 rows with a matching workbook identifier | 108 |
| Distinct workbook literals matched to those rows | 110 |
| Matched candidate acquisitions | 335 |
| Nonblank unmatched workbook labels / acquisitions | 6 / 16 |
| Blank acquisitions | 11 |
| All workbook acquisitions accounted for | 362 |

The difference between 110 matched workbook literals and 108 matched Table 2 rows comes from spacing variants: `ATCC 96836` and `ATCC96836`, and `ATCC 38873` and `ATCC38873`. The 116 nonblank literals therefore decompose into 110 matched literals plus six unmatched ones. The 110 source rows decompose into 108 matched rows plus two missing identifiers. These counts do not estimate independent genomes.

`W1` and `ATCC MYA409` have no exact or explicit-alias workbook match. `Kabbage_A.brassicicola` remains an unmatched label; the species resemblance does not establish that it is W1. Other unmatched labels are `ATCC48694`, `NRRL1061`, `NRRL4593`, `NRRL4904`, and `NRRL66628`. All have three workbook acquisitions except NRRL4593, which has one. No mapping was inferred from similar numbers, species, accession reuse, or equal sample counts.

Of the 108 matched source rows, 105 have all three literal conditions, Cheerios, Oats, and Rice. NRRL4539 has Cheerios and Rice; NRRL2393 has Oats and Rice; NRRL89 has Cheerios and Oats. NRRL89 includes three Oats acquisitions and one Cheerios acquisition. Those observations remain as recorded and do not become extra strains. A map-only NRRL2393 Cheerios acquisition is listed separately and contributes no workbook measurement.

## Proposed eligibility scope

Apply one source-assertion rule to the full cohort: a Table 2 study row with an unambiguous identifier or explicit table-alias match to at least one workbook acquisition is a candidate for the documentary cohort. Preserve all matching conditions and acquisitions and flag known identity conflicts. This yields 108 candidate study rows and 335 acquisitions, of which 106 rows have no retained identity conflict in the reviewed metadata and two carry explicit conflicts. The latter wording does not imply that the other 106 rows have undergone independent culture authentication.

This rule does not select samples because they support a known product. The six previously usable public query-metadata rows are linked as extra evidence where applicable, but their membership is not an inclusion requirement. All source-study rows were processed under the same lexical rule. Scientific eligibility and method readiness remain separate fields with `not_assessed` and `not_established_by_this_roster` values. No category is called a verified genome.

The existing metadata retains two identity discrepancies: the study's ATCC13490 versus deposited ATCC13496, and ATCC64048/A1/83 versus deposited A1. Both exact documentary joins remain visible, with `candidate_source_asserted_with_identity_conflict` status; neither conflict is repaired by spelling substitution. Any future analytical release must decide their treatment explicitly.

ATCC16872 and CBS172-66 share the printed GCA_001890905.1 assertion but remain different Table 2 rows. ATCC9029 and ATCC64974 share Aspni_NRRL3 and also remain separate rows. The earlier approved-query metadata reports that FMGX0057 and FMGX0054 cannot be oriented between those latter two study rows. This roster resolves neither orientation and does not double-count their overlapping query-specific candidate sets. The GCF member-to-study-row mapping remains a separate task.

No family membership zeros, absence-of-gene claims, comparative scores, new scientific approvals, or release freeze were produced. The study roster alone cannot decide whether a missing family member means nonmembership. Any historical family-membership interpretation must be recorded separately before analytical inputs use it.

## Fields and checks

`source_table_row` numbers Table 2 data rows across all three pages; `source_page_data_row` restarts on each page. `source_row_text` retains the extracted full row. `source_aliases_json` stores the table's comma-separated co-listings. All list-valued fields use JSON, including raw map labels/accessions, acquisition IDs, columns, shared-assembly row IDs, and extra query-metadata links. Ordered acquisition IDs, columns, and stems refer to the same crosswalk rows. `media_counts_json` counts workbook acquisitions, not replicates whose hierarchy has been resolved. Empty source fields on the seven workbook-only rows mean no Table 2 correspondence was accepted.

Checks passed: 110 parsed Table 2 rows; 362 exact workbook-to-crosswalk metadata triples; equality of all workbook label-condition counts with the observation ledger; no workbook literal assigned to two Table 2 rows; 362 acquisitions accounted for exactly once; raw source files left unchanged. Source images and one-off extraction/check scripts are in ignored `data/interim/caesar-study-roster/`. No reusable software or other curated ledgers were changed.

| Retained input | SHA-256 |
|---|---|
| Publisher supplement | `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108` |
| Publisher workbook | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |
| sample-crosswalk.tsv | `69553d85647cc92784ebf49db50da46098da976b44c2bcf3edd15f286b2db79e` |
| caesar-observation-groups-2026-10-02.tsv | `70c74e3b0dbdcd5a1cc5dcd81bed59cb301036b0c7b109740bc9301cb2266e0c` |
| approved-query-inputs-2026-10-02.tsv | `8b7192312b0c6121248219319b709f9f1fa06adebaa14422fc1a3cfbf552cc6f` |
| Output caesar-study-roster-2026-10-02.tsv | `396838ef6097c33eaf32947047c808667d7d046b1d1190294acb199164fe37fb` |
