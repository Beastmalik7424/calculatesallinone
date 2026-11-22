import hashlib
import html
import json
import os
import shutil

from content_v5 import GUIDE_EXTRA, HOME_EXTRA, REVIEW_STATUS, TRUST_EXTRA
from urdu_v5 import URDU_EXTRA
from content_v13 import HUB_EXTRA, TERMS_PARAS, CONTACT_EXTRA, ABOUT_EXTRA
from lang_v6 import LANGS, UI

REVIEWERS_PATH = "reviewers.json"
REVIEWERS = json.load(open(REVIEWERS_PATH, encoding="utf-8")) if os.path.exists(REVIEWERS_PATH) else {}
from datetime import date

SITE_URL = os.environ.get("SITE_URL", "https://calculateallinone.vercel.app").rstrip("/")
ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "ca-pub-9453966537556063").strip()
ADSENSE_SLOT = os.environ.get("ADSENSE_SLOT", "").strip()
# Explicitly fail closed until the publisher confirms account-side consent setup.
# This flag is a safeguard, not an automated check of AdSense/CMP account settings.
ADSENSE_CONSENT_READY = os.environ.get("ADSENSE_CONSENT_READY", "").strip().lower() == "true"
if ADSENSE_SLOT and not ADSENSE_SLOT.isdigit():
    raise SystemExit("ADSENSE_SLOT must contain digits only, using the slot ID from your AdSense ad unit")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "malikadeelbhatti@gmail.com").strip()
SITE_DESCRIPTION = "Free browser-based calculators and everyday utility tools for people worldwide, covering arithmetic, business figures, dates, unit conversions and everyday tasks."
# Visible dates reflect the latest substantive content update for each page.
LASTMOD = {
    "/zakat-calculator/": "2026-11-16",
    "/years-to-days-calculator/": "2026-11-22",
    "/unit-converter/": "2026-11-21",
    "/tasbih-counter/": "2026-11-21",
    "/profit-loss-calculator/": "2026-11-21",
    "/ur/bmi-calculator/": "2026-11-21",
    "/query-calculator/": "2026-11-19",
}
OUT = "public"
STATIC = "static"


def css_asset_version():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), STATIC, "site.css")
    with open(css_path, "rb") as css_file:
        return hashlib.sha256(css_file.read()).hexdigest()[:16]


CSS_ASSET_VERSION = css_asset_version()

L = "block text-base font-medium text-stone-800 dark:text-stone-200 mb-1"
I = "w-full rounded-lg border border-stone-400 dark:border-stone-400 bg-white dark:bg-stone-900 px-3 py-3 text-base min-h-[44px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
B = "bg-gradient-to-r from-sky-700 to-indigo-700 hover:from-sky-800 hover:to-indigo-800 text-white text-base font-semibold px-5 py-3 rounded-xl min-h-[44px] shadow-md focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
B_ZAKAT = "bg-teal-700 hover:bg-teal-800 dark:bg-teal-700 dark:hover:bg-teal-600 text-white text-base font-semibold px-5 py-3 rounded-xl min-h-[44px] shadow-md focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700"
S = "border border-stone-500 dark:border-stone-400 text-stone-900 dark:text-stone-100 text-base font-medium px-5 py-3 rounded-lg min-h-[44px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
R = "mt-6 rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5 text-base leading-relaxed min-h-[3rem]"
H2 = "text-2xl font-bold text-indigo-800 dark:text-indigo-200 mt-12"
P = "mt-3 text-base leading-relaxed text-stone-800 dark:text-stone-200"
LINK = "underline text-sky-800 dark:text-sky-300 hover:text-sky-950"

NOTICE_BADGES = {
    ("en", "bmi-calculator"): (
        "Not a diagnosis",
        "BMI is a screening measure, not a diagnosis. It does not directly measure body fat. See CDC guidance."
    ),
    ("ur", "bmi-calculator"): (
        "تشخیص نہیں",
        "BMI صرف اسکریننگ ہے، تشخیص نہیں۔ یہ جسمانی چربی براہِ راست نہیں ناپتا۔"
    ),
}


def notice_badge(slug, language):
    notice = NOTICE_BADGES.get((language, slug))
    if not notice:
        return ""
    label, detail = notice
    return (
        '<span class="ml-2 inline-block whitespace-nowrap rounded-full border border-amber-300 bg-amber-50 px-1.5 py-0.5 text-[10px] leading-none font-semibold text-amber-950 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100" role="note" aria-label="'
        + html.escape(detail, quote=True) + '" title="' + html.escape(detail, quote=True) + '">'
        + label + "</span>"
    )


def attach_notice_badge(ui, slug, language):
    badge = notice_badge(slug, language)
    if not badge:
        return ui
    if slug == "bmi-calculator":
        return ui.replace("</legend>", badge + "</legend>", 1)
    return ui



def field(fid, label, step="0.01", hint="", autocomplete="off"):
    h = ""
    if hint:
        h = '<p class="text-sm text-stone-700 dark:text-stone-300 mt-1">' + hint + "</p>"
    autocomplete_attr = (' autocomplete="' + html.escape(autocomplete, quote=True) + '"') if autocomplete else ""
    return ('<div><label class="@L@" for="' + fid + '">' + label + '</label>'
            '<input id="' + fid + '" name="' + fid + '" class="@I@" type="number" min="0" step="' + step + '" inputmode="decimal"' + autocomplete_attr + '>' + h + "</div>")


def check(fid, label):
    return ('<label class="flex items-start gap-3 text-base text-stone-900 dark:text-stone-100 min-h-[44px]">'
            '<input id="' + fid + '" type="checkbox" class="mt-1 h-5 w-5"> <span>' + label + "</span></label>")


def result(rid, initially_hidden=False):
    hidden = " hidden" if initially_hidden else ""
    return '<div id="' + rid + '" class="@R@" aria-live="polite"' + hidden + '></div>'


BMI_UI = (
    '<form id="bmi-form" class="space-y-5" novalidate>'
    '<fieldset class="space-y-2"><legend class="@L@">Weight unit</legend>'
    '<div class="flex flex-wrap gap-4">'
    '<label class="flex min-h-[44px] items-center gap-2 text-base text-stone-900 dark:text-stone-100"><input id="bmi-weight-kg" type="radio" name="bmi-weight-unit" value="kg" checked class="h-5 w-5"><span>Kilograms (kg)</span></label>'
    '<label class="flex min-h-[44px] items-center gap-2 text-base text-stone-900 dark:text-stone-100"><input id="bmi-weight-lb" type="radio" name="bmi-weight-unit" value="lb" class="h-5 w-5"><span>Pounds (lb)</span></label>'
    '</div></fieldset>'
    '<div id="bmi-weight-kg-group">'
    '<div><label class="@L@" for="b-kg">Weight (kg)</label>'
    '<input id="b-kg" name="b-kg" class="@I@" type="text" inputmode="decimal" pattern="[0-9]+([.][0-9]+)?" autocomplete="off" spellcheck="false" aria-describedby="b-kg-error">'
    '<p id="b-kg-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div></div>'
    '<div id="bmi-weight-lb-group" class="!hidden" aria-hidden="true">'
    '<div><label class="@L@" for="b-lb">Weight (lb)</label>'
    '<input id="b-lb" name="b-lb" class="@I@" type="text" inputmode="decimal" pattern="[0-9]+([.][0-9]+)?" autocomplete="off" spellcheck="false" aria-describedby="b-lb-error" disabled>'
    '<p id="b-lb-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div></div>'
    '<fieldset class="space-y-2"><legend class="@L@">Height unit</legend>'
    '<div class="flex flex-wrap gap-4">'
    '<label class="flex min-h-[44px] items-center gap-2 text-base text-stone-900 dark:text-stone-100"><input id="bmi-height-cm" type="radio" name="bmi-height-unit" value="cm" checked class="h-5 w-5"><span>Centimeters (cm)</span></label>'
    '<label class="flex min-h-[44px] items-center gap-2 text-base text-stone-900 dark:text-stone-100"><input id="bmi-height-ftin" type="radio" name="bmi-height-unit" value="ftin" class="h-5 w-5"><span>Feet and inches</span></label>'
    '</div></fieldset>'
    '<div id="bmi-metric" class="grid sm:grid-cols-2 gap-4">'
    '<div><label class="@L@" for="b-cm">Height (cm)</label>'
    '<input id="b-cm" name="b-cm" class="@I@" type="text" inputmode="decimal" pattern="[0-9]+([.][0-9]+)?" autocomplete="off" spellcheck="false" aria-describedby="b-cm-error">'
    '<p id="b-cm-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div>'
    '</div>'
    '<div id="bmi-imperial" class="grid sm:grid-cols-2 gap-4 !hidden" aria-hidden="true">'
    '<div><label class="@L@" for="b-ft">Height (ft)</label>'
    '<input id="b-ft" name="b-ft" class="@I@" type="text" inputmode="numeric" pattern="[0-9]+" autocomplete="off" spellcheck="false" aria-describedby="b-ft-error" disabled>'
    '<p id="b-ft-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div>'
    '<div><label class="@L@" for="b-in">Height (in, 0 to 11.99)</label>'
    '<input id="b-in" name="b-in" class="@I@" type="text" inputmode="decimal" pattern="[0-9]+([.][0-9]+)?" autocomplete="off" spellcheck="false" aria-describedby="b-in-error" disabled>'
    '<p id="b-in-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div>'
    '</div>'
    '<button type="submit" class="@B@">Calculate BMI</button></form>'
    + result("bmi-result")
)

