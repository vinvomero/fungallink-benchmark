# HEx PKS17 and compound 6

8 October 2026. Assistant-curated under the user's delegated admission authority. This is a historical reference-supported relationship, not independent biological validation.

## Accepted scope

Admit the source-defined Hydnomerulius pinastri PKS17 reference interval `KN839868.1:143119-188013|source-interval-v1` to Harvey et al.'s compound 6. The [primary paper](https://doi.org/10.1126/sciadv.aar5459) explicitly states that PKS17 produces compound 6, described as a leucine methyl ester bearing a polyketide-derived amide. Supplementary Table S11 and Figures S25–S29 report its NMR characterization. Count one compound-number target, with no additional stereochemical claim.

The measured context is engineered Saccharomyces cerevisiae expression strain 176, not native Hydnomerulius culture. Use a separate `hex2018` cohort. It cannot supply native fungal co-occurrence vectors. No analysis track, ranking pool or scoring adapter is activated by this admission.

## Sequence and sample correspondence

The previously retained supplement Table S8 gives PKS17 as KN839868, 143119–188013, and names pCHKU43.1-2.2, pCHKU43.2-2.2 and pCHKU43.3-2.2. Table S10, PDF page 27, assigns all three to strain 176. The published sequence archive contains all three exact record names.

The accession request resolves to KN839868.1. The reproducible `data/interim/hex-pks17-review-2026-10-08/audit_correspondence.py` checks full-length exact containment of all 13 annotated reference proteins in six-frame translations of those three retained sequence records. All 13 match, including the 2,652-aa PKS. No edited or designed sequence was produced. The archive lacks useful CDS annotations for the fungal inserts; the audit therefore uses sequence containment rather than assuming annotation absence means gene absence. Record hashes and per-protein match results are retained in `correspondence-audit.json`.

This supports the source reference interval through the tested protein set. It does not assert identical native regulatory DNA, native gene order in the expression constructs, native production, or pathway sufficiency independent of the yeast host. Classification is reference-supported because the query is the native reference interval and the measured experiment used refactored constructs.

## Measurement resolution and limits

The main text's explicit PKS17-to-compound-6 statement and the numbered NMR record supply the historical measured-product attribution. Table S11 was visually inspected. Figure S18, PDF page 36, shows expression-strain/control chromatograms, but it displays several ions and does not explicitly identify which is compound 6. Do not equate every panel with a different molecule or assign compound 6 to a displayed ion by inference. The positive target is `source-compound:6`; it is not a native feature ID.

Table S8 prints length 44,894 whereas the inclusive accession interval contains 44,895 bases. Preserve the source endpoints and name the inclusive convention explicitly; do not silently correct the source length. All 13 CDS features in the returned interval are nonpartial. No whole-genome alternative-locus search was performed, and exact protein occurrence is only checked in the three specified expression records.

The existing HEx input screen remains valid: full numeric candidate tables, stable acquisition mapping and native feature/spectrum joins were not recovered. No repeated deposit search or new raw conversion was performed. Other HEx candidates remain unadmitted; this decision does not waive their construct-version discrepancies or product-identification gaps.

## Reuse and reopening

Reused the retained article XML/text, 72-page supplement, three expression records inside the existing 78-record archive, and prior source inventory. Only the source-specified reference interval was newly retrieved. Its receipt retains URL, retrieval time, bytes and SHA-256. This is public 2018 characterization with known prior exposure, not an unfamiliar-pathway case.

Reopen biological admission for a correction to PKS17 identity, incompatible expression-record versions, broken compound-number attribution or contradictory product-specific evidence. Reopen input readiness for an exact processed-table/raw-manifest locator and a validated compound-6-to-feature bridge. Do not rerun the 13-protein containment check without changed source bytes or a new question.
