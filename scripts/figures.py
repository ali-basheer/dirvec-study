#!/usr/bin/env python3
"""Figures of the draft (paper/figures/*.pdf), drawn from the verbatim script outputs in results/.

Every plotted number is read from a verbatim eval.py or descq.py output table (results/session3.md,
session5.md, session11.md, session12.md, session14_outputs.md, session15_outputs.md when present)
and cross-checked against the draft's own tables (Tables 2 to 5 of paper/main.tex): a number that
differs between a figure or a table and its verbatim source stops the script. The numbers each figure uses, with
their source files, are written to paper/figures/figdata.json. The two figures of session 27 (fig_searcher,
fig_budgetsweep) are drawn from the per-query files data/s27_*.npz; the searcher figure recomputes its intervals
with scripts/s27.py and stops if one differs from results/session27_outputs.md.

Usage: python3 scripts/figures.py            (writes the PDFs, figdata.json and PNG previews)
       python3 scripts/figures.py --study    (the study figure alone)
       python3 scripts/figures.py --s27      (the two session-27 figures alone)
       python3 scripts/figures.py --sigir    (the SIGIR version's single-column figures, in paper/sigir)
"""
import json
import math
import os
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper", "figures")
PREVIEW = os.environ.get("FIG_PREVIEW")  # a directory for PNG previews, if set

# ---------------------------------------------------------------- style (dataviz reference palette)
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#ffffff"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
GRAY = "#a9a79f"
ENC = {  # fixed slot order; marker shape carries the family (circle: vision-language, square: dual tower)
    "E1": {"color": BLUE, "marker": "o", "name": "E1 jina-v4", "family": "vision-language"},
    "E2": {"color": ORANGE, "marker": "s", "name": "E2 jina-clip-v2", "family": "dual tower"},
    "E3": {"color": AQUA, "marker": "o", "name": "E3 GME", "family": "vision-language"},
    "E4": {"color": YELLOW, "marker": "s", "name": "E4 Nomic", "family": "dual tower"},
}
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.size": 3, "ytick.major.size": 3, "axes.grid": False, "grid.color": GRID,
    "grid.linewidth": 0.6, "lines.linewidth": 1.6, "lines.solid_capstyle": "round",
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300, "figure.dpi": 150,
    "axes.titleweight": "bold", "axes.titlelocation": "left",
})


# ---------------------------------------------------------------- reading the verbatim outputs

