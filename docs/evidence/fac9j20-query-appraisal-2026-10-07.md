# AtFAC9J20 locus-to-measured-product appraisal

The three historical relationships support biological eligibility at the tested-locus scope: the benzomalvin locus to facms0004, the sesterterpenoid locus to facms0005, and the valactamide locus to facms0017. I recommend keeping all three for scientific adjudication as directly supported labels. The unnamed sesterterpenoid qualifies at its measured-product resolution. Valactamide eligibility is conditional on accepting the documented correspondence between the paper's valA/valB and the deposited lptB/lptA annotations. This appraisal makes no canonical admissions.

Exact accession-based query envelopes can now be proposed. Missing sequence access is no longer the obstacle for these three cases. The remaining scoring inputs are a complete candidate-feature pool, its sample mapping, and a supported join from the historical facms products to released feature IDs. Those gaps do not erase the biological evidence.

## Record and query scope

The existing [KX449366.1 GenBank record](https://www.ncbi.nlm.nih.gov/nuccore/KX449366.1) was retrieved on 2026-10-07 as `data/raw/fac9j20-query-appraisal-2026-10-07/KX449366.1.gb`. It is a circular 118,762-bp shuttle vector derived from *Aspergillus terreus* ATCC 20542. The [paper](https://doi.org/10.1038/nchembio.2408), Figure 3a, explicitly divides that length into a 102,722-bp insert and 16,040-bp vector. The full record must not be assigned to each of its three BGCs.

For a source-defined BGC-to-feature release, use the smallest contiguous envelope containing the deposited genes corresponding to the source-supported pathway roster. Coordinates below are 1-based inclusive on KX449366.1, in accession orientation. This proposed `gene-envelope v1` rule retains intervening sequence and excludes extra flanks. It defines reproducible query inputs; it does not claim experimentally established outer BGC boundaries or that these sequences alone are sufficient for production.

| Measured target | Deposited roster | Proposed query envelope | Length |
|---|---|---:|---:|
| facms0004, benzomalvin A/D | benZ, benY, benX | 77570..91727 | 14,158 bp |
| facms0005, unnamed sesterterpenoid | sttB, sttA | 17667..22733 | 5,067 bp |
| facms0017, valactamide A | lptB, lptA, corresponding to paper valA, valB | 50180..66867 | 16,688 bp |

These are three distinct pathway candidates, supported by separate gene rosters and selective product loss in the source. They share one FAC, donor strain, study, and heterologous host context. They are not three independent strains or cohorts; relatedness and shared experimental context belong in uncertainty and exposure records. No GCF query is established here.

The deposited annotations and Supplementary Table 2 (printed p.32) correspond as follows. The paper gives strand-oriented start/stop values; its ranges below are reordered only for comparison.

| Paper gene | Paper range | GenBank range / strand | Protein accession |
|---|---:|---|---|
| benZ | 77576..84859 | 77570..84852, minus | AQM58287.1 |
| benY | 86362..89695 | 86356..89688, plus | AQM58288.1 |
| benX | 90495..91734 | 90489..91727, minus | AQM58289.1 |
| sttB | 17673..19694 | 17667..19687, minus | AQM58280.1 |
| sttA | 20124..22740 | 20118..22733, plus | AQM58281.1 |
| valA | 50187..57999 | lptB: 50180..57992, minus | AQM58285.1 |
| valB | 58960..66874 | lptA: 58954..66867, plus | AQM58286.1 |

The paper's lower endpoints are six bases above the deposited endpoints except valA, whose lower endpoint is seven bases above; all upper endpoints are seven bases above. These differences are retained, not silently converted by a uniform shift. The gene-level identity of benX/Y/Z and sttA/B is explicit in both sources. The val alias mapping is an inference supported by the same FAC, nearby matching locations, orientation, adjacency, and matching PKS versus NRPS annotation. GenBank does not explicitly list valA or valB as synonyms. Supplementary Table 2 identifies valA as the corrected single gene corresponding to NIH2624 ATEG_03575 and ATEG_03574; it identifies valB as ATEG_03576. No transfer to NIH2624 or another assembly is being claimed.

There is also a one-base insert/vector seam discrepancy: GenBank labels 102722..118762 as `pFAC cloning vector`, an inclusive length of 16,041. The article reports 16,040 vector bases. All proposed envelopes lie far from that seam, so the discrepancy does not change their extracted sequence. Its cause remains unresolved.

## Biological and measurement evidence

Supplementary Figure 2A-C (pp.3-4), visually inspected here, links each historical facms label to an MS1 spectrum, selected-ion chromatogram, FAC background, corresponding deletion, and native-parent trace. Supplementary Table 3 (p.33), also visually inspected, distinguishes the three product responses. Article Figure 3 reports the same selective assignment with biological replicate summaries. These observations concern the tested AtFAC9J20 loci directly. A new universal homology threshold would add no relevant evidence for this scope.

**facms0004.** Deletion of benY or benZ removes benzomalvin A/D; benX deletion decreases production without eliminating it. The article discusses possible host methyltransferase rescue. The source therefore supports the ben locus relationship, but not the claim that every named gene is individually essential. Article identification results and Supplementary Figures 4-5 (pp.14-15) support the A/D atropisomer target through synthetic-standard comparison, MS/MS, and coinjection. The reported peaks near 38 and 41 minutes belong to one product-resolution target, not two independent successes. Panel 2A reports m/z 382.153; article identification text reports 382.1547. Table 1/panel and article neutral formulas also differ. Preserve those source fields; use the named historical target rather than a mass-only reconstructed join.

**facms0005.** The source reports that sttA and sttB deletion each removes the measured sesterterpenoid while benzomalvin A/D and valactamide A remain detected (Table 3). Supplementary Figure 2B and Figures 8-10 (pp.19-20) support a measured target with reported neutral formula C25H36O2 and terpenoid-class MS/MS. The paper discusses possible structural relatives without establishing a particular structure. Eligibility should therefore name `unnamed measured sesterterpenoid facms0005`, not ophiobolin or variecolin. The panel reports m/z 369.277, Figure 8 reports 369.2783, and Figure 9 reports 369.2710. This source discrepancy prevents using those numbers as an exact raw-feature join; it does not make the historical target unmeasured or invalidate the selective deletion evidence.

**facms0017.** Deletion of either valA or valB removes facms0017 while the other two products remain detected (Table 3). Discovery used AtFAC9J20-ΔbenY, but the article and Supplementary Figures 2C, 11 and 12 also report the target in the parental FAC and donor strain. Thus the label is not restricted to a signal observed only in the discovery deletion background. Figures 11-19 (pp.21-26), article Figure 4, and the structure-results text support valactamide A with NMR/MS and L-Val/L-Ile assignment. Article Figure 4 expressly leaves methyl-substituent stereochemistry undetermined. Do not inflate this into complete absolute stereochemical resolution or extend the present row to valactamides B-H. The historical facms0017-to-valactamide A naming is explicit in the article, not inferred from mass.

The Table 3 null deletion removes benX through valA and loses benzomalvin and valactamide while retaining the terpenoid. Along with the individual deletions, this supports three pathway assignments within the shared FAC. It does not establish complete biosynthetic autonomy or rule out every contribution from the host.

## Readiness and disposition

Recommend biological eligibility for all three source-defined tested-locus relationships after scientific review, using the target resolutions above. The val gene aliases need an explicit reviewed correspondence decision; their source evidence is strong enough to recommend that decision rather than leave the locus unspecified. The accession-based envelopes are concrete proposals for that review. If a method requires broader predicted BGC boundaries, declare a separate boundary procedure and preserve the tested-gene roster instead of expanding silently.

The historical label-to-measurement relationship is traceable at article/supplement level. No released matrix row, full candidate universe, or native MS/MS scan join is established by this packet. A complete pool and mapping are needed before comparison scores can be computed. Missing MS/MS is only a spectral-track limitation. Neither an exact structural name nor a complete candidate pool is a prerequisite for the biological recommendation.

The specific analytical records still needed are the complete processed feature CSV/table with stable row IDs, m/z, retention-time units and all sample intensities; a sample/acquisition map covering FAC background, deletant, controls, replicate and processing inclusion; and the original facms0004/0005/0017-to-feature-row crosswalk, including adduct and atropisomer grouping. A spectral extension would also need native scan IDs or a validated spectral export joined to those rows. This is an input specification, not a request sent to the authors.

FAC-Score selected these discoveries, and the 2017 paper and product-annotated sequence are public prior evidence. Methods must disclose reference/training exposure and keep gold product names and annotations out of method inputs unless the track expressly permits those fields. These cases are retrospective source evidence, not unseen-pathway tests.

## Provenance and checks

The [three-row TSV](../../data/curated/fac9j20-query-appraisal-2026-10-07.tsv) records proposed envelopes, sequence hashes, source locators, separate readiness fields, recommendations, and shared context. [Appraisal provenance](../../data/raw/fac9j20-query-appraisal-2026-10-07/appraisal-provenance.json) records raw-file hashes, sizes, source paths, retrieval URL, parsed annotations, the full-sequence hash, and the TSV hash. GenBank file SHA-256: `8a83376c0937ce3f4ce280a759c67f0712546ccfd418f138b8e2b12873857211`. Sequence hashes use uppercase ASCII bases without a header or newline.

The retained supplement PDF hash is `6ea1aa7dc34516cf8dcf4b0003b3a9798ab4569106d8f1027dc94f22bcde0d72`. This review read the existing inventory, article text, supplement captions/tables, and accession metadata; visually inspected supplement pp.3, 4, 13, 32 and 33; and parsed the downloaded record with Biopython 1.88. Later chemistry captions and article text were read without re-inspecting every NMR/MS image. Rendered pages and the finite artifact-generation script are retained in `scratch/fac9j20-query-appraisal-2026-10-07/`. No new experiments, sequence design, rankings, external correspondence, public release, or canonical ledger edits were performed.

The canonical plan, benchmark contract, and humanizer skill were read. The humanizer's referenced secondary guide was absent; its main rules were applied. Requested route: `gpt-6-astra`, reasoning `medium`; actual serving model and effort were not exposed by a receipt. This is an automated scientific appraisal for host verification and later scientific review, not independent biological sign-off.


Host verification matched eight source/derived file fingerprints, the full record identity and length, and all three envelope coordinates, lengths and sequence hashes against the deposited gene annotations. Supplementary Tables2/3 on PDF pages32/33 were inspected visually. The valA coordinate exception was corrected during review and remains explicit. Receipt: `data/raw/fac9j20-query-appraisal-2026-10-07/host-verification.json`. These checks do not constitute researcher admission or an independent biological review.
