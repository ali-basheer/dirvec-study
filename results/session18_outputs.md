# Session 18 outputs, verbatim

Written by scripts/s18_run.sh on the pod, 2026-10-02T16:37Z, repo commit 66698b7.
Nothing here is edited. The verdicts and the reading are in results/session18.md. The generated texts are in
data/s18/ (captions, abstracts and member descriptions, gzipped json lines).

## Run log

```
15:31:43 start, commit 074ac14, resume 0
15:32:29 text heads (E1 venv, background)
15:32:29 vLLM venv: vllm==0.11.0 transformers>=4.57,<4.58
15:33:02 vLLM venv: vllm 0.11.0 torch 2.8.0+cu128 cuda 12.8 transformers 4.57.6
15:33:02 describe with mistral-community/pixtral-12b
15:44:26 describe with mistral-community/pixtral-12b: exit 0, 3959 lines
15:44:26 heads: 12757 text-like files embedded under E1, 0 without text, 473s
15:44:26 summarize with Qwen/Qwen3-VL-8B-Instruct
16:16:43 summarize with Qwen/Qwen3-VL-8B-Instruct: exit 0, 12880 lines
16:16:43 captions 12880, abstracts 2597, members 3959
16:16:43 embed, E1
16:21:33 embed, E3
16:23:38 eval, e1
16:35:10 start, commit 66698b7, resume 1
16:35:41 S18_FROM=eval: generation and embedding skipped (outputs on the volume)
16:35:41 eval, e1
16:36:27 H18a (jina-embeddings-v4): s1 - c on Q_title, image-heavy folders, recall@5 = -0.007 [-0.049, +0.038] over 1382 queries and 813 families: outcome 'between'.
16:36:27 H18b (jina-embeddings-v4): Q_mem P1, 1959 queries and 731 families; gate d = 0.785 >= 0.25 (passed); c - s1 = +0.291 [+0.259, +0.322] (holds); c - a = +0.290 [+0.260, +0.324] (holds): H18b survives.
16:36:27 eval, e3
16:37:13 H18a (gme-Qwen2-VL-2B-Instruct): s1 - c on Q_title, image-heavy folders, recall@5 = -0.263 [-0.433, -0.096] over 1382 queries and 813 families: outcome 'below c'.
16:37:13 H18b (gme-Qwen2-VL-2B-Instruct): Q_mem P1, 1959 queries and 731 families; gate d = 0.751 >= 0.25 (passed); c - s1 = +0.344 [+0.310, +0.380] (holds); c - a = +0.290 [+0.259, +0.322] (holds): H18b survi
16:37:13 generated texts into data/s18 (gzip, raw model outputs kept for the member descriptions only)
```

## Environment

```
NVIDIA H100 80GB HBM3, 580.126.09, 81559 MiB
overlay                       60G   19G   42G  31% /
mfs#us-ne-1.runpod.net:9421  992T  646T  347T  66% /workspace
nproc 12
               total        used        free      shared  buff/cache   available
Mem:            2015         252         986           3         791        1763
E1 venv: torch 2.8.0+cu128 transformers 4.52.4 scikit-learn 1.9.1
```

## Generation and embedding summaries

