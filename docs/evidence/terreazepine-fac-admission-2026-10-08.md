# Terreazepine: FACMS0016 admission

8 October 2026. Assistant-curated under the user's existing delegation; no independent human validation is claimed.

## Decision and scope

Admit one directly supported relationship between the deposited AtFAC7O19 tested-gene envelope, `MT376588.1:92115-102627|gene-envelope-v1`, and the historical terreazepine/FACMS0016 measured target. This adds one BGC query. The reported S/R mixture is one target, not two independent relationships. No new scores or native feature joins are claimed.

## Evidence chain

The retained 2017 census, `data/curated/fac-supplement-evidence-2026-10-07.tsv`, identifies FACMS0016 as the AtFAC7O19 product, with ATEG_07358 as the deleted NRPS anchor and a displayed m/z of 310.119. Its Supplementary Figure 2F is the historical measured-target evidence.

The [2020 primary follow-up](https://doi.org/10.1128/mBio.01691-20) explicitly starts from the previously reported AtFAC7O19 product, cites the 2017 study, reports m/z 310.1188 and C17H15N3O3, and names the characterized product terreazepine. The bridge uses the same named FAC, donor, gene anchor and cited discovery, with mass as corroboration. It is not a mass-only assignment. The source reports purification from FAC-transformed A. nidulans, NMR, MS/MS and comparisons with synthetic material. Chiral chromatography supports an approximately 2:1 S/R mixture in the isolated natural material; no separate benchmark targets are inferred.

The follow-up explicitly deposits the sequenced FAC as MT376588. Table S1A maps FAC38_35/TzpA to ATEG_07358 and FAC38_36/TzpB to ATEG_07359. MT376588.1 annotates these genes consecutively on the minus strand. Extracted CDS translations exactly match their deposited translations (2,510 and 420 amino acids). The query envelope uses the deposited version's one-based inclusive CDS extrema, 92,115–102,627. It is the tested two-gene envelope, not a claim to exhaustive predicted cluster boundaries or autonomous sufficiency. Figure 2A, Table S1A page 2 and Figure S5 were visually inspected.

Figure 2D shows the product in the intact pathway and a roughly 5,000-fold reduction after the reported NRPS domain deletion. Figure S5 shows a strong reduction following the IDO deletion in the transcription-factor-overexpression context. These are historical experimental observations, not proposed experiments. Host contribution remains possible.

## Differences retained

- Table S1A gives ascending extrema 92,114–99,708 and 101,177–102,627; GenBank's one-based starts are one base higher. Use deposited coordinates and preserve the printed table rather than silently treating both conventions as identical.
- The paper calls the completed clone 114.911 kb; MT376588.1 is 114,922 bases. This 11-base length discrepancy does not alter the explicit accession attribution, but is not resolved by the present review.
- Main text says no product after IDO deletion; Figure S5's caption says very low production and gives nonzero signal. Record strong reduction, not proven absolute absence.
- Figure 2D labels time in seconds, whereas Figure S5 labels minutes. Neither is converted into a raw-file retention-time join.
- Source identifiers use tzp/Tzp; secondary resources can transpose these letters. Keep accession and FAC38 identifiers authoritative.

## Input readiness and exposure

The source establishes a sequence-defined tested-locus relationship and a traceable published measured target. The complete FAC candidate pool, eligible sample map and native row/scan bridge remain missing. No FAC scoring is activated. The source's FAC-score selection and 2017/2020 published characterization are prior exposure. This is not an unseen-pathway case or a new independent cohort.

Retained source payloads, hashes and the reproducible sequence audit are in `data/interim/terreazepine-fac-review-2026-10-08/`. The paper XML is PMC7448278.1; metadata reports CC BY. This review read chemistry descriptions and captions, not every underlying NMR spectrum. Reopen for corrected FAC identity, incompatible sequence annotation, a broken source-target bridge or contradictory product-specific evidence. Reopen input readiness only for a concrete complete-table/sample-map locator or recovered export.
