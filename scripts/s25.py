#!/usr/bin/env python3
"""dirvec session 25: four post hoc estimates a blind review asked for (BRIEF.md, session 25).

Nothing is embedded or re-run: every input is a per-query file in data/, and every number is E1.
The gates come first; the script stops with exit code 3 before any new number if one fails.

  python3 scripts/s25.py > results/session25_outputs.md

1. GitHub at the natural mix: c - a over all queries, by stratum (mixed or not), and reweighted to
   the eligible share of mixed directories.
2. Zenodo (S11) where c is a strict compression of its folder: c - d there and elsewhere.
3. Zenodo read as GitHub is read: P1s and P2s, creator families weighted equally.
4. A budget curve from session 21's per-query ranks, and labelled against blind centroids at 2 KiB.
"""
import gzip
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval as ev  # noqa: E402
import pool  # noqa: E402
import s19  # noqa: E402
from validity import CLUSTER_OFFSET, PUBLISHED, SEEDS, boot_mean, cells_of, eff_families, fmt  # noqa: E402

ROOT = ev.ROOT
CELLS = ["all", "P1", "P2", "M1", "M2"]
BUDGETS = [512, 1024, 2048, 4096, 8192]
CURVE = ["mean", "kmeans", "kkind", "sample", "allbits"]
ELIGIBLE = {"s19": (1501, 35970), "s24": (3286, 65984)}   # mixed and all eligible directories, as printed
NOVEC_EXT = {"doc", "pptx", "odp", ""}                     # no encoder path (BRIEF.md, session 25, item 2)
TABLE_S11_E1 = {"a": (0.692, 0.421, 0.370, 0.730, 0.830),   # results/session11.md, E1, all P1 P2 M1 M2
                "c": (0.796, 0.674, 0.539, 0.810, 0.894),
                "d": (0.804, 0.685, 0.551, 0.821, 0.897)}
IMG = set(ev.IMAGE_INPUTS)
out = []


def jl(path):
    p = os.path.join(ROOT, path)
    with (gzip.open(p, "rt") if p.endswith(".gz") else open(p)) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def stop(msg):
    out.append("")
    out.append(msg)
    print("\n".join(out))
    sys.exit(3)


def iv(t):
    return f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


def oiv(t):
    return f"{t[0]:+.3f} [{t[1][0]:+.3f}, {t[1][1]:+.3f}]"


def owner_mean(x, owners):
    keys = sorted(set(owners))
    gi = {k: i for i, k in enumerate(keys)}
    g = np.array([gi[k] for k in owners])
    return float((np.bincount(g, weights=x, minlength=len(keys)) / np.bincount(g, minlength=len(keys))).mean())


# ------------------------------------------------------------------ gates
out.append("# Session 25 outputs, verbatim (scripts/s25.py)")
out.append("")
out.append("## Gates")
out.append("")
bad = []
for d in ("s19", "s24"):
    D = pool.Draw(d)
    for what, line, found in D.lines:
        if found is False:
            bad.append((d, what))
    out.append(f"- pool.py's Draw on {d.upper()}: {sum(1 for _, _, f in D.lines if f)} printed lines reproduced, "
               f"{sum(1 for _, _, f in D.lines if f is False)} different, {sum(1 for _, _, f in D.lines if f is None)} not run.")
if bad:
    stop(f"NOT REPRODUCED: {bad}. Stopping before any new number.")

GT = {r["query_path"]: r for r in jl("data/gt_structural_s11.jsonl")}
R11 = jl("data/ranks_s21_s11_e1.jsonl.gz")
qp = [r["query_path"] for r in R11]
qd = np.array([r["relevant_dir"] for r in R11])
qm = np.array([GT[p]["modality"] for p in qp])
qb = np.array([GT[p]["image_frac_bucket"] for p in qp])
cells = cells_of(qm, qb)
hit = {x: np.array([r[f"rank_{x}_f32"] <= 5 for r in R11], float) for x in "acd"}
got = {x: tuple(round(float(hit[x][cells[c]].mean()), 3) for c in CELLS) for x in "acd"}
for x in "acd":
    same = got[x] == TABLE_S11_E1[x]
    out.append(f"- S11 recall@5 of {x} (f32), all P1 P2 M1 M2: here {got[x]}; session 11 {TABLE_S11_E1[x]}; "
               f"{'same' if same else 'DIFFERENT'}")
    if not same:
        bad.append(("s11 table", x))
