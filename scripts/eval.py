#!/usr/bin/env python3
"""dirvec evaluation: leave-one-out directory-stage recall@k.

Directory representations, each built from D's embedded children (ok flag in the cache):
  a  pooled centroid: mean of child vectors, one vector
  b  per-modality centroids: mean per manifest modality present in D, up to 6 vectors
  c  per-modality k-reps: k-means per modality, k = min(3, n_m), up to 18 vectors
  c4 as c with a budget that scales with the group: k = min(3, ceil(n_m / 4)) (session 6)
  c2 as c with k = min(2, n_m) (session 6)
  cs as c with a budget that grows with the group: k = min(n_m, max(3, ceil(sqrt(n_m)))) (session 19;
     the same three per label up to nine files, then 4 at 10 to 16, 5 at 17 to 25, 10 at 82 to 100)
  d  file-level max (no container layer): every child vector kept
Session 8 (--calib, --reps), not in the default list:
  ab  balanced centroid: mean of the per-input-group means (image inputs, text inputs), one vector
  ac, acb, cc, dc  a, ab, c, d built from centered child vectors, queries centered
Input groups: image inputs are modality image and pdf_scanned, text inputs everything else.
Centering: v' = normalise(v - mu_g), mu_g the mean of the unit file vectors of group g over the
files of a calibration split (--calib, a fraction of all directories, stratified by image_frac
bucket, seed --calib-seed). Calibration directories stay ranking candidates but give no queries.
Session 9 (--calib, --queries dev|eval, --reps), families of candidate representations:
  F1 <s>_p<alpha>   weighted pooling, one vector: unit(sum_g n_g^alpha * mean_g) over the two input
                     groups, alpha in {0, .25, .5, .75, 1}; space s = u (uncentered; p1 is a, p0 is
                     ab) or c (centered; p1 is ac, p0 is acb)
  F2 <s>_p<alpha>   the same pooling after a linear alignment of every image-input vector (files and
                     queries) in the centered space, fitted on the calibration split: s = proc
                     (orthogonal Procrustes on the pairs of centered group means of calibration
                     directories with both groups), coral (whiten with the calibration image
                     covariance, recolour with the text covariance, both Ledoit-Wolf), ridge<lambda>
                     (ridge least squares on the Procrustes pairs, lambda in {1, 10, 100, 1000})
  F3 b2, bc2        one unit centroid per input group, max scoring (uncentered, centered); bc is b
                     on centered vectors
  F4 f4_w<wc>, f4b_w<wc>  the partitioned vector: one index entry [unit mean_img,c ; unit mean_txt,c ;
                     has_img ; has_txt] (zeros for an absent group); the query of group g is
                     [w_same q ; w_cross q ; 0 ; 0] with its own slot first, w_same = 1, w_cross in
                     {0, .25, .5, .75, 1}; the score is one inner product. f4b adds a bias for the
                     cross-group slot (carried in the indicator dimension), chosen on the dev queries
                     as the mean of (same-slot score minus cross-slot score) of the query's own
                     folder, per query group.
  F5 tb2, tbg, tbc (uncentered), tb2c, tbgc, tbcc (centered)  type-blind k-means with max scoring at
                     k = min(2, n), k = input groups present, k = sum_m min(3, n_m) (c's budget)
Dev queries: those whose directory is in the calibration split; eval queries: the rest.
Session 10 (--s10, --split-dirs, --s10-pair): the same-modality dilution control on the synthetic
sets written by synth.py (data/manifest_s10_<set>.jsonl, dirs_s10_<set>.jsonl, gt_s10_<set>.jsonl).
--split-dirs names the dirs file the calibration split is drawn from (the session 5 file, so that
the split and the group means are the session 8 ones whatever the synthetic dirs file contains).
--s10 prints the cells of that session (guest queries, host queries, guest queries by fraction
bin) with recall@1, @5, @10 and the loss (d - x) per row; --s10-pair <ranks file of the other set>
adds the paired difference of the losses over the hosts common to both sets (H10).
Score(q, D) = max cosine between q and D's representative vectors.
Leave-one-out: for query f in D0, D0's representation is rebuilt without f; every other
directory keeps its full representation (f is not in it, and near-duplicates of f outside
D0 were removed from the query set by build_gt.py). All directories with n(D) >= 3 are ranked.
rank = 1 + number of directories scoring strictly higher than D0.

Metrics: recall@k, k in {1, 3, 5, 10}, per image_frac bucket, per query modality and per
bucket x modality. 95 percent bootstrap interval of recall@5 by resampling directories
(1000 resamples, seed 0) within each cell; the same resamples give paired intervals for
the differences b - a and c - a.

Session 3 (--criterion s3) adds the pre-registered primary cells, each pooling two buckets:
  image queries in [0,.2) and [.2,.5); text-like queries (text, table, pdf_text, other) in
  [.5,.8) and [.8,1]. Paired 95 percent intervals of c - a and b - a on recall@5 (1000 resamples
  of the cell's directories). H dies unless c - a excludes zero (lower bound > 0) in both.
  Secondary: d - c for every cell, vectors per directory.
  eval.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s3 --manifest data/manifest_s3.jsonl
          --dirs data/dirs_s3.jsonl --gt data/gt_structural_s3.jsonl --criterion s3

Writes markdown tables to stdout and the per-query ranks to data/emb/<emb>/ranks.jsonl.
"""
import argparse
import json
import os
import sys
import warnings
from collections import Counter, defaultdict

import numpy as np
from sklearn.cluster import KMeans

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
BUCKETS = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]
MODALITIES = ["image", "pdf_text", "pdf_scanned", "text", "table", "other"]
REPS = ["a", "b", "c", "c4", "c2", "d"]
S8_REPS = ["a", "b", "c", "d", "ac", "ab", "acb", "cc", "dc"]
CENTERED = {"ac": "a", "acb": "ab", "cc": "c", "dc": "d"}   # centered rep -> rep it applies to Vc
IMAGE_INPUTS = ["image", "pdf_scanned"]
KS = [1, 3, 5, 10]
N_BOOT = 1000
ALPHAS = ["0", "0.25", "0.5", "0.75", "1"]
ALIGNED = ["proc", "coral", "ridge1", "ridge10", "ridge100", "ridge1000"]
S9_F1 = [f"{s}_p{a}" for s in ("u", "c") for a in ALPHAS]
S9_F2 = [f"{s}_p{a}" for s in ALIGNED for a in ALPHAS]
S9_F3 = ["b2", "bc2", "bc"]
S9_F4 = [f"{b}_w{w}" for b in ("f4", "f4b") for w in ALPHAS]
S9_F5 = ["tb2", "tbg", "tbc", "tb2c", "tbgc", "tbcc"]
S9_REF = ["a", "b", "c", "d", "ac", "cc", "dc"]
S9_REPS = S9_REF + S9_F1 + S9_F2 + S9_F3 + S9_F4 + S9_F5
FAMILIES = {"F1": S9_F1, "F2": S9_F2, "F3": S9_F3, "F4": S9_F4, "F5": S9_F5}


def parse_rep(rep):
    """Session 9 rep name -> (space, base, param). space: u, c or an ALIGNED name; base: one of the
    build() bases; param: alpha (F1, F2), w_cross (F4) or the budget (F5). Legacy names unchanged."""
    if rep in REPS or rep in S8_REPS:
        return ("c" if rep in CENTERED else "u", CENTERED.get(rep, rep), None)
    if rep == "cs":
        return ("u", "cs", None)
    if "_p" in rep:
        s, a = rep.split("_p")
        return (s, "p", float(a))
    if rep in ("b2", "bc2"):
        return ("c" if rep == "bc2" else "u", "b2", None)
    if rep == "bc":
        return ("c", "b", None)
    if rep.startswith("f4"):
        b, w = rep.split("_w")
        return ("c", b, float(w))
    if rep.startswith("tb"):
        budget = rep[2]
        return ("c" if rep.endswith("c") and len(rep) == 4 else "u", "tb", budget)
    raise ValueError(rep)


