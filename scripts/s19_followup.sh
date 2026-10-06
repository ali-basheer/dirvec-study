#!/bin/bash
# Session 21 on the pod: what to store in a fixed number of bytes of a folder's metadata (BRIEF.md,
# session 21). scripts/s19_run.sh calls this after session 19's outputs are pushed; it can also be run
# by hand: bash scripts/s19_followup.sh. CPU only, on the caches of session 19 and of S11.
# The registered tests are those of "S19 E1". Outputs, verbatim: results/session21_outputs.md, pushed
# once after the two E1 runs and again at the end.
# Then, on the same pod: session 24 (scripts/s24_run.sh, a second draw of GitHub directories), the
# session 21 tests on that draw (results/session24_budget_outputs.md), and session 23
# (scripts/s23_run.sh, whole repository trees). S24_SKIP=1 or S23_SKIP=1 leaves one out.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
LOG=${S21_LOG:-/workspace/logs/s21}
PY=${S19_PY:-/workspace/venv/bin/python}
TRAILER1="Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
TRAILER2="Claude-Session: https://claude.ai/code/session_01L3uBXsnxCDj3XA5StyfgGU"
mkdir -p "$LOG"
rm -f "$LOG"/budget_*.md "$LOG/run.log"            # a second call starts clean
unset S21_BUDGETS S21_REG_BUDGET S21_SELFTEST       # the registered budgets, whatever the environment holds
export DIRVEC_THREADS=3 OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
code_id() { sha256sum scripts/budget.py scripts/quant.py scripts/eval.py | sha256sum | cut -c1-16; }

CODE=$(code_id)
step "start, commit $(git rev-parse --short HEAD), budget.py with quant.py and eval.py $CODE"
"$PY" scripts/s21_selftest.py > "$LOG/selftest.txt" 2>&1 || { step "self-test FAILED: no session 21 run"; tail -5 "$LOG/selftest.txt" | tee -a "$LOG/run.log"; exit 1; }
tail -1 "$LOG/selftest.txt" | tee -a "$LOG/run.log"

