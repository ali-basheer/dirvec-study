# Session 18 results: written folder abstracts against per-modality representatives

> **Errata, added 2026-10-04 after the fifth blind pass of the number audit
> (reports/number_audit_2026-10-01.md). The text and tables below are unchanged; where a sentence and a
> verbatim table disagree, the table is right.**
> - "c plus the abstract is the best title row": among a, c, d, s1, s0 and s1c. Under E1 the abstract
>   written with file names ties it over all titles (sw1 0.816, s1c 0.816). Under E3 tc (0.735), td
>   (0.741) and bm25 (0.746) are above s1c (0.729). What holds under both encoders is that s1c - c is
>   above zero. (Added after the consistency read of the same day: so are the centered rows of session
>   14's title table under E3, cc 0.733 and dc 0.738, results/session14_outputs.md.)
> - "L0 is weaker than L1": on the member descriptions under both encoders and on titles under E1.
>   On titles under E3 L0 is the stronger one (s0 0.650 against s1 0.547 over all titles; s0 - c
>   -0.068, s1 - c -0.171).
> - "1,924 of the 1,959 P1 folders' L1 abstracts name images at all": 1,959 is the number of P1 query
>   images, which sit in 832 folders, and the count matched substrings (image, photo, micrograph,
>   figure, diagram, chart, graph), so that "geographic" counted. Recount of 4 October on
>   data/s18/abstracts.jsonl.gz and data/s18/members.jsonl.gz, case-insensitive, whole words, with
>   `\b(?:images?|photos?|photographs?|micrographs?|figures?|pictures?|illustrations?|diagrams?|charts?|plots?|maps?|graphs?)\b`:
>   the L1 abstracts of 809 of the 832 P1 folders (the folders of 1,930 of the 1,959 P1 images) use
>   at least one of these words.
> - "finds the folder of a described image exactly as often as the pooled vector, 0.490 each": equal
>   at three decimals. c - s1 is +0.291 and c - a +0.290, one query apart.
> - "leaves the pooled vector where it was" (the caption rows): not under E3 on P1 descriptions, where
>   ta - a is -0.045 [-0.060, -0.027].
> - (Added after the seventh pass of the same day.) "no digit in any L1 or L0" and "any name that
>   contains a digit ... drops out of captions and abstracts": true of the digits 0 to 9. The rule is
>   `\d` on whitespace tokens (scripts/s18.py), which does not match superscript or subscript digits.
>   Recount on data/s18: 159 of the 12,880 captions, 38 of the 2,597 L1 abstracts and 10 of the L0
>   abstracts keep such a token (CO₂, R², δ¹⁸O). The abstract written with the full file names (sw1) is
>   not stripped, as the brief fixes; 2,419 of the 2,597 hold a digit.
> - (Added after the seventh pass.) "The model sees no title, description, record ID or full file
>   name": none was given as a field. A title can still reach an abstract through a text head, a
>   caption or a file's name words. Recount on data/s18/abstracts.jsonl.gz against
>   data/selection_s11.jsonl, lower case, punctuation removed: the L1 abstract holds the record's
>   title word for word in 38 of the 2,146 folders whose title has five words or more, 19 of them
>   publications. The file vectors that a, c and d are built from embed the first 2,000 tokens of the
>   same extracted texts, of which a text head is the first 500.

Pre-registered in BRIEF.md (c6dba27) before any session 18 number. Outputs verbatim in
results/session18_outputs.md (fdf7c06); the generated captions, abstracts and member descriptions are in
data/s18/. Run on 2 October 2026, 15:30 to 16:38 UTC.

## Verdicts

- **H18a (titles, image-heavy folders): split.** Under E1 the abstract is level with c: s1 0.781 against
  c 0.788, s1 - c = -0.007 [-0.049, +0.038] over 1,382 queries and 813 creator families, outcome
  "between". Under E3 it falls below: s1 0.467 against c 0.729, s1 - c = -0.263 [-0.433, -0.096],
  outcome "below c". By the brief, the paper reports a split.
- **H18b (descriptions of minority images): survives under E1 and E3.** On P1 (1,959 queries, 731
  families) the gate holds (d 0.785 under E1, 0.751 under E3). Under E1 the written abstract finds the
  folder of a described image exactly as often as the pooled vector, 0.490 each, against 0.781 for c:
  c - s1 = +0.291 [+0.259, +0.322], c - a = +0.290 [+0.260, +0.324]. Under E3: s1 0.404, a 0.457, c
  0.747; c - s1 = +0.344 [+0.310, +0.380], c - a = +0.290 [+0.259, +0.322].
- The reproduction check passed: a, c and d equal descq.py rank for rank on all 2,597 title and 2,399
  description queries under both encoders.

## Secondaries

- **Majority images lose too.** On M1 (2,000 images in image-heavy folders, 492 families) the abstract
  is far below c although images are the majority: E1 s1 0.458, c 0.732, c - s1 = +0.274 [+0.239,
  +0.313]; E3 +0.300 [+0.260, +0.341]. The pooled vector loses little there (c - a +0.069 [+0.043,
  +0.100] under E1, +0.049 [+0.022, +0.080] under E3). An abstract summarizes a folder; it does not keep
  each member findable. Exploratory count, not pre-registered: 1,924 of the 1,959 P1 folders' L1
  abstracts name images at all (image, photo, micrograph, figure and the like), so the loss is not the
  abstract leaving the images out but describing them in general terms.
- **c plus the abstract is the best title row.** s1c - c on all titles: +0.025 [+0.018, +0.033] under
  E1 (0.816 against 0.792), +0.010 [+0.006, +0.016] under E3; on member queries it changes nothing (P1
  +0.001 [+0.000, +0.002] under E1, +0.001 [-0.003, +0.004] under E3).
- **One folder per family and the four series.** Under E1, s1 - c on image-heavy titles is +0.042
  [+0.020, +0.064] with one folder per family and +0.029 [+0.005, +0.055] without the four digitization
  series, and -0.096 [-0.143, -0.008] on the series (396 queries, 4 families); so outside the series the
  E1 abstract is slightly above c on titles. Under E3 it stays below outside the series (-0.100
  [-0.133, -0.067]; one folder per family -0.090 [-0.121, -0.057]). H18b does not move: one folder per
  family gives c - s1 +0.295 and c - a +0.297 under E1, +0.352 and +0.301 under E3; no P1 query is in
  the four series.
- **L0 is weaker than L1.** On titles s0 - c = -0.043 [-0.076, -0.007] under E1 and -0.068 [-0.135,
  -0.006] under E3 (all titles); on P1 descriptions c - s0 = +0.424 and +0.425.
- **File names in the abstract help a little on titles only.** sw1 - s1 on all titles +0.020 [+0.009,
  +0.032] under E1, +0.074 [+0.053, +0.097] under E3; on P1 descriptions -0.006 [-0.025, +0.014] (E1).
- **The caption rows put the loss on dilution, not on the modality gap.** Replacing every image vector
  with its caption's vector leaves the pooled vector where it was (titles: ta - a -0.005 [-0.016,
  +0.007] under E1, +0.013 [-0.011, +0.041] under E3; P1 descriptions: -0.009 [-0.020, +0.001] and
  -0.045 [-0.060, -0.027]), while per-group representatives still recover the loss inside that all-text
  space (tc - ta on titles +0.136 [+0.098, +0.187] and +0.141 [+0.105, +0.183]; on P1 +0.247 [+0.220,
  +0.277] and +0.359 [+0.325, +0.398]). This agrees with session 10 (most of the loss is count
  dilution).
