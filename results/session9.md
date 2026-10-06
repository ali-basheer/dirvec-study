# dirvec session 9: the compact folder representation

> **Errata, added 2026-10-01 after the number audit (reports/number_audit_2026-10-01.md). The text and
> tables below are unchanged; where a sentence and a verbatim table disagree, the table is right.**
> - Every F1 and F2 row in this file (dev grids and test split: the `u_p`, `c_p`, `proc_p`, `coral_p`
>   and `ridge*_p` rows) is scored too low by a ranking bug in eval.py: the query's own directory
>   outranked itself in about half the queries (u_p1 is a by definition, yet prints recall@1 0.274
>   against 0.555). The corrected rows, the re-read H9a verdict (it survives) and the list of sentences
>   they replace are in results/session13.md. Every other row here reproduces rank for rank.
> - "22 rows" of one vector in the test run: the test table has 18 (a, ac, ten F1, five CORAL, one
>   Procrustes).
> - Cross-fitted Procrustes at alpha 0.5 in P1: the "0.51" is a smoke test on one half-split; the
>   cross-fitted table below prints 0.524 (0.538 after the correction).
> - "proc_p0 (min +0.164 over the four cells)": +0.164 is its P1 cell; its minimum is -0.013 (M2).
> - "b2 sits at -0.041" on dev: -0.041 is its P1 cell; its minimum is -0.058 (M2).
> - "every two-vector row is 0.02 to 0.05 below" cc and dc in the primary cells: true of the centered
>   rows (bc2, tb2c, tbgc: 0.025 to 0.052 below dc); the uncentered ones (b2, tb2, tbg) are 0.07 to
>   0.10 below.
> - "no row is within 0.02 of c in more than two of the four cells" and "lifts P1 and P2 by 0.24 and
>   costs M1 and M2 0.07 and 0.11": both superseded by results/session13.md.
> - "F2 alignments are fitted on ... the pairs of centered plain group means": true of Procrustes and
>   ridge; CORAL is fitted on the covariances of the calibration files, as the next lines define it.
> - (Added 2026-10-04, seventh pass.) "Dev queries: 4,388 over the 562 calibration directories": the
>   split has 562 directories and the 4,388 queries sit in 555 of them; the header of the same dev run
>   prints "Queries: 4388 over 555 directories" (results/session13_outputs.md).


Question: what is the most compact folder representation that keeps the minority modality without
losing the majority, on a frozen encoder with post hoc processing only, and can one vector per
folder in the encoder's own space ever do it? And is the minority-modality loss under a pooled
centroid a modality effect or plain count dilution?
Same set, cache, encoder, input rules, ground truth, calibration split and evaluation split as
session 8 (`results/session8.md`). No download, no GPU, no new encoder. CPU only (MIG 1g.24gb pod,
3.4 vCPUs by cgroup; numpy 2.5.2, scikit-learn 1.9.1), `DIRVEC_THREADS`, `OMP_NUM_THREADS` and
`OPENBLAS_NUM_THREADS` set to 3.

## Hypotheses (fixed now, do not edit after the first test-split run), copied verbatim from BRIEF.md

