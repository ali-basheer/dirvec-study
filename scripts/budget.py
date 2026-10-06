#!/usr/bin/env python3
"""dirvec session 21: what to store in a fixed number of bytes of a folder's metadata (BRIEF.md, session 21).

A folder's summary sits in its metadata and may take B bytes. Each policy below fills at most B bytes;
the float32 query is scored against what is stored and a folder's score is its largest cosine. A vector
at one bit per dimension takes ceil(dim / 8) bytes, so B bytes hold n = B // ceil(dim / 8) of them.

  mean      the pooled mean (eval.py's a) in the most precise of f32, f16, int8, int4, bin that fits B
  kindmean  one mean per kind (eval.py's b), all in the most precise format in which they fit B
            together; when one bit each does not fit, the kinds with the most files are kept
  sample    n files' vectors at one bit. The n are dealt to the kinds present one at a time, the kind
            with the most files first; a kind keeps its files with the smallest hash priority
  fsample   the same with a fixed share: every kind present keeps its n // kinds files of smallest
            priority and unused slots stay empty (when n is below the number of kinds, the n kinds
            with the most files keep one file each)
  usample   the n files with the smallest hash priority, kinds ignored, one bit
  ffirst    n files by farthest-first traversal from the file nearest the mean, one bit
  kmeans    min(n, files) centroids of spherical k-means over all files, one bit
  medoid    for each of those clusters the member nearest its centroid, one bit (a real file's vector;
            members within 1e-6 of the nearest count as tied and the first in manifest order is taken)
  kkind     the allotment of `sample`; each kind's files reduced to its allotment by k-means, one bit
  allbits   every file at one bit on its first m dimensions, m = min(dim, 8 * (B // files)); the query
            is cut to the same m dimensions and renormalised

A kind is the manifest's modality label (image, pdf_text, pdf_scanned, text, table, other). A folder
with at most n files is stored whole, all its files at one bit, by every policy but mean, kindmean
and fsample. The hash priority of a file is sha1("21:" + its manifest path), so a folder's sample is
fixed by its file names, needs no clustering, and every stored vector is a file's own. usample merges
exactly (the bottom-n of a union is the bottom-n of the two bottom-n samples), and so does fsample
whenever n is at least the number of kinds; sample, which refills unused slots, does not. Rows named
sample#22 to #25 and usample#22 to #25 repeat the two samples under other hash seeds. k-means is
spherical, in kernel form on the folder's cosine matrix, seeded by farthest-first traversal, at most
25 Lloyd steps, no random numbers. Leave-one-out as eval.py: the query's own folder is rebuilt
without the query, then stored. "Not whole" at a budget: the queries whose folder holds more than n
files besides the query.

Checks before any number is printed: the mean in f32 must reproduce the ranks file's rank_a, and every
file opened in f32 its rank_d, query for query (exit 3 otherwise).

  budget.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s19 --manifest data/manifest_s19.jsonl
            --dirs data/dirs_s19.jsonl --gt data/gt_structural_s19.jsonl --calib-seed 20261104
            --ranks data/emb/jina-embeddings-v4_s19/ranks_s19_e1.jsonl --label "S19 E1" --tag _s21_e1
            [--registered]
Writes markdown to stdout and the per-query ranks to data/emb/<emb>/ranks<tag>.jsonl.
"""
import argparse
import hashlib
import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval as ev  # noqa: E402
import quant as qn  # noqa: E402

BUDGETS = [int(b) for b in os.environ.get("S21_BUDGETS", "512,1024,2048,4096,8192").split(",")]   # the variables are for
REG_BUDGET = int(os.environ.get("S21_REG_BUDGET", 2048))                                             # the self-test only
POLICIES = ["mean", "kindmean", "sample", "fsample", "usample", "ffirst", "kmeans", "medoid", "kkind", "allbits"]
SIZE_BINS = [("3 to 10", 3, 10), ("11 to 30", 11, 30), ("31 to 100", 31, 10 ** 9)]
MARGIN, SESOI, MIN_OWNERS = 0.02, 0.05, 100
TIE = 1e-5
NEAR = 1e-6                               # scores this close to the own folder's are near-ties (float32 cosines)
REGISTERED = ([512, 1024, 2048, 4096, 8192], 2048)
PRIO_SEED = 21
MORE_SEEDS = [22, 23, 24, 25]            # the two samples again with other hash seeds, reported beside seed 21
MODS = ev.MODALITIES


def lab(B):
    return f"{B} B" if B < 1024 else f"{B // 1024} KiB"


def prio(path, seed=PRIO_SEED):
    return int(hashlib.sha1(f"{seed}:{path}".encode()).hexdigest()[:15], 16)


def bits(X):
    """One bit per dimension, decoded: +1 / -1 scaled to unit length."""
    X = np.asarray(X, np.float32)
    return np.where(X >= 0, np.float32(1.0), np.float32(-1.0)) / np.float32(np.sqrt(X.shape[-1]))


def mean_format(B, dim, n_vec=1):
    """The most precise format in which n_vec vectors fit B bytes, or None."""
    return next((f for f in qn.FORMATS if n_vec * qn.vec_bytes(f, dim) <= B), None)


