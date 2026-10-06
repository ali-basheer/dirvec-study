#!/usr/bin/env python3
"""dirvec session 23: a walk down whole repository trees, guided by folder summaries (BRIEF.md, session 23).

Every directory of a repository carries two summaries of B bytes: one of its own files and one of its
whole subtree. A file is the query; its directory is the target; the file is taken out of every
summary that held it. The reader starts at the repository's root. At a directory it scores "stay" by
the directory's own-files summary and each child directory by that child's subtree summary (the
largest cosine between the float32 query and what is stored), takes the best, and stops when "stay"
wins or there is no child. The walk succeeds when it stops in the target directory. It reads one
summary per candidate, so its cost is the number of candidates it scored. Beside it, `flat` reads the
own-files summary of every directory of the repository and takes the best.

Summaries (scripts/budget.py's definitions; n = B // ceil(dim / 8) one-bit vectors):
  mean      the mean of the files' vectors in the most precise format that fits B
  usample   the n files with the smallest hash priority, one bit each (merges exactly up a tree)
  fsample   every kind present keeps its n // kinds files of smallest priority (merges exactly)
  sample    n files dealt to the kinds one at a time, the largest kind first (does not merge exactly)
  all       every file at one bit, whatever it takes (no budget; the ceiling of the three samples)
and two that use no vector:
  names     the largest cosine between the query file's name and the names of the candidate's files
            (the whole lowercased name, extension included; character 3- and 4-grams, TF-IDF fitted on
            the names of the repository's embedded files), as a listing of unlimited length would allow
  chance    the expected success of a reader who picks a candidate at random at every step

A minority query is a file whose input group (image inputs against the rest) holds under half of the
repository's other embedded files, and that still has a sibling of its group in its own directory.
Equal scores go to the first candidate, "stay" before the children in path order, and in flat to the
first directory in the order of depth and path; a query's walk or flat rank is flagged when a rival
scores within 1e-6 of the winner or of the target.

  tree.py --model jina-embeddings-v4 --emb jina-embeddings-v4_s23 --manifest data/manifest_s23.jsonl
          --dirs data/dirs_s23.jsonl --gt data/gt_structural_s23.jsonl --label "S23 E1" [--registered]
Writes markdown to stdout and one row per query to data/emb/<emb>/walk_s23.jsonl.
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import budget as bg  # noqa: E402
import eval as ev  # noqa: E402
import quant as qn  # noqa: E402

BUDGETS = [int(b) for b in os.environ.get("S23_BUDGETS", "2048,8192").split(",")]     # the variables are for
REG_BUDGET = int(os.environ.get("S23_REG_BUDGET", 2048))                               # the self-test only
REGISTERED = ([2048, 8192], 2048)
VEC_POLICIES = ["mean", "usample", "fsample", "sample", "all"]
MARGIN, SESOI, MIN_OWNERS = 0.02, 0.05, 100
NEAR = 1e-6
MODS = ev.MODALITIES


def parent(v):
    return v.rsplit("/", 1)[0] if "/" in v else ""


def pick(policy, files, kinds, pr, n):
    """Positions (into `files`) that a sample policy keeps. kinds and pr are aligned with files."""
    m = len(files)
    if policy == "all" or m == 0:
        return list(range(m))
    if policy == "usample":
        return sorted(range(m), key=lambda i: pr[i])[:n]
    cnt = Counter(kinds)
    order = sorted(cnt, key=lambda k: (-cnt[k], MODS.index(k)))
    if policy == "fsample":
        q = n // len(order)
        if q == 0:
            order, q = order[:n], 1
        got = {k: q for k in order}
    else:                                                    # sample: the round-robin allotment of budget.py
        got = bg.allot(kinds, n)
    out = []
    for k in order:
        idx = sorted((i for i in range(m) if kinds[i] == k), key=lambda i: pr[i])
        out += idx[:got.get(k, 0)]
    return out


class Repo:
    """One repository: its directories as a tree and its embedded files."""

    def __init__(self, name, owner, dir_files):
        # dir_files: {repo_dir: [manifest rows of its embedded files]}, only directories that hold one
        self.name, self.owner = name, owner
        nodes = {""}
        for d in dir_files:
            v = d
            while v:
                nodes.add(v)
                v = parent(v)
        self.nodes = sorted(nodes, key=lambda v: (v.count("/") + (1 if v else 0), v))
        self.children = defaultdict(list)
        for v in self.nodes:
            if v:
                self.children[parent(v)].append(v)
        self.own = {v: list(dir_files.get(v, [])) for v in self.nodes}
        self.sub = {}
        for v in reversed(self.nodes):                       # children before parents
            s = list(self.own[v])
            for c in self.children[v]:
                s += self.sub[c]
            self.sub[v] = s
        self.files = self.sub[""]                           # manifest rows, in a fixed order
        self.loc = {r: i for i, r in enumerate(self.files)}

    def path_to(self, t):
        out, v = [t], t
        while v:
            v = parent(v)
            out.append(v)
        return out[::-1]                                     # root first


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--emb", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--gt", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--registered", action="store_true")
    ap.add_argument("--out", default="walk_s23.jsonl")
    args = ap.parse_args()
    R, L = ev.ROOT, args.label
    if args.registered and (BUDGETS, REG_BUDGET) != REGISTERED and not os.environ.get("S23_SELFTEST"):
        sys.exit("--registered: the budgets are not the registered ones (S23_BUDGETS or S23_REG_BUDGET is set)")

    emb_dir = os.path.join(ev.DATA, "emb", args.emb)
    V = np.load(os.path.join(emb_dir, "vectors.npy"))
    index = [json.loads(l) for l in open(os.path.join(emb_dir, "index.jsonl"))]
    manifest = [json.loads(l) for l in open(os.path.join(R, args.manifest))]
    dirs = {r["dir"]: r for r in (json.loads(l) for l in open(os.path.join(R, args.dirs)))}
    gt = [json.loads(l) for l in open(os.path.join(R, args.gt))]
    assert [r["path"] for r in index] == [r["path"] for r in manifest], "cache not in manifest order"
    assert all(r.get("repo") and r.get("owner") and r.get("repo_dir") is not None for r in dirs.values()), \
        "a directory row lacks repo, owner or repo_dir"
    ok = np.array([bool(r["ok"]) for r in index])
    mods = np.array([r["modality"] for r in manifest])
    is_img = np.isin(mods, ev.IMAGE_INPUTS)
    pos = {r["path"]: i for i, r in enumerate(manifest)}
    dim = V.shape[1]
    binb = qn.vec_bytes("bin", dim)
    prio = np.array([bg.prio(r["path"]) for r in manifest], dtype=np.int64)
    Vu = ev.unit(V).astype(np.float32)

    by_repo = defaultdict(lambda: defaultdict(list))
    for i, r in enumerate(manifest):
        if ok[i]:
            d = dirs[r["dir"]]
            by_repo[d["repo"]][d["repo_dir"]].append(i)
    owner_of = {d["repo"]: d["owner"] for d in dirs.values()}
    repos = {name: Repo(name, owner_of[name], df) for name, df in by_repo.items()}
    q_by_repo = defaultdict(list)
    for g in gt:
        i = pos[g["query_path"]]
        if ok[i]:
            q_by_repo[dirs[g["relevant_dir"]]["repo"]].append(i)

    rows = []                                                # one dict per query
    n_alone = [0]
    stored = {}
    keys = [(p, B) for B in BUDGETS for p in VEC_POLICIES] + [("names", 0)]
    for name in sorted(repos):
        rp = repos[name]
        qs = q_by_repo.get(name, [])
        if not qs or len(rp.nodes) < 2:
            continue
        F = np.array(rp.files, int)
        kinds_all = [str(mods[i]) for i in F]
        pr_all = [int(prio[i]) for i in F]
        Q = V[qs]
        Sbin = Q @ bg.bits(Vu[F]).T                          # (queries, files): the query against a file at one bit
        # names: character n-grams of the file names without their last extension
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        stems = [os.path.basename(manifest[i]["path"]).lower() for i in F]      # the whole name, extension included
        try:
            X = normalize(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), sublinear_tf=True).fit_transform(stems))
            Sname = np.asarray((X[[rp.loc[i] for i in qs]] @ X.T).todense(), dtype=np.float32)
        except ValueError:                                   # no n-gram at all (names shorter than three characters)
            Sname = np.zeros((len(qs), len(F)), np.float32)
        n_img_repo = int(is_img[F].sum())

        def sets_of(v):
            return [rp.loc[i] for i in rp.own[v]], [rp.loc[i] for i in rp.sub[v]]

        loc_sets = {v: sets_of(v) for v in rp.nodes}
        sums = {v: (None, None) for v in rp.nodes}

        def score_set(key, qi, li, files_loc, vsum, removed):
            """The query's score against the summary of the files `files_loc` (the query's own position
            li taken out when `removed`). -inf for an empty set."""
            policy, B = key
            fl = [f for f in files_loc if f != li] if removed else files_loc
            if not fl:
                return -np.inf
            if policy == "names":
                return float(Sname[qi, fl].max())
            if policy == "mean":
                m = ev.build("a", V[F[fl]], None)             # eval.py's pooled mean of the files left
                return float((qn.store(m, bg.mean_format(B, dim)) @ Q[qi])[0])
            n = B // binb
            chosen = pick(policy, fl, [kinds_all[f] for f in fl], [pr_all[f] for f in fl], n)
            return float(Sbin[qi, [fl[c] for c in chosen]].max())

        # static scores: every query against every node's two summaries, nothing removed
        static = {}
        for key in keys:
            if key not in stored:
                stored[key] = [0, 0, 0, 0]                    # own: summaries, vectors; subtree: summaries, vectors
            own_s = np.full((len(qs), len(rp.nodes)), -np.inf, np.float32)
            sub_s = np.full((len(qs), len(rp.nodes)), -np.inf, np.float32)
            policy, B = key
            for j, v in enumerate(rp.nodes):
                for arr, fl, vs in ((own_s, loc_sets[v][0], sums[v][0]), (sub_s, loc_sets[v][1], sums[v][1])):
                    if not fl:
                        continue
                    if policy == "names":
                        arr[:, j] = Sname[:, fl].max(axis=1)
                    elif policy == "mean":
                        arr[:, j] = Q @ qn.store(ev.build("a", V[F[fl]], None), bg.mean_format(B, dim))[0]
                    else:
                        chosen = pick(policy, fl, [kinds_all[f] for f in fl], [pr_all[f] for f in fl], B // binb)
                        arr[:, j] = Sbin[:, [fl[c] for c in chosen]].max(axis=1)
                        k0 = 0 if arr is own_s else 2
                        stored[key][k0] += 1
                        stored[key][k0 + 1] += len(chosen)
            static[key] = (own_s, sub_s)
        node_ix = {v: j for j, v in enumerate(rp.nodes)}
        dir_nodes = [v for v in rp.nodes if rp.own[v]]

        for qi, i in enumerate(qs):
            li = rp.loc[i]
            t = dirs[manifest[i]["dir"]]["repo_dir"]
            if len(rp.own[t]) < 2:                           # no other embedded file in its directory: not a query here
                n_alone[0] += 1
                continue
            path = rp.path_to(t)
            on_path = set(path)
            grp = bool(is_img[i])
            n_grp = n_img_repo if grp else len(F) - n_img_repo
            sib = any(bool(is_img[j]) == grp for j in rp.own[t] if j != i)
            row = {"query_path": manifest[i]["path"], "repo": name, "owner": rp.owner, "target": t,
                   "depth": len(path) - 1, "n_dirs": len(dir_nodes), "n_files": len(F),
                   "minority": bool((n_grp - 1) < 0.5 * (len(F) - 1) and sib), "image": grp, "sibling": bool(sib)}
            # chance: a uniform pick among the candidates at every step of the true path
            p_chance, v = 1.0, ""
            for step in range(len(path)):
                cands = (1 if [f for f in loc_sets[v][0] if f != li] else 0) + len(rp.children[v])
                p_chance *= 1.0 / max(cands, 1)
                if step + 1 < len(path):
                    v = path[step + 1]
            row["chance"] = p_chance
            for key in keys:
                own_s, sub_s = static[key]

                def s_own(v):
                    if v == t:
                        return score_set(key, qi, li, loc_sets[v][0], sums[v][0], True)
                    return float(own_s[qi, node_ix[v]])

                def s_sub(v):
                    if v in on_path:
                        return score_set(key, qi, li, loc_sets[v][1], sums[v][1], True)
                    return float(sub_s[qi, node_ix[v]])

                v, read, first, wtie = "", 0, None, 0
                while True:
                    cands = []
                    so = s_own(v)
                    if so > -np.inf:
                        cands.append(("", so))               # "" as a candidate means stay
                    cands += [(c, s_sub(c)) for c in rp.children[v]]
                    cands = [c for c in cands if c[1] > -np.inf]
                    if not cands:
                        break
                    read += len(cands)
                    best = max(range(len(cands)), key=lambda k: (cands[k][1], -k))   # the first of equal scores
                    if sum(1 for c in cands if c[1] >= cands[best][1] - NEAR) > 1:
                        wtie = 1
                    if first is None:
                        first = (v if cands[best][0] == "" else cands[best][0])
                    if cands[best][0] == "":
                        break
                    v = cands[best][0]
                flat = [(u, s_own(u)) for u in dir_nodes]     # in the order of depth and path
                flat = [x for x in flat if x[1] > -np.inf]
                st = dict(flat).get(t, -np.inf)
                # the target's rank: directories scoring higher, and those scoring the same that come before it
                rank, seen_t = 1, False
                for u, sc in flat:
                    if u == t:
                        seen_t = True
                    elif sc > st or (sc == st and not seen_t):
                        rank += 1
                tag = f"{key[0]}@{key[1]}" if key[1] else key[0]
                row[f"walk_{tag}"] = int(v == t)
                row[f"first_{tag}"] = int(first == (path[1] if len(path) > 1 else ""))
                row[f"read_{tag}"] = read
                row[f"wtie_{tag}"] = wtie
                row[f"flat_{tag}"] = int(rank == 1) if st > -np.inf else 0
                row[f"flat3_{tag}"] = int(rank <= 3) if st > -np.inf else 0
                row[f"ftie_{tag}"] = int(sum(1 for _, sc in flat if abs(sc - st) <= NEAR) > 1) if st > -np.inf else 0
            row["flat_read"] = len(flat)
            rows.append(row)
        print(f"  {name}: {len(qs)} queries, {len(rp.nodes)} directories", file=sys.stderr, flush=True)

    with open(os.path.join(emb_dir, args.out), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    # ---- tables
    nq = len(rows)
    owners = np.array([r["owner"] for r in rows])
    mino = np.array([r["minority"] for r in rows], dtype=bool)
    depth = np.array([r["depth"] for r in rows], dtype=int)
    if nq == 0:
        print(f"## {L}\n\nNo query survived (no directory with two embedded files in a tree).")
        return
    allq = np.ones(nq, bool)
    cells = [("all", allq), ("minority", mino), ("not minority", ~mino)]

    def col(k):
        return np.array([r[k] for r in rows], float)

    def wmean(x, sel):
        if not sel.any():
            return float("nan")
        _, g = np.unique(owners[sel], return_inverse=True)
        return float((np.bincount(g, weights=x[sel]) / np.bincount(g)).mean())

    def f3(x):
        return "n/a" if x != x else f"{x:.3f}"

    out = [f"## {L}: {args.model} ({dim} dimensions; one bit per dimension is {binb} bytes a vector)", ""]
    n_repo = len({r["repo"] for r in rows})
    out.append(f"Queries: {nq} over {n_repo} repositories and {len(set(owners))} owners ({n_alone[0]} files left out as "
               f"queries because their directory holds no other embedded file); minority {int(mino.sum())} "
               f"(from {len(set(owners[mino]))} owners). Directories holding an embedded file per repository: mean "
               f"{np.mean([r['n_dirs'] for r in rows]):.1f} (query-weighted); depth of the target: " +
               ", ".join(f"{d} {int((depth == d).sum())}" for d in sorted(set(depth))) +
               f". Summaries a walk reads, mean over queries: " +
               ", ".join(f"{p}@{B} {col(f'read_{p}@{B}').mean():.1f}" for B in BUDGETS for p in VEC_POLICIES) +
               f"; flat reads {col('flat_read').mean():.1f}. All rates below are owner-weighted: the mean over owners of "
               f"the owner's mean.")
    out.append("")
    out.append(f"### {L} success: the walk stops in the target directory; flat: the target is first among all directories")
    out.append("")
    out.append("| budget | summary | " + " | ".join(f"walk, {n} ({int(s.sum())})" for n, s in cells) + " | " +
               " | ".join(f"flat, {n}" for n, _ in cells) + " | flat top 3, all | first step right, all | first step right, minority |")
    out.append("|---|---|" + "---:|" * (2 * len(cells) + 3))
    tags = [(bg.lab(B), p, f"{p}@{B}") for B in BUDGETS for p in VEC_POLICIES] + [("none", "names", "names")]
    for b, p, tag in tags:
        out.append(f"| {b} | {p} | " + " | ".join(f3(wmean(col(f"walk_{tag}"), s)) for _, s in cells) + " | " +
                   " | ".join(f3(wmean(col(f"flat_{tag}"), s)) for _, s in cells) +
                   f" | {f3(wmean(col(f'flat3_{tag}'), allq))} | {f3(wmean(col(f'first_{tag}'), allq))} | "
                   f"{f3(wmean(col(f'first_{tag}'), mino))} |")
    out.append("| none | chance | " + " | ".join(f3(wmean(col("chance"), s)) for _, s in cells) + " | " +
               " | ".join(f3(wmean(1.0 / np.maximum(col("flat_read"), 1), s)) for _, s in cells) + " | | | |")
    out.append("")
    out.append(f"### {L} what is read and what is stored (reads owner-weighted; flat reads one summary a directory)")
    out.append("")
    out.append("| budget | summary | summaries the walk reads, all | minority | flat reads, all | walk reads as a share of flat | "
               "vectors stored per own-files summary | per subtree summary | walk decided by a near-tie, all | flat near-tie at the target, all |")
    out.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for b, p, tag in tags:
        key = (p, int(tag.split("@")[1])) if "@" in tag else (p, 0)
        st_ = stored.get(key, [0, 0, 0, 0])
        wr, fr = wmean(col(f"read_{tag}"), allq), wmean(col("flat_read"), allq)
        out.append(f"| {b} | {p} | {wr:.1f} | {wmean(col(f'read_{tag}'), mino):.1f} | {fr:.1f} | {wr / max(fr, 1e-9):.2f} | "
                   f"{st_[1] / max(st_[0], 1):.2f} | {st_[3] / max(st_[2], 1):.2f} | {f3(wmean(col(f'wtie_{tag}'), allq))} | "
                   f"{f3(wmean(col(f'ftie_{tag}'), allq))} |")
    out.append("")
    out.append(f"### {L} walk success by the depth of the target (owner-weighted)")
    out.append("")
    dbins = [("root", depth == 0), ("depth 1", depth == 1), ("depth 2", depth == 2), ("depth 3 or more", depth >= 3)]
    out.append("| budget | summary | " + " | ".join(f"{n} ({int(s.sum())})" for n, s in dbins) + " |")
    out.append("|---|---|" + "---:|" * len(dbins))
    for b, p, tag in tags:
        out.append(f"| {b} | {p} | " + " | ".join(f3(wmean(col(f"walk_{tag}"), s)) for _, s in dbins) + " |")
    out.append("| none | chance | " + " | ".join(f3(wmean(col("chance"), s)) for _, s in dbins) + " |")
    out.append("")

    def diff_row(name, x, sel, seed, kind=None):
        if sel.sum() < 2 or len(set(owners[sel])) < 2:
            return f"| {name} | {int(sel.sum())} | | | | | no test |"
        pt, i95, i98, no = bg.oboot(x[sel], owners[sel], seed)
        read = "none"
        if kind:
            lo, hi = i98
            if no < MIN_OWNERS:
                read = f"inconclusive (fewer than {MIN_OWNERS} owners)"
            elif kind == "loss":
                read = ("confirmed (lower bound at or above +0.05)" if lo >= SESOI else
                        "below +0.05 (upper bound under +0.05)" if hi < SESOI else
                        "present, size open (lower bound above zero)" if lo > 0 else "inconclusive")
            elif kind == "kinds":
                read = ("the kinds matter (lower bound above zero)" if lo > 0 else
                        "the uniform sample is better (upper bound below zero)" if hi < 0 else
                        "no difference at the margin (interval within -0.02 and +0.02)" if lo >= -MARGIN and hi <= MARGIN
                        else "inconclusive")
            else:
                read = ("not inferior (lower bound at or above -0.02)" if lo >= -MARGIN else
                        "inferior (upper bound under -0.02)" if hi < -MARGIN else "inconclusive")
        return (f"| {name} | {int(sel.sum())} | {no} | {pt:+.3f} | [{i95[0]:+.3f}, {i95[1]:+.3f}] | "
                f"[{i98[0]:+.3f}, {i98[1]:+.3f}] | {read} |")

    out.append(f"### {L} differences in success (owner-weighted, 10,000 resamples of owners)")
    out.append("")
    out.append("| difference | queries | owners | point | 95% | 98.33% | reading |")
    out.append("|---|---:|---:|---:|---|---|---|")
    for bi, B in enumerate(BUDGETS):
        reg = args.registered and B == REG_BUDGET
        lb = bg.lab(B)
        w = lambda p: col(f"walk_{p}@{B}")  # noqa: E731
        fl = lambda p: col(f"flat_{p}@{B}")  # noqa: E731
        s0 = 23000 + 100 * bi
        out.append(diff_row(f"{'H23a (primary)' if reg else lb}: walk, fsample - mean, minority, {lb}", w("fsample") - w("mean"),
                            mino, s0 + 1, "loss" if reg else None))
        out.append(diff_row(f"{'H23b (primary)' if reg else lb}: walk, fsample - usample, minority, {lb}",
                            w("fsample") - w("usample"), mino, s0 + 2, "kinds" if reg else None))
        out.append(diff_row(f"{'H23c (primary)' if reg else lb}: walk - flat, fsample, all queries, {lb}",
                            w("fsample") - fl("fsample"), allq, s0 + 3, "margin" if reg else None))
        for nm, x, sel, k in [("walk, fsample - mean, all", w("fsample") - w("mean"), allq, 4),
                              ("walk, usample - mean, minority", w("usample") - w("mean"), mino, 5),
                              ("walk, sample - fsample, minority", w("sample") - w("fsample"), mino, 6),
                              ("walk, sample - usample, minority (the kinds with every slot used)", w("sample") - w("usample"), mino, 13),
                              ("walk, all - fsample, minority", w("all") - w("fsample"), mino, 7),
                              ("walk, fsample - names, all", w("fsample") - col("walk_names"), allq, 8),
                              ("walk, fsample - names, minority", w("fsample") - col("walk_names"), mino, 9),
                              ("flat, fsample - mean, minority", fl("fsample") - fl("mean"), mino, 10),
                              ("walk - flat, mean, all", w("mean") - fl("mean"), allq, 11),
                              ("walk - flat, fsample, minority", w("fsample") - fl("fsample"), mino, 12)]:
            out.append(diff_row(f"{lb}: {nm}", x, sel, s0 + k))
    out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
