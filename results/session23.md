# Session 23 results: a walk down whole repository trees, guided by folder summaries

Pre-registered in BRIEF.md (2e80415, OpenTimestamps proof a848d3e) while the session 19 pod was
embedding its first draw, before any retrieval number of the GitHub source existed; the harvest was
raised from 200 to 300 trees in the session 24 brief (84d1a96) before any tree was read. Corpus pushed
before any embedding (6665a7e); outputs verbatim in results/session23_outputs.md (ca95b57). One
automated run of scripts/s23_run.sh on the session 19 pod (s46ksd0pdara1o), started by
scripts/s19_followup.sh after session 24 on 5 October 2026: start 08:00 UTC, the self-test of tree.py
against a plain implementation passed (32,945 values; 5 differences, all near-ties), harvest 08:01 to
08:16, corpus pushed 08:19, E1 embedded 33,092 files from 08:19 to 10:36 (32,060 embedded), the walk
and the outputs by 10:37. The watcher stopped the pod at 10:38. No step failed.

Trees. 2,328 repositories of session 19's pool read in their own seeded order; 261 taken whole (11.2
percent of those read) before the 33,000-file stop: 33,092 files, 8,354 with an image extension, in
8,587 directories with a kept file. Queries: 20,814 over 260 repositories and 259 owners; the minority
cell (the query's input group holds under half of the repository's other embedded files, and its
directory holds a sibling of its group) has 2,844 queries from 208 owners. A repository has 37.9
directories with an embedded file on average (query-weighted), and the targets lie at depths 0 to 14,
about half of them at depth 3 or more (10,075 queries).

## Hypotheses, verbatim from BRIEF.md (session 23)
One family, three tests, under E1 at 2 KiB, each read on its 98.33 percent interval:
- H23a, the loss at inner nodes: walk success with fsample minus walk success with mean on the
  minority queries, read as session 19 reads a loss (confirmed if the lower bound is at least +0.05;
  below +0.05 if the upper bound is under it; present with the size open if the lower bound is above
  zero; inconclusive otherwise).
- H23b, the kinds in a summary that merges: walk success with fsample minus with usample on the
  minority queries. The kinds matter if the lower bound is above zero; the uniform sample is better
  if the upper bound is below zero; no difference at the margin if the interval lies within -0.02
  and +0.02; inconclusive otherwise.
- H23c, the walk against reading every directory: walk success minus flat success, both with
  fsample, over all queries. Not inferior if the lower bound is at least -0.02; inferior if the upper
  bound is under -0.02; inconclusive otherwise. Reported with the summaries each reads.
Expectation, written before the run and not a test: H23a confirmed, since an image query in a
repository of mostly text meets children whose means all look like text; H23b the kinds matter;
H23c open, since a walk compounds its errors over the levels; names strong, since session 17 found
file-name routers level with the pooled vector on leave-one-out queries.

The walk (BRIEF.md): from the root, at each directory the reader scores "stay" by the directory's
own-files summary and each child by the child's subtree summary, takes the best, and stops when "stay"
wins. Success: it stops in the target directory. Flat: the own-files summary of every directory of the
repository is read and the best taken. fsample keeps a fixed share of the slots per kind and merges
exactly up the tree; usample is the bottom-k sample by hash, kinds ignored.

## Verdicts

| test | queries | owners | point | 95% | 98.33% | reading |
|---|---:|---:|---:|---|---|---|
| H23a: walk, fsample - mean, minority, 2 KiB | 2844 | 208 | +0.024 | [-0.014, +0.063] | [-0.022, +0.073] | inconclusive |
| H23b: walk, fsample - usample, minority, 2 KiB | 2844 | 208 | +0.064 | [+0.034, +0.097] | [+0.028, +0.104] | the kinds matter |
| H23c: walk - flat, fsample, all queries, 2 KiB | 20814 | 259 | -0.069 | [-0.083, -0.056] | [-0.086, -0.054] | inferior |