TOOLS = [
    {
        "slug": "zakat-calculator",
        "category": "money",
        "name": "Zakat Calculator",
        "app": "FinanceApplication",
        "description": "Estimate Hanafi Zakat on eligible cash, gold, silver, trade stock and recoverable receivables, or Sayyid Sistani's limited Ja'fari business-goods method. Enter metal prices.",
        "h1": "Zakat Calculator: Hanafi and Ja'fari (Sayyid Sistani)",
        "lead": "No sign-up is required. Your calculation runs in this browser, and you enter metal prices yourself because live market rates are not fetched. Choose one of two separate methods: Sunni Hanafi or the specific Ja'fari trading-goods ruling published by Sayyid Sistani. Enter gold and silver prices per gram or per the clearly defined Sindh-standard tola. Review the method, source notes and exclusions before relying on the estimate.",
        "ui": (
            '<form id="zakat-form" class="ca-calculator-engine w-full max-w-xl mx-auto pb-20" novalidate>'
            + '<div data-zakat-primary>'
            + '<div class="zakat-section space-y-2" data-zakat-step="setup">'
            + '<p id="zakat-hanafi-setup-note" class="text-xs leading-tight text-stone-700 dark:text-stone-300">Choose a silver or gold Nisab method. The 2.5% estimate applies only when the selected threshold and Hawl conditions are met.</p>'
            + '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2">'
            + '<div><label class="@L@" for="z-currency">Currency code (ISO 4217)</label>'
            + '<input id="z-currency" name="z-currency" class="@I@" type="text" value="PKR" maxlength="3" minlength="3" pattern="[A-Za-z]{3}" autocapitalize="characters" autocomplete="off" spellcheck="false">'
            + '</div>'
            + '<div><label class="@L@" for="z-school-of-thought">School of thought / calculation method</label>'
            + '<select id="z-school-of-thought" name="z-school-of-thought" class="@I@">'
            + '<option value="sunni-hanafi" selected>Sunni — Hanafi</option>'
            + '<option value="jafari-sistani">Shia Ja\'fari — Sayyid Sistani</option>'
            + '</select>'
            + '</div>'
            + '</div></div>'
            + '<div id="z-sunni-fields" class="zakat-section space-y-2" data-zakat-step="nisab">'
            + '<div><label class="@L@" for="z-nisab-method">Nisab method</label>'
            + '<select id="z-nisab-method" name="z-nisab-method" class="@I@">'
            + '<option value="silver" selected>Silver Nisab (612.36 g, South Asian classical conversion)</option>'
            + '<option value="gold-87">Gold Nisab (87.48 g, South Asian classical conversion)</option>'
            + '</select></div></div>'
            + '<div id="z-jafari-nisab-primary" hidden><label class="@L@" for="z-jafari-nisab-method">Trading-goods Nisab reference</label>'
            + '<select id="z-jafari-nisab-method" name="z-jafari-nisab-method" class="@I@">'
            + '<option value="gold" selected>Gold: 69.12 g (15 common mithqals)</option>'
            + '<option value="silver">Silver: 483.84 g (105 common mithqals)</option>'
            + '</select></div>'
            + '</div>'
            + '<details open class="zakat-advanced mt-2 rounded-xl border border-stone-200 dark:border-stone-700 p-2">'
            + '<summary class="min-h-[44px] cursor-pointer flex items-center font-semibold text-stone-900 dark:text-stone-100">Additional assets, metal prices and conditions</summary>'
            + '<p class="mt-2 text-sm text-stone-700 dark:text-stone-300">Examples: PKR, USD, GBP, EUR, SAR, AED, INR. Use one currency for every amount and metal price.</p>'
            + '<p class="text-sm text-stone-700 dark:text-stone-300">Choose the method you follow. The Shia Ja\'fari option is specifically limited to Sayyid Sistani\'s published rulings, not every Ja\'fari authority.</p>'
            + '<div id="z-sunni-asset-fields" class="space-y-3">'
            + '<div class="zakat-section space-y-3" data-zakat-step="sunni-assets-a">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Eligible assets</h2>'
            + '<p class="text-sm text-stone-700 dark:text-stone-300">Enter market values in the selected currency. Leave categories you do not own at zero.</p>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-cash", "Cash held at home")
            + field("z-bank", "Bank and current account balances")
            + field("z-savings", "Savings, deposits and cash equivalents")
            + '</div></div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="sunni-assets-b">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Gold, silver and jewellery</h2>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-gold", "Eligible gold value")
            + field("z-silver", "Eligible silver value")
            + field("z-jewellery", "Permissible personal-use gold/silver jewellery")
            + '</div></div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="sunni-assets-c">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Business assets</h2>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-businesscash", "Business cash and bank balance")
            + field("z-stock", "Trade inventory at current sale value", autocomplete="off")
            + '</div></div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="sunni-assets-d">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Recoverable receivables</h2>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-recv", "Recoverable loans and receivables")
            + '</div></div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="sunni-assets-e">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Property held for resale</h2>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-property", "Property held for resale (only if bought for resale)")
            + '</div></div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="sunni-liabilities">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Liabilities and payments</h2>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-debts", "Eligible short-term debts and dues")
            + field("z-paid", "Zakat already paid for this Zakat year")
            + '</div>'
            + check("z-hawl", "One full lunar Zakat year (hawl) is complete")
            + '</div></div>'
            + '<div id="z-jafari-fields" class="space-y-3" hidden>'
            + '<p class="text-sm text-stone-700 dark:text-stone-300">Sayyid Sistani only. This estimates qualifying trading goods under obligatory precaution. Ordinary banknotes and deposits are excluded. Khums is separate.</p>'
            + '<div class="zakat-section space-y-3" data-zakat-step="jafari-ownership">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Ownership conditions</h2>'
            + check("z-jafari-owner", "Owner remained adult and sane throughout the year")
            + '</div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="jafari-trade">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Trading goods</h2>'
            + field("z-jafari-trade-value", "Current market value of qualifying trading goods")
            + check("z-jafari-acquired", "Trading goods were acquired through a contract of exchange, such as a purchase")
            + '</div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="jafari-hawl-intent">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Hawl and profit intention</h2>'
            + check("z-jafari-hawl", "One full year has passed since the intention to profit began")
            + check("z-jafari-intent", "Intention to profit continued throughout the year")
            + '</div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="jafari-conditions">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Trading-goods conditions</h2>'
            + check("z-jafari-access", "Owner retained the right to dispose of the goods throughout the year")
            + check("z-jafari-market", "Market value did not fall below the purchase cost during the year")
            + '<p class="text-sm text-stone-700 dark:text-stone-300">This path excludes cash, banknotes, ordinary savings, personal jewellery, crops and livestock. It is not a complete Zakat or Khums assessment.</p>'
            + '</div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="jafari-coins">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Personal gold/silver coins</h2>'
            + check("z-jafari-coins-used-as-money", "These are minted gold/silver coins that are prevalently used as money in transactions")
            + '<div id="z-jafari-coin-inputs" class="space-y-3" hidden>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-jafari-gold-coins-weight", "Total minted gold-coin weight (selected unit)")
            + field("z-jafari-silver-coins-weight", "Total minted silver-coin weight (selected unit)")
            + '</div>'
            + check("z-jafari-gold-coins-hawl", "Gold coins remained at or above the first Nisab for 11 lunar months")
            + check("z-jafari-silver-coins-hawl", "Silver coins remained at or above the first Nisab for 11 lunar months")
            + check("z-jafari-coins-access", "Owner retained legal and actual right of disposal over these coins")
            + '<p class="text-sm text-stone-700 dark:text-stone-300">Only use this if the coins are minted and are actually used prevalently as money in transactions. Sistani states that gold and silver are not currently used as money. Ordinary banknotes, bank deposits, bullion bars and jewellery do not qualify. If unsure, leave this option off and consult Sistani&#39;s office.</p>'
            + '</div></div>'
            + '</div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="price-unit">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Metal price unit</h2>'
            + '<div><label class="@L@" for="z-metal-price-unit">Metal price unit</label>'
            + '<select id="z-metal-price-unit" name="z-metal-price-unit" class="@I@">'
            + '<option value="gram" selected>Price per gram</option>'
            + '<option value="tola">Price per Sindh Government standard tola (11.6638 g)</option>'
            + '<option value="ounce">Price per troy ounce (31.1034768 g)</option>'
            + '</select></div>'
            + '<p class="text-sm text-stone-700 dark:text-stone-300">Choose one unit and use it for both metal prices.</p>'
            + '</div>'
            + '<div class="zakat-section space-y-3" data-zakat-step="metal-prices">'
            + '<h2 class="text-lg font-semibold text-stone-900 dark:text-stone-100">Metal prices for Nisab</h2>'
            + '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-silverprice", "Silver price in selected unit")
            + field("z-goldprice", "24-karat gold price in selected unit")
            + '</div>'
            + '<p class="text-sm text-stone-700 dark:text-stone-300">Prices are converted to per-gram rates before Nisab is calculated. This is an estimate, not a fatwa.</p>'
            + '</div>'
            + '</details>'
            + '<div class="fixed inset-x-0 bottom-0 z-20 bg-white dark:bg-stone-900 border-t border-stone-200 dark:border-stone-700 px-3 pt-2 pb-2">'
            + '<button id="zakat-submit" type="submit" class="@B@ w-full max-w-xl mx-auto min-h-[44px]">Calculate Zakat</button>'
            + '</div>'
            + result("zakat-result", False)
            + '</form>'
        ),
        "guide": [
            ("What this calculator does", [
                "This calculator estimates annual Zakat on eligible monetary wealth. It adds the asset values you enter, subtracts the eligible liabilities you report, checks the remaining net wealth against the Nisab method you selected, and applies 2.5 percent when the conditions are met. It is a transparent arithmetic aid, not a religious ruling or a substitute for a scholar who understands your school of law and financial circumstances.",
                "Use the figures that apply on your own Zakat due date, usually the Hijri date on which your Zakat year completes. The date is personal to you. It is not automatically 1 January, the tax year, Ramadan, or the date you open this page. Keep a record of the date and the price sources you used so you can review the calculation next year."
            ]),
            ("Choose a Nisab method carefully", [
                "Nisab is the minimum qualifying threshold. This Hanafi calculator provides two reference choices commonly cited in South Asian Hanafi guidance: 612.36 g of silver or 87.48 g of gold. The initial selection is silver. The monetary threshold is the selected metal weight multiplied by the current price per gram you enter. These weights are fixed references; their cash value changes with the local market price. Select the basis advised by your qualified Hanafi scholar for your circumstances. Do not choose a method merely because it produces a lower or higher result.",
                "Enter the current local price per gram for the selected metal in the same currency as your assets. For silver Nisab, enter the silver price. For either gold Nisab option, enter a 24-karat gold price. This calculator does not fetch a live metal price or other live commodity prices, convert currencies, or claim that an old sample rate is today's rate. Confirm the metal price with a reliable local bullion or jewellers' source on your calculation date. Ask a qualified scholar which Nisab basis applies to your circumstances."
            ]),
            ("Hanafi method and calculation limits", [
                "Choose Sunni — Hanafi only if you follow the Hanafi school. The calculator defaults to the 612.36 g silver Nisab and also provides the 87.48 g gold reference. The silver and gold prices are entered separately, and the calculator converts a selected Sindh-standard tola quote to a per-gram price before valuing Nisab. The asset fields are a structured estimate, not an automatic religious classification of every holding. The liabilities field subtracts the amount you enter, but the tool cannot decide whether a specific loan, instalment or business liability is deductible under your circumstances. The Hawl checkbox is self-reported and does not track balances throughout the lunar year. This is not a complete Hanafi fiqh engine. Follow a qualified Hanafi scholar for personal rulings and exceptional cases.",
                "Pakistan-specific Hanafi note: Darul Ifta Banuri Town's fatwa 144608101364 (17 February 2025) says the 7.5-tola gold Nisab applies when gold is the only zakatable asset. If gold is held with cash, silver or trade goods, it tests the combined zakatable value against the 52.5-tola silver Nisab. This is that institution's published position, not a claim that every Hanafi authority uses the same rule. Follow the qualified scholar you trust. Source: [Banuri Town fatwa 144608101364](https://www.banuri.edu.pk/readquestion/144608101364/17-02-2025).",
                "For jewellery, enter only the eligible metal value. Do not enter the same jewellery value in both the jewellery field and the eligible gold or silver fields. Purity, stones, workmanship, trade use and personal use can affect valuation or classification. The calculator cannot inspect jewellery or determine its eligible weight. Obtain a reliable valuation and ask a qualified Hanafi scholar about uncertain cases."
            ]),
            ("Shia Ja'fari method: Sayyid Sistani", [
                "Choose Shia Ja'fari — Sayyid Sistani only if you follow this authority. His official rulings distinguish obligatory Zakat from Khums. The official Q&A says ordinary money saved in bank accounts and monetary bills do not carry obligatory Zakat under this method, while Khums may apply after annual expenses. Do not use the Sunni cash-and-bank calculation for this path.",
                "This calculator implements one limited Sistani path: trading goods acquired through a contract of exchange and held for profit, based on obligatory precaution. The official ruling requires the owner to be adult and sane; the goods to reach at least 15 common mithqals of coined gold or 105 common mithqals of coined silver; one year to pass from the intention to profit; the profit intention to continue throughout the year; the owner to retain the right of disposal; and the goods to remain saleable at or above their capital cost throughout the year. The official rate is one-fortieth, or 2.5 percent. The form checks these conditions and does not calculate an amount if any condition is unconfirmed.",
                "The Sistani trading-goods Nisab references used here are 69.12 g of gold and 483.84 g of silver. The calculator also has a separate optional input for minted gold/silver coins, but only when they are prevalently used as money in transactions and the owner meets the separate 11-lunar-month, adult/sane and disposal conditions. Ruling 1915 states that gold and silver are not currently used as money in transactions, so ordinary banknotes, bank deposits, bullion bars and jewellery are not included. This calculator does not cover every Sistani Zakat category, including agricultural produce and livestock, and it does not calculate Khums. Other Ja'fari maraji may have different rulings. Confirm your own marja's guidance before relying on an estimate."
            ]),
            ("Gram, Sindh Government standard tola and troy ounce price input", [
                "Choose the unit used by your jeweller: gram, Sindh Government standard tola (11.6638 g), or troy ounce (31.1034768 g). The calculator converts both entered metal prices to a per-gram rate before calculating Nisab. Some published Zakat guidance describes a 12.5 g Pakistani tola, so the 11.6638 g government standard is not a universal market convention. Confirm the actual gram basis with your jeweller.",
                "Use the same currency for assets and metal prices. The calculator does not fetch live rates. The selected unit applies to both gold and silver prices. Choose tola only for a quote based on 11.6638 g and troy ounce only for a quote based on 31.1034768 g. If a Pakistani market quote uses 12.5 g per tola or another basis, convert it to a per-gram price and select gram."
            ]),
            ("Illustrative small-shop Nisab comparison", [
                "Consider a hypothetical shop on its Zakat date: cash and bank balances total PKR 180,000, saleable trade stock at its current eligible value is PKR 520,000, and recoverable receivables are PKR 70,000. The PKR 180,000 cash figure already includes, for illustration, PKR 15,000 in JazzCash and PKR 20,000 in Easypaisa; count those available balances once, not again as separate assets. If eligible short-term supplier debts are PKR 120,000, the illustrative net wealth is PKR 180,000 + PKR 520,000 + PKR 70,000 − PKR 120,000 = PKR 650,000. This assumes the amounts qualify under the scholarly method the owner follows; shop equipment and personal-use assets are not added as trade stock. Ask a qualified scholar about restricted or disputed balances.",
                "To demonstrate the arithmetic only, suppose the local silver price were PKR 200 per gram and 24-karat gold were PKR 25,000 per gram. Silver Nisab at 612.36 g would be PKR 122,472. Gold Nisab at 87.48 g would be PKR 2,187,000. These sample prices are hypothetical, not a live market quote, and must not be used as today's metal prices.",
                "At PKR 650,000, the example exceeds the illustrative silver threshold but not either illustrative gold threshold. If the silver method is the one the owner has been advised to follow and the Hawl condition is met, 2.5% of PKR 650,000 is PKR 16,250 before subtracting any eligible Zakat already paid for that year. Under the Hanafi gold threshold in this example, the amount does not reach Nisab. This shows why the method must be selected according to qualified religious guidance before entering figures; do not choose a Nisab method based on which result is lower or preferred."
            ]),
            ("Which assets to include", [
                "Cash includes notes and coins you own. Bank balances include current, savings and similar accounts. Add other savings, fixed deposits, cash equivalents and money set aside for a future purchase when they remain your wealth. Avoid counting the same money twice. If a bank balance is already included in your savings total, do not enter it again in another field.",
                "Gold and silver should be entered at their eligible current monetary value, not at the original purchase price. Jewellery valuation can depend on the school of law, use, purity, stones and local practice. For mixed jewellery, estimate the metal value separately from stones and workmanship where appropriate. Do not assume that every scholar treats personal jewellery in the same way.",
                "Investments should reflect the zakatable portion and valuation method relevant to the investment and the scholarly approach you follow. Listed shares, funds, certificates and similar holdings may be treated differently depending on whether they are held for trading, investment income or long-term ownership. Do not automatically enter the full face value of a bond, retirement account or fund without checking its actual eligible value.",
                "Business owners can include business cash, bank balances, trade inventory valued at its current sale value, and receivables that are reasonably expected to be recovered. Do not enter machinery, shop fittings, tools, delivery vehicles or premises used to operate the business as trade inventory. A loan given to another person should only be included when recovery is expected under the method you follow.",
                "A pension or retirement account is included here only as the amount you can access or withdraw under the method you follow. Tax, penalties, vesting restrictions and access conditions can materially change that amount. Cryptocurrency is an optional field for holdings treated as zakatable wealth by the scholar or authority you follow. Property is included in this tool only when it is held for resale or trade. Property held for personal use or rental income needs a different analysis."
            ]),
            ("Which liabilities may be deducted", [
                "The liabilities field subtracts exactly the amount you enter. It does not decide whether a particular debt is deductible under Hanafi rulings. Enter only the amount your qualified Hanafi scholar says is eligible. Debt type, due date and repayment structure can change the ruling. Do not automatically subtract the full outstanding balance of a long-term loan.",
                "Enter only liabilities that your chosen scholarly approach permits you to deduct. Many contemporary calculation guides focus on debts and instalments due immediately or within the next twelve lunar months, including overdue bills, supplier invoices, rent, taxes and near-term instalments. The treatment of longer-term debts differs. Do not subtract the full outstanding balance of a long mortgage or student loan automatically when only near-term instalments may be deductible under the guidance you follow.",
                "Do not subtract future household spending that is not yet due, an estimate of ordinary living costs, or interest as though it were an eligible Zakat liability. If you have several debts, list only the amount due within the permitted period and avoid counting the same instalment twice. If you are unsure whether a debt is deductible, calculate both ways for discussion with a qualified scholar rather than presenting one disputed answer as universal."
            ]),
            ("How the calculation works", [
                "The arithmetic is: total eligible assets minus eligible liabilities equals net zakatable wealth. Net wealth cannot be less than zero in this estimate. The selected Nisab threshold equals the selected metal weight multiplied by the current price per gram you entered. If net wealth is below that threshold, the calculator reports that the threshold is not met. If net wealth reaches or exceeds the threshold but you have not confirmed completion of the lunar year, it explains that the Hawl condition is not confirmed.",
                "When the selected Nisab is met and you confirm that the lunar Zakat year is complete, the estimate applies 2.5 percent to net zakatable wealth. Zakat already paid for this same Zakat year is then subtracted from the calculated amount. The remaining balance cannot fall below zero. If the amount entered as already paid is greater than the calculated Zakat, the tool flags the excess for review rather than treating it as a negative payment."
            ]),
            ("Worked example with checkable arithmetic", [
                "Assume the values are all in PKR. Cash is 300,000, bank balances are 400,000, savings are 100,000, eligible gold is 150,000, business stock is 200,000, and recoverable receivables are 50,000. Total eligible assets are 1,200,000. Assume eligible short-term liabilities are 100,000. Net zakatable wealth is 1,200,000 minus 100,000, which equals 1,100,000.",
                "For illustration only, assume silver costs PKR 1,000 per gram on the Zakat date. Silver Nisab is 612.36 multiplied by 1,000, which equals PKR 612,360. Net wealth of PKR 1,100,000 is above that threshold. At 2.5 percent, the initial Zakat is PKR 27,500. If PKR 5,000 has already been paid toward this same Zakat year, the remaining balance is PKR 22,500. The example price is hypothetical and must not be reused as a current market quote."
            ]),
    ("Worked example: personal silver Nisab", ["Using a hypothetical silver price of PKR 3,000 per gram, 612.36 × 3,000 = PKR 1,837,080. If net wealth is PKR 700,000, it is below this personal silver Nisab and the estimate is zero. If net wealth is PKR 2,000,000, 2.5% is PKR 50,000."]),
                    ("Personal-use property and other exclusions", [
                "Personal-use belongings such as your main home, ordinary clothing, household furniture, personal car and tools used for your work are generally not treated as trade inventory in a basic monetary Zakat calculation. A property purchased with the intention of resale is different from the home in which you live. Rental property itself and the rent saved from it can be treated differently, so do not enter the entire value of a rental building in the resale-property field without qualified guidance.",
                "Agricultural produce, livestock, treasure, business structures, jointly owned assets and complex retirement arrangements can have separate Nisab rules, rates, dates or ownership tests. This calculator is not designed to calculate agricultural or livestock Zakat. It should not force every kind of wealth into a single 2.5 percent formula."
            ]),
            ("Review record", ["Last reviewed: 2026-11-16 by site maintainer Muhammad Fayyaz Adeel. This page was checked against the linked official and scholarly sources. It is not an independent scholar review or a fatwa."]),
            ("Pakistan bank deduction threshold is separate", [
                "For the 1447 AH (2026) Ramazan cycle, Pakistan's official notification identifies the Zakat year as 1446–1447 AH and sets PKR 503,529 as the threshold for source deduction from specified saving, profit and loss sharing (PLS), and similar bank accounts on the first day of Ramazan. The State Bank of Pakistan circular forwarded that notification to banks. This is a year-specific statutory bank-deduction threshold for the account types named in the notification. It is not a universal personal Zakat Nisab, does not replace your selected gold or silver method, and the bank deduction threshold changes yearly. Do not carry it forward to a later Zakat year without a new official notification.",
                "If you live in Pakistan, use the currency code PKR and check the latest Ministry of Poverty Alleviation and Social Safety or State Bank of Pakistan notice for the relevant Zakat year. Whether a bank deduction applies to your account can depend on the law, account type, declaration and applicable exemptions. Your personal Zakat calculation may be different from an automatic bank deduction."
            ]),
            ("Worldwide currency support, privacy and limitations", [
                "The currency field accepts a three-letter ISO 4217 currency code, such as PKR, USD, GBP, EUR, SAR, AED or INR, when the browser supports that currency. Every asset, liability and metal price must be entered in the same currency. The currency code changes how the result is labelled and formatted. It does not convert amounts between currencies. If you own assets in several currencies, convert them to one chosen currency using a reliable exchange rate for your Zakat date before entering them, and keep the conversion record.",
                "The calculator runs in your browser. It does not need your name, bank login, account number or personal financial documents. Do not enter sensitive account credentials. The page does not save your entries to a personal account or provide a secure financial record. Save your own calculation privately if you need a record. Browser support for currency formatting can vary, so use a standard ISO code supported by your device.",
                "This tool does not decide the religious status of every asset, whether a debt is deductible, whether jewellery is exempt, how jointly owned wealth is divided, how a pension is treated, or how missed Zakat from earlier years should be repaid. It does not calculate agricultural produce or livestock. Its result is only as reliable as the amounts, market prices, currency conversion and scholarly assumptions you enter. Consult a qualified local scholar for a personal ruling. The page is maintained by Muhammad Fayyaz Adeel. Last reviewed: 2026-11-16. Religious rulings are attributed to the named official and scholarly sources linked below; this page is not endorsed as a fatwa by a religious authority."
            ])
        ],
        "faq": [
            ("Which calculation method should I choose?", "Choose Sunni — Hanafi if you follow the Hanafi school. Choose Shia Ja'fari — Sayyid Sistani only if you follow his published rulings. These are separate calculation paths, not interchangeable versions of one formula. Other Ja'fari authorities and other Sunni schools may have different rulings and are not implemented by this calculator."),
            ("What does the Shia Ja'fari Sistani option calculate?", "It estimates qualifying trading goods under Sayyid Sistani's published obligatory-precaution ruling and, only if the strict conditions are met, minted gold/silver coins prevalently used as money in transactions. It checks the owner, Nisab, the applicable 11-month or one-year holding condition, disposal rights and business-goods market-value conditions. It does not calculate ordinary cash, banknotes, bank deposits, bullion, ordinary jewellery, Khums, crops or livestock."),
            ("Does Sistani's method apply obligatory Zakat to ordinary bank savings?", "His official Q&A says Zakat is not obligatory on ordinary bank deposits and monetary bills; Khums is a separate obligation and may apply to savings after annual expenses. Other Ja'fari authorities may differ."),
            ("Which metal price units can I use?", "Choose gram (1 g), Sindh Government standard tola (11.6638 g), or troy ounce (31.1034768 g). Select the unit that matches the jeweller’s quote. Some Pakistani quotes use 12.5 g per tola, which differs from the Sindh Government standard. For that quote, convert to a per-gram price and choose gram.")
        ],
        "sources": 'Primary and supporting references: <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/2317/" rel="noopener noreferrer">Sayyid Sistani official gold Nisab ruling</a>; <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/2318/" rel="noopener noreferrer">Sayyid Sistani official silver Nisab and coined-money rulings</a>; <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/8243/" rel="noopener noreferrer">Sayyid Sistani official mithqal weight conversion table</a>; <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/2323/" rel="noopener noreferrer">Sayyid Sistani official trading-goods conditions</a>; <a class="' + LINK + '" href="https://www.sistani.org/english/qa/14884/" rel="noopener noreferrer">Sayyid Sistani official bank-deposit and monetary-bill Q&amp;A</a>; <a class="' + LINK + '" href="https://islamqa.org/hanafi/answerstofatawa/118729/who-is-liable-to-pay-zakat/" rel="noopener noreferrer">Hanafi scholar reference for 87.48 g gold and 612.36 g silver Nisab</a>; <a class="' + LINK + '" href="https://islamqa.org/hanafi/darulfiqh/156652/" rel="noopener noreferrer">Hanafi jewellery guidance by Darulfiqh</a>; <a class="' + LINK + '" href="https://seekersguidance.org/answers/hanafi-fiqh/which-debts-affect-zakat-for-both-debtor-and-creditor/" rel="noopener noreferrer">Hanafi debt guidance and scholarly comparison</a>; <a class="' + LINK + '" href="https://sindhlaws.gov.pk/Setup/Publications_SindhCode/PUB-16-000006.pdf" rel="noopener noreferrer">Sindh Government official tola conversion table</a>; <a class="' + LINK + '" href="https://www.islamic-relief.org.uk/giving/islamic-giving/zakat/zakat-on-jewellery/" rel="noopener noreferrer">Islamic Relief jewellery and tola guidance</a>; <a class="' + LINK + '" href="https://nzfworldwide.com/wp-content/uploads/2022/03/NZF_Zakat-Calculation-Principle-No.1.pdf" rel="noopener noreferrer">NZF Worldwide Zakat calculation principles</a>; <a class="' + LINK + '" href="https://www.sbp.org.pk/circulars/bprd-circular-letter-no-03-of-2026" rel="noopener noreferrer">State Bank of Pakistan 2026 circular</a>. These sources describe named authorities and methods; they do not establish one ruling for every Muslim.'
    },
    {
        "slug": "bmi-calculator",
        "category": "health",
        "name": "BMI Calculator",
        "app": "HealthApplication",
        "description": "Calculate adult body mass index in metric or imperial units with WHO weight category ranges.",
        "h1": "BMI Calculator for Adults",
        "lead": "Calculate your body mass index in metric or imperial units. BMI is a screening measure for adults. It is not a diagnosis.",
        "ui": (
            '<form id="bmi-form" class="space-y-5" novalidate>'
            '<div><label class="@L@" for="bmi-unit">Units</label>'
            '<select id="bmi-unit" name="bmi-unit" class="@I@"><option value="metric">Metric (kg and cm)</option><option value="imperial">Imperial (lb and ft/in)</option></select></div>'
            '<div id="bmi-metric" class="grid sm:grid-cols-2 gap-4">'
            + field("b-kg", "Weight (kg)", step="0.1")
            + field("b-cm", "Height (cm)", step="0.1")
            + '</div>'
            '<div id="bmi-imperial" class="grid sm:grid-cols-2 gap-4 hidden">'
            + field("b-lb", "Weight (lb)", step="0.1")
            + '<div class="grid grid-cols-2 gap-3">'
            + field("b-ft", "Height (ft)", step="1")
            + field("b-in", "Height (in, 0 to 11.9)", step="0.1")
            + '</div></div>'
            '<button type="submit" class="@B@">Calculate BMI</button></form>'
            + result("bmi-result")
        ),
        "guide": [
            ("The formula", [
                "Weight can be entered in kilograms (kg) or pounds (lb), independently of the height unit. When kg is selected, BMI equals weight in kilograms divided by height in meters, squared.",
                "When lb is selected, BMI equals 703 multiplied by weight in pounds, divided by total height in inches, squared. The calculator converts feet and inches into total inches for this formula.",
                "If you select kg with feet and inches, the calculator converts the height to centimeters and uses the metric formula. Switching weight units clears the previous result so you can recalculate with the new unit.",
            ]),
            ("Adult weight categories", [
                "The World Health Organization uses these ranges for adults: below 18.5 is underweight, 18.5 to 24.9 is normal weight, 25.0 to 29.9 is overweight, and 30.0 or above is in the obesity range.",
            ]),
            ("Worked example, metric", [
                "A person weighs 70 kg and is 175 cm tall. Height in meters is 1.75. Squared, that is 3.0625.",
                "BMI equals 70 divided by 3.0625, which is 22.9 to one decimal place. This is in the normal weight range.",
            ]),
            ("Worked example, imperial", [
                "A person weighs 154 lb and is 5 ft 9 in tall. Total height is 69 inches.",
                "BMI equals 703 multiplied by 154, divided by 69 squared (4,761). The result is 22.7, which is in the normal weight range.",
            ]),
            ("Common mistakes", [
                "Entering height in feet with decimals. 5.9 feet is 5 feet 10.8 inches, not 5 feet 9 inches. Use feet and inches separately.",
                "Using BMI for children or teenagers. Their assessment uses age and sex specific percentile charts.",
                "Treating BMI as body fat. Muscle, frame size and age change what the same number means.",
            ]),
            ("When to speak to a clinician", [
                "BMI is a starting point. A doctor or qualified health professional can assess weight in the context of your history, waist size, blood pressure, blood tests and other factors.",
            ]),
        ],
        "faq": [
            ("Can I use this for children?", "No. This page covers adults. Children and teenagers are assessed with age and sex specific percentile charts."),
            ("Is BMI a diagnosis?", "No. It is a screening measure. Discuss your result with a doctor or qualified health professional."),
            ("What does 0 to 11.9 inches mean?", "Inches must be at least 0 and less than 12. For example, 5 ft 11 in is valid, while 5 ft 13 in is not."),
        ],
        "sources": 'Adult BMI categories follow the <a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" target="_blank" rel="noopener noreferrer">World Health Organization</a> classification. The <a class="' + LINK + '" href="https://www.nhs.uk/health-assessment-tools/calculate-your-body-mass-index/calculate-bmi-for-adults" target="_blank" rel="noopener noreferrer">NHS adult BMI calculator</a> explains ethnicity-specific interpretation. The <a class="' + LINK + '" href="https://www.nhs.uk/health-assessment-tools/calculate-your-waist-to-height-ratio" target="_blank" rel="noopener noreferrer">NHS waist-to-height ratio calculator</a> explains the half-height check. The <a class="' + LINK + '" href="https://doi.org/10.2337/doci26-0003" target="_blank" rel="noopener noreferrer">2026 Standards of Care in Overweight and Obesity</a> describes current clinical assessment criteria. The calculator itself continues to display the standard adult WHO categories and does not diagnose a condition.',
    },
    {
        "slug": "profit-loss-calculator",
        "category": "money",
        "name": "Profit and Loss Calculator",
        "app": "UtilitiesApplication",
        "description": "Free profit and loss calculator: calculate business net profit, profit margin, product profit percentage and markup from revenue, costs and selling price.",
        "h1": "Profit and Loss Calculator",
        "lead": "This profit loss calculator compares business operating profit with product-level profit or loss, markup and margin.",
        "ui": (
            '<form id="pl-form" class="space-y-5" novalidate>'
            '<fieldset class="ca-profit-modes"><legend class="@L@">Calculation type</legend>'
            '<div class="grid grid-cols-2 gap-2">'
            '<label class="ca-profit-mode"><input type="radio" name="pl-mode" value="business" checked> Business P&amp;L</label>'
            '<label class="ca-profit-mode"><input type="radio" name="pl-mode" value="product"> Product profit</label></div></fieldset>'
            '<div id="pl-business-fields" class="grid sm:grid-cols-2 gap-4">'
            + field("p-revenue", "Total revenue")
            + field("p-cogs", "Cost of goods sold")
            + field("p-expenses", "Other business expenses")
            + '</div>'
            '<div id="pl-product-fields" class="grid sm:grid-cols-2 gap-4" hidden>'
            + field("p-cost", "Cost price")
            + field("p-sell", "Selling price")
            + '</div><button type="submit" class="@B@">Calculate profit or loss</button></form>'
            + result("pl-result")
        ),
        "guide": [
            ("Business P&L formulas", [
                "Gross profit equals total revenue minus cost of goods sold. Net operating profit equals gross profit minus other business expenses.",
                "Net operating margin equals net operating profit divided by total revenue, multiplied by 100. When revenue is zero, margin is not available.",
                "This simplified operating P&L excludes separate interest and income tax calculations. Enter those amounts in other expenses only when appropriate.",
            ]),
            ("Product profit formulas", [
                "Product profit or loss equals selling price minus cost price. A negative result is a loss.",
                "Product markup percentage equals profit divided by cost price, multiplied by 100. Gross margin equals profit divided by selling price, multiplied by 100. Either percentage is unavailable when its denominator is zero.",
            ]),
            ("Worked example, profit", [
                "Cost price is 800. Selling price is 1,000. Profit is 200.",
                "Percentage is 200 divided by 800, multiplied by 100, which is 25 percent of cost.",
            ]),
            ("Worked example, loss", [
                "Cost price is 500. Selling price is 450. The result is a loss of 50.",
                "Percentage is minus 50 divided by 500, multiplied by 100, which is a loss of 10 percent of cost.",
            ]),
            ("Common mistakes", [
                "Calculating the percentage on selling price instead of cost. Margin on selling price is a different figure.",
                "Forgetting other costs such as shipping, packaging, platform fees and tax. Include them in cost price for a true result.",
            ]),
        ],
        "faq": [
            ("Why is margin different from markup?", "Product mode shows both markup on cost and gross margin on selling price. Business mode shows net operating margin on revenue."),
            ("Why does it show N/A?", "Product markup is unavailable when cost is zero. Business margin is unavailable when revenue is zero."),
        ],
        "sources": 'Formula references: <a class="' + LINK + '" href="https://openstax.org/books/introduction-business/pages/14-5-the-income-statement" target="_blank" rel="noopener noreferrer">OpenStax: The Income Statement</a> explains inventory, cost of goods sold, gross profit, operating expenses and why profit is not cash. <a class="' + LINK + '" href="https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f2/technical-articles/ratio-analysis.html" target="_blank" rel="noopener noreferrer">ACCA Ratio Analysis</a> explains gross and operating profit margin ratios. This calculator is a simplified estimate, not a formal financial statement.',
    },
    {
        "slug": "discount-calculator",
        "category": "money",
        "name": "Discount Calculator",
        "app": "UtilitiesApplication",
        "description": "Calculate the final sale price and the amount saved from an original price and a discount percentage.",
        "h1": "Discount Calculator",
        "lead": "Enter the original price and the discount percentage to see the amount you save and the final price.",
        "ui": (
            '<form id="disc-form" class="space-y-5" novalidate>'
            '<div class="grid sm:grid-cols-2 gap-4">'
            + field("d-price", "Original price")
            + field("d-pct", "Discount (%, 0 to 100)")
            + '</div><button type="submit" class="@B@">Calculate Discount</button></form>'
            + result("disc-result")
        ),
        "guide": [
            ("The formulas", [
                "Amount saved equals original price multiplied by the discount percentage, divided by 100.",
                "Final price equals original price minus the amount saved.",
            ]),
            ("Worked example", [
                "Original price is 2,500. Discount is 20 percent.",
                "Amount saved is 2,500 multiplied by 20, divided by 100, which is 500. Final price is 2,500 minus 500, which is 2,000.",
            ]),
            ("Common mistakes", [
                "Applying two discounts by adding their percentages. A 20 percent and a 10 percent discount in sequence give 28 percent in total, not 30 percent.",
                "Forgetting that tax is usually charged after the discount. This tool does not add tax.",
            ]),
        ],
        "faq": [
            ("Can the discount be above 100 percent?", "No. The discount must be between 0 and 100."),
            ("Does this include tax?", "No. Add tax to the final price if your store charges it after discounts."),
        ],
        "sources": "Standard percentage formulas.",
    },
    {
        "slug": "age-calculator",
        "category": "time",
        "name": "Age Calculator",
        "app": "UtilitiesApplication",
        "description": "Calculate exact age in years, months, days and total days from a date of birth.",
        "h1": "Age Calculator",
        "lead": "Enter your date of birth to see your exact age in years, months and days, plus the total number of days you have lived.",
        "ui": (
            '<form id="age-form" class="space-y-5" novalidate>'
            '<div><label class="@L@" for="a-dob">Date of birth</label>'
            '<input id="a-dob" name="dob" type="date" class="@I@"></div>'
            '<button type="submit" class="@B@">Calculate Age</button></form>'
            + result("age-result")
        ),
        "guide": [
            ("How the age is calculated", [
                "The calculator subtracts the birth date from today's date year by year, month by month and day by day.",
                "When the day count goes below zero, it borrows the number of days in the previous month. When the month count goes below zero, it borrows 12 months from the year.",
            ]),
            ("Worked example", [
                "Birth date is 15 March 1990. Calculation date is 8 October 2026.",
                "Years are 36. Months are 7, but the day count is minus 7, so one month is borrowed and September's 30 days are added. Result: 6 months and 23 days.",
                "Total days lived is 13,356.",
            ]),
            ("Common mistakes", [
                "Entering a date in the wrong order. Use the calendar date of birth as printed on your records.",
                "Expecting the age to change at a specific hour. The calculator compares calendar dates only.",
            ]),
        ],
        "faq": [
            ("Does it accept future dates?", "No. The date of birth must be today or earlier."),
            ("Does my time zone change the result?", "No. The calculator compares calendar dates, so the time of day does not change the result."),
        ],
        "sources": "Calendar arithmetic using the Gregorian calendar.",
    },
    {
        "slug": "unit-converter",
        "category": "math",
        "name": "Unit Converter",
        "app": "UtilitiesApplication",
        "description": "Convert weight, length and temperature units with validation for physical limits.",
        "h1": "Unit Converter for Weight, Length and Temperature",
        "lead": "Convert common weight, length and temperature units. Negative weights and lengths and temperatures below absolute zero are rejected.",
        "ui": (
            '<form id="conv-form" class="space-y-5" novalidate>'
            '<div class="grid sm:grid-cols-3 gap-4">'
            '<div><label class="@L@" for="u-cat">Category</label>'
            '<select id="u-cat" class="@I@"><option value="weight">Weight</option><option value="length">Length</option><option value="temp">Temperature</option></select></div>'
            + field("u-val", "Value", step="any")
            + '<div><label class="@L@" for="u-from">From</label><select id="u-from" class="@I@"></select></div>'
            + '</div>'
            '<div><label class="@L@" for="u-to">To</label><select id="u-to" class="@I@"></select></div>'
            '<button type="submit" class="@B@">Convert</button></form>'
            + result("conv-result")
        ),
        "guide": [
            ("How conversion works", [
                "Weight converts through kilograms and length converts through meters. Each unit has a fixed multiplier to the base unit.",
                "Temperature uses formulas rather than multipliers. Fahrenheit equals Celsius multiplied by 9 divided by 5, plus 32.",
            ]),
            ("Worked example", [
                "1 mile is 1,609.344 meters, which is 1.609344 kilometers.",
                "100 degrees Fahrenheit equals (100 minus 32) multiplied by 5 divided by 9, which is 37.78 degrees Celsius.",
            ]),
            ("Common mistakes", [
                "Mixing pounds and kilograms. 1 kilogram is about 2.2046 pounds, not 2.",
                "Entering a negative weight or length. Physical weight and length cannot be negative.",
            ]),
            ("Supported unit categories and choices", [
                "Weight: kilograms (kg), grams (g), pounds (lb) and ounces (oz). The pound and ounce options use avoirdupois mass units. Length: metres (m), centimetres (cm), kilometres (km), feet (ft), inches (in) and miles (mi). Temperature: Celsius (°C), Fahrenheit (°F) and Kelvin (K). These are the three categories currently supported by this converter.",
                "This tool does not currently convert area, volume, speed, time, pressure or digital data. Choose a converter that explicitly supports the quantity you need rather than treating unlike quantities as interchangeable."
            ]),
            ("The conversion formula and worked examples", [
                "Weight and length use a shared base unit. First convert the input to kilograms or metres, then convert from that base unit to the target unit. Result = value × source-unit factor ÷ target-unit factor. This keeps each conversion on one consistent path.",
                "For example, 1 kg = 2.20462 lb when rounded to six significant figures, and 1 mile = 1.609344 km (displayed as 1.60934 km at six significant figures). The international avoirdupois pound is exactly 0.45359237 kg. NIST Handbook 44 (2026), Appendix C, lists the exact pound-to-kilogram relationship.",
                "Temperature uses offset formulas rather than a single multiplier because Celsius, Fahrenheit and Kelvin have different zero points. °F = °C × 9/5 + 32; °C = (°F − 32) × 5/9; K = °C + 273.15. For example, 100°F = 37.78°C when rounded to two decimal places. See the <a class='" + LINK + "' href='https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9' target='_blank' rel='noopener noreferrer'>NIST Guide to the SI, Appendix B.9</a> for the published temperature conversion equations."
            ]),
            ("Precision, input limits and common mistakes", [
                "Weight and length results are displayed to six significant figures. Temperature results are displayed to two decimal places. A rounded display may not show every digit of an exact conversion factor, so do not interpret the number of displayed digits as a statement about measurement accuracy.",
                "Negative weight and length inputs are rejected. Celsius and Fahrenheit values may be negative, but no temperature can be below absolute zero. Absolute zero is -273.15°C (0 K). A value below that limit is rejected.",
                "Check that both selected units measure the same kind of quantity and that you selected the intended temperature scale. This tool converts mass, length and temperature only; it does not calculate density, area or volume."
            ]),
        ],
        "faq": [
            ("Why is a negative weight rejected?", "A physical weight or length cannot be negative. Temperature in Celsius and Fahrenheit can be negative."),
            ("Why is Kelvin rejected below zero?", "Zero Kelvin is absolute zero. No temperature can be lower."),
            ("Which units does the converter support?", "It supports kg, g, lb and oz for weight; m, cm, km, ft, in and mi for length; and °C, °F and K for temperature."),
            ("Why does temperature need a formula instead of a multiplier?", "Celsius, Fahrenheit and Kelvin have different zero points. Temperature conversions therefore need an offset as well as a scale factor, such as °F = °C × 9/5 + 32."),
            ("Is one pound exactly 0.45359237 kilograms?", "Yes. The international avoirdupois pound is exactly 0.45359237 kg. See NIST Handbook 44 (2026), Appendix C."),
            ("How many decimal places does the converter show?", "Weight and length results are shown to six significant figures. Temperature results are shown to two decimal places. The displayed result may therefore be rounded."),
            ("Can I convert area, volume or speed here?", "No. This converter currently supports weight, length and temperature only.")
        ],
        "sources": "Conversion factors follow standard SI and imperial definitions, for example 1 pound equals 0.45359237 kilograms exactly.",
    },
    {
        "slug": "standard-calculator",
        "category": "math",
        "name": "Standard & Scientific Calculator",
        "app": "UtilitiesApplication",
        "description": "Free online standard and scientific calculator with large buttons for addition, subtraction, percentages, trigonometry, square roots and logarithms.",
        "h1": "Online Standard and Scientific Calculator",
        "lead": "Use standard arithmetic or switch to Scientific Mode for trigonometry, powers, roots, logarithms and statistics. Calculations run in your browser.",
        "ui": (
            '<div class="max-w-sm mx-auto">'
            '<output id="calc-display" class="block text-right text-3xl font-semibold bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 rounded-xl px-4 py-5 min-h-[4rem] break-all" aria-live="polite">0</output>'
            '<div id="calc-pad" class="grid grid-cols-4 gap-3 mt-4">'
            '<button class="@S@" data-key="C">C</button>'
            '<button class="@S@" data-key="BS" aria-label="Delete last character">⌫</button>'
            '<button class="@S@" data-key="%">%</button>'
            '<button class="@S@" data-key="/" aria-label="Divide">÷</button>'
            '<button class="@S@" data-key="7">7</button>'
            '<button class="@S@" data-key="8">8</button>'
            '<button class="@S@" data-key="9">9</button>'
            '<button class="@S@" data-key="*" aria-label="Multiply">×</button>'
            '<button class="@S@" data-key="4">4</button>'
            '<button class="@S@" data-key="5">5</button>'
            '<button class="@S@" data-key="6">6</button>'
            '<button class="@S@" data-key="-" aria-label="Subtract">−</button>'
            '<button class="@S@" data-key="1">1</button>'
            '<button class="@S@" data-key="2">2</button>'
            '<button class="@S@" data-key="3">3</button>'
            '<button class="@S@" data-key="+" aria-label="Add">+</button>'
            '<button class="@S@" data-key="00">00</button>'
            '<button class="@S@" data-key="0">0</button>'
            '<button class="@S@" data-key=".">.</button>'
            '<button class="@B@" data-key="=">=</button>'
            '</div></div>'
        ),
        "guide": [
            ("How it calculates", [
                "The calculator follows standard order of operations. Multiplication and division are done before addition and subtraction.",
                "The percent key divides the last number you entered by 100. For example, 50 + 10% becomes 50 + 0.1.",
                "A minus sign at the start of an expression makes the first number negative, for example -5 + 3 equals -2.",
            ]),
            ("Worked example", [
                "Enter 2 + 3 × 4. Multiplication happens first: 3 × 4 is 12, then 2 + 12 is 14.",
            ]),
            ("Limits", [
                "Parentheses are supported. Use the ( and ) buttons to group calculations. The calculator follows standard operator precedence, with multiplication and division before addition and subtraction.",
            ]),
        ],
        "faq": [
            ("Is my data sent to a server?", "No. The calculation runs in your browser."),
            ("Why does it show Error?", "The expression is incomplete, such as a trailing operator, or it contains a division by zero."),
        ],
        "sources": "Standard arithmetic order of operations.",
    },
    {
        "slug": "tasbih-counter",
        "category": "worship",
        "name": "Tasbih Counter",
        "app": "UtilitiesApplication",
        "description": "Free online digital tasbih counter for dhikr and zikr with 33, 99 and custom targets. Tap to count on mobile or desktop; no app download needed.",
        "h1": "Free Online Tasbih Counter",
        "lead": "Count dhikr on this device. Choose a phrase and target, then undo a tap if needed.",
        "ui": (
            '<div class="ca-tasbih-shell max-w-lg mx-auto space-y-5" id="tasbih-app">'
            '<div class="ca-tasbih-settings">'
            '<div class="grid sm:grid-cols-2 gap-4">'
            '<div><label class="@L@" for="t-phrase">Dhikr phrase</label>'
            '<select id="t-phrase" class="@I@">'
            '<option value="SubhanAllah">SubhanAllah</option><option value="Alhamdulillah">Alhamdulillah</option>'
            '<option value="Allahu Akbar">Allahu Akbar</option><option value="Astaghfirullah">Astaghfirullah</option>'
            '<option value="La ilaha illallah">La ilaha illallah</option><option value="custom">Custom phrase</option></select></div>'
            '<div class="ca-tasbih-custom-phrase"><label class="@L@" for="t-custom-phrase">Custom phrase (up to 40 characters)</label>'
            '<input id="t-custom-phrase" class="@I@" type="text" maxlength="40" autocomplete="off" disabled aria-describedby="t-phrase-error">'
            '<p id="t-phrase-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div></div>'
            '<div><label class="@L@" for="t-target">Target</label>'
            '<select id="t-target" class="@I@"><option value="33">33</option><option value="99">99</option><option value="100">100</option><option value="custom">Custom target</option></select></div>'
            '<div id="t-custom-target-wrap" hidden><label class="@L@" for="t-custom-target">Custom target (1 to 10,000)</label>'
            '<input id="t-custom-target" class="@I@" type="text" inputmode="numeric" autocomplete="off" pattern="[0-9]+" aria-describedby="t-target-error">'
            '<p id="t-target-error" class="mt-1 text-sm text-red-700 dark:text-red-300" aria-live="polite"></p></div>'
            '</div>'
            '<output id="t-count" class="block text-center text-6xl sm:text-7xl font-semibold tabular-nums bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 rounded-xl py-8" aria-live="polite">0</output>'
            '<p id="t-progress" class="text-center text-base text-stone-800 dark:text-stone-200" aria-live="polite"></p>'
            '<p id="t-storage-note" class="text-sm text-amber-800 dark:text-amber-200" role="status" hidden>Saving is unavailable in this browser. Your count and selected settings stay in memory only until you leave or reload this page.</p>'
            '<button id="t-tap" type="button" aria-label="Count one" class="w-full min-h-[64px] @B@ text-xl">Count one</button>'
            '<div class="grid grid-cols-2 gap-3"><button id="t-undo" type="button" class="@S@">Undo</button>'
            '<button id="t-reset" type="button" class="@S@">Reset</button></div>'
            '<p class="text-sm text-stone-700 dark:text-stone-300"><span id="t-lifetime-label">Lifetime counted total:</span><output id="t-lifetime">0</output></p>'
            '<p class="text-sm text-stone-700 dark:text-stone-300">Keyboard: press Space or Enter to count when focus is not in a text field or control.</p>'
            '</div>'
        ),
        "guide": [
            ("What is a digital Tasbih counter?", [
                "A digital Tasbih or Dhikr counter records deliberate taps or supported key presses. It can help you track a personal count on a phone or computer, but it does not listen to or verify a recitation.",
                "Tasbih, Tasbeeh, Dhikr and Zikr are commonly used names or spellings associated with remembrance. Transliteration and usage can vary. This page is a counting aid, not a religious authority.",
            ]),
            ("How to use this online Tasbih counter", [
                "Choose one of the five preset phrases or select Custom phrase and enter up to 40 characters. Choose a preset target of 33, 99 or 100, or select Custom target and enter a whole number from 1 to 10,000. Targets are personal tracking settings.",
                "Press Count one once for each count you want to record. You can also press Space or Enter when focus is not inside another control or text field. The progress message shows how many counts remain. When the selected target is reached, the page displays a message and may briefly vibrate if your device and browser support vibration.",
                "Undo subtracts one from the current count when it is above zero. Reset requires confirmation before clearing the current count. The lifetime total tracks accepted taps separately from the current count.",
            ]),
            ("Five phrases and plain meanings", [
                "SubhanAllah is commonly translated as “Glory be to Allah.” This is a plain-language meaning, not a detailed commentary.",
                "Alhamdulillah is commonly translated as “Praise belongs to Allah” or “All praise is due to Allah.”",
                "Allahu Akbar is commonly translated as “Allah is greater” or “Allah is the Greatest.”",
                "Astaghfirullah means “I seek forgiveness from Allah.”",
                "La ilaha illallah means “There is no deity worthy of worship except Allah.” Transliteration and English wording can vary; consult a qualified teacher if you need a formal translation or pronunciation guidance.",
            ]),
            ("Saving and privacy", [
                "When browser storage is available, the current count, selected phrase and selected target, including a custom target, are saved locally in the same browser and device. The saved information does not sync across devices and is not uploaded to a server. Clearing site data, private browsing or browser restrictions can make saved values unavailable.",
                "If storage is unavailable, the counter can continue in memory during the current page visit, but values may be lost when you reload or leave. A target is a personal tracking setting, not a religious ruling or a claim that a particular number or reward is required.",
            ]),
            ("Worked example: target and remaining count", [
                "For a personal target of 99 presses and a current count of 67, the remaining amount is 99 - 67 = 32. Three groups of 33 presses make 3 x 33 = 99. This is an arithmetic example only; it does not prescribe a religious practice.",
            ]),
        ],
        "faq": [
            ("Is my count sent to a server?", "No. The count, phrase and target are stored in this browser on this device when storage is available. They are not uploaded to an account."),
            ("Does my count sync to another device?", "No. The saved values stay in this browser on this device. They do not sync to another browser or phone."),
            ("What happens if browser storage is unavailable?", "The counter can continue in memory during the current page visit. Reloading or leaving the page may lose the count and selected settings."),
            ("Can I use a custom phrase and target?", "Yes. Enter a custom phrase up to 40 characters and a whole-number target from 1 to 10,000. The counter records taps, not recitation."),
            ("What happens when I reach the target?", "The page shows a target-reached message and does not reset automatically. Press Reset and confirm if you want to clear the current count."),
            ("Can I count with a keyboard?", "Yes. Press Space or Enter when focus is not inside a form field or another control."),
        ],
        "sources": "This page documents the counter's functionality only. It does not provide religious rulings or establish a required phrase or repetition count. For religious guidance, consult a qualified scholar or trusted teacher.",
    },
    {
        "slug": "stopwatch",
        "category": "time",
        "name": "Online Stopwatch",
        "app": "UtilitiesApplication",
        "description": "Start, stop and reset a stopwatch with centisecond precision in your browser.",
        "h1": "Online Stopwatch",
        "lead": "Start, stop and reset a stopwatch with hundredths of a second. It runs in your browser tab.",
        "ui": (
            '<div class="max-w-sm min-w-0 mx-auto space-y-5 text-center">'
            '<output id="sw-display" class="block w-full min-w-0 text-[clamp(1.35rem,6vw,3rem)] font-semibold bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 rounded-xl py-8 px-1 tabular-nums" aria-live="off">00:00:00.00</output>'
            '<div class="grid grid-cols-3 gap-3">'
            '<button id="sw-start" class="@B@">Start</button>'
            '<button id="sw-stop" class="@B@">Stop</button>'
            '<button id="sw-reset" class="@S@">Reset</button>'
            '</div></div>'
        ),
        "guide": [
            ("How it works", [
                "The stopwatch reads the browser clock and shows elapsed time in hours, minutes, seconds and hundredths of a second.",
                "Elapsed time is calculated from the start time, so it stays accurate when you return to a tab that was in the background.",
            ]),
            ("Limits", [
                "This is suitable for everyday timing. Official sport or laboratory timing needs certified equipment.",
            ]),
            ("Use the stopwatch for repeatable everyday tasks", [
                "A browser stopwatch is useful for timing a study interval, workout set, cooking step or short work session. Press Start at the beginning, Stop when the interval ends, and Reset before a new attempt. If you compare repeated sessions, use the same start and stop method so the results are more meaningful.",
                "The display shows hundredths of a second, but that display precision is not the same as certified measurement accuracy. Browser scheduling, operating-system load and background-tab throttling can affect how often the screen refreshes. The elapsed-time calculation is based on the browser clock, yet this tool is not intended for official sporting results, laboratory experiments or legal evidence.",
                "This page does not store a history of completed timings. Record any result you need before resetting or reloading the page. If the task requires a verified split time, calibrated hardware or a formal timing protocol, use equipment designed for that purpose instead of relying on a general-purpose browser tool.",
            ]),
        ],
        "faq": [
            ("Does it keep running if I switch tabs?", "Yes. The elapsed time is calculated from the start time, so it stays accurate."),
            ("Is it accurate enough for sport timing?", "It is suitable for everyday timing. Official timing needs certified equipment."),
        ],
        "sources": "Uses the browser's high resolution clock.",
    },
]

HUB_CONTENT = {
    "money": {
        "intro": "Compare loan instalments, Zakat arithmetic, business profit, discounts and compound growth. Each tool states the inputs and method it uses. The worked examples below show how to check the arithmetic and where a calculator estimate differs from a lender quote, tax calculation or religious ruling.",
        "faq": [
            ("What does the EMI calculator estimate?", "It estimates the monthly instalment, total interest and repayment schedule from the loan amount, annual rate and term. Lender fees, insurance and contract-specific charges can change the amount quoted by a lender."),
            ("How is profit margin calculated?", "Gross margin = gross profit divided by sales revenue, multiplied by 100. With PKR 40,000 gross profit on PKR 100,000 sales, gross margin is 40% of sales. If operating profit is PKR 25,000, operating margin is 25% of sales. These measures use different profit figures and should not be confused."),
            ("Does the EMI estimate include lender fees?", "No. The EMI estimate uses the principal, annual interest rate and repayment term entered. Processing fees, insurance, variable-rate clauses, taxes and payment-date rules may change the lender's actual quotation."),
            ("Does the compound interest estimate include deposits or taxes?", "No. It assumes a fixed starting principal, a fixed nominal annual rate and the compounding frequency entered. It excludes additional deposits, withdrawals, fees, taxes and inflation. Check whether a provider quotes a nominal rate or an effective annual yield before comparing results."),
            ("Are these tools accurate for business accounts?", "They calculate the arithmetic for the inputs you give, but they do not replace an accountant. Tax rules, inventory valuation, payment fees and accounting policies are not included."),
            ("Does the Zakat calculator give a religious ruling?", "No. It lets you select a silver or gold Nisab reference, enter your own metal price and currency, and estimates the arithmetic when the stated conditions are met. Scholarly views can differ, so consult a qualified scholar about your circumstances."),
        ],
    },
    "health": {
        "intro": "The health tools on CalculatesAll give screening estimates, not diagnoses. The BMI calculator uses the standard formula, weight in kilograms divided by height in metres squared, and the adult weight categories published by the World Health Organization. Use the result as a starting point for a conversation with a doctor or another health professional.",
        "faq": [
            ("How is BMI calculated?", "BMI = weight (kg) ÷ height (m)². Example: a person who weighs 70 kg and is 1.75 m tall has BMI 70 ÷ (1.75 × 1.75) = 70 ÷ 3.06 = 22.9, which falls in the normal range of 18.5 to 24.9."),
            ("What are the adult BMI categories?", "The World Health Organization groups adults as underweight (below 18.5), normal (18.5 to 24.9), overweight (25.0 to 29.9) and obesity (30.0 and above)."),
            ("Should I use BMI to decide if I am healthy?", "BMI does not measure body fat or muscle directly. Athletes with high muscle mass often have a high BMI, and some adults with a normal BMI carry a high share of body fat. Discuss your result with a doctor."),
            ("Is BMI accurate for children and teenagers?", "No. The adult categories above apply to adults aged 18 and over. For children and teenagers, health professionals compare BMI with age- and sex-specific growth charts."),
            ("How do I calculate BMI in pounds and inches?", "BMI = 703 × weight (lb) ÷ height (in)². Example: 154 lb at 69 inches gives 703 × 154 ÷ 69² = 108,262 ÷ 4,761 = 22.7."),
        ],
    },
    "time": {
        "intro": "Choose a date or time tool: calculate age from calendar dates, find the days between two dates, convert years to days with a 365-day year, the Gregorian average or an exact start-date method, or convert days to years using a selected year length. Use the browser stopwatch for timing. Query Calculator also answers supported date, month and time-conversion questions in several languages.",
        "faq": [
            ("Does the age calculator use my time zone?", "No. It compares calendar dates only."),
        ],
    },
    "math": {
        "intro": "Choose the calculator by the question. The Standard & Scientific Calculator handles arithmetic expressions with brackets and order of operations. Scientific Mode also supports powers, roots, trigonometry, logarithms and statistics such as mean, median, sum, standard deviation and variance. Example: mean(1, 2, 3) = (1 + 2 + 3) ÷ 3 = 6 ÷ 3 = 2. Check: median(1, 2, 3) = 2. The Percentage Calculator finds a percentage of an amount, what percentage a part is of a whole, or the percentage change between two values. Example: 18% of 250 = 18 ÷ 100 = 0.18, then 250 × 0.18 = 45. Check: 10% of 250 = 25 and 8% of 250 = 20, so 25 + 20 = 45. For two comparable values with no before-and-after baseline, the Percentage Difference Calculator divides their absolute gap by their average. Example: 40 and 60 have a difference of 20 and an average of 50, so their percentage difference is 40%. The Ratio Calculator simplifies two- or three-term ratios, scales an equivalent two-term ratio or solves A:B = C:D when one positive value is missing. Examples: 10:15 simplifies to 2:3, 100:200:400 simplifies to 1:2:4, and 2:3 = 4:6 because 2 × 6 = 3 × 4. The Fraction Calculator adds, subtracts, multiplies and divides fractions, then simplifies the result. Example: 1/2 + 1/3 uses denominator 6, so 3/6 + 2/6 = 5/6. Check: 0.5 + 0.333333… = 0.833333…, the decimal value of 5/6. The Unit Converter changes values between units of the same quantity. Choose weight, length or temperature before selecting the starting and target units. Example: 10 lb × 0.45359237 kg per lb = 4.5359237 kg. Check: 4.5359237 kg ÷ 0.45359237 kg per lb = 10 lb. NIST Handbook 44 (2026) lists the pound-to-kilogram factor. The conversion factor is listed in <a href=\"https://doi.org/10.6028/NIST.HB.44-2026\" target=\"_blank\" rel=\"noopener noreferrer\">NIST Handbook 44 (2026), Appendix C</a>.",
        "faq": [
            ("What is 25% of 200?", "25% of 200 is 50. Step 1: write 25% as 25 ÷ 100 = 0.25. Step 2: multiply 200 × 25 = 5,000, then divide 5,000 ÷ 100 = 50. Check: 200 × 0.25 = 50."),
            ("How do I simplify a ratio?", "Divide every term by the greatest common divisor. For example, 10:15 becomes 2:3 and 100:200:400 becomes 1:2:4. To solve A:B = C:D, enter exactly three positive values and use A × D = B × C to find the missing term."),
            ("What is 1/2 + 1/3?", "The answer is 5/6. Step 1: use the common denominator 6. Step 2: convert 1/2 to 3/6 and 1/3 to 2/6. Step 3: add 3/6 + 2/6 = 5/6. Check in decimals: 0.5 + 0.333333… = 0.833333…, and 5 ÷ 6 = 0.833333…."),
            ("Can I convert kilograms to pounds?", "Yes. In the Unit Converter, select Weight, choose kilograms as the starting unit and pounds as the target. NIST Handbook 44 (2026) lists 1 pound as 0.45359237 kilograms. Example: 1 kg ÷ 0.45359237 kg per pound = about 2.20462262 lb. Check by reversing the conversion: 2.20462262 × 0.45359237 = about 1.00000000 kg. The displayed result may be rounded. See <a href=\"https://doi.org/10.6028/NIST.HB.44-2026\" target=\"_blank\" rel=\"noopener noreferrer\">NIST Handbook 44 (2026), Appendix C</a>."),
            ("Why can the denominator not be zero?", "A fraction means its numerator divided by its denominator. Division by zero has no defined value, so a fraction such as 3/0 has no numerical result. The Fraction Calculator rejects a zero denominator rather than returning a misleading number."),
            ("How do I calculate percentage change?", "Subtract the starting value from the new value, divide that difference by the starting value, then multiply by 100. Example: from 80 to 92, the increase is 92 − 80 = 12; 12 ÷ 80 × 100 = 15%. Check: 80 × 1.15 = 92, so the new value is 15% above the starting value."),
            ("When should I use percentage difference instead of percentage change?", "Use percentage difference when neither value is the starting point. It divides the absolute gap by the average, so swapping the two values does not change the result. Use percentage change when one value is the baseline."),
            ("When should I use scientific mode?", "Use Scientific Mode when the calculation needs a supported power, root, trigonometric function, logarithm or statistical operation. For ordinary addition, subtraction, multiplication and division, the standard keypad is sufficient. Check the function and angle setting shown by the calculator before evaluating a trigonometric expression.")
        ],
    },
    "worship": {
        "intro": "Worship and daily-use tools help you keep count of dhikr and similar practices. The tasbih counter saves your count on the device you use, and it does not send your count anywhere.",
        "faq": [
            ("Is my count shared with other people?", "No. The count is stored only in the browser on your device."),
        ],
    },
}

