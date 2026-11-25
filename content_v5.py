"""Editorial content for CalculatesAll. Edit text here, then run npm run build."""

REVIEW_STATUS = {
    "bmi-calculator": "Formula is weight divided by height squared. Categories follow the adult ranges shown on this page. This tool is not a clinical assessment.",
    "profit-loss-calculator": "Formulas follow the method stated on this page.",
    "discount-calculator": "Formulas follow the method stated on this page.",
    "age-calculator": "Calendar method counts whole years, months and days between the two dates entered.",
    "unit-converter": "Conversions use the factors shown in the worked examples on this page.",
    "standard-calculator": "Expressions follow standard operator precedence, as shown in the examples on this page.",
    "stopwatch": "Elapsed time comes from the browser timer, as described on this page.",
}

GUIDE_EXTRA = {
    "zakat-calculator": [],
    "bmi-calculator": [],
    "profit-loss-calculator": [],
    "discount-calculator": [
        ("Worked example: discount and sales tax", [
            "Suppose an item has a listed price of 2,000, a 15% discount and a 10% sales tax calculated on the discounted price. The discount is 300, the discounted price is 1,700, and the tax is 170. The final amount is 1,870.",
            "If a store calculates tax before applying a discount, the receipt can differ. This example assumes tax is charged on the discounted price. The calculator reports the discount result only and is not a tax-inclusive checkout quote.",
        ]),
        ("Why the order of percentage changes matters", [
            "A 25% discount followed by a 10% price increase leaves a 100-unit starting price at 82.50: first 100 becomes 75, then 75 increases by 7.50. It is not the same as subtracting 15% from the starting price.",
            "For sequential adjustments, apply each percentage to the amount immediately before that step. Keep intermediate values unrounded when calculating a final payable amount, then follow the applicable currency and merchant rounding rules.",
        ]),
        ("Calculate a second discount from the reduced price", [
            "On PKR 4,500, a 20% discount first reduces the price to PKR 3,600. A further 10% applies to PKR 3,600, so it saves PKR 360 and leaves PKR 3,240. The total saving is PKR 1,260, or 28% of the original price, not 30%.",
            "The second percentage uses the reduced amount as its base. Calculate each step in order instead of adding the two percentages together.",
        ]),
        ("Find the original price from a discounted price", [
            "When the final price and discount rate are known, original price = final price ÷ (1 − discount rate). The discount rate must be written as a decimal, and the discount must be below 100%.",
            "Example: a final price of PKR 3,600 after a 20% discount represents 80% of the original price. Therefore 3,600 ÷ 0.80 = PKR 4,500. This reverse calculation does not verify whether a seller's advertised original price was genuine.",
        ]),
    ],
    "age-calculator": [
        ("Worked example: age across a leap day", [
            "A person born on 28 February 2000 is 24 full calendar years old on 28 February 2024. The period from 28 February 2024 to 1 March 2024 spans two elapsed days because 2024 includes 29 February. Calendar age and total elapsed days answer different questions.",
            "When you need an exact day count for a deadline, enter both dates rather than estimating years times 365. The number of leap days depends on the specific years in the interval, and the result can differ by several days over a lifetime.",
        ]),
        ("What a calendar-age result does not tell you", [
            "An age expressed in years, months and days is based on calendar dates, not the time of birth. Two people born on the same date but at different hours will receive the same calendar-age result.",
            "For an official age requirement, verify which date and time zone the issuing authority uses. This calculator does not determine legal eligibility, and a document's rules may differ from an ordinary calendar calculation.",
        ]),
        ("Leap years", [
            "A leap year has 366 days. The extra day falls on 29 February. Leap years occur in years divisible by 4, except years divisible by 100 that are not divisible by 400.",
            "The calculator follows the Gregorian calendar, so day counts include every leap day between the two dates.",
        ]),
        ("Birthdays on 29 February", [
            "For a 29 February birth, this calculator uses 28 February as the anniversary in non-leap years. This is a calculation convention, not a legal rule. Legal age and eligibility rules can differ by jurisdiction, so check the relevant authority for official decisions.",
        ]),
        ("Using the total days figure", [
            "The total days figure is useful for planning, for example counting days until a milestone. It counts whole days, not hours, so the result does not change during the day.",
        ]),
    ],
    "unit-converter": [
        ("Metric and imperial systems", [
            "Most of the world uses the metric system. The United States uses customary units, and the United Kingdom uses imperial units for many everyday measures. Converting between them is common for travel, cooking and building.",
            "The conversion factors used here are exact for the pound, the foot, the inch and the mile. Results are shown to six significant figures.",
        ]),
        ("Worked example with length", [
            "Five kilometres divided by 1.609344 gives 3.10686 miles, rounded to six significant figures.",
            "Converting the rounded value 3.10686 miles back to kilometres gives approximately 5 km, not exactly 5 km. Keep the unrounded value for intermediate steps when a precise round trip matters.",
        ]),
        ("Temperature is different", [
            "Temperature scales have different zero points, so the calculator uses formulas instead of multiplication. Kelvin starts at absolute zero, so it cannot be negative.",
        ]),
    ],
    "standard-calculator": [
        ("Parentheses", [
            "Use parentheses to change the order of operations. For example, (2 + 3) multiplied by 4 is 20, while 2 + 3 multiplied by 4 is 14.",
            "Nested parentheses are also supported. For example, ((1 + 2) multiplied by (3 + 4)) is 21.",
        ]),
        ("Percent key", [
            "The percent key divides the last number by 100. For example, 200 then percent becomes 2, which you can then use in a calculation.",
        ]),
        ("Errors", [
            "Error means the expression is incomplete, for example it ends with an operator or has unmatched parentheses. Cannot divide by zero means the divisor was zero.",
        ]),
    ],
    "stopwatch": [
        ("Starting and stopping", [
            "Press Start when the activity begins and Stop when it ends. Press Reset to clear the display before the next timing.",
            "The display shows hours, minutes, seconds and hundredths of a second, so short intervals are readable.",
        ]),
        ("Accuracy and limits", [
            "The stopwatch uses the browser clock and reads time with high resolution. Your device, browser load and background activity can add small delays to the displayed value.",
        ]),
    ],
}

