#!/usr/bin/env python3
"""dirvec session 18: written folder abstracts against per-modality representatives (BRIEF.md, session 18).

Subcommands, in the order scripts/s18_run.sh runs them:
  heads      E1 venv, CPU. The first 500 tokens (E1's Qwen2.5 tokenizer) of the text embed.py's
             prepare() extracts, for every text-like file embedded under E1 -> data/emb/s18/heads.jsonl
  describe   vLLM venv, one model. One sentence per member image, written by a vision-language model
             outside the Qwen family: every S11 evaluation query of cell P1 and 2,000 of cell M1
             (seed 20261018) -> data/emb/s18/members.jsonl. Exit 10 if the model fails the smoke test.
  summarize  vLLM venv, one model. A caption of every image and of the first page of every scanned PDF
             embedded under E1, then per folder the L1 overview, the L0 sentence and the with-names L1
             -> data/emb/s18/captions.jsonl, abstracts.jsonl. Exit 10 if the model fails the smoke test.
  embed      E1 or E3 environment. Abstracts, captions and member descriptions through the encoder's
             text path -> data/emb/<emb>/s18_vecs.npz
  eval       E1 venv, CPU. Rows, cells, creator-clustered intervals, verdicts of H18a and H18b -> stdout

Every generation step appends one json line per item and skips items already written, so a rerun
resumes. Nothing is fitted or chosen on the queries.
"""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
DATA = os.path.join(ROOT, "data")
GEN = os.path.join(DATA, "emb", "s18")
E1_EMB = "jina-embeddings-v4_s11"
MAN, DIRS, SEL = "data/manifest_s11.jsonl", "data/dirs_s11.jsonl", "data/selection_s11.jsonl"
IMAGE_INPUTS = ("image", "pdf_scanned")
LO_B, HI_B = ("[0,.2)", "[.2,.5)"), ("[.5,.8)", "[.8,1]")
MAXPIX = 602112            # E1's pixel cap (768 tokens of 28 x 28)
HEAD_TOKENS = 500
SEED = 18
M1_N, M1_SEED = 2000, 20261018
SUB_SEED = 20261019        # one folder per creator family
GATE, MARGIN = 0.25, 0.05
L1_MAX, L0_MAX = 4000, 256
SUMMARIZERS = ["Qwen/Qwen3-VL-8B-Instruct", "Qwen/Qwen2.5-VL-7B-Instruct"]
DESCRIBERS = ["mistral-community/pixtral-12b", "HuggingFaceM4/Idefics3-8B-Llama3",
              "llava-hf/llava-v1.6-mistral-7b-hf"]
KIND = {"image": ("image", "images"), "pdf_scanned": ("scanned document", "scanned documents"),
        "pdf_text": ("PDF document", "PDF documents"), "text": ("text file", "text files"),
        "table": ("table", "tables"), "other": ("office document", "office documents")}
FOUR = {"digital humanities jena", "nona, dronova", "royal botanic garden edinburgh",
        "finnish museum of natural history luomus, university of helsinki"}

PROMPT_CAPTION = (
    "Describe this image for a search index in two to four plain sentences: what it shows, what kind of "
    "image it is (for example a photograph, micrograph, map, chart, diagram, drawing or scanned page), and "
    "any visible words that name its subject. Do not write digits, codes or identifiers.")
PROMPT_MEMBER = (
    "Write one sentence that describes this image, the way someone searching for it would describe it. "
    "Do not write digits, codes, identifiers or file names.")
PROMPT_L1 = (
    "Below is the content of one folder. For each file you see its type, the words of its name, and either "
    "a description of the image or the beginning of its text.\n\n"
    "Write an overview of this folder for a search index: at most 4,000 characters of plain prose. Say what "
    "the folder is about, what kinds of files it holds, and what the files show or contain, so that someone "
    "searching for any one of its files would recognise this folder. Cover every kind of file in the folder, "
    "the images as well as the documents. Do not write digits, codes, identifiers or file names. Do not use "
    "lists, headings or markdown.\n\n{header}\n\n{entries}")
PROMPT_SW1 = (
    "Below is the content of one folder. For each file you see its type, its file name, and either a "
    "description of the image or the beginning of its text.\n\n"
    "Write an overview of this folder for a search index: at most 4,000 characters of plain prose. Say what "
    "the folder is about, what kinds of files it holds, and what the files show or contain, so that someone "
    "searching for any one of its files would recognise this folder. Cover every kind of file in the folder, "
    "the images as well as the documents. You may name files. Do not use lists, headings or markdown.\n\n"
    "{header}\n\n{entries}")
PROMPT_L0 = (
    "Here is an overview of one folder. Write one sentence of at most 256 characters that says what the "
    "folder holds, for a search index. Do not write digits, codes, identifiers or file names. Plain text "
    "only.\n\n{l1}")
DIGIT = re.compile(r"\d")


def log(msg):
    print(f"{time.strftime('%H:%M:%S', time.gmtime())} {msg}", file=sys.stderr, flush=True)


def jl(path):
    with open(path if os.path.isabs(path) else os.path.join(ROOT, path)) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def done_keys(path, key):
    return {r[key] for r in jl(path)} if os.path.exists(path) else set()


