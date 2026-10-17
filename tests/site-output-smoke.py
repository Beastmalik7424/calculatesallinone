import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
xml = ET.parse(ROOT / "sitemap.xml").getroot()
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [node.find("sm:loc", ns).text for node in xml.findall("sm:url", ns)]
titles = {}
descriptions = {}
assert urls, "Sitemap has no URLs"
assert len(urls) == len(set(urls)), "Duplicate URLs found in sitemap"
lastmod_entries = {
    node.find("sm:loc", ns).text: node.find("sm:lastmod", ns).text
    for node in xml.findall("sm:url", ns)
    if node.find("sm:lastmod", ns) is not None
}
assert lastmod_entries == {SITE + "/zakat-calculator/": "2026-10-08"}, (
    "Only verified per-page lastmod dates should be emitted; got " + repr(lastmod_entries)
)
assert all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) for value in lastmod_entries.values()), (
    "Sitemap lastmod values must use YYYY-MM-DD format."
)

def output_for_url(url):
    parsed = urlparse(url)
    assert parsed.scheme == "https" and parsed.netloc == urlparse(SITE).netloc, f"Unexpected sitemap host: {url}"
    path = parsed.path.strip("/")
    return ROOT / path / "index.html" if path else ROOT / "index.html"

for url in urls:
    page = output_for_url(url)
    assert page.is_file(), f"Sitemap URL has no generated HTML: {url} -> {page}"
    html = page.read_text(encoding="utf-8")
    title_match = re.search(r"<title>([^<]+)</title>", html)
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
    assert title_match, f"Missing title: {url}"
    assert desc_match, f"Missing description: {url}"
    titles[url] = title_match.group(1)
    descriptions[url] = desc_match.group(1)
    assert html.count("<h1") == 1, f"Expected exactly one primary heading: {url}"
    assert f'<link rel="canonical" href="{url}">' in html, f"Canonical mismatch: {url}"
    assert '<meta name="robots" content="index, follow">' in html, f"Page not indexable: {url}"

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

# The Urdu root is a localized site homepage, not a standard-calculator landing page.
urdu_home_url = SITE + "/ur/"
assert titles[urdu_home_url].startswith("CalculatesAll |"), (
    "Urdu homepage title must identify the site and its broad purpose: " + titles[urdu_home_url]
)
assert "معیاری کیلکولیٹر" not in titles[urdu_home_url], (
    "Urdu homepage title incorrectly targets only the standard calculator."
)
ur_home_html = output_for_url(urdu_home_url).read_text(encoding="utf-8")
ur_home_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", ur_home_html, re.S)
assert ur_home_h1 and "مفت آن لائن کیلکولیٹرز" in ur_home_h1.group(1), (
    "Urdu homepage H1 must describe the calculator collection."
)

sitemap_urls = set(urls)
generated = set()
for page in ROOT.rglob("index.html"):
    rel = page.parent.relative_to(ROOT).as_posix()
    path = "/" + (rel + "/" if rel != "." else "")
    generated.add(SITE + path)
assert generated == sitemap_urls, (
    "Sitemap/page mismatch. Missing from sitemap: " + repr(sorted(generated - sitemap_urls)) +
    "; URLs without generated pages: " + repr(sorted(sitemap_urls - generated))
)

robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert "User-agent: *" in robots and "Allow: /" in robots
assert f"Sitemap: {SITE}/sitemap.xml" in robots

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
privacy_html = (ROOT / "privacy" / "index.html").read_text(encoding="utf-8")
marketplace_html = (ROOT / "marketplaces" / "index.html").read_text(encoding="utf-8")
assert "Advertising is disabled by default" in privacy_html, "Privacy page must state that ads are disabled by default"
assert "ADSENSE_CONSENT_READY=true" in privacy_html, "Privacy page must disclose the consent-readiness safeguard"
assert "Google-certified consent management platform" in privacy_html, "Privacy page must describe the CMP requirement"
assert "cookie identifiers" in privacy_html and "web beacons" in privacy_html and "IP addresses" in privacy_html, "Privacy page must disclose relevant advertising technologies/data"
assert "https://policies.google.com/technologies/partner-sites" in privacy_html, "Privacy page must link Google's data-use disclosure"
assert "deliberately does not create an ads.txt file" in marketplace_html, "Marketplace guide must explain why ads.txt can return 404"

# Google Search Console ownership HTML must be present in the deployed output.
verification_file = ROOT / "google2e764d068684499b.html"
assert verification_file.is_file(), "Google Search Console verification file missing from Vercel output"
assert verification_file.read_text(encoding="utf-8").strip() == "google-site-verification: google2e764d068684499b.html", "Google Search Console verification file content mismatch"


# Per-page structured-data and language audit.
# Parse every JSON-LD block rather than only checking that a script tag exists.
for url in urls:
    page = output_for_url(url)
    html = page.read_text(encoding="utf-8")
    lang_match = re.search(r'<html lang="([^"]+)"', html)
    assert lang_match, f"Missing document language: {url}"
    page_lang = lang_match.group(1)
    jsonld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert jsonld_blocks, f"Missing JSON-LD structured data: {url}"
    parsed_schemas = []
    for block in jsonld_blocks:
        try:
            parsed_schemas.append(json.loads(block))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Invalid JSON-LD on {url}: {exc}") from exc
    for item in parsed_schemas:
        if item.get("@type") in ("WebSite", "WebPage", "CollectionPage", "WebApplication"):
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
assert "/assets/site.css?v=20261017-mobile-contrast-fix" in homepage_html, "Stylesheet cache-buster must change with the contrast fix"

# Keep the browser-side calculator implementation free from dynamic code execution.
app_js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
assert "eval(" not in app_js and "new Function" not in app_js, "Dynamic code execution found in app.js"

print(f"PASS: {len(urls)} unique sitemap URLs, indexability, canonical URLs, internal links, valid JSON-LD, language metadata, and translated breadcrumbs.")
