#!/usr/bin/env python3
"""Focused regression checks for the Urdu BMI page's answerability and trust signals."""
import html
import json
import re
from pathlib import Path

PAGE = Path("public/ur/bmi-calculator/index.html")
SITE = "https://calculateallinone.vercel.app"
EXPECTED_TITLE = "BMI کیلکولیٹر اردو میں | بالغ افراد | CalculatesAll"
EXPECTED_DESCRIPTION = "بالغوں کا BMI اردو میں معلوم کریں۔ وزن kg/lb اور قد cm یا فٹ/انچ درج کریں۔ WHO کی حدیں دیکھیں۔ یہ اسکریننگ ہے، تشخیص نہیں۔"


def visible(value):
    value = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", value)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def main():
    assert PAGE.is_file(), "Urdu BMI page was not generated"
    raw = PAGE.read_text(encoding="utf-8")
    main_match = re.search(r"<main\b[^>]*>(.*?)</main>", raw, re.S | re.I)
    assert main_match, "Urdu BMI page is missing main content"
    body = main_match.group(1)

    title = re.search(r"<title>(.*?)</title>", raw, re.S | re.I)
    description = re.search(r'<meta name="description" content="([^"]*)"', raw)
    assert title and html.unescape(title.group(1)) == EXPECTED_TITLE, "Unexpected Urdu BMI search title"
    assert description and html.unescape(description.group(1)) == EXPECTED_DESCRIPTION, "Unexpected Urdu BMI meta description"
    assert len(EXPECTED_TITLE) < 60, "Title exceeds the site's tested title limit"
    assert 70 <= len(EXPECTED_DESCRIPTION) < 160, "Meta description is outside the site's tested length range"
    assert f'<link rel="canonical" href="{SITE}/ur/bmi-calculator/">' in raw, "Canonical URL changed"
    assert '<meta name="robots" content="index, follow">' in raw, "Urdu BMI page must remain indexable"
    assert '<html lang="ur" dir="rtl">' in raw, "Urdu language or RTL direction changed"

    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", body, re.S | re.I)
    assert len(h1s) == 1, f"Expected exactly one H1, found {len(h1s)}"
    first_paragraph = re.search(r"</h1>\s*<p\b[^>]*>(.*?)</p>", body, re.S | re.I)
    assert first_paragraph, "A direct opening answer must follow the H1"
    opening = visible(first_paragraph.group(1))
    for phrase in ("BMI", "وزن", "قد", "میٹر", "اسکریننگ"):
        assert phrase in opening, f"Answer-first opening is missing {phrase!r}"
    assert "÷" in opening and "²" in opening, "Opening must state the BMI formula directly"
    assert len(opening.split()) >= 25, "Opening answer must contain enough context to stand alone"
    assert "تشخیص نہیں" in opening, "Opening must clarify that BMI is not a diagnosis"

    assert 'id="bmi-form"' in body and "BMI کا حساب کریں" in body, "Existing BMI calculator form or action is missing"
    assert 'id="bmi-urdu-summary"' in body, "A concise, visible answer summary is missing"
    assert "BMI کیا ہے اور اسے کیسے نکالتے ہیں?" in body, "Missing question-led BMI definition section"
    assert "بالغوں کے BMI کی معیاری حدود کیا ہیں?" in body, "Missing question-led adult BMI category section"
    assert "جنوبی ایشیائی افراد کے لیے اضافی BMI حدود کیا ہیں?" in body, "Missing South Asian risk-threshold explanation"
    assert "BMI کن باتوں کی نشاندہی نہیں کرتا?" in body, "Missing BMI limitation section"
    assert "BMI کے نتیجے کے بعد کیا کرنا چاہیے?" in body, "Missing next-step section"

    # The international WHO categories stay unchanged; Asian action points are explicitly contextualised.
    for phrase in ("18.5", "25", "30", "23.0", "27.5", "WHO"):
        assert phrase in visible(body), f"Missing supported BMI threshold or source: {phrase}"
    body_text = visible(body)
    assert "درجہ بندی کا متبادل نہیں" in body_text, "Asian action points must not be presented as a replacement global classification"
    assert "تمام ایشیائی آبادیوں کے لیے ایک ہی نئی حد مقرر نہیں کی جا سکتی" in body_text, "Asian risk thresholds need a population-specific limitation"

    for domain in ("who.int", "cdc.gov", "nhs.uk", "pubmed.ncbi.nlm.nih.gov"):
        assert domain in body, f"Missing visible authoritative source link: {domain}"
    assert "صفحے کے منتظم" in body and "Muhammad Fayyaz Adeel" in body and 'href="/about/"' in body, "Missing truthful maintainer identity"
    assert "طبی تشخیص یا علاج کا متبادل نہیں" in body, "The page must retain its medical-use limitation"
    assert "طبی ماہر نے جائزہ لیا" not in body, "The page must not claim an unverified medical review"

    schemas = []
    for match in re.finditer(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', raw, re.S | re.I):
        parsed = json.loads(match.group(1))
        schemas.extend(parsed if isinstance(parsed, list) else [parsed])
    app = next((item for item in schemas if item.get("@type") == "WebApplication"), None)
    page = next((item for item in schemas if item.get("@type") == "WebPage"), None)
    faq = next((item for item in schemas if item.get("@type") == "FAQPage"), None)
    breadcrumb = next((item for item in schemas if item.get("@type") == "BreadcrumbList"), None)
    organization = next((item for item in schemas if item.get("@type") == "Organization"), None)
    assert app and page and faq and breadcrumb and organization, "Missing WebApplication, WebPage, FAQPage, BreadcrumbList or Organization JSON-LD"
    assert "inLanguage" not in breadcrumb, "BreadcrumbList must not use the unsupported inLanguage property"
    assert "https://github.com/Beastmalik7424/calculatesallinone" in organization.get("sameAs", []), "Organization must link to its official source repository"
    assert app.get("description") == html.unescape(description.group(1)), "WebApplication description must match the visible search description"
    assert app.get("author", {}).get("@id") == SITE + "/#maintainer", "WebApplication author entity is missing"
    assert app.get("publisher", {}).get("@id") == SITE + "/#organization", "WebApplication publisher entity is missing"
    assert page.get("author", {}).get("@id") == SITE + "/#maintainer", "WebPage author entity is missing"
    assert page.get("publisher", {}).get("@id") == SITE + "/#organization", "WebPage publisher entity is missing"
    assert page.get("dateModified") == "2026-11-06", "Verified page-specific content update date is missing"
    citations = " ".join(page.get("citation", []))
    for domain in ("who.int", "cdc.gov", "nhs.uk", "pubmed.ncbi.nlm.nih.gov"):
        assert domain in citations, f"Missing structured citation: {domain}"

    visible_questions = [
        visible(q) for q in re.findall(r"<summary\b[^>]*>(.*?)</summary>", body, re.S | re.I)
    ]
    schema_questions = [item.get("name") for item in faq.get("mainEntity", [])]
    assert len(visible_questions) >= 6, "Expected useful visible FAQ coverage"
    assert schema_questions == visible_questions, "FAQ JSON-LD must exactly match visible FAQ questions"
    assert len(re.findall(r"<h2\b[^>]*>.*?\?</h2>", body, re.S | re.I)) >= 5, "Expected at least five question-led answer sections"

    print("PASS: Urdu BMI title, description, canonical and indexability")
    print("PASS: answer-first definition, summary and question-led self-contained sections")
    print("PASS: WHO and South Asian BMI thresholds are distinguished accurately")
    print("PASS: visible authoritative citations, maintainer disclosure and medical-review limitation")
    print("PASS: WebApplication, WebPage and FAQ structured data match visible content")
    print("PASS: existing BMI form remains present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
