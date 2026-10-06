# dirvec session 10: the same-modality dilution control

> **Errata, added 2026-10-01 after the number audit (reports/number_audit_2026-10-01.md). The text and
> tables below are unchanged; where a sentence and a verbatim table disagree, the table is right.**
> - "c and cc lose nothing in either set (within 0.02 of d)" on guest queries: c is -0.024 in CROSS and
>   cc +0.021 in SAME. Within 0.025.
> - "both synthetic losses are twice the natural one": the SAME loss (0.500) is twice the natural 0.241
>   to 0.253; the CROSS loss (0.707) is 2.8 to 2.9 times it.
> - Reading the summary: 0.500 and 0.707 are over each set's own hosts (19 and 11); 0.583 and 0.763,
>   their difference +0.180 and the "three quarters" (76 percent) are over the 10 hosts common to both
>   sets. Do not mix the two subsets. The labelled pair's SAME loss (b2 0.521) is larger than the
>   pooled centroid's (0.500), not equal to it.
> - The natural loss d - a in P1 on the evaluation split, "0.241", is computed from rounded recall
>   values; the verbatim x - d table (results/session9.md, results/session13_outputs.md) prints 0.242.


Question: is the minority-modality loss under a pooled centroid (session 3, sessions 5 to 9) a
modality effect, or plain count dilution that any minority of the same size would produce? Session 9
could not separate the two on natural folders because blind k-means recovers the modality partition
(purity 0.88 to 0.99). This session builds the control the prior-art report names
(`reports/prior_art_2026-09-30.md`, objection table, first row): a minority of the same input group,
at the same fraction, from the same kind of foreign source (another single-group Zenodo record),
against a minority of the other input group.
Same set, cache, encoder, input rules, ground truth, calibration split and centering means as
sessions 8 and 9. No download, no GPU, no new encoder. CPU only (MIG 1g.24gb pod, 3.4 vCPUs by
cgroup; numpy 2.5.2, scikit-learn 1.9.1), `DIRVEC_THREADS`, `OMP_NUM_THREADS` and
`OPENBLAS_NUM_THREADS` set to 3.

## Hypothesis (fixed now, do not edit after the first eval run), copied verbatim from BRIEF.md

## Hypothesis (fixed now, do not edit after the first eval run)
H10 (modality, beyond dilution): on guest queries the pooled centroid a loses more against d when
the guest is of the other input group than when it is of the same input group at the same
fraction: loss_CROSS(a) - loss_SAME(a) > 0. Kill: H10 is dead if the paired 95 percent interval
over hosts of loss_CROSS(a) - loss_SAME(a) includes zero. Report the two losses themselves and the
same difference for ac (centering may account for part of it).
Secondary, reported, no kill: the same difference for tb2, tb2c, b2 and bc2 (does a second
representative recover a same-modality guest as well as a cross-modality one); host-query losses
in both sets (what the guest costs the host); losses by fraction bin; the same-folder cosine host-
guest in both sets next to the session 9 within-group and cross-group numbers; the number of
hosts, guests and queries per set; vectors per folder.

## Changes to the scripts (defaults unchanged)

`scripts/synth.py` (new) builds the two sets. `scripts/eval.py`: `calib_split()` factored out of
`centered_space()` (synth.py imports it, so the hosts are evaluation-split directories under the
session 8 split); `--split-dirs` (the dirs file the calibration split is drawn from; the session 5
file is passed with a synthetic dirs file, so the split, the in-calibration file mask and the group
means mu_img and mu_txt are the session 8 ones: guests come from evaluation-split directories only,
so no calibration file changes directory); `--s10` (the session 10 cells and tables, replacing the
session 3, 8 and 9 sections); `--s10-pair <ranks file of the other set>` (the paired difference of
the losses over the hosts common to both sets, and the H10 line when the run is CROSS against SAME).
The representation names are the existing ones (a, ac, b2, bc2, tb2, tb2c, c, cc, d, dc).

Implementation choices not fixed by the brief, written down before the eval run:
- Embedded file: a cache row with ok = true. Hosts and donors are judged on embedded files; guest
  files are drawn from the donor's embedded files, and the donor's other files leave the candidate
  list with the donor directory (the manifest rows keep the donor as their dir, and the donor is not
  in the synthetic dirs file, so eval.py never builds a folder for them).
