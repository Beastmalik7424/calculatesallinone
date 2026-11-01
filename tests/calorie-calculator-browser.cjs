"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const failures = [];
  try {
    for (const viewport of [{ width: 320, height: 568 }, { width: 390, height: 844 }, { width: 1366, height: 768 }]) {
      const page = await browser.newPage({ viewport });
      const errors = [], nonGetRequests = [], measurementLeaks = [];
      page.on("pageerror", error => errors.push(error.message));
      page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
      page.on("request", request => {
        if (request.method() !== "GET") nonGetRequests.push(request.method() + " " + request.url());
        const queryKeys = Array.from(new URL(request.url()).searchParams.keys());
        const postData = request.postData() || "";
        const sensitiveKeys = /(?:^|[?&,"'])(?:age|weight|height|coefficient|activity(?:Id|Level)?|pregnancyStatus|restingKcalPerDay|maintenanceKcalPerDay|calorieResult)["']?\s*[:=]/i;
        if (queryKeys.some(key => /^(age|weight|height|coefficient|activity(?:Id|Level)?|pregnancyStatus|restingKcalPerDay|maintenanceKcalPerDay|calorieResult)$/i.test(key)) || sensitiveKeys.test(postData)) {
          measurementLeaks.push(request.method() + " " + request.url());
        }
      });
      const response = await page.goto("http://127.0.0.1:4174/calorie-calculator/", { waitUntil: "domcontentloaded" });
      assert.equal(response && response.status(), 200);
      assert.equal(await page.locator("#calorie-form").isVisible(), true);
      assert.equal(await page.locator("#calorie-form").evaluate(el => el.tagName), "FORM");
      assert.equal(await page.locator("#calorie-result").getAttribute("role"), "status");
      assert.equal(await page.locator("#calorie-error").getAttribute("role"), "alert");
      assert.equal(await page.getByLabel("Age (years)").count(), 1);
      assert.equal(await page.getByLabel("Equation coefficient").count(), 1);
      assert.equal(await page.locator("#cal-weight").count(), 1);
      const associatedWeightLabels = await page.locator("#cal-weight").evaluate(el => Array.from(el.labels || []).map(label => label.textContent.trim()));
      assert.equal(associatedWeightLabels.filter(label => label === "Weight").length, 1, "Weight input must have exactly one explicit, correctly named associated label");
      assert.equal(await page.getByLabel("Weight unit").count(), 1);

      const layout = await page.evaluate(() => {
        const rect = selector => { const el = document.querySelector(selector); if (!el) return null; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return { top: r.top, bottom: r.bottom, height: r.height, marginTop: s.marginTop, marginBottom: s.marginBottom, paddingTop: s.paddingTop, paddingBottom: s.paddingBottom, display: s.display }; };
        return { overflow: document.documentElement.scrollWidth > innerWidth + 2, buttonBottom: document.querySelector("#cal-calculate").getBoundingClientRect().bottom, viewportHeight: innerHeight, buttonTop: document.querySelector("#cal-calculate").getBoundingClientRect().top, pageHeight: document.documentElement.scrollHeight, body: rect("body"), main: rect("main"), breadcrumb: rect("main nav"), pageHeader: rect("main header"), eligibility: rect("main aside"), card: rect("main section"), form: rect("#calorie-form"), age: rect("#cal-age"), weight: rect("#cal-weight"), height: rect("#cal-height-cm"), activity: rect("#cal-activity"), eligible: rect("#cal-eligibility") };
      });
      console.log("CALORIE VIEWPORT", viewport.width, JSON.stringify(layout));
      const geometry = await page.evaluate(() => {
        const rect = selector => { const el = document.querySelector(selector); if (!el) return null; const r = el.getBoundingClientRect(); return { top:r.top, bottom:r.bottom, height:r.height, display:getComputedStyle(el).display }; };
        return { nav:rect("nav"), header:rect("header"), eligibility:rect('[role="note"]'), section:rect("#calorie-form").parentElement, form:rect("#calorie-form"), fields:Array.from(document.querySelector("#calorie-form").children).map(el=>({id:el.id,tag:el.tagName,top:el.getBoundingClientRect().top,bottom:el.getBoundingClientRect().bottom,height:el.getBoundingClientRect().height,display:getComputedStyle(el).display,grid:getComputedStyle(el).gridTemplateColumns})) };
      });
      console.log("CALORIE GEOMETRY", viewport.width, JSON.stringify(geometry));
      await page.screenshot({ path: "/tmp/calorie-calculator-" + viewport.width + ".png", fullPage: false });
      console.log("Calorie calculator first-screen geometry", viewport.width, layout);
      assert.equal(layout.overflow, false, "No horizontal overflow at " + viewport.width + "px");
      assert.ok(layout.buttonBottom <= layout.viewportHeight, "Calculate action must be visible in first viewport at " + viewport.width + "px");
      await page.locator("#cal-age").fill("30");
      await page.locator("#cal-coefficient").selectOption("male");
      await page.locator("#cal-weight").fill("70");
      await page.locator("#cal-height-cm").fill("175");
      await page.locator("#cal-activity").selectOption("sedentary");
      await page.locator("#cal-eligibility").selectOption("no");
      await page.locator("#cal-age").focus();
      await page.keyboard.press("Enter");
      assert.match(await page.locator("#calorie-result").innerText(), /1,648\.8 kcal\/day/);
      assert.match(await page.locator("#calorie-result").innerText(), /1,978\.5 kcal\/day/);
      assert.match(await page.locator("#calorie-result").innerText(), /Equation: Mifflin–St Jeor \(1990\)/);
      assert.ok(await page.locator('#calorie-result a[href="https://pubmed.ncbi.nlm.nih.gov/2305711/"]').count() >= 1, "Result must cite the Mifflin–St Jeor source");
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
      assert.equal(await page.locator("#cal-height-label").innerText(), "Height (ft / in)");
      assert.equal(await page.locator("#cal-height-label").getAttribute("for"), "cal-height-ft");
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
      await page.locator("#cal-reset").focus();
      await page.keyboard.press("Enter");
      assert.equal(await page.locator("#cal-age").inputValue(), "");
      assert.equal(await page.locator("#cal-weight").inputValue(), "");
      assert.equal(await page.locator("#cal-height-unit").inputValue(), "cm");
      assert.equal(await page.locator("#cal-height-label").innerText(), "Height (cm)");
      assert.equal(await page.locator("#cal-height-label").getAttribute("for"), "cal-height-cm");
      assert.equal(await page.locator("#calorie-result").isVisible(), false);
      assert.equal(await page.locator("#cal-age").evaluate(el => el === document.activeElement), true, "Reset should return focus to age");
      await page.waitForTimeout(100);
      assert.deepEqual(nonGetRequests, [], "Calculations must not send network requests");
      assert.deepEqual(measurementLeaks, [], "Measurements and calculated results must not appear in analytics or other request payloads");
      const privacy = await page.evaluate(() => ({ query: location.search, hash: location.hash, keys: Object.keys(localStorage).filter(key => /calorie|weight|height|age/i.test(key)), sessionKeys: Object.keys(sessionStorage).filter(key => /calorie|weight|height|age/i.test(key)), cookie: document.cookie }));
      assert.equal(privacy.query, "");
      assert.equal(privacy.hash, "");
      assert.deepEqual(privacy.keys, []);
      assert.deepEqual(privacy.sessionKeys, []);
      assert.doesNotMatch(privacy.cookie, /calorie|weight|height|age/i);
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
