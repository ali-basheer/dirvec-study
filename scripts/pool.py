#!/usr/bin/env python3
"""dirvec session 24: the two draws of GitHub directories pooled (BRIEF.md, session 24, "Pooled estimates").

  python3 scripts/pool.py                  the reproduction check on each draw, then the pooled table
  python3 scripts/pool.py --draws s19      the reproduction check on S19 alone (no pooled number)

Inputs, all in the repository (the pod pushes them; nothing is embedded or ranked here), for a draw d:
  data/ranks_<d>_e1.jsonl.gz           eval.py's per-query ranks under E1
  data/flags_<d>.jsonl.gz              s19.py's per-query flags (owner, names, sibling, folder size, c equals d)
  data/ranks_s21_<d>_e1.jsonl.gz       budget.py's per-query ranks under E1
  data/commitq_ranks_<d>_e1.jsonl.gz   the commit-subject queries' ranks under E1
  data/manifest_<d>.jsonl, data/dirs_<d>.jsonl
  data/notok_code_<d>_e1.txt           the code files of the draw that E1 did not embed, read from the cache
                                       index on the pod, so that a no-code folder is s19.py's (embedded files only)
and what s19.py and budget.py printed for the draw: results/session19_outputs.md and
results/session21_outputs.md for S19, results/session24_outputs.md and results/session24_budget_outputs.md
for S24.

Step 1, each draw alone: every row this script pools is recomputed from those files with the printing
script's own cells, estimator and seed, and the line is compared with the printed line, character for
character. One difference and the script stops (exit code 3) before any pooled number.

Step 2, the pooled table. For a test, the queries of both draws that fall in its cell; the mean over
owners of the owner's mean, an owner present in both draws counted once with all its queries (an owner
is the lowercased account name in both draws); percentile intervals from 10,000 resamples of owners
(s19.py's oboot), one seed per test, 24101 and up in the order of POOLED below; the reading its rule
gives, a primary test on its 98.33 percent interval and a secondary one on its 95 percent interval. The
pooled estimate is the size on this source and carries no verdict for H19a or H24a (BRIEF.md).
"""
import argparse
import gzip
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402
import budget as bg  # noqa: E402
import quant as qn  # noqa: E402
import s19  # noqa: E402
from validity import cells_of  # noqa: E402

ROOT = ev.ROOT
DIM_E1 = 2048                                    # jina-embeddings-v4; budget.py printed it for S19 E1
OUTPUTS = {"s19": ("results/session19_outputs.md", "results/session21_outputs.md"),
           "s24": ("results/session24_outputs.md", "results/session24_budget_outputs.md")}

# s19.py validity, the registered table (name, x, y, cell, seed, rule, primary), as s19.py lists it
S19_TESTS = [("H19a P1s: c - a", "c", "a", "P1s", 19001, "loss", True),
             ("H19a P2s: c - a", "c", "a", "P2s", 19002, "loss", True),
             ("H19c: c - d where c differs from d", "c", "d", "c differs", 19003, "margin", True),
             ("H19b P1s clean: c - a", "c", "a", "P1s clean", 19004, "loss", False),
             ("H19b P2s clean: c - a", "c", "a", "P2s clean", 19005, "loss", False),
             ("no-code folders, P1s: c - a", "c", "a", "P1s no code", 19006, "loss", False),
             ("no-code folders, P2s: c - a", "c", "a", "P2s no code", 19007, "loss", False),
             ("all of P1 (lone images included): c - a", "c", "a", "P1", 19008, "loss", False),
             ("all of P2 (lone texts included): c - a", "c", "a", "P2", 19009, "loss", False),
             ("cs - d where c differs from d", "cs", "d", "c differs", 19010, "margin", False)]
# budget.py --registered at 2,048 bytes (test, x, y, cell, seed, rule); seed = budget.py's bseed(bi, ci, pi)
REG_B = 2048
BUDGETS = [512, 1024, 2048, 4096, 8192]
PAIRS = [("sample", "mean"), ("kmeans", "mean"), ("sample", "kmeans"), ("sample", "usample")]
DCELLS = ["all", "minority", "all, not whole", "minority, not whole"]
BUDGET_TESTS = [("H21a", "sample", "mean", "minority, not whole", "loss"),
                ("H21b", "sample", "kmeans", "all, not whole", "margin"),
                ("H21c", "sample", "usample", "minority, not whole", "kinds")]
