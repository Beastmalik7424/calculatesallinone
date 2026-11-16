"use strict";
const assert = require("node:assert/strict");
const { calculate, assetKeys } = require("../static/zakat-calculator.js");

const base = {
  currency: "PKR",
  nisabMethod: "silver",
  silverPricePerGram: 100,
  goldPricePerGram: 10000,
  metalPriceUnit: "gram",
  hawlComplete: true,
  liabilities: 0,
  zakatPaid: 0
};

let r = calculate({
  ...base,
  schoolOfThought: "sunni-hanafi",
  assets: { cash: 50000, jewellery: 50000 }
});
assert.equal(r.totalAssets, 100000, "Hanafi method must include qualifying personal-use jewellery");
assert.equal(r.zakatBeforePaid, 2500);

for (const [method, grams, priceKey] of [
  ["gold-85", 85, "goldPricePerGram"],
  ["silver-595", 595, "silverPricePerGram"]
]) {
  const result = calculate({
    ...base,
    schoolOfThought: "sunni-shafii",
    nisabMethod: method,
    [priceKey]: 100,
    assets: { cash: grams * 100 },
    hawlComplete: true
  });
  assert.equal(result.nisabGrams, grams, method + " must use its selected sourced reference weight");
  assert.equal(result.nisabThreshold, grams * 100, method + " must calculate the threshold correctly");
}
r = calculate({
  ...base,
  schoolOfThought: "sunni-shafii",
  goldPricePerGram: 100,
  assets: { cash: 8500 },
  hawlComplete: true
});
assert.equal(r.nisabGrams, 85, "Non-Hanafi presets must default to the common modern 85 g gold reference");
assert.equal(r.nisabThreshold, 8500, "The default modern gold threshold must use 85 g");

for (const school of ["sunni-shafii", "sunni-maliki", "sunni-hanbali"]) {
  r = calculate({
    ...base,
    schoolOfThought: school,
    nisabMethod: "gold-87",
    goldPricePerGram: 100,
    assets: { cash: 50000, jewellery: 50000 }
  });
  assert.equal(r.totalAssets, 50000, school + " must exclude ordinary permissible personal-use jewellery");
  assert.equal(r.schoolOfThought, school);
}

r = calculate({
  ...base,
  schoolOfThought: "jafari-sistani",
  jafariNisabMethod: "gold",
  tradeGoodsValue: 1000000,
  tradeGoodsAcquiredByExchange: true,
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: true,
  ownerAdultAndSane: true
});
assert.equal(r.nisabGrams, 69.12);
assert.equal(r.nisabThreshold, 691200);
assert.equal(r.zakatBeforePaid, 25000);
assert.equal(r.methodology, "jafari-sistani-trading-goods-obligatory-precaution");

r = calculate({
  ...base,
  schoolOfThought: "jafari-sistani",
  jafariNisabMethod: "gold",
  tradeGoodsValue: 1000000,
  tradeGoodsAcquiredByExchange: false,
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: true,
  ownerAdultAndSane: true
});
assert.equal(r.status, "conditions_incomplete", "Sistani trading goods must be acquired through a contract of exchange");
assert.equal(r.zakatBeforePaid, 0);

r = calculate({
  ...base,
  schoolOfThought: "jafari-sistani",
  jafariNisabMethod: "silver",
  silverPricePerGram: 100,
  tradeGoodsValue: 100000,
  tradeGoodsAcquiredByExchange: true,
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: true,
  ownerAdultAndSane: true
});
assert.equal(r.nisabGrams, 483.84);
assert.equal(r.nisabThreshold, 48384);
assert.equal(r.zakatBeforePaid, 2500);

r = calculate({
  ...base,
  schoolOfThought: "jafari-sistani",
  jafariNisabMethod: "gold",
  tradeGoodsValue: 1000000,
  assets: { cash: 1000000, bank: 500000 },
  tradeGoodsAcquiredByExchange: true,
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: true,
  ownerAdultAndSane: true
});
assert.equal(r.totalAssets, 1000000, "Sistani method must calculate qualifying trading goods, not add banknotes/cash");
assert.equal(r.zakatBeforePaid, 25000);

r = calculate({
  ...base,
  schoolOfThought: "jafari-sistani",
  jafariNisabMethod: "gold",
  tradeGoodsValue: 1000000,
  tradeGoodsAcquiredByExchange: true,
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: false,
  ownerAdultAndSane: true
});
assert.equal(r.status, "conditions_incomplete");
assert.equal(r.zakatBeforePaid, 0);

const validSistaniConditions = {
  ownerAdultAndSane: true,
  tradeGoodsAcquiredByExchange: true,
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: true
};
for (const condition of Object.keys(validSistaniConditions)) {
  const incomplete = calculate({
    ...base,
    schoolOfThought: "jafari-sistani",
    jafariNisabMethod: "gold",
    tradeGoodsValue: 1000000,
    ...validSistaniConditions,
    [condition]: false
  });
  assert.equal(incomplete.status, "conditions_incomplete", "Sistani condition must be mandatory: " + condition);
}

