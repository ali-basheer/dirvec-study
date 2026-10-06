# Session 24 results: a second draw of GitHub directories, sized for the owner minimum

Pre-registered in BRIEF.md (84d1a96, OpenTimestamps proof 22b5759) after session 19's E1 table was
read and before any number of sessions 21 and 23 existed. scripts/pool.py was committed before this
draw was embedded (5a108f4, proof 4fab7c9). Corpus pushed before any embedding (15cc35a); outputs
verbatim in results/session24_outputs.md (78f2bb8) and results/session24_budget_outputs.md (a30a27d);
the pooled estimates in results/session24_pooled_outputs.md (22f62f5). One automated run of
scripts/s24_run.sh on the session 19 pod (s46ksd0pdara1o), started by scripts/s19_followup.sh after
session 21 on 5 October 2026: start 04:42 UTC, pool 33 days by 05:12, one harvest round 05:12 to 06:03
(full), corpus pushed 06:07, E1 embedded 06:08 to 07:54, eval, commit-subject queries and validity by
07:59, budget.py on this draw 07:59 to 08:00. No step failed and nothing was resumed. s19.py
reproduced eval.py's directory intervals of c - a in P1 and P2 (same, same); budget.py reproduced
eval.py's a and d ranks rank for rank; pool.py reproduced all fourteen lines it pools on each draw
alone, character for character, before any pooled number.

Corpus. 33 days read (session 19's 14 included), 35,516 repositories with at least five stars, 13,193
usable; 8,307 repositories read that session 19 had not read (8,303 tarballs, 4 over the size cap).
65,984 eligible directories in them, 3,286 mixed (5.0 percent; 12.6 percent at the root, 4.0 percent
at depth two or more). Scored set: 2,600 directories (2,000 mixed, 600 other), 21,854 files, 1,885
repositories, 1,826 owners, 3.5 GB of kept files. E1 embedded 20,924 files. Evaluation queries: 12,951
over 1,923 directories and 1,473 owners (16,185 queries with a vector, 3,234 of them in the calibration
directories). Commit-subject queries: 1,827 over 845 directories and 731 owners.

## Hypotheses, verbatim from BRIEF.md (session 24)
Primary family, three tests on this draw, each read on its 98.33 percent interval:
- H24a. H19a's statistic and readings: c minus a in P1s and in P2s under E1. Confirmed if both cells
  are confirmed; replicated with the size open if both are confirmed or present; not replicated at
  the registered size if either cell is below +0.05; inconclusive otherwise.
- H24c. H19c's: c minus d where c differs from d. Not inferior if the lower bound is at least -0.02;
  inferior if the upper bound is under -0.02; inconclusive otherwise.
Secondary, read on the 95 percent interval as in session 19: H24b, the H24a statistic on the clean
subset; H24d, c minus a with the commit subject as the query on image-heavy directories, with
session 19's gate; no-code folders; all of P1 and of P2; cs minus d.
The byte-budget tests on this draw, one family of three on 98.33 percent intervals, with session
21's cells, budget (2,048 bytes), policies and readings: H24e is H21a (sample minus mean, minority
queries whose folder is not stored whole), H24f is H21b (sample minus k-means, all queries whose
folder is not stored whole), H24g is H21c (sample minus the uniform sample, minority, not whole).
Pooled over both draws, reported with 95 and 98.33 percent intervals and the reading its rule gives:
every test above and H21a, H21b, H21c.

What decides what (BRIEF.md): the second-source claim rests on H24a and H24c read on this draw alone;
the pooled estimate is the size on this source and carries no verdict for H19a or H24a. For H21a,
H21b and H21c, a cell with fewer than 100 owners on a single draw takes the pooled reading, with the
two single-draw reads in the same table.

## Verdicts on this draw (E1)

| test | queries | owners | point | 95% | 98.33% | reading |
|---|---:|---:|---:|---|---|---|
| H24a P1s: c - a (primary) | 506 | 172 | +0.210 | [+0.155, +0.266] | [+0.144, +0.279] | confirmed |
| H24a P2s: c - a (primary) | 669 | 197 | +0.196 | [+0.144, +0.248] | [+0.133, +0.260] | confirmed |
| H24c: c - d where c differs from d (primary) | 9729 | 918 | -0.002 | [-0.008, +0.005] | [-0.010, +0.006] | not inferior |
| H24b P1s clean: c - a | 232 | 118 | +0.180 | [+0.113, +0.250] | [+0.099, +0.267] | confirmed |
| H24b P2s clean: c - a | 355 | 155 | +0.209 | [+0.147, +0.275] | [+0.134, +0.288] | confirmed |
| no-code folders, P1s: c - a | 230 | 67 | +0.169 | [+0.090, +0.252] | [+0.074, +0.270] | inconclusive (fewer than 100 owners) |
| no-code folders, P2s: c - a | 420 | 127 | +0.181 | [+0.120, +0.245] | [+0.107, +0.260] | confirmed |
| all of P1 (lone images included): c - a | 1083 | 705 | +0.055 | [+0.034, +0.076] | [+0.029, +0.080] | present, size open |
| all of P2 (lone texts included): c - a | 978 | 469 | +0.095 | [+0.065, +0.125] | [+0.060, +0.131] | confirmed |
| cs - d where c differs from d | 9729 | 918 | -0.002 | [-0.009, +0.004] | [-0.010, +0.005] | not inferior |
| H24d: commit subjects, image-heavy, c - a | 271 | 138 | +0.117 | [+0.065, +0.169] | | confirmed (gate passed: d 0.258, names 0.122) |
| H24e (H21a): sample - mean, minority, not whole, 2 KiB | 672 | 146 | +0.252 | [+0.193, +0.312] | [+0.181, +0.327] | confirmed |
| H24f (H21b): sample - kmeans, all, not whole, 2 KiB | 6294 | 365 | -0.052 | [-0.064, -0.040] | [-0.067, -0.038] | inferior |
| H24g (H21c): sample - usample, minority, not whole, 2 KiB | 672 | 146 | +0.097 | [+0.061, +0.136] | [+0.054, +0.145] | the kinds matter |

