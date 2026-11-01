"""Standalone calculator page definitions. Uses the existing site's shell and metadata pipeline."""
import html

PAGES = [
 ("percentage-calculator","Percentage Calculator","Work out X% of a number, what percent one number is of another, or the percentage change between two values.",[("value","Percentage (%)","number"),("total","Number","number")],"X% of Y = X divided by 100, multiplied by Y. For example, 25% of 200 is 50. X as a percent of Y = X divided by Y, multiplied by 100, so 30 out of 120 is 25%. Percentage change = (new value minus old value) divided by old value, multiplied by 100, so 80 to 100 is a 25% increase."),
 ("fraction-calculator","Fraction Calculator","Add, subtract, multiply and divide two fractions. Get a simplified fraction result with a positive denominator.",[("a","First numerator","number"),("b","First denominator","number"),("c","Second numerator","number"),("d","Second denominator","number")],"For addition, a/b + c/d = (ad + bc)/bd. Fractions are reduced to lowest terms."),
 ("compound-interest-calculator","Compound Interest Calculator","Estimate compounded investment growth from principal, annual rate, time and compounding frequency with clear formulas.",[("principal","Starting amount","number"),("rate","Annual interest rate (%)","number"),("years","Years","number"),("frequency","Compounding times per year (1 to 365)","number")],"Formula: A = P × (1 + r/n)^(nt). Rates are entered as annual percentages. This estimate excludes fees, taxes and additional deposits."),
 ("date-calculator","Days Between Dates Calculator","Find how many days are between two dates, how many days are left until a date, or how many have passed since one. Leap years are included.",[("start","Start date","date"),("end","End date","date")],"The result is end date minus start date in full calendar days. It does not count the starting day."),
]


