"""Standalone calculator page definitions. Uses the existing site's shell and metadata pipeline."""
import html

PAGES = [
 ("percentage-calculator","Percentage Calculator","Calculate a percentage of a number, find what percentage one amount is of another, or measure percentage change with clear inputs and steps.",[("value","Percentage (%)","number"),("total","Number","number")],"What is 25% of 200? Enter 25 and 200 to get 50. Formula: percentage divided by 100, multiplied by the number."),
 ("fraction-calculator","Fraction Calculator","Add, subtract, multiply or divide fractions and simplify the result.",[("a","First numerator","number"),("b","First denominator","number"),("c","Second numerator","number"),("d","Second denominator","number")],"For addition, a/b + c/d = (ad + bc)/bd. Fractions are reduced to lowest terms."),
 ("compound-interest-calculator","Compound Interest Calculator","Estimate compound growth from a starting amount, annual rate, time and compounding frequency.",[("principal","Starting amount","number"),("rate","Annual interest rate (%)","number"),("years","Years","number"),("frequency","Compounding times per year (1 to 365)","number")],"Formula: A = P × (1 + r/n)^(nt). Rates are entered as annual percentages. This estimate excludes fees, taxes and additional deposits."),
 ("date-calculator","Date Difference Calculator","Find the signed number of calendar days between two dates using the Gregorian calendar, including leap years.",[("start","Start date","date"),("end","End date","date")],"The result is end date minus start date in full calendar days. It does not count the starting day."),
]


