import datetime
import html
import json
import re
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
HUB_PATHS = {"/ar/", "/es/", "/fr/", "/hi/", "/ur/", "/money/", "/health/", "/math/", "/time/", "/worship/"}
TOOL_SLUGS = {"zakat-calculator", "bmi-calculator", "profit-loss-calculator", "discount-calculator", "age-calculator", "unit-converter", "standard-calculator", "tasbih-counter", "stopwatch"}
NO_SLASH_PATHS = ["/contact", "/editorial-policy", "/methodology", "/privacy", "/terms"]

def page_path(file):
    rel = file.parent.relative_to(ROOT).as_posix()
    return "/" if rel == "." else "/" + rel.strip("/") + "/"

def strip_tags(value):
    # Count visible main content, including lists and FAQ text, but exclude
    # navigation, footer, scripts and styles.
    value = re.sub(r"<script[^>]*>.*?</script>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<style[^>]*>.*?</style>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<nav[^>]*>.*?</nav>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<footer[^>]*>.*?</footer>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<noscript[^>]*>.*?</noscript>", " ", value, flags=re.S|re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", value))

def word_count(value):
    return len(strip_tags(value).split())

def source_files(path):
    if path in ("/ar/", "/hi/", "/es/", "/fr/"):
        return ["lang_v6.py", "build.py"]
    if path == "/ur/":
        return ["build.py"]
    if path.startswith("/ur/"):
        return ["urdu_v5.py", "build.py"]
    if path in ("/money/", "/health/", "/math/", "/time/", "/worship/"):
        return ["content_v13.py", "build.py"]
    if path == "/":
        return ["build.py"]
    if path in ("/about/", "/privacy/", "/methodology/", "/editorial-policy/", "/terms/", "/contact/", "/marketplaces/", "/affiliate-disclosure/"):
        return ["build.py", "content_v13.py"]
    return ["content_v5.py", "build.py"]

def git_date(path):
    sources = source_files(path)
    dates = []
    for src in sources:
        try:
            value = subprocess.check_output(["git", "log", "-1", "--format=%cs", "--", src], text=True, stderr=subprocess.DEVNULL).strip()
            if re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
                dates.append(value)
        except (OSError, subprocess.CalledProcessError):
            continue
    if dates:
        return max(dates), None
    return datetime.date.today().isoformat(), ", ".join(sources)

def normalize_meta(raw, path, lang):
    title_match = re.search(r"<title>(.*?)</title>", raw, re.S)
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', raw)
    if not title_match or not desc_match:
        raise SystemExit("Missing title/description: " + path)
    title = html.unescape(title_match.group(1).strip())
    desc = html.unescape(desc_match.group(1).strip())
    if len(title) > 59:
        title = re.sub(r" \\| Free Online Tool \\| CalculatesAll$", " | CalculatesAll", title)
        if len(title) > 59:
            suffix = " | CalculatesAll"
            title = title[:59-len(suffix)].rstrip(" |") + suffix
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0].rstrip(" ,.;:") + "..."
    if len(desc) < 120:
        tail = " فارمولا، مثال اور حدود دیکھ کر نتیجے کو سمجھیں۔" if lang == "ur" else " Review the formula, worked example and limits before relying on the result."
        separator = "" if desc.endswith(("۔", ".", "!", "?")) else "."
        desc = desc + separator + " " + tail.lstrip()
    if len(desc) < 120:
        desc = (desc + (" طریقہ اور مثال دیکھیں۔" if lang == "ur" else " Check the stated method and example."))[:160]
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0].rstrip(" ,.;:") + "..."
    raw = re.sub(r"<title>.*?</title>", "<title>" + html.escape(title, quote=False) + "</title>", raw, count=1, flags=re.S)
    raw = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + html.escape(desc, quote=True) + '"', raw, count=1)
    return raw, title, desc

