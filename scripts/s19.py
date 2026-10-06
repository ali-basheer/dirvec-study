#!/usr/bin/env python3
"""dirvec session 19: the minority-modality loss on directories of GitHub repositories (BRIEF.md, session 19).

  corpus          counts of the pool, the harvest, the eligible directories and the scored set
  validity        H19a, H19b, H19c and the secondaries, from eval.py's rank files (nothing is embedded)
  commitq build   the commit-subject query set -> data/commitq_s19.jsonl
  commitq embed   embed that set with one encoder -> data/emb/<emb>/commitq_s19.npz
  commitq eval    H19d and its secondaries

  s19.py corpus > corpus.md
  s19.py validity --ranks E1=data/emb/jina-embeddings-v4_s19/ranks_s19_e1.jsonl[,E4=...]
                  --index data/emb/jina-embeddings-v4_s19/index.jsonl --evalmd E1=<eval.py output>[,E4=...]
  s19.py commitq build
  s19.py commitq embed --model jina-embeddings-v4 --emb jina-embeddings-v4_s19
  s19.py commitq eval  --model jina-embeddings-v4 --emb jina-embeddings-v4_s19 --enc E1

An owner is the account that holds the repository (lowercased). Intervals marked owner-clustered
resample owners, 1,000 times, and recompute the statistic over all queries of the drawn owners; the
owner-weighted estimate gives every owner the same weight. Both are validity.py's boot_mean, as in
session 17, with the owner in place of the creator family. The directory bootstrap printed beside
them is eval.py's (same cells, same seeds), and `validity` stops with exit code 3 before any new
number if it does not reproduce eval.py's printed intervals of c - a.
"""
import argparse
import gzip
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402
from validity import (boot_mean, cells_of, eff_families, fmt, name_baseline, stem_ext,  # noqa: E402
                      SEEDS, CLUSTER_OFFSET)

ROOT = ev.ROOT
SFX = os.environ.get("S19_SFX", "_s19")   # the self-test (scripts/s19_selftest.py) runs on a _t19 copy
LO_B, HI_B = ["[0,.2)", "[.2,.5)"], ["[.5,.8)", "[.8,1]"]
SIZE_BINS = [("3 to 10", 3, 10), ("11 to 30", 11, 30), ("31 to 100", 31, 10 ** 9)]
SIB_BINS = [("none", 0, 0), ("1 or 2", 1, 2), ("3 or more", 3, 10 ** 9)]
DEPTH_BINS = [("root", 0, 0), ("depth 1", 1, 1), ("depth 2 or more", 2, 10 ** 9)]
MARGIN = 0.02
SESOI = 0.05
MIN_OWNERS = 100
CODE_EXT = set("py r jl m c h cpp hpp java js ts sh sql lean ipynb rmd qmd".split())
CONFIG_EXT = set("json xml yaml yml toml ini cfg log cff bib".split())
CQ_ROWS = ["a", "ac", "c", "cc", "d", "dc"]
CQ_MAX_PER_DIR = 3
CQ_MIN_WORDS = 4
CQ_GATE = 0.10
CQ_STOP_EXACT = {"add files via upload", "initial commit", "first commit"}
CQ_STOP_PREFIX = ("merge ", "revert ")
STRIP = ".,:;!?()[]{}<>\"'`*#"


def load(path):
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    if not os.path.exists(p) and os.path.exists(p + ".gz"):
        with gzip.open(p + ".gz", "rt") as fh:
            return [json.loads(l) for l in fh if l.strip()]
    with open(p) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def pairs(arg):
    return dict(item.split("=", 1) for item in arg.split(",")) if arg else {}


def binned(x, bins):
    return [(name, (x >= lo) & (x <= hi)) for name, lo, hi in bins]


def oboot(z, owners, seed, B=10000):
    """The registered estimator: the mean over owners of each owner's mean of z, with percentile
    intervals from B resamples of the owners. Returns (point, (lo95, hi95), (lo98, hi98), owners);
    the second interval is the 98.33 percent one (Bonferroni for the three primary tests)."""
    keys = sorted(set(owners))
    gi = {k: i for i, k in enumerate(keys)}
    g = np.array([gi[k] for k in owners])
    gm = np.bincount(g, weights=z, minlength=len(keys)) / np.bincount(g, minlength=len(keys))
    rng = np.random.default_rng(seed)
    bs = np.empty(B)
    for i0 in range(0, B, 1000):
        idx = rng.integers(0, len(keys), size=(min(1000, B - i0), len(keys)))
        bs[i0:i0 + len(idx)] = gm[idx].mean(axis=1)
    q = np.percentile(bs, [2.5, 97.5, 100 * 0.05 / 6, 100 * (1 - 0.05 / 6)])
    return float(gm.mean()), (float(q[0]), float(q[1])), (float(q[2]), float(q[3])), len(keys)


def outcome(lo, hi, n_owners):
    """The four registered outcomes of a loss, read on an interval [lo, hi]."""
    if n_owners < MIN_OWNERS:
        return f"inconclusive (fewer than {MIN_OWNERS} owners)"
    if lo >= SESOI:
        return "confirmed (lower bound at or above +0.05)"
    if hi < SESOI:
        return "below +0.05 (upper bound under +0.05)"
    if lo > 0:
        return "present, size open (lower bound above zero)"
    return "inconclusive"


