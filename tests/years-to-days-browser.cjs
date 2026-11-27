"use strict";

const assert = require("node:assert/strict");
const { chromium } = require("playwright");
function isExpectedGooglePreferredSourceReportOnlyNotice(text) {
  return text.startsWith('Framing \'https://news.google.com/\' violates the following report-only Content Security Policy directive: "frame-ancestors \'self\'".') &&
    text.includes("The violation has been logged, but no further action has been taken.");
}


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
        if (msg.type() === "error" && !isExpectedGooglePreferredSourceReportOnlyNotice(msg.text())) errors.push("console: " + msg.text());
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
      // Plain numeric inputs remain supported for the common query quantities.
      for (const [years, expected] of [
        ["5", /5 years = 1,826\.2125 days/],
        ["10", /10 years = 3,652\.425 days/],
        ["13", /13 years = 4,748\.1525 days/]
      ]) {
        await value.fill(years);
        await submit();
        assert.match(await result.innerText(), expected, years + " years must use the Gregorian mean");
      }
      await value.fill("0");
      await submit();
      assert.match(await result.innerText(), /0 years = 0 days/, "zero years must convert to zero days");
      await value.fill("0.5");
      await submit();
      assert.match(await result.innerText(), /0.5 years = 182\.62125 days/, "decimal years must retain the selected Gregorian mean");
      await value.fill("1000000");
      await submit();
      assert.match(await result.innerText(), /1,000,000 years = 365,242,500 days/, "maximum supported year input must remain finite and accurate");
      await value.fill("1000001");
      await submit();
      assert.match(await result.innerText(), /Enter a number from 0 to 1,000,000/, "values above the supported maximum must be rejected");
      await value.fill("80");
      await submit();
      assert.match(await result.innerText(), /80 years = 29,219\.4 days/);
      await value.fill("19");
      await submit();
      assert.match(await result.innerText(), /19 years = 6,939\.6075 days/);
      await value.fill("30");
      await submit();
      assert.match(await result.innerText(), /30 years = 10,957\.275 days/);

      await value.fill("80");
      await method.selectOption("365.25");
      await submit();
      assert.match(await result.innerText(), /80 years = 29,220 days/);

      // Reverse conversion: average months are explicitly estimates, not calendar months.
      await direction.selectOption("days-to-years");
      await method.selectOption("365.2425");
      await value.fill("0");
      await submit();
      assert.match(await result.innerText(), /0 days = 0 years/);
      await value.fill("1000000");
      await submit();
      assert.match(await result.innerText(), /1,000,000 days = 2,737\.907/);
      await value.fill("1188");
      await submit();
      assert.match(await result.innerText(), /Approximate breakdown: 3 years, 3 months and 0\.96 days/);
      assert.match(await result.innerText(), /Exact calendar months require a start date/);
      await value.fill("1009");
      await submit();
      assert.match(await result.innerText(), /Approximate breakdown: 2 years, 9 months and 4\.58 days/);

      await method.selectOption("365");
      await value.fill("1009");
      await submit();
      assert.match(await result.innerText(), /2\.76438356 years/);

      // Exact calendar mode counts real leap days and handles a February 29 anniversary.
      await direction.selectOption("years-to-days");
      await method.selectOption("calendar");
      const startDate = page.locator("#yd-start-date");
      await startDate.fill("2024-01-01");
      await value.fill("0");
      await submit();
      assert.match(await result.innerText(), /0 calendar years = 0 days/);
      await value.fill("1.5");
      await submit();
      assert.match(await result.innerText(), /Enter a whole number of years/, "exact calendar mode must reject decimal years");
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

      const propertyRuns = await page.evaluate(() => {
        const form = document.querySelector("#years-days-form");
        const direction = document.querySelector("#yd-direction");
        const method = document.querySelector("#yd-method");
        const value = document.querySelector("#yd-value");
        const startDate = document.querySelector("#yd-start-date");
        const result = document.querySelector("#yd-result");
        let seed = 20261114;
        const random = () => {
          seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5;
          return (seed >>> 0) / 4294967296;
        };
        const factors = [365, 365.25, 365.2425];
        let count = 0;
        for (let i = 0; i < 1000; i++) {
          const mode = i % 3;
          let expected;
          let match;
          if (mode === 2) {
            const year = 1900 + Math.floor(random() * 100);
            const month = 1 + Math.floor(random() * 12);
            const lastDay = new Date(Date.UTC(year, month, 0)).getUTCDate();
            const day = 1 + Math.floor(random() * lastDay);
            const years = Math.floor(random() * 20);
            const start = new Date(Date.UTC(year, month - 1, day));
            const end = new Date(start.getTime());
            end.setUTCFullYear(year + years);
            expected = Math.round((end.getTime() - start.getTime()) / 86400000);
            direction.value = "years-to-days";
            direction.dispatchEvent(new Event("change", { bubbles: true }));
            method.value = "calendar";
            method.dispatchEvent(new Event("change", { bubbles: true }));
            startDate.value = String(year).padStart(4, "0") + "-" + String(month).padStart(2, "0") + "-" + String(day).padStart(2, "0");
            value.value = String(years);
            form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
            match = result.textContent.match(/calendar years = ([\d,]+(?:\.\d+)?) days;/);
          } else {
            const factor = factors[Math.floor(random() * factors.length)];
            if (mode === 0) {
              const years = Math.round(random() * 100000000) / 100;
              direction.value = "years-to-days";
              direction.dispatchEvent(new Event("change", { bubbles: true }));
              method.value = String(factor);
              method.dispatchEvent(new Event("change", { bubbles: true }));
              value.value = String(years);
              expected = years * factor;
              form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
              match = result.textContent.match(/ years = ([\d,]+(?:\.\d+)?) days;/);
            } else {
              const days = Math.round(random() * 100000000) / 100;
              direction.value = "days-to-years";
              direction.dispatchEvent(new Event("change", { bubbles: true }));
              method.value = String(factor);
              method.dispatchEvent(new Event("change", { bubbles: true }));
              value.value = String(days);
              expected = days / factor;
              form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
              match = result.textContent.match(/ days = ([\d,]+(?:\.\d+)?) years\./);
            }
          }
          if (!match) throw new Error("Simulation " + i + " produced an unexpected result: " + result.textContent);
          const actual = Number(match[1].replace(/,/g, ""));
          const tolerance = 1e-7 * Math.max(1, Math.abs(expected));
          if (!Number.isFinite(actual) || Math.abs(actual - expected) > tolerance) {
            throw new Error("Simulation " + i + " mismatch: expected " + expected + ", got " + actual);
          }
          count++;
        }
        return count;
      });
      assert.equal(propertyRuns, 1000, "1,000 deterministic fixed-year and exact-calendar simulations must run");
      console.log("Years-to-Days property simulations PASS: " + propertyRuns + " at " + viewport.width + "px");

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
