# Session 23 outputs, verbatim

Written by scripts/s23_run.sh on the pod, 2026-10-05T10:37Z, repo commit 6665a7e.
Nothing here is edited. The verdicts and the reading are in results/session23.md.

## Run log

```
08:00:49 start, commit a30a27d, tree.py 5c19534283980641
OK: tree.py agrees with the plain implementation on 32945 values (599 queries, 11 summaries; walk, summaries read, first step, flat top 1 and top 3); differences explained by near-ties: 5; the rules of tree_fetch.py hold on the made-up trees.
08:01:01 harvest of whole trees
tree harvest done (full): 261 trees, 33092 files
Repositories read: 2328 ({'ok': 2327, 'oversize': 1}); trees taken: 261, 0.112 of those read; files 33092, image files 8354; directories with a kept file 8587.
Not taken, by the first rule failed: fewer than 8 directories with a kept file 1380, fewer than 5 image files 309, fewer than 40 kept files 219, more than 300 kept files 141, no directory at depth 2 or more 15, fewer than 5 other kept files 1, more than 200 MB 1.
08:16:10 manifest
manifest: 33092 files, 8587 dirs; modality counts {'text': 24065, 'image': 8046, 'other': 332, 'pdf_text': 223, 'table': 376, 'pdf_scanned': 50}
notes: {'image unreadable': 122}
08:16:34 ground truth
08:19:32 corpus files pushed
08:19:51 manifest rows 33092; files missing or of another size 0
08:19:51 E1: embed all files
10:36:44 E1: { "files": 33092, "ok": 32060, "skipped": {  "no encoder path for modality other ext doc": 1,  "image smaller than 28 px (16x16)": 356,  "image smaller than 28 px (19x19)": 11,  "image smaller than 28 px (20x20)": 79,  "image smaller than 28 px (1x1)": 55,  "image smaller than 28 px (14x14)": 1,  "i
10:36:44 E1: the walk
```

## Harvest

Repositories read: 2328 ({'ok': 2327, 'oversize': 1}); trees taken: 261, 0.112 of those read; files 33092, image files 8354; directories with a kept file 8587.
Not taken, by the first rule failed: fewer than 8 directories with a kept file 1380, fewer than 5 image files 309, fewer than 40 kept files 219, more than 300 kept files 141, no directory at depth 2 or more 15, fewer than 5 other kept files 1, more than 200 MB 1.

## build_gt.py report

```
{
 "queries": 21482,
 "qualifying_dirs": 3178,
 "qualifying_dirs_per_bucket": {
  "[0,.2)": 2593,
  "[.2,.5)": 92,
  "[.5,.8)": 70,
  "[.8,1]": 423
 },
 "queries_per_bucket": {
  "[0,.2)": 16887,
  "[.2,.5)": 507,
  "[.5,.8)": 327,
  "[.8,1]": 3761
 },
 "queries_per_modality": {
  "text": 16678,
  "image": 4013,
  "other": 304,
  "pdf_text": 172,
  "table": 308,
  "pdf_scanned": 7
 },
 "dedupe": {
  "exact_files": 3950,
  "exact_pairs": 11153,
  "exact_pairs_cross_dir": 9905,
  "exact_pairs_within_dir": 1248,
  "files_excluded_as_queries_degenerate_image": 190,
  "files_excluded_as_queries_dup": 6266,
  "files_phashed": 7897,
  "files_simhashed": 23023,
  "image_files": 3480,
  "image_pairs": 54235,
  "image_pairs_cross_dir": 44345,
  "image_pairs_within_dir": 9890,
  "text_files": 2266,
  "text_pairs": 5267,
  "text_pairs_cross_dir": 5059,
  "text_pairs_within_dir": 208
 },
 "kill_criterion_passed": true
}
```

## S23 E1: jina-embeddings-v4 (2048 dimensions; one bit per dimension is 256 bytes a vector)

Queries: 20814 over 260 repositories and 259 owners (10 files left out as queries because their directory holds no other embedded file); minority 2844 (from 208 owners). Directories holding an embedded file per repository: mean 37.9 (query-weighted); depth of the target: 0 1449, 1 3670, 2 5620, 3 4440, 4 2420, 5 1731, 6 397, 7 262, 8 393, 9 258, 10 111, 11 21, 12 35, 13 4, 14 3. Summaries a walk reads, mean over queries: mean@2048 15.6, usample@2048 14.0, fsample@2048 13.5, sample@2048 13.7, all@2048 16.3, mean@8192 15.6, usample@8192 15.6, fsample@8192 15.3, sample@8192 15.5, all@8192 16.3; flat reads 37.9. All rates below are owner-weighted: the mean over owners of the owner's mean.

### S23 E1 success: the walk stops in the target directory; flat: the target is first among all directories

