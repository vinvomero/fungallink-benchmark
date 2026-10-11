# NPClassScore counting kernel

This independently written stdlib kernel computes forward genomic-to-chemical class frequencies from the NPLinker 1.2.0 compound table. It is a bounded Phase 4 implementation unit under `docs/plans/2026-09-30-2052-benchmark-paper-plan.md`. It supports a separately authored adapter; it does not establish fungal input compatibility or add an independent substantive linking method to the benchmark.

The reference is NPLinker commit `d01a68a4b0569907d7e28d1a673a82a6790b7346`: `ClassMatches._read_mibig_classes`, `_get_class_counts`, `_get_scoring_tables`, and `NPClassScoring._npclass_score`. No upstream implementation or production class asset is vendored. The synthetic test table is original test data.

## Public Python interface

Import `load_class_table` and `score_classes` from `scripts.npclassscore`. These functions use no third-party dependencies and make no network calls.

```python
from scripts.npclassscore import load_class_table, score_classes

table = load_class_table("path/to/MIBiG2.0_compounds_with_AS_BGC_CF_NPC_classes.txt")
result = score_classes(
    table,
    {"mibig_classes": ["Polyketide"]},
    {"npc_pathway": "Polyketides"},
)
assert result["status"] == "ok"
assert result["score"] == 548 / 722
source_digest = table.metadata["source_sha256"]
```

`load_class_table(path)` accepts a filesystem path or `pathlib.Path` and returns a `ClassTable` object with two public attributes, `metadata` and `counts`. Treat both as read-only. Malformed tables raise `ValueError`; file-access errors propagate. The loader records the actual bytes' digest but does not enforce the production pin: a production adapter must compare it with the manifest before using the table. This permits the same loader to read the synthetic fixture.

`metadata` is JSON-compatible and has these fields:

| Field | Type and meaning |
|---|---|
| `source_sha256` | Lowercase hexadecimal SHA-256 of the original file bytes |
| `source_size_bytes` | Integer byte length |
| `compound_rows` | Integer number of unique compound identifiers, not unique BGCs |
| `genomic_levels` | Scorer-supported names: `mibig_classes`, `as_classes` |
| `table_genomic_levels` | Counted names: `mibig_classes`, `class:subclass`, `as_classes` |
| `chemical_levels` | All nine chemical columns listed below |
| `vocabulary` | Dictionary from level name to sorted list of observed terms, including terms without a partner on the other side |
| `vocabulary_sizes` | Dictionary from level name to integer vocabulary size |
| `pair_totals` | Dictionary `[genomic_level][chemical_level]` giving total Cartesian pair observations, not compound count |

`counts[genomic_level][chemical_level][genomic_term][chemical_term]` is an integer observation count. All level combinations exist; term keys exist only when observed in a pair. `class:subclass` counts remain available for inspection but are not a scoring input. Missing term keys are not stored as zeros.

`score_classes(table, genomic_classes, spectral_classes)` accepts dictionaries, never gold labels. The caller supplies genomic classes already normalized to the table's vocabulary. Supported genomic keys are exactly `mibig_classes` and `as_classes`; each value is a list of nonempty, trimmed strings. Empty lists and omitted keys mean absent annotations. This function performs no BiG-SCAPE conversion, antiSMASH conversion, or GCF aggregation.

Supported spectral keys are `cf_kingdom`, `cf_superclass`, `cf_class`, `cf_subclass`, `cf_direct_parent`, `npc_class`, `npc_superclass`, `npc_pathway`, and `npc_isglycoside`. A value is one nonempty, trimmed top-predicted term string, or Python `None` (JSON null) for an absent prediction. Omitted keys also mean absent predictions. `npc_isglycoside` uses string labels such as `"0"` and `"1"`. Prediction probabilities are neither accepted nor used. Empty strings are malformed, not null. Keys outside the supported names, wrong container/value types, and malformed strings raise `ValueError`.

Each result is JSON-compatible. Common top-level fields are:

| Field | Meaning |
|---|---|
| `source_sha256` | Digest copied from `table.metadata` |
| `direction` | Always `"genomic_to_spectral"` |
| `pairs` | List of usable pair audit objects |
| `skipped_pairs` | List of pair identity objects with `reason: "missing_denominator"` |
| `unknown_terms` | List of objects with `side` (`genomic` or `spectral`), `level`, and `term` |

A pair identity contains `genomic_level`, `genomic_term`, `spectral_level`, and `spectral_term`. A usable pair adds integer `count`, integer positive `denominator`, and float `score`. Pairs are ordered by sorted genomic level, genomic term, then spectral level. Repeated input genomic terms are assessed once; this does not deduplicate the compound reference table. Unknown-term audits are ordered by side (genomic first), sorted level, then sorted term.

Successful results add `status: "ok"` and float `score`, the maximum score among usable pairs. At least one usable pair is required. There is no cutoff, tie breaking, confidence weighting, or score transformation.

Unavailable results add `status: "input_unavailable"` and one `reason`, with no top-level `score`. Reasons are checked in this order:

1. `unknown_vocabulary`: any supplied term is outside that level's reference vocabulary, even if another supplied pair could score. The unknown terms are listed and no pairs are evaluated.
2. `missing_genomic_classes`: no genomic terms were supplied.
3. `missing_spectral_classes`: no non-null spectral term was supplied.
4. `no_usable_class_pairs`: known terms exist on both sides, but none has a positive forward denominator. The skipped pairs identify why.

