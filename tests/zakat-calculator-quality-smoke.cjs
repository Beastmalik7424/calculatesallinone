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
  "z-currency", "z-school-of-thought", "z-nisab-method", "z-metal-price-unit",
  "z-jafari-nisab-method", "z-jafari-trade-value", "z-jafari-owner", "z-jafari-acquired",
  "z-jafari-hawl", "z-jafari-intent", "z-jafari-access", "z-jafari-market",
  "z-silverprice", "z-goldprice", "z-cash", "z-bank", "z-savings",
  "z-gold", "z-silver", "z-jewellery", "z-investments", "z-businesscash", "z-stock", "z-recv",
  "z-pension", "z-crypto", "z-property", "z-debts", "z-paid",
  "z-hawl", "zakat-result"
]) {
  assert.match(en, new RegExp('id="' + id + '"'), "English calculator missing " + id);
  assert.match(ur, new RegExp('id="' + id + '"'), "Urdu calculator missing " + id);
}
for (const term of [
  "ISO 4217", "silver Nisab", "gold Nisab", "612.36", "87.48", 
  "503,529", "1446–1447 AH", "1447 AH (2026)", "State Bank of Pakistan", "first day of Ramazan",
  "saving, profit and loss sharing", "2.5%", "personal Zakat Nisab",
  "PKR 1,837,080", "PKR 700,000", "PKR 2,000,000", "PKR 50,000",
  "bank deduction threshold changes yearly", "Which assets to include", "Which liabilities may be deducted", "How the calculation works", "Worked example with checkable arithmetic", "Personal-use property and other exclusions", "Pakistan bank deduction threshold is separate", "Worldwide currency support, privacy and limitations", "Worked example",
  "does not fetch a live metal price", "qualified scholar", "Sources",
  "Hanafi", "Sayyid Sistani",
  "obligatory precaution", "Khums", "69.12 g", "483.84 g",
  "11.6638", "trading goods", "personal-use gold/silver jewellery",
  "ordinary banknotes", "right of disposal", "capital cost", "contract of exchange",
  
  
  "Hawl checkbox is self-reported", "does not track balances throughout the lunar year",
   "not a complete Hanafi fiqh engine",
  "Do not enter the same jewellery value in both", "Muhammad Fayyaz Adeel"
]) {
  assert.ok(enText.toLowerCase().includes(term.toLowerCase()), "English page missing approved content: " + term);
}
for (const term of [
  "503,529", "612.36", "87.48", "1446–1447", "رمضان کے پہلے دن", "پاکستان", "نصاب",
  "اثاثے", "واجبات", "2.5", "رمضان کے پہلے دن", "ہر سال بدلتی ہے",
  "سیستانی", "جعفری", "احتیاطِ واجب", "خمس", "69.12", "483.84",
  "11.6638", "حنفی", "تجارتی مال",
  "محمد فیاض عدیل", "خود تصدیق", "پورے قمری سال", "ایک ہی زیور کی قیمت", "مکمل فقہی انجن"
]) {
  assert.ok(urText.includes(term), "Urdu page missing approved localized content: " + term);
}
assert.equal((en.match(/<summary\b/gi) || []).length, 4, "English Zakat page must retain four concise page-specific FAQs");
assert.equal((ur.match(/<summary\b/gi) || []).length, 4, "Urdu Zakat page must retain four concise page-specific FAQs");
const enNisab = en.match(/<select id="z-nisab-method"[^>]*>([\s\S]*?)<\/select>/);
const urNisab = ur.match(/<select id="z-nisab-method"[^>]*>([\s\S]*?)<\/select>/);
assert.ok(enNisab && urNisab, "Both locales must expose the Nisab selector");
assert.equal((enNisab[1].match(/<option\b/g) || []).length, 2, "English UI must expose only the Hanafi gold and silver Nisab choices");
assert.equal((urNisab[1].match(/<option\b/g) || []).length, 2, "Urdu UI must expose the same two Hanafi Nisab choices");

