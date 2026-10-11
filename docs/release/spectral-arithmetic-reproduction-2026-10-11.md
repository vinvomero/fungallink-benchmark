# Reproduction from saved spectral classes

An isolated same-host workspace containing18 copied files reproduced all1,347 diagnostic candidate rows exactly:1,249 for6-MSA and98 for ilicicolin H. This includes380 numeric scores and967 unavailable-input rows. Saved class-count diagnostics, coverage, target scores and rank bounds matched. The [receipt](../../data/interim/spectral-arithmetic-reproduction-2026-10-11/receipt.json) records every copied file hash, interpreter, command and outcome.

The verifier reads frozen genomic classes, predicted spectral classes, coverage and the pinned class table. It checks input/output hashes, reconstructs every score, and checks the saved partial-rank arithmetic. It ran with Python `-I` from the isolated workspace. A deliberate first-candidate score change in that copy failed the output-integrity check; the original bytes were then restored. Production data were untouched.

Run `python -I scripts/verify_saved_spectral_diagnostics.py --root <restored-workspace>` after restoring the exact paths and hashes listed in the receipt. The verifier does not invoke the original diagnostic runners, spectral predictors, native tools or downloads. It cannot overwrite scientific outputs.

This closes the saved-class-to-linking-result reproduction step. It is not independent researcher/host replication, raw feature reconstruction, sequence annotation reproduction or a new run of the neural/SVM predictors. Those boundaries remain explicit in the paper. Missing inputs remain unavailable, and complete evaluated coverage stays11 relationships.
