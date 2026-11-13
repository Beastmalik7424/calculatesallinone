from pathlib import Path
import json
import re

def page(slug):
    path = Path("public") / slug / "index.html"
    assert path.is_file(), f"Missing generated /{slug}/ page"
    html = path.read_text(encoding="utf-8")
    assert re.search(r'<link rel="canonical" href="https://calculateallinone\.vercel\.app/' + slug + r'/">', html), slug
    assert re.search(r'<meta name="robots" content="index, follow">', html), slug
    assert '<nav aria-label="Breadcrumb"' in html, f"Missing visible breadcrumb on /{slug}/"
    assert '<a class="underline text-sky-800 dark:text-sky-300 hover:text-sky-950" href="/">Home</a>' in html, f"Missing Home breadcrumb link on /{slug}/"
    schemas = [json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    nodes = [node for item in schemas for node in (item.get("@graph", []) if isinstance(item, dict) and "@graph" in item else [item])]
    crumbs = [node for node in nodes if node.get("@type") == "BreadcrumbList"]
    assert len(crumbs) == 1, f"Expected one BreadcrumbList on /{slug}/"
    items = crumbs[0].get("itemListElement", [])
    assert len(items) == 2 and items[0].get("item") == "https://calculateallinone.vercel.app/" and items[1].get("item") == f"https://calculateallinone.vercel.app/{slug}/", f"Invalid breadcrumb schema on /{slug}/"
    return html

for slug in ("money", "math", "health", "time", "worship"):
    page(slug)

money = page("money")
math = page("math")
time = page("time")

for phrase in (
    "How is profit margin calculated?",
    "gross margin is 40% of sales",
    "operating margin is 25% of sales",
    "Does the EMI estimate include lender fees?",
    "fixed nominal annual rate",
    "Does the compound interest estimate include deposits or taxes?",
):
    assert phrase.lower() in money.lower(), ("money", phrase)

for phrase in (
    "What is 25% of 200?",
    "What is 1/2 + 1/3?",
    "How do I simplify a ratio?",
    "10:15",
    "2:3",
    "100:200:400",
    "1:2:4",
    "percentage difference",
    "25% of 200 is 50",
    "5/6",
    "Can I convert kilograms to pounds?",
    "Why can the denominator not be zero?",
):
    assert phrase.lower() in math.lower(), ("math", phrase)

for slug in ("percentage-calculator", "percentage-difference-calculator", "ratio-calculator", "fraction-calculator"):
    assert f'href="/{slug}/"' in math, slug
assert 'href="/calorie-calculator/"' in page("health"), "Health hub must link to the adult calorie calculator"
health_html = page("health")
health_description = re.search(r'<meta name="description" content="([^"]+)"', health_html)
assert health_description, "Health hub must have a meta description"
assert 120 <= len(health_description.group(1)) <= 160, "Health hub meta description should use its available search snippet space"
assert "worked examples" in health_description.group(1).lower(), "Health hub description should accurately mention its worked examples"
assert 'href="/compound-interest-calculator/"' in money
for phrase in (
    "calculate age from calendar dates",
    "find the days between two dates",
    "convert years to days with a 365-day year, the Gregorian average or an exact start-date method",
    "convert days to years using a selected year length",
    "Query Calculator also answers supported date, month and time-conversion questions",
):
    assert phrase.lower() in time.lower(), ("time", phrase)

years_to_days = (Path("public") / "years-to-days-calculator" / "index.html").read_text(encoding="utf-8")
title_line = next((line for line in years_to_days.splitlines() if "<title>" in line), "")
assert "<title>Years to Days Calculator | How Many Days in X Years?</title>" in title_line, "Years-to-days title should name both supported conversion directions"
description_line = next((line for line in years_to_days.splitlines() if '<meta name="description"' in line), "")
assert "Convert years to days or days to years using 365, 365.25 or 365.2425-day methods." in description_line and "Use a start date for exact Gregorian calendar days." in description_line, "Years-to-days metadata must describe all three methods and both result modes"
assert "Exact calendar years (years to days only)" in years_to_days, "Years-to-days UI must keep the exact-mode direction limitation visible"

print("Money, Math and Time hub content, canonical/indexability and contextual links verified")
