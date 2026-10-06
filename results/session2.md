# dirvec session 2: encoder pilot and first measurement

> **Errata, added 2026-10-01 after the number audit (reports/number_audit_2026-10-01.md). The text and
> tables below are unchanged; where a sentence and a verbatim table disagree, the table is right.**
> - "The file-level baseline d is at or above b and c in every cell": not in every cell. For image
>   queries in [.5,.8) b and c are at 0.837 against d's 0.833, and two more cells differ by 0.002 to
>   0.010 the same way. d is not beaten by more than 0.010 anywhere on this set.
> - "Where the query's modality dominates the directory, a is as good as b and c": for text-like
>   queries in [0,.2) a is 0.949 against c's 0.970; for image queries in [.8,1] c - a is -0.001.


Date: 2026-09-29. Hardware: NVIDIA RTX PRO 4500 Blackwell Server Edition (32 GB), RunPod.
Corpus: 400 Zenodo directories, 4,773 files, rebuilt with `fetch.py download` (0 failures);
`manifest.py` reproduces the committed sha256 for every file (see NOTES.md, session 2).

## Verdict

**The claim is dead under the session 2 kill criterion.** On image queries in the
[.8,1] bucket the pooled centroid (a) is not beaten: b - a = -0.018 (95% CI -0.029 to -0.007,
b is worse), c - a = -0.001 (-0.020 to +0.016). In [.5,.8) both b and c beat a
(+0.054, CIs exclude zero), but the criterion needs both high buckets.

What the numbers show instead (post hoc, not a pre-registered test): the pooled centroid loses
the *minority* modality of each directory, not images as such. Image queries lose most in
text-heavy directories ([0,.2): recall@5 a 0.427, b 0.672, c 0.695). Text-like queries lose most
in image-heavy directories ([.8,1]: a 0.347, b 0.639, c 0.618). Where the query's modality
dominates the directory, a is as good as b and c. The file-level baseline d is at or above b and c
in every cell; the container representations match it at about half the vectors
(c: 5.3 per directory, d: 11.8), they do not beat it.

## Encoder pilot

20 directories, 5 per image_frac bucket, drawn with seed 20260929 from directories holding at
least 2 images and at least 1 text or table file; all 395 of their files embedded.
Check: for every text or table file (213), rank each image of its own directory among all
167 pilot images by cosine (1,433 pairs). Random median rank is 84; random median of the best
own-image rank is 19.

| model | text path | median rank | median normalised rank | median best own-image rank |
|---|---|---:|---:|---:|
| jina-embeddings-v4 | query (`prompt_name="query"`) | **8** | 0.048 | **1** |
| jina-embeddings-v4 | document (`prompt_name="passage"`) | 11 | 0.066 | 1 |
| nomic-embed-multimodal-3b | query (`process_queries`) | 19 | 0.114 | 1 |
| nomic-embed-multimodal-3b | document (`process_texts`) | 54 | 0.323 | 20 |
| random | | 84 | 0.5 | 19 |

Both models beat random clearly on their query-side text path. nomic's document-side text path
is near random on the best-own-image measure: the model was trained for text queries against page
images only. Pilot wall time 205 s (jina) and 185 s (nomic) for 395 files.

## Encoder choice

jina-embeddings-v4, `jinaai/jina-embeddings-v4` revision 853c867b65b749f3c3c72a06868140d842e04f06,
single-vector mode (2048 d), `task="retrieval"`, text through the query-side path, images at
most 602,112 pixels (768 visual tokens), bfloat16, transformers 4.52.4. Every file encoded once
the same way, so the same vector serves as query and as directory child.

Embedded: 4,729 of 4,773 files (image 2,285, text 1,003, table 943, pdf_text 326,
pdf_scanned 67, other 105). Skipped and counted, all manifest modality "other": 20 files PIL
cannot identify (19 tif, 1 png), 10 pptx, 6 doc, 2 odp, 5 without extension, 1 corrupt docx.
Full run 33 min.

## Method

