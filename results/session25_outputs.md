# Session 25 outputs, verbatim (scripts/s25.py)

## Gates

- pool.py's Draw on S19: 14 printed lines reproduced, 0 different, 0 not run.
- pool.py's Draw on S24: 14 printed lines reproduced, 0 different, 0 not run.
- S11 recall@5 of a (f32), all P1 P2 M1 M2: here (0.692, 0.421, 0.37, 0.73, 0.83); session 11 (0.692, 0.421, 0.37, 0.73, 0.83); same
- S11 recall@5 of c (f32), all P1 P2 M1 M2: here (0.796, 0.674, 0.539, 0.81, 0.894); session 11 (0.796, 0.674, 0.539, 0.81, 0.894); same
- S11 recall@5 of d (f32), all P1 P2 M1 M2: here (0.804, 0.685, 0.551, 0.821, 0.897); session 11 (0.804, 0.685, 0.551, 0.821, 0.897); same
- S11 c - a in P1, eval.py's directory interval: here +0.253 [+0.214, +0.294]; published +0.253 [+0.214, +0.294]; same
- S11 c - a in P2, eval.py's directory interval: here +0.169 [+0.136, +0.200]; published +0.169 [+0.136, +0.200]; same
- S11 family-weighted c - a in P1: here +0.133 [+0.103, +0.163]; session 17 +0.133 [+0.103, +0.163]; same
- S11 family-weighted c - a in P2: here +0.137 [+0.110, +0.164]; session 17 +0.137 [+0.110, +0.164]; same

All gates passed.

## 1. GitHub at the natural mix (E1, c - a)

Owner-weighted: the mean over owners of the owner's mean, 95 percent interval from 10,000 resamples of owners (s19.oboot). Pooled: both draws' queries, an owner in both counted once.

| draw | queries | subset | queries in it | owners | c - a |
|---|---:|---|---:|---:|---|
| S19 | 7372 | all queries | 7372 | 858 | +0.020 [+0.009, +0.030] |
| S19 | 7372 | mixed directories | 4482 | 593 | +0.035 [+0.021, +0.048] |
| S19 | 7372 | other directories | 2890 | 316 | -0.009 [-0.021, +0.004] |
| S24 | 12951 | all queries | 12951 | 1473 | +0.019 [+0.010, +0.028] |
| S24 | 12951 | mixed directories | 9991 | 1229 | +0.028 [+0.018, +0.039] |
| S24 | 12951 | other directories | 2960 | 308 | -0.026 [-0.038, -0.014] |
| pooled | 20323 | all queries | 20323 | 2313 | +0.019 [+0.012, +0.026] |
| pooled | 20323 | mixed directories | 14473 | 1806 | +0.030 [+0.022, +0.039] |
| pooled | 20323 | other directories | 5850 | 624 | -0.017 [-0.026, -0.008] |

Natural mix: the mean over directories of each directory's mean c - a, within mixed and other directories, combined with the eligible share of mixed directories; 95 percent interval from 10,000 resamples of owners. The scored set takes at most two mixed and two other directories per repository, so each stratum is a sample of its eligible directories, not a uniform draw.

| draw | eligible share mixed | mixed directories | other directories | owners | natural-mix c - a | directory-weighted, mixed | directory-weighted, other |
|---|---:|---:|---:|---:|---|---:|---:|
| S19 | 1501/35970 = 0.042 | 702 | 470 | 858 | -0.006 [-0.019, +0.008] | +0.032 | -0.008 |
| S24 | 3286/65984 = 0.050 | 1457 | 466 | 1473 | -0.021 [-0.033, -0.010] | +0.027 | -0.024 |
| pooled | 4787/101954 = 0.047 | 2159 | 936 | 2313 | -0.014 [-0.022, -0.005] | +0.029 | -0.016 |

## 2. S11 where c is a strict compression (E1, c_f32 - d_f32)

Files without a vector by the manifest rule: 320 of 25990. Evaluation queries the rule counts as without a vector: 0 of 17140. A query's folder compresses strictly if, the query left out, some label keeps more than three files: 13247 of 17140 queries (0.773) over 1268 of 2035 directories.