| budget | summary | walk, all (20814) | walk, minority (2844) | walk, not minority (17970) | flat, all | flat, minority | flat, not minority | flat top 3, all | first step right, all | first step right, minority |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 KiB | mean | 0.630 | 0.686 | 0.619 | 0.671 | 0.782 | 0.651 | 0.859 | 0.814 | 0.791 |
| 2 KiB | usample | 0.542 | 0.646 | 0.519 | 0.599 | 0.745 | 0.575 | 0.825 | 0.739 | 0.750 |
| 2 KiB | fsample | 0.528 | 0.710 | 0.489 | 0.597 | 0.745 | 0.573 | 0.823 | 0.717 | 0.814 |
| 2 KiB | sample | 0.537 | 0.723 | 0.499 | 0.599 | 0.746 | 0.575 | 0.825 | 0.729 | 0.824 |
| 2 KiB | all | 0.625 | 0.753 | 0.603 | 0.625 | 0.753 | 0.603 | 0.840 | 0.839 | 0.862 |
| 8 KiB | mean | 0.630 | 0.686 | 0.619 | 0.671 | 0.782 | 0.651 | 0.859 | 0.814 | 0.791 |
| 8 KiB | usample | 0.614 | 0.731 | 0.592 | 0.622 | 0.753 | 0.600 | 0.840 | 0.822 | 0.832 |
| 8 KiB | fsample | 0.605 | 0.753 | 0.580 | 0.622 | 0.753 | 0.600 | 0.839 | 0.809 | 0.857 |
| 8 KiB | sample | 0.613 | 0.753 | 0.589 | 0.622 | 0.753 | 0.600 | 0.840 | 0.819 | 0.856 |
| 8 KiB | all | 0.625 | 0.753 | 0.603 | 0.625 | 0.753 | 0.603 | 0.840 | 0.839 | 0.862 |
| none | names | 0.477 | 0.649 | 0.445 | 0.478 | 0.655 | 0.450 | 0.701 | 0.740 | 0.786 |
| none | chance | 0.069 | 0.092 | 0.063 | 0.047 | 0.049 | 0.046 | | | |

### S23 E1 what is read and what is stored (reads owner-weighted; flat reads one summary a directory)

| budget | summary | summaries the walk reads, all | minority | flat reads, all | walk reads as a share of flat | vectors stored per own-files summary | per subtree summary | walk decided by a near-tie, all | flat near-tie at the target, all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 KiB | mean | 14.1 | 11.0 | 32.7 | 0.43 | 0.00 | 0.00 | 0.001 | 0.000 |
| 2 KiB | usample | 13.0 | 10.5 | 32.7 | 0.40 | 2.90 | 3.97 | 0.006 | 0.003 |
| 2 KiB | fsample | 12.7 | 11.6 | 32.7 | 0.39 | 2.86 | 3.86 | 0.009 | 0.003 |
| 2 KiB | sample | 12.9 | 11.7 | 32.7 | 0.39 | 2.90 | 3.97 | 0.009 | 0.003 |
| 2 KiB | all | 14.8 | 12.2 | 32.7 | 0.45 | 3.77 | 11.95 | 0.008 | 0.003 |
| 8 KiB | mean | 14.1 | 11.0 | 32.7 | 0.43 | 0.00 | 0.00 | 0.001 | 0.000 |
| 8 KiB | usample | 14.4 | 11.7 | 32.7 | 0.44 | 3.58 | 7.36 | 0.009 | 0.003 |
| 8 KiB | fsample | 14.2 | 12.1 | 32.7 | 0.43 | 3.55 | 6.95 | 0.009 | 0.003 |
| 8 KiB | sample | 14.3 | 12.1 | 32.7 | 0.44 | 3.58 | 7.36 | 0.009 | 0.003 |
| 8 KiB | all | 14.8 | 12.2 | 32.7 | 0.45 | 3.77 | 11.95 | 0.008 | 0.003 |
| none | names | 14.7 | 12.9 | 32.7 | 0.45 | 0.00 | 0.00 | 0.191 | 0.153 |

### S23 E1 walk success by the depth of the target (owner-weighted)

| budget | summary | root (1449) | depth 1 (3670) | depth 2 (5620) | depth 3 or more (10075) |
|---|---|---:|---:|---:|---:|
| 2 KiB | mean | 0.675 | 0.551 | 0.573 | 0.574 |
| 2 KiB | usample | 0.702 | 0.525 | 0.498 | 0.450 |
| 2 KiB | fsample | 0.698 | 0.522 | 0.473 | 0.439 |
| 2 KiB | sample | 0.698 | 0.526 | 0.482 | 0.448 |
| 2 KiB | all | 0.574 | 0.562 | 0.594 | 0.575 |
| 8 KiB | mean | 0.675 | 0.552 | 0.572 | 0.574 |
| 8 KiB | usample | 0.623 | 0.557 | 0.572 | 0.558 |
| 8 KiB | fsample | 0.639 | 0.551 | 0.557 | 0.544 |
| 8 KiB | sample | 0.627 | 0.551 | 0.568 | 0.557 |
| 8 KiB | all | 0.574 | 0.562 | 0.594 | 0.575 |
| none | names | 0.433 | 0.425 | 0.417 | 0.426 |
| none | chance | 0.209 | 0.116 | 0.052 | 0.016 |