DONE_RUNS=""
run() {  # run <key> <label> <model> <emb> <set> <calibration seed> <ranks file> [--registered]
  local key=$1 label=$2 model=$3 emb=$4 set=$5 seed=$6 ranks=$7; shift 7
  if [ ! -s "$ranks" ] || [ ! -s "data/emb/$emb/vectors.npy" ]; then step "$label: no cache or ranks file, skipped"; return 0; fi
  [ "$(code_id)" = "$CODE" ] || step "WARNING: budget.py, quant.py or eval.py changed since the start ($(code_id) at $(git rev-parse --short HEAD))"
  step "$label"
  "$PY" scripts/budget.py --model "$model" --emb "$emb" --manifest "data/manifest_$set.jsonl" --dirs "data/dirs_$set.jsonl" \
    --gt "data/gt_structural_$set.jsonl" --calib-seed "$seed" --ranks "$ranks" --label "$label" --tag "_s21_$key" "$@" \
    > "$LOG/budget_$key.md" 2>> "$LOG/run.log"
  local rc=$?
  if [ $rc -ne 0 ]; then step "$label: budget.py stopped with exit code $rc"; [ -s "$LOG/budget_$key.md" ] && mv "$LOG/budget_$key.md" "$LOG/budget_$key.failed.md"; return 0; fi
  DONE_RUNS="$DONE_RUNS $key"
}
write_out() {
  OUT=results/session21_outputs.md
  {
    echo "# Session 21 outputs, verbatim"
    echo
    echo "Written by scripts/s19_followup.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
    echo "Nothing here is edited. The verdicts and the reading are in results/session21.md."
    echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
    for key in $DONE_RUNS; do echo; cat "$LOG/budget_$key.md"; done
    for f in "$LOG"/budget_*.failed.md; do [ -e "$f" ] && { echo; echo "## A run that stopped: $(basename "$f")"; echo; cat "$f"; }; done
  } > "$OUT"
  # per-query ranks of the E1 runs and of session 19 itself, so that a table can be recomputed without the pod
  local extra=""
  for pair in "data/emb/jina-embeddings-v4_s19/ranks_s21_s19_e1.jsonl:data/ranks_s21_s19_e1.jsonl.gz" \
              "data/emb/jina-embeddings-v4_s11/ranks_s21_s11_e1.jsonl:data/ranks_s21_s11_e1.jsonl.gz" \
              "data/emb/jina-embeddings-v4_s19/ranks_s19_e1.jsonl:data/ranks_s19_e1.jsonl.gz" \
              "/workspace/logs/s19/flags.jsonl:data/flags_s19.jsonl.gz" \
              "/workspace/logs/s19/commitq_ranks_e1.jsonl:data/commitq_ranks_s19_e1.jsonl.gz"; do
    local src=${pair%%:*} dst=${pair##*:}
    [ -s "$src" ] && gzip -c "$src" > "$dst" && extra="$extra $dst"
  done
  git add -f "$OUT" $extra || return 1
  git commit -q -m "$1" -m "$TRAILER1
$TRAILER2" -- "$OUT" $extra || return 1
  for i in 1 2 3 4; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 15
  done
  return 1
}

E1=jina-embeddings-v4; E2=jina-clip-v2; E3=gme-Qwen2-VL-2B-Instruct; E4=nomic-embed-v1.5
run s19_e1 "S19 E1" $E1 ${E1}_s19 s19 20261104 data/emb/${E1}_s19/ranks_s19_e1.jsonl --registered
run s11_e1 "S11 E1" $E1 ${E1}_s11 s11 20261102 data/emb/${E1}_s11/ranks_s11_e1.jsonl
write_out "session 21: outputs of the byte-budget runs under E1 (S19 and S11), verbatim" && step "E1 outputs pushed" || step "push of the E1 outputs failed"
run s19_e4 "S19 E4" $E4 ${E4}_s19 s19 20261104 data/emb/${E4}_s19/ranks_s19_e4.jsonl
run s19_e2 "S19 E2" $E2 ${E2}_s19 s19 20261104 data/emb/${E2}_s19/ranks_s19_e2.jsonl
run s11_e4 "S11 E4" $E4 ${E4}_s11 s11 20261102 data/emb/${E4}_s11/ranks_s15_e4.jsonl
run s11_e2 "S11 E2" $E2 ${E2}_s11 s11 20261102 data/emb/${E2}_s11/ranks_s11_e2.jsonl
run s11_e3 "S11 E3" $E3 ${E3}_s11 s11 20261102 data/emb/${E3}_s11/ranks_s14_e3.jsonl
step "session 21 done:$DONE_RUNS"
write_out "session 21: outputs of the byte-budget runs (S19 under E1, E4, E2; S11 under E1 to E4), verbatim" || { step "push of the outputs failed"; exit 1; }
rc=0
case " $DONE_RUNS " in *" s19_e1 "*) ;; *) echo "the registered run (S19 E1) did not finish" >> "$LOG/run.log"; rc=2;; esac
# session 24 (a second draw of GitHub directories, BRIEF.md), then session 21's tests on it
if [ -f scripts/s24_run.sh ] && [ -z "${S24_SKIP:-}" ]; then
  step "session 24: scripts/s24_run.sh at $(git rev-parse --short HEAD)"
  if bash scripts/s24_run.sh > /workspace/logs/s24_driver.log 2>&1; then
    step "session 24 done"
    run s24_e1 "S24 E1" $E1 ${E1}_s24 s24 20261104 data/emb/${E1}_s24/ranks_s24_e1.jsonl --registered
    if [ -s "$LOG/budget_s24_e1.md" ]; then
      OUT24=results/session24_budget_outputs.md
      {
        echo "# Session 24, the byte-budget runs of session 21 on the second draw (E1), verbatim"
        echo
        echo "Written by scripts/s19_followup.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
        echo "Nothing here is edited. scripts/budget.py printed the tables, so the test names say H21a, H21b and H21c:"
        echo "on this draw they are the replication registered in BRIEF.md, session 24 (H24e, H24f, H24g)."
        echo; cat "$LOG/budget_s24_e1.md"
      } > "$OUT24"
      gzip -c "data/emb/${E1}_s24/ranks_s21_s24_e1.jsonl" > data/ranks_s21_s24_e1.jsonl.gz
      git add -f "$OUT24" data/ranks_s21_s24_e1.jsonl.gz \
        && git commit -q -m "session 24: outputs of the byte-budget run on the second draw (E1), verbatim" -m "$TRAILER1
$TRAILER2" -- "$OUT24" data/ranks_s21_s24_e1.jsonl.gz
      for i in 1 2 3 4; do
        git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && { step "session 24 byte-budget outputs pushed"; break; }
        sleep 15
      done
    fi
  else
    step "session 24 failed (see /workspace/logs/s24/run.log)"
  fi
fi
# session 23 (whole repository trees, BRIEF.md) on the same pod, if its driver is in the repository by now
if [ -f scripts/s23_run.sh ] && [ -z "${S23_SKIP:-}" ]; then
  step "session 23: scripts/s23_run.sh at $(git rev-parse --short HEAD)"
  bash scripts/s23_run.sh > /workspace/logs/s23_driver.log 2>&1 && step "session 23 done" || step "session 23 failed (see /workspace/logs/s23/run.log)"
fi
exit $rc
