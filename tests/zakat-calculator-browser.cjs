"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

let browser;
(async () => {
  browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") pageErrors.push(message.text());
  });

  await page.goto("http://127.0.0.1:4174/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("html").getAttribute("lang"), "en");
  for (const id of ["z-currency","z-school-of-thought","z-nisab-method","z-metal-price-unit","z-jafari-nisab-method","z-jafari-trade-value","z-jafari-owner","z-jafari-acquired","z-jafari-hawl","z-jafari-intent","z-jafari-access","z-jafari-market","z-jewellery","z-bank","z-savings","z-investments","z-businesscash","z-pension","z-crypto","z-property","z-goldprice","z-silverprice","z-paid"]) {
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
  assert.equal(await page.locator("#z-nisab-method option").count(), 5, "Classical, modern and cited Shafi'i Nisab weights must be available");
  await page.locator("#z-nisab-method").selectOption("gold-85");
  await page.locator("#z-cash").fill("8500");
  await page.locator("#z-goldprice").fill("100");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /212\.5/);
  await page.locator("#z-nisab-method").selectOption("silver-595");
  await page.locator("#z-cash").fill("59500");
  await page.locator("#z-silverprice").fill("100");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /1,487\.5/);
  await page.locator("#z-nisab-method").selectOption("gold-96");
  await page.locator("#z-cash").fill("9600");
  await page.locator("#z-goldprice").fill("100");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /240/);
  await page.locator("#z-nisab-method").selectOption("gold-96");
  await page.locator("#z-cash").fill("9600");
  await page.locator("#z-goldprice").fill("100");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /240/);

  // Sunni school distinction: Hanafi includes ordinary qualifying jewellery.
  await page.locator("#z-school-of-thought").selectOption("sunni-hanafi");
  await page.locator("#z-metal-price-unit").selectOption("gram");
  await page.locator("#z-currency").fill("PKR");
  await page.locator("#z-nisab-method").selectOption("silver");
  await page.locator("#z-cash").fill("500000");
  await page.locator("#z-jewellery").fill("150000");
  await page.locator("#z-silverprice").fill("1000");
  await page.locator("#z-debts").fill("0");
  await page.locator("#z-paid").fill("0");
  await page.locator("#z-hawl").check();
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /16,250/);

  // Sindh Government standard tola price must normalize to the same gram-based Nisab result.
  assert.match(await page.locator('#z-metal-price-unit option[value="tola"]').innerText(), /Sindh Government standard tola/);
  await page.locator("#z-metal-price-unit").selectOption("tola");
  await page.locator("#z-goldprice").fill("11663.8");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /2,500/);

  // Sistani path must hide the Sunni form and require all six published conditions.
  await page.locator("#z-school-of-thought").selectOption("jafari-sistani");
  assert.equal(await page.locator("#z-sunni-fields").isVisible(), false);
  assert.equal(await page.locator("#z-jafari-fields").isVisible(), true);
  assert.equal(await page.locator("#z-sunni-asset-fields").count(), 1, "Sunni-only asset and liability section must have a dedicated wrapper");
  assert.equal(await page.locator("#z-sunni-asset-fields").isVisible(), false, "Sunni assets, liabilities and Hawl must be hidden in the Sistani method");
  for (const id of ["z-cash","z-bank","z-savings","z-gold","z-silver","z-jewellery","z-investments","z-businesscash","z-stock","z-recv","z-pension","z-crypto","z-property","z-debts","z-paid","z-hawl"]) {
    assert.equal(await page.locator("#" + id).isVisible(), false, "Sunni-only field must be hidden in the Sistani method: " + id);
  }
  await page.locator("#z-metal-price-unit").selectOption("gram");
  await page.locator("#z-jafari-nisab-method").selectOption("gold");
  await page.locator("#z-goldprice").fill("1000");
  await page.locator("#z-jafari-trade-value").fill("1000000");
  for (const id of ["z-jafari-owner","z-jafari-acquired","z-jafari-hawl","z-jafari-intent","z-jafari-access","z-jafari-market"]) {
    await page.locator("#" + id).check();
  }
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /25,000/);
  await page.locator("#z-jafari-acquired").uncheck();
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /all six Sayyid Sistani/i);

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
  await page.locator("#z-school-of-thought").selectOption("jafari-sistani");
  assert.equal(await page.locator("#z-sunni-fields").isVisible(), false, "Urdu Sunni Nisab selector must be hidden in the Sistani method");
  assert.equal(await page.locator("#z-sunni-asset-fields").isVisible(), false, "Urdu Sunni assets, liabilities and Hawl must be hidden in the Sistani method");
  for (const id of ["z-cash","z-bank","z-savings","z-gold","z-silver","z-jewellery","z-investments","z-businesscash","z-stock","z-recv","z-pension","z-crypto","z-property","z-debts","z-paid","z-hawl"]) {
    assert.equal(await page.locator("#" + id).isVisible(), false, "Urdu Sunni-only field must be hidden in the Sistani method: " + id);
  }
  assert.equal(await page.locator("#z-jafari-fields").isVisible(), true, "Urdu Sistani fields must be visible");
  const urOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert.equal(urOverflow, false, "Urdu page must not overflow a 375px viewport");

  assert.deepEqual(pageErrors, [], "Zakat pages must have no browser console or page errors");
  await browser.close();
  console.log("Zakat browser regression: English and Urdu flows, ISO currency, Nisab methods, Hawl, labels and 375px layout passed");
})().catch(async error => {
  console.error(error);
  if (browser) await browser.close().catch(() => {});
  process.exitCode = 1;
});
