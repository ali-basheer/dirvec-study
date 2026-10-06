#!/bin/bash
# Session 26 on the pod (BRIEF.md, session 26): s26.py score on the caches already on the volume,
# then s26.py report; the per-query npz files and the report are pushed. Nothing is embedded.
# Writes $LOG/DONE or $LOG/FAILED at the end; scripts/pod_autostop.sh watches for them.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
LOG=${S26_LOG:-/workspace/logs/s26}
PY=${S26_PY:-/workspace/venv/bin/python}
TRAILERS="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01VJwLKMD3oGsGT8vRdtj6Es"
mkdir -p "$LOG"
rm -f "$LOG/run.log" "$LOG/DONE" "$LOG/FAILED"
export DIRVEC_THREADS=3 OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3 TOKENIZERS_PARALLELISM=false

step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
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

step "start, commit $(git rev-parse --short HEAD), $(nproc) cores"
E1=jina-embeddings-v4; E2=jina-clip-v2; E3=gme-Qwen2-VL-2B-Instruct; E4=nomic-embed-v1.5
# set|enc|cache|check ranks|flags|calibration seed
RUNS="s19|E1|$E1|data/ranks_s19_e1.jsonl.gz|data/flags_s19.jsonl.gz|20261104
s24|E1|$E1|data/ranks_s24_e1.jsonl.gz|data/flags_s24.jsonl.gz|20261104
s11|E1|$E1|data/emb/${E1}_s11/ranks_s11_e1.jsonl||20261102
s11|E3|$E3|data/emb/${E3}_s11/ranks_s14_e3.jsonl||20261102
s11|E2|$E2|data/emb/${E2}_s11/ranks_s11_e2.jsonl||20261102
s11|E4|$E4|data/emb/${E4}_s11/ranks_s15_e4.jsonl||20261102
s19|E4|$E4|data/emb/${E4}_s19/ranks_s19_e4.jsonl||20261104
s19|E2|$E2|data/emb/${E2}_s19/ranks_s19_e2.jsonl||20261104"
NPZ=""
while IFS='|' read -r S E M CHECK FLAGS SEED; do
  e=$(echo "$E" | tr 'E' 'e')
  EMB="data/emb/${M}_$S"
  if [ ! -s "$EMB/vectors.npy" ]; then step "$S $E: no cache at $EMB, skipped"; continue; fi
  if [ ! -s "$CHECK" ] && [ "$S $E" = "s11 E1" ]; then CHECK=data/ranks_s21_s11_e1.jsonl.gz; fi
  if [ ! -s "$CHECK" ]; then step "$S $E: no stored ranks at $CHECK, skipped"; continue; fi
  OUT="data/s26_${S}_$e.npz"
  step "$S $E: score ($EMB, check $CHECK${FLAGS:+, flags $FLAGS})"
  "$PY" scripts/s26.py score --set "$S" --emb "$EMB" --enc "$E" --calib-seed "$SEED" --check "$CHECK" \
    ${FLAGS:+--flags "$FLAGS"} --out "$OUT" --procs 3 > "$LOG/score_${S}_$e.json" 2> "$LOG/score_${S}_$e.log" < /dev/null
  rc=$?
  step "$S $E: exit $rc; $(tail -1 "$LOG/score_${S}_$e.log" | cut -c1-400)"
  [ -s "$OUT" ] && NPZ="$NPZ $OUT"
done <<< "$RUNS"

OUT=results/session26_outputs.md
{
  # shellcheck disable=SC2086
  "$PY" scripts/s26.py report $NPZ 2> "$LOG/report.log" || echo "REPORT FAILED: $(tail -3 "$LOG/report.log")"
  echo
  echo "Written by scripts/s26_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and the reading are in results/session26.md."
  echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
} > "$OUT.tmp" && mv "$OUT.tmp" "$OUT"
# shellcheck disable=SC2086
if push "session 26 outputs: representatives for mixed folders at the natural mix, names with vectors (verbatim)" "$OUT" $NPZ; then
  step "session 26 done"
  touch "$LOG/DONE"
else
  step "push FAILED"
  touch "$LOG/FAILED"
fi
