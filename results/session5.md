# dirvec session 5: scale

Question: does the session 4 result (two-stage retrieval with c at k = 10 matches the flat walk d
at half the scoring) hold on every remaining eligible directory of the pool, and how does it
compare with an approximate flat index?
Encoder, revision, input rules (with the session 4 .xls rule) and ground truth rules as in session 4.
Embedding: jina-embeddings-v4, revision 853c867b, bfloat16, text mode query; 8,501 cache rows on an
NVIDIA RTX PRO 6000 Blackwell and 19,044 on a MIG 1g.24gb slice of the same card (the pod was
swapped mid-session). Retrieval and timing on CPU (3.4 vCPUs by cgroup; numpy 2.5.2,
scikit-learn 1.9.1, hnswlib 0.8.0), one BLAS thread for query times, each timing run alone.

## Hypothesis (copied verbatim from BRIEF.md, fixed before the first eval run)

H5: on the large set, two-stage retrieval with c and k = 10 loses no more than 0.01 hit@10 against
the exact flat walk d, and scores at most half the vectors.
Kill: if the paired 95% bootstrap interval (1000 resamples over directories) of hit@10, two-stage
c at k = 10 minus exact d, lies entirely below -0.01 over all queries, H5 is dead. Report it
plainly either way.
Secondary, reported, no kill: the same for a and b; the session 3 primary cells (c - a, recall@5)
on the large set; an approximate flat baseline (HNSW over all file vectors) with its recall
against exact d, its index size and its query time; two-stage with an HNSW over the
representatives as stage 1.

## Verdict

H5 is not dead under its kill criterion. Over all 23,119 queries, hit@10 of two-stage c at k = 10
minus exact d is -0.001, 95% CI [-0.003, +0.001]; the interval does not lie below -0.01, and it
contains zero.
The cost half of H5 is false as stated: c at k = 10 scores 14,965 vectors per query against 27,242
for d, a share of 0.55, not at most half. The kill criterion tests only the recall half, so H5
survives the kill and fails its second clause. Both halves are reported here; neither is
reinterpreted.

## Summary

1. Recall: c at k = 10 is within 0.001 of d on hit@1 (0.681 against 0.682) and hit@10 (0.797
   against 0.798), intervals containing zero. Same as on 400 directories in session 4.
2. Cost: the share went up from 0.48 and 0.49 (session 4) to 0.55. Stage 1 alone is 14,803
   representatives, 0.54 of the file vectors, because the large set has fewer files per directory
   (9.70 against 11.82 and 12.12) while c keeps 5.27 representatives per directory. c pays for its
   recall with a stage 1 that is about as large as half the corpus; it is not a small index.
   Brute force query time: c at k = 10 2,893 us against 5,191 us flat, 0.56.
3. a and b at k = 10 lose more than 0.01 hit@10: a -0.085 [-0.092, -0.077], b -0.024
   [-0.029, -0.019]. Under the H5 rule both would be dead. They score 0.11 and 0.27 of the vectors.
4. Session 3 primary cells, recall@5: c - a is +0.238 [+0.207, +0.268] (P1, image queries in
   [0,.2)+[.2,.5)) and +0.233 [+0.207, +0.262] (P2, text-like queries in [.5,.8)+[.8,1]). The
   session 3 hypothesis holds on the large set, with larger gaps than on 400 directories
   (+0.188 and +0.197 in session 4). d is still not beaten: d - c at recall@5 is +0.007
   [+0.001, +0.014] and +0.012 [+0.007, +0.016] in those cells.
5. The approximate flat baseline changes the cost picture. HNSW over the 27,243 file vectors
   (M = 16, ef_construction = 200) at ef_search 64 has recall@10 0.991 against exact d and loses
   0.006 hit@10 [-0.007, -0.005] at 232 us per query, 22 times faster than brute force d and
   12 times faster than brute force two-stage c at k = 10.
6. Two-stage with HNSW over the c representatives as stage 1 (ef_search 100, 100 representatives,
   exact stage 2 over 10 directories) keeps the exact two-stage recall (hit@10 -0.001
   [-0.003, +0.000], directory overlap 0.998) at 359 us. Against flat HNSW this is slower than
   ef_search 64 (232 us, -0.006) and faster than ef_search 128 (402 us, -0.004) and 256 (711 us,
   -0.003), with a loss closer to zero than any flat HNSW setting tried. Near 0.4 ms the gap is
   0.003 hit@10 (-0.001 against -0.004 at ef_search 128), a difference no interval here tests.
   Against an approximate flat index the container layer does not buy speed; at best it buys a
   few thousandths of hit@10 at similar speed.
7. Storage: the flat HNSW index is 227.2 MB. Two-stage with HNSW over c needs its 123.5 MB index
   plus the 223.2 MB of file vectors for stage 2, 346.7 MB, 1.53 times the flat HNSW.
8. Scale caveat: 2,808 directories (7 times session 4) and 27,243 embedded files (5.7 times) is still small.
   Brute force d takes 5 ms here. The HNSW numbers are the ones that carry over to larger trees.

All queries, k = 10 for two-stage, one thread:

| method | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | vectors scored | share of flat | us per query | index MB |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| d, exact flat (brute force) | 0.682 | 0.798 | | | 27242 | 1.00 | 5191 | 223.2 |
| a, exact two-stage | 0.624 | 0.713 | -0.085 | [-0.092, -0.077] | 2951 | 0.11 | 456 | 246.2 |
| b, exact two-stage | 0.667 | 0.774 | -0.024 | [-0.029, -0.019] | 7325 | 0.27 | 1432 | 281.9 |
| c, exact two-stage | 0.681 | 0.797 | -0.001 | [-0.003, +0.001] | 14965 | 0.55 | 2893 | 344.4 |
| flat HNSW, ef 64 | 0.678 | 0.793 | -0.006 | [-0.007, -0.005] | | | 232 | 227.2 |
| flat HNSW, ef 128 | 0.679 | 0.794 | -0.004 | [-0.005, -0.003] | | | 402 | 227.2 |
| c, HNSW stage 1, ef 100 | 0.682 | 0.797 | -0.001 | [-0.003, +0.000] | | | 359 | 346.7 |