for c in ("P1", "P2"):
    s = cells[c]
    here = fmt(boot_mean(hit["c"][s] - hit["a"][s], qd[s], SEEDS[c]))
    same = here == PUBLISHED[("E1", c)]
    out.append(f"- S11 c - a in {c}, eval.py's directory interval: here {here}; published {PUBLISHED[('E1', c)]}; "
               f"{'same' if same else 'DIFFERENT'}")
    if not same:
        bad.append(("s11 interval", c))

sel11 = {r["id"]: r for r in jl("data/selection_s11.jsonl")}
dirs11 = {r["dir"]: r for r in jl("data/dirs_s11.jsonl")}


def fam_of(d):                                   # validity.py's family: the first creator, lowercased
    cr = sel11[dirs11[d]["record"]].get("creators") or []
    return cr[0].strip().lower() if cr else f"record:{dirs11[d]['record']}"


qf = np.array([fam_of(d) for d in qd])
printed17 = open(os.path.join(ROOT, "results/session17_outputs.md")).read().splitlines()
for c in ("P1", "P2"):
    s = cells[c]
    here = iv(boot_mean(hit["c"][s] - hit["a"][s], qf[s], SEEDS[c] + CLUSTER_OFFSET, weighted=True))
    want = [ln.rstrip(" |").split("| ")[-1] for ln in printed17 if ln.startswith(f"| E1 | all | c - a | {c} |")]
    same = bool(want) and here == want[0]
    out.append(f"- S11 family-weighted c - a in {c}: here {here}; session 17 {want[0] if want else None}; "
               f"{'same' if same else 'DIFFERENT'}")
    if not same:
        bad.append(("s11 family-weighted", c))
if bad:
    stop(f"NOT REPRODUCED: {bad}. Stopping before any new number.")
out.append("")
out.append("All gates passed.")
out.append("")

# ------------------------------------------------------------------ 1. GitHub at the natural mix


def gh(d):
    R = jl(f"data/ranks_{d}_e1.jsonl.gz")
    F = {r["query_path"]: r for r in jl(f"data/flags_{d}.jsonl.gz")}
    sel = {f"data/corpus_{d}/gh_{r['id']}": r for r in jl(f"data/selection_{d}.jsonl")}
    q_d = np.array([g["relevant_dir"] for g in R])
    assert all(x in sel for x in q_d), f"{d}: a query directory is not in the selection"
    return {"z": np.array([float(g["rank_c"] <= 5) - float(g["rank_a"] <= 5) for g in R]),
            "qd": q_d, "qo": np.array([F[g["query_path"]]["owner"] for g in R]),
            "mixed": np.array([bool(sel[x]["mixed_ext"]) for x in q_d])}


def natural(parts, p, seed, B=10000):
    """Mean over directories of each directory's mean z, within the mixed and the other directories,
    combined with the eligible share p of mixed directories; percentile interval over owner resamples."""
    rows = []
    for P in parts:
        for x in sorted(set(P["qd"])):
            s = P["qd"] == x
            rows.append((P["qo"][s][0], bool(P["mixed"][s][0]), float(P["z"][s].mean())))
    owners = sorted(set(o for o, _, _ in rows))
    oi = {o: i for i, o in enumerate(owners)}
    sm, nm, so, no = (np.zeros(len(owners)) for _ in range(4))
    for o, m, v in rows:
        if m:
            sm[oi[o]] += v
            nm[oi[o]] += 1
        else:
            so[oi[o]] += v
            no[oi[o]] += 1
    point = p * sm.sum() / nm.sum() + (1 - p) * so.sum() / no.sum()
    rng = np.random.default_rng(seed)
    bs = []
    for i0 in range(0, B, 1000):
        i = rng.integers(0, len(owners), size=(min(1000, B - i0), len(owners)))
        bs.append(p * sm[i].sum(1) / nm[i].sum(1) + (1 - p) * so[i].sum(1) / no[i].sum(1))
    lo, hi = np.percentile(np.concatenate(bs), [2.5, 97.5])
    return float(point), float(lo), float(hi), len(owners), int(nm.sum()), int(no.sum())


