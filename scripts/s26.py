#!/usr/bin/env python3
"""dirvec session 26 (BRIEF.md, session 26): representatives for mixed folders only (m), at the
natural mix of GitHub directories, and a hybrid of file names and vectors.

  s26.py score --set s19 --emb data/emb/jina-embeddings-v4_s19 --enc E1 --calib-seed 20261104 \
               --check data/ranks_s19_e1.jsonl.gz [--flags data/flags_s19.jsonl.gz] --out data/s26_s19_e1.npz
  s26.py report data/s26_*.npz > results/session26_outputs.md

`score` needs the vectors (on the pod). It rebuilds a, c and d exactly as scripts/indep_eval.py does
(the second implementation, which reproduced eval.py's ranks for every query), adds the policies m,
m2 and u and the name router, checks the gates and writes per-query ranks and counts. `report` reads
only the npz files.

Per query and policy X in POL: rank_X (scored set) and hm_X, the competitors of the mixed stratum
that score strictly above the own folder (the other stratum's count is rank_X - 1 - hm_X). Per query
and X in FUSE: the rank of the own folder under reciprocal rank fusion (k = 60) of the name router's
ranking and X's.
"""
import argparse
import concurrent.futures as cf
import gzip
import json
import multiprocessing as mp
import os
import subprocess
import sys
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402
import indep_eval as ie  # noqa: E402

ROOT = os.path.dirname(HERE)
POL = ("a", "c", "d", "m", "m2", "u")
FUSE = ("a", "c", "d", "m")
RRF_K = 60
IMAGE_INPUTS = ("image", "pdf_scanned")
NAMES_S11 = (0.700, 0.617, 0.587, 0.786, 0.688)     # the File names row: all, P1, P2, M1, M2
T0 = time.time()


def log(msg):
    sys.stderr.write("[%7.1fs] %s\n" % (time.time() - T0, msg))
    sys.stderr.flush()


def jl(path):
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    with (gzip.open(p, "rt") if p.endswith(".gz") else open(p)) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def is_mixed(labels):
    """The policy's rule: a file labelled image and at least one file of another label."""
    img = labels == "image"
    return bool(img.any() and (~img).any())


def rep_a(X):
    """a as eval.py builds it (build("a")), a (1, dim) row: indep_eval.rep_a takes the norm and the
    product by other kernels, which can move a score by a float32 ulp (one S19 query in the first run)."""
    return ev.unit(X.mean(axis=0, keepdims=True))


def group_means(X, labels):
    """m2: one normalised mean per input group present (image inputs first), as eval.py's b2."""
    img = np.isin(labels, IMAGE_INPUTS)
    return np.concatenate([ev.unit(X[s].mean(axis=0, keepdims=True)) for s in (img, ~img) if s.any()])


# ------------------------------------------------------------------ phase 1, per directory
def work_chunk(dir_names):
    """indep_eval.work_chunk with m2 and the facts the policies need. For each directory: its full
    c and m2 vectors and whether it is mixed; for each of its evaluation queries the leave-one-out
    scores of a, c, d and m2, whether the folder without the query is mixed, and the number of other
    files of the query's input group."""
    w = ie._W
    full_out, own = [], []
    for D in dir_names:
        ch = w.children.get(D)
        if ch is None:
            z = np.zeros((0, w.dim), dtype=np.float32)
            full_out.append((D, z, z, False))
            continue
        X = np.array(w.V[ch], dtype=np.float32)
        labs = w.mod[ch]
        groups = {}
        for L in ie.LABELS:
            sel = np.nonzero(labs == L)[0]
            if sel.size:
                groups[L] = sel
        full = {L: ie.rep_c_group(X[sel]) for L, sel in groups.items()}
        full_out.append((D, np.concatenate([full[L] for L in ie.LABELS if L in full]),
                         group_means(X, labs), is_mixed(labs)))
        img_all = np.isin(labs, IMAGE_INPUTS)
        for qpos, mi in w.by_dir.get(D, ()):
            pos = np.nonzero(ch == mi)[0]
            if pos.size != 1:
                ie.fail("query row %d is not among the ok children of %s" % (mi, D))
            pos = int(pos[0])
            q = np.array(w.V[mi], dtype=np.float32)
            keep = np.ones(len(ch), dtype=bool)
            keep[pos] = False
            sib = int((img_all[keep] == img_all[pos]).sum())
            if not keep.any():
                own.append((qpos, ie.NEG_INF, ie.NEG_INF, ie.NEG_INF, ie.NEG_INF, False, sib))
                continue
            Xl = X[keep]
            s_a = np.float32((rep_a(Xl) @ q).max())
            s_d = np.float32((Xl @ q).max())
            parts = []
            for L in ie.LABELS:
                if L == labs[pos]:
                    rest = groups[L][groups[L] != pos]
                    if rest.size:
                        parts.append(ie.rep_c_group(X[rest]))
                elif L in full:
                    parts.append(full[L])
            s_c = np.float32((np.concatenate(parts) @ q).max())
            s_b = np.float32((group_means(Xl, labs[keep]) @ q).max())
            own.append((qpos, s_a, s_c, s_d, s_b, is_mixed(labs[keep]), sib))
    return full_out, own


