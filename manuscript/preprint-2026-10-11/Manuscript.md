\begin{center}
{\LARGE\bfseries\color{ink}FungalLink v2: a curated benchmark for linking fungal biosynthetic gene clusters to measured metabolites\par}
\vspace{10pt}
{\large Vin Vomero}\\[3pt]
Independent researcher\\[3pt]
\href{mailto:vvomero@gmail.com}{vvomero@gmail.com}\\[8pt]
{\small 11 October 2026}
\end{center}
\vspace{4pt}
\hrule
\vspace{8pt}
\begin{minipage}{\textwidth}\small\textbf{Abstract.} Fungal genome--metabolome linking requires traceable associations between biosynthetic loci and measured features, yet published evidence and computational inputs are often fragmented. FungalLink v2 assembles 30 curated relationships across 16 genomic query identities from five study cohorts. It distinguishes experimental support, chemical assignment, reference transfer and input readiness. Twenty relationships are directly supported and ten are reference-supported under stated criteria. Eleven relationships support complete retrospective evaluations across seven query views from one source-selected cohort, with 9,339 measured candidate features. Two additional relationships have partial spectral diagnostics; 17 lack usable benchmark inputs. Versioned evidence records and candidate definitions support an evaluator that handles tied scores, multiple products and unavailable outputs. Deterministic numerical evaluations are reproducible from frozen inputs. Shared pathways, historical label exposure and incomplete chemical assignments constrain interpretation: the resource supports retrospective recovery of supported targets and method testing, without providing unbiased estimates of unseen-pathway performance.\par\end{minipage}
\vspace{9pt}
\hrule
\vspace{8pt}

## Background and Summary

A fungal biosynthetic gene cluster (BGC) and an experimentally characterized reference product do not by themselves identify a product in a measured feature table. Here, a feature is an LC-MS signal defined by the source processing, rather than an independently confirmed compound. That task needs explicit connections among the sampled genomic locus or family, source experiment and measurement. FungalLink v2 records these connections and supplies fixed candidate pools and an evaluation interface for comparing genome-to-measured-metabolite linking methods.

The resource builds on existing data and methods. Caesar and colleagues supplied the principal fungal cohort and source-selected gene-cluster families (GCFs), which group sequence-related clusters [1]. NPLinker combines co-occurrence with complementary scores, NPClassScore adds genomic–chemical class correspondence, and NPOmix predicts toward gene-cluster families from fragmentation profiles [2–4]. Their inputs and prediction directions differ. Reusable comparison requires the task and permitted information to be stated before interpreting rankings.

| Existing resource | Established contribution | Added FungalLink record or use |
|---|---|---|
| Caesar fungal metabologenomics [1] | Paired measurements, selected families and source associations | Audited identifier joins, qualified measured-target labels, fixed 9,339-feature pools and frozen observation rosters |
| Paired Omics Data Platform [5] | Paired-data metadata and validated BGC–MS/MS links | Per-relationship evidence, input-readiness and task-specific candidate definitions for comparative retrieval |
| MIBiG 4.0 [8] | Experimentally characterized reference BGCs and products | Explicit transfer limits from references to sampled queries and measured features; a reference record alone does not identify a measured target |
| NPLinker and NPLinker 2 [2,6] | Linking workflows and extensible scoring infrastructure | A qualified fungal task with tie-aware, product-aware evaluation and coverage accounting |

FungalLink assembles published fungal evidence into a common task for comparative retrieval. Its contribution is the traceable path from biological evidence to an eligible query and measured target, together with fixed inputs and evaluation rules (Figure 1). The 30 relationships represent 16 genomic query identities; biological eligibility, evidence strength and computational readiness are recorded separately.


\begin{figure}[!htbp]
\centering
\includegraphics[width=\linewidth,height=0.62\textheight,keepaspectratio]{figures/Figure-1.pdf}
\caption{Query definition and evaluation. A sequence-defined BGC or an explicitly rostered GCF ranks measured metabolite features. Genomic and measurement provenance define method inputs; curated query-target relationships enter a separate evaluation channel. Complete rankings retain all 9,339 Caesar features, including unnamed candidates. Evidence strength, biological eligibility, input readiness and prior exposure are recorded separately. This separation does not remove historical use of labels in source-family selection. Arrows indicate information flow, not causal evidence; unresolved candidate links remain unlabeled.}
\label{fig:1}
\end{figure}

