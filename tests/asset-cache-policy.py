#!/usr/bin/env python3
"""Verify immutable asset URLs are cached for at least one day without unsafe long caching."""
import json
import re
from pathlib import Path

config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
rules = [rule for rule in config.get("headers", []) if rule.get("source") == "/assets/(.*)"]
assert len(rules) == 1, "vercel.json must define exactly one static asset header rule"
headers = {item.get("key", "").lower(): item.get("value", "") for item in rules[0].get("headers", [])}
cache_control = headers.get("cache-control", "")
match = re.search(r"(?:^|,)\\s*max-age=(\\d+)(?:,|$)", cache_control, re.I)
assert match, "static assets must declare a numeric Cache-Control max-age"
assert int(match.group(1)) >= 86400, "static assets must be cacheable for at least one day"
assert "immutable" not in cache_control.lower(), "do not mark unversioned asset URLs immutable"
print("PASS: static assets have at least one-day browser caching without unsafe immutable caching")
