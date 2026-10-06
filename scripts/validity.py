#!/usr/bin/env python3
"""dirvec session 17: is the minority-modality loss a fingerprint or creator artifact? (BRIEF.md, session 17)

Reads per-query ranks written by earlier sessions (no new embedding) and reports, per encoder:
  - c - a and other pairs per cell with three intervals: eval.py's directory bootstrap (reproduced
    here as a check of this code), a creator-clustered bootstrap (a family is the first creator of the
    Zenodo record, lowercased), and a family-weighted estimate with its clustered interval;
  - the same on fingerprint-free subsets: queries the filename-only baseline misses (rank > 5),
    queries without a same-stem sibling of another extension among the folder's embedded files,
    queries outside the four digitization series, and all three at once (the clean set);
  - the verdicts of H17a, H17b and H17c and the secondaries of the brief.

  validity.py --set s11 --ranks E1=<jsonl>,E2=...,E3=...,E4=... --index <E1 index.jsonl>
              --indep <indep_eval ranks jsonl> --descq E1=<jsonl>,... > out.md
  validity.py --set s5 --ranks E1=<jsonl> --light > out.md      (S3 and S5: clustered c - a only)
A failed reproduction of eval.py's published directory intervals exits with code 3 before any
new number is printed.
"""
import argparse
import json
import os
import sys
from collections import Counter

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = 1000
LO_B, HI_B = ["[0,.2)", "[.2,.5)"], ["[.5,.8)", "[.8,1]"]
TEXTLIKE = ["text", "table", "pdf_text", "other"]
SEEDS = {"all": 1, "P1": 50, "P2": 51, "M1": 56, "M2": 57}
CLUSTER_OFFSET = 1000          # creator-clustered resamples use the cell seed plus this
FOUR = {"digital humanities jena", "nona, dronova", "royal botanic garden edinburgh",
        "finnish museum of natural history luomus, university of helsinki"}
# eval.py's directory intervals of c - a as printed in results/session11.md, session14_outputs.md and
# session15_outputs.md (S11, calibration seed 20261102); this script must reproduce them exactly.
PUBLISHED = {("E1", "P1"): "+0.253 [+0.214, +0.294]", ("E1", "P2"): "+0.169 [+0.136, +0.200]",
             ("E2", "P1"): "+0.500 [+0.462, +0.538]", ("E2", "P2"): "+0.348 [+0.312, +0.386]",
             ("E3", "P1"): "+0.205 [+0.164, +0.244]", ("E3", "P2"): "+0.158 [+0.125, +0.188]",
             ("E4", "P1"): "+0.442 [+0.398, +0.482]", ("E4", "P2"): "+0.433 [+0.396, +0.470]"}
PUBLISHED_H15C = {"P1": "+0.189 [+0.145, +0.231]", "P2": "+0.265 [+0.226, +0.305]"}


def load(path):
    with open(path if os.path.isabs(path) else os.path.join(ROOT, path)) as fh:
        return [json.loads(l) for l in fh]


def stem_ext(path):
    b = os.path.basename(path).lower()
    i = b.rfind(".")
    return (b[:i], b[i + 1:]) if i > 0 else (b, "")


