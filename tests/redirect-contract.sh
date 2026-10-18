#!/usr/bin/env bash
set -euo pipefail

# Vercel's existing trailingSlash=true contract uses HTTP 308. Accept 301 or
# 308 because both are permanent redirects. Do not change routing to force 301.
SITE_URL="${SITE_URL:-https://calculateallinone.vercel.app}"
for path in contact editorial-policy methodology privacy terms; do
  headers="$(mktemp)"
  code="$(curl --silent --show-error --max-time 25 --max-redirs 0 -D "$headers" -o /dev/null -w '%{http_code}' "$SITE_URL/$path")"
  location="$(awk 'tolower($1) == "location:" { sub(/\r$/, "", $2); print $2 }' "$headers" | tail -n 1)"
  rm -f "$headers"
  case "$code" in
    301|308) ;;
    *) echo "FAIL /$path: expected permanent redirect 301 or 308, got $code"; exit 1 ;;
  esac
  resolved="$(python3 -c 'import sys; from urllib.parse import urljoin; print(urljoin(sys.argv[1], sys.argv[2]))' "$SITE_URL/$path" "$location")"
  expected="$SITE_URL/$path/"
  if [ "$resolved" != "$expected" ]; then
    echo "FAIL /$path: redirect target '$resolved', expected '$expected'"
    exit 1
  fi
  final_code="$(curl --silent --show-error --max-time 25 --location --output /dev/null --write-out '%{http_code}' "$SITE_URL/$path")"
  if [ "$final_code" != "200" ]; then
    echo "FAIL /$path: final destination returned $final_code"
    exit 1
  fi
  echo "PASS /$path -> $code -> $expected (final $final_code)"
done
