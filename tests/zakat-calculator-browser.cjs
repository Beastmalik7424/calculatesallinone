"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const BASE_URL = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/+$/, "");

const FIELD_STEP = {
  "z-currency":"setup","z-school-of-thought":"setup","z-nisab-method":"nisab","z-jafari-nisab-method":"nisab",
  "z-metal-price-unit":"price-unit","z-silverprice":"metal-prices","z-goldprice":"metal-prices",
  "z-cash":"sunni-assets-a","z-bank":"sunni-assets-a","z-savings":"sunni-assets-a",
  "z-gold":"sunni-assets-b","z-silver":"sunni-assets-b","z-jewellery":"sunni-assets-b",
  "z-investments":"sunni-assets-c","z-businesscash":"sunni-assets-c","z-stock":"sunni-assets-c",
  "z-recv":"sunni-assets-d","z-pension":"sunni-assets-d",
  "z-crypto":"sunni-assets-e","z-property":"sunni-assets-e",
  "z-debts":"sunni-liabilities","z-paid":"sunni-liabilities","z-hawl":"sunni-liabilities",
  "z-jafari-trade-value":"jafari-trade","z-jafari-owner":"jafari-trade","z-jafari-acquired":"jafari-trade",
  "z-jafari-hawl":"jafari-hawl-intent","z-jafari-intent":"jafari-hawl-intent",
  "z-jafari-access":"jafari-conditions","z-jafari-market":"jafari-conditions"
};
async function goToStep(page, key) {
  const form = page.locator("#zakat-form");
  const order = (await form.getAttribute("data-step-order") || "").split(",").filter(Boolean);
  let current = await form.getAttribute("data-current-step");
  let index = order.indexOf(current);
  const target = order.indexOf(key);
  assert.ok(index >= 0 && target >= 0, "Unknown Zakat step " + key + " in " + order.join(","));
  while (index < target) {
    await page.locator("#zakat-next").click({ scroll: "none" });
    index += 1;
  }
  while (index > target) {
    await page.locator("#zakat-back").click({ scroll: "none" });
    index -= 1;
  }
  assert.equal(await form.getAttribute("data-current-step"), key);
  assert.equal(await page.evaluate(() => window.scrollY), 0, "Zakat step navigation must not scroll the page");
}
async function setField(page, id, action, value) {
  const key = FIELD_STEP[id];
  assert.ok(key, "Missing step mapping for " + id);
  await goToStep(page, key);
  const control = page.locator("#" + id);
  if (action === "fill") await control.fill(value);
  else if (action === "select") await control.selectOption(value);
  else if (action === "check") await control.check();
  else if (action === "uncheck") await control.uncheck();
  else throw new Error("Unknown field action " + action);
}
async function submitZakat(page) {
  const form = page.locator("#zakat-form");
  const order = (await form.getAttribute("data-step-order")).split(",");
  await goToStep(page, order[order.length - 1]);
  await page.locator("#zakat-submit").click({ scroll: "none" });
  assert.equal(await page.evaluate(() => window.scrollY), 0, "Submitting Zakat must not scroll the page");
}


