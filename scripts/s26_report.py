#!/usr/bin/env python3
"""The report of session 26 (BRIEF.md, session 26), from the npz files of `s26.py score`.

  python3 scripts/s26.py report data/s26_*.npz > results/session26_outputs.md

Nothing here needs a vector. A set whose gates failed is listed as FAILED and none of its numbers is
printed.
"""
import json
import os
import sys

import numpy as np
from scipy.stats import hypergeom

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validity import CLUSTER_OFFSET, SEEDS, boot_mean, cells_of  # noqa: E402

ELIGIBLE = {"s19": (1501, 35970), "s24": (3286, 65984)}   # mixed and all eligible directories (session 25)
N_M_BRIEF = {"s19": 26, "s24": 31}                         # natural-mix mixed candidates, as the brief states
NAMES_S11 = (0.700, 0.617, 0.587, 0.786, 0.688)
POL = ("a", "c", "d", "m", "m2", "u")
FUSE = ("a", "c", "d", "m")
CELLS = ("all", "P1", "P2", "M1", "M2")
SESOI, NI_MARGIN, MIN_OWNERS = 0.05, 0.005, 100
Q98 = (100 * 0.05 / 6, 100 * (1 - 0.05 / 6))
out = []


def p(line=""):
    out.append(line)


def load(path):
    z = np.load(path, allow_pickle=False)
    d = {k: z[k] for k in z.files}
    d["meta"] = json.loads(str(d["meta"]))
    d["path"] = path
    return d


def oboot(z, owners, seed, B=10000):
    """s19.oboot: mean over owners of the owner's mean; 95 and 98.33 percent percentile intervals."""
    keys = sorted(set(owners))
    gi = {k: i for i, k in enumerate(keys)}
    g = np.array([gi[k] for k in owners])
    gm = np.bincount(g, weights=z, minlength=len(keys)) / np.bincount(g, minlength=len(keys))
    rng = np.random.default_rng(seed)
    bs = np.empty(B)
    for i0 in range(0, B, 1000):
        idx = rng.integers(0, len(keys), size=(min(1000, B - i0), len(keys)))
        bs[i0:i0 + len(idx)] = gm[idx].mean(axis=1)
    q = np.percentile(bs, [2.5, 97.5, Q98[0], Q98[1]])
    return float(gm.mean()), (float(q[0]), float(q[1])), (float(q[2]), float(q[3])), len(keys)


def natural(parts, pm, seed, B=10000):
    """Session 25's natural-mix estimator (s25.natural) with the 98.33 percent interval added: within
    the mixed and the other stratum the mean over directories of each directory's mean z, combined
    with the eligible share pm; percentile intervals over 10,000 resamples of owners."""
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
    point = pm * sm.sum() / nm.sum() + (1 - pm) * so.sum() / no.sum()
    rng = np.random.default_rng(seed)
    bs = []
    for i0 in range(0, B, 1000):
        i = rng.integers(0, len(owners), size=(min(1000, B - i0), len(owners)))
        bs.append(pm * sm[i].sum(1) / nm[i].sum(1) + (1 - pm) * so[i].sum(1) / no[i].sum(1))
    bs = np.concatenate(bs)
    lo, hi, lo98, hi98 = np.percentile(bs, [2.5, 97.5, Q98[0], Q98[1]])
    return float(point), (float(lo), float(hi)), (float(lo98), float(hi98)), len(owners), int(nm.sum()), int(no.sum())


def f3(x):
    return f"{x:+.3f}"


def ivs(t, both=True):
    s = f"{t[0]:+.3f} [{t[1][0]:+.3f}, {t[1][1]:+.3f}]"
    return s + (f" [{t[2][0]:+.3f}, {t[2][1]:+.3f}]" if both else "")


