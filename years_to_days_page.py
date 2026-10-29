"""A years-to-days calculator integrated with the site's existing shell and SEO pipeline."""
def build_years_to_days_page(head, shell, write):
    path = "/years-to-days-calculator/"
    title = "Years to Days Calculator | CalculatesAll"
    description = (
        "Convert whole calendar years to exact elapsed days from a start date. "
        "Count leap days, weeks, hours and minutes with worked examples."
    )
    body = """
<section class="rounded-xl border border-stone-300 dark:border-stone-700 bg-white dark:bg-stone-900 p-4 sm:p-6">
  <h1 class="text-2xl font-bold text-stone-900 dark:text-white">Years to Days Calculator</h1>
  <p class="mt-3 text-base text-stone-800 dark:text-stone-200">Enter a start date and a whole number of years to find the exact number of elapsed calendar days. The calculation uses the Gregorian calendar and includes leap years.</p>
  <form id="years-days-form" class="mt-4 grid gap-3" novalidate>
    <div class="grid sm:grid-cols-2 gap-4">
      <div>
        <label class="block font-semibold text-stone-900 dark:text-white" for="yd-start">Start date</label>
        <input required class="w-full rounded-lg border border-stone-400 dark:border-stone-500 bg-white dark:bg-stone-900 dark:text-white text-stone-900 p-3 min-h-[44px]" id="yd-start" type="date" min="0001-01-01" max="9999-12-31">
      </div>
      <div>
        <label class="block font-semibold text-stone-900 dark:text-white" for="yd-years">Whole calendar years</label>
        <input required class="w-full rounded-lg border border-stone-400 dark:border-stone-500 bg-white dark:bg-stone-900 dark:text-white text-stone-900 p-3 min-h-[44px]" id="yd-years" type="number" min="0" max="9998" step="1" value="4" inputmode="numeric">
      </div>
    </div>
    <button class="rounded-lg bg-sky-700 text-white font-bold p-3 min-h-[44px]" type="submit">Calculate exact days</button>
  </form>
  <p id="yd-error" role="alert" class="mt-3 text-red-700 dark:text-red-300" aria-live="assertive"></p>
  <div aria-live="polite" class="mt-4">
    <p class="text-base text-stone-700 dark:text-stone-200">Total elapsed days</p>
    <p id="yd-days" class="text-3xl font-bold text-stone-900 dark:text-white">—</p>
    <p id="yd-end" class="mt-2 text-stone-700 dark:text-stone-200"></p>
    <div class="overflow-x-auto">
      <table class="w-full mt-3 text-left">
        <tbody>
          <tr><th scope="row" class="p-2 border-b border-stone-300 dark:border-stone-700">Weeks and days</th><td class="p-2 border-b border-stone-300 dark:border-stone-700" id="yd-weeks">—</td></tr>
          <tr><th scope="row" class="p-2 border-b border-stone-300 dark:border-stone-700">Hours</th><td class="p-2 border-b border-stone-300 dark:border-stone-700" id="yd-hours">—</td></tr>
          <tr><th scope="row" class="p-2 border-b border-stone-300 dark:border-stone-700">Minutes</th><td class="p-2 border-b border-stone-300 dark:border-stone-700" id="yd-minutes">—</td></tr>
          <tr><th scope="row" class="p-2 border-b border-stone-300 dark:border-stone-700">February 29 dates within the interval</th><td class="p-2 border-b border-stone-300 dark:border-stone-700" id="yd-leap">—</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="mt-6">
  <h2 class="text-xl font-semibold">How years are converted to days</h2>
  <p class="mt-3 text-base leading-relaxed">A calendar year normally has 365 days, but a leap year has 366. Leap years occur when the year is divisible by 4, except century years that are not divisible by 400. For example, 2000 was a leap year, but 1900 and 2100 are not. That means multiplying a number of years by 365 will not always give the exact answer.</p>
  <p class="mt-3 text-base leading-relaxed">This tool adds the specified number of calendar years to the start date and counts elapsed days up to, but not including, the end date. It calculates using UTC calendar dates, so daylight saving or your computer's time zone does not add or remove a day. Zero years returns zero days. Only whole years are accepted.</p>
  <h2 class="text-xl font-semibold mt-6">Worked examples</h2>
  <p class="mt-3 text-base leading-relaxed"><strong>Four years:</strong> From January 1, 2024 to January 1, 2028 there are <strong>1,461 days</strong>, including February 29, 2024. Four calendar years crossing the non-leap century year 2100 can instead be 1,460 days.</p>
  <p class="mt-3 text-base leading-relaxed"><strong>80 years:</strong> From October 30, 2026 to October 30, 2106 there are <strong>29,219 days</strong>, including 19 leap days. The exact count depends on the date and years chosen.</p>
  <p class="mt-3 text-base leading-relaxed"><strong>February 29 birthdays or anniversaries:</strong> If the starting date is February 29 and the ending year is not a leap year, this calculator uses February 28 as the anniversary. Other contracts or institutions may use March 1 instead. This rule changes the elapsed-day count.</p>
  <h2 class="text-xl font-semibold mt-6">Quick reference</h2>
  <p class="mt-3 text-base leading-relaxed">One ordinary year is 365 days and one leap year is 366 days. Five years usually cover 1,826 or 1,827 days. A span of 80 years cannot be converted exactly without a start date, especially when it crosses a non-leap century year.</p>
  <h2 class="text-xl font-semibold mt-6">Common uses</h2>
  <p class="mt-3 text-base leading-relaxed">Convert the duration of a personal goal, a long-term project or a warranty into days. For legal agreements, loan interest or official deadlines, check whether the relevant rules count both endpoints or use a special day-count convention. This is an elapsed-calendar-days tool, not a business-days calculator.</p>
  <h2 class="text-xl font-semibold mt-6">Frequently asked questions</h2>
  <details class="mt-3"><summary class="font-semibold cursor-pointer">How many days are in 4 years?</summary><p class="mt-2">Often 1,461, but a four-year period can have 1,460 days if no leap day falls in the interval. Select the start date for an exact result.</p></details>
  <details class="mt-3"><summary class="font-semibold cursor-pointer">Does a year always have 365 days?</summary><p class="mt-2">No. A leap year has 366 days. The Gregorian leap-year rule also excludes century years not divisible by 400.</p></details>
  <details class="mt-3"><summary class="font-semibold cursor-pointer">Are my dates uploaded?</summary><p class="mt-2">The calculation runs in your browser. This calculator does not send your entered dates to a server or save them in browser storage.</p></details>
  <nav aria-label="Related calculators" class="mt-6">
    <a class="underline text-sky-800 dark:text-sky-300" href="/date-calculator/">Date Difference Calculator</a> ·
    <a class="underline text-sky-800 dark:text-sky-300" href="/time/">Time calculators</a>
  </nav>
</section>
"""
    schema = [{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Years to Days Calculator",
        "url": "https://calculateallinone.vercel.app" + path,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any",
        "isAccessibleForFree": True
    }]
    page = head(title, description, path, schema) + shell(body, current_path=path)
    page = page.replace("</body>", '<script defer src="/assets/years-to-days.js"></script></body>')
    write(path, page)
    return (path, [])

