#!/usr/bin/env python3
"""Require exactly one non-empty H1 on every generated HTML page, including noindex locale pages."""
import html
import re
import sys
from pathlib import Path

ROOT = Path("public")
failures = []
pages = sorted(ROOT.rglob("index.html"))

if not pages:
    failures.append("No generated index.html pages found under public/")

for page in pages:
    source = page.read_text(encoding="utf-8")
    visible_markup = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", source)
    headings = re.findall(r"(?is)<h1\b[^>]*>(.*?)</h1>", visible_markup)
    relative = page.parent.relative_to(ROOT).as_posix()
    route = "/" if relative == "." else "/" + relative.strip("/") + "/"
    if len(headings) != 1:
        failures.append(f"{route}: expected exactly one H1, found {len(headings)}")
        continue
    heading_text = html.unescape(re.sub(r"(?is)<[^>]+>", " ", headings[0]))
    heading_text = " ".join(heading_text.split())
    if not heading_text:
        failures.append(f"{route}: H1 is empty")
    if len(heading_text) > 180:
        failures.append(f"{route}: H1 is excessively long ({len(heading_text)} characters)")

if failures:
    print("ALL-GENERATED-PAGES H1 AUDIT: FAIL")
    for failure in failures:
        print("FAIL:", failure)
    sys.exit(1)

print("ALL-GENERATED-PAGES H1 AUDIT: PASS")
print("Generated HTML pages checked:", len(pages))
print("Exactly one non-empty H1 per indexable and noindex page: PASS")
