#!/usr/bin/env python3
"""Verify useful structure, visible FAQs and relevant internal paths on extra calculators."""
import json
import re
from pathlib import Path

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
PAGES = {
    "percentage-calculator": {
        "hub": "math",
        "app": "UtilitiesApplication",
        "questions": [
            "What is 25% of 200?",
            "What percent is 30 of 120?",
            "How do I calculate a percentage increase?",
            "Why is a fall from 100 to 80 only 20% when a rise from 80 to 100 is 25%?",
        ],
        "related": ["discount-calculator", "profit-loss-calculator", "fraction-calculator"],
        "headings": ["Three percentage questions", "Discounts and tax", "Percentage increase and decrease"],
    },
    "fraction-calculator": {
        "hub": "math",
        "app": "UtilitiesApplication",
        "questions": [
            "What is 1/2 + 1/3?",
            "What is 1/2 minus 1/3?",
            "How do I divide fractions?",
            "Can I enter decimals?",
        ],
        "related": ["percentage-calculator", "standard-calculator"],
        "headings": ["Adding and subtracting fractions", "Multiplying and dividing fractions", "Improper fractions and zero"],
    },
    "compound-interest-calculator": {
        "hub": "money",
        "app": "FinanceApplication",
        "questions": [
            "How much is 1,000 at 12% compounded monthly for one year?",
            "What is the difference between simple and compound interest?",
            "What number should I enter for monthly compounding?",
            "Does this include monthly deposits?",
        ],
        "related": ["emi-calculator", "profit-loss-calculator"],
        "headings": ["Compound interest formula", "Worked example", "What the estimate leaves out"],
    },
    "date-calculator": {
        "hub": "time",
        "app": "UtilitiesApplication",
        "questions": [
            "How many days are there from 1 January to 31 December 2026?",
            "How many days are in 2024?",
            "How do I count days left until a future date?",
            "Does this count weekends and holidays?",
        ],
        "related": ["age-calculator", "years-to-days-calculator"],
        "headings": ["How the days are counted", "Leap years", "Dates without time zones"],
    },
}

def schemas_in(html):
    result = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        data = json.loads(raw)
        if isinstance(data, list):
            result.extend(data)
        elif isinstance(data, dict) and "@graph" in data:
            result.extend(data["@graph"])
        else:
            result.append(data)
    return result

def main():
    for slug, spec in PAGES.items():
        path = ROOT / slug / "index.html"
        assert path.is_file(), f"Missing generated page: /{slug}/"
        html = path.read_text(encoding="utf-8")
        assert '<nav aria-label="Breadcrumb"' in html, f"Missing visible breadcrumb: /{slug}/"
        assert f'href="/{spec["hub"]}/"' in html, f"Missing category hub path: /{slug}/"
        assert '<h2 class="text-xl font-semibold">Common questions</h2>' in html, f"Missing FAQ heading: /{slug}/"
        for heading in spec["headings"]:
            assert f">{heading}</h2>" in html, f"Missing section heading {heading!r}: /{slug}/"
        for question in spec["questions"]:
            assert f"<summary" in html and question in html, f"Missing visible FAQ: {question!r}"
        nodes = schemas_in(html)
        assert any(node.get("@type") == "WebApplication" and node.get("applicationCategory") == spec["app"] for node in nodes), f"Missing WebApplication schema: /{slug}/"
        crumbs = [node for node in nodes if node.get("@type") == "BreadcrumbList"]
        assert len(crumbs) == 1, f"Expected one BreadcrumbList: /{slug}/"
        items = crumbs[0].get("itemListElement", [])
        assert len(items) == 3, f"Breadcrumb depth mismatch: /{slug}/"
        assert items[0].get("item") == SITE + "/", f"Home breadcrumb mismatch: /{slug}/"
        assert items[1].get("item") == SITE + f'/{spec["hub"]}/', f"Hub breadcrumb mismatch: /{slug}/"
        assert items[2].get("item") == SITE + f'/{slug}/', f"Page breadcrumb mismatch: /{slug}/"
        faq = [node for node in nodes if node.get("@type") == "FAQPage"]
        assert len(faq) == 1, f"Expected one FAQPage schema: /{slug}/"
        faq_questions = [item.get("name") for item in faq[0].get("mainEntity", [])]
        assert faq_questions == spec["questions"], f"FAQ schema differs from visible questions: /{slug}/"
        related = html[html.find('aria-label="Related calculators"'):] if 'aria-label="Related calculators"' in html else ""
        for target in spec["related"]:
            assert f'href="/{target}/"' in related, f"Missing related link /{target}/ from /{slug}/"
        print(f"PASS: /{slug}/ structure, breadcrumbs, schema, FAQs and related links")
    print("PASS: all four extra calculator pages have complete semantic navigation and helpful FAQs")

if __name__ == "__main__":
    main()
