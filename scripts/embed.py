#!/usr/bin/env python3
"""dirvec embedding: one vector per file, one unified multimodal encoder.

Input rule per manifest modality, fixed for the whole study:
  image        the image (RGB: JPEG draft and integer reduce to about 2048 px, palettes expanded,
               16-bit/float min-max scaled, alpha on white; build_gt.py hashes through the same path)
  text, table  extracted text, first 2000 tokens (csv/tsv/text read as UTF-8; xlsx via
               openpyxl, xls via xlrd, one tab-separated line per row, sheets in order;
               since session 4 an .xls that xlrd rejects and that is plain UTF-8 text is read as text)
  pdf_text     pdftotext output (first 50 pages), first 2000 tokens
  pdf_scanned  page renders at 100 dpi, first 8 pages, mean of page vectors
  other        office docs converted to text with pandoc (docx odt rtf), first 2000 tokens;
               anything pandoc cannot read (doc, pptx, odp, unreadable images) is skipped and counted
Token counts use the Qwen2.5 tokenizer shipped with the model (both candidates share it).
Every stored vector is L2-normalised.
The session 11 encoder E2 (jina-clip-v2) gets the same inputs: the text is cut to its first 2000
tokens with E1's Qwen2.5 tokenizer, so both encoders read the same characters, then goes through
E2's own tokenizer (limit 8192, not reached by 2000 Qwen tokens in practice; anything longer is
truncated there); the image is the same load_rgb image, resized by E2's shipped preprocessing
(shortest side to 512, centre crop). Text mode query is E2's task retrieval.query, doc the plain
text tower.
The session 14 encoder E3 (gme-Qwen2-VL-2B-Instruct, Alibaba) gets the same inputs as E1 and E2:
texts cut to their first 2000 tokens with E1's tokenizer, the same load_rgb images, the same page
renders. Fixed for E3: bfloat16; max_image_tokens 768 (E1's pixel cap, 602,112 pixels) and the
model's default min_image_tokens 256; max_length 2200, so a 2000-token text keeps the end token the
model pools on; no instruction for any input (the model's default system prompt), so its query and
document text paths are the same; the model's own embed() is called in batches (its
get_*_embeddings wrappers fork loader workers per call). Its code refuses transformers >= 4.52, so
it runs in the E1 venv with transformers 4.51.3 put first on PYTHONPATH (scripts/s14_run.sh).
The session 15 encoder E4 (Nomic Embed v1.5, Nomic AI) is a second CLIP-family dual tower: the image
tower nomic-embed-vision-v1.5 was trained contrastively against the frozen text tower
nomic-embed-text-v1.5; model code from nomic-ai/nomic-bert-2048 (trust_remote_code, code revision
pinned). Same inputs as E1 to E3: texts cut to their first 2000 tokens with E1's tokenizer, then
E4's own tokenizer with a limit of 8192 and rotary_scaling_factor 2 (dynamic NTK scaling, no change
below the 2048 trained positions); the same load_rgb images through E4's shipped
CLIPImageProcessor (squashed to 224 x 224, no crop); the same page renders. Fixed for E4: float32;
text vector = masked mean of the last hidden states, layer norm without parameters, L2 norm (the
model card's recipe, all 768 dimensions); image vector = the CLS token of the last hidden state, L2
norm. Text mode query is the prefix "search_query: " (the one the model card names for text used
against images), doc is "search_document: ". It runs in the E1 venv (transformers 4.52.4).

Stages
  pilot  embed all files of N pilot directories with one model, both text paths (query-side
         and document-side), and report the text -> own-directory-image rank check
         -> data/emb/pilot/<model><tag>.json
         Session 11: pilot --model jina-clip-v2 --manifest data/manifest_s11.jsonl
                           --dirs data/dirs_s11.jsonl --tag _s11 --calib 0.2 --calib-seed 20261102
         (the 20 directories are drawn from the calibration split, so no evaluation directory is read)
  all    embed every manifest file with one model and one text path
         -> data/emb/<model><tag>/vectors.npy (manifest order), index.jsonl (path, modality, ok, ...)
         Files already in the cache are never re-embedded; files whose input failed are retried.
         Session 3: all --model jina-embeddings-v4 --text-mode query
                        --manifest data/manifest_s3.jsonl --tag _s3
         Session 5: all --model jina-embeddings-v4 --text-mode query
                        --manifest data/manifest_s5.jsonl --tag _s5
         The cache is written every --checkpoint files (default 1000); inputs are prepared on
         --prep-workers threads (default 8), in row order.

Environments (transformers versions differ, so one venv per model):
  jina   transformers 4.52.4, peft 0.15.2, trust_remote_code
  gme    the jina venv with transformers 4.51.3 (--no-deps, its own target directory) first on PYTHONPATH
  nomic  colpali-engine 0.3.12, transformers 4.53.3, peft 0.16.0
  E2 runs in the jina venv plus einops and timm (trust_remote_code, no flash-attn, no xformers)
  E4 runs in the jina venv as is (transformers 4.52.4, einops; trust_remote_code, no flash-attn)
  both   torch 2.8.0+cu128, tifffile + imagecodecs (ZSTD TIFFs), openpyxl, xlrd, pandoc, poppler
"""
import argparse
import json
import os
import random
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
BUCKETS = ["[0,.2)", "[.2,.5)", "[.5,.8)", "[.8,1]"]

