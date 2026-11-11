#!/usr/bin/env python3
"""Verify useful, checkable examples on existing calculator pages.

This deliberately checks examples and transparent assumptions, not a minimum
word count. Google does not prescribe a preferred page length.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path("public")
CASES = {
    "query-calculator": [
        "Question: 2 weeks in hours.",
        "2 x 7 = 14 days.",
        "14 x 24 = 336 hours.",
        "Question: 3 days to minutes.",
        "3 x 24 = 72 hours.",
        "72 x 60 = 4,320 minutes.",
        "Divide the answer by each factor used in the question, in reverse order.",
        "115 months in years and days",
        "115 months = 9 years and 7 months",
        "Pakistan independence date",
        "14 August 1947",
        "exact calendar days require a start date",
    ],
    "stopwatch": [
        "A lap time of 83 seconds equals 1 minute and 23 seconds.",
        "A total of 3,725 seconds equals 1 hour, 2 minutes and 5 seconds.",
    ],
    "calorie-calculator": [
        "resting energy expenditure (REE)",
        "1,648.75 kcal/day REE",
        "1,978.5 kcal/day",
        "498 healthy adults aged 19–78",
        "activity multipliers are consumer estimates",
        "Pregnancy and breastfeeding estimates are available only for ages 19+",
        "has not been medically reviewed",
        "REE is not a universal minimum safe calorie intake",
        "does not implement the NIDDK dynamic weight-change model",
    ],
    "ratio-calculator": [
        "10:15",
        "2:3",
        "1.5:2.5",
        "A:B = C:D",
        "cross multiplication",
        "up to six decimal places",
    ],
    "years-to-days-calculator": [
        "Choose the year method",
        "For 13 years, the simple result is 4,745 days, the Julian-average result is 4,748.25 days, and the Gregorian-average result is 4,748.1525 days.",
        "For 29 years, the simple conversion is 29 x 365 = 10,585 days.",
        "1,009 days, the results are 2.76438356 years",
        "For exact calendar dates, this calculator counts whole calendar days between anniversaries.",
        "Inputs range from 0 to 1,000,000",
        "3 years, 3 months and 0.96 days",
    ],
}

def visible_text(path):
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"(?is)<(script|style|nav)\b.*?</\1>", " ", source)
    source = re.sub(r"<[^>]+>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(source)).strip()

def main():
    failures = []
    for slug, expected_phrases in CASES.items():
        path = ROOT / slug / "index.html"
        if not path.is_file():
            failures.append(f"/{slug}/ was not generated")
            continue
        text = visible_text(path)
        for phrase in expected_phrases:
            if phrase not in text:
                failures.append(f"/{slug}/ is missing worked example: {phrase}")
        if "OWNER TO PROVIDE" in text or "REQUIRES OWNER OR COUNSEL REVIEW" in text:
            failures.append(f"/{slug}/ contains an unresolved legal placeholder")
    home_path = ROOT / "index.html"
    if not home_path.is_file():
        failures.append("Homepage / was not generated")
    else:
        home_text = visible_text(home_path)
        for phrase in [
            "Free Online Calculators",
            "Free online calculators for health, money, business, dates, maths and everyday tasks.",
            "Browse all free calculators",
        ]:
            if phrase not in home_text:
                failures.append("Homepage is missing the verified answer-first summary: " + phrase)
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("PASS: query, stopwatch, ratio and years-to-days worked examples are present and checkable")
    print("PASS: no unresolved legal placeholders in the checked calculator pages")
    return 0

if __name__ == "__main__":
    sys.exit(main())
