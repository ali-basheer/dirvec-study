# dirvec session 11: the two-vector result on fresh folders, with a second encoder

> **Errata, added 2026-10-01 after the number audit (reports/number_audit_2026-10-01.md). The text and
> tables below are unchanged; where a sentence and a verbatim table disagree, the table is right.**
> - Summary table, "dc - d, all": the E1 value is +0.015 [+0.012, +0.017] in the verbatim table, not
>   +0.014.
> - "three intervals lie entirely below -0.02" for tb2c - c under E2: four of the five do (all
>   queries, P1, P2, M2).
> - c "match[es] the flat walk d within 0.02 in every cell": true of the five cells all, P1, P2, M1,
>   M2 (largest d - c +0.012 under E1, +0.018 under E2). Single-bucket cells reach +0.029 and +0.030
>   under E1 (image [0,.2), text-like [.8,1]) and +0.023 under E2 (text-like [0,.2)).
> - "purity drops to 0.89 under both encoders" after centering: the tables print 0.885 (E1) and 0.895
>   (E2).
> - "the centered flat walk dc is the best row everywhere": under E2 cc is above dc in P1 (0.575
>   against 0.570) and P2 (0.404 against 0.401).


Question: does the session 9 result hold on folders that took part in no selection, and under an
encoder from a different family? Session 9 found, post hoc on the session 5 evaluation split, that
no single vector in the encoder's space matches the per-modality k-reps c and that two blind
centered clusters per folder (tb2c, 2.00 vectors) come within 0.013 recall@5 of c in every cell.
This session is the pre-registered test of both parts: a fresh Zenodo corpus (part A, NOTES.md
"session 11 part A done") embedded with the study's encoder E1 (jina-embeddings-v4, a Qwen2.5-VL
embedder) and with E2 (jina-clip-v2, a CLIP-family dual tower), the evaluation split scored once per
encoder, nothing chosen. E3 (gme-Qwen2-VL-2B-Instruct) was not run (NOTES.md session 11).

Part B ran on a full RTX PRO 6000 (96 GB, 13.6 vCPUs by cgroup); `DIRVEC_THREADS`,
`OMP_NUM_THREADS` and `OPENBLAS_NUM_THREADS` 13; numpy 2.5.2, scikit-learn 1.9.1, torch 2.8.0+cu128,
transformers 4.52.4.

## Hypotheses (fixed now, do not edit after the first eval run on the new corpus), copied verbatim from BRIEF.md

H11a (two blind centered clusters match c, fresh folders): on the new corpus under E1, tb2c is within
0.02 recall@5 of c over all queries and in each of P1, P2, M1, M2. Kill: H11a is dead if in any of
the five cells the paired interval of (tb2c - c) lies entirely below -0.02.
H11b (the finding is not the encoder): under E2, the pooled centroid a loses to c in both primary
cells (c - a interval above zero in P1 and P2, as in session 3), and tb2c is within 0.02 of c by the
H11a rule. Kill: H11b is dead if either part fails under E2.
Secondary, reported, no kill: the same rows under E3 if run; c - a, cc - c, dc - d, bc2 - c in every
cell per encoder; the modality gap and the same-folder cosines per encoder before and after
centering; purity of the blind two-cluster split per encoder; vectors per folder; the session 10
counts of single-group directories in the new corpus (whether a larger dilution control becomes
possible).

## Corpus, caches and queries

- Corpus (part A, commits cdf9050, 04277b5, ed04d2d): 2,597 Zenodo records from a new pool snapshot
  (pages 21 to 40 per year), none in any earlier selection; 25,990 files, 28.5 GB; files per
  directory median 7, mean 10.0; directories per bucket [0,.2) 420, [.2,.5) 795, [.5,.8) 978,
  [.8,1] 404. Ground truth: 21,553 leave-one-out queries over 2,544 qualifying directories.
- Calibration split: 20 percent of the directories (520), seed 20261102, stratified by bucket; its
  files give the group means mu_img and mu_txt per encoder and nothing else. Evaluation split: the
  other 2,077 directories. All 2,597 directories are ranking candidates.
- E1 cache `data/emb/jina-embeddings-v4_s11/` (revision 853c867b, the session 5 input rules): 25,637
  of 25,990 files embedded. Skipped: 333 files of modality other with no encoder path (tif, pptx,
  doc, no extension, ...), 15 images (under 28 px or wrong mode), 4 tables xlrd could not read,
  1 empty text. The first E1 run crashed at file 25,000 on a scanned PDF whose rendered page was
  5 by 6 px; embed.py now skips rendered pages the processor refuses (commit b5f2f4a) and the run
  was resumed from its checkpoint; the resumed 997 files include every pdf_scanned file (346 ok).
- E2 cache `data/emb/jina-clip-v2_s11/` (revision e10d47f5, the same prepare() inputs, texts cut to
  2000 tokens of E1's tokenizer, E2's shipped image preprocessing): the same 25,637 files ok.
- Evaluation: 17,140 evaluation-split queries over 2,035 directories per encoder (328 queries
  dropped for lack of a vector, 310 of them modality other; 4,085 calibration queries unused).
  Vectors per folder: a and ac 1.00, bc2 1.95, tb2 and tb2c 2.00, c and cc 5.20, d and dc 9.87.
- E2 pilot (part A, 20 calibration directories, text to own-directory image rank among 159 images):
  median 51 against random 80, E1 26 on the same files. A weak pass under the brief's rule.

## Verdicts

Cells: all (17,140 queries, 2,035 directories), P1 image queries in [0,.2)+[.2,.5) (1,959 queries,
832 directories), P2 text-like queries in [.5,.8)+[.8,1] (2,146, 1,044), M1 image queries in
[.5,.8)+[.8,1] (5,571, 937), M2 text-like queries in [0,.2)+[.2,.5) (7,272, 948). Recall@5, paired
95 percent bootstrap intervals over directories, 1000 resamples.

**H11a survives, by the kill rule and by little.** Under E1, tb2c - c is -0.015 [-0.022, -0.007]
over all queries, -0.037 [-0.058, -0.014] in P1, +0.036 [+0.018, +0.053] in P2, -0.005 [-0.016,
+0.004] in M1 and -0.032 [-0.046, -0.019] in M2. No interval lies entirely below -0.02, so the kill
does not fire; but the point estimates in P1 and M2 are outside the 0.02 margin and the M2 upper
bound clears it by 0.001. Read plainly: on fresh folders two blind centered clusters recover most of
what c recovers, not all of it. Against the pooled centroid, a - c is -0.253 in P1 and -0.064 in M2,
so tb2c closes 85 percent of the P1 gap and half of the M2 gap, and beats c in P2. At recall@10 the
rows are tb2c 0.827 and c 0.828 over all queries (P1 0.704 against 0.717, M2 0.900 against 0.917).
The session 9 numbers (within 0.013 everywhere) were the optimistic end of what this representation
does.

**H11b is dead, on its second clause.** Its first clause holds, and strongly: under E2 the pooled
centroid loses the minority modality far more than under E1. c - a is +0.500 [+0.462, +0.538] in P1
and +0.348 [+0.312, +0.386] in P2; a's recall@5 on the minority cells is 0.055 and 0.035 (recall@1
0.032 and 0.017), against c's 0.555 and 0.383. The second clause fails: tb2c - c under E2 is -0.049
[-0.058, -0.039] over all queries, -0.105 [-0.130, -0.080] in P1, -0.052 [-0.076, -0.029] in P2,
-0.008 [-0.019, +0.004] in M1 and -0.063 [-0.078, -0.049] in M2; three intervals lie entirely below
-0.02. Two vectors per folder are not enough under a CLIP-family encoder.

**What holds under both encoders (secondary).**

| quantity, recall@5 | E1 jina-embeddings-v4 | E2 jina-clip-v2 |
|---|---|---|
| c - a, P1 | +0.253 [+0.214, +0.294] | +0.500 [+0.462, +0.538] |
| c - a, P2 | +0.169 [+0.136, +0.200] | +0.348 [+0.312, +0.386] |
| c - a, M1 and M2 | +0.080, +0.064 | +0.146, +0.176 |
| ac - c, P1 and P2 (centering alone) | -0.161, -0.065 | -0.277, -0.154 |
| c - d, all / P1 / P2 | -0.008 / -0.010 / -0.012 | -0.011 / +0.001 / +0.000 |
| cc - c, all / P1 / P2 | +0.014 / +0.039 / +0.051 | +0.010 / +0.020 / +0.021 |
| dc - d, all | +0.014 | +0.012 |
| bc2 - c, P1 / P2 / M1 / M2 | -0.004 / +0.052 / -0.037 / -0.049 | -0.017 / +0.007 / -0.052 / -0.112 |
| tb2c - c, P1 / P2 / M1 / M2 | -0.037 / +0.036 / -0.005 / -0.032 | -0.105 / -0.052 / -0.008 / -0.063 |
| modality gap, uncentered / centered | 0.381 / 0.080 | 0.787 / 0.092 |
| same-folder cosine img-txt, uncentered / centered | 0.518 / 0.193 | 0.196 / 0.096 |
| same-folder cosine img-img, txt-txt (uncentered) | 0.776, 0.725 | 0.751, 0.701 |
| purity of the blind two-cluster split, tb2 / tb2c | 0.918 / 0.885 | 0.982 / 0.895 |

- The finding itself is not the encoder. One pooled vector loses the minority modality of a folder
  under both encoders, and the loss scales with the modality gap: 0.25 and 0.17 recall@5 in the
  primary cells under the VLM embedder (gap 0.38), 0.50 and 0.35 under the CLIP dual tower (gap
  0.79, same-folder image-text cosine 0.20 against 0.70 to 0.75 within a modality). Centering alone
  (ac, the GR-CLIP fix before pooling) recovers between a third and two thirds of it under both.
- The per-modality k-reps c (5.20 vectors) match the flat walk d within 0.02 in every cell under
  both encoders, and centered cc beats d in the primary cells under both. The remedy is robust; its
  minimal budget is not.
- How many vectors, and found how, depends on the encoder. Under E1 two blind centered clusters
  reach within 0.04 of c; under E2 they fall 0.05 to 0.10 short in P1, P2 and M2. The labelled pair
  bc2 (one centered centroid per input group) keeps the minority under both encoders (P1 -0.004 and
  -0.017, P2 +0.052 and +0.007) but loses the majority text queries (M2 -0.049 and -0.112): one
  centroid per modality is too coarse for the majority side, and k-means within the modality (c's
  k = 3 per label) is what keeps it. Blind clustering finds the modality partition in both spaces
  (purity 0.92 and 0.98 uncentered), so the shortfall of tb2c under E2 is not a failure to find the
  modalities; after centering, purity drops to 0.89 under both encoders and under E2 the minority
  cluster is lost in enough folders to cost 0.10 in P1.
- The session 10 counts: on the E1 cache, 101 single-group evaluation-split directories (37 image,
  64 text), 43 with at least 6 embedded files (18 image, 25 text), against 42 (18, 24) counted on the
  manifest in part A and 31 in the session 5 set. A larger same-modality dilution control is not
  available in this corpus either; it needs a corpus selected for single-type folders.