GUIDES = {
"percentage-calculator": [
    "Use this mode for one precise question: what is x percent of a given amount? For example, 18% of PKR 2,500 is calculated as 2,500 × 18 ÷ 100 = PKR 450. The result is the percentage amount, not the final price after a discount or tax. Select the reverse mode when you know a part and a whole and need to find what percentage the part represents of another amount.",
    "Worked example: a shop lists an item at PKR 2,500 and offers an 18% discount. The discount amount is PKR 450. Subtract it from the original price: 2,500 − 450 = PKR 2,050 before any separately applied tax or delivery charge. If the question is instead what percentage PKR 450 is of PKR 2,500, use the reverse mode: 450 ÷ 2,500 × 100 = 18%.",
    "Percentage changes are applied to the current base at each step. Starting at 100, an increase of 20% gives 120. A later decrease of 20% is 24, leaving 96. The two changes do not cancel because the second percentage uses 120 as its base. For a tax-inclusive price or stacked discount, confirm the order and the base used by the seller.",
    "Enter finite numbers. The reverse calculation requires a non-zero whole amount. Percentage change is calculated as (new value − starting value) ÷ starting value × 100 and requires a positive starting value. A zero or negative starting value makes an ordinary increase/decrease percentage undefined or misleading. Results use browser number arithmetic and are formatted for readability, so do not treat the displayed decimal as a bank settlement or tax filing amount. This tool does not determine local tax rules, eligibility or legal pricing requirements.",
    "To find what percentage one amount is of another, divide the part by the whole and multiply by 100. For example, 18 out of 72 is 25 percent because 18 ÷ 72 × 100 = 25. This is a different question from finding 25 percent of 72, which gives 18. Check which quantity is the part and which is the whole before entering values.",
    "To measure a percentage change, subtract the starting value from the ending value, divide that difference by the starting value, and multiply by 100. A change from 80 to 92 is a 15 percent increase. A change from 80 to 68 is a 15 percent decrease. If the starting value is zero, percentage change is undefined. A negative starting value also needs careful interpretation because the sign can make a simple increase/decrease label misleading.",
],
"fraction-calculator": [
    "A fraction has a numerator above a denominator. The denominator cannot be zero. A zero denominator is invalid because division by zero has no defined value. To add one half and one third, multiply each numerator by the other denominator, add the two products, and divide by the product of the denominators. The result is five sixths. Subtraction uses the same common denominator but subtracts the cross-products. The calculator then reduces the result to lowest terms using the greatest common divisor.",
    "For multiplication, multiply the numerators and multiply the denominators. Two thirds times three quarters is six twelfths, which simplifies to one half. For division, multiply the first fraction by the reciprocal of the second fraction. Dividing by a fraction with a zero numerator is undefined, so the tool rejects that operation. A negative sign is always placed in the numerator of the simplified result.",
    "You can enter improper fractions, such as seven fourths, as well as proper fractions. An improper fraction has a numerator whose absolute value is at least as large as the denominator. It may be written as a mixed number, but this calculator intentionally returns a single simplified fraction to keep the arithmetic unambiguous. Zero is represented as zero over one. Inputs must be whole numbers, not decimal approximations.",
    "The browser has a safe range for integer arithmetic. Extremely large numerators or denominators can exceed that range, and the calculator rejects results that are not safe integers rather than silently reporting a rounded fraction. For measurements that require decimal values, convert the quantity to a fraction using an appropriate exact scale first. For example, 0.5 is one half. Check units separately because adding fractions of different physical units does not produce a meaningful measurement.",
    "A useful check after adding or subtracting is to compare the result with the size of the inputs. One half plus one third must be greater than one half and less than one, and five sixths meets that check. For multiplication of positive proper fractions, the result is smaller than either factor. These reasonableness checks do not replace the arithmetic, but they can reveal a misplaced numerator or denominator.",
    "To compare fractions with different denominators, convert them to equivalent fractions with a common denominator. For example, three quarters and two thirds become nine twelfths and eight twelfths, so three quarters is larger by one twelfth. Equivalent fractions represent the same value even when their numerators and denominators differ. The calculator returns the reduced form so equivalent results are displayed consistently.",
],
"compound-interest-calculator": [
    "Compound interest adds each period's interest to the balance before calculating the next period's interest. This calculator models one starting principal, a fixed nominal annual rate, a fixed duration in years and a fixed compounding frequency. It does not model recurring deposits, withdrawals, changing rates, fees, tax or inflation. Enter the nominal annual rate, not an APY that already includes compounding.",
    "Worked example: with a principal of 1,000, a nominal annual rate of 10%, one year and semiannual compounding, the periodic rate is 10% ÷ 2 = 5%. First period: 1,000 × 1.05 = 1,050. Second period: 1,050 × 1.05 = 1,102.50. Total interest is 1,102.50 − 1,000 = 102.50. The same principal and rate with annual compounding produce 1,100, or 100 interest.",
    "Compare the result with simple interest only as a like-for-like illustration. At 10% for one year on 1,000, simple interest is 1,000 × 0.10 × 1 = 100 and the final amount is 1,100. Semiannual compound interest gives 1,102.50 because the second period also earns interest on the first period's 50. The comparison assumes the same nominal rate and term; real products can quote rates differently.",
    "The formula is A = P × (1 + r/n)^(n×t), where P is principal, r is the annual rate as a decimal, n is compounding periods per year and t is years. The tool permits fractional years as a mathematical estimate. Banks may use actual-day conventions, payment dates and rounding rules that differ from this model. The result is not a forecast or a recommendation to invest.",
    "Compare compounding frequency using the same principal, nominal annual rate and duration. With 1,000 at 10 percent for one year, annual compounding produces 1,100, while monthly compounding produces about 1,104.71 under the stated formula. The difference is caused by interest being added to the balance more frequently. It does not mean that a monthly product is automatically better, because fees, rate conditions, access restrictions and taxes can outweigh the small mathematical difference.",
    "Simple interest uses the original principal as the base for every period. At 1,000 and 10 percent for three years, simple interest adds 300 and gives 1,300 before costs. Annual compounding gives 1,331 because each year's interest becomes part of the next year's base. Use the calculator only when the provider's rate is a nominal annual rate and the stated compounding frequency matches the product terms. If the provider quotes APY or an effective annual rate, do not enter it as though it were a nominal rate without converting it correctly.",
],
"date-calculator": [
    "This tool returns signed elapsed Gregorian calendar days: end date minus start date. A later end date gives a positive result, an earlier end date gives a negative result, and identical dates give zero. The start date is not counted as a completed elapsed day. The calculation uses date-only values, not hours, time zones or daylight-saving clock changes.",
    "Worked example: 28 February 2024 to 1 March 2024 is 2 days because 29 February is a leap day. The same dates in 2025 are 1 day. If a form or contract counts both the first and last dates, the inclusive count for a forward interval is normally the elapsed result plus one. Check the specific rule before using a date count for a deadline.",
    "To verify a result manually, count the calendar-day boundary crossings from the start date up to the end date. For a forward interval that crosses a month, include the actual length of that month. February has 29 days in a leap year and 28 otherwise. The Gregorian leap-year rule is divisible by four, except century years unless divisible by 400.",
    "This calculator does not count weekdays only, remove public holidays, calculate working days, or decide legal deadline rules. It also does not measure exact elapsed hours between timestamps. Use a jurisdiction-specific business calendar for working-day deadlines, and confirm contract, court, travel or immigration counting rules with the relevant authority. Invalid dates are rejected rather than silently changed.",
    "Before relying on a result, compare the entered dates with the source document and confirm whether it asks for elapsed days, inclusive calendar days or business days. Those counting methods answer different questions and can produce different totals.",
    "For example, a trip that begins on 10 June and ends on 15 June spans five elapsed calendar days when the start date is excluded. If a form asks for every date touched by the trip, it may expect six dates instead. This difference is why the result should be described as elapsed days, not automatically as the number of nights, billable days or inclusive deadline days.",
    "Use the signed result to compare date order as well as duration. A result of minus 5 means the end date is five calendar days before the start date. Swapping the two dates changes the sign but not the absolute number of days. This tool does not calculate hours between timestamps, count working days, identify public holidays or decide when a legal notice period expires. Those tasks require the relevant time zone, local rules and calendar.",
]
}


