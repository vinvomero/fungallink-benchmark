# FungalLink

A curated benchmark for linking fungal biosynthetic gene clusters and gene-cluster families to measured metabolite features.

**Data 1.0.0; preprint 1.0.2.** Documentation updated 13 October 2026. There are 30 admitted relationships across 16 biological query identities: 20 directly supported and 10 reference-supported. Eleven relationships have complete evaluated inputs for the declared co-occurrence workflows through seven query views; two have partial spectral diagnostics and 17 lack usable comparison inputs. All complete evaluations share one source-selected cohort and one conservative analysis group. This is a retrospective benchmark, not an independent held-out test.

Read the [LaTeX preprint](manuscript/preprint-2026-10-11/Manuscript.pdf), [Supplementary Methods](manuscript/preprint-2026-10-11/Supplementary-Methods.pdf) and [comparative results](manuscript/preprint-2026-10-11/Comparative-results.pdf). The [release addendum](RELEASE-ADDENDUM.md) records the verified public download and editorial corrections.

## Download and start

Download `fungallink-data-v1.0.0.zip` from the [versioned release](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0). Extract to a fresh directory and run:

```sh
python scripts/verify_public_release.py .
python scripts/reproduce_public_core.py .
```

The first command verifies every packaged payload against `PUBLIC-MANIFEST.json`. The second extracts the immutable core package to a new directory and checks the primary roster for the expanded target set and both family-view extensions. Add `--all-rosters` for the 216 method/roster combinations. Neither command performs new biological adjudication, predictor inference or native phylogenetic fitting.

Read [relationship traceability](docs/release/mapping-traceability-v1.md), [input readiness](docs/release/relationship-readiness-v1.md) and [reproduction stages](docs/release/reproduction-stages-v1.md). The [30-row traceability index](data/manifests/relationship-traceability-v1.tsv) connects ledger IDs, evidence, decisions and evaluated targets. The [similarity dictionary](docs/release/similarity-independence-v1.md) explains the bounded chemical, genomic and spectral comparisons.

## Additional reproduction stages

The data ZIP includes four unchanged numerical/software component archives under `data/processed/`. Historical filenames containing `private` describe their preparation state; those exact bytes are now released with the notices here. Extract each nested archive into a separate directory. Core replay uses only Python's standard library. Saved spectral arithmetic requires the hash-pinned upstream association table. Saved phylogeny reconstruction requires the recorded Linux environment; the retained Windows last-decimal mismatch remains documented. See the stage guide for commands and exact boundaries.

Three third-party input files are intentionally obtained upstream. Run `python scripts/retrieve_public_dependencies.py .` to fetch and verify the paths in `UPSTREAM-INPUTS.json`. Existing mismatched files are never overwritten. This supports the saved similarity stages and the class-table dependency; it is not a raw-to-fit acquisition pipeline. Download-only dependencies retain their upstream terms.

The Git repository contains code, documentation, curation and selected records. The full data ZIP supplies larger scientific inputs and nested reconstruction packages. Use the ZIP for execution; a clone alone is not the full data release. Evidence crosswalks distinguish bundled, upstream-retrievable and omitted historical source records. Raw author workbooks, correspondence, publisher reading copies, predictor weights and third-party executables are not distributed.

## Scientific limits

Unknown associations are not negative labels. Evidence class does not imply exact chemical structure or complete method inputs. Family-view transformations do not add biological query identities. The 18 overlapping observation rosters are sensitivity populations, not cross-validation folds. Chemical similarity is available for five supported structures; model-training overlap is incompletely known. The fixed-tree comparison retains its composition-test failures and optimizer-recovery history. Numerical agreement does not establish biological correctness or independent scientific validation.

The source label-to-strain bridge used a historical author-supplied workbook and clarifications. Project-generated reconciliations and documented inferences are released; wholly public reconstruction of that bridge is not claimed. See [the numerical source notice](docs/release/numerical-source-notice-2026-10-11.md).

## Licenses and citation

Original code: Apache-2.0. Original curation, results and documentation: CC BY 4.0. Underlying source materials retain their terms and attribution; these licenses are not a grant over third-party assets. See [license scope](docs/release/licenses/SCOPE.md) and `THIRD-PARTY-NOTICE.md`.

Cite Vin Vomero (2026), *FungalLink*, version 1.0.0, with the release URL. No DOI or journal acceptance is claimed. The LaTeX preprint and supplements are supplied in `manuscript/preprint-2026-10-11/` with matching editable sources. AI assistance and the absence of independent specialist re-adjudication are disclosed in the manuscript. This repository release is not a bioRxiv posting or journal submission.

The current reading edition is [preprint 1.0.2](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.2); cite it separately from data 1.0.0. The published code baseline is commit [1533306af78701f66f5d35295d47f2010c085d71](https://github.com/vinvomero/fungallink-benchmark/tree/1533306af78701f66f5d35295d47f2010c085d71). Later documentation edits do not change that code identity. The journal revision is an unpublished candidate. Historical private-candidate wording inside the frozen ZIP is superseded for current access by this README and the release addendum.
