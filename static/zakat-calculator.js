(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.ZakatCalculator = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";
  const NISAB = Object.freeze({
    silver: Object.freeze({ grams: 612.36, priceKey: "silverPricePerGram", label: "Silver 612.36 g" }),
    "gold-87": Object.freeze({ grams: 87.48, priceKey: "goldPricePerGram", label: "Gold 87.48 g" }),
    "gold-85": Object.freeze({ grams: 85, priceKey: "goldPricePerGram", label: "Gold 85 g" })
  });
  const ASSET_KEYS = Object.freeze([
    "cash", "bank", "savings", "gold", "silver", "investments",
    "businessCash", "stock", "receivables", "pension", "crypto", "property"
  ]);
  function amount(value, name) {
    const n = value === undefined || value === null || value === "" ? 0 : Number(value);
    if (!Number.isFinite(n) || n < 0) throw new RangeError(name + " must be a finite, non-negative amount");
    return n;
  }
  function validateCurrency(code) {
    const value = String(code || "").trim().toUpperCase();
    if (!/^[A-Z]{3}$/.test(value)) throw new RangeError("Enter a valid three-letter ISO 4217 currency code");
    try {
      new Intl.NumberFormat("en", { style: "currency", currency: value }).format(0);
    } catch (_) {
      throw new RangeError("Currency code is not supported by this browser");
    }
    return value;
  }
  function calculate(input) {
    if (!input || typeof input !== "object") throw new TypeError("Zakat calculation input is required");
    const currency = validateCurrency(input.currency || "PKR");
    const method = NISAB[input.nisabMethod || "silver"];
    if (!method) throw new RangeError("Choose a supported Nisab method");
    const metalPrice = amount(input[method.priceKey], method.priceKey);
    if (metalPrice <= 0) throw new RangeError("Enter a current metal price per gram in the selected currency");
    const assets = input.assets || {};
    const totalAssets = ASSET_KEYS.reduce((sum, key) => sum + amount(assets[key], key), 0);
    const totalLiabilities = amount(input.liabilities, "liabilities");
    const netAssets = Math.max(0, totalAssets - totalLiabilities);
    const nisabThreshold = method.grams * metalPrice;
    if (!Number.isFinite(totalAssets) || !Number.isFinite(nisabThreshold) || !Number.isFinite(netAssets)) {
      throw new RangeError("Amounts exceed the supported calculation range");
    }
    const hawlComplete = input.hawlComplete === true;
    const zakatPaid = amount(input.zakatPaid, "zakatPaid");
    const meetsNisab = netAssets >= nisabThreshold;
    const status = !meetsNisab ? "below_nisab" : (!hawlComplete ? "hawl_incomplete" : "payable");
    const zakatBeforePaid = status === "payable" ? netAssets * 0.025 : 0;
    if (!Number.isFinite(zakatBeforePaid)) throw new RangeError("Zakat result exceeds the supported calculation range");
    return Object.freeze({
      currency, nisabMethod: input.nisabMethod || "silver", nisabLabel: method.label,
      nisabGrams: method.grams, metalPricePerGram: metalPrice,
      totalAssets, totalLiabilities, netAssets, nisabThreshold,
      meetsNisab, hawlComplete, status, zakatRate: 0.025,
      zakatBeforePaid, zakatPaid,
      balanceDue: Math.max(0, zakatBeforePaid - zakatPaid),
      overpayment: Math.max(0, zakatPaid - zakatBeforePaid)
    });
  }
  return Object.freeze({ calculate, validateCurrency, assetKeys: ASSET_KEYS, nisabMethods: NISAB });
});
