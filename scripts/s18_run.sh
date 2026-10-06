#!/bin/bash
# Session 18: written folder abstracts against per-modality representatives (BRIEF.md, session 18).
# Run on a full RTX PRO 6000 pod with the dirvec volume: bash scripts/s18_run.sh
# Steps: text heads (E1 venv, in the background) | vLLM venv | member descriptions (first describer
# that passes the smoke test) | captions and abstracts (first summarizer that passes) | E1 and E3
# embeddings of the generated texts | eval under E1 and E3 | outputs committed and pushed.
# Resumable: S18_RESUME=1 skips finished steps; generation steps skip items already written and keep the
# model that wrote them. Writes $LOG/DONE at the end, $LOG/FAILED on any failure (the pod watcher,
# scripts/pod_autostop.sh, looks for either).
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S18_LOG:-/workspace/logs/s18}
PYJ=${S18_PY:-/workspace/venv/bin/python}   # E1 venv: embed.py, eval.py, descq.py
VV=${S18_VV:-/root/vv}                       # vLLM venv on the container disk
TF=${S18_TF:-/root/tf451}                    # transformers 4.51.3 for E3, first on PYTHONPATH
HFG=${S18_HFGEN:-/root/hf_gen}               # summarizer and describer weights (container disk)
HFE3=${S18_HFE3:-/root/hf_gme}               # E3 weights (container disk, 8.8 GB)
GEN=data/emb/s18
SUMMARIZERS="Qwen/Qwen3-VL-8B-Instruct Qwen/Qwen2.5-VL-7B-Instruct"
DESCRIBERS="mistral-community/pixtral-12b HuggingFaceM4/Idefics3-8B-Llama3 llava-hf/llava-v1.6-mistral-7b-hf"
mkdir -p "$LOG" "$GEN"
cd "$REPO" || exit 1
export DIRVEC_THREADS=${DIRVEC_THREADS:-12} OMP_NUM_THREADS=${OMP_NUM_THREADS:-12} OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-12}
export HF_HUB_ENABLE_HF_TRANSFER=0 PIP_NO_CACHE_DIR=1 TOKENIZERS_PARALLELISM=false
# the pod image points the uv, pip and Hugging Face caches at /workspace; the volume quota cannot hold them
# (the first run of this driver failed there), so every cache goes to the container disk
export UV_CACHE_DIR=/root/.cache/uv PIP_CACHE_DIR=/root/.cache/pip XDG_CACHE_HOME=/root/.cache \
  VIRTUALENV_OVERRIDE_APP_DATA=/root/.cache/virtualenv VLLM_CACHE_ROOT=/root/.cache/vllm
RESUME=${S18_RESUME:-0}
rm -f "$LOG/DONE" "$LOG/FAILED"