def allot(kinds, n):
    """n slots dealt to the kinds present, one at a time, the kind with the most files first (ties in
    the order of eval.py's MODALITIES); a kind takes no more slots than it has files. {kind: slots}."""
    cnt = Counter(kinds)
    order = sorted(cnt, key=lambda m: (-cnt[m], MODS.index(m)))
    got = {m: 0 for m in order}
    left = min(n, len(kinds))
    while left > 0:
        for m in order:
            if left > 0 and got[m] < cnt[m]:
                got[m] += 1
                left -= 1
    return got


def ffirst_idx(G, n):
    """Farthest-first traversal on a cosine matrix: start at the row with the largest row sum (the file
    nearest the mean), then add the file whose largest cosine to those chosen is smallest."""
    m = len(G)
    if n >= m:
        return list(range(m))
    first = int(np.argmax(G.sum(axis=1)))
    chosen = [first]
    best = G[first].astype(np.float64).copy()
    best[first] = np.inf
    while len(chosen) < n:
        j = int(np.argmin(best))
        chosen.append(j)
        best = np.maximum(best, G[j])
        best[chosen] = np.inf
    return chosen


def kmeans(G, k, iters=25):
    """Spherical k-means of unit vectors from their cosine matrix G. Returns (labels 0..k'-1, medoids):
    the member of each cluster nearest its centroid. k' can be below k when a cluster empties."""
    m = len(G)
    if k >= m:
        return np.arange(m), list(range(m))
    seeds = ffirst_idx(G, k)
    lb = np.argmax(G[:, seeds], axis=1)
    lb[seeds] = np.arange(k)
    G64 = G.astype(np.float64)
    sim = None
    for _ in range(iters):
        A = np.zeros((m, k))
        A[np.arange(m), lb] = 1.0
        S = G64 @ A                                           # cosines summed over each cluster's members
        nrm = np.sqrt(np.maximum((A * S).sum(axis=0), 1e-18))   # length of each cluster's summed vector
        sim = S / nrm
        sim[:, A.sum(axis=0) == 0] = -np.inf
        new = np.argmax(sim, axis=1)
        if np.array_equal(new, lb):
            break
        lb = new
    A = np.zeros((m, k))
    A[np.arange(m), lb] = 1.0
    S = G64 @ A
    sim = S / np.sqrt(np.maximum((A * S).sum(axis=0), 1e-18))
    used = [j for j in range(k) if A[:, j].any()]
    med = []
    for j in used:                       # the two members of a pair are equally near their centroid:
        sj = np.where(lb == j, sim[:, j], -np.inf)   # members within 1e-6 of the nearest tie, the first is taken
        med.append(int(np.argmax(sj >= sj.max() - 1e-6)))
    return np.searchsorted(used, lb), med


def centroids(X, lb):
    """Unit sums of the rows of X per label, one bit per dimension."""
    k = int(lb.max()) + 1
    C = np.zeros((k, X.shape[1]), np.float32)
    np.add.at(C, lb, X)
    return bits(C)


_KM = {}


class Folder:
    """One folder's embedded files: rows of the manifest, unit vectors, cosines, kinds, priorities."""

    def __init__(self, rows, V, mods_all, paths):
        self.rows = np.asarray(rows, int)
        self.X = ev.unit(V[self.rows]).astype(np.float32)
        self.G = self.X @ self.X.T
        self.kinds = [str(mods_all[i]) for i in self.rows]
        self.prio = {sd: np.array([prio(paths[i], sd) for i in self.rows], dtype=np.int64)
                     for sd in [PRIO_SEED] + MORE_SEEDS}


def choose(fd, keep, n, policy, seed=PRIO_SEED):
    """What `policy` stores of the files fd[keep] in n one-bit vectors.
    Returns ("files", positions in fd) or ("vecs", stored unit vectors)."""
    keep = np.asarray(keep, int)
    pr = fd.prio[seed]
    if policy == "fsample":                                   # fixed share: no refill, so not whole even if n >= files
        kinds = [fd.kinds[i] for i in keep]
        cnt = Counter(kinds)
        order = sorted(cnt, key=lambda m: (-cnt[m], MODS.index(m)))
        q = n // max(len(order), 1)
        if q == 0:
            order, q = order[:n], 1
        files = []
        for m in order:
            sub = keep[[i for i, kd in enumerate(kinds) if kd == m]]
            files.append(sub[np.argsort(pr[sub], kind="stable")[:q]])
        return "files", (np.concatenate(files) if files else keep)
    if n >= len(keep) or len(keep) == 0:
        return "files", keep
    if policy == "usample":
        return "files", keep[np.argsort(pr[keep], kind="stable")[:n]]
    if policy in ("sample", "kkind"):
        kinds = [fd.kinds[i] for i in keep]
        got = allot(kinds, n)
        files, vecs = [], []
        for m, q in got.items():
            if q == 0:
                continue
            sub = keep[[i for i, kd in enumerate(kinds) if kd == m]]
            if policy == "sample":
                files.append(sub[np.argsort(pr[sub], kind="stable")[:q]])
            elif q >= len(sub):
                vecs.append(bits(fd.X[sub]))
            else:
                lb, _ = kmeans(fd.G[np.ix_(sub, sub)], q)
                vecs.append(centroids(fd.X[sub], lb))
        return ("files", np.concatenate(files)) if policy == "sample" else ("vecs", np.concatenate(vecs))
    if policy == "ffirst":
        return "files", keep[ffirst_idx(fd.G[np.ix_(keep, keep)], n)]
    key = (id(fd), n, len(keep), int(keep.sum()))             # kmeans and medoid share one clustering
    if key not in _KM:
        _KM.clear() if len(_KM) > 200000 else None
        _KM[key] = kmeans(fd.G[np.ix_(keep, keep)], n)
    lb, med = _KM[key]
    if policy == "medoid":
        return "files", keep[med]
    if policy == "kmeans":
        return "vecs", centroids(fd.X[keep], lb)
    raise ValueError(policy)


