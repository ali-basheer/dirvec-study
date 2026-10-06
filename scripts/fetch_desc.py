#!/usr/bin/env python3
"""Session 12: fetch the Zenodo record description of every selected session 11 record.
Writes data/desc_s11.jsonl (one row per record: id, title, description as plain text,
publication_date). Resumable: records already in the file are skipped. One request per second
(Zenodo guest rate limit). Usage: python scripts/fetch_desc.py [--limit N]
"""
import argparse, html, json, os, re, sys, time
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEL = os.path.join(ROOT, "data", "selection_s11.jsonl")
OUT = os.path.join(ROOT, "data", "desc_s11.jsonl")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_html(s):
    s = TAG_RE.sub(" ", s or "")
    s = html.unescape(s)
    return WS_RE.sub(" ", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=1.1)
    args = ap.parse_args()
    ids = []
    with open(SEL) as fh:
        for line in fh:
            r = json.loads(line)
            ids.append((int(r["id"]), r.get("title", "")))
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as fh:
            for line in fh:
                done.add(int(json.loads(line)["id"]))
    todo = [(i, t) for i, t in ids if i not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(ids)} records, {len(done)} done, {len(todo)} to fetch", flush=True)
    sess = requests.Session()
    sess.headers["User-Agent"] = "dirvec-study/0.1 (research; contact via repository)"
    n_ok = n_fail = 0
    with open(OUT, "a") as out:
        for k, (rid, title) in enumerate(todo):
            url = f"https://zenodo.org/api/records/{rid}"
            row = {"id": rid, "title": title, "description": "", "publication_date": "", "status": 0}
            for attempt in range(3):
                try:
                    r = sess.get(url, timeout=30)
                    row["status"] = r.status_code
                    if r.status_code == 200:
                        md = r.json().get("metadata", {})
                        row["description"] = strip_html(md.get("description", ""))
                        row["publication_date"] = md.get("publication_date", "")
                        if not row["title"]:
                            row["title"] = md.get("title", "")
                        break
                    if r.status_code == 429:
                        time.sleep(30 * (attempt + 1))
                        continue
                    break
                except Exception as e:  # noqa: BLE001
                    row["status"] = -1
                    row["error"] = repr(e)[:120]
                    time.sleep(5)
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            n_ok += row["status"] == 200
            n_fail += row["status"] != 200
            if (k + 1) % 100 == 0:
                print(f"  {k + 1}/{len(todo)} fetched, {n_ok} ok, {n_fail} failed, {time.strftime('%H:%M:%S')}", flush=True)
            time.sleep(args.sleep)
    print(f"done: {n_ok} ok, {n_fail} failed", flush=True)


if __name__ == "__main__":
    main()
