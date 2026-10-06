# Session 21 results: what to store in a fixed number of bytes of a folder's metadata (both sources)

Pre-registered in BRIEF.md (472acc6, OpenTimestamps proof 9c8c5e3) while the session 19 pod was in
its harvest, before any number of session 19 or 21 existed. Outputs verbatim in
results/session21_outputs.md (2601d59 for the two E1 runs, 53d3bfb for all seven). Run on the session
19 pod by scripts/s19_followup.sh, CPU only, 04:22 to 04:42 UTC on 5 October 2026, on cached
vectors. The self-test passed first (59,850 ranks against a plain implementation; 106 differences,
all near-ties of allbits at a 12-byte self-test budget). In each of the seven runs budget.py
reproduced eval.py's a and d ranks rank for rank before any new number (S19 under E1, E4, E2; S11
under E1 to E4).

At 2 KiB under E1 a folder's metadata holds eight one-bit vectors (256 bytes each) or the mean in
int8. On S19, 75.5 percent of the folders fit whole at that budget; 3,333 of the 7,372 evaluation
queries and 310 of the 581 minority queries have a folder that does not.

## Hypotheses, verbatim from BRIEF.md (session 21)
One family, three tests, under E1 on S19 at 2 KiB (S3's allowance for user metadata, half an ext4
block; under E1 eight one-bit vectors against the mean in int8), each read on its 98.33 percent
interval. All three are read on queries whose folder is not whole at 2 KiB, where what is stored is
a strict subset of the folder: a folder stored whole is every file at one bit under sample, kmeans
and usample alike, which session 20 already compared with the mean, and counting those queries
would pull the two differences between samples to zero.
- H21a, the bytes are better spent on a few coarse file vectors than on one precise mean: sample
  minus mean on the minority queries whose folder is not whole, read as session 19 reads a loss
  (confirmed if the lower bound is at least +0.05; below +0.05 if the upper bound is under it;
  present with the size open if the lower bound is above zero; inconclusive otherwise).
- H21b, the sample needs no clustering: sample minus kmeans over all queries whose folder is not
  whole. Not inferior if the lower bound is at least -0.02; inferior if the upper bound is under
  -0.02; inconclusive otherwise.
- H21c, the kinds: sample minus usample on the minority queries whose folder is not whole. The kinds
  matter if the lower bound is above zero; the uniform sample is better if the upper bound is below
  zero; no difference at the margin if the interval lies within -0.02 and +0.02; inconclusive
  otherwise.
Expectation, written before the run and not a test: H21a confirmed; H21c the kinds matter, because a
uniform sample of eight from a folder of thirty usually misses its three images; H21b open at 2 KiB,
where a sample of a large folder covers its majority worse than centroids do; fsample below sample
in small folders, where it leaves slots empty.

The policies (BRIEF.md): sample, n files at one bit dealt to the kinds present and chosen by a hash of
the file's path; usample, the n files of smallest hash, kinds ignored; kmeans, n centroids of
spherical k-means over all files at one bit; mean, the folder's mean in the best format that fits.
Session 19's owner minimum applies: a test with fewer than 100 owners is inconclusive.

## Verdicts

| test | queries | owners | point | 95% | 98.33% | reading |
|---|---:|---:|---:|---|---|---|
| H21a: sample - mean, minority, not whole | 310 | 70 | +0.269 | [+0.178, +0.365] | [+0.158, +0.384] | inconclusive (fewer than 100 owners) |
| H21b: sample - kmeans, all, not whole | 3333 | 207 | -0.042 | [-0.057, -0.029] | [-0.060, -0.026] | inferior |
| H21c: sample - usample, minority, not whole | 310 | 70 | +0.116 | [+0.064, +0.173] | [+0.054, +0.187] | inconclusive (fewer than 100 owners) |

- **H21a: inconclusive** by the owner minimum. The interval lies above +0.05 throughout.
- **H21b: inferior.** Where a folder holds more than eight files besides the query, eight k-means
  centroids at one bit route better than eight of the folder's own files at one bit, by 0.042.