- n_G = max(2, round(f * n_H / (1 - f))) with f drawn once per host from U[0.2, 0.5) (seed 20261001,
  one stream, hosts in a seeded random order); the realised fraction n_G / (n_H + n_G) is the one
  reported and binned ([0.2, 0.35) and [0.35, 0.5], the upper bin closed because rounding can land
  exactly on 0.5).
- Donor rule: the pool for a host and a set is the single-group evaluation-split directories of the
  required group with at least n_G embedded files, other than the host, that have not donated in
  either set and have not received a guest in either set. Directories with fewer than 6 embedded
  files (never hosts) are preferred, uniformly at random; the rest of the pool is used when there
  are none. A directory that donates is never a host, so the hosts are the same in both sets unless
  a pool ran dry. Guest files are a uniform draw without replacement from the donor's embedded files.
- The host's dirs row gets the synthetic counts and image_frac (its bucket field in the ground truth
  is the synthetic folder's); nothing in this session uses the buckets.
- Queries of a synthetic folder: its embedded files that are queries in `data/gt_structural_s5.jsonl`
  (the session 5 dedupe exclusions kept), marked host or guest. Leave-one-out as before: a guest query
  is scored against its host built from the other n_G - 1 guest files and the host's own files.
- Bootstrap: 1000 resamples of hosts, seed per cell; the cross-set difference resamples the hosts
  common to both sets for that cell (a host is in a cell when it has queries of that cell in both sets).

## Set construction (`scripts/synth.py`, no eval number read before the reproduction check)

The definitions allow far fewer hosts than the brief hoped for. The session 5 set was selected for
mixed folders: of the 2,246 evaluation-split directories, 2,149 have both input groups. Only 97 are
single-group (33 image-input, 64 text-input), and only 31 of those have at least 6 embedded files
(13 image, 18 text). Donors come from the same 97 directories, so the two sets consume each other's
material.

| | SAME | CROSS |
|---|---:|---:|
| hosts with queries | 20 (7 image-input, 13 text-input) | 16 (7 image, 9 text) |
| donor directories (one per host) | 20 | 16 |
| guest files moved | 102 | 69 |
| queries: host + guest | 176 + 94 | 110 + 41 |
| realised guest fraction: min, median, mean, max | 0.222, 0.337, 0.336, 0.478 | 0.222, 0.348, 0.337, 0.478 |
| hosts per fraction bin [0.2, 0.35) and [0.35, 0.5] | 11, 9 | 8, 8 |
| ranking candidates | 2,788 | 2,792 |

Hosts with a guest in both sets: 16 (fewer than 150; the brief says run anyway, and this run did).
Four hosts have a guest in SAME only, none in CROSS only: all four are text-input hosts whose
CROSS guest would need 5, 6, 5 and 17 image-input files, and no unused image-input directory of that
size was left (33 image-input directories in all, 13 of them hosts). Eleven host-eligible directories
were consumed as donors. The two sets share the 16 paired hosts, their
fractions and their seed; a host's guest file count is the same in both sets.

## Reproduction check (before any synthetic number was read)

`eval.py --criterion s3 --calib 0.2 --reps a,c,d,ac,cc,dc` on the unmodified session 5 files with
the patched script (`ranks_s10repro.jsonl`, `/workspace/logs/s10_repro.md`) gives ranks identical
to `ranks_s8.jsonl` for all six rows on all 18,742 queries; recall@5 over all queries a 0.689,
c 0.783, d 0.783, ac 0.724, cc 0.800, dc 0.801 as in `results/session8.md`.

## Verdict (one run per set: `eval.py ... --split-dirs data/dirs_s5.jsonl --calib 0.2 --s10`, CROSS with `--s10-pair` on the SAME ranks; under a minute each)

Read every interval below with the counts in mind: 10 hosts carry the H10 comparison, 19 and 11
hosts the guest cells of SAME and CROSS. Nothing here is a precise estimate.

