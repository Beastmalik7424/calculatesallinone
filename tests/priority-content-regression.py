#!/usr/bin/env python3
"""Regression tests for the verified BMI, P&L, Money hub and Zakat content."""
from pathlib import Path
import html
import re

ROOT = Path("public")
PAGES = {
    "bmi-calculator": {
        "required": ["Adult BMI categories", "23.0", "27.5", "action points", "waist circumference", "70 kg", "1.70 m", "24.2", "Limitations", "Sources", "Last reviewed"],
        "faqs": 3,
        "sources": ["who.int", "doi.org/10.1016/S0140-6736(03)15268-3"],
    },
    "profit-loss-calculator": {
        "required": ["COGS", "opening inventory", "purchases", "closing inventory", "gross profit", "gross margin", "100,000", "45,000", "55,000", "55%", "profit is not cash", "payout delays", "Limitations", "Sources", "Last reviewed"],
        "faqs": 3,
        "sources": ["openstax.org"],
    },
    "zakat-calculator": {
        "required": ["503,529", "1447 AH", "first day of Ramazan", "saving", "2.5%", "87.48 g", "612.36 g", "1,837,080", "700,000", "2,000,000", "50,000", "changes yearly", "Limitations", "Sources", "Last reviewed"],
        "faqs": 3,
        "sources": ["sbp.org.pk", "doi.org"],
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

money_source = read("money")
money = visible(money_source)
for phrase in ["recommended process", "reconcile platform payouts", "count inventory", "record expenses and fees",
               "reconcile the bank or wallet balance", "review gross and net profit", "lock the period",
               "next month's opening stock", "monthly close"]:
    assert phrase.casefold() in money.casefold(), f"/money/ missing monthly-close step: {phrase}"
assert "not an official accounting standard" in money.casefold(), "Money hub must label the checklist as a recommendation"
assert "Sources" in money and "Last reviewed: 2026-11-16" in money, "Money hub needs sources and review date"
assert re.search(r"<a\b[^>]*href=[\"']https?://[^\"']+[\"']", money_source, re.I), "Money hub needs a working source link"
money_faqs = [visible(q) for q in re.findall(r"<summary\b[^>]*>(.*?)</summary>", money_source, re.S | re.I)]
assert 3 <= len(money_faqs) <= 4, f"/money/ must have 3–4 unique FAQs, got {len(money_faqs)}"
assert len(set(q.casefold() for q in money_faqs)) == len(money_faqs), "Money hub repeats an FAQ"

home = visible((ROOT / "index.html").read_text(encoding="utf-8"))
privacy_claim = "calculations run in your browser, and calculator entries are not sent to our server"
assert home.casefold().count(privacy_claim.casefold()) == 1, "Homepage must state the browser privacy claim exactly once"
assert "recalculated whenever a tool changes" not in home.casefold(), "Remove unsupported automatic recalculation claim"
print("PASS: priority page structure, sources, review dates, unique paragraphs/FAQs and homepage claims")