```
heads: 12757 text-like files embedded under E1, 0 without text, 473s
jina-embeddings-v4: wrote /workspace/dirvec/data/emb/jina-embeddings-v4_s11/s18_vecs.npz; empty texts encoded as '(no text)': {'l1': 0, 'l0': 0, 'sw1': 0, 'captions': 0, 'members': 0}
gme-Qwen2-VL-2B-Instruct: wrote /workspace/dirvec/data/emb/gme-Qwen2-VL-2B-Instruct_s11/s18_vecs.npz; empty texts encoded as '(no text)': {'l1': 0, 'l0': 0, 'sw1': 0, 'captions': 0, 'members': 0}
15:34:35 mistral-community/pixtral-12b revision c2756cbbb9422eba9f6c5c439a214b0392dfc998; vllm 0.11.0
[1;36m(EngineCore_DP0 pid=2654)[0;0m INFO 10-02 15:34:51 [core.py:77] Initializing a V1 LLM engine (v0.11.0) with config: model='/root/hf_gen/hub/models--mistral-community--pixtral-12b/snapshots/c2756cbbb9422eba9f6c5c439a214b0392dfc998', 
15:35:41 smoke AF2_Fig4A.png: The image shows a molecular structure with different colored regions, including blue, green, and orange sections, likely representing a protein or enzyme comple
15:35:41 smoke FigS1E_13BHalo_ManIIRFP_GALTGFP_H2O.tif: This image appears to be a blurry black and white photo of a person holding a small object.
15:35:41 smoke FigS1E_VPS13BHalo_Bet1GFP_ManIIRFP_H2O.tif: This image appears to show a blurry, black and white view of two bright spots in the night sky.
15:35:41 smoke FigS1F_VapGFP_VPS13BHalo_GalTRFP_H2O.tif: It's a close-up, black and white image of a textured surface with a rough, uneven appearance.
15:35:41 smoke figSM1_uncertainty_process.png: This image illustrates a flowchart for performing an uncertainty analysis on mosquito presence data using machine learning models.
15:35:41 smoke Fig2_b__displacementmap_simu.png: This image shows a 3D box with numerous vectors inside, each represented by colored arrows and circles.
15:35:41 smoke Supplementary_Material_S3.jpg: This image shows various fragments of ancient plant remains, specifically endocarps and exocarps, from archaeological samples.
15:35:41 smoke Suplementary_Figure_1.tiff: This image shows six plots of the log hazard ratio of death against various factors with confidence intervals and p-values for nonlinearity.
15:35:41 smoke Suplementary_Figure_2.tiff: This image shows a series of scatter plots with residuals versus observation IDs for various medical conditions and measurements.
15:35:41 smoke swm_logo.png: This image shows a detailed illustration of a human brain with colorful contour lines and the letters "SWM" below it.
15:44:23 describe done: 3959 new, 0 earlier
15:45:28 Qwen/Qwen3-VL-8B-Instruct revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b; vllm 0.11.0
[1;36m(EngineCore_DP0 pid=8141)[0;0m INFO 10-02 15:45:35 [core.py:77] Initializing a V1 LLM engine (v0.11.0) with config: model='/root/hf_gen/hub/models--Qwen--Qwen3-VL-8B-Instruct/snapshots/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b', spec
15:46:41 smoke TLS_J17136_P02_1_1.tiff: This is a colorful micrograph showing a detailed view of biological tissue, likely stained to highlight different cellular components. The image reveals intrica
15:46:41 smoke TLS_J17136_P02_2_1.tiff: This is a colorful micrograph showing a tissue sample with cells stained in vibrant hues of purple, cyan, and yellow. The image reveals cellular structures and 
15:46:41 smoke TLS_J17136_P03_1_1.tiff: This is a colorful micrograph showing a detailed view of tissue, likely from a biological sample, with cells highlighted in various hues. The image reveals a co
15:46:41 smoke TLS_J17136_P03_2_1.tiff: This is a colorful micrograph showing a dense, textured biological tissue sample with fluorescently labeled cells. The image highlights various cell types and s
15:46:41 smoke TLS_J17136_P03_3_1.tiff: This is a colorful micrograph showing a detailed view of cellular structures, likely from biological tissue, with cells highlighted in various hues. The image r
15:46:41 smoke TLS_J17136_P03_4_1.tiff: This is a colorful micrograph showing a detailed view of tissue, likely from a biological sample, with cells and structures highlighted in vibrant hues. The ima
15:46:41 smoke TLS_J17136_P07_1_1.tiff: This is a colorful micrograph showing a detailed view of biological tissue, likely stained to highlight different cellular components. The image reveals a compl
15:46:41 smoke TLS_J17136_P08A_1_1.tiff: This is a colorful micrograph showing a detailed, magnified view of biological tissue, likely stained to highlight cellular structures. The image displays a com
15:46:41 smoke TLS_J17136_P08B_1_1.tiff: This is a colorful micrograph showing a detailed view of biological tissue, likely stained to highlight different cellular components. The image reveals intrica
15:46:41 smoke TLS_J17136_P08B_2_1.tiff: This is a colorful micrograph showing a dense, textured biological sample with scattered circular and ring-like structures. The image appears to be a stained ti
16:01:24 captions done: 12880 new, 0 earlier
16:16:40 abstracts done: 2597 new, 0 earlier
```

## Session 18, jina-embeddings-v4 (cache jina-embeddings-v4_s11)

### Reproduction check

- title a: 0 of 2597 ranks differ from descq_ranks_e1.jsonl
- title c: 0 of 2597 ranks differ from descq_ranks_e1.jsonl
- title d: 0 of 2597 ranks differ from descq_ranks_e1.jsonl
- desc a: 0 of 2399 ranks differ from descq_ranks_e1.jsonl
- desc c: 0 of 2399 ranks differ from descq_ranks_e1.jsonl
- desc d: 0 of 2399 ranks differ from descq_ranks_e1.jsonl

Reproduced: a, c and d equal descq.py rank for rank.

### Generated texts

- Summarizer Qwen/Qwen3-VL-8B-Instruct (revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b); describer mistral-community/pixtral-12b (revision c2756cbbb9422eba9f6c5c439a214b0392dfc998).
- Abstracts: 2597 folders; characters median / max: L1 1532 / 3690, L0 217 / 256, with names 1679 / 3822; empty: L1 0, L0 0, with names 0; L1 or L0 with a digit: 0.
- Captions: 12880 (0 empty); under this encoder 12880 image-input vectors replaced by their caption in ta, tc, td, 0 kept (no caption).
- Member descriptions: 3959 ({'P1': 1959, 'M1': 2000}); empty 0; name tokens removed in 790 (1394 tokens).
- Folders ranked: 2597. Mean representative vectors per folder: a 1.00, c 5.20, d 9.87, s1 1.00, s0 1.00, sw1 1.00, s1c 6.20, ta 1.00, tc 5.20, td 9.87.

### Q_title (record titles): 2597 queries

Recall@5:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2597 | 1814 | 0.658 | 0.792 | 0.794 | 0.796 | 0.749 | 0.816 | 0.816 | 0.653 | 0.789 | 0.792 | 0.746 | 0.373 |
| text-heavy | 1215 | 1041 | 0.718 | 0.796 | 0.796 | 0.812 | 0.786 | 0.843 | 0.822 | 0.712 | 0.790 | 0.792 | 0.727 | 0.301 |
| image-heavy | 1382 | 813 | 0.606 | 0.788 | 0.792 | 0.781 | 0.716 | 0.792 | 0.811 | 0.601 | 0.789 | 0.792 | 0.763 | 0.436 |