CATEGORIES = [
    {"slug": "money", "name": "Money and Business", "desc": "Compare EMI, Zakat, profit and loss, discounts and compound interest with worked examples, formulas and clear assumptions."},
    {"slug": "health", "name": "Health", "desc": "Calculate adult BMI and estimated maintenance calories in metric or imperial units, with worked examples, clear methods and limitations."},
    {"slug": "time", "name": "Date and Time", "desc": "Use age, date-difference and years-to-days calculators, plus a browser stopwatch, to check calendar spans, time conversions and everyday timing."},
    {"slug": "math", "name": "Math and Converters", "desc": "Calculate percentages, percentage change and percentage difference, ratios, fractions, scientific arithmetic and unit conversions with clear worked examples."},
    {"slug": "worship", "name": "Worship and Daily Use", "desc": "Use a private browser-based tasbih counter for dhikr, with target tracking and local-only count storage on your device."},
]

URDU = {
    "zakat-calculator": {
        "name": "زکوٰۃ کیلکولیٹر",
        "title": "آن لائن زکوٰۃ کیلکولیٹر: حنفی اور جعفری | CalculatesAll",
        "description": "حنفی یا سید سیستانی کے جعفری طریقے سے زکوٰۃ کا تخمینہ لگائیں۔ سونے اور چاندی کی قیمت گرام یا معیاری تولہ میں درج کریں۔",
        "h1": "حنفی اور جعفری زکوٰۃ کیلکولیٹر",
        "lead": "یہ کیلکولیٹر مفت ہے اور اکاؤنٹ بنانے کی ضرورت نہیں۔ حساب آپ کے براؤزر میں ہوتا ہے۔ دھاتوں کی قیمت خود درج کریں کیونکہ یہاں لائیو مارکیٹ ریٹس حاصل نہیں کیے جاتے۔ دو الگ حسابی طریقوں میں سے انتخاب کریں: سنی حنفی، یا آیت اللہ سید سیستانی کے مخصوص جعفری تجارتی مال اور اہل ڈھلے ہوئے سکوں کے محدود احکام۔ سونے اور چاندی کی قیمت فی گرام یا واضح طور پر متعین سندھ کے معیاری تولہ کے مطابق درج کریں۔ حساب کے مفروضے، ماخذ اور حدود ضرور پڑھیں۔",
        "labels": [
            ("Choose a silver or gold Nisab method. The 2.5% estimate applies only when the selected threshold and Hawl conditions are met.", "چاندی یا سونے کا نصاب منتخب کریں۔ 2.5٪ کا تخمینہ صرف منتخب نصاب اور حول کی شرائط پوری ہونے پر لاگو ہوتا ہے۔"),
            ("Currency code (ISO 4217)", "کرنسی کوڈ (ISO 4217)"),
            ("Examples: PKR, USD, GBP, EUR, SAR, AED, INR. Use one currency for every amount and metal price.", "مثالیں: PKR، USD، GBP، EUR، SAR، AED، INR۔ تمام رقوم اور دھاتوں کی قیمت ایک ہی کرنسی میں درج کریں۔"),
            ("School of thought / calculation method", "فقہی مسلک / حساب کا طریقہ"),
            ("Sunni — Hanafi", "سنی — حنفی"),
            ("Shia Ja'fari — Sayyid Sistani", "شیعہ جعفری — آیت اللہ سید سیستانی"),
            ("Choose the method you follow. The Shia Ja'fari option is specifically limited to Sayyid Sistani's published rulings, not every Ja'fari authority.", "وہ طریقہ منتخب کریں جس کی آپ پیروی کرتے ہیں۔ شیعہ جعفری اختیار صرف آیت اللہ سید سیستانی کے شائع شدہ احکام کے لیے ہے، ہر جعفری مرجع کے لیے نہیں۔"),
            ("Nisab method", "نصاب کا طریقہ"),
            ("Silver Nisab (612.36 g, South Asian classical conversion)", "چاندی کا نصاب (612.36 گرام، جنوبی ایشیائی روایتی پیمانہ)"),
            ("Gold Nisab (87.48 g, South Asian classical conversion)", "سونے کا نصاب (87.48 گرام، جنوبی ایشیائی روایتی پیمانہ)"),

            ("Choose a silver or gold Nisab method. The 2.5% estimate applies only when the selected threshold and Hawl conditions are met.", "چاندی یا سونے کا نصاب منتخب کریں۔ 2.5 فیصد کا اندازہ صرف اسی وقت لاگو ہوتا ہے جب منتخب حد اور حول کی شرائط پوری ہوں۔"),
            ("Gold, silver and jewellery", "سونا، چاندی اور زیورات"),
            ("Investments and business assets", "سرمایہ کاری اور کاروباری اثاثے"),
            ("Business assets", "کاروباری اثاثے"),
            ("Receivables and retirement funds", "قابلِ وصول رقوم اور ریٹائرمنٹ فنڈز"),
            ("Digital assets and property", "ڈیجیٹل اثاثے اور جائیداد"),
            ("Liabilities and payments", "واجبات اور ادائیگیاں"),
            ("Trading goods and ownership", "تجارتی مال اور ملکیت"),
            ("Ownership conditions", "ملکیت کی شرائط"),
            ("Trading goods", "تجارتی مال"),
            ("Personal gold/silver coins", "ذاتی سونے اور چاندی کے سکے"),
            ("These are minted gold/silver coins that are prevalently used as money in transactions", "یہ ڈھلے ہوئے سونے یا چاندی کے سکے ہیں جو عام لین دین میں بطور رقم رائج ہیں"),
            ("Total minted gold-coin weight (selected unit)", "ڈھلے ہوئے سونے کے سکوں کا کل وزن (منتخب اکائی)"),
            ("Total minted silver-coin weight (selected unit)", "ڈھلے ہوئے چاندی کے سکوں کا کل وزن (منتخب اکائی)"),
            ("Gold coins remained at or above the first Nisab for 11 lunar months", "سونے کے سکے 11 قمری مہینے تک پہلے نصاب کے برابر یا اس سے زیادہ رہے"),
            ("Silver coins remained at or above the first Nisab for 11 lunar months", "چاندی کے سکے 11 قمری مہینے تک پہلے نصاب کے برابر یا اس سے زیادہ رہے"),
            ("Owner retained legal and actual right of disposal over these coins", "مالک کو پورے عرصے میں ان سکوں پر قانونی اور عملی تصرف کا اختیار حاصل رہا"),
            ("Only use this if the coins are minted and are actually used prevalently as money in transactions. Sistani states that gold and silver are not currently used as money. Ordinary banknotes, bank deposits, bullion bars and jewellery do not qualify. If unsure, leave this option off and consult Sistani&#39;s office.", "یہ اختیار صرف اسی صورت میں استعمال کریں جب سکے ڈھلے ہوئے ہوں اور عام لین دین میں بطور رقم رائج ہوں۔ سیستانی کے مطابق اس وقت سونا اور چاندی لین دین میں بطور رقم استعمال نہیں ہوتے۔ عام بینک نوٹ، بینک ڈپازٹس، بلین کی سلاخیں اور زیورات اس میں شامل نہیں۔ شک ہو تو یہ اختیار بند رکھیں اور دفترِ سیستانی سے رجوع کریں."),
            ("Hawl and profit intention", "حول اور نفع کی نیت"),
            ("Trading-goods conditions", "تجارتی مال کی شرائط"),
            ("Current metal prices", "دھاتوں کی موجودہ قیمتیں"),
            ("Choose one unit and use it for both metal prices.", "ایک اکائی منتخب کریں اور دونوں دھاتوں کی قیمت اسی اکائی میں درج کریں۔"),
            ("Prices are converted to per-gram rates before Nisab is calculated. This is an estimate, not a fatwa.", "نصاب کے حساب سے پہلے قیمتوں کو فی گرام میں تبدیل کیا جاتا ہے۔ یہ ایک اندازہ ہے، فتویٰ نہیں۔"),
            ("Eligible assets", "قابلِ زکوٰۃ اثاثے"),
            ("Enter market values in the selected currency. Leave categories you do not own at zero.", "منتخب کرنسی میں موجودہ مالیت درج کریں۔ جو اثاثہ آپ کے پاس نہیں، اسے صفر رہنے دیں۔"),
            ("Cash held at home", "گھر میں موجود نقد رقم"),
            ("Bank and current account balances", "بینک اور کرنٹ اکاؤنٹ کی رقم"),
            ("Savings, deposits and cash equivalents", "بچت، ڈپازٹس اور نقد کے متبادل"),
            ("Eligible gold value", "قابلِ زکوٰۃ سونے کی مالیت"),
            ("Eligible silver value", "قابلِ زکوٰۃ چاندی کی مالیت"),
            ("Permissible personal-use gold/silver jewellery", "جائز ذاتی استعمال کے سونے/چاندی کے زیورات"),
            ("Zakatable shares and investments", "قابلِ زکوٰۃ شیئرز اور سرمایہ کاری"),
            ("Business cash and bank balance", "کاروبار کی نقد اور بینک رقم"),
            ("Trade inventory at current sale value", "فروخت کے لیے کاروباری مال کی موجودہ قیمت"),
            ("Recoverable loans and receivables", "واپس ملنے والے قرض اور قابلِ وصول رقوم"),
            ("Accessible pension or retirement amount", "قابلِ رسائی پنشن یا ریٹائرمنٹ کی رقم"),
            ("Eligible cryptocurrency holdings", "قابلِ زکوٰۃ کرپٹو کرنسی کی مالیت"),
            ("Property held for resale", "دوبارہ فروخت کے لیے رکھی گئی جائیداد"),
            ("Shia Ja'fari method — Sayyid Sistani", "شیعہ جعفری طریقہ — آیت اللہ سید سیستانی"),
            ("This is not the Sunni cash-and-bank calculation. Under Sayyid Sistani's published rulings, ordinary banknotes and bank deposits do not carry obligatory Zakat. This limited calculator estimates only qualifying trading goods under obligatory precaution. Other Ja'fari authorities may have different rulings. Khums is separate and is not calculated here.", "یہ سنی نقد رقم اور بینک بیلنس والا حساب نہیں ہے۔ آیت اللہ سید سیستانی کے شائع شدہ احکام کے مطابق عام بینک نوٹ اور بینک ڈپازٹس پر واجب زکوٰۃ نہیں۔ یہ محدود کیلکولیٹر صرف احتیاطِ واجب کے تحت اہل تجارتی مال کا تخمینہ لگاتا ہے۔ دوسرے جعفری مراجع کے احکام مختلف ہو سکتے ہیں۔ خمس الگ ہے اور یہاں اس کا حساب نہیں ہوتا۔"),
            ("Sayyid Sistani only. This estimates qualifying trading goods under obligatory precaution. Ordinary banknotes and deposits are excluded. Khums is separate.", "صرف آیت اللہ سید سیستانی کا طریقہ۔ یہ حساب احتیاطِ واجب کے مطابق اہل تجارتی مال کا تخمینہ لگاتا ہے۔ عام بینک نوٹ اور بینک ڈپازٹس شامل نہیں۔ خمس الگ ہے۔"),
            ("Trading-goods Nisab reference", "تجارتی مال کا نصاب"),
            ("Gold: 69.12 g (15 common mithqals)", "سونا: 69.12 گرام (15 مثقالِ صیرفی)"),
            ("Silver: 483.84 g (105 common mithqals)", "چاندی: 483.84 گرام (105 مثقالِ صیرفی)"),
            ("Current market value of qualifying trading goods", "اہل تجارتی مال کی موجودہ بازاری قیمت"),
            ("Owner is adult and sane", "مالک بالغ اور عاقل ہو"),
            ("Trading goods were acquired through a contract of exchange, such as a purchase", "تجارتی مال خرید و فروخت کے معاہدے کے ذریعے حاصل کیا گیا ہو"),
            ("One full lunar year has passed since the intention to profit", "نفع کمانے کی نیت سے ایک مکمل قمری سال گزر چکا ہو"),
            ("Intention to profit continued throughout the year", "پورے سال نفع کمانے کی نیت برقرار رہی ہو"),
            ("Owner retained the right to dispose of the goods throughout the year", "مالک کو پورے سال مال میں تصرف کا حق حاصل رہا ہو"),
            ("Market value did not fall below the purchase cost during the year", "سال کے دوران مال کی بازاری قیمت خریداری کی لاگت سے کم نہ ہوئی ہو"),
            ("This path excludes cash, banknotes, ordinary savings, personal jewellery, crops and livestock. It is not a complete Zakat or Khums assessment.", "اس طریقے میں نقد رقم، بینک نوٹ، عام بچت، ذاتی زیورات، زرعی پیداوار اور مویشی شامل نہیں۔ یہ زکوٰۃ یا خمس کا مکمل حساب نہیں ہے۔"),
            ("Metal prices for Nisab", "نصاب کے لیے دھاتوں کی قیمت"),
            ("Metal price unit", "دھات کی قیمت کی اکائی"),
            ("Price per gram", "فی گرام قیمت"),
            ("Price per Sindh Government standard tola (11.6638 g)", "حکومتِ سندھ کے سرکاری تولہ کے حساب سے قیمت (11.6638 گرام)"),
            ("Price per troy ounce (31.1034768 g)", "فی ٹرائے اونس قیمت (31.1034768 گرام)"),
            ("Enter the current local price in the selected currency and unit. Gram = 1 g, Sindh Government standard tola = 11.6638 g, and troy ounce = 31.1034768 g. The calculator converts both metal prices to a per-gram rate before calculating Nisab.", "منتخب کرنسی اور اکائی میں موجودہ مقامی قیمت درج کریں۔ گرام = 1 گرام، سرکاری تولہ = 11.6638 گرام، اور ٹرائے اونس = 31.1034768 گرام ہے۔ کیلکولیٹر دونوں قیمتوں کو نصاب سے پہلے فی گرام میں تبدیل کرتا ہے۔"),
            ("Silver price in selected unit", "منتخب اکائی میں چاندی کی قیمت"),
            ("24-karat gold price in selected unit", "منتخب اکائی میں 24 قیراط سونے کی قیمت"),
            ("Eligible liabilities and payments", "قابلِ کٹوتی واجبات اور ادائیگیاں"),
            ("Eligible short-term debts and dues", "قابلِ کٹوتی قلیل مدتی قرض اور واجبات"),
            ("Zakat already paid for this Zakat year", "اس زکوٰۃ سال میں پہلے ادا کی گئی زکوٰۃ"),
            ("One full lunar Zakat year (hawl) is complete", "ایک مکمل قمری زکوٰۃ سال (حول) پورا ہو چکا ہے"),
            ("The Hanafi method includes qualifying gold and silver jewellery when eligible under Hanafi guidance. Enter metal value only, avoid duplicate entry, and ask a qualified scholar about unusual jewellery or trade holdings.", "حنفی طریقہ اہل سونے اور چاندی کے زیورات کو حنفی رہنمائی کے مطابق شامل کرتا ہے۔ صرف دھات کی مالیت درج کریں، ایک ہی زیور دوبارہ شمار نہ کریں، اور غیر معمولی زیورات یا تجارتی مال کے بارے میں مستند عالم سے پوچھیں۔"),
            ("This is an estimate, not a fatwa. Debt, jewellery, investments, business goods and retirement rules can differ. Review the source-based guidance below and ask a qualified scholar about your circumstances.", "یہ صرف تخمینہ ہے، فتویٰ نہیں۔ قرض، زیورات، سرمایہ کاری، کاروباری مال اور پنشن کے احکام مختلف ہو سکتے ہیں۔ نیچے مستند ماخذ پر مبنی وضاحت پڑھیں اور اپنے حالات کے مطابق اہل عالم سے رجوع کریں۔"),
            ("One-page Zakat calculator", "ایک صفحے کا زکوٰۃ کیلکولیٹر"),
            ("Choose your method, enter only applicable amounts, then calculate.", "اپنا طریقہ منتخب کریں، صرف متعلقہ رقوم درج کریں، پھر حساب کریں۔"),
            ("Recoverable receivables", "قابلِ وصول رقوم"),
            ("Property held for resale (only if bought for resale)", "دوبارہ فروخت کے لیے خریدی گئی جائیداد کی مالیت"),
            ("Owner remained adult and sane throughout the year", "مالک پورے سال بالغ اور عاقل رہا ہو"),
            ("One full year has passed since the intention to profit began", "نفع کی نیت کرنے کے بعد ایک مکمل سال گزر چکا ہو"),
            ("Sayyid Sistani only. This estimates qualifying trading goods under obligatory precaution. The personal-coin option applies only to minted gold/silver coins that are prevalently used as money in transactions. For qualifying coins, the first Nisab must remain present for 11 lunar months. Sistani states that gold and silver are not currently used as money in transactions, so ordinary banknotes, bank deposits, bullion bars and jewellery are not included. Khums is separate. Other Ja'fari authorities may differ.", "صرف آیت اللہ سید سیستانی کا طریقہ۔ یہ کیلکولیٹر احتیاطِ واجب کے تحت اہل تجارتی مال کا تخمینہ لگاتا ہے۔ ذاتی سکوں کا اختیار صرف ان ڈھلے ہوئے سونے یا چاندی کے سکوں کے لیے ہے جو عام لین دین میں بطور رقم رائج ہوں۔ اہل سکوں کے لیے پہلا نصاب 11 قمری مہینے برقرار رہنا ضروری ہے۔ سیستانی کے مطابق اس وقت سونا اور چاندی لین دین میں بطور رقم استعمال نہیں ہوتے، اس لیے عام بینک نوٹ، بینک ڈپازٹس، بلین کی سلاخیں اور زیورات شامل نہیں۔ خمس الگ ہے۔ دوسرے جعفری مراجع کے احکام مختلف ہو سکتے ہیں۔"),
            ("Calculate Zakat", "زکوٰۃ کا حساب کریں")
        ],
        "how_heading": "زکوٰۃ کا حساب، نصاب اور ضروری وضاحت",
        "faq_heading": "اکثر پوچھے جانے والے سوالات",
        "how": [
            "یہ کیلکولیٹر قابلِ زکوٰۃ مالی اثاثوں پر سالانہ زکوٰۃ کا حسابی تخمینہ بناتا ہے۔ پہلے آپ کے درج کردہ اثاثے جمع ہوتے ہیں، پھر وہ واجبات منہا ہوتے ہیں جنہیں آپ کے اختیار کردہ شرعی طریقے کے مطابق منہا کیا جا سکتا ہے۔ اس کے بعد خالص مال کو منتخب نصاب سے ملایا جاتا ہے۔ اگر نصاب اور قمری سال کی شرط پوری ہو تو 2.5 فیصد کا حساب دکھایا جاتا ہے۔ یہ حسابی سہولت ہے، شرعی فتویٰ یا کسی مستند عالم کا متبادل نہیں۔",
            "اپنی زکوٰۃ کی تاریخ پر موجود مالیت درج کریں۔ عام طور پر یہ وہ ہجری تاریخ ہوتی ہے جب آپ کا زکوٰۃ کا سال مکمل ہوتا ہے۔ ہر شخص کی تاریخ مختلف ہو سکتی ہے۔ یہ خود بخود یکم جنوری، مالی سال، رمضان یا صفحہ کھولنے کی تاریخ نہیں بن جاتی۔ بہتر ہے کہ آپ اپنی تاریخ، دھات کی قیمت کا ماخذ اور استعمال شدہ طریقہ لکھ کر محفوظ رکھیں تاکہ اگلے سال موازنہ کر سکیں۔",
            "نصاب وہ کم از کم مالیت ہے جس کے پہنچنے پر زکوٰۃ کی دوسری شرائط دیکھی جاتی ہیں۔ اس حنفی کیلکولیٹر میں جنوبی ایشیائی حنفی رہنمائی میں عام طور پر بیان کردہ دو وزن دستیاب ہیں: چاندی 612.36 گرام یا سونا 87.48 گرام۔ ابتدا میں چاندی کا نصاب منتخب ہے۔ نقد حد منتخب دھات کے وزن کو زکوٰۃ کی تاریخ پر فی گرام مقامی قیمت سے ضرب دے کر بنتی ہے۔ اپنے حالات کے مطابق نصاب منتخب کرنے کے لیے مستند حنفی عالم کی رہنمائی لیں.",
            "سنی اختیار میں صرف حنفی طریقہ دستیاب ہے۔ یہ 612.36 گرام چاندی کے نصاب کو ابتدائی انتخاب رکھتا ہے اور 87.48 گرام سونے کا متبادل بھی دیتا ہے۔ یہ محدود حسابی تخمینہ ہے، مکمل فقہی انجن نہیں۔ واجبات کے خانے میں درج رقم منہا ہوتی ہے، مگر کیلکولیٹر خود فیصلہ نہیں کرتا کہ کوئی مخصوص قرض یا قسط حنفی حکم کے مطابق قابلِ کٹوتی ہے یا نہیں۔ حول کا چیک باکس آپ کی خود تصدیق ہے، یہ پورے قمری سال میں مال کا ریکارڈ نہیں رکھتا.",
            "پاکستانی حنفی قارئین کے لیے مقامی فقہی وضاحت: جامعہ علوم اسلامیہ بنوری ٹاؤن کے فتویٰ نمبر 144608101364 (17 فروری 2025) کے مطابق 7.5 تولہ سونے کا نصاب اس وقت لاگو ہوتا ہے جب قابلِ زکوٰۃ مال صرف سونا ہو۔ اگر سونے کے ساتھ نقد رقم، چاندی یا مالِ تجارت بھی ہو تو مجموعی قابلِ زکوٰۃ مال کا موازنہ 52.5 تولہ چاندی کے نصاب سے کیا جاتا ہے۔ یہ بنوری ٹاؤن کا شائع شدہ موقف ہے، ہر حنفی دارالافتاء کی رائے کا دعویٰ نہیں۔ اپنے مستند عالم کی ہدایت پر عمل کریں۔ ماخذ: [بنوری ٹاؤن کا فتویٰ 144608101364](https://www.banuri.edu.pk/readquestion/144608101364/17-02-2025)۔",
            "ایک ہی زیور کی قیمت کو زیورات، سونے اور چاندی کے خانوں میں دوبارہ درج نہ کریں۔ خالص پن، نگینے، کاریگری، ذاتی استعمال اور تجارت کا مقصد مالیت یا شرعی درجہ بندی بدل سکتے ہیں۔ کیلکولیٹر زیور کا وزن یا خالص پن خود نہیں جانچتا۔ غیر یقینی صورت میں مستند حنفی عالم اور قابلِ اعتماد جیولر سے رجوع کریں.",
            "شیعہ جعفری اختیار صرف آیت اللہ سید سیستانی کی پیروی کرنے والوں کے لیے ہے۔ ان کے سرکاری سوال و جواب کے مطابق عام بینک ڈپازٹس اور بینک نوٹوں پر واجب زکوٰۃ نہیں، جبکہ سالانہ اخراجات کے بعد بچت پر خمس کا الگ حکم ہو سکتا ہے۔ اس لیے اس اختیار میں سنی نقد اور بینک بیلنس والا فارمولا استعمال نہیں ہوتا۔",
            "یہ کیلکولیٹر سیستانی کے ایک محدود حکم کا حساب کرتا ہے: ایسا تجارتی مال جو تبادلے کے معاہدے سے حاصل کیا گیا ہو اور نفع کے لیے رکھا گیا ہو۔ یہ حکم احتیاطِ واجب کی بنا پر لاگو ہوتا ہے۔ سرکاری حکم کے مطابق مالک بالغ اور عاقل ہو، مال کا نصاب کم از کم 15 مثقالِ صیرفی سونا یا 105 مثقالِ صیرفی چاندی ہو، نفع کی نیت سے ایک سال گزرے، نفع کی نیت پورے سال برقرار رہے، مالک کو پورے سال مال میں تصرف کا حق حاصل ہو، اور مال پورے سال کم از کم اپنی لاگت کے برابر فروخت ہونے کے قابل ہو۔ اس مال پر شرح 2.5 فیصد ہے۔ اگر ان شرائط میں سے کسی کی تصدیق نہ ہو تو کیلکولیٹر رقم نہیں دکھاتا۔",
            "سیستانی کے تجارتی مال کے لیے استعمال شدہ نصاب سونے کے 69.12 گرام اور چاندی کے 483.84 گرام ہیں۔ کیلکولیٹر میں ذاتی سکوں کے لیے الگ اختیاری خانہ بھی ہے، مگر صرف ان ڈھلے ہوئے سونے یا چاندی کے سکوں کے لیے جو عام لین دین میں بطور رقم رائج ہوں اور جن پر 11 قمری مہینے، بالغ و عاقل مالک اور حقِ تصرف کی الگ شرائط پوری ہوں۔ حکم 1915 کے مطابق اس وقت سونا اور چاندی لین دین میں بطور رقم استعمال نہیں ہوتے، اس لیے عام بینک نوٹ، بینک ڈپازٹس، بلین اور زیورات شامل نہیں۔ یہ کیلکولیٹر زرعی پیداوار، مویشی یا خمس کا حساب نہیں کرتا۔ دوسرے جعفری مراجع کے احکام مختلف ہو سکتے ہیں، اس لیے اپنے مرجع کے دفتر سے تصدیق کریں۔",
            "سونے اور چاندی کی قیمت تین اکائیوں میں درج کریں: گرام (1 گرام)، حکومتِ سندھ کا سرکاری تولہ (11.6638 گرام)، یا ٹرائے اونس (31.1034768 گرام)۔ کیلکولیٹر قیمت کو فی گرام میں تبدیل کر کے نصاب نکالتا ہے۔ بعض پاکستانی بازاروں میں تولہ 12.5 گرام بھی استعمال ہوتا ہے، اس لیے صراف سے اصل وزن کی تصدیق کریں۔",
            "تمام اثاثوں اور دھات کی قیمت ایک ہی کرنسی میں درج کریں۔ یہ کیلکولیٹر لائیو قیمت حاصل نہیں کرتا۔ سرکاری تولہ صرف 11.6638 گرام کے نرخ پر اور ٹرائے اونس صرف 31.1034768 گرام کے نرخ پر منتخب کریں۔ اگر بازار کا تولہ 12.5 گرام ہو تو قیمت فی گرام میں تبدیل کر کے گرام منتخب کریں۔",
            "چاندی کا نصاب منتخب ہو تو چاندی کی فی گرام موجودہ قیمت درج کریں۔ سونے کے دونوں طریقوں کے لیے 24 قیراط سونے کی فی گرام قیمت درکار ہے۔ قیمت اسی کرنسی میں ہونی چاہیے جس میں آپ نے اپنے اثاثے اور قرض درج کیے ہیں۔ یہ صفحہ لائیو مارکیٹ قیمت حاصل کرنے کا دعویٰ نہیں کرتا۔ اپنی زکوٰۃ کی تاریخ پر مقامی معتبر صرافہ، بلین یا جیولرز کے ذریعے قیمت کی تصدیق کریں۔ پرانی مثال کی قیمت کو آج کی قیمت نہ سمجھیں۔",
            "نقد رقم میں گھر کے نوٹ اور سکے شامل ہو سکتے ہیں۔ بینک بیلنس میں کرنٹ، سیونگ اور ملتے جلتے اکاؤنٹس شامل کریں۔ دوسری بچت، فکسڈ ڈپازٹ اور نقد کے متبادل بھی شامل ہو سکتے ہیں، بشرطیکہ وہ آپ کی ملکیت ہوں اور آپ کے اختیار کردہ طریقے میں قابلِ زکوٰۃ ہوں۔ ایک ہی رقم کو دو خانوں میں نہ لکھیں۔ اگر بینک بیلنس پہلے ہی بچت کے مجموعے میں شامل ہے تو اسے دوبارہ شامل نہ کریں۔",
            "سونے اور چاندی کی مالیت موجودہ قابلِ اطلاق مارکیٹ ویلیو کے مطابق درج کریں، خریداری کی پرانی قیمت کے مطابق نہیں۔ زیورات کے حکم میں فقہی مسلک، استعمال، خالص دھات، پتھر اور مقامی عمل کے لحاظ سے اختلاف ہو سکتا ہے۔ اگر زیور میں پتھر یا دیگر مواد شامل ہو تو مناسب طریقے سے دھات کی مالیت الگ دیکھیں۔ ہر عالم یا ادارے کا ذاتی زیورات کے بارے میں ایک ہی حکم نہیں ہوتا۔",
            "شیئرز، فنڈز، سرٹیفکیٹس اور دوسری سرمایہ کاری کے لیے صرف وہ مالیت درج کریں جو آپ کے اختیار کردہ شرعی طریقے میں قابلِ زکوٰۃ ہو۔ تجارت کے لیے رکھی گئی سرمایہ کاری اور طویل مدت کے لیے رکھی گئی سرمایہ کاری کا حکم مختلف ہو سکتا ہے۔ کسی بانڈ، پنشن یا فنڈ کی پوری اصل رقم کو خود بخود قابلِ زکوٰۃ نہ سمجھیں۔ اس کی حقیقی قابلِ وصول یا قابلِ زکوٰۃ مالیت معلوم کریں اور ضرورت ہو تو عالم سے پوچھیں۔",
            "کاروبار کے لیے کاروباری نقد، بینک رقم، فروخت کے لیے موجود مال کی موجودہ فروختی قیمت اور وہ قابلِ وصول رقم شامل ہو سکتی ہے جس کی وصولی کی توقع ہو۔ دکان کی مشینری، فرنیچر، کام کے اوزار، ڈیلیوری گاڑی یا کاروبار میں استعمال ہونے والی عمارت کو فروخت کے مال کے طور پر شامل نہ کریں۔ کسی دوسرے کو دیا گیا قرض اسی وقت شامل کریں جب آپ کے اختیار کردہ طریقے کے مطابق اس کی واپسی متوقع ہو۔",
            "پنشن یا ریٹائرمنٹ اکاؤنٹ کے خانے میں صرف وہ رقم درج کریں جو متعلقہ طریقے کے مطابق واقعی قابلِ رسائی یا نکلوائی جا سکتی ہو۔ ٹیکس، جرمانہ، ویسٹنگ کی شرط اور رقم نکالنے کی پابندیاں اصل قابلِ وصول رقم بدل سکتی ہیں۔ کرپٹو کرنسی کا خانہ اختیاری ہے۔ اسے صرف اسی وقت شامل کریں جب آپ کا معتبر عالم یا ادارہ اسے قابلِ زکوٰۃ مال شمار کرتا ہو۔ جائیداد کا خانہ صرف دوبارہ فروخت یا تجارت کے لیے رکھی گئی جائیداد کے لیے ہے۔",
            "قرض کے خانے میں صرف وہ رقم درج کریں جسے آپ کا مستند حنفی عالم آپ کے حالات میں قابلِ کٹوتی قرار دے۔ قرض کی نوعیت، واجب الادا تاریخ اور قسطوں کا شیڈول اہم ہو سکتے ہیں۔ طویل مدتی قرض کا پورا بقایا خود بخود منہا نہ کریں.",
            "آنے والے گھریلو اخراجات جو ابھی واجب نہیں ہوئے، عام مستقبل کے اخراجات کا اندازہ، یا سود کو خود بخود قابلِ کٹوتی قرض نہ سمجھیں۔ اگر کئی قسطیں ہیں تو صرف وہ رقم درج کریں جو مقررہ مدت میں واجب ہوتی ہے۔ ایک ہی قسط کو دو مرتبہ منہا نہ کریں۔ اگر کسی قرض کی کٹوتی کے بارے میں یقین نہیں تو دونوں صورتوں کا حساب بنا کر مستند عالم سے پوچھیں، اختلافی مسئلے کو سب کے لیے ایک ہی حکم نہ بنائیں۔",
            "حساب کا بنیادی طریقہ یہ ہے: کل قابلِ زکوٰۃ اثاثے منفی قابلِ کٹوتی واجبات برابر خالص قابلِ زکوٰۃ مال۔ خالص مال صفر سے کم نہیں دکھایا جاتا۔ منتخب نصاب کی رقم منتخب دھات کے وزن کو فی گرام قیمت سے ضرب دے کر بنتی ہے۔ اگر خالص مال نصاب سے کم ہو تو کیلکولیٹر بتاتا ہے کہ منتخب نصاب پورا نہیں ہوا۔ اگر نصاب پورا ہو مگر آپ قمری سال مکمل ہونے کی تصدیق نہ کریں تو زکوٰۃ کی واجب رقم نہیں دکھائی جاتی۔",
            "جب منتخب نصاب پورا ہو اور آپ قمری زکوٰۃ سال مکمل ہونے کی تصدیق کریں تو خالص قابلِ زکوٰۃ مال پر 2.5 فیصد لگایا جاتا ہے۔ اسی زکوٰۃ سال میں پہلے ادا کی گئی رقم اس حساب سے منہا کی جاتی ہے۔ باقی رقم صفر سے کم نہیں ہو سکتی۔ اگر پہلے ادا کی گئی رقم موجودہ حساب سے زیادہ ہو تو کیلکولیٹر زائد ادائیگی کو الگ دکھاتا ہے۔ اس زائد رقم کے اگلے سال یا کسی اور مد میں استعمال کے بارے میں مستند عالم سے رہنمائی لیں۔",
            "مثال کے طور پر تمام رقوم پاکستانی روپے میں ہیں۔ گھر کی نقد رقم 300,000، بینک بیلنس 400,000، دوسری بچت 100,000، قابلِ زکوٰۃ سونا 150,000، کاروباری مال 200,000 اور قابلِ وصول رقم 50,000 ہے۔ کل اثاثے 1,200,000 بنتے ہیں۔ اگر قابلِ کٹوتی قلیل مدتی قرض 100,000 ہو تو خالص مال 1,100,000 ہوگا۔",
            "صرف مثال کے لیے فرض کریں کہ زکوٰۃ کی تاریخ پر چاندی کی فی گرام قیمت 1,000 روپے ہے۔ چاندی کا نصاب 612.36 ضرب 1,000 یعنی 612,360 روپے بنتا ہے۔ خالص مال 1,100,000 روپے اس نصاب سے زیادہ ہے۔ 2.5 فیصد کے حساب سے ابتدائی زکوٰۃ 27,500 روپے ہوگی۔ اگر اسی زکوٰۃ سال میں 5,000 روپے پہلے ادا کیے جا چکے ہوں تو باقی رقم 22,500 روپے ہوگی۔ مثال کی قیمت فرضی ہے، اسے موجودہ بازار کی قیمت نہ سمجھیں۔",
            "ذاتی استعمال کی چیزیں مثلاً رہائشی گھر، عام لباس، گھریلو فرنیچر، ذاتی گاڑی اور کام کے اوزار عام طور پر فروخت کے کاروباری مال کے برابر نہیں ہوتے۔ دوبارہ فروخت کے ارادے سے خریدی گئی جائیداد ذاتی رہائش سے مختلف ہے۔ کرایے کی عمارت کی پوری مالیت اور اس سے حاصل ہونے والی بچت کا حکم الگ ہو سکتا ہے۔ رہائشی یا کرایے کی جائیداد کی پوری قیمت اس خانے میں درج نہ کریں جب تک مستند رہنمائی نہ لے لیں۔",
            "زرعی پیداوار، مویشی، خزانہ، مشترکہ ملکیت، کاروباری مستقل اثاثے اور پیچیدہ پنشن کے لیے الگ نصاب، شرح، تاریخ یا ملکیت کے اصول ہو سکتے ہیں۔ یہ کیلکولیٹر زرعی یا مویشیوں کی زکوٰۃ نہیں نکالتا۔ ہر قسم کے مال کو ایک ہی 2.5 فیصد کے فارمولے میں شامل کرنا درست نہیں ہوگا۔",
            "آخری جائزہ: 16 نومبر 2026۔ سائٹ کے منتظم محمد فیاض عدیل نے منسلک سرکاری اور علمی ماخذ کے مطابق اس صفحے کی جانچ کی۔ کسی آزاد مفتی یا عالم کی توثیق یا فتویٰ کا دعویٰ نہیں کیا جاتا۔",
            "1447 ہجری (2026) کے رمضان کے پہلے دن کے لیے سرکاری اطلاع میں زکوٰۃ سال 1446–1447 ہجری درج ہے اور مخصوص سیونگ، منافع و نقصان شراکتی (PLS) اور اسی نوعیت کے بینک اکاؤنٹس سے کٹوتی کی حد 503,529 روپے مقرر کی گئی ہے۔ اسٹیٹ بینک آف پاکستان نے یہ اطلاع بینکوں تک پہنچائی۔ یہ مخصوص اکاؤنٹس کے لیے سالانہ قانونی بینک کٹوتی کی حد ہے، ذاتی زکوٰۃ کا نصاب نہیں۔ یہ حد ہر سال بدلتی ہے، اس لیے نئی سرکاری اطلاع کے بغیر اسے اگلے زکوٰۃ سال پر لاگو نہ کریں۔",
            "پاکستان میں رہنے والے افراد کرنسی کوڈ PKR منتخب کریں اور متعلقہ زکوٰۃ سال کے لیے وزارتِ غربت میں کمی اور سماجی تحفظ یا اسٹیٹ بینک آف پاکستان کی تازہ سرکاری اطلاع دیکھیں۔ بینک سے خودکار کٹوتی کا اطلاق اکاؤنٹ کی قسم، قانون، بیان اور قابلِ اطلاق استثنا پر منحصر ہو سکتا ہے۔ آپ کی ذاتی زکوٰۃ اور بینک کی کٹوتی ایک جیسی ہونا ضروری نہیں۔",
            "یہ کیلکولیٹر PKR، USD، GBP، EUR، SAR، AED، INR جیسے تین حروف والے ISO 4217 کرنسی کوڈ قبول کرتا ہے، بشرطیکہ آپ کا براؤزر اسے سپورٹ کرے۔ تمام اثاثے، قرض اور دھات کی قیمت ایک ہی کرنسی میں درج کریں۔ کرنسی کوڈ صرف نتیجے کی علامت اور فارمیٹنگ بدلتا ہے، یہ مختلف کرنسیوں کو خود تبدیل نہیں کرتا۔ اگر آپ کے اثاثے کئی کرنسیوں میں ہیں تو زکوٰۃ کی تاریخ کے قابلِ اعتماد ایکسچینج ریٹ سے پہلے انہیں ایک کرنسی میں تبدیل کریں اور ریکارڈ رکھیں۔",
            "حساب آپ کے براؤزر میں ہوتا ہے۔ اس کے لیے نام، بینک لاگ اِن، اکاؤنٹ نمبر یا مالی دستاویزات درکار نہیں۔ حساس معلومات یا پاس ورڈ درج نہ کریں۔ صفحہ آپ کے اندراجات کو ذاتی اکاؤنٹ میں محفوظ نہیں کرتا۔ اگر آپ کو ریکارڈ چاہیے تو اسے اپنے محفوظ طریقے سے الگ محفوظ کریں۔ مختلف براؤزرز میں کرنسی فارمیٹنگ کی سپورٹ مختلف ہو سکتی ہے، اس لیے معیاری ISO کوڈ استعمال کریں۔",
            "یہ ٹول ہر اثاثے کا شرعی حکم، قرض کی کٹوتی، زیورات کی حیثیت، مشترکہ مال کی تقسیم، پنشن کا حکم یا پچھلے سالوں کی رہ جانے والی زکوٰۃ کا طریقہ طے نہیں کرتا۔ اس کا نتیجہ آپ کے درج کردہ اعداد، دھات کی قیمت، کرنسی کی تبدیلی اور فقہی مفروضوں پر منحصر ہے۔ ذاتی فتویٰ اور پیچیدہ مالی صورت حال کے لیے مستند مقامی عالم سے رجوع کریں۔"
        ],
        "faq": [
            ("کون سا حسابی طریقہ منتخب کروں؟", "اگر آپ حنفی فقہ کی پیروی کرتے ہیں تو سنی — حنفی منتخب کریں۔ شیعہ جعفری — سید سیستانی صرف اسی وقت منتخب کریں جب آپ ان کے شائع شدہ احکام کی پیروی کرتے ہیں۔ دونوں الگ حسابی راستے ہیں۔ دوسرے جعفری مراجع یا دیگر سنی فقہی مکاتب کے احکام مختلف ہو سکتے ہیں اور یہاں نافذ نہیں کیے گئے۔"),
            ("شیعہ جعفری سیستانی اختیار کیا حساب کرتا ہے؟", "یہ آیت اللہ سید سیستانی کے شائع شدہ احتیاطِ واجب کے حکم کے تحت اہل تجارتی مال اور صرف سخت شرائط پوری ہونے پر عام لین دین میں بطور رقم رائج ڈھلے ہوئے سونے یا چاندی کے سکوں کا تخمینہ لگاتا ہے۔ اس میں مالک، نصاب، متعلقہ 11 قمری مہینے یا ایک سال کی مدت، حقِ تصرف اور تجارتی مال کی فروختی قیمت کی شرائط چیک ہوتی ہیں۔ یہ عام نقد رقم، بینک نوٹ، بینک ڈپازٹس، بلین، عام زیورات، خمس، زرعی پیداوار یا مویشی کا حساب نہیں کرتا۔"),
            ("کیا سیستانی کے طریقے میں بینک کی بچت پر واجب زکوٰۃ ہے؟", "ان کے سرکاری سوال و جواب کے مطابق عام بینک ڈپازٹس اور بینک نوٹوں پر واجب زکوٰۃ نہیں۔ سالانہ اخراجات کے بعد بچت پر خمس کا الگ حکم ہو سکتا ہے۔ دوسرے جعفری مراجع کے احکام مختلف ہو سکتے ہیں۔"),
            ("دھات کی قیمت کی کون سی اکائیاں دستیاب ہیں؟", "گرام (1 گرام)، حکومتِ سندھ کا سرکاری تولہ (11.6638 گرام)، یا ٹرائے اونس (31.1034768 گرام) منتخب کریں۔ بازار کا تولہ 12.5 گرام بھی ہو سکتا ہے، اس لیے صراف سے وزن کی تصدیق کریں۔ اگر وزن مختلف ہو تو قیمت فی گرام میں تبدیل کر کے گرام منتخب کریں۔")
        ],
        "sources": 'اہم اور معاون ماخذ: <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/2317/" rel="noopener noreferrer">آیت اللہ سیستانی کے سونے کے نصاب کے سرکاری احکام</a>؛ <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/2318/" rel="noopener noreferrer">چاندی اور سکوں کے سرکاری احکام</a>؛ <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/8243/" rel="noopener noreferrer">مثقال کے وزن کا سرکاری جدول</a>؛ <a class="' + LINK + '" href="https://www.sistani.org/english/book/48/2323/" rel="noopener noreferrer">تجارتی مال کی شرائط</a>؛ <a class="' + LINK + '" href="https://www.sistani.org/english/qa/14884/" rel="noopener noreferrer">بینک ڈپازٹس اور بینک نوٹوں کے بارے میں سرکاری جواب</a>؛ <a class="' + LINK + '" href="https://islamqa.org/hanafi/answerstofatawa/118729/who-is-liable-to-pay-zakat/" rel="noopener noreferrer">حنفی نصاب: 87.48 گرام سونا اور 612.36 گرام چاندی</a>؛ <a class="' + LINK + '" href="https://islamqa.org/hanafi/darulfiqh/156652/" rel="noopener noreferrer">حنفی زیورات کے بارے میں دارالفقہ کی رہنمائی</a>؛ <a class="' + LINK + '" href="https://seekersguidance.org/answers/hanafi-fiqh/which-debts-affect-zakat-for-both-debtor-and-creditor/" rel="noopener noreferrer">حنفی قرض کی کٹوتی کے بارے میں علمی رہنمائی</a>؛ <a class="' + LINK + '" href="https://sindhlaws.gov.pk/Setup/Publications_SindhCode/PUB-16-000006.pdf" rel="noopener noreferrer">حکومتِ سندھ کا سرکاری تولہ تبدیلی جدول</a>؛ <a class="' + LINK + '" href="https://www.islamic-relief.org.uk/giving/islamic-giving/zakat/zakat-on-jewellery/" rel="noopener noreferrer">اسلامک ریلیف کی زیورات اور تولہ رہنمائی</a>؛ <a class="' + LINK + '" href="https://nzfworldwide.com/wp-content/uploads/2022/03/NZF_Zakat-Calculation-Principle-No.1.pdf" rel="noopener noreferrer">NZF Worldwide کے زکوٰۃ اصول</a>؛ <a class="' + LINK + '" href="https://www.sbp.org.pk/circulars/bprd-circular-letter-no-03-of-2026" rel="noopener noreferrer">اسٹیٹ بینک کا 2026 سرکلر</a>۔ یہ ماخذ مخصوص مراجع اور طریقوں کی وضاحت کرتے ہیں، ہر شخص کے لیے ایک ہی شرعی حکم نہیں بناتے۔'
    },
    "bmi-calculator": {
        "name": "BMI کیلکولیٹر",
        "title": "بالغ BMI کیلکولیٹر اردو میں | وزن اور قد | CalculatesAll",
        "description": "بالغوں کا BMI اردو میں نکالیں۔ وزن kg/lb اور قد cm یا فٹ/انچ درج کریں، فارمولا اور WHO حدود سمجھیں۔ BMI اسکریننگ ہے، تشخیص نہیں۔",
        "h1": "بالغوں کے لیے BMI کیلکولیٹر",
        "lead": "بالغوں کا BMI = وزن (kg) ÷ قد (میٹر)²۔ یعنی وزن کو قد کے مربع سے تقسیم کریں۔ 18.5 سے 25 سے کم عمومی حد ہے۔ BMI اسکریننگ ہے، تشخیص نہیں۔",
        "labels": [
            ("Weight (kg)", "وزن (کلو گرام)"),
            ("Weight unit", "وزن کی اکائی"),
            ("Kilograms (kg)", "کلوگرام (kg)"),
            ("Pounds (lb)", "پاؤنڈ (lb)"),
            ("Weight (lb)", "وزن (پاؤنڈ)"),
            ("Height unit", "قد کی اکائی"),
            ("Centimeters (cm)", "سینٹی میٹر (cm)"),
            ("Feet and inches", "فٹ اور انچ"),
            ("Height (cm)", "قد (سینٹی میٹر)"),
            ("Height (ft)", "قد (فٹ)"),
            ("Height (in, 0 to 11.99)", "قد (انچ، 0 سے 11.99)"),
            ("Calculate BMI", "BMI کا حساب کریں"),
        ],
        "how_heading": "فارمولا، درجہ بندی اور حدود",
        "faq_heading": "عام سوالات (FAQ)",
        "how": [
            "بالغوں کا باڈی ماس انڈیکس (BMI) نکالنے کے لیے وزن کلوگرام میں اور قد میٹر میں درکار ہوتا ہے۔ فارمولا یہ ہے: BMI = وزن (کلوگرام) ÷ قد (میٹر)²۔ اگر قد سینٹی میٹر میں ہو تو اسے 100 پر تقسیم کر کے میٹر میں تبدیل کریں۔",
            "اگر قد فٹ اور انچ میں درج کریں تو پہلے کل انچ نکالیں: (فٹ × 12) + انچ۔ پھر کل انچ کو 2.54 سے ضرب دے کر سینٹی میٹر حاصل کریں۔ وزن کلوگرام یا پاؤنڈ میں منتخب کیا جا سکتا ہے؛ پاؤنڈ کو حساب سے پہلے کلوگرام میں تبدیل کیا جاتا ہے۔",
            "بالغوں کے لیے WHO کی عام درجہ بندی میں 18.5 سے کم BMI کم وزن، 18.5 سے 25 سے کم معمول کا وزن، 25 سے 30 سے کم زیادہ وزن، اور 30 یا اس سے زیادہ موٹاپے کی حد ہے۔ درجہ اصل غیر گول شدہ BMI سے منتخب ہوتا ہے، جبکہ اسکرین پر قدر صرف ایک اعشاری جگہ تک گول دکھائی جاتی ہے۔ مثال کے طور پر اصل BMI 24.9827 ہو تو اسکرین پر 25.0 دکھائی دے سکتا ہے، مگر درجہ معمول کا وزن رہے گا کیونکہ اصل قدر 25 سے کم ہے۔",
            "مثال کے طور پر 70 کلوگرام وزن اور 170 سینٹی میٹر قد پر حساب 70 ÷ (1.70 × 1.70) ہے۔ نتیجہ تقریباً 24.2 بنتا ہے، جو بالغوں میں معمول کے وزن کی حد میں آتا ہے۔ اگر قد 5 فٹ 7 انچ ہو تو یہ 67 انچ یا 170.18 سینٹی میٹر بنتا ہے۔",
            "BMI ایک عمومی اسکریننگ پیمانہ ہے، تشخیص نہیں اور ڈاکٹر کے مشورے کا متبادل نہیں۔ یہ جسمانی چربی کو براہ راست نہیں ناپتا اور نہ یہ بتاتا ہے کہ چربی جسم میں کہاں موجود ہے۔ زیادہ عضلات رکھنے والے افراد کا BMI بلند ہو سکتا ہے، اس لیے ایک جیسا BMI دو افراد میں ایک جیسی جسمانی ساخت یا صحت کی نشاندہی نہیں کرتا۔",
            "بچوں اور نوعمروں کے لیے یہ بالغوں والی درجہ بندی استعمال نہیں کرنی چاہیے۔ ان کی جانچ عمر اور جنس کے مطابق BMI-for-age گروتھ چارٹس سے کی جاتی ہے۔ حمل کے دوران بھی BMI کو خاص سیاق میں سمجھنا ضروری ہے۔ بعض بڑی عمر کے افراد یا جسم میں پانی جمع ہونے، بیماری یا عضلات کم ہونے کی صورتوں میں BMI محدود معلومات دے سکتا ہے۔",
            "نتیجے کو صرف عمومی اسکریننگ معلومات سمجھیں، مکمل طبی جانچ نہیں۔ معالج وزن کے ساتھ کمر کا گھیر، بلڈ پریشر، خون کے ٹیسٹ، ادویات، طبی تاریخ، خوراک اور جسمانی سرگرمی بھی دیکھ سکتا ہے۔ اگر وزن تیزی سے بدلے، علامات ہوں، کوئی بیماری ہو یا آپ کو ذاتی مشورہ چاہیے تو مستند ڈاکٹر سے بات کریں۔",
            "یہ ٹول قد کی حد سینٹی میٹر میں 50 سے 260، یا فٹ میں 1 سے 8 اور انچ میں 0 سے 11.99 قبول کرتا ہے۔ وزن کی حد 20 سے 300 کلوگرام یا 44.1 سے 661.3 پاؤنڈ ہے۔ یہ صرف کیلکولیٹر کی ان پٹ حدود ہیں، صحت کے لیے تجویز کردہ وزن یا قد نہیں۔",
        ],
        "faq": [
            ("کیا یہ کیلکولیٹر بچوں اور نوعمروں کے لیے ہے؟", "نہیں۔ یہ بالغوں کے BMI کی درجہ بندی استعمال کرتا ہے۔ بچوں اور نوعمروں کے لیے عمر اور جنس کے مطابق BMI-for-age گروتھ چارٹس درکار ہوتے ہیں۔"),
            ("کیا BMI جسمانی چربی کو ناپتا ہے؟", "نہیں۔ یہ صرف قد اور وزن سے حساب ہوتا ہے۔ یہ جسمانی چربی کو براہ راست نہیں ناپتا اور نہ عضلات اور چربی میں فرق کرتا ہے۔"),
            ("کیا BMI 25 ہونا بیماری کی تشخیص ہے؟", "نہیں۔ گول کی گئی BMI قدر 25.0 بالغوں میں زیادہ وزن کی اسکریننگ حد کا آغاز ہے، تشخیص نہیں۔"),
            ("نتیجے کے بعد کیا کرنا چاہیے؟", "اسے عمومی معلومات سمجھیں۔ اگر وزن میں بڑی تبدیلی، علامات یا طبی مسئلہ ہو تو مستند معالج سے مشورہ کریں۔"),
            ("کیا جنوبی ایشیائی افراد کے لیے BMI کی اضافی حدیں ہیں؟", "جی ہاں۔ WHO کی ماہرین کی مشاورت نے 23.0 اور 27.5 کو اضافی عوامی صحت کے اقدام کے مقامات کے طور پر شناخت کیا، مگر انہیں ہر ایشیائی آبادی کے لیے ایک ہی نئی عالمی درجہ بندی قرار نہیں دیا۔"),
            ("کیا یہ کیلکولیٹر جنوبی ایشیائی خطرے کی حدیں بھی لاگو کرتا ہے؟", "نہیں۔ یہ کیلکولیٹر معیاری بین الاقوامی بالغ BMI درجہ بندی دکھاتا ہے۔ جنوبی ایشیائی پس منظر میں ذاتی خطرے کی تشریح کے لیے مقامی طبی رہنمائی اور معالج سے مشورہ کریں۔"),
        ],
        "sources": 'بالغوں کی معیاری درجہ بندی کے لیے <a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" target="_blank" rel="noopener noreferrer">عالمی ادارۂ صحت (WHO) کی رہنمائی</a>، <a class="' + LINK + '" href="https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html" target="_blank" rel="noopener noreferrer">CDC کی بالغ BMI درجہ بندی</a> اور <a class="' + LINK + '" href="https://www.nhs.uk/health-assessment-tools/calculate-your-body-mass-index/calculate-bmi-for-adults" target="_blank" rel="noopener noreferrer">NHS کی بالغ BMI رہنمائی</a> اور <a class="' + LINK + '" href="https://www.nhs.uk/health-assessment-tools/calculate-your-waist-to-height-ratio" target="_blank" rel="noopener noreferrer">NHS کی کمر اور قد کے تناسب کی رہنمائی</a> دیکھیں۔ ایشیائی آبادیوں کے اضافی BMI اقدام کے مقامات کے لیے <a class="' + LINK + '" href="https://pubmed.ncbi.nlm.nih.gov/14726171/" target="_blank" rel="noopener noreferrer">WHO Expert Consultation کی تحقیق</a> اور <a class="' + LINK + '" href="https://doi.org/10.2337/doci26-0003" target="_blank" rel="noopener noreferrer">2026 Standards of Care</a> بھی ملاحظہ کریں۔',
    },
}