GUIDE_EXTRA["unit-converter"].append(
    ("Check a conversion without trusting a rounded display", [
        "One international inch is exactly 2.54 centimetres. For example, 12 inches equals 30.48 centimetres. This is a defined relationship, not an estimate.",
        "One international avoirdupois pound is exactly 0.45359237 kilograms. Therefore 10 pounds equals 4.5359237 kilograms before display rounding. A shortened result should not be reused as though it were exact.",
        "Temperature uses an offset as well as a scale factor: Fahrenheit = Celsius x 9 / 5 + 32. For example, 25 degrees Celsius equals 77 degrees Fahrenheit. Do not use the length or weight multiplication method for temperature.",
    ]),
)

# Search Console query-specific worked examples. These complement existing tools;
# they do not create near-duplicate landing pages for the same search intent.
GUIDE_EXTRA.setdefault("years-to-days-calculator", []).append(
    ("Years and months in days: interpreting search questions", [
        "For 29 years, the simple conversion is 29 x 365 = 10,585 days. Using the Gregorian average gives 29 x 365.2425 = 10,592.0325 days. The exact calendar-day total depends on the start and end dates.",
        "For 3 years and 2 months, there is no single exact number of days without calendar dates: months contain 28, 29, 30 or 31 days. Enter the actual dates in the date difference calculator for an exact Gregorian calendar interval.",
        "To convert 800,000 days into approximate years, divide by the chosen year length: 800,000 / 365 = about 2,191.78 simple years, 800,000 / 365.25 = about 2,190.28 Julian years, or 800,000 / 365.2425 = about 2,190.33 Gregorian-average years. This is a duration conversion, not a birth-date calculation.",
    ])
)

# Distinctive, query-matched explanations benchmarked against calculator competitors.
# Keep one canonical page per intent and explain assumptions instead of duplicating pages.