- The session 3 and 9 pattern repeats with the usual caveats: the flat walk d is never beaten by a
  compact row in the uncentered space, and the centered flat walk dc is the best row everywhere.

**What this changes in the paper's claim.** The claim that survives every corpus of the study and both
encoder families is the diagnosis and the per-modality remedy: a pooled folder vector loses whichever
modality is the folder's minority, the loss grows with the encoder's modality gap, centering alone
does not fix it, and a handful of per-modality representatives (about five per folder, half the
files) recovers the flat walk. The compact version of the remedy, two vectors per folder, is an
E1 result: pre-registered and surviving on fresh folders by the margin rule, but 0.03 to 0.04 short
of c in two cells, and failing under the CLIP-family encoder. The paper should present two vectors
as the lower bound the VLM embedder allows, not as the general fix.

## Output, E1 jina-embeddings-v4 (`/workspace/logs/s11b/eval_e1.md`, verbatim)

Model: jina-embeddings-v4. Queries: 17140 over 2035 directories; 2597 directories ranked (random recall@k = k/2597). Queries dropped for lack of a vector: 328 {'other': 310, 'image': 13, 'text': 1, 'table': 4}. Queries in calibration directories, not used: 4085.

Mean representative vectors per directory: a 1.00, ac 1.00, c 5.20, cc 5.20, d 9.87, dc 9.87, bc2 1.95, tb2 2.00, tb2c 2.00.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 17140 | 2035 | a | 0.584 | 0.663 | 0.692 | 0.739 | [0.676, 0.706] |
| all | 17140 | 2035 | ac | 0.608 | 0.688 | 0.719 | 0.765 | [0.704, 0.733] |
| all | 17140 | 2035 | c | 0.703 | 0.772 | 0.796 | 0.828 | [0.784, 0.806] |
| all | 17140 | 2035 | cc | 0.713 | 0.783 | 0.810 | 0.844 | [0.799, 0.820] |
| all | 17140 | 2035 | d | 0.715 | 0.781 | 0.804 | 0.833 | [0.792, 0.814] |
| all | 17140 | 2035 | dc | 0.728 | 0.795 | 0.818 | 0.850 | [0.807, 0.828] |
| all | 17140 | 2035 | bc2 | 0.657 | 0.735 | 0.769 | 0.815 | [0.756, 0.780] |
| all | 17140 | 2035 | tb2 | 0.659 | 0.736 | 0.768 | 0.809 | [0.756, 0.779] |
| all | 17140 | 2035 | tb2c | 0.672 | 0.751 | 0.781 | 0.827 | [0.769, 0.792] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 4255 | 332 | a | 0.733 | 0.797 | 0.817 | 0.859 | [0.795, 0.839] |
| [0,.2) | 4255 | 332 | ac | 0.733 | 0.800 | 0.822 | 0.864 | [0.798, 0.846] |
| [0,.2) | 4255 | 332 | c | 0.815 | 0.866 | 0.883 | 0.904 | [0.867, 0.896] |
| [0,.2) | 4255 | 332 | cc | 0.816 | 0.867 | 0.888 | 0.911 | [0.872, 0.901] |
| [0,.2) | 4255 | 332 | d | 0.824 | 0.872 | 0.886 | 0.905 | [0.869, 0.900] |
| [0,.2) | 4255 | 332 | dc | 0.833 | 0.881 | 0.895 | 0.918 | [0.880, 0.909] |
| [0,.2) | 4255 | 332 | bc2 | 0.744 | 0.803 | 0.829 | 0.876 | [0.805, 0.852] |
| [0,.2) | 4255 | 332 | tb2 | 0.760 | 0.815 | 0.839 | 0.881 | [0.817, 0.861] |
| [0,.2) | 4255 | 332 | tb2c | 0.770 | 0.825 | 0.847 | 0.890 | [0.824, 0.869] |
| [.2,.5) | 5112 | 626 | a | 0.568 | 0.649 | 0.682 | 0.734 | [0.654, 0.707] |
| [.2,.5) | 5112 | 626 | ac | 0.600 | 0.689 | 0.721 | 0.767 | [0.695, 0.745] |
| [.2,.5) | 5112 | 626 | c | 0.724 | 0.792 | 0.818 | 0.850 | [0.800, 0.835] |
| [.2,.5) | 5112 | 626 | cc | 0.739 | 0.808 | 0.835 | 0.871 | [0.818, 0.851] |
| [.2,.5) | 5112 | 626 | d | 0.734 | 0.799 | 0.824 | 0.856 | [0.806, 0.841] |
| [.2,.5) | 5112 | 626 | dc | 0.746 | 0.813 | 0.838 | 0.873 | [0.821, 0.853] |
| [.2,.5) | 5112 | 626 | bc2 | 0.674 | 0.754 | 0.790 | 0.830 | [0.768, 0.808] |
| [.2,.5) | 5112 | 626 | tb2 | 0.662 | 0.744 | 0.774 | 0.817 | [0.753, 0.794] |
| [.2,.5) | 5112 | 626 | tb2c | 0.673 | 0.757 | 0.787 | 0.833 | [0.764, 0.806] |
| [.5,.8) | 4567 | 761 | a | 0.400 | 0.483 | 0.517 | 0.567 | [0.482, 0.551] |
| [.5,.8) | 4567 | 761 | ac | 0.446 | 0.529 | 0.566 | 0.625 | [0.532, 0.598] |
| [.5,.8) | 4567 | 761 | c | 0.532 | 0.618 | 0.647 | 0.691 | [0.617, 0.676] |
| [.5,.8) | 4567 | 761 | cc | 0.550 | 0.637 | 0.668 | 0.713 | [0.638, 0.698] |
| [.5,.8) | 4567 | 761 | d | 0.550 | 0.631 | 0.661 | 0.698 | [0.630, 0.691] |
| [.5,.8) | 4567 | 761 | dc | 0.566 | 0.649 | 0.680 | 0.718 | [0.650, 0.708] |
| [.5,.8) | 4567 | 761 | bc2 | 0.542 | 0.630 | 0.670 | 0.727 | [0.643, 0.695] |
| [.5,.8) | 4567 | 761 | tb2 | 0.515 | 0.604 | 0.642 | 0.690 | [0.612, 0.670] |
| [.5,.8) | 4567 | 761 | tb2c | 0.533 | 0.623 | 0.659 | 0.719 | [0.631, 0.686] |
| [.8,1] | 3206 | 316 | a | 0.673 | 0.761 | 0.790 | 0.830 | [0.762, 0.818] |
| [.8,1] | 3206 | 316 | ac | 0.684 | 0.767 | 0.799 | 0.831 | [0.767, 0.830] |
| [.8,1] | 3206 | 316 | c | 0.764 | 0.837 | 0.858 | 0.884 | [0.839, 0.875] |
| [.8,1] | 3206 | 316 | cc | 0.769 | 0.841 | 0.870 | 0.901 | [0.851, 0.885] |
| [.8,1] | 3206 | 316 | d | 0.777 | 0.844 | 0.867 | 0.893 | [0.848, 0.883] |
| [.8,1] | 3206 | 316 | dc | 0.791 | 0.858 | 0.883 | 0.910 | [0.865, 0.898] |
| [.8,1] | 3206 | 316 | bc2 | 0.679 | 0.764 | 0.794 | 0.835 | [0.762, 0.826] |
| [.8,1] | 3206 | 316 | tb2 | 0.723 | 0.809 | 0.842 | 0.871 | [0.824, 0.860] |
| [.8,1] | 3206 | 316 | tb2c | 0.740 | 0.825 | 0.857 | 0.886 | [0.838, 0.874] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 7530 | 1769 | a | 0.529 | 0.615 | 0.650 | 0.698 | [0.625, 0.672] |
| image | 7530 | 1769 | ac | 0.556 | 0.641 | 0.677 | 0.725 | [0.653, 0.700] |
| image | 7530 | 1769 | c | 0.664 | 0.747 | 0.775 | 0.814 | [0.756, 0.792] |
| image | 7530 | 1769 | cc | 0.674 | 0.757 | 0.788 | 0.829 | [0.770, 0.803] |
| image | 7530 | 1769 | d | 0.680 | 0.758 | 0.786 | 0.822 | [0.768, 0.803] |
| image | 7530 | 1769 | dc | 0.692 | 0.771 | 0.798 | 0.836 | [0.781, 0.814] |
| image | 7530 | 1769 | bc2 | 0.622 | 0.709 | 0.746 | 0.797 | [0.726, 0.765] |
| image | 7530 | 1769 | tb2 | 0.627 | 0.714 | 0.752 | 0.794 | [0.733, 0.770] |
| image | 7530 | 1769 | tb2c | 0.636 | 0.727 | 0.761 | 0.810 | [0.742, 0.779] |
| pdf_text | 1603 | 639 | a | 0.717 | 0.800 | 0.820 | 0.857 | [0.789, 0.847] |
| pdf_text | 1603 | 639 | ac | 0.742 | 0.823 | 0.849 | 0.889 | [0.818, 0.874] |
| pdf_text | 1603 | 639 | c | 0.782 | 0.840 | 0.857 | 0.882 | [0.830, 0.878] |
| pdf_text | 1603 | 639 | cc | 0.785 | 0.848 | 0.870 | 0.906 | [0.846, 0.891] |
| pdf_text | 1603 | 639 | d | 0.782 | 0.841 | 0.860 | 0.884 | [0.834, 0.882] |
| pdf_text | 1603 | 639 | dc | 0.790 | 0.850 | 0.871 | 0.904 | [0.846, 0.893] |
| pdf_text | 1603 | 639 | bc2 | 0.749 | 0.836 | 0.862 | 0.893 | [0.835, 0.885] |
| pdf_text | 1603 | 639 | tb2 | 0.760 | 0.827 | 0.847 | 0.882 | [0.819, 0.868] |
| pdf_text | 1603 | 639 | tb2c | 0.771 | 0.835 | 0.857 | 0.897 | [0.829, 0.879] |
| text | 3348 | 1085 | a | 0.566 | 0.629 | 0.653 | 0.692 | [0.618, 0.685] |
| text | 3348 | 1085 | ac | 0.581 | 0.651 | 0.677 | 0.716 | [0.645, 0.709] |
| text | 3348 | 1085 | c | 0.666 | 0.719 | 0.740 | 0.764 | [0.712, 0.766] |
| text | 3348 | 1085 | cc | 0.678 | 0.733 | 0.757 | 0.783 | [0.730, 0.782] |
| text | 3348 | 1085 | d | 0.675 | 0.725 | 0.747 | 0.768 | [0.719, 0.773] |
| text | 3348 | 1085 | dc | 0.685 | 0.738 | 0.760 | 0.786 | [0.733, 0.785] |
| text | 3348 | 1085 | bc2 | 0.617 | 0.688 | 0.720 | 0.763 | [0.691, 0.748] |
| text | 3348 | 1085 | tb2 | 0.615 | 0.680 | 0.713 | 0.752 | [0.684, 0.740] |
| text | 3348 | 1085 | tb2c | 0.636 | 0.703 | 0.733 | 0.771 | [0.704, 0.760] |
| table | 3890 | 837 | a | 0.642 | 0.715 | 0.740 | 0.794 | [0.708, 0.770] |
| table | 3890 | 837 | ac | 0.666 | 0.743 | 0.768 | 0.821 | [0.736, 0.796] |
| table | 3890 | 837 | c | 0.773 | 0.836 | 0.855 | 0.879 | [0.836, 0.871] |
| table | 3890 | 837 | cc | 0.787 | 0.847 | 0.869 | 0.896 | [0.852, 0.885] |
| table | 3890 | 837 | d | 0.791 | 0.847 | 0.861 | 0.884 | [0.844, 0.878] |
| table | 3890 | 837 | dc | 0.807 | 0.862 | 0.881 | 0.902 | [0.865, 0.897] |
| table | 3890 | 837 | bc2 | 0.719 | 0.777 | 0.806 | 0.855 | [0.778, 0.829] |
| table | 3890 | 837 | tb2 | 0.716 | 0.783 | 0.806 | 0.851 | [0.780, 0.830] |
| table | 3890 | 837 | tb2c | 0.728 | 0.796 | 0.820 | 0.870 | [0.794, 0.843] |
| other | 577 | 288 | a | 0.667 | 0.747 | 0.785 | 0.828 | [0.737, 0.825] |
| other | 577 | 288 | ac | 0.685 | 0.775 | 0.820 | 0.861 | [0.774, 0.861] |
| other | 577 | 288 | c | 0.724 | 0.797 | 0.835 | 0.865 | [0.796, 0.868] |
| other | 577 | 288 | cc | 0.747 | 0.823 | 0.856 | 0.894 | [0.818, 0.889] |
| other | 577 | 288 | d | 0.718 | 0.794 | 0.825 | 0.867 | [0.787, 0.858] |
| other | 577 | 288 | dc | 0.750 | 0.825 | 0.854 | 0.896 | [0.818, 0.886] |
| other | 577 | 288 | bc2 | 0.716 | 0.801 | 0.837 | 0.870 | [0.797, 0.873] |
| other | 577 | 288 | tb2 | 0.697 | 0.802 | 0.828 | 0.849 | [0.787, 0.863] |
| other | 577 | 288 | tb2c | 0.735 | 0.821 | 0.846 | 0.872 | [0.808, 0.879] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 377 | 250 | a | 0.170 | 0.231 | 0.260 | 0.302 | [0.201, 0.328] |
| image [0,.2) | 377 | 250 | ac | 0.273 | 0.361 | 0.385 | 0.424 | [0.318, 0.453] |
| image [0,.2) | 377 | 250 | c | 0.424 | 0.483 | 0.512 | 0.554 | [0.439, 0.580] |
| image [0,.2) | 377 | 250 | cc | 0.480 | 0.554 | 0.589 | 0.629 | [0.520, 0.650] |
| image [0,.2) | 377 | 250 | d | 0.464 | 0.512 | 0.541 | 0.578 | [0.472, 0.606] |
| image [0,.2) | 377 | 250 | dc | 0.507 | 0.568 | 0.592 | 0.647 | [0.522, 0.652] |
| image [0,.2) | 377 | 250 | bc2 | 0.440 | 0.509 | 0.536 | 0.594 | [0.464, 0.605] |
| image [0,.2) | 377 | 250 | tb2 | 0.273 | 0.337 | 0.377 | 0.414 | [0.307, 0.448] |
| image [0,.2) | 377 | 250 | tb2c | 0.316 | 0.419 | 0.448 | 0.515 | [0.377, 0.515] |
| image [.2,.5) | 1582 | 582 | a | 0.334 | 0.423 | 0.460 | 0.520 | [0.412, 0.508] |
| image [.2,.5) | 1582 | 582 | ac | 0.401 | 0.501 | 0.544 | 0.611 | [0.493, 0.591] |
| image [.2,.5) | 1582 | 582 | c | 0.610 | 0.687 | 0.713 | 0.755 | [0.678, 0.745] |
| image [.2,.5) | 1582 | 582 | cc | 0.630 | 0.712 | 0.743 | 0.787 | [0.710, 0.772] |
| image [.2,.5) | 1582 | 582 | d | 0.611 | 0.695 | 0.719 | 0.766 | [0.685, 0.750] |
| image [.2,.5) | 1582 | 582 | dc | 0.626 | 0.714 | 0.743 | 0.788 | [0.709, 0.773] |
| image [.2,.5) | 1582 | 582 | bc2 | 0.571 | 0.659 | 0.703 | 0.758 | [0.666, 0.733] |
| image [.2,.5) | 1582 | 582 | tb2 | 0.538 | 0.623 | 0.659 | 0.718 | [0.619, 0.693] |
| image [.2,.5) | 1582 | 582 | tb2c | 0.547 | 0.648 | 0.683 | 0.750 | [0.643, 0.716] |
| image [.5,.8) | 2825 | 680 | a | 0.464 | 0.548 | 0.585 | 0.638 | [0.549, 0.620] |
| image [.5,.8) | 2825 | 680 | ac | 0.490 | 0.570 | 0.609 | 0.668 | [0.573, 0.643] |
| image [.5,.8) | 2825 | 680 | c | 0.562 | 0.663 | 0.699 | 0.752 | [0.669, 0.728] |
| image [.5,.8) | 2825 | 680 | cc | 0.574 | 0.672 | 0.707 | 0.760 | [0.677, 0.735] |
| image [.5,.8) | 2825 | 680 | d | 0.586 | 0.680 | 0.715 | 0.758 | [0.686, 0.745] |
| image [.5,.8) | 2825 | 680 | dc | 0.597 | 0.689 | 0.723 | 0.768 | [0.694, 0.751] |
| image [.5,.8) | 2825 | 680 | bc2 | 0.569 | 0.664 | 0.707 | 0.768 | [0.679, 0.735] |
| image [.5,.8) | 2825 | 680 | tb2 | 0.554 | 0.647 | 0.691 | 0.741 | [0.664, 0.722] |
| image [.5,.8) | 2825 | 680 | tb2c | 0.562 | 0.655 | 0.693 | 0.754 | [0.666, 0.722] |
| image [.8,1] | 2746 | 257 | a | 0.756 | 0.849 | 0.879 | 0.917 | [0.850, 0.906] |
| image [.8,1] | 2746 | 257 | ac | 0.752 | 0.834 | 0.863 | 0.890 | [0.828, 0.896] |
| image [.8,1] | 2746 | 257 | c | 0.833 | 0.905 | 0.925 | 0.948 | [0.909, 0.939] |
| image [.8,1] | 2746 | 257 | cc | 0.828 | 0.897 | 0.924 | 0.951 | [0.910, 0.938] |
| image [.8,1] | 2746 | 257 | d | 0.847 | 0.909 | 0.930 | 0.954 | [0.916, 0.943] |
| image [.8,1] | 2746 | 257 | dc | 0.852 | 0.916 | 0.935 | 0.959 | [0.922, 0.948] |
| image [.8,1] | 2746 | 257 | bc2 | 0.730 | 0.812 | 0.840 | 0.878 | [0.807, 0.875] |
| image [.8,1] | 2746 | 257 | tb2 | 0.801 | 0.886 | 0.918 | 0.946 | [0.902, 0.934] |
| image [.8,1] | 2746 | 257 | tb2c | 0.807 | 0.889 | 0.920 | 0.944 | [0.904, 0.935] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 3814 | 332 | a | 0.794 | 0.857 | 0.877 | 0.918 | [0.850, 0.897] |
| textlike [0,.2) | 3814 | 332 | ac | 0.783 | 0.846 | 0.868 | 0.909 | [0.839, 0.890] |
| textlike [0,.2) | 3814 | 332 | c | 0.856 | 0.906 | 0.921 | 0.940 | [0.909, 0.932] |
| textlike [0,.2) | 3814 | 332 | cc | 0.851 | 0.900 | 0.918 | 0.939 | [0.905, 0.930] |
| textlike [0,.2) | 3814 | 332 | d | 0.862 | 0.909 | 0.921 | 0.938 | [0.907, 0.932] |
| textlike [0,.2) | 3814 | 332 | dc | 0.868 | 0.913 | 0.926 | 0.945 | [0.914, 0.938] |
| textlike [0,.2) | 3814 | 332 | bc2 | 0.777 | 0.835 | 0.860 | 0.905 | [0.832, 0.883] |
| textlike [0,.2) | 3814 | 332 | tb2 | 0.814 | 0.867 | 0.888 | 0.930 | [0.862, 0.907] |
| textlike [0,.2) | 3814 | 332 | tb2c | 0.820 | 0.869 | 0.889 | 0.928 | [0.863, 0.908] |
| textlike [.2,.5) | 3458 | 616 | a | 0.672 | 0.750 | 0.779 | 0.829 | [0.752, 0.803] |
| textlike [.2,.5) | 3458 | 616 | ac | 0.688 | 0.772 | 0.799 | 0.837 | [0.774, 0.822] |
| textlike [.2,.5) | 3458 | 616 | c | 0.774 | 0.838 | 0.864 | 0.893 | [0.848, 0.880] |
| textlike [.2,.5) | 3458 | 616 | cc | 0.788 | 0.852 | 0.877 | 0.909 | [0.861, 0.891] |
| textlike [.2,.5) | 3458 | 616 | d | 0.789 | 0.846 | 0.871 | 0.897 | [0.856, 0.885] |
| textlike [.2,.5) | 3458 | 616 | dc | 0.800 | 0.857 | 0.881 | 0.911 | [0.866, 0.895] |
| textlike [.2,.5) | 3458 | 616 | bc2 | 0.720 | 0.796 | 0.828 | 0.862 | [0.810, 0.848] |
| textlike [.2,.5) | 3458 | 616 | tb2 | 0.718 | 0.797 | 0.825 | 0.860 | [0.807, 0.843] |
| textlike [.2,.5) | 3458 | 616 | tb2c | 0.730 | 0.805 | 0.833 | 0.870 | [0.814, 0.851] |
| textlike [.5,.8) | 1706 | 745 | a | 0.294 | 0.375 | 0.403 | 0.445 | [0.357, 0.446] |
| textlike [.5,.8) | 1706 | 745 | ac | 0.373 | 0.460 | 0.492 | 0.553 | [0.446, 0.535] |
| textlike [.5,.8) | 1706 | 745 | c | 0.480 | 0.543 | 0.562 | 0.589 | [0.520, 0.602] |
| textlike [.5,.8) | 1706 | 745 | cc | 0.510 | 0.577 | 0.603 | 0.636 | [0.564, 0.639] |
| textlike [.5,.8) | 1706 | 745 | d | 0.489 | 0.550 | 0.569 | 0.598 | [0.528, 0.608] |
| textlike [.5,.8) | 1706 | 745 | dc | 0.512 | 0.583 | 0.607 | 0.635 | [0.566, 0.644] |
| textlike [.5,.8) | 1706 | 745 | bc2 | 0.504 | 0.578 | 0.610 | 0.661 | [0.572, 0.647] |
| textlike [.5,.8) | 1706 | 745 | tb2 | 0.450 | 0.529 | 0.557 | 0.604 | [0.518, 0.595] |
| textlike [.5,.8) | 1706 | 745 | tb2c | 0.484 | 0.568 | 0.601 | 0.660 | [0.562, 0.635] |
| textlike [.8,1] | 440 | 299 | a | 0.164 | 0.223 | 0.243 | 0.289 | [0.189, 0.303] |
| textlike [.8,1] | 440 | 299 | ac | 0.266 | 0.357 | 0.405 | 0.466 | [0.343, 0.469] |
| textlike [.8,1] | 440 | 299 | c | 0.343 | 0.420 | 0.450 | 0.491 | [0.387, 0.518] |
| textlike [.8,1] | 440 | 299 | cc | 0.409 | 0.493 | 0.539 | 0.591 | [0.479, 0.597] |
| textlike [.8,1] | 440 | 299 | d | 0.345 | 0.443 | 0.480 | 0.516 | [0.418, 0.545] |
| textlike [.8,1] | 440 | 299 | dc | 0.414 | 0.507 | 0.559 | 0.607 | [0.499, 0.621] |
| textlike [.8,1] | 440 | 299 | bc2 | 0.370 | 0.468 | 0.516 | 0.570 | [0.457, 0.574] |
| textlike [.8,1] | 440 | 299 | tb2 | 0.252 | 0.336 | 0.377 | 0.414 | [0.316, 0.442] |
| textlike [.8,1] | 440 | 299 | tb2c | 0.334 | 0.432 | 0.475 | 0.530 | [0.414, 0.536] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 1959 | 832 | 0.421 | 0.513 | 0.674 | 0.713 | 0.685 | 0.714 | 0.671 | 0.605 | 0.638 | +0.253 | [+0.214, +0.294] |
| P2 textlike in [.5,.8)+[.8,1] | 2146 | 1044 | 0.370 | 0.474 | 0.539 | 0.590 | 0.551 | 0.597 | 0.591 | 0.521 | 0.575 | +0.169 | [+0.136, +0.200] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 part: image [0,.2) | 377 | 250 | 0.260 | 0.385 | 0.512 | 0.589 | 0.541 | 0.592 | 0.536 | 0.377 | 0.448 | +0.252 | [+0.184, +0.321] |
| P1 part: image [.2,.5) | 1582 | 582 | 0.460 | 0.544 | 0.713 | 0.743 | 0.719 | 0.743 | 0.703 | 0.659 | 0.683 | +0.253 | [+0.210, +0.297] |
| P2 part: textlike [.5,.8) | 1706 | 745 | 0.403 | 0.492 | 0.562 | 0.603 | 0.569 | 0.607 | 0.610 | 0.557 | 0.601 | +0.159 | [+0.124, +0.193] |
| P2 part: textlike [.8,1] | 440 | 299 | 0.243 | 0.405 | 0.450 | 0.539 | 0.480 | 0.559 | 0.516 | 0.377 | 0.475 | +0.207 | [+0.143, +0.270] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| image in [.5,.8)+[.8,1] | 5571 | 937 | 0.730 | 0.734 | 0.810 | 0.814 | 0.821 | 0.828 | 0.773 | 0.803 | 0.805 | +0.080 | [+0.063, +0.098] |
| textlike in [0,.2)+[.2,.5) | 7272 | 948 | 0.830 | 0.835 | 0.894 | 0.899 | 0.897 | 0.905 | 0.845 | 0.858 | 0.862 | +0.064 | [+0.050, +0.079] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 1959 | 832 | 0.421 | 0.513 | 0.674 | 0.713 | 0.685 | 0.714 | 0.671 | 0.605 | 0.638 | +0.010 | [+0.003, +0.019] |
| P2 textlike in [.5,.8)+[.8,1] | 2146 | 1044 | 0.370 | 0.474 | 0.539 | 0.590 | 0.551 | 0.597 | 0.591 | 0.521 | 0.575 | +0.012 | [+0.007, +0.018] |
| P1 part: image [0,.2) | 377 | 250 | 0.260 | 0.385 | 0.512 | 0.589 | 0.541 | 0.592 | 0.536 | 0.377 | 0.448 | +0.029 | [+0.013, +0.050] |
| P1 part: image [.2,.5) | 1582 | 582 | 0.460 | 0.544 | 0.713 | 0.743 | 0.719 | 0.743 | 0.703 | 0.659 | 0.683 | +0.006 | [-0.003, +0.015] |
| P2 part: textlike [.5,.8) | 1706 | 745 | 0.403 | 0.492 | 0.562 | 0.603 | 0.569 | 0.607 | 0.610 | 0.557 | 0.601 | +0.008 | [+0.002, +0.013] |
| P2 part: textlike [.8,1] | 440 | 299 | 0.243 | 0.405 | 0.450 | 0.539 | 0.480 | 0.559 | 0.516 | 0.377 | 0.475 | +0.030 | [+0.012, +0.048] |
| image in [.5,.8)+[.8,1] | 5571 | 937 | 0.730 | 0.734 | 0.810 | 0.814 | 0.821 | 0.828 | 0.773 | 0.803 | 0.805 | +0.011 | [+0.003, +0.021] |
| textlike in [0,.2)+[.2,.5) | 7272 | 948 | 0.830 | 0.835 | 0.894 | 0.899 | 0.897 | 0.905 | 0.845 | 0.858 | 0.862 | +0.003 | [-0.001, +0.007] |
| all [0,.2) | 4255 | 332 | 0.817 | 0.822 | 0.883 | 0.888 | 0.886 | 0.895 | 0.829 | 0.839 | 0.847 | +0.003 | [-0.003, +0.008] |
| all [.2,.5) | 5112 | 626 | 0.682 | 0.721 | 0.818 | 0.835 | 0.824 | 0.838 | 0.790 | 0.774 | 0.787 | +0.006 | [+0.002, +0.011] |
| all [.5,.8) | 4567 | 761 | 0.517 | 0.566 | 0.647 | 0.668 | 0.661 | 0.680 | 0.670 | 0.642 | 0.659 | +0.013 | [+0.005, +0.025] |
| all [.8,1] | 3206 | 316 | 0.790 | 0.799 | 0.858 | 0.870 | 0.867 | 0.883 | 0.794 | 0.842 | 0.857 | +0.009 | [+0.001, +0.019] |
| image [0,.2) | 377 | 250 | 0.260 | 0.385 | 0.512 | 0.589 | 0.541 | 0.592 | 0.536 | 0.377 | 0.448 | +0.029 | [+0.011, +0.050] |
| image [.2,.5) | 1582 | 582 | 0.460 | 0.544 | 0.713 | 0.743 | 0.719 | 0.743 | 0.703 | 0.659 | 0.683 | +0.006 | [-0.003, +0.014] |
| image [.5,.8) | 2825 | 680 | 0.585 | 0.609 | 0.699 | 0.707 | 0.715 | 0.723 | 0.707 | 0.691 | 0.693 | +0.017 | [+0.004, +0.034] |
| image [.8,1] | 2746 | 257 | 0.879 | 0.863 | 0.925 | 0.924 | 0.930 | 0.935 | 0.840 | 0.918 | 0.920 | +0.005 | [-0.004, +0.016] |
| textlike [0,.2) | 3814 | 332 | 0.877 | 0.868 | 0.921 | 0.918 | 0.921 | 0.926 | 0.860 | 0.888 | 0.889 | -0.001 | [-0.006, +0.005] |
| textlike [.2,.5) | 3458 | 616 | 0.779 | 0.799 | 0.864 | 0.877 | 0.871 | 0.881 | 0.828 | 0.825 | 0.833 | +0.007 | [+0.001, +0.013] |
| textlike [.5,.8) | 1706 | 745 | 0.403 | 0.492 | 0.562 | 0.603 | 0.569 | 0.607 | 0.610 | 0.557 | 0.601 | +0.008 | [+0.002, +0.013] |
| textlike [.8,1] | 440 | 299 | 0.243 | 0.405 | 0.450 | 0.539 | 0.480 | 0.559 | 0.516 | 0.377 | 0.475 | +0.030 | [+0.013, +0.048] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.692 | 0.421 | 0.370 | 0.730 | 0.830 | -0.104 [-0.115, -0.092] | -0.253 [-0.294, -0.214] | -0.169 [-0.200, -0.136] | -0.080 [-0.098, -0.063] | -0.064 [-0.079, -0.050] | -0.253 |
| ac | ref | 1.00 | 0.719 | 0.513 | 0.474 | 0.734 | 0.835 | -0.077 [-0.087, -0.064] | -0.161 [-0.201, -0.118] | -0.065 [-0.093, -0.035] | -0.076 [-0.095, -0.057] | -0.059 [-0.076, -0.045] | -0.161 |
| c | ref | 5.20 | 0.796 | 0.674 | 0.539 | 0.810 | 0.894 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| cc | ref | 5.20 | 0.810 | 0.713 | 0.590 | 0.814 | 0.899 | +0.014 [+0.011, +0.018] | +0.039 [+0.030, +0.049] | +0.051 [+0.040, +0.061] | +0.004 [-0.002, +0.009] | +0.005 [+0.000, +0.009] | +0.004 |
| d | ref | 9.87 | 0.804 | 0.685 | 0.551 | 0.821 | 0.897 | +0.008 [+0.005, +0.012] | +0.010 [+0.003, +0.019] | +0.012 [+0.007, +0.018] | +0.011 [+0.003, +0.021] | +0.003 [-0.001, +0.007] | +0.003 |
| dc | ref | 9.87 | 0.818 | 0.714 | 0.597 | 0.828 | 0.905 | +0.022 [+0.019, +0.027] | +0.039 [+0.028, +0.051] | +0.059 [+0.047, +0.070] | +0.018 [+0.009, +0.027] | +0.011 [+0.006, +0.015] | +0.011 |
| bc2 | F3 | 1.95 | 0.769 | 0.671 | 0.591 | 0.773 | 0.845 | -0.027 [-0.037, -0.018] | -0.004 [-0.021, +0.015] | +0.052 [+0.038, +0.066] | -0.037 [-0.057, -0.018] | -0.049 [-0.064, -0.036] | -0.049 |
| tb2 | F5 | 2.00 | 0.768 | 0.605 | 0.521 | 0.803 | 0.858 | -0.028 [-0.034, -0.021] | -0.069 [-0.088, -0.050] | -0.018 [-0.031, -0.006] | -0.007 [-0.015, +0.001] | -0.036 [-0.048, -0.024] | -0.069 |
| tb2c | F5 | 2.00 | 0.781 | 0.638 | 0.575 | 0.805 | 0.862 | -0.015 [-0.022, -0.007] | -0.037 [-0.058, -0.014] | +0.036 [+0.018, +0.053] | -0.005 [-0.016, +0.004] | -0.032 [-0.046, -0.019] | -0.037 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.584 | 0.303 | 0.267 | 0.608 | 0.736 |
| ac | 0.608 | 0.377 | 0.351 | 0.619 | 0.738 |
| c | 0.703 | 0.574 | 0.452 | 0.696 | 0.817 |
| cc | 0.713 | 0.601 | 0.489 | 0.699 | 0.821 |
| d | 0.715 | 0.583 | 0.460 | 0.714 | 0.827 |
| dc | 0.728 | 0.603 | 0.492 | 0.723 | 0.836 |
| bc2 | 0.657 | 0.546 | 0.476 | 0.648 | 0.750 |
| tb2 | 0.659 | 0.487 | 0.409 | 0.676 | 0.768 |
| tb2c | 0.672 | 0.503 | 0.453 | 0.683 | 0.777 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.739 | 0.478 | 0.413 | 0.776 | 0.876 |
| ac | 0.765 | 0.575 | 0.535 | 0.777 | 0.875 |
| c | 0.828 | 0.717 | 0.569 | 0.849 | 0.917 |
| cc | 0.844 | 0.757 | 0.627 | 0.854 | 0.925 |
| d | 0.833 | 0.730 | 0.581 | 0.855 | 0.918 |
| dc | 0.850 | 0.761 | 0.630 | 0.862 | 0.929 |
| bc2 | 0.815 | 0.726 | 0.643 | 0.822 | 0.885 |
| tb2 | 0.809 | 0.660 | 0.565 | 0.842 | 0.897 |
| tb2c | 0.827 | 0.704 | 0.633 | 0.848 | 0.900 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.112 [-0.124, -0.100] | -0.263 [-0.307, -0.224] | -0.181 [-0.213, -0.149] | -0.091 [-0.112, -0.073] | -0.067 [-0.082, -0.054] |
| ac | -0.085 [-0.097, -0.071] | -0.172 [-0.213, -0.129] | -0.077 [-0.104, -0.048] | -0.087 [-0.109, -0.067] | -0.062 [-0.079, -0.048] |
| c | -0.008 [-0.012, -0.005] | -0.010 [-0.019, -0.003] | -0.012 [-0.018, -0.007] | -0.011 [-0.021, -0.003] | -0.003 [-0.007, +0.001] |
| cc | +0.006 [+0.002, +0.010] | +0.029 [+0.019, +0.039] | +0.039 [+0.029, +0.048] | -0.007 [-0.017, +0.001] | +0.002 [-0.003, +0.006] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| dc | +0.015 [+0.012, +0.017] | +0.029 [+0.020, +0.039] | +0.047 [+0.037, +0.057] | +0.006 [+0.003, +0.010] | +0.008 [+0.004, +0.011] |
| bc2 | -0.035 [-0.045, -0.025] | -0.014 [-0.031, +0.003] | +0.040 [+0.026, +0.054] | -0.048 [-0.070, -0.027] | -0.052 [-0.067, -0.039] |
| tb2 | -0.036 [-0.043, -0.028] | -0.080 [-0.100, -0.061] | -0.030 [-0.044, -0.018] | -0.018 [-0.031, -0.007] | -0.039 [-0.051, -0.027] |
| tb2c | -0.023 [-0.031, -0.015] | -0.047 [-0.069, -0.026] | +0.024 [+0.007, +0.041] | -0.016 [-0.030, -0.004] | -0.035 [-0.049, -0.023] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.127 [-0.138, -0.115] | -0.292 [-0.334, -0.253] | -0.227 [-0.261, -0.195] | -0.097 [-0.118, -0.079] | -0.074 [-0.089, -0.061] |
| ac | -0.099 [-0.111, -0.086] | -0.201 [-0.241, -0.159] | -0.123 [-0.152, -0.096] | -0.094 [-0.116, -0.074] | -0.070 [-0.086, -0.055] |
| c | -0.022 [-0.027, -0.019] | -0.039 [-0.051, -0.028] | -0.059 [-0.070, -0.047] | -0.018 [-0.027, -0.009] | -0.011 [-0.015, -0.006] |
| cc | -0.008 [-0.012, -0.005] | -0.001 [-0.007, +0.006] | -0.007 [-0.013, -0.002] | -0.014 [-0.023, -0.006] | -0.006 [-0.009, -0.002] |
| d | -0.015 [-0.017, -0.012] | -0.029 [-0.039, -0.020] | -0.047 [-0.057, -0.037] | -0.006 [-0.010, -0.003] | -0.008 [-0.011, -0.004] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| bc2 | -0.050 [-0.059, -0.040] | -0.043 [-0.060, -0.026] | -0.007 [-0.018, +0.005] | -0.055 [-0.076, -0.034] | -0.060 [-0.075, -0.047] |
| tb2 | -0.051 [-0.058, -0.043] | -0.109 [-0.129, -0.090] | -0.077 [-0.091, -0.061] | -0.025 [-0.037, -0.014] | -0.046 [-0.059, -0.035] |
| tb2c | -0.038 [-0.045, -0.030] | -0.076 [-0.095, -0.056] | -0.022 [-0.036, -0.008] | -0.023 [-0.036, -0.011] | -0.043 [-0.057, -0.030] |