# the pooled table: (label, source, key, primary)
POOLED = [("H24a P1s: c - a (pools H19a P1s)", "s19", "H19a P1s: c - a", True),
          ("H24a P2s: c - a (pools H19a P2s)", "s19", "H19a P2s: c - a", True),
          ("H24c: c - d where c differs from d (pools H19c)", "s19", "H19c: c - d where c differs from d", True),
          ("H24b P1s clean: c - a", "s19", "H19b P1s clean: c - a", False),
          ("H24b P2s clean: c - a", "s19", "H19b P2s clean: c - a", False),
          ("no-code folders, P1s: c - a", "s19", "no-code folders, P1s: c - a", False),
          ("no-code folders, P2s: c - a", "s19", "no-code folders, P2s: c - a", False),
          ("all of P1: c - a", "s19", "all of P1 (lone images included): c - a", False),
          ("all of P2: c - a", "s19", "all of P2 (lone texts included): c - a", False),
          ("cs - d where c differs from d", "s19", "cs - d where c differs from d", False),
          ("H24d: commit subjects, image-heavy directories, c - a (pools H19d)", "cq", "H19d", False),
          ("H24e and H21a: sample - mean, minority, not whole (2 KiB)", "budget", "H21a", True),
          ("H24f and H21b: sample - kmeans, all, not whole (2 KiB)", "budget", "H21b", True),
          ("H24g and H21c: sample - usample, minority, not whole (2 KiB)", "budget", "H21c", True)]


def jl(path):
    p = os.path.join(ROOT, path)
    with (gzip.open(p, "rt") if p.endswith(".gz") else open(p)) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def read_s19(lo, hi, no, rule):
    """s19.py's reading of one interval."""
    if rule == "loss":
        return s19.outcome(lo, hi, no)
    if no < s19.MIN_OWNERS:
        return f"inconclusive (fewer than {s19.MIN_OWNERS} owners)"
    return ("not inferior (lower bound at or above -0.02)" if lo >= -s19.MARGIN else
            "inferior (upper bound under -0.02)" if hi < -s19.MARGIN else "inconclusive")


def read_budget(rule, lo, hi, no):
    """budget.py's reading(kind, lo, hi, no)."""
    if no < bg.MIN_OWNERS:
        return f"inconclusive (fewer than {bg.MIN_OWNERS} owners)"
    if rule == "loss":
        return ("confirmed (lower bound at or above +0.05)" if lo >= bg.SESOI else
                "below +0.05 (upper bound under +0.05)" if hi < bg.SESOI else
                "present, size open (lower bound above zero)" if lo > 0 else "inconclusive")
    if rule == "margin":
        return ("not inferior (lower bound at or above -0.02)" if lo >= -bg.MARGIN else
                "inferior (upper bound under -0.02)" if hi < -bg.MARGIN else "inconclusive")
    return ("the kinds matter (lower bound above zero)" if lo > 0 else
            "the uniform sample is better (upper bound below zero)" if hi < 0 else
            "no difference at the margin (interval within -0.02 and +0.02)" if lo >= -bg.MARGIN and hi <= bg.MARGIN
            else "inconclusive")