GUIDE_EXTRA["profit-loss-calculator"].extend([
    ("Build cost of goods sold from stock records", [
        "Before entering Business P&L, calculate cost of goods sold (COGS) for the same accounting period: opening inventory + net purchases + direct inward costs − closing inventory, where net purchases exclude the inward freight or handling shown separately. Closing stock remains an asset, so it is not charged to this period's COGS. If your purchase total already includes inward freight or handling, do not add it again. Use a consistent inventory valuation method and avoid counting a purchase, freight charge or item twice.",
        "Worked shop example: opening saleable stock is PKR 100,000, net purchases excluding inward freight are PKR 70,000, direct inward freight and handling are PKR 10,000, and closing saleable stock is PKR 30,000. COGS is PKR 100,000 + PKR 70,000 + PKR 10,000 − PKR 30,000 = PKR 150,000. If net sales for the same period are PKR 220,000, gross profit is PKR 70,000. After PKR 40,000 of other operating expenses, operating profit is PKR 30,000 and operating margin is PKR 30,000 ÷ PKR 220,000 × 100 = 13.64%. Enter PKR 150,000 in the COGS field, not the full purchases figure.",
    ]),
    ("Profit is not the same as cash available", [
        "A business can report operating profit while some customers have not paid. If PKR 35,000 of the example's sales remain unpaid at month-end, that receivable may be part of reported sales but is not money in the bank. Supplier payment timing, stock purchases, loan principal, tax timing and owner withdrawals also change cash movement.",
        "This calculator estimates product profit or a simplified operating result from the values entered. It does not calculate cash flow, working capital, receivables, payables, depreciation or a complete statutory income statement. Reconcile the estimate with your accounting records before using it for tax, lending or formal reporting.",
    ]),
])


GUIDE_EXTRA["profit-loss-calculator"].append(
    ("Load the full per-item cost before trusting product margin", [
        "Product Profit mode accepts one unit-cost figure and one selling price. It does not separately model payment or marketplace fees, customer-acquisition cost, packaging, storage, seller-paid delivery or returns. If you want those costs included in the per-item result, allocate the relevant amount to each unit and include it in the unit-cost input. If you enter purchase cost alone, read the result as pre-fee product contribution, not take-home profit.",
        "Worked example: purchase cost is PKR 1,000 per item, allocated marketplace and payment fees are PKR 60, seller-paid delivery and packaging are PKR 90, and advertising cost per acquired sale is PKR 50. The loaded unit cost is PKR 1,200. At a selling price of PKR 1,500, estimated product profit is PKR 300 and margin is 20%. If you enter only the PKR 1,000 purchase cost, the calculator shows PKR 500 and 33.33% margin before those omitted costs. Do not include the same fee in both loaded unit cost and Business P&L expenses.",
    ])
)

GUIDE_EXTRA["years-to-days-calculator"].append(
    ("365 days, 365.25 days and 365.2425 days per year", [
        "A fixed 365-day year is useful for simple arithmetic. A Julian year is exactly 365.25 days, a fixed duration used in astronomy. The Gregorian mean is 365.2425 days because its 400-year cycle has 97 leap days: (400 x 365 + 97) / 400 = 365.2425. These methods are not identical over long durations.",
        "For 13 years, the simple result is 4,745 days, the Julian-average result is 4,748.25 days, and the Gregorian-average result is 4,748.1525 days. None establishes the exact number of days between two calendar anniversaries without a start date. Use the date difference tool for that question.",
        "A day count of 800,000 is approximately 2,191.78 simple years, 2,190.28 Julian years or 2,190.33 Gregorian-average years. Always state which year length you selected when comparing conversion results from different sites.",
    ])
)


# Original worked examples for query and stopwatch tools.
GUIDE_EXTRA["query-calculator"] = [
    ("Worked examples", [
        "Question: 2 weeks in hours. Step 1: 2 x 7 = 14 days. Step 2: 14 x 24 = 336 hours. Result: 336 hours.",
        "Question: 3 days to minutes. Step 1: 3 x 24 = 72 hours. Step 2: 72 x 60 = 4,320 minutes. Result: 4,320 minutes.",
        "The same chain works in reverse. For a question such as 336 hours to days, each step divides by the same factor instead of multiplying: 336 / 24 = 14 days, and 14 / 7 = 2 weeks.",
    ]),
    ("Checking an answer by hand", [
        "Divide the answer by each factor used in the question, in reverse order. For 4,320 minutes, dividing by 60 gives 72 hours, and dividing by 24 gives 3 days. This check confirms the unit chain and the arithmetic, using the same fixed factors the calculator uses.",
        "Questions about years use the mean Gregorian year of 365.2425 days per year for fixed-unit conversions in this calculator. A birth-date question counts exact Gregorian calendar days between the two dates you enter, so the two methods can differ over long periods.",
    ]),
]
GUIDE_EXTRA["stopwatch"].append(
    ("Worked examples", [
        "A lap time of 83 seconds equals 1 minute and 23 seconds. Step 1: 1 x 60 = 60 seconds. Step 2: 60 + 23 = 83 seconds.",
        "A total of 3,725 seconds equals 1 hour, 2 minutes and 5 seconds. Step 1: 1 x 3,600 = 3,600 seconds. Step 2: 3,725 - 3,600 = 125 seconds. Step 3: 2 x 60 = 120 seconds, leaving 125 - 120 = 5 seconds.",
    ])
)

