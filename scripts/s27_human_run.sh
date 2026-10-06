#!/bin/bash
# Session 27 on the pod, second half (BRIEF.md, session 27, part A and its amendment): the 27A queries,
# embedded under E1 to E4 with each encoder's query text path (s27.py human-embed), scored against every S11
# folder after the title gate (s27.py human-eval), and reported (s27.py human-report). Run it only after
# data/humanq_s11.jsonl is committed. Needs the GPU of the MIG pod; E3 and E4 weights are downloaded to the
# container disk, E1 and E2 are on the volume (/workspace/hf).
#   S27_QUERIES=data/humanq_s11.jsonl   the export to score (committed)
#   S27_ENCODERS="E1 E2 E3 E4"          E1 decides the verdicts
# $LOG/DONE or $LOG/FAILED tells scripts/pod_autostop.sh to stop the pod.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
LOG=${S27_LOG:-/workspace/logs/s27h}
PY=${S27_PY:-/workspace/venv/bin/python}
QUERIES=${S27_QUERIES:-data/humanq_s11.jsonl}
ENCODERS=${S27_ENCODERS:-"E1 E2 E3 E4"}
TF=${S27_TF:-/root/tf451}             # transformers 4.51.3 for E3, first on PYTHONPATH
HFE3=${S27_HFE3:-/root/hf_gme}
HFE4=${S27_HFE4:-/root/hf_nomic}
TRAILERS="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: ${S27_SESSION:-https://claude.ai/code/session_01XgSYkhgAuaKciibnZZLb5Q}"
mkdir -p "$LOG"
rm -f "$LOG/DONE" "$LOG/FAILED"
export TOKENIZERS_PARALLELISM=false HF_HUB_ENABLE_HF_TRANSFER=0
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
fail() { step "FAILED at: $1"; touch "$LOG/FAILED"; exit 1; }
push() {
  local msg=$1; shift
  git add -f "$@" || fail "git add"
  git commit -q -m "$msg" -m "$TRAILERS" -- "$@" || fail "git commit"
  for i in 1 2 3 4; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 15
  done
  fail "git push"
}
model_of() { case $1 in E1) echo jina-embeddings-v4;; E2) echo jina-clip-v2;; E3) echo gme-Qwen2-VL-2B-Instruct;; E4) echo nomic-embed-v1.5;; esac; }
enc_py() {
  local e=$1; shift
  case $e in
    E1|E2) HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PY" "$@";;
    E3) HF_HOME="$HFE3" HF_HUB_OFFLINE=0 PYTHONPATH="$TF" "$PY" "$@";;
    E4) HF_HOME="$HFE4" HF_HUB_OFFLINE=0 "$PY" "$@";;
  esac
}

step "start, commit $(git rev-parse --short HEAD), encoders $ENCODERS"
git ls-files --error-unmatch "$QUERIES" > /dev/null 2>&1 || fail "$QUERIES is not committed"
"$PY" scripts/humanq_tool.py sample --index "E1=data/emb/jina-embeddings-v4_s11/index.jsonl,E2=data/emb/jina-clip-v2_s11/index.jsonl,E3=data/emb/gme-Qwen2-VL-2B-Instruct_s11/index.jsonl,E4=data/emb/nomic-embed-v1.5_s11/index.jsonl" --check >> "$LOG/run.log" 2>&1 || fail "the sample does not reproduce"
case " $ENCODERS " in *" E3 "*)
  [ -d "$TF/transformers" ] || "$PY" -m pip install -q --no-deps --target "$TF" "transformers==4.51.3" >> "$LOG/run.log" 2>&1 || fail "pip transformers 4.51.3";;
esac
NPZ=""
for E in $ENCODERS; do
  e=$(echo "$E" | tr 'E' 'e')
  M=$(model_of "$E")
  EMB="data/emb/${M}_s11"
  step "$E: embed the queries"
  enc_py "$E" scripts/s27.py human-embed --model "$M" --emb "$EMB" --queries "$QUERIES" \
    > "$LOG/embed_$e.txt" 2> "$LOG/embed_$e.log" < /dev/null || fail "embed $E: $(tail -2 "$LOG/embed_$e.log")"
  step "$E: score"
  "$PY" scripts/s27.py human-eval --enc "$E" --emb "$EMB" --queries "$QUERIES" \
    --check-titles "/workspace/logs/s17/descq_ranks_$e.jsonl" --out "data/s27_human_$e.npz" \
    > "$LOG/eval_$e.json" 2> "$LOG/eval_$e.log" < /dev/null
  step "$E: exit $?; $(grep -o '"gate": .*' "$LOG/eval_$e.json" | cut -c1-300)"
  [ -s "data/s27_human_$e.npz" ] && NPZ="$NPZ data/s27_human_$e.npz"
done
OUT=results/session27_outputs.md
{
  # shellcheck disable=SC2086
  "$PY" scripts/s27.py human-report $NPZ 2> "$LOG/report.log" || echo "REPORT FAILED: $(tail -3 "$LOG/report.log")"
  echo
  echo "Written by scripts/s27_human_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and readings are in results/session27.md."
  echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
} > "$OUT.tmp" && mv "$OUT.tmp" "$OUT"
# shellcheck disable=SC2086
push "session 27 outputs: the 27A queries ($QUERIES), verbatim" "$OUT" $NPZ
step "session 27 (second half) done"
touch "$LOG/DONE"
