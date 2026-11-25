from pathlib import Path
import hashlib
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
assert 'data-tool-set="duplicate"' not in zakat_markup, "Zakat ticker must match the Standard Calculator page (single group, no duplicate marquee)"
assert 'data-tool-set="duplicate"' not in tasbih, "Unrelated inner calculator pages must retain their existing single shortcut group"
assert "@keyframes ca-calculator-marquee" in css, "The homepage marquee animation must remain available"
base_track_rules = re.findall(r"(?:^|})\.ca-calculator-track\{([^}]*)\}", css)
assert base_track_rules and all("animation:" not in rule for rule in base_track_rules), "Single-group inner-page tickers must not run the two-group marquee animation"
duplicate_group_track_overrides = re.findall(r'body:has\(\.ca-calculator-group\[data-tool-set="duplicate"\]\) \.ca-calculator-track\s*\{([^}]*)\}', css)
assert any("animation:ca-calculator-marquee 48s linear infinite" in rule for rule in duplicate_group_track_overrides), "Only pages with a duplicate visual group may run the continuous marquee"
standard_markup = output_for("/standard-calculator/")
assert 'data-tool-set="duplicate"' not in standard_markup, "Standard Calculator must retain its single-group shortcut ticker"
emi_markup = output_for("/emi-calculator/")
assert 'data-tool-set="duplicate"' in emi_markup, "EMI page must retain its duplicate group for continuous marquee motion"
zakat_track_overrides = re.findall(r"body:has\(#main \.ca-tool-zakat-calculator\) \.ca-calculator-track\{([^}]*)\}", css)
assert any("animation:none" in rule and "transform:none" in rule for rule in zakat_track_overrides), "Single-group Zakat tickers must stay stationary and scrollable"
zakat_carousel_overrides = re.findall(r"body:has\(#main \.ca-tool-zakat-calculator\) \.ca-calculator-carousel\s*\{([^}]*)\}", css)
assert any("overflow-x:auto" in rule and "overflow-y:hidden" in rule for rule in zakat_carousel_overrides), "Zakat shortcut links must remain reachable by horizontal scrolling"
zakat_link_overrides = re.findall(r"body:has\(#main \.ca-tool-zakat-calculator\) \.ca-calculator-link\{([^}]*)\}", css)
assert zakat_link_overrides and all("min-height:44px" in rule and "height:44px" in rule for rule in zakat_link_overrides), "Zakat shortcut links must meet the 44px touch-target design target"
assert "theme-toggle" in zakat_markup and zakat_markup.index('id="theme-toggle"') < zakat_markup.index('class="ca-calculator-carousel"'), "Theme control must remain in the upper header row"
assert "ca-site-nav-topline" in zakat_markup, "Header must keep its separate top controls row"
assert "#t-tap" in css and "min-height:48px" in css, "Tasbih Count one button must retain a visible, accessible touch target"
print("Calculator ticker, all 17 destinations, inner-page header layout and Tasbih action smoke tests PASS")

css_version = hashlib.sha256((ROOT / "assets" / "site.css").read_bytes()).hexdigest()[:16]
assert f'<link rel="stylesheet" href="/assets/site.css?v={css_version}">' in zakat_markup, "Zakat pages must use the content-hash version of the deployed stylesheet"
assert zakat_markup.count('data-tool-set="primary"') == 1 and zakat_markup.count('data-tool-set="duplicate"') == 0, "Zakat pages must render one primary ticker group, like the Standard Calculator page"
zakat_group = primary_group(zakat_markup, "/zakat-calculator/")
current_zakat = re.search(r'data-tool-shortcut="zakat-calculator"[^>]*aria-current="page"', zakat_group)
first_calorie = re.search(r'data-tool-shortcut="calorie-calculator"', zakat_group)
assert current_zakat and first_calorie and first_calorie.start() < current_zakat.start(), "Zakat ticker must retain the shared default calculator order and mark the current page"
assert re.search(r'<input id="z-stock"[^>]*autocomplete="off"', zakat_markup), "Financial trade-stock input must disable browser autofill"
zakat_amount_inputs = re.findall(r'<input id="z-[^"]+"[^>]*type="number"[^>]*>', zakat_markup)
assert zakat_amount_inputs and all('autocomplete="off"' in item for item in zakat_amount_inputs), "Every financial amount input must explicitly disable inappropriate browser autofill"
assert "body:has(#main .ca-tool-zakat-calculator) #main" in css, "Zakat content must sit on a solid contrast-checkable surface"
assert "html.dark body:has(#main .ca-tool-zakat-calculator) #main" in css, "Dark-mode Zakat content must retain a solid contrast-checkable surface"
assert "body:has(#main .ca-tool-zakat-calculator) header" in css and "body:has(#main .ca-tool-zakat-calculator) footer" in css, "Zakat header and footer must use opaque surfaces for reliable contrast"
assert "body:has(#main .ca-tool-zakat-calculator) #main>h1" in css, "Zakat page title must use a solid text color instead of gradient-clipped text"
assert "bg-teal-700 hover:bg-teal-800 dark:bg-teal-700" in zakat_markup, "Zakat calculate action must match the Standard Calculator teal action palette"
assert "bg-gradient-to-r from-sky-700 to-indigo-700" not in zakat_markup, "Zakat calculate action must not rely on an unmeasured gradient contrast"
