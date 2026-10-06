#!/bin/bash
# Session 19: the minority-modality loss on directories of GitHub repositories (BRIEF.md, session 19).
# Run on the pod from anywhere: bash scripts/s19_run.sh
#   S19_ENCODERS="E1 E4 E2"   encoders, in order; E1 decides the hypotheses
#   S19_THREADS=3 S19_PREP=4  CPU threads and input-preparation threads (12 and 12 on a full card)
#   S19_RESUME=1              skip every step whose output is already there
# Steps: pool and harvest (repeated until the scored set is full), manifest, ground truth, commit
# history and the commit-subject queries, corpus counts, then per encoder: embedding, eval.py with
# the session 11 command line plus tbc and cs, the commit-subject queries; then s19.py validity over
# the encoders that ran. The corpus files are committed and pushed as soon as they exist, and
# results/session19_outputs.md (every output verbatim) at the end. $LOG/DONE or $LOG/FAILED tells the
# pod watcher (scripts/pod_autostop.sh) to stop the pod.
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
LOG=${S19_LOG:-/workspace/logs/s19}
PY=${S19_PY:-/workspace/venv/bin/python}
CORPUS=${S19_CORPUS:-/root/corpus_s19}       # the files themselves, on the container disk; rebuilt by fetch_gh.py download
TMP=${S19_TMP:-/root/tmp_s19}
HFN=${S19_HF_NOMIC:-/root/hf_nomic}
ENCODERS=${S19_ENCODERS:-"E1 E4 E2"}
THREADS=${S19_THREADS:-3}
PREP=${S19_PREP:-4}
SEED=20261104
TRAILER1="Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
TRAILER2="Claude-Session: https://claude.ai/code/session_01L3uBXsnxCDj3XA5StyfgGU"
mkdir -p "$LOG" "$CORPUS" "$TMP"
cd "$REPO" || exit 1
export DIRVEC_THREADS=$THREADS OMP_NUM_THREADS=$THREADS OPENBLAS_NUM_THREADS=$THREADS
export HF_HUB_ENABLE_HF_TRANSFER=0 TOKENIZERS_PARALLELISM=false
rm -f "$LOG/DONE" "$LOG/FAILED"
[ -e data/corpus_s19 ] || ln -s "$CORPUS" data/corpus_s19

fail() { echo "FAILED at: $1" | tee -a "$LOG/run.log"; touch "$LOG/FAILED"; exit 1; }
step() { echo "$(date -u +%H:%M:%S) $1" | tee -a "$LOG/run.log"; }
have() { [ -n "${S19_RESUME:-}" ] && [ -s "$1" ]; }
push() {  # push "<message>" file...
  local msg=$1; shift
  git add -f "$@" || fail "git add"
  git commit -q -m "$msg" -m "$TRAILER1" -m "$TRAILER2" -- "$@" || fail "git commit"
  for i in 1 2 3 4; do
    git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1 && git push -q >> "$LOG/run.log" 2>&1 && return 0
    sleep 15
  done
  fail "git push"
}
model_of() { case $1 in E1) echo jina-embeddings-v4;; E2) echo jina-clip-v2;; E4) echo nomic-embed-v1.5;; *) fail "unknown encoder $1";; esac; }
enc_py() {  # enc_py E? args...: the encoder's environment
  local e=$1; shift
  case $e in
    E1|E2) HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PY" "$@";;
    E4) HF_HOME="$HFN" HF_HUB_OFFLINE=0 "$PY" "$@";;
  esac
}

step "start, commit $(git rev-parse --short HEAD), encoders $ENCODERS, threads $THREADS, prep $PREP"
"$PY" - > "$LOG/env.txt" 2>> "$LOG/run.log" <<'PY' || fail "environment"
import sys, numpy, sklearn, scipy, requests, PIL, imagehash, subprocess
print("python", sys.version.split()[0], "numpy", numpy.__version__, "scikit-learn", sklearn.__version__, "scipy", scipy.__version__,
      "requests", requests.__version__, "pillow", PIL.__version__)