Index MB for the exact rows: vectors at 2048 float32 (two-stage: representatives plus file vectors).
For the HNSW rows: hnswlib index file size (two-stage: plus 223.2 MB of file vectors). Brute force
and HNSW times come from two runs (`twostage.py --timing`, `hnsw.py`) on the same pod, each alone.

## The set (steps 1 to 4)

Selection (step 1, `data/selection_s5.jsonl`): every eligible record of the pool not in the session 1
or session 3 selections, same eligibility, caps and licences. 2,809 records, 27,562 files, 28.97 GB.
Records per bucket (pool image_frac): [0,.2) 433, [.2,.5) 1,007, [.5,.8) 1,055, [.8,1] 314.

Download (step 2): 27,545 of 27,562 files, md5-verified by `fetch.py`. Record 22672636 (17 files,
bucket [0,.2), cc-by-4.0) returned HTTP 403 for every file on two runs; the Zenodo API now lists it
as access_right restricted, updated 2026-09-28, after the pool was built. It is not in the set.
All other transfer failures (IncompleteRead) succeeded on retry.

Manifest and ground truth (step 3): 2,808 directories, 27,545 files. The set is not balanced.
Buckets below are recomputed from the files on disk and differ slightly from the pool buckets.

| bucket | directories | files | embedded files | qualifying directories | queries (ground truth) | queries with a vector |
|---|---:|---:|---:|---:|---:|---:|
| [0,.2) | 459 | 6633 | 6479 | 455 | 6049 | 5899 |
| [.2,.5) | 1005 | 8095 | 8005 | 992 | 7426 | 7349 |
| [.5,.8) | 1034 | 8763 | 8719 | 1016 | 6874 | 6838 |
| [.8,1] | 310 | 4054 | 4040 | 306 | 3058 | 3044 |
| all | 2808 | 27545 | 27243 | 2769 | 23407 | 23130 |

Modalities on disk: image 12,279, text 5,872, table 5,353, pdf_text 2,604, other 1,107,
pdf_scanned 330; 121 unreadable images, 1 pdfinfo failure.
Dedupe (`build_gt.py`): 882 exact duplicate pairs (601 across directories), 3,368 near-duplicate
image pairs (1,038 across), 2,484 near-duplicate text pairs (1,822 across); 4,071 files excluded as
queries as duplicates, 72 as degenerate images. Kill criterion of session 1 (at least 200
qualifying directories, at least 40 per bucket): passed.

Cache (step 4, `data/emb/jina-embeddings-v4_s5/`): 27,243 ok, 302 skipped by the fixed input rules
(115 unreadable tif classed other, 58 pptx, 42 without extension, 36 doc, 11 images under 28 px,
10 empty text, 8 WMF, 6 png and 1 pdf classed other, 5 odp, 4 corrupt zip, 4 .xls that are
xlsx, 1 corrupt docx, 1 xlsx that openpyxl rejects).
Ok by modality: image 12,260, text 5,870, table 5,342, pdf_text 2,604, other 837, pdf_scanned 330.
Queries dropped for lack of a vector: 277; 11 more have no embedded sibling and are dropped from
the file-level numbers of steps 5 and 6.

## Step 5: two-stage on the large set

Output of `python scripts/twostage.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s5
--manifest data/manifest_s5.jsonl --dirs data/dirs_s5.jsonl --gt data/gt_structural_s5.jsonl
--timing --timing-queries 2000`. Definitions as in `results/session4.md`, method. Every query was
evaluated (the per-query leave-one-out k-means took under 10 minutes on 3 vCPUs), so `--sample`
was not used. Query time over 2,000 queries drawn with a fixed seed.

Model: jina-embeddings-v4, cache jina-embeddings-v4_s5. Queries with a vector: 23130; with at least one embedded sibling: 23119 (11 dropped from the file-level numbers). 2808 directories ranked, 27243 embedded files.

### Index size

| index | vectors | vectors per directory | MB at 2048 float32 | with file vectors for stage 2: vectors | MB |
|---|---:|---:|---:|---:|---:|
| a | 2808 | 1.00 | 23.0 | 30051 | 246.2 |
| b | 7172 | 2.55 | 58.8 | 34415 | 281.9 |
| c | 14803 | 5.27 | 121.3 | 42046 | 344.4 |
| d | 27243 | 9.70 | 223.2 | 27243 | 223.2 |

### all queries: 23119 queries over 2756 directories

