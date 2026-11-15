"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") pageErrors.push(message.text());
  });

  await page.goto("http://127.0.0.1:4174/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("html").getAttribute("lang"), "en");
  for (const id of ["z-currency","z-nisab-method","z-bank","z-savings","z-investments","z-businesscash","z-pension","z-crypto","z-property","z-goldprice","z-silverprice","z-paid"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing English field " + id);
  }
  for (const id of ["z-currency","z-nisab-method","z-cash","z-bank","z-goldprice","z-debts","z-paid"]) {
    assert.ok(await page.locator('label[for="' + id + '"]').count() === 1, "Missing accessible label for " + id);
  }

  await page.locator("#z-currency").fill("USD");
  await page.locator("#z-nisab-method").selectOption("gold-87");
  await page.locator("#z-cash").fill("100000");
  await page.locator("#z-bank").fill("50000");
  await page.locator("#z-debts").fill("10000");
  await page.locator("#z-goldprice").fill("1000");
  await page.locator("#z-paid").fill("1000");
  await page.locator("#z-hawl").check();
  await page.locator('#zakat-form button[type="submit"]').click();
  const globalResult = await page.locator("#zakat-result").innerText();
  assert.match(globalResult, /2\.5 percent/i);
  assert.match(globalResult, /Assets:/i);
  assert.match(globalResult, /Eligible liabilities:/i);
  assert.match(globalResult, /Remaining balance:/i);
  assert.match(globalResult, /2,500/);

  await page.locator("#z-currency").fill("ZZZ");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /three-letter ISO currency code/i);

  await page.locator("#z-currency").fill("PKR");
  await page.locator("#z-nisab-method").selectOption("silver");
  await page.locator("#z-cash").fill("612360");
  await page.locator("#z-bank").fill("0");
  await page.locator("#z-debts").fill("0");
  await page.locator("#z-silverprice").fill("1000");
  await page.locator("#z-paid").fill("0");
  await page.locator("#z-hawl").uncheck();
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /lunar Zakat year/i);
  await page.locator("#z-hawl").check();
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /15,309/);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert.equal(overflow, false, "English page must not overflow a 375px viewport");
  await page.locator('#zakat-form button[type="submit"]').scrollIntoViewIfNeeded();
  assert.equal(await page.locator('#zakat-form button[type="submit"]').isVisible(), true);

  await page.goto("http://127.0.0.1:4174/ur/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("html").getAttribute("lang"), "ur");
  assert.equal(await page.locator("html").getAttribute("dir"), "rtl");
  for (const id of ["z-currency","z-nisab-method","z-bank","z-savings","z-investments","z-goldprice","z-silverprice","z-paid"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing Urdu field " + id);
  }
  await page.locator("#z-currency").fill("PKR");
  await page.locator("#z-cash").fill("700000");
  await page.locator("#z-silverprice").fill("1000");
  await page.locator("#z-hawl").check();
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /واجب الادا/);
  const urOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert.equal(urOverflow, false, "Urdu page must not overflow a 375px viewport");

  assert.deepEqual(pageErrors, [], "Zakat pages must have no browser console or page errors");
  await browser.close();
  console.log("Zakat browser regression: English and Urdu flows, ISO currency, Nisab methods, Hawl, labels and 375px layout passed");
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
