# First three admission decisions

Reviewed 2 October 2026. This is an automated evidence recommendation under the canonical plan and benchmark contract, not researcher signoff or an admitted release. Requested route: gpt-6-astra / medium; no serving-side receipt was exposed. Existing evidence records remain unchanged.

The published chemistry and named workbook rows suffice for the feature-only measured targets in all three cases. The unresolved native-scan joins affect spectral inputs only. Acetylaszonalenin still has incomplete experimental pathway support. Emericellamide A's exact-reference duplicate ambiguity is resolved; the broader competing-locus criterion remains open. Pestalamide B has enough recorded biological evidence for the proposed directly supported GCF relationship, pending researcher signoff and the release inputs.

## Evidence examined

I read the [canonical plan](../plans/2026-09-30-2052-benchmark-paper-plan.md), [benchmark contract](../../protocol/benchmark-contract.md), original three evidence packets, [label ledger](../../data/curated/label-evidence.tsv), and [30 September source receipt](first-three-source-checks.json). I visually rechecked cached Supplementary Figure 1, PDF pages 20 and 22 (printed S19 and S21), and Figure 2b, PDF page 25 (printed S24). The caption explicitly calls both Type I and Type II authenticated-standard routes high-confidence hits. Figure 2b compares acetylaszonalenin standard and CBS 544.65 extract.

The publisher workbook SHA-256 was rechecked as `4726f832f82da431cc7e0a7b048b9e5d3e0d7de0831b8d20e9dab24bb5131fbb`. A fresh read of Sheet1 confirmed the named rows and measurements below. The host also reported a complete-export check matching all three IDs and nine observations against the stored receipt. That export check is a host-reported verification, separate from this review's workbook read.

| Product | Feature; Sheet1 row | m/z; retention time in min | Recorded condition heights |
|---|---|---|---|
| Acetylaszonalenin | 2127; 2135 | 416.2000372; 3.664442544 | EI:EK = 1,130,000,000; 639,000,000; 1,130,000,000 |
| Emericellamide A | 8468; 8476 | 610.4233936; 4.682688131 | BY:CA = 13,600,000; 4,178,886.75; 5,658,963.5 |
| Pestalamide B | 810; 818 | 343.1280596; 2.256973731 | DN:DP = 1,250,000,000; 222,000,000; 46,200,000 |

Pathway experiments, prior sequence comparisons, and strain correspondence are assessed from the existing packets and receipt. They were not repeated by this reviewer. This review also incorporates the separate [2 October emericellamide competing-locus assessment](emericellamide-competing-locus-review-2026-10-02.md) and its five-row result table. The host reported an independent check of the full annotation counts and source-file MD5 verification. A fresh request for the [Caesar primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC10313767/) returned a browser challenge; the local `caesar-paper.txt` is HTML, not usable article text. No new full-text review of that article is claimed.

## Decisions

For acetylaszonalenin, accept the chemical identity and historical feature-2127 join for feature-only evaluation. Authenticated-standard evidence and the source-named workbook row meet those two requirements without recovering a native scan. Figure retention times belong to the figure's analytical comparison; they do not replace workbook retention time or supply scan membership.

Retain the relationship as provisional for headline eligibility on the evidence currently recorded. The [acetylaszonalenin packet](acetylaszonalenin.md) explicitly describes partial biochemical characterization, not experimental establishment of the complete reference pathway. Same-strain correspondence and strong chemistry do not fill that causal gap. The researcher may record a narrower evidence interpretation, with reasons, but this review does not upgrade partial support to a complete pathway claim. The pending correspondence, organization, and competing-locus assessments remain evidence gaps; serializing an already supported query is a separate input task. Reject the historical wrong-locus assignment, as the existing packet already does.

For emericellamide A, accept the source Type II named-product resolution and feature-8468 join. Type II is not a lower ordinal confidence class than Type I in this source. The published authenticated-standard route supports the named feature; the isomer warning in the reference paper does not, by itself, contradict that identification. Preserve the caveat and do not infer another congener. Under the historical inclusive 10^7 threshold, only the recorded Cheerios condition is present; the other two measurements are not evidence of biological absence.

The [emericellamide packet](emericellamide-a.md) records experimental reference evidence and full-length exact matches. Those support the proposed reference-supported classification. The new [competing-locus assessment](emericellamide-competing-locus-review-2026-10-02.md) found each retained reference exactly once among 10,534 released annotated proteins, resolving duplicate exact-reference ambiguity. Diverged alternatives and unannotated coding sequences were not assessed; 63 CDS records without released proteins were outside that search. The broader criterion remains unresolved unless the researcher documents why the completed source-specific check is sufficient under the contract. Recommend reference-supported eligibility once that criterion is settled and the researcher signs off. Do not describe sequence packaging as missing chemical proof, or sign off now on the strength of chemistry alone.

For pestalamide B, accept the chemical identity and historical feature-810 join, and recommend directly supported GCF eligibility pending researcher signoff. The [pestalamide packet](pestalamide-b.md) records isolated-product MS/NMR evidence and experimental representation of a member of the source family. That meets the contract's direct-GCF rule; a new native-strain experiment is not required. The named workbook target and the Table 6 maximum provide a traceable measured target. The experimental evidence recorded in the packet distinguishes this relationship from a correlation-only label.

Freezing the family roster, sample mappings, clustering provenance, and shared candidate universe remains input work. It does not erase the experimental evidence for the represented member. A separate exact-BGC query would have its own input requirements and must not silently replace the GCF query. No claim is made that all nine displayed family members independently produce the named metabolite.

## Gap register and scope

The [machine-readable register](../../data/curated/first-three-admission-decisions-2026-10-02.tsv) assigns every listed issue one disposition: `resolved_by_evidence`, `still_unresolved`, `human_decision`, or `input_only`. Each row states the source and consequence. Its 24 rows contain ten resolved evidence issues, three unresolved evidence issues, three human decisions, and eight input-only issues. Counts describe review issues, not labels, experiments, or independent queries. The added exact-reference duplicate row records a completed subcheck without claiming the broader competing-locus requirement is satisfied.

Researcher-led review by Vin Vomero remains pending. Public records can supply the evidence; external review is not a new prerequisite. Biological eligibility, feature-release readiness, and spectral readiness remain separate. These are three relationships from one source study, with repeated conditions preserved as measurements rather than new biological units. No biological admission count is added by this review.
