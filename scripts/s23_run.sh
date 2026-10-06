#!/bin/bash
# Session 23 on the pod: whole repository trees and the walk guided by folder summaries (BRIEF.md,
# session 23). Called by scripts/s19_followup.sh after session 21, or by hand: bash scripts/s23_run.sh
#   S23_RESUME=1   skip every step whose output is already there
# Steps: self-test, harvest of whole trees, manifest, ground truth (pushed before anything is
# embedded), E1 embedding, scripts/tree.py with the registered tests, results/session23_outputs.md.
# It writes no DONE or FAILED marker of its own: the caller stops the pod.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
LOG=${S23_LOG:-/workspace/logs/s23}
PY=${S19_PY:-/workspace/venv/bin/python}
CORPUS=${S23_CORPUS:-/root/corpus_s23}
TMP=${S23_TMP:-/root/tmp_s23}
M=jina-embeddings-v4
TRAILERS="Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01L3uBXsnxCDj3XA5StyfgGU"
mkdir -p "$LOG" "$CORPUS" "$TMP"
unset S23_BUDGETS S23_REG_BUDGET S23_SELFTEST S21_BUDGETS S21_REG_BUDGET S21_SELFTEST
export DIRVEC_THREADS=3 OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 HF_HUB_ENABLE_HF_TRANSFER=0 TOKENIZERS_PARALLELISM=false
[ -e data/corpus_s23 ] || ln -s "$CORPUS" data/corpus_s23
[ -n "${S23_RESUME:-}" ] || rm -f "$LOG/run.log"

step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
fail() {  # what there is goes to the repository, so that a stop is on record without the pod
  step "FAILED at: $1"
  {
    echo "# Session 23 outputs: INCOMPLETE, the run stopped at: $1"
    echo
    echo "Written by scripts/s23_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
    echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
    for f in harvest.log manifest.log embed_e1.log tree_e1.log selftest.txt; do
      [ -s "$LOG/$f" ] && { echo; echo "## The end of $f"; echo; echo '```'; tail -15 "$LOG/$f" | cut -c1-300; echo '```'; }
    done
  } > results/session23_outputs.md
  local extra=""
  [ -s data/harvest_s23.jsonl ] && gzip -kf data/harvest_s23.jsonl && extra="data/harvest_s23.jsonl.gz"
  push "session 23: the run stopped at: $1 (run log and the ends of its logs)" results/session23_outputs.md $extra
  exit 1
}
have() { [ -n "${S23_RESUME:-}" ] && [ -s "$1" ]; }
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

step "start, commit $(git rev-parse --short HEAD), tree.py $(sha256sum scripts/tree.py scripts/budget.py scripts/tree_fetch.py | sha256sum | cut -c1-16)"
"$PY" scripts/s23_selftest.py > "$LOG/selftest.txt" 2>&1 || { tail -5 "$LOG/selftest.txt" | tee -a "$LOG/run.log"; fail "self-test"; }
tail -1 "$LOG/selftest.txt" | tee -a "$LOG/run.log"

if have data/gt_structural_s23.jsonl; then
  step "resume: corpus, manifest and ground truth already there"
else
  [ -s data/pool_s19.jsonl ] || gunzip -kf data/pool_s19.jsonl.gz || fail "no pool"
  step "harvest of whole trees"
  "$PY" scripts/tree_fetch.py harvest --repos 300 --files 33000 --tmp "$TMP" --workers 6 > "$LOG/harvest_state.json" 2>> "$LOG/harvest.log" || fail "harvest"
  tail -1 "$LOG/harvest.log" | tee -a "$LOG/run.log"
  "$PY" - > "$LOG/harvest.md" 2>> "$LOG/run.log" <<'PY' || fail "harvest counts"
import json
from collections import Counter
hv = [json.loads(l) for l in open("data/harvest_s23.jsonl") if l.strip()]
ok = [r for r in hv if r["status"] == "ok"]
took = [r for r in ok if r.get("taken")]
print(f"Repositories read: {len(hv)} ({dict(Counter(r['status'] for r in hv))}); trees taken: {len(took)}, "
      f"{len(took) / max(len(ok), 1):.3f} of those read; files {sum(r['n_files'] for r in took)}, "
      f"image files {sum(r['n_image'] for r in took)}; directories with a kept file {sum(r['n_dirs'] for r in took)}.")
