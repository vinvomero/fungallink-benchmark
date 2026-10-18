# FungalLink

Compare how well methods link fungal genes to measured products using the same inputs, candidate pools and supported answers. FungalLink provides curated relationships, ranking methods and saved results that you can inspect or reproduce.

**[Explore the evidence and results](https://fungallink-paper-explorer.vin-vomero-2210.chatgpt.site/)** · [Download data 1.0.0](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0)

By [Vin Vomero](https://orcid.org/0009-0005-1241-5849), Independent researcher. Updated 17 October 2026.

## What you can compare

The benchmark records 30 supported relationships across 16 biological query identities: 20 directly supported and 10 reference-supported. A query is a biosynthetic gene cluster or a defined gene-cluster family. Candidates are measured metabolite features, including signals whose chemical identity is unknown.

- **11 relationships** have complete evaluations through seven query views.
- **2 relationships** have partial spectral diagnostics.
- **17 relationships** lack usable comparison inputs.

The main comparison ranks 9,339 measured features for five queries. It preserves the original six-product evaluation and the later nine-target evaluation, both using 105 observations. A separate comparison uses the same 66 observations for all methods, including BayesTraits. The emericellamide and acetylaszonalenin family-view extensions are reported separately.

All complete evaluations belong to one source-selected cohort and one conservative analysis group. The results measure retrospective recovery of supported products; they do not establish performance on independent, unseen pathways.

## Current manuscripts and evidence

The [research website](https://fungallink-paper-explorer.vin-vomero-2210.chatgpt.site/#sources) provides the 17 October research manuscript, supplementary methods, accepted evidence qualifications, and a separate Scientific Data Data Descriptor with its supplement. These are prepared manuscripts. Neither has been submitted, and no Zenodo DOI has been assigned.

On 17 October, Vin Vomero personally reviewed and accepted qualified decisions for all 30 relationships and eleven evidence annotations. The website supplies the accepted annotation package separately from the frozen data release. Query identities, biological labels, target sets, readiness counts and reported scores are unchanged. AI-assisted evidence appraisal, automated checks and same-host reruns are disclosed; author acceptance is not independent specialist validation.

The latest manuscript release **tagged in this repository** remains [preprint 1.0.2](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.2). Its [paper](manuscript/preprint-2026-10-11/Manuscript.pdf), [methods](manuscript/preprint-2026-10-11/Supplementary-Methods.pdf), [comparative results](manuscript/preprint-2026-10-11/Comparative-results.pdf) and editable sources remain available. The newer website editions do not replace those release assets or data 1.0.0. The [13 October release addendum](RELEASE-ADDENDUM.md) records earlier verification and editorial corrections; its pending-review statement predates the author acceptance above.

## Download and reproduce

Download `fungallink-data-v1.0.0.zip` from the [data release](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0). Extract it into a fresh directory, open a terminal there and run:

```sh
python scripts/verify_public_release.py .
python scripts/reproduce_public_core.py .
```

The first command checks packaged files against `PUBLIC-MANIFEST.json`. The second checks the primary observation roster for the expanded target set and both family-view extensions. Core replay uses Python's standard library. A repository clone alone does not contain the full data release; use the ZIP for these commands.

To check all 216 method/roster combinations, use a new output directory:

```sh
python scripts/reproduce_public_core.py . --all-rosters --output public-core-all-rosters
```

The output directory must not already exist. These commands reproduce saved numerical results. They do not repeat biological review, predictor inference or native phylogenetic fitting.

For other stages, follow the [reproduction guide](docs/release/reproduction-stages-v1.md). The data ZIP includes four numerical/software component archives under `data/processed/`; extract each into a separate directory. Historical filenames containing `private` describe their preparation state. Those exact archives are now released under the accompanying notices.

Three third-party inputs must be obtained from their original sources:

```sh
python scripts/retrieve_public_dependencies.py .
```

This command retrieves and verifies the files listed in `UPSTREAM-INPUTS.json` without overwriting mismatched files. They support saved similarity calculations and the spectral class-table dependency. Saved phylogeny reconstruction requires the recorded Linux environment; the documented Windows last-decimal mismatch remains unresolved. Each stage's guide states what can be reproduced and which inputs it needs.

## Inspect the evidence

Use the [30-row traceability index](data/manifests/relationship-traceability-v1.tsv) and [mapping guide](docs/release/mapping-traceability-v1.md) to follow a released relationship to its evidence and evaluated targets. The [readiness guide](docs/release/relationship-readiness-v1.md) separates biological support from usable method inputs. The [similarity dictionary](docs/release/similarity-independence-v1.md) describes the chemical, genomic and spectral comparisons. Read the accepted qualifications on the website alongside these base-release records.

Unknown associations are not negative labels. Supporting evidence does not necessarily establish an exact chemical structure. Family views do not create new biological query identities, and the 18 overlapping observation rosters are sensitivity checks rather than independent test sets. Chemical similarity is available for five supported structures. Model-training overlap remains incompletely known, and the fixed-tree comparison retains its composition-test failures and optimizer-recovery history.

The historical sample-label-to-strain mapping used an author-supplied workbook and clarifications. Released reconciliations document that mapping, but it cannot be rebuilt entirely from public materials. Raw author workbooks, correspondence, publisher reading copies, predictor weights and third-party executables are excluded. See the [numerical source notice](docs/release/numerical-source-notice-2026-10-11.md).

## Acknowledgment

The author thanks Lindsay K. Caesar for generously answering questions by email, sharing the strain-label workbook, and clarifying sample identities and source data. Her assistance helped establish the connections between the published study and the records used in FungalLink.

## Licenses and citation

Original code is licensed under Apache-2.0; original curation, results and documentation under CC BY 4.0. Third-party materials retain their own terms and attribution. See [license scope](docs/release/licenses/SCOPE.md) and [third-party notices](THIRD-PARTY-NOTICE.md).

Cite Vin Vomero (2026), *FungalLink*, data version 1.0.0, with its [release URL](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0). Cite the manuscript edition you used separately, including its version or date. No DOI, bioRxiv posting or journal acceptance is claimed.

The published code baseline is commit [1533306af78701f66f5d35295d47f2010c085d71](https://github.com/vinvomero/fungallink-benchmark/tree/1533306af78701f66f5d35295d47f2010c085d71). Later documentation edits do not change that identity or the frozen data archive.