Recall@1:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2597 | 1814 | 0.484 | 0.659 | 0.666 | 0.655 | 0.608 | 0.677 | 0.686 | 0.483 | 0.658 | 0.669 | 0.662 | 0.288 |
| text-heavy | 1215 | 1041 | 0.562 | 0.663 | 0.680 | 0.687 | 0.664 | 0.709 | 0.694 | 0.565 | 0.669 | 0.682 | 0.640 | 0.198 |
| image-heavy | 1382 | 813 | 0.415 | 0.655 | 0.653 | 0.627 | 0.559 | 0.649 | 0.679 | 0.411 | 0.649 | 0.657 | 0.682 | 0.367 |

Recall@10:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2597 | 1814 | 0.713 | 0.828 | 0.831 | 0.827 | 0.788 | 0.851 | 0.851 | 0.714 | 0.827 | 0.831 | 0.772 | 0.414 |
| text-heavy | 1215 | 1041 | 0.766 | 0.840 | 0.840 | 0.849 | 0.829 | 0.884 | 0.864 | 0.760 | 0.838 | 0.844 | 0.759 | 0.360 |
| image-heavy | 1382 | 813 | 0.666 | 0.818 | 0.823 | 0.807 | 0.753 | 0.821 | 0.839 | 0.674 | 0.817 | 0.819 | 0.784 | 0.462 |

Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of first-creator families):

| pair | all | text-heavy | image-heavy |
|---|---|---|---|
| s1 - c | +0.004 [-0.026, +0.032] | +0.016 [-0.014, +0.043] | -0.007 [-0.049, +0.038] |
| s1 - a | +0.138 [+0.114, +0.161] | +0.095 [+0.069, +0.121] | +0.176 [+0.136, +0.209] |
| c - a | +0.134 [+0.098, +0.178] | +0.078 [+0.051, +0.106] | +0.182 [+0.123, +0.243] |
| s0 - c | -0.043 [-0.076, -0.007] | -0.010 [-0.041, +0.018] | -0.072 [-0.119, -0.014] |
| sw1 - s1 | +0.020 [+0.009, +0.032] | +0.030 [+0.016, +0.044] | +0.010 [-0.006, +0.027] |
| s1c - c | +0.025 [+0.018, +0.033] | +0.026 [+0.017, +0.036] | +0.023 [+0.014, +0.037] |
| s1c - s1 | +0.020 [-0.003, +0.046] | +0.010 [-0.014, +0.037] | +0.030 [-0.007, +0.066] |
| d - c | +0.002 [-0.003, +0.008] | +0.000 [-0.008, +0.008] | +0.004 [-0.002, +0.012] |
| ta - a | -0.005 [-0.016, +0.007] | -0.006 [-0.017, +0.006] | -0.004 [-0.021, +0.018] |
| tc - ta | +0.136 [+0.098, +0.187] | +0.078 [+0.052, +0.107] | +0.187 [+0.123, +0.257] |
| tc - c | -0.002 [-0.009, +0.005] | -0.006 [-0.014, +0.002] | +0.001 [-0.012, +0.013] |
| td - d | -0.002 [-0.008, +0.004] | -0.004 [-0.011, +0.003] | -0.001 [-0.012, +0.010] |
| bm25 - s1 | -0.050 [-0.104, +0.018] | -0.086 [-0.129, -0.037] | -0.019 [-0.111, +0.079] |
| fn - s1 | -0.423 [-0.528, -0.294] | -0.511 [-0.547, -0.472] | -0.346 [-0.545, -0.146] |

One folder per creator family (drawn with seed 20261019), and the four digitization series apart (recall@5 differences, clustered intervals):

| cell | subset | queries | families | s1 - c | c - a | s1 - a |
|---|---|---:|---:|---|---|---|
| all | one folder per family | 1814 | 1814 | +0.038 [+0.022, +0.053] | +0.114 [+0.096, +0.132] | +0.152 [+0.132, +0.171] |
| all | the four series | 396 | 4 | -0.096 [-0.143, -0.008] | +0.227 [+0.011, +0.349] | +0.131 [-0.032, +0.206] |
| all | without the four series | 2201 | 1810 | +0.022 [+0.004, +0.040] | +0.117 [+0.099, +0.137] | +0.139 [+0.119, +0.160] |
| text-heavy | one folder per family | 1041 | 1041 | +0.033 [+0.012, +0.054] | +0.065 [+0.043, +0.086] | +0.098 [+0.073, +0.123] |
| text-heavy | the four series | 0 | 0 |  |  |  |
| text-heavy | without the four series | 1215 | 1041 | +0.016 [-0.014, +0.043] | +0.078 [+0.051, +0.106] | +0.095 [+0.069, +0.121] |
| image-heavy | one folder per family | 813 | 813 | +0.042 [+0.020, +0.064] | +0.178 [+0.146, +0.209] | +0.220 [+0.188, +0.253] |
| image-heavy | the four series | 396 | 4 | -0.096 [-0.143, -0.008] | +0.227 [+0.011, +0.349] | +0.131 [-0.032, +0.206] |
| image-heavy | without the four series | 986 | 809 | +0.029 [+0.005, +0.055] | +0.164 [+0.135, +0.195] | +0.194 [+0.157, +0.229] |

### Q_desc (title and description): 2399 queries

Recall@5:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2399 | 1705 | 0.708 | 0.850 | 0.854 | 0.850 | 0.824 | 0.866 | 0.880 | 0.700 | 0.846 | 0.850 | 0.784 | 0.473 |
| text-heavy | 1156 | 986 | 0.797 | 0.843 | 0.845 | 0.882 | 0.866 | 0.899 | 0.874 | 0.796 | 0.842 | 0.844 | 0.763 | 0.471 |
| image-heavy | 1243 | 753 | 0.626 | 0.857 | 0.862 | 0.819 | 0.784 | 0.836 | 0.886 | 0.611 | 0.850 | 0.854 | 0.804 | 0.475 |