**H10 (modality, beyond dilution) survives.** On guest queries, the pooled centroid a loses to d by
0.763 recall@5 when the guest is of the other input group and by 0.583 when it is of the same
input group at the same fraction, over the 10 hosts that have guest queries in both sets:
loss_CROSS(a) - loss_SAME(a) = +0.180 [+0.021, +0.345]. The interval excludes zero, so the kill does
not fire. Over the full guest cells (19 SAME hosts, 11 CROSS hosts) the losses are 0.500 [0.366,
0.614] and 0.707 [0.514, 0.864]. In CROSS not one of the 41 guest queries reaches its host's top 5
under a (recall@5 0.000, recall@10 0.000). For ac the same difference is +0.117 [-0.064, +0.322]
(losses 0.763 and 0.646 on the paired hosts): centering the guest of the other group buys nothing in
CROSS (a and ac are identical there, 0.000) and costs 0.06 in SAME, so the ac difference is two
thirds of the a difference, and its interval includes zero. Centering accounts for about a third of
what a shows; the rest is within the noise of 10 hosts.

**How much of the loss is present with no modality difference at all.** Most of it. A same-modality
minority from another record, at the same fraction, costs the pooled centroid 0.500 recall@5 on the
guest queries (0.583 on the paired hosts); the other-modality minority costs 0.707 (0.763 paired).
Taking the paired numbers, 76 percent of the cross-modality loss is there with no modality
difference; taking the full cells, 71 percent. For comparison the natural minority-modality loss the
paper is about, d - a on the session 5 evaluation split (`results/session8.md`), is 0.241 in P1 and
0.253 in P2: both synthetic losses are twice the natural one, because a guest from another record is
topically foreign as well as a minority. The same-folder cosines say so: host-guest 0.537 uncentered
and 0.063 centered in SAME, 0.419 and 0.023 in CROSS, against 0.727 to 0.766 within host or guest
files (0.40 to 0.55 centered); the natural same-folder image-text cosine is 0.524 uncentered and
0.205 centered (session 9), the natural within-group one 0.72 to 0.77 and 0.46 to 0.57. So the
control is harsher than the natural case on both sides, and the SAME guest is as far from its host
after centering (0.063) as the CROSS guest (0.023), with no modality gap to blame. The pooled
centroid loses any foreign minority of this size; the other-modality one it loses more, by 0.18
recall@5 at these counts.

**Secondary.** The two-vector rows, guest queries, loss (d - x) in SAME and CROSS and the paired
difference over the 10 common hosts:

| rep | SAME loss (19 hosts) | CROSS loss (11 hosts) | CROSS - SAME (10 hosts) |
|---|---|---|---|
| b2 | +0.521 [+0.378, +0.650] | +0.000 [-0.061, +0.073] | -0.604 [-0.786, -0.393] |
| bc2 | +0.649 [+0.508, +0.750] | -0.024 [-0.115, +0.059] | -0.672 [-0.833, -0.465] |
| tb2 | +0.106 [+0.009, +0.231] | +0.024 [-0.051, +0.105] | -0.057 [-0.206, +0.095] |
| tb2c | +0.160 [+0.029, +0.313] | +0.098 [-0.065, +0.261] | -0.061 [-0.353, +0.264] |
| c | +0.011 [-0.025, +0.045] | -0.024 [-0.075, +0.000] | -0.047 [-0.096, +0.002] |
| cc | +0.021 [-0.026, +0.068] | +0.000 [-0.065, +0.083] | -0.042 [-0.093, +0.008] |

- The labelled two-vector rows b2 and bc2 recover the cross-modality guest completely (loss 0.000
  and -0.024 in CROSS) and cannot see a same-modality guest at all: in a single-group folder they
  are one vector, and their SAME loss (0.52, 0.65) is a's (0.50) plus the cost of giving every mixed
  competitor two vectors. The blind two-cluster rows tb2 and tb2c recover most of the guest in both
  sets (SAME loss 0.106 and 0.160, CROSS 0.024 and 0.098), and their CROSS - SAME difference is
  within noise of zero: a second representative found by clustering recovers a same-modality guest
  about as well as a cross-modality one. c and cc lose nothing in either set (within 0.02 of d).
- Host queries: a same-modality guest costs the host nothing (a loss 0.017 [-0.042, +0.087] in
  SAME), a cross-modality guest costs it 0.118 [0.012, 0.218] in CROSS; the paired difference is
  +0.118 [+0.026, +0.238]. The other-group minority pulls the centroid away from the majority as
  well; the same-group one does not, at these fractions.
