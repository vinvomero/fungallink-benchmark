# Assessing the genomic-to-measurement connections

Updated 11 October 2026. The private presubmission candidate v2 adds source locators and this guide. It preserves every scientific payload from candidate v1. The manuscript and older component filenames retain their original versions; v2 changes delivery documentation only.

The records let a reader inspect all 30 current label decisions and their stated evidence. They do not establish that all 30 have runnable benchmark inputs or that every historical sample assignment has independent public confirmation. Eleven relationships have complete evaluated inputs, two have partial diagnostics, and 17 identify source experiments without usable benchmark inputs.

## Follow a relationship

Start with [the 30-row traceability table](../../data/manifests/relationship-traceability-v1.tsv). Select `relationship_id` and follow `evidence_packet`, `current_decision` and any `supersession`. Read `source_locator` for the experimental panel, table or accession, and `uncertainty` for the limit on the assignment. The [readiness table](../../data/curated/relationship-readiness-v1.tsv) supplies experimental context, reference transfer and method eligibility. The [ledger](../../data/curated/label-evidence.tsv) remains authoritative.

For complete records, `evaluation_record` identifies a packaged gold file whose query, relationship and positive target agree exactly with the traceability row. For partial diagnostics, it identifies the saved evaluation containing that target ID; this does not establish complete candidate coverage. For the 17 input-missing records, source target names or panels are evidence locators, not executable feature IDs.

## Inspect the sample mapping

For the Caesar population, follow these packaged records in order:

1. [Member eligibility](../../data/curated/seven-admitted-member-eligibility-2026-10-03.tsv): source family members, proposed sample identities, evidence scope, conflicts and embedded historical row snapshots.
2. [Population mapping](../../data/curated/caesar-source-gcf-population-2026-10-03.tsv): assembly assertions, study-roster IDs, acquisitions, label/condition observations and per-family membership. `historical_bridge_rows_json` preserves the actual imported mapping rows and their physical row numbers.
3. [Study roster](../../data/curated/caesar-study-roster-2026-10-02.tsv) and [sample crosswalk](../../data/curated/sample-crosswalk.tsv): source strain/accession assertions and measurement identities. [Labels](../../data/processed/caesar-source-observations-v1/labels.tsv) and [conditions](../../data/processed/caesar-source-observations-v1/conditions.tsv) retain the observed measurement records.
4. The relationship's saved gold file and versioned evaluation records identify the frozen task. Historical tables retain their original `proposed` wording; the current readiness and frozen evaluation records establish which subset was actually evaluated.

The population table contains 116 rows, including 105 marked for internal source-selected inclusion. Withheld or conflicting mappings remain visible. The original author workbook and correspondence are not bundled. Their derived assertions are inspectable in the embedded rows, but that does not make their original provenance independently public or resolve identity conflicts. See the [source provenance addendum](source-provenance-addendum-2026-10-07.md). Do not infer that all members of a family produce a compound, or treat unresolved relationships as negatives.

## Open the source evidence

Use `workspace_path` in the [evidence crosswalk](../../data/manifests/release-evidence-v1.tsv) to find `source_url`. The [locator record](../../planning/provenance-links-2026-10-11/link-request.json) distinguishes exact file URLs from parent publications and landing pages. Parent-source links do not claim byte identity with a local text extract or cropped figure.

Six previously unlinked primary dependencies were downloaded on 11 October and matched the retained SHA-256 values: the FAC supplement, acu-dioxomorpholine article and supplement, and HEx article, Figure 5 and supplement. [Retrieval receipt](../../planning/provenance-links-2026-10-11/link-results.json). Eight further locators were recovered from existing records; their availability was not rechecked in this repair. Publisher terms continue to apply. Internal scripts, private records and local derivatives without public hosting should not be mistaken for missing public download links.

The [mapping audit](../../planning/provenance-links-2026-10-11/mapping-audit.json) checks record joins and embedded historical rows against the retained original. Hashes and joins do not validate the biological conclusions. Human scientific review and an authorized external download test remain open.