CATEGORY = {
    "percentage-calculator": ("/math/", "Math and Converters"),
    "fraction-calculator": ("/math/", "Math and Converters"),
    "compound-interest-calculator": ("/money/", "Money and Business"),
    "date-calculator": ("/time/", "Date and Time"),
}

RELATED_LINKS = {
    "percentage-calculator": [
        ("/discount-calculator/", "Discount Calculator"),
        ("/profit-loss-calculator/", "Profit and Loss Calculator"),
        ("/fraction-calculator/", "Fraction Calculator"),
    ],
    "fraction-calculator": [
        ("/percentage-calculator/", "Percentage Calculator"),
        ("/standard-calculator/", "Standard & Scientific Calculator"),
        ("/unit-converter/", "Unit Converter"),
    ],
    "compound-interest-calculator": [
        ("/emi-calculator/", "EMI Calculator"),
        ("/profit-loss-calculator/", "Profit and Loss Calculator"),
        ("/discount-calculator/", "Discount Calculator"),
    ],
    "date-calculator": [
        ("/age-calculator/", "Age Calculator"),
        ("/years-to-days-calculator/", "Years to Days Calculator"),
        ("/query-calculator/", "Query Calculator"),
    ],
}

SECTION_HEADINGS = {
    "percentage-calculator": ["Worked percentage examples", "Discounts and tax", "Percentage increase and decrease", "Input limits and rounding", "Finding a percentage share", "How percentage change is measured"],
    "fraction-calculator": ["Adding and subtracting fractions", "Multiplying and dividing fractions", "Improper fractions and zero denominators", "Large numbers and decimal inputs", "Check the result", "Compare equivalent fractions"],
    "compound-interest-calculator": ["What compound interest means", "Worked example: semiannual compounding", "Simple versus compound interest", "Formula and variables", "Compare compounding frequency", "Assumptions and limits"],
    "date-calculator": ["How elapsed days are counted", "Leap-year example", "Verify the result manually", "Business days and legal deadlines", "Inclusive versus elapsed dates", "Date order and negative results"],
}

