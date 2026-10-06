# Session 22 results: a folder's summary written to ext4 and read back

Protocol in BRIEF.md (5196f75) before the real trees were laid out; outputs verbatim in
results/session22_outputs.md. Two runs of scripts/store.py in the workspace on 5 October 2026
(kernel 6.18.44, mke2fs 1.47.0, ext4 with 4 KiB blocks on a loop device, root; no pod, no cost): one
with readahead off, one with the kernel's readahead as shipped. The trees are the first 300
repositories of data/ghdirs_s19.jsonl.gz with 5 to 400 eligible directories: 9,934 directories (6,426
eligible, the others their ancestors) and 50,906 files; the eligible directories lie at depth 3.83
on average, 18 at most. 400 descents and 40 updates, drawn with seed 20261105. This session measures
the store. Nothing was embedded or ranked and no hypothesis of the study is read on it.

## What a reader fetches (blocks of 4 KiB, after an unmount and a mount)

A cold descent lists 9.3 blocks of directories and inodes on its own with readahead off, and fetches
11.6 summaries on the way. What the summaries add, per summary fetched:

| where the summary lives | 2,048 bytes | 4,000 bytes | 8,192 bytes |
|---|---:|---:|---:|
| attribute of the directory | 1.20 | 1.20 | 2.30 (ea_inode) |
| sidecar file in the directory | 2.04 | 2.04 | 3.04 |
| one packed index per tree | 0.82 | 1.33 | 2.40 |
| one packed index for the volume | 13.15 | 13.63 | 14.74 |
| per-file vectors, 256-byte inodes | 5.61 per directory | | |
| per-file vectors, 1,024-byte inodes | 2.04 per directory | | |

With the kernel's readahead as shipped (32 inode-table blocks, 128 KiB of file data) the walk alone
reads 62.4 blocks and the same column reads: attribute 1.26, 1.26 and 2.44; sidecar 2.13, 2.13 and
3.13; index per tree 2.11, 3.40 and 5.88; volume index 37.55, 40.01 and 47.63; per-file vectors 5.61
and 1.60.

On a scan of every directory the summaries add 1.00 block a directory as an attribute, 1.01 as a
sidecar, and 0.53 in a packed index at 2,048 bytes, 1.00 at 4,000 and 2.0 at 8,192 in all three.

## Reading
- An attribute of the directory costs about one block beyond the directory's inode: 1.20 blocks per
  summary on a cold descent, at 2,048 and at 4,000 bytes alike, since ext4 keeps an inode's
  attributes in one block.
- A packed index at the root of the tree is cheaper where it packs two summaries in a block: 0.82 at
  2,048 bytes with readahead off, and 0.53 against 1.00 a directory on a full scan. At 4,000 bytes it
  is no cheaper (1.33), and with the kernel's default readahead it reads more than the attribute at
  every size, because reading a small range of a file pulls its neighbours in. So the attribute is
  not the cheapest place in every case. The packed index wins a full scan of small summaries.
- A sidecar file costs 0.8 block more than the attribute: its inode and its data block.
- One index for the whole volume, as built here with a table read whole, costs an order of magnitude
  more on a cold descent, all of it the table. A real one would need its own lookup structure. Not
  built.
- Without a folder summary, fetching the one-bit vectors of a directory's files costs 5.61 blocks a
  directory on default ext4, where a 256-byte attribute does not fit a 256-byte inode and takes a
  block of its own for every file, and 2.04 with 1,024-byte inodes, which hold it.
- 8,192 bytes, the 64 kilobits the study started from, are an ext4 attribute only with ea_inode:
  2.30 blocks to read, and 23.9 blocks written by sync to replace one, against 7.0 for an attribute
  of 2,048 or 4,000 bytes (sidecar 6.0, indexes 6.4 to 7.0; by unmount 27.9 against 11.0).
- A directory's user attribute arrives with cp -a, cp -r --preserve=xattr, tar --xattrs and mv
  within the file system. It is lost by cp -r, by tar with default options and by git, which stores
  no extended attribute: a cloned repository carries no summary until something writes one.

## Limits
One kernel, one file system with mke2fs defaults, a loop device, random bytes as summaries, one
block of data a file. Block counts, not times. The descent reads the summaries of every child of
every directory on the way; a reader that prunes would read fewer. Other file systems store
attributes differently (the paper's table of limits), and nothing here measures them.
