# dirvec session 7: the container layer against flat HNSW at matched time

Question: at the same query time, does two-stage retrieval with HNSW over the c representatives
as stage 1 beat flat HNSW over the file vectors on hit@10?
Same set, cache, encoder, input rules and ground truth as sessions 5 and 6 (`results/session5.md`):
2,808 directories, 27,243 embedded files, 23,119 queries with at least one embedded sibling.
No download, no GPU. CPU only (MIG 1g.24gb pod, 3.4 vCPUs by cgroup; numpy 2.5.2, hnswlib 0.8.0),
`DIRVEC_THREADS`, `OMP_NUM_THREADS` and `OPENBLAS_NUM_THREADS` set to 3. Index builds on one
thread (`--build-threads 1`), query times on one thread, best of 3 passes over the same 2,000
queries as sessions 5 and 6.

Changes to `scripts/hnsw.py` (commit e6fec4f): `--build-threads`; flat ef_search grid
{32, 48, 64, 96, 128, 192, 256} (was {16, 32, 64, 128, 256}); stage 1 ef_search {100, 128, 256},
the values sessions 5 and 6 used; per-query hit@1 and hit@10 of every setting in
`data/emb/jina-embeddings-v4_s5/hnsw.jsonl` (no times in it), times and index sizes in
`hnsw_times.json`; the checks and the H7 comparison below. M, ef_construction, seed, K_REPS and
stage 2 unchanged.

Two runs, one after the other, each alone on the CPU, about 9 minutes each (13:06 to 13:15 and
13:15 to 13:23 UTC). Run 1 is the reported run; this was fixed before run 2 finished. Run 2 is
the reproducibility check and its times are reported alongside.

## Hypothesis (copied verbatim from BRIEF.md, fixed before the first eval run)

H7: on the session 5 set, two-stage retrieval with HNSW over the c representatives as stage 1
(ef_search 100, 100 representatives, exact stage 2 over the top 10 directories) has higher hit@10
over all queries than flat HNSW over the file vectors at the matched setting: the smallest
ef_search in {32, 48, 64, 96, 128, 192, 256} whose measured query time in the same run is at least
the two-stage query time.
Kill: H7 is dead if the paired 95% bootstrap interval (1000 resamples over directories) of hit@10,
two-stage HNSW c minus matched flat HNSW, over all queries, does not lie entirely above zero.
Report it plainly either way.
Secondary, reported, no kill: the same for c4 and c2 as stage 1; the same comparison in the
session 3 primary cells P1 and P2; hit@1; storage of each against flat HNSW.

## Verdict

H7 is dead. Over all 23,119 queries, two-stage with HNSW over c (stage 1 ef_search 100, 345 us per
query in run 1) against flat HNSW at the matched setting (ef_search 128, 462 us, the smallest grid
value not faster than the two-stage): hit@10 0.797 against 0.796, difference +0.0006, 95% CI
[-0.0012, +0.0023]. The interval does not lie entirely above zero.
The verdict does not depend on which run's times pick the matched setting. In run 2 the two-stage
took 359 us, flat ef_search 128 took 329 us and ef_search 192 457 us, so the matched setting was
192: difference +0.0003, CI [-0.0015, +0.0020]. Against every flat setting from ef_search 48 up the
interval covers zero (table below); only against ef_search 32, at a third of the two-stage time,
does it lie above zero.

## Reproducibility and checks

- With `--build-threads 1` the two runs wrote byte-identical `hnsw.jsonl` files (sha256
  3b7ce0d8...fd529a91). Every recall, hit and interval in the two runs' tables is identical; only
  query times differ.
- Exact two-stage at k = 10 (leave-one-out, rebuilt from this script's own exact stage 1 directory
  lists and stage 2) against `twostage.jsonl`: directory hit, hit@1 and hit@10 equal on every
  query for a, b, c, c4 and c2.
- Exact d: this script's own exact top 10 agrees with `twostage.jsonl` d on hit@1 for 0.9992 and on
  hit@10 for 0.9998 of the queries. The difference is tie order only: `hnsw.py` takes the top 10
  with `argpartition`, `twostage.py` with a stable sort; with a stable sort on the same scores the
  hit@1 match is 23,119 of 23,119. The exact d hits used in every difference below are the ones in
  `twostage.jsonl`; this script's exact top 10 is only the reference for recall@10.

## H7 table (run 1)

Stage 1 at ef_search 100 against flat HNSW at the matched setting. Paired 95% interval, 1000
resamples of the cell's directories (seeds 301, 302, 303 for all queries, P1, P2). Storage: stage 1
index plus the raw file vectors for stage 2 (223.2 MB), against the flat index (227.2 MB, vectors
included).

