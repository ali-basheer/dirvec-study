#!/usr/bin/env python3
"""Blank every number in paper/main.tex for a blind number audit.

A checker who has not seen the draft gets the draft's sentences with every number replaced by a
numbered blank and refills the blanks from results/, BRIEF.md, scripts/ and data/.
scripts/audit_compare.py then compares the refilled numbers with the draft's.

Writes into --out (keep that directory away from the checker, hand over cloze.txt only):
  cloze.txt   one unit (sentence or table row) per line, numbers as [[B001]], number words as [[WORD]]
  key.json    blank id -> the number as the draft prints it
  units.json  every unit with its blank ids and whether it is in cloze.txt

With --since <git rev>, cloze.txt holds only the units that are not in that revision of the draft
(for re-checking a revised draft). Blank ids count over the whole text either way.
With --word-ids, the number words of the units in cloze.txt get ids of their own ([[W001]], ...) and
wkey.json holds them, so a checker's words can be compared too (a count of sessions or of questions
is a number). With --context, a unit in cloze.txt is preceded by its section and paragraph headings
when they are not in cloze.txt themselves, and a table with a row in cloze.txt keeps its other rows,
all marked "[context]"; a checker then knows which encoder a table block belongs to.

Usage: python scripts/audit_cloze.py --out /somewhere/private [--since 3dd2aef] [--tex paper/main.tex]
                                     [--word-ids] [--context]
"""
import argparse
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = (r"\b(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
         r"seventeen|eighteen|nineteen|twenty|half|halved|third|thirds|quarter|quarters|fifth|tenth|twice)\b")
KEEP = r"two-stage|two-vector|one-vector|single-vector|two-centroid|two-fold|five-cell"


def plain(src):
    """LaTeX to readable text; tables become rows ending in ';;' with cells separated by '|'."""
    t = src[src.index(r"\begin{abstract}"):src.index(r"\end{document}")]
    t = re.sub(r"\\bibliographystyle\{.*?\}|\\bibliography\{.*?\}", "", t)
    t = re.sub(r"\\label\{[^}]*\}", "", t)
    t = re.sub(r"~?\\ref\{([^}]*)\}", lambda m: " <ref:%s>" % m.group(1), t)
    t = re.sub(r"\\cite[pt]\{([^}]*)\}", "<cite>", t)
    t = re.sub(r"\\ci\{([^}]*)\}\{([^}]*)\}", r"[\1, \2]", t)
    t = re.sub(r"\\rep\{([^}]*)\}", r"`\1`", t)
    t = re.sub(r"\\textsubscript\{([^}]*)\}", r"_\1", t)
    t = re.sub(r"\\(textbf|emph|texttt|paragraph|section|caption)\{",
               lambda m: {"paragraph": "\n### ", "section": "\n## ", "caption": "CAPTION: "}.get(m.group(1), ""), t)
    t = re.sub(r"\\multicolumn\{\d+\}\{[^}]*\}\{", "", t)
    t = re.sub(r"\\cmidrule\([^)]*\)\{[^}]*\}", "", t)
    t = re.sub(r"\\(toprule|midrule|bottomrule|centering|small|scriptsize|maketitle|appendix)\b", "", t)
    t = re.sub(r"\\setlength\{\\tabcolsep\}\{[^}]*\}", "", t)
    t = re.sub(r"\\resizebox\{\\textwidth\}\{!\}\{%", "", t)
    t = re.sub(r"\\begin\{tabular\}\{[^}]*\}", "TABLE:", t)
    t = re.sub(r"\\end\{tabular\}\}?", "END TABLE", t)
    t = re.sub(r"\\begin\{table\}\[t\]|\\end\{table\}", "", t)
    t = re.sub(r"\\begin\{figure\}\[t\]|\\end\{figure\}", "", t)  # figures: only the caption is text
    t = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", "", t)
    t = re.sub(r"\\(begin|end)\{(abstract|enumerate|itemize|description)\}", "", t)
    t = re.sub(r"\\item\[([^\]]*)\]", r"\n- [\1]", t)
    t = t.replace(r"\item", "\n-").replace("\\\\", " ;;\n").replace("&", "|")
    t = re.sub(r"\\footnote\{", " (footnote: ", t)
    t = t.replace(r"\_", "_").replace(r"\,", " ").replace(r"\%", "%")
    for a, b in ((r"\lceil", "ceil("), (r"\rceil", ")"), (r"\min", "min"), (r"\mu", "mu"), (r"\alpha", "alpha"),
                 (r"\in", "in"), (r"\mathrm", "")):
        t = t.replace(a, b)
    t = t.replace("$", "").replace("{", "").replace("}", "")
    return re.sub(r"[ \t]+", " ", t)