r = calculate({
  ...base,
  schoolOfThought: "sunni-hanafi",
  nisabMethod: "silver",
  silverPricePerGram: 1166.38,
  metalPriceUnit: "tola",
  assets: { cash: 100000 },
  hawlComplete: true
});
assert.ok(Math.abs(r.metalPricePerGram - 100) < 1e-10, "tola price must normalize to per-gram price");
assert.ok(Math.abs(r.nisabThreshold - 61236) < 1e-8, "tola conversion must preserve the silver Nisab threshold");

assert.throws(() => calculate({ ...base, schoolOfThought: "unknown" }), /school/i);
assert.throws(() => calculate({ ...base, metalPriceUnit: "ounce" }), /metal price unit/i);
assert.throws(() => calculate({ ...base, schoolOfThought: "jafari-sistani", jafariNisabMethod: "unknown" }), /Jafari Nisab/i);

// Deterministic stress coverage across all four Sunni options and both price units.
let seed = 20261116;
function random() {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 4294967296;
}
for (let i = 0; i < 2000; i++) {
  const school = ["sunni-hanafi", "sunni-shafii", "sunni-maliki", "sunni-hanbali"][i % 4];
  const nisabMethod = ["silver", "gold-87", "silver-595", "gold-85"][i % 4];
  const metalPriceUnit = i % 3 === 0 ? "tola" : "gram";
  const silverPerGram = 50 + random() * 300;
  const goldPerGram = 5000 + random() * 15000;
  const selectedPerGram = nisabMethod === "silver" ? silverPerGram : goldPerGram;
  const assets = Object.fromEntries(assetKeys.map(key => [key, Math.floor(random() * 1000000) / 100]));
  const result = calculate({
    currency: "PKR",
    schoolOfThought: school,
    nisabMethod,
    metalPriceUnit,
    silverPricePerGram: metalPriceUnit === "tola" ? silverPerGram * 11.6638 : silverPerGram,
    goldPricePerGram: metalPriceUnit === "tola" ? goldPerGram * 11.6638 : goldPerGram,
    assets,
    liabilities: Math.floor(random() * 500000) / 100,
    zakatPaid: Math.floor(random() * 50000) / 100,
    hawlComplete: i % 3 === 0
  });
  assert.ok(Number.isFinite(result.totalAssets) && Number.isFinite(result.netAssets));
  assert.equal(result.personalJewelleryIncluded, school === "sunni-hanafi");
  assert.ok(Math.abs(result.metalPricePerGram - selectedPerGram) < 1e-8);
  assert.ok(result.balanceDue >= 0 && result.balanceDue <= result.zakatBeforePaid);
  assert.ok(result.zakatBeforePaid === 0 || Math.abs(result.zakatBeforePaid - result.netAssets * 0.025) < 1e-7);
}

// Deterministic stress coverage for Sistani's two trading-goods Nisab paths.
for (let i = 0; i < 1000; i++) {
  const jafariNisabMethod = i % 2 === 0 ? "gold" : "silver";
  const metalPriceUnit = i % 3 === 0 ? "tola" : "gram";
  const nisabGrams = jafariNisabMethod === "gold" ? 69.12 : 483.84;
  const pricePerGram = 100 + random() * 500;
  const priceKey = jafariNisabMethod === "gold" ? "goldPricePerGram" : "silverPricePerGram";
  const threshold = nisabGrams * pricePerGram;
  const tradeGoodsValue = Math.floor(random() * threshold * 2);
  const conditions = {
    ownerAdultAndSane: true,
    tradeGoodsAcquiredByExchange: true,
    tradeGoodsHawlComplete: true,
    tradeGoodsProfitIntentContinuous: true,
    tradeGoodsAccessContinuous: true,
    tradeGoodsMarketValueAtLeastCost: true
  };
  if (i % 2 === 0) conditions[Object.keys(conditions)[i % 6]] = false;
  const result = calculate({
    currency: "PKR",
    schoolOfThought: "jafari-sistani",
    jafariNisabMethod,
    metalPriceUnit,
    [priceKey]: metalPriceUnit === "tola" ? pricePerGram * 11.6638 : pricePerGram,
    tradeGoodsValue,
    ...conditions
  });
  if (i % 2 === 0) {
    assert.equal(result.status, "conditions_incomplete");
    assert.equal(result.zakatBeforePaid, 0);
  } else {
    assert.equal(result.status, tradeGoodsValue >= threshold ? "payable" : "below_nisab");
    assert.equal(result.zakatBeforePaid, tradeGoodsValue >= threshold ? tradeGoodsValue * 0.025 : 0);
  }
}
console.log("Zakat fiqh-method tests: PASS (2,000 Sunni + 1,000 Sistani deterministic scenarios, plus boundary and validation cases)");
