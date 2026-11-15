"use strict";
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  try {
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  const pageErrors = [];
  page.on("pageerror", error => pageErrors.push(error.message));
  page.on("console", message => {
    if (message.type() === "error") pageErrors.push(message.text());
  });

  await page.goto("http://127.0.0.1:4174/zakat-calculator/", { waitUntil: "networkidle" });
  assert.equal(await page.locator("html").getAttribute("lang"), "en");
  for (const id of ["z-currency","z-sect","z-sunni-school","z-marja","z-nisab-method","z-bank","z-savings","z-investments","z-businesscash","z-pension","z-crypto","z-property","z-goldprice","z-silverprice","z-paid"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing English field " + id);
  }
  for (const id of ["z-currency","z-sect","z-sunni-school","z-marja","z-nisab-method","z-cash","z-bank","z-goldprice","z-debts","z-paid"]) {
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
  assert.equal(await page.locator("#z-sunni-school-wrap").isVisible(), true);
  assert.equal(await page.locator("#z-marja-wrap").isVisible(), false);
  await page.locator("#z-sect").selectOption("shia");
  assert.equal(await page.locator("#z-sunni-school-wrap").isVisible(), false);
  assert.equal(await page.locator("#z-marja-wrap").isVisible(), true);
  await page.locator('#zakat-form button[type="submit"]').click();
  const sistaniResult = await page.locator("#zakat-result").innerText();
  assert.match(sistaniResult, /Ayatollah Sistani/i);
  assert.match(sistaniResult, /paper banknotes/i);
  assert.doesNotMatch(sistaniResult, /Remaining balance:/i);
  await page.locator("#z-sect").selectOption("sunni");
  await page.locator("#z-sunni-school").selectOption("maliki");
  await page.locator('#zakat-form button[type="submit"]').click();
  assert.match(await page.locator("#zakat-result").innerText(), /2,500/);
  assert.match(await page.locator("#zakat-result").innerText(), /Selected Sunni madhhab: Maliki/);
  assert.match(await page.locator("#zakat-result").innerText(), /Confirm disputed jewellery, debt, investment, pension and Hawl rulings/);

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

  for (const id of ["u-sect","u-school","u-marja","u-hanafi-position","u-crop","u-quantity","u-value","u-currency","u-irrigation","u-eligible","u-mixed-confirm"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing Ushr field " + id);
  }
  await page.locator("#u-sect").selectOption("sunni");
  await page.locator("#u-school").selectOption("shafii");
  await page.locator("#u-crop").selectOption("wheat");
  await page.locator("#u-quantity").fill("700");
  await page.locator("#u-value").fill("100000");
  await page.locator("#u-irrigation").selectOption("rain");
  await page.locator("#u-eligible").check();
  await page.locator('#ushr-form button[type="submit"]').click();
  assert.match(await page.locator("#ushr-result").innerText(), /10,000/);
  assert.match(await page.locator("#ushr-result").innerText(), /70 kg/);
  await page.locator("#u-crop").selectOption("rice");
  await page.locator('#ushr-form button[type="submit"]').click();
  const riceReviewEn = await page.locator("#ushr-result").innerText();
  assert.match(riceReviewEn, /five-wasq threshold is a volume measure/i);
  assert.doesNotMatch(riceReviewEn, /Estimated Ushr:/i);
  await page.locator("#u-crop").selectOption("wheat");
  await page.locator("#u-school").selectOption("hanafi");
  await page.locator("#u-hanafi-position").selectOption("abu-hanifa");
  await page.locator("#u-quantity").fill("100");
  await page.locator("#u-value").fill("50000");
  await page.locator("#u-irrigation").selectOption("cost");
  await page.locator('#ushr-form button[type="submit"]').click();
  assert.match(await page.locator("#ushr-result").innerText(), /2,500/);
  await page.locator("#u-quantity").fill("0");
  await page.locator('#ushr-form button[type="submit"]').click();
  const noHarvestEn = await page.locator("#ushr-result").innerText();
  assert.match(noHarvestEn, /No harvested produce was entered/i);
  assert.doesNotMatch(noHarvestEn, /2,500|null%|Estimated Ushr:/i);
  await page.locator("#u-quantity").fill("100");
  await page.locator("#u-irrigation").selectOption("mixed");
  await page.locator('#ushr-form button[type="submit"]').click();
  assert.match(await page.locator("#ushr-result").innerText(), /mixed irrigation/i);
  await page.locator("#u-mixed-confirm").check();
  await page.locator('#ushr-form button[type="submit"]').click();
  assert.match(await page.locator("#ushr-result").innerText(), /3,750/);
  await page.locator("#u-sect").selectOption("shia");
  assert.equal(await page.locator("#u-marja-wrap").isVisible(), true);
  await page.locator("#u-crop").selectOption("wheat");
  await page.locator("#u-quantity").fill("900");
  await page.locator("#u-value").fill("100000");
  await page.locator("#u-irrigation").selectOption("mixed");
  await page.locator('#ushr-form button[type="submit"]').click();
  assert.match(await page.locator("#ushr-result").innerText(), /7,500/);
  await page.locator("#u-crop").selectOption("maize");
  await page.locator('#ushr-form button[type="submit"]').click();
  assert.match(await page.locator("#ushr-result").innerText(), /four specified crops/i);

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
  assert.match(await page.locator("#zakat-result").innerText(), /منتخب سنی فقہی مسلک: حنفی/);
  for (const id of ["u-sect","u-school","u-marja","u-hanafi-position","u-crop","u-quantity","u-value","u-currency","u-irrigation","u-eligible","u-mixed-confirm"]) {
    assert.equal(await page.locator("#" + id).count(), 1, "Missing Urdu Ushr field " + id);
  }
  await page.locator("#u-sect").selectOption("shia");
  await page.locator("#u-crop").selectOption("raisins");
  await page.locator("#u-quantity").fill("900");
  await page.locator("#u-value").fill("100000");
  await page.locator("#u-irrigation").selectOption("rain");
  await page.locator('#ushr-form button[type="submit"]').click();
  const urUshrResult = await page.locator("#ushr-result").innerText();
  assert.match(urUshrResult, /عشر کا تخمینہ/);
  assert.match(urUshrResult, /(?:90|۹۰) کلوگرام/);
  assert.match(urUshrResult, /کشمش/);
  assert.doesNotMatch(urUshrResult, /Sistani's|Estimated Ushr|Crop:/i, "Urdu Ushr result must not leak English guidance");
  assert.match(urUshrResult, /(?:10|۱۰)/);
  await page.locator("#u-quantity").fill("0");
  await page.locator('#ushr-form button[type="submit"]').click();
  const noHarvestUr = await page.locator("#ushr-result").innerText();
  assert.match(noHarvestUr, /مثبت مقدار درج کریں/);
  assert.doesNotMatch(noHarvestUr, /عشر کا تخمینہ/);
  await page.locator("#u-sect").selectOption("sunni");
  await page.locator("#u-school").selectOption("shafii");
  await page.locator("#u-crop").selectOption("rice");
  await page.locator("#u-quantity").fill("700");
  await page.locator("#u-value").fill("100000");
  await page.locator("#u-irrigation").selectOption("rain");
  await page.locator("#u-eligible").check();
  await page.locator("#ushr-form button[type=\"submit\"]").click();
  const riceReviewUr = await page.locator("#ushr-result").innerText();
  assert.match(riceReviewUr, /پانچ وسق حجم کی پیمائش ہے/);
  assert.doesNotMatch(riceReviewUr, /عشر کا تخمینہ/);
  const urOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert.equal(urOverflow, false, "Urdu page must not overflow a 375px viewport");

  assert.deepEqual(pageErrors, [], "Zakat pages must have no browser console or page errors");
  console.log("Zakat browser regression: English and Urdu flows, ISO currency, Nisab methods, Hawl, crop-specific Nisab safeguards, labels and 375px layout passed");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
