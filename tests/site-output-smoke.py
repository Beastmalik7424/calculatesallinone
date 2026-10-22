import html as html_lib
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
xml = ET.parse(ROOT / "sitemap.xml").getroot()
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [node.find("sm:loc", ns).text for node in xml.findall("sm:url", ns)]
sitemap_urls = set(urls)
titles = {}
descriptions = {}
assert urls, "Sitemap has no URLs"
assert SITE + "/emi-calculator/" in set(urls), "The live EMI calculator must be included in the XML sitemap"
assert len(urls) == len(set(urls)), "Duplicate URLs found in sitemap"
lastmod_entries = {
    node.find("sm:loc", ns).text: node.find("sm:lastmod", ns).text
    for node in xml.findall("sm:url", ns)
    if node.find("sm:lastmod", ns) is not None
}
assert set(lastmod_entries) <= set(urls), "Sitemap lastmod entries must refer only to listed URLs"
assert all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) for value in lastmod_entries.values()), (
    "Sitemap lastmod values must use YYYY-MM-DD format."
)
expected_lastmod_entries = {
    SITE + "/contact/": "2026-10-21",
    SITE + "/discount-calculator/": "2026-10-21",
    SITE + "/editorial-policy/": "2026-10-21",
    SITE + "/health/": "2026-10-21",
}
assert lastmod_entries == expected_lastmod_entries, (
    "Only the four scoped pages with verified content/template updates may carry lastmod dates. "
    f"Expected {expected_lastmod_entries!r}, got {lastmod_entries!r}"
)
def output_for_url(url):
    parsed = urlparse(url)
    assert parsed.scheme == "https" and parsed.netloc == urlparse(SITE).netloc, f"Unexpected sitemap host: {url}"
    path = parsed.path.strip("/")
    return ROOT / path / "index.html" if path else ROOT / "index.html"
# The standalone EMI page must use the shared SVG favicon instead of triggering a missing /favicon.ico request.
emi_html = output_for_url(SITE + "/emi-calculator/").read_text(encoding="utf-8")
assert '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">' in emi_html, "EMI calculator must use the site's existing favicon asset"
# Category hubs are indexable when their explanatory sections and tool links are present.
for hub in ("/money/", "/health/", "/math/", "/time/", "/worship/"):
    assert SITE + hub in sitemap_urls, f"Substantive category hub should be indexable: {hub}"
# Localized homepages remain noindex until their translated tool journeys receive competent review.
for locale_home in ("/ar/", "/hi/", "/es/", "/fr/", "/ur/"):
    locale_file = ROOT / locale_home.strip("/") / "index.html"
    assert locale_file.is_file(), f"Localized homepage missing: {locale_home}"
    locale_html = locale_file.read_text(encoding="utf-8")
    assert 'name="robots" content="noindex, follow"' in locale_html, f"Unreviewed localized homepage must stay noindex: {locale_home}"
    assert SITE + locale_home not in sitemap_urls, f"Unreviewed localized homepage must not be in sitemap: {locale_home}"
for url in urls:
    page = output_for_url(url)
    assert page.is_file(), f"Sitemap URL has no generated HTML: {url} -> {page}"
    html = page.read_text(encoding="utf-8")
    assert "Last reviewed: 2026-10-18" not in html and "آخری جائزہ: 2026-10-18" not in html, f"Unverified blanket review date remains: {url}"
    title_match = re.search(r"<title>([^<]+)</title>", html)
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
    assert title_match, f"Missing title: {url}"
    assert desc_match, f"Missing description: {url}"
    titles[url] = title_match.group(1)
    descriptions[url] = desc_match.group(1)
    assert 70 <= len(descriptions[url]) <= 160, f"Meta description length outside 70-160 characters: {url} ({len(descriptions[url])})"
    assert "Review the formula, worked example and limits before relying on the result" not in descriptions[url], f"Generic irrelevant metadata appended: {url}"
    if url == SITE + "/profit-loss-calculator/":
        assert title_match.group(1) == "Profit and Loss Calculator | CalculatesAll", (
            "Profit and Loss title must be complete and descriptive."
        )
    assert html.count("<h1") == 1, f"Expected exactly one primary heading: {url}"
    assert f'<link rel="canonical" href="{url}">' in html, f"Canonical mismatch: {url}"
    assert '<meta name="robots" content="index, follow">' in html, f"Page not indexable: {url}"
# Important calculator controls need stable form names for native form semantics and progressive fallback.
age_html = output_for_url(SITE + "/age-calculator/").read_text(encoding="utf-8")
assert 'id="a-dob" name="dob" type="date"' in age_html, "Age input must expose a stable form name"
bmi_html = output_for_url(SITE + "/bmi-calculator/").read_text(encoding="utf-8")
for control_name in ("bmi-height-unit", "bmi-weight-unit", "b-kg", "b-lb", "b-cm", "b-ft", "b-in"):
    assert 'name="' + control_name + '"' in bmi_html, f"BMI control missing form name: {control_name}"
