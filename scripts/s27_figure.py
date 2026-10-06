#!/usr/bin/env python3
"""The figure of session 27B: recall@5 against vectors per folder, from the per-query files of s27.py.

  python3 scripts/s27_figure.py data/s27_s11_e1.npz data/s27_s11_e2.npz ... --out results/session27_budget

Writes <out>.png and <out>.pdf: rows are encoders, columns the cells (all, P1, P2, M1, M2); in each panel
the labelled rows Lk (solid), the blind rows BK (dashed) and the blind rows at the labelled budget Mk
(dotted) against the mean number of vectors per folder; a at one vector and d at all files as points, d's
level as a thin line. --centered draws the centered rows instead. Nothing is computed here that the
report does not print.
"""
import argparse
import json
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s27  # noqa: E402

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
COLOR = {"E1": "#2a78d6", "E2": "#eb6834", "E3": "#1baf7a", "E4": "#eda100"}
NAME = {"E1": "E1 jina-v4", "E2": "E2 jina-clip-v2", "E3": "E3 GME", "E4": "E4 Nomic"}
CELLS = ("all", "P1", "P2", "M1", "M2")
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7, "axes.edgecolor": AXIS,
    "axes.linewidth": 0.8, "xtick.color": INK2, "ytick.color": INK2, "axes.labelcolor": INK2,
    "pdf.fonttype": 42, "savefig.dpi": 200, "axes.titleweight": "bold", "axes.titlelocation": "left",
})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--centered", action="store_true")
    args = ap.parse_args()
    sets = {}
    for p in args.npz:
        d = s27.load_npz(p)
        if d["meta"]["kind"] == "budget" and d["meta"]["set"] == "s11" and d["meta"]["gate"]["pass"]:
            sets[d["meta"]["enc"]] = d
    encs = [e for e in ("E1", "E2", "E3", "E4") if e in sets]
    sfx = "c" if args.centered else ""
    fig, axes = plt.subplots(len(encs), len(CELLS), figsize=(7.2, 1.55 * len(encs) + 0.5), sharex=True, squeeze=False)
    for i, e in enumerate(encs):
        d = sets[e]
        cs = s27.s11_cells(d["modality"], d["bucket"])
        nv = d["meta"]["nvec"]
        col = COLOR[e]
        for j, c in enumerate(CELLS):
            ax = axes[i][j]
            sel = cs[c]

            def r5(r):
                return float((d[f"rank_{r}"][sel] <= 5).mean())
            ref_a, ref_d = "a" + sfx, "d" + sfx
            ax.axhline(r5(ref_d), color=MUTED, lw=0.6, ls=(0, (1, 2)), zorder=1)
            for fam, ks, ls in (("L", s27.LK, "-"), ("B", s27.BK, "--"), ("M", s27.LK, ":")):
                rows = [f"{fam}{k}{sfx}" for k in ks if f"rank_{fam}{k}{sfx}" in d]
                ax.plot([nv[r] for r in rows], [r5(r) for r in rows], ls=ls, color=col if fam == "L" else INK2,
                        lw=1.4 if fam == "L" else 1.0, marker="o" if fam == "L" else None, ms=2.6, zorder=3 if fam == "L" else 2)
            ax.plot([nv[ref_a]], [r5(ref_a)], "D", ms=3.2, color="white", mec=INK, mew=0.9, zorder=4)
            ax.plot([nv[ref_d]], [r5(ref_d)], "s", ms=3.2, color=INK, zorder=4)
            ax.set_xscale("log", base=2)
            ax.set_xticks([1, 2, 4, 8])
            ax.set_xticklabels(["1", "2", "4", "8"])
            ax.grid(True, color=GRID, lw=0.5)
            ax.tick_params(length=2)
            if i == 0:
                ax.set_title(c, color=INK)
            if j == 0:
                ax.set_ylabel(f"{NAME[e]}\nrecall@5")
            if i == len(encs) - 1:
                ax.set_xlabel("vectors per folder")
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=INK2, lw=1.4, marker="o", ms=2.6, label="labelled, k = 1 to 5 per label"),
               Line2D([], [], color=INK2, lw=1.0, ls="--", label="blind, K = 2 to 8"),
               Line2D([], [], color=INK2, lw=1.0, ls=":", label="blind at the labelled count"),
               Line2D([], [], color="white", marker="D", mec=INK, ms=3.5, lw=0, label="mean (a)"),
               Line2D([], [], color=INK, marker="s", ms=3.5, lw=0, label="every file (d)")]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(0.5, -0.005))
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(f"{args.out}.{ext}", bbox_inches="tight")
    print(json.dumps({"encoders": encs, "centered": args.centered, "out": args.out}))


if __name__ == "__main__":
    main()