GUIDES = {
"percentage-calculator": [
"Percentages express a part of a hundred, and this calculator answers three different questions. X% of a number: 25% of 200 is 200 multiplied by 25 and divided by 100, which is 50. X as a percent of Y: 30 out of 120 is 30 divided by 120, multiplied by 100, which is 25%. Percentage change: moving from 80 to 100 is a change of 20 on a starting value of 80, which is a 25% increase. The second and third questions need a starting value that is not zero, because dividing by zero has no answer.",
"Use this calculation to estimate a discount amount before subtracting it from the original price. For example, a 15 percent discount on 80 is 12, so the reduced price is 68. For a tax amount, add the percentage amount instead of subtracting it. If an item costs 80 before a 15 percent tax, the tax is 12 and the total is 92. Always check whether the advertised percentage applies to the original amount or to a previously adjusted amount.",
"A percentage increase and a percentage decrease are not interchangeable. If a price rises by 20 percent and then falls by 20 percent, the final price is not the original price. Starting from 100, the increase gives 120 and the subsequent decrease gives 96. The second percentage is calculated using 120 as its base. For sequential changes, apply each percentage to the latest amount rather than adding the percentages together.",
"Enter finite numeric values, including decimals where needed. Negative percentages produce negative results, which can be meaningful for a signed adjustment but may not describe a normal retail discount. Very large numbers may lose decimal precision because browsers use standard floating-point arithmetic. For financial settlement or tax filing, verify the rounding policy required by your jurisdiction. This tool is a quick arithmetic aid rather than an official tax determination."
],
"fraction-calculator": [
"A fraction has a numerator above a denominator. The denominator cannot be zero. A zero denominator is invalid because division by zero has no defined value. To add one half and one third, multiply each numerator by the other denominator, add the two products, and divide by the product of the denominators. The result is five sixths. Subtraction uses the same common denominator but subtracts the cross-products. The calculator then reduces the result to lowest terms using the greatest common divisor.",
"For multiplication, multiply the numerators and multiply the denominators. Two thirds times three quarters is six twelfths, which simplifies to one half. For division, multiply the first fraction by the reciprocal of the second fraction. Dividing by a fraction with a zero numerator is undefined, so the tool rejects that operation. A negative sign is always placed in the numerator of the simplified result.",
"You can enter improper fractions, such as seven fourths, as well as proper fractions. An improper fraction has a numerator whose absolute value is at least as large as the denominator. It may be written as a mixed number, but this calculator intentionally returns a single simplified fraction to keep the arithmetic unambiguous. Zero is represented as zero over one. Inputs must be whole numbers, not decimal approximations.",
"The browser has a safe range for integer arithmetic. Extremely large numerators or denominators can exceed that range, and the calculator rejects results that are not safe integers rather than silently reporting a rounded fraction. For measurements that require decimal values, convert the quantity to a fraction using an appropriate exact scale first. For example, 0.5 is one half. Check units separately because adding fractions of different physical units does not produce a meaningful measurement."
],
"compound-interest-calculator": [
"Compound interest means that previously earned interest is included in later interest calculations. This calculator uses a fixed starting amount, a constant nominal annual rate, a fixed duration measured in years, and a selected number of compounding periods per year. The mathematical formula is A = P times (1 + r/n) raised to the power n times t. Here P is principal, r is the annual rate expressed as a decimal, n is periods per year, and t is years.",
"Consider a starting amount of 1,000, a nominal annual rate of 10 percent, and semiannual compounding for one year. Each six-month period earns 5 percent. After the first period the balance is 1,050, and after the second period it is 1,102.50. The interest earned is 102.50. Annual compounding at the same nominal rate would instead produce 1,100. Compounding frequency can therefore affect the ending balance.",
"The result assumes the interest rate stays constant and that no additional deposits or withdrawals occur. It does not subtract account charges, taxes, inflation, or other costs. Actual bank and investment products may use different day-count conventions, variable rates, or periodic payment schedules. An advertised annual percentage yield is not always interchangeable with a nominal annual interest rate, so verify which type of rate your provider quotes.",
"Enter the starting amount, rate, years, and compounding frequency as numeric values. Choose one for annual, twelve for monthly, or 365 for daily compounding. The tool permits fractional years as an estimate under the standard mathematical formula, but that may not match a bank's precise posting calendar. Negative annual rates are mathematically possible within valid limits, but a rate that makes the periodic growth factor zero or negative is rejected. The displayed monetary result is rounded to two decimals for readability."
],
"date-calculator": [
"This date calculator measures the signed number of full Gregorian calendar days between two dates. Choose a start date and an end date. The tool subtracts the start date from the end date. If the end date is later, the result is positive. If the end date is earlier, the result is negative. If both dates are the same, the result is zero. The starting day is not counted as a completed day of elapsed time.",
"Leap years are included automatically. For example, from 28 February 2024 to 1 March 2024 there are two elapsed Gregorian calendar days because 29 February occurs between them. The same interval in 2025 spans one day. The same interval in 2025 spans one day. A year is generally a leap year when divisible by four, except century years that are not divisible by four hundred. The calculation follows the proleptic Gregorian calendar for supported dates.",
"Calendar dates are different from timestamps. A date such as January 1 has no specified hour, minute, or time zone. The calculator converts the date components to midnight UTC internally, so daylight saving changes in the visitor's local time zone do not change the number of calendar days. This makes it useful for checking travel date intervals, planning deadlines, and comparing dates across regions without mixing in clock-time offsets.",
"If a booking, contract, or legal deadline counts both the first and last dates, the required inclusive day count may be one greater than this tool's result for a forward interval. Always verify the counting convention in the applicable rules. The tool does not exclude weekends, holidays, or business closures. For a business-day count, you need a separate calendar with the relevant country's holiday schedule. Invalid dates such as February 29 in a non-leap year are rejected rather than silently adjusted."
]
}


