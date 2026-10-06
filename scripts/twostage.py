#!/usr/bin/env python3
"""dirvec two-stage retrieval and cost: directory stage (a, b, c), then files inside the top k
directories, against the flat walk d (every file vector scored, no container layer).

Query and leave-one-out as in eval.py: the query is a file f of directory D0, D0's
representation is rebuilt without f, f itself is never a candidate.
  stage 1  rank all directories by max cosine against their representatives (a, b, c, and
           from session 6 c4 and c2, see eval.py),
           keep the top k, k in {1, 3, 5, 10}. Ties are broken in favour of D0, which matches
           eval.py (rank = 1 + number of directories scoring strictly higher).
  stage 2  rank the embedded files of those k directories by cosine against the query.
  flat d   rank every embedded file of the corpus by cosine.
Relevant files of a query: the other embedded files of D0 (its siblings). Queries with no
embedded sibling are dropped from the file-level numbers and counted.

File-level metrics, fixed before the first run:
  hit@n    at least one sibling among the top n files, n in {1, 5, 10}
  sib@10   siblings among the top 10 files / min(10, number of siblings)
Cost per query: vectors scored = stage 1 representatives of all directories + files of the
top k directories (flat: all files but the query).
Paired 95 percent bootstrap intervals (1000 resamples of the cell's directories) for the
difference two-stage minus flat on hit@1, hit@10 and sib@10.

Index size: representative vectors per directory and bytes at 2048 float32. A two-stage index
holds the representatives and the file vectors; the flat index holds the file vectors only.

Query time (--timing): brute force numpy, one query at a time, one BLAS thread, full
representations (no leave-one-out), top 10 files returned. Best of 5 passes over all queries
(session 5: over --timing-queries queries drawn with a fixed seed).
Session 5 (large set): --sample N evaluates N queries stratified by bucket, if the per-query
leave-one-out k-means is too slow for all of them.

  twostage.py --model jina-embeddings-v4 [--timing]
  twostage.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s3 --manifest data/manifest_s3.jsonl
              --dirs data/dirs_s3.jsonl --gt data/gt_structural_s3.jsonl [--timing]

Writes markdown to stdout and per-query rows to data/emb/<emb>/twostage.jsonl (keys d and
<rep>_k<k>, e.g. c4_k10; before session 6 the keys were <rep><k>, e.g. c10).

Session 9: --calib (fraction, seed --calib-seed, as eval.py) restricts the queries to the
evaluation split and allows stage 1 representations of the session 9 families (--stage1, a comma
list of eval.py names such as bc2, f4_w0.5, f4b_w0.5; eval.py parse_rep). Stage 2 scores the
files with the uncentered vectors unless --stage2 c. Rows go to twostage<tag>.jsonl.
  twostage.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s5 ... --calib 0.2
              --stage1 c,bc2,f4_w0.5 --tag _s9
"""
import argparse
import json
import os
import sys
import time
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eval import BUCKETS, TEXTLIKE, build, parse_rep, query_vectors, centered_space, f4_bias, align_spaces  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
STAGE1 = ["a", "b", "c", "c4", "c2"]
KS = [1, 3, 5, 10]
NS = [1, 5, 10]
N_BOOT = 1000
DIM_BYTES = 2048 * 4
METRICS = ["hit@1", "hit@5", "hit@10", "sib@10"]


def build_rep(rep, X, mods):
    space, base, param = parse_rep(rep)
    return build(base, X, mods, param)


def n_vec(rep, R):
    """vectors a representation stores: F4 rows hold two d-dimensional slots."""
    return len(R) * (2 if parse_rep(rep)[1] in ("f4", "f4b") else 1)


def file_metrics(scores, is_sib, n_sib):
    """hit@1, hit@5, hit@10, sib@10 for one candidate list."""
    top = np.argsort(-scores, kind="stable")[:10]
    rel = is_sib[top]
    return [float(rel[:n].any()) for n in NS] + [float(rel.sum()) / min(10, n_sib)]


