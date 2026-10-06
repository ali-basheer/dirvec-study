# Session 27, part A: queries written by a model as a simulated searcher

Brief: BRIEF.md, session 27 (commit d23baee, OpenTimestamps proof in ffe7758) and its amendment to 27A
(d5c1bb9, proof in 94cee6c), both committed before any of these queries was embedded or scored. Queries:
data/simq_s11.jsonl, 200 queries for 100 folders, written by six subagents (Claude Opus 5.5) that knew
nothing of the study, from the prompt data/simq_s11_prompt.txt. Outputs, verbatim:
results/session27_outputs.md (d5bba32); per-query ranks in data/s27_human_e1.npz to e4, from which
`python3 scripts/s27.py human-report` rebuilds every number. Run on the MIG pod s46ksd0pdara1o in one launch
(scripts/s27_human_run.sh), 5 October 2026, 22:41 to 22:54 UTC; the pod stopped itself.

These are not queries written by a person, and the paper reports them as queries a model wrote as a
simulated searcher, from what a person would see. The line of the outputs that reads "c-d over all human
queries" carries the label s27.py had before the amendment.

## What happened to the queries a person was to write
The tool (scripts/humanq_tool.py; sample ea7e8a7) went to Ali at 17:33 Toronto. Its first folder, F001,
holds raw numeric data files, and with every digit hidden their documents showed as rows of #; a display fix
(bac89e2) showed each hidden number as [num]. Ali judged the documents unreadable and asked for synthetic
queries at 17:49. No query was exported from the tool. While explaining the display fix, the assistant told
Ali what F001's pictures show; since he wrote no query, that description reached none.

