#!/usr/bin/env python3
"""Self-test for eval.py's ranking: rows that are the same vector by construction must rank the same.

Session 9 defines u_p1 as a, c_p1 as ac, u_p0 as ab and c_p0 as acb (BRIEF.md, session 9, F1). Before
the session 13 correction the weighted-pooling builder returned float64 vectors, the query's own
directory score was rounded into a float32 score row and compared against its unrounded self, and
the own directory outranked itself in about half the queries: every F1 and F2 row lost about half
its recall@1 and 0.006 to 0.013 recall@5. This test builds a small synthetic corpus with a modality
gap, runs eval.py end to end on it (no cache, no GPU, under a minute) and fails unless

  1. every build() base returns float32 for float32 input, and
  2. the four identities above hold: the same ranks on at least 99 percent of the queries (the two
     builders sum in a different order, so a tie can break differently) and recall@1, @5 and @10
     within 0.01.

Usage: python scripts/selftest_ranks.py [path to an eval.py to test, default the one next to it]
"""
import importlib.util
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("u_p1", "a"), ("c_p1", "ac"), ("u_p0", "ab"), ("c_p0", "acb")]


def synth(root, n_dirs=120, d=64, seed=7):
    """A corpus with two input groups offset by a gap, topic vectors per directory and a minority
    group in most directories. Files of one directory share its topic; images share an offset."""
    rng = np.random.default_rng(seed)
    gap = rng.normal(size=d)
    gap /= np.linalg.norm(gap)
    manifest, vecs, dirs, gt = [], [], [], []
    for j in range(n_dirs):
        name = f"dir{j:04d}"
        n = int(rng.integers(5, 13))
        n_img = int(rng.integers(1, n))               # at least one file of each group
        topic = rng.normal(size=d)
        topic /= np.linalg.norm(topic)
        frac = n_img / n
        for i in range(n):
            img = i < n_img
            v = topic + (0.9 * gap if img else -0.9 * gap) + 0.6 * rng.normal(size=d) / np.sqrt(d) * 3
            path = f"{name}/f{i:02d}.{'png' if img else 'txt'}"
            manifest.append({"path": path, "dir": name, "modality": "image" if img else "text"})
            vecs.append(v / np.linalg.norm(v))
        dirs.append({"dir": name, "n_files": n, "image_frac": frac})
    V = np.array(vecs, np.float32)
    data = os.path.join(root, "data")
    emb = os.path.join(data, "emb", "synth")
    os.makedirs(emb)
    np.save(os.path.join(emb, "vectors.npy"), V)
    by_dir = {r["dir"]: r for r in dirs}

    def bucket(f):
        return "[0,.2)" if f < 0.2 else "[.2,.5)" if f < 0.5 else "[.5,.8)" if f < 0.8 else "[.8,1]"

    with open(os.path.join(emb, "index.jsonl"), "w") as fh:
        for r in manifest:
            fh.write(json.dumps({"path": r["path"], "modality": r["modality"], "ok": True, "done": True}) + "\n")
    for fn, rows in (("manifest_t.jsonl", manifest), ("dirs_t.jsonl", dirs)):
        with open(os.path.join(data, fn), "w") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
    with open(os.path.join(data, "gt_t.jsonl"), "w") as fh:
        for r in manifest:
            fh.write(json.dumps({"query_path": r["path"], "relevant_dir": r["dir"], "modality": r["modality"],
                                 "image_frac_bucket": bucket(by_dir[r["dir"]]["image_frac"])}) + "\n")
    return emb


def main():
    target = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "eval.py")
    spec = importlib.util.spec_from_file_location("eval_under_test", target)
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    failures = []

    # 1. dtypes of every builder
    rng = np.random.default_rng(0)
    X = rng.normal(size=(9, 16)).astype(np.float32)
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    mods = np.array(["image"] * 4 + ["text"] * 3 + ["table"] * 2)
    for base, param in [("a", None), ("b", None), ("c", None), ("c4", None), ("c2", None), ("d", None), ("ab", None),
                        ("p", 0.0), ("p", 0.5), ("p", 1.0), ("b2", None), ("f4", 0.5), ("tb", "2"), ("tb", "g"), ("tb", "c")]:
        R = ev.build(base, X, mods, param)
        line = f"build({base!r}, param={param!r}): dtype {R.dtype}"
        if R.dtype != np.float32:
            failures.append(line)
            line += "   <-- not float32"
        print(line)

    # 2. the identities, end to end
    with tempfile.TemporaryDirectory() as root:
        emb = synth(root)
        ev.ROOT, ev.DATA = root, os.path.join(root, "data")
        reps = "a,c,d,ac,ab,acb,cc,dc," + ",".join(x for x, _ in PAIRS)
        argv = sys.argv
        sys.argv = ["eval.py", "--model", "synth", "--emb", "synth", "--manifest", "data/manifest_t.jsonl",
                    "--dirs", "data/dirs_t.jsonl", "--gt", "data/gt_t.jsonl", "--criterion", "s3",
                    "--calib", "0.2", "--reps", reps, "--tag", "_selftest"]
        try:
            with redirect_stdout(io.StringIO()):
                ev.main()
        finally:
            sys.argv = argv
        with open(os.path.join(emb, "ranks_selftest.jsonl")) as fh:
            rows = [json.loads(l) for l in fh]
    print(f"\n{len(rows)} synthetic queries")
    print("| pair | same rank | R@1 | R@5 | R@10 |")
    print("|---|---:|---|---|---|")
    for x, y in PAIRS:
        rx = np.array([r[f"rank_{x}"] for r in rows])
        ry = np.array([r[f"rank_{y}"] for r in rows])
        same = float((rx == ry).mean())
        rec = [(float((rx <= k).mean()), float((ry <= k).mean())) for k in (1, 5, 10)]
        print(f"| {x} against {y} | {same:.3f} | " + " | ".join(f"{a:.3f} against {b:.3f}" for a, b in rec) + " |")
        if same < 0.99 or any(abs(a - b) > 0.01 for a, b in rec):
            failures.append(f"{x} is not {y}: same rank on {same:.3f} of the queries, recall {rec}")
    if failures:
        print("\nFAIL")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print("\nOK: every builder returns float32 and the four identities hold.")


if __name__ == "__main__":
    main()