Recall@1:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2399 | 1705 | 0.563 | 0.729 | 0.739 | 0.721 | 0.682 | 0.737 | 0.759 | 0.570 | 0.728 | 0.737 | 0.685 | 0.371 |
| text-heavy | 1156 | 986 | 0.676 | 0.728 | 0.740 | 0.776 | 0.743 | 0.806 | 0.758 | 0.684 | 0.728 | 0.740 | 0.667 | 0.354 |
| image-heavy | 1243 | 753 | 0.458 | 0.730 | 0.738 | 0.670 | 0.625 | 0.672 | 0.761 | 0.464 | 0.728 | 0.734 | 0.702 | 0.386 |

Recall@10:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2399 | 1705 | 0.764 | 0.884 | 0.885 | 0.880 | 0.865 | 0.901 | 0.914 | 0.748 | 0.883 | 0.882 | 0.814 | 0.512 |
| text-heavy | 1156 | 986 | 0.837 | 0.875 | 0.878 | 0.906 | 0.900 | 0.928 | 0.910 | 0.830 | 0.878 | 0.881 | 0.800 | 0.514 |
| image-heavy | 1243 | 753 | 0.696 | 0.892 | 0.892 | 0.857 | 0.832 | 0.876 | 0.917 | 0.672 | 0.888 | 0.883 | 0.827 | 0.511 |

Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of first-creator families):

| pair | all | text-heavy | image-heavy |
|---|---|---|---|
| s1 - c | -0.000 [-0.046, +0.044] | +0.040 [+0.015, +0.062] | -0.038 [-0.098, +0.038] |
| s1 - a | +0.141 [+0.102, +0.179] | +0.086 [+0.064, +0.107] | +0.193 [+0.122, +0.251] |
| c - a | +0.142 [+0.087, +0.211] | +0.046 [+0.023, +0.070] | +0.231 [+0.141, +0.323] |
| s0 - c | -0.026 [-0.069, +0.019] | +0.023 [-0.000, +0.046] | -0.072 [-0.131, +0.004] |
| sw1 - s1 | +0.017 [+0.007, +0.026] | +0.016 [+0.004, +0.028] | +0.017 [+0.001, +0.034] |
| s1c - c | +0.030 [+0.021, +0.040] | +0.031 [+0.021, +0.041] | +0.029 [+0.018, +0.045] |
| s1c - s1 | +0.030 [-0.008, +0.070] | -0.009 [-0.028, +0.012] | +0.067 [+0.001, +0.119] |
| d - c | +0.004 [-0.000, +0.008] | +0.003 [-0.003, +0.009] | +0.005 [-0.001, +0.012] |
| ta - a | -0.008 [-0.025, +0.009] | -0.001 [-0.011, +0.009] | -0.015 [-0.041, +0.015] |
| tc - ta | +0.146 [+0.085, +0.229] | +0.046 [+0.024, +0.068] | +0.239 [+0.131, +0.352] |
| tc - c | -0.004 [-0.010, +0.001] | -0.001 [-0.006, +0.004] | -0.007 [-0.017, +0.001] |
| td - d | -0.004 [-0.008, -0.000] | -0.001 [-0.006, +0.004] | -0.007 [-0.015, -0.001] |
| bm25 - s1 | -0.065 [-0.125, -0.005] | -0.119 [-0.162, -0.077] | -0.015 [-0.115, +0.067] |
| fn - s1 | -0.377 [-0.467, -0.262] | -0.412 [-0.457, -0.364] | -0.344 [-0.513, -0.170] |

One folder per creator family (drawn with seed 20261019), and the four digitization series apart (recall@5 differences, clustered intervals):

| cell | subset | queries | families | s1 - c | c - a |
|---|---|---:|---:|---|---|
| all | one folder per family | 1705 | 1705 | +0.053 [+0.039, +0.070] | +0.101 [+0.084, +0.119] |
| all | the four series | 324 | 4 | -0.244 [-0.367, -0.105] | +0.386 [+0.022, +0.526] |
| all | without the four series | 2075 | 1701 | +0.038 [+0.021, +0.055] | +0.104 [+0.086, +0.122] |
| text-heavy | one folder per family | 986 | 986 | +0.055 [+0.035, +0.075] | +0.034 [+0.015, +0.054] |
| text-heavy | the four series | 0 | 0 |  |  |
| text-heavy | without the four series | 1156 | 986 | +0.040 [+0.015, +0.062] | +0.046 [+0.023, +0.070] |
| image-heavy | one folder per family | 753 | 753 | +0.044 [+0.020, +0.068] | +0.197 [+0.166, +0.230] |
| image-heavy | the four series | 324 | 4 | -0.244 [-0.367, -0.105] | +0.386 [+0.022, +0.526] |
| image-heavy | without the four series | 919 | 749 | +0.035 [+0.013, +0.059] | +0.176 [+0.146, +0.206] |

### Q_mem (one-sentence descriptions of member images; the image stays in its folder): 3959 queries

Recall@5:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 1959 | 731 | 0.490 | 0.781 | 0.785 | 0.490 | 0.357 | 0.484 | 0.781 | 0.481 | 0.727 | 0.734 | 0.560 | 0.061 |
| M1 | 2000 | 492 | 0.663 | 0.732 | 0.767 | 0.458 | 0.320 | 0.454 | 0.732 | 0.655 | 0.707 | 0.721 | 0.731 | 0.031 |