def e1_ok(manifest):
    idx = jl(os.path.join("data/emb", E1_EMB, "index.jsonl"))
    assert [r["path"] for r in idx] == [r["path"] for r in manifest], "E1 cache order differs from the manifest"
    return [bool(r.get("ok")) for r in idx]


def name_words(path):
    b = os.path.basename(path)
    i = b.rfind(".")
    stem = b[:i] if i > 0 else b
    return [w for w in re.findall(r"[^\W\d_]+", stem) if len(w) >= 2]


def clean(t):
    return " ".join(re.sub(r"[*#`]+", "", t or "").split())


def strip_digit_tokens(t):
    return " ".join(w for w in t.split() if not DIGIT.search(w))


def cut(t, n, sentence):
    if len(t) <= n:
        return t
    c = t[:n + 1]
    if sentence:
        ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", c) if m.end() <= n]
        if ends and ends[-1] >= n // 2:
            return c[:ends[-1]]
    k = c[:n].rfind(" ")
    return c[:k] if k > 0 else c[:n]


# ---------------------------------------------------------------- images for the VLMs

def image_data_url(row):
    """JPEG data URL of the file's image (pdf_scanned: page one at 100 dpi), at most MAXPIX pixels,
    the short side at least 56 px; None when there is no usable image."""
    import embed as em
    from PIL import Image
    path = os.path.join(ROOT, row["path"])
    if row["modality"] == "pdf_scanned":
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "100", "-png", path, os.path.join(td, "p")],
                           capture_output=True, timeout=600)
            pngs = sorted(f for f in os.listdir(td) if f.endswith(".png"))
            if not pngs:
                return None
            im = em.load_rgb(os.path.join(td, pngs[0]))
    else:
        im = em.load_rgb(path)
    w, h = im.size
    if min(w, h) < 1 or max(w, h) > 200 * min(w, h):
        return None
    if w * h > MAXPIX:
        s = (MAXPIX / (w * h)) ** 0.5
        im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.BICUBIC)
    w, h = im.size
    if min(w, h) < 56:
        s = 56 / min(w, h)
        im = im.resize((max(56, round(w * s)), max(56, round(h * s))), Image.BICUBIC)
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def safe_payload(row):
    try:
        return image_data_url(row)
    except Exception as e:  # noqa: BLE001
        log(f"image failed {row['path']}: {e!r}"[:200])
        return None


def chat(llm, sp, convs):
    """Texts for a batch of conversations; a failed batch is retried one conversation at a time."""
    try:
        return [o.outputs[0].text for o in llm.chat(convs, sp, use_tqdm=False)]
    except Exception as e:  # noqa: BLE001
        log(f"batch of {len(convs)} failed ({e!r}"[:200] + "); one at a time")
    out = []
    for c in convs:
        try:
            out.append(llm.chat([c], sp, use_tqdm=False)[0].outputs[0].text)
        except Exception as e:  # noqa: BLE001
            log(f"item failed: {e!r}"[:200])
            out.append(None)
    return out


def gen_images(llm, sp, rows, prompt, workers, chunk=256):
    """Yield (row, raw text or None) in row order; images are prepared on worker threads."""
    from concurrent.futures import ThreadPoolExecutor

    def run(buf):
        convs = [[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": p}},
                                               {"type": "text", "text": prompt}]}] for _, p in buf if p]
        it = iter(chat(llm, sp, convs) if convs else [])
        for r, p in buf:
            yield r, (next(it) if p else None)

    with ThreadPoolExecutor(workers) as ex:
        buf = []
        for r, p in zip(rows, ex.map(safe_payload, rows)):
            buf.append((r, p))
            if len(buf) >= chunk:
                yield from run(buf)
                buf = []
        if buf:
            yield from run(buf)


def load_llm(model_id, max_len, qwen, fake=False):
    if fake:
        return FakeLLM(model_id), "fake"
    from huggingface_hub import snapshot_download
    import vllm
    from vllm import LLM
    local = snapshot_download(model_id, allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "*.jinja",
                                                        "*.py", "*.tiktoken"])
    rev = os.path.basename(local.rstrip("/"))
    log(f"{model_id} revision {rev}; vllm {vllm.__version__}")
    llm = LLM(model=local, max_model_len=max_len, seed=SEED, gpu_memory_utilization=0.88,
              limit_mm_per_prompt={"image": 1, "video": 0} if qwen else {"image": 1})
    return llm, rev


def sampling(max_tokens, fake=False):
    if fake:
        return {"max_tokens": max_tokens}
    from vllm import SamplingParams
    return SamplingParams(temperature=0.0, max_tokens=max_tokens, seed=SEED)


class FakeLLM:
    """CPU stand-in for the local tests: echoes a digest of the prompt."""

    class _O:
        def __init__(self, t):
            self.outputs = [type("X", (), {"text": t})()]

    def __init__(self, name):
        self.name = name

    def chat(self, convs, sp, use_tqdm=False):
        out = []
        for c in convs:
            content = c[0]["content"]
            txt = content if isinstance(content, str) else content[-1]["text"]
            n = sp["max_tokens"] * 4
            out.append(self._O(("A folder about 12 rocks and a map, file E0001. " * 200)[:n] if "folder" in txt
                               else f"An image of a grey rock sample 42 next to a ruler, {len(txt)} words."))
        return out


