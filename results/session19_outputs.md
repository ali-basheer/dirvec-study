# Session 19 outputs, verbatim

Written by scripts/s19_run.sh on the pod, 2026-10-05T04:22Z, repo commit 889df59.
Nothing here is edited. The verdicts and the reading are in results/session19.md.

## Run log

```
01:52:17 start, commit 5683418, encoders E1 E4 E2, threads 3, prep 4
01:52:30 search API without a token answers HTTP 200
01:52:30 pool, round 1: at least 3000 usable repositories
pool done: 7959 repositories, 3080 usable, 8 days
02:04:15 harvest, round 1
harvest done (pool exhausted): 707 mixed, 600 other directories, 9997 files
harvest log: 3080 repositories, {'ok': 3078, 'oversize': 2}
02:32:35 pool, round 2: at least 5500 usable repositories
pool done: 14834 repositories, 5517 usable, 14 days
02:41:47 harvest, round 2
harvest done (full): 1000 mixed, 600 other directories, 12656 files
harvest log: 4322 repositories, {'ok': 4320, 'oversize': 2}
02:50:07 manifest
manifest: 12656 files, 1600 dirs; modality counts {'text': 7100, 'image': 5109, 'table': 83, 'other': 153, 'pdf_text': 189, 'pdf_scanned': 22}
notes: {'pdfinfo failed': 17, 'image unreadable': 16}
02:50:16 ground truth
02:51:02 commit history
history done: 1079 repositories read now, 10068 qualifying commits, 0 failed
commit-subject queries: 1162 over 522 directories, from 10068 qualifying commits in 819 directories (6918 dropped by the rules, 72 repeated within a directory, 1916 beyond three per directory).
02:54:02 corpus files pushed
02:54:07 manifest rows 12656; files missing or of another size 0
02:54:07 E1: embed all files (jina-embeddings-v4)
03:50:29 E1: files 12656; ok 12049; not ok by modality {'image': 466, 'other': 130, 'text': 10, 'table': 1}
03:50:29 E1: eval
7372 eval queries (236 dropped, no vector: {'image': 107, 'other': 128, 'table': 1}; 1717 in calibration directories), 1600 directories ranked
  rep a done
  rep ac done
  rep c done
  rep cc done
  rep d done
  rep dc done
  rep tb2c done
  rep tbc done
  rep cs done
03:52:56 E1: commit-subject queries
You have video processor config saved in `preprocessor.json` file which is deprecated. Video processor configs should be saved in their own `video_preprocessor.json` file. You can rename the file or load and save the processor back which renames it automatically. Loading from `preprocessor.json` will be removed in v5.0.
Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]Loading checkpoint shards:  50%|█████     | 1/2 [00:01<00:01,  1.14s/it]Loading checkpoint shards: 100%|██████████| 2/2 [00:01<00:00,  1.34it/s]Loading checkpoint shards: 100%|██████████| 2/2 [00:01<00:00,  1.24it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:01<00:00,  1.13s/it]Encoding texts...: 100%|██████████| 1/1 [00:01<00:00,  1.13s/it]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.40it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.03it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.65it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.90it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 15.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.56it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.87it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.78it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.15it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.16it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.98it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.12it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.71it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.51it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.21it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 17.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.94it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.89it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.01it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.51it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.28it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.99it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.62it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.89it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.94it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.66it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.26it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 17.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.66it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.06it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.06it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.84it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.54it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.58it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.62it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.84it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.00it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.69it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.71it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 13.59it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.82it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.34it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.66it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.55it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.57it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.77it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.24it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.97it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.24it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.79it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.04it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.12it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.76it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.00it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.45it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.00it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.42it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.27it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.21it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.88it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.03it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.87it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.86it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 14.31it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.55it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.98it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.71it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.70it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.16it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.61it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.34it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.88it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 13.74it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.24it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.16it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.88it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.55it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.47it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.96it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.86it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.31it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.70it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.19it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.94it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 17.21it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.58it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.80it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.76it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.03it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.98it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.54it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.83it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.08it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.65it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.39it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.70it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.74it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.96it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.32it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.84it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.90it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.07it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.87it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.06it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.19it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.11it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.84it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 27.54it/s]
1162 commit-subject queries embedded in 9s -> /workspace/dirvec/data/emb/jina-embeddings-v4_s19/commitq_s19.npz
03:54:16 E1: done; validity over E1
03:54:16 E4: embed all files (nomic-embed-v1.5)
04:02:07 E4: files 12656; ok 12049; not ok by modality {'image': 466, 'other': 130, 'text': 10, 'table': 1}
04:02:07 E4: eval
7372 eval queries (236 dropped, no vector: {'image': 107, 'other': 128, 'table': 1}; 1717 in calibration directories), 1600 directories ranked
  rep a done
  rep ac done
  rep c done
  rep cc done
  rep d done
  rep dc done
  rep tb2c done
  rep tbc done
  rep cs done
04:03:44 E4: commit-subject queries
Fetching 10 files:   0%|          | 0/10 [00:00<?, ?it/s]Fetching 10 files: 100%|██████████| 10/10 [00:00<00:00, 2214.87it/s]
Fetching 15 files:   0%|          | 0/15 [00:00<?, ?it/s]Fetching 15 files: 100%|██████████| 15/15 [00:00<00:00, 2765.48it/s]
<All keys matched successfully>
Fetching 3 files:   0%|          | 0/3 [00:00<?, ?it/s]Fetching 3 files: 100%|██████████| 3/3 [00:00<00:00, 1557.10it/s]
Using a slow image processor as `use_fast` is unset and a slow processor was saved with this model. `use_fast=True` will be the default behavior in v4.52, even if the model was saved with a slow processor. This will result in minor differences in outputs. You'll still be able to use a slow processor with `use_fast=False`.
E4: transformers 4.52.4, text NomicBertModel rotary scaling 2, image NomicVisionModel, processor CLIPImageProcessor size {'height': 224, 'width': 224} crop True
1162 commit-subject queries embedded in 1s -> /workspace/dirvec/data/emb/nomic-embed-v1.5_s19/commitq_s19.npz
04:04:23 E4: done; validity over E1 E4
04:04:23 E2: embed all files (jina-clip-v2)
04:19:19 E2: files 12656; ok 12049; not ok by modality {'image': 466, 'other': 130, 'text': 10, 'table': 1}
04:19:19 E2: eval
7372 eval queries (236 dropped, no vector: {'image': 107, 'other': 128, 'table': 1}; 1717 in calibration directories), 1600 directories ranked
  rep a done
  rep ac done
  rep c done
  rep cc done
  rep d done
  rep dc done
  rep tb2c done
  rep tbc done
  rep cs done
04:21:09 E2: commit-subject queries
/workspace/hf/modules/transformers_modules/jinaai/jina-clip-implementation/39e6a55ae971b59bea6e44675d237c99762e7ee2/modeling_clip.py:140: UserWarning: Flash attention is not installed. Check https://github.com/Dao-AILab/flash-attention?tab=readme-ov-file#installation-and-features for installation instructions, disabling
  warnings.warn(
/workspace/hf/modules/transformers_modules/jinaai/jina-clip-implementation/39e6a55ae971b59bea6e44675d237c99762e7ee2/modeling_clip.py:175: UserWarning: xFormers is not installed. Check https://github.com/facebookresearch/xformers?tab=readme-ov-file#installing-xformers for installation instructions, disabling
  warnings.warn(
1162 commit-subject queries embedded in 7s -> /workspace/dirvec/data/emb/jina-clip-v2_s19/commitq_s19.npz
04:22:25 E2: done; validity over E1 E4 E2
```

## Environment

```
python 3.12.3 numpy 2.5.2 scikit-learn 1.9.1 scipy 1.18.1 requests 2.34.2 pillow 12.3.0
git version 2.43.0
```

## Session 19 corpus

Pool: 14 days read, 23 search intervals (0 flagged incomplete by the API, 1 returned fewer rows than their count), 14834 repositories with at least 5 stars, 5517 usable (not a fork, a licence of the list, at most 200 MB).
Not usable: licence None 7174, licence GPL-3.0 848, licence NOASSERTION 626, licence AGPL-3.0 176, size 145, licence GPL-2.0 100, licence LGPL-3.0 51, licence MPL-2.0 51, licence MIT-0 32, licence LGPL-2.1 23, licence CC-BY-SA-4.0 19, licence WTFPL 12.
Usable by licence: MIT 4027, Apache-2.0 1123, BSD-3-Clause 173, Unlicense 57, CC0-1.0 46, BSD-2-Clause 39, ISC 25, CC-BY-4.0 23, 0BSD 4.

Harvest: 4322 repositories read (ok 4320, oversize 2); 3619 hold an eligible directory, 803 a mixed one, 1079 gave a directory to the scored set.

Eligible directories listed in the harvested repositories: 35970; mixed (an image file and another kept file): 1501, 0.042.
Per repository with an eligible directory (3619): mean share of mixed directories 0.089; repositories with at least one mixed directory 803.

| eligible directories | all | mixed | share mixed |
|---|---:|---:|---:|
| all | 35970 | 1501 | 0.042 |
| root | 2766 | 311 | 0.112 |
| depth 1 | 4388 | 339 | 0.077 |
| depth 2 or more | 28816 | 851 | 0.030 |
| 3 to 10 kept files | 30196 | 1167 | 0.039 |
| 11 to 30 kept files | 4749 | 299 | 0.063 |
| 31 to 100 kept files | 1025 | 35 | 0.034 |

