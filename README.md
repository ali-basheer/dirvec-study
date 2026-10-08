# A few vectors for a mixed folder

A pre-registered measurement of what one mean embedding loses when it stands for a folder that mixes
images and texts, and of what a folder's few kilobytes of metadata can store instead.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23178122.svg)](https://doi.org/10.5281/zenodo.23178122)

## Paper

- **Title:** A few vectors for a mixed folder: a pre-registered measurement of pooled directory
  embeddings
- **Author:** Ali Basheer, Craftpine Inc., Toronto
  ([ORCID 0009-0006-2396-9932](https://orcid.org/0009-0006-2396-9932))
- **Status:** preprint, version 1, published 6 October 2026. Not peer reviewed.
- **DOI:** [10.5281/zenodo.23178122](https://doi.org/10.5281/zenodo.23178122)
- **Zenodo:** https://zenodo.org/records/23178122

This repository holds the study's code, data manifests, pre-registration briefs and results. The
paper is also at https://www.craftpine.com/dirvec. The PDF published there has SHA-256
`8bef21aed187c640b44ebeb35f17b89704fc0df508e0e21186e8dbb82a9d5068`.

## Abstract

A folder's metadata is read before its files and holds a few kilobytes. A vector stored there can
route a query without opening the folder, and the cheapest is the mean of its files' embeddings. We
ask when the mean is enough and what to store when it is not. Under our main vision-language
embedder, the mean does at least as well as a few representatives on GitHub directories that do not
mix media, about 95 percent of those eligible. Representatives for mixed folders only are level with
the mean over all directories (both post hoc). Where a folder mixes images and texts, the mean loses
its minority modality. On Zenodo record folders a held-out minority file finds its folder 0.16 to
0.25 recall@5 less often with the mean than with a few per-modality representatives under two
vision-language embedders, and 0.35 to 0.50 less often under two CLIP-family dual towers. There,
four representatives per label are not inferior to searching every file, at a 0.02 margin, over all
queries and in every cell under all four encoders (post hoc). On queries that a language model wrote
as a simulated searcher, the loss under the main embedder is 0.14 (interval 0.02 to 0.28) for
pictures in text-heavy folders and 0.42 (0.28 to 0.56) for documents in image-heavy ones. At three
per label every folder's representatives fit in 8 KiB at a further cost of at most 0.012 in any
cell. In 2 KiB a per-kind sample of the folder's files keeps the minority files the mean loses, and
on ext4 a summary of 2,048 or 4,000 bytes costs 1.2 blocks per cold directory read. With every
creator weighted equally the main embedder's file-query loss is 0.13 and 0.14, and 0.06 and 0.12 on
queries whose names do not give the folder away. Every hypothesis was fixed in a brief before its
test. Five briefs are timestamped externally, the rest dated by the working repository's history.
Code, manifests and briefs are released.

## Research question

The study asks when the mean of a folder's file embeddings is enough and what it loses when the
folder mixes images and texts. It measures this on Zenodo record folders, on directories of public
GitHub repositories and on queries that a language model wrote as a simulated searcher, under four
encoders, and tests what a folder's few kilobytes of metadata can keep instead. Every test was written
into a brief with its criterion before the numbers that decide it were computed. The paper splits
the question into the seven listed under [Results](#results).

## Key findings

For folders that do not mix media, the mean is enough. Mixed directories are 4 to 5 percent of
eligible GitHub directories, and on the others the mean does at least as well as a few
representatives under the main vision-language embedder (post hoc). Where a folder mixes images and
texts, the mean loses its minority modality. On Zenodo record folders a held-out minority file finds
its folder 0.16 to 0.25 recall@5 less often with the mean than with a few per-modality
representatives under two vision-language embedders, and 0.35 to 0.50 less often under two
CLIP-family dual towers. On those folders four representatives per label are not inferior to
searching every file, at a 0.02 margin, over all queries and in every cell under all four encoders
(post hoc). At three per label every folder's representatives fit in 8 KiB at a further cost of at
most 0.012 in any cell. The loss also shows on queries that a language model wrote as a simulated
searcher. "Post hoc" marks what the paper marks post hoc.

## Where it applies

The paper's discussion gives a rule for any system that keeps one vector per folder, collection or
source and routes queries on it, such as a source router for retrieval-augmented generation (one
router the paper cites takes each source's centroid as an input), an agent's directory-shaped memory
or a folder-level file search. Where a folder does not mix images with other files, keep the mean.
Where it does, keep a few representatives per kind. A file system tells the two apart by file type
without embedding anything. At the scale measured, a folder layer bought nothing over a flat HNSW
index. The paper evaluated none of these systems, and its folders are Zenodo records and GitHub
directories; personal working directories, mailboxes and agent memories were not measured.

## Method

- **Datasets.** Four disjoint draws of Zenodo record folders: S1 (400-directory pilot), S3
  (400-directory pre-registered retest), S5 (main set, 2,808 records) and S11 (confirmation set,
  2,597 records). Two draws of directories of public GitHub repositories: S19 (1,600 directories of
  1,079 repositories) and S24 (2,600 directories of 1,885 repositories), with owners as the
  independent unit. Session 23 walks 261 whole repository trees.
- **Folders.** Zenodo records of 3 to 60 files that hold both an image type and a document type,
  under a CC0 or CC-BY licence, 2017 to 2026. GitHub directories with 3 to 100 kept files, from
  non-fork repositories with at least five stars and one of nine permissive licences.
- **Modalities.** Five kinds of file (image, PDF, text, table, office document), labelled image,
  pdf_text, pdf_scanned, text, table and other. Images are mostly scientific figures.
- **Models.** E1 jina-embeddings-v4 (the main vision-language embedder, 2,048 dimensions); E2
  jina-clip-v2 (CLIP-family dual tower, 1,024); E3 gme-Qwen2-VL-2B-Instruct (vision-language
  embedder, 1,536); E4 Nomic Embed v1.5 (CLIP-family dual tower, 768).
- **Embeddings.** One vector per file. Images are read as images; text, tables, text PDFs and office
  documents give their first 2,000 tokens of extracted text; a scanned PDF gives the mean of the
  vectors of its first eight page renders.
- **Pooling and representations.** Built leave-one-out and scored by the maximum cosine over a
  folder's vectors: the pooled centroid (the mean of the folder's file vectors); one centroid per
  modality label; per-modality k-means with up to three representatives per label; and every file
  vector, the flat file-level reference. Centered variants subtract each input group's mean first.
- **Retrieval evaluation.** Directory retrieval: a held-out file is a simulated known-item query and
  its own folder is the one relevant item. Recall@5, read by cell (minority and majority modality),
  with 95 percent paired bootstrap intervals from 1,000 resamples of directories on the Zenodo sets
  and percentile intervals from 10,000 resamples of owners on GitHub.
  Further queries: record titles and descriptions, commit subjects, and queries a language model
  wrote as a simulated searcher.
- **Pre-registration.** 27 sessions, each with a brief written before it. Twenty-two tested a
  hypothesis whose kill criterion was fixed in the brief before the numbers that decide it were
  computed. The briefs of sessions 19, 21, 23, 24 and 27 are timestamped with OpenTimestamps;
  the others are dated by the working repository's history. Analyses added after review are marked
  post hoc, and hypotheses that died or stayed inconclusive are reported.

## Reproducibility

### Layout

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

### Integrity and verification

The SHA-256 of the published PDF is given under [Paper](#paper) above.

This repository is the release of the study: the final state of its working repository, without the
history. Commit identifiers in `results/` refer to the working repository, which is available on
request. `python3 scripts/verify_prereg.py` checks each timestamped commit from its git objects and
compares the brief it holds with `BRIEF.md`. The proofs are complete: each holds the Bitcoin block
that anchors it (blocks 969925 to 970090, 5 October 2026). `ots verify prereg/session19_commit.txt.ots`
checks a proof against a Bitcoin node, and the Merkle root that `ots info` prints for each block can
be compared with a block explorer's.

### Reproducing

- `python3 scripts/s27.py report data/s27_s11_*.npz data/s27seeds_*.npz data/s27_s24_e1.npz` and
  `python3 scripts/s27.py human-report data/s27_human_*.npz` rebuild the outputs of session 27 from its
  per-query files, `python3 scripts/s26.py report data/s26_*.npz` those of session 26 and
  `python3 scripts/s25.py` those of session 25. None of them needs a vector.
- Embedding needs a GPU: `scripts/embed.py` with a manifest, then `scripts/eval.py`. The drivers in
  `scripts/` give the exact command lines of every run.
- `bash scripts/arxiv_pack.sh` builds the long version, and `bash scripts/sigir_build.sh` builds the
  short one and checks every number of it against the results files.

## Results

The paper's answers to its questions. Every pre-registered hypothesis and its verdict is
listed in the paper's appendix, and each session's results file in `results/` gives its full tables,
readings and deviations.

- **When is the mean enough?** On GitHub directories that do not mix media, about 95 percent of
  those eligible, the mean does at least as well as a few representatives under E1 (post hoc). Keeping
  representatives only for folders that hold an image and another file keeps most of the minority
  gain and is level with the mean over all directories at the natural mix (post hoc).
- **What does the mean lose in a mixed folder?** Under E1 the loss is 0.17
  to 0.25 recall@5 across the three Zenodo draws; on the last draw it is 0.158 and 0.205 under a
  second vision-language embedder and 0.35 to 0.50 under two CLIP-family dual towers. With every
  creator weighted equally it is 0.13 and 0.14 under E1, and 0.06 and 0.12 on queries whose file
  names do not give the folder away. On GitHub directories, with at least 100 owners per cell, it is
  0.21 and 0.20 under E1 on the draw sized for that minimum (S24), confirmed in both cells.
- **Does the loss reach a simulated searcher's queries?** Yes under E1: 0.140 recall@5 for pictures
  in text-heavy folders and 0.420 for documents in image-heavy ones, both registered before any query
  was scored. Under E2 the picture cell shows no loss.
- **Why?** A mixed folder is two clusters, its images and its texts, and one vector sits between
  them. Centering recovers 8 to 62 percent of the loss depending on the encoder and the cell.
- **What fixes it, and at what budget?** A few k-means representatives per modality label. Four per
  label are not inferior to exhaustive file-level search at a 0.02 margin under all four encoders
  (post hoc). Three per label take 3,993 to 10,648 bytes per folder on average by encoder at one
  byte per dimension. Two vectors per folder fall short under three of the four encoders.
- **Does a folder summary guide a walk down a tree?** Not yet at 2 KiB: on 261 repository trees the
  guided walk finds the target 0.069 less often than reading every directory's own summary, though
  it reads 0.39 as many.
- **Does a written folder abstract do better?** Not for the folder's images.

## Citation

Please cite the paper, using the version DOI
[10.5281/zenodo.23178122](https://doi.org/10.5281/zenodo.23178122). GitHub's "Cite this
repository" button reads [`CITATION.cff`](CITATION.cff), and [`citation/`](citation/) holds BibTeX,
RIS and CSL JSON files and formatted strings.

**BibTeX**

```bibtex
@misc{basheer2026fewvectors,
  author       = {Basheer, Ali},
  title        = {A few vectors for a mixed folder: a pre-registered measurement of pooled directory embeddings},
  year         = {2026},
  month        = oct,
  date         = {2026-10-06},
  publisher    = {Zenodo},
  version      = {1},
  doi          = {10.5281/zenodo.23178122},
  url          = {https://doi.org/10.5281/zenodo.23178122},
  note         = {Preprint, not peer reviewed. Code and data: https://github.com/ali-basheer/dirvec-study}
}
```

**APA**

> Basheer, A. (2026). *A few vectors for a mixed folder: a pre-registered measurement of pooled
> directory embeddings* (Version 1) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.23178122

**IEEE**

> A. Basheer, "A few vectors for a mixed folder: a pre-registered measurement of pooled directory
> embeddings," Zenodo, preprint, Oct. 6, 2026, doi: 10.5281/zenodo.23178122.

The concept DOI [10.5281/zenodo.23178121](https://doi.org/10.5281/zenodo.23178121) stands for all
versions and resolves to the latest one.

## Links

- Zenodo record: https://zenodo.org/records/23178122
- DOI: https://doi.org/10.5281/zenodo.23178122
- Landing page and PDF (Craftpine): https://www.craftpine.com/dirvec
- ORCID: https://orcid.org/0009-0006-2396-9932
- Author website: https://www.basheerali.com/
- Code and data: https://github.com/ali-basheer/dirvec-study

## License

- **Code** (`scripts/`): MIT License, see [`LICENSE`](LICENSE).
- **Paper, briefs, results and data manifests** (the LaTeX source and figures in `paper/`,
  `BRIEF.md`, `prereg/`, `results/`, `reports/`, `citation/` and the files in `data/`):
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