GH = {d: gh(d) for d in ("s19", "s24")}
out.append("## 1. GitHub at the natural mix (E1, c - a)")
out.append("")
out.append("Owner-weighted: the mean over owners of the owner's mean, 95 percent interval from 10,000 resamples "
           "of owners (s19.oboot). Pooled: both draws' queries, an owner in both counted once.")
out.append("")
out.append("| draw | queries | subset | queries in it | owners | c - a |")
out.append("|---|---:|---|---:|---:|---|")
seed = 25010
for name, parts in (("S19", [GH["s19"]]), ("S24", [GH["s24"]]), ("pooled", [GH["s19"], GH["s24"]])):
    z = np.concatenate([P["z"] for P in parts])
    o = np.concatenate([P["qo"] for P in parts])
    m = np.concatenate([P["mixed"] for P in parts])
    for sname, s in (("all queries", np.ones(len(z), bool)), ("mixed directories", m), ("other directories", ~m)):
        seed += 1
        t = s19.oboot(z[s], o[s], seed)
        out.append(f"| {name} | {len(z)} | {sname} | {int(s.sum())} | {t[3]} | {oiv(t)} |")
out.append("")
out.append("Natural mix: the mean over directories of each directory's mean c - a, within mixed and other "
           "directories, combined with the eligible share of mixed directories; 95 percent interval from 10,000 "
           "resamples of owners. The scored set takes at most two mixed and two other directories per repository, "
           "so each stratum is a sample of its eligible directories, not a uniform draw.")
out.append("")
out.append("| draw | eligible share mixed | mixed directories | other directories | owners | natural-mix c - a | "
           "directory-weighted, mixed | directory-weighted, other |")
out.append("|---|---:|---:|---:|---:|---|---:|---:|")
pooled_eligible = (ELIGIBLE["s19"][0] + ELIGIBLE["s24"][0], ELIGIBLE["s19"][1] + ELIGIBLE["s24"][1])
draws_nat = [("S19", [GH["s19"]], ELIGIBLE["s19"]), ("S24", [GH["s24"]], ELIGIBLE["s24"]),
             ("pooled", [GH["s19"], GH["s24"]], pooled_eligible)]
for k, (name, parts, (mx, al)) in enumerate(draws_nat):
    p = mx / al
    t = natural(parts, p, 25101 + k)
    dm = {True: [], False: []}
    for P in parts:
        for x in sorted(set(P["qd"])):
            s = P["qd"] == x
            dm[bool(P["mixed"][s][0])].append(float(P["z"][s].mean()))
    out.append(f"| {name} | {mx}/{al} = {p:.3f} | {t[4]} | {t[5]} | {t[3]} | {t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}] | "
               f"{np.mean(dm[True]):+.3f} | {np.mean(dm[False]):+.3f} |")
out.append("")

# ------------------------------------------------------------------ 2. and 3. Zenodo (S11)
M = jl("data/manifest_s11.jsonl")
novec = [r for r in M if r.get("note") or r["ext"].lower() in NOVEC_EXT]
by_dir = defaultdict(list)
for r in M:
    if not (r.get("note") or r["ext"].lower() in NOVEC_EXT):
        by_dir[r["dir"]].append((r["path"], r["modality"]))
