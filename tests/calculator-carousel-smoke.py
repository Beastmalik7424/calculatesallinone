from pathlib import Path
import re

ROOT = Path("public")
ENGLISH_TOOLS = {
    "zakat-calculator", "bmi-calculator", "profit-loss-calculator",
    "discount-calculator", "age-calculator", "unit-converter",
    "standard-calculator", "tasbih-counter", "stopwatch",
    "years-to-days-calculator", "query-calculator", "emi-calculator",
    "percentage-calculator", "fraction-calculator",
    "compound-interest-calculator", "date-calculator", "calorie-calculator",
}


def output_for(path):
    parts = [part for part in path.strip("/").split("/") if part]
    target = ROOT.joinpath(*parts, "index.html") if parts else ROOT / "index.html"
    assert target.is_file(), f"Missing generated page: {path}"
    return target.read_text(encoding="utf-8")


def primary_group(markup, path):
    assert 'class="ca-calculator-carousel"' in markup, f"Calculator carousel missing on {path}"
    assert 'data-tool-set="primary"' in markup, f"Primary calculator link group missing on {path}"
    match = re.search(
        r'<div class="ca-calculator-group" data-tool-set="primary">(.*?)</div>',
        markup, re.S
    )
    assert match, f"Could not locate primary calculator group on {path}"
    return match.group(1)


for path in ("/", "/bmi-calculator/", "/tasbih-counter/", "/percentage-calculator/", "/emi-calculator/"):
    markup = output_for(path)
    group = primary_group(markup, path)
    found = set(re.findall(r'data-tool-shortcut="([^"]+)"', group))
    first_shortcut = re.search(r'data-tool-shortcut="([^"]+)"', group)
    assert first_shortcut and first_shortcut.group(1) == "calorie-calculator", (
        f"Adult Calorie Calculator must be the first visible carousel shortcut on {path}"
    )
    assert found == ENGLISH_TOOLS, (
        f"Carousel must expose all 17 calculator destinations on {path}. "
        f"Missing={sorted(ENGLISH_TOOLS-found)}, extra={sorted(found-ENGLISH_TOOLS)}"
    )
    if path == "/emi-calculator/":
        assert '<nav aria-label="Main" class="site-nav">' in markup, "EMI carousel must reuse the existing site navigation row"
    else:
        assert '<header' in markup and '</header>' in markup
        header = markup.split("</header>", 1)[0]
        assert 'class="ca-calculator-carousel"' in header, (
            f"Carousel must stay inside the existing header so it does not push calculator content down: {path}"
        )
    if path != "/":
        slug = path.strip("/").split("/")[-1]
        assert re.search(
            r'data-tool-shortcut="' + re.escape(slug) + r'"[^>]*aria-current="page"',
            group
        ), f"Current calculator must be visibly and accessibly active on {path}"

# Every shipped language homepage must render all 17 calculator names in its own language.
LANGUAGE_LABELS = {
    "ar": ["حاسبة تحويل السنوات إلى أيام", "حاسبة الاستعلام", "حاسبة الأقساط", "حاسبة النسبة المئوية", "حاسبة الكسور", "حاسبة الفائدة المركبة", "حاسبة الفرق بين التواريخ", "حاسبة السعرات الحرارية للبالغين"],
    "hi": ["वर्ष से दिन कैलकुलेटर", "क्वेरी कैलकुलेटर", "ईएमआई कैलकुलेटर", "प्रतिशत कैलकुलेटर", "भिन्न कैलकुलेटर", "चक्रवृद्धि ब्याज कैलकुलेटर", "तिथि अंतर कैलकुलेटर", "वयस्क कैलोरी कैलकुलेटर"],
    "es": ["Calculadora de años a días", "Calculadora de consultas", "Calculadora de EMI", "Calculadora de porcentajes", "Calculadora de fracciones", "Calculadora de interés compuesto", "Calculadora de diferencia de fechas", "Calculadora de calorías para adultos"],
    "fr": ["Calculatrice années en jours", "Calculatrice de requêtes", "Calculatrice EMI", "Calculatrice de pourcentage", "Calculatrice de fractions", "Calculatrice d’intérêts composés", "Calculatrice de différence de dates", "Calculateur de calories pour adultes"],
}
for lang, required_labels in LANGUAGE_LABELS.items():
    markup = output_for("/" + lang + "/")
    assert 'data-tool-set="duplicate"' in markup, f"{lang} homepage must retain the moving carousel duplicate"
    group = primary_group(markup, "/" + lang + "/")
    found = set(re.findall(r'data-tool-shortcut="([^"]+)"', group))
    assert found == ENGLISH_TOOLS, f"{lang} carousel must include all 17 calculators"
    for label in required_labels:
        assert label in group, f"{lang} carousel missing translated full calculator name: {label}"

