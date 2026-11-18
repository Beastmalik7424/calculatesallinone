"use strict";
const assert = require("node:assert/strict");
const { calculate, assetKeys, sunniSchools, nisabMethods, jafariNisabMethods, sindhStandardTolaGrams, troyOunceGrams } = require("../static/zakat-calculator.js");

const base = {
  currency: "PKR", nisabMethod: "silver", silverPricePerGram: 100,
  goldPricePerGram: 10000, metalPriceUnit: "gram", hawlComplete: true,
  liabilities: 0, zakatPaid: 0
};

assert.deepEqual(sunniSchools, ["sunni-hanafi"]);
assert.deepEqual(Object.keys(nisabMethods).sort(), ["gold-87", "silver"]);
assert.equal(sindhStandardTolaGrams, 11.6638);
assert.equal(troyOunceGrams, 31.1034768);
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

// RED regression: unclassified pension and cryptocurrency balances must not be silently
// treated as eligible Hanafi wealth until their school-specific treatment is verified.
r = calculate({ ...base, schoolOfThought: "sunni-hanafi", assets: { cash: 70000, pension: 900000, crypto: 800000, investments: 500000 } });
assert.equal(r.totalAssets, 70000);

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
  assert.ok(Math.abs(r.zakatBeforePaid - grams * 2.5) < 1e-9, "Floating-point result must match the exact rational amount within precision tolerance");
}
r = calculate({ ...base, schoolOfThought: "jafari-sistani", jafariNisabMethod: "gold", tradeGoodsValue: 1000000, assets: { cash: 900000, bank: 500000 }, ...validSistaniConditions });
assert.equal(r.totalAssets, 1000000);
assert.equal(r.zakatBeforePaid, 25000);
for (const condition of Object.keys(validSistaniConditions)) {
  const incomplete = calculate({ ...base, schoolOfThought: "jafari-sistani", tradeGoodsValue: 1000000, ...validSistaniConditions, [condition]: false });
  assert.equal(incomplete.status, "conditions_incomplete");
  assert.equal(incomplete.zakatBeforePaid, 0);
}

// Sistani personal gold/silver coin Zakat is separate from ordinary cash and from business goods.
// Rulings 1912-1918 require minted coins used prevalently as money, separate metal Nisabs,
// the 11-month holding condition, adult/sane ownership, and legal/actual disposal rights.
const validCoinConditions = {
  jafariCoinsUsedAsMoney: true,
  ownerAdultAndSane: true,
  tradeGoodsAccessContinuous: true,
  jafariGoldCoinsHawlComplete: true,
  jafariSilverCoinsHawlComplete: true
};
const coinBase = {
  ...base, schoolOfThought: "jafari-sistani", jafariNisabMethod: "gold",
  tradeGoodsValue: 0, goldPricePerGram: 100, silverPricePerGram: 10,
  ...validCoinConditions
};
r = calculate({ ...coinBase, jafariGoldCoinsWeight: 69.12 });
assert.equal(r.goldCoinsStatus, "payable");
assert.equal(r.goldCoinsTaxableGrams, 69.12);
assert.equal(r.goldCoinsZakatBase, 6912);
assert.equal(r.zakatBase, 6912);
assert.equal(r.zakatBeforePaid, 172.8);

// Gold's second Nisab increment is 3 common mithqals (13.824 g): a smaller
// increase remains assessed on the first Nisab; a full increment is assessed in full.
r = calculate({ ...coinBase, jafariGoldCoinsWeight: 73.728 });
assert.equal(r.goldCoinsTaxableGrams, 69.12);
r = calculate({ ...coinBase, jafariGoldCoinsWeight: 82.944 });
assert.equal(r.goldCoinsTaxableGrams, 82.944);
assert.equal(r.zakatBeforePaid, 207.36);

// Silver's second Nisab increment is 21 common mithqals (96.768 g).
r = calculate({ ...coinBase, jafariGoldCoinsWeight: 488.448, jafariGoldCoinsWeight: 0, jafariSilverCoinsWeight: 488.448 });
assert.equal(r.silverCoinsStatus, "payable");
assert.equal(r.silverCoinsTaxableGrams, 483.84);
assert.equal(r.silverCoinsZakatBase, 4838.4);
r = calculate({ ...coinBase, jafariSilverCoinsWeight: 580.608 });
assert.equal(r.silverCoinsTaxableGrams, 580.608);

