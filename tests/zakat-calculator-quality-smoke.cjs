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
  "z-currency", "z-nisab-method", "z-silverprice", "z-goldprice",
  "z-cash", "z-bank", "z-savings", "z-gold", "z-silver",
  "z-investments", "z-businesscash", "z-stock", "z-recv",
  "z-pension", "z-crypto", "z-property", "z-debts", "z-paid",
  "z-hawl", "zakat-result"
]) {
  assert.match(en, new RegExp('id="' + id + '"'), "English calculator missing " + id);
  assert.match(ur, new RegExp('id="' + id + '"'), "Urdu calculator missing " + id);
}
for (const term of [
  "ISO 4217", "silver Nisab", "gold Nisab", "612.36", "87.48",
  "503,529", "State Bank of Pakistan", "Hawl", "short-term liabilities",
  "personal-use", "business inventory", "recoverable receivables",
  "2.5%", "Worked example", "What this calculator does not decide"
]) {
  assert.ok(enText.toLowerCase().includes(term.toLowerCase()), "English page missing useful topic: " + term);
}
for (const term of [
  "503,529", "612.36", "87.48", "قمری سال", "پاکستان", "نصاب",
  "اثاثے", "واجب الادا", "2.5"
]) {
  assert.ok(urText.includes(term), "Urdu page missing localized topic: " + term);
}
assert.ok(enText.split(/\s+/).length >= 1000, "English Zakat guide is too thin (<1000 visible words)");
assert.ok(urText.split(/\s+/).length >= 700, "Urdu Zakat guide is too thin (<700 visible words)");
assert.match(en, /application\/ld\+json/, "English page must retain structured data");
assert.match(ur, /application\/ld\+json/, "Urdu page must retain structured data");
assert.match(en, /canonical/i, "English page must retain canonical metadata");
assert.match(ur, /canonical/i, "Urdu page must retain canonical metadata");
console.log("Zakat global calculator content and localization gates: PASS");

// Pure calculation-engine tests. These are independent of page rendering.
const { calculate, validateCurrency } = require("../static/zakat-calculator.js");
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
assert.equal(result.balanceDue, 1250);
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
assert.throws(() => calculate({ ...base, currency: "ZZZ" }), /not supported/);
assert.throws(() => calculate({ ...base, assets: { cash: Number.MAX_VALUE, bank: Number.MAX_VALUE } }), /supported range/);

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