BMI_URDU_SECTIONS = [
    ("bmi-urdu-measurement", "وزن اور قد کی پیمائش کیسے درست رکھیں?", [
        "قد ناپتے وقت جوتے اتاریں، سیدھی سطح پر کھڑے ہوں اور سر کو سیدھا رکھیں۔ وزن کے لیے ترازو سخت اور ہموار فرش پر رکھیں۔ درست اکائی منتخب کریں اور سینٹی میٹر کو میٹر سمجھ کر درج نہ کریں۔",
        "BMI ایک عمومی اسکریننگ پیمانہ ہے، تشخیص نہیں اور ڈاکٹر کے مشورے کا متبادل نہیں۔ اگر آپ وقت کے ساتھ تبدیلی دیکھ رہے ہیں تو ایک ہی ترازو اور ملتے جلتے حالات میں پیمائش کریں۔ یہ طریقہ ریکارڈ کو زیادہ قابلِ موازنہ بناتا ہے، مگر BMI کو طبی تشخیص نہیں بناتا۔",
    ]),
    ("bmi-urdu-rounding", "دکھائی گئی BMI قدر اور درجہ مختلف کیوں ہو سکتے ہیں?", [
        "درجہ اصل غیر گول شدہ BMI سے منتخب ہوتا ہے، جبکہ اسکرین پر قدر ایک اعشاری جگہ تک گول دکھائی جاتی ہے۔ مثال کے طور پر اصل BMI 24.9827 ہو تو 25.0 دکھائی دے سکتا ہے، مگر درجہ معمول کا وزن رہتا ہے کیونکہ اصل قدر 25 سے کم ہے۔",
        "بالغوں کی معیاری WHO حد میں معمول کا وزن 18.5 سے 25 سے کم BMI ہے۔ یہ عددی حد اسکریننگ کے لیے ہے، کسی فرد کی بیماری کی تشخیص نہیں۔",
    ]),
    ("bmi-urdu-south-asian", "جنوبی ایشیائی افراد کے لیے اضافی BMI حدود کیا ہیں?", [
        "جنوبی ایشیائی پس منظر کے بعض افراد میں ذیابیطس اور دل کی بیماری کا خطرہ نسبتاً کم BMI پر بھی بڑھ سکتا ہے۔ WHO کی 2004 ماہرین کی مشاورت نے 23.0 اور 27.5 کو اضافی عوامی صحت کے اقدام کے مقامات بتایا، مگر واضح کیا کہ تمام ایشیائی آبادیوں کے لیے ایک ہی نئی حد مقرر نہیں کی جا سکتی۔ یہ اقدام کے مقامات معیاری بین الاقوامی 18.5، 25 اور 30 کی درجہ بندی کا متبادل نہیں ہیں۔",
        "برطانیہ کی NHS رہنمائی جنوبی ایشیائی پس منظر کے بالغ افراد کے لیے BMI 23 سے 27.4 کو زائد وزن اور 27.5 یا اس سے زیادہ کو موٹاپے کی حد شمار کرتی ہے۔ یہ NHS کی مخصوص رہنمائی ہے، ہر ملک یا ہر فرد کے لیے خودکار تشخیص نہیں۔ یہ کیلکولیٹر معیاری WHO حدود دکھاتا ہے اور ان اضافی حدوں کو خودکار طور پر لاگو نہیں کرتا۔",
    ]),
    ("bmi-urdu-waist", "کمر کے گھیر اور قد کا تناسب کیوں اہم ہے?", [
        "2026 Standards of Care in Overweight and Obesity کے مطابق ایشیائی پس منظر کے بالغ افراد میں BMI 23 kg/m² سے اضافی چربی کی اسکریننگ کی جا سکتی ہے۔ موٹاپے کی طبی تشخیص کے لیے یہ معیار BMI 27.5 kg/m² یا اس سے زیادہ، یا BMI 23 سے 27.4 کے ساتھ مرکزی چربی کی موجودگی (کمر اور قد کا تناسب کم از کم 0.5، یا کمر کا گھیر خواتین میں کم از کم 80 cm اور مردوں میں 90 cm) بیان کرتا ہے۔ اس معیار میں یہ بھی بتایا گیا ہے کہ مختلف ایشیائی ممالک کے لیے مخصوص حدیں مختلف ہو سکتی ہیں۔ یہ طبی معیار ہیں، خود تشخیص یا اس کیلکولیٹر کی خودکار درجہ بندی نہیں۔",
        "NHS کی رہنمائی میں BMI 35 سے کم رکھنے والے بالغ افراد کے لیے کمر کا گھیر قد کے نصف سے کم رکھنے کی عملی جانچ بھی شامل ہے۔ مثال کے طور پر 175 cm قد کا نصف 87.5 cm ہے۔ یہ صرف اسکریننگ رہنمائی ہے، تشخیص نہیں۔ یہ کیلکولیٹر کمر کی پیمائش نہیں لیتا اور ان اضافی معیاروں کو خودکار طور پر لاگو نہیں کرتا۔",
    ]),
    ("bmi-urdu-search-intent", "پاکستان میں BMI calculator اور Body Mass Index کا اردو مطلب", [
        "پاکستان میں BMI calculator تلاش کرنے والے بالغ افراد اس صفحے پر وزن اور قد کی درست اکائیاں منتخب کرکے اپنا BMI معلوم کر سکتے ہیں۔ وزن kg یا lb اور قد cm یا فٹ/انچ میں درج کریں۔",
        "Body Mass Index کا اردو مطلب جسمانی کمیت کا اشاریہ ہے۔ یہ وزن اور قد سے حاصل ہونے والا اسکریننگ پیمانہ ہے، طبی تشخیص نہیں۔ نتیجے کو WHO کی بالغوں کی حدود اور صفحے پر بیان کردہ جنوبی ایشیائی تناظر کے ساتھ سمجھیں۔",
    ]),

]


def bmi_urdu_guide_html():
    out = ""
    for section_id, heading, paragraphs in BMI_URDU_SECTIONS:
        out += '<section class="mt-8" aria-labelledby="' + section_id + '">'
        out += '<h2 id="' + section_id + '" class="' + H2 + '">' + heading + '</h2>'
        if section_id == "bmi-urdu-categories":
            out += (
                '<div class="mt-4 overflow-x-auto rounded-xl border border-stone-300 dark:border-stone-700">'
                '<table dir="rtl" class="w-full border-collapse text-sm" aria-label="بالغوں کی BMI درجہ بندی">'
                '<thead><tr>'
                '<th scope="col" class="border-b border-stone-300 dark:border-stone-700 p-3 text-start">BMI (kg/m²)</th>'
                '<th scope="col" class="border-b border-stone-300 dark:border-stone-700 p-3 text-start">بالغوں کا زمرہ</th>'
                '</tr></thead><tbody>'
                '<tr><td class="border-b border-stone-200 dark:border-stone-800 p-3">18.5 سے کم</td><td class="border-b border-stone-200 dark:border-stone-800 p-3">کم وزن</td></tr>'
                '<tr><td class="border-b border-stone-200 dark:border-stone-800 p-3">18.5 سے 24.9</td><td class="border-b border-stone-200 dark:border-stone-800 p-3">معمول کا وزن</td></tr>'
                '<tr><td class="border-b border-stone-200 dark:border-stone-800 p-3">25.0 سے 29.9</td><td class="border-b border-stone-200 dark:border-stone-800 p-3">زیادہ وزن</td></tr>'
                '<tr><td class="p-3">30.0 یا زیادہ</td><td class="p-3">موٹاپا</td></tr>'
                '</tbody></table></div>'
            )
        for paragraph in paragraphs:
            out += '<p class="' + P + '">' + paragraph + '</p>'
        out += '</section>'
    return out



EXTRA = {
    "zakat-calculator": {
        "quick": "Total eligible assets minus eligible liabilities equals net zakatable wealth. Compare that amount with the silver or gold Nisab you selected using the current price per gram you entered. If the selected threshold is met and the lunar year (hawl) is complete, the estimate applies 2.5 percent and subtracts Zakat already paid for the same year.",
        "faq": [],
    },
    "bmi-calculator": {
        "quick": "BMI uses weight in kg divided by height in metres squared when kg is selected, or 703 × weight in lb divided by height in total inches squared when lb is selected. For adults, 18.5 to 24.9 is the WHO normal weight range.",
        "faq": [
            ("Is a BMI of 25 unhealthy?", "A BMI of 25 is at the start of the overweight range. It is a screening number only. Waist size, blood pressure and blood tests give a fuller picture, and a clinician can interpret them with you."),
            ("Does BMI work for athletes?", "BMI can overstate body fat in people with high muscle mass. A clinician can use other measures for athletes."),
        ],
    },
    "profit-loss-calculator": {
        "quick": "",
        "faq": [
            ("What is the difference between markup and margin?", "Product markup uses cost as its base; product gross margin uses selling price. Business operating margin uses revenue after listed expenses. These percentages are not interchangeable."),
            ("How do I include shipping?", "Add shipping, packaging and platform fees to the cost price before you calculate."),
            ("Does this calculator include tax automatically?", "No. Enter relevant direct costs and expenses in the appropriate fields. Sales tax, income tax, refunds and statutory accounting treatment are not inferred by the calculator."),
            ("What does net operating profit mean here?", "In Business P&L mode it is revenue minus cost of goods sold and the other expenses you enter. It is not a full audited income statement and may exclude interest, tax or costs that you have not entered."),
        ],
    },
    "discount-calculator": {
        "quick": "",
        "faq": [
            ("How do I calculate two discounts together?", "Apply the first discount to the original price, then apply the second discount to the reduced price. Stacked discounts are not the same as adding the percentages."),
        ],
    },
    "age-calculator": {
        "quick": "Age is calculated by subtracting the birth date from today's date, year by year, month by month and day by day, then borrowing from the previous month where needed.",
        "faq": [
            ("How do I find my age in days?", "Enter your date of birth. The total days lived figure is shown with your years, months and days."),
        ],
    },
    "unit-converter": {
        "quick": "Convert by multiplying the value by the factor from the starting unit to the base unit, then dividing by the factor from the target unit to the base unit.",
        "faq": [
            ("How do I convert centimeters to inches?", "Divide centimeters by 2.54. For example, 10 cm is about 3.94 inches. One inch is exactly 2.54 centimeters."),
            ("How do I convert kilograms to pounds?", "Multiply kilograms by about 2.20462262. For example, 1 kg is about 2.2046 lb. The exact reference is 1 lb = 0.45359237 kg."),
            ("How do I convert Celsius to Fahrenheit?", "Multiply Celsius by 9, divide by 5, then add 32."),
        ],
    },
    "standard-calculator": {
        "quick": "Multiplication and division run before addition and subtraction. The percent key divides the last number by 100.",
        "faq": [
            ("Does this calculator handle parentheses?", "Yes. Use the ( and ) buttons to group calculations. Multiplication and division run before addition and subtraction."),
        ],
    },
    "tasbih-counter": {
        "quick": "",
        "faq": [],
    },
    "stopwatch": {
        "quick": "Press Start to begin timing, Stop to pause, and Reset to clear. The display shows hours, minutes, seconds and hundredths.",
        "faq": [
            ("Does the stopwatch continue after I close the tab?", "No. Closing or reloading the page stops and clears the stopwatch."),
        ],
    },
}


DIGIT = "bg-white dark:bg-stone-800 border border-slate-200 dark:border-stone-600 text-slate-900 dark:text-stone-100 text-2xl font-semibold rounded-xl min-h-[64px] shadow-sm hover:bg-teal-50 dark:hover:bg-stone-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700"
OPS = "bg-teal-700 hover:bg-teal-800 dark:bg-teal-700 dark:hover:bg-teal-600 text-white text-2xl font-bold rounded-xl min-h-[64px] shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700"
SPECIAL = "bg-slate-100 hover:bg-teal-50 dark:bg-stone-700 dark:hover:bg-stone-600 border border-slate-200 dark:border-stone-600 text-slate-900 dark:text-stone-100 text-xl font-bold rounded-xl min-h-[64px] shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700"
EQUALS = "bg-slate-900 hover:bg-slate-800 dark:bg-teal-700 dark:hover:bg-teal-600 text-white text-2xl font-bold rounded-xl min-h-[64px] shadow-md col-span-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700"

CALC_UI = (
    '<div class="ca-calculator-engine max-w-xl mx-auto">'
    '<output id="calc-display" class="block text-right text-4xl font-bold bg-white dark:bg-stone-950 border border-slate-200 dark:border-stone-600 rounded-2xl px-5 py-6 min-h-[5rem] break-all text-slate-900 dark:text-stone-100 shadow-inner" aria-live="polite">0</output>'
    '<button id="calc-mode-toggle" type="button" class="' + SPECIAL + ' mt-3 w-full" aria-pressed="false">Scientific Mode</button>'
    '<p id="calc-history" class="mt-2 min-h-6 text-right text-xs text-stone-600 dark:text-stone-300 break-words" aria-live="polite"></p>'
    '<div id="calc-pad" class="grid grid-cols-4 gap-3 mt-3">'
    '<button class="' + SPECIAL + '" data-key="C">C</button>'
    '<button class="' + DIGIT + '" data-key="(" aria-label="Open parenthesis">(</button>'
    '<button class="' + DIGIT + '" data-key=")" aria-label="Close parenthesis">)</button>'
    '<button class="' + SPECIAL + '" data-key="BS" aria-label="Delete last character">⌫</button>'
    '<button class="' + DIGIT + '" data-key="7">7</button>'
    '<button class="' + DIGIT + '" data-key="8">8</button>'
    '<button class="' + DIGIT + '" data-key="9">9</button>'
    '<button class="' + OPS + '" data-key="/" aria-label="Divide">÷</button>'
    '<button class="' + DIGIT + '" data-key="4">4</button>'
    '<button class="' + DIGIT + '" data-key="5">5</button>'
    '<button class="' + DIGIT + '" data-key="6">6</button>'
    '<button class="' + OPS + '" data-key="*" aria-label="Multiply">×</button>'
    '<button class="' + DIGIT + '" data-key="1">1</button>'
    '<button class="' + DIGIT + '" data-key="2">2</button>'
    '<button class="' + DIGIT + '" data-key="3">3</button>'
    '<button class="' + OPS + '" data-key="-" aria-label="Subtract">−</button>'
    '<button class="' + DIGIT + '" data-key="00">00</button>'
    '<button class="' + DIGIT + '" data-key="0">0</button>'
    '<button class="' + DIGIT + '" data-key=".">.</button>'
    '<button class="' + OPS + '" data-key="+" aria-label="Add">+</button>'
    '<button class="' + SPECIAL + '" data-key="sqrt" aria-label="Square root">√</button>'
    '<button class="' + SPECIAL + '" data-key="%">%</button>'
    '<button class="' + EQUALS + '" data-key="=">=</button>'
    '</div>'
    '<div id="scientific-pad" class="grid grid-cols-5 gap-2 mt-3" hidden>'
    '<button id="calc-angle-toggle" type="button" class="' + SPECIAL + '" data-key="angle-toggle" aria-pressed="false">DEG</button>'
    '<button class="' + SPECIAL + '" data-key="C">AC</button>'
    '<button class="' + SPECIAL + '" data-key="BS" aria-label="Delete last character">⌫</button>'
    '<button class="' + SPECIAL + '" data-key="M+">M+</button>'
    '<button class="' + SPECIAL + '" data-key="MR">MR</button>'
    '<button class="' + SPECIAL + '" data-key="MC">MC</button>'
    '<button class="' + DIGIT + '" data-key="(">(</button>'
    '<button class="' + DIGIT + '" data-key=")">)</button>'
    '<button class="' + DIGIT + '" data-key="pi">π</button>'
    '<button class="' + DIGIT + '" data-key="e">e</button>'
    '<button class="' + SPECIAL + '" data-key="Ans">Ans</button>'
    '<button class="' + SPECIAL + '" data-key="sin">sin</button>'
    '<button class="' + SPECIAL + '" data-key="cos">cos</button>'
    '<button class="' + SPECIAL + '" data-key="tan">tan</button>'
    '<button class="' + SPECIAL + '" data-key="asin">sin⁻¹</button>'
    '<button class="' + SPECIAL + '" data-key="acos">cos⁻¹</button>'
    '<button class="' + SPECIAL + '" data-key="atan">tan⁻¹</button>'
    '<button class="' + SPECIAL + '" data-key="acsc">csc⁻¹</button>'
    '<button class="' + SPECIAL + '" data-key="asec">sec⁻¹</button>'
    '<button class="' + SPECIAL + '" data-key="acot">cot⁻¹</button>'
    '<button class="' + SPECIAL + '" data-key="sec">sec</button>'
    '<button class="' + SPECIAL + '" data-key="csc">csc</button>'
    '<button class="' + SPECIAL + '" data-key="cot">cot</button>'
    '<button class="' + SPECIAL + '" data-key="sqrt">√</button>'
    '<button class="' + SPECIAL + '" data-key="cbrt">∛</button>'
    '<button class="' + SPECIAL + '" data-key="root">ⁿ√</button>'
    '<button class="' + SPECIAL + '" data-key="square">x²</button>'
    '<button class="' + SPECIAL + '" data-key="cube">x³</button>'
    '<button class="' + SPECIAL + '" data-key="^">xʸ</button>'
    '<button class="' + SPECIAL + '" data-key="log">log</button>'
    '<button class="' + SPECIAL + '" data-key="ln">ln</button>'
    '<button class="' + SPECIAL + '" data-key="exp">eˣ</button>'
    '<button class="' + SPECIAL + '" data-key="tenpow">10ˣ</button>'
    '<button class="' + SPECIAL + '" data-key="reciprocal">1/x</button>'
    '<button class="' + SPECIAL + '" data-key="sinh">sinh</button>'
    '<button class="' + SPECIAL + '" data-key="cosh">cosh</button>'
    '<button class="' + SPECIAL + '" data-key="tanh">tanh</button>'
    '<button class="' + SPECIAL + '" data-key="csch">csch</button>'
    '<button class="' + SPECIAL + '" data-key="sech">sech</button>'
    '<button class="' + SPECIAL + '" data-key="coth">coth</button>'
    '<button class="' + SPECIAL + '" data-key="abs">abs</button>'
    '<button class="' + SPECIAL + '" data-key="floor">floor</button>'
    '<button class="' + SPECIAL + '" data-key="ceil">ceil</button>'
    '<button class="' + SPECIAL + '" data-key="round">round</button>'
    '<button class="' + SPECIAL + '" data-key="!">n!</button>'
    '<button class="' + SPECIAL + '" data-key="%">%</button>'
    '<button class="' + SPECIAL + '" data-key="nPr">nPr</button>'
    '<button class="' + SPECIAL + '" data-key="nCr">nCr</button>'
    '<button class="' + SPECIAL + '" data-key="mod">mod</button>'
    '<button class="' + SPECIAL + '" data-key="mean">mean</button>'
    '<button class="' + SPECIAL + '" data-key="median">median</button>'
    '<button class="' + SPECIAL + '" data-key="stdev">stdev</button>'
    '<button class="' + SPECIAL + '" data-key="stdevp">stdevp</button>'
    '<button class="' + SPECIAL + '" data-key="var">var</button>'
    '<button class="' + SPECIAL + '" data-key="varp">varp</button>'
    '<button class="' + SPECIAL + '" data-key="min">min</button>'
    '<button class="' + SPECIAL + '" data-key="max">max</button>'
    '<button class="' + SPECIAL + '" data-key="sum">sum</button>'
    '<button class="' + SPECIAL + '" data-key="gcd">gcd</button>'
    '<button class="' + SPECIAL + '" data-key="lcm">lcm</button>'
    '<button class="' + DIGIT + '" data-key="7">7</button>'
    '<button class="' + DIGIT + '" data-key="8">8</button>'
    '<button class="' + DIGIT + '" data-key="9">9</button>'
    '<button class="' + OPS + '" data-key="/">÷</button>'
    '<button class="' + OPS + '" data-key="*">×</button>'
    '<button class="' + DIGIT + '" data-key="4">4</button>'
    '<button class="' + DIGIT + '" data-key="5">5</button>'
    '<button class="' + DIGIT + '" data-key="6">6</button>'
    '<button class="' + OPS + '" data-key="-">−</button>'
    '<button class="' + OPS + '" data-key="+">+</button>'
    '<button class="' + DIGIT + '" data-key="1">1</button>'
    '<button class="' + DIGIT + '" data-key="2">2</button>'
    '<button class="' + DIGIT + '" data-key="3">3</button>'
    '<button class="' + DIGIT + '" data-key="0">0</button>'
    '<button class="' + DIGIT + '" data-key=".">.</button>'
    '<button class="' + EQUALS + '" data-key="=">=</button>'
    '</div></div>'
)


