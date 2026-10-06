#!/usr/bin/env python3
"""dirvec session 16: the target type known in advance (BRIEF.md, session 16).

The query's type is its kind, as a file system records it: image, pdf (pdf_text or pdf_scanned),
text, table, other. Rows, all uncentered and leave-one-out as in eval.py:
  a, c, d          eval.py's pooled centroid, per-modality k-reps and every file. With --check-ranks
                   their ranks must equal that file's rank_a, rank_c and rank_d query for query, or the
                   script stops with exit code 3 before any other number is printed.
  a+F, c+F, d+F    composition filter: only directories whose composition holds the query's kind are
                   ranked. Composition: the manifest's files of the directory, with or without a
                   vector; the query file counts in its own directory, which the stored folder holds.
  a+P, c+P, d+P    composition prior: score + tau * ln share(D) over the directories x+F ranks, share
                   = files of the query's kind / files of D (the same counts). tau per row, chosen on
                   the dev queries: the TAUS value with the highest recall@5 over all dev queries,
                   ties to the smaller tau.
  a_T, c_T, d_T    type-only groups: a directory is scored only by its representatives of the
                   query's kind: a_T the unit mean of its files of that kind, c_T c's representatives
                   of the labels of that kind, d_T its files of that kind. A directory with no vector
                   of that kind is not ranked.
Singletons: queries whose own directory keeps no other file of their kind with a vector. Under x_T
their own directory has nothing to match, so x_T is compared on the other queries only.
Ranks as eval.py: 1 + the number of ranked directories scoring strictly higher than the own
directory, float32 scores (float64 once the prior is added). Paired bootstrap as eval.py: 1000
resamples of the cell's directories, eval.py's cell seeds.

  typeq.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s11 --manifest data/manifest_s11.jsonl
           --dirs data/dirs_s11.jsonl --gt data/gt_structural_s11.jsonl --calib 0.2
           --calib-seed 20261102 --check-ranks data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl
           --label E1 --tag _s16_e1 [--selftest 200]
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

KIND = {"image": "image", "pdf_text": "pdf", "pdf_scanned": "pdf", "text": "text", "table": "table",
        "other": "other"}
KINDS = ["image", "pdf", "text", "table", "other"]
TAUS = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
BASES = ["a", "c", "d"]
ROWS = BASES + [f"{x}+F" for x in BASES] + [f"{x}+P" for x in BASES]
ROWS_T = [f"{x}_T" for x in BASES]
MISS = 10 ** 9            # rank of a query whose own directory has nothing to match (singletons, x_T)


def rep_kinds(base, mods):
    """Kind of each representative eval.py's build(base) returns, in its order (None for a)."""
    if base == "a":
        return np.array([None], dtype=object)
    if base == "d":
        return np.array([KIND[m] for m in mods], dtype=object)
    return np.array([KIND[m] for m in ev.MODALITIES for _ in range(min(3, int((mods == m).sum())))],
                    dtype=object)


