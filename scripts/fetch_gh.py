#!/usr/bin/env python3
"""dirvec session 19 corpus: directories of public GitHub repositories (a second, non-Zenodo source).

Four stages, each resumable:
  pool      repositories created on randomly drawn days, from the GitHub search API
            -> data/pool_s19.jsonl, data/pool_s19_days.jsonl
  harvest   per repository, in a fixed random order: the tarball of the default branch, every
            eligible directory listed (data/ghdirs_s19.jsonl, one row per eligible directory, and
            data/harvest_s19.jsonl, one row per repository), a random draw of directories kept as
            the scored set (data/selection_s19.jsonl; files in data/corpus_s19/gh_<id>/;
            data/download_log_s19.jsonl)
  download  rebuild data/corpus_s19 from data/selection_s19.jsonl (tarballs by commit)
  history   commits that changed files of one selected directory only -> data/commits_s19.jsonl

What a folder is here. A directory of a repository, at any depth, with its direct children only.
Kept files are those the study can encode, by the extension table and the size caps of fetch.py
(session 1). A directory is eligible when it keeps 3 to 100 such files and at most 100 MB. It is
mixed when it keeps at least one file with an image extension and at least one other kept file.
Directories under a hidden path component (a name that starts with a dot) or under a vendored
dependency folder (VENDORED) are not listed, and hidden files are not kept.

The frame. Days are drawn uniformly without replacement from 2016-01-01 to 2025-12-31 (the order
is a seeded shuffle of all days). For a drawn day the pool holds every public repository created
on that day with at least five stars, as the search API returns them; a day with more than 1,000
results is split in halves until every interval returns at most 1,000. A repository is used when
it is not a fork, its licence as GitHub reports it is in LICENCES, and its size is at most 200 MB.
Repositories are harvested in a seeded random order. From each one the scored set takes up to two
mixed and up to two other eligible directories, drawn at random with a seed fixed by the
repository's id, until the targets for mixed and other directories or the file budget are reached.
The rate of mixed directories among all eligible directories is reported from ghdirs_s19.jsonl,
which lists every eligible directory of every harvested repository, drawn or not.

GitHub terms: the public REST search API without a token (10 requests a minute) and the public
tarball endpoint. Set GITHUB_TOKEN to raise the search limit; it is sent to api.github.com only.
The endpoints can be redirected for tests: GH_API, GH_CODELOAD, GH_GIT.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import posixpath
import random
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch import EXT_MODALITY, FILE_CAP, DIR_CAP, bucket, ext_of, safe_name  # noqa: E402

ROOT = os.path.dirname(HERE)
API = os.environ.get("GH_API", "https://api.github.com").rstrip("/")
CODELOAD = os.environ.get("GH_CODELOAD", "https://codeload.github.com").rstrip("/")
GIT = os.environ.get("GH_GIT", "https://github.com").rstrip("/")
UA = "dirvec-corpus-builder/0.2 (research; github.com/ali-basheer/dirvec)"

DAY_FROM, DAY_TO = dt.date(2016, 1, 1), dt.date(2025, 12, 31)
MIN_STARS = 5
LICENCES = ("MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "CC0-1.0",
            "CC-BY-4.0", "0BSD")
REPO_KB_CAP = 200_000                 # the size field of the API, in KB
TAR_CAP = 300 * 1024 * 1024           # a tarball larger than this is not read
MIN_FILES, MAX_FILES = 3, 100
VENDORED = {"node_modules", "vendor", "third_party", "bower_components", "site-packages", "Pods",
            "__pycache__"}
PER_REPO_MIXED, PER_REPO_OTHER = 2, 2
HISTORY_DEPTH = 3000                  # commits read per repository
HISTORY_KEEP = 50                     # qualifying commits kept per directory, newest first


def jl(path):
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def rel(p):
    return os.path.join(ROOT, p)


# ---------------------------------------------------------------- pool

class Search:
    """Search API client: one request at a time, paced under the limit, waits out a rate limit."""

    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.s.headers["Accept"] = "application/vnd.github+json"
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            self.s.headers["Authorization"] = "Bearer " + tok
        self.gap = float(os.environ.get("GH_SEARCH_GAP", 2.2 if tok else 6.5))
        self.last = 0.0

    def get(self, q, page):
        for attempt in range(40):               # a rate limit is waited out (a minute at a time, as a rule)
            wait = self.gap - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            try:
                r = self.s.get(API + "/search/repositories", timeout=60,
                               params={"q": q, "per_page": 100, "page": page})
            except requests.RequestException as e:
                print(f"  network error {e!r}; retry {attempt}", file=sys.stderr)
                time.sleep(min(120, 10 * (attempt + 1)))
                continue
            if r.status_code == 200:
                return r.json()
            if r.status_code in (403, 429):
                reset = r.headers.get("x-ratelimit-reset")
                after = r.headers.get("retry-after")
                pause = float(after) if after else (max(5.0, float(reset) - time.time() + 2) if reset else 60.0)
                print(f"  rate limit ({r.status_code}); sleeping {min(pause, 300):.0f}s", file=sys.stderr)
                time.sleep(min(pause, 300))
                continue
            if r.status_code == 422:      # the 1,000-result window was passed
                return {"total_count": None, "items": [], "incomplete_results": False}
            print(f"  HTTP {r.status_code}: {r.text[:120]}; retry {attempt}", file=sys.stderr)
            time.sleep(min(120, 10 * (attempt + 1)))
        raise RuntimeError(f"gave up on search {q!r} page {page}")


def day_order(seed):
    days = [DAY_FROM + dt.timedelta(i) for i in range((DAY_TO - DAY_FROM).days + 1)]
    random.Random(seed).shuffle(days)
    return days


def repo_row(it, day):
    return {"id": it["id"], "full_name": it["full_name"], "owner": (it.get("owner") or {}).get("login", ""),
            "default_branch": it.get("default_branch"), "size_kb": it.get("size"),
            "stars": it.get("stargazers_count"), "license": (it.get("license") or {}).get("spdx_id"),
            "fork": bool(it.get("fork")), "archived": bool(it.get("archived")),
            "language": it.get("language"), "created_at": it.get("created_at"),
            "pushed_at": it.get("pushed_at"), "day": day}


def usable(r):
    return (not r["fork"] and r["license"] in LICENCES and r["default_branch"]
            and 0 < (r["size_kb"] or 0) <= REPO_KB_CAP)


def stage_pool(args):
    pool_path, days_path = rel(args.out), rel(args.days_log)
    os.makedirs(os.path.dirname(pool_path), exist_ok=True)
    pool = {r["id"]: r for r in jl(pool_path)}
    done_days = {r["day"] for r in jl(days_path)}
    n_usable = sum(usable(r) for r in pool.values())
    print(f"pool: {len(pool)} repositories, {n_usable} usable, {len(done_days)} days done", file=sys.stderr)
    client = Search()
    order = day_order(args.seed)
    with open(pool_path, "a") as out, open(days_path, "a") as dlog:
        for k, day in enumerate(order):
            if n_usable >= args.min_usable or len(done_days) >= args.max_days:
                break
            ds = day.isoformat()
            if ds in done_days:
                continue
            stack = [(dt.datetime.combine(day, dt.time(0, 0, 0)), dt.datetime.combine(day, dt.time(23, 59, 59)))]
            intervals, got_day = [], 0
            while stack:
                a, b = stack.pop()
                q = f"created:{a.isoformat()}Z..{b.isoformat()}Z stars:>={MIN_STARS}"
                first = client.get(q, 1)
                for _ in range(3):                      # the API can answer before its search finished
                    if not first.get("incomplete_results"):
                        break
                    time.sleep(5)
                    first = client.get(q, 1)
                total = first.get("total_count") or 0
                if total > 1000 and (b - a).total_seconds() >= 2:
                    mid = a + (b - a) / 2
                    mid = mid.replace(microsecond=0)
                    stack.append((mid + dt.timedelta(seconds=1), b))
                    stack.append((a, mid))
                    continue
                items, incomplete, page = list(first.get("items", [])), bool(first.get("incomplete_results")), 1
                while len(items) < min(total, 1000) and page < 10:
                    page += 1
                    nxt = client.get(q, page)
                    if not nxt.get("items"):
                        break
                    items += nxt["items"]
                    incomplete |= bool(nxt.get("incomplete_results"))
                new = 0
                for it in items:
                    if it["id"] in pool:
                        continue
                    row = repo_row(it, ds)
                    pool[it["id"]] = row
                    out.write(json.dumps(row, ensure_ascii=False) + "\n")
                    new += 1
                    n_usable += usable(row)
                out.flush()
                got_day += new
                intervals.append({"from": a.isoformat() + "Z", "to": b.isoformat() + "Z", "total_count": total,
                                  "returned": len(items), "new": new, "incomplete_results": incomplete})
            dlog.write(json.dumps({"day": ds, "order": k, "intervals": intervals}) + "\n")
            dlog.flush()
            done_days.add(ds)
            print(f"{ds}: +{got_day} (pool {len(pool)}, usable {n_usable}, days {len(done_days)})", file=sys.stderr)
    print(f"pool done: {len(pool)} repositories, {n_usable} usable, {len(done_days)} days", file=sys.stderr)


# ---------------------------------------------------------------- tarballs

def tar_url(full_name, ref):
    return f"{CODELOAD}/{full_name}/tar.gz/{quote(ref, safe='/')}"


def fetch_tar(url, dest):
    """Stream a tarball to dest. Returns (status, note, bytes)."""
    note = "retries exhausted"
    for attempt in range(6):
        try:
            with requests.get(url, stream=True, timeout=120, headers={"User-Agent": UA}) as r:
                if r.status_code == 404:
                    return "missing", "HTTP 404", 0
                if r.status_code in (403, 429) or r.status_code >= 500:
                    note = f"HTTP {r.status_code}"
                    time.sleep(30 * (attempt + 1))
                    continue
                if r.status_code != 200:
                    return "fail", f"HTTP {r.status_code}", 0
                n = 0
                with open(dest, "wb") as out:
                    for chunk in r.iter_content(1 << 16):
                        n += len(chunk)
                        if n > TAR_CAP:
                            return "oversize", f"tarball above {TAR_CAP} bytes", n
                        out.write(chunk)
                return "ok", "", n
        except requests.RequestException as e:
            note = repr(e)[:160]
            time.sleep(10 * (attempt + 1))
    return "fail", note, 0


def listed(parts):
    """True when the directory path (a list of components) is one the study lists."""
    return not any(p.startswith(".") or p in VENDORED for p in parts)


def scan_tar(path):
    """(commit sha, {dir: {"kept": [(name, size, ext, modality_ext)], "excluded": n}}, note)."""
    dirs = defaultdict(lambda: {"kept": [], "excluded": 0})
    try:
        with tarfile.open(path, "r:gz") as tf:
            for m in tf:
                if not m.isreg():
                    continue
                parts = m.name.split("/")[1:]          # drop the <repo>-<ref> top folder
                if not parts:
                    continue
                dparts, name = parts[:-1], parts[-1]
                if not listed(dparts):
                    continue
                d = dirs["/".join(dparts)]
                ext = ext_of(name)
                mod = EXT_MODALITY.get(ext)
                if name.startswith(".") or mod is None or m.size <= 0 or m.size > FILE_CAP:
                    d["excluded"] += 1
                else:
                    d["kept"].append((name, m.size, ext, mod))
            sha = tf.pax_headers.get("comment", "")
    except Exception as e:  # noqa: BLE001  (tarfile, gzip and zlib raise several unrelated types)
        return "", {}, "tar unreadable: " + repr(e)[:120]
    return sha, dirs, ""


def eligible_dirs(dirs):
    """Eligible directories of one repository, as rows without the file lists."""
    rows = {}
    for d, v in dirs.items():
        kept = v["kept"]
        size = sum(k[1] for k in kept)
        if not (MIN_FILES <= len(kept) <= MAX_FILES) or size > DIR_CAP:
            continue
        c = Counter(k[3] for k in kept)
        n_img = c.get("image", 0)
        rows[d] = {"dir": d, "depth": 0 if d == "" else d.count("/") + 1, "n_kept": len(kept),
                   "n_image": n_img, "n_pdf": c.get("pdf", 0), "n_text": c.get("text", 0),
                   "n_table": c.get("table", 0), "n_other": c.get("other", 0), "bytes": size,
                   "n_excluded": v["excluded"], "mixed": bool(n_img and len(kept) > n_img)}
    return rows


def extract(tar_path, wanted, corpus):
    """wanted: {repo dir: (corpus folder, {file name: safe name})}. Writes the files; returns names written."""
    written = set()
    with tarfile.open(tar_path, "r:gz") as tf:
        for m in tf:
            if not m.isreg():
                continue
            parts = m.name.split("/")[1:]
            if not parts:
                continue
            d, name = "/".join(parts[:-1]), parts[-1]
            if d not in wanted or name not in wanted[d][1]:
                continue
            folder, names = wanted[d]
            dest = os.path.join(corpus, folder, names[name])
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            src = tf.extractfile(m)
            with open(dest + ".part", "wb") as out:
                shutil.copyfileobj(src, out)
            os.replace(dest + ".part", dest)
            written.add((d, name))
    return written


def name_map(kept):
    """{file name: flat safe name}, unique within the folder, as fetch.py names downloaded files."""
    used, out = set(), {}
    for name in sorted(k[0] for k in kept):
        s = safe_name(name)
        stem, ext = os.path.splitext(s)
        k = 1
        while s in used:
            k += 1
            s = f"{stem}_{k}{ext}"
        used.add(s)
        out[name] = s
    return out


def selection_row(repo, sha, d, info, kept, idx, names):
    n_img = info["n_image"]
    did = f"{repo['id']}_{idx}"
    blob = f"https://github.com/{repo['full_name']}/blob/{sha}/"
    files = [{"key": k[0], "name": names[k[0]], "size": k[1], "ext": k[2], "modality_ext": k[3],
              "url": blob + quote(posixpath.join(d, k[0]))} for k in sorted(kept)]
    return {"id": did, "repo_id": repo["id"], "repo": repo["full_name"], "owner": (repo["owner"] or "").lower(),
            "creators": [(repo["owner"] or "").lower()], "sha": sha, "dir": d, "depth": info["depth"],
            "license": repo["license"], "stars": repo["stars"], "language": repo["language"],
            "created_at": repo["created_at"], "pushed_at": repo["pushed_at"], "mixed_ext": info["mixed"],
            "n_files_total": len(kept) + info["n_excluded"], "n_included": len(kept),
            "n_excluded": info["n_excluded"], "included_bytes": info["bytes"],
            "image_frac": n_img / len(kept), "bucket": bucket(n_img / len(kept)), "files": files}


# ---------------------------------------------------------------- harvest

def harvest_order(pool, seed):
    repos = sorted((r for r in pool if usable(r)), key=lambda r: r["id"])
    random.Random(seed).shuffle(repos)
    return repos


def stage_harvest(args):
    pool = jl(rel(args.pool))
    corpus = rel(args.corpus)
    sel_path, log_path = rel(args.selection), rel(args.log)
    hv_path, gd_path = rel(args.harvest_log), rel(args.ghdirs)
    os.makedirs(corpus, exist_ok=True)
    done = {r["repo_id"] for r in jl(hv_path)}
    sel = jl(sel_path)
    n_mixed = sum(1 for r in sel if r["mixed_ext"])
    n_other = len(sel) - n_mixed
    n_files = sum(r["n_included"] for r in sel)
    order = harvest_order(pool, args.seed)
    todo = [r for r in order if r["id"] not in done]
    print(f"harvest: {len(order)} usable repositories, {len(done)} done; scored set {n_mixed} mixed, "
          f"{n_other} other, {n_files} files", file=sys.stderr)
    tmpdir = tempfile.mkdtemp(prefix="ghtar_", dir=args.tmp)

    def grab(repo):
        dest = os.path.join(tmpdir, f"{repo['id']}.tar.gz")
        status, note, nbytes = fetch_tar(tar_url(repo["full_name"], "refs/heads/" + repo["default_branch"]), dest)
        sha, dirs = "", {}
        if status == "ok":
            sha, dirs, note = scan_tar(dest)
            if note:
                status = "fail"
            elif not re.fullmatch(r"[0-9a-f]{40}", sha):
                status, note = "fail", "no commit id in the tarball"
        return repo, dest, status, note, nbytes, sha, dirs

    def full():
        # the file budget is reached when not even the smallest eligible directory (MIN_FILES) fits
        return (n_mixed >= args.mixed and n_other >= args.other) or n_files > args.files - MIN_FILES

    with open(sel_path, "a") as sel_out, open(log_path, "a") as log, open(hv_path, "a") as hv, \
            open(gd_path, "a") as gd, ThreadPoolExecutor(args.workers) as ex:
        i = 0
        while i < len(todo) and not full():
            batch = todo[i:i + args.workers * 2]
            i += len(batch)
            for repo, dest, status, note, nbytes, sha, dirs in ex.map(grab, batch):
                row = {"repo_id": repo["id"], "repo": repo["full_name"], "status": status, "note": note,
                       "tar_bytes": nbytes, "sha": sha}
                if status == "ok" and not full():
                    elig = eligible_dirs(dirs)
                    for d in sorted(elig):
                        gd.write(json.dumps({"repo_id": repo["id"], "repo": repo["full_name"], **elig[d]},
                                            ensure_ascii=False) + "\n")
                    rng = random.Random(f"{args.seed}:{repo['id']}")
                    mixed = sorted(d for d in elig if elig[d]["mixed"])
                    other = sorted(d for d in elig if not elig[d]["mixed"])
                    take = rng.sample(mixed, min(len(mixed), PER_REPO_MIXED, max(0, args.mixed - n_mixed)))
                    take += rng.sample(other, min(len(other), PER_REPO_OTHER, max(0, args.other - n_other)))
                    chosen, wanted = [], {}
                    for d in sorted(take):
                        if n_files + sum(elig[x]["n_kept"] for x in chosen) + elig[d]["n_kept"] > args.files:
                            continue
                        chosen.append(d)
                    for idx, d in enumerate(chosen):
                        names = name_map(dirs[d]["kept"])
                        srow = selection_row(repo, sha, d, elig[d], dirs[d]["kept"], idx, names)
                        wanted[d] = (f"gh_{srow['id']}", names, srow)
                    written = extract(dest, {d: (w[0], w[1]) for d, w in wanted.items()}, corpus) if wanted else set()
                    n_bad = 0
                    for d, (folder, names, srow) in wanted.items():
                        missing = [f["key"] for f in srow["files"] if (d, f["key"]) not in written]
                        if missing:       # never seen; kept out of the scored set and counted in the harvest row
                            n_bad += 1
                            shutil.rmtree(os.path.join(corpus, folder), ignore_errors=True)
                            print(f"  extract incomplete, directory left out: {repo['full_name']} {d!r} {missing[:3]}",
                                  file=sys.stderr)
                            continue
                        sel_out.write(json.dumps(srow, ensure_ascii=False) + "\n")
                        for f in srow["files"]:
                            log.write(json.dumps({"url": f["url"], "status": "ok", "note": "",
                                                  "path": os.path.relpath(os.path.join(corpus, folder, f["name"]), ROOT),
                                                  "record": srow["id"], "key": f["key"],
                                                  "license": srow["license"], "doi": None}, ensure_ascii=False) + "\n")
                        n_mixed += srow["mixed_ext"]
                        n_other += not srow["mixed_ext"]
                        n_files += srow["n_included"]
                    row.update({"n_dirs": len(dirs), "n_eligible": len(elig),
                                "n_eligible_mixed": len(mixed), "n_taken": len(chosen) - n_bad,
                                **({"n_extract_incomplete": n_bad} if n_bad else {})})
                    hv.write(json.dumps(row, ensure_ascii=False) + "\n")
                elif status != "ok":
                    hv.write(json.dumps(row, ensure_ascii=False) + "\n")
                # a repository fetched after the scored set filled is not logged: it stays unharvested
                if os.path.exists(dest):
                    os.remove(dest)
                for fh in (sel_out, log, hv, gd):
                    fh.flush()
            print(f"  {i}/{len(todo)} repositories; scored set {n_mixed} mixed, {n_other} other, {n_files} files",
                  file=sys.stderr)
    shutil.rmtree(tmpdir, ignore_errors=True)
    state = "full" if full() else "pool exhausted"
    print(f"harvest done ({state}): {n_mixed} mixed, {n_other} other directories, {n_files} files", file=sys.stderr)
    print(json.dumps({"state": state, "mixed": n_mixed, "other": n_other, "files": n_files}))


# ---------------------------------------------------------------- download (rebuild by commit)

def stage_download(args):
    sel = jl(rel(args.selection))
    corpus = rel(args.corpus)
    by_repo = defaultdict(list)
    for r in sel:
        by_repo[(r["repo"], r["sha"])].append(r)
    tmpdir = tempfile.mkdtemp(prefix="ghtar_", dir=args.tmp)
    counts = Counter()

    def one(item):
        (full_name, sha), rows = item
        if all(os.path.exists(os.path.join(corpus, f"gh_{r['id']}", f["name"])) for r in rows for f in r["files"]):
            return "present"
        dest = os.path.join(tmpdir, hashlib.sha1(f"{full_name}@{sha}".encode()).hexdigest() + ".tar.gz")
        status, note, _ = fetch_tar(tar_url(full_name, sha), dest)
        if status != "ok":
            print(f"  FAIL {full_name}@{sha[:10]}: {status} {note}", file=sys.stderr)
            return "fail"
        wanted = {r["dir"]: (f"gh_{r['id']}", {f["key"]: f["name"] for f in r["files"]}) for r in rows}
        written = extract(dest, wanted, corpus)
        os.remove(dest)
        miss = sum(1 for r in rows for f in r["files"] if (r["dir"], f["key"]) not in written)
        return "ok" if not miss else "incomplete"

    with ThreadPoolExecutor(args.workers) as ex:
        for res in ex.map(one, sorted(by_repo.items())):
            counts[res] += 1
    shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"download done: {dict(counts)} over {len(by_repo)} repositories", file=sys.stderr)


# ---------------------------------------------------------------- history

def git(args, cwd=None, timeout=300):
    # public repositories only: no stored credential is sent and git never waits at a prompt
    return subprocess.run(["git", "-c", "core.quotePath=false", "-c", "credential.helper="] + args, cwd=cwd,
                          capture_output=True, text=True, errors="replace", timeout=timeout,
                          env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, stdin=subprocess.DEVNULL)


def commits_of(full_name, sha, rows, depth):
    """Qualifying commits per selected directory of one repository: every path the commit changed
    lies directly in that directory, and at least one of them is a kept file of the directory at
    the harvested commit. No author name or address is read."""
    want = {r["dir"]: (r["id"], {f["key"] for f in r["files"]}) for r in rows}
    tmp = tempfile.mkdtemp(prefix="ghhist_")
    out, note = [], ""
    try:
        r = git(["init", "-q", tmp])
        url = f"{GIT}/{full_name}.git"
        r = git(["fetch", "-q", "--filter=blob:none", f"--depth={depth}", url, sha], cwd=tmp, timeout=420)
        if r.returncode != 0:
            return [], "fetch failed: " + r.stderr.strip()[:160]
        r = git(["log", "--no-merges", "--no-renames", "--name-only", "--format=%x1e%H%x1f%ct%x1f%s", "FETCH_HEAD"],
                cwd=tmp, timeout=420)
        if r.returncode != 0:
            return [], "log failed: " + r.stderr.strip()[:160]
        kept_n = Counter()
        for rec in r.stdout.split("\x1e")[1:]:
            head, _, body = rec.partition("\n")
            parts = head.split("\x1f")
            if len(parts) != 3:
                continue
            paths = [p for p in body.split("\n") if p.strip()]
            if not paths:
                continue
            ds = {posixpath.dirname(p) for p in paths}
            if len(ds) != 1:
                continue
            d = ds.pop()
            if d not in want:
                continue
            did, keys = want[d]
            n_kept = sum(1 for p in paths if posixpath.basename(p) in keys)
            if not n_kept or kept_n[did] >= HISTORY_KEEP:
                continue
            kept_n[did] += 1
            out.append({"id": did, "repo": full_name, "commit": parts[0], "time": int(parts[1]),
                        "subject": parts[2], "n_changed": len(paths), "n_changed_kept": n_kept})
    except subprocess.TimeoutExpired:
        note = "timeout"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out, note


def stage_history(args):
    sel = jl(rel(args.selection))
    out_path, log_path = rel(args.out), rel(args.history_log)
    done = {r["repo"] for r in jl(log_path)}
    by_repo = defaultdict(list)
    for r in sel:
        by_repo[(r["repo"], r["sha"])].append(r)
    todo = [it for it in sorted(by_repo.items()) if it[0][0] not in done]
    print(f"history: {len(by_repo)} repositories, {len(done)} done", file=sys.stderr)
    lock = threading.Lock()
    n = Counter()

    def one(item):
        (full_name, sha), rows = item
        commits, note = commits_of(full_name, sha, rows, args.depth)
        with lock:
            for c in commits:
                out.write(json.dumps(c, ensure_ascii=False) + "\n")
            log.write(json.dumps({"repo": full_name, "commits": len(commits), "note": note}) + "\n")
            out.flush()
            log.flush()
            n["repos"] += 1
            n["commits"] += len(commits)
            n["failed"] += bool(note)
            if n["repos"] % 100 == 0:
                print(f"  {n['repos']} repositories, {n['commits']} commits, {n['failed']} failed", file=sys.stderr)

    with open(out_path, "a") as out, open(log_path, "a") as log, ThreadPoolExecutor(args.workers) as ex:
        list(ex.map(one, todo))
    print(f"history done: {n['repos']} repositories read now, {n['commits']} qualifying commits, "
          f"{n['failed']} failed", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("pool")
    p.add_argument("--seed", type=int, default=20261104)
    p.add_argument("--min-usable", type=int, default=4000, help="stop when the pool holds this many usable repositories")
    p.add_argument("--max-days", type=int, default=400, help="never read more than this many days")
    p.add_argument("--out", default="data/pool_s19.jsonl")
    p.add_argument("--days-log", default="data/pool_s19_days.jsonl")
    p = sub.add_parser("harvest")
    p.add_argument("--seed", type=int, default=20261104)
    p.add_argument("--mixed", type=int, default=1000, help="target number of mixed directories")
    p.add_argument("--other", type=int, default=600, help="target number of other directories")
    p.add_argument("--files", type=int, default=24000, help="file budget of the scored set")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--pool", default="data/pool_s19.jsonl")
    p.add_argument("--corpus", default="data/corpus_s19")
    p.add_argument("--selection", default="data/selection_s19.jsonl")
    p.add_argument("--log", default="data/download_log_s19.jsonl")
    p.add_argument("--harvest-log", default="data/harvest_s19.jsonl")
    p.add_argument("--ghdirs", default="data/ghdirs_s19.jsonl")
    p.add_argument("--tmp", default=None, help="folder for tarballs while they are read (default: the system's)")
    p = sub.add_parser("download")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--corpus", default="data/corpus_s19")
    p.add_argument("--selection", default="data/selection_s19.jsonl")
    p.add_argument("--tmp", default=None)
    p = sub.add_parser("history")
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--depth", type=int, default=HISTORY_DEPTH)
    p.add_argument("--selection", default="data/selection_s19.jsonl")
    p.add_argument("--out", default="data/commits_s19.jsonl")
    p.add_argument("--history-log", default="data/history_s19.jsonl")
    args = ap.parse_args()
    {"pool": stage_pool, "harvest": stage_harvest, "download": stage_download, "history": stage_history}[args.stage](args)


if __name__ == "__main__":
    main()