urdu_home = output_for("/ur/")
urdu_home_group = primary_group(urdu_home, "/ur/")
urdu_found = set(re.findall(r'data-tool-shortcut="([^"]+)"', urdu_home_group))
assert urdu_found == ENGLISH_TOOLS, "Urdu carousel must show all 17 calculators, including tools without Urdu pages"
assert 'href="/years-to-days-calculator/"' in urdu_home_group, "Untranslated Urdu tool destinations must safely fall back to their existing English pages"
assert "سال سے دن کیلکولیٹر" in urdu_home_group, "Urdu carousel must still show the Urdu calculator name"
assert "بالغ افراد کا کیلوری کیلکولیٹر" in urdu_home_group, "Urdu carousel must include the adult calorie calculator"

urdu = output_for("/ur/tasbih-counter/")
urdu_group = primary_group(urdu, "/ur/tasbih-counter/")
assert 'data-tool-shortcut="tasbih-counter"' in urdu_group
assert re.search(
    r'data-tool-shortcut="tasbih-counter"[^>]*aria-current="page"',
    urdu_group
), "Urdu Tasbih page must highlight its own calculator shortcut"

tasbih = output_for("/tasbih-counter/")
assert 'id="t-tap"' in tasbih, "Tasbih Count one action must remain in generated HTML"
css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
homepage_markup = output_for("/")
zakat_markup = output_for("/zakat-calculator/")
assert 'data-tool-set="duplicate"' in homepage_markup, "Homepage must retain its moving carousel for the existing calculator-first layout"
assert 'data-tool-set="duplicate"' not in zakat_markup, "Zakat pages must use one stable shortcut row without duplicate marquee links"
assert 'data-tool-set="duplicate"' not in tasbih, "Unrelated inner calculator pages must retain their existing single shortcut group"
assert "@keyframes ca-calculator-marquee" in css, "The shared calculator ticker animation must remain available on unaffected pages"
assert re.search(r"\\.ca-calculator-track\\s*\\{[^}]*animation:\\s*ca-calculator-marquee\\s+48s\\s+linear\\s+infinite", css), "Unaffected calculator pages must retain the shared continuous ticker animation"
zakat_track_overrides = re.findall(r"body:has\\(#main \\.ca-tool-zakat-calculator\\) \\.ca-calculator-track\\{([^}]*)\\}", css)
assert zakat_track_overrides and all("animation:none" in rule and "transform:none" in rule for rule in zakat_track_overrides), "Zakat pages must use a stable, non-moving shortcut track"
zakat_link_overrides = re.findall(r"body:has\\(#main \\.ca-tool-zakat-calculator\\) \\.ca-calculator-link\\{([^}]*)\\}", css)
assert zakat_link_overrides and all("min-height:44px" in rule and "height:44px" in rule for rule in zakat_link_overrides), "Zakat shortcut links must meet the 44px touch-target design target"
assert "theme-toggle" in zakat_markup and zakat_markup.index('id="theme-toggle"') < zakat_markup.index('class="ca-calculator-carousel"'), "Theme control must remain in the upper header row"
assert "ca-site-nav-topline" in zakat_markup, "Header must keep its separate top controls row"
assert "#t-tap" in css and "min-height:48px" in css, "Tasbih Count one button must retain a visible, accessible touch target"
print("Calculator ticker, all 17 destinations, inner-page header layout and Tasbih action smoke tests PASS")

assert '<link rel="stylesheet" href="/assets/site.css?v=20261118-zakat-mobile-ticker-v4">' in zakat_markup, "Zakat pages must use the current cache-busted stylesheet URL"
assert zakat_markup.count('data-tool-set="primary"') == 1 and 'data-tool-set="duplicate"' not in zakat_markup, "Zakat pages must render one non-duplicated shortcut group"
zakat_group = primary_group(zakat_markup, "/zakat-calculator/")
current_zakat = re.search(r'data-tool-shortcut="zakat-calculator"[^>]*aria-current="page"', zakat_group)
first_calorie = re.search(r'data-tool-shortcut="calorie-calculator"', zakat_group)
assert current_zakat and first_calorie and current_zakat.start() < first_calorie.start(), "Current Zakat shortcut must appear first"
assert re.search(r'<input id="z-stock"[^>]*autocomplete="off"', zakat_markup), "Financial trade-stock input must disable browser autofill"
