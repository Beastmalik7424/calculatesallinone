"""Standalone calculator page definitions. Uses the existing site's shell and metadata pipeline."""
import html

PAGES = [
 ("percentage-calculator","Percentage Calculator","Calculate a percentage of any number instantly. Enter the percentage and the base value to see the exact arithmetic result.",[("value","Percentage (%)","number"),("total","Number","number")],"What is 25% of 200? Enter 25 and 200 to get 50. Formula: percentage divided by 100, multiplied by the number."),
 ("fraction-calculator","Fraction Calculator","Add, subtract, multiply and divide two fractions. Get a simplified fraction result with a positive denominator.",[("a","First numerator","number"),("b","First denominator","number"),("c","Second numerator","number"),("d","Second denominator","number")],"For addition, a/b + c/d = (ad + bc)/bd. Fractions are reduced to lowest terms."),
 ("compound-interest-calculator","Compound Interest Calculator","Estimate compounded investment growth from principal, annual rate, time and compounding frequency with clear formulas.",[("principal","Starting amount","number"),("rate","Annual interest rate (%)","number"),("years","Years","number"),("frequency","Compounding times per year (1 to 365)","number")],"Formula: A = P × (1 + r/n)^(nt). Rates are entered as annual percentages. This estimate excludes fees, taxes and additional deposits."),
 ("date-calculator","Date Difference Calculator","Find the signed number of calendar days between two dates using the Gregorian calendar, including leap years.",[("start","Start date","date"),("end","End date","date")],"The result is end date minus start date in full calendar days. It does not count the starting day."),
]


GUIDES = {
"percentage-calculator": [
"Use this mode for one precise question: what is x percent of a given amount? For example, 18% of PKR 2,500 is calculated as 2,500 × 18 ÷ 100 = PKR 450. The result is the percentage amount, not the final price after a discount or tax. Select the reverse mode when you know a part and a whole and need to find what percentage the part represents.",
"Worked example: a shop lists an item at PKR 2,500 and offers an 18% discount. The discount amount is PKR 450. Subtract it from the original price: 2,500 − 450 = PKR 2,050 before any separately applied tax or delivery charge. If the question is instead what percentage PKR 450 is of PKR 2,500, use the reverse mode: 450 ÷ 2,500 × 100 = 18%.",
"Percentage changes are applied to the current base at each step. Starting at 100, an increase of 20% gives 120. A later decrease of 20% is 24, leaving 96. The two changes do not cancel because the second percentage uses 120 as its base. For a tax-inclusive price or stacked discount, confirm the order and the base used by the seller.",
"Enter finite numbers. The reverse calculation requires a non-zero whole amount. Negative values can be mathematically valid for signed adjustments but are not ordinary retail prices. Results use browser number arithmetic and are formatted for readability, so do not treat the displayed decimal as a bank settlement or tax filing amount. This tool does not determine local tax rules, eligibility or legal pricing requirements."
],
"fraction-calculator": [
"A fraction has a numerator above a denominator. The denominator cannot be zero. To add one half and one third, multiply each numerator by the other denominator, add the two products, and divide by the product of the denominators. The result is five sixths. Subtraction uses the same common denominator but subtracts the cross-products. The calculator then reduces the result to lowest terms using the greatest common divisor.",
"For multiplication, multiply the numerators and multiply the denominators. Two thirds times three quarters is six twelfths, which simplifies to one half. For division, multiply the first fraction by the reciprocal of the second fraction. Dividing by a fraction with a zero numerator is undefined, so the tool rejects that operation. A negative sign is always placed in the numerator of the simplified result.",
"You can enter improper fractions, such as seven fourths, as well as proper fractions. An improper fraction has a numerator whose absolute value is at least as large as the denominator. It may be written as a mixed number, but this calculator intentionally returns a single simplified fraction to keep the arithmetic unambiguous. Zero is represented as zero over one. Inputs must be whole numbers, not decimal approximations.",
"The browser has a safe range for integer arithmetic. Extremely large numerators or denominators can exceed that range, and the calculator rejects results that are not safe integers rather than silently reporting a rounded fraction. For measurements that require decimal values, convert the quantity to a fraction using an appropriate exact scale first. For example, 0.5 is one half. Check units separately because adding fractions of different physical units does not produce a meaningful measurement."
],
"compound-interest-calculator": [
"Compound interest adds each period's interest to the balance before calculating the next period's interest. This calculator models one starting principal, a fixed nominal annual rate, a fixed duration in years and a fixed compounding frequency. It does not model recurring deposits, withdrawals, changing rates, fees, tax or inflation. Enter the nominal annual rate, not an APY that already includes compounding.",
"Worked example: with a principal of 1,000, a nominal annual rate of 10%, one year and semiannual compounding, the periodic rate is 10% ÷ 2 = 5%. First period: 1,000 × 1.05 = 1,050. Second period: 1,050 × 1.05 = 1,102.50. Total interest is 1,102.50 − 1,000 = 102.50. The same principal and rate with annual compounding produce 1,100, or 100 interest.",
"Compare the result with simple interest only as a like-for-like illustration. At 10% for one year on 1,000, simple interest is 1,000 × 0.10 × 1 = 100 and the final amount is 1,100. Semiannual compound interest gives 1,102.50 because the second period also earns interest on the first period's 50. The comparison assumes the same nominal rate and term; real products can quote rates differently.",
"The formula is A = P × (1 + r/n)^(n×t), where P is principal, r is the annual rate as a decimal, n is compounding periods per year and t is years. The tool permits fractional years as a mathematical estimate. Banks may use actual-day conventions, payment dates and rounding rules that differ from this model. The result is not a forecast or a recommendation to invest."
],
"date-calculator": [
"This tool returns signed elapsed Gregorian calendar days: end date minus start date. A later end date gives a positive result, an earlier end date gives a negative result, and identical dates give zero. The start date is not counted as a completed elapsed day. The calculation uses date-only values, not hours, time zones or daylight-saving clock changes.",
"Worked example: 28 February 2024 to 1 March 2024 is 2 days because 29 February is a leap day. The same dates in 2025 are 1 day. If a form or contract counts both the first and last dates, the inclusive count for a forward interval is normally the elapsed result plus one. Check the specific rule before using a date count for a deadline.",
"To verify a result manually, count the calendar-day boundary crossings from the start date up to the end date. For a forward interval that crosses a month, include the actual length of that month. February has 29 days in a leap year and 28 otherwise. The Gregorian leap-year rule is divisible by four, except century years unless divisible by 400.",
"This calculator does not count weekdays only, remove public holidays, calculate working days, or decide legal deadline rules. It also does not measure exact elapsed hours between timestamps. Use a jurisdiction-specific business calendar for working-day deadlines, and confirm contract, court, travel or immigration counting rules with the relevant authority. Invalid dates are rejected rather than silently changed."
]
}