- By fraction bin (guest queries, a): SAME 0.531 [0.325, 0.714] in [0.2, 0.35) and 0.467 [0.258,
  0.607] in [0.35, 0.5]; CROSS 0.714 (4 hosts, 14 queries) and 0.704 [0.545, 0.833]. Neither set
  shows the loss falling as the guest grows toward half the folder; the bins are too small to say
  more (3 and 7 paired hosts).
- Vectors per folder over all ranked directories: a 1.00, b2 1.96 to 1.97, tb2 2.00, c 5.29 to
  5.30, d 9.74 to 9.76 (a few more than session 9's 2.55, 5.27 and 9.70 because the guest files
  make the synthetic folders larger and the donors leave). Over the synthetic folders: b2 1.00 in
  SAME and 2.00 in CROSS, c 5.75 and 7.56, d 14.80 and 12.31.
- Recall@1 and recall@10 tell the same story (tables below): a on CROSS guest queries is 0.000 at
  every k; on SAME guest queries 0.128 at k = 1 and 0.394 at k = 10 against d's 0.638 and 0.798.

**What this changes in the paper's claim.** The minority-modality loss of a pooled folder vector is
not only a modality effect. The larger part of it, about three quarters at these counts, is what a
pooled vector does to any foreign minority of a fifth to a half of the folder; the modality
difference adds a further 0.18 recall@5 on the minority's own queries and a 0.12 cost on the
majority's, both with intervals that clear zero by little. The finding that survives is the one
session 9 reached from the other side: a folder is two clusters and one vector sits between them;
in this corpus the clusters are the modalities, and per-modality labels are a cheap way to find
them, but blind clustering finds the same split (session 9) and also finds a same-modality minority
that the labels cannot (this session, tb2 and tb2c against b2 and bc2 in SAME).

Caveats, all of them serious: 16 hosts in both sets, 10 in the H10 comparison, 41 CROSS guest
queries; hosts are the only single-group directories of a corpus selected to be mixed, so they are
small records (median guest fraction 0.34 on 6 to 33 files); the guests are topically foreign in a
way a natural minority modality is not, which inflates both losses and may inflate their difference
(a text guest among images differs from its host in topic and in modality, a text guest among texts
in topic only, but the two topic distances need not be equal: the centered host-guest cosines, 0.063
and 0.023, are close but not identical); and the donor rule prefers small donors. The control the
reviewer asked for exists now, with an answer in the expected direction and an interval that would
not survive one or two hosts moving. A larger version needs a corpus with single-group folders of
its own, which the session 11 proposal in BRIEF.md provides for.

## Output, SAME (`/workspace/logs/s10_same.md`, session 10 sections)

### Session 10 set SAME: counts

Hosts (synthetic folders with queries): 20; guest directories: 20; guest files moved: 102; queries: 270 (176 host, 94 guest).
Realised guest fraction over hosts: min 0.222, median 0.337, mean 0.336, max 0.478; hosts per bin: guest frac [0.2,0.35) 11, guest frac [0.35,0.5] 9.
Vectors per folder, all ranked directories: a 1.00, ac 1.00, b2 1.96, bc2 1.96, tb2 2.00, tb2c 2.00, c 5.29, cc 5.29, d 9.76, dc 9.76; synthetic folders: a 1.00, ac 1.00, b2 1.00, bc2 1.00, tb2 2.00, tb2c 2.00, c 5.75, cc 5.75, d 14.80, dc 14.80.

### Session 10 set SAME: same-folder cosine over the synthetic folders (pairs pooled over folders)

| vectors | host-host | guest-guest | host-guest |
|---|---:|---:|---:|
| uncentered | 0.727 (1177) | 0.705 (322) | 0.537 (1337) |
| centered | 0.441 (1177) | 0.399 (322) | 0.063 (1337) |

### Session 10 set SAME: recall@5 per cell and the loss d - x with the paired 95% interval over hosts

