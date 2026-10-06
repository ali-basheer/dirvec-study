# Session 25: what a blind review asked for, from per-query files already in the repository

Brief: BRIEF.md, session 25 (commit e79c6e1, before any of the four estimates existed). Outputs,
verbatim: results/session25_outputs.md (scripts/s25.py, about 12 seconds on the workspace; nothing
embedded, no pod). Every number is E1 and post hoc; the paper reports them as such.

## Gates
All passed: pool.py's Draw reproduces the 14 printed lines of each GitHub draw; the S21 ranks give
session 11's recall@5 of a, c and d in all five cells and eval.py's intervals of c minus a in P1
and P2; validity.py's family-weighted c minus a gives session 17's +0.133 and +0.137.

## Readings
1. **GitHub at the natural mix.** Over all evaluation queries, owner-weighted, c minus a is +0.020
   [+0.009, +0.030] on S19, +0.019 [+0.010, +0.028] on S24 and +0.019 [+0.012, +0.026] pooled. It
   is +0.030 [+0.022, +0.039] on the queries of mixed directories and -0.017 [-0.026, -0.008] on the
   queries of the other directories (pooled), where the representatives cost the mean a little.
   Weighted to the eligible share of mixed directories (4,787 of 101,954, 0.047), directory-weighted
   within each stratum, the net is -0.006 [-0.019, +0.008] on S19, -0.021 [-0.033, -0.010] on S24
   and -0.014 [-0.022, -0.005] pooled. At the natural mix of GitHub directories, c is not better
   than the mean over all queries; its gain is confined to mixed folders. The candidates are still
   the scored set's folders (over-sampled for mixing), so the reweighting is approximate.
2. **Zenodo where c compresses.** 13,247 of 17,140 S11 queries (0.773) have a folder in which, the
   query left out, some label keeps more than three files. There c minus d is -0.006 [-0.011,
   -0.002] over all queries, -0.007 [-0.016, +0.003] in P1, -0.015 [-0.022, -0.008] in P2, -0.010
   [-0.022, +0.002] in M1 and -0.001 [-0.005, +0.004] in M2. On the other 3,893 queries, where c
   equals d for the query's own folder, c minus d is -0.014 [-0.020, -0.009]: competitors are still
   compressed, so "within 0.02" is not an artefact of c equalling d.
3. **Zenodo read as the GitHub draws are read.** With the query's folder holding a sibling of its
   input group (P1s 1,545 queries, P2s 1,673) and creator families weighted equally, c minus a is
   +0.266 [+0.224, +0.313] and +0.239 [+0.199, +0.276]; query-weighted it is +0.324 and +0.218.
   Against GitHub pooled (+0.205 and +0.186, owner-weighted) the Zenodo loss is larger on matched
   definitions, not "about the size". On all of P1 and P2, lone files included, family-weighted
   Zenodo is +0.133 and +0.137 against GitHub's +0.069 and +0.071 (S19) and +0.055 and +0.095 (S24).
   Lone queries are 414 of 1,959 in P1 and 473 of 2,146 in P2 on Zenodo.
4. **Budget curve.** On S11 the mean stays at recall@5 0.692 over all queries and 0.44 on the
   minority queries at every budget. Blind k-means at one bit reaches 0.762 and 0.675 at 512 bytes
   (two centroids), 0.798 and 0.712 at 2 KiB and 0.804 and 0.719 at 8 KiB, level with every file at
   one bit (0.803, 0.719) and with d in float32 over all queries (0.804). On GitHub the mean is 0.650
   and 0.420 and k-means 0.661 and 0.570 at 512 bytes, 0.669 and 0.635 at 2 KiB, 0.671 and 0.643 at
   8 KiB. Labels add nothing at equal bytes: kkind minus kmeans at 2 KiB is -0.002 [-0.004, -0.000]
   over all S11 queries and -0.002 [-0.007, +0.004] on its minority queries, and -0.001 and -0.003
   on GitHub (2,313 and 536 owners).

5. **The number of candidate folders** (item 5, registered after items 1 to 4 were read, before it
   was computed). With the own folder and n - 1 others drawn at random, the expected loss under E1
   on S11 is +0.014 and +0.032 in P1 and P2 with 10 candidates, +0.049 and +0.093 with 30, +0.114
   and +0.140 with 100, +0.184 and +0.135 with 300 and +0.232 and +0.152 with 1,000, against +0.253
   and +0.169 with all 2,597. On GitHub (P1s, P2s, owner-weighted) it is +0.013 and +0.049 with 10,
   +0.138 and +0.161 with 100 and +0.188 and +0.183 with 1,000. The loss grows with the number of
   folders that compete; a router choosing among ten sources loses little of it. Re-running the
   script with item 5 added reproduces items 1 to 4 line for line.

## Re-read, not computed
Session 20's intervals of c minus d read as non-inferiority (lower bound at or above -0.02): over
all queries c passes under all four encoders (lowest bound -0.015, E4). In the cells it passes
everywhere under E3, falls just below in one cell under E1 (M1, -0.021) and under E2 (M2, -0.025),
and in three under E4 (P1 -0.022, P2 -0.024, M1 -0.024). The registered rule (no interval entirely
below -0.02) had passed all of them.

## What this changes in the paper
- The recommendation narrows: representatives where a folder is mixed; the mean elsewhere and at
  inner nodes of a tree. A policy that keeps representatives for mixed folders only was not tested.
- The cross-source sentence ("about the size measured on Zenodo") goes; matched numbers replace it.
- "Within 0.02 of searching every file" becomes the non-inferiority reading above, with the
  strict-compression subset.
- Type labels are a convenience: at equal bytes, blind centroids do as well.

## Deviations
- The first commit of scripts/s25.py (e79c6e1) had an unclosed parenthesis in the natural-mix loop.
  It was fixed before the script first ran; no number existed before the fix.
- The manifest rule misses 33 of the 353 files the encoders skipped (read failures it cannot see),
  as the brief said; it counts no evaluation query as without a vector.
