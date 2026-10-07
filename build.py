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
ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "").strip()
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "malikadeelbhatti@gmail.com").strip()
LAST_REVIEWED = "2026-10-08"  # change only when a guide, formula or policy text really changes
OUT = "public"
STATIC = "static"

L = "block text-base font-medium text-stone-800 dark:text-stone-200 mb-1"
I = "w-full rounded-lg border border-stone-400 dark:border-stone-500 dark:border-stone-400 bg-white dark:bg-stone-900 px-3 py-3 text-base min-h-[44px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
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
            '<input id="' + fid + '" class="@I@" type="number" min="0" step="' + step + '" inputmode="decimal">' + h + "</div>")


def check(fid, label):
    return ('<label class="flex items-start gap-3 text-base text-stone-900 dark:text-stone-100 min-h-[44px]">'
            '<input id="' + fid + '" type="checkbox" class="mt-1 h-5 w-5"> <span>' + label + "</span></label>")


def result(rid):
    return '<div id="' + rid + '" class="@R@" aria-live="polite"></div>'


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
            + field("z-cash", "Cash and bank savings")
            + field("z-gold", "Gold value (in your currency)")
            + field("z-silver", "Silver value (in your currency)")
            + field("z-stock", "Business goods for sale (market value)")
            + field("z-recv", "Money owed to you that you expect to receive")
            + field("z-debts", "Debts due now (subtracted from wealth)")
            + "</div>"
            + field("z-silverprice", "Silver price per gram today (in your currency)", hint="Required to check Nisab. Without it, no Zakat amount is shown.")
            + check("z-hawl", "This wealth has been held for one full lunar year (hawl)")
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
            '<select id="bmi-unit" class="@I@"><option value="metric">Metric (kg and cm)</option><option value="imperial">Imperial (lb and ft/in)</option></select></div>'
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
                "Metric: BMI equals weight in kilograms divided by height in meters, squared.",
                "Imperial: BMI equals 703 multiplied by weight in pounds, divided by height in inches, squared.",
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
        "description": "Calculate profit or loss and profit percentage from cost price and selling price.",
        "h1": "Profit and Loss Calculator",
        "lead": "Enter the cost price and the selling price to see whether you made a profit or a loss, and by what percentage of cost.",
        "ui": (
            '<form id="pl-form" class="space-y-5" novalidate>'
            '<div class="grid sm:grid-cols-2 gap-4">'
            + field("p-cost", "Cost price")
            + field("p-sell", "Selling price")
            + '</div><button type="submit" class="@B@">Calculate</button></form>'
            + result("pl-result")
        ),
        "guide": [
            ("The formulas", [
                "Profit or loss equals selling price minus cost price. A negative result is a loss.",
                "Percentage equals profit or loss divided by cost price, multiplied by 100.",
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
            ("Why is margin different from markup?", "Markup is calculated on cost. Margin is calculated on selling price. This calculator shows the percentage on cost price."),
            ("Why does it show N/A?", "A percentage cannot be calculated when cost price is zero, because the formula divides by cost."),
        ],
        "sources": "Standard accounting formulas for profit and percentage on cost.",
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
            '<input id="a-dob" type="date" class="@I@"></div>'
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
        "name": "Standard Calculator",
        "app": "UtilitiesApplication",
        "description": "Use a standard calculator for addition, subtraction, multiplication, division and percentages in your browser.",
        "h1": "Online Standard Calculator",
        "lead": "A simple calculator for everyday arithmetic. Calculations run in your browser and are not sent to a server.",
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
                "Parentheses are not supported in this version. Enter the calculation in the order of operations instead.",
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
        "description": "Count tasbih with preset targets. The count stays saved on this device only.",
        "h1": "Online Tasbih Counter",
        "lead": "Tap to count your dhikr with a 33, 100 or 1000 target, or count without a target. The count is saved on this device only.",
        "ui": (
            '<div class="max-w-sm mx-auto space-y-5">'
            '<div><label class="@L@" for="t-target">Target</label>'
            '<select id="t-target" class="@I@"><option value="33">33</option><option value="100">100</option><option value="1000">1000</option><option value="0">Unlimited</option></select></div>'
            '<output id="t-count" class="block text-center text-6xl font-semibold bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 rounded-xl py-8" aria-live="polite">0</output>'
            '<p id="t-progress" class="text-center text-base text-stone-800 dark:text-stone-200" aria-live="polite"></p>'
            '<div class="grid grid-cols-2 gap-3">'
            '<button id="t-tap" class="@B@">Tap to count</button>'
            '<button id="t-reset" class="@S@">Reset</button>'
            '</div></div>'
        ),
        "guide": [
            ("How it works", [
                "Each tap adds one to the count. When a target is selected, the progress line shows how many remain.",
                "The count is stored in your browser's local storage. Clearing browser data or using another device starts a new count.",
            ]),
            ("Common mistakes", [
                "Resetting by accident. Reset clears the saved count on this device.",
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
            '<div class="max-w-sm mx-auto space-y-5 text-center">'
            '<output id="sw-display" class="block text-5xl font-semibold bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 rounded-xl py-8 tabular-nums" aria-live="off">00:00:00.00</output>'
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
        "intro": "These tools cover the money questions people ask most often: how much Zakat is due, whether a sale made a profit or a loss, and how much a discount saves. Each calculation shows its formula and a worked example, so you can check the result yourself.",
        "faq": [
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
    {"slug": "money", "name": "Money and Business", "desc": "Zakat, profit and loss, and discount calculators for everyday money decisions."},
    {"slug": "health", "name": "Health", "desc": "Adult body mass index calculation with WHO weight categories."},
    {"slug": "time", "name": "Date and Time", "desc": "Exact age in years, months and days, and a browser stopwatch."},
    {"slug": "math", "name": "Math and Converters", "desc": "Standard arithmetic and unit conversion for weight, length and temperature."},
    {"slug": "worship", "name": "Worship and Daily Use", "desc": "A tasbih counter that saves your count on this device."},
]

URDU = {
    "zakat-calculator": {
        "name": "زکوٰۃ کیلکولیٹر",
        "title": "نصاب چیک کے ساتھ زکوٰۃ کیلکولیٹر | CalculatesAll",
        "description": "چاندی کے نصاب کے ساتھ خالص مال پر 2.5 فیصد زکوٰۃ کا حساب کریں اور قمری سال مکمل ہونے کی تصدیق کریں۔",
        "h1": "نصاب چیک کے ساتھ زکوٰۃ کیلکولیٹر",
        "lead": "اپنی بچت اور اثاثے درج کریں، پھر چاندی کی فی گرام قیمت لکھیں۔ کیلکولیٹر پہلے نصاب چیک کرتا ہے اور زکوٰۃ کی رقم اسی وقت دکھاتا ہے جب نصاب اور قمری سال کی شرط پوری ہو۔",
        "labels": [
            ("Cash and bank savings", "نقد اور بینک میں بچت"),
            ("Gold value (in your currency)", "سونے کی قیمت (آپ کی کرنسی میں)"),
            ("Silver value (in your currency)", "چاندی کی قیمت (آپ کی کرنسی میں)"),
            ("Business goods for sale (market value)", "فروخت کے لیے کاروباری سامان (بازاری قیمت)"),
            ("Money owed to you that you expect to receive", "آپ کو واجب الادا رقم جو آپ کو ملنے کی امید ہے"),
            ("Debts due now (subtracted from wealth)", "ابھی واجب الادا قرض (مال سے منہا ہوگا)"),
            ("Silver price per gram today (in your currency)", "آج چاندی کی فی گرام قیمت (آپ کی کرنسی میں)"),
            ("This wealth has been held for one full lunar year (hawl)", "یہ مال ایک مکمل قمری سال (حول) تک رکھا گیا ہے"),
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
        "description": "میٹرک یا امپیریل اکائیوں میں بالغوں کا باڈی ماس انڈیکس نکالیں اور WHO کی وزن کی درجہ بندی دیکھیں۔",
        "h1": "بالغوں کے لیے BMI کیلکولیٹر",
        "lead": "میٹرک یا امپیریل اکائیوں میں اپنا باڈی ماس انڈیکس نکالیں۔ BMI بالغوں کے لیے ایک اسکریننگ پیمانہ ہے، تشخیص نہیں۔",
        "labels": [
            ("Metric (kg and cm)", "میٹرک (کلو گرام اور سینٹی میٹر)"),
            ("Imperial (lb and ft/in)", "امپیریل (پاؤنڈ اور فٹ/انچ)"),
            ("Weight (kg)", "وزن (کلو گرام)"),
            ("Height (cm)", "قد (سینٹی میٹر)"),
            ("Weight (lb)", "وزن (پاؤنڈ)"),
            ("Height (ft)", "قد (فٹ)"),
            ("Height (in, 0 to 11.9)", "قد (انچ، 0 سے 11.9)"),
            ("Calculate BMI", "BMI کا حساب کریں"),
            ("Units", "اکائیاں"),
        ],
        "how_heading": "فارمولا اور درجہ بندی",
        "faq_heading": "سوالات",
        "how": [
            "میٹرک فارمولا: BMI = وزن (کلو گرام) ÷ قد (میٹر)²۔",
            "امپیریل فارمولا: BMI = 703 × وزن (پاؤنڈ) ÷ قد (انچ)²۔",
            "WHO کے مطابق بالغوں کے لیے: 18.5 سے کم کم وزن، 18.5 سے 24.9 معمول کا وزن، 25.0 سے 29.9 زیادہ وزن، اور 30.0 یا زیادہ موٹاپے کی حد۔",
            "مثال: 70 کلو گرام اور 175 سینٹی میٹر قد پر BMI تقریباً 22.9 ہے، جو معمول کے وزن کی حد میں ہے۔",
            "بچوں اور نوجوانوں کے لیے عمر اور جنس کے مطابق percentile چارٹ استعمال ہوتے ہیں۔ BMI جسمانی چربی کی براہِ راست پیمائش نہیں۔",
        ],
        "faq": [
            ("کیا یہ بچوں کے لیے ہے؟", "نہیں۔ یہ صفحہ بالغوں کے لیے ہے۔ بچوں کے لیے percentile چارٹ استعمال کریں۔"),
            ("کیا BMI تشخیص ہے؟", "نہیں۔ یہ ایک اسکریننگ پیمانہ ہے۔ نتیجہ کسی ڈاکٹر یا معالج سے ضرور ڈسکس کریں۔"),
        ],
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
        "quick": "BMI equals weight in kilograms divided by height in meters squared. For adults, 18.5 to 24.9 is the WHO normal weight range.",
        "faq": [
            ("Is a BMI of 25 unhealthy?", "A BMI of 25 is at the start of the overweight range. It is a screening number only. Waist size, blood pressure and blood tests give a fuller picture, and a clinician can interpret them with you."),
            ("Does BMI work for athletes?", "BMI can overstate body fat in people with high muscle mass. A clinician can use other measures for athletes."),
        ],
    },
    "profit-loss-calculator": {
        "quick": "Profit equals selling price minus cost price. Profit percentage equals profit divided by cost price, multiplied by 100.",
        "faq": [
            ("What is the difference between profit percentage and profit margin?", "Profit percentage uses cost as the base. Profit margin uses selling price as the base. This calculator shows profit percentage on cost."),
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
            ("How many kilograms are in a pound?", "One pound is exactly 0.45359237 kilograms."),
            ("How do I convert Celsius to Fahrenheit?", "Multiply Celsius by 9, divide by 5, then add 32."),
        ],
    },
    "standard-calculator": {
        "quick": "Multiplication and division run before addition and subtraction. The percent key divides the last number by 100.",
        "faq": [
            ("Does this calculator handle parentheses?", "Not in this version. Calculate the inner part first, then enter the result."),
        ],
    },
    "tasbih-counter": {
        "quick": "Each tap adds one. Choose 33, 100, 1000 or unlimited as the target. The count is kept on this device only.",
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


DIGIT = "bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-600 text-stone-900 dark:text-stone-100 text-xl font-semibold rounded-xl min-h-[56px] shadow-sm hover:bg-stone-100 dark:hover:bg-stone-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
OPS = "bg-gradient-to-br from-fuchsia-600 to-indigo-700 text-white text-xl font-bold rounded-xl min-h-[56px] shadow-md hover:from-fuchsia-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
SPECIAL = "bg-gradient-to-br from-amber-700 to-orange-800 text-white text-lg font-bold rounded-xl min-h-[56px] shadow-md focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"
EQUALS = "bg-gradient-to-br from-emerald-700 to-teal-800 text-white text-2xl font-bold rounded-xl min-h-[56px] shadow-lg col-span-3 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-800"

CALC_UI = (
    '<div class="max-w-sm mx-auto">'
    '<output id="calc-display" class="block text-right text-3xl font-bold bg-stone-50 dark:bg-stone-950 border border-stone-300 dark:border-stone-600 rounded-2xl px-4 py-5 min-h-[4rem] break-all text-stone-900 dark:text-stone-100" aria-live="polite">0</output>'
    '<div id="calc-pad" class="grid grid-cols-4 gap-3 mt-4">'
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
    '<button class="' + SPECIAL + '" data-key="%">%</button>'
    '<button class="' + EQUALS + '" data-key="=">=</button>'
    '</div></div>'
)

for _t in TOOLS:
    _t["guide"] = _t["guide"] + GUIDE_EXTRA.get(_t["slug"], [])
    _t["sources"] = _t["sources"] + " " + REVIEW_STATUS.get(_t["slug"], "")
    if _t["slug"] == "standard-calculator":
        _t["ui"] = CALC_UI


def home_extra_html(lang):
    block = HOME_EXTRA[lang]
    out = '<h2 class="' + H2 + '">' + block["heading"] + "</h2>"
    for p in block["paragraphs"]:
        out += '<p class="' + P + '">' + p + "</p>"
    heading = "سوالات" if lang == "ur" else "Questions"
    out += '<h2 class="' + H2 + '">' + heading + '</h2><div class="mt-3">' + faq_html(block["faq"]) + "</div>"
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
    client = os.environ.get("ADSENSE_CLIENT", "").strip()
    line = "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0"
    if client:
        pub = client.replace("ca-pub-", "pub-")
        if not pub.startswith("pub-") or not pub[4:].isdigit():
            raise SystemExit("ADSENSE_CLIENT must look like ca-pub-1234567890123456")
        line = "google.com, " + pub + ", DIRECT, f08c47fec0942fa0"
    with open(os.path.join(OUT, "ads.txt"), "w", encoding="utf-8") as f:
        f.write(line + "\n")
    return bool(client)


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
    if not ADSENSE_CLIENT:
        return ""
    return ('<div class="my-10 min-h-[100px]" aria-label="Advertisement">'
            '<ins class="adsbygoogle" style="display:block" data-ad-client="' + ADSENSE_CLIENT + '" '
            'data-ad-format="auto" data-full-width-responsive="true"></ins></div>')


def nav_items(lang="en"):
    items = ""
    for t in TOOLS:
        if lang == "ur":
            if t["slug"] not in URDU:
                continue
            name = URDU[t["slug"]]["name"]
            href = "/ur/" + t["slug"]
        else:
            name = t["name"]
            href = "/" + t["slug"]
        items += '<li><a class="' + LINK + '" href="' + href + '">' + name + "</a></li>"
    return items



LANG_LOCALE = {"en": "en_US", "ur": "ur_PK", "ar": "ar_AR", "hi": "hi_IN", "es": "es_ES", "fr": "fr_FR"}
RTL_LANGS = ("ur", "ar")
SHELL_EN = {"menu": "All tools", "skip": "Skip to content", "about": "About", "privacy": "Privacy", "contact": "Contact",
            "methodology": "Methodology", "editorial": "Editorial policy", "tag": "© CalculatesAll. Free tools that run in your browser.",
            "theme": "Dark mode", "lang": "Languages", "terms": "Terms of use"}
SHELL_UR = {"menu": "تمام ٹولز", "skip": "مرکزی مواد پر جائیں", "about": "ہمارے بارے میں", "privacy": "رازداری", "contact": "رابطہ",
            "methodology": "طریقہ کار", "editorial": "ادارتی پالیسی", "tag": "© CalculatesAll۔ مفت ٹولز جو آپ کے براؤزر میں چلتے ہیں۔",
            "theme": "ڈارک موڈ", "lang": "زبانیں", "terms": "شرائط استعمال"}
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
    return merged


def home_alts_all():
    return [(l["code"], l["path"]) for l in LANGS] + [("x-default", "/")]


def head(title, desc, path, schema, lang="en", noindex=False, alternates=None):
    url = SITE_URL + path
    robots = "noindex, follow" if noindex else "index, follow"
    alt = ""
    if alternates:
        for code, href in alternates:
            alt += '<link rel="alternate" hreflang="' + code + '" href="' + SITE_URL + href + '">\n'
    ads = ""
    if ADSENSE_CLIENT:
        ads = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
               + ADSENSE_CLIENT + '" crossorigin="anonymous"></script>\n')
    ld = ""
    for s in schema:
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
        '<link rel="canonical" href="' + url + '">\n'
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
        '<meta name="theme-color" content="#f0f9ff">\n'
        + theme_script
        + '<link rel="stylesheet" href="/assets/site.css">\n'
        + ld + ads + "</head>\n"
    )


def lang_links(lang, s):
    items = ""
    for l in LANGS:
        if l["code"] == lang:
            continue
        items += ('<li><a class="' + LINK + ' min-h-[44px] inline-flex items-center" hreflang="' + l["code"]
                  + '" href="' + l["path"] + '">' + l["name"] + "</a></li>")
    return ('<nav aria-label="' + s["lang"] + '" class="mt-2"><ul class="flex flex-wrap gap-x-5 gap-y-1 text-sm">'
            + items + "</ul></nav>")


def shell(main_html, lang="en"):
    s = shell_strings(lang)
    home = "/" if lang == "en" else "/" + lang + "/"
    return (
        '<body class="min-h-screen bg-gradient-to-br from-indigo-100 via-sky-50 to-fuchsia-100 dark:from-stone-950 dark:via-stone-900 dark:to-indigo-950 text-stone-900 dark:text-stone-100 antialiased">\n'
        '<div aria-hidden="true" class="pointer-events-none fixed inset-0 -z-10 overflow-hidden">'
        '<div class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-fuchsia-300/40 blur-3xl"></div>'
        '<div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full bg-sky-300/40 blur-3xl"></div>'
        '<div class="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-emerald-300/30 blur-3xl"></div></div>\n'
        '<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:bg-white focus:px-3 focus:py-2 focus:rounded">' + s["skip"] + '</a>\n'
        '<div class="h-1.5 bg-gradient-to-r from-fuchsia-500 via-sky-500 to-emerald-500"></div>'
        '<header class="sticky top-0 z-20 bg-white/80 dark:bg-stone-900/80 backdrop-blur border-b border-stone-200 dark:border-stone-700 shadow-sm">'
        '<nav class="max-w-5xl mx-auto px-5 py-3 flex items-center justify-between gap-4" aria-label="Main">'
        '<a href="' + home + '" class="font-extrabold text-xl bg-gradient-to-r from-fuchsia-600 via-indigo-600 to-sky-600 bg-clip-text text-transparent min-h-[44px] inline-flex items-center">CalculatesAll</a>'
        '<div class="flex items-center gap-3">'
        '<button id="theme-toggle" type="button" class="' + S + ' min-h-[44px]">' + s["theme"] + '</button>'
        '<details class="relative"><summary class="cursor-pointer text-base min-h-[44px] inline-flex items-center px-2">' + s["menu"] + '</summary>'
        '<ul class="absolute right-0 mt-2 w-64 bg-white border border-stone-300 rounded-lg p-3 space-y-2 text-base shadow-lg z-10">'
        + nav_items("ur" if lang == "ur" else "en")
        + '</ul></details></div></nav></header>\n'
        '<main id="main" class="max-w-3xl mx-auto px-5 py-10">' + main_html + '</main>\n'
        '<footer class="mt-12 bg-white/80 dark:bg-stone-900/80 backdrop-blur border-t border-stone-200 dark:border-stone-700">'
        '<div class="max-w-5xl mx-auto px-5 py-8 flex flex-col gap-4 text-sm text-stone-800">'
        '<div class="flex flex-col sm:flex-row gap-4 sm:items-center sm:justify-between">'
        '<p>' + s["tag"] + '</p>'
        '<nav class="flex flex-wrap gap-5" aria-label="Footer">'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/about">' + s["about"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/privacy">' + s["privacy"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/contact">' + s["contact"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/methodology">' + s["methodology"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/editorial-policy">' + s["editorial"] + '</a>'
        '<a class="' + LINK + ' min-h-[44px] inline-flex items-center" href="/terms">' + s["terms"] + '</a>'
        '</nav></div>'
        + lang_links(lang, s) +
        '</div></footer>\n'
        '<script src="/assets/app.js" defer></script>\n'
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
        {"@context": "https://schema.org", "@type": "WebSite", "name": "CalculatesAll", "url": SITE_URL + path, "inLanguage": code},
        {"@context": "https://schema.org", "@type": "Organization", "name": "CalculatesAll", "url": SITE_URL + "/",
         "logo": SITE_URL + "/assets/favicon.svg"},
    ]
    write(path, head(u["title"], u["desc"], path, schema, lang=code, alternates=home_alts_all()) + shell(body, lang=code))
    return path



def fill(s):
    return s.replace("@L@", L).replace("@I@", I).replace("@B@", B).replace("@S@", S).replace("@R@", R)


def write(path, content):
    rel = path.strip("/")
    folder = os.path.join(OUT, rel) if rel else OUT
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(fill(content))


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
    if path == "/standard-calculator/":
        return doc.replace('<link rel="canonical" href="' + SITE_URL + path + '">', '<link rel="canonical" href="' + SITE_URL + '/">')
    if path == "/ur/standard-calculator/":
        return doc.replace('<link rel="canonical" href="' + SITE_URL + path + '">', '<link rel="canonical" href="' + SITE_URL + '/ur/">')
    return doc


def tool_page(t):
    path = "/" + t["slug"] + "/"
    url = SITE_URL + path
    cat = next(c for c in CATEGORIES if c["slug"] == t["category"])
    title = t["name"] + " | Free Online Tool | CalculatesAll"
    desc = t["description"]
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": url,
         "description": desc, "applicationCategory": t["app"], "operatingSystem": "Any",
         "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": cat["name"], "item": SITE_URL + "/" + cat["slug"] + "/"},
            {"@type": "ListItem", "position": 3, "name": t["name"], "item": url}]},
    ]
    related = ""
    for other in TOOLS:
        if other["slug"] != t["slug"] and other["category"] == t["category"]:
            related += '<li><a class="' + LINK + '" href="/' + other["slug"] + '">' + other["name"] + "</a></li>"
    alternates = None
    if t["slug"] in URDU:
        alternates = [("en", path), ("ur", "/ur" + path), ("x-default", path)]
    updated = '<p class="mt-8 text-sm text-stone-800 dark:text-stone-200">Last updated: ' + LAST_REVIEWED + ". " + t["sources"] + "</p>"
    body = (
        '<nav aria-label="Breadcrumb" class="text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap gap-2">'
        '<li><a class="' + LINK + '" href="/">Home</a></li><li aria-hidden="true">/</li>'
        '<li><a class="' + LINK + '" href="/' + cat["slug"] + '/">' + cat["name"] + '</a></li><li aria-hidden="true">/</li>'
        '<li aria-current="page">' + t["name"] + "</li></ol></nav>"
        '<h1 class="text-3xl font-extrabold bg-gradient-to-r from-fuchsia-700 via-indigo-700 to-sky-700 bg-clip-text text-transparent mt-4"><span aria-hidden="true">' + TILE_ICON.get(t["slug"], "") + '</span> ' + t["h1"] + '</h1>'
        '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + t["lead"] + '</p>'
        '<section class="mt-8 rounded-2xl bg-white/95 dark:bg-stone-900/95 shadow-xl ring-1 ring-stone-200 dark:ring-stone-700 p-5 sm:p-6" aria-label="Calculator">' + t["ui"] + '</section>'
        + ad_slot()
        + '<p class="mt-8 rounded-xl bg-sky-50 dark:bg-sky-950 border border-sky-200 dark:border-sky-800 p-5 text-base text-stone-900 dark:text-stone-100"><strong>Quick answer.</strong> ' + EXTRA[t["slug"]]["quick"] + '</p>'
        + guide_html(t["guide"])
        + '<h2 class="' + H2 + '">Questions</h2><div class="mt-3">' + faq_html(t["faq"] + EXTRA[t["slug"]]["faq"]) + "</div>"
        + updated
        + review_box(t["slug"])
        + '<section class="mt-12"><h2 class="text-xl font-semibold text-stone-900 dark:text-stone-100">More in ' + cat["name"] + '</h2>'
        '<ul class="mt-3 grid sm:grid-cols-2 gap-2 text-base">' + related + "</ul></section>"
    )
    rs = reviewer_schema(t["slug"])
    if rs:
        schema.append(rs)
    write(path, canon_override(head(title, desc, path, schema, alternates=alternates) + shell(body), path))
    return path


def urdu_tool_page(t):
    u = URDU[t["slug"]]
    path = "/ur/" + t["slug"] + "/"
    url = SITE_URL + path
    ui = t["ui"]
    for en, ur in u["labels"]:
        ui = ui.replace(">" + en + "<", ">" + ur + "<")
        ui = ui.replace('"' + en + '"', '"' + ur + '"')
    schema = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": u["name"], "url": url,
         "description": u["description"], "inLanguage": "ur", "applicationCategory": t["app"],
         "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
    ]
    how = ""
    for p in u["how"]:
        how += '<p class="' + P + '">' + p + "</p>"
    faq = faq_html(u["faq"])
    body = (
        '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100 mt-4">' + u["h1"] + '</h1>'
        '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + u["lead"] + '</p>'
        '<section class="mt-8" aria-label="کیلکولیٹر">' + ui + '</section>'
        '<h2 class="' + H2 + '">' + u["how_heading"] + '</h2>' + how
        + '<h2 class="' + H2 + '">' + u["faq_heading"] + '</h2><div class="mt-3">' + faq + "</div>"
        + '<p class="mt-10 text-sm text-stone-800 dark:text-stone-200"><a class="' + LINK + '" href="/' + t["slug"] + '/" hreflang="en">انگریزی ورژن</a></p>'
    )
    alternates = [("en", "/" + t["slug"] + "/"), ("ur", path), ("x-default", "/" + t["slug"] + "/")]
    write(path, canon_override(head(u["title"], u["description"], path, schema, lang="ur", alternates=alternates) + shell(body, lang="ur"), path))
    return path


def category_page(c):
    path = "/" + c["slug"] + "/"
    items = ""
    for t in TOOLS:
        if t["category"] == c["slug"]:
            items += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                      '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/' + t["slug"] + '">' + t["name"] + "</a>"
                      '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + t["description"] + "</p></li>")
    title = c["name"] + " | CalculatesAll"
    schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": c["name"], "url": SITE_URL + path}]
    body = ('<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">' + c["name"] + '</h1>'
            '<p class="mt-3 text-lg text-stone-900 dark:text-stone-100">' + c["desc"] + '</p>'
            '<p class="mt-4 text-base leading-relaxed text-stone-800 dark:text-stone-200">' + HUB_CONTENT[c["slug"]]["intro"] + '</p>'
            '<ul class="mt-8 grid gap-4">' + items + "</ul>"
        + guide_html(HUB_EXTRA[c["slug"]]) +
            '<h2 class="' + H2 + '">Questions</h2><div class="mt-3">' + faq_html(HUB_CONTENT[c["slug"]]["faq"]) + "</div>")
    write(path, head(title, c["desc"], path, schema) + shell(body))
    return path


def static_page(path, title, desc, h1, paragraphs, noindex=False):
    schema = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": SITE_URL + path}]
    body = '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">' + h1 + '</h1>'
    for p in paragraphs:
        body += '<p class="' + P + '">' + p + "</p>"
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
        h1 = "Free Online Calculators and Utility Tools"
        lead = "CalculatesAll has calculators for money, health, dates, units and daily use. Each tool runs in your browser, and your entries are not sent to our server."
        cards = ""
        for c in CATEGORIES:
            cards += ('<li class="rounded-xl bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 p-5">'
                      '<a class="text-lg font-semibold text-sky-800 dark:text-sky-300 underline min-h-[44px] inline-flex items-center" href="/' + c["slug"] + '/">' + c["name"] + "</a>"
                      '<p class="mt-2 text-base text-stone-800 dark:text-stone-200">' + c["desc"] + "</p></li>")
    alternates = home_alts_all()
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "CalculatesAll", "url": SITE_URL + "/", "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "Organization", "name": "CalculatesAll", "url": SITE_URL + "/",
         "logo": SITE_URL + "/assets/favicon.svg"},
    ]
    body = (
        '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100 mt-2">' + h1 + '</h1>'
        '<p class="mt-4 text-lg text-stone-900 dark:text-stone-100">' + lead + '</p>'
        '<ul class="mt-10 grid gap-4">' + cards + "</ul>" + home_extra_html(lang)
    )
    write(path, head(title, desc, path, schema, lang=lang, alternates=alternates) + shell(body, lang=lang))
    return path


