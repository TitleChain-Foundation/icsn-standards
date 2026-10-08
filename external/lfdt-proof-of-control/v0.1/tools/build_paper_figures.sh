#!/usr/bin/env bash
# Rebuild every figure the paper includes, from the repository's SVGs.
#
# The PDFs are gitignored (they are build output), so run this once after
# cloning, and again whenever a diagram or a benchmark result changes.
#
#   ./tools/build_paper_figures.sh && (cd paper && tectonic -Z shell-escape main.tex)
#
# Requires rsvg-convert (brew install librsvg).

set -euo pipefail
cd "$(dirname "$0")/.."

command -v rsvg-convert >/dev/null || {
  echo "rsvg-convert not found: brew install librsvg" >&2; exit 1; }

# Regenerate the SVGs first so a stale figure cannot survive a data change.
python3 tools/generate_diagrams.py
python3 tools/generate_charts.py

FIGURES=(
  tier-ladder reference-architecture evidence-flow mapping-coverage roadmap
  chart-scaling chart-frontier chart-retention chart-anchor chart-batch
  chart-merkle
)

mkdir -p paper/figures

# The Society lockup comes from the brand kit and must never be redrawn.
# A copy, not a symlink; refreshed from the kit when the kit is present,
# with the committed paper/figures/aais-lockup.png standing otherwise.
BRAND_KIT_LOCKUP="../../comms/brand-kit/png/advanced-ai-society-logo-offwhite-large-2386px.png"
if [[ -f "$BRAND_KIT_LOCKUP" ]]; then
  cp "$BRAND_KIT_LOCKUP" paper/figures/aais-lockup.png
fi

for f in "${FIGURES[@]}"; do
  src="images/diagrams/${f}-light.svg"
  [[ -f "$src" ]] || { echo "missing $src" >&2; exit 1; }
  rsvg-convert -f pdf "$src" -o "paper/figures/${f}.pdf"
  printf '  %-28s -> paper/figures/%s.pdf\n' "$src" "$f"
done

echo "${#FIGURES[@]} figures built"
