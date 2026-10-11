# HEx PKS15 and PKS23 evidence decisions

8 October 2026. Assistant-curated under existing delegated authority. The retained [HEx primary paper](https://doi.org/10.1126/sciadv.aar5459), supplement and sequence archive were reused. Two source-specified reference intervals and the main Figure 5 image were newly retrieved. No raw-data reconstruction or sequence design was performed.

## PKS15: admit one reference-supported historical target

The paper explicitly reports PKS15 producing orsellinic acid, compound 3, as its major product; Figure 5 labels its structure as 3. Supplementary Figure S16 (PDF page 34) shows strain 247 and control 137 chromatograms. Treat compound 3 as a source-identified measured-product target. This review does not establish an authenticated-standard comparison, NMR confirmation or a native feature-row join for that product. Do not count the many ion panels as additional molecules or automatically map a panel to compound 3 by mass.

Table S8 identifies the Moniliophthora roreri native reference interval AWSO01000045, 179446–203577, and pCHKU39.1-2.2 plus pCHKU39.2-2.2. Table S10 assigns these same records to expression strain 247. Both exact names occur in the retained Datafile S1 archive. The reference accession resolves to AWSO01000045.1. All seven annotated full-length reference proteins, including the 2,201-aa PKS, exactly match proteins encoded by these two archived records. No reference CDS is marked partial in the returned interval.

Accept `AWSO01000045.1:179446-203577|source-interval-v1` to `source-compound:3`, named orsellinic-acid-associated measured product (source identification). Classification is reference-supported: the native interval is represented by its tested protein set in engineered yeast, not by unchanged native regulatory DNA. The inclusive interval is 24,132 bases; the source prints 24,131. Preserve both with their conventions stated. Host contribution is not excluded; native production, whole-genome exclusivity and independently validated structure are not claimed.

## PKS23: preserve two unadmitted candidates

The main text and Figure 5 explicitly attribute compounds 4 and 5 to PKS23. Table S8 maps the reference interval KE720645, 48853–80314, to pCHSU70.1-2.2 and pCHSU70.2-2.2. Table S10 maps these records to expression strain 241. Both archived record names exist. Main Figure 5 and Supplementary Figure S22 (PDF page 38) display nine genes and product/ion evidence.

Only five of nine reference proteins match in full in the two archived records. The unmatched identifiers are ERF77219.1, ERF77222.1, ERF77225.1 and ERF77226.1. A bounded diagnostic also found none of their nonoverlapping 20-aa chunks in six-frame translations of these records. This is not an identity percentage or proof of biological absence. The discrepancy could reflect source record scope or version, annotation differences, or another unresolved correspondence issue. Do not infer a cause or replace the source query with a convenient subset merely to admit it.

Leave both numbered products unadmitted pending reconciliation of the nine-gene source diagram with the two archived records. Reopen only for an explicit source correction, another exact sequence-record version, or primary evidence defining which genes were represented in the tested strain. Do not repeat the exact-match or chunk checks without new evidence.

## Shared limitations and provenance

Both cases are yeast-expression evidence in the separate hex2018 cohort. They supply no native fungal co-occurrence matrix. The existing full-pool, sample-map and native feature/spectrum gaps remain open. Biological admission does not activate scoring. Public characterization and source selection are prior exposure, and no additional independence is inferred from ion panels or biological replicates.

The scripts, per-protein results, retrieved reference intervals, receipts and inspected figure renders are retained in `data/interim/hex-pks15-pks23-review-2026-10-08/`. Reproduce each containment audit with `python data/interim/hex-pks15-pks23-review-2026-10-08/audit_correspondence.py PKS15` or `PKS23`. Source archive SHA-256 is `59b3676602610d66501953c3dc89d3fef94b14a77192442ae87d8b7a1c9c1c25`. PMC metadata reports CC BY-NC for the article; no new public redistribution occurs.