| stage 1 | k | dir recall@k | hit@1 | hit@5 | hit@10 | sib@10 | vectors scored | hit@1 minus d | 95% CI | hit@10 minus d | 95% CI | sib@10 minus d | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| a | 1 | 0.555 | 0.555 | 0.555 | 0.555 | 0.555 | 2824 | -0.127 | [-0.139, -0.115] | -0.244 | [-0.256, -0.231] | +0.113 | [+0.102, +0.123] |
| a | 3 | 0.648 | 0.590 | 0.641 | 0.646 | 0.465 | 2853 | -0.092 | [-0.101, -0.083] | -0.152 | [-0.163, -0.141] | +0.023 | [+0.017, +0.029] |
| a | 5 | 0.686 | 0.607 | 0.668 | 0.680 | 0.451 | 2881 | -0.074 | [-0.082, -0.067] | -0.118 | [-0.127, -0.109] | +0.009 | [+0.004, +0.013] |
| a | 10 | 0.734 | 0.624 | 0.690 | 0.713 | 0.442 | 2951 | -0.058 | [-0.064, -0.052] | -0.085 | [-0.092, -0.077] | -0.000 | [-0.004, +0.003] |
| b | 1 | 0.637 | 0.637 | 0.637 | 0.637 | 0.637 | 7189 | -0.045 | [-0.053, -0.036] | -0.161 | [-0.172, -0.151] | +0.195 | [+0.185, +0.205] |
| b | 3 | 0.723 | 0.652 | 0.717 | 0.722 | 0.492 | 7220 | -0.030 | [-0.036, -0.025] | -0.077 | [-0.085, -0.069] | +0.049 | [+0.045, +0.053] |
| b | 5 | 0.756 | 0.660 | 0.737 | 0.751 | 0.464 | 7250 | -0.022 | [-0.027, -0.018] | -0.047 | [-0.053, -0.041] | +0.022 | [+0.019, +0.024] |
| b | 10 | 0.795 | 0.667 | 0.745 | 0.774 | 0.449 | 7325 | -0.014 | [-0.018, -0.011] | -0.024 | [-0.029, -0.019] | +0.007 | [+0.005, +0.008] |
| c | 1 | 0.678 | 0.678 | 0.678 | 0.678 | 0.678 | 14820 | -0.004 | [-0.008, +0.000] | -0.120 | [-0.127, -0.113] | +0.236 | [+0.228, +0.245] |
| c | 3 | 0.754 | 0.679 | 0.750 | 0.754 | 0.502 | 14853 | -0.003 | [-0.005, -0.001] | -0.044 | [-0.048, -0.040] | +0.060 | [+0.057, +0.063] |
| c | 5 | 0.783 | 0.681 | 0.766 | 0.779 | 0.465 | 14886 | -0.001 | [-0.002, +0.000] | -0.019 | [-0.022, -0.016] | +0.023 | [+0.021, +0.024] |
| c | 10 | 0.813 | 0.681 | 0.767 | 0.797 | 0.446 | 14965 | -0.001 | [-0.002, +0.001] | -0.001 | [-0.003, +0.001] | +0.004 | [+0.004, +0.005] |
| d (flat) | | | 0.682 | 0.769 | 0.798 | 0.442 | 27242 | | | | | | |

### P1 image in [0,.2)+[.2,.5): 2821 queries over 1283 directories

| stage 1 | k | dir recall@k | hit@1 | hit@5 | hit@10 | sib@10 | vectors scored | hit@1 minus d | 95% CI | hit@10 minus d | 95% CI | sib@10 minus d | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| a | 1 | 0.294 | 0.294 | 0.294 | 0.294 | 0.294 | 2822 | -0.241 | [-0.272, -0.210] | -0.390 | [-0.421, -0.360] | +0.007 | [-0.018, +0.031] |
| a | 3 | 0.386 | 0.345 | 0.381 | 0.384 | 0.261 | 2848 | -0.189 | [-0.216, -0.163] | -0.299 | [-0.330, -0.269] | -0.025 | [-0.040, -0.012] |
| a | 5 | 0.422 | 0.363 | 0.412 | 0.417 | 0.254 | 2873 | -0.172 | [-0.199, -0.146] | -0.267 | [-0.296, -0.237] | -0.032 | [-0.046, -0.020] |
| a | 10 | 0.494 | 0.395 | 0.463 | 0.477 | 0.258 | 2934 | -0.139 | [-0.165, -0.115] | -0.206 | [-0.231, -0.179] | -0.028 | [-0.040, -0.017] |
| b | 1 | 0.504 | 0.504 | 0.504 | 0.504 | 0.504 | 7188 | -0.031 | [-0.048, -0.014] | -0.179 | [-0.200, -0.160] | +0.217 | [+0.196, +0.238] |
| b | 3 | 0.597 | 0.513 | 0.591 | 0.595 | 0.336 | 7216 | -0.022 | [-0.031, -0.012] | -0.088 | [-0.103, -0.075] | +0.050 | [+0.042, +0.057] |
| b | 5 | 0.635 | 0.518 | 0.611 | 0.629 | 0.307 | 7243 | -0.016 | [-0.025, -0.008] | -0.054 | [-0.066, -0.043] | +0.021 | [+0.016, +0.025] |
| b | 10 | 0.673 | 0.521 | 0.621 | 0.650 | 0.294 | 7312 | -0.013 | [-0.020, -0.006] | -0.033 | [-0.042, -0.023] | +0.007 | [+0.005, +0.010] |
| c | 1 | 0.523 | 0.523 | 0.523 | 0.523 | 0.523 | 14820 | -0.011 | [-0.020, -0.003] | -0.160 | [-0.177, -0.144] | +0.237 | [+0.217, +0.257] |
| c | 3 | 0.618 | 0.532 | 0.613 | 0.616 | 0.345 | 14850 | -0.003 | [-0.007, +0.001] | -0.067 | [-0.078, -0.055] | +0.059 | [+0.051, +0.066] |
| c | 5 | 0.660 | 0.535 | 0.639 | 0.657 | 0.312 | 14880 | +0.001 | [-0.002, +0.004] | -0.027 | [-0.034, -0.020] | +0.025 | [+0.021, +0.029] |
| c | 10 | 0.697 | 0.535 | 0.643 | 0.674 | 0.290 | 14953 | +0.000 | [-0.001, +0.002] | -0.009 | [-0.013, -0.005] | +0.004 | [+0.003, +0.005] |
| d (flat) | | | 0.535 | 0.647 | 0.683 | 0.286 | 27242 | | | | | | |

### P2 textlike in [.5,.8)+[.8,1]: 3166 queries over 1274 directories

