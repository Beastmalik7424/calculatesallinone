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

# Verify local image/script asset references resolve in the generated output.
for page in ROOT.rglob("index.html"):
    html = page.read_text(encoding="utf-8")
    for src in re.findall(r'src="(/assets/[^"]+)"', html):
        target = ROOT / urlparse(src).path.lstrip("/")
        assert target.is_file(), f"Broken local asset reference in {page}: {src}"

for required in ("/marketplaces/", "/affiliate-disclosure/", "/about/", "/privacy/", "/contact/"):
    assert SITE + required in sitemap_urls, f"Required public page missing from sitemap: {required}"
privacy_html = (ROOT / "privacy" / "index.html").read_text(encoding="utf-8")
marketplace_html = (ROOT / "marketplaces" / "index.html").read_text(encoding="utf-8")
assert "Advertising is currently disabled" in privacy_html, "Privacy page must explain disabled ads and conditional ads.txt"
assert "deliberately does not create an ads.txt file" in marketplace_html, "Marketplace guide must explain why ads.txt can return 404"

# Google Search Console ownership HTML must be present in the deployed output.
verification_file = ROOT / "google2e764d068684499b.html"
assert verification_file.is_file(), "Google Search Console verification file missing from Vercel output"
assert verification_file.read_text(encoding="utf-8").strip() == "google-site-verification: google2e764d068684499b.html", "Google Search Console verification file content mismatch"

print(f"PASS: {len(urls)} unique sitemap URLs, every generated page indexable, canonicalized, and internally linked.")
