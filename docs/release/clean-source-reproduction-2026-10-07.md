# Private clean source reproduction

This run rebuilds the numerical source-selected comparison from the cached publisher workbook and pinned curation inputs. It uses a new local Git source snapshot and a clean clone, with outputs written outside the checkout. It goes upstream of the earlier rerun from copied final inputs. It does not reproduce the biological adjudication or make the inherited historical mapping public.

The declared stages passed in 121.8 seconds from snapshot commit `df45051040ad58f9a7d9ddd78cf5cd9b5812220a`. All 20 output files across the four source stages matched exactly. The complete canonical released inputs matched, as did expanded gold with nine relationships across five queries. All four primary deterministic methods reproduced their full rankings and expanded evaluations exactly. A separate full-command negative control added one newline to a private test copy of the sample crosswalk; the driver rejected its changed fingerprint before creating outputs. See `receipt.json` and `negative-control.json` in the result directory.

The source snapshot and clone are under `scratch/clean-source-reproduction-2026-10-07/`. The separate `inputcache/` holds source bytes, curation tables, comparison references, and the existing dependency packages. Fresh results and the machine-readable receipt are under `data/processed/clean-source-reproduction-2026-10-07/`. Nothing was downloaded. No original release files were changed, and no main-repository commit was made.

## Commands and checks

To package a new run from this repository, where the named scratch and output directories do not yet exist:

```powershell
python scripts/reproduce_private_source.py --prepare .
```

To rerun the existing clean clone with its pinned cache, choose a fresh output directory:

```powershell
python -I scratch/clean-source-reproduction-2026-10-07/checkout/scripts/reproduce_private_source.py --run --cache scratch/clean-source-reproduction-2026-10-07/inputcache --output scratch/clean-source-reproduction-2026-10-07/repeat-output
```

The driver checks a clean checkout and every source/cache fingerprint before work. It runs the frozen original feature exporter, candidate builder, condition-summary builder and GCF-input builder. Every declared table and the draft input JSON must match its frozen SHA-256 and byte count exactly. It then changes only the documented track identity, serializes the release input JSON canonically and checks its full hash against the original release. This comparison covers all candidate vectors, source-membership vectors, candidate pools and query metadata.

Expanded gold is rebuilt from the pinned reviewed label table and query-group table. Its complete parsed JSON must equal the frozen nine-relationship gold. All four deterministic methods run on the rebuilt primary population. Their full parsed ranking results and expanded-gold evaluations must equal the frozen primary results exactly. No numerical tolerance is used. Monte Carlo and the other 17 observation rosters are not rerun here; the earlier 72-run result remains a separate receipt.

The driver stops on any differing fingerprint, vector, gold record, ranking or evaluation. Builder manifests can change when runtime/dependency metadata changes, so their bytes are recorded rather than compared to historical manifests. The tables and scientific inputs they describe are compared exactly.

## Input boundary

The public starting bytes are the cached Caesar publisher workbook, `41589_2023_1276_MOESM4_ESM.xlsx`, 19,251,141 bytes, SHA-256 `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb`. Its official locator and earlier retrieval checks are retained in the copied source registry and legacy-import registry. The workbook's 9,339 features remain intact; the published 9,301 count is not used to filter rows.

The sample crosswalk, observation grouping ledger, GCF population ledger and reviewed label/group tables are retained curation inputs. They are hashed and validated by the builders, but they are not generated anew from public evidence in this run. In particular, the population retains source-selected family membership and alias decisions informed by the historical author-workbook mapping. Its historical crosswalk is included only as provenance: 19,186 bytes, SHA-256 `d5b107a3c6c947a30cca8022b5357eef396fa3b33747314a84ac798d34d8cf99`. The FMGX-to-strain edge is not established as public. The original author-workbook bytes and a complete public derivation of those curation decisions are not supplied by this run. This prevents a claim of a wholly public source rebuild.

Frozen gold and primary result files in `inputcache/references/` are comparison references only. Builders never use them as source observations or labels. The expected stage hashes are taken from previously frozen manifests and checked against the retained originals before packaging.

## Environment and independence

The requested route was `gpt-6-astra` with `medium` reasoning. No serving-side receipt was exposed, so the actual serving model and effort remain unverified.

This is the same agent/researcher and Windows host, with a separate clean Git checkout and isolated Python imports. It is not an independent researcher or different-machine reproduction. `receipt.json` records the Python executable/version, platform, snapshot commit, timing, checked outputs and result status. The run uses one Python process and leaves the live BUSCO batch alone.

The first attempt failed before output construction because `python -I` could not find the existing user-site `openpyxl`. The correction copies the already installed `openpyxl` 3.1.5 and `et_xmlfile` package bytes into the separate cache and hashes every file. No new environment, installation or system change was made. The isolated scratch source received a second local commit, and the clone fast-forwarded to it before the affected stages were restarted. The initial failure is retained in `scratch/clean-source-reproduction-2026-10-07/initial-attempt-failure.txt`.

The checked-in dependency declaration pins `openpyxl==3.1.5`; the input manifest pins the actual package files, including the XML helper. Reusing that cache requires the recorded compatible Python runtime. The package remains private because public accessibility of source material does not establish redistribution rights.
