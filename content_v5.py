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
    "zakat-calculator": [
        ("Who must pay Zakat", [
            "Zakat is an obligation on a Muslim who owns zakatable wealth above the Nisab threshold for a full lunar year. The rules apply to net wealth after the debts due now are subtracted.",
            "Scholars agree on the general obligation, but they differ on details. This is why the calculator states its method and asks you to confirm lunar year timing yourself.",
        ]),
        ("Assets usually included", [
            "Cash in hand, bank savings, gold and silver held as wealth, goods held for sale in a business, and money owed to you that you expect to receive are the most common zakatable items.",
            "Gold and silver jewelry worn for personal use is treated differently by different schools. Check your own school's ruling or ask a scholar before you count it.",
        ]),
        ("Assets usually excluded", [
            "Your home that you live in, your everyday furniture, your vehicle used for daily travel, and tools used for work are generally not zakatable wealth.",
            "Rental income and property held for rent follow their own rules. The rent itself, or the value of property bought for resale, can be zakatable depending on the ruling you follow.",
        ]),
        ("Lunar year and timing", [
            "The hawl is one lunar year, which is about 354 days. It starts from the date your wealth first reached Nisab and stays above it.",
            "If your wealth falls below Nisab during the year, the count usually restarts once it rises above Nisab again. Keep a dated record of your balances to make this easier to check.",
        ]),
        ("Zakat arithmetic and worked example", [
            "For commonly zakatable wealth, the calculation is 2.5% of net zakatable wealth when the applicable Nisab and lunar-year requirements are met. This tool uses a silver-based Nisab of 612.36 grams multiplied by the entered silver price per gram. A gold-based reference sometimes used is 87.48 grams; the applicable basis depends on scholarly guidance.",
            "Example: PKR 500,000 savings + PKR 200,000 precious metals + PKR 100,000 trading inventory = PKR 800,000 gross assets. After PKR 150,000 qualifying debts, net wealth is PKR 650,000. At PKR 250 per gram of silver, Nisab = 612.36 × 250 = PKR 153,090. The arithmetic gives Zakat = 650,000 × 0.025 = PKR 16,250.",
        ]),
        ("Zakat limitations and common questions", [
            "Only deduct debts qualifying under the method you follow; treatment of near-term instalments, mortgages and other liabilities varies. Do not assume all long-term debt is deductible. Check current valuations, Nisab basis and lunar-year timing.",
            "Is Zakat always 2.5%? Not for every asset category. Is a primary home zakatable? A home used as a residence is generally treated differently from trading inventory, but circumstances vary. This is a calculation aid, not a religious ruling. Consult a qualified scholar. Reference: https://islamic-relief.org/news/how-to-calculate-and-pay-zakat/",
        ]),
    ],
    "bmi-calculator": [
        ("Why BMI is used", [
            "BMI is a simple, low cost measure that is used in large population studies and in clinics as a first step. It needs only weight and height, so it is easy to repeat over time.",
            "Because it is simple, it cannot tell muscle from fat, or fat in the belly from fat under the skin. Treat it as a starting point for a conversation with a clinician.",
        ]),
        ("Groups where BMI needs care", [
            "Athletes and people with high muscle mass can have a high BMI with a low body fat level. Older adults can have a normal BMI with a high body fat level and low muscle mass.",
            "BMI is not a reliable guide during pregnancy, because healthy weight gain is expected. Ask your midwife or doctor about gestational weight targets.",
        ]),
        ("How to measure correctly", [
            "Weigh yourself in the morning, after using the toilet and before eating, in light clothing. Measure height without shoes, standing straight against a flat wall.",
            "Round your height to the nearest millimetre or sixteenth of an inch, and check that you entered the correct units before reading the result.",
        ]),
        ("BMI formula and worked example", [
            "For adults, BMI = weight in kilograms divided by height in metres squared. For 70 kg and 1.75 m, BMI = 70 / (1.75 × 1.75) = 22.8571, displayed as 22.9.",
            "WHO adult screening thresholds: underweight below 18.5; normal weight 18.5 to below 25; overweight 25 to below 30; obesity 30 or above. These categories are not a diagnosis. Children require age- and sex-specific references. Reference: https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight",
        ]),
        ("BMI questions and mistakes", [
            "Do not confuse centimetres and metres or use adult categories for children. Standard adult categories are not appropriate for assessing weight during pregnancy. Athletes may have high BMI due to muscle.",
            "Is BMI a body-fat test? No. Does the formula differ by sex? No, but clinical interpretation depends on more than BMI. Seek qualified clinical advice for individual health decisions.",
        ]),
    ],
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
        "Questions about years use 365 days per year in this calculator. A birth-date question counts exact Gregorian calendar days between the two dates you enter, so the two methods can differ by a few days over long periods.",
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
            "CalculatesAll brings together free browser-based tools for everyday calculations. Use the Zakat calculator to estimate net zakatable wealth after eligible debts, check a silver Nisab threshold using the price you enter, and confirm the lunar-year condition yourself. Religious rulings can differ, so review the stated method and consult a trusted qualified scholar for your circumstances.",
            "Use the profit and loss calculator to compare selling price with cost, and the discount calculator to work out savings and a final price. For example, a 20% discount on a price of 1,000 leaves 800 before any applicable tax or fees. Your actual business profit may also depend on shipping, packaging, payment fees, tax and other costs not entered into a simple calculator.",
            "The adult BMI calculator uses weight divided by height squared, with unit handling for metric and imperial inputs. BMI is a screening measure, not a diagnosis, and it does not directly measure body fat. Read the limitations and the World Health Organization's adult BMI information before using the result to discuss health with a clinician: <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index\">WHO body mass index information</a>.",
            "The age calculator works with calendar dates, the unit converter applies defined conversion factors, and the stopwatch and tasbih counter support simple timing and counting tasks. For a reference example, one inch is defined as exactly 25.4 millimetres. See the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.nist.gov/pml/owm/si-units-length\">National Institute of Standards and Technology's length-unit reference</a> for the inch definition.",
            "How are results checked? Each calculator page explains its formula, includes a worked example where it helps, and states important limitations. Worked examples are recalculated whenever a tool changes, and reported errors are corrected on the affected page. For high-stakes financial, medical or religious decisions, confirm the result with a qualified professional.",
            "Calculations are designed to run in your browser without sending calculator entries to our server. The tasbih counter stores its count on your device. The site may load third-party advertising or other resources, which are described in the privacy policy. Avoid entering sensitive personal information into any online tool unless you understand how it handles data.",
            "The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/calorie-calculator/\">adult calorie calculator</a> estimates maintenance energy for adults using the Mifflin–St Jeor equation and a stated activity factor. It is an estimate, not a measured metabolic rate or a diet prescription. The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/emi-calculator/\">EMI calculator</a> estimates a fixed-rate monthly installment and shows a repayment schedule. The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/compound-interest-calculator/\">compound interest calculator</a> models one starting balance at a fixed nominal annual rate and compounding frequency, excluding additional deposits, fees and taxes. The <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/percentage-calculator/\">percentage calculator</a> and <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/fraction-calculator/\">fraction calculator</a> explain the arithmetic steps, while the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/date-calculator/\">date calculator</a> counts signed Gregorian calendar days and the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/years-to-days-calculator/\">Years to Days calculator</a> distinguishes fixed-year conversions from exact calendar-date results. The Zakat calculator applies the stated silver Nisab of 612.36 grams and a 2.5% rate to net zakatable wealth when the stated conditions are met. Read the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/zakat-calculator/\">Zakat method</a> and note that scholarly rulings can differ. The adult BMI tool uses the WHO adult categories: below 18.5, 18.5 to 24.9, 25.0 to 29.9, and 30 or above. See the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight\" rel=\"noopener noreferrer\">WHO fact sheet</a> for context.",
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
            "مالی حساب کے لیے زکوٰۃ کیلکولیٹر میں نقد رقم، بچت، متعلقہ اثاثے، واجب الادا قرض اور چاندی کی فی گرام قیمت درج کریں۔ منافع اور نقصان کے ٹول میں قیمت خرید اور قیمت فروخت ایک ہی کرنسی میں لکھیں۔ ڈسکاؤنٹ کیلکولیٹر اصل قیمت اور رعایت کا فیصد استعمال کرتا ہے، مگر ٹیکس، شپنگ اور دکان کی اضافی فیس خود شامل نہیں کرتا۔",
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
        "Zakat uses the silver Nisab of 612.36 grams and 2.5 percent of net wealth. It does not show an amount until the Nisab and lunar year checks are complete.",
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
GUIDE_EXTRA["zakat-calculator"].extend([
    ("Pre-payment checklist", [
        "1. Choose the calculation method you intend to follow and confirm the applicable Nisab basis with a qualified scholar. This page calculates with its stated silver-based Nisab; it does not compare every school or asset rule. 2. Record the date your zakatable wealth first reached the relevant Nisab. 3. List the cash, bank balances, precious metals, trading stock and receivables that your chosen method treats as zakatable. 4. Value those items consistently at the valuation date you are using. 5. List only debts or liabilities that your chosen method permits you to deduct, and do not automatically subtract every future instalment. 6. Check the current silver price per gram from a source you trust and record the date and currency of that quote. 7. Confirm that the required lunar year has elapsed and ask a qualified scholar about any unusual assets, ownership changes or disputed deductions before payment.",
        "Worked arithmetic check: if eligible net wealth is PKR 650,000 and the entered silver price is PKR 250 per gram, the stated silver Nisab is 612.36 × 250 = PKR 153,090. The net wealth is above that example threshold. If the stated 2.5% method and lunar-year condition also apply, the arithmetic is PKR 650,000 × 0.025 = PKR 16,250. The example does not decide whether those inputs or conditions apply to a particular person.",
    ]),
    ("Why silver price and lunar-year confirmation are required", [
        "The silver price converts the calculator's fixed 612.36-gram silver Nisab into the currency amount used for the comparison. A missing or zero price leaves that threshold unknown, so the tool withholds a Zakat amount rather than silently assuming a market value. Enter a dated price per gram in the same currency as the assets and debts; the calculator does not fetch or verify a live market quote.",
        "The lunar-year confirmation is a separate condition from the arithmetic. The checkbox records that the user has checked the hawl requirement; it cannot verify the date wealth first reached Nisab or determine how a scholar applies the rule to interruptions or changing balances. The tool withholds the amount until the user confirms this condition. This is a user confirmation, not an automated religious assessment.",
    ]),
    ("Arithmetic aid, not a scholarly ruling", [
        "This calculator performs arithmetic using the silver Nisab, 2.5% rate and inputs shown on the page. It cannot decide which assets count, how personal-use jewellery is treated, which debts may be deducted, whether a lunar year has been completed, or which scholarly opinion applies to your circumstances. Schools and qualified scholars may differ on these questions. Treat the displayed figure as a calculation under the stated assumptions only, not a fatwa or personal religious advice. Before paying, confirm the method and any uncertain asset or liability with a qualified scholar.",
    ]),
])