def kind_of(path, modality):
    """image, code, config, prose or table: a finer label for reporting only (the representations
    use the manifest's modality labels, as in every other session)."""
    if modality in ("image", "pdf_scanned"):
        return "image"
    if modality == "table":
        return "table"
    ext = stem_ext(path)[1]
    if ext in CODE_EXT:
        return "code"
    if ext in CONFIG_EXT:
        return "config"
    return "prose"


# ---------------------------------------------------------------- corpus

def cmd_corpus(args):
    pool = load(f"data/pool{SFX}.jsonl")
    days = load(f"data/pool{SFX}_days.jsonl")
    hv = load(f"data/harvest{SFX}.jsonl")
    gd = load(f"data/ghdirs{SFX}.jsonl")
    sel = load(f"data/selection{SFX}.jsonl")
    sys.path.insert(0, HERE)
    import fetch_gh as fg
    out = ["## Session 19 corpus", ""]
    usable = [r for r in pool if fg.usable(r)]
    inc = sum(1 for d in days for i in d["intervals"] if i["incomplete_results"])
    short = sum(1 for d in days for i in d["intervals"] if i["returned"] < min(i["total_count"], 1000))
    out.append(f"Pool: {len(days)} days read, {sum(len(d['intervals']) for d in days)} search intervals "
               f"({inc} flagged incomplete by the API, {short} returned fewer rows than their count), "
               f"{len(pool)} repositories with at least {fg.MIN_STARS} stars, {len(usable)} usable "
               f"(not a fork, a licence of the list, at most {fg.REPO_KB_CAP // 1000} MB).")
    why = Counter()
    for r in pool:
        if r["fork"]:
            why["fork"] += 1
        elif r["license"] not in fg.LICENCES:
            why["licence " + str(r["license"])] += 1
        elif not (0 < (r["size_kb"] or 0) <= fg.REPO_KB_CAP):
            why["size"] += 1
    out.append("Not usable: " + ", ".join(f"{k} {v}" for k, v in why.most_common(12)) + ".")
    out.append("Usable by licence: " + ", ".join(f"{k} {v}" for k, v in Counter(r["license"] for r in usable).most_common()) + ".")
    st = Counter(r["status"] for r in hv)
    okr = [r for r in hv if r["status"] == "ok"]
    out.append("")
    out.append(f"Harvest: {len(hv)} repositories read ({', '.join(f'{k} {v}' for k, v in st.most_common())}); "
               f"{sum(1 for r in okr if r.get('n_eligible'))} hold an eligible directory, "
               f"{sum(1 for r in okr if r.get('n_eligible_mixed'))} a mixed one, "
               f"{sum(1 for r in okr if r.get('n_taken'))} gave a directory to the scored set.")
    n, m = len(gd), sum(1 for r in gd if r["mixed"])
    out.append("")
    out.append(f"Eligible directories listed in the harvested repositories: {n}; mixed (an image file and "
               f"another kept file): {m}, {m / max(n, 1):.3f}.")
    per_repo = defaultdict(list)
    for r in gd:
        per_repo[r["repo_id"]].append(r["mixed"])
    rates = [np.mean(v) for v in per_repo.values()]
    out.append(f"Per repository with an eligible directory ({len(per_repo)}): mean share of mixed directories "
               f"{np.mean(rates) if rates else float('nan'):.3f}; repositories with at least one mixed directory "
               f"{sum(1 for v in per_repo.values() if any(v))}.")
    out.append("")
    out.append("| eligible directories | all | mixed | share mixed |")
    out.append("|---|---:|---:|---:|")
    dep = np.array([r["depth"] for r in gd])
    kept = np.array([r["n_kept"] for r in gd])
    mix = np.array([r["mixed"] for r in gd], bool)
    for name, s in [("all", np.ones(len(gd), bool))] + binned(dep, DEPTH_BINS) + \
            [(f"{nm} kept files", s) for nm, s in binned(kept, SIZE_BINS)]:
        out.append(f"| {name} | {int(s.sum())} | {int((s & mix).sum())} | {(s & mix).sum() / max(s.sum(), 1):.3f} |")
    out.append("")
    nm_ = sum(1 for r in sel if r["mixed_ext"])
    out.append(f"Scored set: {len(sel)} directories ({nm_} mixed by extension, {len(sel) - nm_} other), "
               f"{sum(r['n_included'] for r in sel)} files, {len({r['repo'] for r in sel})} repositories, "
               f"{len({r['owner'] for r in sel})} owners.")
    sdep = np.array([r["depth"] for r in sel])
    skept = np.array([r["n_included"] for r in sel])
    out.append("By depth: " + ", ".join(f"{nm} {int(s.sum())}" for nm, s in binned(sdep, DEPTH_BINS)) +
               ". By kept files: " + ", ".join(f"{nm} {int(s.sum())}" for nm, s in binned(skept, SIZE_BINS)) + ".")
    out.append("Licences: " + ", ".join(f"{k} {v}" for k, v in Counter(r["license"] for r in sel).most_common()) + ".")
    out.append("Languages (GitHub's label, ten most frequent): " +
               ", ".join(f"{k} {v}" for k, v in Counter(str(r["language"]) for r in sel).most_common(10)) + ".")
    yrs = Counter(str(r["created_at"])[:4] for r in sel)
    out.append("Repository creation year: " + ", ".join(f"{k} {yrs[k]}" for k in sorted(yrs)) + ".")
    for name in (f"data/manifest{SFX}.jsonl", f"data/dirs{SFX}.jsonl"):
        if not os.path.exists(os.path.join(ROOT, name)):
            print("\n".join(out))
            return
    manifest = load(f"data/manifest{SFX}.jsonl")
    dirs = load(f"data/dirs{SFX}.jsonl")
    out.append("")
    out.append(f"Manifest: {len(manifest)} files in {len(dirs)} directories; modality " +
               ", ".join(f"{k} {v}" for k, v in Counter(r["modality"] for r in manifest).most_common()) + ".")
    bk = Counter(ev.bucket_of(r["image_frac"]) for r in dirs)
    both = sum(1 for r in dirs if (r["n_image"] + r["n_pdf_scanned"]) and
               (r["n_files"] - r["n_image"] - r["n_pdf_scanned"]))
    out.append("Directories per image-fraction bucket: " + ", ".join(f"{b} {bk[b]}" for b in ev.BUCKETS) +
               f". Directories with both input groups in the manifest: {both}.")
    print("\n".join(out))