| rep | all (270 q, 20 hosts) | guest (94 q, 19 hosts) | host (176 q, 20 hosts) | guest frac [0.2,0.35) (49 q, 10 hosts) | guest frac [0.35,0.5] (45 q, 9 hosts) |
|---|---|---|---|---|---|
| a | 0.656, loss +0.185 [+0.126, +0.252] | 0.266, loss +0.500 [+0.366, +0.614] | 0.864, loss +0.017 [-0.042, +0.087] | 0.286, loss +0.531 [+0.325, +0.714] | 0.244, loss +0.467 [+0.258, +0.607] |
| ac | 0.544, loss +0.296 [+0.237, +0.356] | 0.128, loss +0.638 [+0.500, +0.734] | 0.767, loss +0.114 [+0.043, +0.193] | 0.143, loss +0.673 [+0.480, +0.810] | 0.111, loss +0.600 [+0.419, +0.738] |
| b2 | 0.637, loss +0.204 [+0.133, +0.278] | 0.245, loss +0.521 [+0.378, +0.650] | 0.847, loss +0.034 [-0.035, +0.118] | 0.245, loss +0.571 [+0.386, +0.759] | 0.244, loss +0.467 [+0.231, +0.632] |
| bc2 | 0.519, loss +0.322 [+0.260, +0.387] | 0.117, loss +0.649 [+0.508, +0.750] | 0.733, loss +0.148 [+0.069, +0.241] | 0.143, loss +0.673 [+0.480, +0.810] | 0.089, loss +0.622 [+0.424, +0.774] |
| tb2 | 0.789, loss +0.052 [+0.004, +0.123] | 0.660, loss +0.106 [+0.009, +0.231] | 0.858, loss +0.023 [-0.035, +0.093] | 0.633, loss +0.184 [+0.042, +0.457] | 0.689, loss +0.022 [-0.128, +0.125] |
| tb2c | 0.741, loss +0.100 [+0.040, +0.170] | 0.606, loss +0.160 [+0.029, +0.313] | 0.812, loss +0.068 [+0.006, +0.137] | 0.592, loss +0.224 [+0.061, +0.500] | 0.622, loss +0.089 [-0.128, +0.281] |
| c | 0.837, loss +0.004 [-0.018, +0.028] | 0.755, loss +0.011 [-0.025, +0.045] | 0.881, loss +0.000 [-0.031, +0.036] | 0.816, loss +0.000 [+0.000, +0.000] | 0.689, loss +0.022 [-0.059, +0.085] |
| cc | 0.822, loss +0.019 [-0.015, +0.064] | 0.745, loss +0.021 [-0.026, +0.068] | 0.864, loss +0.017 [-0.031, +0.082] | 0.816, loss +0.000 [-0.059, +0.065] | 0.667, loss +0.044 [-0.045, +0.118] |
| d | 0.841, loss +0.000 [+0.000, +0.000] | 0.766, loss +0.000 [+0.000, +0.000] | 0.881, loss +0.000 [+0.000, +0.000] | 0.816, loss +0.000 [+0.000, +0.000] | 0.711, loss +0.000 [+0.000, +0.000] |
| dc | 0.844, loss -0.004 [-0.021, +0.013] | 0.777, loss -0.011 [-0.064, +0.038] | 0.881, loss +0.000 [+0.000, +0.000] | 0.816, loss +0.000 [-0.059, +0.065] | 0.733, loss -0.022 [-0.105, +0.051] |

### Session 10 set SAME: recall@1 per cell

| rep | all (270 q, 20 hosts) | guest (94 q, 19 hosts) | host (176 q, 20 hosts) | guest frac [0.2,0.35) (49 q, 10 hosts) | guest frac [0.35,0.5] (45 q, 9 hosts) |
|---|---|---|---|---|---|
| a | 0.507 | 0.128 | 0.710 | 0.163 | 0.089 |
| ac | 0.419 | 0.032 | 0.625 | 0.061 | 0.000 |
| b2 | 0.437 | 0.085 | 0.625 | 0.082 | 0.089 |
| bc2 | 0.363 | 0.021 | 0.545 | 0.041 | 0.000 |
| tb2 | 0.652 | 0.500 | 0.733 | 0.490 | 0.511 |
| tb2c | 0.633 | 0.500 | 0.705 | 0.510 | 0.489 |
| c | 0.733 | 0.649 | 0.778 | 0.694 | 0.600 |
| cc | 0.737 | 0.670 | 0.773 | 0.714 | 0.622 |
| d | 0.752 | 0.638 | 0.812 | 0.714 | 0.556 |
| dc | 0.774 | 0.660 | 0.835 | 0.694 | 0.622 |

### Session 10 set SAME: recall@10 per cell

