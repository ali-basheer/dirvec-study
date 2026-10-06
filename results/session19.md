# Session 19 results: the minority-modality loss on a second source (directories of GitHub repositories)

Pre-registered in BRIEF.md (5bfe3a4, OpenTimestamps proof a108019) before any repository was listed;
code amended before the harvest (612e8f5, proof 5683418), no definition changed. Corpus pushed before
any embedding (889df59); outputs verbatim in results/session19_outputs.md (c111c0c). One automated run
of scripts/s19_run.sh on the MIG pod s46ksd0pdara1o (1g.24gb, $0.59/h) on 5 October 2026: start 01:52
UTC, corpus pushed 02:54, E1 embedded 02:54 to 03:50, E4 03:54 to 04:02, E2 04:04 to 04:19, outputs
pushed 04:22. No step failed and nothing was resumed. Under each encoder s19.py first reproduced
eval.py's directory intervals of c - a in P1 and P2 (six of six the same).

Corpus. 14 days read, 14,834 repositories with at least five stars, 5,517 usable; 4,322 read (4,320
tarballs, 2 over the size cap). 35,970 eligible directories in the repositories read, 1,501 mixed (4.2
percent; 11.2 percent at the root, 3.0 percent at depth two or more). Scored set: 1,600 directories
(1,000 mixed, 600 other), 12,656 files (1.6 GB), 1,079 repositories, 1,053 owners. E1, E4 and E2 each embedded
12,049 files (607 not embedded: 466 images, 130 other, 10 text, 1 table). Evaluation queries: 7,372
over 1,172 directories and 858 owners, the same set under the three encoders (9,089 queries with a
vector, 1,717 of them in the calibration directories). Commit-subject queries:
1,162 over 522 directories and 440 owners, from 10,068 qualifying commits.

## Hypotheses, verbatim from BRIEF.md (session 19)
Primary family, three tests, each read on its 98.33 percent interval (Bonferroni over the three):
- H19a. Under E1 on the evaluation queries, c minus a in P1s and in P2s. Confirmed if both cells
  are confirmed. Replicated with the size open if both are confirmed or present. Not replicated at
  the registered size if either cell is below +0.05. Inconclusive otherwise.
- H19c. Under E1, on the queries whose folder c does not hold whole (a label keeps more than three
  files once the query is left out), c minus d. Not inferior if L is at least -0.02; inferior if U
  is under -0.02; inconclusive otherwise.
Secondary, with a registered reading on the 95 percent interval:
- H19b. The H19a statistic on the clean subset of P1s and of P2s, read as a loss.
- H19d. With the commit subject as the query, c minus a on image-heavy directories (image fraction
  at least 0.5), read as a loss. Gate: file-level search d reaches recall@5 of at least 0.10 on
  those queries and more than the file names alone. If the gate fails the test is untestable.
- The H19a statistic on no-code folders; on all of P1 and of P2; cs minus d where c differs from d.

Definitions used by the readings (BRIEF.md): owner-weighted mean (the mean over owners of the owner's
mean), percentile intervals from 10,000 resamples of owners, and a test with fewer than 100 owners is
inconclusive. A loss x - y on [L, U] is confirmed if L is at least +0.05, below +0.05 if U is under
+0.05, present with the size open if L is above zero, inconclusive otherwise.

## Verdicts (E1 decides)

| test | queries | owners | point | 95% | 98.33% | reading |
|---|---:|---:|---:|---|---|---|
| H19a P1s: c - a (primary) | 226 | 86 | +0.193 | [+0.114, +0.277] | [+0.099, +0.295] | inconclusive (fewer than 100 owners) |
| H19a P2s: c - a (primary) | 355 | 98 | +0.166 | [+0.093, +0.241] | [+0.080, +0.260] | inconclusive (fewer than 100 owners) |
| H19c: c - d where c differs from d (primary) | 5381 | 512 | -0.002 | [-0.011, +0.006] | [-0.014, +0.008] | not inferior |
| H19b P1s clean: c - a | 118 | 60 | +0.188 | [+0.090, +0.293] | [+0.071, +0.317] | inconclusive (fewer than 100 owners) |
| H19b P2s clean: c - a | 205 | 82 | +0.142 | [+0.063, +0.225] | [+0.045, +0.245] | inconclusive (fewer than 100 owners) |
| no-code folders, P1s: c - a | 67 | 31 | +0.210 | [+0.075, +0.355] | [+0.048, +0.392] | inconclusive (fewer than 100 owners) |
| no-code folders, P2s: c - a | 232 | 62 | +0.096 | [+0.022, +0.173] | [+0.007, +0.190] | inconclusive (fewer than 100 owners) |
| all of P1 (lone images included): c - a | 500 | 334 | +0.069 | [+0.037, +0.100] | [+0.030, +0.108] | present, size open |
| all of P2 (lone texts included): c - a | 512 | 231 | +0.071 | [+0.036, +0.107] | [+0.028, +0.114] | present, size open |
| cs - d where c differs from d | 5381 | 512 | -0.001 | [-0.011, +0.007] | [-0.013, +0.009] | not inferior |

- **H19a: inconclusive.** Both cells hold fewer than the 100 owners the brief requires (86 and 98).
  Read without the owner minimum, both lower bounds of the 98.33 percent intervals are above +0.05
  (+0.099 and +0.080), which the rule calls confirmed; the rule is not relaxed after the fact.
- **H19c: not inferior.** Where c is a real compression of its folder, c stays within 0.02 of opening
  every file (lower bound -0.014, 512 owners).