def smoke(llm, sp, rows, prompt, workers):
    outs = [clean(t or "") for _, t in gen_images(llm, sp, rows, prompt, workers)]
    for r, t in zip(rows, outs):
        log(f"smoke {os.path.basename(r['path'])}: {t[:160]}")
    return len(outs) == len(rows) and all(len(t) >= 10 for t in outs)


# ---------------------------------------------------------------- heads

def cmd_heads(a):
    import embed as em
    from concurrent.futures import ThreadPoolExecutor
    man = jl(MAN)
    ok = e1_ok(man)
    rows = [r for r, o in zip(man, ok) if o and r["modality"] not in IMAGE_INPUTS]
    if a.fake:
        class T:
            def __call__(self, t, add_special_tokens=False):
                return {"input_ids": t.split()}

            def decode(self, ids):
                return " ".join(ids)
        tok = T()
    else:
        from huggingface_hub import snapshot_download
        from transformers import AutoTokenizer
        spec = em.MODELS[em.CUT_TOKENIZER]
        tok = AutoTokenizer.from_pretrained(snapshot_download(spec["id"], revision=spec["revision"],
                                                              allow_patterns=["*.json", "*.txt"]))
    os.makedirs(GEN, exist_ok=True)
    out = os.path.join(GEN, "heads.jsonl")
    n_empty, t0 = 0, time.time()
    with open(out + ".tmp", "w") as fh, ThreadPoolExecutor(a.workers) as ex:
        for i, (r, (kind, payload, note)) in enumerate(zip(rows, ex.map(em.prepare, rows))):
            head = ""
            if kind == "text":
                head = " ".join(tok.decode(tok(payload[:20000], add_special_tokens=False)["input_ids"][:HEAD_TOKENS]).split())
            n_empty += not head
            fh.write(json.dumps({"path": r["path"], "head": head, "note": note}) + "\n")
            if (i + 1) % 2000 == 0:
                log(f"heads {i + 1}/{len(rows)}")
    os.replace(out + ".tmp", out)
    print(f"heads: {len(rows)} text-like files embedded under E1, {n_empty} without text, {time.time() - t0:.0f}s")


# ---------------------------------------------------------------- describe

def member_queries():
    ranks = jl(os.path.join("data/emb", E1_EMB, "ranks_s11_e1.jsonl"))
    p1 = [g for g in ranks if g["modality"] == "image" and g["image_frac_bucket"] in LO_B]
    m1 = [g for g in ranks if g["modality"] == "image" and g["image_frac_bucket"] in HI_B]
    pick = sorted(np.random.default_rng(M1_SEED).choice(len(m1), min(M1_N, len(m1)), replace=False))
    return [(g, "P1") for g in p1] + [(m1[i], "M1") for i in pick], len(p1), len(m1)


def strip_member(raw, path):
    t = strip_digit_tokens(clean(raw))
    nw = {w.lower() for w in name_words(path) if len(w) >= 3}
    keep, removed = [], 0
    for w in t.split():
        if re.sub(r"^\W+|\W+$", "", w).lower() in nw:
            removed += 1
        else:
            keep.append(w)
    return " ".join(keep), removed


def cmd_describe(a):
    byp = {r["path"]: r for r in jl(MAN)}
    qs, n_p1, n_m1 = member_queries()
    log(f"member queries: P1 {n_p1} (all), M1 {sum(c == 'M1' for _, c in qs)} of {n_m1}")
    llm, rev = load_llm(a.model, 8192, qwen=False, fake=a.fake)
    sp = sampling(80, a.fake)
    if not smoke(llm, sp, [byp[g["query_path"]] for g, _ in qs[:10]], PROMPT_MEMBER, a.workers):
        log(f"smoke test failed for {a.model}")
        sys.exit(10)
    out = os.path.join(GEN, "members.jsonl")
    done = done_keys(out, "path")
    todo = [(g, c) for g, c in qs if g["query_path"] not in done]
    cell = {g["query_path"]: (g, c) for g, c in todo}
    n, t0 = 0, time.time()
    with open(out, "a") as fh:
        for r, raw in gen_images(llm, sp, [byp[g["query_path"]] for g, _ in todo], PROMPT_MEMBER, a.workers):
            g, c = cell[r["path"]]
            text, removed = strip_member(raw, r["path"]) if raw else ("", 0)
            fh.write(json.dumps({"path": r["path"], "dir": g["relevant_dir"], "cell": c,
                                 "bucket": g["image_frac_bucket"], "raw": raw, "text": text,
                                 "name_tokens_removed": removed, "model": a.model, "revision": rev}) + "\n")
            n += 1
            if n % 500 == 0:
                fh.flush()
                log(f"describe {n}/{len(todo)} ({time.time() - t0:.0f}s)")
    log(f"describe done: {n} new, {len(done)} earlier")


# ---------------------------------------------------------------- summarize

