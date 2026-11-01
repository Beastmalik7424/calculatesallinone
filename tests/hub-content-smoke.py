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
worship = page("worship")
for phrase in (
    "Choose a target of 33, 99 or 100",
    "custom whole-number target from 1 to 10,000",
    "If storage is blocked, the counter works in memory only until you leave or reload the page.",
):
    assert phrase.lower() in worship.lower(), ("worship", phrase)

for stale_phrase in ("33, 100 or 1000", "choose unlimited"):
    assert stale_phrase not in worship.lower(), ("stale tasbih instructions", stale_phrase)

description = re.search(r'<meta name="description" content="([^"]+)"', worship)
assert description and "count, phrase and target are stored locally when browser storage is available" in description.group(1).lower(), "Worship hub metadata must describe storage conditionally"

home = (Path("public") / "index.html").read_text(encoding="utf-8")
assert "33, 99, 100 or custom targets and local count storage when available" in home.lower(), "Homepage worship card must describe the real targets and conditional storage"

tasbih = (Path("public") / "tasbih-counter" / "index.html").read_text(encoding="utf-8")
assert "Custom target (1 to 10,000)" in tasbih, "Tasbih calculator custom target range changed without updating the hub"
for preset in ("33", "99", "100"):
    assert preset in tasbih, f"Tasbih calculator preset {preset} is missing"

print("Money and Math hub content, canonical/indexability and contextual links verified")