| stage 1 | k | dir recall@k | hit@1 | hit@5 | hit@10 | sib@10 | vectors scored | hit@1 minus d | 95% CI | hit@10 minus d | 95% CI | sib@10 minus d | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| a | 1 | 0.287 | 0.287 | 0.287 | 0.287 | 0.287 | 2822 | -0.273 | [-0.302, -0.244] | -0.408 | [-0.436, -0.378] | +0.011 | [-0.011, +0.032] |
| a | 3 | 0.391 | 0.341 | 0.385 | 0.390 | 0.238 | 2850 | -0.219 | [-0.247, -0.192] | -0.305 | [-0.332, -0.277] | -0.038 | [-0.052, -0.024] |
| a | 5 | 0.436 | 0.371 | 0.423 | 0.432 | 0.233 | 2878 | -0.189 | [-0.215, -0.163] | -0.263 | [-0.288, -0.235] | -0.043 | [-0.056, -0.031] |
| a | 10 | 0.489 | 0.398 | 0.462 | 0.478 | 0.234 | 2948 | -0.162 | [-0.187, -0.138] | -0.217 | [-0.243, -0.189] | -0.042 | [-0.054, -0.031] |
| b | 1 | 0.527 | 0.527 | 0.527 | 0.527 | 0.527 | 7187 | -0.033 | [-0.046, -0.021] | -0.169 | [-0.186, -0.152] | +0.251 | [+0.232, +0.270] |
| b | 3 | 0.618 | 0.547 | 0.614 | 0.618 | 0.323 | 7216 | -0.013 | [-0.021, -0.004] | -0.078 | [-0.089, -0.066] | +0.047 | [+0.040, +0.054] |
| b | 5 | 0.649 | 0.551 | 0.633 | 0.646 | 0.294 | 7246 | -0.009 | [-0.016, -0.002] | -0.050 | [-0.060, -0.040] | +0.018 | [+0.013, +0.022] |
| b | 10 | 0.687 | 0.556 | 0.647 | 0.671 | 0.281 | 7320 | -0.004 | [-0.011, +0.002] | -0.025 | [-0.034, -0.017] | +0.005 | [+0.003, +0.008] |
| c | 1 | 0.558 | 0.558 | 0.558 | 0.558 | 0.558 | 14818 | -0.002 | [-0.009, +0.005] | -0.138 | [-0.154, -0.123] | +0.282 | [+0.262, +0.303] |
| c | 3 | 0.640 | 0.562 | 0.637 | 0.640 | 0.331 | 14849 | +0.002 | [-0.004, +0.007] | -0.056 | [-0.065, -0.047] | +0.055 | [+0.048, +0.063] |
| c | 5 | 0.669 | 0.563 | 0.657 | 0.668 | 0.293 | 14880 | +0.003 | [-0.002, +0.008] | -0.028 | [-0.035, -0.022] | +0.017 | [+0.013, +0.021] |
| c | 10 | 0.698 | 0.562 | 0.662 | 0.689 | 0.278 | 14956 | +0.002 | [-0.003, +0.007] | -0.007 | [-0.011, -0.002] | +0.002 | [+0.001, +0.003] |
| d (flat) | | | 0.560 | 0.662 | 0.696 | 0.276 | 27242 | | | | | | |

### image in [.5,.8)+[.8,1]: 6682 queries over 1218 directories

| stage 1 | k | dir recall@k | hit@1 | hit@5 | hit@10 | sib@10 | vectors scored | hit@1 minus d | 95% CI | hit@10 minus d | 95% CI | sib@10 minus d | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| a | 1 | 0.581 | 0.581 | 0.581 | 0.581 | 0.581 | 2822 | -0.077 | [-0.096, -0.058] | -0.179 | [-0.201, -0.158] | +0.146 | [+0.128, +0.164] |
| a | 3 | 0.674 | 0.609 | 0.665 | 0.672 | 0.476 | 2848 | -0.049 | [-0.064, -0.035] | -0.089 | [-0.105, -0.073] | +0.041 | [+0.033, +0.050] |
| a | 5 | 0.708 | 0.621 | 0.685 | 0.701 | 0.458 | 2873 | -0.038 | [-0.050, -0.026] | -0.060 | [-0.075, -0.045] | +0.023 | [+0.016, +0.029] |
| a | 10 | 0.757 | 0.632 | 0.698 | 0.730 | 0.446 | 2936 | -0.026 | [-0.037, -0.017] | -0.031 | [-0.043, -0.019] | +0.011 | [+0.005, +0.015] |
| b | 1 | 0.607 | 0.607 | 0.607 | 0.607 | 0.607 | 7187 | -0.052 | [-0.070, -0.033] | -0.154 | [-0.174, -0.135] | +0.172 | [+0.155, +0.190] |
| b | 3 | 0.686 | 0.614 | 0.679 | 0.684 | 0.482 | 7214 | -0.045 | [-0.058, -0.032] | -0.076 | [-0.093, -0.060] | +0.047 | [+0.039, +0.057] |
| b | 5 | 0.721 | 0.623 | 0.698 | 0.716 | 0.457 | 7242 | -0.035 | [-0.046, -0.025] | -0.044 | [-0.059, -0.030] | +0.022 | [+0.016, +0.028] |
| b | 10 | 0.768 | 0.634 | 0.701 | 0.737 | 0.440 | 7310 | -0.025 | [-0.033, -0.017] | -0.023 | [-0.034, -0.013] | +0.005 | [+0.001, +0.009] |
| c | 1 | 0.657 | 0.657 | 0.657 | 0.657 | 0.657 | 14818 | -0.001 | [-0.009, +0.006] | -0.104 | [-0.115, -0.093] | +0.222 | [+0.207, +0.237] |
| c | 3 | 0.724 | 0.654 | 0.720 | 0.723 | 0.496 | 14850 | -0.005 | [-0.008, -0.001] | -0.038 | [-0.045, -0.031] | +0.061 | [+0.055, +0.066] |
| c | 5 | 0.749 | 0.656 | 0.732 | 0.746 | 0.458 | 14880 | -0.002 | [-0.005, +0.000] | -0.015 | [-0.021, -0.009] | +0.023 | [+0.020, +0.026] |
| c | 10 | 0.783 | 0.657 | 0.729 | 0.764 | 0.439 | 14952 | -0.002 | [-0.004, +0.000] | +0.003 | [-0.001, +0.008] | +0.004 | [+0.003, +0.005] |
| d (flat) | | | 0.658 | 0.730 | 0.761 | 0.435 | 27242 | | | | | | |