# Independent time-conversion and question calculators. Both are linked automatically
# in the navigation, category pages, home tool list, sitemap, and SEO metadata.
TOOLS.extend([
    {
        "slug": "years-to-days-calculator", "category": "time",
        "name": "Years to Days Calculator", "app": "UtilitiesApplication",
        "description": "Convert years to days or days to years using 365, 365.25 or 365.2425-day methods. Use a start date for exact Gregorian calendar days.",
        "h1": "Years to Days Calculator",
        "lead": "Convert years and days with 365, 365.25 or 365.2425-day methods. Use a start date to count exact calendar days.",
        "ui": (
            '<form id="years-days-form" class="space-y-3" novalidate>'
            '<div class="grid grid-cols-2 gap-3">'
            '<div><label class="@L@" for="yd-direction">Convert</label>'
            '<select class="@I@" id="yd-direction"><option value="years-to-days">Years to days</option><option value="days-to-years">Days to years</option></select></div>'
            '<div><label class="@L@" for="yd-method">Year length</label>'
            '<select class="@I@" id="yd-method"><option value="365">365-day year</option><option value="365.25">Julian average (365.25)</option><option value="365.2425">Gregorian average (365.2425)</option><option id="yd-calendar-option" value="calendar">Exact calendar years (years to days only)</option></select></div>'
            '</div>'
            '<label class="@L@" id="yd-value-label" for="yd-value">Number of years</label>'
            '<input class="@I@" id="yd-value" type="number" min="0" max="1000000" step="any" inputmode="decimal" value="80" required>'
            '<div id="yd-exact-fields" hidden><label class="@L@" for="yd-start-date">Start date (Gregorian calendar)</label>'
            '<input class="@I@" id="yd-start-date" type="date" min="0001-01-01" max="9999-12-31" disabled>'
            '<p class="mt-2 text-sm">Exact mode accepts whole years and counts actual days from the start date up to, but not including, the anniversary. For 29 February, a non-leap anniversary uses 1 March.</p></div>'
            '<button id="yd-submit" class="@B@" type="submit">Convert Years</button></form>'
            '<div id="yd-result" class="@R@" role="status" aria-live="polite"></div>'
        ),
        "guide": [
            ("Quick answers to common years-to-days questions", [
                "Using the 365.2425-day Gregorian mean, 5 years = 1,826.2125 days using the Gregorian average. The 365-day method gives 1,825 days, while the 365.25-day Julian average gives 1,826.25 days.",
                "Using the 365.2425-day Gregorian mean, 30 years = 10,957.275 days using the Gregorian average. The 365-day method gives 10,950 days, while the 365.25-day Julian average gives 10,957.5 days.",
                "For the reverse question, 70,000 days ÷ 365.2425 = 191.6535 years using the Gregorian mean. This is a decimal-year estimate, not an exact calendar age.",
                "Exact calendar days depend on the start date because the actual Gregorian interval may include leap days. Enter the start date and a whole number of years in Exact calendar years when you need the elapsed day count for a specific anniversary.",
                "The Gregorian rule adds 97 leap days in each 400-year cycle, which produces the 365.2425-day average. The <a class='" + LINK + "' href='https://aa.usno.navy.mil/faq/leap_years' target='_blank' rel='noopener noreferrer'>U.S. Naval Observatory leap-year explanation</a> describes the rule, and <a class='" + LINK + "' href='https://www.nist.gov/pml/time-and-frequency-division/popular-links/time-frequency-z/time-frequency-z-x-z' target='_blank' rel='noopener noreferrer'>NIST's year definition</a> identifies the average Gregorian year as 365.2425 days."
            ])
        ],
        "faq": [
            ("Which year-length methods can I use?", "Choose 365 days, the 365.25-day Julian year or the 365.2425-day Gregorian average. These are fixed-duration conversions; the exact calendar option counts actual days from a start date."),
            ("Does exact calendar mode include leap days?", "Yes. It counts actual Gregorian calendar days up to, but not including, the ending anniversary. A 29 February start uses 1 March when the ending year is not a leap year."),
            ("Can I convert days to years?", "Yes. Select Days to years and choose one of the three fixed year lengths. The result is a decimal-year estimate with an approximate years, months and days breakdown."),
            ("Can exact calendar mode use decimal years?", "No. Exact calendar mode accepts whole years and a valid Gregorian start date. The fixed 365, 365.25 and 365.2425 methods accept decimal values."),
            ("How many days are in 13 years?", "Using the 365.2425-day Gregorian average, 13 years is 4,748.1525 days (about 4,748.15 days). The exact count in a calendar interval can differ because leap days depend on the start date. Use Exact calendar years to count an actual 13-year anniversary interval."),
        ],
        "sources": 'Julian year: exactly 365.25 days (<a class="' + LINK + '" href="https://ssd.jpl.nasa.gov/astro_par.html" target="_blank" rel="noopener noreferrer">NASA/JPL astrodynamic parameters</a>). Gregorian mean year: 365.2425 days over the 400-year cycle (<a class="' + LINK + '" href="https://aa.usno.navy.mil/faq/leap_years" target="_blank" rel="noopener noreferrer">U.S. Naval Observatory leap-year guidance</a>).'
    },
    {
        "slug": "query-calculator", "category": "time",
        "name": "Query Calculator", "app": "UtilitiesApplication",
        "description": "Ask supported time, date and simple arithmetic questions in plain language. Convert years, months, weeks and hours, calculate Gregorian age from a birth date, and see the method.",
        "h1": "Time & Date Query Calculator",
        "lead": "Type a supported question in plain language, such as 115 months in years and days, 80 years to days, a date of birth, or 2 weeks to hours. Results use stated conversion rules, and unsupported questions are not guessed.",
        "ui": (
            '<form id="query-time-form" class="space-y-4" novalidate>'
            '<label class="@L@" for="qt-question">Your question</label>'
            '<input class="@I@" id="qt-question" type="text" maxlength="160" value="DOB 29-02-1984 age in days" required>'
            '<p class="text-sm">Try: 115 months in years and days, 80 years to days, DOB 29-07-1984 age in days, or 2 weeks in hours. Exact calendar totals need a start date.</p>'
            '<button class="@B@" type="submit">Calculate Answer</button></form>'
            '<div id="qt-result" class="@R@" role="status" aria-live="polite">Enter a supported question and tap Calculate Answer.</div>'
        ),
        "guide": [
            ("What this calculator can answer", [
                "This is a deterministic, browser-based parser for a defined set of everyday time, date and arithmetic questions. It can convert common time units, convert months and years, estimate months as an average number of days, calculate Gregorian age from a birth date through today's local date, and solve clearly worded addition or subtraction questions.",
                "It also recognizes the fixed Pakistan independence date query and returns 14 August 1947 from the National Assembly of Pakistan historical reference. It is not a general search engine or an AI chatbot: it does not look up arbitrary facts, fetch live information, solve complex equations, or fill in missing dates by guesswork. If a question does not match a supported pattern, simplify the wording or use the dedicated calculator for that task."
            ]),
            ("Conversion rules and assumptions", [
                "A year contains 12 calendar months. For conversions between years and fixed time units, this calculator uses the mean Gregorian year of 365.2425 days. Therefore 80 years ≈ 29,219.4 days, and 1 year = 8,765.82 hours. These are average-unit conversions, not counts for a particular start and end date.",
                "A month does not have one fixed number of calendar days. When a question asks for months in days, the calculator uses the Gregorian average of 30.436875 days per month. For example, 115 months = 9 years and 7 months, or about 3,500.24 average days. For a date-specific result, exact calendar days require a start date and end date.",
                "Smaller fixed units use 1 week = 7 days, 1 day = 24 hours, 1 hour = 60 minutes and 1 minute = 60 seconds. For example, 2 weeks = 336 hours and 3 days = 4,320 minutes. The same factors are used in reverse conversions."
            ]),
            ("Date of birth and Gregorian age", [
                "Enter a valid date of birth in DD-MM-YYYY, DD/MM/YYYY or ISO YYYY-MM-DD format. Some English month-name formats are also recognized. The calculator counts actual Gregorian days from the birth date through the current local date on your device, then reports completed calendar years, months and remaining days.",
                "Invalid dates and birth dates in the future are rejected. The tool uses today's date from your device and does not provide a separate field for choosing a historical or future reference date. It calculates Gregorian age, not Hijri age or a legal age ruling for a particular jurisdiction."
            ]),
            ("Simple arithmetic and language input", [
                "The parser supports clearly expressed addition and subtraction, including common wording such as amounts added, distributed, stolen or remaining. For example, 99 − 29 − 19 = 51. It does not parse arbitrary algebra, nested expressions or every possible sentence.",
                "Defined number words, units and arithmetic terms are recognized in English, Roman Urdu, Urdu, Hindi, Arabic, Spanish and French. This is limited vocabulary and pattern recognition, not full translation or unrestricted speech understanding. Different spellings and dialects may not be recognized."
            ]),
            ("Limits and checking an answer", [
                "Use a date-based calculator when you need the exact number of calendar days between two dates, because month lengths and leap days vary. The average month and mean-year conversions on this page are estimates for unit conversion, not substitutes for a specific calendar interval.",
                "To check a fixed-unit result, reverse the conversion. For 4,320 minutes, divide by 60 to get 72 hours, then divide by 24 to get 3 days. A correct reverse calculation should return the starting quantity, subject to the displayed rounding."
            ])
        ],
        "faq": [
            ("How many days are in 80 years?", "This calculator uses the mean Gregorian year of 365.2425 days. Therefore 80 years ≈ 29,219.4 days. A simple 365-day multiplication gives 29,200, but that is not the method used for this calculator's year-to-day conversion."),
            ("Can I convert months to years and days?", "Yes. 115 months is 9 years and 7 months because 12 months make one year. Its average day equivalent is about 3,500.24 days using 30.436875 days per month. Exact calendar days need the actual dates."),
            ("Can I calculate age from a birth date?", "Yes. Enter a valid Gregorian date of birth. The calculator reports elapsed days and completed years, months and days through today's local date on your device. You cannot select a separate reference date on this page."),
            ("Which languages can I use?", "The parser recognizes defined terms and number forms in English, Roman Urdu, Urdu, Hindi, Arabic, Spanish and French. It does not understand every sentence, spelling or dialect."),
            ("Does this calculator answer any question?", "No. It supports specified time-unit conversions, month and year conversions, Gregorian birth-date age, simple addition and subtraction, and a fixed Pakistan Independence Day date lookup. It is not a general-purpose search engine or AI question-answering service.")
        ],
        "sources": "Fixed units: 1 week = 7 days, 1 day = 24 hours, 1 hour = 60 minutes and 1 minute = 60 seconds. Mean Gregorian year: 365.2425 days over the 400-year calendar cycle; see the <a class=\"" + LINK + "\" href=\"https://aa.usno.navy.mil/faq/leap_years\" target=\"_blank\" rel=\"noopener noreferrer\">U.S. Naval Observatory leap-year guidance</a>. Pakistan date: National Assembly of Pakistan, Parliamentary History, https://na.gov.pk/en/content.php?id=75."
    }
])
EXTRA.update({
    "years-to-days-calculator": {"faq": [], "quick": ""},
    "query-calculator": {"faq": [], "quick": "Year conversions use the 365.2425-day mean Gregorian year. Month-to-day conversions use 30.436875 average days per month; exact calendar totals need actual dates."},
})

TOOLS.append({
    "slug": "calorie-calculator",
    "category": "health",
    "name": "Adult Calorie Calculator",
    "app": "HealthApplication",
    "description": "Estimate adult maintenance calories using the Mifflin–St Jeor resting-energy equation and a clearly stated consumer activity assumption. Results are estimates, not medical advice.",
    "h1": "Adult Calorie Calculator",
    "lead": "Estimate adult daily maintenance calories from resting energy expenditure and an explicit activity assumption.",
    "guide": [],
    "sources": "",
})
for _t in TOOLS:
    _t["guide"] = _t["guide"] + GUIDE_EXTRA.get(_t["slug"], [])
    _t["sources"] = _t["sources"] + " " + REVIEW_STATUS.get(_t["slug"], "")
    if _t["slug"] == "standard-calculator":
        _t["ui"] = CALC_UI
        _t["guide"] += [
            ("How to use the online standard and scientific calculator", [
                "CalculatesAll is a free online calculator for everyday arithmetic and more advanced scientific calculations. Use the standard keypad for addition, subtraction, multiplication, division, percentages and brackets. Select Scientific Mode when you need trigonometry, powers, roots, logarithms, factorials, combinations or permutations. The calculator works in a modern browser on desktop and mobile, with large, touch-friendly keys.",
                "Enter an expression in the same order you would write it on paper. Brackets are evaluated first, then powers, multiplication and division, and finally addition and subtraction. For example, 2 + 3 × 4 equals 14 because multiplication takes priority. Use parentheses in (2 + 3) × 4 to make the result 20. Press clear to start again, or use backspace to remove the last character.",
            ]),
            ("Scientific calculator functions and angle modes", [
                "Scientific Mode includes sine, cosine and tangent, inverse trigonometric functions, square roots, powers, constants such as pi and e, logarithms, factorials, combinations and permutations. Choose DEG when an angle is expressed in degrees, such as sin(30), which equals 0.5. Choose RAD when an angle is expressed in radians, such as sin(pi/2), which equals 1. Using the wrong angle mode is a common reason a trigonometry answer looks incorrect.",
                "The calculator also provides an answer memory and basic memory controls to help with multi-step calculations. Check the displayed expression before pressing equals, especially when using negative exponents, nested brackets or logarithms with a custom base. Some inputs have no real-number result, such as dividing by zero or taking a square root of a negative number, so invalid operations should be corrected rather than treated as a numeric answer.",
            ]),
            ("Who can use this free online calculator", [
                "Students can check arithmetic and practise algebra or trigonometry. Teachers and tutors can demonstrate order of operations, powers and angle conversion. Households can work out percentages, discounts and everyday totals, while office users can verify figures before entering them into a spreadsheet. These examples describe common uses, not a guarantee that a result is suitable for every professional task.",
                "CalculatesAll performs calculations in the browser and is designed for quick access without installing an app. It is a practical calculation aid, not a substitute for independently checking high-stakes engineering, financial, medical or scientific work. For important results, verify the formula, units, rounding and assumptions with an authoritative source or qualified professional. If an answer seems unexpected, split the expression into smaller steps and compare the intermediate values.",
            ]),
        ]


def home_extra_html(lang):
    block = HOME_EXTRA[lang]
    out = '<h2 class="' + H2 + '">' + block["heading"] + "</h2>"
    for p in block["paragraphs"]:
        out += '<p class="' + P + '">' + p + "</p>"
    contact_email = html.escape(CONTACT_EMAIL, quote=True)
    if lang == "ur":
        contact_copy = "حساب میں ممکنہ خرابی رپورٹ کرنے کے لیے صفحے کا نام، درج کردہ اعداد اور متوقع نتیجہ شامل کرکے " + '<a class="' + LINK + '" href="mailto:' + contact_email + '">' + html.escape(CONTACT_EMAIL) + '</a>' + " پر ای میل کریں۔"
    else:
        contact_copy = "Found a possible calculation error? Email " + '<a class="' + LINK + '" href="mailto:' + contact_email + '">' + html.escape(CONTACT_EMAIL) + '</a>' + " with the page name, input values and expected result so the issue can be reproduced."
    out += '<p class="' + P + '">' + contact_copy + "</p>"
    heading = "سوالات" if lang == "ur" else "Frequently asked questions: Are these calculators free, private, and reliable?"
    answer_first = (
        "جی ہاں۔ CalculatesAll کے ٹولز مفت ہیں، حساب آپ کے براؤزر میں ہوتا ہے اور درج کردہ اعداد ہمارے سرور کو نہیں بھیجے جاتے۔ ہر کیلکولیٹر اپنا فارمولا اور حدود بتاتا ہے۔ اہم مالی، طبی یا دینی فیصلے کے لیے متعلقہ ماہر سے تصدیق کریں۔"
        if lang == "ur" else
        "Yes. CalculatesAll tools are free, calculations run in your browser, and calculator entries are not sent to our server. Each tool explains its formula and limits. Confirm important financial, medical or religious decisions with a qualified professional."
    )
    out += '<h2 class="' + H2 + '">' + heading + '</h2><p class="' + P + '">' + answer_first + '</p><div class="mt-3">' + faq_html(block["faq"]) + "</div>"
    if lang == "en":
        out += '<p class="' + P + '">Choose a tool for the task at hand. The <a class="' + LINK + '" href="/profit-loss-calculator/">Profit and Loss Calculator</a> separates product markup from gross margin, the <a class="' + LINK + '" href="/years-to-days-calculator/">Years to Days Calculator</a> distinguishes fixed-year and calendar-date methods, and the <a class="' + LINK + '" href="/tasbih-counter/">Tasbih Counter</a> keeps its count on your device.</p>'
        out += '<p class="' + P + '">CalculatesAll is a free online calculator project independently maintained by Muhammad Fayyaz Adeel. ' + SITE_DESCRIPTION + ' <a class="' + LINK + '" href="/about/">About the maintainer</a>.</p>'
        out += '<section aria-labelledby="how-it-works" class="mt-8"><h2 id="how-it-works" class="' + H2 + '">How it works</h2><ol class="mt-3 list-decimal pl-6 space-y-2 text-base leading-relaxed text-stone-800 dark:text-stone-200"><li>Choose a calculator for the task you want to complete.</li><li>Enter your values and select the units or options the tool requests.</li><li>Review the result and formula, including the worked example and stated limitations, before relying on it.</li></ol><p class="' + P + '">No account or download is required. Calculator entries are processed in your browser and are not sent to our server.</p></section>'
        out += '<p class="' + P + '"><a class="inline-flex min-h-[44px] items-center justify-center rounded-lg bg-sky-700 px-5 py-3 font-semibold text-white hover:bg-sky-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800" href="#all-tools">Browse all free calculators</a></p>'
    return out


URDU.update(URDU_EXTRA)


def review_box(slug):
    rv = REVIEWERS.get(slug)
    if not rv:
        return ""
    return ('<aside class="mt-10 rounded-xl bg-white border border-stone-300 p-5 text-base text-stone-900" aria-label="Reviewer">'
            '<p class="font-semibold">Reviewed by ' + rv["name"] + "</p>"
            '<p class="mt-1 text-stone-800">' + rv["credentials"] + "</p>"
            '<p class="mt-2 text-stone-800">' + rv["bio"] + "</p>"
            '<p class="mt-2 text-sm text-stone-800">Review date: ' + rv["review_date"] + ". " + rv.get("scope", "") + "</p></aside>")


def reviewer_schema(slug):
    rv = REVIEWERS.get(slug)
    if not rv:
        return None
    return {"@context": "https://schema.org", "@type": "Person", "name": rv["name"],
            "jobTitle": rv["credentials"], "description": rv["bio"], "url": SITE_URL + "/editorial-policy/"}


def write_ads_txt():
    # Do not publish a fake publisher ID. Google AdSense supplies the real ID
    # after account approval; until then, no ads.txt file should be generated.
    import re

    client = os.environ.get("ADSENSE_CLIENT", ADSENSE_CLIENT).strip()
    ads_path = os.path.join(OUT, "ads.txt")
    if not client:
        if os.path.exists(ads_path):
            os.remove(ads_path)
        return False
    if not re.fullmatch(r"ca-pub-\d{16}", client):
        raise SystemExit("ADSENSE_CLIENT must be a real-format ID like ca-pub-1234567890123456")
    pub = "pub-" + client[len("ca-pub-"):]
    with open(ads_path, "w", encoding="utf-8") as f:
        f.write("google.com, " + pub + ", DIRECT, f08c47fec0942fa0\n")
    return True