An adapter should preserve these unavailable states and reasons rather than inventing a low score. It must supply benchmark query/candidate/run identifiers, verify candidate universes, and record prediction provenance under the benchmark adapter contract. Those operations are outside this kernel.

## Counting and direction

The UTF-8 TSV must contain exactly these columns, once each, in any order: `compound_name`, `class:subclass`, `as_classes`, `smiles`, `inchi_key`, and the nine chemical levels above. Every data row must have the full number of columns, including empty trailing fields. Empty or duplicate compound identifiers, malformed headers, row widths, and empty/untrimmed terms within populated class cells raise `ValueError`. There must be at least one compound row. Structure strings are carried in the file but unused.

Split `class:subclass` and `as_classes` on commas. Every populated MIBiG entry has a colon, with a nonempty base class and an optional subclass. Subclass terms retain the full `Class:Subclass` string. Split chemical labels on semicolon followed by a space (`; `). Empty cells have no terms. Cell term order does not affect counts, and repeated labels in a cell retain their multiplicity.

For the base MIBiG classes, follow the inspected upstream rule: if at least two class entries contain `nrp`, `pks`, or `polyketide` case-insensitively, replace those entries with one `PKS-NRP_Hybrids` term and keep the other classes. This is the source's substring/count rule, not a new biological interpretation of hybrids. Replace exact `Alkaloid` base labels with `Other`. Neither transformation alters subclass or antiSMASH counts.

For each compound row, add one observation for every Cartesian combination of a genomic term and chemical term. Different compounds sharing a BGC prefix remain separate observations. For genomic term b and chemical term m at named levels, the forward denominator is the sum of all chemical-term pair counts for b at that chemical level. Thus a multilabel chemical row contributes more than one denominator observation.

The synthetic table has b1 paired with m1 three times and m2 once; b2 pairs with m1 twice and m2 four times. The b1 forward scores are 3/4 and 1/4, independent of b2's counts. A known chemical term with an unobserved pair receives a valid empirical zero when b has a positive denominator for that ontology. That zero is not a negative biological label.

On the pinned production asset, `Polyketide` to `Polyketides` at `npc_pathway` has count 548 and forward denominator 722, giving `0.7590027700831025`. The reverse denominator would be 963. This kernel does not expose reverse scoring.

Two deliberate scorer deviations prevent a claim of full NPLinker equivalence. Named ontology lookup includes the first chemical level, whereas the inspected upstream truth-value test skips positional index zero. Unknown supplied vocabulary yields `input_unavailable`, whereas the inspected upstream scorer can return its zero fallback. The parser also rejects duplicate compound identifiers rather than silently overwriting earlier rows. Valid compound/multilabel counting and forward normalization follow the inspected source.

## Retrieve and verify the reference table

The machine-readable pin is `data/manifests/npclassscore-method.json`. Download only when needed, outside the tracked repository, and verify both byte size and SHA-256:

```powershell
$npclassAsset = Join-Path $env:TEMP 'MIBiG2.0_compounds_with_AS_BGC_CF_NPC_classes.txt'
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/NPLinker/nplinker/d01a68a4b0569907d7e28d1a673a82a6790b7346/prototype/nplinker/data/MIBiG2.0_compounds_with_AS_BGC_CF_NPC_classes.txt' -OutFile $npclassAsset
if ((Get-Item -LiteralPath $npclassAsset).Length -ne 732160) { throw 'Unexpected asset size' }
if ((Get-FileHash -LiteralPath $npclassAsset -Algorithm SHA256).Hash.ToLowerInvariant() -ne '96268b2e2d20e935976892e4f052c32592073a763cba85f33c7c654215b566ff') { throw 'Unexpected asset digest' }
```

The inspected upstream repository/code has an Apache-2.0 license. No separate notice for this bundled class asset was identified in this inspection. That does not establish rights for each underlying database record. The recipe avoids redistributing the asset; publication still needs the project's rights review.

## Verification and limits

Run `python -m unittest tests.test_npclassscore`. The first focused test was observed failing with `ModuleNotFoundError` before the production module was written. The passing tests use independent synthetic counts for direction, maximum selection, named first ontology, zero versus absent/unknown inputs, missing denominators, repeated compounds from one BGC, row/column/input reordering, hybrid and Alkaloid normalization, Cartesian chemical labels, malformed inputs, and duplicate compound identifiers. The separately run local production-asset smoke check loaded 2,112 compounds and reproduced 548/722 with the pinned digest. It is not a fungal benchmark validation.

The host also compared 47,419 count cells and 47,419 forward score cells across both supported genomic levels and all nine chemical levels against AST-extracted upstream source. All matched, with maximum absolute score difference 0.0. That check used `python -X utf8` and a pandas `dtype=float` compatibility bridge for the old source's missing-value handling; it was not a full NPLinker run. Explicit UTF-8 decoding in this kernel avoids the platform-dependent mojibake observed when the reference source used the Windows default encoding.

Requested implementation route: `gpt-6-astra`, reasoning `medium`. The parent reports the native route as Astra/medium; no serving-side receipt was exposed to this worker, so actual model/effort remain unverified here.

No predictor, spectral preprocessing, GCF construction, scientific label eligibility decision, benchmark run, learned model, or gold-derived annotation is included. Training/reference overlap with a future benchmark remains unknown and must be audited before interpreting its results.
