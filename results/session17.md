# Session 17 results: is the minority-modality loss a fingerprint or creator artifact?

> **Errata, added 2026-10-04 after the fifth blind pass of the number audit
> (reports/number_audit_2026-10-01.md). The text and tables below are unchanged; where a sentence and a
> verbatim table disagree, the table is right.**
> - "About half of what the pooled vector loses on image queries is on queries whose folder its file
>   names already give away": what halves is the loss per query. On the 750 clean P1 queries c - a is
>   0.51 (E1), 0.46 (E3), 0.56 (E4) and 0.65 (E2) of its value over all 1,959. The 1,209 P1 queries
>   whose folder the names give away (Flags table) lose more per query and carry most of the lost
>   queries: from the printed rates, about 81, 75, 82 and 79 percent under E1 to E4
>   (1 - 750 x clean rate / (1,959 x rate over all)).
> - "The text-query loss (P2) does not shrink": under E1 and E3. Under E2 and E4 the clean-subset loss
>   is lower than over all queries (+0.298 against +0.348, +0.391 against +0.433), so "all of the
>   text-side loss holds where names do not help" is true of E1 and E3 only.
> - Not in the reading: on the clean subset the loss in the majority cells is smaller as well, and
>   under E1 it is gone in M1 (-0.002 [-0.029, +0.029], against +0.080 over all queries).
> - "Creator clustering ... moves no verdict": of the verdicts it re-read (c - a on S11 and S5, c - d,
>   tb2c - c under E1, E4 - E1 and E2 - E1, c - a on the title and description queries). S3, H5 to H10,
>   H11b's second clause, H12b and sessions 16 and 20 rest on directory resamples. "The P2 intervals
>   widen most": of P1 and P2; M1 widens more than P2 under E1 and E3.
> - "prolific creators contribute larger losses than the median creator": the family-weighted estimate
>   is a mean over families, so the comparison is with the average creator.
> - The brief (BRIEF.md, session 17) gives the filename router's recall@5 in P2 as 0.588; the verbatim
>   table prints 0.587 (1,259 of 2,146). The brief also says only that no c - a number had been
>   computed on the new subsets; counts on them had been read.
> - The last section plans session 18 for after the 4 October usage reset. It was pre-registered and
>   run on 2 October (BRIEF.md, results/session18.md).

Pre-registered in BRIEF.md (0c69594) before any number on the new subsets; outputs verbatim in
results/session17_outputs.md (d641dd1). Chosen on 2 October by an advisory panel of four agents
(three SIGIR reviewers, a literature and data scout, a practitioner and investor, a methodologist)
and two judges who had not seen the deliberation; both judges put these checks first. One automated
run on the MIG pod, 14:10 to 14:13 UTC, stopped by the watcher; about $0.06. No vector was computed.

Checks of the code before any new number: the directory bootstrap of scripts/validity.py reproduces
eval.py's published c - a intervals in P1 and P2 under E1 to E4 and the published H15c intervals
exactly; the descq.py rerun with per-query ranks reproduces the H12a statistic (+0.182 [+0.158,
+0.206]); on S5 it reproduces +0.238 [+0.207, +0.268] and +0.233 [+0.207, +0.262].

## Hypotheses, verbatim from BRIEF.md (session 17)
H17a (the loss survives creator clustering): under each of E1 to E4, the creator-clustered 95
percent interval of (c minus a) in recall@5 lies above zero in P1 and in P2 (all evaluation
queries). Kill: dead under an encoder if either interval includes zero or lies below it. The paper
keeps "under all four encoders" only if it holds under all four.
H17b (the loss is not fingerprint matching): on the clean subset, under E1 and under E3, (c minus a)
in recall@5 is at least +0.05 and its creator-clustered interval lies above zero, in P1 and in P2.
Kill: dead if either condition fails in either cell under either encoder. E2 and E4 reported.
H17c (the metric reproduces): indep_eval.py on the E1 cache gives, for rows a, c and d, recall@5 equal
to eval.py's at three decimals in all, P1, P2, M1 and M2, and identical ranks for at least 99 percent
of the queries of each row (a few exact ties between twin files in different folders may round
differently). Kill: dead otherwise; then nothing else is read until the difference is explained.
Secondary, reported, no kill: c - a on each component subset (names miss; no sibling; not the four
series) and in M1 and M2; family-weighted estimates; families and effective families per cell; the
filename-only baseline with its pooled form; c - d under clustering for E1 to E4 (does any interval
fall entirely below -0.02, the within-0.02 claim); tb2c - c under E1 by the H11a rule under
clustering; the E4 - E1 and E2 - E1 loss differences (H15c) under clustering, and the directory form
checked against the published +0.189 and +0.265; the title and description queries (descq.py rerun
with a new option that writes per-query ranks and changes no number; the E1 H12a statistic must
reproduce +0.182 [+0.158, +0.206]): c - a on image-heavy and text-heavy folders under clustering, and
on the title queries that a filename-only router misses; S3 and S5 under E1, clustered c - a, if
their ranks files are on the volume.
Expectation, written before the run, not a kill: H17a holds under all four (the effects are far from
zero) but the P2 intervals widen; the loss shrinks on the clean subset and stays above +0.05 under E1
and E3; H17c holds.