def write_review_sheet():
    import csv
    os.makedirs("review", exist_ok=True)
    rows = []
    for code in ["ar", "hi", "es", "fr"]:
        for key, val in UI[code].items():
            if isinstance(val, str):
                rows.append((code, key, val))
            elif isinstance(val, dict):
                for k2, v2 in val.items():
                    rows.append((code, key + "." + k2, v2))
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    if isinstance(item, str):
                        rows.append((code, key + "." + str(i), item))
                    else:
                        for j, part in enumerate(item):
                            rows.append((code, key + "." + str(i) + "." + str(j), part))
    for code in ["ur"]:
        for slug, u in URDU.items():
            for key in ("name", "title", "description", "h1", "lead"):
                rows.append((code, slug + "." + key, u[key]))
            for i, p in enumerate(u["how"]):
                rows.append((code, slug + ".how." + str(i), p))
            for i, (q, a) in enumerate(u["faq"]):
                rows.append((code, slug + ".faq." + str(i), q + " | " + a))
    with open("review/translations_review.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["language", "key", "text", "reviewer_status", "reviewer_correction", "reviewer_name"])
        for row in rows:
            w.writerow([row[0], row[1], row[2], "", "", ""])
    return len(rows)


def ad_slot():
    # Fail closed until valid IDs and account-side consent setup are confirmed.
    # ADSENSE_CONSENT_READY is a manual deployment safeguard, not CMP verification.
    if not ADSENSE_CLIENT or not ADSENSE_SLOT or not ADSENSE_CONSENT_READY:
        return ""
    return ('<div class="my-10 min-h-[100px]" aria-label="Advertisement">'
            '<ins class="adsbygoogle" style="display:block" data-ad-client="' + ADSENSE_CLIENT + '" '
            'data-ad-slot="' + ADSENSE_SLOT + '" data-ad-format="auto" data-full-width-responsive="true"></ins></div>')


def nav_items(lang="en"):
    items = ""
    for t in TOOLS:
        if lang == "ur":
            if t["slug"] not in URDU:
                continue
            name = URDU[t["slug"]]["name"]
            href = "/ur/" + t["slug"]
        elif lang in UI:
            name = UI[lang].get("tools", {}).get(t["slug"], t["name"])
            href = "/" + t["slug"]
        else:
            name = t["name"]
            href = "/" + t["slug"]
        items += '<li><a class="' + LINK + '" href="' + href + '"' + (' hreflang="en"' if lang not in ("en", "ur") else "") + '>' + name + "</a></li>"

    # EMI is a standalone calculator rather than an entry in TOOLS, so add it
    # explicitly to the shared menu to keep navigation complete without
    # changing the generated calculator-page pipeline.
    emi_names = {
        "en": "EMI Calculator",
        "ur": "ای ایم آئی کیلکولیٹر",
        "ar": "حاسبة الأقساط",
        "hi": "ईएमआई कैलकुलेटर",
        "es": "Calculadora de EMI",
        "fr": "Calculateur EMI",
    }
    emi_name = emi_names.get(lang, "EMI Calculator")
    items += '<li><a class="' + LINK + '" href="/emi-calculator/"' + (' hreflang="en"' if lang not in ("en", "ur") else "") + '>' + emi_name + "</a></li>"
    return items




CAROUSEL_TOOLS = (
    ("calorie-calculator", "Adult Calorie Calculator", "Cal"),
    ("zakat-calculator", "Zakat Calculator", "Zakat"),
    ("bmi-calculator", "BMI Calculator", "BMI"),
    ("profit-loss-calculator", "Profit and Loss Calculator", "P/L"),
    ("discount-calculator", "Discount Calculator", "Disc"),
    ("age-calculator", "Age Calculator", "Age"),
    ("unit-converter", "Unit Converter", "Units"),
    ("standard-calculator", "Standard and Scientific Calculator", "Std"),
    ("tasbih-counter", "Tasbih Counter", "Tasbih"),
    ("stopwatch", "Online Stopwatch", "Timer"),
    ("years-to-days-calculator", "Years to Days Calculator", "Y→D"),
    ("query-calculator", "Query Calculator", "Query"),
    ("emi-calculator", "EMI Calculator", "EMI"),
    ("percentage-calculator", "Percentage Calculator", "%"),
    ("fraction-calculator", "Fraction Calculator", "Frac"),
    ("compound-interest-calculator", "Compound Interest Calculator", "CI"),
    ("date-calculator", "Date Difference Calculator", "Date"),
)

CAROUSEL_TRANSLATIONS = {
    "ur": {
        "zakat-calculator": "زکوٰۃ کیلکولیٹر", "bmi-calculator": "بی ایم آئی کیلکولیٹر",
        "profit-loss-calculator": "منافع اور نقصان کیلکولیٹر", "discount-calculator": "ڈسکاؤنٹ کیلکولیٹر",
        "age-calculator": "عمر کیلکولیٹر", "unit-converter": "یونٹ کنورٹر",
        "standard-calculator": "معیاری اور سائنسی کیلکولیٹر", "tasbih-counter": "تسبیح کاؤنٹر",
        "stopwatch": "آن لائن اسٹاپ واچ", "years-to-days-calculator": "سال سے دن کیلکولیٹر",
        "query-calculator": "کوئری کیلکولیٹر", "emi-calculator": "قسط کیلکولیٹر",
        "percentage-calculator": "فیصد کیلکولیٹر", "fraction-calculator": "کسر کیلکولیٹر",
        "compound-interest-calculator": "مرکب سود کیلکولیٹر", "date-calculator": "تاریخوں کا فرق کیلکولیٹر",
        "calorie-calculator": "بالغ افراد کا کیلوری کیلکولیٹر",
    },
    "ar": {
        "years-to-days-calculator": "حاسبة تحويل السنوات إلى أيام", "query-calculator": "حاسبة الاستعلام",
        "emi-calculator": "حاسبة الأقساط", "percentage-calculator": "حاسبة النسبة المئوية",
        "fraction-calculator": "حاسبة الكسور", "compound-interest-calculator": "حاسبة الفائدة المركبة",
        "date-calculator": "حاسبة الفرق بين التواريخ",
        "calorie-calculator": "حاسبة السعرات الحرارية للبالغين",
    },
    "hi": {
        "years-to-days-calculator": "वर्ष से दिन कैलकुलेटर", "query-calculator": "क्वेरी कैलकुलेटर",
        "emi-calculator": "ईएमआई कैलकुलेटर", "percentage-calculator": "प्रतिशत कैलकुलेटर",
        "fraction-calculator": "भिन्न कैलकुलेटर", "compound-interest-calculator": "चक्रवृद्धि ब्याज कैलकुलेटर",
        "date-calculator": "तिथि अंतर कैलकुलेटर",
        "calorie-calculator": "वयस्क कैलोरी कैलकुलेटर",
    },
    "es": {
        "years-to-days-calculator": "Calculadora de años a días", "query-calculator": "Calculadora de consultas",
        "emi-calculator": "Calculadora de EMI", "percentage-calculator": "Calculadora de porcentajes",
        "fraction-calculator": "Calculadora de fracciones", "compound-interest-calculator": "Calculadora de interés compuesto",
        "date-calculator": "Calculadora de diferencia de fechas",
        "calorie-calculator": "Calculadora de calorías para adultos",
    },
    "fr": {
        "years-to-days-calculator": "Calculatrice années en jours", "query-calculator": "Calculatrice de requêtes",
        "emi-calculator": "Calculatrice EMI", "percentage-calculator": "Calculatrice de pourcentage",
        "fraction-calculator": "Calculatrice de fractions", "compound-interest-calculator": "Calculatrice d’intérêts composés",
        "date-calculator": "Calculatrice de différence de dates",
        "calorie-calculator": "Calculateur de calories pour adultes",
    },
}

CAROUSEL_SHORT_UR = {
    "calorie-calculator": "کیلوری", "zakat-calculator": "زکوٰۃ", "bmi-calculator": "BMI",
    "profit-loss-calculator": "نفع", "discount-calculator": "ڈسک",
    "age-calculator": "عمر", "unit-converter": "اکائی",
    "standard-calculator": "حساب", "tasbih-counter": "تسبیح",
    "stopwatch": "وقت", "years-to-days-calculator": "سال",
    "query-calculator": "سوال", "emi-calculator": "EMI",
    "percentage-calculator": "%", "fraction-calculator": "کسر",
    "compound-interest-calculator": "سود", "date-calculator": "تاریخ",
}


def calculator_carousel(lang="en", current_path=None):
    s = shell_strings(lang)
    groups = []
    groups_to_render = (("primary", False), ("duplicate", True)) if current_path in ("/", "/ur/", "/ar/", "/hi/", "/es/", "/fr/", "/zakat-calculator/", "/ur/zakat-calculator/") else (("primary", False),)
    for group_name, duplicate in groups_to_render:
        links = []
        tools_to_render = CAROUSEL_TOOLS
        if current_path in ("/zakat-calculator/", "/ur/zakat-calculator/"):
            tools_to_render = sorted(CAROUSEL_TOOLS, key=lambda item: item[0] != "zakat-calculator")
        for slug, english_name, short_name in tools_to_render:
            if lang == "ur":
                name = CAROUSEL_TRANSLATIONS["ur"][slug]
                href = ("/ur/" if slug in URDU else "/") + slug + "/"
            elif lang in UI:
                name = UI[lang].get("tools", {}).get(slug) or CAROUSEL_TRANSLATIONS.get(lang, {}).get(slug) or english_name
                href = "/" + slug + "/"
            else:
                name = english_name
                href = "/" + slug + "/"
            active = ' aria-current="page"' if not duplicate and current_path == href else ""
            tabindex = ' tabindex="-1"' if duplicate else ""
            short_label = CAROUSEL_SHORT_UR.get(slug, short_name) if lang == "ur" else short_name
            links.append(
                '<a class="ca-calculator-link" data-tool-shortcut="' + slug
                + '" data-short-label="' + html.escape(short_label, quote=True)
                + '" href="' + href + '" aria-label="' + html.escape(name, quote=True)
                + '" title="' + html.escape(name, quote=True) + '"' + active + tabindex + '>'
                + html.escape(name) + '</a>'
            )
        hidden = ' aria-hidden="true"' if duplicate else ""
        groups.append(
            '<div class="ca-calculator-group" data-tool-set="' + group_name + '"' + hidden + '>'
            + "".join(links) + '</div>'
        )
    return (
        '<div class="ca-calculator-carousel" role="region" aria-label="' + s["calculators"] + '">'
        '<div class="ca-calculator-track">' + "".join(groups) + '</div></div>'
    )


LANG_LOCALE = {"en": "en_US", "ur": "ur_PK", "ar": "ar_AR", "hi": "hi_IN", "es": "es_ES", "fr": "fr_FR"}
RTL_LANGS = ("ur", "ar")
SHELL_EN = {"menu": "All tools", "skip": "Skip to content", "about": "About", "privacy": "Privacy", "contact": "Contact",
            "methodology": "Methodology", "editorial": "Editorial policy", "tag": "© CalculatesAll. Free tools that run in your browser.",
            "theme": "Dark mode", "calculators": "Calculator shortcuts", "lang": "Languages", "terms": "Terms of use", "main": "Main", "footer": "Footer", "affiliate": "Advertising disclosure", "confidence": "CALCULATE WITH CONFIDENCE", "many": "ONE PLACE, MANY ANSWERS", "free": "FREE", "discount": "Discount Calculator", "health_link": "Health"}
SHELL_UR = {"menu": "تمام ٹولز", "skip": "مرکزی مواد پر جائیں", "about": "ہمارے بارے میں", "privacy": "رازداری", "contact": "رابطہ",
            "methodology": "طریقہ کار", "editorial": "ادارتی پالیسی", "tag": "© CalculatesAll۔ مفت ٹولز جو آپ کے براؤزر میں چلتے ہیں۔",
            "theme": "ڈارک موڈ", "calculators": "کیلکولیٹر منتخب کریں", "lang": "زبانیں", "terms": "شرائط استعمال", "main": "مرکزی نیویگیشن", "footer": "فٹر", "affiliate": "افیلی ایٹ انکشاف", "confidence": "اعتماد کے ساتھ حساب کریں", "many": "ایک جگہ، کئی جواب", "free": "مفت", "discount": "ڈسکاؤنٹ کیلکولیٹر", "health_link": "صحت"}
THEME_LABEL = {"ar": "الوضع الداكن", "hi": "डार्क मोड", "es": "Modo oscuro", "fr": "Mode sombre"}


def shell_strings(lang):
    if lang == "en":
        return SHELL_EN
    if lang == "ur":
        return SHELL_UR
    merged = dict(SHELL_EN)
    merged.update(UI[lang])
    merged["theme"] = THEME_LABEL[lang]
    merged["lang"] = {"ar": "اللغات", "hi": "भाषाएँ", "es": "Idiomas", "fr": "Langues"}[lang]
    merged["discount"] = UI[lang]["tools"]["discount-calculator"]
    merged["health_link"] = UI[lang]["cats"]["health"]
    merged["calculators"] = {"ar": "اختصارات الحاسبات", "hi": "कैलकुलेटर शॉर्टकट", "es": "Accesos a calculadoras", "fr": "Raccourcis calculatrice"}[lang]
    return merged


def home_alts_all():
    return [(l["code"], l["path"]) for l in LANGS] + [("x-default", "/")]


def head(title, desc, path, schema, lang="en", noindex=False, alternates=None):
    url = SITE_URL + path
    # Keep one canonical, linked identity graph on every public page.
    # Merge page-level declarations rather than duplicating the homepage Organization/WebSite nodes.
    if path != "/404":
        schema = list(schema or [])
        shared_entities = [
            {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website",
             "name": "CalculatesAll", "url": SITE_URL + "/", "description": SITE_DESCRIPTION,
             "publisher": {"@id": SITE_URL + "/#organization"}},
            {"@context": "https://schema.org", "@type": "Organization", "@id": SITE_URL + "/#organization",
             "name": "CalculatesAll", "url": SITE_URL + "/", "description": SITE_DESCRIPTION,
             "sameAs": ["https://github.com/Beastmalik7424/calculatesallinone"],
             "logo": SITE_URL + "/assets/favicon.svg",
             "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "url": SITE_URL + "/contact/"}},
            {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/#maintainer",
             "name": "Muhammad Fayyaz Adeel", "alternateName": ["Malik Adeel Bhatti"],
             "description": "Maintainer of the CalculatesAll online calculator project.",
             "url": SITE_URL + "/about/", "sameAs": ["https://github.com/Beastmalik7424"],
             "affiliation": {"@id": SITE_URL + "/#organization"}},
        ]
        for entity in shared_entities:
            existing = next((item for item in schema
                             if item.get("@id") == entity["@id"]
                             or (item.get("@type") == entity["@type"]
                                 and item.get("name") == entity["name"]
                                 and item.get("url", SITE_URL + "/") == entity["url"])), None)
            if existing is None:
                schema.append(entity)
            else:
                existing["@context"] = "https://schema.org"
                existing["@type"] = entity["@type"]
                existing["@id"] = entity["@id"]
                for key, value in entity.items():
                    if key not in ("@context", "@type", "@id"):
                        existing[key] = value
    robots = "noindex, follow" if noindex else "index, follow"
    alt = ""
    if alternates:
        for code, href in alternates:
            alt += '<link rel="alternate" hreflang="' + code + '" href="' + SITE_URL + href + '">\n'
    ads = ""
    # Use AdSense's lightweight ownership meta tag while ads are disabled.
    # Download the ad library only when a real slot and the consent gate are enabled.
    verification = ""
    if ADSENSE_CLIENT:
        verification = '<meta name="google-adsense-account" content="' + html.escape(ADSENSE_CLIENT, quote=True) + '">\n'
    if ADSENSE_CLIENT and ADSENSE_SLOT and ADSENSE_CONSENT_READY:
        ads = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
               + ADSENSE_CLIENT + '" crossorigin="anonymous"></script>\n')
    ld = ""
    for s in schema:
        # Add page language only to schema types that support inLanguage.
        # This keeps structured data consistent with the actual HTML language.
        if s.get("@type") in ("WebSite", "WebPage", "ProfilePage", "CollectionPage", "WebApplication"):
            s.setdefault("inLanguage", lang)
        ld += '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>\n"
    og_image = SITE_URL + "/assets/og-image.png"
    dir_attr = ' dir="rtl"' if lang in RTL_LANGS else ' dir="ltr"'
    locale = LANG_LOCALE.get(lang, "en_US")
    theme_script = (
        "<script>\n(function () {\ntry {\nvar s = localStorage.getItem(\"theme\")\n"
        "if (s === \"dark\") document.documentElement.classList.add(\"dark\")\n"
        "} catch (e) {\nreturn\n}\n})()\n</script>\n"
    )
    return (
        '<!DOCTYPE html>\n<html lang="' + lang + '"' + dir_attr + '>\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
        '<title>' + title + '</title>\n'
        '<meta name="description" content="' + desc + '">\n'
        '<meta name="robots" content="' + robots + '">\n'
        + ('' if path == "/404" else '<link rel="canonical" href="' + url + '">\n')
        + alt
        + '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:site_name" content="CalculatesAll">\n'
        '<meta property="og:locale" content="' + locale + '">\n'
        '<meta property="og:title" content="' + title + '">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:url" content="' + url + '">\n'
        '<meta property="og:image" content="' + og_image + '">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="' + title + '">\n'
        '<meta name="twitter:description" content="' + desc + '">\n'
        '<meta name="twitter:image" content="' + og_image + '">\n'
        '<meta name="google-site-verification" content="DnTlrPscc56w3Xe-QHyaXhObsePjw4y_G-5i5qQl_wY">\n'
        + verification
        + '<meta name="theme-color" content="#f0f9ff">\n'
        + theme_script
        + '<link rel="stylesheet" href="/assets/site.css?v=' + CSS_ASSET_VERSION + '">\n'
        + ld + ads + "</head>\n"
    )


def lang_links(lang, s, current_path=None):
    # Calculator language links preserve the current tool and only show
    # locales for which an equivalent translated page exists.
    import re
    match = re.fullmatch(r"/(?:ur/)?([^/]+)/", current_path or "")
    if match and match.group(1) in {t["slug"] for t in TOOLS}:
        slug = match.group(1)
        if slug not in URDU:
            return ""
        choices = [
            ("en", "English", "/" + slug + "/"),
            ("ur", "اردو", "/ur/" + slug + "/"),
        ]
        items = ""
        for code, name, href in choices:
            if code == lang:
                continue
            items += ('<li><a class="' + LINK + ' min-h-[44px] inline-flex items-center rounded-full px-3 py-1 bg-white/80 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700" hreflang="' + code
                      + '" href="' + href + '">' + name + "</a></li>")
        return ('<nav aria-label="' + s["lang"] + '" class="mt-3"><ul class="flex flex-wrap gap-x-3 gap-y-2 text-sm">'
                + items + "</ul></nav>")

    items = ""
    for l in LANGS:
        if l["code"] == lang:
            continue
        items += ('<li><a class="' + LINK + ' min-h-[44px] inline-flex items-center rounded-full px-3 py-1 bg-white/80 dark:bg-stone-800/80 border border-stone-200 dark:border-stone-700" hreflang="' + l["code"]
                  + '" href="' + l["path"] + '">' + l["name"] + "</a></li>")
    return ('<nav aria-label="' + s["lang"] + '" class="mt-3"><ul class="flex flex-wrap gap-x-3 gap-y-2 text-sm">'
            + items + "</ul></nav>")


FOOTER_EMI_LABEL = {"en": "EMI Calculator", "ur": "ای ایم آئی کیلکولیٹر", "ar": "حاسبة الأقساط", "hi": "ईएमआई कैलकुलेटर", "es": "Calculadora de EMI", "fr": "Calculateur EMI"}


def shell(main_html, lang="en", current_path=None):
    s = shell_strings(lang)
    home = "/"
    brand_home_label = {"en": " home page", "ur": " ہوم پیج", "ar": " الصفحة الرئيسية", "hi": " होम पेज", "es": " página de inicio", "fr": " page d’accueil"}.get(lang, " home page")
    main_width = "max-w-screen-2xl" if current_path in ("/", "/ur/", "/ar/", "/hi/", "/es/", "/fr/") else "max-w-3xl"
    menu_position = "left-0 right-auto" if lang in RTL_LANGS else "right-0"
    tool_paths = {"/" + t["slug"] + "/" for t in TOOLS if t["slug"] != "standard-calculator"}
    urdu_tool_paths = {"/ur/" + slug + "/" for slug in URDU if slug != "standard-calculator"}
    main_classes = main_width + " mx-auto px-5 py-10"
    if current_path in tool_paths | urdu_tool_paths:
        main_classes += " ca-tool-main"
    if current_path == "/calorie-calculator/":
        main_classes += " ca-tool-calorie-calculator"
    return (
        '<body class="min-h-screen bg-gradient-to-br from-slate-100 via-sky-50 to-teal-50 dark:from-slate-950 dark:via-slate-900 dark:to-teal-950 text-stone-900 dark:text-stone-100 antialiased">\n'
        '<div aria-hidden="true" class="pointer-events-none fixed inset-0 -z-10 overflow-hidden">'
        '<div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-violet-300/30 blur-3xl"></div>'
        '<div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full bg-sky-300/35 blur-3xl"></div>'
        '<div class="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-teal-300/30 blur-3xl"></div></div>\n'
        '<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:bg-white focus:px-3 focus:py-2 focus:rounded">' + s["skip"] + '</a>\n'
        '<div class="h-1.5 bg-gradient-to-r from-teal-500 via-sky-500 to-indigo-500"></div>'
        '<header class="sticky top-0 z-20 bg-white/80 dark:bg-stone-900/80 backdrop-blur border-b border-stone-200 dark:border-stone-700 shadow-sm">'
        '<nav class="ca-site-nav max-w-screen-2xl mx-auto w-full px-4 py-2 flex flex-col items-stretch gap-2" aria-label="' + s["main"] + '">'
        '<div class="ca-site-nav-topline flex w-full items-center justify-between gap-3" dir="ltr">'
        '<a href="' + home + '" aria-label="CalculatesAll' + brand_home_label + '" class="font-extrabold text-xl text-slate-900 dark:text-white min-h-[44px] inline-flex items-center gap-2"><span aria-hidden="true" class="inline-block h-3 w-3 rounded-sm bg-gradient-to-br from-teal-500 to-indigo-600"></span>CalculatesAll<span class="sr-only">' + brand_home_label + '</span></a>'
        '<button id="theme-toggle" type="button" class="' + S + ' min-h-[44px] shrink-0">' + s["theme"] + '</button>'
        '</div>'
        + calculator_carousel(lang, current_path)
        + '</nav></header>\n'
        '<main id="main" class="' + main_classes + '">' + main_html + '</main>\n'
        '<footer class="mt-12 bg-white/80 dark:bg-stone-900/80 backdrop-blur border-t border-stone-200 dark:border-stone-700">'
        '<div class="max-w-5xl mx-auto px-5 py-8 flex flex-col gap-4 text-sm text-stone-800">'
        '<div class="flex flex-col sm:flex-row gap-4 sm:items-center sm:justify-between">'
        '<p>' + s["tag"] + '</p>'
        '<nav class="flex flex-wrap gap-5" aria-label="' + s["footer"] + '">'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/about/">' + s["about"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/emi-calculator/">' + (FOOTER_EMI_LABEL["ur"] if lang == "ur" else "EMI Calculator") + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/privacy/">' + s["privacy"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/contact/">' + s["contact"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/discount-calculator/">' + s["discount"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/health/">' + s["health_link"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/methodology/">' + s["methodology"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/editorial-policy/">' + s["editorial"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/terms/">' + s["terms"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/affiliate-disclosure/">' + s["affiliate"] + '</a>'
        '</nav></div>'
        + lang_links(lang, s, current_path) +
        '<div class="mt-4"><a href="https://fazier.com" target="_blank" rel="noopener"><img src="https://fazier.com/api/v1//public/badges/launch_badges.svg?badge_type=launched&theme=light" width="120" alt="Fazier badge" loading="lazy"></a></div>\n' +
        '</div></footer>\n'
        '<script src="/assets/zakat-calculator.js?v=20261116-hanafi-jafari-1" defer></script>\n'
        '<script src="/assets/app.js?v=20261116-hanafi-jafari-1" defer></script>\n'
        '</body>\n</html>\n'
    )


def home_lang_page(code):
    u = UI[code]
    path = "/" + code + "/"
    cards = ""
    for c in CATEGORIES:
        cards += ('<li class="rounded-xl bg-white border border-stone-300 p-5">'
                  '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/' + c["slug"] + '/">' + u["cats"][c["slug"]] + "</a>"
                  '<p class="mt-2 text-base text-stone-800">' + u["cat_desc"][c["slug"]] + "</p></li>")
    extra = '<h2 class="' + H2 + '">' + u["heading"] + "</h2>"
    for p in u["paragraphs"]:
        extra += '<p class="' + P + '">' + p + "</p>"
    extra += '<h2 class="' + H2 + '">' + u["faq"] + '</h2><div class="mt-3">' + faq_html(u["faq_items"]) + "</div>"
    body = (
        '<h1 class="text-3xl font-semibold text-stone-900 mt-2">' + u["h1"] + '</h1>'
        '<p class="mt-4 text-lg text-stone-900">' + u["lead"] + '</p>'
        '<ul class="mt-10 grid gap-4">' + cards + "</ul>" + extra
    )
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website", "name": "CalculatesAll", "url": SITE_URL + "/", "inLanguage": code},
        {"@context": "https://schema.org", "@type": "Organization", "@id": SITE_URL + "/#organization", "name": "CalculatesAll", "url": SITE_URL + "/",
         "description": SITE_DESCRIPTION,
         "logo": SITE_URL + "/assets/favicon.svg",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "url": SITE_URL + "/contact/"}},
        {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/#maintainer", "name": "Muhammad Fayyaz Adeel", "url": SITE_URL + "/about/", "worksFor": {"@id": SITE_URL + "/#organization"}},
    ]
    write(path, head(u["title"], u["desc"], path, schema, lang=code, alternates=home_alts_all()) + shell(body, lang=code, current_path=path))
    return path



def fill(s):
    button_class = B_ZAKAT if 'id="zakat-form"' in s else B
    return s.replace("@L@", L).replace("@I@", I).replace("@B@", button_class).replace("@S@", S).replace("@R@", R)


def write(path, content):
    rel = path.strip("/")
    folder = os.path.join(OUT, rel) if rel else OUT
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(fill(content))


def years_to_days_reference_html():
    years_values = [1, 1.5, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 25, 29, 30, 32, 40, 50, 60, 74, 80, 100]
    quick_values = [2, 3, 5, 7, 9, 10, 13, 20]
    def formatted(value):
        return format(value, ",.5f").rstrip("0").rstrip(".")
    def table_rows(values):
        rows = ""
        for years in values:
            rows += ('<tr><th scope="row" class="border-b p-3">' + formatted(years) + '</th>'
                     '<td class="border-b p-3">' + formatted(years * 365) + '</td>'
                     '<td class="border-b p-3">' + formatted(years * 365.25) + '</td>'
                     '<td class="border-b p-3">' + formatted(years * 365.2425) + '</td></tr>')
        return rows
    table_start = ('<div class="mt-4 overflow-x-auto"><table class="w-full border-collapse text-left text-sm">'
                   '<caption class="sr-only">Years converted to days using 365-day, 365.25-day Julian and 365.2425-day Gregorian year lengths</caption>'
                   '<thead><tr><th scope="col" class="border-b p-3">Years</th><th scope="col" class="border-b p-3">365-day method</th><th scope="col" class="border-b p-3">Julian average (365.25)</th><th scope="col" class="border-b p-3">Gregorian average (365.2425)</th></tr></thead><tbody>')
    table_end = '</tbody></table></div>'
    out = ('<section class="mt-8"><h2 class="' + H2 + '">Quick reference: years to days</h2>'
           '<p class="' + P + '">A short comparison for common examples. Fixed-year methods are estimates; exact calendar totals depend on the start date.</p>'
           + table_start + table_rows(quick_values) + table_end
           + '<details id="years-days-full-reference" class="mt-4 rounded-lg border border-stone-300 dark:border-stone-700 p-4">'
           '<summary class="cursor-pointer font-medium min-h-[44px] flex items-center">Show all 29 years-to-days reference examples</summary>'
           + table_start + table_rows(years_values) + table_end
           + '</details><p class="' + P + '">For exact elapsed days between calendar dates, use Exact calendar years in the calculator above. The expanded table is a duration reference, not a substitute for a date-specific count.</p></section>')
    return out


def days_to_years_reference_html():
    day_counts = [724, 1068, 1145, 1188, 1297, 1476, 2436, 2600, 7200, 27375, 28000, 42069]
    out = ('<section class="mt-10"><h2 class="' + H2 + '">Worked reference: days to years</h2>'
           '<p class="' + P + '">Convert days to decimal years by dividing by 365, 365.25 or 365.2425. Values are rounded to four decimal places; these are duration estimates, not calendar ages.</p>'
           '<div class="mt-4 overflow-x-auto"><table class="w-full border-collapse text-left text-sm">'
           '<caption class="sr-only">Example day counts converted to decimal years using 365-day, Julian-average and Gregorian-average year lengths</caption>'
           '<thead><tr><th scope="col" class="border-b p-3">Days</th><th scope="col" class="border-b p-3">365-day year</th><th scope="col" class="border-b p-3">Julian average (365.25)</th><th scope="col" class="border-b p-3">Gregorian average (365.2425)</th></tr></thead><tbody>')
    for days in day_counts:
        simple = format(days / 365, ".4f")
        julian = format(days / 365.25, ".4f")
        average = format(days / 365.2425, ".4f")
        out += ('<tr><th scope="row" class="border-b p-3">' + format(days, ",") + '</th>'
                '<td class="border-b p-3">' + simple + '</td>'
                '<td class="border-b p-3">' + julian + '</td>'
                '<td class="border-b p-3">' + average + '</td></tr>')
    out += ('</tbody></table></div><p class="' + P + '">A decimal-year result does not identify the exact calendar age or elapsed years. For an exact interval, enter the actual start and end dates in the Date Difference Calculator.</p></section>')
    return out


def guide_html(sections):
    out = ""
    for heading, paras in sections:
        out += '<h2 class="' + H2 + '">' + heading + "</h2>"
        for p in paras:
            out += '<p class="' + P + '">' + p + "</p>"
    return out


def faq_html(items):
    out = ""
    for q, a in items:
        out += ('<details class="border-b border-stone-300 dark:border-stone-700 py-4">'
                '<summary class="cursor-pointer font-medium text-stone-900 dark:text-stone-100 min-h-[44px] flex items-center">' + q + "</summary>"
                '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + a + "</p></details>")
    return out


def canon_override(doc, path):
    # Each calculator page contains its own explanatory content and should
    # self-canonicalize. Do not point the standard calculator at the home page.
    return doc


ANSWER_BLOCKS = {
    "zakat-calculator": {
        "en": 'This calculator lets you compare silver and gold Nisab reference weights and formats the result in your selected ISO currency. It does not fetch live metal prices or issue a religious ruling. The Pakistan PKR 503,529 figure shown below is a separate, year-specific bank source-deduction threshold for 1446–1447 AH, not a universal personal Nisab. Sources: <a class="' + LINK + '" href="https://www.islamic-relief.org.uk/giving/islamic-giving/zakat/zakat-calculator/" rel="noopener noreferrer">Islamic Relief</a> and <a class="' + LINK + '" href="https://www.sbp.org.pk/circulars/bprd-circular-letter-no-03-of-2026" rel="noopener noreferrer">State Bank of Pakistan</a>.',
        "ur": 'یہ کیلکولیٹر چاندی اور سونے کے نصاب کے مختلف وزن منتخب کرنے اور نتیجہ منتخب کرنسی میں دکھانے کی سہولت دیتا ہے۔ یہ لائیو دھات کی قیمت حاصل نہیں کرتا اور نہ ہی شرعی فتویٰ دیتا ہے۔ پاکستان کی 503,529 روپے کی رقم 1446–1447 ہجری کے مخصوص بینک اکاؤنٹس کی سرکاری کٹوتی کی حد تھی، ہر شخص کا ذاتی نصاب نہیں۔ ماخذ: <a class="' + LINK + '" href="https://www.islamic-relief.org.uk/giving/islamic-giving/zakat/zakat-calculator/" rel="noopener noreferrer">اسلامک ریلیف</a> اور <a class="' + LINK + '" href="https://www.sbp.org.pk/circulars/bprd-circular-letter-no-03-of-2026" rel="noopener noreferrer">اسٹیٹ بینک آف پاکستان</a>۔'
    },
    "bmi-calculator": {
        "en": 'For adults, the CDC classifies a BMI from 25.0 to less than 30.0 as overweight; BMI is a screening measure, not a diagnosis. Source: <a class="' + LINK + '" href="https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html" target="_blank" rel="noopener noreferrer">CDC adult BMI categories</a>.',
        "ur": 'بالغ افراد میں CDC کے مطابق BMI کی 25.0 سے 30.0 سے کم حد کو زائد وزن کہا جاتا ہے؛ BMI صرف ابتدائی جانچ ہے، تشخیص نہیں۔ ماخذ: <a class="' + LINK + '" href="https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html" target="_blank" rel="noopener noreferrer">CDC کی بالغوں کے لیے BMI درجہ بندی</a>۔'
    },
    "profit-loss-calculator": {
        "en": 'Business example: revenue 1,000, cost of goods sold 600 and other expenses 150 gives net operating profit 250 and margin 25%. Product example: cost 1,000 and selling price 1,200 gives markup 20%. Source: <a class="' + LINK + '" href="/methodology/">CalculatesAll calculation methodology</a>.',
        "ur": ''
    },
    "discount-calculator": {
        "en": 'A 20% discount on a price of 1,000 saves 200 and leaves a final price of 800 before tax or extra charges. Source: <a class="' + LINK + '" href="/methodology/">CalculatesAll calculation methodology</a>.',
        "ur": '1,000 کی قیمت پر 20٪ رعایت سے 200 کی بچت ہوتی ہے اور ٹیکس یا اضافی فیس سے پہلے آخری قیمت 800 رہتی ہے۔ ماخذ: <a class="' + LINK + '" href="/methodology/">CalculatesAll کا حسابی طریقۂ کار</a>۔'
    },
    "age-calculator": {
        "en": 'A leap year has 366 calendar days, which is one reason age should be calculated from calendar dates rather than by dividing days by 365. Source: <a class="' + LINK + '" href="https://www.timeanddate.com/date/leapyear.html" target="_blank" rel="noopener noreferrer">timeanddate leap-year explanation</a>.',
        "ur": 'لیپ سال میں 366 دن ہوتے ہیں، اس لیے عمر کو صرف کل دنوں کو 365 پر تقسیم کر کے نکالنا درست نہیں۔ ماخذ: <a class="' + LINK + '" href="https://www.timeanddate.com/date/leapyear.html" target="_blank" rel="noopener noreferrer">لیپ سال کی وضاحت</a>۔'
    },
    "unit-converter": {
        "en": 'One international avoirdupois pound equals exactly 0.45359237 kilograms. Source: <a class="' + LINK + '" href="https://nvlpubs.nist.gov/nistpubs/hb/2026/NIST.HB.44-2026.pdf" target="_blank" rel="noopener noreferrer">NIST Handbook 44 (2026), Appendix C</a>.',
        "ur": 'ایک بین الاقوامی پاؤنڈ بالکل 0.45359237 کلوگرام کے برابر ہے۔ ماخذ: <a class="' + LINK + '" href="https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9" target="_blank" rel="noopener noreferrer">NIST کی اکائیوں کی تبدیلی کی جدول</a>۔'
    },
    "standard-calculator": {
        "en": 'Using the usual order of operations, 2 + 3 × 4 equals 14 because multiplication is evaluated before addition. Source: <a class="' + LINK + '" href="https://www.khanacademy.org/math/arithmetic/arith-review-negative-numbers/arith-review-order-of-operations/a/order-of-operations-review" target="_blank" rel="noopener noreferrer">Khan Academy order of operations</a>.',
        "ur": 'عام ترتیبِ عملیات کے مطابق 2 + 3 × 4 کا جواب 14 ہے، کیونکہ جمع سے پہلے ضرب کی جاتی ہے۔ ماخذ: <a class="' + LINK + '" href="https://www.khanacademy.org/math/arithmetic/arith-review-negative-numbers/arith-review-order-of-operations/a/order-of-operations-review" target="_blank" rel="noopener noreferrer">Khan Academy کی ترتیبِ عملیات</a>۔'
    },
    "tasbih-counter": {
        "en": 'Each tap adds exactly one to the count, so starting from zero, 33 taps show 33. The target, undo and reset controls never change a count without a tap or your confirmation.',
        "ur": 'ہر دبانے سے گنتی میں ٹھیک ایک کا اضافہ ہوتا ہے، اس لیے صفر سے شروع کر کے 33 بار دبانے پر گنتی 33 ہو گی۔'
    },
    "stopwatch": {
        "en": 'One second contains 1,000 milliseconds, the unit commonly used for sub-second timing displays. Source: <a class="' + LINK + '" href="https://www.nist.gov/pml/owm/metric-si/si-units" target="_blank" rel="noopener noreferrer">NIST SI units</a>.',
        "ur": 'ایک سیکنڈ میں 1,000 ملی سیکنڈ ہوتے ہیں، جو ایک سیکنڈ سے کم وقت دکھانے کے لیے استعمال ہوتے ہیں۔ ماخذ: <a class="' + LINK + '" href="https://www.nist.gov/pml/owm/metric-si/si-units" target="_blank" rel="noopener noreferrer">NIST کی SI اکائیاں</a>۔'
    }
}

def answer_block(slug, lang="en"):
    text = ANSWER_BLOCKS.get(slug, {}).get(lang)
    if not text:
        return ""
    label = "ماخذ پر مبنی وضاحت" if lang == "ur" else "Evidence-based note"
    return '<p class="mt-5 rounded-xl border border-sky-200 dark:border-sky-800 bg-sky-50 dark:bg-sky-950 p-4 text-base leading-relaxed"><strong>' + label + '.</strong> ' + text + '</p>'


BMI_GUIDE = [
    ("The formula", [
        "Weight can be entered in kilograms (kg) or pounds (lb), independently of the height unit. When kg is selected, adult BMI is calculated by dividing weight in kilograms by height in metres squared. When height is entered in centimetres, divide it by 100 first.",
        "For feet and inches, convert total height to centimetres with (feet × 12 + inches) × 2.54. If kg is selected, the calculator uses the metric formula. If lb is selected, BMI equals 703 multiplied by weight in pounds, divided by total height in inches squared.",
    ]),
    ("Adult BMI categories", [
        "For adults, the standard WHO categories are underweight below 18.5, normal weight from 18.5 to below 25, overweight from 25 to below 30, and obesity from 30 upward. This calculator assigns the category using the unrounded BMI and rounds only the displayed number to one decimal place. A displayed value of 25.0 can therefore remain in the normal weight category when the exact BMI is just below 25.",
        "These categories are population-level screening ranges. They do not determine whether an individual is healthy, and they should not be used as a personal diagnosis or treatment plan.",
    ]),
    ("Worked examples", [
        "If an adult weighs 70 kg and is 170 cm tall, the calculation is 70 ÷ (1.70 × 1.70), giving a BMI of 24.2 after rounding. The displayed adult category is normal weight.",
        "For someone who is 5 ft 7 in tall, total height is 67 inches. Converting that to centimetres gives 170.18 cm. With a weight of 70 kg, BMI is also about 24.2. Enter feet and inches separately rather than entering a decimal number such as 5.7 feet.",
    ]),
    ("What BMI cannot tell you", [
        "BMI does not measure body fat directly or show where fat is stored. A person with substantial muscle mass may have a higher BMI without having the same body-fat level as another person with the same BMI. Body frame, fat distribution, health history and other measurements can change how the result should be interpreted.",
        "BMI categories for adults are not suitable for children and teenagers, who need age- and sex-specific growth charts. BMI also needs special interpretation during pregnancy and may be less informative for some older adults or people with fluid retention, recent illness or changes in muscle mass.",
    ]),
    ("Using the result responsibly", [
        "BMI is a general screening tool. It does not measure body fat directly and does not replace advice from a doctor.",
        "Use the number as one starting point, not as a complete assessment of health. A healthcare professional may consider waist circumference, blood pressure, blood tests, medicines, family history, activity and nutrition alongside BMI.",
        "Speak with a qualified clinician if you are worried about weight changes, have symptoms, are pregnant, have a medical condition, or need advice for a child or teenager. Do not change medication, restrict food severely or start a treatment plan based on this calculator alone.",
        "The calculator accepts adult heights from 50 to 260 cm, or feet from 1 to 8 and inches from 0 to 11.99. Weight input limits are 20 to 300 kg or 44.1 to 661.3 lb. These are input limits for this tool, not medical recommendations.",
    ]),
]
BMI_FAQ = [
    ("Can I use this BMI calculator for children or teenagers?", "No. This calculator uses adult BMI categories. Children and teenagers need age- and sex-specific BMI-for-age growth charts interpreted in the right context."),
    ("Does BMI measure body fat?", "No. BMI uses height and weight only. It cannot directly measure body fat or distinguish muscle from fat."),
    ("Is a BMI of 25 a diagnosis?", "No. An exact adult BMI of 25.0 is the start of the overweight screening category, not a diagnosis. A displayed value of 25.0 may be rounded from a slightly lower exact BMI, so the category is based on the unrounded value. A clinician can interpret it with other health information."),
    ("Why can the displayed BMI and category appear to differ near a boundary?", "The category is selected using the unrounded BMI. The displayed number is rounded to one decimal place. For example, an exact BMI of 24.98 displays as 25.0 but remains in the normal weight category. At exactly 25.0, the adult screening category is overweight."),
    ("What should I do with my result?", "Treat it as general information. Discuss concerns or major weight changes with a qualified healthcare professional, especially if you have symptoms or a medical condition."),
]
BMI_SOURCES = 'Adult BMI categories follow the <a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" target="_blank" rel="noopener noreferrer">World Health Organization</a> classification. The <a class="' + LINK + '" href="https://www.nhs.uk/health-assessment-tools/calculate-your-body-mass-index/calculate-bmi-for-adults" target="_blank" rel="noopener noreferrer">NHS adult BMI calculator</a> explains ethnicity-specific interpretation. The <a class="' + LINK + '" href="https://www.nhs.uk/health-assessment-tools/calculate-your-waist-to-height-ratio" target="_blank" rel="noopener noreferrer">NHS waist-to-height ratio calculator</a> explains the half-height check. The <a class="' + LINK + '" href="https://doi.org/10.2337/doci26-0003" target="_blank" rel="noopener noreferrer">2026 Standards of Care in Overweight and Obesity</a> describes current clinical assessment criteria. This calculator displays standard adult WHO categories and does not diagnose a condition.'

def tool_page(t):
    path = "/" + t["slug"] + "/"
    url = SITE_URL + path
    cat = next(c for c in CATEGORIES if c["slug"] == t["category"])
    if t["slug"] == "zakat-calculator":
        title = "Zakat Calculator Online | Hanafi and Sistani Ja'fari Nisab"
        desc = "Hanafi Zakat on cash, gold, silver, stock and receivables, or Sayyid Sistani's limited Ja'fari trading-goods method, with clear assumptions."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "bmi-calculator":
        title = "BMI Calculator for Adults | cm or ft/in | CalculatesAll"
        desc = "Calculate adult BMI using kilograms and centimetres or kilograms with feet and inches. See WHO adult BMI ranges and their limitations."
        ui = BMI_UI
        guide = BMI_GUIDE + GUIDE_EXTRA.get(t["slug"], [])
        faqs = BMI_FAQ
        sources = BMI_SOURCES
    elif t["slug"] == "profit-loss-calculator":
        title = "Profit and Loss Calculator | Markup and Margin"
        desc = "Calculate product profit, business operating profit, loss, markup and margin from revenue, costs and expenses. Includes clear formulas and PKR examples."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "unit-converter":
        title = "Unit Converter | Weight, Length & Temperature"
        desc = "Convert kilograms, grams, pounds, ounces, metric and imperial lengths, and Celsius, Fahrenheit or Kelvin. See formulas, examples and input limits."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "years-to-days-calculator":
        title = "Years to Days Calculator | How Many Days in X Years?"
        desc = "Convert years to days or days to years with 365, 365.25 or 365.2425-day methods. Compare examples and count exact calendar days from a start date."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "tasbih-counter":
        title = "Tasbih Calculator Online | Dhikr Counter | CalculatesAll"
        desc = "Free online tasbih calculator for dhikr and zikr. Count 33, 99 or a custom target, undo taps and keep progress in this browser when storage is available."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "discount-calculator":
        title = "Discount Calculator: Sale Price & Savings | CalculatesAll"
        desc = "Calculate a discount, final sale price and total savings from the original price and discount percentage."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "stopwatch":
        title = "Free Online Stopwatch | CalculatesAll"
        desc = "Use a free online stopwatch with start, stop, reset and hundredths-of-a-second timing in your browser."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    else:
        title = t["name"] + " | Free Online Tool | CalculatesAll"
        desc = t["description"]
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    ui = attach_notice_badge(ui, t["slug"], "en")
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": url,
         "description": desc, "applicationCategory": t["app"], "operatingSystem": "Any",
         "author": {"@id": SITE_URL + "/#maintainer"}, "publisher": {"@id": SITE_URL + "/#organization"},
         "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": cat["name"], "item": SITE_URL + "/" + cat["slug"] + "/"},
            {"@type": "ListItem", "position": 3, "name": t["name"], "item": url}]},
        {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/#maintainer", "name": "Muhammad Fayyaz Adeel", "url": SITE_URL + "/about/", "worksFor": {"@id": SITE_URL + "/#organization"}},
        {"@context": "https://schema.org", "@type": "Organization", "@id": SITE_URL + "/#organization", "name": "CalculatesAll", "url": SITE_URL + "/", "description": SITE_DESCRIPTION, "logo": SITE_URL + "/assets/favicon.svg", "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "url": SITE_URL + "/contact/"}},
    ]
    if t["slug"] == "zakat-calculator":
        schema[1]["@id"] = url + "#breadcrumb"
        schema.append({
            "@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage",
            "name": title, "url": url, "description": desc,
            "author": {"@id": SITE_URL + "/#maintainer"},
            "publisher": {"@id": SITE_URL + "/#organization"},
            "isPartOf": {"@id": SITE_URL + "/#website"},
            "breadcrumb": {"@id": url + "#breadcrumb"},
            "dateModified": "2026-11-16",
            "citation": [
                "https://www.sistani.org/english/book/48/2317/",
                "https://www.sistani.org/english/book/48/2318/",
                "https://www.sistani.org/english/book/48/2323/",
                "https://www.sistani.org/english/qa/14884/",
                "https://islamqa.org/hanafi/darulfiqh/156652/",
                "https://sindhlaws.gov.pk/Setup/Publications_SindhCode/PUB-16-000006.pdf",
                "https://www.islamic-relief.org.uk/giving/islamic-giving/zakat/zakat-calculator/",
                "https://nzfworldwide.com/wp-content/uploads/2022/03/NZF_Zakat-Calculation-Principle-No.1.pdf",
                "https://www.sbp.org.pk/circulars/bprd-circular-letter-no-03-of-2026",
            ],
            "inLanguage": "en",
        })
    elif t["slug"] == "bmi-calculator":
        # Link the page entity to the visible maintainer, site publisher, source citation and breadcrumb.
        # Do not claim medical review, ratings, or a dateModified that has not been verified.
        schema[1]["@id"] = url + "#breadcrumb"
        schema.append({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": url + "#webpage",
            "name": title,
            "url": url,
            "description": desc,
            "author": {"@id": SITE_URL + "/#maintainer"},
            "publisher": {"@id": SITE_URL + "/#organization"},
            "isPartOf": {"@id": SITE_URL + "/#website"},
            "breadcrumb": {"@id": url + "#breadcrumb"},
            "citation": ["https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight"],
            "inLanguage": "en",
        })
    related_map = {
        "tasbih-counter": [("stopwatch", "Online Stopwatch"), ("zakat-calculator", "Zakat Calculator")],
        "profit-loss-calculator": [("discount-calculator", "Discount Calculator"), ("percentage-calculator", "Percentage Calculator"), ("emi-calculator", "EMI Calculator"), ("compound-interest-calculator", "Compound Interest Calculator")],
        "discount-calculator": [("percentage-calculator", "Percentage Calculator"), ("profit-loss-calculator", "Profit and Loss Calculator")],
        "standard-calculator": [("percentage-calculator", "Percentage Calculator"), ("fraction-calculator", "Fraction Calculator")],
        "age-calculator": [("date-calculator", "Date Difference Calculator"), ("years-to-days-calculator", "Years to Days Calculator")],
        "years-to-days-calculator": [("date-calculator", "Date Difference Calculator"), ("age-calculator", "Age Calculator"), ("query-calculator", "Query Calculator"), ("unit-converter", "Unit Converter")],
        "query-calculator": [("years-to-days-calculator", "Years to Days Calculator"), ("age-calculator", "Age Calculator")],
        "unit-converter": [("bmi-calculator", "Adult BMI Calculator"), ("calorie-calculator", "Calorie Calculator")],
    }
    related_items = related_map.get(t["slug"], [])
    related = "".join(
        '<li><a class="' + LINK + '" href="/' + slug + '/">' + label + "</a></li>"
        for slug, label in related_items
    )
    related_section = (
        '<section class="mt-12"><h2 class="text-xl font-semibold text-stone-900 dark:text-stone-100">Related calculators</h2>'
        '<ul class="mt-3 grid sm:grid-cols-2 gap-2 text-base">' + related + "</ul></section>"
    ) if related else ""
    alternates = None
    if t["slug"] in URDU:
        alternates = [("en", path), ("ur", "/ur" + path), ("x-default", path)]
    updated_date = LASTMOD.get(path)
    updated = ('<p class="mt-8 text-sm text-stone-800 dark:text-stone-200">Last updated: ' + updated_date + "</p>") if updated_date else ""
    if t["slug"] in {"standard-calculator", "zakat-calculator"}:
        calculator_classes = "ca-tool-standard-calculator"
        if t["slug"] == "zakat-calculator":
            calculator_classes += " ca-tool-zakat-calculator"
        calculator_section = (
            '<section id="tool-calculator" class="' + calculator_classes + ' mt-2 rounded-2xl bg-white/95 dark:bg-stone-900/95 shadow-xl ring-1 ring-stone-200 dark:ring-stone-700 p-3 sm:p-4" aria-label="Calculator">'
            + ui + '</section>'
        )
    else:
        calculator_section = (
            '<section id="tool-calculator" class="ca-tool-calculator ca-tool-' + t["slug"] + ' mt-4 rounded-2xl bg-white/95 dark:bg-stone-900/95 shadow-xl ring-1 ring-stone-200 dark:ring-stone-700 p-5 sm:p-6" aria-label="Calculator">'
            + ui + '</section>'
        )
    answer_note = answer_block(t["slug"], "en")
    breadcrumb_html = (
        '<nav aria-label="Breadcrumb" class="text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap gap-2">'
        '<li><a class="' + LINK + '" href="/">Home</a></li>'
        '<li><span aria-hidden="true" class="mr-2">/</span><a class="' + LINK + '" href="/' + cat["slug"] + '/">' + cat["name"] + '</a></li>'
        '<li aria-current="page"><span aria-hidden="true" class="mr-2">/</span>' + t["name"] + "</li></ol></nav>"
    )
    primary_tool_content = calculator_section + (breadcrumb_html if t["slug"] == "profit-loss-calculator" else "") + answer_note
    profit_reference_table = (
        '<section class="mt-8" aria-labelledby="markup-margin-comparison">'
        '<h2 id="markup-margin-comparison" class="' + H2 + '">Markup versus margin at a glance</h2>'
        '<p class="' + P + '">Both percentages describe profit against a different base. The base must be named before comparing results.</p>'
        '<div class="mt-4 overflow-x-auto rounded-xl border border-stone-300 dark:border-stone-700">'
        '<table class="w-full min-w-[600px] border-collapse text-left text-sm"><caption class="sr-only">Profit, markup and margin formulas with worked examples</caption>'
        '<thead class="bg-slate-100 dark:bg-stone-800"><tr><th scope="col" class="p-3">Measure</th><th scope="col" class="p-3">Formula</th><th scope="col" class="p-3">Worked example</th></tr></thead>'
        '<tbody>'
        '<tr class="border-t border-stone-200 dark:border-stone-700"><th scope="row" class="p-3">Product profit</th><td class="p-3">Selling price − cost price</td><td class="p-3">1,000 − 800 = 200</td></tr>'
        '<tr class="border-t border-stone-200 dark:border-stone-700"><th scope="row" class="p-3">Markup on cost</th><td class="p-3">Profit ÷ cost × 100</td><td class="p-3">200 ÷ 800 × 100 = 25%</td></tr>'
        '<tr class="border-t border-stone-200 dark:border-stone-700"><th scope="row" class="p-3">Product gross margin</th><td class="p-3">Profit ÷ selling price × 100</td><td class="p-3">200 ÷ 1,000 × 100 = 20%</td></tr>'
        '<tr class="border-t border-stone-200 dark:border-stone-700"><th scope="row" class="p-3">Business operating margin</th><td class="p-3">Operating profit ÷ revenue × 100</td><td class="p-3">(1,000 − 600 − 150) ÷ 1,000 × 100 = 25%</td></tr>'
        '</tbody></table></div></section>'
    ) if t["slug"] == "profit-loss-calculator" else ""
    priority_first_screen = t["slug"] in {"tasbih-counter", "profit-loss-calculator", "years-to-days-calculator"}
    opening_lead = '<p class="ca-tool-lead mt-3 text-base leading-relaxed text-stone-900 dark:text-stone-100">' + t["lead"] + '</p>'
    body = (
        ("" if t["slug"] == "profit-loss-calculator" else breadcrumb_html)
        + '<h1 class="text-3xl font-extrabold bg-gradient-to-r from-fuchsia-700 via-indigo-700 to-sky-700 bg-clip-text text-transparent mt-4' + (' ca-tool-zakat-heading' if t["slug"] == "zakat-calculator" else '') + '"><span aria-hidden="true">' + TILE_ICON.get(t["slug"], "") + '</span> ' + t["h1"] + '</h1>'
        + (opening_lead + primary_tool_content
           if priority_first_screen
           else primary_tool_content + '<p class="ca-tool-lead-after mt-3 text-base text-stone-900 dark:text-stone-100">' + t["lead"] + '</p>'
           if t["slug"] in {tool["slug"] for tool in TOOLS}
           else '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + t["lead"] + '</p>' + primary_tool_content)
        + ad_slot()
        + (('<h2 class="' + H2 + '">How it is calculated</h2>'
            + '<p class="mt-4 rounded-xl bg-sky-50 dark:bg-sky-950 border border-sky-200 dark:border-sky-800 p-5 text-base text-stone-900 dark:text-stone-100"><strong>Worked method.</strong> ' + EXTRA[t["slug"]]["quick"] + '</p>')
           if EXTRA[t["slug"]]["quick"].strip() else "")
        + profit_reference_table
        + (years_to_days_reference_html() + guide_html(guide[:2]) + guide_html(guide[2:]) + days_to_years_reference_html()
           if t["slug"] == "years-to-days-calculator" else guide_html(guide))
        + '<h2 class="' + H2 + '">Common questions</h2><div class="mt-3">' + faq_html(faqs) + "</div>"
        + '<h2 class="' + H2 + '">' + ("Scope and religious guidance" if t["slug"] == "tasbih-counter" else "Sources") + '</h2><p class="' + P + '">' + sources + '</p>'
        + '<p class="mt-6 text-sm text-stone-700 dark:text-stone-300">Maintained by <a class="' + LINK + '" href="/about/">Muhammad Fayyaz Adeel</a>.</p>'
        + updated
        + review_box(t["slug"])
        + related_section
    )
    rs = reviewer_schema(t["slug"])
    if rs:
        schema.append(rs)
    write(path, canon_override(head(title, desc, path, schema, alternates=alternates) + shell(body, current_path=path), path))
    return path


def urdu_tool_page(t):
    u = URDU[t["slug"]]
    path = "/ur/" + t["slug"] + "/"
    url = SITE_URL + path
    ui = BMI_UI if t["slug"] == "bmi-calculator" else t["ui"]
    for en, ur in u["labels"]:
        # Localize labels regardless of their HTML wrapper (span, legend, button, or attribute).
        ui = ui.replace(">" + en + "<", ">" + ur + "<")
        ui = ui.replace(">" + en + "</legend>", ">" + ur + "</legend>")
        ui = ui.replace('"' + en + '"', '"' + ur + '"')
        if t["slug"] == "bmi-calculator":
            ui = ui.replace(en, ur)
    if t["slug"] == "standard-calculator":
        ui = ui.replace('>Scientific Mode</button>', '>سائنسی کیلکولیٹر</button>')
    if t["slug"] == "zakat-calculator":
        ui = ui.replace(">Additional assets, metal prices and conditions<", ">اضافی اثاثے، دھاتوں کی قیمتیں اور شرائط<")
    if t["slug"] == "profit-loss-calculator":
        ui = ui.replace("> Business P&amp;L</label>", "> کاروبار کا نفع و نقصان</label>")
        ui = ui.replace("> Product profit</label>", "> پروڈکٹ کا نفع</label>")
    if t["slug"] == "tasbih-counter":
        ui = ui.replace("Saving is unavailable in this browser. Your count and selected settings stay in memory only until you leave or reload this page.", "اس براؤزر میں گنتی محفوظ کرنا ممکن نہیں ہے، اور منتخب ترتیبات بھی محفوظ نہیں ہوں گی۔ گنتی اور ترتیبات اس صفحے کو چھوڑنے یا دوبارہ لوڈ کرنے تک عارضی طور پر رہیں گی۔")
        ui = ui.replace('<label class="', '<label lang="ur" class="')
        ui = ui.replace('id="t-lifetime-label">', 'id="t-lifetime-label" lang="ur">')
    ui = attach_notice_badge(ui, t["slug"], "ur")
    cat = next(c for c in CATEGORIES if c["slug"] == t["category"])
    cat_ur = {"money": "پیسہ اور کاروبار", "health": "صحت", "time": "تاریخ اور وقت", "math": "ریاضی اور اکائیاں", "worship": "عبادت اور روزمرہ"}[cat["slug"]]
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": u["name"], "url": url,
         "description": u["description"], "inLanguage": "ur", "applicationCategory": t["app"],
         "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "صفحہ اول", "item": SITE_URL + "/ur/"},
            {"@type": "ListItem", "position": 2, "name": cat_ur, "item": SITE_URL + "/" + cat["slug"] + "/"},
            {"@type": "ListItem", "position": 3, "name": u["name"], "item": url}]},
    ]
    if t["slug"] == "zakat-calculator":
        schema[0]["author"] = {"@id": SITE_URL + "/#maintainer"}
        schema[0]["publisher"] = {"@id": SITE_URL + "/#organization"}
        schema.append({
            "@context": "https://schema.org", "@type": "WebPage",
            "name": u["title"], "url": url, "inLanguage": "ur",
            "author": {"@id": SITE_URL + "/#maintainer"},
            "publisher": {"@id": SITE_URL + "/#organization"},
            "dateModified": "2026-11-16",
            "citation": [
                "https://www.sistani.org/english/book/48/2317/",
                "https://www.sistani.org/english/book/48/2318/",
                "https://www.sistani.org/english/book/48/2323/",
                "https://www.sistani.org/english/qa/14884/",
                "https://islamqa.org/hanafi/darulfiqh/156652/",
                "https://sindhlaws.gov.pk/Setup/Publications_SindhCode/PUB-16-000006.pdf",
                "https://www.islamic-relief.org.uk/giving/islamic-giving/zakat/zakat-calculator/",
                "https://nzfworldwide.com/wp-content/uploads/2022/03/NZF_Zakat-Calculation-Principle-No.1.pdf",
                "https://www.sbp.org.pk/circulars/bprd-circular-letter-no-03-of-2026",
            ],
        })
        how = ""
        for p in u["how"]:
            how += '<p class="' + P + '">' + p + "</p>"
    elif t["slug"] == "bmi-calculator":
        schema[0]["author"] = {"@id": SITE_URL + "/#maintainer"}
        schema[0]["publisher"] = {"@id": SITE_URL + "/#organization"}
        schema.append({
            "@context": "https://schema.org", "@type": "WebPage",
            "name": u["title"], "url": url, "inLanguage": "ur",
            "author": {"@id": SITE_URL + "/#maintainer"},
            "publisher": {"@id": SITE_URL + "/#organization"},
            "dateModified": "2026-11-09",
            "citation": [
                "https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight",
                "https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html",
                "https://www.nhs.uk/conditions/overweight-and-obesity/",
                "https://pubmed.ncbi.nlm.nih.gov/14726171/",
            ],
        })
        how = bmi_urdu_guide_html()
    else:
        how = ""
        for p in u["how"]:
            how += '<p class="' + P + '">' + p + "</p>"
    faq = faq_html(u["faq"])
    if t["slug"] == "zakat-calculator":
        calculator_section = (
            '<section id="tool-calculator" class="ca-tool-standard-calculator ca-tool-zakat-calculator mt-2 rounded-2xl bg-white/95 dark:bg-stone-900/95 shadow-xl ring-1 ring-stone-200 dark:ring-stone-700 p-3 sm:p-4" aria-label="کیلکولیٹر">'
            + ui + '</section>'
        )
    elif t["slug"] == "standard-calculator":
        calculator_section = (
            '<section id="tool-calculator" class="ca-tool-standard-calculator mt-4" aria-label="کیلکولیٹر">'
            + ui + '</section>'
        )
    else:
        calculator_section = (
            '<section id="tool-calculator" class="ca-tool-calculator ca-tool-' + t["slug"] + ' mt-4" aria-label="کیلکولیٹر">'
            + ui + '</section>'
        )
    answer_note = "" if t["slug"] in ("bmi-calculator", "discount-calculator") else answer_block(t["slug"], "ur")
    primary_tool_content = calculator_section + answer_note
    body = (
        '<nav aria-label="صفحہ کی ترتیب" class="text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap gap-2">'
        '<li><a class="' + LINK + '" href="/ur/">صفحہ اول</a></li><li aria-hidden="true">/</li>'
        '<li><a class="' + LINK + '" href="/' + cat["slug"] + '/">' + cat_ur + '</a></li><li aria-hidden="true">/</li>'
        '<li aria-current="page">' + u["name"] + '</li></ol></nav>'
        '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100 mt-4' + (' ca-tool-zakat-heading' if t["slug"] == "zakat-calculator" else '') + '">' + u["h1"] + '</h1>'
    )
    _lead_class = "mt-2 text-base leading-5" if t["slug"] == "bmi-calculator" else "mt-3 text-lg"
    _urdu_lead = '<p class="' + _lead_class + ' text-stone-900 dark:text-stone-100">' + u["lead"] + '</p>'
    if t["slug"] in {"standard-calculator", "zakat-calculator"}:
        body += primary_tool_content + _urdu_lead
    else:
        body += _urdu_lead + primary_tool_content
    how_section = how if t["slug"] == "bmi-calculator" else ('<h2 class="' + H2 + '">' + u["how_heading"] + '</h2>' + how)
    source_checked = (
        '<p class="mt-3 text-sm text-stone-700 dark:text-stone-300">ماخذ کی آخری جانچ اور صفحے کی تازہ کاری: 16 نومبر 2026۔</p>'
        if t["slug"] == "zakat-calculator" else
        '<p class="mt-3 text-sm text-stone-700 dark:text-stone-300">ماخذ کی آخری جانچ: 6 نومبر 2026۔</p>'
        if t["slug"] == "bmi-calculator" else ""
    )
    maintainer_note = (
        '<p class="mt-8 text-sm text-stone-700 dark:text-stone-300">صفحے کے منتظم: <a class="' + LINK + '" href="/about/">Muhammad Fayyaz Adeel</a>۔ یہ زکوٰۃ کا حسابی تخمینہ ہے، فتویٰ نہیں۔</p>'
        if t["slug"] == "zakat-calculator" else
        '<p class="mt-8 text-sm text-stone-700 dark:text-stone-300">صفحے کے منتظم: <a class="' + LINK + '" href="/about/">Muhammad Fayyaz Adeel</a>۔ یہ صفحہ عمومی معلومات فراہم کرتا ہے، طبی تشخیص یا علاج کا متبادل نہیں۔</p>'
        if t["slug"] == "bmi-calculator" else ""
    )
    related_urdu = ""
    if t["slug"] == "bmi-calculator":
        related_urdu = (
            '<section class="mt-8" aria-labelledby="bmi-urdu-related">'
            '<h2 id="bmi-urdu-related" class="' + H2 + '">متعلقہ کیلکولیٹر اور ٹولز</h2>'
            '<ul class="mt-3 grid gap-3 sm:grid-cols-2">'
            '<li><a class="' + LINK + '" href="/health/">صحت کے کیلکولیٹر</a></li>'
            '<li><a class="' + LINK + '" href="/bmi-calculator/" hreflang="en">BMI Calculator in English</a></li>'
            '<li><a class="' + LINK + '" href="/calorie-calculator/">بالغوں کا کیلوری کیلکولیٹر</a></li>'
            '<li><a class="' + LINK + '" href="/ur/age-calculator/">عمر کیلکولیٹر</a></li>'
            '<li><a class="' + LINK + '" href="/ur/unit-converter/">یونٹ کنورٹر</a></li>'
            '</ul></section>'
        )
    body += (
        how_section
        + '<h2 class="' + H2 + '">' + u["faq_heading"] + '</h2><div class="mt-3">' + faq + "</div>"
        + ('<h2 class="' + H2 + '">ماخذ</h2><p class="' + P + '">' + u["sources"] + '</p>' if u.get("sources") else "")
        + source_checked + maintainer_note + related_urdu
        + '<p class="mt-10 text-sm text-stone-800 dark:text-stone-200"><a class="' + LINK + '" href="/' + t["slug"] + '/" hreflang="en">انگریزی ورژن</a></p>'
    )
    alternates = [("en", "/" + t["slug"] + "/"), ("ur", path), ("x-default", "/" + t["slug"] + "/")]
    write(path, canon_override(head(u["title"], u["description"], path, schema, lang="ur", alternates=alternates) + shell(body, lang="ur", current_path=path), path))
    return path


