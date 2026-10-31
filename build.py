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
# No page-specific substantive update dates are currently verified.
LASTMOD = {}
OUT = "public"
STATIC = "static"

L = "block text-base font-medium text-stone-800 dark:text-stone-200 mb-1"
I = "w-full rounded-lg border border-stone-400 dark:border-stone-400 bg-white dark:bg-stone-900 px-3 py-3 text-base min-h-[44px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
B = "bg-gradient-to-r from-sky-700 to-indigo-700 hover:from-sky-800 hover:to-indigo-800 text-white text-base font-semibold px-5 py-3 rounded-xl min-h-[44px] shadow-md focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
S = "border border-stone-500 dark:border-stone-400 text-stone-900 dark:text-stone-100 text-base font-medium px-5 py-3 rounded-lg min-h-[44px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
R = "mt-6 rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5 text-base leading-relaxed min-h-[3rem]"
H2 = "text-2xl font-bold text-indigo-800 dark:text-indigo-200 mt-12"
P = "mt-3 text-base leading-relaxed text-stone-800 dark:text-stone-200"
LINK = "underline text-sky-800 dark:text-sky-300 hover:text-sky-950"


def field(fid, label, step="0.01", hint=""):
    h = ""
    if hint:
        h = '<p class="text-sm text-stone-700 dark:text-stone-300 mt-1">' + hint + "</p>"
    return ('<div><label class="@L@" for="' + fid + '">' + label + '</label>'
            '<input id="' + fid + '" name="' + fid + '" class="@I@" type="number" min="0" step="' + step + '" inputmode="decimal">' + h + "</div>")


def check(fid, label):
    return ('<label class="flex items-start gap-3 text-base text-stone-900 dark:text-stone-100 min-h-[44px]">'
            '<input id="' + fid + '" type="checkbox" class="mt-1 h-5 w-5"> <span>' + label + "</span></label>")


