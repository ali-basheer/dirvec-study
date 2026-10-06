#!/usr/bin/env python3
"""Check that a prose revision of a LaTeX paper changed no number, citation or cross-reference.

Compares two versions of the file section by section (split at \\section): the multiset of numbers,
of citation keys and of \\ref labels must be equal in every section. Numbers inside citation keys,
labels and macro names are ignored. Order changes inside a section are reported as a note, not a
failure (a restructured sentence may move a number).

Usage: python3 scripts/numcheck.py OLD.tex NEW.tex          (or OLD as a git revision: rev:paper/main.tex)
"""
import re
import subprocess
import sys
from collections import Counter

NUM = re.compile(r"(?<![A-Za-z\\@_\d.])[-+]?\d+(?:,\d{3})*(?:\.\d+)?")


def load(spec):
    if spec.startswith("rev:"):
        rev, path = spec[4:].split(":", 1)
        return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    return open(spec, encoding="utf-8").read()


def sections(tex):
    body = tex[tex.find("\\begin{document}"):]
    body = re.sub(r"(?<!\\)%.*", "", body)
    parts = re.split(r"\\section\*?\{", body)
    out = []
    for p in parts:
        title = p.split("}", 1)[0][:50] if out else "(front matter)"
        cites = re.findall(r"\\cite[tp]?\*?\{([^}]*)\}", p)
        keys = [k.strip() for c in cites for k in c.split(",")]
        refs = re.findall(r"\\(?:eq)?ref\{([^}]*)\}", p)
        stripped = re.sub(r"\\(?:cite[tp]?\*?|ref|eqref|label|includegraphics(?:\[[^\]]*\])?|bibliography(?:style)?)\{[^}]*\}", " ", p)
        stripped = re.sub(r"\\[A-Za-z]+", " ", stripped)  # macro names
        nums = NUM.findall(stripped)
        out.append({"title": title, "nums": nums, "cites": keys, "refs": refs})
    return out


def main():
    old, new = sections(load(sys.argv[1])), sections(load(sys.argv[2]))
    ok = True
    if len(old) != len(new):
        print(f"FAIL: {len(old)} sections before, {len(new)} after")
        sys.exit(1)
    for a, b in zip(old, new):
        for what in ("nums", "cites", "refs"):
            ca, cb = Counter(a[what]), Counter(b[what])
            if ca != cb:
                ok = False
                print(f"FAIL [{b['title']}] {what}: removed {dict(ca - cb)}, added {dict(cb - ca)}")
            elif a[what] != b[what]:
                print(f"note [{b['title']}] {what}: same items, order changed")
    tot = sum(len(s["nums"]) for s in new)
    print(("OK" if ok else "FAILED") + f": {len(new)} sections, {tot} numbers, "
          f"{sum(len(s['cites']) for s in new)} citations, {sum(len(s['refs']) for s in new)} references compared")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