STEPS = {
    "en": [("Step 1", "Type your numbers on the calculator."), ("Step 2", "Tap = to see the answer."), ("Step 3", "Tap any coloured button to open another tool.")],
    "ur": [("پہلا قدم", "کیلکولیٹر پر اپنے نمبر لکھیں۔"), ("دوسرا قدم", "جواب دیکھنے کے لیے = دبائیں۔"), ("تیسرا قدم", "کسی دوسرے ٹول کے لیے کوئی رنگین بٹن دبائیں۔")],
}

TILE_GRAD = {
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
    path = "/ur/" if urdu else "/"
    if urdu:
        title = "معیاری کیلکولیٹر | CalculatesAll"
        desc = "مفت آن لائن معیاری کیلکولیٹر۔ رنگین بٹنوں سے زکوٰۃ، BMI، منافع، عمر، ڈسکاؤنٹ اور یونٹ کنورٹر کھولیں۔"
        h1 = "معیاری کیلکولیٹر"
        lead = "یہ ایک سادہ کیلکولیٹر ہے۔ دوسرا ٹول کھولنے کے لیے نیچے کا کوئی رنگین بٹن دبائیں۔"
        more_h = "دوسرے ٹولز"
    else:
        title = "Standard Calculator | Free Online Calculators | CalculatesAll"
        desc = "Free online standard calculator. Open Zakat, BMI, profit and loss, age, discount, unit converter and more with one tap."
        h1 = "Standard Calculator"
        lead = "A simple calculator for everyday sums. To open another tool, tap one of the colourful buttons below."
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
    cats = ""
    if not urdu:
        for c in CATEGORIES:
            cats += ('<li><a class="rounded-full px-4 py-2 text-sm font-semibold min-h-[44px] inline-flex items-center '
                     + CAT_PILL[c["slug"]] + '" href="/' + c["slug"] + '/">' + c["name"] + "</a></li>")
        cats = '<nav aria-label="Categories" class="mt-8"><ul class="flex flex-wrap gap-3">' + cats + "</ul></nav>"
    hero = ('<div class="rounded-3xl p-[3px] bg-gradient-to-r from-fuchsia-500 via-sky-500 to-emerald-500 shadow-2xl">'
            '<div class="rounded-3xl bg-white/95 dark:bg-stone-900/95 p-4 sm:p-6">'
            '<section aria-label="Calculator">' + CALC_UI + "</section></div></div>")
    body = (
        '<h1 class="text-3xl font-extrabold bg-gradient-to-r from-fuchsia-700 via-indigo-700 to-sky-700 bg-clip-text text-transparent dark:from-fuchsia-300 dark:to-sky-300 mt-2">' + h1 + "</h1>"
        '<p class="mt-3 text-lg text-stone-800 dark:text-stone-200">' + lead + "</p>"
        '<div class="mt-6">' + hero + "</div>"
        '<ul class="mt-6 grid grid-cols-3 gap-3">' + trust + "</ul>"
        + '<ol class="mt-6 grid gap-3 sm:grid-cols-3">' + "".join('<li class="rounded-xl bg-white/90 dark:bg-stone-900/90 p-4 shadow ring-1 ring-stone-200 dark:ring-stone-700 text-base text-stone-900 dark:text-stone-100"><span class="block text-sm font-bold text-indigo-700 dark:text-indigo-300">' + n + "</span>" + t + "</li>" for n, t in STEPS[lang]) + "</ol>"
        '<h2 class="' + H2 + '">' + more_h + "</h2>"
        '<ul class="mt-4 grid grid-cols-2 gap-4">' + tiles + "</ul>"
        + cats
        + home_extra_html(lang)
    )
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "CalculatesAll", "url": SITE_URL + "/", "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "WebApplication", "name": "Standard Calculator", "url": SITE_URL + "/",
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "Organization", "name": "CalculatesAll", "url": SITE_URL + "/",
         "logo": SITE_URL + "/assets/favicon.svg"},
    ]
    write(path, head(title, desc, path, schema, lang=lang, alternates=home_alts_all()) + shell(body, lang=lang))


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
        items += ("  <url>\n    <loc>" + SITE_URL + path + "</loc>\n    <lastmod>" + LAST_REVIEWED + "</lastmod>\n" + links + "  </url>\n")
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
    assets = os.path.join(OUT, "assets")
    os.makedirs(assets, exist_ok=True)
    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
               '<rect width="64" height="64" rx="12" fill="#0c4a6e"/>'
               '<text x="32" y="42" font-size="30" text-anchor="middle" fill="#ffffff" font-family="Arial, sans-serif" font-weight="bold">CA</text></svg>')
    with open(os.path.join(assets, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(favicon)
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. og-image.png was not generated.")
        return
    img = Image.new("RGB", (1200, 630), (12, 74, 110))
    draw = ImageDraw.Draw(img)
    try:
        big = ImageFont.truetype("DejaVuSans-Bold.ttf", 84)
        small = ImageFont.truetype("DejaVuSans.ttf", 40)
    except OSError:
        big = ImageFont.load_default(size=84)
        small = ImageFont.load_default(size=40)
    draw.text((80, 210), "CalculatesAll", font=big, fill=(255, 255, 255))
    draw.text((80, 330), "Free calculators for money, health, dates and units", font=small, fill=(224, 242, 254))
    draw.text((80, 400), "Zakat | BMI | Profit and Loss | Age | Discount | Converter", font=small, fill=(186, 230, 253))
    img.save(os.path.join(assets, "og-image.png"), "PNG", optimize=True)


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
        ("/about", "About CalculatesAll", "About CalculatesAll, its free tools and how they are built.", "About CalculatesAll", [
            "CalculatesAll is a collection of free online calculators and everyday utility tools.",
            "Calculations run in your browser. The tools do not store your entries on our server.",
            "Religious and health tools state their limits on the page. For a ruling on Zakat or a diagnosis, consult a qualified scholar or health professional.",
        ]),
        ("/privacy", "Privacy Policy | CalculatesAll", "How CalculatesAll handles data, local storage and advertising.", "Privacy Policy", [
            "Calculator inputs are processed in your browser. We do not send them to our server.",
            "The tasbih counter and the stopwatch do not send data anywhere. The tasbih counter keeps its count in local storage on your device. You can clear this from your browser settings.",
            "CalculatesAll does not run its own analytics or accounts. If the site owner enables advertising, Google and its partners may use cookies to show ads. For visitors in the European Economic Area and the United Kingdom, consent for personalized ads is collected through a Google certified consent message configured in the Google AdSense account. Until that message is configured, personalized ads are not shown to those visitors.",
            "Google's use of data is described at policies.google.com. Contact " + CONTACT_EMAIL + " with privacy questions.",
        ]),
        ("/methodology", "How Our Calculations Work | CalculatesAll", "The formulas, data sources and limits behind each CalculatesAll tool.", "How Our Calculations Work", [
            "Each tool uses a published formula. Zakat uses the silver Nisab of 612.36 grams. BMI uses the standard formula with WHO adult categories. Profit, discount, age and unit conversions use standard arithmetic and fixed conversion factors.",
            "Every tool page states its assumptions and limits. When a rule depends on a school of law or a clinical judgement, the page says so and points to a qualified professional.",
            "If you find a formula error, email " + CONTACT_EMAIL + " with the tool name and the inputs. We correct confirmed errors and show the update date on the tool page.",
        ]),
        ("/editorial-policy", "Editorial Policy | CalculatesAll", "How CalculatesAll writes, checks and updates its tool guides.", "Editorial Policy", [
            "Tool guides are written to explain the formula, show a worked example, and list common mistakes. Numbers in worked examples are checked with a calculation before publication.",
            "Religious and health content is labelled as a general guide. For a ruling on Zakat or a diagnosis, consult a qualified scholar or health professional.",
            "Each guide shows a last updated date. Sources are named where they are used, and we do not publish claims that we cannot support with a named source.",
        ]),
        ("/terms", "Terms of Use | CalculatesAll", "The terms for using the free calculators and information on CalculatesAll.", "Terms of Use", TERMS_PARAS),
        ("/contact", "Contact CalculatesAll", "Contact CalculatesAll for corrections, feedback or questions about any calculator. We read every message and publish confirmed corrections on the tool page.", "Contact", [
            "For corrections, feedback or questions about a tool, email " + CONTACT_EMAIL + ".",
        ]),
    ]
    for path, title, desc, h1, paras in static_pages:
        paras = paras + TRUST_EXTRA.get(path, []) + {"/contact": CONTACT_EXTRA, "/about": ABOUT_EXTRA}.get(path, [])
        static_page(path, title, desc, h1, paras)
        entries.append((path, []))
    not_found()
    og_and_favicon()
    entries = [e for e in entries if 'standard-calculator' not in e[0]]
    sitemap(entries)
    robots()
    shutil.copytree(STATIC, os.path.join(OUT, "assets"), dirs_exist_ok=True)
    configured = write_ads_txt()
    print("ads.txt " + ("set from ADSENSE_CLIENT" if configured else "still placeholder (set ADSENSE_CLIENT)"))
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
