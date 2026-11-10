"""Hub page that links every free calculator and explains how to choose one."""
import html

H2 = "mt-10 text-2xl font-semibold text-stone-900 dark:text-stone-100"
H3 = "mt-6 text-lg font-semibold text-stone-900 dark:text-stone-100"
P = "mt-4 text-base leading-7 text-stone-800 dark:text-stone-200"
LINK = "text-sky-800 dark:text-sky-300 underline"
TH = "border border-stone-300 dark:border-stone-700 p-3 text-left"
TD = "border border-stone-300 dark:border-stone-700 p-3 align-top"

PATH = "/free-online-calculators/"
TITLE = "Free Online Calculators for Money, Health, Math and Time"
DESC = ("Free online calculators for Zakat, EMI, BMI, percentages, ratios, age, dates and unit conversion. Each tool shows its formula, an example and its limits.")

TOOLS = [
    ("Zakat Calculator", "/zakat-calculator/", "Money", "Estimates zakatable wealth using the method stated on the page.", "Check the nisab value and debts you enter."),
    ("EMI Calculator", "/emi-calculator/", "Money", "Estimates a monthly loan installment and a repayment schedule.", "Lender fees and contract terms can change the final quote."),
    ("Profit and Loss Calculator", "/profit-loss-calculator/", "Money", "Works out profit, loss and margin from cost and selling price.", "Confirm whether the percentage uses cost or selling price."),
    ("Discount Calculator", "/discount-calculator/", "Money", "Calculates the sale price and saving from a discount percentage.", "Taxes and fees are excluded unless you add them."),
    ("Compound Interest Calculator", "/compound-interest-calculator/", "Money", "Projects growth with principal, rate, time and compounding frequency.", "Projections are not guaranteed returns."),
    ("Adult Calorie Calculator", "/calorie-calculator/", "Health", "Estimates daily maintenance calories for adults.", "It is an estimate, not a medical plan."),
    ("BMI Calculator", "/bmi-calculator/", "Health", "Calculates adult body mass index in metric or imperial units.", "BMI is a screening measure, not a diagnosis."),
    ("Percentage Calculator", "/percentage-calculator/", "Math", "Finds a percentage of a number, or the percentage one number is of another.", "Confirm which value is the base."),
    ("Percentage Difference Calculator", "/percentage-difference-calculator/", "Math", "Compares two non-negative values using their average.", "Use percentage change when one value is the starting point."),
    ("Ratio Calculator", "/ratio-calculator/", "Math", "Simplifies two- or three-term ratios, scales an equivalent ratio or solves a proportion with one missing value.", "Use the same units. Three-term ratios keep all three quantities in order."),
    ("Fraction Calculator", "/fraction-calculator/", "Math", "Adds, subtracts, multiplies and divides fractions exactly.", "Results are simplified fractions."),
    ("Standard Calculator", "/standard-calculator/", "Math", "Performs everyday arithmetic with a scientific mode.", "Check operator order when using parentheses."),
    ("Unit Converter", "/unit-converter/", "Math", "Converts length, weight, temperature and other common units.", "Temperature needs an offset as well as a scale factor."),
    ("Age Calculator", "/age-calculator/", "Date and Time", "Calculates exact age in years, months and days.", "Confirm the date of birth and the reference date."),
    ("Date Difference Calculator", "/date-calculator/", "Date and Time", "Counts the days or time between two dates.", "Check whether the start and end dates are counted."),
    ("Years to Days Calculator", "/years-to-days-calculator/", "Date and Time", "Converts years into days, hours, minutes and seconds.", "Leap years change the total slightly."),
    ("Query Calculator", "/query-calculator/", "Date and Time", "Answers supported plain-language time conversion questions.", "It answers only the question types it supports."),
    ("Stopwatch", "/stopwatch/", "Date and Time", "Measures elapsed time in your browser.", "It is for everyday timing, not certified measurement."),
    ("Tasbih Counter", "/tasbih-counter/", "Worship and Daily Use", "Counts dhikr with an optional target.", "The count is stored on the current device."),
]