def category_page(c):
    path = "/" + c["slug"] + "/"
    items = ""
    for t in TOOLS:
        if t["category"] == c["slug"]:
            items += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                      '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/' + t["slug"] + '/">' + t["name"] + "</a>"
                      '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + t["description"] + "</p></li>")
    if c["slug"] == "money":
        items += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                  '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/emi-calculator/">EMI Calculator</a>'
                  '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">Estimate monthly loan installments, total interest and a month-by-month repayment schedule. Lender fees and contract terms may change the final quote.</p></li>')
    for slug, label in {"math": [("percentage-calculator", "Percentage Calculator"), ("percentage-difference-calculator", "Percentage Difference Calculator"), ("ratio-calculator", "Ratio Calculator"), ("fraction-calculator", "Fraction Calculator")], "money": [("compound-interest-calculator", "Compound Interest Calculator")], "time": [("date-calculator", "Date Difference Calculator")]}.get(c["slug"], []):
        items += '<li><a class="text-sky-800 underline" href="/' + slug + '/">' + label + '</a></li>'
    related = "".join(
        '<li><a class="text-sky-800 dark:text-sky-300 underline" href="/'
        + other["slug"] + '/">' + html.escape(other["name"]) + "</a></li>"
        for other in CATEGORIES if other["slug"] != c["slug"]
    )
    title = c["name"] + " | CalculatesAll"
    schema = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": c["name"], "url": SITE_URL + path},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": c["name"], "item": SITE_URL + path},
        ]},
    ]
    breadcrumb = (
        '<nav aria-label="Breadcrumb" class="mb-6 text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap items-center gap-2">'
        '<li><a class="' + LINK + '" href="/">Home</a></li><li aria-hidden="true">/</li>'
        '<li aria-current="page">' + html.escape(c["name"]) + '</li></ol></nav>'
    )
    body = (breadcrumb
            + '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">' + c["name"] + '</h1>'
            '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + c["desc"] + '</p>'
            '<p class="mt-4 text-base leading-relaxed text-stone-800 dark:text-stone-200">' + HUB_CONTENT[c["slug"]]["intro"] + '</p>'
            '<ul class="mt-8 grid gap-4">' + items + "</ul>"
        + '<nav aria-label="Other calculator categories" class="mt-8"><h2 class="text-xl font-semibold">Explore other calculator categories</h2><ul class="mt-3 flex flex-wrap gap-4">' + related + "</ul></nav>"
        + guide_html(HUB_EXTRA[c["slug"]]) +
            '<h2 class="' + H2 + '">Questions</h2><div class="mt-3">' + faq_html(HUB_CONTENT[c["slug"]]["faq"]) + "</div>")
    write(path, head(title, c["desc"], path, schema) + shell(body))
    return path


def static_page(path, title, desc, h1, paragraphs, noindex=False):
    if path == "/about/":
        schema = [{"@context": "https://schema.org", "@type": "AboutPage", "@id": SITE_URL + "/about/#webpage",
                   "name": title, "url": SITE_URL + path, "description": desc,
                   "mainEntity": {"@id": SITE_URL + "/#organization"},
                   "about": {"@id": SITE_URL + "/#maintainer"},
                   "isPartOf": {"@id": SITE_URL + "/#website"}}]
    else:
        schema = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": SITE_URL + path}]
    if path in ("/about/", "/contact/", "/editorial-policy/"):
        schema.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": SITE_URL + path + "#breadcrumb",
                       "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": SITE_URL + path},
        ]})
        if path == "/about/":
            schema[0]["breadcrumb"] = {"@id": SITE_URL + path + "#breadcrumb"}
    if path == "/about/":
        body = ('<nav aria-label="Breadcrumb" class="mb-6 text-sm text-stone-700 dark:text-stone-300"><ol class="flex flex-wrap items-center gap-2">'
                '<li><a class="' + LINK + '" href="/">Home</a></li><li aria-hidden="true">/</li>'
                '<li aria-current="page">About CalculatesAll</li></ol></nav>')
    else:
        body = ""
    body += '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">' + h1 + '</h1>'
    methodology_headings = {
        0: "How to use this methodology",
        1: "Arithmetic, percentages and fractions",
        4: "Money, profit, discounts and loans",
        8: "Dates and unit conversions",
        10: "Health and Zakat calculation limits",
        12: "Rounding, input validation and verification",
        15: "Privacy, references and corrections",
        18: "Calculator-specific assumptions",
        21: "Practical checks for money and unit conversions",
    } if path == "/methodology/" else {}
    for index, p in enumerate(paragraphs):
        if index in methodology_headings:
            body += '<h2 class="' + H2 + '">' + methodology_headings[index] + "</h2>"
        body += '<p class="' + P + '">' + p + "</p>"
    if path == "/about/":
        contact_email = html.escape(CONTACT_EMAIL, quote=True)
        body += (
            '<section aria-labelledby="about-maintainer" class="mt-8">'
            '<h2 id="about-maintainer" class="' + H2 + '">Who maintains CalculatesAll?</h2>'
            '<p class="' + P + '">CalculatesAll is maintained by Muhammad Fayyaz Adeel, also known as Malik Adeel Bhatti. The maintainer looks after the calculator pages, site updates and reproducible correction reports. See the <a class="' + LINK + '" href="https://github.com/Beastmalik7424" rel="noopener noreferrer">public GitHub profile</a> and <a class="' + LINK + '" href="https://github.com/Beastmalik7424/calculatesallinone" rel="noopener noreferrer">source repository</a>. This identifies project responsibility; it does not claim a regulated professional qualification or independent expert review.</p>'
            '</section>'
            '<section aria-labelledby="about-tools" class="mt-8">'
            '<h2 id="about-tools" class="' + H2 + '">What calculators and tools are available?</h2>'
            '<p class="' + P + '">The money tools include the <a class="' + LINK + '" href="/profit-loss-calculator/">Profit and Loss Calculator</a>, <a class="' + LINK + '" href="/discount-calculator/">Discount Calculator</a>, <a class="' + LINK + '" href="/emi-calculator/">EMI Calculator</a>, <a class="' + LINK + '" href="/zakat-calculator/">Zakat Calculator</a> and <a class="' + LINK + '" href="/compound-interest-calculator/">Compound Interest Calculator</a>. Date and measurement tools include the <a class="' + LINK + '" href="/age-calculator/">Age Calculator</a>, <a class="' + LINK + '" href="/years-to-days-calculator/">Years to Days Calculator</a>, <a class="' + LINK + '" href="/date-calculator/">Date Difference Calculator</a>, <a class="' + LINK + '" href="/query-calculator/">Query Calculator</a> and <a class="' + LINK + '" href="/unit-converter/">Unit Converter</a>.</p>'
            '<p class="' + P + '">For the complete list of free calculators, see the <a class="' + LINK + '" href="/free-online-calculators/">free online calculators guide</a>.</p>'
            '<p class="' + P + '">Browse the <a class="' + LINK + '" href="/money/">Money and Business</a>, <a class="' + LINK + '" href="/math/">Math and Converters</a>, <a class="' + LINK + '" href="/time/">Date and Time</a>, <a class="' + LINK + '" href="/health/">Health</a> and <a class="' + LINK + '" href="/worship/">Worship and Daily Use</a> categories to find related tools and their stated scope.</p>'
            '<p class="' + P + '">The Query Calculator accepts defined plain-language time and date conversions, Gregorian age from a birth date, and simple addition or subtraction. It states its average-year and average-month assumptions and rejects unsupported questions instead of guessing.</p>'
            '<p class="' + P + '">Math tools include the <a class="' + LINK + '" href="/percentage-calculator/">Percentage Calculator</a>, <a class="' + LINK + '" href="/percentage-difference-calculator/">Percentage Difference Calculator</a> and <a class="' + LINK + '" href="/fraction-calculator/">Fraction Calculator</a>. Everyday tools include the <a class="' + LINK + '" href="/standard-calculator/">Standard Calculator</a>, <a class="' + LINK + '" href="/bmi-calculator/">adult BMI calculator</a>, <a class="' + LINK + '" href="/tasbih-counter/">Tasbih Counter</a> and <a class="' + LINK + '" href="/stopwatch/">Stopwatch</a>.</p>'
            '</section>'
            '<section aria-labelledby="about-checks" class="mt-8">'
            '<h2 id="about-checks" class="' + H2 + '">How are calculator methods and changes checked?</h2>'
            '<p class="' + P + '">Calculator pages explain their required inputs, formulas, assumptions and important limits. Worked examples are included where they help a visitor check the result. The project uses automated checks for representative calculations, boundary and invalid inputs, generated pages and site metadata. Test coverage varies by tool. Passing tests reduce regression risk, but they do not prove every possible input or device combination. Read the <a class="' + LINK + '" href="/methodology/">calculation methodology</a> and <a class="' + LINK + '" href="/editorial-policy/">editorial policy</a> for more detail.</p>'
            '<h3 class="mt-6 text-lg font-semibold text-stone-900 dark:text-stone-100">Which reference sources support selected tools?</h3>'
            '<p class="' + P + '">Where a method relies on published health, measurement or financial guidance, the relevant calculator page links to its source. Examples include the <a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" target="_blank" rel="noopener noreferrer">World Health Organization adult BMI information</a>, the <a class="' + LINK + '" href="https://www.nist.gov/pml/owm/si-units-length" target="_blank" rel="noopener noreferrer">NIST length-unit reference</a>, the <a class="' + LINK + '" href="https://openstax.org/books/principles-finance/pages/5-1-the-income-statement" target="_blank" rel="noopener noreferrer">OpenStax income-statement chapter</a> and <a class="' + LINK + '" href="https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f2/technical-articles/ratio-analysis.html" target="_blank" rel="noopener noreferrer">ACCA ratio-analysis guidance</a>.</p>'
            '</section>'
            '<section aria-labelledby="about-privacy" class="mt-8">'
            '<h2 id="about-privacy" class="' + H2 + '">What happens to calculator inputs?</h2>'
            '<p class="' + P + '">Values entered into calculator forms are processed in your browser and are not sent to the CalculatesAll server. The Tasbih Counter stores its count on the current device. The hosting provider and third-party resources may process technical request data, and advertising services may use cookies as explained in the <a class="' + LINK + '" href="/privacy/">privacy policy</a>. Avoid sending sensitive financial, medical or account information in an email.</p>'
            '</section>'
            '<section aria-labelledby="about-limits" class="mt-8">'
            '<h2 id="about-limits" class="' + H2 + '">What are the limits of these tools?</h2>'
            '<p class="' + P + '">A calculator can only account for the inputs and assumptions it is designed to use. Check the units, percentage basis and exclusions shown on the relevant tool before relying on a result.</p>'
            '<div class="mt-4 overflow-x-auto"><table class="w-full border-collapse text-left text-sm"><caption class="mb-2 text-left font-semibold text-stone-900 dark:text-stone-100">Important assumptions to check before using a result</caption>'
            '<thead><tr><th scope="col" class="border border-stone-300 dark:border-stone-700 p-3">Tool area</th><th scope="col" class="border border-stone-300 dark:border-stone-700 p-3">What to check</th></tr></thead><tbody>'
            '<tr><th scope="row" class="border border-stone-300 dark:border-stone-700 p-3">Money</th><td class="border border-stone-300 dark:border-stone-700 p-3">The percentage basis matters. Taxes, fees, shipping and other costs are included only when the tool supports them and you enter them.</td></tr>'
            '<tr><th scope="row" class="border border-stone-300 dark:border-stone-700 p-3">Dates</th><td class="border border-stone-300 dark:border-stone-700 p-3">Calendar months have different lengths and leap years affect durations. Check whether the selected tool counts the start and end dates inclusively.</td></tr>'
            '<tr><th scope="row" class="border border-stone-300 dark:border-stone-700 p-3">Units</th><td class="border border-stone-300 dark:border-stone-700 p-3">Confirm both units. Temperature conversions require an offset as well as a scale factor.</td></tr>'
            '<tr><th scope="row" class="border border-stone-300 dark:border-stone-700 p-3">Health and Zakat</th><td class="border border-stone-300 dark:border-stone-700 p-3">Adult BMI is a screening measure, not a diagnosis. The Zakat calculator follows its stated method and is not a religious ruling.</td></tr>'
            '<tr><th scope="row" class="border border-stone-300 dark:border-stone-700 p-3">Timing</th><td class="border border-stone-300 dark:border-stone-700 p-3">The stopwatch is for everyday timing, not certified measurement.</td></tr>'
            '</tbody></table></div>'
            '<p class="' + P + '">For important financial, medical or religious decisions, confirm the result with an appropriately qualified professional or scholar.</p>'
            '</section>'
            '<section aria-labelledby="about-contact" class="mt-8">'
            '<h2 id="about-contact" class="' + H2 + '">How can a calculation issue be reported?</h2>'
            '<p class="' + P + '">Email <a class="' + LINK + '" href="mailto:' + contact_email + '">' + html.escape(CONTACT_EMAIL) + '</a> or use the <a class="' + LINK + '" href="/contact/">contact page</a>. Include the calculator name, page URL, exact input values, displayed result, expected result and steps to reproduce the issue. Do not include passwords, payment details, medical records or other sensitive personal information.</p>'
            '</section>'
        )
    write(path, head(title, desc, path, schema, noindex=noindex) + shell(body))
    return path

def home_page(lang="en"):
    if lang == "ur":
        path = "/ur/"
        title = "CalculatesAll | مفت آن لائن کیلکولیٹرز اور ٹولز"
        desc = "زکوٰۃ، BMI، منافع و نقصان، عمر، ڈسکاؤنٹ، یونٹ کنورژن، معیاری کیلکولیٹر، تسبیح کاؤنٹر اور اسٹاپ واچ کے مفت ٹولز۔"
        h1 = "مفت آن لائن کیلکولیٹرز اور یوٹیلیٹی ٹولز"
        lead = "CalculatesAll میں پیسوں، صحت، تاریخوں، اکائیوں اور روزمرہ استعمال کے کیلکولیٹرز ہیں۔ ہر ٹول آپ کے براؤزر میں چلتا ہے اور آپ کی درج کردہ معلومات ہمارے سرور پر نہیں بھیجی جاتیں۔"
        cards = ""
        for t in TOOLS:
            if t["slug"] in URDU:
                cards += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                          '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/ur/' + t["slug"] + '/">' + URDU[t["slug"]]["name"] + "</a>"
                          '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + URDU[t["slug"]]["description"] + "</p></li>")
    else:
        path = "/"
        title = "CalculatesAll | Free Online Calculators and Utility Tools"
        desc = "Free online calculators for Zakat, BMI, profit and loss, age, discounts, unit conversion, a standard calculator, tasbih counter and stopwatch."
        h1 = "EMI, BMI and Zakat Calculators"
        lead = "CalculatesAll is a free online calculator for everyday maths. Tap the buttons or use your keyboard."
        cards = ""
        for c in CATEGORIES:
            cards += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                      '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/' + c["slug"] + '/">' + c["name"] + "</a>"
                      '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + c["desc"] + "</p></li>")
    alternates = home_alts_all()
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "CalculatesAll", "url": SITE_URL + "/", "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "Organization", "name": "CalculatesAll", "url": SITE_URL + "/",
         "description": SITE_DESCRIPTION,
         "logo": SITE_URL + "/assets/favicon.svg",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "url": SITE_URL + "/contact/"}},
    ]
    body = (
        '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100 mt-2">' + h1 + '</h1>'
        '<p class="mt-4 text-lg text-stone-900 dark:text-stone-100">' + lead + '</p>'
        '<ul class="mt-10 grid gap-4">' + cards + "</ul>" + home_extra_html(lang)
    )
    write(path, head(title, desc, path, schema, lang=lang, alternates=alternates) + shell(body, lang=lang, current_path=path))
    return path


STEPS = {
    "en": [("Step 1", "Type your numbers on the calculator."), ("Step 2", "Tap = to see the answer."), ("Step 3", "Tap any coloured button to open another tool.")],
    "ur": [("پہلا قدم", "کیلکولیٹر پر اپنے نمبر لکھیں۔"), ("دوسرا قدم", "جواب دیکھنے کے لیے = دبائیں۔"), ("تیسرا قدم", "کسی دوسرے ٹول کے لیے کوئی رنگین بٹن دبائیں۔")],
}

TILE_GRAD = {
    "years-to-days-calculator": "bg-gradient-to-br from-indigo-700 to-sky-700",
    "query-calculator": "bg-gradient-to-br from-teal-700 to-blue-800",
    "zakat-calculator": "bg-gradient-to-br from-emerald-700 to-teal-700",
    "bmi-calculator": "bg-gradient-to-br from-rose-700 to-pink-700",
    "profit-loss-calculator": "bg-gradient-to-br from-sky-700 to-blue-800",
    "discount-calculator": "bg-gradient-to-br from-orange-700 to-amber-700",
    "calorie-calculator": "bg-gradient-to-br from-orange-700 to-rose-800",
    "age-calculator": "bg-gradient-to-br from-violet-700 to-purple-800",
    "unit-converter": "bg-gradient-to-br from-indigo-700 to-blue-800",
    "stopwatch": "bg-gradient-to-br from-cyan-700 to-teal-800",
    "tasbih-counter": "bg-gradient-to-br from-green-700 to-emerald-800",
}
TILE_ICON = {
    "years-to-days-calculator": "📅",
    "query-calculator": "🔎",
    "zakat-calculator": "🤲",
    "bmi-calculator": "⚖️",
    "calorie-calculator": "⚡",
    "profit-loss-calculator": "📈",
    "discount-calculator": "🏷️",
    "age-calculator": "🎂",
    "unit-converter": "📐",
    "stopwatch": "⏱️",
    "tasbih-counter": "📿",
}
TILE_BASE = ("rounded-2xl p-4 min-h-[104px] flex flex-col items-center justify-center gap-1 text-center "
             "text-white text-xl font-bold shadow-lg hover:shadow-2xl hover:-translate-y-1 transition "
             "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white")
CAT_PILL = {
    "money": "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
    "health": "bg-rose-100 text-rose-900 dark:bg-rose-900/60 dark:text-rose-100",
    "time": "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
    "math": "bg-violet-100 text-violet-900 dark:bg-violet-900/60 dark:text-violet-100",
    "worship": "bg-teal-100 text-teal-900 dark:bg-teal-900/60 dark:text-teal-100",
}
TRUST = {
    "en": ["🆓 Free", "🔒 Private", "⚡ Fast"],
    "ur": ["🆓 مفت", "🔒 محفوظ", "⚡ تیز"],
}
TRUST_CLASS = [
    "bg-emerald-100 text-emerald-900 dark:bg-emerald-900/60 dark:text-emerald-100",
    "bg-sky-100 text-sky-900 dark:bg-sky-900/60 dark:text-sky-100",
    "bg-amber-100 text-amber-900 dark:bg-amber-900/60 dark:text-amber-100",
]


def home_app_page(lang):
    urdu = lang == "ur"
    s = shell_strings(lang)
    path = "/ur/" if urdu else "/"
    if urdu:
        title = "CalculatesAll | مفت آن لائن کیلکولیٹرز اور یوٹیلیٹی ٹولز"
        desc = "زکوٰۃ، BMI، منافع و نقصان، عمر، ڈسکاؤنٹ، اکائیوں کی تبدیلی اور روزمرہ کاموں کے لیے مفت آن لائن کیلکولیٹرز۔"
        h1 = "مفت آن لائن کیلکولیٹرز اور یوٹیلیٹی ٹولز"
        lead = "CalculatesAll میں پیسے، صحت، تاریخوں، اکائیوں اور روزمرہ استعمال کے لیے مفت ٹولز موجود ہیں۔ حساب آپ کے براؤزر میں ہوتا ہے اور آپ کے درج کردہ اعداد ہمارے سرور کو نہیں بھیجے جاتے۔"
        more_h = "دوسرے ٹولز"
        tools_heading_action = '<span class="ca-home-free">' + s["free"] + '</span>'
    else:
        title = "CalculatesAll | Free Online Calculators and Utility Tools"
        desc = "Free online calculators for health, money, business, dates, mathematics and everyday conversions, with clear formulas and no sign-up."
        h1 = "Free Online Calculators"
        lead = "Free online calculators for health, money, business, dates, maths and everyday tasks. Calculate BMI, Zakat, EMI, profit and loss with clear formulas and no sign-up."
        more_h = "Calculator tools"
        tools_heading_action = '<a class="ca-home-free no-underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600" href="#ca-all-tools-menu" aria-label="Browse all free calculator tools">Browse all free calculators</a>'
    trust = ""
    for i, label in enumerate(TRUST[lang]):
        trust += '<li class="rounded-xl p-3 text-center text-sm font-bold ' + TRUST_CLASS[i] + '">' + label + "</li>"
    tiles = ""
    # Build the homepage grid from the canonical calculator navigation list so
    # new standalone calculators cannot silently disappear from the main index.
    for slug, english_name, _short_name in CAROUSEL_TOOLS:
        if slug == "standard-calculator":
            continue  # The standard calculator is already the homepage hero.
        if urdu and slug not in URDU:
            continue
        name = CAROUSEL_TRANSLATIONS["ur"][slug] if urdu else english_name
        href = ("/ur/" if urdu else "/") + slug + "/"
        icon = TILE_ICON.get(slug, "🧮")
        gradient = TILE_GRAD.get(slug, "bg-gradient-to-br from-cyan-700 to-blue-800")
        tiles += ('<li><a href="' + href + '" class="' + TILE_BASE + " " + gradient + '">'
                  '<span class="text-4xl" aria-hidden="true">' + icon + "</span>"
                  "<span>" + name + "</span></a></li>")
    all_tool_links = ""
    for slug, english_name, _short_name in CAROUSEL_TOOLS:
        if urdu:
            tool_name = CAROUSEL_TRANSLATIONS["ur"][slug]
            tool_href = ("/ur/" if slug in URDU else "/") + slug + "/"
        else:
            tool_name = english_name
            tool_href = "/" + slug + "/"
        all_tool_links += (
            '<li><a class="flex min-h-[44px] items-center rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 font-semibold text-slate-900 hover:bg-sky-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700" href="'
            + tool_href + '">' + html.escape(tool_name) + '</a></li>'
        )
    all_tools_menu = (
        '<details id="ca-all-tools-menu" class="mb-4 rounded-xl border border-slate-300 bg-white/95 shadow-sm dark:border-slate-700 dark:bg-stone-900/95">'
        '<summary class="flex min-h-[48px] cursor-pointer list-none items-center justify-between rounded-xl bg-slate-900 px-4 py-3 font-bold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-500 dark:bg-slate-100 dark:text-slate-950">'
        + ("مفت کیلکولیٹر منتخب کریں" if urdu else "Choose a free calculator")
        + '<span aria-hidden="true">⌄</span></summary>'
        '<div class="border-t border-slate-200 p-3 dark:border-slate-700">'
        '<ul class="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">' + all_tool_links + '</ul>'
        '</div></details>'
    )
    cats = ""
    if not urdu:
        for c in CATEGORIES:
            cats += ('<li><a class="rounded-full px-4 py-2 text-sm font-semibold min-h-[44px] inline-flex items-center '
                     + CAT_PILL[c["slug"]] + '" href="/' + c["slug"] + '/">' + c["name"] + "</a></li>")
        cats = '<nav aria-label="Categories" class="mt-8"><ul class="flex flex-wrap gap-3">' + cats + "</ul></nav>"
    side_title = "Designed for quick answers" if not urdu else "فوری جواب کے لیے آسان ڈیزائن"
    side_desc = "Clear buttons, readable results, and useful everyday tools in one place." if not urdu else "آسان بٹن، واضح نتائج اور روزمرہ کے مفید ٹولز ایک جگہ۔"
    calc_title = "Standard Calculator" if not urdu else "معیاری کیلکولیٹر"
    tool_intro = 'Choose a calculator, or browse the <a class="text-sky-800 dark:text-sky-300 underline" href="/free-online-calculators/">complete free online calculators guide</a>. You can also explore the <a class="text-sky-800 dark:text-sky-300 underline" href="/money/">Money and Business</a> and <a class="text-sky-800 dark:text-sky-300 underline" href="/math/">Math and Converters</a> hubs.' if not urdu else "شروع کرنے کے لیے کوئی ٹول منتخب کریں۔"
    free_label = "FREE TOOLS • PRIVATE BY DESIGN • NO SIGN-UP" if not urdu else "مفت ٹولز • نجی استعمال • سائن اپ نہیں"
    language_links = ""
    if not urdu:
        language_links = (
            '<nav aria-label="Other languages" class="mt-8">'
            '<h2 class="text-xl font-semibold">Other language versions</h2>'
            '<ul class="mt-3 flex flex-wrap gap-3">'
            '<li><a class="' + LINK + '" href="/ar/">العربية</a></li>'
            '<li><a class="' + LINK + '" href="/es/">Español</a></li>'
            '<li><a class="' + LINK + '" href="/fr/">Français</a></li>'
            '</ul></nav>'
        )
    hero_ui = CALC_UI
    if urdu:
        for en, ur in URDU["standard-calculator"]["labels"]:
            hero_ui = hero_ui.replace('aria-label="' + en + '"', 'aria-label="' + ur + '"')
        hero_ui = hero_ui.replace('>Scientific Mode</button>', '>سائنسی کیلکولیٹر</button>')
    hero = ('<section aria-label="' + ("کیلکولیٹر" if urdu else "Calculator") + '" class="ca-home-calculator"><div class="ca-home-card-heading"><span class="ca-home-kicker">' + calc_title + '</span>' + ('<a href="/ur/tasbih-counter/" aria-label="تسبیح کاؤنٹر کھولیں" style="display:inline-flex;align-items:center;justify-content:center;min-height:36px;padding:4px 12px;border-radius:9px;background:#0f766e;color:#fff;font-size:14px;font-weight:700;text-decoration:none;white-space:nowrap">📿 تسبیح کاؤنٹر</a>' if urdu else '<a href="/tasbih-counter/" aria-label="Open Tasbih Counter" style="display:inline-flex;align-items:center;justify-content:center;min-height:36px;padding:4px 12px;border-radius:9px;background:#0f766e;color:#fff;font-size:14px;font-weight:700;text-decoration:none;white-space:nowrap">📿 Tasbih Counter</a>') + '<span class="ca-home-live-dot" aria-hidden="true"></span></div>' + hero_ui + "</section>")
    body = (
        '<div class="ca-home-wrap">'
        '<div class="ca-home-header">'
        '<p class="ca-home-badge">' + free_label + '</p>'
        '<h1>' + h1 + '</h1>'
        '<p class="ca-home-lead">' + lead + '</p>'
        '</div>'
        '<div class="ca-home-layout">'
        '<aside class="ca-home-side ca-home-side-left">'
        '<span class="ca-home-side-icon" aria-hidden="true">✦</span>'
        '<p class="ca-home-side-eyebrow">' + s["confidence"] + '</p>'
        '<h2>' + side_title + '</h2>'
        '<p class="ca-home-side-copy">' + side_desc + '</p>'
        '<ul class="ca-home-benefits">'
        + ''.join('<li><span aria-hidden="true">✓</span>' + label + '</li>' for label in TRUST[lang])
        + '</ul><div class="ca-home-orbit" aria-hidden="true"><span>＋</span><span>÷</span><span>×</span><span>％</span></div>'
        '</aside>'
        + hero
        + '<aside id="all-tools" class="ca-home-tools">'
        + '<div class="ca-home-tools-heading"><div><p class="ca-home-side-eyebrow">' + s["many"] + '</p><h2>' + more_h + '</h2></div>' + tools_heading_action + '</div>'
        + all_tools_menu
        + '<p class="ca-home-tools-copy">' + tool_intro + '</p>'
        + '<ul class="ca-home-tool-grid">' + tiles + '</ul></aside>'
        '</div>'
        + cats
        + ('<nav aria-label="Related calculators" class="mt-8"><h2 class="text-xl font-semibold">Explore more calculators</h2><ul class="mt-3 grid gap-3"><li><a class="text-sky-800 dark:text-sky-300 underline" href="/percentage-calculator/">Percentage Calculator</a></li><li><a class="text-sky-800 dark:text-sky-300 underline" href="/fraction-calculator/">Fraction Calculator</a></li><li><a class="text-sky-800 dark:text-sky-300 underline" href="/compound-interest-calculator/">Compound Interest Calculator</a></li><li><a class="text-sky-800 dark:text-sky-300 underline" href="/date-calculator/">Date Difference Calculator</a></li></ul></nav>' if not urdu else '')
        + '<section class="ca-home-extra">' + home_extra_html(lang) + '</section>'
        + language_links
        + '</div>'
    )
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website", "name": "CalculatesAll", "url": SITE_URL + path, "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "WebApplication", "name": "Standard Calculator", "url": SITE_URL + path,
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "author": {"@id": SITE_URL + "/#maintainer"}, "publisher": {"@id": SITE_URL + "/#organization"},
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "Organization", "@id": SITE_URL + "/#organization", "name": "CalculatesAll", "url": SITE_URL + "/",
         "description": SITE_DESCRIPTION,
         "logo": SITE_URL + "/assets/favicon.svg",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "url": SITE_URL + "/contact/"}},
        {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/#maintainer", "name": "Muhammad Fayyaz Adeel", "url": SITE_URL + "/about/", "worksFor": {"@id": SITE_URL + "/#organization"}},
    ]
    write(path, head(title, desc, path, schema, lang=lang, alternates=home_alts_all()) + shell(body, lang=lang, current_path=path))


