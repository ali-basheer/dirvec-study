# Session 20 results: per-modality representatives in a metadata field of fixed size

> **Errata, added 2026-10-04 after the fifth blind pass of the number audit
> (reports/number_audit_2026-10-01.md). The text and tables below are unchanged; where a sentence and a
> verbatim table disagree, the table is right.**
> - "its recall@5 there is within 0.007 of c in float32 (... E1, E3 and E4 within 0.001)": by the
>   rounded levels. The paired table gives c_bin - c_f32 over all queries under E3 as -0.002
>   [-0.004, +0.000].
> - "One bit per dimension is free under E1 and E3": by the H20b rule against d. Against c in float32
>   the interval excludes zero in M2 under E1 (-0.003 [-0.006, -0.001]) and in M1 and M2 under E3
>   (-0.004 and -0.006), and c at one bit is +0.014 [+0.008, +0.021] above it in P2 under E3.
> - Four bits per dimension carry no registered verdict (H20a is one byte, H20b one bit). Read by the
>   same rule as a secondary, c_int4 - d_f32 has one interval entirely below -0.02: E2, M2, -0.030
>   [-0.038, -0.022]. So at 8 KiB c passes the rule under E1 and E3 (one bit, H20b), passes it under
>   E4 and fails it under E2 (four bits, secondary); at 16 KiB no interval lies entirely below -0.02.
> - Budgets: the brief names a real limit for 2, 4 and 64 KiB. Limits near 8 KiB (Google Cloud Storage,
>   custom metadata per object) and 16 KiB (Btrfs, default node size) were looked up on 4 October
>   (reports/citations_verified.md, "Added 2026-10-04").

Pre-registered in BRIEF.md (a50f2e6) before any session 20 number; outputs verbatim in
results/session20_outputs.md (5c73cbb). One automated run on the MIG pod bmao44n64ohrwp
(scripts/s20_run.sh): resumed 22:52 UTC on 2 October 2026, quant.py ran 22:53 to 23:00 for the four
encoders, and the watcher stopped the pod at 23:00:57 on the DONE marker; about $0.09. Under all four
encoders the f32 rows reproduced the a, c and d ranks of sessions 11, 14 and 15 query for query
(17,140 evaluation queries each). The float64 self-test (200 queries per encoder, every row) found no
unexplained difference; four ranks differed through near-ties within 1e-5 of the own folder's score
(E2: c_f16, d_f32, d_f16; E4: d_int4).

## Hypotheses, verbatim from BRIEF.md (session 20)
H20a (one byte per dimension): under each of E1 to E4, no paired 95 percent interval of
(c_int8 - d_f32) in recall@5 over all queries, P1, P2, M1 or M2 lies entirely below -0.02 (H15b's
rule). Dead under an encoder if any of the five does.
H20b (one bit per dimension): the same for (c_bin - d_f32). Dead under an encoder if any of the five
intervals lies entirely below -0.02.
H20c (one bit per dimension still keeps the minority modality): under each encoder, the paired
interval of (c_bin - a_f32) in recall@5 lies above zero in P1 and in P2. Dead under an encoder if
either includes zero or lies below it.
What the paper says: where H20b survives, c fits in the bytes the bin row of the bytes table gives
and still routes within 0.02 of opening every folder; where only H20a survives, the claim is one
byte per dimension at the budget its row gives; where H20c survives, one bit per dimension of c
beats one float32 vector of a on the minority files.
Secondary, reported, no kill: every row at recall@1, 5 and 10 in every cell; the cost of each format
(c_f - c_f32, a_f - a_f32, d_f - d_f32); c_f - a_f and c_f - d_f at equal precision; the lower bounds
against -0.02 (the stricter non-inferiority reading); the bytes table (mean, 95th percentile, max,
share of folders within each budget) for a, c and d; the budget table.
Expectation, written before the run, not a kill: int8 costs nothing measurable (c_int8 within 0.005
of c_f32 in every cell); one bit costs more at 768 dimensions (E4) than at 2,048 (E1), and H20b may
fail in a minority cell under a dual tower; H20c survives under all four, since c - a was 0.16 to
0.50 in the minority cells.

## Verdicts

| hypothesis | E1 (2,048 dims) | E2 (1,024) | E3 (1,536) | E4 (768) |
|---|---|---|---|---|
| H20a: c_int8 - d_f32 | survives | survives | survives | survives |
| H20b: c_bin - d_f32 | survives | dead (M2) | survives | dead (all, P1, M1) |
| H20c: c_bin - a_f32, P1 and P2 | survives | survives | survives | survives |

- H20a. No interval lies entirely below -0.02. Lowest lower bounds: E1 -0.021 (M1), E2 -0.025 (M2),
  E3 -0.013 (M1), E4 -0.024 (P2). These are c's own distance from d, not a cost of int8:
  c_int8 - c_f32 is within 0.001 of zero in every cell under every encoder, its intervals inside
  [-0.003, +0.002].
