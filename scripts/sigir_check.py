#!/usr/bin/env python3
"""Check the SIGIR version (paper/sigir/main.tex) against the long version (paper/main.tex).

The SIGIR text is the long version cut down by deletion, so the long version's audits cover it as
far as its sentences are the long version's. This script says how far that is.

1. Every unit (sentence, caption, table row, as scripts/audit_cloze.py cuts them) is put in one class:
     same     word for word a unit of the long version
     cut      a unit of the long version with words deleted and nothing added or reordered
     other    anything else: these are listed and have to be checked against the record by hand or
              by a blind checker (--cloze DIR writes the cut and the other units as a cloze, as
              audit_cloze.py does)
   For "cut" and "other" units every number must occur in the long version or in one of the record
   files given; a number found nowhere stops the script.
2. The table of cells (tab:cells) is set one encoder per block here and two encoders wide in the long
   version; every row of it here must equal the long version's row for the same encoder and
   representation, number by number. A row that is not a representation (file names) is checked as
   an ordinary unit in step 1.
3. No em or en dash and no "--" in the source; no author name, affiliation, address or repository
   address (the submission is anonymous).
4. With --pdf: the body (everything before the references) must end on page 9 or before.

Usage: python3 scripts/sigir_check.py [record file ...] [--pdf build/sigir/dirvec_sigir_review.pdf]
                                      [--list] [--cloze DIR]
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import audit_cloze as ac  # noqa: E402

NUM = re.compile(r"(?<![A-Za-z@_\d.])[+\-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![A-Za-z\d])")
IDENT = r"Basheer|basheerali|Craftpine|alisons|ali-basheer|Toronto|github\.com"
PAGES = 9


def sigir_plain(src):
    """The SIGIR source in the form audit_cloze.plain() expects of the long version."""
    src = re.sub(r"\\begin\{CCSXML\}.*?\\end\{CCSXML\}", "", src, flags=re.S)
    src = re.sub(r"\\ccsdesc\[\d+\]\{[^}]*\}|\\keywords\{[^}]*\}", "", src)
    src = re.sub(r"\\(begin|end)\{(figure|table)\*\}", r"\\\1{\2}", src)
    src = src.replace("\\resizebox{\\columnwidth}", "\\resizebox{\\textwidth}")
    m = re.search(r"\\newcommand\{\\anonrepo\}\{(.*)\}", src)
    src = src.replace("\\anonrepo", m.group(1)) if m else src
    return ac.plain(src)


def words(u):
    return re.findall(r"\S+", u)


def is_cut(short, long_):
    """True if the words of `short` are a subsequence of the words of `long_` (punctuation at a cut ignored)."""
    norm = lambda w: w.strip(".,;:()")  # noqa: E731
    it = iter(norm(w) for w in words(long_))
    return all(any(norm(w) == x for x in it) for w in words(short) if norm(w))


def cells(tex):
    """tab:cells as {(encoder, representation): [five numbers]}."""
    i = tex.index("\\label{tab:cells}")
    block = tex[i: tex.index("\\end{tabular}", i)]
    out, order = {}, []
    for line in block.splitlines():
        heads = re.findall(r"\\multicolumn\{\d+\}\{[lc]\}\{(E\d)", line)
        if heads:
            order = heads
            continue
        m = re.match(r"\\rep\{(\w+)\}[^&]*\(([\d.]+)\) & (.*)\\\\", line.strip())
        if m and order:
            vals = [x.strip() for x in m.group(3).split("&")]
            for k, enc in enumerate(order):
                out[(enc, m.group(1))] = [m.group(2)] + vals[5 * k: 5 * k + 5]
    return out


def body_end(pdf):
    """(page, column, fraction of the column) where the reference list starts."""
    x = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    for n, page in enumerate(x.split("<page ")[1:], 1):
        m = re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>(?:REFERENCES|References)</word>', page)
        if m:
            ys = [float(y) for xm, y in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)"', page)
                  if 50 < float(xm) < 300 and float(y) > 75]
            col = 1 if float(m.group(1)) < 300 else 2
            first = col == 1 and float(m.group(2)) <= min(ys) + 1
            return n, col, first
    return None


def main():
    args = sys.argv[1:]
    show = "--list" in args
    args = [a for a in args if a != "--list"]
    pdf = cloze = None
    for flag in ("--pdf", "--cloze"):
        if flag in args:
            i = args.index(flag)
            val, args = args[i + 1], args[:i] + args[i + 2:]
            pdf, cloze = (val, cloze) if flag == "--pdf" else (pdf, val)
    stex = open(os.path.join(ROOT, "paper", "sigir", "main.tex"), encoding="utf-8").read()
    ltex = open(os.path.join(ROOT, "paper", "main.tex"), encoding="utf-8").read()
    lplain = ac.plain(ltex)
    lunits = ac.units(lplain)
    lset = set(lunits)
    sunits = ac.units(sigir_plain(stex))
    rec = "\n".join(open(f, encoding="utf-8").read() for f in args)
    rec_plain = rec.replace(",", "")
    bad = 0

    # 1. classes
    klass, missing = [], []
    in_cells = False
    for u in sunits:
        if u.startswith(("CAPTION: Recall@5 on the S11 evaluation split", "CAPTION: Recall@5 on the confirmation set")):
            in_cells = True                      # the rows that follow are compared in step 2
        if u in lset:
            klass.append("same")
        elif (in_cells and u.endswith(";;") and (u.lstrip("| ").startswith("`") or not NUM.search(u))) \
                or u.startswith(("TABLE:", "END TABLE")):
            klass.append("table")
            in_cells = in_cells and not u.startswith("END TABLE")
        elif any(is_cut(u, v) for v in lunits if len(v) >= len(u)):
            klass.append("cut")
        else:
            klass.append("other")
        if klass[-1] in ("cut", "other"):
            for m in NUM.finditer(re.sub(r"<ref:[^>]*>", " ", u)):
                n = m.group(0)
                bare = n.replace(",", "")
                cands = {n, bare, n.lstrip("+"), bare.lstrip("+")}
                if not any(c in lplain or c in rec or c in rec_plain for c in cands):
                    missing.append((n, u[:110]))
    count = {k: klass.count(k) for k in ("same", "cut", "other", "table")}
    print(f"{len(sunits)} units: {count['same']} word for word in the long version, {count['cut']} cut from one of "
          f"its units, {count['other']} other, {count['table']} rows of the table of cells")
    print(f"numbers of the cut and other units found neither in the long version nor in the record files: {len(missing)}")
    for n, u in missing:
        print("   MISSING", n, "|", u)
    bad += len(missing)
    if show:
        for k in ("other", "cut"):
            for u, c in zip(sunits, klass):
                if c == k:
                    print(f"  [{k}] {u}")

    # 2. the table of cells
    a, b = cells(stex), cells(ltex)
    diff = [k for k in sorted(a) if a.get(k) != b.get(k)]
    print(f"table of cells: {len(a)} rows by encoder here, {len(b)} in the long version, {len(diff)} of these differ")
    for k in diff:
        print("   DIFFERS", k, a.get(k), b.get(k))
    bad += len(diff) + (0 if len(b) == 32 and a and set(a) <= set(b) else 1)

    # 3. dashes and identity
    lines = stex.split("\n")
    dash = [ln for ln in lines if re.search(r"[–—]", ln) or ("--" in ln and not ln.lstrip().startswith("%"))]
    ident = [ln[:90] for ln in lines if re.search(IDENT, ln) and "anthropic" not in ln.lower()]
    print(f"lines with a dash: {len(dash)}; lines that name the author, the affiliation or the repository: {len(ident)}")
    for ln in ident:
        print("   IDENT", ln)
    bad += len(dash) + len(ident)

    # 4. the page limit
    if pdf:
        end = body_end(pdf)
        ok = end is not None and (end[0] <= PAGES or (end[0] == PAGES + 1 and end[2]))
        print(f"references start on page {end[0]}, column {end[1]}" + (", at its top" if end[2] else "") + ": "
              + ("the body ends on page %d or before" % PAGES if ok else "THE BODY RUNS PAST PAGE %d" % PAGES))
        bad += 0 if ok else 1

    # a cloze of the units that are not word for word the long version's, for a checker who has not seen the draft
    if cloze:
        flags = [c in ("cut", "other") for c in klass]
        key, rows, wkey = ac.blank_all(sunits, flags)
        for r, f in zip(rows, flags):
            r["shown"] = f
        os.makedirs(cloze, exist_ok=True)
        with open(os.path.join(cloze, "cloze.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(ac.with_context(sunits, rows)) + "\n")
        json.dump(key, open(os.path.join(cloze, "key.json"), "w"), indent=0)
        json.dump(rows, open(os.path.join(cloze, "units.json"), "w"), indent=0, ensure_ascii=False)
        json.dump(wkey, open(os.path.join(cloze, "wkey.json"), "w"), indent=0)
        print(f"cloze: {sum(flags)} units, {sum(len(r['ids']) for r in rows if r['shown'])} blanks, "
              f"{len(wkey)} number words, in {cloze}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
