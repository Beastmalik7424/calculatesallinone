"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  try {
    for (const viewport of [{ width: 320, height: 640 }, { width: 390, height: 844 }, { width: 1366, height: 768 }]) {
      const page = await browser.newPage({ viewport });
      const errors = [], nonGetRequests = [], measurementLeaks = [];
      page.on("pageerror", error => errors.push(error.message));
      page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
      page.on("request", request => {
        if (request.method() !== "GET") nonGetRequests.push(request.method() + " " + request.url());
        const url = new URL(request.url());
        if ([...url.searchParams.keys()].some(key => /^(age|weight|height|bodyFatPercent|calories)$/i.test(key))) measurementLeaks.push(request.url());
      });
      const response = await page.goto("http://127.0.0.1:4174/calorie-calculator/", { waitUntil: "domcontentloaded" });
      assert.equal(response && response.status(), 200);
      assert.equal(await page.locator("#calorie-form").isVisible(), true);
      assert.equal(await page.locator("#cal-formula").inputValue(), "mifflin");
      assert.equal(await page.locator("#cal-body-fat-field").isVisible(), false, "Body-fat input must be hidden unless Katch–McArdle is selected");
      assert.equal(await page.locator("#cal-height-imperial").isVisible(), false, "Imperial height controls must stay hidden while metric units are selected");
      const helperWidthRatio = await page.evaluate(() => {
        const form = document.querySelector("#calorie-form");
        const help = document.querySelector("#cal-coefficient-help");
        return help.getBoundingClientRect().width / form.getBoundingClientRect().width;
      });
      assert.ok(helperWidthRatio >= 0.9, "Coefficient guidance must span the full form width on narrow screens");
      assert.equal(await page.locator("#calorie-result").isVisible(), false);
      assert.equal(await page.locator("#calorie-error").getAttribute("role"), "alert");
      assert.equal(await page.locator("#calorie-result").getAttribute("role"), "status");
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 2), false, "No horizontal overflow at " + viewport.width + "px");
      for (const id of ["cal-age", "cal-coefficient", "cal-weight", "cal-height", "cal-activity", "cal-formula"]) {
        assert.equal(await page.locator('label[for="' + id + '"]').count(), 1, "Visible label required for " + id);
      }
      await page.locator("#cal-age").fill("30");
      await page.locator("#cal-coefficient").selectOption("male");
      await page.locator("#cal-weight").fill("70");
      await page.locator("#cal-height").fill("175");
      await page.locator("#cal-activity").selectOption("sedentary");
      await page.locator("#cal-calculate").click();
      const result = await page.locator("#calorie-result").innerText();
      assert.match(result, /1,978\.5 kcal\/day/);
      assert.match(result, /1,648\.8 kcal\/day/);
      assert.match(result, /1,678\.5 kcal\/day/);
      assert.match(result, /1,478\.5 kcal\/day/);
      assert.match(result, /2,228\.5 kcal\/day/);
      assert.match(result, /Maintenance macro split/i);
      assert.equal(await page.locator("#calorie-error").innerText(), "");
      await page.locator("#cal-formula").selectOption("harris-benedict");
      assert.equal(await page.locator("#cal-body-fat-field").isVisible(), false);
      assert.equal(await page.locator("#calorie-result").isVisible(), false, "Changing inputs must clear stale results");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-result").innerText(), /Revised Harris–Benedict/);
      await page.locator("#cal-formula").selectOption("katch-mcardle");
      assert.equal(await page.locator("#cal-body-fat-field").isVisible(), true);
      assert.equal(await page.locator("#cal-body-fat").isEnabled(), true);
      await page.locator("#cal-body-fat").fill("20");
      await page.locator("#cal-calculate").click();
      assert.match(await page.locator("#calorie-result").innerText(), /Katch–McArdle/);
      await page.locator("#cal-formula").selectOption("mifflin");
      assert.equal(await page.locator("#cal-body-fat-field").isVisible(), false);
      assert.equal(await page.locator("#cal-body-fat").isDisabled(), true);
      await page.locator("#cal-reset").click();
      assert.equal(await page.locator("#calorie-result").isVisible(), false);
      assert.equal(await page.locator("#cal-age").inputValue(), "");
      assert.deepEqual(errors, [], "No browser JavaScript or console errors at " + viewport.width + "px");
      assert.deepEqual(nonGetRequests, [], "Calculator must not send non-GET requests");
      assert.deepEqual(measurementLeaks, [], "Calculator measurements must not appear in request URLs");
      await page.close();
    }
    console.log("Calorie calculator mobile/desktop browser, formula-switching, results and privacy checks: PASS");
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