GUIDE_EXTRA["bmi-calculator"].extend([
    ("What a BMI result is useful for and what it is not", [
        "For adults, BMI is useful as a quick, repeatable screening measure based on weight and height. It can help describe a broad weight category, compare measurements taken consistently over time, and identify when a fuller health discussion may be useful. It is not a direct measurement of body fat, waist fat, muscle, fitness or an individual's disease risk.",
        "A BMI result cannot diagnose a condition or explain why a person's weight has changed. It may be misleading for people with high muscle mass, during pregnancy, in older adults with changing muscle mass, and for children who need age- and sex-specific growth references. Do not use this number alone to start, stop or change treatment, medication, diet or exercise. This calculator is a screening aid, not a diagnosis or professional medical advice.",
    ]),
    ("Pakistan and South Asia context", [
        "Body composition and the distribution of body fat can differ between populations, and cardiometabolic risk may be present at lower BMI values in some Asian populations than standard international adult cut-offs alone suggest. A 2004 WHO expert consultation identified 23 and 27.5 kg/m² as additional public-health action points for Asian populations, while retaining the standard WHO BMI cut-offs as international classifications. These action points are not a replacement set of WHO adult categories and should not be treated as a personal diagnosis or a universal threshold for every South Asian individual. To keep this tool's output consistent and transparent, it continues to report the standard WHO adult categories shown above; it does not silently substitute a different threshold. A doctor or qualified local health professional can interpret the result alongside waist measurement, medical history and other relevant information. Pakistan's 2019 Dietary Guidelines for Better Nutrition also describe the Asian-population risk bands in a local public-health context. See the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://pubmed.ncbi.nlm.nih.gov/14726171/\" rel=\"noopener noreferrer\">WHO Expert Consultation (2004) on BMI in Asian populations</a>, the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://pc.gov.pk/uploads/report/Pakistan_Dietary_Nutrition_2019.pdf\" rel=\"noopener noreferrer\">Pakistan Dietary Guidelines for Better Nutrition (2019)</a> and the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight\" rel=\"noopener noreferrer\">WHO adult BMI definitions</a> for their respective contexts.",
        "This note is general educational information. It does not assign a South Asian diagnosis, provide a personal risk estimate or replace an assessment by a local doctor. The appropriate interpretation can vary by individual and clinical context.",
    ]),
])