Leave-one-out over `gt_structural.jsonl`: 4,115 queries, of which 44 ("other" files with no
vector) drop out, leaving 4,071 over 398 directories. All 400 directories rank (random
recall@k = k/400). For each query the query's own directory is rebuilt without it; score is
the max cosine over a directory's representative vectors. Bootstrap: 1,000 resamples of the
directories in each cell; the paired columns use the same resamples for both representations.

a pooled centroid; b per-modality centroids; c per-modality k-means reps, k = min(3, n_m);
d every child vector (file-level max, no container layer).

## Tables (output of `python scripts/eval.py --model jina-embeddings-v4`)

Model: jina-embeddings-v4. Queries: 4071 over 398 directories; 400 directories ranked (random recall@k = k/400). Queries dropped for lack of a vector: 44 {'other': 44}.

Mean representative vectors per directory: a 1.00, b 2.54, c 5.34, d 11.82.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 4071 | 398 | a | 0.722 | 0.808 | 0.842 | 0.892 | [0.824, 0.860] |
| all | 4071 | 398 | b | 0.767 | 0.842 | 0.881 | 0.918 | [0.865, 0.898] |
| all | 4071 | 398 | c | 0.807 | 0.868 | 0.891 | 0.929 | [0.875, 0.907] |
| all | 4071 | 398 | d | 0.813 | 0.871 | 0.897 | 0.931 | [0.881, 0.912] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 1453 | 103 | a | 0.794 | 0.878 | 0.900 | 0.926 | [0.876, 0.922] |
| [0,.2) | 1453 | 103 | b | 0.809 | 0.885 | 0.924 | 0.937 | [0.901, 0.941] |
| [0,.2) | 1453 | 103 | c | 0.868 | 0.926 | 0.941 | 0.950 | [0.923, 0.956] |
| [0,.2) | 1453 | 103 | d | 0.875 | 0.929 | 0.942 | 0.951 | [0.925, 0.957] |
| [.2,.5) | 725 | 100 | a | 0.688 | 0.789 | 0.832 | 0.884 | [0.791, 0.865] |
| [.2,.5) | 725 | 100 | b | 0.770 | 0.844 | 0.870 | 0.912 | [0.831, 0.903] |
| [.2,.5) | 725 | 100 | c | 0.790 | 0.852 | 0.876 | 0.916 | [0.838, 0.905] |
| [.2,.5) | 725 | 100 | d | 0.790 | 0.852 | 0.887 | 0.920 | [0.850, 0.918] |
| [.5,.8) | 781 | 97 | a | 0.597 | 0.675 | 0.721 | 0.828 | [0.654, 0.781] |
| [.5,.8) | 781 | 97 | b | 0.703 | 0.777 | 0.816 | 0.885 | [0.760, 0.863] |
| [.5,.8) | 781 | 97 | c | 0.698 | 0.777 | 0.814 | 0.895 | [0.758, 0.861] |
| [.5,.8) | 781 | 97 | d | 0.697 | 0.775 | 0.814 | 0.898 | [0.759, 0.862] |
| [.8,1] | 1112 | 98 | a | 0.740 | 0.821 | 0.857 | 0.897 | [0.833, 0.883] |
| [.8,1] | 1112 | 98 | b | 0.756 | 0.831 | 0.879 | 0.921 | [0.850, 0.905] |
| [.8,1] | 1112 | 98 | c | 0.816 | 0.867 | 0.891 | 0.934 | [0.862, 0.915] |
| [.8,1] | 1112 | 98 | d | 0.828 | 0.876 | 0.901 | 0.937 | [0.871, 0.924] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 1780 | 359 | a | 0.689 | 0.774 | 0.820 | 0.889 | [0.788, 0.850] |
| image | 1780 | 359 | b | 0.734 | 0.816 | 0.857 | 0.915 | [0.830, 0.879] |
| image | 1780 | 359 | c | 0.774 | 0.839 | 0.866 | 0.924 | [0.837, 0.891] |
| image | 1780 | 359 | d | 0.785 | 0.840 | 0.872 | 0.926 | [0.844, 0.896] |
| pdf_text | 315 | 146 | a | 0.771 | 0.835 | 0.863 | 0.908 | [0.817, 0.904] |
| pdf_text | 315 | 146 | b | 0.810 | 0.851 | 0.879 | 0.908 | [0.833, 0.919] |
| pdf_text | 315 | 146 | c | 0.790 | 0.854 | 0.879 | 0.914 | [0.835, 0.919] |
| pdf_text | 315 | 146 | d | 0.794 | 0.860 | 0.883 | 0.927 | [0.839, 0.922] |
| text | 944 | 212 | a | 0.693 | 0.811 | 0.843 | 0.878 | [0.798, 0.880] |
| text | 944 | 212 | b | 0.736 | 0.818 | 0.883 | 0.908 | [0.848, 0.912] |
| text | 944 | 212 | c | 0.816 | 0.880 | 0.900 | 0.930 | [0.867, 0.926] |
| text | 944 | 212 | d | 0.815 | 0.882 | 0.904 | 0.931 | [0.870, 0.928] |
| table | 881 | 194 | a | 0.792 | 0.854 | 0.868 | 0.906 | [0.828, 0.902] |
| table | 881 | 194 | b | 0.844 | 0.915 | 0.931 | 0.947 | [0.907, 0.949] |
| table | 881 | 194 | c | 0.869 | 0.921 | 0.940 | 0.951 | [0.917, 0.957] |
| table | 881 | 194 | d | 0.873 | 0.930 | 0.949 | 0.952 | [0.928, 0.966] |
| other | 105 | 47 | a | 0.838 | 0.886 | 0.905 | 0.924 | [0.824, 0.958] |
| other | 105 | 47 | b | 0.876 | 0.924 | 0.924 | 0.924 | [0.850, 0.971] |
| other | 105 | 47 | c | 0.876 | 0.914 | 0.924 | 0.924 | [0.850, 0.971] |
| other | 105 | 47 | d | 0.876 | 0.905 | 0.914 | 0.924 | [0.844, 0.963] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 131 | 80 | a | 0.313 | 0.366 | 0.427 | 0.511 | [0.308, 0.541] |
| image [0,.2) | 131 | 80 | b | 0.511 | 0.641 | 0.672 | 0.695 | [0.559, 0.771] |
| image [0,.2) | 131 | 80 | c | 0.534 | 0.641 | 0.695 | 0.718 | [0.586, 0.788] |
| image [0,.2) | 131 | 80 | d | 0.588 | 0.649 | 0.702 | 0.733 | [0.598, 0.794] |
| image [.2,.5) | 210 | 96 | a | 0.429 | 0.567 | 0.638 | 0.729 | [0.536, 0.730] |
| image [.2,.5) | 210 | 96 | b | 0.633 | 0.714 | 0.752 | 0.814 | [0.657, 0.822] |
| image [.2,.5) | 210 | 96 | c | 0.638 | 0.719 | 0.743 | 0.814 | [0.649, 0.819] |
| image [.2,.5) | 210 | 96 | d | 0.652 | 0.724 | 0.762 | 0.814 | [0.670, 0.836] |
| image [.5,.8) | 478 | 90 | a | 0.640 | 0.726 | 0.782 | 0.914 | [0.711, 0.847] |
| image [.5,.8) | 478 | 90 | b | 0.707 | 0.795 | 0.837 | 0.937 | [0.785, 0.886] |
| image [.5,.8) | 478 | 90 | c | 0.711 | 0.799 | 0.837 | 0.944 | [0.769, 0.893] |
| image [.5,.8) | 478 | 90 | d | 0.707 | 0.789 | 0.833 | 0.944 | [0.765, 0.890] |
| image [.8,1] | 961 | 93 | a | 0.821 | 0.898 | 0.932 | 0.963 | [0.907, 0.954] |
| image [.8,1] | 961 | 93 | b | 0.800 | 0.872 | 0.915 | 0.955 | [0.884, 0.941] |
| image [.8,1] | 961 | 93 | c | 0.867 | 0.913 | 0.931 | 0.966 | [0.901, 0.956] |
| image [.8,1] | 961 | 93 | d | 0.879 | 0.917 | 0.939 | 0.968 | [0.909, 0.963] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 1304 | 101 | a | 0.845 | 0.932 | 0.949 | 0.970 | [0.930, 0.966] |
| textlike [0,.2) | 1304 | 101 | b | 0.843 | 0.914 | 0.953 | 0.965 | [0.935, 0.969] |
| textlike [0,.2) | 1304 | 101 | c | 0.906 | 0.959 | 0.970 | 0.977 | [0.957, 0.981] |
| textlike [0,.2) | 1304 | 101 | d | 0.908 | 0.962 | 0.971 | 0.977 | [0.958, 0.982] |
| textlike [.2,.5) | 506 | 100 | a | 0.798 | 0.885 | 0.915 | 0.953 | [0.884, 0.945] |
| textlike [.2,.5) | 506 | 100 | b | 0.830 | 0.903 | 0.925 | 0.958 | [0.895, 0.952] |
| textlike [.2,.5) | 506 | 100 | c | 0.858 | 0.913 | 0.937 | 0.962 | [0.912, 0.960] |
| textlike [.2,.5) | 506 | 100 | d | 0.852 | 0.911 | 0.943 | 0.968 | [0.916, 0.965] |
| textlike [.5,.8) | 291 | 95 | a | 0.512 | 0.577 | 0.608 | 0.680 | [0.502, 0.702] |
| textlike [.5,.8) | 291 | 95 | b | 0.687 | 0.739 | 0.773 | 0.794 | [0.693, 0.837] |
| textlike [.5,.8) | 291 | 95 | c | 0.667 | 0.735 | 0.770 | 0.811 | [0.684, 0.830] |
| textlike [.5,.8) | 291 | 95 | d | 0.670 | 0.746 | 0.780 | 0.818 | [0.696, 0.842] |
| textlike [.8,1] | 144 | 89 | a | 0.194 | 0.299 | 0.347 | 0.451 | [0.239, 0.452] |
| textlike [.8,1] | 144 | 89 | b | 0.465 | 0.549 | 0.639 | 0.688 | [0.511, 0.733] |
| textlike [.8,1] | 144 | 89 | c | 0.472 | 0.556 | 0.618 | 0.722 | [0.496, 0.715] |
| textlike [.8,1] | 144 | 89 | d | 0.486 | 0.597 | 0.646 | 0.729 | [0.528, 0.740] |