strict = np.zeros(len(qp), bool)
sib = np.zeros(len(qp), bool)
missing = 0
for k, p in enumerate(qp):
    members = by_dir[qd[k]]
    if not any(x == p for x, _ in members):
        missing += 1
    others = [mm for x, mm in members if x != p]
    strict[k] = max(Counter(others).values(), default=0) > 3
    sib[k] = sum(1 for mm in others if (mm in IMG) == (qm[k] in IMG)) >= 1

out.append("## 2. S11 where c is a strict compression (E1, c_f32 - d_f32)")
out.append("")
out.append(f"Files without a vector by the manifest rule: {len(novec)} of {len(M)}. Evaluation queries the rule "
           f"counts as without a vector: {missing} of {len(qp)}. A query's folder compresses strictly if, the query "
           f"left out, some label keeps more than three files: {int(strict.sum())} of {len(qp)} queries "
           f"({strict.mean():.3f}) over {len(set(qd[strict]))} of {len(set(qd))} directories.")
out.append("")
out.append("| cell | queries | strict | share strict | c - d, strict [95% directories] | c - d, not strict [95%] | "
           "c - d, all [95%] |")
out.append("|---|---:|---:|---:|---|---|---|")
for c in CELLS:
    s = cells[c]
    z = hit["c"] - hit["d"]
    a_ = boot_mean(z[s & strict], qd[s & strict], SEEDS[c])
    b_ = boot_mean(z[s & ~strict], qd[s & ~strict], SEEDS[c])
    c_ = boot_mean(z[s], qd[s], SEEDS[c])
    out.append(f"| {c} | {int(s.sum())} | {int((s & strict).sum())} | {(s & strict).sum() / s.sum():.3f} | "
               f"{iv(a_)} | {iv(b_)} | {iv(c_)} |")
out.append("")

out.append("## 3. S11 read as the GitHub draws are read (E1, c - a)")
out.append("")
out.append("P1s and P2s keep the queries whose folder, the query left out, holds another file of the query's input "
           "group (same file count as item 2). Family-weighted: every creator family counts once, 95 percent "
           "interval from 1,000 resamples of families (validity.boot_mean, weighted). Query-weighted: the paper's "
           "estimate, with eval.py's directory interval.")
out.append("")
out.append("| cell | queries | directories | families (effective) | query-weighted [95% directories] | "
           "family-weighted [95% families] |")
out.append("|---|---:|---:|---|---|---|")
z = hit["c"] - hit["a"]
for name, s, base in (("P1", cells["P1"], "P1"), ("P2", cells["P2"], "P2"),
                      ("P1s", cells["P1"] & sib, "P1"), ("P2s", cells["P2"] & sib, "P2")):
    q_ = boot_mean(z[s], qd[s], SEEDS[base])
    f_ = boot_mean(z[s], qf[s], SEEDS[base] + CLUSTER_OFFSET, weighted=True)
    out.append(f"| {name} | {int(s.sum())} | {len(set(qd[s]))} | {len(set(qf[s]))} ({eff_families(qf[s]):.0f}) | "
               f"{iv(q_)} | {iv(f_)} |")
out.append(f"")
out.append(f"Lone queries (no other file of their input group in the folder): P1 {int((cells['P1'] & ~sib).sum())} "
           f"of {int(cells['P1'].sum())}, P2 {int((cells['P2'] & ~sib).sum())} of {int(cells['P2'].sum())}.")
out.append("")

# ------------------------------------------------------------------ 4. the budget curve
out.append("## 4. A budget curve (E1): recall@5 by bytes per folder")
out.append("")
out.append("Session 21's per-query ranks. S11 query-weighted; GitHub owner-weighted (both draws' queries, an owner "
           "in both counted once). Minority: P1s and P2s.")
