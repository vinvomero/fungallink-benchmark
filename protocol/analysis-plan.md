# FungalLink analysis plan

Version 0.1, 2026-09-30. Initial specification under the [benchmark contract](benchmark-contract.md) and [canonical project plan](../docs/plans/2026-09-30-2052-benchmark-paper-plan.md). Data populations, software versions, reviewers and run limits are not yet frozen. This document defines proposed estimands and scoring rules; no benchmark results were generated to choose them.

## Comparison population

Report each query type, information track and candidate-pool release separately. Directly supported and reference-supported labels enter the main comparison after admission; provisional source associations enter a separately named exploratory analysis. Preserve both label-evidence class and source-selection status. Biological support does not erase selection by a source correlation method.

For query q, let C_q be its frozen candidate set, N_q its size, and P_qj the nonempty feature set for distinct supported product j. Let J_q be the number of product targets and P_q the union of these sets. Adducts/isotopes of one product belong to one target. If a feature cannot distinguish two proposed products, adjudicate a single ambiguity target before scoring; never count one ambiguous ion as two separately proven products. Report positive-target losses from candidate filtering outside these conditional scoring denominators.

The primary summaries are known-positive any-hit at k = 1, 10, 100 and reciprocal rank of the first supported target. Define k_q = min(k, N_q), print the cap and affected query count, and report pool sizes. A high score measures recovery of curated targets, not correctness of all high-ranked candidates. Unknown candidates are unlabeled; no biological precision, false-positive rate or AUROC will be claimed without independently established negatives.

## Exact tie credit and multiple products

For an untied ordering, H_q(k) = 1 if any member of P_q appears by k_q, otherwise 0; RR_q = 1/min rank(P_q). Expected values under a uniform random permutation within each equal-score block are the reported scores. Use exact serialized score equality by default; any numerical rounding/tolerance is a method-level choice frozen before evaluation. Never substitute a mean rank into a nonlinear metric.

The following formulas are direct combinatorial definitions of this protocol, not claims about a published evaluator. Let the earliest score block containing any member of P_q have a candidates strictly above it, t tied candidates, and p positive candidates. For r = min(t, max(0, k_q - a)):

```
E[H_q(k)] = 1 - choose(t-p, r) / choose(t, r)
E[RR_q] = sum[u=1..t-p+1] choose(t-u, p-1) / choose(t,p) / (a+u)
```

Set choose(n,r) = 0 when r > n or r < 0. The first formula counts the probability of drawing no positive in the first r positions. The second places the first positive at position u and chooses the remaining p-1 positions after it. It therefore averages reciprocal ranks directly.

For each product j, repeat H using P_qj. Secondary distinct-product recovery is `R_q(k) = (1/J_q) sum_j E[H_qj(k)]`. Report this together with any-hit and the fraction recovering every curated product. Do not count every adduct as an independent success. For exact all-products credit, remove products already recovered strictly above the block crossing k_q; call the remainder U. If the boundary block B has size t and r selected positions, then:

```
E[all products recovered] =
  sum[S subset of U] (-1)^|S|
    * choose(t - |union[j in S](P_qj intersect B)|, r) / choose(t,r)
```

This inclusion-exclusion expression handles products lacking any boundary-block candidate by returning zero, and yields one if U is empty. At a block boundary, r can equal t. Implement an equivalent exact counting routine if enumeration is costly; verify it against small exhaustive permutations. Report per-product first-target ranks and best/worst tie bounds as well. For any-hit and RR the first-positive rank bounds are a+1 and a+t-p+1. Use valid whole permutations, not incompatible per-product extremes, for all-products bounds.

Acceptance fixtures before real scoring: with two positives in an all-tied pool of four, expected hit@1 is 1/2, hit@2 is 5/6, and RR is 13/18. With two distinct singleton products in that pool, distinct-product recovery@2 is 1/2 and all-products@2 is 1/6. Add shuffled-ID joins, duplicate aliases, multiple ion aliases for one product, reversed direction, cutoff-spanning ties, abstention and malformed/partial-output fixtures. These are requirements for later implementation, not completed tests.

## Coverage and paired denominators

Let Q be every frozen track-eligible query. Partition every method's Q into valid complete output, abstention, input unavailable, execution failure and invalid output. A method that cannot be installed or cannot support the track is reported as unavailable, outside the ranking comparison, with its reason; it does not receive an invented performance estimate.

For an admitted runnable method, end-to-end scores retain all of Q and assign zero retrieval credit to each non-output status. Zero measures failure to deliver retrieval in this workflow, not a claim that the method ranked a true target last. Keep each status count separate. Conditional scores use only valid outputs and print that denominator. Coverage is valid-output queries divided by |Q|, accompanied by per-status rates and pathway-group coverage. An empty conditional set is `not estimable`, not zero.

For each comparison roster, freeze the common input-eligible subset from manifests before runs, without using method performance. Compare end-to-end scores there and on full Q, retaining failures. Also show a paired valid-output subset for diagnostic conditional performance, listing omitted queries and groups. This last subset is outcome-dependent and cannot replace the main comparison. A spectral method's reduced coverage must remain visible against the full parent feature-track population, even when a separate spectral-ready experiment is reported.

## Weighting and uncertainty

Aggregate products inside query metrics first. Average query metrics within each pathway-group/cohort, average those cohort means within each pathway group, then give each pathway group equal weight. This prevents a pathway represented by many loci, congeners or cohorts from dominating. Publish query-, cohort- and group-level values and membership counts so the weighting is auditable. Apply the same hierarchy to end-to-end status/coverage summaries; also report plain query counts.

