#!/usr/bin/env python3
"""Audit every indexable generated page, not only a hand-picked SEO sample."""
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
INDEXABLE_FILE = Path("indexable.txt")
NOINDEX_FILE = Path("noindex.txt")
ERRORS = []


def check(condition, message):
    if not condition:
        ERRORS.append(message)


def read_text(path):
    if not path.is_file():
        ERRORS.append("MISSING: " + str(path))
        return ""
    return path.read_text(encoding="utf-8")


def output_path(route):
    return ROOT / route.strip("/") / "index.html" if route != "/" else ROOT / "index.html"


indexable = [line.strip() for line in read_text(INDEXABLE_FILE).splitlines() if line.strip()]
noindex = [line.strip() for line in read_text(NOINDEX_FILE).splitlines() if line.strip()]
check(bool(indexable), "indexable.txt must contain at least one route")
check(len(indexable) == len(set(indexable)), "indexable.txt contains duplicate routes")
check(len(noindex) == len(set(noindex)), "noindex.txt contains duplicate routes")
check(not (set(indexable) & set(noindex)), "a route appears in both indexable.txt and noindex.txt")

titles = {}
descriptions = {}
sitemap_path = ROOT / "sitemap.xml"
sitemap_urls = set()
try:
    sitemap_root = ET.parse(sitemap_path).getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {
        node.findtext("sm:loc", namespaces=ns)
        for node in sitemap_root.findall("sm:url", ns)
    }
except (ET.ParseError, OSError) as exc:
    ERRORS.append("sitemap.xml is missing or invalid: " + str(exc))

expected_urls = {SITE + route for route in indexable}
check(sitemap_urls == expected_urls,
      "sitemap URLs must match indexable.txt exactly; missing="
      + ", ".join(sorted(expected_urls - sitemap_urls))
      + "; unexpected=" + ", ".join(sorted(sitemap_urls - expected_urls)))

for route in indexable:
    source_path = output_path(route)
    raw = read_text(source_path)
    if not raw:
        continue

    title_matches = re.findall(r"<title>(.*?)</title>", raw, re.S | re.I)
    description_matches = re.findall(
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
        raw, re.I
    )
    canonical_matches = re.findall(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
        raw, re.I
    )
    robots_matches = re.findall(
        r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']',
        raw, re.I
    )
    h1_count = len(re.findall(r"<h1\b", raw, re.I))

    check(len(title_matches) == 1, route + ": expected exactly one title")
    check(len(description_matches) == 1, route + ": expected exactly one meta description")
    check(len(canonical_matches) == 1, route + ": expected exactly one canonical")
    check(len(robots_matches) == 1, route + ": expected exactly one robots directive")
    check(h1_count == 1, route + ": expected exactly one H1, found " + str(h1_count))

    if title_matches:
        title = html.unescape(title_matches[0]).strip()
        titles[route] = title
        check(bool(title), route + ": title is empty")
        check(len(title) <= 63, route + ": title exceeds 63 characters (" + str(len(title)) + ")")

    if description_matches:
        description = html.unescape(description_matches[0]).strip()
        descriptions[route] = description
        check(70 <= len(description) <= 160,
              route + ": meta description length outside 70-160 (" + str(len(description)) + ")")

    check(canonical_matches == [SITE + route],
          route + ": canonical must be the exact self-referencing production URL")
    check(robots_matches and robots_matches[0].strip().lower() == "index, follow",
          route + ": indexable route must use 'index, follow'")

    check(bool(re.search(r"<main\b", raw, re.I)), route + ": missing main landmark")
    check(bool(re.search(r'<html\b[^>]*\blang=["\'][a-z]{2}(?:-[A-Za-z0-9-]+)?["\']', raw, re.I)),
          route + ": missing valid HTML language declaration")
    check(not re.search(r"<img\b(?![^>]*\balt\s*=)", raw, re.I),
          route + ": image missing alt attribute")

    schema_blocks = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        raw, re.S | re.I
    )
    check(bool(schema_blocks), route + ": missing JSON-LD")
    page_entities = []
    for block in schema_blocks:
        try:
            parsed = json.loads(block)
        except json.JSONDecodeError as exc:
            ERRORS.append(route + ": invalid JSON-LD: " + str(exc))
            continue
        nodes = parsed if isinstance(parsed, list) else [parsed]
        page_entities.extend(
            node for node in nodes
            if isinstance(node, dict)
            and node.get("@type") in ("WebPage", "AboutPage", "ProfilePage")
        )
    check(len(page_entities) == 1,
          route + ": expected exactly one page-level WebPage/AboutPage entity")

check(len(set(titles.values())) == len(titles), "duplicate titles across indexable pages")
check(len(set(descriptions.values())) == len(descriptions), "duplicate descriptions across indexable pages")

for route in noindex:
    raw = read_text(output_path(route))
    if not raw:
        continue
    robots = re.search(
        r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']',
        raw, re.I
    )
    check(bool(robots and "noindex" in robots.group(1).lower()),
          route + ": noindex manifest route must have a noindex directive")
    check(SITE + route not in sitemap_urls,
          route + ": noindex route must not appear in sitemap")

robots_txt = read_text(ROOT / "robots.txt")
check(bool(re.search(
    r"(?ms)^User-agent: OAI-SearchBot\s*\nAllow: /\s*\nDisallow: /404(?:\s|$)",
    robots_txt
)), "robots.txt must allow OAI-SearchBot and keep /404 blocked")
check(not re.search(r"(?m)^Disallow:\s*/\s*$", robots_txt),
      "robots.txt must not block the whole site")
sitemap_lines = [
    line.strip() for line in robots_txt.splitlines()
    if line.strip().lower().startswith("sitemap:")
]
check(sitemap_lines == ["Sitemap: " + SITE + "/sitemap.xml"],
      "robots.txt must contain exactly one production sitemap URL")

if ERRORS:
    print("ALL-INDEXABLE-PAGES SEO AUDIT: FAIL")
    for error in ERRORS:
        print("FAIL:", error)
    sys.exit(1)

print("ALL-INDEXABLE-PAGES SEO AUDIT: PASS")
print("Indexable routes checked:", len(indexable))
print("Noindex routes checked:", len(noindex))
print("Titles, descriptions, canonicals, robots, H1, language, image alt, JSON-LD and sitemap coverage: PASS")
print("OAI-SearchBot robots permission: PASS")
