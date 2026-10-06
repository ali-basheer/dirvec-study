# Session 26: representatives for mixed folders only, at the natural mix, and names with vectors

Brief: BRIEF.md, session 26 (commit c0f1caa, before any number below existed). Code: scripts/s26.py,
scripts/s26_report.py, scripts/s26_run.sh (c4bf7f2). Outputs, verbatim: results/session26_outputs.md
(run on the session 19 pod, 5 October 2026, 17:26 to 17:31 UTC, CPU only, from the cached vectors);
per-query ranks and counts in data/s26_<set>_<enc>.npz, from which `s26.py report` rebuilds every
number. The paper marks all of it post hoc: it was registered after the blind review, on draws that
earlier sessions had already read.

## Gates
All passed on the second run. For S19 under E1, E4 and E2, S24 under E1 and S11 under E1 to E4, the
ranks of a, c and d equal the stored eval.py ranks for every evaluation query (7,372, 12,951 and
17,140). The name router gives name_rank_d of the flags for every GitHub query and the File names row
on S11 (0.700, 0.617, 0.587, 0.786, 0.688). The counts of siblings agree with the flags. Session 25's
natural-mix c minus a with the scored sets' candidates comes out again from these ranks, -0.014
[-0.022, -0.005], to the third decimal of its interval.

## Verdicts (E1, G1 and G2 pooled, natural-mix candidates, 98.33 percent intervals, owners)
- **H26a confirmed.** m minus a is +0.143 [+0.094, +0.197] in P1s (732 queries, 258 owners) and
  +0.180 [+0.134, +0.228] in P2s (1,024 queries, 294 owners).
- **H26b not inferior.** Over all queries at the natural mix m minus a is +0.001 [+0.000, +0.002]
  (lower bound +0.0004, margin -0.005).
- **H26c failed.** Over all queries at the natural mix m minus c is +0.007 [-0.000, +0.015]; the
  lower bound is -0.0001, not above zero (95 percent: [+0.001, +0.013]).
- **H26d survived under E1 and E3.** On S11, with names fused, c minus a is +0.104 (creator-clustered
  [+0.067, +0.144]) in P1 and +0.067 ([+0.041, +0.097]) in P2 under E1, and +0.075 ([+0.044,
  +0.109]) and +0.057 ([+0.035, +0.086]) under E3.

## Readings
1. **The policy.** Representatives for folders that hold an image and another file, the mean for the
   rest, keep most of the minority gain at the natural mix and cost nothing over all directories.
   Against representatives for every folder it gives up 0.021 [0.006, 0.036] in P1s and 0.012
   [0.004, 0.021] in P2s (95 percent). The own folder of a P1s or P2s query is represented the same
   way under m and c for 1,718 of the 1,756 queries (98 percent; for the other 38 the folder without
   the query holds no file labelled image, counted from the npz files after the report), so that
   difference comes from competitors kept as means. On the queries of the
   other directories m equals a (+0.000 [-0.000, +0.001]) and c costs -0.009 [-0.015, -0.002].
2. **The cost of representatives everywhere, re-estimated.** With candidates at the natural mix (every
   other-stratum folder of a draw and 26 or 31 mixed ones, about 630 in all), c minus a over all
   queries at the natural mix is -0.006 [-0.012, -0.000], against -0.014 [-0.022, -0.005] with the
   scored sets' candidates (session 25). Most of session 25's figure came from candidates that
   over-sample mixed folders.
3. **The mean beside the representatives (u).** At the natural mix u minus a is +0.004 [+0.000,
   +0.009] over all queries, +0.154 in P1s and +0.192 in P2s (c: +0.164 and +0.192). Under E1 on S11
   u reaches recall@5 0.804 over all queries, as d does. No verdict was registered for u.
4. **Other settings.** With 100 natural-mix candidates m minus a is +0.059 and +0.135 in P1s and P2s
   and +0.000 over all queries; with the scored sets' candidates +0.191 and +0.181 and -0.004
   [-0.008, +0.000]. m2 (two group means for mixed folders) is level with m: +0.136 and +0.190 in P1s
   and P2s and +0.001 over all queries at the natural mix.
5. **Other encoders (G1, secondary).** At the natural mix m minus a over all queries is +0.008
   [+0.007, +0.009] under E4 and +0.004 [+0.002, +0.005] under E2, and +0.558 and +0.432 (E4) and
   +0.538 and +0.337 (E2) in P1s and P2s (86 and 98 owners, short of the owner minimum).
6. **Names with vectors.** Reciprocal rank fusion (k = 60) with the name router keeps about two
   fifths of the loss: on S11 under E1 fused c minus a is +0.104 and +0.067 in P1 and P2 against
   +0.253 and +0.169 unfused, and on GitHub pooled +0.083 [+0.051, +0.116] and +0.067 [+0.044, +0.091]
   in P1s and P2s against +0.205 and +0.186. Equal-weight fusion helps the pooled vector and the two
   dual towers, and lowers the representatives of the vision-language embedders over all queries
   (S11 E1: names + c 0.780 against c 0.796; E3: 0.790 against 0.811). On GitHub, where names alone
   reach 0.271 and 0.265, fusion lowers recall from 0.706 to 0.387 (S19, c). Fusion with names is
   therefore not a free hybrid here, and the loss remains inside it.
7. **m on Zenodo.** 2,500 of the 2,597 S11 folders are mixed by the rule, and m minus c is -0.000
   [-0.002, +0.001] over all queries under E1.

## What this changes in the paper
- The recommendation is now tested: representatives where a folder mixes media, by file type, and the
  mean elsewhere, keep most of the minority gain and are level with the mean over all directories at
  the natural mix. The registered comparison with representatives for every folder failed by its
  98.33 percent bound; the paper says so.
- The natural-mix cost of representatives for every folder is -0.006 with natural-mix candidates,
  beside session 25's -0.014 with the scored sets' candidates.
- "A hybrid of names and vectors was not run" goes; the fusion result replaces it, for the two
  vision-language embedders (under the dual towers most of the loss remains in the fusion).
- A check of the new text by a separate agent found no wrong number and fourteen points of framing
  (two fifths true under E1 and E3 only, the candidate settings reported selectively, H26c missing
  from the summaries, post hoc marks); all were taken into both papers.

## Deviations
- The first run (17:22 UTC) stopped at the gate as registered: under E1 on S19 one query's rank of a
  differed from eval.py's (data/corpus_s19/gh_428155597_0/demo.gif, 129 against 128), a float32
  near-tie. indep_eval.rep_a takes the norm and the own score by other kernels than eval.py's
  build("a"). s26.py now builds a, and the group means of m2, as eval.py does (c4bf7f2), and the
  second run passed every gate. The report of the first run was never produced; only that query's
  rank of a was read from its files.
- The first run's S24 and S11 E1 files had passed their gates; they were scored again with the
  corrected a, with the other sets.
