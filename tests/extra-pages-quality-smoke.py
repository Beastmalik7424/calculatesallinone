from pathlib import Path
import json
import re
from html import unescape
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import extra_calculator_pages as page_content

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
    "percentage-difference-calculator": {
        "category": "/math/",
        "phrases": [
            "Percentage difference compares two non-negative values",
            "percentage difference = |A - B|",
            "For 40 and 60",
            "For 80 and 100",
            "Percentage difference and percentage change answer different questions",
            "returns 200%",
            "both values are zero",
            "same unit and measurement basis",
        ],
    },
    "ratio-calculator": {
        "category": "/math/",
        "phrases": [
            "10:15",
            "2:3",
            "1.5:2.5",
            "A:B = C:D",
            "cross multiplication",
            "up to six decimal places",
            "positive known values",
            "100:200:400",
            "1:2:4",
            "three-term ratio",
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
            "calendar breakdown",
            "month-end clamping",
            "4.14 weeks",
            "business days",
            "inclusive",
        ],
    },
}

for slug, headings_for_page in page_content.SECTION_HEADINGS.items():
    assert len(headings_for_page) == len(page_content.GUIDES[slug]), f"Section headings and guide paragraphs are out of sync: {slug}"

for slug, spec in CASES.items():
    path = ROOT / slug / "index.html"
    assert path.is_file(), f"Missing /{slug}/"
    source = path.read_text(encoding="utf-8")
    decoded = unescape(source)
    title = re.search(r"<title>(.*?)</title>", source, re.S)
    description = re.search(r'<meta name="description" content="([^"]*)"', source)
    canonical = f'<link rel="canonical" href="https://calculateallinone.vercel.app/{slug}/">'
    title_text = unescape(title.group(1)) if title else ""
    title_limit = 63 if slug == "date-calculator" else 60
    assert title and 25 <= len(title_text) <= title_limit, f"Invalid title: {slug}"
    if slug == "date-calculator":
        assert title_text == "Date Difference Calculator | Days Between Dates | CalculatesAll", "Date calculator title must preserve the exact requested search-intent wording"
        headings = [unescape(value) for value in re.findall(r"<h2[^>]*>(.*?)</h2>", source)]
        assert "Gregorian leap-year rule" in headings, "Date calculator must label its Gregorian leap-year explanation accurately"
        assert "Calendar-day counting limitations" in headings, "Date calculator limitations need a heading that matches the content"
        assert "Check the required counting rule" in headings, "Date calculator must explain that elapsed, inclusive and business-day rules differ"
        assert "Inclusive versus elapsed dates" not in headings, "Date calculator must not label business-day limitations as a counting-mode explanation"
        section_text = {
            unescape(heading): unescape(paragraph)
            for heading, paragraph in re.findall(
                r'<section class="mt-6"><h2[^>]*>(.*?)</h2><p[^>]*>(.*?)</p></section>',
                source,
                re.S,
            )
        }
        limitations = section_text["Calendar-day counting limitations"]
        assert "does not exclude weekends or public holidays" in limitations and "legal deadline rules" in limitations, "Date calculator must state its business-day and holiday limitations"
        counting_rule = section_text["Check the required counting rule"]
        assert "elapsed days, inclusive calendar days or business days" in counting_rule, "Date calculator must distinguish the three counting rules"
        signed_results = section_text["Date order and negative results"]
        assert "later end date produces a positive result" in signed_results, "Date calculator must explain positive signed results"
        assert "earlier end date produces a negative result" in signed_results, "Date calculator must explain negative signed results"
        assert "reversing the dates changes the sign" in signed_results.lower(), "Date calculator must explain how reversing dates affects the sign"
    assert description and 70 <= len(unescape(description.group(1))) <= 160, f"Invalid description: {slug}"
    assert canonical in source, f"Canonical mismatch: {slug}"
    assert '<meta name="robots" content="index, follow">' in source, f"Unexpected indexability: {slug}"
    assert f'href="{spec["category"]}"' in source, f"Missing category breadcrumb: {slug}"
    assert 'id="extra-calculator-form"' in source and ">Calculate</button>" in source, f"Missing calculator form: {slug}"
    assert "Maintained by" in source and "Muhammad Fayyaz Adeel" in source and 'href="/about/"' in source, f"Missing honest maintainer byline: {slug}"
    assert "representative results and invalid inputs are covered by automated tests" in source and "not an independent professional review" in source, f"Missing accurate verification disclosure: {slug}"
    if slug in ("fraction-calculator", "compound-interest-calculator", "ratio-calculator"):
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
    assert "WebApplication" not in types, f"Ineligible SoftwareApplication rich-result markup must be omitted: {slug}"
    assert "BreadcrumbList" in types, f"Missing breadcrumb schema: {slug}"
    expected_domain = {
        "percentage-calculator": "openstax.org",
        "percentage-difference-calculator": "mathsisfun.org",
        "ratio-calculator": "openstax.org",
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
    "/percentage-difference-calculator/",
    "/fraction-calculator/",
):
    assert f'href="{href}"' in about_html, f"Missing About-page link: {href}"

print("Extra calculator content, metadata, breadcrumb, schema, mode and About-page link checks: PASS")
