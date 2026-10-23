import datetime
import html
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
HUB_PATHS = {"/money/", "/health/", "/math/", "/time/", "/worship/"}
# These homepage translations are not yet confirmed by a competent native-language reviewer.
# Keep them accessible to visitors but out of search results until the translated journey is checked.
UNREVIEWED_LOCALE_HOMES = {"/ar/", "/hi/", "/es/", "/fr/", "/ur/"}
DESCRIPTION_FALLBACKS = {
    "/about/": "Learn what CalculatesAll offers, how its free calculators work, and the principles behind clear formulas, examples and stated limitations.",
    "/privacy/": "Read how CalculatesAll handles calculator inputs, local browser storage, advertising technologies, cookies and privacy choices.",
    "/contact/": "Contact CalculatesAll to report a calculator issue, suggest an improvement or ask about the site's content and privacy practices.",
    "/methodology/": "See the formulas, conversion factors, worked examples and limitations used by CalculatesAll's calculators and reference tools.",
    "/editorial-policy/": "Learn how CalculatesAll researches, checks, updates and corrects its calculator guides, formulas and reference information.",
    "/terms/": "Read the terms for using CalculatesAll's free calculators, including accuracy limits, professional-advice disclaimers and permitted use.",
    "/marketplaces/": "Review official marketplace resources and the setup requirements for digital products, affiliate links and compliant website monetization.",
    "/affiliate-disclosure/": "Read when CalculatesAll may earn affiliate commissions and how any future affiliate links will be identified to visitors.",
    "/tasbih-counter/": "Use a free online tasbih counter for dhikr. Set a target, track your tasbeeh count, and save progress on this device without downloading an app.",
}
URDU_DESCRIPTION_FALLBACKS = {
    "/ur/zakat-calculator/": "اپنی بچت، اثاثے اور واجب الادا قرض درج کرکے چاندی کے نصاب اور مکمل قمری سال کی شرط کے مطابق زکوٰۃ کا حساب کریں۔",
    "/ur/bmi-calculator/": "بالغ افراد کا BMI میٹرک یا امپیریل اکائیوں میں معلوم کریں، WHO وزن کی درجہ بندی دیکھیں اور نتیجے کی حدود سمجھیں۔",
    "/ur/age-calculator/": "تاریخ پیدائش سے عمر سال، مہینوں اور دنوں میں معلوم کریں، کل دن دیکھیں، اور تاریخ کے حساب کی حدود سمجھیں۔",
    "/ur/profit-loss-calculator/": "قیمت خرید اور فروخت درج کرکے منافع یا نقصان اور اس کا فیصد معلوم کریں، پھر فارمولا اور مثال دیکھیں۔",
    "/ur/discount-calculator/": "اصل قیمت اور رعایت کا فیصد درج کرکے بچت اور آخری قیمت معلوم کریں، ساتھ ہی حساب کا طریقہ اور مثال دیکھیں۔",
    "/ur/standard-calculator/": "براؤزر میں جمع، تفریق، ضرب، تقسیم، فیصد اور قوسین کے ساتھ حساب کریں اور حساب کے اصول سمجھیں۔",
    "/ur/stopwatch/": "براؤزر میں وقت شروع، روکیں اور دوبارہ صفر کریں، اور مختصر وقت کی پیمائش میں ممکنہ فرق سمجھیں۔",
    "/ur/tasbih-counter/": "ذکر کی گنتی کے لیے ہدف مقرر کریں، باقی تعداد دیکھیں اور گنتی کو اسی ڈیوائس پر محفوظ رکھیں۔",
}
NO_SLASH_PATHS = ["/contact", "/editorial-policy", "/methodology", "/privacy", "/terms"]

def page_path(file):
    rel = file.parent.relative_to(ROOT).as_posix()
    return "/" if rel == "." else "/" + rel.strip("/") + "/"

