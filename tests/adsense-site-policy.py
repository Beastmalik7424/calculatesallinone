#!/usr/bin/env python3
"""Site-side AdSense policy checks for calculateallinone. Checks headings, exact
phrases and date format. Does not check word counts (see tests/content-gates.py)."""
import re
import html
import sys
from pathlib import Path

ROOT = Path("public")
TOOLS_WITH_EXAMPLE = ["stopwatch", "query-calculator", "ratio-calculator"]
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


privacy_text = page_text("privacy")
af¶»§q«^