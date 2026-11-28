#!/usr/bin/env python3
"""Allow truthful WebApplication descriptions only on the four requested calculator pages.

No rating, review, aggregate score or rich-result eligibility is claimed.
"""
import json
import re
from pathlib import Path

ROOT = Path("public")
assert ROOT.is_dir(), "Generated public directory is missing"
pages = sorted(ROOT.rglob("index.html"))
assert pages, "No generated HTML pages found"
allowed = {
    "emi-calculator/index.html",
    "tasbih-counter/index.html",
    "years-to-days-calculator/index.html",
    "zakat-calculator/index.html",
}
checked = 0
found = set()
for path in pages:
    relative = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8")
    applications = []
    for match in re.finditer(r'<script\\b(?=[^>]*\\btype=["\\']application/ld\\+json["\\'])(.*?)>(.*?)</script>', raw, re.S | re.I):
        parsed = json.loads(match.group(2))
        nodes = parsed if isinstance(parsed, list) else parsed.get("@graph", [parsed]) if isinstance(parsed, dict) else []
        applications.extend(node for node in nodes if isinstance(node, dict) and node.get("@type") == "WebApplication")
        checked += 1
    if relative in allowed:
        assert len(applications) == 1, f"{relative} must contain exactly one WebApplication entity"
        app = applications[0]
        assert app.get("url", "").endswith("/" + relative.split("/")[0] + "/"), f"{relative} WebApplication URL mismatch"
        assert app.get("offers", {}).get("price") == "0", f"{relative} must describe the free calculator accurately"
        assert not any(key in app for key in ("aggregateRating", "review", "reviews", "ratingValue", "ratingCount")), (
            f"{relative} must not invent ratings or reviews"
        )
        found.add(relative)
    else:
        assert not applications, f"Unexpected WebApplication markup in {relative}"
assert checked, "No JSON-LD blocks were checked"
assert found == allowed, f"Missing priority WebApplication pages: {sorted(allowed - found)}"
for required in ("WebPage", "Organization", "BreadcrumbList"):
    assert any(f'"@type":"{required}"' in p.read_text(encoding="utf-8") for p in pages), (
        f"Required truthful {required} structured data disappeared"
    )
print(f"PASS: checked {len(pages)} generated pages and {checked} JSON-LD blocks; four priority WebApplication entities have no fabricated ratings")
