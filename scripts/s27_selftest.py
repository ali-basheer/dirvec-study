#!/usr/bin/env python3
"""Self-test of scripts/s27.py and scripts/humanq_tool.py (session 27) on a synthetic set.

1. Writes a synthetic S11-like set (data/*_t27*, data/emb/synth27, data/corpus_t27) and runs eval.py on it
   (rows a, ac, c, cc, d, dc, tb2, tb2c, tbc, tbcc; calibration 0.2, seed 20261102).
2. s27.py budget and seeds on it: the gates must pass against eval.py's ranks (L3 = c, L3c = cc, B2 = tb2,
   B2c = tb2c, M3 = tbc, M3c = tbcc, a, ac, d, dc; L3s0 = c, B2cs0 = tb2c).
3. Every row of both runs recomputed by a plain implementation: every folder rebuilt from scratch for every
   query, scores in float64. A rank may differ only where a competitor scores within 1e-5 of the own folder.
4. s27.py report runs on the two files.
5. humanq_tool.py sample, payload and html on the synthetic set; s27.py human-eval with a title gate against
   descq.py's own ranks (descq.py eval --dump-ranks on the same set), its ranks recomputed plainly, and
   human-report.
Everything it writes is removed at the end unless --keep.

  python3 scripts/s27_selftest.py [--keep]
"""
import gzip
import json
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402
import s27  # noqa: E402

PY = sys.executable
TIE = 1e-5
EMB = "data/emb/synth27"
WRITTEN = ["data/manifest_t27.jsonl", "data/dirs_t27.jsonl", "data/gt_structural_t27.jsonl", "data/selection_t27.jsonl",
           "data/humanq_sample_t27.jsonl", "data/humanq_t27.jsonl", EMB, "data/corpus_t27", "build/t27"]


def run(cmd, ok_codes=(0,)):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode not in ok_codes:
        sys.stderr.write(r.stdout[-3000:] + "\n" + r.stderr[-5000:] + "\n")
        sys.exit(f"FAILED: {' '.join(cmd)} exited {r.returncode}")
    return r


def make_set(rng):
    from PIL import Image
    labels = ev.MODALITIES
    os.makedirs(os.path.join(ROOT, EMB), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "data/corpus_t27"), exist_ok=True)
    dim = 24
    gap = rng.normal(0, 1, dim)
    lab_off = {L: rng.normal(0, 0.8, dim) for L in labels}
    man, dirs, sel, vecs, index = [], [], [], [], []
    words = ["river", "sample", "core", "plot", "field", "survey", "leaf", "rock", "map", "chart", "grain", "soil",
             "photo", "table", "notes", "report", "image", "site", "season", "trap"]
    for k in range(72):
        d = f"data/corpus_t27/zenodo_{1000 + k}"
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
        n = int(rng.integers(3, 26))
        frac = rng.choice([0.1, 0.35, 0.65, 0.9])
        mods = ["image" if rng.random() < frac else str(rng.choice(["text", "table", "pdf_text", "other", "pdf_scanned"],
                                                                      p=[.4, .3, .1, .15, .05])) for _ in range(n)]
        topic = rng.normal(0, 1, dim)
        sub = [rng.normal(0, 0.9, dim) for _ in range(3)]
        for j, m in enumerate(mods):
            ext = {"image": "png", "text": "txt", "table": "csv", "pdf_text": "pdf", "other": "docx", "pdf_scanned": "pdf"}[m]
            name = f"f{j:02d}_{words[j % len(words)]}.{ext}"
            path = f"{d}/{name}"
            if m == "image":
                arr = (rng.random((40 + j, 60, 3)) * 255).astype(np.uint8)
                Image.fromarray(arr).save(os.path.join(ROOT, path))
            elif m in ("text", "table"):
                with open(os.path.join(ROOT, path), "w") as fh:
                    sep = "," if m == "table" else " "
                    fh.write(sep.join(str(rng.choice(words)) for _ in range(60)) + f" {name} 2024 site 12\n")
            v = topic + sub[j % 3] + lab_off[m] + (gap if m in ("image", "pdf_scanned") else 0) + rng.normal(0, 0.7, dim)
            vecs.append(v / np.linalg.norm(v))
            okf = bool(rng.random() > 0.06) and m not in ("pdf_text", "other", "pdf_scanned")
            man.append({"path": path, "dir": d, "modality": m, "ext": ext, "sha256": f"{k:04d}{j:04d}" * 8,
                        "record": 1000 + k, "bytes": 1, "pages": None, "chars_per_page": None, "note": "", "key": name})
            index.append({"path": path, "ok": okf, "done": True})
        n_img = sum(1 for m in mods if m == "image")
        dirs.append({"dir": d, "n_files": n, "image_frac": n_img / n, "record": 1000 + k,
                     **{f"n_{L}": sum(1 for m in mods if m == L) for L in labels}})
        fam = f"creator {k % 61}"
        sel.append({"id": 1000 + k, "creators": [fam.title()], "title": f"The {words[k % 20]} {words[(k + 3) % 20]} survey of site {k}"})
    for name, rows in (("manifest_t27", man), ("dirs_t27", dirs), ("selection_t27", sel)):
        with open(os.path.join(ROOT, f"data/{name}.jsonl"), "w") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in rows)
    with open(os.path.join(ROOT, "data/gt_structural_t27.jsonl"), "w") as fh:
        for r in man:
            dr = next(x for x in dirs if x["dir"] == r["dir"])
            fh.write(json.dumps({"query_path": r["path"], "relevant_dir": r["dir"], "modality": r["modality"],
                                 "image_frac_bucket": ev.bucket_of(dr["image_frac"])}) + "\n")
    np.save(os.path.join(ROOT, EMB, "vectors.npy"), np.array(vecs, np.float32))
    with open(os.path.join(ROOT, EMB, "index.jsonl"), "w") as fh:
        fh.writelines(json.dumps(r) + "\n" for r in index)
    return man, dirs