def boot_mean(z, groups, seed, weighted=False):
    """Point estimate and 95% percentile interval of the mean of z over 1000 resamples of the groups
    (with replacement). weighted=False: query-weighted mean (sums over the resampled groups divided by
    their query counts), the statistic eval.py's directory bootstrap uses. weighted=True: the mean over
    groups of each group's own mean (every group counts once)."""
    keys = sorted(set(groups))
    gi = {k: i for i, k in enumerate(keys)}
    g = np.array([gi[k] for k in groups])
    zs = np.bincount(g, weights=z, minlength=len(keys))
    ns = np.bincount(g, minlength=len(keys)).astype(float)
    idx = np.random.default_rng(seed).integers(0, len(keys), size=(B, len(keys)))
    if weighted:
        gm = zs / ns
        point, bs = gm.mean(), gm[idx].mean(axis=1)
    else:
        point, bs = z.mean(), zs[idx].sum(axis=1) / ns[idx].sum(axis=1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return float(point), float(lo), float(hi), len(keys)


def fmt(t):
    return f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


def cells_of(qm, qb):
    lo = np.isin(qb, LO_B)
    hi = np.isin(qb, HI_B)
    img = qm == "image"
    tl = np.isin(qm, TEXTLIKE)
    return {"all": np.ones(len(qm), bool), "P1": img & lo, "P2": tl & hi, "M1": img & hi, "M2": tl & lo}


def eff_families(fams):
    c = Counter(fams)
    n = sum(c.values())
    return 1.0 / sum((v / n) ** 2 for v in c.values()) if n else float("nan")


def name_baseline(manifest, ok, ranked, qpaths, title_queries=None):
    """Filename-only baseline. Char 3-4-gram TF-IDF (sublinear tf, char_wb) of the lowercased basename
    without its last extension, fitted on the embedded files of the ranked directories. d_fn: the max
    cosine over a folder's files (the query's own folder without the query file); a_fn: the cosine to
    the unit sum of the folder's name vectors (own folder without the query). Rank as eval.py: 1 + the
    number of directories scoring strictly higher. title_queries: optional {dir: title} scored with
    d_fn against every folder's full set of names (the title is not a file)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    import scipy.sparse as sp
    files = [i for i, r in enumerate(manifest) if ok[i] and r["dir"] in ranked]
    files.sort(key=lambda i: (ranked[manifest[i]["dir"]], i))           # grouped by directory
    owner = np.array([ranked[manifest[i]["dir"]] for i in files])
    names = [stem_ext(manifest[i]["path"])[0] for i in files]
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), sublinear_tf=True)
    X = normalize(vec.fit_transform(names)).astype(np.float32).tocsr()
    fpos = {manifest[i]["path"]: k for k, i in enumerate(files)}
    nd = len(ranked)
    bounds = np.searchsorted(owner, np.arange(nd + 1))
    M = sp.csr_matrix((np.ones(len(owner), np.float32), (owner, np.arange(len(owner)))), shape=(nd, len(owner)))
    S = (M @ X).tocsr()
    A = normalize(S).astype(np.float32).tocsr()
    nz = bounds[1:] > bounds[:-1]
    rd, ra = np.zeros(len(qpaths), int), np.zeros(len(qpaths), int)
    for s in range(0, len(qpaths), 400):
        qi = np.array([fpos[p] for p in qpaths[s:s + 400]])
        Q = X[qi]
        sim = (Q @ X.T).toarray()
        PA = (Q @ A.T).toarray()
        for k, f in enumerate(qi):
            own = owner[f]
            row = sim[k]
            dmax = np.full(nd, -np.inf, np.float32)
            dmax[nz] = np.maximum.reduceat(row, bounds[:-1][nz])
            members = np.arange(bounds[own], bounds[own + 1])
            others = members[members != f]
            own_d = row[others].max() if len(others) else -np.inf
            dmax[own] = own_d
            rd[s + k] = 1 + int((dmax > own_d).sum())
            v = S[own] - Q[k]
            nv = float(np.sqrt(v.multiply(v).sum()))
            own_a = np.float32((v @ Q[k].T).toarray()[0, 0] / nv) if nv > 1e-9 else -np.inf
            sc = PA[k].copy()
            sc[own] = own_a
            ra[s + k] = 1 + int((sc > own_a).sum())
    rt = {}
    if title_queries:
        ds = list(title_queries)
        T = normalize(vec.transform([title_queries[d].lower() for d in ds])).astype(np.float32).tocsr()
        for s in range(0, len(ds), 400):
            sim = (T[s:s + 400] @ X.T).toarray()
            for k, d in enumerate(ds[s:s + 400]):
                dmax = np.full(nd, -np.inf, np.float32)
                dmax[nz] = np.maximum.reduceat(sim[k], bounds[:-1][nz])
                own = ranked[d]
                rt[d] = 1 + int((dmax > dmax[own]).sum())
    return rd, ra, rt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", required=True, choices=["s3", "s5", "s11"])
    ap.add_argument("--ranks", required=True, help="E1=<jsonl>[,E2=...]")
    ap.add_argument("--index", help="index.jsonl of an S11 cache (ok flags), needed without --light")
    ap.add_argument("--indep", help="ranks written by scripts/indep_eval.py for E1 (H17c)")
    ap.add_argument("--descq", help="E1=<jsonl>,... per-query ranks dumped by descq.py eval")
    ap.add_argument("--light", action="store_true", help="clustered c - a only (S3, S5)")
    ap.add_argument("--skip-repro", action="store_true",
                    help="for tests on synthetic caches only: skip the comparison with eval.py's published intervals")
    args = ap.parse_args()
    sfx = {"s3": "_s3", "s5": "_s5", "s11": "_s11"}[args.set]
    manifest = load(f"data/manifest{sfx}.jsonl")
    dirs = {r["dir"]: r for r in load(f"data/dirs{sfx}.jsonl")}
    sel = {r["id"]: r for r in load(f"data/selection{sfx}.jsonl")}

    def fam_of(d):
        cr = sel[dirs[d]["record"]].get("creators") or []
        return cr[0].strip().lower() if cr else f"record:{dirs[d]['record']}"

    ranks = {}
    for item in args.ranks.split(","):
        e, p = item.split("=", 1)
        ranks[e] = load(p)
    encs = list(ranks)
    qpaths = [g["query_path"] for g in ranks[encs[0]]]
    for e in encs[1:]:
        assert [g["query_path"] for g in ranks[e]] == qpaths, f"{e}: query set or order differs from {encs[0]}"
    g0 = ranks[encs[0]]
    qd = np.array([g["relevant_dir"] for g in g0])
    qm = np.array([g["modality"] for g in g0])
    qb = np.array([g["image_frac_bucket"] for g in g0])
    qf = np.array([fam_of(d) for d in qd])
    cells = cells_of(qm, qb)
    H = {e: {r: np.array([g[f"rank_{r}"] <= 5 for g in ranks[e]], float) for r in ("a", "c", "d", "tb2c")
             if f"rank_{r}" in ranks[e][0]} for e in encs}
    out = [f"## Session 17 validity checks, set {args.set.upper()}", ""]
    out.append(f"Queries: {len(qpaths)} over {len(set(qd))} directories and {len(set(qf))} creator families; "
               f"encoders {', '.join(encs)}.")
    out.append("")

    # 1. reproduction of eval.py's published directory intervals (a check of this code)
    if args.set == "s11" and not args.skip_repro:
        bad = []
        lines = []
        for e in encs:
            for c in ("P1", "P2"):
                s = cells[c]
                got = fmt(boot_mean(H[e]["c"][s] - H[e]["a"][s], qd[s], SEEDS[c]))
                ok_ = got == PUBLISHED.get((e, c))
                lines.append(f"{e} {c}: here {got}; published {PUBLISHED.get((e, c))}; {'same' if ok_ else 'DIFFERENT'}")
                bad += [] if ok_ else [(e, c)]
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

    def block(title, pairs, subsets, encs_, clustered_only=False):
        out.append(f"### {title}")
        out.append("")
        head = "| encoder | subset | pair | cell | queries | dirs | families (effective) | point | directory 95% | creator-clustered 95% | family-weighted [clustered 95%] |"
        out.append(head)
        out.append("|---|---|---|---|---:|---:|---|---:|---|---|---|")
        res = {}
        for e in encs_:
            for sname, smask in subsets:
                for x, y in pairs:
                    if x not in H[e] or y not in H[e]:
                        continue
                    for c in ("all", "P1", "P2", "M1", "M2"):
                        s = cells[c] & smask
                        if s.sum() < 2:
                            continue
                        z = H[e][x][s] - H[e][y][s]
                        dirb = boot_mean(z, qd[s], SEEDS[c])
                        clu = boot_mean(z, qf[s], SEEDS[c] + CLUSTER_OFFSET)
                        fw = boot_mean(z, qf[s], SEEDS[c] + CLUSTER_OFFSET, weighted=True)
                        res[(e, sname, x, y, c)] = (dirb, clu, fw, int(s.sum()))
                        out.append(f"| {e} | {sname} | {x} - {y} | {c} | {int(s.sum())} | {len(set(qd[s]))} | "
                                   f"{clu[3]} ({eff_families(qf[s]):.0f}) | {dirb[0]:+.3f} | [{dirb[1]:+.3f}, {dirb[2]:+.3f}] | "
                                   f"[{clu[1]:+.3f}, {clu[2]:+.3f}] | {fw[0]:+.3f} [{fw[1]:+.3f}, {fw[2]:+.3f}] |")
        out.append("")
        return res

    if args.light:
        block(f"c - a on {args.set.upper()} (all queries)", [("c", "a")], [("all", np.ones(len(qd), bool))], encs)
        print("\n".join(out))
        return

    # 2. flags: same-stem siblings, the four series, the filename-only baseline
    idx_rows = load(args.index)
    assert [r["path"] for r in idx_rows] == [r["path"] for r in manifest], "index not in manifest order"
    ok = np.array([bool(r["ok"]) for r in idx_rows])
    ranked = {d: j for j, d in enumerate(sorted(d for d, r in dirs.items() if r["n_files"] >= 3))}
    by_dir = {}
    for i, r in enumerate(manifest):
        if ok[i]:
            by_dir.setdefault(r["dir"], []).append(i)
    rowpos = {r["path"]: i for i, r in enumerate(manifest)}
    sib = np.zeros(len(qpaths), bool)
    for k, p in enumerate(qpaths):
        st, ex = stem_ext(p)
        for j in by_dir[manifest[rowpos[p]]["dir"]]:
            if manifest[j]["path"] != p:
                s2, e2 = stem_ext(manifest[j]["path"])
                if s2 == st and e2 != ex:
                    sib[k] = True
                    break
    four = np.isin(qf, list(FOUR))
    titles = None
    if args.descq:
        import gzip
        tt = {}
        with gzip.open(os.path.join(ROOT, "data", "pool_s11.jsonl.gz"), "rt") as fh:
            for line in fh:
                r = json.loads(line)
                tt[int(r["id"])] = r.get("title", "")
        titles = {d: tt.get(int(r["record"]), "") for d, r in dirs.items() if tt.get(int(r["record"]), "").strip()}
    rd, ra, rt = name_baseline(manifest, ok, ranked, qpaths, titles)
    missed = rd > 5
    clean = missed & ~sib & ~four
    out.append("### Flags (counts over the evaluation queries)")
    out.append("")
    out.append("| cell | queries | families (effective) | same-stem sibling | four series | names alone in top 5 | clean (none of the three) |")
    out.append("|---|---:|---|---:|---:|---:|---:|")
    for c, s in cells.items():
        out.append(f"| {c} | {int(s.sum())} | {len(set(qf[s]))} ({eff_families(qf[s]):.0f}) | {int((s & sib).sum())} | "
                   f"{int((s & four).sum())} | {int((s & ~missed).sum())} | {int((s & clean).sum())} |")
    out.append("")
    out.append("### Filename-only baseline (no encoder): recall@5")
    out.append("")
    out.append("| cell | d_fn (max over names) | a_fn (pooled names) | d_fn - a_fn |")
    out.append("|---|---:|---:|---:|")
    for c, s in cells.items():
        out.append(f"| {c} | {(rd[s] <= 5).mean():.3f} | {(ra[s] <= 5).mean():.3f} | {(rd[s] <= 5).mean() - (ra[s] <= 5).mean():+.3f} |")
    out.append("")

    allq = np.ones(len(qd), bool)
    subsets = [("all", allq), ("names miss", missed), ("no sibling", ~sib), ("not the four series", ~four), ("clean", clean)]
    res = block("c - a by subset (H17a reads 'all', H17b reads 'clean')", [("c", "a")], subsets, encs)

    # 3. verdicts
    out.append("### Verdicts")
    out.append("")
    h17a = {}
    for e in encs:
        cl = {c: res[(e, "all", "c", "a", c)][1] for c in ("P1", "P2")}
        h17a[e] = all(cl[c][1] > 0 for c in cl)
        out.append(f"H17a ({e}): creator-clustered c - a in P1 {fmt(cl['P1'])}, in P2 {fmt(cl['P2'])}; both above zero: "
                   f"{'yes, H17a survives' if h17a[e] else 'no, H17a is dead'} under {e}.")
    for e in encs:
        cl = {c: res[(e, 'clean', 'c', 'a', c)][1] for c in ("P1", "P2")}
        okb = all(cl[c][0] >= 0.05 and cl[c][1] > 0 for c in cl)
        role = "decides" if e in ("E1", "E3") else "reported, no kill"
        out.append(f"H17b ({e}, {role}): clean subset c - a in P1 {fmt(cl['P1'])} ({res[(e, 'clean', 'c', 'a', 'P1')][3]} queries), "
                   f"in P2 {fmt(cl['P2'])} ({res[(e, 'clean', 'c', 'a', 'P2')][3]} queries); point at least +0.05 and interval above zero in both: "
                   f"{'yes' if okb else 'no'}" + (f", H17b {'survives' if okb else 'is dead'} under {e}." if e in ("E1", "E3") else "."))
    if args.indep:
        ind = {g["query_path"]: g for g in load(args.indep)}
        common = [k for k, p in enumerate(qpaths) if p in ind]
        msg = [f"H17c: {len(ind)} queries in the independent ranks, {len(common)} in common with eval.py's {len(qpaths)} (E1)."]
        okc = len(common) == len(qpaths) == len(ind)
        for r in ("a", "c", "d"):
            mine = np.array([ranks["E1"][k][f"rank_{r}"] for k in common])
            theirs = np.array([ind[qpaths[k]][f"rank_{r}"] for k in common])
            same = float((mine == theirs).mean())
            r5 = []
            for c, s in cells.items():
                sc = s[common]
                a1, b1 = f"{(mine[sc] <= 5).mean():.3f}", f"{(theirs[sc] <= 5).mean():.3f}"
                r5.append(f"{c} {a1}/{b1}")
                okc &= a1 == b1
            okc &= same >= 0.99
            msg.append(f"  {r}: identical ranks {same:.5f} ({int((mine != theirs).sum())} differ); recall@5 eval.py/independent: " + ", ".join(r5))
        msg.append(f"H17c: {'yes, H17c survives' if okc else 'no, H17c is dead'} (recall@5 equal at three decimals in all five cells and at least 99 percent identical ranks per row).")
        out += msg
    out.append("")

    # 4. secondaries
    block("Secondary: c - d (the within-0.02 claim; an interval entirely below -0.02 flips it)", [("c", "d")],
          [("all", allq)], encs)
    if "E1" in H and "tb2c" in H["E1"]:
        block("Secondary: tb2c - c under E1 (H11a rule: an interval entirely below -0.02 kills)", [("tb2c", "c")],
              [("all", allq)], ["E1"])
    out.append("### Secondary: the loss compared between encoders on the same queries (H15c and E2 against E1)")
    out.append("")
    out.append("| pair | cell | directory 95% (eval.py's cell seeds) | creator-clustered 95% |")
    out.append("|---|---|---|---|")
    for x, y in (("E4", "E1"), ("E2", "E1"), ("E3", "E1")):
        if x in H and y in H:
            for c in ("P1", "P2"):
                s = cells[c]
                z = (H[x]["c"][s] - H[x]["a"][s]) - (H[y]["c"][s] - H[y]["a"][s])
                dirb = boot_mean(z, qd[s], SEEDS[c])
                clu = boot_mean(z, qf[s], SEEDS[c] + CLUSTER_OFFSET)
                note = ""
                if (x, y) == ("E4", "E1"):
                    note = f" (published {PUBLISHED_H15C[c]}: {'same' if fmt(dirb) == PUBLISHED_H15C[c] else 'DIFFERENT'})"
                out.append(f"| {x} - {y} | {c} | {fmt(dirb)}{note} | [{clu[1]:+.3f}, {clu[2]:+.3f}] |")
    out.append("")
    if args.descq:
        out.append("### Secondary: title and description queries, c - a in recall@5 (one query per folder)")
        out.append("")
        out.append("| encoder | set | folders | queries | point | creator-clustered 95% | names miss: queries, point [clustered 95%] |")
        out.append("|---|---|---|---:|---:|---|---|")
        for item in args.descq.split(","):
            e, p = item.split("=", 1)
            rows = load(p)
            for which in ("title", "desc"):
                for fname, buckets in (("image-heavy", HI_B), ("text-heavy", LO_B)):
                    rr = [r for r in rows if r["set"] == which and r["image_frac_bucket"] in buckets]
                    if not rr:
                        continue
                    z = np.array([float(r["rank_c"] <= 5) - float(r["rank_a"] <= 5) for r in rr])
                    fams = np.array([fam_of(r["relevant_dir"]) for r in rr])
                    clu = boot_mean(z, fams, 2000 + (fname == "text-heavy"))
                    tail = ""
                    if which == "title":
                        m = np.array([rt.get(r["relevant_dir"], 1) > 5 for r in rr])
                        if m.sum() > 1:
                            cm = boot_mean(z[m], fams[m], 2002 + (fname == "text-heavy"))
                            tail = f"{int(m.sum())}, {fmt(cm)}"
                    out.append(f"| {e} | {which} | {fname} | {len(rr)} | {clu[0]:+.3f} | [{clu[1]:+.3f}, {clu[2]:+.3f}] | {tail} |")
        out.append("")
    with open(os.environ.get("S17_FLAGS", os.devnull), "w") as fh:
        for k, p in enumerate(qpaths):
            fh.write(json.dumps({"query_path": p, "family": str(qf[k]), "sibling": bool(sib[k]), "four": bool(four[k]),
                                 "name_rank_d": int(rd[k]), "name_rank_a": int(ra[k])}) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
