# FungalLink benchmark contract

Protocol version: 0.1, initial Phase 1 specification, 2026-09-30. Status: proposed operational choices; not an admitted dataset or a scientific-review sign-off. Authority: [canonical project plan](../docs/plans/2026-09-30-2052-benchmark-paper-plan.md). The research audits supply starting evidence, not current acceptance decisions.

The benchmark asks how well compatible methods rank supported measured metabolite features for a fungal BGC or GCF, given fixed inputs, and how much of that task each method can cover. It supports a reusable comparison and accompanying paper. It does not require unfamiliar pathways, new knockouts, a fixed minimum number of pathways, or a significant winning method.

## Task and information boundaries

| Track | Query | Candidates and permitted information |
|---|---|---|
| Core GCF-to-feature | Versioned family with an explicit locus/member roster | Measured features; declared cohort-wide abundance/presence data, audited sample/genome crosswalk, GCF membership |
| BGC-to-feature | Sequence-defined locus with accession version and boundaries | Measured features; locus sequence, boundaries, declared homology/model inputs and any cohort context named in the track manifest |
| Spectral extension | Either query type, reported separately | Same feature universe where possible, plus validated feature-spectrum joins and declared predicted class inputs; narrower pools require a separately named release |
| Optional unfamiliar-pathway evaluation | Groups held out under a documented exposure rule | Separately frozen training/test groups and allowed external assets; not a prerequisite for the core benchmark |

BGC and GCF scores are never pooled into one headline result. A BGC-to-GCF transformation is part of a named workflow, not an implicit change in query type. Structure retrieval needs a separate experiment unless an explicit structure-to-measurement mapping makes its output comparable; disclose the added information.

Methods may use unlabeled observations across the released cohort when the track permits it. They may not read evaluator positive sets, evidence packets, curated product names, or gold-derived chemical classes through method input objects. External databases, pretrained models, public reference annotations, and predicted classes require named versions, allowed fields, and exposure records. Training on public answers must be disclosed; a new repository does not make Caesar blind. Freeze learned preprocessing and tuning on development data. Label-independent cohort normalization is allowed when declared.

## Entities and stable joins

Use opaque, immutable IDs with a type prefix and a registry, such as `strain:000001`; names, accessions, and historical feature numbers are aliases. IDs are never reused. Revision-sensitive entities carry an explicit version or a new ID with `supersedes_id`. Store alias provenance, mapping status (`verified`, `inferred`, `unresolved`), reason, curator, and date. Missing values are explicit and never converted silently into absence.

For the initial Caesar interface, use `cohort_id=caesar2023`. Derive acquisition IDs deterministically from that namespace and the exact source acquisition stem, preserving case and punctuation in the alias record and stripping only the recognized representation extension. Record the derivation algorithm. An acquisition stem is not a strain identifier; uncertain strain aliases remain explicit. Do not strip suffixes or merge stems through an undocumented name heuristic.

| Entity | Minimum identity and relationships |
|---|---|
| Study/cohort | Source accession/DOI; cohort defines a declared sample population |
| Biological strain | Organism and strain aliases, source identity evidence; distinct from an assembly |
| Culture | Strain, medium, growth condition, biological replicate and batch |
| Extraction | Culture, extraction protocol and replicate |
| Acquisition | Extraction, instrument run and technical replicate |
| File representation | Acquisition, format, source ID and byte checksum; mzML/mzXML copies are not replicates |
| Assembly | Accession including version, sequence checksum, strain correspondence, GenBank/RefSeq alias decision |
| BGC | Assembly, contig, coordinates/coordinate convention, sequence checksum, boundary procedure/version |
| GCF | Versioned member BGC roster, method/parameters, source-selected or reconstructed status |
| Feature | Cohort and processing-release ID, source row alias, m/z, retention time/unit; reprocessing creates new IDs |
| Spectrum | Acquisition and native scan identifier or validated export identifier, processing version, feature join provenance |
| Product target | Declared chemical resolution and a set of supported feature IDs; ion aliases share one product target |
| Query | Track, cohort, BGC/GCF version, candidate-pool version and positive-set version |
| Pathway group | Related queries/products joined across cohorts for weighting, splitting and uncertainty; membership evidence and revision |

Identical assemblies and accession synonyms do not create independent genomes. They also do not prove that two named cultures are the same strain. Preserve both kinds of relationship. Group closely related pathways and repeated biological entities consistently across development/test partitions; a pathway group is not automatically identical to a GCF.

Each source record needs a stable source ID, accession/DOI, retrieval URL/date, file size, checksum, version, reuse terms and expected content. Each derived artifact records source IDs, software/parameters, timestamp and checksum. Local paths belong in ignored configuration. Imported historical assets retain origin, revision/hash and license in `data/manifests/legacy-imports.tsv`; the release must work without neighboring repositories.

## Evidence and admission

One proposed query-product relationship receives one evidence record, with separate assessments of chemical identity, experimentally supported reference pathway, sampled-locus correspondence, and measured-target correspondence. Record source page/table/figure, actual organism/locus, alternative explanations, reviewer and disposition. Retain the source's chemical tiers separately from these decisions.

| Class | Rule and use |
|---|---|
| Directly supported | Experimental pathway-product evidence applies to the queried locus, or an experimentally represented member of the queried GCF, and the measured target is traceable. Eligible for the main comparison once reviewed. State which member has direct evidence; do not imply all members do. |
| Reference-supported | Experimental reference pathway plus justified sampled-locus homology/family membership, supported chemistry and a measured-target join. Eligible with its transferred scope stated. Homology transfer to another locus remains reference-supported. |
| Provisional | A decisive join is missing, or the relationship primarily rests on source correlation. Exploratory/source-recovery analysis only. |
| Rejected or unresolved | Conflict, incorrect assignment, unsupported identity or unresolved target. Keep the reason and reopening evidence in the exclusion ledger; do not score as a negative. |