# Search-intent structure for each page: H1, category hub, section headings for GUIDES paragraphs, FAQs.
META = {
"percentage-calculator": {
 "h1": "Percentage Calculator", "cat": ("math", "Math and Converters"), "app": "UtilitiesApplication",
 "headings": ["Three percentage questions", "Discounts and tax", "Percentage increase and decrease", "Input and rounding limits", "Finding a percentage or measuring change"],
 "faq": [
  ("What is 25% of 200?", "50. Multiply 200 by 25 and divide by 100."),
  ("What percent is 30 of 120?", "25%. Divide 30 by 120 to get 0.25, then multiply by 100."),
  ("How do I calculate a percentage increase?", "Subtract the old value from the new value, divide by the old value and multiply by 100. From 80 to 100 is (100 minus 80) divided by 80, which is a 25% increase."),
  ("Why is a fall from 100 to 80 only 20% when a rise from 80 to 100 is 25%?", "Each change is measured against its own starting value. The rise is 20 out of 80, and the fall is 20 out of 100."),
 ],
},
"fraction-calculator": {
 "h1": "Fraction Calculator", "cat": ("math", "Math and Converters"), "app": "UtilitiesApplication",
 "headings": ["Adding and subtracting fractions", "Multiplying and dividing fractions", "Improper fractions and zero", "Large numbers and decimals", "Comparing equivalent fractions"],
 "faq": [
  ("What is 1/2 + 1/3?", "5/6. Cross-multiply to get 3/6 + 2/6, then add the numerators."),
  ("What is 1/2 minus 1/3?", "1/6. With the common denominator 6, the fractions are 3/6 and 2/6, and 3 minus 2 is 1."),
  ("How do I divide fractions?", "Multiply the first fraction by the reciprocal of the second. For example, 3/4 divided by 1/2 is 3/4 times 2/1, which is 6/4 and simplifies to 3/2."),
  ("Can I enter decimals?", "No. Enter whole-number numerators and denominators. Convert a decimal first, for example 0.75 is 3/4."),
 ],
},
"compound-interest-calculator": {
 "h1": "Compound Interest Calculator", "cat": ("money", "Money and Business"), "app": "FinanceApplication",
 "headings": ["Compound interest formula", "Worked example", "What the estimate leaves out", "Choosing the compounding frequency", "Simple versus compound interest"],
 "faq": [
  ("How much is 1,000 at 12% compounded monthly for one year?", "About 1,126.83. Each month earns 1%, so the amount is 1,000 times 1.01 to the power of 12. Yearly compounding at 12% gives 1,120.00, and daily compounding gives about 1,127.47."),
  ("What is the difference between simple and compound interest?", "Simple interest is earned only on the starting amount. Compound interest is also earned on interest already added, so the balance grows faster over time."),
  ("What number should I enter for monthly compounding?", "Enter 12 for monthly, 4 for quarterly, 1 for yearly and 365 for daily compounding."),
  ("Does this include monthly deposits?", "No. It assumes one starting amount with no further deposits or withdrawals, and it does not subtract fees or tax."),
 ],
},
"date-calculator": {
 "h1": "Days Between Dates Calculator", "cat": ("time", "Date and Time"), "app": "UtilitiesApplication",
 "headings": ["How the days are counted", "Leap years", "Dates without time zones", "Inclusive counts and business days", "Checking a date interval"],
 "faq": [
  ("How many days are there from 1 January to 31 December 2026?", "364 days when the end date minus the start date is counted. If both the first and last day are included, it is 365."),
  ("How many days are in 2024?", "366, because 2024 is a leap year. From 1 January 2024 to 1 January 2025 is 366 days."),
  ("How do I count days left until a future date?", "Enter today as the start date and the future date as the end date. The result is the number of days remaining."),
  ("Does this count weekends and holidays?", "Yes. It counts every calendar day. It does not remove weekends or public holidays."),
 ],
},
}

