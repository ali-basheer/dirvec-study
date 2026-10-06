#!/bin/bash
# Session 16: the target type known in advance (BRIEF.md, session 16). CPU only, the S11 caches.
# Run on the pod from anywhere: bash scripts/s16_run.sh
# Writes $LOG/{env.txt,typeq_e1.md..typeq_e4.md,run.log}. When every encoder's run succeeds it writes
# results/session16_outputs.md (the outputs verbatim), commits and pushes that one file and touches
# $LOG/DONE. If a reproduction check or a self-test fails (typeq.py exits 3 or 4) or any step fails, it
# touches $LOG/FAILED and stops; the outputs so far stay in $LOG. The pod watcher
# (scripts/pod_autostop.sh) looks for either marker.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S16_LOG:-/workspace/logs/s16}
PY=${S16_PY:-/workspace/venv/bin/python}
mkdir -p "$LOG"
cd "$REPO" || exit 1
export DIRVEC_THREADS=${DIRVEC_THREADS:-3} OMP_NUM_THREADS=${OMP_NUM_THREADS:-3} OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-3}
rm -f "$LOG/DONE" "$LOG/FAILED"

fail() { echo "FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }

COMMON="--manifest data/manifest_s11.jsonl --dirs data/dirs_s11.jsonl --gt data/gt_structural_s11.jsonl --calib 0.2 --calib-seed 20261102 --selftest 200"
ENC="E1|jina-embeddings-v4|jina-embeddings-v4_s11|ranks_s11_e1
E2|jina-clip-v2|jina-clip-v2_s11|ranks_s11_e2
E3|gme-Qwen2-VL-2B-Instruct|gme-Qwen2-VL-2B-Instruct_s11|ranks_s14_e3
E4|nomic-embed-v1.5|nomic-embed-v1.5_s11|ranks_s15_e4"

step "start, commit $(git rev-parse --short HEAD), threads $OMP_NUM_THREADS"
"$PY" - > "$LOG/env.txt" 2>> "$LOG/run.log" <<'PY' || fail "environment"
import sys, numpy, sklearn, os
print("python", sys.version.split()[0], "numpy", numpy.__version__, "scikit-learn", sklearn.__version__,
      "cpus", len(os.sched_getaffinity(0)))
PY
while IFS='|' read -r E MODEL EMB RANKS; do
  for f in "data/emb/$EMB/vectors.npy" "data/emb/$EMB/index.jsonl" "data/emb/$EMB/$RANKS.jsonl"; do
    [ -s "$f" ] || fail "missing $f"
  done
done <<< "$ENC"

while IFS='|' read -r E MODEL EMB RANKS; do
  e=$(echo "$E" | tr 'E' 'e')
  step "typeq $E ($MODEL)"
  "$PY" scripts/typeq.py --model "$MODEL" --emb "$EMB" $COMMON --check-ranks "data/emb/$EMB/$RANKS.jsonl" \
    --label "$E" --tag "_s16_$e" > "$LOG/typeq_$e.md" 2>> "$LOG/run.log" < /dev/null
  rc=$?
  [ $rc -eq 3 ] && fail "typeq $E: the a, c, d ranks do not reproduce $RANKS (see $LOG/typeq_$e.md)"
  [ $rc -eq 4 ] && fail "typeq $E: self-test differences (see $LOG/typeq_$e.md)"
  [ $rc -ne 0 ] && fail "typeq $E exit $rc"
  step "$(grep -h '^Reproduction' "$LOG/typeq_$e.md" | cut -c1-200)"
  step "$(grep -h '^Self-test' "$LOG/typeq_$e.md")"
  grep -h '^H16' "$LOG/typeq_$e.md" | cut -c1-120 | while read -r l; do step "$l"; done
done <<< "$ENC"

OUT=results/session16_outputs.md
{
  echo "# Session 16 outputs, verbatim"
  echo
  echo "Written by scripts/s16_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and the reading are in results/session16.md."
  echo
  echo '## Run log'
  echo
  echo '```'
  cat "$LOG/run.log"
  echo '```'
  echo
  echo '## Environment'
  echo
  echo '```'
  cat "$LOG/env.txt"
  echo '```'
  for e in e1 e2 e3 e4; do
    echo
    cat "$LOG/typeq_$e.md"
  done
} > "$OUT"
step "commit and push $OUT"
git add "$OUT" || fail "git add"
git commit -q -m "session 16: outputs of the known-target-type run (filter, prior, type-only groups; E1 to E4 on S11), verbatim" -- "$OUT" || fail "git commit"
pushed=no
for i in 1 2 3; do
  if git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1; then pushed=yes; break; fi
  sleep 10
done
[ "$pushed" = yes ] || fail "git push"
step "session 16 done"
touch "$LOG/DONE"