const enSchool = en.match(/<select id="z-school-of-thought"[^>]*>([\s\S]*?)<\/select>/);
const urSchool = ur.match(/<select id="z-school-of-thought"[^>]*>([\s\S]*?)<\/select>/);
assert.ok(enSchool && urSchool, "Both locales must expose the school-of-thought selector");
assert.equal((enSchool[1].match(/<option\b/g) || []).length, 2, "English UI must expose only Hanafi and the named Ja'fari authority");
assert.equal((urSchool[1].match(/<option\b/g) || []).length, 2, "Urdu UI must expose the same two methods");
assert.match(en, /value="jafari-sistani"/, "Sistani calculation path must be explicitly named");
assert.match(en, /value="tola"/, "Sindh Government standard tola unit must be selectable");
assert.match(en, /value="ounce"/, "Troy ounce unit must be selectable");
assert.match(en, /31\.1034768 g/, "Troy ounce conversion must be visible");
assert.match(ur, /31\.1034768 گرام/, "Urdu page must explain the troy ounce conversion");
assert.match(en, /11\.6638 g/, "Sindh Government standard tola conversion must be visible");
assert.match(en, /Sindh Government standard tola/, "The 11.6638 g unit must be named as the Sindh Government standard, not a universal Pakistani market tola");
const enMetalUnits = en.match(/<select id="z-metal-price-unit"[^>]*>([\s\S]*?)<\/select>/);
const urMetalUnits = ur.match(/<select id="z-metal-price-unit"[^>]*>([\s\S]*?)<\/select>/);
assert.ok(enMetalUnits && urMetalUnits, "Both locales must expose the metal price unit selector");
assert.equal((enMetalUnits[1].match(/<option\b/g) || []).length, 3, "English UI must expose exactly gram, standard tola and troy ounce");
assert.equal((urMetalUnits[1].match(/<option\b/g) || []).length, 3, "Urdu UI must expose exactly the same three price units");
assert.match(en, /12\.5 g/, "The 12.5 g competing convention must be disclosed");
assert.match(ur, /12\.5 گرام/, "Urdu content must disclose the 12.5 g competing convention");
assert.match(en, /zakat-on-jewellery/, "English content must cite the scholar-reviewed jewellery and tola guidance");
assert.match(ur, /zakat-on-jewellery/, "Urdu content must cite the scholar-reviewed jewellery and tola guidance");
assert.match(en, /id="z-sunni-fields"/, "Sunni fields must have a separate visibility container");
for (const [name, html] of [["English", en], ["Urdu", ur]]) {
  const wrapperAt = html.indexOf('id="z-sunni-asset-fields"');
  const jafariAt = html.indexOf('id="z-jafari-fields"');
  assert.ok(wrapperAt >= 0 && jafariAt > wrapperAt, name + " Sunni assets/liabilities wrapper must precede the Ja'fari section");
  for (const id of ["z-cash","z-bank","z-savings","z-gold","z-silver","z-jewellery","z-investments","z-businesscash","z-stock","z-recv","z-pension","z-crypto","z-property","z-debts","z-paid","z-hawl"]) {
    const fieldAt = html.indexOf('id="' + id + '"');
    assert.ok(fieldAt > wrapperAt && fieldAt < jafariAt, name + " Sunni-only field must be inside its visibility wrapper: " + id);
  }
}
assert.match(en, /id="z-jafari-fields"[^>]*hidden/, "Sistani fields must be separately hidden by default");
assert.match(en, /sistani\.org\/english\/book\/48\/2323/, "English content must cite Sistani's official trading-goods ruling");
assert.match(ur, /sistani\.org\/english\/book\/48\/2323/, "Urdu content must cite Sistani's official trading-goods ruling");
assert.match(en, /sindhlaws\.gov\.pk/, "English content must cite the Sindh Government conversion table");
assert.match(ur, /sindhlaws\.gov\.pk/, "Urdu content must cite the Sindh Government conversion table");
assert.match(en, /which-debts-affect-zakat-for-both-debtor-and-creditor/, "English content must cite scholarly debt-rule guidance");
assert.match(ur, /which-debts-affect-zakat-for-both-debtor-and-creditor/, "Urdu content must cite scholarly debt-rule guidance");
assert.match(ur, /answerstofatawa\/118729/, "Urdu content must cite the Hanafi gold and silver Nisab reference");
assert.doesNotMatch(ur, /zatca\.gov\.sa|aliftaa\.jo/, "The two-option calculator must not promote unrelated Nisab conversion systems as its own methods");

assert.match(enNisab[1], /value="gold-87"/);
assert.doesNotMatch(enNisab[1], /gold-85|silver-595|gold-96/);

