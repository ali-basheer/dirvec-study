# dirvec session 14: a third encoder from another vendor (E3) on the confirmation set

Why this session exists. The draft's limitations named its cheapest point of attack: both encoders
came from one vendor (Jina). This session adds E3, Alibaba-NLP/gme-Qwen2-VL-2B-Instruct (revision
9cfa6413f704a7c1cf5064d240748e10c876b286), a vision-language embedder on another base (Qwen2-VL-2B,
1,536 dimensions), on the confirmation set S11 under the session 11 protocol. Ali approved the
compute on 2026-10-01 at 19:40 Toronto.

Pod 3m5g5g80psfwnm (full RTX PRO 6000; the usual card pod had no free GPU), resumed 23:53 UTC,
stopped by the watcher at 01:06:54 UTC after the outputs were pushed: 74 minutes, about $2.60
(balance $20.62 before, $18.04 after). Brief, code and driver committed before anything ran
(65941c3); outputs verbatim in results/session14_outputs.md (a4760bc). Environment: the E1 venv
(torch 2.8.0+cu128, numpy 2.5.2, pillow 12.3.0, scikit-learn 1.9.1) with transformers 4.51.3 first
on the path. Timings: pilot 54 s, `embed.py all` 60 minutes for 25,990 files, eval 4 minutes, title
and description queries 2 minutes.

## Hypotheses (verbatim from BRIEF.md, session 14)