def result(rid):
    return '<div id="' + rid + '" class="@R@" aria-live="polite"></div>'


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
        "description": "Calculate Zakat at 2.5 percent on net wealth with a silver Nisab check and lunar year (hawl) confirmation.",
        "h1": "Zakat Calculator with Nisab Check",
        "lead": "Enter your savings and assets, then the silver price per gram. The calculator checks Nisab first and shows a Zakat amount only after the Nisab and lunar year conditions are confirmed.",
        "ui": (
            '<form id="zakat-form" class="space-y-5" novalidate>'
            '<div class="grid sm:grid-cols-2 gap-4">'
            + field("z-cash", "Cash / savings")
            + field("z-gold", "Gold value")
            + field("z-silver", "Silver value")
            + field("z-stock", "Stock for sale")
            + field("z-recv", "Expected receivables")
            + field("z-debts", "Debts due now")
            + "</div>"
            + field("z-silverprice", "Silver price per gram", hint="Required to check Nisab. Without it, no Zakat amount is shown.")
            + check("z-hawl", "Held for one full lunar year (hawl)")
            + '<button type="submit" class="@B@">Calculate Zakat</button></form>'
            + result("zakat-result")
        ),
        "guide": [
            ("What Zakat is", [
                "Zakat is 2.5 percent of net zakatable wealth. It is due when wealth is at or above Nisab and has been held for one full lunar year (hawl).",
            ]),
            ("Step by step", [
                "Step 1. Add cash, bank savings, gold, silver, business goods for sale and money owed to you that you expect to receive.",
                "Step 2. Subtract debts due now. If the result is below zero, use zero.",
                "Step 3. Nisab is 612.36 grams of silver. Multiply 612.36 by the silver price per gram you entered.",
                "Step 4. If net wealth is below Nisab, no Zakat is due. If it is above Nisab and the lunar year is complete, Zakat equals net wealth multiplied by 0.025.",
            ]),
            ("Worked example", [
                "Cash and bank savings are 1,000,000. Debts due now are 100,000. Net wealth is 900,000.",
                "Silver price is 1,000 per gram. Nisab is 612.36 multiplied by 1,000, which is 612,360.",
                "Net wealth of 900,000 is above Nisab. If one lunar year is complete, Zakat is 900,000 multiplied by 0.025, which is 22,500.",
            ]),
            ("Common mistakes", [
                "Using the gold Nisab (87.48 grams) when the silver Nisab applies, or the reverse. This tool uses silver, which is the lower threshold and the more cautious choice for most people.",
                "Forgetting that the lunar year counts from when the wealth reached Nisab, not from the start of the calendar year.",
                "Counting personal items that are not held for trade. Rules on personal jewelry and some debts differ between scholars.",
            ]),
            ("Limits of this tool", [
                "This tool follows the common silver Nisab method. Rulings on jewelry, property held for rent, loans to others and debts can differ between legal schools. Confirm your figures with a qualified scholar before you pay.",
            ]),
        ],
        "faq": [
            ("What is Nisab for silver?", "The Nisab used on this page is 612.36 grams of silver. Its money value depends on the silver price you enter."),
            ("Why does the calculator not show an amount?", "It needs the silver price to check Nisab, and it needs you to confirm the lunar year. The Zakat amount appears only after both conditions are met."),
            ("Is this a religious ruling?", "No. It is a calculation tool. For a ruling on your situation, consult a qualified scholar."),
        ],
        "sources": "Method based on the silver Nisab of 612.36 grams, which is widely used in South Asian Zakat guidance. Rules differ between schools of law.",
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
        "sources": "Adult BMI categories follow the World Health Organization classification. The calculation uses the standard BMI formula.",
    },
    {
        "slug": "profit-loss-calculator",
        "category": "money",
        "name": "Profit and Loss Calculator",
        "app": "UtilitiesApplication",
        "description": "Free profit and loss calculator: calculate business net profit, profit margin, product profit percentage and markup from revenue, costs and selling price.",
        "h1": "Profit and Loss Calculator for Business and Products",
        "lead": "A profit and loss calculator estimates business profit or loss from revenue, costs and expenses, or product profit from cost and selling price. Choose the calculation type to see the correct percentage basis.",
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
        "sources": 'Formula references: <a class="' + LINK + '" href="https://openstax.org/books/principles-finance/pages/5-1-the-income-statement" target="_blank" rel="noopener noreferrer">OpenStax Principles of Finance: The Income Statement</a> explains gross profit, operating income and margin. <a class="' + LINK + '" href="https://www.accaglobal.com/gb/en/student/exam-support-resources/fundamentals-exams-study-resources/f2/technical-articles/ratio-analysis.html" target="_blank" rel="noopener noreferrer">ACCA Ratio Analysis</a> explains gross and operating profit margin ratios. This calculator is a simplified estimate, not a formal financial statement.',
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
                "Final price equals original price minus amount saved.",
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
        ],
        "faq": [
            ("Why is a negative weight rejected?", "A physical weight or length cannot be negative. Temperature in Celsius and Fahrenheit can be negative."),
            ("Why is Kelvin rejected below zero?", "Zero Kelvin is absolute zero. No temperature can be lower."),
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
        "lead": "A free digital tasbeeh counter for daily dhikr. Choose a phrase, set a target, and keep your count on this device without downloading an app.",
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
            '<p id="t-storage-note" class="text-sm text-amber-800 dark:text-amber-200" role="status" hidden>Saving is unavailable in this browser. Your count is kept in memory until you leave or reload this page.</p>'
            '<button id="t-tap" type="button" aria-label="Count one" class="w-full min-h-[64px] @B@ text-xl">Count one</button>'
            '<div class="grid grid-cols-2 gap-3"><button id="t-undo" type="button" class="@S@">Undo</button>'
            '<button id="t-reset" type="button" class="@S@">Reset</button></div>'
            '<p class="text-sm text-stone-700 dark:text-stone-300"><span id="t-lifetime-label">Lifetime counted total:</span><output id="t-lifetime">0</output></p>'
            '<p class="text-sm text-stone-700 dark:text-stone-300">Keyboard: press Space or Enter to count when focus is not in a text field or control.</p>'
            '</div>'
        ),
        "guide": [
            ("What is tasbih?", [
                "Tasbih is a word used for remembrance of Allah and devotional phrases. This page is a counting aid, not a religious authority, and it does not decide which phrase or number a person should choose.",
                "The counter records button presses. It cannot verify that a phrase was recited, detect a missed count, or determine whether a practice is required. Use it in the way that fits your own practice, and ask a qualified scholar or trusted teacher about religious rulings.",
            ]),
            ("How to use this online tasbih counter", [
                "Choose one of the five preset phrases or select Custom phrase and enter up to 40 characters. Choose a target of 33, 99, or 100, or select Custom target and enter a whole number from 1 to 10,000. The custom target field accepts digits only. A value outside the allowed range or a decimal is rejected with an error message.",
                "Press Count one once for each count you want to record. You can also press Space or Enter when focus is not inside another control or text field. The progress message shows how many counts remain. When the selected target is reached, the page displays a message and may briefly vibrate if your device and browser support vibration.",
                "Undo subtracts one from the current count when the count is above zero. Reset asks for confirmation before clearing the current count. The lifetime total tracks accepted count taps and is kept separately from the current session count. The phrase and current count are saved in this browser when storage is available.",
            ]),
            ("Five phrases and plain meanings", [
                "SubhanAllah is commonly translated as “Glory be to Allah.” This is a plain-language meaning, not a detailed commentary.",
                "Alhamdulillah is commonly translated as “Praise belongs to Allah” or “All praise is due to Allah.”",
                "Allahu Akbar is commonly translated as “Allah is greater” or “Allah is the Greatest.”",
                "Astaghfirullah means “I seek forgiveness from Allah.”",
                "La ilaha illallah means “There is no deity worthy of worship except Allah.” Transliteration and English wording can vary; consult a qualified teacher if you need a formal translation or pronunciation guidance.",
            ]),
            ("Saving, privacy, and limitations", [
                "The counter uses local browser storage on your device. It does not need an account and does not send the count to a server. Browser privacy settings, private browsing, clearing site data, or switching devices can make saved values unavailable. If storage is blocked, the counter continues in memory and displays a note, but values may be lost when you reload or leave the page.",
                "A target is only a personal tracking setting in this tool. The page does not claim that a specific number is required or that using a digital counter has a particular religious reward. It does not replace prayer beads, finger counting, personal judgement, or guidance from a qualified scholar.",
            ]),
        ],
        "faq": [
            ("Is the count saved on a server?", "No. It is saved only in this browser."),
            ("What happens when I reach the target?", "The counter shows that the target is reached. Press Reset to start again."),
        ],
        "sources": "Tasbih counts are recorded on the device only.",
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
        "intro": "These tools cover common money questions: how to estimate a loan's monthly EMI and repayment interest, how much Zakat is due, whether a sale made a profit or loss, and how much a discount saves. Each calculator explains its method and assumptions, so you can check the result yourself.",
        "faq": [
            ("What does the EMI calculator estimate?", "It estimates the monthly installment, total interest and repayment schedule from the loan amount, annual rate and term. Lender fees and contract-specific charges can change the amount quoted by a lender."),
            ("Are these tools accurate for business accounts?", "They calculate the arithmetic correctly for the inputs you give. They do not replace an accountant, and tax rules are not included."),
            ("Does the Zakat calculator give a religious ruling?", "No. It applies the silver Nisab method and shows the rules it uses. For a ruling on your situation, consult a qualified scholar."),
        ],
    },
    "health": {
        "intro": "The health tools on CalculatesAll give screening numbers, not diagnoses. The BMI calculator uses the standard formula and the World Health Organization adult weight categories, in metric or imperial units.",
        "faq": [
            ("Should I use BMI to decide if I am healthy?", "BMI is one screening measure. It does not show body fat or fitness directly. Discuss your result with a doctor or health professional."),
        ],
    },
    "time": {
        "intro": "Date and time tools help you measure exact age in years, months and days, and time an activity with a browser stopwatch. Age is calculated from calendar dates, so the time of day does not change the result.",
        "faq": [
            ("Does the age calculator use my time zone?", "No. It compares calendar dates only."),
        ],
    },
    "math": {
        "intro": "Math and converter tools cover everyday arithmetic and unit conversion. The unit converter uses fixed conversion factors for weight, length and temperature, and rejects values that cannot exist in the physical world.",
        "faq": [
            ("Does the standard calculator run on a server?", "No. All arithmetic runs in your browser, and your numbers are not sent anywhere."),
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
    {"slug": "money", "name": "Money and Business", "desc": "Money calculators for EMI, Zakat, profit and loss, and discounts, with worked examples and clear limits for everyday decisions."},
    {"slug": "health", "name": "Health", "desc": "Calculate adult BMI in metric or imperial units, review WHO weight categories, and understand what the screening result cannot tell you."},
    {"slug": "time", "name": "Date and Time", "desc": "Calculate age in years, months and days, and use a browser stopwatch for everyday timing with clear notes about date and timing limits."},
    {"slug": "math", "name": "Math and Converters", "desc": "Use a standard calculator and convert weight, length and temperature with validation for invalid or physically impossible values."},
    {"slug": "worship", "name": "Worship and Daily Use", "desc": "Use a private browser-based tasbih counter for dhikr, with target tracking and local-only count storage on your device."},
]

URDU = {
    "zakat-calculator": {
        "name": "زکوٰۃ کیلکولیٹر",
        "title": "نصاب چیک کے ساتھ زکوٰۃ کیلکولیٹر | CalculatesAll",
        "description": "چاندی کے نصاب کے ساتھ خالص مال پر 2.5 فیصد زکوٰۃ کا حساب کریں اور قمری سال مکمل ہونے کی تصدیق کریں۔",
        "h1": "نصاب چیک کے ساتھ زکوٰۃ کیلکولیٹر",
        "lead": "اپنی بچت اور اثاثے درج کریں، پھر چاندی کی فی گرام قیمت لکھیں۔ کیلکولیٹر پہلے نصاب چیک کرتا ہے اور زکوٰۃ کی رقم اسی وقت دکھاتا ہے جب نصاب اور قمری سال کی شرط پوری ہو۔",
        "labels": [
            ("Cash / savings", "نقد اور بینک بچت"),
            ("Gold value", "سونے کی قیمت"),
            ("Silver value", "چاندی کی قیمت"),
            ("Stock for sale", "فروخت کا کاروباری مال"),
            ("Expected receivables", "وصول ہونے والی رقم"),
            ("Debts due now", "موجودہ واجب الادا قرض"),
            ("Silver price per gram", "چاندی کی فی گرام قیمت"),
            ("Held for one full lunar year (hawl)", "یہ مال ایک مکمل قمری سال (حول) تک رکھا گیا ہے"),
            ("Calculate Zakat", "زکوٰۃ کا حساب کریں"),
            ("Required to check Nisab. Without it, no Zakat amount is shown.", "نصاب چیک کرنے کے لیے ضروری ہے۔ اس کے بغیر زکوٰۃ کی رقم نہیں دکھائی جائے گی۔"),
        ],
        "how_heading": "حساب کا طریقہ",
        "faq_heading": "سوالات",
        "how": [
            "زکوٰۃ خالص قابلِ زکوٰۃ مال کا 2.5 فیصد ہے۔ یہ اس وقت واجب ہوتی ہے جب مال نصاب کے برابر یا اس سے زیادہ ہو اور ایک مکمل قمری سال تک رکھا گیا ہو۔",
            "پہلے نقد، بینک بچت، سونا، چاندی، فروخت کے سامان اور وصول ہونے والی رقم کو جمع کریں۔ پھر ابھی واجب الادا قرض منہا کریں۔",
            "چاندی کا نصاب 612.36 گرام ہے۔ اس کو فی گرام قیمت سے ضرب دیں۔ اگر خالص مال نصاب سے کم ہو تو زکوٰۃ واجب نہیں۔",
            "مثال: نقد 1,000,000 ہے اور قرض 100,000 ہے تو خالص مال 900,000 ہوگا۔ چاندی 1,000 فی گرام ہو تو نصاب 612,360 ہوگا۔ قمری سال مکمل ہونے پر زکوٰۃ 900,000 کا 2.5 فیصد، یعنی 22,500 ہوگی۔",
            "زیورات، کرایے کی جائیداد اور قرض کے بعض معاملات میں فقہاء کی آراء مختلف ہیں۔ ادائیگی سے پہلے کسی مستند عالم سے تصدیق کریں۔",
        ],
        "faq": [
            ("چاندی کا نصاب کیا ہے؟", "اس صفحے پر نصاب 612.36 گرام چاندی ہے۔ اس کی رقمی قیمت آپ کی درج کردہ چاندی کی قیمت پر ہے۔"),
            ("کیلکولیٹر رقم کیوں نہیں دکھاتا؟", "نصاب چیک کرنے کے لیے چاندی کی قیمت اور قمری سال کی تصدیق دونوں ضروری ہیں۔"),
            ("کیا یہ شرعی فتویٰ ہے؟", "نہیں۔ یہ حساب کا ایک آلہ ہے۔ اپنے معاملے کے فتوے کے لیے کسی مستند عالم سے رجوع کریں۔"),
        ],
    },
    "bmi-calculator": {
        "name": "BMI کیلکولیٹر",
        "title": "بالغوں کے لیے BMI کیلکولیٹر | CalculatesAll",
        "description": "کلوگرام یا پاؤنڈ وزن اور سینٹی میٹر یا فٹ و انچ قد سے بالغوں کا BMI نکالیں، درجہ بندی اور حدود سمجھیں۔",
        "h1": "بالغوں کے لیے BMI کیلکولیٹر",
        "lead": "وزن کے لیے کلوگرام یا پاؤنڈ اور قد کے لیے سینٹی میٹر یا فٹ اور انچ منتخب کریں۔ یہ کیلکولیٹر بالغوں کے لیے ہے۔",
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
        "faq_heading": "عام سوالات",
        "how": [
            "بالغوں کا باڈی ماس انڈیکس (BMI) نکالنے کے لیے وزن کلوگرام میں اور قد میٹر میں درکار ہوتا ہے۔ فارمولا یہ ہے: BMI = وزن (کلوگرام) ÷ قد (میٹر)²۔ اگر قد سینٹی میٹر میں ہو تو اسے 100 پر تقسیم کر کے میٹر میں تبدیل کریں۔",
            "اگر قد فٹ اور انچ میں درج کریں تو پہلے کل انچ نکالیں: (فٹ × 12) + انچ۔ پھر کل انچ کو 2.54 سے ضرب دے کر سینٹی میٹر حاصل کریں۔ وزن کلوگرام یا پاؤنڈ میں منتخب کیا جا سکتا ہے؛ پاؤنڈ کو حساب سے پہلے کلوگرام میں تبدیل کیا جاتا ہے۔",
            "بالغوں کے لیے WHO کی عام درجہ بندی میں 18.5 سے کم BMI کم وزن، 18.5 سے 25 سے کم معمول کا وزن، 25 سے 30 سے کم زیادہ وزن، اور 30 یا اس سے زیادہ موٹاپے کی حد ہے۔ یہ کیلکولیٹر پہلے BMI کو ایک اعشاری جگہ تک گول کرتا ہے، پھر اسی دکھائی گئی قدر کے مطابق درجہ منتخب کرتا ہے۔",
            "مثال کے طور پر 70 کلوگرام وزن اور 170 سینٹی میٹر قد پر حساب 70 ÷ (1.70 × 1.70) ہے۔ نتیجہ تقریباً 24.2 بنتا ہے، جو بالغوں میں معمول کے وزن کی حد میں آتا ہے۔ اگر قد 5 فٹ 7 انچ ہو تو یہ 67 انچ یا 170.18 سینٹی میٹر بنتا ہے۔",
            "BMI جسمانی چربی کو براہ راست نہیں ناپتا اور نہ یہ بتاتا ہے کہ چربی جسم میں کہاں موجود ہے۔ زیادہ عضلات رکھنے والے افراد کا BMI بلند ہو سکتا ہے، اس لیے ایک جیسا BMI دو افراد میں ایک جیسی جسمانی ساخت یا صحت کی نشاندہی نہیں کرتا۔",
            "بچوں اور نوعمروں کے لیے یہ بالغوں والی درجہ بندی استعمال نہیں کرنی چاہیے۔ ان کی جانچ عمر اور جنس کے مطابق BMI-for-age گروتھ چارٹس سے کی جاتی ہے۔ حمل کے دوران بھی BMI کو خاص سیاق میں سمجھنا ضروری ہے۔ بعض بڑی عمر کے افراد یا جسم میں پانی جمع ہونے، بیماری یا عضلات کم ہونے کی صورتوں میں BMI محدود معلومات دے سکتا ہے۔",
            "نتیجے کو صرف عمومی اسکریننگ معلومات سمجھیں، مکمل طبی جانچ نہیں۔ معالج وزن کے ساتھ کمر کا گھیر، بلڈ پریشر، خون کے ٹیسٹ، ادویات، طبی تاریخ، خوراک اور جسمانی سرگرمی بھی دیکھ سکتا ہے۔ اگر وزن تیزی سے بدلے، علامات ہوں، کوئی بیماری ہو یا آپ کو ذاتی مشورہ چاہیے تو مستند ڈاکٹر سے بات کریں۔",
            "یہ ٹول قد کی حد سینٹی میٹر میں 50 سے 260، یا فٹ میں 1 سے 8 اور انچ میں 0 سے 11.99 قبول کرتا ہے۔ وزن کی حد 20 سے 300 کلوگرام یا 44.1 سے 661.3 پاؤنڈ ہے۔ یہ صرف کیلکولیٹر کی ان پٹ حدود ہیں، صحت کے لیے تجویز کردہ وزن یا قد نہیں۔",
            "BMI ایک عمومی اسکریننگ پیمانہ ہے۔ یہ جسمانی چربی کو براہ راست نہیں ناپتا اور ڈاکٹر کے مشورے کا متبادل نہیں۔",
        ],
        "faq": [
            ("کیا یہ کیلکولیٹر بچوں اور نوعمروں کے لیے ہے؟", "نہیں۔ یہ بالغوں کے BMI کی درجہ بندی استعمال کرتا ہے۔ بچوں اور نوعمروں کے لیے عمر اور جنس کے مطابق BMI-for-age گروتھ چارٹس درکار ہوتے ہیں۔"),
            ("کیا BMI جسمانی چربی کو ناپتا ہے؟", "نہیں۔ یہ صرف قد اور وزن سے حساب ہوتا ہے۔ یہ جسمانی چربی کو براہ راست نہیں ناپتا اور نہ عضلات اور چربی میں فرق کرتا ہے۔"),
            ("کیا BMI 25 ہونا بیماری کی تشخیص ہے؟", "نہیں۔ گول کی گئی BMI قدر 25.0 بالغوں میں زیادہ وزن کی اسکریننگ حد کا آغاز ہے، تشخیص نہیں۔"),
            ("نتیجے کے بعد کیا کرنا چاہیے؟", "اسے عمومی معلومات سمجھیں۔ اگر وزن میں بڑی تبدیلی، علامات یا طبی مسئلہ ہو تو مستند معالج سے مشورہ کریں۔"),
            ("حد کے قریب درجہ کیوں بدل سکتا ہے؟", "کیلکولیٹر BMI کو ایک اعشاری جگہ تک گول کر کے درجہ منتخب کرتا ہے۔ اس لیے دکھائی گئی 25.0 کی قدر زیادہ وزن کی حد میں شمار ہوتی ہے۔"),
        ],
        "sources": 'بالغوں کی BMI درجہ بندی کے لیے <a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" rel="noopener noreferrer">عالمی ادارۂ صحت (WHO) کی موٹاپے اور زیادہ وزن سے متعلق معلومات</a> دیکھیں۔ BMI صرف اسکریننگ پیمانہ ہے اور اسے طبی سیاق میں سمجھنا چاہیے۔',
    },
}


EXTRA = {
    "zakat-calculator": {
        "quick": "Zakat is 2.5 percent of net zakatable wealth, due when that wealth is at least the Nisab (612.36 grams of silver) and has been held for one lunar year.",
        "faq": [
            ("Is Zakat due on my home?", "Your home that you live in is not zakatable wealth. Rental property income and goods held for sale can be zakatable, so check the rules for each asset with a scholar."),
            ("Do I subtract debts?", "Debts due now are commonly subtracted from zakatable wealth. Whether particular long-term debts are deducted is a point scholars discuss, so confirm your case."),
        ],
    },
    "bmi-calculator": {
        "quick": "BMI uses weight in kg divided by height in metres squared when kg is selected, or 703 × weight in lb divided by height in total inches squared when lb is selected. For adults, 18.5 to 24.9 is the WHO normal weight range.",
        "faq": [
            ("Is a BMI of 25 unhealthy?", "A BMI of 25 is at the start of the overweight range. It is a screening number only. Waist size, blood pressure and blood tests give a fuller picture, and a clinician can interpret them with you."),
            ("Does BMI work for athletes?", "BMI can overstate body fat in people with high muscle mass. A clinician can use other measures for athletes."),
        ],
    },
    "profit-loss-calculator": {
        "quick": "Business P&L: net operating profit = revenue - cost of goods sold - other expenses, and operating margin = net operating profit / revenue x 100. Product mode: profit = selling price - cost price, markup = profit / cost price x 100, and gross margin = profit / selling price x 100.",
        "faq": [
            ("What is the difference between markup and margin?", "Product markup uses cost as its base; product gross margin uses selling price. Business operating margin uses revenue after listed expenses. These percentages are not interchangeable."),
            ("How do I include shipping?", "Add shipping, packaging and platform fees to the cost price before you calculate."),
        ],
    },
    "discount-calculator": {
        "quick": "Amount saved equals original price multiplied by the discount percentage, divided by 100. Final price equals original price minus the amount saved.",
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
        "quick": "Each tap adds one. Choose a target of 33, 99, 100, or a custom whole number from 1 to 10,000. The count stays on this device when browser storage is available.",
        "faq": [
            ("Will my count move to another phone?", "No. The count is stored only in the browser on this device."),
        ],
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
        "description": "Convert years into days, weeks, hours, minutes and seconds using a 365-day year, the Gregorian average, or exact calendar dates that include leap days.",
        "h1": "Years to Days Calculator",
        "lead": "Convert years to days, weeks, hours, minutes and seconds. Choose a simple or average-year conversion, or enter a start date for an exact leap-year-aware day count.",
        "ui": (
            '<form id="years-days-form" class="space-y-4" novalidate>'
            '<label class="@L@" for="yd-value">Number of years</label>'
            '<input class="@I@" id="yd-value" type="number" min="0" max="1000000" step="any" inputmode="decimal" value="80" required>'
            '<label class="@L@" for="yd-method">Conversion method</label>'
            '<select class="@I@" id="yd-method"><option value="365">365 days per year (simple)</option><option value="365.2425">365.2425 days per year (Gregorian average)</option><option value="calendar">Exact calendar years (requires start date)</option></select>'
            '<div id="yd-exact-fields" hidden><label class="@L@" for="yd-start-date">Start date (Gregorian calendar)</label>'
            '<input class="@I@" id="yd-start-date" type="date" min="0001-01-01" max="9999-12-31" disabled>'
            '<p class="mt-2 text-sm">Exact mode accepts whole years and counts actual days from the start date up to, but not including, the anniversary. For 29 February, a non-leap anniversary uses 1 March.</p></div>'
            '<button class="@B@" type="submit">Convert Years</button></form>'
            '<div id="yd-result" class="@R@" role="status" aria-live="polite"></div>'
        ),
        "guide": [
            ("Conversion formulas", ["Days = years multiplied by 365 for the simple method. For the Gregorian average, days = years multiplied by 365.2425. Weeks = days divided by 7. Hours = days multiplied by 24. Minutes = hours multiplied by 60. Seconds = minutes multiplied by 60."]),
            ("Worked example", ["80 years = 29,200 days by the 365-day method, or 29,219.4 days by the Gregorian average method. These are conversions, not exact elapsed days between calendar dates."]),
            ("Accuracy limits", ["Calendar years vary between 365 and 366 days. For exact elapsed days, choose Exact calendar years, enter a valid start date and whole number of years. The ending anniversary is excluded and any February 29 inside the period is counted. When a start date is February 29 and the ending year is not leap, the ending anniversary is March 1. For legal deadlines, check the rule that applies to your document."]),
            ("Choosing the right method", ["Use the simple 365-day method when a worksheet or a question explicitly defines one year as 365 days. Use the Gregorian average for long-term approximate conversions across many years, because the Gregorian calendar has 97 leap years in every 400-year cycle. Neither method tells you the exact days between two birthdays without their dates. If you need the exact elapsed time, use the Age Calculator with actual calendar dates. The weeks shown can contain fractions because the conversion divides the day result by seven."]),
            ("Reading the results", ["Hours, minutes and seconds are derived from the selected number of days, not from an assumed start time. Decimal years can produce fractional days and seconds. The calculator shows up to eight decimal places for readability. Rounding the displayed value does not change the internal conversion factor. For example, 1.5 simple years is 547.5 days, which is 78.21428571 weeks and 13,140 hours. For a calendar-specific result, select real start and end dates instead of assuming every year is equal."])
        ],
        "faq": [("How many days are in 80 years?", "29,200 with the simple method, or 29,219.4 with the Gregorian-average method."),
                ("Does this account for leap years?", "Yes in Exact calendar years mode, which uses a start date and counts actual February 29 dates. The average method only approximates leap-year frequency.")],
        "sources": "Gregorian mean year: 365.2425 days over the 400-year Gregorian calendar cycle."
    },
    {
        "slug": "query-calculator", "category": "time",
        "name": "Query Calculator", "app": "UtilitiesApplication",
        "description": "Ask a simple question in English or Roman Urdu about converting years, days, weeks, hours or minutes with clear supported units.",
        "h1": "Query Calculator for Time Conversions",
        "lead": "Ask a time conversion question such as 80 years mein kitne din hote hain? Supports exact birth-date age in days and conversions between years, days, weeks, hours, minutes and seconds.",
        "ui": (
            '<form id="query-time-form" class="space-y-4" novalidate>'
            '<label class="@L@" for="qt-question">Your question</label>'
            '<input class="@I@" id="qt-question" type="text" maxlength="160" value="Ager birth date 29-07-1984 ho to age kitne days hogi?" required>'
            '<p class="text-sm">Uses 365 days per year. Try: 2 weeks in hours, 3 days to minutes, 80 years mein kitne din.</p>'
            '<button class="@B@" type="submit">Calculate Answer</button></form>'
            '<div id="qt-result" class="@R@" role="status" aria-live="polite">Enter a question and tap Calculate Answer. If no result appears, refresh this page.</div>'
        ),
        "guide": [
            ("How it works", ["The question parser recognizes one nonnegative number, a supported source unit and a supported target unit. It calculates using fixed time conversion factors and never guesses unsupported questions."]),
            ("Examples", ["80 years to days = 29,200 days. 2 weeks to hours = 336 hours. 3 days to minutes = 4,320 minutes."]),
            ("Limits", ["The parser supports time conversions and exact Gregorian birth-date-to-today calculations, not arbitrary arithmetic. Time conversion questions use 365 days per year."]),
            ("Supported question patterns", ["Enter one numeric amount followed by a supported time unit and a target unit. For example, 2 weeks in hours, 3 days to minutes, and 80 years mein kitne din hote hain are supported. The parser recognizes year, years, day, days, din, week, weeks, hour, hours, minute, minutes, second and seconds, plus a few Roman Urdu alternatives. It does not use artificial intelligence or guess the meaning of unfamiliar terms. If a question is unclear, it asks for a simpler time conversion instead of giving a potentially misleading number."]),
            ("Understanding answers", ["A year is treated as exactly 365 days in this calculator. A week is seven days, a day is 24 hours, an hour is 60 minutes and a minute is 60 seconds. This makes results repeatable and straightforward to check independently. Leap years and daylight-saving transitions are not inferred from a sentence. For a birth-date question, exact elapsed days are calculated through today using Gregorian calendar dates. Time-unit questions are not intended for legal deadlines, payroll or astronomy. For a different year convention, open the Years to Days Calculator and choose the Gregorian average method."])
        ],
        "faq": [("Can I ask in Roman Urdu?", "Yes, simple patterns such as 80 years mein kitne din hote hain are supported."),
                ("Can I ask any mathematical question?", "No. This version supports time-unit conversion questions only.")],
        "sources": "Fixed conversion factors: 1 day = 24 hours, 1 hour = 60 minutes, 1 minute = 60 seconds; simple year = 365 days."
    }
])
EXTRA.update({slug: {"faq": [], "quick": ""} for slug in ("years-to-days-calculator", "query-calculator")})

