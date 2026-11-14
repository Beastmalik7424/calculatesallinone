#!/usr/bin/env python3
"""Site-side AdSense policy checks for calculateallinone. Checks headings, exact
phrases and date format. Does not check word counts (see tests/content-gates.py)."""
import re
import html
import sys
from pathlib import Path

ROOT = Path("public")
TOOLS_WITH_EXAMPLE = ["stopwatch", "tasbih-counter", "query-calculator", "ratio-calculator"]
AFFILIATE_PHRASE = "Advertising is not enabled on the site at present"
ERRORS = []


def page_text(path):
    raw = (ROOT / path / "index.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()


def has_heading(path, name):
    raw = (ROOT / path / "index.html").read_text(encoding="utf-8")
    return re.search(r"<h[1-6][^>]*>\s*" + re.escape(name) + r"\s*</h[1-6]>", raw) is not None


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


all_html = "".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("index.html"))
check("Marketplace guide" not in all_html, "built pages still mention 'Marketplace guide'")
check('href="/marketplaces/"' not in all_html, "a link to /marketplaces/ still exists")

check("malikadeelbhatti@gmail.com" in page_text("contact"), "/contact/ does not show the contact email")
check(AFFILIATE_PHRASE in page_text("affiliate-disclosure"),
      "/affiliate-disclosure/ must contain the exact phrase: " + AFFILIATE_PHRASE)

for slug in TOOLS_WITH_EXAMPLE:
    for name in ("Worked example", "Method", "Limits"):
        check(has_heading(slug, name), f"/{slug}/ has no heading exactly '{name}'")

for p in ROOT.rglob("index.html"):
    m = re.search(r"Last updated:\s*(\d{4}-\d{2}-\d{2})(?=\s|<)", p.read_text(encoding="utf-8"))
    if m:
        check(re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1)) is not None,
              f"{p}: 'Last updated' is not YYYY-MM-DD")

for e in ERRORS:
    print("FAIL:", e)
print(f"{len(ERRORS)} failing checks")
sys.exit(1 if ERRORS else 0)
