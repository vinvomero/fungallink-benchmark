# Private phylogeny reconstruction candidate

This snapshot contains 116,782 hashed payloads used by the unchanged terminal audit: frozen numerical inputs, completed tree records, primary and recovery fit logs, selected-fit receipts, rankings, evaluations and code. `AUDIT-COPY.json` lists every payload hash and byte count. This is a private saved-fit reconstruction package, not a public release or an environment distribution.

The compressed archive SHA-256 is `16c763eeb86d3823a9ce6aba4a51892b9fd2fea7ea89ddca13cdcd586a1f04f0`. Its decompressed TAR SHA-256 is `1365b8d266b0dffd74bba68b2443d5fcb52da5a485aeedddf76e5bf19d01ac76`. Decompression was checked against the exact snapshot previously extracted, hash-verified and successfully audited.

## Reconstruct the saved results

Use a fresh directory on Linux-local storage. Check the archive SHA-256 before extracting. Allow at least 2 GB free space. From the extracted root, run:

```
python -S -B scripts/check_phylogeny_recovery_completion.py --root . --output terminal-audit.json
python -S -B scripts/export_phylogeny_paper_tables.py --root . --output reviewer-tables
```

Both commands are read-only with respect to scientific inputs and saved results. They write their requested outputs; use new output paths. The exporter repeats the terminal audit before writing 30 query rows, 54 product rows and six method summaries. Do not invoke the workflow or recovery runner to reproduce this saved-fit stage: those entry points launch native analyses.

The successful original interpreter was CPython 3.12.15, GCC 15.3.0, on x86_64 WSL2 Linux with glibc 2.43. The saved-fit checker uses the standard library. Exact equality is platform-sensitive: a Windows reconstruction differed at the last decimal of one probability. Preserve that discrepancy if encountered; do not relax tolerances. The original-environment receipt and isolated no-site check are supplied. No cross-platform numerical equivalence is claimed.

The passed audit covers 7,290 nonconstant query-feature pattern pairs, including 24 recovered pairs, complete candidate restoration and evaluation arithmetic. It does not reconstruct raw measurements or historical mappings, rerun BUSCO/MAFFT/IQ-TREE/BayesTraits, validate biological labels, establish optimizer global convergence or validate the phylogenetic model. Absolute historical paths in receipts are provenance; audit file reads use the extracted root.

All material stays private pending author-approved release scope. The archive retains source-dependent inputs and historical provenance; inclusion does not settle their public redistribution. No native executables or Python environment are supplied. This package complements the separate deterministic-core and saved-class spectral candidates.