- **H19b: inconclusive** (60 and 82 owners). Both 95 percent lower bounds are above zero.
- **H19d: inconclusive** (66 owners). The gate passed: d reaches 0.254 on these queries against 0.066
  for the file names alone. c - a is +0.010 [-0.061, +0.078].
- Secondaries: on all of P1 and of P2 the loss is present with the size open (+0.069, +0.071; 334 and
  231 owners). cs - d is not inferior.

E4 and E2, read by the same rules, with no verdict of their own (results/session19_outputs.md):

| encoder | H19a P1s | H19a P2s | H19c | H19b P1s clean | H19b P2s clean | H19d (commit subjects) |
|---|---|---|---|---|---|---|
| E4 | +0.460 [+0.347, +0.574] | +0.408 [+0.303, +0.517] | -0.002 [-0.011, +0.007] | +0.388 [+0.277, +0.504] | +0.328 [+0.236, +0.424] | +0.101 [+0.040, +0.172] |
| E2 | +0.471 [+0.357, +0.585] | +0.301 [+0.204, +0.401] | +0.003 [-0.005, +0.011] | +0.389 [+0.276, +0.508] | +0.272 [+0.185, +0.364] | +0.146 [+0.071, +0.230] |

H19a and H19c on their 98.33 percent intervals, the others on their 95 percent intervals. Every H19a
and H19b cell is inconclusive by the owner minimum under both encoders; H19c is not inferior under
both; H19d passes its gate under both (d 0.139 and 0.172 against names 0.066) and is inconclusive by
owners.

## Reading
- The loss is on the second source under all three encoders. The minority files of GitHub
  directories, images among texts (P1s) and texts among images (P2s), are found less often through
  the pooled vector a than through the per-modality representatives c: by 0.19 and 0.17 under E1,
  0.46 and 0.41 under E4, 0.47 and 0.30 under E2. All six 98.33 percent intervals lie above zero (the
lowest lower bound is +0.080). What the
  registered test cannot say is whether this holds over enough independent owners: 86 and 98 is fewer
  than the 100 the brief fixed. Session 24, registered after this table was read (BRIEF.md), draws a
  second sample of directories twice the size and reads the same tests on it alone.
- The loss is where the brief said a lone file cannot show it. On all of P1, half of whose queries are
  lone images among texts with no image sibling to be found through, c - a is +0.069; on P1s it is
  +0.193.
- File names do not explain it. On the clean subset, where neither file-name router finds the folder
  at rank 5 and no file shares the query's stem, c - a is +0.188 and +0.142 under E1.
- By the kind of the query file under E1 (P2s, owner-weighted, 95 percent): code +0.298 [+0.136,
  +0.457] (80 queries, 37 owners), config +0.143, prose +0.096; images in P1s +0.193.
- c keeps what opening every file keeps. H19c holds under all three encoders. Over all queries c - d
  is +0.001 under E1 (directory interval [-0.003, +0.005]). In P1 d is ahead of c by 0.022
  (directory interval [-0.040, -0.004]); in P2 by 0.018. These are secondaries without a reading.
- The two dual towers lose more than E1 on the same queries, as on Zenodo: (c - a) under E4 minus
  under E1 is +0.126 in P1 and +0.281 in P2; under E2 +0.136 and +0.137 (directory intervals above
  zero).
- Written queries. With commit subjects as the query on image-heavy directories, E1 shows no loss
  (+0.010, interval across zero), while E4 and E2 show +0.10 and +0.15. These are text queries for a
  folder that is mostly images, so the pooled vector is dominated by the folder's majority; under E1
  it routes them as well as c does. The test is inconclusive by owners under all three, and the E1
  point is the honest reading: on human-written queries the loss under the strongest encoder was not
  seen on this draw.
- Mixed directories are rare in the wild: 4.2 percent of the eligible directories of the repositories
  read, more at the root (11.2 percent) than deeper (3.0 percent at depth two or more). The scored set
  over-samples them on purpose (BRIEF.md).

## Deviations
- The code was amended before the harvest (612e8f5, listed in the brief with its proof); no
  definition, cell, test or reading changed.
- A preflight ran on the pod before the run (scripts/s19_preflight.sh: the self-test in the pod's own
  Python and the real endpoints on a throwaway draw, seed 7, one day, nine directories, suffix _p19,
  removed afterwards). It computes no retrieval number.
- The E1 table above was read on the pod at 03:54 UTC, before the E4 and E2 numbers existed. Session
  24 was written after it (BRIEF.md, committed 04:07 UTC, proof 22b5759). It is a replication designed
  after a first result was seen, and the paper says so. H19a's verdict stays what this brief makes it.
- Sessions 21 and 23 were registered while this run was going (472acc6 during the harvest, 2e80415
  during the E1 embedding), before any number of theirs or of this session existed.

## After session 24 (5 October 2026)
Session 24 (results/session24.md) drew 2,600 further directories (2,000 mixed) from 8,307 repositories
that session 19 had not read and read the same tests under E1. H24a is confirmed in both cells
(P1s +0.210 [+0.144, +0.279] from 172 owners, P2s +0.196 [+0.133, +0.260] from 197) and H24c is not
inferior (-0.002 [-0.010, +0.006], 918 owners). Pooled over both draws the loss is +0.205 and +0.186
(258 and 294 owners), the size on this source; the pooled estimate carries no verdict for H19a, which
stays inconclusive.
