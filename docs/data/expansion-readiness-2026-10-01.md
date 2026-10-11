# External-cohort input readiness

Checked 2026-10-01. This review advances the two expansion cohorts in the canonical benchmark plan by inspecting available measurement schemas and repository metadata. It admits no new labels. The number of independently evidenced, eligible relationships remains unknown for both cohorts; zero admissions from this review does not mean zero eligible relationships exist.

Requested execution route: `gpt-6-astra`, `medium` reasoning. No serving-side receipt was available, so the actual serving model and effort are unverified. The humanizer skill and CE Work knowledge-work instructions were applied. No source files, existing registries, or biological evidence packets were changed.

## A. fischeri has a concrete feature matrix

The [Figshare 25316452 chemistry workbook](https://ndownloader.figshare.com/files/48332083), version 1, contains two sheets. Direct inspection of the retained, checksum-verified file gives:

| Sheet | Measurement rows | Unique row keys | Numeric measurement columns | Numeric cells |
|---|---:|---:|---:|---:|
| Samples individual | 256 | 256 | 96 | 24,576 |
| Average biological | 256 | 256 | 32 | 8,192 |

Both sheets use `mz/RT` as the first-column header, followed by composite numeric row keys. They have the same keys in the same order. Every measurement cell is numeric and none is empty. There are no separate feature-number, scan, native-spectrum-ID, or annotation columns in these two sheets. Preserve the composite keys as opaque source identifiers until their component order and units are documented.

The individual headers contain 16 distinct strain strings, two condition suffixes (`30`, `37`), and three replicate suffixes per strain-condition group. Removing only the replicate suffix produces exactly the 32 averaged headers. All 8,192 averaged cells match the arithmetic means of the corresponding three individual cells within relative tolerance 1e-9 and absolute tolerance 1e-6. These are verified header and arithmetic relationships, not proof that each replicate is a separately acquired biological sample. Neither 96 columns nor 32 averages is an independent-strain count.

This establishes a 256-row deposited measurement pool. It does **not** establish that all detected features survived source filtering or that this is the full measured universe required by the benchmark. The two [Figshare manifests](https://api.figshare.com/v2/articles/25316452) and [analysis-code manifest](https://api.figshare.com/v2/articles/28380431) list no standalone MGF or mzML export. The chemistry workbook has no feature-to-spectrum join. The deferred 38,551,860-byte notebook was not inspected, so embedded data there remain unknown.

The companion assembly-metrics workbook contains 16 sections labelled `DTO1` through `DTO16`; chemistry uses collection-style strain labels instead. Their equal counts do not establish correspondence. No verified chemistry-to-versioned-assembly accession crosswalk was produced in this review.

[Steffen et al.](https://pubs.rsc.org/en/content/articlehtml/2026/ob/d5ob01965f) report 60 characterized metabolites across 16 strains, with 22 assigned to known pairs and 38 proposed associations. The method uses structural and genomic similarity. Those are source-reported assignments, not 60 independent experimental labels or 22 benchmark admissions. The paper's data-availability statement directs readers to Figshare 25316452 for the earlier measurements and 28380431 for the later analysis code. Reusing its predicted associations as evaluation truth would require a separate evidence review and exposure accounting.

Disposition: retain this cohort as a feature-only expansion candidate. The next bounded pass should document the 256-row selection history, establish the collection-label crosswalk, and determine whether an auditable spectrum export exists. If those remain unresolved after one source review, record the missing item and retain the matrix as a scoped source pool. Do not silently call it a complete untargeted candidate universe or replace measured-feature retrieval with structure retrieval.

## A. flavus needs an inspectable processed export

The retained [Zenodo 18670081 manifest](https://zenodo.org/records/18670081), version index 3, lists `554AF.mzmine4.output.zip` at 1,763,473,033 bytes, depositor MD5 `e72ea40fcbe8af594a8eae6f6f855a05`. Its contents remain uninspected. Two bounded HTTP tail requests on October 1, through the API content URL and the record download URL, returned HTTP 403. The API metadata retry also returned 403. No ZIP central directory or archive body was obtained. This is a failure of these access routes today, not evidence that the deposit lacks the claimed files.

The host's primary-source inspection of [Xie et al., Data availability](https://www.nature.com/articles/s41467-026-70721-8) found author-reported spectral data and abundance tables at eight MS2 thresholds in Zenodo, plus mirror plots for 355 metabolites. These claims identify useful export types; they do not verify the number of feature rows, usable scans, joins, or independent labels. The earlier acquisition pilot inspected the separate mirror-plot archive and found SVG files. A plot collection cannot substitute for the quantitative matrix or an auditable feature-to-spectrum table.

The paper identifies MSV000096910 and MSV000096982 as positive- and negative-mode deposits, respectively. Direct inspection of their retained depositor manifests gives:

| Deposit | Listed files | mzXML filenames | Other listed files |
|---|---:|---:|---:|
| MSV000096910 | 563 | 562 unique | 1 params.xml |
| MSV000096982 | 540 | 539 unique | 1 params.xml |

There are 535 shared mzXML filenames, 27 found only in the first deposit, and four only in the second. This is filename overlap across modes. File-content equivalence was not checked, and these counts cannot be added to obtain independent cultures or strains. The primary article's paired-omics section reports 544 strains after seven were filtered for quality; the deposited filenames and the archive's `554AF` name still need reconciliation against explicit sample metadata.

Feature-row count, full candidate-pool coverage, sample-to-assembly matches, and the integrity of any feature-to-spectrum identifiers are unknown until the processed archive can be inspected. The exact MZmine 4 version and export settings are also unverified. Independently experimentally supported labels have not been counted. Association scores, including NPLinker outputs, cannot establish independent truth for evaluating the same method.

Disposition: retain as a processed-data expansion candidate with an access dependency. The next bounded pass should obtain only the ZIP directory and small metadata/table headers through a working public route, then compare feature IDs, sample columns, mode labels, threshold variants, and spectrum identifiers. Pick and document a candidate universe before comparing methods; eight threshold exports are not eight independent cohorts. Stop after that access/schema pass if the same dependency persists, and record the precise missing export rather than downloading all raw acquisitions.

## Verification record

The chemistry workbook is retained at `data/raw/sources/metadata/figshare-25316452--6_Chemistry_raw.xlsx`, SHA-256 `6c0c0ddab2d4a15b9b82f0f65510beaf12e21feea5f05c82c3d8fbfcbaf80bba`. OpenXML inspection and an independent openpyxl read agreed on dimensions and key counts. Averaging was checked by header-based grouping, not column position. Readiness counts are also recorded in `data/curated/expansion-readiness-2026-10-01.tsv`.

MassIVE counts came from `MSV000096910-file-manifest.json` and `MSV000096982-file-manifest.json`, whose provenance and hashes are already in `data/manifests/sources.tsv`. Primary article claims are distinguished above from payload inspection. Neither source has a validated spectral track or admitted label set on the evidence inspected here. Method training exposure, reference overlap, and redistribution rights still require their own review before a release.
