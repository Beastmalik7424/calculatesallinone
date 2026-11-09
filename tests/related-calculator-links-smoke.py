from pathlib import Path

# Keep internal recommendations tightly related to the task on each calculator page.
checks = {
    "tasbih-counter": ["stopwatch", "zakat-calculator"],
    "profit-loss-calculator": ["discount-calculator", "percentage-calculator", "emi-calculator", "compound-interest-calculator"],
    "discount-calculator": ["percentage-calculator", "profit-loss-calculator"],
    "standard-calculator": ["percentage-calculator", "fraction-calculator"],
    "age-calculator": ["date-calculator", "years-to-days-calculator"],
    "years-to-days-calculator": ["date-calculator", "age-calculator", "query-calculator", "unit-converter"],
    "query-calculator": ["years-to-days-calculator", "age-calculator"],
}
for page, slugs in checks.items():
    html = (Path("public") / page / "index.html").read_text(encoding="utf-8")
    assert '<h2 class="text-xl font-semibold text-stone-900 dark:text-stone-100">Related calculators</h2>' in html, page
    for slug in slugs:
        assert f'href="/{slug}/"' in html, (page, slug)
        assert (Path("public") / slug / "index.html").exists(), slug

for page, slugs in {
    "percentage-calculator": ["percentage-difference-calculator", "ratio-calculator"],
    "percentage-difference-calculator": ["percentage-calculator", "standard-calculator", "fraction-calculator", "ratio-calculator"],
    "ratio-calculator": ["percentage-calculator", "percentage-difference-calculator", "fraction-calculator"],
}.items():
    html = (Path("public") / page / "index.html").read_text(encoding="utf-8")
    assert '<nav aria-label="Related calculators"' in html, page
    for slug in slugs:
        assert f'href="/{slug}/"' in html, (page, slug)
        assert (Path("public") / slug / "index.html").exists(), slug

# Pages without a genuinely related tool must not receive unrelated generic recommendations.
for page in ("bmi-calculator", "zakat-calculator", "stopwatch", "unit-converter"):
    html = (Path("public") / page / "index.html").read_text(encoding="utf-8")
    assert "Related calculators" not in html, page

# The homepage and category hubs continue to expose all core journeys.
for page, slugs in {
    "/": ["percentage-calculator", "fraction-calculator", "compound-interest-calculator", "date-calculator"],
    "/math/": ["percentage-calculator", "percentage-difference-calculator", "ratio-calculator", "fraction-calculator"],
    "/money/": ["compound-interest-calculator"],
    "/time/": ["date-calculator"],
}.items():
    html = (Path("public") / page.strip("/") / "index.html").read_text(encoding="utf-8")
    for slug in slugs:
        assert f'href="/{slug}/"' in html, (page, slug)
print("Curated related-calculator links and hub journeys verified")
