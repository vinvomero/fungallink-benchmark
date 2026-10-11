# FungalLink presubmission release map, version 1 with similarity delivery update

The current private container is `fungallink-presubmission-release-v3.zip`. It adds the completed similarity companion, its inputs and provenance, and revised manuscript/release documentation. Frozen v1 and v2 containers remain retained. Every inherited scientific input, score, evaluation and nested archive remains byte-identical to v2; changed inherited manuscript/documentation paths and new payloads are listed in the v3 build receipt. Start with the [mapping traceability guide](mapping-traceability-v1.md) to inspect each connection and its source links.

This private candidate collects the revised Data Descriptor, current curation and readiness records, source evidence decisions, and three preserved numerical reconstruction packages. It is prepared for human scientific review. No external download, public deposit or submission has been verified.

The benchmark has 30 admitted relationships across 16 ledger query identities. Eleven relationships have complete evaluated coverage, two have partial diagnostics, and 17 lack usable expression-screen inputs. Complete results cover seven query views in one conservative source-selected analysis group. These counts describe different units.

## Read and extract

Verify `fungallink-presubmission-release-v3.zip` with the included, unchanged `scripts/verify_private_review_archive.py`, then extract into a fresh directory. `REVIEW-MANIFEST.json` records the size and SHA-256 of every outer payload. The adjacent `build-receipt.json` identifies the outer ZIP itself. Verification checks bytes and membership, not biological correctness.

Start with [the paper](../../manuscript/benchmark-paper-review.md), [Supplementary Methods](../../manuscript/Supplementary-Methods.md), and [the reproduction guide](reproduction-stages-v1.md). The rendered Word/PDF files accompany the Markdown. [Comparative results](../../manuscript/comparative-results-v1.md) retain detailed interpretation. [Scientific review](../../manuscript/scientific-review-v1.tsv) records pending accountable human judgments; automated record checks do not fill those fields.

Nested packages must be extracted into separate fresh directories. They retain their original bytes and historical status. Never extract one package over another or over this outer directory.

| Component | Archive within this release | Payloads and use |
|---|---|---|
| Core version 1 | `data/processed/core-numerical-candidate-v1-2026-10-11/fungallink-core-numerical-private-v1.zip` | 458 payloads; frozen numerical input to deterministic rankings/evaluations, 216 method/roster combinations across three tracks |
| Spectral version 1 | `data/processed/spectral-release-candidate-v1-2026-10-11/fungallink-spectral-private-candidate-v1.zip` | 93 payloads; saved-class arithmetic for 1,347 rows, requiring the separately pinned class table |
| Phylogeny version 1 | `data/processed/phylogeny-audit-candidate-v1-2026-10-11/fungallink-phylogeny-audit-private-v1.tar.gz` | 116,782 payloads; reconstruction of 7,290 saved pattern pairs and evaluations using the recorded Linux environment |
| Software review candidate | `data/processed/release-review-candidate-2026-10-07/fungallink-software-review-candidate.zip` | Synthetic fixtures and adapter demonstration; not an additional biological task |

Nested manifests/checksums and adjacent original build receipts provide the component identities. [Reproduction stages](reproduction-stages-v1.tsv) give the actual commands, boundaries, comparison rules and retained runtimes. Predictor inference, raw measurement processing and native tree/model fitting are separate stages; bundling their outputs does not reproduce those stages. Exact phylogeny reconstruction uses the [recorded environment](environment/phylogeny-linux-explicit.txt). The original Windows last-decimal failure remains part of the evidence.

## Files and joins

The outer archive preserves project-relative paths. `manuscript/` contains the paper, figures, tables, supporting results, claims, references and disclosure. `docs/evidence/` and `protocol/` contain original curation and decision records. Selected numerical checks and retrieval receipts remain at their original `data/interim/` or `data/raw/` paths; those path names do not change their content into raw publisher payloads. Source articles, copied supplements, source workbooks, private correspondence and predictor weights are excluded. The project-state checker, its targeted tests, amendment records and execution receipts are retained as audit evidence for the exact provenance-only ledger change. They require global operational planning records for a full repository check and are not a standalone advertised workflow in this package. The numerical stages in the reproduction guide define the runnable scope.

