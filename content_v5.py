"""Editorial content for CalculatesAll. Edit text here, then run npm run build."""

REVIEW_STATUS = {
    "bmi-calculator": "Formula and WHO categories checked against the stated method. Clinical review is pending.",
    "profit-loss-calculator": "Formulas checked against the stated method.",
    "discount-calculator": "Formulas checked against the stated method.",
    "age-calculator": "Calendar method checked against worked examples.",
    "unit-converter": "Conversion factors checked against published definitions.",
    "standard-calculator": "Order of operations checked with test expressions.",
    "tasbih-counter": "Static output and automated build checks passed; direct device interaction testing is pending.",
    "stopwatch": "Timing method checked against the browser clock.",
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
    ],
    "profit-loss-calculator": [
        ("Profit and loss in a business", [
            "A sale is profitable only when the selling price is higher than the total cost of the item. Total cost includes purchase price and direct costs such as freight, packaging, storage and payment fees.",
            "A business with several products should calculate profit for each product line, because a high margin on one item can hide a loss on another.",
        ]),
        ("Example with a loss", [
            "Cost price is 1,500 and selling price is 1,200. The difference is minus 300, which is a loss of 300.",
            "The percentage is minus 300 divided by 1,500, multiplied by 100, which is minus 20 percent. The loss is 20 percent of cost.",
        ]),
        ("Common mistakes", [
            "Forgetting that discounts reduce the selling price. Calculate profit after the discount you actually gave the customer.",
            "Comparing a percentage on cost with a percentage on selling price. Always check which base a percentage uses before you compare two figures.",
        ]),
    ],
    "discount-calculator": [
        ("Stacked discounts", [
            "Two discounts applied one after another are not the same as adding their percentages. A 20 percent discount followed by a 10 percent discount on the reduced price gives a total reduction of 28 percent, not 30 percent.",
            "Example: an item priced at 1,000 with 20 percent off becomes 800. A further 10 percent off 800 is 80, so the final price is 720. The total saving is 280, which is 28 percent of 1,000.",
        ]),
        ("Discount before or after tax", [
            "Most shops calculate the discount on the price before tax. Some countries and shops calculate tax first. Check the receipt to see how your store applies the discount.",
        ]),
        ("Using discounts for pricing", [
            "To find the price that gives a target final price, divide the target by one minus the discount rate. For a 20 percent discount and a target of 800, the original price is 800 divided by 0.8, which is 1,000.",
        ]),
    ],
    "age-calculator": [
        ("Leap years", [
            "A leap year has 366 days. The extra day falls on 29 February. Leap years occur in years divisible by 4, except years divisible by 100 that are not divisible by 400.",
            "The calculator follows the Gregorian calendar, so day counts include every leap day between the two dates.",
        ]),
        ("Birthdays on 29 February", [
            "The calculator counts calendar dates. A person born on 29 February has a birthday in leap years only. Many countries treat 1 March as the legal birthday in other years, so check your local rule if you need it for a document.",
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
            "Converting in the other direction, 3.10686 miles multiplied by 1.609344 gives back 5 kilometres.",
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
    "tasbih-counter": [
        ("Choosing a target", [
            "Choose a preset target of 33, 99 or 100, or enter a custom whole number from 1 to 10,000. The target is a personal tracking setting, not a religious ruling or a claim that a particular number is required.",
        ]),
        ("Privacy of your count", [
            "The count is stored only in your browser on this device when browser storage is available. If storage is blocked, the counter works in memory until the page is reloaded or closed. CalculatesAll does not send the count to a server or link it to an account.",
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

# Worked examples and checking steps added for the AdSense content review.
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
GUIDE_EXTRA["years-to-days-calculator"] = [
    ("Worked example for 12 years", [
        "Simple method: 12 x 365 = 4,380 days. Weeks: 4,380 / 7 = 625.71 weeks. Hours: 4,380 x 24 = 105,120 hours.",
        "Gregorian average method: 12 x 365.2425 = 4,382.91 days. The difference between the two methods is 2.91 days over 12 years, which equals 0.2425 days per year multiplied by 12.",
        "Minutes: 105,120 x 60 = 6,307,200 minutes. Seconds: 6,307,200 x 60 = 378,432,000 seconds.",
    ]),
    ("Checking a result", [
        "Divide the day count by 365 for the simple method. 4,380 / 365 = 12. For the Gregorian method, divide by 365.2425. 4,382.91 / 365.2425 = 12. These divisions confirm the result without a calculator app.",
        "Fractional years work the same way. 0.5 x 365 = 182.5 days in the simple method, which is 182 days and 12 hours, because 0.5 x 24 = 12 hours.",
    ]),
]
GUIDE_EXTRA["stopwatch"].append(
    ("Worked examples", [
        "A lap time of 83 seconds equals 1 minute and 23 seconds. Step 1: 1 x 60 = 60 seconds. Step 2: 60 + 23 = 83 seconds.",
        "A total of 3,725 seconds equals 1 hour, 2 minutes and 5 seconds. Step 1: 1 x 3,600 = 3,600 seconds. Step 2: 3,725 - 3,600 = 125 seconds. Step 3: 2 x 60 = 120 seconds, leaving 125 - 120 = 5 seconds.",
    ])
)
GUIDE_EXTRA["tasbih-counter"].append(
    ("Worked example", [
        "Target 99 is reached after 99 presses. Three rounds of 33 presses give 3 x 33 = 99 presses, which matches the target. If you select a target of 100 instead, 100 - 99 = 1 more press is needed after the first 99.",
        "The counter stores the count on this device only. It does not check which phrase you recited, so the worked example describes presses, not the number of recitations you intended.",
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
            "How are results checked? Each calculator page explains its method, includes a worked example where applicable, and states important limitations. The site also runs automated build checks for generated pages, metadata, sitemap consistency and key calculator behaviours. Automated tests reduce regression risk, but they do not replace independent professional review or testing on every device.",
            "Calculations are designed to run in your browser without sending calculator entries to our server. The tasbih counter stores its count on your device. The site may load third-party advertising or other resources, which are described in the privacy policy. Avoid entering sensitive personal information into any online tool unless you understand how it handles data.",
            "The Zakat calculator states the method it applies: a silver Nisab of 612.36 grams and a 2.5% rate on net zakatable wealth when the stated conditions are met. Scholarly rulings can differ, so read the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"/zakat-calculator/\">Zakat calculator method</a> and consult a qualified scholar for your circumstances. The adult BMI tool uses World Health Organization adult categories: below 18.5, 18.5 to 24.9, 25.0 to 29.9, and 30 or above. See the <a class=\"underline text-sky-800 dark:text-sky-300\" href=\"https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight\" rel=\"noopener noreferrer\">WHO fact sheet</a> for context.",
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
        "We read every message. Corrections to confirmed formula errors are published on the tool page with an updated date.",
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
        "Each tool page shows a review status. Where subject expert review is pending, the page says so. We do not present a page as reviewed by a person until that review is complete and named.",
        "Worked examples are calculated before they are published. Dates on each page show when the guide was last changed.",
        "Content quality checks focus on accuracy, usefulness, and clear limits rather than repeating search phrases. Calculator pages should answer the main user question near the top, define the inputs, explain the formula, show a worked example where it helps, and answer common follow-up questions. Category pages should help visitors choose the right tool rather than repeat the same paragraph for every calculator.",
        "Technical checks include a unique title and meta description, one primary heading, a self-referencing canonical, crawlable internal links, valid structured data, sitemap consistency and working local assets. Build tests also check representative input boundaries and calculator behaviour. These checks are designed to catch common regressions, but they are not a claim that every possible input or browser combination has been exhaustively tested.",
        "We prefer official or primary references for definitions and factual claims. Health content is general information and should not be presented as a diagnosis. Zakat guidance states the method used and acknowledges that religious rulings can differ. Conversion factors should match recognised definitions, and example arithmetic should be reproducible from the numbers shown.",
        "A correction should include the page URL, input values, the displayed result and the expected result or source. Confirmed defects are corrected in the code or content, then automated checks are run before deployment. We avoid inventing review dates, expert endorsements, user testimonials or performance claims that cannot be verified."
    ],
    "/marketplaces": [
        "Before using a marketplace or monetization programme, read its current eligibility, content, payout, disclosure and tax requirements directly from the provider. A guide page is not evidence that an account is approved, that a product is listed, or that a commission link is active. Approval and geographic eligibility can change, so verify them in the provider's own dashboard before publishing a claim.",
        "For website advertising, keep publisher ownership verification separate from the decision to load ad scripts. Only configure real ad-unit identifiers after reviewing consent requirements and testing the deployed page. An ads.txt file should match the actual publisher ID; it must not contain invented account data. The current calculator site keeps ad slots disabled unless the required settings are explicitly configured.",
        "For digital products, describe the deliverable honestly and include format, compatibility, refund conditions and limitations. Do not imply that a free online calculator is a paid downloadable product unless an original downloadable file is genuinely offered. Affiliate links should be identified clearly, and ordinary official links should not be described as commission links unless tracking and programme approval are in place."
    ],
    "/privacy": [
        "You can ask us about the personal information we hold about you by contacting the address on the contact page. Because the calculators run in your browser, we normally hold no personal information about you.",
    ],
}
