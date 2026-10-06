# Session 24: pooled estimates over the two GitHub draws, verbatim

Printed by `python3 scripts/pool.py` (5a108f4) in the workspace on 2026-10-05T08:01Z, repo commit a30a27d, from the per-query files the pod pushed (S19: c111c0c and 53d3bfb; S24: 78f2bb8 and a30a27d) and data/notok_code_s19_e1.txt and data/notok_code_s24_e1.txt (the code files E1 did not embed, read from the cache index on the pod). Nothing here is edited. The verdicts and the reading are in results/session24.md.


## Step 1: each draw alone, recomputed from the per-query files and compared with the printed lines

- S19 H19a P1s: c - a: same
  `| E1 | H19a P1s: c - a (primary) | 226 | 86 | +0.193 | [+0.114, +0.277] | [+0.099, +0.295] | inconclusive (fewer than 100 owners) |`
- S19 H19a P2s: c - a: same
  `| E1 | H19a P2s: c - a (primary) | 355 | 98 | +0.166 | [+0.093, +0.241] | [+0.080, +0.260] | inconclusive (fewer than 100 owners) |`
- S19 H19c: c - d where c differs from d: same
  `| E1 | H19c: c - d where c differs from d (primary) | 5381 | 512 | -0.002 | [-0.011, +0.006] | [-0.014, +0.008] | not inferior (lower bound at or above -0.02) |`
- S19 H19b P1s clean: c - a: same
  `| E1 | H19b P1s clean: c - a | 118 | 60 | +0.188 | [+0.090, +0.293] | [+0.071, +0.317] | inconclusive (fewer than 100 owners) |`
- S19 H19b P2s clean: c - a: same
  `| E1 | H19b P2s clean: c - a | 205 | 82 | +0.142 | [+0.063, +0.225] | [+0.045, +0.245] | inconclusive (fewer than 100 owners) |`
- S19 no-code folders, P1s: c - a: same
  `| E1 | no-code folders, P1s: c - a | 67 | 31 | +0.210 | [+0.075, +0.355] | [+0.048, +0.392] | inconclusive (fewer than 100 owners) |`
- S19 no-code folders, P2s: c - a: same
  `| E1 | no-code folders, P2s: c - a | 232 | 62 | +0.096 | [+0.022, +0.173] | [+0.007, +0.190] | inconclusive (fewer than 100 owners) |`
- S19 all of P1 (lone images included): c - a: same
  `| E1 | all of P1 (lone images included): c - a | 500 | 334 | +0.069 | [+0.037, +0.100] | [+0.030, +0.108] | present, size open (lower bound above zero) |`
- S19 all of P2 (lone texts included): c - a: same
  `| E1 | all of P2 (lone texts included): c - a | 512 | 231 | +0.071 | [+0.036, +0.107] | [+0.028, +0.114] | present, size open (lower bound above zero) |`
- S19 cs - d where c differs from d: same
  `| E1 | cs - d where c differs from d | 5381 | 512 | -0.001 | [-0.011, +0.007] | [-0.013, +0.009] | not inferior (lower bound at or above -0.02) |`
- S19 H19d: same
  `H19d statistic (E1): image-heavy directories, 122 queries from 66 owners; gate, recall@5 of d 0.254 (needs 0.10 and more than names alone, 0.066): passed; owner-weighted c - a +0.010 [-0.061, +0.078]; H19d: inconclusive (fewer than 100 owners).`
- S19 H21a: same
  `| H21a (primary): sample - mean, minority, not whole | 310 | 70 | +0.269 | [+0.178, +0.365] | [+0.158, +0.384] | inconclusive (fewer than 100 owners) |`
- S19 H21b: same
  `| H21b (primary): sample - kmeans, all, not whole | 3333 | 207 | -0.042 | [-0.057, -0.029] | [-0.060, -0.026] | inferior (upper bound under -0.02) |`
- S19 H21c: same
  `| H21c (primary): sample - usample, minority, not whole | 310 | 70 | +0.116 | [+0.064, +0.173] | [+0.054, +0.187] | inconclusive (fewer than 100 owners) |`