FAQ = [
    ("Are these calculators free to use?", "Yes. Every calculator on this page is free to use in your browser. No account, signup or payment is required."),
    ("Do I need to install an app?", "No. The calculators work in a standard mobile or desktop browser, and the layout adjusts to the screen size."),
    ("Are my entered values sent to a server?", "Calculator inputs are processed in your browser. The Tasbih Counter stores its count on the current device. Read the privacy policy for information about hosting and advertising."),
    ("How are the results checked?", "Each calculator uses a stated formula, and worked examples are included where they help you check a result. Automated tests cover representative inputs and boundary cases. Read the methodology page for the full approach."),
    ("Can a calculator replace professional advice?", "No. Tools for health, money and Zakat give estimates based on the inputs you provide. For important decisions, confirm the result with a qualified professional or scholar."),
    ("How do I report a wrong result?", "Send the calculator name, page URL, exact inputs, the displayed result, the expected result and the steps to reproduce it to the email on the contact page."),
]


def _tool_table():
    rows = []
    for name, href, category, does, check in TOOLS:
        rows.append(
            '<tr><th scope="row" class="' + TD + '"><a class="' + LINK + '" href="' + href + '">' + html.escape(name) + "</a></th>"
            '<td class="' + TD + '">' + html.escape(category) + "</td>"
            '<td class="' + TD + '">' + html.escape(does) + "</td>"
            '<td class="' + TD + '">' + html.escape(check) + "</td></tr>"
        )
    return (
        '<div class="mt-4 overflow-x-auto"><table class="w-full border-collapse text-sm">'
        '<caption class="mb-2 text-left font-semibold text-stone-900 dark:text-stone-100">All free calculators on CalculatesAll</caption>'
        '<thead><tr><th scope="col" class="' + TH + '">Calculator</th><th scope="col" class="' + TH + '">Category</th>'
        '<th scope="col" class="' + TH + '">What it calculates</th><th scope="col" class="' + TH + '">Check before you rely on it</th></tr></thead>'
        "<tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def _decision_table():
    items = [
        ("Work out zakat on savings and gold", "Zakat Calculator"),
        ("Plan a loan installment", "EMI Calculator"),
        ("Check the sale price after a discount", "Discount Calculator"),
        ("Compare cost, selling price and margin", "Profit and Loss Calculator"),
        ("Find what percent one number is of another", "Percentage Calculator"),
        ("Compare two values without a starting point", "Percentage Difference Calculator"),
        ("Find how many days are between two dates", "Date Difference Calculator"),
        ("Find someone's exact age", "Age Calculator"),
        ("Convert between units of measure", "Unit Converter"),
        ("Check adult BMI", "BMI Calculator"),
    ]
    rows = "".join(
        '<tr><td class="' + TD + '">' + html.escape(task) + '</td><td class="' + TD + '">' + html.escape(tool) + "</td></tr>"
        for task, tool in items
    )
    return (
        '<div class="mt-4 overflow-x-auto"><table class="w-full border-collapse text-sm">'
        '<caption class="mb-2 text-left font-semibold text-stone-900 dark:text-stone-100">Find the right tool by task</caption>'
        '<thead><tr><th scope="col" class="' + TH + '">If you need to</th><th scope="col" class="' + TH + '">Use</th></tr></thead>'
        "<tbody>" + rows + "</tbody></table></div>"
    )


def _faq():
    out = []
    for question, answer in FAQ:
        out.append('<h3 class="' + H3 + '">' + html.escape(question) + "</h3>")
        out.append('<p class="' + P + '">' + html.escape(answer) + "</p>")
    return "".join(out)


def build_hub_page(head, shell, write):
    schema = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": TITLE,
         "url": "https://calculateallinone.vercel.app" + PATH, "description": DESC},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "Free online calculators",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": name,
              "url": "https://calculateallinone.vercel.app" + href}
             for i, (name, href, _c, _d, _k) in enumerate(TOOLS)
         ]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://calculateallinone.vercel.app/"},
            {"@type": "ListItem", "position": 2, "name": "Free Online Calculators", "item": "https://calculateallinone.vercel.app/free-online-calculators/"},
        ]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in FAQ
        ]},
    ]
    body = (
        '<nav aria-label="Breadcrumb" class="mb-4 text-sm text-stone-700 dark:text-stone-300"><ol class="flex flex-wrap items-center gap-2"><li><a class="' + LINK + '" href="/">Home</a></li><li aria-hidden="true">/</li><li aria-current="page">Free Online Calculators</li></ol></nav>'
        '<h1 class="text-3xl font-semibold text-stone-900 dark:text-stone-100">Free Online Calculators for Money, Health, Math and Time</h1>'
        '<p class="' + P + '">CalculatesAll brings together free browser-based calculators for everyday money, health, math, date and daily worship tasks. '
        "There are " + str(len(TOOLS)) + " calculators in total. Each one states its formula or method, shows an example where it helps, and lists the assumptions that affect the result.</p>"
        '<h2 id="all-calculators" class="' + H2 + '">Which free calculators are available?</h2>'
        '<p class="' + P + '">Browse the full list below, or open a category: '
        '<a class="' + LINK + '" href="/money/">Money and Business</a>, <a class="' + LINK + '" href="/health/">Health</a>, '
        '<a class="' + LINK + '" href="/math/">Math and Converters</a>, <a class="' + LINK + '" href="/time/">Date and Time</a> and '
        '<a class="' + LINK + '" href="/worship/">Worship and Daily Use</a>.</p>'
        + _tool_table()
        + '<h2 id="choose-tool" class="' + H2 + '">How do I choose the right calculator?</h2>'
        '<p class="' + P + '">Start with the question you want answered, not the category. Two tools can look similar but use different bases. '
        "For example, percentage change measures growth from a starting value, while percentage difference compares two values with their average as the base.</p>"
        + _decision_table()
        + '<h2 id="money" class="' + H2 + '">What are the money calculators used for?</h2>'
        '<p class="' + P + '">The money tools cover loans, sales, profit, savings growth and Zakat. Each one depends on the inputs you enter. A discount calculator, for instance, '
        "shows the reduction from the price you type, so taxes, delivery fees and coupons are left out unless you include them yourself. "
        'See the <a class="' + LINK + '" href="/methodology/">calculation methodology</a> for the formulas used.</p>'
        '<h2 id="health" class="' + H2 + '">What do the health calculators estimate?</h2>'
        '<p class="' + P + '">The BMI and adult calorie calculators give screening estimates for adults. They do not diagnose a condition or replace a clinical assessment. '
        "Use the result as a starting point for a conversation with a doctor or dietitian.</p>"
        '<h2 id="math-time" class="' + H2 + '">What math and date tools help with daily tasks?</h2>'
        '<p class="' + P + '">The math tools handle percentages, fractions, unit conversions and everyday arithmetic. The date tools count the time between two dates, convert years into days and find exact age. '
        "Calendar months have different lengths, and leap years change totals, so check whether the selected tool counts the start and end dates.</p>"
        '<h2 id="worship" class="' + H2 + '">Which worship and daily-use tools are included?</h2>'
        '<p class="' + P + '">The Tasbih Counter helps you keep count of dhikr on your phone or computer, with an optional target. The count is stored only on the current device.</p>'
        '<h2 id="faq" class="' + H2 + '">Frequently asked questions</h2>'
        + _faq()
        + '<h2 id="next" class="' + H2 + '">Where should I go next?</h2>'
        '<p class="' + P + '">If you are new to the site, start with the <a class="' + LINK + '" href="/zakat-calculator/">Zakat Calculator</a>, the <a class="' + LINK + '" href="/emi-calculator/">EMI Calculator</a> '
        'or the <a class="' + LINK + '" href="/percentage-calculator/">Percentage Calculator</a>. Each page explains its inputs and gives an example you can reproduce by hand. '
        'Questions about results can be sent through the <a class="' + LINK + '" href="/contact/">contact page</a>.</p>'
    )
    write(PATH, head(TITLE, DESC, PATH, schema) + shell(body))
    return [(PATH, [])]
