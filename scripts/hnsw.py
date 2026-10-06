#!/usr/bin/env python3
"""dirvec approximate baselines: HNSW (hnswlib) as the flat walk and as stage 1 of two-stage.

Same queries, leave-one-out rule and relevance as twostage.py (siblings of the query in its
own directory; the query itself is never a candidate).

  flat HNSW   one index over every embedded file vector (inner product on unit vectors).
              Search k = 11, drop the query, keep the top 10. Recall@10 against the exact flat
              walk's top 10, hit@1 and hit@10 against the siblings, paired 95 percent bootstrap
              interval (1000 resamples of directories) of hit@10 minus exact d.
  stage 1     one index over the representatives of every directory (a, b, c, c4 or c2,
              full representations; c4 and c2 from session 6). Search K_REPS representatives,
              map them to directories in score order (a directory's score is its best retrieved
              representative). Leave-one-out: the query's own directory is dropped from the result
              and re-inserted with its exact score from the representation rebuilt without the
              query, as in twostage.py. Keep the top 10 directories, then rank their files exactly
              (stage 2 as in twostage.py).
              Reported: overlap of the 10 directories with exact stage 1, hit@1, hit@10, and the
              interval of hit@10 minus exact d.
Parameters are fixed: M = 16, ef_construction = 200, random seed 100; flat ef_search in EFS
(session 7 grid), stage 1 ef_search in STAGE1_EFS (the values sessions 5 and 6 used).
Index bytes: the size of the saved hnswlib index file. Query time: one thread
(hnswlib set_num_threads(1), one BLAS thread for stage 2), one query at a time, full
representations, best of 3 passes over --timing-queries queries (fixed seed); microseconds per
query. Build time is reported with --build-threads threads (default NTHREADS: DIRVEC_THREADS if
set, else os.cpu_count(); set it where the cgroup allows fewer CPUs than os.cpu_count() reports).
Builds on several threads are not reproducible; --build-threads 1 is (session 7).

Session 7 (H7): per-query hit@1 and hit@10 of exact d, the exact two-stage (k = 10) and every flat
and HNSW stage 1 setting go to data/emb/<emb>/hnsw.jsonl (no times, so two runs can be compared
byte for byte). Checks: exact d and exact two-stage hit@1, hit@10 and directory hit against
twostage.jsonl. Paired comparison: each stage 1 at ef_search 100 against flat HNSW at the smallest
ef_search in EFS whose query time in this run is at least the two-stage query time; paired 95
percent interval (1000 resamples of directories) of the difference, all queries, P1 and P2.

  hnsw.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s5 --manifest data/manifest_s5.jsonl
          --dirs data/dirs_s5.jsonl --gt data/gt_structural_s5.jsonl

Reads data/emb/<emb>/twostage.jsonl for the exact d metrics of each query (run twostage.py first).
Writes markdown to stdout.
"""
import argparse
import json
import os
import sys
import tempfile
import time

import hnswlib
from importlib.metadata import version
import numpy as np
from threadpoolctl import threadpool_limits

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eval import build  # noqa: E402
from eval import BUCKETS, TEXTLIKE  # noqa: E402
from twostage import file_metrics, load  # noqa: E402

M_HNSW, EF_CONSTRUCTION, SEED = 16, 200, 100
EFS = [32, 48, 64, 96, 128, 192, 256]
STAGE1_EFS = [100, 128, 256]
H7_EF = 100
STAGE1 = ["a", "b", "c", "c4", "c2"]
K_DIRS = 10
K_REPS = 100
N_BOOT = 1000
NTHREADS = int(os.environ.get("DIRVEC_THREADS", os.cpu_count()))


def make_index(X, nthreads):
    idx = hnswlib.Index(space="ip", dim=X.shape[1])
    idx.init_index(max_elements=len(X), M=M_HNSW, ef_construction=EF_CONSTRUCTION, random_seed=SEED)
    idx.set_num_threads(nthreads)
    t0 = time.time()
    idx.add_items(X, np.arange(len(X)))
    build_s = time.time() - t0
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "i.bin")
        idx.save_index(p)
        nbytes = os.path.getsize(p)
    idx.set_num_threads(1)
    return idx, nbytes, build_s


