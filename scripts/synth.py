#!/usr/bin/env python3
"""dirvec session 10: synthetic folders for the same-modality dilution control.

Hosts: evaluation-split directories (the session 8 calibration split, eval.calib_split over the
session 5 dirs file, seed 20260930) whose embedded files (ok in the cache) are all of one input
group (image inputs: modality image and pdf_scanned; text inputs: the rest), with at least
--min-host embedded files. Guests: for each host, n_G embedded files of one other single-group
evaluation-split directory (a different Zenodo record), n_G = max(--min-guest, round(f * n_H /
(1 - f))) with f drawn uniformly from [--frac-lo, --frac-hi) with --seed, once per host, so both
sets share the hosts, the fractions and the seed. Two sets: SAME (the donor has the host's input
group) and CROSS (the other group).

Donor rule. Hosts are processed in a seeded random order. The donor pool for a host and a set is
the single-group evaluation-split directories of the required group with at least n_G embedded
files, other than the host, that have not donated in either set and have not received a guest in
either set; among them, directories with fewer than --min-host embedded files (never hosts) are
preferred, and the donor is drawn uniformly from the preferred ones, or from the rest when there
are none. A directory that donates is never a host, so the hosts are the same in both sets except
where a pool ran dry, in which case the host has a guest in one set only. The guest files are a
uniform draw without replacement from the donor's embedded files.

Outputs, per set: data/manifest_s10_<set>.jsonl (every session 5 row in the cache order; guest
rows get dir = host and guest_from = the donor directory), data/dirs_s10_<set>.jsonl (the session 5
dirs without the donor directories; host rows with the counts and image_frac of the synthetic
folder), data/gt_s10_<set>.jsonl (every embedded file of every synthetic folder that is a query in
the session 5 ground truth, that is not excluded by the session 5 dedupe: query_path, relevant_dir
= host, modality, image_frac_bucket of the synthetic folder, role host|guest, guest_frac = the
realised n_G / (n_H + n_G), guest_dir, set). The cache is not touched.
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from eval import IMAGE_INPUTS, MODALITIES, bucket_of, calib_split  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--emb", default="jina-embeddings-v4_s5")
    ap.add_argument("--manifest", default="data/manifest_s5.jsonl")
    ap.add_argument("--dirs", default="data/dirs_s5.jsonl")
    ap.add_argument("--gt", default="data/gt_structural_s5.jsonl")
    ap.add_argument("--calib", type=float, default=0.2)
    ap.add_argument("--calib-seed", type=int, default=20260930)
    ap.add_argument("--seed", type=int, default=20261001)
    ap.add_argument("--min-host", type=int, default=6)
    ap.add_argument("--min-guest", type=int, default=2)
    ap.add_argument("--frac-lo", type=float, default=0.2)
    ap.add_argument("--frac-hi", type=float, default=0.5)
    ap.add_argument("--out-prefix", default="data/%s_s10_%s.jsonl", help="pattern with (kind, set)")
    args = ap.parse_args()

    with open(os.path.join(ROOT, args.manifest)) as fh:
        manifest = [json.loads(l) for l in fh]
    with open(os.path.join(ROOT, "data", "emb", args.emb, "index.jsonl")) as fh:
        index = [json.loads(l) for l in fh]
    with open(os.path.join(ROOT, args.dirs)) as fh:
        dirs = {r["dir"]: r for r in (json.loads(l) for l in fh)}
    with open(os.path.join(ROOT, args.gt)) as fh:
        gt_queries = {g["query_path"] for g in (json.loads(l) for l in fh)}
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache not in manifest order"
    ok = [r["ok"] for r in index]

    calib = calib_split(dirs, args.calib, args.calib_seed)
    embedded = defaultdict(list)
    for i, r in enumerate(manifest):
        if ok[i]:
            embedded[r["dir"]].append(i)
    group = {}
    for d, rows in embedded.items():
        g = {("img" if manifest[i]["modality"] in IMAGE_INPUTS else "txt") for i in rows}
        if len(g) == 1 and d not in calib and dirs[d]["n_files"] >= 3:
            group[d] = g.pop()
    single = sorted(group)
    eligible = [d for d in single if len(embedded[d]) >= args.min_host]
    print(f"evaluation-split single-group directories: {len(single)} ("
          f"{sum(group[d] == 'img' for d in single)} image, {sum(group[d] == 'txt' for d in single)} text); "
          f"host-eligible (>= {args.min_host} embedded files): {len(eligible)} ("
          f"{sum(group[d] == 'img' for d in eligible)} image, {sum(group[d] == 'txt' for d in eligible)} text)")

    rng = np.random.default_rng(args.seed)
    order = [eligible[i] for i in rng.permutation(len(eligible))]
    donated, hosted = set(), set()
    plan = {"SAME": {}, "CROSS": {}}       # set -> host -> (donor, [file indices], f, n_G)
    fracs = {}
    for h in order:
        if h in donated:
            continue
        n_h = len(embedded[h])
        f = float(rng.uniform(args.frac_lo, args.frac_hi))
        n_g = max(args.min_guest, int(round(f * n_h / (1 - f))))
        fracs[h] = (f, n_h, n_g)
        for set_name in ("SAME", "CROSS"):
            need = group[h] if set_name == "SAME" else ("txt" if group[h] == "img" else "img")
            pool = [d for d in single if group[d] == need and d != h and len(embedded[d]) >= n_g
                    and d not in donated and d not in hosted]
            small = [d for d in pool if len(embedded[d]) < args.min_host]
            pick_from = small or pool
            if not pick_from:
                continue
            donor = pick_from[int(rng.integers(len(pick_from)))]
            files = sorted(embedded[donor])
            chosen = sorted(int(files[i]) for i in rng.choice(len(files), size=n_g, replace=False))
            plan[set_name][h] = (donor, chosen, f, n_g)
            donated.add(donor)
        if h in plan["SAME"] or h in plan["CROSS"]:
            hosted.add(h)

    both = sorted(set(plan["SAME"]) & set(plan["CROSS"]))
    print(f"hosts with a guest in both sets: {len(both)}; SAME only: {len(set(plan['SAME']) - set(both))}; "
          f"CROSS only: {len(set(plan['CROSS']) - set(both))}; host-eligible directories consumed as donors: "
          f"{sum(d in donated for d in eligible)}; hosts without a guest in either set: "
          f"{sum(h not in hosted and h not in donated for h in eligible)}")
    if len(both) < 150:
        print(f"NOTE: fewer than 150 hosts have a guest in both sets ({len(both)}); the brief says run anyway.")

    for set_name in ("SAME", "CROSS"):
        p = plan[set_name]
        donors = {donor for donor, _, _, _ in p.values()}
        host_of = {}
        for h, (donor, chosen, f, n_g) in p.items():
            for i in chosen:
                host_of[i] = h
        with open(os.path.join(ROOT, args.out_prefix % ("manifest", set_name.lower())), "w") as fh:
            for i, r in enumerate(manifest):
                row = dict(r)
                if i in host_of:
                    row["guest_from"] = r["dir"]
                    row["dir"] = host_of[i]
                fh.write(json.dumps(row) + "\n")
        new_dirs = {}
        for d, r in dirs.items():
            if d in donors:
                continue
            row = dict(r)
            if d in p:
                donor, chosen, f, n_g = p[d]
                c = Counter(manifest[i]["modality"] for i in chosen)
                row["n_files"] = r["n_files"] + n_g
                for m in MODALITIES:
                    row[f"n_{m}"] = r[f"n_{m}"] + c.get(m, 0)
                row["image_frac"] = row["n_image"] / row["n_files"]
                row["pdf_scanned_frac"] = row["n_pdf_scanned"] / row["n_files"]
                row["guest_dir"] = donor
                row["n_guest"] = n_g
            new_dirs[d] = row
        with open(os.path.join(ROOT, args.out_prefix % ("dirs", set_name.lower())), "w") as fh:
            for d in sorted(new_dirs):
                fh.write(json.dumps(new_dirs[d]) + "\n")
        n_q = Counter()
        realised = []
        with open(os.path.join(ROOT, args.out_prefix % ("gt", set_name.lower())), "w") as fh:
            for h in sorted(p):
                donor, chosen, f, n_g = p[h]
                n_h = len(embedded[h])
                frac = n_g / (n_h + n_g)
                realised.append(frac)
                b = bucket_of(new_dirs[h]["image_frac"])
                for i in sorted(embedded[h] + chosen, key=lambda i: manifest[i]["path"]):
                    if manifest[i]["path"] not in gt_queries:
                        continue
                    role = "guest" if i in chosen else "host"
                    n_q[role] += 1
                    fh.write(json.dumps({"query_path": manifest[i]["path"], "relevant_dir": h,
                                         "modality": manifest[i]["modality"], "image_frac_bucket": b,
                                         "role": role, "guest_frac": frac, "drawn_frac": f,
                                         "guest_dir": donor, "set": set_name}) + "\n")
        fr = np.array(realised)
        print(f"{set_name}: hosts {len(p)} ({sum(group[h] == 'img' for h in p)} image, {sum(group[h] == 'txt' for h in p)} text), "
              f"donor directories {len(donors)}, guest files {sum(len(v[1]) for v in p.values())}, "
              f"queries {n_q['host']} host + {n_q['guest']} guest; realised guest fraction min {fr.min():.3f} "
              f"median {np.median(fr):.3f} mean {fr.mean():.3f} max {fr.max():.3f}; "
              f"hosts in [0.2,0.35) {int((fr < 0.35).sum())}, in [0.35,0.5] {int((fr >= 0.35).sum())}; "
              f"ranking candidates {len(new_dirs)}")


if __name__ == "__main__":
    main()
