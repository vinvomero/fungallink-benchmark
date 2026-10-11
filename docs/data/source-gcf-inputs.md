# Draft numerical inputs for source-selected GCFs

`scripts/build_source_gcf_inputs.py` turns the proposed source-study population and retained source-observation bundle into numerical inputs for five source-selected GCFs. It doesn't read biological gold, change admission decisions, or run a method. Successful construction leaves `analytical_release_ready=false` and `scoring_ready=false` in the manifest.

Run from the repository root with an explicit output directory:

```powershell
python scripts/build_source_gcf_inputs.py --source-dir data/processed/caesar-source-observations-v1 --population data/curated/caesar-source-gcf-population-2026-10-03.tsv --output-dir data/processed/caesar-source-gcf-draft-v1
```

The [population proposal](caesar-source-gcf-population-2026-10-03.md) declares 105 shared observations, five GCF queries, and 116 metadata rows. These are source-study observations, not 105 independent genomes. The builder uses the explicit population flag, checks its recorded denominators, and keeps every candidate in the source bundle, including unnamed features. It doesn't hardcode the real candidate or observation counts; synthetic fixtures exercise the same contract.

Each included observation takes the union of its exact recorded condition IDs. The condition heights already contain within-condition medians. The new height is their maximum, missing if any required condition height is missing. Presence is `1` if any condition is detected, `0` if every required condition is observed below threshold, and missing otherwise. An alias spanning disjoint media therefore keeps the condition medians. No averaging of label maxima, pooling acquisitions across media, normalization, or automatic assembly merging occurs.

The five queries are `source:NRPSPKS_85`, `source:TERPENE_40`, `source:NRPSLIKE_59`, `source:NRPKS_18`, and `source:NRPS_66`. A genomic-presence `0` means nonmembership in the fixed deposited source roster. It doesn't establish biological genomic absence. Unknown membership cannot enter an included column. Withheld rows remain visible with their explicit reason and original states.

| Output | Contents |
|---|---|
| `candidates.tsv` | All candidate IDs, m/z, and retention time; annotation fields are excluded. |
| `observations.tsv` | Every population row and its original metadata fields, including aliases, shared assemblies, provenance, full family rosters, and unresolved members. |
| `source-membership.tsv` | Every population ID, inclusion flag, disposition, and five membership states. |
| `observation-heights.tsv` | All candidates by included observation; raw heights, with empty cells for missing values. |
| `observation-presence.tsv` | The matching binary matrix, with empty cells for missing values. |
| `inputs.json` | Schema `"1"` input for `run_baselines.py`, containing only declared IDs, feature presence, and source membership. |
| `manifest.json` | Versions, source and output fingerprints, inherited provenance, rules, exclusions, limitations, and validation counts. |

`inputs.json` uses the baseline interface's `strain_ids` field for source-study observation IDs. This field name doesn't assert genome independence. `normalized_abundance` is omitted because the retained heights are raw. The existing global-abundance baseline consequently reports unavailable input. Gold answers remain external. Metadata and manifests are audit artifacts and should not be supplied as method features.

The builder verifies fingerprints and row counts for every source table it reads. It also checks the population's labels/conditions fingerprints against the supplied bundle, exact candidate and condition correspondence, complete observation partitioning, acquisition unions, valid membership states, and finite nonnegative heights. Presence must agree with the source threshold of 10,000,000. Historical evidence fingerprints embedded in population metadata are retained as provenance; the builder doesn't reopen or independently validate those upstream evidence files.

Rows and columns are keyed by IDs, so source ordering cannot change numerical alignment. The same input bytes and code produce the same output bytes without timestamps. Files are staged before replacement, and the manifest is published last, following the existing bundle builders. Source or validation failures before publication preserve existing outputs.

The synthetic tests use hand-calculated condition summaries, an unnamed candidate, explicit missing cells, a withheld identity, and deliberately permuted IDs. They check the public builder and CLI, baseline schema compatibility, annotation exclusion, fingerprints, and deterministic output. They don't calculate real-data scores or validate biological identities.

Release freezing, learned methods, sequence-defined BGC packaging, whole-cohort reconstruction, and publication remain outside this builder. Source selection, known-reference exposure, historical crosswalk authority, unresolved reuse rights, and assembly dependence still need to be carried into any later analytical release.