def read(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def section(text, start, stop="\n## "):
    i = text.find(start)
    if i < 0:
        raise KeyError(start)
    j = text.find(stop, i + len(start))
    return text[i: j if j > 0 else len(text)]


def md_table(text, heading):
    """Rows of the first markdown table after a '### <heading>' line, as dicts keyed by the header."""
    i = text.find("### " + heading)
    if i < 0:
        raise KeyError(heading)
    rows = []
    for line in text[i:].splitlines()[1:]:
        if line.startswith("|"):
            if line.startswith("|---"):
                continue
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif rows:
            break
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


def ci(s):
    m = re.match(r"\[([-+]\d\.\d+), ([-+]\d\.\d+)\]", s.strip())
    return float(m.group(1)), float(m.group(2))


def val_ci(s):
    m = re.match(r"([-+]\d\.\d+) (\[.*\])", s.strip())
    return float(m.group(1)), ci(m.group(2))


EVAL_SOURCES = {  # (set, encoder) -> (file, start of its verbatim eval output)
    ("S3", "E1"): ("results/session3.md", "### Session 3 primary cells"),
    ("S5", "E1"): ("results/session5.md", "### Session 3 primary cells"),
    ("S11", "E1"): ("results/session11.md", "## Output, E1"),
    ("S11", "E2"): ("results/session11.md", "## Output, E2"),
    ("S11", "E3"): ("results/session14_outputs.md", "## eval.py"),
    ("S11", "E4"): ("results/session15_outputs.md", "## eval.py"),
}
DESCQ_SOURCES = {
    "E1": ("results/session12.md", "### /workspace/logs/s12/descq_e1.md", "\n### /workspace"),
    "E2": ("results/session12.md", "### /workspace/logs/s12/descq_e2.md", "\n### /workspace"),
    "E3": ("results/session14_outputs.md", "## descq.py", "\n## "),
    "E4": ("results/session15_outputs.md", "## descq.py", "\n## "),
}
GAP_S5 = ("results/session8.md", "Session 8 modality gap, evaluation split")  # Table 4's S5 rows
CELLS = ["all", "P1", "P2", "M1", "M2"]


def load_eval():
    data = {}
    for key, (rel, start) in EVAL_SOURCES.items():
        text = read(rel)
        if text is None:
            continue
        sec = section(text, start, "\n## " if start.startswith("## ") else "\n## ")
        d = {"source": rel}
        prim = md_table(sec, "Session 3 primary cells")
        maj = md_table(sec, "Majority-modality cells")
        for name, row in (("P1", prim[0]), ("P2", prim[1]), ("M1", maj[0]), ("M2", maj[1])):
            d[name] = {"c-a": float(row["c-a"]), "ci": ci(row["c-a 95% CI"]), "queries": int(row["queries"])}
        if key[0] == "S11":
            lv = md_table(sec, "Session 9 (eval queries): recall@5 per cell")
            d["levels"] = {}
            for r in lv:
                vals = [float(r[k]) for k in r if k.startswith("R@5")]
                d["levels"][r["rep"]] = {"vec": float(r["vec/folder"]), **dict(zip(CELLS, vals))}
            gap = md_table(sec, "Session 9 modality gap per space")
            d["gap"] = {r["vectors"]: [float(r[k]) for k in list(r)[1:]] for r in gap}
        data[key] = d
    text = read(GAP_S5[0])
    if text is not None and ("S5", "E1") in data:
        names = {"before centering": "uncentered", "after centering": "centered"}
        data[("S5", "E1")]["gap"] = {names[r["vectors"]]: [float(r[k].split()[0]) for k in list(r)[1:]]
                                     for r in md_table(text, GAP_S5[1])}
    return data


def load_descq():
    out = {}
    for enc, (rel, start, stop) in DESCQ_SOURCES.items():
        text = read(rel)
        if text is None:
            continue
        sec = section(text, start, stop)
        out[enc] = {"source": rel}
        for q, head in (("title", "Session 12 Q_title (record titles): paired differences"),
                        ("desc", "Session 12 Q_desc (title and description): paired differences")):
            rows = {r["cell"]: r for r in md_table(sec, head)}
            out[enc][q] = {b: {"c-a": val_ci(rows[b]["c - a"])[0], "ci": val_ci(rows[b]["c - a"])[1],
                               "queries": int(rows[b]["queries"])}
                           for b in ("[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]")}
    return out


REPS5 = ["a", "ac", "tb2", "tb2c", "c", "cc", "d"]  # the rows of Table 5
NLQ_CELLS = [("title", "all"), ("title", "T"), ("title", "I"), ("desc", "all"), ("desc", "T"), ("desc", "I")]


def load_descq_levels():
    """Recall@5 levels of the title and description queries: {enc: {rep: [six values in NLQ_CELLS order]}}."""
    out = {}
    for enc, (rel, start, stop) in DESCQ_SOURCES.items():
        text = read(rel)
        if text is None:
            continue
        sec = section(text, start, stop)
        tabs = {"title": {r["cell"]: r for r in md_table(sec, "Session 12 Q_title (record titles): 2")},
                "desc": {r["cell"]: r for r in md_table(sec, "Session 12 Q_desc (title and description): 2")}}
        keys = {"all": "all", "T": "text-heavy [0,.2)+[.2,.5)", "I": "image-heavy [.5,.8)+[.8,1]"}
        out[enc] = {rep: [float(tabs[q][keys[c]][f"R@5 {rep}"]) for q, c in NLQ_CELLS] for rep in REPS5}
    return out


# ---------------------------------------------------------------- cross-check against the draft's tables

def tex_tables():
    tex = open(os.path.join(ROOT, "paper", "main.tex"), encoding="utf-8").read()

    def block(label):
        i = tex.index("\\label{%s}" % label)
        return tex[i: tex.index("\\end{tabular}", i)]

    num = r"\$?([-+]?\d\.\d+)\$?"
    loss = {}
    for line in block("tab:loss").splitlines():
        m = re.match(r"(S\d+) \(.*?\) & (E\d)[^&]*& " + num + r" \\ci\{([-+]\d\.\d+)\}\{([-+]\d\.\d+)\} & "
                     + num + r" \\ci\{([-+]\d\.\d+)\}\{([-+]\d\.\d+)\} & " + num + " & " + num, line.strip())
        if m:
            g = m.groups()
            loss[(g[0], g[1])] = {"P1": (float(g[2]), float(g[3]), float(g[4])),
                                  "P2": (float(g[5]), float(g[6]), float(g[7])), "M1": float(g[8]), "M2": float(g[9])}
    cells, order = {}, []
    for line in block("tab:cells").splitlines():
        heads = re.findall(r"\\multicolumn\{5\}\{c\}\{(E\d)", line)
        if heads:
            order = heads
            continue
        m = re.match(r"\\rep\{(\w+)\}[^&]*\(([\d.]+)\) & (.*)\\\\", line.strip())
        if m and order:
            vals = [float(x) for x in m.group(3).split("&")]
            for k, enc in enumerate(order):
                cells[(enc, m.group(1))] = vals[5 * k: 5 * k + 5]
    gap = {}
    for line in block("tab:gap").splitlines():
        m = re.match(r"(S\d+), (E\d) & (uncentered|centered) & (.*)\\\\", line.strip())
        if m:
            gap[(m.group(1), m.group(2), m.group(3))] = [float(x) for x in m.group(4).split("&")]
    nlq, order = {}, []
    for line in block("tab:nlq").splitlines():
        heads = re.findall(r"\\multicolumn\{6\}\{c\}\{(E\d)", line)
        if heads:
            order = heads
            continue
        m = re.match(r"\\rep\{(\w+)\}[^&]*\(([\d.]+)\) & (.*)\\\\", line.strip())
        if m and order:
            vals = [float(x) for x in m.group(3).split("&")]
            for k, enc in enumerate(order):
                nlq[(enc, m.group(1))] = vals[6 * k: 6 * k + 6]
    return loss, cells, gap, nlq


def cross_check(ev, dl=None):
    loss, cells, gap, nlq = tex_tables()
    problems, checked = [], 0
    for key, d in ev.items():
        if key in loss:
            t = loss[key]
            for c in ("P1", "P2"):
                checked += 1
                if (d[c]["c-a"], *d[c]["ci"]) != t[c]:
                    problems.append(f"{key} {c}: results {d[c]['c-a']} {d[c]['ci']}, Table 2 {t[c]}")
            for c in ("M1", "M2"):
                checked += 1
                if d[c]["c-a"] != t[c]:
                    problems.append(f"{key} {c}: results {d[c]['c-a']}, Table 2 {t[c]}")
        if key[0] == "S11":
            for rep, lv in d["levels"].items():
                if (key[1], rep) in cells:
                    checked += 1
                    if [lv[c] for c in CELLS] != cells[(key[1], rep)]:
                        problems.append(f"{key} {rep}: results {[lv[c] for c in CELLS]}, Table 3 {cells[(key[1], rep)]}")
        for kind, vals in d.get("gap", {}).items():
            if (*key, kind) in gap:
                checked += 1
                if vals != gap[(*key, kind)]:
                    problems.append(f"{key} gap {kind}: results {vals}, Table 4 {gap[(*key, kind)]}")
    for enc, reps in (dl or {}).items():
        for rep, vals in reps.items():
            if (enc, rep) in nlq:
                checked += 1
                if vals != nlq[(enc, rep)]:
                    problems.append(f"{enc} {rep} text queries: results {vals}, Table 5 {nlq[(enc, rep)]}")
    # every table entry must have had a source to be compared with
    missing = [f"Table 2 {k}" for k in loss if k not in ev]
    missing += [f"Table 3 {k}" for k in cells if ("S11", k[0]) not in ev or k[1] not in ev[("S11", k[0])]["levels"]]
    missing += [f"Table 4 {k}" for k in gap if k[:2] not in ev or k[2] not in ev[k[:2]].get("gap", {})]
    missing += [f"Table 5 {k}" for k in nlq if k[0] not in (dl or {}) or k[1] not in dl[k[0]]]
    return checked, problems, missing


# ---------------------------------------------------------------- figure helpers

def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    # no creation date in the PDF, so a rerun on the same sources writes the same bytes
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight", pad_inches=0.02,
                metadata={"CreationDate": None})
    if PREVIEW:
        os.makedirs(PREVIEW, exist_ok=True)
        fig.savefig(os.path.join(PREVIEW, name + ".png"), bbox_inches="tight", pad_inches=0.02, dpi=200)
    plt.close(fig)


def clean(ax, grid_axis="x"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid_axis:
        ax.grid(True, axis=grid_axis, color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)


def encs_present(ev):
    return [e for e in ("E1", "E2", "E3", "E4") if ("S11", e) in ev]


# ---------------------------------------------------------------- Figure 1: the setup (schematic)

def doc_icon(ax, x, y, w=0.11, h=0.15, color=ORANGE):
    fold = 0.035
    ax.add_patch(Polygon([[x, y], [x + w, y], [x + w, y + h - fold], [x + w - fold, y + h], [x, y + h]],
                         closed=True, facecolor=SURFACE, edgecolor=color, linewidth=1.0))
    ax.add_patch(Polygon([[x + w - fold, y + h], [x + w - fold, y + h - fold], [x + w, y + h - fold]],
                         closed=True, facecolor=color, edgecolor=color, linewidth=0.8, alpha=0.35))
    for k in range(3):
        yy = y + h * (0.62 - 0.2 * k)
        ax.plot([x + 0.022, x + w - 0.028 - (0.02 if k == 2 else 0)], [yy, yy], color=color, lw=0.9, alpha=0.8)


def img_icon(ax, x, y, w=0.11, h=0.15, color=BLUE):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012",
                                facecolor="#e8f1fb", edgecolor=color, linewidth=1.0))
    ax.add_patch(Polygon([[x + 0.012, y + 0.02], [x + 0.05, y + 0.085], [x + 0.075, y + 0.05],
                          [x + 0.092, y + 0.07], [x + w - 0.01, y + 0.02]], closed=True,
                         facecolor=color, edgecolor="none", alpha=0.75))
    ax.add_patch(matplotlib.patches.Circle((x + 0.078, y + 0.112), 0.013, facecolor=YELLOW, edgecolor="none"))


