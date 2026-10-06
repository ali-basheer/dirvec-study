# dirvec session 15: a second CLIP-family dual tower (E4, Nomic Embed v1.5) on the confirmation set

Why this session exists. After session 14 every statement about a CLIP-family dual tower rested on
one model, jina-clip-v2 (E2), which is also the weakest cross-modal encoder on these files. This
session adds E4, Nomic Embed v1.5 from a third vendor: the image tower nomic-embed-vision-v1.5
trained contrastively against the frozen text tower nomic-embed-text-v1.5 (768 dimensions), on S11
under the session 11 protocol. Ali asked for it on 2026-10-01 at 22:05 Toronto ("run it, make it
robust").

Brief, code and driver committed before anything ran (7a0bc62); outputs verbatim in
results/session15_outputs.md (916875b). Pod bmao44n64ohrwp (PRO 6000 MIG 1g.24gb, 3.4 vCPUs,
$0.59 an hour), resumed 02:18:55 UTC and stopped by the watcher at 02:59:16 UTC: 40 minutes. The
RTX PRO 4500 pod the brief named first (8ojyoafh1y9b1y) turned out to be in US-KS-2 without the
dirvec volume; it ran for about a minute and was stopped, and both RTX PRO 6000 pods had no free
GPU, so the run used the MIG slice with 4 preparation threads instead of 14 (the number of threads
changes no vector) and a watcher deadline of 4 hours instead of 3. Cost about $0.40 (balance $18.03
before, $17.63 after). Environment: the E1 venv as is (transformers 4.52.4, torch 2.8.0+cu128,
einops 0.8.2). Timings: pilot 22 s, `embed.py all` 24 minutes for 25,990 files, eval 8 minutes.

One step failed and was resumed. xenc.py read the query key as `path` where eval.py writes
`query_path`, and stopped with a KeyError after the pilot, the embedding, the ok-set check and the
eval had finished. The watcher's stop was caught before it fired, the key name was fixed (b5e6991,
nothing else changed) and the driver resumed with S15_RESUME=1, which skipped every step whose
output was already written. The run log in the outputs file shows the failure and the resume.

## Hypotheses (verbatim from BRIEF.md, session 15)

H15a (the loss under a second dual tower): on the S11 evaluation split (calibration seed 20261102,
the session 11 queries), under E4, the paired 95 percent interval of (c minus a) in recall@5 lies
above zero in P1 and in P2. Kill: H15a is dead if either interval includes zero or lies below it.
H15b (per-modality representatives keep file-level search under E4): no paired 95 percent interval
of (c minus d) in recall@5 over all queries, P1, P2, M1 or M2 lies entirely below -0.02. Kill: H15b
is dead if any of the five does.
H15c (the larger loss belongs to dual towers, not to one model): on the same queries, the loss
under E4 exceeds the loss under E1: the paired 95 percent interval of [(c - a) under E4] minus
[(c - a) under E1] in recall@5, over 1000 resamples of the cell's evaluation directories with
eval.py's cell seeds (scripts/xenc.py), lies above zero in P1 and in P2. Kill: H15c is dead if
either interval includes zero or lies below it.
Secondary, reported, no kill: everything session 14 reported (the Table 3 rows with recall@1 and
@10, tb2c minus c read by the H11a rule, centering's share, the gap table, purity, the title and
description queries, the ok set against E1, the longest E4 text input); xenc.py's statistic for E4
against E2 and E3 and for E2 against E1; xenc.py's per-encoder c - a intervals checked against
eval.py's.
Expectation, written before the run, not a kill: E4's gap is wide like E2's and its loss lies above
E1's in both minority cells; c stays within 0.02 of d.

## Gate

Passed, weakly. On the 20 calibration-split directories of E2's pilot (309 files, none skipped),
E4 ranks a text or table file's own-directory images at a median of 65.5 of 159 (random 80); median
best own-image rank 14 (random 29). With the "search_document: " prefix the median is 69. On the
same check E1 scored 26, E2 51 and E3 21. E4 is the weakest of the four on this check.

## Corpus, queries and inputs

E4's ok set is E1's exactly: 25,637 of 25,990 files (results/session15_outputs.md, okset). The
evaluation queries are the session 11 ones: 17,140 over 2,035 evaluation directories, 2,597
directories ranked; P1 1,959 queries, P2 2,146, M1 5,571, M2 7,272.

Text inputs and E4's own tokenizer (scripts/count_e4_tokens.py, run on the pod after the embedding,
output /workspace/logs/s15/e4_tokens.txt): of 12,757 text inputs, 1,738 pass 2,048 E4 tokens (the
dynamic rotary scaling is in effect for them) and 14 pass 8,192 and are cut by E4's tokenizer
(eleven office documents converted by pandoc, two source-code PDFs and one CSV; the longest has
18,666 E4 tokens). E4 therefore reads the same characters as E1 to E3 for 12,743 of the 12,757 text
inputs. The cause is tokenization: a 2,000-token E1 cut of text with long runs of punctuation (table
rules made of dashes, code) becomes many more WordPiece tokens.

