# Trichoderma ilicicolin appraisal

Date: 2026-10-07. Curator: automated CE Work evidence unit; no human or independent scientific validation claimed. Requested route: gpt-6-astra / medium; actual serving model and effort unverified. Canonical benchmark plan read before curation. This is a source appraisal, not admission to a release.

Burger et al. (2025), DOI [10.1186/s13068-025-02628-3](https://doi.org/10.1186/s13068-025-02628-3), supports a defensible biological link between the QM6a ilicicolin locus and ilicicolin H. It does not yet supply a release-ready sequence-to-feature chain. Two gaps remain: the supplied Trichoderma sequence is labeled RUT C-30, while experimental samples are QM6a derivatives; and the exact chemically supported product must be joined to the deposited feature export.

Ilicicolin K warrants a separate, provisional relationship row. Do not turn H and K into two independent pathway queries.

## Biological and chemical evidence

For H, article Fig. 2C-D compares QM6a derivatives: activated OETriliR, triliA deletion in that background, triliE deletion in that background, and the study's wildtype control. H disappears following triliA deletion. The source matched H mass, retention time, and collision cross section to an authentic standard. Its isolated H is also covered by supplementary Table S6 and NMR Figures S13-S14. This is direct native-host perturbation evidence for the QM6a locus, not merely a molecular-network inference. The source's wildtype is QM6a Δmus53, rather than an unmodified field isolate (Table 2).

The paper separates H (compound 1, RT 5.84 min) from 8-epi-H (compound 2, 6.31 min) and bis-diene (compound 3, 6.57 min). These compounds share a formula and similar fragmentation. Do not merge them by mass or spectral similarity. Another same-mass compound elutes at 8.23 min; that compound is not K.

K is an isolated, measured derivative with formula C27H29NO5 and a proposed structure supported by NMR and fragmentation (article Figs. 4-5; supplement S8-S10, Table S7, Figs. S15-S16). Supplement S8 explicitly qualifies the ether linkage: its direct NMR proof was unavailable, and the assignment rests on shifts and the combined spectra. S8 was rendered and visually inspected; its text and structure agree. This uncertainty should remain visible even though the article describes K as structurally elucidated.

The K-like network nodes have m/z about 448.2117 and IDs 5, 6, and 9. The paper calls ID 9 a redundant feature-detection artifact. It does not establish, in the inspected prose or supplement, which of IDs 5 and 6 corresponds to the isolated K structure. Neither shared formula nor network proximity resolves that choice. The paper establishes K recovery in the activated-host study, but the explicit triliA knockout result presented for H must not be silently extended to an exact K feature or to an enzyme-complete K pathway.

## Sequence and strain scope

Supplementary file 4 parses as GenBank KI911142.1, length 30,604 nt, with eight CDS records. Its definition and SOURCE feature specify **Trichoderma reesei RUT C-30**. Sequence SHA-256: `759c315a5e2a32176fd1ca1d4ef261f70c2b55af4c143dfe82a2b91e4bef5d62`. It contains only A/C/G/T bases. The excerpt retains the parent scaffold accession, but the retrieved record does not state the original scaffold offset. Its local coordinates must not be presented as full-scaffold coordinates.

Article Fig. 1 describes a QM6a comparison; Table 1 supplies QM6a/RutC30 protein aliases. Table 2 establishes QM6a derivative experiments. These source statements do not settle whether the provided RUT C-30 sequence matches the measured QM6a locus. The file's eight CDSs carry protein IDs ETS03591.1 through ETS03598.1, but the appraisal does not invent gene assignments from their order.

The other supplied GBKs are Neonectria sp. DH2 RQWH01000002.1 (52,165 nt, antiSMASH 7.1.0 metadata) and Talaromyces variabilis HXQ-H-1 MK539848.1 (31,370 nt). They are comparison sequences, not additional independently measured genomes in this cohort. The TriliR FASTA contains alternative gene models, not a complete experimentally matched QM6a cluster.

Exact lookup anchors from article Table 1 follow. These are JGI protein IDs, not assembly accessions or independently verified sequence equivalences.

| Gene | QM6a JGI ID | RutC30 JGI ID |
|---|---|---|
| triliA | 58285 | 128011 |
| triliB | 58289 | 74247 |
| triliC | 58953 | 33667 |
| triliD | not provided | 75073 |
| triliE | 76204 | 96728 |
| triliR | 72993 | 74475 |

The article also names QM6a chromosome-level TriliR model 110738 (787 aa), in contrast with older QM6a model 72993 (462 aa). No complete QM6a BGC accession/boundary is supplied in the inspected article text. Supplied KI911142.1 local CDS spans, in GenBank 1-based closed coordinates, are ETS03591.1: 1..1189 (+); ETS03592.1: 3148..4176 (+); ETS03593.1: 4521..16676 (-); ETS03594.1: 18525..19667 (+); ETS03595.1: 20161..21597 (-); ETS03596.1: 22943..23928 (-); ETS03597.1: 24630..26326 (+); ETS03598.1: 28241..30604 (-). The uppercase SOURCE feature covers 4521..30604, and is not an original-scaffold offset declaration.

To reopen sequence readiness, retrieve the versioned QM6a locus and demonstrate correspondence to the supplied sequence or define a QM6a query directly, with boundaries, full gene content, and competing-locus checks. If the RUT C-30 locus is used instead, classify the relationship as reference-supported only after a documented transfer assessment. Do not call that locus directly tested by this study.

## Measurement and method readiness

The companion acquisition unit owns MSV000095813 exports and sample mapping. This unit downloaded no MassIVE data. Article-derived feature IDs are network-local identifiers until verified against that export. Required joins are: H compound 1 to its source feature row and, for spectral evaluation, exported spectrum/native identifier; K isolate to exactly one supported source feature or an explicitly justified ambiguous target set; sample names to QM6a derivative genotypes.

Companion result: the complete inspected deposit contains 18 Bruker raw acquisitions (about 2.732 GB), the MZmine batch, and parameters; no processed CSV, MGF, or GraphML export was found. Its attached-reanalysis list was empty. Local output paths in the batch do not establish deposited contents. Neither H nor K has a recovered native feature join. Closing this gap requires a recovered source export or a separately versioned reprocessing release followed by chemical reassignment; do not carry article network IDs into newly processed rows.

One parental genetic background, several perturbations, and four biological replicates per condition do not create several independent genomes. The source can support a locus-to-measured-feature case; it cannot by itself provide an independent-strain co-occurrence evaluation. Keep culture/condition observations separate from independent genome counts.

The full unfiltered deposited feature universe, preprocessing version, and sample eligibility must be frozen before comparison. MZmine 4.0.3 and Skyline 22.2 are source processing versions, not benchmark method versions. Gold annotations must not become method inputs. Exposure is retrospective/public: H pathway literature predates this paper, and K was public in 2025; training or database overlap remains method-specific and unverified.

## Saved evidence and disposition

Raw files, extracted text, sequence inspection, and SHA-256/byte provenance are in `data/raw/trichoderma-evidence-2026-10-07/`. Article XML came from Europe PMC because the direct publisher HTML request returned a browser challenge. That challenge is preserved under an explicit filename and is not treated as article content. The article is CC BY 4.0; the publisher's supplementary material is linked from its article. Supplementary file 3 (RT-qPCR workbook) was not required for this bounded appraisal and was not downloaded.

H: strong biological evidence, chemistry resolved at source, query-to-sampled-locus correspondence unresolved, measured feature join delegated. K: measured chemistry with a documented bond-assignment caveat, exact locus-product support and native feature resolution incomplete. Zero relationships are admitted here. Stop this source review after the recorded joins; do not repeat the article or supplement inspection unless a new source resolves them.
