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
      const response = await page.goto(base + path, { waitUntil: "networkidle", timeout: 30000 });
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
    const response = await page.goto(base + "/standard-calculator/", { waitUntil: "networkidle", timeout: 30000 });
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