# ---------------------------------------------------------------- validity

def parse_evalmd(path):
    """eval.py's printed c - a in the two primary cells: {'P1': '+0.253 [+0.214, +0.294]', ...}."""
    txt = open(path if os.path.isabs(path) else os.path.join(ROOT, path)).read()
    got = {}
    for cell, lab in (("P1", "P1 image in [0,.2)+[.2,.5)"), ("P2", "P2 textlike in [.5,.8)+[.8,1]")):
        m = re.search(r"\| " + re.escape(lab) + r" \|[^\n]*\| ([+-]\d\.\d{3}) \| (\[[^\]]+\]) \|", txt)
        got[cell] = f"{m.group(1)} {m.group(2)}" if m else None
    return got


def cmd_validity(args):
    manifest = load(f"data/manifest{SFX}.jsonl")
    dirs = {r["dir"]: r for r in load(f"data/dirs{SFX}.jsonl")}
    ranks = {e: load(p) for e, p in pairs(args.ranks).items()}
    evalmd = pairs(args.evalmd)
    encs = list(ranks)
    dec = encs[0]
    own = {e: ranks[e] for e in encs}                      # each encoder's own rows, for the reproduction check
    shared = set.intersection(*[{g["query_path"] for g in ranks[e]} for e in encs])
    for e in encs:
        by = {g["query_path"]: g for g in ranks[e]}
        ranks[e] = [by[g["query_path"]] for g in own[dec] if g["query_path"] in shared]
    qpaths = [g["query_path"] for g in ranks[dec]]
    g0 = ranks[dec]
    qd = np.array([g["relevant_dir"] for g in g0])
    qm = np.array([g["modality"] for g in g0])
    qb = np.array([g["image_frac_bucket"] for g in g0])
    qo = np.array([dirs[d].get("owner") or f"record:{dirs[d]['record']}" for d in qd])
    cells = cells_of(qm, qb)
    rows_avail = [r for r in ("a", "c", "d", "cs", "tb2c", "tbc", "cc", "dc", "ac") if f"rank_{r}" in g0[0]]
    H = {e: {r: np.array([g[f"rank_{r}"] <= 5 for g in ranks[e]], float) for r in rows_avail} for e in encs}
    out = [f"## Session 19 validity and verdicts ({', '.join(encs)}; {dec} decides the hypotheses)", ""]
    out.append(f"Queries: {len(qpaths)} over {len(set(qd))} directories and {len(set(qo))} owners "
               f"(effective owners {eff_families(qo):.0f}). Queries per encoder before taking those all encoders "
               f"share: " + ", ".join(f"{e} {len(own[e])}" for e in encs) + ".")
    out.append("")

    # 1. this code against eval.py's printed directory intervals
    bad, lines = [], []
    for e in encs:
        want = parse_evalmd(evalmd[e]) if e in evalmd else {}
        od = np.array([g["relevant_dir"] for g in own[e]])
        ocells = cells_of(np.array([g["modality"] for g in own[e]]), np.array([g["image_frac_bucket"] for g in own[e]]))
        oz = np.array([float(g["rank_c"] <= 5) - float(g["rank_a"] <= 5) for g in own[e]])
        for c in ("P1", "P2"):
            s = ocells[c]
            got = fmt(boot_mean(oz[s], od[s], SEEDS[c])) if s.sum() > 1 else None
            same = got is not None and got == want.get(c)
            lines.append(f"{e} {c}: here {got}; eval.py {want.get(c)}; {'same' if same else 'DIFFERENT'}")
            bad += [] if same or args.skip_repro else [(e, c)]
    out.append("### Reproduction of eval.py's directory intervals of c - a")
    out.append("")
    out += [f"- {l}" for l in lines]
    out.append("")
    if bad:
        out.append(f"NOT REPRODUCED: {bad}. Stopping before any new number.")
        print("\n".join(out))
        sys.exit(3)
    out.append("Reproduced: the directory bootstrap here is eval.py's.")
    out.append("")

    # 2. per-query facts from the manifest and the ok flags of the deciding encoder's cache
    idx_rows = load(args.index)
    assert [r["path"] for r in idx_rows] == [r["path"] for r in manifest], "index not in manifest order"
    ok = np.array([bool(r["ok"]) for r in idx_rows])
    ranked = {d: j for j, d in enumerate(sorted(d for d, r in dirs.items() if r["n_files"] >= 3))}
    by_dir = defaultdict(list)
    for i, r in enumerate(manifest):
        if ok[i]:
            by_dir[r["dir"]].append(i)
    rowpos = {r["path"]: i for i, r in enumerate(manifest)}
    is_img = lambda i: manifest[i]["modality"] in ev.IMAGE_INPUTS  # noqa: E731
    n_dir = np.zeros(len(qpaths), int)
    sib_same = np.zeros(len(qpaths), int)
    c_is_d = np.zeros(len(qpaths), bool)
    sib = np.zeros(len(qpaths), bool)
    depth = np.array([dirs[d].get("repo_depth") or 0 for d in qd])
    for k, p in enumerate(qpaths):
        i0 = rowpos[p]
        members = by_dir[manifest[i0]["dir"]]
        others = [j for j in members if j != i0]
        n_dir[k] = len(members)
        sib_same[k] = sum(1 for j in others if is_img(j) == is_img(i0))
        c_is_d[k] = max(Counter(manifest[j]["modality"] for j in others).values(), default=0) <= 3
        st, ex = stem_ext(p)
        sib[k] = any(stem_ext(manifest[j]["path"])[0] == st and stem_ext(manifest[j]["path"])[1] != ex for j in others)
    rd, ra, _ = name_baseline(manifest, ok, ranked, qpaths)
    missed = (rd > 5) & (ra > 5)
    clean = missed & ~sib
    has_sib = sib_same >= 1
    qkind = np.array([kind_of(p, m) for p, m in zip(qpaths, qm)])
    code_dirs = {d for d, members in by_dir.items()
                 if any(kind_of(manifest[j]["path"], manifest[j]["modality"]) == "code" for j in members)}
    nocode = np.array([d not in code_dirs for d in qd])
    allq = np.ones(len(qd), bool)

    def triple(z, s, cell):
        """directory, owner-clustered and owner-weighted intervals of mean(z) over the queries s."""
        return (boot_mean(z[s], qd[s], SEEDS[cell]), boot_mean(z[s], qo[s], SEEDS[cell] + CLUSTER_OFFSET),
                boot_mean(z[s], qo[s], SEEDS[cell] + CLUSTER_OFFSET, weighted=True))

    out.append("### Flags (counts over the evaluation queries)")
    out.append("")
    out.append("| cell | queries | directories | owners (effective) | same-stem sibling | names alone in top 5 | clean |")
    out.append("|---|---:|---:|---|---:|---:|---:|")
    for c, s in cells.items():
        out.append(f"| {c} | {int(s.sum())} | {len(set(qd[s]))} | {len(set(qo[s]))} ({eff_families(qo[s]):.0f}) | "
                   f"{int((s & sib).sum())} | {int((s & ~missed).sum())} | {int((s & clean).sum())} |")
    out.append("")
    out.append("### Filename-only baseline (no encoder): recall@5")
    out.append("")
    out.append("| cell | d_fn (max over names) | a_fn (pooled names) |")
    out.append("|---|---:|---:|")
    for c, s in cells.items():
        if s.any():
            out.append(f"| {c} | {(rd[s] <= 5).mean():.3f} | {(ra[s] <= 5).mean():.3f} |")
    out.append("")

    def block(title, prs, subsets, cell_names=("all", "P1", "P2", "M1", "M2")):
        out.append(f"### {title}")
        out.append("")
        out.append("| encoder | subset | pair | cell | queries | directories | owners (effective) | point | "
                   "directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |")
        out.append("|---|---|---|---|---:|---:|---|---:|---|---|---|")
        res = {}
        for e in encs:
            for sname, smask in subsets:
                for x, y in prs:
                    if x not in H[e] or y not in H[e]:
                        continue
                    for c in cell_names:
                        s = cells[c] & smask
                        if s.sum() < 2 or len(set(qo[s])) < 2:
                            continue
                        t = triple(H[e][x] - H[e][y], s, c)
                        res[(e, sname, x, y, c)] = t + (int(s.sum()),)
                        out.append(f"| {e} | {sname} | {x} - {y} | {c} | {int(s.sum())} | {len(set(qd[s]))} | "
                                   f"{t[1][3]} ({eff_families(qo[s]):.0f}) | {t[0][0]:+.3f} | [{t[0][1]:+.3f}, {t[0][2]:+.3f}] | "
                                   f"[{t[1][1]:+.3f}, {t[1][2]:+.3f}] | {t[2][0]:+.3f} [{t[2][1]:+.3f}, {t[2][2]:+.3f}] |")
        out.append("")
        return res

    def levels(title, groups, rows, cell_names):
        out.append(f"### {title}")
        out.append("")
        out.append("| encoder | group | cell | queries | owners | c equals d | " + " | ".join(f"R@5 {r}" for r in rows) + " |")
        out.append("|---|---|---|---:|---:|---:|" + "---:|" * len(rows))
        for e in encs:
            for gname, gmask in groups:
                for c in cell_names:
                    s = cells[c] & gmask
                    if not s.any():
                        continue
                    out.append(f"| {e} | {gname} | {c} | {int(s.sum())} | {len(set(qo[s]))} | {c_is_d[s].mean():.3f} | " +
                               " | ".join(f"{H[e][r][s].mean():.3f}" if r in H[e] else "" for r in rows) + " |")
        out.append("")

    subsets = [("all", allq), ("names miss", missed), ("no sibling", ~sib), ("clean", clean)]
    res = block("c - a by subset (H19a reads 'all', H19b reads 'clean')", [("c", "a")], subsets)
    resd = block("c - d, cs - d and cs - c (H19c reads c - d over all queries)", [("c", "d"), ("cs", "d"), ("cs", "c")],
                 [("all", allq)])

    # the registered statistics: owner-weighted, 10,000 owner resamples, 95 and 98.33 percent intervals
    out.append("### The registered tests (owner-weighted mean, 10,000 resamples of owners)")
    out.append("")
    out.append("| encoder | test | queries | owners | point | 95% | 98.33% | reading |")
    out.append("|---|---|---:|---:|---:|---|---|---|")
    P = {"P1s": cells["P1"] & has_sib, "P2s": cells["P2"] & has_sib}
    tests = [("H19a P1s: c - a", "c", "a", P["P1s"], 19001, "loss", True),
             ("H19a P2s: c - a", "c", "a", P["P2s"], 19002, "loss", True),
             ("H19c: c - d where c differs from d", "c", "d", ~c_is_d, 19003, "margin", True),
             ("H19b P1s clean: c - a", "c", "a", P["P1s"] & clean, 19004, "loss", False),
             ("H19b P2s clean: c - a", "c", "a", P["P2s"] & clean, 19005, "loss", False),
             ("no-code folders, P1s: c - a", "c", "a", P["P1s"] & nocode, 19006, "loss", False),
             ("no-code folders, P2s: c - a", "c", "a", P["P2s"] & nocode, 19007, "loss", False),
             ("all of P1 (lone images included): c - a", "c", "a", cells["P1"], 19008, "loss", False),
             ("all of P2 (lone texts included): c - a", "c", "a", cells["P2"], 19009, "loss", False),
             ("cs - d where c differs from d", "cs", "d", ~c_is_d, 19010, "margin", False)]
    reg = {}
    for e in encs:
        for name, x, y, s, seed, how, primary in tests:
            if x not in H[e] or y not in H[e] or s.sum() < 2 or len(set(qo[s])) < 2:
                out.append(f"| {e} | {name} | {int(s.sum())} | {len(set(qo[s])) if s.any() else 0} | | | | no test (empty) |")
                continue
            pt, i95, i98, no = oboot(H[e][x][s] - H[e][y][s], qo[s], seed)
            lo, hi = i98 if primary else i95
            if how == "loss":
                read = outcome(lo, hi, no)
            elif no < MIN_OWNERS:
                read = f"inconclusive (fewer than {MIN_OWNERS} owners)"
            else:
                read = ("not inferior (lower bound at or above -0.02)" if lo >= -MARGIN else
                        "inferior (upper bound under -0.02)" if hi < -MARGIN else "inconclusive")
            reg[(e, name)] = read
            out.append(f"| {e} | {name}{' (primary)' if primary else ''} | {int(s.sum())} | {no} | {pt:+.3f} | "
                       f"[{i95[0]:+.3f}, {i95[1]:+.3f}] | [{i98[0]:+.3f}, {i98[1]:+.3f}] | {read} |")
    out.append("")
    out.append("### Verdicts")
    out.append("")
    for e in encs:
        role = "decides" if e == dec else "reported by the same rules, no verdict of its own"
        a1, a2 = reg.get((e, tests[0][0]), "no test"), reg.get((e, tests[1][0]), "no test")
        if a1.startswith("confirmed") and a2.startswith("confirmed"):
            v = "confirmed in both cells"
        elif a1.startswith("below") or a2.startswith("below"):
            v = "not replicated at the registered size in at least one cell"
        elif all(x.startswith(("confirmed", "present")) for x in (a1, a2)):
            v = "replicated, with the size open in at least one cell"
        else:
            v = "inconclusive"
        out.append(f"H19a ({e}, {role}): P1s {a1}; P2s {a2}. H19a: {v}.")
        out.append(f"H19b ({e}, secondary): clean P1s {reg.get((e, tests[3][0]), 'no test')}; clean P2s {reg.get((e, tests[4][0]), 'no test')}.")
        out.append(f"H19c ({e}, {role}): {reg.get((e, tests[2][0]), 'no test')}.")
    out.append("")
    out.append("### Secondary: the minority cells by the kind of the query file (c - a, owner-weighted, 95%)")
    out.append("")
    out.append("| encoder | cell | kind | queries | owners | R@5 a | R@5 c | R@5 d | c - a |")
    out.append("|---|---|---|---:|---:|---:|---:|---:|---|")
    for e in encs:
        for cname in ("P1s", "P2s"):
            for k in ("image", "prose", "code", "config", "table"):
                s = P[cname] & (qkind == k)
                if s.sum() < 2 or len(set(qo[s])) < 2:
                    continue
                pt, i95, _, no = oboot(H[e]["c"][s] - H[e]["a"][s], qo[s], 19020)
                out.append(f"| {e} | {cname} | {k} | {int(s.sum())} | {no} | {H[e]['a'][s].mean():.3f} | {H[e]['c'][s].mean():.3f} | "
                           f"{H[e]['d'][s].mean():.3f} | {pt:+.3f} [{i95[0]:+.3f}, {i95[1]:+.3f}] |")
    out.append("")

    size_groups = binned(n_dir, SIZE_BINS)
    levels("Secondary: recall@5 by the number of embedded files in the query's folder", size_groups,
           [r for r in ("a", "c", "cs", "d") if r in rows_avail], ("all", "P1", "P2", "M1", "M2"))
    block("Secondary: differences by the number of embedded files in the query's folder",
          [("c", "a"), ("c", "d"), ("cs", "d")], size_groups)
    block("Secondary: differences on the queries whose folder c does not hold whole (a label keeps more than three files)",
          [("c", "a"), ("c", "d"), ("cs", "d")], [("c differs from d", ~c_is_d), ("c equals d", c_is_d)])
    sib_groups = binned(sib_same, SIB_BINS)
    levels("Secondary: recall@5 by the number of other files of the query's input group in its folder", sib_groups,
           [r for r in ("a", "c", "d") if r in rows_avail], ("P1", "P2"))
    block("Secondary: c - a by the number of other files of the query's input group in its folder", [("c", "a")],
          sib_groups, cell_names=("P1", "P2"))
    block("Secondary: c - a by the depth of the folder in its repository", [("c", "a")], binned(depth, DEPTH_BINS),
          cell_names=("all", "P1", "P2"))
    prs = [p for p in (("tb2c", "c"), ("c", "tbc"), ("cc", "c"), ("dc", "d"), ("ac", "a")) if p[0] in rows_avail and p[1] in rows_avail]
    if prs:
        block("Secondary: the other rows with owner-clustered intervals", prs, [("all", allq)])
    if len(encs) > 1:
        out.append("### Secondary: the loss compared between encoders on the same queries, (c - a) under X minus (c - a) under Y")
        out.append("")
        out.append("| pair | cell | point | directory 95% | owner-clustered 95% |")
        out.append("|---|---|---:|---|---|")
        for x in encs[1:]:
            for c in ("P1", "P2"):
                s = cells[c]
                if s.sum() < 2:
                    continue
                z = (H[x]["c"] - H[x]["a"]) - (H[dec]["c"] - H[dec]["a"])
                t = triple(z, s, c)
                out.append(f"| {x} - {dec} | {c} | {t[0][0]:+.3f} | [{t[0][1]:+.3f}, {t[0][2]:+.3f}] | [{t[1][1]:+.3f}, {t[1][2]:+.3f}] |")
        out.append("")
    if args.flags:
        with open(args.flags, "w") as fh:
            for k, p in enumerate(qpaths):
                fh.write(json.dumps({"query_path": p, "owner": str(qo[k]), "sibling": bool(sib[k]),
                                     "name_rank_d": int(rd[k]), "name_rank_a": int(ra[k]), "n_dir": int(n_dir[k]),
                                     "sib_same": int(sib_same[k]), "c_is_d": bool(c_is_d[k]), "depth": int(depth[k])}) + "\n")
    print("\n".join(out))


