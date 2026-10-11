# Exact-B reference records

Reviewed 2026-10-03 under the [canonical plan](../plans/2026-09-30-2052-benchmark-paper-plan.md) and [benchmark contract](../../protocol/benchmark-contract.md). Notoamide B is ready for a researcher decision under the existing reference-supported class. Emericellamide B remains provisional. These are recommendations, not admissions or scientific signoff; no canonical ledger was changed.

Requested route: `gpt-6-astra / medium`; no serving-side receipt was exposed, so the actual model and effort are unverified. Humanizer rules applied. The Life Science Research `ncbi-entrez-skill/scripts/ncbi_entrez.py` script performed every Entrez call.

## Notoamide B

The earlier [sampled-correspondence packet](notoamide-b-sampled-correspondence-2026-10-03.md) supplies the FMGX0064 / Asposti1 / NRRL420 anchor, measured feature9213, quantified reference correspondence and bounded ambiguity assessment. This review adds bibliographic evidence, with no new sequence analysis.

Four sources distinguish the reference assignment from full mechanistic reconstruction:

- [Ding et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2941195/), abstract, Figure 1 and Results on cluster localization, reports a reference cluster in the producing MF297-2 strain and experimentally characterized early pathway activities. Primary full-text sections were inspected through the web tool; direct local retrieval returned a browser challenge. This source was newly inspected for this packet, not a newly published discovery.
- [Finefield et al. 2011, PMID 21714564](https://pubmed.ncbi.nlm.nih.gov/21714564/), retrieved PubMed abstract, reports intact precursor incorporation into exact notoamide B in both named reference fungi. It supports the native precursor-product relationship, not a gene-deletion result. Full text was inaccessible in the bounded attempt.
- [Sunderhaus et al. 2013, PMID 23249380](https://pubmed.ncbi.nlm.nih.gov/23249380/), retrieved PubMed abstract, reports another precursor-incorporation result ending in B in those fungi. Again, abstract-only inspection; neither a new native locus perturbation nor proof of every intervening assignment.
- [Fraley et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7483341/), Results and Figure 1, experimentally identifies the exact-B products against standards from reference-locus enzymes. The full HTML was retrieved and inspected this time, extending the earlier indexed-text access. Scheme 2 and the conclusion retain uncertainty about intervening steps and native reaction order. That uncertainty does not erase the measured exact-B outcome.

My assessment is that the combined published cluster assignment, native exact-product incorporation and exact-B reference-enzyme outcome support ordinary reference-supported review. The contract asks for an experimentally supported reference pathway; it does not require a complete minimal gene set, every enzyme mechanism, or a whole-cluster knockout. Calling all remaining mechanistic uncertainty a mandatory reference-assignment failure would add a gate that the contract does not state. No separate partial-pathway class is needed solely for that reason.

Recommend `source:NRPS_66 -> feature9213`, anchored to FMGX0064, at source-named B resolution without an enantiomer claim. A researcher must still record acceptance of this reference-evidence rationale and the existing identity, coverage, organization and bounded competing-locus criteria. The evidence does not establish necessity or sufficiency of the entire drawn region, production by all seven family members, absence of other genomic contributors, or direct perturbation of NRRL420. Preserve the overlapping family views and one related pathway group. Release inputs and spectral joins remain separate.

## Emericellamide B

The [prior exact-product packet](exact-product-gap-resolution-2026-10-02.md) remains correct about the missing exact-B experimental reference assignment. Fresh PubMed abstracts confirm that [Chiang et al. 2008, PMID 18559263](https://pubmed.ncbi.nlm.nih.gov/18559263/) experimentally links A and C-F, while [Oh et al. 2007, PMID 17323993](https://pubmed.ncbi.nlm.nih.gov/17323993/) reports B isolation and structural assignment without a locus assignment. These were previously known sources, freshly retrieved here.

The useful new primary inspection was [Park et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7885118/). Its complete article XML was retrieved through Europe PMC. The emericellamide Results paragraph and Figure 6B caption were inspected: the caption expressly identifies the illustrated structure as emericellamide A. Changes in a general emericellamide signal and reference-cluster expression do not establish exact B. The later [AtfA/AtfB study, PMID 36766807](https://pubmed.ncbi.nlm.nih.gov/36766807/) was screened at abstract level; it describes expression regulation, not an exact-B experimental assignment.

Retain `source:HRPKS_71 -> feature5402` as provisional source recovery. The reopening record is an existing primary experiment or a documented, researcher-reviewed assignment argument that connects the reference locus specifically to B. It need not characterize every enzyme or perturb the Caesar culture. A/C-F support, a database B name, and co-occurrence alone do not close this congener-specific gap. This unsuccessful bounded search creates no negative label.

## Retrieval scope and provenance

Two finite search rounds used PubMed `esearch` with `retmax=10`, followed by `efetch` XML. Round 1 queried each product with biosynthesis/cluster terms, sorted by publication date: 10 of 42 notoamide hits and 10 of 11 emericellamide hits were returned. Round 2 narrowed to notoamide biosynthesis-title/NotI/NotH/NotD terms excluding indexed reviews, and exact emericellamide B terms: eight and one returned records respectively. PubMed translated the second emericellamide phrase unexpectedly as an author clause; the preserved translation makes that limitation visible. No exhaustive absence claim follows. Three additional named citations were fetched directly from Fraley's bibliography, without another search round. Altogether 32 unique PubMed records were screened.

Raw queries, PubMed XML, retrieved article material and download receipts are under `data/raw/sources/expansion-2026-10-03/caesar-reference/`. Scratch `data/interim/caesar-reference-records/` retains script receipts, a 32-record screening index and SHA-256 manifest. Failed Europe PMC XML calls returned HTTP 500; three local PMC HTML responses were browser challenges. Those bytes are failed-access records, not inspected full texts. No supplement is claimed as inspected.

Fraley full HTML SHA-256: `543c163f7add6f8c01803952a7e064f75afa60e2081606b4fa010b1d7c8bbc72`. Park article XML SHA-256: `77b41483e70e76fd480ee1c5dfe283036a709a530ef5838b1a7fd7f8b9210f59`. Retrieval used Python 3.13.5 and the installed Life Science Research 1.0.3 Entrez script. Article reuse rights remain those of the source publishers; retained material is private working evidence, not authorization to redistribute.

The [companion TSV](../../data/curated/caesar-reference-records-2026-10-03.tsv) preserves two relationship records and separates reference appraisal from overall status. No new independent query, pathway, biological sample, method version, candidate universe or spectral-ready target was added. Both cases remain source-selected retrospective material with known-reference exposure.