GUIDE_EXTRA["profit-loss-calculator"].extend([
    ("Markup and margin use different bases", [
        "Markup measures profit against cost: markup percentage = (selling price − cost) ÷ cost × 100. Gross margin measures profit against selling price: gross margin percentage = (selling price − cost) ÷ selling price × 100. If an item costs PKR 800 and sells for PKR 1,000, the profit is PKR 200, markup is 200 ÷ 800 × 100 = 25%, and gross margin is 200 ÷ 1,000 × 100 = 20%. The profit amount is the same, but the percentages differ because their denominators differ.",
        "A business operating margin has another base: net operating profit divided by revenue. If revenue is PKR 100,000, cost of goods sold is PKR 60,000 and entered operating expenses are PKR 15,000, gross profit is PKR 40,000, net operating profit is PKR 25,000, and net operating margin is 25,000 ÷ 100,000 × 100 = 25%. Do not label product markup or gross margin as business operating margin.",
    ]),
    ("Business mode and Product mode answer different questions", [
        "Product mode compares one item's cost price with its selling price. It reports the profit or loss amount, markup on cost and gross margin on selling price. Use it when you are pricing or reviewing an individual product and have entered the relevant product cost.",
        "Business mode uses total revenue, cost of goods sold and the other operating expenses entered. It calculates gross profit or loss, then subtracts those entered expenses to show net operating profit or loss and net operating margin on revenue. It is a simplified operating view, not a complete income statement, audited account or tax calculation. Costs not entered, including interest, tax, refunds or other charges, are not inferred.",
    ]),
    ("Common pricing mistakes this calculator helps expose", [
        "A frequent mistake is calling markup a margin, even though one divides by cost and the other by selling price. Another is pricing from the supplier invoice alone while leaving out freight, packaging or other direct costs needed to get the item ready for sale. A third is treating revenue minus product cost as net business profit while ignoring rent, wages, utilities or other operating expenses.",
        "Other avoidable errors include mixing currencies, entering a selling price before a discount as though it were the amount actually received, forgetting returns or platform/payment charges, and assuming sales tax or income tax has been calculated automatically. Use one currency, enter costs in the correct mode, and reconcile the result with invoices and business records. The calculator does not replace accounting or tax advice.",
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