Reference transfer must report sequence identity and coverage, gene content, biosynthetic organization, and competing-locus checks. Biology review must set applicable decision criteria before cross-case application. No universal identity threshold is invented here. Congener transfer requires its own evidence; emericellamide A cannot establish emericellamide B by analogy. A new perturbation in every historical culture is not required.

Chemical ambiguity can support a broader, explicitly named target only where the evidence supports that resolution. An ambiguous isomer group is one target, not several proven products. Keep separate fields for biological admission and input readiness (`feature_ready`, `sequence_ready`, `spectral_ready`, with reasons). Missing MS/MS does not disqualify an otherwise supported feature-only label. Spectrum joins require auditable native identifiers or a validated export; mass/retention proximity alone is insufficient.

Seek a second scientific review of main labels. If only researcher-led review is available, identify the reviewer and disclose that limitation. Automated checks cannot provide biological or chemical sign-off. Neither this document nor the initial three case packets establishes a final query count.

## Candidate pools and query eligibility

Start Caesar from all 9,339 audited workbook rows, retaining unnamed features. Reconcile the published 9,301 count before release. The 362 workbook sample columns, 357 mapped stems, and historical 338 included acquisitions describe different processing states, not independent-sample counts. The [historical inclusion reconciliation](../docs/data/historical-inclusion-reconciliation.md) explains 338 without adopting the old strain corrections. Audit the complete 25-row association census rather than selecting previously successful recoveries.

Apply label-independent integrity/QC rules before method runs: parseable unique feature IDs, documented handling of duplicate records, valid measurements, and explicitly assessed contamination or processing artifacts. Do not remove a candidate for lacking a chemical name, MS/MS, or a favorable score. Every removal gets a reason and source-to-release mapping. Changed filters produce a named candidate-pool version; give both original and retained counts. Biological ion aliases remain measured candidates, but are grouped for product recovery. Duplicate file representations are not distinct measured candidates.

All queries in a cohort/track use the same pool unless a documented technical scope requires separate pools. A label is track-eligible only if its query exists, permitted required inputs and sample joins are valid, and at least one supported target lies in the pool. Record losses of other supported products, and preserve their original denominator in the release flow report. Method-specific input gaps cannot retroactively remove a query from the track population.

Source-selected GCFs and reconstructed GCFs are separate releases. Selected HTML records do not establish a complete reconstructed genomic universe. Reconstruction needs a declared complete BGC/GCF scope, parameters chosen without test optimization, and full rosters. Supported scored queries remain a subset of that genomic context.

## Observational units and replicate aggregation

The primary co-occurrence unit is the biological strain within a cohort. Preserve culture/condition data for sensitivity analyses. This prevents repeated media or file formats from increasing the apparent number of genomes.

Proposed default: after acquisition QC and a frozen, label-independent normalization, take the median intensity across valid technical acquisitions per extraction, then medians across extractions per culture and cultures within a strain-condition. Retain measured zeros; do not substitute zero for missing acquisitions. Presence requires a frozen cohort-specific detection/blank rule applied at the strain-condition level. Set strain presence to any detected condition and strain abundance to the maximum condition-level value. This represents detectable production under the sampled conditions. Report condition counts because unequal sampling offers unequal detection opportunities.

The exact normalization, detection threshold, blank rule and valid condition roster remain release decisions based on source documentation and QC, before comparative ranks are inspected. If historical processing cannot support this hierarchy, release its documented aggregation separately rather than pretending it follows these defaults. Sensitivities use equal condition opportunity where possible and the median across conditions. Neither variant adds strain observations.

Genomic presence is `1` for a verified locus/member, `0` only when a complete-enough declared search supports absence, and missing otherwise. Freeze a common eligible strain roster per query for core co-occurrence methods; do not let each method choose favorable strains. Candidate-specific missingness is a release validation issue with an explicit handling rule, not automatic absence.

## Method interface and freeze

Each adapter returns `query_id`, `candidate_id`, finite numeric `score`, `method_id`, `run_id` and status; larger scores rank first. Query-level status includes `ok`, `abstain`, `input_unavailable`, `execution_failure`, or `invalid_output`, with machine-readable reason. Missing queries are failures unless explicitly classified with evidence. Gold remains evaluator-only.

The primary interface requires complete rankings of the frozen candidate pool. Unknown IDs, duplicate candidate rows, nonfinite scores, unannounced direction changes, and partial rankings are invalid. Do not silently rank omitted candidates last. A workflow can predeclare a label-independent fallback for missing candidate scores; it then returns a complete ranking, records fallback counts and becomes a distinct workflow. A top-list-only method needs a separately specified censored-ranking experiment before entry.

Freeze actual software commit/package/container digest, dependencies, score definition, parameters, normalization, assets/database versions and checksums, seeds, resource limits and failure rules. Proposed baseline definitions and metric policy are in [analysis-plan.md](analysis-plan.md). NPLinker is a framework name, not a sufficient method specification. A second compatible substantive approach remains an implementation/admission question; do not count two wrappers around one score as distinct approaches.

Before the main run, a release manifest must identify queries, candidates, positives/product aliases, pathway groups, eligible strains, preprocessing, allowed information, exposure, methods and reviewer decisions by checksum. Record protocol edits in a dated decision log with rationale, affected artifacts, whether results were seen, and required reruns. Once results have informed a choice, call the affected data development/retrospective or issue a new evaluation release. Preserve earlier manifests and results. Public release and external correspondence still require user authorization.