## Methods

### Source selection and evidence qualification

The inventory covers the Caesar cohort, fungal artificial chromosome and mass spectrometry (FAC-MS) studies, HEx heterologous-expression experiments, the Trichoderma ilicicolin study and the black-yeast-study 6-methylsalicylic acid (6-MSA) expression case [1,9–15]. Source screening and later admission decisions are retained with their dated scope; no common screening denominator is available. The initial task uses publicly studied, historically selected families and is retrospective. Unresolved or rejected associations remain outside the positive sets and do not become negative labels.

Each admitted relationship connects a genomic query identity to a measured target at its supported chemical resolution. Direct support requires an experimentally represented queried locus or family member joined to the measured product. Reference-supported assignments transfer established pathway evidence through documented correspondence. These categories do not replace chemical-identity qualifiers, locus correspondence or native versus heterologous expression context. An identifier in a published figure or table is linked to a computational feature only when the measurement correspondence is documented.

The current ledger contains nine GCF relationships across five GCF queries and 21 BGC relationships across eleven BGC queries, with 20 direct and ten reference-supported assignments. Multiple products from valactamide or benzomalvin share their underlying query. Putative pestalamide E/F, valactamide congeners and other chemically qualified assignments retain that resolution. FAC and HEx measurements do not supply native fungal co-occurrence vectors. The 6-MSA query is the observed expression sequence, including its one-amino-acid difference from the cited reference.

