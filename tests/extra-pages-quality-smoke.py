from pathlib import Path
import json
import re
from html import unescape

ROOT = Path("public")
CASES = {
    "percentage-calculator": {
        "category": "/math/",
        "phrases": [
            "What is X% of a number?",
            "What percentage is one number of another?",
            "What is the percentage change?",
            "25% of 200",
            "30 out of 120",
            "starting value",
        ],
    },
    "fraction-calculator": {
        "category": "/math/",
        "phrases": [
            "1/2 + 1/3",
            "5/6",
            "common denominator",
            "improper fractions",
            "denominator cannot be zero",
        ],
    },
    "compound-interest-calculator": {
        "category": "/money/",
        "phrases": [
            "1,102.50",
            "1,000",
            "10%",
            "nominal annual rate",
            "fees",
            "inflation",
        ],
    },
    "date-calculator": {
        "category": "/time/",
        "phrases": [
            "28 February 2024",
            "29 February",
            "elapsed Gregorian calendar days",
            "business days",
            "inclusive",
        ],
    },
}

for slug, spec in CASES.items():
    path = ROOT / slug / "index.html"
    assert path.is_file(), f"Missing /{slug}/"
    source = path.read_text(encoding="utf-8")
    decoded = unescape(source)
    title = re.search(r"<title>(.*?)</title>", source, re.S)
    description = re.search(r'<meta name="description" content="([^"]*)"', source)
    canonical = f'<link rel="canonical" href="https://calculateallinone.vercel.app/{slug}/">'
    assert title and 25 <= len(unescape(title.group(1))) <= 60, f"Invalid title: {slug}"
    assert description and 70 <= len(unescape(description.group(1))) <= 160, f"Invalid description: {slug}"
    assert canonical in source, f"Canonical mismatch: {slug}"
    assert '<meta name="robots" content="index, follow">' in source, f"Unexpected indexability: {slug}"
    assert f'href="{spec["category"]}"' in source, f"Missing category breadcrumb: {slug}"
    assert 'id="extra-calculator-form"' in source and ">Calculate</button>" in source, f"Missing calculator form: {slug}"
    assert "Maintained by" in source and "Muhammad Fayyaz Adeel" in source and 'href="/about/"' in source, f"Missing honest maintainer byline: {slug}"
    assert "representative results and invalid inputs are covered by automated tests" in source and "not an independent professional review" in source, f"Missing accurate verification disclosure: {slug}"
    if slug in ("fraction-calculator", "compound-interest-calculator"):
        assert source.index('id="extra-calculator-form"') < source.index("Maintained by"), f"Compact form must precede trust notes: {slug}"
        assert "grid-cols-2" in source, f"Missing compact two-column form: {slug}"
    assert "Report this calculator" in source and 'href="/contact/"' in source, f"Missing calculator-specific feedback path: {slug}"
    assert source.count("<details") >= 4, f"Expected four useful FAQs: {slug}"
    assert source.count("<h2") >= 7, f"Missing explanatory sections: {slug}"
    for phrase in spec["phrases"]:
        assert phrase.lower() in decoded.lower(), f"Missing page-specific content {phrase!r}: {slug}"
    scripts = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', source, re.S)
    schemas = [json.loads(item) for item in scripts]
    types = {schema.get("@type") for schema in schemas}
    assert "WebApplication" in types, f"Missing WebApplication schema: {slug}"
    assert any(schema.get("@type") == "WebApplication" and schema.get("author", {}).get("@id") == "https://calculateallinone.vercel.app/#maintainer" and schema.get("publisher", {}).get("@id") == "https://calculateallinone.vercel.app/#organization" for schema in schemas), f"Missing truthful author/publisher entity links: {slug}"
    assert "BreadcrumbList" in types, f"Missing breadcrumb schema: {slug}"
    expected_domain = {
        "percentage-calculator": "openstax.org",
        "fraction-calculator": "openstax.org",
        "compound-interest-calculator": "investor.gov",
        "date-calculator": "aa.usno.navy.mil",
    }[slug]
    assert expected_domain in decoded, f"Missing authoritative reference link: {slug}"
    assert any(schema.get("@type") == "WebPage" and expected_domain in " ".join(schema.get("citation", [])) for schema in schemas), f"Missing structured source citations: {slug}"

percentage_html = (ROOT / "percentage-calculator" / "index.html").read_text(encoding="utf-8")
for value in (r'value=["\']of["\']', r'value=["\']share["\']', r'value=["\']change["\']', r'id=["\']percentage-mode["\']'):
    assert re.search(value, percentage_html), f"Missing percentage mode control: {value}"

about_html = (ROOT / "about" / "index.html").read_text(encoding="utf-8")
for href in (
    "/compound-interest-calculator/",
    "/date-calculator/",
    "/percentage-calculator/",
    "/fraction-calculator/",
):
    assert f'href="{href}"' in about_html, f"Missing About-page link: {href}"

print("Extra calculator content, metadata, breadcrumb, schema, mode and About-page link checks: PASS")
