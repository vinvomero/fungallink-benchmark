# Notoamide B sampled correspondence

Reviewed 2026-10-03 for relationship 21, feature9213. **A defensible sampled homology anchor is now documented in FMGX0064 / Asposti1 / NRRL420.** The overall relationship remains provisional: the reviewed reference literature provides a proposed pathway with experimental support for particular steps, including the exact-B reaction, rather than an established complete reference-locus-to-B assignment under a recorded researcher criterion. Sequence correspondence and sample provenance are no longer the same unresolved question.

Requested route: `gpt-6-astra / medium`; actual serving model/effort receipt unavailable. Humanizer rules applied. Authority remains the [canonical plan](../plans/2026-09-30-2052-benchmark-paper-plan.md) and [contract](../../protocol/benchmark-contract.md). No admissions, scientific signoff or canonical ledgers were changed.

## Comparison across the seven represented members

The publisher NRPS_66 drawing contains 18 BGC0000818.1 reference proteins, 19 BGC0001084.1 reference proteins and 98 proteins across seven sampled regions. Each reference protein was scored against every protein in each sampled region: **3,626 pairwise scores and 259 retained best matches**. Both reference drawings and all seven members remain in the [TSV](../../data/curated/notoamide-b-sampled-correspondence-2026-10-03.tsv), including weak and reused winners. All scores are retained in scratch. No additional regions were downloaded or reconstructed.

The ten-record notAâ€“J block in BGC0000818.1 was used to compare candidates because it includes the reference core and product-specific reaction annotation. This is a comparison subset, not a claim that all ten are necessary, sufficient, experimentally characterized, or the complete pathway boundary. Other reference records remain in the results. The summary counts are mechanical correspondence descriptors, not an identity threshold or admission rule.

| Member | Displayed proteins | Distinct winners for ten-record block | Reciprocal winners within this drawing | NotI winner identity % | NotI reference coverage % | NotI sample coverage % |
|---|---:|---:|---:|---:|---:|---:|
| FMGX0011 | 9 | 5 | 5 | 44.780 | 99.538 | 94.518 |
| FMGX0014 | 20 | 10 | 10 | 69.482 | 84.758 | 94.832 |
| FMGX0019 | 7 | 5 | 4 | 44.836 | 98.383 | 95.302 |
| FMGX0028 | 9 | 5 | 5 | 44.235 | 98.152 | 94.444 |
| FMGX0030 | 20 | 9 | 7 | 28.652 | 82.217 | 73.402 |
| FMGX0064 | 17 | 10 | 10 | 69.515 | 100.000 | 98.409 |
| FMGX0082 | 16 | 8 | 8 | 68.822 | 100.000 | 99.540 |

FMGX0014 and FMGX0064 have ten distinct reciprocal winners. FMGX0014 preserves a continuous reversed order but has lower paired coverage for the product-specific reaction record. FMGX0064 was selected for provenance follow-up because it retains full reference coverage for that record and near-full two-sided coverage throughout the ten-record block. This was retrospective curator prioritization after inspecting all seven, not a predeclared statistical classifier. A diagnostic mean of best score/reference self-score over the ten records ranks FMGX0014 slightly higher overall (0.690227 versus 0.677665); it was not used to override the product-specific coverage concern. The choice does not establish that FMGX0014 is biologically ineligible.

## FMGX0064 provides a traceable sampled anchor