Scored set: 1600 directories (1000 mixed by extension, 600 other), 12656 files, 1079 repositories, 1053 owners.
By depth: root 445, depth 1 398, depth 2 or more 757. By kept files: 3 to 10 1293, 11 to 30 264, 31 to 100 43.
Licences: MIT 1147, Apache-2.0 339, BSD-3-Clause 59, CC0-1.0 13, Unlicense 13, BSD-2-Clause 13, ISC 10, CC-BY-4.0 5, 0BSD 1.
Languages (GitHub's label, ten most frequent): Python 356, JavaScript 213, TypeScript 192, C++ 86, Dart 75, Jupyter Notebook 71, Java 61, HTML 52, Swift 51, C# 49.
Repository creation year: 2016 239, 2018 35, 2019 193, 2021 420, 2023 236, 2024 158, 2025 319.

Manifest: 12656 files in 1600 directories; modality text 7100, image 5109, pdf_text 189, other 153, table 83, pdf_scanned 22.
Directories per image-fraction bucket: [0,.2) 700, [.2,.5) 378, [.5,.8) 244, [.8,1] 278. Directories with both input groups in the manifest: 1000.

## build_gt.py report

```
{
 "queries": 9325,
 "qualifying_dirs": 1473,
 "qualifying_dirs_per_bucket": {
  "[0,.2)": 698,
  "[.2,.5)": 355,
  "[.5,.8)": 207,
  "[.8,1]": 213
 },
 "queries_per_bucket": {
  "[0,.2)": 5150,
  "[.2,.5)": 1719,
  "[.5,.8)": 1117,
  "[.8,1]": 1339
 },
 "queries_per_modality": {
  "text": 6505,
  "image": 2414,
  "table": 83,
  "pdf_text": 165,
  "other": 149,
  "pdf_scanned": 9
 },
 "dedupe": {
  "exact_files": 1853,
  "exact_pairs": 13521,
  "exact_pairs_cross_dir": 12202,
  "exact_pairs_within_dir": 1319,
  "files_excluded_as_queries_degenerate_image": 209,
  "files_excluded_as_queries_dup": 3228,
  "files_phashed": 4921,
  "files_simhashed": 6922,
  "image_files": 2497,
  "image_pairs": 119488,
  "image_pairs_cross_dir": 107475,
  "image_pairs_within_dir": 12013,
  "text_files": 542,
  "text_pairs": 2321,
  "text_pairs_cross_dir": 2259,
  "text_pairs_within_dir": 62
 },
 "kill_criterion_passed": true
}
```

## Commit-subject queries, build

```
commit-subject queries: 1162 over 522 directories, from 10068 qualifying commits in 819 directories (6918 dropped by the rules, 72 repeated within a directory, 1916 beyond three per directory).
```

## E1: embedding

```
files 12656; ok 12049; not ok by modality {'image': 466, 'other': 130, 'text': 10, 'table': 1}
```

## E1: eval.py

Model: jina-embeddings-v4. Queries: 7372 over 1172 directories; 1600 directories ranked (random recall@k = k/1600). Queries dropped for lack of a vector: 236 {'image': 107, 'other': 128, 'table': 1}. Queries in calibration directories, not used: 1717.

Mean representative vectors per directory: a 1.00, ac 1.00, c 3.70, cc 3.70, d 7.53, dc 7.53, tb2c 1.99, tbc 3.70, cs 3.97.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 7372 | 1172 | a | 0.676 | 0.768 | 0.792 | 0.823 | [0.776, 0.809] |
| all | 7372 | 1172 | ac | 0.690 | 0.782 | 0.808 | 0.838 | [0.790, 0.826] |
| all | 7372 | 1172 | c | 0.700 | 0.792 | 0.813 | 0.837 | [0.798, 0.828] |
| all | 7372 | 1172 | cc | 0.710 | 0.802 | 0.824 | 0.853 | [0.809, 0.840] |
| all | 7372 | 1172 | d | 0.699 | 0.792 | 0.812 | 0.838 | [0.796, 0.828] |
| all | 7372 | 1172 | dc | 0.710 | 0.805 | 0.827 | 0.855 | [0.813, 0.842] |
| all | 7372 | 1172 | tb2c | 0.706 | 0.800 | 0.822 | 0.851 | [0.807, 0.837] |
| all | 7372 | 1172 | tbc | 0.700 | 0.791 | 0.814 | 0.838 | [0.799, 0.829] |
| all | 7372 | 1172 | cs | 0.703 | 0.794 | 0.814 | 0.838 | [0.799, 0.829] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 4157 | 555 | a | 0.786 | 0.868 | 0.885 | 0.906 | [0.869, 0.898] |
| [0,.2) | 4157 | 555 | ac | 0.788 | 0.873 | 0.892 | 0.910 | [0.877, 0.905] |
| [0,.2) | 4157 | 555 | c | 0.774 | 0.865 | 0.883 | 0.899 | [0.866, 0.897] |
| [0,.2) | 4157 | 555 | cc | 0.776 | 0.871 | 0.890 | 0.911 | [0.873, 0.903] |
| [0,.2) | 4157 | 555 | d | 0.766 | 0.863 | 0.879 | 0.900 | [0.861, 0.894] |
| [0,.2) | 4157 | 555 | dc | 0.773 | 0.872 | 0.889 | 0.911 | [0.872, 0.903] |
| [0,.2) | 4157 | 555 | tb2c | 0.781 | 0.870 | 0.888 | 0.911 | [0.873, 0.901] |
| [0,.2) | 4157 | 555 | tbc | 0.774 | 0.865 | 0.884 | 0.900 | [0.867, 0.898] |
| [0,.2) | 4157 | 555 | cs | 0.774 | 0.866 | 0.884 | 0.900 | [0.868, 0.898] |
| [.2,.5) | 1357 | 284 | a | 0.515 | 0.628 | 0.650 | 0.698 | [0.616, 0.681] |
| [.2,.5) | 1357 | 284 | ac | 0.559 | 0.673 | 0.704 | 0.743 | [0.673, 0.732] |
| [.2,.5) | 1357 | 284 | c | 0.571 | 0.668 | 0.694 | 0.727 | [0.656, 0.728] |
| [.2,.5) | 1357 | 284 | cc | 0.600 | 0.702 | 0.723 | 0.766 | [0.692, 0.753] |
| [.2,.5) | 1357 | 284 | d | 0.591 | 0.682 | 0.709 | 0.741 | [0.671, 0.742] |
| [.2,.5) | 1357 | 284 | dc | 0.605 | 0.705 | 0.730 | 0.769 | [0.694, 0.762] |
| [.2,.5) | 1357 | 284 | tb2c | 0.595 | 0.697 | 0.726 | 0.763 | [0.698, 0.754] |
| [.2,.5) | 1357 | 284 | tbc | 0.567 | 0.668 | 0.692 | 0.730 | [0.655, 0.723] |
| [.2,.5) | 1357 | 284 | cs | 0.576 | 0.674 | 0.697 | 0.731 | [0.659, 0.731] |
| [.5,.8) | 865 | 165 | a | 0.501 | 0.603 | 0.642 | 0.680 | [0.574, 0.699] |
| [.5,.8) | 865 | 165 | ac | 0.536 | 0.642 | 0.682 | 0.736 | [0.614, 0.739] |
| [.5,.8) | 865 | 165 | c | 0.591 | 0.684 | 0.712 | 0.746 | [0.656, 0.763] |
| [.5,.8) | 865 | 165 | cc | 0.628 | 0.703 | 0.735 | 0.772 | [0.676, 0.790] |
| [.5,.8) | 865 | 165 | d | 0.607 | 0.694 | 0.726 | 0.750 | [0.671, 0.775] |
| [.5,.8) | 865 | 165 | dc | 0.625 | 0.710 | 0.749 | 0.778 | [0.695, 0.799] |
| [.5,.8) | 865 | 165 | tb2c | 0.582 | 0.702 | 0.733 | 0.765 | [0.673, 0.788] |
| [.5,.8) | 865 | 165 | tbc | 0.597 | 0.680 | 0.716 | 0.750 | [0.660, 0.765] |
| [.5,.8) | 865 | 165 | cs | 0.601 | 0.686 | 0.716 | 0.751 | [0.659, 0.767] |
| [.8,1] | 993 | 168 | a | 0.590 | 0.684 | 0.729 | 0.770 | [0.679, 0.775] |
| [.8,1] | 993 | 168 | ac | 0.595 | 0.674 | 0.709 | 0.752 | [0.635, 0.779] |
| [.8,1] | 993 | 168 | c | 0.659 | 0.748 | 0.772 | 0.804 | [0.726, 0.813] |
| [.8,1] | 993 | 168 | cc | 0.653 | 0.733 | 0.764 | 0.798 | [0.715, 0.808] |
| [.8,1] | 993 | 168 | d | 0.644 | 0.729 | 0.749 | 0.785 | [0.694, 0.796] |
| [.8,1] | 993 | 168 | dc | 0.663 | 0.744 | 0.768 | 0.805 | [0.716, 0.813] |
| [.8,1] | 993 | 168 | tb2c | 0.648 | 0.732 | 0.757 | 0.792 | [0.706, 0.803] |
| [.8,1] | 993 | 168 | tbc | 0.663 | 0.746 | 0.776 | 0.804 | [0.730, 0.815] |
| [.8,1] | 993 | 168 | cs | 0.665 | 0.748 | 0.767 | 0.803 | [0.722, 0.807] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 1846 | 642 | a | 0.514 | 0.606 | 0.648 | 0.692 | [0.608, 0.682] |
| image | 1846 | 642 | ac | 0.515 | 0.599 | 0.648 | 0.698 | [0.605, 0.688] |
| image | 1846 | 642 | c | 0.592 | 0.675 | 0.702 | 0.737 | [0.666, 0.736] |
| image | 1846 | 642 | cc | 0.600 | 0.671 | 0.696 | 0.735 | [0.659, 0.729] |
| image | 1846 | 642 | d | 0.590 | 0.672 | 0.697 | 0.730 | [0.660, 0.732] |
| image | 1846 | 642 | dc | 0.604 | 0.683 | 0.710 | 0.746 | [0.674, 0.743] |
| image | 1846 | 642 | tb2c | 0.574 | 0.657 | 0.684 | 0.725 | [0.644, 0.718] |
| image | 1846 | 642 | tbc | 0.593 | 0.672 | 0.702 | 0.739 | [0.666, 0.735] |
| image | 1846 | 642 | cs | 0.599 | 0.676 | 0.699 | 0.741 | [0.665, 0.732] |
| pdf_text | 148 | 37 | a | 0.858 | 0.939 | 0.939 | 0.939 | [0.851, 0.988] |
| pdf_text | 148 | 37 | ac | 0.851 | 0.939 | 0.939 | 0.939 | [0.851, 0.988] |
| pdf_text | 148 | 37 | c | 0.845 | 0.953 | 0.959 | 0.959 | [0.903, 0.993] |
| pdf_text | 148 | 37 | cc | 0.872 | 0.953 | 0.953 | 0.966 | [0.894, 0.987] |
| pdf_text | 148 | 37 | d | 0.838 | 0.939 | 0.959 | 0.959 | [0.903, 0.993] |
| pdf_text | 148 | 37 | dc | 0.858 | 0.946 | 0.953 | 0.966 | [0.894, 0.987] |
| pdf_text | 148 | 37 | tb2c | 0.872 | 0.953 | 0.953 | 0.953 | [0.884, 0.993] |
| pdf_text | 148 | 37 | tbc | 0.858 | 0.959 | 0.959 | 0.973 | [0.903, 0.993] |
| pdf_text | 148 | 37 | cs | 0.858 | 0.953 | 0.959 | 0.959 | [0.903, 0.993] |
| text | 5273 | 1078 | a | 0.728 | 0.819 | 0.838 | 0.864 | [0.821, 0.852] |
| text | 5273 | 1078 | ac | 0.748 | 0.842 | 0.860 | 0.883 | [0.843, 0.873] |
| text | 5273 | 1078 | c | 0.732 | 0.827 | 0.847 | 0.867 | [0.831, 0.862] |
| text | 5273 | 1078 | cc | 0.742 | 0.842 | 0.864 | 0.890 | [0.848, 0.878] |
| text | 5273 | 1078 | d | 0.731 | 0.828 | 0.848 | 0.871 | [0.830, 0.863] |
| text | 5273 | 1078 | dc | 0.742 | 0.843 | 0.864 | 0.889 | [0.847, 0.878] |
| text | 5273 | 1078 | tb2c | 0.747 | 0.845 | 0.866 | 0.891 | [0.852, 0.880] |
| text | 5273 | 1078 | tbc | 0.732 | 0.828 | 0.849 | 0.869 | [0.832, 0.864] |
| text | 5273 | 1078 | cs | 0.733 | 0.830 | 0.849 | 0.868 | [0.833, 0.865] |
| table | 77 | 34 | a | 0.688 | 0.805 | 0.831 | 0.857 | [0.648, 0.921] |
| table | 77 | 34 | ac | 0.649 | 0.792 | 0.818 | 0.857 | [0.620, 0.922] |
| table | 77 | 34 | c | 0.740 | 0.818 | 0.857 | 0.870 | [0.721, 0.942] |
| table | 77 | 34 | cc | 0.753 | 0.857 | 0.883 | 0.922 | [0.760, 0.957] |
| table | 77 | 34 | d | 0.740 | 0.844 | 0.857 | 0.870 | [0.721, 0.942] |
| table | 77 | 34 | dc | 0.753 | 0.844 | 0.870 | 0.909 | [0.739, 0.949] |
| table | 77 | 34 | tb2c | 0.701 | 0.818 | 0.844 | 0.896 | [0.680, 0.937] |
| table | 77 | 34 | tbc | 0.714 | 0.792 | 0.831 | 0.844 | [0.660, 0.927] |
| table | 77 | 34 | cs | 0.740 | 0.818 | 0.857 | 0.870 | [0.721, 0.942] |
| other | 21 | 9 | a | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | ac | 0.810 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | c | 0.905 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | cc | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | d | 0.905 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | dc | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | tb2c | 0.810 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | tbc | 0.905 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | cs | 0.905 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 142 | 121 | a | 0.141 | 0.183 | 0.232 | 0.296 | [0.153, 0.324] |
| image [0,.2) | 142 | 121 | ac | 0.176 | 0.268 | 0.345 | 0.366 | [0.255, 0.438] |
| image [0,.2) | 142 | 121 | c | 0.204 | 0.310 | 0.338 | 0.380 | [0.244, 0.424] |
| image [0,.2) | 142 | 121 | cc | 0.246 | 0.352 | 0.373 | 0.415 | [0.282, 0.463] |
| image [0,.2) | 142 | 121 | d | 0.239 | 0.345 | 0.359 | 0.387 | [0.263, 0.443] |
| image [0,.2) | 142 | 121 | dc | 0.268 | 0.380 | 0.408 | 0.423 | [0.321, 0.497] |
| image [0,.2) | 142 | 121 | tb2c | 0.211 | 0.275 | 0.289 | 0.359 | [0.208, 0.371] |
| image [0,.2) | 142 | 121 | tbc | 0.211 | 0.296 | 0.331 | 0.387 | [0.241, 0.416] |
| image [0,.2) | 142 | 121 | cs | 0.204 | 0.303 | 0.338 | 0.394 | [0.244, 0.423] |
| image [.2,.5) | 358 | 242 | a | 0.204 | 0.296 | 0.321 | 0.380 | [0.252, 0.394] |
| image [.2,.5) | 358 | 242 | ac | 0.229 | 0.318 | 0.380 | 0.453 | [0.309, 0.451] |
| image [.2,.5) | 358 | 242 | c | 0.327 | 0.388 | 0.419 | 0.478 | [0.348, 0.484] |
| image [.2,.5) | 358 | 242 | cc | 0.352 | 0.422 | 0.444 | 0.503 | [0.373, 0.511] |
| image [.2,.5) | 358 | 242 | d | 0.338 | 0.408 | 0.441 | 0.492 | [0.370, 0.509] |
| image [.2,.5) | 358 | 242 | dc | 0.346 | 0.436 | 0.464 | 0.525 | [0.388, 0.533] |
| image [.2,.5) | 358 | 242 | tb2c | 0.335 | 0.411 | 0.447 | 0.503 | [0.374, 0.517] |
| image [.2,.5) | 358 | 242 | tbc | 0.324 | 0.399 | 0.419 | 0.483 | [0.349, 0.485] |
| image [.2,.5) | 358 | 242 | cs | 0.330 | 0.394 | 0.419 | 0.478 | [0.351, 0.485] |
| image [.5,.8) | 473 | 140 | a | 0.586 | 0.687 | 0.732 | 0.763 | [0.663, 0.791] |
| image [.5,.8) | 473 | 140 | ac | 0.579 | 0.672 | 0.725 | 0.776 | [0.659, 0.788] |
| image [.5,.8) | 473 | 140 | c | 0.641 | 0.727 | 0.759 | 0.789 | [0.701, 0.813] |
| image [.5,.8) | 473 | 140 | cc | 0.674 | 0.723 | 0.755 | 0.791 | [0.684, 0.819] |
| image [.5,.8) | 473 | 140 | d | 0.658 | 0.736 | 0.772 | 0.793 | [0.715, 0.823] |
| image [.5,.8) | 473 | 140 | dc | 0.670 | 0.738 | 0.776 | 0.805 | [0.716, 0.829] |
| image [.5,.8) | 473 | 140 | tb2c | 0.607 | 0.717 | 0.746 | 0.776 | [0.678, 0.808] |
| image [.5,.8) | 473 | 140 | tbc | 0.638 | 0.717 | 0.761 | 0.793 | [0.700, 0.814] |
| image [.5,.8) | 473 | 140 | cs | 0.655 | 0.732 | 0.763 | 0.801 | [0.706, 0.814] |
| image [.8,1] | 873 | 139 | a | 0.662 | 0.758 | 0.804 | 0.845 | [0.756, 0.851] |
| image [.8,1] | 873 | 139 | ac | 0.652 | 0.729 | 0.766 | 0.810 | [0.686, 0.845] |
| image [.8,1] | 873 | 139 | c | 0.738 | 0.824 | 0.845 | 0.874 | [0.804, 0.884] |
| image [.8,1] | 873 | 139 | cc | 0.718 | 0.796 | 0.820 | 0.851 | [0.771, 0.868] |
| image [.8,1] | 873 | 139 | d | 0.715 | 0.798 | 0.816 | 0.849 | [0.763, 0.866] |
| image [.8,1] | 873 | 139 | dc | 0.729 | 0.804 | 0.824 | 0.858 | [0.773, 0.871] |
| image [.8,1] | 873 | 139 | tb2c | 0.712 | 0.788 | 0.812 | 0.849 | [0.763, 0.862] |
| image [.8,1] | 873 | 139 | tbc | 0.741 | 0.821 | 0.847 | 0.872 | [0.806, 0.884] |
| image [.8,1] | 873 | 139 | cs | 0.742 | 0.821 | 0.837 | 0.873 | [0.795, 0.876] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 4011 | 555 | a | 0.810 | 0.893 | 0.909 | 0.927 | [0.895, 0.921] |
| textlike [0,.2) | 4011 | 555 | ac | 0.811 | 0.896 | 0.911 | 0.930 | [0.898, 0.924] |
| textlike [0,.2) | 4011 | 555 | c | 0.795 | 0.885 | 0.902 | 0.917 | [0.888, 0.917] |
| textlike [0,.2) | 4011 | 555 | cc | 0.795 | 0.890 | 0.908 | 0.929 | [0.895, 0.922] |
| textlike [0,.2) | 4011 | 555 | d | 0.785 | 0.881 | 0.898 | 0.918 | [0.882, 0.913] |
| textlike [0,.2) | 4011 | 555 | dc | 0.791 | 0.890 | 0.906 | 0.929 | [0.892, 0.921] |
| textlike [0,.2) | 4011 | 555 | tb2c | 0.802 | 0.892 | 0.909 | 0.931 | [0.896, 0.923] |
| textlike [0,.2) | 4011 | 555 | tbc | 0.794 | 0.886 | 0.904 | 0.919 | [0.889, 0.918] |
| textlike [0,.2) | 4011 | 555 | cs | 0.794 | 0.886 | 0.904 | 0.918 | [0.889, 0.918] |
| textlike [.2,.5) | 996 | 282 | a | 0.626 | 0.746 | 0.767 | 0.811 | [0.733, 0.801] |
| textlike [.2,.5) | 996 | 282 | ac | 0.676 | 0.799 | 0.819 | 0.846 | [0.786, 0.849] |
| textlike [.2,.5) | 996 | 282 | c | 0.659 | 0.767 | 0.792 | 0.816 | [0.755, 0.827] |
| textlike [.2,.5) | 996 | 282 | cc | 0.689 | 0.801 | 0.822 | 0.860 | [0.788, 0.854] |
| textlike [.2,.5) | 996 | 282 | d | 0.681 | 0.780 | 0.804 | 0.830 | [0.766, 0.840] |
| textlike [.2,.5) | 996 | 282 | dc | 0.697 | 0.801 | 0.824 | 0.855 | [0.789, 0.858] |
| textlike [.2,.5) | 996 | 282 | tb2c | 0.688 | 0.799 | 0.825 | 0.856 | [0.794, 0.856] |
| textlike [.2,.5) | 996 | 282 | tbc | 0.653 | 0.764 | 0.789 | 0.817 | [0.751, 0.825] |
| textlike [.2,.5) | 996 | 282 | cs | 0.664 | 0.774 | 0.796 | 0.821 | [0.757, 0.833] |
| textlike [.5,.8) | 392 | 159 | a | 0.398 | 0.503 | 0.533 | 0.579 | [0.436, 0.624] |
| textlike [.5,.8) | 392 | 159 | ac | 0.485 | 0.605 | 0.630 | 0.689 | [0.536, 0.713] |
| textlike [.5,.8) | 392 | 159 | c | 0.531 | 0.633 | 0.656 | 0.694 | [0.571, 0.726] |
| textlike [.5,.8) | 392 | 159 | cc | 0.571 | 0.679 | 0.712 | 0.750 | [0.639, 0.778] |
| textlike [.5,.8) | 392 | 159 | d | 0.546 | 0.643 | 0.671 | 0.699 | [0.592, 0.736] |
| textlike [.5,.8) | 392 | 159 | dc | 0.571 | 0.676 | 0.717 | 0.745 | [0.645, 0.782] |
| textlike [.5,.8) | 392 | 159 | tb2c | 0.551 | 0.684 | 0.717 | 0.753 | [0.648, 0.783] |
| textlike [.5,.8) | 392 | 159 | tbc | 0.546 | 0.635 | 0.661 | 0.699 | [0.579, 0.730] |
| textlike [.5,.8) | 392 | 159 | cs | 0.536 | 0.630 | 0.658 | 0.691 | [0.574, 0.726] |
| textlike [.8,1] | 120 | 107 | a | 0.067 | 0.142 | 0.183 | 0.225 | [0.104, 0.288] |
| textlike [.8,1] | 120 | 107 | ac | 0.183 | 0.275 | 0.292 | 0.333 | [0.197, 0.396] |
| textlike [.8,1] | 120 | 107 | c | 0.083 | 0.200 | 0.242 | 0.292 | [0.160, 0.339] |
| textlike [.8,1] | 120 | 107 | cc | 0.175 | 0.275 | 0.358 | 0.408 | [0.260, 0.467] |
| textlike [.8,1] | 120 | 107 | d | 0.125 | 0.225 | 0.267 | 0.325 | [0.175, 0.364] |
| textlike [.8,1] | 120 | 107 | dc | 0.183 | 0.308 | 0.367 | 0.417 | [0.276, 0.472] |
| textlike [.8,1] | 120 | 107 | tb2c | 0.175 | 0.325 | 0.358 | 0.375 | [0.265, 0.466] |
| textlike [.8,1] | 120 | 107 | tbc | 0.092 | 0.200 | 0.267 | 0.308 | [0.178, 0.367] |
| textlike [.8,1] | 120 | 107 | cs | 0.100 | 0.217 | 0.258 | 0.292 | [0.169, 0.358] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 500 | 363 | 0.296 | 0.370 | 0.396 | 0.424 | 0.418 | 0.448 | 0.402 | 0.394 | 0.396 | +0.100 | [+0.060, +0.142] |
| P2 textlike in [.5,.8)+[.8,1] | 512 | 266 | 0.451 | 0.551 | 0.559 | 0.629 | 0.576 | 0.635 | 0.633 | 0.568 | 0.564 | +0.107 | [+0.060, +0.161] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 part: image [0,.2) | 142 | 121 | 0.232 | 0.345 | 0.338 | 0.373 | 0.359 | 0.408 | 0.289 | 0.331 | 0.338 | +0.106 | [+0.038, +0.167] |
| P1 part: image [.2,.5) | 358 | 242 | 0.321 | 0.380 | 0.419 | 0.444 | 0.441 | 0.464 | 0.447 | 0.419 | 0.419 | +0.098 | [+0.046, +0.152] |
| P2 part: textlike [.5,.8) | 392 | 159 | 0.533 | 0.630 | 0.656 | 0.712 | 0.671 | 0.717 | 0.717 | 0.661 | 0.658 | +0.122 | [+0.059, +0.193] |
| P2 part: textlike [.8,1] | 120 | 107 | 0.183 | 0.292 | 0.242 | 0.358 | 0.267 | 0.367 | 0.358 | 0.267 | 0.258 | +0.058 | [+0.009, +0.110] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| image in [.5,.8)+[.8,1] | 1346 | 279 | 0.779 | 0.752 | 0.815 | 0.797 | 0.800 | 0.807 | 0.789 | 0.816 | 0.811 | +0.036 | [+0.012, +0.061] |
| textlike in [0,.2)+[.2,.5) | 5007 | 837 | 0.880 | 0.893 | 0.880 | 0.891 | 0.879 | 0.890 | 0.893 | 0.881 | 0.882 | +0.000 | [-0.008, +0.007] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 500 | 363 | 0.296 | 0.370 | 0.396 | 0.424 | 0.418 | 0.448 | 0.402 | 0.394 | 0.396 | +0.022 | [+0.004, +0.040] |
| P2 textlike in [.5,.8)+[.8,1] | 512 | 266 | 0.451 | 0.551 | 0.559 | 0.629 | 0.576 | 0.635 | 0.633 | 0.568 | 0.564 | +0.018 | [+0.006, +0.031] |
| P1 part: image [0,.2) | 142 | 121 | 0.232 | 0.345 | 0.338 | 0.373 | 0.359 | 0.408 | 0.289 | 0.331 | 0.338 | +0.021 | [-0.014, +0.061] |
| P1 part: image [.2,.5) | 358 | 242 | 0.321 | 0.380 | 0.419 | 0.444 | 0.441 | 0.464 | 0.447 | 0.419 | 0.419 | +0.022 | [+0.003, +0.043] |
| P2 part: textlike [.5,.8) | 392 | 159 | 0.533 | 0.630 | 0.656 | 0.712 | 0.671 | 0.717 | 0.717 | 0.661 | 0.658 | +0.015 | [+0.005, +0.028] |
| P2 part: textlike [.8,1] | 120 | 107 | 0.183 | 0.292 | 0.242 | 0.358 | 0.267 | 0.367 | 0.358 | 0.267 | 0.258 | +0.025 | [-0.009, +0.063] |
| image in [.5,.8)+[.8,1] | 1346 | 279 | 0.779 | 0.752 | 0.815 | 0.797 | 0.800 | 0.807 | 0.789 | 0.816 | 0.811 | -0.015 | [-0.030, -0.001] |
| textlike in [0,.2)+[.2,.5) | 5007 | 837 | 0.880 | 0.893 | 0.880 | 0.891 | 0.879 | 0.890 | 0.893 | 0.881 | 0.882 | -0.001 | [-0.006, +0.003] |
| all [0,.2) | 4157 | 555 | 0.885 | 0.892 | 0.883 | 0.890 | 0.879 | 0.889 | 0.888 | 0.884 | 0.884 | -0.004 | [-0.008, +0.001] |
| all [.2,.5) | 1357 | 284 | 0.650 | 0.704 | 0.694 | 0.723 | 0.709 | 0.730 | 0.726 | 0.692 | 0.697 | +0.015 | [+0.008, +0.022] |
| all [.5,.8) | 865 | 165 | 0.642 | 0.682 | 0.712 | 0.735 | 0.726 | 0.749 | 0.733 | 0.716 | 0.716 | +0.014 | [+0.005, +0.023] |
| all [.8,1] | 993 | 168 | 0.729 | 0.709 | 0.772 | 0.764 | 0.749 | 0.768 | 0.757 | 0.776 | 0.767 | -0.023 | [-0.044, -0.005] |
| image [0,.2) | 142 | 121 | 0.232 | 0.345 | 0.338 | 0.373 | 0.359 | 0.408 | 0.289 | 0.331 | 0.338 | +0.021 | [-0.014, +0.061] |
| image [.2,.5) | 358 | 242 | 0.321 | 0.380 | 0.419 | 0.444 | 0.441 | 0.464 | 0.447 | 0.419 | 0.419 | +0.022 | [+0.003, +0.042] |
| image [.5,.8) | 473 | 140 | 0.732 | 0.725 | 0.759 | 0.755 | 0.772 | 0.776 | 0.746 | 0.761 | 0.763 | +0.013 | [+0.002, +0.025] |
| image [.8,1] | 873 | 139 | 0.804 | 0.766 | 0.845 | 0.820 | 0.816 | 0.824 | 0.812 | 0.847 | 0.837 | -0.030 | [-0.054, -0.009] |
| textlike [0,.2) | 4011 | 555 | 0.909 | 0.911 | 0.902 | 0.908 | 0.898 | 0.906 | 0.909 | 0.904 | 0.904 | -0.004 | [-0.010, +0.001] |
| textlike [.2,.5) | 996 | 282 | 0.767 | 0.819 | 0.792 | 0.822 | 0.804 | 0.824 | 0.825 | 0.789 | 0.796 | +0.012 | [+0.003, +0.020] |
| textlike [.5,.8) | 392 | 159 | 0.533 | 0.630 | 0.656 | 0.712 | 0.671 | 0.717 | 0.717 | 0.661 | 0.658 | +0.015 | [+0.005, +0.029] |
| textlike [.8,1] | 120 | 107 | 0.183 | 0.292 | 0.242 | 0.358 | 0.267 | 0.367 | 0.358 | 0.267 | 0.258 | +0.025 | [-0.008, +0.062] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.792 | 0.296 | 0.451 | 0.779 | 0.880 | -0.021 [-0.029, -0.012] | -0.100 [-0.142, -0.060] | -0.107 [-0.161, -0.060] | -0.036 [-0.061, -0.012] | +0.000 [-0.007, +0.008] | -0.107 |
| ac | ref | 1.00 | 0.808 | 0.370 | 0.551 | 0.752 | 0.893 | -0.005 [-0.018, +0.006] | -0.026 [-0.074, +0.017] | -0.008 [-0.055, +0.041] | -0.063 [-0.114, -0.021] | +0.013 [+0.005, +0.021] | -0.063 |
| c | ref | 3.70 | 0.813 | 0.396 | 0.559 | 0.815 | 0.880 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| cc | ref | 3.70 | 0.824 | 0.424 | 0.629 | 0.797 | 0.891 | +0.011 [+0.005, +0.017] | +0.028 [+0.000, +0.057] | +0.070 [+0.043, +0.100] | -0.018 [-0.037, +0.000] | +0.011 [+0.005, +0.016] | -0.018 |
| d | ref | 7.53 | 0.812 | 0.418 | 0.576 | 0.800 | 0.879 | -0.001 [-0.005, +0.003] | +0.022 [+0.004, +0.040] | +0.018 [+0.006, +0.031] | -0.015 [-0.030, -0.001] | -0.001 [-0.006, +0.003] | -0.015 |
| dc | ref | 7.53 | 0.827 | 0.448 | 0.635 | 0.807 | 0.890 | +0.014 [+0.009, +0.019] | +0.052 [+0.022, +0.084] | +0.076 [+0.050, +0.105] | -0.008 [-0.024, +0.006] | +0.010 [+0.004, +0.015] | -0.008 |
| tb2c | F5 | 1.99 | 0.822 | 0.402 | 0.633 | 0.789 | 0.893 | +0.009 [+0.002, +0.016] | +0.006 [-0.033, +0.044] | +0.074 [+0.043, +0.110] | -0.026 [-0.047, -0.008] | +0.012 [+0.005, +0.020] | -0.026 |
| tbc | F5 | 3.70 | 0.814 | 0.394 | 0.568 | 0.816 | 0.881 | +0.001 [-0.001, +0.003] | -0.002 [-0.012, +0.008] | +0.010 [+0.002, +0.020] | +0.001 [-0.005, +0.008] | +0.000 [-0.001, +0.002] | -0.002 |
| cs | ref | 3.97 | 0.814 | 0.396 | 0.564 | 0.811 | 0.882 | +0.001 [-0.001, +0.003] | +0.000 [-0.008, +0.008] | +0.006 [-0.002, +0.016] | -0.004 [-0.011, +0.004] | +0.002 [-0.000, +0.004] | -0.004 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.676 | 0.186 | 0.320 | 0.635 | 0.773 |
| ac | 0.690 | 0.214 | 0.414 | 0.626 | 0.784 |
| c | 0.700 | 0.292 | 0.426 | 0.704 | 0.768 |
| cc | 0.710 | 0.322 | 0.479 | 0.703 | 0.774 |
| d | 0.699 | 0.310 | 0.447 | 0.695 | 0.764 |
| dc | 0.710 | 0.324 | 0.480 | 0.708 | 0.773 |
| tb2c | 0.706 | 0.300 | 0.463 | 0.675 | 0.779 |
| tbc | 0.700 | 0.292 | 0.439 | 0.705 | 0.766 |
| cs | 0.703 | 0.294 | 0.434 | 0.712 | 0.768 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.823 | 0.356 | 0.496 | 0.816 | 0.904 |
| ac | 0.838 | 0.428 | 0.605 | 0.798 | 0.913 |
| c | 0.837 | 0.450 | 0.600 | 0.844 | 0.897 |
| cc | 0.853 | 0.478 | 0.670 | 0.830 | 0.916 |
| d | 0.838 | 0.462 | 0.611 | 0.829 | 0.901 |
| dc | 0.855 | 0.496 | 0.668 | 0.840 | 0.914 |
| tb2c | 0.851 | 0.462 | 0.664 | 0.823 | 0.916 |
| tbc | 0.838 | 0.456 | 0.607 | 0.844 | 0.899 |
| cs | 0.838 | 0.454 | 0.598 | 0.848 | 0.899 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.020 [-0.029, -0.011] | -0.122 [-0.169, -0.082] | -0.125 [-0.178, -0.079] | -0.022 [-0.046, +0.004] | +0.001 [-0.007, +0.009] |
| ac | -0.005 [-0.016, +0.006] | -0.048 [-0.096, -0.002] | -0.025 [-0.074, +0.021] | -0.048 [-0.094, -0.006] | +0.014 [+0.005, +0.023] |
| c | +0.001 [-0.003, +0.005] | -0.022 [-0.040, -0.004] | -0.018 [-0.031, -0.006] | +0.015 [+0.001, +0.030] | +0.001 [-0.003, +0.006] |
| cc | +0.012 [+0.006, +0.017] | +0.006 [-0.022, +0.037] | +0.053 [+0.029, +0.078] | -0.003 [-0.021, +0.015] | +0.012 [+0.007, +0.017] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| dc | +0.015 [+0.011, +0.019] | +0.030 [+0.002, +0.060] | +0.059 [+0.035, +0.085] | +0.007 [-0.002, +0.017] | +0.011 [+0.007, +0.015] |
| tb2c | +0.010 [+0.002, +0.018] | -0.016 [-0.053, +0.022] | +0.057 [+0.029, +0.086] | -0.011 [-0.033, +0.011] | +0.014 [+0.006, +0.021] |
| tbc | +0.002 [-0.002, +0.006] | -0.024 [-0.040, -0.009] | -0.008 [-0.018, +0.002] | +0.016 [+0.003, +0.032] | +0.002 [-0.003, +0.006] |
| cs | +0.002 [-0.002, +0.006] | -0.022 [-0.040, -0.006] | -0.012 [-0.023, +0.000] | +0.011 [-0.001, +0.024] | +0.003 [-0.001, +0.008] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.035 [-0.043, -0.026] | -0.152 [-0.199, -0.105] | -0.184 [-0.242, -0.135] | -0.028 [-0.053, +0.000] | -0.010 [-0.018, -0.002] |
| ac | -0.019 [-0.031, -0.009] | -0.078 [-0.120, -0.039] | -0.084 [-0.133, -0.044] | -0.055 [-0.103, -0.014] | +0.003 [-0.004, +0.011] |
| c | -0.014 [-0.019, -0.009] | -0.052 [-0.084, -0.022] | -0.076 [-0.105, -0.050] | +0.008 [-0.006, +0.024] | -0.010 [-0.015, -0.004] |
| cc | -0.003 [-0.007, +0.001] | -0.024 [-0.045, -0.004] | -0.006 [-0.017, +0.004] | -0.010 [-0.024, +0.004] | +0.001 [-0.002, +0.005] |
| d | -0.015 [-0.019, -0.011] | -0.030 [-0.060, -0.002] | -0.059 [-0.085, -0.035] | -0.007 [-0.017, +0.002] | -0.011 [-0.015, -0.007] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| tb2c | -0.005 [-0.012, +0.002] | -0.046 [-0.076, -0.018] | -0.002 [-0.025, +0.019] | -0.018 [-0.038, +0.005] | +0.003 [-0.003, +0.009] |
| tbc | -0.013 [-0.018, -0.008] | -0.054 [-0.084, -0.026] | -0.066 [-0.094, -0.042] | +0.010 [-0.006, +0.026] | -0.009 [-0.014, -0.004] |
| cs | -0.013 [-0.018, -0.008] | -0.052 [-0.084, -0.022] | -0.070 [-0.098, -0.045] | +0.004 [-0.009, +0.018] | -0.008 [-0.013, -0.003] |

### Session 9 selection rule applied to the eval queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F5 | tbc | 3.70 | -0.002 | -0.002 | +0.010 | +0.001 | +0.000 |

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.437 | 0.762 | 0.736 | 0.498 |
| centered | 0.139 | 0.524 | 0.470 | 0.149 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2c | 1.99 | 0.912 | 738 |
| tbc | 3.70 | 0.985 | 738 |

### Session 9 hypotheses on the eval queries

H9c, c - tbc (type-blind k-means at c's budget, uncentered): P1 image in [0,.2)+[.2,.5) +0.002 [-0.008, +0.012]; P2 textlike in [.5,.8)+[.8,1] -0.010 [-0.020, -0.002]; interval includes zero in a primary cell: yes, H9c dead.

## Session 19 commit-subject queries, E1 (jina-embeddings-v4, cache jina-embeddings-v4_s19)

Queries: 1162 over 522 directories and 440 owners; 1595 directories ranked (random recall@5 = 0.0031); 0 queries dropped because their directory has no embedded file. Representations use all embedded files of a directory (the query is not a file). Calibration seed 20261104 gives the text mean for the centered rows.

### recall@1

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.145 | 0.130 | 0.174 | 0.153 | 0.185 | 0.169 | 0.056 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.148 | 0.131 | 0.175 | 0.150 | 0.184 | 0.166 | 0.058 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.115 | 0.123 | 0.164 | 0.180 | 0.197 | 0.189 | 0.041 |

### recall@5

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.265 | 0.250 | 0.294 | 0.279 | 0.316 | 0.293 | 0.096 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.273 | 0.257 | 0.303 | 0.281 | 0.323 | 0.295 | 0.099 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.197 | 0.197 | 0.221 | 0.262 | 0.254 | 0.270 | 0.066 |

### recall@10

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.327 | 0.303 | 0.354 | 0.331 | 0.382 | 0.349 | 0.132 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.340 | 0.313 | 0.363 | 0.335 | 0.393 | 0.355 | 0.136 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.213 | 0.213 | 0.270 | 0.303 | 0.287 | 0.303 | 0.098 |

### Differences in recall@5: point, owner-clustered 95% interval

| cell | subset | queries | c - a | d - c | ac - a | cc - c |
|---|---|---:|---|---|---|---|
| all | all | 1162 | +0.029 [+0.010, +0.050] | +0.022 [+0.005, +0.036] | -0.015 [-0.032, +0.003] | -0.015 [-0.033, +0.003] |
| all | names miss | 1051 | +0.027 [+0.008, +0.045] | +0.022 [+0.007, +0.038] | -0.015 [-0.032, +0.003] | -0.012 [-0.031, +0.007] |
| text-heavy [0,.2)+[.2,.5) | all | 1040 | +0.030 [+0.008, +0.050] | +0.020 [+0.004, +0.036] | -0.016 [-0.035, +0.001] | -0.022 [-0.043, -0.004] |
| text-heavy [0,.2)+[.2,.5) | names miss | 937 | +0.027 [+0.005, +0.048] | +0.020 [+0.002, +0.038] | -0.018 [-0.037, +0.002] | -0.019 [-0.039, +0.002] |
| image-heavy [.5,.8)+[.8,1] | all | 122 | +0.025 [-0.036, +0.083] | +0.033 [+0.008, +0.064] | +0.000 [-0.039, +0.037] | +0.041 [+0.000, +0.085] |
| image-heavy [.5,.8)+[.8,1] | names miss | 114 | +0.026 [-0.038, +0.082] | +0.035 [+0.008, +0.068] | +0.009 [-0.029, +0.049] | +0.044 [+0.000, +0.095] |

H19d statistic (E1): image-heavy directories, 122 queries from 66 owners; gate, recall@5 of d 0.254 (needs 0.10 and more than names alone, 0.066): passed; owner-weighted c - a +0.010 [-0.061, +0.078]; H19d: inconclusive (fewer than 100 owners).

## E4: embedding

```
files 12656; ok 12049; not ok by modality {'image': 466, 'other': 130, 'text': 10, 'table': 1}
  longest text input 8192 tokens (limit 8192)
```

## E4: eval.py

Model: nomic-embed-v1.5. Queries: 7372 over 1172 directories; 1600 directories ranked (random recall@k = k/1600). Queries dropped for lack of a vector: 236 {'image': 107, 'other': 128, 'table': 1}. Queries in calibration directories, not used: 1717.

Mean representative vectors per directory: a 1.00, ac 1.00, c 3.70, cc 3.70, d 7.53, dc 7.53, tb2c 1.99, tbc 3.70, cs 3.97.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 7372 | 1172 | a | 0.513 | 0.586 | 0.612 | 0.640 | [0.587, 0.640] |
| all | 7372 | 1172 | ac | 0.573 | 0.667 | 0.696 | 0.736 | [0.675, 0.717] |
| all | 7372 | 1172 | c | 0.614 | 0.693 | 0.721 | 0.754 | [0.701, 0.741] |
| all | 7372 | 1172 | cc | 0.620 | 0.705 | 0.733 | 0.767 | [0.713, 0.752] |
| all | 7372 | 1172 | d | 0.612 | 0.703 | 0.729 | 0.762 | [0.708, 0.749] |
| all | 7372 | 1172 | dc | 0.621 | 0.708 | 0.737 | 0.773 | [0.717, 0.755] |
| all | 7372 | 1172 | tb2c | 0.614 | 0.702 | 0.730 | 0.763 | [0.711, 0.749] |
| all | 7372 | 1172 | tbc | 0.613 | 0.693 | 0.719 | 0.754 | [0.699, 0.738] |
| all | 7372 | 1172 | cs | 0.616 | 0.697 | 0.722 | 0.757 | [0.702, 0.742] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 4157 | 555 | a | 0.726 | 0.803 | 0.821 | 0.846 | [0.799, 0.841] |
| [0,.2) | 4157 | 555 | ac | 0.726 | 0.805 | 0.823 | 0.849 | [0.800, 0.843] |
| [0,.2) | 4157 | 555 | c | 0.712 | 0.791 | 0.814 | 0.841 | [0.791, 0.836] |
| [0,.2) | 4157 | 555 | cc | 0.712 | 0.796 | 0.820 | 0.847 | [0.796, 0.840] |
| [0,.2) | 4157 | 555 | d | 0.707 | 0.797 | 0.821 | 0.848 | [0.797, 0.841] |
| [0,.2) | 4157 | 555 | dc | 0.715 | 0.797 | 0.823 | 0.851 | [0.800, 0.843] |
| [0,.2) | 4157 | 555 | tb2c | 0.715 | 0.802 | 0.825 | 0.852 | [0.801, 0.845] |
| [0,.2) | 4157 | 555 | tbc | 0.713 | 0.792 | 0.815 | 0.843 | [0.792, 0.836] |
| [0,.2) | 4157 | 555 | cs | 0.711 | 0.793 | 0.815 | 0.843 | [0.791, 0.836] |
| [.2,.5) | 1357 | 284 | a | 0.172 | 0.241 | 0.265 | 0.291 | [0.219, 0.313] |
| [.2,.5) | 1357 | 284 | ac | 0.380 | 0.491 | 0.526 | 0.564 | [0.489, 0.562] |
| [.2,.5) | 1357 | 284 | c | 0.439 | 0.517 | 0.547 | 0.592 | [0.498, 0.591] |
| [.2,.5) | 1357 | 284 | cc | 0.472 | 0.562 | 0.593 | 0.628 | [0.551, 0.633] |
| [.2,.5) | 1357 | 284 | d | 0.455 | 0.547 | 0.579 | 0.615 | [0.534, 0.623] |
| [.2,.5) | 1357 | 284 | dc | 0.465 | 0.560 | 0.590 | 0.630 | [0.544, 0.634] |
| [.2,.5) | 1357 | 284 | tb2c | 0.461 | 0.542 | 0.574 | 0.612 | [0.533, 0.611] |
| [.2,.5) | 1357 | 284 | tbc | 0.434 | 0.515 | 0.548 | 0.599 | [0.497, 0.595] |
| [.2,.5) | 1357 | 284 | cs | 0.444 | 0.520 | 0.555 | 0.597 | [0.504, 0.602] |
| [.5,.8) | 865 | 165 | a | 0.060 | 0.073 | 0.084 | 0.108 | [0.033, 0.142] |
| [.5,.8) | 865 | 165 | ac | 0.240 | 0.380 | 0.427 | 0.511 | [0.373, 0.477] |
| [.5,.8) | 865 | 165 | c | 0.466 | 0.542 | 0.582 | 0.622 | [0.508, 0.646] |
| [.5,.8) | 865 | 165 | cc | 0.474 | 0.572 | 0.605 | 0.657 | [0.536, 0.668] |
| [.5,.8) | 865 | 165 | d | 0.475 | 0.564 | 0.592 | 0.637 | [0.522, 0.655] |
| [.5,.8) | 865 | 165 | dc | 0.479 | 0.578 | 0.608 | 0.660 | [0.536, 0.669] |
| [.5,.8) | 865 | 165 | tb2c | 0.462 | 0.557 | 0.587 | 0.624 | [0.517, 0.655] |
| [.5,.8) | 865 | 165 | tbc | 0.461 | 0.539 | 0.571 | 0.607 | [0.501, 0.634] |
| [.5,.8) | 865 | 165 | cs | 0.467 | 0.549 | 0.580 | 0.621 | [0.508, 0.645] |
| [.8,1] | 993 | 168 | a | 0.479 | 0.596 | 0.675 | 0.717 | [0.627, 0.717] |
| [.8,1] | 993 | 168 | ac | 0.483 | 0.580 | 0.630 | 0.695 | [0.569, 0.692] |
| [.8,1] | 993 | 168 | c | 0.574 | 0.659 | 0.689 | 0.731 | [0.638, 0.733] |
| [.8,1] | 993 | 168 | cc | 0.561 | 0.636 | 0.674 | 0.721 | [0.619, 0.720] |
| [.8,1] | 993 | 168 | d | 0.550 | 0.641 | 0.670 | 0.711 | [0.616, 0.718] |
| [.8,1] | 993 | 168 | dc | 0.567 | 0.649 | 0.687 | 0.737 | [0.635, 0.730] |
| [.8,1] | 993 | 168 | tb2c | 0.531 | 0.630 | 0.672 | 0.717 | [0.618, 0.718] |
| [.8,1] | 993 | 168 | tbc | 0.572 | 0.659 | 0.683 | 0.725 | [0.633, 0.729] |
| [.8,1] | 993 | 168 | cs | 0.585 | 0.667 | 0.688 | 0.729 | [0.638, 0.731] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 1846 | 642 | a | 0.280 | 0.347 | 0.393 | 0.421 | [0.333, 0.445] |
| image | 1846 | 642 | ac | 0.336 | 0.426 | 0.468 | 0.531 | [0.417, 0.514] |
| image | 1846 | 642 | c | 0.479 | 0.557 | 0.587 | 0.626 | [0.543, 0.628] |
| image | 1846 | 642 | cc | 0.479 | 0.550 | 0.582 | 0.625 | [0.539, 0.621] |
| image | 1846 | 642 | d | 0.470 | 0.555 | 0.579 | 0.614 | [0.535, 0.620] |
| image | 1846 | 642 | dc | 0.483 | 0.562 | 0.594 | 0.640 | [0.550, 0.636] |
| image | 1846 | 642 | tb2c | 0.438 | 0.524 | 0.561 | 0.603 | [0.516, 0.600] |
| image | 1846 | 642 | tbc | 0.474 | 0.553 | 0.580 | 0.621 | [0.536, 0.621] |
| image | 1846 | 642 | cs | 0.486 | 0.564 | 0.586 | 0.622 | [0.543, 0.626] |
| pdf_text | 148 | 37 | a | 0.480 | 0.507 | 0.514 | 0.514 | [0.257, 0.759] |
| pdf_text | 148 | 37 | ac | 0.703 | 0.845 | 0.872 | 0.885 | [0.732, 0.945] |
| pdf_text | 148 | 37 | c | 0.824 | 0.905 | 0.912 | 0.919 | [0.803, 0.971] |
| pdf_text | 148 | 37 | cc | 0.851 | 0.912 | 0.926 | 0.932 | [0.837, 0.971] |
| pdf_text | 148 | 37 | d | 0.831 | 0.912 | 0.912 | 0.932 | [0.803, 0.971] |
| pdf_text | 148 | 37 | dc | 0.838 | 0.912 | 0.912 | 0.926 | [0.803, 0.971] |
| pdf_text | 148 | 37 | tb2c | 0.838 | 0.912 | 0.912 | 0.919 | [0.803, 0.971] |
| pdf_text | 148 | 37 | tbc | 0.838 | 0.905 | 0.919 | 0.919 | [0.821, 0.971] |
| pdf_text | 148 | 37 | cs | 0.824 | 0.905 | 0.912 | 0.919 | [0.808, 0.967] |
| text | 5273 | 1078 | a | 0.595 | 0.672 | 0.693 | 0.720 | [0.662, 0.720] |
| text | 5273 | 1078 | ac | 0.652 | 0.747 | 0.771 | 0.803 | [0.749, 0.792] |
| text | 5273 | 1078 | c | 0.654 | 0.734 | 0.761 | 0.794 | [0.737, 0.782] |
| text | 5273 | 1078 | cc | 0.660 | 0.752 | 0.779 | 0.812 | [0.757, 0.798] |
| text | 5273 | 1078 | d | 0.654 | 0.747 | 0.775 | 0.807 | [0.751, 0.796] |
| text | 5273 | 1078 | dc | 0.662 | 0.752 | 0.780 | 0.814 | [0.757, 0.800] |
| text | 5273 | 1078 | tb2c | 0.668 | 0.758 | 0.784 | 0.814 | [0.762, 0.803] |
| text | 5273 | 1078 | tbc | 0.654 | 0.735 | 0.761 | 0.795 | [0.736, 0.782] |
| text | 5273 | 1078 | cs | 0.654 | 0.736 | 0.764 | 0.798 | [0.739, 0.784] |
| table | 77 | 34 | a | 0.519 | 0.558 | 0.571 | 0.597 | [0.220, 0.764] |
| table | 77 | 34 | ac | 0.519 | 0.584 | 0.636 | 0.740 | [0.346, 0.810] |
| table | 77 | 34 | c | 0.662 | 0.701 | 0.740 | 0.779 | [0.526, 0.878] |
| table | 77 | 34 | cc | 0.662 | 0.753 | 0.792 | 0.805 | [0.605, 0.903] |
| table | 77 | 34 | d | 0.688 | 0.753 | 0.766 | 0.792 | [0.558, 0.893] |
| table | 77 | 34 | dc | 0.649 | 0.740 | 0.792 | 0.818 | [0.605, 0.903] |
| table | 77 | 34 | tb2c | 0.610 | 0.662 | 0.688 | 0.714 | [0.417, 0.843] |
| table | 77 | 34 | tbc | 0.636 | 0.701 | 0.740 | 0.779 | [0.526, 0.878] |
| table | 77 | 34 | cs | 0.662 | 0.714 | 0.740 | 0.779 | [0.526, 0.878] |
| other | 21 | 9 | a | 0.762 | 0.762 | 0.810 | 0.857 | [0.222, 0.965] |
| other | 21 | 9 | ac | 0.810 | 0.857 | 0.857 | 0.857 | [0.333, 0.983] |
| other | 21 | 9 | c | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | cc | 0.857 | 0.857 | 0.857 | 0.857 | [0.333, 0.983] |
| other | 21 | 9 | d | 0.857 | 0.857 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | dc | 0.857 | 0.857 | 0.857 | 0.857 | [0.333, 0.983] |
| other | 21 | 9 | tb2c | 0.857 | 0.857 | 0.857 | 0.857 | [0.333, 0.983] |
| other | 21 | 9 | tbc | 0.857 | 0.857 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | cs | 0.905 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 142 | 121 | a | 0.000 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] |
| image [0,.2) | 142 | 121 | ac | 0.000 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] |
| image [0,.2) | 142 | 121 | c | 0.063 | 0.092 | 0.099 | 0.113 | [0.037, 0.167] |
| image [0,.2) | 142 | 121 | cc | 0.070 | 0.092 | 0.113 | 0.120 | [0.044, 0.192] |
| image [0,.2) | 142 | 121 | d | 0.056 | 0.092 | 0.106 | 0.120 | [0.043, 0.177] |
| image [0,.2) | 142 | 121 | dc | 0.063 | 0.092 | 0.106 | 0.120 | [0.043, 0.177] |
| image [0,.2) | 142 | 121 | tb2c | 0.014 | 0.042 | 0.042 | 0.049 | [0.000, 0.099] |
| image [0,.2) | 142 | 121 | tbc | 0.070 | 0.099 | 0.099 | 0.113 | [0.037, 0.167] |
| image [0,.2) | 142 | 121 | cs | 0.063 | 0.099 | 0.099 | 0.113 | [0.037, 0.167] |
| image [.2,.5) | 358 | 242 | a | 0.000 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] |
| image [.2,.5) | 358 | 242 | ac | 0.034 | 0.075 | 0.084 | 0.101 | [0.035, 0.138] |
| image [.2,.5) | 358 | 242 | c | 0.187 | 0.254 | 0.277 | 0.302 | [0.203, 0.344] |
| image [.2,.5) | 358 | 242 | cc | 0.212 | 0.251 | 0.263 | 0.288 | [0.186, 0.331] |
| image [.2,.5) | 358 | 242 | d | 0.201 | 0.257 | 0.265 | 0.279 | [0.191, 0.333] |
| image [.2,.5) | 358 | 242 | dc | 0.209 | 0.251 | 0.268 | 0.302 | [0.192, 0.337] |
| image [.2,.5) | 358 | 242 | tb2c | 0.159 | 0.196 | 0.221 | 0.254 | [0.150, 0.292] |
| image [.2,.5) | 358 | 242 | tbc | 0.182 | 0.243 | 0.279 | 0.316 | [0.204, 0.352] |
| image [.2,.5) | 358 | 242 | cs | 0.193 | 0.260 | 0.279 | 0.299 | [0.203, 0.351] |
| image [.5,.8) | 473 | 140 | a | 0.093 | 0.112 | 0.125 | 0.148 | [0.033, 0.214] |
| image [.5,.8) | 473 | 140 | ac | 0.279 | 0.397 | 0.448 | 0.550 | [0.362, 0.532] |
| image [.5,.8) | 473 | 140 | c | 0.510 | 0.581 | 0.617 | 0.662 | [0.539, 0.688] |
| image [.5,.8) | 473 | 140 | cc | 0.518 | 0.605 | 0.636 | 0.693 | [0.561, 0.705] |
| image [.5,.8) | 473 | 140 | d | 0.514 | 0.607 | 0.632 | 0.677 | [0.558, 0.694] |
| image [.5,.8) | 473 | 140 | dc | 0.522 | 0.624 | 0.655 | 0.708 | [0.581, 0.719] |
| image [.5,.8) | 473 | 140 | tb2c | 0.474 | 0.573 | 0.609 | 0.653 | [0.530, 0.677] |
| image [.5,.8) | 473 | 140 | tbc | 0.495 | 0.573 | 0.603 | 0.645 | [0.527, 0.663] |
| image [.5,.8) | 473 | 140 | cs | 0.507 | 0.588 | 0.615 | 0.653 | [0.540, 0.682] |
| image [.8,1] | 873 | 139 | a | 0.542 | 0.674 | 0.763 | 0.811 | [0.717, 0.806] |
| image [.8,1] | 873 | 139 | ac | 0.545 | 0.655 | 0.712 | 0.785 | [0.644, 0.784] |
| image [.8,1] | 873 | 139 | c | 0.651 | 0.743 | 0.777 | 0.824 | [0.730, 0.821] |
| image [.8,1] | 873 | 139 | cc | 0.635 | 0.718 | 0.759 | 0.808 | [0.705, 0.809] |
| image [.8,1] | 873 | 139 | d | 0.623 | 0.724 | 0.755 | 0.798 | [0.702, 0.804] |
| image [.8,1] | 873 | 139 | dc | 0.643 | 0.732 | 0.774 | 0.827 | [0.724, 0.818] |
| image [.8,1] | 873 | 139 | tb2c | 0.601 | 0.711 | 0.758 | 0.810 | [0.708, 0.804] |
| image [.8,1] | 873 | 139 | tbc | 0.648 | 0.743 | 0.770 | 0.817 | [0.722, 0.814] |
| image [.8,1] | 873 | 139 | cs | 0.663 | 0.753 | 0.775 | 0.821 | [0.729, 0.820] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 4011 | 555 | a | 0.753 | 0.832 | 0.851 | 0.876 | [0.831, 0.869] |
| textlike [0,.2) | 4011 | 555 | ac | 0.752 | 0.834 | 0.853 | 0.880 | [0.833, 0.872] |
| textlike [0,.2) | 4011 | 555 | c | 0.735 | 0.816 | 0.840 | 0.867 | [0.818, 0.860] |
| textlike [0,.2) | 4011 | 555 | cc | 0.734 | 0.821 | 0.845 | 0.873 | [0.823, 0.864] |
| textlike [0,.2) | 4011 | 555 | d | 0.730 | 0.822 | 0.846 | 0.874 | [0.824, 0.865] |
| textlike [0,.2) | 4011 | 555 | dc | 0.738 | 0.822 | 0.848 | 0.877 | [0.826, 0.867] |
| textlike [0,.2) | 4011 | 555 | tb2c | 0.740 | 0.829 | 0.853 | 0.880 | [0.833, 0.871] |
| textlike [0,.2) | 4011 | 555 | tbc | 0.736 | 0.816 | 0.840 | 0.869 | [0.820, 0.860] |
| textlike [0,.2) | 4011 | 555 | cs | 0.733 | 0.818 | 0.840 | 0.869 | [0.819, 0.859] |
| textlike [.2,.5) | 996 | 282 | a | 0.234 | 0.328 | 0.360 | 0.397 | [0.303, 0.416] |
| textlike [.2,.5) | 996 | 282 | ac | 0.504 | 0.639 | 0.684 | 0.730 | [0.636, 0.726] |
| textlike [.2,.5) | 996 | 282 | c | 0.528 | 0.609 | 0.643 | 0.695 | [0.591, 0.692] |
| textlike [.2,.5) | 996 | 282 | cc | 0.564 | 0.672 | 0.711 | 0.749 | [0.668, 0.754] |
| textlike [.2,.5) | 996 | 282 | d | 0.544 | 0.650 | 0.691 | 0.734 | [0.642, 0.740] |
| textlike [.2,.5) | 996 | 282 | dc | 0.555 | 0.670 | 0.705 | 0.747 | [0.658, 0.753] |
| textlike [.2,.5) | 996 | 282 | tb2c | 0.568 | 0.666 | 0.700 | 0.739 | [0.654, 0.741] |
| textlike [.2,.5) | 996 | 282 | tbc | 0.523 | 0.611 | 0.643 | 0.700 | [0.589, 0.695] |
| textlike [.2,.5) | 996 | 282 | cs | 0.532 | 0.612 | 0.653 | 0.703 | [0.601, 0.705] |
| textlike [.5,.8) | 392 | 159 | a | 0.020 | 0.026 | 0.036 | 0.059 | [0.007, 0.078] |
| textlike [.5,.8) | 392 | 159 | ac | 0.194 | 0.360 | 0.401 | 0.464 | [0.292, 0.495] |
| textlike [.5,.8) | 392 | 159 | c | 0.413 | 0.495 | 0.538 | 0.574 | [0.438, 0.621] |
| textlike [.5,.8) | 392 | 159 | cc | 0.421 | 0.533 | 0.566 | 0.612 | [0.469, 0.648] |
| textlike [.5,.8) | 392 | 159 | d | 0.429 | 0.513 | 0.543 | 0.589 | [0.441, 0.629] |
| textlike [.5,.8) | 392 | 159 | dc | 0.426 | 0.523 | 0.551 | 0.602 | [0.450, 0.636] |
| textlike [.5,.8) | 392 | 159 | tb2c | 0.449 | 0.538 | 0.561 | 0.589 | [0.460, 0.649] |
| textlike [.5,.8) | 392 | 159 | tbc | 0.421 | 0.497 | 0.533 | 0.561 | [0.435, 0.615] |
| textlike [.5,.8) | 392 | 159 | cs | 0.418 | 0.503 | 0.538 | 0.582 | [0.438, 0.619] |
| textlike [.8,1] | 120 | 107 | a | 0.025 | 0.033 | 0.033 | 0.033 | [0.000, 0.120] |
| textlike [.8,1] | 120 | 107 | ac | 0.033 | 0.033 | 0.033 | 0.042 | [0.000, 0.120] |
| textlike [.8,1] | 120 | 107 | c | 0.017 | 0.042 | 0.050 | 0.058 | [0.000, 0.137] |
| textlike [.8,1] | 120 | 107 | cc | 0.025 | 0.042 | 0.050 | 0.092 | [0.000, 0.137] |
| textlike [.8,1] | 120 | 107 | d | 0.017 | 0.042 | 0.050 | 0.075 | [0.000, 0.137] |
| textlike [.8,1] | 120 | 107 | dc | 0.017 | 0.042 | 0.050 | 0.083 | [0.000, 0.137] |
| textlike [.8,1] | 120 | 107 | tb2c | 0.017 | 0.042 | 0.042 | 0.042 | [0.000, 0.127] |
| textlike [.8,1] | 120 | 107 | tbc | 0.017 | 0.042 | 0.050 | 0.058 | [0.000, 0.137] |
| textlike [.8,1] | 120 | 107 | cs | 0.017 | 0.042 | 0.050 | 0.058 | [0.000, 0.137] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 500 | 363 | 0.000 | 0.060 | 0.226 | 0.220 | 0.220 | 0.222 | 0.170 | 0.228 | 0.228 | +0.226 | [+0.173, +0.281] |
| P2 textlike in [.5,.8)+[.8,1] | 512 | 266 | 0.035 | 0.314 | 0.424 | 0.445 | 0.428 | 0.434 | 0.439 | 0.420 | 0.424 | +0.389 | [+0.297, +0.471] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 part: image [0,.2) | 142 | 121 | 0.000 | 0.000 | 0.099 | 0.113 | 0.106 | 0.106 | 0.042 | 0.099 | 0.099 | +0.099 | [+0.037, +0.167] |
| P1 part: image [.2,.5) | 358 | 242 | 0.000 | 0.084 | 0.277 | 0.263 | 0.265 | 0.268 | 0.221 | 0.279 | 0.279 | +0.277 | [+0.208, +0.346] |
| P2 part: textlike [.5,.8) | 392 | 159 | 0.036 | 0.401 | 0.538 | 0.566 | 0.543 | 0.551 | 0.561 | 0.533 | 0.538 | +0.503 | [+0.388, +0.596] |
| P2 part: textlike [.8,1] | 120 | 107 | 0.033 | 0.033 | 0.050 | 0.050 | 0.050 | 0.050 | 0.042 | 0.050 | 0.050 | +0.017 | [+0.000, +0.062] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| image in [.5,.8)+[.8,1] | 1346 | 279 | 0.539 | 0.620 | 0.721 | 0.716 | 0.712 | 0.733 | 0.706 | 0.711 | 0.719 | +0.182 | [+0.130, +0.238] |
| textlike in [0,.2)+[.2,.5) | 5007 | 837 | 0.753 | 0.819 | 0.800 | 0.818 | 0.815 | 0.820 | 0.822 | 0.801 | 0.803 | +0.047 | [+0.034, +0.062] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 500 | 363 | 0.000 | 0.060 | 0.226 | 0.220 | 0.220 | 0.222 | 0.170 | 0.228 | 0.228 | -0.006 | [-0.022, +0.006] |
| P2 textlike in [.5,.8)+[.8,1] | 512 | 266 | 0.035 | 0.314 | 0.424 | 0.445 | 0.428 | 0.434 | 0.439 | 0.420 | 0.424 | +0.004 | [-0.012, +0.019] |
| P1 part: image [0,.2) | 142 | 121 | 0.000 | 0.000 | 0.099 | 0.113 | 0.106 | 0.106 | 0.042 | 0.099 | 0.099 | +0.007 | [+0.000, +0.022] |
| P1 part: image [.2,.5) | 358 | 242 | 0.000 | 0.084 | 0.277 | 0.263 | 0.265 | 0.268 | 0.221 | 0.279 | 0.279 | -0.011 | [-0.031, +0.003] |
| P2 part: textlike [.5,.8) | 392 | 159 | 0.036 | 0.401 | 0.538 | 0.566 | 0.543 | 0.551 | 0.561 | 0.533 | 0.538 | +0.005 | [-0.013, +0.024] |
| P2 part: textlike [.8,1] | 120 | 107 | 0.033 | 0.033 | 0.050 | 0.050 | 0.050 | 0.050 | 0.042 | 0.050 | 0.050 | +0.000 | [+0.000, +0.000] |
| image in [.5,.8)+[.8,1] | 1346 | 279 | 0.539 | 0.620 | 0.721 | 0.716 | 0.712 | 0.733 | 0.706 | 0.711 | 0.719 | -0.009 | [-0.024, +0.006] |
| textlike in [0,.2)+[.2,.5) | 5007 | 837 | 0.753 | 0.819 | 0.800 | 0.818 | 0.815 | 0.820 | 0.822 | 0.801 | 0.803 | +0.015 | [+0.008, +0.022] |
| all [0,.2) | 4157 | 555 | 0.821 | 0.823 | 0.814 | 0.820 | 0.821 | 0.823 | 0.825 | 0.815 | 0.815 | +0.006 | [-0.000, +0.013] |
| all [.2,.5) | 1357 | 284 | 0.265 | 0.526 | 0.547 | 0.593 | 0.579 | 0.590 | 0.574 | 0.548 | 0.555 | +0.032 | [+0.018, +0.048] |
| all [.5,.8) | 865 | 165 | 0.084 | 0.427 | 0.582 | 0.605 | 0.592 | 0.608 | 0.587 | 0.571 | 0.580 | +0.010 | [-0.004, +0.024] |
| all [.8,1] | 993 | 168 | 0.675 | 0.630 | 0.689 | 0.674 | 0.670 | 0.687 | 0.672 | 0.683 | 0.688 | -0.019 | [-0.035, -0.002] |
| image [0,.2) | 142 | 121 | 0.000 | 0.000 | 0.099 | 0.113 | 0.106 | 0.106 | 0.042 | 0.099 | 0.099 | +0.007 | [+0.000, +0.022] |
| image [.2,.5) | 358 | 242 | 0.000 | 0.084 | 0.277 | 0.263 | 0.265 | 0.268 | 0.221 | 0.279 | 0.279 | -0.011 | [-0.030, +0.003] |
| image [.5,.8) | 473 | 140 | 0.125 | 0.448 | 0.617 | 0.636 | 0.632 | 0.655 | 0.609 | 0.603 | 0.615 | +0.015 | [-0.006, +0.038] |
| image [.8,1] | 873 | 139 | 0.763 | 0.712 | 0.777 | 0.759 | 0.755 | 0.774 | 0.758 | 0.770 | 0.775 | -0.022 | [-0.041, -0.001] |
| textlike [0,.2) | 4011 | 555 | 0.851 | 0.853 | 0.840 | 0.845 | 0.846 | 0.848 | 0.853 | 0.840 | 0.840 | +0.006 | [-0.001, +0.013] |
| textlike [.2,.5) | 996 | 282 | 0.360 | 0.684 | 0.643 | 0.711 | 0.691 | 0.705 | 0.700 | 0.643 | 0.653 | +0.048 | [+0.031, +0.068] |
| textlike [.5,.8) | 392 | 159 | 0.036 | 0.401 | 0.538 | 0.566 | 0.543 | 0.551 | 0.561 | 0.533 | 0.538 | +0.005 | [-0.014, +0.023] |
| textlike [.8,1] | 120 | 107 | 0.033 | 0.033 | 0.050 | 0.050 | 0.050 | 0.050 | 0.042 | 0.050 | 0.050 | +0.000 | [+0.000, +0.000] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.612 | 0.000 | 0.035 | 0.539 | 0.753 | -0.109 [-0.129, -0.087] | -0.226 [-0.281, -0.173] | -0.389 [-0.471, -0.297] | -0.182 [-0.238, -0.130] | -0.047 [-0.062, -0.034] | -0.389 |
| ac | ref | 1.00 | 0.696 | 0.060 | 0.314 | 0.620 | 0.819 | -0.025 [-0.039, -0.012] | -0.166 [-0.212, -0.118] | -0.109 [-0.159, -0.063] | -0.101 [-0.153, -0.051] | +0.019 [+0.009, +0.030] | -0.166 |
| c | ref | 3.70 | 0.721 | 0.226 | 0.424 | 0.721 | 0.800 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| cc | ref | 3.70 | 0.733 | 0.220 | 0.445 | 0.716 | 0.818 | +0.012 [+0.004, +0.019] | -0.006 [-0.025, +0.008] | +0.021 [+0.000, +0.045] | -0.004 [-0.021, +0.014] | +0.018 [+0.008, +0.027] | -0.006 |
| d | ref | 7.53 | 0.729 | 0.220 | 0.428 | 0.712 | 0.815 | +0.008 [+0.002, +0.014] | -0.006 [-0.022, +0.006] | +0.004 [-0.012, +0.019] | -0.009 [-0.024, +0.006] | +0.015 [+0.008, +0.022] | -0.009 |
| dc | ref | 7.53 | 0.737 | 0.222 | 0.434 | 0.733 | 0.820 | +0.016 [+0.009, +0.022] | -0.004 [-0.018, +0.008] | +0.010 [-0.006, +0.026] | +0.012 [-0.004, +0.029] | +0.019 [+0.012, +0.028] | -0.004 |
| tb2c | F5 | 1.99 | 0.730 | 0.170 | 0.439 | 0.706 | 0.822 | +0.009 [+0.001, +0.017] | -0.056 [-0.090, -0.024] | +0.016 [-0.004, +0.036] | -0.015 [-0.035, +0.007] | +0.022 [+0.012, +0.031] | -0.056 |
| tbc | F5 | 3.70 | 0.719 | 0.228 | 0.420 | 0.711 | 0.801 | -0.001 [-0.005, +0.002] | +0.002 [-0.014, +0.022] | -0.004 [-0.015, +0.006] | -0.010 [-0.020, +0.000] | +0.001 [-0.002, +0.004] | -0.010 |
| cs | ref | 3.97 | 0.722 | 0.228 | 0.424 | 0.719 | 0.803 | +0.001 [-0.001, +0.004] | +0.002 [+0.000, +0.006] | +0.000 [-0.006, +0.005] | -0.001 [-0.008, +0.006] | +0.002 [-0.001, +0.006] | -0.001 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.513 | 0.000 | 0.021 | 0.384 | 0.650 |
| ac | 0.573 | 0.024 | 0.156 | 0.452 | 0.703 |
| c | 0.614 | 0.152 | 0.320 | 0.601 | 0.694 |
| cc | 0.620 | 0.172 | 0.328 | 0.594 | 0.701 |
| d | 0.612 | 0.160 | 0.332 | 0.585 | 0.693 |
| dc | 0.621 | 0.168 | 0.330 | 0.600 | 0.701 |
| tb2c | 0.614 | 0.118 | 0.348 | 0.556 | 0.706 |
| tbc | 0.613 | 0.150 | 0.326 | 0.594 | 0.694 |
| cs | 0.616 | 0.156 | 0.324 | 0.608 | 0.693 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.640 | 0.000 | 0.053 | 0.578 | 0.781 |
| ac | 0.736 | 0.072 | 0.365 | 0.702 | 0.850 |
| c | 0.754 | 0.248 | 0.453 | 0.767 | 0.832 |
| cc | 0.767 | 0.240 | 0.490 | 0.767 | 0.848 |
| d | 0.762 | 0.234 | 0.469 | 0.756 | 0.846 |
| dc | 0.773 | 0.250 | 0.480 | 0.785 | 0.851 |
| tb2c | 0.763 | 0.196 | 0.461 | 0.755 | 0.852 |
| tbc | 0.754 | 0.258 | 0.443 | 0.756 | 0.835 |
| cs | 0.757 | 0.246 | 0.459 | 0.762 | 0.836 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.117 [-0.138, -0.094] | -0.220 [-0.278, -0.164] | -0.393 [-0.471, -0.299] | -0.173 [-0.232, -0.120] | -0.062 [-0.078, -0.047] |
| ac | -0.033 [-0.047, -0.020] | -0.160 [-0.206, -0.112] | -0.113 [-0.164, -0.064] | -0.092 [-0.140, -0.045] | +0.004 [-0.005, +0.015] |
| c | -0.008 [-0.014, -0.002] | +0.006 [-0.006, +0.022] | -0.004 [-0.019, +0.012] | +0.009 [-0.006, +0.024] | -0.015 [-0.022, -0.008] |
| cc | +0.004 [-0.002, +0.010] | +0.000 [-0.008, +0.008] | +0.018 [+0.002, +0.036] | +0.004 [-0.010, +0.020] | +0.003 [-0.005, +0.011] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| dc | +0.008 [+0.004, +0.011] | +0.002 [-0.004, +0.009] | +0.006 [-0.002, +0.015] | +0.021 [+0.010, +0.033] | +0.005 [+0.000, +0.009] |
| tb2c | +0.001 [-0.007, +0.009] | -0.050 [-0.082, -0.019] | +0.012 [-0.006, +0.030] | -0.006 [-0.026, +0.016] | +0.007 [-0.001, +0.016] |
| tbc | -0.010 [-0.015, -0.004] | +0.008 [-0.011, +0.033] | -0.008 [-0.020, +0.004] | -0.001 [-0.016, +0.015] | -0.014 [-0.021, -0.007] |
| cs | -0.007 [-0.012, -0.001] | +0.008 [-0.002, +0.023] | -0.004 [-0.019, +0.012] | +0.007 [-0.008, +0.023] | -0.012 [-0.019, -0.005] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.124 [-0.146, -0.102] | -0.222 [-0.279, -0.166] | -0.398 [-0.479, -0.306] | -0.194 [-0.251, -0.142] | -0.067 [-0.083, -0.051] |
| ac | -0.041 [-0.055, -0.027] | -0.162 [-0.209, -0.114] | -0.119 [-0.169, -0.072] | -0.113 [-0.164, -0.066] | -0.000 [-0.010, +0.010] |
| c | -0.016 [-0.022, -0.009] | +0.004 [-0.008, +0.018] | -0.010 [-0.026, +0.006] | -0.012 [-0.029, +0.004] | -0.019 [-0.028, -0.012] |
| cc | -0.004 [-0.009, +0.001] | -0.002 [-0.008, +0.004] | +0.012 [-0.002, +0.028] | -0.016 [-0.034, -0.001] | -0.002 [-0.009, +0.005] |
| d | -0.008 [-0.011, -0.004] | -0.002 [-0.009, +0.004] | -0.006 [-0.015, +0.002] | -0.021 [-0.033, -0.010] | -0.005 [-0.009, -0.000] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| tb2c | -0.006 [-0.014, +0.001] | -0.052 [-0.085, -0.021] | +0.006 [-0.012, +0.022] | -0.027 [-0.048, -0.004] | +0.002 [-0.006, +0.011] |
| tbc | -0.017 [-0.024, -0.011] | +0.006 [-0.012, +0.031] | -0.014 [-0.028, +0.000] | -0.022 [-0.038, -0.005] | -0.019 [-0.027, -0.011] |
| cs | -0.014 [-0.020, -0.008] | +0.006 [-0.004, +0.018] | -0.010 [-0.027, +0.006] | -0.013 [-0.030, +0.004] | -0.017 [-0.024, -0.010] |