IMG_PTS = [(0.24, 0.74), (0.31, 0.80), (0.20, 0.64), (0.33, 0.68), (0.27, 0.58), (0.38, 0.76)]
TXT_PTS = [(0.70, 0.40), (0.79, 0.45), (0.66, 0.30)]
QUERY = (0.84, 0.30)
IMG_REPS = [(0.275, 0.77), (0.235, 0.61), (0.355, 0.72)]  # k-means centres of pairs of image vectors


def space_panel(ax, title, faded=False):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.04",
                                facecolor="#fbfbf9", edgecolor=GRID, linewidth=0.8))
    a = 0.28 if faded else 1.0
    for x, y in IMG_PTS:
        ax.plot(x, y, "o", ms=5.5, color=BLUE, alpha=a, mec=SURFACE, mew=1.0)
    for x, y in TXT_PTS:
        ax.plot(x, y, "o", ms=5.5, color=ORANGE, alpha=a, mec=SURFACE, mew=1.0)
    ax.set_title(title, fontsize=8, pad=3)


def fig_setup():
    fig = plt.figure(figsize=(6.6, 1.95))
    w = 0.215
    xs = [0.0, 0.262, 0.524, 0.786]
    axs = [fig.add_axes([x, 0.06, w, 0.80]) for x in xs]
    # 1 the folder
    ax = axs[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Polygon([[0.05, 0.05], [0.95, 0.05], [0.95, 0.80], [0.48, 0.80], [0.42, 0.88], [0.05, 0.88]],
                         closed=True, facecolor="#f6f5f1", edgecolor=AXIS, linewidth=1.0))
    for k, (x, y) in enumerate([(0.11, 0.55), (0.25, 0.55), (0.39, 0.55), (0.11, 0.33), (0.25, 0.33), (0.39, 0.33)]):
        img_icon(ax, x, y)
    for x, y in [(0.58, 0.55), (0.72, 0.55), (0.58, 0.33)]:
        doc_icon(ax, x, y)
    ax.text(0.5, 0.17, "6 images, 3 documents", ha="center", va="center", fontsize=7, color=INK2)
    ax.set_title("1  A folder of mixed files", fontsize=8, pad=3)
    # 2 every file becomes a vector
    space_panel(axs[1], "2  One vector per file")
    ax = axs[1]
    ax.text(0.29, 0.90, "images", ha="center", fontsize=7, color=INK2)
    ax.text(0.72, 0.17, "texts", ha="center", fontsize=7, color=INK2)
    ax.annotate("", xy=(0.70, 0.40), xytext=(0.30, 0.70),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.8, shrinkA=7, shrinkB=7))
    ax.text(0.55, 0.61, "gap", fontsize=7, color=MUTED, rotation=-37, ha="center", va="center")
    # 3 pooled
    space_panel(axs[2], "3  Pooled: one mean vector (a)", faded=True)
    ax = axs[2]
    mx = sum(p[0] for p in IMG_PTS + TXT_PTS) / 9
    my = sum(p[1] for p in IMG_PTS + TXT_PTS) / 9
    ax.plot([QUERY[0], mx], [QUERY[1], my], color=INK2, lw=1.0)
    ax.plot(mx, my, "*", ms=12, color=INK, mec=SURFACE, mew=1.0)
    ax.text(mx - 0.03, my + 0.07, "mean", fontsize=7, color=INK, ha="center")
    ax.plot(*QUERY, "D", ms=5.5, color=SURFACE, mec=ORANGE, mew=1.6)
    ax.text(QUERY[0], QUERY[1] - 0.11, "query", fontsize=7, color=INK2, ha="center")
    ax.text(0.50, 0.07, "the mean is far from the query", fontsize=6.8, color=INK2, ha="center")
    # 4 per-modality representatives
    space_panel(axs[3], "4  Per-modality: a few vectors (c)", faded=True)
    ax = axs[3]
    reps = [(x, y, BLUE) for x, y in IMG_REPS] + [(x, y, ORANGE) for x, y in TXT_PTS]
    near = min(TXT_PTS, key=lambda p: (p[0] - QUERY[0]) ** 2 + (p[1] - QUERY[1]) ** 2)
    ax.plot([QUERY[0], near[0]], [QUERY[1], near[1]], color=INK2, lw=1.0)
    for x, y, c in reps:
        ax.plot(x, y, "o", ms=8.5, color=SURFACE, mec=c, mew=1.7)
        ax.plot(x, y, "o", ms=2.8, color=c)
    ax.plot(*QUERY, "D", ms=5.5, color=SURFACE, mec=ORANGE, mew=1.6)
    ax.text(QUERY[0], QUERY[1] - 0.11, "query", fontsize=7, color=INK2, ha="center")
    ax.text(0.50, 0.07, "a text vector is next to the query", fontsize=6.8, color=INK2, ha="center")
    for x0 in xs[:3]:
        fig.patches.append(FancyArrowPatch((x0 + w + 0.006, 0.46), (x0 + 0.262 - 0.006, 0.46),
                                           transform=fig.transFigure, arrowstyle="-|>", mutation_scale=8,
                                           color=MUTED, lw=1.0))
    save(fig, "fig_setup")


# ---------------------------------------------------------------- Figure 2: the loss across draws and encoders

def fig_loss(ev):
    rows = [("S3", "E1"), ("S5", "E1"), ("S11", "E1"), ("S11", "E3"), ("S11", "E2"), ("S11", "E4")]
    rows = [r for r in rows if r in ev]
    labels = {("S3", "E1"): "S3 retest, E1", ("S5", "E1"): "S5 main set, E1", ("S11", "E1"): "S11, E1 jina-v4",
              ("S11", "E3"): "S11, E3 GME", ("S11", "E2"): "S11, E2 jina-clip-v2", ("S11", "E4"): "S11, E4 Nomic"}
    fig, ax = plt.subplots(figsize=(6.6, 0.42 * len(rows) + 0.9))
    y0 = list(range(len(rows)))[::-1]
    for y, key in zip(y0, rows):
        d = ev[key]
        for c, dy, col, mk in (("P1", 0.13, BLUE, "o"), ("P2", -0.13, ORANGE, "s")):
            v, (lo, hi) = d[c]["c-a"], d[c]["ci"]
            ax.plot([lo, hi], [y + dy, y + dy], color=col, lw=1.4, solid_capstyle="butt")
            ax.plot(v, y + dy, mk, ms=5.5, color=col, mec=SURFACE, mew=1.0, zorder=3)
        for c in ("M1", "M2"):
            ax.plot(d[c]["c-a"], y, "o", ms=3.6, color=GRAY, mec=SURFACE, mew=0.6, zorder=2)
    ax.axvline(0, color=AXIS, lw=0.8)
    ax.set_yticks(y0)
    ax.set_yticklabels([labels[r] for r in rows])
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlim(-0.02, 0.6)
    ax.set_xlabel("recall@5 lost by the pooled vector (c minus a), with 95 percent intervals")
    clean(ax, "x")
    ax.tick_params(axis="y", length=0)
    n_vlm = sum(1 for r in rows if ENC[r[1]]["family"] == "vision-language")
    if 0 < n_vlm < len(rows):
        ysep = y0[n_vlm - 1] - 0.5
        ax.axhline(ysep, color=GRID, lw=0.8)
        ax.text(0.598, y0[0] + 0.33, "vision-language embedders", ha="right", va="center", fontsize=7, color=MUTED)
        ax.text(0.598, ysep - 0.17, "dual towers (CLIP family)", ha="right", va="center", fontsize=7, color=MUTED)
    handles = [Line2D([], [], color=BLUE, marker="o", ms=5, lw=1.4, label="P1: image queries, text-heavy folders"),
               Line2D([], [], color=ORANGE, marker="s", ms=5, lw=1.4, label="P2: text queries, image-heavy folders"),
               Line2D([], [], color=GRAY, marker="o", ms=3.6, lw=0, label="M1, M2: majority cells")]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False,
              handlelength=1.8, columnspacing=1.4)
    save(fig, "fig_loss")
    return {f"{k[0]} {k[1]}": {c: ev[k][c] for c in ("P1", "P2", "M1", "M2")} | {"source": ev[k]["source"]} for k in rows}