- S24 H19a P1s: c - a: same
  `| E1 | H19a P1s: c - a (primary) | 506 | 172 | +0.210 | [+0.155, +0.266] | [+0.144, +0.279] | confirmed (lower bound at or above +0.05) |`
- S24 H19a P2s: c - a: same
  `| E1 | H19a P2s: c - a (primary) | 669 | 197 | +0.196 | [+0.144, +0.248] | [+0.133, +0.260] | confirmed (lower bound at or above +0.05) |`
- S24 H19c: c - d where c differs from d: same
  `| E1 | H19c: c - d where c differs from d (primary) | 9729 | 918 | -0.002 | [-0.008, +0.005] | [-0.010, +0.006] | not inferior (lower bound at or above -0.02) |`
- S24 H19b P1s clean: c - a: same
  `| E1 | H19b P1s clean: c - a | 232 | 118 | +0.180 | [+0.113, +0.250] | [+0.099, +0.267] | confirmed (lower bound at or above +0.05) |`
- S24 H19b P2s clean: c - a: same
  `| E1 | H19b P2s clean: c - a | 355 | 155 | +0.209 | [+0.147, +0.275] | [+0.134, +0.288] | confirmed (lower bound at or above +0.05) |`
- S24 no-code folders, P1s: c - a: same
  `| E1 | no-code folders, P1s: c - a | 230 | 67 | +0.169 | [+0.090, +0.252] | [+0.074, +0.270] | inconclusive (fewer than 100 owners) |`
- S24 no-code folders, P2s: c - a: same
  `| E1 | no-code folders, P2s: c - a | 420 | 127 | +0.181 | [+0.120, +0.245] | [+0.107, +0.260] | confirmed (lower bound at or above +0.05) |`
- S24 all of P1 (lone images included): c - a: same
  `| E1 | all of P1 (lone images included): c - a | 1083 | 705 | +0.055 | [+0.034, +0.076] | [+0.029, +0.080] | present, size open (lower bound above zero) |`
- S24 all of P2 (lone texts included): c - a: same
  `| E1 | all of P2 (lone texts included): c - a | 978 | 469 | +0.095 | [+0.065, +0.125] | [+0.060, +0.131] | confirmed (lower bound at or above +0.05) |`
- S24 cs - d where c differs from d: same
  `| E1 | cs - d where c differs from d | 9729 | 918 | -0.002 | [-0.009, +0.004] | [-0.010, +0.005] | not inferior (lower bound at or above -0.02) |`
- S24 H19d: same
  `H19d statistic (E1): image-heavy directories, 271 queries from 138 owners; gate, recall@5 of d 0.258 (needs 0.10 and more than names alone, 0.122): passed; owner-weighted c - a +0.117 [+0.065, +0.169]; H19d: confirmed (lower bound at or above +0.05).`
- S24 H21a: same
  `| H21a (primary): sample - mean, minority, not whole | 672 | 146 | +0.252 | [+0.193, +0.312] | [+0.181, +0.327] | confirmed (lower bound at or above +0.05) |`
- S24 H21b: same
  `| H21b (primary): sample - kmeans, all, not whole | 6294 | 365 | -0.052 | [-0.064, -0.040] | [-0.067, -0.038] | inferior (upper bound under -0.02) |`
- S24 H21c: same
  `| H21c (primary): sample - usample, minority, not whole | 672 | 146 | +0.097 | [+0.061, +0.136] | [+0.054, +0.145] | the kinds matter (lower bound above zero) |`

Reproduced: every line above is the line s19.py or budget.py printed.

## Step 2: pooled over S19 and S24 (owner-weighted mean, 10,000 resamples of owners; a primary test is read on its 98.33 percent interval, a secondary one on its 95 percent interval)

