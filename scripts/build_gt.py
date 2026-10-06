#!/usr/bin/env python3
"""dirvec structural ground truth, leave-one-out.

For every file f in a directory D with n(D) >= 3: query = f, relevant = {D}.
The directory representation scored against f must later be built without f.

Dedupe first, so leave-one-out cannot leak:
  exact      sha256 over every file
  image      perceptual hash (phash, 64 bit) over image files and page 1 of pdf_scanned files, hamming <= --phash
  text       simhash (64 bit, unique word 3-gram shingles) over text, table and pdf_text files, hamming <= --simhash
A file with at least one duplicate anywhere (same directory or another one) is not a query.
Images that are constant after conversion to 8-bit grey (blank scans, transparent PNGs with nothing
else) are degenerate: not hashed and not queries either.
The corpus itself is left intact; manifest.jsonl and dirs.jsonl are not modified.

Image decoding goes through embed.load_rgb (the encoder's path: palette images expanded before the
reduce, TIFFs Pillow cannot decode read with tifffile), then converted to grey. Session 1 used
load_grey, which failed silently on 35 images, so those were never dedupe-checked.

Paths default to the session 1 files; session 3 runs
  build_gt.py --manifest data/manifest_s3.jsonl --dirs data/dirs_s3.jsonl --out data/gt_structural_s3.jsonl

Output data/gt_structural.jsonl: query_path, relevant_dir, modality, image_frac_bucket
Prints bucket counts, dedupe stats and the kill criterion verdict (>= 200 qualifying dirs, >= 40 per bucket).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from multiprocessing import Pool

import imagehash
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # very large valid images are still images; encoders downscale

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from embed import load_rgb  # noqa: E402
BUCKETS = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]
TEXT_LIMIT = 40000     # chars of text hashed per file
MIN_TEXT = 100         # below this, simhash is noise; exact hash only
DEGENERATE_STD = 1.0   # grey std at 64x64 below this: constant image


def bucket(frac):
    if frac < 0.2:
        return BUCKETS[0]
    if frac < 0.5:
        return BUCKETS[1]
    if frac < 0.8:
        return BUCKETS[2]
    return BUCKETS[3]


# ---------------------------------------------------------------- hashing

def phash_file(path):
    """(hash or None, degenerate flag). Decodes through embed.load_rgb, the encoder's path."""
    try:
        im = load_rgb(path).convert("L")
    except Exception:  # noqa: BLE001
        return None, False
    small = np.asarray(im.resize((64, 64)), dtype=np.float64)
    if small.std() < DEGENERATE_STD:
        return None, True
    return int(str(imagehash.phash(im)), 16), False


def phash_pdf_page1(path):
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "p")
        try:
            subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "40", "-png", path, out],
                           capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            return None, False
        pngs = [f for f in os.listdir(td) if f.endswith(".png")]
        if not pngs:
            return None, False
        return phash_file(os.path.join(td, pngs[0]))


def text_of(path, modality):
    if modality == "pdf_text":
        try:
            r = subprocess.run(["pdftotext", "-l", "50", "-enc", "UTF-8", path, "-"],
                               capture_output=True, text=True, errors="replace", timeout=180)
            return r.stdout[:TEXT_LIMIT]
        except subprocess.TimeoutExpired:
            return ""
    try:
        with open(path, "rb") as fh:
            return fh.read(TEXT_LIMIT * 2).decode("utf-8", errors="replace")[:TEXT_LIMIT]
    except OSError:
        return ""


def simhash(text):
    toks = re.findall(r"\w+", text.lower())
    if len(toks) < 3:
        return None
    shingles = {" ".join(toks[i:i + 3]) for i in range(len(toks) - 2)}  # unique: repeated rows must not dominate
    v = [0] * 64
    for sh in shingles:
        h = int.from_bytes(hashlib.blake2b(sh.encode(), digest_size=8).digest(), "big")
        for b in range(64):
            v[b] += 1 if (h >> b) & 1 else -1
    return sum(1 << b for b in range(64) if v[b] > 0)


def hash_row(row):
    path = os.path.join(ROOT, row["path"])
    m = row["modality"]
    out = {"path": row["path"], "phash": None, "simhash": None, "text_len": 0, "degenerate": False}
    if m == "image":
        out["phash"], out["degenerate"] = phash_file(path)
    elif m == "pdf_scanned":
        out["phash"], out["degenerate"] = phash_pdf_page1(path)
    elif m in ("text", "table", "pdf_text"):
        t = text_of(path, m)
        out["text_len"] = len(re.sub(r"\s+", "", t))
        if out["text_len"] >= MIN_TEXT:
            out["simhash"] = simhash(t)
    return out


