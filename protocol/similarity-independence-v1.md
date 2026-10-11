# Similarity and dependence protocol, version 1

Frozen before pair computation on 11 October 2026. The accepted plan is `docs/plans/2026-10-11-1704-similarity-independence-plan.md`. This analysis does not change admissions, frozen groups, scores or releases. It covers 30 relationships, 16 biological queries, 11 complete, two partial and 17 missing input states. Automated extraction and checks are attributed to Codex; chemical and biological scientific review remains pending.

The reproducible runner records the SHA-256 of this protocol, the accepted plan, all four backbone tables, consumed files, parameters and its own source before computing pair values. Its manifest pins Python and installed package versions and hashes their distribution records. Original text, sequences, boundaries and uncertainty remain available beside derived representations.

## Structures

A structure enters the supported primary set only when an admitted product's source evidence and a stable reference identifier support its mapping to the retained structure record. Name equality alone is insufficient. Each of the 30 relationships receives a disposition, with alternative members in separate rows. Proposed structures remain in a separate scenario; unavailable or unresolved structures are null. Formula checks report the RDKit formula and comparison with any retained source formula; unavailable source formula is explicit. Source InChIKeys are preserved even when their stereochemical layer disagrees with the SMILES.

RDKit sanitization preserves charges, isotopes and supplied stereochemistry. No tautomer canonicalization or neutralization occurs. Unsupported multi-component inputs are excluded. Binary Morgan fingerprints use radius 2, 2,048 bits and bond types; the primary excludes chirality. Tanimoto is bit intersection/union. A separate chiral sensitivity is eligible only when both molecules have no unassigned potential stereocenters. Exact isomeric canonical equality is recorded separately. All unordered relationship pairs remain accounted for, including null pairs. Alternative sets retain all member combinations and minimum/maximum. Flags at 0.7 and 0.9 are descriptive.

## Genomic representations

Extract all members and embedded proteins in the seven retained source-selected family HTML files, including reference members, with archive/member hashes, source IDs, protein order and annotations. Accepted locus and construct files are distinguished from reference proxies and individual CDS records. Do not equate a source-selected family with the full BGC universe.

New global alignments use Biopython BLOSUM62, gap-open -10, gap-extension -0.5, including terminal gaps. Select the first optimal alignment returned by the pinned library deterministically; record the number of optimal paths, or an explicit overflow. Identity is identical nongap pairs / paired nongap residues; each coverage is paired residues / full sequence length. Full-sequence exact equality uses the strings and hashes. Compatible source-annotated biosynthetic roles define comparison eligibility; incompatible or unclassified roles have null similarity. Broad PKS, NRPS and hybrid classes are distinct. For bounded locus pairs, retain reciprocal best ties across compatible annotated proteins, and original order. Qualifying fractions use 70% or 90% identity with at least 80% coverage of both proteins. Completeness denominators include unclassified annotated proteins, which cannot be declared dissimilar from missing role assignments. Scores and family distributions describe represented loci, not verified orthology or product equivalence.

## Spectra

Use all 91 Trichoderma and 291 black-yeast native joined spectra. Within-pool unordered pairs are eligible when both processed peak lists are nonempty. Cross-pool pairs require known compatible polarity and charge; excluded pairs retain a reason. Preserve native acquisition/scan provenance and unknown instrument or collision energy. No mass/retention-time join to historical Caesar features is inferred.

Keep finite positive peaks at m/z >=10; remove peaks within +/-1 Da of known precursor; retain peaks at least 1% of the remaining base peak; square-root intensities and L2-normalize. Record all filtering counts. Use the actual matchms CosineHungarian implementation with tolerance 0.02 Da, mz_power=0 and intensity_power=1. Record cosine and matched peaks. Flags require >=6 matched peaks and cosine >=0.7 or >=0.9. Exact native-scan and exact sorted original peak-list duplication are separate. Similarity does not identify isomers, adducts or a pathway product.

## Dependence and exposure

Established typed edges include identical query, curated shared pathway, shared construct/host and shared study/candidate pool. `not_adjudicated` is never a shared pathway. Observation grouping reuses the existing ledger; no assembly-string-derived biological replicate claim is made. Descriptive chemical/spectral resemblance and sequence equality are separate edge types with endpoint namespaces and provenance. Proposed connected-component scenarios print the edge types used and merger edges. Frozen groups remain authoritative. No independent holdout is established merely by absent edges; with one complete-analysis group, between-group uncertainty is not estimable.

Exposure is assessed per actual method layer and declared local asset: source selection, public reference membership and weight-specific training membership remain separate. Allowed statuses are confirmed_overlap, no_match_in_declared_complete_roster, partial_roster_no_match, unknown and not_applicable. Neither a class table nor Rosetta mappings establish training membership. Deterministic controls have no learned training set. No new weights or broad external acquisition are permitted.

## Verification

Check authoritative ID joins, all pair denominators, canonical ordering, missing values rather than zeros, exact duplicates, independent hand-calculated alignment/fingerprint/cosine fixtures, sparse spectra and alternative-set ranges. Run focused tests before and after implementing the computational functions. Record a red result when the new implementation is absent. Check protected hashes after the run. Scientific interpretation is not validated by these software checks.