## Verdicts

H17a survives under all four encoders. H17b survives under E1 and E3 (the deciding encoders) and the
same conditions hold under E2 and E4. H17c survives: the independent re-implementation gives the same
rank as eval.py for every one of the 17,140 queries in rows a, c and d.

| encoder | c - a, P1: directory / creator-clustered 95% | c - a, P2: directory / creator-clustered 95% | clean subset P1 (750 queries) | clean subset P2 (877 queries) |
|---|---|---|---|---|
| E1 | +0.253 [+0.214, +0.294] / [+0.202, +0.303] | +0.169 [+0.136, +0.200] / [+0.119, +0.225] | +0.128 [+0.074, +0.180] | +0.172 [+0.126, +0.222] |
| E2 | +0.500 [+0.462, +0.538] / [+0.456, +0.544] | +0.348 [+0.312, +0.386] / [+0.255, +0.446] | +0.323 [+0.264, +0.383] | +0.298 [+0.247, +0.343] |
| E3 | +0.205 [+0.164, +0.244] / [+0.152, +0.260] | +0.158 [+0.125, +0.188] / [+0.111, +0.209] | +0.095 [+0.038, +0.150] | +0.163 [+0.115, +0.218] |
| E4 | +0.442 [+0.398, +0.482] / [+0.396, +0.482] | +0.433 [+0.396, +0.470] / [+0.317, +0.549] | +0.248 [+0.187, +0.304] | +0.391 [+0.331, +0.444] |

Clean-subset intervals are creator-clustered.

## Reading

- **The fingerprint is real, and it sits on the image side.** File names alone, which no encoder
  sees, place the own folder in the top five for 0.700 of the evaluation queries (P1 0.617, P2
  0.587), level with the pooled E1 vector (0.692). On the queries the names miss, without same-stem
  siblings and outside the four digitization series, the image-query loss (P1) is about half of what
  it is over all queries (E1 0.128 against 0.253, E3 0.095 against 0.205, E2 0.323 against 0.500, E4
  0.248 against 0.442). The text-query loss (P2) does not shrink (E1 0.172 against 0.169, E3 0.163
  against 0.158). Removing the four digitization series alone raises it under E1 (0.212), E2, E3 and
  E4. About half of what the pooled vector loses on image queries is on queries whose folder its file
  names already give away, which fits lost sibling matching (images of one series that resemble each
  other more than anything else); the subsets differ in other ways too, so this is a reading, not a
  decomposition. The rest of the image-side loss, and all of the text-side loss, holds where names
  do not help.
- **Creator clustering widens the intervals and moves no verdict.** The P2 intervals widen most,
  since about 47 effective creator families stand behind the 2,146 P2 queries (P1: 204). Every
  headline interval stays above zero; the E4 - E1 and E2 - E1 loss differences (H15c) stay above
  zero (E4 - E1 P1 [+0.142, +0.239], P2 [+0.184, +0.346]); no c - d interval falls entirely below
  -0.02 under any encoder (the within-0.02 claim holds; the lowest bound is -0.027, E4 P2, with an
  upper bound of -0.010); tb2c - c under E1 still passes the H11a rule (P1 [-0.063, -0.014], M2
  [-0.064, -0.010]). On S5 under E1 the clustered intervals are [+0.198, +0.282] and [+0.196,
  +0.274]. S3's ranks file is not on the volume, so S3 was not re-read.
- **Family-weighted estimates are smaller** (each creator counts once): over all queries P1 +0.133
  and P2 +0.137 under E1 (clean subset +0.059 and +0.115). Prolific creators contribute larger
  losses than the median creator.
- **Natural-language queries hold under clustering**: c - a on image-heavy folders with the title as
  the query is +0.182 [+0.126, +0.242] under E1 (H12a), and +0.134 [+0.101, +0.175] on the 744
  image-heavy title queries a filename-only router misses. Under E2, E3 and E4 the name-missed values
  are +0.239, +0.148 and +0.493.
- **The metric reproduces.** An implementation written from a specification alone, without the
  first one's code, gives identical ranks; the reproductions of sessions 13 to 16 were not
  independent (typeq.py and descq.py import eval.py), and this one is.

## What it means for the paper (to write when the study wraps up)

Report the filename-only baseline and the clean subset next to the headline; give creator-clustered
intervals for every headline claim; say that about half of the image-side loss is sibling matching
and that the text-side loss is not. The sentence "under all four encoders" survives every check.

## Decision for session 18 (by the rule fixed in the brief)

H17a, H17b and H17c hold, so session 18 is the judges' modified Proposal 3: one model-written abstract
per folder against a, c and d on title queries, plus member-description queries written by a
vision-language model outside the Qwen family with the target kept in its folder; caption-for-image
rows; BM25 and filename rows; creator-clustered intervals. To be pre-registered after the 4 October
usage reset.