for _t in TOOLS:
    _t["guide"] = _t["guide"] + GUIDE_EXTRA.get(_t["slug"], [])
    _t["sources"] = _t["sources"] + " " + REVIEW_STATUS.get(_t["slug"], "")
    if _t["slug"] == "standard-calculator":
        _t["ui"] = CALC_UI
        _t["guide"] += [
            ("How to use the online standard and scientific calculator", [
                "CalculateAllInOne is a free online calculator for everyday arithmetic and more advanced scientific calculations. Use the standard keypad for addition, subtraction, multiplication, division, percentages and brackets. Select Scientific Mode when you need trigonometry, powers, roots, logarithms, factorials, combinations or permutations. The calculator works in a modern browser on desktop and mobile, with large, touch-friendly keys.",
                "Enter an expression in the same order you would write it on paper. Brackets are evaluated first, then powers, multiplication and division, and finally addition and subtraction. For example, 2 + 3 × 4 equals 14 because multiplication takes priority. Use parentheses in (2 + 3) × 4 to make the result 20. Press clear to start again, or use backspace to remove the last character.",
            ]),
            ("Scientific calculator functions and angle modes", [
                "Scientific Mode includes sine, cosine and tangent, inverse trigonometric functions, square roots, powers, constants such as pi and e, logarithms, factorials, combinations and permutations. Choose DEG when an angle is expressed in degrees, such as sin(30), which equals 0.5. Choose RAD when an angle is expressed in radians, such as sin(pi/2), which equals 1. Using the wrong angle mode is a common reason a trigonometry answer looks incorrect.",
                "The calculator also provides an answer memory and basic memory controls to help with multi-step calculations. Check the displayed expression before pressing equals, especially when using negative exponents, nested brackets or logarithms with a custom base. Some inputs have no real-number result, such as dividing by zero or taking a square root of a negative number, so invalid operations should be corrected rather than treated as a numeric answer.",
            ]),
            ("Who can use this free online calculator", [
                "Students can check arithmetic and practise algebra or trigonometry. Teachers and tutors can demonstrate order of operations, powers and angle conversion. Households can work out percentages, discounts and everyday totals, while office users can verify figures before entering them into a spreadsheet. These examples describe common uses, not a guarantee that a result is suitable for every professional task.",
                "CalculateAllInOne performs calculations in the browser and is designed for quick access without installing an app. It is a practical calculation aid, not a substitute for independently checking high-stakes engineering, financial, medical or scientific work. For important results, verify the formula, units, rounding and assumptions with an authoritative source or qualified professional. If an answer seems unexpected, split the expression into smaller steps and compare the intermediate values.",
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



LANG_LOCALE = {"en": "en_US", "ur": "ur_PK", "ar": "ar_AR", "hi": "hi_IN", "es": "es_ES", "fr": "fr_FR"}
RTL_LANGS = ("ur", "ar")
SHELL_EN = {"menu": "All tools", "skip": "Skip to content", "about": "About", "privacy": "Privacy", "contact": "Contact",
            "methodology": "Methodology", "editorial": "Editorial policy", "tag": "© CalculatesAll. Free tools that run in your browser.",
            "theme": "Dark mode", "lang": "Languages", "terms": "Terms of use", "main": "Main", "footer": "Footer", "marketplace": "Marketplace guide", "affiliate": "Advertising disclosure", "confidence": "CALCULATE WITH CONFIDENCE", "many": "ONE PLACE, MANY ANSWERS", "free": "FREE", "discount": "Discount Calculator", "health_link": "Health"}
SHELL_UR = {"menu": "تمام ٹولز", "skip": "مرکزی مواد پر جائیں", "about": "ہمارے بارے میں", "privacy": "رازداری", "contact": "رابطہ",
            "methodology": "طریقہ کار", "editorial": "ادارتی پالیسی", "tag": "© CalculatesAll۔ مفت ٹولز جو آپ کے براؤزر میں چلتے ہیں۔",
            "theme": "ڈارک موڈ", "lang": "زبانیں", "terms": "شرائط استعمال", "main": "مرکزی نیویگیشن", "footer": "فٹر", "marketplace": "مارکیٹ پلیس رہنما", "affiliate": "افیلی ایٹ انکشاف", "confidence": "اعتماد کے ساتھ حساب کریں", "many": "ایک جگہ، کئی جواب", "free": "مفت", "discount": "ڈسکاؤنٹ کیلکولیٹر", "health_link": "صحت"}
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
             "logo": SITE_URL + "/assets/favicon.svg",
             "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": CONTACT_EMAIL, "url": SITE_URL + "/contact/"}},
            {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/#maintainer",
             "name": "Muhammad Fayyaz Adeel", "alternateName": ["Malik Adeel Bhatti"],
             "description": "Maintainer of the CalculatesAll online calculator project.",
             "url": SITE_URL + "/about/",
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
        + '<link rel="stylesheet" href="/assets/site.css?v=20261026-standard-mobile-v6">\n'
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
    home = "/" if lang == "en" else "/" + lang + "/"
    brand_home_label = {"en": " home page", "ur": " ہوم پیج", "ar": " الصفحة الرئيسية", "hi": " होम पेज", "es": " página de inicio", "fr": " page d’accueil"}.get(lang, " home page")
    main_width = "max-w-screen-2xl" if current_path in ("/", "/ur/", "/ar/", "/hi/", "/es/", "/fr/") else "max-w-3xl"
    menu_position = "left-0 right-auto" if lang in RTL_LANGS else "right-0"
    tool_paths = {"/" + t["slug"] + "/" for t in TOOLS if t["slug"] != "standard-calculator"}
    urdu_tool_paths = {"/ur/" + slug + "/" for slug in URDU if slug != "standard-calculator"}
    main_classes = main_width + " mx-auto px-5 py-10"
    if current_path in tool_paths | urdu_tool_paths:
        main_classes += " ca-tool-main"
    return (
        '<body class="min-h-screen bg-gradient-to-br from-slate-100 via-sky-50 to-teal-50 dark:from-slate-950 dark:via-slate-900 dark:to-teal-950 text-stone-900 dark:text-stone-100 antialiased">\n'
        '<div aria-hidden="true" class="pointer-events-none fixed inset-0 -z-10 overflow-hidden">'
        '<div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-violet-300/30 blur-3xl"></div>'
        '<div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full bg-sky-300/35 blur-3xl"></div>'
        '<div class="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-teal-300/30 blur-3xl"></div></div>\n'
        '<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:bg-white focus:px-3 focus:py-2 focus:rounded">' + s["skip"] + '</a>\n'
        '<div class="h-1.5 bg-gradient-to-r from-teal-500 via-sky-500 to-indigo-500"></div>'
        '<header class="sticky top-0 z-20 bg-white/80 dark:bg-stone-900/80 backdrop-blur border-b border-stone-200 dark:border-stone-700 shadow-sm">'
        '<nav class="max-w-5xl mx-auto px-5 py-3 flex flex-wrap items-center justify-between gap-3" aria-label="' + s["main"] + '">'
        '<a href="' + home + '" aria-label="CalculatesAll' + brand_home_label + '" class="font-extrabold text-xl text-slate-900 dark:text-white min-h-[44px] inline-flex items-center gap-2"><span aria-hidden="true" class="inline-block h-3 w-3 rounded-sm bg-gradient-to-br from-teal-500 to-indigo-600"></span>CalculatesAll<span class="sr-only">' + brand_home_label + '</span></a>'
        '<div class="flex items-center gap-3">'
        '<button id="theme-toggle" type="button" class="' + S + ' min-h-[44px]">' + s["theme"] + '</button>'
        '<details class="relative"><summary class="cursor-pointer text-base min-h-[44px] inline-flex items-center px-2">' + s["menu"] + '</summary>'
        '<ul class="absolute ' + menu_position + ' mt-2 w-64 max-w-[calc(100vw-2rem)] overflow-x-hidden break-words bg-white border border-stone-300 rounded-lg p-3 space-y-2 text-base shadow-lg z-10" style="max-width:calc(100vw - 2rem);overflow-wrap:anywhere;box-sizing:border-box">'
        + nav_items(lang)
        + '</ul></details></div></nav></header>\n'
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
        '</div></footer>\n'
        '<script src="/assets/app.js?v=20261030-exact-years-1" defer></script>\n'
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
    return s.replace("@L@", L).replace("@I@", I).replace("@B@", B).replace("@S@", S).replace("@R@", R)


def write(path, content):
    rel = path.strip("/")
    folder = os.path.join(OUT, rel) if rel else OUT
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(fill(content))


def years_to_days_reference_html():
    rows = [
        (1, "365", "365.2425"),
        (2, "730", "730.485"),
        (3, "1,095", "1,095.7275"),
        (5, "1,825", "1,826.2125"),
        (10, "3,650", "3,652.425"),
        (20, "7,300", "7,304.85"),
        (50, "18,250", "18,262.125"),
        (80, "29,200", "29,219.4"),
        (100, "36,500", "36,524.25"),
    ]
    out = ('<section class="mt-10"><h2 class="' + H2 + '">Quick reference: years to days</h2>'
           '<p class="' + P + '">Common conversions using a fixed 365-day year and the 365.2425-day Gregorian average. Average-method values can be fractional days.</p>'
           '<div class="mt-4 overflow-x-auto"><table class="w-full border-collapse text-left text-sm">'
           '<caption class="sr-only">Years converted to days using the 365-day and Gregorian-average methods</caption>'
           '<thead><tr><th scope="col" class="border-b p-3">Years</th><th scope="col" class="border-b p-3">365-day method</th><th scope="col" class="border-b p-3">Gregorian average</th></tr></thead><tbody>')
    for years, simple, average in rows:
        out += ('<tr><th scope="row" class="border-b p-3">' + str(years) + '</th>'
                '<td class="border-b p-3">' + simple + '</td>'
                '<td class="border-b p-3">' + average + '</td></tr>')
    out += ('</tbody></table></div><p class="' + P + '">For exact elapsed days between calendar dates, use Exact calendar years in the calculator above. This table is a duration reference, not a substitute for a date-specific count.</p></section>')
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
        "en": 'This calculator uses the silver Nisab standard of 612.36 grams and applies 2.5% to eligible net wealth when the required conditions are met. Nisab standards differ, so this page names the silver standard it uses. Source: <a class="' + LINK + '" href="https://islamicrelief.org.au/our-work/islamic-giving/nisab/" target="_blank" rel="noopener noreferrer">Islamic Relief Australia Nisab guidance</a>.',
        "ur": 'یہ کیلکولیٹر چاندی کے 612.36 گرام نصاب اور اہل خالص مال پر 2.5٪ شرح استعمال کرتا ہے۔ نصاب کے معیار مختلف ہو سکتے ہیں، اس لیے یہاں چاندی کا معیار واضح کیا گیا ہے۔ ماخذ: <a class="' + LINK + '" href="https://islamicrelief.org.au/our-work/islamic-giving/nisab/" target="_blank" rel="noopener noreferrer">اسلامک ریلیف آسٹریلیا کی نصاب رہنمائی</a>۔'
    },
    "bmi-calculator": {
        "en": 'For adults, the CDC classifies a BMI from 25.0 to less than 30.0 as overweight; BMI is a screening measure, not a diagnosis. Source: <a class="' + LINK + '" href="https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html" target="_blank" rel="noopener noreferrer">CDC adult BMI categories</a>.',
        "ur": 'بالغ افراد میں CDC کے مطابق BMI کی 25.0 سے 30.0 سے کم حد کو زائد وزن کہا جاتا ہے؛ BMI صرف ابتدائی جانچ ہے، تشخیص نہیں۔ ماخذ: <a class="' + LINK + '" href="https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html" target="_blank" rel="noopener noreferrer">CDC کی بالغوں کے لیے BMI درجہ بندی</a>۔'
    },
    "profit-loss-calculator": {
        "en": 'Business example: revenue 1,000, cost of goods sold 600 and other expenses 150 gives net operating profit 250 and margin 25%. Product example: cost 1,000 and selling price 1,200 gives markup 20%. Source: <a class="' + LINK + '" href="/methodology/">CalculatesAll calculation methodology</a>.',
        "ur": 'اگر کسی چیز کی قیمت خرید 1,000 اور فروخت 1,200 ہو تو دوسرے کاروباری اخراجات سے پہلے فرق 200 ہے۔ یہ اسی کیلکولیٹر کا بنیادی تقابل ہے۔ ماخذ: <a class="' + LINK + '" href="/methodology/">CalculatesAll کا حسابی طریقۂ کار</a>۔'
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
        "en": 'One international avoirdupois pound equals exactly 0.45359237 kilograms. Source: <a class="' + LINK + '" href="https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9" target="_blank" rel="noopener noreferrer">NIST conversion factors</a>.',
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
        "For adults, the standard WHO categories are underweight below 18.5, normal weight from 18.5 to below 25, overweight from 25 to below 30, and obesity from 30 upward. This calculator rounds BMI to one decimal place before assigning the displayed category. Values near a boundary can therefore display in the next category after rounding.",
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
    ("Is a BMI of 25 a diagnosis?", "No. A rounded adult BMI of 25.0 is the start of the overweight screening category, not a diagnosis. A clinician can interpret it with other health information."),
    ("Why does the category change near a boundary?", "This calculator rounds the calculated BMI to one decimal place before choosing a category. A displayed value of 25.0 is classified in the overweight category."),
    ("What should I do with my result?", "Treat it as general information. Discuss concerns or major weight changes with a qualified healthcare professional, especially if you have symptoms or a medical condition."),
]
BMI_SOURCES = 'Adult BMI categories are based on the World Health Organization\'s classification. Read the <a class="' + LINK + '" href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" rel="noopener noreferrer">WHO fact sheet on obesity and overweight</a>. BMI is a screening measure and should be interpreted in context.'

def tool_page(t):
    path = "/" + t["slug"] + "/"
    url = SITE_URL + path
    cat = next(c for c in CATEGORIES if c["slug"] == t["category"])
    if t["slug"] == "bmi-calculator":
        title = "BMI Calculator for Adults | cm or ft/in | CalculatesAll"
        desc = "Calculate adult BMI using kilograms and centimetres or kilograms with feet and inches. See WHO adult BMI ranges and their limitations."
        ui = BMI_UI
        guide = BMI_GUIDE + GUIDE_EXTRA.get(t["slug"], [])
        faqs = BMI_FAQ
        sources = BMI_SOURCES
    elif t["slug"] == "profit-loss-calculator":
        title = "Profit and Loss Calculator | Business P&L and Product Profit"
        desc = "Free business P&L calculator for revenue, cost of goods sold and expenses, plus product profit and markup. See gross profit, operating profit and margin."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "years-to-days-calculator":
        title = "Years to Days Calculator | Exact and Average"
        desc = "Convert years to days using 365 days, the Gregorian average of 365.2425 days, or exact calendar dates. See quick-reference examples and leap-year limits."
        ui = t["ui"]
        guide = t["guide"]
        faqs = t["faq"] + EXTRA[t["slug"]]["faq"]
        sources = t["sources"]
    elif t["slug"] == "tasbih-counter":
        title = "Free Online Tasbih Counter | Digital Tasbeeh Counter"
        desc = "Free online tasbih counter for daily dhikr. Tap to count, set targets of 33, 99 or 100, and save your count on your device. No download needed."
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
    related = ""
    related_tools = [other for other in TOOLS if other["slug"] != t["slug"] and other["category"] == t["category"]]
    related_tools += [other for other in TOOLS if other["slug"] != t["slug"] and other not in related_tools]
    for other in related_tools[:2]:
        related += '<li><a class="' + LINK + '" href="/' + other["slug"] + '/">' + other["name"] + "</a></li>"
    alternates = None
    if t["slug"] in URDU:
        alternates = [("en", path), ("ur", "/ur" + path), ("x-default", path)]
    updated_date = LASTMOD.get(path)
    updated = ('<p class="mt-8 text-sm text-stone-800 dark:text-stone-200">Last updated: ' + updated_date + ". " + t["sources"] + "</p>") if updated_date else ""
    calculator_section = (
        ('<section id="tool-calculator" class="ca-tool-calculator ca-tool-' + t["slug"] + ' mt-4 rounded-2xl bg-white/95 dark:bg-stone-900/95 shadow-xl ring-1 ring-stone-200 dark:ring-stone-700 p-5 sm:p-6" aria-label="Calculator">'
         if t["slug"] != "standard-calculator" else
         '<section id="tool-calculator" class="ca-tool-standard-calculator mt-2 rounded-2xl bg-white/95 dark:bg-stone-900/95 shadow-xl ring-1 ring-stone-200 dark:ring-stone-700 p-3 sm:p-4" aria-label="Calculator">')
        + ui + '</section>'
    )
    answer_note = answer_block(t["slug"], "en")
    primary_tool_content = calculator_section + answer_note
    breadcrumb_html = (
        '<nav aria-label="Breadcrumb" class="text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap gap-2">'
        '<li><a class="' + LINK + '" href="/">Home</a></li>'
        '<li><span aria-hidden="true" class="mr-2">/</span><a class="' + LINK + '" href="/' + cat["slug"] + '/">' + cat["name"] + '</a></li>'
        '<li aria-current="page"><span aria-hidden="true" class="mr-2">/</span>' + t["name"] + "</li></ol></nav>"
    )
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
    body = (
        ("" if t["slug"] == "profit-loss-calculator" else breadcrumb_html)
        + '<h1 class="text-3xl font-extrabold bg-gradient-to-r from-fuchsia-700 via-indigo-700 to-sky-700 bg-clip-text text-transparent mt-4"><span aria-hidden="true">' + TILE_ICON.get(t["slug"], "") + '</span> ' + t["h1"] + '</h1>'
        + (primary_tool_content + '<p class="ca-tool-lead-after mt-3 text-base text-stone-900 dark:text-stone-100">' + t["lead"] + '</p>'
           if t["slug"] in {tool["slug"] for tool in TOOLS}
           else '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + t["lead"] + '</p>' + primary_tool_content)
        + (breadcrumb_html if t["slug"] == "profit-loss-calculator" else "")
        + ad_slot()
        + (('<h2 class="' + H2 + '">How it is calculated</h2>'
            + '<p class="mt-4 rounded-xl bg-sky-50 dark:bg-sky-950 border border-sky-200 dark:border-sky-800 p-5 text-base text-stone-900 dark:text-stone-100"><strong>Worked method.</strong> ' + EXTRA[t["slug"]]["quick"] + '</p>')
           if EXTRA[t["slug"]]["quick"].strip() else "")
        + profit_reference_table
        + (guide_html(guide[:2]) + years_to_days_reference_html() + guide_html(guide[2:])
           if t["slug"] == "years-to-days-calculator" else guide_html(guide))
        + '<h2 class="' + H2 + '">Common questions</h2><div class="mt-3">' + faq_html(faqs) + "</div>"
        + '<h2 class="' + H2 + '">Sources</h2><p class="' + P + '">' + sources + '</p>'
        + '<p class="mt-6 text-sm text-stone-700 dark:text-stone-300">Maintained by <a class="' + LINK + '" href="/about/">Muhammad Fayyaz Adeel</a>.</p>'
        + updated
        + review_box(t["slug"])
        + '<section class="mt-12"><h2 class="text-xl font-semibold text-stone-900 dark:text-stone-100">More in ' + cat["name"] + '</h2>'
        '<ul class="mt-3 grid sm:grid-cols-2 gap-2 text-base">' + related + "</ul></section>"
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
    if t["slug"] == "profit-loss-calculator":
        ui = ui.replace("> Business P&amp;L</label>", "> کاروبار کا نفع و نقصان</label>")
        ui = ui.replace("> Product profit</label>", "> پروڈکٹ کا نفع</label>")
    if t["slug"] == "tasbih-counter":
        ui = ui.replace("Saving is unavailable in this browser. Your count is kept in memory until you leave or reload this page.", "اس براؤزر میں گنتی محفوظ کرنا ممکن نہیں ہے۔ آپ کی گنتی اس صفحے کو چھوڑنے یا دوبارہ لوڈ کرنے تک عارضی طور پر محفوظ رہے گی۔")
        ui = ui.replace('<label class="', '<label lang="ur" class="')
        ui = ui.replace('id="t-lifetime-label">', 'id="t-lifetime-label" lang="ur">')
    cat = next(c for c in CATEGORIES if c["slug"] == t["category"])
    cat_ur = {"money": "پیسہ اور کاروبار", "health": "صحت", "time": "تاریخ اور وقت", "math": "ریاضی اور اکائیاں", "worship": "عبادت اور روزمرہ"}[cat["slug"]]
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": u["name"], "url": url,
         "description": u["description"], "inLanguage": "ur", "applicationCategory": t["app"],
         "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "inLanguage": "ur", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "صفحہ اول", "item": SITE_URL + "/ur/"},
            {"@type": "ListItem", "position": 2, "name": cat_ur, "item": SITE_URL + "/" + cat["slug"] + "/"},
            {"@type": "ListItem", "position": 3, "name": u["name"], "item": url}]},
    ]
    how = ""
    for p in u["how"]:
        how += '<p class="' + P + '">' + p + "</p>"
    faq = faq_html(u["faq"])
    calculator_section = (
        ('<section id="tool-calculator" class="ca-tool-calculator ca-tool-' + t["slug"] + ' mt-4" aria-label="کیلکولیٹر">'
         if t["slug"] != "standard-calculator" else
         '<section id="tool-calculator" class="ca-tool-standard-calculator mt-4" aria-label="کیلکولیٹر">')
        + ui + '</section>'
    )
    answer_note = "" if t["slug"] in ("bmi-calculator", "discount-calculator") else answer_block(t["slug"], "ur")
    primary_tool_content = calculator_section + answer_note
    body = (
        '<nav aria-label="صفحہ کی ترتیب" class="text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap gap-2">'
        '<li><a class="' + LINK + '" href="/ur/">صفحہ اول</a></li><li aria-hidden="true">/</li>'
        '<li><a class="' + LINK + '" href="/' + cat["slug"] + '/">' + cat_ur + '</a></li><li aria-hidden="true">/</li>'
        '<li aria-current="page">' + u["name"] + '</li></ol></nav>'
        '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100 mt-4">' + u["h1"] + '</h1>'
        '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + u["lead"] + '</p>'
        + primary_tool_content
        + '<h2 class="' + H2 + '">' + u["how_heading"] + '</h2>' + how
        + '<h2 class="' + H2 + '">' + u["faq_heading"] + '</h2><div class="mt-3">' + faq + "</div>"
        + ('<h2 class="' + H2 + '">ماخذ</h2><p class="' + P + '">' + u["sources"] + '</p>' if u.get("sources") else "")
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
                      '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/' + t["slug"] + '">' + t["name"] + "</a>"
                      '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + t["description"] + "</p></li>")
    if c["slug"] == "money":
        items += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                  '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/emi-calculator/">EMI Calculator</a>'
                  '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">Estimate monthly loan installments, total interest and a month-by-month repayment schedule. Lender fees and contract terms may change the final quote.</p></li>')
    for slug, label in {"math": [("percentage-calculator", "Percentage Calculator"), ("fraction-calculator", "Fraction Calculator")], "money": [("compound-interest-calculator", "Compound Interest Calculator")], "time": [("date-calculator", "Date Difference Calculator")]}.get(c["slug"], []):
        items += '<li><a class="text-sky-800 underline" href="/' + slug + '/">' + label + '</a></li>'
    related = "".join(
        '<li><a class="text-sky-800 dark:text-sky-300 underline" href="/'
        + other["slug"] + '/">' + html.escape(other["name"]) + "</a></li>"
        for other in CATEGORIES if other["slug"] != c["slug"]
    )
    title = c["name"] + " | CalculatesAll"
    schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": c["name"], "url": SITE_URL + path}]
    if c["slug"] == "health":
        schema.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Health", "item": SITE_URL + "/health/"},
        ]})
    body = ('<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">' + c["name"] + '</h1>'
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
    for p in paragraphs:
        body += '<p class="' + P + '">' + p + "</p>"
    if path == "/about/":
        contact_email = html.escape(CONTACT_EMAIL, quote=True)
        body += (
            '<section aria-labelledby="about-maintainer" class="mt-8">'
            '<h2 id="about-maintainer" class="' + H2 + '">Who maintains CalculatesAll?</h2>'
            '<p class="' + P + '">CalculatesAll is maintained by Muhammad Fayyaz Adeel, also known as Malik Adeel Bhatti. The maintainer looks after the calculator pages, site updates and reproducible correction reports. This identifies the person responsible for the project; it does not claim a regulated professional qualification or independent expert review.</p>'
            '</section>'
            '<section aria-labelledby="about-tools" class="mt-8">'
            '<h2 id="about-tools" class="' + H2 + '">What calculators and tools are available?</h2>'
            '<p class="' + P + '">The money tools include the <a class="' + LINK + '" href="/profit-loss-calculator/">Profit and Loss Calculator</a>, <a class="' + LINK + '" href="/discount-calculator/">Discount Calculator</a>, <a class="' + LINK + '" href="/emi-calculator/">EMI Calculator</a> and <a class="' + LINK + '" href="/zakat-calculator/">Zakat Calculator</a>. Date and measurement tools include the <a class="' + LINK + '" href="/age-calculator/">Age Calculator</a>, <a class="' + LINK + '" href="/years-to-days-calculator/">Years to Days Calculator</a>, <a class="' + LINK + '" href="/query-calculator/">Query Calculator</a> and <a class="' + LINK + '" href="/unit-converter/">Unit Converter</a>.</p>'
            '<p class="' + P + '">The Query Calculator accepts supported plain-language time-conversion questions, such as asking how many days are in 80 years; it does not try to answer arbitrary questions.</p>'
            '<p class="' + P + '">Everyday tools include the <a class="' + LINK + '" href="/standard-calculator/">Standard Calculator</a>, <a class="' + LINK + '" href="/bmi-calculator/">adult BMI calculator</a>, <a class="' + LINK + '" href="/tasbih-counter/">Tasbih Counter</a> and <a class="' + LINK + '" href="/stopwatch/">Stopwatch</a>.</p>'
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
                          '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/ur/' + t["slug"] + '">' + URDU[t["slug"]]["name"] + "</a>"
                          '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + URDU[t["slug"]]["description"] + "</p></li>")
    else:
        path = "/"
        title = "CalculatesAll | Free Online Calculators and Utility Tools"
        desc = "Free online calculators for Zakat, BMI, profit and loss, age, discounts, unit conversion, a standard calculator, tasbih counter and stopwatch."
        h1 = "Free Online Standard Calculator"
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
    else:
        title = "CalculatesAll | Free Online Calculators and Utility Tools"
        desc = "Free online calculators for EMI, Zakat, BMI, profit and loss, discounts, age and unit conversion, with clear formulas and browser-based tools."
        h1 = "Free Online Standard Calculator"
        lead = "Fast, free, and private. Tap the buttons or use your keyboard to calculate."
        more_h = "More free tools"
    trust = ""
    for i, label in enumerate(TRUST[lang]):
        trust += '<li class="rounded-xl p-3 text-center text-sm font-bold ' + TRUST_CLASS[i] + '">' + label + "</li>"
    tiles = ""
    for t in TOOLS:
        if t["slug"] == "standard-calculator":
            continue
        if urdu and t["slug"] not in URDU:
            continue
        name = URDU[t["slug"]]["name"] if urdu else t["name"]
        href = ("/ur/" if urdu else "/") + t["slug"] + "/"
        tiles += ('<li><a href="' + href + '" class="' + TILE_BASE + " " + TILE_GRAD[t["slug"]] + '">'
                  '<span class="text-4xl" aria-hidden="true">' + TILE_ICON[t["slug"]] + "</span>"
                  "<span>" + name + "</span></a></li>")
    if not urdu:
        tiles += ('<li><a href="/emi-calculator/" class="' + TILE_BASE + ' bg-gradient-to-br from-cyan-700 to-blue-800">'
                  '<span class="text-4xl" aria-hidden="true">💳</span>'
                  '<span>EMI Calculator</span></a></li>')
    cats = ""
    if not urdu:
        for c in CATEGORIES:
            cats += ('<li><a class="rounded-full px-4 py-2 text-sm font-semibold min-h-[44px] inline-flex items-center '
                     + CAT_PILL[c["slug"]] + '" href="/' + c["slug"] + '/">' + c["name"] + "</a></li>")
        cats = '<nav aria-label="Categories" class="mt-8"><ul class="flex flex-wrap gap-3">' + cats + "</ul></nav>"
    side_title = "Designed for quick answers" if not urdu else "فوری جواب کے لیے آسان ڈیزائن"
    side_desc = "Clear buttons, readable results, and useful everyday tools in one place." if not urdu else "آسان بٹن، واضح نتائج اور روزمرہ کے مفید ٹولز ایک جگہ۔"
    calc_title = "Standard Calculator" if not urdu else "معیاری کیلکولیٹر"
    tool_intro = "Choose a tool to get started." if not urdu else "شروع کرنے کے لیے کوئی ٹول منتخب کریں۔"
    free_label = "FREE TOOLS • PRIVATE BY DESIGN • NO SIGN-UP" if not urdu else "مفت ٹولز • نجی استعمال • سائن اپ نہیں"
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
        + '<div class="ca-home-tools-heading"><div><p class="ca-home-side-eyebrow">' + s["many"] + '</p><h2>' + more_h + '</h2></div><span class="ca-home-free">' + s["free"] + '</span></div>'
        + '<p class="ca-home-tools-copy">' + tool_intro + '</p>'
        + '<ul class="ca-home-tool-grid">' + tiles + '</ul></aside>'
        '</div>'
        + cats
        + ('<nav aria-label="Related calculators" class="mt-8"><h2 class="text-xl font-semibold">Explore more calculators</h2><ul class="mt-3 grid gap-3"><li><a class="text-sky-800 dark:text-sky-300 underline" href="/percentage-calculator/">Percentage Calculator</a></li><li><a class="text-sky-800 dark:text-sky-300 underline" href="/fraction-calculator/">Fraction Calculator</a></li><li><a class="text-sky-800 dark:text-sky-300 underline" href="/compound-interest-calculator/">Compound Interest Calculator</a></li><li><a class="text-sky-800 dark:text-sky-300 underline" href="/date-calculator/">Date Difference Calculator</a></li></ul></nav>' if not urdu else '')
        + '<section class="ca-home-extra">' + home_extra_html(lang) + '</section>'
        '</div>'
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
            "<strong>Advertising and cookies.</strong> CalculatesAll may show advertising served by Google AdSense. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet. Google and its partners may also use web beacons, IP addresses and device identifiers to measure and protect advertising. Read <a class='underline text-sky-800 dark:text-sky-300' href='https://policies.google.com/technologies/partner-sites' target='_blank' rel='noopener noreferrer'>how Google uses information from sites that use its services</a> and the <a class='underline text-sky-800 dark:text-sky-300' href='https://policies.google.com/technologies/ads' target='_blank' rel='noopener noreferrer'>Google advertising technologies page</a>.",
            "<strong>Your choices.</strong> You can opt out of personalised advertising by visiting <a class='underline text-sky-800 dark:text-sky-300' href='https://adssettings.google.com/' target='_blank' rel='noopener noreferrer'>Google Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalised advertising at <a class='underline text-sky-800 dark:text-sky-300' href='https://www.aboutads.info/choices/' target='_blank' rel='noopener noreferrer'>www.aboutads.info</a>. Opting out stops personalised ads; you may still see non-personalised ads. You can also block or delete cookies in your browser settings.",
            "<strong>Visitors in the EEA, UK and Switzerland.</strong> Where the law requires it, you will be asked for consent through a Google-certified consent message before personalised advertising cookies are used, and you can change your choice later.",
            "<strong>Children.</strong> CalculatesAll is a general-audience website. It is not directed at children under 13 and we do not knowingly collect personal information from children.",
            "<strong>External links.</strong> Some pages link to official sources such as the World Health Organization or NIST. Those websites have their own privacy policies.",
            "<strong>Changes and contact.</strong> If this policy changes, the updated version will be published on this page. For privacy questions, email <a class='underline text-sky-800 dark:text-sky-300' href='mailto:" + CONTACT_EMAIL + "'>" + CONTACT_EMAIL + "</a>.",
        ]),
        ("/methodology/", "How Our Calculations Work | CalculatesAll", "See the formulas, conversion factors, worked examples and limitations used by CalculatesAll calculators and reference tools.", "How Our Calculations Work", [
            "Each tool uses a published formula. Zakat uses the silver Nisab of 612.36 grams. BMI uses the standard formula with WHO adult categories. Profit, discount, age and unit conversions use standard arithmetic and fixed conversion factors.",
            "Every tool page states its assumptions and limits. When a rule depends on a school of law or a clinical judgement, the page says so and points to a qualified professional.",
            "If you find a formula error, email " + CONTACT_EMAIL + " with the tool name and the inputs. We check the report, correct confirmed errors on the tool page and reply to let you know.",
        ]),
        ("/editorial-policy/", "Editorial Policy | CalculatesAll", "Learn how CalculatesAll researches, checks, updates and corrects its calculator guides, formulas and reference information.", "Editorial Policy", [
            "Tool guides are written to explain the formula, show a worked example, and list common mistakes. Numbers in worked examples are shown as step-by-step calculations.",
            "Religious and health content is labelled as a general guide. For a ruling on Zakat or a diagnosis, consult a qualified scholar or health professional.",
            "A last-updated date is shown only when a substantive page update is tracked. We name sources where they support a claim, and we correct confirmed errors when reported or discovered. We do not label a page as independently reviewed unless that review has taken place.",
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
            'For corrections, feedback or questions about a tool, email <a class="' + LINK + '" href="mailto:' + html.escape(CONTACT_EMAIL, quote=True) + '">' + html.escape(CONTACT_EMAIL) + '</a>.',
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
        elif path == "/editorial-policy/":
            paras = [
                "Calculator guides describe the inputs, method, worked examples where helpful, common mistakes and limitations. Each worked example states its calculation so readers can repeat it.",
                "We prefer official or primary references for factual claims. Health information is general guidance, not a diagnosis; Zakat calculations state their method and do not replace a qualified scholar's ruling.",
                "Page reviews and expert endorsements are identified only when they have actually taken place. Update dates reflect tracked substantive changes.",
                "Quality checks cover representative inputs and boundaries, generated pages, titles, descriptions, canonical URLs, structured data, sitemap entries and internal links. They reduce regression risk but cannot cover every browser or situation.",
                "To request a correction, send the page URL, inputs, displayed result and expected result or source. Confirmed issues are investigated and corrected, with relevant checks before publication.",
                "A guide distinguishes facts, assumptions and examples. A worked example illustrates a particular set of inputs; it is not a prediction or a guarantee that the same answer applies to every visitor.",
                "Financial tools specify the base of each percentage and do not silently include fees, taxes or other costs that the visitor has not entered. Users should review the displayed assumptions before using a result for a decision.",
                "Date and conversion tools describe their units and conventions. A month is not treated as a constant number of days, and temperature conversions account for the different zero points of the scales.",
                "Medical screening content identifies the population for which a formula is intended and makes clear that a calculator cannot replace clinical evaluation. Religious guidance states the calculation approach without presenting a numerical output as a personal ruling.",
                "Editorial changes should be checked for factual accuracy, accessibility and readability on small screens. Technical checks examine navigation, generated links, language versions and structured data where applicable.",
                "A passing automated test does not establish that a page is error-free. Browser behavior, accessibility and calculations can still require manual review, especially when a new feature or formula is introduced.",
                "When a source is revised or a reported issue is confirmed, the relevant explanation and any affected example should be updated together. We avoid adding unsupported claims about external expert approval or the date of a review.",
                "Visitors can independently reproduce many examples with the inputs and methods shown. Reports that include a specific page, input values and an expected outcome are more actionable than a general statement that a result looks wrong.",
            ]
        elif path == "/affiliate-disclosure/":
            paras = [
                "CalculatesAll is free to use. Advertising is not currently enabled on the site. If ads are enabled in the future, they will be separated from calculator results, buttons and navigation.",
                "CalculatesAll does not currently use affiliate links. Any future affiliate relationship will be disclosed beside relevant links and on this page.",
                "Advertising does not determine calculator formulas, worked examples or results. We do not publish paid reviews, invented ratings or undisclosed sponsored editorial content.",
                'Questions about this disclosure can be sent to <a class="underline text-sky-800 dark:text-sky-300" href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a>.',
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
    print("Built " + str(len(entries)) + " indexable URLs into " + OUT + "/")


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
