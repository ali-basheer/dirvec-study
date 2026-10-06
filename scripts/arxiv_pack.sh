#!/usr/bin/env bash
# Build the arXiv upload package from paper/main.tex.
#   bash scripts/arxiv_pack.sh [outdir]
# 1. builds the paper with its bibliography (latexmk, bibtex) in a scratch copy,
# 2. stages main.tex, the generated main.bbl and the six figure PDFs,
# 3. compiles the staged files alone, with no .bib and no .bst, as arXiv would,
# 4. checks the source for em and en dashes and for "--", and writes the tarball.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
out=${1:-$repo/build/arxiv}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# 1. full build (the .bib path in main.tex is ../reports/citations_verified.bib)
mkdir -p "$work/full/paper" "$work/full/reports"
cp "$repo/paper/main.tex" "$repo/paper/plainnat-nonote.bst" "$work/full/paper/"
cp -r "$repo/paper/figures" "$work/full/paper/"
cp "$repo/reports/citations_verified.bib" "$work/full/reports/"
(cd "$work/full/paper" && latexmk -pdf -bibtex -interaction=nonstopmode main.tex > build.log 2>&1)

# 2. stage what arXiv needs
stage="$work/stage"
mkdir -p "$stage/figures"
cp "$work/full/paper/main.tex" "$work/full/paper/main.bbl" "$stage/"
cp "$repo"/paper/figures/fig_*.pdf "$stage/figures/"

# 3. compile the staged files alone (no bibtex: arXiv uses main.bbl when it is there)
mkdir -p "$work/test"
cp -r "$stage/." "$work/test/"
(cd "$work/test" && pdflatex -interaction=nonstopmode main.tex > /dev/null \
  && pdflatex -interaction=nonstopmode main.tex > /dev/null \
  && pdflatex -interaction=nonstopmode main.tex > /dev/null)
if grep -E "^!|undefined|Citation .* undefined|Reference .* undefined" "$work/test/main.log"; then
  echo "staged build has errors or undefined references" >&2; exit 1
fi
cmp <(pdftotext "$work/full/paper/main.pdf" - ) <(pdftotext "$work/test/main.pdf" - ) \
  || { echo "staged PDF text differs from the full build" >&2; exit 1; }

# 4. dash check on the source (U+2014, U+2013, and "--" outside comments)
if LC_ALL=C grep -naP '\xe2\x80[\x93\x94]' "$stage/main.tex"; then echo "em or en dash in main.tex" >&2; exit 1; fi
if grep -nv '^\s*%' "$stage/main.tex" | grep -n -- '--'; then echo '"--" in main.tex' >&2; exit 1; fi

mkdir -p "$out"
cp "$work/test/main.pdf" "$out/dirvec_arxiv.pdf"
tar -C "$stage" -czf "$out/dirvec_arxiv_source.tar.gz" main.tex main.bbl figures
echo "pages: $(pdfinfo "$out/dirvec_arxiv.pdf" | awk '/^Pages/{print $2}')"
tar -tzvf "$out/dirvec_arxiv_source.tar.gz"
