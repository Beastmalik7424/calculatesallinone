#!/usr/bin/env python3
"""Site-side AdSense policy checks for calculateallinone. Checks headings, exact
phrases and date format. Does not check word counts (see tests/content-gates.py)."""
import re
import html
import sys
from pathlib import Path

ROOT = Path("public")
TOOLS_WITH_EXAMPLE = ["stopwatch", "tasbih-counter", "query-calculator", "ratio-calculator"]
AFFILIATE_PHRASE = "Advertising is not enabled on the site at present"
ERRORS = []


def page_text(path):
    raw = (ROOT / path / "index.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()


def has_heading(path, name):
    raw = (ROOT / path / "index.html").read_text(encoding="utf-8")
    return re.search(r"<h[1-6][^>]*>\s*" + re.escape(name) + r"\s*</h[1-6]>", raw) is not None


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


all_html = "".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("index.html"))
check("Marketplace guide" not in all_html, "built pages still mention 'Marketplace guide'")
check('href="/marketplaces/"' not in all_html, "a link to /marketplaces/ still exists")

check("malikadeelbhatti@gmail.com" in page_text("contact"), "/contact/ does not show the contact email")
check(AFFILIATE_PHRASE in page_text("affiliate-disclosure"),
      "/affiliate-disclosure/ must contain the exact phrase: " + AFFILIATE_PHRASE)


privacy_text = page_text("privacy")
affiliate_text = page_text("affiliate-disclosure")
terms_text = page_text("terms")
check("No Google AdSense ad units are currently displayed" in privacy_text,
      "/privacy/ must distinguish the current no-ad state from future advertising.")
check("does not currently load the AdSense ad-serving script" in privacy_text,
      "/privacy/ must accurately describe the current inactive ad-code state.")
check("CalculatesAll may show advertising served by Google AdSense" not in privacy_text,
      "/privacy/ must not imply that AdSense is currently active.")
check("No AdSense ad units are currently displayed" in affiliate_text,
      "/affiliate-disclosure/ must accurately state that no ad units are active.")
check("does not currently load the AdSense ad-serving script" in affiliate_text,
      "/affiliate-disclosure/ must distinguish publisher verification from active ad serving.")
check("Advertising is not currently displayed" in terms_text,
      "/terms/ must not imply that advertising is already being displayed.")
check("Advertising may appear on some pages" not in terms_text,
      "/terms/ must not use ambiguous present/future advertising language.")

for slug in TOOLS_WITH_EXAMPLE:
    for name in ("Worked example", "Method", "Limits"):
        check(has_heading(slug, name), f"/{slug}/ has no heading exactly '{name}'")

for p in ROOT.rglob("index.html"):
    m = re.search(r"Last updated:\s*(\d{4}-\d{2}-\d{2})(?=\s|<)", p.read_text(encoding="utf-8"))
    if m:
        check(re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1)) is not None,
              f"{p}: 'Last updated' is not YYYY-MM-DD")

# Regression gates for the two pages where the live preview exposed repeated
# explanations. These checks target duplicate sections, not arbitrary word counts.
discount_html = (ROOT / "discount-calculator" / "index.html").read_text(encoding="utf-8")
for repeated_heading in (
    "Single discount worked example",
    "Stacked discounts",
    "Successive discounts worked example",
):
    check(not has_heading("discount-calculator", repeated_heading),
          f"/discount-calculator/ repeats the concept in '{repeated_heading}'")

savings_formula_count = discount_html.count("Amount saved equals original price multiplied by the discount percentage, divided by 100.")
check(savings_formula_count == 1,
      f"/discount-calculator/ must show its primary savings formula exactly once (found {savings_formula_count})")
final_price_formula_count = discount_html.count("Final price equals original price minus the amount saved.")
check(final_price_formula_count == 1,
      f"/discount-calculator/ must show its final-price formula exactly once (found {final_price_formula_count})")

profit_html = (ROOT / "profit-loss-calculator" / "index.html").read_text(encoding="utf-8")
for repeated_heading in (
    "Profit and loss in a business",
    "Example with a loss",
    "More common mistakes",
    "Profit loss calculator: cost versus selling price",
    "Profit margin versus markup: practical comparison",
):
    check(not has_heading("profit-loss-calculator", repeated_heading),
          f"/profit-loss-calculator/ repeats material already explained in '{repeated_heading}'")
check(has_heading("profit-loss-calculator", "Pakistan shop example: include direct selling costs"),
      "/profit-loss-calculator/ must retain its distinctive local-cost example")

# Urdu content must accurately describe the calculator modes exposed in the UI.
ur_profit = page_text("ur/profit-loss-calculator")
check("یہ کیلکولیٹر قیمت خرید پر فیصد دکھاتا ہے۔" not in ur_profit,
      "/ur/profit-loss-calculator/ must not claim that every percentage uses cost as its base")
for phrase in ("کاروباری موڈ", "آپریٹنگ منافع", "آپریٹنگ مارجن", "مارک اپ", "مجموعی مارجن", "PKR 880", "PKR 1,100", "PKR 220"):
    check(phrase in ur_profit, "/ur/profit-loss-calculator/ is missing mode-specific explanation or the verified PKR example: " + phrase)

ur_standard = page_text("ur/standard-calculator")
check("نہیں۔ یہ روزمرہ کے بنیادی حساب کے لیے ہے۔" not in ur_standard,
      "/ur/standard-calculator/ must not deny the Scientific Mode that the UI provides")
for phrase in ("سائنسی موڈ", "قوت", "جذر", "لوگارتھم", "فیکٹوریل", "DEG", "RAD"):
    check(phrase in ur_standard, "/ur/standard-calculator/ is missing a supported Scientific Mode explanation: " + phrase)

ur_discount = page_text("ur/discount-calculator")
check("ٹیکس آخری قیمت کے بعد شامل کریں۔" not in ur_discount,
      "/ur/discount-calculator/ must not present one universal tax order")
check("PKR 3,240" in ur_discount,
      "/ur/discount-calculator/ must retain one concrete successive-discount example")
check("ٹیکس کی بنیاد دکان اور مقامی قواعد کے مطابق مختلف ہو سکتی ہے" in ur_discount,
      "/ur/discount-calculator/ must state that tax treatment varies and is excluded")

ur_stopwatch = page_text("ur/stopwatch")
check("ٹیب بدلنے پر بھی وقت درست رہتا ہے" not in ur_stopwatch,
      "/ur/stopwatch/ must not guarantee accuracy when background-tab scheduling is variable")
check("پس منظر میں ٹیب کی تازہ کاری میں تاخیر ہو سکتی ہے" in ur_stopwatch,
      "/ur/stopwatch/ must explain the background-tab display limitation")

for e in ERRORS:
    print("FAIL:", e)
print(f"{len(ERRORS)} failing checks")
sys.exit(1 if ERRORS else 0)
