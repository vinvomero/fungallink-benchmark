# Private spectral candidate, version 1

The [archive](../../data/processed/spectral-release-candidate-v1-2026-10-11/fungallink-spectral-private-candidate-v1.zip) is built and verified. It contains 77 proposed inventory files, 14 supporting source files, a current-status README and an external-dependency map. The 93 payload hashes are recorded inside the archive. SHA256: `15e0f109e618df4a1645e1e2c4649a277e5bae9d954c4443a91c7aae5c549857`; size: 588,884 bytes.

The wrapper distinguishes current admissions from historical candidate-only and not-ready fields. Frozen files retain their original bytes. The pinned class table remains an external dependency, with its retrieval recipe included. Predictor weights, raw acquisitions and original environments are outside this candidate. Original-contribution licensing and public release remain owner decisions. No publication occurred.

After extraction into a separate directory, all 93 hashes passed. Restoring the exact retained external table allowed the included verifier to reproduce all 1,347 candidate rows: 380 scores and 967 unavailable-input records, with matching partial-rank bounds. This used the saved predictions on the same host. It did not rerun predictor inference, raw processing or biological adjudication.

- [Build receipt](../../data/processed/spectral-release-candidate-v1-2026-10-11/build-receipt.json)
- [Extraction and reproduction receipt](../../data/processed/spectral-release-candidate-v1-2026-10-11/extraction-verification.json)
- [Builder](../../scripts/build_spectral_release_candidate.py), which refuses an existing destination

This candidate covers the two partial spectral diagnostics. The Caesar benchmark, phylogeny comparison and complete paper remain separate work. Eleven relationships still have complete evaluated coverage; packaging these diagnostics does not increase that count. Next, integrate the completed phylogeny results after the terminal audit, then build the full private paper package with its own release scope.
