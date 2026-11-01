from pathlib import Path
import re

def page(slug):
    path = Path("public") / slug / "index.html"
    assert path.is_file(), f"Missing generated /{slug}/ page"
    html = path.read_text(encoding="utf-8")
    assert re.search(r'<link rel="canonical" href="https://calculateallinone\\.vercel\\.app/' + slug + r'/">', html), slug
    assert re.search(r'<meta name="robots" content="index, follow">', html), slug
    return html

money = page("money")
math = page("math")

for phrase in (
    "How is profit margin calculated?",
    "40% gross margin",
    "25% operating margin",
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
