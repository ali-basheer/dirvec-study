#!/usr/bin/env python3
"""Session 12: natural-language queries against folder representations.

Query = the Zenodo record's title (set Q_title), or the title followed by the record description
(set Q_desc, records with a fetched description only); relevant = the record's own directory.
The query is not a file, so every directory representation is built from all of the directory's
embedded files (no leave-one-out) and every directory with at least one embedded file is both a
candidate and a query. Centered rows center the query with mu_txt of the calibration split (the
query is a text input); nothing is fitted on the queries.

  embed: python scripts/descq.py embed --model jina-embeddings-v4 --emb jina-embeddings-v4_s11
  eval:  python scripts/descq.py eval  --model jina-embeddings-v4 --emb jina-embeddings-v4_s11 > out.md
"""
import argparse, gzip, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402

BUCKETS = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]
ROWS = ["a", "ac", "c", "cc", "d", "dc", "bc2", "tb2", "tb2c"]
KS = [1, 5, 10]


def load_jsonl(path):
    with open(path) as fh:
        return [json.loads(l) for l in fh]


def load_queries(dirs):
    """{dir: (title, description or '')} from the pool snapshot and the fetched descriptions."""
    titles = {}
    with gzip.open(os.path.join(ev.DATA, "pool_s11.jsonl.gz"), "rt") as fh:
        for line in fh:
            r = json.loads(line)
            titles[int(r["id"])] = r.get("title", "")
    desc = {}
    p = os.path.join(ev.DATA, "desc_s11.jsonl")
    if os.path.exists(p):
        for r in load_jsonl(p):
            if r.get("status") == 200:
                if not titles.get(int(r["id"])) and r.get("title"):
                    titles[int(r["id"])] = r["title"]
                desc[int(r["id"])] = r.get("description", "")
    out = {}
    for d, row in dirs.items():
        rid = int(row["record"])
        t = titles.get(rid, "")
        out[d] = (t, desc.get(rid, ""))
    return out


