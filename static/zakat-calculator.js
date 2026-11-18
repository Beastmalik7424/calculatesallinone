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
  const JAFARI_COIN_NISAB = Object.freeze({
    gold: Object.freeze({ grams: 69.12, incrementGrams: 13.824, priceKey: "goldPricePerGram", label: "Sistani minted gold coins 69.12 g; next increment 13.824 g" }),
    silver: Object.freeze({ grams: 483.84, incrementGrams: 96.768, priceKey: "silverPricePerGram", label: "Sistani minted silver coins 483.84 g; next increment 96.768 g" })
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
    const zakatBase = values.zakatBase === undefined ? values.netAssets : amount(values.zakatBase, "zakatBase");
    const zakatBeforePaid = values.status === "payable" ? zakatBase * 0.025 : 0;
    if (!Number.isFinite(zakatBeforePaid)) throw new RangeError("Zakat result exceeds the supported calculation range");
    const zakatPaid = amount(values.zakatPaid, "zakatPaid");
    return Object.freeze({
      ...values,
      zakatBase,
      zakatRate: 0.025,
      zakatBeforePaid,
      zakatPaid,
      balanceDue: Math.max(0, zakatBeforePaid - zakatPaid),
      overpayment: Math.max(0, zakatPaid - zakatBeforePaid)
    });
  }
  function gramsPerUnit(unit) {
    return unit === "tola" ? SINDH_STANDARD_TOLA_GRAMS : (unit === "ounce" ? TROY_OUNCE_GRAMS : 1);
  }
  function weightInGrams(value, unit, name) {
    const grams = amount(value, name) * gramsPerUnit(unit);
    if (!Number.isFinite(grams)) throw new RangeError(name + " exceeds the supported calculation range");
    return grams;
  }
  function taxableCoinGrams(weightGrams, firstNisabGrams, incrementGrams) {
    if (weightGrams + 1e-9 < firstNisabGrams) return 0;
    const increments = Math.floor((weightGrams - firstNisabGrams + 1e-9) / incrementGrams);
    return firstNisabGrams + increments * incrementGrams;
  }
  function calculateJafari(input, currency, metalPriceUnit) {
    const nisabMethod = JAFARI_NISAB[input.jafariNisabMethod || "gold"];
    if (!nisabMethod) throw new RangeError("Choose a supported Jafari Nisab method");

    const tradeGoodsValue = amount(input.tradeGoodsValue, "tradeGoodsValue");
    const metalPrice = tradeGoodsValue > 0 ? pricePerGram(input, nisabMethod.priceKey, metalPriceUnit) : 0;
    const nisabThreshold = tradeGoodsValue > 0 ? nisabMethod.grams * metalPrice : 0;
    const conditions = {
      adultAndSane: input.ownerAdultAndSane === true,
      acquiredThroughExchange: input.tradeGoodsAcquiredByExchange === true,
      hawlComplete: input.tradeGoodsHawlComplete === true,
      profitIntentionContinuous: input.tradeGoodsProfitIntentContinuous === true,
      accessContinuous: input.tradeGoodsAccessContinuous === true,
      marketValueAtLeastCost: input.tradeGoodsMarketValueAtLeastCost === true
    };
    const conditionsMet = Object.values(conditions).every(Boolean);
    const tradeGoodsMeetsNisab = tradeGoodsValue > 0 && tradeGoodsValue >= nisabThreshold;
    const tradeGoodsStatus = tradeGoodsValue <= 0 ? "not_applicable" :
      (!tradeGoodsMeetsNisab ? "below_nisab" : (!conditionsMet ? "conditions_incomplete" : "payable"));
    const tradeGoodsZakatBase = tradeGoodsStatus === "payable" ? tradeGoodsValue : 0;

    const coinsUsedAsMoney = input.jafariCoinsUsedAsMoney === true;
    const coinOwnerAndAccess = conditions.adultAndSane && conditions.accessContinuous;
    const goldCoinsWeightGrams = weightInGrams(input.jafariGoldCoinsWeight, metalPriceUnit, "jafariGoldCoinsWeight");
    const silverCoinsWeightGrams = weightInGrams(input.jafariSilverCoinsWeight, metalPriceUnit, "jafariSilverCoinsWeight");

    function evaluateCoins(metal, weightGrams, hawlComplete) {
      const method = JAFARI_COIN_NISAB[metal];
      const meetsNisab = coinsUsedAsMoney && weightGrams + 1e-9 >= method.grams;
      if (!coinsUsedAsMoney || weightGrams <= 0) {
        return { status: "not_applicable", meetsNisab: false, taxableGrams: 0, value: 0, zakatBase: 0, pricePerGram: 0 };
      }
      if (!meetsNisab) {
        return { status: "below_nisab", meetsNisab: false, taxableGrams: 0, value: 0, zakatBase: 0, pricePerGram: 0 };
      }
      const taxableGrams = taxableCoinGrams(weightGrams, method.grams, method.incrementGrams);
      if (!coinOwnerAndAccess || !hawlComplete) {
        return { status: "conditions_incomplete", meetsNisab: true, taxableGrams, value: 0, zakatBase: 0, pricePerGram: 0 };
      }
      const price = pricePerGram(input, method.priceKey, metalPriceUnit);
      return {
        status: "payable",
        meetsNisab: true,
        taxableGrams,
        value: weightGrams * price,
        zakatBase: taxableGrams * price,
        pricePerGram: price
      };
    }

    const goldCoins = evaluateCoins("gold", goldCoinsWeightGrams, input.jafariGoldCoinsHawlComplete === true);
    const silverCoins = evaluateCoins("silver", silverCoinsWeightGrams, input.jafariSilverCoinsHawlComplete === true);
    const goldCoinsZakatBase = goldCoins.zakatBase;
    const silverCoinsZakatBase = silverCoins.zakatBase;
    const zakatBase = tradeGoodsZakatBase + goldCoinsZakatBase + silverCoinsZakatBase;
    const totalAssets = tradeGoodsValue + goldCoins.value + silverCoins.value;
    const totalLiabilities = 0;
    const netAssets = totalAssets;
    if (![totalAssets, nisabThreshold, netAssets, zakatBase].every(Number.isFinite)) {
      throw new RangeError("Amounts exceed the supported calculation range");
    }

    const meetsNisab = tradeGoodsMeetsNisab || goldCoins.meetsNisab || silverCoins.meetsNisab;
    const anyConditionsIncomplete = tradeGoodsStatus === "conditions_incomplete" ||
      goldCoins.status === "conditions_incomplete" || silverCoins.status === "conditions_incomplete";
    const status = zakatBase > 0 ? "payable" : (anyConditionsIncomplete ? "conditions_incomplete" : "below_nisab");
    const coinConditions = {
      mintedAndCommonlyUsedAsMoney: coinsUsedAsMoney,
      adultAndSane: conditions.adultAndSane,
      accessContinuous: conditions.accessContinuous,
      goldHawlComplete: input.jafariGoldCoinsHawlComplete === true,
      silverHawlComplete: input.jafariSilverCoinsHawlComplete === true
    };

    return finishResult({
      currency,
      schoolOfThought: "jafari-sistani",
      methodology: "jafari-sistani-personal-coins-and-trading-goods",
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
      conditions: { tradeGoods: conditions, coins: coinConditions },
      coinConditionsMet: coinsUsedAsMoney && coinOwnerAndAccess &&
        (goldCoinsWeightGrams < JAFARI_COIN_NISAB.gold.grams || coinConditions.goldHawlComplete) &&
        (silverCoinsWeightGrams < JAFARI_COIN_NISAB.silver.grams || coinConditions.silverHawlComplete),
      tradeGoodsStatus,
      tradeGoodsZakatBase,
      goldCoinsStatus: goldCoins.status,
      silverCoinsStatus: silverCoins.status,
      goldCoinsWeightGrams,
      silverCoinsWeightGrams,
      goldCoinsTaxableGrams: goldCoins.taxableGrams,
      silverCoinsTaxableGrams: silverCoins.taxableGrams,
      goldCoinsValue: goldCoins.value,
      silverCoinsValue: silverCoins.value,
      goldCoinsZakatBase,
      silverCoinsZakatBase,
      coinNisab: JAFARI_COIN_NISAB,
      zakatBase,
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
    jafariCoinNisabMethods: JAFARI_COIN_NISAB,
    sunniSchools: SUNNI_SCHOOLS,
    sindhStandardTolaGrams: SINDH_STANDARD_TOLA_GRAMS,
    troyOunceGrams: TROY_OUNCE_GRAMS
  });
});