| stage 1 | cell | queries | dirs | two-stage us | matched flat ef | flat us | two-stage hit@10 | flat hit@10 | hit@10 diff | 95% CI | two-stage hit@1 | flat hit@1 | hit@1 diff | 95% CI | storage ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|---:|
| c | all queries | 23119 | 2756 | 345 | 128 | 462 | 0.797 | 0.796 | +0.0006 | [-0.0012, +0.0023] | 0.682 | 0.681 | +0.0008 | [-0.0003, +0.0018] | 1.53 |
| c | P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 345 | 128 | 462 | 0.674 | 0.678 | -0.0039 | [-0.0082, +0.0004] | 0.535 | 0.532 | +0.0025 | [+0.0007, +0.0049] | 1.53 |
| c | P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 345 | 128 | 462 | 0.689 | 0.692 | -0.0028 | [-0.0071, +0.0016] | 0.563 | 0.559 | +0.0041 | [-0.0000, +0.0088] | 1.53 |
| c4 | all queries | 23119 | 2756 | 331 | 128 | 462 | 0.791 | 0.796 | -0.0048 | [-0.0072, -0.0024] | 0.678 | 0.681 | -0.0024 | [-0.0040, -0.0008] | 1.33 |
| c4 | P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 331 | 128 | 462 | 0.662 | 0.678 | -0.0160 | [-0.0241, -0.0084] | 0.528 | 0.532 | -0.0043 | [-0.0090, +0.0004] | 1.33 |
| c4 | P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 331 | 128 | 462 | 0.676 | 0.692 | -0.0158 | [-0.0227, -0.0085] | 0.557 | 0.559 | -0.0016 | [-0.0071, +0.0043] | 1.33 |
| c2 | all queries | 23119 | 2756 | 334 | 128 | 462 | 0.792 | 0.796 | -0.0041 | [-0.0065, -0.0016] | 0.679 | 0.681 | -0.0019 | [-0.0034, -0.0003] | 1.41 |
| c2 | P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 334 | 128 | 462 | 0.668 | 0.678 | -0.0099 | [-0.0168, -0.0035] | 0.532 | 0.532 | -0.0007 | [-0.0046, +0.0028] | 1.41 |
| c2 | P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 334 | 128 | 462 | 0.684 | 0.692 | -0.0076 | [-0.0129, -0.0022] | 0.562 | 0.559 | +0.0028 | [-0.0015, +0.0076] | 1.41 |

Run 2 (same hits, different times): c 359 us, matched flat ef_search 192 (457 us), all queries
+0.0003 [-0.0015, +0.0020], P1 -0.0046 [-0.0089, -0.0004], P2 -0.0038 [-0.0081, +0.0006]; c4 324
us, matched 128 (329 us), numbers as run 1; c2 330 us, matched 192 (457 us), all queries -0.0044
[-0.0068, -0.0018].

## c, c4 and c2 at stage 1 ef_search 100 against every flat setting (all queries, hit@10)

Difference two-stage minus flat, paired 95% interval (seed 301). Per-query hits are the same in
both runs; the flat times are run 1 / run 2.

| flat ef_search | flat us (run 1 / run 2) | c | c4 | c2 |
|---:|---:|---|---|---|
| 32 | 123 / 112 | +0.0023 [+0.0004, +0.0041] | -0.0031 [-0.0056, -0.0006] | -0.0024 [-0.0049, +0.0003] |
| 48 | 160 / 152 | +0.0017 [-0.0001, +0.0035] | -0.0037 [-0.0061, -0.0012] | -0.0030 [-0.0055, -0.0004] |
| 64 | 200 / 188 | +0.0010 [-0.0007, +0.0027] | -0.0044 [-0.0068, -0.0019] | -0.0037 [-0.0061, -0.0011] |
| 96 | 273 / 260 | +0.0010 [-0.0008, +0.0027] | -0.0045 [-0.0069, -0.0021] | -0.0038 [-0.0062, -0.0012] |
| 128 | 462 / 329 | +0.0006 [-0.0012, +0.0023] | -0.0048 [-0.0072, -0.0024] | -0.0041 [-0.0065, -0.0016] |
| 192 | 649 / 457 | +0.0003 [-0.0015, +0.0020] | -0.0051 [-0.0076, -0.0027] | -0.0044 [-0.0068, -0.0018] |
| 256 | 818 / 576 | +0.0002 [-0.0015, +0.0018] | -0.0052 [-0.0077, -0.0029] | -0.0045 [-0.0070, -0.0020] |

Two-stage times (run 1 / run 2): c 345 / 359, c4 331 / 324, c2 334 / 330 us.

## Secondary

- c4 and c2 as stage 1 lose to flat HNSW at the matched setting over all queries: c4 -0.0048
  [-0.0072, -0.0024], c2 -0.0041 [-0.0065, -0.0016] hit@10 (run 1). Both lose at every flat
  setting from ef_search 48 up; c4 also at 32.