- **Lexical rows.** BM25 over each folder's file names, captions and text heads reaches 0.746 on all
  titles (0.763 image-heavy): bm25 - s1 = -0.050 [-0.104, +0.018] under E1 and +0.199 [+0.106, +0.314]
  under E3. On P1 descriptions BM25 reaches 0.560; bm25 - c = -0.220 [-0.255, -0.190] under E1. File names alone reach 0.373 on titles and 0.061 on P1 descriptions (the descriptions carry no
  name tokens: 1,394 were removed from 790 of 3,959 sentences).
- **The flat walk adds little over c** on titles (d - c +0.002 [-0.003, +0.008], E1) and on P1
  (+0.005 [-0.006, +0.014]); on M1 it adds +0.035 [+0.021, +0.050].
- **Q_desc (title and description, 2,399 queries) follows Q_title.** E1: s1 0.850 and c 0.850 on all,
  s1 - c on image-heavy -0.038 [-0.098, +0.038]. E3: s1 0.665 against c 0.776 on all.
- **Generated texts.** Summarizer Qwen3-VL-8B-Instruct (revision 0c351dd), describer Pixtral-12B
  (mistral-community/pixtral-12b, revision c2756cb), both under vLLM 0.11.0, both passed the smoke test
  first. L1 median 1,532 characters (max 3,690), L0 median 217, with names 1,679; no digit in any L1 or
  L0; no empty text. A side effect of the digit rule worth stating in the paper: any name that contains a
  digit (marker names, formulas, sample codes) drops out of captions and abstracts.

