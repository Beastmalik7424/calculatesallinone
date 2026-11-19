"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const BASE_URL = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/$/, "");
let browser;

(async () => {
  browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  // Compare the actual inner calculator bounds, not only the shared outer card.
  const layoutPage = await browser.newPage({ viewport: { width: 1366, height: 900 } });
  for (const viewport of [
    { width: 320, height: 740 },
    { width: 390, height: 844 },
    { width: 768, height: 1024 },
    { width: 1366, height: 900 }
  ]) {
    await layoutPage.setViewportSize(viewport);
    const standardResponse = await layoutPage.goto(BASE_URL + "/standard-calculator/", { waitUntil: "load" });
    assert.equal(standardResponse && standardResponse.status(), 200, "Standard Calculator reference must load");
    const standardBounds = await layoutPage.locator("#calc-pad").evaluate(el => {
      const wrapper = el.parentElement;
      const r = wrapper.getBoundingClientRect();
      return { x: r.x, width: r.width };
    });
    const zakatResponse = await layoutPage.goto(BASE_URL + "/zakat-calculator/", { waitUntil: "load" });
    assert.equal(zakatResponse && zakatResponse.status(), 200, "Zakat Calculator must load for inner-layout comparison");
    const zakatBounds = await layoutPage.locator("#zakat-form").evaluate(el => {
      const r = el.getBoundingClientRect();
      return { x: r.x, width: r.width };
    });
    assert.ok(Math.abs(zakatBounds.width - standardBounds.width) <= 2,
      "Zakat form width must match Standard Calculator at " + viewport.width +
      "px (standard=" + standardBounds.width + ", zakat=" + zakatBounds.width + ")");
    assert.ok(Math.abs(zakatBounds.x - standardBounds.x) <= 2,
      "Zakat form must share Standard Calculator's horizontal position at " + viewport.width + "px");
  }
    const zakatFormStyle = await layoutPage.locator("#zakat-form").evaluate(el => {
      const r = el.getBoundingClientRect();
      const shell = document.querySelector("#tool-calculator").getBoundingClientRect();
      const submit = getComputedStyle(document.querySelector("#zakat-submit"));
      return {
        formWidth: r.width,
        shellInnerWidth: shell.width - parseFloat(getComputedStyle(document.querySelector("#tool-calculator")).paddingLeft) - parseFloat(getComputedStyle(document.querySelector("#tool-calculator")).paddingRight),
        submitBackground: submit.backgroundColor,
        introCard: [...el.querySelectorAll("h2")].some(h => h.textContent.trim() === "One-page Zakat calculator")
      };
    });
    assert.equal(zakatFormStyle.introCard, false,
      "Zakat must not show a separate introductory card inside the calculator shell");
    assert.equal(zakatFormStyle.submitBackground, "rgb(15, 118, 110)",
      "Zakat primary action must use the Standard Calculator teal action color");
  await layoutPage.close();

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
  assert.equal(await page.locator("#zakat-submit").isVisible(), true, "Calculate action must be visible in the form");
  assert.equal(await page.locator("#zakat-form button:visible, #zakat-form input:visible, #zakat-form select:visible").first().getAttribute("id"), "z-currency",
    "The first visible form control must be the currency input, not an introductory hero button");
  assert.ok(await page.locator("#zakat-submit").evaluate(el => {
    const method = document.querySelector("#z-school-of-thought");
    return !!method && !!(method.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING);
  }), "The first-screen Calculate Zakat action must follow the currency and school selectors");
  assert.ok(await page.locator("#zakat-submit-bottom").evaluate(el => {
    const lastRequiredPrice = document.querySelector("#z-goldprice");
    return !!lastRequiredPrice && !!(lastRequiredPrice.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING);
  }), "The final Calculate Zakat action must follow all asset, liability, method and metal-price fields");
  assert.equal(await page.locator("#z-stock").getAttribute("autocomplete"), "off",
    "Financial trade-stock values must not be browser-autofilled");
  const englishAmountInputs = page.locator("#zakat-form input[type=number]");
  assert.ok(await englishAmountInputs.count() >= 10, "Expected all English Zakat amount inputs");
  for (const input of await englishAmountInputs.all()) {
    assert.equal(await input.getAttribute("autocomplete"), "off",
      "Every English Zakat amount input must disable browser autofill: " + await input.getAttribute("id"));
  }
  const shortcutNav = page.locator("header .ca-calculator-carousel");
  assert.equal(await shortcutNav.locator('[data-tool-set="duplicate"]').count(), 1,
    "Zakat pages must render one aria-hidden duplicate for the continuous ticker");
  assert.match(await shortcutNav.locator(".ca-calculator-track").evaluate(el => getComputedStyle(el).animationName), /ca-calculator-marquee/,
    "Zakat calculator shortcuts must move continuously like the shared ticker");
  assert.equal(await shortcutNav.locator('[data-tool-set="primary"] [data-tool-shortcut]').count(), 17,
    "All 17 calculator destinations must remain available in the primary shortcut group");
  assert.equal(await shortcutNav.locator('[data-tool-set="duplicate"] [data-tool-shortcut]').count(), 17,
    "The visual ticker duplicate must contain all 17 destinations");
  // Freeze the marquee at its initial frame so this visibility assertion is deterministic.
  await shortcutNav.locator(".ca-calculator-track").evaluate(el => {
    for (const animation of el.getAnimations()) { animation.pause(); animation.currentTime = 0; }
  });
  assert.ok(await shortcutNav.locator('[data-tool-set="primary"] [data-tool-shortcut][aria-current="page"]').evaluate(el => {
    const item = el.getBoundingClientRect();
    const nav = el.closest(".ca-calculator-carousel").getBoundingClientRect();
    return item.height >= 44 && item.left >= nav.left && item.right <= nav.right;
  }), "Active calculator shortcut must be visible in the ticker's initial frame and have a 44px touch target");
  assert.equal(await shortcutNav.locator('[data-tool-shortcut]').first().getAttribute("aria-current"), "page",
    "Current calculator shortcut must be first for immediate discoverability");
  assert.equal(await page.locator("#zakat-result").isVisible(), true,
    "The result panel must be visible on first paint");
  const advancedDetails = page.locator("#zakat-form details").first();
  assert.equal(await advancedDetails.evaluate(el => el.open), false,
    "All secondary Zakat inputs must start inside a closed details section");
  await advancedDetails.locator("summary").click();
  assert.equal(await advancedDetails.evaluate(el => el.open), true,
    "Secondary Zakat inputs must expand with one click");

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

  // Personal coin path: only reveal optional coin fields after the user confirms
  // minted gold/silver coins are prevalently used as money in transactions.
  assert.equal(await page.locator("#z-jafari-coin-inputs").isVisible(), false,
    "Sistani personal-coin inputs must remain hidden until the currency-use condition is selected");
  await page.locator("#z-jafari-trade-value").fill("0");
  await page.locator("#z-jafari-coins-used-as-money").check();
  assert.equal(await page.locator("#z-jafari-coin-inputs").isVisible(), true,
    "Qualifying personal-coin inputs must appear after explicit confirmation");
  await page.locator("#z-jafari-coins-access").check();
  await page.locator("#z-jafari-gold-coins-hawl").check();
  await page.locator("#z-jafari-gold-coins-weight").fill("69.11");
  await page.locator("#zakat-submit").click();
  const belowNisabCoinResult = await page.locator("#zakat-result").innerText();
  assert.match(belowNisabCoinResult, /Business-goods Nisab reference: Not applicable/i,
    "Coin-only below-Nisab result must not display a zero business-goods threshold");

  await page.locator("#z-jafari-gold-coins-weight").fill("69.12");
  await page.locator("#z-jafari-coins-access").check();
  await page.locator("#z-jafari-gold-coins-hawl").check();
  await page.locator("#zakat-submit").click();
  assert.match(await page.locator("#zakat-result").innerText(), /172\.8/,
    "Sistani personal gold coins must calculate 2.5% of the first gold Nisab when all separate conditions are met");

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
    if (viewport.width <= 600) {
      const setupColumns = await page.locator('#zakat-form [data-zakat-step="setup"] .grid').evaluate(el => getComputedStyle(el).gridTemplateColumns.split(' ').length);
      assert.equal(setupColumns, 1, "Zakat setup selectors must stack to full width on narrow screens");
    }
    assert.ok(metrics.controls.every(control => control.height >= 44), "Every visible Zakat input, select and button must retain a 44px minimum touch target at " + viewport.width + "px");
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
    "Recoverable receivables",
    "Property held for resale (only if bought for resale)",
    "Sayyid Sistani only. This estimates qualifying trading goods under obligatory precaution.",
    "Owner remained adult and sane throughout the year",
    "One full year has passed since the intention to profit began"
  ]) {
    assert.equal(urduFormText.includes(untranslated), false,
      "Urdu Zakat form must not show untranslated English text: " + untranslated);
  }
  assert.match(urduFormText, /قابلِ وصول رقوم/,
    "Urdu receivables heading must be translated");
  assert.match(urduFormText, /دوبارہ فروخت کے لیے رکھی گئی جائیداد/,
    "Urdu resale-property field must be translated");
  assert.equal(await page.locator("#zakat-form").evaluate(el => getComputedStyle(el).direction), "rtl",
    "Urdu form controls and grids must inherit right-to-left direction");
  assert.equal(await page.locator("#z-currency").evaluate(el => getComputedStyle(el).direction), "ltr",
    "Currency code must remain left-to-right inside the Urdu form");
  for (const input of await urAmountInputs.all()) {
    assert.equal(await input.evaluate(el => getComputedStyle(el).direction), "ltr",
      "Numeric financial values must remain left-to-right inside the Urdu form: " + await input.getAttribute("id"));
  }
  assert.equal(await page.locator("#z-school-of-thought").evaluate(el => getComputedStyle(el).direction), "rtl",
    "Method selector must retain RTL direction");

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

  // Urdu Sistani coin-only below-Nisab result must not display a zero business-goods threshold.
  await page.locator("#z-school-of-thought").selectOption("jafari-sistani");
  await page.locator("#z-jafari-coins-used-as-money").check();
  await page.locator("#z-jafari-silver-coins-weight").fill("483.83");
  await page.locator("#z-jafari-coins-access").check();
  await page.locator("#z-jafari-silver-coins-hawl").check();
  await page.locator("#z-silverprice").fill("100");
  await page.locator("#zakat-submit").click();
  const urduBelowCoinResult = await page.locator("#zakat-result").innerText();
  assert.match(urduBelowCoinResult, /لاگو نہیں/,
    "Urdu coin-only below-Nisab result must not display a zero business-goods threshold");


  // The Zakat calculator shell must match the dedicated Standard Calculator,
  // not merely keep its own controls visible. Compare rendered browser geometry
  // and computed shell styles at real viewports, without scrolling either page.
  for (const localePath of ["/zakat-calculator/", "/ur/zakat-calculator/"]) {
    for (const viewport of [
      { width: 320, height: 568 },
      { width: 360, height: 740 },
      { width: 390, height: 844 },
      { width: 1366, height: 768 }
    ]) {
      await page.setViewportSize(viewport);
      await page.goto(BASE_URL + "/standard-calculator/", { waitUntil: "networkidle" });
      const standardShell = await page.locator("#tool-calculator").evaluate(el => {
        const r = el.getBoundingClientRect();
        const h = document.querySelector("#main > h1").getBoundingClientRect();
        const s = getComputedStyle(el);
        return {
          left: r.left, width: r.width, topGap: r.top - h.bottom,
          paddingTop: s.paddingTop, paddingRight: s.paddingRight,
          paddingBottom: s.paddingBottom, paddingLeft: s.paddingLeft,
          borderRadius: s.borderRadius, borderTopWidth: s.borderTopWidth,
          backgroundColor: s.backgroundColor, boxShadow: s.boxShadow,
          marginTop: s.marginTop,
          breadcrumbDisplay: (() => { const nav = document.querySelector("#main > nav"); return nav ? getComputedStyle(nav).display : "absent"; })()
        };
      });
      await page.goto(BASE_URL + localePath, { waitUntil: "networkidle" });
      const zakatShell = await page.locator("#tool-calculator").evaluate(el => {
        const r = el.getBoundingClientRect();
        const h = document.querySelector("#main > h1").getBoundingClientRect();
        const s = getComputedStyle(el);
        return {
          left: r.left, width: r.width, topGap: r.top - h.bottom,
          paddingTop: s.paddingTop, paddingRight: s.paddingRight,
          paddingBottom: s.paddingBottom, paddingLeft: s.paddingLeft,
          borderRadius: s.borderRadius, borderTopWidth: s.borderTopWidth,
          backgroundColor: s.backgroundColor, boxShadow: s.boxShadow,
          marginTop: s.marginTop,
          breadcrumbDisplay: (() => { const nav = document.querySelector("#main > nav"); return nav ? getComputedStyle(nav).display : "absent"; })()
        };
      });
      assert.ok(Math.abs(zakatShell.left - standardShell.left) <= 2,
        localePath + " calculator must align horizontally with Standard Calculator at " + viewport.width + "px: " + JSON.stringify({ standardShell, zakatShell }));
      assert.ok(Math.abs(zakatShell.width - standardShell.width) <= 2,
        localePath + " calculator must have the same width as Standard Calculator at " + viewport.width + "px: " + JSON.stringify({ standardShell, zakatShell }));
      for (const key of ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "borderRadius", "borderTopWidth", "backgroundColor", "boxShadow", "marginTop", "breadcrumbDisplay"]) {
        assert.equal(zakatShell[key], standardShell[key],
          localePath + " shell " + key + " must match Standard Calculator at " + viewport.width + "px: " + JSON.stringify({ standardShell, zakatShell }));
      }
      assert.ok(Math.abs(zakatShell.topGap - standardShell.topGap) <= 2,
        localePath + " calculator vertical placement must match Standard Calculator at " + viewport.width + "px: " + JSON.stringify({ standardShell, zakatShell }));
    }
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