assert 'id="bmi-height-cm"' in bmi_html and 'id="bmi-height-ftin"' in bmi_html, "BMI height mode radios are required"
assert 'id="b-kg-error"' in bmi_html and 'aria-describedby="b-cm-error"' in bmi_html, "BMI fields need associated error messages"
assert 'id="b-ft" name="b-ft"' in bmi_html and 'type="text" inputmode="numeric" pattern="[0-9]+"' in bmi_html, "Feet input must preserve raw text for strict validation"
assert 'id="b-kg" name="b-kg"' in bmi_html and 'type="text" inputmode="decimal" pattern="[0-9]+([.][0-9]+)?"' in bmi_html, "Weight input must preserve raw text for strict validation"
assert 'id="b-lb"' in bmi_html and 'id="bmi-weight-lb"' in bmi_html, "Target BMI page must offer pounds alongside kilograms"
assert "<title>BMI Calculator for Adults | cm or ft/in | CalculatesAll</title>" in bmi_html, "BMI title must be complete and unique"
assert "BMI is a general screening tool. It does not measure body fat directly and does not replace advice from a doctor." in bmi_html, "English BMI disclaimer must be visible in page content"
assert "Weight can be entered in kilograms (kg) or pounds (lb), independently of the height unit." in bmi_html, "English BMI guide must document independent weight units"
urdu_bmi_html = output_for_url(SITE + "/ur/bmi-calculator/").read_text(encoding="utf-8")
for control_name in ("bmi-height-unit", "bmi-weight-unit", "b-kg", "b-lb", "b-cm", "b-ft", "b-in"):
    assert 'name="' + control_name + '"' in urdu_bmi_html, f"Urdu BMI control missing form name: {control_name}"
assert 'id="b-lb"' in urdu_bmi_html and 'id="bmi-weight-lb"' in urdu_bmi_html, "Urdu BMI page must offer pounds alongside kilograms"
assert "BMI ایک عمومی اسکریننگ پیمانہ ہے" in urdu_bmi_html, "Urdu BMI disclaimer is required"
# RTL dropdown must anchor to the left edge and stay within viewport bounds.
assert 'class="absolute left-0 right-auto mt-2 w-64 max-w-[calc(100vw-2rem)] overflow-x-hidden break-words' in urdu_bmi_html, "Urdu RTL tools menu must use left anchoring and bounded width"
assert 'style="max-width:calc(100vw - 2rem);overflow-wrap:anywhere;box-sizing:border-box"' in urdu_bmi_html, "Urdu tools menu must prevent viewport overflow"
english_menu_html = output_for_url(SITE + "/bmi-calculator/").read_text(encoding="utf-8")
assert 'class="absolute right-0 mt-2 w-64 max-w-[calc(100vw-2rem)] overflow-x-hidden break-words' in english_menu_html, "English tools menu must retain right anchoring and bounded width"
assert len(titles.values()) == len(set(titles.values())), "Duplicate page titles found: " + repr(titles)
assert len(descriptions.values()) == len(set(descriptions.values())), "Duplicate meta descriptions found: " + repr(descriptions)
# The root URL is the site homepage, not a duplicate Standard Calculator landing page.
home_url = SITE + "/"
assert titles[home_url].startswith("CalculatesAll |"), (
    "Homepage title must identify the site and its broad purpose, not a single calculator: " + titles[home_url]
)
assert "Standard Calculator" not in titles[home_url], (
    "Homepage title incorrectly targets the Standard Calculator page."
)
assert descriptions[home_url].startswith("Free online calculators for"), (
    "Homepage description should describe the site's main calculator/tool categories."
)
# Bing Webmaster ownership verification must be present in the delivered homepage head.
home_html = output_for_url(home_url).read_text(encoding="utf-8")
bing_tag = '<meta name="msvalidate.01" content="07D62A8BA67BA474B5A13A27E6770782" />'
head_match = re.search(r"<head\b[^>]*>(.*?)</head>", home_html, re.S | re.I)
body_match = re.search(r"<body\b", home_html, re.I)
assert head_match and body_match and head_match.start() < body_match.start(), (
    "Homepage must have a valid head before body for Bing verification."
)
assert home_html.count(bing_tag) == 1 and bing_tag in head_match.group(1), (
    "Bing verification meta tag must appear exactly once inside the homepage head."
)
# Homepage organization/entity signals and descriptive brand navigation must be machine-readable.
assert 'aria-label="CalculatesAll home page"' in home_html, "Brand link should describe its homepage destination"
assert 'href="mailto:' in home_html, "Homepage should expose a direct correction contact"
home_schemas = [
    json.loads(match.group(1))
    for match in re.finditer(r"""<script\b(?=[^>]*\btype=["']application/ld\+json["'])[^>]*>(.*?)</script>""", home_html, re.S | re.I)
]
organization_schema = next((schema for schema in home_schemas if schema.get("@type") == "Organization"), None)
assert organization_schema is not None, "Homepage Organization schema is required"
contact_point = organization_schema.get("contactPoint", {})
assert contact_point.get("@type") == "ContactPoint" and contact_point.get("email"), "Organization schema must expose the configured support email"
assert contact_point.get("url") == SITE + "/contact/", "Organization schema must link to the canonical contact page"
assert "612.36 grams" in home_html and "25.0 to 29.9" in home_html, "Homepage proof points must include the calculator method and WHO adult BMI ranges"
# The Urdu root is a localized site homepage, not a standard-calculator landing page.
urdu_home_url = SITE + "/ur/"
ur_home_html = output_for_url(urdu_home_url).read_text(encoding="utf-8")
if urdu_home_url in sitemap_urls:
    assert titles[urdu_home_url].startswith("CalculatesAll |"), (
        "Urdu homepage title must identify the site and its broad purpose: " + titles[urdu_home_url]
    )
    assert "معیاری کیلکولیٹر" not in titles[urdu_home_url], (
        "Urdu homepage title incorrectly targets only the standard calculator."
    )
    ur_home_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", ur_home_html, re.S)
    assert ur_home_h1 and "مفت آن لائن کیلکولیٹرز" in ur_home_h1.group(1), (
        "Urdu homepage H1 must describe the calculator collection."
    )
else:
    assert 'name="robots" content="noindex, follow"' in ur_home_html, (
        "Urdu homepage omitted from sitemap must be marked noindex."
    )
sitemap_urls = set(urls)
generated = set()
for page in ROOT.rglob("index.html"):
    rel = page.parent.relative_to(ROOT).as_posix()
    path = "/" + (rel + "/" if rel != "." else "")
    generated.add(SITE + path)