All 17 FMGX0064 protein identifiers carry the Asposti1 prefix, and the publisher identifies its region as scaffold_55.region001. [JGI's official Asposti1 v1.0 page](https://mycocosm.jgi.doe.gov/Asposti1/Asposti1.home.html) names the sequenced strain as Aspergillus ostianus CBS 103.07. The [JCM1959 catalogue](https://www.jcm.riken.jp/cgi-bin/jcm/jcm_number?JCM=1959) explicitly lists CBS 103.07 and NRRL420 as collection aliases. This is a documentary culture-collection correspondence, not proof that the sequenced and assayed vials were genetically unchanged.

Caesar Supplementary Table2 row53 assigns A. ostianus NRRL420 to Asposti1; the [curated source roster](../../data/curated/caesar-study-roster-2026-10-02.tsv) joins that exact strain label to workbook columns JF, JG and JH. A fresh read of feature9213, Sheet1 row9221, gives **35,800,000; 28,100,000; 88,300,000** for the NRRL420 Cheerios, Oats and Rice observations respectively. These are three source acquisitions, not three strains or a new presence rule.

Supplementary Table4 names the historical feature as notoamide B. The paired standard panel Figure2h illustrates NRRL236, not NRRL420. Thus the NRRL420 bridge is an observation of the same source-defined feature under the published feature assignment; it is not a fresh authenticated-standard comparison for NRRL420. No chiral assignment or native scan join is inferred. The chemistry/name resolution established in the [earlier packet](nine-reference-resolution-2026-10-02.md) is retained at source-named B resolution.

The quantified block in FMGX0064 is:

| Reference protein | Sample annotation | Identities / paired residues | Identity % | Reference paired coverage % | Sample paired coverage % |
|---|---|---:|---:|---:|---:|
| AGC83572.1 | jgi.p_Asposti1_114569 | 234/336 | 69.643 | 94.118 | 98.534 |
| AGC83573.1 | jgi.p_Asposti1_114705 | 321/447 | 71.812 | 98.242 | 98.675 |
| AGC83574.1 | jgi.p_Asposti1_114556 | 315/425 | 74.118 | 99.765 | 99.299 |
| AGC83575.1 | jgi.p_Asposti1_178383 | 408/608 | 67.105 | 99.346 | 98.541 |
| AGC83576.1 | jgi.p_Asposti1_114803 | 1360/2181 | 62.357 | 98.022 | 96.847 |
| AGC83577.1 | jgi.p_Asposti1_114806 | 303/434 | 69.816 | 99.770 | 96.231 |
| AGC83578.1 | jgi.p_Asposti1_200786 | 390/536 | 72.761 | 98.529 | 99.814 |
| AGC83579.1 | jgi.p_Asposti1_188905 | 337/497 | 67.807 | 99.599 | 99.400 |
| AGC83580.1 | jgi.p_Asposti1_200791 | 301/433 | 69.515 | 100.000 | 98.409 |
| AGC83581.1 | jgi.p_Asposti1_114829 | 240/358 | 67.039 | 98.895 | 97.019 |

The ten identities range from 62.357% to 74.118%; reference coverage is 94.118â€“100%, and sample coverage is 96.231â€“99.814%. Each record has a unique highest-scoring counterpart within the 17-protein drawing and is also the unique reverse winner within the 18-protein reference drawing. This bounded reciprocal check separates the two related monooxygenase annotations: the NotI reference AGC83580.1 selects jgi.p_Asposti1_200791, while the other upstream reference selects a different sampled protein. The second historical reference's NotI record ADM34142.1 independently selects the same sampled annotation at 308/433 identities (71.132%), 100% reference coverage and 98.409% sample coverage.

Organization differs from the reference. In reference Aâ€“J order, sampled indices are 7,6,5,4,9,10,11,12,13,14: the Aâ€“D block is reversed in display order, then Eâ€“J runs consecutively, with another annotation at index8 between the blocks. This supports related local organization without claiming identical synteny. All ten core counterparts are distinct sampled annotations. The remaining eight BGC0000818.1 records do not have comparable block correspondence in this drawing; they are retained as lower-scoring matches rather than deleted or declared dispensable. No complete minimal gene set was established.

## The NRRL236 proxy remains a separate limitation

For FMGX0011, six consecutive reference records align strongly to five ordered sampled annotations, including one combined annotation. That is partial correspondence, not six separate sampled genes. The [NCBI assembly metadata](https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_009812435.1/dataset_report) identifies the assembly Caesar assigns to NRRL236 as **UdeA_Aid1**, BioSample SAMN11259652, WGS VTSW01. Bounded metadata retrieval for [VTSW01000173.1](https://www.ncbi.nlm.nih.gov/nuccore/VTSW01000173.1) agrees. It does not list NRRL236 as an alias. The source-assigned different-strain proxy therefore stays flagged; it is not silently merged by species name.

NRRL236 feature9213 values HZ=251854.6719, IA=27700000 and IB=207000000 were verified again. Its chemistry panel remains useful. Failure to establish that culture's exact genome correspondence does not invalidate the separate FMGX0064 family anchor. Other members were quantitatively compared but their sample/culture provenance was not independently validated in this bounded follow-up.

## Reference evidence and the remaining decision

[Li et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3511817/), Figure2, Table1 and the notoamide discussion, connects the reference cluster annotations to a proposed biosynthetic account in the producing organisms. It reports experimental support for early activities and precursor incorporation, while several intervening enzyme assignments remain proposals. Its broader locus assignment should not be represented as a complete native-locus perturbation result. The primary article's indexed text and publisher/PubMed abstracts were inspected; direct PMC access returned a challenge.

[Fraley et al. 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7483341/), Figure1 and primary indexed text, supplies exact-B biochemical reaction evidence against standards in the reference systems. That strengthens the product-specific argument but does not automatically turn every gene in a related cluster into an experimentally established native pathway to B. No later complete reference-locus assignment was established in this bounded check. This is a limit of the reviewed evidence, not a claim that no such evidence exists.

The sampled chain can now be presented for a researcher decision: `source:NRPS_66`, anchored to FMGX0064's Asposti1 region, ranks feature9213 at unspecified-enantiomer B resolution. Accepting a reference-supported label still requires an explicit judgment that the published pathway assignment and partial experimental chain are adequate for that class, together with a criterion accepting the measured identities, coverage and changed organization. If the chosen reference class requires stronger whole-locus-to-product evidence, that remains a material unmet condition. A new perturbation in Caesar's culture is not imposed; an existing published locus-product assignment or an explicit partial-pathway evidence policy could settle the question. Neither automated homology nor the source's correlation is scientific approval.

No competing locus was established within the selected source-family scope. NRPS_66 and DMAT_21 co-label FMGX0064's same region, along with MIXED_89; those labels are overlapping views, not independent positive pathways. Reciprocal checks cover displayed proteins only. The review does not assert absence of alternative loci elsewhere in any genome, production by all seven members, transfer to A or E/E4, or a particular enantiomer. The historical family remains one proposed query and one related pathway group.

## Reproducibility and limits

Python 3.13.5, Biopython 1.88, BeautifulSoup 4.14.3; PairwiseAligner global mode, BLOSUM62, gap opening âˆ’10, extension âˆ’0.5 including terminal gaps, epsilon 1e-6, first maximum-scoring alignment. Identity is identical non-gap residue pairs divided by all non-gap pairs; coverage divides the paired count by each full unaligned protein length. TSV fields retain lengths, paired and identical counts, columns, score and second score, ties, reverse winner, and sequence SHA-256 values. Reciprocal winner checks reuse the same score matrix, adding no comparisons. Self-scores for normalization add 37 unique self comparisons (computed repeatedly per member); they are distinct from the 3,626 cross-record scores.

Archive SHA-256: `0cef389310eccd261255e51919e7fe5f1f772cc73be2b0d42e0f5f8e30245a54`. Embedded NRPS_66 SHA-256: `104490c3fffb4e27a0623ea9587bf8e2ed2ead5ab4317a8de817baeeaabdd843`. Publisher URLs/reuse status remain in [legacy imports](../../data/manifests/legacy-imports.tsv). Fresh feature reads used openpyxl; its version and workbook hash are in scratch. The JGI strain text was available through the web tool's indexed official page; direct local HTTP retrieval returned 403 and the retained HTML records that failure. JCM returned its catalogue page. These access differences are preserved in the source receipt.

Scratch at `data/interim/notoamide-b-sampled-correspondence/` holds both the initial FMGX0011 comparison and the final seven-member comparison, all 3,626 scores, the metadata responses, source receipts, scripts, hashes and validation. The final TSV contains 259 rows. The reference versions are the embedded historical `.1` records; the later MIBiG display was used only to map reference annotation names. All source-selected known labels remain retrospective exposure. Biological eligibility, frozen 9,339-feature inputs, observation rules and spectral readiness remain separate decisions.