- P1 and P2: c is below flat HNSW on hit@10 in both cells (P1 -0.0039 [-0.0082, +0.0004], P2
  -0.0028 [-0.0071, +0.0016]; run 2 P1 -0.0046 [-0.0089, -0.0004]) and above it on hit@1 (P1
  +0.0025 [+0.0007, +0.0049], P2 +0.0041 [-0.0000, +0.0088]). c4 and c2 lose 0.008 to 0.016 hit@10
  in both cells, all intervals below zero.
- hit@1, all queries: c +0.0008 [-0.0003, +0.0018], c4 -0.0024 [-0.0040, -0.0008], c2 -0.0019
  [-0.0034, -0.0003].
- Storage against the flat HNSW index: c 1.53, c4 1.33, c2 1.41 times.
- Flat HNSW with a one-thread build is at -0.004 to -0.001 hit@10 of exact d across the grid
  (recall@10 0.989 to 0.996). At ef_search 64 it is at -0.002; the three-thread builds of sessions 5
  and 6 were at -0.006. Whether one-thread builds are better in general or this graph is a lucky
  draw was not tested (one build, seed 100). Against this graph, the 0.003 hit@10 gap that H7 was
  written to test shrinks to +0.0006 at the matched setting.

## Run 1 output (`hnsw.py --build-threads 1`)

hnswlib 0.8.0, numpy 2.5.2. M = 16, ef_construction = 200, inner product, seed 100. 23119 queries with at least one embedded sibling, 2808 directories, 27243 file vectors. Query time: one thread, best of 3 passes over 2000 queries.
Check: exact d from this script against twostage.jsonl, hit@1 equal on 0.9992 and hit@10 on 0.9998 of the queries.

### Flat HNSW over the file vectors

Index: 27243 vectors, 227.2 MB on disk (raw vectors 223.2 MB), built in 10 s on 1 threads.

| ef_search | recall@10 vs exact | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | us per query |
|---:|---:|---:|---:|---:|---|---:|
| exact d | 1.000 | 0.682 | 0.798 | | | 5239 |
| 32 | 0.989 | 0.680 | 0.795 | -0.004 | [-0.004, -0.003] | 123 |
| 48 | 0.992 | 0.680 | 0.795 | -0.003 | [-0.004, -0.002] | 160 |
| 64 | 0.994 | 0.681 | 0.796 | -0.002 | [-0.003, -0.002] | 200 |
| 96 | 0.995 | 0.681 | 0.796 | -0.002 | [-0.003, -0.002] | 273 |
| 128 | 0.996 | 0.681 | 0.796 | -0.002 | [-0.003, -0.001] | 462 |
| 192 | 0.996 | 0.681 | 0.797 | -0.002 | [-0.002, -0.001] | 649 |
| 256 | 0.996 | 0.681 | 0.797 | -0.001 | [-0.002, -0.001] | 818 |

### Two-stage with HNSW over the representatives as stage 1, k = 10 directories

Stage 1 retrieves 100 representatives (ef_search at least 100); stage 2 is exact over the files of the 10 directories. Directory overlap: share of the 10 directories that exact stage 1 also returns. Two-stage time includes stage 2.

| stage 1 | representatives | index MB | build s | ef_search | dir overlap vs exact | dir recall@10 | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | us per query |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| a | 2808 | 23.4 | 0 | 100 | 0.999 | 0.734 | 0.624 | 0.713 | -0.085 | [-0.093, -0.077] | 206 |
| a | 2808 | 23.4 | 0 | 128 | 1.000 | 0.734 | 0.624 | 0.713 | -0.085 | [-0.093, -0.077] | 224 |
| a | 2808 | 23.4 | 0 | 256 | 1.000 | 0.734 | 0.624 | 0.713 | -0.085 | [-0.093, -0.078] | 307 |
| b | 7172 | 59.8 | 2 | 100 | 0.999 | 0.795 | 0.667 | 0.774 | -0.024 | [-0.029, -0.019] | 285 |
| b | 7172 | 59.8 | 2 | 128 | 1.000 | 0.795 | 0.667 | 0.774 | -0.024 | [-0.029, -0.019] | 400 |
| b | 7172 | 59.8 | 2 | 256 | 1.000 | 0.795 | 0.667 | 0.774 | -0.024 | [-0.029, -0.019] | 501 |
| c | 14803 | 123.5 | 5 | 100 | 0.999 | 0.813 | 0.682 | 0.797 | -0.001 | [-0.003, +0.000] | 345 |
| c | 14803 | 123.5 | 5 | 128 | 0.999 | 0.813 | 0.681 | 0.797 | -0.001 | [-0.003, +0.001] | 398 |
| c | 14803 | 123.5 | 5 | 256 | 1.000 | 0.813 | 0.681 | 0.797 | -0.001 | [-0.003, +0.001] | 635 |
| c4 | 9512 | 79.3 | 3 | 100 | 0.999 | 0.813 | 0.678 | 0.791 | -0.007 | [-0.009, -0.004] | 331 |
| c4 | 9512 | 79.3 | 3 | 128 | 1.000 | 0.813 | 0.678 | 0.791 | -0.007 | [-0.009, -0.004] | 385 |
| c4 | 9512 | 79.3 | 3 | 256 | 1.000 | 0.813 | 0.678 | 0.791 | -0.007 | [-0.009, -0.004] | 823 |
| c2 | 11634 | 97.0 | 4 | 100 | 0.999 | 0.808 | 0.679 | 0.792 | -0.006 | [-0.008, -0.003] | 334 |
| c2 | 11634 | 97.0 | 4 | 128 | 0.999 | 0.808 | 0.679 | 0.792 | -0.006 | [-0.008, -0.003] | 391 |
| c2 | 11634 | 97.0 | 4 | 256 | 1.000 | 0.808 | 0.679 | 0.792 | -0.006 | [-0.008, -0.003] | 617 |