MODELS = {
    "jina-embeddings-v4": {"id": "jinaai/jina-embeddings-v4",
                           "revision": "853c867b65b749f3c3c72a06868140d842e04f06"},
    "nomic-embed-multimodal-3b": {"id": "nomic-ai/nomic-embed-multimodal-3b",
                                  "revision": "298930bb768c50b91d2799d6f3b0daf46ea52e70"},
    # session 11: E2, a CLIP-family dual tower
    "jina-clip-v2": {"id": "jinaai/jina-clip-v2",
                     "revision": "e10d47f5691d0454a0fb5d13f46f2199b74cb436", "dim": 1024,
                     "max_text_tokens": 8192},
    # session 14: E3, a VLM embedder from another vendor on another base (Qwen2-VL-2B)
    "gme-Qwen2-VL-2B-Instruct": {"id": "Alibaba-NLP/gme-Qwen2-VL-2B-Instruct",
                                 "revision": "9cfa6413f704a7c1cf5064d240748e10c876b286", "dim": 1536,
                                 "max_length": 2200, "min_image_tokens": 256},
    # session 15: E4, a second CLIP-family dual tower from a third vendor (Nomic AI). The text
    # revision is the last before the repository's transformers 5 rewrite; the code is pinned too.
    "nomic-embed-v1.5": {"id": "nomic-ai/nomic-embed-text-v1.5",
                         "revision": "e5cf08aadaa33385f5990def41f7a23405aec398",
                         "allow": ["*.json", "*.txt", "model.safetensors"],
                         "vision_id": "nomic-ai/nomic-embed-vision-v1.5",
                         "vision_revision": "e3a725bce72db07ca4adb1d83da08903f3ee02f8",
                         "code_revision": "7710840340a098cfb869c4f65e87cf2b1b70caca",
                         "dim": 768, "max_text_tokens": 8192, "rotary_scaling_factor": 2},
}
CUT_TOKENIZER = "jina-embeddings-v4"   # E2 and E3 texts are cut with E1's tokenizer
DEVICE = os.environ.get("DIRVEC_DEVICE", "cuda")  # E3 and E4 only; "cpu" for the smoke tests
MAX_TOKENS = 2000
MAX_PIXELS = 602112         # 768 visual tokens of 28x28; both models' shipped default
PDF_DPI, PDF_PAGES = 100, 8
TEXT_CHARS = 60000          # pre-cut before tokenising; 2000 tokens never need more
PANDOC_EXT = {"docx", "odt", "rtf"}  # pandoc 3.1.3 has no pptx reader


def bucket(frac):
    if frac < 0.2:
        return BUCKETS[0]
    if frac < 0.5:
        return BUCKETS[1]
    if frac < 0.8:
        return BUCKETS[2]
    return BUCKETS[3]


# ---------------------------------------------------------------- inputs

def minmax_u8(a):
    a = np.asarray(a, dtype=np.float64)
    lo, hi = np.nanmin(a), np.nanmax(a)
    a = np.zeros_like(a) if not hi > lo else (a - lo) * (255.0 / (hi - lo))
    return np.nan_to_num(a).astype(np.uint8)