def min_rank(S):
    """Per row: 1 plus the number of entries strictly greater than each entry."""
    out = np.empty(S.shape, dtype=np.int64)
    n = S.shape[1]
    for i in range(S.shape[0]):
        s = np.sort(S[i])
        out[i] = 1 + (n - np.searchsorted(s, S[i], side="right"))
    return out


# ------------------------------------------------------------------ score
def score(args):
    sfx = "_" + args.set
    cfg = dict(manifest=os.path.join(ROOT, f"data/manifest{sfx}.jsonl"), dirs=os.path.join(ROOT, f"data/dirs{sfx}.jsonl"),
               gt=os.path.join(ROOT, f"data/gt_structural{sfx}.jsonl"), emb=os.path.join(ROOT, args.emb)
               if not os.path.isabs(args.emb) else args.emb, calib=0.2, calib_seed=args.calib_seed)
    w = ie.load_world(cfg, full_checks=False)
    w.cfg = cfg
    man = jl(cfg["manifest"])
    dirs = {r["dir"]: r for r in jl(cfg["dirs"])}
    ranked = w.ranked
    nR = len(ranked)
    pos_of = {d: j for j, d in enumerate(ranked)}
    nq = len(w.queries)
    log(f"{args.set} {args.enc}: {nR} ranked directories, {nq} evaluation queries")

    # strata and groups
    if args.set in ("s19", "s24"):
        sel = {f"data/corpus_{args.set}/gh_{r['id']}": r for r in jl(f"data/selection_{args.set}.jsonl")}
        stratum = np.array([bool(sel[d]["mixed_ext"]) for d in ranked])
        grp_of = {d: dirs[d].get("owner") or f"record:{dirs[d]['record']}" for d in ranked}
    else:
        sel = {r["id"]: r for r in jl(f"data/selection_{args.set}.jsonl")}
        stratum = np.ones(nR, bool)

        def fam(d):
            cr = sel[dirs[d]["record"]].get("creators") or []
            return cr[0].strip().lower() if cr else f"record:{dirs[d]['record']}"
        grp_of = {d: fam(d) for d in ranked}

    # phase 1
    procs = max(1, min(args.procs, os.cpu_count() or 1))
    own = np.full((4, nq), -np.inf, dtype=np.float32)          # a, c, d, m2
    mixed_own = np.zeros(nq, bool)
    sib_same = np.zeros(nq, np.int64)
    c_by, b_by, mixed_full = {}, {}, {}
    chunks = [ranked[i:i + 12] for i in range(0, nR, 12)]

    def take(res):
        fo, ow = res
        for D, C, B, mx in fo:
            c_by[D], b_by[D], mixed_full[D] = C, B, mx
        for qpos, sa, sc, sd, sb, mx, sb_ in ow:
            own[:, qpos] = (sa, sc, sd, sb)
            mixed_own[qpos] = mx
            sib_same[qpos] = sb_

    done = False
    if procs > 1:
        for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
            os.environ[var] = "1"
        try:
            with cf.ProcessPoolExecutor(max_workers=procs, mp_context=mp.get_context("spawn"),
                                        initializer=ie._init_worker, initargs=(cfg,)) as ex:
                for res in ex.map(work_chunk, chunks):
                    take(res)
            done = True
        except (OSError, cf.process.BrokenProcessPool) as exc:
            log(f"worker pool failed ({exc}); phase 1 again in this process")
            c_by.clear(), b_by.clear(), mixed_full.clear()
            own[:] = -np.inf
    if not done:
        ie._W = w
        for ch_ in chunks:
            take(work_chunk(ch_))
    log("phase 1 done")

    # phase 2: competitor scores, ranks, counts by stratum, names, fusion
    a_rows, d_blocks, c_blocks, b_blocks = [], [], [], []
    for D in ranked:
        ch = w.children.get(D)
        if ch is None:
            a_rows.append(None)
            d_blocks.append(np.zeros((0, w.dim), dtype=np.float32))
        else:
            X = np.array(w.V[ch], dtype=np.float32)
            a_rows.append(rep_a(X)[0])
            d_blocks.append(X)
        c_blocks.append(c_by[D])
        b_blocks.append(b_by[D])
    a_idx = np.array([j for j, r in enumerate(a_rows) if r is not None], dtype=np.int64)
    A = np.ascontiguousarray(np.stack([r for r in a_rows if r is not None]))
    Dm, d_st, d_ne = ie.segments(d_blocks)
    Cm, c_st, c_ne = ie.segments(c_blocks)
    Bm, b_st, b_ne = ie.segments(b_blocks)
    mixed_vec = np.array([mixed_full[D] for D in ranked])
    log(f"matrices: A {A.shape}, C {Cm.shape}, D {Dm.shape}, M2 {Bm.shape}; mixed by the rule {int(mixed_vec.sum())}, "
        f"mixed stratum {int(stratum.sum())}")

    # the name router (validity.name_baseline, with every folder's score kept)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    files = [i for i, r in enumerate(man) if w.ok[i] and r["dir"] in pos_of]
    files.sort(key=lambda i: (pos_of[man[i]["dir"]], i))
    fowner = np.array([pos_of[man[i]["dir"]] for i in files])
    stems = []
    for i in files:
        b = os.path.basename(man[i]["path"]).lower()
        k = b.rfind(".")
        stems.append(b[:k] if k > 0 else b)
    Xn = normalize(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), sublinear_tf=True).fit_transform(stems))
    Xn = Xn.astype(np.float32).tocsr()
    fpos = {man[i]["path"]: k for k, i in enumerate(files)}
    bounds = np.searchsorted(fowner, np.arange(nR + 1))
    nz = bounds[1:] > bounds[:-1]

    q_rows = np.array([i for _, i in w.queries], dtype=np.int64)
    q_dir = np.array([pos_of[g["relevant_dir"]] for g, _ in w.queries], dtype=np.int64)
    R = {x: np.zeros(nq, np.int64) for x in POL}
    HM = {x: np.zeros(nq, np.int64) for x in POL}
    RRF = {x: np.zeros(nq, np.int64) for x in FUSE}
    name_rank = np.zeros(nq, np.int64)
    blk = args.block
    for b0 in range(0, nq, blk):
        b1 = min(b0 + blk, nq)
        B = b1 - b0
        rows = np.arange(B)
        Q = np.array(w.V[q_rows[b0:b1]], dtype=np.float32)
        sa = np.full((B, nR), -np.inf, dtype=np.float32)
        sa[:, a_idx] = ie.block_product(Q, A)
        sc = ie.max_per_directory(Q, Cm, c_st, c_ne, nR)
        sd = ie.max_per_directory(Q, Dm, d_st, d_ne, nR)
        sb = ie.max_per_directory(Q, Bm, b_st, b_ne, nR)
        comp = {"a": sa, "c": sc, "d": sd, "m": np.where(mixed_vec, sc, sa), "m2": np.where(mixed_vec, sb, sa),
                "u": np.maximum(sa, sc)}
        mo = mixed_own[b0:b1]
        ownv = {"a": own[0, b0:b1], "c": own[1, b0:b1], "d": own[2, b0:b1],
                "m": np.where(mo, own[1, b0:b1], own[0, b0:b1]), "m2": np.where(mo, own[3, b0:b1], own[0, b0:b1]),
                "u": np.maximum(own[0, b0:b1], own[1, b0:b1])}
        qd = q_dir[b0:b1]
        for x in POL:
            S = comp[x]
            S[rows, qd] = -np.inf                                # the own folder never competes
            above = S > ownv[x][:, None]
            R[x][b0:b1] = 1 + above.sum(axis=1)
            HM[x][b0:b1] = (above & stratum[None, :]).sum(axis=1)
        # names
        qi = np.array([fpos[man[i]["path"]] for i in q_rows[b0:b1]])
        sim = (Xn[qi] @ Xn.T).toarray()
        N = np.full((B, nR), -np.inf, dtype=np.float32)
        N[:, nz] = np.maximum.reduceat(sim, bounds[:-1][nz], axis=1)
        for k in range(B):
            members = np.arange(bounds[qd[k]], bounds[qd[k] + 1])
            others = members[members != qi[k]]
            N[k, qd[k]] = sim[k, others].max() if len(others) else -np.inf
        name_rank[b0:b1] = 1 + (N > N[rows, qd][:, None]).sum(axis=1)
        rn = min_rank(N)
        for x in FUSE:
            S = comp[x].copy()
            S[rows, qd] = ownv[x]
            f = 1.0 / (RRF_K + min_rank(S)) + 1.0 / (RRF_K + rn)
            fo = f[rows, qd][:, None]
            better = (f > fo) | ((f == fo) & (S > ownv[x][:, None]))
            better[rows, qd] = False
            RRF[x][b0:b1] = 1 + better.sum(axis=1)
        if b0 // blk % 10 == 0:
            log(f"phase 2: {b1}/{nq}")
    log("phase 2 done")

    # gates
    gate = {}
    chk = {r["query_path"]: r for r in jl(args.check)}
    qpaths = [g["query_path"] for g, _ in w.queries]
    gate["queries_here"], gate["queries_check"] = nq, len(chk)
    gate["queries_missing_in_check"] = sum(1 for p in qpaths if p not in chk)
    for x in ("a", "c", "d"):
        key = f"rank_{x}" if f"rank_{x}" in next(iter(chk.values())) else f"rank_{x}_f32"
        want = np.array([chk[p][key] if p in chk else -1 for p in qpaths])
        gate[f"differ_{x}"] = int((want != R[x]).sum())
        gate[f"key_{x}"] = key
    if args.flags:
        fl = {r["query_path"]: r for r in jl(args.flags)}
        gate["names_differ"] = int(sum(1 for k, p in enumerate(qpaths) if p not in fl or fl[p]["name_rank_d"] != name_rank[k]))
        gate["sib_same_differ"] = int(sum(1 for k, p in enumerate(qpaths) if p in fl and fl[p]["sib_same"] != sib_same[k]))
    gate["pass"] = bool(gate["queries_missing_in_check"] == 0 and gate["queries_here"] == gate["queries_check"]
                        and all(gate[f"differ_{x}"] == 0 for x in "acd") and gate.get("names_differ", 0) == 0)
    log(f"gates: {gate}")
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "?"
    meta = dict(set=args.set, enc=args.enc, emb=args.emb, check=args.check, flags=args.flags or "", calib_seed=args.calib_seed,
                n_ranked=nR, n_mixed_stratum=int(stratum.sum()), n_mixed_rule=int(mixed_vec.sum()), commit=commit,
                seconds=round(time.time() - T0, 1), gate=gate)
    out = os.path.join(ROOT, args.out) if not os.path.isabs(args.out) else args.out
    np.savez_compressed(
        out, meta=np.array(json.dumps(meta)), qpath=np.array(qpaths), qdir=q_dir,
        qdirname=np.array([g["relevant_dir"] for g, _ in w.queries]),
        grp=np.array([grp_of[g["relevant_dir"]] for g, _ in w.queries]),
        modality=np.array([g["modality"] for g, _ in w.queries]),
        bucket=np.array([g["image_frac_bucket"] for g, _ in w.queries]),
        stratum_own=stratum[q_dir], mixed_own=mixed_own, sib_same=sib_same, name_rank=name_rank,
        **{f"rank_{x}": R[x] for x in POL}, **{f"hm_{x}": HM[x] for x in POL}, **{f"rrf_{x}": RRF[x] for x in FUSE})
    print(json.dumps(meta))
    return 0 if gate["pass"] else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score")
    s.add_argument("--set", required=True, choices=["s11", "s19", "s24"])
    s.add_argument("--emb", required=True)
    s.add_argument("--enc", required=True)
    s.add_argument("--calib-seed", type=int, required=True)
    s.add_argument("--check", required=True)
    s.add_argument("--flags")
    s.add_argument("--out", required=True)
    s.add_argument("--procs", type=int, default=3)
    s.add_argument("--block", type=int, default=256)
    r = sub.add_parser("report")
    r.add_argument("npz", nargs="+")
    args = ap.parse_args()
    if args.cmd == "score":
        sys.exit(score(args))
    import s26_report
    sys.exit(s26_report.report(args.npz))


if __name__ == "__main__":
    main()
