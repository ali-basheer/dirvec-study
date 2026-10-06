#!/usr/bin/env python3
"""dirvec manifest: one row per file, one row per directory.

Walks data/corpus/<dir>/<file>. Modality is an index-time label: by extension for
image, text, table and office docs; PDFs split into pdf_text / pdf_scanned by
pdftotext characters per page (threshold --pdf-chars, default 50, first 50 pages).
Files pdftotext or PIL cannot open are kept in the tree with modality "other" and
a note, so the directory composition stays honest.

Paths default to the session 1 corpus; session 3 runs
  manifest.py --corpus data/corpus_s3 --selection data/selection_s3.jsonl --log data/download_log_s3.jsonl
              --out-manifest data/manifest_s3.jsonl --out-dirs data/dirs_s3.jsonl
Session 19 (directories of GitHub repositories, scripts/fetch_gh.py) adds --dir-prefix gh_: the corpus
folders are named gh_<id>, the licence note points at the repository tree at its commit, and the
directory rows carry owner, repo, repo_dir and repo_depth from the selection file. The default prefix
(zenodo_) and every output for the Zenodo sets are unchanged.
Notes never contain absolute paths (error texts are rewritten relative to the repo root).

Outputs
  data/manifest.jsonl  path, dir, modality, bytes, sha256, pages, source_url, licence_note (+ ext, record, key, chars_per_page, note)
  data/dirs.jsonl      dir, n_files, n_<modality> counts, image_frac, pdf_scanned_frac, depth, n_excluded, record, license
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from multiprocessing import Pool

from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # very large valid images are still images; encoders downscale

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CORPUS = os.path.join(DATA, "corpus")
MODALITIES = ["image", "pdf_text", "pdf_scanned", "text", "table", "other"]

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from fetch import EXT_MODALITY, ext_of  # noqa: E402

PDF_CHARS = 50
PDF_MAX_PAGES = 50


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_stats(path):
    """(pages, chars_per_page, note). pages None when unreadable."""
    try:
        info = subprocess.run(["pdfinfo", path], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return None, None, "pdfinfo timeout"
    m = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
    if info.returncode != 0 or not m:
        return None, None, "pdfinfo failed: " + info.stderr.strip()[:80]
    pages = int(m.group(1))
    if pages == 0:
        return 0, 0.0, "zero pages"
    n = min(pages, PDF_MAX_PAGES)
    try:
        txt = subprocess.run(["pdftotext", "-l", str(n), "-enc", "UTF-8", path, "-"],
                             capture_output=True, text=True, errors="replace", timeout=180)
    except subprocess.TimeoutExpired:
        return pages, None, "pdftotext timeout"
    if txt.returncode != 0:
        return pages, None, "pdftotext failed: " + txt.stderr.strip()[:80]
    chars = len(re.sub(r"\s+", "", txt.stdout))
    return pages, chars / n, ""


def relnote(text):
    """Error text without the absolute checkout path, so the manifest reproduces across checkouts."""
    return text.replace(ROOT + os.sep, "")


def image_ok(path):
    try:
        with Image.open(path) as im:
            im.verify()
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, "image unreadable: " + relnote(repr(e))[:80]


def file_row(args):
    path, pdf_chars = args
    rel = os.path.relpath(path, ROOT)
    ext = ext_of(path)
    mod = EXT_MODALITY.get(ext, "other")
    row = {"path": rel, "dir": os.path.dirname(rel), "modality": mod,
           "bytes": os.path.getsize(path), "sha256": sha256_of(path), "pages": None,
           "ext": ext, "chars_per_page": None, "note": ""}
    if mod == "pdf":
        pages, cpp, note = pdf_stats(path)
        row["pages"], row["chars_per_page"], row["note"] = pages, cpp, relnote(note)
        if pages is None or cpp is None:
            row["modality"] = "other"
        else:
            row["modality"] = "pdf_scanned" if cpp < pdf_chars else "pdf_text"
    elif mod == "image":
        ok, note = image_ok(path)
        if not ok:
            row["modality"], row["note"] = "other", note
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf-chars", type=float, default=PDF_CHARS, help="chars per page below which a PDF is pdf_scanned")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--corpus", default="data/corpus", help="corpus directory, repo-relative")
    ap.add_argument("--selection", default="data/selection.jsonl", help="selection file, repo-relative")
    ap.add_argument("--log", default="data/download_log.jsonl", help="download log, repo-relative")
    ap.add_argument("--out-manifest", default="data/manifest.jsonl", help="repo-relative")
    ap.add_argument("--out-dirs", default="data/dirs.jsonl", help="repo-relative")
    ap.add_argument("--dir-prefix", default="zenodo_",
                    help="corpus folder name is this prefix plus the selection row's id (session 19: gh_)")
    args = ap.parse_args()
    corpus = os.path.join(ROOT, args.corpus)

    # provenance from fetch stage
    src = {}
    with open(os.path.join(ROOT, args.log)) as fh:
        for line in fh:
            r = json.loads(line)
            if r["status"] == "ok" and "url" in r:
                src[r["path"]] = r
    selection = {}
    with open(os.path.join(ROOT, args.selection)) as fh:
        for line in fh:
            r = json.loads(line)
            selection[f"{args.dir_prefix}{r['id']}"] = r

    paths = []
    for d in sorted(os.listdir(corpus)):
        dp = os.path.join(corpus, d)
        if not os.path.isdir(dp):
            continue
        for f in sorted(os.listdir(dp)):
            fp = os.path.join(dp, f)
            if os.path.isfile(fp) and not f.endswith(".part"):
                paths.append(fp)
    print(f"{len(paths)} files in {args.corpus}", file=sys.stderr)

    with Pool(args.workers) as pool:
        rows = pool.map(file_row, [(p, args.pdf_chars) for p in paths], chunksize=8)

    out_manifest = os.path.join(ROOT, args.out_manifest)
    with open(out_manifest, "w") as out:
        for row in rows:
            prov = src.get(row["path"], {})
            rec = selection.get(os.path.basename(row["dir"]), {})
            lic = rec.get("license") or prov.get("license") or "unknown"
            creators = rec.get("creators") or []
            who = creators[0] + (" et al." if len(creators) > 1 else "") if creators else ""
            row["source_url"] = prov.get("url", "")
            row["record"] = rec.get("id")
            row["key"] = prov.get("key", "")
            if rec.get("repo"):      # session 19: a directory of a GitHub repository at a fixed commit
                tree = f"https://github.com/{rec['repo']}/tree/{rec.get('sha')}/{rec.get('dir', '')}".rstrip("/")
                row["licence_note"] = f"{lic}; {tree}; {rec.get('owner', '')}".strip("; ")
            else:
                row["licence_note"] = f"{lic}; https://doi.org/{rec.get('doi')}; {who}".strip("; ")
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    by_dir = {}
    for row in rows:
        by_dir.setdefault(row["dir"], []).append(row)
    out_dirs = os.path.join(ROOT, args.out_dirs)
    with open(out_dirs, "w") as out:
        for d in sorted(by_dir):
            rs = by_dir[d]
            c = Counter(r["modality"] for r in rs)
            n = len(rs)
            rec = selection.get(os.path.basename(d), {})
            out.write(json.dumps({
                "dir": d, "n_files": n,
                **{f"n_{m}": c.get(m, 0) for m in MODALITIES},
                "image_frac": c.get("image", 0) / n,
                "pdf_scanned_frac": c.get("pdf_scanned", 0) / n,
                "depth": d.count("/") - args.corpus.rstrip("/").count("/"),
                "n_excluded": rec.get("n_excluded"),
                "record": rec.get("id"), "license": rec.get("license"),
                **({"owner": rec.get("owner"), "repo": rec["repo"], "repo_dir": rec.get("dir", ""),
                    "repo_depth": rec.get("depth")} if rec.get("repo") else {}),
            }, ensure_ascii=False) + "\n")

    tot = Counter(r["modality"] for r in rows)
    print(f"manifest: {len(rows)} files, {len(by_dir)} dirs; modality counts {dict(tot)}", file=sys.stderr)
    notes = Counter(r["note"].split(":")[0] for r in rows if r["note"])
    if notes:
        print(f"notes: {dict(notes)}", file=sys.stderr)


if __name__ == "__main__":
    main()
