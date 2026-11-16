#!/usr/bin/env python3
"""Regression tests for useful, source-backed priority-page content and preserved controls."""
from pathlib import Path
import html
import re

ROOT = Path("public")
PAGES = {
    "bmi-calculator": {
        "required": [
            "Adult BMI categories", "23.0", "27.5", "action points",
            "waist circumference", "70 kg", "1.70 m", "24.2",
            "independently of the height unit", "Limitations", "Sources",
            "Last reviewed",
        ],
        "faqs": 6,
        "sources": ["who.int", "cdc.gov", "doi.org/10.1016/S0140-6736(03)15268-3"],
    },
    "profit-loss-calculator": {
        "required": [
            "Business P&L formulas", "Product profit formulas",
            "Markup versus margin at a glance", "opening inventory",
            "purchases", "closing inventory", "gross profit", "gross margin",
            "100,000", "45,000", "55,000", "55%",
            "PKR 800", "PKR 50", "PKR 30", "PKR 1,100", "PKR 220",
            "markup on cost", "gross margin on selling price",
            "profit is not cash", "payout delays",
            "does not count inventory or derive COGS for you",
            "Limitations", "Sources", "Last reviewed",
        ],
        "faqs": 6,
        "sources": ["openstax.org", "accaglobal.com"],
    },
    "zakat-calculator": {
        "required": [
            "503,529", "1446–1447 AH", "1447 AH (2026)", "first day of Ramazan",
            "saving", "profit and loss sharing", "2.5%",
            "87.48 g", "612.36 g",
            "Which assets to include", "Which liabilities may be deducted",
            "How the calculation works", "Worked example with checkable arithmetic",
            "1,837,080", "700,000", "2,000,000", "50,000",
            "Personal-use property and other exclusions",
            "Pakistan bank deduction threshold is separate",
            "Worldwide currency support, privacy and limitations",
            "changes yearly", "qualified scholar", "Sources", "Last reviewed",
        ],
        "faqs": 8,
        "sources": ["sbp.org.pk", "islamic-relief.org.uk", "islamweb.net"],
    },
}


def read(slug):
    path = ROOT / slug / "index.html"
    assert path.is_file(), f"Missing generated page: {path}"
    return path.read_text(encoding="utf-8")


def visible(source):
    source = re.sub(r"(?is)<(script|style|nav)\b.*?</\1>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", source))).strip()


faq_sets = {}
paragraph_sets = {}
for slug, spec in PAGES.items():
    source = read(slug)
    text = visible(source)
    for phrase in spec["required"]:
        assert phrase.casefold() in text.casefold(), f"/{slug}/ missing required content: {phrase}"
    for domain in spec["sources"]:
        assert domain in source, f"/{slug}/ missing source link for {domain}"
    hrefs = re.findall(r"<a\b[^>]*href=[\"']https?://[^\"']+[\"']", source, re.I)
    assert hrefs, f"/{slug}/ needs working external source links"
    questions = [visible(q) for q in re.findall(r"<summary\b[^>]*>(.*?)</summary>", source, re.S | re.I)]
    assert len(questions) == spec["faqs"], f"/{slug}/ must have exactly {spec['faqs']} page-specific FAQs, got {len(questions)}"
    assert len(set(q.casefold() for q in questions)) == len(questions), f"/{slug}/ repeats an FAQ"
    faq_sets[slug] = set(q.casefold() for q in questions)
    paragraphs = [visible(p) for p in re.findall(r"<p\b[^>]*>(.*?)</p>", source, re.S | re.I)]
    paragraph_sets[slug] = set(p.casefold() for p in paragraphs if len(p) > 60)
    assert "Maintained by" in source and "Muhammad Fayyaz Adeel" in source, f"/{slug}/ missing author byline"
    assert re.search(r"Last reviewed: 2026-11-16", text), f"/{slug}/ missing current Last reviewed date"

for left in paragraph_sets:
    for right in paragraph_sets:
        if left >= right:
            continue
        duplicates = paragraph_sets[left] & paragraph_sets[right]
        assert not duplicates, f"Duplicated substantive paragraphs across {left} and {right}: {sorted(duplicates)[:1]}"
        assert not (faq_sets[left] & faq_sets[right]), f"FAQ question repeated across {left} and {right}"

