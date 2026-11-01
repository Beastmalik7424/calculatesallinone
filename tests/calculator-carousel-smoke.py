from pathlib import Path
import re

ROOT = Path("public")
ENGLISH_TOOLS = {
    "zakat-calculator", "bmi-calculator", "profit-loss-calculator",
    "discount-calculator", "age-calculator", "unit-converter",
    "standard-calculator", "tasbih-counter", "stopwatch",
    "years-to-days-calculator", "query-calculator", "emi-calculator",
    "percentage-calculator", "fraction-calculator",
    "compound-interest-calculator", "date-calculator",
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
    assert found == ENGLISH_TOOLS, (
        f"Carousel must expose all 16 calculator destinations on {path}. "
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

# Every shipped language homepage must render all 16 calculator names in its own language.
LANGUAGE_LABELS = {
    "ar": ["حاسبة تحويل السنوات إلى أيام", "حاسبة الاستعلام", "حاسبة الأقساط", "حاسبة النسبة المئوية", "حاسبة الكسور", "حاسبة الفائدة المركبة", "حاسبة الفرق بين التواريخ"],
    "hi": ["वर्ष से दिन कैलकुलेटर", "क्वेरी कैलकुलेटर", "ईएमआई कैलकुलेटर", "प्रतिशत कैलकुलेटर", "भिन्न कैलकुलेटर", "चक्रवृद्धि ब्याज कैलकुलेटर", "तिथि अंतर कैलकुलेटर"],
    "es": ["Calculadora de años a días", "Calculadora de consultas", "Calculadora de EMI", "Calculadora de porcentajes", "Calculadora de fracciones", "Calculadora de interés compuesto", "Calculadora de diferencia de fechas"],
    "fr": ["Calculatrice années en jours", "Calculatrice de requêtes", "Calculatrice EMI", "Calculatrice de pourcentage", "Calculatrice de fractions", "Calculatrice d’intérêts composés", "Calculatrice de différence de dates"],
}
for lang, required_labels in LANGUAGE_LABELS.items():
    markup = output_for("/" + lang + "/")
    group = primary_group(markup, "/" + lang + "/")
    found = set(re.findall(r'data-tool-shortcut="([^"]+)"', group))
    assert found == ENGLISH_TOOLS, f"{lang} carousel must include all 16 calculators"
    for label in required_labels:
        assert label in group, f"{lang} carousel missing translated full calculator name: {label}"

urdu_home = output_for("/ur/")
urdu_home_group = primary_group(urdu_home, "/ur/")
urdu_found = set(re.findall(r'data-tool-shortcut="([^"]+)"', urdu_home_group))
assert urdu_found == ENGLISH_TOOLS, "Urdu carousel must show all 16 calculators, including tools without Urdu pages"
assert 'href="/years-to-days-calculator/"' in urdu_home_group, "Untranslated Urdu tool destinations must safely fall back to their existing English pages"
assert "سال سے دن کیلکولیٹر" in urdu_home_group, "Urdu carousel must still show the Urdu calculator name"

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
assert "@keyframes ca-calculator-marquee" in css, "Calculator shortcuts must auto-slide"
assert ".ca-calculator-carousel:focus-within" in css, "Keyboard focus must pause the moving carousel"
assert "prefers-reduced-motion" in css and ".ca-calculator-track" in css, (
    "Reduced-motion users must get a non-animated, manually scrollable carousel"
)
assert "#t-tap" in css and "min-height:48px" in css, (
    "Tasbih Count one button must retain a visible, accessible touch target"
)

print("Calculator carousel, active links, reduced-motion support and Tasbih action smoke tests PASS")