## Verdicts

**H15a survives.** Under E4, c minus a is +0.442 [+0.398, +0.482] in P1 and +0.433 [+0.396, +0.470]
in P2. The pooled centroid finds the directory of a minority-modality query in the top five 0.6
percent (P1) and 0.5 percent (P2) of the time, against 44.8 and 43.8 percent for c. The majority
cells lose too: +0.292 [+0.262, +0.324] (M1) and +0.221 [+0.195, +0.245] (M2).

**H15b survives.** c minus d is -0.012 [-0.015, -0.008] over all queries, -0.013 [-0.022, -0.003]
in P1, -0.018 [-0.024, -0.010] in P2, -0.013 [-0.024, -0.004] in M1 and -0.008 [-0.013, -0.004] in
M2. No interval lies entirely below -0.02, so the hypothesis survives by the rule. Unlike under E1
to E3, every interval lies entirely below zero: under E4 c is 0.008 to 0.018 below the flat walk in
every cell, and two lower bounds reach -0.024.

**H15c survives.** On the same queries, the loss under E4 minus the loss under E1 is +0.189
[+0.145, +0.231] in P1 and +0.265 [+0.226, +0.305] in P2. xenc.py's per-encoder c - a intervals
equal eval.py's for all four encoders in P1 and P2 (the check in the outputs file).

The expectation held: E4's gap (1.095) is wider than E2's (0.787), its loss lies above E1's in
both minority cells, and c stays within 0.02 of d.

## Secondary

Recall@5 on the S11 evaluation split under E4 (vectors per folder in parentheses):

| row | all | P1 | P2 | M1 | M2 |
|---|---:|---:|---:|---:|---:|
| a (1.00) | 0.397 | 0.006 | 0.005 | 0.397 | 0.621 |
| ac (1.00) | 0.544 | 0.082 | 0.189 | 0.572 | 0.756 |
| bc2 (1.95) | 0.633 | 0.421 | 0.451 | 0.616 | 0.762 |
| tb2 (2.00) | 0.640 | 0.415 | 0.426 | 0.624 | 0.780 |
| tb2c (2.00) | 0.640 | 0.331 | 0.398 | 0.657 | 0.788 |
| c (5.20) | 0.693 | 0.448 | 0.438 | 0.689 | 0.842 |
| cc (5.20) | 0.703 | 0.460 | 0.465 | 0.693 | 0.850 |
| d (9.87) | 0.705 | 0.460 | 0.456 | 0.702 | 0.850 |
| dc (9.87) | 0.715 | 0.470 | 0.466 | 0.715 | 0.858 |

- Strength: over all queries c reaches 0.693 under E4, against 0.811 (E3), 0.796 (E1) and 0.683
  (E2). In the minority cells E4's c is 0.448 and 0.438 (E2 0.555 and 0.383). The two dual towers
  are the two weakest cross-modal encoders here, by the pilot check and by c over all queries.
- The loss between encoders (xenc.py, paired over directories): E2 minus E1 is +0.247 [+0.208,
  +0.286] in P1 and +0.179 [+0.142, +0.223] in P2; E4 minus E3 +0.237 [+0.194, +0.282] and +0.276
  [+0.237, +0.321]; E4 minus E2 -0.058 [-0.088, -0.025] in P1 and +0.086 [+0.067, +0.105] in P2.
  E4 loses more than E1 and E3, and E2 more than E1, in both minority cells with intervals above
  zero. E2 against E3 was not computed (point differences +0.295 and +0.190). Between the two towers
  the order differs by cell.
- Per bucket (c minus a): image queries in [0,.2) +0.284 [+0.208, +0.353] and [.2,.5) +0.480;
  text-like queries in [.5,.8) +0.472 and [.8,1] +0.284 [+0.219, +0.347].
- Two vectors fail under E4 by the H11a rule: tb2c minus c is -0.054 [-0.063, -0.045] over all
  queries, -0.117 [-0.147, -0.090] in P1, -0.040 [-0.057, -0.023] in P2, -0.032 [-0.045, -0.019] in
  M1 and -0.054 [-0.070, -0.041] in M2; four of the five intervals lie entirely below -0.02. Two
  vectors per folder pass the rule under E1 only, of four encoders.
- The labelled pair bc2 against c: -0.027 [-0.045, -0.009] in P1, +0.013 [+0.001, +0.025] in P2,
  -0.073 [-0.092, -0.054] in M1, -0.080 [-0.096, -0.064] in M2, the same pattern as under E1 to E3
  (little loss or a gain in the minority cells, a loss on the majority). Over all queries the blind
  pair is ahead of the labelled pair (0.640 against 0.633), and the labelled pair is ahead in both
  minority cells.
