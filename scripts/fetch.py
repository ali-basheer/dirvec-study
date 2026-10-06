#!/usr/bin/env python3
"""dirvec corpus fetch: Zenodo open-licence records as mixed-media directories.

Three stages, each resumable:
  pool      pull candidate record metadata from the Zenodo search API -> data/pool.jsonl
  select    stratified sample of records by image fraction        -> data/selection.jsonl
  download  fetch the selected files into data/corpus/<dir>/       -> data/download_log.jsonl

Session 11 takes a new pool snapshot beyond the pages of the first one and draws uniformly from it:
  fetch.py pool --page-from 21 --pages-per-year 20 --out data/pool_s11.jsonl
  fetch.py select --pool data/pool_s11.jsonl --total N --seed 20261101 --exclude ... --out data/selection_s11.jsonl

Session 3 draws fresh directories from the same pool, excluding the session 1 records:
  fetch.py select --seed 20261001 --exclude data/selection.jsonl --out data/selection_s3.jsonl
  fetch.py download --selection data/selection_s3.jsonl --corpus data/corpus_s3 --log data/download_log_s3.jsonl

A record is a directory. Files are kept only if their extension maps to a
modality the study can encode (image, pdf, text, table, office doc) and they
are under the size cap. Archives, media, geodata and binaries are excluded and
counted per directory so the transformation of the tree is visible.

Zenodo terms: public API, guest rate limits honoured from response headers.
Licence per record: CC0 or CC-BY only. Attribution (CC-BY) is carried in
data/selection.jsonl (creators, doi) and in manifest licence_note.
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys
import threading
import time
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests

API = "https://zenodo.org/api/records"
UA = "dirvec-corpus-builder/0.1 (research; contact via zenodo record comments)"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CORPUS = os.path.join(DATA, "corpus")

LICENCES = ("cc0-1.0", "cc-zero", "cc-by-4.0", "cc-by-3.0")

EXT_MODALITY = {}
for _e in "jpg jpeg png tif tiff gif bmp webp".split():
    EXT_MODALITY[_e] = "image"
EXT_MODALITY["pdf"] = "pdf"
for _e in ("txt md rst tex bib json xml html htm yaml yml log cff toml ini cfg "
           "py r jl m c h cpp hpp java js ts sh sql lean ipynb rmd qmd").split():
    EXT_MODALITY[_e] = "text"
for _e in "csv tsv xlsx xls ods".split():
    EXT_MODALITY[_e] = "table"
for _e in "docx doc pptx ppt odt odp rtf".split():
    EXT_MODALITY[_e] = "other"

FILE_CAP = 25 * 1024 * 1024        # per file
DIR_CAP = 100 * 1024 * 1024        # included bytes per directory
MIN_FILES, MAX_FILES = 3, 60
BUCKETS = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]


def bucket(frac):
    if frac < 0.2:
        return BUCKETS[0]
    if frac < 0.5:
        return BUCKETS[1]
    if frac < 0.8:
        return BUCKETS[2]
    return BUCKETS[3]


def ext_of(key):
    return os.path.splitext(key)[1].lower().lstrip(".")


class Client:
    """requests session that obeys Zenodo rate-limit headers and retries."""

    def __init__(self, min_interval):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.min_interval = min_interval
        self.last = 0.0
        self.lock = threading.Lock()

    def _throttle(self):
        with self.lock:
            wait = self.min_interval - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()

    def get(self, url, stream=False, **kw):
        for attempt in range(8):
            self._throttle()
            try:
                r = self.s.get(url, stream=stream, timeout=120, **kw)
            except requests.RequestException as e:
                print(f"  network error {e}; retry {attempt}", file=sys.stderr)
                time.sleep(5 * (attempt + 1))
                continue
            remaining = r.headers.get("X-RateLimit-Remaining")
            if r.status_code == 429 or (remaining is not None and int(remaining) <= 1):
                reset = r.headers.get("X-RateLimit-Reset")
                pause = max(5.0, float(reset) - time.time() + 1) if reset else 60.0
                print(f"  rate limit; sleeping {pause:.0f}s", file=sys.stderr)
                r.close()
                time.sleep(min(pause, 120))
                if r.status_code == 429:
                    continue
                return self.get(url, stream=stream, **kw)
            if r.status_code >= 500:
                r.close()
                time.sleep(10 * (attempt + 1))
                continue
            return r
        raise RuntimeError(f"gave up on {url}")


# ---------------------------------------------------------------- pool

def classify_record(rec):
    """Return per-record summary with included/excluded file lists."""
    files = rec.get("files") or []
    inc, exc = [], Counter()
    for f in files:
        key = f.get("key", "")
        ext = ext_of(key)
        mod = EXT_MODALITY.get(ext)
        size = int(f.get("size") or 0)
        if mod is None:
            exc["type:" + (ext or "none")] += 1
        elif size <= 0:
            exc["empty"] += 1
        elif size > FILE_CAP:
            exc["oversize"] += 1
        else:
            inc.append({"key": key, "size": size, "checksum": f.get("checksum"),
                        "url": f["links"]["self"], "ext": ext, "modality_ext": mod})
    meta = rec.get("metadata", {})
    n = len(inc)
    n_img = sum(1 for f in inc if f["modality_ext"] == "image")
    return {
        "id": rec["id"],
        "conceptrecid": rec.get("conceptrecid"),
        "doi": rec.get("doi"),
        "title": meta.get("title", ""),
        "license": (meta.get("license") or {}).get("id"),
        "creators": [c.get("name") for c in meta.get("creators", [])][:6],
        "publication_date": meta.get("publication_date"),
        "resource_type": (meta.get("resource_type") or {}).get("type"),
        "n_files_total": len(files),
        "n_included": n,
        "n_excluded": sum(exc.values()),
        "excluded": dict(exc),
        "included_bytes": sum(f["size"] for f in inc),
        "image_frac": (n_img / n) if n else None,
        "bucket": bucket(n_img / n) if n else None,
        "files": inc,
    }


def stage_pool(args):
    os.makedirs(DATA, exist_ok=True)
    out_path = os.path.join(ROOT, args.out)
    seen = set()
    if os.path.exists(out_path):
        with open(out_path) as fh:
            for line in fh:
                seen.add(json.loads(line)["id"])
    print(f"pool has {len(seen)} records", file=sys.stderr)
    client = Client(min_interval=2.1)  # guest search limit 30/min
    base_q = ("files.types:(jpg OR jpeg OR png OR tif OR tiff) AND "
              "files.types:(pdf OR csv OR txt OR xlsx OR md OR docx OR json OR tsv OR xls) AND "
              f"files.count:[{MIN_FILES} TO {MAX_FILES}] AND access.files:public AND "
              "metadata.rights.id:(cc0-1.0 OR cc-zero OR cc-by-4.0 OR cc-by-3.0)")
    with open(out_path, "a") as out:
        for year in range(args.year_from, args.year_to + 1):
            q = f"{base_q} AND metadata.publication_date:[{year}-01-01 TO {year}-12-31]"
            got = 0
            for page in range(args.page_from, args.page_from + args.pages_per_year):
                r = client.get(API, params={"q": q, "size": 25, "page": page, "sort": "mostrecent"})
                if r.status_code != 200:
                    print(f"  {year} p{page}: HTTP {r.status_code} {r.text[:120]}", file=sys.stderr)
                    break
                hits = r.json().get("hits", {}).get("hits", [])
                if not hits:
                    break
                for rec in hits:
                    if rec["id"] in seen:
                        continue
                    seen.add(rec["id"])
                    out.write(json.dumps(classify_record(rec), ensure_ascii=False) + "\n")
                    got += 1
                out.flush()
            print(f"{year}: +{got} (pool {len(seen)})", file=sys.stderr)


# ---------------------------------------------------------------- select

def load_pool(path="data/pool.jsonl"):
    """The pool file if present, else its committed .gz snapshot."""
    path = os.path.join(ROOT, path)
    if os.path.exists(path):
        with open(path) as fh:
            return [json.loads(l) for l in fh]
    import gzip
    with gzip.open(path + ".gz", "rt") as fh:
        return [json.loads(l) for l in fh]


def eligible(rec):
    if rec["license"] not in LICENCES:
        return False
    if not (MIN_FILES <= rec["n_included"] <= MAX_FILES):
        return False
    if rec["included_bytes"] > DIR_CAP:
        return False
    return True


def stage_select(args):
    pool = load_pool(args.pool)
    # records (and their concepts) already drawn by an earlier selection are not eligible again
    ex_ids, ex_concepts = set(), set()
    for path in args.exclude:
        with open(os.path.join(ROOT, path)) as fh:
            for line in fh:
                r = json.loads(line)
                ex_ids.add(r["id"])
                ex_concepts.add(r["conceptrecid"] or r["id"])
    if args.exclude:
        print(f"excluding {len(ex_ids)} records ({len(ex_concepts)} concepts) from {args.exclude}", file=sys.stderr)
    # one version per concept: keep the newest record id
    by_concept = {}
    for rec in pool:
        if not eligible(rec):
            continue
        c = rec["conceptrecid"] or rec["id"]
        if rec["id"] in ex_ids or c in ex_concepts:
            continue
        if c not in by_concept or rec["id"] > by_concept[c]["id"]:
            by_concept[c] = rec
    cands = defaultdict(list)
    for rec in by_concept.values():
        cands[rec["bucket"]].append(rec)
    rng = random.Random(args.seed)
    chosen = []
    if args.total:
        # uniform over the whole eligible pool, no stratification
        pool_all = sorted(by_concept.values(), key=lambda r: r["id"])
        rng.shuffle(pool_all)
        chosen = pool_all[:args.total]
        drawn = Counter(r["bucket"] for r in chosen)
        for b in BUCKETS:
            print(f"{b}: {len(cands[b])} eligible, taking {drawn[b]}", file=sys.stderr)
    else:
        for b in BUCKETS:
            pool_b = sorted(cands[b], key=lambda r: r["id"])
            rng.shuffle(pool_b)
            take = pool_b[:args.per_bucket]
            print(f"{b}: {len(pool_b)} eligible, taking {len(take)}", file=sys.stderr)
            chosen.extend(take)
    n_files = sum(r["n_included"] for r in chosen)
    print(f"selected {len(chosen)} dirs, {n_files} files, "
          f"{sum(r['included_bytes'] for r in chosen)/1e9:.2f} GB", file=sys.stderr)
    with open(os.path.join(ROOT, args.out), "w") as out:
        for rec in sorted(chosen, key=lambda r: r["id"]):
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- download

def safe_name(key):
    name = unicodedata.normalize("NFKD", key).encode("ascii", "ignore").decode()
    name = name.replace("/", "__")
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    if len(name) > 120:
        stem, ext = os.path.splitext(name)
        name = stem[:110] + ext
    return name or "file"


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stage_download(args):
    with open(os.path.join(ROOT, args.selection)) as fh:
        selection = [json.loads(l) for l in fh]
    corpus = os.path.join(ROOT, args.corpus)
    log_path = os.path.join(ROOT, args.log)
    done = set()
    if os.path.exists(log_path):
        with open(log_path) as fh:
            for line in fh:
                row = json.loads(line)
                if row["status"] == "ok":
                    done.add(row["url"])
    client = Client(min_interval=0.5)  # file limit 133/min, stay under
    jobs = []
    for rec in selection:
        d = os.path.join(corpus, f"zenodo_{rec['id']}")
        os.makedirs(d, exist_ok=True)
        used = set()
        for f in rec["files"]:
            name = safe_name(f["key"])
            stem, ext = os.path.splitext(name)
            k = 1
            while name in used:
                k += 1
                name = f"{stem}_{k}{ext}"
            used.add(name)
            path = os.path.join(d, name)
            if f["url"] in done and os.path.exists(path):
                continue
            jobs.append((rec, f, path))
    print(f"{len(jobs)} files to fetch, {len(done)} already done", file=sys.stderr)
    counts = Counter()
    log_lock = threading.Lock()

    def fetch_one(job):
        rec, f, path = job
        want = (f.get("checksum") or "").replace("md5:", "")
        status, note = "ok", ""
        if os.path.exists(path) and want and md5_of(path) == want:
            note = "already present"
        else:
            try:
                r = client.get(f["url"], stream=True)
                if r.status_code != 200:
                    status, note = "fail", f"HTTP {r.status_code}"
                else:
                    tmp = path + ".part"
                    with open(tmp, "wb") as out:
                        for chunk in r.iter_content(1 << 16):
                            out.write(chunk)
                    got = md5_of(tmp)
                    if want and got != want:
                        status, note = "fail", f"md5 mismatch {got} != {want}"
                        os.remove(tmp)
                    else:
                        os.replace(tmp, path)
            except Exception as e:  # noqa: BLE001
                status, note = "fail", repr(e)[:200]
                if os.path.exists(path + ".part"):
                    os.remove(path + ".part")
        row = {"url": f["url"], "path": os.path.relpath(path, ROOT), "status": status, "note": note,
               "record": rec["id"], "key": f["key"], "license": rec["license"], "doi": rec["doi"]}
        with log_lock:
            log.write(json.dumps(row) + "\n")
            log.flush()
            counts[status] += 1
            if status == "fail":
                print(f"  FAIL {rec['id']} {f['key']}: {note}", file=sys.stderr)
            if sum(counts.values()) % 200 == 0:
                print(f"  {counts['ok']} ok, {counts['fail']} failed", file=sys.stderr)

    with open(log_path, "a") as log, ThreadPoolExecutor(args.workers) as ex:
        list(ex.map(fetch_one, jobs))
    print(f"download done: {counts['ok']} ok, {counts['fail']} failed, {len(done)} were already done", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("pool")
    p.add_argument("--year-from", type=int, default=2017)
    p.add_argument("--year-to", type=int, default=2026)
    p.add_argument("--pages-per-year", type=int, default=20)
    p.add_argument("--page-from", type=int, default=1, help="first result page per year (session 11: 21)")
    p.add_argument("--out", default="data/pool.jsonl", help="pool file, repo-relative")
    p = sub.add_parser("select")
    p.add_argument("--per-bucket", type=int, default=100)
    p.add_argument("--seed", type=int, default=20260928)
    p.add_argument("--pool", default="data/pool.jsonl", help="pool file, repo-relative (.gz snapshot used if absent)")
    p.add_argument("--total", type=int, default=0,
                   help="draw this many uniformly over the whole eligible pool instead of --per-bucket")
    p.add_argument("--exclude", action="append", default=[],
                   help="selection file (repo-relative) whose records and concepts are not drawn again; repeatable")
    p.add_argument("--out", default="data/selection.jsonl", help="output selection file, repo-relative")
    p = sub.add_parser("download")
    p.add_argument("--workers", type=int, default=3)
    p.add_argument("--selection", default="data/selection.jsonl", help="selection file, repo-relative")
    p.add_argument("--corpus", default="data/corpus", help="corpus directory, repo-relative")
    p.add_argument("--log", default="data/download_log.jsonl", help="download log, repo-relative")
    args = ap.parse_args()
    {"pool": stage_pool, "select": stage_select, "download": stage_download}[args.stage](args)


if __name__ == "__main__":
    main()