def not_found():
    body = ('<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">Page not found</h1>'
            '<p class="' + P + '">The page you asked for does not exist. Go to the <a class="' + LINK + '" href="/">home page</a> or choose a tool from the menu.</p>')
    doc = head("Page not found | CalculatesAll", "This page does not exist. Use the menu to choose a calculator, or go to the home page to start calculating.", "/404", [], noindex=True) + shell(body)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(fill(doc))


def sitemap(entries):
    items = ""
    for path, alts in entries:
        links = ""
        for code, href in alts:
            links += '    <xhtml:link rel="alternate" hreflang="' + code + '" href="' + SITE_URL + href + '"/>\n'
        items += ("  <url>\n    <loc>" + SITE_URL + path + "</loc>\n" + links + "  </url>\n")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + items + "</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def robots():
    text = "User-agent: *\nAllow: /\nDisallow: /404\n\nSitemap: " + SITE_URL + "/sitemap.xml\n"
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(text)


def og_and_favicon():
    import struct
    import zlib

    assets = os.path.join(OUT, "assets")
    os.makedirs(assets, exist_ok=True)
    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
               '<rect width="64" height="64" rx="12" fill="#0c4a6e"/>'
               '<text x="32" y="42" font-size="30" text-anchor="middle" fill="#ffffff" font-family="Arial, sans-serif" font-weight="bold">CA</text></svg>')
    with open(os.path.join(assets, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(favicon)

    # Generate a real 1200x630 PNG with Python's standard library only.
    # This avoids optional Pillow dependencies and works on a clean Vercel build.
    width, height = 1200, 630
    pixels = bytearray(width * height * 3)
    top, middle, bottom = (12, 74, 110), (49, 46, 129), (6, 95, 70)
    for y in range(height):
        if y < height // 2:
            t = y / (height // 2)
            a, b = top, middle
        else:
            t = (y - height // 2) / (height - height // 2)
            a, b = middle, bottom
        row_color = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
        start = y * width * 3
        for x in range(width):
            shift = int(5 * x / width)
            idx = start + x * 3
            pixels[idx] = min(255, row_color[0] + shift)
            pixels[idx + 1] = min(255, row_color[1] + shift)
            pixels[idx + 2] = min(255, row_color[2] + shift)

    def rect(x1, y1, x2, y2, color, outline=False):
        for y in range(max(0, y1), min(height, y2)):
            for x in range(max(0, x1), min(width, x2)):
                if outline and x not in (x1, x2 - 1) and y not in (y1, y2 - 1):
                    continue
                idx = (y * width + x) * 3
                pixels[idx:idx + 3] = bytes(color)

    font = {
        "A": ("01110","10001","10001","11111","10001","10001","10001"),
        "B": ("11110","10001","10001","11110","10001","10001","11110"),
        "C": ("01111","10000","10000","10000","10000","10000","01111"),
        "D": ("11110","10001","10001","10001","10001","10001","11110"),
        "E": ("11111","10000","10000","11110","10000","10000","11111"),
        "F": ("11111","10000","10000","11110","10000","10000","10000"),
        "G": ("01111","10000","10000","10111","10001","10001","01111"),
        "H": ("10001","10001","10001","11111","10001","10001","10001"),
        "I": ("11111","00100","00100","00100","00100","00100","11111"),
        "J": ("00111","00010","00010","00010","10010","10010","01100"),
        "K": ("10001","10010","10100","11000","10100","10010","10001"),
        "L": ("10000","10000","10000","10000","10000","10000","11111"),
        "M": ("10001","11011","10101","10101","10001","10001","10001"),
        "N": ("10001","11001","10101","10011","10001","10001","10001"),
        "O": ("01110","10001","10001","10001","10001","10001","01110"),
        "P": ("11110","10001","10001","11110","10000","10000","10000"),
        "Q": ("01110","10001","10001","10001","10101","10010","01101"),
        "R": ("11110","10001","10001","11110","10100","10010","10001"),
        "S": ("01111","10000","10000","01110","00001","00001","11110"),
        "T": ("11111","00100","00100","00100","00100","00100","00100"),
        "U": ("10001","10001","10001","10001","10001","10001","01110"),
        "V": ("10001","10001","10001","10001","10001","01010","00100"),
        "W": ("10001","10001","10001","10101","10101","10101","01010"),
        "X": ("10001","10001","01010","00100","01010","10001","10001"),
        "Y": ("10001","10001","01010","00100","00100","00100","00100"),
        "Z": ("11111","00001","00010","00100","01000","10000","11111"),
        "0": ("01110","10001","10011","10101","11001","10001","01110"),
        "1": ("00100","01100","00100","00100","00100","00100","01110"),
        "2": ("01110","10001","00001","00010","00100","01000","11111"),
        "3": ("11110","00001","00001","01110","00001","00001","11110"),
        "4": ("00010","00110","01010","10010","11111","00010","00010"),
        "5": ("11111","10000","10000","11110","00001","00001","11110"),
        "6": ("01110","10000","10000","11110","10001","10001","01110"),
        "7": ("11111","00001","00010","00100","01000","01000","01000"),
        "8": ("01110","10001","10001","01110","10001","10001","01110"),
        "9": ("01110","10001","10001","01111","00001","00001","01110"),
        "&": ("01100","10010","10100","01000","10101","10010","01101"),
        "|": ("00100","00100","00100","00100","00100","00100","00100"),
        "-": ("00000","00000","00000","11111","00000","00000","00000"),
        ".": ("00000","00000","00000","00000","00000","00110","00110"),
        ":": ("00000","00110","00110","00000","00110","00110","00000"),
    }

    def draw_text(x, y, text, scale, color):
        cursor = x
        for char in text.upper():
            if char == " ":
                cursor += 3 * scale
                continue
            pattern = font.get(char)
            if pattern:
                for py, line in enumerate(pattern):
                    for px, bit in enumerate(line):
                        if bit == "1":
                            rect(cursor + px * scale, y + py * scale,
                                 cursor + (px + 1) * scale, y + (py + 1) * scale, color)
            cursor += 6 * scale

    rect(70, 70, 1130, 560, (255, 255, 255), outline=True)
    rect(105, 110, 117, 500, (56, 189, 248))
    rect(117, 110, 121, 500, (52, 211, 153))
    draw_text(155, 185, "CALCULATESALL", 11, (255, 255, 255))
    draw_text(158, 305, "FREE ONLINE CALCULATORS", 5, (224, 242, 254))
    draw_text(158, 380, "ZAKAT | BMI | PROFIT & LOSS | AGE | DISCOUNT", 3, (209, 250, 229))
    draw_text(158, 430, "UNIT CONVERTER | STANDARD CALCULATOR", 3, (209, 250, 229))
    draw_text(158, 490, "FAST - FREE - BROWSER BASED", 2, (186, 230, 253))

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))

    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(pixels[y * stride:(y + 1) * stride])
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(os.path.join(assets, "og-image.png"), "wb") as f:
        f.write(png)

    # Keep an SVG copy for browsers that prefer vector previews.
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
           '<rect width="1200" height="630" fill="#0c4a6e"/>'
           '<text x="80" y="250" font-family="Arial, sans-serif" font-size="82" font-weight="700" fill="#ffffff">CalculatesAll</text>'
           '<text x="80" y="330" font-family="Arial, sans-serif" font-size="36" fill="#e0f2fe">Free online calculators</text></svg>')
    with open(os.path.join(assets, "og-image.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

def normalize_internal_page_links():
    """Use canonical trailing-slash URLs for links to generated pages."""
    import re
    from urllib.parse import urlsplit

    def normalize(match):
        quote, raw = match.group(1), match.group(2)
        parsed = urlsplit(raw)
        path = parsed.path
        if not path.startswith("/") or path == "/" or path.endswith("/"):
            return match.group(0)
        target = os.path.join(OUT, path.lstrip("/"), "index.html")
        if not os.path.isfile(target):
            return match.group(0)
        suffix = raw[len(path):]
        return "href=" + quote + path + "/" + suffix + quote

    for root, _, files in os.walk(OUT):
        for filename in files:
            if not filename.endswith(".html"):
                continue
            path = os.path.join(root, filename)
            with open(path, encoding="utf-8") as source:
                html = source.read()
            normalized = re.sub(r'href=(["\'])(/[^"\']*)\1', normalize, html)
            if normalized != html:
                with open(path, "w", encoding="utf-8") as target:
                    target.write(normalized)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    entries = []
    home_alts = home_alts_all()
    home_app_page("en")
    home_app_page("ur")
    for code in ["ar", "hi", "es", "fr"]:
        entries.append((home_lang_page(code), home_alts_all()))
    entries.append(("/", home_alts))
    entries.append(("/ur/", home_alts))
    for c in CATEGORIES:
        entries.append((category_page(c), []))
    for t in TOOLS:
        if t["slug"] == "calorie-calculator":
            from calorie_calculator import build_calorie_page
            path = build_calorie_page(head, shell, write)
        else:
            path = tool_page(t)
        if t["slug"] in URDU:
            alts = [("en", path), ("ur", "/ur" + path), ("x-default", path)]
            entries.append((path, alts))
            entries.append((urdu_tool_page(t), alts))
        else:
            entries.append((path, []))
    static_pages = [
        ("/about/", "About CalculatesAll | Project, Methods & Privacy", "Meet the maintainer of CalculatesAll, explore its free browser-based calculators, learn how methods are checked, and find privacy and contact details.", "About CalculatesAll", ABOUT_EXTRA),
        ("/privacy/", "Privacy Policy | CalculatesAll", "Read how CalculatesAll handles calculator inputs, local browser storage, advertising technologies, cookies and privacy choices.", "Privacy Policy", [
            "This policy explains what information CalculatesAll handles when you use the website. It applies to every page on calculateallinone.vercel.app.",
            "<strong>Calculator entries.</strong> The numbers and dates you type into a calculator are processed by JavaScript in your own browser. They are not sent to our server and we do not keep a copy of them.",
            "<strong>Data stored on your device.</strong> The tasbih counter saves your current count, chosen phrase and target in your browser's local storage, and the dark-mode setting is saved the same way. This information stays on your device. You can remove it at any time by clearing this site's data in your browser settings.",
            "<strong>No accounts or analytics.</strong> CalculatesAll does not offer user accounts, does not run its own analytics and does not sell personal information. Like most websites, our hosting provider (Vercel) may process technical request data such as IP address, browser type and the page requested in order to deliver and secure the site.",
            "<strong>Advertising and cookies.</strong> No Google AdSense ad units are currently displayed on CalculatesAll, and the site does not currently load the AdSense ad-serving script. The publisher ID and ads.txt seller record are present, but neither is an active ad unit. If advertising is enabled, the following applies: Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet. Google and its partners may also use web beacons, IP addresses and device identifiers to measure and protect advertising. Read <a class='underline text-sky-800 dark:text-sky-300' href='https://policies.google.com/technologies/partner-sites' target='_blank' rel='noopener noreferrer'>how Google uses information from sites that use its services</a> and the <a class='underline text-sky-800 dark:text-sky-300' href='https://policies.google.com/technologies/ads' target='_blank' rel='noopener noreferrer'>Google advertising technologies page</a>.",
            "<strong>Your choices.</strong> You can opt out of personalised advertising by visiting <a class='underline text-sky-800 dark:text-sky-300' href='https://adssettings.google.com/' target='_blank' rel='noopener noreferrer'>Google Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalised advertising at <a class='underline text-sky-800 dark:text-sky-300' href='https://www.aboutads.info/choices/' target='_blank' rel='noopener noreferrer'>www.aboutads.info</a>. Opting out stops personalised ads; you may still see non-personalised ads. You can also block or delete cookies in your browser settings.",
            "<strong>Visitors in the EEA, UK and Switzerland.</strong> Where the law requires it, you will be asked for consent through a Google-certified consent message before personalised advertising cookies are used, and you can change your choice later.",
            "<strong>Children.</strong> CalculatesAll is a general-audience website. It is not directed at children under 13 and we do not knowingly collect personal information from children.",
            "<strong>External links.</strong> Some pages link to official sources such as the World Health Organization or NIST. Those websites have their own privacy policies.",
            "<strong>Changes and contact.</strong> If this policy changes, the updated version will be published on this page. For privacy questions, email <a class='underline text-sky-800 dark:text-sky-300' href='mailto:" + CONTACT_EMAIL + "'>" + CONTACT_EMAIL + "</a>.",
        ]),
        ("/methodology/", "How Our Calculations Work | CalculatesAll", "Understand the formulas, worked examples, units, rounding conventions, input checks and limitations behind CalculatesAll calculators.", "How Our Calculations Work", [
            "This methodology explains how to interpret and check results from our calculators. A number is useful only when the input values, units, time period and calculation convention match the question being asked. Each calculator page remains the authoritative guide to that tool's exact formula, supported inputs and assumptions. If a tool page gives a more specific convention, follow that page rather than applying a general rule from this overview.",
            "Order of operations example: 8 + 3 × 4 = 20 because multiplication is performed before addition. With brackets, (8 + 3) × 4 = 44. When checking an expression, work through brackets first, then powers, then multiplication and division, then addition and subtraction. This prevents a common error where a correct formula is entered with the wrong grouping.",
            "Percentage example: 18% of 250 is 250 × 18 ÷ 100 = 45. To find what percentage 45 represents out of 250, calculate 45 ÷ 250 × 100 = 18%. Percentage change is a different question: (new value − starting value) ÷ starting value × 100. If the starting value is zero, percentage change is undefined. Always identify whether you need a percentage amount, a percentage share, a discount, a markup, a margin or a percentage change.",
            "Fraction example: 1/2 + 1/3 = 3/6 + 2/6 = 5/6. Addition and subtraction require a common denominator. Multiplication multiplies the numerators and denominators. Division multiplies by the reciprocal and cannot divide by a zero fraction. A fraction result may be shown in reduced form, as a mixed number or as a decimal. These are different displays of the same value when the conversion is exact.",
            "Discount example: an item priced at PKR 4,500 with a 20% discount has a discount amount of PKR 900 (4,500 × 0.20) and a discounted price of PKR 3,600 (4,500 − 900). This is the price before any separately applied tax, delivery charge or service fee. A displayed discount does not prove that a seller's original price was genuine.",
            "Profit example: if an item costs PKR 800 and sells for PKR 1,000, the gross profit is PKR 200 before overheads and other expenses. Markup on cost is 200 ÷ 800 × 100 = 25%. Gross margin on selling price is 200 ÷ 1,000 × 100 = 20%. Markup and margin are not interchangeable because they use different denominators. Net profit requires additional costs that may not be included in a simple calculator.",
            "Compound-interest estimates depend on the principal, rate, time and compounding frequency. For a single initial principal with a fixed nominal annual rate, the common periodic-compounding formula is A = P × (1 + r/n)^(n×t), where P is principal, r is the annual rate expressed as a decimal, n is the number of compounding periods per year and t is time in years. This model does not automatically include additional deposits, withdrawals, taxes, fees, changing rates or inflation unless the specific tool explicitly provides those inputs.",
            "Loan-payment estimates depend on the amount financed, interest rate, term, payment frequency and lender's rate convention. A calculator estimate is not a loan offer or a lender's amortisation statement. Actual payments can differ because of fees, insurance, taxes, variable rates, rounding, payment dates and lender-specific rules. Compare the estimate with the written terms supplied by the lender before making a financial commitment.",
            "Date example: from 28 February 2024 to 1 March 2024 there are 2 elapsed calendar days because 2024 includes 29 February. The same dates in 2025 are 1 elapsed day. Elapsed-day counts normally exclude the starting date. Inclusive counting, working days, public holidays, time-zone changes and legal deadline rules are separate conventions and should not be inferred from a simple calendar-day result.",
            "Unit conversion example: one inch is exactly 25.4 millimetres. To convert inches to millimetres, multiply by 25.4. To convert millimetres to inches, divide by 25.4. Temperature conversion is different because it includes an offset: Celsius to Fahrenheit is (°C × 9/5) + 32. Confirm that both selected units measure the same physical quantity before converting.",
            "Health calculation limits: adult BMI is calculated as weight in kilograms divided by height in metres squared. For example, 70 kg at 1.75 m gives 70 ÷ (1.75 × 1.75) = 22.86, approximately. BMI is a screening measure, not a diagnosis, and it does not directly measure body fat or individual health. Age, pregnancy, body composition and clinical context can affect interpretation. Seek qualified medical advice for personal decisions.",
            "Religious calculation limits: the Zakat calculator offers selectable silver and gold Nisab reference weights, including 612.36 grams of silver, 87.48 grams of gold and 85 grams of gold. These are alternative references, not one universal personal method. The page accepts a user-entered metal price and ISO currency, and applies the stated arithmetic only after the selected threshold and lunar-year conditions are confirmed. Rulings about eligible assets, debts, jewellery, business stock, agricultural wealth, pensions and the due date can differ by scholarly method and personal circumstances. Pakistan's PKR 503,529 source-deduction threshold is a separate, year-specific bank rule for 1446–1447 AH, not personal Nisab. Treat the result as an estimate based on the displayed assumptions and confirm a personal ruling with a qualified scholar.",
            "Rounding and precision: a displayed value may be rounded to make it easier to read. Rounding a final display is not the same as rounding every intermediate step. Where a calculation has several stages, retain sufficient precision through intermediate operations and round at the stage required by the relevant tool, institution or standard. Currency settlement, tax filings, engineering work and legal calculations may require rules that differ from a general online estimate.",
            "Input validation: inputs should be checked before a result is presented. Examples of invalid inputs include a zero denominator, division by zero, a date that does not exist, a negative physical length, a missing value, a non-finite number or incompatible units. Some tools also set practical input limits to prevent unsafe calculations or misleading output. If a tool rejects an input, check its supported range and units rather than trying to force a result.",
            "How we check tools: representative examples should be compared with independently calculated expected results. Boundary cases and invalid inputs should also be checked where applicable. Automated tests can detect regressions in formulas, page generation, required content and links, but passing tests does not mean every device, browser, language or real-world situation has been independently certified. We do not describe automated checks as professional certification.",
            "Privacy and browser processing: pages that describe calculations as browser-based perform the relevant calculation in the visitor's browser. The Privacy Policy explains technical data handled by the hosting, security, analytics or advertising services and any tool-specific local storage behaviour. Do not include passwords, account numbers or other sensitive personal information when reporting a problem.",
            "Reference sources and what they support: the " + '<a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" target="_blank" rel="noopener noreferrer">World Health Organization BMI and obesity guidance</a>' + " explains the adult BMI formula and why age-specific interpretation matters. The " + '<a class="' + LINK + '" href="https://www.nist.gov/pml/owm/si-units-length" target="_blank" rel="noopener noreferrer">National Institute of Standards and Technology length reference</a>' + " documents the exact inch-to-millimetre relationship. " + '<a class="' + LINK + '" href="https://openstax.org/books/precalculus-2e/pages/4-1-exponential-functions" target="_blank" rel="noopener noreferrer">OpenStax exponential functions</a>' + " explains the periodic compound-interest formula and worked examples. The " + '<a class="' + LINK + '" href="https://aa.usno.navy.mil/faq/leap_years" target="_blank" rel="noopener noreferrer">U.S. Naval Observatory leap-year guide</a>' + " describes the Gregorian leap-year rule. These references support the stated methods and do not endorse this website.",
            "Report a suspected error: email " + CONTACT_EMAIL + " with the calculator page URL, the exact input values and units, the result shown, the result you expected and the steps needed to reproduce the difference. For date or time issues, include the date format and time zone. A reproducible report helps us isolate whether the issue is a formula, input, display, browser or explanation problem. We investigate specific reports and correct confirmed errors.",
        ]),
        ("/editorial-policy/", "Editorial Policy | CalculatesAll", "Learn how CalculatesAll researches, checks, updates and corrects its calculator guides, formulas and reference information.", "Editorial Policy", [
            "Our purpose is to help visitors complete everyday calculations and understand what a result means. Calculator guides are designed around the task a visitor is trying to complete, not around a target word count. Where useful, a guide explains the required inputs, formula, worked example, assumptions, common mistakes and situations in which the result should not be relied on.",
            "The project maintainer is identified on the About and Terms pages. The maintainer is responsible for site operation, content updates and handling correction reports. This does not imply medical, legal, accounting, financial or religious credentials. We do not invent expert reviewers, author biographies, qualifications, testimonials or independent review claims.",
            "Calculation examples are selected so visitors can reproduce the arithmetic. Where a method depends on a recognised standard or an external authority, the relevant page should identify the source and explain which part of the method it supports. Sources are not presented as endorsing CalculatesAll unless the source has explicitly done so.",
            "Automated checks are used for representative calculations, invalid inputs, generated page structure, required explanatory content, internal links and metadata where the relevant test exists. Coverage differs between tools. A passing automated test is evidence for the cases tested, not proof that every possible input, browser, device or real-world use has been independently verified.",
            "Health and religious pages are general educational tools, not individual professional advice. Adult BMI is a screening measure and not a diagnosis. Zakat calculations follow the assumptions displayed by the relevant calculator and cannot settle every scholarly difference or personal circumstance. Visitors should consult a qualified professional or scholar for decisions that require individual judgement.",
            "We correct confirmed errors rather than silently changing a result without explanation. Please report the page URL, exact input values and units, result shown, expected result and steps to reproduce the issue to " + CONTACT_EMAIL + ". We investigate reproducible reports and update the relevant explanation or calculation when an error is confirmed.",
            "A last-updated date is shown only when a substantive page update is tracked. We do not add dates to imply freshness when no meaningful review or change has occurred. Page content, sources and examples are revisited when an issue is reported, a method changes or a material correction is needed.",
        ]),
        ("/terms/", "Terms of Use | CalculatesAll", "Read the terms for using CalculatesAll free calculators, including accuracy limits, professional-advice disclaimers and permitted use.", "Terms of Use", TERMS_PARAS),
        ("/affiliate-disclosure/", "Advertising Disclosure | CalculatesAll", "How CalculatesAll is funded, how advertising is labelled and why ads never change calculator results.", "Advertising and Affiliate Disclosure", [
            "CalculatesAll is free to use. The site may be supported by advertising served by Google AdSense. Ads are shown in clearly separated areas and are never disguised as calculator results, buttons or navigation.",
            "CalculatesAll does not currently use affiliate links. If affiliate links are added in the future, they will be clearly labelled next to the link and explained on this page.",
            "Advertising does not influence how any tool works. Formulas, worked examples and results are the same for every visitor, and advertisers cannot pay to change them.",
            "We do not publish paid reviews, invented ratings or sponsored content presented as editorial content.",
            "An advertisement is not an endorsement by CalculatesAll. We do not control the advertiser, its offer or the destination page, so review third-party terms before taking action.",
            'For information about advertising cookies and privacy choices, read the <a class="underline text-sky-800 dark:text-sky-300" href="/privacy/">Privacy Policy</a>. Any future affiliate relationship will be disclosed before or beside the relevant link.',
            'Questions about this disclosure can be sent to <a class="underline text-sky-800 dark:text-sky-300" href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a>.',
        ]),
        ("/contact/", "Contact CalculatesAll", "Contact CalculatesAll for corrections, feedback or questions about any calculator. We read every message and publish confirmed corrections on the tool page.", "Contact", [
            'For corrections, feedback, accessibility problems, Urdu translation fixes or questions about a calculator, email <a class="' + LINK + '" href="mailto:' + html.escape(CONTACT_EMAIL, quote=True) + '">' + html.escape(CONTACT_EMAIL) + '</a>.',
            "To help us reproduce a calculation issue, identify the calculator and include its full page URL, the exact input values and units you entered, the result displayed, and the result you expected. If the issue depends on a particular sequence, describe the steps and options you selected. You can also include the source or formula that supports the expected result.",
            "We read every message. A report with specific inputs, units and an expected result gives us something that can be checked. A general statement that a result looks wrong may not provide enough information to reproduce the issue, and we may need more details before we can confirm it.",
            'When a formula or content error is confirmed, we correct the affected tool page and retest the calculator before publishing the update. The <a class="' + LINK + '" href="/editorial-policy/">Editorial Policy</a> explains the correction process. For information about personal information and site data, read the <a class="' + LINK + '" href="/privacy/">Privacy Policy</a>. Please do not send passwords, payment details, medical records or other sensitive personal information. We do not promise a fixed response time.',
        ]),
    ]
    for path, title, desc, h1, paras in static_pages:
        # Keep these trust pages focused: avoid repeating material from older content layers.
        if path == "/contact/":
            desc = "Contact CalculatesAll to report a calculator error, accessibility issue or translation problem. Include the page URL, inputs and expected result for review."
            paras = [
                'For corrections, feedback, accessibility problems or translation issues, email <a class="' + LINK + '" href="mailto:' + html.escape(CONTACT_EMAIL, quote=True) + '">' + html.escape(CONTACT_EMAIL) + '</a>.',
                "To report a calculation error, include the calculator name, page URL, exact input values, displayed result, expected result and steps to reproduce the issue. For date or time calculations, include the date format and time zone if relevant.",
                "Do not email passwords, payment card numbers, bank details, medical records or other sensitive personal information. Calculator entries remain in your browser. We only receive details you choose to include in your message.",
                'For formula methods, read the <a class="' + LINK + '" href="/methodology/">calculation methodology</a>. For the correction process, read the <a class="' + LINK + '" href="/editorial-policy/">editorial policy</a>. For data handling, read the <a class="' + LINK + '" href="/privacy/">privacy policy</a>.',
            ]
            paras = paras + CONTACT_EXTRA
        elif path == "/editorial-policy/":
            paras = [
                "Calculator guides describe the inputs, method, worked examples where helpful, common mistakes and limitations. Each worked example states its calculation so readers can repeat it. Guides are designed around the visitor task, not around a target word count.",
                "The project maintainer is identified on the About and Terms pages. This identifies responsibility for site operation and corrections, but does not imply medical, legal, accounting, financial or religious credentials. We do not invent expert reviewers, author biographies, qualifications, testimonials or independent review claims.",
                "We prefer official or primary references for factual claims. Health information is general guidance, not a diagnosis; Zakat calculations state their method and do not replace a qualified scholar's ruling.",
                "Page reviews and expert endorsements are identified only when they have actually taken place. Update dates reflect tracked substantive changes.",
                "Quality checks cover representative inputs and boundaries, generated pages, titles, descriptions, canonical URLs, structured data, sitemap entries and internal links. They reduce regression risk but cannot cover every browser or situation.",
                "To request a correction, send the page URL, inputs, displayed result and expected result or source. Confirmed issues are investigated and corrected, with relevant checks before publication.",
                "A guide distinguishes facts, assumptions and examples. A worked example illustrates a particular set of inputs; it is not a prediction or a guarantee that the same answer applies to every visitor.",
                "Financial tools specify the base of each percentage and do not silently include fees, taxes or other costs that the visitor has not entered. Users should review the displayed assumptions before using a result for a decision.",
                "Date and conversion tools describe their units and conventions. A month is not treated as a constant number of days, and temperature conversions account for the different zero points of the scales.",
                "Medical screening content identifies the population for which a formula is intended and makes clear that a calculator cannot replace clinical evaluation. Religious guidance states the calculation approach without presenting a numerical output as a personal ruling.",
                "Editorial changes should be checked for factual accuracy, accessibility and readability on small screens. Technical checks examine navigation, generated links, language versions and structured data where applicable.",
                "A passing automated test is evidence for the cases tested, not proof that every possible input, browser, device or real-world situation has been independently verified. Browser behavior, accessibility and calculations can still require manual review, especially when a new feature or formula is introduced.",
                "When a source is revised or a reported issue is confirmed, the relevant explanation and any affected example should be updated together. We avoid adding unsupported claims about external expert approval or the date of a review.",
                "Visitors can independently reproduce many examples with the inputs and methods shown. Reports that include the page URL, exact input values and units, displayed result, expected result and steps to reproduce the issue are more actionable than a general statement that a result looks wrong. Please send correction reports to " + CONTACT_EMAIL + ".",
            ]
        elif path == "/affiliate-disclosure/":
            paras = [
                "CalculatesAll is free to use. Advertising is not enabled on the site at present. No AdSense ad units are currently displayed, and the site does not currently load the AdSense ad-serving script. A publisher ID and ads.txt seller record are present, but neither is an active ad unit. If advertising is enabled in the future, it will be clearly separated from calculator results, buttons and navigation.",
                "CalculatesAll does not currently have active affiliate links. Any third-party marketplace links are ordinary information or sign-up links, not affiliate links, and no commission tracking is active by default. No visitor should treat an ordinary marketplace link as an endorsement or an affiliate recommendation.",
                "AdSense ad serving will be enabled only after any required Google site or account approval, a valid ad-unit ID, applicable consent requirements and policy checks are complete. The site will not use placeholder publisher IDs or invented ad-slot IDs.",
                "Advertising does not determine calculator formulas, worked examples or results. The same calculation method applies regardless of advertising. We do not publish paid reviews, invented ratings or sponsored content presented as independent editorial content.",
                "An advertisement is not an endorsement by CalculatesAll. Advertisers and their partners control their own offers and destination pages, so visitors should review third-party terms before taking action. The Privacy Policy explains how advertising cookies and privacy choices are addressed if advertising is introduced.",
                "If a genuine affiliate relationship is introduced later, it will be clearly labelled beside the relevant link and explained on this page before or when visitors use it. Until then, no affiliate links or commission-based tracking are active.",
                'Questions about this disclosure can be sent to <a class="underline text-sky-800 dark:text-sky-300" href="mailto:' + html.escape(CONTACT_EMAIL, quote=True) + '">' + html.escape(CONTACT_EMAIL) + '</a>.',
            ]
        elif path == "/about/":
            # ABOUT_EXTRA is already supplied by the About page definition above.
            pass
        else:
            paras = paras + TRUST_EXTRA.get(path.rstrip("/") if path.rstrip("/") in TRUST_EXTRA else path, []) + {"/contact/": CONTACT_EXTRA}.get(path, [])
        static_page(path, title, desc, h1, paras)
        entries.append((path, []))
    from extra_calculator_pages import build_extra_pages
    entries.extend(build_extra_pages(head, shell, write))
    from hub_page import build_hub_page
    entries.extend(build_hub_page(head, shell, write))
    entries.append(("/emi-calculator/", []))
    not_found()
    normalize_internal_page_links()
    og_and_favicon()
    sitemap(entries)
    robots()
    shutil.copytree(STATIC, os.path.join(OUT, "assets"), dirs_exist_ok=True)
    # Publish the standalone EMI calculator through the generated-page pipeline.
    emi_source = "emi-calculator.html"
    if not os.path.isfile(emi_source):
        raise SystemExit("Required emi-calculator.html source file is missing")
    emi_output = os.path.join(OUT, "emi-calculator")
    os.makedirs(emi_output, exist_ok=True)
    with open(emi_source, encoding="utf-8") as f:
        emi_html = f.read()
    if ADSENSE_CLIENT and 'name="google-adsense-account"' not in emi_html:
        emi_html = emi_html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="google-adsense-account" content="' + html.escape(ADSENSE_CLIENT, quote=True) + '">', 1)
    with open(os.path.join(emi_output, "index.html"), "w", encoding="utf-8") as f:
        f.write(emi_html)
    # Preserve the Google Search Console HTML ownership token in Vercel output.
    # The repo root is not deployed because Vercel publishes only the public/ directory.
    google_verification = "google2e764d068684499b.html"
    if os.path.isfile(google_verification):
        shutil.copy2(google_verification, os.path.join(OUT, google_verification))
    # Preserve the IndexNow key as a root-level static asset in the deployed output.
    indexnow_key = "c07ad49659854199b740dc06dbd825a5.txt"
    if os.path.isfile(indexnow_key):
        shutil.copy2(indexnow_key, os.path.join(OUT, indexnow_key))
    llms_source = "llms.txt"
    if os.path.isfile(llms_source):
        shutil.copy2(llms_source, os.path.join(OUT, llms_source))
    configured = write_ads_txt()
    print("ads.txt " + ("configured from ADSENSE_CLIENT" if configured else "not generated until a real ADSENSE_CLIENT is configured"))
    print("translation review rows: " + str(write_review_sheet()))
    verify_csp_hashes()
    print("Generated " + str(len(entries)) + " page routes into " + OUT + " before SEO indexability filtering")


def verify_csp_hashes():
    import glob
    import hashlib
    import base64
    import re as _re
    cfg = json.load(open("vercel.json", encoding="utf-8"))
    csp = ""
    for h in cfg["headers"][0]["headers"]:
        if h["key"] == "Content-Security-Policy":
            csp = h["value"]
    for p in glob.glob(OUT + "/**/*.html", recursive=True):
        raw = open(p, encoding="utf-8").read()
        for body in _re.findall(r'<script(?![^>]*src=)(?![^>]*type="application/ld\+json")[^>]*>(.*?)</script>', raw, _re.S):
            digest = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode()
            if ("'sha256-" + digest + "'") not in csp:
                raise SystemExit("CSP hash missing for an inline script in " + p + ". Update vercel.json with sha256-" + digest)
    print("CSP inline script hashes verified")



if __name__ == "__main__":
    main()
