#!/usr/bin/env python3
"""dirvec session 22: a folder's summary written to a real file system and read back (BRIEF.md, session 22).

The study argues for a summary kept in a folder's metadata. Here the summaries are written to ext4
and the blocks a reader fetches from the device are counted, for four places a summary can live:

  attr     an extended attribute of the directory itself (user.dirvec)
  sidecar  a file .dirvec inside the directory
  tree     one index file at the root of each repository tree: a table of paths and offsets, then the
           summaries back to back
  global   one index file for the whole volume, built the same way
  files    no folder summary: every file carries its own one-bit vector in an attribute (user.vec)
           and the reader fetches the vectors of all files of a directory

The trees are real: every eligible directory of the repositories that session 19 harvested
(data/ghdirs_s19.jsonl.gz), laid out with its path, its ancestors and its number of kept files. Every
directory of a tree, eligible or an ancestor, gets a summary of B bytes of random data (the bytes'
values do not change what is read); every file is one block of random data. One image per layout and
budget, so that no layout pays for another's metadata.

Counting. /sys/block/<loop>/stat gives the sectors read from and written to the image. The file
system is unmounted and mounted again before each measurement, so nothing is in memory (this kernel
keeps metadata buffers through drop_caches). Blocks are 4 KiB. For a descent the reader starts at
the tree's root, lists the directory, fetches the summary of every child directory, steps into the
child on the way to the target, and repeats until the target is listed; "walk only" is the same walk
without fetching a summary, and the difference is what the summaries cost.

  store.py --trees data/ghdirs_s19.jsonl.gz --work /path/with/2GB [--n-trees 300] [--descents 400]
           [--budgets 2048,4000,8192] [--only attr,sidecar] > results/session22_outputs.md
Needs root (loop mounts), mkfs.ext4, and a kernel with ext4. Nothing here embeds or ranks anything.
"""
import argparse
import gzip
import json
import os
import random
import shutil
import struct
import subprocess
import sys
from collections import defaultdict

BLOCK = 4096
VEC = 256                      # one file's vector at one bit per dimension under E1
SEED = 20261105


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"FAILED: {cmd}\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
    return r


class Image:
    """An ext4 image on a loop device, mounted at <work>/mnt."""

    readahead = True          # False: no inode-table readahead and no file readahead, so only the blocks asked for are read

    def __init__(self, work, name, size_mb, mkfs_opts="", inodes=0):
        self.img = os.path.join(work, name + ".img")
        self.mnt = os.path.join(work, "mnt")
        os.makedirs(self.mnt, exist_ok=True)
        if os.path.exists(self.img):
            os.remove(self.img)
        sh(f"truncate -s {size_mb}M {self.img} && mkfs.ext4 -q -F {mkfs_opts} {'-N ' + str(inodes) if inodes else ''} {self.img}")
        self.dev = None

    def mount(self):
        sh(f"mount -o loop,noatime{'' if Image.readahead else ',inode_readahead_blks=0'} {self.img} {self.mnt}")
        self.dev = sh(f"findmnt -n -o SOURCE {self.mnt}").stdout.strip().split("/")[-1]
        if not Image.readahead:
            with open(f"/sys/block/{self.dev}/queue/read_ahead_kb", "w") as fh:
                fh.write("0\n")

    def umount(self):
        os.sync()
        sh(f"umount {self.mnt}")

    def remount(self):
        self.umount()
        self.mount()

    def counters(self):
        v = open(f"/sys/block/{self.dev}/stat").read().split()
        return int(v[2]), int(v[6])           # sectors read, sectors written

    def features(self):
        out = sh(f"dumpe2fs -h {self.img} 2>/dev/null | egrep 'Inode size|Block size|Filesystem features'").stdout
        return " ".join(out.split())

    def destroy(self):
        if self.dev:
            sh(f"umount {self.mnt}", check=False)
        if os.path.exists(self.img):
            os.remove(self.img)