FAQS = {
    "percentage-calculator": [
        ("What is 25% of 200?", "50. Multiply 200 by 25 and divide by 100."),
        ("What percentage is 45 of 250?", "18%. Divide 45 by 250 and multiply by 100."),
        ("What percentage is 30 out of 120?", "25%. Divide 30 by 120 and multiply by 100."),
        ("What is the percentage change from 80 to 100?", "A 25% increase. The change is 20, and 20 divided by the starting value 80 is 0.25."),
        ("Why does a 20% rise followed by a 20% fall not return to the starting amount?", "Starting from 100, a 20% rise gives 120. A 20% fall from 120 is 24, leaving 96."),
    ],
    "fraction-calculator": [
        ("What is 1/2 + 1/3?", "5/6. Convert to sixths: 3/6 + 2/6 = 5/6."),
        ("How do I divide two fractions?", "Multiply the first fraction by the reciprocal of the second. For example, 3/4 divided by 1/2 is 3/2."),
        ("Can a fraction have a zero denominator?", "No. A zero denominator is invalid because division by zero is undefined."),
        ("Can I enter decimal numerators or denominators?", "No. Enter whole-number numerators and denominators. Convert a decimal first, for example 0.75 is 3/4."),
    ],
    "compound-interest-calculator": [
        ("How much is 1,000 at 10% compounded semiannually for one year?", "1,102.50. Each six-month period earns 5%, so the balance is 1,000 × 1.05 × 1.05."),
        ("What is the difference between simple and compound interest?", "Simple interest is calculated on the starting principal. Compound interest also earns interest on interest already added to the balance."),
        ("What number should I enter for monthly compounding?", "Enter 12 for monthly, 4 for quarterly, 1 for annual and 365 for daily compounding."),
        ("Does this include fees, tax or additional deposits?", "No. The estimate assumes one starting amount, a constant nominal annual rate and no deposits, withdrawals, fees or tax."),
    ],
    "date-calculator": [
        ("How many days are there from 28 February 2024 to 1 March 2024?", "2 elapsed Gregorian calendar days because 29 February 2024 is a leap day."),
        ("How many days are there from 28 February 2025 to 1 March 2025?", "1 elapsed calendar day. 2025 is not a leap year."),
        ("Does the result include both the start date and end date?", "No. It is elapsed days, calculated as end date minus start date. An inclusive count may be one greater for a forward interval."),
        ("Does this calculate business days?", "No. It counts calendar days and does not remove weekends or public holidays. Use a calendar for the relevant jurisdiction for business-day deadlines."),
    ],
}


SOURCE_LINKS = {
    "percentage-calculator": [
        ("OpenStax: Percent applications and percent increase", "https://openstax.org/books/prealgebra-2e/pages/6-2-solve-general-applications-of-percent", "Textbook reference for percent applications, increase and decrease calculations."),
    ],
    "fraction-calculator": [
        ("OpenStax: Add and subtract fractions with different denominators", "https://openstax.org/books/prealgebra/pages/4-5-add-and-subtract-fractions-with-different-denominators", "Explains common denominators and the worked 1/2 + 1/3 = 5/6 example."),
        ("OpenStax: Fraction operations", "https://openstax.org/books/prealgebra-2e/pages/4-key-concepts", "Summarizes fraction multiplication, division, addition and subtraction."),
    ],
    "compound-interest-calculator": [
        ("Investor.gov: Compound Interest Calculator", "https://www.investor.gov/financial-tools-calculators/calculators/compound-interest-calculator", "Official investor education reference for principal, annual rate, time and compounding frequency."),
        ("Investor.gov: What is compound interest?", "https://www.investor.gov/additional-resources/information/youth/teachers-classroom-resources/what-compound-interest", "Explains how interest can accrue on both principal and previously earned interest."),
    ],
    "date-calculator": [
        ("U.S. Naval Observatory: Leap Years", "https://aa.usno.navy.mil/faq/leap_years", "Authoritative explanation of the Gregorian leap-year rule, including century years and the 400-year exception."),
    ],
}

