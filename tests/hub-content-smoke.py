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
    schemas = [json.loads(raw) for raw in re.findall(r'<script type="application/ld\\+json">(.*?)</script>', html, re.S)]
    nodes = [node for item in schemas for node in (item.get("@graph", []) if isinstance(item, dict) and "@graph" in item else [item])]
    crumbs = [node for node in nodes if node.get("@type") == "BreadcrumbList"]
    assert len(crumbs) == 1, f"Expected one BreadcrumbList on /{slug}/"
    items = crumbs[0].get("itemListElement", [])
    assert len(items) == 2 and items[0].get("item") == "https://calculateallinone.vercel.app/" and items[1].get("item") == f"https://calculateallinone.vercel.app/{slug}/", f"Invalid breadcrumb schema on /{slug}/"
    return html

money = page("money")
math = page("math")

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
    "25% of 200 is 50",
    "5/6",
    "Can I convert kilograms to pounds?",
    "Why can the denominator not be zero?",
):
    assert phrase.lower() in math.lower(), ("math", phrase)

for slug in ("percentage-calculator", "fraction-calculator"):
    assert f'href="/{slug}/"' in math, slug
assert 'href="/compound-interest-calculator/"' in money
print("Money and Math hub content, canonical/indexability and contextual links verified")