def units(t):
    out = []
    for line in t.split("\n"):
        line = line.strip()
        if line:
            out += [u.strip() for u in re.split(r"(?<=[.?!])\s+(?=[A-Z`(\[])", line) if u.strip()]
    return out


def blank_all(us, word_ids=None):
    """Blank numbers (keyed) and number words unit by unit with one running counter.

    word_ids: None, or one flag per unit; the number words of a flagged unit get ids and go into wkey.
    """
    key, wkey, rows = {}, {}, []
    num = re.compile(r"(?<![A-Za-z@_\d.\x00])[+\-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![A-Za-z\d])")
    for n, u in enumerate(us):
        protect = {}

        def prot(m):
            k = "\x00%d\x00" % len(protect)
            protect[k] = m.group(0)
            return k

        s = re.sub(r"\[0,\s?\.2\)|\[\.2,\s?\.5\)|\[\.5,\s?\.8\)|\[\.8,\s?1\]|\[0\.2, 0\.5\)", prot, u)
        s = re.sub(r"<ref:[^>]*>|hnswlib \d+\.\d+\.\d+|an idea from 1991|" + KEEP, prot, s)
        s = re.sub(r"(?i)(sessions? )(\d+)((,? \d+)*( to \d+| and \d+)*)", prot, s)
        ids = []

        def blank(m):
            bid = "B%03d" % (len(key) + 1)
            key[bid] = m.group(0)
            ids.append(bid)
            return "[[%s]]" % bid

        s = num.sub(blank, s)
        wids = []

        def wblank(m):
            if not (word_ids and word_ids[n]):
                return "[[WORD]]"
            wid = "W%03d" % (len(wkey) + 1)
            wkey[wid] = m.group(0)
            wids.append(wid)
            return "[[%s]]" % wid

        s = re.sub(WORDS, wblank, s, flags=re.I)
        for k, v in protect.items():
            s = s.replace(k, v)
        rows.append({"text": s, "ids": ids, "wids": wids})
    return key, rows, wkey


def with_context(us, rows):
    """The lines of cloze.txt with headings and table rows added as context for the shown units."""
    out, sec, par, last = [], None, None, (None, None)
    table = None
    for u, r in zip(us, rows):
        if u.startswith("## "):
            sec, par = r["text"], None
        elif u.startswith("### "):
            par = r["text"]
        if u.startswith("TABLE:"):
            table = []
        if table is not None:
            table.append(r)
            if "END TABLE" in u:
                if any(x["shown"] for x in table):
                    out += [x["text"] if x["shown"] else "[context] " + re.sub(r"\[\[B\d+\]\]", "[[...]]", x["text"])
                            for x in table]
                table = None
            continue
        if r["shown"]:
            if (sec, par) != last and not u.startswith("#"):
                if sec != last[0]:
                    out.append("[context] " + (sec or "## Abstract"))
                if par:
                    out.append("[context] " + par)
            elif sec is None and not out:
                out.append("[context] ## Abstract")
            last = (sec, par)
            out.append(r["text"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="paper/main.tex")
    ap.add_argument("--out", required=True)
    ap.add_argument("--since", default=None, help="git revision; write only the units that are not in it")
    ap.add_argument("--word-ids", action="store_true", help="give the number words of the written units ids (wkey.json)")
    ap.add_argument("--context", action="store_true", help="add headings and table rows as [context] lines")
    args = ap.parse_args()
    new = units(plain(open(os.path.join(ROOT, args.tex), encoding="utf-8").read()))
    old = set()
    if args.since:
        src = subprocess.run(["git", "-C", ROOT, "show", f"{args.since}:{args.tex}"], capture_output=True,
                             text=True, check=True).stdout
        old = set(units(plain(src)))
    flags = [u not in old for u in new]
    key, rows, wkey = blank_all(new, flags if args.word_ids else None)
    for r, f in zip(rows, flags):
        r["shown"] = f
    os.makedirs(args.out, exist_ok=True)
    shown = sum(len(r["ids"]) for r in rows if r["shown"])
    lines = with_context(new, rows) if args.context else [r["text"] for r in rows if r["shown"]]
    with open(os.path.join(args.out, "cloze.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    json.dump(key, open(os.path.join(args.out, "key.json"), "w"), indent=0)
    json.dump(rows, open(os.path.join(args.out, "units.json"), "w"), indent=0, ensure_ascii=False)
    if args.word_ids:
        json.dump(wkey, open(os.path.join(args.out, "wkey.json"), "w"), indent=0)
    print(f"{len(key)} blanks in {len(new)} units; {sum(r['shown'] for r in rows)} units and {shown} blanks written to cloze.txt"
          + (f"; {len(wkey)} number words keyed" if args.word_ids else ""))


if __name__ == "__main__":
    main()
