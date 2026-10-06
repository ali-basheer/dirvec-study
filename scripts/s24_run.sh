#!/bin/bash
# Session 24 on the pod: a second draw of GitHub directories, sized for the owner minimum that
# session 19 missed (BRIEF.md, session 24). Same code as session 19 under other file names: the day
# order goes on where session 19's pool stopped, only repositories session 19 did not read are
# harvested, and E1 alone is run. Called by scripts/s19_followup.sh, or by hand: bash scripts/s24_run.sh
#   S24_RESUME=1   skip every step whose output is already there
# It writes no DONE or FAILED marker of its own: the caller stops the pod.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
LOG=${S24_LOG:-/workspace/logs/s24}
PY=${S19_PY:-/workspace/venv/bin/python}
CORPUS=${S24_CORPUS:-/root/corpus_s24}
TMP=${S24_TMP:-/root/tmp_s24}
KEEP=${S24_KEEP:-/workspace/logs/s24}          # the working harvest log lives on the volume, so a stop does not lose it
M=jina-embeddings-v4
SEED=20261104
TRAILERS="Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01L3uBXsnxCDj3XA5StyfgGU"
mkdir -p "$LOG" "$CORPUS" "$TMP" "$KEEP"
export S19_SFX=_s24
export DIRVEC_THREADS=3 OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 HF_HUB_ENABLE_HF_TRANSFER=0 TOKENIZERS_PARALLELISM=false
[ -e data/corpus_s24 ] || ln -s "$CORPUS" data/corpus_s24
[ -n "${S24_RESUME:-}" ] || rm -f "$LOG/run.log"

step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
have() { [ -n "${S24_RESUME:-}" ] && [ -s "$1" ]; }
push() {  # push "<message>" file...
  local msg=$1; shift
  git add -f "$@" || return 1
  git commit -q -m "$msg" -m "$TRAILERS" -- "$@" || return 1
  for i in 1 2 3 4; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 15
  done
  return 1
}
fail() {  # what there is goes to the repository
  step "FAILED at: $1"
  {
    echo "# Session 24 outputs: INCOMPLETE, the run stopped at: $1"
    echo
    echo "Written by scripts/s24_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
    echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
    for f in pool.log harvest.log manifest.log history.log embed_e1.log; do
      [ -s "$LOG/$f" ] && { echo; echo "## The end of $f"; echo; echo '```'; tail -15 "$LOG/$f" | cut -c1-300; echo '```'; }
    done
  } > results/session24_outputs.md
  push "session 24: the run stopped at: $1 (run log and the ends of its logs)" results/session24_outputs.md
  exit 1
}

step "start, commit $(git rev-parse --short HEAD)"
ALL="$KEEP/harvest_all.jsonl"                  # session 19's harvest rows, then this session's
if have data/gt_structural_s24.jsonl; then
  step "resume: corpus, manifest and ground truth already there"
else
  [ -s data/pool_s19.jsonl ] || gunzip -kf data/pool_s19.jsonl.gz || fail "no session 19 pool"
  [ -s data/harvest_s19.jsonl ] || gunzip -kf data/harvest_s19.jsonl.gz || fail "no session 19 harvest log"
  [ -s data/pool_s24.jsonl ] || cp data/pool_s19.jsonl data/pool_s24.jsonl
  [ -s data/pool_s24_days.jsonl ] || cp data/pool_s19_days.jsonl data/pool_s24_days.jsonl
  [ -s "$ALL" ] || cp data/harvest_s19.jsonl "$ALL"
  N19=$(wc -l < data/harvest_s19.jsonl)
  need=13000
  for round in 1 2 3 4; do
    step "pool, round $round: at least $need usable repositories (session 19's 5,517 included)"
    "$PY" scripts/fetch_gh.py pool --seed $SEED --min-usable $need --out data/pool_s24.jsonl --days-log data/pool_s24_days.jsonl 2>> "$LOG/pool.log" || fail "pool"
    tail -1 "$LOG/pool.log" | tee -a "$LOG/run.log"
    step "harvest, round $round"
    "$PY" scripts/fetch_gh.py harvest --seed $SEED --mixed 2000 --other 600 --files 40000 --tmp "$TMP" --workers 6 \
      --pool data/pool_s24.jsonl --corpus data/corpus_s24 --selection data/selection_s24.jsonl --log data/download_log_s24.jsonl \
      --harvest-log "$ALL" --ghdirs data/ghdirs_s24.jsonl > "$LOG/harvest_state.json" 2>> "$LOG/harvest.log" || fail "harvest"
    tail -1 "$LOG/harvest.log" | tee -a "$LOG/run.log"
    tail -n +$((N19 + 1)) "$ALL" > data/harvest_s24.jsonl
    "$PY" - data/harvest_s24.jsonl >> "$LOG/run.log" 2>&1 <<'PY' || fail "more than 10 percent of the tarballs could not be fetched"
