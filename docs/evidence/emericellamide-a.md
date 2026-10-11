# Emericellamide A, ATCC 38163

Curated 30 September 2026. Researcher-led scientific disposition is pending Vin Vomero's review; no external reviewer is assigned. Proposed evidence class: **reference-supported, pending scientific review**. Full-length sequence identity supports the named source locus. The source Tier II chemical assignment is retained separately; no assignment to emericellamide B is made.

Caesar Supplementary Table 4 linkage 6 connects feature 8468 to HRPKS_71 and BGC0001290. A fresh visual inspection of Supplementary Figure 1 (PDF page 22, printed S21) confirms the emericellamide A panel is labeled Type II dereplication, 25 HCD. Its caption (PDF page 20) describes Types I and II as high-confidence authenticated-standard routes from different in-house databases, not an ordinal ranking between those two routes. The packet retains the historical field name Tier II while preserving that distinction. The displayed precursor is 610.4144; it is not silently substituted for the workbook centroid or used to assign a native scan. Sheet1 row 8476 gives m/z 610.4233936 and retention time 4.682688131 min. ATCC38163 columns BY, BZ, and CA contain 13,600,000 (Cheerios), 4,178,886.75 (Oats), and 5,658,963.5 (Rice). Only Cheerios reaches the source's inclusive 10^7 presence threshold. Below threshold is not evidence of biological absence. See [the exact cell and filename receipt](first-three-source-checks.json).

[Chiang et al. 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2494592/) identified emericellamide A by NMR and linked it to easAâ€“D through deletion experiments (Figures 1â€“2). R153 supplied the wild-type material; TN02A3 was the deletion recipient. These are not Caesar's literal culture. Figure 1 also marks a minor product sharing its MS/MS fragments, so fragmentation resemblance alone cannot assign an isomer. The five proteins present in the reference record must not be described as five experimentally necessary genes: the paper establishes four eas genes, and the small intervening hypothetical gene is dispensable.

The [FGSC A4 record](https://www.fgsc.net/strain_detail.php?id=4) lists ATCC 38163 as an alias. Caesar Supplementary Table 2 maps ATCC38163 to GCA_000011425.1. Its FMGX0049 label is supported by the retained author-workbook crosswalk; that private/historical bridge is not a new public product validation.

The publisher's HRPKS_71 HTML identifies BN001307.1.region009 / FMGX0049 and supplies full protein sequences in its openBlast attributes. This pass compared those strings with a fresh download of [BGC0001290.4](https://mibig.secondarymetabolites.org/repository/BGC0001290.4/BGC0001290.gbk). All five are identical across their full length:

| Protein | Length, aa | Identity | Reference coverage |
|---|---:|---:|---:|
| CBF87069.1 | 6,919 | 100% | 100% |
| CBF87071.1 | 164 | 100% | 100% |
| CBF87072.1 | 2,534 | 100% | 100% |
| CBF87074.1 | 479 | 100% | 100% |
| CBF87076.1 | 565 | 100% | 100% |

The downloaded GenBank SHA-256 is `ae461b418993f199272cb911cf56605642b161580fa7b13315dabf7fa093727b`. The HTML SHA-256 is `dbf05efdc8d60c2393af056814e63862abc7fa767aa8134e1845a1e50681ccf8`. Per-protein hashes and the comparison method are in the receipt. This independently reruns a file comparison, not a biological validation experiment.

The reference core is BN001307.1:4,230,453â€“4,267,876. The historical region009 is not the retained antiSMASH 8.0.4 region009 at 3,555,138â€“3,586,573. The retained comparison maps the source to region011 at 4,200,456â€“4,292,984. Region numbers are annotation-specific. The same-numbered successor region is an explicit wrong-locus alternative, not competing evidence for emericellamide production. This pass did not perform an assembly-wide search for another eas-like cassette.

The evidence supports a reference-supported BGC candidate at the named locus and an associated source GCF candidate. These are different queries. A family-level release still needs its full member roster and sample mapping frozen; a sequence-defined release needs its sequence and boundaries packaged. The remaining scientific decision is whether the source Tier II named-product assignment is sufficient for the declared feature-only track, with its isomer caveat stated. The source panel has now been inspected. An assembly-wide competing-locus check remains unfinished work, not proof that a new wet-lab experiment is required. Historical native-scan membership is unresolved and excludes this target from a spectral extension until resolved.

Source-selection and known-pathway exposure must be recorded. This case was chosen using published correlations and a known reference, so it cannot establish unbiased discovery rates or unseen-pathway performance. No human scientific sign-off is claimed.
