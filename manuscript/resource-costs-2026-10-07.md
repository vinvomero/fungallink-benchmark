# Measured computational costs

7 October 2026. The [machine-readable table](resource-costs-2026-10-07.tsv) transcribes retained receipts for completed numerical work and native-tool checks. It covers a measured subset of the benchmark workflow. It does not measure the complete cost of literature review, biological curation, public-input reconstruction, all data acquisition, the full marker batch, fungal tree inference or the phylogenetic comparator. No new analysis or native job was run to prepare this report.

The initial comparison contains five queries and 9,339 measured-feature candidates per query. Its 18 overlapping observation rosters and four deterministic methods produce 72 evaluations; they do not produce 72 independent biological datasets. Original scoring and its reproducibility rerun have separate receipts. The expanded analysis reused the 72 original rankings and changed the evaluated positive sets, so its short runtime cannot be reported as the cost of fresh scoring.

| Completed work | Wall seconds | CPU seconds | Recorded memory |
| --- | ---: | ---: | --- |
| Original 72 scoring/evaluation intervals (sum) | 55.603 | 55.188 | 199.16 MiB cumulative process peak |
| Later exact rerun of 72 deterministic outputs | 63.938 | NA | NA |
| Initial shared random computation, 4,000 repeats | 358.546 | 355.297 | 199.16 MiB cumulative process peak |
| Expanded gold with cached scores | 16.696 | NA | NA |
| Clean-source declared stages | 121.795 | NA | NA |
| Synthetic IQ-TREE component only | 5.783 | 5.653 | NA |

The random result was computed once and applied to the 18 equivalent candidate rosters. Its receipt reports `precision_achieved`: the maximum Monte Carlo standard error was 0.0008148165324141222 at 4,000 repeats, below the 0.001 tolerance. The configured maximum was 10,000 repeats; the computation converged before that limit. The 208,834,560-byte Windows process peak includes earlier work in the same process and is not an isolated memory requirement for random scoring. The clean-source run recorded 121.795 seconds and 216,760,145 logical bytes across its 38 listed output files. It used a separate clean checkout on the same host with cached source material, dependencies and retained curation. CPU time and peak RAM were not captured for that run. Its output total excludes the checkout, input cache, receipt itself and temporary files.

## Completed marker jobs

The following real-data jobs have successful execution and retained completion or verification receipts. Times come from their `/usr/bin/time` logs. The previously completed genome pilot is counted once, although the batch reused it. Native output bytes are sums of the retained native file manifests; archive sizes are the retained compressed files' logical lengths read from file metadata.

| Job | Wall minutes | CPU hours | Peak RSS MiB | Native output bytes | Archive bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| protein-pilot-GCA_000003125.1 | 2.151 | 0.1437 | 164.75 | 12923707 | 2145202 |
| protein-pilot-GCA_000011425.1 | 1.800 | 0.1214 | 165.09 | 11487712 | 1942460 |
| protein-pilot-GCA_000769745.1 | 2.491 | 0.1653 | 165.12 | 10603035 | 1904450 |
| protein-pilot-GCA_001890105.1 | 2.039 | 0.1363 | 165.14 | 10808884 | 1767890 |
| protein-pilot-GCA_002120325.1 | 1.844 | 0.1262 | 165.20 | 9833194 | 1677554 |
| genome-pilot-GCA_027569885.1 | 18.492 | 1.2189 | 933.96 | 1205701164 | 301740427 |
| completed-batch-GCA_001890905.1 | 2.088 | 0.1417 | 165.06 | 11063531 | 1797054 |
| completed-batch-GCA_027569015.1 | 25.468 | 1.6853 | 941.68 | 1224233416 | 317144183 |
| completed-batch-GCA_027569075.1 | 19.264 | 1.2691 | 930.37 | 1161606886 | 271524294 |

Five protein pilots took 107.98–149.47 seconds each. The later completed protein batch job took 125.30 seconds. The genome pilot and two completed new genome jobs took 1,109.53, 1,528.08 and 1,155.86 seconds, respectively. Their CPU totals were 4,388.00, 6,066.96 and 4,568.61 seconds. Each requested four CPUs on the documented eight-CPU, eight-GiB WSL host. The retained environment records BUSCO 6.1.0, HMMER 3.4, Python 3.12.15 and the dated lineage dataset; genome-mode receipts also record Miniprot 0.18-r281. CPU model was not documented in the inspected receipts. Two protein pilots fall outside the eventual batch population, so their costs must not be treated as completed work for that population.

This snapshot includes only the three new batch jobs with both `done.json` and an exit-zero execution receipt: GCA_001890905.1, GCA_027569015.1 and GCA_027569075.1. The inspected batch status was still running at 15:17:20 UTC, with GCA_027569055.1 active. Neither its partial files nor the live workflow establish completion. No process was stopped or restarted. Inference timings exclude download, compression and export verification. Wrapper elapsed times can exceed the GNU time interval, particularly in the polled batch runner; the table consistently uses the native timing log for these jobs.

## Measurement boundaries

Elapsed wall time is calendar time within the recorded timer; CPU time is consumed processor time. CPU-hours equal CPU-seconds divided by 3,600. GNU time's user and system times are added. Its maximum RSS field, labelled `kbytes`, is converted using 1,024 bytes per unit. This is a reported maximum resident-set statistic, not a measurement of total simultaneous memory across every child process. Windows cumulative peak working set and Linux RSS are different measurements and should not be compared as isolated method requirements.

Disk columns distinguish uncompressed logical native output bytes from compressed archive bytes. They are alternative representations, not an estimate of peak disk use; neither column is filesystem allocated space. All temporary-peak cells remain `NA`. Missing RAM, CPU, disk and hardware values also remain `NA`. GNU time filesystem I/O counters are not substituted for retained storage. No large data payload was hashed or read to estimate these costs.

The native tree smoke used six synthetic taxa, one marker and 500 sites. MAFFT 7.526, IQ-TREE 2.4.0 and Biopython 1.85 completed, but only the IQ-TREE component logged total time: 5.783 wall seconds and 5.653 CPU seconds on one thread. The complete-file manifest totals 42,128 bytes, excluding its own completion receipt. Neither the configured memory limit nor IQ-TREE's predicted memory requirement is observed peak RSS. Full-smoke duration and measured peak memory are unavailable. This small synthetic run cannot support a runtime projection for the fungal dataset.

No full-run projection is supplied: the completed subset does not establish the cost of the outstanding marker jobs, alignment, tree search or comparator. Monetary cost, electricity, environment setup, failed attempts and human review time were not measured for this table. The older [resource ledger](../planning/resource-estimate.tsv) separately records retrieval attempts, deposit-listing byte totals and a transfer scenario; those entries are not an end-to-end execution measurement and were not added to these times.

The TSV preserves receipt paths, software, units and scope for each row. Section S11 of [Supplementary Methods](Supplementary-Methods.md) links these two artifacts as the resource-cost supplement; no method score or existing results table was changed.

<!-- Requested authoring route: gpt-6-astra / medium. Actual serving receipt unavailable. Humanizer applied. -->
