"use strict";
const assert = require("node:assert/strict");
const { calculate, assetKeys, sunniSchools, nisabMethods, jafariNisabMethods, sindhStandardTolaGrams } = require("../static/zakat-calculator.js");

const base = {
  currency: "PKR", nisabMethod: "silver", silverPricePerGram: 100,
  goldPricePerGram: 10000, metalPriceUnit: "gram", hawlComplete: true,
  liabilities: 0, zakatPaid: 0
};

assert.deepEqual(sunniSchools, ["sunni-hanafi"]);
assert.deepEqual(Object.keys(nisabMethods).sort(), ["gold-87", "silver"]);
assert.equal(sindhStandardTolaGrams, 11.6638);
assert.equal(nisabMethods.silver.grams, 612.36);
assert.equal(nisabMethods["gold-87"].grams, 87.48);
assert.equal(jafariNisabMethods.gold.grams, 69.12);
assert.equal(jafariNisabMethods.silver.grams, 483.84);

let r = calculate({ ...base, schoolOfThought: "sunni-hanafi", assets: { cash: 50000, jewellery: 50000 } });
assert.equal(r.totalAssets, 100000);
assert.equal(r.zakatBeforePaid, 2500);
assert.equal(r.personalJewelleryIncluded, true);
assert.equal(r.nisabGrams, 612.36);

r = calculate({ ...base, schoolOfThought: "sunni-hanafi", nisabMethod: "gold-87", goldPricePerGram: 100, assets: { cash: 8748 } });
assert.equal(r.nisabThreshold, 8748);
assert.equal(r.nisabGrams, 87.48);
assert.equal(r.status, "payable");

r = calculate({ ...base, schoolOfThought: "sunni-hanafi", assets: { cash: 70000 }, hawlComplete: false });
assert.equal(r.status, "hawl_incomplete");
assert.equal(r.zakatBeforePaid, 0);

r = calculate({ ...base, schoolOfThought: "sunni-hanafi", assets: { cash: 70000 }, zakatPaid: 500 });
assert.equal(r.balanceDue, 1250);
assert.equal(r.overpayment, 0);
r = calculate({ ...base, schoolOfThought: "sunni-hanafi", assets: { cash: 70000 }, zakatPaid: 2000 });
assert.equal(r.balanceDue, 0);
assert.equal(r.overpayment, 250);

r = calculate({ ...base, schoolOfThought: "sunni-hanafi", metalPriceUnit: "tola", silverPricePerGram: 1166.38, assets: { cash: 100000 } });
assert.ok(Math.abs(r.metalPricePerGram - 100) < 1e-10);
assert.ok(Math.abs(r.nisabThreshold - 61236) < 1e-8);

for (const school of ["sunni-shafii", "sunni-maliki", "sunni-hanbali", "unknown"]) {
  assert.throws(() => calculate({ ...base, schoolOfThought: school }), /Hanafi|school/i);
}
assert.throws(() => calculate({ ...base, nisabMethod: "gold-85" }), /Nisab method/i);
assert.throws(() => calculate({ ...base, schoolOfThought: "jafari-sistani", jafariNisabMethod: "unknown" }), /Jafari Nisab/i);

const validSistaniConditions = {
  ownerAdultAndSane: true, tradeGoodsAcquiredByExchange: true, tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true, tradeGoodsAccessContinuous: true, tradeGoodsMarketValueAtLeastCost: true
};
for (const [method, grams, priceKey] of [["gold",69.12,"goldPricePerGram"],["silver",483.84,"silverPricePerGram"]]) {
  r = calculate({ ...base, schoolOfThought: "jafari-sistani", jafariNisabMethod: method, [priceKey]: 100, tradeGoodsValue: grams * 100, ...validSistaniConditions });
  assert.equal(r.nisabGrams, grams);
  assert.equal(r.nisabThreshold, grams * 100);
  assert.equal(r.zakatBeforePaid, grams * 2.5);
}
r = calculate({ ...base, schoolOfThought: "jafari-sistani", jafariNisabMethod: "gold", tradeGoodsValue: 1000000, assets: { cash: 900000, bank: 500000 }, ...validSistaniConditions });
assert.equal(r.totalAssets, 1000000);
assert.equal(r.zakatBeforePaid, 25000);
for (const condition of Object.keys(validSistaniConditions)) {
  const incomplete = calculate({ ...base, schoolOfThought: "jafari-sistani", tradeGoodsValue: 1000000, ...validSistaniConditions, [condition]: false });
  assert.equal(incomplete.status, "conditions_incomplete");
  assert.equal(incomplete.zakatBeforePaid, 0);
}