# ------------------------------------------------------------------ expected hits
def hits(D, setting):
    """{policy: per-query hit@5} for a GitHub set: 'scored' (every folder of the draw), 'natural'
    (every other-stratum folder and N_m mixed ones) or 'natural100'."""
    meta = D["meta"]
    s = D["stratum_own"].astype(int)
    n_m = meta["n_mixed_stratum"]
    n_o = meta["n_ranked"] - n_m
    pm = ELIGIBLE[meta["set"]][0] / ELIGIBLE[meta["set"]][1]
    avail_m, avail_o = n_m - s, n_o - (1 - s)
    out_ = {}
    for x in POL:
        r = D[f"rank_{x}"]
        hm = D[f"hm_{x}"]
        ho = r - 1 - hm
        if setting == "scored":
            out_[x] = (r <= 5).astype(float)
        elif setting == "natural":
            N_m = int(round(n_o * pm / (1 - pm)))
            assert N_m == N_M_BRIEF[meta["set"]], (meta["set"], N_m)
            # every other-stratum folder is a candidate, so exactly ho of them are above the own folder
            out_[x] = np.where(ho <= 4, hypergeom.cdf(np.maximum(4 - ho, 0), avail_m, hm, N_m), 0.0)
        else:
            N_m = int(round(99 * pm))
            N_o = 99 - N_m
            e = np.zeros(len(r))
            for j in range(5):
                e += hypergeom.pmf(j, avail_m, hm, N_m) * hypergeom.cdf(4 - j, avail_o, ho, N_o)
            out_[x] = e
    return out_


def gh_cells(D):
    c = cells_of(D["modality"], D["bucket"])
    sib = D["sib_same"] >= 1
    return {"P1s": c["P1"] & sib, "P2s": c["P2"] & sib, "all": np.ones(len(sib), bool)}


