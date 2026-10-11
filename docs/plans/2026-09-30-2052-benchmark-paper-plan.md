# FungalLink v2 benchmark and paper plan
Created: 2026-09-30

## Outcome and working assumptions

Produce a reusable benchmark for comparing methods that link fungal biosynthetic gene clusters (BGCs), or explicitly defined gene-cluster families (GCFs), to measured metabolite features. Deliver a versioned dataset, reviewed reference answers, compatible baseline implementations, an evaluation interface, reproducible results, and a manuscript ready for submission.

The main question is practical: given the same query and candidate molecules, how well does each method recover supported products, and how much of the benchmark can it evaluate? Generalization to unseen pathways is an optional track. It is not a condition for completing the benchmark.

The project remains in the private [vinvomero/fungallinkv2 repository](https://github.com/vinvomero/fungallinkv2) during development. Public release, preprint posting, external correspondence, journal submission, and expenditure beyond an agreed budget require explicit authorization at the relevant checkpoint. Preparation proceeds before those checkpoints.

This plan assumes public data reuse, no new wet-lab work, one primary researcher, and access to scientific review and a separate rerun. Assign the named people during Phase 1. Automated review does not substitute for biological or chemical adjudication. If outside reviewers are unavailable, document researcher-led review and a separate clean-environment rerun honestly; do not claim independent validation. Lack of an outside reviewer need not stop acquisition, implementation, or drafting.

Planning was dispatched through the native subagent route with requested model `gpt-6-astra` and reasoning effort `high`, following the user's routing instruction. Dispatch was accepted; no serving-side receipt confirmed the actual model or effort. The host reviewed the returned plan before saving it.

## Starting evidence

The portable source of record for the initial inventory is `research_audit/source-inventory.json`, read alongside `research_audit/PROJECT-ASSESSMENT.md` and `research_audit/BENCHMARK-FEASIBILITY-VERDICT.md`. The local, ignored `research_audit/input-audit.json` contains additional machine-specific inspection details.

The Caesar workbook contains 9,339 measured features. Its 362 sample columns, the supplied map's 357 acquisition stems, and the earlier pipeline's 338 included acquisitions describe different states that need reconciliation. The map contains 714 format-specific rows, including mzML/mzXML duplicates, 109 mapped strain labels, and 107 accession strings. None of these counts establishes the number of independent genomes.

The source association census contains 25 rows spanning 16 reference BGCs: nine Tier I, six Tier II, two Tier III, and eight Tier IV chemical calls. Fifteen stronger chemical calls are a curation starting pool, not fifteen accepted genome-to-feature links.

Acetylaszonalenin, emericellamide A, and pestalamide B provide concrete first cases. Their remaining requirements differ. Known errors, including alternariol assigned to a griseofulvin reference pathway, must be corrected or excluded regardless of historical recovery rank. No final admitted query count is assumed.

Preserve the neighboring historical repositories as read-only sources. Record imported files and code by origin, revision where available, hash, and license. Record stable source locators in `data/manifests/legacy-imports.tsv`; local locations belong in ignored configuration. The released benchmark must run without either neighboring checkout. Import useful assets selectively rather than copying old acceptance gates wholesale.

## Research contract

Freeze the contract before running comparative experiments.

| Track | Query and target | Required inputs | Interpretation |
|---|---|---|---|
| Core GCF-to-feature | A versioned family with an explicit member roster ranks measured LC-MS features | GCF membership, sample/genome crosswalk, feature abundance or presence matrix | Comparative recovery of supported family-product associations |
| BGC-to-feature | A sequence-defined locus ranks the same kind of measured feature | Locus sequence and boundaries; declared homology or other model inputs | Locus-level retrieval, limited by the evidence supporting that locus |
| Spectral extension | Either query type ranks features with validated MS/MS membership | Everything required by its query type plus feature-spectrum joins | Comparison of methods using spectral or predicted chemical-class information |
| Optional unfamiliar-pathway evaluation | Group-held-out queries under a declared exposure rule | Enough independent groups and compatible training data | Restricted generalization claim, reported separately |

Do not pool BGC and GCF results into one headline score. A GCF method can enter a BGC workflow only through a documented BGC-to-GCF transformation applied consistently and disclosed as part of that workflow. Structure-retrieval methods belong in a separate optional experiment unless an explicit structure-to-measurement mapping makes their output comparable. Such a mapping changes their information access.

For each track and cohort, freeze queries, candidate IDs, positive sets, eligible samples, preprocessing, grouping, and allowed information in a release manifest. Keep unnamed measured candidates. Missing annotations are not grounds for removal.

Use the full audited Caesar workbook as the initial candidate pool, subject only to documented integrity and quality rules. Explain the 9,301-versus-9,339 discrepancy without silently substituting counts. Any filtered pool becomes a separately named version with a removal ledger.

A correct result retrieves an evidence-supported measured target. It does not establish biological activity, a new pathway, or a causal assignment for every remaining candidate.

## Work sequence and responsibilities

Elapsed times are estimates, not deadlines. They assume bounded curation and overlapping drafting; re-estimate after the acquisition pilot. The final pathway count and method coverage are execution-time findings, not planning prerequisites.

| Phase | Accountable role | Dependencies | Estimated effort | Completion evidence |
|---|---|---|---|---|
| 1. Contract and source registry | Research lead | This plan | 3–5 working days | Frozen initial protocol and provenance schema |
| 2. Data assembly and label review | Data curator with biology/chemistry reviewers | Phase 1 | 3–5 person-weeks | Reviewed census, joined inputs, expansion decision |
| 3. Release construction | Bioinformatics and metabolomics lead | Accepted sources from Phase 2 | 2–4 person-weeks | Validated feature release; spectral release if ready |
| 4. Baselines and evaluation | Software lead and statistical reviewer | Frozen task; development data | 2–3 person-weeks | Tested adapters, score audit, evaluation specification |
| 5. Experiments and interpretation | Research lead and statistical reviewer | Frozen release and methods | 1–2 person-weeks | Complete results, sensitivity analyses, claim ledger |
| 6. Rerun and manuscript | Separate reproducer where available; lead author | Phase 5; drafting begins earlier | 3–4 person-weeks | Rerun report and submission package |
| 7. Release, submission, revision | Corresponding author | Publication approval | Journal-dependent | Archived release, submission record, response package |

Allow roughly 12–18 calendar weeks with suitable overlap and specialist availability; person-effort estimates do not guarantee that elapsed schedule. A mostly solo project may take longer. Changes in effort must name their cause rather than silently extending curation.

### Phase 1: Establish the protocol and acquisition ledger

Create `protocol/benchmark-contract.md`, `protocol/analysis-plan.md`, and `data/manifests/sources.tsv`. Record research questions, permitted inputs, evidence rules, grouping, planned metrics, and protocol-change policy before comparison results are inspected.

Give every source a stable ID with accession or DOI, retrieval URL, retrieval date, file size, checksum, version, license or reuse terms, and expected content. Separate source files from derived artifacts.

Start with:

- Caesar: PRJNA852164, MSV000089848, the publisher feature workbook, selected GCF archive, and primary/supplementary papers.
- A. fischeri: PRJNA1129834, Figshare 25316452 and 28380431, and the Steffen study.
- A. flavus: PRJCA035534, MSV000096910, MSV000096982, Zenodo 18670081, and the Xie study.

Inspect deposit manifests and a small representative subset before bulk retrieval. Estimate bytes, transfer duration, temporary processing space, storage duplication, and CPU/RAM needs from actual files. Record inaccessible or restricted material; do not make it an invisible dependency.

Build separate identifiers for study, biological strain, culture, extraction, acquisition, file representation, assembly, BGC, GCF, feature, and spectrum. A technical replicate is not another strain. Preserve raw aliases and every normalization decision.

Resolve GenBank/RefSeq correspondence and identical assemblies explicitly, retaining accession versions and sequence checksums. Do not collapse cultures solely because they share an assembly, or treat accession aliases as independent genomes.

Deliver `data/curated/sample-crosswalk.tsv` and a reconciliation report accounting for all source columns, unmatched stems, blanks, inferred mappings, and exclusions. Inferred sample matches carry uncertainty and cannot silently become verified links.

### Phase 2: Finish a bounded evidence census

Use one row per proposed query-product relationship, with separate fields for chemical identity, experimentally supported reference pathway, sampled-locus correspondence, and measured-target correspondence. Capture source pages, tables, figures, accession versions, sequence comparisons, alternative loci, reviewer, decision, and unresolved issues in `data/curated/label-evidence.tsv` and supporting records.

| Evidence class | Admission rule | Evaluation use |
|---|---|---|
| Directly supported | Experimental pathway-product evidence for the queried locus, or an experimentally represented GCF member, plus a traceable measured target; evidence transferred to another locus through homology belongs below | Main comparison; strongest-evidence sensitivity analysis |
| Reference-supported | Experimentally established reference pathway, justified sampled-locus homology or family membership, supported chemistry, and measured-target join | Main comparison with its scope stated; stratified results |
| Provisional | A plausible link lacks one decisive connection or relies primarily on source correlation | Exploratory/source-recovery supplement |
| Rejected or unresolved | Conflicting assignment, wrong organism/locus, unsupported identity, or unresolved target | Exclusion ledger; no contribution to headline scores |

Keep the underlying evidence dimensions visible. These classes do not replace the source's chemical-identification tiers. A new perturbation in each historical culture is not required. Spectral readiness is a separate field, not a universal biological-label gate.

Require sequence identity and coverage, gene content, relevant biosynthetic organization, and competing-locus checks for reference-supported assignments. Set decision criteria with the biology reviewer before applying them across cases. High sequence identity alone does not establish every congener.

Review the corrected acetylaszonalenin locus and feature 2127 first. Then resolve emericellamide A and feature 8468, preserving its reported five-protein full-length exact-match evidence for verification. Do not extend that assignment to emericellamide B by analogy. Finish pestalamide B's strain/locus/GCF/feature chain around feature 810 and NRPSPKS_85.

Audit all 25 Caesar rows, not only successful historical recoveries. An ambiguous isomer or product family may support a broader target set if the published task expressly permits that resolution. Do not force a precise name onto weaker evidence.

For each candidate, allow one documented source review and one focused resolution attempt, with a default cap of two curator-days before a disposition. Record what specific new evidence would reopen it. Draft author inquiries where useful; send them only with authorization. Awaiting correspondence does not prevent disposition of the rest.

Screen A. fischeri and A. flavus using the same rules. Their reported metabolite or profile counts are not accepted-label counts. NPLinker-generated associations alone cannot become truth for evaluating NPLinker.

At the end of this phase, produce an internal capacity table showing accepted relationships, independent pathway groups, cohorts, chemical classes, evidence tiers, and spectral coverage. Seek a second scientific review of every main-comparison label; record disagreements and how they were resolved. If review is researcher-led rather than independent, record that limitation explicitly.

If coverage is too narrow, undertake one additional, two-week targeted public-data search directed at missing diversity or evidence. Then make a documented decision: freeze a scoped comparative benchmark, approve a named further acquisition effort, or report a specific unresolved prerequisite. Judge whether results can inform the declared comparison using the diversity table and planned uncertainty analysis, not a fixed arbitrary query minimum. Do not loop indefinitely, invent a minimum of 30 pathways, or silently replace the benchmark with a descriptive audit.

### Phase 3: Build versioned analytical inputs

Construct the feature-only release first. Store abundance matrices, presence rules, sample metadata, normalized assemblies, BGC sequences and boundaries, GCF memberships, positive sets, and exclusion records under stable schemas.

Freeze how technical replicates, cultures, and media become the observational units used in co-occurrence scores. Repeated media from one strain must not increase the apparent number of independent genomes. Preserve condition-level data for sensitivity analysis.

For GCFs, distinguish source-selected families from families reconstructed under a declared procedure. Record tool versions, reference databases, thresholds, and cluster boundaries. Caesar labels helped select historical GCF thresholds; the source-recovery analysis must acknowledge that exposure.

A reconstructed release needs a complete defined BGC/GCF universe for its stated scope. The 29 selected HTML records cannot stand in for all predicted clusters. This does not mean every cohort BGC must become a scored query: supported queries and their full measured-feature candidate pools remain distinct from genomic context. Choose reconstruction parameters from external defaults or development data, then freeze them before evaluation.

Time-box recovery of historical feature-to-MS/MS membership to five working days. Accept a join only with auditable scan/native identifiers or an equivalent validated project export. Mass and retention-time proximity alone can produce ambiguous joins.

If historical joins remain unavailable, create a new processed release from raw files with versioned conversion, feature detection, alignment, filtering, and spectral export. Give it new feature IDs. Re-establish positive targets using the available chemical evidence and record ambiguous matches or lost targets. Never reuse historical feature numbers as if they survived reprocessing.

Keep the feature-only comparison moving while this proceeds. A spectral extension can be deferred with an explicit coverage report; its incompleteness does not invalidate abundance-based evaluation.

Deliver source-to-output manifests and a machine-readable validation report. Each admitted query must have at least one valid positive inside its released candidate universe. Structural uncertainty remains separate from MS/MS availability. Fix query eligibility before method runs; report excluded positives and their reasons so availability filtering stays visible.

### Phase 4: Implement fair comparisons

Publish a method manifest describing the actual score or workflow, implementation version, parameters, input fields, pretrained assets, reference-database versions, and failure behavior. NPLinker alone is not a method name.

The core suite should include repeated random ranking, global abundance/prevalence controls, a prevalence-difference score, and a declared Metcalf co-occurrence implementation. A second compatible substantive linking approach is desirable beyond simple controls; if unavailable, decide whether named expansion or adapter work is needed before claiming broad multi-method coverage. Do not count two wrappers around the same score as distinct approaches.

Use prevalence difference as an explicit score: feature prevalence among family-bearing strains minus prevalence among non-bearing strains, with both denominators and degenerate cases specified. Verify the Metcalf implementation against its documented contingency-table weights and normalization. Do not substitute a similarly named score.

Evaluate NPClassScore-assisted workflows, spectral IOKR, or NPOmix only after checking actual fungal input compatibility and output direction. Chemical classes must come from the released prediction pipeline or an explicitly allowed external source, not the gold product identity. Record an unavailable method as unavailable with a reason, not as a fabricated low score.

Compare methods within matched information tracks. Report both a common eligible subset and coverage on the full track population. A method needing MS/MS must not appear superior merely because difficult spectrum-free cases disappeared from its denominator.

Define an adapter contract returning query ID, candidate ID, score, method/run IDs, and status. Preserve ties; abstentions and execution failures have separate reason codes. Validate unknown IDs, duplicates, invalid scores, partial rankings, and candidate-set mismatches before scoring. Gold answers must be accessible to the evaluator, not method input objects.

Meaningful tests must cover hand-calculated ranks and multi-positive cases, ties at a cutoff, all-tied scores, abstention, malformed outputs, duplicate aliases, and reversed ranking direction. Verify a tiny end-to-end fixture with deliberately shuffled IDs so accidental row alignment cannot pass. Check baseline values against hand-worked examples or the upstream reference implementation. Put these under `tests/` with fixtures under `tests/fixtures/` and keep real-data integration checks separately identified.

Demonstrate extensibility with a separately written adapter using only the published interface and documentation. Avoid tests that merely repeat the implementation's formula.

## Exposure, statistics, and experimental controls

Treat Caesar as public development or retrospective evaluation. Moving it into a new repository does not restore blindness.

Record exact training overlap, reference-record overlap, sequence/pathway similarity, chemical similarity where known, and unknown exposure for each learned method. Pretrained models whose training data cannot be audited receive an exposure-unknown designation.

For supervised tuning, assign related pathway groups and duplicate biological entities consistently to development/test partitions. Fit normalization or tuning choices only where permitted. If grouped cross-validation is more suitable than a tiny fixed test set, freeze folds before tuning and keep close members of a group together. A novel-pathway claim requires additional exclusion rules; ordinary known-pathway comparison does not. Describe co-occurrence methods' use of unlabeled cohort-wide observations as part of the task, rather than confusing that legitimate information with access to evaluation labels.

Separate independently supported labels from associations selected by the source method's correlation signal. Analyze each stratum and their differences. External cohorts provide another comparison setting, not automatic immunity from selection bias.

Predeclare:

- Primary summaries: pathway-group macro-averaged known-positive hit rate at ranks 1, 10, and 100, and reciprocal rank of the first supported target. Cap and label cutoffs where candidate pools are smaller.
- Secondary summaries: recovery of all curated positives, per-query ranks, coverage, abstentions, runtime, memory, and candidate-pool size.
- Multi-positive handling: any-hit retrieval and recovery across distinct supported products, with adducts/isotopes grouped so they do not inflate biological success.
- Tie handling: expected credit under uniform ordering within tied blocks, with best/worst rank bounds as a sensitivity analysis. Calculate the expectation for the declared metric, not the metric of a substituted mean rank.
- Missing-output handling: conditional results on covered queries plus end-to-end results assigning zero known-positive retrieval credit to abstention; processing failures remain visible separately. Partial output rules must be specified before evaluation.

Unknown candidates are unlabeled, not confirmed negatives. Do not present precision, false-positive rate, or AUROC as biological accuracy without the required negative evidence. A method's unsupported high-ranking candidate may still be correct.

Aggregate products within pathway groups before estimating overall uncertainty. Bootstrap paired differences at the pathway-group level, accounting for repeated groups across cohorts; do not resample every adduct, medium, or congener as an independent test. When there are too few groups for stable interval estimates, show paired results and leave-one-group-out sensitivity without pretending a nominal interval settles superiority. State whether inference is conditional on the observed cohort and label set.

Use repeated random rankings with fixed seeds and enough repetitions to stabilize reported summaries. Run label-independent candidate-difficulty analyses, strain/species or phylogeny-aware controls where data permit, and restricted permutations preserving relevant dependence. Report when few exchangeable units limit a control.

Freeze sensitivity analyses before the main run: direct versus reference-supported labels, source versus reconstructed GCFs, replicate aggregation, candidate filtering, class/spectral availability, exposure strata, and influential pathway groups. Parameters selected for better test performance require a new development designation or release. No statistically significant winner is required for completion.

## Results, figures, and paper

Write the introduction and methods while data work proceeds. Store a bibliography and claim-to-evidence ledger in `manuscript/`. Refresh the focused literature review at protocol freeze and before submission, using primary papers and current journal guidance.

Compare the contribution with [NPLinker](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008920), [NPClassScore](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-022-01444-3), [NPOmix](https://academic.oup.com/pnasnexus/article/1/5/pgac257/6847575), [NPLinker 2](https://doi.org/10.21105/joss.09528), [MIBiG 4.0](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701617/), and structure-retrieval resources. Do not claim fungal linking or BGC-to-structure retrieval is new.

Use [Caesar](https://www.nature.com/articles/s41589-023-01276-8), [Steffen](https://doi.org/10.1039/d5ob01965f), and [Xie](https://www.nature.com/articles/s41467-026-70721-8) as data-source references, with each cohort's exact contribution and limitations described. The proposed contribution is a reusable fungal measured-product comparison resource with audited evidence, fixed inputs, and honest coverage and uncertainty.

Prepare five main figures, combining panels where appropriate:

1. Task definition and provenance from strain/genome through query to measured target.
2. Curation flow and coverage by evidence class, pathway group, and cohort.
3. Paired method results with uncertainty and coverage.
4. Effects of source selection, exposure, candidate composition, and available inputs.
5. Traceable successes and failures, including corrected assignments where informative.

Supplement with complete query evidence, exclusions, method manifests, per-query results, resource costs, and reproducibility instructions. Generate tables and plots from frozen results rather than editing values manually. Maintain the main text, bibliography, figures, supplements, availability statements, and cover letter as separately reviewable artifacts.

At the capacity checkpoint, assess journal fit using current scope, recent comparable papers, data/code requirements, article type, costs, and expected contribution. Scientific Data is a candidate to screen if the main contribution is reusable data; Bioinformatics if the evaluation framework and comparison carry the paper; PLOS Computational Biology if results support a broader computational insight. These are provisional screening options, not verified recommendations or promised destinations. Select a primary and fallback venue before final formatting.

A scoped benchmark remains useful when method differences are inconclusive. Distinguish no resolved winner from no useful benchmark.

## Resources, release, and completion

Begin with processed deposits and targeted genome retrieval. Do not download every raw acquisition before the manifest and storage estimate exist. The reviewed A. flavus listing includes a roughly 1.8-GB processed archive, but that does not estimate the full raw-data footprint.

Maintain `planning/resource-estimate.tsv` with measured pilot retrieval time, storage, CPU-hours, peak RAM, review time, and projected full-run cost. Use local compute where suitable. Set a monetary cap with the user before paid cloud runs or services; continue independent work while that decision is pending. GPU access is optional unless an admitted method requires it.

Deliver a lockfile or container specification, workflow commands, checksums, and a small redistributable example. Separate restricted or unlicensed sources from distributable outputs. Public accessibility does not itself confer redistribution rights. Use download recipes and accession manifests where redistribution is not permitted. Choose explicit licenses for original code and data during release preparation after rights review.

A reproducer must start from a clean checkout and documented public inputs, regenerate the benchmark release or its declared reproducible stages, run the baseline/evaluator workflow, and reproduce headline tables within specified tolerances. Prefer a different researcher or environment; disclose the actual degree of independence. Record hardware, failures, manual interventions, and deviations. Fix documentation or workflow and repeat affected stages.

Publication readiness requires:

- Reviewed labels and exclusions, with no unsupported admission count.
- Frozen task populations and compatible methods evaluated under the same declared conditions.
- Per-query results, uncertainty, coverage, and limitations sufficient to assess every headline claim.
- A successful clean-checkout rerun, with its independence stated, and a working external-adapter example.
- Data/code licensing, author contributions, competing interests, and availability statements completed.
- A finished manuscript, supplement, figures, cover letter, and repository/archive release candidate.

Keep GitHub private until public release is authorized. Prepare archival deposit contents and DOI metadata, embargo or reviewer access where supported, and a tagged release before asking for publication approval. Do not publish third-party PDFs, private correspondence, or restricted data as a convenience.

After authorized release and submission, maintain a revision ledger linking each reviewer request to a response, analysis change, and manuscript location. Preserve the submitted benchmark version. Corrections produce a new release and impact assessment; they do not overwrite the evidence used in the original submission.

The endpoint is a defensible benchmark, reproducible paper, and completed submission/revision process. Acceptance remains the journal's decision.

## Start here and track execution

The first work package is Phase 1 plus the first three Phase 2 cases. Produce the initial source registry, declared task/evidence rules, sample reconciliation, and evidence packets for acetylaszonalenin, emericellamide A, and pestalamide B. Each packet ends in an admission decision or a specific recorded gap. Do not begin another general feasibility review.

Maintain `planning/WORKLOG.md` during execution with phase, action, artifact, evidence, blocker, and next action. Keep this plan canonical; record material protocol changes in a dated decision log before applying them. Create bounded software implementation plans when the evaluator and adapters are ready to build, preserving this research plan's scientific contract. A request to begin implementation is separate from this planning request.

The first checkpoint should answer what data have been retrieved, what the three example packets support, and what remains to resolve across the full census. It must not claim a completed benchmark or freeze a favorable query count from those examples alone.


## User amendment, 9 October 2026

The user adopted a version 1 target of 30 admitted relationships. Stop admission expansion at 30; preserve all evidence eligibility rules and keep evaluated coverage and independent query/group counts separate. This is an operational target, not a publication minimum or a requirement for 30 pathways. See [decision](../../protocol/decisions/2026-10-09-thirty-linkage-target.md). The earlier proposed time cap and evaluated-coverage targets were not separately adopted.