### textlike in [0,.2)+[.2,.5): 10223 queries over 1413 directories

| stage 1 | k | dir recall@k | hit@1 | hit@5 | hit@10 | sib@10 | vectors scored | hit@1 minus d | 95% CI | hit@10 minus d | 95% CI | sib@10 minus d | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| a | 1 | 0.693 | 0.693 | 0.693 | 0.693 | 0.693 | 2826 | -0.084 | [-0.101, -0.068] | -0.194 | [-0.212, -0.175] | +0.151 | [+0.134, +0.167] |
| a | 3 | 0.784 | 0.723 | 0.778 | 0.782 | 0.585 | 2859 | -0.054 | [-0.065, -0.043] | -0.105 | [-0.120, -0.091] | +0.043 | [+0.036, +0.050] |
| a | 5 | 0.823 | 0.741 | 0.806 | 0.817 | 0.569 | 2890 | -0.036 | [-0.044, -0.028] | -0.070 | [-0.081, -0.059] | +0.027 | [+0.022, +0.031] |
| a | 10 | 0.860 | 0.752 | 0.819 | 0.841 | 0.556 | 2967 | -0.025 | [-0.031, -0.019] | -0.046 | [-0.055, -0.038] | +0.014 | [+0.010, +0.017] |
| b | 1 | 0.729 | 0.729 | 0.729 | 0.729 | 0.729 | 7191 | -0.048 | [-0.063, -0.035] | -0.158 | [-0.175, -0.142] | +0.187 | [+0.169, +0.202] |
| b | 3 | 0.814 | 0.748 | 0.810 | 0.813 | 0.593 | 7225 | -0.029 | [-0.038, -0.021] | -0.073 | [-0.086, -0.063] | +0.051 | [+0.045, +0.057] |
| b | 5 | 0.846 | 0.757 | 0.830 | 0.841 | 0.565 | 7259 | -0.020 | [-0.027, -0.014] | -0.045 | [-0.054, -0.037] | +0.022 | [+0.018, +0.026] |
| b | 10 | 0.881 | 0.766 | 0.840 | 0.865 | 0.550 | 7341 | -0.012 | [-0.016, -0.007] | -0.022 | [-0.028, -0.016] | +0.008 | [+0.006, +0.010] |
| c | 1 | 0.774 | 0.774 | 0.774 | 0.774 | 0.774 | 14822 | -0.003 | [-0.009, +0.003] | -0.113 | [-0.123, -0.102] | +0.232 | [+0.219, +0.246] |
| c | 3 | 0.849 | 0.774 | 0.844 | 0.849 | 0.602 | 14858 | -0.003 | [-0.006, -0.001] | -0.038 | [-0.044, -0.032] | +0.060 | [+0.056, +0.065] |
| c | 5 | 0.874 | 0.775 | 0.858 | 0.871 | 0.565 | 14894 | -0.002 | [-0.004, -0.000] | -0.016 | [-0.020, -0.012] | +0.023 | [+0.021, +0.025] |
| c | 10 | 0.901 | 0.776 | 0.860 | 0.886 | 0.547 | 14979 | -0.001 | [-0.002, +0.000] | -0.000 | [-0.002, +0.002] | +0.005 | [+0.004, +0.006] |
| d (flat) | | | 0.777 | 0.862 | 0.887 | 0.542 | 27242 | | | | | | |

### Query time

Microseconds per query, brute force numpy 2.5.2, one BLAS thread, best of 5 passes over 2000 queries, top 10 files returned. 2808 directories, 27243 file vectors. Directory stage alone in the first column (for d: the flat walk with a max per directory).

| index | directory stage only | two-stage k=1 | two-stage k=3 | two-stage k=5 | two-stage k=10 | flat walk |
|---|---:|---:|---:|---:|---:|---:|
| a | 333 | 358 | 377 | 399 | 456 | |
| b | 1348 | 1375 | 1400 | 1398 | 1432 | |
| c | 2766 | 2798 | 2814 | 2853 | 2893 | |
| d | 5156 |  |  |  |  | 5191 |

## Step 6: HNSW baselines

Output of `python scripts/hnsw.py` with the same arguments and `--timing-queries 2000`,
`DIRVEC_THREADS=3` for the build and the batch searches (the cgroup allows 3.4 vCPUs while
`os.cpu_count()` reports 128). Recall@10 is against the exact flat top 10; hit@n and intervals as in
step 5.

hnswlib 0.8.0, numpy 2.5.2. M = 16, ef_construction = 200, inner product, seed 100. 23119 queries with at least one embedded sibling, 2808 directories, 27243 file vectors. Query time: one thread, best of 3 passes over 2000 queries.

### Flat HNSW over the file vectors

Index: 27243 vectors, 227.2 MB on disk (raw vectors 223.2 MB), built in 5 s on 3 threads.

| ef_search | recall@10 vs exact | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | us per query |
|---:|---:|---:|---:|---:|---|---:|
| exact d | 1.000 | 0.682 | 0.798 | | | 5197 |
| 16 | 0.965 | 0.669 | 0.782 | -0.016 | [-0.018, -0.015] | 86 |
| 32 | 0.984 | 0.675 | 0.789 | -0.009 | [-0.011, -0.008] | 138 |
| 64 | 0.991 | 0.678 | 0.793 | -0.006 | [-0.007, -0.005] | 232 |
| 128 | 0.994 | 0.679 | 0.794 | -0.004 | [-0.005, -0.003] | 402 |
| 256 | 0.995 | 0.680 | 0.795 | -0.003 | [-0.004, -0.002] | 711 |