H14a (the loss holds under a third encoder): on the S11 evaluation split (calibration seed
20261102, the session 11 queries), under E3, the paired 95 percent interval of (c minus a) in
recall@5 lies above zero in P1 and in P2. Kill: H14a is dead if either interval includes zero or
lies below it.
H14b (per-modality representatives keep file-level search under E3): no paired 95 percent interval
of (c minus d) in recall@5 over all queries, P1, P2, M1 or M2 lies entirely below -0.02. Kill: H14b
is dead if any of the five does.
Secondary, reported, no kill: recall@5 of a, ac, bc2, tb2, tb2c, c, cc, d, dc in the five cells
(the draft's Table 3 rows), with recall@1 and recall@10; tb2c minus c read by the H11a rule (the
two-vector budget under E3); centering's share of the loss, (ac - a) / (c - a) in P1 and P2; the
gap table (norm of mean image-input minus mean text-input vector, same-folder cosines, uncentered
and centered); purity of blind 2-means; the session 12 title and description queries under E3
(descq.py: H12a's statistic and the per-cell table); E3's ok set against E1's.
Expectation, written before the run, not a kill: the loss holds in both minority cells, of a size
between E1's and E2's if E3's gap lies between theirs; c stays within 0.02 of d.

## Gate

Passed. On the 20 calibration-split directories of E2's pilot (309 files, none skipped), E3 ranks a
text or table file's own-directory images at a median of 21 of 159 (random 80); median best
own-image rank 1 (random 29). On the same check E1 scored 26 and E2 51 (session 11).

## Corpus and queries

E3's ok set is E1's exactly: 25,637 of 25,990 files, the same files (results/session14_outputs.md,
okset). So the evaluation queries are the session 11 ones: 17,140 over 2,035 evaluation
directories, 2,597 directories ranked; P1 1,959 queries, P2 2,146, M1 5,571, M2 7,272.

## Verdicts

**H14a survives.** Under E3, c minus a is +0.205 [+0.164, +0.244] in P1 and +0.158 [+0.125, +0.188]
in P2. The majority cells lose too, by less: +0.076 [+0.060, +0.092] (M1) and +0.062 [+0.049,
+0.076] (M2).

**H14b survives.** c minus d is -0.003 [-0.006, -0.001] over all queries, -0.004 [-0.011, +0.004] in
P1, -0.003 [-0.008, +0.002] in P2, -0.006 [-0.013, -0.000] in M1 and -0.001 [-0.004, +0.003] in M2.
No interval comes near -0.02; the largest point gap is 0.006 (under E1 it was 0.012, under E2 0.018).

The expectation held in part: the loss holds in both minority cells and c stays with d. Its size is
not between E1's and E2's: E3's gap (0.369) is about E1's (0.381 on S11), and so is its loss
(P1 0.205 against E1's 0.253, P2 0.158 against 0.169), not E2's (0.787; 0.500 and 0.348).

## Secondary

Recall@5 on the S11 evaluation split under E3 (vectors per folder in parentheses):

| row | all | P1 | P2 | M1 | M2 |
|---|---:|---:|---:|---:|---:|
| a (1.00) | 0.716 | 0.536 | 0.386 | 0.761 | 0.827 |
| ac (1.00) | 0.731 | 0.552 | 0.471 | 0.768 | 0.826 |
| bc2 (1.95) | 0.782 | 0.709 | 0.593 | 0.812 | 0.833 |
| tb2 (2.00) | 0.782 | 0.699 | 0.520 | 0.828 | 0.846 |
| tb2c (2.00) | 0.788 | 0.682 | 0.565 | 0.831 | 0.849 |
| c (5.20) | 0.811 | 0.741 | 0.544 | 0.837 | 0.889 |
| cc (5.20) | 0.816 | 0.742 | 0.568 | 0.839 | 0.890 |
| d (9.87) | 0.815 | 0.744 | 0.547 | 0.843 | 0.890 |
| dc (9.87) | 0.820 | 0.745 | 0.569 | 0.847 | 0.894 |

- E3 is the strongest of the three encoders on these files: c reaches 0.811 over all queries (E1
  0.796, E2 0.683) and 0.741 and 0.544 in the minority cells (E1 0.674 and 0.539, E2 0.555 and
  0.383). Recall@1 of c 0.714 over all queries, of a 0.604.
- The two-vector budget fails under E3 by the H11a rule: tb2c minus c is -0.023 [-0.030, -0.016]
  over all queries, -0.058 [-0.077, -0.039] in P1, +0.021 [+0.006, +0.037] in P2, -0.006 [-0.015,
  +0.003] in M1 and -0.040 [-0.054, -0.029] in M2; P1 and M2 lie entirely below -0.02. Two vectors
  per folder therefore pass the rule under E1 only (session 11), and fall short under E2 and E3.
- The labelled pair bc2 keeps the minority and loses the majority text queries, as under E1 and E2:
  -0.032 [-0.048, -0.016] in P1, +0.049 [+0.037, +0.062] in P2, -0.024 [-0.040, -0.011] in M1 and
  -0.057 [-0.070, -0.044] in M2 against c. Over all queries the blind pair is ahead of the labelled
  pair (0.788 against 0.782), and the labelled pair is ahead in both minority cells, as under E1
  and E2.
- Centering's share of the loss: (ac - a) / (c - a) is 0.078 in P1 (0.016 of 0.205) and 0.538 in
  P2 (0.085 of 0.158). Under E3 centering recovers almost nothing for image queries in text-heavy
  folders. Across the three encoders on S11 the share runs from 8 to 62 percent (E1 36 and 62, E2
  45 and 56, E3 8 and 54).
- Centering helps the multi-vector rows a little: cc minus c +0.004 [+0.002, +0.007] over all
  queries, +0.025 [+0.017, +0.032] in P2; dc minus d +0.006 [+0.004, +0.008].
- Gap table, evaluation directories: uncentered gap 0.369, same-folder cosine image-image 0.611,
  text-text 0.569, image-text 0.272; centered gap 0.080, cosines 0.543, 0.439, 0.174. Under E3, as
  under E1 and E2, a folder's images and texts are two clusters: the cross cosine is well below
  both within-modality cosines, before and after centering.
- Purity of the blind two-cluster split over the 1,976 evaluation folders with both input groups:
  0.898 uncentered (tb2), 0.879 centered (tb2c). E1 0.918 and 0.885, E2 0.982 and 0.895.
- Per bucket (c minus a): image queries in [0,.2) +0.180 [+0.124, +0.242] and [.2,.5) +0.210;
  text-like queries in [.5,.8) +0.147 [+0.112, +0.180] and [.8,1] +0.198 [+0.135, +0.262].

Title and description queries (descq.py, the session 12 protocol; no instruction on the query, as
on the files):

- H12a's statistic under E3: c minus a over the 1,382 image-heavy directories on Q_title is +0.218
  [+0.190, +0.244]; on Q_desc +0.189 [+0.163, +0.216]. On text-heavy directories +0.044 [+0.020,
  +0.067] and +0.032 [+0.009, +0.055]: the loss is on both sides of a text query here too, smaller
  on the text-heavy side.
- Per bucket on Q_title: +0.038 [+0.000, +0.074] in [0,.2), +0.047 in [.2,.5), +0.206 in [.5,.8),
  +0.248 [+0.193, +0.302] in [.8,1]; on Q_desc +0.075, +0.009 [-0.020, +0.038], +0.154, +0.284.
  The largest loss is in [.8,1] as under E1 and E2; the smallest is in [0,.2) on titles and in
  [.2,.5) on descriptions.
- Centering the query with the file-side text mean (ac minus a) helps under E3, unlike E1 (nothing)
  and E2 (hurts): +0.049 [+0.038, +0.060] over all titles, +0.103 on image-heavy and -0.014 [-0.027,
  +0.000] on text-heavy directories; on descriptions +0.039, +0.098 and -0.025 [-0.037, -0.013].
  It still leaves most of the loss: on image-heavy title queries ac reaches 0.615 against c's 0.729.
- Two vectors against a text query: tb2c minus c is -0.025 [-0.040, -0.012] on Q_title and -0.022
  [-0.035, -0.008] on Q_desc, about what they lose with file queries (-0.023). Under E3 the centered
  pair is the better of the two on titles (0.693 against tb2's 0.674), the reverse of E1 and E2.
- c stays with the flat walk: d minus c +0.004 [-0.001, +0.010] on Q_title and +0.005 [-0.000,
  +0.010] on Q_desc. Levels on Q_title: a 0.582, c 0.718, d 0.722; E3 is weaker than E1 on titles
  (c 0.792), with no instruction on the query.

## What this changes in the draft

- The loss under a vision-language embedder is no longer one vendor's: 0.16 to 0.25 recall@5 in
  the minority cells across E1 (three draws) and E3 (the confirmation set), pre-registered for E3.
- c within 0.02 of the flat walk holds under all three encoders.
- Two vectors per folder: passes the rule under E1 only; the budget the study supports is about
  five per-modality representatives, not two.
- Centering's share: 8 to 62 percent across encoders and cells on S11, not "about half"; under E3
  almost nothing for image queries.
- The limitations: three encoders from two vendors, two of them vision-language embedders; the
  CLIP-family statements still rest on one model.
- Section 7: the query-side centering finding is encoder-dependent (helps under E3), and the
  "smallest in [.2,.5)" and "tb2 better on titles" readings hold under E1 and E2 only.