HOME_EXTRA = {
    "en": {
        "heading": "What can you calculate with these free tools?",
        "paragraphs": [
            "CalculatesAll brings together free browser-based tools for everyday calculations. Use the Zakat calculator to compare silver or gold Nisab methods, enter a supported ISO currency code, list eligible assets and debts, and confirm the lunar-year condition. Pakistan's statutory bank deduction threshold is explained separately. Religious rulings can differ, so review the stated method and consult a trusted qualified scholar for your circumstances.",
            "Use the profit and loss calculator to compare selling price with cost, and the discount calculator to work out savings and a final price. For example, a 20% discount on a price of 1,000 leaves 800 before any applicable tax or fees. Your actual business profit may also depend on shipping, packaging, payment fees, tax and other costs not entered into a simple calculator.",
            "The adult BMI calculator uses weight divided by height squared, with unit handling for metric and imperial inputs. BMI is a screening measure, not a diagnosis, and it does not directly measure body fat. Read the limitations and the World Health Organization's adult BMI information before using the result to discuss health with a clinician: <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index\">WHO body mass index information</a>.",
            "The age calculator works with calendar dates, the unit converter applies defined conversion factors, and the stopwatch and tasbih counter support simple timing and counting tasks. For a reference example, one inch is defined as exactly 25.4 millimetres. See the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.nist.gov/pml/owm/si-units-length\">National Institute of Standards and Technology's length-unit reference</a> for the inch definition.",
            "How are results checked? Each calculator page explains its formula, includes a worked example where it helps, and states important limitations. Worked examples are recalculated whenever a tool changes, and reported errors are corrected on the affected page. For high-stakes financial, medical or religious decisions, confirm the result with a qualified professional.",
            "Calculations are designed to run in your browser without sending calculator entries to our server. The tasbih counter stores its count on your device. The site may load third-party advertising or other resources, which are described in the privacy policy. Avoid entering sensitive personal information into any online tool unless you understand how it handles data.",
            "The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/calorie-calculator/\">adult calorie calculator</a> estimates maintenance energy for adults using the Mifflin–St Jeor equation and a stated activity factor. It is an estimate, not a measured metabolic rate or a diet prescription. The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/emi-calculator/\">EMI calculator</a> estimates a fixed-rate monthly installment and shows a repayment schedule. The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/compound-interest-calculator/\">compound interest calculator</a> models one starting balance at a fixed nominal annual rate and compounding frequency, excluding additional deposits, fees and taxes. The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/percentage-calculator/\">percentage calculator</a> and <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/fraction-calculator/\">fraction calculator</a> explain the arithmetic steps, while the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/date-calculator/\">date calculator</a> counts signed Gregorian calendar days and the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/years-to-days-calculator/\">Years to Days calculator</a> distinguishes fixed-year conversions from exact calendar-date results. The Zakat calculator compares selectable silver or gold Nisab methods, accepts a browser-supported ISO currency code and separates Pakistan's year-specific bank deduction threshold from personal Zakat. It uses user-entered metal prices and does not claim live market data. Read the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/zakat-calculator/\">Zakat method</a> and note that scholarly rulings can differ. The adult BMI tool uses the WHO adult categories: below 18.5, 18.5 to 24.9, 25.0 to 29.9, and 30 or above. See the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight\" rel=\"noopener noreferrer\">WHO fact sheet</a> for context.",
        ],
        "faq": [
            ("Are the calculators free?", "Yes. The calculators and utility tools are free to use."),
            ("Do you store the numbers I enter?", "Calculator entries are processed in your browser and are not sent to our server. The tasbih counter keeps its count on your device. See the privacy policy for third-party resources and advertising."),
            ("Are the results accurate enough for important decisions?", "The tools use stated methods and examples, but results depend on correct inputs and each tool's limitations. Confirm financial, health or religious decisions with an appropriate qualified professional."),
        ],
    },
    "ur": {
        "heading": "CalculatesAll پر آپ کیا کر سکتے ہیں",
        "paragraphs": [
            "CalculatesAll میں وہ ٹولز اکٹھے ہیں جو لوگ ہر ہفتے استعمال کرتے ہیں۔ زکوٰۃ اور منافع کے حساب مالی فیصلوں میں مدد دیتے ہیں۔ BMI بالغوں کے لیے ایک اسکریننگ نمبر دیتا ہے۔ عمر، ڈسکاؤنٹ اور یونٹ کے ٹولز روزمرہ حساب کرتے ہیں۔ اسٹاپ واچ اور تسبیح کاؤنٹر وقت اور ذکر کے لیے ہیں۔",
            "ہر ٹول کا صفحہ اس کا فارمولا، ایک مثال اور اس کی حدود بتاتا ہے۔ اس سے آپ نتیجہ خود جانچ سکتے ہیں اور جان سکتے ہیں کہ کب کسی ماہر سے رجوع کرنا ہے۔",
            "مالی حساب کے لیے زکوٰۃ کیلکولیٹر میں اپنی کرنسی کا ISO کوڈ، چاندی یا سونے کا نصاب، اثاثے، قابلِ کٹوتی قرض اور متعلقہ دھات کی فی گرام قیمت درج کریں۔ پاکستان کی بینک کٹوتی کی سرکاری حد ذاتی شرعی نصاب سے الگ بیان کی گئی ہے۔ منافع اور نقصان کے ٹول میں قیمت خرید اور قیمت فروخت ایک ہی کرنسی میں لکھیں۔ ڈسکاؤنٹ کیلکولیٹر اصل قیمت اور رعایت کا فیصد استعمال کرتا ہے، مگر ٹیکس، شپنگ اور دکان کی اضافی فیس خود شامل نہیں کرتا۔",
            "صحت کے لیے BMI کیلکولیٹر بالغ افراد کے وزن اور قد سے ایک عمومی اسکریننگ نمبر نکالتا ہے، تشخیص نہیں کرتا۔ عمر کیلکولیٹر تاریخ پیدائش سے سال، مہینے اور دن گنتا ہے، جبکہ یونٹ کنورٹر وزن، لمبائی اور درجہ حرارت کی اکائیاں بدلتا ہے۔ نتیجہ استعمال کرنے سے پہلے درج کردہ اکائیوں اور مثال کو دوبارہ دیکھیں۔",
            "تسبیح کاؤنٹر کی گنتی اسی آلے کے براؤزر میں رہتی ہے اور ڈیٹا صاف کرنے سے مٹ سکتی ہے۔ اسٹاپ واچ روزمرہ کاموں کے وقت کے لیے ہے، سرکاری کھیلوں یا سائنسی پیمائش کے لیے تصدیق شدہ آلے کا متبادل نہیں۔ حساب براؤزر میں کیا جاتا ہے، تاہم اہم مالی، طبی یا دینی فیصلے کے لیے متعلقہ ماہر سے تصدیق ضروری ہے۔",
        ],
        "faq": [
            ("کیا یہ کیلکولیٹر مفت ہیں؟", "ہاں۔ CalculatesAll کے تمام ٹولز مفت ہیں۔"),
            ("کیا آپ کے درج کردہ اعداد محفوظ ہوتے ہیں؟", "نہیں۔ حساب آپ کے براؤزر میں ہوتا ہے۔ تسبیح کاؤنٹر گنتی صرف آپ کے آلے پر رکھتا ہے۔"),
        ],
    },
}