- **H23a: inconclusive.** At 2 KiB, a per-kind sample does not walk to the minority files measurably
  better than the mean does (+0.024, interval across zero). By the brief, the paper reports the walk as
  built and says that a per-kind summary did not help it at the registered size.
- **H23b: the kinds matter.** Among summaries that merge exactly up a tree, the one that keeps a share
  per kind walks to the minority files better than the uniform sample, by +0.064.
- **H23c: inferior.** At 2 KiB the walk finds the target 0.069 less often than reading the own-files
  summary of every directory, and it reads 0.39 as many summaries (12.7 against 32.7 per query,
  owner-weighted). By the brief, the summaries at this budget serve a flat read of a tree and not a
  descent.

## Reading
Owner-weighted success, 2 KiB (results/session23_outputs.md):

| summary | walk, all | walk, minority | flat, all | flat, minority | first step right, minority |
|---|---:|---:|---:|---:|---:|
| mean | 0.630 | 0.686 | 0.671 | 0.782 | 0.791 |
| usample | 0.542 | 0.646 | 0.599 | 0.745 | 0.750 |
| fsample | 0.528 | 0.710 | 0.597 | 0.745 | 0.814 |
| sample | 0.537 | 0.723 | 0.599 | 0.746 | 0.824 |
| every file at one bit (no budget) | 0.625 | 0.753 | 0.625 | 0.753 | 0.862 |
| file names (no vector) | 0.477 | 0.649 | 0.478 | 0.655 | 0.786 |
| chance | 0.069 | 0.092 | 0.047 | 0.049 | |

- The mean is the strongest summary for the walk over all queries at 2 KiB (0.630 against 0.528 for
  fsample; fsample minus mean -0.103 [-0.121, -0.085]). At this budget the samples hold few vectors:
  fsample stores 2.86 vectors per own-files summary and 3.86 per subtree summary on average, against
  eight slots, because a kind with fewer files than its share leaves its slots empty. Most
  directories hold few files, but the subtrees a walk compares near the root hold many more than
  eight (a tree holds 127 kept files on average), and a plausible reading is that a few sampled files
  cover a large subtree's majority worse than its mean does. This reading was not tested.
- On the minority queries the per-kind samples are ahead of the mean in the walk, by little and not
  measurably at the registered size (fsample +0.024, sample +0.037 by the table), and their first step
  is right more often (0.814 and 0.824 against 0.791). In the flat read the mean is ahead on the
  minority queries too (flat, fsample minus mean -0.037 [-0.062, -0.014]).
- At 8 KiB (32 one-bit vectors, a secondary without a reading), the walk with fsample beats the mean on
  the minority queries by +0.067 [+0.031, +0.103] and stays 0.017 [-0.023, -0.011] behind the flat
  read over all queries, where the mean is 0.041 behind. More bytes make the per-kind sample the better
  summary for the minority files and bring the walk within reach of the flat read.
- The kinds matter for a merging summary at both budgets (fsample minus usample +0.064 at 2 KiB,
  +0.021 [+0.007, +0.039] at 8 KiB), and sample against usample, the kinds with every slot used, gives
  +0.077 [+0.047, +0.108] at 2 KiB.
- Vectors add to names: fsample beats the file-name reader by +0.050 [+0.026, +0.074] over all queries
  at 2 KiB and +0.127 [+0.106, +0.150] at 8 KiB. The expectation that names would be strong held only
  in part: names reach 0.477 over all queries, below every vector summary.
- By the depth of the target, the samples are best at the root (0.698 for fsample) and fall with depth
  (0.439 at depth 3 or more), while the mean holds about level (0.574 at depth 3 or more). A walk
  compounds its errors over the levels, as the brief expected for H23c.

## Deviations
- The harvest stopped at the 33,000-file limit with 261 trees, short of the 300 the amended brief
  allowed; the brief says the run goes on with what there is.
- Nothing else; the self-test, the harvest rules and the readings ran as registered.