Recall@1:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 1959 | 731 | 0.352 | 0.630 | 0.645 | 0.351 | 0.237 | 0.344 | 0.629 | 0.340 | 0.589 | 0.597 | 0.419 | 0.022 |
| M1 | 2000 | 492 | 0.483 | 0.531 | 0.608 | 0.303 | 0.181 | 0.303 | 0.531 | 0.483 | 0.533 | 0.561 | 0.549 | 0.011 |

Recall@10:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 1959 | 731 | 0.552 | 0.840 | 0.838 | 0.549 | 0.418 | 0.541 | 0.841 | 0.546 | 0.786 | 0.792 | 0.630 | 0.088 |
| M1 | 2000 | 492 | 0.746 | 0.798 | 0.827 | 0.534 | 0.390 | 0.522 | 0.799 | 0.724 | 0.768 | 0.782 | 0.799 | 0.051 |

Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of first-creator families):

| pair | P1 | M1 |
|---|---|---|
| c - s1 | +0.291 [+0.259, +0.322] | +0.274 [+0.239, +0.313] |
| c - a | +0.290 [+0.260, +0.324] | +0.069 [+0.043, +0.100] |
| c - s0 | +0.424 [+0.392, +0.461] | +0.411 [+0.363, +0.464] |
| sw1 - s1 | -0.006 [-0.025, +0.014] | -0.004 [-0.022, +0.014] |
| s1c - c | +0.001 [+0.000, +0.002] | +0.000 [+0.000, +0.000] |
| s1c - s1 | +0.291 [+0.260, +0.323] | +0.274 [+0.239, +0.313] |
| d - c | +0.005 [-0.006, +0.014] | +0.035 [+0.021, +0.050] |
| ta - a | -0.009 [-0.020, +0.001] | -0.008 [-0.030, +0.013] |
| tc - ta | +0.247 [+0.220, +0.277] | +0.051 [+0.035, +0.072] |
| tc - c | -0.053 [-0.075, -0.032] | -0.025 [-0.046, -0.005] |
| td - d | -0.051 [-0.073, -0.028] | -0.046 [-0.067, -0.025] |
| bm25 - c | -0.220 [-0.255, -0.190] | -0.001 [-0.031, +0.032] |
| fn - c | -0.719 [-0.767, -0.673] | -0.701 [-0.778, -0.611] |

One folder per creator family (drawn with seed 20261019), and the four digitization series apart (recall@5 differences, clustered intervals):

| cell | subset | queries | families | c - s1 | c - a | d - c |
|---|---|---:|---:|---|---|---|
| P1 | one folder per family | 1769 | 731 | +0.295 [+0.260, +0.330] | +0.297 [+0.265, +0.332] | +0.006 [-0.007, +0.017] |
| P1 | the four series | 0 | 0 |  |  |  |
| P1 | without the four series | 1959 | 731 | +0.291 [+0.259, +0.322] | +0.290 [+0.260, +0.324] | +0.005 [-0.006, +0.014] |
| M1 | one folder per family | 1548 | 492 | +0.276 [+0.236, +0.318] | +0.077 [+0.048, +0.109] | +0.039 [+0.022, +0.058] |
| M1 | the four series | 352 | 4 | +0.244 [+0.130, +0.358] | +0.060 [+0.013, +0.146] | +0.020 [+0.000, +0.027] |
| M1 | without the four series | 1648 | 488 | +0.280 [+0.240, +0.318] | +0.070 [+0.039, +0.099] | +0.039 [+0.021, +0.055] |

H18a (jina-embeddings-v4): s1 - c on Q_title, image-heavy folders, recall@5 = -0.007 [-0.049, +0.038] over 1382 queries and 813 families: outcome 'between'.
H18b (jina-embeddings-v4): Q_mem P1, 1959 queries and 731 families; gate d = 0.785 >= 0.25 (passed); c - s1 = +0.291 [+0.259, +0.322] (holds); c - a = +0.290 [+0.260, +0.324] (holds): H18b survives.

## Session 18, gme-Qwen2-VL-2B-Instruct (cache gme-Qwen2-VL-2B-Instruct_s11)

### Reproduction check

- title a: 0 of 2597 ranks differ from descq_ranks_e3.jsonl
- title c: 0 of 2597 ranks differ from descq_ranks_e3.jsonl
- title d: 0 of 2597 ranks differ from descq_ranks_e3.jsonl
- desc a: 0 of 2399 ranks differ from descq_ranks_e3.jsonl
- desc c: 0 of 2399 ranks differ from descq_ranks_e3.jsonl
- desc d: 0 of 2399 ranks differ from descq_ranks_e3.jsonl

Reproduced: a, c and d equal descq.py rank for rank.

### Generated texts

- Summarizer Qwen/Qwen3-VL-8B-Instruct (revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b); describer mistral-community/pixtral-12b (revision c2756cbbb9422eba9f6c5c439a214b0392dfc998).
- Abstracts: 2597 folders; characters median / max: L1 1532 / 3690, L0 217 / 256, with names 1679 / 3822; empty: L1 0, L0 0, with names 0; L1 or L0 with a digit: 0.
- Captions: 12880 (0 empty); under this encoder 12880 image-input vectors replaced by their caption in ta, tc, td, 0 kept (no caption).
- Member descriptions: 3959 ({'P1': 1959, 'M1': 2000}); empty 0; name tokens removed in 790 (1394 tokens).
- Folders ranked: 2597. Mean representative vectors per folder: a 1.00, c 5.20, d 9.87, s1 1.00, s0 1.00, sw1 1.00, s1c 6.20, ta 1.00, tc 5.20, td 9.87.