# ---------------------------------------------------------------- Figure 3: a folder is two clusters (cosines)

def fig_cosines(ev):
    encs = [e for e in ("E1", "E3", "E2", "E4") if ("S11", e) in ev]
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 0.38 * len(encs) + 1.05), sharey=True)
    used = {}
    for ax, kind, title in ((axs[0], "uncentered", "Before centering"),
                            (axs[1], "centered", "After per-modality centering")):
        for k, e in enumerate(encs):
            y = len(encs) - 1 - k
            gap, ii, tt, it = ev[("S11", e)]["gap"][kind]
            used.setdefault(e, {})[kind] = {"gap": gap, "img-img": ii, "txt-txt": tt, "img-txt": it}
            ax.plot([it, max(ii, tt)], [y, y], color=GRID, lw=3.2, solid_capstyle="round", zorder=1)
            ax.plot(ii, y, "o", ms=5.2, color=GRAY, mec=SURFACE, mew=0.8, zorder=2)
            ax.plot(tt, y, "^", ms=5.4, color=GRAY, mec=SURFACE, mew=0.8, zorder=2)
            ax.plot(it, y, "D", ms=5.4, color=BLUE, mec=SURFACE, mew=0.8, zorder=3)
            ax.text(1.03, y, f"gap {gap:.3f}", ha="left", va="center", fontsize=7, color=MUTED, clip_on=False)
        ax.set_xlim(0, 1.0)
        ax.set_title(title)
        clean(ax, "x")
        ax.tick_params(axis="y", length=0)
        ax.set_xlabel("mean cosine of two files in the same folder")
    axs[0].set_yticks(range(len(encs))[::-1])
    axs[0].set_yticklabels([ENC[e]["name"] + ("  (VLM)" if ENC[e]["family"] == "vision-language" else "  (dual)")
                            for e in encs])
    axs[0].set_ylim(-0.6, len(encs) - 0.4)
    handles = [Line2D([], [], color=GRAY, marker="o", ms=5, lw=0, label="image with image"),
               Line2D([], [], color=GRAY, marker="^", ms=5, lw=0, label="text with text"),
               Line2D([], [], color=BLUE, marker="D", ms=5, lw=0, label="image with text")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.55, 0.97), ncol=3, frameon=False)
    fig.tight_layout(w_pad=1.5)
    save(fig, "fig_cosines")
    return used


# ---------------------------------------------------------------- Figure 4: what each budget keeps

def fig_budget(ev):
    encs = encs_present(ev)
    reps = [("a", "1\na"), ("tb2c", "2\ntb2c"), ("c", "5.2\nc"), ("d", "9.9\nd")]
    panels = [("P1", "P1: image query,\ntext-heavy folder"), ("P2", "P2: text query,\nimage-heavy folder"),
              ("M1", "M1: image query,\nimage-heavy folder"), ("M2", "M2: text query,\ntext-heavy folder")]
    fig, axs = plt.subplots(1, 4, figsize=(6.6, 2.35), sharey=True)
    used = {}
    for ax, (cell, title) in zip(axs, panels):
        xs = [math.log2(ev[("S11", encs[0])]["levels"][r]["vec"]) for r, _ in reps]
        for e in encs:
            lv = ev[("S11", e)]["levels"]
            ys = [lv[r][cell] for r, _ in reps]
            used.setdefault(e, {})[cell] = dict(zip([r for r, _ in reps], ys))
            ax.plot(xs, ys, color=ENC[e]["color"], lw=1.5, zorder=2)
            ax.plot(xs, ys, ENC[e]["marker"], ms=4.6, color=ENC[e]["color"], mec=SURFACE, mew=0.8, zorder=3)
        ax.set_xticks(xs)
        ax.set_xticklabels([lab for _, lab in reps], fontsize=6.8)
        ax.set_xlim(xs[0] - 0.35, xs[-1] + 0.35)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=7.6, linespacing=1.15)
        clean(ax, "y")
    axs[0].set_ylabel("recall@5")
    fig.text(0.5, -0.05, "vectors per folder (log scale) and the representation that uses them", ha="center",
             fontsize=8, color=INK2)
    handles = [Line2D([], [], color=ENC[e]["color"], marker=ENC[e]["marker"], ms=4.6, lw=1.5, label=ENC[e]["name"])
               for e in encs]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.98), ncol=len(encs), frameon=False)
    fig.tight_layout(w_pad=0.8)
    save(fig, "fig_budget")
    return used


# ---------------------------------------------------------------- Figure 5: text queries by image fraction

def fig_textq(dq):
    encs = [e for e in ("E1", "E2", "E3", "E4") if e in dq]
    buckets = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.3), sharey=True)
    offs = {e: (k - (len(encs) - 1) / 2) * 0.07 for k, e in enumerate(encs)}
    for ax, (q, title) in zip(axs, (("title", "Query: the record's title"),
                                    ("desc", "Query: title and description"))):
        for e in encs:
            vals = [dq[e][q][b]["c-a"] for b in buckets]
            xs = [k + offs[e] for k in range(4)]
            for x, b in zip(xs, buckets):
                lo, hi = dq[e][q][b]["ci"]
                ax.plot([x, x], [lo, hi], color=ENC[e]["color"], lw=0.9, alpha=0.55, solid_capstyle="butt")
            ax.plot(xs, vals, color=ENC[e]["color"], lw=1.5, zorder=2)
            ax.plot(xs, vals, ENC[e]["marker"], ms=4.6, color=ENC[e]["color"], mec=SURFACE, mew=0.8, zorder=3)
        ax.axhline(0, color=AXIS, lw=0.8)
        ax.set_xticks(range(4))
        ax.set_xticklabels(buckets)
        ax.set_title(title)
        clean(ax, "y")
        ax.set_xlabel("share of images in the folder")
    axs[0].set_ylabel("recall@5 lost by the pooled vector")
    handles = [Line2D([], [], color=ENC[e]["color"], marker=ENC[e]["marker"], ms=4.6, lw=1.5, label=ENC[e]["name"])
               for e in encs]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.98), ncol=len(encs), frameon=False)
    fig.tight_layout(w_pad=1.2)
    save(fig, "fig_textq")
    return {e: {q: dq[e][q] for q in ("title", "desc")} | {"source": dq[e]["source"]} for e in encs}


# ---------------------------------------------------------------- Figure 0: the study at a glance