def folder_prompt(files, caps, heads, with_names, max_head_chars=None):
    kinds = Counter(r["modality"] for r in files)
    parts = [f"{n} {KIND[m][0] if n == 1 else KIND[m][1]}" for m, n in sorted(kinds.items(), key=lambda x: -x[1])]
    header = f"The folder holds {len(files)} file{'s' if len(files) != 1 else ''}: " + ", ".join(parts) + "."
    lines = []
    for i, r in enumerate(files, 1):
        kind = KIND[r["modality"]][0]
        label = (f"file name: {os.path.basename(r['path'])}" if with_names
                 else f"name words: {' '.join(name_words(r['path'])) or 'none'}")
        if r["modality"] in IMAGE_INPUTS:
            content = f"Image description: {caps.get(r['path']) or '(no description)'}"
        else:
            h = heads.get(r["path"]) or "(no text)"
            content = f"Beginning of the text: {h[:max_head_chars] if max_head_chars else h}"
        lines.append(f"File {i}: {kind}; {label}. {content}")
    return (PROMPT_SW1 if with_names else PROMPT_L1).format(header=header, entries="\n".join(lines))


def cmd_summarize(a):
    man = jl(MAN)
    ok = e1_ok(man)
    rows_img = [r for r, o in zip(man, ok) if o and r["modality"] in IMAGE_INPUTS]
    llm, rev = load_llm(a.model, 40960, qwen=True, fake=a.fake)
    sp_cap, sp_l1, sp_l0 = sampling(200, a.fake), sampling(1200, a.fake), sampling(100, a.fake)
    if not smoke(llm, sp_cap, rows_img[:10], PROMPT_CAPTION, a.workers):
        log(f"smoke test failed for {a.model}")
        sys.exit(10)
    capf = os.path.join(GEN, "captions.jsonl")
    done = done_keys(capf, "path")
    todo = [r for r in rows_img if r["path"] not in done]
    n, t0 = 0, time.time()
    with open(capf, "a") as fh:
        for r, raw in gen_images(llm, sp_cap, todo, PROMPT_CAPTION, a.workers):
            fh.write(json.dumps({"path": r["path"], "raw": raw,
                                 "caption": strip_digit_tokens(clean(raw)) if raw else "",
                                 "model": a.model, "revision": rev}) + "\n")
            n += 1
            if n % 1000 == 0:
                fh.flush()
                log(f"captions {n}/{len(todo)} ({time.time() - t0:.0f}s)")
    log(f"captions done: {n} new, {len(done)} earlier")

    caps = {c["path"]: c["caption"] for c in jl(capf)}
    heads = {h["path"]: h["head"] for h in jl(os.path.join(GEN, "heads.jsonl"))}
    by_dir = defaultdict(list)
    for r, o in zip(man, ok):
        if o:
            by_dir[r["dir"]].append(r)
    absf = os.path.join(GEN, "abstracts.jsonl")
    done = done_keys(absf, "dir")
    todo = [d for d in sorted(by_dir) if d not in done]
    tok = None if a.fake else llm.get_tokenizer()

    def fit(files, with_names):
        p = folder_prompt(files, caps, heads, with_names)
        if tok is not None and len(tok(p)["input_ids"]) > 39000:      # 60 long text files at most in S11
            p = folder_prompt(files, caps, heads, with_names, max_head_chars=600)
        return p

    n, t0 = 0, time.time()
    with open(absf, "a") as fh:
        for s in range(0, len(todo), a.chunk):
            ds = todo[s:s + a.chunk]
            convs = ([[{"role": "user", "content": fit(by_dir[d], False)}] for d in ds] +
                     [[{"role": "user", "content": fit(by_dir[d], True)}] for d in ds])
            outs = chat(llm, sp_l1, convs)
            l1_raw, sw_raw = outs[:len(ds)], outs[len(ds):]
            l1 = [cut(strip_digit_tokens(clean(t)), L1_MAX, True) if t else "" for t in l1_raw]
            have = [i for i, x in enumerate(l1) if x]
            got = chat(llm, sp_l0, [[{"role": "user", "content": PROMPT_L0.format(l1=l1[i])}] for i in have])
            l0_raw = [None] * len(ds)
            for i, t in zip(have, got):
                l0_raw[i] = t
            for i, d in enumerate(ds):
                fh.write(json.dumps({
                    "dir": d, "n_files": len(by_dir[d]),
                    "l1": l1[i], "l0": cut(strip_digit_tokens(clean(l0_raw[i])), L0_MAX, False) if l0_raw[i] else "",
                    "sw1": cut(clean(sw_raw[i]), L1_MAX, True) if sw_raw[i] else "",
                    "l1_raw": l1_raw[i], "l0_raw": l0_raw[i], "sw1_raw": sw_raw[i],
                    "model": a.model, "revision": rev}) + "\n")
            n += len(ds)
            fh.flush()
            log(f"abstracts {n}/{len(todo)} ({time.time() - t0:.0f}s)")
    log(f"abstracts done: {n} new, {len(done)} earlier")


# ---------------------------------------------------------------- embed

