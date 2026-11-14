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
    "/tasbih-counter/": "Free online tasbih calculator for dhikr and zikr. Count 33, 99 or a custom target, undo taps and save progress in this browser. No sign-up or app.",
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
VERIFIED_PAGE_UPDATE_DATES = {
    # This date records the verified Urdu BMI threshold-copy correction and source check in this change.
    "/ur/bmi-calculator/": "2026-11-09",
    # This date records the age-page leap-day anniversary disclosure and boundary-test update.
    "/age-calculator/": "2026-11-11",
    # This date records the verified Years-to-Days answer examples, calendar distinction and source review.
    "/years-to-days-calculator/": "2026-11-14",
    # This date records the verified unit definitions, conversion formulas, rounding and input-limit review.
    "/unit-converter/": "2026-11-14",
    # This date records the verified Tasbih keyboard, local-storage and reset-behaviour disclosures.
    "/tasbih-counter/": "2026-11-14",
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

def remove_ineligible_software_app_from_html(raw, path):
    """Strip WebApplication nodes from JSON-LD on pages excluded from normal SEO finalization."""
    pattern = r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    def clean_script(match):
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise SystemExit("Invalid JSON-LD in " + path + ": " + str(exc))
        cleaned = remove_ineligible_software_app(parsed)
        if cleaned is None:
            return ""
        return '<script type="application/ld+json">' + json.dumps(cleaned, ensure_ascii=False, separators=(",", ":")) + '</script>'
    return re.sub(pattern, clean_script, raw, flags=re.S | re.I)


def remove_ineligible_software_app(node):
    """Remove ineligible app rich-result nodes while preserving their page-level entity links."""
    if isinstance(node, list):
        apps = [item for item in node if isinstance(item, dict) and item.get("@type") == "WebApplication"]
        pages = [item for item in node if isinstance(item, dict) and item.get("@type") in ("WebPage", "AboutPage", "ProfilePage") ]
        for app in apps:
            matching_pages = [page for page in pages if app.get("url") and page.get("url") == app.get("url")]
            if not matching_pages and len(pages) == 1:
                matching_pages = pages
            for page in matching_pages:
                for key in ("author", "publisher", "citation"):
                    if key in app and key not in page:
                        page[key] = app[key]
        return [cleaned for item in node if (cleaned := remove_ineligible_software_app(item)) is not None]
    if isinstance(node, dict):
        if node.get("@type") == "WebApplication":
            return None
        cleaned = {}
        for key, value in node.items():
            cleaned_value = remove_ineligible_software_app(value)
            if cleaned_value is not None:
                cleaned[key] = cleaned_value
        return cleaned
    return node


def normalize_meta(raw, path, lang):
    title_match = re.search(r"<title>(.*?)</title>", raw, re.S)
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', raw)
    if not title_match or not desc_match:
        raise SystemExit("Missing title/description: " + path)
    title = html.unescape(title_match.group(1).strip())
    title_overrides = {
        "/about/": "About CalculatesAll | Project, Methods & Privacy",
        "/zakat-calculator/": "Zakat Calculator: Nisab Check & 2.5% Zakat | CalculatesAll",
        "/query-calculator/": "Query Calculator: Time, Dates & Math | CalculatesAll",
        "/percentage-calculator/": "Percentage Calculator: What Is X% of Y? | CalculatesAll",
        "/fraction-calculator/": "Fraction Calculator with Simplified Answers | CalculatesAll",
        "/compound-interest-calculator/": "Compound Interest Calculator Online | CalculatesAll",
        "/date-calculator/": "Date Difference Calculator | Days Between Dates | CalculatesAll",
        "/years-to-days-calculator/": "Years to Days Calculator | How Many Days in X Years?",
        "/money/": "Money Calculators: EMI, Zakat, Profit | CalculatesAll",
        "/math/": "Math Calculators and Unit Converters | CalculatesAll",
        "/contact/": "Contact CalculatesAll | Help and Feedback",
        "/health/": "Health Calculators and BMI Guide | CalculatesAll",
        "/calorie-calculator/": "Calorie Calculator | Maintenance & TDEE | CalculatesAll",
        "/terms/": "Terms of Use | CalculatesAll Free Tools",
        "/time/": "Date and Time Calculators | CalculatesAll",
        "/ur/age-calculator/": "عمر کیلکولیٹر | سال، مہینے اور دن",
        "/ur/bmi-calculator/": "بالغ BMI کیلکولیٹر اردو میں | وزن اور قد | CalculatesAll",
    }
    title = title_overrides.get(path, title)
    # Repair the known malformed title explicitly rather than truncating it into a fragment.
    if path == "/profit-loss-calculator/":
        title = "Profit and Loss Calculator | Markup and Margin"
    if path == "/tasbih-counter/":
        title = "Tasbih Calculator Online | Dhikr Counter | CalculatesAll"
    if path == "/standard-calculator/":
        title = "Standard and Scientific Calculator | CalculatesAll"
    if path == "/age-calculator/":
        title = "Age Calculator | Years, Months & Days | CalculatesAll"
    if path == "/unit-converter/":
        title = "Unit Converter | Weight, Length & Temperature"
    desc = html.unescape(desc_match.group(1).strip())
    description_overrides = {
    "/about/": "Meet the maintainer of CalculatesAll, explore its free browser-based calculators, learn how methods are checked, and find privacy and contact details.",
    "/affiliate-disclosure/": "Learn how CalculatesAll is funded, how advertisements are labelled, and how future affiliate links will be disclosed without influencing calculator results.",
    "/compound-interest-calculator/": "Estimate compound interest from your starting balance, annual rate, time and compounding frequency. Review the formula and see how growth accumulates.",
    "/contact/": "Contact CalculatesAll to report a calculator error, accessibility issue or translation problem. Include the page URL, inputs and expected result for review.",
    "/date-calculator/": "Compare dates with elapsed or inclusive day counts, calendar years, months and days, and decimal weeks. Gregorian leap-year and month-end rules are explained.",
    "/discount-calculator/": "Calculate your discount amount, final sale price and total savings from the original price and discount percentage. See the formula and a worked example.",
    "/query-calculator/": "Ask in English, Roman Urdu and six other languages about time, months, birth dates and simple arithmetic. Includes the Pakistan Independence Day date.",
    "/fraction-calculator/": "Add, subtract, multiply or divide two fractions and get a simplified result. The calculator keeps a positive denominator and explains the arithmetic steps.",
    "/stopwatch/": "Use a free online stopwatch in your browser with start, stop and reset controls. Measure elapsed time to hundredths of a second without installing an app.",
    "/years-to-days-calculator/": "Convert years to days or days to years using 365, 365.25 or 365.2425-day methods. Use a start date for exact Gregorian calendar days.",
    "/profit-loss-calculator/": "Calculate product profit, business operating profit, loss, markup and margin from revenue, costs and expenses. Includes clear formulas and PKR examples.",
    "/worship/": "Use a browser-based tasbih counter for dhikr, set a target and keep your count on this device. The page explains local storage and reset behaviour.",
    "/zakat-calculator/": "Calculate 2.5 percent Zakat on net wealth, check the silver Nisab threshold and lunar-year condition. Confirm personal rulings with a qualified scholar."
}
    urdu_description_overrides = {
    "/ur/age-calculator/": "تاریخ پیدائش اور مطلوبہ تاریخ درج کرکے عمر سال، مہینوں اور دنوں میں معلوم کریں۔ کل گزرے دن بھی دیکھیں اور کیلکولیٹر کے تاریخوں کے حساب کا طریقہ سمجھیں۔",
    "/ur/bmi-calculator/": "بالغوں کا BMI اردو میں نکالیں۔ وزن kg/lb اور قد cm یا فٹ/انچ درج کریں، فارمولا اور WHO حدود سمجھیں۔ BMI اسکریننگ ہے، تشخیص نہیں۔",
    "/ur/discount-calculator/": "اصل قیمت اور رعایت کا فیصد درج کرکے بچت، رعایت کے بعد آخری قیمت اور حساب کا طریقہ دیکھیں۔ مختلف رعایتوں کا موازنہ کریں اور خریداری سے پہلے نتیجہ چیک کریں۔",
    "/ur/profit-loss-calculator/": "قیمت خرید اور فروخت درج کرکے منافع یا نقصان اور اس کا فیصد معلوم کریں۔ کاروباری آمدنی، لاگت اور اخراجات سے خالص منافع کا حساب بھی کریں اور فارمولے دیکھیں۔",
    "/ur/standard-calculator/": "براؤزر میں جمع، تفریق، ضرب، تقسیم، فیصد اور قوسین کے ساتھ حساب کریں۔ سائنسی موڈ میں مثلثاتی افعال، جذر اور لاگرتھم استعمال کریں، بغیر ایپ ڈاؤن لوڈ کیے۔",
    "/ur/stopwatch/": "براؤزر میں وقت شروع، روکیں اور دوبارہ صفر کریں۔ اسٹاپ واچ سیکنڈ کے سو حصوں تک وقت دکھاتی ہے، مگر درستگی آلے اور براؤزر کی کارکردگی پر منحصر ہو سکتی ہے۔",
    "/ur/tasbih-counter/": "ذکر کے لیے تسبیح کاؤنٹر استعمال کریں، 33، 99 یا اپنا ہدف مقرر کریں اور گنتی اسی ڈیوائس پر محفوظ رکھیں۔ گنتی واپس لینے، صفر کرنے اور محفوظ رہنے کا طریقہ دیکھیں۔",
    "/ur/unit-converter/": "وزن، لمبائی اور درجہ حرارت کی اکائیاں تبدیل کریں، جیسے کلوگرام سے پاؤنڈ، سینٹی میٹر سے انچ اور سیلسیئس سے فارن ہائیٹ۔ ہر تبدیلی کا نتیجہ فوری دیکھیں۔",
    "/ur/zakat-calculator/": "چاندی کے نصاب کے مطابق خالص مال پر 2.5 فیصد زکوٰۃ کا حساب کریں۔ نقدی، سونا، چاندی، کاروباری مال اور واجب الادا قرض درج کریں، پھر قمری سال کی شرط کی تصدیق کریں۔"
}
    desc = description_overrides.get(path, urdu_description_overrides.get(path, desc))
    if path == "/tasbih-counter/":
        desc = "Free online tasbih calculator for dhikr and zikr. Count 33, 99 or a custom target, undo taps and save progress in this browser. No sign-up or app."
    if path == "/age-calculator/":
        desc = "Calculate your exact age in years, months and days, plus total days lived. Enter a birth date for a clear, free online age calculation."
    if path == "/unit-converter/":
        desc = "Convert kilograms, grams, pounds, ounces, metric and imperial lengths, and Celsius, Fahrenheit or Kelvin. See formulas, examples and input limits."
    # This exact-intent date title is 63 characters and has a dedicated regression gate.
    if path != "/date-calculator/" and len(title) > 59:
        title = re.sub(r" \| Free Online Tool \| CalculatesAll$", " | CalculatesAll", title)
        if len(title) > 59:
            suffix = " | CalculatesAll"
            title = title[:59-len(suffix)].rstrip(" |") + suffix
    if len(desc) < 120:
        desc = DESCRIPTION_FALLBACKS.get(path, URDU_DESCRIPTION_FALLBACKS.get(path, desc))
    if len(desc) > 160:
        shortened = desc[:157].rsplit(" ", 1)[0].rstrip(" ,.;:")
        desc = shortened + "..."
    if len(desc) < 70 or len(desc) > 160:
        raise SystemExit("Meta description needs a useful, page-specific 70-160 character description: " + path + " (" + str(len(desc)) + ")")
    raw = re.sub(r"<title>.*?</title>", "<title>" + html.escape(title, quote=False) + "</title>", raw, count=1, flags=re.S)
    raw = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + html.escape(desc, quote=True) + '"', raw, count=1)
    # Keep Open Graph and Twitter previews aligned with the canonical page title and description.
    for attr, name, value in (
        ("property", "og:title", title),
        ("property", "og:description", desc),
        ("name", "twitter:title", title),
        ("name", "twitter:description", desc),
    ):
        pattern = '(<meta ' + attr + '="' + name + '" content=")[^"]*(")'
        raw, count = re.subn(pattern, lambda m: m.group(1) + html.escape(value, quote=True) + m.group(2), raw, count=1)
        if count != 1:
            raise SystemExit("Missing or duplicate social meta tag: " + path + " " + name)
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
        # Keep Bing verification on the homepage, immediately after the UTF-8 declaration.
        if path == "/":
            verification_tag = '<meta name="msvalidate.01" content="07D62A8BA67BA474B5A13A27E6770782" />'
            raw = re.sub(r'<meta\b(?=[^>]*\bname=["\']msvalidate\.01["\'])[^>]*>\s*', "", raw, count=1, flags=re.I)
            charset_match = re.search(r'(<meta\b[^>]*\bcharset\s*=\s*["\'][^"\']+["\'][^>]*>)', raw, re.I)
            if not charset_match:
                raise SystemExit("Homepage is missing its UTF-8 charset declaration")
            raw = raw[:charset_match.end()] + "\n" + verification_tag + raw[charset_match.end():]
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
        # Clean only the two audited pages. Preserve all tags, script data, CSS, and their order.
        if path in ("/", "/emi-calculator/"):
            def normalize_audited_head(match):
                inner = re.sub(r"\r?\n[ \t\r]*\r?\n+", "\n", match.group(2)).strip("\r\n")
                return match.group(1) + "\n" + inner + "\n" + match.group(3)
            raw, head_count = re.subn(r"(<head\b[^>]*>)(.*?)(</head>)", normalize_audited_head, raw, count=1, flags=re.S | re.I)
            if head_count != 1:
                raise SystemExit("Missing or malformed head element: " + path)
        if path in noindex:
            raw = remove_ineligible_software_app_from_html(raw, path)
            file.write_text(raw, encoding="utf-8")
            continue
        lang_match = re.search(r'<html lang="([^"]+)"', raw)
        lang = lang_match.group(1) if lang_match else "en"
        raw, title, desc = normalize_meta(raw, path, lang)
        titles[path] = title
        descriptions[path] = desc
        # Keep only an exact, verified page-specific update date. Never claim a review that did not occur.
        update_stamp = re.compile(r'<p class="mt-8 text-sm text-stone-(?:800|700) dark:text-stone-(?:200|300)">(?:Last updated:|Last reviewed:|آخری جائزہ:) [0-9]{4}-[0-9]{2}-[0-9]{2}.*?</p>', re.S)
        verified_date = VERIFIED_PAGE_UPDATE_DATES.get(path)
        def retain_verified_update(match):
            stamp = match.group(0)
            expected_prefix = '<p class="mt-8 text-sm text-stone-800 dark:text-stone-200">Last updated: ' + verified_date + '</p>'
            return stamp if verified_date and stamp.startswith(expected_prefix) else ""
        raw = update_stamp.sub(retain_verified_update, raw, count=1)
        schemas = []
        jsonld_script_pattern = r"""<script\b(?=[^>]*\btype=["']application/ld\+json["'])[^>]*>(.*?)</script>"""
        for match in re.finditer(jsonld_script_pattern, raw, re.S | re.I):
            try:
                schemas.append(json.loads(match.group(1)))
            except json.JSONDecodeError as exc:
                raise SystemExit("Invalid JSON-LD in " + path + ": " + str(exc))
        web_page = next((s for s in schemas if isinstance(s, dict) and s.get("@type") in ("WebPage", "AboutPage", "ProfilePage")), None)
        if web_page is None:
            web_page = {"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical}
            schemas.append(web_page)
        # Google requires a genuine app rating or review for SoftwareApplication rich results.
        # The site has no verified public app reviews, so remove this optional rich-result type
        # while transferring truthful author/publisher/citation links to the page entity.
        # Preserve the original page object because the sanitizer transfers those links to it.
        schemas = remove_ineligible_software_app(schemas)
        page_schema_types = ("WebPage", "AboutPage", "ProfilePage")
        matching_page_index = next((i for i, item in enumerate(schemas)
                                    if isinstance(item, dict)
                                    and item.get("@type") in page_schema_types
                                    and ((web_page.get("@id") and item.get("@id") == web_page.get("@id"))
                                         or (web_page.get("url") and item.get("url") == web_page.get("url")))), None)
        if matching_page_index is None:
            matching_page_index = next((i for i, item in enumerate(schemas)
                                        if isinstance(item, dict) and item.get("@type") in page_schema_types), None)
        if matching_page_index is None:
            schemas.append(web_page)
        else:
            # The sanitizer returns rebuilt dictionaries. Reinsert the original page node so
            # its transferred author/publisher/citation fields and subsequent metadata updates
            # are the same object that gets serialized, without duplicating a page entity.
            schemas[matching_page_index] = web_page
        web_page["name"] = title
        web_page["url"] = canonical
        # Keep dateModified only for pages with an explicit, page-specific substantive update.
        verified_date = VERIFIED_PAGE_UPDATE_DATES.get(path)
        for item in schemas:
            if isinstance(item, dict) and item.get("@type") in ("WebPage", "AboutPage", "ProfilePage"):
                if verified_date:
                    item["dateModified"] = verified_date
                else:
                    item.pop("dateModified", None)
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
        title_limit = 63 if path == "/date-calculator/" else 59
        if len(title) > title_limit:
            raise SystemExit("Title exceeds " + str(title_limit) + " characters: " + path)
        if not 70 <= len(descriptions[path]) <= 160:
            raise SystemExit("Description outside 70-160 characters: " + path + " (" + str(len(descriptions[path])) + ")")
    indexable = sorted(path for path in paths if path not in noindex)
    noindex_list = sorted(noindex)
    Path("indexable.txt").write_text("\n".join(indexable) + "\n", encoding="utf-8")
    Path("noindex.txt").write_text("\n".join(noindex_list) + ("\n" if noindex_list else ""), encoding="utf-8")
    Path("urls.txt").write_text("\n".join(SITE + path for path in indexable) + "\n", encoding="utf-8")
    Path("no-slash.txt").write_text("\n".join(NO_SLASH_PATHS) + "\n", encoding="utf-8")
    indexable_urls = {SITE + path for path in indexable}
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    ET.register_namespace("xhtml", "http://www.w3.org/1999/xhtml")
    urlset = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    for path in indexable:
        raw = paths[path].read_text(encoding="utf-8")
        canonical = SITE + path
        node = ET.SubElement(urlset, "{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        ET.SubElement(node, "{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text = canonical
        for code, href in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', raw):
            if href in indexable_urls:
                ET.SubElement(node, "{http://www.w3.org/1999/xhtml}link", {"rel":"alternate","hreflang":code,"href":href})
    ET.indent(urlset, space="  ")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding="unicode") + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: OAI-SearchBot\nAllow: /\nDisallow: /404\n\n"
        "User-agent: *\nAllow: /\nDisallow: /404\n\n"
        "Sitemap: " + SITE + "/sitemap.xml\n",
        encoding="utf-8",
    )
    report = ["SEO build report", "Freshness metadata: dateModified set only for verified page-specific updates; sitemap lastmod omitted", "Indexable pages: " + str(len(indexable)),
              "Noindex pages: " + str(len(noindex_list)), "Sitemap URLs: " + str(len(indexable)),
              "Titles: unique and within page-specific limits", "Descriptions: unique, page-specific and 70-160 characters",
              "JSON-LD: parsed and serialized as valid JSON", "Hub decisions:"]
    report.extend("  " + p + ": " + ("noindex" if p in noindex else "indexable") for p in sorted(HUB_PATHS))
    Path("seo-build-report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
