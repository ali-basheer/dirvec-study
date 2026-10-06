# The paper

- `main.tex`: the long version, the preprint (DOI 10.5281/zenodo.23178122). Figures in `figures/`, drawn by
  `scripts/figures.py` from the results files.
- `sigir/main.tex`: the short version in ACM format (anonymous review copy). Its two single-column
  figures are drawn by `scripts/figures.py --sigir`.

The bibliography is `../reports/citations_verified.bib`, referenced by relative path.

Build:

- `bash scripts/arxiv_pack.sh` builds `main.tex` with its bibliography, stages `main.tex`, the generated
  `main.bbl` and the figures, compiles the staged files alone as arXiv would, and writes the source
  package and the PDF to `build/arxiv/`.
- `bash scripts/sigir_build.sh` builds the short version in `build/sigir/` and runs
  `scripts/sigir_check.py`, which traces every number of it to the long version or to the results
  files and checks the page limit and anonymity.
- `python3 scripts/revcheck.py <git rev> results/*.md BRIEF.md` lists, for a revision of `main.tex`,
  the numbers it added and whether each occurs in the record.