### Session 9 selection rule applied to the eval queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F5 | tbc | 3.70 | -0.010 | +0.002 | -0.004 | -0.010 | +0.001 |

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 1.100 | 0.894 | 0.725 | 0.055 |
| centered | 0.125 | 0.555 | 0.431 | 0.028 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2c | 1.99 | 0.929 | 738 |
| tbc | 3.70 | 1.000 | 738 |

### Session 9 hypotheses on the eval queries

H9c, c - tbc (type-blind k-means at c's budget, uncentered): P1 image in [0,.2)+[.2,.5) -0.002 [-0.022, +0.014]; P2 textlike in [.5,.8)+[.8,1] +0.004 [-0.006, +0.015]; interval includes zero in a primary cell: yes, H9c dead.

## Session 19 commit-subject queries, E4 (nomic-embed-v1.5, cache nomic-embed-v1.5_s19)

Queries: 1162 over 522 directories and 440 owners; 1595 directories ranked (random recall@5 = 0.0031); 0 queries dropped because their directory has no embedded file. Representations use all embedded files of a directory (the query is not a file). Calibration seed 20261104 gives the text mean for the centered rows.

### recall@1

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.059 | 0.073 | 0.089 | 0.096 | 0.114 | 0.106 | 0.056 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.066 | 0.081 | 0.094 | 0.098 | 0.119 | 0.109 | 0.058 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.000 | 0.008 | 0.041 | 0.074 | 0.074 | 0.082 | 0.041 |

### recall@5

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.127 | 0.153 | 0.172 | 0.162 | 0.194 | 0.192 | 0.096 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.142 | 0.165 | 0.181 | 0.169 | 0.201 | 0.200 | 0.099 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.000 | 0.049 | 0.098 | 0.098 | 0.139 | 0.123 | 0.066 |

### recall@10

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.174 | 0.196 | 0.215 | 0.216 | 0.235 | 0.244 | 0.132 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.194 | 0.211 | 0.222 | 0.221 | 0.240 | 0.250 | 0.136 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.000 | 0.074 | 0.156 | 0.172 | 0.189 | 0.197 | 0.098 |

### Differences in recall@5: point, owner-clustered 95% interval

| cell | subset | queries | c - a | d - c | ac - a | cc - c |
|---|---|---:|---|---|---|---|
| all | all | 1162 | +0.045 [+0.025, +0.066] | +0.022 [+0.006, +0.038] | +0.026 [+0.009, +0.045] | -0.010 [-0.026, +0.005] |
| all | names miss | 1051 | +0.034 [+0.012, +0.054] | +0.011 [-0.003, +0.026] | +0.019 [+0.001, +0.036] | -0.010 [-0.027, +0.007] |
| text-heavy [0,.2)+[.2,.5) | all | 1040 | +0.038 [+0.017, +0.060] | +0.020 [+0.004, +0.037] | +0.023 [+0.003, +0.041] | -0.012 [-0.031, +0.006] |
| text-heavy [0,.2)+[.2,.5) | names miss | 937 | +0.028 [+0.004, +0.050] | +0.007 [-0.007, +0.023] | +0.018 [-0.001, +0.036] | -0.012 [-0.027, +0.004] |
| image-heavy [.5,.8)+[.8,1] | all | 122 | +0.098 [+0.038, +0.169] | +0.041 [+0.009, +0.079] | +0.049 [+0.008, +0.104] | +0.000 [-0.033, +0.033] |
| image-heavy [.5,.8)+[.8,1] | names miss | 114 | +0.088 [+0.036, +0.148] | +0.044 [+0.009, +0.086] | +0.026 [+0.000, +0.071] | +0.000 [-0.035, +0.035] |

H19d statistic (E4): image-heavy directories, 122 queries from 66 owners; gate, recall@5 of d 0.139 (needs 0.10 and more than names alone, 0.066): passed; owner-weighted c - a +0.101 [+0.040, +0.172]; H19d: inconclusive (fewer than 100 owners) (the registered reading is the E1 run).

## E2: embedding

```
files 12656; ok 12049; not ok by modality {'image': 466, 'other': 130, 'text': 10, 'table': 1}
```

## E2: eval.py

Model: jina-clip-v2. Queries: 7372 over 1172 directories; 1600 directories ranked (random recall@k = k/1600). Queries dropped for lack of a vector: 236 {'image': 107, 'other': 128, 'table': 1}. Queries in calibration directories, not used: 1717.

Mean representative vectors per directory: a 1.00, ac 1.00, c 3.70, cc 3.70, d 7.53, dc 7.53, tb2c 1.99, tbc 3.70, cs 3.97.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 7372 | 1172 | a | 0.499 | 0.582 | 0.612 | 0.653 | [0.588, 0.639] |
| all | 7372 | 1172 | ac | 0.536 | 0.631 | 0.666 | 0.708 | [0.643, 0.690] |
| all | 7372 | 1172 | c | 0.570 | 0.651 | 0.679 | 0.714 | [0.658, 0.700] |
| all | 7372 | 1172 | cc | 0.571 | 0.658 | 0.688 | 0.724 | [0.666, 0.709] |
| all | 7372 | 1172 | d | 0.569 | 0.652 | 0.677 | 0.714 | [0.654, 0.699] |
| all | 7372 | 1172 | dc | 0.574 | 0.663 | 0.690 | 0.730 | [0.668, 0.712] |
| all | 7372 | 1172 | tb2c | 0.566 | 0.651 | 0.681 | 0.720 | [0.659, 0.703] |
| all | 7372 | 1172 | tbc | 0.570 | 0.651 | 0.680 | 0.712 | [0.659, 0.701] |
| all | 7372 | 1172 | cs | 0.574 | 0.655 | 0.680 | 0.716 | [0.659, 0.701] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 4157 | 555 | a | 0.641 | 0.719 | 0.745 | 0.782 | [0.720, 0.771] |
| [0,.2) | 4157 | 555 | ac | 0.635 | 0.723 | 0.752 | 0.784 | [0.724, 0.777] |
| [0,.2) | 4157 | 555 | c | 0.638 | 0.721 | 0.747 | 0.780 | [0.718, 0.772] |
| [0,.2) | 4157 | 555 | cc | 0.636 | 0.724 | 0.751 | 0.781 | [0.723, 0.778] |
| [0,.2) | 4157 | 555 | d | 0.630 | 0.721 | 0.748 | 0.783 | [0.718, 0.774] |
| [0,.2) | 4157 | 555 | dc | 0.633 | 0.728 | 0.756 | 0.789 | [0.727, 0.783] |
| [0,.2) | 4157 | 555 | tb2c | 0.640 | 0.724 | 0.751 | 0.785 | [0.723, 0.777] |
| [0,.2) | 4157 | 555 | tbc | 0.639 | 0.721 | 0.748 | 0.779 | [0.719, 0.774] |
| [0,.2) | 4157 | 555 | cs | 0.644 | 0.725 | 0.749 | 0.781 | [0.719, 0.775] |
| [.2,.5) | 1357 | 284 | a | 0.201 | 0.288 | 0.324 | 0.366 | [0.290, 0.356] |
| [.2,.5) | 1357 | 284 | ac | 0.335 | 0.447 | 0.490 | 0.542 | [0.451, 0.528] |
| [.2,.5) | 1357 | 284 | c | 0.391 | 0.469 | 0.500 | 0.535 | [0.448, 0.547] |
| [.2,.5) | 1357 | 284 | cc | 0.399 | 0.487 | 0.520 | 0.574 | [0.474, 0.562] |
| [.2,.5) | 1357 | 284 | d | 0.403 | 0.475 | 0.499 | 0.542 | [0.445, 0.549] |
| [.2,.5) | 1357 | 284 | dc | 0.408 | 0.489 | 0.515 | 0.568 | [0.463, 0.562] |
| [.2,.5) | 1357 | 284 | tb2c | 0.380 | 0.468 | 0.504 | 0.550 | [0.464, 0.542] |
| [.2,.5) | 1357 | 284 | tbc | 0.393 | 0.473 | 0.500 | 0.531 | [0.447, 0.545] |
| [.2,.5) | 1357 | 284 | cs | 0.392 | 0.473 | 0.497 | 0.537 | [0.446, 0.544] |
| [.5,.8) | 865 | 165 | a | 0.225 | 0.298 | 0.328 | 0.373 | [0.245, 0.402] |
| [.5,.8) | 865 | 165 | ac | 0.371 | 0.476 | 0.527 | 0.597 | [0.457, 0.591] |
| [.5,.8) | 865 | 165 | c | 0.479 | 0.551 | 0.586 | 0.628 | [0.510, 0.651] |
| [.5,.8) | 865 | 165 | cc | 0.497 | 0.579 | 0.615 | 0.653 | [0.543, 0.681] |
| [.5,.8) | 865 | 165 | d | 0.496 | 0.562 | 0.584 | 0.628 | [0.509, 0.649] |
| [.5,.8) | 865 | 165 | dc | 0.502 | 0.580 | 0.602 | 0.665 | [0.529, 0.666] |
| [.5,.8) | 865 | 165 | tb2c | 0.465 | 0.561 | 0.588 | 0.642 | [0.515, 0.655] |
| [.5,.8) | 865 | 165 | tbc | 0.474 | 0.554 | 0.586 | 0.628 | [0.511, 0.651] |
| [.5,.8) | 865 | 165 | cs | 0.486 | 0.556 | 0.592 | 0.634 | [0.517, 0.656] |
| [.8,1] | 993 | 168 | a | 0.548 | 0.658 | 0.698 | 0.747 | [0.646, 0.739] |
| [.8,1] | 993 | 168 | ac | 0.540 | 0.630 | 0.670 | 0.718 | [0.600, 0.733] |
| [.8,1] | 993 | 168 | c | 0.605 | 0.690 | 0.720 | 0.756 | [0.673, 0.759] |
| [.8,1] | 993 | 168 | cc | 0.602 | 0.685 | 0.713 | 0.748 | [0.659, 0.757] |
| [.8,1] | 993 | 168 | d | 0.607 | 0.682 | 0.705 | 0.739 | [0.659, 0.745] |
| [.8,1] | 993 | 168 | dc | 0.617 | 0.698 | 0.731 | 0.758 | [0.684, 0.770] |
| [.8,1] | 993 | 168 | tb2c | 0.600 | 0.677 | 0.706 | 0.745 | [0.651, 0.752] |
| [.8,1] | 993 | 168 | tbc | 0.609 | 0.690 | 0.722 | 0.754 | [0.676, 0.760] |
| [.8,1] | 993 | 168 | cs | 0.607 | 0.692 | 0.718 | 0.756 | [0.671, 0.759] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 1846 | 642 | a | 0.377 | 0.462 | 0.492 | 0.534 | [0.441, 0.541] |
| image | 1846 | 642 | ac | 0.426 | 0.512 | 0.561 | 0.613 | [0.514, 0.601] |
| image | 1846 | 642 | c | 0.521 | 0.590 | 0.621 | 0.655 | [0.582, 0.658] |
| image | 1846 | 642 | cc | 0.522 | 0.596 | 0.622 | 0.661 | [0.582, 0.659] |
| image | 1846 | 642 | d | 0.527 | 0.593 | 0.611 | 0.648 | [0.572, 0.647] |
| image | 1846 | 642 | dc | 0.534 | 0.607 | 0.635 | 0.677 | [0.598, 0.672] |
| image | 1846 | 642 | tb2c | 0.496 | 0.575 | 0.607 | 0.653 | [0.565, 0.646] |
| image | 1846 | 642 | tbc | 0.520 | 0.593 | 0.625 | 0.657 | [0.584, 0.660] |
| image | 1846 | 642 | cs | 0.525 | 0.595 | 0.619 | 0.655 | [0.578, 0.656] |
| pdf_text | 148 | 37 | a | 0.736 | 0.811 | 0.838 | 0.845 | [0.719, 0.915] |
| pdf_text | 148 | 37 | ac | 0.824 | 0.899 | 0.912 | 0.919 | [0.803, 0.969] |
| pdf_text | 148 | 37 | c | 0.824 | 0.892 | 0.899 | 0.919 | [0.782, 0.961] |
| pdf_text | 148 | 37 | cc | 0.845 | 0.905 | 0.919 | 0.946 | [0.826, 0.969] |
| pdf_text | 148 | 37 | d | 0.804 | 0.885 | 0.885 | 0.919 | [0.763, 0.951] |
| pdf_text | 148 | 37 | dc | 0.831 | 0.905 | 0.905 | 0.939 | [0.793, 0.965] |
| pdf_text | 148 | 37 | tb2c | 0.831 | 0.912 | 0.932 | 0.946 | [0.837, 0.982] |
| pdf_text | 148 | 37 | tbc | 0.818 | 0.892 | 0.899 | 0.926 | [0.782, 0.961] |
| pdf_text | 148 | 37 | cs | 0.811 | 0.885 | 0.892 | 0.919 | [0.772, 0.955] |
| text | 5273 | 1078 | a | 0.534 | 0.618 | 0.649 | 0.689 | [0.619, 0.674] |
| text | 5273 | 1078 | ac | 0.566 | 0.665 | 0.696 | 0.735 | [0.670, 0.720] |
| text | 5273 | 1078 | c | 0.578 | 0.664 | 0.692 | 0.728 | [0.666, 0.716] |
| text | 5273 | 1078 | cc | 0.579 | 0.672 | 0.703 | 0.738 | [0.676, 0.726] |
| text | 5273 | 1078 | d | 0.576 | 0.665 | 0.694 | 0.732 | [0.666, 0.720] |
| text | 5273 | 1078 | dc | 0.580 | 0.674 | 0.703 | 0.741 | [0.676, 0.728] |
| text | 5273 | 1078 | tb2c | 0.582 | 0.670 | 0.699 | 0.736 | [0.673, 0.723] |
| text | 5273 | 1078 | tbc | 0.580 | 0.664 | 0.692 | 0.725 | [0.667, 0.716] |
| text | 5273 | 1078 | cs | 0.583 | 0.668 | 0.695 | 0.731 | [0.668, 0.720] |
| table | 77 | 34 | a | 0.468 | 0.494 | 0.519 | 0.623 | [0.167, 0.734] |
| table | 77 | 34 | ac | 0.468 | 0.532 | 0.571 | 0.675 | [0.263, 0.769] |
| table | 77 | 34 | c | 0.571 | 0.623 | 0.649 | 0.675 | [0.391, 0.814] |
| table | 77 | 34 | cc | 0.571 | 0.636 | 0.675 | 0.740 | [0.432, 0.826] |
| table | 77 | 34 | d | 0.584 | 0.623 | 0.649 | 0.675 | [0.391, 0.814] |
| table | 77 | 34 | dc | 0.558 | 0.649 | 0.662 | 0.727 | [0.410, 0.820] |
| table | 77 | 34 | tb2c | 0.519 | 0.584 | 0.623 | 0.675 | [0.365, 0.792] |
| table | 77 | 34 | tbc | 0.571 | 0.623 | 0.636 | 0.662 | [0.365, 0.803] |
| table | 77 | 34 | cs | 0.571 | 0.623 | 0.649 | 0.662 | [0.391, 0.814] |
| other | 21 | 9 | a | 0.857 | 0.857 | 0.857 | 0.857 | [0.444, 0.983] |
| other | 21 | 9 | ac | 0.905 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | c | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | cc | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | d | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | dc | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | tb2c | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | tbc | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |
| other | 21 | 9 | cs | 0.857 | 0.905 | 0.905 | 0.905 | [0.556, 1.000] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 142 | 121 | a | 0.000 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] |
| image [0,.2) | 142 | 121 | ac | 0.007 | 0.021 | 0.042 | 0.049 | [0.014, 0.077] |
| image [0,.2) | 142 | 121 | c | 0.092 | 0.120 | 0.134 | 0.148 | [0.057, 0.219] |
| image [0,.2) | 142 | 121 | cc | 0.092 | 0.141 | 0.155 | 0.169 | [0.075, 0.240] |
| image [0,.2) | 142 | 121 | d | 0.106 | 0.134 | 0.134 | 0.148 | [0.057, 0.219] |
| image [0,.2) | 142 | 121 | dc | 0.099 | 0.141 | 0.169 | 0.197 | [0.089, 0.260] |
| image [0,.2) | 142 | 121 | tb2c | 0.049 | 0.063 | 0.092 | 0.113 | [0.030, 0.167] |
| image [0,.2) | 142 | 121 | tbc | 0.092 | 0.127 | 0.141 | 0.155 | [0.060, 0.228] |
| image [0,.2) | 142 | 121 | cs | 0.099 | 0.134 | 0.134 | 0.148 | [0.057, 0.219] |
| image [.2,.5) | 358 | 242 | a | 0.014 | 0.031 | 0.031 | 0.039 | [0.011, 0.059] |
| image [.2,.5) | 358 | 242 | ac | 0.112 | 0.184 | 0.223 | 0.279 | [0.162, 0.289] |
| image [.2,.5) | 358 | 242 | c | 0.254 | 0.277 | 0.307 | 0.327 | [0.223, 0.380] |
| image [.2,.5) | 358 | 242 | cc | 0.268 | 0.296 | 0.313 | 0.372 | [0.240, 0.380] |
| image [.2,.5) | 358 | 242 | d | 0.251 | 0.285 | 0.293 | 0.316 | [0.223, 0.361] |
| image [.2,.5) | 358 | 242 | dc | 0.268 | 0.296 | 0.318 | 0.363 | [0.244, 0.384] |
| image [.2,.5) | 358 | 242 | tb2c | 0.209 | 0.246 | 0.277 | 0.332 | [0.208, 0.340] |
| image [.2,.5) | 358 | 242 | tbc | 0.251 | 0.279 | 0.307 | 0.327 | [0.229, 0.379] |
| image [.2,.5) | 358 | 242 | cs | 0.254 | 0.274 | 0.285 | 0.313 | [0.213, 0.353] |
| image [.5,.8) | 473 | 140 | a | 0.313 | 0.404 | 0.440 | 0.495 | [0.333, 0.526] |
| image [.5,.8) | 473 | 140 | ac | 0.459 | 0.558 | 0.632 | 0.696 | [0.554, 0.708] |
| image [.5,.8) | 473 | 140 | c | 0.550 | 0.619 | 0.658 | 0.698 | [0.586, 0.721] |
| image [.5,.8) | 473 | 140 | cc | 0.556 | 0.645 | 0.681 | 0.723 | [0.611, 0.750] |
| image [.5,.8) | 473 | 140 | d | 0.567 | 0.636 | 0.658 | 0.712 | [0.586, 0.717] |
| image [.5,.8) | 473 | 140 | dc | 0.571 | 0.653 | 0.683 | 0.753 | [0.614, 0.744] |
| image [.5,.8) | 473 | 140 | tb2c | 0.518 | 0.636 | 0.672 | 0.734 | [0.594, 0.746] |
| image [.5,.8) | 473 | 140 | tbc | 0.541 | 0.628 | 0.662 | 0.702 | [0.589, 0.725] |
| image [.5,.8) | 473 | 140 | cs | 0.560 | 0.630 | 0.668 | 0.708 | [0.599, 0.728] |
| image [.8,1] | 873 | 139 | a | 0.622 | 0.745 | 0.790 | 0.845 | [0.746, 0.835] |
| image [.8,1] | 873 | 139 | ac | 0.605 | 0.701 | 0.745 | 0.797 | [0.664, 0.819] |
| image [.8,1] | 873 | 139 | c | 0.684 | 0.780 | 0.810 | 0.850 | [0.769, 0.848] |
| image [.8,1] | 873 | 139 | cc | 0.678 | 0.767 | 0.794 | 0.827 | [0.745, 0.841] |
| image [.8,1] | 873 | 139 | d | 0.686 | 0.771 | 0.794 | 0.830 | [0.750, 0.834] |
| image [.8,1] | 873 | 139 | dc | 0.694 | 0.785 | 0.816 | 0.842 | [0.776, 0.854] |
| image [.8,1] | 873 | 139 | tb2c | 0.675 | 0.761 | 0.790 | 0.829 | [0.741, 0.840] |
| image [.8,1] | 873 | 139 | tbc | 0.688 | 0.779 | 0.813 | 0.849 | [0.774, 0.851] |
| image [.8,1] | 873 | 139 | cs | 0.686 | 0.782 | 0.808 | 0.850 | [0.765, 0.847] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 4011 | 555 | a | 0.665 | 0.745 | 0.772 | 0.811 | [0.746, 0.796] |
| textlike [0,.2) | 4011 | 555 | ac | 0.658 | 0.748 | 0.777 | 0.810 | [0.749, 0.801] |
| textlike [0,.2) | 4011 | 555 | c | 0.657 | 0.743 | 0.769 | 0.802 | [0.741, 0.794] |
| textlike [0,.2) | 4011 | 555 | cc | 0.655 | 0.744 | 0.772 | 0.803 | [0.745, 0.797] |
| textlike [0,.2) | 4011 | 555 | d | 0.648 | 0.742 | 0.770 | 0.805 | [0.742, 0.796] |
| textlike [0,.2) | 4011 | 555 | dc | 0.652 | 0.749 | 0.777 | 0.810 | [0.748, 0.803] |
| textlike [0,.2) | 4011 | 555 | tb2c | 0.661 | 0.747 | 0.775 | 0.809 | [0.746, 0.799] |
| textlike [0,.2) | 4011 | 555 | tbc | 0.658 | 0.742 | 0.769 | 0.801 | [0.742, 0.794] |
| textlike [0,.2) | 4011 | 555 | cs | 0.663 | 0.746 | 0.771 | 0.804 | [0.743, 0.797] |
| textlike [.2,.5) | 996 | 282 | a | 0.266 | 0.379 | 0.427 | 0.482 | [0.383, 0.468] |
| textlike [.2,.5) | 996 | 282 | ac | 0.413 | 0.539 | 0.584 | 0.635 | [0.541, 0.627] |
| textlike [.2,.5) | 996 | 282 | c | 0.439 | 0.537 | 0.568 | 0.608 | [0.520, 0.615] |
| textlike [.2,.5) | 996 | 282 | cc | 0.445 | 0.554 | 0.593 | 0.646 | [0.544, 0.641] |
| textlike [.2,.5) | 996 | 282 | d | 0.456 | 0.542 | 0.571 | 0.622 | [0.519, 0.626] |
| textlike [.2,.5) | 996 | 282 | dc | 0.456 | 0.557 | 0.584 | 0.641 | [0.530, 0.636] |
| textlike [.2,.5) | 996 | 282 | tb2c | 0.440 | 0.546 | 0.584 | 0.628 | [0.540, 0.628] |
| textlike [.2,.5) | 996 | 282 | tbc | 0.442 | 0.541 | 0.567 | 0.603 | [0.520, 0.614] |
| textlike [.2,.5) | 996 | 282 | cs | 0.440 | 0.543 | 0.572 | 0.616 | [0.522, 0.622] |
| textlike [.5,.8) | 392 | 159 | a | 0.120 | 0.171 | 0.194 | 0.227 | [0.106, 0.290] |
| textlike [.5,.8) | 392 | 159 | ac | 0.265 | 0.378 | 0.401 | 0.477 | [0.292, 0.501] |
| textlike [.5,.8) | 392 | 159 | c | 0.393 | 0.469 | 0.500 | 0.543 | [0.397, 0.589] |
| textlike [.5,.8) | 392 | 159 | cc | 0.426 | 0.500 | 0.536 | 0.569 | [0.436, 0.623] |
| textlike [.5,.8) | 392 | 159 | d | 0.411 | 0.472 | 0.495 | 0.526 | [0.395, 0.588] |
| textlike [.5,.8) | 392 | 159 | dc | 0.418 | 0.492 | 0.505 | 0.559 | [0.405, 0.596] |
| textlike [.5,.8) | 392 | 159 | tb2c | 0.401 | 0.469 | 0.487 | 0.531 | [0.389, 0.580] |
| textlike [.5,.8) | 392 | 159 | tbc | 0.393 | 0.464 | 0.495 | 0.538 | [0.392, 0.583] |
| textlike [.5,.8) | 392 | 159 | cs | 0.395 | 0.467 | 0.500 | 0.543 | [0.395, 0.589] |
| textlike [.8,1] | 120 | 107 | a | 0.008 | 0.025 | 0.025 | 0.033 | [0.000, 0.090] |
| textlike [.8,1] | 120 | 107 | ac | 0.067 | 0.117 | 0.125 | 0.142 | [0.059, 0.220] |
| textlike [.8,1] | 120 | 107 | c | 0.033 | 0.033 | 0.067 | 0.075 | [0.008, 0.155] |
| textlike [.8,1] | 120 | 107 | cc | 0.050 | 0.083 | 0.125 | 0.175 | [0.052, 0.221] |
| textlike [.8,1] | 120 | 107 | d | 0.033 | 0.033 | 0.058 | 0.075 | [0.008, 0.131] |
| textlike [.8,1] | 120 | 107 | dc | 0.058 | 0.067 | 0.117 | 0.150 | [0.049, 0.212] |
| textlike [.8,1] | 120 | 107 | tb2c | 0.058 | 0.067 | 0.092 | 0.133 | [0.034, 0.177] |
| textlike [.8,1] | 120 | 107 | tbc | 0.033 | 0.042 | 0.058 | 0.067 | [0.008, 0.131] |
| textlike [.8,1] | 120 | 107 | cs | 0.033 | 0.033 | 0.067 | 0.075 | [0.008, 0.155] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 500 | 363 | 0.022 | 0.172 | 0.258 | 0.268 | 0.248 | 0.276 | 0.224 | 0.260 | 0.242 | +0.236 | [+0.173, +0.298] |
| P2 textlike in [.5,.8)+[.8,1] | 512 | 266 | 0.154 | 0.336 | 0.398 | 0.439 | 0.393 | 0.414 | 0.395 | 0.393 | 0.398 | +0.244 | [+0.180, +0.306] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 part: image [0,.2) | 142 | 121 | 0.000 | 0.042 | 0.134 | 0.155 | 0.134 | 0.169 | 0.092 | 0.141 | 0.134 | +0.134 | [+0.054, +0.214] |
| P1 part: image [.2,.5) | 358 | 242 | 0.031 | 0.223 | 0.307 | 0.313 | 0.293 | 0.318 | 0.277 | 0.307 | 0.285 | +0.277 | [+0.196, +0.354] |
| P2 part: textlike [.5,.8) | 392 | 159 | 0.194 | 0.401 | 0.500 | 0.536 | 0.495 | 0.505 | 0.487 | 0.495 | 0.500 | +0.306 | [+0.229, +0.381] |
| P2 part: textlike [.8,1] | 120 | 107 | 0.025 | 0.125 | 0.067 | 0.125 | 0.058 | 0.117 | 0.092 | 0.058 | 0.067 | +0.042 | [+0.008, +0.086] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| image in [.5,.8)+[.8,1] | 1346 | 279 | 0.667 | 0.705 | 0.756 | 0.754 | 0.746 | 0.769 | 0.749 | 0.760 | 0.759 | +0.089 | [+0.061, +0.122] |
| textlike in [0,.2)+[.2,.5) | 5007 | 837 | 0.704 | 0.738 | 0.729 | 0.737 | 0.731 | 0.739 | 0.737 | 0.729 | 0.731 | +0.025 | [+0.014, +0.037] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 500 | 363 | 0.022 | 0.172 | 0.258 | 0.268 | 0.248 | 0.276 | 0.224 | 0.260 | 0.242 | -0.010 | [-0.034, +0.006] |
| P2 textlike in [.5,.8)+[.8,1] | 512 | 266 | 0.154 | 0.336 | 0.398 | 0.439 | 0.393 | 0.414 | 0.395 | 0.393 | 0.398 | -0.006 | [-0.020, +0.006] |
| P1 part: image [0,.2) | 142 | 121 | 0.000 | 0.042 | 0.134 | 0.155 | 0.134 | 0.169 | 0.092 | 0.141 | 0.134 | +0.000 | [+0.000, +0.000] |
| P1 part: image [.2,.5) | 358 | 242 | 0.031 | 0.223 | 0.307 | 0.313 | 0.293 | 0.318 | 0.277 | 0.307 | 0.285 | -0.014 | [-0.048, +0.009] |
| P2 part: textlike [.5,.8) | 392 | 159 | 0.194 | 0.401 | 0.500 | 0.536 | 0.495 | 0.505 | 0.487 | 0.495 | 0.500 | -0.005 | [-0.021, +0.011] |
| P2 part: textlike [.8,1] | 120 | 107 | 0.025 | 0.125 | 0.067 | 0.125 | 0.058 | 0.117 | 0.092 | 0.058 | 0.067 | -0.008 | [-0.025, +0.000] |
| image in [.5,.8)+[.8,1] | 1346 | 279 | 0.667 | 0.705 | 0.756 | 0.754 | 0.746 | 0.769 | 0.749 | 0.760 | 0.759 | -0.010 | [-0.023, +0.002] |
| textlike in [0,.2)+[.2,.5) | 5007 | 837 | 0.704 | 0.738 | 0.729 | 0.737 | 0.731 | 0.739 | 0.737 | 0.729 | 0.731 | +0.002 | [-0.005, +0.008] |
| all [0,.2) | 4157 | 555 | 0.745 | 0.752 | 0.747 | 0.751 | 0.748 | 0.756 | 0.751 | 0.748 | 0.749 | +0.001 | [-0.005, +0.008] |
| all [.2,.5) | 1357 | 284 | 0.324 | 0.490 | 0.500 | 0.520 | 0.499 | 0.515 | 0.504 | 0.500 | 0.497 | -0.001 | [-0.014, +0.011] |
| all [.5,.8) | 865 | 165 | 0.328 | 0.527 | 0.586 | 0.615 | 0.584 | 0.602 | 0.588 | 0.586 | 0.592 | -0.002 | [-0.012, +0.007] |
| all [.8,1] | 993 | 168 | 0.698 | 0.670 | 0.720 | 0.713 | 0.705 | 0.731 | 0.706 | 0.722 | 0.718 | -0.015 | [-0.030, +0.001] |
| image [0,.2) | 142 | 121 | 0.000 | 0.042 | 0.134 | 0.155 | 0.134 | 0.169 | 0.092 | 0.141 | 0.134 | +0.000 | [+0.000, +0.000] |
| image [.2,.5) | 358 | 242 | 0.031 | 0.223 | 0.307 | 0.313 | 0.293 | 0.318 | 0.277 | 0.307 | 0.285 | -0.014 | [-0.045, +0.010] |
| image [.5,.8) | 473 | 140 | 0.440 | 0.632 | 0.658 | 0.681 | 0.658 | 0.683 | 0.672 | 0.662 | 0.668 | +0.000 | [-0.012, +0.014] |
| image [.8,1] | 873 | 139 | 0.790 | 0.745 | 0.810 | 0.794 | 0.794 | 0.816 | 0.790 | 0.813 | 0.808 | -0.016 | [-0.036, +0.001] |
| textlike [0,.2) | 4011 | 555 | 0.772 | 0.777 | 0.769 | 0.772 | 0.770 | 0.777 | 0.775 | 0.769 | 0.771 | +0.001 | [-0.005, +0.008] |
| textlike [.2,.5) | 996 | 282 | 0.427 | 0.584 | 0.568 | 0.593 | 0.571 | 0.584 | 0.584 | 0.567 | 0.572 | +0.003 | [-0.012, +0.018] |
| textlike [.5,.8) | 392 | 159 | 0.194 | 0.401 | 0.500 | 0.536 | 0.495 | 0.505 | 0.487 | 0.495 | 0.500 | -0.005 | [-0.021, +0.010] |
| textlike [.8,1] | 120 | 107 | 0.025 | 0.125 | 0.067 | 0.125 | 0.058 | 0.117 | 0.092 | 0.058 | 0.067 | -0.008 | [-0.030, +0.000] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.612 | 0.022 | 0.154 | 0.667 | 0.704 | -0.067 [-0.080, -0.052] | -0.236 [-0.298, -0.173] | -0.244 [-0.306, -0.180] | -0.089 [-0.122, -0.061] | -0.025 [-0.037, -0.014] | -0.244 |
| ac | ref | 1.00 | 0.666 | 0.172 | 0.336 | 0.705 | 0.738 | -0.013 [-0.025, -0.001] | -0.086 [-0.138, -0.038] | -0.062 [-0.118, -0.009] | -0.051 [-0.093, -0.014] | +0.010 [-0.002, +0.021] | -0.086 |
| c | ref | 3.70 | 0.679 | 0.258 | 0.398 | 0.756 | 0.729 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| cc | ref | 3.70 | 0.688 | 0.268 | 0.439 | 0.754 | 0.737 | +0.009 [+0.002, +0.014] | +0.010 [-0.023, +0.035] | +0.041 [+0.020, +0.064] | -0.002 [-0.021, +0.016] | +0.008 [+0.001, +0.015] | -0.002 |
| d | ref | 7.53 | 0.677 | 0.248 | 0.393 | 0.746 | 0.731 | -0.002 [-0.007, +0.003] | -0.010 [-0.034, +0.006] | -0.006 [-0.020, +0.006] | -0.010 [-0.023, +0.002] | +0.002 [-0.005, +0.008] | -0.010 |
| dc | ref | 7.53 | 0.690 | 0.276 | 0.414 | 0.769 | 0.739 | +0.011 [+0.006, +0.017] | +0.018 [-0.010, +0.040] | +0.016 [-0.002, +0.035] | +0.013 [+0.000, +0.026] | +0.010 [+0.003, +0.017] | +0.010 |
| tb2c | F5 | 1.99 | 0.681 | 0.224 | 0.395 | 0.749 | 0.737 | +0.001 [-0.007, +0.010] | -0.034 [-0.077, +0.002] | -0.004 [-0.037, +0.030] | -0.007 [-0.031, +0.013] | +0.008 [-0.001, +0.017] | -0.034 |
| tbc | F5 | 3.70 | 0.680 | 0.260 | 0.393 | 0.760 | 0.729 | +0.001 [-0.002, +0.003] | +0.002 [-0.014, +0.016] | -0.006 [-0.014, +0.002] | +0.004 [-0.002, +0.010] | +0.000 [-0.003, +0.003] | -0.006 |
| cs | ref | 3.97 | 0.680 | 0.242 | 0.398 | 0.759 | 0.731 | +0.001 [-0.002, +0.004] | -0.016 [-0.040, +0.000] | +0.000 [-0.006, +0.006] | +0.002 [-0.007, +0.011] | +0.002 [-0.001, +0.006] | -0.016 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.499 | 0.010 | 0.094 | 0.513 | 0.585 |
| ac | 0.536 | 0.082 | 0.219 | 0.553 | 0.609 |
| c | 0.570 | 0.208 | 0.309 | 0.637 | 0.614 |
| cc | 0.571 | 0.218 | 0.338 | 0.635 | 0.613 |
| d | 0.569 | 0.210 | 0.322 | 0.644 | 0.610 |
| dc | 0.574 | 0.220 | 0.334 | 0.651 | 0.613 |
| tb2c | 0.566 | 0.164 | 0.320 | 0.620 | 0.617 |
| tbc | 0.570 | 0.206 | 0.309 | 0.637 | 0.615 |
| cs | 0.574 | 0.210 | 0.311 | 0.642 | 0.619 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.653 | 0.028 | 0.182 | 0.722 | 0.745 |
| ac | 0.708 | 0.214 | 0.398 | 0.762 | 0.775 |
| c | 0.714 | 0.276 | 0.434 | 0.796 | 0.764 |
| cc | 0.724 | 0.314 | 0.477 | 0.790 | 0.772 |
| d | 0.714 | 0.268 | 0.420 | 0.789 | 0.769 |
| dc | 0.730 | 0.316 | 0.463 | 0.811 | 0.776 |
| tb2c | 0.720 | 0.270 | 0.438 | 0.796 | 0.773 |
| tbc | 0.712 | 0.278 | 0.428 | 0.797 | 0.762 |
| cs | 0.716 | 0.266 | 0.434 | 0.800 | 0.767 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.065 [-0.079, -0.050] | -0.226 [-0.283, -0.167] | -0.238 [-0.300, -0.175] | -0.079 [-0.114, -0.047] | -0.027 [-0.041, -0.014] |
| ac | -0.011 [-0.024, +0.002] | -0.076 [-0.118, -0.033] | -0.057 [-0.111, -0.006] | -0.041 [-0.081, -0.005] | +0.008 [-0.005, +0.021] |
| c | +0.002 [-0.003, +0.007] | +0.010 [-0.006, +0.034] | +0.006 [-0.006, +0.020] | +0.010 [-0.002, +0.023] | -0.002 [-0.008, +0.005] |
| cc | +0.010 [+0.004, +0.017] | +0.020 [+0.004, +0.037] | +0.047 [+0.028, +0.069] | +0.008 [-0.007, +0.024] | +0.006 [-0.002, +0.014] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| dc | +0.013 [+0.009, +0.017] | +0.028 [+0.013, +0.045] | +0.021 [+0.006, +0.040] | +0.023 [+0.014, +0.033] | +0.008 [+0.003, +0.014] |
| tb2c | +0.003 [-0.005, +0.012] | -0.024 [-0.054, +0.002] | +0.002 [-0.026, +0.034] | +0.003 [-0.016, +0.022] | +0.006 [-0.005, +0.016] |
| tbc | +0.002 [-0.003, +0.007] | +0.012 [-0.002, +0.026] | +0.000 [-0.014, +0.015] | +0.014 [+0.002, +0.026] | -0.002 [-0.009, +0.005] |
| cs | +0.003 [-0.002, +0.007] | -0.006 [-0.013, +0.000] | +0.006 [-0.006, +0.019] | +0.013 [+0.002, +0.024] | +0.001 [-0.005, +0.006] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.078 [-0.092, -0.063] | -0.254 [-0.309, -0.194] | -0.260 [-0.323, -0.197] | -0.102 [-0.137, -0.070] | -0.035 [-0.048, -0.022] |
| ac | -0.024 [-0.037, -0.012] | -0.104 [-0.148, -0.061] | -0.078 [-0.132, -0.030] | -0.064 [-0.102, -0.029] | -0.000 [-0.013, +0.012] |
| c | -0.011 [-0.017, -0.006] | -0.018 [-0.040, +0.010] | -0.016 [-0.035, +0.002] | -0.013 [-0.026, +0.000] | -0.010 [-0.017, -0.003] |
| cc | -0.003 [-0.008, +0.002] | -0.008 [-0.022, +0.004] | +0.025 [+0.011, +0.041] | -0.015 [-0.026, -0.003] | -0.002 [-0.009, +0.005] |
| d | -0.013 [-0.017, -0.009] | -0.028 [-0.045, -0.013] | -0.021 [-0.040, -0.006] | -0.023 [-0.033, -0.014] | -0.008 [-0.014, -0.003] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| tb2c | -0.010 [-0.018, -0.002] | -0.052 [-0.084, -0.023] | -0.020 [-0.047, +0.008] | -0.020 [-0.038, -0.003] | -0.002 [-0.013, +0.008] |
| tbc | -0.011 [-0.017, -0.006] | -0.016 [-0.036, +0.002] | -0.021 [-0.041, -0.002] | -0.009 [-0.022, +0.004] | -0.010 [-0.017, -0.003] |
| cs | -0.010 [-0.016, -0.005] | -0.034 [-0.052, -0.019] | -0.016 [-0.035, +0.004] | -0.010 [-0.025, +0.004] | -0.008 [-0.015, -0.001] |