| rep | all (270 q, 20 hosts) | guest (94 q, 19 hosts) | host (176 q, 20 hosts) | guest frac [0.2,0.35) (49 q, 10 hosts) | guest frac [0.35,0.5] (45 q, 9 hosts) |
|---|---|---|---|---|---|
| a | 0.733 | 0.394 | 0.915 | 0.367 | 0.422 |
| ac | 0.626 | 0.223 | 0.841 | 0.224 | 0.222 |
| b2 | 0.696 | 0.330 | 0.892 | 0.306 | 0.356 |
| bc2 | 0.567 | 0.160 | 0.784 | 0.163 | 0.156 |
| tb2 | 0.833 | 0.702 | 0.903 | 0.673 | 0.733 |
| tb2c | 0.781 | 0.638 | 0.858 | 0.592 | 0.689 |
| c | 0.867 | 0.798 | 0.903 | 0.837 | 0.756 |
| cc | 0.852 | 0.798 | 0.881 | 0.857 | 0.733 |
| d | 0.863 | 0.798 | 0.898 | 0.816 | 0.778 |
| dc | 0.881 | 0.819 | 0.915 | 0.837 | 0.800 |

## Output, CROSS (`/workspace/logs/s10_cross.md`, session 10 sections, paired against SAME)

### Session 10 set CROSS: counts

Hosts (synthetic folders with queries): 16; guest directories: 16; guest files moved: 69; queries: 151 (110 host, 41 guest).
Realised guest fraction over hosts: min 0.222, median 0.348, mean 0.337, max 0.478; hosts per bin: guest frac [0.2,0.35) 8, guest frac [0.35,0.5] 8.
Vectors per folder, all ranked directories: a 1.00, ac 1.00, b2 1.97, bc2 1.97, tb2 2.00, tb2c 2.00, c 5.30, cc 5.30, d 9.74, dc 9.74; synthetic folders: a 1.00, ac 1.00, b2 2.00, bc2 2.00, tb2 2.00, tb2c 2.00, c 7.56, cc 7.56, d 12.31, dc 12.31.

### Session 10 set CROSS: same-folder cosine over the synthetic folders (pairs pooled over folders)

| vectors | host-host | guest-guest | host-guest |
|---|---:|---:|---:|
| uncentered | 0.738 (480) | 0.766 (151) | 0.419 (598) |
| centered | 0.488 (480) | 0.545 (151) | 0.023 (598) |

### Session 10 set CROSS: recall@5 per cell and the loss d - x with the paired 95% interval over hosts

| rep | all (151 q, 16 hosts) | guest (41 q, 11 hosts) | host (110 q, 16 hosts) | guest frac [0.2,0.35) (14 q, 4 hosts) | guest frac [0.35,0.5] (27 q, 7 hosts) |
|---|---|---|---|---|---|
| a | 0.523, loss +0.278 [+0.172, +0.377] | 0.000, loss +0.707 [+0.514, +0.864] | 0.718, loss +0.118 [+0.012, +0.218] | 0.000, loss +0.714 [+0.000, +1.000] | 0.000, loss +0.704 [+0.545, +0.833] |
| ac | 0.523, loss +0.278 [+0.185, +0.365] | 0.000, loss +0.707 [+0.514, +0.864] | 0.718, loss +0.118 [+0.043, +0.184] | 0.000, loss +0.714 [+0.000, +1.000] | 0.000, loss +0.704 [+0.545, +0.833] |
| b2 | 0.775, loss +0.026 [-0.045, +0.102] | 0.707, loss +0.000 [-0.061, +0.073] | 0.800, loss +0.036 [-0.054, +0.133] | 0.643, loss +0.071 [+0.000, +0.200] | 0.741, loss -0.037 [-0.107, +0.000] |
| bc2 | 0.768, loss +0.033 [-0.039, +0.111] | 0.732, loss -0.024 [-0.115, +0.059] | 0.782, loss +0.055 [-0.039, +0.147] | 0.643, loss +0.071 [+0.000, +0.200] | 0.778, loss -0.074 [-0.182, +0.000] |
| tb2 | 0.762, loss +0.040 [-0.037, +0.126] | 0.683, loss +0.024 [-0.051, +0.105] | 0.791, loss +0.045 [-0.051, +0.159] | 0.643, loss +0.071 [+0.000, +0.200] | 0.704, loss +0.000 [-0.100, +0.097] |
| tb2c | 0.735, loss +0.066 [-0.020, +0.143] | 0.610, loss +0.098 [-0.065, +0.261] | 0.782, loss +0.055 [-0.039, +0.147] | 0.571, loss +0.143 [+0.000, +0.222] | 0.630, loss +0.074 [-0.167, +0.310] |
| c | 0.801, loss +0.000 [-0.039, +0.055] | 0.732, loss -0.024 [-0.075, +0.000] | 0.827, loss +0.009 [-0.037, +0.082] | 0.714, loss +0.000 [+0.000, +0.000] | 0.741, loss -0.037 [-0.111, +0.000] |
| cc | 0.801, loss +0.000 [-0.048, +0.058] | 0.707, loss +0.000 [-0.065, +0.083] | 0.836, loss +0.000 [-0.061, +0.078] | 0.714, loss +0.000 [+0.000, +0.000] | 0.704, loss +0.000 [-0.097, +0.136] |
| d | 0.801, loss +0.000 [+0.000, +0.000] | 0.707, loss +0.000 [+0.000, +0.000] | 0.836, loss +0.000 [+0.000, +0.000] | 0.714, loss +0.000 [+0.000, +0.000] | 0.704, loss +0.000 [+0.000, +0.000] |
| dc | 0.801, loss +0.000 [-0.019, +0.020] | 0.707, loss +0.000 [-0.065, +0.083] | 0.836, loss +0.000 [+0.000, +0.000] | 0.714, loss +0.000 [+0.000, +0.000] | 0.704, loss +0.000 [-0.097, +0.136] |

