# Session 16 results: the target type known in advance

> **Errata, added 2026-10-04 after the fifth blind pass of the number audit
> (reports/number_audit_2026-10-01.md). The text and tables below are unchanged; where a sentence and a
> verbatim table disagree, the table is right.**
> - Singletons per cell ("438 of 1,959 in P1, 731 of 2,146 in P2 and 1 in M1"): the list leaves out M2,
>   501 of 7,272, and the 21 pdf_scanned queries that belong to no P or M cell; 438 + 731 + 1 + 501 + 21
>   is the 1,692 (results/session16_outputs.md, the singletons line of each encoder).
> - "The descriptive grid shows the trade the brief expected at larger weights": only in part. P1, P2
>   and recall over all queries fall under all four encoders. Of the majority cells only M1 rises, by
>   at most 0.006 under E1 to E3 and 0.009 under E4 (0.698 against 0.689 at tau 0.01), and M2 never
>   rises above the filter at any weight.
> - "H16c dies because the selected prior does almost nothing": that is the reading. By the kill rule
>   it dies because under each encoder at least one of the P1 and P2 intervals does not lie below zero;
>   under E4 the P1 interval is below zero (-0.010 [-0.015, -0.005]) and the P2 interval is not.
> - "c_T - c+F is -0.009, -0.002, -0.013 and -0.004": over all non-singleton queries. By cell it runs
>   from -0.034 (E3, P1) to +0.001 (E4, M1).
> - "As a prior it lowers recall at every weight that changes anything" (the answer to the question):
>   from tau 0.005 upward, under all four encoders. At the selected weights recall over all queries
>   is unchanged under E1 and E4 (0.801 and 0.698) and 0.002 lower under E2 and E3.

Pre-registered in BRIEF.md (9cc0019) before any session 16 number; outputs verbatim in
results/session16_outputs.md (b1595dd). One automated run on the MIG pod used for sessions 13 and 15
(scripts/s16_run.sh), 04:41 to 04:48 UTC on 2 October 2026, about $0.10 including setup. Under all
four encoders typeq.py reproduced the a, c and d ranks of sessions 11, 14 and 15 query for query, and
its self-test (the F, P and T ranks of 200 evaluation queries recomputed with plain loops) found no
difference.

