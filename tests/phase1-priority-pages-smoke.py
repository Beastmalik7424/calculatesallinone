#!/usr/bin/env python3
"""Regression checks for the four Phase 1 priority calculator landing pages.

These checks exercise generated static HTML, not a duplicate implementation of
calculator formulas. They protect metadata, first-screen order, navigation,
language alternates and JSON-LD syntax.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"

CASES = {
    "tasbih-counter": {
        "title": "Tasbih Calculator Online | Dhikr Counter | CalculatesAll",
        "description": "Free Tasbih and Tasbeeh counter for dhikr and zikr. Count 33, 99 or custom targets, undo taps and keep progress on this device when storage allows.",
        "form": 'id="tasbih-app"',
        "category": "/worship/",
        "related": ["/stopwatch/", "/zakat-calculator/", "/ur/tasbih-counter/"],
        "faq_min": 6,
        "h1": "Free Online Tasbih Counter",
    },
    "profit-loss-calculator": {
        "title": "Profit and Loss Calculator | Markup and Margin",
        "description": "Calculate product profit, business operating profit, loss, markup and margin from revenue, costs and expenses. Includes clear formulas and PKR examples.",
        "form": 'id="pl-form"',
        "category": "/money/",
        "related": ["/discount-calculator/", "/percentage-calculator/", "/emi-calculator/", "/compound-interest-calculator/"],
        "faq_min": 5,
        "h1": "Profit and Loss Calculator",
    },
    "years-to-days-calculator": {
        "title": "Years to Days Calculator | How Many Days in X Years?",
        "description": "Convert years to days or days to years using 365, 365.25 or 365.2425-day methods. Use a start date for exact Gregorian calendar days.",
        "form": 'id="years-days-form"',
        "category": "/time/",
        "related": ["/date-calculator/", "/age-calculator/", "/query-calculator/", "/unit-converter/"],
        "faq_min": 5,
        "h1": "Years to Days Calculator",
    },
    "unit-converter": {
        "title": "Unit Converter | Weight, Length & Temperature",
        "description": "Convert kilograms, grams, pounds, ounces, metric and imperial lengths, and Celsius, Fahrenheit or Kelvin. See formulas, examples and input limits.",
        "form": 'id="conv-form"',
        "category": "/math/",
        "related": ["/bmi-calculator/", "/calorie-calculator/"],
        "faq_min": 5,
        "h1": "Unit Converter for Weight, Length and Temperature",
    },
}

def read_page(slug):
    path = ROOT / slug / "index.html"
    assert path.is_file(), f"Missing generated page: /{slug}/"
    return path.read_text(encoding="utf-8")

def jsonld_documents(source, slug):
    blocks = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        source, re.S | re.I
    )
    assert blocks, f"/{slug}/ has no JSON-LD"
    parsed = []
    for block in blocks:
        try:
            parsed.append(json.loads(block))
        except json.JSONDecodeError as error:
            raise AssertionError(f"Invalid JSON-LD on /{slug}/: {error}") from error
    return parsed

def check_english_page(slug, spec):
    source = read_page(slug)
    title_match = re.search(r"<title>(.*?)</title>", source, re.S | re.I)
    assert title_match and html.unescape(title_match.group(1)) == spec["title"], f"Search title mismatch: {slug}; expected={spec['title']!r}; actual={html.unescape(title_match.group(1)) if title_match else None!r}"
    description = re.search(r'<meta name="description" content="([^"]*)"', source)
    assert description and description.group(1) == spec["description"], f"Meta description mismatch: {slug}: got {description.group(1) if description else None!r}, expected {spec['description']!r}"
    assert f'<link rel="canonical" href="{SITE}/{slug}/">' in source, f"Canonical changed: {slug}"
    assert '<meta name="robots" content="index, follow">' in source, f"Unexpected robots directive: {slug}"
    assert source.count("<h1") == 1 and spec["h1"] in source, f"Expected one clear H1: {slug}"
    assert spec["category"] in source, f"Missing category navigation: {slug}"
    assert spec["form"] in source, f"Existing calculator UI missing: {slug}"

    main = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S | re.I)
    assert main, f"Missing main landmark: {slug}"
    body = main.group(1)
    h1_pos = body.find("<h1")
    form_pos = body.find(spec["form"])
    lead_match = re.search(r'<p class="[^"]*\bca-tool-lead\b[^"]*">', body)
    assert h1_pos >= 0 and lead_match, f"Missing first-screen heading/value proposition: {slug}"
    if slug == "unit-converter":
        assert h1_pos < form_pos < lead_match.start(), f"Existing calculator-first layout must remain unchanged: {slug}"
    else:
        assert h1_pos < lead_match.start() < form_pos, f"Lead must appear between H1 and calculator: {slug}"

    assert "Related calculators" in body, f"Missing related tools section: {slug}"
    for target in spec["related"]:
        link_source = source if target.startswith("/ur/") else body
        assert f'href="{target}"' in link_source, f"Missing relevant internal link {target} on {slug}"
        assert (ROOT / target.strip("/") / "index.html").is_file(), f"Broken generated target {target}"

    questions = re.findall(r"<summary\b[^>]*>(.*?)</summary>", body, re.S | re.I)
    assert len(questions) >= spec["faq_min"], f"Insufficient visible FAQs: {slug}"
    jsonld_documents(source, slug)

def check_urdu_bmi():
    slug = "ur/bmi-calculator"
    source = read_page(slug)
    title = "بالغ BMI کیلکولیٹر اردو میں | وزن اور قد | CalculatesAll"
    description = "بالغوں کا BMI اردو میں نکالیں۔ وزن kg/lb اور قد cm یا فٹ/انچ درج کریں، فارمولا اور WHO حدود سمجھیں۔ BMI اسکریننگ ہے، تشخیص نہیں۔"
    assert f"<title>{title}</title>" in source, "Urdu BMI title mismatch"
    meta = re.search(r'<meta name="description" content="([^"]*)"', source)
    assert meta and meta.group(1) == description, "Urdu BMI description mismatch"
    assert f'<link rel="canonical" href="{SITE}/ur/bmi-calculator/">' in source, "Urdu BMI canonical changed"
    assert '<meta name="robots" content="index, follow">' in source, "Urdu BMI must remain indexable"
    assert '<html lang="ur" dir="rtl">' in source, "Urdu language direction changed"
    main = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S | re.I)
    assert main, "Urdu BMI main landmark missing"
    body = main.group(1)
    assert body.find("<h1") < body.find("بالغوں کا BMI = وزن") < body.find('id="bmi-form"'), "Urdu BMI lead must precede the calculator"
    for target in ("/health/", "/bmi-calculator/", "/calorie-calculator/", "/ur/age-calculator/", "/ur/unit-converter/"):
        assert f'href="{target}"' in body, f"Urdu BMI missing relevant link: {target}"
        assert (ROOT / target.strip("/") / "index.html").is_file(), f"Broken Urdu BMI target: {target}"
    assert "Related calculators" in body or "متعلقہ کیلکولیٹر" in body, "Urdu BMI related tools section missing"
    assert "پاکستان میں BMI calculator" in body, "Urdu BMI page is missing the observed Pakistan BMI query wording"
    assert "Body Mass Index کا اردو مطلب جسمانی کمیت کا اشاریہ ہے" in body, "Urdu BMI page is missing the observed Urdu meaning query"
    assert len(re.findall(r"<summary\b", body, re.I)) >= 6, "Urdu BMI needs six visible FAQs"
    links = re.findall(r'<link\b[^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\']', source, re.I)
    assert {(lang, href) for lang, href in links} >= {
        ("en", SITE + "/bmi-calculator/"),
        ("ur", SITE + "/ur/bmi-calculator/"),
        ("x-default", SITE + "/bmi-calculator/"),
    }, "Urdu BMI hreflang alternates changed"
    jsonld_documents(source, slug)

def visible_text(slug):
    source = read_page(slug)
    main = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S | re.I)
    assert main, f"Missing main content: /{slug}/"
    body = re.sub(r"(?is)<(script|style|nav)\b.*?</\1>", " ", main.group(1))
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()

def check_targeted_content():
    required = {
        "years-to-days-calculator": [
            "Maintained by Muhammad Fayyaz Adeel",
            "Quick answers to common years-to-days questions",
            "5 years = 1,826.2125 days using the Gregorian average",
            "30 years = 10,957.275 days using the Gregorian average",
            "How many days are in 13 years?",
            "4,748.1525 days",
            "70,000 days ÷ 365.2425 = 191.6535 years",
            "Exact calendar days depend on the start date",
            "U.S. Naval Observatory leap-year explanation",
            "NIST's year definition",
        ],
        "unit-converter": [
            "Maintained by Muhammad Fayyaz Adeel",
            "Can centimeters be converted to pounds or kilograms?",
            "how many centimeters are in a pound",
            "cm to kg",
            "cm to lb",
            "Centimeters measure length",
            "pounds and kilograms measure mass",
            "Supported unit categories and choices",
            "Weight: kilograms (kg), grams (g), pounds (lb) and ounces (oz)",
            "Length: metres (m), centimetres (cm), kilometres (km), feet (ft), inches (in) and miles (mi)",
            "Temperature: Celsius (°C), Fahrenheit (°F) and Kelvin (K)",
            "Result = value × source-unit factor ÷ target-unit factor",
            "Temperature uses offset formulas rather than a single multiplier",
            "1 kg = 2.20462 lb",
            "100°F = 37.78°C",
            "Negative weight and length inputs are rejected",
            "Absolute zero is -273.15°C",
            "NIST Guide to the SI, Appendix B.9",
            "NIST Handbook 44 (2026), Appendix C",
        ],
        "tasbih-counter": [
            "Maintained by Muhammad Fayyaz Adeel",
            "Tasbih calculator and free online Tasbeeh counter",
            "calculator tasbih",
            "free online Tasbeeh counter",
            "does not listen to recitation",
            "What is a digital Tasbih counter?",
            "How to use this online Tasbih counter",
            "Five phrases and plain meanings",
            "Saving and privacy",
            "Worked example: target and remaining count",
            "Targets are personal tracking settings",
            "same browser and device",
            "does not sync across devices",
            "selected target",
            "custom target",
            "Reset requires confirmation",
            "Can I count with a keyboard?",
            "What happens if browser storage is unavailable?",
        ],
        "profit-loss-calculator": [
            "Maintained by Muhammad Fayyaz Adeel",
            "Using an online profit and loss calculator",
            "online profit and loss calculator",
            "Business P&L estimates gross profit",
            "Product profit compares a selling price",
            "profit and loss calculator online",
            "gross profit calculator",
            "operating profit calculator",
            "profit margin calculator",
            "does not calculate net profit after interest and tax",
            "does not calculate break-even sales",
        ],
    }
    for slug, phrases in required.items():
        content = visible_text(slug)
        for phrase in phrases:
            assert phrase.lower() in content.lower(), f"/{slug}/ is missing researched, user-facing content: {phrase}"
    expected_dates = {
        "tasbih-counter": "2026-11-21",
        "years-to-days-calculator": "2026-11-22",
        "unit-converter": "2026-11-21",
        "profit-loss-calculator": "2026-11-21",
    }
    for slug, expected_date in expected_dates.items():
        assert f"Last updated: {expected_date}" in visible_text(slug), f"/{slug}/ must display its verified update date"
    years_html = read_page("years-to-days-calculator")
    assert "https://aa.usno.navy.mil/faq/leap_years" in years_html
    assert "https://www.nist.gov/pml/time-and-frequency-division/popular-links/time-frequency-z/time-frequency-z-x-z" in years_html
    unit_html = read_page("unit-converter")
    assert "https://nvlpubs.nist.gov/nistpubs/hb/2026/NIST.HB.44-2026.pdf" in unit_html
    assert "https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9" in unit_html

def check_tasbih_content_structure():
    source = read_page("tasbih-counter")
    main_match = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S | re.I)
    assert main_match, "Tasbih page is missing its main content"
    body = main_match.group(1)
    headings = [html.unescape(value).strip() for value in re.findall(r"<h2[^>]*>(.*?)</h2>", body, re.S | re.I)]
    expected = [
        "What is a digital Tasbih counter?",
        "How to use this online Tasbih counter",
        "Five phrases and plain meanings",
        "Saving and privacy",
        "Worked example: target and remaining count",
        "Common questions",
        "Scope and religious guidance",
        "Related calculators",
    ]
    for heading in expected:
        assert headings.count(heading) == 1, f"Tasbih page must contain exactly one '{heading}' section"
    obsolete = [
        "Keyboard, storage and reset behaviour",
        "Saving, privacy, and limitations",
        "Choosing a target",
        "Privacy of your count",
        "Tasbih calculator and digital zikr counter example",
        "Choosing the right online tasbeeh counter",
        "Worked example",
        "Method",
        "Limits",
        "Using the counter during a short daily session",
        "What the counter can and cannot verify",
        "How it is calculated",
        "Sources",
    ]
    for heading in obsolete:
        assert heading not in headings, f"Redundant or misleading Tasbih section remains: {heading}"
    questions = [
        html.unescape(re.sub(r"<[^>]+>", " ", value)).strip()
        for value in re.findall(r"<summary\b[^>]*>(.*?)</summary>", body, re.S | re.I)
    ]
    assert len(questions) == 6, f"Tasbih page should have six distinct FAQs, got {len(questions)}"
    assert len({question.casefold() for question in questions}) == len(questions), "Tasbih FAQ questions must not be duplicated"
    content = visible_text("tasbih-counter")
    assert content.casefold().count("three groups of 33 presses") == 1, "The 99-count worked example must appear once"
    assert content.count("99 - 67 = 32") == 1, "The remaining-count arithmetic must appear once"
    assert "When browser storage is available, the current count, selected phrase and selected target" in content, "The page must accurately explain which settings persist"
    assert "does not sync across devices" in content.lower(), "The page must explain device-local storage"



def check_years_quick_reference():
    source = read_page("years-to-days-calculator")
    section_marker = "Quick reference: years to days"
    assert section_marker in source, "Years-to-days quick reference section is missing"
    quick_section = source.split(section_marker, 1)[1]
    quick_match = re.search(r"<table\b[^>]*>(.*?)</table>", quick_section, re.S | re.I)
    assert quick_match, "Years-to-days quick reference table is missing"

    def table_rows(table_html):
        parsed = []
        for year, cells_html in re.findall(r'<tr>\s*<th\b[^>]*scope="row"[^>]*>(.*?)</th>(.*?)</tr>', table_html, re.S | re.I):
            cells = [
                html.unescape(re.sub(r"<[^>]+>", "", value)).strip()
                for value in re.findall(r"<td\b[^>]*>(.*?)</td>", cells_html, re.S | re.I)
            ]
            parsed.append((html.unescape(re.sub(r"<[^>]+>", "", year)).strip(), cells))
        return parsed

    expected_years = ["2", "3", "5", "7", "9", "10", "13", "20"]
    quick_rows = table_rows(quick_match.group(1))
    actual_years = [year for year, _ in quick_rows]
    assert actual_years == expected_years, (
        "Quick reference must prioritize observed 28-day GSC year queries without changing its table structure; "
        f"expected={expected_years!r}, actual={actual_years!r}"
    )

    expected_values = {
        "2": ["730", "730.5", "730.485"],
        "3": ["1,095", "1,095.75", "1,095.7275"],
        "5": ["1,825", "1,826.25", "1,826.2125"],
        "7": ["2,555", "2,556.75", "2,556.6975"],
        "10": ["3,650", "3,652.5", "3,652.425"],
        "13": ["4,745", "4,748.25", "4,748.1525"],
        "9": ["3,285", "3,287.25", "3,287.1825"],
        "20": ["7,300", "7,305", "7,304.85"],
    }
    assert dict(quick_rows) == expected_values, "Quick-reference arithmetic changed"

    full_reference = quick_section.split('id="years-days-full-reference"', 1)[1]
    full_match = re.search(r"<table\b[^>]*>(.*?)</table>", full_reference, re.S | re.I)
    assert full_match, "Expanded years-to-days reference table is missing"
    full_rows = table_rows(full_match.group(1))
    assert len(full_rows) == 29, f"Expanded reference must retain 29 examples, got {len(full_rows)}"
    assert set(expected_years).issubset({year for year, _ in full_rows}), "Quick-reference rows must remain in the expanded table"
    assert "19" in {year for year, _ in full_rows}, "Removing 19 years from the quick table must not remove it from the expanded reference"

    visible = visible_text("years-to-days-calculator")
    assert "Last updated: 2026-11-22" in visible, "Visible update date must match the substantive quick-reference refresh"
    schemas = jsonld_documents(source, "years-to-days-calculator")
    webpage = next((item for item in schemas if item.get("@type") == "WebPage"), None)
    assert webpage and webpage.get("dateModified") == "2026-11-22", "Structured dateModified must match the visible update date"



def main():
    for slug, spec in CASES.items():
        check_english_page(slug, spec)
    check_urdu_bmi()
    check_targeted_content()
    check_years_quick_reference()
    check_tasbih_content_structure()
    print("PASS: priority pages have targeted metadata, first-screen order, relevant links, FAQs, valid JSON-LD, preserved canonicals, and research-backed content")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
