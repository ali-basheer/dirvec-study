#!/usr/bin/env python3
"""Cross-encoder paired comparison of the minority loss (session 15, H15c).

Input: eval.py rank files (data/emb/<emb>/ranks<tag>.jsonl) of several encoders over the same
queries (the S11 evaluation split, calibration seed 20261102). For a pair X-Y and a cell the
statistic is

    [(c - a) under X] minus [(c - a) under Y], recall@5,

with a 95 percent interval from 1000 resamples of the cell's directories; both encoders see the
same resampled directories and queries, so the interval is paired. Cells and seeds are eval.py's
(--criterion s3): P1 image queries in [0,.2)+[.2,.5) (seed 50), P2 text-like queries in
[.5,.8)+[.8,1] (seed 51), M1 image queries in [.5,.8)+[.8,1] (seed 56), M2 text-like queries in
[0,.2)+[.2,.5) (seed 57); "all" uses seed 49. With the same seed and the same directories the
per-encoder c - a interval printed here is eval.py's own, which checks this script against it.

Usage: python scripts/xenc.py E1=data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl \
           E4=data/emb/nomic-embed-v1.5_s11/ranks_s15_e4.jsonl --pairs E4-E1
"""
import argparse
import json
from collections import defaultdict

import numpy as np

BUCKETS = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]
TEXTLIKE = ["text", "table", "pdf_text", "other"]
N_BOOT = 1000


def load(path):
    with open(path) as fh:
        return [json.loads(l) for l in fh]


def cells(qb, qm):
    textlike = np.isin(qm, TEXTLIKE)
    return [
        ("all", np.ones(len(qb), bool), 49),
        ("P1 image in [0,.2)+[.2,.5)", (qm == "image") & np.isin(qb, BUCKETS[:2]), 50),
        ("P2 textlike in [.5,.8)+[.8,1]", textlike & np.isin(qb, BUCKETS[2:]), 51),
        ("M1 image in [.5,.8)+[.8,1]", (qm == "image") & np.isin(qb, BUCKETS[2:]), 56),
        ("M2 textlike in [0,.2)+[.2,.5)", textlike & np.isin(qb, BUCKETS[:2]), 57),
    ]


def boot_loss(qd, sel, ranks_c, ranks_a, idx, cdirs):
    """Resampled recall@5 of c minus a for one encoder, over the given directory resamples."""
    pos = {d: i for i, d in enumerate(cdirs)}
    h = np.zeros((len(cdirs), 2))
    n = np.zeros(len(cdirs))
    for d, rc, ra in zip(qd[sel], ranks_c[sel], ranks_a[sel]):
        j = pos[d]
        h[j, 0] += rc <= 5
        h[j, 1] += ra <= 5
        n[j] += 1
    tot = n[idx].sum(axis=1)
    return h[:, 0][idx].sum(axis=1) / tot - h[:, 1][idx].sum(axis=1) / tot, (h[:, 0].sum() - h[:, 1].sum()) / n.sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="NAME=path to an eval.py rank file")
    ap.add_argument("--pairs", required=True, help="comma-separated X-Y pairs of NAMEs")
    args = ap.parse_args()
    data = {}
    for spec in args.files:
        name, path = spec.split("=", 1)
        data[name] = load(path)
    names = list(data)
    ref = data[names[0]]
    for name in names[1:]:
        other = data[name]
        assert len(other) == len(ref), f"{name}: {len(other)} queries, {names[0]}: {len(ref)}"
        for a, b in zip(ref, other):
            assert (a["query_path"], a["relevant_dir"], a["modality"], a["image_frac_bucket"]) == \
                   (b["query_path"], b["relevant_dir"], b["modality"], b["image_frac_bucket"]), \
                f"query lists differ at {a['query_path']} / {b['query_path']}"
    qd = np.array([g["relevant_dir"] for g in ref])
    qb = np.array([g["image_frac_bucket"] for g in ref])
    qm = np.array([g["modality"] for g in ref])
    rk = {name: {rep: np.array([g[f"rank_{rep}"] for g in rows]) for rep in ("a", "c")} for name, rows in data.items()}

    print(f"Queries: {len(ref)} over {len(set(qd))} directories, identical in the {len(names)} rank files "
          f"({', '.join(names)}). Recall@5; 95 percent intervals from {N_BOOT} resamples of each cell's directories.")
    print()
    print("### c - a per encoder (must equal eval.py's c-a interval for the primary and majority cells)")
    print()
    print("| encoder | cell | queries | dirs | c - a | 95% CI |")
    print("|---|---|---:|---:|---:|---|")
    boots = {}
    for cname, sel, seed in cells(qb, qm):
        cdirs = sorted(set(qd[sel]))
        idx = np.random.default_rng(seed).integers(0, len(cdirs), size=(N_BOOT, len(cdirs)))
        for name in names:
            b, point = boot_loss(qd, sel, rk[name]["c"], rk[name]["a"], idx, cdirs)
            boots[(name, cname)] = (b, point)
            lo, hi = np.percentile(b, [2.5, 97.5])
            print(f"| {name} | {cname} | {int(sel.sum())} | {len(cdirs)} | {point:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
    print()
    print("### Paired difference of the loss between encoders: (c - a) under X minus (c - a) under Y")
    print()
    print("| X - Y | cell | (c - a) X | (c - a) Y | difference | 95% CI | interval above zero |")
    print("|---|---|---:|---:|---:|---|---|")
    for pair in args.pairs.split(","):
        x, y = pair.split("-")
        for cname, sel, seed in cells(qb, qm):
            bx, px = boots[(x, cname)]
            by, py = boots[(y, cname)]
            lo, hi = np.percentile(bx - by, [2.5, 97.5])
            print(f"| {x} - {y} | {cname} | {px:+.3f} | {py:+.3f} | {px - py:+.3f} | [{lo:+.3f}, {hi:+.3f}] | "
                  f"{'yes' if lo > 0 else 'no'} |")


if __name__ == "__main__":
    main()
