"""Editorial content for CalculatesAll. Edit text here, then run npm run build."""

REVIEW_STATUS = {
    "zakat-calculator": "Method stated on this page. Subject expert review by a qualified scholar is pending.",
    "bmi-calculator": "Formula and WHO categories checked against the stated method. Clinical review is pending.",
    "profit-loss-calculator": "Formulas checked against the stated method.",
    "discount-calculator": "Formulas checked against the stated method.",
    "age-calculator": "Calendar method checked against worked examples.",
    "unit-converter": "Conversion factors checked against published definitions.",
    "standard-calculator": "Order of operations checked with test expressions.",
    "tasbih-counter": "Behaviour checked on this device only.",
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
            "Targets of 33, 100 and 1000 are common for dhikr, and the counter also supports an unlimited count. Choose the target that matches your practice.",
        ]),
        ("Privacy of your count", [
            "The count is stored only in your browser on this device. CalculatesAll does not send the count to a server or link it to an account.",
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

HOME_EXTRA = {
    "en": {
        "heading": "What you can do on CalculatesAll",
        "paragraphs": [
            "CalculatesAll brings together tools that people use every week. Zakat and profit calculations help with money decisions. BMI gives a screening number for adults. Age, discount and unit tools handle everyday arithmetic. The stopwatch and tasbih counter help with timing and dhikr.",
            "Each tool shows its formula, a worked example and its limits on the tool page. This makes it easier to check a result yourself, and it tells you when a question needs a professional.",
        ],
        "faq": [
            ("Are the calculators free?", "Yes. All tools on CalculatesAll are free to use."),
            ("Do you store the numbers I enter?", "No. Calculations run in your browser. The tasbih counter keeps its count on your device only."),
            ("Are the results accurate?", "The formulas are standard and each tool states its method. For rulings on religious questions or diagnoses, consult a qualified professional."),
        ],
    },
    "ur": {
        "heading": "CalculatesAll پر آپ کیا کر سکتے ہیں",
        "paragraphs": [
            "CalculatesAll میں وہ ٹولز اکٹھے ہیں جو لوگ ہر ہفتے استعمال کرتے ہیں۔ زکوٰۃ اور منافع کے حساب مالی فیصلوں میں مدد دیتے ہیں۔ BMI بالغوں کے لیے ایک اسکریننگ نمبر دیتا ہے۔ عمر، ڈسکاؤنٹ اور یونٹ کے ٹولز روزمرہ حساب کرتے ہیں۔ اسٹاپ واچ اور تسبیح کاؤنٹر وقت اور ذکر کے لیے ہیں۔",
            "ہر ٹول کا صفحہ اس کا فارمولا، ایک مثال اور اس کی حدود بتاتا ہے۔ اس سے آپ نتیجہ خود جانچ سکتے ہیں اور جان سکتے ہیں کہ کب کسی ماہر سے رجوع کرنا ہے۔",
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
    ],
    "/editorial-policy": [
        "Each tool page shows a review status. Where subject expert review is pending, the page says so. We do not present a page as reviewed by a person until that review is complete and named.",
        "Worked examples are calculated before they are published. Dates on each page show when the guide was last changed.",
    ],
    "/privacy": [
        "You can ask us about the personal information we hold about you by contacting the address on the contact page. Because the calculators run in your browser, we normally hold no personal information about you.",
    ],
}
