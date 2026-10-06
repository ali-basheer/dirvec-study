# Session 22 outputs, verbatim: summaries on ext4, blocks read and written; readahead off (inode_readahead_blks=0, read_ahead_kb=0): only the blocks asked for are read

Kernel 6.18.44-fc-v70; mke2fs 1.47.0 (5-Feb-2023); blocks of 4096 bytes; every measurement after an unmount and a mount. Trees: the first 300 repositories of data/ghdirs_s19.jsonl.gz with 5 to 400 eligible directories: 9934 directories (6426 eligible, the others their ancestors), 50906 files; depth of the eligible directories: mean 3.83, maximum 18. Descents: 400 (a tree and one of its eligible directories, drawn with seed 20261105); updates: 40 of them.

## Reading

| where the summary lives | summary bytes | file system | scan: blocks per directory, walk only | scan: with summaries | scan: the summaries' share | descent: blocks, walk only | descent: with summaries | descent: the summaries' share | summaries fetched per descent | blocks per summary fetched |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| attr | 2048 | 256-byte inodes | 1.32 | 2.32 | 1.00 | 9.3 | 23.2 | 13.9 | 11.6 | 1.20 |
| sidecar | 2048 | 256-byte inodes | 1.38 | 2.38 | 1.01 | 9.4 | 33.1 | 23.6 | 11.6 | 2.04 |
| tree | 2048 | 256-byte inodes | 1.32 | 1.85 | 0.53 | 9.3 | 18.8 | 9.6 | 11.6 | 0.82 |
| global | 2048 | 256-byte inodes | 1.32 | 1.83 | 0.51 | 9.3 | 161.9 | 152.6 | 11.6 | 13.15 |
| attr | 4000 | 256-byte inodes | 1.32 | 2.32 | 1.00 | 9.3 | 23.2 | 13.9 | 11.6 | 1.20 |
| sidecar | 4000 | 256-byte inodes | 1.38 | 2.38 | 1.01 | 9.4 | 33.1 | 23.7 | 11.6 | 2.04 |
| tree | 4000 | 256-byte inodes | 1.32 | 2.32 | 1.00 | 9.3 | 24.7 | 15.5 | 11.6 | 1.33 |
| global | 4000 | 256-byte inodes | 1.32 | 2.31 | 0.99 | 9.3 | 167.5 | 158.2 | 11.6 | 13.63 |
| attr | 8192 | 256-byte inodes, ea_inode | 1.38 | 3.38 | 2.01 | 9.5 | 36.1 | 26.6 | 11.6 | 2.30 |
| sidecar | 8192 | 256-byte inodes | 1.38 | 3.38 | 2.01 | 9.4 | 44.7 | 35.3 | 11.6 | 3.04 |
| tree | 8192 | 256-byte inodes | 1.32 | 3.36 | 2.04 | 9.3 | 37.1 | 27.8 | 11.6 | 2.40 |
| global | 8192 | 256-byte inodes | 1.32 | 3.33 | 2.01 | 9.3 | 180.4 | 171.1 | 11.6 | 14.74 |
| files | 256 | 256-byte inodes | 1.32 | 6.51 | 5.19 | 9.3 | 74.4 | 65.1 | 11.6 | 5.61 |
| files | 256 | 1024-byte inodes | 1.72 | 2.53 | 0.81 | 9.8 | 33.4 | 23.6 | 11.6 | 2.04 |

For `files` a 'summary' is the set of one-bit vectors of a directory's own files, 256 bytes each, and the bytes column is one vector.

## Writing: one directory's summary replaced

| where the summary lives | summary bytes | blocks written by sync | blocks written by unmount |
|---|---:|---:|---:|
| attr | 2048 | 7.0 | 11.0 |
| sidecar | 2048 | 6.0 | 10.0 |
| tree | 2048 | 6.5 | 10.4 |
| global | 2048 | 6.4 | 10.4 |
| attr | 4000 | 7.0 | 11.0 |
| sidecar | 4000 | 6.0 | 10.0 |
| tree | 4000 | 6.9 | 10.9 |
| global | 4000 | 7.0 | 11.0 |
| attr | 8192 | 23.9 | 27.9 |
| sidecar | 8192 | 7.0 | 11.0 |
| tree | 8192 | 8.0 | 12.0 |
| global | 8192 | 8.0 | 12.0 |

## Copying: does a directory's user attribute arrive?

| method | the attribute |
|---|---|
| cp -a | kept |
| cp -r | lost |
| cp -r --preserve=xattr | kept |
| tar, default options | lost |
| tar --xattrs | kept |
| git add, commit, clone | lost |
| mv within the file system | kept |

## File systems built

- 256-byte inodes: Filesystem features: has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum Block size: 4096 Inode size: 256
- 256-byte inodes, ea_inode: Filesystem features: has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg ea_inode sparse_super large_file huge_file dir_nlink extra_isize metadata_csum Block size: 4096 Inode size: 256
- 1024-byte inodes: Filesystem features: has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum Block size: 4096 Inode size: 1024