- **H21c: inconclusive** by the owner minimum. The interval lies above zero throughout.
- Session 24 (BRIEF.md, registered before any session 21 number) fixes what the paper takes from
  these: for a test whose cell holds fewer than 100 owners, the pooled reading over both GitHub
  draws, with the two single-draw readings in the same table. That applies to H21a and H21c. H21b
  holds 207 owners and its reading stands; session 24's H24f is its replication on the second draw.
- Near-ties change no registered row: the rows with ties counted for and against the own folder are
  the same as the tests (results/session21_outputs.md).

## Reading
- What the bytes buy on the minority files (S19, E1, 2 KiB, owner-weighted recall@5 over the 581
  minority queries): the mean in int8 0.423; sample 0.624, kmeans 0.626, medoid 0.627, kkind 0.618,
  kindmean 0.558, usample 0.580. With no budget, c in f32 reaches 0.605, every file in f32 0.628 and
  every file at one bit 0.633. Eight one-bit vectors chosen with the kinds or the clusters in view
  (sample, kmeans, medoid, kkind) reach the level of every file in f32; one mean per kind and the
  uniform sample fall short of it.
- The registered remedy is not the best policy at this budget. On folders that do not fit, k-means
  centroids beat the sample by 0.042 over all queries. On the minority queries the two are level
  (sample - kmeans -0.014 [-0.040, +0.014]). The cost of the sample is on the majority files of large
  folders, where eight files cover the folder worse than eight centroids.
- The same signs on every source and encoder at 2 KiB, read as secondaries:

| source, encoder | sample - mean, minority not whole | sample - kmeans, all not whole | sample - usample, minority not whole |
|---|---|---|---|
| S19, E1 (owner-weighted) | +0.269 [+0.178, +0.365] | -0.042 [-0.057, -0.029] | +0.116 [+0.064, +0.173] |
| S19, E4 (owner-weighted) | +0.444 [+0.231, +0.671] | -0.032 [-0.066, -0.008] | +0.067 [+0.000, +0.167] |
| S19, E2 (owner-weighted) | +0.453 [+0.292, +0.616] | -0.033 [-0.058, -0.013] | +0.049 [-0.026, +0.133] |
| S11, E1 (query-weighted) | +0.308 [+0.266, +0.354] | -0.078 [-0.090, -0.065] | +0.107 [+0.086, +0.131] |
| S11, E4 (query-weighted) | +0.706 [+0.647, +0.756] | -0.044 [-0.053, -0.034] | +0.055 [+0.033, +0.080] |
| S11, E2 (query-weighted) | +0.704 [+0.662, +0.746] | -0.053 [-0.064, -0.043] | +0.078 [+0.059, +0.098] |
| S11, E3 (query-weighted) | +0.287 [+0.235, +0.340] | -0.059 [-0.071, -0.047] | +0.064 [+0.048, +0.083] |

  95 percent intervals; on S11 from 1,000 resamples of the cell's directories, as eval.py.
- What the paper says, by the brief's outcomes: H21b inferior, so the paper says what clustering buys
  at 2 KiB (0.03 to 0.08 of recall on the folders that do not fit) and that a summary made of the
  files' own vectors, which a directory can keep up to date without clustering, pays it. H21a and
  H21c take the pooled reading of session 24.

## After session 24 (5 October 2026)
Session 24 (results/session24.md) read the same three tests on a second GitHub draw (E1, 2 KiB) and
pooled both draws, by rules fixed before any session 21 number existed. On the second draw alone:
sample - mean on the minority queries not whole +0.252 [+0.181, +0.327] from 146 owners (confirmed),
sample - kmeans over all queries not whole -0.052 [-0.067, -0.038] from 365 owners (inferior), sample -
usample on the minority queries not whole +0.097 [+0.054, +0.145] from 146 owners (the kinds matter).
Pooled: +0.258 [+0.198, +0.321] from 216 owners, -0.048 [-0.060, -0.037] from 572, +0.103
[+0.067, +0.142] from 216 (98.33 percent intervals). Since the S19 cells of H21a and H21c hold 70
owners, the readings the paper takes for them are the pooled ones: **H21a confirmed** and **H21c the
kinds matter**. H21b is inferior on both draws and pooled.
