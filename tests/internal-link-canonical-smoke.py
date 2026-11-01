#!/usr/bin/env python3
"""Check that internal HTML links point directly to trailing-slash canonical routes."""
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path("public")

def main():
    failures = []
    pages = sorted(ROOT.rglob("index.html"))
    for page in pages:
        source = page.read_text(encoding="utf-8")
        for href in re.findall(r'''href=["']([^"']+)["']''', source, re.I):
            if not href.startswith("/") or href.startswith("//"):
                continue
            path = urlsplit(href).path
            if path in ("", "/") or path.startswith("/assets/"):
                continue
            # Static files are not page routes and do not use trailing slashes.
            if Path(path).suffix:
                continue
            if not path.endswith("/"):
                failures.append(f"{page}: {href} should point directly to a trailing-slash route")
                continue
            target = ROOT / path.strip("/") / "index.html"
            if not target.is_file():
                failures.append(f"{page}: {href} has no generated page target")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print(f"PASS: {len(pages)} generated pages use direct trailing-slash internal links")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
