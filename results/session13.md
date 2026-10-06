# dirvec session 13: correction of the session 9 single-vector rows

> **Errata, added 2026-10-04 after the seventh pass of the number audit
> (reports/number_audit_2026-10-01.md). The text and tables below are unchanged; where a sentence and a
> verbatim table disagree, the table is right.**
> - "every other row of the study reproduces rank for rank" (the paragraph below): the check that ran
>   is C2, which compares this session's rank files with session 9's. It covers the session 9 rows
>   that do not use the weighted-pooling builder, 26 on the dev queries, 7 on the cross-fitted dev
>   grid and 17 on the test queries. No rank file of another session was compared here.
> - "The single vectors that keep the minority (c_p0, coral_p0, coral_p0.25, c_p0.25) are the ones
>   that lose most in M2": five single vectors are no more than 0.02 below c in both minority cells,
>   the four named and u_p0 = ab (-0.017 and -0.018). They are 0.055 to 0.113 below c in M2. The rows
>   that lose most in M2 are the four ridge rows at alpha 0, 0.116 to 0.138 below c, and those are
>   0.130 to 0.489 below c in P1 as well (results/session13_outputs.md, the x - c table of the test
>   split).

Why this session exists. On 2026-10-01 the draft's numbers were checked against results/ by checkers
that had not seen the draft (reports/number_audit_2026-10-01.md). One of them found that every F1
and F2 row of session 9 was scored too low by a bug in scripts/eval.py. This session fixes the bug,
reruns the session 9 dev grids and test split, and re-reads H9a on the corrected rows. Nothing else
changes: every other row of the study reproduces rank for rank.

Pod bmao44n64ohrwp (MIG 1g.24gb slice, 3 threads), 2026-10-01 17:49 to 18:08 UTC, driven by hand
through the pod's command endpoint; about $0.19. Brief committed before any corrected number was
read (333a4b0, after the fix f59db72). numpy 2.5.2, scikit-learn 1.9.1. The outputs are in
results/session13_outputs.md, verbatim, as the pod wrote and pushed them (fb80c7b).

## The bug

`build()` for the weighted-pooling base (every `<space>_p<alpha>` name: F1 and F2) multiplied a
float32 group mean by `g.sum() ** param`, a NumPy float64 scalar, so the folder vector was float64.
`rank_rep()` computed the query's own-directory score in float64, wrote it into a float32 score row
and then counted `s > own` against the unrounded value. Whenever the float32 rounding went up, the
query's own directory counted as scoring strictly higher than itself. Rank + 1 in half the queries.

It was visible in the committed session 9 tables: u_p1 is a and c_p1 is ac by definition, yet they
printed recall@1 0.274 against 0.555 and 0.295 against 0.588, and recall@5 0.681 against 0.689 and
0.715 against 0.724. Every F1 and F2 row had recall@1 between 0.27 and 0.30.

