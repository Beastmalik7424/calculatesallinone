"use strict";

const assert = require("node:assert/strict");
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    const pageErrors = [];
    page.on("pageerror", error => pageErrors.push(error.message));

    const response = await page.goto("http://127.0.0.1:4174/", { waitUntil: "domcontentloaded" });
    assert.equal(response.status(), 200, "homepage must return HTTP 200");
    await page.waitForSelector(".ca-home-calculator #calc-pad button");

    const initial = await page.evaluate(() => ({
      buttonCount: document.querySelectorAll(".ca-home-calculator #calc-pad button").length,
      calculatorBeforeTools: Boolean(
        document.querySelector(".ca-home-calculator") &&
        document.querySelector(".ca-home-tools") &&
        (document.querySelector(".ca-home-calculator").compareDocumentPosition(
          document.querySelector(".ca-home-tools")
        ) & Node.DOCUMENT_POSITION_FOLLOWING)
      ),
    }));
    assert.equal(initial.buttonCount, 23, "homepage calculator must keep all 23 keypad buttons");
    assert.equal(initial.calculatorBeforeTools, true, "calculator must remain before the All Tools panel");

    let scenarios = 0;
    const failures = [];
    for (const theme of ["light", "dark"]) {
      await page.evaluate(isDark => document.documentElement.classList.toggle("dark", isDark), theme === "dark");
      for (let width = 320; width <= 1920; width += 2) {
        await page.setViewportSize({ width, height: 800 });
        const metrics = await page.evaluate(() => {
          const calculator = document.querySelector(".ca-home-calculator");
          const tools = document.querySelector(".ca-home-tools");
          const keypad = [...document.querySelectorAll(".ca-home-calculator #calc-pad button")];
          const toolLinks = [...document.querySelectorAll(".ca-home-tool-grid a")];
          const rect = element => {
            const box = element.getBoundingClientRect();
            return { left: box.left, right: box.right, width: box.width, height: box.height };
          };
          return {
            viewportWidth: window.innerWidth,
            documentWidth: document.documentElement.scrollWidth,
            calculator: rect(calculator),
            tools: rect(tools),
            keypadTargets: keypad.map(rect),
            toolTargets: toolLinks.map(rect),
            keypadCount: keypad.length,
          };
        });
        scenarios += 1;
        const invalid = metrics.documentWidth > metrics.viewportWidth + 1 ||
          metrics.calculator.width <= 0 ||
          metrics.tools.width <= 0 ||
          metrics.calculator.right > metrics.viewportWidth + 1 ||
          metrics.tools.right > metrics.viewportWidth + 1 ||
          metrics.keypadCount !== 23 ||
          metrics.keypadTargets.some(target => target.width < 44 || target.height < 44) ||
          metrics.toolTargets.some(target => target.width < 44 || target.height < 44);
        if (invalid && failures.length < 25) {
          failures.push({ theme, width, metrics });
        }
      }
    }

    assert.deepEqual(pageErrors, [], "homepage must not produce uncaught browser errors");
    assert.equal(
      failures.length,
      0,
      "responsive layout failed at one or more viewport/theme combinations: " +
      JSON.stringify(failures)
    );
    console.log(
      "PASS: " + scenarios +
      " responsive viewport/theme simulations (801 widths × light/dark), " +
      "23 calculator keypad targets and tool-link touch targets checked"
    );
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
