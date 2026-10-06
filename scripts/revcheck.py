#!/usr/bin/env python3
"""Number check of a content revision of paper/main.tex against a base revision.

scripts/numcheck.py is for a prose pass, where no number may change. This script is for a revision
that adds or changes results. It does not replace the blind audit (scripts/audit_cloze.py): it only
says where the numbers moved and whether every added number occurs in the record at all.

1. Per section (matched by title): the numbers, citation keys and \\ref labels removed and added.
2. Every unit (sentence or table row, as scripts/audit_cloze.py cuts them) that is not in the base
   revision: each of its numbers must occur in one of the record files given, or in the base draft,
   or be listed with --allow (numbers taken from cited documentation and not from the record).
3. Dashes in the added units and in the source; the length of the abstract as plain text.

Usage: python3 scripts/revcheck.py <base git rev> [record file ...] [--allow 64 4,096 ...] [--dump]
       (--dump prints the added and the removed units)
"""
import os
import re
import subprocess
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import audit_cloze  # noqa: E402
import numcheck  # noqa: E402

NUM = re.compile(r"(?<![A-Za-z@_\d.])[+\-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![A-Za-z\d])")


def main():
    args = sys.argv[1:]
    dump = "--dump" in args
    args = [a for a in args if a != "--dump"]
    allow = set()
    if "--allow" in args:
        i = args.index("--allow")
        allow, args = set(args[i + 1:]), args[:i]
    if not args:
        sys.exit(__doc__)
    base_rev, rec_files = args[0], args[1:]
    old = subprocess.run(["git", "-C", ROOT, "show", f"{base_rev}:paper/main.tex"], capture_output=True,
                         text=True, check=True).stdout
    new = open(os.path.join(ROOT, "paper", "main.tex"), encoding="utf-8").read()

    # 1. per section
    so = {s["title"]: s for s in numcheck.sections(old)}
    sn = {s["title"]: s for s in numcheck.sections(new)}
    print("== sections:", len(so), "before,", len(sn), "after; new:", [t for t in sn if t not in so],
          "gone:", [t for t in so if t not in sn])
    for title, b in sn.items():
        a = so.get(title, {"nums": [], "cites": [], "refs": []})
        for what in ("nums", "cites", "refs"):
            ca, cb = Counter(a[what]), Counter(b[what])
            if ca != cb:
                rem, add = dict(ca - cb), dict(cb - ca)
                shown = f": {add}" if what != "nums" or len(add) < 25 else ""
                print(f"[{title}] {what}: removed {rem if rem else '-'}; added {len(add)} distinct{shown}")

    # 2. the units that are not in the base, and their numbers
    uo = set(audit_cloze.units(audit_cloze.plain(old)))
    un = audit_cloze.units(audit_cloze.plain(new))
    added = [u for u in un if u not in uo]
    removed = [u for u in uo if u not in set(un)]
    print(f"\n== units: {len(un)} now, {len(added)} not in the base, {len(removed)} of the base gone")
    rec = "\n".join(open(f, encoding="utf-8").read() for f in rec_files)
    rec_plain = rec.replace(",", "")
    oldplain = audit_cloze.plain(old)
    missing, total, distinct = [], 0, set()
    for u in added:
        for m in NUM.finditer(re.sub(r"<ref:[^>]*>", " ", u)):
            n = m.group(0)
            total += 1
            distinct.add(n)
            bare = n.replace(",", "")
            cands = {n, bare, n.lstrip("+"), bare.lstrip("+")}
            if not (any(c in rec or c in rec_plain for c in cands) or any(c in oldplain for c in cands)
                    or n in allow):
                missing.append((n, u[:110]))
    print(f"numbers in the added units: {total} ({len(distinct)} distinct); not found in the record files, "
          f"the base draft or the --allow list: {len(missing)}")
    for n, u in missing:
        print("   MISSING", n, "|", u)

    # 3. dashes and the abstract
    bad = [u for u in added if re.search(r"[–—]|--", u)]
    print(f"\n== added units with an em or en dash or a double hyphen: {len(bad)}")
    raw_bad = [ln for ln in new.split("\n")
               if re.search(r"[–—]", ln) or ("--" in ln and not ln.lstrip().startswith("%"))]
    print("lines of main.tex with a dash:", len(raw_bad))
    a = new[new.index("\\begin{abstract}") + len("\\begin{abstract}"):new.index("\\end{abstract}")]
    a = re.sub(r"\s+", " ", a.strip().replace("$k$", "k"))
    print("abstract:", len(a), "characters as plain text (arXiv's limit is 1,920)")
    if dump:
        for u in added:
            print("  +", u)
        for u in removed:
            print("  -", u)
    if missing or bad or raw_bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