### Session 10 set CROSS: recall@1 per cell

| rep | all (151 q, 16 hosts) | guest (41 q, 11 hosts) | host (110 q, 16 hosts) | guest frac [0.2,0.35) (14 q, 4 hosts) | guest frac [0.35,0.5] (27 q, 7 hosts) |
|---|---|---|---|---|---|
| a | 0.397 | 0.000 | 0.545 | 0.000 | 0.000 |
| ac | 0.411 | 0.000 | 0.564 | 0.000 | 0.000 |
| b2 | 0.669 | 0.585 | 0.700 | 0.571 | 0.593 |
| bc2 | 0.669 | 0.561 | 0.709 | 0.571 | 0.556 |
| tb2 | 0.662 | 0.561 | 0.700 | 0.571 | 0.556 |
| tb2c | 0.642 | 0.463 | 0.709 | 0.429 | 0.481 |
| c | 0.709 | 0.610 | 0.745 | 0.643 | 0.593 |
| cc | 0.728 | 0.610 | 0.773 | 0.643 | 0.593 |
| d | 0.709 | 0.610 | 0.745 | 0.643 | 0.593 |
| dc | 0.735 | 0.610 | 0.782 | 0.643 | 0.593 |

### Session 10 set CROSS: recall@10 per cell

| rep | all (151 q, 16 hosts) | guest (41 q, 11 hosts) | host (110 q, 16 hosts) | guest frac [0.2,0.35) (14 q, 4 hosts) | guest frac [0.35,0.5] (27 q, 7 hosts) |
|---|---|---|---|---|---|
| a | 0.563 | 0.000 | 0.773 | 0.000 | 0.000 |
| ac | 0.583 | 0.000 | 0.800 | 0.000 | 0.000 |
| b2 | 0.815 | 0.756 | 0.836 | 0.643 | 0.815 |
| bc2 | 0.781 | 0.756 | 0.791 | 0.643 | 0.815 |
| tb2 | 0.808 | 0.756 | 0.827 | 0.643 | 0.815 |
| tb2c | 0.781 | 0.732 | 0.800 | 0.643 | 0.778 |
| c | 0.828 | 0.756 | 0.855 | 0.714 | 0.778 |
| cc | 0.821 | 0.756 | 0.845 | 0.714 | 0.778 |
| d | 0.841 | 0.780 | 0.864 | 0.714 | 0.815 |
| dc | 0.841 | 0.732 | 0.882 | 0.714 | 0.741 |

### Session 10: loss_CROSS(x) - loss_SAME(x) at recall@5, paired bootstrap over the hosts common to both sets

Loss of x on a cell is (d - x) in recall@5 within a set; the difference is this set's loss minus the other set's, over hosts that have queries of the cell in both sets, 1000 resamples of those hosts.