### Q_title (record titles): 2597 queries

Recall@5:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2597 | 1814 | 0.582 | 0.718 | 0.722 | 0.547 | 0.650 | 0.621 | 0.729 | 0.595 | 0.735 | 0.741 | 0.746 | 0.373 |
| text-heavy | 1215 | 1041 | 0.662 | 0.705 | 0.710 | 0.638 | 0.696 | 0.686 | 0.719 | 0.642 | 0.718 | 0.723 | 0.727 | 0.301 |
| image-heavy | 1382 | 813 | 0.512 | 0.729 | 0.733 | 0.467 | 0.609 | 0.564 | 0.737 | 0.553 | 0.750 | 0.757 | 0.763 | 0.436 |

Recall@1:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2597 | 1814 | 0.399 | 0.569 | 0.578 | 0.382 | 0.475 | 0.438 | 0.581 | 0.410 | 0.582 | 0.591 | 0.662 | 0.288 |
| text-heavy | 1215 | 1041 | 0.508 | 0.554 | 0.571 | 0.453 | 0.528 | 0.502 | 0.570 | 0.498 | 0.563 | 0.574 | 0.640 | 0.198 |
| image-heavy | 1382 | 813 | 0.303 | 0.582 | 0.585 | 0.318 | 0.428 | 0.381 | 0.590 | 0.332 | 0.599 | 0.606 | 0.682 | 0.367 |

Recall@10:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2597 | 1814 | 0.658 | 0.763 | 0.769 | 0.622 | 0.701 | 0.688 | 0.776 | 0.662 | 0.782 | 0.784 | 0.772 | 0.414 |
| text-heavy | 1215 | 1041 | 0.714 | 0.759 | 0.771 | 0.709 | 0.750 | 0.756 | 0.775 | 0.703 | 0.773 | 0.775 | 0.759 | 0.360 |
| image-heavy | 1382 | 813 | 0.609 | 0.767 | 0.767 | 0.545 | 0.658 | 0.628 | 0.776 | 0.627 | 0.790 | 0.792 | 0.784 | 0.462 |

Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of first-creator families):

| pair | all | text-heavy | image-heavy |
|---|---|---|---|
| s1 - c | -0.171 [-0.285, -0.076] | -0.067 [-0.109, -0.033] | -0.263 [-0.433, -0.096] |
| s1 - a | -0.035 [-0.096, +0.025] | -0.024 [-0.051, +0.003] | -0.045 [-0.136, +0.070] |
| c - a | +0.136 [+0.084, +0.205] | +0.044 [+0.006, +0.088] | +0.218 [+0.140, +0.304] |
| s0 - c | -0.068 [-0.135, -0.006] | -0.009 [-0.054, +0.027] | -0.120 [-0.217, -0.016] |
| sw1 - s1 | +0.074 [+0.053, +0.097] | +0.048 [+0.028, +0.069] | +0.098 [+0.062, +0.129] |
| s1c - c | +0.010 [+0.006, +0.016] | +0.013 [+0.006, +0.021] | +0.008 [+0.003, +0.014] |
| s1c - s1 | +0.182 [+0.089, +0.297] | +0.081 [+0.048, +0.120] | +0.271 [+0.107, +0.437] |
| d - c | +0.004 [-0.000, +0.010] | +0.005 [-0.004, +0.015] | +0.004 [-0.001, +0.010] |
| ta - a | +0.013 [-0.011, +0.041] | -0.020 [-0.035, -0.007] | +0.041 [-0.002, +0.081] |
| tc - ta | +0.141 [+0.105, +0.183] | +0.076 [+0.042, +0.118] | +0.198 [+0.139, +0.249] |
| tc - c | +0.017 [+0.010, +0.026] | +0.012 [+0.003, +0.022] | +0.021 [+0.009, +0.037] |
| td - d | +0.018 [+0.011, +0.028] | +0.012 [+0.004, +0.022] | +0.024 [+0.010, +0.043] |
| bm25 - s1 | +0.199 [+0.106, +0.314] | +0.089 [+0.051, +0.134] | +0.296 [+0.124, +0.463] |
| fn - s1 | -0.174 [-0.298, -0.005] | -0.337 [-0.375, -0.298] | -0.031 [-0.240, +0.205] |

One folder per creator family (drawn with seed 20261019), and the four digitization series apart (recall@5 differences, clustered intervals):

| cell | subset | queries | families | s1 - c | c - a | s1 - a |
|---|---|---:|---:|---|---|---|
| all | one folder per family | 1814 | 1814 | -0.058 [-0.080, -0.037] | +0.091 [+0.070, +0.112] | +0.033 [+0.010, +0.055] |
| all | the four series | 396 | 4 | -0.667 [-0.851, -0.178] | +0.348 [+0.085, +0.502] | -0.318 [-0.702, -0.013] |
| all | without the four series | 2201 | 1810 | -0.082 [-0.110, -0.058] | +0.098 [+0.076, +0.123] | +0.016 [-0.008, +0.038] |
| text-heavy | one folder per family | 1041 | 1041 | -0.038 [-0.065, -0.012] | +0.023 [-0.002, +0.048] | -0.015 [-0.042, +0.013] |
| text-heavy | the four series | 0 | 0 |  |  |  |
| text-heavy | without the four series | 1215 | 1041 | -0.067 [-0.109, -0.033] | +0.044 [+0.006, +0.088] | -0.024 [-0.051, +0.003] |
| image-heavy | one folder per family | 813 | 813 | -0.090 [-0.121, -0.057] | +0.180 [+0.145, +0.213] | +0.090 [+0.057, +0.121] |
| image-heavy | the four series | 396 | 4 | -0.667 [-0.851, -0.178] | +0.348 [+0.085, +0.502] | -0.318 [-0.702, -0.013] |
| image-heavy | without the four series | 986 | 809 | -0.100 [-0.133, -0.067] | +0.165 [+0.134, +0.199] | +0.065 [+0.026, +0.103] |

