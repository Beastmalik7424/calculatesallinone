#!/usr/bin/env python3
"""Validate the homepage and eight scoped HTML files with the Nu HTML Checker."""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

FILES = [
    Path("public/index.html"),
    Path("public/ar/index.html"),
    Path("public/es/index.html"),
    Path("public/fr/index.html"),
    Path("public/about/index.html"),
    Path("public/contact/index.html"),
    Path("public/discount-calculator/index.html"),
    Path("public/editorial-policy/index.html"),
    Path("public/health/index.html"),
]
ENDPOINT = "https://validator.w3.org/nu/?out=json"
failed = False
for path in FILES:
    if not path.is_file():
        print(f"HTML VALIDATION FAIL {path}: file missing")
        failed = True
        continue
    request = urllib.request.Request(
        ENDPOINT,
        data=path.read_bytes(),
        headers={"Content-Type": "text/html; charset=utf-8", "User-Agent": "CalculateAllInOne-SEO-Validation/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"HTML VALIDATION ERROR {path}: validator request failed: {exc}")
        failed = True
        continue
    messages = result.get("messages", [])
    errors = [m for m in messages if m.get("type") in ("error", "fatal")]
    warnings = [m for m in messages if m.get("type") == "info" and m.get("subType") == "warning"]
    if errors:
        print(f"HTML VALIDATION FAIL {path}: {len(errors)} errors, {len(warnings)} warnings")
        for item in errors:
            line = item.get("lastLine", item.get("firstLine", "?"))
            col = item.get("lastColumn", item.get("firstColumn", "?"))
            print(f"  line {line}, col {col}: {item.get('message', 'Unspecified HTML error')}")
        failed = True
    else:
        print(f"HTML VALIDATION PASS {path}: 0 errors, {len(warnings)} warnings")
if failed:
    print("Nu HTML Checker: FAIL")
    sys.exit(1)
print("Nu HTML Checker: PASS (9 files, zero errors)")