def main():
    files = sorted(ROOT.rglob("index.html"))
    if not files:
        raise SystemExit("No generated HTML pages found")
    paths = {page_path(f): f for f in files}
    noindex = set()
    page_dates = {path: git_date(path) for path in paths}
    # Count full visible main content, not just text before the first list.
    for path in sorted(HUB_PATHS):
        file = paths.get(path)
        if not file:
            continue
        raw = file.read_text(encoding="utf-8")
        main_match = re.search(r"<main[^>]*>(.*?)</main>", raw, re.S)
        main_html = main_match.group(1) if main_match else ""
        visible_words = word_count(main_html)
        hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', main_html)
        has_tool_links = any(href in ("/" + slug + "/", "/ur/" + slug + "/") for href in hrefs for slug in TOOL_SLUGS)
        if visible_words < 150 or not has_tool_links:
            noindex.add(path)
    # Preserve any intentional noindex pages, including 404.
    for path, file in paths.items():
        raw = file.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="noindex', raw):
            noindex.add(path)
    results = {}
    titles, descriptions = {}, {}
    for path, file in paths.items():
        raw = file.read_text(encoding="utf-8")
        canonical = SITE + path
        raw = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + canonical + '">', raw, count=1)
        def keep_alternate(match):
            href = match.group(2)
            return "" if any(href == SITE + excluded for excluded in noindex) else match.group(0)
        raw = re.sub(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"\s*/?>', keep_alternate, raw)
        robot_value = "noindex, follow" if path in noindex else "index, follow"
        raw = re.sub(r'<meta name="robots" content="[^"]*"', '<meta name="robots" content="' + robot_value + '"', raw, count=1)
        if path in noindex:
            file.write_text(raw, encoding="utf-8")
            continue
        lang_match = re.search(r'<html lang="([^"]+)"', raw)
        lang = lang_match.group(1) if lang_match else "en"
        raw, title, desc = normalize_meta(raw, path, lang)
        titles[path] = title
        descriptions[path] = desc
        label = "آخری جائزہ" if lang == "ur" else "Last reviewed"
        review_date = page_dates[path][0]
        review_html = '<p class="mt-8 text-sm text-stone-700 dark:text-stone-300">' + label + ': ' + review_date + '</p>'
        # Replace the old tool-page update stamp with the source-derived date.
        raw = re.sub(r'<p class="mt-8 text-sm text-stone-800 dark:text-stone-200">Last updated: [0-9]{4}-[0-9]{2}-[0-9]{2}\. .*?</p>', review_html, raw, count=1, flags=re.S)
        if ("Last reviewed: " + review_date) not in raw and ("آخری جائزہ: " + review_date) not in raw:
            raw = raw.replace("</main>", review_html + "</main>", 1)
        schemas = []
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
            try:
                schemas.append(json.loads(match.group(1)))
            except json.JSONDecodeError as exc:
                raise SystemExit("Invalid JSON-LD in " + path + ": " + str(exc))
        web_page = next((s for s in schemas if s.get("@type") == "WebPage"), None)
        if web_page is None:
            web_page = {"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical}
            schemas.append(web_page)
        web_page["name"] = title
        web_page["url"] = canonical
        web_page["dateModified"] = review_date
        web_page["inLanguage"] = lang
        # FAQPage rich-result markup is intentionally excluded by project policy.
        schemas = [s for s in schemas if s.get("@type") != "FAQPage"]
        raw = re.sub(r'<script type="application/ld\+json">.*?</script>[ \t\r\n]*', "", raw, flags=re.S)
        schema_html = "".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False, separators=(",", ":")) + '</script>\n' for s in schemas)
        raw = raw.replace("</head>", schema_html + "</head>", 1)
        file.write_text(raw, encoding="utf-8")
        results[path] = raw
    if len(set(titles.values())) != len(titles):
        raise SystemExit("Duplicate titles among indexable pages")
    if len(set(descriptions.values())) != len(descriptions):
        raise SystemExit("Duplicate descriptions among indexable pages")
    for path, title in titles.items():
        if len(title) >= 60:
            raise SystemExit("Title >=60 characters: " + path)
        if not 120 <= len(descriptions[path]) <= 160:
            raise SystemExit("Description outside 120-160 characters: " + path + " (" + str(len(descriptions[path])) + ")")
    indexable = sorted(path for path in paths if path not in noindex)
    noindex_list = sorted(noindex)
    Path("indexable.txt").write_text("\n".join(indexable) + "\n", encoding="utf-8")
    Path("noindex.txt").write_text("\n".join(noindex_list) + ("\n" if noindex_list else ""), encoding="utf-8")
    Path("urls.txt").write_text("\n".join(indexable) + "\n", encoding="utf-8")
    Path("no-slash.txt").write_text("\n".join(NO_SLASH_PATHS) + "\n", encoding="utf-8")
    indexable_urls = {SITE + path for path in indexable}
    urlset = ET.Element("urlset", {"xmlns":"http://www.sitemaps.org/schemas/sitemap/0.9","xmlns:xhtml":"http://www.w3.org/1999/xhtml"})
    fallbacks = []
    for path in indexable:
        raw = paths[path].read_text(encoding="utf-8")
        canonical = SITE + path
        node = ET.SubElement(urlset, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text = canonical
        lastmod, fallback = page_dates[path]
        ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod").text = lastmod
        if fallback:
            fallbacks.append(path + " uses build date because git log returned no date for " + fallback)
        for code, href in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', raw):
            if href in indexable_urls:
                ET.SubElement(node, "{http://www.w3.org/1999/xhtml}link", {"rel":"alternate","hreflang":code,"href":href})
    ET.indent(urlset, space="  ")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding="unicode") + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /404\n\nSitemap: " + SITE + "/sitemap.xml\n", encoding="utf-8")
    report = ["SEO build report", "Review dates: source-file git dates", "Indexable pages: " + str(len(indexable)),
              "Noindex pages: " + str(len(noindex_list)), "Sitemap URLs: " + str(len(indexable)),
              "Titles: unique and under 60 characters", "Descriptions: unique and 120-160 characters",
              "JSON-LD: parsed and serialized as valid JSON", "Hub decisions:"]
    report.extend("  " + p + ": " + ("noindex" if p in noindex else "indexable") for p in sorted(HUB_PATHS))
    report.append("Lastmod fallbacks:")
    report.extend("  " + item for item in fallbacks)
    Path("seo-build-report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