### Q_desc (title and description): 2399 queries

Recall@5:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2399 | 1705 | 0.662 | 0.776 | 0.780 | 0.665 | 0.752 | 0.728 | 0.801 | 0.686 | 0.788 | 0.796 | 0.784 | 0.473 |
| text-heavy | 1156 | 986 | 0.723 | 0.755 | 0.762 | 0.762 | 0.804 | 0.795 | 0.789 | 0.714 | 0.765 | 0.770 | 0.763 | 0.471 |
| image-heavy | 1243 | 753 | 0.606 | 0.795 | 0.797 | 0.575 | 0.705 | 0.666 | 0.812 | 0.660 | 0.809 | 0.821 | 0.804 | 0.475 |

Recall@1:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2399 | 1705 | 0.495 | 0.644 | 0.650 | 0.486 | 0.591 | 0.563 | 0.673 | 0.511 | 0.657 | 0.667 | 0.685 | 0.371 |
| text-heavy | 1156 | 986 | 0.580 | 0.616 | 0.631 | 0.579 | 0.651 | 0.642 | 0.658 | 0.571 | 0.630 | 0.649 | 0.667 | 0.354 |
| image-heavy | 1243 | 753 | 0.417 | 0.671 | 0.669 | 0.399 | 0.536 | 0.489 | 0.687 | 0.455 | 0.683 | 0.685 | 0.702 | 0.386 |

Recall@10:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 2399 | 1705 | 0.729 | 0.831 | 0.829 | 0.727 | 0.798 | 0.787 | 0.846 | 0.738 | 0.840 | 0.846 | 0.814 | 0.512 |
| text-heavy | 1156 | 986 | 0.776 | 0.826 | 0.825 | 0.823 | 0.848 | 0.849 | 0.843 | 0.758 | 0.833 | 0.833 | 0.800 | 0.514 |
| image-heavy | 1243 | 753 | 0.685 | 0.836 | 0.833 | 0.639 | 0.752 | 0.729 | 0.849 | 0.720 | 0.847 | 0.858 | 0.827 | 0.511 |

Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of first-creator families):

| pair | all | text-heavy | image-heavy |
|---|---|---|---|
| s1 - c | -0.110 [-0.229, -0.008] | +0.007 [-0.025, +0.037] | -0.220 [-0.377, -0.034] |
| s1 - a | +0.003 [-0.069, +0.075] | +0.039 [+0.015, +0.066] | -0.031 [-0.137, +0.107] |
| c - a | +0.113 [+0.069, +0.163] | +0.032 [+0.002, +0.062] | +0.189 [+0.123, +0.250] |
| s0 - c | -0.023 [-0.079, +0.036] | +0.048 [+0.015, +0.080] | -0.090 [-0.166, +0.009] |
| sw1 - s1 | +0.063 [+0.033, +0.101] | +0.033 [+0.016, +0.050] | +0.091 [+0.035, +0.145] |
| s1c - c | +0.025 [+0.017, +0.034] | +0.034 [+0.023, +0.046] | +0.017 [+0.009, +0.028] |
| s1c - s1 | +0.135 [+0.037, +0.250] | +0.027 [+0.001, +0.056] | +0.237 [+0.057, +0.390] |
| d - c | +0.005 [-0.001, +0.010] | +0.007 [-0.002, +0.016] | +0.002 [-0.004, +0.009] |
| ta - a | +0.024 [-0.005, +0.056] | -0.010 [-0.022, +0.003] | +0.055 [+0.006, +0.101] |
| tc - ta | +0.102 [+0.077, +0.122] | +0.051 [+0.022, +0.082] | +0.149 [+0.119, +0.176] |
| tc - c | +0.012 [+0.005, +0.020] | +0.010 [+0.001, +0.019] | +0.014 [+0.004, +0.027] |
| td - d | +0.016 [+0.008, +0.025] | +0.008 [-0.001, +0.017] | +0.023 [+0.012, +0.040] |
| bm25 - s1 | +0.119 [+0.014, +0.236] | +0.001 [-0.041, +0.042] | +0.228 [+0.054, +0.382] |
| fn - s1 | -0.193 [-0.312, -0.033] | -0.292 [-0.339, -0.243] | -0.101 [-0.316, +0.137] |

One folder per creator family (drawn with seed 20261019), and the four digitization series apart (recall@5 differences, clustered intervals):

