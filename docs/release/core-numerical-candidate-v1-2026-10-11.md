# Executable private core candidate

The [archive](../../data/processed/core-numerical-candidate-v1-2026-10-11/fungallink-core-numerical-private-v1.zip) reproduces the deterministic numerical stages for all 11 completely evaluated relationships. It includes the expanded five-query comparison and the two separately reported family-view extensions. All 216 method/roster combinations reproduced their complete rankings and evaluation objects exactly after extraction into a separate directory.

Each comparison supplies 18 frozen rosters, four deterministic workflows, gold labels, numerical inputs, frozen code and expected outputs. The package preserves selected source bytes and maps their original paths in `MANIFEST.json`. Expanded gold uses the original unchanged five-query rankings. No frozen source was modified.

The archive has 459 members, including its manifest, and occupies 39,957,780 bytes. SHA256: `61ddcc9245279255b5eaf486322cd8c22d558b088683c390be7cdda004dc1ed9`. All 458 payload hashes passed. The extracted replay took 253.861 seconds with Python 3.13.5, isolated imports and site packages disabled. A newline change in an extracted input was rejected before scoring; the original bytes were restored. That check did not touch production inputs.

- [Build receipt](../../data/processed/core-numerical-candidate-v1-2026-10-11/build-receipt.json)
- [All-roster reproduction receipt](../../data/processed/core-numerical-candidate-v1-2026-10-11/reproduction.json)
- [Changed-input check](../../data/processed/core-numerical-candidate-v1-2026-10-11/negative-control.json)
- [Builder](../../scripts/build_core_numerical_candidate.py)

After extraction, run these commands from the extracted root:

```
python -I -S -B expanded/reproduce.py --all-rosters
python -I -S -B emericellamide/reproduce.py --all-rosters
python -I -S -B acetylaszonalenin/reproduce.py --all-rosters
```

Omit `--all-rosters` for a primary-roster check. No external data, installed scientific packages or neighboring repository is needed for this numerical stage. The archive README defines the input boundary and public-release limits.

This is same-host automated replay, not independent researcher validation or reconstruction of raw measurements, historical mappings or biological labels. It does not rerun Monte Carlo, spectral predictors or the separate phylogeny workflow. The 18 overlapping rosters are sensitivity populations, not independent replicates. Public release provenance and original-contribution licenses remain separate decisions; this private archive does not resolve them. The full manuscript package still needs terminal phylogeny results and final author review.
