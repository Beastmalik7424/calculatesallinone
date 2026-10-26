"""Standalone calculator page definitions. Uses the existing site's shell and metadata pipeline."""
import html

PAGES = [
 ("percentage-calculator","Percentage Calculator","Calculate a percentage of any number instantly. Enter the percentage and the base value to see the exact arithmetic result.",[("value","Percentage (%)","number"),("total","Number","number")],"What is 25% of 200? Enter 25 and 200 to get 50. Formula: percentage divided by 100, multiplied by the number."),
 ("fraction-calculator","Fraction Calculator","Add, subtract, multiply and divide two fractions. Get a simplified fraction result with a positive denominator.",[("a","First numerator","number"),("b","First denominator","number"),("c","Second numerator","number"),("d","Second denominator","number")],"For addition, a/b + c/d = (ad + bc)/bd. Fractions are reduced to lowest terms."),
 ("compound-interest-calculator","Compound Interest Calculator","Estimate compounded investment growth from principal, annual rate, time and compounding frequency with clear formulas.",[("principal","Starting amount","number"),("rate","Annual interest rate (%)","number"),("years","Years","number"),("frequency","Compounding times per year (1 to 365)","number")],"Formula: A = P × (1 + r/n)^(nt). Rates are entered as annual percentages. This estimate excludes fees, taxes and additional deposits."),
 ("date-calculator","Date Difference Calculator","Find the signed number of calendar days between two dates using the Gregorian calendar, including leap years.",[("start","Start date","date"),("end","End date","date")],"The result is end date minus start date in full calendar days. It does not count the starting day."),
]

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