def load_tiff_fallback(path):
    """TIFFs Pillow cannot decode (ZSTD compression, odd tiling): tifffile + imagecodecs,
    strided down to about 2048 px, min-max scaled unless already 8-bit RGB(A)."""
    import tifffile
    a = np.asarray(tifffile.imread(path, level=0))
    a = np.squeeze(a)
    if a.ndim == 3 and a.shape[0] in (3, 4) and a.shape[-1] not in (3, 4):
        a = np.moveaxis(a, 0, -1)
    if a.ndim == 3 and a.shape[-1] not in (3, 4):
        a = a[..., 0]
    k = max(1, -(-max(a.shape[:2]) // 2048))
    a = a[::k, ::k]
    if a.ndim == 2:
        return Image.fromarray(minmax_u8(a), "L").convert("RGB")
    a = a[..., :3]
    return Image.fromarray(a if a.dtype == np.uint8 else minmax_u8(a), "RGB")


def load_rgb(path):
    """RGB PIL image, about 2048 px at most. Palette images are
    expanded before the size reduce (Image.reduce rejects mode P); TIFFs Pillow cannot decode go
    through load_tiff_fallback."""
    try:
        return _load_rgb_pil(path)
    except Exception:  # noqa: BLE001
        if path.lower().endswith((".tif", ".tiff")):
            return load_tiff_fallback(path)
        raise


def _load_rgb_pil(path):
    with Image.open(path) as im:
        im.draft("RGB", (2048, 2048))
        im.load()
        if im.mode in ("P", "PA", "1"):
            im = im.convert("RGBA" if (im.mode == "PA" or "transparency" in im.info) else "RGB")
        k = max(im.size) // 2048
        if k > 1:
            im = im.reduce(k)
        if im.mode in ("I;16", "I;16B", "I;16L", "I", "F"):
            return Image.fromarray(minmax_u8(np.asarray(im)), "L").convert("RGB")
        if im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info):
            rgba = im.convert("RGBA")
            bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            bg.alpha_composite(rgba)
            return bg.convert("RGB")
        return im.convert("RGB")


def table_text(path, ext):
    lines = []
    if ext == "xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            lines.append(f"# sheet: {ws.title}")
            for row in ws.iter_rows(values_only=True):
                cells = ["" if v is None else str(v) for v in row]
                while cells and cells[-1] == "":
                    cells.pop()
                if cells:
                    lines.append("\t".join(cells))
                if sum(len(l) for l in lines) > TEXT_CHARS:
                    return "\n".join(lines)
        return "\n".join(lines)
    if ext == "xls":
        import xlrd
        try:
            wb = xlrd.open_workbook(path, on_demand=True)
        except xlrd.XLRDError:
            # session 4: tab-separated text saved with an .xls extension is read as text;
            # anything with NUL bytes or invalid UTF-8 in its first 4096 bytes still fails
            with open(path, "rb") as fh:
                head = fh.read(4096)
            if b"\x00" in head or not is_utf8(head):
                raise
            return raw_text(path)
        for sh in wb.sheets():
            lines.append(f"# sheet: {sh.name}")
            for i in range(sh.nrows):
                cells = [str(v) for v in sh.row_values(i)]
                while cells and cells[-1] == "":
                    cells.pop()
                if cells:
                    lines.append("\t".join(cells))
                if sum(len(l) for l in lines) > TEXT_CHARS:
                    return "\n".join(lines)
        return "\n".join(lines)
    return raw_text(path)


def is_utf8(head):
    """True if the bytes decode as UTF-8, allowing a multi-byte character cut at the end."""
    try:
        head.decode("utf-8")
    except UnicodeDecodeError as e:
        return e.start >= len(head) - 3
    return True


def raw_text(path):
    with open(path, "rb") as fh:
        return fh.read(TEXT_CHARS * 2).decode("utf-8", errors="replace").replace("\x00", "")[:TEXT_CHARS]


def pdf_text(path):
    r = subprocess.run(["pdftotext", "-l", "50", "-enc", "UTF-8", path, "-"],
                       capture_output=True, text=True, errors="replace", timeout=300)
    return r.stdout[:TEXT_CHARS]


def pdf_pages(path):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-f", "1", "-l", str(PDF_PAGES), "-r", str(PDF_DPI), "-png",
                        path, os.path.join(td, "p")], capture_output=True, timeout=600)
        pngs = sorted(f for f in os.listdir(td) if f.endswith(".png"))
        return [load_rgb(os.path.join(td, f)) for f in pngs]


