#!/bin/bash
# Session 15: the fourth encoder E4 (Nomic Embed v1.5, a dual tower) on the session 11 set (BRIEF.md, session 15).
# Run on the pod from anywhere: bash scripts/s15_run.sh
# S15_RESUME=1 skips the pilot, the embedding and the eval when their outputs are already in $LOG
# (used once, after xenc.py failed on a key name; nothing that had run was repeated).
# Writes $LOG/{env.txt,pilot.json,gate.txt,embed.json,okset.txt,eval.md,xenc.md,xcheck.txt,descq.md,run.log}.
# When every step succeeds it writes results/session15_outputs.md (the outputs verbatim), commits and pushes that
# one file and touches $LOG/DONE. If the pilot gate fails it does the same with the pilot only (the
# brief's stop rule). On any other failure it touches $LOG/FAILED and stops. The pod watcher
# (scripts/pod_autostop.sh) looks for either marker.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S15_LOG:-/workspace/logs/s15}
PYJ=${S15_PY:-/workspace/venv/bin/python}   # the E1 venv (transformers 4.52.4): everything, E4 included
HFN=${S15_HF:-/root/hf_nomic}                 # E4 weights and model code on the container disk (about 0.9 GB)
PREP=${S15_PREP:-14}                          # input-preparation threads (no effect on any vector)
M=nomic-embed-v1.5
mkdir -p "$LOG"
cd "$REPO" || exit 1
export DIRVEC_THREADS=${DIRVEC_THREADS:-8} OMP_NUM_THREADS=${OMP_NUM_THREADS:-8} OPENBLAS_NUM_THREADS=${OPENBLAS_NUM_THREADS:-8}
export HF_HUB_ENABLE_HF_TRANSFER=0 HF_HUB_OFFLINE=0
rm -f "$LOG/DONE" "$LOG/FAILED"

