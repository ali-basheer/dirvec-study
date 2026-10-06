#!/usr/bin/env python3
"""Session 13 rank checks: the corrected rerun of session 9 against the session 9 rank files.

Reads data/emb/<emb>/ranks_s9{dev,devcv,test}.jsonl (session 9, written before the ranking fix) and
ranks_s13{dev,devcv,test}.jsonl (this session) and prints, as markdown:

  C2  reproduction: for every row that does not use the weighted-pooling builder (every name without
      "_p"), the share of queries whose rank is identical in the old and the new file. The brief
      requires 1.000 for all of them.
  C3  identity: in the new files, u_p1 against a, c_p1 against ac, u_p0 against ab, c_p0 against acb:
      share of queries with the same rank, and recall@1, @5, @10 of both.
  How far each weighted-pooling row moved: recall@5 before and after, over all queries and in the
      four cells, and the share of queries whose rank dropped by exactly one.

No number here is a result of the study; the tables of record are eval.py's own outputs.
"""
import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTLIKE = {"text", "table", "pdf_text", "other"}
LOW, HIGH = {"[0,.2)", "[.2,.5)"}, {"[.5,.8)", "[.8,1]"}
IDENT = [("u_p1", "a"), ("c_p1", "ac"), ("u_p0", "ab"), ("c_p0", "acb")]


def load(path):
    with open(path) as fh:
        rows = [json.loads(l) for l in fh]
    reps = [k[5:] for k in rows[0] if k.startswith("rank_")]
    return rows, reps


def cells(rows):
    mod = np.array([r["modality"] for r in rows])
    b = np.array([r["image_frac_bucket"] for r in rows])
    img = mod == "image"
    txt = np.isin(mod, list(TEXTLIKE))
    lo, hi = np.isin(b, list(LOW)), np.isin(b, list(HIGH))
    return [("all", np.ones(len(rows), bool)), ("P1", img & lo), ("P2", txt & hi), ("M1", img & hi), ("M2", txt & lo)]


def col(rows, rep):
    return np.array([r[f"rank_{rep}"] for r in rows])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emb", default="jina-embeddings-v4_s5")
    args = ap.parse_args()
    emb = os.path.join(ROOT, "data", "emb", args.emb)
    ok = True
    for split in ("dev", "devcv", "test"):
        old_p, new_p = os.path.join(emb, f"ranks_s9{split}.jsonl"), os.path.join(emb, f"ranks_s13{split}.jsonl")
        if not os.path.exists(new_p):
            print(f"\n## {split}: {new_p} missing")
            ok = False
            continue
        new, new_reps = load(new_p)
        print(f"\n## {split}: {len(new)} queries, {len(new_reps)} rows in the session 13 file")
        cs = cells(new)
        if os.path.exists(old_p):
            old, old_reps = load(old_p)
            same_q = len(old) == len(new) and all(a["query_path"] == b["query_path"] for a, b in zip(old, new))
            print(f"\nSession 9 file: {len(old)} queries, {len(old_reps)} rows; same queries in the same order: {'yes' if same_q else 'NO'}.")
            if not same_q:
                ok = False
            else:
                common = [r for r in new_reps if r in old_reps]
                print("\n### C2 reproduction: rows that do not use the weighted-pooling builder\n")
                print("| row | identical rank | max abs rank change |")
                print("|---|---:|---:|")
                for r in common:
                    if "_p" in r:
                        continue
                    a, b = col(old, r), col(new, r)
                    share = float((a == b).mean())
                    print(f"| {r} | {share:.4f} | {int(np.abs(a - b).max())} |")
                    if share < 1.0:
                        ok = False
                print("\n### Weighted-pooling rows: recall@5 in the session 9 file and in the session 13 file\n")
                print("| row | rank lower by exactly 1 | rank unchanged | other | " +
                      " | ".join(f"{n} before | {n} after" for n, _ in cs) + " | R@1 all before | R@1 all after |")
                print("|---|---:|---:|---:|" + "---:|---:|" * len(cs) + "---:|---:|")
                for r in common:
                    if "_p" not in r:
                        continue
                    a, b = col(old, r), col(new, r)
                    d = a - b
                    cols = " | ".join(f"{(a[s] <= 5).mean():.3f} | {(b[s] <= 5).mean():.3f}" for _, s in cs)
                    print(f"| {r} | {(d == 1).mean():.3f} | {(d == 0).mean():.3f} | {((d != 0) & (d != 1)).mean():.3f} | "
                          f"{cols} | {(a <= 1).mean():.3f} | {(b <= 1).mean():.3f} |")
        else:
            print(f"\nSession 9 file {old_p} not found: no reproduction check for this split.")
            ok = False
        print("\n### C3 identity in the session 13 file\n")
        print("| pair | same rank | R@1 | R@5 | R@10 | largest recall@5 gap over the five cells |")
        print("|---|---:|---|---|---|---:|")
        for x, y in IDENT:
            if x not in new_reps or y not in new_reps:
                print(f"| {x} against {y} | not in this run | | | | |")
                continue
            a, b = col(new, x), col(new, y)
            same = float((a == b).mean())
            gap = max(abs(float((a[s] <= 5).mean() - (b[s] <= 5).mean())) for _, s in cs if s.any())
            rec = " | ".join(f"{(a <= k).mean():.3f} against {(b <= k).mean():.3f}" for k in (1, 5, 10))
            print(f"| {x} against {y} | {same:.4f} | {rec} | {gap:.4f} |")
            if same < 0.99 or gap > 0.001:
                ok = False
    print("\nChecks " + ("PASS: C2 identical on every unaffected row, C3 within tolerance." if ok else
                         "FAIL: see the tables above."))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
