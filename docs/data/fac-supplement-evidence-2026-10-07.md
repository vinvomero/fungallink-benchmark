# FAC-MS supplement evidence inventory

The recovered supplement supports a concrete biological evidence review of **17 historical product rows from 15 FACs**. Supplementary Figure 2 has one panel for every product in article Table 1, with an MS1 spectrum, a selected-ion chromatogram, a corresponding deletion comparison, and published gene anchors. These are measured products, including unnamed products. None has been admitted to the benchmark by this inventory.

AtFAC9J20 carries three separately supported pathway candidates: benzomalvin A/D, an unnamed sesterterpenoid, and valactamide A. Counting FACs would merge those pathways. Counting every product row as an independent query would also be unjustified before sequence-based pathway grouping and review. The article's 56 screened FACs and 156-library FACs describe other populations, not accepted query counts.

The machine-readable inventory is [fac-supplement-evidence-2026-10-07.tsv](../../data/curated/fac-supplement-evidence-2026-10-07.tsv). Its 17 rows are source relationships, not a candidate molecule universe or an admission ledger.

## Sources and inspection

Source: Clevenger et al., *A Scalable Platform to Identify Fungal Secondary Metabolites and Their Gene Clusters*, DOI [10.1038/nchembio.2408](https://doi.org/10.1038/nchembio.2408), [PMC5577364](https://pmc.ncbi.nlm.nih.gov/articles/PMC5577364/), 2017. This review used retained files only:

- `data/raw/expression-dataset-screen-2026-10-07/fac-text.txt`: article text, especially Table 1, discovery/validation results, and AtFAC9J20 sequence analysis.
- `fac-supplement.pdf`: 43 pages, 19,775,222 bytes, SHA-256 `6ea1aa7dc34516cf8dcf4b0003b3a9798ab4569106d8f1027dc94f22bcde0d72`.
- `fac-supplement.txt` and `fac-supplement-retrieval.json`: extracted captions/tables and retrieval provenance. The retrieval record identifies the PMC Open Data supplement object.

All Figure 2 panels A-Q were visually inspected in rendered printed pages 3-12. Those renders and the small TSV-generation script are in `scratch/fac-supplement-evidence-2026-10-07/`. Later figure captions and Supplementary Table 2 were read from the extracted text; later image panels were not exhaustively re-reviewed. The canonical project plan and humanizer skill were read. The skill's referenced writing-guide file was absent; its main rules were applied.

## Product and locus anchors

The m/z column reproduces the Figure 2 `[M+H]+` label. It is not a remeasured value or a raw-file join. Gene identifiers reproduce the panel's deletion anchor. They do not establish sequence versions, complete BGC boundaries, or exact correspondence to an independently downloaded assembly.

| Source product | Base FAC | Panel / page | Deleted-gene anchor in panel | Reported m/z |
|---|---|---|---|---:|
| facms0001 | AaFAC6A16 | G / 6 | AACU_46595 | 403.202 |
| facms0002 | AaFAC2P8 | I / 7 | AACU_59515 | 559.234 |
| facms0003 | AaFAC10D7 | H / 6 | AACU_51108 | 274.036 |
| facms0004, benzomalvin A/D | AtFAC9J20 | A / 3 | benZ; benY and benX also mapped | 382.153 |
| facms0005, unnamed sesterterpenoid | AtFAC9J20 | B / 3 | sttA, ATEG_03568 | 369.277 |
| facms0006 | AtFAC5L7 | O / 11 | ATEG_07500 | 674.269 |
| facms0007 | AtFAC9H19 | D / 4 | ATEG_07067 | 610.925 |
| facms0008 | AtFAC5N15 | E / 5 | ATEG_07380 | 278.212 |
| facms0009 | AwFAC1H17 | N / 10 | ASPWE_085322 | 423.182 |
| facms0010 | AwFAC1K8 | J / 8 | ASPWE_027400 | 988.557 |
| facms0011 | AwFAC4D8 | M / 10 | ASPWE_044725 | 680.356 |
| facms0012 | AwFAC4E11 | K / 8 | ASPWE_034272 | 577.317 |
| facms0013 | AwFAC1B1 | Q / 12 | ASPWE_163793 | 472.209 |
| facms0014 | AwFAC3D3 | P / 12 | ASPWE_151732 | 736.205 |
| facms0015 | AwFAC4D17 | L / 9 | ASPWE_042597 | 542.386 |
| facms0016 | AtFAC7O19 | F / 5 | ATEG_07358 | 310.119 |
| facms0017, valactamide A | AtFAC9J20 | C / 4 | valB, ATEG_03576 | 507.416 |

The source strains are A. aculeatus ATCC 16872, A. wentii DTO 134E9, and A. terreus ATCC 20542. The article Table 1 lists facms0017 in an AtFAC9J20-ΔbenY background, while its supplement panel includes the AtFAC9J20 parent FAC trace. The TSV preserves both names.

AtFAC9J20 has a reported 102,722-bp fungal insert and a stable accession, **KX449366**, in the article. The host's retained `fac-locus-accession-summary.json`, inspected in this review, confirms **KX449366.1**, titled *Shuttle vector AtFAC9J20, complete sequence*, at **118,762 bp**, derived from A. terreus ATCC 20542. That length is the whole vector, not the fungal insert. No sequence was downloaded or validated here. Supplementary Table 2 maps its named genes and NIH2624 homologs; benX/benY/benZ lack those reference homologs. Thus sequence access is already anchored for the three AtFAC9J20 candidates, whereas the other 14 product rows have published gene anchors but no FAC sequence accession supplied by this packet. These statements do not assert that those sequences are unavailable elsewhere.

## Evidence strength and eligibility

Figure 2's caption reports genetic validation for all 17 products. Each inspected panel plots the product in its FAC background alongside the corresponding deletant and native parent strain. The article states that the assigned signal was eliminated in the validated cases. This is direct historical perturbation evidence for biological adjudication, stronger than a FAC-Score association alone. FAC-Score selected the original hits, so the resource also retains source-selection exposure: deletion support does not make selection blind.

The historical `facms` identifiers and their panels provide traceable measured-target anchors for a source-level label review. Missing a full abundance matrix does **not** erase that evidence or exclude unnamed products from biological eligibility. Admission still needs an explicit queried locus or GCF scope, scientific review of the source-to-query correspondence, and a declared resolution for the measured target. facms0006's gene-class conflict needs particular attention before locus-level adjudication.

Chemical identification varies. Benzomalvin A/D has synthetic-standard, MS/MS, and coinjection support in Supplementary Figure 5 (p.15). The two atropisomer peaks are not two independent benchmark successes. Valactamide A has MS/MS, NMR, and stereochemical evidence in Figures 11-19 (pp.21-26). facms0005 has formula and MS/MS support for a sesterterpenoid class in Figures 8-10 (pp.19-20), with no resolved exact structure. The remaining 14 Figure 2 products are unnamed in this census; Table 1 gives no formula for facms0007 or facms0010. Structure identification and biological link support remain separate.

Later supplement captions describe valactamides A-H, including deletion-associated disappearance and MS/MS comparisons (Figures 20-22, pp.27-29); only A has the stated NMR structure determination. Benzomalvins E/B and proposed intermediates also appear elsewhere in the article. These ancillary measurements were not added to the 17-row Figure 2 inventory. They need their own source-to-target review and must not inflate independent pathway counts.

## Source discrepancies retained

- **facms0006:** Table 1 says NRPS deletion and `Cryptic=No`. Figure 2O boxes gene e, ATEG_07500, annotated PKS; it shows a flat native-parent trace. A separate NRPS, ATEG_07488, is present in the diagram. The evidence packet does not silently replace one account with the other.
- **facms0008:** Table 1 says `Cryptic=Yes`; Figure 2E shows a native-parent peak. The FAC/deletant contrast remains visible, but native-expression status is unresolved.
- **facms0003:** Table 1 summarizes the deleted class as PKS, while Figure 2H annotates the boxed gene as NRPS/PKS. The hybrid annotation is retained.
- **facms0004:** the Table 1/panel formula differs from the neutral formula stated in the article text. The source fields are retained without a silent formula correction.
- **facms0005:** Figure 2, Figure 8, and Figure 9 contain different reported m/z values. Figure 9's 369.2710 differs from Figure 8's 369.2783. For this reason, no mass-only match is treated as a historical feature join. facms0009 also has a Table 1 mass versus panel m/z discrepancy worth resolving when the analytical input is reviewed.
- Several later captions print A. terreus `ATCC 20524`, whereas the article's library description and Supplementary Table 1 identify `ATCC 20542`. Source strain assignment follows that explicit library provenance; the transposition is retained as a source discrepancy, not an additional strain.

## Remaining inputs and bounded disposition

This is now a **label-rich acquisition candidate** for the comparative benchmark. Its direct evidence can be reviewed without waiting for spectra. The immediate input gap is a complete measured-feature candidate pool and its sample mapping, not a lack of biological validation.

No full historical feature matrix, complete candidate-ID universe, validated `facms`-to-feature mapping, or feature-to-MS/MS scan join has been recovered in this packet. The host's retained MassIVE check reports 12 raw files totaling about 6.7 GB under MSV000081097 and no attached reanalysis. That restricted listing does not establish coverage of the 56-FAC screen. It cannot stand in for the full cohort matrix or justify retrospective co-occurrence scores. No mass/retention-time match was made to those raw files here.

Reopening release readiness requires a defined complete feature pool with eligible-sample metadata and a validated mapping from these historical products to released feature IDs. Query readiness requires accession/version and boundary review, FAC-to-source-strain correspondence, and pathway grouping; KX449366 gives the most concrete starting point for three candidates. A spectral extension separately requires auditable scan/native identifiers or an equivalent validated export. None of these unresolved input fields is a biological negative label.

Keep the 17 candidate relationships in this evidence inventory for adjudication. Do not promote them into the canonical admission ledger, claim 17 independent queries, or call the source ready for the main comparison on the present inputs. No canonical plan, admission file, or repository history was changed by this unit.

Routing requested: `gpt-6-astra`, reasoning `medium`. The native subagent dispatch supplied that request; no serving-side receipt exposed the actual model or effort. Host verification checked all 17 Table 1 product/FAC/mass/deletion-class/cryptic fields against the retained article, the supplement hash, and source PDF pages 3 and 12 visually. It also checked KX449366.1 through NCBI metadata. Receipt: `data/raw/expression-dataset-screen-2026-10-07/fac-host-verification.json`. This is a transcription and limited visual check within the same session, not independent biological adjudication.