def load(args):
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
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache not in manifest order"
    assert all(r.get("done") for r in index), "cache incomplete"
    ok = np.array([r["ok"] for r in index])
    mods = np.array([r["modality"] for r in manifest])
    dir_list = sorted(d for d, r in dirs.items() if r["n_files"] >= 3)
    children = {d: [] for d in dir_list}
    for i, r in enumerate(manifest):
        if ok[i] and r["dir"] in children:
            children[r["dir"]].append(i)
    children = {d: np.array(v, int) for d, v in children.items()}
    pos = {r["path"]: i for i, r in enumerate(manifest)}
    queries = [g for g in gt if ok[pos[g["query_path"]]]]
    ctx = {"spaces": {"u": V}, "is_img": None, "bias": None, "stage1": STAGE1}
    if getattr(args, "calib", 0) > 0:
        calib, is_img, in_calib, mu, Vc = centered_space(V, ok, mods, manifest, dirs, args.calib, args.calib_seed)
        ctx["spaces"]["c"] = Vc
        ctx["is_img"] = is_img
        ctx["stage1"] = args.stage1.split(",")
        need = sorted({parse_rep(r)[0] for r in ctx["stage1"]} - {"u", "c"})
        if need:
            calib_dirs = [d for d in dir_list if d in calib]
            ctx["spaces"].update(align_spaces(Vc, is_img, ok, in_calib, children, calib_dirs, need)[0])
        if any(parse_rep(r)[1] == "f4b" for r in ctx["stage1"]):
            dev_q = [g for g in queries if g["relevant_dir"] in calib]
            ctx["bias"] = f4_bias(Vc, is_img, children, pos, dev_q)[0]
            print(f"  F4b bias {ctx['bias']}", file=sys.stderr)
        queries = [g for g in queries if g["relevant_dir"] not in calib]
        print(f"  calibration split: {len(calib)} directories; {len(queries)} evaluation-split queries", file=sys.stderr)
    if getattr(args, "sample", 0) and len(queries) > args.sample:
        queries = stratified_sample(queries, args.sample)
    return emb_dir, V, mods, dir_list, children, pos, queries, ctx


def stratified_sample(queries, n, seed=20261002):
    """n queries, allocated to image_frac buckets in proportion to their size, drawn with a fixed seed;
    returned in ground-truth order."""
    rng = np.random.default_rng(seed)
    by_b = {b: [i for i, g in enumerate(queries) if g["image_frac_bucket"] == b] for b in BUCKETS}
    take = []
    for b in BUCKETS:
        k = round(n * len(by_b[b]) / len(queries))
        take += rng.choice(by_b[b], size=min(k, len(by_b[b])), replace=False).tolist()
    return [queries[i] for i in sorted(take)]