- Centering's share of the loss, (ac - a) / (c - a), from the printed levels as for E1 to E3: 17
  percent in P1 (0.076 of 0.442) and 42 percent in P2 (0.184 of 0.433). Across the four encoders on
  S11 the share runs from 8 to 62 percent (E1 36 and 62, E2 45 and 56, E3 8 and 54, E4 17 and 42).
- Centering helps the multi-vector rows: cc minus c +0.010 [+0.006, +0.013] over all queries,
  +0.027 [+0.019, +0.036] in P2; dc minus d +0.010 [+0.008, +0.013].
- Gap table, evaluation directories: uncentered gap 1.095, same-folder cosine image-image 0.917,
  text-text 0.698, image-text 0.066; centered gap 0.106, cosines 0.555, 0.406, 0.034. E4 has the
  widest gap of the four, and a folder's images and texts are close to orthogonal (cross cosine
  0.066).
- Purity of the blind two-cluster split over the 1,976 evaluation folders with both input groups:
  0.998 uncentered (tb2), 0.932 centered (tb2c).

Title and description queries (descq.py, the session 12 protocol; the "search_query: " prefix, as on
the files):

- H12a's statistic under E4: c minus a over the 1,382 image-heavy directories on Q_title is +0.548
  [+0.522, +0.577]; on Q_desc +0.555 [+0.526, +0.584]. On text-heavy directories +0.237 [+0.211,
  +0.265] and +0.223 [+0.196, +0.251]. The pooled centroid finds an image-heavy folder from its
  title in the top five 0.7 percent of the time (Q_title, a 0.007; Q_desc 0.005).
- Per bucket on Q_title: +0.095 [+0.052, +0.140] in [0,.2), +0.312 in [.2,.5), +0.564 in [.5,.8),
  +0.510 [+0.458, +0.557] in [.8,1]; on Q_desc +0.097, +0.290, +0.564, +0.530. Under E4 the largest
  loss is in [.5,.8) and the smallest in [0,.2), where under E1 and E2 the largest was in [.8,1] and
  the smallest in [.2,.5).
- Centering the query with the file-side text mean helps under E4 everywhere except the most
  text-heavy bucket: ac minus a +0.193 [+0.177, +0.209] over all titles, +0.248 on image-heavy and
  +0.131 [+0.109, +0.151] on text-heavy directories; on descriptions +0.236, +0.327 and +0.138
  [+0.114, +0.162]. In [0,.2) it does nothing (-0.007 [-0.036, +0.019] and -0.015 [-0.045, +0.015]).
  It still leaves most of the loss: on image-heavy title queries ac reaches 0.255 against c's 0.555.
- Two vectors against a text query: tb2c minus c is -0.042 [-0.057, -0.027] on Q_title and -0.008
  [-0.025, +0.009] on Q_desc, less than with file queries (-0.054). The centered pair is ahead of the
  uncentered one on both text query sets (0.566 against 0.563 on titles, 0.627 against 0.621 on
  descriptions); with file queries the two are level over all queries (0.640 each).
- c falls further behind the flat walk with text queries under E4: d minus c is +0.020 [+0.013,
  +0.026] on Q_title and +0.025 [+0.018, +0.033] on Q_desc (under E1 to E3 at most 0.011). Levels on
  Q_title: a 0.205, c 0.608, d 0.628; E4 is the weakest of the four encoders on titles.

## What this changes in the draft

- The CLIP-family statements no longer rest on one model. Under two dual towers from different
  vendors the loss is 0.35 to 0.50 in the minority cells, and the larger loss than under E1 is now
  pre-registered and paired (H15c), with E2 against E1 reported the same way.
- c within 0.02 of the flat walk holds under all four encoders by the rule; under E4 c is below d in
  every cell (0.008 to 0.018), and with text queries by 0.020 and 0.025.
- Two vectors per folder pass under one encoder of four.
- Centering's share: 8 to 62 percent across four encoders (E4 17 and 42).
- Section 7: query-side centering helps under E3 and E4 and does nothing or hurts under E1 and E2;
  under E4 the loss peaks in [.5,.8), not [.8,1]; "c within 0.011 of d in all runs" holds for six of
  the eight runs.
- The limitations: four encoders from three vendors; both dual towers are weak on the pilot check
  and the two weakest cross-modal encoders here, so part of their larger loss is the encoders; E4
  cuts 14 of 12,757 texts at 8,192 tokens.

## Note added after the run (2026-10-01, Toronto)

The pilot report and the cache's index rows on the pod give E4's dtype as "bfloat16". embed.py
wrote that label as a constant for every model, and it is wrong for E4: the brief fixed float32, and
the E4 branch loads both towers without a torch_dtype, so in float32 (a CPU load through the same
code path reports float32). embed.py now writes the dtype the weights were loaded in. No vector and
no number in this file changes.

