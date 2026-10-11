# Acu-dioxomorpholine A-associated FAC target

Admit one reference-supported, source-accession-defined locus-to-measured-target relationship, under the user's delegated scientific judgment. This adds one query identity. It does not establish an independent cohort or an executable FAC benchmark.

## Primary evidence

Robey et al., DOI [10.1021/acschembio.8b00024](https://doi.org/10.1021/acschembio.8b00024), explicitly identifies FACMS0001 from AaFAC30-6A16 as the acu-dioxomorpholine A-associated signal. The name is based on high-resolution MS/MS and related-compound comparison, not new NMR elucidation. Its supplement Table S1 assigns three protein accessions to adxA–C. Figure S5 separately shows loss of the named target for those three deletions and persistence in four other deletion backgrounds. Table S1 and Figure S5 were visually inspected, actual PDF pages 8–9 (printed 7–8).

The 2017 inventory's facms0001/AaFAC6A16 case and the follow-up share the explicit product identifier and numbered FAC designation, with a matching principal measured ion. This is accepted as the follow-up of that case, not a second relationship. A same-mass match alone would not justify the bridge. The follow-up says only A was detected in the FAC extracts; B is not admitted by analogy. The reference database's B product heading does not override that primary distinction.

## Query and correspondence

The published protein accessions resolve to XP_020052773.1, XP_020052774.1 and XP_020052775.1 from A. aculeatus ATCC16872. Their lengths match Table S1 (2413, 378 and 422 aa). All three are explicitly annotated on NW_017962991.1; genomic CDS retranslation equals each complete retrieved protein. The smallest contiguous envelope is **NW_017962991.1:92289–104578**, 1-based inclusive, 12,290 bases. This defines `reference-gene-envelope-v1`, not an experimentally established minimal cluster.

The [audit](../../data/interim/acu-dioxomorpholine-fac-review-2026-10-08/reference-query-audit.json) records coordinates, strands, translation checks and hashes. Each exact protein occurs once among annotated CDSs on this scaffold; no whole-assembly alternative search or exclusive biosynthesis claim is made. The source assigns the accessions explicitly; the correspondence does not rest on protein-length agreement alone.

Figure S5 draws adxC forward, whereas the reference annotation places it reverse. This remains unresolved. The explicit protein attribution and same-donor annotation support the reference query, but do not establish that this reference interval is byte-identical to the tested FAC. No independently deposited complete AaFAC30-6A16 clone was recovered. For that reason the relationship is **reference-supported**, with the reference interval named as the query, rather than a claim of direct experimental validation of that exact sequence. Changed gene organization is not silently repaired or inferred away.

## Target and readiness

Target ID: `facms0001`; product label: `acu-dioxomorpholine A-associated measured product (structure proposed)`. Evidence includes the 2017 named measurement, the follow-up's explicit identifier and Figure S5's target-specific comparison. Source FAC-Score values differ between the papers (8.9 versus10); neither is a benchmark score and neither is used for admission.

The complete FAC candidate pool, eligible samples and source-to-export feature joins remain unresolved. No scoring, spectral activation, donor-pilot transfer or positive-set amendment follows from this admission. Proposed structure, source selection, reference/clone distinction, diagram discrepancy and shared expression-host context remain attached to the label.

## Retained sources

`data/interim/acu-dioxomorpholine-fac-review-2026-10-08/` contains the untouched versioned PMC XML, the ACS Figshare supplement and metadata, source protein/transcript/scaffold records, retrieval receipts and reference-query audit. The PMC metadata skill supplied the XML locator. The publisher browser returned403 and a guessed versioned PMC supplement object returned404; the exact-title Figshare API query recovered article6149300/file11106800. No failed route was presented as a successful retrieval. Public redistribution rights are not established by access.

Reopen for a corrected primary accession assignment, a conflicting FAC identity, a source correction affecting the named target, or contradictory locus/product evidence. Native input recovery remains a separate question. Reviewer: assistant-curated under user delegation, not independent human review.
