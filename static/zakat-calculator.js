(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.ZakatCalculator = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";
  const SINDH_STANDARD_TOLA_GRAMS = 11.6638;
  const TROY_OUNCE_GRAMS = 31.1034768;
  const NISAB = Object.freeze({
    silver: Object.freeze({ grams: 612.36, priceKey: "silverPricePerGram", label: "Silver 612.36 g (classical South Asian conversion)" }),
    "gold-87": Object.freeze({ grams: 87.48, priceKey: "goldPricePerGram", label: "Gold 87.48 g (classical South Asian conversion)" }),
  });
  const JAFARI_NISAB = Object.freeze({
    gold: Object.freeze({ grams: 69.12, priceKey: "goldPricePerGram", label: "Sistani coined gold 69.12 g" }),
    silver: Object.freeze({ grams: 483.84, priceKey: "silverPricePerGram", label: "Sistani coined silver 483.84 g" })
  });
  const SUNNI_SCHOOLS = Object.freeze(["sunni-hanafi"]);
  const ASSET_KEYS = Object.freeze([
    "cash", "bank", "savings", "gold", "silver", "jewellery",
    "businessCash", "stock", "receivables", "property"
  ]);
  function amount(value, name) {
    const n = value === undefined || value === null || value === "" ? 0 : Number(value);
    if (!Number.isFinite(n) || n < 0) throw new RangeError(name + " must be a finite, non-negative amount");
    return n;
  }
  function validateCurrency(code) {
    const value = String(code || "").trim().toUpperCase();
    if (!/^[A-Z]{3}$/.test(value)) throw new RangeError("Enter a valid three-letter ISO 4217 currency code");
    let supported = null;
    if (typeof Intl.supportedValuesOf === "function") {
      supported = Intl.supportedValuesOf("currency");
    } else {
      supported = ["PKR","USD","GBP","EUR","SAR","AED","INR","BDT","NPR","LKR","QAR","KWD","BHD","OMR","JPY","CNY","CAD","AUD","NZD","CHF","SGD","MYR","IDR","THB","PHP","KRW","HKD","ZAR","NGN","EGP","BRL","MXN","TRY","SEK","NOK","DKK","PLN","CZK","HUF","ILS"];
    }
    if (!supported.includes(value)) throw new RangeError("Currency code is not supported by this browser");
    try {
      new Intl.NumberFormat("en", { style: "currency", currency: value }).format(0);
    } catch (_) {
      throw new RangeError("Currency code is not supported by this browser");
    }
    return value;
  }
  function pricePerGram(input, priceKey, unit) {
    const raw = amount(input[priceKey], priceKey);
    if (raw <= 0) throw new RangeError("Enter a current metal price in the selected currency and unit");
    const gramsPerUnit = unit === "tola" ? SINDH_STANDARD_TOLA_GRAMS : (unit === "ounce" ? TROY_OUNCE_GRAMS : 1);
    return raw / gramsPerUnit;
  }
  function finishResult(values) {
    const zakatBeforePaid = values.status === "payable" ? values.netAssets * 0.025 : 0;
    if (!Number.isFinite(zakatBeforePaid)) throw new RangeError("Zakat result exceeds the supported calculation range");
    const zakatPaid = amount(values.zakatPaid, "zakatPaid");
    return Object.freeze({
      ...values,
      zakatRate: 0.025,
      zakatBeforePaid,
      zakatPaid,
      balanceDue: Math.max(0, zakatBeforePaid - zakatPaid),
      overpayment: Math.max(0, zakatPaid - zakatBeforePaid)
    });
  }
  function calculateJafari(input, currency, metalPriceUnit) {
    const nisabMethod = JAFARI_NISAB[input.jafariNisabMethod || "gold"];
    if (!nisabMethod) throw new RangeError("Choose a supported Jafari Nisab method");
    const metalPrice = pricePerGram(input, nisabMethod.priceKey, metalPriceUnit);
    const tradeGoodsValue = amount(input.tradeGoodsValue, "tradeGoodsValue");
    const totalAssets = tradeGoodsValue;
    const totalLiabilities = 0;
    const netAssets = tradeGoodsValue;
    const nisabThreshold = nisabMethod.grams * metalPrice;
    if (![totalAssets, nisabThreshold, netAssets].every(Number.isFinite)) {
      throw new RangeError("Amounts exceed the supported calculation range");
    }
    const conditions = {
      adultAndSane: input.ownerAdultAndSane === true,
      acquiredThroughExchange: input.tradeGoodsAcquiredByExchange === true,
      hawlComplete: input.tradeGoodsHawlComplete === true,
      profitIntentionContinuous: input.tradeGoodsProfitIntentContinuous === true,
      accessContinuous: input.tradeGoodsAccessContinuous === true,
      marketValueAtLeastCost: input.tradeGoodsMarketValueAtLeastCost === true
    };
    const conditionsMet = Object.values(conditions).every(Boolean);
    const meetsNisab = netAssets >= nisabThreshold;
    const status = !conditionsMet ? "conditions_incomplete" : (!meetsNisab ? "below_nisab" : "payable");
    return finishResult({
      currency,
      schoolOfThought: "jafari-sistani",
      methodology: "jafari-sistani-trading-goods-obligatory-precaution",
      nisabMethod: "jafari-" + (input.jafariNisabMethod || "gold"),
      nisabLabel: nisabMethod.label,
      nisabGrams: nisabMethod.grams,
      metalPricePerGram: metalPrice,
      metalPriceUnit,
      totalAssets,
      totalLiabilities,
      netAssets,
      nisabThreshold,
      meetsNisab,
      conditionsMet,
      conditions,
      hawlComplete: conditions.hawlComplete,
      status,
      zakatPaid: input.zakatPaid
    });
  }
  function calculate(input) {
    if (!input || typeof input !== "object") throw new TypeError("Zakat calculation input is required");
    const currency = validateCurrency(input.currency || "PKR");
    const schoolOfThought = input.schoolOfThought || "sunni-hanafi";
    const metalPriceUnit = input.metalPriceUnit || "gram";
    if (!["gram", "tola", "ounce"].includes(metalPriceUnit)) throw new RangeError("Choose a supported metal price unit");
    if (schoolOfThought === "jafari-sistani") return calculateJafari(input, currency, metalPriceUnit);
    if (!SUNNI_SCHOOLS.includes(schoolOfThought)) throw new RangeError("Choose Hanafi or the supported Ja'fari method");
    const nisabMethod = input.nisabMethod || "silver";
    const method = NISAB[nisabMethod];
    if (!method) throw new RangeError("Choose a supported Nisab method");
    const metalPrice = pricePerGram(input, method.priceKey, metalPriceUnit);
    const assets = input.assets || {};
    const personalJewellery = amount(assets.jewellery, "jewellery");
    const totalAssets = ASSET_KEYS.reduce((sum, key) => {
      if (key === "jewellery" && schoolOfThought !== "sunni-hanafi") return sum;
      return sum + amount(assets[key], key);
    }, 0);
    const totalLiabilities = amount(input.liabilities, "liabilities");
    const netAssets = Math.max(0, totalAssets - totalLiabilities);
    const nisabThreshold = method.grams * metalPrice;
    if (!Number.isFinite(totalAssets) || !Number.isFinite(nisabThreshold) || !Number.isFinite(netAssets)) {
      throw new RangeError("Amounts exceed the supported calculation range");
    }
    const hawlComplete = input.hawlComplete === true;
    const meetsNisab = netAssets >= nisabThreshold;
    const status = !meetsNisab ? "below_nisab" : (!hawlComplete ? "hawl_incomplete" : "payable");
    return finishResult({
      currency,
      schoolOfThought,
      methodology: schoolOfThought,
      nisabMethod,
      nisabLabel: method.label,
      nisabGrams: method.grams,
      metalPricePerGram: metalPrice,
      metalPriceUnit,
      totalAssets,
      totalLiabilities,
      netAssets,
      nisabThreshold,
      meetsNisab,
      hawlComplete,
      personalJewelleryValue: personalJewellery,
      personalJewelleryIncluded: schoolOfThought === "sunni-hanafi",
      status,
      zakatPaid: input.zakatPaid
    });
  }
  return Object.freeze({
    calculate,
    validateCurrency,
    assetKeys: ASSET_KEYS,
    nisabMethods: NISAB,
    jafariNisabMethods: JAFARI_NISAB,
    sunniSchools: SUNNI_SCHOOLS,
    sindhStandardTolaGrams: SINDH_STANDARD_TOLA_GRAMS,
    troyOunceGrams: TROY_OUNCE_GRAMS
  });
});