def family_of(rep):
    return next((f for f, names in FAMILIES.items() if rep in names), "ref")


def unit(x):
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)


def kreps(X, seed=0, k=None):
    """k-means reps for one modality group: k = min(3, n) unless given. Unit-normalised centroids."""
    k = min(3, len(X)) if k is None else k
    if k == len(X):
        return X
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # duplicate children give fewer than k distinct points; harmless
        km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X)
    return unit(km.cluster_centers_.astype(np.float32))


def kmeans_labels(X, k, seed=0):
    """Cluster labels of the k-means run kreps() performs (same parameters and seed)."""
    if k >= len(X):
        return np.arange(len(X))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X).labels_


def tb_k(base_budget, mods):
    """Type-blind k-means budget (session 9 F5): '2' min(2, n), 'g' input groups present,
    'c' the sum over modality labels of min(3, n_m), which is c's budget."""
    n = len(mods)
    if base_budget == "2":
        return min(2, n)
    if base_budget == "g":
        img = np.isin(mods, IMAGE_INPUTS)
        return int(img.any()) + int((~img).any())
    return sum(min(3, int((mods == m).sum())) for m in MODALITIES)


def build(rep, X, mods, param=None):
    """Representative vectors of one directory from child vectors X (n, d) and modality labels.
    rep is a base name (see parse_rep); param the family parameter (alpha, w_cross or budget)."""
    if len(X) == 0:
        return np.zeros((0, X.shape[1] if rep not in ("f4", "f4b") else 2 * X.shape[1] + 2), np.float32)
    if rep == "a":
        return unit(X.mean(axis=0, keepdims=True))
    if rep == "d":
        return X
    if rep == "ab":
        img = np.isin(mods, IMAGE_INPUTS)
        means = [X[g].mean(axis=0) for g in (img, ~img) if g.any()]
        return unit(np.mean(means, axis=0, keepdims=True))
    if rep == "p":                                        # F1, F2: unit(sum_g n_g^alpha mean_g)
        img = np.isin(mods, IMAGE_INPUTS)
        # float(): g.sum() ** param is a NumPy float64 scalar, which promoted the vector to float64
        # (session 13 correction; see rank_rep). The representatives are float32 like every other row.
        v = sum(float(g.sum()) ** param * X[g].mean(axis=0) for g in (img, ~img) if g.any())
        return unit(v[None, :]).astype(np.float32)
    if rep == "b2":                                       # F3: one unit centroid per input group
        img = np.isin(mods, IMAGE_INPUTS)
        return np.concatenate([unit(X[g].mean(axis=0, keepdims=True)) for g in (img, ~img) if g.any()])
    if rep in ("f4", "f4b"):                              # F4: [mean_img ; mean_txt ; has_img ; has_txt]
        img = np.isin(mods, IMAGE_INPUTS)
        d = X.shape[1]
        out = np.zeros((1, 2 * d + 2), np.float32)
        for i, g in enumerate((img, ~img)):
            if g.any():
                out[0, i * d:(i + 1) * d] = unit(X[g].mean(axis=0))
                out[0, 2 * d + i] = 1.0
        return out
    if rep == "tb":                                       # F5: type-blind k-means
        return kreps(X, k=tb_k(param, mods))
    out = []
    for m in MODALITIES:
        sel = mods == m
        if not sel.any():
            continue
        n_m = int(sel.sum())
        if rep == "b":
            out.append(unit(X[sel].mean(axis=0, keepdims=True)))
        elif rep == "c":
            out.append(kreps(X[sel]))
        elif rep == "c4":
            out.append(kreps(X[sel], k=min(3, -(-n_m // 4))))
        elif rep == "c2":
            out.append(kreps(X[sel], k=min(2, n_m)))
        elif rep == "cs":
            out.append(kreps(X[sel], k=min(n_m, max(3, int(np.ceil(np.sqrt(n_m)))))))
        else:
            raise ValueError(rep)
    return np.concatenate(out)


def max_scores(q, reps_by_dir, dir_list):
    """(n_dirs,) max cosine of q against each directory's representatives."""
    return np.array([(R @ q).max() if len(R) else -np.inf for R in (reps_by_dir[d] for d in dir_list)])


def boot(hits_by_dir, dirs, rng_idx):
    """recall over resampled directories. hits_by_dir: {dir: (hits, n)}; rng_idx: (B, len(dirs))."""
    h = np.array([hits_by_dir[d][0] for d in dirs], float)
    n = np.array([hits_by_dir[d][1] for d in dirs], float)
    return h[rng_idx].sum(axis=1) / n[rng_idx].sum(axis=1)


TEXTLIKE = ["text", "table", "pdf_text", "other"]


def s3_section(out, qb, qm, recall_row, cell_boot, fmt, REPS=REPS):
    """Session 3 pre-registered primary cells, their per-bucket parts, and d - c everywhere."""
    primary, parts, majority, buckets = s3_cells(qb, qm)

    def diff_table(title, cells, pairs):
        out.append("")
        out.append(f"### {title}")
        out.append("")
        out.append("| cell | queries | dirs | " + " | ".join(REPS) + " | " +
                   " | ".join(f"{p} | {p} 95% CI" for p in pairs) + " |")
        out.append("|---|---:|---:|" + "---:|" * len(REPS) + "---:|---|" * len(pairs))
        res = {}
        for name, sel, seed in cells:
            if not sel.any():
                continue
            rr = recall_row(sel)
            ci, diff, nd = cell_boot(sel, seed)
            r5 = {rep: rr[rep][2] for rep in REPS}
            cols = []
            for p in pairs:
                x, y = p.split("-")
                cols.append(f"{r5[x] - r5[y]:+.3f} | [{diff[p][0]:+.3f}, {diff[p][1]:+.3f}]")
            out.append(f"| {name} | {int(sel.sum())} | {nd} | " + " | ".join(fmt(r5[rep]) for rep in REPS) +
                       " | " + " | ".join(cols) + " |")
            res[name] = diff
        return res

    budget = [p for p in ["c-a", "b-a", "c4-a", "c2-a"] if p.split("-")[0] in REPS]
    prim = diff_table("Session 3 primary cells: recall@5, paired bootstrap over directories",
                      primary, budget)
    diff_table("Primary cells split by bucket (not part of the criterion)", parts, budget)
    diff_table("Majority-modality cells (for contrast, not part of the criterion)", majority,
               [p for p in ("c-a", "b-a") if p.split("-")[0] in REPS])
    diff_table("Secondary: d - c everywhere, recall@5",
               primary + parts + majority + buckets, ["d-c"])
    out.append("")
    alive = all(prim[name]["c-a"][0] > 0 for name, _, _ in primary if name in prim) and len(prim) == 2
    out.append("Paired 95% interval of c - a excludes zero (lower bound > 0): " +
               "; ".join(f"{name}: {'yes' if prim[name]['c-a'][0] > 0 else 'no'}" for name in prim) + ".")
    out.append(f"H {'survives' if alive else 'is dead'} under the session 3 kill criterion.")


def bucket_of(frac):
    """image_frac bucket, as in build_gt.py."""
    return BUCKETS[0] if frac < 0.2 else BUCKETS[1] if frac < 0.5 else BUCKETS[2] if frac < 0.8 else BUCKETS[3]


def modality_gap(V, Vc, is_img, children, dirs_eval):
    """Gap between the mean image-input and mean text-input vectors (Liang et al. 2022) and mean
    cosine of same-folder file pairs within and across groups, over dirs_eval, before and after."""
    idx = np.concatenate([children[d] for d in dirs_eval])
    res = {}
    for name, X in (("before", unit(V)), ("after", Vc)):
        gap = float(np.linalg.norm(X[idx][is_img[idx]].mean(axis=0) - X[idx][~is_img[idx]].mean(axis=0)))
        sums = defaultdict(lambda: [0.0, 0])
        for d in dirs_eval:
            c = children[d]
            G = X[c] @ X[c].T
            g = is_img[c]
            iu = np.triu(np.ones((len(c), len(c)), bool), 1)
            for key, m in (("img-img", np.outer(g, g)), ("txt-txt", np.outer(~g, ~g)),
                           ("img-txt", np.outer(g, ~g) | np.outer(~g, g))):
                sel = iu & m
                sums[key][0] += float(G[sel].sum())
                sums[key][1] += int(sel.sum())
        res[name] = {"gap": gap, **{k: (v[0] / v[1] if v[1] else float("nan"), v[1]) for k, v in sums.items()}}
    res["files"] = (int(is_img[idx].sum()), int((~is_img[idx]).sum()), len(dirs_eval))
    return res


def calib_split(dirs, frac, seed):
    """Session 8 calibration split. Stratified: per bucket (in BUCKETS order, dirs sorted) a random
    round(frac * n) of the directories."""
    calib = set()
    rng = np.random.default_rng(seed)
    for b in BUCKETS:
        ds = sorted(d for d, r in dirs.items() if bucket_of(r["image_frac"]) == b)
        n_cal = int(round(frac * len(ds)))
        calib.update(ds[i] for i in rng.permutation(len(ds))[:n_cal])
    return calib


def centered_space(V, ok, mods_all, manifest, dirs, frac, seed):
    """Session 8 calibration split (calib_split over dirs) and centering. Returns the calibration
    set, the image-input mask, the in-calibration mask over files, the group means and the centered
    unit vectors Vc."""
    calib = calib_split(dirs, frac, seed)
    is_img = np.isin(mods_all, IMAGE_INPUTS)
    in_calib = np.array([r["dir"] in calib for r in manifest])
    Vu = unit(V)
    mu = {g: Vu[ok & in_calib & sel].mean(axis=0) for g, sel in (("img", is_img), ("txt", ~is_img))}
    Vc = unit(Vu - np.where(is_img[:, None], mu["img"], mu["txt"])).astype(np.float32)
    return calib, is_img, in_calib, mu, Vc


def align_spaces(Vc, is_img, ok, in_calib, children, calib_dirs, names):
    """Session 9 F2: every image-input vector (files and queries) of the centered space Vc mapped by
    a linear alignment fitted on the calibration split; text-input vectors unchanged. Returns
    {name: (N, d) unit vectors} for the requested ALIGNED names, and a dict of fit notes."""
    d = Vc.shape[1]
    pairs = [(Vc[c[is_img[c]]].mean(axis=0), Vc[c[~is_img[c]]].mean(axis=0))
             for c in (children[x] for x in calib_dirs) if is_img[c].any() and (~is_img[c]).any()]
    X = np.array([p[0] for p in pairs], np.float64)
    Y = np.array([p[1] for p in pairs], np.float64)
    notes = {"pairs": len(pairs)}
    out = {}
    img_rows = np.where(ok & is_img)[0]

    def apply(fn, name):
        W = Vc.copy()
        W[img_rows] = unit(fn(Vc[img_rows].astype(np.float64))).astype(np.float32)
        out[name] = W

    for name in names:
        if name == "proc":
            U, s, Vt = np.linalg.svd(X.T @ Y)
            R = U @ Vt
            apply(lambda Z: Z @ R, name)
        elif name == "coral":
            from sklearn.covariance import LedoitWolf
            Zi = Vc[img_rows[in_calib[img_rows]]].astype(np.float64)
            Zt = Vc[np.where(ok & ~is_img & in_calib)[0]].astype(np.float64)
            lw_i, lw_t = LedoitWolf().fit(Zi), LedoitWolf().fit(Zt)
            notes["coral_shrinkage"] = (float(lw_i.shrinkage_), float(lw_t.shrinkage_))

            def pow_sym(C, p):
                w, U = np.linalg.eigh(C)
                return (U * np.maximum(w, 1e-12) ** p) @ U.T
            A = pow_sym(lw_i.covariance_, -0.5) @ pow_sym(lw_t.covariance_, 0.5)
            mi, mt = Zi.mean(axis=0), Zt.mean(axis=0)
            apply(lambda Z: (Z - mi) @ A + mt, name)
        elif name.startswith("ridge"):
            lam = float(name[5:])
            R = np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ Y)
            apply(lambda Z: Z @ R, name)
        else:
            raise ValueError(name)
    return out, notes


def query_vectors(rep, Q, q_img, bias):
    """The query matrix a rep scores against. F4: [w_same q ; w_cross q ; 0 ; 0] with the query's own
    slot first (w_same = 1); f4b carries w_cross * bias[g] in the cross-group indicator slot."""
    space, base, param = parse_rep(rep)
    if base not in ("f4", "f4b"):
        return Q
    d = Q.shape[1]
    out = np.zeros((len(Q), 2 * d + 2), np.float32)
    out[q_img, :d] = Q[q_img]
    out[q_img, d:2 * d] = param * Q[q_img]
    out[~q_img, d:2 * d] = Q[~q_img]
    out[~q_img, :d] = param * Q[~q_img]
    if base == "f4b":
        out[q_img, 2 * d + 1] = param * bias["img"]
        out[~q_img, 2 * d] = param * bias["txt"]
    return out


def f4_bias(Vc, is_img, children, pos, dev_queries):
    """F4b bias per query group, chosen on the dev queries: mean over dev queries whose leave-one-out
    folder has both input groups of (q . unit mean of its own group minus q . unit mean of the other
    group), centered vectors."""
    sums = {"img": [0.0, 0], "txt": [0.0, 0]}
    for g in dev_queries:
        p = pos[g["query_path"]]
        keep = children[g["relevant_dir"]]
        keep = keep[keep != p]
        gi = is_img[keep]
        if not (gi.any() and (~gi).any()):
            continue
        q = Vc[p]
        same, cross = (gi, ~gi) if is_img[p] else (~gi, gi)
        s = float(q @ unit(Vc[keep][same].mean(axis=0))) - float(q @ unit(Vc[keep][cross].mean(axis=0)))
        key = "img" if is_img[p] else "txt"
        sums[key][0] += s
        sums[key][1] += 1
    return {k: v[0] / v[1] for k, v in sums.items()}, {k: v[1] for k, v in sums.items()}


def purity(rep, W, mods_all, is_img, children, dirs_eval):
    """Session 9 F5 cluster purity over folders with both input groups: share of files whose
    cluster's strict-majority input group is their own (full folders, no leave-one-out)."""
    space, base, budget = parse_rep(rep)
    hit = tot = nd = 0
    for d in dirs_eval:
        c = children[d]
        gi = is_img[c]
        if not (gi.any() and (~gi).any()):
            continue
        nd += 1
        lab = kmeans_labels(W[c], tb_k(budget, mods_all[c]))
        for l in np.unique(lab):
            m = lab == l
            n_i = int(gi[m].sum())
            n_t = int(m.sum()) - n_i
            hit += n_i if n_i > n_t else n_t if n_t > n_i else 0
            tot += int(m.sum())
    return hit / tot, nd


def s9_section(out, qb, qm, ranks, cell_res, fmt, reps, n_reps, split, extra):
    """Session 9: five cells, x - c, x - d, x - dc, selection per family, H9a to H9c."""
    primary, parts, majority, buckets = s3_cells(qb, qm)
    cells = [("all", np.ones(len(qb), bool), 1)] + primary + majority
    four = [c[0] for c in primary + majority]
    res = {name: cell_res(sel, seed) for name, sel, seed in cells}

    def r_at(rep, sel, k=5):
        return float((ranks[rep][sel] <= k).mean())

    def ci(x):
        lo, hi = np.percentile(x, [2.5, 97.5])
        return lo, hi

    out.append("")
    out.append(f"### Session 9 ({split} queries): recall@5 per cell and x - c, paired bootstrap over directories")
    out.append("")
    out.append("| rep | family | vec/folder | " + " | ".join(f"R@5 {n}" for n, _, _ in cells) + " | " +
               " | ".join(f"x-c {n}" for n, _, _ in cells) + " | min over 4 cells |")
    out.append("|---|---|---:|" + "---:|" * len(cells) + "---|" * len(cells) + "---:|")
    diff = {}
    for rep in reps:
        cols, dcols = [], []
        diff[rep] = {}
        for name, sel, seed in cells:
            r, nd = res[name]
            cols.append(fmt(r_at(rep, sel)))
            dstat = r_at(rep, sel) - r_at("c", sel)
            lo, hi = ci(r[rep] - r["c"])
            diff[rep][name] = (dstat, lo, hi)
            dcols.append(f"{dstat:+.3f} [{lo:+.3f}, {hi:+.3f}]")
        mn = min(diff[rep][n][0] for n in four)
        out.append(f"| {rep} | {family_of(rep)} | {n_reps[rep]:.2f} | " + " | ".join(cols) + " | " +
                   " | ".join(dcols) + f" | {mn:+.3f} |")

    for k in (1, 10):
        out.append("")
        out.append(f"### Session 9 ({split} queries): recall@{k} per cell")
        out.append("")
        out.append("| rep | " + " | ".join(n for n, _, _ in cells) + " |")
        out.append("|---|" + "---:|" * len(cells))
        for rep in reps:
            out.append(f"| {rep} | " + " | ".join(fmt(r_at(rep, sel, k)) for _, sel, _ in cells) + " |")

    for ref in ("d", "dc"):
        if ref not in reps:
            continue
        out.append("")
        out.append(f"### Session 9 ({split} queries): x - {ref}, recall@5, paired bootstrap over directories")
        out.append("")
        out.append("| rep | " + " | ".join(n for n, _, _ in cells) + " |")
        out.append("|---|" + "---|" * len(cells))
        for rep in reps:
            cols = []
            for name, sel, seed in cells:
                r, nd = res[name]
                lo, hi = ci(r[rep] - r[ref])
                cols.append(f"{r_at(rep, sel) - r_at(ref, sel):+.3f} [{lo:+.3f}, {hi:+.3f}]")
            out.append(f"| {rep} | " + " | ".join(cols) + " |")

    # selection per family: max over configurations of the min over the four cells of (x - c);
    # ties to fewer vectors, then smaller alpha or w_cross, then name
    out.append("")
    out.append(f"### Session 9 selection rule applied to the {split} queries (valid only on dev)")
    out.append("")
    out.append("| family | selected | vec/folder | min over 4 cells of (x - c) | " + " | ".join(four) + " |")
    out.append("|---|---|---:|---:|" + "---:|" * len(four))
    selected = {}
    for fam, names in FAMILIES.items():
        cands = [r for r in names if r in reps]
        if not cands:
            continue
        key = lambda r: (-min(diff[r][n][0] for n in four), n_reps[r], parse_rep(r)[2] or 0, r)
        best = sorted(cands, key=key)[0]
        selected[fam] = best
        out.append(f"| {fam} | {best} | {n_reps[best]:.2f} | {min(diff[best][n][0] for n in four):+.3f} | " +
                   " | ".join(f"{diff[best][n][0]:+.3f}" for n in four) + " |")

    if extra.get("f4_bias"):
        b, n = extra["f4_bias"]
        out.append("")
        out.append(f"F4b bias (dev queries, leave-one-out folders with both groups): image queries {b['img']:+.4f} "
                   f"(n = {n['img']}), text queries {b['txt']:+.4f} (n = {n['txt']}).")
    if extra.get("align_notes"):
        out.append("")
        out.append(f"Alignment fit: {extra['align_notes']}.")
    if extra.get("gaps"):
        out.append("")
        out.append(f"### Session 9 modality gap per space, {split} directories")
        out.append("")
        out.append("| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |")
        out.append("|---|---:|---:|---:|---:|")
        for name, g in extra["gaps"].items():
            out.append(f"| {name} | {g['gap']:.3f} | " +
                       " | ".join(f"{g[k][0]:.3f}" for k in ("img-img", "txt-txt", "img-txt")) + " |")
    if extra.get("purity"):
        out.append("")
        out.append(f"### Session 9 F5 cluster purity, {split} directories with both input groups")
        out.append("")
        out.append("| rep | vec/folder | purity | folders |")
        out.append("|---|---:|---:|---:|")
        for rep, (p, nd) in extra["purity"].items():
            out.append(f"| {rep} | {n_reps[rep]:.2f} | {p:.3f} | {nd} |")

    # hypotheses, meaningful on the eval (test) split only
    out.append("")
    out.append(f"### Session 9 hypotheses on the {split} queries" +
               (" (dev: informative only, the verdict is the test split)" if split == "dev" else ""))
    out.append("")
    for fam in ("F1", "F2"):
        if fam in selected:
            r = selected[fam]
            ups = {n: diff[r][n][2] for n in four}
            dead = all(u > -0.02 for u in ups.values())
            out.append(f"H9a, {fam} selected {r}: upper bounds of (x - c) " +
                       ", ".join(f"{n} {u:+.3f}" for n, u in ups.items()) +
                       f"; all above -0.02: {'yes, H9a dead' if dead else 'no, H9a survives this family'}.")
    for fam in ("F3", "F4"):
        if fam in selected:
            r = selected[fam]
            ups = {n: diff[r][n][2] for n, _, _ in cells}
            dead = any(u < -0.02 for u in ups.values())
            out.append(f"H9b, {fam} selected {r}: upper bounds of (x - c) " +
                       ", ".join(f"{n} {u:+.3f}" for n, u in ups.items()) +
                       f"; any below -0.02: {'yes, H9b dead for this family' if dead else 'no, H9b survives this family'}.")
    if "tbc" in reps:
        parts_ = []
        dead = False
        for name, sel, seed in primary:
            r, nd = res[name]
            lo, hi = ci(r["c"] - r["tbc"])
            parts_.append(f"{name} {r_at('c', sel) - r_at('tbc', sel):+.3f} [{lo:+.3f}, {hi:+.3f}]")
            dead |= lo <= 0 <= hi
        out.append("H9c, c - tbc (type-blind k-means at c's budget, uncentered): " + "; ".join(parts_) +
                   f"; interval includes zero in a primary cell: {'yes, H9c dead' if dead else 'no, H9c survives'}.")
    if "tbcc" in reps and "cc" in reps:
        parts_ = []
        for name, sel, seed in primary:
            r, nd = res[name]
            lo, hi = ci(r["cc"] - r["tbcc"])
            parts_.append(f"{name} {r_at('cc', sel) - r_at('tbcc', sel):+.3f} [{lo:+.3f}, {hi:+.3f}]")
        out.append("Secondary, cc - tbcc (centered): " + "; ".join(parts_) + ".")
    return selected

S10_REPS = ["a", "ac", "b2", "bc2", "tb2", "tb2c", "c", "cc", "d", "dc"]
S19_REPS = ["cs"]   # session 19: per-modality k-means with a square-root budget; not in any default list
S10_BINS = [("guest frac [0.2,0.35)", 0.2, 0.35), ("guest frac [0.35,0.5]", 0.35, 0.5000001)]


def s10_cells(queries):
    """Session 10 cells over the queries of one synthetic set: all, guest, host, guest by fraction bin."""
    role = np.array([g.get("role", "") for g in queries])
    frac = np.array([g.get("guest_frac", np.nan) for g in queries], float)
    guest = role == "guest"
    cells = [("all", np.ones(len(queries), bool), 74), ("guest", guest, 70), ("host", role == "host", 71)]
    cells += [(name, guest & (frac >= lo) & (frac < hi), 72 + i) for i, (name, lo, hi) in enumerate(S10_BINS)]
    return cells


def s10_section(out, queries, ranks, cell_res, fmt, reps, n_reps, full, manifest, children, V, Vc, pair):
    """Session 10: counts, recall per cell, the loss (d - x) per cell, same-folder cosines host-guest,
    and with pair (the other set's ranks rows) the paired difference of the losses over common hosts."""
    set_name = next((g.get("set") for g in queries if g.get("set")), "?")
    hosts = sorted({g["relevant_dir"] for g in queries})
    guest_dirs = sorted({g.get("guest_dir") for g in queries if g.get("guest_dir")})
    host_frac = {g["relevant_dir"]: float(g["guest_frac"]) for g in queries if "guest_frac" in g}
    fr = np.array([host_frac[h] for h in hosts if h in host_frac])
    role = np.array([g.get("role", "") for g in queries])
    n_guest_files = sum(1 for r in manifest if r.get("guest_from"))
    out.append("")
    out.append(f"### Session 10 set {set_name}: counts")
    out.append("")
    out.append(f"Hosts (synthetic folders with queries): {len(hosts)}; guest directories: {len(guest_dirs)}; guest files moved: "
               f"{n_guest_files}; queries: {len(queries)} ({int((role == 'host').sum())} host, {int((role == 'guest').sum())} guest).")
    if len(fr):
        out.append(f"Realised guest fraction over hosts: min {fr.min():.3f}, median {np.median(fr):.3f}, mean {fr.mean():.3f}, "
                   f"max {fr.max():.3f}; hosts per bin: " +
                   ", ".join(f"{name} {int(((fr >= lo) & (fr < hi)).sum())}" for name, lo, hi in S10_BINS) + ".")
    out.append("Vectors per folder, all ranked directories: " + ", ".join(f"{r} {n_reps[r]:.2f}" for r in reps) +
               "; synthetic folders: " +
               ", ".join(f"{r} {np.mean([len(full[r][h]) for h in hosts]):.2f}" for r in reps) + ".")

    # same-folder cosines host-guest, host-host, guest-guest, uncentered and centered
    guest_file = np.array([bool(r.get("guest_from")) for r in manifest])
    out.append("")
    out.append(f"### Session 10 set {set_name}: same-folder cosine over the synthetic folders (pairs pooled over folders)")
    out.append("")
    out.append("| vectors | host-host | guest-guest | host-guest |")
    out.append("|---|---:|---:|---:|")
    for name, X in (("uncentered", unit(V)), ("centered", Vc)):
        sums = defaultdict(lambda: [0.0, 0])
        for h in hosts:
            c = children[h]
            G = X[c] @ X[c].T
            g = guest_file[c]
            iu = np.triu(np.ones((len(c), len(c)), bool), 1)
            for key, m in (("host-host", np.outer(~g, ~g)), ("guest-guest", np.outer(g, g)),
                           ("host-guest", np.outer(g, ~g) | np.outer(~g, g))):
                sel = iu & m
                sums[key][0] += float(G[sel].sum())
                sums[key][1] += int(sel.sum())
        out.append(f"| {name} | " + " | ".join(f"{sums[k][0] / sums[k][1]:.3f} ({sums[k][1]})" if sums[k][1] else "nan"
                                             for k in ("host-host", "guest-guest", "host-guest")) + " |")

    cells = s10_cells(queries)
    res = {name: cell_res(sel, seed) for name, sel, seed in cells if sel.any()}

    def r_at(rep, sel, k=5):
        return float((ranks[rep][sel] <= k).mean())

    def ci(x):
        lo, hi = np.percentile(x, [2.5, 97.5])
        return lo, hi

    for k in (5, 1, 10):
        out.append("")
        out.append(f"### Session 10 set {set_name}: recall@{k} per cell" +
                   (" and the loss d - x with the paired 95% interval over hosts" if k == 5 else ""))
        out.append("")
        head = [f"{n} ({int(sel.sum())} q, {res[n][1]} hosts)" for n, sel, _ in cells if sel.any()]
        out.append("| rep | " + " | ".join(head) + " |")
        out.append("|---|" + "---|" * len(head))
        for rep in reps:
            cols = []
            for name, sel, seed in cells:
                if not sel.any():
                    continue
                v = fmt(r_at(rep, sel, k))
                if k == 5 and "d" in reps:
                    lo, hi = ci(res[name][0]["d"] - res[name][0][rep])
                    v += f", loss {r_at('d', sel) - r_at(rep, sel):+.3f} [{lo:+.3f}, {hi:+.3f}]"
                cols.append(v)
            out.append(f"| {rep} | " + " | ".join(cols) + " |")

    if pair is None:
        return
    other = next((g.get("set") for g in pair if g.get("set")), "?")
    preps = [r for r in reps if f"rank_{r}" in pair[0] and "d" in reps]
    pranks = {r: np.array([g[f"rank_{r}"] for g in pair]) for r in preps}
    pcells = s10_cells(pair)
    qd = np.array([g["relevant_dir"] for g in queries])
    pd_ = np.array([g["relevant_dir"] for g in pair])
    out.append("")
    out.append(f"### Session 10: loss_{set_name}(x) - loss_{other}(x) at recall@5, paired bootstrap over the hosts common to both sets")
    out.append("")
    out.append("Loss of x on a cell is (d - x) in recall@5 within a set; the difference is this set's loss minus the other set's, "
               "over hosts that have queries of the cell in both sets, 1000 resamples of those hosts.")
    out.append("")
    names = [n for n, _, _ in cells]
    out.append("| rep | " + " | ".join(names) + " |")
    out.append("|---|" + "---|" * len(names))
    verdict = {}
    for rep in preps:
        cols = []
        for (name, sel, seed), (_, psel, _) in zip(cells, pcells):
            common = sorted(set(qd[sel]) & set(pd_[psel]))
            if len(common) < 2:
                cols.append("n/a")
                continue
            rng = np.random.default_rng(seed + 100)
            idx = rng.integers(0, len(common), size=(N_BOOT, len(common)))

            def loss(rk, dd, s):
                hb = {r: defaultdict(lambda: [0, 0]) for r in ("d", rep)}
                for d, rd, rx in zip(dd[s], rk["d"][s], rk[rep][s]):
                    hb["d"][d][0] += int(rd <= 5)
                    hb["d"][d][1] += 1
                    hb[rep][d][0] += int(rx <= 5)
                    hb[rep][d][1] += 1
                cs = set(common)
                m = np.array([d in cs for d in dd[s]])
                point = float((rk["d"][s][m] <= 5).mean() - (rk[rep][s][m] <= 5).mean())
                return boot(hb["d"], common, idx) - boot(hb[rep], common, idx), point
            lt, pt = loss(ranks, qd, sel)
            lo_, po = loss(pranks, pd_, psel)
            diff = lt - lo_
            lo, hi = ci(diff)
            cols.append(f"{pt - po:+.3f} [{lo:+.3f}, {hi:+.3f}] (this {pt:+.3f}, other {po:+.3f}, {len(common)} hosts)")
            if rep == "a" and name == "guest":
                verdict = {"stat": pt - po, "lo": lo, "hi": hi, "n": len(common)}
        out.append(f"| {rep} | " + " | ".join(cols) + " |")
    if verdict and set_name == "CROSS" and other == "SAME":
        out.append("")
        dead = verdict["lo"] <= 0 <= verdict["hi"]
        out.append(f"H10: loss_CROSS(a) - loss_SAME(a) on guest queries = {verdict['stat']:+.3f} "
                   f"[{verdict['lo']:+.3f}, {verdict['hi']:+.3f}] over {verdict['n']} hosts; the interval "
                   f"{'includes' if dead else 'excludes'} zero: H10 {'is dead' if dead else 'survives'}.")


def s3_cells(qb, qm):
    """Session 3 cells: primary, their per-bucket parts, majority-modality cells, and per-bucket cells."""
    textlike = np.isin(qm, TEXTLIKE)
    primary = [
        ("P1 image in [0,.2)+[.2,.5)", (qm == "image") & np.isin(qb, BUCKETS[:2]), 50),
        ("P2 textlike in [.5,.8)+[.8,1]", textlike & np.isin(qb, BUCKETS[2:]), 51),
    ]
    parts = [
        ("P1 part: image [0,.2)", (qm == "image") & (qb == BUCKETS[0]), 52),
        ("P1 part: image [.2,.5)", (qm == "image") & (qb == BUCKETS[1]), 53),
        ("P2 part: textlike [.5,.8)", textlike & (qb == BUCKETS[2]), 54),
        ("P2 part: textlike [.8,1]", textlike & (qb == BUCKETS[3]), 55),
    ]
    majority = [
        ("image in [.5,.8)+[.8,1]", (qm == "image") & np.isin(qb, BUCKETS[2:]), 56),
        ("textlike in [0,.2)+[.2,.5)", textlike & np.isin(qb, BUCKETS[:2]), 57),
    ]
    buckets = ([(f"all {b}", qb == b, 60 + i) for i, b in enumerate(BUCKETS)] +
               [(f"image {b}", (qb == b) & (qm == "image"), 30 + i) for i, b in enumerate(BUCKETS)] +
               [(f"textlike {b}", (qb == b) & textlike, 40 + i) for i, b in enumerate(BUCKETS)])
    return primary, parts, majority, buckets


def s8_section(out, qb, qm, ranks, cell_res, fmt, reps, gap):
    """Session 8: H8 on the evaluation split, secondary differences, modality gap."""
    primary, parts, majority, buckets = s3_cells(qb, qm)
    everything = [("all", np.ones(len(qb), bool), 1)]

    def r5(rep, sel):
        return float((ranks[rep][sel] <= 5).mean())

    def ci(x):
        lo, hi = np.percentile(x, [2.5, 97.5])
        return f"[{lo:+.3f}, {hi:+.3f}]", lo

    one = [x for x in ("ac", "ab", "acb") if x in reps]
    out.append("")
    out.append("### Session 8 H8: (x - a) - 0.5 * (c - a), recall@5, paired bootstrap over directories")
    out.append("")
    out.append("| cell | queries | dirs | a | c | " + " | ".join(one) + " | " +
               " | ".join(f"{x}: stat | {x}: 95% CI" for x in one) + " |")
    out.append("|---|---:|---:|---:|---:|" + "---:|" * len(one) + "---:|---|" * len(one))
    verdict = {}
    for name, sel, seed in primary + parts:
        res, nd = cell_res(sel, seed)
        cols = []
        for x in one:
            st = (r5(x, sel) - r5("a", sel)) - 0.5 * (r5("c", sel) - r5("a", sel))
            txt, lo = ci((res[x] - res["a"]) - 0.5 * (res["c"] - res["a"]))
            cols.append(f"{st:+.3f} | {txt}")
            if x == "ac" and name.startswith("P") and "part" not in name:
                verdict[name] = lo > 0
        out.append(f"| {name} | {int(sel.sum())} | {nd} | {fmt(r5('a', sel))} | {fmt(r5('c', sel))} | " +
                   " | ".join(fmt(r5(x, sel)) for x in one) + " | " + " | ".join(cols) + " |")

    def diff_table(title, cells, pairs):
        out.append("")
        out.append(f"### {title}")
        out.append("")
        out.append("| cell | queries | dirs | " + " | ".join(f"{p} | {p} 95% CI" for p in pairs) + " |")
        out.append("|---|---:|---:|" + "---:|---|" * len(pairs))
        for name, sel, seed in cells:
            if not sel.any():
                continue
            res, nd = cell_res(sel, seed)
            cols = []
            for p in pairs:
                x, y = p.split("-")
                cols.append(f"{r5(x, sel) - r5(y, sel):+.3f} | {ci(res[x] - res[y])[0]}")
            out.append(f"| {name} | {int(sel.sum())} | {nd} | " + " | ".join(cols) + " |")

    cells = everything + primary + parts + majority + buckets
    diff_table("Session 8 secondary: one-vector representations minus a, recall@5",
               cells, [f"{x}-a" for x in one] + ["c-a"])
    diff_table("Session 8 secondary: centered minus uncentered, recall@5",
               cells, [p for p in ("ac-a", "acb-ab", "cc-c", "dc-d") if all(r in reps for r in p.split("-"))])

    n_cal, per_b, n_img, n_txt, mu_norm = gap["calib"]
    out.append("")
    out.append(f"Calibration split: {n_cal} directories (" +
               ", ".join(f"{b} {n}" for b, n in per_b.items()) + f"), {n_img} image-input and {n_txt} "
               f"text-input embedded files; |mu_img| {mu_norm['img']:.3f}, |mu_txt| {mu_norm['txt']:.3f}.")
    fi, ft, nd = gap["files"]
    out.append("")
    out.append(f"### Session 8 modality gap, evaluation split ({nd} directories, {fi} image-input and {ft} "
               "text-input embedded files)")
    out.append("")
    out.append("| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img (pairs) | "
               "txt-txt (pairs) | img-txt (pairs) |")
    out.append("|---|---:|---:|---:|---:|")
    for name in ("before", "after"):
        g = gap[name]
        out.append(f"| {name} centering | {g['gap']:.3f} | " +
                   " | ".join(f"{g[k][0]:.3f} ({g[k][1]})" for k in ("img-img", "txt-txt", "img-txt")) + " |")
    out.append("")
    out.append("Paired 95% interval of (ac - a) - 0.5 * (c - a) lies entirely above zero: " +
               "; ".join(f"{n}: {'yes' if v else 'no'}" for n, v in verdict.items()) + ".")
    alive = len(verdict) == 2 and all(verdict.values())
    out.append(f"H8 {'survives' if alive else 'is dead'} under the session 8 kill criterion.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", help="cache directory under data/emb (default: the model name)")
    ap.add_argument("--manifest", default="data/manifest.jsonl", help="repo-relative")
    ap.add_argument("--dirs", default="data/dirs.jsonl", help="repo-relative")
    ap.add_argument("--split-dirs", default=None,
                    help="session 10: repo-relative dirs file the calibration split is drawn from "
                         "(default: --dirs); pass the session 5 file with a synthetic --dirs")
    ap.add_argument("--gt", default="data/gt_structural.jsonl", help="repo-relative")
    ap.add_argument("--criterion", choices=["s2", "s3"], default="s2",
                    help="s2: session 2 kill criterion; s3: session 3 pre-registered primary cells")
    ap.add_argument("--reps", default=",".join(REPS),
                    help=f"comma list of representations (default {','.join(REPS)}; session 8: {','.join(S8_REPS)})")
    ap.add_argument("--calib", type=float, default=0.0,
                    help="fraction of directories held out to compute the group means (session 8: 0.2); "
                         "their files give no queries; required by ac, acb, cc, dc; adds the session 8 section")
    ap.add_argument("--calib-seed", type=int, default=20260930)
    ap.add_argument("--tag", default="", help="ranks written to data/emb/<emb>/ranks<tag>.jsonl")
    ap.add_argument("--queries", choices=["eval", "dev"], default="eval",
                    help="session 9: eval = queries of the evaluation split (default, as before); "
                         "dev = queries whose directory is in the calibration split")
    ap.add_argument("--s9", action="store_true", help="session 9 output section (needs --calib)")
    ap.add_argument("--s10", action="store_true",
                    help="session 10 output section on a synthetic set (needs --calib; the gt rows carry "
                         "role, guest_frac and guest_dir from synth.py)")
    ap.add_argument("--s10-pair", default=None,
                    help="session 10: repo-relative ranks file of the other synthetic set; adds the paired "
                         "difference of the losses over the hosts common to both sets")
    ap.add_argument("--align-cv", action="store_true",
                    help="session 9, dev queries only: fit every F2 alignment on half of the calibration "
                         "directories (alternate folds per bucket, sorted) and score the dev queries of the other "
                         "half, so that the dev numbers of F2 are not in-sample; the alignments are fitted on "
                         "the calibration split as a whole otherwise")
    args = ap.parse_args()
    reps = args.reps.split(",")
    assert all(r in REPS + S8_REPS + S9_REPS + S10_REPS + S19_REPS for r in reps), reps
    assert args.calib > 0 or all(parse_rep(r)[0] == "u" and parse_rep(r)[1] not in ("f4", "f4b") for r in reps), \
        "centered, aligned and F4 reps need --calib"
    assert args.calib > 0 or (not args.s9 and args.queries == "eval"), "--s9 and --queries dev need --calib"
    assert args.calib > 0 or not args.s10, "--s10 needs --calib"

    emb_dir = os.path.join(DATA, "emb", args.emb or args.model)
    V = np.load(os.path.join(emb_dir, "vectors.npy"))
    with open(os.path.join(emb_dir, "index.jsonl")) as fh:
        index = [json.loads(l) for l in fh]
    with open(os.path.join(ROOT, args.manifest)) as fh:
        manifest = [json.loads(l) for l in fh]
    with open(os.path.join(ROOT, args.dirs)) as fh:
        dirs = {r["dir"]: r for r in (json.loads(l) for l in fh)}
    with open(os.path.join(ROOT, args.gt)) as fh:
        gt = [json.loads(l) for l in fh]
    split_src = dirs
    if args.split_dirs:
        with open(os.path.join(ROOT, args.split_dirs)) as fh:
            split_src = {r["dir"]: r for r in (json.loads(l) for l in fh)}
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache not in manifest order"
    assert all(r.get("done") for r in index), "cache incomplete"

    pos = {r["path"]: i for i, r in enumerate(manifest)}
    ok = np.array([r["ok"] for r in index])
    mods_all = np.array([r["modality"] for r in manifest])
    dir_list = sorted(d for d, r in dirs.items() if r["n_files"] >= 3)
    children = {d: [] for d in dir_list}
    for i, r in enumerate(manifest):
        if ok[i] and r["dir"] in children:
            children[r["dir"]].append(i)
    children = {d: np.array(v, int) for d, v in children.items()}

    calib, gap = set(), None
    if args.calib > 0:
        calib, is_img, in_calib, mu, Vc = centered_space(V, ok, mods_all, manifest, split_src, args.calib, args.calib_seed)
        eval_dirs = [d for d in dir_list if d not in calib]
        calib_dirs = [d for d in dir_list if d in calib]
        split_dirs = calib_dirs if args.queries == "dev" else eval_dirs
        gap = modality_gap(V, Vc, is_img, children, eval_dirs)
        gap["calib"] = (len(calib), {b: sum(bucket_of(split_src[d]["image_frac"]) == b for d in calib) for b in BUCKETS},
                        int((ok & in_calib & is_img).sum()), int((ok & in_calib & ~is_img).sum()),
                        {g: float(np.linalg.norm(m)) for g, m in mu.items()})
    else:
        Vc = None
        is_img = np.isin(mods_all, IMAGE_INPUTS)

    spaces = {"u": V, "c": Vc}
    extra = {}
    need = sorted({parse_rep(r)[0] for r in reps} - {"u", "c"}, key=ALIGNED.index)
    fold_of_dir = {}
    if need and args.align_cv:
        assert args.queries == "dev", "--align-cv is for the dev queries"
        for b in BUCKETS:
            for i, d in enumerate(d for d in calib_dirs if bucket_of(dirs[d]["image_frac"]) == b):
                fold_of_dir[d] = i % 2
        fold_spaces = []
        for f in (0, 1):
            fit_dirs = [d for d in calib_dirs if fold_of_dir[d] != f]
            fit_mask = in_calib & np.array([fold_of_dir.get(r["dir"], -1) != f for r in manifest])
            aligned, notes = align_spaces(Vc, is_img, ok, fit_mask, children, fit_dirs, need)
            fold_spaces.append(aligned)
            print(f"  fold {f}: aligned spaces fitted on {len(fit_dirs)} calibration directories: {notes}", file=sys.stderr)
        extra["align_notes"] = f"two-fold cross-fitting over the calibration directories, {notes}"
        for name in need:
            spaces[name] = [fold_spaces[0][name], fold_spaces[1][name]]
    elif need:
        aligned, extra["align_notes"] = align_spaces(Vc, is_img, ok, in_calib, children, calib_dirs, need)
        spaces.update(aligned)
        print(f"  aligned spaces {need} built: {extra['align_notes']}", file=sys.stderr)
    if args.s9:
        extra["gaps"] = {"uncentered": modality_gap(V, unit(V), is_img, children, split_dirs)["after"]}
        for name in ["c"] + need:
            if isinstance(spaces[name], list):
                continue                                  # cross-fitted: the test run reports the gap
            extra["gaps"]["centered" if name == "c" else name] = \
                modality_gap(V, spaces[name], is_img, children, split_dirs)["after"]

    def vecs(rep, fold=None):
        sp = spaces[parse_rep(rep)[0]]
        return sp[fold] if isinstance(sp, list) else sp

    def build_rep(rep, X, mods):
        space, base, param = parse_rep(rep)
        return build(base, X, mods, param)

    def build_full(rep, fold=None):
        return {d: build_rep(rep, vecs(rep, fold)[children[d]], mods_all[children[d]]) for d in dir_list}

    full = {rep: build_full(rep, 0 if isinstance(spaces[parse_rep(rep)[0]], list) else None) for rep in reps}
    n_reps = {rep: np.mean([len(full[rep][d]) for d in dir_list]) for rep in reps}
    for rep in reps:
        if parse_rep(rep)[1] in ("f4", "f4b"):
            n_reps[rep] = 2.0                             # two d-dimensional slots per folder, one entry

    in_dev = args.queries == "dev"
    queries = [g for g in gt if ok[pos[g["query_path"]]] and (g["relevant_dir"] in calib) == in_dev]
    dropped = Counter(g["modality"] for g in gt if not ok[pos[g["query_path"]]])
    n_dropped = sum(dropped.values())
    n_calib_q = sum(1 for g in gt if ok[pos[g["query_path"]]] and g["relevant_dir"] in calib)
    dir_idx = {d: j for j, d in enumerate(dir_list)}
    print(f"{len(queries)} {args.queries} queries ({n_dropped} dropped, no vector: {dict(dropped)}; "
          f"{n_calib_q} in calibration directories), "
          f"{len(dir_list)} directories ranked", file=sys.stderr)

    bias = None
    if any(parse_rep(r)[1] == "f4b" for r in reps):
        dev_q = [g for g in gt if ok[pos[g["query_path"]]] and g["relevant_dir"] in calib]
        bias, n_bias = f4_bias(Vc, is_img, children, pos, dev_q)
        extra["f4_bias"] = (bias, n_bias)
        print(f"  F4b bias {bias} over {n_bias} dev queries", file=sys.stderr)
    if args.s9:
        extra["purity"] = {rep: purity(rep, vecs(rep), mods_all, is_img, children, split_dirs)
                           for rep in reps if parse_rep(rep)[1] == "tb"}

    # full-representation scores for every query at once, per rep: max over reps of each dir
    qpos = [pos[g["query_path"]] for g in queries]
    q_img = is_img[qpos]
    q_fold = np.array([fold_of_dir.get(g["relevant_dir"], -1) for g in queries])
    ranks = {rep: np.zeros(len(queries), int) for rep in reps}

    def rank_rep(rep, W, reps_by_dir, qsel):
        """ranks of the queries qsel (indices) against reps_by_dir built in space W."""
        Q = query_vectors(rep, W[[qpos[i] for i in qsel]], q_img[qsel], bias)
        allR = np.concatenate([reps_by_dir[d] for d in dir_list])
        owner = np.concatenate([np.full(len(reps_by_dir[d]), j) for j, d in enumerate(dir_list)])
        S = Q @ allR.T                                   # (nq, total reps)
        dir_scores = np.full((len(qsel), len(dir_list)), -np.inf, np.float32)
        order = np.argsort(owner, kind="stable")
        bounds = np.searchsorted(owner[order], np.arange(len(dir_list) + 1))
        S = S[:, order]
        for j in range(len(dir_list)):
            if bounds[j + 1] > bounds[j]:
                dir_scores[:, j] = S[:, bounds[j]:bounds[j + 1]].max(axis=1)
        for k, qi in enumerate(qsel):
            g = queries[qi]
            d0 = g["relevant_dir"]
            p = pos[g["query_path"]]
            keep = children[d0][children[d0] != p]
            R = build_rep(rep, W[keep], mods_all[keep])
            # The own-directory score is compared in the dtype of the score row. Before the session 13
            # correction a float64 representative (base "p") gave a float64 own score that was rounded
            # into the float32 row and then compared against its unrounded self, so the query's own
            # directory counted as scoring strictly higher than itself in about half the queries.
            own = np.float32((R @ Q[k]).max()) if len(R) else np.float32(-np.inf)
            s = dir_scores[k].copy()
            s[dir_idx[d0]] = own
            assert s.dtype == np.float32 and not (s[dir_idx[d0]] > own)
            ranks[rep][qi] = 1 + int((s > own).sum())

    for rep in reps:
        if isinstance(spaces[parse_rep(rep)[0]], list):
            for f in (0, 1):
                rank_rep(rep, vecs(rep, f), full[rep] if f == 0 else build_full(rep, f), np.where(q_fold == f)[0])
        else:
            rank_rep(rep, vecs(rep), full[rep], np.arange(len(queries)))
        print(f"  rep {rep} done", file=sys.stderr)

    with open(os.path.join(emb_dir, f"ranks{args.tag}.jsonl"), "w") as fh:
        for qi, g in enumerate(queries):
            fh.write(json.dumps({**g, **{f"rank_{rep}": int(ranks[rep][qi]) for rep in reps}}) + "\n")

    qb = np.array([g["image_frac_bucket"] for g in queries])
    qm = np.array([g["modality"] for g in queries])
    qd = np.array([g["relevant_dir"] for g in queries])

    def recall_row(sel):
        return {rep: [float((ranks[rep][sel] <= k).mean()) if sel.any() else float("nan") for k in KS] for rep in reps}

    def cell_res(sel, seed):
        """recall@5 over the same 1000 resamples of the cell's directories, per rep."""
        cdirs = sorted(set(qd[sel]))
        rng = np.random.default_rng(seed)
        idx = rng.integers(0, len(cdirs), size=(N_BOOT, len(cdirs)))
        res = {}
        for rep in reps:
            hb = defaultdict(lambda: [0, 0])
            for d, r in zip(qd[sel], ranks[rep][sel]):
                hb[d][0] += int(r <= 5)
                hb[d][1] += 1
            res[rep] = boot(hb, cdirs, idx)
        return res, len(cdirs)

    def cell_boot(sel, seed):
        """recall@5 bootstrap per rep and paired diffs, resampling directories in the cell."""
        res, nd = cell_res(sel, seed)
        ci = {rep: np.percentile(res[rep], [2.5, 97.5]) for rep in reps}
        diff = {f"{x}-a": np.percentile(res[x] - res["a"], [2.5, 97.5]) for x in ("b", "c", "c4", "c2", "d") if x in res}
        if "d" in res and "c" in res:
            diff["d-c"] = np.percentile(res["d"] - res["c"], [2.5, 97.5])
        return ci, diff, nd

    def fmt(x):
        return f"{x:.3f}"

    out = []
    out.append(f"Model: {args.model}. Queries: {len(queries)} over {len(set(qd))} directories; "
               f"{len(dir_list)} directories ranked (random recall@k = k/{len(dir_list)}). "
               f"Queries dropped for lack of a vector: {n_dropped} {dict(dropped)}." +
               (f" Queries in calibration directories{', not used' if not in_dev else ' (dev, used)'}: {n_calib_q}."
                if calib else ""))
    out.append("")
    out.append("Mean representative vectors per directory: " +
               ", ".join(f"{rep} {n_reps[rep]:.2f}" for rep in reps) + ".")

    def table(title, cells):
        out.append("")
        out.append(f"### {title}")
        out.append("")
        out.append("| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |")
        out.append("|---|---:|---:|---|---:|---:|---:|---:|---|")
        for name, sel, seed in cells:
            if not sel.any():
                continue
            rr = recall_row(sel)
            ci, diff, nd = cell_boot(sel, seed)
            for rep in reps:
                lo, hi = ci[rep]
                out.append(f"| {name} | {int(sel.sum())} | {nd} | {rep} | " +
                           " | ".join(fmt(x) for x in rr[rep]) + f" | [{fmt(lo)}, {fmt(hi)}] |")

    everything = np.ones(len(queries), bool)
    table("All queries", [("all", everything, 1)])
    table("Per image_frac bucket, all query modalities",
          [(b, qb == b, 10 + i) for i, b in enumerate(BUCKETS)])
    table("Per query modality, all buckets",
          [(m, qm == m, 20 + i) for i, m in enumerate(MODALITIES) if m != "pdf_scanned"])
    table("Image queries per bucket",
          [(f"image {b}", (qb == b) & (qm == "image"), 30 + i) for i, b in enumerate(BUCKETS)])
    table("Text-like queries (text, table, pdf_text, other) per bucket",
          [(f"textlike {b}", (qb == b) & np.isin(qm, ["text", "table", "pdf_text", "other"]), 40 + i)
           for i, b in enumerate(BUCKETS)])

    if args.s10:
        pair = None
        if args.s10_pair:
            with open(os.path.join(ROOT, args.s10_pair)) as fh:
                pair = [json.loads(l) for l in fh]
        s10_section(out, queries, ranks, cell_res, fmt, reps, n_reps, full, manifest, children, V, Vc, pair)
    elif args.criterion == "s3":
        s3_section(out, qb, qm, recall_row, cell_boot, fmt, reps)
        if args.calib > 0 and not args.s9:
            s8_section(out, qb, qm, ranks, cell_res, fmt, reps, gap)
        if args.s9:
            s9_section(out, qb, qm, ranks, cell_res, fmt, reps, n_reps, args.queries, extra)
    else:
        # kill criterion: image queries in [.5,.8) and [.8,1], b and c vs a, paired bootstrap on recall@5
        out.append("")
        out.append("### Kill criterion: image queries, recall@5, paired bootstrap over directories")
        out.append("")
        out.append("| bucket | queries | dirs | " + " | ".join(reps) +
                   " | b-a | b-a 95% CI | c-a | c-a 95% CI | d-a | d-a 95% CI |")
        out.append("|---|---:|---:|" + "---:|" * len(reps) + "---:|---|---:|---|---:|---|")
        verdict = {}
        for i, b in enumerate(BUCKETS):
            sel = (qb == b) & (qm == "image")
            if not sel.any():
                continue
            rr = recall_row(sel)
            ci, diff, nd = cell_boot(sel, 30 + i)
            r5 = {rep: rr[rep][2] for rep in reps}
            out.append(f"| {b} | {int(sel.sum())} | {nd} | " + " | ".join(fmt(r5[rep]) for rep in reps) + " | " +
                       " | ".join(f"{r5[x] - r5['a']:+.3f} | [{diff[x + '-a'][0]:+.3f}, {diff[x + '-a'][1]:+.3f}]"
                                  for x in ("b", "c", "d")) + " |")
            if b in ("[.5,.8)", "[.8,1]"):
                verdict[b] = {x: bool(diff[x + "-a"][0] > 0) for x in ("b", "c")}
        out.append("")
        alive = all(verdict[b]["b"] or verdict[b]["c"] for b in verdict)
        out.append("Paired 95% interval of the difference excludes zero (lower bound > 0): " +
                   "; ".join(f"{b}: b-a {'yes' if v['b'] else 'no'}, c-a {'yes' if v['c'] else 'no'}"
                             for b, v in verdict.items()) + ".")
        out.append(f"Claim {'survives' if alive else 'is dead'} under the session 2 kill criterion.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
