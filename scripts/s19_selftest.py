#!/usr/bin/env python3
"""Self-test of the session 19 pipeline, end to end, with no network, no GPU and no real data.

Builds a few dozen small git repositories, serves them through a local stand-in for the GitHub search
API and the tarball endpoint, and runs every step the pod will run: fetch_gh.py pool, harvest and
history, manifest.py, build_gt.py, eval.py with the session 19 command line (on synthetic vectors
with a modality offset), s19.py corpus, validity, commitq build and commitq eval. It fails on any
error, on a rank of a, c or d that changes when cs is added to the row list, and when the planted
effect (the pooled vector loses minority files that still have a sibling) is not found.

  python3 scripts/s19_selftest.py          (about a minute; writes data/*_t19* and removes them)
"""
import io
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch_gh as fg  # noqa: E402

T = "_t19"
N_REPOS, SEED, DIM = 60, 20261104, 48
rnd = random.Random(1)
nprng = np.random.default_rng(1)
WORDS = ("river delta survey sample pressure valve turbine ledger invoice harbour signal antenna glacier "
         "pollen enzyme lattice orbit tariff quorum seismic").split()


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(map(str, cmd))}\n{r.stdout[-2000:]}\n{r.stderr[-3000:]}")
    return r


def png(path):
    Image.fromarray(nprng.integers(0, 255, size=(64, 64, 3), dtype=np.uint8)).save(path)


def text(path, topic, n=80):
    with open(path, "w") as fh:
        fh.write(" ".join(rnd.choice(WORDS + [topic] * 6) + str(rnd.randint(0, 99999)) for _ in range(n)) + "\n")


def make_repo(work, remotes, i, day):
    owner, name = f"owner{i % 45:02d}", f"proj{i:03d}"
    d = os.path.join(work, owner, name)
    os.makedirs(d)
    g = lambda *a: run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t", *a])  # noqa: E731
    run(["git", "init", "-q", "-b", "main", d])
    topic = f"topic{i}"
    os.makedirs(os.path.join(d, "src"))
    os.makedirs(os.path.join(d, "docs"))
    os.makedirs(os.path.join(d, "assets", "shots"))
    os.makedirs(os.path.join(d, "node_modules", "x"))
    os.makedirs(os.path.join(d, ".hidden"))
    text(os.path.join(d, "README.md"), topic)
    text(os.path.join(d, ".gitignore"), topic)
    for k in range(rnd.randint(4, 9)):
        text(os.path.join(d, "src", f"mod{k}.py"), topic + "src")
    for k in range(3):
        text(os.path.join(d, "node_modules", "x", f"v{k}.js"), "vendor")
        text(os.path.join(d, ".hidden", f"h{k}.txt"), "hidden")
    g("add", "-A")
    g("commit", "-q", "-m", "initial commit")
    for k in range(rnd.randint(4, 8)):                       # docs: text-heavy, images the minority
        text(os.path.join(d, "docs", f"page{k}.md"), topic + "docs")
    for k in range(rnd.randint(2, 3)):
        png(os.path.join(d, "docs", f"fig{k}.png"))
    g("add", "-A")
    g("commit", "-q", "-m", f"write the first chapters of the user guide about {topic} with figures docs/fig0.png")
    for k in range(rnd.randint(5, 9)):                       # shots: image-heavy, texts the minority
        png(os.path.join(d, "assets", "shots", f"shot{k}.png"))
    for k in range(2):
        text(os.path.join(d, "assets", "shots", f"notes{k}.txt"), topic + "shots")
    g("add", "-A")
    g("commit", "-q", "-m", f"capture new dashboard screenshots for the {topic} release gallery")
    png(os.path.join(d, "assets", "shots", "shot_extra.png"))
    g("add", "-A")
    g("commit", "-q", "-m", "Update shot_extra.png")
    sha = g("rev-parse", "HEAD").stdout.strip()
    bare = os.path.join(remotes, owner, name + ".git")
    os.makedirs(os.path.dirname(bare), exist_ok=True)
    run(["git", "clone", "-q", "--bare", d, bare])
    run(["git", "-C", bare, "config", "uploadpack.allowFilter", "true"])
    run(["git", "-C", bare, "config", "uploadpack.allowAnySHA1InWant", "true"])
    return {"id": 1000 + i, "full_name": f"{owner}/{name}", "owner": {"login": owner}, "default_branch": "main",
            "size": 300, "stargazers_count": 7, "license": {"spdx_id": "MIT" if i % 7 else "GPL-3.0"},
            "fork": i % 11 == 0, "archived": False, "language": "Python",
            "created_at": f"{day}T{i % 24:02d}:10:00Z", "pushed_at": f"{day}T23:00:00Z", "_dir": d, "_sha": sha}


