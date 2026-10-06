#!/usr/bin/env python3
"""Self-test of scripts/tree.py (session 23): every walk recomputed by a second, plain implementation.

Builds a synthetic set of repository trees (no network, no files on disk beyond the manifest: 14
repositories, directories up to depth 4, two input groups, some files without a vector), runs tree.py
with budgets of 16 and 64 bytes (2 and 8 one-bit vectors of 8 bytes; the mean in bin and in int8), and
recomputes for every query and every summary the walk, its first step, the number of summaries it
read and the flat rank, from path strings and the vectors alone: every directory's sets rebuilt per
query by filtering, every summary rebuilt from scratch. It fails on any difference that a near-tie
(two candidates within 1e-6) does not explain, and it checks the rules of tree_fetch.py on made-up trees.

  python3 scripts/s23_selftest.py        (under a minute; writes data/*_t23* and removes them)
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
import tree_fetch as tf  # noqa: E402

T, DIM = "_t23", 64
BUDGETS = [16, 64]
MODS = ev.MODALITIES
NEAR = 1e-6


def unit(x):
    x = np.asarray(x, np.float64)
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-300)


def onebit(x):
    return unit(np.where(np.asarray(x) >= 0, 1.0, -1.0))


def make(rng):
    manifest, dirs, gt, vecs, okf = [], [], [], [], []
    gap = unit(rng.normal(size=DIM))
    for r in range(14):
        owner, repo = f"own{r % 11}", f"own{r % 11}/repo{r}"
        paths = {""}
        for _ in range(int(rng.integers(8, 22))):
            depth = int(rng.integers(0, 5))
            p = "/".join(str(rng.choice(["src", "docs", "img", "lib", "data"])) + str(int(rng.integers(0, 3))) for _ in range(depth))
            paths.add(p)
        rtopic = rng.normal(size=DIM)
        for k, p in enumerate(sorted(paths)):
            n = int(rng.integers(1, 8))
            frac = float(rng.choice([0.0, 0.2, 0.7, 1.0]))
            d = f"data/corpus{T}/gh_{r}_{k}"
            topic = rtopic * 0.5 + rng.normal(size=DIM)
            kinds = ["image" if rng.random() < frac else str(rng.choice(["text", "text", "table", "pdf_text"])) for _ in range(n)]
            n_img = sum(m == "image" for m in kinds)
            dirs.append({"dir": d, "n_files": n, "n_image": n_img, "n_pdf_scanned": 0, "image_frac": n_img / n,
                         "record": f"{r}_{k}", "owner": owner, "repo": repo, "repo_dir": p,
                         "repo_depth": p.count("/") + 1 if p else 0})
            b = ev.bucket_of(n_img / n)
            for i, m in enumerate(kinds):
                path = f"{d}/{'fig' if m == 'image' else 'note'}{i}_{str(rng.choice(['alpha', 'beta', 'gamma']))}.{'png' if m == 'image' else 'txt'}"
                manifest.append({"path": path, "dir": d, "modality": m})
                v = unit(topic) + (0.8 if m == "image" else -0.8) * gap + 0.9 * unit(rng.normal(size=DIM))
                vecs.append(unit(v))
                okf.append(bool(rng.random() > 0.06))
                if n >= 3:
                    gt.append({"query_path": path, "relevant_dir": d, "modality": m, "image_frac_bucket": b})
    return manifest, dirs, gt, np.array(vecs, np.float32), okf


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


def plain_score(policy, B, rows, q, V, kind, pr, name_sim):
    """The query's score against the summary of the manifest rows `rows` (the query is not among them)."""
    if not rows:
        return -np.inf
    if policy == "names":
        return max(name_sim[j] for j in rows)
    X = V[rows].astype(np.float64)
    if policy == "mean":
        m = unit(np.asarray(V[rows], np.float32).mean(axis=0))
        f = "bin" if B < DIM // 2 else "int4" if B < DIM else "int8" if B < 2 * DIM else "f16" if B < 4 * DIM else "f32"
        m32 = np.asarray(m, np.float32)
        if f == "bin":
            st = onebit(m32)
        elif f in ("int8", "int4"):
            top = 127.0 if f == "int8" else 7.0
            st = unit(np.rint(m32 * (np.float32(top) / np.abs(m32).max())))
        elif f == "f16":
            st = unit(m32.astype(np.float16).astype(np.float64))
        else:
            st = unit(m32)
        return float(st @ q)
    n = B // (DIM // 8)
    kinds = [kind[j] for j in rows]
    idx = list(range(len(rows)))
    if policy == "all":
        keep = idx
    elif policy == "usample":
        keep = sorted(idx, key=lambda i: pr[rows[i]])[:n]
    elif policy == "fsample":
        cnt = Counter(kinds)
        order = sorted(cnt, key=lambda m: (-cnt[m], MODS.index(m)))
        share = n // len(order)
        if share == 0:
            order, share = order[:n], 1
        keep = []
        for m in order:
            keep += sorted([i for i in idx if kinds[i] == m], key=lambda i: pr[rows[i]])[:share]
    else:
        got, order = quotas(kinds, n)
        keep = []
        for m in order:
            keep += sorted([i for i in idx if kinds[i] == m], key=lambda i: pr[rows[i]])[:got[m]]
    return float((onebit(unit(X[keep])) @ q).max())