import json, sys
from collections import Counter
c = Counter(json.loads(l)["status"] for l in open(sys.argv[1]) if l.strip())
n = sum(c.values())
print(f"harvest log of this session: {n} repositories, {dict(c)}")
sys.exit(1 if n and c.get("fail", 0) > 0.10 * n else 0)
PY
    grep -q '"state": "full"' "$LOG/harvest_state.json" && break
    need=$((need + 2500))
  done
  grep -q '"state": "full"' "$LOG/harvest_state.json" || step "the pool was exhausted before the scored set was full: going on with what there is"
  step "manifest"
  "$PY" scripts/manifest.py --corpus data/corpus_s24 --selection data/selection_s24.jsonl --log data/download_log_s24.jsonl \
    --out-manifest data/manifest_s24.jsonl --out-dirs data/dirs_s24.jsonl --dir-prefix gh_ --workers 3 2> "$LOG/manifest.log" || fail "manifest"
  tail -2 "$LOG/manifest.log" | tee -a "$LOG/run.log"
  step "ground truth"
  "$PY" scripts/build_gt.py --manifest data/manifest_s24.jsonl --dirs data/dirs_s24.jsonl --out data/gt_structural_s24.jsonl \
    --workers 3 > "$LOG/gt.json" 2>> "$LOG/run.log" || fail "build_gt"
fi
if have data/commitq_s24.jsonl; then
  step "resume: commit history and queries already there"
else
  step "commit history"
  "$PY" scripts/fetch_gh.py history --selection data/selection_s24.jsonl --out data/commits_s24.jsonl --history-log data/history_s24.jsonl 2> "$LOG/history.log" || fail "history"
  tail -1 "$LOG/history.log" | tee -a "$LOG/run.log"
  "$PY" scripts/s19.py commitq build > "$LOG/commitq_build.txt" 2>> "$LOG/run.log" || fail "commitq build"
  cat "$LOG/commitq_build.txt" | tee -a "$LOG/run.log"
fi
"$PY" scripts/s19.py corpus > "$LOG/corpus.md" 2>> "$LOG/run.log" || fail "corpus counts"
if ! git ls-files --error-unmatch data/manifest_s24.jsonl > /dev/null 2>&1; then
  for f in pool_s24 harvest_s24 ghdirs_s24 commits_s24; do gzip -kf "data/$f.jsonl" || fail "gzip $f"; done
  push "session 24: the corpus of the second draw (pool with session 19's days, harvest log of the new repositories, eligible directories, selection, manifest, ground truth, commits and commit-subject queries)" \
    data/pool_s24.jsonl.gz data/pool_s24_days.jsonl data/harvest_s24.jsonl.gz data/ghdirs_s24.jsonl.gz data/selection_s24.jsonl \
    data/manifest_s24.jsonl data/dirs_s24.jsonl data/gt_structural_s24.jsonl data/commits_s24.jsonl.gz data/commitq_s24.jsonl \
    && step "corpus files pushed" || step "push of the corpus files failed (the run goes on)"
fi

check_files() {
  "$PY" - > "$LOG/files_check.txt" 2>> "$LOG/run.log" <<'PY'
import json, os, sys
rows = [json.loads(l) for l in open("data/manifest_s24.jsonl") if l.strip()]
miss = [r["path"] for r in rows if not os.path.isfile(r["path"]) or os.path.getsize(r["path"]) != r["bytes"]]
print(f"manifest rows {len(rows)}; files missing or of another size {len(miss)}")
sys.exit(1 if miss else 0)
PY
}
if ! check_files; then
  step "$(cat "$LOG/files_check.txt"): rebuilding the corpus from the selection"
  "$PY" scripts/fetch_gh.py download --selection data/selection_s24.jsonl --corpus data/corpus_s24 --tmp "$TMP" --workers 6 2>> "$LOG/download.log" || fail "download"
  check_files || fail "files of the manifest are missing after the rebuild"