TRUST_EXTRA = {
    "/about": [
        "CalculatesAll exists to give clear, checkable calculations in one place. Each tool explains its formula and its limits, so you can see how a number was produced.",
        "We do not sell your data and we do not run accounts. If the site shows advertising, the advertising partner follows its own policies, which are described on the privacy page.",
    ],
    "/contact": [
        "Use this address for corrections, feedback, accessibility problems and Urdu translation fixes. Please include the tool name, the inputs you used and the result you expected.",
        "We read every message. Confirmed formula or content errors are corrected on the affected tool page.",
    ],
    "/methodology": [
        "Zakat compares eligible net wealth with the selected silver or gold Nisab, uses the metal price and ISO currency entered by the user, and applies 2.5 percent only when the selected threshold and lunar-year conditions are confirmed. Pakistan's statutory bank deduction threshold is a separate year-specific rule.",
        "BMI uses weight divided by height squared in metric units, and the equivalent 703 factor in imperial units. Categories follow the World Health Organization adult ranges.",
        "Profit and discount calculations use percentages with a clear base. Age is calculated from calendar dates on the Gregorian calendar. Unit conversions use fixed factors from published definitions.",
        "For a money calculation, the most important first check is the base used for the percentage. Profit percentage is calculated on cost price, while a discount is calculated on the original price. A business margin uses selling price as its base, so it should not be confused with markup. If shipping, taxes, platform charges or refunds affect the real result, include them separately rather than assuming a simple calculator knows those costs.",
        "For unit conversions, weight and length use defined conversion factors, while temperature requires offset formulas. Celsius and Fahrenheit do not share the same zero point. Results may be rounded for readability, so retain extra digits for intermediate calculations when precision matters. Age uses calendar dates because months have different lengths and leap years affect total days.",
        "A calculation page should make its assumptions visible, provide a checkable example and state what it does not model. These pages are designed for transparent everyday arithmetic. They are not a substitute for an accountant, clinician, qualified religious scholar or certified measurement instrument when a decision requires professional judgement."
    ],
    "/editorial-policy": [
        "Where a page has been checked against a stated method or official source, the page names that source. We do not claim review by a doctor, scholar or other expert unless that review has actually taken place.",
        "Worked examples are calculated before they are published and are recalculated when a tool changes.",
        "Content quality checks focus on accuracy, usefulness, and clear limits rather than repeating search phrases. Calculator pages should answer the main user question near the top, define the inputs, explain the formula, show a worked example where it helps, and answer common follow-up questions. Category pages should help visitors choose the right tool rather than repeat the same paragraph for every calculator.",
        "Before a change is published, each calculator is tested with representative inputs, including boundary values and invalid entries, so that errors are shown clearly instead of producing a misleading number.",
        "We prefer official or primary references for definitions and factual claims. Health content is general information and should not be presented as a diagnosis. Zakat guidance states the method used and acknowledges that religious rulings can differ. Conversion factors should match recognised definitions, and example arithmetic should be reproducible from the numbers shown.",
        "A correction should include the page URL, input values, the displayed result and the expected result or source. Confirmed errors are corrected and the calculator is re-tested before the update is published. We avoid inventing review dates, expert endorsements, user testimonials or performance claims that cannot be verified."
    ],
    "/privacy": [
        "You can ask us about the personal information we hold about you by contacting the address on the contact page. Because the calculators run in your browser, we normally hold no personal information about you.",
    ],
}