| cell | queries | strict | share strict | c - d, strict [95% directories] | c - d, not strict [95%] | c - d, all [95%] |
|---|---:|---:|---:|---|---|---|
| all | 17140 | 13247 | 0.773 | -0.006 [-0.011, -0.002] | -0.014 [-0.020, -0.009] | -0.008 [-0.012, -0.005] |
| P1 | 1959 | 1470 | 0.750 | -0.007 [-0.016, +0.003] | -0.020 [-0.040, -0.002] | -0.010 [-0.019, -0.003] |
| P2 | 2146 | 1712 | 0.798 | -0.015 [-0.022, -0.008] | -0.002 [-0.011, +0.005] | -0.012 [-0.018, -0.007] |
| M1 | 5571 | 3997 | 0.717 | -0.010 [-0.022, +0.002] | -0.015 [-0.025, -0.007] | -0.011 [-0.021, -0.003] |
| M2 | 7272 | 5922 | 0.814 | -0.001 [-0.005, +0.004] | -0.013 [-0.020, -0.007] | -0.003 [-0.007, +0.001] |

## 3. S11 read as the GitHub draws are read (E1, c - a)

P1s and P2s keep the queries whose folder, the query left out, holds another file of the query's input group (same file count as item 2). Family-weighted: every creator family counts once, 95 percent interval from 1,000 resamples of families (validity.boot_mean, weighted). Query-weighted: the paper's estimate, with eval.py's directory interval.

| cell | queries | directories | families (effective) | query-weighted [95% directories] | family-weighted [95% families] |
|---|---:|---:|---|---|---|
| P1 | 1959 | 832 | 731 (204) | +0.253 [+0.214, +0.294] | +0.133 [+0.103, +0.163] |
| P2 | 2146 | 1044 | 626 (47) | +0.169 [+0.136, +0.200] | +0.137 [+0.110, +0.164] |
| P1s | 1545 | 418 | 373 (140) | +0.324 [+0.276, +0.372] | +0.266 [+0.224, +0.313] |
| P2s | 1673 | 571 | 360 (31) | +0.218 [+0.179, +0.256] | +0.239 [+0.199, +0.276] |

Lone queries (no other file of their input group in the folder): P1 414 of 1959, P2 473 of 2146.

## 4. A budget curve (E1): recall@5 by bytes per folder

Session 21's per-query ranks. S11 query-weighted; GitHub owner-weighted (both draws' queries, an owner in both counted once). Minority: P1s and P2s.

### S11: 17140 queries, 3218 minority

| summary | 512 B, all | 512 B, minority | 1024 B, all | 1024 B, minority | 2048 B, all | 2048 B, minority | 4096 B, all | 4096 B, minority | 8192 B, all | 8192 B, minority |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mean | 0.692 | 0.443 | 0.694 | 0.443 | 0.692 | 0.441 | 0.692 | 0.440 | 0.692 | 0.440 |
| kmeans | 0.762 | 0.675 | 0.782 | 0.706 | 0.798 | 0.712 | 0.802 | 0.718 | 0.804 | 0.719 |
| kkind | 0.739 | 0.638 | 0.781 | 0.702 | 0.796 | 0.709 | 0.802 | 0.717 | 0.804 | 0.719 |
| sample | 0.590 | 0.554 | 0.690 | 0.641 | 0.754 | 0.694 | 0.788 | 0.716 | 0.801 | 0.720 |
| allbits | 0.697 | 0.603 | 0.746 | 0.662 | 0.789 | 0.702 | 0.800 | 0.716 | 0.803 | 0.719 |

### GitHub: 20323 queries, 1756 minority, 2313 owners (536 in the minority cell)

| summary | 512 B, all | 512 B, minority | 1024 B, all | 1024 B, minority | 2048 B, all | 2048 B, minority | 4096 B, all | 4096 B, minority | 8192 B, all | 8192 B, minority |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mean | 0.645 | 0.420 | 0.647 | 0.417 | 0.650 | 0.420 | 0.650 | 0.421 | 0.650 | 0.421 |
| kmeans | 0.661 | 0.570 | 0.667 | 0.619 | 0.669 | 0.635 | 0.671 | 0.642 | 0.671 | 0.643 |
| kkind | 0.659 | 0.603 | 0.666 | 0.621 | 0.668 | 0.632 | 0.670 | 0.641 | 0.671 | 0.643 |
| sample | 0.570 | 0.561 | 0.645 | 0.618 | 0.666 | 0.636 | 0.670 | 0.643 | 0.671 | 0.644 |
| allbits | 0.549 | 0.498 | 0.625 | 0.574 | 0.660 | 0.621 | 0.669 | 0.633 | 0.671 | 0.642 |

### Labels against blind centroids at 2,048 bytes: kkind - kmeans (95 percent interval; directories on S11, owners on GitHub)

| set | all | minority |
|---|---|---|
| S11 | -0.002 [-0.004, -0.000] | -0.002 [-0.007, +0.004] |
| GitHub | -0.001 [-0.002, -0.000] (2313 owners) | -0.003 [-0.011, +0.004] (536 owners) |