def plain_ranks(rows, npz):
    """Every row rebuilt from scratch for every query, float64 scores; returns {row: (ranks, near-tie mask)}."""
    man = [json.loads(l) for l in open(os.path.join(ROOT, "data/manifest_t27.jsonl"))]
    dirs = {json.loads(l)["dir"]: json.loads(l) for l in open(os.path.join(ROOT, "data/dirs_t27.jsonl"))}
    index = [json.loads(l) for l in open(os.path.join(ROOT, EMB, "index.jsonl"))]
    ok = np.array([r["ok"] for r in index])
    V = np.load(os.path.join(ROOT, EMB, "vectors.npy"))
    mods = np.array([r["modality"] for r in man])
    calib, is_img, in_calib, mu, Vc = ev.centered_space(V, ok, mods, man, dirs, 0.2, 20261102)
    space = {"u": V, "c": Vc}
    ranked = sorted(d for d, r in dirs.items() if r["n_files"] >= 3)
    kids = {d: np.array([i for i, r in enumerate(man) if ok[i] and r["dir"] == d], int) for d in ranked}
    row_of = {r["path"]: i for i, r in enumerate(man)}

    def build(row, X, labs):
        fam, p, sp, seed = s27.parse_row(row)
        if len(X) == 0:
            return X
        if fam == "a":
            return ev.unit(X.mean(axis=0, keepdims=True))
        if fam == "d":
            return X
        if fam == "L":
            return np.concatenate([ev.kreps(X[labs == L], seed=seed, k=min(p, int((labs == L).sum())))
                                   for L in ev.MODALITIES if (labs == L).any()])
        cnt = [int((labs == L).sum()) for L in ev.MODALITIES]
        k = min(p, len(X)) if fam == "B" else s27.label_budget(cnt, p)
        return ev.kreps(X, seed=seed, k=k)

    out = {}
    qpaths = list(npz["qpath"])
    for row in rows:
        sp = s27.parse_row(row)[2]
        W = space[sp]
        full = {d: build(row, W[kids[d]], mods[kids[d]]) for d in ranked}
        rk = np.zeros(len(qpaths), int)
        tie = np.zeros(len(qpaths), bool)
        for k, qp in enumerate(qpaths):
            i = row_of[qp]
            d0 = man[i]["dir"]
            q = W[i].astype(np.float64)
            keep = kids[d0][kids[d0] != i]
            R0 = build(row, W[keep], mods[keep])
            own = (R0.astype(np.float64) @ q).max() if len(R0) else -np.inf
            sc = np.array([(full[d].astype(np.float64) @ q).max() if len(full[d]) else -np.inf for d in ranked if d != d0])
            rk[k] = 1 + int((sc > own).sum())
            tie[k] = bool(np.any(np.abs(sc - own) < TIE))
        out[row] = (rk, tie)
    return out