## What it means for the paper (to write when the study wraps up)

The reviewers' objection that the cited systems route on written abstracts, not on a mean of file
vectors, is now answered with that design made strong (an abstract asked to cover every kind of file,
written from a caption of every image): it loses a described member image as badly as the pooled
vector (0.490 against 0.781 for c under E1), and loses majority images as well. On whole-folder title
queries the abstract matches c under E1 and falls below it under E3, and c with the abstract added is
the best title row under both. The recommendation becomes: keep per-modality representatives; a written
abstract is a useful extra vector for folder-level text queries, not a replacement. The caption rows
belong next to the session 10 dilution control.

## Run notes

- Pre-registration c6dba27. First attempt on a full RTX PRO 6000 (pod 4r4ybj7jrhuabc): the pod image
  points UV_CACHE_DIR, PIP_CACHE_DIR and HF_HOME at /workspace, and the vLLM install filled the volume
  quota (9.7 GB of uv cache) before any model ran; the watcher stopped the pod at the FAILED marker.
  The cache was removed from a MIG pod and the driver now keeps every cache on the container disk
  (074ac14).
- No full RTX PRO 6000 was free in US-NE-1 afterwards; the run went to an H100 SXM 80 GB pod
  (70edpmti03won7, $3.49/h, 26 vCPUs). Describer 15:33 to 15:44, text heads 473 s in parallel,
  captions and abstracts 15:45 to 16:17, E1 and E3 embeddings 16:17 to 16:24.
- The first evaluation read the vectors out of the .npz inside per-item loops (an NpzFile rereads the
  whole array on every access); it was stopped after 10 minutes, before any number was printed, fixed
  (66698b7) and rerun from the evaluation step (S18_FROM=eval).
- Cost about $4.15 (H100 about $3.95, the failed first attempt about $0.13, the MIG pod about $0.04).
  RunPod balance $13.28 at 16:41 UTC; all pods EXITED.

## The pre-registration (BRIEF.md, verbatim)