Check: exact two-stage (k = 10, leave-one-out) from this script against twostage.jsonl: a: directory hit equal on 1.0000, hit@1 on 1.0000, hit@10 on 1.0000; b: directory hit equal on 1.0000, hit@1 on 1.0000, hit@10 on 1.0000; c: directory hit equal on 1.0000, hit@1 on 1.0000, hit@10 on 1.0000; c4: directory hit equal on 1.0000, hit@1 on 1.0000, hit@10 on 1.0000; c2: directory hit equal on 1.0000, hit@1 on 1.0000, hit@10 on 1.0000.

### H7: two-stage HNSW (stage 1 ef_search 100) against flat HNSW at matched time

Matched flat setting: the smallest ef_search in {32, 48, 64, 96, 128, 192, 256} whose query time in this run is at least the two-stage query time. Paired 95% interval, 1000 resamples of the cell's directories. Storage: stage 1 index plus the raw file vectors for stage 2, against the flat index (227.2 MB, vectors included).

| stage 1 | cell | queries | dirs | two-stage us | matched flat ef | flat us | two-stage hit@10 | flat hit@10 | hit@10 diff | 95% CI | two-stage hit@1 | flat hit@1 | hit@1 diff | 95% CI | storage ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|---:|
| c | all queries | 23119 | 2756 | 345 | 128 | 462 | 0.797 | 0.796 | +0.0006 | [-0.0012, +0.0023] | 0.682 | 0.681 | +0.0008 | [-0.0003, +0.0018] | 1.53 |
| c | P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 345 | 128 | 462 | 0.674 | 0.678 | -0.0039 | [-0.0082, +0.0004] | 0.535 | 0.532 | +0.0025 | [+0.0007, +0.0049] | 1.53 |
| c | P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 345 | 128 | 462 | 0.689 | 0.692 | -0.0028 | [-0.0071, +0.0016] | 0.563 | 0.559 | +0.0041 | [-0.0000, +0.0088] | 1.53 |
| c4 | all queries | 23119 | 2756 | 331 | 128 | 462 | 0.791 | 0.796 | -0.0048 | [-0.0072, -0.0024] | 0.678 | 0.681 | -0.0024 | [-0.0040, -0.0008] | 1.33 |
| c4 | P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 331 | 128 | 462 | 0.662 | 0.678 | -0.0160 | [-0.0241, -0.0084] | 0.528 | 0.532 | -0.0043 | [-0.0090, +0.0004] | 1.33 |
| c4 | P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 331 | 128 | 462 | 0.676 | 0.692 | -0.0158 | [-0.0227, -0.0085] | 0.557 | 0.559 | -0.0016 | [-0.0071, +0.0043] | 1.33 |
| c2 | all queries | 23119 | 2756 | 334 | 128 | 462 | 0.792 | 0.796 | -0.0041 | [-0.0065, -0.0016] | 0.679 | 0.681 | -0.0019 | [-0.0034, -0.0003] | 1.41 |
| c2 | P1 image in [0,.2)+[.2,.5) | 2821 | 1283 | 334 | 128 | 462 | 0.668 | 0.678 | -0.0099 | [-0.0168, -0.0035] | 0.532 | 0.532 | -0.0007 | [-0.0046, +0.0028] | 1.41 |
| c2 | P2 textlike in [.5,.8)+[.8,1] | 3166 | 1274 | 334 | 128 | 462 | 0.684 | 0.692 | -0.0076 | [-0.0129, -0.0022] | 0.562 | 0.559 | +0.0028 | [-0.0015, +0.0076] | 1.41 |