The corrected acetylaszonalenin relationship is defined by its identified core biosynthetic genes. A separate DMAT_34 family view is used for evaluation under the [8 October correction](https://github.com/vinvomero/fungallink-benchmark/blob/main/protocol/decisions/2026-10-08-acetylaszonalenin-family-source-correction.md). All three accepted-core proteins occur in the historical source display; contrary region coordinates belonged to successor annotation numbering. Full historical nucleotide boundaries remain unverified. The assembly contamination flag and unknown locus-specific contamination status remain separate qualifications.

Curation used retained primary studies, accession records, source panels and sequence correspondence records. Later admission judgments included assistant-assisted curation under delegated authority and have not undergone independent specialist re-adjudication. Numerical verification is separate from biological and chemical appraisal.

### Query representations, candidate pools and exposure

The original frozen task uses five source-selected GCF queries, six supported products and all 9,339 workbook features, including unnamed candidates. Its separate nine-target amendment changes only the positive-set version. Emericellamide HRPKS_71 and acetylaszonalenin DMAT_34 extensions add complete coverage for two existing BGC relationships through declared BGC-to-GCF transformations. They do not create new biological admissions. Together these analyses cover eleven relationships through seven query views.

Binary genomic membership records whether an observation belongs to the deposited family member list. A zero denotes a checked observation outside that list; it does not demonstrate that the genome lacks the cluster. The primary observation roster, or fixed sample list, comprises 105 source-study observations. Preprocessing uses within-condition medians, recorded condition unions, maximum condition height and any-condition detection at 10,000,000 in raw, unnormalized height units. Zero presence requires every required condition to be observed below threshold; unresolved observations remain missing.

Eighteen overlapping observation rosters retain the primary 105 observations, the 102-observation three-media restriction, eight 102-observation assembly-representative choices and their eight 99-observation three-media restrictions. They are sensitivity populations, not held-out tests or independent biological replicates. Source labels informed historical family selection. Freezing later inputs does not remove that exposure. All complete query views belong to one conservative analysis group; this does not assert a single biological pathway.

### Workflows and evaluation

The local workflows, version 0.1.0, compare global feature prevalence, the difference in feature prevalence between family members and nonmembers, raw Metcalf co-occurrence, standardized Metcalf and uniform random ranking. Global prevalence provides a query-independent baseline. The two Metcalf variants weight the joint presence and absence pattern; standardization adjusts for the fixed-margin null expectation. They are related adaptations for complete feature tables, not complete NPLinker workflows [2]. Supplementary Methods provides equations, exact input permissions and degenerate-case behavior.

Prevalence difference abstains if either roster category is empty. Standardized Metcalf abstains for invariant membership and otherwise assigns invariant features zero with a zero-variance flag. Complete rankings retain exact ties without score cutoffs. Methods receive permitted observations separately from evaluator positives. Missing required inputs cannot silently shrink a candidate pool or denominator.

The evaluator requires one finite score per candidate for a valid query. It preserves abstention, input unavailability, execution failure and invalid-output reasons. Supported products have disjoint target sets; multiple ions assigned to one product do not increase the product count. Hit@1, @10 and @100 measure retrieval of any supported target. We also report expected reciprocal rank of the first target, mean product recovery and the probability of recovering every product. These are known-positive retrieval measures, not biological precision or false-positive rates.

Equal scores receive expected credit under uniform permutations within each tied block. Reciprocal rank is averaged over the possible first-target positions, rather than calculated from a mean rank. Metrics are averaged by query within cohort and analysis group. Conditional summaries include valid outputs; end-to-end summaries also account for failed or unavailable query outputs. Entirely unavailable methods are reported with reasons rather than fabricated scores.

Uniform random ranking supplies exact expectations and a separately recorded Monte Carlo check. Simulation error is distinct from biological uncertainty. The single conservative analysis group cannot support biological confidence intervals or leave-one-group-out inference; the 18 overlapping rosters assess sensitivity to sample composition.

### Spectral diagnostics and fixed-tree comparison

Two separate reference-informed class diagnostics retain their full candidate pools: 1,249 features for 6-MSA and 98 for ilicicolin H. Spec2Class source revision `21c6f9433227c689d00549eae25e1fa2d4238fc3` [16] supplies predicted superclasses. Weight revisions, preprocessing and prediction environments are specified in Supplementary Methods and the runtime manifests. A pinned NPLinker class-association table combines these predictions with a transferred T1PKS annotation for 6-MSA or the published PKS-NRPS annotation of TriliA. These genomic classes are reference-informed, not blind sequence predictions. Unmatched vocabularies, absent spectra and empty processed spectra remain uncovered. Scored-only ranks and conservative full-pool bounds are reported separately.

A distinct comparison projects the five original GCF queries, nine supported targets and 9,339 candidates onto 66 observations with distinct versioned assemblies. It adds a BayesTraits dependent-versus-independent binary-character score motivated by published phylogeny-aware metabologenomics [7]. Marker reconstruction, MAFFT 7.526 alignment and filtering yielded 1,078 markers and 551,870 sites. IQ-TREE 2.4.0 fitted an unpartitioned LG+F+G4 model; the tree was midpoint-rooted before branch rescaling. No support resampling was performed.

A retrospective recovery amendment permits an alternative optimizer only for the specified nested-likelihood check failure. Twenty-four of 7,290 distinct nonconstant pairs used this recovery. Original failed attempts, selection rules and terminal checks remain retained. Full computational procedures, versions and fixed validity checks are in [Supplementary Methods](Supplementary-Methods.pdf); all comparative results and Tables 1–3 remain in [Comparative results v1](Comparative-results.pdf).

### Similarity and dependence

A separate companion analysis measures resemblance only where retained representations permit comparison, without changing labels, retrieval scores or frozen analysis groups. Supported structures use binary Morgan fingerprints with radius 2, 2,048 bits, bond types enabled and chirality disabled; Tanimoto is the fraction of shared set bits in their union. Chiral sensitivity is withheld because source identifiers do not resolve the stereochemical distinctions in the supplied structures. Compatible source-annotated core proteins use global BLOSUM62 alignment with gap opening −10 and extension −0.5, including terminal gaps. Identity is identical residues divided by paired nongap residues, with coverage reported against both full sequences. Protein-content fractions use all displayed annotated proteins as denominators and qualifying core matches as numerators; they are lower bounds, not whole-cluster similarity estimates.

Within each native joined spectral pool, peaks below m/z 10, within ±1 Da of a known precursor, or below 1% of the base peak are removed. Square-root intensities are L2-normalized before CosineHungarian matching at 0.02 Da. Resemblance flags require cosine at least 0.7 and six matched peaks; 0.9 is a stricter sensitivity. Typed dependence edges distinguish shared queries, curated pathways, construct/host context, sequence identity and spectral resemblance. Reference membership is assessed against declared retained assets separately from model-training membership. The [protocol](https://github.com/vinvomero/fungallink-benchmark/blob/main/protocol/similarity-independence-v1.md), [report](https://github.com/vinvomero/fungallink-benchmark/blob/main/docs/evaluation/similarity-independence-v1.md) and [data dictionary](https://github.com/vinvomero/fungallink-benchmark/blob/main/docs/release/similarity-independence-v1.md) preserve parameters, provenance, missingness and software versions.

## Data Records

FungalLink is organized into relationship evidence, task inputs and frozen outputs. Table D1 summarizes the inventory and Figure 2 shows its distribution across cohorts. The supporting record directory identifies the versioned files and their schemas.

| Record collection | Content and purpose |
|---|---|
| Relationship evidence and readiness | Thirty admitted relationships, biological query identities, source anchors, chemical resolution, uncertainty and complete, partial or missing input states |
| Task definitions and exposure | Candidate populations, query transformations, observation rosters, positive sets, method versions, prior exposure and analysis groups |
| Numerical inputs and results | Frozen inputs, complete rankings, per-query and per-product metrics, partial-output bounds and run receipts |
| Similarity and dependence | Supported representations, eligible pair comparisons, missingness, typed dependencies and reference-exposure checks |
| Provenance and reproduction | Evidence locators, hashes, field dictionaries, rights scope and commands for each reproduction stage |

A score is identified by its candidate population, query representation and version, observation roster, positive-set version and method/run identifier. A biological relationship key alone is insufficient. Feature identifiers are local to a dataset: mass labels, source panels and spectrum identifiers require explicit crosswalks before they can enter the evaluation. Genomic coordinates retain their recorded source convention and accession version. The three numerical tracks and similarity companion retain separate version identities within the public version 1.0.0 release.

Relationship identifiers connect the evidence ledger to the readiness table. Biological query identity is stored separately from its computational representation, so a BGC-to-GCF transformation remains visible. Source target identifiers and evaluated feature identifiers are also separate. Exposure records distinguish known reference use from model-training overlap, which remains unknown.

Missing inputs, unknown biological links, unsupported exact chemical identities and unavailable method output are different states. The dictionaries specify their literal codes. Scores are dimensionless; rank ranges describe exact ties and missing-output bounds. Observation heights retain the source's raw intensity scale. The original code is licensed under Apache-2.0; original curation, results and documentation are CC BY 4.0. Third-party payloads retain their source terms and scoped dispositions.

Table D1. Current relationship readiness. Counts are reconciled to the authoritative ledger and derived readiness view; query views and relationships use different denominators.

| Dimension | Count | Interpretation |
|---|---:|---|
| Admitted relationships | 30 | Qualified positive relationships, not 30 runnable tasks |
| Biological query identities | 16 | Shared products do not add queries |
| Directly supported relationships | 20 | Experimental support at the stated query/chemical resolution |
| Reference-supported relationships | 10 | Explicit transfer and correspondence limits |
| Complete evaluated relationships | 11 | Seven query views from one source-selected cohort |
| Completed partial diagnostics | 2 | 6-MSA and ilicicolin H; not pooled with complete outputs |
| Input-incomplete relationships | 17 | Fifteen FAC and two HEx relationships |
| Conservative complete-analysis groups | 1 | No independent held-out test or biological confidence interval |


\begin{figure}[!htbp]
\centering
\includegraphics[width=\linewidth,height=0.62\textheight,keepaspectratio]{figures/Figure-2.pdf}
\caption{Current relationship evidence and computational coverage. Panel a separates direct and reference-supported relationships; panel b uses the same 30-relationship denominator to distinguish complete evaluation, partial diagnostics and missing inputs. The query column counts biological identities within each cohort, not products or independent pathways. Caesar contributes all eleven completely evaluated relationships through seven query views, including the emericellamide and acetylaszonalenin family-view extensions. FAC-MS contributes fifteen input-incomplete relationships across five queries; HEx contributes two across two queries. Trichoderma and the black-yeast study each contribute one partial diagnostic. The latter uses a fungal synthase measured in a yeast-expression strain. All complete query views remain within one conservative analysis group. Evidence classes do not imply exact structure resolution.}
\label{fig:2}
\end{figure}

## Technical Validation

### Identifier, evidence and coverage checks

Frozen manifests check candidate membership, query identity, positive-set versions and hashes before evaluation. Multiple measured products from one query remain separate targets, while multiple ions assigned to one product do not increase the product count. Unknown candidates stay unlabeled. The release preserves source discrepancies, disputed transfers and superseded decisions so that users can inspect the basis of each positive relationship. These checks establish record consistency rather than new biological evidence.

The original source rebuild reproduced 20 scientific output files and the released complete input exactly from cached source bytes and pinned curation. It did not derive historical sample/family mappings wholly from public data or repeat biological adjudication. Same-host automated reruns are identified as such.

### Evaluator behavior and numerical reconstruction

Exact ties can give fractional hit credit. In the initial pestalamide example, raw Metcalf placed one product within ranks 1–8 and the other within ranks 41–49. Hit@10 was 1, product recovery@10 was 0.5 and all-products recovery@10 was 0. This demonstrates why any-hit retrieval cannot replace product-level recovery. Supporting Figures S1–S3 and Tables 1–3 give all workflow comparisons, including the distinct six-product and nine-target versions.

The benchmark also distinguishes retrieval of one product from recovery of a query's broader product set. In the five-query, six-product comparison, primary Hit@10 was 0.854 for raw Metcalf, 0.615 for standardized Metcalf and 0.487 for prevalence difference. All three recovered every supported product by rank 100. Adding three supported targets without changing any scores left raw Metcalf Hit@10 unchanged, but reduced its mean product recovery@10 from 0.754 to 0.604 and all-products recovery@10 from 0.654 to 0.454. Early retrieval alone therefore missed a consequential change in target coverage.

The two separately frozen family-view extensions show why results must also remain traceable to individual queries. For emericellamide A, the three query-dependent workflows recovered the target within 100 candidates on every roster, but none within ten on the primary roster. For acetylaszonalenin, prevalence difference and standardized Metcalf ranked the target second on the primary roster, while raw Metcalf ranked it 92nd. These results describe source-selected queries in one conservative group; they do not establish a general method winner.

The retained audit reproduced 216 deterministic core combinations from extracted frozen inputs and reported 188 tests, including two skips, with no recorded failures. Saved-class reconstruction reproduced 1,347 spectral diagnostic rows after restoration of the pinned external association table. These are recorded checks, not new tests performed for this revision. Predictor inference, source acquisition and raw processing have separate starting boundaries.

The 6-MSA diagnostic scores 291 of 1,249 candidates. Its target ranks 95–291 within scored outputs and 95–1,249 under full-pool missing-output bounds. Ilicicolin H scores 89 of 98 candidates, with corresponding target bounds of 16–21 and 16–30. These results retain missing scores and reference exposure. Neither contributes a completely evaluated relationship.

### Conditional phylogeny validation

Reconstruction from retained native logs in the original Linux environment verified all 7,290 pair patterns, including 24 recovered pairs, without refitting. Supplementary Methods documents the environment dependence and the unchanged exact-check criterion.

Conditional on the fixed tree, model and matched 66-observation population, BayesTraits had lower Hit@10 than raw and standardized Metcalf (0.256 versus 0.494 and 0.528) and higher product recovery@100 (0.782 versus 0.657 and 0.621). Supporting Table 3 preserves all 36 metric cells and their full-precision exports. The comparison does not isolate a causal effect of phylogeny against the different 105-observation population.

IQ-TREE reported composition-test failures in 65 of 66 sequences. The fixed unpartitioned model, midpoint rooting, absence of support resampling and retrospective optimizer recovery constrain these findings. Numerical agreement does not validate the tree, establish global optimizer convergence or show general biological superiority.

### Representation coverage and dependence

Five source-specific product crosswalks support machine-readable connectivity structures: acetylaszonalenin, emericellamide A, griseofulvin, fellutamide B and aspernidine A. Their ten pairwise Tanimoto values range from 0.0323 to 0.1463; none reaches 0.7. Only ten of the 435 possible relationship pairs can be compared; 425 are unavailable because 25 relationships lack supported structures. This subset cannot establish chemical diversity across all 30 relationships. The genomic analysis represents 79 displayed members of seven source-selected GCFs and ten accepted locus, construct or CDS anchors. Of 10,516 cross-member core pair records, 3,575 have compatible annotated roles and numerical alignments. Incompatible roles remain null, and incomplete or core-only representations cannot establish whole-cluster dissimilarity.

All 91 Trichoderma and 291 black-yeast native joined spectra survived the declared filtering, yielding 4,095 and 42,195 within-pool pairs, respectively. Of these 46,290 comparisons, 93 meet the 0.7/six-peak resemblance rule and 51 meet the 0.9/six-peak rule. The 26,481 cross-pool pairs are excluded because the retained export charges have opposite signs. Seven Trichoderma and 958 black-yeast candidates still lack joined spectra. High cosine does not identify an isomer, adduct or genome-product relationship; acquisition settings and missing spectra limit interpretation.

Eight valactamide relationships share one query and four benzomalvin relationships share another. Three AtFAC9J20 loci share a construct/host context without becoming one pathway. The conservative dependence scenario has five components, only one containing complete evaluated relationships. These scenarios preserve the frozen complete-analysis group and establish no independent holdout or between-group uncertainty estimate. Bounded reference-file checks are recorded separately from weight-specific predictor training membership, which remains unknown. Figure 3 summarizes the represented chemical, genomic and spectral comparisons without treating missing representations as dissimilarity.


\begin{figure}[!htbp]
\centering
\includegraphics[width=\linewidth,height=0.62\textheight,keepaspectratio]{figures/Figure-3.pdf}
\caption{Representation coverage limits similarity assessment. Panel a shows the ten available pairwise Morgan-fingerprint Tanimoto values for five supported connectivity structures; values span 0.0323--0.1463. The color scale runs from 0 to 0.16, rather than the full possible 0--1 range. Blank diagonal cells are self-comparisons and are excluded. The five structures represent only five of thirty admitted relationships, and ten of 435 possible relationship pairs. Panel b states the distinct eligible comparison units: 3,575 compatible annotated core-protein comparisons among 10,516 cross-member records, and 46,290 within-pool spectral comparisons. Spectral comparisons comprise 4,095 Trichoderma and 42,195 black-yeast pairs; 26,481 cross-pool pairs are excluded because the retained charge signs differ. Ninety-three within-pool pairs meet cosine ≥0.7 with at least six matched peaks; 51 meet the stricter ≥0.9 rule. Incompatible core roles and missing structures are unavailable, not zero similarity. These measurements neither establish whole-cluster dissimilarity nor create independent evaluation groups.}
\label{fig:3}
\end{figure}

## Usage Notes

For a complete-output comparison, select the eleven covered relationships through their seven declared query views and use the corresponding frozen candidate manifests. Keep the original five-query analysis and each family-view extension identifiable. Use the two partial spectral diagnostics only with their coverage and full-pool bounds; seventeen FAC/HEx relationships are evidence records without usable comparison inputs.

The reproduction-stage guide distinguishes source acquisition and raw LC-MS processing, predictor inference, marker/alignment/tree/native fitting, and saved numerical reconstruction. Select a stage whose starting artifacts are available. The exact phylogeny reconstruction requires the environment recorded in `docs/release/environment/phylogeny-linux-explicit.txt`. A successful numerical replay does not imply raw-to-fit replication or independent scientific validation.

The task supports reference retrieval, adapter testing and retrospective method comparison against the same candidate universes. It does not support precision against verified negatives, unbiased unseen-pathway performance, independent-query significance testing or product-random train/test splitting. Genomic correspondence, chemical structure similarity and ion/adduct redundancy are different dependencies. Historical exposure and unknown model-training overlap remain recorded rather than assumed absent.

## Data Availability

The versioned data release is publicly available at [FungalLink v2, version 1.0.0](https://github.com/vinvomero/fungallink-benchmark/releases/tag/v1.0.0). It contains curated evidence, numerical inputs, frozen results, reconstruction packages and a SHA-256 manifest. Anonymous download, payload verification and primary-roster numerical replay were checked on 11 October 2026. Three upstream inputs use pinned retrieval recipes; raw author workbooks and correspondence are excluded. The historical mapping provenance and remaining input gaps are documented. No DOI has been assigned.

## Code Availability

Ranking adapters, the evaluator, input builders, figure recipes and a separately authored synthetic adapter example are available in the [public code repository](https://github.com/vinvomero/fungallink-benchmark). Frozen manifests identify the versions used. The synthetic example demonstrates interface use, not fungal performance. Original software is approved for Apache-2.0 licensing; third-party software and model assets retain their own terms. The three numerical candidates cover the deterministic core, saved-class arithmetic and saved phylogeny fits/evaluations within their declared boundaries. The version 1.0.0 release identifies the corresponding software snapshot and reproduction instructions.

## Author contributions

Vin Vomero defined the research objective, directed the project and supplied retained source materials and correspondence. AI-assisted contributions are disclosed below and do not constitute authorship.

## Funding

The author declares no funding.

## Competing interests

The author declares no competing interests.

## Acknowledgments

Lindsay K. Caesar supplied a historical strain-label workbook and clarifications used in the retained crosswalk. Project-generated reconciliations incorporate those records and marked inferences. Attachment-origin verification does not certify every inferred mapping or a wholly public derivation.

## AI assistance

OpenAI Codex assistants contributed to literature retrieval and synthesis, evidence appraisal and delegated admission judgments, processing and evaluation code, tests, numerical checks, figures, manuscript drafting and revision. The [AI-use record](https://github.com/vinvomero/fungallink-benchmark/blob/main/manuscript/ai-use-record-v1.md) records known dates, roles and requested model settings. Serving-model receipts are unavailable and actual serving identity is not inferred. Automated checks and same-host reruns do not supply human scientific accountability. Scientific judgments and manuscript approval remain the responsibility of the human author; final review has not yet been recorded.

\FloatBarrier

## References

\small

1. Caesar, Lindsay K.; Butun, Fatma A.; Robey, Matthew T., et al. (2023). Correlative metabologenomics of 110 fungi reveals metabolite–gene cluster pairs. Nature Chemical Biology 19(7): 846–854. https://doi.org/10.1038/s41589-023-01276-8

2. Hjörleifsson Eldjárn, Grímur; Ramsay, Andrew; van der Hooft, Justin J. J., et al. (2021). Ranking microbial metabolomic and genomic links in the NPLinker framework using complementary scoring functions. PLOS Computational Biology 17(5): e1008920. https://doi.org/10.1371/journal.pcbi.1008920

3. Louwen, Joris J. R.; Medema, Marnix H.; van der Hooft, Justin J. J. (2023). Enhanced correlation-based linking of biosynthetic gene clusters to their metabolic products through chemical class matching. Microbiome 11: 13. https://doi.org/10.1186/s40168-022-01444-3

4. Leão, Tiago F.; Wang, Mingxun; da Silva, Ricardo, et al. (2022). NPOmix: A machine learning classifier to connect mass spectrometry fragmentation data to biosynthetic gene clusters. PNAS Nexus 1(5): pgac257. https://doi.org/10.1093/pnasnexus/pgac257

5. Schorn, Michelle A.; Verhoeven, Stefan; Ridder, Lars, et al. (2021). A community resource for paired genomic and metabolomic data mining. Nature Chemical Biology 17(4): 363–368. https://doi.org/10.1038/s41589-020-00724-z

6. Geng, Cunliang; Crocioni, Giulia; Hecht, Helge, et al. (2026). NPLinker 2: a modular and customizable framework for paired omics analyses. Journal of Open Source Software 11(121): 9528. https://doi.org/10.21105/joss.09528

7. Boldt, Judith; Porten, Christoph; Haeckl, F. P. Jake, et al. (2026). Phylogeny-Aware Metabologenomics Accurately Assigns Natural Products to Biosynthetic Gene Clusters. Microbial Biotechnology 19(1): e70298. https://doi.org/10.1111/1751-7915.70298

8. Zdouc, Mitja M.; Blin, Kai; Louwen, Nico L. L., et al. (2025). MIBiG 4.0: advancing biosynthetic gene cluster curation through global collaboration. Nucleic Acids Research 53(D1): D678–D690. https://doi.org/10.1093/nar/gkae1115

9. Burger, Isabella; Schmal, Matthias; Peikert, Kathrin, et al. (2025). Discovery of the antifungal compound ilicicolin K through genetic activation of the ilicicolin biosynthetic pathway in Trichoderma reesei. Biotechnology for Biofuels and Bioproducts 18: 32. https://doi.org/10.1186/s13068-025-02628-3

10. Clevenger, Kenneth D.; Bok, Jin Woo; Ye, Rosa, et al. (2017). A Scalable Platform to Identify Fungal Secondary Metabolites and Their Gene Clusters. Nature Chemical Biology 13(8): 895–901. https://doi.org/10.1038/nchembio.2408

11. Robey, Matthew T.; Ye, Rosa; Bok, Jin Woo; Clevenger, Kenneth D.; Islam, Md Nurul; Chen, Cynthia; Gupta, Raveena; Swyers, Michael; Wu, Edward; Gao, Peng; Thomas, Paul M.; Wu, Chengcang C.; Keller, Nancy P.; Kelleher, Neil L. (2018). Identification of the First Diketomorpholine Biosynthetic Pathway Using FAC-MS Technology. ACS Chemical Biology 13(5): 1142–1147. https://doi.org/10.1021/acschembio.8b00024

12. Caesar, Lindsay K.; Robey, Matthew T.; Swyers, Michael; Islam, Md N.; Ye, Rosa; Vagadia, Purav P.; Schiltz, Gary E.; Thomas, Paul M.; Wu, Chengcang C.; Kelleher, Neil L.; Keller, Nancy P.; Bok, Jin Woo (2020). Heterologous Expression of the Unusual Terreazepine Biosynthetic Gene Cluster Reveals a Promising Approach for Identifying New Chemical Scaffolds. mBio 11(4): e01691-20. https://doi.org/10.1128/mBio.01691-20

13. Harvey, Colin J. B.; Tang, Mancheng; Schlecht, Ulrich; Horecka, Joe; Fischer, Curt R.; Lin, Hsiao-Ching; Li, Jian; Naughton, Brian; Cherry, James A.; Miranda, Molly; Li, Yong Fuga; Chu, Angela M.; Hennessy, James R.; Vandova, Gergana A.; Inglis, Diane; Aiyar, Raeka S.; Steinmetz, Lars M.; Davis, Ronald W.; Medema, Marnix H.; Sattely, Elizabeth; Khosla, Chaitan; St. Onge, Robert P.; Tang, Yi; Hillenmeyer, Maureen E. (2018). HEx: A heterologous expression platform for the discovery of fungal natural products. Science Advances 4(4): eaar5459. https://doi.org/10.1126/sciadv.aar5459

14. Clevenger, Kenneth D.; Ye, Rosa; Bok, Jin Woo; Thomas, Paul M.; Islam, Md Nurul; Miley, Galen P.; Robey, Matthew T.; Chen, Cynthia; Yang, KaHoua; Swyers, Michael; Wu, Edward; Gao, Peng; Wu, Chengcang C.; Keller, Nancy P.; Kelleher, Neil L. (2018). Interrogation of Benzomalvin Biosynthesis Using Fungal Artificial Chromosomes with Metabolomic Scoring (FAC-MS): Discovery of a Benzodiazepine Synthase Activity. Biochemistry 57(23): 3237–3243. https://doi.org/10.1021/acs.biochem.8b00076

15. Gadar-Lopez, Adrian E.; Calheiros de Carvalho, Ana; Li, Xiaowei, et al. (2026). Black yeasts are efficient heterologous hosts for the production of a wide range of fungal polyketides. Nature Chemical Biology. Advance online publication, 3 August 2026. https://doi.org/10.1038/s41589-026-02282-2

16. Spec2Class contributors. Spec2Class software, source revision 21c6f9433227c689d00549eae25e1fa2d4238fc3. https://github.com/VickiPol/Spec2Class/tree/21c6f9433227c689d00549eae25e1fa2d4238fc3