for (const bad of [-1, NaN, Infinity, -Infinity, "not-a-number"]) {
  assert.throws(() => calculate({ ...base, assets: { cash: bad } }));
  assert.throws(() => calculate({ ...base, liabilities: bad }));
  assert.throws(() => calculate({ ...base, silverPricePerGram: bad }));
  assert.throws(() => calculate({ ...base, zakatPaid: bad }));
}
assert.throws(() => calculate({ ...base, currency: "ZZZ" }), /currency/i);
assert.throws(() => calculate({ ...base, assets: { cash: Number.MAX_VALUE, bank: Number.MAX_VALUE } }), /supported calculation range/i);

// 2,000 deterministic Hanafi scenarios across both supported Nisab metals and both price units.
let seed = 20261116;
function random() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
for (let i = 0; i < 2000; i++) {
  const nisabMethod = i % 2 === 0 ? "silver" : "gold-87";
  const metalPriceUnit = i % 3 === 0 ? "tola" : "gram";
  const silver = 50 + random() * 300, gold = 5000 + random() * 15000;
  const selected = nisabMethod === "silver" ? silver : gold;
  const assets = Object.fromEntries(assetKeys.map(key => [key, Math.floor(random() * 1000000) / 100]));
  const liabilities = Math.floor(random() * 500000) / 100, paid = Math.floor(random() * 50000) / 100;
  const result = calculate({
    currency: "PKR", schoolOfThought: "sunni-hanafi", nisabMethod, metalPriceUnit,
    silverPricePerGram: metalPriceUnit === "tola" ? silver * 11.6638 : silver,
    goldPricePerGram: metalPriceUnit === "tola" ? gold * 11.6638 : gold,
    assets, liabilities, zakatPaid: paid, hawlComplete: i % 3 === 0
  });
  assert.ok(Number.isFinite(result.totalAssets) && Number.isFinite(result.netAssets));
  assert.equal(result.personalJewelleryIncluded, true);
  assert.ok(Math.abs(result.metalPricePerGram - selected) < 1e-8);
  assert.ok(result.balanceDue >= 0 && result.balanceDue <= result.zakatBeforePaid);
  assert.ok(result.zakatBeforePaid === 0 || Math.abs(result.zakatBeforePaid - result.netAssets * 0.025) < 1e-7);
}

// 1,000 deterministic Sistani scenarios covering both Nisab metals and all six conditions.
for (let i = 0; i < 1000; i++) {
  const jafariNisabMethod = i % 2 === 0 ? "gold" : "silver";
  const metalPriceUnit = i % 3 === 0 ? "tola" : "gram";
  const grams = jafariNisabMethod === "gold" ? 69.12 : 483.84;
  const price = 100 + random() * 500, threshold = grams * price;
  const tradeGoodsValue = Math.floor(random() * threshold * 2);
  const conditions = { ...validSistaniConditions };
  if (i % 2 === 0) conditions[Object.keys(conditions)[i % 6]] = false;
  const priceKey = jafariNisabMethod === "gold" ? "goldPricePerGram" : "silverPricePerGram";
  const result = calculate({
    currency: "PKR", schoolOfThought: "jafari-sistani", jafariNisabMethod, metalPriceUnit,
    [priceKey]: metalPriceUnit === "tola" ? price * 11.6638 : price,
    tradeGoodsValue, ...conditions
  });
  if (i % 2 === 0) {
    assert.equal(result.status, "conditions_incomplete");
    assert.equal(result.zakatBeforePaid, 0);
  } else {
    assert.equal(result.status, tradeGoodsValue >= threshold ? "payable" : "below_nisab");
    assert.equal(result.zakatBeforePaid, tradeGoodsValue >= threshold ? tradeGoodsValue * 0.025 : 0);
  }
}
console.log("Zakat engine: PASS (2,000 Hanafi + 1,000 Sistani deterministic scenarios, boundary, validation and unit-conversion cases)");
