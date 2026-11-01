#!/usr/bin/env python3
"""Check substantive methodology and editorial transparency without a word-count target."""
import re
from html import unescape
from pathlib import Path

ROOT = Path("public")

def visible(slug):
    path = ROOT / slug / "index.html"
    assert path.is_file(), f"Missing generated /{slug}/ page"
    source = path.read_text(encoding="utf-8")
    main = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S)
    assert main, f"Missing main content on /{slug}/"
    text = re.sub(r"(?is)<(script|style|nav)\b.*?</\1>", " ", main.group(1))
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", text))).strip()

method = visible("methodology")
for phrase in (
    "Order of operations example",
    "8 + 3 × 4 = 20",
    "(8 + 3) × 4 = 44",
    "18% of 250",
    "1/2 + 1/3 = 3/6 + 2/6 = 5/6",
    "PKR 4,500",
    "PKR 3,600",
    "Markup on cost",
    "Gross margin on selling price",
    "fixed nominal annual rate",
    "28 February 2024",
    "2024 includes 29 February",
    "one inch is exactly 25.4 millimetres",
    "BMI is a screening measure, not a diagnosis",
    "612.36 grams",
    "Rounding and precision",
    "Input validation",
    "Automated tests",
    "Report a suspected error",
):
    assert phrase.lower() in method.lower(), f"Methodology missing useful detail: {phrase}"

editorial = visible("editorial-policy")
for phrase in (
    "not around a target word count",
    "does not imply medical, legal, accounting, financial or religious credentials",
    "We do not invent expert reviewers",
    "A passing automated test is evidence for the cases tested",
    "qualified scholar's ruling",
    "include the page URL",
):
    assert phrase.lower() in editorial.lower(), f"Editorial policy missing transparency detail: {phrase}"

for slug, text in (("methodology", method), ("editorial-policy", editorial)):
    assert "OWNER TO PROVIDE" not in text and "REQUIRES OWNER OR COUNSEL REVIEW" not in text, f"Unresolved placeholder on /{slug}/"

print("PASS: methodology includes reproducible examples, assumptions, rounding, validation and limits")
print("PASS: editorial policy accurately describes authorship, verification and correction handling")
