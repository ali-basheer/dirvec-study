#!/usr/bin/env python3
"""Session 15 check: how many S11 text inputs E4's own tokenizer cuts, and how many pass 2048 tokens.

Every text input is cut to its first 2000 tokens with E1's tokenizer (embed.py), so E1 to E4 read the
same characters unless E4's tokenizer, with its limit of 8192, cuts the text again. This script
prepares every text-like S11 file exactly as embed.py does, applies the 2000-token cut and counts the
E4 tokens of "search_query: " + text. Run on the pod after the session 15 embedding:

  HF_HOME=/root/hf_nomic /workspace/venv/bin/python scripts/count_e4_tokens.py

Session 15's output (/workspace/logs/s15/e4_tokens.txt) is quoted in results/session15.md.
"""
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import embed as em  # noqa: E402
from huggingface_hub import snapshot_download  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402

cut = em.MODELS[em.CUT_TOKENIZER]
tok1 = AutoTokenizer.from_pretrained(snapshot_download(cut["id"], revision=cut["revision"],
                                                       allow_patterns=["*.json", "*.txt"]))
spec = em.MODELS["nomic-embed-v1.5"]
tok4 = AutoTokenizer.from_pretrained(snapshot_download(spec["id"], revision=spec["revision"],
                                                       allow_patterns=spec["allow"]), model_max_length=10 ** 9)
rows = [json.loads(l) for l in open(os.path.join(em.ROOT, "data/manifest_s11.jsonl"))]
rows = [r for r in rows if r["modality"] in ("text", "table", "pdf_text", "other")]
n = over2048 = 0
over = []
with ThreadPoolExecutor(2) as pool:
    for r, (kind, payload, note) in zip(rows, pool.map(em.prepare, rows)):
        if kind != "text":
            continue
        t = tok1.decode(tok1(payload, add_special_tokens=False)["input_ids"][:2000])
        m = len(tok4("search_query: " + t)["input_ids"])
        n += 1
        over2048 += m > 2048
        if m > 8192:
            over.append((r["path"], r["modality"], m))
print(f"text inputs {n}; over 2048 E4 tokens {over2048}; over 8192 (cut by E4's tokenizer) {len(over)}")
for p in over:
    print(" ", *p)