def near_pairs(items, max_dist):
    """items: list of (path, 64-bit int). Yields (path_a, path_b) with hamming <= max_dist."""
    n = len(items)
    for i in range(n):
        pi, hi = items[i]
        for j in range(i + 1, n):
            pj, hj = items[j]
            if bin(hi ^ hj).count("1") <= max_dist:
                yield pi, pj


def tally(pairs, stats, kind):
    files = set()
    for a, b in pairs:
        files.add(a)
        files.add(b)
        stats[f"{kind}_pairs"] += 1
        stats[f"{kind}_pairs_cross_dir" if os.path.dirname(a) != os.path.dirname(b) else f"{kind}_pairs_within_dir"] += 1
    stats[f"{kind}_files"] = len(files)
    return files


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phash", type=int, default=6, help="max hamming distance for image near-dups")
    ap.add_argument("--simhash", type=int, default=3, help="max hamming distance for text near-dups")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--manifest", default="data/manifest.jsonl", help="repo-relative")
    ap.add_argument("--dirs", default="data/dirs.jsonl", help="repo-relative")
    ap.add_argument("--out", default="data/gt_structural.jsonl", help="repo-relative")
    args = ap.parse_args()

    with open(os.path.join(ROOT, args.manifest)) as fh:
        manifest = [json.loads(l) for l in fh]
    with open(os.path.join(ROOT, args.dirs)) as fh:
        dirs = {r["dir"]: r for r in (json.loads(l) for l in fh)}
    by_dir = defaultdict(list)
    for r in manifest:
        by_dir[r["dir"]].append(r)

    stats = Counter()

    # exact
    by_sha = defaultdict(list)
    for r in manifest:
        by_sha[r["sha256"]].append(r["path"])
    exact_pairs = [(g[i], g[j]) for g in by_sha.values() if len(g) > 1
                   for i in range(len(g)) for j in range(i + 1, len(g))]
    dup_files = tally(exact_pairs, stats, "exact")

    # near
    with Pool(args.workers) as pool:
        hashes = pool.map(hash_row, manifest, chunksize=8)
    ph = [(h["path"], h["phash"]) for h in hashes if h["phash"] is not None]
    sh = [(h["path"], h["simhash"]) for h in hashes if h["simhash"] is not None]
    degenerate = {h["path"] for h in hashes if h["degenerate"]}
    dup_files |= tally(list(near_pairs(ph, args.phash)), stats, "image")
    dup_files |= tally(list(near_pairs(sh, args.simhash)), stats, "text")
    stats["files_excluded_as_queries_dup"] = len(dup_files)
    stats["files_excluded_as_queries_degenerate_image"] = len(degenerate)
    stats["files_phashed"] = len(ph)
    stats["files_simhashed"] = len(sh)
    excluded = dup_files | degenerate

    out_path = os.path.join(ROOT, args.out)
    n_q = 0
    qualifying = Counter()
    q_bucket = Counter()
    q_mod = Counter()
    with open(out_path, "w") as out:
        for d in sorted(by_dir):
            rows = by_dir[d]
            if len(rows) < 3:
                continue
            b = bucket(dirs[d]["image_frac"])
            wrote = 0
            for r in sorted(rows, key=lambda r: r["path"]):
                if r["path"] in excluded:
                    continue
                out.write(json.dumps({"query_path": r["path"], "relevant_dir": d,
                                      "modality": r["modality"], "image_frac_bucket": b}) + "\n")
                wrote += 1
                q_bucket[b] += 1
                q_mod[r["modality"]] += 1
            if wrote:
                qualifying[b] += 1
            n_q += wrote

    total_dirs = sum(qualifying.values())
    ok = total_dirs >= 200 and all(qualifying[b] >= 40 for b in BUCKETS)
    report = {
        "queries": n_q,
        "qualifying_dirs": total_dirs,
        "qualifying_dirs_per_bucket": {b: qualifying[b] for b in BUCKETS},
        "queries_per_bucket": {b: q_bucket[b] for b in BUCKETS},
        "queries_per_modality": dict(q_mod),
        "dedupe": dict(sorted(stats.items())),
        "kill_criterion_passed": ok,
    }
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
