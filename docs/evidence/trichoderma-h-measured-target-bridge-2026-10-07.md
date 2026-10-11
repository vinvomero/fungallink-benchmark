# Ilicicolin H measured-target bridge

Date: 2026-10-07. Requested route: gpt-6-astra / medium; actual serving model and effort unverified. Automated appraisal only. No canonical admission or human chemical validation.

The MZmine 3.9.0 reprocessing export contains a defensible **ilicicolin H candidate at row 30**, m/z 434.23256913309, RT 5.8394184 min, with exported spectrum `FEATURE_ID=30`. Its identification recommendation rests on the published chromatography, measured fragmentation, and direction of the sample difference together. It is not a new authentic-standard confirmation, and row 30 is not claimed to equal a historical MZmine 4.0.3 node number.

Raw scan membership is still being checked by the processing unit. The MGF `SCANS=30` field is an export feature identifier, not evidence of raw scan 30. The row-to-exported-spectrum join is exact; raw-scan provenance must be added separately.

## Source-side anchors

The retained [Burger et al. article](https://doi.org/10.1186/s13068-025-02628-3) reports matching H mass, retention time, and collision cross section to an authentic standard using Skyline 22.2. H was also isolated and characterized by NMR (supplement Table S6, Figs. S13-S14). Those source chemical results identify H; the reprocessed files inherit their relevance only through a documented measurement bridge.

For molecular networking the paper switched TIMS off, retained the LC eluents and gradient, and used Auto MS/MS. Consequently the two network acquisitions have no transferable measured CCS value. They should not be treated as direct CCS-standard matches. The text assigns network RTs of 5.84 min to H, 6.31 to 8-epi-H, 6.57 to bis-diene, and 8.23 to another same-mass compound. Fig. 2's separate chromatogram appears shifted slightly later than these textual network RTs; its plot is not a substitute for a numerical acquisition-specific RT record.

Figures 2, 3, and 4 were downloaded from the PMC figure URLs embedded in the retained article XML and visually inspected. Fig. 3 labels H's protonated ion at 434.2326, dehydrated ion at 416.2219, and sodium adduct at 456.2143. It gives no historical feature ID for H's labeled molecule node. Fig. 4 labels H fragments at 134.0600, 173.1327, 216.0651, 230.0449, 248.0555, 258.0760 and 416.2210, with precursor 434.2321. These are visually read labels, not a recovered numerical source spectrum; no digitized-intensity cosine score was fabricated.

The paper explicitly says H and 8-epi-H have nearly identical fragments and similar intensities. Their spectra alone cannot establish stereoisomer identity. By contrast, bis-diene shows stronger 189.1639 and 272.0909 fragments. All three share the prominent 230.0449 fragment. The later 8.23-min compound remains unresolved; it must not be relabeled H because of the same mass or shared fragments.

## Reprocessed candidates and competing assignments

Inspection used the processing unit's `mzmine390/output/full_candidate_pool_quant.csv` and `full_candidate_pool.mgf`, fingerprinted in `inspected-export-fingerprints.json`. The full pool has 98 rows and 91 exported spectra. All four rows within the article's EICC locator of 434.2326 ±0.02 Da were inspected across the entire exported RT range. This inclusive locator was an audit query, not a tuned feature-processing threshold or a claim that 0.02 Da alone identifies H.

The host separately verified all 91 unique CSV-to-MGF joins, mass/RT agreement at exported precision, finite nonnegative numerical cells, and retention of seven spectrum-free candidates. That receipt is `data/raw/trichoderma-measurements-2026-10-07/pilot-export-host-verification.json`; it verifies serialization rather than chemical identity. Inspected CSV SHA-256: `eee096ce16990f97d52c6f9f9c21a62b4e0997a08173833ae971f2365c15864d`; MGF SHA-256: `ce6e54dafd624c8e0b50910952d3d84c11ca6dc3766c362f097039fa2a6e6d6c`.

| Reprocessed row | m/z | RT, min | OE area | diliE area | Interpretation |
|---|---:|---:|---:|---:|---|
| 30 | 434.23256913309 | 5.8394184 | 88565.99 | 12587.079 | H recommendation |
| 35 | 434.23250992280373 | 6.3057547 | 18935.469 | 100943.48 | competing epimer-like row |
| 43 | 434.2324796022705 | 6.570394 | 20579.1 | 68031.3 | competing bis-diene-like row |
| 64 | 434.23250916869154 | 8.224282 | 2265.5115 | 9613.492 | later unresolved isomer |

The column labels refer to `Molecular Networking_OE_timsOFF.d` and `Molecular Networking_diliE_timsOFF.d`. Their aliases are consistent with the source's OETriliR and ΔTriliE backgrounds, but sample provenance must retain the filename-based crosswalk rather than imply a separately recovered biological metadata sheet. These are two acquisitions, not the article's quadruplicate comparison and not two independent genomes.

Row 30's exported MS/MS base peak is 230.0449. Other observed peaks are 134.0602, 173.1327, 216.0656, 248.0558, 258.0765, and 416.2229. Each lies within 0.0019 Da of the corresponding labeled H peak. The 189.1635 fragment is 2.93% of the base peak, whereas row 43 has 189.1639 at 34%. Row 43 also has 272.0909 at 5%; row 30 has no close peak at that mass. These comparisons agree with the paper's bis-diene distinction. They do not distinguish H from its epimer by fragmentation alone.

The chromatographic assignment is supported by the measured pattern across the two files: row 30 is 7.04-fold higher in OE than diliE, while rows 35 and 43 are 5.33- and 3.31-fold higher in diliE than OE. This is consistent with the paper's H decrease and intermediate accumulation after triliE deletion. It is corroborating within-study evidence, not an independent replication or a test of significance. The absent wildtype and triliA-deletion acquisitions in this two-file release cannot be reconstructed from these values.

The numerical inspection record contains nearest peaks and their mass errors for every competitor. A nearest peak is not automatically a match: for example, row 30's nearest peak to 272.0909 is almost 1 Da away and is explicitly not evidence for that fragment.

## Exact export join and remaining provenance

Recommended candidate key: the processing release's row 30 in the full 98-row candidate pool. Recommended exported spectrum key: `full_candidate_pool.mgf`, `FEATURE_ID=30`, `PEPMASS=434.2326`, `RTINSECONDS=350.365`, `MSLEVEL=2`, `CHARGE=1+`. This RT is the exported row-level value; do not substitute it for every individual fragmentation event's RT. All competitors remain in the candidate universe.

The SIRIUS export contains additional row-30 spectra and lists both source filenames, with row-level RTs around 349.60 and 351.13 seconds. Its repeated `SCANS=30` is still a feature identifier. Filename lists alone do not recover the underlying Bruker fragmentation-event IDs or prove which event generated the selected GNPS spectrum.

The processing worker is checking a saved project export for: acquisition identifier, raw TSF frame or native scan identifier, precursor m/z, event RT, collision energy, row membership, and the selected/merged spectrum provenance. For spectral readiness, the requested validation is to show these memberships for row 30 and competing rows 35/43/64, then demonstrate that the selected row-30 spectrum matches the fingerprinted MGF peak list. If the exporter merges or selects spectra, retain that rule and the parent events rather than invent a single native scan. This check is not a universal prerequisite for feature-only biological eligibility.

This is a newly processed MZmine 3.9.0 release. Source MZmine 4.0.3 was unavailable without login; the processing unit records compatibility warnings and deviations. The source's historical export was not recovered, so the recommendation transfers published chemical evidence to a new feature, not to an allegedly restored historical node. The complete candidate pool was retained, and neither feature-detection settings nor candidate inclusion were changed using these labels.

The QM6a reference locus is independently defined in `trichoderma-qm6a-correspondence-2026-10-07.md`. The H feature-only relationship is ready for scientific adjudication of the source-to-row-30 chemical transfer and its stated sample scope. That judgment should consider the combined chromatographic, fragment, and abundance evidence above, while retaining the filename-derived sample crosswalk and absence of a newly run standard. Missing native MS/MS event membership does not by itself invalidate that feature-only relationship. No biological admission is made by this automated appraisal.

Spectral readiness remains a separate decision: CSV-to-exported-MGF membership is verified, while raw event or equivalent project-level provenance is still being checked. Release freezing is technical packaging only; it is needed for reproducible evaluation, not to judge the biological evidence. This source-side appraisal is complete and need not remain open while those technical checks proceed.
