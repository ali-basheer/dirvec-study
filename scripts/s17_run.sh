#!/bin/bash
# Session 17: validity checks of the minority-modality loss (BRIEF.md, session 17). CPU only, on the
# ranks and caches already on the volume; nothing is embedded.
# Run on the pod from anywhere: bash scripts/s17_run.sh
# Writes $LOG/{env.txt,ranks_files.txt,indep_e1.md,indep_e1.jsonl,descq_e1..e4.md,descq_ranks_e1..e4.jsonl,
# validity_s11.md,validity_s3.md,validity_s5.md,flags_s11.jsonl,run.log}. When every step succeeds it writes
# results/session17_outputs.md (the outputs verbatim), commits and pushes that one file and touches $LOG/DONE.
# A failed reproduction (validity.py exit 3) or any failed step touches $LOG/FAILED and stops. The pod watcher
# (scripts/pod_autostop.sh) looks for either marker.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S17_LOG:-/workspace/logs/s17}
PY=${S17_PY:-/workspace/venv/bin/python}
mkdir -p "$LOG"
cd "$REPO" || exit 1
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-3} OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-3} DIRVEC_THREADS=${DIRVEC_THREADS:-3}
rm -f "$LOG/DONE" "$LOG/FAILED" "$LOG"/descq_ranks_e*.jsonl

fail() { echo "FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }

ENC="E1|jina-embeddings-v4|jina-embeddings-v4_s11|ranks_s11_e1
E2|jina-clip-v2|jina-clip-v2_s11|ranks_s11_e2
E3|gme-Qwen2-VL-2B-Instruct|gme-Qwen2-VL-2B-Instruct_s11|ranks_s14_e3
E4|nomic-embed-v1.5|nomic-embed-v1.5_s11|ranks_s15_e4"

step "start, commit $(git rev-parse --short HEAD), threads $OMP_NUM_THREADS"
"$PY" - > "$LOG/env.txt" 2>> "$LOG/run.log" <<'PY' || fail "environment"
import sys, os, numpy, sklearn, scipy
print("python", sys.version.split()[0], "numpy", numpy.__version__, "scikit-learn", sklearn.__version__,
      "scipy", scipy.__version__, "cpus", len(os.sched_getaffinity(0)))
PY
RANKS=""
DESCQ=""
while IFS='|' read -r E MODEL EMB R; do
  for f in "data/emb/$EMB/index.jsonl" "data/emb/$EMB/$R.jsonl" "data/emb/$EMB/descq_s12.npz"; do
    [ -s "$f" ] || fail "missing $f"
  done
  e=$(echo "$E" | tr 'E' 'e')
  RANKS="$RANKS${RANKS:+,}$E=data/emb/$EMB/$R.jsonl"
  DESCQ="$DESCQ${DESCQ:+,}$E=$LOG/descq_ranks_$e.jsonl"
done <<< "$ENC"
[ -f data/desc_s11.jsonl ] || gunzip -k data/desc_s11.jsonl.gz || fail "gunzip desc"
ls -la data/emb/*/ranks*.jsonl > "$LOG/ranks_files.txt" 2>&1

step "independent re-implementation, E1 (H17c)"
"$PY" scripts/indep_eval.py --manifest data/manifest_s11.jsonl --dirs data/dirs_s11.jsonl --gt data/gt_structural_s11.jsonl \
  --emb data/emb/jina-embeddings-v4_s11 --calib 0.2 --calib-seed 20261102 --out "$LOG/indep_e1.jsonl" \
  --check data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl > "$LOG/indep_e1.md" 2>> "$LOG/run.log" < /dev/null || fail "indep_eval"

while IFS='|' read -r E MODEL EMB R; do
  e=$(echo "$E" | tr 'E' 'e')
  step "descq eval with per-query ranks, $E"
  "$PY" scripts/descq.py eval --model "$MODEL" --emb "$EMB" --dump-ranks "$LOG/descq_ranks_$e.jsonl" \
    > "$LOG/descq_$e.md" 2>> "$LOG/run.log" < /dev/null || fail "descq $E"
done <<< "$ENC"
grep -q "c - a on image-heavy directories, Q_title, recall@5 = +0.182 \[+0.158, +0.206\]" "$LOG/descq_e1.md" \
  || fail "descq E1 does not reproduce the published H12a statistic"
step "descq E1 reproduces H12a (+0.182 [+0.158, +0.206])"

step "validity checks, S11"
S17_FLAGS="$LOG/flags_s11.jsonl" "$PY" scripts/validity.py --set s11 --ranks "$RANKS" \
  --index data/emb/jina-embeddings-v4_s11/index.jsonl --indep "$LOG/indep_e1.jsonl" --descq "$DESCQ" \
  > "$LOG/validity_s11.md" 2>> "$LOG/run.log" < /dev/null
rc=$?
[ $rc -eq 3 ] && fail "validity.py does not reproduce eval.py's published intervals (see $LOG/validity_s11.md)"
[ $rc -ne 0 ] && fail "validity.py exit $rc"
grep -h '^H17' "$LOG/validity_s11.md" | cut -c1-160 | while read -r l; do step "$l"; done

for s in s3 s5; do
  f="data/emb/jina-embeddings-v4_$s/ranks.jsonl"
  if [ -s "$f" ]; then
    step "clustered c - a, $s (secondary)"
    "$PY" scripts/validity.py --set "$s" --ranks "E1=$f" --light > "$LOG/validity_$s.md" 2>> "$LOG/run.log" < /dev/null \
      || fail "validity $s"
  else
    echo "no ranks file at $f" > "$LOG/validity_$s.md"
    step "no ranks file for $s"
  fi
done

OUT=results/session17_outputs.md
{
  echo "# Session 17 outputs, verbatim"
  echo
  echo "Written by scripts/s17_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and the reading are in results/session17.md."
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
  echo
  echo '## Ranks files on the volume'
  echo
  echo '```'
  cat "$LOG/ranks_files.txt"
  echo '```'
  echo
  echo '## indep_eval.py, E1 on S11 (H17c input)'
  echo
  cat "$LOG/indep_e1.md"
  echo
  cat "$LOG/validity_s11.md"
  for s in s3 s5; do
    echo
    cat "$LOG/validity_$s.md"
  done
  for e in e1 e2 e3 e4; do
    echo
    echo "## descq.py eval, $e (rerun to dump per-query ranks; the numbers must equal session 12, 14 and 15)"
    echo
    cat "$LOG/descq_$e.md"
  done
} > "$OUT"
step "commit and push $OUT"
git add "$OUT" || fail "git add"
git commit -q -m "session 17: outputs of the validity checks (creator clustering, filename fingerprints, same-stem siblings, independent re-implementation), verbatim" -- "$OUT" || fail "git commit"
pushed=no
for i in 1 2 3; do
  if git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1; then pushed=yes; break; fi
  sleep 10
done
[ "$pushed" = yes ] || fail "git push"
step "session 17 done"
touch "$LOG/DONE"
