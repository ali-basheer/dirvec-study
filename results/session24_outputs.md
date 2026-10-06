# Session 24 outputs, verbatim

Written by scripts/s24_run.sh on the pod, 2026-10-05T07:59Z, repo commit 15cc35a.
Nothing here is edited. scripts/s19.py printed the tables, so its headings and test names say session 19 and H19:
on this draw they are the session 24 tests, H24a for H19a, H24b for H19b, H24c for H19c and H24d for H19d.
The verdicts and the reading are in results/session24.md.

## Run log

```
04:42:07 start, commit 53d3bfb
04:42:07 pool, round 1: at least 13000 usable repositories (session 19's 5,517 included)
pool done: 35516 repositories, 13193 usable, 33 days
05:11:52 harvest, round 1
harvest done (full): 2000 mixed, 600 other directories, 21854 files
harvest log of this session: 8307 repositories, {'ok': 8303, 'oversize': 4}
06:03:07 manifest
manifest: 21854 files, 2600 dirs; modality counts {'image': 9008, 'text': 11813, 'table': 316, 'other': 262, 'pdf_text': 277, 'pdf_scanned': 178}
notes: {'image unreadable': 82, 'pdfinfo failed': 7}
06:03:25 ground truth
06:04:58 commit history
history done: 1885 repositories read now, 18240 qualifying commits, 0 failed
commit-subject queries: 1827 over 845 directories, from 18240 qualifying commits in 1361 directories (12877 dropped by the rules, 197 repeated within a directory, 3339 beyond three per directory).
06:07:44 corpus files pushed
06:07:53 manifest rows 21854; files missing or of another size 0
06:07:53 E1: embed all files
07:53:47 E1: { "files": 21854, "ok": 20924, "skipped": {  "image smaller than 28 px (16x16)": 194,  "image smaller than 28 px (21x21)": 3,  "image smaller than 28 px (1x1)": 147,  "empty text": 9,  "no encoder path for modality other ext png": 72,  "image smaller than 28 px (16x15)": 2,  "image smaller than 28 p
07:53:47 E1: eval
12951 eval queries (348 dropped, no vector: {'image': 119, 'other': 229}; 3234 in calibration directories), 2600 directories ranked
  rep a done
  rep ac done
  rep c done
  rep cc done
  rep d done
  rep dc done
  rep tb2c done
  rep tbc done
  rep cs done
07:57:32 E1: commit-subject queries
You have video processor config saved in `preprocessor.json` file which is deprecated. Video processor configs should be saved in their own `video_preprocessor.json` file. You can rename the file or load and save the processor back which renames it automatically. Loading from `preprocessor.json` will be removed in v5.0.
Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]Loading checkpoint shards:  50%|█████     | 1/2 [00:01<00:01,  1.16s/it]Loading checkpoint shards: 100%|██████████| 2/2 [00:01<00:00,  1.32it/s]Loading checkpoint shards: 100%|██████████| 2/2 [00:01<00:00,  1.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:01<00:00,  1.24s/it]Encoding texts...: 100%|██████████| 1/1 [00:01<00:00,  1.24s/it]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 13.32it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.82it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.90it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.85it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.04it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.84it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.80it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.49it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.27it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.42it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.55it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.96it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.33it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.97it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.97it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.31it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.57it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.64it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.74it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.92it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 10.59it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.32it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 13.81it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.86it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.93it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.94it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.99it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.03it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.61it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.68it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.27it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.64it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.07it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.51it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.84it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.01it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.25it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.16it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.62it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.25it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.97it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.69it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.11it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.71it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 10.53it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.57it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.36it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.65it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.97it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.92it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.73it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.50it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.04it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.75it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.21it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.35it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.19it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.55it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.92it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.73it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.51it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.12it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.52it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.61it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.04it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.66it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.99it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.63it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 20.96it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.57it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.33it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.00it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.73it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.94it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.57it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.12it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.60it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.56it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.23it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.26it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.90it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.15it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.92it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.26it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.98it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.11it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.69it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.70it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.13it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.87it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.45it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.71it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.97it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.56it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.95it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.25it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.75it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.27it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.06it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.25it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.48it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.00it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.26it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.54it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.54it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.32it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.52it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 12.98it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.94it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.92it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 13.44it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.21it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.66it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.60it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.96it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.71it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00,  8.83it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00,  8.52it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.68it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.21it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.16it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.30it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.52it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.89it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.50it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.46it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.72it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.83it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.88it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.92it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.62it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.09it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.99it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.17it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.10it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.08it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.19it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.15it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.67it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 13.85it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 10.91it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.00it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.60it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.14it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.93it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 22.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.86it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 16.68it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.20it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.05it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.08it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.19it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 26.18it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.69it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.69it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 21.56it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 25.22it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.19it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 17.16it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 24.02it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 23.33it/s]
Encoding texts...:   0%|          | 0/1 [00:00<?, ?it/s]Encoding texts...: 100%|██████████| 1/1 [00:00<00:00, 27.22it/s]
1827 commit-subject queries embedded in 13s -> /workspace/dirvec/data/emb/jina-embeddings-v4_s24/commitq_s24.npz
```

## Session 19 corpus

Pool: 33 days read, 54 search intervals (0 flagged incomplete by the API, 2 returned fewer rows than their count), 35516 repositories with at least 5 stars, 13193 usable (not a fork, a licence of the list, at most 200 MB).
Not usable: licence None 17034, licence GPL-3.0 2153, licence NOASSERTION 1545, size 362, licence AGPL-3.0 355, licence GPL-2.0 287, licence MPL-2.0 126, licence LGPL-3.0 119, licence MIT-0 78, licence LGPL-2.1 56, licence CC-BY-SA-4.0 42, licence WTFPL 29.
Usable by licence: MIT 9499, Apache-2.0 2713, BSD-3-Clause 442, Unlicense 168, CC0-1.0 134, BSD-2-Clause 106, CC-BY-4.0 60, ISC 59, 0BSD 12.

Harvest: 8307 repositories read (ok 8303, oversize 4); 6878 hold an eligible directory, 1610 a mixed one, 1885 gave a directory to the scored set.

Eligible directories listed in the harvested repositories: 65984; mixed (an image file and another kept file): 3286, 0.050.
Per repository with an eligible directory (6878): mean share of mixed directories 0.094; repositories with at least one mixed directory 1610.

| eligible directories | all | mixed | share mixed |
|---|---:|---:|---:|
| all | 65984 | 3286 | 0.050 |
| root | 5174 | 652 | 0.126 |
| depth 1 | 8115 | 528 | 0.065 |
| depth 2 or more | 52695 | 2106 | 0.040 |
| 3 to 10 kept files | 55552 | 2677 | 0.048 |
| 11 to 30 kept files | 8733 | 503 | 0.058 |
| 31 to 100 kept files | 1699 | 106 | 0.062 |