print("Not taken, by the first rule failed: " + ", ".join(f"{k} {v}" for k, v in Counter(r.get("why_not") for r in ok if not r.get("taken")).most_common()) + ".")
n = len(hv)
if n and sum(1 for r in hv if r["status"] == "fail") > 0.10 * n:
    raise SystemExit("more than 10 percent of the tarballs could not be fetched")
PY
  cat "$LOG/harvest.md" | tee -a "$LOG/run.log"
  step "manifest"
  "$PY" scripts/manifest.py --corpus data/corpus_s23 --selection data/selection_s23.jsonl --log data/download_log_s23.jsonl \
    --out-manifest data/manifest_s23.jsonl --out-dirs data/dirs_s23.jsonl --dir-prefix gh_ --workers 3 2> "$LOG/manifest.log" || fail "manifest"
  tail -2 "$LOG/manifest.log" | tee -a "$LOG/run.log"
  step "ground truth"
  "$PY" scripts/build_gt.py --manifest data/manifest_s23.jsonl --dirs data/dirs_s23.jsonl --out data/gt_structural_s23.jsonl \
    --workers 3 > "$LOG/gt.json" 2>> "$LOG/run.log" || fail "build_gt"
fi
if ! git ls-files --error-unmatch data/manifest_s23.jsonl > /dev/null 2>&1; then
  gzip -kf data/harvest_s23.jsonl || fail "gzip"
  push "session 23: the corpus of whole trees (harvest log, selection, manifest, ground truth)" \
    data/harvest_s23.jsonl.gz data/selection_s23.jsonl data/manifest_s23.jsonl data/dirs_s23.jsonl data/gt_structural_s23.jsonl \
    && step "corpus files pushed" || step "push of the corpus files failed (the run goes on)"
fi

check_files() {
  "$PY" - > "$LOG/files_check.txt" 2>> "$LOG/run.log" <<'PY'
import json, os, sys
rows = [json.loads(l) for l in open("data/manifest_s23.jsonl") if l.strip()]
miss = [r["path"] for r in rows if not os.path.isfile(r["path"]) or os.path.getsize(r["path"]) != r["bytes"]]
print(f"manifest rows {len(rows)}; files missing or of another size {len(miss)}")
sys.exit(1 if miss else 0)
PY
}
if ! check_files; then
  step "$(cat "$LOG/files_check.txt"): rebuilding the corpus from the selection"
  "$PY" scripts/fetch_gh.py download --selection data/selection_s23.jsonl --corpus data/corpus_s23 --tmp "$TMP" --workers 6 2>> "$LOG/download.log" || fail "download"
  check_files || fail "files of the manifest are missing after the rebuild"
fi
step "$(cat "$LOG/files_check.txt")"

EMB="${M}_s23"
if have "data/emb/$EMB/walk_s23.jsonl" && have "$LOG/tree_e1.md"; then
  step "resume: E1 already evaluated"
else
  step "E1: embed all files"
  emb() { HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PY" scripts/embed.py all --model "$M" --text-mode query --manifest data/manifest_s23.jsonl \
            --tag _s23 --checkpoint 1000 --prep-workers 4 > "$LOG/embed_e1.json" 2>> "$LOG/embed_e1.log"; }
  emb || { step "E1: embedding stopped; one retry (the cache keeps what is done)"; emb || fail "E1 embedding"; }
  step "E1: $(tr -d '\n' < "$LOG/embed_e1.json" | cut -c1-300)"
  step "E1: the walk"
  "$PY" scripts/tree.py --model "$M" --emb "$EMB" --manifest data/manifest_s23.jsonl --dirs data/dirs_s23.jsonl \
    --gt data/gt_structural_s23.jsonl --label "S23 E1" --registered > "$LOG/tree_e1.md" 2>> "$LOG/tree_e1.log" || fail "tree.py"
fi

OUT=results/session23_outputs.md
{
  echo "# Session 23 outputs, verbatim"
  echo
  echo "Written by scripts/s23_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and the reading are in results/session23.md."
  echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
  echo; echo '## Harvest'; echo; cat "$LOG/harvest.md" 2>/dev/null
  echo; echo '## build_gt.py report'; echo; echo '```'; cat "$LOG/gt.json" 2>/dev/null; echo '```'
  echo; cat "$LOG/tree_e1.md"
} > "$OUT"
gzip -c "data/emb/$EMB/walk_s23.jsonl" > data/walk_s23_e1.jsonl.gz
push "session 23: outputs of the walk down whole repository trees (E1), verbatim" "$OUT" data/walk_s23_e1.jsonl.gz || fail "push of the outputs"
step "session 23 done"