---

# Session 22 outputs, verbatim: summaries on ext4, blocks read and written; readahead as the kernel ships it (32 inode-table blocks, 128 KiB of file data)

Kernel 6.18.44-fc-v70; mke2fs 1.47.0 (5-Feb-2023); blocks of 4096 bytes; every measurement after an unmount and a mount. Trees: the first 300 repositories of data/ghdirs_s19.jsonl.gz with 5 to 400 eligible directories: 9934 directories (6426 eligible, the others their ancestors), 50906 files; depth of the eligible directories: mean 3.83, maximum 18. Descents: 400 (a tree and one of its eligible directories, drawn with seed 20261105); updates: 40 of them.

## Reading

| where the summary lives | summary bytes | file system | scan: blocks per directory, walk only | scan: with summaries | scan: the summaries' share | descent: blocks, walk only | descent: with summaries | descent: the summaries' share | summaries fetched per descent | blocks per summary fetched |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| attr | 2048 | 256-byte inodes | 1.38 | 2.38 | 1.00 | 62.4 | 77.1 | 14.6 | 11.6 | 1.26 |
| sidecar | 2048 | 256-byte inodes | 1.44 | 2.44 | 1.00 | 64.7 | 89.4 | 24.7 | 11.6 | 2.13 |
| tree | 2048 | 256-byte inodes | 1.38 | 1.91 | 0.53 | 62.1 | 86.7 | 24.5 | 11.6 | 2.11 |
| global | 2048 | 256-byte inodes | 1.38 | 1.89 | 0.51 | 62.4 | 498.3 | 435.8 | 11.6 | 37.55 |
| attr | 4000 | 256-byte inodes | 1.38 | 2.38 | 1.00 | 62.4 | 77.1 | 14.6 | 11.6 | 1.26 |
| sidecar | 4000 | 256-byte inodes | 1.44 | 2.44 | 1.00 | 64.7 | 89.4 | 24.7 | 11.6 | 2.13 |
| tree | 4000 | 256-byte inodes | 1.38 | 2.38 | 1.00 | 62.1 | 101.6 | 39.5 | 11.6 | 3.40 |
| global | 4000 | 256-byte inodes | 1.38 | 2.37 | 0.99 | 62.4 | 526.8 | 464.4 | 11.6 | 40.01 |
| attr | 8192 | 256-byte inodes, ea_inode | 1.44 | 3.44 | 2.00 | 64.5 | 92.9 | 28.3 | 11.6 | 2.44 |
| sidecar | 8192 | 256-byte inodes | 1.44 | 3.44 | 2.00 | 64.7 | 101.0 | 36.3 | 11.6 | 3.13 |
| tree | 8192 | 256-byte inodes | 1.38 | 3.42 | 2.04 | 62.1 | 130.3 | 68.2 | 11.6 | 5.88 |
| global | 8192 | 256-byte inodes | 1.38 | 3.39 | 2.01 | 62.4 | 615.3 | 552.8 | 11.6 | 47.63 |
| files | 256 | 256-byte inodes | 1.38 | 6.51 | 5.13 | 62.4 | 127.5 | 65.1 | 11.6 | 5.61 |
| files | 256 | 1024-byte inodes | 2.53 | 2.53 | 0.00 | 75.1 | 93.7 | 18.5 | 11.6 | 1.60 |

For `files` a 'summary' is the set of one-bit vectors of a directory's own files, 256 bytes each, and the bytes column is one vector.

## Writing: one directory's summary replaced

| where the summary lives | summary bytes | blocks written by sync | blocks written by unmount |
|---|---:|---:|---:|
| attr | 2048 | 7.0 | 11.0 |
| sidecar | 2048 | 6.0 | 10.0 |
| tree | 2048 | 6.5 | 10.4 |
| global | 2048 | 6.4 | 10.4 |
| attr | 4000 | 7.0 | 11.0 |
| sidecar | 4000 | 6.0 | 10.0 |
| tree | 4000 | 6.9 | 10.9 |
| global | 4000 | 7.0 | 11.0 |
| attr | 8192 | 23.9 | 27.9 |
| sidecar | 8192 | 7.0 | 11.0 |
| tree | 8192 | 8.0 | 12.0 |
| global | 8192 | 8.0 | 12.0 |

## Copying: does a directory's user attribute arrive?

| method | the attribute |
|---|---|
| cp -a | kept |
| cp -r | lost |
| cp -r --preserve=xattr | kept |
| tar, default options | lost |
| tar --xattrs | kept |
| git add, commit, clone | lost |
| mv within the file system | kept |

## File systems built

- 256-byte inodes: Filesystem features: has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum Block size: 4096 Inode size: 256
- 256-byte inodes, ea_inode: Filesystem features: has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg ea_inode sparse_super large_file huge_file dir_nlink extra_isize metadata_csum Block size: 4096 Inode size: 256
- 1024-byte inodes: Filesystem features: has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum Block size: 4096 Inode size: 1024
