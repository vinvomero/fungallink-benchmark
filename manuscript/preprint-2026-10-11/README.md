# LaTeX preprint edition

The main article is `Manuscript.pdf`. Supporting files are `Supplementary-Methods.pdf` and `Comparative-results.pdf`. Each has its corresponding editable `.tex` source. The vector figures and verified bibliography are included. Numbers, labels and comparisons retain the fact-checked scientific edition; public availability statements reflect the verified 11 October release.

Compile from this directory with Tectonic 0.17.0:

```sh
tectonic Manuscript.tex
tectonic Supplementary-Methods.tex
tectonic Comparative-results.tex
```

The source was generated with Pandoc 3.12.1 and then typeset with Tectonic. The `.tex` files are sufficient for compilation with their included figure assets. Tectonic retrieves its TeX support bundle on first use. No scientific analysis is rerun. `references.bib` preserves the verified bibliography; the `.tex` references are embedded so a separate bibliography tool is unnecessary.

This is an author-prepared preprint edition, not a Nature typeset article or a record of bioRxiv posting. Public data/code are available; a repository DOI, final author scientific review and journal/preprint-server submission are separate.