The fix (f59db72): the builder returns float32, the own score is compared in the dtype of the score
row, and an assertion guards it. `scripts/selftest_ranks.py` runs eval.py end to end on a synthetic
corpus and fails unless u_p1, c_p1, u_p0 and c_p0 rank as a, ac, ab and acb; it fails on the old
eval.py (u_p1 recall@1 0.289 against a's 0.552) and passes on the new one.

The direction of the bias favoured H9a, which is why the verdict had to be read again.

## Hypothesis (verbatim from BRIEF.md, session 13, which copies session 9's H9a unchanged)

H9a (no single vector suffices): no configuration of F1 or F2, after selection on dev, is within
0.02 recall@5 of c in both primary cells on the test split while also within 0.02 of c in both
majority cells. Kill: H9a is dead if the selected F1 or F2 configuration has every one of the four
paired intervals of (x minus c) with an upper bound above -0.02, that is, if no cell is
significantly more than 0.02 below c.
- The verdict is read on the configurations the corrected dev grids select. If they differ from
  session 9's selections (c_p0.5 and coral_p0.75), both sets are reported and the corrected
  selection carries the verdict.
- Expectation, written before the run, not a kill: the F1 and F2 rows rise by about 0.005 to 0.015
  recall@5 and by about a factor of two at recall@1; H9a survives; the best minimum over the four
  cells among the one-vector test rows moves from -0.060 to about -0.05.

## Checks (read before any corrected number)

- C1, self-test on the pod: passes.
- C2, reproduction: every row that does not use the weighted-pooling builder has ranks identical to
  the session 9 files on every query: 26 rows on the 4,388 dev queries, 7 on the cross-fitted dev
  grid, 17 on the 18,742 test queries (a, b, c, d, ac, cc, dc, b2, bc2, bc, f4_w0.5, tb2, tbg, tbc,
  tb2c, tbgc, tbcc). So H9b, H9c and every F3, F4 and F5 number of session 9 stand as printed.
- C3, identity: in the new files u_p1 has a's ranks, c_p1 has ac's, u_p0 has ab's and c_p0 has
  acb's on every query (dev and test).
- What the bug did, row by row: in the session 9 files the F1, CORAL and ridge rows have the rank of
  exactly one more than now on 48 to 52 percent of the queries and the same rank on the rest. Recall@1
  roughly doubles (u_p1 0.274 to 0.555). On the test split recall@5 rises by 0.007 to 0.011 over all
  queries and by 0.005 to 0.013 per cell.
- A side finding on Procrustes: its rows also differ on 4 to 22 percent of the queries in ways that
  are not the off-by-one. The Procrustes map W = U V^T comes from the SVD of a 2,048 by 2,048 matrix
  of rank at most 534 (the number of fitting pairs), so its completion on the null space is
  arbitrary and differs between runs (two threads in session 9, three here). The Procrustes rows are
  reproducible only up to that; they were never selected and nothing in the paper depends on their
  third decimal.

## Dev selection on the corrected grids

Unchanged. F1: c_p0.5 (centered, alpha 0.5), dev minimum over the four cells -0.068 (session 9
printed -0.077). F2, on the two-fold cross-fitted grid: coral_p0.75, dev minimum -0.066 (-0.073).
The literal in-sample F2 grid still picks proc_p0 (minimum -0.009), which is the leak session 9
documented: Procrustes at alpha 0.5 scores recall@5 0.887 in P1 in-sample on the dev queries (c
0.710) and 0.538 cross-fitted. (Session 9's prose quoted 0.88 and 0.51; the 0.51 was a smoke test on
one half-split, and its own cross-fitted table printed 0.524.) Ridge is between -0.215 and worse
cross-fitted; its P1 recall@5 runs from 0.03 to 0.52.

## Verdict

**H9a survives on the corrected rows.** Test split, 18,742 queries, x minus c in recall@5 with paired
95 percent intervals over directories (c: 0.783 all, 0.647 P1, 0.680 P2, 0.751 M1, 0.875 M2):

| row | all | P1 | P2 | M1 | M2 |
|---|---|---|---|---|---|
| c_p0.5 (F1 selected), session 13 | -0.041 [-0.051, -0.031] | -0.048 [-0.077, -0.021] | -0.045 [-0.070, -0.019] | -0.027 [-0.047, -0.009] | -0.047 [-0.061, -0.036] |
| the same row as session 9 printed it | -0.051 | -0.061 [-0.090, -0.033] | -0.053 [-0.078, -0.027] | -0.035 [-0.056, -0.018] | -0.058 [-0.072, -0.044] |
| coral_p0.75 (F2 selected), session 13 | -0.038 [-0.047, -0.029] | -0.030 [-0.062, +0.000] | -0.086 [-0.110, -0.059] | -0.001 [-0.016, +0.016] | -0.049 [-0.062, -0.038] |
| the same row as session 9 printed it | -0.046 | -0.039 [-0.071, -0.008] | -0.094 [-0.119, -0.068] | -0.008 [-0.023, +0.008] | -0.056 [-0.069, -0.044] |

For c_p0.5 the upper bounds are -0.021 (P1), -0.019 (P2), -0.009 (M1) and -0.036 (M2): two cells
are significantly more than 0.02 below c, P1 by a hair and M2 clearly. For coral_p0.75 they are
+0.000, -0.059, +0.016 and -0.038: P2 and M2 are significantly more than 0.02 below. Neither kill
fires. The expectation written before the run held: the rows rose by about 0.01, and the best
minimum over the four cells moved from -0.060 to -0.048.

## Secondary: every one-vector row on the test split

The test run scored 44 one-vector rows: a, ac, ab, acb, the ten F1 rows and all thirty F2 rows. Four
of them are duplicates by construction (u_p1 = a, c_p1 = ac, u_p0 = ab, c_p0 = acb), so 40 distinct
single vectors. Session 9's prose said 22 rows; its test table had 18 (a, ac, ten F1, five CORAL,
one Procrustes).