// Gold and silver do not combine to meet either personal-coin Nisab.
r = calculate({ ...coinBase, jafariGoldCoinsWeight: 69.11, jafariSilverCoinsWeight: 483.83 });
assert.equal(r.goldCoinsStatus, "below_nisab");
assert.equal(r.silverCoinsStatus, "below_nisab");
assert.equal(r.zakatBeforePaid, 0);
assert.equal(r.status, "below_nisab");

// Coins not minted/common as money, or missing the owner/disposal/11-month conditions,
// must not be charged merely because their weight reaches the threshold.
r = calculate({ ...coinBase, jafariCoinsUsedAsMoney: false, jafariGoldCoinsWeight: 100 });
assert.equal(r.goldCoinsStatus, "not_applicable");
assert.equal(r.zakatBeforePaid, 0);
r = calculate({ ...coinBase, jafariGoldCoinsHawlComplete: false, jafariGoldCoinsWeight: 69.12 });
assert.equal(r.goldCoinsStatus, "conditions_incomplete");
assert.equal(r.status, "conditions_incomplete");
assert.equal(r.zakatBeforePaid, 0);
r = calculate({ ...coinBase, ownerAdultAndSane: false, jafariGoldCoinsWeight: 69.12 });
assert.equal(r.goldCoinsStatus, "conditions_incomplete");
assert.equal(r.zakatBeforePaid, 0);
r = calculate({ ...coinBase, tradeGoodsAccessContinuous: false, jafariSilverCoinsWeight: 483.84 });
assert.equal(r.silverCoinsStatus, "conditions_incomplete");
assert.equal(r.zakatBeforePaid, 0);

// Coin weights and metal prices use the same selected unit and must remain
// economically equivalent for grams, the 11.6638 g standard tola and troy ounces.
for (const [metalPriceUnit, factor] of [["gram", 1], ["tola", 11.6638], ["ounce", 31.1034768]]) {
  const converted = calculate({
    ...coinBase, metalPriceUnit,
    goldPricePerGram: 100 * factor,
    silverPricePerGram: 10 * factor,
    jafariGoldCoinsWeight: 69.12 / factor
  });
  assert.ok(Math.abs(converted.goldCoinsTaxableGrams - 69.12) < 1e-8);
  assert.ok(Math.abs(converted.zakatBeforePaid - 172.8) < 1e-7);
}
assert.throws(() => calculate({ ...coinBase, jafariGoldCoinsWeight: -1 }), /jafariGoldCoinsWeight/);

// Qualifying business goods and qualifying coins are separate bases; their
// eligible amounts are summed only after each category independently passes its rules.
r = calculate({
  ...coinBase, tradeGoodsValue: 100000, jafariNisabMethod: "gold",
  tradeGoodsAcquiredByExchange: true, tradeGoodsHawlComplete: true,
  tradeGoodsProfitIntentContinuous: true, tradeGoodsMarketValueAtLeastCost: true,
  jafariGoldCoinsWeight: 69.12
});
assert.equal(r.tradeGoodsZakatBase, 100000);
assert.equal(r.goldCoinsZakatBase, 6912);
assert.equal(r.zakatBase, 106912);
assert.equal(r.zakatBeforePaid, 2672.8);

for (const bad of [-1, NaN, Infinity, -Infinity, "not-a-number"]) {
  assert.throws(() => calculate({ ...base, assets: { cash: bad } }));
  assert.throws(() => calculate({ ...base, liabilities: bad }));
  assert.throws(() => calculate({ ...base, silverPricePerGram: bad }));
  assert.throws(() => calculate({ ...base, zakatPaid: bad }));
}
assert.throws(() => calculate({ ...base, currency: "ZZZ" }), /currency/i);
assert.throws(() => calculate({ ...base, assets: { cash: Number.MAX_VALUE, bank: Number.MAX_VALUE } }), /supported calculation range/i);

