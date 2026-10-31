#!/usr/bin/env python3
"""Focused build-output checks for the eight scoped SEO URLs."""
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
TARGETS = {
    "/ar/": "noindex",
    "/es/": "noindex",
    "/fr/": "noindex",
    "/about/": "index",
    "/contact/": "index",
    "/discount-calculator/": "index",
    "/editorial-policy/": "index",
    "/health/": "index",
}
CHECK_PAGES = {"/": ROOT / "index.html"}
for path in TARGETS:
    CHECK_PAGES[path] = ROOT / path.strip("/") / "index.html"

errors = []
def check(condition, message):
    if not condition:
        errors.append(message)

def read(path):
    if not path.exists():
        errors.append("MISSING: " + str(path))
        return ""
    return path.read_text(encoding="utf-8")

def visible_main(raw):
    match = re.search(r"<main\b[^>]*>(.*?)</main>", raw, re.S | re.I)
    main = match.group(1) if match else ""
    main = re.sub(r"<(script|style|form|nav|footer|header)\b[^>]*>.*?</\1>", " ", main, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", main))

pages = {path: read(file) for path, file in CHECK_PAGES.items()}
titles, descriptions = {}, {}
for path, raw in pages.items():
    if not raw:
        continue
    title = re.search(r"<title>(.*?)</title>", raw, re.S | re.I)
    desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', raw, re.I)
    canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', raw, re.I)
    robots = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', raw, re.I)
    titles[path] = html.unescape(title.group(1).strip()) if title else ""
    descriptions[path] = html.unescape(desc.group(1).strip()) if desc else ""
    check(bool(title), path + ": missing title")
    check(bool(desc), path + ": missing meta description")
    check(bool(canonical), path + ": missing canonical")
    check(bool(canonical and canonical.group(1) == SITE + path), path + ": canonical is not self-referencing slash URL")
    check(bool(robots), path + ": missing meta robots")
    if path in TARGETS:
        expected = TARGETS[path]
        check(bool(robots and (("noindex" in robots.group(1).lower()) == (expected == "noindex"))),
              path + ": robots does not match the reviewed decision")
        if expected == "noindex":
            check(not re.search(r'<link\s+rel=["\']alternate["\']\s+hreflang=', raw, re.I),
                  path + ": noindex language homepage must not publish hreflang alternates")
    h1_count = len(re.findall(r"<h1\b", raw, re.I))
    check(h1_count == 1, path + ": expected exactly one H1, got " + str(h1_count))
    check(len(titles[path]) < 60, path + ": title must be under 60 characters (" + str(len(titles[path])) + ")")
    check(0 < len(descriptions[path]) < 160, path + ": description must be under 160 characters")
    check(not re.search(r"<img\b(?![^>]*\balt\s*=)", raw, re.I), path + ": image missing alt attribute")
    if path in ("/about/", "/contact/", "/discount-calculator/", "/editorial-policy/", "/health/"):
        schemas = []
        for match in re.finditer(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', raw, re.S | re.I):
            try:
                obj = __import__("json").loads(match.group(1))
                schemas.extend(obj if isinstance(obj, list) else [obj])
            except Exception as exc:
                errors.append(path + ": invalid JSON-LD: " + str(exc))
        check(any(obj.get("@type") == "BreadcrumbList" for obj in schemas), path + ": missing BreadcrumbList")
        if path == "/about/":
            check(any(obj.get("@type") == "AboutPage" for obj in schemas), path + ": missing AboutPage schema")
            check(not any(obj.get("@type") in ("WebPage", "ProfilePage") for obj in schemas), path + ": duplicate or mismatched page schema")
            check(any(obj.get("@type") == "Organization" and obj.get("@id") == SITE + "/#organization" for obj in schemas), path + ": missing canonical Organization entity")
            check(any(obj.get("@type") == "Person" and obj.get("@id") == SITE + "/#maintainer" for obj in schemas), path + ": missing canonical maintainer entity")
        if path == "/discount-calculator/":
            check(any(obj.get("@type") == "WebApplication" for obj in schemas), path + ": missing WebApplication")
            check(any(obj.get("@type") == "FAQPage" for obj in schemas), path + ": missing FAQPage for visible FAQs")
            check(visible_main(raw).count("?") >= 3, path + ": expected at least three visible FAQ questions")
    if path in ("/about/", "/discount-calculator/", "/editorial-policy/", "/health/"):
        words = re.findall(r"\b[\w’'-]+\b", visible_main(raw), re.UNICODE)
        minimum = 420 if path == "/about/" else (300 if path == "/discount-calculator/" else 150)
        print("WORDCOUNT", path, len(words))
        check(len(words) >= minimum, path + ": main-content word count below " + str(minimum) + " (" + str(len(words)) + ")")

check(len(set(titles.values())) == len(titles), "duplicate titles across homepage and eight scoped pages")
check(len(set(descriptions.values())) == len(descriptions), "duplicate descriptions across homepage and eight scoped pages")

home = pages.get("/", "")
check('href="#all-tools"' in home and "Browse all free calculators" in home,
      "homepage is missing the primary browse-calculators CTA")
check("Muhammad Fayyaz Adeel" in home and 'href="/about/"' in home,
      "homepage is missing the named maintainer and About link")
profit_loss = read(ROOT / "profit-loss-calculator" / "index.html")
check("online calculator" in home.lower(), "homepage should retain the online calculator topic wording")
check("profit loss calculator" in profit_loss.lower(), "profit-loss page should retain the profit loss calculator wording")
for path in TARGETS:
    check(bool(re.search(r'href=["\']' + re.escape(path) + r'["\']', home)),
          "homepage is missing direct internal link to " + path)

sitemap_path = ROOT / "sitemap.xml"
sitemap = read(sitemap_path)
try:
    root = ET.fromstring(sitemap)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {node.findtext("sm:loc", namespaces=ns) for node in root.findall("sm:url", ns)}
    for path, decision in TARGETS.items():
        url = SITE + path
        check((url in locs) == (decision == "index"), "sitemap membership mismatch for " + url)
        if decision == "index":
            node = next((n for n in root.findall("sm:url", ns) if n.findtext("sm:loc", namespaces=ns) == url), None)
            lastmod = node.findtext("sm:lastmod", namespaces=ns) if node is not None else None
            check(lastmod is None, "unverified lastmod must be omitted for " + url)
    for url in locs:
        check(url.endswith("/"), "sitemap URL lacks trailing slash: " + str(url))
    for node in root.findall("sm:url", ns):
        check(node.find("sm:lastmod", ns) is None,
              "sitemap must omit unverified lastmod: " + str(node.findtext("sm:loc", namespaces=ns)))
    print("SITEMAP_SCOPED_INDEXABLE_URLS")
    for path, decision in TARGETS.items():
        if decision == "index":
            print(SITE + path)
except ET.ParseError as exc:
    errors.append("invalid sitemap XML: " + str(exc))

robots_txt = read(ROOT / "robots.txt")
sitemap_lines = [line.strip() for line in robots_txt.splitlines() if line.strip().lower().startswith("sitemap:")]
check(sitemap_lines == ["Sitemap: " + SITE + "/sitemap.xml"], "robots.txt must have exactly one full sitemap URL")
check(not any(line.strip() == "Disallow: /" for line in robots_txt.splitlines()), "robots.txt blocks the whole site")

# Internal links from the homepage and seven target pages must resolve to a generated page or asset.
for source_path, raw in pages.items():
    for href in re.findall(r'\bhref=["\']([^"\']+)["\']', raw, re.I):
        if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#", "data:")):
            continue
        dest = urlparse(href).path
        if not dest:
            continue
        candidate = ROOT / dest.lstrip("/")
        if dest.endswith("/"):
            candidate = candidate / "index.html"
        elif not candidate.suffix:
            candidate = candidate / "index.html"
        check(candidate.exists(), source_path + ": broken internal link " + href)

if errors:
    print("SEO SEVEN-PAGE AUDIT: FAIL")
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)
print("SEO SEVEN-PAGE AUDIT: PASS")
print("Title/description uniqueness: PASS")
print("Canonical, robots, H1, image alt, breadcrumbs, sitemap, lastmod and internal links: PASS")