def query_texts(qmap, dir_list, which):
    texts, keep = [], []
    for d in dir_list:
        t, de = qmap[d]
        if which == "title":
            if t.strip():
                texts.append(t.strip()); keep.append(d)
        else:
            if t.strip() and de.strip():
                texts.append(t.strip() + ". " + de.strip()); keep.append(d)
    return texts, keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["embed", "eval"])
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", required=True)
    ap.add_argument("--manifest", default="data/manifest_s11.jsonl")
    ap.add_argument("--dirs", default="data/dirs_s11.jsonl")
    ap.add_argument("--calib", type=float, default=0.2)
    ap.add_argument("--calib-seed", type=int, default=20261102)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--dump-ranks", default=None,
                    help="session 17: also write the per-query ranks of every row to this jsonl path "
                         "(one line per query set and directory); changes no number")
    args = ap.parse_args()

    manifest = load_jsonl(os.path.join(ev.ROOT, args.manifest))
    dirs = {r["dir"]: r for r in load_jsonl(os.path.join(ev.ROOT, args.dirs))}
    emb_dir = os.path.join(ev.DATA, "emb", args.emb)
    index = load_jsonl(os.path.join(emb_dir, "index.jsonl"))
    ok = np.array([bool(r.get("ok")) for r in index])
    assert len(index) == len(manifest), "cache and manifest differ in length"
    assert all(a["path"] == b["path"] for a, b in zip(index, manifest)), "cache order differs from manifest"
    mods_all = np.array([r["modality"] for r in manifest])
    dir_of = np.array([r["dir"] for r in manifest])
    dir_list = sorted(d for d in set(dir_of[ok]) if d in dirs)
    qmap = load_queries(dirs)
    npz = os.path.join(emb_dir, "descq_s12.npz")

    if args.cmd == "embed":
        import embed as em  # noqa: E402
        enc = em.Encoder(args.model)
        out = {}
        for which in ("title", "desc"):
            texts, keep = query_texts(qmap, dir_list, which)
            if not texts:
                print(f"{which}: no queries", file=sys.stderr); continue
            cut = [enc.truncate(t)[0] for t in texts]
            t0 = time.time()
            Q = enc.encode_texts(cut, "query")
            print(f"{which}: {len(texts)} queries embedded in {time.time() - t0:.0f}s", file=sys.stderr)
            out[which + "_vecs"] = Q.astype(np.float32)
            out[which + "_dirs"] = np.array(keep)
        np.savez(npz, **out)
        print(f"wrote {npz}", file=sys.stderr)
        return

    # ---- eval
    V = np.load(os.path.join(emb_dir, "vectors.npy"))
    calib, is_img, in_calib, mu, Vc = ev.centered_space(V, ok, mods_all, manifest, dirs, args.calib, args.calib_seed)
    Vu = ev.unit(V).astype(np.float32)
    children = {d: np.where((dir_of == d) & ok)[0] for d in dir_list}
    data = np.load(npz)
    reps_cache = {}

    def reps_for(row):
        if row in reps_cache:
            return reps_cache[row]
        space, base, param = ev.parse_rep(row)
        X_all = Vc if space == "c" else Vu
        reps_cache[row] = {d: ev.build(base, X_all[children[d]], mods_all[children[d]], param) for d in dir_list}
        return reps_cache[row]

    out = []
    out.append(f"Model: {args.model}, cache {args.emb}. Directories ranked: {len(dir_list)}; calibration seed {args.calib_seed} "
               f"({len(calib)} calibration directories give mu_txt for the centered rows). Representations built from all "
               f"embedded files of each directory (no leave-one-out; the query is not a file).")
    out.append("")
    out.append("Mean representative vectors per directory: " + ", ".join(
        f"{row} {np.mean([len(reps_for(row)[d]) for d in dir_list]):.2f}" for row in ROWS) + ".")
    rng = np.random.default_rng(0)
    for which in ("title", "desc"):
        if which + "_vecs" not in data.files:
            out.append(f"\nNo {which} queries embedded."); continue
        Q = data[which + "_vecs"]
        qdirs = list(data[which + "_dirs"])
        Qc = ev.unit(Q - mu["txt"]).astype(np.float32)
        qb = np.array([ev.bucket_of(dirs[d]["image_frac"]) for d in qdirs])
        ranks = {}
        pos = {d: i for i, d in enumerate(dir_list)}
        qpos = np.array([pos[d] for d in qdirs])
        for row in ROWS:
            space = ev.parse_rep(row)[0]
            R = reps_for(row)
            blocks = [R[d] for d in dir_list]
            starts = np.cumsum([0] + [len(b) for b in blocks[:-1]])
            R_all = np.concatenate(blocks).astype(np.float32)
            qv = Qc if space == "c" else Q
            rk = np.zeros(len(qdirs), int)
            for i0 in range(0, len(qdirs), 256):
                S = qv[i0:i0 + 256] @ R_all.T
                D = np.maximum.reduceat(S, starts, axis=1)          # (chunk, n_dirs) max over each directory's reps
                tgt = D[np.arange(len(D)), qpos[i0:i0 + 256]]
                rk[i0:i0 + 256] = 1 + (D > tgt[:, None]).sum(axis=1)
            ranks[row] = rk
        if args.dump_ranks:
            with open(args.dump_ranks, "a") as fh:
                for i, d in enumerate(qdirs):
                    fh.write(json.dumps({"set": which, "relevant_dir": d, "image_frac_bucket": str(qb[i]),
                                         **{f"rank_{r}": int(ranks[r][i]) for r in ROWS}}) + "\n")
        cells = [("all", np.ones(len(qdirs), bool)),
                 ("text-heavy [0,.2)+[.2,.5)", np.isin(qb, BUCKETS[:2])),
                 ("image-heavy [.5,.8)+[.8,1]", np.isin(qb, BUCKETS[2:]))] + [(b, qb == b) for b in BUCKETS]
        label = {"title": "Q_title (record titles)", "desc": "Q_desc (title and description)"}[which]
        out.append(f"\n### Session 12 {label}: {len(qdirs)} queries, one per directory")
        out.append("")
        out.append("| cell | queries | " + " | ".join(f"R@5 {r}" for r in ROWS) + " |")
        out.append("|---|---:|" + "---:|" * len(ROWS))
        for name, sel in cells:
            out.append(f"| {name} | {int(sel.sum())} | " + " | ".join(f"{(ranks[r][sel] <= 5).mean():.3f}" for r in ROWS) + " |")
        for k in (1, 10):
            out.append(f"\n### Session 12 {label}: recall@{k}")
            out.append("")
            out.append("| cell | queries | " + " | ".join(f"{r}" for r in ROWS) + " |")
            out.append("|---|---:|" + "---:|" * len(ROWS))
            for name, sel in cells:
                out.append(f"| {name} | {int(sel.sum())} | " + " | ".join(f"{(ranks[r][sel] <= k).mean():.3f}" for r in ROWS) + " |")
        pairs = [("c", "a"), ("ac", "a"), ("tb2c", "c"), ("bc2", "c"), ("cc", "c"), ("d", "c"), ("dc", "d")]
        out.append(f"\n### Session 12 {label}: paired differences in recall@5, 95 percent bootstrap over directories ({args.boot} resamples)")
        out.append("")
        out.append("| cell | queries | " + " | ".join(f"{x} - {y}" for x, y in pairs) + " |")
        out.append("|---|---:|" + "---|" * len(pairs))
        verdict = None
        for name, sel in cells:
            idx = np.where(sel)[0]
            cols = []
            for x, y in pairs:
                hx = (ranks[x][idx] <= 5).astype(float); hy = (ranks[y][idx] <= 5).astype(float)
                diff = hx - hy
                stat = diff.mean()
                bs = rng.integers(0, len(idx), size=(args.boot, len(idx)))
                b = diff[bs].mean(axis=1)
                lo, hi = np.percentile(b, [2.5, 97.5])
                cols.append(f"{stat:+.3f} [{lo:+.3f}, {hi:+.3f}]")
                if which == "title" and name.startswith("image-heavy") and (x, y) == ("c", "a"):
                    verdict = (stat, lo, hi)
            out.append(f"| {name} | {len(idx)} | " + " | ".join(cols) + " |")
        if verdict is not None:
            stat, lo, hi = verdict
            out.append(f"\nH12a statistic ({args.model}): c - a on image-heavy directories, Q_title, recall@5 = {stat:+.3f} [{lo:+.3f}, {hi:+.3f}]; "
                       + ("interval above zero: H12a survives." if lo > 0 else "interval includes zero: H12a is dead.")
                       + (" (The pre-registered verdict is the E1 run.)" if args.model != "jina-embeddings-v4" else ""))
    print("\n".join(out))


if __name__ == "__main__":
    main()
