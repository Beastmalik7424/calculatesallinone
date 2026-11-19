"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const BASE_URL = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/+$/, "");
const VIEWPORTS = [
  { name: "phone-320", width: 320, height: 740 },
  { name: "phone-390", width: 390, height: 844 },
  { name: "tablet-768", width: 768, height: 1024 },
  { name: "desktop-1366", width: 1366, height: 900 }
];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const failures = [];
  let checks = 0;
  try {
    for (const viewport of VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height } });
      for (const route of [
        { path: "/standard-calculator/", selector: "#tool-calculator > .max-w-sm", label: "Standard Calculator" },
        { path: "/zakat-calculator/", selector: "#zakat-form", label: "Zakat Calculator" }
      ]) {
        const response = await page.goto(BASE_URL + route.path, { waitUntil: "load" });
        assert.equal(response && response.status(), 200, route.label + " must load at " + viewport.name);
        const metrics = await page.locator(route.selector).evaluate(el => {
          const r = el.getBoundingClientRect();
          const s = getComputedStyle(el);
          return { x: r.x, width: r.width, right: r.right, marginLeft: s.marginLeft, marginRight: s.marginRight };
        });
        if (route.label === "Standard Calculator") {
          page.__standardMetrics = metrics;
        } else {
          const standard = page.__standardMetrics;
          assert.ok(standard, "Standard Calculator reference geometry must be captured");
          assert.ok(Math.abs(metrics.width - standard.width) <= 2,
            "Zakat form width must match Standard Calculator width at " + viewport.name +
            " (standard=" + standard.width + ", zakat=" + metrics.width + ")");
          assert.ok(Math.abs(metrics.x - standard.x) <= 2,
            "Zakat form must be centered at the same position as Standard Calculator at " + viewport.name);
          assert.equal(await page.locator("#zakat-submit").isVisible(), true,
            "Calculate action must remain visible at " + viewport.name);
          assert.ok(await page.locator("#z-currency").count() === 1,
            "First Zakat field must remain present at " + viewport.name);
          checks += 4;
        }
      }
      await page.close();
    }
    console.log("Zakat/Standard inner-layout checks passed: " + checks + " assertions across " + VIEWPORTS.length + " viewports.");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