# ------------------------------------------------------------------ report
def report(paths):
    sets = {}
    for pth in paths:
        if not os.path.exists(pth):
            continue
        D = load(pth)
        sets[(D["meta"]["set"], D["meta"]["enc"])] = D
    p("# Session 26 outputs, verbatim (scripts/s26.py report)")
    p()
    p("Files read: " + ", ".join(sorted(os.path.basename(D["path"]) for D in sets.values())) + ".")
    p()
    p("## Gates")
    p()
    p("| set | encoder | queries | ranked folders | mixed stratum | mixed by the rule | a, c, d ranks differing | "
      "name ranks differing | sibling counts differing | seconds | commit | gate |")
    p("|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|")
    ok = {}
    for key in sorted(sets):
        D = sets[key]
        m, g = D["meta"], D["meta"]["gate"]
        passed = bool(g["pass"])
        note = ""
        if key[0] == "s11":
            c = cells_of(D["modality"], D["bucket"])
            got = tuple(round(float((D["name_rank"][c[x]] <= 5).mean()), 3) for x in CELLS)
            same = got == NAMES_S11
            passed = passed and same
            note = (f"; names recall@5 ({', '.join(f'{v:.3f}' for v in got)}) against "
                    f"({', '.join(f'{v:.3f}' for v in NAMES_S11)}): {'same' if same else 'DIFFERENT'}")
        ok[key] = passed
        p(f"| {key[0].upper()} | {key[1]} | {g['queries_here']} (check {g['queries_check']}) | {m['n_ranked']} | "
          f"{m['n_mixed_stratum']} | {m['n_mixed_rule']} | {g['differ_a']}, {g['differ_c']}, {g['differ_d']} "
          f"({g['key_a'].replace('rank_a', '').strip('_') or 'eval.py rows'}) | {g.get('names_differ', 'n/a')} | "
          f"{g.get('sib_same_differ', 'n/a')} | {m['seconds']} | {m['commit']} | {'pass' if passed else 'FAILED'}{note} |")
    p()
    bad = [k for k, v in ok.items() if not v]
    if bad:
        p("FAILED: " + ", ".join(f"{a.upper()} {b}" for a, b in bad) + ". None of their numbers is reported below.")
        p()
    good = {k: v for k, v in sets.items() if ok[k]}

    # ---------------------------------------------------------- 1. primary
    p("## 1. Primary: E1, G1 and G2 pooled, natural-mix candidates")
    p()
    prim = [good.get(("s19", "E1")), good.get(("s24", "E1"))]
    verdicts = {}
    if any(x is None for x in prim):
        p("S19 or S24 under E1 is missing or failed a gate: H26a to H26c have no verdict.")
        p()
    else:
        for D in prim:
            m = D["meta"]
            n_m = m["n_mixed_stratum"]
            n_o = m["n_ranked"] - n_m
            pm = ELIGIBLE[m["set"]][0] / ELIGIBLE[m["set"]][1]
            p(f"- {m['set'].upper()}: {m['n_ranked']} folders, {n_m} mixed and {n_o} other; eligible share {pm:.4f}; "
              f"natural-mix candidates: every other folder and {int(round(n_o * pm / (1 - pm)))} mixed ones drawn at "
              f"random ({n_o + int(round(n_o * pm / (1 - pm)))} with the own folder counted once); 100 candidates: "
              f"{int(round(99 * pm))} mixed and {99 - int(round(99 * pm))} other besides the own folder.")
        p()
        pooled_pm = (ELIGIBLE["s19"][0] + ELIGIBLE["s24"][0]) / (ELIGIBLE["s19"][1] + ELIGIBLE["s24"][1])
        H = {st: [hits(D, st) for D in prim] for st in ("natural", "natural100", "scored")}
        cells = [gh_cells(D) for D in prim]
        owners = np.concatenate([D["grp"] for D in prim])
        qd = np.concatenate([D["qdirname"] for D in prim])
        mixed = np.concatenate([D["stratum_own"] for D in prim])
        cat = lambda st, x: np.concatenate([h[x] for h in H[st]])  # noqa: E731
        cel = {c: np.concatenate([cc[c] for cc in cells]) for c in ("P1s", "P2s", "all")}

        def nat(st, x, y, seed, pm=pooled_pm, sub=None):
            parts = []
            for D, h in zip(prim if sub is None else [prim[sub]], H[st] if sub is None else [H[st][sub]]):
                parts.append({"z": h[x] - h[y], "qd": D["qdirname"], "qo": D["grp"], "mixed": D["stratum_own"]})
            return natural(parts, pm, seed)

        tA = oboot(cat("natural", "m")[cel["P1s"]] - cat("natural", "a")[cel["P1s"]], owners[cel["P1s"]], 26001)
        tB = oboot(cat("natural", "m")[cel["P2s"]] - cat("natural", "a")[cel["P2s"]], owners[cel["P2s"]], 26002)
        tC = nat("natural", "m", "a", 26003)
        tD = nat("natural", "m", "c", 26004)
        p("| test | estimate | queries | owners | point | 95% | 98.33% |")
        p("|---|---|---:|---:|---:|---|---|")
        p(f"| H26a | P1s: m - a, owner-weighted | {int(cel['P1s'].sum())} | {tA[3]} | {f3(tA[0])} | "
          f"[{tA[1][0]:+.3f}, {tA[1][1]:+.3f}] | [{tA[2][0]:+.3f}, {tA[2][1]:+.3f}] |")
        p(f"| H26a | P2s: m - a, owner-weighted | {int(cel['P2s'].sum())} | {tB[3]} | {f3(tB[0])} | "
          f"[{tB[1][0]:+.3f}, {tB[1][1]:+.3f}] | [{tB[2][0]:+.3f}, {tB[2][1]:+.3f}] |")
        p(f"| H26b | all queries at the natural mix: m - a | {len(owners)} | {tC[3]} | {f3(tC[0])} | "
          f"[{tC[1][0]:+.3f}, {tC[1][1]:+.3f}] | [{tC[2][0]:+.3f}, {tC[2][1]:+.3f}] |")
        p(f"| H26c | all queries at the natural mix: m - c | {len(owners)} | {tD[3]} | {f3(tD[0])} | "
          f"[{tD[1][0]:+.3f}, {tD[1][1]:+.3f}] | [{tD[2][0]:+.3f}, {tD[2][1]:+.3f}] |")
        p()
        p(f"Natural-mix strata: {tC[4]} mixed and {tC[5]} other directories with evaluation queries, pooled eligible share "
          f"{pooled_pm:.4f}.")
        p()

        def conf(t):
            if t[3] < MIN_OWNERS:
                return f"inconclusive (fewer than {MIN_OWNERS} owners)"
            if t[2][0] >= SESOI:
                return "confirmed (lower bound at or above +0.05)"
            if t[2][1] < SESOI:
                return "below +0.05 (upper bound under +0.05)"
            return "present, size open" if t[2][0] > 0 else "inconclusive"
        a1, a2 = conf(tA), conf(tB)
        verdicts["H26a"] = "confirmed in both cells" if a1.startswith("confirmed") and a2.startswith("confirmed") else \
            f"not confirmed (P1s {a1}; P2s {a2})"
        verdicts["H26b"] = (f"not inferior (lower bound {tC[2][0]:+.4f} at or above -{NI_MARGIN})" if tC[2][0] >= -NI_MARGIN
                            else f"FAILED: lower bound {tC[2][0]:+.4f} below -{NI_MARGIN}")
        verdicts["H26c"] = (f"above zero (lower bound {tD[2][0]:+.4f})" if tD[2][0] > 0
                            else f"FAILED: lower bound {tD[2][0]:+.4f} not above zero")
        p("### Verdicts")
        p()
        p(f"- H26a (m - a in P1s and P2s, 98.33%, lower bound at least +0.05): P1s {a1}; P2s {a2}. H26a: {verdicts['H26a']}.")
        p(f"- H26b (m - a over all queries at the natural mix, 98.33%, lower bound at least -0.005): {verdicts['H26b']}.")
        p(f"- H26c (m - c over all queries at the natural mix, 98.33%, lower bound above zero): {verdicts['H26c']}.")
        p()

        # ------------------------------------------------------ 2. secondary
        p("## 2. Secondary, E1 (G1 and G2)")
        p()
        p("### Recall@5 by policy")
        p()
        p("All at the natural mix: the stratum-weighted estimator over all queries. P1s and P2s: owner-weighted. "
          "Pooled over G1 and G2.")
        p()
        p("| candidates | estimate | " + " | ".join(POL) + " |")
        p("|---|---|" + "---:|" * len(POL))
        for st, lab in (("natural", "natural mix"), ("natural100", "natural mix, 100"), ("scored", "scored set")):
            row = []
            for x in POL:
                parts = [{"z": h[x], "qd": D["qdirname"], "qo": D["grp"], "mixed": D["stratum_own"]} for D, h in zip(prim, H[st])]
                row.append(natural(parts, pooled_pm, 26100, B=1000)[0])
            p(f"| {lab} | all at the natural mix | " + " | ".join(f"{v:.3f}" for v in row) + " |")
            for c in ("P1s", "P2s"):
                s = cel[c]
                row = [oboot(cat(st, x)[s], owners[s], 26101, B=1000)[0] for x in POL]
                p(f"| {lab} | {c} | " + " | ".join(f"{v:.3f}" for v in row) + " |")
        p()
        p("### Differences (95 percent intervals, 10,000 resamples of owners)")
        p()
        p("| candidates | draw | estimate | m - a | m - c | m2 - a | u - a | c - a |")
        p("|---|---|---|---|---|---|---|---|")
        seed = 26200
        for st, lab in (("natural", "natural mix"), ("natural100", "natural mix, 100"), ("scored", "scored set")):
            for di, dname in ((None, "pooled"), (0, "G1"), (1, "G2")):
                pm_ = pooled_pm if di is None else ELIGIBLE[prim[di]["meta"]["set"]][0] / ELIGIBLE[prim[di]["meta"]["set"]][1]
                row = []
                for x, y in (("m", "a"), ("m", "c"), ("m2", "a"), ("u", "a"), ("c", "a")):
                    seed += 1
                    row.append(ivs(nat(st, x, y, seed, pm_, di), both=False))
                p(f"| {lab} | {dname} | all at the natural mix | " + " | ".join(row) + " |")
                hsel = H[st] if di is None else [H[st][di]]
                own_ = owners if di is None else prim[di]["grp"]
                cel_ = cel if di is None else cells[di]
                mix_ = mixed if di is None else prim[di]["stratum_own"]
                for c, extra in (("P1s", None), ("P2s", None), ("all", None), ("all", True), ("all", False)):
                    s = cel_[c] if extra is None else (cel_[c] & (mix_ == extra))
                    name = c if extra is None else ("queries of mixed directories" if extra else "queries of other directories")
                    if c == "all" and extra is None:
                        name = "all queries, owner-weighted"
                    row = []
                    for x, y in (("m", "a"), ("m", "c"), ("m2", "a"), ("u", "a"), ("c", "a")):
                        seed += 1
                        z = np.concatenate([h[x] for h in hsel]) - np.concatenate([h[y] for h in hsel])
                        row.append(ivs(oboot(z[s], own_[s], seed), both=False))
                    p(f"| {lab} | {dname} | {name} | " + " | ".join(row) + " |")
        p()
        # session 25's estimate, reproduced from these ranks
        t25 = natural([{"z": h["c"] - h["a"], "qd": D["qdirname"], "qo": D["grp"], "mixed": D["stratum_own"]}
                       for D, h in zip(prim, H["scored"])], pooled_pm, 25103)
        p(f"Check: session 25's natural-mix c - a with the scored sets' candidates (seed 25103), recomputed from these "
          f"ranks: {t25[0]:+.3f} [{t25[1][0]:+.3f}, {t25[1][1]:+.3f}] (session 25: -0.014 [-0.022, -0.005]).")
        p()
        p("H26a to H26c on 98.33% intervals with the other candidate settings (no verdict, for the reading):")
        p()
        for st, lab in (("natural100", "natural mix, 100 candidates"), ("scored", "scored set")):
            a = oboot(cat(st, "m")[cel["P1s"]] - cat(st, "a")[cel["P1s"]], owners[cel["P1s"]], 26301)
            b = oboot(cat(st, "m")[cel["P2s"]] - cat(st, "a")[cel["P2s"]], owners[cel["P2s"]], 26302)
            c_ = nat(st, "m", "a", 26303)
            d_ = nat(st, "m", "c", 26304)
            p(f"- {lab}: P1s m - a {ivs(a)}; P2s m - a {ivs(b)}; all, m - a {ivs(c_)}; all, m - c {ivs(d_)}.")
        p()

    # ---------------------------------------------------------- 2b. G1 under E4 and E2
    for enc in ("E4", "E2"):
        D = good.get(("s19", enc))
        if D is None:
            p(f"## 2b. G1 under {enc}: missing or failed a gate.")
            p()
            continue
        p(f"## 2b. G1 under {enc} (secondary)")
        p()
        pm = ELIGIBLE["s19"][0] / ELIGIBLE["s19"][1]
        cl = gh_cells(D)
        p("| candidates | estimate | m - a | m - c | m2 - a | u - a | c - a |")
        p("|---|---|---|---|---|---|---|")
        seed = 26400 + (0 if enc == "E4" else 100)
        for st, lab in (("natural", "natural mix"), ("scored", "scored set")):
            h = hits(D, st)
            row = []
            for x, y in (("m", "a"), ("m", "c"), ("m2", "a"), ("u", "a"), ("c", "a")):
                seed += 1
                row.append(ivs(natural([{"z": h[x] - h[y], "qd": D["qdirname"], "qo": D["grp"], "mixed": D["stratum_own"]}],
                                       pm, seed), both=False))
            p(f"| {lab} | all at the natural mix | " + " | ".join(row) + " |")
            for c in ("P1s", "P2s"):
                s = cl[c]
                row = []
                for x, y in (("m", "a"), ("m", "c"), ("m2", "a"), ("u", "a"), ("c", "a")):
                    seed += 1
                    row.append(ivs(oboot((h[x] - h[y])[s], D["grp"][s], seed), both=False) + f" ({len(set(D['grp'][s]))})")
                p(f"| {lab} | {c} | " + " | ".join(row) + " |")
        p()

    # ---------------------------------------------------------- 3. names with vectors
    p("## 3. Names with vectors: reciprocal rank fusion (k = 60), scored sets")
    p()
    p("### Zenodo confirmation set (S11), recall@5")
    p()
    for enc in ("E1", "E2", "E3", "E4"):
        D = good.get(("s11", enc))
        if D is None:
            p(f"- S11 {enc}: missing or failed a gate.")
            continue
        c = cells_of(D["modality"], D["bucket"])
        p(f"#### {enc}")
        p()
        p("| row | " + " | ".join(CELLS) + " |")
        p("|---|" + "---:|" * len(CELLS))
        rows = [("names alone", D["name_rank"])] + [(x, D[f"rank_{x}"]) for x in POL] + \
               [(f"names + {x}", D[f"rrf_{x}"]) for x in FUSE]
        for name, r in rows:
            p(f"| {name} | " + " | ".join(f"{(r[c[x]] <= 5).mean():.3f}" for x in CELLS) + " |")
        p()
        qd, fam = D["qdirname"], D["grp"]
        p("| difference | cell | point | directory 95% | creator-clustered 95% |")
        p("|---|---|---:|---|---|")
        res = {}
        for (x, y, lab) in (("rrf_c", "rrf_a", "names + c minus names + a"), ("rrf_d", "rrf_a", "names + d minus names + a"),
                            ("rrf_c", "rrf_d", "names + c minus names + d"), ("rank_c", "rank_a", "c - a (no names)"),
                            ("rank_m", "rank_c", "m - c (no names)")):
            for cell in ("all", "P1", "P2", "M1", "M2"):
                s = c[cell]
                z = (D[x] <= 5).astype(float) - (D[y] <= 5).astype(float)
                t1 = boot_mean(z[s], qd[s], SEEDS[cell])
                t2 = boot_mean(z[s], fam[s], SEEDS[cell] + CLUSTER_OFFSET)
                res[(lab, cell)] = (t1, t2)
                p(f"| {lab} | {cell} | {t1[0]:+.3f} | [{t1[1]:+.3f}, {t1[2]:+.3f}] | [{t2[1]:+.3f}, {t2[2]:+.3f}] |")
        p()
        if enc in ("E1", "E3"):
            vv = []
            for cell in ("P1", "P2"):
                t1, t2 = res[("names + c minus names + a", cell)]
                vv.append((cell, t1[0] >= SESOI and t2[1] > 0, t1[0], t2[1]))
            verdict = "survived" if all(v[1] for v in vv) else "died"
            verdicts[f"H26d {enc}"] = verdict
            p(f"H26d ({enc}): " + "; ".join(f"{cell} fused c - a {pt:+.3f}, creator-clustered lower bound {lo:+.3f}"
                                           for cell, _, pt, lo in vv) + f". H26d under {enc}: {verdict}.")
            p()
    p("### GitHub (E1), owner-weighted recall@5 and fused c - a")
    p()
    gh = [(n, good.get((n, "E1"))) for n in ("s19", "s24")]
    gh = [(n, D) for n, D in gh if D is not None]
    if gh:
        p("| draw | estimate | names alone | a | c | d | m | names + a | names + c | names + d | names + m |")
        p("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n, D in gh:
            cl = gh_cells(D)
            for c in ("all", "P1s", "P2s"):
                s = cl[c]
                vals = [D["name_rank"]] + [D[f"rank_{x}"] for x in ("a", "c", "d", "m")] + [D[f"rrf_{x}"] for x in FUSE]
                p(f"| {n.upper()} | {c} | " + " | ".join(f"{oboot((v[s] <= 5).astype(float), D['grp'][s], 26500, B=1000)[0]:.3f}"
                                                       for v in vals) + " |")
        p()
        p("| draw | cell | names + c minus names + a | c - a (no names) | owners |")
        p("|---|---|---|---|---:|")
        seed = 26600
        own_all = np.concatenate([D["grp"] for _, D in gh])
        for c in ("P1s", "P2s"):
            for n, D in gh + [("pooled", None)]:
                if D is None:
                    s = np.concatenate([gh_cells(E)[c] for _, E in gh])
                    zf = np.concatenate([(E["rrf_c"] <= 5).astype(float) - (E["rrf_a"] <= 5) for _, E in gh])
                    zv = np.concatenate([(E["rank_c"] <= 5).astype(float) - (E["rank_a"] <= 5) for _, E in gh])
                    o = own_all
                else:
                    s = gh_cells(D)[c]
                    zf = (D["rrf_c"] <= 5).astype(float) - (D["rrf_a"] <= 5)
                    zv = (D["rank_c"] <= 5).astype(float) - (D["rank_a"] <= 5)
                    o = D["grp"]
                seed += 2
                t1, t2 = oboot(zf[s], o[s], seed), oboot(zv[s], o[s], seed + 1)
                p(f"| {n.upper()} | {c} | {ivs(t1, both=False)} | {ivs(t2, both=False)} | {t1[3]} |")
        p()
    p("## Verdicts in one place")
    p()
    for k in ("H26a", "H26b", "H26c", "H26d E1", "H26d E3"):
        p(f"- {k}: {verdicts.get(k, 'no verdict (missing input or a failed gate)')}")
    print("\n".join(out))
    return 0