print(subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip())
PY
"$PY" scripts/selftest_ranks.py > "$LOG/selftest_ranks.txt" 2>&1 || fail "selftest_ranks.py"

# ---- corpus
if have data/gt_structural_s19.jsonl; then
  step "resume: corpus, manifest and ground truth already there"
else
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 30 -H "User-Agent: dirvec" "https://api.github.com/search/repositories?q=stars:%3E%3D5+created:2020-01-01&per_page=1")
  step "search API without a token answers HTTP $code"
  if [ "$code" != 200 ] && [ -z "${GITHUB_TOKEN:-}" ]; then
    sleep 70
    code=$(curl -s -o /dev/null -w '%{http_code}' -m 30 -H "User-Agent: dirvec" "https://api.github.com/search/repositories?q=stars:%3E%3D5+created:2020-01-01&per_page=1")
    if [ "$code" != 200 ]; then
      tok=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
      [ -n "$tok" ] && export GITHUB_TOKEN="$tok" && step "search API still refuses (HTTP $code): using the pod's stored GitHub credential for search requests"
      unset tok
    fi
  fi
  need=3000
  for round in 1 2 3 4 5 6; do
    step "pool, round $round: at least $need usable repositories"
    "$PY" scripts/fetch_gh.py pool --seed $SEED --min-usable $need 2>> "$LOG/pool.log" || fail "pool"
    tail -1 "$LOG/pool.log" | tee -a "$LOG/run.log"
    step "harvest, round $round"
    "$PY" scripts/fetch_gh.py harvest --seed $SEED --tmp "$TMP" --workers 6 > "$LOG/harvest_state.json" 2>> "$LOG/harvest.log" || fail "harvest"
    tail -1 "$LOG/harvest.log" | tee -a "$LOG/run.log"
    # tarballs that could not be fetched (throttling, network) must stay rare, or the draw is not the registered one
    "$PY" - data/harvest_s19.jsonl >> "$LOG/run.log" 2>&1 <<'PY' || fail "more than 10 percent of the tarballs could not be fetched"
import json, sys
from collections import Counter
c = Counter(json.loads(l)["status"] for l in open(sys.argv[1]) if l.strip())
n = sum(c.values())
print(f"harvest log: {n} repositories, {dict(c)}")
sys.exit(1 if n and c.get("fail", 0) > 0.10 * n else 0)
PY
    grep -q '"state": "full"' "$LOG/harvest_state.json" && break
    need=$((need + 2500))
  done
  grep -q '"state": "full"' "$LOG/harvest_state.json" || step "the pool was exhausted before the scored set was full: going on with what there is"
  unset GITHUB_TOKEN
  step "manifest"
  "$PY" scripts/manifest.py --corpus data/corpus_s19 --selection data/selection_s19.jsonl --log data/download_log_s19.jsonl \
    --out-manifest data/manifest_s19.jsonl --out-dirs data/dirs_s19.jsonl --dir-prefix gh_ --workers "$THREADS" 2> "$LOG/manifest.log" || fail "manifest"
  tail -2 "$LOG/manifest.log" | tee -a "$LOG/run.log"
  step "ground truth"
  "$PY" scripts/build_gt.py --manifest data/manifest_s19.jsonl --dirs data/dirs_s19.jsonl --out data/gt_structural_s19.jsonl \
    --workers "$THREADS" > "$LOG/gt.json" 2>> "$LOG/run.log" || fail "build_gt"
fi
if have data/commitq_s19.jsonl; then
  step "resume: commit history and queries already there"
else
  step "commit history"
  "$PY" scripts/fetch_gh.py history 2> "$LOG/history.log" || fail "history"
  tail -1 "$LOG/history.log" | tee -a "$LOG/run.log"
  "$PY" scripts/s19.py commitq build > "$LOG/commitq_build.txt" 2>> "$LOG/run.log" || fail "commitq build"
  cat "$LOG/commitq_build.txt" | tee -a "$LOG/run.log"