def pandoc_text(path):
    r = subprocess.run(["pandoc", "-t", "plain", "--wrap=none", path],
                       capture_output=True, text=True, errors="replace", timeout=300)
    if r.returncode != 0:
        raise RuntimeError("pandoc: " + r.stderr.strip()[:80])
    return r.stdout[:TEXT_CHARS]


def prepare(row):
    """(kind, payload, note): kind in image | pages | text | skip."""
    path = os.path.join(ROOT, row["path"])
    m, ext = row["modality"], row["ext"]
    try:
        if m == "image":
            im = load_rgb(path)
            if min(im.size) < 28:  # below one 28 px vision patch the processor refuses the image
                return "skip", None, f"image smaller than 28 px ({im.size[0]}x{im.size[1]})"
            if max(im.size) > 200 * min(im.size):  # the processor refuses aspect ratios above 200
                return "skip", None, f"image aspect ratio above 200 ({im.size[0]}x{im.size[1]})"
            return "image", im, ""
        if m == "pdf_scanned":
            pages = pdf_pages(path)
            n_all = len(pages)
            # the same two refusals as for images, per rendered page (a tiny page crashed the
            # session 11 E1 run at file 25,000)
            pages = [pg for pg in pages if min(pg.size) >= 28 and max(pg.size) <= 200 * min(pg.size)]
            if not pages:
                return "skip", None, ("no pages rendered" if n_all == 0
                                      else f"{n_all} pages, none within the processor's size limits")
            note = f"{len(pages)} pages" + (f" ({n_all - len(pages)} dropped for size)" if n_all != len(pages) else "")
            return "pages", pages, note
        if m in ("text", "table"):
            t = table_text(path, ext) if m == "table" else raw_text(path)
        elif m == "pdf_text":
            t = pdf_text(path)
        elif m == "other" and ext in PANDOC_EXT:
            t = pandoc_text(path)
        else:
            return "skip", None, f"no encoder path for modality {m} ext {ext or '(none)'}"
    except Exception as e:  # noqa: BLE001
        return "skip", None, "input failed: " + repr(e)[:100]
    if not t.strip():
        return "skip", None, "empty text"
    return "text", t, ""


# ---------------------------------------------------------------- encoders

