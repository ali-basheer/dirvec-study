#!/usr/bin/env python3
"""Leave-one-out directory retrieval (dirvec): an independent re-implementation.

Written from the written specification only. For every evaluation query file f in a
directory D0, the file's vector is scored against one representation per directory and
the rank of D0 among the ranked directories is reported for three representations:

    a  one vector, the L2-normalised mean of the directory's child vectors
    c  per-modality k-means representatives, k = min(3, n) per modality label
    d  every child vector (the flat file-level walk)

A directory scores the maximum dot product between the query vector and its
representative vectors. D0 is rebuilt without f; every other directory keeps the
representation built from all its children. The rank of a query is 1 plus the number of
other ranked directories whose float32 score is strictly greater than D0's score.

Numerics (the specification leaves these open; they only matter for queries whose own
score is within a few float32 ulps of a competitor's): every vector and score is float32;
the competitor scores of a block of queries come from one matrix-matrix product per row
type (numpy @, never a block of one query), and D0's own score is a separate matrix-vector
product of its leave-one-out representation with the query vector.

Example:
    python3 scripts/indep_eval.py --manifest data/manifest_s11.jsonl \
        --dirs data/dirs_s11.jsonl --gt data/gt_structural_s11.jsonl \
        --emb data/emb/synth16 --calib 0.2 --calib-seed 20261102 \
        --out /tmp/indep_ranks.jsonl --check data/emb/synth16/ranks_synth.jsonl
"""

import argparse
import concurrent.futures as cf
import json
import multiprocessing as mp
import os
import sys
import time
import warnings
from types import SimpleNamespace

import numpy as np

LABELS = ("image", "pdf_text", "pdf_scanned", "text", "table", "other")
BUCKETS = ("[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]")
TEXT_LIKE = ("text", "table", "pdf_text", "other")
TEXT_HEAVY = ("[0,.2)", "[.2,.5)")      # image fraction below 0.5
IMAGE_HEAVY = ("[.5,.8)", "[.8,1]")     # image fraction of 0.5 or more
CELLS = ("all", "P1", "P2", "M1", "M2")
REPS = ("a", "c", "d")
KS = (1, 5, 10)
NORM_FLOOR = 1e-12
NEG_INF = np.float32(-np.inf)


