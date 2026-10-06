# Session 27, parts B and C: the budget from one to eight vectors, and the k-means seed

Brief: BRIEF.md, session 27 (commit d23baee, its OpenTimestamps proof in ffe7758, both before any number
below existed). Code: scripts/s27.py and scripts/s27_run.sh (d23baee). Outputs, verbatim:
results/session27_budget_outputs.md (d9a8352); per-query ranks in data/s27_s11_e1.npz to e4,
data/s27seeds_s11_e1.npz to e4 and data/s27_s24_e1.npz, from which `python3 scripts/s27.py report` rebuilds
every number without a vector (rebuilt in the workspace on 5 October: identical to the pod's file).
Figures: results/session27_budget.png and .pdf (uncentered rows) and results/session27_budget_centered.png
and .pdf, drawn by scripts/s27_figure.py from the same files. Run on the MIG pod s46ksd0pdara1o (3.4 vCPUs,
three processes, CPU only, from the cached vectors) on 5 October 2026, 21:21 to 22:08 UTC, in one launch;
the pod stopped itself. Cost about $0.49 (balance $7.25 before, $6.76 after).

## Gates
All passed. Under E1, E2, E3 and E4, the rows a, ac, d, dc, L3 (c), L3c (cc), B2 (tb2) and B2c (tb2c)
equal the stored eval.py ranks for every one of the 17,140 evaluation queries, and under E1 a, L3 and d
also equal the f32 rows of data/ranks_s21_s11_e1. The 27C rows at seed 0 do the same. On G2 (S24, 12,951
queries) a, L3, d and M3 equal data/ranks_s24_e1, whose tbc column makes M3 checked against eval.py on a
real set as well, and the sibling counts equal the flags.

## Reading H27d: the smallest budget not inferior to searching every file
A value qualifies under an encoder if the lower bound of x minus d is at or above -0.02 over all queries
and in P1, P2, M1 and M2 (paired directory bootstrap, eval.py's cell seeds). From the outputs:

| family | E1 | E2 | E3 | E4 | all four |
|---|---|---|---|---|---|
| labelled, uncentered | 4 (4, 5) | 4 (4, 5) | 3 (3, 4, 5) | 4 (4, 5) | 4 |
| labelled, centered | 3 (3, 4, 5) | 3 (3, 4, 5) | 3 (3, 4, 5) | 4 (4, 5) | 4 |
| blind, uncentered | 6 (6, 8) | 8 (8) | 5 (5, 6, 8) | none | none |
| blind, centered | 4 (4, 5, 6, 8) | 5 (5, 6, 8) | 5 (5, 6, 8) | 8 (8) | 8 |
| blind at the labelled budget, uncentered | 3 (3, 4, 5) | 3 (3, 4, 5) | 3 (3, 4, 5) | none | none |
| blind at the labelled budget, centered | 2 (2, 3, 4, 5) | 2 (2, 3, 4, 5) | 4 (4, 5) | 3 (3, 4, 5) | 4 |

1. **Labelled.** Four centroids per label (L4, 6.02 vectors per folder on S11) is the smallest labelled
   budget that qualifies under all four encoders, uncentered or centered. Three per label (c, 5.20 vectors)
   qualifies uncentered under E3 only; its binding cells are M1 under E1 (lower bound -0.021), M2 under E2
   (-0.025) and P2 under E4 (-0.024), as session 25 found when it re-read session 20's intervals. Centered,
   three per label qualifies under E1, E2 and E3. One and two per label never qualify.
2. **Blind.** Uncentered blind k-means does not qualify under E4 at any K up to eight. Centered, it needs
   eight clusters (6.13 vectors) to qualify under all four encoders; under E1 four are enough.
3. **Blind at the labelled count.** Centered, the blind split qualifies at four under all four encoders and
   at two under E1 and E2. Uncentered, it never qualifies under E4, where its binding cell is P1 from two per
   label up (lower bounds -0.064 to -0.030).
4. **Centered rows pass the flat walk.** With about six vectors, the centered rows are above d over all
   queries under every encoder: L4c minus d +0.010 [+0.006, +0.014] under E1, +0.007 [+0.003, +0.011] under
   E2, +0.003 [-0.000, +0.005] under E3 and +0.004 [+0.000, +0.008] under E4, with M4c and B8c close to them.
   Under E1 the gain sits in the minority cells (L4c minus d +0.028 in P1 and +0.045 in P2).

What the brief fixed it to mean: "a budget rule between two and five was not pre-registered here and is the
one open experiment we would run next" becomes four representatives per label, not inferior to every file in
every cell under all four encoders, where three hold under one encoder uncentered and three of four centered.

## Labels at the same number of vectors
Lk minus Mk, folder by folder at the same count (outputs, "Labelled minus blind"). At one and two per label the
labels move recall from the majority files to the minority ones: at k = 1, uncentered, P1 +0.013, +0.007,
+0.013 and +0.004 and P2 +0.013, +0.027, +0.027 and +0.000 under E1 to E4, against M1 -0.029, -0.028, -0.020
and -0.018; over all queries the blind split is level or ahead (-0.010 to -0.005). From three per label up the
two are within 0.015 in every cell under E1 to E3 (over all queries -0.007 to +0.000). Under E4,
uncentered, the labels keep P1 ahead at every count (+0.014 [+0.000, +0.028] at three, +0.010 at four,
+0.014 [+0.005, +0.024] at five). The labels buy the split of the budget across kinds, which matters when
the budget is small and under the dual tower E4.

## Reading H27e: the k-means seed
The largest spread of recall@5 across random_state 0, 1 and 2, over the five cells and four encoders:
- c (L3): 0.0026 (E2, P1). Below the 0.005 the brief expected. c minus a moves by the same amounts, a having
  no seed; under E1 it is +0.253, +0.254 and +0.253 in P1 across the three seeds.
- tb2c (B2c): 0.0084 (E4, M2). Above the 0.005 the brief expected; two clusters depend more on the start.
Per-seed numbers for every cell and encoder are in the outputs.

## Secondary: G2 (S24) under E1, owner-weighted
1,473 owners over all 12,951 queries, 172 in P1s, 197 in P2s. No row qualifies by the same margin in P1s
and P2s, where the owner-clustered intervals are wider: L4 minus d is -0.007 [-0.010, -0.003] over all queries,
-0.015 [-0.031, -0.002] in P1s and -0.018 [-0.033, -0.005] in P2s; L5 -0.011 [-0.028, +0.003] and -0.015
[-0.029, -0.003]. The order of the families is the one S11 shows: two blind vectors lose most in the minority
cells (B2 minus d -0.068 and -0.080), and from four or five vectors labelled and blind rows are within about
0.01 of each other. No verdict was registered here.

## Deviations
- None in 27B or 27C. Rows, seeds, cells and intervals are those of the brief; the second figure (centered
  rows) is an addition. M3 had no stored ranks on S11, as the brief says; on G2 it was checked against tbc.
- 27A, recorded here because it happened in the same run: the sample and the payload of the tool were built
  as registered. Two display fixes followed before anyone wrote a query (029cb4b: superscript and subscript
  digits masked too; bac89e2: hidden numbers shown as [num], with a note on files of numbers only). They are
  in results/session27.md with the rest of 27A.

## The pre-registration (BRIEF.md, verbatim: the common definitions, 27B, 27C and the gates)

> ## Common definitions (fixed now)
> - Set: S11 (2,597 ranked folders, 25,990 files) and its evaluation split (calibration seed 20261102,
>   20 percent, stratified, as in every S11 session). Encoders E1 to E4 with their S11 caches and ok sets.
>   E1 is primary.
> - Image fraction: a folder's share of files labelled image (data/dirs_s11.jsonl), bucketed as eval.py
>   buckets it: [0,.2), [.2,.5), [.5,.8), [.8,1]. Text-like labels: text, table, pdf_text, other.
> - Family: the first creator of the folder's record, lowercased (session 17). The four digitization
>   series: session 17's.
>
>
> ## 27B. The budget from one to eight vectors
>
> - Queries: the S11 evaluation queries of each encoder (17,140 under E1), leave-one-out as eval.py: the
>   query's own folder is rebuilt without it, every other folder keeps its full representation, a folder
>   scores its best cosine, rank 1 plus the number of folders scoring strictly higher, in float32.
> - Rows, each uncentered and centered (suffix c; eval.py's centered space at calibration seed 20261102,
>   the query centered with its own group's mean), all built with eval.py's kreps (scikit-learn KMeans,
>   n_init 10, random_state 0, centroids renormalised):
>   - Lk, labelled, k = 1 to 5: per label, min(k, n_label) centroids. L3 is c and L3c is cc.
>   - BK, blind, K in 2, 3, 4, 5, 6, 8: min(K, n) centroids over all of the folder's vectors. B2 is tb2 and
>     B2c is tb2c.
>   - Mk, blind at the labelled budget, k = 1 to 5: over all of the folder's vectors, as many centroids as
>     Lk keeps for that folder (the sum over labels of min(k, n_label), counted on the folder as built).
>     M3 is session 9's tbc.
>   - References: a, ac, d, dc.
> - Reported per encoder: recall@5 (recall@1 and @10 beside) over all queries and in P1, P2, M1, M2; the
>   mean number of vectors per folder; x minus d and x minus c with paired 95 percent intervals from 1,000
>   resamples of directories at eval.py's cell seeds (all 1, P1 50, P2 51, M1 56, M2 57).
> - Reading H27d (a reading, not a kill test): per family (L, Lc, B, Bc, M, Mc), the smallest k or K at
>   which the lower bound of x minus d is at or above -0.02 over all queries and in P1, P2, M1 and M2,
>   under each encoder and under all four together, or "none". And at an equal number of centroids in
>   every folder, Lk minus Mk over all queries and in each cell, per encoder, with its interval: what the
>   labels buy when the count is held fixed. A figure: recall@5 against vectors per folder, one panel per
>   cell, labelled and blind, four encoders.
> - What it means for the paper: the smallest qualifying budget replaces "a budget rule between two and
>   five was not pre-registered here and is the one open experiment we would run next". If no labelled
>   budget up to five qualifies under an encoder, the paper says so for that encoder. If Mk matches Lk at
>   every k, the labels buy only the split of the budget, as the Discussion already says.
> - Secondary, if the volume holds the S24 E1 cache: the uncentered L, B and M rows with a and d on G2
>   under E1 (calibration seed 20261104), owner-weighted over all queries, P1s and P2s (s19.oboot, 10,000
>   resamples of owners; seeds 27101 to 27103), x minus d and x minus c. No verdict.
>
> ## 27C. The k-means seed
>
> - c (L3) and tb2c (B2c) rebuilt with random_state 0, 1 and 2 under all four encoders, otherwise as 27B,
>   with a beside them.
> - Reading H27e: the largest spread (largest minus smallest) of recall@5 across the three seeds over the
>   five cells under any encoder, and the same for c minus a. Expected below 0.005, not a test. Per-seed
>   numbers reported.
>
> ## Gates (the scripts stop before any new number of a set if one fails)
> - 27B and 27C, per encoder: the rows a, ac, d, dc, L3, L3c, B2 and B2c (and L3s0, B2cs0 in 27C) equal,
>   for every evaluation query, the eval.py ranks stored on the volume (ranks_s11_e1, ranks_s11_e2,
>   ranks_s14_e3, ranks_s15_e4, which hold a, ac, c, cc, d, dc, tb2 and tb2c), and under E1 also the f32
>   rows of data/ranks_s21_s11_e1. M3 equals eval.py's tbc on the synthetic set of the self-test; no
>   stored file holds tbc on S11. On G2: a, c and d equal data/ranks_s24_e1, and the counts of siblings equal the
>   flags. A set that fails is reported as FAILED with none of its new numbers.
> - 27A: the sample reproduces data/humanq_sample_s11.jsonl byte for byte, and under each encoder the
>   scorer reproduces descq.py's ranks of a, c and d on the S11 titles (session 17's dumps,
>   /workspace/logs/s17/descq_ranks_e1 to e4) before any human query is scored.
>
