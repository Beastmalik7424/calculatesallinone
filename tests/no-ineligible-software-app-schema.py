#!/usr/bin/env python3
"""Regression guard for removing ineligible SoftwareApplication rich-result markup."""
import json
import re
from pathlib import Path

ROOT = Path("public")
assert ROOT.is_dir(), "Generated public directory is missing"
pages = sorted(ROOT.rglob("index.html"))
assert pages, "No generated HTML pages found"
checked = 0
for path in pages:
    raw = path.read_text(encoding="utf-8")
    for match in re.finditer(r'<script\b(?=[^>]*\btype=["\']application/ld\+json["\'])(.*?)>(.*?)</script>', raw, re.S | re.I):
        parsed = json.loads(match.group(2))
        nodes = parsed if isinstance(parsed, list) else parsed.get("@graph", [parsed]) if isinstance(parsed, dict) else []
        assert not any(node.get("@type") == "WebApplication" for node in nodes if isinstance(node, dict)), (
            f"Google-ineligible WebApplication markup remains in {path}"
        )
        checked += 1
assert checked, "No JSON-LD blocks were checked"
for required in ("WebPage", "Organization", "BreadcrumbList"):
    assert any(f'"@type":"{required}"' in p.read_text(encoding="utf-8") for p in pages), (
        f"Required truthful {required} structured data disappeared"
    )
print(f"PASS: checked {len(pages)} generated pages and {checked} JSON-LD blocks; retained core site schema")