assert.match(urNisab[1], /value="gold-87"/);
assert.doesNotMatch(urNisab[1], /gold-85|silver-595|gold-96/);



for (const term of [
  "503,529", "612.36", "87.48", "زکوٰۃ سال", "پاکستان", "نصاب",
  "اثاثے", "واجبات", "2.5"
]) {
  assert.ok(urText.includes(term), "Urdu page missing localized topic: " + term);
}
assert.ok(enText.length > 500, "English Zakat page must contain the requested substantive guidance");
assert.ok(urText.length > 300, "Urdu Zakat page must contain the translated guidance");
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
assert.ok(!en.includes("islamweb.net/en/fatwa/81355"), "English page must not cite the unsupported Islamweb reference for Nisab");
assert.ok(!ur.includes("islamweb.net/en/fatwa/81355"), "Urdu page must not cite the unsupported Islamweb reference for Nisab");
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
assert.equal(result.balanceDue, 1247.5);
assert.equal(result.overpayment, 0);
result = calculate({ ...base, assets: { cash: 70000 }, zakatPaid: 2000 });
assert.equal(result.balanceDue, 0);
assert.equal(result.overpayment, 252.5);

result = calculate({ ...base, nisabMethod: "gold-87", assets: { cash: 900000 }, goldPricePerGram: 10000 });
assert.equal(result.nisabThreshold, 874800);
assert.equal(result.nisabGrams, 87.48);
for (const [nisabMethod, grams, priceKey] of [["gold-87", 87.48, "goldPricePerGram"], ["silver", 612.36, "silverPricePerGram"]]) {
  const result = calculate({ ...base, nisabMethod, [priceKey]: 100, assets: { cash: grams * 100 }, hawlComplete: true });
  assert.equal(result.nisabGrams, grams, nisabMethod + " must remain a supported Nisab choice");
}

for (const bad of [-1, NaN, Infinity, -Infinity, "not-a-number"]) {
  assert.throws(() => calculate({ ...base, assets: { cash: bad } }));
  assert.throws(() => calculate({ ...base, liabilities: bad }));
  assert.throws(() => calculate({ ...base, silverPricePerGram: bad }));
  assert.throws(() => calculate({ ...base, zakatPaid: bad }));
}
assert.throws(() => calculate({ ...base, nisabMethod: "unknown" }), /Nisab method/);
assert.throws(() => calculate({ ...base, metalPriceUnit: "unknown" }), /unit/i);
result = calculate({ ...base, metalPriceUnit: "ounce", silverPricePerGram: 100 * 31.1034768, assets: { cash: 70000 } });
assert.ok(Math.abs(result.metalPricePerGram - 100) < 1e-10);
assert.ok(Math.abs(result.nisabThreshold - 61236) < 1e-7);
assert.throws(() => calculate({ ...base, currency: "ZZZ" }), /not supported/);
assert.throws(() => calculate({ ...base, assets: { cash: Number.MAX_VALUE, bank: Number.MAX_VALUE } }), /supported calculation range/);

// Deterministic property simulation: 2,000 varied asset/liability combinations.
let seed = 20261115;
function random() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
for (let i = 0; i < 2000; i++) {
  const assets = {};
  for (const key of ["cash","bank","savings","gold","silver","jewellery","investments","businessCash","stock","receivables","pension","crypto","property"]) {
    assets[key] = Math.floor(random() * 25000000) / 100;
  }
  const liabilities = Math.floor(random() * 10000000) / 100;
  const price = 10 + random() * 500;
  const paid = Math.floor(random() * 500000) / 100;
  const r = calculate({
    currency: "PKR", nisabMethod: i % 2 === 0 ? "gold-87" : "silver",
    silverPricePerGram: price, goldPricePerGram: price * 100,
    assets, liabilities, zakatPaid: paid, hawlComplete: i % 2 === 0
  });
  assert.ok(r.totalAssets >= 0 && r.totalLiabilities >= 0 && r.netAssets >= 0);
  assert.ok(r.balanceDue >= 0 && r.overpayment >= 0);
  assert.ok(r.balanceDue <= r.zakatBeforePaid);
  assert.ok(r.zakatBeforePaid === 0 || Math.abs(r.zakatBeforePaid - r.netAssets * 0.025) < 1e-7);
}
console.log("Zakat calculation engine: 2,000 deterministic scenarios passed");