fail() { echo "$(date -u +%H:%M:%S) FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
e1() { HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PYJ" "$@"; }
gme() { HF_HOME="$HFE3" HF_HUB_OFFLINE=0 PYTHONPATH="$TF" "$PYJ" "$@"; }
lines() { [ -s "$1" ] && wc -l < "$1" || echo 0; }

step "start, commit $(git rev-parse --short HEAD), resume $RESUME"
{
  nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
  df -h /root /workspace | tail -n 2
  echo "nproc $(nproc)"; free -g | head -n 2
  "$PYJ" -c 'import torch, transformers, sklearn; print("E1 venv: torch", torch.__version__, "transformers", transformers.__version__, "scikit-learn", sklearn.__version__)'
} > "$LOG/env.txt" 2>&1
for f in "data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl" "data/emb/jina-embeddings-v4_s11/descq_s12.npz" \
         "data/emb/gme-Qwen2-VL-2B-Instruct_s11/descq_s12.npz" "data/emb/gme-Qwen2-VL-2B-Instruct_s11/vectors.npy"; do
  [ -s "$f" ] || fail "missing $f"
done
[ -f data/desc_s11.jsonl ] || gunzip -k data/desc_s11.jsonl.gz || fail "gunzip desc"

# S18_FROM=eval: everything before the evaluation is done (its outputs are on the volume); go straight to eval
if [ "${S18_FROM:-start}" != eval ]; then
HEADS_PID=""
if [ -s "$GEN/heads.jsonl" ]; then
  step "text heads present ($(lines $GEN/heads.jsonl))"
else
  step "text heads (E1 venv, background)"
  ( e1 scripts/s18.py heads --workers 6 > "$LOG/heads.txt" 2> "$LOG/heads.log" < /dev/null; echo $? > "$LOG/heads.rc" ) &
  HEADS_PID=$!
fi

install_vllm() {
  rm -rf "$VV"
  step "vLLM venv: $*"
  { python3 -m pip install -q uv && python3 -m uv venv "$VV" --python python3 \
      && python3 -m uv pip install --python "$VV/bin/python" "$@" tifffile imagecodecs; } >> "$LOG/install.log" 2>&1 || return 1
  rm -rf "$UV_CACHE_DIR"
  "$VV/bin/python" -c 'import vllm, torch, transformers; print("vLLM venv: vllm", vllm.__version__, "torch", torch.__version__, "cuda", torch.version.cuda, "transformers", transformers.__version__)' \
    >> "$LOG/env.txt" 2>> "$LOG/install.log" || return 1
  step "$(tail -n 1 "$LOG/env.txt")"
}

# run_gen <stage> <output file> <models...>: the first model that passes the smoke test does the whole
# stage. A model is replaced only while the output holds nothing; a resume keeps the model of the output.
run_gen() {
  local stage=$1 out=$2 rc m prev
  shift 2
  prev=$(head -n 1 "$out" 2>/dev/null | "$PYJ" -c 'import json,sys; l=sys.stdin.read().strip(); print(json.loads(l)["model"] if l else "")')
  [ -n "$prev" ] && set -- "$prev"
  for m in "$@"; do
    step "$stage with $m"
    HF_HOME="$HFG" HF_HUB_OFFLINE=0 timeout 180m "$VV/bin/python" scripts/s18.py "$stage" --model "$m" --workers 12 \
      >> "$LOG/$stage.log" 2>&1 < /dev/null
    rc=$?
    rm -rf "$HFG/hub/models--${m//\//--}"
    step "$stage with $m: exit $rc, $(lines "$out") lines"
    [ $rc -eq 0 ] && return 0
    [ "$(lines "$out")" -gt 0 ] && return 2
  done
  return 10
}

[ -x "$VV/bin/python" ] && "$VV/bin/python" -c 'import vllm' 2>/dev/null || install_vllm "vllm==0.11.0" "transformers>=4.57,<4.58" \
  || fail "vLLM install (pinned)"
run_gen describe "$GEN/members.jsonl" $DESCRIBERS
rc=$?
if [ $rc -eq 10 ]; then
  step "no describer passed with the pinned vLLM; trying the latest vLLM"
  install_vllm "vllm" || fail "vLLM install (latest)"
  run_gen describe "$GEN/members.jsonl" $DESCRIBERS
  rc=$?
fi
[ $rc -eq 0 ] || fail "describe (exit $rc)"

if [ -n "$HEADS_PID" ]; then
  wait "$HEADS_PID"
  [ "$(cat "$LOG/heads.rc" 2>/dev/null)" = "0" ] || fail "text heads (see $LOG/heads.log)"
  step "$(cat "$LOG/heads.txt")"
fi
[ -s "$GEN/heads.jsonl" ] || fail "no text heads"

run_gen summarize "$GEN/captions.jsonl" $SUMMARIZERS
rc=$?
[ $rc -eq 0 ] || fail "summarize (exit $rc)"
step "captions $(lines $GEN/captions.jsonl), abstracts $(lines $GEN/abstracts.jsonl), members $(lines $GEN/members.jsonl)"

if [ "$RESUME" = 1 ] && [ -s data/emb/jina-embeddings-v4_s11/s18_vecs.npz ] && [ data/emb/jina-embeddings-v4_s11/s18_vecs.npz -nt "$GEN/abstracts.jsonl" ]; then
  step "E1 vectors present"
else
  step "embed, E1"
  e1 scripts/s18.py embed --model jina-embeddings-v4 --emb jina-embeddings-v4_s11 --batch 32 \
    > "$LOG/embed_e1.txt" 2> "$LOG/embed_e1.log" < /dev/null || fail "embed E1"
fi
if [ ! -d "$TF/transformers" ]; then
  "$PYJ" -m pip install -q --no-deps --target "$TF" "transformers==4.51.3" >> "$LOG/install.log" 2>&1 || fail "pip transformers 4.51.3"
fi
if [ "$RESUME" = 1 ] && [ -s data/emb/gme-Qwen2-VL-2B-Instruct_s11/s18_vecs.npz ] && [ data/emb/gme-Qwen2-VL-2B-Instruct_s11/s18_vecs.npz -nt "$GEN/abstracts.jsonl" ]; then
  step "E3 vectors present"
else
  step "embed, E3"
  gme scripts/s18.py embed --model gme-Qwen2-VL-2B-Instruct --emb gme-Qwen2-VL-2B-Instruct_s11 --batch 32 \
    > "$LOG/embed_e3.txt" 2> "$LOG/embed_e3.log" < /dev/null || fail "embed E3"
fi

else
  step "S18_FROM=eval: generation and embedding skipped (outputs on the volume)"
fi

for E in "e1 jina-embeddings-v4 jina-embeddings-v4_s11" "e3 gme-Qwen2-VL-2B-Instruct gme-Qwen2-VL-2B-Instruct_s11"; do
  set -- $E
  step "eval, $1"
  e1 scripts/s18.py eval --model "$2" --emb "$3" --repro "/workspace/logs/s17/descq_ranks_$1.jsonl" \
    --dump-ranks "$LOG/ranks_$1.jsonl" > "$LOG/eval_$1.md" 2>> "$LOG/eval.log" < /dev/null
  rc=$?
  [ $rc -eq 3 ] && fail "eval $1: a, c and d do not reproduce descq.py (see $LOG/eval_$1.md)"
  [ $rc -eq 0 ] || fail "eval $1 (exit $rc)"
  grep -h '^H18' "$LOG/eval_$1.md" | cut -c1-200 | while read -r l; do step "$l"; done
done

step "generated texts into data/s18 (gzip, raw model outputs kept for the member descriptions only)"
mkdir -p data/s18
"$PYJ" - <<'PY' || fail "slim copies"
import gzip, json
keep = {"captions": ["path", "caption", "model", "revision"],
        "abstracts": ["dir", "n_files", "l1", "l0", "sw1", "model", "revision"],
        "members": ["path", "dir", "cell", "bucket", "raw", "text", "name_tokens_removed", "model", "revision"]}
for name, ks in keep.items():
    with open(f"data/emb/s18/{name}.jsonl") as fi, gzip.open(f"data/s18/{name}.jsonl.gz", "wt") as fo:
        for l in fi:
            r = json.loads(l)
            fo.write(json.dumps({k: r.get(k) for k in ks}) + "\n")
PY

OUT=results/session18_outputs.md
{
  echo "# Session 18 outputs, verbatim"
  echo
  echo "Written by scripts/s18_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and the reading are in results/session18.md. The generated texts are in"
  echo "data/s18/ (captions, abstracts and member descriptions, gzipped json lines)."
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
  echo '## Generation and embedding summaries'
  echo
  echo '```'
  cat "$LOG/heads.txt" "$LOG/embed_e1.txt" "$LOG/embed_e3.txt" 2>/dev/null
  grep -h "smoke\|revision\|done:" "$LOG/describe.log" "$LOG/summarize.log" 2>/dev/null | cut -c1-240
  echo '```'
  echo
  cat "$LOG/eval_e1.md"
  echo
  cat "$LOG/eval_e3.md"
} > "$OUT"
step "commit and push $OUT and data/s18"
git add "$OUT" data/s18 || fail "git add"
git commit -q -m "session 18: outputs of the written-abstract run (abstracts, captions and member descriptions in data/s18; eval under E1 and E3), verbatim" -- "$OUT" data/s18 || fail "git commit"
pushed=no
for i in 1 2 3; do
  if git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1; then pushed=yes; break; fi
  sleep 10
done
[ "$pushed" = yes ] || fail "git push"
step "session 18 done"
touch "$LOG/DONE"