GOOD, BAD, MIXED = "#0ca30c", "#d03b3b", "#fab219"  # status palette: survived, died, partly or split
STUDY = [  # (session, set, label, verdict, note); verdicts as in the appendix of the draft. On S11 the note
    # names the encoders a hypothesis was read under, and no note means all four (the caption says so).
    (1, "S1", "corpus", None, ""), (2, "S1", "Claim", "dead", ""),
    (3, "S3", "H", "survived", ""), (4, "S3", "cost", None, ""),
    (5, "S5", "H5", "partly", ""), (6, "S5", "H6", "dead", ""), (7, "S5", "H7", "dead", ""),
    (8, "S5", "H8", "dead", ""), (9, "S5", "H9a", "survived", ""), (9, "S5", "H9b", "partly", ""),
    (9, "S5", "H9c", "dead", ""), (10, "S5", "H10", "survived", "synthetic"),
    (11, "S11", "H11a", "survived", "E1"), (11, "S11", "H11b", "dead", "E2"),
    (12, "S11", "H12a", "survived", "E1"), (12, "S11", "H12b", "survived", "E1, E2"),
    (13, "S5", "H9a", "survived", "re-run"),
    (14, "S11", "H14a", "survived", "E3"), (14, "S11", "H14b", "survived", "E3"),
    (15, "S11", "H15a", "survived", "E4"), (15, "S11", "H15b", "survived", "E4"),
    (15, "S11", "H15c", "survived", "E4 vs E1"),
    (16, "S11", "H16a", "survived", ""), (16, "S11", "H16b", "dead", ""), (16, "S11", "H16c", "dead", ""),
    (17, "S11", "H17a", "survived", ""), (17, "S11", "H17b", "survived", "E1, E3"),
    (17, "S11", "H17c", "survived", "E1"),
    (18, "S11", "H18a", "split", "E1, E3"), (18, "S11", "H18b", "survived", "E1, E3"),
    (20, "S11", "H20a", "survived", ""), (20, "S11", "H20b", "split", ""), (20, "S11", "H20c", "survived", ""),
    # GitHub directories (S19, S24) and repository trees (S23): E1 decides; E4 and E2 have no verdict of their own
    (19, "S19", "H19a", "inconclusive", ""), (19, "S19", "H19b", "inconclusive", ""),
    (19, "S19", "H19c", "survived", ""), (19, "S19", "H19d", "inconclusive", ""),
    (21, "S19", "H21a", "survived", "pooled"), (21, "S19", "H21b", "dead", ""),
    (21, "S19", "H21c", "survived", "pooled"),
    (22, "S19", "store", None, ""),
    (23, "S23", "H23a", "inconclusive", ""), (23, "S23", "H23b", "survived", ""), (23, "S23", "H23c", "dead", ""),
    (24, "S24", "H24a", "survived", ""), (24, "S24", "H24b", "survived", ""), (24, "S24", "H24c", "survived", ""),
    (24, "S24", "H24d", "survived", ""), (24, "S24", "H24e", "survived", ""), (24, "S24", "H24f", "dead", ""),
    (24, "S24", "H24g", "survived", ""),
    (25, "S11", "estimates", None, "S19, S24"),   # post hoc estimates from per-query files, no hypothesis
    # session 26, registered after a blind review on draws already read (post hoc in the paper)
    (26, "S19", "H26a", "survived", "pooled"), (26, "S19", "H26b", "survived", "pooled"),
    (26, "S19", "H26c", "dead", "pooled"), (26, "S11", "H26d", "survived", "E1, E3"),
    # session 27: queries a model wrote as a simulated searcher (H27a to H27c, E1), and two registered readings
    # without a kill criterion, the budget from one to eight vectors and the k-means seed (all four encoders)
    (27, "S11", "H27a", "survived", "E1"), (27, "S11", "H27b", "survived", "E1"), (27, "S11", "H27c", "survived", "E1"),
    (27, "S11", "budget", None, ""), (27, "S11", "seed", None, ""),
]


def study_check():
    """The list above against the appendix of the draft: the same hypotheses, sessions and sets."""
    app = read("paper/main.tex")
    app = app[app.index("\\label{app:hyp}"):]
    listed = set()
    for label, where in re.findall(r"\\item\[(Claim|H\w*) \(([^)]*)\)", app):
        sset = re.search(r"\bS\d+\b", where).group(0)
        for sess in re.findall(r"session (\d+)", where):
            listed.add((int(sess), sset, label))
    drawn = {it[:3] for it in STUDY if it[3]}
    return sorted(listed - drawn), sorted(drawn - listed)


def fig_study(upto=None, name="fig_study"):
    """The long version's study figure: the list of sessions at text width (6.5 in), type at 7.4 pt."""
    return fig_study_list(6.5, name, 7.4)


# ---------------------------------------------------------------- the SIGIR version's single-column figures
# acmart sigconf sets a column 241 pt (3.34 in) wide. These four are drawn at that width, so their type is
# printed at the size given here (6.5 to 7.2 pt), and the small labels use the darker of the two greys. The long
# version's figures, scaled to a column, would print at about half their size.

COLW = 3.34


def fig_study_list(W, name, fs):
    """The study as a list: one row per session with its draw, the hypotheses and their verdicts in a line.
    W is the printed width in inches and fs the type size in points (the figure is saved at its own size)."""
    sessions = sorted({it[0] for it in STUDY})
    row_h, top, legend_h = 0.03 * fs / 1.7, 0.18 * fs / 6.5, 0.31 * fs / 6.5
    H = top + row_h * len(sessions) + legend_h
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    rend = fig.canvas.get_renderer()

    def width(t):  # inches
        return t.get_window_extent(rend).width / fig.dpi

    k_ = fs / 6.5
    x_sess, x_draw, x_items = 0.44 * k_, 0.56 * k_, 0.93 * k_
    ax.text(x_sess, H - 0.09 * k_, "session", ha="right", va="center", fontsize=fs, color=INK2)
    ax.text(x_draw, H - 0.09 * k_, "draw", ha="left", va="center", fontsize=fs, color=INK2)
    ax.text(x_items, H - 0.09 * k_, "hypotheses and verdicts", ha="left", va="center", fontsize=fs, color=INK2)
    ax.plot([0.08, W - 0.04], [H - top + 0.02] * 2, color=GRID, lw=0.8)

    def marker(x, y, verdict, ms=1.0):
        ms *= k_
        if verdict is None:
            ax.plot(x, y, "s", ms=4.2 * ms, color=GRAY, mec=SURFACE, mew=0.5, zorder=3)
        elif verdict == "survived":
            ax.plot(x, y, "o", ms=5.4 * ms, color=GOOD, mec=SURFACE, mew=0.5, zorder=3)
        elif verdict == "dead":
            ax.plot(x, y, "X", ms=5.8 * ms, color=BAD, mec=SURFACE, mew=0.4, zorder=3)
        elif verdict == "split":
            ax.plot(x, y, "D", ms=4.6 * ms, color=MIXED, mec=SURFACE, mew=0.5, zorder=3)
        elif verdict == "inconclusive":
            ax.plot(x, y, "o", ms=5.0 * ms, color=SURFACE, mec=INK2, mew=0.9, zorder=3)
        else:
            ax.plot(x, y, "o", ms=5.4 * ms, color=MIXED, mec=MIXED, mew=0.9, zorder=3, fillstyle="left",
                    markerfacecoloralt=SURFACE)

    right = 0.0
    for k, sess in enumerate(sessions):
        y = H - top - row_h * (k + 0.5)
        its = [it for it in STUDY if it[0] == sess]
        # a session on two draws (session 26) shows its first draw in the column and the other in the note
        its = [it if it[1] == its[0][1] else (it[0], its[0][1], it[2], it[3], ", ".join(x for x in (it[1], it[4]) if x))
               for it in its]
        if k % 2 == 0:
            ax.add_patch(Rectangle((0.08, y - row_h / 2), W - 0.12, row_h, facecolor="#f6f5f1", edgecolor="none",
                                   zorder=0))
        ax.text(x_sess, y, str(sess), ha="right", va="center", fontsize=fs, color=INK2)
        ax.text(x_draw, y, its[0][1], ha="left", va="center", fontsize=fs, color=INK2)
        x = x_items + 0.04 * k_
        for _, _, label, verdict, note in its:
            marker(x, y, verdict)
            t = ax.text(x + 0.075 * k_, y, label + (f" ({note})" if note else ""), ha="left", va="center", fontsize=fs,
                        color=INK if verdict else INK2, zorder=4)
            x += 0.075 * k_ + width(t) + 0.15 * k_
        right = max(right, x - 0.15 * k_)
    assert right < W - 0.02, f"a row of the study figure is {right:.2f} in wide, the figure {W} in"
    leg = [("survived", "survived"), ("dead", "died"), ("partly", "partly (one clause, or one of two readings)"),
           ("split", "split by encoder"), ("inconclusive", "inconclusive"), (None, "no hypothesis")]
    used = {it[3] for it in STUDY} | {"survived", "dead"}
    leg = [e for e in leg if e[0] in used or e[0] is None]
    y, x = legend_h - 0.13 * k_, 0.16
    for verdict, text in leg:
        t = ax.text(x + 0.075 * k_, y, text, ha="left", va="center", fontsize=fs, color=INK2)
        if x + 0.075 * k_ + width(t) > W - 0.05:     # wrap to a second legend line
            t.remove()
            y, x = y - 0.13 * k_, 0.16
            t = ax.text(x + 0.075 * k_, y, text, ha="left", va="center", fontsize=fs, color=INK2)
        marker(x, y, verdict, ms=0.95)
        x += 0.075 * k_ + width(t) + 0.17 * k_
    save_col(fig, name)
    return [list(it) for it in STUDY]


