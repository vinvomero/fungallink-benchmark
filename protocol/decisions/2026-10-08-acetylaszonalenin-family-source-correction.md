# Acetylaszonalenin historical family-source correction

Date: 8 October 2026. Assistant-curated evidence correction under the user's delegated scientific judgment. This changes the interpretation of retained source metadata, not the accepted named-core BGC, its biological label or its assembly-quality limits.

## Contradiction and resolution

The September packet `docs/evidence/acetylaszonalenin.md` calls the publisher DMAT_34 / DS027698.1.region002 a different locus at 778,075–809,148. The October correspondence packet inherited that exclusion. Tracing the cited neighboring ledger shows those coordinates accompanied by antiSMASH version 8.0.4. The later query-context record then looked for the successor region004 name in historical publisher displays. Region numbers do not identify the same interval across annotation runs.

The exact retained publisher DMAT_34 HTML (SHA-256 `abc266aef43318cacd513263aeb0eb8d8e9165e30b8697c72f9f74b50a029c73`) instead contains EAW16180.1, EAW16181.1 and EAW16182.1 inside the SVG belonging specifically to sampled FMGX0033 / DS027698.1.region002. Each complete openBlast protein string equals the accepted named-core annotation: 2,359, 437 and 509 residues. The same sampled anchor occurs on NRPS_85. The check scopes to the sampled block, not the separately inserted MIBiG reference. Gene order and displayed arrow directions agree with the accepted core; their polygon coordinates are retained for inspection.

The old blanket claim that the publisher family lacks the accepted source locus is therefore superseded. The newer same-numbered interval can still be a different locus; it cannot supply coordinates for the publisher's historical region. The historical full-region nucleotide boundaries remain unverified. No equivalence between complete historical and successor regions is inferred.

## Evaluation decision

Permit a separately declared DMAT_34 family view of existing relationship `caesar2023:corrected:5`, anchored by that exact sampled protein correspondence and the already-approved chemistry/reference evidence. Keep the corrected named-core BGC as the original biological query identity. Choose DMAT_34 because it is the source's recorded association, before evaluating this view; NRPS_85 is an alternate representation, not another independent positive or a performance-based choice.

The full source roster contains three sampled members. Existing population mapping gives three members and 102 documentary nonmembers among 105 included observations; eleven withheld rows stay unknown. Roster nonmembership does not establish genomic absence. Do not assert production by every family member or increase biological admission counts. Retain the contaminated-assembly flag, unknown locus-specific status and absence of a genome-wide uniqueness claim.

Next: freeze a separate retrospective extension with all 9,339 candidates, the existing 18 observation rosters, unchanged method versions and a separate gold channel before computing scores. Preserve all current original, expanded, emericellamide and running phylogeny packages. Prior benchmark results are known; this will not be a prospective evaluation.

## Saved evidence

`data/interim/acetylaszonalenin-family-reconciliation-2026-10-08/` contains both exact HTML files, `verification.json`, `membership.tsv` and a bounded excerpt of the prior coordinate record with its source hash. Existing evidence and approved protocol records are preserved unchanged. This dated correction must be read alongside their older exclusion wording.