| test | primary | S19 queries, owners, point | S24 queries, owners, point | pooled queries | pooled owners (in both) | pooled point | 95% | 98.33% | reading |
|---|---|---|---|---:|---|---:|---|---|---|
| H24a P1s: c - a (pools H19a P1s) | yes | 226, 86, +0.193 | 506, 172, +0.210 | 732 | 258 (0) | +0.205 | [+0.160, +0.251] | [+0.152, +0.263] | confirmed (lower bound at or above +0.05) |
| H24a P2s: c - a (pools H19a P2s) | yes | 355, 98, +0.166 | 669, 197, +0.196 | 1024 | 294 (1) | +0.186 | [+0.144, +0.229] | [+0.135, +0.238] | confirmed (lower bound at or above +0.05) |
| H24c: c - d where c differs from d (pools H19c) | yes | 5381, 512, -0.002 | 9729, 918, -0.002 | 15110 | 1425 (5) | -0.002 | [-0.007, +0.003] | [-0.008, +0.005] | not inferior (lower bound at or above -0.02) |
| H24b P1s clean: c - a | no | 118, 60, +0.188 | 232, 118, +0.180 | 350 | 178 (0) | +0.182 | [+0.127, +0.240] | [+0.114, +0.253] | confirmed (lower bound at or above +0.05) |
| H24b P2s clean: c - a | no | 205, 82, +0.142 | 355, 155, +0.209 | 560 | 236 (1) | +0.186 | [+0.137, +0.237] | [+0.127, +0.248] | confirmed (lower bound at or above +0.05) |
| no-code folders, P1s: c - a | no | 67, 31, +0.210 | 230, 67, +0.169 | 297 | 98 (0) | +0.182 | [+0.114, +0.255] | [+0.100, +0.270] | inconclusive (fewer than 100 owners) |
| no-code folders, P2s: c - a | no | 232, 62, +0.096 | 420, 127, +0.181 | 652 | 189 (0) | +0.153 | [+0.105, +0.205] | [+0.094, +0.217] | confirmed (lower bound at or above +0.05) |
| all of P1: c - a | no | 500, 334, +0.069 | 1083, 705, +0.055 | 1583 | 1027 (12) | +0.061 | [+0.044, +0.079] | [+0.040, +0.082] | present, size open (lower bound above zero) |
| all of P2: c - a | no | 512, 231, +0.071 | 978, 469, +0.095 | 1490 | 699 (1) | +0.087 | [+0.064, +0.110] | [+0.059, +0.115] | confirmed (lower bound at or above +0.05) |
| cs - d where c differs from d | no | 5381, 512, -0.001 | 9729, 918, -0.002 | 15110 | 1425 (5) | -0.002 | [-0.007, +0.003] | [-0.008, +0.004] | not inferior (lower bound at or above -0.02) |
| H24d: commit subjects, image-heavy directories, c - a (pools H19d) | no | 122, 66, +0.010 | 271, 138, +0.117 | 393 | 203 (1) | +0.083 | [+0.041, +0.126] | [+0.034, +0.135] | present, size open (lower bound above zero); gate: recall@5 of d 0.257, names alone 0.104 |
| H24e and H21a: sample - mean, minority, not whole (2 KiB) | yes | 310, 70, +0.269 | 672, 146, +0.252 | 982 | 216 (0) | +0.258 | [+0.208, +0.310] | [+0.198, +0.321] | confirmed (lower bound at or above +0.05) |
| H24f and H21b: sample - kmeans, all, not whole (2 KiB) | yes | 3333, 207, -0.042 | 6294, 365, -0.052 | 9627 | 572 (0) | -0.048 | [-0.058, -0.040] | [-0.060, -0.037] | inferior (upper bound under -0.02) |
| H24g and H21c: sample - usample, minority, not whole (2 KiB) | yes | 310, 70, +0.116 | 672, 146, +0.097 | 982 | 216 (0) | +0.103 | [+0.073, +0.135] | [+0.067, +0.142] | the kinds matter (lower bound above zero) |

The per-draw points are the owner-weighted means printed in step 1; the pooled reading is the size on this source and is no verdict for H19a or H24a. For H21a, H21b and H21c a cell with fewer than 100 owners on a single draw takes the pooled reading (BRIEF.md, session 24).