fail() { echo "FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
e4() { HF_HOME="$HFN" "$PYJ" "$@"; }

write_outputs() {
  local OUT=results/session15_outputs.md
  {
    echo "# Session 15 outputs, verbatim"
    echo
    echo "Written by scripts/s15_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
    echo "Nothing here is edited. The verdicts and the reading are in results/session15.md."
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
    echo '## Pilot (`embed.py pilot`, report data/emb/pilot/nomic-embed-v1.5_s11.json)'
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
      echo '## eval.py, session 11 command line (`--tag _s15_e4`)'
      echo
      cat "$LOG/eval.md"
    fi
    if [ -s "$LOG/xenc.md" ]; then
      echo
      echo '## xenc.py (the loss compared between encoders on the same queries; H15c)'
      echo
      cat "$LOG/xenc.md"
      echo
      echo '```'
      cat "$LOG/xcheck.txt"
      echo '```'
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
  git commit -q -m "session 15: outputs of the fourth-encoder run (E4, Nomic Embed v1.5 dual tower), verbatim" -- "$OUT" || fail "git commit"
  for i in 1 2 3; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 10
  done
  fail "git push"
}

step "start, commit $(git rev-parse --short HEAD), prep threads $PREP"
e4 - > "$LOG/env.txt" 2>> "$LOG/run.log" <<'PY' || fail "environment"
import sys, numpy, PIL, torch, tokenizers, huggingface_hub, transformers, sklearn, einops
print("python", sys.version.split()[0])
print("transformers", transformers.__version__, transformers.__file__)
print("torch", torch.__version__, "cuda", torch.version.cuda, "gpu", torch.cuda.get_device_name(0))
print("numpy", numpy.__version__, "pillow", PIL.__version__, "tokenizers", tokenizers.__version__,
      "huggingface_hub", huggingface_hub.__version__, "scikit-learn", sklearn.__version__, "einops", einops.__version__)
PY
grep -q "^transformers 4.52.4 " "$LOG/env.txt" || fail "transformers 4.52.4 expected in the E1 venv"
for f in data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl data/emb/jina-clip-v2_s11/ranks_s11_e2.jsonl \
         data/emb/gme-Qwen2-VL-2B-Instruct_s11/ranks_s14_e3.jsonl; do
  [ -s "$f" ] || fail "missing $f"
done

if [ -n "${S15_RESUME:-}" ] && [ -s "$LOG/gate.txt" ] && ! grep -q "gate FAILED" "$LOG/gate.txt"; then
  step "resume: pilot and gate already done ($(cat "$LOG/gate.txt"))"
else
step "pilot (20 calibration-split directories of S11)"
e4 scripts/embed.py pilot --model $M --manifest data/manifest_s11.jsonl --dirs data/dirs_s11.jsonl \
  --tag _s11 --calib 0.2 --calib-seed 20261102 > "$LOG/pilot.json" 2>> "$LOG/run.log" || fail "pilot"
"$PYJ" - "data/emb/pilot/${M}_s11.json" > "$LOG/gate.txt" 2>> "$LOG/run.log" <<'PY' || fail "gate check"
import json, sys
r = json.load(open(sys.argv[1]))["text_mode"]
q, d = r["query"], r["doc"]
ok = q["median_rank"] < q["random_median_rank"]
print(f"median rank of own-directory images for text and table files {q['median_rank']} "
      f"(random {q['random_median_rank']}), median best own-image rank {q['median_best_own_rank']} "
      f"(random {q['random_median_best_own_rank']}); doc prefix for information: {d['median_rank']}; "
      f"gate {'passed' if ok else 'FAILED'}")
PY
step "$(cat "$LOG/gate.txt")"
if grep -q "gate FAILED" "$LOG/gate.txt"; then
  step "gate failed: stop by the brief's rule, outputs with the pilot only"
  write_outputs
  touch "$LOG/DONE"
  exit 0
fi
fi

if [ -n "${S15_RESUME:-}" ] && [ -s "$LOG/okset.txt" ] && [ -s "data/emb/${M}_s11/index.jsonl" ]; then
  step "resume: embedding and ok set already done ($(head -1 "$LOG/okset.txt"))"
else
step "embed all S11 files"
e4 scripts/embed.py all --model $M --text-mode query --manifest data/manifest_s11.jsonl --tag _s11 \
  --prep-workers "$PREP" > "$LOG/embed.json" 2>> "$LOG/embed.log" || fail "embed all"
grep "longest text input" "$LOG/embed.log" | tail -1 | tee -a "$LOG/run.log"
step "ok set against E1"
"$PYJ" - > "$LOG/okset.txt" 2>> "$LOG/run.log" <<'PY' || fail "ok set"
import json
e4 = [json.loads(l) for l in open("data/emb/nomic-embed-v1.5_s11/index.jsonl")]
e1 = [json.loads(l) for l in open("data/emb/jina-embeddings-v4_s11/index.jsonl")]
assert [a["path"] for a in e4] == [b["path"] for b in e1]
a = [bool(r.get("ok")) for r in e4]; b = [bool(r.get("ok")) for r in e1]
print(f"files {len(a)}; ok under E4 {sum(a)}, under E1 {sum(b)}, both {sum(x and y for x, y in zip(a, b))}, "
      f"E4 only {sum(x and not y for x, y in zip(a, b))}, E1 only {sum(y and not x for x, y in zip(a, b))}")
for r4, r1 in zip(e4, e1):
    if bool(r4.get("ok")) != bool(r1.get("ok")):
        print(" ", r4["path"], "| E4:", r4.get("note"), "| E1:", r1.get("note"))
PY
fi

if [ -n "${S15_RESUME:-}" ] && grep -q "Session 9 hypotheses on the eval queries" "$LOG/eval.md" 2>/dev/null && [ -s "data/emb/${M}_s11/ranks_s15_e4.jsonl" ]; then
  step "resume: eval already done"
else
step "eval (session 11 command line, --tag _s15_e4)"
"$PYJ" scripts/eval.py --model $M --emb ${M}_s11 --manifest data/manifest_s11.jsonl --dirs data/dirs_s11.jsonl \
  --gt data/gt_structural_s11.jsonl --criterion s3 --calib 0.2 --calib-seed 20261102 --queries eval --s9 \
  --reps a,ac,c,cc,d,dc,bc2,tb2,tb2c --tag _s15_e4 > "$LOG/eval.md" 2>> "$LOG/run.log" || fail "eval"
fi

step "xenc (H15c: the loss under E4 against E1, E2, E3 on the same queries)"
"$PYJ" scripts/xenc.py E1=data/emb/jina-embeddings-v4_s11/ranks_s11_e1.jsonl \
  E2=data/emb/jina-clip-v2_s11/ranks_s11_e2.jsonl E3=data/emb/gme-Qwen2-VL-2B-Instruct_s11/ranks_s14_e3.jsonl \
  E4=data/emb/${M}_s11/ranks_s15_e4.jsonl --pairs E4-E1,E4-E2,E4-E3,E2-E1 > "$LOG/xenc.md" 2>> "$LOG/run.log" || fail "xenc"
"$PYJ" - "$LOG/xenc.md" "$LOG/eval.md" > "$LOG/xcheck.txt" 2>> "$LOG/run.log" <<'PY' || fail "xenc check"
# xenc.py's per-encoder c - a intervals must equal eval.py's: E1 and E2 as printed in
# results/session11.md, E3 in results/session14_outputs.md, E4 in this run's eval output.
import re, sys
x = open(sys.argv[1]).read()
known = {("E1", "P1"): "+0.253 | [+0.214, +0.294]", ("E1", "P2"): "+0.169 | [+0.136, +0.200]",
         ("E2", "P1"): "+0.500 | [+0.462, +0.538]", ("E2", "P2"): "+0.348 | [+0.312, +0.386]",
         ("E3", "P1"): "+0.205 | [+0.164, +0.244]", ("E3", "P2"): "+0.158 | [+0.125, +0.188]"}
ev = open(sys.argv[2]).read()
for cell, lab in (("P1", "P1 image in"), ("P2", "P2 textlike in")):
    m = re.search(r"\| " + re.escape(lab) + r"[^\n]*\| ([+-]\d\.\d{3}) \| (\[[^\]]+\]) \|", ev)
    known[("E4", cell)] = f"{m.group(1)} | {m.group(2)}" if m else "(not found in eval.md)"
ok = True
for (enc, cell), want in known.items():
    lab = "P1 image in [0,.2)+[.2,.5)" if cell == "P1" else "P2 textlike in [.5,.8)+[.8,1]"
    m = re.search(r"\| " + enc + r" \| " + re.escape(lab) + r" \| \d+ \| \d+ \| ([^|]+) \| ([^|]+) \|", x)
    got = f"{m.group(1).strip()} | {m.group(2).strip()}" if m else "(missing)"
    same = got == want
    ok &= same
    print(f"{enc} {cell}: xenc {got}; eval.py {want}; {'same' if same else 'DIFFERENT'}")
print("xenc reproduces eval.py's c - a intervals:", "yes" if ok else "NO")
PY
step "$(tail -1 "$LOG/xcheck.txt")"

step "descq embed (title and description queries)"
[ -f data/desc_s11.jsonl ] || gunzip -k data/desc_s11.jsonl.gz || fail "gunzip desc"
e4 scripts/descq.py embed --model $M --emb ${M}_s11 2>> "$LOG/run.log" || fail "descq embed"
step "descq eval"
"$PYJ" scripts/descq.py eval --model $M --emb ${M}_s11 > "$LOG/descq.md" 2>> "$LOG/run.log" || fail "descq eval"

write_outputs
step "session 15 done"
touch "$LOG/DONE"