### Kill criterion: image queries, recall@5, paired bootstrap over directories

| bucket | queries | dirs | a | b | c | d | b-a | b-a 95% CI | c-a | c-a 95% CI | d-a | d-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|
| [0,.2) | 131 | 80 | 0.427 | 0.672 | 0.695 | 0.702 | +0.244 | [+0.117, +0.377] | +0.267 | [+0.148, +0.400] | +0.275 | [+0.156, +0.406] |
| [.2,.5) | 210 | 96 | 0.638 | 0.752 | 0.743 | 0.762 | +0.114 | [+0.038, +0.198] | +0.105 | [+0.031, +0.184] | +0.124 | [+0.049, +0.207] |
| [.5,.8) | 478 | 90 | 0.782 | 0.837 | 0.837 | 0.833 | +0.054 | [+0.018, +0.096] | +0.054 | [+0.009, +0.101] | +0.050 | [+0.007, +0.096] |
| [.8,1] | 961 | 93 | 0.932 | 0.915 | 0.931 | 0.939 | -0.018 | [-0.029, -0.007] | -0.001 | [-0.020, +0.016] | +0.006 | [-0.018, +0.028] |

Paired 95% interval of the difference excludes zero (lower bound > 0): [.5,.8): b-a yes, c-a yes; [.8,1]: b-a no, c-a no.
Claim is dead under the session 2 kill criterion.
