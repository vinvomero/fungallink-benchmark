# Lichen measurement recovery, 3 October 2026

No measurement matrix, spectrum export, or verified GNPS/MassIVE accession was recovered for [Singh et al., DOI 10.1099/mgen.0.001569](https://doi.org/10.1099/mgen.0.001569). This closes the present public-record lookup with a specific missing dependency. It does not establish that the data are absent from every public service.

The existing acquisition report, expansion census, retained article XML, Zenodo metadata and voucher table were read first. Their successful downloads were reused. The canonical benchmark plan remains unchanged, and no labels were admitted.

## What this pass added

The [GNPS public dataset catalog](https://gnps.ucsd.edu/ProteoSAFe/datasets_json.jsp) returned 20,313 records. A case-insensitive search across serialized metadata found 46 records containing `lichen`; none contained `maonian`, `garima`, `001569`, `20231007`, or `olafsd`. All 109 source acquisition stems begin with `20231007`. Five `medema` records and one `zdouc` record concerned other studies. These are catalog-field results, not searches inside every deposited raw file or every public GNPS analysis task.

One plausible adjacent record deserved a file-list check: [MSV000093729](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=fbeb6b30f7a1409d82bee27fbe6ea0af), uploaded under `yux_OSU1`, describes cyanolichens collected in the northwestern United States. Its listing contains 87 files and no exact stem match to the source's 109 acquisitions. Its catalog lists an Agilent 6545 instrument. No same-voucher relationship was established. It cannot replace the requested cohort merely because its uploader appears associated with a coauthor.

The [earlier preprint](https://www.researchsquare.com/article/rs-6073935/v1) was downloaded and its text inspected. It describes GNPS networking but its availability statement points to the article and supplements without supplying an accession. Its six supplementary filenames include an S6 workbook, consistent with the published voucher metadata; these preprint supplements were not downloaded again.

A GitHub repository search for `lichen omics` returned two repositories. The coauthor's [Lichenomics repository](https://github.com/dapizarro/Lichenomics) contains workflow documentation and tables named as examples. Its tree, main README and metabolomics README supplied no study-specific accession. Example tables were not accepted as study measurements.

The [PODP project-summary endpoint](https://pairedomicsdata.bioinformatics.nl/api/projects) returned 81 summaries. No summary matched `lichen`, `maonian`, `001569` or `garima`. This limited result cannot rule out lichen records whose organism details occur only inside a project. The parallel PODP census did find the older KoLRI deposit MSV000084781 through those details. That is a separate cohort, not a recovered accession for this paper; acquisition and curation of it belong to the PODP lane.

Targeted web searches used the DOI, PMCID, paper title, author names, GNPS/MassIVE terms and acquisition-date stem. They located the preprint and author repository but no verified measurement accession. Search-engine omissions are not evidence of nonexistence.

## Metadata distinction

Rechecking the retained [source voucher table](https://www.ebi.ac.uk/biostudies/files/S-EPMC12711211/mgen-11-01569-s002.xlsx) found 109 unique acquisition stems, 108 sample IDs, 107 exact voucher strings and 78 species strings. `PSU3` occurs twice. `IT_MtLim_ParmeliaSp_2 (AMNH)` occurs in three acquisitions. These counts do not establish independent genomes or resolve whether the repetition is technical, biological or a transcription issue. Preserve all original rows until the measurement and voucher crosswalk can resolve it.

Atranorin retains the experimental reference evidence documented in the earlier census. Its expansion-cohort locus, measured target and voucher correspondence remain unresolved. Missing MS/MS is also a method-input issue, separate from those biological-label gaps. The prospective candidate universe and method exposure remain unfrozen.

## Recorded boundary

The next useful evidence is a specific public GNPS task, MassIVE accession, or author-supplied public file locator that resolves to the 109 acquisition names and their voucher map. Repeating the same title searches will not create that connection. No authors were contacted.

The [decision TSV](../../data/curated/lichen-measurement-recovery-2026-10-03.tsv) contains eight scoped findings. New catalog responses, repository records, preprint PDF/text, adjacent file listing, numerical audit and SHA-256 inventory are under `data/interim/lichen-measurement-recovery/`. The catalog is retained as search evidence, not measurement input. Existing source provenance remains in `data/manifests/new-cohort-discovery-2026-10-03.tsv`.

Requested route: gpt-6-astra with medium reasoning. No serving receipt was exposed, so actual model and effort remain unverified. Humanizer rules were applied; its referenced extended guide is absent from the installed package. The Life Science Research PMC skill was read; no redundant PMC availability request was made because the full article was already retained. This was agent-led acquisition review, not independent scientific validation.
