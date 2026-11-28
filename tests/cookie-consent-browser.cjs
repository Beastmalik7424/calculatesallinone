"use strict";

const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const base = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/$/, "");

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  try {
    const page = await browser.newPage({ viewport: { width: 320, height: 568 } });
    let adRequests = 0;
    await page.route(base + "/years-to-days-calculator/**", async route => {
      const response = await route.fetch();
      const html = await response.text();
      const consentMeta =
        '<meta name="ca-adsense-client" content="ca-pub-0000000000000000">' +
        '<meta name="ca-adsense-slot" content="1234567890">' +
        '<meta name="ca-adsense-consent-ready" content="true">';
      await route.fulfill({ response, body: html.replace(/<head>/i, "<head>" + consentMeta) });
    });
    await page.route("**/adsbygoogle.js*", async route => {
      adRequests += 1;
      await route.fulfill({
        status: 200,
        contentType: "application/javascript",
        body: "window.adsbygoogle = window.adsbygoogle || []; window.__testAdsScriptLoaded = true;"
      });
    });

    await page.goto(base + "/years-to-days-calculator/", { waitUntil: "load", timeout: 30000 });
    const banner = page.locator("#ca-cookie-consent");
    await banner.waitFor({ state: "visible" });
    const calculatorActionReachable = await page.locator("#yd-submit").evaluate(action => {
      const rect = action.getBoundingClientRect();
      const hit = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
      return action === hit || action.contains(hit);
    });
    assert.equal(calculatorActionReachable, true,
      "the consent banner must not cover or intercept the Years-to-Days primary calculator action on a 320px viewport");
    assert.equal(await page.evaluate(() => localStorage.getItem("cookie_consent")), null,
      "unset consent must show the banner");
    assert.ok(await page.evaluate(() => parseFloat(document.body.style.paddingBottom) > 0),
      "bottom padding must be reserved while the banner is undecided");
    assert.equal(adRequests, 0, "the advertising script must not load before a choice");

    await page.locator("#ca-cookie-reject").click();
    assert.equal(await page.evaluate(() => localStorage.getItem("cookie_consent")), "rejected");
    await banner.waitFor({ state: "hidden" });
    assert.equal(await page.evaluate(() => document.body.style.paddingBottom), "",
      "body padding must be restored after rejection");
    assert.equal(adRequests, 0, "reject must block the advertising script");

    await page.reload({ waitUntil: "load" });
    assert.equal(await page.locator("#ca-cookie-consent").count(), 0,
      "a saved rejection must keep the banner hidden after reload");
    assert.equal(adRequests, 0, "a saved rejection must continue to block ads");

    await page.evaluate(() => localStorage.removeItem("cookie_consent"));
    await page.reload({ waitUntil: "load" });
    await page.locator("#ca-cookie-consent").waitFor({ state: "visible" });
    await page.locator("#ca-cookie-accept").click();
    assert.equal(await page.evaluate(() => localStorage.getItem("cookie_consent")), "accepted");
    await page.waitForFunction(
      () => document.querySelector('script[data-ca-adsense-loaded="true"]') !== null,
      null,
      { timeout: 5000 }
    );
    await page.waitForFunction(() => window.__testAdsScriptLoaded === true, null, { timeout: 5000 });
    assert.equal(adRequests, 1, "accept must load the advertising script exactly once");
    assert.equal(await page.locator("#ca-cookie-consent").count(), 0,
      "a saved acceptance must hide the banner");

    const tasbih = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await tasbih.goto(base + "/tasbih-counter/", { waitUntil: "load", timeout: 30000 });
    const tasbihBanner = tasbih.locator("#ca-cookie-consent");
    if (await tasbihBanner.count()) await tasbih.locator("#ca-cookie-reject").click();
    const count = tasbih.locator("#t-count");
    const target = tasbih.locator("#t-target");
    const custom = tasbih.locator("#t-custom-target");
    const tap = tasbih.locator("#t-tap");
    const undo = tasbih.locator("#t-undo");
    const reset = tasbih.locator("#t-reset");
    await target.selectOption("33");
    for (let i = 0; i < 33; i++) await tap.click();
    assert.equal(await count.innerText(), "33", "33 taps must produce a count of 33");
    assert.match(await tasbih.locator("#t-progress").innerText(), /reached/i,
      "the 33-count preset must report completion");

    await undo.click();
    assert.equal(await count.innerText(), "32", "Undo must reverse one tap");
    for (let i = 0; i < 40; i++) await undo.click();
    assert.equal(await count.innerText(), "0", "Undo must floor at zero");

    await target.selectOption("custom");
    for (const invalid of ["0", "-1", "1.5", "10001", ""]) {
      await custom.fill(invalid);
      await tap.click();
      assert.equal(await count.innerText(), "0", "invalid custom target must not increment: " + invalid);
      assert.match(await tasbih.locator("#t-target-error").innerText(), /whole number from 1 to 10,000/);
    }
    await custom.fill("10000");
    await tap.click();
    assert.equal(await count.innerText(), "1", "custom target 10,000 must be accepted");

    tasbih.once("dialog", dialog => dialog.accept());
    await reset.click();
    assert.equal(await count.innerText(), "0", "Reset must clear the current count");
    await undo.click();
    assert.equal(await count.innerText(), "0", "Undo must not reverse a Reset");

    await tasbih.locator("body").click({ position: { x: 8, y: 700 } });
    await tasbih.keyboard.press("Space");
    assert.equal(await count.innerText(), "1", "Space must add exactly one count");
    await tasbih.keyboard.press("Enter");
    assert.equal(await count.innerText(), "2", "Enter must add exactly one count");
    await tap.focus();
    await tasbih.keyboard.press("Space");
    assert.equal(await count.innerText(), "3", "Space on the count button must not double-fire");
    await tasbih.keyboard.press("Enter");
    assert.equal(await count.innerText(), "4", "Enter on the count button must not double-fire");

    console.log("PASS: consent unset/accepted/rejected persistence, ad-script gating, Tasbih presets, custom targets, Undo, Reset and keyboard single-fire.");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