def main():
    keep = "--keep" in sys.argv
    rng = np.random.default_rng(27)
    for p in WRITTEN:
        q = os.path.join(ROOT, p)
        if os.path.isdir(q):
            shutil.rmtree(q)
        elif os.path.exists(q):
            os.remove(q)
    try:
        man, dirs = make_set(rng)
        print("synthetic set written:", len(man), "files,", len(dirs), "folders")
        run([PY, "scripts/eval.py", "--model", "synth27", "--emb", "synth27", "--manifest", "data/manifest_t27.jsonl",
             "--dirs", "data/dirs_t27.jsonl", "--gt", "data/gt_structural_t27.jsonl", "--criterion", "s3", "--calib", "0.2",
             "--calib-seed", "20261102", "--reps", "a,ac,c,cc,d,dc,tb2,tb2c,tbc,tbcc", "--tag", "_t27"])
        tmp = os.path.join(ROOT, "build/t27")
        os.makedirs(tmp, exist_ok=True)
        for kind in ("budget", "seeds"):
            r = run([PY, "scripts/s27.py", kind, "--set", "t27", "--emb", EMB, "--enc", "E1", "--calib-seed", "20261102",
                     "--check", f"{EMB}/ranks_t27.jsonl", "--out", f"build/t27/{kind}.npz", "--procs", "2", "--tmp", tmp])
            meta = json.loads(r.stdout.strip().splitlines()[-1])
            assert meta["gate"]["pass"], meta["gate"]
            print(kind, "gate passed:", meta["gate"]["checks"][0]["rows"])
            z = np.load(os.path.join(tmp, f"{kind}.npz"))
            rows = meta["rows"]
            pr = plain_ranks(rows, z)
            bad = 0
            for row in rows:
                got = z[f"rank_{row}"]
                want, tie = pr[row]
                diff = got != want
                bad += int((diff & ~tie).sum())
                if diff.any():
                    print(f"  {row}: {int(diff.sum())} ranks differ, {int((diff & tie).sum())} of them at a near-tie")
            assert bad == 0, f"{bad} ranks differ without a near-tie"
            print(kind, f"plain recomputation: every rank of {len(rows)} rows agrees ({len(z['qpath'])} queries)")
        rep = run([PY, "scripts/s27.py", "report", "build/t27/budget.npz", "build/t27/seeds.npz"])
        assert "Reading H27d" in rep.stdout and "Reading H27e" in rep.stdout
        print("report ran:", len(rep.stdout.splitlines()), "lines")

        # 27A on the synthetic set
        idx = f"{EMB}/index.jsonl"
        run([PY, "scripts/humanq_tool.py", "sample", "--index", f"E1={idx},E2={idx},E3={idx},E4={idx}",
             "--manifest", "data/manifest_t27.jsonl", "--dirs", "data/dirs_t27.jsonl", "--gt", "data/gt_structural_t27.jsonl",
             "--selection", "data/selection_t27.jsonl", "--out", "data/humanq_sample_t27.jsonl"])
        r = run([PY, "scripts/humanq_tool.py", "sample", "--index", f"E1={idx},E2={idx},E3={idx},E4={idx}",
                 "--manifest", "data/manifest_t27.jsonl", "--dirs", "data/dirs_t27.jsonl", "--gt", "data/gt_structural_t27.jsonl",
                 "--selection", "data/selection_t27.jsonl", "--out", "data/humanq_sample_t27.jsonl", "--check"])
        assert "identical" in r.stderr
        sample = [json.loads(l) for l in open(os.path.join(ROOT, "data/humanq_sample_t27.jsonl"))]
        assert sample, "no folder sampled"
        fams = [s["family"] for s in sample]
        assert len(fams) == len(set(fams)), "a family twice in the sample"
        print("sample:", len(sample), "folders,", dict(zip(*np.unique([s["bucket"] for s in sample], return_counts=True))))
        run([PY, "scripts/humanq_tool.py", "payload", "--sample", "data/humanq_sample_t27.jsonl", "--manifest",
             "data/manifest_t27.jsonl", "--selection", "data/selection_t27.jsonl", "--out", "build/t27/payload.json.gz"])
        pl = json.load(gzip.open(os.path.join(tmp, "payload.json.gz"), "rt"))
        blob = json.dumps(pl)
        assert "zenodo_" not in blob and ".png" not in blob and ".csv" not in blob, "a path or name leaked into the payload"
        assert not any(ch.isdigit() for f in pl["folders"] for x in f["files"] for ch in x.get("text", "")), "a digit leaked"
        run([PY, "scripts/humanq_tool.py", "html", "--payload", "build/t27/payload.json.gz", "--out", "build/t27/tool.html"])
        # queries: the first target of each kind, a few words, vectors near the target's
        V = np.load(os.path.join(ROOT, EMB, "vectors.npy"))
        row_of = {r["path"]: i for i, r in enumerate(man)}
        lines, vecs, qids, texts = [], [], [], []
        for s in sample:
            files = {f["key"]: f for f in s["files"]}
            for kind in ("QI", "QT"):
                t = s[f"targets_{kind}"][0]
                text = f"{kind.lower()} words about {files[t]['modality']} {s['key'].lower()}"
                lines.append(json.dumps({"build": "x", "folder": s["key"], "kind": kind, "target": t, "query": text,
                                         "writer": "test", "skipped": []}))
                v = V[row_of[files[t]["path"]]] + rng.normal(0, 0.15, V.shape[1])
                vecs.append(v / np.linalg.norm(v))
                qids.append(f"{s['key']}:{kind}")
                texts.append(text)
        with open(os.path.join(ROOT, "data/humanq_t27.jsonl"), "w") as fh:
            fh.write("\n".join(lines) + "\n")
        np.savez(os.path.join(ROOT, EMB, "humanq_s27.npz"), vecs=np.array(vecs, np.float32), qid=np.array(qids),
                 query=np.array(texts))
        # titles for the gate, and descq.py's own ranks of them
        ranked = sorted(d["dir"] for d in dirs if d["n_files"] >= 3)
        tv = []
        for d in ranked:
            ii = [i for i, r in enumerate(man) if r["dir"] == d]
            v = V[ii].mean(axis=0) + rng.normal(0, 0.2, V.shape[1])
            tv.append(v / np.linalg.norm(v))
        index = [json.loads(l) for l in open(os.path.join(ROOT, EMB, "index.jsonl"))]
        with_ok = sorted({man[i]["dir"] for i, r in enumerate(index) if r["ok"]})
        tdirs = [d for d in with_ok]
        tv = [tv[ranked.index(d)] if d in ranked else tv[0] for d in tdirs]
        np.savez(os.path.join(ROOT, EMB, "descq_s12.npz"), title_vecs=np.array(tv, np.float32), title_dirs=np.array(tdirs))
        dump = os.path.join(tmp, "descq_dump.jsonl")
        run([PY, "scripts/descq.py", "eval", "--model", "synth27", "--emb", "synth27", "--manifest", "data/manifest_t27.jsonl",
             "--dirs", "data/dirs_t27.jsonl", "--dump-ranks", dump])
        r = run([PY, "scripts/s27.py", "human-eval", "--enc", "E1", "--emb", EMB, "--queries", "data/humanq_t27.jsonl",
                 "--sample", "data/humanq_sample_t27.jsonl", "--manifest", "data/manifest_t27.jsonl", "--dirs",
                 "data/dirs_t27.jsonl", "--check-titles", dump, "--out", "build/t27/human_e1.npz"])
        meta = json.loads(r.stdout.strip().splitlines()[-1])
        assert meta["gate"]["pass"], meta["gate"]
        print("human-eval: title gate passed", {k: v for k, v in meta["gate"].items() if k != "pass"})
        z = np.load(os.path.join(tmp, "human_e1.npz"))
        # plain recomputation of the human ranks
        mods = np.array([r["modality"] for r in man])
        okv = np.array([r["ok"] for r in index])
        dl = with_ok
        dirs_d = {d["dir"]: d for d in dirs}
        calib, is_img, in_calib, mu, Vc = ev.centered_space(V, okv, mods, man, dirs_d, 0.2, 20261102)
        Vu = ev.unit(V).astype(np.float32)
        Q = np.array(vecs, np.float32)
        Qc = ev.unit(Q - mu["txt"]).astype(np.float32)
        own_dir = {s["key"]: s["dir"] for s in sample}
        bad = 0
        for row in s27.HROWS:
            space, base, param = ev.parse_rep(row)
            X = Vc if space == "c" else Vu
            reps = {d: ev.build(base, X[[i for i in range(len(man)) if okv[i] and man[i]["dir"] == d]],
                                mods[[i for i in range(len(man)) if okv[i] and man[i]["dir"] == d]], param) for d in dl}
            for k, qid in enumerate(qids):
                q = (Qc if space == "c" else Q)[k].astype(np.float64)
                sc = {d: (reps[d].astype(np.float64) @ q).max() for d in dl}
                o = sc[own_dir[qid.split(":")[0]]]
                want = 1 + sum(1 for d, v in sc.items() if v > o)
                near = any(abs(v - o) < TIE for d, v in sc.items() if d != own_dir[qid.split(":")[0]])
                if want != z[f"rank_{row}"][k] and not near:
                    bad += 1
        assert bad == 0, f"{bad} human ranks differ without a near-tie"
        print("human-eval: every rank agrees with the plain recomputation")
        r = run([PY, "scripts/s27.py", "human-report", "build/t27/human_e1.npz", "--min-folders", "1"])
        assert "Venue rule" in r.stdout
        print("human-report ran:", len(r.stdout.splitlines()), "lines")
        print("SELF-TEST PASSED")
    finally:
        if not keep:
            for p in WRITTEN:
                q = os.path.join(ROOT, p)
                if os.path.isdir(q):
                    shutil.rmtree(q)
                elif os.path.exists(q):
                    os.remove(q)


if __name__ == "__main__":
    main()