| cell | subset | queries | families | s1 - c | c - a |
|---|---|---:|---:|---|---|
| all | one folder per family | 1705 | 1705 | +0.011 [-0.008, +0.031] | +0.073 [+0.052, +0.093] |
| all | the four series | 324 | 4 | -0.762 [-0.852, -0.538] | +0.333 [+0.123, +0.379] |
| all | without the four series | 2075 | 1701 | -0.009 [-0.033, +0.014] | +0.079 [+0.059, +0.099] |
| text-heavy | one folder per family | 986 | 986 | +0.028 [+0.003, +0.052] | +0.016 [-0.007, +0.042] |
| text-heavy | the four series | 0 | 0 |  |  |
| text-heavy | without the four series | 1156 | 986 | +0.007 [-0.025, +0.037] | +0.032 [+0.002, +0.062] |
| image-heavy | one folder per family | 753 | 753 | -0.011 [-0.041, +0.021] | +0.143 [+0.108, +0.181] |
| image-heavy | the four series | 324 | 4 | -0.762 [-0.840, -0.538] | +0.333 [+0.123, +0.379] |
| image-heavy | without the four series | 919 | 749 | -0.028 [-0.065, +0.006] | +0.138 [+0.107, +0.169] |

### Q_mem (one-sentence descriptions of member images; the image stays in its folder): 3959 queries

Recall@5:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 1959 | 731 | 0.457 | 0.747 | 0.751 | 0.404 | 0.322 | 0.408 | 0.748 | 0.412 | 0.772 | 0.780 | 0.560 | 0.061 |
| M1 | 2000 | 492 | 0.669 | 0.719 | 0.742 | 0.418 | 0.299 | 0.411 | 0.718 | 0.678 | 0.736 | 0.773 | 0.731 | 0.031 |

Recall@1:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 1959 | 731 | 0.323 | 0.587 | 0.606 | 0.266 | 0.198 | 0.261 | 0.587 | 0.292 | 0.630 | 0.645 | 0.419 | 0.022 |
| M1 | 2000 | 492 | 0.462 | 0.531 | 0.563 | 0.257 | 0.172 | 0.245 | 0.531 | 0.483 | 0.556 | 0.598 | 0.549 | 0.011 |

Recall@10:

| cell | queries | families | a | c | d | s1 | s0 | sw1 | s1c | ta | tc | td | bm25 | fn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 1959 | 731 | 0.520 | 0.818 | 0.818 | 0.465 | 0.375 | 0.467 | 0.818 | 0.481 | 0.823 | 0.835 | 0.630 | 0.088 |
| M1 | 2000 | 492 | 0.753 | 0.788 | 0.811 | 0.499 | 0.365 | 0.493 | 0.787 | 0.750 | 0.799 | 0.824 | 0.799 | 0.051 |

Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of first-creator families):

| pair | P1 | M1 |
|---|---|---|
| c - s1 | +0.344 [+0.310, +0.380] | +0.300 [+0.260, +0.341] |
| c - a | +0.290 [+0.259, +0.322] | +0.049 [+0.022, +0.080] |
| c - s0 | +0.425 [+0.391, +0.463] | +0.419 [+0.366, +0.474] |
| sw1 - s1 | +0.004 [-0.017, +0.025] | -0.007 [-0.032, +0.021] |
| s1c - c | +0.001 [-0.003, +0.004] | -0.001 [-0.004, +0.001] |
| s1c - s1 | +0.344 [+0.310, +0.381] | +0.299 [+0.258, +0.340] |
| d - c | +0.004 [-0.007, +0.015] | +0.024 [+0.009, +0.039] |
| ta - a | -0.045 [-0.060, -0.027] | +0.009 [-0.008, +0.030] |
| tc - ta | +0.359 [+0.325, +0.398] | +0.058 [+0.036, +0.081] |
| tc - c | +0.025 [+0.001, +0.050] | +0.018 [-0.006, +0.043] |
| td - d | +0.029 [+0.006, +0.050] | +0.031 [+0.005, +0.059] |
| bm25 - c | -0.187 [-0.219, -0.157] | +0.012 [-0.019, +0.050] |
| fn - c | -0.686 [-0.736, -0.632] | -0.688 [-0.759, -0.607] |

One folder per creator family (drawn with seed 20261019), and the four digitization series apart (recall@5 differences, clustered intervals):

| cell | subset | queries | families | c - s1 | c - a | d - c |
|---|---|---:|---:|---|---|---|
| P1 | one folder per family | 1769 | 731 | +0.352 [+0.316, +0.388] | +0.301 [+0.270, +0.333] | +0.005 [-0.008, +0.018] |
| P1 | the four series | 0 | 0 |  |  |  |
| P1 | without the four series | 1959 | 731 | +0.344 [+0.310, +0.380] | +0.290 [+0.259, +0.322] | +0.004 [-0.007, +0.015] |
| M1 | one folder per family | 1548 | 492 | +0.299 [+0.255, +0.341] | +0.055 [+0.021, +0.090] | +0.030 [+0.014, +0.045] |
| M1 | the four series | 352 | 4 | +0.276 [+0.019, +0.439] | +0.043 [+0.013, +0.098] | -0.011 [-0.036, +0.000] |
| M1 | without the four series | 1648 | 488 | +0.305 [+0.260, +0.346] | +0.050 [+0.018, +0.083] | +0.031 [+0.014, +0.047] |

H18a (gme-Qwen2-VL-2B-Instruct): s1 - c on Q_title, image-heavy folders, recall@5 = -0.263 [-0.433, -0.096] over 1382 queries and 813 families: outcome 'below c'.
H18b (gme-Qwen2-VL-2B-Instruct): Q_mem P1, 1959 queries and 731 families; gate d = 0.751 >= 0.25 (passed); c - s1 = +0.344 [+0.310, +0.380] (holds); c - a = +0.290 [+0.259, +0.322] (holds): H18b survives.
