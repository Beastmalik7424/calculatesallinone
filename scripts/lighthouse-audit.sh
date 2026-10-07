#!/usr/bin/env bash
# Run after the site is live. Needs Node 22 and Google Chrome installed on your machine.
# Usage: bash scripts/lighthouse-audit.sh https://calculateallinone.vercel.app
set -euo pipefail
SITE="${1:-https://calculateallinone.vercel.app}"
OUT="lighthouse-reports"
mkdir -p "$OUT"
PAGES=("/" "/zakat-calculator/" "/bmi-calculator/" "/profit-loss-calculator/" "/ur/" "/ur/zakat-calculator/" "/money/" "/about/")
for p in "${PAGES[@]}"; do
  name=$(echo "$p" | tr '/' '_')
  npx --yes lighthouse "$SITE$p" --only-categories=performance,accessibility,best-practices,seo \
    --form-factor=mobile --screenEmulation.mobile --quiet \
    --output=html --output=json --output-path="$OUT/report$name"
  echo "done $p"
done
echo "Reports saved in $OUT/. Target: every category 90 or higher, LCP under 2.5s, CLS under 0.1."
