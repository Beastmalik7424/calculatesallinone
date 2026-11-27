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
        "description": "Free Tasbih calculator and digital Tasbih counter. Tasbeeh counter with 33, 99, 100 or custom targets, undo and local saving when supported.",
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
        "description": "How many days in 5, 10, 13, 19 or 30 years? Compare 365, 365.25 and 365.2425-day methods, or count exact Gregorian days from a start date.",
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
    if slug == "tasbih-counter":
        assert len(description.group(1)) <= 140 and "when supported" in description.group(1), "Tasbih meta description must qualify local saving because browser storage may be unavailable"
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
        unit_value = re.search(r'<input\b[^>]*id="u-val"[^>]*>', source)
        assert unit_value, "Unit Converter value input must exist"
        assert not re.search(r"\bmin\s*=", unit_value.group(0)), "Unit Converter value input must not declare min=0 because Celsius and Fahrenheit accept negative values above absolute zero"
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
            "How many days in 5 years? Using the 365.2425-day Gregorian mean, 5 years = 1,826.2125 days using the Gregorian average",
            "How many days in 30 years? Using the 365.2425-day Gregorian mean, 30 years = 10,957.275 days",
            "How many days are in 13 years?",
            "5 years how many days",
            "5 years is how many days",
            "how many days are in 5 years",
            "5 years to days",
            "10 years in days",
            "10 years is how many days",
            "how many days are in 10 years",
            "How many days are in 5 and a half years?",
            "2,007.5 days",
            "2,008.875 days",
            "2,008.83375 days",
            "How many days are in 5 years and 4 months?",
            "1,946.6667 days",
            "1,948 days",
            "1,947.96 days",
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
            "tasbih counter online",
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
    tasbih_faq = re.findall(r"<summary\b[^>]*>(.*?)</summary>", read_page("tasbih-counter"), re.S | re.I)
    assert "What is a Tasbih calculator?" in [html.unescape(item).strip() for item in tasbih_faq], "Tasbih page must answer the exact calculator-intent question"
    years_faq = re.findall(r"<summary\b[^>]*>(.*?)</summary>", read_page("years-to-days-calculator"), re.S | re.I)
    years_faq = [html.unescape(item).strip() for item in years_faq]
    assert "How many days in 19 years?" in years_faq, "Years-to-Days FAQ must answer the observed 19-year query"
    assert "How many days in 30 years?" in years_faq, "Years-to-Days FAQ must answer the observed 30-year query"

    expected_dates = {
        "tasbih-counter": "2026-11-27",
        "years-to-days-calculator": "2026-11-27",
        "unit-converter": "2026-11-21",
        "profit-loss-calculator": "2026-11-21",
        "query-calculator": "2026-11-27",
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
    assert len(questions) == 7, f"Tasbih page should have seven distinct FAQs, got {len(questions)}"
    assert len({question.casefold() for question in questions}) == len(questions), "Tasbih FAQ questions must not be duplicated"
    content = visible_text("tasbih-counter")
    assert "Choose 33, 99 or a custom target" in content, "Tasbih introduction must foreground 99 and custom targets"
    assert "Space or Enter" in content and "Undo" in content, "Tasbih introduction must foreground keyboard counting and Undo"
    assert content.casefold().count("three groups of 33 presses") == 1, "The 99-count worked example must appear once"
    assert content.count("99 - 67 = 32") == 1, "The remaining-count arithmetic must appear once"
    assert "When browser storage is available, the current count, selected phrase and selected target" in content, "The page must accurately explain which settings persist"
    assert "does not sync across devices" in content.lower(), "The page must explain device-local storage"
    for phrase in (
        "Practical counting workflows and milestones",
        "choose Custom target and enter 1,000",
        "three groups of 33",
        "ten sets of 100",
        "polite live output",
        "does not intercept your typing",
        "when local storage is available",
    ):
        assert phrase.lower() in content.lower(), "Tasbih practical workflow or accessibility guidance is missing: " + phrase



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

    expected_years = ["2", "3", "4", "5", "7", "9", "10", "11", "12", "13", "14", "15", "16", "18", "19", "20", "21", "23", "28", "30", "60", "80"]
    quick_rows = table_rows(quick_match.group(1))
    actual_years = [year for year, _ in quick_rows]
    assert actual_years == expected_years, (
        "Quick reference must prioritize common year values without changing its table structure; "
        f"expected={expected_years!r}, actual={actual_years!r}"
    )

    expected_values = {
        "2": ["730", "730.5", "730.485"],
        "3": ["1,095", "1,095.75", "1,095.7275"],
        "4": ["1,460", "1,461", "1,460.97"],
        "5": ["1,825", "1,826.25", "1,826.2125"],
        "7": ["2,555", "2,556.75", "2,556.6975"],
        "9": ["3,285", "3,287.25", "3,287.1825"],
        "10": ["3,650", "3,652.5", "3,652.425"],
        "11": ["4,015", "4,017.75", "4,017.6675"],
        "12": ["4,380", "4,383", "4,382.91"],
        "13": ["4,745", "4,748.25", "4,748.1525"],
        "14": ["5,110", "5,113.5", "5,113.395"],
        "15": ["5,475", "5,478.75", "5,478.6375"],
        "16": ["5,840", "5,844", "5,843.88"],
        "18": ["6,570", "6,574.5", "6,574.365"],
        "19": ["6,935", "6,939.75", "6,939.6075"],
        "20": ["7,300", "7,305", "7,304.85"],
        "21": ["7,665", "7,670.25", "7,670.0925"],
        "23": ["8,395", "8,400.75", "8,400.5775"],
        "28": ["10,220", "10,227", "10,226.79"],
        "30": ["10,950", "10,957.5", "10,957.275"],
        "60": ["21,900", "21,915", "21,914.55"],
        "80": ["29,200", "29,220", "29,219.4"],
    }
    assert dict(quick_rows) == expected_values, "Quick-reference arithmetic changed"

    full_reference = quick_section.split('id="years-days-full-reference"', 1)[1]
    full_match = re.search(r"<table\b[^>]*>(.*?)</table>", full_reference, re.S | re.I)
    assert full_match, "Expanded years-to-days reference table is missing"
    full_rows = table_rows(full_match.group(1))
    assert len(full_rows) == 63, f"Expanded reference must contain 63 calculated examples, got {len(full_rows)}"
    assert set(expected_years).issubset({year for year, _ in full_rows}), "Quick-reference rows must remain in the expanded table"
    assert "19" in {year for year, _ in full_rows}, "The 19-year conversion row must remain in the expanded reference"
    expected_additional_year_rows = {
        "8": ["2,920", "2,922", "2,921.94"],
        "17": ["6,205", "6,209.25", "6,209.1225"],
        "18": ["6,570", "6,574.5", "6,574.365"],
        "22": ["8,030", "8,035.5", "8,035.335"],
        "23": ["8,395", "8,400.75", "8,400.5775"],
        "28": ["10,220", "10,227", "10,226.79"],
        "36": ["13,140", "13,149", "13,148.73"],
        "65": ["23,725", "23,741.25", "23,740.7625"],
    }
    full_row_map = dict(full_rows)
    for year, values in expected_additional_year_rows.items():
        assert full_row_map.get(year) == values, f"Expanded reference is missing the expected calculated row for {year} years"

    visible = visible_text("years-to-days-calculator")
    common_query_answers = (
        ("How many days in 2 years?", "730.485 days"),
        ("How many days in 3 years?", "1,095.7275 days"),
        ("How many days in 4 years?", "1,460.97 days"),
        ("How many days in 5 years?", "1,826.2125 days"),
        ("How many days in 10 years?", "3,652.425 days"),
        ("How many days are in 13 years?", "4,748.1525 days"),
        ("How many days in 19 years?", "6,939.6075 days"),
        ("How many days in 30 years?", "10,957.275 days"),
    )
    for question, answer in common_query_answers:
        assert question in visible and answer in visible, (
            "Years-to-Days content must directly answer common question examples with verified values: " + question
        )
    assert "Last updated: 2026-11-27" in visible, "Visible update date must match the question-led answer and snippet refresh"
    schemas = jsonld_documents(source, "years-to-days-calculator")
    webpage = next((item for item in schemas if item.get("@type") == "WebPage"), None)
    assert webpage and webpage.get("dateModified") == "2026-11-27", "Structured dateModified must match the visible update date"




def check_years_ten_year_faq():
    source = read_page("years-to-days-calculator")
    schemas = jsonld_documents(source, "years-to-days-calculator")
    faq_schema = next((item for item in schemas if item.get("@type") == "FAQPage"), None)
    assert faq_schema, "Years-to-Days page must retain its FAQPage structured data"
    question = next(
        (item for item in faq_schema.get("mainEntity", []) if item.get("name") == "How many days in 10 years?"),
        None,
    )
    assert question, "The 10-year question must have its own visible FAQ and FAQPage entry"
    answer = question.get("acceptedAnswer", {}).get("text", "")
    for phrase in (
        "3,650 days",
        "3,652.425 days",
        "3,652.5 days",
        "3,653 days",
        "3,652 days",
        "1 Jan 2020 to 1 Jan 2030",
        "1 Jan 2021 to 1 Jan 2031",
    ):
        assert phrase in answer, "10-year FAQ must distinguish average methods from exact calendar intervals: " + phrase
    main_match = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S | re.I)
    assert main_match, "Years-to-Days page main content is missing"
    summaries = [
        html.unescape(re.sub(r"<[^>]+>", " ", value)).strip()
        for value in re.findall(r"<summary\b[^>]*>(.*?)</summary>", main_match.group(1), re.S | re.I)
    ]
    assert "How many days in 10 years?" in summaries, "10-year answer must be visible as a user-facing FAQ, not only mentioned in guide prose"
    content = visible_text("years-to-days-calculator").lower()
    for phrase in (
        "fixed 365-day convention",
        "common year has 365 days and a leap year has 366 days",
        "29 February is added",
        "divisible by 4",
        "divisible by 400",
        "1900 was not a leap year",
        "2000 was",
        "97 leap days",
        "mean year is exactly 365.2425 days",
        "age example",
        "contract example",
        "project timeline example",
        "do not subtract weekends, public holidays",
    ):
        assert phrase.lower() in content, "Years-to-Days practical method guidance is missing: " + phrase


