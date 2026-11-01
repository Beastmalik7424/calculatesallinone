"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const failures = [];
  try {
    for (const viewport of [{ width: 320, height: 568 }, { width: 390, height: 844 }, { width: 1366, height: 768 }]) {
      const page = await browser.newPage({ viewport });
      const errors = [], nonGetRequests = [];
      page.on("pageerror", error => errors.push(error.message));
      page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
      page.on("request", request => { if (request.method() !== "GET") nonGetRequests.push(request.method() + " " + request.url()); });
      const response = await page.goto("http://127.0.0.1:4174/calorie-calculator/", { waitUntil: "domcontentloaded" });
      assert.equal(response && response.status(), 200);
      assert.equal(await page.locator("#calorie-form").isVisible(), true);
      const layout = await page.evaluate(() => ({ overflow: document.documentElement.scrollWidth > innerWidth + 2, buttonBottom: document.querySelector("#cal-calculate").getBoundingClientRect().bottom, viewportHeight: innerHeight }));
      assert.equal(layout.overflow, false, "No horizontal overflow at " + viewport.width + "px");
      assert.ok(layout.buttonBottom <= layout.viewportHeight, "Calculate action must be visible in first viewport at " + viewport.width + "px");
      await page.locator("#cal-age").fill("30");
      await page.locator("#cal-coefficient").selectOption("male");
      await page.locator("#cal-weight").fill("70");
      await page.locator("#cal-height-cm").fill("175");
      await page.locator("#cal-activity").selectOption("sedentary");
      await page.locator("#cal-eligibility").selectOption("no");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-result").innerText(), /1,648\.8 kcal\/day/);
      assert.match(await page.locator("#calorie-result").innerText(), /1,978\.5 kcal\/day/);
      assert.match(await page.locator("#calorie-result").innerText(), /Equation: Mifflin–St Jeor \\(1990\\)/);
      assert.equal(await page.locator('#calorie-result a[href="https://pubmed.ncbi.nlm.nih.gov/2305711/"]').count(), 1);
      await page.locator("#cal-coefficient").selectOption("female");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-result").innerText(), /1,482\.8 kcal\/day/);
      assert.match(await page.locator("#calorie-result").innerText(), /1,779\.3 kcal\/day/);
      await page.locator("#cal-coefficient").selectOption("male");
      await page.locator("#cal-activity").selectOption("moderate");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-result").innerText(), /2,555\.6 kcal\/day/);
      await page.locator("#cal-height-unit").selectOption("ft-in");
      assert.equal(await page.locator("#cal-height-imperial").isVisible(), true);
      await page.locator("#cal-height-ft").fill("5");
      await page.locator("#cal-height-in").fill("8.89763779527559");
      await page.locator("#cal-weight-unit").selectOption("lb");
      await page.locator("#cal-weight").fill("154.323583529414");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-result").innerText(), /1,648\.8 kcal\/day/);
      await page.locator("#cal-eligibility").selectOption("pregnant");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-error").innerText(), /not intended for pregnancy or breastfeeding/i);
      assert.equal(await page.locator("#calorie-result").isVisible(), false);
      await page.locator("#cal-eligibility").selectOption("no");
      await page.locator("#cal-age").fill("17");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-error").innerText(), /18 or older/i);
      await page.locator("#cal-reset").click();
      assert.equal(await page.locator("#cal-age").inputValue(), "");
      assert.equal(await page.locator("#cal-weight").inputValue(), "");
      assert.equal(await page.locator("#cal-height-unit").inputValue(), "cm");
      assert.equal(await page.locator("#calorie-result").isVisible(), false);
      await page.waitForTimeout(100);
      assert.deepEqual(nonGetRequests, [], "Calculations must not send network requests");
      const privacy = await page.evaluate(() => ({ query: location.search, hash: location.hash, keys: Object.keys(localStorage).filter(key => /calorie|weight|height|age/i.test(key)) }));
      assert.equal(privacy.query, "");
      assert.equal(privacy.hash, "");
      assert.deepEqual(privacy.keys, []);
      assert.deepEqual(errors, [], "No browser console or page errors at " + viewport.width + "px");
      console.log("Calorie calculator browser checks PASS at " + viewport.width + "x" + viewport.height);
      await page.close();
    }
  } catch (error) {
    failures.push(error.stack || error.message);
  } finally { await browser.close(); }
  if (failures.length) { failures.forEach(message => console.error(message)); process.exitCode = 1; }
  else console.log("Adult calorie calculator browser, privacy and responsive checks: PASS");
})();