class Encoder:
    """Uniform wrapper: encode_texts(list[str], mode) / encode_images(list[PIL]) -> (n, d) unit vectors.
    mode 'query' uses the model's query-side text path, 'doc' its document-side text path."""

    def __init__(self, name, batch_text=8, batch_image=8):
        import torch
        self.torch = torch
        self.name = name
        self.bt, self.bi = batch_text, int(os.environ.get("DIRVEC_IMG_BATCH", batch_image))
        spec = MODELS[name]
        self.dim = spec.get("dim", 2048)
        from huggingface_hub import snapshot_download
        local = snapshot_download(spec["id"], revision=spec["revision"], allow_patterns=spec.get("allow"))
        if name == "jina-embeddings-v4":
            from transformers import AutoModel
            self.m = AutoModel.from_pretrained(local, trust_remote_code=True,
                                               torch_dtype=torch.bfloat16).cuda().eval()
            self.tok = self.m.processor.tokenizer
        elif name == "jina-clip-v2":
            from transformers import AutoModel, AutoTokenizer
            cut = MODELS[CUT_TOKENIZER]
            self.tok = AutoTokenizer.from_pretrained(snapshot_download(
                cut["id"], revision=cut["revision"], allow_patterns=["*.json", "*.txt"]))
            self.m = AutoModel.from_pretrained(local, trust_remote_code=True,
                                               torch_dtype=torch.bfloat16).cuda().eval()
        elif name == "gme-Qwen2-VL-2B-Instruct":
            import transformers
            from transformers import AutoConfig, AutoModel, AutoTokenizer
            if not transformers.__version__.startswith("4.51."):
                sys.exit(f"E3 needs transformers 4.51.x, found {transformers.__version__} ({transformers.__file__})")
            cut = MODELS[CUT_TOKENIZER]
            self.tok = AutoTokenizer.from_pretrained(snapshot_download(
                cut["id"], revision=cut["revision"], allow_patterns=["*.json", "*.txt"]))
            cfg = AutoConfig.from_pretrained(local, trust_remote_code=True,
                                             min_image_tokens=spec["min_image_tokens"],
                                             max_image_tokens=MAX_PIXELS // (28 * 28),
                                             max_length=spec["max_length"])
            cfg._name_or_path = local  # the model builds its processor from this path: the pinned snapshot
            self.m = AutoModel.from_pretrained(local, config=cfg, trust_remote_code=True,
                                               torch_dtype=torch.bfloat16).to(DEVICE).eval()
            ip = self.m.processor.image_processor
            print(f"E3: transformers {transformers.__version__}, max_length {self.m.max_length}, "
                  f"pixels {getattr(ip, 'min_pixels', None)} to {getattr(ip, 'max_pixels', None)}, "
                  f"instruction {self.m.default_instruction!r}", file=sys.stderr, flush=True)
            if self.m.max_length != spec["max_length"] or getattr(ip, "max_pixels", MAX_PIXELS) != MAX_PIXELS:
                sys.exit("E3 settings did not take")
        elif name == "nomic-embed-v1.5":
            import transformers
            from transformers import AutoImageProcessor, AutoModel, AutoTokenizer
            cut = MODELS[CUT_TOKENIZER]
            self.tok = AutoTokenizer.from_pretrained(snapshot_download(
                cut["id"], revision=cut["revision"], allow_patterns=["*.json", "*.txt"]))
            self.ttok = AutoTokenizer.from_pretrained(local, model_max_length=spec["max_text_tokens"])
            self.m = AutoModel.from_pretrained(local, trust_remote_code=True, code_revision=spec["code_revision"],
                                               rotary_scaling_factor=spec["rotary_scaling_factor"]).to(DEVICE).eval()
            vlocal = snapshot_download(spec["vision_id"], revision=spec["vision_revision"],
                                       allow_patterns=["*.json", "model.safetensors"])
            self.vm = AutoModel.from_pretrained(vlocal, trust_remote_code=True,
                                                code_revision=spec["code_revision"]).to(DEVICE).eval()
            self.vp = AutoImageProcessor.from_pretrained(vlocal)
            self.longest = 0  # longest text input seen, in E4 tokens (8192 would mean a cut)
            print(f"E4: transformers {transformers.__version__}, text {type(self.m).__name__} rotary scaling "
                  f"{self.m.config.rotary_scaling_factor}, image {type(self.vm).__name__}, processor "
                  f"{type(self.vp).__name__} size {self.vp.size} crop {self.vp.do_center_crop}",
                  file=sys.stderr, flush=True)
            if self.m.config.rotary_scaling_factor != spec["rotary_scaling_factor"]:
                sys.exit("E4 settings did not take")
        else:
            from colpali_engine.models import BiQwen2_5, BiQwen2_5_Processor
            self.m = BiQwen2_5.from_pretrained(local, torch_dtype=torch.bfloat16,
                                               device_map="cuda:0").eval()
            self.p = BiQwen2_5_Processor.from_pretrained(local)
            self.p.image_processor.max_pixels = MAX_PIXELS
            self.tok = self.p.tokenizer

    def dtype_name(self):
        """The dtype the weights were loaded in (E4 loads in float32; the others in bfloat16)."""
        return str(next(self.m.parameters()).dtype).replace("torch.", "")

    def truncate(self, text):
        ids = self.tok(text, add_special_tokens=False)["input_ids"][:MAX_TOKENS]
        return self.tok.decode(ids), len(ids)

    @staticmethod
    def _unit(a):
        a = np.asarray(a, dtype=np.float32)
        return a / np.maximum(np.linalg.norm(a, axis=1, keepdims=True), 1e-12)

    def encode_texts(self, texts, mode):
        if not texts:
            return np.zeros((0, self.dim), np.float32)
        out = []
        with self.torch.no_grad():
            for i in range(0, len(texts), self.bt):
                chunk = texts[i:i + self.bt]
                if self.name == "jina-embeddings-v4":
                    v = self.m.encode_text(chunk, task="retrieval", max_length=MAX_TOKENS + 16,
                                           prompt_name="query" if mode == "query" else "passage",
                                           batch_size=len(chunk), return_numpy=True)
                elif self.name == "jina-clip-v2":
                    v = self.m.encode_text(chunk, task="retrieval.query" if mode == "query" else None,
                                           batch_size=len(chunk), show_progress_bar=False,
                                           max_length=MODELS[self.name]["max_text_tokens"])
                elif self.name == "gme-Qwen2-VL-2B-Instruct":
                    # no instruction: query and document side are the same default system prompt
                    v = self.m.embed(texts=chunk, images=[None] * len(chunk), is_query=False)
                    v = v.float().cpu().numpy()
                elif self.name == "nomic-embed-v1.5":
                    prefix = "search_query: " if mode == "query" else "search_document: "
                    b = self.ttok([prefix + t for t in chunk], padding=True, truncation=True,
                                  max_length=MODELS[self.name]["max_text_tokens"], return_tensors="pt").to(DEVICE)
                    self.longest = max(self.longest, int(b["attention_mask"].sum(1).max()))
                    h = self.m(**b)[0]
                    msk = b["attention_mask"].unsqueeze(-1).to(h.dtype)
                    v = (h * msk).sum(1) / msk.sum(1).clamp(min=1e-9)
                    v = self.torch.nn.functional.layer_norm(v, normalized_shape=(v.shape[1],))
                    v = v.float().cpu().numpy()
                else:
                    b = (self.p.process_queries(texts=chunk) if mode == "query"
                         else self.p.process_texts(chunk)).to("cuda:0")
                    v = self.m(**b).float().cpu().numpy()
                out.append(self._unit(v))
        return np.concatenate(out)

    def encode_images(self, images):
        if not images:
            return np.zeros((0, self.dim), np.float32)
        out = []
        with self.torch.no_grad():
            for i in range(0, len(images), self.bi):
                chunk = images[i:i + self.bi]
                if self.name == "jina-embeddings-v4":
                    v = self.m.encode_image(chunk, task="retrieval", batch_size=len(chunk),
                                            max_pixels=MAX_PIXELS, return_numpy=True)
                elif self.name == "jina-clip-v2":
                    v = self.m.encode_image(chunk, batch_size=len(chunk), show_progress_bar=False)
                elif self.name == "gme-Qwen2-VL-2B-Instruct":
                    v = self.m.embed(texts=[None] * len(chunk), images=chunk, is_query=False)
                    v = v.float().cpu().numpy()
                elif self.name == "nomic-embed-v1.5":
                    b = self.vp(chunk, return_tensors="pt").to(DEVICE)
                    v = self.vm(**b).last_hidden_state[:, 0].float().cpu().numpy()
                else:
                    b = self.p.process_images(chunk).to("cuda:0")
                    v = self.m(**b).float().cpu().numpy()
                out.append(self._unit(v))
        return np.concatenate(out)


