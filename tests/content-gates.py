#!/usr/bin/env python3
"""Content gates for the AdSense low-value-content review.

Usage: python3 tests/content-gates.py [--strict]
Exits 1 with --strict when any check fails.
"""
import argparse
import html
import os
import re
import sys

OUT = "public"
INDEXABLE = "indexable.txt"
WORD_PAGES = ["query-calculator", "years-to-days-calculator"]
MIN_WORDS = 500
EXAMPLE_PAGES = ["stopwatch", "tasbih-counter", "bmi-calculator", "query-calculator"]
EXAMPLE_RE = re.compile(r"example[\s\S]{0,400}?\d[\d,.]*\s*[x\u00d7+/=\-]\s*\d", re.I)
FORBIDDEN = ["expert reviewed", "medically reviewed"]


def visible_text(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    src = re.sub(r"(?is)<(script|style|nav)\b.*?</\1>", " ", src)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(src)


def indexable_urls():
    with open(INDEXABLE, encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip().startswith("/")]


def built_page(url):
    return os.path.join(OUT, url.strip("/"), "index.html")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    failures = []

    for slug in WORD_PAGES:
        path = built_page(f"/{slug}/")
        words = len(visible_text(path).split()) if os.path.exists(path) else 0
        if words < MIN_WORDS:
            failures.append(f"(a) /{slug}/ has {words} visible words, need {MIN_WORDS}")

    for slug in EXAMPLE_PAGES:
        path = built_page(f"/{slug}/")
        text = visible_text(path) if os.path.exists(path) else ""
        if not EXAMPLE_RE.search(text):
            failures.append(f"(b) /{slug}/ has no worked example with a numeric calculation")

    for url in indexable_urls():
        path = built_page(url)
        if not os.path.exists(path):
            failures.append(f"(c) {url} is in indexable.txt but was not built")
            continue
        low = visible_text(path).lower()
        for phrase in FORBIDDEN:
            if phrase in low:
                failures.append(f"(c) {url} contains '{phrase}'")

    for line in failures:
        print("FAIL", line)
    print(f"{len(failures)} failure(s)")
    return 1 if (failures and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
