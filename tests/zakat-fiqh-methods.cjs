"use strict";
const assert = require("node:assert/strict");
const { calculate } = require("../static/zakat-calculator.js");

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
  tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true,
  tradeGoodsAccessContinuous: true,
  tradeGoodsMarketValueAtLeastCost: false,
  ownerAdultAndSane: true
});
assert.equal(r.status, "conditions_incomplete");
assert.equal(r.zakatBeforePaid, 0);

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

console.log("Zakat fiqh-method engine tests: PASS (11 method, condition, threshold and unit assertions)");
