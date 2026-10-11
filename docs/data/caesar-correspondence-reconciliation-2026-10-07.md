# Caesar correspondence reconciliation

Checked 2026-10-07. Private working record; no correspondence sent. This corrects the proposed combined request and its assumption that the genome-label bridge still needed to be requested.

The evidence checked here consists of retained correspondence logs and an attachment audit, not a newly retrieved original email thread.

| Question | Existing answer | Disposition |
|---|---|---|
| FMGX/UNCG identifiers to strains | The September 19 reply audit records `first paper strains.xlsx`, 146 data rows, SHA-256 `2f5be40cc9c1355f7dc4df062e5a93001dc9c351900fffc7e9f9d41bffc3d5b7`. The author described it as old and possibly incomplete. It has strain names but no assembly-accession column. The retained reconciliation joins 108 workbook rows to tracked strain records and 126 of 131 representative GCF members to assemblies. | Remove the generic request. We possess and already use the derived bridge. Whether a public copy exists is a separate provenance question, not missing research input. |
| Sample-to-strain table | August 31 contact log records that the supplement provides strain/accession identities but she had no metabolomics sample map to supply. Vin returned the project's reconciled CSV/TSV on September 1. | Do not request the same table again. |
| Ambiguous sample labels | The log records NIH2624 correction, ATCC 96836 and W1 identities, and species spelling corrections. | Reuse the recorded answers. |
| Were all study strains represented? | The initial August 31 statement that all were run was qualified by September 2 follow-up: A. tanneri appeared absent from the deposit; the starting population had been reduced at different stages. | Preserve the later qualification. Running a strain does not establish that its files were deposited. |
| Representative GCF selection | September reply audit records manual selection based on the component judged to define/initiate the scaffold when one BGC entered multiple categories. | Already answered at procedural level; no new general question. |
| Five denominator exclusions | Author did not recall the rule. A possible duplicate was only a vague recollection. | Record as not recalled; do not repeat as though unanswered correspondence were pending. |
| Six unmatched ATCC48694/NRRL1061 workbook acquisitions | No answer specific to these six filenames was found in the records inspected. General population history does not identify them. | Provisional narrow residual only. Do not claim outreach is necessary or that the data do not exist. |
| FAC-MS full feature tables and construct/sample map | Not answered in the Caesar records inspected. | Separate study-specific residual; not resolved by this check. |

Sources inspected read-only:

- `../terralabv2/docs/governance/2026-08-29-depositor-contact-log.md`: August 31 and September 2 responses and September 1 map return.
- `../fungallink/docs/governance/2026-08-29-depositor-contact-log.md`: stale copy still reporting no reply; must not govern current status.
- `../fungallink/docs/research/evidence/caesar-author-response-2026-09-19.json`: source answers and attachment provenance.
- `../fungallink/configs/caesar_evidence_sources.json`: workbook hash and source description.
- `../fungallink/output/caesar-response-2026-09-20/reconcile-report.txt`: historical join counts above; these are mapping counts, not admitted benchmark relationships.
- `data/raw/sources/caesar-2023/historical-label-strain-assembly-crosswalk-2026-09-20.tsv`: existing v2 import.

Follow-up attachment verification: both maps in the retained September 1 sent record match the v2 source-manifest hashes and byte lengths exactly. They are project-generated reconciliations incorporating Caesar's answers and marked inferences. See [source provenance addendum](../release/source-provenance-addendum-2026-10-07.md) for full hashes and paths. Their origin is no longer unidentified.

No labels, benchmark counts, or frozen inputs changed. Nothing was sent. The previous draft overstated the need for another genome-label request because it failed to distinguish existing privately supplied evidence from public retrieval provenance.