## Hypotheses, verbatim from BRIEF.md (session 16)
H16a (knowing the type does not rescue the pooled vector): on the evaluation queries, the paired 95
percent interval of (c+F minus a+F) in recall@5 lies above zero in P1 and in P2. Read under each
encoder. Kill: H16a is dead under an encoder if either interval includes zero or lies below it.
H16b (Ali's design: with the type known, one pooled vector per type keeps per-type
representatives): on the non-singleton evaluation queries, no paired 95 percent interval of (a_T
minus c_T) in recall@5 over all queries, P1, P2, M1 or M2 lies entirely below -0.02. Read under
each encoder. Kill: H16b is dead under an encoder if any of the five does.
H16c (a composition prior trades the minority for the majority): with tau chosen on the dev
queries, the paired 95 percent interval of (c+P minus c+F) in recall@5 lies below zero in P1 and in
P2. Read under each encoder. Kill: H16c is dead under an encoder if either interval includes zero
or lies above it.
The paper states a hypothesis as holding only where it holds under all four encoders.
Secondary, reported, no kill: every row in every cell with recall@1 and recall@10; x+F minus x,
x+P minus x+F, x_T minus x+F, c_T minus d_T, a_T minus d_T and a_T minus c+F with intervals; the
dev grid and the selected tau per encoder and row; c+P on the evaluation queries for every tau
(descriptive, nothing is chosen on it); per kind, the directories holding it, the directories with a
vector of it, the queries, the singletons and the mean number of directories x+F ranks; singletons
per cell; vectors stored per directory (a_T: the kinds present with a vector).
Expectation, written before the run, not a kill: the filter changes little for image and text
queries, which nearly every folder holds, and more for pdf, table and other queries; H16a survives
under all four encoders; H16b dies in M2 under most encoders (one vector is too coarse for a
folder's many texts, as bc2 was); c+P gains in M1 and M2 and loses in P1 and P2.

## Verdicts

| encoder | H16a: c+F - a+F, P1 and P2 | H16b: a_T - c_T, non-singleton queries | H16c: c+P - c+F, P1 and P2 |
|---|---|---|---|
| E1 | +0.253 [+0.214, +0.293], +0.161 [+0.129, +0.192]: survives | all -0.032 [-0.041, -0.024], M1 -0.043 [-0.060, -0.026], M2 -0.035 [-0.048, -0.023] entirely below -0.02: dead | tau 0.001: -0.001 [-0.003, +0.000], -0.001 [-0.003, +0.000]: dead |
| E2 | +0.500 [+0.462, +0.538], +0.345 [+0.310, +0.383]: survives | all -0.050 [-0.060, -0.041], M1 -0.038 [-0.053, -0.022], M2 -0.068 [-0.084, -0.052]: dead | tau 0.001: -0.001 [-0.002, +0.000], +0.000 [-0.001, +0.001]: dead |
| E3 | +0.204 [+0.163, +0.243], +0.153 [+0.123, +0.182]: survives | all -0.029 [-0.036, -0.021], M1 -0.035 [-0.051, -0.021], M2 -0.036 [-0.048, -0.025]: dead | tau 0.001: +0.001 [+0.000, +0.002], -0.001 [-0.003, +0.000]: dead |
| E4 | +0.442 [+0.398, +0.482], +0.442 [+0.404, +0.479]: survives | all -0.049 [-0.058, -0.040], M1 -0.065 [-0.082, -0.047], M2 -0.045 [-0.060, -0.033]: dead | tau 0.002: -0.010 [-0.015, -0.005], -0.000 [-0.002, +0.001]: dead |

H16a survives under all four encoders. H16b is dead under all four, in the same three cells (all
queries, M1, M2). H16c is dead under all four, for a reason the brief did not foresee (below).

## Reading

- **The filter changes little on these folders.** Over all queries a+F - a is +0.006 to +0.008 and
  c+F - c is +0.004 to +0.006 under the four encoders. Image queries gain nothing (96.8 percent of
  the folders hold an image); the gains are on the rarer kinds, for example under E1 pdf_scanned
  queries (a 0.693 to 0.776, c 0.792 to 0.828) and other (a 0.785 to 0.841, c 0.835 to 0.879). With
  the filter the pooled centroid still loses the minority at about the size it lost without it
  (H16a; under E1 +0.253 and +0.161 against +0.253 and +0.169).
- **One pooled vector per kind, scored against the query's kind (Ali's design), recovers most of
  the pooled centroid's loss but not the majority side.** a_T stores 2.42 vectors per folder. On
  the non-singleton queries a_T - a+F is +0.059 to +0.259 over all queries and +0.206 to +0.607 in
  P1 across the four encoders. Against per-type k-means representatives it falls short in the
  majority cells under every encoder (a_T - c_T in M1 -0.035 to -0.065, in M2 -0.035 to -0.068), so
  H16b is dead. Within one kind a folder can hold many files, and one mean is too coarse for them,
  as bc2 was for the text side in session 11. In P2 under E1 and E3, a_T is above c_T (+0.013 and
  +0.020).
- **Restricting c to the query's kind does not help.** c_T - c+F is -0.009, -0.002, -0.013 and
  -0.004 over all non-singleton queries under E1 to E4, and -0.024 and -0.034 in P1 under E1 and
  E3. A representative of another kind sometimes carries the own folder. With c, the known type is
  worth having only as a filter.
- **The prior.** Under E1 to E3 no weight in the grid raises dev recall@5 of c+P above the filter
  alone (at three decimals, E3 is level at 0.001 and below from 0.002), and under E4 the best weight
  gains 0.002. The rule therefore picked 0.001 or 0.002,
  where the prior changes evaluation recall@5 by at most 0.010 in any of the five cells (E4, P1).
  H16c dies because the selected prior does almost nothing, not because it spares the minority. The
  descriptive grid shows the trade the brief expected at larger weights: under E1 at tau 0.05, P1
  falls from 0.674 to 0.584 and M1 rises from 0.810 to 0.816, and recall@5 over all queries falls
  from 0.801 to 0.775. At tau 0.05 recall over all queries falls under all four encoders.
- **Singletons.** 1,692 of the 17,140 evaluation queries are singletons: 438 of 1,959 in P1, 731 of
  2,146 in P2 and 1 in M1. Under leave-one-out a type-only group has nothing to match for them. In a
  real tree the stored folder holds the target, so this is a property of the protocol, and the x_T
  comparisons are on the other 15,448 queries.

## The answer to the question (Ali, 2 October, 00:03 Toronto)

On these folders, storing each folder's type composition helps little. As a filter it adds 0.004
to 0.008 recall@5, because nearly every folder holds images and text. As a prior it lowers recall
at every weight that changes anything, and it lowers the minority most. Knowing the type helps when
each folder keeps a separate group per type: one pooled vector per type recovers most of the pooled
centroid's loss at 2.4 vectors per folder, and a few k-means representatives per type close the
rest (0.035 to 0.068 recall@5 in the majority cells). A tree of single-type folders would gain more from the
filter, and this corpus cannot show that. For the paper: a short section in the SIGIR version.