indexable_paths = [line.strip() for line in Path("indexable.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
noindex_paths = [line.strip() for line in Path("noindex.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
assert {SITE + path for path in indexable_paths} == sitemap_urls, "indexable.txt must exactly match sitemap URLs"
assert not ({SITE + path for path in noindex_paths} & sitemap_urls), "noindex URLs must not appear in sitemap"
assert {SITE + path for path in indexable_paths + noindex_paths} == generated, (
    "Manifest/page mismatch. Missing manifests: " + repr(sorted(generated - {SITE + path for path in indexable_paths + noindex_paths})) +
    "; unexpected manifest URLs: " + repr(sorted({SITE + path for path in indexable_paths + noindex_paths} - generated))
)
for path in noindex_paths:
    page_html = output_for_url(SITE + path).read_text(encoding="utf-8")
    assert 'name="robots" content="noindex, follow"' in page_html, "noindex manifest page lacks robots tag: " + path
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert "User-agent: *" in robots and "Allow: /" in robots
assert f"Sitemap: {SITE}/sitemap.xml" in robots
llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
assert llms.startswith("# CalculatesAll"), "Root llms.txt must be published as readable Markdown"
assert SITE + "/emi-calculator/" in llms, "llms.txt should reference the EMI calculator"
# Verify root-relative links point to generated pages or existing static assets.
broken = []
for page in ROOT.rglob("index.html"):
    html = page.read_text(encoding="utf-8")
    for href in re.findall(r'href="(/[^"]*)"', html):
        path = urlparse(href).path
        if path.startswith("/assets/"):
            target = ROOT / path.lstrip("/")
            if not target.is_file():
                broken.append((str(page), href))
        else:
            normalized = path.strip("/")
            target = ROOT / normalized / "index.html" if normalized else ROOT / "index.html"
            if not target.is_file():
                broken.append((str(page), href))
            elif path != "/" and not path.endswith("/"):
                broken.append((str(page), href + " (page URL missing trailing slash)"))
assert not broken, "Broken or non-canonical internal hrefs found: " + repr(broken[:20])
# Every indexable sitemap URL should have at least one crawlable incoming internal link.
# Count root-relative links; canonical tags are absolute and do not count as discovery links.
incoming = {url: set() for url in sitemap_urls}
for page in ROOT.rglob("index.html"):
    rel = page.parent.relative_to(ROOT).as_posix()
    source_url = SITE + "/" + (rel + "/" if rel != "." else "")
    html = page.read_text(encoding="utf-8")
    for href in re.findall(r'href="(/[^"]*)"', html):
        target = SITE + urlparse(href).path
        if target in incoming and target != source_url:
            incoming[target].add(source_url)
orphans = sorted(url for url, sources in incoming.items() if not sources)
assert not orphans, "Sitemap URLs without an incoming crawlable internal link: " + repr(orphans)
contact_html = (ROOT / "contact" / "index.html").read_text(encoding="utf-8")
assert 'href="mailto:' in contact_html, "Contact email must be a clickable mailto link"
# Verify local image/script asset references resolve in the generated output.
for page in ROOT.rglob("index.html"):
    html = page.read_text(encoding="utf-8")
    for src in re.findall(r'src="(/assets/[^"]+)"', html):
        target = ROOT / urlparse(src).path.lstrip("/")
        assert target.is_file(), f"Broken local asset reference in {page}: {src}"
for required in ("/marketplaces/", "/affiliate-disclosure/", "/about/", "/privacy/", "/contact/"):
    assert SITE + required in sitemap_urls, f"Required public page missing from sitemap: {required}"
vercel_config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
assert vercel_config.get("cleanUrls") is False, "Vercel cleanUrls must stay disabled so the Google ownership HTML file is served at its exact URL"
csp_header = next(item["value"] for item in vercel_config["headers"][0]["headers"] if item["key"] == "Content-Security-Policy")
connect_src = re.search(r"(?:^|;)\s*connect-src\s+([^;]+)", csp_header)
assert connect_src and all(host in connect_src.group(1).split() for host in ("https://ep1.adtrafficquality.google", "https://ep2.adtrafficquality.google")), (
    "CSP connect-src must allow only the exact Google Ad Traffic Quality endpoints observed in production."
)
script_src = re.search(r"(?:^|;)\s*script-src\s+([^;]+)", csp_header)
assert script_src and "https://ep2.adtrafficquality.google" in script_src.group(1).split(), (
    "CSP script-src must allow the exact Google Ad Traffic Quality script host observed in production."
)
frame_src = re.search(r"(?:^|;)\s*frame-src\s+([^;]+)", csp_header)
assert frame_src and "https://ep2.adtrafficquality.google" in frame_src.group(1).split(), (
    "CSP frame-src must allow the exact Google SODAR iframe host observed in production."
)
img_src = re.search(r"(?:^|;)\s*img-src\s+([^;]+)", csp_header)
assert img_src and "https://ep1.adtrafficquality.google" in img_src.group(1).split(), (
    "CSP img-src must allow the exact Google Ad Traffic Quality image host observed in production."
)
privacy_html = (ROOT / "privacy" / "index.html").read_text(encoding="utf-8")
marketplace_html = (ROOT / "marketplaces" / "index.html").read_text(encoding="utf-8")
assert "Ad slots are currently disabled" in privacy_html and "lightweight AdSense ownership meta tag is present" in privacy_html and "external AdSense JavaScript is not loaded" in privacy_html, "Privacy page must explain lightweight ownership verification and inactive ad loading"
assert "ADSENSE_CONSENT_READY=true" in privacy_html, "Privacy page must disclose the consent-readiness safeguard"
assert "Google-certified consent management platform" in privacy_html, "Privacy page must describe the CMP requirement"
assert "cookie identifiers" in privacy_html and "web beacons" in privacy_html and "IP addresses" in privacy_html, "Privacy page must disclose relevant advertising technologies/data"
assert "https://policies.google.com/technologies/partner-sites" in privacy_html, "Privacy page must link Google's data-use disclosure"
assert "https://policies.google.com/privacy" in privacy_html, "Privacy page must link Google's privacy policy"
assert "https://adssettings.google.com/" in privacy_html, "Privacy page must link Google's personalized-ad settings"
assert "https://optout.aboutads.info/" in privacy_html, "Privacy page must link an industry advertising opt-out resource"
assert "Third-party vendors, including Google, may use cookies" in privacy_html, "Privacy page must explain third-party advertising cookies"
assert "Available opt-out choices may not disable all advertising" in privacy_html, "Privacy page must not overpromise the effect of opt-out choices"
assert "publishes the matching ads.txt entry" in marketplace_html, "Marketplace guide must accurately describe the configured ads.txt entry"
# ads.txt must never contain a fabricated publisher ID or an entry unrelated to the configured account.
ads_path = ROOT / "ads.txt"
ads_client = os.environ.get("ADSENSE_CLIENT", "ca-pub-9453966537556063").strip()
if ads_client:
    assert re.fullmatch(r"ca-pub-\d{16}", ads_client), "ADSENSE_CLIENT must be a real-format AdSense publisher ID"
    expected_ads_line = "google.com, " + ads_client.removeprefix("ca-") + ", DIRECT, f08c47fec0942fa0"
    assert ads_path.is_file(), "Configured AdSense publisher ID requires a generated ads.txt"
    assert ads_path.read_text(encoding="utf-8").strip() == expected_ads_line, "ads.txt must match the configured publisher ID exactly"
else:
    assert not ads_path.exists(), "Do not generate ads.txt without the real AdSense publisher ID"
# Ad code must remain fail-closed unless all required deployment settings are present.
ads_slot = os.environ.get("ADSENSE_SLOT", "").strip()
consent_ready = os.environ.get("ADSENSE_CONSENT_READY", "").strip().lower() == "true"
ads_enabled = bool(ads_client and ads_slot.isdigit() and consent_ready)
all_generated_html = "\n".join(
    page.read_text(encoding="utf-8") for page in ROOT.rglob("index.html")
)
ads_script = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client="
if ads_client:
    assert '<meta name="google-adsense-account" content="' + ads_client + '">' in all_generated_html, "AdSense ownership meta tag must be present for the configured publisher ID"
if ads_enabled:
    assert ads_script + ads_client in all_generated_html, "Configured ads must load the matching publisher script"
else:
    assert "adsbygoogle.js" not in all_generated_html, "Do not load the external AdSense JavaScript while ads are disabled"
    assert 'class="adsbygoogle"' not in all_generated_html, "Ad slots must not render while monetization is disabled"
# Google Search Console ownership HTML must be present in the deployed output.
verification_file = ROOT / "google2e764d068684499b.html"
assert verification_file.is_file(), "Google Search Console verification file missing from Vercel output"
assert verification_file.read_text(encoding="utf-8").strip() == "google-site-verification: google2e764d068684499b.html", "Google Search Console verification file content mismatch"
# Urdu homepage visible UI must not leak English marketing labels or calculator aria labels.
for english_text in ("CALCULATE WITH CONFIDENCE", "ONE PLACE, MANY ANSWERS", "Marketplace guide", "Affiliate disclosure", 'aria-label="Open parenthesis"', 'aria-label="Divide"', 'aria-label="Square root"'):
    assert english_text not in ur_home_html, "English UI text remains on Urdu homepage: " + english_text
# Load the Urdu calculator output before checking its shared navigation and footer.
urdu_standard_html = (ROOT / "ur" / "standard-calculator" / "index.html").read_text(encoding="utf-8")
# Urdu calculator breadcrumbs and shared navigation/footer must use Urdu labels.
for english_text in ("Math and Converters", "Marketplace guide", "Affiliate disclosure", 'aria-label="Main"', 'aria-label="Footer"'):
    assert english_text not in urdu_standard_html, "English shared UI text remains on Urdu calculator: " + english_text
# Shared navigation and footer must be localized on every translated homepage.
localized_home_checks = {
    "ar": {
        "terms": "شروط الاستخدام", "marketplace": "دليل منصات البيع",
        "affiliate": "إفصاح الروابط التابعة", "main": 'aria-label="القائمة الرئيسية"',
        "footer": 'aria-label="تذييل الصفحة"',
    },
    "hi": {
        "terms": "उपयोग की शर्तें", "marketplace": "मार्केटप्लेस गाइड",
        "affiliate": "एफिलिएट प्रकटीकरण", "main": 'aria-label="मुख्य नेविगेशन"',
        "footer": 'aria-label="पाद लेख"',
    },
    "es": {
        "terms": "Términos de uso", "marketplace": "Guía de plataformas",
        "affiliate": "Divulgación de afiliación", "main": 'aria-label="Navegación principal"',
        "footer": 'aria-label="Pie de página"',
    },
    "fr": {
        "terms": "Conditions d’utilisation", "marketplace": "Guide des plateformes",
        "affiliate": "Divulgation d’affiliation", "main": 'aria-label="Navigation principale"',
        "footer": 'aria-label="Pied de page"',
    },
}
for locale, expected in localized_home_checks.items():
    localized_html = output_for_url(SITE + "/" + locale + "/").read_text(encoding="utf-8")
    for key, expected_text in expected.items():
        assert expected_text in localized_html, f"Missing localized {key} label on /{locale}/"
    for english_text in ("All tools", "Terms of use", "Marketplace guide", "Affiliate disclosure", 'aria-label="Main"', 'aria-label="Footer"'):
        assert english_text not in localized_html, f"English shared UI text remains on /{locale}/: {english_text}"
# Tool-menu labels on translated homepages must not fall back to English.
localized_tool_labels = {
    "ar": ("حاسبة الزكاة", "حاسبة مؤشر كتلة الجسم", "حاسبة العمر"),
    "hi": ("ज़कात कैलकुलेटर", "BMI कैलकुलेटर", "आयु कैलकुलेटर"),
    "es": ("Calculadora de Zakat", "Calculadora de IMC", "Calculadora de edad"),
    "fr": ("Calculatrice de Zakat", "Calculatrice d’IMC", "Calculatrice d’âge"),
}
english_tool_labels = (
    "Zakat Calculator", "BMI Calculator", "Profit and Loss Calculator",
    "Discount Calculator", "Age Calculator", "Unit Converter",
    "Standard Calculator", "Tasbih Counter", "Online Stopwatch",
)
for locale, labels in localized_tool_labels.items():
    localized_html = output_for_url(SITE + "/" + locale + "/").read_text(encoding="utf-8")
    for label in labels:
        assert ">" + label + "</a>" in localized_html, f"Missing localized tool label on /{locale}/: {label}"
    for label in english_tool_labels:
        assert ">" + label + "</a>" not in localized_html, f"English tool label remains in /{locale}/ menu: {label}"
# The Zakat page must not show an unfinished expert-review note when no reviewer is listed.
zakat_html = (ROOT / "zakat-calculator" / "index.html").read_text(encoding="utf-8")
assert "Subject expert review by a qualified scholar is pending." not in zakat_html, (
    "Do not expose the unfinished Zakat expert-review note to visitors."
)
# Urdu calculator UI controls must not retain English accessible labels.
for english_label in ("Open parenthesis", "Close parenthesis", "Delete last character", "Divide", "Multiply", "Subtract", "Add", "Square root"):
    assert 'aria-label="' + english_label + '"' not in urdu_standard_html, (
        "English calculator accessibility label remains on Urdu page: " + english_label
    )
# Per-page structured-data and language audit.
# Parse every JSON-LD block rather than only checking that a script tag exists.
for url in urls:
    page = output_for_url(url)
    html = page.read_text(encoding="utf-8")
    lang_match = re.search(r'<html lang="([^"]+)"', html)
    assert lang_match, f"Missing document language: {url}"
    page_lang = lang_match.group(1)
    jsonld_blocks = re.findall(r"""<script\b(?=[^>]*\btype=["']application/ld\+json["'])[^>]*>(.*?)</script>""", html, re.S | re.I)
    assert jsonld_blocks, f"Missing JSON-LD structured data: {url}"
    parsed_schemas = []
    for block in jsonld_blocks:
        try:
            parsed_schemas.append(json.loads(block))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Invalid JSON-LD on {url}: {exc}") from exc
    faq_schemas = [item for item in parsed_schemas if item.get("@type") == "FAQPage"]
    assert len(faq_schemas) <= 1, f"Duplicate FAQPage JSON-LD blocks on {url}: {len(faq_schemas)}"
    for faq_schema in faq_schemas:
        questions = faq_schema.get("mainEntity", [])
        assert questions and isinstance(questions, list), f"FAQPage must contain Question entities: {url}"
        for question in questions:
            name = question.get("name", "")
            answer = question.get("acceptedAnswer", {}).get("text", "")
            assert 1 <= len(name) <= 200, f"FAQ question name is empty or suspiciously long on {url}: {len(name)}"
            assert name.rstrip().endswith(("?", "؟")), f"FAQ question name must be a concise visible question on {url}: {name[:100]!r}"
            assert 1 <= len(answer) <= 3000, f"FAQ answer is empty or suspiciously long on {url}: {len(answer)}"
    if url == SITE + "/":
        assert len(faq_schemas) == 1, "Homepage must have one FAQPage schema"
        names = {item.get("name") for item in faq_schemas[0].get("mainEntity", [])}
        expected = {
            "Are the calculators free?",
            "Do you store the numbers I enter?",
            "Are the results accurate enough for important decisions?",
        }
        assert expected.issubset(names), f"Homepage FAQ schema must contain the concise visible questions: {expected - names}"
    if url.endswith("/emi-calculator/"):
        assert len(faq_schemas) == 1, "EMI page must have exactly one FAQPage schema generated from visible FAQ content"
        app_schemas = [item for item in parsed_schemas if item.get("@type") == "WebApplication"]
        assert len(app_schemas) == 1, "EMI page must retain exactly one WebApplication schema"
        assert app_schemas[0].get("url") == url, "EMI WebApplication schema URL must match its canonical URL"
        assert app_schemas[0].get("inLanguage") == page_lang, "EMI WebApplication schema language must match the HTML language"
    for item in parsed_schemas:
        if item.get("@type") == "WebPage":
            assert "dateModified" not in item, (
                f"Do not publish unverified dateModified on {url}."
            )
        if item.get("@type") in ("WebSite", "WebPage", "CollectionPage", "WebApplication"):
            if "inLanguage" in item:
                assert item.get("inLanguage") == page_lang, (
                f"Schema language mismatch on {url}: HTML={page_lang}, schema={item.get('inLanguage')}"
            )
    if url.endswith("/ur/"):
        websites = [x for x in parsed_schemas if x.get("@type") == "WebSite"]
        apps = [x for x in parsed_schemas if x.get("@type") == "WebApplication"]
        assert websites and websites[0].get("url") == url, "Urdu homepage WebSite schema URL must match its canonical URL"
        assert apps and apps[0].get("url") == url, "Urdu homepage WebApplication schema URL must match its canonical URL"
    if "/ur/" in url and url.rstrip("/").split("/")[-1] in {
        "zakat-calculator", "bmi-calculator", "profit-loss-calculator", "discount-calculator",
        "age-calculator", "unit-converter", "standard-calculator", "tasbih-counter", "stopwatch"
    }:
        assert any(x.get("@type") == "BreadcrumbList" for x in parsed_schemas), (
            f"Urdu calculator page missing BreadcrumbList schema: {url}"
        )
        assert 'aria-label="صفحہ کی ترتیب"' in html, f"Urdu calculator page missing visible breadcrumb: {url}"
# Verify explicit contrast styles for operation buttons survive the production CSS build.
site_css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
for selector in (
    '#main.max-w-3xl #calc-pad button[data-key="/"]',
    '#main.max-w-3xl #calc-pad button[data-key="="]',
):
    assert selector in site_css, f"Missing calculator contrast selector in built CSS: {selector}"
assert "background-color:#0f766e!important" in site_css, "Operator button background must be explicitly high-contrast"
assert "background-color:#0f172a!important" in site_css, "Equals button background must be explicitly high-contrast"
homepage_html = (ROOT / "index.html").read_text(encoding="utf-8")
assert "/assets/site.css?v=20261023-home-layout-fix-v2" in homepage_html, "Homepage must load the current calculator layout stylesheet"
assert ".ca-home-layout{display:grid" in site_css, "Homepage calculator layout must use the responsive single-column grid"
assert ".ca-home-layout{display:grid;grid-template-columns:minmax(0,1fr)!important" in site_css, "Desktop homepage must force tools below the calculator"
assert ".ca-home-side-left{display:none!important}" in site_css, "Homepage promotional sidebar must not push the calculator below the fold"
assert ".ca-home-calculator .ca-calculator-engine{width:100%;max-width:100%" in site_css, "Homepage calculator must use the available width"
# Every dynamic calculator message, unit label, category label, and theme label
# must be translated for all supported languages, not silently fall back to English.
# This checks source coverage at build time; browser tests separately verify rendered output.
app_js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
required_message_keys = (
    "zakatNoPrice", "zakatInput", "zakatBelow", "zakatHawl", "zakatDue",
    "bmiInput", "bmiInputImp", "bmiResult", "bmiUnder", "bmiNormal",
    "bmiOver", "bmiObese", "profitEnter", "profitWord", "lossWord",
    "profitNA", "profitPct", "ageEnter", "ageFuture", "ageCheck",
    "ageResult", "discInput", "discResult", "convEnter",
    "convAbsoluteZero", "convKelvin", "convNeg", "convResult",
    "calcError", "calcDiv", "calcSqrtNegative", "calcNeedValue",
    "tasbihNone", "tasbihReached", "tasbihLeft", "themeDark", "themeLight",
    "numeric", "units", "cats"
)
locale_order = ("en", "ur", "ar", "hi", "es", "fr")
locale_blocks = {}
for index, locale in enumerate(locale_order):
    start = app_js.find("    " + locale + ": {")
    assert start >= 0, f"Missing calculator message dictionary for locale {locale}"
    end = min(
        (position for next_locale in locale_order[index + 1:]
         if (position := app_js.find("    " + next_locale + ": {", start + 1)) >= 0),
        default=app_js.find("\n  }\n\n  var UNITS", start)
    )
    assert end > start, f"Could not isolate calculator message dictionary for locale {locale}"
    locale_blocks[locale] = app_js[start:end]
    for key in required_message_keys:
        assert re.search(r"\b" + re.escape(key) + r"\s*:", locale_blocks[locale]), (
            f"Locale {locale} is missing calculator message key: {key}"
        )
    for key in ("kg", "g", "lb", "oz", "m", "cm", "km", "ft", "in", "mi", "C", "F", "K"):
        assert re.search(r"\b" + re.escape(key) + r"\s*:", locale_blocks[locale]), (
            f"Locale {locale} is missing unit label: {key}"
        )
    for key in ("weight", "length", "temp"):
        assert re.search(r"\b" + key + r"\s*:", locale_blocks[locale]), (
            f"Locale {locale} is missing converter category label: {key}"
        )
assert 'var code = (document.documentElement.lang || "en").toLowerCase().split("-")[0]' in app_js, (
    "Calculator message selection must support language tags such as es-ES and fr-FR."
)
assert "Object.prototype.hasOwnProperty.call(MSG, code) ? code : \"en\"" in app_js, (
    "Unknown languages must safely fall back to English."
)
assert "eval(" not in app_js and "new Function" not in app_js, "Dynamic code execution found in app.js"
# The standalone EMI page must be discoverable through the main site and related calculators.
emi_html = (ROOT / "emi-calculator" / "index.html").read_text(encoding="utf-8")
assert '<link rel="canonical" href="https://calculateallinone.vercel.app/emi-calculator/">' in emi_html, "EMI canonical must use the slash URL"
assert '<a href="/">Browse all free calculators</a>' in emi_html, "EMI page must link back to the calculator hub"
for related in ("/zakat-calculator/", "/bmi-calculator/", "/discount-calculator/", "/profit-loss-calculator/", "/methodology/", "/about/"):
    assert 'href="' + related + '"' in emi_html, "EMI page is missing crawlable related link: " + related
assert 'aria-label="Related calculators"' in emi_html, "EMI related links must be grouped in a labelled navigation region"
# SEO/GEO content floor for indexable discovery pages. This intentionally excludes
# legal/privacy/contact disclosures, where padding copy to hit a word target would hurt clarity.
def visible_main_text(page_html):
    match = re.search(r"<main\b[^>]*>(.*?)</main>", page_html, re.S | re.I)
    assert match, "Indexable page is missing its main landmark"
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", match.group(1), flags=re.S | re.I)
    text = re.sub(r"<nav\b[^>]*>.*?</nav>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = html_lib.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", text).strip()
def content_words(text):
    return re.findall(r"[\w]+(?:['’][\w]+)?", text, flags=re.UNICODE)
excluded_short_pages = {"/privacy/", "/terms/", "/contact/", "/affiliate-disclosure/"}
content_floor_pages = [
    url for url in urls
    if urlparse(url).path not in excluded_short_pages
]
# Keep the Urdu homepage useful even while it remains noindex pending native-language review.
urdu_home_for_content = SITE + "/ur/"
if urdu_home_for_content not in content_floor_pages:
    content_floor_pages.append(urdu_home_for_content)
thin_pages = []
for url in content_floor_pages:
    page_html = output_for_url(url).read_text(encoding="utf-8")
    words = content_words(visible_main_text(page_html))
    if len(words) < 300:
        thin_pages.append((urlparse(url).path, len(words)))
assert not thin_pages, (
    "Indexable SEO/GEO landing pages must contain at least 300 words of visible, page-specific main content "
    "(excluding shared navigation/footer and legal/contact disclosures): " + repr(thin_pages)
)
# Require each SEO landing page to contain enough distinct terms to catch repeated boilerplate.
low_unique = []
for url in content_floor_pages:
    page_html = output_for_url(url).read_text(encoding="utf-8")
    words = [w.casefold() for w in content_words(visible_main_text(page_html))]
    unique_count = len(set(words))
    if unique_count < 90:
        low_unique.append((urlparse(url).path, unique_count))
assert not low_unique, "SEO/GEO landing pages appear too repetitive or thin: " + repr(low_unique)
print(f"PASS: {len(urls)} unique sitemap URLs, indexability, canonical URLs, internal links, valid JSON-LD, language metadata, and translated breadcrumbs.")
# Homepage content should provide direct, qualified answers and primary-source references.
home_html = (ROOT / "index.html").read_text(encoding="utf-8")
tool_grid_match = re.search(r'<ul class="ca-home-tool-grid">(.*?)</ul>', home_html, re.S)
assert tool_grid_match, "Homepage must render the primary tools grid"
tool_grid_html = tool_grid_match.group(1)
assert tool_grid_html.count('href="/emi-calculator/"') == 1, "Homepage tools grid must contain exactly one EMI Calculator link"
assert "EMI Calculator" in tool_grid_html, "Homepage tools grid must visibly label the EMI Calculator"
money_html = output_for_url(SITE + "/money/").read_text(encoding="utf-8")
money_list_match = re.search(r'<ul class="mt-8 grid gap-4">(.*?)</ul>', money_html, re.S)
assert money_list_match, "Money and Business hub must render its calculator list"
money_list_html = money_list_match.group(1)
assert money_list_html.count('href="/emi-calculator/"') == 1, "Money and Business hub must contain exactly one EMI Calculator link"
assert "EMI Calculator" in money_list_html, "Money and Business hub must visibly label the EMI Calculator"
all_tools_match = re.search(r'<details[^>]*><summary[^>]*>All tools</summary>.*?<ul[^>]*>(.*?)</ul></details>', home_html, re.S)
assert all_tools_match, "Homepage must render the expandable All tools menu"
all_tools_html = all_tools_match.group(1)
assert all_tools_html.count('href="/emi-calculator/"') == 1, "All tools menu must contain exactly one EMI Calculator link"
assert "EMI Calculator" in all_tools_html, "All tools menu must visibly label the EMI Calculator"
assert "<h2" in home_html and "What can you calculate with these free tools?" in home_html, "Homepage must include a clear, question-formatted explanatory heading"
assert "Frequently asked questions: Are these calculators free, private, and reliable?" in home_html, "Homepage must include a clear FAQ section heading"
assert "a 20% discount on a price of 1,000 leaves 800" in home_html, "Homepage worked example must remain present"
assert "https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index" in home_html, "Homepage health reference must link to WHO"
assert "https://www.nist.gov/pml/owm/si-units-length" in home_html, "Homepage conversion reference must link to NIST"
assert "BMI is a screening measure, not a diagnosis" in home_html, "Homepage must retain BMI limitation wording"
assert "<h1>Free Online Standard Calculator</h1>" in home_html, "Homepage H1 must identify the primary calculator"
assert "Fast, free, and private. Tap the buttons or use your keyboard to calculate." in home_html, "Homepage opening paragraph must be concise and action-oriented"
# The standard calculator landing page now explicitly describes its scientific mode.
scientific_url = SITE + "/standard-calculator/"
assert "Scientific" in titles[scientific_url], "Calculator page title must identify the scientific mode"
assert "scientific calculator" in descriptions[scientific_url].lower(), "Calculator meta description must describe scientific calculations"
scientific_html = output_for_url(scientific_url).read_text(encoding="utf-8")
assert "Scientific Mode" in scientific_html, "Scientific mode toggle must be present in generated HTML"
assert "how to use the online standard and scientific calculator" in visible_main_text(scientific_html).lower(), "Scientific calculator guide must be visible to crawlers"
# Calculator-first layout contract: all tool pages except the standard calculator
# put the working tool directly after the heading/short lead, before explanatory notes.
calculator_slugs = (
    "zakat-calculator", "bmi-calculator", "profit-loss-calculator",
    "discount-calculator", "age-calculator", "unit-converter",
    "tasbih-counter", "stopwatch",
)
for slug in calculator_slugs:
    tool_html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
    calc_pos = tool_html.find('<section id="tool-calculator"')
    h1_pos = tool_html.find("<h1")
    lead_pos = tool_html.find('<p class="mt-3 text-lg', h1_pos)
    assert h1_pos >= 0 and lead_pos > h1_pos and calc_pos > lead_pos, (
        f"Calculator must follow the heading and short lead: /{slug}/"
    )
    main_open = re.search(r'<main id="main" class="[^"]*ca-tool-main[^"]*">', tool_html)
    assert main_open, f"Non-standard calculator page must use the compact calculator-first main layout: /{slug}/"
    note_pos = tool_html.find("Evidence-based note")
    if note_pos >= 0:
        assert calc_pos < note_pos, f"Calculator must appear before the explanatory note: /{slug}/"
    method_pos = tool_html.find("How it is calculated")
    assert method_pos < 0 or calc_pos < method_pos, f"Calculator must appear before guide content: /{slug}/"
# Urdu tool pages follow the same positioning contract where a translated tool exists.
for slug in calculator_slugs:
    urdu_page = ROOT / "ur" / slug / "index.html"
    if not urdu_page.is_file():
        continue
    urdu_html = urdu_page.read_text(encoding="utf-8")
    calc_pos = urdu_html.find('<section id="tool-calculator"')
    h1_pos = urdu_html.find("<h1")
    lead_pos = urdu_html.find('<p class="mt-3 text-lg', h1_pos)
    assert h1_pos >= 0 and lead_pos > h1_pos and calc_pos > lead_pos, (
        f"Urdu calculator must follow the heading and short lead: /ur/{slug}/"
    )
    assert calc_pos < urdu_html.find("<h2"), f"Urdu calculator must appear before guide content: /ur/{slug}/"
    assert re.search(r'<main id="main" class="[^"]*ca-tool-main[^"]*">', urdu_html), (
        f"Urdu tool page must use the compact calculator-first main layout: /ur/{slug}/"
    )
# The standalone EMI tool keeps its complete form ahead of jump links and long repayment content.
emi_html = output_for_url(SITE + "/emi-calculator/").read_text(encoding="utf-8")
emi_calc_pos = emi_html.find('<section id="calculator"')
emi_jump_pos = emi_html.find('<nav aria-label="Jump links">')
emi_schedule_pos = emi_html.find('<section id="schedule"')
assert emi_calc_pos >= 0 and emi_jump_pos > emi_calc_pos, "EMI calculator must appear before jump links"
assert emi_schedule_pos > emi_jump_pos, "EMI jump links must remain before the long repayment schedule"
assert "#main.ca-tool-main" in site_css and ".ca-tool-calculator" in site_css, "Calculator-first spacing rules must be present in the compiled stylesheet"
# Guard the homepage Standard Calculator against layout regressions.
home_html = (ROOT / "index.html").read_text(encoding="utf-8")
home_calc_pos = home_html.find('class="ca-home-calculator"')
home_h1_pos = home_html.find("<h1")
assert home_h1_pos >= 0 and home_calc_pos > home_h1_pos, "Homepage Standard Calculator must follow the heading"
site_css_compact = re.sub(r"\s+", "", site_css)
assert ".ca-home-layout" in site_css_compact and "grid-template-columns:minmax(0,1fr)" in site_css_compact, "Homepage calculator must use a single wide column"
assert ".ca-home-side{display:none!important}" in site_css_compact and ".ca-home-tools{display:block!important;width:100%}" in site_css_compact, "Homepage should hide decorative side copy but preserve the other-tools list below the calculator"
assert ".ca-home-calculator" in site_css, "Homepage calculator styles must survive the CSS build"
input_css = (ROOT.parent / "styles" / "input.css").read_text(encoding="utf-8")
assert re.search(r"@media\s*\(max-width:\s*640px\)[\s\S]*?\.ca-home-calculator\s+#calc-pad\s+button\s*\{\s*min-height:\s*2\.8rem", input_css), "Homepage mobile calculator sizing must be explicitly defined in source CSS"
assert "20261023-home-layout-fix-v2" in home_html, "Homepage must load the restored calculator-first stylesheet"
layout_marker = "/* Persistent homepage calculator-first layout override. Keep this in source CSS because build:css regenerates static/site.css. */"
assert layout_marker in input_css, "Calculator-first desktop layout must live in source CSS, not only the generated stylesheet"
layout_override = input_css.split(layout_marker, 1)[1]
assert re.search(r"\.ca-home-layout\s*\{[^}]*grid-template-columns:\s*minmax\(0,\s*1fr\)", layout_override), "Persistent homepage layout override must force one desktop column after the legacy responsive rules"
legacy_grid_pos = site_css_compact.find("@media(max-width:1200px)")
final_grid_pos = site_css_compact.rfind(".ca-home-layout{display:grid;grid-template-columns:minmax(0,1fr)")
assert final_grid_pos > legacy_grid_pos, "Generated CSS must retain the one-column desktop override after legacy grid rules"
assert 'id="all-tools" class="ca-home-tools"' in home_html, "Homepage must expose a stable All Tools anchor for cross-page navigation"
standard_tool_html = output_for_url(SITE + "/standard-calculator/").read_text(encoding="utf-8")
assert "ca-tool-main" not in standard_tool_html, "Standard Calculator tool route must not receive compact non-standard tool styling"
standard_tool_h1_pos = standard_tool_html.find("<h1")
standard_tool_lead_end = standard_tool_html.find("</p>", standard_tool_h1_pos)
standard_tool_calc_pos = standard_tool_html.find('id="calc-display"')
standard_tool_note_pos = standard_tool_html.find("Evidence-based note")
assert standard_tool_calc_pos > standard_tool_lead_end, "Standard calculator widget must follow its title and lead"
assert standard_tool_note_pos < 0 or standard_tool_calc_pos < standard_tool_note_pos, "Standard calculator widget must precede explanatory notes"