// 3,000 deterministic Hanafi scenarios across both Nisab metals and all three price units.
let seed = 20261116;
function random() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
for (let i = 0; i < 3000; i++) {
  const nisabMethod = i % 2 === 0 ? "silver" : "gold-87";
  const metalPriceUnit = ["gram", "tola", "ounce"][i % 3];
  const silver = 50 + random() * 300, gold = 5000 + random() * 15000;
  const selected = nisabMethod === "silver" ? silver : gold;
  const assets = Object.fromEntries(assetKeys.map(key => [key, Math.floor(random() * 1000000) / 100]));
  const liabilities = Math.floor(random() * 500000) / 100, paid = Math.floor(random() * 50000) / 100;
  const result = calculate({
    currency: "PKR", schoolOfThought: "sunni-hanafi", nisabMethod, metalPriceUnit,
    silverPricePerGram: silver * (metalPriceUnit === "tola" ? 11.6638 : metalPriceUnit === "ounce" ? 31.1034768 : 1),
    goldPricePerGram: gold * (metalPriceUnit === "tola" ? 11.6638 : metalPriceUnit === "ounce" ? 31.1034768 : 1),
    assets, liabilities, zakatPaid: paid, hawlComplete: i % 3 === 0
  });
  assert.ok(Number.isFinite(result.totalAssets) && Number.isFinite(result.netAssets));
  assert.equal(result.personalJewelleryIncluded, true);
  assert.ok(Math.abs(result.metalPricePerGram - selected) < 1e-8);
  assert.ok(result.balanceDue >= 0 && result.balanceDue <= result.zakatBeforePaid);
  assert.ok(result.zakatBeforePaid === 0 || Math.abs(result.zakatBeforePaid - result.netAssets * 0.025) < 1e-7);
}

// 1,500 deterministic Sistani scenarios covering both Nisab metals, all three units and all six conditions.
for (let i = 0; i < 1500; i++) {
  const jafariNisabMethod = i % 2 === 0 ? "gold" : "silver";
  const metalPriceUnit = ["gram", "tola", "ounce"][i % 3];
  const grams = jafariNisabMethod === "gold" ? 69.12 : 483.84;
  const price = 100 + random() * 500, threshold = grams * price;
  const tradeGoodsValue = Math.floor(random() * threshold * 2);
  const conditions = { ...validSistaniConditions };
  if (i % 2 === 0) conditions[Object.keys(conditions)[Math.floor(i / 2) % 6]] = false;
  const priceKey = jafariNisabMethod === "gold" ? "goldPricePerGram" : "silverPricePerGram";
  const result = calculate({
    currency: "PKR", schoolOfThought: "jafari-sistani", jafariNisabMethod, metalPriceUnit,
    [priceKey]: price * (metalPriceUnit === "tola" ? 11.6638 : metalPriceUnit === "ounce" ? 31.1034768 : 1),
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
// Cross-unit economic equivalence: identical per-gram market prices must produce identical
// normalized metal prices, Nisab thresholds, statuses and Zakat for gram, tola and troy ounce.
for (const schoolOfThought of ["sunni-hanafi", "jafari-sistani"]) {
  for (const nisabMethod of schoolOfThought === "sunni-hanafi" ? ["silver", "gold-87"] : ["gold", "silver"]) {
    const priceKey = nisabMethod === "silver" ? "silverPricePerGram" : "goldPricePerGram";
    const perGram = 1234.567;
    const gramsPerUnit = { gram: 1, tola: 11.6638, ounce: 31.1034768 };
    const results = Object.entries(gramsPerUnit).map(([metalPriceUnit, factor]) => calculate({
      ...base, schoolOfThought,
      ...(schoolOfThought === "sunni-hanafi" ? { nisabMethod, assets: { cash: 900000 }, hawlComplete: true } :
        { jafariNisabMethod: nisabMethod, tradeGoodsValue: 900000, ...validSistaniConditions }),
      metalPriceUnit, [priceKey]: perGram * factor
    }));
    for (const result of results.slice(1)) {
      assert.ok(Math.abs(result.metalPricePerGram - results[0].metalPricePerGram) < 1e-9);
      assert.ok(Math.abs(result.nisabThreshold - results[0].nisabThreshold) < 1e-7);
      assert.equal(result.status, results[0].status);
      assert.ok(Math.abs(result.zakatBeforePaid - results[0].zakatBeforePaid) < 1e-7);
    }
  }
}
console.log("Zakat engine: PASS (3,000 Hanafi + 1,500 Sistani deterministic scenarios, all three units and cross-unit equivalence)");
