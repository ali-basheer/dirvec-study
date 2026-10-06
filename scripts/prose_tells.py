#!/usr/bin/env python3
"""Count the tells of machine-drafted prose in the units of paper/main.tex that a revision added.

A unit is a sentence, a caption or a list item, as scripts/audit_cloze.py cuts them; table rows are
left out. The counts are a worklist for a prose pass and not a verdict: a colon after "Kill" in the
appendix or a contrast that is the finding stays. After the pass, scripts/numcheck.py has to show
that no number, citation or reference changed.

Usage: python3 scripts/prose_tells.py <base git rev> [--list]      (--list prints the units behind each count)
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import audit_cloze as ac  # noqa: E402

INFLATED = (r"\b(delve|underscore|highlight\w*|pivotal|crucial|landscape|realm|tapestry|intricate|multifaceted|"
            r"nuanced|comprehensive|holistic|robust\w*|leverag\w*|utiliz\w*|utilis\w*|facilitat\w*|foster\w*|"
            r"showcas\w*|seamless\w*|paramount|meticulous\w*|novel)\b")
SIGNPOST = (r"\b(In this section|We now turn|It is worth noting|Importantly|Notably|Crucially|Interestingly|Indeed|"
            r"In other words|It should be noted)\b")


def prose_words(u):
    """Words of prose in a unit; numbers, intervals, citations, references and representation names do not count."""
    s = re.sub(r"\[[^\]]*\]|<cite>|<ref:[^>]*>|`[^`]*`", " ", u)
    s = re.sub(r"[-+]?\d[\d,.]*", " ", s)
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))


def verdict_line(u):
    return u.startswith(("- [", "Survived", "Dead", "Split"))


TELLS = {
    "dashes": lambda u: len(re.findall(r"[–—]|--| - ", u)),
    "semicolons": lambda u: 1 if ";" in u and not verdict_line(u) else 0,
    "semicolons in appendix entries": lambda u: 1 if ";" in u and verdict_line(u) else 0,
    "colons before a clause": lambda u: len(re.findall(
        r"(?<![\]\)\d]):\s+[a-z`]", re.sub(r"^\- \[[^\]]*\]", "", re.sub(r"^CAPTION:", "", u)))),
    "contrast pairs (X, not Y; and not; rather than; instead of)": lambda u: len(re.findall(
        r", not |\band not\b|\bnot \w+ but\b|\brather than\b|\binstead of\b", u)),
    "signposts": lambda u: len(re.findall(SIGNPOST, u)),
    "inflated words": lambda u: len(re.findall(INFLATED, u, flags=re.I)),
    "hedge stacks": lambda u: len(re.findall(r"\b(may|might|could)\s+(potentially|possibly|perhaps)\b", u, flags=re.I)),
    "rhetorical questions": lambda u: u.count("?"),
    "more than two parenthetical groups with numbers": lambda u: 1 if len(re.findall(r"\([^()]*\d[^()]*\)", u)) > 2 else 0,
    "sentences over 40 words of prose": lambda u: 1 if prose_words(u) > 40 else 0,
}


def main():
    args = [a for a in sys.argv[1:] if a != "--list"]
    if len(args) != 1:
        sys.exit(__doc__)
    old = subprocess.run(["git", "-C", ROOT, "show", f"{args[0]}:paper/main.tex"], capture_output=True, text=True,
                         check=True).stdout
    tex = open(os.path.join(ROOT, "paper", "main.tex"), encoding="utf-8").read()
    base = set(ac.units(ac.plain(old)))
    units = [u for u in ac.units(ac.plain(tex))
             if u not in base and not u.endswith(";;") and not u.startswith(("TABLE", "END TABLE"))]
    print(len(units), "units of prose added since", args[0])
    for name, count in TELLS.items():
        hits = [(u, count(u)) for u in units if count(u)]
        print(f"{sum(h for _, h in hits):3d}  {name}")
        if "--list" in sys.argv:
            for u, _ in hits:
                print("       *", u[:400])


if __name__ == "__main__":
    main()