fi
step "$(cat "$LOG/files_check.txt")"

EMB="${M}_s24"
if have "data/emb/$EMB/ranks_s24_e1.jsonl" && have "$LOG/validity.md"; then
  step "resume: E1 already evaluated"
else
  step "E1: embed all files"
  emb() { HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PY" scripts/embed.py all --model "$M" --text-mode query --manifest data/manifest_s24.jsonl \
            --tag _s24 --checkpoint 1000 --prep-workers 4 > "$LOG/embed_e1.json" 2>> "$LOG/embed_e1.log"; }
  emb || { step "E1: embedding stopped; one retry (the cache keeps what is done)"; emb || fail "E1 embedding"; }
  step "E1: $(tr -d '\n' < "$LOG/embed_e1.json" | cut -c1-300)"
  step "E1: eval"
  "$PY" scripts/eval.py --model "$M" --emb "$EMB" --manifest data/manifest_s24.jsonl --dirs data/dirs_s24.jsonl \
    --gt data/gt_structural_s24.jsonl --criterion s3 --calib 0.2 --calib-seed $SEED --queries eval --s9 \
    --reps a,ac,c,cc,d,dc,tb2c,tbc,cs --tag _s24_e1 > "$LOG/eval_e1.md" 2>> "$LOG/run.log" || fail "E1 eval"
  step "E1: commit-subject queries"
  HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PY" scripts/s19.py commitq embed --model "$M" --emb "$EMB" 2>> "$LOG/run.log" \
    && "$PY" scripts/s19.py commitq eval --model "$M" --emb "$EMB" --enc E1 --calib-seed $SEED \
         --dump-ranks "$LOG/commitq_ranks_e1.jsonl" > "$LOG/commitq_e1.md" 2>> "$LOG/run.log" \
    || { step "E1: commit-subject queries failed"; echo "(failed; see the run log)" > "$LOG/commitq_e1.md"; }
  "$PY" scripts/s19.py validity --ranks "E1=data/emb/$EMB/ranks_s24_e1.jsonl" --index "data/emb/$EMB/index.jsonl" \
    --evalmd "E1=$LOG/eval_e1.md" --flags "$LOG/flags.jsonl" > "$LOG/validity.md" 2>> "$LOG/run.log"
  rc=$?
  [ $rc -eq 3 ] && fail "validity does not reproduce eval.py's intervals"
  [ $rc -ne 0 ] && fail "validity"
fi

OUT=results/session24_outputs.md
{
  echo "# Session 24 outputs, verbatim"
  echo
  echo "Written by scripts/s24_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. scripts/s19.py printed the tables, so its headings and test names say session 19 and H19:"
  echo "on this draw they are the session 24 tests, H24a for H19a, H24b for H19b, H24c for H19c and H24d for H19d."
  echo "The verdicts and the reading are in results/session24.md."
  echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
  echo; cat "$LOG/corpus.md"
  echo; echo '## build_gt.py report'; echo; echo '```'; cat "$LOG/gt.json" 2>/dev/null; echo '```'
  echo; echo '## Commit-subject queries, build'; echo; echo '```'; cat "$LOG/commitq_build.txt" 2>/dev/null; echo '```'
  echo; echo "## E1: eval.py"; echo; cat "$LOG/eval_e1.md"
  echo; cat "$LOG/commitq_e1.md"
  echo; cat "$LOG/validity.md"
} > "$OUT"
gzip -c "data/emb/$EMB/ranks_s24_e1.jsonl" > data/ranks_s24_e1.jsonl.gz
gzip -c "$LOG/flags.jsonl" > data/flags_s24.jsonl.gz
[ -s "$LOG/commitq_ranks_e1.jsonl" ] && gzip -c "$LOG/commitq_ranks_e1.jsonl" > data/commitq_ranks_s24_e1.jsonl.gz
push "session 24: outputs of the second draw of GitHub directories (E1), verbatim" "$OUT" data/ranks_s24_e1.jsonl.gz data/flags_s24.jsonl.gz \
  $( [ -s data/commitq_ranks_s24_e1.jsonl.gz ] && echo data/commitq_ranks_s24_e1.jsonl.gz ) || fail "push of the outputs"
step "session 24 done"
