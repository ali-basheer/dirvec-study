#!/usr/bin/env python3
"""Self-test of scripts/budget.py (session 21): every row recomputed by a second, plain implementation.

Runs scripts/s19_selftest.py and keeps its synthetic set (110 directories, 48 dimensions), runs
budget.py on it with budgets of 12 to 192 bytes (2 to 32 one-bit vectors of 6 bytes; the mean in bin,
int4, int8, f16 and f32), then recomputes every policy at every budget for every evaluation query in
float64, from the vectors themselves: explicit centroids instead of the cosine-matrix form, loops
instead of gathered columns. It fails when a rank differs and the difference is not explained by a
folder scoring within 1e-5 of the query's own folder, when the rows that must coincide do not, or when
a policy stores more bytes than the budget.

  python3 scripts/s21_selftest.py        (about two minutes; writes data/*_t19* and removes them)
"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402

BUDGETS = [12, 24, 48, 96, 192]
POLICIES = ["mean", "kindmean", "sample", "fsample", "usample", "ffirst", "kmeans", "medoid", "kkind", "allbits"]
SEEDS = [21, 22, 23, 24, 25]
BYTES = {"f32": 4.0, "f16": 2.0, "int8": 1.0, "int4": 0.5, "bin": 0.125}
TIE = 1e-5
MODS = ev.MODALITIES


def unit(x):
    x = np.asarray(x, np.float64)
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-300)


def onebit(x):
    return unit(np.where(np.asarray(x) >= 0, 1.0, -1.0))


def stored(x, f):
    x = np.asarray(x, np.float32)
    if f == "f32":
        return unit(x)
    if f == "f16":
        return unit(x.astype(np.float16).astype(np.float64))
    if f in ("int8", "int4"):
        top = 127.0 if f == "int8" else 7.0
        return unit(np.rint(x.astype(np.float32) * (np.float32(top) / np.abs(x).max(axis=-1, keepdims=True))))
    return onebit(x)


def fit_format(B, dim, n):
    for f in ("f32", "f16", "int8", "int4", "bin"):
        if n * int(np.ceil(BYTES[f] * dim)) <= B:
            return f
    return None


def quotas(kinds, n):
    cnt = Counter(kinds)
    order = sorted(cnt, key=lambda m: (-cnt[m], MODS.index(m)))
    got = dict.fromkeys(order, 0)
    left, r = min(n, len(kinds)), 1
    while left > 0:
        for m in order:
            if cnt[m] >= r and left > 0:
                got[m] += 1
                left -= 1
        r += 1
    return got, order


def far_first(X, n):
    if n >= len(X):
        return list(range(len(X)))
    C = X @ X.T
    chosen = [int(np.argmax(X @ X.sum(axis=0)))]
    while len(chosen) < n:
        worst = np.array([np.inf if i in chosen else max(C[i, j] for j in chosen) for i in range(len(X))])
        chosen.append(int(np.argmin(worst)))
    return chosen


def lloyd(X, k):
    """Spherical k-means with explicit centroids. Returns (list of member index lists, medoids)."""
    n = len(X)
    if k >= n:
        return [[i] for i in range(n)], list(range(n))
    seeds = far_first(X, k)
    lb = np.argmax(X @ X[seeds].T, axis=1)
    for j, s in enumerate(seeds):
        lb[s] = j
    for _ in range(25):
        sim = np.full((n, k), -np.inf)
        for j in range(k):
            if (lb == j).any():
                c = X[lb == j].sum(axis=0)
                sim[:, j] = X @ c / np.linalg.norm(c)
        new = np.argmax(sim, axis=1)
        if np.array_equal(new, lb):
            break
        lb = new
    groups, med = [], []
    for j in range(k):
        mem = np.where(lb == j)[0]
        if len(mem):
            c = X[mem].sum(axis=0)
            groups.append(list(mem))
            cs = X[mem] @ c / np.linalg.norm(c)
            med.append(int(mem[[i for i in range(len(mem)) if cs[i] >= cs.max() - 1e-6][0]]))
    return groups, med


def summary(policy, B, X32, kinds, pr, dim):
    """Stored unit vectors of one folder (rows of X32: its files' cache vectors), or (vectors, m) for
    allbits, where m is the number of leading dimensions kept."""
    n = B // int(np.ceil(dim / 8))
    X = unit(X32)
    f = len(X)
    if f == 0:
        return np.zeros((0, dim))
    if policy == "mean":
        return stored(unit(np.asarray(X32, np.float32).mean(axis=0, keepdims=True)), fit_format(B, dim, 1))
    if policy == "kindmean":
        present = [m for m in MODS if m in kinds]
        means = {m: unit(np.asarray(X32, np.float32)[[i for i in range(f) if kinds[i] == m]].mean(axis=0)) for m in present}
        fmt = fit_format(B, dim, len(present))
        if fmt is None:
            cnt = Counter(kinds)
            present = sorted(present, key=lambda m: (-cnt[m], MODS.index(m)))[:max(1, n)]
            fmt = "bin"
        return np.array([stored(means[m], fmt) for m in present])
    if policy == "allbits":
        m = min(dim, 8 * (B // f))
        return onebit(X[:, :m]), m
    if policy == "fsample":                       # a fixed share for every kind present, no refill
        cnt = Counter(kinds)
        order = sorted(cnt, key=lambda m: (-cnt[m], MODS.index(m)))
        share = n // len(order)
        if share == 0:
            order, share = order[:n], 1
        pick = []
        for m in order:
            pick += sorted([i for i in range(f) if kinds[i] == m], key=lambda i: pr[i])[:share]
        return onebit(X[pick])
    if n >= f:
        return onebit(X)
    if policy == "usample":
        return onebit(X[sorted(range(f), key=lambda i: pr[i])[:n]])
    if policy in ("sample", "kkind"):
        got, order = quotas(kinds, n)
        out = []
        for m in order:
            idx = [i for i in range(f) if kinds[i] == m]
            if got[m] == 0:
                continue
            if policy == "sample":
                out.append(onebit(X[sorted(idx, key=lambda i: pr[i])[:got[m]]]))
            else:
                groups, _ = lloyd(X[idx], got[m])
                out.append(onebit(np.array([X[idx][g].sum(axis=0) for g in groups])))
        return np.concatenate(out)
    if policy == "ffirst":
        return onebit(X[far_first(X, n)])
    groups, med = lloyd(X, n)
    if policy == "medoid":
        return onebit(X[med])
    return onebit(np.array([X[g].sum(axis=0) for g in groups]))


def score(s, q, dim):
    if isinstance(s, tuple):
        vecs, m = s
        return float((vecs @ unit(q[:m])).max()) if len(vecs) else -np.inf
    return float((s @ unit(q)).max()) if len(s) else -np.inf


def main():
    env = dict(os.environ, S19_KEEP="1")
    r = subprocess.run([sys.executable, "scripts/s19_selftest.py"], cwd=ROOT, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FAILED: s19_selftest.py\n" + r.stdout[-1500:] + r.stderr[-1500:])
    T = "_t19"
    try:
        emb = os.path.join(ROOT, "data", "emb", f"synth{T}")
        # files without a vector, as the input rules leave them: two whole directories and every 17th file
        idx = [json.loads(l) for l in open(os.path.join(emb, "index.jsonl"))]
        gone = sorted({os.path.dirname(x["path"]) for x in idx})[3:5]
        for i, x in enumerate(idx):
            if os.path.dirname(x["path"]) in gone or i % 17 == 5:
                x["ok"] = False
        with open(os.path.join(emb, "index.jsonl"), "w") as fh:
            fh.write("".join(json.dumps(x) + "\n" for x in idx))
        r = subprocess.run([sys.executable, "scripts/eval.py", "--model", "synth", "--emb", f"synth{T}", "--manifest",
                            f"data/manifest{T}.jsonl", "--dirs", f"data/dirs{T}.jsonl", "--gt", f"data/gt_structural{T}.jsonl",
                            "--criterion", "s3", "--calib", "0.2", "--calib-seed", "20261104", "--queries", "eval", "--s9",
                            "--reps", "a,c,d", "--tag", "_full"], cwd=ROOT, capture_output=True, text=True,
                           env=dict(os.environ, OMP_NUM_THREADS="2"))
        if r.returncode != 0:
            sys.exit("FAILED: eval.py\n" + r.stderr[-2000:])
        cmd = [sys.executable, "scripts/budget.py", "--model", "synth", "--emb", f"synth{T}", "--manifest",
               f"data/manifest{T}.jsonl", "--dirs", f"data/dirs{T}.jsonl", "--gt", f"data/gt_structural{T}.jsonl",
               "--calib-seed", "20261104", "--ranks", f"data/emb/synth{T}/ranks_full.jsonl", "--label", "T19",
               "--tag", "_s21", "--registered"]
        env = dict(os.environ, S21_BUDGETS=",".join(map(str, BUDGETS)), S21_REG_BUDGET="24", OMP_NUM_THREADS="2")
        env.pop("S21_SELFTEST", None)     # other budgets than the registered ones must be refused with --registered
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        assert r.returncode != 0 and "not the registered ones" in r.stderr, "the guard on the budgets did not stop the run"
        env["S21_SELFTEST"] = "1"
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("FAILED: budget.py\n" + r.stdout[-1500:] + r.stderr[-3000:])
        md = r.stdout
        assert ("Reproduced rank for rank." in md or "Reproduced up to near-ties." in md) and "H21a (primary): sample - mean, minority, not whole" in md \
            and "H21b (primary): sample - kmeans, all, not whole" in md \
            and "H21c (primary): sample - usample, minority, not whole" in md, md[:800]
        got = {}
        for l in open(os.path.join(emb, "ranks_s21.jsonl")):
            x = json.loads(l)
            got[x["query_path"]] = x

        V = np.load(os.path.join(emb, "vectors.npy"))
        manifest = [json.loads(l) for l in open(os.path.join(ROOT, f"data/manifest{T}.jsonl"))]
        dirs = {x["dir"]: x for x in (json.loads(l) for l in open(os.path.join(ROOT, f"data/dirs{T}.jsonl")))}
        gt = [json.loads(l) for l in open(os.path.join(ROOT, f"data/gt_structural{T}.jsonl"))]
        dim = V.shape[1]
        binb = int(np.ceil(dim / 8))
        dir_list = sorted(d for d, x in dirs.items() if x["n_files"] >= 3)
        okf = [bool(x["ok"]) for x in idx]
        files = {d: [i for i, m in enumerate(manifest) if m["dir"] == d and okf[i]] for d in dir_list}
        assert any(len(v) == 0 for v in files.values()) and not all(okf)
        pos = {m["path"]: i for i, m in enumerate(manifest)}
        prs = {sd: [int(hashlib.sha1(f"{sd}:{m['path']}".encode()).hexdigest(), 16) for m in manifest] for sd in SEEDS}
        kind = [m["modality"] for m in manifest]
        calib = ev.calib_split(dirs, 0.2, 20261104)
        queries = [g for g in gt if g["relevant_dir"] not in calib and okf[pos[g["query_path"]]]]
        assert {g["query_path"] for g in queries} == set(got), "query sets differ"

        def summ(policy, B, rows, sd=21):
            return summary(policy, B, V[rows], [kind[i] for i in rows], [prs[sd][i] for i in rows], dim)

        bad, excused, checked, over = Counter(), Counter(), 0, []
        for B in BUDGETS:
            for policy, sd in [(p, 21) for p in POLICIES] + [(p, sd) for p in ("sample", "usample") for sd in SEEDS[1:]]:
                row = f"{policy}@{B}" if sd == 21 else f"{policy}#{sd}@{B}"
                full = {d: summ(policy, B, files[d], sd) for d in dir_list}
                for d in dir_list:                                  # bytes stored never exceed the budget
                    s = full[d]
                    by = (len(s[0]) * int(np.ceil(s[1] / 8))) if isinstance(s, tuple) else None
                    if policy in ("sample", "fsample", "usample", "ffirst", "kmeans", "medoid", "kkind"):
                        by = len(s) * binb
                    if by is not None and by > B:
                        over.append((policy, B, d, by))
                for g in queries:
                    q = V[pos[g["query_path"]]].astype(np.float64)
                    own_rows = [i for i in files[g["relevant_dir"]] if i != pos[g["query_path"]]]
                    o = score(summ(policy, B, own_rows, sd), q, dim)
                    sc = np.array([o if d == g["relevant_dir"] else score(full[d], q, dim) for d in dir_list])
                    rank = 1 + int((sc > o).sum())
                    have = got[g["query_path"]][f"rank_{row}"]
                    checked += 1
                    if rank != have:
                        near = np.abs(sc - o) < TIE
                        lo, hi = 1 + int((sc > o + TIE).sum()), 1 + int(((sc > o) | near).sum()) - 1
                        if lo <= have <= max(hi, lo):
                            excused[row] += 1
                        else:
                            bad[row] += 1
        assert not over, over[:5]
        assert not bad, f"ranks differ from the plain implementation: {dict(bad)}"
        # rows that must coincide: every folder stored whole at 96 and 192 bytes; the f32 mean is eval.py's a;
        # the near-tie bounds bracket the rank
        for g in got.values():
            for pol in ("mean", "sample", "usample", "kmeans"):
                assert g[f"ranklo_{pol}@24"] <= g[f"rank_{pol}@24"] <= g[f"rankhi_{pol}@24"], (g["query_path"], pol)
            whole = {g[f"rank_{p}@{B}"] for B in (96, 192) for p in POLICIES[2:] if p != "fsample"}
            assert whole == {g["rank_d_bin"]}, (g["query_path"], whole, g["rank_d_bin"])
            assert g["rank_mean@192"] == g["rank_a_f32"]
        print(f"OK: budget.py agrees with the plain implementation on {checked} ranks ({len(queries)} queries, "
              f"{len(BUDGETS) * (len(POLICIES) + 8)} rows); differences explained by near-ties: {sum(excused.values())} "
              f"{dict(excused) if excused else ''}; "
              f"no summary above its budget; the rows that must coincide do.")
    finally:
        for p in glob.glob(os.path.join(ROOT, "data", f"*{T}*")) + [os.path.join(ROOT, "data", "emb", f"synth{T}")]:
            shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))


if __name__ == "__main__":
    main()