def strip_tags(value):
    value = re.sub(r"<script[^>]*>.*?</script>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<style[^>]*>.*?</style>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<nav[^>]*>.*?</nav>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<ul[^>]*>.*?</ul>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<ol[^>]*>.*?</ol>", " ", value, flags=re.S|re.I)
    value = re.sub(r"<details[^>]*>.*?</details>", " ", value, flags=re.S|re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", value))

class FAQDetailsParser(HTMLParser):
    """Extract FAQ text from each details block without crossing element boundaries."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.items = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "details":
            self.stack.append({"summary": [], "answer": [], "field": None, "summary_seen": False, "answer_seen": False})
            return
        if not self.stack:
            return
        current = self.stack[-1]
        if tag == "summary" and not current["summary_seen"]:
            current["summary_seen"] = True
            current["field"] = "summary"
        elif tag == "p" and current["summary_seen"] and not current["answer_seen"]:
            current["answer_seen"] = True
            current["field"] = "answer"

    def handle_data(self, data):
        if self.stack and self.stack[-1]["field"]:
            self.stack[-1][self.stack[-1]["field"]].append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if not self.stack:
            return
        current = self.stack[-1]
        if tag in ("summary", "p"):
            current["field"] = None
        elif tag == "details":
            item = self.stack.pop()
            question = " ".join("".join(item["summary"]).split())
            answer = " ".join("".join(item["answer"]).split())
            if question and answer:
                self.items.append((question, answer))


def extract_faq_items(raw):
    parser = FAQDetailsParser()
    parser.feed(raw)
    faq_items = []
    for question, answer in parser.items:
        q_text = " ".join(strip_tags(question).split())
        a_text = " ".join(strip_tags(answer).split())
        # Reject malformed captures instead of publishing concatenated page text as a question.
        if not q_text or not a_text or len(q_text) > 200 or len(a_text) > 3000:
            continue
        if not q_text.endswith(("?", "؟")):
            continue
        faq_items.append({"@type": "Question", "name": q_text, "acceptedAnswer": {"@type": "Answer", "text": a_text}})
    return faq_items


def word_count(value):
    return len(strip_tags(value).split())

def normalize_meta(raw, path, lang):
    title_match = re.search(r"<title>(.*?)</title>", raw, re.S)
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', raw)
    if not title_match or not desc_match:
        raise SystemExit("Missing title/description: " + path)
    title = html.unescape(title_match.group(1).strip())
    # Repair the known malformed title explicitly rather than truncating it into a fragment.
    if path == "/profit-loss-calculator/":
        title = "Profit and Loss Calculator | CalculatesAll"
    if path == "/standard-calculator/":
        title = "Standard and Scientific Calculator | CalculatesAll"
    if path == "/tasbih-counter/":
        title = "Online Tasbih Counter | Free Dhikr Counter | CalculatesAll"
    desc = html.unescape(desc_match.group(1).strip())
    if path == "/tasbih-counter/":
        desc = "Use a free online tasbih counter for dhikr. Set a target, track your tasbeeh count, and save progress on this device without downloading an app."
    if len(title) > 59:
        title = re.sub(r" \\| Free Online Tool \\| CalculatesAll$", " | CalculatesAll", title)
        if len(title) > 59:
            suffix = " | CalculatesAll"
            title = title[:59-len(suffix)].rstrip(" |") + suffix
    if len(desc) < 90:
        desc = DESCRIPTION_FALLBACKS.get(path, URDU_DESCRIPTION_FALLBACKS.get(path, desc))
    if len(desc) > 160:
        shortened = desc[:157].rsplit(" ", 1)[0].rstrip(" ,.;:")
        desc = shortened + "..."
    if len(desc) < 70 or len(desc) > 160:
        raise SystemExit("Meta description needs a useful, page-specific 70-160 character description: " + path + " (" + str(len(desc)) + ")")
    raw = re.sub(r"<title>.*?</title>", "<title>" + html.escape(title, quote=False) + "</title>", raw, count=1, flags=re.S)
    raw = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + html.escape(desc, quote=True) + '"', raw, count=1)
    return raw, title, desc

def main():
    files = sorted(ROOT.rglob("index.html"))
    if not files:
        raise SystemExit("No generated HTML pages found")
    paths = {page_path(f): f for f in files}
    noindex = set()
    # Keep category hubs indexable only when they have an explanatory structure and crawlable tool links.
    for path in sorted(HUB_PATHS):
        file = paths.get(path)
        if not file:
            continue
        raw = file.read_text(encoding="utf-8")
        main_match = re.search(r"<main[^>]*>(.*?)</main>", raw, re.S)
        main_html = main_match.group(1) if main_match else ""
        has_tool_links = bool(re.search(r'<a[^>]+href="/(?:[a-z]{2}/)?[a-z0-9-]+/?"', main_html))
        # Category hubs have their own intro, tool directory, several explanatory sections and FAQs.
        # Validate this structure rather than imposing a word-count threshold Google does not publish.
        guide_headings = len(re.findall(r"<h2\b", main_html, re.I))
        explanatory_paragraphs = len(re.findall(r"<p\b", main_html, re.I))
        if guide_headings < 4 or explanatory_paragraphs < 6 or not has_tool_links:
            noindex.add(path)
    noindex.update(UNREVIEWED_LOCALE_HOMES)
    # Preserve any intentional noindex pages, including 404.
    for path, file in paths.items():
        raw = file.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="noindex', raw):
            noindex.add(path)
    results = {}
    titles, descriptions = {}, {}
    for path, file in paths.items():
        raw = file.read_text(encoding="utf-8")
        # Bing Webmaster Tools ownership verification belongs on the homepage only.
        if path == "/" and not re.search(r'<meta\s+name=["\']msvalidate\.01["\']', raw, re.I):
            verification_tag = '<meta name="msvalidate.01" content="07D62A8BA67BA474B5A13A27E6770782" />'
            raw = re.sub(r"<head([^>]*)>", lambda match: match.group(0) + "\n    " + verification_tag, raw, count=1, flags=re.I)
        canonical = SITE + path
        raw = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + canonical + '">', raw, count=1)
        def keep_alternate(match):
            href = match.group(2)
            return "" if any(href == SITE + excluded for excluded in noindex) else match.group(0)
        alternate_pattern = r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"\s*/?>'
        if path in noindex:
            # A noindex language page should not advertise itself as a hreflang search landing page.
            raw = re.sub(alternate_pattern, "", raw)
        else:
            raw = re.sub(alternate_pattern, keep_alternate, raw)
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
        # Remove legacy blanket review/update stamps. Never claim a page was reviewed unless that review occurred.
        raw = re.sub(r'<p class="mt-8 text-sm text-stone-(?:800|700) dark:text-stone-(?:200|300)">(?:Last updated:|Last reviewed:|آخری جائزہ:) [0-9]{4}-[0-9]{2}-[0-9]{2}.*?</p>', "", raw, count=1, flags=re.S)
        schemas = []
        jsonld_script_pattern = r"""<script\b(?=[^>]*\btype=["']application/ld\+json["'])[^>]*>(.*?)</script>"""
        for match in re.finditer(jsonld_script_pattern, raw, re.S | re.I):
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
        # Shared source-file commit dates do not prove when this individual page was reviewed.
        web_page.pop("dateModified", None)
        web_page["inLanguage"] = lang
        faq_items = extract_faq_items(raw)
        if faq_items:
            schemas = [s for s in schemas if s.get("@type") != "FAQPage"]
            schemas.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_items})
        raw = re.sub(jsonld_script_pattern + r"[ \t\r\n]*", "", raw, flags=re.S | re.I)
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
        if not 70 <= len(descriptions[path]) <= 160:
            raise SystemExit("Description outside 70-160 characters: " + path + " (" + str(len(descriptions[path])) + ")")
    indexable = sorted(path for path in paths if path not in noindex)
    noindex_list = sorted(noindex)
    Path("indexable.txt").write_text("\n".join(indexable) + "\n", encoding="utf-8")
    Path("noindex.txt").write_text("\n".join(noindex_list) + ("\n" if noindex_list else ""), encoding="utf-8")
    Path("urls.txt").write_text("\n".join(SITE + path for path in indexable) + "\n", encoding="utf-8")
    Path("no-slash.txt").write_text("\n".join(NO_SLASH_PATHS) + "\n", encoding="utf-8")
    indexable_urls = {SITE + path for path in indexable}
    # Dates are added only for pages substantively updated in this change.
    lastmod_by_path = {
        "/contact/": "2026-10-21",
        "/discount-calculator/": "2026-10-21",
        "/editorial-policy/": "2026-10-21",
        "/health/": "2026-10-21",
    }
    urlset = ET.Element("urlset", {"xmlns":"http://www.sitemaps.org/schemas/sitemap/0.9","xmlns:xhtml":"http://www.w3.org/1999/xhtml"})
    for path in indexable:
        raw = paths[path].read_text(encoding="utf-8")
        canonical = SITE + path
        node = ET.SubElement(urlset, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text = canonical
        if path in lastmod_by_path:
            ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod").text = lastmod_by_path[path]
        for code, href in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', raw):
            if href in indexable_urls:
                ET.SubElement(node, "{http://www.w3.org/1999/xhtml}link", {"rel":"alternate","hreflang":code,"href":href})
    ET.indent(urlset, space="  ")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding="unicode") + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /404\n\nSitemap: " + SITE + "/sitemap.xml\n", encoding="utf-8")
    report = ["SEO build report", "Freshness metadata: lastmod/dateModified omitted because reliable page-specific dates are unavailable", "Indexable pages: " + str(len(indexable)),
              "Noindex pages: " + str(len(noindex_list)), "Sitemap URLs: " + str(len(indexable)),
              "Titles: unique and under 60 characters", "Descriptions: unique, page-specific and 70-160 characters",
              "JSON-LD: parsed and serialized as valid JSON", "Hub decisions:"]
    report.extend("  " + p + ": " + ("noindex" if p in noindex else "indexable") for p in sorted(HUB_PATHS))
    Path("seo-build-report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
