"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const failures = [];
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on("pageerror", error => errors.push(error.message));
    page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
    const response = await page.goto("http://127.0.0.1:8123/query-calculator/", { waitUntil: "domcontentloaded" });
    assert.equal(response && response.status(), 200);
    const input = page.locator("#qt-question");
    const result = page.locator("#qt-result");
    assert.equal(await input.count(), 1);
    assert.equal(await result.count(), 1);

    const inputCases = [
      // Full Search Console-style questions must bind the unit after the
      // quantity as the source, even when the target unit appears earlier.
      ["How many days are in 5 years?", /5 years ≈ 1,826\.21 days/i],
      ["How many days in 5 years?", /5 years ≈ 1,826\.21 days/i],
      ["How many days is 5 years?", /5 years ≈ 1,826\.21 days/i],
      ["5 years is how many days?", /5 years ≈ 1,826\.21 days/i],
      ["Convert 5 years into days.", /5 years ≈ 1,826\.21 days/i],
      ["How many days are in ten years?", /10 years ≈ 3,652\.43 days/i],
      ["How many days are in thirteen years?", /13 years ≈ 4,748\.15 days/i],
      ["How many days is five years?", /5 years ≈ 1,826\.21 days/i],
      ["How many days are in 5 and a half years?", /5\.5 years ≈ 2,008\.83 days/i],
      ["How many years are in 2,555 days?", /2,555 days ≈ 6\.995 years/i],
      ["How many hours are in 3 weeks?", /3 weeks = 504 hours/i],
      ["How many years are in 2,555 days?", /2,555 days ≈ 6\.995 years/i],
      ["How many days are in 6 years and 10 months?", /6 years and 10 months ≈ 2,495\.82 days/i],
      ["How many days is 4 years and 2 months?", /4 years and 2 months ≈ 1,521\.84 days/i],
      ["1 125 days to years", /1,125 days ≈ 3\.08 years/i],
      ["36 500 days in years", /36,500 days ≈ 99\.93 years/i],
      ["How many years are in 14 thousand days?", /14,000 days ≈ 38\.3307 years/i],
      ["How many years are in 21k days?", /21,000 days ≈ 57\.496 years/i],
      ["How many years are in 1.3k days?", /1,300 days ≈ 3\.5593 years/i],
      ["Hoeveel jaar is 10000 dagen?", /10,000 days ≈ 27\.3791 years/i],
      ["80 saal me kitne din hote hai", /80 years ≈ 29,219\.4 days/i],
      ["How many days in 3.5 years?", /3\.5 years ≈ 1,278\.35 days/i],
      ["How many days is five years?", /5 years ≈ 1,826\.21 days/i],
      ["How many days are in two years?", /2 years ≈ 730\.49 days/i],
      ["How many days is 8 and a half years?", /8\.5 years ≈ 3,104\.56 days/i],
      ["80 years to days", /80 years ≈ 29,219\.4 days/i],
      ["1 year in hours", /1 year = 8,765\.82 hours.*mean Gregorian year of 365\.2425 days/i],
      ["34 years in days months and weeks", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["thirty four years in days months and weeks", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 months in days and weeks", /34 months = 1,034\.85 days.*147\.84 weeks/i],
      ["34 saal mn kitne din mahine aur haftay", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 سال میں کتنے دن مہینے اور ہفتے", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 साल में कितने दिन महीने और सप्ताह", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 años en días meses y semanas", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 ans en jours mois et semaines", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 سنوات بالأيام والأشهر والأسابيع", /34 years = 12,418\.25 days.*408 months.*1,774\.04 weeks/i],
      ["34 mn kitnay days months and weeks", /Which unit does 34 refer to/i]
    ];
    for (const [question, expected] of inputCases) {
      await input.fill(question);
      await input.press("Enter");
      await page.waitForFunction(() => document.querySelector("#qt-result").textContent.trim().length > 0);
      const actual = await result.innerText();
      assert.match(actual, expected, question + " => " + actual);
    }

    const localeCases = [
      ["en", /years = .*days.*months.*weeks/i],
      ["ur", /سال کے برابر .*دن.*مہینے.*ہفتے/],
      ["ar", /سنوات تساوي .*أيام.*أشهر.*أسابيع/],
      ["hi", /वर्ष = .*दिन.*महीने.*सप्ताह/],
      ["es", /años = .*días.*meses.*semanas/i],
      ["fr", /ans = .*jours.*mois.*semaines/i]
    ];
    for (const [locale, expected] of localeCases) {
      await page.evaluate(code => { document.documentElement.lang = code; }, locale);
      await input.fill("34 years in days months and weeks");
      await input.press("Enter");
      const actual = await result.innerText();
      assert.match(actual, expected, locale + " => " + actual);
    }
    assert.deepEqual(errors, [], "Query Calculator must not emit browser console or page errors");
    console.log("Query Calculator real-browser multi-unit, multilingual input and localized output checks: PASS");
    await page.close();
  } catch (error) {
    failures.push(error.stack || error.message);
  } finally {
    await browser.close();
  }
  if (failures.length) {
    failures.forEach(message => console.error(message));
    process.exitCode = 1;
  }
})();