def evaluate(args, out):
    emb_dir, V, mods, dir_list, children, pos, queries, ctx = load(args)
    STAGE1 = ctx["stage1"]
    spaces = ctx["spaces"]

    def space(rep):
        return spaces[parse_rep(rep)[0]]
    dir_idx = {d: j for j, d in enumerate(dir_list)}
    n_dirs = len(dir_list)
    file_dir = np.full(len(V), -1, int)
    for d, c in children.items():
        file_dir[c] = dir_idx[d]
    all_files = np.concatenate([children[d] for d in dir_list])
    child_list = [children[d] for d in dir_list]

    full = {rep: {d: build_rep(rep, space(rep)[children[d]], mods[children[d]]) for d in dir_list} for rep in STAGE1 + ["d"]}
    n_reps = {rep: np.array([n_vec(rep, full[rep][d]) for d in dir_list]) for rep in full}

    qpos = np.array([pos[g["query_path"]] for g in queries])
    V2 = spaces[getattr(args, "stage2", "u")]
    Q = V2[qpos]
    SF = Q @ V2.T                                        # (nq, n_files) file scores, stage 2 and flat
    q_img = ctx["is_img"][qpos] if ctx["is_img"] is not None else None
    nq = len(queries)
    n_sib = np.array([len(children[g["relevant_dir"]]) - 1 for g in queries])

    methods = [(rep, k) for rep in STAGE1 for k in KS] + ["d"]
    M = {m: np.zeros((nq, len(METRICS)), np.float32) for m in methods}
    scored = {m: np.zeros(nq, np.float64) for m in methods}
    dir_hit = {m: np.zeros(nq, bool) for m in methods}
    not_d0 = np.ones(n_dirs, int)

    # flat walk
    for qi in range(nq):
        if n_sib[qi] < 1:
            continue
        cand = all_files[all_files != qpos[qi]]
        M["d"][qi] = file_metrics(SF[qi, cand], file_dir[cand] == dir_idx[queries[qi]["relevant_dir"]], n_sib[qi])
        scored["d"][qi] = len(cand)
    print("  flat d done", file=sys.stderr, flush=True)

    for rep in STAGE1:
        W = space(rep)
        Qr = query_vectors(rep, W[qpos], q_img, ctx["bias"])
        allR = np.concatenate([full[rep][d] for d in dir_list])
        rows = np.array([len(full[rep][d]) for d in dir_list])
        starts = np.concatenate([[0], np.cumsum(rows)[:-1]])
        assert (rows > 0).all(), "a directory without embedded children"
        dir_scores = np.maximum.reduceat(Qr @ allR.T, starts, axis=1)
        total_reps = int(n_reps[rep].sum())
        for qi, g in enumerate(queries):
            j0 = dir_idx[g["relevant_dir"]]
            p = qpos[qi]
            keep = children[g["relevant_dir"]]
            keep = keep[keep != p]
            R = build_rep(rep, W[keep], mods[keep])
            s = dir_scores[qi].copy()
            # own score in the dtype of the score row, so that the directory never outranks itself
            # (session 13 correction of eval.py; every stage 1 row used so far is float32 already)
            own = s.dtype.type((R @ Qr[qi]).max()) if len(R) else s.dtype.type(-np.inf)
            s[j0] = own
            not_d0[j0] = 0
            order = np.lexsort((not_d0, -s))             # by score, D0 first among ties
            not_d0[j0] = 1
            rank = 1 + int((s > own).sum())
            n_stage1 = total_reps - n_reps[rep][j0] + n_vec(rep, R)
            for k in KS:
                m = (rep, k)
                top = order[:k]
                dir_hit[m][qi] = rank <= k
                assert dir_hit[m][qi] == (j0 in top)
                cand = np.concatenate([child_list[j] for j in top])
                cand = cand[cand != p]
                scored[m][qi] = n_stage1 + len(cand)
                if n_sib[qi] < 1 or len(cand) == 0:
                    continue
                M[m][qi] = file_metrics(SF[qi, cand], file_dir[cand] == j0, n_sib[qi])
        print(f"  rep {rep} done", file=sys.stderr, flush=True)
    # under d the directory stage is the flat walk itself: top file's directory
    with open(os.path.join(emb_dir, f"twostage{getattr(args, 'tag', '')}.jsonl"), "w") as fh:
        for qi, g in enumerate(queries):
            row = dict(g, n_siblings=int(n_sib[qi]))
            for m in methods:
                key = m if m == "d" else f"{m[0]}_k{m[1]}"
                row[key] = {"dir_hit": bool(dir_hit[m][qi]) if m != "d" else None,
                            "scored": int(scored[m][qi]),
                            **{x: round(float(v), 4) for x, v in zip(METRICS, M[m][qi])}}
            fh.write(json.dumps(row) + "\n")

    qb = np.array([g["image_frac_bucket"] for g in queries])
    qm = np.array([g["modality"] for g in queries])
    qd = np.array([g["relevant_dir"] for g in queries])
    has_sib = n_sib >= 1
    textlike = np.isin(qm, TEXTLIKE)
    cells = [
        ("all queries", np.ones(nq, bool), 101),
        ("P1 image in [0,.2)+[.2,.5)", (qm == "image") & np.isin(qb, BUCKETS[:2]), 102),
        ("P2 textlike in [.5,.8)+[.8,1]", textlike & np.isin(qb, BUCKETS[2:]), 103),
        ("image in [.5,.8)+[.8,1]", (qm == "image") & np.isin(qb, BUCKETS[2:]), 104),
        ("textlike in [0,.2)+[.2,.5)", textlike & np.isin(qb, BUCKETS[:2]), 105),
    ]

    out.append(f"Model: {args.model}, cache {os.path.basename(emb_dir)}. Queries with a vector: {nq}"
               + (f" (evaluation split, calibration fraction {args.calib}; stage 2 and flat on the "
                  f"{'centered' if getattr(args, 'stage2', 'u') == 'c' else 'uncentered'} vectors)"
                  if getattr(args, "calib", 0) > 0 else "") + "; "
               f"with at least one embedded sibling: {int(has_sib.sum())} "
               f"({int((~has_sib).sum())} dropped from the file-level numbers). "
               f"{n_dirs} directories ranked, {len(all_files)} embedded files.")
    out.append("")
    out.append("### Index size")
    out.append("")
    out.append("| index | vectors | vectors per directory | MB at 2048 float32 | with file vectors for stage 2: vectors | MB |")
    out.append("|---|---:|---:|---:|---:|---:|")
    nf = len(all_files)
    for rep in STAGE1 + ["d"]:
        n = int(n_reps[rep].sum())
        tot = n + nf if rep != "d" else nf
        out.append(f"| {rep} | {n} | {n / n_dirs:.2f} | {n * DIM_BYTES / 1e6:.1f} | {tot} | {tot * DIM_BYTES / 1e6:.1f} |")

    for name, sel, seed in cells:
        sel = sel & has_sib
        if not sel.any():
            continue
        cdirs = sorted(set(qd[sel]))
        dpos = {d: j for j, d in enumerate(cdirs)}
        di = np.array([dpos[d] for d in qd[sel]])
        idx = np.random.default_rng(seed).integers(0, len(cdirs), size=(N_BOOT, len(cdirs)))
        cnt = np.bincount(di, minlength=len(cdirs)).astype(float)

        def boot_diff(x):
            """paired interval of mean(x) over resampled directories; x is a per-query difference."""
            sums = np.bincount(di, weights=x, minlength=len(cdirs))
            b = sums[idx].sum(axis=1) / cnt[idx].sum(axis=1)
            return np.percentile(b, [2.5, 97.5])

        out.append("")
        out.append(f"### {name}: {int(sel.sum())} queries over {len(cdirs)} directories")
        out.append("")
        out.append("| stage 1 | k | dir recall@k | hit@1 | hit@5 | hit@10 | sib@10 | vectors scored | "
                   "hit@1 minus d | 95% CI | hit@10 minus d | 95% CI | sib@10 minus d | 95% CI |")
        out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---|")
        base = M["d"][sel]
        for m in methods:
            x = M[m][sel]
            mean = x.mean(axis=0)
            if m == "d":
                out.append(f"| d (flat) | | | " + " | ".join(f"{v:.3f}" for v in mean) +
                           f" | {scored[m][sel].mean():.0f} | | | | | | |")
                continue
            cols = []
            for c in (0, 2, 3):
                lo, hi = boot_diff((x[:, c] - base[:, c]).astype(float))
                cols.append(f"{mean[c] - base[:, c].mean():+.3f} | [{lo:+.3f}, {hi:+.3f}]")
            out.append(f"| {m[0]} | {m[1]} | {dir_hit[m][sel].mean():.3f} | " +
                       " | ".join(f"{v:.3f}" for v in mean) +
                       f" | {scored[m][sel].mean():.0f} | " + " | ".join(cols) + " |")


