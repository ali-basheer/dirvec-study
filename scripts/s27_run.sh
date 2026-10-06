#!/bin/bash
# Session 27 on the pod, first half (BRIEF.md, session 27): the 27A sample and the payload of the query
# tool, then 27B (the budget sweep) and 27C (the k-means seeds) from the cached S11 vectors under E1 to E4,
# and the uncentered sweep on G2 (S24) under E1 if its cache is on the volume. Nothing is embedded.
#   S27_BRIEF=<commit>   the brief's commit; the run stops unless it is an ancestor of HEAD
#   S27_PROCS=4          worker processes (default: the cores)
#   S27_RESUME=1         skip a scoring step whose npz file exists
# The sample is pushed to main as soon as it exists; the payload goes to the branch humanq-payload as a
# commit with no parent (never to main); the npz files and results/session27_budget_outputs.md are pushed
# at the end. $LOG/DONE or $LOG/FAILED tells scripts/pod_autostop.sh to stop the pod.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
LOG=${S27_LOG:-/workspace/logs/s27}
PY=${S27_PY:-/workspace/venv/bin/python}
PROCS=${S27_PROCS:-$(nproc)}
TMP=${S27_TMP:-/root/tmp_s27}
TRAILERS="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01XgSYkhgAuaKciibnZZLb5Q"
mkdir -p "$LOG" "$TMP"
rm -f "$LOG/DONE" "$LOG/FAILED"
export OMP_NUM_THREADS=$PROCS OPENBLAS_NUM_THREADS=$PROCS MKL_NUM_THREADS=$PROCS TOKENIZERS_PARALLELISM=false

step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
fail() { step "FAILED at: $1"; touch "$LOG/FAILED"; exit 1; }
have() { [ -n "${S27_RESUME:-}" ] && [ -s "$1" ]; }
push() {  # push "<message>" file...
  local msg=$1; shift
  git add -f "$@" || fail "git add"
  git commit -q -m "$msg" -m "$TRAILERS" -- "$@" || fail "git commit"
  for i in 1 2 3 4; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 15
  done
  fail "git push"
}

step "start, commit $(git rev-parse --short HEAD), $(nproc) cores, $PROCS processes"
[ -n "${S27_BRIEF:-}" ] && git merge-base --is-ancestor "$S27_BRIEF" HEAD || fail "the brief's commit ${S27_BRIEF:-(not given)} is not in HEAD"
"$PY" - > "$LOG/env.txt" 2>> "$LOG/run.log" <<'PY' || fail "environment"
import sys, numpy, sklearn, scipy, PIL
print("python", sys.version.split()[0], "numpy", numpy.__version__, "scikit-learn", sklearn.__version__,
      "scipy", scipy.__version__, "pillow", PIL.__version__)
PY
cat "$LOG/env.txt" >> "$LOG/run.log"

E1=jina-embeddings-v4; E2=jina-clip-v2; E3=gme-Qwen2-VL-2B-Instruct; E4=nomic-embed-v1.5
IDX="E1=data/emb/${E1}_s11/index.jsonl,E2=data/emb/${E2}_s11/index.jsonl,E3=data/emb/${E3}_s11/index.jsonl,E4=data/emb/${E4}_s11/index.jsonl"

# ---- 27A: the sample, then the payload of the tool
if git ls-files --error-unmatch data/humanq_sample_s11.jsonl > /dev/null 2>&1; then
  "$PY" scripts/humanq_tool.py sample --index "$IDX" --check >> "$LOG/run.log" 2>&1 || fail "sample check"
  step "sample: the committed file reproduces"
else
  "$PY" scripts/humanq_tool.py sample --index "$IDX" >> "$LOG/run.log" 2>&1 || fail "sample"
  push "session 27: the 27A sample (folders, targets and display order drawn by the brief's rule), before any query is written" \
    data/humanq_sample_s11.jsonl
  step "sample pushed"
fi
if have build/humanq/payload_s11.json.gz; then
  step "payload present"
else
  step "payload"
  "$PY" scripts/humanq_tool.py payload > "$LOG/payload.log" 2>&1 || fail "payload"
  tail -1 "$LOG/payload.log" | tee -a "$LOG/run.log"
