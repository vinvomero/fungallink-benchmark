# Build source observations

`scripts/build_source_observations.py` implements the numeric transformation in
[the dated source-observation specification](../../protocol/caesar-source-observations-2026-10-02.md).
It accepts an annotation-free acquisition candidate bundle and the grouping ledger.
It creates no query, reference answer, ranking, biological identity, or genome linkage.

Run from the repository root with Python's standard library:

```powershell
python scripts/build_source_observations.py --source-dir data/processed/caesar-candidate-bundle-v1 --grouping-ledger data/curated/caesar-observation-groups-2026-10-02.tsv --output-dir data/processed/caesar-source-observations-v1
python -m unittest tests.test_build_source_observations tests.test_build_candidate_bundle
```

The Python entry point is `build(source_dir, grouping_ledger, output_dir)`. It returns
the output manifest. Input failures raise `ValueError`; the CLI reports them with
exit status 2. File access failures retain Python's ordinary exception behavior.

## Numeric rules

The condition height is the median of all acquisitions in the exact recorded
cohort/label/medium group. An even group uses the mean of its two middle values.
Decimal arithmetic preserves the supplied decimal values when calculating medians.
A height of 10,000,000 meets the detection rule. All candidates remain in every
matrix, including candidates below threshold everywhere. Zeros remain zero.

An empty acquisition value makes that feature's group median and group presence
missing. The label height is the maximum over its recorded media when all their
group medians are known. Otherwise the maximum is missing, since an unknown
condition could exceed the observed maximum. Label presence is still `1` if any
known condition reaches threshold. It is `0` only when all recorded conditions
are known and below threshold; otherwise it is missing. Missing output cells are
empty TSV fields.

The sampled-condition summary doesn't invent a measurement for an unrecorded
medium. `complete_media_roster` records whether a label has Cheerios, Oats, and
Rice, the fixed roster in this version of the specification. Blank and map-only
records contribute neither summaries nor condition opportunities.

## Files and keys

| Output | Contents |
|---|---|
| `candidates.tsv` | Every source candidate, with the existing annotation-free fields |
| `conditions.tsv` | One source observation per exact cohort/label/medium group, with acquisition membership |
| `labels.tsv` | Exact literal labels, recorded media, condition IDs, acquisition membership, and roster completeness |
| `condition-heights.tsv`, `condition-presence.tsv` | Candidate rows by condition observation columns |
| `label-heights.tsv`, `label-presence.tsv` | Candidate rows by literal-label observation columns |
| `grouping-ledger.tsv` | Byte-for-byte input ledger, including excluded records and source assertions |
| `manifest.json` | Rules, counts, input/output fingerprints, code fingerprints, Python version, and artifact readiness |

Matrix rows sort by candidate ID. Observation columns sort by their literal
cohort/label/medium keys. No trimming or alias repair occurs. IDs use `condition:`
or `label:` followed by the SHA-256 of a compact UTF-8 JSON array containing the
literal key parts. IDs therefore survive input reordering. Metadata acquisition
arrays sort by acquisition ID; the copied ledger retains the original array order
and corresponding source assertions.

The manifest records the source manifest and every consumed payload fingerprint,
the ledger fingerprint, and the builder and shared TSV helper fingerprints.
Repeating a build with identical inputs, code, and Python version produces the
same bytes. Reordering a ledger changes its copied bytes and provenance hash,
while the matrices and observation metadata remain unchanged.

## Checks and limits

The builder verifies source hashes, byte counts, row counts, candidate IDs,
dimensions, missing/zero cell counts, and finite nonnegative heights. The ledger
must partition every acquisition exactly once. Its measured-column membership,
array lengths, acquisition roles, cohort IDs, counts, exclusion reasons, and
candidate pool sizes must agree with the candidate bundle. An eligible source
group can't be silently excluded, and a blank or map-only record can't become
an eligible observation. Malformed or mismatched inputs stop the build.

These checks establish internal consistency. The candidate bundle intentionally
has no workbook label or medium fields, so the builder cannot independently
verify the ledger's literal label assignments against the original workbook.
The source review and the fingerprinted ledger provide that provenance.

Files are staged beside the destination, with a final input-change check before
publication. The manifest is published last. This follows the candidate builder's
pattern, not a transaction over the whole output directory: an interrupted
publication can leave payloads that fail the previous manifest's fingerprints.
Consumers must verify the manifest before using a bundle.

The builder holds the source payloads and parsed abundance rows in memory. Memory
use grows with the acquisition-by-candidate matrix; no disk-backed spool is
implemented. Run full builds and the full test suite sequentially when memory is
tight.

Raw-height summaries are unnormalized. This unit adds no normalization, blank
subtraction, imputation, feature filter, alternate detection method, sensitivity
analysis, scoring adapter, or scientific approval flow. The condition data and
roster flag preserve the inputs for the predeclared later checks. Output metadata
states that biological identity and genome-linked eligibility are unestablished;
analytical release and scoring readiness remain false. These artifact statements
don't change any separately recorded scientific label decision.

The synthetic tests use hand-calculated odd, even, and singleton medians; an
inclusive threshold boundary; missing and all-zero features; literal-label spacing;
partial and complete media rosters; blank/map-only controls; shuffled IDs; and
input-integrity failures. They prove software behavior, not biological validation.
