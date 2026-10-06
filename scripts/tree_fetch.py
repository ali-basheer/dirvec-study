#!/usr/bin/env python3
"""dirvec session 23 corpus: whole repository trees (BRIEF.md, session 23).

Repositories of session 19's pool, read in a seeded order of their own (seed 20261106). A repository
is taken whole when its tree qualifies; every listed directory that holds a kept file goes into the
corpus with all its kept files. Listed directories and kept files are session 19's (fetch_gh.py:
nothing under a hidden or vendored path component, the extension table and the 25 MB cap of session
1). A tree qualifies when it has

  at least 8 directories that hold a kept file, one of them at depth 2 or more,
  40 to 300 kept files and at most 200 MB of them,
  at least 5 kept files with an image extension and at least 5 others.

Reading stops at 300 repositories or 33,000 files (200 and 22,000 until the amendment in BRIEF.md,
session 24, made before any tree was read). Every repository read is logged with what it
held and why it was or was not taken (data/harvest_s23.jsonl), so the share of trees that qualify is
on record. The corpus files go to data/corpus_s23/gh_<repository id>_<n>/ and data/selection_s23.jsonl
has one row per directory, in the format manifest.py reads for session 19.

  tree_fetch.py harvest [--repos 300] [--files 33000] [--workers 6] [--tmp DIR]
  fetch_gh.py download --selection data/selection_s23.jsonl --corpus data/corpus_s23   (rebuild by commit)
"""
import argparse
import json
import os
import random
import re
import shutil
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_gh as fg  # noqa: E402

SEED = 20261106
MIN_DIRS, MIN_DEPTH = 8, 2
MIN_FILES, MAX_FILES = 40, 300
MAX_BYTES = 200 * 1024 * 1024
MIN_GROUP = 5


def tree_stats(dirs):
    """Counts of one repository's listed directories that hold a kept file."""
    held = {d: v["kept"] for d, v in dirs.items() if v["kept"]}
    files = [k for kept in held.values() for k in kept]
    n_img = sum(1 for k in files if k[3] == "image")
    depth = max((0 if d == "" else d.count("/") + 1 for d in held), default=0)
    return held, {"n_dirs": len(held), "n_files": len(files), "n_image": n_img, "n_other_kept": len(files) - n_img,
                  "bytes": sum(k[1] for k in files), "max_depth": depth}


def why_not(st):
    """None when the tree qualifies, else the first rule it fails."""
    if st["n_dirs"] < MIN_DIRS:
        return "fewer than 8 directories with a kept file"
    if st["max_depth"] < MIN_DEPTH:
        return "no directory at depth 2 or more"
    if st["n_files"] < MIN_FILES:
        return "fewer than 40 kept files"
    if st["n_files"] > MAX_FILES:
        return "more than 300 kept files"
    if st["bytes"] > MAX_BYTES:
        return "more than 200 MB"
    if st["n_image"] < MIN_GROUP:
        return "fewer than 5 image files"
    if st["n_other_kept"] < MIN_GROUP:
        return "fewer than 5 other kept files"
    return None


def dir_info(d, kept, excluded):
    c = Counter(k[3] for k in kept)
    n_img = c.get("image", 0)
    return {"dir": d, "depth": 0 if d == "" else d.count("/") + 1, "n_kept": len(kept), "n_image": n_img,
            "n_pdf": c.get("pdf", 0), "n_text": c.get("text", 0), "n_table": c.get("table", 0),
            "n_other": c.get("other", 0), "bytes": sum(k[1] for k in kept), "n_excluded": excluded,
            "mixed": bool(n_img and len(kept) > n_img)}