def check_bmi_content():
    """Guard BMI guidance, source transparency and unchanged calculator controls."""
    bmi_source = read_page("bmi-calculator")
    bmi_text = visible_text("bmi-calculator")
    required = (
        "How to use this BMI calculator",
        "What is body mass index (BMI)?",
        "BMI formula and unit conversions",
        "Standard adult BMI categories",
        "BMI interpretation for South Asian adults",
        "Waist-to-height ratio: an additional measure",
        "What BMI cannot tell you",
        "Using your result responsibly",
        "Medical disclaimer",
        "23.0 to 27.4",
        "27.5 or above",
        "does not automatically apply",
        "unrounded BMI",
        "BMI = weight in kilograms",
        "CDC's adult BMI categories are for ages 20 and older",
    )
    for phrase in required:
        assert phrase.lower() in bmi_text.lower(), "BMI page is missing researched content: " + phrase
    for source_url in (
        "https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight",
        "https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html",
        "https://www.cdc.gov/growth-chart-training/hcp/using-bmi/calculating-bmi.html",
        "https://www.nice.org.uk/guidance/ng246/chapter/Identifying-and-assessing-overweight-obesity-and-central-adiposity",
        "https://pubmed.ncbi.nlm.nih.gov/14726171/",
    ):
        assert source_url in bmi_source, "BMI page is missing an authoritative reference: " + source_url
    assert "reviewed by" not in bmi_text.lower(), "BMI page must not imply an unverified medical review"
    assert "medically reviewed" not in bmi_text.lower(), "BMI page must not claim medical review that has not occurred"
    assert "doctor-approved" not in bmi_text.lower(), "BMI page must not claim unverified doctor approval"
    assert 'id="bmi-form"' in bmi_source and 'id="b-kg"' in bmi_source and 'id="b-cm"' in bmi_source, "BMI calculator controls must remain present"
    assert 'href="/calorie-calculator/"' in bmi_source, "BMI page must retain its relevant adult calorie calculator link"
    assert len(re.findall(r"<summary\b", bmi_source, re.I)) >= 8, "BMI page must retain its useful FAQs"
    for heading in ("How to use this BMI calculator", "What is body mass index (BMI)?", "BMI formula and unit conversions", "Standard adult BMI categories", "BMI interpretation for South Asian adults", "Waist-to-height ratio: an additional measure", "What BMI cannot tell you", "Using your result responsibly", "How BMI and calorie estimates differ", "Medical disclaimer"):
        assert bmi_text.count(heading) == 1, "BMI section must appear exactly once: " + heading
    assert "How to measure consistently" not in bmi_text and "Pakistan and South Asia context" not in bmi_text, "Superseded BMI sections must not be duplicated"


def check_urdu_unit_converter():
    path = ROOT / "ur" / "unit-converter" / "index.html"
    assert path.exists(), "Existing Urdu Unit Converter page must remain generated"
    source = path.read_text(encoding="utf-8")
    unit_value = re.search(r'<input\b[^>]*id="u-val"[^>]*>', source)
    assert unit_value, "Urdu Unit Converter value input must exist"
    assert not re.search(r"\bmin\s*=", unit_value.group(0)), "Urdu Unit Converter value input must allow valid negative temperatures"


def main():
    for slug, spec in CASES.items():
        check_english_page(slug, spec)
    check_urdu_bmi()
    check_urdu_unit_converter()
    check_targeted_content()
    check_bmi_content()
    check_years_quick_reference()
    check_years_ten_year_faq()
    check_tasbih_content_structure()
    print("PASS: priority pages have targeted metadata, first-screen order, relevant links, FAQs, valid JSON-LD, preserved canonicals, and research-backed content")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
