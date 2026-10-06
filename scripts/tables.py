#!/usr/bin/env python3
"""Print the LaTeX rows of the draft's Tables 2 to 5 from the verbatim outputs in results/.

The rows are generated, not typed, so a table cannot drift from its source: Table 2's E4 row, Tables
3 and 5 in two blocks each (vision-language embedders E1 and E3 above, dual towers E2 and E4 below)
and Table 4's E4 rows. scripts/figures.py then cross-checks Tables 2 to 5 of paper/main.tex against
the same sources and stops on any difference. Usage: python3 scripts/tables.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figures as F  # noqa: E402

REPS3 = [("a", "1.00"), ("ac", "1.00"), ("bc2", "1.95"), ("tb2c", "2.00"), ("c", "5.20"), ("cc", "5.20"),
         ("d", "9.87"), ("dc", "9.87")]
NAMES = {"E1": "E1 jina-embeddings-v4", "E2": "E2 jina-clip-v2", "E3": "E3 gme-Qwen2-VL-2B",
         "E4": "E4 Nomic Embed v1.5"}
REPS5 = [("a", "pooled", "1.00"), ("ac", "pooled, query centered", "1.00"), ("tb2", "two blind clusters", "2.00"),
         ("tb2c", "the same, centered", "2.00"), ("c", "per-modality $k$-reps", "5.20"),
         ("cc", "the same, centered", "5.20"), ("d", "every file", "9.87")]


def f3(x):
    return f"{x:.3f}"


def table2_row(ev, key, label, enc_label):
    d = ev[key]
    p1, p2 = d["P1"], d["P2"]
    return (f"{label} & {enc_label} & ${p1['c-a']:+.3f}$ \\ci{{{p1['ci'][0]:+.3f}}}{{{p1['ci'][1]:+.3f}}} & "
            f"${p2['c-a']:+.3f}$ \\ci{{{p2['ci'][0]:+.3f}}}{{{p2['ci'][1]:+.3f}}} & ${d['M1']['c-a']:+.3f}$ & "
            f"${d['M2']['c-a']:+.3f}$ \\\\")


def table3_block(ev, encs):
    lines = [" & " + " & ".join(f"\\multicolumn{{5}}{{c}}{{{NAMES[e]}}}" for e in encs) + " \\\\"]
    lines.append("\\cmidrule(lr){2-6}\\cmidrule(lr){7-11}")
    lines.append(" & " + " & ".join(["all & P1 & P2 & M1 & M2"] * len(encs)) + " \\\\")
    lines.append("\\midrule")
    for rep, vec in REPS3:
        vals = []
        for e in encs:
            lv = ev[("S11", e)]["levels"][rep]
            assert f"{lv['vec']:.2f}" == vec, (e, rep, lv["vec"])
            vals += [f3(lv[c]) for c in F.CELLS]
        lines.append(f"\\rep{{{rep}}} ({vec}) & " + " & ".join(vals) + " \\\\")
    return lines


def table4_rows(ev, e):
    out = []
    for kind in ("uncentered", "centered"):
        g = ev[("S11", e)]["gap"][kind]
        out.append(f"S11, {e} & {kind} & " + " & ".join(f3(x) for x in g) + " \\\\")
    return out


def table5_block(lv, encs):
    lines = [" & " + " & ".join(f"\\multicolumn{{6}}{{c}}{{{NAMES[e]}}}" for e in encs) + " \\\\"]
    lines.append("\\cmidrule(lr){2-7}\\cmidrule(lr){8-13}")
    lines.append(" & " + " & ".join(["\\multicolumn{3}{c}{Q\\textsubscript{title}} & \\multicolumn{3}{c}{Q\\textsubscript{desc}}"] * len(encs)) + " \\\\")
    lines.append("\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}\\cmidrule(lr){8-10}\\cmidrule(lr){11-13}")
    lines.append(" & " + " & ".join(["all & T & I & all & T & I"] * len(encs)) + " \\\\")
    lines.append("\\midrule")
    for rep, desc, vec in REPS5:
        vals = []
        for e in encs:
            vals += [f3(x) for x in lv[e][rep]]
        lines.append(f"\\rep{{{rep}}} ({vec}) & " + " & ".join(vals) + " \\\\")
    return lines


def main():
    ev = F.load_eval()
    print("% Table 2, E4 row")
    if ("S11", "E4") in ev:
        print(table2_row(ev, ("S11", "E4"), "S11 (kill-tested)", "E4 (Nomic)"))
    print("% Table 3 blocks")
    for encs in (("E1", "E3"), ("E2", "E4")):
        if all(("S11", e) in ev for e in encs):
            print("\n".join(table3_block(ev, encs)))
    print("% Table 4, E4 rows")
    if ("S11", "E4") in ev:
        print("\n".join(table4_rows(ev, "E4")))
    lv = F.load_descq_levels()
    print("% Table 5 blocks")
    for encs in (("E1", "E3"), ("E2", "E4")):
        if all(e in lv for e in encs):
            print("\n".join(table5_block(lv, encs)))


if __name__ == "__main__":
    main()