out.append("")
curves = {}
mino11 = (cells["P1"] | cells["P2"]) & sib
curves["S11"] = (R11, np.ones(len(R11), bool), mino11, None)
ghr, ghall, ghmin, gho = [], [], [], []
for d in ("s19", "s24"):
    BR = jl(f"data/ranks_s21_{d}_e1.jsonl.gz")
    G = {g["query_path"]: g for g in jl(f"data/ranks_{d}_e1.jsonl.gz")}
    F = {r["query_path"]: r for r in jl(f"data/flags_{d}.jsonl.gz")}
    dirs = {r["dir"]: r for r in jl(f"data/dirs_{d}.jsonl")}
    bm = np.array([G[b["query_path"]]["modality"] for b in BR])
    bb = np.array([G[b["query_path"]]["image_frac_bucket"] for b in BR])
    primary, _, _, _ = ev.s3_cells(bb, bm)
    bsib = np.array([F[b["query_path"]]["sib_same"] >= 1 for b in BR])
    ghr += BR
    ghall.append(np.ones(len(BR), bool))
    ghmin.append((primary[0][1] & bsib) | (primary[1][1] & bsib))
    gho.append(np.array([dirs[b["relevant_dir"]]["owner"] for b in BR]))
curves["GitHub"] = (ghr, np.concatenate(ghall), np.concatenate(ghmin), np.concatenate(gho))
for name, (RR, alls, mino, owners) in curves.items():
    out.append(f"### {name}: {len(RR)} queries, {int(mino.sum())} minority"
               + (f", {len(set(owners))} owners ({len(set(owners[mino]))} in the minority cell)" if owners is not None else ""))
    out.append("")
    out.append("| summary | " + " | ".join(f"{B} B, all | {B} B, minority" for B in BUDGETS) + " |")
    out.append("|---|" + "---:|---:|" * len(BUDGETS))
    for pol in CURVE:
        cols = []
        for B in BUDGETS:
            h = np.array([r[f"rank_{pol}@{B}"] <= 5 for r in RR], float)
            for s in (alls, mino):
                cols.append(f"{(h[s].mean() if owners is None else owner_mean(h[s], owners[s])):.3f}")
        out.append(f"| {pol} | " + " | ".join(cols) + " |")
    out.append("")
out.append("### Labels against blind centroids at 2,048 bytes: kkind - kmeans (95 percent interval; directories on "
           "S11, owners on GitHub)")
out.append("")
out.append("| set | all | minority |")
out.append("|---|---|---|")
for k, (name, (RR, alls, mino, owners)) in enumerate(curves.items()):
    zz = (np.array([r["rank_kkind@2048"] <= 5 for r in RR], float) -
          np.array([r["rank_kmeans@2048"] <= 5 for r in RR], float))
    cols = []
    for j, s in enumerate((alls, mino)):
        if owners is None:
            dd = np.array([r["relevant_dir"] for r in RR])
            cols.append(iv(boot_mean(zz[s], dd[s], 25201 + 10 * k + j)))
        else:
            t = s19.oboot(zz[s], owners[s], 25201 + 10 * k + j)
            cols.append(f"{oiv(t)} ({t[3]} owners)")
    out.append(f"| {name} | {cols[0]} | {cols[1]} |")
out.append("")
print("\n".join(out))


# ------------------------------------------------------------------ 5. the number of candidate folders
from scipy.special import gammaln  # noqa: E402


