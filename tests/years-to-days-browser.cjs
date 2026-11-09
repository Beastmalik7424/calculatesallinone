"use strict";

const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const base = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/$/, "");
const viewports = [
  { width: 320, height: 568 },
  { width: 390, height: 844 },
  { width: 1366, height: 768 }
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  try {
    for (const viewport of viewports) {
      const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
      const errors = [];
      page.on("console", msg => {
        if (msg.type() === "error") errors.push("console: " + msg.text());
      });
      page.on("pageerror", error => errors.push("pageerror: " + error.message));

      const response = await page.goto(base + "/years-to-days-calculator/", {
        waitUntil: "load",
        timeout: 30000
      });
      assert.equal(response && response.status(), 200, "Years-to-Days page must return HTTP 200");

      const layout = await page.evaluate(() => {
        const form = document.querySelector("#years-days-form");
        const input = document.querySelector("#yd-value");
        const submit = document.querySelector("#yd-submit");
        if (!form || !input || !submit) return { missing: true };
        const formBox = form.getBoundingClientRect();
        const inputBox = input.getBoundingClientRect();
        const submitBox = submit.getBoundingClientRect();
        return {
          missing: false,
          horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 2,
          formFits: formBox.width <= window.innerWidth + 2,
          inputFits: inputBox.width <= window.innerWidth + 2,
          submitFits: submitBox.width <= window.innerWidth + 2,
          inputVisible: inputBox.width > 0 && inputBox.height > 0,
          submitVisible: submitBox.width > 0 && submitBox.height > 0
        };
      });
      assert.equal(layout.missing, false, "Years-to-Days controls must exist");
      assert.equal(layout.horizontalOverflow, false, "Page must not overflow horizontally at " + viewport.width + "px");
      assert.equal(layout.formFits, true, "Calculator form must fit the viewport at " + viewport.width + "px");
      assert.equal(layout.inputFits, true, "Value input must fit the viewport at " + viewport.width + "px");
      assert.equal(layout.submitFits, true, "Submit button must fit the viewport at " + viewport.width + "px");
      assert.equal(layout.inputVisible, true, "Value input must be visible");
      assert.equal(layout.submitVisible, true, "Submit button must be visible");

      const form = page.locator("#years-days-form");
      const direction = page.locator("#yd-direction");
      const method = page.locator("#yd-method");
      const value = page.locator("#yd-value");
      const result = page.locator("#yd-result");
      const submit = () => form.locator('button[type="submit"]').click();

      // Forward conversion: Gregorian average and fixed Julian year.
      await direction.selectOption("years-to-days");
      await method.selectOption("365.2425");
      await value.fill("80");
      await submit();
      assert.match(await result.innerText(), /80 years = 29,219\.4 days/);

      await method.selectOption("365.25");
      await submit();
      assert.match(await result.innerText(), /80 years = 29,220 days/);

      // Reverse conversion: average months are explicitly estimates, not calendar months.
      await direction.selectOption("days-to-years");
      await method.selectOption("365.2425");
      await value.fill("1188");
      await submit();
      assert.match(await result.innerText(), /Approximate breakdown: 3 years, 3 months and 0\.96 days/);
      assert.match(await result.innerText(), /Exact calendar months require a start date/);

      await method.selectOption("365");
      await value.fill("1009");
      await submit();
      assert.match(await result.innerText(), /2\.76438356 years/);

      // Exact calendar mode counts real leap days and handles a February 29 anniversary.
      await direction.selectOption("years-to-days");
      await method.selectOption("calendar");
      const startDate = page.locator("#yd-start-date");
      await startDate.fill("2024-01-01");
      await value.fill("4");
      await submit();
      assert.match(await result.innerText(), /1,461 days/);
      assert.match(await result.innerText(), /Leap days included: 1/);

      await startDate.fill("2024-02-29");
      await value.fill("1");
      await submit();
      assert.match(await result.innerText(), /366 days/);
      assert.match(await result.innerText(), /End \(exclusive\): 2025-03-01/);

      // Reverse mode must disable exact calendar mode rather than silently treating it as fixed days.
      await direction.selectOption("days-to-years");
      assert.equal(await page.locator("#yd-calendar-option").isDisabled(), true);
      assert.equal(await page.locator("#yd-exact-fields").isHidden(), true);
      await value.fill("-1");
      await method.selectOption("365.2425");
      await submit();
      assert.match(await result.innerText(), /Enter a number of days from 0 to 1,000,000/);

      if (errors.length) {
        throw new Error("Browser errors at " + viewport.width + "px: " + errors.join("; "));
      }
      console.log("Years-to-Days browser PASS at " + viewport.width + "px");
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exit(1);
});
