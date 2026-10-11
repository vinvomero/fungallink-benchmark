# Phoenicin query reference review, 3 October 2026

The published phoenicin reference has direct experimental support, but this bounded check did not resolve it to an exact sequence-defined BGC query. A versioned genome for the named strain is public: [GCA_028826765.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_028826765.1/), assembly name ASM2882676v1, WGS master [JAPQKK000000000.1](https://www.ncbi.nlm.nih.gov/nuccore/JAPQKK000000000.1), and BioSample [SAMN30185301](https://www.ncbi.nlm.nih.gov/biosample/SAMN30185301). The missing link is a source-supported mapping from the paper's phoenicin gene names to particular sequence records and coordinates. No benchmark admission or target-feature decision was made here.

## What the retained sources establish

The [experimental reference paper](https://doi.org/10.1002/batt.202200365), retained as `data/raw/sources/expansion-2026-10-03/phoenicin/reference-paper.pdf`, identifies IBT 34669 on PDF page 8. PDF page 4 reports phoenicin loss after perturbing the named PhS1 locus. The accompanying cluster assignment is direct source evidence for this reference organism. It is not a new assignment inferred in this review from another species.

The [retained institutional thesis](https://backend.orbit.dtu.dk/ws/portalfiles/portal/310619224/Final_thesis.pdf), PDF page 201, reproduces Supplementary Figure 2. Panel a depicts the named phoenicin cluster; panel c shows loss of the phoenicin-associated signal in the altered strain. Visual inspection of the existing `reference-figure.png` confirms that the diagram uses PhS1 and numbered functional labels corresponding to the paper's PhS3, PhS4 and PhS5 names. It supplies neither locus tags nor accession numbers, genomic coordinates, sequence lengths, or a nucleotide scale. These are gene names and a proposed cluster membership, not a recoverable sequence interval.

The main paper and the thesis's reference-paper section and supplement were checked for accession, locus, scaffold and contig locators. None linked the named phoenicin genes to a public sequence record. The paper's data-availability statement on PDF page 11 directs requests to the corresponding author. Its genome-sequencing method citation is not an accession crosswalk. Complete mechanism reconstruction is unnecessary for the benchmark question and was not attempted.

## Versioned public metadata

On 3 October 2026, targeted NCBI Entrez requests returned the following records:

| Record | Observed content | Scope |
|---|---|---|
| JAPQKK000000000.1 | P. atrosanguineum strain IBT 34669; culture collection IBT:34669; PRJNA867151; SAMN30185301 | Direct strain metadata in the WGS record |
| JAPQKK01 | Ten component accessions, JAPQKK010000001 through JAPQKK010000010 | Versioned WGS project component range; the master itself is not a BGC sequence |
| GCA_028826765.1 | ASM2882676v1; contig-level assembly; linked SAMN30185301; annotation flags present | A recoverable genome resource, not a published phoenicin locus definition |

The culture identifier matches the reference paper. Treating this deposited assembly as the exact genome underlying the experimental assignment remains a correspondence based on that shared identifier; the reviewed paper does not explicitly cite this assembly. The WGS master cites the later comparative Penicillium genome study. Annotation availability does not establish that any annotation is the paper's PhS1.

A targeted Protein search, `(phoenicin[All Fields] OR PhS1[Gene Name]) AND Penicillium[Organism]`, returned zero IDs. This only records failure to resolve the locus under those names on that date. It does not establish absence of deposited sequences or rule out unnamed annotations. No whole genome, protein set or homologous pathway was downloaded or reconstructed.

## Disposition and reopening evidence

Keep the biological reference as experimentally supported and the sequence query as unresolved. The precise missing artifact is an author/source mapping of PhS1 and the intended cluster members to accession-versioned gene or protein records, or a contig accession and interval with a declared boundary convention. An annotated cluster record linked explicitly to this reference would also resolve the locator. Once such a mapping exists, a later curator can extract and checksum the sequence and state any boundary inference separately.

Do not replace the missing mapping with the whole-genome accession, the schematic's visual spacing, or pathway claims from the comparison organism. If a future sequence comparison supplies the mapping instead of a published cross-reference, label it as inferred and document its uncertainty. The current gap concerns executable locus input, not a demand for every biosynthetic step to be established.

The companion TSV separates the reference assignment, public metadata, sequence readiness and measured-target readiness. Feature 38 remains a candidate crosswalk under the separate target review; this report does not upgrade it.

## Audit trail

Raw responses and a filtered source-locator audit are in `scratch/phoenicin-query-reference/`. `receipts.json` records hashes of these files and the retained PDFs. Entrez calls used the `life-science-research:ncbi-entrez-skill` script. The humanizer skill was applied to this text; its optional referenced guide was absent at the installed path.

The parent task requested `gpt-6-astra` with `medium` reasoning. This worker has no serving-side receipt confirming its actual model or effort, so no actual-serving claim is made. No correspondence, public release, genomic engineering protocol extraction, benchmark admission or main-report edit occurred.