def build_extra_pages(head,shell,write):
    entries=[]
    for slug,title,description,fields,explanation in PAGES:
        path="/"+slug+"/"
        body='<section class="rounded-xl border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-900 p-4 sm:p-6">'
        body+='<h1 class="text-2xl font-bold text-stone-900 dark:text-white">'+html.escape(title)+'</h1>'
        body+='<p class="mt-2 text-base text-stone-700 dark:text-stone-200">'+html.escape(description)+'</p>'
        body+='<form id="extra-calculator-form" data-calculator="'+slug.replace("-calculator","").replace("compound-interest","compound").replace("date","date")+'" class="mt-3 grid grid-cols-2 gap-x-3 gap-y-2">'
        for key,label,kind in fields:
            body+='<div class="min-w-0"><label for="'+key+'" class="block text-sm font-semibold text-stone-800 dark:text-stone-100">'+html.escape(label)+'</label>'
            body+='<input required id="'+key+'" type="'+kind+'" '+('step="1" ' if slug=="fraction-calculator" and kind=="number" else 'step="any" ' if kind=="number" else '')+'class="w-full min-w-0 rounded-lg border border-stone-400 bg-white p-2 text-base text-stone-900 min-h-[44px]"></div>'
        if slug=="fraction-calculator":
            body+='<div class="col-span-2 min-w-0"><label for="operation" class="block text-sm font-semibold">Operation</label><select id="operation" class="w-full min-w-0 rounded-lg border border-stone-400 p-2 text-base text-stone-900 bg-white min-h-[44px]"><option value="add">Add</option><option value="subtract">Subtract</option><option value="multiply">Multiply</option><option value="divide">Divide</option></select></div>'
        body+='<button type="submit" class="col-span-2 rounded-lg bg-sky-700 text-white font-bold p-3 min-h-[44px]">Calculate</button></form>'
        body+='<p role="status" aria-live="polite" id="extra-result" class="mt-4 text-xl font-bold text-stone-900 dark:text-white"></p></section>'
        body+='<section class="mt-6"><h2 class="text-xl font-semibold">How this calculation works</h2><p class="mt-3">'+html.escape(explanation)+'</p></section>'
        for paragraph in GUIDES[slug]:
            body+='<p class="mt-4 leading-7 text-stone-800 dark:text-stone-200">'+html.escape(paragraph)+'</p>'
        body+='<nav aria-label="Related calculators" class="mt-6"><h2 class="text-xl font-semibold">More free calculators</h2><ul>'
        for other,other_title,*_ in PAGES:
            if other!=slug:body+='<li class="mt-2"><a class="text-sky-800 underline dark:text-sky-300" href="/'+other+'/">'+html.escape(other_title)+'</a></li>'
        body+='</ul></nav>'
        schema=[{"@context":"https://schema.org","@type":"WebPage","name":title,"url":"https://calculateallinone.vercel.app"+path}]
        page=head(title+" | CalculatesAll",description,path,schema)+shell(body,current_path=path)
        page=page.replace("</body>",'<script defer src="/assets/extra-calculators.js"></script><script defer src="/assets/extra-calculators-ui.js"></script></body>')
        write(path,page)
        entries.append((path,[]))
    return entries