def cmd_embed(a):
    absr = jl(os.path.join(GEN, "abstracts.jsonl"))
    caps = jl(os.path.join(GEN, "captions.jsonl"))
    mem = jl(os.path.join(GEN, "members.jsonl"))
    if a.fake:
        class Enc:
            dim = 16

            def truncate(self, t):
                return t, len(t.split())

            def encode_texts(self, texts, mode):
                rng = np.random.default_rng(len(texts))
                v = rng.normal(size=(len(texts), self.dim)).astype(np.float32)
                return v / np.linalg.norm(v, axis=1, keepdims=True)
        enc = Enc()
    else:
        import embed as em
        enc = em.Encoder(a.model, batch_text=a.batch)
    empty = Counter()

    def E(name, texts):
        t0 = time.time()
        empty[name] = sum(not t for t in texts)
        v = enc.encode_texts([enc.truncate(t)[0] if t else "(no text)" for t in texts], "query")
        log(f"{a.model}: {name} {len(texts)} texts in {time.time() - t0:.0f}s")
        return v.astype(np.float32)

    out = {"abs_dirs": np.array([r["dir"] for r in absr]),
           "l1": E("l1", [r["l1"] for r in absr]), "l0": E("l0", [r["l0"] for r in absr]),
           "sw1": E("sw1", [r["sw1"] for r in absr]),
           "cap_paths": np.array([r["path"] for r in caps]), "cap": E("captions", [r["caption"] for r in caps]),
           "mem_paths": np.array([r["path"] for r in mem]), "mem": E("members", [r["text"] for r in mem])}
    path = os.path.join(DATA, "emb", a.emb, "s18_vecs.npz")
    np.savez(path, **out)
    print(f"{a.model}: wrote {path}; empty texts encoded as '(no text)': {dict(empty)}")


# ---------------------------------------------------------------- eval

def bm25_matrix(docs, k1=1.2, b=0.75):
    from sklearn.feature_extraction.text import CountVectorizer
    import scipy.sparse as sp
    cv = CountVectorizer(token_pattern=r"(?u)\b\w+\b", lowercase=True, dtype=np.float32)
    tf = cv.fit_transform(docs).tocsr()
    dl = np.asarray(tf.sum(axis=1)).ravel()
    avg = dl.mean()
    df = np.asarray((tf > 0).sum(axis=0)).ravel()
    idf = np.log(1 + (len(docs) - df + 0.5) / (df + 0.5)).astype(np.float32)
    tf = tf.tocoo()
    w = idf[tf.col] * tf.data * (k1 + 1) / (tf.data + k1 * (1 - b + b * dl[tf.row] / avg))
    W = sp.csr_matrix((w.astype(np.float32), (tf.row, tf.col)), shape=tf.shape)
    return cv, W


def lexical_ranks(S, pos):
    """Ranks from a score matrix (queries, folders); a target scoring zero counts as a miss."""
    tgt = S[np.arange(len(pos)), pos]
    rk = 1 + (S > tgt[:, None]).sum(axis=1)
    rk[tgt <= 0] = S.shape[1]
    return rk


def vec_ranks(Q, blocks, pos):
    starts = np.cumsum([0] + [len(x) for x in blocks[:-1]])
    R = np.concatenate(blocks).astype(np.float32)
    rk = np.zeros(len(Q), int)
    for i in range(0, len(Q), 256):
        D = np.maximum.reduceat(Q[i:i + 256] @ R.T, starts, axis=1)
        tgt = D[np.arange(len(D)), pos[i:i + 256]]
        rk[i:i + 256] = 1 + (D > tgt[:, None]).sum(axis=1)
    return rk