Join [readiness](../../data/curated/relationship-readiness-v1.tsv) to the authoritative [ledger](../../data/curated/label-evidence.tsv) on `relationship_id`. Join the human review table on the same key. `query_id` is the biological ledger identity; `evaluation_query_view` can identify a separately declared family representation. Do not combine those into a larger independent-query count. The [readiness dictionary](relationship-readiness-v1.md) documents all fields. [Task exposure](../../data/manifests/task-exposure-v1.tsv) records task/method versions, candidate populations and prior exposure; overlapping rosters are sensitivity populations, with no independent held-out test.

[Release evidence](../../data/manifests/release-evidence-v1.tsv) is the dependency crosswalk. Each row represents a relationship source, manuscript claim, current-document link, or historical audit occurrence. Repeated locators are intentional: they retain the citing context. The original audit had 77 absent outer-path occurrences covering 61 unique paths, not 77 absent datasets.

| Field | Meaning |
|---|---|
| `relationship_id`, `claim_id`, `context` | Relationship or claim key when applicable, plus the document or audit occurrence that uses the evidence |
| `workspace_path` | Original locator, retained even for excluded or historically misresolved links |
| `release_relative_path` | Included outer path; historical snapshot links can map to a separately identified original project record |
| `archive_path`, `archive_member` | Exact nested archive and member when an exact-byte equivalent is present; use the archive's own extraction directory |
| `source_url`, `sha256`, `version` | Retained source locator and byte identity/version; blank hash means no file at that locator, not a successful verification |
| `disposition`, `reason`, `note` | `include`, `retrieve`, `omit` or `unresolved`, with the scope and reason |

A missing relationship or claim key means the row documents another dependency context. Unknown scientific metadata stays `unknown`, `not_applicable` or the explicit pending code used by its source table. An `omit` row can document a directory locator or excluded historical supporting file; it is not a negative biological label. `retrieve` provides an existing source route without claiming a new retrieval succeeded. Any `unresolved` required input remains a gap. Immutable historical documents may retain excluded-file links; consult the crosswalk rather than interpreting those as bundled payloads. Historical snapshot links mapped to current original records are identified explicitly and are not fabricated snapshot copies.

## Attribution and limits

The [numerical source notice](numerical-source-notice-2026-10-11.md), [assembly attribution](../../data/manifests/release-assembly-attribution-2026-10-11.tsv), spectral source dispositions and [licence scope](licenses/SCOPE.md) govern the selected components. Original code uses Apache-2.0; original curation, generated results and documentation use CC BY 4.0. Those licences do not replace third-party terms. Factual derived numerical inputs retain source attribution and the disclosed historical author-workbook mapping basis. The raw author workbook and correspondence are excluded.

The [pinned class-table route](npclassscore-dependency-route-2026-10-11.md) is required for spectral arithmetic. Retained evidence packets give source papers, experimental anchors, accessions, uncertainty and superseding decisions where copied source publications are omitted. The package does not claim that every source can be acquired anonymously or that all raw-to-fit steps are portable.

Final scientific approval, manuscript/disclosure approval and authorization for external sharing remain open. Local fresh extraction demonstrates local portability only. An authorized anonymous download and its numerical checks must be recorded separately before claiming that access route works.

## Similarity companion in private candidate v3

The [similarity dictionary](similarity-independence-v1.md) describes the bounded pair tables and their joins. The [input-disposition index](../../data/manifests/similarity-input-disposition-v1.tsv) identifies every manifest-consumed input at its exact outer archive path and hash. The output manifest, stage receipts, source sequence/structure/spectrum records, scripts and recorded environment accompany the outputs. Package checks verify membership and bytes; they do not claim a new scientific rerun, public source retrieval or human biological review. The prior replay evidence applies only to the unchanged inherited numerical payloads.