def timing(args, out):
    from threadpoolctl import threadpool_limits
    emb_dir, V, mods, dir_list, children, pos, queries, ctx = load(args)
    STAGE1 = [r for r in ctx["stage1"] if parse_rep(r)[0] == "u" and parse_rep(r)[1] not in ("f4", "f4b")]
    n_dirs = len(dir_list)
    # file vectors stored directory by directory, so a directory is one slice
    sizes = np.array([len(children[d]) for d in dir_list])
    F = np.ascontiguousarray(np.concatenate([V[children[d]] for d in dir_list]))
    fstart = np.concatenate([[0], np.cumsum(sizes)])
    Q = np.ascontiguousarray(V[[pos[g["query_path"]] for g in queries]])
    if args.timing_queries and len(Q) > args.timing_queries:
        Q = Q[np.sort(np.random.default_rng(100).choice(len(Q), size=args.timing_queries, replace=False))]
    reps = {}
    for rep in STAGE1 + ["d"]:
        R = [build_rep(rep, V[children[d]], mods[children[d]]) for d in dir_list]
        n = np.array([len(r) for r in R])
        reps[rep] = (np.ascontiguousarray(np.concatenate(R)), np.concatenate([[0], np.cumsum(n)[:-1]]))

    def top10(s):
        if len(s) <= 10:
            return np.argsort(-s)
        t = np.argpartition(-s, 10)[:10]
        return t[np.argsort(-s[t])]

    def flat(q):
        return top10(F @ q)

    def dir_only(rep, k, q):
        R, starts = reps[rep]
        ds = np.maximum.reduceat(R @ q, starts)
        return np.argpartition(-ds, k - 1)[:k] if k < n_dirs else np.arange(n_dirs)

    def two(rep, k, q):
        top = dir_only(rep, k, q)
        cand = np.concatenate([np.arange(fstart[j], fstart[j + 1]) for j in top])
        return cand[top10(F[cand] @ q)]

    def clock(fn):
        best = np.inf
        for _ in range(5):
            t0 = time.perf_counter()
            for q in Q:
                fn(q)
            best = min(best, time.perf_counter() - t0)
        return best / len(Q) * 1e6

    out.append("")
    out.append("### Query time")
    out.append("")
    out.append(f"Microseconds per query, brute force numpy {np.__version__}, one BLAS thread, best of 5 passes "
               f"over {len(Q)} queries, top 10 files returned. {n_dirs} directories, {len(F)} file vectors. "
               "Directory stage alone in the first column (for d: the flat walk with a max per directory).")
    out.append("")
    out.append("| index | directory stage only | " + " | ".join(f"two-stage k={k}" for k in KS) + " | flat walk |")
    out.append("|---|---:|" + "---:|" * len(KS) + "---:|")
    with threadpool_limits(limits=1):
        for rep in STAGE1:
            row = [clock(lambda q: dir_only(rep, 5, q))] + [clock(lambda q: two(rep, k, q)) for k in KS]
            out.append(f"| {rep} | " + " | ".join(f"{x:.0f}" for x in row) + " | |")
        out.append(f"| d | {clock(lambda q: dir_only('d', 5, q)):.0f} | " + " | " * len(KS) + f"{clock(flat):.0f} |")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", help="cache directory under data/emb (default: the model name)")
    ap.add_argument("--manifest", default="data/manifest.jsonl", help="repo-relative")
    ap.add_argument("--dirs", default="data/dirs.jsonl", help="repo-relative")
    ap.add_argument("--gt", default="data/gt_structural.jsonl", help="repo-relative")
    ap.add_argument("--timing", action="store_true", help="also measure query time")
    ap.add_argument("--timing-queries", type=int, default=0,
                    help="time on this many queries (fixed seed) instead of all; 0 = all")
    ap.add_argument("--sample", type=int, default=0,
                    help="evaluate this many queries, stratified by bucket, fixed seed; 0 = all")
    ap.add_argument("--calib", type=float, default=0.0, help="session 9: calibration fraction (eval.py --calib)")
    ap.add_argument("--calib-seed", type=int, default=20260930)
    ap.add_argument("--stage1", default=",".join(STAGE1), help="session 9: comma list of stage 1 representations")
    ap.add_argument("--stage2", choices=["u", "c"], default="u", help="session 9: stage 2 and flat vectors")
    ap.add_argument("--tag", default="", help="rows written to data/emb/<emb>/twostage<tag>.jsonl")
    args = ap.parse_args()
    out = []
    evaluate(args, out)
    if args.timing:
        timing(args, out)
    print("\n".join(out))


if __name__ == "__main__":
    main()
