#!/usr/bin/env python3
"""Verify useful, checkable examples on existing calculator pages.

This deliberately checks examples and transparent assumptions, not a minimum
word count. Google does not prescribe a preferred page length.
"""
import html
import json
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
        "For exact calendar dates, this calculator counts whole calendar days between anniversaries.",
        "29 10,585 10,592.25 10,592.0325",
        "6 2,190 2,191.5 2,191.455",
        "15 5,475 5,478.75 5,478.6375",
        "25 9,125 9,131.25 9,131.0625",
        "29 10,585 10,592.25 10,592.0325",
        "30 10,950 10,957.5 10,957.275",
        "1,009 days is 2.76438356 years using a 365-day year, 2.76249144 years using the 365.25-day Julian average, or 2.76254817 years",
        "365.25-day Julian average",
        "1,068 2.9260 2.9240 2.9241",
        "1,188 3.2548 3.2526 3.2526",
        "1,297 3.5534 3.5510 3.5511",
        "2,600 7.1233 7.1184 7.1186",
        "How many years and months are in 1,188 days?",
        "3 years, 3 average months and 0.96 days",
        "1.5 547.5 547.875 547.86375",
        "Worked reference: days to years",
        "724 1.9836 1.9822 1.9822",
        "1,145 3.1370 3.1348 3.1349",
        "1,476 4.0438 4.0411 4.0412",
        "2,436 6.6740 6.6694 6.6695",
        "7,200 19.7260 19.7125 19.7129",
        "27,375 75.0000 74.9487 74.9502",
        "28,000 76.7123 76.6598 76.6614",
        "42,069 115.2575 115.1786 115.1810",
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
    contact_path = ROOT / "contact" / "index.html"
    if not contact_path.is_file():
        failures.append("/contact/ was not generated")
    else:
        contact_html = contact_path.read_text(encoding="utf-8")
        main_match = re.search(r"<main\b[^>]*>(.*?)</main>", contact_html, re.S | re.I)
        contact_main = main_match.group(1) if main_match else ""
        contact_main = re.sub(r"(?is)<(script|style|nav)\b.*?</\1>", " ", contact_main)
        contact_main = re.sub(r"<[^>]+>", " ", contact_main)
        contact_text = re.sub(r"\s+", " ", html.unescape(contact_main)).strip()
        for phrase in [
            "Contact CalculatesAll by email",
            "calculator corrections",
            "exact input values and units",
            "displayed result, expected result",
            "Do not include passwords",
            "Calculation methodology",
            "Editorial policy",
            "Privacy policy",
            "How do I report a calculator error?",
            "What information should I include?",
            "How long does a reply take?",
        ]:
            if phrase not in contact_text:
                failures.append("/contact/ is missing required contact guidance: " + phrase)
        if len(contact_text.split()) < 180:
            failures.append("/contact/ has fewer than 180 visible words")
        if contact_text.lower().count("how do i report a calculator error?") != 1:
            failures.append("/contact/ does not expose the expected visible FAQ question")
        faq_scripts = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            contact_html,
            re.S,
        )
        faq_nodes = []
        for script in faq_scripts:
            try:
                node = json.loads(script)
            except json.JSONDecodeError:
                failures.append("/contact/ contains invalid JSON-LD")
                continue
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                faq_nodes.append(node)
        if len(faq_nodes) != 1:
            failures.append("/contact/ must contain exactly one FAQPage node")
        elif len(faq_nodes[0].get("mainEntity", [])) != 3:
            failures.append("/contact/ FAQPage must match exactly three visible questions")
        if contact_main.count("<details") != 3:
            failures.append("/contact/ must display exactly three FAQ details")
        allowed_urls = {
            line.strip().rstrip("/") + "/"
            for line in Path("urls.txt").read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("https://calculateallinone.vercel.app/")
        }
        internal_links = re.findall(r'href="(/[^"#?]*)', contact_main)
        for link in internal_links:
            canonical_link = "https://calculateallinone.vercel.app" + link
            if not (canonical_link.rstrip("/") + "/") in allowed_urls:
                failures.append("/contact/ contains an internal link absent from urls.txt: " + link)
        for unsupported_claim in [
            "we do not sell your personal information",
            "we will reply within",
            "usually within",
            "medically reviewed",
            "independently reviewed",
        ]:
            if unsupported_claim in contact_text.lower():
                failures.append("/contact/ contains an unsupported claim: " + unsupported_claim)
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("PASS: query, stopwatch, ratio and years-to-days worked examples are present and checkable")
    print("PASS: no unresolved legal placeholders in the checked calculator pages")
    return 0

if __name__ == "__main__":
    sys.exit(main())
