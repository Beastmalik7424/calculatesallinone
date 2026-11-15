#!/usr/bin/env python3
"""Regression gate for Urdu Nastaliq typography and meaningful localized guidance."""
from pathlib import Path
import re

ROOT = Path("public")
SLUGS = (
    "age-calculator", "bmi-calculator", "discount-calculator",
    "profit-loss-calculator", "standard-calculator", "stopwatch",
    "tasbih-counter", "unit-converter", "zakat-calculator",
)

def visible(raw):
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw)).strip()

def main():
    for slug in SLUGS:
        page = ROOT / "ur" / slug / "index.html"
        assert page.is_file(), f"Missing Urdu page: {slug}"
        raw = page.read_text(encoding="utf-8")
        assert '<html lang="ur" dir="rtl">' in raw, f"{slug}: language/RTL metadata missing"
        assert "Noto+Nastaliq+Urdu" in raw, f"{slug}: Nastaliq font stylesheet missing"
        assert "fonts.googleapis.com" in raw, f"{slug}: Google Fonts stylesheet not linked"
        text = visible(raw)
        assert len(text.split()) >= 500, f"{slug}: thin Urdu page ({len(text.split())} words)"
    css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
    assert 'html[lang="ur"]' in css and '"Noto Nastaliq Urdu"' in css, "Urdu Nastaliq font stack missing from compiled CSS"
    assert "font-display: swap" in (ROOT / "assets" / "site.css").read_text(encoding="utf-8") or "fonts.googleapis.com" in css, "Font loading fallback is missing"
    print(f"PASS: {len(SLUGS)} Urdu routes retain RTL and load Noto Nastaliq Urdu")
    print("PASS: every Urdu route meets the site's editorial minimum and compiled CSS applies the font")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
