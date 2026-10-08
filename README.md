# dirvec: a pre-registered measurement of pooled directory embeddings

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23178122.svg)](https://doi.org/10.5281/zenodo.23178122)
[![Preprint: not peer reviewed](https://img.shields.io/badge/preprint-not%20peer%20reviewed-lightgrey)](https://www.craftpine.com/dirvec)
[![ORCID 0009-0006-2396-9932](https://img.shields.io/badge/ORCID-0009--0006--2396--9932-a6ce39)](https://orcid.org/0009-0006-2396-9932)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
[![Paper, briefs, results, data: CC BY 4.0](https://img.shields.io/badge/paper%2C%20data-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

Code, data manifests, pre-registration briefs and results for the study *A few vectors for a mixed
folder: a pre-registered measurement of pooled directory embeddings* (Ali Basheer, 2026).

Paper (preprint, not peer reviewed): https://doi.org/10.5281/zenodo.23178122, also at
https://www.craftpine.com/dirvec. The PDF published there has SHA-256
`8bef21aed187c640b44ebeb35f17b89704fc0df508e0e21186e8dbb82a9d5068`.

The study asks when the mean of a folder's file embeddings is enough and what it loses when the
folder mixes images and texts. It measures this on Zenodo record folders, on directories of public
GitHub repositories and on queries that a language model wrote as a simulated searcher, under four
encoders, and tests what a folder's few kilobytes of metadata can keep instead. Every test was written
into a brief with its criterion before the numbers that decide it were computed.

## Key results

Quoted from the paper's abstract. Recall@5 is the fraction of queries whose folder is ranked in the
top five; the paper reports it with 95 percent paired bootstrap intervals. The main vision-language
embedder is jina-embeddings-v4. The paper gives the definitions and the per-cell tables.

- Under the main vision-language embedder, the mean does at least as well as a few representatives on
  GitHub directories that do not mix media, about 95 percent of those eligible. Representatives for
  mixed folders only are level with the mean over all directories (both post hoc).
- Where a folder mixes images and texts, **the mean loses its minority modality**. On Zenodo record
  folders a held-out minority file finds its folder 0.16 to 0.25 recall@5 less often with the mean
  than with a few per-modality representatives under two vision-language embedders, and 0.35 to 0.50
  less often under two CLIP-family dual towers.
- On those folders, four representatives per label are not inferior to searching every file, at a
  0.02 margin, over all queries and in every cell under all four encoders (post hoc).
- On queries that a language model wrote as a simulated searcher, the loss under the main embedder is
  0.14 (interval 0.02 to 0.28) for pictures in text-heavy folders and 0.42 (0.28 to 0.56) for
  documents in image-heavy ones.
- At three per label every folder's representatives fit in **8 KiB** at a further cost of at most
  0.012 in any cell. In 2 KiB a per-kind sample of the folder's files keeps the minority files the
  mean loses, and on ext4 a summary of 2,048 or 4,000 bytes costs 1.2 blocks per cold directory read.

Encoders: jina-embeddings-v4 and gme-Qwen2-VL-2B-Instruct (vision-language embedders), jina-clip-v2
and Nomic Embed v1.5 (CLIP-family dual towers).

## Layout

- `BRIEF.md`: the pre-registration briefs, one section per session, each committed before the numbers
  it decides. `prereg/` holds the OpenTimestamps proofs for the commits of the briefs of sessions 19,
  21, 23, 24 and 27, and the git objects of those commits.
- `results/`: one results file per session with its verdicts, readings and deviations, and the
  verbatim outputs of each run.
- `data/`: manifests (paths, hashes, licences, source URLs), selections, ground truth and per-query
  ranks. The files themselves are not redistributed. `scripts/fetch.py` (Zenodo) and
  `scripts/fetch_gh.py` (GitHub) rebuild the corpora from the manifests.
- `scripts/`: embedding (`embed.py`), evaluation (`eval.py`, and `indep_eval.py`, a second
  implementation written from a specification), the session scripts (`sNN.py`) and the drivers that
  ran them (`sNN_run.sh`).
- `paper/`: the long version (`main.tex`, the arXiv version) and the short version (`sigir/main.tex`).
- `reports/citations_verified.bib`: the bibliography. `citations_verified.md` records how each entry
  was checked.

Each results file records its session as it ran. Where a later session or the paper revises a
reading, the later text governs. Sessions 25 and 26 list the readings they changed.

This repository is the release of the study: the final state of its working repository, without the
history. Commit identifiers in `results/` refer to the working repository, which is available on
request. `python3 scripts/verify_prereg.py` checks each timestamped commit from its git objects and
compares the brief it holds with `BRIEF.md`. The proofs are complete: each holds the Bitcoin block
that anchors it (blocks 969925 to 970090, 5 October 2026). `ots verify prereg/session19_commit.txt.ots`
checks a proof against a Bitcoin node, and the Merkle root that `ots info` prints for each block can
be compared with a block explorer's.

## Reproducing

- `python3 scripts/s27.py report data/s27_s11_*.npz data/s27seeds_*.npz data/s27_s24_e1.npz` and
  `python3 scripts/s27.py human-report data/s27_human_*.npz` rebuild the outputs of session 27 from its
  per-query files, `python3 scripts/s26.py report data/s26_*.npz` those of session 26 and
  `python3 scripts/s25.py` those of session 25. None of them needs a vector.
- Embedding needs a GPU: `scripts/embed.py` with a manifest, then `scripts/eval.py`. The drivers in
  `scripts/` give the exact command lines of every run.
- `bash scripts/arxiv_pack.sh` builds the long version, and `bash scripts/sigir_build.sh` builds the
  short one and checks every number of it against the results files.

## Cite

If you use this code, data or results, please cite the paper. GitHub's "Cite this repository" button
reads [`CITATION.cff`](CITATION.cff).

> Basheer, A. (2026). *A few vectors for a mixed folder: a pre-registered measurement of pooled
> directory embeddings* (Version 1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.23178122

```bibtex
@misc{basheer2026fewvectors,
  author       = {Basheer, Ali},
  title        = {A few vectors for a mixed folder: a pre-registered measurement of pooled directory embeddings},
  year         = {2026},
  month        = oct,
  publisher    = {Zenodo},
  version      = {1},
  doi          = {10.5281/zenodo.23178122},
  url          = {https://doi.org/10.5281/zenodo.23178122},
  note         = {Preprint, not peer reviewed. Code and data: https://github.com/ali-basheer/dirvec-study}
}
```

The DOI above identifies version 1. The concept DOI
[10.5281/zenodo.23178121](https://doi.org/10.5281/zenodo.23178121) stands for all versions and
resolves to the latest one.

## License

- **Code** (`scripts/`): MIT License, see [`LICENSE`](LICENSE).
- **Paper, briefs, results and data manifests** (the LaTeX source and figures in `paper/`,
  `BRIEF.md`, `prereg/`, `results/`, `reports/` and the files in `data/`):
  [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
  The full licence text is in [`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt).
- **Excluded.** `paper/plainnat-nonote.bst` is a modified copy of `plainnat.bst` (natbib,
  P. W. Daly) and stays under the LaTeX Project Public License. The corpora are not redistributed;
  each file's own licence and source URL are listed in the manifests in `data/`. Text and metadata
  that `data/` reproduces from Zenodo records and GitHub repositories (titles, descriptions, file
  paths, repository names and commit messages) remain under the terms of their sources.

## Use of AI

AI assistants (Claude, Anthropic; Gemini, Google) were used throughout this work, for writing,
coding, analysis and review. Models also produced study materials. Qwen3-VL-8B-Instruct wrote the
image captions and folder abstracts, Pixtral-12B wrote the image descriptions used as queries, and
Claude Opus 5.5 wrote the queries of session 27 as a simulated searcher that was told nothing about the
study. No person wrote queries for the study. The author conceived and directed the study and takes
full responsibility for its content.

## Keywords

directory embeddings · folder embeddings · pooled embeddings · mean pooling · modality gap ·
mixed-modality retrieval · vision-language embeddings · CLIP · collection representation ·
federated search · directory retrieval · semantic file systems · extended attributes ·
pre-registration