def fig_study_col():
    return fig_study_list(COLW, "fig_study_col", 6.5)


def fig_loss_col(ev):
    rows = [("S3", "E1"), ("S5", "E1"), ("S11", "E1"), ("S11", "E3"), ("S11", "E2"), ("S11", "E4")]
    labels = {("S3", "E1"): "Retest, E1", ("S5", "E1"): "Main, E1", ("S11", "E1"): "Confirm., E1",
              ("S11", "E3"): "Confirm., E3", ("S11", "E2"): "Confirm., E2", ("S11", "E4"): "Confirm., E4"}
    fig, ax = plt.subplots(figsize=(COLW, 1.95))
    y0 = list(range(len(rows)))[::-1]
    for y, key in zip(y0, rows):
        d = ev[key]
        for c, dy, col, mk in (("P1", 0.14, BLUE, "o"), ("P2", -0.14, ORANGE, "s")):
            v, (lo, hi) = d[c]["c-a"], d[c]["ci"]
            ax.plot([lo, hi], [y + dy, y + dy], color=col, lw=1.3, solid_capstyle="butt")
            ax.plot(v, y + dy, mk, ms=4.6, color=col, mec=SURFACE, mew=0.8, zorder=3)
        for c in ("M1", "M2"):
            ax.plot(d[c]["c-a"], y, "o", ms=3.2, color=GRAY, mec=SURFACE, mew=0.5, zorder=2)
    ax.axvline(0, color=AXIS, lw=0.8)
    ax.set_yticks(y0)
    ax.set_yticklabels([labels[r] for r in rows], fontsize=7)
    ax.set_ylim(-1.0, len(rows) - 0.25)
    ax.set_xlim(-0.02, 0.6)
    ax.tick_params(axis="x", labelsize=6.8)
    ax.set_xlabel("recall@5 lost by the pooled vector (c minus a)", fontsize=7.2)
    clean(ax, "x")
    ax.tick_params(axis="y", length=0)
    n_vlm = sum(1 for r in rows if ENC[r[1]]["family"] == "vision-language")
    ax.axhline(y0[n_vlm - 1] - 0.5, color=GRID, lw=0.8)
    ax.text(0.598, y0[0] + 0.5, "vision-language embedders", ha="right", va="center", fontsize=6.5, color=INK2)
    ax.text(0.598, y0[-1] - 0.72, "CLIP-family dual towers", ha="right", va="center", fontsize=6.5, color=INK2)
    handles = [Line2D([], [], color=BLUE, marker="o", ms=4.4, lw=1.3, label="P1: image queries, text-heavy folders"),
               Line2D([], [], color=ORANGE, marker="s", ms=4.4, lw=1.3, label="P2: text queries, image-heavy folders"),
               Line2D([], [], color=GRAY, marker="o", ms=3.2, lw=0, label="M1, M2: majority cells")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.0), ncol=1, frameon=False, fontsize=6.8,
               handlelength=1.6, labelspacing=0.25, borderaxespad=0.1)
    fig.subplots_adjust(left=0.215, right=0.965, top=0.775, bottom=0.185)
    save_col(fig, "fig_loss_col")


def fig_cosines_col(ev):
    encs = ["E1", "E3", "E2", "E4"]
    fig, axs = plt.subplots(2, 1, figsize=(COLW, 2.12), sharex=True)
    for ax, kind, title in ((axs[0], "uncentered", "Before centering"),
                            (axs[1], "centered", "After per-modality centering")):
        for k, e in enumerate(encs):
            y = len(encs) - 1 - k
            gap, ii, tt, it = ev[("S11", e)]["gap"][kind]
            ax.plot([it, max(ii, tt)], [y, y], color=GRID, lw=2.8, solid_capstyle="round", zorder=1)
            ax.plot(ii, y, "o", ms=4.6, color=GRAY, mec=SURFACE, mew=0.7, zorder=2)
            ax.plot(tt, y, "^", ms=4.8, color=GRAY, mec=SURFACE, mew=0.7, zorder=2)
            ax.plot(it, y, "D", ms=4.6, color=BLUE, mec=SURFACE, mew=0.7, zorder=3)
            ax.text(1.03, y, f"gap {gap:.3f}", ha="left", va="center", fontsize=6.5, color=INK2, clip_on=False)
        ax.set_xlim(0, 1.0)
        ax.set_title(title, fontsize=7.2, pad=2.5)
        clean(ax, "x")
        ax.tick_params(axis="y", length=0)
        ax.tick_params(axis="x", labelsize=6.8)
        ax.set_yticks(range(len(encs))[::-1])
        ax.set_yticklabels([ENC[e]["name"] + (" (VLM)" if ENC[e]["family"] == "vision-language" else " (dual)")
                            for e in encs], fontsize=6.8)
        ax.set_ylim(-0.6, len(encs) - 0.4)
    axs[1].set_xlabel("mean cosine of two files in the same folder", fontsize=7.2)
    handles = [Line2D([], [], color=GRAY, marker="o", ms=4.4, lw=0, label="image with image"),
               Line2D([], [], color=GRAY, marker="^", ms=4.4, lw=0, label="text with text"),
               Line2D([], [], color=BLUE, marker="D", ms=4.4, lw=0, label="image with text")]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False, fontsize=6.8,
               handletextpad=0.2, columnspacing=1.2, borderaxespad=0.1)
    fig.subplots_adjust(left=0.30, right=0.845, top=0.845, bottom=0.165, hspace=0.42)
    save_col(fig, "fig_cosines_col")


