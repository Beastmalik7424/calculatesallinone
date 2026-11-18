"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const BASE_URL = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/$/, "");
let browser;

(async () => {
  browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const pageErrors = [];
  const consoleErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  const response = await page.goto(BASE_URL + "/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(response && response.status(), 200, "English Zakat page must return HTTP 200");
  assert.equal(await page.locator("#zakat-form").count(), 1, "Single Zakat form must be present");
  assert.equal(await page.locator("#zakat-next, #zakat-back, #zakat-step-progress").count(), 0,
    "Single-page calculator must not expose Next/Back wizard controls or step progress");
  assert.equal(await page.locator("#zakat-submit").isVisible(), true, "Calculate action must be visible at the top of the form");
  assert.equal(await page.locator("#z-stock").getAttribute("autocomplete"), "off",
    "Financial trade-stock values must not be browser-autofilled");
  const englishAmountInputs = page.locator("#zakat-form input[type=number]");
  assert.ok(await englishAmountInputs.count() >= 10, "Expected all English Zakat amount inputs");
  for (const input of await englishAmountInputs.all()) {
    assert.equal(await input.getAttribute("autocomplete"), "off",
      "Every English Zakat amount input must disable browser autofill: " + await input.getAttribute("id"));
  }
  const shortcutNav = page.locator("header .ca-calculator-carousel");
  assert.equal(await shortcutNav.locator('[data-tool-set="duplicate"]').count(), 0,
    "Zakat pages must not duplicate moving calculator shortcuts");
  assert.equal(await shortcutNav.locator('[data-tool-shortcut]').count(), 17,
    "All calculator destinations must remain available in the shortcut navigation");
  assert.ok(await shortcutNav.locator('[data-tool-shortcut][aria-current="page"]').evaluate(el => {
    const item = el.getBoundingClientRect();
    const nav = el.closest(".ca-calculator-carousel").getBoundingClientRect();
    return item.height >= 44 && item.left >= nav.left && item.right <= nav.right;
  }), "Active calculator shortcut must be visible and have a 44px touch target");
  assert.equal(await shortcutNav.locator('[data-tool-shortcut]').first().getAttribute("aria-current"), "page",
    "Current calculator shortcut must be first for immediate discoverability");

  for (const id of ["z-currency","z-school-of-thought","z-nisab-method","z-metal-price-unit","z-silverprice","z-goldprice",
    "z-cash","z-bank","z-savings","z-gold","z-silver","z-jewellery","z-businesscash","z-stock","z-recv","z-property","z-debts","z-paid","z-hawl"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing supported Hanafi field " + id);
    assert.equal(await page.locator("#" + id).isVisible(), true, "All Hanafi inputs must be accessible on the same page: " + id);
  }
  for (const id of ["z-investments","z-pension","z-crypto"]) {
    assert.equal(await page.locator("#" + id).count(), 0, "Unverified asset must not be offered: " + id);
  }

  // Hanafi independent expected-value case: PKR 100,000 net wealth, silver at PKR 100/g.
  await page.locator("#z-cash").fill("100000");
  await page.locator("#z-silverprice").fill("100");
  await page.locator("#z-hawl").check();
  await page.locator("#zakat-submit").click();
  const hanafiResult = await page.locator("#zakat-result").innerText();
  assert.match(hanafiResult, /2,500/, "Hanafi calculation must independently return PKR 2,500");

  // Sistani business-goods path: only trade goods count, ordinary Hanafi cash fields are hidden.
  await page.locator("#z-school-of-thought").selectOption("jafari-sistani");
  assert.equal(await page.locator("#z-jafari-fields").isVisible(), true, "Sistani section must become visible");
  assert.equal(await page.locator("#z-sunni-asset-fields").isVisible(), false, "Hanafi personal-wealth fields must be hidden for Sistani");
  assert.equal(await page.locator("#z-jafari-trade-value").isVisible(), true, "Sistani trade-goods value must be visible without wizard navigation");
  await page.locator("#z-jafari-trade-value").fill("1000000");
  await page.locator("#z-goldprice").fill("100");
  for (const id of ["z-jafari-owner","z-jafari-acquired","z-jafari-hawl","z-jafari-intent","z-jafari-access","z-jafari-market"]) {
    await page.locator("#" + id).check();
  }
  await page.locator("#zakat-submit").click();
  const sistaniResult = await page.locator("#zakat-result").innerText();
  assert.match(sistaniResult, /25,000/, "Sistani business-goods calculation must return PKR 25,000 when all six conditions and Nisab are met");

  // Each required Sistani condition must gate the result.
  await page.locator("#z-jafari-market").uncheck();
  await page.locator("#zakat-submit").click();
  assert.match(await page.locator("#zakat-result").innerText(), /condition|شرائط/i,
    "Sistani result must not be payable when a required condition is false");

  // Responsive geometry: no horizontal overflow and accessible control heights.
  for (const viewport of [{ width: 320, height: 740 }, { width: 390, height: 844 }, { width: 768, height: 1024 }, { width: 1440, height: 900 }]) {
    await page.setViewportSize(viewport);
    const metrics = await page.evaluate(() => ({
      width: innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      formWidth: document.querySelector("#zakat-form").getBoundingClientRect().width,
      controls: [...document.querySelectorAll("#zakat-form input:not([type=checkbox]), #zakat-form select, #zakat-form button")].filter(el => !el.closest("[hidden]")).map(el => ({
        id: el.id,
        height: el.getBoundingClientRect().height
      }))
    }));
    assert.equal(metrics.documentWidth, metrics.width, "No horizontal overflow at " + viewport.width + "px");
    assert.ok(metrics.formWidth > 0 && metrics.formWidth <= metrics.width, "Form must fit viewport width at " + viewport.width + "px");
    assert.ok(metrics.controls.every(control => control.height >= 40), "Inputs/buttons must retain usable height at " + viewport.width + "px");
  }

  // Urdu page must preserve RTL and the same no-wizard behaviour.
  const ur = await page.goto(BASE_URL + "/ur/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(ur && ur.status(), 200, "Urdu Zakat page must return HTTP 200");
  assert.equal(await page.locator("html").getAttribute("lang"), "ur");
  assert.equal(await page.locator("html").getAttribute("dir"), "rtl");
  assert.equal(await page.locator("#zakat-next, #zakat-back, #zakat-step-progress").count(), 0,
    "Urdu calculator must not expose wizard navigation");
  assert.equal(await page.locator("#zakat-submit").isVisible(), true);

  const urAmountInputs = page.locator("#zakat-form input[type=number]");
  assert.ok(await urAmountInputs.count() >= 10, "Expected all Urdu Zakat amount inputs");
  for (const input of await urAmountInputs.all()) {
    assert.equal(await input.getAttribute("autocomplete"), "off",
      "Every Urdu Zakat amount input must disable browser autofill: " + await input.getAttribute("id"));
  }

  // Urdu must be a complete localized experience, not an English form inside an RTL page.
  const urduFormText = await page.locator("#zakat-form").innerText();
  for (const untranslated of [
    "One-page Zakat calculator",
    "Choose your method, enter only applicable amounts, then calculate.",
    "Recoverable receivables",
    "Property held for resale (only if bought for resale)",
    "Sayyid Sistani only. This estimates qualifying trading goods under obligatory precaution.",
    "Owner remained adult and sane throughout the year",
    "One full year has passed since the intention to profit began"
  ]) {
    assert.equal(urduFormText.includes(untranslated), false,
      "Urdu Zakat form must not show untranslated English text: " + untranslated);
  }
  assert.match(urduFormText, /ایک صفحے کا زکوٰۃ کیلکولیٹر/,
    "Urdu form heading must be translated");
  assert.match(urduFormText, /قابلِ وصول رقوم/,
    "Urdu receivables heading must be translated");
  assert.match(urduFormText, /دوبارہ فروخت کے لیے رکھی گئی جائیداد/,
    "Urdu resale-property field must be translated");
  assert.equal(await page.locator("#zakat-form").evaluate(el => getComputedStyle(el).direction), "rtl",
    "Urdu form controls and grids must inherit right-to-left direction");

  for (const viewport of [{ width: 320, height: 740 }, { width: 360, height: 800 }, { width: 390, height: 844 }, { width: 768, height: 1024 }, { width: 1366, height: 900 }]) {
    await page.setViewportSize(viewport);
    const metrics = await page.evaluate(() => ({
      width: innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      mainWidth: document.querySelector("#main").getBoundingClientRect().width,
      formWidth: document.querySelector("#zakat-form").getBoundingClientRect().width,
      formDirection: getComputedStyle(document.querySelector("#zakat-form")).direction
    }));
    assert.equal(metrics.documentWidth, metrics.width, "Urdu RTL page must not overflow horizontally at " + viewport.width + "px");
    assert.ok(metrics.mainWidth > 0 && metrics.mainWidth <= metrics.width, "Urdu page container must fit viewport at " + viewport.width + "px");
    assert.ok(metrics.formWidth > 0 && metrics.formWidth <= metrics.mainWidth, "Urdu calculator must fit its page container at " + viewport.width + "px");
    assert.equal(metrics.formDirection, "rtl", "Urdu form must remain RTL at " + viewport.width + "px");
  }

  assert.deepEqual(pageErrors, [], "Zakat browser page must not produce uncaught JavaScript errors");
  assert.deepEqual(consoleErrors, [], "Zakat browser page must not produce console errors");
  console.log("Zakat browser: PASS (single-page Hanafi and Sistani flows, both locales, 4 responsive widths, no console errors)");
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
}).finally(async () => {
  if (browser) await browser.close();
});
