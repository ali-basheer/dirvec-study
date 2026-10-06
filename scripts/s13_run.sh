#!/bin/bash
# Session 13: correction rerun of the session 9 dev grids and test split with the fixed ranking.
# CPU only. Run on the pod from anywhere: bash scripts/s13_run.sh
# Writes $LOG/{selftest.txt,dev.md,devcv.md,test.md,check.md,run.log}; when every step succeeds it
# writes results/session13_outputs.md (the outputs verbatim), commits and pushes that one file and
# touches $LOG/DONE. On any failure it touches $LOG/FAILED and stops. The pod watcher looks for
# either marker.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S13_LOG:-/workspace/logs/s13}
PY=${S13_PY:-/workspace/venv/bin/python}
mkdir -p "$LOG"
cd "$REPO" || exit 1
export DIRVEC_THREADS=${DIRVEC_THREADS:-3} OMP_NUM_THREADS=${OMP_NUM_THREADS:-3} OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-3}
rm -f "$LOG/DONE" "$LOG/FAILED"

COMMON="--model jina-embeddings-v4 --emb jina-embeddings-v4_s5 --manifest data/manifest_s5.jsonl --dirs data/dirs_s5.jsonl --gt data/gt_structural_s5.jsonl --criterion s3 --calib 0.2 --s9"
REF="a,b,c,d,ac,cc,dc"
AL="0 0.25 0.5 0.75 1"
names() { local out=""; for s in "$@"; do for a in $AL; do out="$out,${s}_p${a}"; done; done; echo "${out#,}"; }
F1=$(names u c)
F2=$(names proc coral ridge1 ridge10 ridge100 ridge1000)
F3="b2,bc2,bc"
F4=$(out=""; for b in f4 f4b; do for w in $AL; do out="$out,${b}_w${w}"; done; done; echo "${out#,}")
F5="tb2,tbg,tbc,tb2c,tbgc,tbcc"
# dev: the 66 names of session 9 plus ab and acb (the session 8 rows that u_p0 and c_p0 must equal)
DEV="$REF,ab,acb,$F1,$F2,$F3,$F4,$F5"
# cross-fitted dev: the 37 names of session 9
DEVCV="$REF,$F2"
# test: the 33 rows of session 9, ab and acb, and every other F2 name, so that whatever the corrected
# dev grids select is already scored
TEST="$REF,ab,acb,$F1,$F2,b2,bc2,bc,f4_w0.5,$F5"

fail() { echo "FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }

step "start, commit $(git rev-parse --short HEAD), threads $DIRVEC_THREADS, $($PY -c 'import numpy, sklearn; print("numpy", numpy.__version__, "scikit-learn", sklearn.__version__)')"
step "selftest"
$PY scripts/selftest_ranks.py > "$LOG/selftest.txt" 2>> "$LOG/run.log" || fail selftest
step "dev grid (literal)"
$PY scripts/eval.py $COMMON --queries dev --reps "$DEV" --tag _s13dev > "$LOG/dev.md" 2>> "$LOG/run.log" || fail "dev grid"
step "dev grid (two-fold cross-fitted F2)"
$PY scripts/eval.py $COMMON --queries dev --align-cv --reps "$DEVCV" --tag _s13devcv > "$LOG/devcv.md" 2>> "$LOG/run.log" || fail "cross-fitted dev grid"
step "test split"
$PY scripts/eval.py $COMMON --queries eval --reps "$TEST" --tag _s13test > "$LOG/test.md" 2>> "$LOG/run.log" || fail "test split"
step "rank checks"
$PY scripts/s13_check.py > "$LOG/check.md" 2>> "$LOG/run.log"
CHECK=$?
step "rank checks exit $CHECK"

OUT=results/session13_outputs.md
{
  echo "# Session 13 outputs, verbatim"
  echo
  echo "Written by scripts/s13_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdict and the reading are in results/session13.md."
  echo
  echo '## Run log'
  echo
  echo '```'
  grep -v '^  rep \|^  aligned\|^  fold' "$LOG/run.log"
  echo '```'
  echo
  echo '## scripts/selftest_ranks.py'
  echo
  echo '```'
  cat "$LOG/selftest.txt"
  echo '```'
  echo
  echo '## scripts/s13_check.py'
  cat "$LOG/check.md"
  echo
  echo '## Dev grid, literal (`--queries dev`, tag _s13dev)'
  echo
  cat "$LOG/dev.md"
  echo
  echo '## Dev grid, two-fold cross-fitted F2 (`--queries dev --align-cv`, tag _s13devcv)'
  echo
  cat "$LOG/devcv.md"
  echo
  echo '## Test split (`--queries eval`, tag _s13test)'
  echo
  cat "$LOG/test.md"
} > "$OUT"

step "commit and push $OUT"
git add "$OUT" || fail "git add"
git commit -q -m "session 13: outputs of the correction rerun, verbatim (selftest, rank checks, dev grid, cross-fitted dev grid, test split)" -- "$OUT" || fail "git commit"
for i in 1 2 3; do
  git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && break
  sleep 10
  [ "$i" = 3 ] && fail "git push"
done
step "session 13 done"
touch "$LOG/DONE"