| rep | all | guest | host | guest frac [0.2,0.35) | guest frac [0.35,0.5] |
|---|---|---|---|---|---|
| a | +0.069 [-0.011, +0.144] (this +0.278, other +0.209, 16 hosts) | +0.180 [+0.021, +0.345] (this +0.763, other +0.583, 10 hosts) | +0.118 [+0.026, +0.238] (this +0.118, other +0.000, 16 hosts) | +0.242 [+0.000, +0.292] (this +0.909, other +0.667, 3 hosts) | +0.148 [-0.065, +0.392] (this +0.704, other +0.556, 7 hosts) |
| ac | +0.011 [-0.068, +0.098] (this +0.278, other +0.267, 16 hosts) | +0.117 [-0.064, +0.322] (this +0.763, other +0.646, 10 hosts) | +0.055 [+0.000, +0.115] (this +0.118, other +0.064, 16 hosts) | +0.159 [+0.000, +0.292] (this +0.909, other +0.750, 3 hosts) | +0.093 [-0.157, +0.368] (this +0.704, other +0.611, 7 hosts) |
| b2 | -0.200 [-0.290, -0.106] (this +0.026, other +0.227, 16 hosts) | -0.604 [-0.786, -0.393] (this +0.000, other +0.604, 10 hosts) | +0.018 [-0.016, +0.056] (this +0.036, other +0.018, 16 hosts) | -0.659 [-1.000, +0.000] (this +0.091, other +0.750, 3 hosts) | -0.593 [-0.779, -0.348] (this -0.037, other +0.556, 7 hosts) |
| bc2 | -0.258 [-0.370, -0.143] (this +0.033, other +0.291, 16 hosts) | -0.672 [-0.833, -0.465] (this -0.026, other +0.646, 10 hosts) | -0.045 [-0.125, +0.029] (this +0.055, other +0.100, 16 hosts) | -0.659 [-1.000, +0.000] (this +0.091, other +0.750, 3 hosts) | -0.685 [-0.871, -0.455] (this -0.074, other +0.611, 7 hosts) |
| tb2 | -0.001 [-0.068, +0.057] (this +0.040, other +0.041, 16 hosts) | -0.057 [-0.206, +0.095] (this +0.026, other +0.083, 10 hosts) | +0.045 [+0.000, +0.103] (this +0.045, other +0.000, 16 hosts) | -0.159 [-0.500, +0.000] (this +0.091, other +0.250, 3 hosts) | -0.028 [-0.188, +0.167] (this +0.000, other +0.028, 7 hosts) |
| tb2c | -0.021 [-0.114, +0.075] (this +0.066, other +0.087, 16 hosts) | -0.061 [-0.353, +0.264] (this +0.105, other +0.167, 10 hosts) | +0.027 [-0.012, +0.075] (this +0.055, other +0.027, 16 hosts) | -0.152 [-0.750, +0.167] (this +0.182, other +0.333, 3 hosts) | -0.037 [-0.392, +0.417] (this +0.074, other +0.111, 7 hosts) |
| c | -0.006 [-0.029, +0.020] (this +0.000, other +0.006, 16 hosts) | -0.047 [-0.096, +0.002] (this -0.026, other +0.021, 10 hosts) | +0.009 [+0.000, +0.031] (this +0.009, other +0.000, 16 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 3 hosts) | -0.065 [-0.124, +0.006] (this -0.037, other +0.028, 7 hosts) |
| cc | -0.023 [-0.042, -0.006] (this +0.000, other +0.023, 16 hosts) | -0.042 [-0.093, +0.008] (this +0.000, other +0.042, 10 hosts) | -0.009 [-0.031, +0.000] (this +0.000, other +0.009, 16 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 3 hosts) | -0.056 [-0.118, +0.015] (this +0.000, other +0.056, 7 hosts) |
| d | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 16 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 10 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 16 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 3 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 7 hosts) |
| dc | +0.000 [-0.023, +0.026] (this +0.000, other +0.000, 16 hosts) | +0.000 [-0.063, +0.089] (this +0.000, other +0.000, 10 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 16 hosts) | +0.000 [+0.000, +0.000] (this +0.000, other +0.000, 3 hosts) | +0.000 [-0.089, +0.118] (this +0.000, other +0.000, 7 hosts) |

H10: loss_CROSS(a) - loss_SAME(a) on guest queries = +0.180 [+0.021, +0.345] over 10 hosts; the interval excludes zero: H10 survives.