For a paired contrast, calculate each group's method-A minus method-B score using exactly the same eligible query/cohort membership. Bootstrap whole pathway groups, with replacement, retaining every cohort observation of a sampled group together. Proposed default: 10,000 paired draws, seed 20260930, percentile 95% intervals for mean differences. Record generator/library versions and Monte Carlo stability. Cohort-specific contrasts use the same grouping rule within cohort. Never independently resample ions, congeners, strains or media as if they were pathway tests.

These intervals are conditional on the observed cohorts, candidate pools and curated label set; pathway groups also require a credible independence judgment. Report group count, individual differences, ties, interval width and leave-one-group-out estimates for every headline contrast. With one group, uncertainty across groups is not estimable. With few groups, label intervals descriptive and assess their discrete support and sensitivity; do not impose a query-count gate or interpret a narrow nominal interval as proof of broad superiority. If relatedness crosses assigned groups, merge groups or add a coarser-group sensitivity before claims.

The four primary metrics describe retrieval; they are not four opportunities to select a winner. Report all planned method pairs and metrics with effect sizes and intervals. No confirmatory superiority test or multiplicity-adjusted p-value claim is planned for v0.1. Such a claim requires a dated analysis amendment before the relevant results are inspected. Inconclusive method differences do not prevent benchmark completion.

## Proposed baselines

| Workflow | Frozen definition to implement |
|---|---|
| Uniform random ranking | Uniform permutations of the full candidate pool, with recorded per-query/per-repeat seeds and stable ID ordering; report both exact expected retrieval and repeated-rank variability |
| Global prevalence | Fraction of eligible strains with detected feature, independent of query genomic presence |
| Global abundance | Mean of released strain-level normalized abundance across the same eligible strains, independent of query genomic presence |
| Prevalence difference | `mean(feature present | genomic presence=1) - mean(feature present | genomic presence=0)`; report both denominators, abstain if either is zero |
| Declared Metcalf co-occurrence | Raw contingency score and a separately named standardized workflow, verified against the primary definition and a pinned implementation; these are related variants, not two independent substantive approaches |

For Metcalf, with genomic presence first and feature presence second, the raw score is `10*n11 - 10*n01 + n00 + 0*n10`. Standardization uses the mean and variance under fixed genomic/feature prevalence and hypergeometric overlap. Verify the implementation, orientation and zero-variance behavior before admission. This follows the score and null described in sections 2.1–2.2 of the [NPLinker primary paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008920), read for this specification. Its use on individual measured-feature presence vectors is an explicit adaptation from the paper's family-level formulation.

Proposed standardized-workflow convention: a zero-variance candidate receives neutral score 0 with a recorded `zero_variance` flag; if genomic presence has no variation, abstain for that query. Check and disclose any difference from the pinned upstream implementation; changing that convention defines a different workflow. Unresolved genomic presence is not absence.

Begin random controls with 10,000 repeats and seed 20260930. Derive per-query seeds from an explicitly documented stable digest, never a process-dependent hash. Compare simulated mean metrics with exact tie/all-tied expectations. Double repetitions if Monte Carlo standard error exceeds 0.001 for any reported aggregate; report repetitions and achieved error. Distinguish random-ranking variability from uncertainty across biological pathway groups.

NPClassScore-assisted workflows, spectral IOKR and NPOmix are candidate additions, not promised admitted methods. Check fungal inputs, ranking direction, allowed information and output completeness first. A second compatible substantive approach beyond simple controls remains unresolved. Freeze software and database versions after compatibility testing; do not write an unverified version into the manifest. Include compute time, peak memory, setup cost, failure reasons and fallback behavior for every admitted method.

## Exposure, controls and changes

Caesar is development/retrospective. Log source-selected GCF thresholds, historical rank inspection, exact training/reference overlap, pathway/sequence similarity, chemical similarity where known, and unknown exposure. External cohorts are not automatically unexposed. Freeze grouped folds before supervised tuning, keep repeated biological/pathway entities together, and fit label-dependent decisions on development data only. An unfamiliar-pathway claim needs its own exclusion rules and population.

Predeclare these sensitivities before the main run: direct versus reference-supported labels; independently supported versus source-correlation-selected cases; source versus reconstructed GCFs; any-condition versus median/equal-opportunity aggregation; candidate filtering and pool size; spectral/class availability; exposure strata; and leave-one-pathway-group-out influence. Use only variants whose data exist, listing unavailable analyses and why. Do not choose the best-performing variant as the new primary result.

Candidate-difficulty summaries use label-independent descriptors such as candidate prevalence, abundance, pool size and spectral availability. Where strain/species/phylogeny metadata permit, compare within declared strata and permute whole strain genomic profiles relative to metabolomic profiles within defensible exchangeability blocks, retaining cultures/conditions together. Freeze block construction, permutation statistic and seed before running that control. Do not treat poorly exchangeable strains as a valid null; report when too few units allow an informative permutation. These controls assess confounding and task composition, not proof that every candidate is biologically false.

Analysis freeze requires signed or otherwise attributed scientific dispositions, a frozen release manifest, pathway groups, method roster/versions, common subsets, split/exposure records, score/failure conventions, seeds, sensitivity availability and evaluator fixture validation. Vin Vomero is the research lead. No external reviewers are currently available, as confirmed by the research lead on 2026-09-30. Record researcher-led scientific dispositions separately from automated source checks. Statistical review and a separate reproducer remain unassigned; their absence does not stop acquisition, implementation or drafting, and any later rerun must state its actual independence.

Before freeze, log substantive edits with their rationale and evidence. After freeze, preserve the original artifacts; record each deviation, whether comparative results were already visible, its impact and the reruns required. Corrections generate a new release. Any performance-driven parameter choice moves the affected analysis to development status. Final admitted population, method coverage and uncertainty remain execution findings.