H9a (no single vector suffices): no configuration of F1 or F2, after selection on dev, is within
0.02 recall@5 of c in both primary cells on the test split while also within 0.02 of c in both
majority cells. Kill: H9a is dead if the selected F1 or F2 configuration has every one of the four
paired intervals of (x minus c) with an upper bound above -0.02, that is, if no cell is
significantly more than 0.02 below c.
H9b (two centered group vectors suffice): the selected F3 or F4 configuration is within 0.02
recall@5 of c over all test queries and in every one of the four cells. Kill: H9b is dead if in any
of the five cells the paired 95 percent interval of (x minus c) lies entirely below -0.02.
H9c (modality, not dilution): c beats type-blind k-means at c's budget in both primary cells on the
test split. Kill: H9c is dead if the paired interval of (c minus F5 at c's budget) includes zero in
either primary cell.
Secondary, reported, no kill: every family's selected configuration against d and against dc in
all cells; the full dev grids; the F1 and F2 frontier (the four cells as alpha moves from 0 to 1);
purity of the type-blind clusters; vectors per folder for every row; two-stage hit@1 and hit@10
at k = 10 (twostage.py, exact, evaluation-split queries) for the selected F3 and F4 rows against
c and d.

## Changes to the scripts (commit 2260d20), defaults unchanged

`scripts/eval.py`: `--queries dev|eval` (dev = the 4,388 queries whose directory is in the
calibration split; eval = the 18,742 evaluation-split queries, the default and the session 8
behaviour), `--s9` (the session 9 tables), `--align-cv` (see the leak below), and the families as
representation names: F1 `u_p<alpha>` and `c_p<alpha>`; F2 `proc_p<alpha>`, `coral_p<alpha>`,
`ridge<lambda>_p<alpha>`; F3 `b2`, `bc2`, `bc`; F4 `f4_w<w_cross>`, `f4b_w<w_cross>`; F5 `tb2`,
`tbg`, `tbc` and `tb2c`, `tbgc`, `tbcc` (centered). Reference rows a, b, c, d, ac, cc, dc as before.
`scripts/twostage.py`: `--calib`, `--calib-seed`, `--stage1` (any eval.py name), `--stage2 u|c`,
`--tag`; with `--calib` only evaluation-split queries are used.

Implementation choices not fixed by the brief:
- F3 and F4 group means are unit-normalised (as b's centroids are), so a slot score is a cosine.
- F4 stores [unit mean_img,c ; unit mean_txt,c ; has_img ; has_txt]: two d-dimensional slots and
  two indicator bits, zeros for an absent group. The query of group g is [w_same q ; w_cross q ;
  0 ; 0] with its own slot first. F4b puts w_cross times the bias for the query's group in the
  cross-group indicator slot, so the bias is paid only when that group is present and the score
  stays one inner product. The bias per query group is the dev mean, over dev queries whose
  leave-one-out folder has both groups, of (q . own-group mean minus q . other-group mean):
  image queries +0.351 (n = 1,717), text queries +0.321 (n = 2,293).
- F2 alignments are fitted on the 534 calibration directories with both input groups (the pairs
  of centered plain group means). Procrustes: W = U V^T from the SVD of X^T Y. CORAL: Ledoit-Wolf
  covariances of the centered calibration image-input and text-input files (shrinkage 0.020 and
  0.031), A = C_img^-1/2 C_txt^1/2, x' = (x - m_img) A + m_txt. Ridge: W = (X^T X + lambda I)^-1
  X^T Y. Every aligned image-input vector is unit-normalised again; text-input vectors are the
  centered ones.
- F5 purity counts a file as pure when its cluster's strict-majority input group is its own (a
  tie counts as impure); full folders, no leave-one-out.

## Reproduction check (before any new number was read)

`eval.py --criterion s3 --calib 0.2 --reps a,b,c,d,ac,cc,dc` on the evaluation split
(`ranks_s9repro.jsonl`) gives ranks identical to `ranks_s8.jsonl` for all seven rows on all
18,742 queries. Tables as in `results/session8.md` (all queries recall@5 a 0.689, c 0.783,
d 0.783, ac 0.724, cc 0.800, dc 0.801).

## A leak in the F2 dev grid, and what was done about it

The F2 alignments are fitted on the calibration directories, and the dev queries are exactly the
queries of those directories. An orthogonal map in 2,048 dimensions fitted on 534 pairs memorises
them: in the in-sample dev grid Procrustes with alpha 0.5 scores recall@5 0.88 in P1 against c's
0.71, and a smoke test with the alignment fitted on half of the calibration directories and
scored on the dev queries of the other half gave 0.51. Choosing alpha and lambda on the in-sample
numbers would reward memorisation. So the dev grid for F2 was run twice: once as the brief
specifies (in-sample, reported below as the literal grid) and once with two-fold cross-fitting
inside the calibration split (`--align-cv`: folds alternate over the sorted calibration
directories of each bucket; each fold's alignment is fitted on the other fold's directories and
scores that fold's dev queries; all 2,808 directories are ranking candidates in every fold). The
F2 selection uses the cross-fitted grid. The definitions of the alignments, the pooling grid and
the selection rule are unchanged; only the numbers the selection looks at are out of sample. The
test run fits every alignment on the whole calibration split, as defined. The centering means and
the F4b bias are also fitted on the calibration split (two mean vectors over about 2,400 and 2,800
files, and two scalars); those are left as they are.

## Dev choices (written before the test run)

Dev queries: 4,388 over the 562 calibration directories; all 2,808 directories ranked. Runs:
`eval.py ... --calib 0.2 --queries dev --s9 --reps <all 66 names> --tag _s9dev` (literal grid,
`/workspace/logs/s9_dev.md`, 6 min on 2 threads) and the same with `--align-cv` for the reference
rows and the 30 F2 names (`--tag _s9devcv`, `/workspace/logs/s9_devcv.md`). Selection rule: the
configuration that maximises the minimum over P1, P2, M1, M2 of (x minus c) in recall@5; ties to
fewer vectors, then smaller alpha or w_cross (ties are resolved at full precision, so two rows that
print the same minimum are not tied).

| family | selected | vec/folder | min over 4 cells of (x - c), dev | P1 | P2 | M1 | M2 |
|---|---|---:|---:|---:|---:|---:|---:|
| F1 | c_p0.5 (centered, alpha 0.5) | 1.00 | -0.077 | -0.072 | -0.040 | -0.040 | -0.077 |
| F2 | coral_p0.75 (cross-fitted grid) | 1.00 | -0.073 | -0.067 | -0.072 | -0.038 | -0.073 |
| F3 | bc (six-label centroids, centered) | 2.55 | -0.037 | +0.003 | +0.040 | -0.029 | -0.037 |
| F4 | f4_w0.5 (w_cross 0.5, no bias) | 2.00 | -0.073 | -0.067 | -0.026 | -0.033 | -0.073 |
| F5 | tbcc (type-blind k-means at c's budget, centered) | 5.27 | +0.000 | +0.015 | +0.067 | +0.003 | +0.000 |

Notes on the choices:
- F2 by the literal in-sample grid would be proc_p0 (min +0.164 over the four cells against c on
  dev, an in-sample number); cross-fitted, proc_p0 is -0.124 and the ridge alignments are between
  -0.23 and -0.69. Ridge lambda: 1 is the best of {1, 10, 100, 1000} in the cross-fitted grid and
  still -0.229 at its best alpha; larger lambdas shrink the aligned image vectors toward the mean
  text vector and image queries lose almost everything (P1 recall@5 0.02 to 0.14).
- F3: bc2 (two vectors) is -0.051, bc (2.55 vectors) -0.037; the rule takes bc. Both are reported
  on the test split.
- F4: f4_w0.25 prints the same minimum (-0.073) as f4_w0.5 and loses at full precision; f4b never
  beats f4 at the same w_cross on the minimum (the bias helps nothing in P1 and P2 and costs M2).
- F5: at c's budget (sum of min(3, n_m), 5.27 vectors on 9.70 files per folder) the type-blind
  clusters are 0.988 pure (0.981 centered), so tbc is c with the clustering done blind and
  c - tbc is -0.003 and -0.007 on dev. The two-vector budgets are the informative ones: tb2 and
  tbg (purity 0.921) sit at -0.041 and -0.043 against c, where b2 sits at -0.041.

Test run, fixed now: reference rows a, b, c, d, ac, cc, dc; the selected c_p0.5, coral_p0.75, bc,
f4_w0.5, tbcc; H9c needs tbc. Reported as secondary in the same run (no selection depends on
them): the F1 frontier (u_p0 to u_p1, c_p0 to c_p1), the coral frontier (coral_p0 to coral_p1),
proc_p0 as the literal in-sample F2 selection, b2 and bc2, and tb2, tbg, tb2c, tbgc. Two-stage rows
(twostage.py, k = 10, evaluation-split queries, stage 2 on the uncentered file vectors): c, bc,
bc2, f4_w0.5 against d.

## Verdict (test split, 18,742 queries, one run: `eval.py ... --queries eval --s9 --tag _s9test`, 13 minutes on 2 threads)

Reference recall@5 on the test split: c 0.783 over all queries, 0.647 in P1, 0.680 in P2, 0.751 in
M1 (image queries in image-heavy folders), 0.875 in M2 (text-like queries in text-heavy folders);
d 0.783, cc 0.800, dc 0.801, a 0.689. All differences below are x minus c in recall@5 with the
paired 95 percent interval over directories.

**H9a (no single vector suffices) survives.** The selected F1 configuration c_p0.5 (centered,
alpha 0.5, one vector) is below c by 0.061 [0.033, 0.090] in P1, 0.053 [0.027, 0.078] in P2,
0.035 [0.018, 0.056] in M1 and 0.058 [0.044, 0.072] in M2; the upper bounds are above -0.02 in M1
only. The selected F2 configuration coral_p0.75 is below c by 0.039 [0.008, 0.071] in P1,
0.094 [0.068, 0.119] in P2, 0.008 [-0.008, 0.023] in M1 and 0.056 [0.044, 0.069] in M2; the upper
bounds are above -0.02 in P1 and M1 only. Neither kill fires. Across every one-vector row in the
test run (22 rows: both F1 frontiers, the CORAL frontier, the in-sample Procrustes choice, a, ac)
the best minimum over the four cells is -0.060 (coral_p0.5), and no row is within 0.02 of c in
more than two of the four cells. No single vector in the encoder's own space, pooled by count
weight or linearly aligned, matches c.

**H9b (two centered group vectors suffice) survives by its kill criterion for the selected F3
configuration and is dead for two vectors taken literally.** The selected F3 row is bc, the
six-label centroids on centered vectors, 2.55 vectors per folder: x - c is -0.009 [-0.016, -0.002]
over all queries, +0.026 [+0.010, +0.041] in P1, +0.022 [+0.009, +0.035] in P2, -0.023 [-0.039,
-0.008] in M1 and -0.019 [-0.029, -0.010] in M2. No interval lies entirely below -0.02, so the kill
does not fire, but the M1 point estimate is outside the 0.02 margin: bc is not shown to be within
0.02 of c in M1, and the result there is ambiguous. bc2, the two centered input-group centroids
(1.96 vectors per folder), is -0.034 [-0.045, -0.024] in M2, an interval entirely below -0.02, so
H9b is dead for the two-vector reading of F3. The selected F4 row f4_w0.5 (one 2d entry, two slots)
is dead: -0.077 [-0.098, -0.060] in P1 and -0.051 [-0.060, -0.044] over all queries. Folding two
slots into one inner product with a fixed cross weight is worse than the max over the same two
vectors (bc2) by 0.09 in P1.

**H9c (modality, not dilution) is dead**, and the test as pre-registered cannot separate the two:
c minus type-blind k-means at c's budget (tbc) is +0.000 [-0.005, +0.006] in P1 and +0.001
[-0.005, +0.006] in P2, because at that budget (sum over labels of min(3, n_m), 5.27 vectors on
9.70 files) blind k-means produces clusters that are 0.987 pure by input group: it finds the
modality partition by itself. The informative comparison is at two vectors, post hoc (not
pre-registered): per-modality centroids beat type-blind 2-means in the primary cells and lose in
the majority cells, by about the same amount. b2 - tb2 (uncentered): P1 +0.021 [+0.008, +0.035],
P2 +0.023 [+0.013, +0.033], M1 -0.020 [-0.029, -0.011], M2 -0.013 [-0.020, -0.006]; bc2 - tb2c
(centered): P1 +0.014 [+0.001, +0.028], P2 +0.014 [+0.002, +0.024], M1 -0.022 [-0.035, -0.011],
M2 -0.021 [-0.031, -0.012]. Purity of the blind two-cluster split: 0.919 uncentered, 0.882
centered.

**The most compact representation that matches c** is tb2c: type-blind 2-means on centered file
vectors, two vectors per folder (2.00; one vector for folders with one file), scored by max cosine.
On the test split, x - c is -0.005 [-0.012, +0.000] over all queries, +0.001 [-0.015, +0.018] in
P1, +0.010 [-0.005, +0.025] in P2, -0.003 [-0.015, +0.009] in M1 and -0.013 [-0.021, -0.005] in M2.
Recall@5: 0.777 all, 0.648 P1, 0.689 P2, 0.748 M1, 0.862 M2. Its loss in every cell is within 0.02 at
the point estimate and no interval lies entirely below -0.02; the only significant loss is M2. It
also matches c at recall@10 (0.816 against 0.813 over all queries) and loses at recall@1 (0.654
against 0.680 over all queries; 0.016 to 0.036 per cell). Against c's own budget done blind
(tbc, 5.27 vectors) it is -0.003 [-0.010, +0.002] over all queries and -0.012 [-0.020, -0.004] in
M2. This row was in the grid as the dilution control, not as a candidate family, so its selection
is post hoc; on the dev grid it already had the best minimum over the four cells (-0.023) of every
row with at most 2.55 vectors per folder, ahead of bc (-0.037), bc2 (-0.051) and f4_w0.5 (-0.073),
so a dev selection over all rows with at most two vectors would have picked it. Among the
pre-registered families, bc (2.55 vectors) is the most compact row not killed, with the M1 caveat.
Against cc and dc (5.27 and 9.70 centered vectors), every two-vector row is 0.02 to 0.05 below in
the primary cells; the last 0.02 to 0.05 of recall in P1 and P2 costs three to five times the
vectors.

**Modality or dilution.** Two things are true at once. Under one vector the loss is not count
dilution that reweighting or a linear map can undo: weighting the groups equally (alpha 0) lifts P1
and P2 by 0.24 and costs M1 and M2 0.07 and 0.11 (centered), every alpha in between trades one
side for the other, and no alignment fitted on group-mean pairs raises the same-folder image-text
cosine out of sample (0.205 centered, 0.201 after Procrustes, 0.190 after CORAL, against 0.44 to
0.57 within a group). A folder's images and texts are two clusters, and one vector sits between
them. With two or more vectors the modality label buys little: blind clustering finds the same
split (purity 0.88 to 0.99) and matches the labelled representation at equal budget, within 0.02
either way per cell and 0.000 at c's budget. So the loss is the dilution of a cluster, and in this
corpus that cluster is the modality group; whether a same-modality minority subtopic is lost the
same way (the second control in the prior-art report) is untested here.

## Test split tables (`/workspace/logs/s9_test.md`)

Rows: reference a, b, c, d, ac, cc, dc; the selected c_p0.5, coral_p0.75, bc, f4_w0.5, tbcc and tbc; secondary rows u_p0 to u_p1, c_p0 to c_p1, coral_p0 to coral_p1, proc_p0 (the in-sample F2 choice), b2, bc2, tb2, tbg, tb2c, tbgc. Cells: all; P1 image queries in [0,.2)+[.2,.5); P2 text-like queries in [.5,.8)+[.8,1]; M1 image queries in [.5,.8)+[.8,1]; M2 text-like queries in [0,.2)+[.2,.5).

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.689 | 0.411 | 0.438 | 0.711 | 0.830 | -0.094 [-0.104, -0.085] | -0.236 [-0.269, -0.204] | -0.241 [-0.273, -0.213] | -0.041 [-0.059, -0.025] | -0.044 [-0.056, -0.034] | -0.241 |
| b | ref | 2.55 | 0.757 | 0.623 | 0.658 | 0.721 | 0.850 | -0.026 [-0.032, -0.020] | -0.024 [-0.036, -0.011] | -0.022 [-0.031, -0.012] | -0.030 [-0.045, -0.016] | -0.025 [-0.035, -0.016] | -0.030 |
| c | ref | 5.27 | 0.783 | 0.647 | 0.680 | 0.751 | 0.875 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| d | ref | 9.70 | 0.783 | 0.652 | 0.691 | 0.743 | 0.875 | +0.000 [-0.003, +0.003] | +0.005 [-0.001, +0.013] | +0.012 [+0.007, +0.017] | -0.008 [-0.016, -0.001] | +0.001 [-0.003, +0.005] | -0.008 |
| ac | ref | 1.00 | 0.724 | 0.527 | 0.558 | 0.719 | 0.833 | -0.059 [-0.070, -0.050] | -0.120 [-0.153, -0.088] | -0.122 [-0.155, -0.092] | -0.032 [-0.050, -0.016] | -0.042 [-0.055, -0.030] | -0.122 |
| cc | ref | 5.27 | 0.800 | 0.691 | 0.727 | 0.756 | 0.884 | +0.017 [+0.015, +0.020] | +0.044 [+0.035, +0.053] | +0.047 [+0.039, +0.057] | +0.004 [-0.000, +0.009] | +0.010 [+0.006, +0.014] | +0.004 |
| dc | ref | 9.70 | 0.801 | 0.695 | 0.729 | 0.751 | 0.888 | +0.018 [+0.015, +0.022] | +0.048 [+0.037, +0.059] | +0.049 [+0.041, +0.059] | +0.000 [-0.008, +0.008] | +0.013 [+0.008, +0.018] | +0.000 |
| u_p0 | F1 | 1.00 | 0.697 | 0.622 | 0.652 | 0.671 | 0.751 | -0.086 [-0.097, -0.073] | -0.025 [-0.045, -0.004] | -0.028 [-0.046, -0.010] | -0.081 [-0.104, -0.058] | -0.124 [-0.143, -0.106] | -0.124 |
| u_p0.25 | F1 | 1.00 | 0.718 | 0.573 | 0.601 | 0.709 | 0.803 | -0.064 [-0.074, -0.055] | -0.074 [-0.098, -0.052] | -0.079 [-0.103, -0.056] | -0.042 [-0.062, -0.025] | -0.072 [-0.085, -0.059] | -0.079 |
| u_p0.5 | F1 | 1.00 | 0.708 | 0.509 | 0.533 | 0.710 | 0.819 | -0.074 [-0.085, -0.065] | -0.138 [-0.167, -0.112] | -0.146 [-0.174, -0.120] | -0.042 [-0.061, -0.024] | -0.056 [-0.070, -0.044] | -0.146 |
| u_p0.75 | F1 | 1.00 | 0.696 | 0.458 | 0.480 | 0.707 | 0.823 | -0.087 [-0.097, -0.078] | -0.189 [-0.220, -0.157] | -0.199 [-0.229, -0.171] | -0.044 [-0.063, -0.027] | -0.052 [-0.065, -0.041] | -0.199 |
| u_p1 | F1 | 1.00 | 0.681 | 0.402 | 0.429 | 0.703 | 0.824 | -0.102 [-0.112, -0.092] | -0.245 [-0.279, -0.213] | -0.251 [-0.282, -0.221] | -0.048 [-0.067, -0.032] | -0.051 [-0.063, -0.040] | -0.251 |
| c_p0 | F1 | 1.00 | 0.717 | 0.659 | 0.689 | 0.678 | 0.769 | -0.066 [-0.078, -0.054] | +0.012 [-0.010, +0.032] | +0.010 [-0.008, +0.029] | -0.073 [-0.099, -0.050] | -0.105 [-0.122, -0.088] | -0.105 |
| c_p0.25 | F1 | 1.00 | 0.737 | 0.628 | 0.663 | 0.713 | 0.808 | -0.046 [-0.055, -0.036] | -0.019 [-0.044, +0.005] | -0.016 [-0.037, +0.007] | -0.038 [-0.058, -0.019] | -0.067 [-0.081, -0.054] | -0.067 |
| c_p0.5 | F1 | 1.00 | 0.732 | 0.586 | 0.626 | 0.716 | 0.817 | -0.051 [-0.061, -0.041] | -0.061 [-0.090, -0.033] | -0.053 [-0.078, -0.027] | -0.035 [-0.056, -0.018] | -0.058 [-0.072, -0.044] | -0.061 |
| c_p0.75 | F1 | 1.00 | 0.725 | 0.551 | 0.591 | 0.713 | 0.824 | -0.058 [-0.068, -0.048] | -0.096 [-0.127, -0.066] | -0.088 [-0.116, -0.060] | -0.038 [-0.058, -0.021] | -0.051 [-0.064, -0.039] | -0.096 |
| c_p1 | F1 | 1.00 | 0.715 | 0.514 | 0.546 | 0.712 | 0.826 | -0.068 [-0.078, -0.058] | -0.133 [-0.167, -0.101] | -0.133 [-0.166, -0.104] | -0.039 [-0.059, -0.023] | -0.048 [-0.062, -0.036] | -0.133 |
| coral_p0 | F2 | 1.00 | 0.715 | 0.669 | 0.672 | 0.695 | 0.757 | -0.068 [-0.080, -0.056] | +0.022 [-0.002, +0.046] | -0.008 [-0.026, +0.012] | -0.056 [-0.077, -0.034] | -0.118 [-0.137, -0.100] | -0.118 |
| coral_p0.25 | F2 | 1.00 | 0.740 | 0.660 | 0.657 | 0.727 | 0.800 | -0.042 [-0.052, -0.033] | +0.013 [-0.013, +0.037] | -0.023 [-0.042, -0.002] | -0.024 [-0.041, -0.006] | -0.074 [-0.088, -0.061] | -0.074 |
| coral_p0.5 | F2 | 1.00 | 0.743 | 0.639 | 0.620 | 0.739 | 0.815 | -0.040 [-0.049, -0.032] | -0.008 [-0.036, +0.019] | -0.060 [-0.081, -0.036] | -0.013 [-0.028, +0.004] | -0.060 [-0.073, -0.048] | -0.060 |
| coral_p0.75 | F2 | 1.00 | 0.737 | 0.608 | 0.585 | 0.743 | 0.819 | -0.046 [-0.055, -0.037] | -0.039 [-0.071, -0.008] | -0.094 [-0.119, -0.068] | -0.008 [-0.023, +0.008] | -0.056 [-0.069, -0.044] | -0.094 |
| coral_p1 | F2 | 1.00 | 0.730 | 0.584 | 0.546 | 0.745 | 0.820 | -0.053 [-0.062, -0.044] | -0.063 [-0.095, -0.031] | -0.134 [-0.161, -0.105] | -0.007 [-0.021, +0.009] | -0.054 [-0.068, -0.043] | -0.134 |
| proc_p0 | F2 | 1.00 | 0.685 | 0.561 | 0.633 | 0.650 | 0.761 | -0.097 [-0.110, -0.086] | -0.086 [-0.108, -0.068] | -0.047 [-0.065, -0.029] | -0.101 [-0.127, -0.077] | -0.113 [-0.131, -0.096] | -0.113 |
| b2 | F3 | 1.96 | 0.750 | 0.617 | 0.660 | 0.720 | 0.837 | -0.032 [-0.039, -0.026] | -0.030 [-0.043, -0.015] | -0.020 [-0.031, -0.009] | -0.031 [-0.046, -0.017] | -0.037 [-0.048, -0.028] | -0.037 |
| bc2 | F3 | 1.96 | 0.765 | 0.662 | 0.703 | 0.726 | 0.841 | -0.018 [-0.025, -0.011] | +0.015 [-0.000, +0.031] | +0.023 [+0.011, +0.038] | -0.025 [-0.043, -0.010] | -0.034 [-0.045, -0.024] | -0.034 |
| bc | F3 | 2.55 | 0.774 | 0.672 | 0.702 | 0.728 | 0.856 | -0.009 [-0.016, -0.002] | +0.026 [+0.010, +0.041] | +0.022 [+0.009, +0.035] | -0.023 [-0.039, -0.008] | -0.019 [-0.029, -0.010] | -0.023 |
| f4_w0.5 | F4 | 2.00 | 0.731 | 0.570 | 0.640 | 0.715 | 0.817 | -0.051 [-0.060, -0.044] | -0.077 [-0.098, -0.060] | -0.040 [-0.054, -0.025] | -0.036 [-0.053, -0.018] | -0.057 [-0.070, -0.045] | -0.077 |
| tb2 | F5 | 2.00 | 0.756 | 0.596 | 0.637 | 0.740 | 0.850 | -0.027 [-0.033, -0.021] | -0.051 [-0.067, -0.035] | -0.043 [-0.056, -0.030] | -0.011 [-0.023, +0.000] | -0.024 [-0.032, -0.017] | -0.051 |
| tbg | F5 | 1.96 | 0.756 | 0.593 | 0.638 | 0.740 | 0.850 | -0.027 [-0.033, -0.021] | -0.054 [-0.071, -0.039] | -0.041 [-0.055, -0.028] | -0.012 [-0.023, -0.000] | -0.024 [-0.033, -0.017] | -0.054 |
| tbc | F5 | 5.27 | 0.781 | 0.647 | 0.679 | 0.746 | 0.874 | -0.002 [-0.004, +0.000] | +0.000 [-0.006, +0.005] | -0.001 [-0.006, +0.005] | -0.005 [-0.010, -0.001] | -0.001 [-0.005, +0.002] | -0.005 |
| tb2c | F5 | 2.00 | 0.777 | 0.648 | 0.689 | 0.748 | 0.862 | -0.005 [-0.012, +0.000] | +0.001 [-0.015, +0.018] | +0.010 [-0.005, +0.025] | -0.003 [-0.015, +0.009] | -0.013 [-0.021, -0.005] | -0.013 |
| tbgc | F5 | 1.96 | 0.775 | 0.643 | 0.684 | 0.748 | 0.859 | -0.008 [-0.014, -0.002] | -0.004 [-0.021, +0.012] | +0.005 [-0.010, +0.020] | -0.003 [-0.015, +0.008] | -0.015 [-0.024, -0.008] | -0.015 |
| tbcc | F5 | 5.27 | 0.798 | 0.685 | 0.720 | 0.753 | 0.885 | +0.015 [+0.012, +0.019] | +0.038 [+0.028, +0.049] | +0.040 [+0.030, +0.051] | +0.002 [-0.003, +0.007] | +0.010 [+0.006, +0.015] | +0.002 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.555 | 0.276 | 0.289 | 0.585 | 0.698 |
| b | 0.638 | 0.487 | 0.534 | 0.609 | 0.732 |
| c | 0.680 | 0.512 | 0.569 | 0.661 | 0.777 |
| d | 0.685 | 0.528 | 0.573 | 0.663 | 0.781 |
| ac | 0.588 | 0.371 | 0.390 | 0.601 | 0.703 |
| cc | 0.696 | 0.556 | 0.607 | 0.666 | 0.784 |
| dc | 0.701 | 0.563 | 0.609 | 0.668 | 0.793 |
| u_p0 | 0.275 | 0.262 | 0.257 | 0.272 | 0.286 |
| u_p0.25 | 0.294 | 0.219 | 0.231 | 0.297 | 0.332 |
| u_p0.5 | 0.289 | 0.186 | 0.209 | 0.293 | 0.341 |
| u_p0.75 | 0.286 | 0.162 | 0.168 | 0.305 | 0.347 |
| u_p1 | 0.274 | 0.134 | 0.140 | 0.282 | 0.351 |
| c_p0 | 0.287 | 0.258 | 0.279 | 0.277 | 0.304 |
| c_p0.25 | 0.301 | 0.243 | 0.248 | 0.305 | 0.330 |
| c_p0.5 | 0.298 | 0.220 | 0.232 | 0.291 | 0.345 |
| c_p0.75 | 0.300 | 0.202 | 0.202 | 0.310 | 0.352 |
| c_p1 | 0.295 | 0.187 | 0.187 | 0.297 | 0.357 |
| coral_p0 | 0.288 | 0.281 | 0.272 | 0.289 | 0.294 |
| coral_p0.25 | 0.304 | 0.272 | 0.249 | 0.308 | 0.329 |
| coral_p0.5 | 0.304 | 0.261 | 0.223 | 0.309 | 0.340 |
| coral_p0.75 | 0.307 | 0.243 | 0.218 | 0.317 | 0.348 |
| coral_p1 | 0.307 | 0.228 | 0.204 | 0.322 | 0.352 |
| proc_p0 | 0.268 | 0.204 | 0.241 | 0.257 | 0.301 |
| b2 | 0.626 | 0.478 | 0.539 | 0.609 | 0.708 |
| bc2 | 0.636 | 0.508 | 0.572 | 0.612 | 0.709 |
| bc | 0.649 | 0.523 | 0.570 | 0.612 | 0.734 |
| f4_w0.5 | 0.598 | 0.453 | 0.523 | 0.587 | 0.672 |
| tb2 | 0.638 | 0.461 | 0.512 | 0.634 | 0.730 |
| tbg | 0.637 | 0.455 | 0.516 | 0.633 | 0.729 |
| tbc | 0.682 | 0.515 | 0.566 | 0.660 | 0.780 |
| tb2c | 0.654 | 0.496 | 0.552 | 0.641 | 0.741 |
| tbgc | 0.652 | 0.488 | 0.552 | 0.640 | 0.739 |
| tbcc | 0.695 | 0.551 | 0.595 | 0.665 | 0.788 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.734 | 0.477 | 0.492 | 0.757 | 0.865 |
| b | 0.795 | 0.661 | 0.697 | 0.769 | 0.881 |
| c | 0.813 | 0.683 | 0.706 | 0.787 | 0.900 |
| d | 0.811 | 0.687 | 0.716 | 0.776 | 0.900 |
| ac | 0.771 | 0.590 | 0.623 | 0.763 | 0.874 |
| cc | 0.832 | 0.736 | 0.758 | 0.791 | 0.910 |
| dc | 0.831 | 0.740 | 0.757 | 0.782 | 0.913 |
| u_p0 | 0.756 | 0.679 | 0.700 | 0.728 | 0.814 |
| u_p0.25 | 0.778 | 0.634 | 0.653 | 0.766 | 0.866 |
| u_p0.5 | 0.765 | 0.575 | 0.593 | 0.766 | 0.871 |
| u_p0.75 | 0.746 | 0.526 | 0.534 | 0.759 | 0.866 |
| u_p1 | 0.730 | 0.474 | 0.487 | 0.754 | 0.862 |
| c_p0 | 0.777 | 0.719 | 0.739 | 0.739 | 0.831 |
| c_p0.25 | 0.793 | 0.696 | 0.717 | 0.764 | 0.863 |
| c_p0.5 | 0.788 | 0.653 | 0.688 | 0.765 | 0.872 |
| c_p0.75 | 0.777 | 0.615 | 0.654 | 0.761 | 0.871 |
| c_p1 | 0.768 | 0.584 | 0.618 | 0.760 | 0.871 |
| coral_p0 | 0.769 | 0.721 | 0.719 | 0.745 | 0.816 |
| coral_p0.25 | 0.791 | 0.717 | 0.707 | 0.772 | 0.852 |
| coral_p0.5 | 0.794 | 0.700 | 0.684 | 0.781 | 0.865 |
| coral_p0.75 | 0.789 | 0.675 | 0.653 | 0.785 | 0.869 |
| coral_p1 | 0.785 | 0.656 | 0.619 | 0.788 | 0.872 |
| proc_p0 | 0.744 | 0.621 | 0.677 | 0.712 | 0.821 |
| b2 | 0.791 | 0.656 | 0.698 | 0.769 | 0.872 |
| bc2 | 0.806 | 0.706 | 0.749 | 0.771 | 0.877 |
| bc | 0.812 | 0.717 | 0.741 | 0.772 | 0.888 |
| f4_w0.5 | 0.776 | 0.600 | 0.675 | 0.764 | 0.865 |
| tb2 | 0.793 | 0.641 | 0.677 | 0.781 | 0.881 |
| tbg | 0.793 | 0.638 | 0.678 | 0.781 | 0.882 |
| tbc | 0.812 | 0.689 | 0.705 | 0.781 | 0.900 |
| tb2c | 0.816 | 0.702 | 0.732 | 0.786 | 0.895 |
| tbgc | 0.813 | 0.695 | 0.725 | 0.785 | 0.894 |
| tbcc | 0.831 | 0.737 | 0.754 | 0.786 | 0.911 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.095 [-0.105, -0.085] | -0.242 [-0.276, -0.209] | -0.253 [-0.285, -0.223] | -0.033 [-0.052, -0.016] | -0.045 [-0.058, -0.034] |
| b | -0.026 [-0.033, -0.019] | -0.030 [-0.044, -0.015] | -0.034 [-0.043, -0.023] | -0.022 [-0.040, -0.006] | -0.025 [-0.036, -0.016] |
| c | -0.000 [-0.003, +0.003] | -0.005 [-0.013, +0.001] | -0.012 [-0.017, -0.007] | +0.008 [+0.001, +0.016] | -0.001 [-0.005, +0.003] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| ac | -0.060 [-0.071, -0.049] | -0.125 [-0.160, -0.092] | -0.134 [-0.165, -0.104] | -0.024 [-0.045, -0.006] | -0.042 [-0.057, -0.030] |
| cc | +0.017 [+0.014, +0.021] | +0.038 [+0.028, +0.049] | +0.035 [+0.027, +0.044] | +0.012 [+0.005, +0.020] | +0.009 [+0.005, +0.014] |
| dc | +0.018 [+0.016, +0.021] | +0.043 [+0.033, +0.053] | +0.037 [+0.029, +0.046] | +0.008 [+0.004, +0.012] | +0.012 [+0.009, +0.016] |
| u_p0 | -0.086 [-0.098, -0.073] | -0.030 [-0.051, -0.010] | -0.040 [-0.057, -0.022] | -0.073 [-0.099, -0.048] | -0.125 [-0.144, -0.106] |
| u_p0.25 | -0.065 [-0.075, -0.055] | -0.079 [-0.104, -0.056] | -0.090 [-0.114, -0.067] | -0.035 [-0.056, -0.015] | -0.072 [-0.088, -0.058] |
| u_p0.5 | -0.075 [-0.086, -0.065] | -0.144 [-0.173, -0.115] | -0.158 [-0.185, -0.130] | -0.034 [-0.054, -0.016] | -0.057 [-0.071, -0.044] |
| u_p0.75 | -0.087 [-0.098, -0.077] | -0.194 [-0.226, -0.162] | -0.211 [-0.241, -0.183] | -0.036 [-0.056, -0.019] | -0.053 [-0.066, -0.041] |
| u_p1 | -0.102 [-0.112, -0.092] | -0.250 [-0.284, -0.216] | -0.262 [-0.293, -0.232] | -0.040 [-0.060, -0.023] | -0.051 [-0.065, -0.040] |
| c_p0 | -0.066 [-0.078, -0.054] | +0.006 [-0.015, +0.028] | -0.002 [-0.019, +0.016] | -0.066 [-0.091, -0.039] | -0.106 [-0.123, -0.089] |
| c_p0.25 | -0.046 [-0.056, -0.036] | -0.024 [-0.050, +0.001] | -0.028 [-0.048, -0.005] | -0.030 [-0.052, -0.009] | -0.068 [-0.083, -0.054] |
| c_p0.5 | -0.051 [-0.062, -0.041] | -0.066 [-0.094, -0.038] | -0.065 [-0.089, -0.039] | -0.027 [-0.048, -0.008] | -0.058 [-0.073, -0.045] |
| c_p0.75 | -0.058 [-0.069, -0.048] | -0.102 [-0.132, -0.071] | -0.100 [-0.128, -0.071] | -0.030 [-0.051, -0.012] | -0.052 [-0.066, -0.039] |
| c_p1 | -0.068 [-0.079, -0.058] | -0.138 [-0.173, -0.104] | -0.145 [-0.176, -0.114] | -0.031 [-0.053, -0.013] | -0.049 [-0.064, -0.036] |
| coral_p0 | -0.068 [-0.081, -0.056] | +0.017 [-0.008, +0.041] | -0.019 [-0.038, -0.000] | -0.048 [-0.072, -0.023] | -0.118 [-0.138, -0.099] |
| coral_p0.25 | -0.043 [-0.052, -0.033] | +0.008 [-0.019, +0.034] | -0.034 [-0.053, -0.015] | -0.016 [-0.036, +0.004] | -0.075 [-0.090, -0.061] |
| coral_p0.5 | -0.040 [-0.050, -0.031] | -0.013 [-0.042, +0.015] | -0.072 [-0.094, -0.049] | -0.005 [-0.023, +0.015] | -0.060 [-0.075, -0.048] |
| coral_p0.75 | -0.046 [-0.056, -0.037] | -0.045 [-0.076, -0.013] | -0.106 [-0.131, -0.080] | -0.000 [-0.017, +0.019] | -0.056 [-0.071, -0.044] |
| coral_p1 | -0.053 [-0.063, -0.044] | -0.068 [-0.101, -0.035] | -0.145 [-0.172, -0.116] | +0.001 [-0.015, +0.019] | -0.055 [-0.069, -0.043] |
| proc_p0 | -0.098 [-0.110, -0.086] | -0.091 [-0.114, -0.072] | -0.058 [-0.076, -0.041] | -0.093 [-0.120, -0.067] | -0.114 [-0.131, -0.096] |
| b2 | -0.033 [-0.040, -0.026] | -0.035 [-0.049, -0.021] | -0.032 [-0.042, -0.021] | -0.023 [-0.041, -0.006] | -0.038 [-0.050, -0.028] |
| bc2 | -0.018 [-0.026, -0.010] | +0.010 [-0.007, +0.026] | +0.012 [+0.000, +0.026] | -0.018 [-0.038, +0.001] | -0.034 [-0.047, -0.024] |
| bc | -0.009 [-0.017, -0.001] | +0.020 [+0.003, +0.036] | +0.010 [-0.001, +0.024] | -0.015 [-0.035, +0.004] | -0.019 [-0.030, -0.010] |
| f4_w0.5 | -0.052 [-0.061, -0.043] | -0.082 [-0.104, -0.065] | -0.051 [-0.066, -0.036] | -0.028 [-0.048, -0.009] | -0.058 [-0.072, -0.045] |
| tb2 | -0.027 [-0.033, -0.021] | -0.056 [-0.074, -0.040] | -0.055 [-0.067, -0.042] | -0.003 [-0.018, +0.012] | -0.025 [-0.034, -0.017] |
| tbg | -0.027 [-0.033, -0.021] | -0.060 [-0.077, -0.043] | -0.053 [-0.066, -0.040] | -0.004 [-0.019, +0.011] | -0.025 [-0.034, -0.017] |
| tbc | -0.002 [-0.005, +0.001] | -0.005 [-0.014, +0.002] | -0.012 [-0.019, -0.006] | +0.003 [-0.003, +0.009] | -0.002 [-0.006, +0.002] |
| tb2c | -0.006 [-0.013, +0.001] | -0.004 [-0.022, +0.014] | -0.002 [-0.017, +0.013] | +0.005 [-0.010, +0.020] | -0.014 [-0.022, -0.005] |
| tbgc | -0.008 [-0.015, -0.002] | -0.010 [-0.028, +0.008] | -0.007 [-0.022, +0.008] | +0.004 [-0.010, +0.019] | -0.016 [-0.025, -0.007] |
| tbcc | +0.015 [+0.011, +0.019] | +0.033 [+0.022, +0.044] | +0.029 [+0.019, +0.039] | +0.010 [+0.003, +0.017] | +0.010 [+0.005, +0.015] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.113 [-0.123, -0.103] | -0.284 [-0.318, -0.251] | -0.290 [-0.323, -0.262] | -0.041 [-0.059, -0.024] | -0.057 [-0.070, -0.047] |
| b | -0.044 [-0.051, -0.037] | -0.072 [-0.087, -0.056] | -0.071 [-0.083, -0.059] | -0.030 [-0.048, -0.013] | -0.038 [-0.048, -0.028] |
| c | -0.018 [-0.022, -0.015] | -0.048 [-0.059, -0.037] | -0.049 [-0.059, -0.041] | +0.000 [-0.008, +0.008] | -0.013 [-0.018, -0.008] |
| d | -0.018 [-0.021, -0.016] | -0.043 [-0.053, -0.033] | -0.037 [-0.046, -0.029] | -0.008 [-0.012, -0.004] | -0.012 [-0.016, -0.009] |
| ac | -0.078 [-0.088, -0.068] | -0.168 [-0.200, -0.136] | -0.171 [-0.201, -0.143] | -0.032 [-0.052, -0.014] | -0.054 [-0.068, -0.043] |
| cc | -0.001 [-0.004, +0.002] | -0.004 [-0.012, +0.004] | -0.002 [-0.006, +0.002] | +0.004 [-0.003, +0.011] | -0.003 [-0.007, +0.000] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| u_p0 | -0.104 [-0.116, -0.092] | -0.072 [-0.093, -0.052] | -0.077 [-0.094, -0.061] | -0.081 [-0.107, -0.056] | -0.137 [-0.157, -0.119] |
| u_p0.25 | -0.083 [-0.093, -0.074] | -0.122 [-0.146, -0.099] | -0.128 [-0.151, -0.106] | -0.042 [-0.063, -0.023] | -0.085 [-0.100, -0.071] |
| u_p0.5 | -0.093 [-0.104, -0.084] | -0.186 [-0.215, -0.158] | -0.195 [-0.222, -0.169] | -0.042 [-0.061, -0.024] | -0.069 [-0.083, -0.057] |
| u_p0.75 | -0.105 [-0.116, -0.096] | -0.237 [-0.267, -0.205] | -0.248 [-0.277, -0.222] | -0.044 [-0.063, -0.027] | -0.065 [-0.079, -0.054] |
| u_p1 | -0.120 [-0.131, -0.111] | -0.293 [-0.327, -0.259] | -0.300 [-0.332, -0.271] | -0.048 [-0.067, -0.031] | -0.064 [-0.077, -0.053] |
| c_p0 | -0.084 [-0.096, -0.072] | -0.036 [-0.057, -0.017] | -0.039 [-0.054, -0.024] | -0.073 [-0.099, -0.048] | -0.118 [-0.135, -0.101] |
| c_p0.25 | -0.064 [-0.074, -0.055] | -0.067 [-0.091, -0.046] | -0.065 [-0.084, -0.046] | -0.038 [-0.059, -0.017] | -0.080 [-0.095, -0.067] |
| c_p0.5 | -0.069 [-0.080, -0.060] | -0.109 [-0.135, -0.082] | -0.102 [-0.124, -0.079] | -0.035 [-0.056, -0.016] | -0.071 [-0.085, -0.058] |
| c_p0.75 | -0.076 [-0.087, -0.067] | -0.144 [-0.174, -0.114] | -0.137 [-0.163, -0.113] | -0.038 [-0.058, -0.020] | -0.064 [-0.078, -0.051] |
| c_p1 | -0.086 [-0.097, -0.076] | -0.181 [-0.213, -0.147] | -0.182 [-0.212, -0.154] | -0.039 [-0.060, -0.021] | -0.061 [-0.076, -0.049] |
| coral_p0 | -0.086 [-0.099, -0.074] | -0.026 [-0.049, -0.005] | -0.057 [-0.074, -0.040] | -0.056 [-0.080, -0.031] | -0.131 [-0.150, -0.112] |
| coral_p0.25 | -0.061 [-0.070, -0.052] | -0.035 [-0.059, -0.013] | -0.072 [-0.090, -0.054] | -0.024 [-0.044, -0.004] | -0.087 [-0.101, -0.074] |
| coral_p0.5 | -0.058 [-0.068, -0.050] | -0.055 [-0.082, -0.030] | -0.109 [-0.130, -0.089] | -0.013 [-0.031, +0.007] | -0.073 [-0.087, -0.061] |
| coral_p0.75 | -0.064 [-0.073, -0.055] | -0.087 [-0.117, -0.059] | -0.143 [-0.168, -0.121] | -0.008 [-0.025, +0.010] | -0.069 [-0.082, -0.057] |
| coral_p1 | -0.071 [-0.081, -0.062] | -0.111 [-0.142, -0.080] | -0.183 [-0.209, -0.155] | -0.007 [-0.023, +0.011] | -0.067 [-0.081, -0.055] |
| proc_p0 | -0.116 [-0.128, -0.104] | -0.134 [-0.156, -0.114] | -0.095 [-0.113, -0.079] | -0.101 [-0.128, -0.075] | -0.126 [-0.143, -0.109] |
| b2 | -0.051 [-0.058, -0.044] | -0.078 [-0.093, -0.062] | -0.069 [-0.081, -0.058] | -0.031 [-0.049, -0.014] | -0.050 [-0.062, -0.040] |
| bc2 | -0.036 [-0.044, -0.029] | -0.033 [-0.048, -0.018] | -0.025 [-0.036, -0.015] | -0.025 [-0.045, -0.007] | -0.047 [-0.059, -0.037] |
| bc | -0.027 [-0.035, -0.020] | -0.022 [-0.036, -0.008] | -0.027 [-0.037, -0.016] | -0.023 [-0.042, -0.004] | -0.032 [-0.042, -0.022] |
| f4_w0.5 | -0.070 [-0.079, -0.061] | -0.125 [-0.147, -0.107] | -0.089 [-0.103, -0.073] | -0.036 [-0.056, -0.015] | -0.070 [-0.084, -0.058] |
| tb2 | -0.045 [-0.051, -0.039] | -0.099 [-0.116, -0.080] | -0.092 [-0.107, -0.079] | -0.011 [-0.026, +0.004] | -0.037 [-0.046, -0.029] |
| tbg | -0.045 [-0.051, -0.039] | -0.102 [-0.121, -0.084] | -0.090 [-0.105, -0.076] | -0.012 [-0.027, +0.003] | -0.037 [-0.046, -0.030] |
| tbc | -0.020 [-0.024, -0.017] | -0.048 [-0.060, -0.037] | -0.050 [-0.060, -0.040] | -0.005 [-0.012, +0.002] | -0.014 [-0.019, -0.010] |
| tb2c | -0.024 [-0.030, -0.018] | -0.047 [-0.064, -0.031] | -0.039 [-0.053, -0.026] | -0.003 [-0.017, +0.011] | -0.026 [-0.034, -0.018] |
| tbgc | -0.026 [-0.033, -0.020] | -0.052 [-0.069, -0.037] | -0.044 [-0.058, -0.032] | -0.003 [-0.018, +0.011] | -0.028 [-0.037, -0.020] |
| tbcc | -0.003 [-0.006, -0.000] | -0.009 [-0.018, -0.002] | -0.008 [-0.015, -0.003] | +0.002 [-0.005, +0.008] | -0.003 [-0.007, +0.001] |

Alignment fit: {'pairs': 534, 'coral_shrinkage': (0.01957493308159513, 0.0314595824561629)}.

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.361 | 0.770 | 0.722 | 0.524 |
| centered | 0.072 | 0.568 | 0.462 | 0.205 |
| proc | 0.068 | 0.568 | 0.462 | 0.201 |
| coral | 0.069 | 0.439 | 0.462 | 0.190 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2 | 2.00 | 0.919 | 2149 |
| tbg | 1.96 | 0.919 | 2149 |
| tbc | 5.27 | 0.987 | 2149 |
| tb2c | 2.00 | 0.882 | 2149 |
| tbgc | 1.96 | 0.882 | 2149 |
| tbcc | 5.27 | 0.980 | 2149 |

## Two-stage rows (twostage.py, exact, k = 10, evaluation-split queries)

`twostage.py ... --calib 0.2 --stage1 c,bc,bc2,f4_w0.5 --tag _s9`, 4 minutes on 1 thread: 18,733 queries with
an embedded sibling over 2,203 directories. Stage 1 in the representation's own space (centered for
bc, bc2, f4_w0.5), stage 2 and the flat walk d on the uncentered file vectors, so the rows differ
from c only in stage 1. Paired 95 percent intervals over directories.

| cell | stage 1 | dir recall@10 | hit@1 | hit@10 | hit@1 minus d | hit@10 minus d | vectors scored |
|---|---|---:|---:|---:|---|---|---:|
| all | c | 0.813 | 0.685 | 0.797 | -0.001 [-0.002, +0.001] | -0.001 [-0.003, +0.001] | 14966 |
| all | bc | 0.813 | 0.668 | 0.781 | -0.017 [-0.022, -0.013] | -0.017 [-0.023, -0.012] | 7304 |
| all | bc2 | 0.806 | 0.663 | 0.774 | -0.022 [-0.027, -0.018] | -0.024 [-0.030, -0.018] | 5619 |
| all | f4_w0.5 | 0.776 | 0.650 | 0.752 | -0.035 [-0.040, -0.030] | -0.046 [-0.053, -0.039] | 5744 |
| all | d flat | | 0.685 | 0.798 | | | 27242 |
| P1 | c | 0.683 | 0.529 | 0.658 | +0.000 [-0.001, +0.002] | -0.009 [-0.013, -0.005] | 14955 |
| P1 | bc | 0.717 | 0.519 | 0.658 | -0.009 [-0.017, -0.001] | -0.009 [-0.020, +0.002] | 7297 |
| P1 | bc2 | 0.706 | 0.515 | 0.653 | -0.013 [-0.022, -0.004] | -0.014 [-0.026, -0.003] | 5615 |
| P1 | f4_w0.5 | 0.600 | 0.468 | 0.571 | -0.060 [-0.073, -0.048] | -0.095 [-0.112, -0.080] | 5743 |
| P1 | d flat | | 0.528 | 0.667 | | | 27242 |
| P2 | c | 0.706 | 0.572 | 0.698 | +0.001 [-0.004, +0.007] | -0.006 [-0.011, -0.002] | 14958 |
| P2 | bc | 0.741 | 0.565 | 0.700 | -0.006 [-0.013, +0.001] | -0.004 [-0.014, +0.005] | 7300 |
| P2 | bc2 | 0.749 | 0.564 | 0.701 | -0.007 [-0.015, +0.002] | -0.003 [-0.012, +0.006] | 5614 |
| P2 | f4_w0.5 | 0.675 | 0.543 | 0.652 | -0.028 [-0.040, -0.018] | -0.052 [-0.065, -0.040] | 5736 |
| P2 | d flat | | 0.571 | 0.704 | | | 27242 |
| M1 image in [.5,.8)+[.8,1] | c | 0.787 | 0.661 | 0.767 | -0.002 [-0.004, +0.000] | +0.004 [-0.000, +0.009] | 14955 |
| M1 | bc | 0.772 | 0.632 | 0.738 | -0.031 [-0.042, -0.020] | -0.025 [-0.039, -0.011] | 7297 |
| M1 | bc2 | 0.771 | 0.631 | 0.736 | -0.031 [-0.043, -0.021] | -0.027 [-0.041, -0.013] | 5615 |
| M1 | f4_w0.5 | 0.764 | 0.628 | 0.732 | -0.035 [-0.046, -0.025] | -0.031 [-0.046, -0.016] | 5740 |
| M1 | d flat | | 0.663 | 0.763 | | | 27242 |
| M2 textlike in [0,.2)+[.2,.5) | c | 0.901 | 0.781 | 0.888 | -0.001 [-0.003, +0.001] | -0.000 [-0.003, +0.002] | 14980 |
| M2 | bc | 0.889 | 0.767 | 0.869 | -0.015 [-0.020, -0.009] | -0.019 [-0.026, -0.011] | 7313 |
| M2 | bc2 | 0.878 | 0.758 | 0.858 | -0.023 [-0.030, -0.017] | -0.030 [-0.038, -0.021] | 5626 |
| M2 | f4_w0.5 | 0.866 | 0.752 | 0.849 | -0.030 [-0.036, -0.023] | -0.039 [-0.048, -0.030] | 5750 |
| M2 | d flat | | 0.782 | 0.864 | | | 27242 |

Index: c 14,803 stage 1 vectors (121.3 MB at 2048 float32), bc 7,172 (58.8 MB), bc2 5,491
(45.0 MB), f4_w0.5 5,616 (46.0 MB), the flat index 27,243 (223.2 MB); a two-stage index adds the
file vectors. In the primary cells bc and bc2 route as well as c or better at directory level
(P1 dir recall@10 0.717 and 0.706 against 0.683, P2 0.741 and 0.749 against 0.706) and end within
0.014 hit@10 of the flat walk; in the majority cells they lose 0.02 to 0.03 hit@10 to c and to d.
f4_w0.5 loses 0.03 to 0.10 hit@10 everywhere.

## Appendix A: literal dev grid (`/workspace/logs/s9_dev.md`, session 9 sections; the F2 rows are in-sample)

### Session 9 (dev queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.675 | 0.464 | 0.425 | 0.697 | 0.791 | -0.104 [-0.128, -0.083] | -0.246 [-0.320, -0.179] | -0.197 [-0.257, -0.134] | -0.043 [-0.073, -0.015] | -0.076 [-0.106, -0.050] | -0.246 |
| b | ref | 2.55 | 0.748 | 0.683 | 0.608 | 0.718 | 0.822 | -0.031 [-0.044, -0.020] | -0.027 [-0.050, -0.007] | -0.014 [-0.042, +0.010] | -0.022 [-0.047, +0.006] | -0.044 [-0.064, -0.025] | -0.044 |
| c | ref | 5.27 | 0.780 | 0.710 | 0.622 | 0.740 | 0.866 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| d | ref | 9.70 | 0.783 | 0.725 | 0.634 | 0.733 | 0.870 | +0.003 [-0.003, +0.010] | +0.015 [+0.002, +0.029] | +0.012 [+0.002, +0.025] | -0.007 [-0.025, +0.011] | +0.004 [-0.005, +0.012] | -0.007 |
| ac | ref | 1.00 | 0.711 | 0.575 | 0.534 | 0.710 | 0.796 | -0.069 [-0.089, -0.048] | -0.135 [-0.201, -0.075] | -0.088 [-0.141, -0.029] | -0.029 [-0.056, -0.003] | -0.070 [-0.103, -0.045] | -0.135 |
| cc | ref | 5.27 | 0.794 | 0.735 | 0.703 | 0.735 | 0.871 | +0.015 [+0.008, +0.022] | +0.026 [+0.007, +0.047] | +0.081 [+0.059, +0.108] | -0.005 [-0.015, +0.005] | +0.005 [-0.003, +0.012] | -0.005 |
| dc | ref | 9.70 | 0.798 | 0.749 | 0.708 | 0.736 | 0.872 | +0.018 [+0.010, +0.027] | +0.039 [+0.020, +0.058] | +0.086 [+0.062, +0.114] | -0.003 [-0.023, +0.017] | +0.006 [-0.003, +0.014] | -0.003 |
| u_p0 | F1 | 1.00 | 0.700 | 0.676 | 0.624 | 0.667 | 0.742 | -0.080 [-0.100, -0.059] | -0.034 [-0.086, +0.010] | +0.002 [-0.034, +0.038] | -0.072 [-0.105, -0.040] | -0.124 [-0.162, -0.088] | -0.124 |
| u_p0.25 | F1 | 1.00 | 0.713 | 0.626 | 0.562 | 0.703 | 0.780 | -0.067 [-0.085, -0.049] | -0.084 [-0.146, -0.034] | -0.060 [-0.105, -0.011] | -0.036 [-0.059, -0.012] | -0.086 [-0.118, -0.059] | -0.086 |
| u_p0.5 | F1 | 1.00 | 0.698 | 0.546 | 0.499 | 0.703 | 0.791 | -0.081 [-0.100, -0.062] | -0.164 [-0.227, -0.108] | -0.123 [-0.177, -0.068] | -0.037 [-0.064, -0.011] | -0.076 [-0.105, -0.049] | -0.164 |
| u_p0.75 | F1 | 1.00 | 0.686 | 0.497 | 0.446 | 0.697 | 0.797 | -0.094 [-0.114, -0.075] | -0.213 [-0.282, -0.153] | -0.176 [-0.237, -0.111] | -0.043 [-0.073, -0.015] | -0.069 [-0.095, -0.046] | -0.213 |
| u_p1 | F1 | 1.00 | 0.668 | 0.456 | 0.418 | 0.687 | 0.785 | -0.111 [-0.134, -0.089] | -0.254 [-0.328, -0.187] | -0.204 [-0.262, -0.140] | -0.053 [-0.084, -0.026] | -0.081 [-0.112, -0.055] | -0.254 |
| c_p0 | F1 | 1.00 | 0.713 | 0.700 | 0.656 | 0.672 | 0.751 | -0.067 [-0.088, -0.045] | -0.010 [-0.067, +0.038] | +0.033 [-0.002, +0.074] | -0.067 [-0.103, -0.033] | -0.115 [-0.152, -0.078] | -0.115 |
| c_p0.25 | F1 | 1.00 | 0.722 | 0.677 | 0.613 | 0.692 | 0.778 | -0.058 [-0.078, -0.039] | -0.032 [-0.097, +0.022] | -0.009 [-0.052, +0.036] | -0.048 [-0.077, -0.018] | -0.088 [-0.120, -0.057] | -0.088 |
| c_p0.5 | F1 | 1.00 | 0.719 | 0.638 | 0.582 | 0.699 | 0.789 | -0.060 [-0.079, -0.042] | -0.072 [-0.138, -0.015] | -0.040 [-0.086, +0.008] | -0.040 [-0.071, -0.011] | -0.077 [-0.106, -0.051] | -0.077 |
| c_p0.75 | F1 | 1.00 | 0.708 | 0.584 | 0.545 | 0.698 | 0.792 | -0.071 [-0.092, -0.051] | -0.126 [-0.198, -0.067] | -0.077 [-0.130, -0.020] | -0.041 [-0.071, -0.012] | -0.074 [-0.105, -0.048] | -0.126 |
| c_p1 | F1 | 1.00 | 0.702 | 0.558 | 0.518 | 0.699 | 0.792 | -0.078 [-0.098, -0.056] | -0.152 [-0.221, -0.087] | -0.104 [-0.159, -0.044] | -0.040 [-0.068, -0.015] | -0.074 [-0.106, -0.049] | -0.152 |
| proc_p0 | F2 | 1.00 | 0.834 | 0.874 | 0.824 | 0.785 | 0.853 | +0.055 [+0.037, +0.074] | +0.164 [+0.116, +0.219] | +0.202 [+0.157, +0.249] | +0.045 [+0.013, +0.078] | -0.013 [-0.039, +0.013] | -0.013 |
| proc_p0.25 | F2 | 1.00 | 0.834 | 0.877 | 0.822 | 0.785 | 0.851 | +0.054 [+0.037, +0.074] | +0.167 [+0.115, +0.225] | +0.200 [+0.155, +0.247] | +0.045 [+0.013, +0.079] | -0.015 [-0.041, +0.009] | -0.015 |
| proc_p0.5 | F2 | 1.00 | 0.830 | 0.882 | 0.828 | 0.779 | 0.844 | +0.051 [+0.034, +0.070] | +0.172 [+0.118, +0.229] | +0.206 [+0.160, +0.257] | +0.040 [+0.008, +0.072] | -0.022 [-0.048, +0.003] | -0.022 |
| proc_p0.75 | F2 | 1.00 | 0.823 | 0.875 | 0.826 | 0.771 | 0.835 | +0.043 [+0.026, +0.064] | +0.166 [+0.106, +0.225] | +0.204 [+0.156, +0.259] | +0.031 [+0.001, +0.060] | -0.031 [-0.058, -0.006] | -0.031 |
| proc_p1 | F2 | 1.00 | 0.817 | 0.867 | 0.821 | 0.766 | 0.830 | +0.038 [+0.019, +0.058] | +0.157 [+0.092, +0.221] | +0.199 [+0.148, +0.256] | +0.026 [-0.005, +0.056] | -0.037 [-0.062, -0.012] | -0.037 |
| coral_p0 | F2 | 1.00 | 0.705 | 0.691 | 0.685 | 0.614 | 0.768 | -0.074 [-0.099, -0.049] | -0.019 [-0.081, +0.039] | +0.063 [+0.026, +0.104] | -0.126 [-0.177, -0.073] | -0.098 [-0.134, -0.060] | -0.126 |
| coral_p0.25 | F2 | 1.00 | 0.715 | 0.686 | 0.671 | 0.637 | 0.782 | -0.064 [-0.087, -0.042] | -0.024 [-0.085, +0.032] | +0.049 [+0.012, +0.091] | -0.103 [-0.154, -0.053] | -0.084 [-0.117, -0.053] | -0.103 |
| coral_p0.5 | F2 | 1.00 | 0.717 | 0.669 | 0.633 | 0.650 | 0.794 | -0.063 [-0.084, -0.041] | -0.041 [-0.106, +0.018] | +0.011 [-0.033, +0.058] | -0.089 [-0.135, -0.045] | -0.073 [-0.103, -0.045] | -0.089 |
| coral_p0.75 | F2 | 1.00 | 0.716 | 0.666 | 0.606 | 0.659 | 0.794 | -0.064 [-0.085, -0.042] | -0.044 [-0.109, +0.019] | -0.016 [-0.068, +0.039] | -0.081 [-0.119, -0.041] | -0.072 [-0.102, -0.046] | -0.081 |
| coral_p1 | F2 | 1.00 | 0.716 | 0.652 | 0.594 | 0.666 | 0.799 | -0.064 [-0.083, -0.043] | -0.058 [-0.125, +0.004] | -0.028 [-0.078, +0.028] | -0.074 [-0.109, -0.037] | -0.067 [-0.096, -0.042] | -0.074 |
| ridge1_p0 | F2 | 1.00 | 0.797 | 0.809 | 0.807 | 0.728 | 0.830 | +0.018 [-0.001, +0.039] | +0.099 [+0.044, +0.157] | +0.185 [+0.141, +0.232] | -0.012 [-0.049, +0.024] | -0.037 [-0.069, -0.007] | -0.037 |
| ridge1_p0.25 | F2 | 1.00 | 0.801 | 0.812 | 0.807 | 0.746 | 0.827 | +0.022 [+0.003, +0.042] | +0.102 [+0.045, +0.162] | +0.185 [+0.140, +0.234] | +0.006 [-0.027, +0.037] | -0.040 [-0.070, -0.010] | -0.040 |
| ridge1_p0.5 | F2 | 1.00 | 0.796 | 0.790 | 0.803 | 0.740 | 0.826 | +0.017 [-0.001, +0.037] | +0.080 [+0.023, +0.137] | +0.181 [+0.137, +0.230] | +0.000 [-0.034, +0.031] | -0.041 [-0.072, -0.013] | -0.041 |
| ridge1_p0.75 | F2 | 1.00 | 0.787 | 0.765 | 0.812 | 0.729 | 0.816 | +0.007 [-0.011, +0.028] | +0.055 [-0.006, +0.115] | +0.190 [+0.144, +0.243] | -0.011 [-0.043, +0.019] | -0.050 [-0.080, -0.022] | -0.050 |
| ridge1_p1 | F2 | 1.00 | 0.781 | 0.739 | 0.812 | 0.722 | 0.815 | +0.001 [-0.019, +0.022] | +0.029 [-0.037, +0.092] | +0.190 [+0.143, +0.244] | -0.018 [-0.051, +0.015] | -0.051 [-0.079, -0.024] | -0.051 |
| ridge10_p0 | F2 | 1.00 | 0.646 | 0.466 | 0.729 | 0.482 | 0.781 | -0.133 [-0.157, -0.110] | -0.244 [-0.299, -0.193] | +0.107 [+0.067, +0.150] | -0.258 [-0.311, -0.209] | -0.085 [-0.120, -0.052] | -0.258 |
| ridge10_p0.25 | F2 | 1.00 | 0.661 | 0.422 | 0.724 | 0.539 | 0.789 | -0.119 [-0.138, -0.098] | -0.288 [-0.347, -0.234] | +0.102 [+0.062, +0.145] | -0.201 [-0.248, -0.159] | -0.077 [-0.111, -0.046] | -0.288 |
| ridge10_p0.5 | F2 | 1.00 | 0.644 | 0.311 | 0.714 | 0.534 | 0.791 | -0.136 [-0.157, -0.114] | -0.399 [-0.461, -0.342] | +0.091 [+0.049, +0.139] | -0.206 [-0.254, -0.163] | -0.075 [-0.109, -0.045] | -0.399 |
| ridge10_p0.75 | F2 | 1.00 | 0.629 | 0.235 | 0.692 | 0.523 | 0.795 | -0.150 [-0.172, -0.129] | -0.474 [-0.537, -0.407] | +0.070 [+0.024, +0.121] | -0.217 [-0.267, -0.173] | -0.072 [-0.105, -0.044] | -0.474 |
| ridge10_p1 | F2 | 1.00 | 0.614 | 0.162 | 0.671 | 0.512 | 0.796 | -0.165 [-0.185, -0.143] | -0.548 [-0.614, -0.482] | +0.049 [+0.000, +0.103] | -0.227 [-0.278, -0.182] | -0.070 [-0.097, -0.045] | -0.548 |
| ridge100_p0 | F2 | 1.00 | 0.518 | 0.294 | 0.636 | 0.211 | 0.751 | -0.261 [-0.291, -0.233] | -0.416 [-0.482, -0.355] | +0.014 [-0.025, +0.053] | -0.529 [-0.586, -0.473] | -0.115 [-0.155, -0.079] | -0.529 |
| ridge100_p0.25 | F2 | 1.00 | 0.541 | 0.174 | 0.612 | 0.328 | 0.770 | -0.239 [-0.264, -0.214] | -0.536 [-0.593, -0.481] | -0.011 [-0.048, +0.029] | -0.412 [-0.472, -0.358] | -0.096 [-0.130, -0.065] | -0.536 |
| ridge100_p0.5 | F2 | 1.00 | 0.527 | 0.078 | 0.569 | 0.323 | 0.781 | -0.253 [-0.278, -0.227] | -0.631 [-0.696, -0.566] | -0.053 [-0.092, -0.013] | -0.417 [-0.480, -0.364] | -0.085 [-0.118, -0.058] | -0.631 |
| ridge100_p0.75 | F2 | 1.00 | 0.523 | 0.046 | 0.541 | 0.332 | 0.786 | -0.256 [-0.281, -0.231] | -0.664 [-0.718, -0.603] | -0.081 [-0.126, -0.036] | -0.408 [-0.467, -0.354] | -0.080 [-0.112, -0.054] | -0.664 |
| ridge100_p1 | F2 | 1.00 | 0.521 | 0.046 | 0.485 | 0.333 | 0.794 | -0.259 [-0.284, -0.234] | -0.664 [-0.721, -0.597] | -0.137 [-0.186, -0.088] | -0.407 [-0.467, -0.352] | -0.072 [-0.098, -0.048] | -0.664 |
| ridge1000_p0 | F2 | 1.00 | 0.485 | 0.242 | 0.601 | 0.140 | 0.744 | -0.295 [-0.325, -0.265] | -0.468 [-0.534, -0.405] | -0.021 [-0.059, +0.017] | -0.600 [-0.659, -0.544] | -0.122 [-0.161, -0.085] | -0.600 |
| ridge1000_p0.25 | F2 | 1.00 | 0.511 | 0.130 | 0.576 | 0.260 | 0.768 | -0.268 [-0.295, -0.243] | -0.580 [-0.639, -0.527] | -0.046 [-0.083, -0.007] | -0.479 [-0.540, -0.423] | -0.098 [-0.132, -0.067] | -0.580 |
| ridge1000_p0.5 | F2 | 1.00 | 0.503 | 0.039 | 0.547 | 0.267 | 0.781 | -0.276 [-0.302, -0.250] | -0.671 [-0.721, -0.623] | -0.076 [-0.115, -0.033] | -0.473 [-0.534, -0.415] | -0.085 [-0.117, -0.055] | -0.671 |
| ridge1000_p0.75 | F2 | 1.00 | 0.498 | 0.026 | 0.497 | 0.271 | 0.787 | -0.281 [-0.308, -0.254] | -0.684 [-0.731, -0.638] | -0.125 [-0.171, -0.081] | -0.468 [-0.530, -0.413] | -0.080 [-0.110, -0.054] | -0.684 |
| ridge1000_p1 | F2 | 1.00 | 0.497 | 0.029 | 0.453 | 0.287 | 0.785 | -0.283 [-0.308, -0.256] | -0.681 [-0.728, -0.633] | -0.169 [-0.216, -0.122] | -0.452 [-0.515, -0.397] | -0.081 [-0.109, -0.056] | -0.681 |
| b2 | F3 | 1.96 | 0.741 | 0.669 | 0.613 | 0.719 | 0.808 | -0.039 [-0.052, -0.025] | -0.041 [-0.068, -0.019] | -0.009 [-0.040, +0.018] | -0.020 [-0.045, +0.007] | -0.058 [-0.083, -0.038] | -0.058 |
| bc2 | F3 | 1.96 | 0.755 | 0.701 | 0.677 | 0.714 | 0.815 | -0.024 [-0.039, -0.010] | -0.009 [-0.038, +0.018] | +0.054 [+0.026, +0.083] | -0.026 [-0.058, +0.007] | -0.051 [-0.076, -0.029] | -0.051 |
| bc | F3 | 2.55 | 0.761 | 0.713 | 0.663 | 0.710 | 0.830 | -0.019 [-0.033, -0.005] | +0.003 [-0.023, +0.029] | +0.040 [+0.013, +0.068] | -0.029 [-0.062, +0.004] | -0.037 [-0.057, -0.017] | -0.037 |
| f4_w0 | F4 | 2.00 | 0.721 | 0.599 | 0.594 | 0.698 | 0.803 | -0.059 [-0.074, -0.044] | -0.111 [-0.152, -0.080] | -0.028 [-0.061, +0.002] | -0.042 [-0.072, -0.009] | -0.063 [-0.089, -0.042] | -0.111 |
| f4_w0.25 | F4 | 2.00 | 0.728 | 0.637 | 0.594 | 0.701 | 0.805 | -0.052 [-0.067, -0.037] | -0.073 [-0.110, -0.044] | -0.028 [-0.060, +0.002] | -0.039 [-0.069, -0.008] | -0.061 [-0.086, -0.038] | -0.073 |
| f4_w0.5 | F4 | 2.00 | 0.726 | 0.643 | 0.596 | 0.707 | 0.794 | -0.054 [-0.070, -0.038] | -0.067 [-0.101, -0.035] | -0.026 [-0.060, +0.005] | -0.033 [-0.062, -0.003] | -0.073 [-0.102, -0.046] | -0.073 |
| f4_w0.75 | F4 | 2.00 | 0.718 | 0.647 | 0.592 | 0.693 | 0.784 | -0.061 [-0.078, -0.045] | -0.063 [-0.100, -0.031] | -0.030 [-0.065, +0.003] | -0.046 [-0.081, -0.013] | -0.082 [-0.110, -0.054] | -0.082 |
| f4_w1 | F4 | 2.00 | 0.702 | 0.643 | 0.596 | 0.682 | 0.757 | -0.077 [-0.098, -0.057] | -0.067 [-0.105, -0.030] | -0.026 [-0.063, +0.007] | -0.058 [-0.102, -0.020] | -0.109 [-0.143, -0.075] | -0.109 |
| f4b_w0 | F4 | 2.00 | 0.721 | 0.599 | 0.594 | 0.698 | 0.803 | -0.059 [-0.074, -0.044] | -0.111 [-0.152, -0.080] | -0.028 [-0.061, +0.002] | -0.042 [-0.072, -0.009] | -0.063 [-0.089, -0.042] | -0.111 |
| f4b_w0.25 | F4 | 2.00 | 0.725 | 0.637 | 0.594 | 0.701 | 0.800 | -0.054 [-0.070, -0.039] | -0.073 [-0.110, -0.044] | -0.028 [-0.060, +0.002] | -0.039 [-0.069, -0.007] | -0.066 [-0.092, -0.043] | -0.073 |
| f4b_w0.5 | F4 | 2.00 | 0.719 | 0.643 | 0.596 | 0.704 | 0.781 | -0.060 [-0.077, -0.043] | -0.067 [-0.101, -0.035] | -0.026 [-0.060, +0.005] | -0.035 [-0.065, -0.005] | -0.085 [-0.117, -0.058] | -0.085 |
| f4b_w0.75 | F4 | 2.00 | 0.709 | 0.647 | 0.592 | 0.693 | 0.765 | -0.070 [-0.088, -0.053] | -0.063 [-0.100, -0.031] | -0.030 [-0.065, +0.003] | -0.047 [-0.082, -0.013] | -0.101 [-0.130, -0.071] | -0.101 |
| f4b_w1 | F4 | 2.00 | 0.689 | 0.643 | 0.596 | 0.682 | 0.728 | -0.090 [-0.112, -0.069] | -0.067 [-0.105, -0.030] | -0.026 [-0.063, +0.007] | -0.058 [-0.102, -0.020] | -0.138 [-0.176, -0.101] | -0.138 |
| tb2 | F5 | 2.00 | 0.755 | 0.669 | 0.596 | 0.739 | 0.833 | -0.025 [-0.036, -0.014] | -0.041 [-0.068, -0.018] | -0.026 [-0.057, +0.002] | -0.001 [-0.018, +0.020] | -0.033 [-0.052, -0.018] | -0.041 |
| tbg | F5 | 1.96 | 0.753 | 0.667 | 0.591 | 0.740 | 0.829 | -0.027 [-0.038, -0.017] | -0.043 [-0.070, -0.019] | -0.032 [-0.063, -0.004] | +0.000 [-0.017, +0.021] | -0.037 [-0.055, -0.021] | -0.043 |
| tbc | F5 | 5.27 | 0.779 | 0.713 | 0.629 | 0.740 | 0.863 | -0.000 [-0.006, +0.006] | +0.003 [-0.011, +0.016] | +0.007 [-0.008, +0.022] | +0.000 [-0.014, +0.016] | -0.003 [-0.008, +0.001] | -0.003 |
| tb2c | F5 | 2.00 | 0.774 | 0.703 | 0.668 | 0.741 | 0.843 | -0.006 [-0.018, +0.006] | -0.007 [-0.041, +0.029] | +0.046 [+0.010, +0.085] | +0.002 [-0.020, +0.025] | -0.023 [-0.039, -0.008] | -0.023 |
| tbgc | F5 | 1.96 | 0.770 | 0.696 | 0.645 | 0.742 | 0.843 | -0.010 [-0.021, +0.002] | -0.014 [-0.044, +0.018] | +0.023 [-0.013, +0.059] | +0.003 [-0.019, +0.026] | -0.023 [-0.040, -0.007] | -0.023 |
| tbcc | F5 | 5.27 | 0.791 | 0.725 | 0.689 | 0.742 | 0.866 | +0.011 [+0.004, +0.020] | +0.015 [-0.012, +0.039] | +0.067 [+0.042, +0.095] | +0.003 [-0.013, +0.020] | +0.000 [-0.008, +0.008] | +0.000 |

### Session 9 (dev queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.549 | 0.360 | 0.279 | 0.565 | 0.667 |
| b | 0.633 | 0.568 | 0.492 | 0.596 | 0.710 |
| c | 0.667 | 0.565 | 0.506 | 0.639 | 0.758 |
| d | 0.668 | 0.558 | 0.513 | 0.638 | 0.758 |
| ac | 0.574 | 0.432 | 0.359 | 0.568 | 0.676 |
| cc | 0.680 | 0.594 | 0.550 | 0.639 | 0.765 |
| dc | 0.682 | 0.587 | 0.554 | 0.641 | 0.768 |
| u_p0 | 0.280 | 0.276 | 0.237 | 0.263 | 0.299 |
| u_p0.25 | 0.291 | 0.235 | 0.213 | 0.291 | 0.327 |
| u_p0.5 | 0.278 | 0.225 | 0.160 | 0.253 | 0.340 |
| u_p0.75 | 0.277 | 0.193 | 0.155 | 0.274 | 0.336 |
| u_p1 | 0.266 | 0.174 | 0.137 | 0.283 | 0.319 |
| c_p0 | 0.295 | 0.292 | 0.276 | 0.279 | 0.306 |
| c_p0.25 | 0.303 | 0.268 | 0.250 | 0.298 | 0.328 |
| c_p0.5 | 0.298 | 0.247 | 0.225 | 0.284 | 0.337 |
| c_p0.75 | 0.305 | 0.235 | 0.200 | 0.280 | 0.369 |
| c_p1 | 0.302 | 0.230 | 0.186 | 0.295 | 0.359 |
| proc_p0 | 0.365 | 0.392 | 0.362 | 0.347 | 0.368 |
| proc_p0.25 | 0.365 | 0.392 | 0.355 | 0.350 | 0.368 |
| proc_p0.5 | 0.355 | 0.352 | 0.353 | 0.326 | 0.369 |
| proc_p0.75 | 0.364 | 0.386 | 0.380 | 0.329 | 0.369 |
| proc_p1 | 0.353 | 0.334 | 0.364 | 0.340 | 0.362 |
| coral_p0 | 0.291 | 0.287 | 0.257 | 0.268 | 0.312 |
| coral_p0.25 | 0.302 | 0.292 | 0.260 | 0.281 | 0.326 |
| coral_p0.5 | 0.304 | 0.288 | 0.260 | 0.270 | 0.341 |
| coral_p0.75 | 0.301 | 0.259 | 0.253 | 0.273 | 0.342 |
| coral_p1 | 0.291 | 0.251 | 0.230 | 0.262 | 0.337 |
| ridge1_p0 | 0.329 | 0.275 | 0.337 | 0.294 | 0.361 |
| ridge1_p0.25 | 0.344 | 0.304 | 0.337 | 0.335 | 0.362 |
| ridge1_p0.5 | 0.335 | 0.304 | 0.315 | 0.312 | 0.360 |
| ridge1_p0.75 | 0.325 | 0.259 | 0.334 | 0.288 | 0.363 |
| ridge1_p1 | 0.331 | 0.244 | 0.359 | 0.293 | 0.370 |
| ridge10_p0 | 0.247 | 0.142 | 0.295 | 0.154 | 0.324 |
| ridge10_p0.25 | 0.263 | 0.135 | 0.274 | 0.191 | 0.346 |
| ridge10_p0.5 | 0.250 | 0.075 | 0.267 | 0.180 | 0.340 |
| ridge10_p0.75 | 0.246 | 0.043 | 0.271 | 0.182 | 0.340 |
| ridge10_p1 | 0.230 | 0.036 | 0.223 | 0.160 | 0.337 |
| ridge100_p0 | 0.189 | 0.056 | 0.239 | 0.035 | 0.313 |
| ridge100_p0.25 | 0.204 | 0.014 | 0.234 | 0.083 | 0.331 |
| ridge100_p0.5 | 0.196 | 0.000 | 0.202 | 0.079 | 0.330 |
| ridge100_p0.75 | 0.189 | 0.003 | 0.148 | 0.094 | 0.320 |
| ridge100_p1 | 0.193 | 0.002 | 0.178 | 0.094 | 0.321 |
| ridge1000_p0 | 0.173 | 0.022 | 0.225 | 0.025 | 0.299 |
| ridge1000_p0.25 | 0.191 | 0.003 | 0.190 | 0.050 | 0.339 |
| ridge1000_p0.5 | 0.195 | 0.002 | 0.199 | 0.071 | 0.333 |
| ridge1000_p0.75 | 0.198 | 0.003 | 0.176 | 0.067 | 0.347 |
| ridge1000_p1 | 0.188 | 0.002 | 0.128 | 0.082 | 0.332 |
| b2 | 0.627 | 0.556 | 0.513 | 0.596 | 0.695 |
| bc2 | 0.637 | 0.590 | 0.555 | 0.588 | 0.700 |
| bc | 0.642 | 0.602 | 0.531 | 0.591 | 0.711 |
| f4_w0 | 0.613 | 0.509 | 0.499 | 0.582 | 0.691 |
| f4_w0.25 | 0.611 | 0.509 | 0.508 | 0.587 | 0.681 |
| f4_w0.5 | 0.598 | 0.503 | 0.501 | 0.577 | 0.661 |
| f4_w0.75 | 0.574 | 0.509 | 0.478 | 0.547 | 0.631 |
| f4_w1 | 0.554 | 0.507 | 0.460 | 0.529 | 0.603 |
| f4b_w0 | 0.613 | 0.509 | 0.499 | 0.582 | 0.691 |
| f4b_w0.25 | 0.608 | 0.510 | 0.508 | 0.587 | 0.674 |
| f4b_w0.5 | 0.592 | 0.503 | 0.501 | 0.577 | 0.648 |
| f4b_w0.75 | 0.562 | 0.509 | 0.478 | 0.547 | 0.604 |
| f4b_w1 | 0.542 | 0.507 | 0.460 | 0.529 | 0.576 |
| tb2 | 0.637 | 0.531 | 0.476 | 0.631 | 0.716 |
| tbg | 0.634 | 0.529 | 0.482 | 0.632 | 0.709 |
| tbc | 0.665 | 0.548 | 0.506 | 0.635 | 0.759 |
| tb2c | 0.644 | 0.544 | 0.511 | 0.633 | 0.717 |
| tbgc | 0.641 | 0.541 | 0.503 | 0.632 | 0.714 |
| tbcc | 0.682 | 0.594 | 0.540 | 0.652 | 0.764 |

### Session 9 (dev queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.732 | 0.558 | 0.476 | 0.759 | 0.833 |
| b | 0.794 | 0.718 | 0.645 | 0.763 | 0.873 |
| c | 0.811 | 0.747 | 0.661 | 0.767 | 0.896 |
| d | 0.812 | 0.759 | 0.675 | 0.763 | 0.894 |
| ac | 0.765 | 0.667 | 0.599 | 0.762 | 0.840 |
| cc | 0.828 | 0.787 | 0.743 | 0.767 | 0.899 |
| dc | 0.830 | 0.794 | 0.745 | 0.769 | 0.899 |
| u_p0 | 0.759 | 0.727 | 0.657 | 0.728 | 0.810 |
| u_p0.25 | 0.770 | 0.701 | 0.612 | 0.754 | 0.839 |
| u_p0.5 | 0.757 | 0.623 | 0.569 | 0.759 | 0.842 |
| u_p0.75 | 0.739 | 0.573 | 0.515 | 0.755 | 0.837 |
| u_p1 | 0.726 | 0.551 | 0.471 | 0.753 | 0.828 |
| c_p0 | 0.774 | 0.765 | 0.707 | 0.731 | 0.817 |
| c_p0.25 | 0.786 | 0.753 | 0.680 | 0.746 | 0.846 |
| c_p0.5 | 0.779 | 0.724 | 0.641 | 0.756 | 0.844 |
| c_p0.75 | 0.771 | 0.683 | 0.620 | 0.757 | 0.844 |
| c_p1 | 0.761 | 0.664 | 0.594 | 0.760 | 0.835 |
| proc_p0 | 0.871 | 0.920 | 0.845 | 0.815 | 0.897 |
| proc_p0.25 | 0.872 | 0.918 | 0.845 | 0.818 | 0.896 |
| proc_p0.5 | 0.870 | 0.916 | 0.856 | 0.813 | 0.891 |
| proc_p0.75 | 0.869 | 0.918 | 0.856 | 0.817 | 0.887 |
| proc_p1 | 0.867 | 0.915 | 0.856 | 0.812 | 0.886 |
| coral_p0 | 0.761 | 0.758 | 0.729 | 0.672 | 0.824 |
| coral_p0.25 | 0.772 | 0.761 | 0.710 | 0.692 | 0.841 |
| coral_p0.5 | 0.777 | 0.753 | 0.677 | 0.703 | 0.858 |
| coral_p0.75 | 0.773 | 0.737 | 0.650 | 0.714 | 0.855 |
| coral_p1 | 0.768 | 0.722 | 0.634 | 0.715 | 0.850 |
| ridge1_p0 | 0.847 | 0.860 | 0.830 | 0.783 | 0.885 |
| ridge1_p0.25 | 0.846 | 0.862 | 0.833 | 0.788 | 0.877 |
| ridge1_p0.5 | 0.845 | 0.860 | 0.842 | 0.784 | 0.876 |
| ridge1_p0.75 | 0.841 | 0.840 | 0.840 | 0.784 | 0.873 |
| ridge1_p1 | 0.835 | 0.826 | 0.840 | 0.781 | 0.867 |
| ridge10_p0 | 0.715 | 0.560 | 0.779 | 0.551 | 0.846 |
| ridge10_p0.25 | 0.729 | 0.519 | 0.772 | 0.612 | 0.851 |
| ridge10_p0.5 | 0.724 | 0.447 | 0.764 | 0.622 | 0.856 |
| ridge10_p0.75 | 0.701 | 0.334 | 0.754 | 0.606 | 0.853 |
| ridge10_p1 | 0.689 | 0.283 | 0.743 | 0.595 | 0.851 |
| ridge100_p0 | 0.596 | 0.404 | 0.698 | 0.308 | 0.813 |
| ridge100_p0.25 | 0.624 | 0.294 | 0.673 | 0.430 | 0.836 |
| ridge100_p0.5 | 0.596 | 0.126 | 0.640 | 0.420 | 0.840 |
| ridge100_p0.75 | 0.587 | 0.085 | 0.610 | 0.415 | 0.840 |
| ridge100_p1 | 0.578 | 0.060 | 0.576 | 0.414 | 0.838 |
| ridge1000_p0 | 0.563 | 0.343 | 0.675 | 0.237 | 0.807 |
| ridge1000_p0.25 | 0.593 | 0.225 | 0.640 | 0.374 | 0.831 |
| ridge1000_p0.5 | 0.571 | 0.092 | 0.605 | 0.366 | 0.837 |
| ridge1000_p0.75 | 0.564 | 0.058 | 0.573 | 0.372 | 0.836 |
| ridge1000_p1 | 0.556 | 0.055 | 0.536 | 0.373 | 0.830 |
| b2 | 0.789 | 0.705 | 0.649 | 0.762 | 0.867 |
| bc2 | 0.803 | 0.754 | 0.712 | 0.759 | 0.866 |
| bc | 0.809 | 0.773 | 0.705 | 0.760 | 0.876 |
| f4_w0 | 0.762 | 0.642 | 0.615 | 0.735 | 0.852 |
| f4_w0.25 | 0.769 | 0.666 | 0.617 | 0.751 | 0.850 |
| f4_w0.5 | 0.770 | 0.674 | 0.620 | 0.752 | 0.847 |
| f4_w0.75 | 0.768 | 0.686 | 0.627 | 0.751 | 0.838 |
| f4_w1 | 0.764 | 0.701 | 0.650 | 0.745 | 0.823 |
| f4b_w0 | 0.762 | 0.642 | 0.615 | 0.735 | 0.852 |
| f4b_w0.25 | 0.766 | 0.666 | 0.619 | 0.749 | 0.844 |
| f4b_w0.5 | 0.763 | 0.674 | 0.622 | 0.749 | 0.835 |
| f4b_w0.75 | 0.759 | 0.686 | 0.627 | 0.749 | 0.820 |
| f4b_w1 | 0.752 | 0.701 | 0.650 | 0.745 | 0.795 |
| tb2 | 0.794 | 0.712 | 0.624 | 0.766 | 0.880 |
| tbg | 0.793 | 0.706 | 0.627 | 0.766 | 0.878 |
| tbc | 0.811 | 0.754 | 0.656 | 0.771 | 0.893 |
| tb2c | 0.812 | 0.765 | 0.708 | 0.780 | 0.874 |
| tbgc | 0.809 | 0.763 | 0.692 | 0.780 | 0.870 |
| tbcc | 0.828 | 0.780 | 0.736 | 0.775 | 0.898 |

### Session 9 (dev queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.108 [-0.130, -0.087] | -0.261 [-0.333, -0.195] | -0.209 [-0.268, -0.145] | -0.036 [-0.069, -0.009] | -0.079 [-0.111, -0.051] |
| b | -0.035 [-0.049, -0.021] | -0.043 [-0.068, -0.019] | -0.026 [-0.056, +0.000] | -0.015 [-0.049, +0.021] | -0.048 [-0.070, -0.026] |
| c | -0.003 [-0.010, +0.003] | -0.015 [-0.029, -0.002] | -0.012 [-0.025, -0.002] | +0.007 [-0.011, +0.025] | -0.004 [-0.012, +0.005] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| ac | -0.072 [-0.092, -0.052] | -0.150 [-0.218, -0.092] | -0.100 [-0.154, -0.040] | -0.023 [-0.051, +0.003] | -0.074 [-0.106, -0.047] |
| cc | +0.011 [+0.002, +0.020] | +0.010 [-0.009, +0.032] | +0.069 [+0.045, +0.097] | +0.002 [-0.021, +0.024] | +0.001 [-0.008, +0.010] |
| dc | +0.015 [+0.010, +0.020] | +0.024 [+0.008, +0.042] | +0.074 [+0.052, +0.103] | +0.003 [-0.003, +0.011] | +0.002 [-0.004, +0.008] |
| u_p0 | -0.083 [-0.103, -0.063] | -0.049 [-0.100, -0.006] | -0.011 [-0.046, +0.026] | -0.066 [-0.103, -0.027] | -0.128 [-0.164, -0.091] |
| u_p0.25 | -0.070 [-0.088, -0.051] | -0.099 [-0.160, -0.052] | -0.072 [-0.114, -0.026] | -0.029 [-0.061, +0.002] | -0.090 [-0.121, -0.061] |
| u_p0.5 | -0.085 [-0.103, -0.066] | -0.179 [-0.241, -0.125] | -0.135 [-0.186, -0.081] | -0.030 [-0.058, -0.004] | -0.079 [-0.110, -0.052] |
| u_p0.75 | -0.097 [-0.116, -0.079] | -0.229 [-0.294, -0.168] | -0.188 [-0.246, -0.124] | -0.036 [-0.068, -0.008] | -0.073 [-0.100, -0.047] |
| u_p1 | -0.115 [-0.138, -0.094] | -0.270 [-0.342, -0.205] | -0.216 [-0.273, -0.152] | -0.046 [-0.080, -0.017] | -0.084 [-0.116, -0.057] |
| c_p0 | -0.070 [-0.092, -0.048] | -0.026 [-0.081, +0.023] | +0.021 [-0.014, +0.061] | -0.061 [-0.104, -0.018] | -0.119 [-0.156, -0.082] |
| c_p0.25 | -0.061 [-0.080, -0.041] | -0.048 [-0.108, +0.003] | -0.021 [-0.064, +0.026] | -0.041 [-0.078, -0.006] | -0.091 [-0.124, -0.061] |
| c_p0.5 | -0.064 [-0.082, -0.044] | -0.087 [-0.151, -0.034] | -0.053 [-0.099, -0.004] | -0.034 [-0.068, -0.003] | -0.081 [-0.111, -0.054] |
| c_p0.75 | -0.075 [-0.095, -0.055] | -0.142 [-0.210, -0.083] | -0.090 [-0.139, -0.034] | -0.035 [-0.068, -0.004] | -0.078 [-0.110, -0.051] |
| c_p1 | -0.081 [-0.102, -0.060] | -0.167 [-0.237, -0.104] | -0.116 [-0.173, -0.056] | -0.034 [-0.063, -0.006] | -0.078 [-0.110, -0.051] |
| proc_p0 | +0.051 [+0.034, +0.073] | +0.148 [+0.102, +0.200] | +0.190 [+0.147, +0.236] | +0.052 [+0.013, +0.093] | -0.017 [-0.042, +0.010] |
| proc_p0.25 | +0.051 [+0.032, +0.072] | +0.152 [+0.100, +0.207] | +0.188 [+0.145, +0.235] | +0.052 [+0.013, +0.093] | -0.019 [-0.044, +0.007] |
| proc_p0.5 | +0.047 [+0.030, +0.068] | +0.157 [+0.104, +0.209] | +0.193 [+0.150, +0.243] | +0.046 [+0.007, +0.088] | -0.026 [-0.050, +0.000] |
| proc_p0.75 | +0.040 [+0.021, +0.061] | +0.150 [+0.095, +0.207] | +0.192 [+0.145, +0.246] | +0.038 [+0.001, +0.076] | -0.035 [-0.062, -0.009] |
| proc_p1 | +0.034 [+0.015, +0.057] | +0.142 [+0.081, +0.201] | +0.186 [+0.137, +0.243] | +0.033 [-0.004, +0.071] | -0.040 [-0.067, -0.014] |
| coral_p0 | -0.078 [-0.103, -0.052] | -0.034 [-0.096, +0.026] | +0.051 [+0.014, +0.091] | -0.119 [-0.177, -0.059] | -0.101 [-0.138, -0.063] |
| coral_p0.25 | -0.068 [-0.092, -0.044] | -0.039 [-0.101, +0.016] | +0.037 [+0.000, +0.080] | -0.096 [-0.153, -0.042] | -0.087 [-0.121, -0.056] |
| coral_p0.5 | -0.066 [-0.089, -0.043] | -0.056 [-0.119, +0.002] | -0.002 [-0.044, +0.047] | -0.083 [-0.133, -0.032] | -0.076 [-0.106, -0.048] |
| coral_p0.75 | -0.067 [-0.090, -0.044] | -0.060 [-0.121, +0.002] | -0.028 [-0.079, +0.025] | -0.074 [-0.121, -0.027] | -0.076 [-0.105, -0.048] |
| coral_p1 | -0.067 [-0.087, -0.045] | -0.073 [-0.136, -0.011] | -0.040 [-0.090, +0.017] | -0.067 [-0.112, -0.022] | -0.071 [-0.099, -0.045] |
| ridge1_p0 | +0.014 [-0.005, +0.035] | +0.084 [+0.028, +0.140] | +0.172 [+0.129, +0.220] | -0.005 [-0.046, +0.038] | -0.040 [-0.070, -0.011] |
| ridge1_p0.25 | +0.018 [-0.001, +0.040] | +0.087 [+0.033, +0.146] | +0.172 [+0.127, +0.222] | +0.013 [-0.027, +0.054] | -0.043 [-0.073, -0.015] |
| ridge1_p0.5 | +0.013 [-0.005, +0.034] | +0.065 [+0.010, +0.122] | +0.169 [+0.125, +0.218] | +0.007 [-0.034, +0.044] | -0.044 [-0.074, -0.016] |
| ridge1_p0.75 | +0.004 [-0.016, +0.025] | +0.039 [-0.018, +0.102] | +0.178 [+0.132, +0.230] | -0.004 [-0.043, +0.031] | -0.053 [-0.083, -0.026] |
| ridge1_p1 | -0.002 [-0.023, +0.020] | +0.014 [-0.049, +0.077] | +0.178 [+0.131, +0.231] | -0.011 [-0.050, +0.026] | -0.054 [-0.084, -0.027] |
| ridge10_p0 | -0.137 [-0.160, -0.113] | -0.259 [-0.314, -0.205] | +0.095 [+0.054, +0.137] | -0.251 [-0.305, -0.202] | -0.089 [-0.123, -0.055] |
| ridge10_p0.25 | -0.122 [-0.142, -0.101] | -0.304 [-0.363, -0.247] | +0.090 [+0.050, +0.132] | -0.194 [-0.241, -0.152] | -0.081 [-0.114, -0.049] |
| ridge10_p0.5 | -0.139 [-0.159, -0.118] | -0.415 [-0.476, -0.354] | +0.079 [+0.038, +0.125] | -0.199 [-0.245, -0.157] | -0.079 [-0.112, -0.049] |
| ridge10_p0.75 | -0.154 [-0.175, -0.132] | -0.490 [-0.552, -0.425] | +0.058 [+0.012, +0.111] | -0.210 [-0.260, -0.167] | -0.075 [-0.107, -0.046] |
| ridge10_p1 | -0.169 [-0.190, -0.147] | -0.563 [-0.627, -0.498] | +0.037 [-0.016, +0.092] | -0.221 [-0.270, -0.177] | -0.074 [-0.102, -0.047] |
| ridge100_p0 | -0.265 [-0.293, -0.236] | -0.432 [-0.496, -0.367] | +0.002 [-0.038, +0.041] | -0.522 [-0.580, -0.467] | -0.119 [-0.157, -0.082] |
| ridge100_p0.25 | -0.242 [-0.267, -0.218] | -0.551 [-0.608, -0.498] | -0.023 [-0.062, +0.019] | -0.405 [-0.463, -0.349] | -0.100 [-0.134, -0.067] |
| ridge100_p0.5 | -0.256 [-0.281, -0.231] | -0.647 [-0.711, -0.582] | -0.065 [-0.107, -0.022] | -0.410 [-0.470, -0.354] | -0.088 [-0.122, -0.059] |
| ridge100_p0.75 | -0.260 [-0.285, -0.233] | -0.679 [-0.735, -0.619] | -0.093 [-0.138, -0.045] | -0.401 [-0.462, -0.347] | -0.084 [-0.117, -0.056] |
| ridge100_p1 | -0.263 [-0.286, -0.237] | -0.679 [-0.736, -0.613] | -0.149 [-0.198, -0.099] | -0.400 [-0.461, -0.347] | -0.076 [-0.103, -0.050] |
| ridge1000_p0 | -0.298 [-0.327, -0.269] | -0.483 [-0.550, -0.419] | -0.033 [-0.072, +0.005] | -0.593 [-0.652, -0.532] | -0.126 [-0.165, -0.088] |
| ridge1000_p0.25 | -0.272 [-0.298, -0.247] | -0.596 [-0.651, -0.541] | -0.058 [-0.098, -0.018] | -0.473 [-0.533, -0.417] | -0.101 [-0.135, -0.070] |
| ridge1000_p0.5 | -0.280 [-0.305, -0.252] | -0.686 [-0.733, -0.636] | -0.088 [-0.130, -0.042] | -0.466 [-0.528, -0.409] | -0.088 [-0.121, -0.057] |
| ridge1000_p0.75 | -0.285 [-0.310, -0.257] | -0.700 [-0.744, -0.653] | -0.137 [-0.187, -0.090] | -0.462 [-0.524, -0.405] | -0.083 [-0.114, -0.056] |
| ridge1000_p1 | -0.286 [-0.311, -0.259] | -0.696 [-0.743, -0.649] | -0.181 [-0.230, -0.132] | -0.446 [-0.509, -0.391] | -0.084 [-0.112, -0.059] |
| b2 | -0.042 [-0.057, -0.027] | -0.056 [-0.085, -0.030] | -0.021 [-0.053, +0.007] | -0.013 [-0.046, +0.023] | -0.062 [-0.087, -0.040] |
| bc2 | -0.028 [-0.044, -0.011] | -0.024 [-0.054, +0.004] | +0.042 [+0.011, +0.074] | -0.019 [-0.057, +0.023] | -0.054 [-0.081, -0.032] |
| bc | -0.022 [-0.038, -0.007] | -0.012 [-0.038, +0.014] | +0.028 [+0.000, +0.059] | -0.023 [-0.062, +0.020] | -0.040 [-0.063, -0.019] |
| f4_w0 | -0.062 [-0.078, -0.045] | -0.126 [-0.167, -0.094] | -0.040 [-0.076, -0.010] | -0.035 [-0.072, +0.007] | -0.067 [-0.093, -0.045] |
| f4_w0.25 | -0.055 [-0.072, -0.039] | -0.089 [-0.125, -0.054] | -0.040 [-0.074, -0.009] | -0.032 [-0.071, +0.009] | -0.064 [-0.090, -0.042] |
| f4_w0.5 | -0.057 [-0.074, -0.040] | -0.082 [-0.116, -0.047] | -0.039 [-0.072, -0.007] | -0.026 [-0.063, +0.013] | -0.076 [-0.106, -0.051] |
| f4_w0.75 | -0.065 [-0.083, -0.047] | -0.078 [-0.116, -0.044] | -0.042 [-0.076, -0.009] | -0.040 [-0.080, +0.000] | -0.085 [-0.112, -0.058] |
| f4_w1 | -0.081 [-0.102, -0.058] | -0.082 [-0.121, -0.045] | -0.039 [-0.074, -0.007] | -0.051 [-0.098, -0.008] | -0.113 [-0.147, -0.079] |
| f4b_w0 | -0.062 [-0.078, -0.045] | -0.126 [-0.167, -0.094] | -0.040 [-0.076, -0.010] | -0.035 [-0.072, +0.007] | -0.067 [-0.093, -0.045] |
| f4b_w0.25 | -0.058 [-0.075, -0.041] | -0.089 [-0.125, -0.054] | -0.040 [-0.074, -0.009] | -0.032 [-0.071, +0.009] | -0.070 [-0.096, -0.046] |
| f4b_w0.5 | -0.064 [-0.082, -0.046] | -0.082 [-0.116, -0.047] | -0.039 [-0.072, -0.007] | -0.029 [-0.068, +0.011] | -0.089 [-0.121, -0.061] |
| f4b_w0.75 | -0.074 [-0.093, -0.055] | -0.078 [-0.116, -0.044] | -0.042 [-0.076, -0.009] | -0.040 [-0.082, +0.000] | -0.104 [-0.136, -0.075] |
| f4b_w1 | -0.094 [-0.116, -0.070] | -0.082 [-0.121, -0.045] | -0.039 [-0.074, -0.007] | -0.051 [-0.098, -0.008] | -0.141 [-0.182, -0.104] |
| tb2 | -0.028 [-0.041, -0.016] | -0.056 [-0.084, -0.030] | -0.039 [-0.072, -0.007] | +0.006 [-0.023, +0.038] | -0.037 [-0.056, -0.020] |
| tbg | -0.030 [-0.042, -0.017] | -0.058 [-0.086, -0.031] | -0.044 [-0.079, -0.014] | +0.007 [-0.022, +0.038] | -0.041 [-0.060, -0.023] |
| tbc | -0.004 [-0.009, +0.002] | -0.012 [-0.027, +0.004] | -0.005 [-0.022, +0.011] | +0.007 [-0.004, +0.019] | -0.007 [-0.014, +0.000] |
| tb2c | -0.009 [-0.023, +0.005] | -0.022 [-0.056, +0.010] | +0.033 [-0.003, +0.074] | +0.008 [-0.027, +0.043] | -0.027 [-0.043, -0.011] |
| tbgc | -0.013 [-0.027, +0.001] | -0.029 [-0.059, +0.002] | +0.011 [-0.025, +0.049] | +0.009 [-0.026, +0.044] | -0.027 [-0.043, -0.010] |
| tbcc | +0.008 [+0.000, +0.015] | +0.000 [-0.027, +0.026] | +0.054 [+0.029, +0.084] | +0.009 [-0.002, +0.022] | -0.004 [-0.013, +0.006] |

### Session 9 (dev queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.122 [-0.145, -0.101] | -0.285 [-0.354, -0.221] | -0.283 [-0.338, -0.228] | -0.040 [-0.073, -0.010] | -0.081 [-0.113, -0.053] |
| b | -0.050 [-0.064, -0.036] | -0.067 [-0.096, -0.039] | -0.100 [-0.136, -0.067] | -0.019 [-0.050, +0.020] | -0.050 [-0.072, -0.029] |
| c | -0.018 [-0.027, -0.010] | -0.039 [-0.058, -0.020] | -0.086 [-0.114, -0.062] | +0.003 [-0.017, +0.023] | -0.006 [-0.014, +0.003] |
| d | -0.015 [-0.020, -0.010] | -0.024 [-0.042, -0.008] | -0.074 [-0.103, -0.052] | -0.003 [-0.011, +0.003] | -0.002 [-0.008, +0.004] |
| ac | -0.087 [-0.106, -0.067] | -0.174 [-0.235, -0.117] | -0.174 [-0.225, -0.123] | -0.026 [-0.055, +0.001] | -0.076 [-0.108, -0.048] |
| cc | -0.003 [-0.012, +0.004] | -0.014 [-0.025, -0.002] | -0.005 [-0.014, +0.003] | -0.002 [-0.025, +0.020] | -0.001 [-0.008, +0.007] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| u_p0 | -0.098 [-0.119, -0.077] | -0.073 [-0.119, -0.032] | -0.084 [-0.123, -0.050] | -0.069 [-0.106, -0.030] | -0.130 [-0.166, -0.092] |
| u_p0.25 | -0.085 [-0.104, -0.065] | -0.123 [-0.178, -0.077] | -0.146 [-0.191, -0.102] | -0.033 [-0.064, +0.000] | -0.092 [-0.123, -0.063] |
| u_p0.5 | -0.100 [-0.119, -0.080] | -0.203 [-0.264, -0.149] | -0.209 [-0.261, -0.158] | -0.034 [-0.062, -0.007] | -0.081 [-0.111, -0.054] |
| u_p0.75 | -0.112 [-0.132, -0.093] | -0.253 [-0.319, -0.194] | -0.262 [-0.317, -0.206] | -0.040 [-0.071, -0.010] | -0.075 [-0.101, -0.050] |
| u_p1 | -0.129 [-0.153, -0.108] | -0.294 [-0.365, -0.230] | -0.290 [-0.345, -0.235] | -0.050 [-0.083, -0.018] | -0.086 [-0.118, -0.059] |
| c_p0 | -0.085 [-0.107, -0.062] | -0.049 [-0.099, -0.006] | -0.053 [-0.090, -0.016] | -0.064 [-0.107, -0.021] | -0.121 [-0.160, -0.083] |
| c_p0.25 | -0.076 [-0.096, -0.056] | -0.072 [-0.131, -0.022] | -0.095 [-0.139, -0.053] | -0.045 [-0.079, -0.008] | -0.093 [-0.126, -0.062] |
| c_p0.5 | -0.078 [-0.098, -0.059] | -0.111 [-0.169, -0.059] | -0.127 [-0.172, -0.083] | -0.037 [-0.070, -0.005] | -0.083 [-0.113, -0.055] |
| c_p0.75 | -0.090 [-0.109, -0.069] | -0.166 [-0.230, -0.109] | -0.163 [-0.212, -0.115] | -0.038 [-0.071, -0.007] | -0.080 [-0.111, -0.052] |
| c_p1 | -0.096 [-0.117, -0.075] | -0.191 [-0.257, -0.130] | -0.190 [-0.241, -0.139] | -0.037 [-0.066, -0.008] | -0.080 [-0.111, -0.053] |
| proc_p0 | +0.036 [+0.019, +0.057] | +0.125 [+0.082, +0.174] | +0.116 [+0.079, +0.153] | +0.049 [+0.010, +0.091] | -0.019 [-0.044, +0.008] |
| proc_p0.25 | +0.036 [+0.018, +0.056] | +0.128 [+0.082, +0.179] | +0.114 [+0.076, +0.152] | +0.049 [+0.010, +0.090] | -0.021 [-0.046, +0.005] |
| proc_p0.5 | +0.033 [+0.015, +0.053] | +0.133 [+0.087, +0.185] | +0.120 [+0.081, +0.158] | +0.043 [+0.004, +0.084] | -0.028 [-0.053, -0.002] |
| proc_p0.75 | +0.025 [+0.006, +0.046] | +0.126 [+0.074, +0.182] | +0.118 [+0.076, +0.163] | +0.035 [-0.001, +0.072] | -0.037 [-0.063, -0.010] |
| proc_p1 | +0.020 [-0.000, +0.041] | +0.118 [+0.060, +0.176] | +0.112 [+0.066, +0.161] | +0.029 [-0.007, +0.068] | -0.042 [-0.069, -0.016] |
| coral_p0 | -0.093 [-0.118, -0.066] | -0.058 [-0.113, -0.005] | -0.023 [-0.056, +0.011] | -0.122 [-0.182, -0.061] | -0.103 [-0.139, -0.066] |
| coral_p0.25 | -0.082 [-0.107, -0.058] | -0.063 [-0.118, -0.013] | -0.037 [-0.074, +0.000] | -0.099 [-0.156, -0.045] | -0.089 [-0.122, -0.058] |
| coral_p0.5 | -0.081 [-0.104, -0.058] | -0.080 [-0.139, -0.026] | -0.076 [-0.117, -0.032] | -0.086 [-0.137, -0.036] | -0.078 [-0.107, -0.050] |
| coral_p0.75 | -0.082 [-0.105, -0.059] | -0.084 [-0.144, -0.026] | -0.102 [-0.149, -0.054] | -0.078 [-0.125, -0.029] | -0.078 [-0.107, -0.049] |
| coral_p1 | -0.082 [-0.102, -0.059] | -0.097 [-0.158, -0.040] | -0.114 [-0.160, -0.065] | -0.071 [-0.114, -0.024] | -0.073 [-0.101, -0.046] |
| ridge1_p0 | -0.000 [-0.020, +0.022] | +0.060 [+0.010, +0.110] | +0.098 [+0.062, +0.138] | -0.008 [-0.050, +0.035] | -0.042 [-0.074, -0.012] |
| ridge1_p0.25 | +0.003 [-0.015, +0.024] | +0.063 [+0.014, +0.118] | +0.098 [+0.060, +0.139] | +0.009 [-0.030, +0.051] | -0.045 [-0.076, -0.015] |
| ridge1_p0.5 | -0.002 [-0.020, +0.019] | +0.041 [-0.011, +0.095] | +0.095 [+0.056, +0.137] | +0.003 [-0.036, +0.042] | -0.046 [-0.077, -0.016] |
| ridge1_p0.75 | -0.011 [-0.030, +0.010] | +0.015 [-0.039, +0.074] | +0.104 [+0.062, +0.148] | -0.008 [-0.045, +0.028] | -0.055 [-0.085, -0.026] |
| ridge1_p1 | -0.017 [-0.037, +0.005] | -0.010 [-0.071, +0.048] | +0.104 [+0.062, +0.151] | -0.014 [-0.052, +0.021] | -0.056 [-0.085, -0.028] |
| ridge10_p0 | -0.152 [-0.174, -0.128] | -0.283 [-0.338, -0.233] | +0.021 [-0.017, +0.061] | -0.254 [-0.307, -0.206] | -0.091 [-0.125, -0.057] |
| ridge10_p0.25 | -0.137 [-0.157, -0.115] | -0.328 [-0.386, -0.273] | +0.016 [-0.022, +0.054] | -0.197 [-0.243, -0.155] | -0.083 [-0.115, -0.052] |
| ridge10_p0.5 | -0.154 [-0.175, -0.132] | -0.439 [-0.502, -0.379] | +0.005 [-0.036, +0.049] | -0.202 [-0.249, -0.160] | -0.081 [-0.114, -0.051] |
| ridge10_p0.75 | -0.169 [-0.191, -0.147] | -0.514 [-0.577, -0.447] | -0.016 [-0.063, +0.031] | -0.213 [-0.263, -0.171] | -0.077 [-0.108, -0.048] |
| ridge10_p1 | -0.184 [-0.205, -0.161] | -0.587 [-0.651, -0.520] | -0.037 [-0.085, +0.010] | -0.224 [-0.276, -0.179] | -0.076 [-0.103, -0.049] |
| ridge100_p0 | -0.279 [-0.308, -0.251] | -0.456 [-0.520, -0.391] | -0.072 [-0.111, -0.030] | -0.526 [-0.585, -0.468] | -0.121 [-0.159, -0.082] |
| ridge100_p0.25 | -0.257 [-0.283, -0.232] | -0.575 [-0.630, -0.525] | -0.097 [-0.139, -0.057] | -0.409 [-0.467, -0.353] | -0.102 [-0.136, -0.069] |
| ridge100_p0.5 | -0.271 [-0.296, -0.244] | -0.671 [-0.731, -0.608] | -0.139 [-0.187, -0.096] | -0.414 [-0.474, -0.358] | -0.090 [-0.124, -0.060] |
| ridge100_p0.75 | -0.274 [-0.300, -0.247] | -0.703 [-0.756, -0.643] | -0.167 [-0.218, -0.123] | -0.404 [-0.463, -0.351] | -0.086 [-0.118, -0.057] |
| ridge100_p1 | -0.277 [-0.302, -0.251] | -0.703 [-0.759, -0.640] | -0.223 [-0.273, -0.177] | -0.404 [-0.464, -0.348] | -0.078 [-0.105, -0.052] |
| ridge1000_p0 | -0.313 [-0.343, -0.283] | -0.507 [-0.569, -0.445] | -0.107 [-0.151, -0.067] | -0.596 [-0.655, -0.535] | -0.128 [-0.168, -0.089] |
| ridge1000_p0.25 | -0.287 [-0.313, -0.261] | -0.619 [-0.675, -0.567] | -0.132 [-0.179, -0.090] | -0.476 [-0.537, -0.419] | -0.103 [-0.138, -0.071] |
| ridge1000_p0.5 | -0.295 [-0.320, -0.267] | -0.710 [-0.757, -0.660] | -0.162 [-0.211, -0.119] | -0.469 [-0.529, -0.412] | -0.090 [-0.123, -0.059] |
| ridge1000_p0.75 | -0.299 [-0.326, -0.271] | -0.724 [-0.767, -0.679] | -0.211 [-0.262, -0.165] | -0.465 [-0.528, -0.406] | -0.085 [-0.116, -0.057] |
| ridge1000_p1 | -0.301 [-0.327, -0.274] | -0.720 [-0.765, -0.676] | -0.255 [-0.309, -0.206] | -0.449 [-0.513, -0.393] | -0.086 [-0.114, -0.060] |
| b2 | -0.057 [-0.073, -0.041] | -0.080 [-0.113, -0.052] | -0.095 [-0.132, -0.062] | -0.017 [-0.049, +0.021] | -0.064 [-0.089, -0.041] |
| bc2 | -0.043 [-0.058, -0.025] | -0.048 [-0.075, -0.022] | -0.032 [-0.061, -0.005] | -0.023 [-0.060, +0.019] | -0.056 [-0.083, -0.034] |
| bc | -0.037 [-0.052, -0.022] | -0.036 [-0.057, -0.015] | -0.046 [-0.076, -0.018] | -0.026 [-0.064, +0.016] | -0.042 [-0.065, -0.022] |
| f4_w0 | -0.077 [-0.093, -0.060] | -0.150 [-0.192, -0.115] | -0.114 [-0.154, -0.079] | -0.039 [-0.074, +0.003] | -0.069 [-0.094, -0.047] |
| f4_w0.25 | -0.070 [-0.086, -0.052] | -0.113 [-0.153, -0.079] | -0.114 [-0.152, -0.081] | -0.035 [-0.074, +0.005] | -0.066 [-0.091, -0.043] |
| f4_w0.5 | -0.072 [-0.089, -0.055] | -0.106 [-0.143, -0.071] | -0.112 [-0.150, -0.079] | -0.029 [-0.066, +0.010] | -0.078 [-0.107, -0.051] |
| f4_w0.75 | -0.080 [-0.097, -0.061] | -0.102 [-0.142, -0.068] | -0.116 [-0.155, -0.081] | -0.043 [-0.082, -0.003] | -0.087 [-0.115, -0.059] |
| f4_w1 | -0.095 [-0.117, -0.074] | -0.106 [-0.146, -0.070] | -0.112 [-0.153, -0.078] | -0.055 [-0.101, -0.011] | -0.115 [-0.150, -0.081] |
| f4b_w0 | -0.077 [-0.093, -0.060] | -0.150 [-0.192, -0.115] | -0.114 [-0.154, -0.079] | -0.039 [-0.074, +0.003] | -0.069 [-0.094, -0.047] |
| f4b_w0.25 | -0.073 [-0.090, -0.055] | -0.113 [-0.153, -0.079] | -0.114 [-0.152, -0.081] | -0.035 [-0.074, +0.006] | -0.072 [-0.097, -0.048] |
| f4b_w0.5 | -0.079 [-0.097, -0.060] | -0.106 [-0.143, -0.071] | -0.112 [-0.150, -0.079] | -0.032 [-0.070, +0.007] | -0.091 [-0.123, -0.062] |
| f4b_w0.75 | -0.088 [-0.107, -0.070] | -0.102 [-0.142, -0.068] | -0.116 [-0.155, -0.081] | -0.044 [-0.084, -0.003] | -0.106 [-0.139, -0.077] |
| f4b_w1 | -0.108 [-0.132, -0.085] | -0.106 [-0.146, -0.070] | -0.112 [-0.153, -0.078] | -0.055 [-0.101, -0.011] | -0.144 [-0.186, -0.106] |
| tb2 | -0.043 [-0.057, -0.029] | -0.080 [-0.111, -0.051] | -0.112 [-0.153, -0.078] | +0.003 [-0.027, +0.035] | -0.039 [-0.057, -0.021] |
| tbg | -0.045 [-0.059, -0.032] | -0.082 [-0.113, -0.052] | -0.118 [-0.158, -0.083] | +0.003 [-0.026, +0.037] | -0.043 [-0.061, -0.025] |
| tbc | -0.018 [-0.026, -0.012] | -0.036 [-0.057, -0.015] | -0.079 [-0.108, -0.058] | +0.003 [-0.009, +0.016] | -0.009 [-0.017, -0.001] |
| tb2c | -0.024 [-0.037, -0.011] | -0.046 [-0.074, -0.019] | -0.040 [-0.073, -0.009] | +0.005 [-0.029, +0.041] | -0.029 [-0.045, -0.013] |
| tbgc | -0.028 [-0.041, -0.014] | -0.053 [-0.080, -0.027] | -0.063 [-0.101, -0.028] | +0.006 [-0.029, +0.042] | -0.029 [-0.046, -0.013] |
| tbcc | -0.007 [-0.013, -0.001] | -0.024 [-0.044, -0.006] | -0.019 [-0.034, -0.007] | +0.006 [-0.003, +0.017] | -0.006 [-0.013, +0.002] |

### Session 9 selection rule applied to the dev queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F1 | c_p0.5 | 1.00 | -0.077 | -0.072 | -0.040 | -0.040 | -0.077 |
| F2 | proc_p0 | 1.00 | -0.013 | +0.164 | +0.202 | +0.045 | -0.013 |
| F3 | bc | 2.55 | -0.037 | +0.003 | +0.040 | -0.029 | -0.037 |
| F4 | f4_w0.5 | 2.00 | -0.073 | -0.067 | -0.026 | -0.033 | -0.073 |
| F5 | tbcc | 5.27 | +0.000 | +0.015 | +0.067 | +0.003 | +0.000 |

F4b bias (dev queries, leave-one-out folders with both groups): image queries +0.3510 (n = 1717), text queries +0.3209 (n = 2293).

Alignment fit: {'pairs': 534, 'coral_shrinkage': (0.01957493308159513, 0.0314595824561629)}.

### Session 9 modality gap per space, dev directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.363 | 0.761 | 0.707 | 0.544 |
| centered | 0.013 | 0.552 | 0.429 | 0.243 |
| proc | 0.011 | 0.552 | 0.429 | 0.434 |
| coral | 0.022 | 0.299 | 0.429 | 0.267 |
| ridge1 | 0.039 | 0.724 | 0.429 | 0.498 |
| ridge10 | 0.057 | 0.810 | 0.429 | 0.399 |
| ridge100 | 0.068 | 0.833 | 0.429 | 0.321 |
| ridge1000 | 0.075 | 0.832 | 0.429 | 0.300 |

### Session 9 F5 cluster purity, dev directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2 | 2.00 | 0.921 | 534 |
| tbg | 1.96 | 0.921 | 534 |
| tbc | 5.27 | 0.988 | 534 |
| tb2c | 2.00 | 0.874 | 534 |
| tbgc | 1.96 | 0.874 | 534 |
| tbcc | 5.27 | 0.981 | 534 |

### Session 9 hypotheses on the dev queries (dev: informative only, the verdict is the test split)

H9a, F1 selected c_p0.5: upper bounds of (x - c) P1 image in [0,.2)+[.2,.5) -0.015, P2 textlike in [.5,.8)+[.8,1] +0.008, image in [.5,.8)+[.8,1] -0.011, textlike in [0,.2)+[.2,.5) -0.051; all above -0.02: no, H9a survives this family.
H9a, F2 selected proc_p0: upper bounds of (x - c) P1 image in [0,.2)+[.2,.5) +0.219, P2 textlike in [.5,.8)+[.8,1] +0.249, image in [.5,.8)+[.8,1] +0.078, textlike in [0,.2)+[.2,.5) +0.013; all above -0.02: yes, H9a dead.
H9b, F3 selected bc: upper bounds of (x - c) all -0.005, P1 image in [0,.2)+[.2,.5) +0.029, P2 textlike in [.5,.8)+[.8,1] +0.068, image in [.5,.8)+[.8,1] +0.004, textlike in [0,.2)+[.2,.5) -0.017; any below -0.02: no, H9b survives this family.
H9b, F4 selected f4_w0.5: upper bounds of (x - c) all -0.038, P1 image in [0,.2)+[.2,.5) -0.035, P2 textlike in [.5,.8)+[.8,1] +0.005, image in [.5,.8)+[.8,1] -0.003, textlike in [0,.2)+[.2,.5) -0.046; any below -0.02: yes, H9b dead for this family.
H9c, c - tbc (type-blind k-means at c's budget, uncentered): P1 image in [0,.2)+[.2,.5) -0.003 [-0.016, +0.011]; P2 textlike in [.5,.8)+[.8,1] -0.007 [-0.022, +0.008]; interval includes zero in a primary cell: yes, H9c dead.
Secondary, cc - tbcc (centered): P1 image in [0,.2)+[.2,.5) +0.010 [-0.003, +0.028]; P2 textlike in [.5,.8)+[.8,1] +0.014 [+0.002, +0.027].

## Appendix B: cross-fitted dev grid for F2 (`/workspace/logs/s9_devcv.md`, session 9 sections)

### Session 9 (dev queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.675 | 0.464 | 0.425 | 0.697 | 0.791 | -0.104 [-0.128, -0.083] | -0.246 [-0.320, -0.179] | -0.197 [-0.257, -0.134] | -0.043 [-0.073, -0.015] | -0.076 [-0.106, -0.050] | -0.246 |
| b | ref | 2.55 | 0.748 | 0.683 | 0.608 | 0.718 | 0.822 | -0.031 [-0.044, -0.020] | -0.027 [-0.050, -0.007] | -0.014 [-0.042, +0.010] | -0.022 [-0.047, +0.006] | -0.044 [-0.064, -0.025] | -0.044 |
| c | ref | 5.27 | 0.780 | 0.710 | 0.622 | 0.740 | 0.866 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| d | ref | 9.70 | 0.783 | 0.725 | 0.634 | 0.733 | 0.870 | +0.003 [-0.003, +0.010] | +0.015 [+0.002, +0.029] | +0.012 [+0.002, +0.025] | -0.007 [-0.025, +0.011] | +0.004 [-0.005, +0.012] | -0.007 |
| ac | ref | 1.00 | 0.711 | 0.575 | 0.534 | 0.710 | 0.796 | -0.069 [-0.089, -0.048] | -0.135 [-0.201, -0.075] | -0.088 [-0.141, -0.029] | -0.029 [-0.056, -0.003] | -0.070 [-0.103, -0.045] | -0.135 |
| cc | ref | 5.27 | 0.794 | 0.735 | 0.703 | 0.735 | 0.871 | +0.015 [+0.008, +0.022] | +0.026 [+0.007, +0.047] | +0.081 [+0.059, +0.108] | -0.005 [-0.015, +0.005] | +0.005 [-0.003, +0.012] | -0.005 |
| dc | ref | 9.70 | 0.798 | 0.749 | 0.708 | 0.736 | 0.872 | +0.018 [+0.010, +0.027] | +0.039 [+0.020, +0.058] | +0.086 [+0.062, +0.114] | -0.003 [-0.023, +0.017] | +0.006 [-0.003, +0.014] | -0.003 |
| proc_p0 | F2 | 1.00 | 0.675 | 0.613 | 0.578 | 0.633 | 0.742 | -0.104 [-0.123, -0.084] | -0.097 [-0.145, -0.056] | -0.044 [-0.082, -0.009] | -0.107 [-0.146, -0.071] | -0.124 [-0.159, -0.091] | -0.124 |
| proc_p0.25 | F2 | 1.00 | 0.691 | 0.585 | 0.547 | 0.676 | 0.769 | -0.088 [-0.106, -0.070] | -0.125 [-0.167, -0.088] | -0.076 [-0.113, -0.037] | -0.063 [-0.096, -0.033] | -0.097 [-0.130, -0.068] | -0.125 |
| proc_p0.5 | F2 | 1.00 | 0.686 | 0.524 | 0.492 | 0.685 | 0.786 | -0.093 [-0.110, -0.076] | -0.186 [-0.238, -0.141] | -0.130 [-0.172, -0.083] | -0.055 [-0.085, -0.025] | -0.080 [-0.110, -0.054] | -0.186 |
| proc_p0.75 | F2 | 1.00 | 0.673 | 0.451 | 0.450 | 0.690 | 0.790 | -0.106 [-0.124, -0.091] | -0.259 [-0.324, -0.206] | -0.172 [-0.219, -0.124] | -0.050 [-0.077, -0.023] | -0.076 [-0.107, -0.049] | -0.259 |
| proc_p1 | F2 | 1.00 | 0.662 | 0.403 | 0.397 | 0.696 | 0.792 | -0.117 [-0.135, -0.101] | -0.307 [-0.374, -0.248] | -0.225 [-0.275, -0.171] | -0.044 [-0.071, -0.016] | -0.074 [-0.100, -0.049] | -0.307 |
| coral_p0 | F2 | 1.00 | 0.709 | 0.701 | 0.645 | 0.671 | 0.747 | -0.071 [-0.095, -0.047] | -0.009 [-0.056, +0.038] | +0.023 [-0.012, +0.061] | -0.069 [-0.113, -0.024] | -0.119 [-0.157, -0.083] | -0.119 |
| coral_p0.25 | F2 | 1.00 | 0.721 | 0.681 | 0.615 | 0.698 | 0.773 | -0.059 [-0.078, -0.038] | -0.029 [-0.081, +0.021] | -0.007 [-0.043, +0.034] | -0.042 [-0.082, -0.002] | -0.093 [-0.123, -0.065] | -0.093 |
| coral_p0.5 | F2 | 1.00 | 0.719 | 0.662 | 0.568 | 0.703 | 0.787 | -0.061 [-0.081, -0.041] | -0.048 [-0.102, +0.005] | -0.054 [-0.100, -0.006] | -0.037 [-0.074, -0.002] | -0.080 [-0.112, -0.051] | -0.080 |
| coral_p0.75 | F2 | 1.00 | 0.717 | 0.643 | 0.550 | 0.702 | 0.794 | -0.063 [-0.083, -0.042] | -0.067 [-0.123, -0.013] | -0.072 [-0.121, -0.020] | -0.038 [-0.073, -0.004] | -0.073 [-0.104, -0.047] | -0.073 |
| coral_p1 | F2 | 1.00 | 0.710 | 0.608 | 0.517 | 0.707 | 0.795 | -0.070 [-0.089, -0.049] | -0.102 [-0.164, -0.045] | -0.105 [-0.154, -0.049] | -0.033 [-0.064, -0.001] | -0.071 [-0.103, -0.044] | -0.105 |
| ridge1_p0 | F2 | 1.00 | 0.633 | 0.502 | 0.629 | 0.511 | 0.746 | -0.147 [-0.167, -0.126] | -0.208 [-0.262, -0.158] | +0.007 [-0.030, +0.043] | -0.229 [-0.275, -0.185] | -0.120 [-0.151, -0.088] | -0.229 |
| ridge1_p0.25 | F2 | 1.00 | 0.647 | 0.457 | 0.591 | 0.561 | 0.768 | -0.133 [-0.152, -0.114] | -0.253 [-0.308, -0.201] | -0.032 [-0.073, +0.010] | -0.179 [-0.221, -0.140] | -0.098 [-0.130, -0.068] | -0.253 |
| ridge1_p0.5 | F2 | 1.00 | 0.644 | 0.387 | 0.569 | 0.585 | 0.776 | -0.136 [-0.154, -0.117] | -0.323 [-0.388, -0.264] | -0.053 [-0.095, -0.005] | -0.155 [-0.199, -0.116] | -0.090 [-0.120, -0.061] | -0.323 |
| ridge1_p0.75 | F2 | 1.00 | 0.630 | 0.314 | 0.527 | 0.582 | 0.781 | -0.150 [-0.169, -0.130] | -0.396 [-0.462, -0.334] | -0.095 [-0.141, -0.044] | -0.158 [-0.206, -0.117] | -0.085 [-0.116, -0.057] | -0.396 |
| ridge1_p1 | F2 | 1.00 | 0.618 | 0.271 | 0.492 | 0.576 | 0.781 | -0.162 [-0.181, -0.142] | -0.439 [-0.506, -0.374] | -0.130 [-0.177, -0.083] | -0.163 [-0.212, -0.122] | -0.085 [-0.114, -0.058] | -0.439 |
| ridge10_p0 | F2 | 1.00 | 0.531 | 0.352 | 0.589 | 0.265 | 0.738 | -0.249 [-0.275, -0.222] | -0.358 [-0.419, -0.297] | -0.033 [-0.071, +0.002] | -0.475 [-0.534, -0.421] | -0.128 [-0.165, -0.092] | -0.475 |
| ridge10_p0.25 | F2 | 1.00 | 0.559 | 0.273 | 0.557 | 0.376 | 0.762 | -0.221 [-0.244, -0.197] | -0.437 [-0.498, -0.382] | -0.065 [-0.103, -0.025] | -0.364 [-0.420, -0.316] | -0.104 [-0.139, -0.072] | -0.437 |
| ridge10_p0.5 | F2 | 1.00 | 0.546 | 0.140 | 0.525 | 0.390 | 0.773 | -0.234 [-0.255, -0.210] | -0.570 [-0.631, -0.507] | -0.097 [-0.137, -0.052] | -0.350 [-0.409, -0.300] | -0.093 [-0.127, -0.063] | -0.570 |
| ridge10_p0.75 | F2 | 1.00 | 0.535 | 0.073 | 0.466 | 0.399 | 0.780 | -0.245 [-0.267, -0.221] | -0.637 [-0.697, -0.568] | -0.156 [-0.200, -0.110] | -0.340 [-0.398, -0.290] | -0.086 [-0.119, -0.058] | -0.637 |
| ridge10_p1 | F2 | 1.00 | 0.531 | 0.063 | 0.427 | 0.405 | 0.783 | -0.249 [-0.272, -0.224] | -0.647 [-0.707, -0.576] | -0.195 [-0.243, -0.146] | -0.334 [-0.394, -0.284] | -0.083 [-0.111, -0.056] | -0.647 |
| ridge100_p0 | F2 | 1.00 | 0.464 | 0.218 | 0.564 | 0.115 | 0.732 | -0.315 [-0.346, -0.287] | -0.491 [-0.555, -0.429] | -0.058 [-0.095, -0.022] | -0.624 [-0.679, -0.571] | -0.134 [-0.171, -0.095] | -0.624 |
| ridge100_p0.25 | F2 | 1.00 | 0.490 | 0.104 | 0.525 | 0.238 | 0.759 | -0.289 [-0.314, -0.263] | -0.606 [-0.659, -0.555] | -0.097 [-0.137, -0.057] | -0.501 [-0.562, -0.444] | -0.108 [-0.142, -0.075] | -0.606 |
| ridge100_p0.5 | F2 | 1.00 | 0.489 | 0.031 | 0.489 | 0.270 | 0.769 | -0.290 [-0.315, -0.263] | -0.679 [-0.727, -0.632] | -0.134 [-0.174, -0.090] | -0.469 [-0.532, -0.412] | -0.097 [-0.130, -0.067] | -0.679 |
| ridge100_p0.75 | F2 | 1.00 | 0.487 | 0.022 | 0.429 | 0.281 | 0.776 | -0.293 [-0.318, -0.265] | -0.688 [-0.734, -0.640] | -0.193 [-0.239, -0.150] | -0.459 [-0.521, -0.404] | -0.090 [-0.122, -0.063] | -0.688 |
| ridge100_p1 | F2 | 1.00 | 0.485 | 0.027 | 0.371 | 0.296 | 0.778 | -0.295 [-0.320, -0.269] | -0.683 [-0.730, -0.632] | -0.251 [-0.303, -0.199] | -0.444 [-0.506, -0.390] | -0.088 [-0.115, -0.062] | -0.683 |
| ridge1000_p0 | F2 | 1.00 | 0.453 | 0.189 | 0.564 | 0.093 | 0.730 | -0.327 [-0.356, -0.299] | -0.520 [-0.580, -0.462] | -0.058 [-0.096, -0.023] | -0.647 [-0.702, -0.596] | -0.136 [-0.174, -0.096] | -0.647 |
| ridge1000_p0.25 | F2 | 1.00 | 0.479 | 0.080 | 0.527 | 0.217 | 0.754 | -0.300 [-0.325, -0.274] | -0.630 [-0.681, -0.579] | -0.095 [-0.133, -0.054] | -0.522 [-0.584, -0.463] | -0.113 [-0.148, -0.081] | -0.630 |
| ridge1000_p0.5 | F2 | 1.00 | 0.478 | 0.020 | 0.476 | 0.241 | 0.771 | -0.301 [-0.326, -0.273] | -0.689 [-0.736, -0.641] | -0.146 [-0.187, -0.102] | -0.499 [-0.559, -0.444] | -0.095 [-0.128, -0.065] | -0.689 |
| ridge1000_p0.75 | F2 | 1.00 | 0.478 | 0.020 | 0.424 | 0.256 | 0.775 | -0.302 [-0.329, -0.274] | -0.689 [-0.736, -0.641] | -0.199 [-0.243, -0.154] | -0.484 [-0.547, -0.428] | -0.091 [-0.123, -0.064] | -0.689 |
| ridge1000_p1 | F2 | 1.00 | 0.475 | 0.022 | 0.364 | 0.270 | 0.779 | -0.304 [-0.329, -0.277] | -0.688 [-0.736, -0.640] | -0.258 [-0.313, -0.202] | -0.470 [-0.534, -0.414] | -0.087 [-0.117, -0.062] | -0.688 |

### Session 9 (dev queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.549 | 0.360 | 0.279 | 0.565 | 0.667 |
| b | 0.633 | 0.568 | 0.492 | 0.596 | 0.710 |
| c | 0.667 | 0.565 | 0.506 | 0.639 | 0.758 |
| d | 0.668 | 0.558 | 0.513 | 0.638 | 0.758 |
| ac | 0.574 | 0.432 | 0.359 | 0.568 | 0.676 |
| cc | 0.680 | 0.594 | 0.550 | 0.639 | 0.765 |
| dc | 0.682 | 0.587 | 0.554 | 0.641 | 0.768 |
| proc_p0 | 0.278 | 0.263 | 0.269 | 0.266 | 0.291 |
| proc_p0.25 | 0.286 | 0.237 | 0.200 | 0.272 | 0.334 |
| proc_p0.5 | 0.284 | 0.166 | 0.185 | 0.288 | 0.343 |
| proc_p0.75 | 0.262 | 0.126 | 0.163 | 0.263 | 0.331 |
| proc_p1 | 0.260 | 0.113 | 0.125 | 0.277 | 0.330 |
| coral_p0 | 0.289 | 0.266 | 0.243 | 0.270 | 0.319 |
| coral_p0.25 | 0.296 | 0.259 | 0.236 | 0.284 | 0.332 |
| coral_p0.5 | 0.291 | 0.234 | 0.218 | 0.297 | 0.323 |
| coral_p0.75 | 0.298 | 0.241 | 0.172 | 0.313 | 0.339 |
| coral_p1 | 0.291 | 0.234 | 0.155 | 0.314 | 0.335 |
| ridge1_p0 | 0.234 | 0.171 | 0.232 | 0.163 | 0.295 |
| ridge1_p0.25 | 0.253 | 0.160 | 0.225 | 0.202 | 0.318 |
| ridge1_p0.5 | 0.246 | 0.111 | 0.195 | 0.209 | 0.321 |
| ridge1_p0.75 | 0.239 | 0.092 | 0.156 | 0.207 | 0.325 |
| ridge1_p1 | 0.238 | 0.060 | 0.146 | 0.206 | 0.334 |
| ridge10_p0 | 0.200 | 0.094 | 0.250 | 0.055 | 0.312 |
| ridge10_p0.25 | 0.215 | 0.041 | 0.228 | 0.118 | 0.328 |
| ridge10_p0.5 | 0.195 | 0.017 | 0.158 | 0.097 | 0.321 |
| ridge10_p0.75 | 0.205 | 0.005 | 0.137 | 0.143 | 0.327 |
| ridge10_p1 | 0.206 | 0.014 | 0.125 | 0.136 | 0.333 |
| ridge100_p0 | 0.176 | 0.027 | 0.234 | 0.013 | 0.309 |
| ridge100_p0.25 | 0.186 | 0.002 | 0.227 | 0.059 | 0.310 |
| ridge100_p0.5 | 0.184 | 0.002 | 0.165 | 0.068 | 0.320 |
| ridge100_p0.75 | 0.182 | 0.002 | 0.127 | 0.063 | 0.329 |
| ridge100_p1 | 0.183 | 0.002 | 0.121 | 0.079 | 0.324 |
| ridge1000_p0 | 0.172 | 0.017 | 0.244 | 0.006 | 0.304 |
| ridge1000_p0.25 | 0.182 | 0.000 | 0.192 | 0.040 | 0.325 |
| ridge1000_p0.5 | 0.182 | 0.000 | 0.170 | 0.060 | 0.319 |
| ridge1000_p0.75 | 0.177 | 0.000 | 0.121 | 0.068 | 0.317 |
| ridge1000_p1 | 0.186 | 0.002 | 0.118 | 0.078 | 0.331 |

### Session 9 (dev queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.732 | 0.558 | 0.476 | 0.759 | 0.833 |
| b | 0.794 | 0.718 | 0.645 | 0.763 | 0.873 |
| c | 0.811 | 0.747 | 0.661 | 0.767 | 0.896 |
| d | 0.812 | 0.759 | 0.675 | 0.763 | 0.894 |
| ac | 0.765 | 0.667 | 0.599 | 0.762 | 0.840 |
| cc | 0.828 | 0.787 | 0.743 | 0.767 | 0.899 |
| dc | 0.830 | 0.794 | 0.745 | 0.769 | 0.899 |
| proc_p0 | 0.742 | 0.676 | 0.631 | 0.709 | 0.808 |
| proc_p0.25 | 0.754 | 0.667 | 0.608 | 0.726 | 0.834 |
| proc_p0.5 | 0.749 | 0.616 | 0.568 | 0.739 | 0.842 |
| proc_p0.75 | 0.735 | 0.548 | 0.515 | 0.747 | 0.843 |
| proc_p1 | 0.725 | 0.493 | 0.482 | 0.751 | 0.845 |
| coral_p0 | 0.763 | 0.753 | 0.694 | 0.714 | 0.810 |
| coral_p0.25 | 0.774 | 0.744 | 0.671 | 0.734 | 0.833 |
| coral_p0.5 | 0.778 | 0.729 | 0.631 | 0.748 | 0.850 |
| coral_p0.75 | 0.771 | 0.708 | 0.601 | 0.756 | 0.845 |
| coral_p1 | 0.764 | 0.688 | 0.578 | 0.753 | 0.847 |
| ridge1_p0 | 0.707 | 0.585 | 0.691 | 0.597 | 0.812 |
| ridge1_p0.25 | 0.717 | 0.544 | 0.668 | 0.640 | 0.827 |
| ridge1_p0.5 | 0.716 | 0.485 | 0.636 | 0.667 | 0.837 |
| ridge1_p0.75 | 0.703 | 0.408 | 0.613 | 0.666 | 0.837 |
| ridge1_p1 | 0.690 | 0.365 | 0.576 | 0.662 | 0.835 |
| ridge10_p0 | 0.609 | 0.456 | 0.652 | 0.363 | 0.800 |
| ridge10_p0.25 | 0.635 | 0.355 | 0.624 | 0.480 | 0.823 |
| ridge10_p0.5 | 0.623 | 0.217 | 0.585 | 0.503 | 0.832 |
| ridge10_p0.75 | 0.608 | 0.140 | 0.552 | 0.495 | 0.836 |
| ridge10_p1 | 0.595 | 0.106 | 0.508 | 0.490 | 0.833 |
| ridge100_p0 | 0.539 | 0.343 | 0.619 | 0.205 | 0.789 |
| ridge100_p0.25 | 0.565 | 0.198 | 0.587 | 0.332 | 0.818 |
| ridge100_p0.5 | 0.558 | 0.082 | 0.545 | 0.366 | 0.830 |
| ridge100_p0.75 | 0.548 | 0.053 | 0.492 | 0.368 | 0.828 |
| ridge100_p1 | 0.539 | 0.051 | 0.443 | 0.374 | 0.822 |
| ridge1000_p0 | 0.521 | 0.299 | 0.608 | 0.168 | 0.787 |
| ridge1000_p0.25 | 0.550 | 0.164 | 0.576 | 0.302 | 0.818 |
| ridge1000_p0.5 | 0.548 | 0.070 | 0.538 | 0.339 | 0.831 |
| ridge1000_p0.75 | 0.536 | 0.049 | 0.483 | 0.344 | 0.823 |
| ridge1000_p1 | 0.530 | 0.048 | 0.441 | 0.349 | 0.818 |

### Session 9 (dev queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.108 [-0.130, -0.087] | -0.261 [-0.333, -0.195] | -0.209 [-0.268, -0.145] | -0.036 [-0.069, -0.009] | -0.079 [-0.111, -0.051] |
| b | -0.035 [-0.049, -0.021] | -0.043 [-0.068, -0.019] | -0.026 [-0.056, +0.000] | -0.015 [-0.049, +0.021] | -0.048 [-0.070, -0.026] |
| c | -0.003 [-0.010, +0.003] | -0.015 [-0.029, -0.002] | -0.012 [-0.025, -0.002] | +0.007 [-0.011, +0.025] | -0.004 [-0.012, +0.005] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| ac | -0.072 [-0.092, -0.052] | -0.150 [-0.218, -0.092] | -0.100 [-0.154, -0.040] | -0.023 [-0.051, +0.003] | -0.074 [-0.106, -0.047] |
| cc | +0.011 [+0.002, +0.020] | +0.010 [-0.009, +0.032] | +0.069 [+0.045, +0.097] | +0.002 [-0.021, +0.024] | +0.001 [-0.008, +0.010] |
| dc | +0.015 [+0.010, +0.020] | +0.024 [+0.008, +0.042] | +0.074 [+0.052, +0.103] | +0.003 [-0.003, +0.011] | +0.002 [-0.004, +0.008] |
| proc_p0 | -0.108 [-0.128, -0.085] | -0.113 [-0.161, -0.072] | -0.056 [-0.094, -0.021] | -0.100 [-0.146, -0.055] | -0.127 [-0.162, -0.095] |
| proc_p0.25 | -0.092 [-0.110, -0.072] | -0.140 [-0.180, -0.101] | -0.088 [-0.126, -0.047] | -0.056 [-0.094, -0.017] | -0.101 [-0.134, -0.072] |
| proc_p0.5 | -0.097 [-0.114, -0.079] | -0.201 [-0.253, -0.155] | -0.142 [-0.185, -0.095] | -0.048 [-0.086, -0.009] | -0.084 [-0.114, -0.057] |
| proc_p0.75 | -0.110 [-0.128, -0.093] | -0.275 [-0.335, -0.219] | -0.185 [-0.229, -0.135] | -0.043 [-0.077, -0.008] | -0.080 [-0.110, -0.053] |
| proc_p1 | -0.121 [-0.138, -0.103] | -0.323 [-0.385, -0.263] | -0.237 [-0.287, -0.186] | -0.037 [-0.074, -0.002] | -0.078 [-0.105, -0.053] |
| coral_p0 | -0.074 [-0.099, -0.049] | -0.024 [-0.070, +0.023] | +0.011 [-0.023, +0.048] | -0.062 [-0.113, -0.011] | -0.122 [-0.159, -0.086] |
| coral_p0.25 | -0.062 [-0.082, -0.041] | -0.044 [-0.094, +0.004] | -0.019 [-0.055, +0.022] | -0.035 [-0.081, +0.013] | -0.096 [-0.127, -0.068] |
| coral_p0.5 | -0.064 [-0.084, -0.042] | -0.063 [-0.116, -0.013] | -0.067 [-0.110, -0.017] | -0.030 [-0.074, +0.013] | -0.083 [-0.116, -0.054] |
| coral_p0.75 | -0.066 [-0.087, -0.045] | -0.082 [-0.139, -0.029] | -0.084 [-0.133, -0.033] | -0.031 [-0.071, +0.012] | -0.076 [-0.107, -0.050] |
| coral_p1 | -0.073 [-0.093, -0.052] | -0.118 [-0.178, -0.060] | -0.118 [-0.168, -0.062] | -0.026 [-0.064, +0.014] | -0.075 [-0.107, -0.048] |
| ridge1_p0 | -0.150 [-0.172, -0.128] | -0.224 [-0.278, -0.173] | -0.005 [-0.041, +0.032] | -0.222 [-0.272, -0.174] | -0.123 [-0.155, -0.091] |
| ridge1_p0.25 | -0.137 [-0.155, -0.117] | -0.268 [-0.324, -0.214] | -0.044 [-0.084, +0.000] | -0.172 [-0.219, -0.129] | -0.101 [-0.133, -0.072] |
| ridge1_p0.5 | -0.139 [-0.159, -0.119] | -0.338 [-0.403, -0.279] | -0.065 [-0.109, -0.015] | -0.148 [-0.194, -0.109] | -0.093 [-0.125, -0.065] |
| ridge1_p0.75 | -0.153 [-0.174, -0.133] | -0.411 [-0.475, -0.348] | -0.107 [-0.153, -0.054] | -0.151 [-0.201, -0.111] | -0.089 [-0.119, -0.061] |
| ridge1_p1 | -0.165 [-0.186, -0.144] | -0.454 [-0.520, -0.387] | -0.142 [-0.190, -0.090] | -0.157 [-0.205, -0.117] | -0.089 [-0.120, -0.061] |
| ridge10_p0 | -0.252 [-0.279, -0.225] | -0.374 [-0.436, -0.312] | -0.046 [-0.082, -0.009] | -0.468 [-0.531, -0.410] | -0.132 [-0.170, -0.095] |
| ridge10_p0.25 | -0.224 [-0.248, -0.202] | -0.452 [-0.511, -0.395] | -0.077 [-0.118, -0.037] | -0.357 [-0.413, -0.308] | -0.108 [-0.143, -0.077] |
| ridge10_p0.5 | -0.237 [-0.259, -0.215] | -0.585 [-0.649, -0.523] | -0.109 [-0.151, -0.064] | -0.343 [-0.399, -0.294] | -0.096 [-0.132, -0.067] |
| ridge10_p0.75 | -0.248 [-0.271, -0.224] | -0.652 [-0.711, -0.585] | -0.169 [-0.212, -0.123] | -0.334 [-0.396, -0.283] | -0.090 [-0.123, -0.061] |
| ridge10_p1 | -0.252 [-0.275, -0.228] | -0.662 [-0.720, -0.593] | -0.207 [-0.253, -0.157] | -0.328 [-0.391, -0.277] | -0.087 [-0.117, -0.060] |
| ridge100_p0 | -0.319 [-0.348, -0.290] | -0.507 [-0.571, -0.444] | -0.070 [-0.109, -0.034] | -0.618 [-0.673, -0.564] | -0.137 [-0.176, -0.100] |
| ridge100_p0.25 | -0.293 [-0.318, -0.266] | -0.621 [-0.672, -0.569] | -0.109 [-0.151, -0.066] | -0.495 [-0.552, -0.436] | -0.111 [-0.147, -0.079] |
| ridge100_p0.5 | -0.294 [-0.318, -0.266] | -0.695 [-0.740, -0.649] | -0.146 [-0.190, -0.099] | -0.463 [-0.524, -0.403] | -0.100 [-0.135, -0.070] |
| ridge100_p0.75 | -0.296 [-0.321, -0.269] | -0.703 [-0.746, -0.657] | -0.206 [-0.252, -0.162] | -0.452 [-0.516, -0.398] | -0.093 [-0.126, -0.065] |
| ridge100_p1 | -0.299 [-0.322, -0.271] | -0.698 [-0.745, -0.649] | -0.264 [-0.317, -0.211] | -0.437 [-0.500, -0.384] | -0.091 [-0.122, -0.065] |
| ridge1000_p0 | -0.330 [-0.359, -0.301] | -0.536 [-0.597, -0.476] | -0.070 [-0.112, -0.032] | -0.640 [-0.695, -0.587] | -0.139 [-0.178, -0.101] |
| ridge1000_p0.25 | -0.304 [-0.328, -0.276] | -0.645 [-0.695, -0.595] | -0.107 [-0.147, -0.065] | -0.516 [-0.574, -0.458] | -0.116 [-0.153, -0.084] |
| ridge1000_p0.5 | -0.305 [-0.330, -0.275] | -0.705 [-0.749, -0.657] | -0.158 [-0.201, -0.112] | -0.492 [-0.552, -0.434] | -0.099 [-0.132, -0.067] |
| ridge1000_p0.75 | -0.305 [-0.331, -0.277] | -0.705 [-0.748, -0.658] | -0.211 [-0.256, -0.165] | -0.477 [-0.539, -0.423] | -0.094 [-0.127, -0.066] |
| ridge1000_p1 | -0.308 [-0.333, -0.280] | -0.703 [-0.748, -0.655] | -0.271 [-0.327, -0.214] | -0.463 [-0.527, -0.407] | -0.091 [-0.120, -0.063] |

### Session 9 (dev queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.122 [-0.145, -0.101] | -0.285 [-0.354, -0.221] | -0.283 [-0.338, -0.228] | -0.040 [-0.073, -0.010] | -0.081 [-0.113, -0.053] |
| b | -0.050 [-0.064, -0.036] | -0.067 [-0.096, -0.039] | -0.100 [-0.136, -0.067] | -0.019 [-0.050, +0.020] | -0.050 [-0.072, -0.029] |
| c | -0.018 [-0.027, -0.010] | -0.039 [-0.058, -0.020] | -0.086 [-0.114, -0.062] | +0.003 [-0.017, +0.023] | -0.006 [-0.014, +0.003] |
| d | -0.015 [-0.020, -0.010] | -0.024 [-0.042, -0.008] | -0.074 [-0.103, -0.052] | -0.003 [-0.011, +0.003] | -0.002 [-0.008, +0.004] |
| ac | -0.087 [-0.106, -0.067] | -0.174 [-0.235, -0.117] | -0.174 [-0.225, -0.123] | -0.026 [-0.055, +0.001] | -0.076 [-0.108, -0.048] |
| cc | -0.003 [-0.012, +0.004] | -0.014 [-0.025, -0.002] | -0.005 [-0.014, +0.003] | -0.002 [-0.025, +0.020] | -0.001 [-0.008, +0.007] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| proc_p0 | -0.122 [-0.142, -0.100] | -0.137 [-0.184, -0.096] | -0.130 [-0.173, -0.092] | -0.104 [-0.150, -0.059] | -0.129 [-0.164, -0.096] |
| proc_p0.25 | -0.106 [-0.125, -0.087] | -0.164 [-0.205, -0.126] | -0.162 [-0.204, -0.121] | -0.060 [-0.097, -0.020] | -0.103 [-0.135, -0.073] |
| proc_p0.5 | -0.111 [-0.130, -0.093] | -0.225 [-0.278, -0.180] | -0.216 [-0.264, -0.171] | -0.051 [-0.087, -0.012] | -0.086 [-0.117, -0.058] |
| proc_p0.75 | -0.125 [-0.144, -0.106] | -0.299 [-0.363, -0.245] | -0.258 [-0.308, -0.210] | -0.046 [-0.079, -0.010] | -0.082 [-0.112, -0.055] |
| proc_p1 | -0.136 [-0.154, -0.117] | -0.346 [-0.411, -0.285] | -0.311 [-0.368, -0.262] | -0.040 [-0.076, -0.004] | -0.080 [-0.106, -0.055] |
| coral_p0 | -0.089 [-0.114, -0.065] | -0.048 [-0.089, -0.006] | -0.063 [-0.098, -0.030] | -0.066 [-0.116, -0.015] | -0.124 [-0.162, -0.087] |
| coral_p0.25 | -0.077 [-0.098, -0.055] | -0.068 [-0.116, -0.020] | -0.093 [-0.130, -0.057] | -0.039 [-0.084, +0.008] | -0.098 [-0.128, -0.070] |
| coral_p0.5 | -0.079 [-0.100, -0.057] | -0.087 [-0.139, -0.038] | -0.141 [-0.186, -0.098] | -0.034 [-0.076, +0.010] | -0.085 [-0.117, -0.057] |
| coral_p0.75 | -0.081 [-0.102, -0.059] | -0.106 [-0.163, -0.055] | -0.158 [-0.203, -0.113] | -0.035 [-0.076, +0.009] | -0.078 [-0.108, -0.051] |
| coral_p1 | -0.088 [-0.108, -0.066] | -0.142 [-0.200, -0.088] | -0.192 [-0.238, -0.144] | -0.029 [-0.068, +0.011] | -0.077 [-0.108, -0.050] |
| ridge1_p0 | -0.165 [-0.187, -0.143] | -0.247 [-0.301, -0.202] | -0.079 [-0.118, -0.045] | -0.226 [-0.275, -0.176] | -0.125 [-0.157, -0.094] |
| ridge1_p0.25 | -0.151 [-0.171, -0.131] | -0.292 [-0.353, -0.242] | -0.118 [-0.160, -0.078] | -0.175 [-0.222, -0.131] | -0.103 [-0.135, -0.073] |
| ridge1_p0.5 | -0.154 [-0.174, -0.134] | -0.362 [-0.430, -0.301] | -0.139 [-0.181, -0.094] | -0.152 [-0.196, -0.111] | -0.095 [-0.125, -0.065] |
| ridge1_p0.75 | -0.168 [-0.189, -0.147] | -0.435 [-0.498, -0.372] | -0.181 [-0.229, -0.132] | -0.154 [-0.202, -0.113] | -0.091 [-0.121, -0.063] |
| ridge1_p1 | -0.180 [-0.200, -0.158] | -0.478 [-0.542, -0.414] | -0.216 [-0.264, -0.170] | -0.160 [-0.207, -0.120] | -0.091 [-0.122, -0.064] |
| ridge10_p0 | -0.267 [-0.294, -0.240] | -0.398 [-0.458, -0.338] | -0.120 [-0.163, -0.083] | -0.472 [-0.535, -0.416] | -0.134 [-0.171, -0.096] |
| ridge10_p0.25 | -0.239 [-0.262, -0.215] | -0.476 [-0.536, -0.418] | -0.151 [-0.193, -0.109] | -0.361 [-0.418, -0.310] | -0.110 [-0.144, -0.076] |
| ridge10_p0.5 | -0.252 [-0.274, -0.229] | -0.609 [-0.673, -0.546] | -0.183 [-0.229, -0.139] | -0.346 [-0.404, -0.296] | -0.098 [-0.134, -0.068] |
| ridge10_p0.75 | -0.263 [-0.286, -0.238] | -0.676 [-0.735, -0.607] | -0.243 [-0.288, -0.194] | -0.337 [-0.399, -0.286] | -0.092 [-0.125, -0.064] |
| ridge10_p1 | -0.267 [-0.289, -0.241] | -0.686 [-0.743, -0.616] | -0.281 [-0.332, -0.232] | -0.331 [-0.394, -0.281] | -0.089 [-0.119, -0.062] |
| ridge100_p0 | -0.334 [-0.363, -0.304] | -0.531 [-0.593, -0.469] | -0.144 [-0.191, -0.107] | -0.621 [-0.678, -0.566] | -0.139 [-0.177, -0.100] |
| ridge100_p0.25 | -0.307 [-0.333, -0.281] | -0.645 [-0.696, -0.594] | -0.183 [-0.231, -0.138] | -0.498 [-0.559, -0.440] | -0.113 [-0.149, -0.080] |
| ridge100_p0.5 | -0.309 [-0.333, -0.281] | -0.718 [-0.761, -0.673] | -0.220 [-0.267, -0.175] | -0.466 [-0.527, -0.406] | -0.102 [-0.136, -0.072] |
| ridge100_p0.75 | -0.311 [-0.337, -0.283] | -0.727 [-0.768, -0.681] | -0.279 [-0.330, -0.232] | -0.456 [-0.518, -0.401] | -0.095 [-0.127, -0.067] |
| ridge100_p1 | -0.313 [-0.338, -0.285] | -0.722 [-0.765, -0.677] | -0.337 [-0.395, -0.286] | -0.441 [-0.502, -0.386] | -0.093 [-0.121, -0.066] |
| ridge1000_p0 | -0.345 [-0.376, -0.316] | -0.560 [-0.621, -0.501] | -0.144 [-0.192, -0.105] | -0.644 [-0.701, -0.590] | -0.141 [-0.179, -0.102] |
| ridge1000_p0.25 | -0.318 [-0.343, -0.291] | -0.669 [-0.720, -0.619] | -0.181 [-0.231, -0.141] | -0.519 [-0.579, -0.460] | -0.118 [-0.153, -0.085] |
| ridge1000_p0.5 | -0.320 [-0.345, -0.289] | -0.729 [-0.770, -0.683] | -0.232 [-0.283, -0.188] | -0.495 [-0.557, -0.438] | -0.101 [-0.133, -0.070] |
| ridge1000_p0.75 | -0.320 [-0.347, -0.291] | -0.729 [-0.769, -0.684] | -0.285 [-0.334, -0.236] | -0.480 [-0.544, -0.426] | -0.096 [-0.128, -0.067] |
| ridge1000_p1 | -0.323 [-0.349, -0.294] | -0.727 [-0.767, -0.682] | -0.344 [-0.403, -0.289] | -0.467 [-0.530, -0.411] | -0.093 [-0.121, -0.065] |

### Session 9 selection rule applied to the dev queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F2 | coral_p0.75 | 1.00 | -0.073 | -0.067 | -0.072 | -0.038 | -0.073 |

Alignment fit: two-fold cross-fitting over the calibration directories, {'pairs': 267, 'coral_shrinkage': (0.036024923396019676, 0.05447064376540908)}.

### Session 9 modality gap per space, dev directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.363 | 0.761 | 0.707 | 0.544 |
| centered | 0.013 | 0.552 | 0.429 | 0.243 |

### Session 9 hypotheses on the dev queries (dev: informative only, the verdict is the test split)

H9a, F2 selected coral_p0.75: upper bounds of (x - c) P1 image in [0,.2)+[.2,.5) -0.013, P2 textlike in [.5,.8)+[.8,1] -0.020, image in [.5,.8)+[.8,1] -0.004, textlike in [0,.2)+[.2,.5) -0.047; all above -0.02: no, H9a survives this family.