def kindmean(V, rows, mods_all, B, dim):
    """One mean per kind in the most precise format in which they fit B together (stored vectors)."""
    if len(rows) == 0:
        return np.zeros((0, dim), np.float32)
    mods = mods_all[rows]
    R = ev.build("b", V[rows], mods)                       # unit means, in MODALITIES order
    present = [m for m in MODS if (mods == m).any()]
    f = mean_format(B, dim, len(present))
    if f is None:
        cnt = Counter(mods)
        top = sorted(present, key=lambda m: (-cnt[m], MODS.index(m)))[:max(1, B // qn.vec_bytes("bin", dim))]
        R = R[[i for i, m in enumerate(present) if m in top]]
        f = "bin"
    return qn.store(R, f)


def oboot(z, owners, seed, B=10000):
    """Owner-weighted mean of z with percentile intervals from B resamples of the owners (session 19's
    registered estimator). Returns (point, (lo95, hi95), (lo98.33, hi98.33), owners)."""
    keys = sorted(set(owners))
    gi = {k: i for i, k in enumerate(keys)}
    g = np.array([gi[k] for k in owners])
    gm = np.bincount(g, weights=z, minlength=len(keys)) / np.bincount(g, minlength=len(keys))
    rng = np.random.default_rng(seed)
    bs = np.empty(B)
    for i0 in range(0, B, 1000):
        idx = rng.integers(0, len(keys), size=(min(1000, B - i0), len(keys)))
        bs[i0:i0 + len(idx)] = gm[idx].mean(axis=1)
    q = np.percentile(bs, [2.5, 97.5, 100 * 0.05 / 6, 100 * (1 - 0.05 / 6)])
    return float(gm.mean()), (float(q[0]), float(q[1])), (float(q[2]), float(q[3])), len(keys)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--gt", required=True)
    ap.add_argument("--calib", type=float, default=0.2)
    ap.add_argument("--calib-seed", type=int, required=True)
    ap.add_argument("--ranks", required=True, help="repo-relative eval.py ranks file: rank_a, rank_c, rank_d of the same queries")
    ap.add_argument("--label", default="")
    ap.add_argument("--tag", default="_s21")
    ap.add_argument("--registered", action="store_true", help="print the registered tests of session 21 (S19 under E1)")
    ap.add_argument("--limit-queries", type=int, default=0, help="tests only: the first N evaluation queries")
    args = ap.parse_args()
    R = ev.ROOT
    L = args.label

    emb_dir = os.path.join(ev.DATA, "emb", args.emb)
    V = np.load(os.path.join(emb_dir, "vectors.npy"))
    index = [json.loads(l) for l in open(os.path.join(emb_dir, "index.jsonl"))]
    manifest = [json.loads(l) for l in open(os.path.join(R, args.manifest))]
    dirs = {r["dir"]: r for r in (json.loads(l) for l in open(os.path.join(R, args.dirs)))}
    gt = [json.loads(l) for l in open(os.path.join(R, args.gt))]
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache not in manifest order"
    if args.registered:
        if not all(r.get("owner") for r in dirs.values()):
            sys.exit("--registered: a directory row has no owner; the registered tests are owner-weighted (exit before any number)")
        if (BUDGETS, REG_BUDGET) != REGISTERED and not os.environ.get("S21_SELFTEST"):
            sys.exit("--registered: the budgets are not the registered ones (S21_BUDGETS or S21_REG_BUDGET is set)")
    pos = {r["path"]: i for i, r in enumerate(manifest)}
    paths = [r["path"] for r in manifest]
    ok = np.array([bool(r["ok"]) for r in index])
    mods_all = np.array([r["modality"] for r in manifest])
    dir_list = sorted(d for d, r in dirs.items() if r["n_files"] >= 3)
    dir_idx = {d: j for j, d in enumerate(dir_list)}
    n_dirs = len(dir_list)
    children = {d: [] for d in dir_list}
    for i, r in enumerate(manifest):
        if ok[i] and r["dir"] in children:
            children[r["dir"]].append(i)
    dim = V.shape[1]
    bin_bytes = qn.vec_bytes("bin", dim)
    qn.check_store(dim)

    calib = ev.calib_split(dirs, args.calib, args.calib_seed)
    q_eval = [g for g in gt if ok[pos[g["query_path"]]] and g["relevant_dir"] not in calib]
    ref = {}
    for l in open(os.path.join(R, args.ranks)):
        x = json.loads(l)
        ref[x["query_path"]] = x
    same_set = {g["query_path"] for g in q_eval} == set(ref)
    if args.limit_queries:
        q_eval = q_eval[:args.limit_queries]
    nq = len(q_eval)
    qrow = np.array([pos[g["query_path"]] for g in q_eval])
    Q = V[qrow]
    j0s = np.array([dir_idx[g["relevant_dir"]] for g in q_eval])
    print(f"{L}: {nq} evaluation queries, {n_dirs} directories ranked, {dim} dimensions", file=sys.stderr)

    folders = [Folder(children[d], V, mods_all, paths) for d in dir_list]
    n_files = np.array([len(fd.rows) for fd in folders])
    col_of = {}                                               # manifest row -> column of the file scores
    for fd in folders:
        for i in fd.rows:
            col_of[int(i)] = len(col_of)
    file_rows = np.array(sorted(col_of, key=col_of.get), int)
    fcols = [np.array([col_of[int(i)] for i in fd.rows], int) for fd in folders]
    starts = np.cumsum([0] + [len(c) for c in fcols[:-1]])
    nonempty = n_files > 0
    qpos_in = []                                              # the query's position in its folder
    for k in range(nq):
        w = np.where(folders[j0s[k]].rows == qrow[k])[0]
        assert len(w) == 1
        qpos_in.append(int(w[0]))

    ranks_lo, ranks_hi = {}, {}       # every folder within NEAR of the own folder counted for it, or against it

    def rank_from(scores, own, name=None):
        scores[np.arange(nq), j0s] = own
        if name is not None:
            ranks_lo[name] = 1 + (scores > (own + NEAR)[:, None]).sum(axis=1)
            ranks_hi[name] = (scores >= (own - NEAR)[:, None]).sum(axis=1)   # the own folder is one of these
        return 1 + (scores > own[:, None]).sum(axis=1)

    def dir_max_files(S):
        out = np.full((S.shape[0], n_dirs), -np.inf, np.float32)
        out[:, nonempty] = np.maximum.reduceat(S, starts[nonempty], axis=1)
        return out

    # ---- reference rows and the two reproduction checks (f32; the products laid out as eval.py's)
    A_all = np.concatenate([ev.build("a", V[fd.rows], mods_all[fd.rows]) for fd in folders if len(fd.rows)])
    own_a = np.zeros(nq, np.float32)
    own_d = np.zeros(nq, np.float32)
    keep_rows = []
    for k in range(nq):
        fd = folders[j0s[k]]
        kr = np.delete(fd.rows, qpos_in[k])
        keep_rows.append(kr)
        own_a[k] = np.float32((ev.build("a", V[kr], mods_all[kr]) @ Q[k]).max()) if len(kr) else np.float32(-np.inf)
        own_d[k] = np.float32((V[kr] @ Q[k]).max()) if len(kr) else np.float32(-np.inf)
    sa = np.full((nq, n_dirs), -np.inf, np.float32)
    sa[:, nonempty] = Q @ A_all.T
    ranks = {"a_f32": rank_from(sa, own_a)}
    sd = dir_max_files(Q @ V[file_rows].T)
    ranks["d_f32"] = rank_from(sd, own_d)
    out = [f"## {L}: {args.model} ({dim} dimensions; one bit per dimension is {bin_bytes} bytes a vector)", ""]
    diffs, loose = {"a": 0, "d": 0}, {"a": 0, "d": 0}
    for b, sc, own in (("a", sa, own_a), ("d", sd, own_d)):
        for k, g in enumerate(q_eval):
            want = int(ref[g["query_path"]][f"rank_{b}"]) if g["query_path"] in ref else None
            if want is None or want == int(ranks[f"{b}_f32"][k]):
                continue
            row = sc[k].astype(np.float64)
            lo = 1 + int((row > own[k] + TIE).sum())
            hi = int((row >= own[k] - TIE).sum())            # the own folder is one of these
            if lo <= want <= hi:
                loose[b] += 1                                 # a folder within TIE of the own folder decides it
            else:
                diffs[b] += 1
    del sa, sd
    ok_rep = same_set and not any(diffs.values())
    out.append(f"Reproduction of {args.ranks}: {nq} queries here, {len(ref)} there, same set: "
               f"{'yes' if same_set else 'NO'}; queries whose rank differs: a {diffs['a'] + loose['a']}, d "
               f"{diffs['d'] + loose['d']}, of which explained by a folder scoring within {TIE:g} of the own folder: a "
               f"{loose['a']}, d {loose['d']}. {'Reproduced rank for rank.' if ok_rep and not any(loose.values()) else 'Reproduced up to near-ties.' if ok_rep else 'NOT REPRODUCED.'}")
    if not ok_rep:
        print("\n".join(out))
        sys.exit(3)
    out.append("")
    if all("rank_c" in ref[g["query_path"]] for g in q_eval):
        ranks["c_f32"] = np.array([int(ref[g["query_path"]]["rank_c"]) for g in q_eval])

    # ---- one bit per dimension: every file's score against every query, once
    Bfile = bits(ev.unit(V[file_rows]))
    Sbin = np.empty((nq, len(file_rows)), np.float32)
    for i0 in range(0, nq, 2048):
        Sbin[i0:i0 + 2048] = Q[i0:i0 + 2048] @ Bfile.T
    Dbin = dir_max_files(Sbin)                                # every folder stored whole
    own_bin_cols = [fcols[j0s[k]][np.arange(len(fcols[j0s[k]])) != qpos_in[k]] for k in range(nq)]
    own_whole = np.array([Sbin[k, c].max() if len(c) else -np.inf for k, c in enumerate(own_bin_cols)], np.float32)
    ranks["d_bin"] = rank_from(Dbin.copy(), own_whole)
    del Bfile

    used = {}                                                 # row -> bytes used per folder (all files)

    def run_policy(policy, B, seed=PRIO_SEED):
        n = B // bin_bytes
        assert n >= 1, "the budget holds no one-bit vector"
        name = f"{policy}@{B}" if seed == PRIO_SEED else f"{policy}#{seed}@{B}"
        refill = policy != "fsample"                          # fsample leaves slots empty, so it is asked every time
        scores = Dbin.copy()
        by = np.minimum(n_files, n) * bin_bytes
        vec_j, vec_m = [], []
        for j, fd in enumerate(folders):
            if (n_files[j] <= n and refill) or n_files[j] == 0:
                continue
            kind, x = choose(fd, np.arange(n_files[j]), n, policy, seed)
            by[j] = len(x) * bin_bytes
            if kind == "vecs":
                vec_j.append(j)
                vec_m.append(x)
            elif len(x) < n_files[j]:
                scores[:, j] = Sbin[:, fcols[j][x]].max(axis=1)
        if vec_j:
            M = np.concatenate(vec_m)
            st = np.cumsum([0] + [len(m) for m in vec_m[:-1]])
            for i0 in range(0, nq, 4096):
                scores[i0:i0 + 4096, vec_j] = np.maximum.reduceat(Q[i0:i0 + 4096] @ M.T, st, axis=1)
        own = np.empty(nq, np.float32)
        for k in range(nq):
            fd = folders[j0s[k]]
            keep = np.delete(np.arange(n_files[j0s[k]]), qpos_in[k])
            if (len(keep) <= n and refill) or len(keep) == 0:
                own[k] = own_whole[k]
                continue
            kind, x = choose(fd, keep, n, policy, seed)
            own[k] = Sbin[k, fcols[j0s[k]][x]].max() if kind == "files" else np.float32((x @ Q[k]).max())
        ranks[name] = rank_from(scores, own, name)
        used[name] = by

    def run_mean(B):
        f = mean_format(B, dim)
        name = f"mean@{B}"
        if f is None:
            return None
        scores = np.full((nq, n_dirs), -np.inf, np.float32)
        scores[:, nonempty] = Q @ qn.store(A_all, f).T
        own = np.array([np.float32((qn.store(ev.build("a", V[kr], mods_all[kr]), f) @ Q[k]).max()) if len(kr)
                        else np.float32(-np.inf) for k, kr in enumerate(keep_rows)], np.float32)
        ranks[name] = rank_from(scores, own, name)
        used[name] = np.full(n_dirs, qn.vec_bytes(f, dim))
        return f

    def run_kindmean(B):
        name = f"kindmean@{B}"
        reps = [kindmean(V, fd.rows, mods_all, B, dim) for fd in folders]
        M = np.concatenate([r if len(r) else np.zeros((1, dim), np.float32) for r in reps])
        st = np.cumsum([0] + [max(len(r), 1) for r in reps[:-1]])
        scores = np.maximum.reduceat(Q @ M.T, st, axis=1).astype(np.float32)
        scores[:, ~nonempty] = -np.inf
        own = np.empty(nq, np.float32)
        for k, kr in enumerate(keep_rows):
            r = kindmean(V, kr, mods_all, B, dim)
            own[k] = np.float32((r @ Q[k]).max()) if len(r) else np.float32(-np.inf)
        ranks[name] = rank_from(scores, own, name)
        used[name] = np.array([len(r) * (qn.vec_bytes(mean_format(B, dim, len(r)) or "bin", dim)) if len(r) else 0 for r in reps])

    def run_allbits(B):
        name = f"allbits@{B}"
        scores = Dbin.copy()
        m_of = np.array([min(dim, 8 * (B // max(f, 1))) for f in n_files])
        for m in sorted(set(m_of[(m_of < dim) & nonempty])):
            js = np.where((m_of == m) & nonempty)[0]
            M = np.concatenate([bits(folders[j].X[:, :m]) for j in js])
            st = np.cumsum([0] + [n_files[j] for j in js[:-1]])
            Qm = ev.unit(Q[:, :m]).astype(np.float32)
            scores[:, js] = np.maximum.reduceat(Qm @ M.T, st, axis=1)
        own = np.empty(nq, np.float32)
        for k in range(nq):
            fd = folders[j0s[k]]
            keep = np.delete(np.arange(n_files[j0s[k]]), qpos_in[k])
            m = min(dim, 8 * (B // max(len(keep), 1)))
            if m >= dim or len(keep) == 0:
                own[k] = own_whole[k]
            else:
                own[k] = np.float32((bits(fd.X[keep][:, :m]) @ ev.unit(Q[k, :m])).max())
        ranks[name] = rank_from(scores, own, name)
        used[name] = np.array([f * max(1, -(-int(m) // 8)) if f else 0 for f, m in zip(n_files, m_of)])

    fmts = {}
    for B in BUDGETS:
        fmts[B] = run_mean(B)
        run_kindmean(B)
        for p in ("sample", "fsample", "usample", "ffirst", "kmeans", "medoid", "kkind"):
            run_policy(p, B)
        for sd in MORE_SEEDS:
            run_policy("sample", B, sd)
            run_policy("usample", B, sd)
        run_allbits(B)
        _KM.clear()
        print(f"  {L} budget {lab(B)} done", file=sys.stderr)

    rows = [f"{p}@{B}" for B in BUDGETS for p in POLICIES if f"{p}@{B}" in ranks]
    rows += [f"{p}#{sd}@{B}" for B in BUDGETS for p in ("sample", "usample") for sd in MORE_SEEDS]
    with open(os.path.join(emb_dir, f"ranks{args.tag}.jsonl"), "w") as fh:
        for k, g in enumerate(q_eval):
            fh.write(json.dumps({"query_path": g["query_path"], "relevant_dir": g["relevant_dir"],
                                 **{f"rank_{r}": int(ranks[r][k]) for r in ["a_f32", "c_f32", "d_f32", "d_bin"] + rows
                                    if r in ranks},
                                 **{f"rank{w}_{r}": int(rk[r][k]) for w, rk in (("lo", ranks_lo), ("hi", ranks_hi))
                                    for r in (f"{p}@{REG_BUDGET}" for p in ("mean", "sample", "usample", "kmeans"))
                                    if r in rk}}) + "\n")

    # ---- cells
    qb = np.array([g["image_frac_bucket"] for g in q_eval])
    qm = np.array([g["modality"] for g in q_eval])
    qd = np.array([g["relevant_dir"] for g in q_eval])
    primary, _, majority, _ = ev.s3_cells(qb, qm)
    is_img_file = np.isin(mods_all, ev.IMAGE_INPUTS)
    has_sib = np.array([(is_img_file[kr] == is_img_file[qrow[k]]).any() if len(kr) else False
                        for k, kr in enumerate(keep_rows)])
    P1s, P2s = primary[0][1] & has_sib, primary[1][1] & has_sib
    allq, mino = np.ones(nq, bool), P1s | P2s
    cells = [("all", allq), ("minority", mino), ("P1s", P1s), ("P2s", P2s),
             ("M1", majority[0][1]), ("M2", majority[1][1])]
    nd = n_files[j0s]
    # the query's folder is not stored whole at budget B: it holds more than n files besides the query
    partial = {B: (nd - 1) > (B // bin_bytes) for B in BUDGETS}
    owned = all(dirs[d].get("owner") for d in dir_list)
    qo = np.array([dirs[d]["owner"] for d in qd]) if owned else qd

    def dcells(B):
        return [("all", allq), ("minority", mino), ("all, not whole", partial[B]), ("minority, not whole", mino & partial[B])]

    def wmean(x, sel):
        """The mean of x over the queries sel: over owners of the owner's mean on S19, over queries otherwise."""
        if not sel.any():
            return float("nan")
        if not owned:
            return float(x[sel].mean())
        _, g = np.unique(qo[sel], return_inverse=True)
        return float((np.bincount(g, weights=x[sel]) / np.bincount(g)).mean())

    def hit(r, rk=None):
        return ((rk or ranks)[r] <= 5).astype(float)

    def r5(r, sel):
        return f"{hit(r)[sel].mean():.3f}" if sel.any() else "n/a"

    def w5(r, sel):
        v = wmean(hit(r), sel)
        return "n/a" if v != v else f"{v:.3f}"

    out.append(f"Queries: {nq} evaluation queries over {len(set(qd))} directories"
               f"{' and ' + str(len(set(qo))) + ' owners' if owned else ''}; {n_dirs} directories ranked (calibration "
               f"seed {args.calib_seed}). Embedded files per directory: mean {n_files.mean():.1f}, median "
               f"{np.median(n_files):.0f}, 95th percentile {np.percentile(n_files, 95):.0f}, max {n_files.max()}. "
               f"Cells: " + ", ".join(f"{n} {int(sel.sum())}" for n, sel in cells) + ". minority is P1s and P2s together: "
               f"a query of the folder's minority input group that still has a sibling of its group. Not whole, at a "
               f"budget: the queries whose folder holds more files besides the query than the budget stores.")
    out.append("")
    out.append(f"### {L} what a budget holds")
    out.append("")
    out.append("| budget | one-bit vectors | folders stored whole | queries not whole | minority queries not whole | mean in | " +
               " | ".join(f"{p}: mean bytes" for p in POLICIES) + " |")
    out.append("|---|---:|---:|---:|---:|---|" + "---:|" * len(POLICIES))
    for B in BUDGETS:
        n = B // bin_bytes
        out.append(f"| {lab(B)} | {n} | {(n_files[nonempty] <= n).mean():.3f} | {int(partial[B].sum())} | "
                   f"{int((mino & partial[B]).sum())} | {fmts[B] or 'none'} | " +
                   " | ".join(f"{used[f'{p}@{B}'][nonempty].mean():.0f}" if f"{p}@{B}" in used else "n/a" for p in POLICIES) + " |")
    out.append("")
    wname = "owner-weighted" if owned else "query-weighted"
    out.append(f"### {L} recall@5 (the first three columns {wname}, as the tests; the others query-weighted, as eval.py's tables)")
    out.append("")
    out.append(f"| budget | policy | all, {wname} | minority, {wname} | minority not whole, {wname} | " +
               " | ".join(f"{n} ({int(sel.sum())})" for n, sel in cells) + " | " +
               " | ".join(f"all, {nm} files" for nm, _, _ in SIZE_BINS) + " | " +
               " | ".join(f"minority, {nm} files" for nm, _, _ in SIZE_BINS) + " |")
    out.append("|---|---|" + "---:|" * (3 + len(cells) + 2 * len(SIZE_BINS)))
    size_sel = [(nd >= lo) & (nd <= hi) for _, lo, hi in SIZE_BINS]

    def table_row(B, what, r):
        nw = w5(r, mino & partial[B]) if B else "n/a"
        return (f"| {lab(B) if B else 'none'} | {what} | {w5(r, allq)} | {w5(r, mino)} | {nw} | " +
                " | ".join(r5(r, sel) for _, sel in cells) + " | " + " | ".join(r5(r, sel) for sel in size_sel) + " | " +
                " | ".join(r5(r, sel & mino) for sel in size_sel) + " |")

    for refrow, what in (("a_f32", "the mean in f32"), ("c_f32", "c in f32 (eval.py)"), ("d_f32", "every file in f32"),
                         ("d_bin", "every file at one bit")):
        if refrow in ranks:
            out.append(table_row(0, what, refrow))
    for B in BUDGETS:
        for p in POLICIES:
            if f"{p}@{B}" in ranks:
                out.append(table_row(B, p, f"{p}@{B}"))
    out.append("")

    def interval(z, sel, seed):
        if owned:
            return oboot(z[sel], qo[sel], seed)
        keys = sorted(set(qd[sel]))
        gi = {k: i for i, k in enumerate(keys)}
        g = np.array([gi[k] for k in qd[sel]])
        zs = np.bincount(g, weights=z[sel], minlength=len(keys))
        ns = np.bincount(g, minlength=len(keys)).astype(float)
        idx = np.random.default_rng(seed).integers(0, len(keys), size=(1000, len(keys)))
        bs = zs[idx].sum(axis=1) / ns[idx].sum(axis=1)
        q = np.percentile(bs, [2.5, 97.5, 100 * 0.05 / 6, 100 * (1 - 0.05 / 6)])
        return float(z[sel].mean()), (float(q[0]), float(q[1])), (float(q[2]), float(q[3])), len(keys)

    def bseed(bi, ci, pi):                       # one bootstrap seed per budget, cell and pair, wherever it is printed
        return 21000 + 1000 * bi + 20 * ci + pi

    seeds = [PRIO_SEED] + MORE_SEEDS

    def srow(p, sd, B):
        return f"{p}@{B}" if sd == PRIO_SEED else f"{p}#{sd}@{B}"

    out.append(f"### {L} the two samples under five hash seeds ({', '.join(map(str, seeds))}; 21 is the registered one): "
               f"recall@5 ({wname}), lowest to highest, and sample - usample per seed")
    out.append("")
    out.append("| budget | cell | queries | sample | usample | sample - usample, seeds 21 to 25 |")
    out.append("|---|---|---:|---|---|---|")
    for B in BUDGETS:
        for cn, sel in dcells(B):
            if not sel.any():
                continue
            v = {p: [wmean(hit(srow(p, sd, B)), sel) for sd in seeds] for p in ("sample", "usample")}
            out.append(f"| {lab(B)} | {cn} | {int(sel.sum())} | " +
                       " | ".join(f"{min(v[p]):.3f} to {max(v[p]):.3f} (seed 21: {v[p][0]:.3f})" for p in ("sample", "usample")) +
                       " | " + ", ".join(f"{a - b:+.3f}" for a, b in zip(v["sample"], v["usample"])) + " |")
    out.append("")

    pairs = [("sample", "mean"), ("kmeans", "mean"), ("sample", "kmeans"), ("sample", "usample"), ("fsample", "sample"),
             ("fsample", "usample"), ("fsample", "mean"), ("kkind", "kmeans"), ("medoid", "kmeans"), ("ffirst", "sample"),
             ("allbits", "sample"), ("kindmean", "mean"), ("sample", None)]
    how = ("owner-weighted mean, 10,000 resamples of owners" if owned else
           "query-weighted mean, 1,000 resamples of the cell's directories")
    out.append(f"### {L} differences in recall@5 at equal bytes: point [95 percent interval] ({how})")
    out.append("")
    out.append("| budget | cell | queries | " + " | ".join(f"{x} - {y}" if y else "sample - every file in f32" for x, y in pairs) + " |")
    out.append("|---|---|---:|" + "---|" * len(pairs))
    for bi, B in enumerate(BUDGETS):
        for ci, (cn, sel) in enumerate(dcells(B)):
            cols = []
            for pi, (x, y) in enumerate(pairs):
                rx, ry = f"{x}@{B}", (f"{y}@{B}" if y else "d_f32")
                if rx not in ranks or ry not in ranks or sel.sum() < 2 or len(set(qo[sel])) < 2:
                    cols.append("n/a")
                    continue
                pt, i95, _, _ = interval(hit(rx) - hit(ry), sel, bseed(bi, ci, pi))
                cols.append(f"{pt:+.3f} [{i95[0]:+.3f}, {i95[1]:+.3f}]")
            out.append(f"| {lab(B)} | {cn} | {int(sel.sum())} | " + " | ".join(cols) + " |")
    out.append("")

    if args.registered:
        B = REG_BUDGET
        bi = BUDGETS.index(B)
        dc = dcells(B)
        out.append(f"### {L} the registered tests of session 21 (budget {lab(B)}; owner-weighted, 10,000 resamples of "
                   f"owners; a primary test is read on its 98.33 percent interval, the rows beside them have no reading)")
        out.append("")
        out.append("| test | queries | owners | point | 95% | 98.33% | reading |")
        out.append("|---|---:|---:|---:|---|---|---|")

        def reading(kind, lo, hi, no):
            if no < MIN_OWNERS:
                return f"inconclusive (fewer than {MIN_OWNERS} owners)"
            if kind == "loss":
                return ("confirmed (lower bound at or above +0.05)" if lo >= SESOI else
                        "below +0.05 (upper bound under +0.05)" if hi < SESOI else
                        "present, size open (lower bound above zero)" if lo > 0 else "inconclusive")
            if kind == "margin":
                return ("not inferior (lower bound at or above -0.02)" if lo >= -MARGIN else
                        "inferior (upper bound under -0.02)" if hi < -MARGIN else "inconclusive")
            return ("the kinds matter (lower bound above zero)" if lo > 0 else
                    "the uniform sample is better (upper bound below zero)" if hi < 0 else
                    "no difference at the margin (interval within -0.02 and +0.02)" if lo >= -MARGIN and hi <= MARGIN
                    else "inconclusive")

        tests = [("H21a", "sample", "mean", 3, 1, "loss"), ("H21b", "sample", "kmeans", 2, 0, "margin"),
                 ("H21c", "sample", "usample", 3, 1, "kinds")]
        for h, x, y, ci, ci_wide, kind in tests:
            pi = pairs.index((x, y))
            rx, ry = f"{x}@{B}", f"{y}@{B}"
            variants = [(f"{h} (primary): {x} - {y}, {dc[ci][0]}", dc[ci][1], bseed(bi, ci, pi), None, True),
                        (f"beside {h}: {x} - {y}, {dc[ci_wide][0]}", dc[ci_wide][1], bseed(bi, ci_wide, pi), None, False),
                        (f"beside {h}: {dc[ci][0]}, near-ties counted for the own folder", dc[ci][1], bseed(bi, ci, pi), ranks_lo, False),
                        (f"beside {h}: {dc[ci][0]}, near-ties counted against the own folder", dc[ci][1], bseed(bi, ci, pi), ranks_hi, False)]
            for name, sel, seed, rk, prim in variants:
                if sel.sum() < 2 or len(set(qo[sel])) < 2:
                    out.append(f"| {name} | {int(sel.sum())} | | | | | no test |")
                    continue
                pt, i95, i98, no = oboot(hit(rx, rk)[sel] - hit(ry, rk)[sel], qo[sel], seed)
                out.append(f"| {name} | {int(sel.sum())} | {no} | {pt:+.3f} | [{i95[0]:+.3f}, {i95[1]:+.3f}] | "
                           f"[{i98[0]:+.3f}, {i98[1]:+.3f}] | {reading(kind, i98[0], i98[1], no) if prim else 'none'} |")
        out.append("")
        out.append("Near-ties at this budget (a folder scoring within 1e-6 of the query's own folder): share of the queries "
                   "whose rank depends on how they are counted: " +
                   "; ".join(f"{p} " + ", ".join(f"{cn} {float((ranks_lo[f'{p}@{B}'][sel] != ranks_hi[f'{p}@{B}'][sel]).mean()) if sel.any() else float('nan'):.4f}"
                                                  for cn, sel in dc) for p in ("mean", "sample", "usample", "kmeans")) + ".")
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