def stage_harvest(args):
    pool = fg.jl(fg.rel(args.pool))
    if not pool and os.path.exists(fg.rel(args.pool) + ".gz"):
        import gzip
        with gzip.open(fg.rel(args.pool) + ".gz", "rt") as fh:
            pool = [json.loads(l) for l in fh if l.strip()]
    corpus = fg.rel(args.corpus)
    sel_path, log_path, hv_path = fg.rel(args.selection), fg.rel(args.log), fg.rel(args.harvest_log)
    os.makedirs(corpus, exist_ok=True)
    hv_rows = fg.jl(hv_path)
    done = {r["repo_id"] for r in hv_rows}
    n_repos = sum(1 for r in hv_rows if r.get("taken"))
    n_files = sum(r.get("n_files", 0) for r in hv_rows if r.get("taken"))
    order = fg.harvest_order(pool, args.seed)
    todo = [r for r in order if r["id"] not in done]
    print(f"tree harvest: {len(order)} usable repositories, {len(done)} read; taken {n_repos} trees, {n_files} files",
          file=sys.stderr)
    tmpdir = tempfile.mkdtemp(prefix="ghtree_", dir=args.tmp)

    def grab(repo):
        dest = os.path.join(tmpdir, f"{repo['id']}.tar.gz")
        status, note, nbytes = fg.fetch_tar(fg.tar_url(repo["full_name"], "refs/heads/" + repo["default_branch"]), dest)
        sha, dirs = "", {}
        if status == "ok":
            sha, dirs, note = fg.scan_tar(dest)
            if note:
                status = "fail"
            elif not re.fullmatch(r"[0-9a-f]{40}", sha):
                status, note = "fail", "no commit id in the tarball"
        return repo, dest, status, note, nbytes, sha, dirs

    def full():
        return n_repos >= args.repos or n_files >= args.files

    with open(sel_path, "a") as sel_out, open(log_path, "a") as log, open(hv_path, "a") as hv, \
            ThreadPoolExecutor(args.workers) as ex:
        i = 0
        while i < len(todo) and not full():
            batch = todo[i:i + args.workers * 2]
            i += len(batch)
            for repo, dest, status, note, nbytes, sha, dirs in ex.map(grab, batch):
                row = {"repo_id": repo["id"], "repo": repo["full_name"], "status": status, "note": note,
                       "tar_bytes": nbytes, "sha": sha}
                if status == "ok" and not full():
                    held, st = tree_stats(dirs)
                    why = why_not(st)
                    row.update(st)
                    row["taken"] = why is None
                    if why is not None:
                        row["why_not"] = why
                    else:
                        wanted, srows = {}, []
                        for idx, d in enumerate(sorted(held)):
                            names = fg.name_map(held[d])
                            srow = fg.selection_row(repo, sha, d, dir_info(d, held[d], dirs[d]["excluded"]), held[d], idx, names)
                            wanted[d] = (f"gh_{srow['id']}", names)
                            srows.append(srow)
                        written = fg.extract(dest, wanted, corpus)
                        missing = [(s["dir"], f["key"]) for s in srows for f in s["files"] if (s["dir"], f["key"]) not in written]
                        if missing:                     # never seen; the tree is left out whole and logged
                            for s in srows:
                                shutil.rmtree(os.path.join(corpus, f"gh_{s['id']}"), ignore_errors=True)
                            row.update({"taken": False, "why_not": "extract incomplete"})
                        else:
                            for s in srows:
                                sel_out.write(json.dumps(s, ensure_ascii=False) + "\n")
                                for f in s["files"]:
                                    log.write(json.dumps({"url": f["url"], "status": "ok", "note": "",
                                                          "path": os.path.relpath(os.path.join(corpus, f"gh_{s['id']}", f["name"]), fg.ROOT),
                                                          "record": s["id"], "key": f["key"], "license": s["license"],
                                                          "doi": None}, ensure_ascii=False) + "\n")
                            n_repos += 1
                            n_files += st["n_files"]
                    hv.write(json.dumps(row, ensure_ascii=False) + "\n")
                elif status != "ok":
                    hv.write(json.dumps(row, ensure_ascii=False) + "\n")
                # a repository fetched after the set filled is not logged: it stays unread
                if os.path.exists(dest):
                    os.remove(dest)
                for fh in (sel_out, log, hv):
                    fh.flush()
            print(f"  {i}/{len(todo)} repositories; {n_repos} trees, {n_files} files", file=sys.stderr)
    shutil.rmtree(tmpdir, ignore_errors=True)
    state = "full" if full() else "pool exhausted"
    print(f"tree harvest done ({state}): {n_repos} trees, {n_files} files", file=sys.stderr)
    print(json.dumps({"state": state, "trees": n_repos, "files": n_files}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("harvest")
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--repos", type=int, default=300)
    p.add_argument("--files", type=int, default=33000)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--pool", default="data/pool_s19.jsonl")
    p.add_argument("--corpus", default="data/corpus_s23")
    p.add_argument("--selection", default="data/selection_s23.jsonl")
    p.add_argument("--log", default="data/download_log_s23.jsonl")
    p.add_argument("--harvest-log", default="data/harvest_s23.jsonl")
    p.add_argument("--tmp", default=None)
    args = ap.parse_args()
    stage_harvest(args)


if __name__ == "__main__":
    main()