### Two-stage with HNSW over the representatives as stage 1, k = 10 directories

Stage 1 retrieves 100 representatives (ef_search at least 100); stage 2 is exact over the files of the 10 directories. Directory overlap: share of the 10 directories that exact stage 1 also returns. Two-stage time includes stage 2.

| stage 1 | representatives | index MB | build s | ef_search | dir overlap vs exact | dir recall@10 | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | us per query |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| a | 2808 | 23.4 | 0 | 100 | 0.999 | 0.734 | 0.624 | 0.713 | -0.085 | [-0.093, -0.077] | 196 |
| a | 2808 | 23.4 | 0 | 128 | 0.999 | 0.734 | 0.624 | 0.713 | -0.085 | [-0.093, -0.077] | 237 |
| a | 2808 | 23.4 | 0 | 256 | 1.000 | 0.734 | 0.624 | 0.713 | -0.085 | [-0.093, -0.078] | 313 |
| b | 7172 | 59.8 | 1 | 100 | 0.999 | 0.795 | 0.668 | 0.774 | -0.024 | [-0.029, -0.019] | 290 |
| b | 7172 | 59.8 | 1 | 128 | 0.999 | 0.795 | 0.667 | 0.774 | -0.024 | [-0.029, -0.019] | 440 |
| b | 7172 | 59.8 | 1 | 256 | 1.000 | 0.795 | 0.667 | 0.774 | -0.024 | [-0.029, -0.019] | 502 |
| c | 14803 | 123.5 | 2 | 100 | 0.998 | 0.813 | 0.682 | 0.797 | -0.001 | [-0.003, +0.000] | 359 |
| c | 14803 | 123.5 | 2 | 128 | 0.999 | 0.813 | 0.681 | 0.797 | -0.001 | [-0.003, +0.001] | 406 |
| c | 14803 | 123.5 | 2 | 256 | 1.000 | 0.813 | 0.681 | 0.797 | -0.001 | [-0.003, +0.001] | 643 |

## Session 3 cells on the large set

Output of `python scripts/eval.py` with the same arguments and `--criterion s3`. Directory recall,
leave-one-out, as in sessions 2 and 3.

Model: jina-embeddings-v4. Queries: 23130 over 2767 directories; 2808 directories ranked (random recall@k = k/2808). Queries dropped for lack of a vector: 277 {'table': 7, 'other': 256, 'image': 12, 'text': 2}.

