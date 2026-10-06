# dirvec

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

## Use of AI

AI assistants (Claude, Anthropic; Gemini, Google) were used throughout this work, for writing,
coding, analysis and review. Models also produced study materials. Qwen3-VL-8B-Instruct wrote the
image captions and folder abstracts, Pixtral-12B wrote the image descriptions used as queries, and
Claude Opus 5.5 wrote the queries of session 27 as a simulated searcher that was told nothing about the
study. No person wrote queries for the study. The author conceived and directed the study and takes
full responsibility for its content.