### Session 9 selection rule applied to the eval queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F3 | bc2 | 1.95 | -0.049 | -0.004 | +0.052 | -0.037 | -0.049 |
| F5 | tb2c | 2.00 | -0.037 | -0.037 | +0.036 | -0.005 | -0.032 |

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.381 | 0.776 | 0.725 | 0.518 |
| centered | 0.080 | 0.575 | 0.458 | 0.193 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2 | 2.00 | 0.918 | 1976 |
| tb2c | 2.00 | 0.885 | 1976 |

### Session 9 hypotheses on the eval queries

H9b, F3 selected bc2: upper bounds of (x - c) all -0.018, P1 image in [0,.2)+[.2,.5) +0.015, P2 textlike in [.5,.8)+[.8,1] +0.066, image in [.5,.8)+[.8,1] -0.018, textlike in [0,.2)+[.2,.5) -0.036; any below -0.02: yes, H9b dead for this family.

## Output, E2 jina-clip-v2 (`/workspace/logs/s11b/eval_e2.md`, verbatim)

Model: jina-clip-v2. Queries: 17140 over 2035 directories; 2597 directories ranked (random recall@k = k/2597). Queries dropped for lack of a vector: 328 {'other': 310, 'image': 13, 'text': 1, 'table': 4}. Queries in calibration directories, not used: 4085.

