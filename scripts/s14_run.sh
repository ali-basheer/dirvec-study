#!/bin/bash
# Session 14: the third encoder E3 (gme-Qwen2-VL-2B-Instruct) on the session 11 set (BRIEF.md, session 14).
# Run on the pod from anywhere: bash scripts/s14_run.sh
# Writes $LOG/{env.txt,pilot.json,gate.txt,embed.json,okset.txt,eval.md,descq.md,run.log}. When every
# step succeeds it writes results/session14_outputs.md (the outputs verbatim), commits and pushes that
# one file and touches $LOG/DONE. If the pilot gate fails it does the same with the pilot only (the
# brief's stop rule). On any other failure it touches $LOG/FAILED and stops. The pod watcher
# (scripts/pod_autostop.sh) looks for either marker.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S14_LOG:-/workspace/logs/s14}
PYJ=${S14_PY:-/workspace/venv/bin/python}   # the E1 venv: eval.py, descq.py eval, and E3 with TF below
TF=${S14_TF:-/root/tf451}                     # transformers 4.51.3 for E3, first on PYTHONPATH
HFG=${S14_HF:-/root/hf_gme}                   # E3 weights on the container disk (8.8 GB)
M=gme-Qwen2-VL-2B-Instruct
mkdir -p "$LOG"
cd "$REPO" || exit 1
export DIRVEC_THREADS=${DIRVEC_THREADS:-8} OMP_NUM_THREADS=${OMP_NUM_THREADS:-8} OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-8}
export HF_HUB_ENABLE_HF_TRANSFER=0 HF_HUB_OFFLINE=0
rm -f "$LOG/DONE" "$LOG/FAILED"