def embed_rows(enc, rows, modes, log_every=200, prep_workers=1):
    """Embed manifest rows. Returns {mode: (n, d) array}, info list. Skipped rows get zero vectors."""
    n = len(rows)
    vecs = {mode: np.zeros((n, enc.dim), np.float32) for mode in modes}
    info = [None] * n
    texts = []          # (i, text)
    t0 = time.time()
    img_buf = []        # (i, image)

    def flush_images():
        if not img_buf:
            return
        v = enc.encode_images([im for _, im in img_buf])
        for (i, _), x in zip(img_buf, v):
            for mode in modes:
                vecs[mode][i] = x
        img_buf.clear()

    # inputs are prepared (decoded, rendered, converted) on worker threads, in row order
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(prep_workers)
    prepared = pool.map(prepare, rows)
    for i, row in enumerate(rows):
        kind, payload, note = next(prepared)
        info[i] = {"path": row["path"], "modality": row["modality"], "ok": kind != "skip",
                   "input": kind, "note": note}
        if kind == "image":
            img_buf.append((i, payload))
            if len(img_buf) >= 32:
                flush_images()
        elif kind == "pages":
            v = enc.encode_images(payload).mean(axis=0, keepdims=True)
            v = enc._unit(v)[0]
            for mode in modes:
                vecs[mode][i] = v
        elif kind == "text":
            t, ntok = enc.truncate(payload)
            info[i]["tokens"] = ntok
            texts.append((i, t))
        if (i + 1) % log_every == 0:
            print(f"  prepared {i + 1}/{n} ({time.time() - t0:.0f}s)", file=sys.stderr, flush=True)
    flush_images()
    pool.shutdown()
    # texts sorted by length so batches pad little
    texts.sort(key=lambda x: len(x[1]))
    for mode in modes:
        v = enc.encode_texts([t for _, t in texts], mode)
        for (i, _), x in zip(texts, v):
            vecs[mode][i] = x
    print(f"  embedded {n} rows in {time.time() - t0:.0f}s", file=sys.stderr, flush=True)
    if hasattr(enc, "longest"):
        print(f"  longest text input {enc.longest} tokens (limit {MODELS[enc.name]['max_text_tokens']})",
              file=sys.stderr, flush=True)
    return vecs, info


