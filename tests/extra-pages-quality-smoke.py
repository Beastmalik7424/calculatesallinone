from pathlib import Path
import json
import re
from html import unescape

ROOT = Path("public")
CASES = {
    "percentage-calculator": {
        "category": "/math/",
        "phrases": ["X% of a number", "X is what percent of Y", "Percentage increase or decrease", "25% of 200", "30 out of 120", "starting value"],
    },
    "fraction-calculator": {
        "category": "/math/",
        "phrases": ["1/2 + 1/3", "5/6", "common denominator", "improper fractions", "zero denominator"],
    },
    "compound-interest-calculator": {
        "category": "/money/",
        "phrases": ["1,102.50", "1,000", "10%", "nominal annual rate", "fees", "inflation"],
    },
    "date-calculator": {
        "category": "/time/",
        "phrases": ["28 February 2024", "29 February", "elapsed Gregorian calendar days", "business days", "inclusive"],
    },
}

for slug, spec in CASES.items():
    path = ROOT / slug / "index.html"
    assert path.is_file(), f"Missing /{slug}/"
    source = path.read_text(encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", source, re.S)
    description = re.search(r'<meta name="description" content="([^"]*)"', source)
    canonical = f'<link rel="canonical" href="https://calculateallinone.vercel.app/{slug}/">'
    assert title and 25 <= len(unescape(title.group(1))) <= 60, f"Invalid title: {slug}"
    assert description and 70 <= len(unescape(description.group(1))) <= 160, f"Invalid description: {slug}"
    assert canonical in source, f"Canonical mismatch: {slug}"
    assert '<meta name="robots" content="index, follow">' in source, f"Unexpected indexability: {slug}"
    assert f'href="{spec["category"]}"' in source, f"Missing category breadcrumb: {slug}"
    assert 'id="extra-calculator-form"' in source and ">Calculate</button>" in source, f"Missing calculator form: {slug}"
    assert source.count("<details") >= 4, f"Expected four useful FAQs: {slug}"
    assert source.count("<h2") >= 7, f"Missing explanatory sections: {slug}"
    for phrase in spec["phrases"]:
        assert phrase.lower() in unescape(source).lower(), f"Missing page-specific content {phrase!r}: {slug}"
    scripts = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', source, re.S)
    schemas = []
    for item in scripts:
        schemas.append(json.loads(item))
    types = {schema.get("@type") for schema in schemas}
    assert "WebApplication" in types, f"Missing WebApplication schema: {slug}"
    assert "BreadcrumbList" in types, f"Missing breadcrumb schema: {slug}"

pct = (ROOT / "percentage-calculator" / "index.html").read_text(encoding="utf-8")
for value in ('value="of"', 'value="whatpercent"', 'value="change"', 'id="pct-mode"'):
    assert value in pct, f"Missing percentage mode control: {value}"

print("Extra calculator page content, metadata, breadcrumb, schema and mode quality checks: PASS")
