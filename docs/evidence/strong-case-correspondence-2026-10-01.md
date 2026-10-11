# Griseofulvin and aspernidine A correspondence assessment

Started 2026-10-01; completed after resumption on 2026-10-02. This assessment proposes dispositions for two existing relationships. It changes no authoritative label, admission count, or protocol. Requested route: `gpt-6-astra` / `medium`; no serving-side receipt was exposed. Work resumed after the reported credit interruption; no claim about the actual serving model is made.

Both relationships remain **provisional for the main comparison** under the canonical plan. Aspernidine A has advanced: the original family artifact establishes correspondence to the reference's annotated locus through six identical versioned protein identifiers in the same order. Repeating an alignment solely to rediscover those record identities is unnecessary. What remains is a documented competing-locus assessment and a defensible scope for transferring this evidence to the declared family. Griseofulvin still needs the reference-to-sampled-member connection itself.

## What the published family evidence establishes

The original publisher archive, `data/raw/sources/caesar-2023/41589_2023_1276_MOESM3_ESM.zip`, was read directly. Only display labels and annotation identifiers were analyzed; no sequence comparison was performed. Its SHA-256 is `0cef389310eccd261255e51919e7fe5f1f772cc73be2b0d42e0f5f8e30245a54`.

[Caesar's methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC10313767/) describe antiSMASH 6 predictions followed by custom domain-based family construction. Shared adjacent domains were a prerequisite for comparing cluster pairs; the similarity metric averaged identities between domains assigned to the same Pfam model. Both families here used cutoff 70. That number is not a measurement of 70% full-length locus identity or coverage. The procedure supplies real similarity and limited organization evidence, but does not report complete reference-to-member coverage, conservation of every relevant gene, or exclusion of another locus. Thresholds were selected using known associations, so these are exposed source families. They are suitable for retrospective source recovery with that limitation recorded.

Membership can define a versioned GCF query. It cannot, by itself, replace the canonical plan's reference-transfer criteria. An inserted MIBiG reference is an experimental anchor, not an experimentally tested Caesar culture. The distinction matters even when the reference and sampled annotations share an assembly.

## Griseofulvin

The `NRPKS_18.html` member has SHA-256 `c662bd2e7da63410bc1ea06a6613b9a393b1894f41880dbcf5bbf16f981efc03`. It contains ten sampled labels and two separate MIBiG anchors, `BGC0000070.1` and `BGC0001284.1`. The sampled roster below is complete at the displayed-label level. Culture and assembly columns are retained historical crosswalk assertions, checked against public Supplementary Table 2 where named; they are not a new public FMGX crosswalk.

| Display label | Historical culture mapping | Assembly or project accession |
| --- | --- | --- |
| FMGX0093 | ATCC 10409 | Penac1 |
| FMGX0099 | ATCC 48919 | Penla1 |
| FMGX0108 | ATCC 10419 | Penca1 |
| FMGX0109 | ATCC 48735 | GCA_000943765.1 |
| FMGX0114 | NRRL 13627 | JAPDEY000000000 |
| FMGX0127 | ATCC 10490 | Penra1 |
| FMGX0135 | NRRL 1001 | JAPDFE000000000 |
| FMGX0137 | NRRL 3503 | JAPDFG000000000 |
| FMGX0138 | NRRL 3647 | JAPDFH000000000 |
| UNCG0006 | G173 | JAPDKY000000000 |

[Chooi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC2884005/) identify the griseofulvin experimental reference strain as *P. aethiopicum* IBT 5753 and provide product-specific genetic evidence. None of the ten historical culture labels is IBT 5753. This does not prove there is no alias; it means one has not been established. The tempting species-level bridge through FMGX0099 is insufficient: [JGI identifies Penla1 as *P. lanosocoeruleum* ATCC 48919](https://myco-lb.jgi.doe.gov/Penla1/Penla1.home.html), while the [JCM catalogue](https://www.jcm.riken.jp/cgi-bin/jcm/jcm_number?JCM=22830) lists ATCC 48919 with FRR 2007, IAM 13784 and MRC 422, without identifying it as IBT 5753. A species-name revision cannot establish culture identity.

The existing packet's feature 2854 join and Type I chemical evidence stand. Its illustrated *A. panamensis* NRRL 1786 chemical observation does not identify an experimentally represented member of this ten-label roster. It should remain chemical evidence, not be repurposed as locus provenance.

Proposed scope: `source:NRPKS_18` to feature `2854`, one griseofulvin pathway group, with the ten sampled labels retained and reference anchors explicitly distinguished. Use this as a provisional source-recovery relationship. Main-comparison admission needs a documented link from the experimentally established griseofulvin pathway to a sampled member, addressing identity/coverage, product-relevant gene content and organization, and competing loci. The second anchor and shared family label do not settle product specificity. No evidence here justifies a direct class or extending griseofulvin support to every congener.

## Aspernidine A

`TERPENE_40.html`, SHA-256 `8a3e7257f951ac875a08e77dbac0361efe1b69f60716fd75550d77161824a8af`, contains eleven sampled labels: FMGX0012, FMGX0016, FMGX0031, FMGX0043, FMGX0048, FMGX0049, FMGX0050, FMGX0051, FMGX0061, FMGX0069 and FMGX0071. Its reference is `BGC0001722.1`.

All six versioned protein identifiers in that reference drawing occur consecutively and in the same order among the seventeen identifiers in the `FMGX0049 / BN001306.1.region007` drawing. This is record-level evidence of the same annotated reference locus inside a broader source region. It closes the earlier question of whether the source region merely happens to share the reference chromosome accession. It establishes displayed gene-content correspondence and ordering for those six records, without claiming a fresh identity/coverage measurement, completeness of the broad region, or a comparison of independently sequenced cultures.

Public Supplementary Table 2 assigns ATCC 38163 to GCA_000011425.1. The historical crosswalk assigns FMGX0049 to that culture and assembly. The [FGSC A4 catalogue](https://www.fgsc.net/strain_detail.php?id=4) identifies ATCC 38163 as an alias. [Yaegashi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3713076/) place their product-specific NMR and genetic evidence in an FGSC A4 mutant background. Together these support reference-background correspondence. They do not establish that Caesar assayed the experimentally perturbed culture, nor prove its locus unchanged through culture history. Directly supported status is therefore not established by this check.

For an assembly-defined family query, identical versioned annotation records are affirmative correspondence evidence. A separate alignment of the same records need not be demanded as a ritual. The canonical criteria still need an explicit adjudication of whether this record identity satisfies identity/coverage for the declared assembly-defined object; it cannot be reported as a measured alignment of the historical culture. The remaining biological blocker is a recorded assessment of alternative loci and the scope of the family-product inference. The selected HTML files are not an assembly-wide locus inventory, so absence of another locus within them cannot supply that assessment.

Retain `source:TERPENE_40` to feature `3485` as the proposed source query. `NRPKS_38.html` (SHA-256 `99ab9f08aafc5fc3319fb02054be00d579f415a4f43e786a7cd975523b2df7b8`) contains the same reference and FMGX0049 locus. Its twelve-member roster shares ten labels with TERPENE_40, adds FMGX0023 and FMGX0078, and omits FMGX0016. These are alternate source-family views of one supported reference pathway, not two independent positives. A union, intersection or narrowed FMGX0049-only query would be a newly declared query, not the historical TERPENE_40 association. In particular, FMGX0016 has no NRPKS_38 label in the artifact; the TERPENE name alone neither invalidates the reference nor proves an intact aspernidine pathway in every member.

The Type II chemical call and feature 3485 join remain supported by the earlier packet. Proposed class remains provisional, now with annotated reference-locus correspondence established. The practical next decision is a bounded adjudication of record identity, alternative-locus evidence and family scope. Repeating general literature searches or requiring a new experiment in every member would not address the remaining criterion.

## Release consequences and verification

Both can be packaged as exposed, provisional source-recovery examples once the sample crosswalk and feature candidate universe are frozen. Neither contributes to headline main-comparison counts from this assessment. A complete all-member production claim is unnecessary for family-level evaluation, but the released member roster and the supported extent of the family-product relationship must be explicit. Detailed causal assignment to every culture is future precision, not a universal family-track gate.

New wet-lab work, an outside reviewer, native MS/MS scan joins, and unfamiliar-pathway generalization are not biological admission prerequisites here. A frozen public/reusable sample crosswalk and candidate universe are method-input requirements. The independent scientific-review limitation must be disclosed; it does not turn unresolved evidence into a negative label.

Metadata checks verified 10/11/12 unique sampled labels in NRPKS_18/TERPENE_40/NRPKS_38, the ten-label overlap of the latter two, and the six-record ordered match inside FMGX0049. Scratch extracts are in ignored `data/interim/strong-case-correspondence/`. The historical crosswalk was read from the neighboring repository without modification: `fungallink/output/caesar-response-2026-09-20/caesar-label-strain-assembly-crosswalk.tsv`, SHA-256 `d5b107a3c6c947a30cca8022b5357eef396fa3b33747314a84ac798d34d8cf99`. It is supporting provenance, not a portable release dependency or execution instruction.

The accompanying TSV has exactly two relationship rows. Earlier packets, the evidence index and the authoritative label ledger were not edited. No external correspondence, publication or Git operation was performed.