# ---------------------------------------------------------------- stages

def load_manifest(path="data/manifest.jsonl"):
    with open(os.path.join(ROOT, path)) as fh:
        return [json.loads(l) for l in fh]


def load_dirs(path="data/dirs.jsonl"):
    with open(os.path.join(ROOT, path)) as fh:
        return {r["dir"]: r for r in (json.loads(l) for l in fh)}


def pilot_dirs(dirs, n, seed):
    """n directories, n/4 per image_frac bucket, each with >= 2 images and >= 1 text or table file."""
    rng = random.Random(seed)
    per = defaultdict(list)
    for d, r in sorted(dirs.items()):
        if r["n_image"] >= 2 and r["n_text"] + r["n_table"] >= 1:
            per[bucket(r["image_frac"])].append(d)
    out = []
    for b in BUCKETS:
        out += rng.sample(per[b], n // len(BUCKETS))
    return sorted(out)


def rank_check(vec, info, rows):
    """For each text/table file, rank every image of its own directory among all pilot images
    by cosine. Returns stats incl. the random expectation."""
    img = [i for i, r in enumerate(rows) if r["modality"] == "image" and info[i]["ok"]]
    img_dir = np.array([rows[i]["dir"] for i in img])
    X = vec[img]
    ranks, norm_ranks, best = [], [], []
    for i, r in enumerate(rows):
        if r["modality"] not in ("text", "table") or not info[i]["ok"]:
            continue
        own = img_dir == r["dir"]
        if not own.any():
            continue
        s = X @ vec[i]
        order = np.argsort(-s, kind="stable")
        rk = np.empty(len(s), int)
        rk[order] = np.arange(1, len(s) + 1)
        ranks += rk[own].tolist()
        norm_ranks += (rk[own] / len(s)).tolist()
        best.append(int(rk[own].min()))
    n_img = len(img)
    # random: rank uniform over 1..n_img; median of best-of-m under random by simulation
    rng = np.random.default_rng(0)
    own_counts = Counter(img_dir.tolist())
    sim_best = []
    for i, r in enumerate(rows):
        if r["modality"] in ("text", "table") and info[i]["ok"] and own_counts.get(r["dir"]):
            m = own_counts[r["dir"]]
            sim_best.append(np.median([rng.permutation(n_img)[:m].min() + 1 for _ in range(200)]))
    return {"n_images": n_img, "n_pairs": len(ranks), "n_text_queries": len(best),
            "median_rank": float(np.median(ranks)), "random_median_rank": (n_img + 1) / 2,
            "median_norm_rank": float(np.median(norm_ranks)),
            "median_best_own_rank": float(np.median(best)),
            "random_median_best_own_rank": float(np.median(sim_best))}


def stage_pilot(args):
    manifest, dirs = load_manifest(args.manifest), load_dirs(args.dirs)
    if args.calib:
        # session 11: draw the pilot inside the calibration split, so it reads no evaluation directory
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from eval import calib_split
        calib = calib_split(dirs, args.calib, args.calib_seed)
        dirs = {d: r for d, r in dirs.items() if d in calib}
    chosen = pilot_dirs(dirs, args.n_dirs, args.seed)
    rows = [r for r in manifest if r["dir"] in set(chosen)]
    print(f"pilot: {len(chosen)} dirs, {len(rows)} files, {Counter(r['modality'] for r in rows)}", file=sys.stderr)
    import torch
    enc = Encoder(args.model)
    t0 = time.time()
    vecs, info = embed_rows(enc, rows, ["query", "doc"])
    secs = time.time() - t0
    report = {"model": args.model, **MODELS[args.model], "dtype": enc.dtype_name(),
              "manifest": args.manifest, "calib": args.calib, "calib_seed": args.calib_seed,
              "gpu": torch.cuda.get_device_name(0), "seconds": round(secs, 1),
              "dirs": chosen, "n_files": len(rows),
              "skipped": Counter(x["note"] for x in info if not x["ok"]),
              "text_mode": {mode: rank_check(vecs[mode], info, rows) for mode in vecs}}
    os.makedirs(os.path.join(DATA, "emb", "pilot"), exist_ok=True)
    with open(os.path.join(DATA, "emb", "pilot", f"{args.model}{args.tag}.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print(json.dumps(report["text_mode"], indent=1))


def stage_all(args):
    manifest = load_manifest(args.manifest)
    out_dir = os.path.join(DATA, "emb", args.model + args.tag)
    os.makedirs(out_dir, exist_ok=True)
    vec_path, idx_path = os.path.join(out_dir, "vectors.npy"), os.path.join(out_dir, "index.jsonl")
    cached = {}
    if os.path.exists(idx_path):
        old_vec = np.load(vec_path)
        with open(idx_path) as fh:
            for j, line in enumerate(fh):
                r = json.loads(line)
                if r.get("done") and not r["note"].startswith("input failed"):  # failures are retried
                    if r.get("text_mode") not in (None, args.text_mode):
                        sys.exit(f"cache was built with text_mode {r['text_mode']}, asked for {args.text_mode}")
                    cached[r["path"]] = (old_vec[j], r)
    todo = [r for r in manifest if r["path"] not in cached]
    print(f"{len(manifest)} files, {len(cached)} cached, {len(todo)} to embed", file=sys.stderr)
    new = {}

    def write_cache():
        """Whole manifest in order; rows not embedded yet are written as pending (zero vector,
        done false), so a rerun picks them up."""
        V = np.zeros((len(manifest), MODELS[args.model].get("dim", 2048)), np.float32)
        with open(idx_path + ".tmp", "w") as fh:
            for j, r in enumerate(manifest):
                v, x = cached.get(r["path"]) or new.get(r["path"]) or (
                    None, {"path": r["path"], "modality": r["modality"], "ok": False, "done": False,
                           "note": "pending"})
                if v is not None:
                    V[j] = v
                fh.write(json.dumps(x) + "\n")
        np.save(vec_path + ".tmp.npy", V)
        os.replace(vec_path + ".tmp.npy", vec_path)
        os.replace(idx_path + ".tmp", idx_path)

    if todo:
        import torch
        enc = Encoder(args.model)
        # since session 5 the cache is written after every --checkpoint files, so a crash late
        # in the pass loses at most one chunk
        for c0 in range(0, len(todo), args.checkpoint):
            chunk = todo[c0:c0 + args.checkpoint]
            vecs, info = embed_rows(enc, chunk, [args.text_mode], prep_workers=args.prep_workers)
            for r, v, x in zip(chunk, vecs[args.text_mode], info):
                x.update({"done": True, "text_mode": args.text_mode, "model": MODELS[args.model]["id"],
                          "revision": MODELS[args.model]["revision"], "dtype": enc.dtype_name(),
                          "gpu": torch.cuda.get_device_name(0)})
                new[r["path"]] = (v, x)
            write_cache()
            print(f"checkpoint: {c0 + len(chunk)}/{len(todo)} embedded", file=sys.stderr, flush=True)
    else:
        write_cache()
    rows = [json.loads(l) for l in open(idx_path)]
    print(json.dumps({"files": len(rows), "ok": sum(r["ok"] for r in rows),
                      "skipped": Counter(r["note"] for r in rows if not r["ok"]),
                      "ok_by_modality": Counter(r["modality"] for r in rows if r["ok"])}, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("pilot")
    p.add_argument("--model", choices=sorted(MODELS), required=True)
    p.add_argument("--n-dirs", type=int, default=20)
    p.add_argument("--seed", type=int, default=20260929)
    p.add_argument("--manifest", default="data/manifest.jsonl", help="repo-relative")
    p.add_argument("--dirs", default="data/dirs.jsonl", help="repo-relative")
    p.add_argument("--tag", default="", help="suffix of the report file, e.g. _s11")
    p.add_argument("--calib", type=float, default=0.0,
                   help="draw the pilot directories from this calibration fraction only (0: all directories)")
    p.add_argument("--calib-seed", type=int, default=20261102)
    p = sub.add_parser("all")
    p.add_argument("--model", choices=sorted(MODELS), required=True)
    p.add_argument("--text-mode", choices=["query", "doc"], required=True)
    p.add_argument("--manifest", default="data/manifest.jsonl", help="repo-relative")
    p.add_argument("--tag", default="", help="suffix of the cache directory, e.g. _s3")
    p.add_argument("--checkpoint", type=int, default=1000, help="write the cache after every N files")
    p.add_argument("--prep-workers", type=int, default=8, help="threads that prepare inputs")
    args = ap.parse_args()
    {"pilot": stage_pilot, "all": stage_all}[args.stage](args)


if __name__ == "__main__":
    main()