def main():
    # the rules of tree_fetch.py on made-up trees
    k = lambda n, mod, size=10: [(f"f{i}", size, "png" if mod == "image" else "txt", mod) for i in range(n)]  # noqa: E731
    good = {f"a/b{i}": {"kept": k(5, "text"), "excluded": 0} for i in range(8)}
    good["img"] = {"kept": k(6, "image"), "excluded": 1}
    held, st = tf.tree_stats(good)
    assert tf.why_not(st) is None and st == {"n_dirs": 9, "n_files": 46, "n_image": 6, "n_other_kept": 40, "bytes": 460, "max_depth": 2}, st
    flat = {f"b{i}": {"kept": k(5, "text"), "excluded": 0} for i in range(8)}
    flat["img"] = {"kept": k(6, "image"), "excluded": 0}
    assert tf.why_not(tf.tree_stats(flat)[1]) == "no directory at depth 2 or more"
    few = dict(list(good.items())[:5])
    assert tf.why_not(tf.tree_stats(few)[1]) == "fewer than 8 directories with a kept file"
    noimg = {d: v for d, v in good.items() if d != "img"}
    noimg["a/b9"] = {"kept": k(5, "text"), "excluded": 0}
    assert tf.why_not(tf.tree_stats(noimg)[1]) == "fewer than 5 image files"
    big = dict(good)
    big["a/huge"] = {"kept": k(300, "text"), "excluded": 0}
    assert tf.why_not(tf.tree_stats(big)[1]) == "more than 300 kept files"

    rng = np.random.default_rng(23)
    manifest, dirs, gt, V, okf = make(rng)
    emb = os.path.join(ROOT, "data", "emb", f"synth{T}")
    try:
        os.makedirs(emb, exist_ok=True)
        np.save(os.path.join(emb, "vectors.npy"), V)
        with open(os.path.join(emb, "index.jsonl"), "w") as fh:
            fh.write("".join(json.dumps({"path": m["path"], "modality": m["modality"], "ok": o, "done": True, "note": ""}) + "\n"
                             for m, o in zip(manifest, okf)))
        for name, rows in (("manifest", manifest), ("dirs", dirs), ("gt_structural", gt)):
            with open(os.path.join(ROOT, f"data/{name}{T}.jsonl"), "w") as fh:
                fh.write("".join(json.dumps(r) + "\n" for r in rows))
        cmd = [sys.executable, "scripts/tree.py", "--model", "synth", "--emb", f"synth{T}", "--manifest", f"data/manifest{T}.jsonl",
               "--dirs", f"data/dirs{T}.jsonl", "--gt", f"data/gt_structural{T}.jsonl", "--label", "T23", "--registered"]
        env = dict(os.environ, S23_BUDGETS=",".join(map(str, BUDGETS)), S23_REG_BUDGET="64", OMP_NUM_THREADS="2")
        env.pop("S23_SELFTEST", None)
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        assert r.returncode != 0 and "not the registered ones" in r.stderr, "the guard on the budgets did not stop the run"
        env["S23_SELFTEST"] = "1"
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("FAILED: tree.py\n" + r.stdout[-1500:] + r.stderr[-3000:])
        md = r.stdout
        assert "H23a (primary): walk, fsample - mean, minority" in md and "H23c (primary): walk - flat, fsample" in md, md[:600]
        got = {x["query_path"]: x for x in (json.loads(l) for l in open(os.path.join(emb, "walk_s23.jsonl")))}

        # ---- the plain implementation
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        drow = {d["dir"]: d for d in dirs}
        pr = [int(hashlib.sha1(f"21:{m['path']}".encode()).hexdigest(), 16) for m in manifest]
        kind = [m["modality"] for m in manifest]
        img = [m["modality"] in ("image", "pdf_scanned") for m in manifest]
        repo_of = [drow[m["dir"]]["repo"] for m in manifest]
        rdir_of = [drow[m["dir"]]["repo_dir"] for m in manifest]
        pos = {m["path"]: i for i, m in enumerate(manifest)}
        n_ok_dir = Counter(m["dir"] for m, o in zip(manifest, okf) if o)
        queries = [g for g in gt if okf[pos[g["query_path"]]] and n_ok_dir[g["relevant_dir"]] >= 2]
        assert {g["query_path"] for g in queries} == set(got), "query sets differ"
        keys = [(p, B) for B in BUDGETS for p in ("mean", "usample", "fsample", "sample", "all")] + [("names", 0)]
        bad, excused, checked = Counter(), 0, 0
        under = lambda a, b: a == b or a.startswith(b + "/") or b == ""  # noqa: E731  (directory a lies in the subtree of b)
        for repo in sorted({drow[g["relevant_dir"]]["repo"] for g in queries}):
            members = [i for i in range(len(manifest)) if repo_of[i] == repo and okf[i]]
            stems = [os.path.basename(manifest[i]["path"]).lower() for i in members]
            X = normalize(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), sublinear_tf=True).fit_transform(stems))
            Xd = np.asarray(X.todense(), np.float32)
            for g in [g for g in queries if drow[g["relevant_dir"]]["repo"] == repo]:
                i = pos[g["query_path"]]
                t = rdir_of[i]
                rest = [j for j in members if j != i]
                q = V[i].astype(np.float64)
                sims = Xd @ Xd[members.index(i)]
                name_sim = {j: float(sims[members.index(j)]) for j in rest}
                # directories that hold an embedded file, in the order of depth and path
                holding = sorted({rdir_of[j] for j in members}, key=lambda d: (d.count("/") + (1 if d else 0), d))
                nodes = {""}
                for d in holding:
                    v = d
                    while v:
                        nodes.add(v)
                        v = v.rsplit("/", 1)[0] if "/" in v else ""
                kids = lambda v: sorted(c for c in nodes if c and (c.rsplit("/", 1)[0] if "/" in c else "") == v)  # noqa: E731
                n_grp = sum(1 for j in rest if img[j] == img[i])
                sib = any(img[j] == img[i] for j in rest if rdir_of[j] == t)
                assert got[g["query_path"]]["minority"] == bool(n_grp < 0.5 * len(rest) and sib), g["query_path"]
                assert got[g["query_path"]]["target"] == t
                for policy, B in keys:
                    tag = f"{policy}@{B}" if B else policy
                    sc = lambda rows: plain_score(policy, B, rows, q, V, kind, pr, name_sim)  # noqa: E731
                    v, read, first, tie = "", 0, None, False
                    while True:
                        cands = [("", sc([j for j in rest if rdir_of[j] == v]))]
                        cands += [(c, sc([j for j in rest if under(rdir_of[j], c)])) for c in kids(v)]
                        cands = [c for c in cands if c[1] > -np.inf]
                        if not cands:
                            break
                        read += len(cands)
                        top = max(c[1] for c in cands)
                        tie = tie or sum(1 for c in cands if c[1] >= top - NEAR) > 1
                        best = next(c for c in cands if c[1] == top)
                        if first is None:
                            first = best[0] if best[0] else v
                        if best[0] == "":
                            break
                        v = best[0]
                    fl = {u: sc([j for j in rest if rdir_of[j] == u]) for u in holding}
                    fl = {u: s for u, s in fl.items() if s > -np.inf}
                    before = holding[:holding.index(t)]
                    rank = 1 + sum(1 for s in fl.values() if s > fl[t]) + sum(1 for u in before if u in fl and fl[u] == fl[t])
                    ftie = sum(1 for s in fl.values() if abs(s - fl[t]) <= NEAR) > 1
                    want_first = (t.split("/")[0] if t else "")
                    h = got[g["query_path"]]
                    for name, mine, theirs, loose in (("walk", int(v == t), h[f"walk_{tag}"], tie),
                                                      ("read", read, h[f"read_{tag}"], tie),
                                                      ("first", int(first == want_first), h[f"first_{tag}"], tie),
                                                      ("flat", int(rank == 1), h[f"flat_{tag}"], ftie),
                                                      ("flat3", int(rank <= 3), h[f"flat3_{tag}"], ftie)):
                        checked += 1
                        if mine != theirs:
                            if loose:
                                excused += 1
                            else:
                                bad[f"{name}_{tag}"] += 1
        assert not bad, f"tree.py differs from the plain implementation: {dict(bad)}"
        print(f"OK: tree.py agrees with the plain implementation on {checked} values ({len(queries)} queries, {len(keys)} "
              f"summaries; walk, summaries read, first step, flat top 1 and top 3); differences explained by near-ties: "
              f"{excused}; the rules of tree_fetch.py hold on the made-up trees.")
    finally:
        for p in glob.glob(os.path.join(ROOT, "data", f"*{T}*")) + [emb]:
            shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))


if __name__ == "__main__":
    main()