def fail(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(2)


def log(msg):
    sys.stderr.write("[%7.1fs] %s\n" % (time.time() - T0, msg))
    sys.stderr.flush()


T0 = time.time()


# --------------------------------------------------------------------------------------
# small helpers taken straight from the definitions
# --------------------------------------------------------------------------------------
def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def bucket_of(x):
    """Definition 1."""
    if x < 0.2:
        return "[0,.2)"
    if x < 0.5:
        return "[.2,.5)"
    if x < 0.8:
        return "[.5,.8)"
    return "[.8,1]"


def calibration_split(dir_rows, calib, calib_seed):
    """Definition 2: one generator, buckets in the fixed order, sorted directory lists."""
    rng = np.random.default_rng(calib_seed)
    by_bucket = {b: [] for b in BUCKETS}
    for row in dir_rows:
        by_bucket[bucket_of(row["image_frac"])].append(row["dir"])
    cal = set()
    for b in BUCKETS:
        ds = sorted(by_bucket[b])
        n_cal = int(round(calib * len(ds)))
        perm = rng.permutation(len(ds))
        for i in perm[:n_cal]:
            cal.add(ds[int(i)])
    return cal


def cells_of(modality, bucket):
    """Definition 10. pdf_scanned queries (and any other label) belong to 'all' only."""
    out = ["all"]
    if modality == "image":
        if bucket in TEXT_HEAVY:
            out.append("P1")
        elif bucket in IMAGE_HEAVY:
            out.append("M1")
    elif modality in TEXT_LIKE:
        if bucket in IMAGE_HEAVY:
            out.append("P2")
        elif bucket in TEXT_HEAVY:
            out.append("M2")
    return out


# --------------------------------------------------------------------------------------
# representations (Definition 6)
# --------------------------------------------------------------------------------------
def unit_rows(M):
    """Divide each row by its L2 norm, with a floor of 1e-12 on the norm (float32)."""
    nrm = np.linalg.norm(M, axis=1, keepdims=True)
    return M / np.maximum(nrm, np.float32(NORM_FLOOR))


def rep_a(X):
    """Mean of the rows of X divided by its L2 norm; X is float32 with at least one row."""
    m = X.mean(axis=0)
    nrm = np.linalg.norm(m)
    return m / np.maximum(nrm, np.float32(NORM_FLOOR))


def rep_c_group(G):
    """Representatives of one modality group (rows in manifest order)."""
    n = G.shape[0]
    k = min(3, n)
    if k == n:
        return G
    from sklearn.cluster import KMeans

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(G)
    cent = np.asarray(km.cluster_centers_).astype(np.float32)
    return unit_rows(cent)


# --------------------------------------------------------------------------------------
# loading the inputs
# --------------------------------------------------------------------------------------
def load_world(cfg, full_checks):
    w = SimpleNamespace()
    man = read_jsonl(cfg["manifest"])
    index = read_jsonl(os.path.join(cfg["emb"], "index.jsonl"))
    if len(index) != len(man):
        fail("index.jsonl has %d rows but the manifest has %d" % (len(index), len(man)))
    for i, (m, r) in enumerate(zip(man, index)):
        if m["path"] != r["path"]:
            fail("row %d: manifest path %r differs from index path %r" % (i, m["path"], r["path"]))
    V = np.load(os.path.join(cfg["emb"], "vectors.npy"), mmap_mode="r")
    if V.ndim != 2 or V.shape[0] != len(man):
        fail("vectors.npy has shape %s for %d manifest rows" % (V.shape, len(man)))
    if V.dtype != np.float32:
        fail("vectors.npy is %s, expected float32" % V.dtype)
    w.V = V
    w.dim = V.shape[1]
    for i, r in enumerate(index):
        if not isinstance(r["ok"], (bool, int)):
            fail("index.jsonl row %d: ok is %r, expected a boolean" % (i, r["ok"]))
    w.ok = np.array([bool(r["ok"]) for r in index], dtype=bool)
    w.mod = np.array([m["modality"] for m in man])
    w.row_dir = [m["dir"] for m in man]
    bad = sorted(set(w.mod.tolist()) - set(LABELS))
    if bad:
        fail("unknown modality labels in the manifest: %s" % bad)
    if full_checks:
        dev = 0.0
        for s0 in range(0, len(man), 4096):
            blk = np.array(V[s0:s0 + 4096], dtype=np.float32)[w.ok[s0:s0 + 4096]]
            if blk.size:
                dev = max(dev, float(np.abs(np.sqrt((blk.astype(np.float64) ** 2).sum(axis=1)) - 1.0).max()))
        w.norm_dev = dev
        if w.norm_dev > 1e-3:
            sys.stderr.write("warning: ok rows are not unit length (max deviation %.3g)\n" % w.norm_dev)

    dir_rows = read_jsonl(cfg["dirs"])
    w.cal = calibration_split(dir_rows, cfg["calib"], cfg["calib_seed"])          # Definition 2
    w.ranked = sorted(r["dir"] for r in dir_rows if r["n_files"] >= 3)            # Definition 3
    w.n_dirs = len(dir_rows)

    kids = {}                                                                     # Definition 4
    for i, d in enumerate(w.row_dir):
        if w.ok[i]:
            kids.setdefault(d, []).append(i)
    w.children = {d: np.array(v, dtype=np.int64) for d, v in kids.items()}

    row_of = {m["path"]: i for i, m in enumerate(man)}
    w.queries = []                                                                # Definition 5
    for g in read_jsonl(cfg["gt"]):
        if g["relevant_dir"] in w.cal:
            continue
        i = row_of.get(g["query_path"])
        if i is None or not w.ok[i]:
            continue
        w.queries.append((g, i))
    w.by_dir = {}
    for qpos, (g, i) in enumerate(w.queries):
        w.by_dir.setdefault(g["relevant_dir"], []).append((qpos, i))
    return w


# --------------------------------------------------------------------------------------
# per-directory work: full 'c' representation and the leave-one-out score of D0
# --------------------------------------------------------------------------------------
_W = None
_LIMITS = None


def _init_worker(cfg):
    global _W, _LIMITS
    try:
        from threadpoolctl import threadpool_limits

        _LIMITS = threadpool_limits(limits=1)
    except Exception:
        pass
    _W = load_world(cfg, full_checks=False)


def work_chunk(dir_names):
    """For each directory: its full 'c' representation (needed as a competitor), and for
    each evaluation query inside it the three leave-one-out scores of the directory."""
    w = _W
    c_full = []
    own = []
    for D in dir_names:
        ch = w.children.get(D)
        if ch is None:
            c_full.append((D, np.zeros((0, w.dim), dtype=np.float32)))
            continue
        X = np.array(w.V[ch], dtype=np.float32)
        labs = w.mod[ch]
        groups = {}
        for L in LABELS:
            sel = np.nonzero(labs == L)[0]
            if sel.size:
                groups[L] = sel
        full = {L: rep_c_group(X[sel]) for L, sel in groups.items()}
        c_full.append((D, np.concatenate([full[L] for L in LABELS if L in full])))

        for qpos, mi in w.by_dir.get(D, ()):
            pos = np.nonzero(ch == mi)[0]
            if pos.size != 1:
                fail("query row %d is not among the ok children of %s" % (mi, D))
            pos = int(pos[0])
            q = np.array(w.V[mi], dtype=np.float32)
            keep = np.ones(len(ch), dtype=bool)
            keep[pos] = False
            if not keep.any():          # D0 has no vector left once f is out
                own.append((qpos, NEG_INF, NEG_INF, NEG_INF))
                continue
            Xl = X[keep]
            s_a = np.float32(rep_a(Xl) @ q)
            s_d = np.float32((Xl @ q).max())
            parts = []
            for L in LABELS:
                if L == labs[pos]:
                    rest = groups[L][groups[L] != pos]
                    if rest.size:
                        parts.append(rep_c_group(X[rest]))
                elif L in full:
                    parts.append(full[L])
            s_c = np.float32((np.concatenate(parts) @ q).max())
            own.append((qpos, s_a, s_c, s_d))
    return c_full, own


# --------------------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------------------
def segments(blocks):
    """blocks: list (one per ranked directory) of float32 (m_i, dim) arrays.
    Returns the stacked matrix, the start offset of every non-empty block and the index
    (in ranked order) of those directories."""
    counts = np.array([b.shape[0] for b in blocks], dtype=np.int64)
    starts = np.concatenate([[0], np.cumsum(counts)[:-1]]) if len(counts) else counts
    nonempty = np.nonzero(counts > 0)[0]
    M = np.ascontiguousarray(np.concatenate([b for b in blocks if b.shape[0]]))
    return M, starts[nonempty], nonempty


def block_product(Q, M):
    """Q @ M.T in float32. A single query would be routed to a matrix-vector kernel whose
    last-bit rounding differs from the matrix-matrix kernel, so it is padded to two rows."""
    if Q.shape[0] == 1:
        return (np.concatenate([Q, Q]) @ M.T)[:1]
    return Q @ M.T


def max_per_directory(Q, M, starts, nonempty, n_ranked):
    S = block_product(Q, M)                       # (B, rows), float32
    mx = np.maximum.reduceat(S, starts, axis=1)    # (B, n_nonempty)
    full = np.full((Q.shape[0], n_ranked), -np.inf, dtype=np.float32)
    full[:, nonempty] = mx
    return full


def evaluate(w, procs, block):
    global _W
    ranked = w.ranked
    n_ranked = len(ranked)
    pos_of = {d: j for j, d in enumerate(ranked)}
    n_q = len(w.queries)

    # phase 1: representation 'c' of every ranked directory and the own scores
    own = np.full((3, n_q), -np.inf, dtype=np.float32)
    c_by_dir = {}
    chunk = 12
    chunks = [ranked[i:i + chunk] for i in range(0, n_ranked, chunk)]
    done = 0
    last = time.time()

    def take(res):
        nonlocal done, last
        cf_, ow_ = res
        for D, C in cf_:
            c_by_dir[D] = C
        for qpos, s_a, s_c, s_d in ow_:
            own[0, qpos], own[1, qpos], own[2, qpos] = s_a, s_c, s_d
        done += 1
        if time.time() - last > 30:
            last = time.time()
            log("phase 1: %d/%d chunks" % (done, len(chunks)))

    if procs > 1:
        for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
            os.environ[var] = "1"
        try:
            ctx = mp.get_context("spawn")
            with cf.ProcessPoolExecutor(max_workers=procs, mp_context=ctx,
                                        initializer=_init_worker, initargs=(w.cfg,)) as ex:
                for res in ex.map(work_chunk, chunks):
                    take(res)
        except (OSError, cf.process.BrokenProcessPool) as exc:
            log("worker pool failed (%s); redoing phase 1 in this process" % exc)
            c_by_dir.clear()
            own[:] = -np.inf
            done = 0
            procs = 1
    if procs <= 1:
        _W = w
        for ch_ in chunks:
            take(work_chunk(ch_))
    log("phase 1 done (%d directories, %d queries)" % (n_ranked, n_q))

    # phase 2: one matrix product per row type for blocks of queries
    a_rows, d_blocks, c_blocks = [], [], []
    for D in ranked:
        ch = w.children.get(D)
        if ch is None:
            a_rows.append(None)
            d_blocks.append(np.zeros((0, w.dim), dtype=np.float32))
        else:
            X = np.array(w.V[ch], dtype=np.float32)
            a_rows.append(rep_a(X))
            d_blocks.append(X)
        c_blocks.append(c_by_dir[D])
    a_idx = np.array([j for j, r in enumerate(a_rows) if r is not None], dtype=np.int64)
    A = np.ascontiguousarray(np.stack([r for r in a_rows if r is not None]))
    Dm, d_start, d_ne = segments(d_blocks)
    Cm, c_start, c_ne = segments(c_blocks)
    log("matrices: A %s  C %s  D %s" % (A.shape, Cm.shape, Dm.shape))

    q_rows = np.array([i for _, i in w.queries], dtype=np.int64)
    q_dir = np.array([pos_of.get(g["relevant_dir"], -1) for g, _ in w.queries], dtype=np.int64)
    ranks = np.zeros((3, n_q), dtype=np.int64)
    ties = np.zeros((3, 2), dtype=np.int64)      # queries with an exact tie / a near tie
    last = time.time()
    for b0 in range(0, n_q, block):
        b1 = min(b0 + block, n_q)
        B = b1 - b0
        Q = np.array(w.V[q_rows[b0:b1]], dtype=np.float32)
        sa = np.full((B, n_ranked), -np.inf, dtype=np.float32)
        sa[:, a_idx] = block_product(Q, A)
        sc = max_per_directory(Q, Cm, c_start, c_ne, n_ranked)
        sd = max_per_directory(Q, Dm, d_start, d_ne, n_ranked)
        sel = q_dir[b0:b1]
        have = np.nonzero(sel >= 0)[0]
        for r, sc_ in enumerate((sa, sc, sd)):
            sc_[have, sel[have]] = -np.inf            # D0 itself never competes
            o = own[r, b0:b1]
            ranks[r, b0:b1] = 1 + (sc_ > o[:, None]).sum(axis=1)
            finite = np.isfinite(o)
            with np.errstate(invalid="ignore"):
                diff = np.abs(sc_ - o[:, None])
            ties[r, 0] += int(((diff == 0) & finite[:, None]).any(axis=1).sum())
            ties[r, 1] += int(((diff <= 1e-6) & finite[:, None]).any(axis=1).sum())
        if time.time() - last > 30:
            last = time.time()
            log("phase 2: %d/%d queries" % (b1, n_q))
    log("phase 2 done")
    return ranks, ties, procs


# --------------------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------------------
def cell_members(rows):
    """rows: list of (modality, bucket). Returns {cell: boolean mask}."""
    masks = {c: np.zeros(len(rows), dtype=bool) for c in CELLS}
    for j, (m, b) in enumerate(rows):
        for c in cells_of(m, b):
            masks[c][j] = True
    return masks


def recall(rank_vec, mask, k):
    n = int(mask.sum())
    if n == 0:
        return float("nan")
    return float((rank_vec[mask] <= k).sum()) / n


def fmt(x):
    return "n/a" if x != x else "%.4f" % x


def print_report(rows, ranks, ties, check_path, out_path, ranked_n, cal_n):
    masks = cell_members([(g["modality"], g["image_frac_bucket"]) for g, _ in rows])
    print("Evaluation queries: %d" % len(rows))
    print("Ranked directories: %d; calibration directories: %d" % (ranked_n, cal_n))
    print("Cell sizes: " + ", ".join("%s=%d" % (c, int(masks[c].sum())) for c in CELLS))
    print()
    print("| row | metric | " + " | ".join(CELLS) + " |")
    print("|---|---|" + "---|" * len(CELLS))
    for r, name in enumerate(REPS):
        for k in KS:
            print("| %s | recall@%d | %s |" % (
                name, k, " | ".join(fmt(recall(ranks[r], masks[c], k)) for c in CELLS)))
    print()
    print("Ranks written to %s" % out_path)
    sys.stderr.write("ties with the own score (exact / within 1e-6), queries per row: %s\n" % (
        ", ".join("%s=%d/%d" % (n, ties[r, 0], ties[r, 1]) for r, n in enumerate(REPS))))

    if not check_path:
        return
    chk = {}
    for row in read_jsonl(check_path):
        chk[row["query_path"]] = row
    mine = {g["query_path"]: j for j, (g, _) in enumerate(rows)}
    common = [p for p in mine if p in chk]
    only_mine = len(mine) - len(common)
    only_chk = len(chk) - len(common)
    print()
    print("Check against %s" % check_path)
    print("Queries present in both files: %d (only in mine: %d, only in check: %d)" % (
        len(common), only_mine, only_chk))
    if not common:
        return
    jm = np.array([mine[p] for p in common], dtype=np.int64)
    cm = cell_members([(chk[p]["modality"], chk[p]["image_frac_bucket"]) for p in common])
    mm = {c: masks[c][jm] for c in CELLS}
    for c in CELLS:
        if (mm[c] != cm[c]).any():
            print("note: cell %s membership differs between the two files for %d queries" % (
                c, int((mm[c] != cm[c]).sum())))
    print()
    print("| row | queries differing | share identical | " + " | ".join(
        "recall@5 %s mine / check" % c for c in CELLS) + " |")
    print("|---|---|---|" + "---|" * len(CELLS))
    diffs = {}
    for r, name in enumerate(REPS):
        a = ranks[r][jm]
        b = np.array([chk[p]["rank_" + name] for p in common], dtype=np.int64)
        nd = int((a != b).sum())
        diffs[name] = (a, b)
        print("| %s | %d | %.6f | %s |" % (
            name, nd, 1.0 - nd / len(common),
            " | ".join("%s / %s" % (fmt(recall(a, mm[c], 5)), fmt(recall(b, cm[c], 5)))
                       for c in CELLS)))
    for name in REPS:
        a, b = diffs[name]
        nd = np.nonzero(a != b)[0]
        if nd.size:
            show = ", ".join("(%s: mine %d, check %d)" % (
                os.path.basename(common[int(i)]), a[i], b[i]) for i in nd[:8])
            print("first differences in row %s: %s" % (name, show))


# --------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--gt", required=True)
    ap.add_argument("--emb", required=True, help="cache directory with vectors.npy and index.jsonl")
    ap.add_argument("--calib", type=float, required=True)
    ap.add_argument("--calib-seed", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--check", default=None, help="ranks jsonl of the first implementation")
    ap.add_argument("--procs", type=int, default=0, help="worker processes for the k-means phase (0: all cores up to 3)")
    ap.add_argument("--block", type=int, default=512, help="queries per matrix product")
    args = ap.parse_args()

    cfg = dict(manifest=args.manifest, dirs=args.dirs, gt=args.gt, emb=args.emb,
               calib=args.calib, calib_seed=args.calib_seed)
    w = load_world(cfg, full_checks=True)
    w.cfg = cfg
    log("loaded: %d manifest rows (%d ok), %d ranked directories, %d calibration directories, "
        "%d evaluation queries" % (len(w.row_dir), int(w.ok.sum()), len(w.ranked), len(w.cal), len(w.queries)))
    if not w.queries:
        fail("no evaluation queries")
    procs = args.procs
    if procs <= 0:
        try:
            procs = len(os.sched_getaffinity(0))
        except AttributeError:
            procs = os.cpu_count() or 1
        procs = max(1, min(procs, 3))

    ranks, ties, procs = evaluate(w, procs, max(1, args.block))

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        for j, (g, _) in enumerate(w.queries):
            fh.write(json.dumps({
                "query_path": g["query_path"],
                "relevant_dir": g["relevant_dir"],
                "modality": g["modality"],
                "image_frac_bucket": g["image_frac_bucket"],
                "rank_a": int(ranks[0, j]),
                "rank_c": int(ranks[1, j]),
                "rank_d": int(ranks[2, j]),
            }) + "\n")
    print_report(w.queries, ranks, ties, args.check, args.out, len(w.ranked), len(w.cal))
    print()
    print("Elapsed seconds: %.1f (%d worker process%s for the k-means phase)" % (
        time.time() - T0, procs, "" if procs == 1 else "es"))
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