fail() { echo "FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
gme() { HF_HOME="$HFG" PYTHONPATH="$TF" "$PYJ" "$@"; }

write_outputs() {
  local OUT=results/session14_outputs.md
  {
    echo "# Session 14 outputs, verbatim"
    echo
    echo "Written by scripts/s14_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
    echo "Nothing here is edited. The verdicts and the reading are in results/session14.md."
    echo
    echo '## Run log'
    echo
    echo '```'
    grep -v '^  prepared \|^  embedded ' "$LOG/run.log"
    echo '```'
    echo
    echo '## Environment'
    echo
    echo '```'
    cat "$LOG/env.txt"
    echo '```'
    echo
    echo '## Pilot (`embed.py pilot`, report data/emb/pilot/gme-Qwen2-VL-2B-Instruct_s11.json)'
    echo
    echo '```'
    cat "data/emb/pilot/${M}_s11.json" 2>/dev/null || cat "$LOG/pilot.json"
    echo '```'
    echo
    echo '## Gate'
    echo
    echo '```'
    cat "$LOG/gate.txt"
    echo '```'
    for f in embed.json okset.txt; do
      if [ -s "$LOG/$f" ]; then
        echo
        echo "## $f"
        echo
        echo '```'
        cat "$LOG/$f"
        echo '```'
      fi
    done
    if [ -s "$LOG/eval.md" ]; then
      echo
      echo '## eval.py, session 11 command line (`--tag _s14_e3`)'
      echo
      cat "$LOG/eval.md"
    fi
    if [ -s "$LOG/descq.md" ]; then
      echo
      echo '## descq.py eval (title and description queries)'
      echo
      cat "$LOG/descq.md"
    fi
  } > "$OUT"
  step "commit and push $OUT"
  git add "$OUT" || fail "git add"
  git commit -q -m "session 14: outputs of the third-encoder run (E3, gme-Qwen2-VL-2B-Instruct), verbatim" -- "$OUT" || fail "git commit"
  for i in 1 2 3; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 10
  done
  fail "git push"
}

step "start, commit $(git rev-parse --short HEAD), threads $DIRVEC_THREADS"
step "transformers 4.51.3 into $TF"
if [ ! -d "$TF/transformers" ]; then
  "$PYJ" -m pip install -q --no-deps --target "$TF" "transformers==4.51.3" >> "$LOG/run.log" 2>&1 || fail "pip transformers"
fi
gme - > "$LOG/env.txt" 2>> "$LOG/run.log" <<'PY' || fail "environment"
import sys, numpy, PIL, torch, tokenizers, huggingface_hub, transformers, sklearn
print("python", sys.version.split()[0])
print("transformers", transformers.__version__, transformers.__file__)
print("torch", torch.__version__, "cuda", torch.version.cuda, "gpu", torch.cuda.get_device_name(0))
print("numpy", numpy.__version__, "pillow", PIL.__version__, "tokenizers", tokenizers.__version__,
      "huggingface_hub", huggingface_hub.__version__, "scikit-learn", sklearn.__version__)
PY
grep -q "^transformers 4.51.3 $TF" "$LOG/env.txt" || fail "transformers 4.51.3 not first on the path"
echo "DIRVEC_IMG_BATCH=${DIRVEC_IMG_BATCH:-8}" >> "$LOG/env.txt"

step "pilot (20 calibration-split directories of S11)"
gme scripts/embed.py pilot --model $M --manifest data/manifest_s11.jsonl --dirs data/dirs_s11.jsonl \
  --tag _s11 --calib 0.2 --calib-seed 20261102 > "$LOG/pilot.json" 2>> "$LOG/run.log" || fail "pilot"
"$PYJ" - "data/emb/pilot/${M}_s11.json" > "$LOG/gate.txt" 2>> "$LOG/run.log" <<'PY' || fail "gate check"
import json, sys
r = json.load(open(sys.argv[1]))["text_mode"]["query"]
ok = r["median_rank"] < r["random_median_rank"]
print(f"median rank of own-directory images for text and table files {r['median_rank']} "
      f"(random {r['random_median_rank']}), median best own-image rank {r['median_best_own_rank']} "
      f"(random {r['random_median_best_own_rank']}); gate {'passed' if ok else 'FAILED'}")
PY
step "$(cat "$LOG/gate.txt")"
if grep -q "gate FAILED" "$LOG/gate.txt"; then
  step "gate failed: stop by the brief's rule, outputs with the pilot only"
  write_outputs
  touch "$LOG/DONE"
  exit 0
fi

step "embed all S11 files"
gme scripts/embed.py all --model $M --text-mode query --manifest data/manifest_s11.jsonl --tag _s11 \
  > "$LOG/embed.json" 2>> "$LOG/embed.log" || fail "embed all"
step "ok set against E1"
"$PYJ" - > "$LOG/okset.txt" 2>> "$LOG/run.log" <<'PY' || fail "ok set"
import json
e3 = [json.loads(l) for l in open("data/emb/gme-Qwen2-VL-2B-Instruct_s11/index.jsonl")]
e1 = [json.loads(l) for l in open("data/emb/jina-embeddings-v4_s11/index.jsonl")]
assert [a["path"] for a in e3] == [b["path"] for b in e1]
a = [bool(r.get("ok")) for r in e3]; b = [bool(r.get("ok")) for r in e1]
print(f"files {len(a)}; ok under E3 {sum(a)}, under E1 {sum(b)}, both {sum(x and y for x, y in zip(a, b))}, "
      f"E3 only {sum(x and not y for x, y in zip(a, b))}, E1 only {sum(y and not x for x, y in zip(a, b))}")
for r3, r1 in zip(e3, e1):
    if bool(r3.get("ok")) != bool(r1.get("ok")):
        print(" ", r3["path"], "| E3:", r3.get("note"), "| E1:", r1.get("note"))
PY

step "eval (session 11 command line, --tag _s14_e3)"
"$PYJ" scripts/eval.py --model $M --emb ${M}_s11 --manifest data/manifest_s11.jsonl --dirs data/dirs_s11.jsonl \
  --gt data/gt_structural_s11.jsonl --criterion s3 --calib 0.2 --calib-seed 20261102 --queries eval --s9 \
  --reps a,ac,c,cc,d,dc,bc2,tb2,tb2c --tag _s14_e3 > "$LOG/eval.md" 2>> "$LOG/run.log" || fail "eval"

step "descq embed (title and description queries)"
[ -f data/desc_s11.jsonl ] || gunzip -k data/desc_s11.jsonl.gz || fail "gunzip desc"
gme scripts/descq.py embed --model $M --emb ${M}_s11 2>> "$LOG/run.log" || fail "descq embed"
step "descq eval"
"$PYJ" scripts/descq.py eval --model $M --emb ${M}_s11 > "$LOG/descq.md" 2>> "$LOG/run.log" || fail "descq eval"

write_outputs
step "session 14 done"
touch "$LOG/DONE"