def load_trees(path, n_trees, min_dirs, max_dirs):
    """[(repo, {dir path: files})] in the order of the list: repositories with min_dirs to max_dirs
    eligible directories. '' is the repository's root."""
    op = gzip.open if path.endswith(".gz") else open
    by_repo, order = defaultdict(dict), []
    with op(path, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            if r["repo"] not in by_repo:
                order.append(r["repo"])
            d = "/".join(safe(p) for p in r["dir"].split("/") if p)       # names as they are written to the image
            by_repo[r["repo"]][d] = max(by_repo[r["repo"]].get(d, 0), int(r["n_kept"]))
    trees = [(repo, by_repo[repo]) for repo in order if min_dirs <= len(by_repo[repo]) <= max_dirs]
    return trees[:n_trees]


def all_dirs(elig):
    """Every directory of a tree: the eligible ones and their ancestors, parents before children."""
    ds = {""}
    for d in elig:
        parts = d.split("/") if d else []
        for i in range(1, len(parts) + 1):
            ds.add("/".join(parts[:i]))
    return sorted(ds, key=lambda d: (d.count("/") + (1 if d else 0), d))


def safe(component):
    return component.replace("\x00", "_")[:200] or "_"


def tree_path(mnt, ti, d):
    return os.path.join(mnt, f"t{ti:04d}", *[safe(p) for p in d.split("/") if p])


def build(image, trees, layout, B, rng):
    """Write the trees and the summaries of one layout. Returns bytes of summaries written."""
    mnt = image.mnt
    blob = lambda n: rng.randbytes(n)  # noqa: E731
    gtable, gdata = [], []
    for ti, (repo, elig) in enumerate(trees):
        dirs = all_dirs(elig)
        ttable, tdata = [], []
        for d in dirs:
            p = tree_path(mnt, ti, d)
            os.makedirs(p, exist_ok=True)
            for i in range(elig.get(d, 0)):
                fp = os.path.join(p, f"f{i:03d}.dat")
                with open(fp, "wb") as fh:
                    fh.write(blob(BLOCK))
                if layout == "files":
                    os.setxattr(fp, "user.vec", blob(VEC))
            if layout == "attr":
                os.setxattr(p, "user.dirvec", blob(B))
            elif layout == "sidecar":
                with open(os.path.join(p, ".dirvec"), "wb") as fh:
                    fh.write(blob(B))
            elif layout == "tree":
                ttable.append(d)
                tdata.append(blob(B))
            elif layout == "global":
                gtable.append(f"t{ti:04d}/{d}")
                gdata.append(blob(B))
        if layout == "tree":
            write_index(os.path.join(tree_path(mnt, ti, ""), ".dirvec.idx"), ttable, tdata)
    if layout == "global":
        write_index(os.path.join(mnt, "dirvec.idx"), gtable, gdata)
    os.sync()


def write_index(path, keys, blobs):
    """An index file: a 4-byte table length, the table (JSON: path -> [offset, length]), the summaries."""
    off, table = 0, {}
    for k, b in zip(keys, blobs):
        table[k] = [off, len(b)]
        off += len(b)
    tb = json.dumps(table, separators=(",", ":")).encode()
    with open(path, "wb") as fh:
        fh.write(struct.pack("<I", len(tb)))
        fh.write(tb)
        for b in blobs:
            fh.write(b)


class IndexReader:
    def __init__(self, path):
        self.fd = os.open(path, os.O_RDONLY)
        n = struct.unpack("<I", os.pread(self.fd, 4, 0))[0]
        self.table = json.loads(os.pread(self.fd, n, 4))
        self.base = 4 + n

    def get(self, key):
        off, ln = self.table[key]
        return os.pread(self.fd, ln, self.base + off)

    def close(self):
        os.close(self.fd)


def fetch(layout, mnt, ti, d, reader, child_files=None):
    """The summary of directory d of tree ti under a layout; returns the bytes fetched."""
    p = tree_path(mnt, ti, d)
    if layout == "attr":
        return len(os.getxattr(p, "user.dirvec"))
    if layout == "sidecar":
        with open(os.path.join(p, ".dirvec"), "rb") as fh:
            return len(fh.read())
    if layout == "tree":
        return len(reader.get(d))
    if layout == "global":
        return len(reader.get(f"t{ti:04d}/{d}"))
    if layout == "files":                      # no folder summary: the vectors of the directory's own files
        return sum(len(os.getxattr(e.path, "user.vec")) for e in os.scandir(p) if e.is_file() and e.name.endswith(".dat"))
    return 0


def descend(layout, image, ti, target, with_summaries):
    """One descent from the root of tree ti to the directory `target`. Returns (blocks read, summaries
    fetched, bytes fetched). The reader lists a directory and fetches the summary of each child
    directory, then steps into the child on the way."""
    mnt = image.mnt
    image.remount()
    r0 = image.counters()[0]
    reader = None
    n_sum = n_bytes = 0
    if with_summaries and layout == "tree":
        reader = IndexReader(os.path.join(tree_path(mnt, ti, ""), ".dirvec.idx"))
    if with_summaries and layout == "global":
        reader = IndexReader(os.path.join(mnt, "dirvec.idx"))
    parts = [p for p in target.split("/") if p]
    cur = ""
    for depth in range(len(parts) + 1):
        p = tree_path(mnt, ti, cur)
        children = sorted(e.name for e in os.scandir(p) if e.is_dir(follow_symlinks=False))
        if with_summaries:
            for c in children:
                # the child's real path equals its safe name here: trees are built from safe names
                n_bytes += fetch(layout, mnt, ti, (cur + "/" + c) if cur else c, reader)
                n_sum += 1
        if depth < len(parts):
            cur = (cur + "/" + safe(parts[depth])) if cur else safe(parts[depth])
    if reader:
        reader.close()
    return (image.counters()[0] - r0) / 8.0, n_sum, n_bytes


def scan(layout, image, trees, with_summaries):
    """Every directory of every tree visited once (os.walk), its summary fetched. Blocks read."""
    mnt = image.mnt
    image.remount()
    r0 = image.counters()[0]
    reader = IndexReader(os.path.join(mnt, "dirvec.idx")) if with_summaries and layout == "global" else None
    n = 0
    for ti in range(len(trees)):
        root = tree_path(mnt, ti, "")
        tr = IndexReader(os.path.join(root, ".dirvec.idx")) if with_summaries and layout == "tree" else None
        for p, dnames, fnames in os.walk(root):
            dnames.sort()
            n += 1
            if with_summaries:
                d = os.path.relpath(p, root).replace(os.sep, "/")
                fetch(layout, mnt, ti, "" if d == "." else d, tr or reader)
        if tr:
            tr.close()
    if reader:
        reader.close()
    return (image.counters()[0] - r0) / 8.0, n


def update(layout, image, ti, d, B, rng):
    """One directory's summary rewritten in place. Blocks written by the time of sync and by unmount."""
    mnt = image.mnt
    image.remount()
    w0 = image.counters()[1]
    p = tree_path(mnt, ti, d)
    new = rng.randbytes(B)
    if layout == "attr":
        os.setxattr(p, "user.dirvec", new)
    elif layout == "sidecar":
        with open(os.path.join(p, ".dirvec"), "r+b") as fh:
            fh.write(new)
    elif layout in ("tree", "global"):
        path = os.path.join(tree_path(mnt, ti, ""), ".dirvec.idx") if layout == "tree" else os.path.join(mnt, "dirvec.idx")
        rd = IndexReader(path)
        off, ln = rd.table[d if layout == "tree" else f"t{ti:04d}/{d}"]
        base = rd.base
        rd.close()
        fd = os.open(path, os.O_WRONLY)
        os.pwrite(fd, new, base + off)
        os.close(fd)
    os.sync()
    w1 = image.counters()[1]
    image.remount()
    w2 = image.counters()[1]
    return (w1 - w0) / 8.0, (w2 - w0) / 8.0


def survival(image):
    """Which ways of copying a tree keep a directory's user attribute. Returns [(method, kept or not)]."""
    mnt = image.mnt
    src = os.path.join(mnt, "surv_src")
    os.makedirs(os.path.join(src, "docs"), exist_ok=True)
    with open(os.path.join(src, "docs", "a.txt"), "w") as fh:
        fh.write("x\n")
    os.setxattr(os.path.join(src, "docs"), "user.dirvec", b"\x01" * 2048)
    out = []

    def kept(dst):
        try:
            return len(os.getxattr(os.path.join(dst, "docs"), "user.dirvec")) == 2048
        except OSError:
            return False

    def trial(name, cmd, dst):
        r = sh(cmd, check=False)
        out.append((name, "not available here" if r.returncode == 127 or "not found" in r.stderr else
                    ("kept" if kept(dst) else "lost")))

    q = lambda p: "'" + p + "'"  # noqa: E731
    trial("cp -a", f"cp -a {q(src)} {q(mnt + '/s_cpa')}", mnt + "/s_cpa")
    trial("cp -r", f"cp -r {q(src)} {q(mnt + '/s_cpr')}", mnt + "/s_cpr")
    trial("cp -r --preserve=xattr", f"cp -r --preserve=xattr {q(src)} {q(mnt + '/s_cpx')}", mnt + "/s_cpx")
    trial("tar, default options", f"mkdir -p {q(mnt + '/s_tar')} && tar -C {q(src)} -cf - . | tar -C {q(mnt + '/s_tar')} -xf -", mnt + "/s_tar")
    trial("tar --xattrs", f"mkdir -p {q(mnt + '/s_tarx')} && tar --xattrs -C {q(src)} -cf - . | tar --xattrs -C {q(mnt + '/s_tarx')} -xf -", mnt + "/s_tarx")
    trial("rsync -a", f"rsync -a {q(src + '/')} {q(mnt + '/s_rs/')}", mnt + "/s_rs")
    trial("rsync -aX", f"rsync -aX {q(src + '/')} {q(mnt + '/s_rsx/')}", mnt + "/s_rsx")
    trial("git add, commit, clone", f"cd {q(src)} && git init -q . && git -c user.name=t -c user.email=t@t add -A && "
          f"git -c user.name=t -c user.email=t@t commit -q -m t && git clone -q {q(src)} {q(mnt + '/s_git')}", mnt + "/s_git")
    shutil.rmtree(os.path.join(src, ".git"), ignore_errors=True)
    trial("mv within the file system", f"mv {q(src)} {q(mnt + '/s_mv')}", mnt + "/s_mv")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trees", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--n-trees", type=int, default=300)
    ap.add_argument("--min-dirs", type=int, default=5)
    ap.add_argument("--max-dirs", type=int, default=400)
    ap.add_argument("--descents", type=int, default=400)
    ap.add_argument("--updates", type=int, default=40)
    ap.add_argument("--budgets", default="2048,4000,8192")
    ap.add_argument("--only", default="")
    ap.add_argument("--readahead", choices=["off", "default"], default="off",
                    help="off: only the blocks asked for are read; default: the kernel's readahead as shipped")
    args = ap.parse_args()
    Image.readahead = args.readahead == "default"
    if os.geteuid() != 0:
        sys.exit("store.py needs root for loop mounts")
    os.makedirs(args.work, exist_ok=True)
    trees = load_trees(args.trees, args.n_trees, args.min_dirs, args.max_dirs)
    if not trees:
        sys.exit("no tree in the list")
    n_dirs = sum(len(all_dirs(e)) for _, e in trees)
    n_elig = sum(len(e) for _, e in trees)
    n_files = sum(sum(e.values()) for _, e in trees)
    depth = [d.count("/") + 1 if d else 0 for _, e in trees for d in e]
    rng = random.Random(SEED)
    targets = []
    for _ in range(args.descents):
        ti = rng.randrange(len(trees))
        targets.append((ti, rng.choice(sorted(trees[ti][1]))))
    upd = targets[:args.updates]
    size_mb = max(256, int((2 * n_files + 6 * n_dirs) * BLOCK * 1.3 / 2 ** 20) + 192)   # room for an attribute block a file
    n_inodes = 2 * (n_files + n_dirs) + 4096
    budgets = [int(b) for b in args.budgets.split(",")]
    only = set(args.only.split(",")) if args.only else None

    ra = ("readahead as the kernel ships it (32 inode-table blocks, 128 KiB of file data)" if Image.readahead else
          "readahead off (inode_readahead_blks=0, read_ahead_kb=0): only the blocks asked for are read")
    out = [f"# Session 22 outputs, verbatim: summaries on ext4, blocks read and written; {ra}", ""]
    out.append(f"Kernel {os.uname().release}; {sh('mkfs.ext4 -V 2>&1 | head -1').stdout.strip()}; blocks of {BLOCK} bytes; "
               f"every measurement after an unmount and a mount. Trees: the first {len(trees)} repositories of "
               f"{args.trees} with {args.min_dirs} to {args.max_dirs} eligible directories: {n_dirs} directories "
               f"({n_elig} eligible, the others their ancestors), {n_files} files; depth of the eligible directories: mean "
               f"{sum(depth) / len(depth):.2f}, maximum {max(depth)}. Descents: {len(targets)} (a tree and one of its "
               f"eligible directories, drawn with seed {SEED}); updates: {len(upd)} of them.")
    out.append("")
    configs = []
    for B in budgets:
        for layout in ("attr", "sidecar", "tree", "global"):
            opts = "-O ea_inode" if layout == "attr" and B > 4000 else ""
            configs.append((layout, B, opts, "256-byte inodes" + (", ea_inode" if opts else "")))
    configs.append(("files", VEC, "", "256-byte inodes"))
    configs.append(("files", VEC, "-I 1024", "1024-byte inodes"))
    rows, base_done = [], {}
    for layout, B, opts, note in configs:
        if only and layout not in only:
            continue
        image = Image(args.work, f"{layout}_{B}", size_mb, opts, n_inodes)
        try:
            image.mount()
            build(image, trees, layout, B, random.Random(SEED + 1))
            feat = image.features()
            # the walk alone, on this very image, then the same walk with the summaries
            s0, nvis = scan(layout, image, trees, False)
            s1, _ = scan(layout, image, trees, True)
            d0 = [descend(layout, image, ti, t, False) for ti, t in targets]
            d1 = [descend(layout, image, ti, t, True) for ti, t in targets]
            up = [update(layout, image, ti, t, B, random.Random(SEED + 2)) for ti, t in upd] if layout != "files" else []
            m = lambda xs: sum(xs) / max(len(xs), 1)  # noqa: E731
            rows.append({
                "layout": layout, "B": B, "note": note, "features": feat,
                "scan_walk": s0, "scan_all": s1, "dirs": nvis,
                "desc_walk": m([x[0] for x in d0]), "desc_all": m([x[0] for x in d1]),
                "desc_n": m([x[1] for x in d1]), "desc_bytes": m([x[2] for x in d1]),
                "upd_sync": m([x[0] for x in up]) if up else None, "upd_umount": m([x[1] for x in up]) if up else None})
            print(f"  {layout} {B} done", file=sys.stderr, flush=True)
        finally:
            image.destroy()

    out.append("## Reading")
    out.append("")
    out.append("| where the summary lives | summary bytes | file system | scan: blocks per directory, walk only | scan: with "
               "summaries | scan: the summaries' share | descent: blocks, walk only | descent: with summaries | descent: "
               "the summaries' share | summaries fetched per descent | blocks per summary fetched |")
    out.append("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        ds = r["desc_all"] - r["desc_walk"]
        out.append(f"| {r['layout']} | {r['B']} | {r['note']} | {r['scan_walk'] / r['dirs']:.2f} | {r['scan_all'] / r['dirs']:.2f} | "
                   f"{(r['scan_all'] - r['scan_walk']) / r['dirs']:.2f} | {r['desc_walk']:.1f} | {r['desc_all']:.1f} | {ds:.1f} | "
                   f"{r['desc_n']:.1f} | {ds / max(r['desc_n'], 1e-9):.2f} |")
    out.append("")
    out.append("For `files` a 'summary' is the set of one-bit vectors of a directory's own files, 256 bytes each, and the "
               "bytes column is one vector.")
    out.append("")
    out.append("## Writing: one directory's summary replaced")
    out.append("")
    out.append("| where the summary lives | summary bytes | blocks written by sync | blocks written by unmount |")
    out.append("|---|---:|---:|---:|")
    for r in rows:
        if r["upd_sync"] is not None:
            out.append(f"| {r['layout']} | {r['B']} | {r['upd_sync']:.1f} | {r['upd_umount']:.1f} |")
    out.append("")
    image = Image(args.work, "survival", 64)
    try:
        image.mount()
        sv = survival(image)
    finally:
        image.destroy()
    out.append("## Copying: does a directory's user attribute arrive?")
    out.append("")
    out.append("| method | the attribute |")
    out.append("|---|---|")
    out += [f"| {a} | {b} |" for a, b in sv if b != "not available here"]
    out.append("")
    out.append("## File systems built")
    out.append("")
    seen = set()
    for r in rows:
        key = (r["note"], r["features"])
        if key not in seen:
            seen.add(key)
            out.append(f"- {r['note']}: {r['features']}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