### Session 9 selection rule applied to the eval queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F5 | tbc | 3.70 | -0.006 | +0.002 | -0.006 | +0.004 | +0.000 |

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.819 | 0.774 | 0.687 | 0.189 |
| centered | 0.155 | 0.557 | 0.445 | 0.085 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2c | 1.99 | 0.912 | 738 |
| tbc | 3.70 | 0.999 | 738 |

### Session 9 hypotheses on the eval queries

H9c, c - tbc (type-blind k-means at c's budget, uncentered): P1 image in [0,.2)+[.2,.5) -0.002 [-0.016, +0.014]; P2 textlike in [.5,.8)+[.8,1] +0.006 [-0.002, +0.014]; interval includes zero in a primary cell: yes, H9c dead.

## Session 19 commit-subject queries, E2 (jina-clip-v2, cache jina-clip-v2_s19)

Queries: 1162 over 522 directories and 440 owners; 1595 directories ranked (random recall@5 = 0.0031); 0 queries dropped because their directory has no embedded file. Representations use all embedded files of a directory (the query is not a file). Calibration seed 20261104 gives the text mean for the centered rows.

### recall@1

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.080 | 0.051 | 0.108 | 0.050 | 0.120 | 0.060 | 0.056 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.085 | 0.052 | 0.109 | 0.048 | 0.127 | 0.061 | 0.058 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.041 | 0.041 | 0.107 | 0.066 | 0.066 | 0.057 | 0.041 |

### recall@5

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.190 | 0.118 | 0.214 | 0.120 | 0.224 | 0.138 | 0.096 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.206 | 0.125 | 0.216 | 0.121 | 0.230 | 0.142 | 0.099 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.057 | 0.057 | 0.197 | 0.107 | 0.172 | 0.098 | 0.066 |

### recall@10

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1162 | 522 | 440 | 0.234 | 0.159 | 0.256 | 0.161 | 0.281 | 0.186 | 0.132 |
| text-heavy [0,.2)+[.2,.5) | 1040 | 454 | 386 | 0.254 | 0.167 | 0.258 | 0.161 | 0.286 | 0.188 | 0.136 |
| image-heavy [.5,.8)+[.8,1] | 122 | 68 | 66 | 0.066 | 0.090 | 0.238 | 0.164 | 0.238 | 0.164 | 0.098 |

### Differences in recall@5: point, owner-clustered 95% interval

| cell | subset | queries | c - a | d - c | ac - a | cc - c |
|---|---|---:|---|---|---|---|
| all | all | 1162 | +0.024 [+0.004, +0.044] | +0.009 [-0.005, +0.024] | -0.072 [-0.091, -0.055] | -0.095 [-0.117, -0.073] |
| all | names miss | 1051 | +0.026 [+0.004, +0.048] | +0.004 [-0.011, +0.018] | -0.069 [-0.087, -0.053] | -0.096 [-0.120, -0.075] |
| text-heavy [0,.2)+[.2,.5) | all | 1040 | +0.011 [-0.009, +0.033] | +0.013 [-0.001, +0.030] | -0.081 [-0.101, -0.063] | -0.095 [-0.119, -0.072] |
| text-heavy [0,.2)+[.2,.5) | names miss | 937 | +0.011 [-0.009, +0.033] | +0.007 [-0.008, +0.023] | -0.077 [-0.097, -0.058] | -0.096 [-0.120, -0.074] |
| image-heavy [.5,.8)+[.8,1] | all | 122 | +0.139 [+0.066, +0.228] | -0.025 [-0.076, +0.017] | +0.000 [-0.023, +0.025] | -0.090 [-0.153, -0.040] |
| image-heavy [.5,.8)+[.8,1] | names miss | 114 | +0.149 [+0.071, +0.240] | -0.026 [-0.077, +0.019] | +0.000 [-0.026, +0.026] | -0.096 [-0.159, -0.038] |

H19d statistic (E2): image-heavy directories, 122 queries from 66 owners; gate, recall@5 of d 0.172 (needs 0.10 and more than names alone, 0.066): passed; owner-weighted c - a +0.146 [+0.071, +0.230]; H19d: inconclusive (fewer than 100 owners) (the registered reading is the E1 run).

## Session 19 validity and verdicts (E1, E4, E2; E1 decides the hypotheses)

Queries: 7372 over 1172 directories and 858 owners (effective owners 419). Queries per encoder before taking those all encoders share: E1 7372, E4 7372, E2 7372.

### Reproduction of eval.py's directory intervals of c - a

- E1 P1: here +0.100 [+0.060, +0.142]; eval.py +0.100 [+0.060, +0.142]; same
- E1 P2: here +0.107 [+0.060, +0.161]; eval.py +0.107 [+0.060, +0.161]; same
- E4 P1: here +0.226 [+0.173, +0.281]; eval.py +0.226 [+0.173, +0.281]; same
- E4 P2: here +0.389 [+0.297, +0.471]; eval.py +0.389 [+0.297, +0.471]; same
- E2 P1: here +0.236 [+0.173, +0.298]; eval.py +0.236 [+0.173, +0.298]; same
- E2 P2: here +0.244 [+0.180, +0.306]; eval.py +0.244 [+0.180, +0.306]; same

Reproduced: the directory bootstrap here is eval.py's.

### Flags (counts over the evaluation queries)

| cell | queries | directories | owners (effective) | same-stem sibling | names alone in top 5 | clean |
|---|---:|---:|---|---:|---:|---:|
| all | 7372 | 1172 | 858 (419) | 569 | 3178 | 4194 |
| P1 | 500 | 363 | 334 (205) | 16 | 132 | 368 |
| P2 | 512 | 266 | 231 (93) | 93 | 167 | 345 |
| M1 | 1346 | 279 | 250 (114) | 79 | 804 | 542 |
| M2 | 5007 | 837 | 647 (296) | 380 | 2068 | 2939 |

### Filename-only baseline (no encoder): recall@5

| cell | d_fn (max over names) | a_fn (pooled names) |
|---|---:|---:|
| all | 0.402 | 0.384 |
| P1 | 0.254 | 0.222 |
| P2 | 0.318 | 0.305 |
| M1 | 0.551 | 0.560 |
| M2 | 0.384 | 0.360 |

### c - a by subset (H19a reads 'all', H19b reads 'clean')

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | all | c - a | all | 7372 | 1172 | 858 (419) | +0.021 | [+0.012, +0.029] | [+0.012, +0.030] | +0.020 [+0.010, +0.031] |
| E1 | all | c - a | P1 | 500 | 363 | 334 (205) | +0.100 | [+0.060, +0.142] | [+0.061, +0.143] | +0.069 [+0.038, +0.101] |
| E1 | all | c - a | P2 | 512 | 266 | 231 (93) | +0.107 | [+0.060, +0.161] | [+0.058, +0.164] | +0.071 [+0.038, +0.108] |
| E1 | all | c - a | M1 | 1346 | 279 | 250 (114) | +0.036 | [+0.012, +0.061] | [+0.012, +0.063] | +0.035 [+0.009, +0.065] |
| E1 | all | c - a | M2 | 5007 | 837 | 647 (296) | +0.000 | [-0.008, +0.007] | [-0.008, +0.008] | -0.000 [-0.013, +0.012] |
| E1 | names miss | c - a | all | 4194 | 1077 | 826 (506) | +0.018 | [+0.006, +0.029] | [+0.008, +0.030] | +0.016 [+0.004, +0.029] |
| E1 | names miss | c - a | P1 | 368 | 313 | 294 (227) | +0.082 | [+0.041, +0.123] | [+0.044, +0.122] | +0.058 [+0.024, +0.091] |
| E1 | names miss | c - a | P2 | 345 | 228 | 203 (132) | +0.093 | [+0.042, +0.147] | [+0.042, +0.148] | +0.056 [+0.021, +0.093] |
| E1 | names miss | c - a | M1 | 542 | 199 | 185 (100) | +0.030 | [-0.008, +0.069] | [-0.006, +0.068] | +0.022 [-0.013, +0.060] |
| E1 | names miss | c - a | M2 | 2939 | 756 | 609 (373) | -0.001 | [-0.013, +0.009] | [-0.012, +0.010] | +0.002 [-0.013, +0.017] |
| E1 | no sibling | c - a | all | 6803 | 1160 | 853 (431) | +0.021 | [+0.012, +0.030] | [+0.012, +0.030] | +0.020 [+0.009, +0.030] |
| E1 | no sibling | c - a | P1 | 484 | 353 | 326 (203) | +0.103 | [+0.061, +0.147] | [+0.058, +0.148] | +0.071 [+0.038, +0.105] |
| E1 | no sibling | c - a | P2 | 419 | 249 | 218 (127) | +0.103 | [+0.060, +0.155] | [+0.053, +0.149] | +0.067 [+0.031, +0.105] |
| E1 | no sibling | c - a | M1 | 1267 | 272 | 245 (110) | +0.039 | [+0.012, +0.065] | [+0.012, +0.065] | +0.036 [+0.007, +0.065] |
| E1 | no sibling | c - a | M2 | 4627 | 826 | 639 (301) | +0.000 | [-0.008, +0.008] | [-0.008, +0.008] | -0.000 [-0.013, +0.013] |
| E1 | clean | c - a | all | 4194 | 1077 | 826 (506) | +0.018 | [+0.006, +0.029] | [+0.008, +0.030] | +0.016 [+0.004, +0.029] |
| E1 | clean | c - a | P1 | 368 | 313 | 294 (227) | +0.082 | [+0.041, +0.123] | [+0.044, +0.122] | +0.058 [+0.024, +0.091] |
| E1 | clean | c - a | P2 | 345 | 228 | 203 (132) | +0.093 | [+0.042, +0.147] | [+0.042, +0.148] | +0.056 [+0.021, +0.093] |
| E1 | clean | c - a | M1 | 542 | 199 | 185 (100) | +0.030 | [-0.008, +0.069] | [-0.006, +0.068] | +0.022 [-0.013, +0.060] |
| E1 | clean | c - a | M2 | 2939 | 756 | 609 (373) | -0.001 | [-0.013, +0.009] | [-0.012, +0.010] | +0.002 [-0.013, +0.017] |
| E4 | all | c - a | all | 7372 | 1172 | 858 (419) | +0.109 | [+0.087, +0.129] | [+0.086, +0.136] | +0.106 [+0.090, +0.124] |
| E4 | all | c - a | P1 | 500 | 363 | 334 (205) | +0.226 | [+0.173, +0.281] | [+0.170, +0.279] | +0.117 [+0.085, +0.152] |
| E4 | all | c - a | P2 | 512 | 266 | 231 (93) | +0.389 | [+0.297, +0.471] | [+0.287, +0.497] | +0.170 [+0.128, +0.216] |
| E4 | all | c - a | M1 | 1346 | 279 | 250 (114) | +0.182 | [+0.130, +0.238] | [+0.122, +0.251] | +0.227 [+0.175, +0.282] |
| E4 | all | c - a | M2 | 5007 | 837 | 647 (296) | +0.047 | [+0.034, +0.062] | [+0.034, +0.062] | +0.085 [+0.065, +0.105] |
| E4 | names miss | c - a | all | 4194 | 1077 | 826 (506) | +0.078 | [+0.060, +0.096] | [+0.059, +0.097] | +0.080 [+0.063, +0.098] |
| E4 | names miss | c - a | P1 | 368 | 313 | 294 (227) | +0.128 | [+0.080, +0.172] | [+0.083, +0.174] | +0.079 [+0.051, +0.109] |
| E4 | names miss | c - a | P2 | 345 | 228 | 203 (132) | +0.238 | [+0.161, +0.318] | [+0.161, +0.317] | +0.124 [+0.086, +0.167] |
| E4 | names miss | c - a | M1 | 542 | 199 | 185 (100) | +0.081 | [+0.021, +0.144] | [+0.023, +0.141] | +0.137 [+0.076, +0.198] |
| E4 | names miss | c - a | M2 | 2939 | 756 | 609 (373) | +0.052 | [+0.033, +0.071] | [+0.033, +0.069] | +0.080 [+0.055, +0.105] |
| E4 | no sibling | c - a | all | 6803 | 1160 | 853 (431) | +0.095 | [+0.077, +0.113] | [+0.077, +0.115] | +0.098 [+0.081, +0.115] |
| E4 | no sibling | c - a | P1 | 484 | 353 | 326 (203) | +0.219 | [+0.166, +0.277] | [+0.160, +0.275] | +0.116 [+0.085, +0.152] |
| E4 | no sibling | c - a | P2 | 419 | 249 | 218 (127) | +0.301 | [+0.224, +0.374] | [+0.220, +0.378] | +0.150 [+0.107, +0.192] |
| E4 | no sibling | c - a | M1 | 1267 | 272 | 245 (110) | +0.147 | [+0.100, +0.194] | [+0.104, +0.198] | +0.210 [+0.161, +0.262] |
| E4 | no sibling | c - a | M2 | 4627 | 826 | 639 (301) | +0.048 | [+0.034, +0.063] | [+0.034, +0.064] | +0.081 [+0.059, +0.102] |
| E4 | clean | c - a | all | 4194 | 1077 | 826 (506) | +0.078 | [+0.060, +0.096] | [+0.059, +0.097] | +0.080 [+0.063, +0.098] |
| E4 | clean | c - a | P1 | 368 | 313 | 294 (227) | +0.128 | [+0.080, +0.172] | [+0.083, +0.174] | +0.079 [+0.051, +0.109] |
| E4 | clean | c - a | P2 | 345 | 228 | 203 (132) | +0.238 | [+0.161, +0.318] | [+0.161, +0.317] | +0.124 [+0.086, +0.167] |
| E4 | clean | c - a | M1 | 542 | 199 | 185 (100) | +0.081 | [+0.021, +0.144] | [+0.023, +0.141] | +0.137 [+0.076, +0.198] |
| E4 | clean | c - a | M2 | 2939 | 756 | 609 (373) | +0.052 | [+0.033, +0.071] | [+0.033, +0.069] | +0.080 [+0.055, +0.105] |
| E2 | all | c - a | all | 7372 | 1172 | 858 (419) | +0.067 | [+0.052, +0.080] | [+0.053, +0.081] | +0.067 [+0.054, +0.080] |
| E2 | all | c - a | P1 | 500 | 363 | 334 (205) | +0.236 | [+0.173, +0.298] | [+0.170, +0.293] | +0.121 [+0.087, +0.156] |
| E2 | all | c - a | P2 | 512 | 266 | 231 (93) | +0.244 | [+0.180, +0.306] | [+0.178, +0.311] | +0.125 [+0.089, +0.164] |
| E2 | all | c - a | M1 | 1346 | 279 | 250 (114) | +0.089 | [+0.061, +0.122] | [+0.058, +0.125] | +0.134 [+0.092, +0.176] |
| E2 | all | c - a | M2 | 5007 | 837 | 647 (296) | +0.025 | [+0.014, +0.037] | [+0.014, +0.037] | +0.046 [+0.031, +0.063] |
| E2 | names miss | c - a | all | 4194 | 1077 | 826 (506) | +0.053 | [+0.038, +0.069] | [+0.039, +0.069] | +0.058 [+0.044, +0.072] |
| E2 | names miss | c - a | P1 | 368 | 313 | 294 (227) | +0.130 | [+0.081, +0.178] | [+0.081, +0.180] | +0.079 [+0.051, +0.110] |
| E2 | names miss | c - a | P2 | 345 | 228 | 203 (132) | +0.194 | [+0.126, +0.268] | [+0.120, +0.263] | +0.102 [+0.066, +0.139] |
| E2 | names miss | c - a | M1 | 542 | 199 | 185 (100) | +0.063 | [+0.017, +0.109] | [+0.019, +0.111] | +0.091 [+0.045, +0.138] |
| E2 | names miss | c - a | M2 | 2939 | 756 | 609 (373) | +0.026 | [+0.012, +0.042] | [+0.011, +0.040] | +0.043 [+0.025, +0.062] |
| E2 | no sibling | c - a | all | 6803 | 1160 | 853 (431) | +0.061 | [+0.047, +0.075] | [+0.048, +0.075] | +0.062 [+0.049, +0.076] |
| E2 | no sibling | c - a | P1 | 484 | 353 | 326 (203) | +0.231 | [+0.169, +0.298] | [+0.165, +0.300] | +0.117 [+0.082, +0.152] |
| E2 | no sibling | c - a | P2 | 419 | 249 | 218 (127) | +0.234 | [+0.172, +0.298] | [+0.166, +0.303] | +0.119 [+0.083, +0.159] |
| E2 | no sibling | c - a | M1 | 1267 | 272 | 245 (110) | +0.083 | [+0.054, +0.114] | [+0.055, +0.116] | +0.128 [+0.090, +0.166] |
| E2 | no sibling | c - a | M2 | 4627 | 826 | 639 (301) | +0.022 | [+0.011, +0.033] | [+0.011, +0.034] | +0.039 [+0.023, +0.055] |
| E2 | clean | c - a | all | 4194 | 1077 | 826 (506) | +0.053 | [+0.038, +0.069] | [+0.039, +0.069] | +0.058 [+0.044, +0.072] |
| E2 | clean | c - a | P1 | 368 | 313 | 294 (227) | +0.130 | [+0.081, +0.178] | [+0.081, +0.180] | +0.079 [+0.051, +0.110] |
| E2 | clean | c - a | P2 | 345 | 228 | 203 (132) | +0.194 | [+0.126, +0.268] | [+0.120, +0.263] | +0.102 [+0.066, +0.139] |
| E2 | clean | c - a | M1 | 542 | 199 | 185 (100) | +0.063 | [+0.017, +0.109] | [+0.019, +0.111] | +0.091 [+0.045, +0.138] |
| E2 | clean | c - a | M2 | 2939 | 756 | 609 (373) | +0.026 | [+0.012, +0.042] | [+0.011, +0.040] | +0.043 [+0.025, +0.062] |

### c - d, cs - d and cs - c (H19c reads c - d over all queries)

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | all | c - d | all | 7372 | 1172 | 858 (419) | +0.001 | [-0.003, +0.005] | [-0.004, +0.005] | -0.003 [-0.007, +0.001] |
| E1 | all | c - d | P1 | 500 | 363 | 334 (205) | -0.022 | [-0.040, -0.004] | [-0.040, -0.006] | -0.029 [-0.047, -0.011] |
| E1 | all | c - d | P2 | 512 | 266 | 231 (93) | -0.018 | [-0.031, -0.006] | [-0.031, -0.006] | -0.017 [-0.035, -0.001] |
| E1 | all | c - d | M1 | 1346 | 279 | 250 (114) | +0.015 | [+0.001, +0.030] | [-0.001, +0.030] | +0.002 [-0.009, +0.011] |
| E1 | all | c - d | M2 | 5007 | 837 | 647 (296) | +0.001 | [-0.003, +0.006] | [-0.003, +0.006] | -0.003 [-0.008, +0.002] |
| E1 | all | cs - d | all | 7372 | 1172 | 858 (419) | +0.002 | [-0.002, +0.006] | [-0.003, +0.006] | -0.002 [-0.006, +0.002] |
| E1 | all | cs - d | P1 | 500 | 363 | 334 (205) | -0.022 | [-0.040, -0.006] | [-0.039, -0.006] | -0.023 [-0.043, -0.007] |
| E1 | all | cs - d | P2 | 512 | 266 | 231 (93) | -0.012 | [-0.023, +0.000] | [-0.024, +0.000] | -0.012 [-0.029, +0.003] |
| E1 | all | cs - d | M1 | 1346 | 279 | 250 (114) | +0.011 | [-0.001, +0.024] | [-0.001, +0.023] | +0.001 [-0.008, +0.008] |
| E1 | all | cs - d | M2 | 5007 | 837 | 647 (296) | +0.003 | [-0.001, +0.008] | [-0.001, +0.007] | -0.001 [-0.006, +0.003] |
| E1 | all | cs - c | all | 7372 | 1172 | 858 (419) | +0.001 | [-0.001, +0.003] | [-0.001, +0.003] | +0.001 [-0.000, +0.003] |
| E1 | all | cs - c | P1 | 500 | 363 | 334 (205) | +0.000 | [-0.008, +0.008] | [-0.008, +0.008] | +0.005 [-0.001, +0.015] |
| E1 | all | cs - c | P2 | 512 | 266 | 231 (93) | +0.006 | [-0.002, +0.016] | [-0.002, +0.015] | +0.005 [-0.004, +0.014] |
| E1 | all | cs - c | M1 | 1346 | 279 | 250 (114) | -0.004 | [-0.011, +0.004] | [-0.011, +0.003] | -0.001 [-0.006, +0.003] |
| E1 | all | cs - c | M2 | 5007 | 837 | 647 (296) | +0.002 | [-0.000, +0.004] | [-0.000, +0.004] | +0.002 [-0.000, +0.004] |
| E4 | all | c - d | all | 7372 | 1172 | 858 (419) | -0.008 | [-0.014, -0.002] | [-0.014, -0.002] | -0.020 [-0.027, -0.013] |
| E4 | all | c - d | P1 | 500 | 363 | 334 (205) | +0.006 | [-0.006, +0.022] | [-0.006, +0.020] | +0.000 [-0.004, +0.004] |
| E4 | all | c - d | P2 | 512 | 266 | 231 (93) | -0.004 | [-0.019, +0.012] | [-0.018, +0.011] | -0.004 [-0.013, +0.004] |
| E4 | all | c - d | M1 | 1346 | 279 | 250 (114) | +0.009 | [-0.006, +0.024] | [-0.007, +0.022] | -0.004 [-0.016, +0.009] |
| E4 | all | c - d | M2 | 5007 | 837 | 647 (296) | -0.015 | [-0.022, -0.008] | [-0.022, -0.007] | -0.033 [-0.044, -0.022] |
| E4 | all | cs - d | all | 7372 | 1172 | 858 (419) | -0.007 | [-0.012, -0.001] | [-0.012, -0.001] | -0.016 [-0.023, -0.009] |
| E4 | all | cs - d | P1 | 500 | 363 | 334 (205) | +0.008 | [-0.002, +0.023] | [-0.002, +0.022] | +0.001 [-0.003, +0.004] |
| E4 | all | cs - d | P2 | 512 | 266 | 231 (93) | -0.004 | [-0.019, +0.012] | [-0.019, +0.011] | -0.006 [-0.016, +0.003] |
| E4 | all | cs - d | M1 | 1346 | 279 | 250 (114) | +0.007 | [-0.008, +0.023] | [-0.008, +0.022] | -0.001 [-0.013, +0.011] |
| E4 | all | cs - d | M2 | 5007 | 837 | 647 (296) | -0.012 | [-0.019, -0.005] | [-0.019, -0.005] | -0.027 [-0.038, -0.018] |
| E4 | all | cs - c | all | 7372 | 1172 | 858 (419) | +0.001 | [-0.001, +0.004] | [-0.001, +0.004] | +0.004 [+0.001, +0.007] |
| E4 | all | cs - c | P1 | 500 | 363 | 334 (205) | +0.002 | [+0.000, +0.006] | [+0.000, +0.006] | +0.000 [+0.000, +0.001] |
| E4 | all | cs - c | P2 | 512 | 266 | 231 (93) | +0.000 | [-0.006, +0.005] | [-0.006, +0.006] | -0.002 [-0.006, +0.001] |
| E4 | all | cs - c | M1 | 1346 | 279 | 250 (114) | -0.001 | [-0.008, +0.006] | [-0.008, +0.006] | +0.002 [-0.002, +0.008] |
| E4 | all | cs - c | M2 | 5007 | 837 | 647 (296) | +0.002 | [-0.001, +0.006] | [-0.001, +0.006] | +0.006 [+0.002, +0.010] |
| E2 | all | c - d | all | 7372 | 1172 | 858 (419) | +0.002 | [-0.003, +0.007] | [-0.003, +0.007] | -0.002 [-0.006, +0.003] |
| E2 | all | c - d | P1 | 500 | 363 | 334 (205) | +0.010 | [-0.006, +0.034] | [-0.006, +0.035] | -0.000 [-0.005, +0.005] |
| E2 | all | c - d | P2 | 512 | 266 | 231 (93) | +0.006 | [-0.006, +0.020] | [-0.007, +0.020] | +0.002 [-0.006, +0.010] |
| E2 | all | c - d | M1 | 1346 | 279 | 250 (114) | +0.010 | [-0.002, +0.023] | [-0.002, +0.023] | -0.005 [-0.015, +0.005] |
| E2 | all | c - d | M2 | 5007 | 837 | 647 (296) | -0.002 | [-0.008, +0.005] | [-0.008, +0.005] | -0.001 [-0.007, +0.005] |
| E2 | all | cs - d | all | 7372 | 1172 | 858 (419) | +0.003 | [-0.002, +0.007] | [-0.002, +0.008] | -0.001 [-0.005, +0.003] |
| E2 | all | cs - d | P1 | 500 | 363 | 334 (205) | -0.006 | [-0.013, +0.000] | [-0.014, +0.000] | -0.003 [-0.007, +0.000] |
| E2 | all | cs - d | P2 | 512 | 266 | 231 (93) | +0.006 | [-0.006, +0.019] | [-0.006, +0.020] | +0.000 [-0.007, +0.007] |
| E2 | all | cs - d | M1 | 1346 | 279 | 250 (114) | +0.013 | [+0.002, +0.024] | [+0.002, +0.023] | +0.000 [-0.007, +0.008] |
| E2 | all | cs - d | M2 | 5007 | 837 | 647 (296) | +0.001 | [-0.005, +0.006] | [-0.005, +0.007] | -0.000 [-0.006, +0.006] |
| E2 | all | cs - c | all | 7372 | 1172 | 858 (419) | +0.001 | [-0.002, +0.004] | [-0.002, +0.004] | +0.001 [-0.002, +0.002] |
| E2 | all | cs - c | P1 | 500 | 363 | 334 (205) | -0.016 | [-0.040, +0.000] | [-0.041, +0.000] | -0.003 [-0.007, +0.000] |
| E2 | all | cs - c | P2 | 512 | 266 | 231 (93) | +0.000 | [-0.006, +0.006] | [-0.006, +0.006] | -0.001 [-0.006, +0.002] |
| E2 | all | cs - c | M1 | 1346 | 279 | 250 (114) | +0.002 | [-0.007, +0.011] | [-0.007, +0.011] | +0.005 [-0.001, +0.012] |
| E2 | all | cs - c | M2 | 5007 | 837 | 647 (296) | +0.002 | [-0.001, +0.006] | [-0.001, +0.006] | +0.000 [-0.002, +0.003] |

### The registered tests (owner-weighted mean, 10,000 resamples of owners)

| encoder | test | queries | owners | point | 95% | 98.33% | reading |
|---|---|---:|---:|---:|---|---|---|
| E1 | H19a P1s: c - a (primary) | 226 | 86 | +0.193 | [+0.114, +0.277] | [+0.099, +0.295] | inconclusive (fewer than 100 owners) |
| E1 | H19a P2s: c - a (primary) | 355 | 98 | +0.166 | [+0.093, +0.241] | [+0.080, +0.260] | inconclusive (fewer than 100 owners) |
| E1 | H19c: c - d where c differs from d (primary) | 5381 | 512 | -0.002 | [-0.011, +0.006] | [-0.014, +0.008] | not inferior (lower bound at or above -0.02) |
| E1 | H19b P1s clean: c - a | 118 | 60 | +0.188 | [+0.090, +0.293] | [+0.071, +0.317] | inconclusive (fewer than 100 owners) |
| E1 | H19b P2s clean: c - a | 205 | 82 | +0.142 | [+0.063, +0.225] | [+0.045, +0.245] | inconclusive (fewer than 100 owners) |
| E1 | no-code folders, P1s: c - a | 67 | 31 | +0.210 | [+0.075, +0.355] | [+0.048, +0.392] | inconclusive (fewer than 100 owners) |
| E1 | no-code folders, P2s: c - a | 232 | 62 | +0.096 | [+0.022, +0.173] | [+0.007, +0.190] | inconclusive (fewer than 100 owners) |
| E1 | all of P1 (lone images included): c - a | 500 | 334 | +0.069 | [+0.037, +0.100] | [+0.030, +0.108] | present, size open (lower bound above zero) |
| E1 | all of P2 (lone texts included): c - a | 512 | 231 | +0.071 | [+0.036, +0.107] | [+0.028, +0.114] | present, size open (lower bound above zero) |
| E1 | cs - d where c differs from d | 5381 | 512 | -0.001 | [-0.011, +0.007] | [-0.013, +0.009] | not inferior (lower bound at or above -0.02) |
| E4 | H19a P1s: c - a (primary) | 226 | 86 | +0.460 | [+0.366, +0.554] | [+0.347, +0.574] | inconclusive (fewer than 100 owners) |
| E4 | H19a P2s: c - a (primary) | 355 | 98 | +0.408 | [+0.321, +0.496] | [+0.303, +0.517] | inconclusive (fewer than 100 owners) |
| E4 | H19c: c - d where c differs from d (primary) | 5381 | 512 | -0.002 | [-0.009, +0.005] | [-0.011, +0.007] | not inferior (lower bound at or above -0.02) |
| E4 | H19b P1s clean: c - a | 118 | 60 | +0.388 | [+0.277, +0.504] | [+0.256, +0.532] | inconclusive (fewer than 100 owners) |
| E4 | H19b P2s clean: c - a | 205 | 82 | +0.328 | [+0.236, +0.424] | [+0.218, +0.446] | inconclusive (fewer than 100 owners) |
| E4 | no-code folders, P1s: c - a | 67 | 31 | +0.505 | [+0.344, +0.661] | [+0.312, +0.704] | inconclusive (fewer than 100 owners) |
| E4 | no-code folders, P2s: c - a | 232 | 62 | +0.478 | [+0.363, +0.591] | [+0.339, +0.614] | inconclusive (fewer than 100 owners) |
| E4 | all of P1 (lone images included): c - a | 500 | 334 | +0.117 | [+0.086, +0.150] | [+0.080, +0.158] | confirmed (lower bound at or above +0.05) |
| E4 | all of P2 (lone texts included): c - a | 512 | 231 | +0.170 | [+0.126, +0.216] | [+0.117, +0.227] | confirmed (lower bound at or above +0.05) |
| E4 | cs - d where c differs from d | 5381 | 512 | -0.001 | [-0.008, +0.006] | [-0.010, +0.008] | not inferior (lower bound at or above -0.02) |
| E2 | H19a P1s: c - a (primary) | 226 | 86 | +0.471 | [+0.375, +0.566] | [+0.357, +0.585] | inconclusive (fewer than 100 owners) |
| E2 | H19a P2s: c - a (primary) | 355 | 98 | +0.301 | [+0.221, +0.382] | [+0.204, +0.401] | inconclusive (fewer than 100 owners) |
| E2 | H19c: c - d where c differs from d (primary) | 5381 | 512 | +0.003 | [-0.003, +0.010] | [-0.005, +0.011] | not inferior (lower bound at or above -0.02) |
| E2 | H19b P1s clean: c - a | 118 | 60 | +0.389 | [+0.276, +0.508] | [+0.253, +0.538] | inconclusive (fewer than 100 owners) |
| E2 | H19b P2s clean: c - a | 205 | 82 | +0.272 | [+0.185, +0.364] | [+0.168, +0.384] | inconclusive (fewer than 100 owners) |
| E2 | no-code folders, P1s: c - a | 67 | 31 | +0.430 | [+0.274, +0.591] | [+0.242, +0.629] | inconclusive (fewer than 100 owners) |
| E2 | no-code folders, P2s: c - a | 232 | 62 | +0.326 | [+0.230, +0.424] | [+0.212, +0.448] | inconclusive (fewer than 100 owners) |
| E2 | all of P1 (lone images included): c - a | 500 | 334 | +0.121 | [+0.089, +0.154] | [+0.082, +0.163] | confirmed (lower bound at or above +0.05) |
| E2 | all of P2 (lone texts included): c - a | 512 | 231 | +0.125 | [+0.088, +0.164] | [+0.080, +0.174] | confirmed (lower bound at or above +0.05) |
| E2 | cs - d where c differs from d | 5381 | 512 | +0.003 | [-0.004, +0.009] | [-0.005, +0.011] | not inferior (lower bound at or above -0.02) |

### Verdicts

H19a (E1, decides): P1s inconclusive (fewer than 100 owners); P2s inconclusive (fewer than 100 owners). H19a: inconclusive.
H19b (E1, secondary): clean P1s inconclusive (fewer than 100 owners); clean P2s inconclusive (fewer than 100 owners).
H19c (E1, decides): not inferior (lower bound at or above -0.02).
H19a (E4, reported by the same rules, no verdict of its own): P1s inconclusive (fewer than 100 owners); P2s inconclusive (fewer than 100 owners). H19a: inconclusive.
H19b (E4, secondary): clean P1s inconclusive (fewer than 100 owners); clean P2s inconclusive (fewer than 100 owners).
H19c (E4, reported by the same rules, no verdict of its own): not inferior (lower bound at or above -0.02).
H19a (E2, reported by the same rules, no verdict of its own): P1s inconclusive (fewer than 100 owners); P2s inconclusive (fewer than 100 owners). H19a: inconclusive.
H19b (E2, secondary): clean P1s inconclusive (fewer than 100 owners); clean P2s inconclusive (fewer than 100 owners).
H19c (E2, reported by the same rules, no verdict of its own): not inferior (lower bound at or above -0.02).

### Secondary: the minority cells by the kind of the query file (c - a, owner-weighted, 95%)

| encoder | cell | kind | queries | owners | R@5 a | R@5 c | R@5 d | c - a |
|---|---|---|---:|---:|---:|---:|---:|---|
| E1 | P1s | image | 226 | 86 | 0.451 | 0.646 | 0.655 | +0.193 [+0.115, +0.279] |
| E1 | P2s | prose | 190 | 65 | 0.742 | 0.821 | 0.847 | +0.096 [+0.022, +0.173] |
| E1 | P2s | code | 80 | 37 | 0.250 | 0.575 | 0.588 | +0.298 [+0.136, +0.457] |
| E1 | P2s | config | 74 | 43 | 0.486 | 0.635 | 0.649 | +0.143 [+0.039, +0.256] |
| E1 | P2s | table | 11 | 10 | 0.455 | 0.636 | 0.636 | +0.200 [+0.000, +0.500] |
| E4 | P1s | image | 226 | 86 | 0.000 | 0.500 | 0.487 | +0.460 [+0.367, +0.554] |
| E4 | P2s | prose | 190 | 65 | 0.047 | 0.726 | 0.742 | +0.487 [+0.367, +0.607] |
| E4 | P2s | code | 80 | 37 | 0.062 | 0.425 | 0.400 | +0.203 [+0.091, +0.329] |
| E4 | P2s | config | 74 | 43 | 0.054 | 0.527 | 0.541 | +0.359 [+0.221, +0.496] |
| E4 | P2s | table | 11 | 10 | 0.000 | 0.545 | 0.545 | +0.500 [+0.200, +0.800] |
| E2 | P1s | image | 226 | 86 | 0.049 | 0.571 | 0.549 | +0.471 [+0.376, +0.566] |
| E2 | P2s | prose | 190 | 65 | 0.363 | 0.726 | 0.721 | +0.315 [+0.215, +0.417] |
| E2 | P2s | code | 80 | 37 | 0.062 | 0.412 | 0.400 | +0.272 [+0.133, +0.420] |
| E2 | P2s | config | 74 | 43 | 0.068 | 0.405 | 0.392 | +0.212 [+0.107, +0.329] |
| E2 | P2s | table | 11 | 10 | 0.000 | 0.273 | 0.273 | +0.200 [+0.000, +0.500] |

### Secondary: recall@5 by the number of embedded files in the query's folder

| encoder | group | cell | queries | owners | c equals d | R@5 a | R@5 c | R@5 cs | R@5 d |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| E1 | 3 to 10 | all | 4354 | 741 | 0.452 | 0.745 | 0.751 | 0.753 | 0.754 |
| E1 | 3 to 10 | P1 | 363 | 279 | 0.471 | 0.262 | 0.317 | 0.322 | 0.342 |
| E1 | 3 to 10 | P2 | 300 | 178 | 0.527 | 0.357 | 0.427 | 0.430 | 0.443 |
| E1 | 3 to 10 | M1 | 636 | 198 | 0.511 | 0.722 | 0.744 | 0.744 | 0.742 |
| E1 | 3 to 10 | M2 | 3052 | 570 | 0.430 | 0.845 | 0.837 | 0.838 | 0.836 |
| E1 | 11 to 30 | all | 2009 | 148 | 0.000 | 0.838 | 0.881 | 0.880 | 0.871 |
| E1 | 11 to 30 | P1 | 103 | 49 | 0.000 | 0.485 | 0.621 | 0.612 | 0.650 |
| E1 | 11 to 30 | P2 | 177 | 60 | 0.000 | 0.576 | 0.740 | 0.751 | 0.763 |
| E1 | 11 to 30 | M1 | 588 | 59 | 0.000 | 0.827 | 0.872 | 0.869 | 0.844 |
| E1 | 11 to 30 | M2 | 1138 | 84 | 0.000 | 0.918 | 0.931 | 0.930 | 0.921 |
| E1 | 31 to 100 | all | 986 | 26 | 0.000 | 0.912 | 0.953 | 0.955 | 0.956 |
| E1 | 31 to 100 | P1 | 33 | 10 | 0.000 | 0.091 | 0.576 | 0.545 | 0.545 |
| E1 | 31 to 100 | P2 | 33 | 5 | 0.000 | 0.606 | 0.758 | 0.758 | 0.758 |
| E1 | 31 to 100 | M1 | 120 | 4 | 0.000 | 0.842 | 0.908 | 0.883 | 0.892 |
| E1 | 31 to 100 | M2 | 799 | 21 | 0.000 | 0.969 | 0.984 | 0.991 | 0.991 |
| E4 | 3 to 10 | all | 4354 | 741 | 0.452 | 0.539 | 0.631 | 0.634 | 0.650 |
| E4 | 3 to 10 | P1 | 363 | 279 | 0.471 | 0.000 | 0.154 | 0.154 | 0.154 |
| E4 | 3 to 10 | P2 | 300 | 178 | 0.527 | 0.053 | 0.280 | 0.277 | 0.287 |
| E4 | 3 to 10 | M1 | 636 | 198 | 0.511 | 0.428 | 0.613 | 0.615 | 0.615 |
| E4 | 3 to 10 | M2 | 3052 | 570 | 0.430 | 0.675 | 0.726 | 0.730 | 0.752 |
| E4 | 11 to 30 | all | 2009 | 148 | 0.000 | 0.664 | 0.813 | 0.811 | 0.804 |
| E4 | 11 to 30 | P1 | 103 | 49 | 0.000 | 0.000 | 0.398 | 0.408 | 0.398 |
| E4 | 11 to 30 | P2 | 177 | 60 | 0.000 | 0.000 | 0.621 | 0.621 | 0.616 |
| E4 | 11 to 30 | M1 | 588 | 59 | 0.000 | 0.636 | 0.803 | 0.801 | 0.787 |
| E4 | 11 to 30 | M2 | 1138 | 84 | 0.000 | 0.843 | 0.885 | 0.881 | 0.878 |
| E4 | 31 to 100 | all | 986 | 26 | 0.000 | 0.837 | 0.939 | 0.940 | 0.933 |
| E4 | 31 to 100 | P1 | 33 | 10 | 0.000 | 0.000 | 0.485 | 0.485 | 0.394 |
| E4 | 31 to 100 | P2 | 33 | 5 | 0.000 | 0.000 | 0.636 | 0.667 | 0.667 |
| E4 | 31 to 100 | M1 | 120 | 4 | 0.000 | 0.642 | 0.883 | 0.867 | 0.850 |
| E4 | 31 to 100 | M2 | 799 | 21 | 0.000 | 0.936 | 0.979 | 0.981 | 0.979 |
| E2 | 3 to 10 | all | 4354 | 741 | 0.452 | 0.521 | 0.576 | 0.578 | 0.577 |
| E2 | 3 to 10 | P1 | 363 | 279 | 0.471 | 0.025 | 0.157 | 0.157 | 0.163 |
| E2 | 3 to 10 | P2 | 300 | 178 | 0.527 | 0.093 | 0.250 | 0.247 | 0.250 |
| E2 | 3 to 10 | M1 | 636 | 198 | 0.511 | 0.555 | 0.665 | 0.675 | 0.675 |
| E2 | 3 to 10 | M2 | 3052 | 570 | 0.430 | 0.614 | 0.640 | 0.640 | 0.638 |
| E2 | 11 to 30 | all | 2009 | 148 | 0.000 | 0.700 | 0.794 | 0.790 | 0.782 |
| E2 | 11 to 30 | P1 | 103 | 49 | 0.000 | 0.019 | 0.485 | 0.476 | 0.485 |
| E2 | 11 to 30 | P2 | 177 | 60 | 0.000 | 0.181 | 0.599 | 0.605 | 0.582 |
| E2 | 11 to 30 | M1 | 588 | 59 | 0.000 | 0.760 | 0.835 | 0.821 | 0.804 |
| E2 | 11 to 30 | M2 | 1138 | 84 | 0.000 | 0.812 | 0.831 | 0.831 | 0.828 |
| E2 | 31 to 100 | all | 986 | 26 | 0.000 | 0.847 | 0.907 | 0.916 | 0.916 |
| E2 | 31 to 100 | P1 | 33 | 10 | 0.000 | 0.000 | 0.667 | 0.455 | 0.455 |
| E2 | 31 to 100 | P2 | 33 | 5 | 0.000 | 0.515 | 0.636 | 0.636 | 0.636 |
| E2 | 31 to 100 | M1 | 120 | 4 | 0.000 | 0.800 | 0.850 | 0.892 | 0.833 |
| E2 | 31 to 100 | M2 | 799 | 21 | 0.000 | 0.904 | 0.936 | 0.950 | 0.959 |

### Secondary: differences by the number of embedded files in the query's folder

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | 3 to 10 | c - a | all | 4354 | 970 | 741 (551) | +0.007 | [-0.003, +0.016] | [-0.004, +0.016] | +0.013 [+0.002, +0.024] |
| E1 | 3 to 10 | c - a | P1 | 363 | 303 | 279 (228) | +0.055 | [+0.019, +0.093] | [+0.019, +0.093] | +0.039 [+0.009, +0.068] |
| E1 | 3 to 10 | c - a | P2 | 300 | 194 | 178 (115) | +0.070 | [+0.018, +0.122] | [+0.023, +0.119] | +0.051 [+0.014, +0.089] |
| E1 | 3 to 10 | c - a | M1 | 636 | 213 | 198 (127) | +0.022 | [-0.005, +0.049] | [-0.005, +0.052] | +0.030 [-0.002, +0.065] |
| E1 | 3 to 10 | c - a | M2 | 3052 | 718 | 570 (417) | -0.009 | [-0.019, +0.001] | [-0.018, +0.002] | -0.003 [-0.016, +0.011] |
| E1 | 3 to 10 | c - d | all | 4354 | 970 | 741 (551) | -0.003 | [-0.008, +0.002] | [-0.008, +0.003] | -0.004 [-0.009, +0.000] |
| E1 | 3 to 10 | c - d | P1 | 363 | 303 | 279 (228) | -0.025 | [-0.043, -0.006] | [-0.045, -0.008] | -0.024 [-0.045, -0.007] |
| E1 | 3 to 10 | c - d | P2 | 300 | 194 | 178 (115) | -0.017 | [-0.034, +0.000] | [-0.034, -0.003] | -0.010 [-0.030, +0.007] |
| E1 | 3 to 10 | c - d | M1 | 636 | 213 | 198 (127) | +0.002 | [-0.010, +0.016] | [-0.011, +0.015] | -0.003 [-0.013, +0.006] |
| E1 | 3 to 10 | c - d | M2 | 3052 | 718 | 570 (417) | +0.000 | [-0.006, +0.006] | [-0.006, +0.006] | -0.003 [-0.008, +0.003] |
| E1 | 3 to 10 | cs - d | all | 4354 | 970 | 741 (551) | -0.001 | [-0.006, +0.004] | [-0.006, +0.004] | -0.003 [-0.007, +0.002] |
| E1 | 3 to 10 | cs - d | P1 | 363 | 303 | 279 (228) | -0.019 | [-0.038, +0.000] | [-0.039, -0.003] | -0.017 [-0.037, +0.001] |
| E1 | 3 to 10 | cs - d | P2 | 300 | 194 | 178 (115) | -0.013 | [-0.030, +0.000] | [-0.031, +0.000] | -0.007 [-0.026, +0.010] |
| E1 | 3 to 10 | cs - d | M1 | 636 | 213 | 198 (127) | +0.002 | [-0.011, +0.015] | [-0.010, +0.015] | -0.002 [-0.012, +0.006] |
| E1 | 3 to 10 | cs - d | M2 | 3052 | 718 | 570 (417) | +0.002 | [-0.004, +0.007] | [-0.004, +0.007] | -0.001 [-0.007, +0.004] |
| E1 | 11 to 30 | c - a | all | 2009 | 161 | 148 (117) | +0.043 | [+0.023, +0.062] | [+0.024, +0.062] | +0.049 [+0.028, +0.074] |
| E1 | 11 to 30 | c - a | P1 | 103 | 49 | 49 (29) | +0.136 | [+0.043, +0.244] | [+0.045, +0.255] | +0.164 [+0.070, +0.278] |
| E1 | 11 to 30 | c - a | P2 | 177 | 65 | 60 (32) | +0.164 | [+0.071, +0.275] | [+0.075, +0.272] | +0.116 [+0.038, +0.197] |
| E1 | 11 to 30 | c - a | M1 | 588 | 60 | 59 (46) | +0.046 | [-0.002, +0.090] | [+0.000, +0.092] | +0.044 [+0.004, +0.091] |
| E1 | 11 to 30 | c - a | M2 | 1138 | 86 | 84 (70) | +0.012 | [-0.001, +0.029] | [-0.001, +0.028] | +0.017 [-0.002, +0.038] |
| E1 | 11 to 30 | c - d | all | 2009 | 161 | 148 (117) | +0.010 | [-0.001, +0.022] | [-0.000, +0.022] | +0.007 [-0.005, +0.018] |
| E1 | 11 to 30 | c - d | P1 | 103 | 49 | 49 (29) | -0.029 | [-0.078, +0.010] | [-0.078, +0.011] | -0.051 [-0.117, +0.000] |
| E1 | 11 to 30 | c - d | P2 | 177 | 65 | 60 (32) | -0.023 | [-0.050, -0.005] | [-0.049, -0.005] | -0.045 [-0.100, -0.003] |
| E1 | 11 to 30 | c - d | M1 | 588 | 60 | 59 (46) | +0.029 | [+0.003, +0.059] | [+0.000, +0.061] | +0.015 [-0.014, +0.044] |
| E1 | 11 to 30 | c - d | M2 | 1138 | 86 | 84 (70) | +0.010 | [+0.000, +0.020] | [-0.001, +0.021] | +0.007 [-0.005, +0.020] |
| E1 | 11 to 30 | cs - d | all | 2009 | 161 | 148 (117) | +0.009 | [-0.001, +0.021] | [-0.001, +0.020] | +0.007 [-0.005, +0.018] |
| E1 | 11 to 30 | cs - d | P1 | 103 | 49 | 49 (29) | -0.039 | [-0.081, -0.008] | [-0.083, -0.008] | -0.056 [-0.122, -0.005] |
| E1 | 11 to 30 | cs - d | P2 | 177 | 65 | 60 (32) | -0.011 | [-0.035, +0.010] | [-0.038, +0.010] | -0.026 [-0.068, +0.002] |
| E1 | 11 to 30 | cs - d | M1 | 588 | 60 | 59 (46) | +0.026 | [+0.004, +0.050] | [+0.004, +0.048] | +0.011 [-0.010, +0.031] |
| E1 | 11 to 30 | cs - d | M2 | 1138 | 86 | 84 (70) | +0.009 | [-0.004, +0.022] | [-0.004, +0.022] | +0.008 [-0.006, +0.024] |
| E1 | 31 to 100 | c - a | all | 986 | 27 | 26 (23) | +0.042 | [+0.018, +0.067] | [+0.019, +0.067] | +0.036 [+0.016, +0.059] |
| E1 | 31 to 100 | c - a | P1 | 33 | 10 | 10 (5) | +0.485 | [+0.350, +0.615] | [+0.357, +0.611] | +0.411 [+0.189, +0.661] |
| E1 | 31 to 100 | c - a | P2 | 33 | 6 | 5 (2) | +0.152 | [+0.000, +0.556] | [+0.000, +0.469] | +0.100 [+0.000, +0.300] |
| E1 | 31 to 100 | c - a | M1 | 120 | 5 | 4 (3) | +0.067 | [-0.023, +0.128] | [+0.000, +0.133] | +0.048 [+0.000, +0.121] |
| E1 | 31 to 100 | c - a | M2 | 799 | 21 | 21 (19) | +0.015 | [+0.001, +0.031] | [+0.001, +0.031] | +0.010 [-0.000, +0.022] |
| E1 | 31 to 100 | c - d | all | 986 | 27 | 26 (23) | -0.003 | [-0.011, +0.007] | [-0.011, +0.006] | -0.003 [-0.010, +0.005] |
| E1 | 31 to 100 | c - d | P1 | 33 | 10 | 10 (5) | +0.030 | [-0.107, +0.089] | [-0.111, +0.089] | -0.012 [-0.090, +0.043] |
| E1 | 31 to 100 | c - d | P2 | 33 | 6 | 5 (2) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E1 | 31 to 100 | c - d | M1 | 120 | 5 | 4 (3) | +0.017 | [-0.054, +0.049] | [-0.031, +0.051] | +0.004 [-0.034, +0.047] |
| E1 | 31 to 100 | c - d | M2 | 799 | 21 | 21 (19) | -0.008 | [-0.016, -0.001] | [-0.016, -0.001] | -0.007 [-0.014, -0.001] |
| E1 | 31 to 100 | cs - d | all | 986 | 27 | 26 (23) | -0.001 | [-0.006, +0.003] | [-0.006, +0.004] | -0.001 [-0.006, +0.004] |
| E1 | 31 to 100 | cs - d | P1 | 33 | 10 | 10 (5) | +0.000 | [-0.111, +0.068] | [-0.125, +0.067] | -0.022 [-0.100, +0.033] |
| E1 | 31 to 100 | cs - d | P2 | 33 | 6 | 5 (2) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E1 | 31 to 100 | cs - d | M1 | 120 | 5 | 4 (3) | -0.008 | [-0.039, +0.017] | [-0.037, +0.015] | -0.014 [-0.038, +0.010] |
| E1 | 31 to 100 | cs - d | M2 | 799 | 21 | 21 (19) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | 3 to 10 | c - a | all | 4354 | 970 | 741 (551) | +0.092 | [+0.076, +0.110] | [+0.071, +0.110] | +0.101 [+0.081, +0.119] |
| E4 | 3 to 10 | c - a | P1 | 363 | 303 | 279 (228) | +0.154 | [+0.105, +0.205] | [+0.102, +0.206] | +0.090 [+0.059, +0.122] |
| E4 | 3 to 10 | c - a | P2 | 300 | 194 | 178 (115) | +0.227 | [+0.158, +0.292] | [+0.152, +0.310] | +0.125 [+0.082, +0.172] |
| E4 | 3 to 10 | c - a | M1 | 636 | 213 | 198 (127) | +0.186 | [+0.121, +0.243] | [+0.126, +0.249] | +0.234 [+0.170, +0.297] |
| E4 | 3 to 10 | c - a | M2 | 3052 | 718 | 570 (417) | +0.051 | [+0.033, +0.068] | [+0.033, +0.069] | +0.088 [+0.065, +0.112] |
| E4 | 3 to 10 | c - d | all | 4354 | 970 | 741 (551) | -0.019 | [-0.027, -0.011] | [-0.027, -0.012] | -0.026 [-0.034, -0.018] |
| E4 | 3 to 10 | c - d | P1 | 363 | 303 | 279 (228) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | 3 to 10 | c - d | P2 | 300 | 194 | 178 (115) | -0.007 | [-0.020, +0.006] | [-0.021, +0.006] | -0.006 [-0.016, +0.001] |
| E4 | 3 to 10 | c - d | M1 | 636 | 213 | 198 (127) | -0.002 | [-0.016, +0.013] | [-0.016, +0.013] | -0.003 [-0.016, +0.009] |
| E4 | 3 to 10 | c - d | M2 | 3052 | 718 | 570 (417) | -0.027 | [-0.036, -0.017] | [-0.037, -0.017] | -0.042 [-0.056, -0.030] |
| E4 | 3 to 10 | cs - d | all | 4354 | 970 | 741 (551) | -0.016 | [-0.023, -0.008] | [-0.023, -0.009] | -0.022 [-0.029, -0.014] |
| E4 | 3 to 10 | cs - d | P1 | 363 | 303 | 279 (228) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | 3 to 10 | cs - d | P2 | 300 | 194 | 178 (115) | -0.010 | [-0.025, +0.003] | [-0.026, +0.003] | -0.009 [-0.020, -0.001] |
| E4 | 3 to 10 | cs - d | M1 | 636 | 213 | 198 (127) | +0.000 | [-0.014, +0.015] | [-0.014, +0.014] | -0.000 [-0.012, +0.011] |
| E4 | 3 to 10 | cs - d | M2 | 3052 | 718 | 570 (417) | -0.022 | [-0.032, -0.012] | [-0.033, -0.013] | -0.035 [-0.047, -0.024] |
| E4 | 11 to 30 | c - a | all | 2009 | 161 | 148 (117) | +0.149 | [+0.101, +0.200] | [+0.101, +0.206] | +0.135 [+0.092, +0.183] |
| E4 | 11 to 30 | c - a | P1 | 103 | 49 | 49 (29) | +0.398 | [+0.250, +0.540] | [+0.237, +0.535] | +0.243 [+0.140, +0.350] |
| E4 | 11 to 30 | c - a | P2 | 177 | 65 | 60 (32) | +0.621 | [+0.465, +0.725] | [+0.480, +0.734] | +0.290 [+0.195, +0.406] |
| E4 | 11 to 30 | c - a | M1 | 588 | 60 | 59 (46) | +0.167 | [+0.080, +0.258] | [+0.083, +0.261] | +0.217 [+0.125, +0.314] |
| E4 | 11 to 30 | c - a | M2 | 1138 | 86 | 84 (70) | +0.042 | [+0.015, +0.076] | [+0.015, +0.075] | +0.062 [+0.023, +0.105] |
| E4 | 11 to 30 | c - d | all | 2009 | 161 | 148 (117) | +0.009 | [-0.002, +0.021] | [-0.002, +0.020] | +0.005 [-0.008, +0.018] |
| E4 | 11 to 30 | c - d | P1 | 103 | 49 | 49 (29) | +0.000 | [-0.034, +0.036] | [-0.037, +0.038] | -0.004 [-0.029, +0.016] |
| E4 | 11 to 30 | c - d | P2 | 177 | 65 | 60 (32) | +0.006 | [-0.024, +0.040] | [-0.027, +0.042] | +0.003 [-0.014, +0.024] |
| E4 | 11 to 30 | c - d | M1 | 588 | 60 | 59 (46) | +0.015 | [-0.014, +0.042] | [-0.015, +0.043] | -0.005 [-0.039, +0.023] |
| E4 | 11 to 30 | c - d | M2 | 1138 | 86 | 84 (70) | +0.007 | [-0.005, +0.020] | [-0.006, +0.020] | +0.010 [-0.006, +0.026] |
| E4 | 11 to 30 | cs - d | all | 2009 | 161 | 148 (117) | +0.007 | [-0.004, +0.019] | [-0.004, +0.019] | +0.004 [-0.009, +0.018] |
| E4 | 11 to 30 | cs - d | P1 | 103 | 49 | 49 (29) | +0.010 | [-0.024, +0.041] | [-0.022, +0.042] | -0.002 [-0.027, +0.016] |
| E4 | 11 to 30 | cs - d | P2 | 177 | 65 | 60 (32) | +0.006 | [-0.024, +0.040] | [-0.027, +0.042] | +0.003 [-0.014, +0.024] |
| E4 | 11 to 30 | cs - d | M1 | 588 | 60 | 59 (46) | +0.014 | [-0.016, +0.041] | [-0.019, +0.044] | -0.004 [-0.039, +0.025] |
| E4 | 11 to 30 | cs - d | M2 | 1138 | 86 | 84 (70) | +0.004 | [-0.009, +0.016] | [-0.009, +0.016] | +0.007 [-0.009, +0.021] |
| E4 | 31 to 100 | c - a | all | 986 | 27 | 26 (23) | +0.102 | [+0.033, +0.191] | [+0.028, +0.205] | +0.104 [+0.025, +0.210] |
| E4 | 31 to 100 | c - a | P1 | 33 | 10 | 10 (5) | +0.485 | [+0.267, +0.583] | [+0.267, +0.578] | +0.299 [+0.106, +0.513] |
| E4 | 31 to 100 | c - a | P2 | 33 | 6 | 5 (2) | +0.636 | [+0.000, +0.909] | [+0.000, +0.968] | +0.220 [+0.000, +0.620] |
| E4 | 31 to 100 | c - a | M1 | 120 | 5 | 4 (3) | +0.242 | [-0.000, +0.617] | [+0.000, +0.724] | +0.311 [+0.007, +0.761] |
| E4 | 31 to 100 | c - a | M2 | 799 | 21 | 21 (19) | +0.043 | [+0.007, +0.090] | [+0.009, +0.092] | +0.060 [+0.007, +0.147] |
| E4 | 31 to 100 | c - d | all | 986 | 27 | 26 (23) | +0.006 | [-0.009, +0.021] | [-0.010, +0.020] | +0.006 [-0.009, +0.020] |
| E4 | 31 to 100 | c - d | P1 | 33 | 10 | 10 (5) | +0.091 | [+0.000, +0.225] | [+0.000, +0.220] | +0.033 [+0.000, +0.100] |
| E4 | 31 to 100 | c - d | P2 | 33 | 6 | 5 (2) | -0.030 | [-0.111, +0.000] | [-0.094, +0.000] | -0.020 [-0.060, +0.000] |
| E4 | 31 to 100 | c - d | M1 | 120 | 5 | 4 (3) | +0.033 | [-0.050, +0.080] | [-0.048, +0.081] | +0.028 [-0.053, +0.091] |
| E4 | 31 to 100 | c - d | M2 | 799 | 21 | 21 (19) | +0.000 | [-0.014, +0.011] | [-0.013, +0.011] | -0.001 [-0.011, +0.006] |
| E4 | 31 to 100 | cs - d | all | 986 | 27 | 26 (23) | +0.007 | [-0.001, +0.018] | [-0.002, +0.018] | +0.007 [-0.003, +0.017] |
| E4 | 31 to 100 | cs - d | P1 | 33 | 10 | 10 (5) | +0.091 | [+0.000, +0.225] | [+0.000, +0.220] | +0.033 [+0.000, +0.100] |
| E4 | 31 to 100 | cs - d | P2 | 33 | 6 | 5 (2) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | 31 to 100 | cs - d | M1 | 120 | 5 | 4 (3) | +0.017 | [-0.065, +0.055] | [-0.051, +0.056] | +0.001 [-0.060, +0.047] |
| E4 | 31 to 100 | cs - d | M2 | 799 | 21 | 21 (19) | +0.003 | [+0.000, +0.006] | [+0.000, +0.006] | +0.002 [+0.000, +0.004] |
| E2 | 3 to 10 | c - a | all | 4354 | 970 | 741 (551) | +0.056 | [+0.042, +0.071] | [+0.041, +0.071] | +0.062 [+0.047, +0.078] |
| E2 | 3 to 10 | c - a | P1 | 363 | 303 | 279 (228) | +0.132 | [+0.085, +0.181] | [+0.085, +0.179] | +0.082 [+0.052, +0.113] |
| E2 | 3 to 10 | c - a | P2 | 300 | 194 | 178 (115) | +0.157 | [+0.096, +0.217] | [+0.091, +0.227] | +0.086 [+0.051, +0.126] |
| E2 | 3 to 10 | c - a | M1 | 636 | 213 | 198 (127) | +0.110 | [+0.067, +0.151] | [+0.067, +0.158] | +0.142 [+0.097, +0.192] |
| E2 | 3 to 10 | c - a | M2 | 3052 | 718 | 570 (417) | +0.026 | [+0.011, +0.040] | [+0.011, +0.039] | +0.050 [+0.032, +0.069] |
| E2 | 3 to 10 | c - d | all | 4354 | 970 | 741 (551) | -0.001 | [-0.007, +0.005] | [-0.006, +0.006] | -0.003 [-0.008, +0.002] |
| E2 | 3 to 10 | c - d | P1 | 363 | 303 | 279 (228) | -0.006 | [-0.014, +0.000] | [-0.014, +0.000] | -0.003 [-0.008, +0.000] |
| E2 | 3 to 10 | c - d | P2 | 300 | 194 | 178 (115) | +0.000 | [-0.013, +0.013] | [-0.013, +0.013] | +0.000 [-0.008, +0.009] |
| E2 | 3 to 10 | c - d | M1 | 636 | 213 | 198 (127) | -0.009 | [-0.022, +0.003] | [-0.022, +0.004] | -0.014 [-0.025, -0.004] |
| E2 | 3 to 10 | c - d | M2 | 3052 | 718 | 570 (417) | +0.002 | [-0.007, +0.010] | [-0.007, +0.009] | -0.001 [-0.008, +0.006] |
| E2 | 3 to 10 | cs - d | all | 4354 | 970 | 741 (551) | +0.001 | [-0.005, +0.006] | [-0.005, +0.007] | -0.002 [-0.007, +0.002] |
| E2 | 3 to 10 | cs - d | P1 | 363 | 303 | 279 (228) | -0.006 | [-0.014, +0.000] | [-0.014, +0.000] | -0.003 [-0.008, +0.000] |
| E2 | 3 to 10 | cs - d | P2 | 300 | 194 | 178 (115) | -0.003 | [-0.016, +0.007] | [-0.016, +0.007] | -0.003 [-0.010, +0.003] |
| E2 | 3 to 10 | cs - d | M1 | 636 | 213 | 198 (127) | +0.000 | [-0.011, +0.013] | [-0.011, +0.012] | -0.004 [-0.013, +0.003] |
| E2 | 3 to 10 | cs - d | M2 | 3052 | 718 | 570 (417) | +0.002 | [-0.006, +0.010] | [-0.006, +0.010] | -0.001 [-0.007, +0.006] |
| E2 | 11 to 30 | c - a | all | 2009 | 161 | 148 (117) | +0.095 | [+0.063, +0.124] | [+0.064, +0.128] | +0.107 [+0.071, +0.143] |
| E2 | 11 to 30 | c - a | P1 | 103 | 49 | 49 (29) | +0.466 | [+0.313, +0.610] | [+0.300, +0.619] | +0.295 [+0.176, +0.415] |
| E2 | 11 to 30 | c - a | P2 | 177 | 65 | 60 (32) | +0.418 | [+0.296, +0.531] | [+0.295, +0.527] | +0.227 [+0.145, +0.322] |
| E2 | 11 to 30 | c - a | M1 | 588 | 60 | 59 (46) | +0.075 | [+0.027, +0.125] | [+0.033, +0.128] | +0.109 [+0.050, +0.182] |
| E2 | 11 to 30 | c - a | M2 | 1138 | 86 | 84 (70) | +0.019 | [+0.001, +0.041] | [-0.001, +0.039] | +0.044 [+0.009, +0.080] |
| E2 | 11 to 30 | c - d | all | 2009 | 161 | 148 (117) | +0.012 | [+0.003, +0.024] | [+0.002, +0.022] | +0.015 [+0.005, +0.025] |
| E2 | 11 to 30 | c - d | P1 | 103 | 49 | 49 (29) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | 11 to 30 | c - d | P2 | 177 | 65 | 60 (32) | +0.017 | [-0.006, +0.046] | [-0.007, +0.048] | +0.006 [-0.008, +0.023] |
| E2 | 11 to 30 | c - d | M1 | 588 | 60 | 59 (46) | +0.031 | [+0.008, +0.055] | [+0.008, +0.056] | +0.024 [+0.007, +0.043] |
| E2 | 11 to 30 | c - d | M2 | 1138 | 86 | 84 (70) | +0.004 | [-0.010, +0.016] | [-0.009, +0.016] | +0.008 [-0.007, +0.023] |
| E2 | 11 to 30 | cs - d | all | 2009 | 161 | 148 (117) | +0.008 | [-0.001, +0.018] | [+0.000, +0.018] | +0.011 [+0.002, +0.020] |
| E2 | 11 to 30 | cs - d | P1 | 103 | 49 | 49 (29) | -0.010 | [-0.031, +0.000] | [-0.031, +0.000] | -0.004 [-0.012, +0.000] |
| E2 | 11 to 30 | cs - d | P2 | 177 | 65 | 60 (32) | +0.023 | [-0.005, +0.056] | [-0.005, +0.055] | +0.010 [-0.005, +0.027] |
| E2 | 11 to 30 | cs - d | M1 | 588 | 60 | 59 (46) | +0.017 | [+0.000, +0.035] | [+0.000, +0.037] | +0.013 [+0.001, +0.028] |
| E2 | 11 to 30 | cs - d | M2 | 1138 | 86 | 84 (70) | +0.004 | [-0.008, +0.015] | [-0.007, +0.016] | +0.007 [-0.007, +0.022] |
| E2 | 31 to 100 | c - a | all | 986 | 27 | 26 (23) | +0.060 | [+0.021, +0.110] | [+0.020, +0.114] | +0.059 [+0.020, +0.108] |
| E2 | 31 to 100 | c - a | P1 | 33 | 10 | 10 (5) | +0.667 | [+0.315, +0.796] | [+0.315, +0.793] | +0.377 [+0.142, +0.630] |
| E2 | 31 to 100 | c - a | P2 | 33 | 6 | 5 (2) | +0.121 | [+0.000, +0.145] | [+0.000, +0.145] | +0.050 [+0.000, +0.110] |
| E2 | 31 to 100 | c - a | M1 | 120 | 5 | 4 (3) | +0.050 | [+0.013, +0.080] | [+0.019, +0.081] | +0.051 [+0.016, +0.091] |
| E2 | 31 to 100 | c - a | M2 | 799 | 21 | 21 (19) | +0.033 | [+0.001, +0.072] | [+0.004, +0.070] | +0.036 [+0.003, +0.075] |
| E2 | 31 to 100 | c - d | all | 986 | 27 | 26 (23) | -0.009 | [-0.023, +0.009] | [-0.023, +0.008] | -0.006 [-0.021, +0.013] |
| E2 | 31 to 100 | c - d | P1 | 33 | 10 | 10 (5) | +0.212 | [+0.000, +0.393] | [+0.000, +0.378] | +0.076 [+0.000, +0.187] |
| E2 | 31 to 100 | c - d | P2 | 33 | 6 | 5 (2) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | 31 to 100 | c - d | M1 | 120 | 5 | 4 (3) | +0.017 | [-0.021, +0.038] | [-0.020, +0.040] | +0.016 [-0.026, +0.047] |
| E2 | 31 to 100 | c - d | M2 | 799 | 21 | 21 (19) | -0.023 | [-0.039, -0.009] | [-0.039, -0.009] | -0.021 [-0.035, -0.009] |
| E2 | 31 to 100 | cs - d | all | 986 | 27 | 26 (23) | +0.000 | [-0.010, +0.012] | [-0.010, +0.011] | +0.001 [-0.008, +0.010] |
| E2 | 31 to 100 | cs - d | P1 | 33 | 10 | 10 (5) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | 31 to 100 | cs - d | P2 | 33 | 6 | 5 (2) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | 31 to 100 | cs - d | M1 | 120 | 5 | 4 (3) | +0.058 | [+0.034, +0.078] | [+0.035, +0.078] | +0.054 [+0.037, +0.074] |
| E2 | 31 to 100 | cs - d | M2 | 799 | 21 | 21 (19) | -0.009 | [-0.016, -0.001] | [-0.016, -0.001] | -0.007 [-0.014, -0.001] |

### Secondary: differences on the queries whose folder c does not hold whole (a label keeps more than three files)

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | c differs from d | c - a | all | 5381 | 623 | 512 (266) | +0.025 | [+0.016, +0.036] | [+0.015, +0.036] | +0.020 [+0.007, +0.034] |
| E1 | c differs from d | c - a | P1 | 328 | 204 | 198 (116) | +0.149 | [+0.093, +0.209] | [+0.093, +0.208] | +0.111 [+0.065, +0.160] |
| E1 | c differs from d | c - a | P2 | 352 | 157 | 138 (51) | +0.128 | [+0.062, +0.199] | [+0.067, +0.197] | +0.090 [+0.044, +0.138] |
| E1 | c differs from d | c - a | M1 | 1019 | 136 | 124 (71) | +0.041 | [+0.011, +0.073] | [+0.011, +0.070] | +0.040 [+0.008, +0.074] |
| E1 | c differs from d | c - a | M2 | 3677 | 383 | 335 (185) | -0.000 | [-0.008, +0.009] | [-0.009, +0.009] | -0.006 [-0.017, +0.005] |
| E1 | c differs from d | c - d | all | 5381 | 623 | 512 (266) | +0.006 | [-0.000, +0.012] | [+0.000, +0.012] | -0.002 [-0.011, +0.006] |
| E1 | c differs from d | c - d | P1 | 328 | 204 | 198 (116) | -0.021 | [-0.047, +0.003] | [-0.047, +0.000] | -0.034 [-0.064, -0.007] |
| E1 | c differs from d | c - d | P2 | 352 | 157 | 138 (51) | -0.020 | [-0.039, -0.005] | [-0.037, -0.005] | -0.023 [-0.050, +0.003] |
| E1 | c differs from d | c - d | M1 | 1019 | 136 | 124 (71) | +0.024 | [+0.007, +0.044] | [+0.006, +0.044] | +0.014 [-0.002, +0.031] |
| E1 | c differs from d | c - d | M2 | 3677 | 383 | 335 (185) | +0.005 | [-0.001, +0.011] | [-0.000, +0.011] | +0.004 [-0.002, +0.011] |
| E1 | c differs from d | cs - d | all | 5381 | 623 | 512 (266) | +0.006 | [+0.001, +0.012] | [+0.001, +0.012] | -0.001 [-0.011, +0.007] |
| E1 | c differs from d | cs - d | P1 | 328 | 204 | 198 (116) | -0.024 | [-0.047, +0.000] | [-0.048, -0.003] | -0.030 [-0.063, -0.002] |
| E1 | c differs from d | cs - d | P2 | 352 | 157 | 138 (51) | -0.011 | [-0.029, +0.003] | [-0.028, +0.003] | -0.014 [-0.041, +0.011] |
| E1 | c differs from d | cs - d | M1 | 1019 | 136 | 124 (71) | +0.018 | [+0.003, +0.034] | [+0.003, +0.035] | +0.009 [-0.004, +0.024] |
| E1 | c differs from d | cs - d | M2 | 3677 | 383 | 335 (185) | +0.007 | [+0.001, +0.013] | [+0.002, +0.013] | +0.005 [-0.002, +0.013] |
| E1 | c equals d | c - a | all | 1991 | 621 | 519 (432) | +0.010 | [-0.004, +0.024] | [-0.005, +0.023] | +0.011 [-0.004, +0.026] |
| E1 | c equals d | c - a | P1 | 172 | 159 | 148 (131) | +0.006 | [-0.029, +0.041] | [-0.029, +0.038] | +0.002 [-0.034, +0.036] |
| E1 | c equals d | c - a | P2 | 160 | 109 | 102 (71) | +0.062 | [+0.006, +0.128] | [+0.006, +0.127] | +0.046 [+0.002, +0.093] |
| E1 | c equals d | c - a | M1 | 327 | 143 | 136 (116) | +0.021 | [-0.016, +0.059] | [-0.018, +0.064] | +0.027 [-0.017, +0.073] |
| E1 | c equals d | c - a | M2 | 1330 | 456 | 389 (321) | +0.001 | [-0.017, +0.018] | [-0.016, +0.017] | +0.006 [-0.015, +0.026] |
| E1 | c equals d | c - d | all | 1991 | 621 | 519 (432) | -0.012 | [-0.017, -0.007] | [-0.018, -0.007] | -0.010 [-0.015, -0.005] |
| E1 | c equals d | c - d | P1 | 172 | 159 | 148 (131) | -0.023 | [-0.047, -0.006] | [-0.049, -0.006] | -0.024 [-0.051, -0.003] |
| E1 | c equals d | c - d | P2 | 160 | 109 | 102 (71) | -0.013 | [-0.031, +0.000] | [-0.032, +0.000] | -0.008 [-0.021, +0.000] |
| E1 | c equals d | c - d | M1 | 327 | 143 | 136 (116) | -0.012 | [-0.026, -0.003] | [-0.025, -0.003] | -0.010 [-0.021, -0.002] |
| E1 | c equals d | c - d | M2 | 1330 | 456 | 389 (321) | -0.011 | [-0.017, -0.004] | [-0.017, -0.004] | -0.009 [-0.017, -0.003] |
| E1 | c equals d | cs - d | all | 1991 | 621 | 519 (432) | -0.010 | [-0.015, -0.005] | [-0.015, -0.005] | -0.007 [-0.013, -0.003] |
| E1 | c equals d | cs - d | P1 | 172 | 159 | 148 (131) | -0.017 | [-0.040, +0.000] | [-0.040, +0.000] | -0.017 [-0.041, +0.000] |
| E1 | c equals d | cs - d | P2 | 160 | 109 | 102 (71) | -0.013 | [-0.031, +0.000] | [-0.032, +0.000] | -0.008 [-0.021, +0.000] |
| E1 | c equals d | cs - d | M1 | 327 | 143 | 136 (116) | -0.009 | [-0.021, +0.000] | [-0.020, +0.000] | -0.008 [-0.018, +0.000] |
| E1 | c equals d | cs - d | M2 | 1330 | 456 | 389 (321) | -0.008 | [-0.015, -0.002] | [-0.015, -0.002] | -0.007 [-0.013, -0.001] |
| E4 | c differs from d | c - a | all | 5381 | 623 | 512 (266) | +0.096 | [+0.068, +0.125] | [+0.066, +0.130] | +0.076 [+0.053, +0.097] |
| E4 | c differs from d | c - a | P1 | 328 | 204 | 198 (116) | +0.290 | [+0.218, +0.365] | [+0.214, +0.360] | +0.158 [+0.113, +0.205] |
| E4 | c differs from d | c - a | P2 | 352 | 157 | 138 (51) | +0.452 | [+0.332, +0.564] | [+0.321, +0.575] | +0.193 [+0.137, +0.251] |
| E4 | c differs from d | c - a | M1 | 1019 | 136 | 124 (71) | +0.164 | [+0.101, +0.237] | [+0.094, +0.244] | +0.201 [+0.129, +0.270] |
| E4 | c differs from d | c - a | M2 | 3677 | 383 | 335 (185) | +0.025 | [+0.009, +0.041] | [+0.010, +0.039] | +0.028 [+0.010, +0.047] |
| E4 | c differs from d | c - d | all | 5381 | 623 | 512 (266) | +0.004 | [-0.003, +0.011] | [-0.003, +0.011] | -0.002 [-0.009, +0.004] |
| E4 | c differs from d | c - d | P1 | 328 | 204 | 198 (116) | +0.009 | [-0.010, +0.032] | [-0.010, +0.033] | +0.001 [-0.007, +0.007] |
| E4 | c differs from d | c - d | P2 | 352 | 157 | 138 (51) | +0.000 | [-0.019, +0.019] | [-0.018, +0.023] | +0.000 [-0.008, +0.011] |
| E4 | c differs from d | c - d | M1 | 1019 | 136 | 124 (71) | +0.014 | [-0.006, +0.031] | [-0.005, +0.033] | -0.002 [-0.020, +0.015] |
| E4 | c differs from d | c - d | M2 | 3677 | 383 | 335 (185) | +0.001 | [-0.006, +0.009] | [-0.007, +0.008] | -0.005 [-0.016, +0.005] |
| E4 | c differs from d | cs - d | all | 5381 | 623 | 512 (266) | +0.004 | [-0.002, +0.011] | [-0.003, +0.011] | -0.001 [-0.008, +0.006] |
| E4 | c differs from d | cs - d | P1 | 328 | 204 | 198 (116) | +0.012 | [-0.003, +0.035] | [-0.006, +0.035] | +0.001 [-0.007, +0.008] |
| E4 | c differs from d | cs - d | P2 | 352 | 157 | 138 (51) | +0.000 | [-0.020, +0.019] | [-0.019, +0.021] | -0.003 [-0.014, +0.009] |
| E4 | c differs from d | cs - d | M1 | 1019 | 136 | 124 (71) | +0.011 | [-0.009, +0.030] | [-0.009, +0.032] | -0.002 [-0.019, +0.016] |
| E4 | c differs from d | cs - d | M2 | 3677 | 383 | 335 (185) | +0.002 | [-0.005, +0.009] | [-0.006, +0.009] | -0.003 [-0.014, +0.007] |
| E4 | c equals d | c - a | all | 1991 | 621 | 519 (432) | +0.142 | [+0.115, +0.170] | [+0.112, +0.172] | +0.131 [+0.106, +0.157] |
| E4 | c equals d | c - a | P1 | 172 | 159 | 148 (131) | +0.105 | [+0.048, +0.169] | [+0.043, +0.175] | +0.057 [+0.024, +0.098] |
| E4 | c equals d | c - a | P2 | 160 | 109 | 102 (71) | +0.250 | [+0.159, +0.331] | [+0.143, +0.360] | +0.130 [+0.075, +0.193] |
| E4 | c equals d | c - a | M1 | 327 | 143 | 136 (116) | +0.239 | [+0.162, +0.323] | [+0.162, +0.314] | +0.258 [+0.188, +0.329] |
| E4 | c equals d | c - a | M2 | 1330 | 456 | 389 (321) | +0.109 | [+0.079, +0.138] | [+0.078, +0.141] | +0.130 [+0.098, +0.161] |
| E4 | c equals d | c - d | all | 1991 | 621 | 519 (432) | -0.041 | [-0.051, -0.030] | [-0.051, -0.031] | -0.041 [-0.051, -0.030] |
| E4 | c equals d | c - d | P1 | 172 | 159 | 148 (131) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | c equals d | c - d | P2 | 160 | 109 | 102 (71) | -0.013 | [-0.032, +0.000] | [-0.032, +0.000] | -0.010 [-0.025, +0.000] |
| E4 | c equals d | c - d | M1 | 327 | 143 | 136 (116) | -0.006 | [-0.021, +0.009] | [-0.022, +0.009] | -0.005 [-0.022, +0.011] |
| E4 | c equals d | c - d | M2 | 1330 | 456 | 389 (321) | -0.058 | [-0.072, -0.043] | [-0.073, -0.044] | -0.060 [-0.078, -0.044] |
| E4 | c equals d | cs - d | all | 1991 | 621 | 519 (432) | -0.036 | [-0.046, -0.026] | [-0.045, -0.026] | -0.035 [-0.045, -0.024] |
| E4 | c equals d | cs - d | P1 | 172 | 159 | 148 (131) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | c equals d | cs - d | P2 | 160 | 109 | 102 (71) | -0.013 | [-0.032, +0.000] | [-0.032, +0.000] | -0.010 [-0.025, +0.000] |
| E4 | c equals d | cs - d | M1 | 327 | 143 | 136 (116) | -0.003 | [-0.018, +0.009] | [-0.017, +0.009] | -0.001 [-0.016, +0.012] |
| E4 | c equals d | cs - d | M2 | 1330 | 456 | 389 (321) | -0.051 | [-0.065, -0.038] | [-0.066, -0.038] | -0.051 [-0.068, -0.035] |
| E2 | c differs from d | c - a | all | 5381 | 623 | 512 (266) | +0.060 | [+0.043, +0.077] | [+0.041, +0.078] | +0.056 [+0.037, +0.074] |
| E2 | c differs from d | c - a | P1 | 328 | 204 | 198 (116) | +0.329 | [+0.244, +0.411] | [+0.248, +0.412] | +0.175 [+0.126, +0.226] |
| E2 | c differs from d | c - a | P2 | 352 | 157 | 138 (51) | +0.273 | [+0.192, +0.358] | [+0.192, +0.354] | +0.152 [+0.103, +0.203] |
| E2 | c differs from d | c - a | M1 | 1019 | 136 | 124 (71) | +0.073 | [+0.037, +0.110] | [+0.039, +0.111] | +0.108 [+0.061, +0.160] |
| E2 | c differs from d | c - a | M2 | 3677 | 383 | 335 (185) | +0.011 | [-0.001, +0.025] | [-0.002, +0.024] | +0.008 [-0.011, +0.026] |
| E2 | c differs from d | c - d | all | 5381 | 623 | 512 (266) | +0.006 | [-0.000, +0.013] | [+0.000, +0.013] | +0.003 [-0.003, +0.010] |
| E2 | c differs from d | c - d | P1 | 328 | 204 | 198 (116) | +0.015 | [-0.012, +0.052] | [-0.010, +0.053] | -0.000 [-0.009, +0.009] |
| E2 | c differs from d | c - d | P2 | 352 | 157 | 138 (51) | +0.006 | [-0.009, +0.022] | [-0.008, +0.022] | +0.001 [-0.005, +0.008] |
| E2 | c differs from d | c - d | M1 | 1019 | 136 | 124 (71) | +0.022 | [+0.007, +0.038] | [+0.007, +0.038] | +0.012 [+0.002, +0.023] |
| E2 | c differs from d | c - d | M2 | 3677 | 383 | 335 (185) | +0.001 | [-0.008, +0.009] | [-0.007, +0.009] | +0.005 [-0.004, +0.014] |
| E2 | c differs from d | cs - d | all | 5381 | 623 | 512 (266) | +0.007 | [+0.001, +0.013] | [+0.001, +0.013] | +0.003 [-0.003, +0.009] |
| E2 | c differs from d | cs - d | P1 | 328 | 204 | 198 (116) | -0.009 | [-0.021, +0.000] | [-0.020, +0.000] | -0.005 [-0.012, +0.000] |
| E2 | c differs from d | cs - d | P2 | 352 | 157 | 138 (51) | +0.009 | [-0.008, +0.026] | [-0.006, +0.027] | +0.003 [-0.004, +0.011] |
| E2 | c differs from d | cs - d | M1 | 1019 | 136 | 124 (71) | +0.021 | [+0.008, +0.033] | [+0.008, +0.033] | +0.011 [+0.002, +0.020] |
| E2 | c differs from d | cs - d | M2 | 3677 | 383 | 335 (185) | +0.004 | [-0.003, +0.011] | [-0.003, +0.012] | +0.005 [-0.004, +0.015] |
| E2 | c equals d | c - a | all | 1991 | 621 | 519 (432) | +0.086 | [+0.067, +0.106] | [+0.065, +0.106] | +0.077 [+0.058, +0.096] |
| E2 | c equals d | c - a | P1 | 172 | 159 | 148 (131) | +0.058 | [+0.012, +0.109] | [+0.018, +0.110] | +0.041 [+0.014, +0.074] |
| E2 | c equals d | c - a | P2 | 160 | 109 | 102 (71) | +0.181 | [+0.103, +0.264] | [+0.087, +0.272] | +0.084 [+0.039, +0.134] |
| E2 | c equals d | c - a | M1 | 327 | 143 | 136 (116) | +0.141 | [+0.090, +0.199] | [+0.093, +0.199] | +0.153 [+0.100, +0.213] |
| E2 | c equals d | c - a | M2 | 1330 | 456 | 389 (321) | +0.065 | [+0.043, +0.089] | [+0.042, +0.087] | +0.078 [+0.054, +0.102] |
| E2 | c equals d | c - d | all | 1991 | 621 | 519 (432) | -0.010 | [-0.016, -0.004] | [-0.016, -0.004] | -0.009 [-0.015, -0.003] |
| E2 | c equals d | c - d | P1 | 172 | 159 | 148 (131) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | c equals d | c - d | P2 | 160 | 109 | 102 (71) | +0.006 | [-0.014, +0.025] | [-0.014, +0.027] | +0.002 [-0.012, +0.015] |
| E2 | c equals d | c - d | M1 | 327 | 143 | 136 (116) | -0.024 | [-0.042, -0.006] | [-0.044, -0.006] | -0.021 [-0.037, -0.006] |
| E2 | c equals d | c - d | M2 | 1330 | 456 | 389 (321) | -0.010 | [-0.017, -0.002] | [-0.017, -0.003] | -0.007 [-0.014, -0.002] |
| E2 | c equals d | cs - d | all | 1991 | 621 | 519 (432) | -0.008 | [-0.013, -0.003] | [-0.014, -0.002] | -0.007 [-0.013, -0.001] |
| E2 | c equals d | cs - d | P1 | 172 | 159 | 148 (131) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | c equals d | cs - d | P2 | 160 | 109 | 102 (71) | +0.000 | [-0.019, +0.017] | [-0.019, +0.016] | -0.002 [-0.015, +0.005] |
| E2 | c equals d | cs - d | M1 | 327 | 143 | 136 (116) | -0.012 | [-0.026, +0.003] | [-0.027, +0.000] | -0.010 [-0.023, +0.000] |
| E2 | c equals d | cs - d | M2 | 1330 | 456 | 389 (321) | -0.009 | [-0.016, -0.002] | [-0.016, -0.002] | -0.007 [-0.013, -0.001] |

### Secondary: recall@5 by the number of other files of the query's input group in its folder

| encoder | group | cell | queries | owners | c equals d | R@5 a | R@5 c | R@5 d |
|---|---|---|---:|---:|---:|---:|---:|---:|
| E1 | none | P1 | 274 | 254 | 0.518 | 0.168 | 0.190 | 0.223 |
| E1 | none | P2 | 157 | 141 | 0.395 | 0.185 | 0.191 | 0.204 |
| E1 | 1 or 2 | P1 | 144 | 71 | 0.201 | 0.472 | 0.646 | 0.674 |
| E1 | 1 or 2 | P2 | 160 | 70 | 0.588 | 0.412 | 0.594 | 0.613 |
| E1 | 3 or more | P1 | 82 | 17 | 0.012 | 0.415 | 0.646 | 0.622 |
| E1 | 3 or more | P2 | 195 | 30 | 0.021 | 0.697 | 0.826 | 0.846 |
| E4 | none | P1 | 274 | 254 | 0.518 | 0.000 | 0.000 | 0.000 |
| E4 | none | P2 | 157 | 141 | 0.395 | 0.000 | 0.000 | 0.000 |
| E4 | 1 or 2 | P1 | 144 | 71 | 0.201 | 0.000 | 0.472 | 0.479 |
| E4 | 1 or 2 | P2 | 160 | 70 | 0.588 | 0.025 | 0.438 | 0.450 |
| E4 | 3 or more | P1 | 82 | 17 | 0.012 | 0.000 | 0.549 | 0.500 |
| E4 | 3 or more | P2 | 195 | 30 | 0.021 | 0.072 | 0.754 | 0.754 |
| E2 | none | P1 | 274 | 254 | 0.518 | 0.000 | 0.000 | 0.000 |
| E2 | none | P2 | 157 | 141 | 0.395 | 0.000 | 0.000 | 0.000 |
| E2 | 1 or 2 | P1 | 144 | 71 | 0.201 | 0.062 | 0.507 | 0.521 |
| E2 | 1 or 2 | P2 | 160 | 70 | 0.588 | 0.075 | 0.419 | 0.419 |
| E2 | 3 or more | P1 | 82 | 17 | 0.012 | 0.024 | 0.683 | 0.598 |
| E2 | 3 or more | P2 | 195 | 30 | 0.021 | 0.344 | 0.703 | 0.687 |

### Secondary: c - a by the number of other files of the query's input group in its folder

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | none | c - a | P1 | 274 | 274 | 254 (236) | +0.022 | [-0.007, +0.055] | [-0.007, +0.051] | +0.021 [-0.007, +0.053] |
| E1 | none | c - a | P2 | 157 | 157 | 141 (130) | +0.006 | [-0.019, +0.032] | [-0.020, +0.033] | +0.007 [-0.018, +0.032] |
| E1 | 1 or 2 | c - a | P1 | 144 | 72 | 71 (66) | +0.174 | [+0.084, +0.265] | [+0.088, +0.262] | +0.190 [+0.101, +0.282] |
| E1 | 1 or 2 | c - a | P2 | 160 | 77 | 70 (58) | +0.181 | [+0.099, +0.269] | [+0.099, +0.280] | +0.182 [+0.102, +0.263] |
| E1 | 3 or more | c - a | P1 | 82 | 17 | 17 (13) | +0.232 | [+0.091, +0.378] | [+0.086, +0.376] | +0.201 [+0.073, +0.350] |
| E1 | 3 or more | c - a | P2 | 195 | 32 | 30 (18) | +0.128 | [+0.035, +0.249] | [+0.033, +0.254] | +0.123 [-0.019, +0.262] |
| E4 | none | c - a | P1 | 274 | 274 | 254 (236) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | none | c - a | P2 | 157 | 157 | 141 (130) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E4 | 1 or 2 | c - a | P1 | 144 | 72 | 71 (66) | +0.472 | [+0.369, +0.580] | [+0.360, +0.577] | +0.448 [+0.338, +0.552] |
| E4 | 1 or 2 | c - a | P2 | 160 | 77 | 70 (58) | +0.412 | [+0.304, +0.525] | [+0.298, +0.535] | +0.328 [+0.231, +0.442] |
| E4 | 3 or more | c - a | P1 | 82 | 17 | 17 (13) | +0.549 | [+0.385, +0.674] | [+0.391, +0.674] | +0.498 [+0.331, +0.640] |
| E4 | 3 or more | c - a | P2 | 195 | 32 | 30 (18) | +0.682 | [+0.527, +0.806] | [+0.495, +0.824] | +0.575 [+0.426, +0.713] |
| E2 | none | c - a | P1 | 274 | 274 | 254 (236) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | none | c - a | P2 | 157 | 157 | 141 (130) | +0.000 | [+0.000, +0.000] | [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| E2 | 1 or 2 | c - a | P1 | 144 | 72 | 71 (66) | +0.444 | [+0.343, +0.551] | [+0.331, +0.555] | +0.448 [+0.338, +0.554] |
| E2 | 1 or 2 | c - a | P2 | 160 | 77 | 70 (58) | +0.344 | [+0.242, +0.449] | [+0.240, +0.449] | +0.270 [+0.179, +0.368] |
| E2 | 3 or more | c - a | P1 | 82 | 17 | 17 (13) | +0.659 | [+0.473, +0.789] | [+0.462, +0.788] | +0.558 [+0.363, +0.722] |
| E2 | 3 or more | c - a | P2 | 195 | 32 | 30 (18) | +0.359 | [+0.241, +0.500] | [+0.227, +0.513] | +0.359 [+0.214, +0.491] |

### Secondary: c - a by the depth of the folder in its repository

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | root | c - a | all | 2143 | 350 | 342 (186) | +0.013 | [-0.001, +0.026] | [-0.001, +0.027] | +0.008 [-0.007, +0.025] |
| E1 | root | c - a | P1 | 267 | 198 | 194 (137) | +0.082 | [+0.036, +0.132] | [+0.033, +0.133] | +0.057 [+0.015, +0.100] |
| E1 | root | c - a | P2 | 57 | 27 | 26 (15) | +0.070 | [-0.058, +0.206] | [-0.048, +0.213] | +0.017 [-0.103, +0.141] |
| E1 | depth 1 | c - a | all | 2124 | 304 | 271 (128) | +0.047 | [+0.029, +0.063] | [+0.028, +0.064] | +0.028 [+0.010, +0.046] |
| E1 | depth 1 | c - a | P1 | 120 | 79 | 75 (47) | +0.167 | [+0.074, +0.254] | [+0.071, +0.258] | +0.129 [+0.056, +0.204] |
| E1 | depth 1 | c - a | P2 | 191 | 90 | 85 (46) | +0.183 | [+0.088, +0.286] | [+0.092, +0.293] | +0.132 [+0.069, +0.206] |
| E1 | depth 2 or more | c - a | all | 3105 | 518 | 387 (174) | +0.010 | [-0.003, +0.022] | [-0.002, +0.022] | +0.017 [-0.001, +0.033] |
| E1 | depth 2 or more | c - a | P1 | 113 | 86 | 79 (41) | +0.071 | [-0.019, +0.160] | [-0.017, +0.158] | +0.025 [-0.032, +0.075] |
| E1 | depth 2 or more | c - a | P2 | 264 | 149 | 128 (39) | +0.061 | [+0.015, +0.116] | [+0.011, +0.119] | +0.044 [+0.005, +0.087] |
| E4 | root | c - a | all | 2143 | 350 | 342 (186) | +0.103 | [+0.072, +0.135] | [+0.074, +0.135] | +0.100 [+0.072, +0.129] |
| E4 | root | c - a | P1 | 267 | 198 | 194 (137) | +0.202 | [+0.133, +0.275] | [+0.137, +0.270] | +0.101 [+0.065, +0.143] |
| E4 | root | c - a | P2 | 57 | 27 | 26 (15) | +0.544 | [+0.361, +0.690] | [+0.340, +0.689] | +0.310 [+0.160, +0.471] |
| E4 | depth 1 | c - a | all | 2124 | 304 | 271 (128) | +0.135 | [+0.100, +0.175] | [+0.093, +0.177] | +0.124 [+0.085, +0.166] |
| E4 | depth 1 | c - a | P1 | 120 | 79 | 75 (47) | +0.308 | [+0.193, +0.411] | [+0.202, +0.418] | +0.195 [+0.122, +0.281] |
| E4 | depth 1 | c - a | P2 | 191 | 90 | 85 (46) | +0.377 | [+0.232, +0.502] | [+0.221, +0.508] | +0.177 [+0.102, +0.256] |
| E4 | depth 2 or more | c - a | all | 3105 | 518 | 387 (174) | +0.095 | [+0.063, +0.135] | [+0.055, +0.144] | +0.077 [+0.054, +0.099] |
| E4 | depth 2 or more | c - a | P1 | 113 | 86 | 79 (41) | +0.195 | [+0.053, +0.348] | [+0.050, +0.325] | +0.069 [+0.024, +0.119] |
| E4 | depth 2 or more | c - a | P2 | 264 | 149 | 128 (39) | +0.364 | [+0.216, +0.502] | [+0.201, +0.524] | +0.136 [+0.085, +0.191] |
| E2 | root | c - a | all | 2143 | 350 | 342 (186) | +0.066 | [+0.042, +0.093] | [+0.043, +0.093] | +0.058 [+0.035, +0.081] |
| E2 | root | c - a | P1 | 267 | 198 | 194 (137) | +0.210 | [+0.141, +0.279] | [+0.139, +0.278] | +0.103 [+0.065, +0.144] |
| E2 | root | c - a | P2 | 57 | 27 | 26 (15) | +0.474 | [+0.298, +0.600] | [+0.298, +0.598] | +0.262 [+0.125, +0.403] |
| E2 | depth 1 | c - a | all | 2124 | 304 | 271 (128) | +0.089 | [+0.064, +0.116] | [+0.062, +0.119] | +0.079 [+0.055, +0.104] |
| E2 | depth 1 | c - a | P1 | 120 | 79 | 75 (47) | +0.300 | [+0.168, +0.419] | [+0.180, +0.419] | +0.202 [+0.122, +0.295] |
| E2 | depth 1 | c - a | P2 | 191 | 90 | 85 (46) | +0.267 | [+0.153, +0.372] | [+0.147, +0.379] | +0.127 [+0.067, +0.193] |
| E2 | depth 2 or more | c - a | all | 3105 | 518 | 387 (174) | +0.052 | [+0.035, +0.072] | [+0.034, +0.070] | +0.058 [+0.038, +0.078] |
| E2 | depth 2 or more | c - a | P1 | 113 | 86 | 79 (41) | +0.230 | [+0.045, +0.404] | [+0.044, +0.397] | +0.071 [+0.022, +0.130] |
| E2 | depth 2 or more | c - a | P2 | 264 | 149 | 128 (39) | +0.178 | [+0.111, +0.254] | [+0.104, +0.250] | +0.095 [+0.051, +0.142] |

### Secondary: the other rows with owner-clustered intervals

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | all | tb2c - c | all | 7372 | 1172 | 858 (419) | +0.009 | [+0.002, +0.016] | [+0.002, +0.016] | +0.027 [+0.020, +0.036] |
| E1 | all | tb2c - c | P1 | 500 | 363 | 334 (205) | +0.006 | [-0.033, +0.044] | [-0.034, +0.046] | +0.037 [+0.000, +0.073] |
| E1 | all | tb2c - c | P2 | 512 | 266 | 231 (93) | +0.074 | [+0.043, +0.110] | [+0.042, +0.111] | +0.116 [+0.072, +0.156] |
| E1 | all | tb2c - c | M1 | 1346 | 279 | 250 (114) | -0.026 | [-0.047, -0.008] | [-0.046, -0.007] | -0.009 [-0.030, +0.009] |
| E1 | all | tb2c - c | M2 | 5007 | 837 | 647 (296) | +0.012 | [+0.005, +0.020] | [+0.005, +0.020] | +0.033 [+0.023, +0.044] |
| E1 | all | c - tbc | all | 7372 | 1172 | 858 (419) | -0.001 | [-0.003, +0.001] | [-0.003, +0.001] | -0.001 [-0.002, +0.001] |
| E1 | all | c - tbc | P1 | 500 | 363 | 334 (205) | +0.002 | [-0.008, +0.012] | [-0.008, +0.012] | -0.005 [-0.014, +0.003] |
| E1 | all | c - tbc | P2 | 512 | 266 | 231 (93) | -0.010 | [-0.020, -0.002] | [-0.020, -0.002] | -0.008 [-0.017, -0.001] |
| E1 | all | c - tbc | M1 | 1346 | 279 | 250 (114) | -0.001 | [-0.008, +0.005] | [-0.009, +0.005] | +0.001 [-0.003, +0.006] |
| E1 | all | c - tbc | M2 | 5007 | 837 | 647 (296) | -0.000 | [-0.002, +0.001] | [-0.002, +0.001] | +0.001 [-0.001, +0.002] |
| E1 | all | cc - c | all | 7372 | 1172 | 858 (419) | +0.011 | [+0.005, +0.017] | [+0.005, +0.017] | +0.025 [+0.018, +0.031] |
| E1 | all | cc - c | P1 | 500 | 363 | 334 (205) | +0.028 | [+0.000, +0.057] | [-0.004, +0.060] | +0.046 [+0.013, +0.077] |
| E1 | all | cc - c | P2 | 512 | 266 | 231 (93) | +0.070 | [+0.043, +0.100] | [+0.046, +0.100] | +0.105 [+0.068, +0.145] |
| E1 | all | cc - c | M1 | 1346 | 279 | 250 (114) | -0.018 | [-0.037, +0.000] | [-0.036, -0.001] | +0.008 [-0.005, +0.023] |
| E1 | all | cc - c | M2 | 5007 | 837 | 647 (296) | +0.011 | [+0.005, +0.016] | [+0.005, +0.017] | +0.025 [+0.016, +0.033] |
| E1 | all | dc - d | all | 7372 | 1172 | 858 (419) | +0.015 | [+0.011, +0.019] | [+0.010, +0.019] | +0.019 [+0.013, +0.026] |
| E1 | all | dc - d | P1 | 500 | 363 | 334 (205) | +0.030 | [+0.002, +0.060] | [+0.002, +0.059] | +0.035 [+0.002, +0.068] |
| E1 | all | dc - d | P2 | 512 | 266 | 231 (93) | +0.059 | [+0.035, +0.085] | [+0.036, +0.084] | +0.097 [+0.061, +0.134] |
| E1 | all | dc - d | M1 | 1346 | 279 | 250 (114) | +0.007 | [-0.002, +0.017] | [-0.003, +0.017] | +0.010 [-0.003, +0.027] |
| E1 | all | dc - d | M2 | 5007 | 837 | 647 (296) | +0.011 | [+0.007, +0.015] | [+0.007, +0.015] | +0.017 [+0.010, +0.024] |
| E1 | all | ac - a | all | 7372 | 1172 | 858 (419) | +0.016 | [+0.007, +0.024] | [+0.006, +0.023] | +0.035 [+0.026, +0.043] |
| E1 | all | ac - a | P1 | 500 | 363 | 334 (205) | +0.074 | [+0.046, +0.102] | [+0.045, +0.105] | +0.090 [+0.058, +0.122] |
| E1 | all | ac - a | P2 | 512 | 266 | 231 (93) | +0.100 | [+0.066, +0.138] | [+0.065, +0.140] | +0.115 [+0.073, +0.156] |
| E1 | all | ac - a | M1 | 1346 | 279 | 250 (114) | -0.027 | [-0.064, +0.002] | [-0.063, +0.002] | +0.009 [-0.010, +0.030] |
| E1 | all | ac - a | M2 | 5007 | 837 | 647 (296) | +0.013 | [+0.007, +0.018] | [+0.007, +0.019] | +0.032 [+0.022, +0.043] |
| E4 | all | tb2c - c | all | 7372 | 1172 | 858 (419) | +0.009 | [+0.001, +0.017] | [+0.001, +0.018] | +0.035 [+0.025, +0.044] |
| E4 | all | tb2c - c | P1 | 500 | 363 | 334 (205) | -0.056 | [-0.090, -0.024] | [-0.091, -0.025] | -0.031 [-0.051, -0.014] |
| E4 | all | tb2c - c | P2 | 512 | 266 | 231 (93) | +0.016 | [-0.004, +0.036] | [-0.002, +0.038] | +0.013 [+0.001, +0.029] |
| E4 | all | tb2c - c | M1 | 1346 | 279 | 250 (114) | -0.015 | [-0.035, +0.007] | [-0.034, +0.005] | +0.011 [-0.009, +0.031] |
| E4 | all | tb2c - c | M2 | 5007 | 837 | 647 (296) | +0.022 | [+0.012, +0.031] | [+0.012, +0.032] | +0.055 [+0.041, +0.071] |
| E4 | all | c - tbc | all | 7372 | 1172 | 858 (419) | +0.001 | [-0.002, +0.005] | [-0.002, +0.005] | -0.000 [-0.004, +0.003] |
| E4 | all | c - tbc | P1 | 500 | 363 | 334 (205) | -0.002 | [-0.022, +0.014] | [-0.019, +0.014] | -0.001 [-0.009, +0.006] |
| E4 | all | c - tbc | P2 | 512 | 266 | 231 (93) | +0.004 | [-0.006, +0.015] | [-0.006, +0.015] | +0.002 [-0.002, +0.005] |
| E4 | all | c - tbc | M1 | 1346 | 279 | 250 (114) | +0.010 | [+0.000, +0.020] | [+0.000, +0.021] | +0.006 [-0.003, +0.015] |
| E4 | all | c - tbc | M2 | 5007 | 837 | 647 (296) | -0.001 | [-0.004, +0.002] | [-0.004, +0.003] | -0.000 [-0.004, +0.004] |
| E4 | all | cc - c | all | 7372 | 1172 | 858 (419) | +0.012 | [+0.004, +0.019] | [+0.005, +0.020] | +0.034 [+0.026, +0.042] |
| E4 | all | cc - c | P1 | 500 | 363 | 334 (205) | -0.006 | [-0.025, +0.008] | [-0.024, +0.010] | -0.000 [-0.006, +0.006] |
| E4 | all | cc - c | P2 | 512 | 266 | 231 (93) | +0.021 | [+0.000, +0.045] | [+0.000, +0.045] | +0.013 [+0.001, +0.024] |
| E4 | all | cc - c | M1 | 1346 | 279 | 250 (114) | -0.004 | [-0.021, +0.014] | [-0.021, +0.013] | +0.018 [+0.003, +0.036] |
| E4 | all | cc - c | M2 | 5007 | 837 | 647 (296) | +0.018 | [+0.008, +0.027] | [+0.008, +0.028] | +0.049 [+0.038, +0.061] |
| E4 | all | dc - d | all | 7372 | 1172 | 858 (419) | +0.008 | [+0.004, +0.011] | [+0.004, +0.011] | +0.008 [+0.003, +0.012] |
| E4 | all | dc - d | P1 | 500 | 363 | 334 (205) | +0.002 | [-0.004, +0.009] | [-0.004, +0.009] | +0.000 [-0.004, +0.005] |
| E4 | all | dc - d | P2 | 512 | 266 | 231 (93) | +0.006 | [-0.002, +0.015] | [-0.002, +0.015] | +0.003 [-0.004, +0.010] |
| E4 | all | dc - d | M1 | 1346 | 279 | 250 (114) | +0.021 | [+0.010, +0.033] | [+0.010, +0.032] | +0.014 [+0.002, +0.027] |
| E4 | all | dc - d | M2 | 5007 | 837 | 647 (296) | +0.005 | [+0.000, +0.009] | [+0.000, +0.010] | +0.009 [+0.003, +0.015] |
| E4 | all | ac - a | all | 7372 | 1172 | 858 (419) | +0.084 | [+0.066, +0.100] | [+0.065, +0.106] | +0.114 [+0.100, +0.129] |
| E4 | all | ac - a | P1 | 500 | 363 | 334 (205) | +0.060 | [+0.028, +0.100] | [+0.026, +0.099] | +0.029 [+0.014, +0.048] |
| E4 | all | ac - a | P2 | 512 | 266 | 231 (93) | +0.279 | [+0.187, +0.361] | [+0.179, +0.385] | +0.109 [+0.077, +0.145] |
| E4 | all | ac - a | M1 | 1346 | 279 | 250 (114) | +0.081 | [+0.027, +0.135] | [+0.030, +0.139] | +0.164 [+0.119, +0.212] |
| E4 | all | ac - a | M2 | 5007 | 837 | 647 (296) | +0.066 | [+0.052, +0.082] | [+0.052, +0.082] | +0.136 [+0.115, +0.157] |
| E2 | all | tb2c - c | all | 7372 | 1172 | 858 (419) | +0.001 | [-0.007, +0.010] | [-0.007, +0.009] | +0.020 [+0.010, +0.029] |
| E2 | all | tb2c - c | P1 | 500 | 363 | 334 (205) | -0.034 | [-0.077, +0.002] | [-0.074, +0.005] | +0.005 [-0.018, +0.029] |
| E2 | all | tb2c - c | P2 | 512 | 266 | 231 (93) | -0.004 | [-0.037, +0.030] | [-0.037, +0.031] | +0.035 [+0.003, +0.068] |
| E2 | all | tb2c - c | M1 | 1346 | 279 | 250 (114) | -0.007 | [-0.031, +0.013] | [-0.028, +0.015] | +0.022 [+0.000, +0.045] |
| E2 | all | tb2c - c | M2 | 5007 | 837 | 647 (296) | +0.008 | [-0.001, +0.017] | [-0.001, +0.017] | +0.028 [+0.015, +0.041] |
| E2 | all | c - tbc | all | 7372 | 1172 | 858 (419) | -0.001 | [-0.003, +0.002] | [-0.003, +0.002] | +0.001 [-0.002, +0.003] |
| E2 | all | c - tbc | P1 | 500 | 363 | 334 (205) | -0.002 | [-0.016, +0.014] | [-0.014, +0.013] | -0.002 [-0.006, +0.001] |
| E2 | all | c - tbc | P2 | 512 | 266 | 231 (93) | +0.006 | [-0.002, +0.014] | [-0.002, +0.015] | +0.003 [-0.001, +0.007] |
| E2 | all | c - tbc | M1 | 1346 | 279 | 250 (114) | -0.004 | [-0.010, +0.002] | [-0.010, +0.002] | -0.003 [-0.010, +0.002] |
| E2 | all | c - tbc | M2 | 5007 | 837 | 647 (296) | -0.000 | [-0.003, +0.003] | [-0.003, +0.003] | +0.001 [-0.002, +0.004] |
| E2 | all | cc - c | all | 7372 | 1172 | 858 (419) | +0.009 | [+0.002, +0.014] | [+0.002, +0.015] | +0.019 [+0.012, +0.026] |
| E2 | all | cc - c | P1 | 500 | 363 | 334 (205) | +0.010 | [-0.023, +0.035] | [-0.020, +0.036] | +0.020 [+0.007, +0.034] |
| E2 | all | cc - c | P2 | 512 | 266 | 231 (93) | +0.041 | [+0.020, +0.064] | [+0.019, +0.064] | +0.055 [+0.028, +0.083] |
| E2 | all | cc - c | M1 | 1346 | 279 | 250 (114) | -0.002 | [-0.021, +0.016] | [-0.019, +0.016] | +0.025 [+0.009, +0.042] |
| E2 | all | cc - c | M2 | 5007 | 837 | 647 (296) | +0.008 | [+0.001, +0.015] | [+0.001, +0.015] | +0.018 [+0.008, +0.026] |
| E2 | all | dc - d | all | 7372 | 1172 | 858 (419) | +0.013 | [+0.009, +0.017] | [+0.009, +0.018] | +0.013 [+0.007, +0.018] |
| E2 | all | dc - d | P1 | 500 | 363 | 334 (205) | +0.028 | [+0.013, +0.045] | [+0.013, +0.044] | +0.025 [+0.010, +0.042] |
| E2 | all | dc - d | P2 | 512 | 266 | 231 (93) | +0.021 | [+0.006, +0.040] | [+0.007, +0.039] | +0.031 [+0.012, +0.054] |
| E2 | all | dc - d | M1 | 1346 | 279 | 250 (114) | +0.023 | [+0.014, +0.033] | [+0.015, +0.032] | +0.025 [+0.013, +0.039] |
| E2 | all | dc - d | M2 | 5007 | 837 | 647 (296) | +0.008 | [+0.003, +0.014] | [+0.003, +0.014] | +0.009 [+0.001, +0.017] |
| E2 | all | ac - a | all | 7372 | 1172 | 858 (419) | +0.054 | [+0.040, +0.066] | [+0.040, +0.067] | +0.083 [+0.071, +0.095] |
| E2 | all | ac - a | P1 | 500 | 363 | 334 (205) | +0.150 | [+0.103, +0.198] | [+0.107, +0.199] | +0.098 [+0.071, +0.128] |
| E2 | all | ac - a | P2 | 512 | 266 | 231 (93) | +0.182 | [+0.135, +0.227] | [+0.134, +0.232] | +0.133 [+0.097, +0.173] |
| E2 | all | ac - a | M1 | 1346 | 279 | 250 (114) | +0.038 | [-0.011, +0.083] | [-0.011, +0.086] | +0.132 [+0.090, +0.174] |
| E2 | all | ac - a | M2 | 5007 | 837 | 647 (296) | +0.035 | [+0.026, +0.044] | [+0.026, +0.043] | +0.080 [+0.065, +0.096] |

### Secondary: the loss compared between encoders on the same queries, (c - a) under X minus (c - a) under Y

| pair | cell | point | directory 95% | owner-clustered 95% |
|---|---|---:|---|---|
| E4 - E1 | P1 | +0.126 | [+0.072, +0.181] | [+0.070, +0.182] |
| E4 - E1 | P2 | +0.281 | [+0.175, +0.371] | [+0.167, +0.398] |
| E2 - E1 | P1 | +0.136 | [+0.080, +0.192] | [+0.078, +0.193] |
| E2 - E1 | P2 | +0.137 | [+0.071, +0.199] | [+0.072, +0.201] |