# Required page sections for the site-side AdSense content checks.
# Keep these explanations tied to each tool's actual behaviour and stated assumptions.
GUIDE_EXTRA["stopwatch"].extend([
    ("Worked example", [
        "If a timing starts at 0 seconds and stops at 83 seconds, the elapsed interval is 83 seconds, or 1 minute and 23 seconds. For a longer interval of 3,725 seconds, divide by 3,600 to get 1 hour with 125 seconds remaining, then divide 125 by 60 to get 2 minutes with 5 seconds remaining.",
    ]),
    ("Method", [
        "Elapsed time is the difference between the recorded stop point and start point. A lap is a checkpoint within the same timing session, while Reset clears the current session so a new interval can be measured.",
    ]),
    ("Limits", [
        "A browser stopwatch is suitable for everyday timing, workouts and study sessions, not certified sports, laboratory or legal measurement. Device scheduling, background tabs and browser load can delay display updates, so do not rely on hundredths of a second as a certified accuracy guarantee.",
    ]),
])


GUIDE_EXTRA["query-calculator"].extend([
    ("Worked example", [
        "Question: 4 hours in minutes. One hour contains 60 minutes, so 4 x 60 = 240 minutes. To check the answer, divide 240 by 60 and confirm that the result is 4 hours.",
    ]),
    ("Method", [
        "For a supported unit conversion, identify the starting unit, apply the conversion factor for that unit pair, and label the result with the target unit. Reverse conversions use the inverse factor. Calendar questions are handled as dates rather than treating every month as an identical number of days.",
    ]),
    ("Limits", [
        "The query tool supports defined question patterns rather than every possible natural-language request. Ambiguous wording, unsupported units or missing date details can prevent a reliable answer. For exact days between calendar dates, provide the relevant start and end dates instead of assuming a month has a fixed length.",
    ]),
])


