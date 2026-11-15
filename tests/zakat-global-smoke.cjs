"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const engine = require("../static/zakat-global.js");

const page = fs.readFileSync("public/zakat-calculator/index.html", "utf8");
const urduPage = fs.readFileSync("public/ur/zakat-calculator/index.html", "utf8");
const script = fs.readFileSync("static/zakat-global.js", "utf8");

for (const id of [
  "z-currency", "z-nisab-basis", "z-goldprice", "z-silverprice",
  "z-investments", "z-committee", "z-resale-property", "z-rate-refresh",
  "z-rate-status", "z-country-guidance"
]) {
  assert.match(page, new RegExp('id="' + id + '"'), "Global Zakat UI must include " + id);
}
assert.match(script, /Intl\.supportedValuesOf\(["']currency["']\)/, "Currency list must use browser ISO currency data when available");
assert.match(script, /xaus\.com\/api\/v1\/spot/, "Live metal prices must use the documented multi-currency spot endpoint");
assert.match(page, /AAOIFI.*35|AAOIFI SS 35/i, "Page must explain the AAOIFI Nisab standard");
assert.match(page, /612\.36/);
assert.match(page, /87\.48/);
assert.match(page, /595/);
assert.match(page, /85/);
assert.match(page, /503,529/);
assert.match(page, /State Bank of Pakistan|SBP/);
assert.match(page, /aaoifi\.com/);
assert.match(page, /islamic-relief\.org/);
assert.match(page, /nzf\.org\.uk/);
assert.match(page, /sbp\.org\.pk/);
assert.match(urduPage, /id="z-currency"/);
assert.match(urduPage, /id="z-nisab-basis"/);
assert.match(urduPage, /پاکستان/);
assert.match(urduPage, /چاندی/);
assert.match(urduPage, /سونا/);

const calculate = engine.calculateZakatCore;
const base = {
  cash: 0, gold: 0, silver: 0, stock: 0, receivables: 0,
  investments: 0, committee: 0, resaleProperty: 0, debts: 0,
  metalPrice: 1, basis: "silver-612.36", hawlComplete: true
};
for (const [basis, grams] of [
  ["silver-612.36", 612.36],
  ["gold-87.48", 87.48],
  ["silver-595", 595],
  ["gold-85", 85]
]) {
  const result = calculate({ ...base, cash: grams, basis });
  assert.equal(result.status, "due", basis + " must be due at the exact Nisab boundary");
  assert.ok(Math.abs(result.zakat - grams * 0.025) < 1e-10, basis + " must calculate 2.5% of the full net wealth");
  assert.equal(calculate({ ...base, cash: grams - 0.01, basis }).status, "below-nisab",
    basis + " must not be due below Nisab");
}
assert.equal(calculate({ ...base, cash: 1000, metalPrice: 0 }).status, "missing-price");
assert.equal(calculate({ ...base, cash: 1000, hawlComplete: false }).status, "hawl-pending");
assert.equal(calculate({ ...base, cash: 1000, debts: 1000 }).status, "below-nisab");
assert.equal(calculate({ ...base, cash: 1000, debts: 100 }).net, 900);
assert.equal(calculate({
  ...base, cash: 1000, investments: 500, committee: 250, resaleProperty: 250, debts: 100
}).net, 1900);
assert.throws(() => calculate({ ...base, cash: -1 }), /non-negative/i);
assert.throws(() => calculate({ ...base, basis: "unknown" }), /Nisab basis/i);
assert.throws(() => calculate({ ...base, metalPrice: -1 }), /non-negative/i);
assert.ok(engine.supportedCurrencies().includes("PKR"));
assert.ok(engine.supportedCurrencies().includes("USD"));
const silver = engine.spotPricePerGram(3000, 280);
assert.ok(Math.abs(silver - (3000 * 280 / 31.1034768)) < 1e-10);
assert.equal(engine.spotPricePerGram(0, 280), null);

console.log("PASS: global Zakat currency, live-rate, Pakistan notice, Urdu parity, four Nisab standards and calculation boundaries");