class Draw:
    """One draw's per-query differences, cells and owners, rebuilt from the pushed files."""

    def __init__(self, d):
        self.d = d
        self.z = {}           # key -> (z over the cell's queries, owners of those queries, rule)
        self.lines = []       # (what, recomputed line, found in the printed output)
        printed_v, printed_b = (open(os.path.join(ROOT, p)).read() for p in OUTPUTS[d])

        # ---- s19.py validity (E1 decides; on S19 every query is shared by E1, E4 and E2)
        R = jl(f"data/ranks_{d}_e1.jsonl.gz")
        F = {r["query_path"]: r for r in jl(f"data/flags_{d}.jsonl.gz")}
        if len(F) != len(R) or any(g["query_path"] not in F for g in R):
            sys.exit(f"{d}: the flags and the eval.py ranks are not the same queries")
        fl = [F[g["query_path"]] for g in R]
        qm = np.array([g["modality"] for g in R])
        qb = np.array([g["image_frac_bucket"] for g in R])
        qd = np.array([g["relevant_dir"] for g in R])
        qo = np.array([f["owner"] for f in fl])
        cells = cells_of(qm, qb)
        has_sib = np.array([f["sib_same"] >= 1 for f in fl])
        sib = np.array([bool(f["sibling"]) for f in fl])
        missed = np.array([f["name_rank_d"] > 5 and f["name_rank_a"] > 5 for f in fl])
        clean = missed & ~sib
        c_is_d = np.array([bool(f["c_is_d"]) for f in fl])
        manifest = jl(f"data/manifest_{d}.jsonl")
        notok = set(open(os.path.join(ROOT, f"data/notok_code_{d}_e1.txt")).read().split())
        code_dirs = {r["dir"] for r in manifest
                     if r["path"] not in notok and s19.kind_of(r["path"], r["modality"]) == "code"}
        nocode = np.array([x not in code_dirs for x in qd])
        H = {r: np.array([g[f"rank_{r}"] <= 5 for g in R], float) for r in ("a", "c", "d", "cs") if f"rank_{r}" in R[0]}
        P1s, P2s = cells["P1"] & has_sib, cells["P2"] & has_sib
        mask = {"P1s": P1s, "P2s": P2s, "c differs": ~c_is_d, "P1s clean": P1s & clean, "P2s clean": P2s & clean,
                "P1s no code": P1s & nocode, "P2s no code": P2s & nocode, "P1": cells["P1"], "P2": cells["P2"]}
        for name, x, y, cell, seed, rule, primary in S19_TESTS:
            s = mask[cell]
            if x not in H or y not in H or s.sum() < 2 or len(set(qo[s])) < 2:
                self.lines.append((name, f"(no test: {int(s.sum())} queries)", None))
                continue
            zz = H[x][s] - H[y][s]
            pt, i95, i98, no = s19.oboot(zz, qo[s], seed)
            lo, hi = i98 if primary else i95
            line = (f"| E1 | {name}{' (primary)' if primary else ''} | {int(s.sum())} | {no} | {pt:+.3f} | "
                    f"[{i95[0]:+.3f}, {i95[1]:+.3f}] | [{i98[0]:+.3f}, {i98[1]:+.3f}] | {read_s19(lo, hi, no, rule)} |")
            self.lines.append((name, line, line in printed_v))
            self.z[name] = (zz, qo[s], rule)

        # ---- the commit-subject queries (H19d on this draw)
        dirs = {r["dir"]: r for r in jl(f"data/dirs_{d}.jsonl")}
        cq_path = f"data/commitq_ranks_{d}_e1.jsonl.gz"
        if os.path.exists(os.path.join(ROOT, cq_path)):
            Q = jl(cq_path)
            cqo = np.array([dirs[g["relevant_dir"]].get("owner") or f"record:{dirs[g['relevant_dir']]['record']}" for g in Q])
            hi_ = np.isin(np.array([g["image_frac_bucket"] for g in Q]), s19.HI_B)
            rk = {r: np.array([g[f"rank_{r}"] for g in Q]) for r in ("a", "c", "d")}
            nr = np.array([g["name_rank"] for g in Q])
            d5, n5 = float((rk["d"][hi_] <= 5).mean()), float((nr[hi_] <= 5).mean())
            zz = (rk["c"][hi_] <= 5).astype(float) - (rk["a"][hi_] <= 5).astype(float)
            pt, i95, _, no = s19.oboot(zz, cqo[hi_], 19030)
            gate = d5 >= s19.CQ_GATE and d5 > n5
            read = s19.outcome(i95[0], i95[1], no) if gate else "untestable (the gate failed)"
            line = (f"H19d statistic (E1): image-heavy directories, {int(hi_.sum())} queries from {no} owners; gate, "
                    f"recall@5 of d {d5:.3f} (needs {s19.CQ_GATE:.2f} and more than names alone, {n5:.3f}): "
                    f"{'passed' if gate else 'failed'}; owner-weighted c - a {pt:+.3f} [{i95[0]:+.3f}, {i95[1]:+.3f}]; "
                    f"H19d: {read}.")
            self.lines.append(("H19d", line, line in printed_v))
            self.z["H19d"] = (zz, cqo[hi_], "loss")
            self.cq = (rk["d"][hi_] <= 5, nr[hi_] <= 5, cqo[hi_])
        else:
            self.lines.append(("H19d", f"(no {cq_path}: the commit-subject queries did not run on this draw)", None))
            self.cq = None

        # ---- budget.py --registered at 2,048 bytes
        BR = jl(f"data/ranks_s21_{d}_e1.jsonl.gz")
        G = {g["query_path"]: g for g in R}
        if any(b["query_path"] not in G for b in BR) or len(BR) != len(R):
            sys.exit(f"{d}: budget.py's queries are not eval.py's")
        bm = np.array([G[b["query_path"]]["modality"] for b in BR])
        bb = np.array([G[b["query_path"]]["image_frac_bucket"] for b in BR])
        bd = np.array([b["relevant_dir"] for b in BR])
        bo = np.array([dirs[x]["owner"] for x in bd])
        primary, _, _, _ = ev.s3_cells(bb, bm)
        bsib = np.array([F[b["query_path"]]["sib_same"] >= 1 for b in BR])
        nd = np.array([F[b["query_path"]]["n_dir"] for b in BR])
        mino = (primary[0][1] & bsib) | (primary[1][1] & bsib)
        partial = (nd - 1) > (REG_B // qn.vec_bytes("bin", DIM_E1))
        dc = {"all": np.ones(len(BR), bool), "minority": mino, "all, not whole": partial, "minority, not whole": mino & partial}
        for h, x, y, cell, rule in BUDGET_TESTS:
            seed = 21000 + 1000 * BUDGETS.index(REG_B) + 20 * DCELLS.index(cell) + PAIRS.index((x, y))
            hx = np.array([b[f"rank_{x}@{REG_B}"] <= 5 for b in BR], float)
            hy = np.array([b[f"rank_{y}@{REG_B}"] <= 5 for b in BR], float)
            s = dc[cell]
            zz = hx[s] - hy[s]
            pt, i95, i98, no = bg.oboot(zz, bo[s], seed)
            line = (f"| {h} (primary): {x} - {y}, {cell} | {int(s.sum())} | {no} | {pt:+.3f} | "
                    f"[{i95[0]:+.3f}, {i95[1]:+.3f}] | [{i98[0]:+.3f}, {i98[1]:+.3f}] | {read_budget(rule, i98[0], i98[1], no)} |")
            self.lines.append((h, line, line in printed_b))
            self.z[h] = (zz, bo[s], rule)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draws", default="s19,s24")
    args = ap.parse_args()
    names = args.draws.split(",")
    out = ["# Session 24: the two draws of GitHub directories pooled (scripts/pool.py)", ""]
    draws = [Draw(d) for d in names]
    out.append("## Step 1: each draw alone, recomputed from the per-query files and compared with the printed lines")
    out.append("")
    bad = []
    for D in draws:
        for what, line, found in D.lines:
            tag = "same" if found else ("DIFFERENT" if found is False else "not run")
            out.append(f"- {D.d.upper()} {what}: {tag}")
            out.append(f"  `{line}`")
            if found is False:
                bad.append((D.d, what))
    out.append("")
    if bad:
        out.append(f"NOT REPRODUCED: {bad}. Stopping before any pooled number.")
        print("\n".join(out))
        sys.exit(3)
    out.append("Reproduced: every line above is the line s19.py or budget.py printed.")
    out.append("")
    if len(draws) < 2:
        print("\n".join(out))
        return

    A, B = draws
    out.append(f"## Step 2: pooled over {A.d.upper()} and {B.d.upper()} (owner-weighted mean, 10,000 resamples of owners; "
               "a primary test is read on its 98.33 percent interval, a secondary one on its 95 percent interval)")
    out.append("")
    out.append("| test | primary | " + " | ".join(f"{D.d.upper()} queries, owners, point" for D in draws) +
               " | pooled queries | pooled owners (in both) | pooled point | 95% | 98.33% | reading |")
    out.append("|---|---|" + "---|" * len(draws) + "---:|---|---:|---|---|---|")
    for k, (label, src, key, primary) in enumerate(POOLED):
        seed = 24101 + k
        parts = [D.z.get(key) for D in draws]
        if any(p is None for p in parts):
            out.append(f"| {label} | {'yes' if primary else 'no'} | " + " | ".join(
                "(no test)" if p is None else f"{len(p[0])}, {len(set(p[1]))}, {p[0].mean():+.3f}" for p in parts) +
                " | | | | | | not pooled (a draw has no test) |")
            continue
        rule = parts[0][2]
        z = np.concatenate([p[0] for p in parts])
        o = np.concatenate([p[1] for p in parts])
        both = len(set(parts[0][1]) & set(parts[1][1]))
        pt, i95, i98, no = s19.oboot(z, o, seed)
        lo, hi = i98 if primary else i95
        if src == "budget":
            read = read_budget(rule, lo, hi, no)
        elif src == "cq":
            dd = np.concatenate([D.cq[0] for D in draws])
            nn = np.concatenate([D.cq[1] for D in draws])
            gate = dd.mean() >= s19.CQ_GATE and dd.mean() > nn.mean()
            read = (s19.outcome(lo, hi, no) if gate else "untestable (the gate failed)") + \
                f"; gate: recall@5 of d {dd.mean():.3f}, names alone {nn.mean():.3f}"
        else:
            read = read_s19(lo, hi, no, rule)
        cols = []
        for D, p in zip(draws, parts):
            gm = np.array([p[0][p[1] == u].mean() for u in sorted(set(p[1]))]).mean()
            cols.append(f"{len(p[0])}, {len(set(p[1]))}, {gm:+.3f}")
        out.append(f"| {label} | {'yes' if primary else 'no'} | " + " | ".join(cols) +
                   f" | {len(z)} | {no} ({both}) | {pt:+.3f} | [{i95[0]:+.3f}, {i95[1]:+.3f}] | "
                   f"[{i98[0]:+.3f}, {i98[1]:+.3f}] | {read} |")
    out.append("")
    out.append("The per-draw points are the owner-weighted means printed in step 1; the pooled reading is the size on this "
               "source and is no verdict for H19a or H24a. For H21a, H21b and H21c a cell with fewer than 100 owners on a "
               "single draw takes the pooled reading (BRIEF.md, session 24).")
    print("\n".join(out))


if __name__ == "__main__":
    main()
