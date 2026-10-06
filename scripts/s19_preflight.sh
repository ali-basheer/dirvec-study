#!/bin/bash
# Session 19 preflight, on the pod, before the registered run: the pod's tools, the pipeline's
# self-test in the pod's own Python, and the real GitHub endpoints on a small throwaway draw.
# It uses seed 7 and files with the suffix _p19, never the registered seed or a registered file,
# and computes no retrieval number. The last line is PREFLIGHT_OK or PREFLIGHT_FAILED.
#   bash scripts/s19_preflight.sh > /workspace/logs/s19/preflight.log 2>&1
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO" || exit 1
PY=${S19_PY:-/workspace/venv/bin/python}
HFN=${S19_HF_NOMIC:-/root/hf_nomic}
W=/root/s19_preflight
P=_p19
bad() { echo "FAIL: $1"; echo PREFLIGHT_FAILED; exit 1; }
say() { echo; echo "== $(date -u +%H:%M:%S) $1"; }
rm -rf "$W" data/*"$P"* data/emb/*"$P"; mkdir -p "$W/tmp" "$W/corpus"
[ -e "data/corpus$P" ] || ln -s "$W/corpus" "data/corpus$P"

say "pod"
echo "commit $(git rev-parse --short HEAD); $(nproc) cpus by nproc; $(grep MemTotal /proc/meminfo)"
df -h / /workspace /root 2>/dev/null | awk '!seen[$0]++'
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader || bad "no GPU"
for t in git curl pdftotext pdftoppm pandoc gzip; do command -v "$t" > /dev/null || bad "tool missing: $t"; done
"$PY" -c "import torch, transformers, numpy, sklearn, scipy, PIL, imagehash, requests; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), 'transformers', transformers.__version__, 'numpy', numpy.__version__)" || bad "python environment"
HF_HOME=/workspace/hf HF_HUB_OFFLINE=1 "$PY" - <<'PY' || bad "E1 or E2 weights are not on the volume"
import sys
sys.path.insert(0, "scripts")
import embed as em
from huggingface_hub import snapshot_download
for n in ("jina-embeddings-v4", "jina-clip-v2"):
    s = em.MODELS[n]
    print(n, "->", snapshot_download(s["id"], revision=s["revision"], allow_patterns=s.get("allow")))
PY

say "self-test of the pipeline in this Python (synthetic repositories, no network)"
"$PY" scripts/s19_selftest.py > "$W/selftest.log" 2>&1 || { tail -20 "$W/selftest.log"; bad "s19_selftest.py"; }
tail -1 "$W/selftest.log"

say "search API, one throwaway day"
curl -s -m 30 -H "User-Agent: dirvec" https://api.github.com/rate_limit | "$PY" -c "import json,sys; d=json.load(sys.stdin)['resources']; print('search', d['search'], 'core', d['core'])" || echo "(rate_limit not readable)"
"$PY" scripts/fetch_gh.py pool --seed 7 --min-usable 40 --max-days 1 --out "data/pool$P.jsonl" --days-log "data/pool${P}_days.jsonl" 2> "$W/pool.log" || { tail -5 "$W/pool.log"; bad "pool"; }
grep -c "rate limit" "$W/pool.log" | sed 's/^/rate-limit waits: /'
tail -1 "$W/pool.log"
cat "data/pool${P}_days.jsonl" | cut -c1-600

say "tarballs, a small draw"
"$PY" scripts/fetch_gh.py harvest --seed 7 --mixed 6 --other 3 --files 150 --workers 4 --pool "data/pool$P.jsonl" \
  --corpus "data/corpus$P" --selection "data/selection$P.jsonl" --log "data/download_log$P.jsonl" \
  --harvest-log "data/harvest$P.jsonl" --ghdirs "data/ghdirs$P.jsonl" --tmp "$W/tmp" > "$W/harvest_state.json" 2> "$W/harvest.log" \
  || { tail -5 "$W/harvest.log"; bad "harvest"; }
tail -1 "$W/harvest.log"; cat "$W/harvest_state.json"
"$PY" - "$P" <<'PY' || bad "harvest gave nothing usable"
import json, sys
from collections import Counter
p = sys.argv[1]
hv = [json.loads(l) for l in open(f"data/harvest{p}.jsonl")]
sel = [json.loads(l) for l in open(f"data/selection{p}.jsonl")]
gd = [json.loads(l) for l in open(f"data/ghdirs{p}.jsonl")]
print("harvest statuses", dict(Counter(r["status"] for r in hv)), "notes", dict(Counter(r["note"] for r in hv if r["note"])))
print("eligible directories", len(gd), "mixed", sum(r["mixed"] for r in gd), "kept files per eligible directory, mean",
      round(sum(r["n_kept"] for r in gd) / max(len(gd), 1), 1), "bytes per kept file, mean",
      round(sum(r["bytes"] for r in gd) / max(sum(r["n_kept"] for r in gd), 1)))
for r in sel:
    print(" ", r["repo"], repr(r["dir"]), "depth", r["depth"], "files", r["n_included"], "image share", round(r["image_frac"], 2), "sha", r["sha"][:10])
ok = [r for r in hv if r["status"] == "ok"]
sys.exit(0 if sel and ok and all(len(r["sha"]) == 40 for r in ok) else 1)
PY

say "manifest, ground truth, history, commit-subject queries, corpus counts"
"$PY" scripts/manifest.py --corpus "data/corpus$P" --selection "data/selection$P.jsonl" --log "data/download_log$P.jsonl" \
  --out-manifest "data/manifest$P.jsonl" --out-dirs "data/dirs$P.jsonl" --dir-prefix gh_ --workers 3 2> "$W/manifest.log" || { tail -5 "$W/manifest.log"; bad "manifest"; }
tail -2 "$W/manifest.log"
"$PY" scripts/build_gt.py --manifest "data/manifest$P.jsonl" --dirs "data/dirs$P.jsonl" --out "data/gt_structural$P.jsonl" --workers 3 > "$W/gt.json" 2> "$W/gt.log" || { tail -5 "$W/gt.log"; bad "build_gt"; }
head -c 600 "$W/gt.json"; echo
"$PY" scripts/fetch_gh.py history --selection "data/selection$P.jsonl" --out "data/commits$P.jsonl" --history-log "data/history$P.jsonl" 2> "$W/history.log" || { tail -5 "$W/history.log"; bad "history"; }
tail -1 "$W/history.log"; cut -c1-200 "data/history$P.jsonl"
S19_SFX=$P "$PY" scripts/s19.py commitq build 2> "$W/commitq.log" || { tail -5 "$W/commitq.log"; bad "commitq build"; }
head -3 "data/commitq$P.jsonl" 2>/dev/null | cut -c1-300
S19_SFX=$P "$PY" scripts/s19.py corpus > "$W/corpus.md" 2> "$W/corpus.log" || { tail -5 "$W/corpus.log"; bad "corpus counts"; }
cat "$W/corpus.md"
grep -q '"fetch failed' "data/history$P.jsonl" && [ "$(grep -c '"note": ""' "data/history$P.jsonl")" = 0 ] && bad "no repository's history could be fetched"

say "the three encoders on the small draw"
for E in E1 E4 E2; do
  case $E in E1) M=jina-embeddings-v4; H=/workspace/hf; O=1;; E2) M=jina-clip-v2; H=/workspace/hf; O=1;; E4) M=nomic-embed-v1.5; H=$HFN; O=0;; esac
  t0=$(date +%s)
  HF_HOME=$H HF_HUB_OFFLINE=$O HF_HUB_ENABLE_HF_TRANSFER=0 TOKENIZERS_PARALLELISM=false "$PY" scripts/embed.py all --model "$M" --text-mode query \
    --manifest "data/manifest$P.jsonl" --tag "$P" --checkpoint 1000 --prep-workers 4 > "$W/embed_$E.json" 2> "$W/embed_$E.log" \
    || { tail -15 "$W/embed_$E.log"; [ "$E" = E1 ] && bad "E1 embedding"; echo "WARNING: $E did not run on this pod"; continue; }
  echo "$E ($M): $(( $(date +%s) - t0 )) s with the model load; $(tr -d '\n' < "$W/embed_$E.json" | cut -c1-400)"
done
nvidia-smi --query-gpu=memory.used --format=csv,noheader

rm -rf data/*"$P"* data/emb/*"$P" "$W/corpus" "$W/tmp"
say "done"
echo PREFLIGHT_OK