Mean representative vectors per directory: a 1.00, b 2.55, c 5.27, d 9.70.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 23130 | 2767 | a | 0.554 | 0.648 | 0.686 | 0.733 | [0.674, 0.699] |
| all | 23130 | 2767 | b | 0.637 | 0.722 | 0.755 | 0.795 | [0.744, 0.766] |
| all | 23130 | 2767 | c | 0.678 | 0.754 | 0.782 | 0.812 | [0.772, 0.792] |
| all | 23130 | 2767 | d | 0.682 | 0.756 | 0.783 | 0.812 | [0.772, 0.794] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 5899 | 455 | a | 0.691 | 0.779 | 0.822 | 0.859 | [0.806, 0.837] |
| [0,.2) | 5899 | 455 | b | 0.725 | 0.810 | 0.848 | 0.880 | [0.831, 0.863] |
| [0,.2) | 5899 | 455 | c | 0.786 | 0.853 | 0.880 | 0.904 | [0.867, 0.891] |
| [0,.2) | 5899 | 455 | d | 0.790 | 0.858 | 0.883 | 0.904 | [0.870, 0.894] |
| [.2,.5) | 7349 | 992 | a | 0.536 | 0.631 | 0.665 | 0.716 | [0.645, 0.687] |
| [.2,.5) | 7349 | 992 | b | 0.642 | 0.730 | 0.759 | 0.798 | [0.742, 0.775] |
| [.2,.5) | 7349 | 992 | c | 0.663 | 0.752 | 0.783 | 0.815 | [0.767, 0.799] |
| [.2,.5) | 7349 | 992 | d | 0.670 | 0.755 | 0.785 | 0.816 | [0.769, 0.801] |
| [.5,.8) | 6838 | 1014 | a | 0.411 | 0.510 | 0.551 | 0.608 | [0.527, 0.576] |
| [.5,.8) | 6838 | 1014 | b | 0.551 | 0.634 | 0.664 | 0.711 | [0.642, 0.686] |
| [.5,.8) | 6838 | 1014 | c | 0.584 | 0.655 | 0.681 | 0.715 | [0.659, 0.702] |
| [.5,.8) | 6838 | 1014 | d | 0.587 | 0.656 | 0.682 | 0.714 | [0.660, 0.704] |
| [.8,1] | 3044 | 306 | a | 0.656 | 0.746 | 0.776 | 0.813 | [0.748, 0.800] |
| [.8,1] | 3044 | 306 | b | 0.647 | 0.731 | 0.773 | 0.813 | [0.741, 0.801] |
| [.8,1] | 3044 | 306 | c | 0.714 | 0.789 | 0.818 | 0.848 | [0.790, 0.842] |
| [.8,1] | 3044 | 306 | d | 0.716 | 0.784 | 0.811 | 0.840 | [0.781, 0.837] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 9503 | 2501 | a | 0.496 | 0.588 | 0.623 | 0.679 | [0.603, 0.644] |
| image | 9503 | 2501 | b | 0.576 | 0.659 | 0.695 | 0.740 | [0.676, 0.713] |
| image | 9503 | 2501 | c | 0.617 | 0.692 | 0.723 | 0.757 | [0.706, 0.739] |
| image | 9503 | 2501 | d | 0.622 | 0.692 | 0.720 | 0.753 | [0.702, 0.737] |
| pdf_text | 2415 | 963 | a | 0.703 | 0.795 | 0.828 | 0.851 | [0.804, 0.849] |
| pdf_text | 2415 | 963 | b | 0.752 | 0.825 | 0.853 | 0.876 | [0.833, 0.871] |
| pdf_text | 2415 | 963 | c | 0.749 | 0.816 | 0.839 | 0.861 | [0.817, 0.859] |
| pdf_text | 2415 | 963 | d | 0.735 | 0.805 | 0.828 | 0.857 | [0.805, 0.849] |
| text | 5169 | 1491 | a | 0.534 | 0.630 | 0.672 | 0.723 | [0.645, 0.697] |
| text | 5169 | 1491 | b | 0.627 | 0.721 | 0.751 | 0.796 | [0.729, 0.771] |
| text | 5169 | 1491 | c | 0.691 | 0.779 | 0.802 | 0.832 | [0.784, 0.818] |
| text | 5169 | 1491 | d | 0.701 | 0.786 | 0.810 | 0.834 | [0.792, 0.826] |
| table | 4987 | 1253 | a | 0.596 | 0.695 | 0.739 | 0.777 | [0.716, 0.760] |
| table | 4987 | 1253 | b | 0.694 | 0.781 | 0.818 | 0.852 | [0.801, 0.833] |
| table | 4987 | 1253 | c | 0.739 | 0.810 | 0.842 | 0.869 | [0.825, 0.856] |
| table | 4987 | 1253 | d | 0.748 | 0.818 | 0.848 | 0.874 | [0.832, 0.862] |
| other | 829 | 412 | a | 0.680 | 0.748 | 0.771 | 0.809 | [0.727, 0.810] |
| other | 829 | 412 | b | 0.729 | 0.802 | 0.819 | 0.848 | [0.781, 0.852] |
| other | 829 | 412 | c | 0.738 | 0.807 | 0.825 | 0.844 | [0.788, 0.860] |
| other | 829 | 412 | d | 0.729 | 0.811 | 0.829 | 0.848 | [0.793, 0.863] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 526 | 346 | a | 0.200 | 0.274 | 0.298 | 0.365 | [0.246, 0.348] |
| image [0,.2) | 526 | 346 | b | 0.392 | 0.470 | 0.529 | 0.572 | [0.473, 0.582] |
| image [0,.2) | 526 | 346 | c | 0.405 | 0.487 | 0.551 | 0.595 | [0.503, 0.602] |
| image [0,.2) | 526 | 346 | d | 0.435 | 0.511 | 0.567 | 0.608 | [0.514, 0.621] |
| image [.2,.5) | 2295 | 937 | a | 0.315 | 0.411 | 0.450 | 0.523 | [0.412, 0.485] |
| image [.2,.5) | 2295 | 937 | b | 0.529 | 0.627 | 0.660 | 0.696 | [0.632, 0.688] |
| image [.2,.5) | 2295 | 937 | c | 0.550 | 0.647 | 0.685 | 0.720 | [0.656, 0.714] |
| image [.2,.5) | 2295 | 937 | d | 0.557 | 0.654 | 0.691 | 0.724 | [0.662, 0.718] |
| image [.5,.8) | 4086 | 933 | a | 0.478 | 0.570 | 0.606 | 0.664 | [0.576, 0.637] |
| image [.5,.8) | 4086 | 933 | b | 0.549 | 0.627 | 0.656 | 0.709 | [0.629, 0.684] |
| image [.5,.8) | 4086 | 933 | c | 0.585 | 0.649 | 0.673 | 0.710 | [0.643, 0.703] |
| image [.5,.8) | 4086 | 933 | d | 0.586 | 0.645 | 0.667 | 0.703 | [0.636, 0.697] |
| image [.8,1] | 2596 | 285 | a | 0.745 | 0.838 | 0.869 | 0.904 | [0.844, 0.893] |
| image [.8,1] | 2596 | 285 | b | 0.698 | 0.779 | 0.822 | 0.861 | [0.788, 0.853] |
| image [.8,1] | 2596 | 285 | c | 0.771 | 0.842 | 0.869 | 0.898 | [0.842, 0.893] |
| image [.8,1] | 2596 | 285 | d | 0.772 | 0.835 | 0.859 | 0.886 | [0.830, 0.885] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 5295 | 448 | a | 0.743 | 0.833 | 0.879 | 0.911 | [0.865, 0.893] |
| textlike [0,.2) | 5295 | 448 | b | 0.761 | 0.846 | 0.882 | 0.913 | [0.866, 0.897] |
| textlike [0,.2) | 5295 | 448 | c | 0.826 | 0.893 | 0.915 | 0.937 | [0.904, 0.926] |
| textlike [0,.2) | 5295 | 448 | d | 0.828 | 0.895 | 0.917 | 0.936 | [0.906, 0.928] |
| textlike [.2,.5) | 4939 | 976 | a | 0.637 | 0.731 | 0.763 | 0.803 | [0.741, 0.783] |
| textlike [.2,.5) | 4939 | 976 | b | 0.693 | 0.778 | 0.804 | 0.844 | [0.786, 0.821] |
| textlike [.2,.5) | 4939 | 976 | c | 0.716 | 0.801 | 0.828 | 0.859 | [0.811, 0.844] |
| textlike [.2,.5) | 4939 | 976 | d | 0.722 | 0.802 | 0.828 | 0.859 | [0.811, 0.843] |
| textlike [.5,.8) | 2724 | 986 | a | 0.311 | 0.421 | 0.468 | 0.523 | [0.434, 0.503] |
| textlike [.5,.8) | 2724 | 986 | b | 0.555 | 0.645 | 0.675 | 0.712 | [0.646, 0.700] |
| textlike [.5,.8) | 2724 | 986 | c | 0.586 | 0.666 | 0.693 | 0.721 | [0.663, 0.718] |
| textlike [.5,.8) | 2724 | 986 | d | 0.590 | 0.675 | 0.705 | 0.731 | [0.677, 0.730] |
| textlike [.8,1] | 442 | 288 | a | 0.143 | 0.210 | 0.238 | 0.278 | [0.189, 0.288] |
| textlike [.8,1] | 442 | 288 | b | 0.355 | 0.455 | 0.486 | 0.534 | [0.426, 0.543] |
| textlike [.8,1] | 442 | 288 | c | 0.385 | 0.477 | 0.523 | 0.554 | [0.461, 0.580] |
| textlike [.8,1] | 442 | 288 | d | 0.394 | 0.491 | 0.532 | 0.570 | [0.468, 0.590] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | b | c | d | c-a | c-a 95% CI | b-a | b-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 0.422 | 0.635 | 0.660 | 0.667 | +0.238 | [+0.207, +0.268] | +0.213 | [+0.183, +0.241] |
| P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 0.436 | 0.649 | 0.669 | 0.681 | +0.233 | [+0.207, +0.262] | +0.213 | [+0.187, +0.241] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | b | c | d | c-a | c-a 95% CI | b-a | b-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| P1 part: image [0,.2) | 526 | 346 | 0.298 | 0.529 | 0.551 | 0.567 | +0.253 | [+0.201, +0.304] | +0.230 | [+0.177, +0.284] |
| P1 part: image [.2,.5) | 2295 | 937 | 0.450 | 0.660 | 0.685 | 0.691 | +0.235 | [+0.202, +0.269] | +0.210 | [+0.179, +0.243] |
| P2 part: textlike [.5,.8) | 2724 | 986 | 0.468 | 0.675 | 0.693 | 0.705 | +0.225 | [+0.194, +0.253] | +0.207 | [+0.176, +0.236] |
| P2 part: textlike [.8,1] | 442 | 288 | 0.238 | 0.486 | 0.523 | 0.532 | +0.285 | [+0.221, +0.344] | +0.249 | [+0.186, +0.302] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | b | c | d | c-a | c-a 95% CI | b-a | b-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| image in [.5,.8)+[.8,1] | 6682 | 1218 | 0.708 | 0.721 | 0.749 | 0.742 | +0.041 | [+0.027, +0.057] | +0.012 | [+0.001, +0.025] |
| textlike in [0,.2)+[.2,.5) | 10234 | 1424 | 0.823 | 0.845 | 0.873 | 0.874 | +0.050 | [+0.040, +0.062] | +0.022 | [+0.013, +0.031] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | b | c | d | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 0.422 | 0.635 | 0.660 | 0.667 | +0.007 | [+0.001, +0.014] |
| P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 0.436 | 0.649 | 0.669 | 0.681 | +0.012 | [+0.007, +0.016] |
| P1 part: image [0,.2) | 526 | 346 | 0.298 | 0.529 | 0.551 | 0.567 | +0.015 | [-0.002, +0.031] |
| P1 part: image [.2,.5) | 2295 | 937 | 0.450 | 0.660 | 0.685 | 0.691 | +0.006 | [-0.001, +0.013] |
| P2 part: textlike [.5,.8) | 2724 | 986 | 0.468 | 0.675 | 0.693 | 0.705 | +0.012 | [+0.007, +0.017] |
| P2 part: textlike [.8,1] | 442 | 288 | 0.238 | 0.486 | 0.523 | 0.532 | +0.009 | [-0.007, +0.025] |
| image in [.5,.8)+[.8,1] | 6682 | 1218 | 0.708 | 0.721 | 0.749 | 0.742 | -0.008 | [-0.015, -0.001] |
| textlike in [0,.2)+[.2,.5) | 10234 | 1424 | 0.823 | 0.845 | 0.873 | 0.874 | +0.001 | [-0.002, +0.005] |
| all [0,.2) | 5899 | 455 | 0.822 | 0.848 | 0.880 | 0.883 | +0.003 | [-0.001, +0.008] |
| all [.2,.5) | 7349 | 992 | 0.665 | 0.759 | 0.783 | 0.785 | +0.002 | [-0.002, +0.006] |
| all [.5,.8) | 6838 | 1014 | 0.551 | 0.664 | 0.681 | 0.682 | +0.001 | [-0.005, +0.007] |
| all [.8,1] | 3044 | 306 | 0.776 | 0.773 | 0.818 | 0.811 | -0.007 | [-0.018, +0.003] |
| image [0,.2) | 526 | 346 | 0.298 | 0.529 | 0.551 | 0.567 | +0.015 | [+0.000, +0.031] |
| image [.2,.5) | 2295 | 937 | 0.450 | 0.660 | 0.685 | 0.691 | +0.006 | [-0.001, +0.013] |
| image [.5,.8) | 4086 | 933 | 0.606 | 0.656 | 0.673 | 0.667 | -0.006 | [-0.016, +0.002] |
| image [.8,1] | 2596 | 285 | 0.869 | 0.822 | 0.869 | 0.859 | -0.010 | [-0.023, +0.001] |
| textlike [0,.2) | 5295 | 448 | 0.879 | 0.882 | 0.915 | 0.917 | +0.002 | [-0.003, +0.007] |
| textlike [.2,.5) | 4939 | 976 | 0.763 | 0.804 | 0.828 | 0.828 | +0.000 | [-0.005, +0.005] |
| textlike [.5,.8) | 2724 | 986 | 0.468 | 0.675 | 0.693 | 0.705 | +0.012 | [+0.008, +0.018] |
| textlike [.8,1] | 442 | 288 | 0.238 | 0.486 | 0.523 | 0.532 | +0.009 | [-0.007, +0.024] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.