def boot_ci(x, qd, seed):
    """paired 95 percent interval of mean(x) resampling directories; x is a per-query difference."""
    cdirs = sorted(set(qd))
    dpos = {d: j for j, d in enumerate(cdirs)}
    di = np.array([dpos[d] for d in qd])
    idx = np.random.default_rng(seed).integers(0, len(cdirs), size=(N_BOOT, len(cdirs)))
    cnt = np.bincount(di, minlength=len(cdirs)).astype(float)
    sums = np.bincount(di, weights=x, minlength=len(cdirs))
    b = sums[idx].sum(axis=1) / cnt[idx].sum(axis=1)
    return np.percentile(b, [2.5, 97.5])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", help="cache directory under data/emb (default: the model name)")
    ap.add_argument("--manifest", default="data/manifest.jsonl", help="repo-relative")
    ap.add_argument("--dirs", default="data/dirs.jsonl", help="repo-relative")
    ap.add_argument("--gt", default="data/gt_structural.jsonl", help="repo-relative")
    ap.add_argument("--timing-queries", type=int, default=2000)
    ap.add_argument("--build-threads", type=int, default=NTHREADS,
                    help="threads for index builds; 1 makes them reproducible")
    args = ap.parse_args()
    out = []

    emb_dir, V, mods, dir_list, children, pos, queries = load(args)
    with open(os.path.join(emb_dir, "twostage.jsonl")) as fh:
        exact = {r["query_path"]: r for r in (json.loads(l) for l in fh)}
    queries = [g for g in queries if exact[g["query_path"]]["n_siblings"] >= 1]
    nq = len(queries)
    dir_idx = {d: j for j, d in enumerate(dir_list)}
    all_files = np.concatenate([children[d] for d in dir_list])
    file_dir = np.full(len(V), -1, int)
    for d, c in children.items():
        file_dir[c] = dir_idx[d]
    qpos = np.array([pos[g["query_path"]] for g in queries])
    qd = np.array([g["relevant_dir"] for g in queries])
    j0s = np.array([dir_idx[d] for d in qd])
    n_sib = np.array([exact[g["query_path"]]["n_siblings"] for g in queries])
    Q = np.ascontiguousarray(V[qpos])
    d_hit1 = np.array([exact[g["query_path"]]["d"]["hit@1"] for g in queries])
    d_hit10 = np.array([exact[g["query_path"]]["d"]["hit@10"] for g in queries])
    per = {"d": (d_hit1, d_hit10)}
    times = {}
    tq = np.sort(np.random.default_rng(SEED).choice(nq, size=min(args.timing_queries, nq), replace=False))
    print(f"{nq} queries, {len(dir_list)} dirs, {len(all_files)} files", file=sys.stderr, flush=True)

    out.append(f"hnswlib {version('hnswlib')}, "
               f"numpy {np.__version__}. M = {M_HNSW}, ef_construction = {EF_CONSTRUCTION}, "
               f"inner product, seed {SEED}. {nq} queries with at least one embedded sibling, "
               f"{len(dir_list)} directories, {len(all_files)} file vectors. Query time: one thread, "
               f"best of 3 passes over {len(tq)} queries.")

    # exact flat top 10 per query (the reference for recall@10), file vectors in directory order
    F = np.ascontiguousarray(V[all_files])
    exact_top = np.zeros((nq, 10), int)
    for s in range(0, nq, 2048):
        S = Q[s:s + 2048] @ F.T
        for r in range(S.shape[0]):
            qi = s + r
            S[r, all_files == qpos[qi]] = -np.inf
            t = np.argpartition(-S[r], 10)[:10]
            exact_top[qi] = all_files[t[np.argsort(-S[r, t])]]

    rel = file_dir[exact_top] == j0s[:, None]
    ok1 = (rel[:, 0] == (d_hit1 > 0)).mean()
    ok10 = (rel.any(axis=1) == (d_hit10 > 0)).mean()
    out.append(f"Check: exact d from this script against twostage.jsonl, hit@1 equal on {ok1:.4f} "
               f"and hit@10 on {ok10:.4f} of the queries.")
    print(f"exact d check {ok1:.4f} {ok10:.4f}", file=sys.stderr, flush=True)

    def clock(fn):
        best = np.inf
        for _ in range(3):
            t0 = time.perf_counter()
            for qi in tq:
                fn(Q[qi])
            best = min(best, time.perf_counter() - t0)
        return best / len(tq) * 1e6

    # ------------------------------------------------ flat HNSW
    idx, nbytes, build_s = make_index(F, args.build_threads)
    flat_bytes = nbytes
    out.append("")
    out.append("### Flat HNSW over the file vectors")
    out.append("")
    out.append(f"Index: {len(F)} vectors, {nbytes / 1e6:.1f} MB on disk (raw vectors "
               f"{F.nbytes / 1e6:.1f} MB), built in {build_s:.0f} s on {args.build_threads} threads.")
    out.append("")
    out.append("| ef_search | recall@10 vs exact | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | us per query |")
    out.append("|---:|---:|---:|---:|---:|---|---:|")
    with threadpool_limits(limits=1):
        t_exact = clock(lambda q: np.argpartition(-(F @ q), 10)[:10])
    times["d"] = t_exact
    out.append(f"| exact d | 1.000 | {d_hit1.mean():.3f} | {d_hit10.mean():.3f} | | | {t_exact:.0f} |")
    for ef in EFS:
        idx.set_ef(max(ef, 11))
        labels, _ = idx.knn_query(Q, k=11, num_threads=NTHREADS)
        rec, h1, h10 = np.zeros(nq), np.zeros(nq), np.zeros(nq)
        for qi in range(nq):
            got = all_files[labels[qi]]
            got = got[got != qpos[qi]][:10]
            rec[qi] = len(np.intersect1d(got, exact_top[qi])) / 10
            rel = file_dir[got] == j0s[qi]
            h1[qi], h10[qi] = float(rel[:1].any()), float(rel.any())
        lo, hi = boot_ci(h10 - d_hit10, qd, 201)
        t = clock(lambda q: idx.knn_query(q, k=11, num_threads=1))
        per[f"flat_ef{ef}"] = (h1, h10)
        times[f"flat_ef{ef}"] = t
        out.append(f"| {ef} | {rec.mean():.3f} | {h1.mean():.3f} | {h10.mean():.3f} | "
                   f"{h10.mean() - d_hit10.mean():+.3f} | [{lo:+.3f}, {hi:+.3f}] | {t:.0f} |")
        print(f"  flat ef {ef} done", file=sys.stderr, flush=True)
    del idx

    # ------------------------------------------------ HNSW over the representatives as stage 1
    out.append("")
    out.append(f"### Two-stage with HNSW over the representatives as stage 1, k = {K_DIRS} directories")
    out.append("")
    out.append(f"Stage 1 retrieves {K_REPS} representatives (ef_search at least {K_REPS}); stage 2 is exact "
               "over the files of the 10 directories. Directory overlap: share of the 10 directories that "
               "exact stage 1 also returns. Two-stage time includes stage 2.")
    out.append("")
    out.append("| stage 1 | representatives | index MB | build s | ef_search | dir overlap vs exact | "
               "dir recall@10 | hit@1 | hit@10 | hit@10 minus exact d | 95% CI | us per query |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|")
    sizes = np.array([len(children[d]) for d in dir_list])
    fstart = np.concatenate([[0], np.cumsum(sizes)])
    checks, storage = [], {}
    for rep in STAGE1:
        full = [build(rep, V[children[d]], mods[children[d]]) for d in dir_list]
        R = np.ascontiguousarray(np.concatenate(full))
        owner = np.concatenate([np.full(len(r), j) for j, r in enumerate(full)])
        starts = np.concatenate([[0], np.cumsum([len(r) for r in full])[:-1]])
        idx, nbytes, build_s = make_index(R, args.build_threads)
        # exact stage 1 (leave-one-out) and the rebuilt own-directory scores
        own = np.zeros(nq)
        exact_dirs = np.zeros((nq, K_DIRS), int)
        not_d0 = np.ones(len(dir_list), int)
        for s0 in range(0, nq, 2048):
            DS = np.maximum.reduceat(Q[s0:s0 + 2048] @ R.T, starts, axis=1)
            for r in range(DS.shape[0]):
                qi = s0 + r
                j0 = j0s[qi]
                keep = children[qd[qi]]
                keep = keep[keep != qpos[qi]]
                Rq = build(rep, V[keep], mods[keep])
                own[qi] = (Rq @ Q[qi]).max() if len(Rq) else -np.inf
                sc = DS[r]
                sc[j0] = own[qi]
                not_d0[j0] = 0
                exact_dirs[qi] = np.lexsort((not_d0, -sc))[:K_DIRS]
                not_d0[j0] = 1
        # exact two-stage from exact_dirs, checked against twostage.jsonl <rep>_k10
        e1, e10, edh = np.zeros(nq), np.zeros(nq), np.zeros(nq, bool)
        for qi in range(nq):
            dirs10 = exact_dirs[qi]
            edh[qi] = j0s[qi] in dirs10
            cand = all_files[np.concatenate([np.arange(fstart[j], fstart[j + 1]) for j in dirs10])]
            cand = cand[cand != qpos[qi]]
            m = file_metrics(V[cand] @ Q[qi], file_dir[cand] == j0s[qi], n_sib[qi])
            e1[qi], e10[qi] = m[0], m[2]
        ts = [exact[g["query_path"]][f"{rep}_k{K_DIRS}"] for g in queries]
        c_dh = np.mean([t["dir_hit"] == bool(x) for t, x in zip(ts, edh)])
        c_1 = np.mean([t["hit@1"] == x for t, x in zip(ts, e1)])
        c_10 = np.mean([t["hit@10"] == x for t, x in zip(ts, e10)])
        checks.append(f"{rep}: directory hit equal on {c_dh:.4f}, hit@1 on {c_1:.4f}, hit@10 on {c_10:.4f}")
        print(f"exact two-stage {rep} check {c_dh:.4f} {c_1:.4f} {c_10:.4f}", file=sys.stderr, flush=True)
        per[f"exact_{rep}_k{K_DIRS}"] = (e1, e10)
        storage[rep] = nbytes
        for ef in STAGE1_EFS:
            idx.set_ef(max(ef, K_REPS))
            labels, dists = idx.knn_query(Q, k=K_REPS, num_threads=NTHREADS)
            ov, dh, h1, h10 = np.zeros(nq), np.zeros(nq), np.zeros(nq), np.zeros(nq)
            for qi in range(nq):
                j0 = j0s[qi]
                seen, top = set(), []
                for lab, dist in zip(labels[qi], dists[qi]):
                    j = owner[lab]
                    if j == j0 or j in seen:
                        continue
                    seen.add(j)
                    top.append((1.0 - dist, j))       # hnswlib ip distance is 1 - dot
                top.append((own[qi], j0))
                top.sort(key=lambda x: (-x[0], x[1] != j0))
                dirs10 = [j for _, j in top[:K_DIRS]]
                ov[qi] = len(set(dirs10) & set(exact_dirs[qi].tolist())) / K_DIRS
                dh[qi] = float(j0 in dirs10)
                cand = np.concatenate([np.arange(fstart[j], fstart[j + 1]) for j in dirs10])
                cand = all_files[cand]
                cand = cand[cand != qpos[qi]]
                m = file_metrics(V[cand] @ Q[qi], file_dir[cand] == j0, n_sib[qi])
                h1[qi], h10[qi] = m[0], m[2]
            lo, hi = boot_ci(h10 - d_hit10, qd, 202)

            def two(q):
                lab, _ = idx.knn_query(q, k=K_REPS, num_threads=1)
                seen, top = set(), []
                for l in lab[0]:
                    j = owner[l]
                    if j not in seen:
                        seen.add(j)
                        top.append(j)
                        if len(top) == K_DIRS:
                            break
                cand = np.concatenate([np.arange(fstart[j], fstart[j + 1]) for j in top])
                s = F[cand] @ q
                t = np.argpartition(-s, 10)[:10] if len(s) > 10 else np.arange(len(s))
                return cand[t[np.argsort(-s[t])]]
            with threadpool_limits(limits=1):
                t = clock(two)
            per[f"hnsw_{rep}_ef{ef}"] = (h1, h10)
            times[f"hnsw_{rep}_ef{ef}"] = t
            out.append(f"| {rep} | {len(R)} | {nbytes / 1e6:.1f} | {build_s:.0f} | {max(ef, K_REPS)} | "
                       f"{ov.mean():.3f} | {dh.mean():.3f} | {h1.mean():.3f} | {h10.mean():.3f} | "
                       f"{h10.mean() - d_hit10.mean():+.3f} | [{lo:+.3f}, {hi:+.3f}] | {t:.0f} |")
            print(f"  stage 1 {rep} ef {ef} done", file=sys.stderr, flush=True)
        del idx
    out.append("")
    out.append("Check: exact two-stage (k = 10, leave-one-out) from this script against twostage.jsonl: "
               + "; ".join(checks) + ".")

    # ------------------------------------------------ per-query rows
    with open(os.path.join(emb_dir, "hnsw.jsonl"), "w") as fh:
        for qi, g in enumerate(queries):
            row = {k: g[k] for k in ("query_path", "relevant_dir", "modality", "image_frac_bucket")}
            for key, (h1, h10) in per.items():
                row[key] = {"hit@1": float(h1[qi]), "hit@10": float(h10[qi])}
            fh.write(json.dumps(row) + "\n")
    with open(os.path.join(emb_dir, "hnsw_times.json"), "w") as fh:
        json.dump({"us_per_query": times, "flat_index_bytes": flat_bytes, "stage1_index_bytes": storage,
                   "file_vector_bytes": int(F.nbytes)}, fh, indent=1)

    # ------------------------------------------------ H7: paired comparison at matched time
    qm = np.array([g["modality"] for g in queries])
    qb = np.array([g["image_frac_bucket"] for g in queries])
    cells = [("all queries", np.ones(nq, bool), 301),
             ("P1 image in [0,.2)+[.2,.5)", (qm == "image") & np.isin(qb, BUCKETS[:2]), 302),
             ("P2 textlike in [.5,.8)+[.8,1]", np.isin(qm, TEXTLIKE) & np.isin(qb, BUCKETS[2:]), 303)]
    out.append("")
    out.append(f"### H7: two-stage HNSW (stage 1 ef_search {H7_EF}) against flat HNSW at matched time")
    out.append("")
    out.append("Matched flat setting: the smallest ef_search in {" + ", ".join(map(str, EFS)) + "} whose query "
               "time in this run is at least the two-stage query time. Paired 95% interval, 1000 resamples of "
               "the cell's directories. Storage: stage 1 index plus the raw file vectors for stage 2, against "
               f"the flat index ({flat_bytes / 1e6:.1f} MB, vectors included).")
    out.append("")
    out.append("| stage 1 | cell | queries | dirs | two-stage us | matched flat ef | flat us | two-stage hit@10 | "
               "flat hit@10 | hit@10 diff | 95% CI | two-stage hit@1 | flat hit@1 | hit@1 diff | 95% CI | storage ratio |")
    out.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---|---:|")
    for rep in ["c", "c4", "c2"]:
        key = f"hnsw_{rep}_ef{H7_EF}"
        t2 = times[key]
        match = next((ef for ef in EFS if times[f"flat_ef{ef}"] >= t2), None)
        ratio = (storage[rep] + F.nbytes) / flat_bytes
        for name, sel, seed in cells:
            if match is None:
                out.append(f"| {rep} | {name} | {int(sel.sum())} | | {t2:.0f} | none | | | | | | | | | | {ratio:.2f} |")
                continue
            fk = f"flat_ef{match}"
            cols = []
            for m in (1, 0):
                x = per[key][m][sel] - per[fk][m][sel]
                lo, hi = boot_ci(x, qd[sel], seed)
                cols.append(f"{per[key][m][sel].mean():.3f} | {per[fk][m][sel].mean():.3f} | "
                            f"{x.mean():+.4f} | [{lo:+.4f}, {hi:+.4f}]")
            out.append(f"| {rep} | {name} | {int(sel.sum())} | {len(set(qd[sel]))} | {t2:.0f} | {match} | "
                       f"{times[fk]:.0f} | " + " | ".join(cols) + f" | {ratio:.2f} |")
    print("\n".join(out))


if __name__ == "__main__":
    main()