def fig_textq_col(dq):
    encs = ["E1", "E2", "E3", "E4"]
    buckets = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]
    fig, axs = plt.subplots(1, 2, figsize=(COLW, 1.72), sharey=True)
    offs = {e: (k - (len(encs) - 1) / 2) * 0.08 for k, e in enumerate(encs)}
    for ax, (q, title) in zip(axs, (("title", "Query: the record's title"), ("desc", "Query: title and description"))):
        for e in encs:
            vals = [dq[e][q][b]["c-a"] for b in buckets]
            xs = [k + offs[e] for k in range(4)]
            for x, b in zip(xs, buckets):
                lo, hi = dq[e][q][b]["ci"]
                ax.plot([x, x], [lo, hi], color=ENC[e]["color"], lw=0.8, alpha=0.55, solid_capstyle="butt")
            ax.plot(xs, vals, color=ENC[e]["color"], lw=1.2, zorder=2)
            ax.plot(xs, vals, ENC[e]["marker"], ms=3.6, color=ENC[e]["color"], mec=SURFACE, mew=0.6, zorder=3)
        ax.axhline(0, color=AXIS, lw=0.8)
        ax.set_xticks(range(4))
        ax.set_xticklabels(buckets, fontsize=6.5)
        ax.set_xlim(-0.4, 3.4)
        ax.tick_params(axis="y", labelsize=6.8)
        ax.set_title(title, fontsize=7, pad=2.5)
        clean(ax, "y")
    axs[0].set_ylabel("recall@5 lost (c minus a)", fontsize=7.2)
    fig.text(0.55, 0.012, "share of images in the folder", ha="center", va="bottom", fontsize=7.2, color=INK2)
    handles = [Line2D([], [], color=ENC[e]["color"], marker=ENC[e]["marker"], ms=3.6, lw=1.2, label=ENC[e]["name"])
               for e in encs]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.54, 1.0), ncol=4, frameon=False, fontsize=6.8,
               handlelength=1.3, handletextpad=0.3, columnspacing=0.9, borderaxespad=0.1)
    fig.subplots_adjust(left=0.125, right=0.99, top=0.81, bottom=0.21, wspace=0.07)
    save_col(fig, "fig_textq_col")


# ---------------------------------------------------------------- session 27: searcher queries and the budget sweep
# Both figures are drawn from the per-query files of scripts/s27.py (data/s27_*.npz). The searcher figure recomputes
# every interval with s27.py's estimator and seeds and stops if one differs from results/session27_outputs.md; the
# budget figure plots recall@5 levels, which results/session27_budget_outputs.md prints for every row and cell.

S27_HUMAN = {e: f"data/s27_human_{e.lower()}.npz" for e in ("E1", "E2", "E3", "E4")}
S27_BUDGET = {e: f"data/s27_s11_{e.lower()}.npz" for e in ("E1", "E2", "E3", "E4")}
SEARCH_CELLS = ("QI-T", "QT-I", "QI-I", "QT-T")


def _s27():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import s27  # noqa: E402
    return s27


def load_s27_searcher():
    """c minus a by encoder and cell on the 27A queries, with creator-clustered 95 percent intervals."""
    s27 = _s27()
    text = read("results/session27_outputs.md")
    out = {}
    for e, rel in S27_HUMAN.items():
        d = s27.load_npz(os.path.join(ROOT, rel))
        cs = s27.human_cells(d["kind"], d["bucket"])
        row = [r for r in md_table(section(text, f"## {e}\n"), "Differences in recall@5") if r["difference"] == "c-a"][0]
        out[e] = {"source": rel}
        for c in ("all",) + SEARCH_CELLS:
            z = ((d["rank_c"] <= 5).astype(float) - (d["rank_a"] <= 5).astype(float))[cs[c]]
            v, (lo, hi), _, nfam = s27.boot_ci(z, d["family"][cs[c]], s27.HSEEDS[c])
            pv, (plo, phi) = val_ci(row[c])
            if max(abs(pv - v), abs(plo - lo), abs(phi - hi)) > 5e-4:
                sys.exit(f"fig_searcher: {e} {c}: recomputed {v:+.3f} [{lo:+.3f}, {hi:+.3f}], printed {row[c]}")
            out[e][c] = {"c-a": pv, "ci": [plo, phi], "families": nfam, "queries": int(cs[c].sum())}
    return out


def _searcher_axes(ax, sq, rows, y0, dy, ms, lw, ms_maj):
    for y, e in zip(y0, rows):
        for c, off, col, mk in (("QI-T", dy, BLUE, "o"), ("QT-I", -dy, ORANGE, "s")):
            v, (lo, hi) = sq[e][c]["c-a"], sq[e][c]["ci"]
            ax.plot([lo, hi], [y + off, y + off], color=col, lw=lw, solid_capstyle="butt")
            ax.plot(v, y + off, mk, ms=ms, color=col, mec=SURFACE, mew=0.9, zorder=3)
        for c in ("QI-I", "QT-T"):
            ax.plot(sq[e][c]["c-a"], y, "o", ms=ms_maj, color=GRAY, mec=SURFACE, mew=0.6, zorder=2)
    ax.axvline(0, color=AXIS, lw=0.8)
    ax.set_xlim(-0.2, 1.0)
    clean(ax, "x")
    ax.tick_params(axis="y", length=0)


def fig_searcher(sq):
    rows = ["E1", "E3", "E2", "E4"]
    fig, ax = plt.subplots(figsize=(6.6, 0.42 * len(rows) + 0.9))
    y0 = list(range(len(rows)))[::-1]
    _searcher_axes(ax, sq, rows, y0, 0.13, 5.5, 1.4, 3.6)
    ax.set_yticks(y0)
    ax.set_yticklabels([ENC[e]["name"] for e in rows])
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlabel("recall@5 lost by the pooled vector (c minus a), with 95 percent intervals")
    ysep = y0[1] - 0.5
    ax.axhline(ysep, color=GRID, lw=0.8)
    ax.text(0.998, y0[0] + 0.33, "vision-language embedders", ha="right", va="center", fontsize=7, color=MUTED)
    ax.text(0.998, ysep - 0.17, "dual towers (CLIP family)", ha="right", va="center", fontsize=7, color=MUTED)
    handles = [Line2D([], [], color=BLUE, marker="o", ms=5, lw=1.4, label="QI-T: picture queries, text-heavy folders"),
               Line2D([], [], color=ORANGE, marker="s", ms=5, lw=1.4, label="QT-I: document queries, image-heavy folders"),
               Line2D([], [], color=GRAY, marker="o", ms=3.6, lw=0, label="QI-I, QT-T: majority cells")]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False,
              handlelength=1.8, columnspacing=1.2, fontsize=7.2)
    save(fig, "fig_searcher")
    return sq