def cmd_eval(a):
    import eval as ev
    import descq
    import validity as va
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize

    man = jl(MAN)
    dirs = {r["dir"]: r for r in jl(DIRS)}
    sel = {r["id"]: r for r in jl(SEL)}
    emb_dir = os.path.join(DATA, "emb", a.emb)
    index = jl(os.path.join(emb_dir, "index.jsonl"))
    assert [r["path"] for r in index] == [r["path"] for r in man], "cache order differs from the manifest"
    ok = np.array([bool(r.get("ok")) for r in index])
    mods = np.array([r["modality"] for r in man])
    dir_of = np.array([r["dir"] for r in man])
    dir_list = sorted(d for d in set(dir_of[ok]) if d in dirs)
    pos = {d: i for i, d in enumerate(dir_list)}
    ch = {d: np.where((dir_of == d) & ok)[0] for d in dir_list}
    X = ev.unit(np.load(os.path.join(emb_dir, "vectors.npy"))).astype(np.float32)
    with np.load(os.path.join(emb_dir, "s18_vecs.npz")) as z:      # read every array once (an NpzFile rereads per access)
        S18 = {k: z[k] for k in z.files}
    absr = {r["dir"]: r for r in jl(os.path.join(GEN, "abstracts.jsonl"))}
    caps = {r["path"]: r for r in jl(os.path.join(GEN, "captions.jsonl"))}
    heads = {r["path"]: r["head"] for r in jl(os.path.join(GEN, "heads.jsonl"))}
    mem = jl(os.path.join(GEN, "members.jsonl"))

    def fam_of(d):
        cr = sel[dirs[d]["record"]].get("creators") or []
        return cr[0].strip().lower() if cr else f"record:{dirs[d]['record']}"

    out = [f"## Session 18, {a.model} (cache {a.emb})", ""]
    # vectors of the generated texts
    apos = {d: i for i, d in enumerate(S18["abs_dirs"])}
    missing = [d for d in dir_list if d not in apos]
    assert not missing, f"{len(missing)} ranked folders have no abstract"
    S = {k: {d: ev.unit(S18[k][apos[d]][None, :]).astype(np.float32) for d in dir_list} for k in ("l1", "l0", "sw1")}
    cpos = {p: i for i, p in enumerate(S18["cap_paths"])}
    Xt = X.copy()
    n_rep = n_keep = 0
    for i in np.where(ok & np.isin(mods, IMAGE_INPUTS))[0]:
        p = man[i]["path"]
        if p in cpos and caps.get(p, {}).get("caption"):
            Xt[i] = ev.unit(S18["cap"][cpos[p]])
            n_rep += 1
        else:
            n_keep += 1
    t0 = time.time()
    reps = {}
    for name, XX, base in (("a", X, "a"), ("c", X, "c"), ("d", X, "d"), ("ta", Xt, "a"), ("tc", Xt, "c"), ("td", Xt, "d")):
        reps[name] = [ev.build(base, XX[ch[d]], mods[ch[d]]) for d in dir_list]
    reps["s1"] = [S["l1"][d] for d in dir_list]
    reps["s0"] = [S["l0"][d] for d in dir_list]
    reps["sw1"] = [S["sw1"][d] for d in dir_list]
    reps["s1c"] = [np.concatenate([c, s]) for c, s in zip(reps["c"], reps["s1"])]
    log(f"{a.model}: representations built in {time.time() - t0:.0f}s")
    VROWS = ["a", "c", "d", "s1", "s0", "sw1", "s1c", "ta", "tc", "td"]
    ROWS = VROWS + ["bm25", "fn"]

    # lexical rows: BM25 over each folder's full file names, captions and text heads; file names alone
    docs = []
    for d in dir_list:
        parts = []
        for i in ch[d]:
            p = man[i]["path"]
            parts.append(os.path.basename(p))
            parts.append(caps[p]["caption"] if p in caps else heads.get(p, ""))
        docs.append(" ".join(parts))
    cv, W = bm25_matrix(docs)
    files = [i for d in dir_list for i in ch[d]]
    owner = np.array([pos[man[i]["dir"]] for i in files])
    names = [va.stem_ext(man[i]["path"])[0] for i in files]
    tv = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), sublinear_tf=True)
    NX = normalize(tv.fit_transform(names)).astype(np.float32).tocsr()
    bounds = np.searchsorted(owner, np.arange(len(dir_list) + 1))

    def lex(texts, tpos):
        Qb = cv.transform(texts)
        Qb.data[:] = 1
        r_bm = lexical_ranks((Qb @ W.T).toarray(), tpos)
        T = normalize(tv.transform([t.lower() for t in texts])).astype(np.float32).tocsr()
        r_fn = np.zeros(len(texts), int)
        for s in range(0, len(texts), 400):
            sim = (T[s:s + 400] @ NX.T).toarray()
            D = np.maximum.reduceat(sim, bounds[:-1], axis=1)
            r_fn[s:s + 400] = lexical_ranks(D, tpos[s:s + 400])
        return r_bm, r_fn

    # query sets
    qmap = descq.load_queries(dirs)
    dq = np.load(os.path.join(emb_dir, "descq_s12.npz"))
    sets = {}
    for which in ("title", "desc"):
        texts, keep = descq.query_texts(qmap, dir_list, which)
        assert list(dq[which + "_dirs"]) == keep, f"{which}: query order differs from descq_s12.npz"
        qb = np.array([ev.bucket_of(dirs[d]["image_frac"]) for d in keep])
        sets[which] = {"Q": dq[which + "_vecs"].astype(np.float32), "texts": texts, "dirs": keep,
                       "cells": {"all": np.ones(len(keep), bool), "text-heavy": np.isin(qb, LO_B),
                                 "image-heavy": np.isin(qb, HI_B)}}
    mpos = {p: i for i, p in enumerate(S18["mem_paths"])}
    mq = [m for m in mem if m["dir"] in pos]
    cellv = np.array([m["cell"] for m in mq])
    sets["mem"] = {"Q": np.stack([S18["mem"][mpos[m["path"]]] for m in mq]).astype(np.float32),
                   "texts": [m["text"] for m in mq], "dirs": [m["dir"] for m in mq],
                   "cells": {"P1": cellv == "P1", "M1": cellv == "M1"}}
    SEEDS = {("title", "all"): 1801, ("title", "text-heavy"): 1802, ("title", "image-heavy"): 1803,
             ("desc", "all"): 1811, ("desc", "text-heavy"): 1812, ("desc", "image-heavy"): 1813,
             ("mem", "P1"): 1850, ("mem", "M1"): 1856}
    PAIRS = {"title": [("s1", "c"), ("s1", "a"), ("c", "a"), ("s0", "c"), ("sw1", "s1"), ("s1c", "c"), ("s1c", "s1"),
                       ("d", "c"), ("ta", "a"), ("tc", "ta"), ("tc", "c"), ("td", "d"), ("bm25", "s1"), ("fn", "s1")],
             "mem": [("c", "s1"), ("c", "a"), ("c", "s0"), ("sw1", "s1"), ("s1c", "c"), ("s1c", "s1"), ("d", "c"),
                     ("ta", "a"), ("tc", "ta"), ("tc", "c"), ("td", "d"), ("bm25", "c"), ("fn", "c")]}
    PAIRS["desc"] = PAIRS["title"]
    KEY = {"title": [("s1", "c"), ("c", "a"), ("s1", "a")], "desc": [("s1", "c"), ("c", "a")],
           "mem": [("c", "s1"), ("c", "a"), ("d", "c")]}
    LABEL = {"title": "Q_title (record titles)", "desc": "Q_desc (title and description)",
             "mem": "Q_mem (one-sentence descriptions of member images; the image stays in its folder)"}

    ranks = {}
    for k, st in sets.items():
        tpos = np.array([pos[d] for d in st["dirs"]])
        R = {r: vec_ranks(st["Q"], reps[r], tpos) for r in VROWS}
        R["bm25"], R["fn"] = lex(st["texts"], tpos)
        ranks[k] = R
        st["fam"] = np.array([fam_of(d) for d in st["dirs"]])
    log(f"{a.model}: ranks done")

    # reproduction of descq.py's a, c and d ranks (session 17 dump)
    out.append("### Reproduction check")
    out.append("")
    if a.repro and os.path.exists(a.repro):
        old = [r for r in jl(a.repro)]
        bad = 0
        for which in ("title", "desc"):
            od = {r["relevant_dir"]: r for r in old if r["set"] == which}
            for r in ("a", "c", "d"):
                diff = sum(int(ranks[which][r][i]) != od[d][f"rank_{r}"] for i, d in enumerate(sets[which]["dirs"]))
                bad += diff
                out.append(f"- {which} {r}: {diff} of {len(sets[which]['dirs'])} ranks differ from {os.path.basename(a.repro)}")
        out.append("")
        if bad:
            out.append("NOT REPRODUCED: the a, c and d rows differ from descq.py. Stopping before any new number.")
            print("\n".join(out))
            sys.exit(3)
        out.append("Reproduced: a, c and d equal descq.py rank for rank.")
    else:
        out.append(f"- no session 17 rank dump at {a.repro}; not checked")
    out.append("")

    # what was generated
    ab = list(absr.values())
    lens = {k: np.array([len(r[k]) for r in ab]) for k in ("l1", "l0", "sw1")}
    out.append("### Generated texts")
    out.append("")
    out.append(f"- Summarizer {ab[0]['model']} (revision {ab[0]['revision']}); describer {mem[0]['model']} "
               f"(revision {mem[0]['revision']}).")
    out.append(f"- Abstracts: {len(ab)} folders; characters median / max: L1 {int(np.median(lens['l1']))} / "
               f"{lens['l1'].max()}, L0 {int(np.median(lens['l0']))} / {lens['l0'].max()}, with names "
               f"{int(np.median(lens['sw1']))} / {lens['sw1'].max()}; empty: L1 {int((lens['l1'] == 0).sum())}, "
               f"L0 {int((lens['l0'] == 0).sum())}, with names {int((lens['sw1'] == 0).sum())}; L1 or L0 with a digit: "
               f"{sum(bool(DIGIT.search(r['l1'] + r['l0'])) for r in ab)}.")
    out.append(f"- Captions: {len(caps)} ({sum(not r['caption'] for r in caps.values())} empty); under this encoder "
               f"{n_rep} image-input vectors replaced by their caption in ta, tc, td, {n_keep} kept (no caption).")
    nm = Counter(m["cell"] for m in mq)
    out.append(f"- Member descriptions: {len(mq)} ({dict(nm)}); empty {sum(not m['text'] for m in mq)}; name tokens "
               f"removed in {sum(m['name_tokens_removed'] > 0 for m in mq)} ({sum(m['name_tokens_removed'] for m in mq)} tokens).")
    out.append(f"- Folders ranked: {len(dir_list)}. Mean representative vectors per folder: " +
               ", ".join(f"{r} {np.mean([len(x) for x in reps[r]]):.2f}" for r in VROWS) + ".")
    out.append("")

    def hit(k, r, kk=5):
        return (ranks[k][r] <= kk).astype(float)

    verdict = {}
    for k, st in sets.items():
        cells = st["cells"]
        out.append(f"### {LABEL[k]}: {len(st['dirs'])} queries")
        out.append("")
        for kk in (5, 1, 10):
            out.append(f"Recall@{kk}:")
            out.append("")
            out.append("| cell | queries | families | " + " | ".join(ROWS) + " |")
            out.append("|---|---:|---:|" + "---:|" * len(ROWS))
            for cn, m in cells.items():
                out.append(f"| {cn} | {int(m.sum())} | {len(set(st['fam'][m]))} | " +
                           " | ".join(f"{hit(k, r, kk)[m].mean():.3f}" for r in ROWS) + " |")
            out.append("")
        out.append("Paired differences in recall@5, creator-clustered 95 percent interval (1,000 resamples of "
                   "first-creator families):")
        out.append("")
        out.append("| pair | " + " | ".join(cells) + " |")
        out.append("|---|" + "---|" * len(cells))
        for x, y in PAIRS[k]:
            cols = []
            for cn, m in cells.items():
                t = va.boot_mean((hit(k, x) - hit(k, y))[m], st["fam"][m], SEEDS[(k, cn)])
                cols.append(va.fmt(t))
                verdict[(k, cn, x, y)] = t
            out.append(f"| {x} - {y} | " + " | ".join(cols) + " |")
        out.append("")
        # one folder per creator family; the four digitization series apart
        rng = np.random.default_rng(SUB_SEED)
        out.append("One folder per creator family (drawn with seed 20261019), and the four digitization series "
                   "apart (recall@5 differences, clustered intervals):")
        out.append("")
        out.append("| cell | subset | queries | families | " + " | ".join(f"{x} - {y}" for x, y in KEY[k]) + " |")
        out.append("|---|---|---:|---:|" + "---|" * len(KEY[k]))
        for cn, m in cells.items():
            idx = np.where(m)[0]
            fam_dirs = defaultdict(set)
            for i in idx:
                fam_dirs[st["fam"][i]].add(st["dirs"][i])
            chosen = {f: sorted(ds)[rng.integers(len(ds))] for f, ds in sorted(fam_dirs.items())}
            one = np.array([st["dirs"][i] == chosen[st["fam"][i]] for i in idx])
            four = np.array([st["fam"][i] in FOUR for i in idx])
            for sn, sub in (("one folder per family", one), ("the four series", four), ("without the four series", ~four)):
                j = idx[sub]
                if len(j) == 0:
                    out.append(f"| {cn} | {sn} | 0 | 0 | " + " | ".join("" for _ in KEY[k]) + " |")
                    continue
                cols = [va.fmt(va.boot_mean((hit(k, x) - hit(k, y))[j], st["fam"][j], SEEDS[(k, cn)])) for x, y in KEY[k]]
                out.append(f"| {cn} | {sn} | {len(j)} | {len(set(st['fam'][j]))} | " + " | ".join(cols) + " |")
        out.append("")

    def outcome(t):
        if t[0] >= MARGIN and t[1] > 0:
            return "above c"
        if t[0] <= -MARGIN and t[2] < 0:
            return "below c"
        return "between"

    t = verdict[("title", "image-heavy", "s1", "c")]
    out.append(f"H18a ({a.model}): s1 - c on Q_title, image-heavy folders, recall@5 = {va.fmt(t)} over "
               f"{int(sets['title']['cells']['image-heavy'].sum())} queries and {t[3]} families: outcome '{outcome(t)}'.")
    g = hit("mem", "d")[sets["mem"]["cells"]["P1"]].mean()
    t1, t2 = verdict[("mem", "P1", "c", "s1")], verdict[("mem", "P1", "c", "a")]
    if g < GATE:
        line = f"gate d = {g:.3f} < {GATE}: H18b is not testable"
    else:
        p1 = t1[0] >= MARGIN and t1[1] > 0
        p2 = t2[0] >= MARGIN and t2[1] > 0
        line = (f"gate d = {g:.3f} >= {GATE} (passed); c - s1 = {va.fmt(t1)} ({'holds' if p1 else 'fails'}); "
                f"c - a = {va.fmt(t2)} ({'holds' if p2 else 'fails'}): H18b {'survives' if p1 and p2 else 'is dead'}")
    out.append(f"H18b ({a.model}): Q_mem P1, {int(sets['mem']['cells']['P1'].sum())} queries and {t1[3]} families; {line}.")
    print("\n".join(out))
    if a.dump_ranks:
        with open(a.dump_ranks, "w") as fh:
            for k, st in sets.items():
                for i, d in enumerate(st["dirs"]):
                    fh.write(json.dumps({"set": k, "relevant_dir": d, "query": mq[i]["path"] if k == "mem" else None,
                                         **{f"rank_{r}": int(ranks[k][r][i]) for r in ROWS}}) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["heads", "describe", "summarize", "embed", "eval"])
    ap.add_argument("--model", help="describe/summarize: HF model id; embed/eval: encoder name as in embed.py")
    ap.add_argument("--emb", help="embed/eval: cache directory under data/emb")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--chunk", type=int, default=512, help="summarize: folders per generation batch")
    ap.add_argument("--batch", type=int, default=32, help="embed: texts per encoder batch")
    ap.add_argument("--repro", help="eval: descq.py rank dump of session 17 for this encoder")
    ap.add_argument("--dump-ranks", help="eval: write per-query ranks of every row here")
    ap.add_argument("--fake", action="store_true", help="local CPU tests only: stand-ins for the models")
    a = ap.parse_args()
    os.makedirs(GEN, exist_ok=True)
    {"heads": cmd_heads, "describe": cmd_describe, "summarize": cmd_summarize, "embed": cmd_embed,
     "eval": cmd_eval}[a.cmd](a)


if __name__ == "__main__":
    main()