fi
"$PY" scripts/s19.py corpus > "$LOG/corpus.md" 2>> "$LOG/run.log" || fail "corpus counts"
if ! git ls-files --error-unmatch data/manifest_s19.jsonl > /dev/null 2>&1; then
  for f in pool_s19 harvest_s19 ghdirs_s19 commits_s19; do gzip -kf "data/$f.jsonl" || fail "gzip $f"; done
  push "session 19: the corpus (pool, harvest log, eligible directories, selection, manifest, ground truth, commits and commit-subject queries)" \
    data/pool_s19.jsonl.gz data/pool_s19_days.jsonl data/harvest_s19.jsonl.gz data/ghdirs_s19.jsonl.gz data/selection_s19.jsonl \
    data/manifest_s19.jsonl data/dirs_s19.jsonl data/gt_structural_s19.jsonl data/commits_s19.jsonl.gz data/commitq_s19.jsonl
  step "corpus files pushed"
fi

# ---- the files on the disk: every manifest row, or the corpus is rebuilt from the selection by commit id
# (a stopped pod loses its container disk, and embed.py would skip a missing file as an input failure)
check_files() {
  "$PY" - > "$LOG/files_check.txt" 2>> "$LOG/run.log" <<'PY'
import json, os, sys
rows = [json.loads(l) for l in open("data/manifest_s19.jsonl") if l.strip()]
miss = [r["path"] for r in rows if not os.path.isfile(r["path"]) or os.path.getsize(r["path"]) != r["bytes"]]
print(f"manifest rows {len(rows)}; files missing or of another size {len(miss)}")
sys.exit(1 if miss else 0)
PY
}
if ! check_files; then
  step "$(cat "$LOG/files_check.txt"): rebuilding the corpus from the selection"
  "$PY" scripts/fetch_gh.py download --tmp "$TMP" --workers 6 2>> "$LOG/download.log" || fail "download"
  tail -1 "$LOG/download.log" | tee -a "$LOG/run.log"
  check_files || fail "files of the manifest are missing after the rebuild"
fi
step "$(cat "$LOG/files_check.txt")"

# ---- encoders
RAN=""
for E in $ENCODERS; do
  M=$(model_of "$E"); e=$(echo "$E" | tr 'E' 'e'); EMB="${M}_s19"
  if have "data/emb/$EMB/ranks_s19_$e.jsonl" && have "$LOG/eval_$e.md" && have "$LOG/commitq_$e.md"; then
    step "resume: $E already evaluated"; RAN="$RAN $E"; continue
  fi
  step "$E: embed all files ($M)"
  if ! enc_py "$E" scripts/embed.py all --model "$M" --text-mode query --manifest data/manifest_s19.jsonl --tag _s19 \
       --checkpoint 1000 --prep-workers "$PREP" > "$LOG/embed_$e.json" 2>> "$LOG/embed_$e.log"; then
    step "$E: embedding stopped; one retry (the cache keeps what is done)"
    enc_py "$E" scripts/embed.py all --model "$M" --text-mode query --manifest data/manifest_s19.jsonl --tag _s19 \
       --checkpoint 1000 --prep-workers "$PREP" > "$LOG/embed_$e.json" 2>> "$LOG/embed_$e.log" || { step "$E: embedding failed twice"; [ "$E" = E1 ] && fail "E1 embedding"; continue; }
  fi
  "$PY" - "data/emb/$EMB/index.jsonl" > "$LOG/okset_$e.txt" 2>> "$LOG/run.log" <<'PY' || fail "ok set $E"
import json, sys
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1])]
print(f"files {len(rows)}; ok {sum(bool(r.get('ok')) for r in rows)}; not ok by modality "
      f"{dict(Counter(r['modality'] for r in rows if not r.get('ok')))}")