Mean representative vectors per directory: a 1.00, ac 1.00, c 5.20, cc 5.20, d 9.87, dc 9.87, bc2 1.95, tb2 2.00, tb2c 2.00.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 17140 | 2035 | a | 0.358 | 0.426 | 0.457 | 0.501 | [0.439, 0.475] |
| all | 17140 | 2035 | ac | 0.432 | 0.517 | 0.559 | 0.613 | [0.543, 0.575] |
| all | 17140 | 2035 | c | 0.585 | 0.654 | 0.683 | 0.720 | [0.668, 0.695] |
| all | 17140 | 2035 | cc | 0.592 | 0.662 | 0.693 | 0.733 | [0.679, 0.705] |
| all | 17140 | 2035 | d | 0.600 | 0.667 | 0.694 | 0.727 | [0.679, 0.706] |
| all | 17140 | 2035 | dc | 0.611 | 0.677 | 0.706 | 0.744 | [0.692, 0.717] |
| all | 17140 | 2035 | bc2 | 0.500 | 0.581 | 0.617 | 0.666 | [0.601, 0.632] |
| all | 17140 | 2035 | tb2 | 0.516 | 0.592 | 0.625 | 0.670 | [0.611, 0.639] |
| all | 17140 | 2035 | tb2c | 0.521 | 0.600 | 0.634 | 0.689 | [0.620, 0.649] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 4255 | 332 | a | 0.504 | 0.576 | 0.611 | 0.653 | [0.576, 0.640] |
| [0,.2) | 4255 | 332 | ac | 0.498 | 0.571 | 0.606 | 0.656 | [0.572, 0.637] |
| [0,.2) | 4255 | 332 | c | 0.649 | 0.706 | 0.733 | 0.769 | [0.706, 0.757] |
| [0,.2) | 4255 | 332 | cc | 0.653 | 0.712 | 0.740 | 0.776 | [0.715, 0.764] |
| [0,.2) | 4255 | 332 | d | 0.674 | 0.731 | 0.753 | 0.784 | [0.727, 0.776] |
| [0,.2) | 4255 | 332 | dc | 0.685 | 0.741 | 0.765 | 0.798 | [0.741, 0.787] |
| [0,.2) | 4255 | 332 | bc2 | 0.497 | 0.568 | 0.597 | 0.655 | [0.562, 0.630] |
| [0,.2) | 4255 | 332 | tb2 | 0.545 | 0.601 | 0.630 | 0.678 | [0.598, 0.660] |
| [0,.2) | 4255 | 332 | tb2c | 0.566 | 0.631 | 0.657 | 0.717 | [0.627, 0.686] |
| [.2,.5) | 5112 | 626 | a | 0.214 | 0.277 | 0.306 | 0.344 | [0.274, 0.336] |
| [.2,.5) | 5112 | 626 | ac | 0.358 | 0.455 | 0.503 | 0.558 | [0.477, 0.529] |
| [.2,.5) | 5112 | 626 | c | 0.555 | 0.626 | 0.656 | 0.695 | [0.628, 0.680] |
| [.2,.5) | 5112 | 626 | cc | 0.570 | 0.640 | 0.673 | 0.718 | [0.646, 0.697] |
| [.2,.5) | 5112 | 626 | d | 0.567 | 0.634 | 0.665 | 0.701 | [0.637, 0.690] |
| [.2,.5) | 5112 | 626 | dc | 0.582 | 0.650 | 0.684 | 0.725 | [0.657, 0.708] |
| [.2,.5) | 5112 | 626 | bc2 | 0.483 | 0.561 | 0.601 | 0.648 | [0.574, 0.627] |
| [.2,.5) | 5112 | 626 | tb2 | 0.471 | 0.554 | 0.592 | 0.637 | [0.563, 0.617] |
| [.2,.5) | 5112 | 626 | tb2c | 0.469 | 0.549 | 0.586 | 0.641 | [0.556, 0.612] |
| [.5,.8) | 4567 | 761 | a | 0.195 | 0.253 | 0.285 | 0.335 | [0.254, 0.316] |
| [.5,.8) | 4567 | 761 | ac | 0.320 | 0.403 | 0.450 | 0.516 | [0.421, 0.480] |
| [.5,.8) | 4567 | 761 | c | 0.474 | 0.551 | 0.582 | 0.624 | [0.552, 0.612] |
| [.5,.8) | 4567 | 761 | cc | 0.483 | 0.557 | 0.591 | 0.637 | [0.563, 0.622] |
| [.5,.8) | 4567 | 761 | d | 0.485 | 0.560 | 0.591 | 0.630 | [0.562, 0.620] |
| [.5,.8) | 4567 | 761 | dc | 0.493 | 0.568 | 0.599 | 0.643 | [0.569, 0.629] |
| [.5,.8) | 4567 | 761 | bc2 | 0.448 | 0.533 | 0.572 | 0.623 | [0.543, 0.601] |
| [.5,.8) | 4567 | 761 | tb2 | 0.449 | 0.529 | 0.563 | 0.611 | [0.535, 0.592] |
| [.5,.8) | 4567 | 761 | tb2c | 0.439 | 0.522 | 0.564 | 0.621 | [0.534, 0.591] |
| [.8,1] | 3206 | 316 | a | 0.624 | 0.708 | 0.741 | 0.785 | [0.713, 0.770] |
| [.8,1] | 3206 | 316 | ac | 0.620 | 0.708 | 0.742 | 0.781 | [0.707, 0.774] |
| [.8,1] | 3206 | 316 | c | 0.705 | 0.780 | 0.803 | 0.835 | [0.779, 0.824] |
| [.8,1] | 3206 | 316 | cc | 0.703 | 0.781 | 0.805 | 0.834 | [0.780, 0.826] |
| [.8,1] | 3206 | 316 | d | 0.721 | 0.785 | 0.807 | 0.834 | [0.784, 0.827] |
| [.8,1] | 3206 | 316 | dc | 0.727 | 0.793 | 0.814 | 0.846 | [0.791, 0.834] |
| [.8,1] | 3206 | 316 | bc2 | 0.606 | 0.698 | 0.731 | 0.772 | [0.698, 0.763] |
| [.8,1] | 3206 | 316 | tb2 | 0.643 | 0.728 | 0.759 | 0.797 | [0.733, 0.785] |
| [.8,1] | 3206 | 316 | tb2c | 0.663 | 0.749 | 0.781 | 0.825 | [0.757, 0.804] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 7530 | 1769 | a | 0.384 | 0.455 | 0.488 | 0.536 | [0.456, 0.517] |
| image | 7530 | 1769 | ac | 0.462 | 0.550 | 0.592 | 0.646 | [0.564, 0.617] |
| image | 7530 | 1769 | c | 0.613 | 0.695 | 0.726 | 0.767 | [0.706, 0.744] |
| image | 7530 | 1769 | cc | 0.620 | 0.700 | 0.731 | 0.773 | [0.712, 0.748] |
| image | 7530 | 1769 | d | 0.626 | 0.703 | 0.733 | 0.769 | [0.713, 0.751] |
| image | 7530 | 1769 | dc | 0.635 | 0.710 | 0.739 | 0.779 | [0.719, 0.756] |
| image | 7530 | 1769 | bc2 | 0.555 | 0.646 | 0.683 | 0.738 | [0.662, 0.703] |
| image | 7530 | 1769 | tb2 | 0.569 | 0.656 | 0.693 | 0.742 | [0.672, 0.711] |
| image | 7530 | 1769 | tb2c | 0.566 | 0.653 | 0.693 | 0.749 | [0.671, 0.712] |
| pdf_text | 1603 | 639 | a | 0.507 | 0.567 | 0.600 | 0.632 | [0.545, 0.644] |
| pdf_text | 1603 | 639 | ac | 0.565 | 0.661 | 0.702 | 0.745 | [0.658, 0.737] |
| pdf_text | 1603 | 639 | c | 0.644 | 0.703 | 0.722 | 0.746 | [0.681, 0.754] |
| pdf_text | 1603 | 639 | cc | 0.656 | 0.719 | 0.744 | 0.778 | [0.705, 0.775] |
| pdf_text | 1603 | 639 | d | 0.642 | 0.704 | 0.722 | 0.745 | [0.681, 0.755] |
| pdf_text | 1603 | 639 | dc | 0.662 | 0.725 | 0.749 | 0.780 | [0.710, 0.781] |
| pdf_text | 1603 | 639 | bc2 | 0.595 | 0.672 | 0.710 | 0.749 | [0.668, 0.743] |
| pdf_text | 1603 | 639 | tb2 | 0.601 | 0.677 | 0.705 | 0.730 | [0.664, 0.737] |
| pdf_text | 1603 | 639 | tb2c | 0.611 | 0.697 | 0.726 | 0.769 | [0.685, 0.758] |
| text | 3348 | 1085 | a | 0.296 | 0.358 | 0.388 | 0.424 | [0.343, 0.429] |
| text | 3348 | 1085 | ac | 0.359 | 0.424 | 0.467 | 0.513 | [0.427, 0.505] |
| text | 3348 | 1085 | c | 0.499 | 0.552 | 0.574 | 0.607 | [0.540, 0.607] |
| text | 3348 | 1085 | cc | 0.506 | 0.561 | 0.585 | 0.620 | [0.551, 0.616] |
| text | 3348 | 1085 | d | 0.520 | 0.567 | 0.594 | 0.618 | [0.558, 0.627] |
| text | 3348 | 1085 | dc | 0.527 | 0.577 | 0.602 | 0.634 | [0.567, 0.633] |
| text | 3348 | 1085 | bc2 | 0.388 | 0.445 | 0.483 | 0.525 | [0.444, 0.518] |
| text | 3348 | 1085 | tb2 | 0.407 | 0.458 | 0.492 | 0.534 | [0.455, 0.527] |
| text | 3348 | 1085 | tb2c | 0.409 | 0.476 | 0.506 | 0.548 | [0.467, 0.542] |
| table | 3890 | 837 | a | 0.300 | 0.371 | 0.404 | 0.447 | [0.363, 0.449] |
| table | 3890 | 837 | ac | 0.378 | 0.471 | 0.513 | 0.575 | [0.475, 0.549] |
| table | 3890 | 837 | c | 0.587 | 0.654 | 0.689 | 0.729 | [0.662, 0.713] |
| table | 3890 | 837 | cc | 0.591 | 0.658 | 0.694 | 0.738 | [0.667, 0.718] |
| table | 3890 | 837 | d | 0.613 | 0.680 | 0.707 | 0.746 | [0.678, 0.732] |
| table | 3890 | 837 | dc | 0.625 | 0.690 | 0.719 | 0.763 | [0.693, 0.744] |
| table | 3890 | 837 | bc2 | 0.454 | 0.532 | 0.563 | 0.616 | [0.528, 0.600] |
| table | 3890 | 837 | tb2 | 0.475 | 0.551 | 0.579 | 0.628 | [0.543, 0.613] |
| table | 3890 | 837 | tb2c | 0.500 | 0.567 | 0.596 | 0.662 | [0.563, 0.630] |
| other | 577 | 288 | a | 0.352 | 0.412 | 0.433 | 0.480 | [0.353, 0.511] |
| other | 577 | 288 | ac | 0.463 | 0.553 | 0.596 | 0.655 | [0.527, 0.658] |
| other | 577 | 288 | c | 0.527 | 0.582 | 0.600 | 0.650 | [0.536, 0.652] |
| other | 577 | 288 | cc | 0.563 | 0.617 | 0.653 | 0.697 | [0.590, 0.704] |
| other | 577 | 288 | d | 0.530 | 0.577 | 0.594 | 0.650 | [0.533, 0.647] |
| other | 577 | 288 | dc | 0.555 | 0.612 | 0.659 | 0.697 | [0.594, 0.713] |
| other | 577 | 288 | bc2 | 0.494 | 0.589 | 0.624 | 0.666 | [0.560, 0.680] |
| other | 577 | 288 | tb2 | 0.497 | 0.565 | 0.596 | 0.638 | [0.534, 0.652] |
| other | 577 | 288 | tb2c | 0.511 | 0.577 | 0.622 | 0.683 | [0.556, 0.680] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 377 | 250 | a | 0.003 | 0.003 | 0.003 | 0.003 | [0.000, 0.008] |
| image [0,.2) | 377 | 250 | ac | 0.029 | 0.045 | 0.080 | 0.119 | [0.049, 0.115] |
| image [0,.2) | 377 | 250 | c | 0.300 | 0.342 | 0.361 | 0.387 | [0.279, 0.438] |
| image [0,.2) | 377 | 250 | cc | 0.324 | 0.361 | 0.390 | 0.411 | [0.306, 0.466] |
| image [0,.2) | 377 | 250 | d | 0.302 | 0.340 | 0.355 | 0.379 | [0.278, 0.427] |
| image [0,.2) | 377 | 250 | dc | 0.313 | 0.355 | 0.379 | 0.408 | [0.299, 0.449] |
| image [0,.2) | 377 | 250 | bc2 | 0.297 | 0.347 | 0.369 | 0.408 | [0.290, 0.437] |
| image [0,.2) | 377 | 250 | tb2 | 0.162 | 0.178 | 0.183 | 0.207 | [0.119, 0.249] |
| image [0,.2) | 377 | 250 | tb2c | 0.106 | 0.122 | 0.138 | 0.178 | [0.089, 0.189] |
| image [.2,.5) | 1582 | 582 | a | 0.039 | 0.057 | 0.067 | 0.084 | [0.041, 0.095] |
| image [.2,.5) | 1582 | 582 | ac | 0.200 | 0.282 | 0.325 | 0.388 | [0.276, 0.368] |
| image [.2,.5) | 1582 | 582 | c | 0.504 | 0.574 | 0.601 | 0.637 | [0.558, 0.638] |
| image [.2,.5) | 1582 | 582 | cc | 0.520 | 0.592 | 0.619 | 0.664 | [0.578, 0.655] |
| image [.2,.5) | 1582 | 582 | d | 0.501 | 0.573 | 0.601 | 0.632 | [0.557, 0.639] |
| image [.2,.5) | 1582 | 582 | dc | 0.515 | 0.583 | 0.615 | 0.654 | [0.574, 0.651] |
| image [.2,.5) | 1582 | 582 | bc2 | 0.469 | 0.546 | 0.578 | 0.636 | [0.536, 0.615] |
| image [.2,.5) | 1582 | 582 | tb2 | 0.468 | 0.535 | 0.568 | 0.618 | [0.526, 0.604] |
| image [.2,.5) | 1582 | 582 | tb2c | 0.406 | 0.489 | 0.525 | 0.586 | [0.479, 0.566] |
| image [.5,.8) | 2825 | 680 | a | 0.297 | 0.381 | 0.425 | 0.493 | [0.381, 0.465] |
| image [.5,.8) | 2825 | 680 | ac | 0.427 | 0.520 | 0.569 | 0.638 | [0.533, 0.604] |
| image [.5,.8) | 2825 | 680 | c | 0.546 | 0.642 | 0.682 | 0.736 | [0.651, 0.712] |
| image [.5,.8) | 2825 | 680 | cc | 0.555 | 0.648 | 0.687 | 0.745 | [0.656, 0.717] |
| image [.5,.8) | 2825 | 680 | d | 0.564 | 0.659 | 0.697 | 0.744 | [0.665, 0.726] |
| image [.5,.8) | 2825 | 680 | dc | 0.572 | 0.664 | 0.700 | 0.753 | [0.669, 0.728] |
| image [.5,.8) | 2825 | 680 | bc2 | 0.523 | 0.621 | 0.668 | 0.736 | [0.636, 0.700] |
| image [.5,.8) | 2825 | 680 | tb2 | 0.529 | 0.629 | 0.673 | 0.735 | [0.643, 0.703] |
| image [.5,.8) | 2825 | 680 | tb2c | 0.530 | 0.627 | 0.679 | 0.749 | [0.650, 0.709] |
| image [.8,1] | 2746 | 257 | a | 0.725 | 0.823 | 0.862 | 0.912 | [0.834, 0.889] |
| image [.8,1] | 2746 | 257 | ac | 0.708 | 0.805 | 0.839 | 0.877 | [0.804, 0.874] |
| image [.8,1] | 2746 | 257 | c | 0.787 | 0.869 | 0.893 | 0.926 | [0.872, 0.910] |
| image [.8,1] | 2746 | 257 | cc | 0.784 | 0.863 | 0.887 | 0.915 | [0.865, 0.908] |
| image [.8,1] | 2746 | 257 | d | 0.806 | 0.873 | 0.897 | 0.925 | [0.875, 0.916] |
| image [.8,1] | 2746 | 257 | dc | 0.813 | 0.878 | 0.899 | 0.929 | [0.877, 0.918] |
| image [.8,1] | 2746 | 257 | bc2 | 0.673 | 0.770 | 0.803 | 0.843 | [0.767, 0.842] |
| image [.8,1] | 2746 | 257 | tb2 | 0.725 | 0.820 | 0.855 | 0.896 | [0.830, 0.880] |
| image [.8,1] | 2746 | 257 | tb2c | 0.757 | 0.847 | 0.880 | 0.922 | [0.857, 0.901] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 3814 | 332 | a | 0.561 | 0.640 | 0.679 | 0.726 | [0.646, 0.709] |
| textlike [0,.2) | 3814 | 332 | ac | 0.550 | 0.628 | 0.664 | 0.715 | [0.628, 0.697] |
| textlike [0,.2) | 3814 | 332 | c | 0.684 | 0.742 | 0.770 | 0.808 | [0.745, 0.794] |
| textlike [0,.2) | 3814 | 332 | cc | 0.687 | 0.747 | 0.775 | 0.813 | [0.750, 0.798] |
| textlike [0,.2) | 3814 | 332 | d | 0.711 | 0.771 | 0.793 | 0.825 | [0.769, 0.815] |
| textlike [0,.2) | 3814 | 332 | dc | 0.724 | 0.780 | 0.804 | 0.837 | [0.781, 0.823] |
| textlike [0,.2) | 3814 | 332 | bc2 | 0.518 | 0.590 | 0.620 | 0.678 | [0.579, 0.655] |
| textlike [0,.2) | 3814 | 332 | tb2 | 0.585 | 0.645 | 0.675 | 0.726 | [0.640, 0.706] |
| textlike [0,.2) | 3814 | 332 | tb2c | 0.616 | 0.684 | 0.711 | 0.773 | [0.678, 0.741] |
| textlike [.2,.5) | 3458 | 616 | a | 0.289 | 0.372 | 0.410 | 0.455 | [0.371, 0.449] |
| textlike [.2,.5) | 3458 | 616 | ac | 0.426 | 0.529 | 0.580 | 0.631 | [0.551, 0.612] |
| textlike [.2,.5) | 3458 | 616 | c | 0.576 | 0.647 | 0.679 | 0.720 | [0.654, 0.701] |
| textlike [.2,.5) | 3458 | 616 | cc | 0.591 | 0.660 | 0.695 | 0.742 | [0.671, 0.719] |
| textlike [.2,.5) | 3458 | 616 | d | 0.595 | 0.660 | 0.692 | 0.731 | [0.666, 0.716] |
| textlike [.2,.5) | 3458 | 616 | dc | 0.611 | 0.678 | 0.714 | 0.756 | [0.688, 0.737] |
| textlike [.2,.5) | 3458 | 616 | bc2 | 0.487 | 0.564 | 0.609 | 0.652 | [0.581, 0.639] |
| textlike [.2,.5) | 3458 | 616 | tb2 | 0.471 | 0.560 | 0.600 | 0.644 | [0.571, 0.629] |
| textlike [.2,.5) | 3458 | 616 | tb2c | 0.495 | 0.574 | 0.611 | 0.663 | [0.584, 0.640] |
| textlike [.5,.8) | 1706 | 745 | a | 0.021 | 0.033 | 0.044 | 0.062 | [0.029, 0.060] |
| textlike [.5,.8) | 1706 | 745 | ac | 0.141 | 0.206 | 0.249 | 0.311 | [0.215, 0.286] |
| textlike [.5,.8) | 1706 | 745 | c | 0.353 | 0.399 | 0.415 | 0.436 | [0.371, 0.457] |
| textlike [.5,.8) | 1706 | 745 | cc | 0.360 | 0.404 | 0.430 | 0.457 | [0.389, 0.473] |
| textlike [.5,.8) | 1706 | 745 | d | 0.353 | 0.396 | 0.414 | 0.438 | [0.371, 0.457] |
| textlike [.5,.8) | 1706 | 745 | dc | 0.361 | 0.406 | 0.429 | 0.459 | [0.387, 0.472] |
| textlike [.5,.8) | 1706 | 745 | bc2 | 0.326 | 0.387 | 0.413 | 0.438 | [0.374, 0.454] |
| textlike [.5,.8) | 1706 | 745 | tb2 | 0.316 | 0.363 | 0.380 | 0.403 | [0.339, 0.422] |
| textlike [.5,.8) | 1706 | 745 | tb2c | 0.287 | 0.348 | 0.370 | 0.406 | [0.330, 0.415] |
| textlike [.8,1] | 440 | 299 | a | 0.000 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] |
| textlike [.8,1] | 440 | 299 | ac | 0.077 | 0.116 | 0.150 | 0.198 | [0.107, 0.198] |
| textlike [.8,1] | 440 | 299 | c | 0.198 | 0.241 | 0.257 | 0.280 | [0.195, 0.316] |
| textlike [.8,1] | 440 | 299 | cc | 0.209 | 0.282 | 0.302 | 0.341 | [0.243, 0.367] |
| textlike [.8,1] | 440 | 299 | d | 0.195 | 0.248 | 0.259 | 0.270 | [0.197, 0.319] |
| textlike [.8,1] | 440 | 299 | dc | 0.198 | 0.273 | 0.293 | 0.341 | [0.234, 0.356] |
| textlike [.8,1] | 440 | 299 | bc2 | 0.205 | 0.264 | 0.298 | 0.341 | [0.237, 0.359] |
| textlike [.8,1] | 440 | 299 | tb2 | 0.143 | 0.166 | 0.175 | 0.189 | [0.118, 0.228] |
| textlike [.8,1] | 440 | 299 | tb2c | 0.091 | 0.145 | 0.180 | 0.234 | [0.124, 0.232] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 1959 | 832 | 0.055 | 0.278 | 0.555 | 0.575 | 0.554 | 0.570 | 0.538 | 0.494 | 0.450 | +0.500 | [+0.462, +0.538] |
| P2 textlike in [.5,.8)+[.8,1] | 2146 | 1044 | 0.035 | 0.229 | 0.383 | 0.404 | 0.383 | 0.401 | 0.390 | 0.338 | 0.331 | +0.348 | [+0.312, +0.386] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 part: image [0,.2) | 377 | 250 | 0.003 | 0.080 | 0.361 | 0.390 | 0.355 | 0.379 | 0.369 | 0.183 | 0.138 | +0.358 | [+0.277, +0.433] |
| P1 part: image [.2,.5) | 1582 | 582 | 0.067 | 0.325 | 0.601 | 0.619 | 0.601 | 0.615 | 0.578 | 0.568 | 0.525 | +0.534 | [+0.492, +0.576] |
| P2 part: textlike [.5,.8) | 1706 | 745 | 0.044 | 0.249 | 0.415 | 0.430 | 0.414 | 0.429 | 0.413 | 0.380 | 0.370 | +0.371 | [+0.327, +0.411] |
| P2 part: textlike [.8,1] | 440 | 299 | 0.000 | 0.150 | 0.257 | 0.302 | 0.259 | 0.293 | 0.298 | 0.175 | 0.180 | +0.257 | [+0.195, +0.315] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| image in [.5,.8)+[.8,1] | 5571 | 937 | 0.640 | 0.702 | 0.786 | 0.786 | 0.796 | 0.798 | 0.734 | 0.763 | 0.778 | +0.146 | [+0.126, +0.168] |
| textlike in [0,.2)+[.2,.5) | 7272 | 948 | 0.551 | 0.624 | 0.727 | 0.737 | 0.745 | 0.761 | 0.615 | 0.639 | 0.664 | +0.176 | [+0.152, +0.200] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | ac | c | cc | d | dc | bc2 | tb2 | tb2c | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 1959 | 832 | 0.055 | 0.278 | 0.555 | 0.575 | 0.554 | 0.570 | 0.538 | 0.494 | 0.450 | -0.001 | [-0.009, +0.008] |
| P2 textlike in [.5,.8)+[.8,1] | 2146 | 1044 | 0.035 | 0.229 | 0.383 | 0.404 | 0.383 | 0.401 | 0.390 | 0.338 | 0.331 | +0.000 | [-0.004, +0.005] |
| P1 part: image [0,.2) | 377 | 250 | 0.003 | 0.080 | 0.361 | 0.390 | 0.355 | 0.379 | 0.369 | 0.183 | 0.138 | -0.005 | [-0.018, +0.006] |
| P1 part: image [.2,.5) | 1582 | 582 | 0.067 | 0.325 | 0.601 | 0.619 | 0.601 | 0.615 | 0.578 | 0.568 | 0.525 | +0.000 | [-0.010, +0.010] |
| P2 part: textlike [.5,.8) | 1706 | 745 | 0.044 | 0.249 | 0.415 | 0.430 | 0.414 | 0.429 | 0.413 | 0.380 | 0.370 | -0.001 | [-0.007, +0.005] |
| P2 part: textlike [.8,1] | 440 | 299 | 0.000 | 0.150 | 0.257 | 0.302 | 0.259 | 0.293 | 0.298 | 0.175 | 0.180 | +0.002 | [+0.000, +0.007] |
| image in [.5,.8)+[.8,1] | 5571 | 937 | 0.640 | 0.702 | 0.786 | 0.786 | 0.796 | 0.798 | 0.734 | 0.763 | 0.778 | +0.010 | [+0.003, +0.018] |
| textlike in [0,.2)+[.2,.5) | 7272 | 948 | 0.551 | 0.624 | 0.727 | 0.737 | 0.745 | 0.761 | 0.615 | 0.639 | 0.664 | +0.018 | [+0.012, +0.025] |
| all [0,.2) | 4255 | 332 | 0.611 | 0.606 | 0.733 | 0.740 | 0.753 | 0.765 | 0.597 | 0.630 | 0.657 | +0.020 | [+0.012, +0.028] |
| all [.2,.5) | 5112 | 626 | 0.306 | 0.503 | 0.656 | 0.673 | 0.665 | 0.684 | 0.601 | 0.592 | 0.586 | +0.009 | [+0.002, +0.016] |
| all [.5,.8) | 4567 | 761 | 0.285 | 0.450 | 0.582 | 0.591 | 0.591 | 0.599 | 0.572 | 0.563 | 0.564 | +0.009 | [+0.002, +0.017] |
| all [.8,1] | 3206 | 316 | 0.741 | 0.742 | 0.803 | 0.805 | 0.807 | 0.814 | 0.731 | 0.759 | 0.781 | +0.004 | [-0.004, +0.012] |
| image [0,.2) | 377 | 250 | 0.003 | 0.080 | 0.361 | 0.390 | 0.355 | 0.379 | 0.369 | 0.183 | 0.138 | -0.005 | [-0.018, +0.006] |
| image [.2,.5) | 1582 | 582 | 0.067 | 0.325 | 0.601 | 0.619 | 0.601 | 0.615 | 0.578 | 0.568 | 0.525 | +0.000 | [-0.010, +0.010] |
| image [.5,.8) | 2825 | 680 | 0.425 | 0.569 | 0.682 | 0.687 | 0.697 | 0.700 | 0.668 | 0.673 | 0.679 | +0.015 | [+0.004, +0.029] |
| image [.8,1] | 2746 | 257 | 0.862 | 0.839 | 0.893 | 0.887 | 0.897 | 0.899 | 0.803 | 0.855 | 0.880 | +0.004 | [-0.005, +0.014] |
| textlike [0,.2) | 3814 | 332 | 0.679 | 0.664 | 0.770 | 0.775 | 0.793 | 0.804 | 0.620 | 0.675 | 0.711 | +0.023 | [+0.014, +0.033] |
| textlike [.2,.5) | 3458 | 616 | 0.410 | 0.580 | 0.679 | 0.695 | 0.692 | 0.714 | 0.609 | 0.600 | 0.611 | +0.013 | [+0.004, +0.022] |
| textlike [.5,.8) | 1706 | 745 | 0.044 | 0.249 | 0.415 | 0.430 | 0.414 | 0.429 | 0.413 | 0.380 | 0.370 | -0.001 | [-0.007, +0.005] |
| textlike [.8,1] | 440 | 299 | 0.000 | 0.150 | 0.257 | 0.302 | 0.259 | 0.293 | 0.298 | 0.175 | 0.180 | +0.002 | [+0.000, +0.007] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.457 | 0.055 | 0.035 | 0.640 | 0.551 | -0.225 [-0.241, -0.210] | -0.500 [-0.538, -0.462] | -0.348 [-0.386, -0.312] | -0.146 [-0.168, -0.126] | -0.176 [-0.200, -0.152] | -0.500 |
| ac | ref | 1.00 | 0.559 | 0.278 | 0.229 | 0.702 | 0.624 | -0.124 [-0.137, -0.111] | -0.277 [-0.319, -0.237] | -0.154 [-0.187, -0.121] | -0.084 [-0.102, -0.066] | -0.103 [-0.122, -0.082] | -0.277 |
| c | ref | 5.20 | 0.683 | 0.555 | 0.383 | 0.786 | 0.727 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| cc | ref | 5.20 | 0.693 | 0.575 | 0.404 | 0.786 | 0.737 | +0.010 [+0.006, +0.013] | +0.020 [+0.013, +0.028] | +0.021 [+0.013, +0.030] | +0.000 [-0.005, +0.005] | +0.011 [+0.004, +0.017] | +0.000 |
| d | ref | 9.87 | 0.694 | 0.554 | 0.383 | 0.796 | 0.745 | +0.011 [+0.007, +0.015] | -0.001 [-0.009, +0.008] | +0.000 [-0.004, +0.005] | +0.010 [+0.003, +0.018] | +0.018 [+0.012, +0.025] | -0.001 |
| dc | ref | 9.87 | 0.706 | 0.570 | 0.401 | 0.798 | 0.761 | +0.023 [+0.019, +0.027] | +0.015 [+0.005, +0.025] | +0.019 [+0.010, +0.028] | +0.012 [+0.005, +0.021] | +0.034 [+0.028, +0.042] | +0.012 |
| bc2 | F3 | 1.95 | 0.617 | 0.538 | 0.390 | 0.734 | 0.615 | -0.066 [-0.077, -0.055] | -0.017 [-0.034, -0.002] | +0.007 [-0.009, +0.024] | -0.052 [-0.070, -0.033] | -0.112 [-0.132, -0.092] | -0.112 |
| tb2 | F5 | 2.00 | 0.625 | 0.494 | 0.338 | 0.763 | 0.639 | -0.058 [-0.067, -0.049] | -0.061 [-0.081, -0.041] | -0.045 [-0.060, -0.029] | -0.023 [-0.037, -0.010] | -0.087 [-0.104, -0.071] | -0.087 |
| tb2c | F5 | 2.00 | 0.634 | 0.450 | 0.331 | 0.778 | 0.664 | -0.049 [-0.058, -0.039] | -0.105 [-0.130, -0.080] | -0.052 [-0.076, -0.029] | -0.008 [-0.019, +0.004] | -0.063 [-0.078, -0.049] | -0.105 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.358 | 0.032 | 0.017 | 0.508 | 0.432 |
| ac | 0.432 | 0.167 | 0.128 | 0.565 | 0.491 |
| c | 0.585 | 0.465 | 0.321 | 0.665 | 0.633 |
| cc | 0.592 | 0.482 | 0.329 | 0.668 | 0.641 |
| d | 0.600 | 0.462 | 0.321 | 0.683 | 0.656 |
| dc | 0.611 | 0.476 | 0.328 | 0.691 | 0.670 |
| bc2 | 0.500 | 0.436 | 0.301 | 0.597 | 0.503 |
| tb2 | 0.516 | 0.409 | 0.281 | 0.626 | 0.531 |
| tb2c | 0.521 | 0.349 | 0.247 | 0.642 | 0.558 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.501 | 0.068 | 0.049 | 0.700 | 0.597 |
| ac | 0.613 | 0.336 | 0.288 | 0.756 | 0.675 |
| c | 0.720 | 0.589 | 0.404 | 0.829 | 0.766 |
| cc | 0.733 | 0.616 | 0.433 | 0.829 | 0.779 |
| d | 0.727 | 0.583 | 0.404 | 0.834 | 0.780 |
| dc | 0.744 | 0.606 | 0.435 | 0.840 | 0.799 |
| bc2 | 0.666 | 0.592 | 0.418 | 0.789 | 0.666 |
| tb2 | 0.670 | 0.539 | 0.359 | 0.814 | 0.687 |
| tb2c | 0.689 | 0.507 | 0.371 | 0.834 | 0.721 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.236 [-0.251, -0.221] | -0.499 [-0.536, -0.460] | -0.348 [-0.386, -0.311] | -0.155 [-0.179, -0.135] | -0.194 [-0.218, -0.170] |
| ac | -0.134 [-0.147, -0.120] | -0.276 [-0.316, -0.237] | -0.154 [-0.187, -0.122] | -0.094 [-0.115, -0.074] | -0.121 [-0.142, -0.101] |
| c | -0.011 [-0.015, -0.007] | +0.001 [-0.008, +0.009] | +0.000 [-0.005, +0.004] | -0.010 [-0.018, -0.003] | -0.018 [-0.025, -0.012] |
| cc | -0.001 [-0.006, +0.004] | +0.021 [+0.012, +0.031] | +0.021 [+0.013, +0.030] | -0.010 [-0.019, -0.002] | -0.008 [-0.016, +0.001] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| dc | +0.012 [+0.009, +0.015] | +0.016 [+0.010, +0.023] | +0.019 [+0.011, +0.027] | +0.003 [-0.001, +0.006] | +0.016 [+0.011, +0.021] |
| bc2 | -0.077 [-0.088, -0.065] | -0.016 [-0.034, +0.000] | +0.007 [-0.010, +0.024] | -0.061 [-0.082, -0.041] | -0.130 [-0.150, -0.109] |
| tb2 | -0.069 [-0.078, -0.059] | -0.060 [-0.082, -0.040] | -0.045 [-0.061, -0.029] | -0.033 [-0.049, -0.017] | -0.105 [-0.124, -0.088] |
| tb2c | -0.059 [-0.069, -0.049] | -0.104 [-0.130, -0.077] | -0.052 [-0.076, -0.029] | -0.018 [-0.033, -0.004] | -0.081 [-0.098, -0.067] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.248 [-0.264, -0.233] | -0.515 [-0.552, -0.476] | -0.366 [-0.405, -0.330] | -0.158 [-0.181, -0.137] | -0.210 [-0.234, -0.187] |
| ac | -0.146 [-0.159, -0.133] | -0.292 [-0.332, -0.253] | -0.172 [-0.206, -0.140] | -0.096 [-0.118, -0.077] | -0.137 [-0.157, -0.117] |
| c | -0.023 [-0.027, -0.019] | -0.015 [-0.025, -0.005] | -0.019 [-0.028, -0.010] | -0.012 [-0.021, -0.005] | -0.034 [-0.042, -0.028] |
| cc | -0.013 [-0.017, -0.009] | +0.006 [-0.002, +0.013] | +0.003 [-0.002, +0.007] | -0.012 [-0.021, -0.005] | -0.024 [-0.030, -0.017] |
| d | -0.012 [-0.015, -0.009] | -0.016 [-0.023, -0.010] | -0.019 [-0.027, -0.011] | -0.003 [-0.006, +0.001] | -0.016 [-0.021, -0.011] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| bc2 | -0.089 [-0.100, -0.077] | -0.032 [-0.049, -0.017] | -0.012 [-0.028, +0.003] | -0.064 [-0.084, -0.045] | -0.146 [-0.167, -0.126] |
| tb2 | -0.081 [-0.090, -0.071] | -0.076 [-0.099, -0.055] | -0.063 [-0.080, -0.047] | -0.036 [-0.051, -0.020] | -0.121 [-0.140, -0.104] |
| tb2c | -0.071 [-0.081, -0.061] | -0.119 [-0.147, -0.094] | -0.070 [-0.092, -0.049] | -0.020 [-0.035, -0.006] | -0.097 [-0.112, -0.083] |

### Session 9 selection rule applied to the eval queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F3 | bc2 | 1.95 | -0.112 | -0.017 | +0.007 | -0.052 | -0.112 |
| F5 | tb2 | 2.00 | -0.087 | -0.061 | -0.045 | -0.023 | -0.087 |

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.787 | 0.751 | 0.701 | 0.196 |
| centered | 0.092 | 0.561 | 0.410 | 0.096 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2 | 2.00 | 0.982 | 1976 |
| tb2c | 2.00 | 0.895 | 1976 |

### Session 9 hypotheses on the eval queries

H9b, F3 selected bc2: upper bounds of (x - c) all -0.055, P1 image in [0,.2)+[.2,.5) -0.002, P2 textlike in [.5,.8)+[.8,1] +0.024, image in [.5,.8)+[.8,1] -0.033, textlike in [0,.2)+[.2,.5) -0.092; any below -0.02: yes, H9b dead for this family.