def fig_searcher_col(sq):
    rows = ["E1", "E3", "E2", "E4"]
    fig, ax = plt.subplots(figsize=(COLW, 1.42))
    y0 = list(range(len(rows)))[::-1]
    _searcher_axes(ax, sq, rows, y0, 0.15, 4.4, 1.3, 3.2)
    ax.set_yticks(y0)
    ax.set_yticklabels([ENC[e]["name"] for e in rows], fontsize=7)
    ax.set_ylim(-0.6, len(rows) - 0.3)
    ax.tick_params(axis="x", labelsize=6.8)
    ax.set_xlabel("recall@5 lost by the pooled vector (c minus a)", fontsize=7.2)
    ax.axhline(y0[1] - 0.5, color=GRID, lw=0.8)
    handles = [Line2D([], [], color=BLUE, marker="o", ms=4.4, lw=1.3, label="QI-T: pictures, text-heavy"),
               Line2D([], [], color=ORANGE, marker="s", ms=4.4, lw=1.3, label="QT-I: documents, image-heavy"),
               Line2D([], [], color=GRAY, marker="o", ms=3.2, lw=0, label="majority cells")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.0), ncol=2, frameon=False, fontsize=6.6,
               handlelength=1.5, handletextpad=0.4, columnspacing=0.9, labelspacing=0.2, borderaxespad=0.1)
    fig.subplots_adjust(left=0.25, right=0.97, top=0.79, bottom=0.235)
    save_col(fig, "fig_searcher_col")


def fig_budgetsweep():
    """Recall@5 against vectors per folder on S11 (session 27B), uncentered rows, one row of panels per encoder."""
    s27 = _s27()
    encs = ["E1", "E3", "E2", "E4"]
    cells = ("all", "P1", "P2", "M1", "M2")
    fig, axes = plt.subplots(len(encs), len(cells), figsize=(6.6, 1.12 * len(encs) + 0.55), sharex=True,
                             squeeze=False)
    used = {}
    for i, e in enumerate(encs):
        d = s27.load_npz(os.path.join(ROOT, S27_BUDGET[e]))
        assert d["meta"]["gate"]["pass"], e
        cs = s27.s11_cells(d["modality"], d["bucket"])
        nv = d["meta"]["nvec"]
        used[e] = {"source": S27_BUDGET[e]}
        for j, c in enumerate(cells):
            ax = axes[i][j]

            def r5(r):
                return float((d[f"rank_{r}"][cs[c]] <= 5).mean())
            ax.axhline(r5("d"), color=MUTED, lw=0.6, ls=(0, (1, 2)), zorder=1)
            for fam, ks, ls in (("L", s27.LK, "-"), ("B", s27.BK, "--"), ("M", s27.LK, ":")):
                rows = [f"{fam}{k}" for k in ks]
                xs, ys = [nv[r] for r in rows], [r5(r) for r in rows]
                used[e].setdefault(c, {}).update(dict(zip(rows, [round(y, 3) for y in ys])))
                ax.plot(xs, ys, ls=ls, color=ENC[e]["color"] if fam == "L" else INK2, lw=1.4 if fam == "L" else 0.9,
                        marker="o" if fam == "L" else None, ms=2.6, zorder=3 if fam == "L" else 2)
            ax.plot([nv["a"]], [r5("a")], "D", ms=3.4, color=SURFACE, mec=INK, mew=0.9, zorder=4)
            ax.plot([nv["d"]], [r5("d")], "s", ms=3.4, color=INK, zorder=4)
            used[e][c].update({"a": round(r5("a"), 3), "d": round(r5("d"), 3)})
            ax.set_xscale("log", base=2)
            ax.set_xticks([1, 2, 4, 8])
            ax.set_xticklabels(["1", "2", "4", "8"])
            ax.minorticks_off()
            clean(ax, "y")
            ax.tick_params(labelsize=6.8, length=2)
            if i == 0:
                ax.set_title({"all": "all queries"}.get(c, c), fontsize=7.8)
            if j == 0:
                ax.set_ylabel(ENC[e]["name"] + "\nrecall@5", fontsize=7.2)
            if i == len(encs) - 1:
                ax.set_xlabel("vectors per folder", fontsize=7.2)
    handles = [Line2D([], [], color=INK2, lw=1.4, marker="o", ms=2.6, label="k per label, k = 1 to 5 (colour)"),
               Line2D([], [], color=INK2, lw=0.9, ls="--", label="blind, K = 2 to 8"),
               Line2D([], [], color=INK2, lw=0.9, ls=":", label="blind, as many as per label"),
               Line2D([], [], color=SURFACE, marker="D", mec=INK, ms=3.6, lw=0, label="mean (a)"),
               Line2D([], [], color=INK, marker="s", ms=3.6, lw=0, label="every file (d)")]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(0.5, -0.01), fontsize=7,
               handlelength=1.8, columnspacing=1.0)
    fig.tight_layout(rect=(0, 0.04, 1, 1), h_pad=0.6, w_pad=0.4)
    save(fig, "fig_budgetsweep")
    return used


def save_col(fig, name):
    """Save at the figure's own size (no tight bounding box), so the printed type size is the one set here."""
    fig.savefig(os.path.join(OUT, name + ".pdf"), metadata={"CreationDate": None})
    if PREVIEW:
        os.makedirs(PREVIEW, exist_ok=True)
        fig.savefig(os.path.join(PREVIEW, name + ".png"), dpi=200)
    plt.close(fig)


def main():
    ev = load_eval()
    dq = load_descq()
    dl = load_descq_levels()
    checked, problems, missing = cross_check(ev, dl)
    print(f"cross-check against the draft's Tables 2 to 5: {checked} rows compared, {len(problems)} differ")
    for p in problems:
        print("  DIFFERS:", p)
    for m in missing:
        print("  NO SOURCE:", m)
    if problems or missing:
        sys.exit("figures not written: a table entry disagrees with its verbatim source or has none")
    undrawn, unlisted = study_check()
    if undrawn or unlisted:
        sys.exit(f"figures not written: the study figure and the appendix differ: not in the figure {undrawn}, "
                 f"not in the appendix {unlisted}")
    if "--sigir" in sys.argv:            # the SIGIR version's single-column figures; nothing else
        global OUT
        OUT = os.path.join(ROOT, "paper", "sigir")
        fig_loss_col(ev)
        fig_searcher_col(load_s27_searcher())
        print("wrote", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith("_col.pdf"))), "in paper/sigir")
        return
    if "--s27" in sys.argv:              # the two session-27 figures alone (the others keep their bytes)
        path = os.path.join(OUT, "figdata.json")
        figdata = json.load(open(path))
        figdata["fig_searcher"] = fig_searcher(load_s27_searcher())
        figdata["fig_budgetsweep"] = fig_budgetsweep()
        with open(path, "w") as fh:
            json.dump(figdata, fh, indent=1, default=list)
        print("wrote fig_searcher.pdf, fig_budgetsweep.pdf")
        return
    if "--study" in sys.argv:            # the study figure alone (the other five keep their bytes)
        path = os.path.join(OUT, "figdata.json")
        figdata = json.load(open(path))
        figdata["fig_study"] = fig_study()
        with open(path, "w") as fh:
            json.dump(figdata, fh, indent=1, default=list)
        print("wrote fig_study.pdf")
        return
    figdata = {"fig_setup": "schematic, no data"}
    fig_setup()
    figdata["fig_study"] = fig_study()
    figdata["fig_loss"] = fig_loss(ev)
    figdata["fig_cosines"] = fig_cosines(ev)
    figdata["fig_budget"] = fig_budget(ev)
    figdata["fig_textq"] = fig_textq(dq)
    figdata["fig_searcher"] = fig_searcher(load_s27_searcher())
    figdata["fig_budgetsweep"] = fig_budgetsweep()
    with open(os.path.join(OUT, "figdata.json"), "w") as fh:
        json.dump(figdata, fh, indent=1, default=list)
    print("wrote", ", ".join(sorted(f for f in os.listdir(OUT) if f.endswith(".pdf"))))


if __name__ == "__main__":
    main()