let browser;
(async () => {
  browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  const pageErrors = [];
  await page.addInitScript(() => {
    Object.defineProperty(navigator, "share", { value: async () => {}, configurable: true });
  });
  page.on("pageerror", error => pageErrors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") pageErrors.push(message.text());
  });

  await page.goto(BASE_URL + "/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("html").getAttribute("lang"), "en");
  assert.equal(await page.locator("#zakat-next").count(), 1, "Mobile Zakat flow must provide an in-place Next control");
  assert.equal(await page.locator("#zakat-back").count(), 1, "Mobile Zakat flow must provide an in-place Back control");
  assert.equal(await page.locator("#zakat-step-progress").count(), 1, "Zakat flow must expose accessible step progress");
  assert.equal(await page.locator("#zakat-submit").count(), 1, "Zakat calculation submit must remain available in the final step");
  const ticker = page.locator("header .ca-calculator-carousel");
  assert.equal(await ticker.count(), 1, "Zakat page must retain the shared calculator ticker");
  assert.equal(await ticker.locator('[data-tool-set="primary"] a').count(), 17, "Primary ticker must expose all 17 calculator destinations");
  assert.equal(await ticker.locator('[data-tool-set="duplicate"]').count(), 0, "Zakat must retain the same single-group structure as other inner calculator pages");
  const tickerMotion = await ticker.locator(".ca-calculator-track").evaluate(el => {
    const style = getComputedStyle(el);
    return { name: style.animationName, duration: style.animationDuration, iteration: style.animationIterationCount };
  });
  assert.deepEqual(tickerMotion, { name: "ca-calculator-marquee", duration: "48s", iteration: "infinite" }, "Zakat must use the same ticker motion as other calculator pages");
  assert.equal(await page.locator("#zakat-result").isVisible(), false, "An empty result panel must not occupy space before the first calculation");
  for (const viewport of [{ width: 390, height: 844 }, { width: 1440, height: 900 }]) {
    await page.setViewportSize(viewport);
    const layout = await page.evaluate(() => ({
      width: innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      navVisible: (() => { const r=document.querySelector("header .ca-calculator-carousel").getBoundingClientRect(); return r.width>0 && r.height>=40; })(),
      mainVisible: (() => { const r=document.querySelector("#main").getBoundingClientRect(); return r.width>0 && r.right<=innerWidth+1; })()
    }));
    assert.equal(layout.documentWidth, layout.width, "Zakat page must not horizontally overflow at " + viewport.width + "px: " + JSON.stringify(layout));
    assert.equal(layout.navVisible, true, "Ticker must remain visible at " + viewport.width + "px");
    assert.equal(layout.mainVisible, true, "Calculator content must fit the viewport width at " + viewport.width + "px");
  }
  await page.setViewportSize({ width: 375, height: 812 });
  assert.ok(await page.locator("#zakat-form .zakat-step-panel:not([hidden])").count() >= 1, "Initial Zakat step panels must be active");
  const initialWizard = await page.evaluate(() => {
    const panels = [...document.querySelectorAll("#zakat-form .zakat-step-panel:not([hidden])")];
    const next = document.querySelector("#zakat-next");
    const rect = e => { const r=e.getBoundingClientRect(); return {top:r.top,bottom:r.bottom,height:r.height}; };
    const controls = panels.flatMap(panel=>[...panel.querySelectorAll('input:not([type="checkbox"]):not([type="hidden"]),select,textarea')]).filter(e=>getComputedStyle(e).display!=="none"&&getComputedStyle(e).visibility!=="hidden");
    return {scrollY, panels:panels.map(rect), next:next?rect(next):null, controls:controls.map(rect), viewport:innerHeight};
  });
  assert.equal(initialWizard.scrollY, 0, "Zakat wizard must start without page scrolling");
  assert.ok(initialWizard.panels.length>=1 && initialWizard.panels.every(r=>r.top>=0&&r.bottom<=initialWizard.viewport), "Initial Zakat step must fit the viewport: "+JSON.stringify(initialWizard));
  assert.ok(initialWizard.next && initialWizard.next.top>=0 && initialWizard.next.bottom<=initialWizard.viewport, "Next control must be reachable without scrolling");
  assert.ok(initialWizard.controls.length>0 && initialWizard.controls.every(r=>r.top>=0&&r.bottom<=initialWizard.viewport), "All initial-step fields must fit without scrolling");
  // Every Sunni/Hanafi input must be visible and enabled when its wizard step is active.
  for (const [id, step] of Object.entries(FIELD_STEP).filter(([id]) => !id.startsWith("z-jafari"))) {
    await goToStep(page, step);
    const control = page.locator("#" + id);
    assert.equal(await control.isVisible(), true, "Active Hanafi input must be visible: " + id);
    assert.equal(await control.isEnabled(), true, "Active Hanafi input must be enabled: " + id);
  }
  await goToStep(page, "setup");
  for (const id of ["z-currency","z-school-of-thought","z-nisab-method","z-metal-price-unit","z-jafari-nisab-method","z-jafari-trade-value","z-jafari-owner","z-jafari-acquired","z-jafari-hawl","z-jafari-intent","z-jafari-access","z-jafari-market","z-jewellery","z-bank","z-savings","z-investments","z-businesscash","z-pension","z-crypto","z-property","z-goldprice","z-silverprice","z-paid"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing English field " + id);
  }
  for (const id of ["z-currency","z-nisab-method","z-cash","z-bank","z-goldprice","z-debts","z-paid"]) {
    assert.ok(await page.locator('label[for="' + id + '"]').count() === 1, "Missing accessible label for " + id);
  }

  await setField(page, "z-currency", "fill", "USD");
  await setField(page, "z-nisab-method", "select", "gold-87");
  await setField(page, "z-cash", "fill", "100000");
  await setField(page, "z-bank", "fill", "50000");
  await setField(page, "z-debts", "fill", "10000");
  await setField(page, "z-goldprice", "fill", "1000");
  await setField(page, "z-paid", "fill", "1000");
  await setField(page, "z-hawl", "check");
  await submitZakat(page);
  const globalResult = await page.locator("#zakat-result").innerText();
  assert.match(globalResult, /2\.5 percent/i);
  assert.match(globalResult, /Assets:/i);
  assert.match(globalResult, /Eligible liabilities:/i);
  assert.match(globalResult, /Remaining balance:/i);
  assert.match(globalResult, /2,500/);
  const shareButton = page.locator('[data-share-result-for="zakat-result"]');
  assert.equal(await shareButton.isVisible(), true, "Share result action must appear after a successful calculation");
  assert.equal(await shareButton.isEnabled(), true, "Share result action must be enabled after a successful calculation");
  await shareButton.click();
  const shareStatus = page.locator('[data-share-result-for="zakat-result"] + span[role="status"]');
  assert.ok((await shareStatus.innerText()).trim().length > 0, "Share result button must complete its browser share action");

  await setField(page, "z-currency", "fill", "ZZZ");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /three-letter ISO currency code/i);

  await setField(page, "z-currency", "fill", "PKR");
  await setField(page, "z-nisab-method", "select", "silver");
  await setField(page, "z-cash", "fill", "612360");
  await setField(page, "z-bank", "fill", "0");
  await setField(page, "z-debts", "fill", "0");
  await setField(page, "z-silverprice", "fill", "1000");
  await setField(page, "z-paid", "fill", "0");
  await setField(page, "z-hawl", "uncheck");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /lunar Zakat year/i);
  await setField(page, "z-hawl", "check");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /15,309/);
  assert.equal(await page.locator("#z-nisab-method option").count(), 2, "Only the Hanafi silver and gold Nisab references must be available");
  await setField(page, "z-nisab-method", "select", "gold-87");
  await setField(page, "z-cash", "fill", "8748");
  await setField(page, "z-goldprice", "fill", "100");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /218\.7/);

  // The only supported Sunni method is Hanafi, including qualifying jewellery.
  await setField(page, "z-school-of-thought", "select", "sunni-hanafi");
  await setField(page, "z-metal-price-unit", "select", "gram");
  await setField(page, "z-currency", "fill", "PKR");
  await setField(page, "z-nisab-method", "select", "silver");
  await setField(page, "z-cash", "fill", "500000");
  await setField(page, "z-jewellery", "fill", "150000");
  await setField(page, "z-silverprice", "fill", "1000");
  await setField(page, "z-debts", "fill", "0");
  await setField(page, "z-paid", "fill", "0");
  await setField(page, "z-hawl", "check");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /16,250/);

  // Sindh Government standard tola price must normalize to the same gram-based Nisab result.
  assert.match(await page.locator('#z-metal-price-unit option[value="tola"]').innerText(), /Sindh Government standard tola/);
  await setField(page, "z-metal-price-unit", "select", "tola");
  await setField(page, "z-nisab-method", "select", "gold-87");
  await setField(page, "z-cash", "fill", "100000");
  await setField(page, "z-jewellery", "fill", "0");
  await setField(page, "z-goldprice", "fill", "11663.8");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /2,500/);

  // Troy-ounce price must produce the same Hanafi result as gram and tola input.
  assert.match(await page.locator('#z-metal-price-unit option[value="ounce"]').innerText(), /troy ounce/i);
  await setField(page, "z-metal-price-unit", "select", "ounce");
  await setField(page, "z-goldprice", "fill", String(1000 * 31.1034768));
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /2,500/);

  // Ja'fari is explicitly limited to Sayyid Sistani and requires all six published conditions.
  assert.equal(await page.locator("#z-school-of-thought option").count(), 2, "Only Hanafi and Ja'fari Sistani methods must be selectable");
  await setField(page, "z-school-of-thought", "select", "jafari-sistani");
  assert.equal(await page.locator("#z-sunni-fields").isVisible(), false);
  await goToStep(page, "nisab");
  assert.equal(await page.locator("#z-jafari-fields").isVisible(), true);
  assert.equal(await page.locator("#z-sunni-asset-fields").count(), 1, "Sunni-only asset and liability section must have a dedicated wrapper");
  assert.equal(await page.locator("#z-sunni-asset-fields").isVisible(), false, "Sunni assets, liabilities and Hawl must be hidden in the Sistani method");
  for (const id of ["z-cash","z-bank","z-savings","z-gold","z-silver","z-jewellery","z-investments","z-businesscash","z-stock","z-recv","z-pension","z-crypto","z-property","z-debts","z-paid","z-hawl"]) {
    assert.equal(await page.locator("#" + id).isVisible(), false, "Sunni-only field must be hidden in the Sistani method: " + id);
  }
  await setField(page, "z-metal-price-unit", "select", "gram");
  await setField(page, "z-jafari-nisab-method", "select", "gold");
  await setField(page, "z-goldprice", "fill", "1000");
  await setField(page, "z-jafari-trade-value", "fill", "1000000");
  for (const id of ["z-jafari-owner","z-jafari-acquired","z-jafari-hawl","z-jafari-intent","z-jafari-access","z-jafari-market"]) {
    await setField(page, id, "check");
  }
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /25,000/);
  await setField(page, "z-jafari-acquired", "uncheck");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /all six Sayyid Sistani/i);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert.equal(overflow, false, "English page must not overflow a 375px viewport");
  assert.equal(await page.locator("#zakat-submit").isVisible(), true);
  assert.equal(await page.evaluate(() => window.scrollY), 0);

  // Repeat the core wizard and result path at a laptop viewport.
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(BASE_URL + "/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("#z-currency").isVisible(), true, "Laptop first screen must expose the currency input");
  await page.locator("#zakat-next").click({ scroll: "none" });
  assert.equal(await page.locator("#zakat-form").getAttribute("data-current-step"), "nisab", "Laptop Next button must advance the wizard");
  assert.equal(await page.locator("#z-nisab-method").isVisible(), true, "Laptop Nisab selector must be visible and active");
  await page.locator("#zakat-back").click({ scroll: "none" });
  assert.equal(await page.locator("#zakat-form").getAttribute("data-current-step"), "setup", "Laptop Back button must return to the first step");
  await setField(page, "z-cash", "fill", "100000");
  await setField(page, "z-silverprice", "fill", "100");
  await setField(page, "z-hawl", "check");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /2,500/, "Laptop calculation must return the independently expected PKR amount");
  assert.equal(await page.locator("#zakat-submit").isVisible(), true, "Laptop Calculate button must remain visible on the final step");

  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto(BASE_URL + "/ur/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("html").getAttribute("lang"), "ur");
  assert.equal(await page.locator("html").getAttribute("dir"), "rtl");
  for (const id of ["z-currency","z-nisab-method","z-bank","z-savings","z-investments","z-goldprice","z-silverprice","z-paid"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing Urdu field " + id);
  }
  await setField(page, "z-currency", "fill", "PKR");
  await setField(page, "z-cash", "fill", "700000");
  await setField(page, "z-silverprice", "fill", "1000");
  await setField(page, "z-hawl", "check");
  await submitZakat(page);
  assert.match(await page.locator("#zakat-result").innerText(), /واجب الادا/);
  await setField(page, "z-school-of-thought", "select", "jafari-sistani");
  assert.equal(await page.locator("#z-sunni-fields").isVisible(), false, "Urdu Sunni Nisab selector must be hidden in the Sistani method");
  assert.equal(await page.locator("#z-sunni-asset-fields").isVisible(), false, "Urdu Sunni assets, liabilities and Hawl must be hidden in the Sistani method");
  for (const id of ["z-cash","z-bank","z-savings","z-gold","z-silver","z-jewellery","z-investments","z-businesscash","z-stock","z-recv","z-pension","z-crypto","z-property","z-debts","z-paid","z-hawl"]) {
    assert.equal(await page.locator("#" + id).isVisible(), false, "Urdu Sunni-only field must be hidden in the Sistani method: " + id);
  }
  await goToStep(page, "nisab");
  assert.equal(await page.locator("#z-jafari-fields").isVisible(), true, "Urdu Sistani fields must be visible on the Nisab step");
  const urOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert.equal(urOverflow, false, "Urdu page must not overflow a 375px viewport");

  for (const width of [320, 375, 390, 768, 1366]) {
    await page.setViewportSize({ width, height: 900 });
    const dimensions = await page.evaluate(() => ({
      viewport: window.innerWidth,
      document: document.documentElement.scrollWidth,
      body: document.body.scrollWidth,
      rootOverflowX: getComputedStyle(document.documentElement).overflowX
    }));
    // Fixed decorative background glows can extend the body's scrollWidth, but html clips them.
    // The document root is the actual horizontally scrollable page viewport.
    assert.ok(
      dimensions.document <= dimensions.viewport && dimensions.rootOverflowX === "clip",
      "Zakat page must not expose horizontal page scrolling at " + width + "px: " + JSON.stringify(dimensions)
    );
  }
  assert.deepEqual(pageErrors, [], "Zakat pages must have no browser console or page errors");
  await browser.close();
  console.log("Zakat browser regression: English and Urdu flows, ISO currency, Nisab methods, Hawl, labels and 375px layout passed");
})().catch(async error => {
  console.error(error);
  if (browser) await browser.close().catch(() => {});
  process.exitCode = 1;
});
