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
  ...[truncated]