bmi_html = read("bmi-calculator")
bmi_description = re.search(r'<meta name="description" content="([^"]+)"', bmi_html)
assert bmi_description, "BMI page must have a meta description"
assert "kilograms or pounds" in bmi_description.group(1).lower(), "BMI description must describe both weight units"
assert "centimetres or feet and inches" in bmi_description.group(1).lower(), "BMI description must describe both height units"
assert "kilograms with feet and inches" not in bmi_description.group(1).lower(), "BMI description must not claim pounds are kilograms"
for control_id in (
    "bmi-weight-kg", "bmi-weight-lb", "bmi-height-cm", "bmi-height-ftin",
    "bmi-weight-kg-group", "bmi-weight-lb-group", "bmi-metric", "bmi-imperial",
):
    assert f'id="{control_id}"' in bmi_html, f"BMI page lost independent unit control: {control_id}"
assert 'id="bmi-unit"' not in bmi_html, "BMI must retain independent weight and height unit selectors"

bmi_worked_sections = re.findall(r"<h2\b[^>]*>\s*Worked examples?\s*</h2>", bmi_html, re.I)
assert len(bmi_worked_sections) == 1, f"BMI must contain one consolidated worked-example section, got {len(bmi_worked_sections)}"

pnl_html = read("profit-loss-calculator")
assert 'id="p-cogs"' in pnl_html and 'id="p-cost"' in pnl_html and 'id="p-sell"' in pnl_html
assert "COGS = opening inventory + purchases" in visible(pnl_html), "P&L must state the exact approved COGS formula"
assert visible(pnl_html).count("COGS = opening inventory + purchases") == 1, "P&L must state the COGS formula once"
assert "does not count inventory or derive COGS for you" in visible(pnl_html), "P&L must distinguish the COGS guide formula from calculator inputs"

zakat_words = len(re.findall(r"\b[\w’'-]+\b", visible(zakat_html)))
urdu_zakat_html = (ROOT / "ur" / "zakat-calculator" / "index.html").read_text(encoding="utf-8")
urdu_zakat_words = len(re.findall(r"\b[\w’'-]+\b", visible(urdu_zakat_html)))
assert zakat_words >= 1000, f"English Zakat page must contain at least 1,000 useful visible words, got {zakat_words}"
assert urdu_zakat_words >= 700, f"Urdu Zakat page must contain at least 700 useful visible words, got {urdu_zakat_words}"

zakat_html = read("zakat-calculator")
assert 'value="silver"' in zakat_html and 'value="gold-87"' in zakat_html and 'value="gold-85"' not in zakat_html
assert "85 g" not in visible(zakat_html), "Zakat page must not present the unapproved 85 g gold method"
assert re.search(r'"dateModified"\s*:\s*"2026-11-16"', zakat_html), "Zakat WebPage dateModified must match the visible review date"

money_source = read("money")
money = visible(money_source)
for phrase in [
    "Choose the right money calculator",
    "Worked examples and how to check a result",
    "Loan and interest assumptions",
    "Currency, precision and limits",
    "Why every percentage needs a named base",
    "Recommended monthly close process",
    "A practical monthly close: from sales to operating profit",
    "recommended working process",
    "reconcile platform payouts",
    "count the inventory",
    "record the month's expenses and platform or payment fees",
    "reconcile the bank or wallet balance",
    "review gross profit, net profit",
    "lock the reviewed period",
    "next month's opening stock",
    "not an official accounting standard",
    "monthly close",
]:
    assert phrase.casefold() in money.casefold(), f"/money/ missing useful guidance: {phrase}"
assert "COGS = opening inventory + purchases − closing inventory" in money, "Money hub must use the approved COGS formula"
assert money.count("COGS = opening inventory + purchases − closing inventory") == 1, "Money hub must state the COGS formula once"
assert "gross profit as revenue minus COGS" in money, "Money hub must use the approved gross-profit basis"
assert "Sources" in money and "Last reviewed: 2026-11-16" in money, "Money hub needs sources and review date"
assert re.search(r"<a\b[^>]*href=[\"']https?://[^\"']+[\"']", money_source, re.I), "Money hub needs a working source link"
money_faqs = [visible(q) for q in re.findall(r"<summary\b[^>]*>(.*?)</summary>", money_source, re.S | re.I)]
assert 3 <= len(money_faqs) <= 4, f"/money/ must have 3–4 unique FAQs, got {len(money_faqs)}"
assert len(set(q.casefold() for q in money_faqs)) == len(money_faqs), "Money hub repeats an FAQ"

home = visible(read("index"))
privacy_claim = "calculations run in your browser, and calculator entries are not sent to our server"
assert home.casefold().count(privacy_claim.casefold()) == 1, "Homepage must state the browser privacy claim exactly once"
assert "recalculated whenever a tool changes" not in home.casefold(), "Remove unsupported automatic recalculation claim"
print("PASS: priority page content, independent BMI controls, accurate metadata, sources, review dates, unique paragraphs/FAQs and homepage claims")
