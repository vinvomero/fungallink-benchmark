# Pestalamide derivative census

Recommend two additional **measured-feature relationships** for review under the existing `source:NRPSPKS_85` query: feature 1950, associated with source putative pestalamide E, and feature 895, associated with source putative pestalamide F. Keep the other four derivatives provisional. Their source annotations do not establish feature-specific experimental support. No canonical admissions were changed.

This is a six-row bounded appraisal using retained primary sources, with no new retrieval or experiment. The [machine-readable census](../../data/curated/pestalamide-derivative-census-2026-10-03.tsv) separates chemical certainty, pathway evidence, target correspondence, and input readiness. Requested route: `gpt-6-astra`, `medium` reasoning; actual serving receipt unavailable. The canonical plan, benchmark contract, and humanizer skill were read and applied. This automated curator appraisal requires host review; it is not independent scientific validation.

| Feature; workbook row | Source annotation; m/z; RT minutes | Supported chemical resolution and disposition |
|---|---|---|
| 757; 765 | derivative 5; 361.137445; 3.101109048 | Unresolved pestalamide-related feature. Keep provisional. Do not equate it with E or collapse it with 1950. |
| 895; 903 | B derivative 1; 387.157844; 2.219772902 | F-associated measured feature, with a putative carboxylated-B structure. Recommend direct feature-only support, pending review. |
| 1887; 1895 | derivative 4; 429.1623053; 2.433723878 | Unresolved pestalamide-related feature. Keep provisional; the nearby mass in the network lacks specific experimental support. |
| 1950; 1958 | derivative 6; 361.1374241; 2.114501449 | E-associated measured feature, with a putative hydrated-B structure. Recommend direct feature-only support, pending review. |
| 6691; 6699 | derivative 3; 415.1477082; 2.269766667 | Unresolved pestalamide-related feature. Keep provisional; do not assign D from mass or the article's generic family description. |
| 6716; 6724 | derivative 2; 491.1858105; 3.225169831 | Unresolved pestalamide-related feature. Keep provisional; Figure 19 does not label a corresponding 491.186 node. |

The [retained supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-023-01276-8/MediaObjects/41589_2023_1276_MOESM1_ESM.pdf), Supplementary Figure 19 (physical PDF page 41, printed page 40), explicitly keys cyan to E and orange to F. Both colored monomer nodes have black outlines. The caption defines these outlines as detection in the transformed heterologous host; their square shapes also identify the reported isotope-incorporation evidence. This is positive experimental evidence for E/F-associated signals, independent of their correlations. The figure's gray 429.166 and 415.15 nodes have no black outlines. Absence of an outline does not prove biological nonproduction, but it supplies no direct detection evidence for those nodes.

The main article's retained BioC passage at offset 22052 assigns that transformed host to the CBS 101.740 pst member, reports production of B and analogues, and reports no detectable pestalamides in the untransformed host. The family-member connection follows the [B packet](pestalamide-b.md): CBS 101.740, FMGX0018, GCA_001889945.1, with documented HYBRID_85/NRPSPKS_85 aliasing. Figure 4a remains a B-specific display. This appraisal does not claim separate E- or F-specific deletion chromatograms or production by every family member.

The critical historical feature bridge comes from Supplementary Table 6 (PDF page 13, printed page 12). I compared its numeric producer maxima with all 9,339 workbook feature rows, using the table's three-significant-figure precision and no mass or source-name filter:

| Source target | Numeric producer vector in Table 6 | Unique matching workbook feature |
|---|---|---|
| E | CBS 101.740: 384,000,000; ATCC 9029: 28,700,000; CBS 113.46: 84,400,000 | 1950 |
| F | CBS 101.740: 61,100,000; ATCC 9029: 24,700,000; ATCC 13490: 16,800,000; ATCC 13157: 42,800,000 | 895 |

Each numeric vector had exactly one match. The [full-pool receipt](../../data/interim/pestalamide-derivative-census/full-candidate-vector-check.json) records the comparison, row count, and matching metadata. This establishes a specific documentary correspondence, not statistical independence or a native scan join. The m/z agreement is supporting information, not the selection rule. Source BDL/ND statuses were not treated as exact numerical zeros: some workbook subthreshold signals occur where Table 6 says ND.

The [workbook receipt](../../data/interim/pestalamide-derivative-census/workbook-check.json) retains exact cells and condition headers. For CBS 101.740, columns DN, DO, DP are Cheerios, Oats, Rice. Feature 1950 has 384,000,000, 109,294.4766, and 0; feature 895 has 61,100,000, 46,300,000, and 20,700,000. By contrast, the same columns for 757 give 279,783.8125, 90,600,000, and 76,900,000. Feature 757 cannot inherit the E assignment merely because its mass is nearly identical. Its longer retention time remains a separate source observation; an isomer or ion-form interpretation is unresolved.

Supplementary Figure 20c,d (PDF page 42, printed page 41) supplies annotated fragmentation and proposed E/F structures. Its caption expressly calls them putative analogues. The main article, BioC offset 20819, likewise describes E and F as inferred hydrated and carboxylated B forms. There is no E/F NMR or authenticated-standard comparison claimed here. The structures remain putative even if their feature relationships are accepted.

This scope fits the existing measured-feature contract without a chemistry-rule change. The contract permits an explicitly named broader target where the evidence supports that resolution. Here, the supported targets are the experimentally detected E-associated feature 1950 and F-associated feature 895, with source-proposed structures recorded as annotations. They are not fully identified molecular structures. The direct-GCF rule requires an experimentally represented member and a traceable measured target; the exact colored nodes and unique Table 6 correspondences supply those connections. If a later track requires exact structures, these two records do not meet that stronger claim without further evidence.

For 757, 1887, 6691, and 6716, reopening requires a feature-specific experimental bridge and a supported target resolution. A broad analogue statement, workbook derivative name, molecular-network connection, or co-occurrence score does not supply the missing connection. Keep them as candidates and unresolved labels, never as negative answers. Feature 1955 remains outside this six-row census and is not admitted as an A dimer; Figure 19 colors its nearby node cyan rather than A-green.

All six historical feature rows are present in the retained source export. Missing native feature-to-spectrum identifiers remain a spectral-readiness gap. The two recommendations share the existing pst query, roster, candidate universe, and prior source-selection exposure. If both are adopted, they expand its positive set by two relationships while adding zero independent queries and zero pathway groups. They do not establish an unfamiliar-pathway evaluation.

Primary-source fingerprints, checked 3 October 2026:

| Retained input | Bytes | SHA-256 |
|---|---:|---|
| Publisher workbook, `41589_2023_1276_MOESM4_ESM.xlsx` | 19,251,141 | `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb` |
| `caesar-supplement-cdn` | 5,911,348 | `259acfe84b6a7033ef3cbd41ba05133ce64ee32c8f102d49541fa4f8b57a2108` |
| `pmc-bioc.xml` | 113,653 | `b507fb31770451e358060fe63c8dd42718b553351a84d9ae4e0d7dd6c0523701` |
| `caesar-feature-source-v1/features.tsv` | 611,087 | `075a06513dd29250c3810ee725549766718d804d7923c83c6fefbdda76cd1dfc` |

Rendered pages 13, 41, and 42, extracted passages, and receipts are retained under `data/interim/pestalamide-derivative-census/`. Figures 19 and 20 were visually inspected. No canonical label, query roster, or production code was changed by this unit; no git commands were run.