# Phase 1 priority-page additions: query-specific examples and practical limits.

GUIDE_EXTRA["profit-loss-calculator"].append(
    ("Pakistan shop example: include direct selling costs", [
        "Suppose a shop buys an item for PKR 800 and pays PKR 50 freight plus PKR 30 packaging before sale. If those direct costs are included, the product cost is PKR 880. Selling it for PKR 1,100 gives PKR 220 profit. Markup on cost is 220 / 880 x 100 = 25%, while gross margin on selling price is 220 / 1,100 x 100 = 20%.",
        "If the PKR 50 freight and PKR 30 packaging are not included in the product cost, the displayed product profit will be overstated by PKR 80. Enter the full cost relevant to the calculation, and keep tax, refunds, platform charges and other operating expenses separate unless the selected mode and inputs include them.",
    ])
)

# Focused educational depth for the Zakat, BMI and profit/loss tools.
# Zakat guidance is maintained in build.py's bilingual Zakat page entry.
GUIDE_EXTRA["profit-loss-calculator"].extend([
    ("When product profit differs from operating profit", [
        "Suppose a business records PKR 100,000 in revenue, PKR 60,000 in cost of goods sold and PKR 15,000 in entered operating expenses. Gross profit is PKR 40,000. Net operating profit is PKR 25,000, and operating margin is PKR 25,000 ÷ PKR 100,000 × 100 = 25%. This business-level result is not the same as the markup or gross margin on one product.",
        "Product mode compares one item's cost price with its selling price. Business mode uses total revenue, cost of goods sold and the other operating expenses entered. Costs not entered, including interest, tax, refunds or other charges, are not inferred. Use the mode that matches the question and reconcile the estimate with invoices and business records.",
    ]),
])

GUIDE_EXTRA["years-to-days-calculator"].append(
    ("Search questions about years, months and exact dates", [
        "A question such as 'how many days are in 10 years?' has more than one valid answer unless the year convention is stated. The simple method gives 3,650 days, the Julian average gives 3,652.5 days, and the Gregorian average gives 3,652.425 days. An actual ten-year calendar interval can contain a different whole-day total depending on its start and end dates.",
        "A question such as 'how many days are in 3 years and 2 months?' cannot have one exact answer without calendar dates because months have 28, 29, 30 or 31 days. Use the Date Difference Calculator with the actual start and end dates when an exact calendar count is required.",
    ])
)
# Commit 5: consolidated Years-to-Days guide, verified against the calculator implementation.
GUIDE_EXTRA["years-to-days-calculator"] = [
    ("Choose a conversion method", [
        "Convert years to days by multiplying by the selected year length, or days to years by dividing by it. Forward results also show weeks, hours, minutes and seconds; reverse results include decimal years and an estimated years, months and days breakdown.",
        "The 365-day option is a simple convention. A Julian year is exactly 365.25 days. The Gregorian average is 365.2425 days across its 400-year cycle, which contains 97 leap days. These fixed lengths estimate durations; exact calendar mode uses an actual Gregorian start date.",
    ]),
    ("Formulas and precision", [
        "Days = Years × Selected days per year. Decimal years = Days ÷ Selected days per year. Weeks = days ÷ 7; hours = days × 24; minutes = days × 1,440; seconds = days × 86,400.",
        "Results display up to eight decimal places. Fixed conversions are durations, not clock-time, time-zone or daylight-saving calculations.",
    ]),
    ("Fixed-year conversion: 80 years", [
        "For 80 years, the 365-day method gives 29,200 days, the 365.25-day Julian method gives 29,220 days, and the 365.2425-day Gregorian average gives 29,219.4 days. For a 10-year comparison, the same methods give 3,650 days, 3,652.5 days and 3,652.425 days. For exact calendar dates, this calculator counts whole calendar days between anniversaries.",
    ]),
    ("Exact calendar years from a start date", [
        "An average cannot give exact days between anniversaries. Select Years to days, choose Exact calendar years, then enter a Gregorian start date and whole years.",
        "It counts up to, but excludes, the ending anniversary. Results include days, whole weeks plus leftover days, hours, minutes, seconds, the exclusive end date and leap days included.",
        "1 January 2024 to 1 January 2028 is 1,461 days, including 29 February 2024. A 29 February start uses 1 March when the ending year is not a leap year: 29 February 2024 plus one year ends exclusively on 1 March 2025, after 366 days. Exact mode accepts whole years only.",
    ]),
    ("Days to years: estimated breakdown", [
        "In Days to years, the selected fixed year length converts the input to decimal years and an estimated years/months/days breakdown. Average month length is the selected year length divided by 12.",
        "Search example: How many years and months are in 1,188 days? Using 365.2425, the result is about 3.25263352 years, or 3 years, 3 average months and 0.96 days. The average month is 30.436875 days. This is not an exact age because months have 28, 29, 30 or 31 days.",
        "1,009 days is 2.76438356 years using a 365-day year, 2.76249144 years using the 365.25-day Julian average, or 2.76254817 years using the 365.2425-day Gregorian average. Using average Gregorian months, the same duration is about 2 years, 9 months and 4.58 days. This is an estimate, not an exact calendar age. Use actual start and end dates when calendar months matter.",
    ]),
    ("Input limits and related tools", [
        "Inputs range from 0 to 1,000,000. Fixed methods accept decimals. Exact mode requires whole years, a valid Gregorian date from 1 January 0001 to 31 December 9999, and an ending year no later than 9999. Invalid dates and unsupported values are rejected.",
        "For two dates, use the <a href='/date-calculator/'>Date Difference Calculator</a>. For age from a birth date, use the <a href='/age-calculator/'>Age Calculator</a>.",
    ]),
]


