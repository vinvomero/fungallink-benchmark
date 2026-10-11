# Proposed member eligibility from retained data

The [eligibility table](../../data/curated/seven-admitted-member-eligibility-2026-10-03.tsv) completes a local mapping review of all 51 rows in the earlier member staging table. Of 36 previously unjoined memberships, 35 now have exact documentary joins to study rows and observation IDs. One remains unresolved after inspection. No row is left marked unattempted.

All seven admitted relationships remain unchanged: five GCF queries and two BGC queries. The 51 rows comprise 49 displayed GCF memberships and two BGC anchors, not independent biological labels or genomes. This is a proposed input disposition, with no release freeze, scoring or change to biological eligibility.

Requested route: `gpt-6-astra`, `medium` reasoning. No serving-side model/effort receipt was exposed. Humanizer rules and the canonical plan apply.

| Mapping result | Membership rows | Proposed treatment |
|---|---:|---|
| Existing reviewed documentary mapping or admitted anchor | 11 | Include with existing scope limits |
| Public archive annotation namespace joined to study table | 12 | Include as a documentary mapping |
| Historical author-workbook-derived crosswalk joined to study table | 23 | Include for internal work with that provenance explicit |
| Existing identity conflicts | 4 | Keep candidate sets; withhold a resolved per-member mapping |
| No usable source identity key after local review | 1 | Keep the member; withhold an observation assignment |

Thus 46 membership rows have proposed mapped observations. These are not 46 method-ready queries. The distinction between the 23 documentary rows and 23 historical-provenance rows is retained in separate disposition fields.

For the twelve new public joins, the member's annotation IDs contain a JGI project namespace also present in exactly one Supplementary Table 2 roster row. The matching rule uses `jgi.p_<exact namespace>_` and retains the complete original identifiers and suffixes. Each join also agrees with the historical correspondence row. This is namespace correspondence, not a sequence comparison or proof of unchanged culture identity.

The other 23 new joins depend on the retained historical display-label bridge. Its repository copy is [historical-label-strain-assembly-crosswalk-2026-09-20.tsv](../../data/raw/sources/caesar-2023/historical-label-strain-assembly-crosswalk-2026-09-20.tsv), SHA-256 `d5b107a3c6c947a30cca8022b5357eef396fa3b33747314a84ac798d34d8cf99`. Its source was an author-workbook-derived reconciliation. It is not independently public evidence for the FMGX/UNCG-to-strain edge. Exact display labels identify its rows; their assembly assertions and punctuation-insensitive strain identifiers then match the public study roster. Species names and index order were not used. The new table embeds each historical row, physical TSV row number and source fingerprint, so its assertions remain inspectable without a neighboring checkout. The host registered the import in `legacy-imports.tsv`; public redistribution rights remain separate.

FMGX0070 is the unresolved member of NRPSLIKE_59. Its historical row has an empty strain and accession, while the retained archive provides a generic node-region label and `g*.t1` annotation IDs. Neither supplies a permitted exact study-roster key. The historical description “Aspergillus sp. JW Fungus” was not used to guess a culture. This completed negative mapping result is not a negative biological label. It also does not prove why the source paper scored eleven strains while displaying twelve members.

Four pestalamide member rows retain their prior conflicts. FMGX0055 still has the A1 versus A1/83 discrepancy; FMGX0053 retains ATCC13490 versus ATCC13496. The historical table assigns individual cultures to FMGX0054 and FMGX0057, but this historical assertion does not override the recorded unresolved public orientation. Both therefore retain the same six-acquisition candidate set for ATCC9029 and ATCC64974.

That last ambiguity has a narrower set-level question: both members belong to NRPSPKS_85, and both candidate cultures carry the source assertion Aspni_NRRL3. A declared GCF workflow may be able to use the two-culture union without choosing which FMGX label belongs to which culture. This unit leaves that scope decision open. Withholding resolved per-member assignments does not establish that the union must be excluded from every GCF analysis, and the two cultures must not become two asserted independent genomes merely because both have measurements.

The table deduplicates acquisition IDs within every row and supplies deduplicated per-query counts. Observation IDs join by exact acquisition membership to the retained label and condition tables. Candidate sets are preserved even when a per-member mapping is withheld.

| Query | Full retained member/anchor rows | Unique candidate acquisitions | Unique acquisitions under the proposed per-member mapping, including historical provenance |
|---|---:|---:|---:|
| Corrected acetylaszonalenin core | 1 | 3 | 3 |
| Emericellamide A BGC | 1 | 3 | 3 |
| NRPSPKS_85 | 9 | 27 | 15 |
| TERPENE_40 | 11 | 35 | 35 |
| NRPSLIKE_59 | 12 | 35 | 35 |
| NRPKS_18 | 10 | 34 | 34 |
| NRPS_66 | 7 | 21 | 21 |

These are acquisition counts. Repeated conditions, cultures, aliases and related query memberships do not create independent genomes. Historical `pending_verification` or `biological_sample_unreviewed` crosswalk fields are preserved source statuses; they do not introduce a new objection to the already admitted biological relationships. The acetylaszonalenin query remains its corrected named core. No all-member product-production claim is made for any family.

Before constructing co-occurrence inputs, specify what a genomic zero means. Absence from a fixed deposited source-family roster can be used only within its declared covered population and with incomplete mappings visible. It is not proof of biological genomic absence. A biological-absence assertion needs a complete-enough search under its declared scope; the historical source-selected track does not automatically require rebuilding the whole cohort's BGC universe. Unknown clustering-run details remain disclosed provenance limits rather than new biological demotions.

The next concrete scope decision is whether the unresolved Aspni_NRRL3 pair can enter the historical GCF input as an explicitly shared two-culture set. Then construct the proposed source-membership/observation table with these disposition and provenance fields intact, leaving FMGX0070 and true identity conflicts unresolved rather than converting them to zeros. The full source-family rosters remain unchanged.

Checks confirmed 51 unique and preserved membership keys, all 35 new joins, exact observation coverage of each candidate set, per-query acquisition deduplication and unchanged canonical label-ledger bytes. Scratch metadata code and the verification receipt are under `data/interim/seven-admitted-member-eligibility/`. No downloads, sequence extraction, operational biological work or production-code changes were performed.
