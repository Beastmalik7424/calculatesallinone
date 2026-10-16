import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
xml = ET.parse(ROOT / "sitemap.xml").getroot()
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [node.find("sm:loc", ns).text for node in xml.findall("sm:url", ns)]
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
    assert re.search(r"<title>[^<]+</title>", html), f"Missing title: {url}"
    assert re.search(r'<meta name="description" content="[^"]+"', html), f"Missing description: {url}"
    assert f'<link rel="canonical" href="{url}">' in html, f"Canonical mismatch: {url}"
    assert '<meta name="robots" content="index, follow">' in html, f"Page not indexable: {url}"

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
    for href in re.findall(r'href="(/[^"#?]*)"', html):
        path = href.split("?", 1)[0]
        if path.startswith("/assets/"):
            target = ROOT / path.lstrip("/")
            if not target.is_file():
                broken.append((str(page), href))
        else:
            normalized = path.strip("/")
            target = ROOT / normalized / "index.html" if normalized else ROOT / "index.html"
            if not target.is_file():
                broken.append((str(page), href))
assert not broken, "Broken internal hrefs found: " + repr(broken[:20])

for required in ("/marketplaces/", "/affiliate-disclosure/", "/about/", "/privacy/", "/contact/"):
    assert SITE + required in sitemap_urls, f"Required public page missing from sitemap: {required}"

print(f"PASS: {len(urls)} unique sitemap URLs, every generated page indexable, canonicalized, and internally linked.")