fi
blob=$(git hash-object -w build/humanq/payload_s11.json.gz) || fail "payload blob"
tree=$(printf '100644 blob %s\tpayload_s11.json.gz\n' "$blob" | git mktree) || fail "payload tree"
pc=$(git commit-tree "$tree" -m "session 27: the payload of the query tool (thumbnails and text heads of the sampled folders); this branch is deleted once the tool is built" -m "$TRAILERS") || fail "payload commit"
for i in 1 2 3 4; do
  git push -q -f origin "$pc:refs/heads/humanq-payload" >> "$LOG/run.log" 2>&1 && { step "payload pushed to the branch humanq-payload ($pc)"; break; }
  sleep 15
  [ "$i" = 4 ] && fail "payload push"
done

# ---- 27B and 27C on S11
# encoder|cache|stored eval.py ranks on the volume
RUNS="E1|$E1|data/emb/${E1}_s11/ranks_s11_e1.jsonl
E2|$E2|data/emb/${E2}_s11/ranks_s11_e2.jsonl
E3|$E3|data/emb/${E3}_s11/ranks_s14_e3.jsonl
E4|$E4|data/emb/${E4}_s11/ranks_s15_e4.jsonl"
NPZ=""
while IFS='|' read -r E M CHECK; do
  e=$(echo "$E" | tr 'E' 'e')
  EMB="data/emb/${M}_s11"
  [ -s "$EMB/vectors.npy" ] || { step "$E: no cache at $EMB, skipped"; continue; }
  CHK=(--check "$CHECK")
  [ "$E" = E1 ] && CHK+=(--check data/ranks_s21_s11_e1.jsonl.gz)
  for kind in budget seeds; do
    OUT="data/s27$([ "$kind" = seeds ] && echo seeds)_s11_$e.npz"
    if have "$OUT"; then step "$E $kind: present"; NPZ="$NPZ $OUT"; continue; fi
    step "$E $kind"
    "$PY" scripts/s27.py "$kind" --set s11 --emb "$EMB" --enc "$E" --calib-seed 20261102 "${CHK[@]}" --out "$OUT" \
      --procs "$PROCS" --tmp "$TMP" > "$LOG/${kind}_s11_$e.json" 2> "$LOG/${kind}_s11_$e.log" < /dev/null
    rc=$?
    step "$E $kind: exit $rc; $(grep -o '"gate": .*' "$LOG/${kind}_s11_$e.json" | cut -c1-600)"
    [ -s "$OUT" ] && NPZ="$NPZ $OUT"
  done
done <<< "$RUNS"

# ---- G2 (S24) under E1, uncentered, secondary
if [ -s "data/emb/${E1}_s24/vectors.npy" ]; then
  OUT=data/s27_s24_e1.npz
  if have "$OUT"; then step "G2: present"; else
    step "G2 budget"
    "$PY" scripts/s27.py budget --set s24 --emb "data/emb/${E1}_s24" --enc E1 --calib-seed 20261104 \
      --check data/ranks_s24_e1.jsonl.gz --flags data/flags_s24.jsonl.gz --uncentered-only --out "$OUT" \
      --procs "$PROCS" --tmp "$TMP" > "$LOG/budget_s24_e1.json" 2> "$LOG/budget_s24_e1.log" < /dev/null
    step "G2: exit $?; $(grep -o '"gate": .*' "$LOG/budget_s24_e1.json" | cut -c1-400)"
  fi
  [ -s "$OUT" ] && NPZ="$NPZ $OUT"
else
  step "G2: no E1 cache for S24 on the volume, skipped"
fi

OUTMD=results/session27_budget_outputs.md
{
  # shellcheck disable=SC2086
  "$PY" scripts/s27.py report $NPZ 2> "$LOG/report.log" || echo "REPORT FAILED: $(tail -3 "$LOG/report.log")"
  echo
  echo "Written by scripts/s27_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The readings are in results/session27_budget.md."
  echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
} > "$OUTMD.tmp" && mv "$OUTMD.tmp" "$OUTMD"
# shellcheck disable=SC2086
push "session 27 outputs: the budget sweep and the k-means seeds (27B, 27C), verbatim" "$OUTMD" $NPZ
step "session 27 (first half) done"
touch "$LOG/DONE"
