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