# Search Console-backed language additions. These sections answer real query wording
# without changing calculator controls, formulas, page URLs or first-screen layout.
GUIDE_EXTRA.setdefault("tasbih-counter", []).append(
    ("Tasbih calculator and free online Tasbeeh counter", [
        "People searching for a Tasbih calculator, a tasbih counter online, calculator tasbih or a free online Tasbeeh counter are usually looking for a simple way to record dhikr counts. This page records deliberate taps, supports preset or custom phrases and targets, and provides undo and reset controls.",
        "It is a counting tool only. It does not listen to recitation, verify pronunciation or determine a religious ruling.",
    ])
)

GUIDE_EXTRA["profit-loss-calculator"].append(
    ("Using an online profit and loss calculator", [
        "This online profit and loss calculator has two distinct modes. Business P&L estimates gross profit and net operating profit from revenue, cost of goods sold and entered expenses. Product profit compares a selling price with its cost price and shows profit or loss, markup and gross margin.",
        "A profit and loss calculator online is only as complete as the amounts entered. Include relevant direct costs, keep all amounts in one currency, and check whether taxes, refunds, platform charges or other expenses are outside the selected inputs.",
    ])
)

GUIDE_EXTRA["unit-converter"].append(
    ("Can centimeters be converted to pounds or kilograms?", [
        "No direct conversion exists between centimeters and pounds or kilograms. Centimeters measure length, while pounds and kilograms measure mass. A question such as 'how many centimeters are in a pound', or a request for cm to kg or cm to lb, mixes different physical quantities, so there is no valid conversion factor.",
        "Use the length category to convert centimeters to inches, or the weight category to convert pounds to kilograms. Convert like quantities only.",
    ])
)


GUIDE_EXTRA["profit-loss-calculator"].append(
    ("Gross profit, operating profit and net profit are different measures", [
        "A gross profit calculator, operating profit calculator and profit margin calculator answer related but different questions. In Business P&L mode, gross profit = revenue − cost of goods sold. Operating profit = gross profit − the operating expenses entered. Each margin is the relevant profit divided by revenue and multiplied by 100. Product mode instead compares one item’s selling price with its entered cost to show product profit, markup and gross margin.",
        "This calculator does not calculate net profit after interest and tax. It also does not calculate break-even sales, because those measures require additional inputs that these modes do not collect. Do not treat operating profit as take-home profit or as a complete financial statement. Reconcile the estimate with the full accounting records before making a business or tax decision.",
    ])
)
