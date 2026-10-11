# Trichoderma network processing with MZmine 3.9.0

The authorized alternative run produced a complete 98-row processed candidate pool across the two deposited TIMS-off acquisitions, with 91 exactly joined MS/MS exports. This is a new MZmine 3.9.0 candidate universe. It is not the recovered historical MZmine 4.0.3 matrix, the 16-sample TIMS metabolomics matrix, or a biological admission.

## Software and declared deviation

The [official MZmine 3.9.0 release](https://github.com/mzmine/mzmine/releases/tag/v3.9.0) was published on 21 August 2023. Its [tagged license](https://github.com/mzmine/mzmine/blob/v3.9.0/LICENSE.txt) is MIT. All required module classes were present in the tagged source, and the inspected processing implementations call their tasks without account checks. The unmodified Windows portable package is 318,746,583 bytes, SHA-256 `d10424038b7bd63c910c1345b60d09b315d87fca91d0314ba658ee990ac2b08c`; it runs with its bundled Java 20.0.1. Package retrieval, license and source receipts are retained. No account, signup, payment or external submission was used. The failed 4.0.3 installation and logs remain untouched.

The source batch's processing thresholds were retained. Changes were native TSF import, local outputs, disabled website/folder opening and an extra ALL-row export. GNPS submission was already false and stayed false. The copied batch header was changed to the declared execution version 3.9.0; it originally specified 4.0.3. Thus the loader's same-version message describes the copied recipe header, not proof of original-source compatibility.

Two source parameters are unsupported by 3.9.0 and were explicitly reported by the loader: `Never remove annotated rows=false`, and metaCorrelate's `Advanced` block (`Keep extended stats=false`; `Simplify for ≥ samples=250`). Correlation grouping reports source parameter version 3 against implementation version 2. These unsupported settings were ignored by 3.9.0. Numeric detection, alignment and filtering thresholds were not tuned, and the result is not claimed equivalent to 4.0.3. Both initial and project-save runs completed all steps with exit 0 and populated outputs.

## Candidate pool and reproducibility checks

The raw inputs are `Molecular Networking_OE_timsOFF.d` and `Molecular Networking_diliE_timsOFF.d`, 182 files totaling 682,009,092 bytes. Their exact source sample IDs and analysis UUIDs are in the 18-row acquisition TSV; these two acquisitions are not independent fungal genomes. The other 16 TIMS acquisitions were not processed.

The source recipe aligned 110 rows. Its unchanged RowsFilter step retained 98, including its isotope validation rule and exemption for features with MS2. `aligned-row-removals.tsv` records the 12 removed row IDs. Gap filling, duplicate handling and correlation grouping retain 98 final rows. `pipeline-featurelists.json` preserves stage counts and IDs. This full pool is defined after the declared source filters; it is not an unfiltered inventory of every raw ion signal.

The full CSV contains 98 unique native export IDs and 196 finite, nonnegative peak-area values. The source-style `MS2 OR ION IDENTITY` export has 91 rows, so it must not replace the full pool. Seven full-pool features lack exported MS/MS: 4, 15, 20, 34, 38, 41 and 67. Their lack of spectra is not a negative biological label.

A second run added only a referencing-project save and wrote to a separate directory. Every feature ID, m/z, retention time and area value agrees exactly, and both runs' MGF files are byte-identical. Correlation-group numbering and partner ordering differ, so byte-level reproducibility is not claimed for those fields or the graph files. Original export files are preserved.

## Native spectrum membership

The saved project supplies 1,097 feature/acquisition/MS2 membership records. `Scan.saveScanToXML` stores zero-based positions in the imported raw scan list. The pinned TSF importer iterates the Frames table, which has contiguous frame IDs in both retained databases; `native-fragment-membership.tsv` records the resulting exact native frame IDs, event RTs, precursor trigger masses, isolation widths, collision energies and parent frame IDs. This mapping is backed by the project XML and raw SQLite records, not inferred from m/z proximity.

The source recipe disables spectral merging. The pinned GNPS exporter selects `getMostIntenseFragmentScan`, which compares the best fragment of each sample by MS level and then descending raw TIC/point count. A direct read with the vendor TSF library bundled in the unmodified 3.9.0 package reproduced the selected spectrum for every exported row. After the declared MS2 intensity threshold of 100, all 91 spectra have the same peak count and exactly match their exported m/z and intensity values at four decimals and two significant digits, respectively. Intensities use half-up tie rounding, including 1050 to 1100. `selected-native-spectrum-check.json` and `verify_native_membership.py` preserve that check. This is a same-worker validation, not independent scientific review.

MGF `FEATURE_ID` joins exactly to the row ID. MGF `SCANS` repeats that feature ID; it is not a native scan number. MGF RT is the row-average chromatographic RT, which can differ from the selected scan's event time.

As a diagnostic for the companion H appraisal, row 30 has m/z 434.23256913309 and row RT 5.8394184 minutes. Its selected spectrum comes from OE frame 5086 (project index 5085), RT 350.131789 seconds, precursor trigger mass 434.23280273521453, collision energy 20, with 241 retained peaks. Same-mass competing rows 35, 43 and 64 occur at 6.3057547, 6.570394 and 8.224282 minutes. These measurements support an evidence review; they do not alone establish identity. No processing choices used those product targets.

## Saved records

`data/raw/trichoderma-measurements-2026-10-07/processing-mzmine390/` contains the original outputs, referencing project, final feature-list XML, membership tables, validation receipts, commands, both recipes/logs, source/license receipts and a SHA-256 manifest. The large portable package and raw acquisition directories remain under `scratch/trichoderma-processing-pilot-2026-10-07/`; their retrieval manifests preserve locations and hashes. The referencing project needs those paths to reopen, while the exported data and membership records are independently readable.

Requested model/effort: gpt-6-astra/medium. Actual serving receipt unavailable. No method training/reference exposure assessment, ranking, query admission or candidate-release freeze was performed in this acquisition unit.