def build_extra_pages(head,shell,write):
    entries=[]
    site="https://calculateallinone.vercel.app"
    for slug,title,description,fields,explanation in PAGES:
        path="/"+slug+"/"
        category_path,category_name=CATEGORY[slug]
        compact_mobile = slug in ("fraction-calculator", "compound-interest-calculator")
        section_padding = "p-3 sm:p-6" if compact_mobile else "p-4 sm:p-6"
        form_margin = "mt-2" if compact_mobile else "mt-3"
        mobile_columns = "grid-cols-2" if compact_mobile else "grid-cols-1"
        full_row_class = "col-span-2" if compact_mobile else "sm:col-span-2"
        trust_markup = (
            '<p class="mt-2 text-sm text-stone-700 dark:text-stone-300">Maintained by <a class="text-sky-800 underline dark:text-sky-300" href="/about/">Muhammad Fayyaz Adeel</a>. See the method, references and limitations below.</p>'
            '<p class="mt-1 text-xs text-stone-600 dark:text-stone-400">Verification: representative results and invalid inputs are covered by automated tests. This is not an independent professional review.</p>'
        )
        body='<nav aria-label="Breadcrumb" class="mb-2 text-sm text-stone-700 dark:text-stone-200"><ol class="flex flex-wrap gap-2"><li><a class="underline text-sky-800 dark:text-sky-300" href="/">Home</a></li><li aria-hidden="true">/</li><li><a class="underline text-sky-800 dark:text-sky-300" href="'+category_path+'">'+html.escape(category_name)+'</a></li><li aria-hidden="true">/</li><li aria-current="page">'+html.escape(title)+'</li></ol></nav>'
        body+='<section class="rounded-xl border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-900 '+section_padding+'">'
        body+='<h1 class="'+('text-xl sm:text-2xl' if compact_mobile else 'text-2xl')+' font-bold text-stone-900 dark:text-white">'+html.escape(title)+'</h1>'
        body+='<p class="mt-2 text-base text-stone-700 dark:text-stone-200">'+html.escape(description)+'</p>'
        if not compact_mobile:
            body+=trust_markup
        body+='<form id="extra-calculator-form" data-calculator="'+slug.replace("-calculator","").replace("compound-interest","compound").replace("date","date")+'" class="'+form_margin+' grid '+mobile_columns+' sm:grid-cols-2 gap-x-3 gap-y-2 min-w-0">'
        if slug=="percentage-calculator":
            body+="<div class='sm:col-span-2 mt-1'><label for='percentage-mode' class='block text-sm font-semibold text-stone-800 dark:text-stone-100'>Calculation type</label><select id='percentage-mode' class='w-full min-w-0 rounded-lg border border-stone-400 bg-white p-2 text-base text-stone-900 min-h-[44px]'><option value='of'>What is X% of a number?</option><option value='share'>What percentage is one number of another?</option><option value='change'>What is the percentage change?</option></select></div>"
        for key,label,kind in fields:
            body+='<div class="min-w-0"><label for="'+key+'" class="block text-sm font-semibold text-stone-800 dark:text-stone-100">'+html.escape(label)+'</label>'
            body+='<input required id="'+key+'" type="'+kind+'" '+('step="1" ' if slug=="fraction-calculator" and kind=="number" else 'step="any" ' if kind=="number" else '')+'class="w-full min-w-0 rounded-lg border border-stone-400 bg-white p-2 text-base text-stone-900 min-h-[44px]"></div>'
        if slug=="fraction-calculator":
            body+='<div class="sm:col-span-2 compact-form-full min-w-0"><label for="operation" class="block text-sm font-semibold">Operation</label><select id="operation" class="w-full min-w-0 rounded-lg border border-stone-400 p-2 text-base text-stone-900 bg-white min-h-[44px]"><option value="add">Add</option><option value="subtract">Subtract</option><option value="multiply">Multiply</option><option value="divide">Divide</option></select></div>'
        body+='<button type="submit" class="sm:col-span-2 compact-form-full rounded-lg bg-sky-700 text-white font-bold p-3 min-h-[44px]">Calculate</button></form>'
        body+='<p role="status" aria-live="polite" id="extra-result" class="mt-3 text-xl font-bold text-stone-900 dark:text-white"></p>'
        if compact_mobile:
            body+=trust_markup
        body+='</section>'
        body+='<section class="mt-6"><h2 class="text-xl font-semibold">How this calculation works</h2><p class="mt-3">'+html.escape(explanation)+'</p></section>'
        for heading,paragraph in zip(SECTION_HEADINGS[slug],GUIDES[slug]):
            body+='<section class="mt-6"><h2 class="text-xl font-semibold">'+html.escape(heading)+'</h2><p class="mt-3 leading-7 text-stone-800 dark:text-stone-200">'+html.escape(paragraph)+'</p></section>'
        faq_items=FAQS[slug]
        body+='<section class="mt-8"><h2 class="text-xl font-semibold">Common questions</h2><div class="mt-3">'
        for question,answer in faq_items:
            body+='<details class="border-b border-stone-300 dark:border-stone-700 py-4"><summary class="cursor-pointer font-medium text-stone-900 dark:text-stone-100 min-h-[44px] flex items-center">'+html.escape(question)+'</summary><p class="mt-2 text-base text-stone-800 dark:text-stone-200">'+html.escape(answer)+'</p></details>'
        body+='</div></section>'
        body+='<section class="mt-8"><h2 class="text-xl font-semibold">Sources and references</h2><ul class="mt-3 list-disc pl-6 space-y-2">'
        for source_title,source_url,source_note in SOURCE_LINKS[slug]:
            body+='<li><a class="text-sky-800 underline dark:text-sky-300" href="'+html.escape(source_url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+html.escape(source_title)+'</a><p class="text-sm text-stone-700 dark:text-stone-300">'+html.escape(source_note)+'</p></li>'
        body+='</ul></section>'
        body+='<p class="mt-6 text-sm text-stone-700 dark:text-stone-300">Found a calculation or content issue? <a class="text-sky-800 underline dark:text-sky-300" href="/contact/">Report this calculator and include the values you entered.</a></p>'
        body+='<nav aria-label="Related calculators" class="mt-8"><h2 class="text-xl font-semibold">More free calculators</h2><ul>'
        for related_path,related_title in RELATED_LINKS[slug]:
            body+='<li class="mt-2"><a class="text-sky-800 underline dark:text-sky-300" href="'+related_path+'">'+html.escape(related_title)+'</a></li>'
        body+='<li class="mt-2"><a class="text-sky-800 underline dark:text-sky-300" href="'+category_path+'">All '+html.escape(category_name)+' tools</a></li></ul></nav>'
        breadcrumb_items=[
            {"@type":"ListItem","position":1,"name":"Home","item":site+"/"},
            {"@type":"ListItem","position":2,"name":category_name,"item":site+category_path},
            {"@type":"ListItem","position":3,"name":title,"item":site+path},
        ]
        faq_entities=[{"@type":"Question","name":question,"acceptedAnswer":{"@type":"Answer","text":answer}} for question,answer in faq_items]
        schema=[
            {"@context":"https://schema.org","@type":"WebPage","name":title,"url":site+path,"description":description,"author":{"@id":site+"/#maintainer"},"citation":[source_url for source_title,source_url,source_note in SOURCE_LINKS[slug]],"inLanguage":"en"},
            {"@context":"https://schema.org","@type":"WebApplication","name":title,"url":site+path,"description":description,"applicationCategory":"FinanceApplication" if slug=="compound-interest-calculator" else "UtilitiesApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","author":{"@id":site+"/#maintainer"},"publisher":{"@id":site+"/#organization"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"inLanguage":"en"},
            {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":breadcrumb_items},
            {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_entities},
        ]
        page=head(title+" | CalculatesAll",description,path,schema)+shell(body,current_path=path)
        page=page.replace("</body>",'<script defer src="/assets/extra-calculators.js"></script><script defer src="/assets/extra-calculators-ui.js"></script></body>')
        write(path,page)
        entries.append((path,[]))
    return entries