## Gates
- The sample was rebuilt on the pod and is identical to data/humanq_sample_s11.jsonl.
- Title gate: under E1 to E4, the scorer's ranks of a, c and d equal descq.py's ranks on all 2,597 record
  titles (session 17's dumps), with no difference.
- d gate (E1): recall@5 0.720 in QI-T and 0.940 in QT-I, above 0.25 in both.

## Verdicts (E1; 95 percent creator-clustered intervals; one folder per family, so 50 families per cell)
- **H27a survives.** c minus a in QI-T is +0.140 [+0.020, +0.280] (98.33 percent: [-0.020, +0.314]).
- **H27b survives.** c minus a in QT-I is +0.420 [+0.280, +0.560] (98.33 percent: [+0.260, +0.594]).
- **H27c: not inferior.** c minus d over all 200 queries is +0.000 [-0.020, +0.020] (98.33 percent: [-0.025,
  +0.020]).
- **Track, by the registered rule: the full-paper track.** The rule reads H27a and H27b together at 95
  percent (an intersection-union test). Counted as one family of three primaries, H27a's 98.33 percent
  interval reaches below zero, and the paper says so.

## Secondaries
1. **Levels under E1 (recall@5).** Over all 200 queries a 0.675, c 0.870, d 0.870. In QT-I a 0.500, c
   0.920, d 0.940; in QI-T a 0.600, c 0.740, d 0.720.
2. **The other encoders.** c minus a in QI-T: E2 -0.020 [-0.160, +0.120], E3 +0.200 [+0.080, +0.340], E4
   +0.160 [+0.040, +0.280]. In QT-I: E2 +0.520 [+0.360, +0.680], E3 +0.400 [+0.240, +0.540], E4 +0.820
   [+0.700, +0.920]. Over all queries: E2 +0.205 [+0.125, +0.290], E3 +0.190 [+0.120, +0.260], E4 +0.440
   [+0.355, +0.520]. The picture cell shows no loss under E2; every other cell of the two primaries does.
3. **Majority cells (E1).** QI-I +0.040 [-0.060, +0.140]; QT-T +0.180 [+0.080, +0.300]. As with titles in
   session 12, a text query loses against the pooled vector in text-heavy folders too.
4. **Centering and two blind vectors (E1).** ac minus a -0.010 [-0.040, +0.020] over all queries. Two blind
   clusters lose against c on these queries: tb2c minus c -0.110 [-0.165, -0.060], tb2 minus c -0.090
   [-0.140, -0.045].
5. **Names.** The name router alone reaches 0.240 under E1. Fused with the vectors (reciprocal rank, k = 60),
   c minus a is +0.090 [+0.045, +0.135] over all queries and +0.220 [+0.100, +0.340] in QT-I.
6. **The queries.** Median eight words (four to twelve); one picture target and one document target were
   skipped as undescribable. All 200 pass the tool's checks (no digit, no copied run of five words).

## What it means for the paper
On queries a model wrote as a searcher, from what a person would see, the pooled vector loses the folder of
a described file in both registered cells under E1: most for a document in an image-heavy folder (0.42
recall@5, and 0.40 to 0.82 across the four encoders), less for a picture in a text-heavy folder (0.14, and
0.16 to 0.20 under E3 and E4, none under E2). Per-label representatives are level with searching every file
on these queries. The section reports the writer as a model and does not call these queries human; the
limitation that no person wrote queries stays.

## Deviations
1. The writer is a model, not the author (the amendment, d5c1bb9). The second-writer reading is dropped.
2. 100 of the 120 folders: the subagent for F061 to F080 was refused by an automated permission check before
   it ran and was not retried. 25 folders per bucket remain.
3. The subagents saw the tool's text heads and thumbnails rebuilt from its payload, plus one sheet of every
   picture per folder in place of the tool's grid; the table prefix "# sheet:" showed as "sheet:".
4. Two display fixes to the tool (029cb4b, bac89e2) before anyone wrote a query; the tool was not used for
   the queries scored here.

## The pre-registration: 27A and its amendment (BRIEF.md, verbatim)

> ## 27A. Queries written by a person
>
> Folders and targets (scripts/humanq_tool.py sample).
> - Possible target: an S11 evaluation query under E1 (a file with an E1 vector that build_gt.py kept as a
>   query; a file with a near-duplicate in another folder is not one) that has a vector under E2, E3 and
>   E4 as well.
> - Eligible folder: an S11 evaluation folder outside the four series with at least two possible targets
>   labelled image and at least two text-like ones.
> - Draw: numpy default_rng(270501). Per bucket, in the order [0,.2), [.8,1], [.2,.5), [.5,.8) (the two
>   scarce buckets first), a permutation of the bucket's eligible folders sorted by path, walked in order;
>   a folder is taken unless its family is already in the sample, until 30 are taken. 120 folders, at most
>   one per family, so a family holds at most one query in any cell.
> - Targets: default_rng(270502). Per folder, a random order of its image targets and one of its
>   text-like targets. The tool marks the first of each and moves to the next only when the writer marks
>   the file impossible to describe (blank, unreadable); skips are recorded. Targets are drawn, not
>   chosen, so the writer cannot pick the files a pooled vector misses.
> - Written to data/humanq_sample_s11.jsonl, with the display order (default_rng(270503)), and committed
>   before any query is written.
>
> The tool (scripts/humanq_tool.py payload and html).
> - One self-contained HTML file, no network. Folders in a fixed order that cycles through the buckets
>   [0,.2), [.2,.5), [.5,.8), [.8,1], so any first 4n folders hold n per bucket. For each folder, every
>   file with an E1 vector, in a random order: images and the first page of scanned PDFs as thumbnails
>   (longest side 320 pixels, through embed.py's load_rgb and its 100 dpi page rendering), every other file
>   as the first 300 characters of the text embed.py's prepare() extracts, with its kind (picture,
>   scanned page, text, table, PDF text, document). Hidden: file names (none is shown; the folder's names
>   are masked where a text head contains them), the record title (absent; any run of four or more of its
>   words is masked in a text head), the description (absent), the record identifier (the file holds
>   opaque keys only) and every digit (shown as #).
> - The writer writes two queries per folder: QI for the marked picture and QT for the marked document,
>   each as the words they would type into a search box to find that file again. Rules shown in the tool:
>   describe the marked file, not the folder as a whole; no digits; no file names; no run of more than
>   four consecutive words copied from what is shown. The tool refuses a query with a digit or with a
>   copied run of five words (case-insensitive, against every text shown for that folder).
> - The writer is the author, who has seen every earlier result and knows the hypotheses. The tool shows
>   no representation, score or rank. If a second person writes queries for the first 40 folders, their
>   export (data/humanq_s11_w2.jsonl) is scored the same way as a separate writer, with no verdict.
> - Export: data/humanq_s11.jsonl, one line per query (folder key, kind QI or QT, target key, query text,
>   writer, the target keys skipped before it), committed before any query is embedded.
>
> Scoring (scripts/s27.py human-embed, human-eval, human-report; driver scripts/s27_human_run.sh).
> - Each query embedded with each encoder's query text path, as descq.py embeds titles (embed.py's
>   truncate, then encode_texts with mode "query"). Representations built from all of a folder's files with
>   a vector under that encoder (no leave-one-out: the query is not a file). Every S11 folder with a vector
>   is a candidate (2,597). Rank 1 plus the number of folders scoring strictly higher.
> - Rows: a, ac, c, cc, d, dc, tb2, tb2c (eval.py's builders; the centered rows use the S11 calibration
>   means and the query centered with mu_txt, as descq.py does).
> - Cells: QI-T, QI queries on folders with image fraction below 0.5; QT-I, QT queries on folders at 0.5 or
>   more; their majority counterparts QI-I and QT-T; and all queries.
> - Intervals: creator-clustered 95 percent (1,000 resamples of families, validity.boot_mean's estimator;
>   seeds all 2700, QI-T 2701, QT-I 2702, QI-I 2703, QT-T 2704). The 98.33 percent interval of every
>   primary is printed beside it, from the same resamples.
> - Names: the name router of session 17 (char_wb 3-4-gram TF-IDF of lowercased base names without the
>   last extension, fitted on the files with a vector of the candidate folders; a folder scores the best
>   cosine of the lowercased query against its files' names) and reciprocal rank fusion (k = 60) of its
>   ranking with those of a, c and d, ties as session 26 breaks them.
> - Minimum: the cells are read only if the export holds queries for at least 80 folders. Otherwise 27A
>   has no verdict and is reported as not run.
>
> Hypotheses (E1; read on the 95 percent creator-clustered intervals).
> - Gate: d reaches recall@5 of at least 0.25 in QI-T and in QT-I (the gate of H18b). A cell that fails
>   it is read as "queries too vague", not as a verdict.
> - H27a: in QI-T, c minus a in recall@5 is at least +0.05 and its interval lies above zero. Survives if
>   both hold; dead otherwise.
> - H27b: the same in QT-I.
> - H27c: over all human queries, c minus d is not inferior if the lower bound is at or above -0.02,
>   inferior if the upper bound is below -0.02, inconclusive otherwise.
> - Multiplicity: the decision below needs H27a and H27b together, an intersection-union test (Berger
>   1982), so each is read at 95 percent without correction. The 98.33 percent intervals are reported for
>   a reader who counts the three primaries as one family.
> - Expectation, written before any query exists, not a test: the record predicts a loss in both cells
>   (session 18's descriptions of minority images +0.290, session 12's titles of image-heavy folders
>   +0.182). With 60 queries per cell at 120 folders the intervals will be several times wider than those.
>
> What decides the venue (fixed here). If H27a and H27b both survive under E1, the SIGIR version goes to
> the full-paper track with 27A as its second results section. If either dies or a gate fails, it goes to
> the reproducibility or resource track that SIGIR 2027 offers, with 27A reported as it came out.
>
> Secondary, reported without verdicts: E2, E3 and E4 on the same queries; ac minus a; tb2c minus c and
> tb2 minus c; d minus c by cell; the fused rows and fused c minus a; QI-I and QT-T; recall@1 and recall@10;
> skips and query lengths; a second writer's c minus a on the folders both wrote.
>
>
> ## Session 27, amendment to 27A before any query is scored (5 October 2026, evening)
>
> What changed. No query was written by a person. The author opened the tool, found that the documents of
> the first folder (raw numeric data files, every digit hidden) could not be read, and asked for synthetic
> queries instead (5 October, 17:49 Toronto). Nothing was exported from the tool. The queries are now written
> by a model acting as a searcher, and the paper says so: they are reported as queries a model wrote as a
> simulated searcher, never as queries written by a person.
>
> The writer (fixed now, before any of these queries is embedded or scored).
> - Model: Claude Opus 5.5 (Anthropic), as six subagents of this session's assistant, twenty folders each in
>   tool order (F001 to F020, F021 to F040, and so on). Each saw only its prompt (data/simq_s11_prompt.txt,
>   verbatim, with its folder list and paths) and its folders' material; the prompt says nothing about the
>   study, its representations, its hypotheses or any result.
> - Material per folder, built from the tool's payload: a sheet of every picture in the folder with the marked
>   picture framed; the marked pictures at the tool's size (the first four of the registered target order);
>   and a text file with the first four documents of the registered target order and every other document,
>   each as the tool showed it (digits hidden, a hidden number shown as [num]).
> - Targets and skips as registered: the first marked file of each kind unless the writer judged it
>   undescribable, then the next. The rules of the tool, checked by script on every query: no digit, no run of
>   five words copied from the folder's text. All 200 queries pass both.
> - Coverage: 100 folders, F001 to F060 and F081 to F120, two queries each (50 in each of QI-T, QT-I, QI-I,
>   QT-T). The subagent for F061 to F080 was refused by an automated permission check before it ran; it was not
>   retried. The brief's minimum of 80 folders is met and the four buckets stay balanced (25 folders each).
> - Export: data/simq_s11.jsonl, in the tool's export format, writer field "simulated searcher (Claude Opus
>   5.5, subagent n)". Committed with this amendment, before any query is embedded.
>
> Everything else in 27A stands as registered: the scoring (s27.py human-embed, human-eval, human-report on
> data/simq_s11.jsonl), the rows, cells, intervals, the title gate, the d gate, H27a to H27c, and the rule that
> decides the SIGIR track, read on these queries. What the paper may claim from them is narrower than from
> queries written by people: the loss on queries a model wrote as a searcher, from what a person would see.
> The second-writer reading is dropped.