# ---------------------------------------------------------------- commit-subject queries

def clean_subject(subject, names):
    """The query text of a commit subject, or None. names: lowercased names and stems of the folder's kept files."""
    low = subject.strip().lower()
    if low in CQ_STOP_EXACT or low.startswith(CQ_STOP_PREFIX):
        return None
    toks = []
    for t in subject.split():
        core = t.strip(STRIP).lower()
        if "/" in t or "\\" in t or core in names:
            continue
        if re.search(r"\.[a-z0-9]{1,5}$", core) and core.rsplit(".", 1)[1] in EXT:
            continue
        toks.append(t)
    text = " ".join(toks).strip()
    if len(re.findall(r"[^\W\d_]{3,}", text)) < CQ_MIN_WORDS:
        return None
    return text


def cq_build(args):
    global EXT
    from fetch import EXT_MODALITY
    EXT = set(EXT_MODALITY)
    sel = {r["id"]: r for r in load(f"data/selection{SFX}.jsonl")}
    dirs = {r["record"]: r for r in load(f"data/dirs{SFX}.jsonl")}
    commits = load(f"data/commits{SFX}.jsonl")
    by_dir = defaultdict(list)
    for c in commits:
        by_dir[c["id"]].append(c)
    n = Counter()
    rows = []
    for did in sorted(by_dir):
        if did not in sel or did not in dirs:
            continue
        names = set()
        for f in sel[did]["files"]:
            k = f["key"].lower()
            names.add(k)
            st = k.rsplit(".", 1)[0]
            if len(st) >= 3:
                names.add(st)
        seen, kept = set(), []
        for c in sorted(by_dir[did], key=lambda c: (-c["time"], c["commit"])):
            n["commits"] += 1
            text = clean_subject(c["subject"], names)
            if text is None:
                n["dropped by the rules"] += 1
                continue
            if text.lower() in seen:
                n["repeated text"] += 1
                continue
            seen.add(text.lower())
            if len(kept) < CQ_MAX_PER_DIR:
                kept.append((c, text))
            else:
                n["beyond three per directory"] += 1
        for c, text in kept:
            rows.append({"qid": f"{did}:{c['commit'][:12]}", "id": did, "dir": dirs[did]["dir"], "commit": c["commit"],
                         "time": c["time"], "text": text})
    with open(os.path.join(ROOT, f"data/commitq{SFX}.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"commit-subject queries: {len(rows)} over {len({r['id'] for r in rows})} directories, from "
          f"{n['commits']} qualifying commits in {len(by_dir)} directories ({n['dropped by the rules']} dropped by the "
          f"rules, {n['repeated text']} repeated within a directory, {n['beyond three per directory']} beyond three per directory).")


def cq_embed(args):
    import embed as em
    qs = load(f"data/commitq{SFX}.jsonl")
    enc = em.Encoder(args.model)
    cut = [enc.truncate(q["text"])[0] for q in qs]
    t0 = time.time()
    Q = enc.encode_texts(cut, "query")
    npz = os.path.join(ev.DATA, "emb", args.emb, f"commitq{SFX}.npz")
    np.savez(npz, vecs=Q.astype(np.float32), qids=np.array([q["qid"] for q in qs]))
    print(f"{len(qs)} commit-subject queries embedded in {time.time() - t0:.0f}s -> {npz}", file=sys.stderr)


def cq_eval(args):
    manifest = load(f"data/manifest{SFX}.jsonl")
    dirs = {r["dir"]: r for r in load(f"data/dirs{SFX}.jsonl")}
    qs = load(f"data/commitq{SFX}.jsonl")
    emb_dir = os.path.join(ev.DATA, "emb", args.emb)
    index = load(os.path.join(emb_dir, "index.jsonl"))
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache order differs from manifest"
    ok = np.array([bool(r.get("ok")) for r in index])
    mods_all = np.array([r["modality"] for r in manifest])
    dir_of = np.array([r["dir"] for r in manifest])
    dir_list = sorted(d for d in set(dir_of[ok]) if d in dirs)
    pos = {d: i for i, d in enumerate(dir_list)}
    data = np.load(os.path.join(emb_dir, f"commitq{SFX}.npz"))
    assert list(data["qids"]) == [q["qid"] for q in qs], "the embedded queries are not data/commitq_s19.jsonl"
    keep = np.array([q["dir"] in pos for q in qs])
    Q = data["vecs"][keep]
    qs = [q for q, k in zip(qs, keep) if k]
    V = np.load(os.path.join(emb_dir, "vectors.npy"))
    calib, is_img, in_calib, mu, Vc = ev.centered_space(V, ok, mods_all, manifest, dirs, args.calib, args.calib_seed)
    Vu = ev.unit(V).astype(np.float32)
    Qc = ev.unit(Q - mu["txt"]).astype(np.float32)
    children = {d: np.where((dir_of == d) & ok)[0] for d in dir_list}
    qdir = np.array([q["dir"] for q in qs])
    qpos = np.array([pos[d] for d in qdir])
    qb = np.array([ev.bucket_of(dirs[d]["image_frac"]) for d in qdir])
    qo = np.array([dirs[d].get("owner") or f"record:{dirs[d]['record']}" for d in qdir])
    ranks = {}
    for row in CQ_ROWS:
        space, base, param = ev.parse_rep(row)
        X = Vc if space == "c" else Vu
        blocks = [ev.build(base, X[children[d]], mods_all[children[d]], param) for d in dir_list]
        starts = np.cumsum([0] + [len(b) for b in blocks[:-1]])
        R_all = np.concatenate(blocks).astype(np.float32)
        qv = Qc if space == "c" else Q
        rk = np.zeros(len(qs), int)
        for i0 in range(0, len(qs), 256):
            S = qv[i0:i0 + 256] @ R_all.T
            D = np.maximum.reduceat(S, starts, axis=1)
            tgt = D[np.arange(len(D)), qpos[i0:i0 + 256]]
            rk[i0:i0 + 256] = 1 + (D > tgt[:, None]).sum(axis=1)
        ranks[row] = rk
    # names alone: the query text against the file names of every folder (char 3- and 4-grams, as validity.py)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    files = [i for i in range(len(manifest)) if ok[i] and manifest[i]["dir"] in pos]
    files.sort(key=lambda i: (pos[manifest[i]["dir"]], i))
    owner = np.array([pos[manifest[i]["dir"]] for i in files])
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), sublinear_tf=True)
    X = normalize(vec.fit_transform([stem_ext(manifest[i]["path"])[0] for i in files])).astype(np.float32).tocsr()
    bounds = np.searchsorted(owner, np.arange(len(dir_list) + 1))
    T = normalize(vec.transform([q["text"].lower() for q in qs])).astype(np.float32).tocsr()
    rn = np.zeros(len(qs), int)
    for i0 in range(0, len(qs), 256):
        sim = (T[i0:i0 + 256] @ X.T).toarray()
        D = np.maximum.reduceat(sim, bounds[:-1], axis=1)
        tgt = D[np.arange(len(D)), qpos[i0:i0 + 256]]
        rn[i0:i0 + 256] = 1 + (D > tgt[:, None]).sum(axis=1)
    if args.dump_ranks:
        with open(args.dump_ranks, "w") as fh:
            for i, q in enumerate(qs):
                fh.write(json.dumps({"qid": q["qid"], "relevant_dir": q["dir"], "image_frac_bucket": str(qb[i]),
                                     "name_rank": int(rn[i]), **{f"rank_{r}": int(ranks[r][i]) for r in CQ_ROWS}}) + "\n")
    cells = [("all", np.ones(len(qs), bool), 2100), ("text-heavy [0,.2)+[.2,.5)", np.isin(qb, LO_B), 2101),
             ("image-heavy [.5,.8)+[.8,1]", np.isin(qb, HI_B), 2102)]
    out = [f"## Session 19 commit-subject queries, {args.enc} ({args.model}, cache {args.emb})", ""]
    out.append(f"Queries: {len(qs)} over {len(set(qdir))} directories and {len(set(qo))} owners; {len(dir_list)} directories "
               f"ranked (random recall@5 = {5 / len(dir_list):.4f}); {int((~keep).sum())} queries dropped because their "
               f"directory has no embedded file. Representations use all embedded files of a directory (the query is not a "
               f"file). Calibration seed {args.calib_seed} gives the text mean for the centered rows.")
    for k in (1, 5, 10):
        out.append("")
        out.append(f"### recall@{k}")
        out.append("")
        out.append("| cell | queries | directories | owners | " + " | ".join(CQ_ROWS) + " | names alone |")
        out.append("|---|---:|---:|---:|" + "---:|" * (len(CQ_ROWS) + 1))
        for name, s, _ in cells:
            if s.any():
                out.append(f"| {name} | {int(s.sum())} | {len(set(qdir[s]))} | {len(set(qo[s]))} | " +
                           " | ".join(f"{(ranks[r][s] <= k).mean():.3f}" for r in CQ_ROWS) + f" | {(rn[s] <= k).mean():.3f} |")
    out.append("")
    out.append("### Differences in recall@5: point, owner-clustered 95% interval")
    out.append("")
    prs = [("c", "a"), ("d", "c"), ("ac", "a"), ("cc", "c")]
    out.append("| cell | subset | queries | " + " | ".join(f"{x} - {y}" for x, y in prs) + " |")
    out.append("|---|---|---:|" + "---|" * len(prs))
    stat = {}
    for name, s, seed in cells:
        for sub, m in (("all", np.ones(len(qs), bool)), ("names miss", rn > 5)):
            ss = s & m
            if ss.sum() < 2 or len(set(qo[ss])) < 2:
                continue
            cols = []
            for x, y in prs:
                z = (ranks[x][ss] <= 5).astype(float) - (ranks[y][ss] <= 5).astype(float)
                t = boot_mean(z, qo[ss], seed + (7 if sub != "all" else 0))
                stat[(name, sub, x, y)] = t
                cols.append(fmt(t))
            out.append(f"| {name} | {sub} | {int(ss.sum())} | " + " | ".join(cols) + " |")
    out.append("")
    hi = cells[2][1]
    if hi.sum() >= 2 and len(set(qo[hi])) >= 2:
        d5, n5 = float((ranks["d"][hi] <= 5).mean()), float((rn[hi] <= 5).mean())
        z = (ranks["c"][hi] <= 5).astype(float) - (ranks["a"][hi] <= 5).astype(float)
        pt, i95, _, no = oboot(z, qo[hi], 19030)
        gate = d5 >= CQ_GATE and d5 > n5
        read = outcome(i95[0], i95[1], no) if gate else "untestable (the gate failed)"
        out.append(f"H19d statistic ({args.enc}): image-heavy directories, {int(hi.sum())} queries from {no} owners; gate, "
                   f"recall@5 of d {d5:.3f} (needs {CQ_GATE:.2f} and more than names alone, {n5:.3f}): "
                   f"{'passed' if gate else 'failed'}; owner-weighted c - a {pt:+.3f} [{i95[0]:+.3f}, {i95[1]:+.3f}]; "
                   f"H19d: {read}" + ("." if args.enc == "E1" else " (the registered reading is the E1 run)."))
    else:
        out.append(f"H19d statistic ({args.enc}): fewer than two queries or owners on image-heavy directories; untestable.")
    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("corpus")
    p = sub.add_parser("validity")
    p.add_argument("--ranks", required=True, help="E1=<eval.py ranks jsonl>[,E4=...]; the first one decides")
    p.add_argument("--index", required=True, help="index.jsonl of the deciding encoder's cache (ok flags)")
    p.add_argument("--evalmd", default="", help="E1=<eval.py markdown output>[,...] for the reproduction check")
    p.add_argument("--flags", default=None, help="write the per-query flags to this jsonl path")
    p.add_argument("--skip-repro", action="store_true", help="tests only: do not stop on a failed reproduction")
    p = sub.add_parser("commitq")
    p.add_argument("what", choices=["build", "embed", "eval"])
    p.add_argument("--model")
    p.add_argument("--emb")
    p.add_argument("--enc", default="E1")
    p.add_argument("--calib", type=float, default=0.2)
    p.add_argument("--calib-seed", type=int, default=20261104)
    p.add_argument("--dump-ranks", default=None)
    args = ap.parse_args()
    if args.cmd == "corpus":
        cmd_corpus(args)
    elif args.cmd == "validity":
        cmd_validity(args)
    else:
        {"build": cq_build, "embed": cq_embed, "eval": cq_eval}[args.what](args)


EXT = set()

if __name__ == "__main__":
    main()