The secondaries are read on their 95 percent intervals, the primary tests and the byte-budget family
on their 98.33 percent intervals.

- **H24a: confirmed in both cells.** The minority-modality loss replicates on a second, larger draw
  of GitHub directories, with 172 and 197 owners and both lower bounds above +0.05.
- **H24c: not inferior.** Where c is a strict compression of its folder it stays within 0.02 of
  opening every file.
- **H24b: confirmed** on the clean subset in both cells. **H24d: confirmed**: with the commit subject
  as the query on image-heavy directories, the flat walk passes its gate and c beats a by +0.117.
- **H24e confirmed, H24f inferior, H24g the kinds matter.** At 2 KiB a kind-balanced sample of the
  folder's files at one bit beats the mean on minority queries and beats the uniform sample; k-means
  centroids beat the sample by 0.052 over all queries whose folder does not fit whole.

## Pooled over both draws (results/session24_pooled_outputs.md)

| test | S19 | S24 | pooled (owners) | 95% | 98.33% | reading |
|---|---|---|---|---|---|---|
| c - a, P1s | +0.193 (86) | +0.210 (172) | +0.205 (258) | [+0.160, +0.251] | [+0.152, +0.263] | confirmed |
| c - a, P2s | +0.166 (98) | +0.196 (197) | +0.186 (294) | [+0.144, +0.229] | [+0.135, +0.238] | confirmed |
| c - d, c not whole | -0.002 (512) | -0.002 (918) | -0.002 (1425) | [-0.007, +0.003] | [-0.008, +0.005] | not inferior |
| clean P1s | +0.188 (60) | +0.180 (118) | +0.182 (178) | [+0.127, +0.240] | [+0.114, +0.253] | confirmed |
| clean P2s | +0.142 (82) | +0.209 (155) | +0.186 (236) | [+0.137, +0.237] | [+0.127, +0.248] | confirmed |
| commit subjects, image-heavy | +0.010 (66) | +0.117 (138) | +0.083 (203) | [+0.041, +0.126] | [+0.034, +0.135] | present, size open |
| H21a: sample - mean | +0.269 (70) | +0.252 (146) | +0.258 (216) | [+0.208, +0.310] | [+0.198, +0.321] | confirmed |
| H21b: sample - kmeans | -0.042 (207) | -0.052 (365) | -0.048 (572) | [-0.058, -0.040] | [-0.060, -0.037] | inferior |
| H21c: sample - usample | +0.116 (70) | +0.097 (146) | +0.103 (216) | [+0.073, +0.135] | [+0.067, +0.142] | the kinds matter |

Owners present in both draws are counted once with all their queries (0 to 5 in these cells, 12 in
all of P1). By the brief's rule, H21a and H21c, whose S19 cells hold 70 owners, take the pooled
readings: H21a confirmed and H21c the kinds matter. H21b is inferior on both draws and pooled.

## Reading
- The second source holds. The loss of the pooled vector on the minority files of mixed GitHub
  directories is +0.210 and +0.196 on this draw alone and +0.205 and +0.186 pooled, about Zenodo's
  size under the same encoder (+0.253 and +0.169 on S11, in the full cells and weighted by query).
  Session 19's first draw was inconclusive
  only by its owner minimum, and its estimates lie inside this draw's intervals.
- File names do not explain it: on the clean subset it is +0.180 and +0.209 here. By kind of query
  file it is +0.254 for code among images, +0.236 for configuration files and +0.134 for prose.
- Written queries. Here the commit-subject test is confirmed (+0.117 from 138 owners), where session
  19's draw showed +0.010 from 66 owners. Pooled it is +0.083, present with the size open. The loss
  reaches human-written text queries on this source, at about half its size on held-out files.
- c stays within 0.02 of opening every file where it is a strict compression (-0.002 on both draws).
- What to keep in 2 KiB, now on two draws: a kind-balanced sample of eight files at one bit keeps the
  minority files (+0.25 over the mean) and the kinds matter (+0.10 over a sample that ignores them),
  while k-means centroids keep the majority of large folders better (0.05 over the sample). On the
  minority queries of this draw the sample reaches owner-weighted recall@5 0.642, as every file in
  float32 does, against 0.418 for the mean.
- Mixed directories are rarer than on Zenodo, whose pool was selected for them: 5.0 percent of the
  eligible directories of the repositories read here (4.2 percent on session 19's), more often at a
  repository's root (12.6 percent) than at depth two or more (4.0 percent).
- The folder is two clusters on this source too. Under E1 the gap between the mean image and the mean
  text vector is 0.412, and same-folder cosines are 0.717 between images, 0.736 between texts and
  0.504 across (0.170 across after centering, against 0.492 and 0.471 within).

## Deviations
- This session was designed after session 19's E1 table had been read (BRIEF.md says so). Nothing
  was chosen on the new draw.
- scripts/pool.py was not written by the conversation that registered the session; the next one wrote
  and committed it at 05:11 UTC, while this draw was being harvested and before any of its files was
  embedded (NOTES.md). It reads the code files that E1 did not embed from data/notok_code_<draw>_e1.txt,
  taken from the cache index on the pod (two files on S19, one on S24), so that a no-code folder is the
  one s19.py counted.
