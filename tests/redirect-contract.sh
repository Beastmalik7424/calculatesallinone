#!/usr/bin/env bash
set -euo pipefail
SITE_URL="${1:-${SITE_URL:-}}"
if [[ -z "$SITE_URL" ]]; then echo "Usage: SITE_URL=https://deployment-url bash tests/redirect-contract.sh"; exit 2; fi
SITE_URL="${SITE_URL%/}"
for path in contact editorial-policy methodology privacy terms; do
  headers="$(mktemp)"
  code="$(curl --silent --show-error --max-time 25 --max-redirs 0 -D "$headers" -o /dev/null -w '%{http_code}' "$SITE_URL/$path")"
  location="$(awk 'tolower($1) == "location:" { sub(/\r$/, "", $2); print $2 }' "$headers" | tail -n 1)"
  rm -f "$headers"
  if [[ "$code" != "301" ]]; then echo "FAIL /$path: expected HTTP 301, got $code"; exit 1; fi
  resolved="$(python3 -c 'import sys; from urllib.parse import urljoin; print(urljoin(sys.argv[1], sys.argv[2]))' "$SITE_URL/$path" "$location")"
  expected="$SITE_URL/$path/"
  if [[ "$resolved" != "$expected" ]]; then echo "FAIL /$path: redirect target $resolved, expected $expected"; exit 1; fi
  final_code="$(curl --silent --show-error --max-time 25 --location --output /dev/null --write-out '%{http_code}' "$SITE_URL/$path")"
  if [[ "$final_code" != "200" ]]; then echo "FAIL /$path: final destination returned $final_code"; exit 1; fi
  echo "PASS /$path -> 301 -> $expected (final $final_code)"
done
