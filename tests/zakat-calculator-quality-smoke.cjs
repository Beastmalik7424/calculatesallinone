#!/usr/bin/env node
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

function page(slug) {
  const file = path.join(__dirname, "..", "public", slug, "index.html");
  assert.ok(fs.existsSync(file), "Missing generated page: " + slug);
  return fs.readFileSync(file, "utf8");
}
function visibleText(html) {
  return html.replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/&amp;/g, "&").replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'").replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">").replace(/\s+/g, " ").trim();
}
const en = page("zakat-calculator");
const ur = page("ur/zakat-calculator");
const enText = visibleText(en);
const urText = visibleText(ur);

for (const id of [
  "z-currency", "z-sect", "z-sunni-school", "z-marja", "z-nisab-method", "z-silverprice", "z-goldprice", "z-sunni-school-wrap", "z-marja-wrap", "u-currency", "u-sect", "u-school", "u-marja", "u-crop", "u-quantity", "u-value", "u-irrigation", "ushr-result",
  "z-cash", "z-bank", "z-savings", "z-gold", "z-silver",
  "z-investments", "z-businesscash", "z-stock", "z-recv",
  "z-pension", "z-crypto", "z-property", "z-debts", "z-paid",
  "z-hawl", "zakat-result"
]) {
  assert.match(en, new RegExp('id="' + id + '"'), "English calculator missing " + id);
  assert.match(ur, new RegExp('id="' + id + '"'), "Urdu calculator missing " + id);
}
for (const term of [
  "ISO 4217", "silver Nisab", "gold Nisab", "612.36", "87.48", "Ushr", "agricultural produce", "rain-fed", "irrigated", "five wasqs", "653 kg", "847 kg", "Hanafi", "Sistani",
  "503,529", "State Bank of Pakistan", "Hawl", "Sunni", "Shia", "Hanafi", "Shafi'i", "Maliki", "Hanbali", "Ja'fari", "Sistani", "short-term liabilities",
  "personal-use", "trade inventory", "receivables",
  "2.5%", "Worked example", "This tool does not decide"
]) {
  assert.ok(enText.toLowerCase().includes(term.toLowerCase()), "English page missing useful topic: " + term);
}
for (const term of [
  "503,529", "612.36", "87.48", "قمری سال", "پاکستان", "نصاب", "سنی", "شیعہ", "سیستانی", "جعفری", "عشر", "زرعی پیداوار", "بارش", "آبپاشی",
  "اثاثے", "واجب الادا", "2.5"
]) {
  assert.ok(urText.includes(term), "Urdu page missing localized topic: " + term);
}
assert.ok(enText.split(/\s+/).length >= 1000, "English Zakat guide is too thin (<1000 visible words)");
assert.ok(urText.split(/\s+/).length >= 700, "Urdu Zakat guide is too thin (<700 visible words)");
for (const term of ["Ushr is separate from annual wealth Zakat", "rain-fed", "five wasqs", "653 kg", "dry-weight", "847 kg", "948 kg", "crop eligibility", "mixed irrigation", "Pakistan Code", "Sudan Zakat Chamber", "21-karat", "Singapore MUIS", "86 g", "investment-held jewellery", "87.28 g", "87.48 g", "NZF Worldwide", "not national laws", "raisins"]) {
  assert.ok(enText.toLowerCase().includes(term.toLowerCase()), "English Ushr guidance missing: " + term);
}
for (const term of ["عشر", "زرعی پیداوار", "بارش", "آبپاشی", "پانچ وسق", "653", "847", "948", "امام ابو حنیفہ", "مخلوط آبپاشی", "سوڈان", "سنگاپور", "ملائیشیا", "کشمش", "87.28", "87.48"]) {
  assert.ok(urText.includes(term), "Urdu Ushr guidance missing: " + term);
}
assert.match(en, /href="https:\/\/www\.sistani\.org\/english\/book\/49\/2410\//, "English Ushr guidance must link to Sistani's primary ruling");
assert.match(en, /href="https:\/\/pakistancode\.gov\.pk\/pdffiles\/administratorfd19eec0a97080f151dac2a8406dea88\.pdf/, "Pakistan statutory Ushr must link to Pakistan Code");
assert.match(ur, /id="u-quantity"/, "Urdu Ushr form must expose harvest quantity");
assert.match(en, /value="raisins"/, "Sistani crop list must use the official English term raisins");
assert.doesNotMatch(en, /value="grapes"/, "Grapes must not be substituted for the official raisins crop wording");
assert.doesNotMatch(enText, /35,700,000/, "Outdated 2025 Sudanese-pound Nisab must not be presented as current");
for (const [name, html] of [["English", en], ["Urdu", ur]]) {
  const submitAt = html.indexOf('type="submit"');
  const assetAt = html.indexOf('id="z-cash"');
  assert.ok(submitAt > 0 && submitAt < assetAt, name + " Zakat submit action must precede the long asset-entry section");
  assert.match(html.slice(submitAt - 100, submitAt + 250), /sticky/, name + " Zakat submit action must remain reachable while entering assets");
}
assert.match(en, /application\/ld\+json/, "English page must retain structured data");
assert.match(ur, /application\/ld\+json/, "Urdu page must retain structured data");
assert.match(en, /canonical/i, "English page must retain canonical metadata");
assert.match(ur, /canonical/i, "Urdu page must retain canonical metadata");
console.log("Zakat global calculator content and localization gates: PASS");

// Pure calculation-engine tests. These are independent of page rendering.
const { calculate, calculateUshr, validateCurrency } = require("../static/zakat-calculator.js");
assert.equal(typeof calculateUshr, "function", "Ushr must have its own calculation engine");
const rainUshr = calculateUshr({ sect: "sunni", school: "shafii", crop: "wheat", eligibleCropConfirmed: true, quantityKg: 700, marketValue: 100000, irrigation: "rain" });
assert.equal(rainUshr.rate, 0.10);
assert.equal(rainUshr.amountDue, 10000);
const pumpUshr = calculateUshr({ sect: "sunni", school: "hanafi", crop: "rice", eligibleCropConfirmed: true, quantityKg: 100, marketValue: 50000, irrigation: "cost" });
assert.equal(pumpUshr.rate, 0.05);
assert.equal(pumpUshr.amountDue, 2500, "Hanafi Abu Hanifa position must not impose the five-wasq threshold");
const belowMajority = calculateUshr({ sect: "sunni", school: "maliki", crop: "wheat", eligibleCropConfirmed: true, quantityKg: 500, marketValue: 100000, irrigation: "rain" });
assert.equal(belowMajority.status, "below_nisab");
assert.equal(belowMajority.amountDue, 0);
const mixedUshr = calculateUshr({ sect: "sunni", school: "hanbali", crop: "wheat", eligibleCropConfirmed: true, quantityKg: 700, marketValue: 100000, irrigation: "mixed" });
assert.equal(mixedUshr.status, "scholar_review_required", "Sunni mixed irrigation must not assume a universal midpoint");
const confirmedMixedUshr = calculateUshr({ sect: "sunni", school: "hanbali", crop: "wheat", quantityKg: 700, marketValue: 100000, irrigation: "mixed", mixedRateConfirmed: true });
assert.equal(confirmedMixedUshr.rate, 0.075);
const sistaniUshr = calculateUshr({ sect: "shia", marja: "sistani", crop: "wheat", quantityKg: 900, marketValue: 100000, irrigation: "mixed" });
const sistaniRaisins = calculateUshr({ sect: "shia", marja: "sistani", crop: "raisins", quantityKg: 900, marketValue: 100000, irrigation: "rain" });
assert.equal(sistaniRaisins.status, "payable");
assert.throws(() => calculateUshr({ sect: "shia", marja: "sistani", crop: "grapes", quantityKg: 900, marketValue: 100000, irrigation: "rain" }), /four specified crops/i);
assert.equal(sistaniUshr.rate, 0.075);
assert.equal(sistaniUshr.nisabKg, 847);
assert.throws(() => calculateUshr({ sect: "shia", marja: "sistani", crop: "maize", quantityKg: 900, marketValue: 100000, irrigation: "rain" }), /four specified crops/i);
assert.throws(() => calculateUshr({ sect: "shia", marja: "other", crop: "wheat", quantityKg: 900, marketValue: 100000, irrigation: "rain" }), /verified Marja/i);
assert.throws(() => calculateUshr({ sect: "sunni", school: "unknown", crop: "wheat", quantityKg: 700, marketValue: 100000, irrigation: "rain" }), /madhhab/i);
assert.throws(() => calculateUshr({ sect: "sunni", school: "hanafi", crop: "wheat", quantityKg: -1, marketValue: 100000, irrigation: "rain" }), /non-negative/i);
assert.throws(() => calculateUshr({ sect: "sunni", school: "hanafi", crop: "wheat", quantityKg: 700, marketValue: 100000, irrigation: "unknown" }), /irrigation/i);
assert.equal(validateCurrency("pkr"), "PKR");
assert.equal(validateCurrency("usd"), "USD");
assert.throws(() => validateCurrency("PK"), /three-letter/);
assert.throws(() => validateCurrency("US1"), /three-letter/);
assert.throws(() => validateCurrency("ZZZ"), /not supported/);

const base = {
  currency: "PKR", nisabMethod: "silver", silverPricePerGram: 100,
  goldPricePerGram: 10000, hawlComplete: true, zakatPaid: 0,
  liabilities: 100, assets: { cash: 10000, bank: 20000 }
};
let result = calculate(base);
assert.equal(result.nisabThreshold, 61236);
assert.equal(result.totalAssets, 30000);
assert.equal(result.netAssets, 29900);
assert.equal(result.status, "below_nisab");
assert.equal(result.balanceDue, 0);

result = calculate({ ...base, assets: { cash: 70000 } });
assert.equal(result.status, "payable");
assert.equal(result.zakatBeforePaid, 1747.5);
assert.equal(result.balanceDue, 1747.5);
result = calculate({ ...base, assets: { cash: 61236 }, liabilities: 0 });
assert.equal(result.status, "payable", "wealth exactly equal to Nisab must qualify");
result = calculate({ ...base, assets: { cash: 70000 }, hawlComplete: false });
assert.equal(result.status, "hawl_incomplete");
assert.equal(result.zakatBeforePaid, 0);
result = calculate({ ...base, assets: { cash: 70000 }, zakatPaid: 500 });
assert.equal(result.balanceDue, 1247.5);
assert.equal(result.overpayment, 0);
result = calculate({ ...base, assets: { cash: 70000 }, zakatPaid: 2000 });
assert.equal(result.balanceDue, 0);
assert.equal(result.overpayment, 252.5);

result = calculate({ ...base, nisabMethod: "gold-87", assets: { cash: 900000 }, goldPricePerGram: 10000 });
assert.equal(result.nisabThreshold, 874800);
assert.equal(result.nisabGrams, 87.48);
result = calculate({ ...base, nisabMethod: "gold-85", assets: { cash: 900000 }, goldPricePerGram: 10000 });
assert.equal(result.nisabThreshold, 850000);
assert.equal(result.nisabGrams, 85);

for (const bad of [-1, NaN, Infinity, -Infinity, "not-a-number"]) {
  assert.throws(() => calculate({ ...base, assets: { cash: bad } }));
  assert.throws(() => calculate({ ...base, liabilities: bad }));
  assert.throws(() => calculate({ ...base, silverPricePerGram: bad }));
  assert.throws(() => calculate({ ...base, zakatPaid: bad }));
}
assert.throws(() => calculate({ ...base, nisabMethod: "unknown" }), /Nisab method/);
const sistaniResult = calculate({ ...base, sect: "shia", marja: "sistani" });
assert.equal(sistaniResult.status, "scholar_review_required", "Ja'fari/Sistani must not be run through the generic Sunni 2.5% cash calculator");
assert.equal(sistaniResult.balanceDue, null, "Unsupported Shia cases must not display a fabricated numeric amount");
assert.match(sistaniResult.guidance, /banknotes|paper money/i);
assert.throws(() => calculate({ ...base, sect: "shia", marja: "unverified" }), /verified Marja/);
assert.throws(() => calculate({ ...base, sect: "unknown" }), /sect/);
assert.throws(() => calculate({ ...base, currency: "ZZZ" }), /not supported/);
assert.throws(() => calculate({ ...base, assets: { cash: Number.MAX_VALUE, bank: Number.MAX_VALUE } }), /supported calculation range/);

// Deterministic property simulation: 2,000 varied asset/liability combinations.
let seed = 20261115;
function random() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
for (let i = 0; i < 2000; i++) {
  const assets = {};
  for (const key of ["cash","bank","savings","gold","silver","investments","businessCash","stock","receivables","pension","crypto","property"]) {
    assets[key] = Math.floor(random() * 25000000) / 100;
  }
  const liabilities = Math.floor(random() * 10000000) / 100;
  const price = 10 + random() * 500;
  const paid = Math.floor(random() * 500000) / 100;
  const r = calculate({
    currency: "PKR", nisabMethod: i % 3 === 0 ? "gold-87" : (i % 3 === 1 ? "gold-85" : "silver"),
    silverPricePerGram: price, goldPricePerGram: price * 100,
    assets, liabilities, zakatPaid: paid, hawlComplete: i % 2 === 0
  });
  assert.ok(r.totalAssets >= 0 && r.totalLiabilities >= 0 && r.netAssets >= 0);
  assert.ok(r.balanceDue >= 0 && r.overpayment >= 0);
  assert.ok(r.balanceDue <= r.zakatBeforePaid);
  assert.ok(r.zakatBeforePaid === 0 || Math.abs(r.zakatBeforePaid - r.netAssets * 0.025) < 1e-7);
}
console.log("Zakat calculation engine: 2,000 deterministic scenarios passed");