def build_extra_pages(head,shell,write):
    site="https://calculateallinone.vercel.app"
    link='underline text-sky-800 dark:text-sky-300 hover:text-sky-950'
    entries=[]
    for slug,title,description,fields,explanation in PAGES:
        path="/"+slug+"/"
        m=META[slug]
        cat_slug,cat_name=m["cat"]
        body='<nav aria-label="Breadcrumb" class="text-sm text-stone-800 dark:text-stone-200"><ol class="flex flex-wrap gap-2"><li><a class="'+link+'" href="/">Home</a></li><li aria-hidden="true">/</li><li><a class="'+link+'" href="/'+cat_slug+'/">'+html.escape(cat_name)+'</a></li><li aria-hidden="true">/</li><li aria-current="page">'+html.escape(title)+'</li></ol></nav>'
        body+='<section class="mt-3 rounded-xl border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-900 p-4 sm:p-6">'
        body+='<h1 class="text-2xl font-bold text-stone-900 dark:text-white">'+html.escape(m["h1"])+'</h1>'
        body+='<p class="mt-2 text-base text-stone-700 dark:text-stone-200">'+html.escape(description)+'</p>'
        body+='<form id="extra-calculator-form" data-calculator="'+slug.replace("-calculator","").replace("compound-interest","compound")+'" class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 min-w-0">'
        if slug=="percentage-calculator":
            body+='<div class="sm:col-span-2"><label for="pct-mode" class="block font-semibold text-stone-800 dark:text-stone-100">What do you want to find?</label><select id="pct-mode" class="w-full min-w-0 max-w-full rounded-lg border border-stone-400 p-3 text-stone-900 bg-white min-h-[44px]"><option value="of">X% of a number</option><option value="whatpercent">X is what percent of Y</option><option value="change">Percentage increase or decrease</option></select></div>'
        for key,label,kind in fields:
            body+='<div class="min-w-0"><label for="'+key+'" class="block font-semibold text-stone-800 dark:text-stone-100">'+html.escape(label)+'</label>'
            body+='<input required id="'+key+'" type="'+kind+'" '+('step="1" ' if slug=="fraction-calculator" and kind=="number" else 'step="any" ' if kind=="number" else '')+'class="w-full min-w-0 rounded-lg border border-stone-400 bg-white p-3 text-lg text-stone-900 min-h-[44px]"></div>'
        if slug=="fraction-calculator":
            body+='<div class="sm:col-span-2"><label for="operation" class="block font-semibold">Operation</label><select id="operation" class="w-full rounded-lg border border-stone-400 p-3 text-stone-900 bg-white min-h-[44px]"><option value="add">Add</option><option value="subtract">Subtract</option><option value="multiply">Multiply</option><option value="divide">Divide</option></select></div>'
        body+='<button type="submit" class="sm:col-span-2 rounded-lg bg-sky-700 text-white font-bold p-3 min-h-[44px]">Calculate</button></form>'
        body+='<p role="status" aria-live="polite" id="extra-result" class="mt-4 text-xl font-bold text-stone-900 dark:text-white"></p></section>'
        body+='<section class="mt-6"><h2 class="text-xl font-semibold">How this calculation works</h2><p class="mt-3">'+html.escape(explanation)+'</p></section>'
        for heading,paragraph in zip(m["headings"],GUIDES[slug]):
            body+='<h2 class="mt-8 text-xl font-semibold">'+html.escape(heading)+'</h2><p class="mt-3 leading-7 text-stone-800 dark:text-stone-200">'+html.escape(paragraph)+'</p>'
        body+='<h2 class="mt-8 text-xl font-semibold">Common questions</h2><div class="mt-3">'
        for q,a in m["faq"]:
            body+=('<details class="border-b border-stone-300 dark:border-stone-700 py-4"><summary class="cursor-pointer font-medium text-stone-900 dark:text-stone-100 min-h-[44px] flex items-center">'+html.escape(q)+'</summary><p class="mt-2 text-base text-stone-800 dark:text-stone-200">'+html.escape(a)+'</p></details>')
        body+='</div>'
        body+='<nav aria-label="Related calculators" class="mt-6"><h2 class="text-xl font-semibold">More free calculators</h2><ul>'
        for other,other_title,*_ in PAGES:
            if other!=slug:body+='<li class="mt-2"><a class="text-sky-800 underline dark:text-sky-300" href="/'+other+'/">'+html.escape(other_title)+'</a></li>'
        body+='<li class="mt-2"><a class="text-sky-800 underline dark:text-sky-300" href="/'+cat_slug+'/">All '+html.escape(cat_name)+' tools</a></li>'
        body+='</ul></nav>'
        url=site+path
        schema=[
            {"@context":"https://schema.org","@type":"WebPage","name":title,"url":url},
            {"@context":"https://schema.org","@type":"WebApplication","name":title,"url":url,"description":description,"applicationCategory":m["app"],"operatingSystem":"Any","browserRequirements":"Requires JavaScript","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"inLanguage":"en"},
            {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":site+"/"},
                {"@type":"ListItem","position":2,"name":cat_name,"item":site+"/"+cat_slug+"/"},
                {"@type":"ListItem","position":3,"name":title,"item":url}]},
        ]
        page=head(title+" | CalculatesAll",description,path,schema)+shell(body,current_path=path)
        page=page.replace("</body>",'<script defer src="/assets/extra-calculators.js?v=20261101-quality"></script><script defer src="/assets/extra-calculators-ui.js?v=20261101-quality"></script></body>')
        write(path,page)
        entries.append((path,[]))
    return entries
