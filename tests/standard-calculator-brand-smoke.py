#!/usr/bin/env python3
"""Guard the standard calculator's visible and search-facing brand identity."""
import re
from pathlib import Path

page = Path("public/standard-calculator/index.html")
assert page.is_file(), "Generated standard calculator page is missing"
source = page.read_text(encoding="utf-8")
main = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S)
assert main, "Standard calculator main content is missing"
assert "CalculateAllInOne" not in main.group(1), "Legacy CalculateAllInOne brand remains in visible page copy"
assert 'property="og:site_name" content="CalculatesAll"' in source, "Open Graph site name must match CalculatesAll"
assert re.search(r"<title>[^<]+\| CalculatesAll</title>", source), "Page title must use the CalculatesAll brand"
assert 'name="twitter:title" content="Standard and Scientific Calculator | CalculatesAll"' in source, "Twitter title must match the page title"
print("PASS: standard calculator visible copy and search-facing brand identity are consistent")
