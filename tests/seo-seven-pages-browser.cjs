const { chromium } = require("playwright");
const assert = require("node:assert/strict");

const base = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/$/, "");
const paths = ["/ar/", "/es/", "/fr/", "/contact/", "/discount-calculator/", "/editorial-policy/", "/health/"];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const failures = [];
  try {
    for (const path of paths) {
      const page = await browser.newPage();
      const errors = [];
      page.on("console", msg => { if (msg.type() === "error") errors.push("console: " + msg.text()); });
      page.on("pageerror", err => errors.push("pageerror: " + err.message));
      const response = await page.goto(base + path, { waitUntil: "load", timeout: 30000 });
      const status = response ? response.status() : 0;
      console.log(path + " HTTP " + status + " browser_errors=" + errors.length);
      for (const error of errors) console.log("  " + error);
      if (status !== 200) failures.push(path + ": expected HTTP 200, got " + status);
      if (errors.length) failures.push(path + ": browser console/page errors detected");
      await page.close();
    }

    // End-to-end calculator checks in a real browser, in addition to parser unit tests.
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    const calculatorErrors = [];
    page.on("console", msg => { if (msg.type() === "error") calculatorErrors.push("console: " + msg.text()); });
    page.on("pageerror", err => calculatorErrors.push("pageerror: " + err.message));
    const response = await page.goto(base + "/standard-calculator/", { waitUntil: "load", timeout: 30000 });
    assert.equal(response && response.status(), 200, "calculator page should return HTTP 200");
    const display = page.locator("#calc-display");
    const key = name => page.locator('#calc-pad button[data-key="' + name + '"]');
    await key("C").click();
    await key("2").click();
    await key("+").click();
    await key("3").click();
    await key("=").click();
    assert.equal((await display.textContent()).trim(), "5", "standard calculator should calculate 2 + 3");

    await page.locator("#calc-mode-toggle").click();
    assert.equal(await page.locator("#scientific-pad").isVisible(), true, "scientific keypad should become visible");
    const sci = name => page.locator('#scientific-pad button[data-key="' + name + '"]');
    await sci("C").click();
    await sci("sin").click();
    await sci("3").click();
    await sci("0").click();
    await sci(")").click();
    await sci("=").click();
    assert.equal((await display.textContent()).trim(), "0.5", "sin(30) should equal 0.5 in degree mode");

    await sci("C").click();
    await sci("angle-toggle").click();
    await sci("sin").click();
    await sci("pi").click();
    await sci("/").click();
    await sci("2").click();
    await sci(")").click();
    await sci("=").click();
    assert.equal((await display.textContent()).trim(), "1", "sin(pi/2) should equal 1 in radian mode");

    await sci("C").click();
    await sci("2").click();
    await sci("^").click();
    await sci("-").click();
    await sci("2").click();
    await sci("=").click();
    assert.equal((await display.textContent()).trim(), "0.25", "negative exponents should work in the browser UI");

    await sci("C").click();
    await sci("1").click();
    await sci("/").click();
    await sci("0").click();
    await sci("=").click();
    assert.match((await display.textContent()).trim(), /divide by zero/i, "division by zero should show a safe error");

    const calculator = await page.locator(".ca-calculator-engine").boundingBox();
    assert.ok(calculator, "calculator should be present in the viewport");
    assert.ok(calculator.x >= 0 && calculator.x + calculator.width <= 392, "calculator should fit a 390px mobile viewport");
    if (calculatorErrors.length) {
      calculatorErrors.forEach(error => console.log("  calculator " + error));
      failures.push("calculator: browser console/page errors detected");
    }
    console.log("/standard-calculator/ interactive browser tests passed (standard, scientific DEG/RAD, negative exponent, divide-by-zero, 390px viewport)");
    await page.close();

    // Desktop regression: homepage calculator must remain the first wide tool and the All Tools section must follow it.
    const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    const desktopErrors = [];
    desktop.on("console", msg => { if (msg.type() === "error") desktopErrors.push("console: " + msg.text()); });
    desktop.on("pageerror", err => desktopErrors.push("pageerror: " + err.message));
    const homeResponse = await desktop.goto(base + "/", { waitUntil: "domcontentloaded", timeout: 30000 });
    assert.equal(homeResponse && homeResponse.status(), 200, "homepage should return HTTP 200 on desktop");
    const stylesheetHref = await desktop.locator('link[rel="stylesheet"][href*="site.css"]').first().getAttribute("href");
    assert.ok(stylesheetHref && stylesheetHref.includes("20261023-home-layout-fix-v3"), "homepage must request the cache-busted candidate stylesheet");
    // The root-relative stylesheet URL above loads this build's generated CSS in the local test server.
    const homeCalculator = await desktop.locator(".ca-home-calculator .ca-calculator-engine").boundingBox();
    const homeTitle = await desktop.locator(".ca-home-header h1").boundingBox();
    const allTools = desktop.locator("#all-tools");
    const allToolsBox = await allTools.boundingBox();
    assert.ok(homeCalculator && homeTitle && allToolsBox, "homepage heading, calculator and All Tools section must exist");
    assert.ok(homeCalculator.y >= homeTitle.y + homeTitle.height, "homepage calculator must follow the main heading");
    assert.ok(homeCalculator.width >= 500, "homepage calculator should be wide on a 1440px desktop");
    const desktopGridColumns = await desktop.locator(".ca-home-layout").evaluate(el => getComputedStyle(el).gridTemplateColumns);
    console.log("homepage desktop geometry: calculator=" + JSON.stringify(homeCalculator) + " allTools=" + JSON.stringify(allToolsBox) + " gridColumns=" + desktopGridColumns);
    assert.equal(desktopGridColumns.trim().split(/\s+/).length, 1, "homepage must use a single desktop column so All Tools cannot sit beside the calculator");
    assert.ok(homeCalculator.y + homeCalculator.height <= allToolsBox.y, "All Tools section must follow the main calculator, not overlap it");
    assert.equal(await allTools.isVisible(), true, "All Tools section must remain visible on desktop");
    assert.ok(homeCalculator.x >= 0 && homeCalculator.x + homeCalculator.width <= 1442, "homepage calculator must fit desktop viewport");
    if (desktopErrors.length) {
      desktopErrors.forEach(error => console.log("  desktop homepage " + error));
      failures.push("desktop homepage: browser console/page errors detected");
    }
    console.log("/ homepage desktop layout passed (1440px, calculator first, All Tools below, no console/page errors)");
    await desktop.close();

    // EMI regression: the standalone page must preserve global navigation and centered layout at desktop and mobile widths.
    for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
      const emiPage = await browser.newPage({ viewport, deviceScaleFactor: 1 });
      const emiErrors = [];
      emiPage.on("console", msg => { if (msg.type() === "error") emiErrors.push("console: " + msg.text()); });
      emiPage.on("pageerror", err => emiErrors.push("pageerror: " + err.message));
      const emiResponse = await emiPage.goto(base + "/emi-calculator/", { waitUntil: "domcontentloaded", timeout: 30000 });
      assert.equal(emiResponse && emiResponse.status(), 200, "EMI page should return HTTP 200");
      const globalNav = emiPage.locator('nav.site-nav[aria-label="Main"]');
      const allToolsLink = globalNav.getByRole("link", { name: "All Tools" });
      assert.equal(await globalNav.isVisible(), true, "EMI page global navigation must remain visible");
      assert.equal(await allToolsLink.isVisible(), true, "EMI page All Tools option must remain visible");
      const emiMain = await emiPage.locator("main.emi-page-main").boundingBox();
      assert.ok(emiMain, "EMI main calculator column must exist");
      assert.ok(emiMain.width <= 961, "EMI calculator content must stay centered within the 960px desktop width cap");
      assert.ok(emiMain.x >= 0 && emiMain.x + emiMain.width <= viewport.width + 1, "EMI content must fit viewport width");
      if (viewport.width === 390) {
        assert.ok((await emiPage.evaluate(() => document.documentElement.scrollWidth)) <= 391, "EMI page must not cause horizontal viewport overflow on mobile");
      }
      if (emiErrors.length) {
        emiErrors.forEach(error => console.log("  EMI " + viewport.width + "px " + error));
        failures.push("EMI " + viewport.width + "px: browser console/page errors detected");
      }
      console.log("/emi-calculator/ layout/navigation passed (" + viewport.width + "px, All Tools visible, no console/page errors)");
      if (viewport.width === 390) {
        const allToolsNavigation = emiPage.waitForURL(url => {
          const target = new URL(url);
          return target.pathname === "/" && target.hash === "#all-tools";
        }, { waitUntil: "domcontentloaded", timeout: 10000 });
        await allToolsLink.click({ noWaitAfter: true });
        await allToolsNavigation;
        assert.equal(new URL(emiPage.url()).pathname, "/", "All Tools link must return to the homepage");
        assert.equal(new URL(emiPage.url()).hash, "#all-tools", "All Tools link must jump to the homepage tools section");
        assert.equal(await emiPage.locator("#all-tools").isVisible(), true, "All Tools anchor target must be visible after navigation");
      }
      await emiPage.close();
    }

    // All English calculator pages: first interactive control must remain near the top and the page must fit mobile/desktop viewports.
    const calculatorRoutes = [
      "/zakat-calculator/", "/bmi-calculator/", "/profit-loss-calculator/",
      "/discount-calculator/", "/age-calculator/", "/unit-converter/",
      "/standard-calculator/", "/tasbih-counter/", "/stopwatch/"
    ];
    for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
      for (const path of calculatorRoutes) {
        const toolPage = await browser.newPage({ viewport, deviceScaleFactor: 1 });
        const toolErrors = [];
        toolPage.on("console", msg => { if (msg.type() === "error") toolErrors.push("console: " + msg.text()); });
        toolPage.on("pageerror", err => toolErrors.push("pageerror: " + err.message));
        const toolResponse = await toolPage.goto(base + path, { waitUntil: "load", timeout: 30000 });
        assert.equal(toolResponse && toolResponse.status(), 200, path + " should return HTTP 200 at " + viewport.width + "px");
        const main = toolPage.locator("main").first();
        assert.equal(await main.count(), 1, path + " should have a main landmark");
        const mainBox = await main.boundingBox();
        assert.ok(mainBox && mainBox.x >= 0 && mainBox.x + mainBox.width <= viewport.width + 2,
          path + " main content must fit " + viewport.width + "px viewport");
        assert.ok((await toolPage.evaluate(() => document.documentElement.scrollWidth)) <= viewport.width + 2,
          path + " must not cause horizontal overflow at " + viewport.width + "px");
        const firstToolControl = main.locator(
          "#tasbih-app, .ca-calculator-engine, #calc-display, form, button[data-key], button[type=submit], input, select, button[type=button]"
        ).first();
        assert.ok(await firstToolControl.count(), path + " must expose an interactive calculator control");
        const controlBox = await firstToolControl.boundingBox();
        assert.ok(controlBox && controlBox.y < 1000,
          path + " calculator controls must not be pushed excessively far below the page heading at " + viewport.width + "px");
        if (toolErrors.length) {
          toolErrors.forEach(error => console.log("  " + path + " " + viewport.width + "px " + error));
          failures.push(path + " " + viewport.width + "px: browser console/page errors detected");
        }
        await toolPage.close();
      }
      console.log("All nine English calculator pages fit " + viewport.width + "px without horizontal overflow and keep controls near the top.");
    }

    // Tasbih counter: clear, readable count and touch targets, working count/undo/reset, and local persistence.
    for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
      const tasbih = await browser.newPage({ viewport, deviceScaleFactor: 1 });
      const tasbihErrors = [];
      tasbih.on("console", msg => { if (msg.type() === "error") tasbihErrors.push("console: " + msg.text()); });
      tasbih.on("pageerror", err => tasbihErrors.push("pageerror: " + err.message));
      const response = await tasbih.goto(base + "/tasbih-counter/", { waitUntil: "load", timeout: 30000 });
      assert.equal(response && response.status(), 200, "Tasbih page should return HTTP 200");
      const counter = tasbih.locator("#tasbih-app");
      const count = tasbih.locator("#t-count");
      const tap = tasbih.locator("#t-tap");
      assert.equal(await counter.isVisible(), true, "Tasbih counter UI must be visible");
      assert.equal((await count.textContent()).trim(), "0", "Tasbih count should start at zero in a clean browser context");
      const countBox = await count.boundingBox();
      const tapBox = await tap.boundingBox();
      assert.ok(countBox && countBox.height >= 140, "Tasbih count display must be large and easy to read");
      assert.ok(tapBox && tapBox.height >= 90, "Tasbih Count one button must be a generous touch target");
      assert.ok(countBox.x >= 0 && countBox.x + countBox.width <= viewport.width + 2,
        "Tasbih count display must fit " + viewport.width + "px viewport");
      await tap.click();
      assert.equal((await count.textContent()).trim(), "1", "Tasbih Count one should increment");
      await tasbih.locator("#t-undo").click();
      assert.equal((await count.textContent()).trim(), "0", "Tasbih Undo should reverse one count");
      await tap.click();
      await tasbih.reload({ waitUntil: "load" });
      assert.equal((await tasbih.locator("#t-count").textContent()).trim(), "1", "Tasbih count should persist on the device after reload");
      await tasbih.locator("#t-reset").click();
      assert.equal((await tasbih.locator("#t-count").textContent()).trim(), "0", "Tasbih Reset should clear the current count");
      assert.ok((await tasbih.evaluate(() => document.documentElement.scrollWidth)) <= viewport.width + 2,
        "Tasbih page must not cause horizontal overflow at " + viewport.width + "px");
      if (tasbihErrors.length) {
        tasbihErrors.forEach(error => console.log("  Tasbih " + viewport.width + "px " + error));
        failures.push("Tasbih " + viewport.width + "px: browser console/page errors detected");
      }
      await tasbih.close();
      console.log("Tasbih interaction and layout passed at " + viewport.width + "px.");
    }

    // EMI first-screen regression: the calculator panel should precede the long explanatory copy and breadcrumb.
    for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
      const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
      const response = await page.goto(base + "/emi-calculator/", { waitUntil: "load", timeout: 30000 });
      assert.equal(response && response.status(), 200, "EMI page should return HTTP 200");
      const heading = await page.locator("h1").boundingBox();
      const calculatorPanel = await page.locator("#calculator").boundingBox();
      const intro = await page.locator(".emi-intro").boundingBox();
      assert.ok(heading && calculatorPanel && intro, "EMI heading, calculator and relocated introduction must exist");
      assert.ok(calculatorPanel.y < intro.y, "EMI calculator must appear before the long description");
      assert.ok(calculatorPanel.y < 300, "EMI calculator should start near the top of the page at " + viewport.width + "px");
      assert.ok((await page.evaluate(() => document.documentElement.scrollWidth)) <= viewport.width + 2,
        "EMI page must not cause horizontal overflow at " + viewport.width + "px");
      await page.close();
    }
  } catch (error) {
    failures.push("interactive calculator browser test: " + (error && error.message ? error.message : String(error)));
  } finally {
    await browser.close();
  }
  if (failures.length) {
    console.error("HEADLESS BROWSER AUDIT: FAIL");
    failures.forEach(x => console.error("FAIL: " + x));
    process.exit(1);
  }
  console.log("HEADLESS BROWSER AUDIT: PASS (7 SEO URLs + calculator end-to-end, zero console/page errors)");
})().catch(err => { console.error(err); process.exit(1); });
