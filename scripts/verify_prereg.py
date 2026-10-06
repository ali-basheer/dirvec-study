#!/usr/bin/env python3
"""Check the timestamped pre-registrations without the history of the working repository.

prereg/sessionNN_commit.txt holds the identifier of the commit of the working repository in which a
brief was registered, and prereg/sessionNN_commit.txt.ots its OpenTimestamps proof. Check a proof with
the OpenTimestamps client:

  ots verify prereg/session19_commit.txt.ots

prereg/objects/ holds the git objects needed to check, from the identifier alone, what that commit
contained: the commit, its root tree and the registered files. This script recomputes the identifier of
every object, reads the brief out of each commit and compares it with BRIEF.md.

  python3 scripts/verify_prereg.py
"""
import datetime
import difflib
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJ = os.path.join(ROOT, "prereg", "objects")
EXTRA = {"session24_pool_commit.txt": ["scripts/pool.py"],
         "session27_commit.txt": ["scripts/s27.py", "scripts/humanq_tool.py"],
         "session27_amend_commit.txt": ["scripts/s27.py", "data/simq_s11.jsonl"]}   # files registered with a commit besides BRIEF.md


def load(name, kind):
    """The object `name` of type kind (commit, tree, blob), after checking that it hashes to its name."""
    data = open(os.path.join(OBJ, f"{name}.{kind}"), "rb").read()
    got = hashlib.sha1(b"%s %d\0" % (kind.encode(), len(data)) + data).hexdigest()
    if got != name:
        sys.exit(f"FAILED: prereg/objects/{name}.{kind} hashes to {got}")
    return data


def entries(tree):
    out, i = {}, 0
    while i < len(tree):
        j = tree.index(b"\0", i)
        name = tree[i:j].split(b" ", 1)[1].decode()
        out[name] = tree[j + 1:j + 21].hex()
        i = j + 21
    return out


def file_at(tree, path):
    parts = path.split("/")
    for d in parts[:-1]:
        tree = load(entries(tree)[d], "tree")
    return load(entries(tree)[parts[-1]], "blob")


def main():
    brief = open(os.path.join(ROOT, "BRIEF.md"), "rb").read()
    proofs = sorted(f for f in os.listdir(os.path.join(ROOT, "prereg")) if f.endswith("_commit.txt"))
    for f in proofs:
        h = open(os.path.join(ROOT, "prereg", f)).read().strip()
        commit = load(h, "commit")
        tree = load(re.search(rb"^tree ([0-9a-f]{40})$", commit, re.M).group(1).decode(), "tree")
        t = re.search(rb"^committer .* (\d+) [+-]\d{4}$", commit, re.M).group(1)
        when = datetime.datetime.fromtimestamp(int(t), datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        subject = commit.split(b"\n\n", 1)[1].split(b"\n", 1)[0].decode()
        print(f"{f}: commit {h[:12]}, {when}")
        print(f"  {subject[:150]}")
        old = file_at(tree, "BRIEF.md")
        if brief.startswith(old):
            print(f"  BRIEF.md at that commit is the first {len(old):,} bytes of the current BRIEF.md, unchanged.")
        else:
            a = old.decode().splitlines()
            b = brief.decode().splitlines()
            sm = difflib.SequenceMatcher(None, a, b[:len(a) + 50], autojunk=False)
            changed = [(i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal" and i1 < len(a)]
            n = sum(i2 - i1 for i1, i2, _, _ in changed)
            print(f"  BRIEF.md at that commit ({len(a):,} lines): {n} of its lines read differently in the current BRIEF.md:")
            for i1, i2, j1, j2 in changed:
                for k in range(i1, i2):
                    print(f"    then: {a[k][:140]}")
                for k in range(j1, min(j2, j1 + (i2 - i1) + 2)):
                    print(f"    now:  {b[k][:140]}")
        for p in EXTRA.get(f, []):
            same = file_at(tree, p) == open(os.path.join(ROOT, p), "rb").read()
            print(f"  {p} at that commit {'is the current file, unchanged' if same else 'differs from the current file'}.")
    print(f"{len(proofs)} commits checked: every object hashes to its identifier.")


if __name__ == "__main__":
    main()