PY
  step "$E: $(cat "$LOG/okset_$e.txt")"
  step "$E: eval"
  "$PY" scripts/eval.py --model "$M" --emb "$EMB" --manifest data/manifest_s19.jsonl --dirs data/dirs_s19.jsonl \
    --gt data/gt_structural_s19.jsonl --criterion s3 --calib 0.2 --calib-seed $SEED --queries eval --s9 \
    --reps a,ac,c,cc,d,dc,tb2c,tbc,cs --tag "_s19_$e" > "$LOG/eval_$e.md" 2>> "$LOG/run.log" || { step "$E: eval failed"; [ "$E" = E1 ] && fail "E1 eval"; continue; }
  step "$E: commit-subject queries"
  enc_py "$E" scripts/s19.py commitq embed --model "$M" --emb "$EMB" 2>> "$LOG/run.log" \
    && "$PY" scripts/s19.py commitq eval --model "$M" --emb "$EMB" --enc "$E" --calib-seed $SEED \
         --dump-ranks "$LOG/commitq_ranks_$e.jsonl" > "$LOG/commitq_$e.md" 2>> "$LOG/run.log" \
    || { step "$E: commit-subject queries failed"; echo "(failed; see the run log)" > "$LOG/commitq_$e.md"; }
  RAN="$RAN $E"
  # the registered tests so far, so that a later failure cannot lose them
  RANKS=""; EVMD=""
  for X in $RAN; do x=$(echo "$X" | tr 'E' 'e'); MX=$(model_of "$X")
    RANKS="$RANKS${RANKS:+,}$X=data/emb/${MX}_s19/ranks_s19_$x.jsonl"; EVMD="$EVMD${EVMD:+,}$X=$LOG/eval_$x.md"; done
  "$PY" scripts/s19.py validity --ranks "$RANKS" --index "data/emb/jina-embeddings-v4_s19/index.jsonl" --evalmd "$EVMD" \
    --flags "$LOG/flags.jsonl" > "$LOG/validity.md" 2>> "$LOG/run.log"
  rc=$?
  [ $rc -eq 3 ] && fail "validity does not reproduce eval.py's intervals"
  [ $rc -ne 0 ] && fail "validity"
  step "$E: done; validity over$RAN"
done

# ---- outputs
OUT=results/session19_outputs.md
{
  echo "# Session 19 outputs, verbatim"
  echo
  echo "Written by scripts/s19_run.sh on the pod, $(date -u +%Y-%m-%dT%H:%MZ), repo commit $(git rev-parse --short HEAD)."
  echo "Nothing here is edited. The verdicts and the reading are in results/session19.md."
  echo; echo '## Run log'; echo; echo '```'; cat "$LOG/run.log"; echo '```'
  echo; echo '## Environment'; echo; echo '```'; cat "$LOG/env.txt"; echo '```'
  echo; cat "$LOG/corpus.md"
  echo; echo '## build_gt.py report'; echo; echo '```'; cat "$LOG/gt.json" 2>/dev/null; echo '```'
  echo; echo '## Commit-subject queries, build'; echo; echo '```'; cat "$LOG/commitq_build.txt" 2>/dev/null; echo '```'
  for E in $RAN; do e=$(echo "$E" | tr 'E' 'e')
    echo; echo "## $E: embedding"; echo; echo '```'; cat "$LOG/okset_$e.txt"; grep "longest text input" "$LOG/embed_$e.log" | tail -1; echo '```'
    echo; echo "## $E: eval.py"; echo; cat "$LOG/eval_$e.md"
    echo; cat "$LOG/commitq_$e.md"
  done
  echo; cat "$LOG/validity.md"
} > "$OUT"
push "session 19: outputs of the GitHub-directories run (encoders$RAN), verbatim" "$OUT"
step "session 19 done"
# a follow-up that entered the repository while this run was going (registered in BRIEF.md first),
# run only after everything above is pushed
git pull -q --rebase --autostash >> "$LOG/run.log" 2>&1
if [ -f scripts/s19_followup.sh ] && [ -z "${S19_NO_FOLLOWUP:-}" ]; then
  step "follow-up: scripts/s19_followup.sh at $(git rev-parse --short HEAD)"
  bash scripts/s19_followup.sh > "$LOG/followup.log" 2>&1 && step "follow-up done" || step "follow-up failed (see followup.log)"
fi
touch "$LOG/DONE"