## 5. The number of candidate folders (E1, post hoc; BRIEF.md, session 25, item 5)

Expected recall@5 when the candidates are the own folder and n - 1 others drawn at random.

### S11 (N = 2,597), query-weighted; c - a with its 95 percent directory interval

| candidates | cell | a | c | d | c - a |
|---:|---|---:|---:|---:|---|
| 10 | all | 0.983 | 0.989 | 0.989 | +0.006 [+0.004, +0.007] |
| 10 | P1 | 0.954 | 0.967 | 0.967 | +0.014 [+0.007, +0.021] |
| 10 | P2 | 0.930 | 0.963 | 0.965 | +0.032 [+0.025, +0.042] |
| 30 | all | 0.952 | 0.971 | 0.972 | +0.019 [+0.016, +0.022] |
| 30 | P1 | 0.864 | 0.912 | 0.913 | +0.049 [+0.034, +0.065] |
| 30 | P2 | 0.823 | 0.916 | 0.919 | +0.093 [+0.078, +0.110] |
| 100 | all | 0.884 | 0.928 | 0.929 | +0.044 [+0.039, +0.048] |
| 100 | P1 | 0.742 | 0.856 | 0.858 | +0.114 [+0.090, +0.141] |
| 100 | P2 | 0.611 | 0.751 | 0.757 | +0.140 [+0.119, +0.164] |
| 300 | all | 0.818 | 0.884 | 0.887 | +0.066 [+0.059, +0.073] |
| 300 | P1 | 0.622 | 0.806 | 0.813 | +0.184 [+0.150, +0.221] |
| 300 | P2 | 0.517 | 0.652 | 0.657 | +0.135 [+0.108, +0.161] |
| 1000 | all | 0.751 | 0.837 | 0.842 | +0.087 [+0.078, +0.096] |
| 1000 | P1 | 0.501 | 0.733 | 0.745 | +0.232 [+0.194, +0.266] |
| 1000 | P2 | 0.432 | 0.583 | 0.593 | +0.152 [+0.123, +0.184] |
| 2597 | all | 0.692 | 0.796 | 0.804 | +0.104 [+0.094, +0.116] |
| 2597 | P1 | 0.421 | 0.674 | 0.685 | +0.253 [+0.213, +0.294] |
| 2597 | P2 | 0.370 | 0.539 | 0.551 | +0.169 [+0.138, +0.201] |

### GitHub (G1 N = 1,600, G2 N = 2,600), owner-weighted over both draws; c - a with its 95 percent owner interval

| candidates | cell | a | c | d | c - a |
|---:|---|---:|---:|---:|---|
| 10 | all | 0.914 | 0.917 | 0.920 | +0.003 [+0.001, +0.006] |
| 10 | P1s | 0.962 | 0.976 | 0.976 | +0.013 [+0.002, +0.027] |
| 10 | P2s | 0.904 | 0.952 | 0.957 | +0.049 [+0.029, +0.070] |
| 30 | all | 0.851 | 0.859 | 0.863 | +0.008 [+0.004, +0.011] |
| 30 | P1s | 0.809 | 0.880 | 0.876 | +0.071 [+0.044, +0.099] |
| 30 | P2s | 0.759 | 0.878 | 0.888 | +0.119 [+0.088, +0.151] |
| 100 | all | 0.791 | 0.805 | 0.811 | +0.014 [+0.009, +0.019] |
| 100 | P1s | 0.663 | 0.801 | 0.802 | +0.138 [+0.100, +0.177] |
| 100 | P2s | 0.641 | 0.803 | 0.812 | +0.161 [+0.127, +0.197] |
| 300 | all | 0.742 | 0.754 | 0.760 | +0.011 [+0.006, +0.017] |
| 300 | P1s | 0.575 | 0.724 | 0.734 | +0.149 [+0.110, +0.191] |
| 300 | P2s | 0.569 | 0.736 | 0.750 | +0.167 [+0.131, +0.202] |
| 1000 | all | 0.687 | 0.703 | 0.709 | +0.016 [+0.010, +0.022] |
| 1000 | P1s | 0.466 | 0.654 | 0.674 | +0.188 [+0.145, +0.232] |
| 1000 | P2s | 0.495 | 0.678 | 0.693 | +0.183 [+0.144, +0.223] |
| full | all | 0.650 | 0.669 | 0.674 | +0.019 [+0.012, +0.026] |
| full | P1s | 0.400 | 0.605 | 0.626 | +0.205 [+0.160, +0.250] |
| full | P2s | 0.449 | 0.635 | 0.657 | +0.186 [+0.143, +0.230] |

