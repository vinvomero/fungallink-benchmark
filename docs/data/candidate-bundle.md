# Acquisition-level candidate preparation

`scripts/build_candidate_bundle.py` prepares method payloads from the existing Caesar source-feature export. It removes source annotations through explicit column whitelists and keeps every candidate and acquisition. This is candidate preparation for the comparative benchmark, not a frozen analytical release.

```powershell
python scripts/build_candidate_bundle.py --source-dir data/processed/caesar-feature-source-v1 --output-dir data/processed/caesar-candidate-bundle-v1
python -m unittest tests.test_build_candidate_bundle -v
```

The library entry point is `build(source_dir, output_dir)`. It requires a complete `source_feature_export` manifest at schema version 1, verifies all three payload hashes and byte counts, and checks rectangular tables, unique IDs, row correspondence, acquisition columns, and declared counts before writing output. It checks the source bytes again before publication. Source and output directories cannot overlap.

| File | Fields and preservation rule |
|---|---|
| `candidates.tsv` | Exactly `candidate_id`, `row m/z`, `row retention time`, in source feature order. |
| `abundances.tsv` | Exact source bytes, including all candidate IDs and acquisition columns. Zero and empty fields remain distinct. |
| `acquisitions.tsv` | Exactly `acquisition_id`, `cohort_id`, `sample_role`, in source metadata order, including map-only acquisitions. |
| `manifest.json` | Output hashes and counts, source-manifest hash and byte count, generator hash/version, Python version, preparation rules, and release limitations. |

No row identity, source alias, workbook coordinate, or curated free-text note is copied into the method payloads. Candidate IDs still expose public source IDs. Annotation removal cannot erase prior exposure or support a claim of unseen-pathway generalization.

The current source manifest declares 9,339 features, 362 abundance columns, and 363 acquisition metadata rows, including one map-only acquisition. The builder preserves that universe; it doesn't select named features. It carries forward the unresolved difference between the published count of 9,301 and the observed 9,339 rows. These are source counts, not independently validated biological labels or independent query counts.

Abundances remain raw and unnormalized. There is no aggregation, filtering, imputation, presence rule, or conversion of acquisitions into independent genomes. No queries, positives, or biological admissions are created, and `analytical_release_ready` remains `false`. Preprocessing, observational-unit decisions, scored queries, and analytical release construction are outside this unit.

Files are staged before publication, with the manifest replaced last. A failed validation leaves an existing bundle unchanged. Publication is per-file rather than one atomic directory swap; an interrupted replacement can leave mixed payload versions, which consumers must reject by checking every hash against the manifest. Use a dedicated output directory and distribute only the four declared files.

Tests use small fixtures with shuffled public IDs, an unnamed feature, an annotation canary, zero and missing abundances, and a map-only acquisition. They also exercise the CLI, repeatability, hash rejection without changing existing output, inconsistent keys and dimensions despite updated hashes, and path collisions. Real-data export and verification are separate from these tests.
