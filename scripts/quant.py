#!/usr/bin/env python3
"""dirvec session 20: per-modality representatives stored in a folder's metadata (BRIEF.md, session 20).

A folder's representatives sit in its metadata (an extended attribute), which is read before any file
in the folder and holds a fixed number of bytes. Every representative of a, c and d is stored in each
of five formats and the float32 query is scored against the stored vector:
  f32   4 bytes per dimension: the vector itself, unchanged (eval.py's rows)
  f16   2 bytes per dimension, half precision
  int8  1 byte per dimension: round(127 x / max|x|) per vector; the scale is not stored (cosine)
  int4  half a byte per dimension: round(7 x / max|x|) per vector
  bin   1 bit per dimension: +1 where x >= 0, else -1
Every format but f32 is decoded to float32 and unit-normalised, so the score is the cosine between the
query and the stored vector. Rows a_<f>, c_<f>, d_<f>: eval.py's pooled centroid, per-modality k-means
representatives and every file, uncentered, leave-one-out (the query's own directory is rebuilt without
the query, then stored). d_f32 is eval.py's d: every file of every folder opened.
With --check-ranks the f32 ranks of a, c and d must equal that file's rank_a, rank_c and rank_d query
for query, or the script stops with exit code 3 before any other number is printed. --selftest n
recomputes every row's rank for n evaluation queries in float64; a rank that differs and is not
explained by directories scoring within 1e-5 of the own directory stops it with exit code 4.
Bytes: a folder's stored size is its number of representatives times the format's bytes per vector,
over the directories ranked, built from all their embedded files (the stored folder holds them all).
Ranks as eval.py: 1 + the directories scoring strictly higher than the own directory, float32 scores.
Paired bootstrap as eval.py: 1000 resamples of the cell's directories, eval.py's cell seeds.

  quant.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s11 --manifest data/manifest_s11.jsonl
           --dirs data/dirs_s11.jsonl --gt data/gt_structural_s11.jsonl --calib 0.2
           --calib-seed 20261102 --check-ranks data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl
           --label E1 --tag _s20_e1 [--selftest 200]
Writes markdown to stdout and the per-query ranks to data/emb/<emb>/ranks<tag>.jsonl.
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval as ev  # noqa: E402  (eval.py: builders, calibration split, cells, bootstrap)

FORMATS = ["f32", "f16", "int8", "int4", "bin"]
BASES = ["a", "c", "d"]
ROWS = [f"{b}_{f}" for b in BASES for f in FORMATS]
BUDGETS = [2048, 4096, 8192, 16384, 65536]
KIB = {b: f"{b // 1024} KiB" for b in BUDGETS}
TIE = 1e-5
MARGIN = -0.02


def vec_bytes(f, dim):
    """Bytes one stored vector of dimension dim takes in format f."""
    return {"f32": 4 * dim, "f16": 2 * dim, "int8": dim, "int4": -(-dim // 2), "bin": -(-dim // 8)}[f]


def store(R, f):
    """Representatives (n, dim) float32 -> the stored vectors the query is scored against."""
    if f == "f32" or len(R) == 0:
        return R
    if f == "f16":
        X = R.astype(np.float16).astype(np.float32)
    elif f in ("int8", "int4"):
        top = np.float32(127.0 if f == "int8" else 7.0)
        m = np.abs(R).max(axis=1, keepdims=True).astype(np.float32)
        X = np.rint(R * (top / np.maximum(m, np.float32(1e-30)))).astype(np.float32)
    elif f == "bin":
        X = np.where(R >= 0, np.float32(1.0), np.float32(-1.0)).astype(np.float32)
    else:
        raise ValueError(f)
    return ev.unit(X).astype(np.float32)


def check_store(dim):
    """The formats do what the docstring says, on random unit vectors of the cache's dimension."""
    rng = np.random.default_rng(2020)
    R = ev.unit(rng.normal(size=(64, dim))).astype(np.float32)
    for f in FORMATS:
        X = store(R, f)
        assert X.dtype == np.float32 and X.shape == R.shape, f
        if f == "f32":
            assert X is R, f
        else:
            assert np.allclose(np.linalg.norm(X, axis=1), 1, atol=1e-5), f
    m = np.abs(R).max(axis=1, keepdims=True)
    for f, top in (("int8", 127), ("int4", 7)):
        code = np.rint(R * (np.float32(top) / m))
        assert np.abs(code).max() == top and np.array_equal(code, np.round(code)), f
        assert np.allclose(store(R, f), ev.unit(code), atol=1e-6), f
    assert np.array_equal(np.sign(store(R, "bin")), np.where(R >= 0, 1.0, -1.0)), "bin"
    assert np.abs(store(R, "f16") - R).max() < 1e-3, "f16"
    assert [vec_bytes(f, 2048) for f in FORMATS] == [8192, 4096, 2048, 1024, 256]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--gt", required=True)
    ap.add_argument("--calib", type=float, default=0.2)
    ap.add_argument("--calib-seed", type=int, default=20261102)
    ap.add_argument("--check-ranks", default=None, help="repo-relative eval.py ranks file to reproduce")
    ap.add_argument("--label", default="")
    ap.add_argument("--tag", default="_s20")
    ap.add_argument("--selftest", type=int, default=0, help="evaluation queries recomputed in float64")
    args = ap.parse_args()
    R = ev.ROOT

    emb_dir = os.path.join(ev.DATA, "emb", args.emb)
    V = np.load(os.path.join(emb_dir, "vectors.npy"))
    index = [json.loads(l) for l in open(os.path.join(emb_dir, "index.jsonl"))]
    manifest = [json.loads(l) for l in open(os.path.join(R, args.manifest))]
    dirs = {r["dir"]: r for r in (json.loads(l) for l in open(os.path.join(R, args.dirs)))}
    gt = [json.loads(l) for l in open(os.path.join(R, args.gt))]
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache not in manifest order"
    assert all(r.get("done") for r in index), "cache incomplete"

    pos = {r["path"]: i for i, r in enumerate(manifest)}
    ok = np.array([r["ok"] for r in index])
    mods_all = np.array([r["modality"] for r in manifest])
    dir_list = sorted(d for d, r in dirs.items() if r["n_files"] >= 3)
    dir_idx = {d: j for j, d in enumerate(dir_list)}
    n_dirs = len(dir_list)
    children = {d: [] for d in dir_list}
    for i, r in enumerate(manifest):
        if ok[i] and r["dir"] in children:
            children[r["dir"]].append(i)
    children = {d: np.array(v, int) for d, v in children.items()}
    dim = V.shape[1]
    check_store(dim)

    calib = ev.calib_split(dirs, args.calib, args.calib_seed)
    q_eval = [g for g in gt if ok[pos[g["query_path"]]] and g["relevant_dir"] not in calib]
    nq = len(q_eval)
    qpos = np.array([pos[g["query_path"]] for g in q_eval])
    Q = V[qpos]
    j0s = np.array([dir_idx[g["relevant_dir"]] for g in q_eval])
    keep_of = []
    for g, p in zip(q_eval, qpos):
        c = children[g["relevant_dir"]]
        keep_of.append(c[c != p])
    print(f"{args.label}: {nq} eval queries, {n_dirs} directories ranked, {dim} dimensions", file=sys.stderr)

    # full representations (dir_list order, so owners are sorted), built once in float32
    full, bounds = {}, {}
    for b in BASES:
        full[b] = {d: ev.build(b, V[children[d]], mods_all[children[d]]) for d in dir_list}
        owner = np.concatenate([np.full(len(full[b][d]), j) for j, d in enumerate(dir_list)])
        assert (np.diff(owner) >= 0).all()
        bounds[b] = np.searchsorted(owner, np.arange(n_dirs + 1))

    sample = np.array([], int)
    if args.selftest:
        sample = np.sort(np.random.default_rng(20).choice(nq, size=min(args.selftest, nq), replace=False))
    in_sample = set(int(k) for k in sample)

    # own directory, leave-one-out: rebuilt once per query and base, then stored in every format
    own = {r: np.zeros(nq, np.float32) for r in ROWS}
    own_reps = {}
    for b in BASES:
        for k in range(nq):
            keep = keep_of[k]
            Rk = ev.build(b, V[keep], mods_all[keep])
            if k in in_sample:
                own_reps[(b, k)] = Rk
            for f in FORMATS:
                own[f"{b}_{f}"][k] = np.float32((store(Rk, f) @ Q[k]).max()) if len(Rk) else np.float32(-np.inf)
        print(f"  {args.label} own directories {b} done", file=sys.stderr)

    def dir_max(S, bd, rows_n, dtype):
        out = np.full((rows_n, n_dirs), -np.inf, dtype)
        for j in range(n_dirs):
            if bd[j + 1] > bd[j]:
                out[:, j] = S[:, bd[j]:bd[j + 1]].max(axis=1)
        return out

    ranks, rows_s = {}, {}
    for b in BASES:
        allR = np.concatenate([full[b][d] for d in dir_list])
        for f in FORMATS:
            r = f"{b}_{f}"
            S = Q @ store(allR, f).T                       # as eval.py: one product, all queries
            dsc = dir_max(S, bounds[b], nq, np.float32)
            del S
            o = own[r]
            dsc[np.arange(nq), j0s] = o
            assert dsc.dtype == np.float32
            ranks[r] = 1 + (dsc > o[:, None]).sum(axis=1)
            if len(sample):
                rows_s[r] = dsc[sample].copy()
            del dsc
        print(f"  {args.label} {b} ranked in {len(FORMATS)} formats", file=sys.stderr)

    out = [f"## {args.label}: {args.model} ({dim} dimensions)" if args.label else f"## {args.model}", ""]

    # reproduction of eval.py's a, c, d ranks by the f32 rows
    if args.check_ranks:
        ref = {}
        for l in open(os.path.join(R, args.check_ranks)):
            x = json.loads(l)
            ref[x["query_path"]] = x
        mine = [g["query_path"] for g in q_eval]
        same_set = set(mine) == set(ref)
        diffs, examples = Counter(), []
        for k, qp in enumerate(mine):
            if qp not in ref:
                continue
            for b in BASES:
                if int(ref[qp][f"rank_{b}"]) != int(ranks[f"{b}_f32"][k]):
                    diffs[b] += 1
                    if len(examples) < 10:
                        examples.append(f"{qp} {b}: eval.py {ref[qp][f'rank_{b}']}, quant {ranks[f'{b}_f32'][k]}")
        ok_rep = same_set and not diffs
        out.append(f"Reproduction of {args.check_ranks}: {len(mine)} queries here, {len(ref)} there, same set: "
                   f"{'yes' if same_set else 'NO'}; queries whose rank differs: " +
                   ", ".join(f"{b} {diffs[b]}" for b in BASES) +
                   f". {'Reproduced rank for rank.' if ok_rep else 'NOT REPRODUCED.'}")
        if not ok_rep:
            out.extend(examples)
            print("\n".join(out))
            sys.exit(3)
        out.append("")

    # self-test: float64, directory maxima recomputed, own directory rebuilt
    if len(sample):
        bad, excused = Counter(), Counter()
        Qs = Q[sample].astype(np.float64)
        for b in BASES:
            allR = np.concatenate([full[b][d] for d in dir_list])
            for f in FORMATS:
                r = f"{b}_{f}"
                S64 = dir_max(Qs @ store(allR, f).astype(np.float64).T, bounds[b], len(sample), np.float64)
                for i, k in enumerate(sample):
                    j0 = j0s[k]
                    Rk = own_reps[(b, k)]
                    o64 = float((store(Rk, f).astype(np.float64) @ Qs[i]).max()) if len(Rk) else -np.inf
                    s64 = S64[i].copy()
                    s64[j0] = o64
                    row, o32 = rows_s[r][i], own[r][k]
                    assert 1 + int((row > o32).sum()) == ranks[r][k]
                    if 1 + int((s64 > o64).sum()) != ranks[r][k]:
                        flip = (s64 > o64) != (row > o32)
                        flip[j0] = False
                        if np.all(np.abs(s64[flip] - o64) < TIE):
                            excused[r] += 1
                        else:
                            bad[r] += 1
        out.append(f"Self-test: {len(sample)} evaluation queries, every row recomputed in float64 (stored vectors, "
                   f"directory maxima, own directory rebuilt): ranks that differ beyond scores within {TIE:g} of the "
                   f"own directory: {sum(bad.values())}{' ' + str(dict(bad)) if bad else ''}; differences explained "
                   f"by such near-ties: {sum(excused.values())}{' ' + str(dict(excused)) if excused else ''}. "
                   f"{'Passed.' if not bad else 'FAILED.'}")
        if bad:
            print("\n".join(out))
            sys.exit(4)
        out.append("")

    with open(os.path.join(emb_dir, f"ranks{args.tag}.jsonl"), "w") as fh:
        for k, g in enumerate(q_eval):
            fh.write(json.dumps({**g, **{f"rank_{r}": int(ranks[r][k]) for r in ROWS}}) + "\n")

    # cells and the bootstrap
    qb = np.array([g["image_frac_bucket"] for g in q_eval])
    qm = np.array([g["modality"] for g in q_eval])
    qd = np.array([g["relevant_dir"] for g in q_eval])
    primary, parts, majority, buckets = ev.s3_cells(qb, qm)
    cells = [("all", np.ones(nq, bool), 1), ("P1", primary[0][1], 50), ("P2", primary[1][1], 51),
             ("M1", majority[0][1], 56), ("M2", majority[1][1], 57)]
    res = {}
    for n, sel, seed in cells:
        cdirs = sorted(set(qd[sel]))
        idx = np.random.default_rng(seed).integers(0, len(cdirs), size=(ev.N_BOOT, len(cdirs)))
        res[n] = {}
        for r in ROWS:
            hb = defaultdict(lambda: [0, 0])
            for d, x in zip(qd[sel], ranks[r][sel]):
                hb[d][0] += int(x <= 5)
                hb[d][1] += 1
            res[n][r] = ev.boot(hb, cdirs, idx)

    def r_at(r, sel, k=5):
        return float((ranks[r][sel] <= k).mean()) if sel.any() else float("nan")

    def diff(x, y, n, sel):
        lo, hi = np.percentile(res[n][x] - res[n][y], [2.5, 97.5])
        return r_at(x, sel) - r_at(y, sel), lo, hi

    def fmt(x):
        return "n/a" if x != x else f"{x:.3f}"

    # bytes per folder
    n_rep = {b: np.array([len(full[b][d]) for d in dir_list]) for b in BASES}
    out.append(f"Queries: {nq} evaluation queries over {len(set(qd))} directories; {n_dirs} directories ranked "
               f"(calibration seed {args.calib_seed}). Representatives per folder (all embedded files): "
               + "; ".join(f"{b} mean {n_rep[b].mean():.2f}, median {np.median(n_rep[b]):.0f}, "
                           f"95th percentile {np.percentile(n_rep[b], 95):.0f}, max {n_rep[b].max()}" for b in BASES)
               + ".")
    out.append("")
    out.append(f"### {args.label} bytes per folder: representatives times bytes per vector")
    out.append("")
    out.append("| row | bytes per vector | mean | 95th percentile | max | " +
               " | ".join(f"folders within {KIB[B]}" for B in BUDGETS) + " |")
    out.append("|---|---:|---:|---:|---:|" + "---:|" * len(BUDGETS))
    for b in BASES:
        for f in FORMATS:
            vb = vec_bytes(f, dim)
            by = n_rep[b] * vb
            out.append(f"| {b}_{f} | {vb} | {by.mean():.0f} | {np.percentile(by, 95):.0f} | {by.max()} | " +
                       " | ".join(f"{(by <= B).mean():.3f}" for B in BUDGETS) + " |")
    out.append("")

    for k in (5, 1, 10):
        out.append(f"### {args.label} recall@{k}")
        out.append("")
        out.append("| row | " + " | ".join(f"{n} ({int(s.sum())})" for n, s, _ in cells) + " |")
        out.append("|---|" + "---:|" * len(cells))
        for r in ROWS:
            out.append(f"| {r} | " + " | ".join(fmt(r_at(r, s, k)) for _, s, _ in cells) + " |")
        out.append("")

    pairs = ([(f"c_{f}", "d_f32") for f in FORMATS] + [("c_bin", "a_f32")] +
             [(f"c_{f}", f"a_{f}") for f in FORMATS] + [(f"c_{f}", "c_f32") for f in FORMATS[1:]] +
             [(f"a_{f}", "a_f32") for f in FORMATS[1:]] + [(f"d_{f}", "d_f32") for f in FORMATS[1:]] +
             [(f"c_{f}", f"d_{f}") for f in FORMATS[1:]])
    out.append(f"### {args.label} paired differences in recall@5 (95 percent intervals, 1000 resamples of the "
               f"cell's directories)")
    out.append("")
    out.append("| x - y | " + " | ".join(n for n, _, _ in cells) + " |")
    out.append("|---|" + "---|" * len(cells))
    for x, y in pairs:
        out.append(f"| {x} - {y} | " + " | ".join(
            "{:+.3f} [{:+.3f}, {:+.3f}]".format(*diff(x, y, n, s)) for n, s, _ in cells) + " |")
    out.append("")

    # budgets: the most precise format whose largest folder fits
    out.append(f"### {args.label} budgets: the most precise format in which every folder fits, its recall@5")
    out.append("")
    out.append("| budget | " + " | ".join(f"{b}: format | {b} R@5 all | {b} R@5 P1 | {b} R@5 P2" for b in BASES) + " |")
    out.append("|---|" + "---|---:|---:|---:|" * len(BASES))
    for B in BUDGETS:
        cols = []
        for b in BASES:
            fit = next((f for f in FORMATS if n_rep[b].max() * vec_bytes(f, dim) <= B), None)
            if fit is None:
                cols.append("none | n/a | n/a | n/a")
            else:
                cols.append(f"{fit} | " + " | ".join(fmt(r_at(f"{b}_{fit}", s)) for n, s, _ in cells if n in
                                                      ("all", "P1", "P2")))
        out.append(f"| {KIB[B]} | " + " | ".join(cols) + " |")
    out.append("")

    # verdicts, the brief's rules
    out.append(f"### {args.label} verdicts (rules of BRIEF.md, session 20)")
    out.append("")
    for h, f in (("H20a", "int8"), ("H20b", "bin")):
        rows = [(n,) + diff(f"c_{f}", "d_f32", n, s) for n, s, _ in cells]
        dead = [n for n, st, lo, hi in rows if hi < MARGIN]
        low = min(rows, key=lambda t: t[2])
        out.append(f"{h} {args.label}: c_{f} - d_f32 in recall@5, intervals lying entirely below {MARGIN}: "
                   f"{', '.join(dead) if dead else 'none'}; lowest lower bound {low[2]:+.3f} ({low[0]}); "
                   f"lower bounds above {MARGIN} in {sum(lo > MARGIN for _, _, lo, _ in rows)} of 5 cells. "
                   f"{'DEAD' if dead else 'Survives'}.")
    rows = [(n,) + diff("c_bin", "a_f32", n, s) for n, s, _ in cells if n in ("P1", "P2")]
    dead = [n for n, st, lo, hi in rows if not lo > 0]
    out.append("H20c " + args.label + ": c_bin - a_f32 in recall@5: " +
               "; ".join(f"{n} {st:+.3f} [{lo:+.3f}, {hi:+.3f}]" for n, st, lo, hi in rows) +
               f". {'DEAD (' + ', '.join(dead) + ')' if dead else 'Survives'}.")
    out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