### S23 E1 differences in success (owner-weighted, 10,000 resamples of owners)

| difference | queries | owners | point | 95% | 98.33% | reading |
|---|---:|---:|---:|---|---|---|
| H23a (primary): walk, fsample - mean, minority, 2 KiB | 2844 | 208 | +0.024 | [-0.014, +0.063] | [-0.022, +0.073] | inconclusive |
| H23b (primary): walk, fsample - usample, minority, 2 KiB | 2844 | 208 | +0.064 | [+0.034, +0.097] | [+0.028, +0.104] | the kinds matter (lower bound above zero) |
| H23c (primary): walk - flat, fsample, all queries, 2 KiB | 20814 | 259 | -0.069 | [-0.083, -0.056] | [-0.086, -0.054] | inferior (upper bound under -0.02) |
| 2 KiB: walk, fsample - mean, all | 20814 | 259 | -0.103 | [-0.121, -0.085] | [-0.125, -0.080] | none |
| 2 KiB: walk, usample - mean, minority | 2844 | 208 | -0.040 | [-0.072, -0.007] | [-0.079, +0.001] | none |
| 2 KiB: walk, sample - fsample, minority | 2844 | 208 | +0.013 | [+0.005, +0.023] | [+0.003, +0.025] | none |
| 2 KiB: walk, sample - usample, minority (the kinds with every slot used) | 2844 | 208 | +0.077 | [+0.047, +0.108] | [+0.041, +0.116] | none |
| 2 KiB: walk, all - fsample, minority | 2844 | 208 | +0.043 | [+0.024, +0.063] | [+0.020, +0.068] | none |
| 2 KiB: walk, fsample - names, all | 20814 | 259 | +0.050 | [+0.026, +0.074] | [+0.021, +0.080] | none |
| 2 KiB: walk, fsample - names, minority | 2844 | 208 | +0.061 | [+0.015, +0.106] | [+0.004, +0.118] | none |
| 2 KiB: flat, fsample - mean, minority | 2844 | 208 | -0.037 | [-0.062, -0.014] | [-0.068, -0.008] | none |
| 2 KiB: walk - flat, mean, all | 20814 | 259 | -0.041 | [-0.053, -0.029] | [-0.056, -0.026] | none |
| 2 KiB: walk - flat, fsample, minority | 2844 | 208 | -0.035 | [-0.052, -0.019] | [-0.057, -0.016] | none |
| 8 KiB: walk, fsample - mean, minority, 8 KiB | 2844 | 208 | +0.067 | [+0.031, +0.103] | [+0.024, +0.111] | none |
| 8 KiB: walk, fsample - usample, minority, 8 KiB | 2844 | 208 | +0.021 | [+0.007, +0.039] | [+0.005, +0.044] | none |
| 8 KiB: walk - flat, fsample, all queries, 8 KiB | 20814 | 259 | -0.017 | [-0.023, -0.011] | [-0.024, -0.010] | none |
| 8 KiB: walk, fsample - mean, all | 20814 | 259 | -0.025 | [-0.041, -0.009] | [-0.044, -0.005] | none |
| 8 KiB: walk, usample - mean, minority | 2844 | 208 | +0.046 | [+0.012, +0.080] | [+0.004, +0.088] | none |
| 8 KiB: walk, sample - fsample, minority | 2844 | 208 | +0.001 | [-0.002, +0.003] | [-0.002, +0.003] | none |
| 8 KiB: walk, sample - usample, minority (the kinds with every slot used) | 2844 | 208 | +0.022 | [+0.007, +0.040] | [+0.005, +0.045] | none |
| 8 KiB: walk, all - fsample, minority | 2844 | 208 | +0.001 | [-0.004, +0.005] | [-0.006, +0.006] | none |
| 8 KiB: walk, fsample - names, all | 20814 | 259 | +0.127 | [+0.106, +0.150] | [+0.101, +0.155] | none |
| 8 KiB: walk, fsample - names, minority | 2844 | 208 | +0.104 | [+0.060, +0.147] | [+0.050, +0.156] | none |
| 8 KiB: flat, fsample - mean, minority | 2844 | 208 | -0.029 | [-0.054, -0.005] | [-0.060, +0.001] | none |
| 8 KiB: walk - flat, mean, all | 20814 | 259 | -0.041 | [-0.053, -0.030] | [-0.056, -0.027] | none |
| 8 KiB: walk - flat, fsample, minority | 2844 | 208 | -0.000 | [-0.004, +0.004] | [-0.004, +0.005] | none |