| row | P1 | P2 | M1 | M2 | min over 4 cells | cells within 0.02 (point) | cells with upper bound above -0.02 |
|---|---|---|---|---|---:|---:|---:|
| c_p0.5 | -0.048 [-0.077, -0.021] | -0.045 [-0.070, -0.019] | -0.027 [-0.047, -0.009] | -0.047 [-0.061, -0.036] | -0.048 | 0 | 2 |
| coral_p0.5 | +0.001 [-0.027, +0.028] | -0.047 [-0.069, -0.023] | -0.006 [-0.022, +0.010] | -0.052 [-0.066, -0.040] | -0.052 | 2 | 2 |
| c_p0.25 | -0.009 [-0.034, +0.016] | -0.008 [-0.028, +0.014] | -0.030 [-0.050, -0.012] | -0.055 [-0.068, -0.042] | -0.055 | 2 | 3 |
| coral_p0.25 | +0.021 [-0.005, +0.046] | -0.012 [-0.030, +0.010] | -0.016 [-0.032, +0.002] | -0.065 [-0.078, -0.052] | -0.065 | 3 | 3 |
| u_p0.25 | -0.065 [-0.090, -0.043] | -0.069 [-0.093, -0.046] | -0.035 [-0.054, -0.018] | -0.059 [-0.072, -0.048] | -0.069 | 0 | 1 |
| c_p0.75 | -0.085 [-0.116, -0.056] | -0.084 [-0.112, -0.056] | -0.031 [-0.050, -0.014] | -0.042 [-0.055, -0.030] | -0.085 | 0 | 1 |
| coral_p0.75 | -0.030 [-0.062, +0.000] | -0.086 [-0.110, -0.059] | -0.001 [-0.016, +0.016] | -0.049 [-0.062, -0.038] | -0.086 | 1 | 2 |
| c_p0 = acb | +0.023 [+0.003, +0.044] | +0.016 [-0.001, +0.035] | -0.065 [-0.090, -0.042] | -0.092 [-0.108, -0.075] | -0.092 | 2 | 2 |
| coral_p0 | +0.032 [+0.008, +0.056] | -0.001 [-0.019, +0.019] | -0.047 [-0.067, -0.024] | -0.110 [-0.128, -0.091] | -0.110 | 2 | 2 |
| u_p0 = ab | -0.017 [-0.038, +0.003] | -0.018 [-0.035, +0.001] | -0.071 [-0.094, -0.049] | -0.113 [-0.131, -0.095] | -0.113 | 2 | 2 |
| c_p1 = ac | -0.120 [-0.153, -0.088] | -0.122 [-0.155, -0.092] | -0.032 [-0.050, -0.016] | -0.042 [-0.055, -0.030] | -0.122 | 0 | 1 |
| u_p1 = a | -0.236 [-0.269, -0.204] | -0.241 [-0.273, -0.213] | -0.041 [-0.059, -0.025] | -0.044 [-0.056, -0.034] | -0.241 | 0 | 0 |

(The ten best rows by their minimum, and the two plain corners; all 44 are in the outputs file.)

- No one-vector row, selected or not, has all four upper bounds above -0.02. The pre-registered
  question of whether an exception has to be named has the answer no.
- The binding cell is M2, text-like queries in text-heavy folders. Every one of the 44 rows is at
  least 0.042 below c there, and no upper bound is above -0.030. The single vectors that keep the
  minority (c_p0, coral_p0, coral_p0.25, c_p0.25) are the ones that lose most in M2.
- The best minimum over the four cells is -0.048 (c_p0.5); session 9 printed -0.060 (coral_p0.5).
- Session 9's sentence that no row is within 0.02 of c in more than two of the four cells does not
  survive the correction: coral_p0.25 is within 0.02 in three cells at the point estimate (P1
  +0.021, P2 -0.012, M1 -0.016) and 0.065 below in the fourth; c_p0.25 and coral_p0.25 have three
  upper bounds above -0.02. Three is the most any row reaches.
- The equal-weight corners. Centered (c_p0 = acb): +0.260 and +0.258 over the pooled centroid in P1
  and P2 (results/session8.md), +0.023 and +0.016 over c, and 0.065 and 0.092 below c in M1 and M2.
  Uncentered (u_p0 = ab): 0.017 and 0.018 below c in the minority cells, 0.071 and 0.113 below in the
  majority cells. Session 9's prose ("lifts P1 and P2 by 0.24 and costs M1 and M2 0.07 and 0.11")
  mixed a lift measured against a with a cost measured against c, on biased rows.
- Alignment and the same-folder cosine, test directories, fitted on the calibration split: image-text
  0.205 centered, 0.201 after Procrustes, 0.190 after CORAL, as session 9 printed. Ridge, which the
  session 9 test run did not include, raises it (0.307, 0.293, 0.246, 0.231 for lambda 1 to 1000) by
  pulling every image vector toward the text mean (same-folder image-image cosine 0.71 to 0.84
  against 0.57 centered), and loses the image queries: P1 recall@5 from 0.517 down to 0.005. So "no
  alignment raises the cross cosine" is true of Procrustes and CORAL only; ridge raises it and is
  worse for it.

## What this replaces

- results/session9.md: the F1 and F2 rows of every table (dev and test), the H9a paragraph's
  magnitudes, "22 rows", "the best minimum ... is -0.060", "no row is within 0.02 of c in more than
  two of the four cells", "0.51" for the cross-fitted Procrustes figure, and the "lifts ... by 0.24
  and costs ... 0.07 and 0.11" sentence. Its tables stay as they were computed; an erratum at the top
  points here. Its F3, F4 and F5 rows, H9b, H9c, the gap and purity tables are unaffected (C2).
- NOTES.md session 9 results and BRIEF.md's "numbers the draft takes from the repo": the same
  figures.
- paper/main.tex: the single-vector paragraph of the remedy section, the abstract's single-vector
  sentence and the appendix entry for H9a take the numbers above.
- Nothing else. Sessions 2 to 8 and 10 to 12 never used the weighted-pooling builder.
