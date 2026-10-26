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
"Percentages express a part of a hundred. When you enter 25 as the percentage and 200 as the number, the calculator multiplies 200 by 25 and divides by 100. The result is 50. This operation answers what a percentage of a number is. It is different from finding what percentage one number represents of another. For that reverse question, divide the part by the total and multiply by 100, provided the total is not zero.",
"Use this calculation to estimate a discount amount before subtracting it from the original price. For example, a 15 percent discount on 80 is 12, so the reduced price is 68. For a tax amount, add the percentage amount instead of subtracting it. If an item costs 80 before a 15 percent tax, the tax is 12 and the total is 92. Always check whether the advertised percentage applies to the original amount or to a previously adjusted amount.",
"A percentage increase and a percentage decrease are not interchangeable. If a price rises by 20 percent and then falls by 20 percent, the final price is not the original price. Starting from 100, the increase gives 120 and the subsequent decrease gives 96. The second percentage is calculated using 120 as its base. For sequential changes, apply each percentage to the latest amount rather than adding the percentages together.",
"Enter finite numeric values, including decimals where needed. Negative percentages produce negative results, which can be meaningful for a signed adjustment but may not describe a normal retail discount. Very large numbers may lose decimal precision because browsers use standard floating-point arithmetic. For financial settlement or tax filing, verify the rounding policy required by your jurisdiction. This tool is a quick arithmetic aid rather than an official tax determination."
],
"fraction-calculator": [
"A fraction has a numerator above a denominator. The denominator cannot be zero. To add one half and one third, multiply each numerator by the other denominator, add the two products, and divide by the product of the denominators. The result is five sixths. Subtraction uses the same common denominator but subtracts the cross-products. The calculator then reduces the result to lowest terms using the greatest common divisor.",
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
"Leap years are included automatically. For example, February 28 to March 1 in 2024 spans two calendar days because February 29 occurs between them. The same interval in 2025 spans one day. A year is generally a leap year when divisible by four, except century years that are not divisible by four hundred. The calculation follows the proleptic Gregorian calendar for supported dates.",
"Calendar dates are different from timestamps. A date such as January 1 has no specified hour, minute, or time zone. The calculator converts the date components to midnight UTC internally, so daylight saving changes in the visitor's local time zone do not change the number of calendar days. This makes it useful for checking travel date intervals, planning deadlines, and comparing dates across regions without mixing in clock-time offsets.",
"If a booking, contract, or legal deadline counts both the first and last dates, the required inclusive day count may be one greater than this tool's result for a forward interval. Always verify the counting convention in the applicable rules. The tool does not exclude weekends, holidays, or business closures. For a business-day count, you need a separate calendar with the relevant country's holiday schedule. Invalid dates such as February 29 in a non-leap year are rejected rather than silently adjusted."
]
}

def build_extra_pages(head,shell,write):
    entries=[]
    for slug,title,description,fields,explanation in PAGES:
        path="/"+slug+"/"
        body='<section class="rounded-xl border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-900 p-4 sm:p-6">'
        body+='<h1 class="text-2xl font-bold text-stone-900 dark:text-white">'+html.escape(title)+'</h1>'
        body+='<p class="mt-2 text-base text-stone-700 dark:text-stone-200">'+html.escape(description)+'</p>'
        body+='<form id="extra-calculator-form" data-calculator="'+slug.replace("-calculator","").replace("compound-interest","compound").replace("date","date")+'" class="mt-4 grid gap-3">'
        for key,label,kind in fields:
            body+='<label for="'+key+'" class="font-semibold text-stone-800 dark:text-stone-100">'+html.escape(label)+'</label>'
            body+='<input required id="'+key+'" type="'+kind+'" '+('step="any" ' if kind=="number" else '')+'class="w-full rounded-lg border border-stone-400 bg-white p-3 text-lg text-stone-900 min-h-[44px]">'
        if slug=="fraction-calculator":
            body+='<label for="operation" class="font-semibold">Operation</label><select id="operation" class="rounded-lg border border-stone-400 p-3 text-stone-900 bg-white"><option value="add">Add</option><option value="subtract">Subtract</option><option value="multiply">Multiply</option><option value="divide">Divide</option></select>'
        body+='<button type="submit" class="rounded-lg bg-sky-700 text-white font-bold p-3 min-h-[44px]">Calculate</button></form>'
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