def lchoose(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def exp_hit5(r, N, n):
    """Expected hit@5 when the candidates are the own folder and n - 1 of the other N - 1 folders,
    drawn uniformly without replacement: P(at most 4 of the r - 1 folders above it are drawn)."""
    r = np.asarray(r, float)
    N = np.asarray(N, float) * np.ones_like(r)
    if n >= N.max():
        return (r <= 5).astype(float)
    above, below = r - 1, N - r
    tot = lchoose(N - 1, n - 1)
    p = np.zeros_like(r)
    for k in range(5):
        ok = (k <= above) & (n - 1 - k <= below) & (n - 1 - k >= 0)
        term = np.where(ok, np.exp(lchoose(np.maximum(above, k), k) + lchoose(np.maximum(below, n - 1 - k), n - 1 - k) - tot), 0.0)
        p += term
    return np.clip(p, 0, 1)


SIZES = [10, 30, 100, 300, 1000, None]
out2 = ["## 5. The number of candidate folders (E1, post hoc; BRIEF.md, session 25, item 5)", "",
        "Expected recall@5 when the candidates are the own folder and n - 1 others drawn at random.", ""]
rk11 = {x: np.array([r[f"rank_{x}_f32"] for r in R11], float) for x in "acd"}
out2.append("### S11 (N = 2,597), query-weighted; c - a with its 95 percent directory interval")
out2.append("")
out2.append("| candidates | cell | a | c | d | c - a |")
out2.append("|---:|---|---:|---:|---:|---|")
for j, n in enumerate(SIZES):
    nn = 2597 if n is None else n
    E = {x: exp_hit5(rk11[x], 2597, nn) for x in "acd"}
    for c in ("all", "P1", "P2"):
        s = cells[c]
        t = boot_mean(E["c"][s] - E["a"][s], qd[s], 25300 + 10 * j + CELLS.index(c))
        out2.append(f"| {nn} | {c} | {E['a'][s].mean():.3f} | {E['c'][s].mean():.3f} | {E['d'][s].mean():.3f} | {iv(t)} |")
out2.append("")
G_r, G_N, G_o, G_cell = {x: [] for x in "acd"}, [], [], []
for d, N in (("s19", 1600), ("s24", 2600)):
    R = jl(f"data/ranks_{d}_e1.jsonl.gz")
    F = {r["query_path"]: r for r in jl(f"data/flags_{d}.jsonl.gz")}
    cm = cells_of(np.array([g["modality"] for g in R]), np.array([g["image_frac_bucket"] for g in R]))
    sb = np.array([F[g["query_path"]]["sib_same"] >= 1 for g in R])
    for x in "acd":
        G_r[x].append(np.array([g[f"rank_{x}"] for g in R], float))
    G_N.append(np.full(len(R), N, float))
    G_o.append(np.array([F[g["query_path"]]["owner"] for g in R]))
    G_cell.append({"all": np.ones(len(R), bool), "P1s": cm["P1"] & sb, "P2s": cm["P2"] & sb})
G_r = {x: np.concatenate(v) for x, v in G_r.items()}
G_N, G_o = np.concatenate(G_N), np.concatenate(G_o)
G_cell = {c: np.concatenate([m[c] for m in G_cell]) for c in ("all", "P1s", "P2s")}
out2.append("### GitHub (G1 N = 1,600, G2 N = 2,600), owner-weighted over both draws; c - a with its 95 percent owner interval")
out2.append("")
out2.append("| candidates | cell | a | c | d | c - a |")
out2.append("|---:|---|---:|---:|---:|---|")
for j, n in enumerate(SIZES):
    E = {}
    for x in "acd":
        if n is None:
            E[x] = (G_r[x] <= 5).astype(float)
        else:
            E[x] = np.concatenate([exp_hit5(G_r[x][G_N == N], N, n) for N in (1600.0, 2600.0)])
    order = np.concatenate([np.where(G_N == N)[0] for N in (1600.0, 2600.0)])
    E = {x: v[np.argsort(order)] for x, v in E.items()} if n is not None else E
    label = "full" if n is None else n
    for k, c in enumerate(("all", "P1s", "P2s")):
        s = G_cell[c]
        t = s19.oboot(E["c"][s] - E["a"][s], G_o[s], 25400 + 10 * j + k)
        out2.append(f"| {label} | {c} | {owner_mean(E['a'][s], G_o[s]):.3f} | {owner_mean(E['c'][s], G_o[s]):.3f} | "
                    f"{owner_mean(E['d'][s], G_o[s]):.3f} | {oiv(t)} |")
out2.append("")
print("\n".join(out2))