- H20b. E1: c_bin - d_f32 from -0.006 to -0.010 by cell, every lower bound above -0.02 (lowest
  -0.019, M1). E3: from +0.012 to -0.010, lowest lower bound -0.017 (M1). E2: dead in M2,
  -0.033 [-0.041, -0.025]; the other four cells hold. E4: dead over all queries,
  -0.057 [-0.062, -0.051], in P1, -0.084 [-0.101, -0.066], and in M1, -0.101 [-0.114, -0.088]; P2
  (-0.025 [-0.033, -0.016]) and M2 (-0.024 [-0.030, -0.018]) hold. Under E4 one bit costs every
  stored vector, not c in particular: d_bin - d_f32 is -0.048 [-0.053, -0.044] over all queries and
  c_bin - d_bin -0.009 [-0.014, -0.003].
- H20c. c_bin - a_f32: E1 P1 +0.255 [+0.216, +0.298], P2 +0.173 [+0.141, +0.205]; E2 +0.503
  [+0.465, +0.541], +0.341 [+0.306, +0.379]; E3 +0.207 [+0.167, +0.246], +0.172 [+0.141, +0.203];
  E4 +0.371 [+0.327, +0.409], +0.426 [+0.390, +0.464].

Against the expectation written before the run: int8 is free, as expected; one bit costs more at 768
dimensions than at 2,048 (c_bin - c_f32 over all queries: E4 -0.045, E1 -0.000), as expected; H20b
failed under both dual towers, under E2 in a majority cell (M2) rather than a minority one; H20c
survives under all four, as expected.

## Bytes (secondary)

c holds 5.20 representatives per folder on average (median 5, 95th percentile 9, at most 14); d holds
9.87 files (at most 60, the cap S11 was built with). Stored size of c per folder in bytes, mean and
largest:

| format | E1 | E2 | E3 | E4 |
|---|---|---|---|---|
| f32 | 42,594; 114,688 | 21,297; 57,344 | 31,945; 86,016 | 15,973; 43,008 |
| f16 | 21,297; 57,344 | 10,648; 28,672 | 15,973; 43,008 | 7,986; 21,504 |
| int8 | 10,648; 28,672 | 5,324; 14,336 | 7,986; 21,504 | 3,993; 10,752 |
| int4 | 5,324; 14,336 | 2,662; 7,168 | 3,993; 10,752 | 1,997; 5,376 |
| bin | 1,331; 3,584 | 666; 1,792 | 998; 2,688 | 499; 1,344 |

## Budgets (secondary)

The most precise format in which every folder's c fits, and c's recall@5 there (all, P1, P2):

| budget | E1 | E2 | E3 | E4 |
|---|---|---|---|---|
| 2 KiB | none | bin 0.675, 0.558, 0.376 | none | bin 0.648, 0.377, 0.431 |
| 4 KiB | bin 0.796, 0.676, 0.543 | bin 0.675, 0.558, 0.376 | bin 0.810, 0.743, 0.558 | bin 0.648, 0.377, 0.431 |
| 8 KiB | bin 0.796, 0.676, 0.543 | int4 0.676, 0.554, 0.379 | bin 0.810, 0.743, 0.558 | int4 0.692, 0.443, 0.441 |
| 16 KiB | int4 0.794, 0.673, 0.540 | int8 0.683, 0.554, 0.382 | int4 0.807, 0.742, 0.547 | int8 0.693, 0.447, 0.438 |
| 64 KiB | f16 0.796, 0.674, 0.539 | f32 0.683, 0.555, 0.383 | f16 0.811, 0.741, 0.544 | f32 0.693, 0.448, 0.438 |
| c_f32, for reference | 0.796, 0.674, 0.539 | 0.683, 0.555, 0.383 | 0.811, 0.741, 0.544 | 0.693, 0.448, 0.438 |
| a_f32, for reference | 0.692, 0.421, 0.370 | 0.457, 0.055, 0.035 | 0.716, 0.536, 0.386 | 0.397, 0.006, 0.005 |

int4 costs at most 0.012 in any cell (c_int4 - c_f32, E2 M2). d fits every folder at 8 KiB only under
E2 and E4 (one bit) and at 16 KiB under all four; its size grows with the folder, while c is bounded at
three representatives per modality label (eighteen at most).

## Reading

- The folder representation the paper recommends fits the metadata field Ali has in mind. At 8 KiB
  (64 kilobits) every folder's c fits under every encoder, at one bit per dimension under the two
  vision-language embedders and at four bits under the two dual towers, and its recall@5 there is
  within 0.007 of c in float32 (E2 0.676 against 0.683; E1, E3 and E4 within 0.001). At 64 KiB,
  Linux's ceiling for one extended attribute, c fits in float16 or float32 under every encoder.
- One byte per dimension is free under all four encoders. One bit per dimension is free under E1 and
  E3 and costs under the dual towers, through the format rather than through c (E4: d at one bit loses
  as much).
- At one bit per dimension c still beats one float32 mean vector on the minority files under every
  encoder, by 0.17 to 0.50: under E1, about 1.3 KB of c against 8 KB of a.
- Not shown: the time to read an extended attribute against listing and opening the files (the reason
  a folder vector is read first); any file system itself (sizes are counted, nothing was written to
  one); folders larger than S11's 60 files, where d grows and c does not.
- For the paper: one paragraph and the budget table, mainly in the SIGIR version; the abstract's
  "about five vectors per folder" can become a size in bytes.