Scored set: 2600 directories (2000 mixed by extension, 600 other), 21854 files, 1885 repositories, 1826 owners.
By depth: root 789, depth 1 601, depth 2 or more 1210. By kept files: 3 to 10 2088, 11 to 30 431, 31 to 100 81.
Licences: MIT 1889, Apache-2.0 522, BSD-3-Clause 87, CC0-1.0 28, Unlicense 26, BSD-2-Clause 22, CC-BY-4.0 20, ISC 6.
Languages (GitHub's label, ten most frequent): Python 561, JavaScript 327, TypeScript 271, C++ 133, Dart 131, Java 120, C# 114, Jupyter Notebook 113, HTML 102, None 83.
Repository creation year: 2016 268, 2017 102, 2018 50, 2019 457, 2020 172, 2021 175, 2022 661, 2023 325, 2024 251, 2025 139.

Manifest: 21854 files in 2600 directories; modality text 11813, image 9008, table 316, pdf_text 277, other 262, pdf_scanned 178.
Directories per image-fraction bucket: [0,.2) 943, [.2,.5) 772, [.5,.8) 510, [.8,1] 375. Directories with both input groups in the manifest: 1976.

## build_gt.py report

```
{
 "queries": 16533,
 "qualifying_dirs": 2401,
 "qualifying_dirs_per_bucket": {
  "[0,.2)": 932,
  "[.2,.5)": 716,
  "[.5,.8)": 447,
  "[.8,1]": 306
 },
 "queries_per_bucket": {
  "[0,.2)": 7992,
  "[.2,.5)": 3586,
  "[.5,.8)": 2271,
  "[.8,1]": 2684
 },
 "queries_per_modality": {
  "image": 5065,
  "text": 10550,
  "table": 301,
  "other": 250,
  "pdf_text": 246,
  "pdf_scanned": 121
 },
 "dedupe": {
  "exact_files": 2706,
  "exact_pairs": 26241,
  "exact_pairs_cross_dir": 25717,
  "exact_pairs_within_dir": 524,
  "files_excluded_as_queries_degenerate_image": 351,
  "files_excluded_as_queries_dup": 5139,
  "files_phashed": 8834,
  "files_simhashed": 11582,
  "image_files": 3649,
  "image_pairs": 165624,
  "image_pairs_cross_dir": 152522,
  "image_pairs_within_dir": 13102,
  "text_files": 1124,
  "text_pairs": 5420,
  "text_pairs_cross_dir": 5213,
  "text_pairs_within_dir": 207
 },
 "kill_criterion_passed": true
}
```

## Commit-subject queries, build

```
commit-subject queries: 1827 over 845 directories, from 18240 qualifying commits in 1361 directories (12877 dropped by the rules, 197 repeated within a directory, 3339 beyond three per directory).
```

## E1: eval.py

Model: jina-embeddings-v4. Queries: 12951 over 1923 directories; 2600 directories ranked (random recall@k = k/2600). Queries dropped for lack of a vector: 348 {'image': 119, 'other': 229}. Queries in calibration directories, not used: 3234.

Mean representative vectors per directory: a 1.00, ac 1.00, c 3.90, cc 3.90, d 8.05, dc 8.05, tb2c 2.00, tbc 3.90, cs 4.21.

### All queries

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| all | 12951 | 1923 | a | 0.629 | 0.723 | 0.752 | 0.787 | [0.739, 0.766] |
| all | 12951 | 1923 | ac | 0.647 | 0.742 | 0.770 | 0.809 | [0.757, 0.783] |
| all | 12951 | 1923 | c | 0.666 | 0.752 | 0.780 | 0.809 | [0.767, 0.793] |
| all | 12951 | 1923 | cc | 0.674 | 0.767 | 0.793 | 0.824 | [0.781, 0.806] |
| all | 12951 | 1923 | d | 0.664 | 0.757 | 0.780 | 0.812 | [0.768, 0.793] |
| all | 12951 | 1923 | dc | 0.675 | 0.771 | 0.798 | 0.826 | [0.786, 0.810] |
| all | 12951 | 1923 | tb2c | 0.662 | 0.760 | 0.784 | 0.817 | [0.772, 0.797] |
| all | 12951 | 1923 | tbc | 0.665 | 0.752 | 0.779 | 0.810 | [0.766, 0.792] |
| all | 12951 | 1923 | cs | 0.668 | 0.755 | 0.780 | 0.811 | [0.767, 0.792] |

### Per image_frac bucket, all query modalities

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| [0,.2) | 6177 | 745 | a | 0.736 | 0.820 | 0.844 | 0.872 | [0.827, 0.858] |
| [0,.2) | 6177 | 745 | ac | 0.738 | 0.824 | 0.850 | 0.879 | [0.834, 0.864] |
| [0,.2) | 6177 | 745 | c | 0.733 | 0.823 | 0.847 | 0.872 | [0.833, 0.861] |
| [0,.2) | 6177 | 745 | cc | 0.739 | 0.833 | 0.854 | 0.879 | [0.840, 0.867] |
| [0,.2) | 6177 | 745 | d | 0.728 | 0.826 | 0.846 | 0.874 | [0.832, 0.860] |
| [0,.2) | 6177 | 745 | dc | 0.734 | 0.834 | 0.857 | 0.881 | [0.843, 0.870] |
| [0,.2) | 6177 | 745 | tb2c | 0.735 | 0.827 | 0.847 | 0.873 | [0.830, 0.861] |
| [0,.2) | 6177 | 745 | tbc | 0.732 | 0.821 | 0.845 | 0.872 | [0.831, 0.859] |
| [0,.2) | 6177 | 745 | cs | 0.733 | 0.822 | 0.847 | 0.873 | [0.832, 0.860] |
| [.2,.5) | 2957 | 573 | a | 0.522 | 0.619 | 0.648 | 0.689 | [0.617, 0.677] |
| [.2,.5) | 2957 | 573 | ac | 0.565 | 0.662 | 0.688 | 0.730 | [0.662, 0.716] |
| [.2,.5) | 2957 | 573 | c | 0.586 | 0.670 | 0.694 | 0.726 | [0.664, 0.723] |
| [.2,.5) | 2957 | 573 | cc | 0.607 | 0.698 | 0.727 | 0.760 | [0.700, 0.755] |
| [.2,.5) | 2957 | 573 | d | 0.590 | 0.678 | 0.701 | 0.736 | [0.671, 0.729] |
| [.2,.5) | 2957 | 573 | dc | 0.600 | 0.699 | 0.727 | 0.754 | [0.699, 0.755] |
| [.2,.5) | 2957 | 573 | tb2c | 0.591 | 0.688 | 0.714 | 0.748 | [0.687, 0.742] |
| [.2,.5) | 2957 | 573 | tbc | 0.582 | 0.670 | 0.696 | 0.727 | [0.665, 0.725] |
| [.2,.5) | 2957 | 573 | cs | 0.587 | 0.672 | 0.694 | 0.727 | [0.663, 0.723] |
| [.5,.8) | 1832 | 354 | a | 0.431 | 0.540 | 0.583 | 0.626 | [0.539, 0.624] |
| [.5,.8) | 1832 | 354 | ac | 0.492 | 0.599 | 0.639 | 0.697 | [0.600, 0.680] |
| [.5,.8) | 1832 | 354 | c | 0.574 | 0.652 | 0.677 | 0.718 | [0.635, 0.716] |
| [.5,.8) | 1832 | 354 | cc | 0.601 | 0.686 | 0.718 | 0.751 | [0.680, 0.752] |
| [.5,.8) | 1832 | 354 | d | 0.567 | 0.660 | 0.684 | 0.713 | [0.642, 0.720] |
| [.5,.8) | 1832 | 354 | dc | 0.591 | 0.682 | 0.715 | 0.742 | [0.675, 0.750] |
| [.5,.8) | 1832 | 354 | tb2c | 0.560 | 0.669 | 0.697 | 0.735 | [0.657, 0.732] |
| [.5,.8) | 1832 | 354 | tbc | 0.568 | 0.652 | 0.678 | 0.716 | [0.634, 0.717] |
| [.5,.8) | 1832 | 354 | cs | 0.576 | 0.653 | 0.676 | 0.717 | [0.633, 0.715] |
| [.8,1] | 1985 | 251 | a | 0.636 | 0.747 | 0.778 | 0.816 | [0.744, 0.808] |
| [.8,1] | 1985 | 251 | ac | 0.628 | 0.736 | 0.765 | 0.810 | [0.727, 0.801] |
| [.8,1] | 1985 | 251 | c | 0.658 | 0.745 | 0.790 | 0.823 | [0.759, 0.818] |
| [.8,1] | 1985 | 251 | cc | 0.641 | 0.738 | 0.774 | 0.816 | [0.740, 0.804] |
| [.8,1] | 1985 | 251 | d | 0.662 | 0.751 | 0.783 | 0.822 | [0.750, 0.812] |
| [.8,1] | 1985 | 251 | dc | 0.678 | 0.763 | 0.799 | 0.840 | [0.767, 0.828] |
| [.8,1] | 1985 | 251 | tb2c | 0.637 | 0.744 | 0.777 | 0.823 | [0.742, 0.810] |
| [.8,1] | 1985 | 251 | tbc | 0.669 | 0.752 | 0.789 | 0.826 | [0.757, 0.817] |
| [.8,1] | 1985 | 251 | cs | 0.669 | 0.764 | 0.794 | 0.833 | [0.763, 0.824] |

### Per query modality, all buckets

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image | 3896 | 1244 | a | 0.494 | 0.600 | 0.638 | 0.682 | [0.605, 0.670] |
| image | 3896 | 1244 | ac | 0.513 | 0.614 | 0.648 | 0.699 | [0.615, 0.678] |
| image | 3896 | 1244 | c | 0.563 | 0.646 | 0.683 | 0.721 | [0.653, 0.711] |
| image | 3896 | 1244 | cc | 0.565 | 0.656 | 0.691 | 0.732 | [0.664, 0.716] |
| image | 3896 | 1244 | d | 0.565 | 0.653 | 0.685 | 0.722 | [0.655, 0.712] |
| image | 3896 | 1244 | dc | 0.578 | 0.668 | 0.706 | 0.742 | [0.678, 0.734] |
| image | 3896 | 1244 | tb2c | 0.543 | 0.647 | 0.681 | 0.726 | [0.652, 0.708] |
| image | 3896 | 1244 | tbc | 0.568 | 0.651 | 0.684 | 0.722 | [0.654, 0.712] |
| image | 3896 | 1244 | cs | 0.571 | 0.655 | 0.686 | 0.726 | [0.655, 0.714] |
| pdf_text | 211 | 83 | a | 0.725 | 0.834 | 0.858 | 0.886 | [0.784, 0.910] |
| pdf_text | 211 | 83 | ac | 0.744 | 0.867 | 0.891 | 0.924 | [0.827, 0.935] |
| pdf_text | 211 | 83 | c | 0.810 | 0.886 | 0.900 | 0.924 | [0.833, 0.941] |
| pdf_text | 211 | 83 | cc | 0.815 | 0.882 | 0.905 | 0.938 | [0.846, 0.946] |
| pdf_text | 211 | 83 | d | 0.796 | 0.891 | 0.900 | 0.919 | [0.834, 0.941] |
| pdf_text | 211 | 83 | dc | 0.801 | 0.891 | 0.919 | 0.938 | [0.861, 0.958] |
| pdf_text | 211 | 83 | tb2c | 0.787 | 0.863 | 0.882 | 0.919 | [0.819, 0.925] |
| pdf_text | 211 | 83 | tbc | 0.791 | 0.877 | 0.896 | 0.924 | [0.826, 0.939] |
| pdf_text | 211 | 83 | cs | 0.801 | 0.886 | 0.905 | 0.919 | [0.839, 0.945] |
| text | 8561 | 1767 | a | 0.686 | 0.775 | 0.799 | 0.829 | [0.783, 0.813] |
| text | 8561 | 1767 | ac | 0.703 | 0.794 | 0.821 | 0.853 | [0.806, 0.834] |
| text | 8561 | 1767 | c | 0.705 | 0.794 | 0.818 | 0.844 | [0.804, 0.831] |
| text | 8561 | 1767 | cc | 0.716 | 0.812 | 0.835 | 0.861 | [0.822, 0.847] |
| text | 8561 | 1767 | d | 0.701 | 0.799 | 0.818 | 0.847 | [0.805, 0.831] |
| text | 8561 | 1767 | dc | 0.711 | 0.812 | 0.835 | 0.860 | [0.822, 0.847] |
| text | 8561 | 1767 | tb2c | 0.711 | 0.807 | 0.827 | 0.854 | [0.813, 0.840] |
| text | 8561 | 1767 | tbc | 0.701 | 0.792 | 0.817 | 0.845 | [0.803, 0.830] |
| text | 8561 | 1767 | cs | 0.704 | 0.794 | 0.817 | 0.845 | [0.803, 0.830] |
| table | 156 | 64 | a | 0.603 | 0.705 | 0.744 | 0.801 | [0.612, 0.835] |
| table | 156 | 64 | ac | 0.635 | 0.744 | 0.782 | 0.853 | [0.670, 0.857] |
| table | 156 | 64 | c | 0.724 | 0.776 | 0.801 | 0.853 | [0.709, 0.873] |
| table | 156 | 64 | cc | 0.744 | 0.782 | 0.827 | 0.859 | [0.744, 0.892] |
| table | 156 | 64 | d | 0.744 | 0.788 | 0.821 | 0.853 | [0.733, 0.886] |
| table | 156 | 64 | dc | 0.750 | 0.788 | 0.827 | 0.859 | [0.741, 0.890] |
| table | 156 | 64 | tb2c | 0.667 | 0.788 | 0.801 | 0.859 | [0.707, 0.872] |
| table | 156 | 64 | tbc | 0.744 | 0.788 | 0.795 | 0.859 | [0.698, 0.866] |
| table | 156 | 64 | cs | 0.737 | 0.788 | 0.808 | 0.840 | [0.713, 0.873] |
| other | 15 | 10 | a | 0.733 | 0.733 | 0.733 | 0.800 | [0.499, 0.929] |
| other | 15 | 10 | ac | 0.733 | 0.733 | 0.733 | 0.800 | [0.499, 0.929] |
| other | 15 | 10 | c | 0.667 | 0.733 | 0.733 | 0.733 | [0.499, 0.929] |
| other | 15 | 10 | cc | 0.733 | 0.733 | 0.733 | 0.733 | [0.499, 0.929] |
| other | 15 | 10 | d | 0.667 | 0.667 | 0.667 | 0.733 | [0.364, 0.867] |
| other | 15 | 10 | dc | 0.733 | 0.733 | 0.733 | 0.733 | [0.499, 0.929] |
| other | 15 | 10 | tb2c | 0.733 | 0.733 | 0.733 | 0.733 | [0.499, 0.929] |
| other | 15 | 10 | tbc | 0.667 | 0.733 | 0.733 | 0.733 | [0.499, 0.929] |
| other | 15 | 10 | cs | 0.667 | 0.733 | 0.733 | 0.733 | [0.499, 0.929] |

### Image queries per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| image [0,.2) | 331 | 274 | a | 0.076 | 0.118 | 0.160 | 0.199 | [0.115, 0.207] |
| image [0,.2) | 331 | 274 | ac | 0.142 | 0.215 | 0.245 | 0.299 | [0.192, 0.299] |
| image [0,.2) | 331 | 274 | c | 0.154 | 0.236 | 0.278 | 0.332 | [0.219, 0.332] |
| image [0,.2) | 331 | 274 | cc | 0.184 | 0.293 | 0.332 | 0.390 | [0.270, 0.393] |
| image [0,.2) | 331 | 274 | d | 0.172 | 0.263 | 0.296 | 0.338 | [0.238, 0.354] |
| image [0,.2) | 331 | 274 | dc | 0.193 | 0.302 | 0.360 | 0.405 | [0.295, 0.421] |
| image [0,.2) | 331 | 274 | tb2c | 0.145 | 0.245 | 0.290 | 0.326 | [0.231, 0.345] |
| image [0,.2) | 331 | 274 | tbc | 0.157 | 0.236 | 0.266 | 0.326 | [0.209, 0.321] |
| image [0,.2) | 331 | 274 | cs | 0.160 | 0.227 | 0.278 | 0.332 | [0.220, 0.334] |
| image [.2,.5) | 752 | 485 | a | 0.219 | 0.309 | 0.336 | 0.392 | [0.287, 0.391] |
| image [.2,.5) | 752 | 485 | ac | 0.271 | 0.364 | 0.399 | 0.460 | [0.349, 0.449] |
| image [.2,.5) | 752 | 485 | c | 0.358 | 0.423 | 0.441 | 0.479 | [0.381, 0.499] |
| image [.2,.5) | 752 | 485 | cc | 0.379 | 0.451 | 0.481 | 0.524 | [0.423, 0.537] |
| image [.2,.5) | 752 | 485 | d | 0.367 | 0.434 | 0.461 | 0.500 | [0.403, 0.515] |
| image [.2,.5) | 752 | 485 | dc | 0.378 | 0.453 | 0.491 | 0.520 | [0.434, 0.545] |
| image [.2,.5) | 752 | 485 | tb2c | 0.340 | 0.428 | 0.467 | 0.520 | [0.414, 0.519] |
| image [.2,.5) | 752 | 485 | tbc | 0.358 | 0.426 | 0.449 | 0.483 | [0.391, 0.504] |
| image [.2,.5) | 752 | 485 | cs | 0.362 | 0.424 | 0.445 | 0.483 | [0.387, 0.501] |
| image [.5,.8) | 1048 | 282 | a | 0.478 | 0.595 | 0.652 | 0.699 | [0.592, 0.705] |
| image [.5,.8) | 1048 | 282 | ac | 0.514 | 0.625 | 0.663 | 0.722 | [0.604, 0.713] |
| image [.5,.8) | 1048 | 282 | c | 0.580 | 0.670 | 0.700 | 0.746 | [0.651, 0.743] |
| image [.5,.8) | 1048 | 282 | cc | 0.605 | 0.694 | 0.727 | 0.760 | [0.678, 0.767] |
| image [.5,.8) | 1048 | 282 | d | 0.569 | 0.674 | 0.702 | 0.734 | [0.652, 0.748] |
| image [.5,.8) | 1048 | 282 | dc | 0.589 | 0.689 | 0.725 | 0.753 | [0.679, 0.765] |
| image [.5,.8) | 1048 | 282 | tb2c | 0.571 | 0.678 | 0.707 | 0.752 | [0.660, 0.747] |
| image [.5,.8) | 1048 | 282 | tbc | 0.577 | 0.669 | 0.699 | 0.739 | [0.650, 0.740] |
| image [.5,.8) | 1048 | 282 | cs | 0.589 | 0.670 | 0.698 | 0.741 | [0.648, 0.743] |
| image [.8,1] | 1765 | 203 | a | 0.700 | 0.816 | 0.848 | 0.886 | [0.819, 0.874] |
| image [.8,1] | 1765 | 203 | ac | 0.684 | 0.790 | 0.820 | 0.862 | [0.782, 0.855] |
| image [.8,1] | 1765 | 203 | c | 0.716 | 0.805 | 0.852 | 0.883 | [0.823, 0.876] |
| image [.8,1] | 1765 | 203 | cc | 0.691 | 0.790 | 0.825 | 0.867 | [0.794, 0.855] |
| image [.8,1] | 1765 | 203 | d | 0.720 | 0.808 | 0.842 | 0.882 | [0.813, 0.868] |
| image [.8,1] | 1765 | 203 | dc | 0.730 | 0.816 | 0.852 | 0.894 | [0.823, 0.879] |
| image [.8,1] | 1765 | 203 | tb2c | 0.687 | 0.796 | 0.829 | 0.874 | [0.795, 0.861] |
| image [.8,1] | 1765 | 203 | tbc | 0.729 | 0.814 | 0.854 | 0.887 | [0.825, 0.878] |
| image [.8,1] | 1765 | 203 | cs | 0.727 | 0.825 | 0.857 | 0.894 | [0.829, 0.881] |

### Text-like queries (text, table, pdf_text, other) per bucket

| cell | queries | dirs | rep | R@1 | R@3 | R@5 | R@10 | R@5 95% CI |
|---|---:|---:|---|---:|---:|---:|---:|---|
| textlike [0,.2) | 5814 | 743 | a | 0.774 | 0.860 | 0.883 | 0.910 | [0.869, 0.896] |
| textlike [0,.2) | 5814 | 743 | ac | 0.772 | 0.858 | 0.884 | 0.912 | [0.871, 0.897] |
| textlike [0,.2) | 5814 | 743 | c | 0.766 | 0.856 | 0.879 | 0.903 | [0.866, 0.892] |
| textlike [0,.2) | 5814 | 743 | cc | 0.770 | 0.864 | 0.883 | 0.907 | [0.870, 0.896] |
| textlike [0,.2) | 5814 | 743 | d | 0.759 | 0.858 | 0.877 | 0.904 | [0.863, 0.891] |
| textlike [0,.2) | 5814 | 743 | dc | 0.765 | 0.864 | 0.885 | 0.908 | [0.872, 0.898] |
| textlike [0,.2) | 5814 | 743 | tb2c | 0.768 | 0.860 | 0.878 | 0.904 | [0.864, 0.892] |
| textlike [0,.2) | 5814 | 743 | tbc | 0.764 | 0.854 | 0.878 | 0.903 | [0.865, 0.891] |
| textlike [0,.2) | 5814 | 743 | cs | 0.765 | 0.856 | 0.879 | 0.903 | [0.865, 0.891] |
| textlike [.2,.5) | 2151 | 566 | a | 0.620 | 0.720 | 0.748 | 0.785 | [0.717, 0.777] |
| textlike [.2,.5) | 2151 | 566 | ac | 0.661 | 0.760 | 0.783 | 0.818 | [0.755, 0.809] |
| textlike [.2,.5) | 2151 | 566 | c | 0.656 | 0.749 | 0.775 | 0.807 | [0.748, 0.802] |
| textlike [.2,.5) | 2151 | 566 | cc | 0.677 | 0.777 | 0.807 | 0.836 | [0.781, 0.832] |
| textlike [.2,.5) | 2151 | 566 | d | 0.658 | 0.756 | 0.777 | 0.812 | [0.750, 0.804] |
| textlike [.2,.5) | 2151 | 566 | dc | 0.668 | 0.778 | 0.804 | 0.831 | [0.777, 0.828] |
| textlike [.2,.5) | 2151 | 566 | tb2c | 0.671 | 0.772 | 0.794 | 0.822 | [0.766, 0.818] |
| textlike [.2,.5) | 2151 | 566 | tbc | 0.650 | 0.748 | 0.775 | 0.807 | [0.747, 0.801] |
| textlike [.2,.5) | 2151 | 566 | cs | 0.656 | 0.751 | 0.773 | 0.807 | [0.746, 0.801] |
| textlike [.5,.8) | 764 | 339 | a | 0.357 | 0.453 | 0.479 | 0.517 | [0.407, 0.550] |
| textlike [.5,.8) | 764 | 339 | ac | 0.454 | 0.555 | 0.597 | 0.654 | [0.536, 0.661] |
| textlike [.5,.8) | 764 | 339 | c | 0.556 | 0.619 | 0.637 | 0.671 | [0.579, 0.691] |
| textlike [.5,.8) | 764 | 339 | cc | 0.585 | 0.668 | 0.698 | 0.732 | [0.642, 0.747] |
| textlike [.5,.8) | 764 | 339 | d | 0.556 | 0.634 | 0.652 | 0.678 | [0.597, 0.704] |
| textlike [.5,.8) | 764 | 339 | dc | 0.586 | 0.665 | 0.692 | 0.721 | [0.637, 0.742] |
| textlike [.5,.8) | 764 | 339 | tb2c | 0.538 | 0.649 | 0.675 | 0.707 | [0.623, 0.725] |
| textlike [.5,.8) | 764 | 339 | tbc | 0.546 | 0.620 | 0.641 | 0.678 | [0.585, 0.694] |
| textlike [.5,.8) | 764 | 339 | cs | 0.550 | 0.620 | 0.636 | 0.675 | [0.579, 0.691] |
| textlike [.8,1] | 214 | 181 | a | 0.107 | 0.173 | 0.201 | 0.238 | [0.129, 0.286] |
| textlike [.8,1] | 214 | 181 | ac | 0.159 | 0.285 | 0.313 | 0.383 | [0.230, 0.400] |
| textlike [.8,1] | 214 | 181 | c | 0.178 | 0.252 | 0.290 | 0.332 | [0.206, 0.382] |
| textlike [.8,1] | 214 | 181 | cc | 0.229 | 0.313 | 0.350 | 0.397 | [0.267, 0.436] |
| textlike [.8,1] | 214 | 181 | d | 0.187 | 0.285 | 0.299 | 0.332 | [0.215, 0.392] |
| textlike [.8,1] | 214 | 181 | dc | 0.252 | 0.332 | 0.369 | 0.402 | [0.286, 0.456] |
| textlike [.8,1] | 214 | 181 | tb2c | 0.224 | 0.313 | 0.346 | 0.397 | [0.264, 0.428] |
| textlike [.8,1] | 214 | 181 | tbc | 0.173 | 0.243 | 0.262 | 0.327 | [0.183, 0.355] |
| textlike [.8,1] | 214 | 181 | cs | 0.187 | 0.266 | 0.285 | 0.336 | [0.200, 0.376] |

### Session 3 primary cells: recall@5, paired bootstrap over directories

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 1083 | 759 | 0.283 | 0.352 | 0.392 | 0.436 | 0.411 | 0.451 | 0.413 | 0.393 | 0.394 | +0.109 | [+0.076, +0.140] |
| P2 textlike in [.5,.8)+[.8,1] | 978 | 520 | 0.418 | 0.535 | 0.561 | 0.622 | 0.575 | 0.622 | 0.603 | 0.558 | 0.559 | +0.143 | [+0.102, +0.189] |

### Primary cells split by bucket (not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 part: image [0,.2) | 331 | 274 | 0.160 | 0.245 | 0.278 | 0.332 | 0.296 | 0.360 | 0.290 | 0.266 | 0.278 | +0.118 | [+0.069, +0.174] |
| P1 part: image [.2,.5) | 752 | 485 | 0.336 | 0.399 | 0.441 | 0.481 | 0.461 | 0.491 | 0.467 | 0.449 | 0.445 | +0.105 | [+0.070, +0.142] |
| P2 part: textlike [.5,.8) | 764 | 339 | 0.479 | 0.597 | 0.637 | 0.698 | 0.652 | 0.692 | 0.675 | 0.641 | 0.636 | +0.158 | [+0.111, +0.211] |
| P2 part: textlike [.8,1] | 214 | 181 | 0.201 | 0.313 | 0.290 | 0.350 | 0.299 | 0.369 | 0.346 | 0.262 | 0.285 | +0.089 | [+0.037, +0.145] |

### Majority-modality cells (for contrast, not part of the criterion)

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | c-a | c-a 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| image in [.5,.8)+[.8,1] | 2813 | 485 | 0.775 | 0.761 | 0.795 | 0.789 | 0.790 | 0.805 | 0.784 | 0.796 | 0.798 | +0.020 | [+0.001, +0.040] |
| textlike in [0,.2)+[.2,.5) | 7965 | 1309 | 0.846 | 0.857 | 0.851 | 0.863 | 0.850 | 0.863 | 0.855 | 0.850 | 0.850 | +0.005 | [-0.002, +0.013] |

### Secondary: d - c everywhere, recall@5

| cell | queries | dirs | a | ac | c | cc | d | dc | tb2c | tbc | cs | d-c | d-c 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 image in [0,.2)+[.2,.5) | 1083 | 759 | 0.283 | 0.352 | 0.392 | 0.436 | 0.411 | 0.451 | 0.413 | 0.393 | 0.394 | +0.019 | [+0.008, +0.031] |
| P2 textlike in [.5,.8)+[.8,1] | 978 | 520 | 0.418 | 0.535 | 0.561 | 0.622 | 0.575 | 0.622 | 0.603 | 0.558 | 0.559 | +0.013 | [+0.003, +0.024] |
| P1 part: image [0,.2) | 331 | 274 | 0.160 | 0.245 | 0.278 | 0.332 | 0.296 | 0.360 | 0.290 | 0.266 | 0.278 | +0.018 | [-0.003, +0.039] |
| P1 part: image [.2,.5) | 752 | 485 | 0.336 | 0.399 | 0.441 | 0.481 | 0.461 | 0.491 | 0.467 | 0.449 | 0.445 | +0.020 | [+0.006, +0.033] |
| P2 part: textlike [.5,.8) | 764 | 339 | 0.479 | 0.597 | 0.637 | 0.698 | 0.652 | 0.692 | 0.675 | 0.641 | 0.636 | +0.014 | [+0.004, +0.027] |
| P2 part: textlike [.8,1] | 214 | 181 | 0.201 | 0.313 | 0.290 | 0.350 | 0.299 | 0.369 | 0.346 | 0.262 | 0.285 | +0.009 | [-0.018, +0.035] |
| image in [.5,.8)+[.8,1] | 2813 | 485 | 0.775 | 0.761 | 0.795 | 0.789 | 0.790 | 0.805 | 0.784 | 0.796 | 0.798 | -0.005 | [-0.020, +0.009] |
| textlike in [0,.2)+[.2,.5) | 7965 | 1309 | 0.846 | 0.857 | 0.851 | 0.863 | 0.850 | 0.863 | 0.855 | 0.850 | 0.850 | -0.001 | [-0.005, +0.003] |
| all [0,.2) | 6177 | 745 | 0.844 | 0.850 | 0.847 | 0.854 | 0.846 | 0.857 | 0.847 | 0.845 | 0.847 | -0.001 | [-0.006, +0.003] |
| all [.2,.5) | 2957 | 573 | 0.648 | 0.688 | 0.694 | 0.727 | 0.701 | 0.727 | 0.714 | 0.696 | 0.694 | +0.007 | [+0.001, +0.013] |
| all [.5,.8) | 1832 | 354 | 0.583 | 0.639 | 0.677 | 0.718 | 0.684 | 0.715 | 0.697 | 0.678 | 0.676 | +0.007 | [-0.004, +0.016] |
| all [.8,1] | 1985 | 251 | 0.778 | 0.765 | 0.790 | 0.774 | 0.783 | 0.799 | 0.777 | 0.789 | 0.794 | -0.007 | [-0.028, +0.012] |
| image [0,.2) | 331 | 274 | 0.160 | 0.245 | 0.278 | 0.332 | 0.296 | 0.360 | 0.290 | 0.266 | 0.278 | +0.018 | [-0.000, +0.040] |
| image [.2,.5) | 752 | 485 | 0.336 | 0.399 | 0.441 | 0.481 | 0.461 | 0.491 | 0.467 | 0.449 | 0.445 | +0.020 | [+0.006, +0.036] |
| image [.5,.8) | 1048 | 282 | 0.652 | 0.663 | 0.700 | 0.727 | 0.702 | 0.725 | 0.707 | 0.699 | 0.698 | +0.002 | [-0.013, +0.017] |
| image [.8,1] | 1765 | 203 | 0.848 | 0.820 | 0.852 | 0.825 | 0.842 | 0.852 | 0.829 | 0.854 | 0.857 | -0.009 | [-0.034, +0.013] |
| textlike [0,.2) | 5814 | 743 | 0.883 | 0.884 | 0.879 | 0.883 | 0.877 | 0.885 | 0.878 | 0.878 | 0.879 | -0.002 | [-0.007, +0.003] |
| textlike [.2,.5) | 2151 | 566 | 0.748 | 0.783 | 0.775 | 0.807 | 0.777 | 0.804 | 0.794 | 0.775 | 0.773 | +0.002 | [-0.004, +0.010] |
| textlike [.5,.8) | 764 | 339 | 0.479 | 0.597 | 0.637 | 0.698 | 0.652 | 0.692 | 0.675 | 0.641 | 0.636 | +0.014 | [+0.004, +0.026] |
| textlike [.8,1] | 214 | 181 | 0.201 | 0.313 | 0.290 | 0.350 | 0.299 | 0.369 | 0.346 | 0.262 | 0.285 | +0.009 | [-0.014, +0.038] |

Paired 95% interval of c - a excludes zero (lower bound > 0): P1 image in [0,.2)+[.2,.5): yes; P2 textlike in [.5,.8)+[.8,1]: yes.
H survives under the session 3 kill criterion.

### Session 9 (eval queries): recall@5 per cell and x - c, paired bootstrap over directories

| rep | family | vec/folder | R@5 all | R@5 P1 image in [0,.2)+[.2,.5) | R@5 P2 textlike in [.5,.8)+[.8,1] | R@5 image in [.5,.8)+[.8,1] | R@5 textlike in [0,.2)+[.2,.5) | x-c all | x-c P1 image in [0,.2)+[.2,.5) | x-c P2 textlike in [.5,.8)+[.8,1] | x-c image in [.5,.8)+[.8,1] | x-c textlike in [0,.2)+[.2,.5) | min over 4 cells |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|
| a | ref | 1.00 | 0.752 | 0.283 | 0.418 | 0.775 | 0.846 | -0.027 [-0.035, -0.020] | -0.109 [-0.140, -0.076] | -0.143 [-0.189, -0.102] | -0.020 [-0.040, -0.001] | -0.005 [-0.013, +0.002] | -0.143 |
| ac | ref | 1.00 | 0.770 | 0.352 | 0.535 | 0.761 | 0.857 | -0.009 [-0.018, -0.001] | -0.040 [-0.077, -0.003] | -0.027 [-0.069, +0.014] | -0.034 [-0.056, -0.013] | +0.006 [-0.002, +0.013] | -0.040 |
| c | ref | 3.90 | 0.780 | 0.392 | 0.561 | 0.795 | 0.851 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 |
| cc | ref | 3.90 | 0.793 | 0.436 | 0.622 | 0.789 | 0.863 | +0.014 [+0.009, +0.019] | +0.044 [+0.030, +0.060] | +0.060 [+0.042, +0.078] | -0.006 [-0.019, +0.006] | +0.011 [+0.007, +0.017] | -0.006 |
| d | ref | 8.05 | 0.780 | 0.411 | 0.575 | 0.790 | 0.850 | +0.001 [-0.004, +0.005] | +0.019 [+0.008, +0.031] | +0.013 [+0.003, +0.024] | -0.005 [-0.020, +0.009] | -0.001 [-0.005, +0.003] | -0.005 |
| dc | ref | 8.05 | 0.798 | 0.451 | 0.622 | 0.805 | 0.863 | +0.019 [+0.013, +0.024] | +0.059 [+0.043, +0.076] | +0.060 [+0.043, +0.080] | +0.010 [-0.005, +0.024] | +0.012 [+0.007, +0.017] | +0.010 |
| tb2c | F5 | 2.00 | 0.784 | 0.413 | 0.603 | 0.784 | 0.855 | +0.005 [-0.001, +0.011] | +0.021 [-0.002, +0.044] | +0.042 [+0.018, +0.067] | -0.011 [-0.025, +0.004] | +0.004 [-0.003, +0.011] | -0.011 |
| tbc | F5 | 3.90 | 0.779 | 0.393 | 0.558 | 0.796 | 0.850 | -0.001 [-0.003, +0.001] | +0.002 [-0.008, +0.011] | -0.003 [-0.012, +0.006] | +0.001 [-0.004, +0.007] | -0.001 [-0.004, +0.001] | -0.003 |
| cs | ref | 4.21 | 0.780 | 0.394 | 0.559 | 0.798 | 0.850 | +0.000 [-0.002, +0.002] | +0.003 [-0.003, +0.009] | -0.002 [-0.009, +0.004] | +0.002 [-0.005, +0.011] | -0.001 [-0.003, +0.001] | -0.002 |

### Session 9 (eval queries): recall@1 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.629 | 0.175 | 0.303 | 0.617 | 0.732 |
| ac | 0.647 | 0.232 | 0.390 | 0.621 | 0.742 |
| c | 0.666 | 0.295 | 0.473 | 0.665 | 0.736 |
| cc | 0.674 | 0.319 | 0.507 | 0.659 | 0.745 |
| d | 0.664 | 0.307 | 0.475 | 0.664 | 0.732 |
| dc | 0.675 | 0.321 | 0.513 | 0.677 | 0.739 |
| tb2c | 0.662 | 0.281 | 0.469 | 0.644 | 0.742 |
| tbc | 0.665 | 0.296 | 0.464 | 0.672 | 0.733 |
| cs | 0.668 | 0.300 | 0.470 | 0.675 | 0.735 |

### Session 9 (eval queries): recall@10 per cell

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---:|---:|---:|---:|---:|
| a | 0.787 | 0.333 | 0.456 | 0.816 | 0.876 |
| ac | 0.809 | 0.411 | 0.595 | 0.810 | 0.887 |
| c | 0.809 | 0.434 | 0.597 | 0.832 | 0.877 |
| cc | 0.824 | 0.483 | 0.658 | 0.827 | 0.888 |
| d | 0.812 | 0.451 | 0.602 | 0.827 | 0.879 |
| dc | 0.826 | 0.485 | 0.651 | 0.841 | 0.887 |
| tb2c | 0.817 | 0.461 | 0.639 | 0.829 | 0.882 |
| tbc | 0.810 | 0.435 | 0.601 | 0.832 | 0.877 |
| cs | 0.811 | 0.437 | 0.601 | 0.837 | 0.877 |

### Session 9 (eval queries): x - d, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.028 [-0.037, -0.019] | -0.128 [-0.160, -0.097] | -0.156 [-0.203, -0.117] | -0.015 [-0.038, +0.008] | -0.004 [-0.012, +0.004] |
| ac | -0.010 [-0.019, -0.002] | -0.059 [-0.093, -0.024] | -0.040 [-0.081, -0.001] | -0.029 [-0.052, -0.006] | +0.007 [-0.001, +0.014] |
| c | -0.001 [-0.005, +0.004] | -0.019 [-0.031, -0.008] | -0.013 [-0.024, -0.003] | +0.005 [-0.009, +0.020] | +0.001 [-0.003, +0.005] |
| cc | +0.013 [+0.008, +0.018] | +0.025 [+0.008, +0.042] | +0.047 [+0.032, +0.064] | -0.001 [-0.014, +0.013] | +0.012 [+0.008, +0.017] |
| d | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| dc | +0.018 [+0.015, +0.021] | +0.040 [+0.025, +0.055] | +0.047 [+0.032, +0.064] | +0.015 [+0.008, +0.021] | +0.013 [+0.009, +0.016] |
| tb2c | +0.004 [-0.003, +0.011] | +0.002 [-0.022, +0.025] | +0.029 [+0.004, +0.053] | -0.006 [-0.022, +0.011] | +0.005 [-0.002, +0.012] |
| tbc | -0.002 [-0.006, +0.003] | -0.018 [-0.029, -0.006] | -0.016 [-0.029, -0.003] | +0.006 [-0.008, +0.021] | -0.000 [-0.004, +0.004] |
| cs | -0.001 [-0.004, +0.003] | -0.017 [-0.028, -0.006] | -0.015 [-0.026, -0.006] | +0.007 [-0.003, +0.019] | +0.000 [-0.004, +0.004] |

### Session 9 (eval queries): x - dc, recall@5, paired bootstrap over directories

| rep | all | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---|---|---|---|
| a | -0.046 [-0.055, -0.037] | -0.168 [-0.201, -0.136] | -0.203 [-0.250, -0.163] | -0.030 [-0.055, -0.006] | -0.017 [-0.024, -0.009] |
| ac | -0.028 [-0.037, -0.019] | -0.099 [-0.132, -0.063] | -0.087 [-0.128, -0.052] | -0.043 [-0.068, -0.019] | -0.006 [-0.014, +0.002] |
| c | -0.019 [-0.024, -0.013] | -0.059 [-0.076, -0.043] | -0.060 [-0.080, -0.043] | -0.010 [-0.024, +0.005] | -0.012 [-0.017, -0.007] |
| cc | -0.005 [-0.009, -0.001] | -0.015 [-0.027, -0.004] | +0.000 [-0.008, +0.008] | -0.016 [-0.030, -0.001] | -0.000 [-0.004, +0.003] |
| d | -0.018 [-0.021, -0.015] | -0.040 [-0.055, -0.025] | -0.047 [-0.064, -0.032] | -0.015 [-0.021, -0.008] | -0.013 [-0.016, -0.009] |
| dc | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| tb2c | -0.014 [-0.020, -0.008] | -0.038 [-0.059, -0.017] | -0.018 [-0.037, -0.001] | -0.021 [-0.039, -0.003] | -0.008 [-0.014, -0.001] |
| tbc | -0.019 [-0.024, -0.014] | -0.057 [-0.076, -0.040] | -0.063 [-0.083, -0.045] | -0.009 [-0.024, +0.006] | -0.013 [-0.018, -0.008] |
| cs | -0.019 [-0.023, -0.014] | -0.056 [-0.073, -0.041] | -0.062 [-0.080, -0.046] | -0.007 [-0.019, +0.004] | -0.013 [-0.018, -0.008] |

### Session 9 selection rule applied to the eval queries (valid only on dev)

| family | selected | vec/folder | min over 4 cells of (x - c) | P1 image in [0,.2)+[.2,.5) | P2 textlike in [.5,.8)+[.8,1] | image in [.5,.8)+[.8,1] | textlike in [0,.2)+[.2,.5) |
|---|---|---:|---:|---:|---:|---:|---:|
| F5 | tbc | 3.90 | -0.003 | +0.002 | -0.003 | +0.001 | -0.001 |

### Session 9 modality gap per space, eval directories

| vectors | gap: norm of mean img minus mean txt | same-folder cos img-img | txt-txt | img-txt |
|---|---:|---:|---:|---:|
| uncentered | 0.412 | 0.717 | 0.736 | 0.504 |
| centered | 0.107 | 0.492 | 0.471 | 0.170 |

### Session 9 F5 cluster purity, eval directories with both input groups

| rep | vec/folder | purity | folders |
|---|---:|---:|---:|
| tb2c | 2.00 | 0.899 | 1486 |
| tbc | 3.90 | 0.989 | 1486 |

### Session 9 hypotheses on the eval queries

H9c, c - tbc (type-blind k-means at c's budget, uncentered): P1 image in [0,.2)+[.2,.5) -0.002 [-0.011, +0.008]; P2 textlike in [.5,.8)+[.8,1] +0.003 [-0.006, +0.012]; interval includes zero in a primary cell: yes, H9c dead.

## Session 19 commit-subject queries, E1 (jina-embeddings-v4, cache jina-embeddings-v4_s24)

Queries: 1827 over 845 directories and 731 owners; 2599 directories ranked (random recall@5 = 0.0019); 0 queries dropped because their directory has no embedded file. Representations use all embedded files of a directory (the query is not a file). Calibration seed 20261104 gives the text mean for the centered rows.

### recall@1

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1827 | 845 | 731 | 0.126 | 0.123 | 0.163 | 0.150 | 0.181 | 0.165 | 0.049 |
| text-heavy [0,.2)+[.2,.5) | 1556 | 696 | 608 | 0.135 | 0.127 | 0.160 | 0.145 | 0.181 | 0.164 | 0.045 |
| image-heavy [.5,.8)+[.8,1] | 271 | 149 | 138 | 0.074 | 0.103 | 0.181 | 0.181 | 0.185 | 0.173 | 0.074 |

### recall@5

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1827 | 845 | 731 | 0.229 | 0.228 | 0.267 | 0.252 | 0.288 | 0.269 | 0.091 |
| text-heavy [0,.2)+[.2,.5) | 1556 | 696 | 608 | 0.245 | 0.237 | 0.269 | 0.249 | 0.293 | 0.270 | 0.085 |
| image-heavy [.5,.8)+[.8,1] | 271 | 149 | 138 | 0.140 | 0.177 | 0.258 | 0.266 | 0.258 | 0.266 | 0.122 |

### recall@10

| cell | queries | directories | owners | a | ac | c | cc | d | dc | names alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1827 | 845 | 731 | 0.283 | 0.271 | 0.321 | 0.293 | 0.341 | 0.318 | 0.128 |
| text-heavy [0,.2)+[.2,.5) | 1556 | 696 | 608 | 0.303 | 0.281 | 0.326 | 0.292 | 0.350 | 0.320 | 0.123 |
| image-heavy [.5,.8)+[.8,1] | 271 | 149 | 138 | 0.166 | 0.214 | 0.288 | 0.299 | 0.288 | 0.306 | 0.155 |

### Differences in recall@5: point, owner-clustered 95% interval

| cell | subset | queries | c - a | d - c | ac - a | cc - c |
|---|---|---:|---|---|---|---|
| all | all | 1827 | +0.038 [+0.022, +0.055] | +0.021 [+0.010, +0.031] | -0.001 [-0.012, +0.011] | -0.015 [-0.030, -0.001] |
| all | names miss | 1661 | +0.034 [+0.017, +0.051] | +0.018 [+0.007, +0.029] | -0.004 [-0.015, +0.009] | -0.017 [-0.032, -0.004] |
| text-heavy [0,.2)+[.2,.5) | all | 1556 | +0.024 [+0.006, +0.040] | +0.024 [+0.012, +0.036] | -0.008 [-0.021, +0.006] | -0.019 [-0.036, -0.004] |
| text-heavy [0,.2)+[.2,.5) | names miss | 1423 | +0.021 [+0.003, +0.041] | +0.021 [+0.009, +0.034] | -0.009 [-0.023, +0.004] | -0.020 [-0.036, -0.005] |
| image-heavy [.5,.8)+[.8,1] | all | 271 | +0.118 [+0.072, +0.169] | +0.000 [-0.021, +0.021] | +0.037 [+0.004, +0.071] | +0.007 [-0.027, +0.039] |
| image-heavy [.5,.8)+[.8,1] | names miss | 238 | +0.109 [+0.061, +0.155] | +0.000 [-0.021, +0.021] | +0.029 [-0.005, +0.064] | +0.000 [-0.030, +0.029] |

H19d statistic (E1): image-heavy directories, 271 queries from 138 owners; gate, recall@5 of d 0.258 (needs 0.10 and more than names alone, 0.122): passed; owner-weighted c - a +0.117 [+0.065, +0.169]; H19d: confirmed (lower bound at or above +0.05).

## Session 19 validity and verdicts (E1; E1 decides the hypotheses)

Queries: 12951 over 1923 directories and 1473 owners (effective owners 640). Queries per encoder before taking those all encoders share: E1 12951.

### Reproduction of eval.py's directory intervals of c - a

- E1 P1: here +0.109 [+0.076, +0.140]; eval.py +0.109 [+0.076, +0.140]; same
- E1 P2: here +0.143 [+0.102, +0.189]; eval.py +0.143 [+0.102, +0.189]; same

Reproduced: the directory bootstrap here is eval.py's.

### Flags (counts over the evaluation queries)

| cell | queries | directories | owners (effective) | same-stem sibling | names alone in top 5 | clean |
|---|---:|---:|---|---:|---:|---:|
| all | 12951 | 1923 | 1473 (640) | 995 | 5815 | 7136 |
| P1 | 1083 | 759 | 705 (371) | 89 | 340 | 743 |
| P2 | 978 | 520 | 469 (216) | 126 | 342 | 636 |
| M1 | 2813 | 485 | 440 (160) | 104 | 1721 | 1092 |
| M2 | 7965 | 1309 | 1048 (463) | 663 | 3310 | 4655 |

### Filename-only baseline (no encoder): recall@5

| cell | d_fn (max over names) | a_fn (pooled names) |
|---|---:|---:|
| all | 0.413 | 0.387 |
| P1 | 0.307 | 0.247 |
| P2 | 0.338 | 0.279 |
| M1 | 0.559 | 0.541 |
| M2 | 0.379 | 0.358 |

### c - a by subset (H19a reads 'all', H19b reads 'clean')

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | all | c - a | all | 12951 | 1923 | 1473 (640) | +0.027 | [+0.020, +0.035] | [+0.020, +0.036] | +0.019 [+0.010, +0.027] |
| E1 | all | c - a | P1 | 1083 | 759 | 705 (371) | +0.109 | [+0.076, +0.140] | [+0.077, +0.143] | +0.055 [+0.033, +0.075] |
| E1 | all | c - a | P2 | 978 | 520 | 469 (216) | +0.143 | [+0.102, +0.189] | [+0.101, +0.189] | +0.095 [+0.065, +0.124] |
| E1 | all | c - a | M1 | 2813 | 485 | 440 (160) | +0.020 | [+0.001, +0.040] | [+0.000, +0.039] | +0.000 [-0.023, +0.024] |
| E1 | all | c - a | M2 | 7965 | 1309 | 1048 (463) | +0.005 | [-0.002, +0.013] | [-0.002, +0.012] | +0.004 [-0.007, +0.014] |
| E1 | names miss | c - a | all | 7136 | 1786 | 1415 (814) | +0.021 | [+0.012, +0.031] | [+0.011, +0.031] | +0.017 [+0.006, +0.028] |
| E1 | names miss | c - a | P1 | 743 | 633 | 594 (460) | +0.066 | [+0.041, +0.093] | [+0.041, +0.093] | +0.039 [+0.019, +0.060] |
| E1 | names miss | c - a | P2 | 636 | 445 | 404 (289) | +0.134 | [+0.094, +0.171] | [+0.096, +0.174] | +0.095 [+0.065, +0.129] |
| E1 | names miss | c - a | M1 | 1092 | 344 | 320 (134) | +0.006 | [-0.021, +0.035] | [-0.020, +0.033] | -0.005 [-0.037, +0.027] |
| E1 | names miss | c - a | M2 | 4655 | 1210 | 996 (611) | +0.003 | [-0.006, +0.012] | [-0.006, +0.012] | +0.003 [-0.009, +0.015] |
| E1 | no sibling | c - a | all | 11956 | 1899 | 1463 (633) | +0.027 | [+0.019, +0.036] | [+0.018, +0.036] | +0.017 [+0.008, +0.026] |
| E1 | no sibling | c - a | P1 | 994 | 716 | 665 (360) | +0.106 | [+0.073, +0.138] | [+0.072, +0.136] | +0.049 [+0.029, +0.069] |
| E1 | no sibling | c - a | P2 | 852 | 496 | 448 (219) | +0.154 | [+0.109, +0.202] | [+0.112, +0.200] | +0.096 [+0.065, +0.128] |
| E1 | no sibling | c - a | M1 | 2709 | 476 | 434 (155) | +0.020 | [-0.000, +0.041] | [+0.001, +0.040] | -0.001 [-0.026, +0.022] |
| E1 | no sibling | c - a | M2 | 7302 | 1294 | 1038 (458) | +0.005 | [-0.004, +0.013] | [-0.003, +0.013] | +0.004 [-0.008, +0.014] |
| E1 | clean | c - a | all | 7136 | 1786 | 1415 (814) | +0.021 | [+0.012, +0.031] | [+0.011, +0.031] | +0.017 [+0.006, +0.028] |
| E1 | clean | c - a | P1 | 743 | 633 | 594 (460) | +0.066 | [+0.041, +0.093] | [+0.041, +0.093] | +0.039 [+0.019, +0.060] |
| E1 | clean | c - a | P2 | 636 | 445 | 404 (289) | +0.134 | [+0.094, +0.171] | [+0.096, +0.174] | +0.095 [+0.065, +0.129] |
| E1 | clean | c - a | M1 | 1092 | 344 | 320 (134) | +0.006 | [-0.021, +0.035] | [-0.020, +0.033] | -0.005 [-0.037, +0.027] |
| E1 | clean | c - a | M2 | 4655 | 1210 | 996 (611) | +0.003 | [-0.006, +0.012] | [-0.006, +0.012] | +0.003 [-0.009, +0.015] |

### c - d, cs - d and cs - c (H19c reads c - d over all queries)

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | all | c - d | all | 12951 | 1923 | 1473 (640) | -0.001 | [-0.005, +0.004] | [-0.005, +0.003] | -0.007 [-0.011, -0.003] |
| E1 | all | c - d | P1 | 1083 | 759 | 705 (371) | -0.019 | [-0.031, -0.008] | [-0.031, -0.008] | -0.023 [-0.036, -0.010] |
| E1 | all | c - d | P2 | 978 | 520 | 469 (216) | -0.013 | [-0.024, -0.003] | [-0.024, -0.003] | -0.019 [-0.033, -0.004] |
| E1 | all | c - d | M1 | 2813 | 485 | 440 (160) | +0.005 | [-0.009, +0.020] | [-0.010, +0.021] | -0.013 [-0.025, -0.003] |
| E1 | all | c - d | M2 | 7965 | 1309 | 1048 (463) | +0.001 | [-0.003, +0.005] | [-0.003, +0.005] | -0.006 [-0.012, -0.001] |
| E1 | all | cs - d | all | 12951 | 1923 | 1473 (640) | -0.001 | [-0.004, +0.003] | [-0.004, +0.003] | -0.006 [-0.010, -0.003] |
| E1 | all | cs - d | P1 | 1083 | 759 | 705 (371) | -0.017 | [-0.028, -0.006] | [-0.028, -0.007] | -0.019 [-0.032, -0.008] |
| E1 | all | cs - d | P2 | 978 | 520 | 469 (216) | -0.015 | [-0.026, -0.006] | [-0.027, -0.006] | -0.020 [-0.034, -0.008] |
| E1 | all | cs - d | M1 | 2813 | 485 | 440 (160) | +0.007 | [-0.003, +0.019] | [-0.003, +0.018] | -0.007 [-0.016, +0.000] |
| E1 | all | cs - d | M2 | 7965 | 1309 | 1048 (463) | +0.000 | [-0.004, +0.004] | [-0.004, +0.003] | -0.006 [-0.012, -0.001] |
| E1 | all | cs - c | all | 12951 | 1923 | 1473 (640) | +0.000 | [-0.002, +0.002] | [-0.002, +0.002] | +0.001 [-0.001, +0.003] |
| E1 | all | cs - c | P1 | 1083 | 759 | 705 (371) | +0.003 | [-0.003, +0.009] | [-0.003, +0.009] | +0.004 [-0.004, +0.011] |
| E1 | all | cs - c | P2 | 978 | 520 | 469 (216) | -0.002 | [-0.009, +0.004] | [-0.008, +0.004] | -0.002 [-0.010, +0.007] |
| E1 | all | cs - c | M1 | 2813 | 485 | 440 (160) | +0.002 | [-0.005, +0.011] | [-0.006, +0.011] | +0.006 [-0.000, +0.013] |
| E1 | all | cs - c | M2 | 7965 | 1309 | 1048 (463) | -0.001 | [-0.003, +0.001] | [-0.003, +0.001] | -0.000 [-0.003, +0.002] |

### The registered tests (owner-weighted mean, 10,000 resamples of owners)

| encoder | test | queries | owners | point | 95% | 98.33% | reading |
|---|---|---:|---:|---:|---|---|---|
| E1 | H19a P1s: c - a (primary) | 506 | 172 | +0.210 | [+0.155, +0.266] | [+0.144, +0.279] | confirmed (lower bound at or above +0.05) |
| E1 | H19a P2s: c - a (primary) | 669 | 197 | +0.196 | [+0.144, +0.248] | [+0.133, +0.260] | confirmed (lower bound at or above +0.05) |
| E1 | H19c: c - d where c differs from d (primary) | 9729 | 918 | -0.002 | [-0.008, +0.005] | [-0.010, +0.006] | not inferior (lower bound at or above -0.02) |
| E1 | H19b P1s clean: c - a | 232 | 118 | +0.180 | [+0.113, +0.250] | [+0.099, +0.267] | confirmed (lower bound at or above +0.05) |
| E1 | H19b P2s clean: c - a | 355 | 155 | +0.209 | [+0.147, +0.275] | [+0.134, +0.288] | confirmed (lower bound at or above +0.05) |
| E1 | no-code folders, P1s: c - a | 230 | 67 | +0.169 | [+0.090, +0.252] | [+0.074, +0.270] | inconclusive (fewer than 100 owners) |
| E1 | no-code folders, P2s: c - a | 420 | 127 | +0.181 | [+0.120, +0.245] | [+0.107, +0.260] | confirmed (lower bound at or above +0.05) |
| E1 | all of P1 (lone images included): c - a | 1083 | 705 | +0.055 | [+0.034, +0.076] | [+0.029, +0.080] | present, size open (lower bound above zero) |
| E1 | all of P2 (lone texts included): c - a | 978 | 469 | +0.095 | [+0.065, +0.125] | [+0.060, +0.131] | confirmed (lower bound at or above +0.05) |
| E1 | cs - d where c differs from d | 9729 | 918 | -0.002 | [-0.009, +0.004] | [-0.010, +0.005] | not inferior (lower bound at or above -0.02) |

### Verdicts

H19a (E1, decides): P1s confirmed (lower bound at or above +0.05); P2s confirmed (lower bound at or above +0.05). H19a: confirmed in both cells.
H19b (E1, secondary): clean P1s confirmed (lower bound at or above +0.05); clean P2s confirmed (lower bound at or above +0.05).
H19c (E1, decides): not inferior (lower bound at or above -0.02).

### Secondary: the minority cells by the kind of the query file (c - a, owner-weighted, 95%)

| encoder | cell | kind | queries | owners | R@5 a | R@5 c | R@5 d | c - a |
|---|---|---|---:|---:|---:|---:|---:|---|
| E1 | P1s | image | 506 | 172 | 0.447 | 0.672 | 0.688 | +0.210 [+0.156, +0.265] |
| E1 | P2s | prose | 347 | 154 | 0.680 | 0.801 | 0.804 | +0.134 [+0.073, +0.195] |
| E1 | P2s | code | 155 | 70 | 0.329 | 0.677 | 0.703 | +0.254 [+0.143, +0.369] |
| E1 | P2s | config | 137 | 74 | 0.482 | 0.693 | 0.701 | +0.236 [+0.144, +0.331] |
| E1 | P2s | table | 30 | 14 | 0.467 | 0.767 | 0.800 | +0.238 [-0.048, +0.524] |

### Secondary: recall@5 by the number of embedded files in the query's folder

| encoder | group | cell | queries | owners | c equals d | R@5 a | R@5 c | R@5 cs | R@5 d |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| E1 | 3 to 10 | all | 7036 | 1234 | 0.450 | 0.689 | 0.698 | 0.699 | 0.708 |
| E1 | 3 to 10 | P1 | 726 | 586 | 0.446 | 0.222 | 0.275 | 0.280 | 0.296 |
| E1 | 3 to 10 | P2 | 566 | 354 | 0.542 | 0.337 | 0.456 | 0.451 | 0.473 |
| E1 | 3 to 10 | M1 | 1184 | 342 | 0.524 | 0.704 | 0.691 | 0.693 | 0.714 |
| E1 | 3 to 10 | M2 | 4545 | 897 | 0.418 | 0.804 | 0.798 | 0.797 | 0.801 |
| E1 | 11 to 30 | all | 3798 | 266 | 0.000 | 0.828 | 0.864 | 0.863 | 0.850 |
| E1 | 11 to 30 | P1 | 239 | 109 | 0.000 | 0.368 | 0.594 | 0.594 | 0.611 |
| E1 | 11 to 30 | P2 | 270 | 99 | 0.000 | 0.504 | 0.644 | 0.644 | 0.652 |
| E1 | 11 to 30 | M1 | 894 | 83 | 0.000 | 0.836 | 0.858 | 0.858 | 0.827 |
| E1 | 11 to 30 | M2 | 2352 | 163 | 0.000 | 0.907 | 0.917 | 0.915 | 0.906 |
| E1 | 31 to 100 | all | 2059 | 53 | 0.000 | 0.841 | 0.918 | 0.919 | 0.914 |
| E1 | 31 to 100 | P1 | 116 | 21 | 0.000 | 0.491 | 0.707 | 0.707 | 0.724 |
| E1 | 31 to 100 | P2 | 129 | 22 | 0.000 | 0.636 | 0.907 | 0.915 | 0.915 |
| E1 | 31 to 100 | M1 | 728 | 26 | 0.000 | 0.821 | 0.894 | 0.900 | 0.876 |
| E1 | 31 to 100 | M2 | 1033 | 27 | 0.000 | 0.912 | 0.956 | 0.955 | 0.958 |

### Secondary: differences by the number of embedded files in the query's folder

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | 3 to 10 | c - a | all | 7036 | 1536 | 1234 (904) | +0.009 | [+0.000, +0.017] | [-0.000, +0.018] | +0.014 [+0.004, +0.025] |
| E1 | 3 to 10 | c - a | P1 | 726 | 621 | 586 (484) | +0.054 | [+0.027, +0.080] | [+0.027, +0.080] | +0.034 [+0.012, +0.054] |
| E1 | 3 to 10 | c - a | P2 | 566 | 385 | 354 (271) | +0.118 | [+0.075, +0.161] | [+0.073, +0.161] | +0.086 [+0.049, +0.123] |
| E1 | 3 to 10 | c - a | M1 | 1184 | 368 | 342 (250) | -0.014 | [-0.038, +0.011] | [-0.038, +0.009] | -0.016 [-0.047, +0.012] |
| E1 | 3 to 10 | c - a | M2 | 4545 | 1080 | 897 (654) | -0.006 | [-0.015, +0.003] | [-0.015, +0.003] | +0.003 [-0.011, +0.014] |
| E1 | 3 to 10 | c - d | all | 7036 | 1536 | 1234 (904) | -0.010 | [-0.014, -0.005] | [-0.014, -0.005] | -0.012 [-0.016, -0.007] |
| E1 | 3 to 10 | c - d | P1 | 726 | 621 | 586 (484) | -0.021 | [-0.035, -0.008] | [-0.034, -0.008] | -0.024 [-0.038, -0.010] |
| E1 | 3 to 10 | c - d | P2 | 566 | 385 | 354 (271) | -0.018 | [-0.033, -0.004] | [-0.032, -0.004] | -0.016 [-0.032, -0.000] |
| E1 | 3 to 10 | c - d | M1 | 1184 | 368 | 342 (250) | -0.023 | [-0.033, -0.014] | [-0.033, -0.014] | -0.024 [-0.035, -0.014] |
| E1 | 3 to 10 | c - d | M2 | 4545 | 1080 | 897 (654) | -0.004 | [-0.009, +0.002] | [-0.010, +0.002] | -0.009 [-0.015, -0.003] |
| E1 | 3 to 10 | cs - d | all | 7036 | 1536 | 1234 (904) | -0.010 | [-0.014, -0.005] | [-0.014, -0.005] | -0.011 [-0.015, -0.007] |
| E1 | 3 to 10 | cs - d | P1 | 726 | 621 | 586 (484) | -0.017 | [-0.029, -0.004] | [-0.030, -0.004] | -0.018 [-0.032, -0.005] |
| E1 | 3 to 10 | cs - d | P2 | 566 | 385 | 354 (271) | -0.023 | [-0.040, -0.009] | [-0.038, -0.009] | -0.021 [-0.037, -0.007] |
| E1 | 3 to 10 | cs - d | M1 | 1184 | 368 | 342 (250) | -0.020 | [-0.030, -0.011] | [-0.031, -0.010] | -0.017 [-0.027, -0.009] |
| E1 | 3 to 10 | cs - d | M2 | 4545 | 1080 | 897 (654) | -0.004 | [-0.010, +0.002] | [-0.010, +0.002] | -0.009 [-0.015, -0.003] |
| E1 | 11 to 30 | c - a | all | 3798 | 291 | 266 (196) | +0.036 | [+0.024, +0.049] | [+0.023, +0.049] | +0.037 [+0.024, +0.050] |
| E1 | 11 to 30 | c - a | P1 | 239 | 115 | 109 (66) | +0.226 | [+0.150, +0.294] | [+0.150, +0.303] | +0.147 [+0.090, +0.208] |
| E1 | 11 to 30 | c - a | P2 | 270 | 102 | 99 (54) | +0.141 | [+0.076, +0.208] | [+0.079, +0.210] | +0.094 [+0.051, +0.145] |
| E1 | 11 to 30 | c - a | M1 | 894 | 85 | 83 (58) | +0.022 | [-0.006, +0.053] | [-0.007, +0.052] | +0.052 [+0.013, +0.099] |
| E1 | 11 to 30 | c - a | M2 | 2352 | 176 | 163 (135) | +0.010 | [-0.002, +0.020] | [-0.000, +0.020] | +0.013 [+0.002, +0.024] |
| E1 | 11 to 30 | c - d | all | 3798 | 291 | 266 (196) | +0.013 | [+0.004, +0.023] | [+0.005, +0.023] | +0.009 [+0.000, +0.018] |
| E1 | 11 to 30 | c - d | P1 | 239 | 115 | 109 (66) | -0.017 | [-0.045, +0.009] | [-0.043, +0.008] | -0.019 [-0.053, +0.012] |
| E1 | 11 to 30 | c - d | P2 | 270 | 102 | 99 (54) | -0.007 | [-0.028, +0.010] | [-0.026, +0.010] | -0.022 [-0.055, +0.005] |
| E1 | 11 to 30 | c - d | M1 | 894 | 85 | 83 (58) | +0.031 | [+0.002, +0.069] | [+0.003, +0.067] | +0.021 [-0.006, +0.049] |
| E1 | 11 to 30 | c - d | M2 | 2352 | 176 | 163 (135) | +0.011 | [+0.004, +0.019] | [+0.005, +0.019] | +0.011 [+0.004, +0.019] |
| E1 | 11 to 30 | cs - d | all | 3798 | 291 | 266 (196) | +0.012 | [+0.005, +0.020] | [+0.005, +0.019] | +0.009 [+0.002, +0.015] |
| E1 | 11 to 30 | cs - d | P1 | 239 | 115 | 109 (66) | -0.017 | [-0.043, +0.005] | [-0.041, +0.008] | -0.020 [-0.054, +0.012] |
| E1 | 11 to 30 | cs - d | P2 | 270 | 102 | 99 (54) | -0.007 | [-0.024, +0.007] | [-0.022, +0.007] | -0.015 [-0.040, +0.003] |
| E1 | 11 to 30 | cs - d | M1 | 894 | 85 | 83 (58) | +0.031 | [+0.011, +0.058] | [+0.011, +0.054] | +0.022 [+0.003, +0.040] |
| E1 | 11 to 30 | cs - d | M2 | 2352 | 176 | 163 (135) | +0.010 | [+0.003, +0.016] | [+0.004, +0.016] | +0.010 [+0.004, +0.016] |
| E1 | 31 to 100 | c - a | all | 2059 | 57 | 53 (44) | +0.077 | [+0.048, +0.113] | [+0.047, +0.116] | +0.087 [+0.054, +0.123] |
| E1 | 31 to 100 | c - a | P1 | 116 | 21 | 21 (12) | +0.216 | [+0.078, +0.347] | [+0.082, +0.350] | +0.174 [+0.075, +0.281] |
| E1 | 31 to 100 | c - a | P2 | 129 | 22 | 22 (10) | +0.271 | [+0.073, +0.544] | [+0.089, +0.540] | +0.291 [+0.142, +0.470] |
| E1 | 31 to 100 | c - a | M1 | 728 | 26 | 26 (20) | +0.073 | [+0.030, +0.130] | [+0.031, +0.129] | +0.063 [+0.012, +0.124] |
| E1 | 31 to 100 | c - a | M2 | 1033 | 29 | 27 (22) | +0.045 | [+0.013, +0.083] | [+0.014, +0.089] | +0.052 [+0.012, +0.105] |
| E1 | 31 to 100 | c - d | all | 2059 | 57 | 53 (44) | +0.004 | [-0.009, +0.017] | [-0.009, +0.018] | +0.010 [-0.009, +0.032] |
| E1 | 31 to 100 | c - d | P1 | 116 | 21 | 21 (12) | -0.017 | [-0.071, +0.013] | [-0.066, +0.016] | -0.022 [-0.063, +0.006] |
| E1 | 31 to 100 | c - d | P2 | 129 | 22 | 22 (10) | -0.008 | [-0.040, +0.018] | [-0.040, +0.016] | -0.052 [-0.150, +0.005] |
| E1 | 31 to 100 | c - d | M1 | 728 | 26 | 26 (20) | +0.018 | [-0.018, +0.054] | [-0.015, +0.056] | +0.021 [-0.020, +0.066] |
| E1 | 31 to 100 | c - d | M2 | 1033 | 29 | 27 (22) | -0.002 | [-0.009, +0.006] | [-0.010, +0.006] | -0.001 [-0.010, +0.010] |
| E1 | 31 to 100 | cs - d | all | 2059 | 57 | 53 (44) | +0.005 | [-0.005, +0.015] | [-0.004, +0.016] | +0.011 [-0.003, +0.031] |
| E1 | 31 to 100 | cs - d | P1 | 116 | 21 | 21 (12) | -0.017 | [-0.071, +0.013] | [-0.066, +0.016] | -0.022 [-0.063, +0.006] |
| E1 | 31 to 100 | cs - d | P2 | 129 | 22 | 22 (10) | +0.000 | [-0.025, +0.022] | [-0.026, +0.020] | -0.041 [-0.136, +0.009] |
| E1 | 31 to 100 | cs - d | M1 | 728 | 26 | 26 (20) | +0.023 | [-0.001, +0.049] | [-0.001, +0.050] | +0.030 [+0.005, +0.068] |
| E1 | 31 to 100 | cs - d | M2 | 1033 | 29 | 27 (22) | -0.004 | [-0.011, +0.002] | [-0.011, +0.002] | -0.007 [-0.015, +0.000] |

### Secondary: differences on the queries whose folder c does not hold whole (a label keeps more than three files)

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | c differs from d | c - a | all | 9729 | 1083 | 918 (413) | +0.034 | [+0.025, +0.045] | [+0.025, +0.044] | +0.024 [+0.013, +0.035] |
| E1 | c differs from d | c - a | P1 | 757 | 463 | 443 (216) | +0.140 | [+0.097, +0.181] | [+0.099, +0.178] | +0.072 [+0.045, +0.101] |
| E1 | c differs from d | c - a | P2 | 658 | 283 | 266 (115) | +0.173 | [+0.120, +0.232] | [+0.116, +0.233] | +0.121 [+0.083, +0.160] |
| E1 | c differs from d | c - a | M1 | 2185 | 229 | 218 (103) | +0.033 | [+0.012, +0.056] | [+0.012, +0.052] | +0.024 [+0.001, +0.049] |
| E1 | c differs from d | c - a | M2 | 6028 | 641 | 553 (297) | +0.006 | [-0.003, +0.016] | [-0.002, +0.016] | -0.002 [-0.012, +0.007] |
| E1 | c differs from d | c - d | all | 9729 | 1083 | 918 (413) | +0.005 | [-0.001, +0.010] | [-0.001, +0.010] | -0.002 [-0.008, +0.004] |
| E1 | c differs from d | c - d | P1 | 757 | 463 | 443 (216) | -0.020 | [-0.036, -0.005] | [-0.034, -0.005] | -0.024 [-0.041, -0.005] |
| E1 | c differs from d | c - d | P2 | 658 | 283 | 266 (115) | -0.006 | [-0.020, +0.006] | [-0.018, +0.006] | -0.011 [-0.031, +0.008] |
| E1 | c differs from d | c - d | M1 | 2185 | 229 | 218 (103) | +0.014 | [-0.004, +0.033] | [-0.003, +0.032] | +0.001 [-0.012, +0.015] |
| E1 | c differs from d | c - d | M2 | 6028 | 641 | 553 (297) | +0.005 | [+0.001, +0.010] | [+0.001, +0.010] | +0.005 [-0.003, +0.013] |
| E1 | c differs from d | cs - d | all | 9729 | 1083 | 918 (413) | +0.004 | [-0.000, +0.009] | [-0.000, +0.009] | -0.002 [-0.009, +0.004] |
| E1 | c differs from d | cs - d | P1 | 757 | 463 | 443 (216) | -0.018 | [-0.033, -0.005] | [-0.033, -0.004] | -0.022 [-0.040, -0.005] |
| E1 | c differs from d | cs - d | P2 | 658 | 283 | 266 (115) | -0.008 | [-0.020, +0.003] | [-0.019, +0.003] | -0.013 [-0.031, +0.003] |
| E1 | c differs from d | cs - d | M1 | 2185 | 229 | 218 (103) | +0.016 | [+0.003, +0.030] | [+0.003, +0.029] | +0.003 [-0.007, +0.014] |
| E1 | c differs from d | cs - d | M2 | 6028 | 641 | 553 (297) | +0.004 | [-0.000, +0.008] | [-0.001, +0.009] | +0.004 [-0.003, +0.011] |
| E1 | c equals d | c - a | all | 3222 | 996 | 862 (703) | +0.007 | [-0.006, +0.020] | [-0.006, +0.020] | +0.010 [-0.004, +0.024] |
| E1 | c equals d | c - a | P1 | 326 | 296 | 287 (253) | +0.037 | [+0.009, +0.069] | [+0.006, +0.072] | +0.024 [-0.002, +0.050] |
| E1 | c equals d | c - a | P2 | 320 | 237 | 222 (187) | +0.081 | [+0.033, +0.130] | [+0.035, +0.133] | +0.065 [+0.026, +0.110] |
| E1 | c equals d | c - a | M1 | 628 | 256 | 242 (196) | -0.025 | [-0.061, +0.009] | [-0.061, +0.007] | -0.026 [-0.061, +0.014] |
| E1 | c equals d | c - a | M2 | 1937 | 669 | 600 (502) | +0.000 | [-0.015, +0.014] | [-0.015, +0.015] | +0.007 [-0.010, +0.024] |
| E1 | c equals d | c - d | all | 3222 | 996 | 862 (703) | -0.017 | [-0.023, -0.012] | [-0.023, -0.012] | -0.017 [-0.023, -0.011] |
| E1 | c equals d | c - d | P1 | 326 | 296 | 287 (253) | -0.018 | [-0.036, -0.003] | [-0.035, -0.003] | -0.021 [-0.038, -0.005] |
| E1 | c equals d | c - d | P2 | 320 | 237 | 222 (187) | -0.028 | [-0.050, -0.010] | [-0.052, -0.012] | -0.026 [-0.048, -0.009] |
| E1 | c equals d | c - d | M1 | 628 | 256 | 242 (196) | -0.025 | [-0.039, -0.013] | [-0.040, -0.013] | -0.029 [-0.046, -0.014] |
| E1 | c equals d | c - d | M2 | 1937 | 669 | 600 (502) | -0.013 | [-0.020, -0.007] | [-0.020, -0.006] | -0.014 [-0.022, -0.007] |
| E1 | c equals d | cs - d | all | 3222 | 996 | 862 (703) | -0.016 | [-0.021, -0.011] | [-0.021, -0.011] | -0.015 [-0.020, -0.010] |
| E1 | c equals d | cs - d | P1 | 326 | 296 | 287 (253) | -0.012 | [-0.028, +0.000] | [-0.027, +0.000] | -0.014 [-0.028, -0.002] |
| E1 | c equals d | cs - d | P2 | 320 | 237 | 222 (187) | -0.031 | [-0.052, -0.012] | [-0.053, -0.012] | -0.029 [-0.051, -0.011] |
| E1 | c equals d | cs - d | M1 | 628 | 256 | 242 (196) | -0.021 | [-0.034, -0.008] | [-0.035, -0.009] | -0.020 [-0.034, -0.007] |
| E1 | c equals d | cs - d | M2 | 1937 | 669 | 600 (502) | -0.012 | [-0.019, -0.007] | [-0.019, -0.006] | -0.014 [-0.022, -0.007] |

### Secondary: recall@5 by the number of other files of the query's input group in its folder

| encoder | group | cell | queries | owners | c equals d | R@5 a | R@5 c | R@5 d |
|---|---|---|---:|---:|---:|---:|---:|---:|
| E1 | none | P1 | 577 | 545 | 0.454 | 0.139 | 0.146 | 0.168 |
| E1 | none | P2 | 309 | 282 | 0.502 | 0.136 | 0.155 | 0.175 |
| E1 | 1 or 2 | P1 | 269 | 126 | 0.212 | 0.353 | 0.587 | 0.606 |
| E1 | 1 or 2 | P2 | 336 | 149 | 0.479 | 0.432 | 0.637 | 0.658 |
| E1 | 3 or more | P1 | 237 | 47 | 0.030 | 0.553 | 0.768 | 0.781 |
| E1 | 3 or more | P2 | 333 | 53 | 0.012 | 0.667 | 0.862 | 0.862 |

### Secondary: c - a by the number of other files of the query's input group in its folder

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | none | c - a | P1 | 577 | 577 | 545 (518) | +0.007 | [-0.012, +0.026] | [-0.012, +0.025] | +0.006 [-0.014, +0.024] |
| E1 | none | c - a | P2 | 309 | 309 | 282 (262) | +0.019 | [-0.010, +0.045] | [-0.007, +0.049] | +0.020 [-0.011, +0.051] |
| E1 | 1 or 2 | c - a | P1 | 269 | 133 | 126 (115) | +0.234 | [+0.168, +0.305] | [+0.169, +0.302] | +0.220 [+0.157, +0.288] |
| E1 | 1 or 2 | c - a | P2 | 336 | 156 | 149 (137) | +0.205 | [+0.149, +0.267] | [+0.144, +0.264] | +0.204 [+0.141, +0.264] |
| E1 | 3 or more | c - a | P1 | 237 | 49 | 47 (31) | +0.215 | [+0.127, +0.303] | [+0.128, +0.307] | +0.177 [+0.098, +0.264] |
| E1 | 3 or more | c - a | P2 | 333 | 55 | 53 (36) | +0.195 | [+0.097, +0.312] | [+0.100, +0.315] | +0.200 [+0.095, +0.307] |

### Secondary: c - a by the depth of the folder in its repository

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | root | c - a | all | 3778 | 633 | 614 (416) | +0.013 | [+0.001, +0.025] | [+0.002, +0.025] | +0.004 [-0.009, +0.015] |
| E1 | root | c - a | P1 | 490 | 397 | 389 (283) | +0.098 | [+0.058, +0.135] | [+0.057, +0.139] | +0.058 [+0.032, +0.085] |
| E1 | root | c - a | P2 | 144 | 81 | 79 (60) | +0.076 | [-0.016, +0.188] | [-0.015, +0.169] | +0.023 [-0.053, +0.097] |
| E1 | depth 1 | c - a | all | 3501 | 468 | 431 (218) | +0.039 | [+0.026, +0.052] | [+0.025, +0.052] | +0.028 [+0.008, +0.048] |
| E1 | depth 1 | c - a | P1 | 268 | 162 | 157 (79) | +0.127 | [+0.049, +0.194] | [+0.055, +0.199] | +0.056 [-0.002, +0.111] |
| E1 | depth 1 | c - a | P2 | 277 | 138 | 134 (77) | +0.184 | [+0.126, +0.242] | [+0.130, +0.242] | +0.158 [+0.104, +0.214] |
| E1 | depth 2 or more | c - a | all | 5672 | 822 | 627 (232) | +0.030 | [+0.017, +0.046] | [+0.017, +0.044] | +0.021 [+0.009, +0.035] |
| E1 | depth 2 or more | c - a | P1 | 325 | 200 | 181 (82) | +0.111 | [+0.055, +0.164] | [+0.054, +0.167] | +0.050 [+0.018, +0.087] |
| E1 | depth 2 or more | c - a | P2 | 557 | 301 | 264 (103) | +0.140 | [+0.078, +0.207] | [+0.079, +0.206] | +0.087 [+0.047, +0.126] |

### Secondary: the other rows with owner-clustered intervals

| encoder | subset | pair | cell | queries | directories | owners (effective) | point | directory 95% | owner-clustered 95% | owner-weighted [clustered 95%] |
|---|---|---|---|---:|---:|---|---:|---|---|---|
| E1 | all | tb2c - c | all | 12951 | 1923 | 1473 (640) | +0.005 | [-0.001, +0.011] | [-0.002, +0.012] | +0.035 [+0.027, +0.042] |
| E1 | all | tb2c - c | P1 | 1083 | 759 | 705 (371) | +0.021 | [-0.002, +0.044] | [-0.001, +0.043] | +0.055 [+0.034, +0.077] |
| E1 | all | tb2c - c | P2 | 978 | 520 | 469 (216) | +0.042 | [+0.018, +0.067] | [+0.017, +0.068] | +0.094 [+0.065, +0.124] |
| E1 | all | tb2c - c | M1 | 2813 | 485 | 440 (160) | -0.011 | [-0.025, +0.004] | [-0.026, +0.004] | +0.034 [+0.017, +0.052] |
| E1 | all | tb2c - c | M2 | 7965 | 1309 | 1048 (463) | +0.004 | [-0.003, +0.011] | [-0.003, +0.011] | +0.031 [+0.023, +0.041] |
| E1 | all | c - tbc | all | 12951 | 1923 | 1473 (640) | +0.001 | [-0.001, +0.003] | [-0.001, +0.003] | -0.000 [-0.002, +0.002] |
| E1 | all | c - tbc | P1 | 1083 | 759 | 705 (371) | -0.002 | [-0.011, +0.008] | [-0.011, +0.008] | -0.001 [-0.010, +0.008] |
| E1 | all | c - tbc | P2 | 978 | 520 | 469 (216) | +0.003 | [-0.006, +0.012] | [-0.006, +0.013] | +0.004 [-0.005, +0.014] |
| E1 | all | c - tbc | M1 | 2813 | 485 | 440 (160) | -0.001 | [-0.007, +0.004] | [-0.007, +0.005] | -0.000 [-0.004, +0.003] |
| E1 | all | c - tbc | M2 | 7965 | 1309 | 1048 (463) | +0.001 | [-0.001, +0.004] | [-0.001, +0.003] | +0.000 [-0.002, +0.003] |
| E1 | all | cc - c | all | 12951 | 1923 | 1473 (640) | +0.014 | [+0.009, +0.019] | [+0.009, +0.019] | +0.036 [+0.030, +0.043] |
| E1 | all | cc - c | P1 | 1083 | 759 | 705 (371) | +0.044 | [+0.030, +0.060] | [+0.030, +0.058] | +0.053 [+0.034, +0.072] |
| E1 | all | cc - c | P2 | 978 | 520 | 469 (216) | +0.060 | [+0.042, +0.078] | [+0.044, +0.080] | +0.100 [+0.074, +0.127] |
| E1 | all | cc - c | M1 | 2813 | 485 | 440 (160) | -0.006 | [-0.019, +0.006] | [-0.019, +0.007] | +0.036 [+0.021, +0.052] |
| E1 | all | cc - c | M2 | 7965 | 1309 | 1048 (463) | +0.011 | [+0.007, +0.017] | [+0.007, +0.016] | +0.034 [+0.027, +0.042] |
| E1 | all | dc - d | all | 12951 | 1923 | 1473 (640) | +0.018 | [+0.015, +0.021] | [+0.015, +0.021] | +0.027 [+0.022, +0.033] |
| E1 | all | dc - d | P1 | 1083 | 759 | 705 (371) | +0.040 | [+0.025, +0.055] | [+0.026, +0.055] | +0.042 [+0.023, +0.062] |
| E1 | all | dc - d | P2 | 978 | 520 | 469 (216) | +0.047 | [+0.032, +0.064] | [+0.032, +0.064] | +0.082 [+0.058, +0.110] |
| E1 | all | dc - d | M1 | 2813 | 485 | 440 (160) | +0.015 | [+0.008, +0.021] | [+0.007, +0.021] | +0.017 [+0.005, +0.030] |
| E1 | all | dc - d | M2 | 7965 | 1309 | 1048 (463) | +0.013 | [+0.009, +0.016] | [+0.009, +0.016] | +0.024 [+0.018, +0.031] |
| E1 | all | ac - a | all | 12951 | 1923 | 1473 (640) | +0.018 | [+0.013, +0.023] | [+0.014, +0.023] | +0.039 [+0.033, +0.046] |
| E1 | all | ac - a | P1 | 1083 | 759 | 705 (371) | +0.069 | [+0.051, +0.090] | [+0.051, +0.089] | +0.088 [+0.067, +0.111] |
| E1 | all | ac - a | P2 | 978 | 520 | 469 (216) | +0.117 | [+0.091, +0.144] | [+0.092, +0.147] | +0.149 [+0.120, +0.180] |
| E1 | all | ac - a | M1 | 2813 | 485 | 440 (160) | -0.014 | [-0.025, -0.002] | [-0.025, -0.002] | +0.004 [-0.011, +0.021] |
| E1 | all | ac - a | M2 | 7965 | 1309 | 1048 (463) | +0.010 | [+0.006, +0.015] | [+0.005, +0.015] | +0.031 [+0.024, +0.040] |