> # dirvec, session 18: written folder abstracts against per-modality representatives
>
> Why this session exists. Session 17's decision rule (H17a, H17b and H17c all held) makes session 18 the
> judges' modified Proposal 3. The SIGIR reviewers' likely sinker is that the cited directory systems do
> not route on a mean of file vectors: builders ship a model-written abstract per folder (OpenViking's
> L0 and L1, LlamaIndex, RAPTOR). This session puts such an abstract against a, c and d, on queries that
> are not files: the record titles (and title plus description), and one-sentence descriptions of single
> member images written by a model from another family, with the image kept in its folder. Ali asked for
> the run on 2 October, 10:55 Toronto ("run session 18"). No session 18 number has been computed.
>
> ## Definitions (fixed now)
> - Set: S11 (2,597 folders, 25,990 files; E1 ok set 25,637). Every folder with an embedded file is a
>   candidate; folder representations use all of its embedded files (no leave-one-out), as descq.py.
> - Encoders: E1 and E3 (primaries), each with its own ok set and its S11 cache. Texts go through the
>   encoder's text path with mode "query" (the mode the S11 caches used for every text input; E3 has
>   one text path).
> - Generated texts (scripts/s18.py, prompts verbatim in the script; greedy decoding, seed 18, vLLM):
>   - Captions: every image and the first page (100 dpi) of every scanned PDF embedded under E1, by the
>     summarizer, from the load_rgb image cut to at most 602,112 pixels; two to four sentences.
>   - Text heads: the first 500 tokens (E1's Qwen2.5 tokenizer) of the text embed.py's prepare()
>     extracts, for every text-like file embedded under E1.
>   - L1 (primary abstract): one per folder from all its embedded files in manifest order (60 at most in
>     S11), each given as its kind, its name words (letter runs of the base name without the extension,
>     two letters or more; digits and separators split them) and its caption or text head. The model sees
>     no title, description, record ID or full file name. The prompt asks for at most 4,000 characters
>     of plain prose that covers every kind of file, images as well as documents, with no digits, codes,
>     identifiers or file names. L0: one sentence of at most 256 characters written from L1.
>   - With-names L1 (sw1, secondary): the same prompt with the full file names, names allowed.
>   - Post-processing: markdown marks removed, whitespace collapsed; in captions, L1 and L0 every token
>     containing a digit is removed; L1 and sw1 cut to 4,000 characters at the last sentence end past
>     2,000 characters (else at a space), L0 to 256 at a space.
>   - Summarizer: Qwen/Qwen3-VL-8B-Instruct; Qwen/Qwen2.5-VL-7B-Instruct if the first fails the smoke
>     test (10 images, every caption at least 10 characters). Revision recorded at download.
>   - Member descriptions: one sentence per image ("the way someone searching for it would describe
>     it", no digits, codes, identifiers or file names) by a model outside the Qwen family, the first of
>     mistral-community/pixtral-12b, HuggingFaceM4/Idefics3-8B-Llama3, llava-hf/llava-v1.6-mistral-7b-hf
>     that passes the same smoke test. Tokens with a digit and tokens equal to one of the image's own
>     name words (three letters or more) are removed. Images: every S11 evaluation query of cell P1
>     under E1 (image in a folder with image_frac below 0.5; 1,959) and 2,000 of cell M1 (image in a
>     folder with image_frac 0.5 or more), drawn without replacement with numpy default_rng(20261018).
>   - A model is replaced only before it has written anything; vLLM 0.11.0 first, the latest vLLM if no
>     describer passes under it.
> - Query sets: Q_title (2,597 record titles, the descq_s12.npz vectors), Q_desc (title and description,
>   secondary), Q_mem (the member descriptions; relevant folder: the image's own, which keeps the image).
> - Rows (recall@k of the relevant folder, rank 1 + the folders scoring strictly higher):
>   a, c, d as descq.py (uncentered); s1, s0, sw1: one vector, the abstract's embedding; s1c: c's
>   representatives plus s1; ta, tc, td: a, c, d with every image-input vector replaced by its caption's
>   embedding (a file without a caption keeps its vector); bm25: Okapi BM25 (k1 1.2, b 0.75, lowercased
>   word tokens, unique query terms) over each folder's full file names, captions and text heads, the
>   lexical ceiling on the abstract's evidence; fn: char_wb 3-4-gram TF-IDF of base names, the folder's
>   max cosine (validity.py's title mode). In bm25 and fn a relevant folder that scores zero is a miss.
> - Cells: Q_title and Q_desc: all, text-heavy (image_frac below 0.5), image-heavy (0.5 or more);
>   Q_mem: P1, M1.
> - Intervals: creator-clustered (validity.boot_mean: 1,000 resamples of first-creator families,
>   query-weighted), seeds: Q_title 1801 all, 1802 text-heavy, 1803 image-heavy; Q_desc 1811 to 1813;
>   Q_mem P1 1850, M1 1856. Secondary subsets: one folder per family (drawn with default_rng(20261019)),
>   the four digitization series of session 17 apart.
> - Reproduction check: the a, c and d ranks on Q_title and Q_desc must equal the descq.py ranks dumped
>   in session 17 (/workspace/logs/s17/descq_ranks_e1.jsonl, _e3.jsonl) for every query; otherwise the
>   run stops before any new number.
>
> ## Hypotheses (fixed now, do not edit after the first evaluation)
> H18a (titles, image-heavy folders: written abstract against per-modality representatives): under E1
> and under E3, s1 - c in recall@5 on Q_title, image-heavy cell, with its clustered interval. Three
> outcomes fixed in advance, per encoder: "above c" (s1 - c at least +0.05 and the interval above zero),
> "below c" (at most -0.05 and the interval below zero), "between" (otherwise). What the paper says:
> above c, a written abstract beats per-modality vectors for whole-folder text search and c's claim is
> confined to member-level queries; below c, c beats the builders' abstract on titles as well; between,
> no difference of practical size on titles. If E1 and E3 disagree the paper reports a split.
> H18b (member descriptions of minority images): under E1 and under E3, on Q_mem cell P1, gated on d
> reaching recall@5 0.25 (below the gate the descriptions do not find their own image and H18b is not
> testable under that encoder). It survives under an encoder if both c - s1 and c - a are at least
> +0.05 with clustered intervals above zero; dead if either fails. The paper keeps "a written abstract
> loses the minority image as the pooled vector does" only if it survives under both.
> Secondary, reported, no kill: every row in every cell at recall@1, 5 and 10; s0 and sw1 against s1;
> s1c against c and s1; d - c; the caption rows (ta - a: what removing the modality gap recovers; tc -
> ta: what is left for dilution; tc - c, td - d); bm25 and fn against s1 (Q_title) and c (Q_mem); M1 as
> the majority control; Q_desc; the one-folder-per-family subsample and the four series.
> Expectation, written before the run, not a kill: on titles s1 is at least level with c (a written
> abstract is text and so is the title), likely "above c" under E1; on P1 descriptions c - a holds as
> in every leave-one-out run and c - s1 is positive but smaller, because an abstract of a text-heavy
> folder will often not mention a minority image.
>
> ## Steps, in order
> 1. Commit this brief, scripts/s18.py and scripts/s18_run.sh before anything runs. s18.py passed a CPU
>    test on a synthetic tree with stand-ins for the models (every subcommand; the reproduction check
>    catches a changed rank; its a, c and d equal descq.py rank for rank on that tree).
> 2. Check the RunPod balance and the Claude limits (15:03 UTC: $17.42; weekly 90 percent, resets
>    4 October 06:00 UTC). Resume a full RTX PRO 6000 pod with the volume (87euwc629ejvph, 50 GB
>    container disk; else 3m5g5g80psfwnm, 40 GB). Run setup_pod.sh; start the watcher with a deadline
>    4.5 hours after the resume and the markers /workspace/logs/s18/DONE and FAILED.
> 3. git pull, then bash scripts/s18_run.sh as a background job: text heads in the background; vLLM
>    venv; member descriptions (the describer's smoke test is the vLLM check on this card); captions
>    and abstracts; E1 and E3 embeddings; eval under E1 and E3; outputs (results/session18_outputs.md
>    and the generated texts in data/s18/) committed and pushed; DONE.
> 4. Confirm the pod stopped. results/session18.md (this block verbatim, the verdicts, the secondaries),
>    NOTES.md, each as its own commit.
>
> ## Inputs and budget
> - On the volume: the S11 corpus, the E1 and E3 caches with descq_s12.npz, the E1 ranks file, the
>   session 17 descq rank dumps, the E1 venv and weights. New on the container disk: a vLLM venv, the
>   summarizer and describer weights (deleted after each stage), E3's weights. Expected 2.5 to 3 hours
>   at $2.09/h, $6 to $7; the watcher caps it at 4.5 hours ($9.41).
>
> ## Rules
> - One commit per deliverable. No em dashes in anything written.
> - Nothing is chosen on the evaluation queries; models, prompts, seeds and thresholds are fixed above.
> - If the reproduction check fails, stop: FAILED, no verdicts.