def kind_means(X, kinds):
    """a_T's vectors: {kind: (1, dim) unit mean of the files of that kind}."""
    return {k: ev.unit(X[kinds == k].mean(axis=0, keepdims=True)) for k in KINDS if (kinds == k).any()}


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
    ap.add_argument("--tag", default="_s16")
    ap.add_argument("--selftest", type=int, default=0,
                    help="recompute the F, P and T ranks of this many evaluation queries with plain loops")
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
    kinds_all = np.array([KIND[m] for m in mods_all], dtype=object)
    dir_list = sorted(d for d, r in dirs.items() if r["n_files"] >= 3)
    dir_idx = {d: j for j, d in enumerate(dir_list)}
    n_dirs = len(dir_list)
    children = {d: [] for d in dir_list}
    for i, r in enumerate(manifest):
        if ok[i] and r["dir"] in children:
            children[r["dir"]].append(i)
    children = {d: np.array(v, int) for d, v in children.items()}

    # composition over the manifest (every kept file, with or without a vector)
    comp = np.zeros((n_dirs, len(KINDS)))
    for r in manifest:
        if r["dir"] in dir_idx:
            comp[dir_idx[r["dir"]], KINDS.index(KIND[r["modality"]])] += 1
    with np.errstate(divide="ignore"):
        logshare = np.log(comp / comp.sum(axis=1, keepdims=True))      # -inf where the kind is absent

    calib = ev.calib_split(dirs, args.calib, args.calib_seed)
    q_eval = [g for g in gt if ok[pos[g["query_path"]]] and g["relevant_dir"] not in calib]
    q_dev = [g for g in gt if ok[pos[g["query_path"]]] and g["relevant_dir"] in calib]
    print(f"{args.label}: {len(q_eval)} eval and {len(q_dev)} dev queries, {n_dirs} directories ranked",
          file=sys.stderr)

    # full representations per base, their owners and kinds (dir_list order, so owners are sorted)
    full, fkind = {}, {}
    for base in BASES:
        full[base] = {d: ev.build(base, V[children[d]], mods_all[children[d]]) for d in dir_list}
        fkind[base] = {d: rep_kinds(base, mods_all[children[d]]) for d in dir_list}
        assert all(len(full[base][d]) == len(fkind[base][d]) for d in dir_list), base
    means = {d: kind_means(V[children[d]], kinds_all[children[d]]) for d in dir_list}
    n_vec = {"a": 1.0, "c": np.mean([len(full["c"][d]) for d in dir_list]),
             "d": np.mean([len(full["d"][d]) for d in dir_list]),
             "a_T": np.mean([len(means[d]) for d in dir_list])}

    def score_rows(queries, with_t, sample=()):
        """Ranks of every row for the given queries. Returns {row: ranks}, {tau: {base: ranks}},
        the singleton mask, the score rows of the self-test sample and per-query facts."""
        qpos = np.array([pos[g["query_path"]] for g in queries])
        qkind = kinds_all[qpos]
        Q = V[qpos]
        ranks = {r: np.zeros(len(queries), np.int64) for r in ROWS + (ROWS_T if with_t else [])}
        pr = {t: {b: np.zeros(len(queries), np.int64) for b in BASES} for t in TAUS}
        single = np.zeros(len(queries), bool)
        keep_of = []
        for g, p in zip(queries, qpos):
            c = children[g["relevant_dir"]]
            keep_of.append(c[c != p])
        for k, keep in enumerate(keep_of):
            single[k] = not (kinds_all[keep] == qkind[k]).any()
        j0s = np.array([dir_idx[g["relevant_dir"]] for g in queries])
        kidx = np.array([KINDS.index(x) for x in qkind])
        cand = comp[:, kidx].T >= 1                                   # (nq, n_dirs) filter
        assert cand[np.arange(len(queries)), j0s].all(), "own directory must pass the filter"
        keep_scores = {}
        for base in BASES:
            allR = np.concatenate([full[base][d] for d in dir_list])
            allK = np.concatenate([fkind[base][d] for d in dir_list])
            owner = np.concatenate([np.full(len(full[base][d]), j) for j, d in enumerate(dir_list)])
            assert (np.diff(owner) >= 0).all()
            bounds = np.searchsorted(owner, np.arange(n_dirs + 1))
            S = Q @ allR.T                                            # as eval.py: one product, all queries
            dsc = np.full((len(queries), n_dirs), -np.inf, np.float32)
            for j in range(n_dirs):
                if bounds[j + 1] > bounds[j]:
                    dsc[:, j] = S[:, bounds[j]:bounds[j + 1]].max(axis=1)
            tsc = None
            if with_t:
                tsc = np.full((len(queries), n_dirs), -np.inf, np.float32)
                for K in KINDS:
                    qs = np.where(qkind == K)[0]
                    if not len(qs):
                        continue
                    if base == "a":                                   # a_T: one unit mean per kind
                        js = [j for j, d in enumerate(dir_list) if K in means[d]]
                        if js:
                            M = np.concatenate([means[dir_list[j]][K] for j in js])
                            tsc[np.ix_(qs, js)] = Q[qs] @ M.T
                        continue
                    cols = np.where(allK == K)[0]
                    if not len(cols):
                        continue
                    sub = S[np.ix_(qs, cols)]
                    starts = np.searchsorted(owner[cols], np.arange(n_dirs + 1))
                    for j in range(n_dirs):
                        if starts[j + 1] > starts[j]:
                            tsc[qs, j] = sub[:, starts[j]:starts[j + 1]].max(axis=1)
            if len(sample):
                keep_scores[base] = (S[sample], dsc[sample], tsc[sample], allK, owner)
            for k, g in enumerate(queries):
                j0, keep = j0s[k], keep_of[k]
                Rk = ev.build(base, V[keep], mods_all[keep])
                own = np.float32((Rk @ Q[k]).max()) if len(Rk) else np.float32(-np.inf)
                s = dsc[k].copy()
                s[j0] = own
                assert s.dtype == np.float32
                ranks[base][k] = 1 + int((s > own).sum())
                ranks[f"{base}+F"][k] = 1 + int((s[cand[k]] > own).sum())
                s64 = s.astype(np.float64)
                own64 = float(own)
                for t in TAUS:
                    sp = s64 + t * logshare[:, kidx[k]]
                    pr[t][base][k] = 1 + int((sp > own64 + t * logshare[j0, kidx[k]]).sum())
                if with_t:
                    if base == "a":
                        m = kind_means(V[keep], kinds_all[keep]).get(qkind[k])
                        own_t = np.float32((m @ Q[k]).max()) if m is not None else np.float32(-np.inf)
                    else:
                        sel = rep_kinds(base, mods_all[keep]) == qkind[k]
                        own_t = np.float32((Rk[sel] @ Q[k]).max()) if sel.any() else np.float32(-np.inf)
                    assert np.isfinite(own_t) != single[k], "singleton flag and type-only group disagree"
                    st = tsc[k].copy()
                    st[j0] = own_t
                    ranks[f"{base}_T"][k] = MISS if single[k] else 1 + int((st > own_t).sum())
            print(f"  {args.label} {'eval' if with_t else 'dev'} {base} done", file=sys.stderr)
        return ranks, pr, single, keep_scores, (qkind, j0s, kidx, cand)

    # dev queries: the prior's weight
    dranks, dpr, _, _, _ = score_rows(q_dev, with_t=False)
    tau = {}
    dev_tab = {}
    for b in BASES:
        r5 = {t: float((dpr[t][b] <= 5).mean()) for t in TAUS}
        dev_tab[b] = (float((dranks[f"{b}+F"] <= 5).mean()), r5)
        best = max(r5.values())
        tau[b] = next(t for t in TAUS if r5[t] == best)

    sample = np.array([], int)
    if args.selftest:
        sample = np.sort(np.random.default_rng(16).choice(len(q_eval), size=min(args.selftest, len(q_eval)),
                                                           replace=False))
    ranks, epr, single, ks, (qkind, j0s, kidx, cand) = score_rows(q_eval, with_t=True, sample=sample)
    for b in BASES:
        ranks[f"{b}+P"] = epr[tau[b]][b]

    out = []
    head = f"## {args.label}: {args.model}" if args.label else f"## {args.model}"
    out.append(head)
    out.append("")

    # reproduction of eval.py's a, c, d ranks
    if args.check_ranks:
        ref = {}
        for l in open(os.path.join(R, args.check_ranks)):
            r = json.loads(l)
            ref[r["query_path"]] = r
        mine = [g["query_path"] for g in q_eval]
        same_set = set(mine) == set(ref)
        diffs = Counter()
        examples = []
        for k, qp in enumerate(mine):
            if qp not in ref:
                continue
            for b in BASES:
                if int(ref[qp][f"rank_{b}"]) != int(ranks[b][k]):
                    diffs[b] += 1
                    if len(examples) < 10:
                        examples.append(f"{qp} {b}: eval.py {ref[qp][f'rank_{b}']}, typeq {ranks[b][k]}")
        ok_rep = same_set and not diffs
        out.append(f"Reproduction of {args.check_ranks}: {len(mine)} queries here, {len(ref)} there, same set: "
                   f"{'yes' if same_set else 'NO'}; queries whose rank differs: " +
                   ", ".join(f"{b} {diffs[b]}" for b in BASES) + f". {'Reproduced rank for rank.' if ok_rep else 'NOT REPRODUCED.'}")
        if not ok_rep:
            out.extend(examples)
            print("\n".join(out))
            sys.exit(3)
        out.append("")

    # self-test: the F, P and T ranks of a sample recomputed with plain loops from the same scores
    if args.selftest:
        bad = Counter()
        for base in BASES:
            S, dsc, tsc, allK, owner = ks[base]
            for row, k in enumerate(sample):
                g = q_eval[k]
                j0, K = j0s[k], qkind[k]
                ki = KINDS.index(K)
                q = V[pos[g["query_path"]]]
                keep = children[g["relevant_dir"]]
                keep = keep[keep != pos[g["query_path"]]]
                Rk = ev.build(base, V[keep], mods_all[keep])
                own = np.float32((Rk @ q).max()) if len(Rk) else np.float32(-np.inf)
                sh0 = comp[j0, ki] / comp[j0].sum()
                rf = rp = 1
                for j in range(n_dirs):
                    if j == j0 or comp[j, ki] < 1:
                        continue
                    sj = dsc[row, j]
                    rf += int(sj > own)
                    sh = comp[j, ki] / comp[j].sum()
                    rp += int(float(sj) + tau[base] * np.log(sh) > float(own) + tau[base] * np.log(sh0))
                bad[f"{base}+F"] += int(rf != ranks[f"{base}+F"][k])
                bad[f"{base}+P"] += int(rp != ranks[f"{base}+P"][k])
                best = {}
                if base == "a":
                    m = kind_means(V[keep], kinds_all[keep]).get(K)
                    own_t = np.float32((m @ q).max()) if m is not None else None
                    for j, d in enumerate(dir_list):
                        if j != j0 and K in means[d]:
                            best[j] = tsc[row, j]
                            assert tsc[row, j] == np.float32((means[d][K] @ q).max()) or \
                                abs(float(tsc[row, j]) - float((means[d][K] @ q).max())) < 1e-5
                else:
                    sel = rep_kinds(base, mods_all[keep]) == K
                    own_t = np.float32((Rk[sel] @ q).max()) if sel.any() else None
                    for i in np.where(allK == K)[0]:
                        j = int(owner[i])
                        if j != j0:
                            best[j] = max(best.get(j, np.float32(-np.inf)), S[row, i])
                rt = MISS if own_t is None else 1 + sum(1 for x in best.values() if x > own_t)
                bad[f"{base}_T"] += int(rt != ranks[f"{base}_T"][k])
        bad = Counter({r: n for r, n in bad.items() if n})
        out.append(f"Self-test on {len(sample)} evaluation queries (F, P and T ranks recomputed with plain loops "
                   f"from the same score rows): " +
                   ("all equal." if not bad else "DIFFERENCES " + ", ".join(f"{r} {n}" for r, n in sorted(bad.items()))))
        out.append("")
        if bad:
            print("\n".join(out))
            sys.exit(4)

    with open(os.path.join(emb_dir, f"ranks{args.tag}.jsonl"), "w") as fh:
        for k, g in enumerate(q_eval):
            row = {**g, "kind": qkind[k], "singleton": bool(single[k])}
            row.update({f"rank_{r}": int(ranks[r][k]) for r in ROWS + ROWS_T})
            row.update({f"rank_c+P{t}": int(epr[t]["c"][k]) for t in TAUS})
            fh.write(json.dumps(row) + "\n")

    # cells
    qb = np.array([g["image_frac_bucket"] for g in q_eval])
    qm = np.array([g["modality"] for g in q_eval])
    qd = np.array([g["relevant_dir"] for g in q_eval])
    primary, parts, majority, buckets = ev.s3_cells(qb, qm)
    main_cells = [("all", np.ones(len(q_eval), bool), 1), ("P1", primary[0][1], 50), ("P2", primary[1][1], 51),
                  ("M1", majority[0][1], 56), ("M2", majority[1][1], 57)]
    label_cells = [(m, qm == m, 20 + i) for i, m in enumerate(ev.MODALITIES)]
    grp = np.isin(qm, ev.IMAGE_INPUTS)
    group_cells = [("image inputs", grp, 90), ("text inputs", ~grp, 91)]
    cells = main_cells + label_cells + group_cells
    names = [n for n, _, _ in cells]

    def boot(sel, seed, rows, rk):
        cdirs = sorted(set(qd[sel]))
        rng = np.random.default_rng(seed)
        idx = rng.integers(0, len(cdirs), size=(ev.N_BOOT, len(cdirs)))
        res = {}
        for r in rows:
            hb = defaultdict(lambda: [0, 0])
            for d, x in zip(qd[sel], rk[r][sel]):
                hb[d][0] += int(x <= 5)
                hb[d][1] += 1
            res[r] = ev.boot(hb, cdirs, idx)
        return res, len(cdirs)

    def r_at(rk, r, sel, k=5):
        return float((rk[r][sel] <= k).mean()) if sel.any() else float("nan")

    def fmt(x):
        return "n/a" if x != x else f"{x:.3f}"

    def level_table(title, rows, mask, rk, k=5, cl=cells):
        out.append(f"### {args.label} {title}")
        out.append("")
        out.append("| row | " + " | ".join(f"{n} ({int((s & mask).sum())})" for n, s, _ in cl) + " |")
        out.append("|---|" + "---:|" * len(cl))
        for r in rows:
            out.append(f"| {r} | " + " | ".join(fmt(r_at(rk, r, s & mask, k)) for _, s, _ in cl) + " |")
        out.append("")

    verdict_ci = {}

    def diff_table(title, pairs, mask, rk, cl=cells):
        out.append(f"### {args.label} {title}")
        out.append("")
        out.append("| x - y | " + " | ".join(n for n, _, _ in cl) + " |")
        out.append("|---|" + "---|" * len(cl))
        rows = sorted({r for p in pairs for r in p})
        res = {}
        for n, s, seed in cl:
            if (s & mask).any():
                res[n] = boot(s & mask, seed, rows, rk)[0]
        for x, y in pairs:
            cols = []
            for n, s, seed in cl:
                if n not in res:
                    cols.append("n/a")
                    continue
                st = r_at(rk, x, s & mask) - r_at(rk, y, s & mask)
                lo, hi = np.percentile(res[n][x] - res[n][y], [2.5, 97.5])
                verdict_ci[(title, x, y, n)] = (st, lo, hi)
                cols.append(f"{st:+.3f} [{lo:+.3f}, {hi:+.3f}]")
            out.append(f"| {x} - {y} | " + " | ".join(cols) + " |")
        out.append("")

    allq = np.ones(len(q_eval), bool)
    ns = ~single
    # counts
    kind_dirs = {K: int((comp[:, KINDS.index(K)] >= 1).sum()) for K in KINDS}
    kind_vec = {K: int(sum(K in means[d] for d in dir_list)) for K in KINDS}
    out.append(f"Queries: {len(q_eval)} evaluation queries over {len(set(qd))} directories, {n_dirs} directories ranked; "
               f"{len(q_dev)} dev queries (calibration seed {args.calib_seed}). Singletons: {int(single.sum())}.")
    out.append("")
    out.append("| kind | directories holding it (composition) | directories with a vector of it | evaluation queries | "
               "singletons | mean directories ranked under x+F |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for K in KINDS:
        s = qkind == K
        if not s.any():
            continue
        nf = float(cand[s].sum(axis=1).mean())
        out.append(f"| {K} | {kind_dirs[K]} ({kind_dirs[K] / n_dirs:.3f}) | {kind_vec[K]} | {int(s.sum())} | "
                   f"{int((single & s).sum())} | {nf:.1f} |")
    out.append("")
    out.append("Singletons per cell: " + ", ".join(f"{n} {int((single & s).sum())} of {int(s.sum())}" for n, s, _ in cells) + ".")
    out.append("")
    out.append("Vectors per directory (stored): " + ", ".join(f"{r} {v:.2f}" for r, v in n_vec.items()) +
               "; x+F and x+P store what x stores, c_T and d_T what c and d store.")
    out.append("")

    # prior weight
    out.append(f"### {args.label} prior weight on the dev queries: recall@5 over all {len(q_dev)} dev queries")
    out.append("")
    out.append("| tau | " + " | ".join(f"{b}+P" for b in BASES) + " |")
    out.append("|---|" + "---:|" * len(BASES))
    out.append("| filter only (tau to 0) | " + " | ".join(fmt(dev_tab[b][0]) for b in BASES) + " |")
    for t in TAUS:
        out.append(f"| {t} | " + " | ".join(fmt(dev_tab[b][1][t]) + (" (selected)" if tau[b] == t else "") for b in BASES) + " |")
    out.append("")
    out.append("Selected: " + ", ".join(f"{b}+P tau {tau[b]}" for b in BASES) + ".")
    out.append("")

    level_table("all evaluation queries: recall@5 (queries per cell in parentheses)", ROWS, allq, ranks)
    diff_table("all evaluation queries: x - y in recall@5, paired 95% interval over directories",
               [("c+F", "a+F"), ("c", "a"), ("a+F", "a"), ("c+F", "c"), ("d+F", "d"), ("a+P", "a+F"),
                ("c+P", "c+F"), ("d+P", "d+F"), ("d+F", "c+F")], allq, ranks)
    level_table("non-singleton evaluation queries: recall@5", ROWS + ROWS_T, ns, ranks)
    diff_table("non-singleton evaluation queries: x - y in recall@5, paired 95% interval over directories",
               [("a_T", "c_T"), ("c_T", "d_T"), ("a_T", "d_T"), ("a_T", "a+F"), ("c_T", "c+F"), ("d_T", "d+F"),
                ("a_T", "c+F")], ns, ranks)
    level_table("singleton evaluation queries: recall@5 (x_T misses them by construction)", ROWS, single, ranks)
    for k in (1, 10):
        level_table(f"all evaluation queries: recall@{k}", ROWS, allq, ranks, k, main_cells)
        level_table(f"non-singleton evaluation queries: recall@{k}", ROWS + ROWS_T, ns, ranks, k, main_cells)
    prk = {f"c+P {t}": epr[t]["c"] for t in TAUS}
    prk["c+F"] = ranks["c+F"]
    level_table("c+P on the evaluation queries for every tau (descriptive; nothing is chosen here), recall@5",
                ["c+F"] + [f"c+P {t}" for t in TAUS], allq, prk, 5, main_cells)

    # verdicts
    T1 = "all evaluation queries: x - y in recall@5, paired 95% interval over directories"
    T2 = "non-singleton evaluation queries: x - y in recall@5, paired 95% interval over directories"
    v = [verdict_ci[(T1, "c+F", "a+F", n)] for n in ("P1", "P2")]
    a_ok = all(lo > 0 for _, lo, _ in v)
    out.append(f"H16a ({args.label}): c+F - a+F in P1 {v[0][0]:+.3f} [{v[0][1]:+.3f}, {v[0][2]:+.3f}], "
               f"in P2 {v[1][0]:+.3f} [{v[1][1]:+.3f}, {v[1][2]:+.3f}]; both intervals above zero: "
               f"{'yes, H16a survives' if a_ok else 'no, H16a is dead'} under {args.label}.")
    v = {n: verdict_ci[(T2, "a_T", "c_T", n)] for n in ("all", "P1", "P2", "M1", "M2")}
    b_dead = [n for n, (_, _, hi) in v.items() if hi < -0.02]
    out.append(f"H16b ({args.label}): a_T - c_T on the non-singleton queries " +
               ", ".join(f"{n} {s:+.3f} [{lo:+.3f}, {hi:+.3f}]" for n, (s, lo, hi) in v.items()) +
               f"; an interval entirely below -0.02: {'yes (' + ', '.join(b_dead) + '), H16b is dead' if b_dead else 'no, H16b survives'} under {args.label}.")
    v = [verdict_ci[(T1, "c+P", "c+F", n)] for n in ("P1", "P2")]
    c_ok = all(hi < 0 for _, _, hi in v)
    out.append(f"H16c ({args.label}, tau {tau['c']}): c+P - c+F in P1 {v[0][0]:+.3f} [{v[0][1]:+.3f}, {v[0][2]:+.3f}], "
               f"in P2 {v[1][0]:+.3f} [{v[1][1]:+.3f}, {v[1][2]:+.3f}]; both intervals below zero: "
               f"{'yes, H16c survives' if c_ok else 'no, H16c is dead'} under {args.label}.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