def serve(repos):
    by_name = {r["full_name"]: r for r in repos}

    class Hd(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/search/repositories":
                qs = parse_qs(u.query)
                q, page = qs["q"][0], int(qs.get("page", ["1"])[0])
                a, b = q.split("created:")[1].split()[0].split("..")
                hit = [r for r in repos if a <= r["created_at"] <= b]
                items = [{k: v for k, v in r.items() if not k.startswith("_")} for r in hit[(page - 1) * 100:page * 100]]
                body = json.dumps({"total_count": len(hit), "incomplete_results": False, "items": items}).encode()
                ctype = "application/json"
            else:
                parts = unquote(u.path).strip("/").split("/")
                r = by_name.get("/".join(parts[:2]))
                if not r or parts[2] != "tar.gz":
                    self.send_response(404); self.end_headers(); return
                ref = "/".join(parts[3:]).replace("refs/heads/", "")
                body = subprocess.run(["git", "-C", r["_dir"], "archive", "--format=tar.gz",
                                       f"--prefix={parts[1]}-main/", ref], capture_output=True).stdout
                ctype = "application/gzip"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Hd)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    tmp = tempfile.mkdtemp(prefix="s19test_")
    work, remotes = os.path.join(tmp, "work"), os.path.join(tmp, "remotes")
    days = [d.isoformat() for d in fg.day_order(SEED)[:3]]
    repos = [make_repo(work, remotes, i, days[i % 3]) for i in range(N_REPOS)]
    srv = serve(repos)
    env = dict(os.environ, GH_API=f"http://127.0.0.1:{srv.server_port}", GH_CODELOAD=f"http://127.0.0.1:{srv.server_port}",
               GH_GIT="file://" + remotes, GH_SEARCH_GAP="0", S19_SFX=T, OMP_NUM_THREADS="2")
    D = lambda n: f"data/{n}"  # noqa: E731
    made = [D(f"pool{T}.jsonl"), D(f"pool{T}_days.jsonl"), D(f"selection{T}.jsonl"), D(f"download_log{T}.jsonl"),
            D(f"harvest{T}.jsonl"), D(f"ghdirs{T}.jsonl"), D(f"commits{T}.jsonl"), D(f"history{T}.jsonl"),
            D(f"manifest{T}.jsonl"), D(f"dirs{T}.jsonl"), D(f"gt_structural{T}.jsonl"), D(f"commitq{T}.jsonl"),
            D(f"corpus{T}"), D(f"emb/synth{T}")]
    for m in made:
        p = os.path.join(ROOT, m)
        shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))
    py = [sys.executable]
    try:
        run(py + ["scripts/fetch_gh.py", "pool", "--seed", str(SEED), "--max-days", "3", "--min-usable", "100000",
                  "--out", made[0], "--days-log", made[1]], cwd=ROOT, env=env)
        r = run(py + ["scripts/fetch_gh.py", "harvest", "--seed", str(SEED), "--mixed", "70", "--other", "40", "--files", "100000",
                      "--pool", made[0], "--corpus", made[12], "--selection", made[2], "--log", made[3],
                      "--harvest-log", made[4], "--ghdirs", made[5], "--tmp", tmp], cwd=ROOT, env=env)
        state = json.loads(r.stdout.strip().splitlines()[-1])
        sel = [json.loads(l) for l in open(os.path.join(ROOT, made[2]))]
        assert state["mixed"] == sum(s["mixed_ext"] for s in sel) > 30, state
        assert all(not s["repo"].startswith("owner") or s["license"] == "MIT" for s in sel)
        assert not any(".hidden" in s["dir"] or "node_modules" in s["dir"] for s in sel)
        assert all(len(s["sha"]) == 40 for s in sel)
        usable = [x for x in repos if not x["fork"] and x["license"]["spdx_id"] == "MIT"]
        assert {s["repo"] for s in sel} <= {x["full_name"] for x in usable}
        # a second harvest call is a no-op (resumable), and download rebuilds a deleted folder by commit
        n_sel = len(sel)
        run(py + ["scripts/fetch_gh.py", "harvest", "--seed", str(SEED), "--mixed", "70", "--other", "40", "--files", "100000",
                  "--pool", made[0], "--corpus", made[12], "--selection", made[2], "--log", made[3],
                  "--harvest-log", made[4], "--ghdirs", made[5], "--tmp", tmp], cwd=ROOT, env=env)
        assert len(open(os.path.join(ROOT, made[2])).readlines()) == n_sel
        victim = os.path.join(ROOT, made[12], f"gh_{sel[0]['id']}")
        before = sorted(os.listdir(victim))
        shutil.rmtree(victim)
        run(py + ["scripts/fetch_gh.py", "download", "--corpus", made[12], "--selection", made[2], "--tmp", tmp], cwd=ROOT, env=env)
        assert sorted(os.listdir(victim)) == before
        run(py + ["scripts/fetch_gh.py", "history", "--selection", made[2], "--out", made[6], "--history-log", made[7]],
            cwd=ROOT, env=env)
        commits = [json.loads(l) for l in open(os.path.join(ROOT, made[6]))]
        assert commits and all(set(c) == {"id", "repo", "commit", "time", "subject", "n_changed", "n_changed_kept"} for c in commits)
        run(py + ["scripts/manifest.py", "--corpus", made[12], "--selection", made[2], "--log", made[3], "--out-manifest", made[8],
                  "--out-dirs", made[9], "--dir-prefix", "gh_"], cwd=ROOT, env=env)
        run(py + ["scripts/build_gt.py", "--manifest", made[8], "--dirs", made[9], "--out", made[10]], cwd=ROOT, env=env)
        manifest = [json.loads(l) for l in open(os.path.join(ROOT, made[8]))]
        dirs = [json.loads(l) for l in open(os.path.join(ROOT, made[9]))]
        assert all(d.get("owner") and d.get("repo") and d.get("repo_depth") is not None for d in dirs)
        assert "github.com" in manifest[0]["licence_note"]
        # synthetic vectors: a topic per directory, an offset per input group
        gap = nprng.normal(size=DIM); gap /= np.linalg.norm(gap)
        topic = {d["dir"]: nprng.normal(size=DIM) for d in dirs}
        V = np.array([topic[m["dir"]] / np.linalg.norm(topic[m["dir"]]) + (0.9 if m["modality"] == "image" else -0.9) * gap
                      + 0.5 * nprng.normal(size=DIM) / np.sqrt(DIM) * 3 for m in manifest], np.float32)
        emb = os.path.join(ROOT, made[13])
        os.makedirs(emb)
        np.save(os.path.join(emb, "vectors.npy"), V / np.linalg.norm(V, axis=1, keepdims=True))
        with open(os.path.join(emb, "index.jsonl"), "w") as fh:
            for m in manifest:
                fh.write(json.dumps({"path": m["path"], "modality": m["modality"], "ok": True, "done": True, "note": ""}) + "\n")
        ev = py + ["scripts/eval.py", "--model", "synth", "--emb", f"synth{T}", "--manifest", made[8], "--dirs", made[9],
                   "--gt", made[10], "--criterion", "s3", "--calib", "0.2", "--calib-seed", "20261104", "--queries", "eval", "--s9"]
        e1 = run(ev + ["--reps", "a,ac,c,cc,d,dc,tb2c,tbc,cs", "--tag", "_full"], cwd=ROOT, env=env).stdout
        run(ev + ["--reps", "a,c,d", "--tag", "_acd"], cwd=ROOT, env=env)
        full = [json.loads(l) for l in open(os.path.join(emb, "ranks_full.jsonl"))]
        acd = [json.loads(l) for l in open(os.path.join(emb, "ranks_acd.jsonl"))]
        assert [(g["query_path"], g["rank_a"], g["rank_c"], g["rank_d"]) for g in full] == \
               [(g["query_path"], g["rank_a"], g["rank_c"], g["rank_d"]) for g in acd], "adding rows changed a, c or d"
        evalmd = os.path.join(tmp, "eval.md")
        open(evalmd, "w").write(e1)
        cor = run(py + ["scripts/s19.py", "corpus"], cwd=ROOT, env=env).stdout
        assert "Eligible directories listed" in cor and "Scored set:" in cor
        val = run(py + ["scripts/s19.py", "validity", "--ranks", f"E1={made[13]}/ranks_full.jsonl", "--index",
                        f"{made[13]}/index.jsonl", "--evalmd", f"E1={evalmd}"], cwd=ROOT, env=env).stdout
        assert "Reproduced: the directory bootstrap here is eval.py's." in val, val[:1500]
        line = next(l for l in val.splitlines() if l.startswith("| E1 | H19a P1s"))
        assert float(line.split("|")[5]) > 0.05, line
        assert "H19a (E1, decides)" in val and "H19c (E1, decides)" in val
        cq = run(py + ["scripts/s19.py", "commitq", "build"], cwd=ROOT, env=env).stdout
        qs = [json.loads(l) for l in open(os.path.join(ROOT, made[11]))]
        assert qs and not any("Update" in q["text"] or "initial" in q["text"].lower() or "fig0" in q["text"] for q in qs), cq
        dpos = {d["dir"]: topic[d["dir"]] for d in dirs}
        Q = np.array([dpos[q["dir"]] / np.linalg.norm(dpos[q["dir"]]) - 0.9 * gap + 0.4 * nprng.normal(size=DIM) for q in qs], np.float32)
        np.savez(os.path.join(emb, f"commitq{T}.npz"), vecs=Q / np.linalg.norm(Q, axis=1, keepdims=True),
                 qids=np.array([q["qid"] for q in qs]))
        ce = run(py + ["scripts/s19.py", "commitq", "eval", "--model", "synth", "--emb", f"synth{T}", "--enc", "E1"], cwd=ROOT, env=env).stdout
        assert "H19d statistic (E1)" in ce, ce[-800:]
        print(cor.splitlines()[2][:160])
        print("\n".join(l for l in val.splitlines() if l.startswith(("| E1 | H19", "H19"))))
        print(cq.strip()[:300])
        print(ce.strip().splitlines()[-1][:400])
        print("OK: the session 19 pipeline runs end to end and the planted loss is found.")
    finally:
        srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)
        for m in ([] if os.environ.get("S19_KEEP") else made):   # S19_KEEP=1: scripts/s21_selftest.py goes on with the set
            p = os.path.join(ROOT, m)
            shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))


if __name__ == "__main__":
    main()
