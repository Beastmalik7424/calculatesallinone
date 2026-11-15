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
    "gold-87-28": Object.freeze({ grams: 87.28, priceKey: "goldPricePerGram", label: "Gold 87.28 g (Islamic Relief Pakistan)" }),
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
  function calculate(input) {
    if (!input || typeof input !== "object") throw new TypeError("Zakat calculation input is required");
    const sect = input.sect || "sunni";
    if (sect !== "sunni" && sect !== "shia") throw new RangeError("Choose a supported sect");
    if (sect === "shia") {
      if (input.marja !== "sistani") throw new RangeError("Choose a verified Marja");
      return Object.freeze({
        sect: "shia", school: "jafari", marja: "sistani",
        status: "scholar_review_required", currency: null,
        balanceDue: null, zakatBeforePaid: null,
        guidance: "Under Ayatollah Sistani's published rulings, ordinary paper banknotes and non-gold/silver coins are not subject to the obligatory Zakat rules for gold and silver money. Zakat on gold and silver applies only to qualifying minted coins used commonly in transactions and subject to the stated Nisab and time conditions. Trading capital has a separate obligatory-precaution ruling. This calculator does not collect the coinage, trading-intention, ownership-duration or other facts needed for a valid Ja'fari ruling, so it will not invent a numeric amount. Consult your Marja's office for your case."
      });
    }
    const school = input.school || "hanafi";
    if (!["hanafi", "shafii", "maliki", "hanbali"].includes(school)) throw new RangeError("Choose a supported Sunni madhhab");
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
      sect, school, currency, nisabMethod: input.nisabMethod || "silver", nisabLabel: method.label,
      nisabGrams: method.grams, metalPricePerGram: metalPrice,
      totalAssets, totalLiabilities, netAssets, nisabThreshold,
      meetsNisab, hawlComplete, status, zakatRate: 0.025,
      zakatBeforePaid, zakatPaid,
      balanceDue: Math.max(0, zakatBeforePaid - zakatPaid),
      overpayment: Math.max(0, zakatPaid - zakatBeforePaid)
    });
  }
  function calculateUshr(input) {
    if (!input || typeof input !== "object") throw new TypeError("Ushr calculation input is required");
    const sect = input.sect || "sunni";
    if (sect !== "sunni" && sect !== "shia") throw new RangeError("Choose a supported sect");
    const quantityKg = amount(input.quantityKg, "harvest quantity");
    const marketValue = amount(input.marketValue, "harvest market value");
    const currency = validateCurrency(input.currency || "PKR");
    const irrigation = input.irrigation;
    if (!["rain", "cost", "mixed"].includes(irrigation)) throw new RangeError("Choose a supported irrigation method");
    const crop = String(input.crop || "").toLowerCase();
    let school = input.school || "hanafi";
    let nisabKg = 653;
    let nisabPosition = "five-wasq";
    if (sect === "shia") {
      if (input.marja !== "sistani") throw new RangeError("Choose a verified Marja");
      school = "jafari";
      if (!["wheat", "barley", "dates", "raisins"].includes(crop)) {
        throw new RangeError("Sistani's verified Ushr ruling covers only the four specified crops");
      }
      nisabKg = 847;
      nisabPosition = "sistani-300-saa";
    } else {
      if (!["hanafi", "shafii", "maliki", "hanbali"].includes(school)) {
        throw new RangeError("Choose a supported Sunni madhhab");
      }
      if (input.eligibleCropConfirmed !== true) {
        throw new RangeError("Confirm that this crop is eligible under your selected madhhab");
      }
      if (school === "hanafi") {
        nisabPosition = input.nisabPosition || "abu-hanifa";
        if (nisabPosition === "abu-hanifa") nisabKg = 0;
        else if (nisabPosition === "sahibayn") nisabKg = 653;
        else throw new RangeError("Choose a verified Hanafi crop Nisab position");
      }
    }
    if (quantityKg === 0) {
      return Object.freeze({
        sect, school, currency, crop, quantityKg, marketValue, irrigation,
        rate: null, nisabKg, nisabPosition, meetsNisab: false, status: "no_harvest",
        produceDueKg: 0, amountDue: 0,
        guidance: "No harvested produce was entered. Ushr is estimated from eligible harvested produce, not from a market-value-only entry."
      });
    }
    // Five wasqs is a volume threshold, not a universal mass threshold.
    // The 653 kg approximation in this tool is only grounded for wheat.
    // Do not reuse wheat's mass conversion for other crops.
    const usesFiveWasq = sect === "sunni" && !(school === "hanafi" && nisabPosition === "abu-hanifa");
    if (usesFiveWasq && crop !== "wheat") {
      return Object.freeze({
        sect, school, currency, crop, quantityKg, marketValue, irrigation,
        rate: null, nisabKg: null, nisabPosition, meetsNisab: null,
        status: "scholar_review_required", produceDueKg: null, amountDue: null,
        guidance: "The five-wasq threshold is a volume measure. Its mass equivalent varies by crop and measurement conditions. A verified crop-specific conversion is not available here, so confirm the threshold with a qualified scholar or agricultural authority. No Ushr amount is estimated."
      });
    }
    if (sect === "sunni" && irrigation === "mixed" && input.mixedRateConfirmed !== true) {
      return Object.freeze({
        sect, school, status: "scholar_review_required", currency,
        amountDue: null, rate: null, nisabKg, nisabPosition,
        guidance: "Mixed irrigation is treated differently in detailed Sunni school rulings and depends on which method predominates. Confirm the applicable rate with your qualified scholar. The calculator will not assume a universal 7.5% midpoint."
      });
    }
    const rate = irrigation === "rain" ? 0.10 : (irrigation === "cost" ? 0.05 : 0.075);
    if (!Number.isFinite(marketValue * rate) || !Number.isFinite(quantityKg * rate)) throw new RangeError("Ushr amount exceeds the supported calculation range");
    const meetsNisab = quantityKg >= nisabKg;
    const status = meetsNisab ? "payable" : "below_nisab";
    return Object.freeze({
      sect, school, currency, crop, quantityKg, marketValue, irrigation,
      rate, nisabKg, nisabPosition, meetsNisab, status,
      produceDueKg: meetsNisab ? quantityKg * rate : 0,
      amountDue: meetsNisab ? marketValue * rate : 0,
      guidance: sect === "shia"
        ? "Sistani's crop Zakat applies only to wheat, barley, dates and raisins at approximately 847 kg. Rain or natural irrigation: 10%; irrigation requiring tools or pumping: 5%; where both methods are commonly regarded as jointly used: 7.5%. Crop expenses and seed are not deducted before checking Nisab under the cited rulings."
        : "This is a crop-specific Ushr estimate, not wealth Zakat. It is due at harvest, with no lunar-year wait. Confirm crop eligibility, crop measurement stage, ownership and any local statutory rules with your qualified scholar or authority."
    });
  }
  return Object.freeze({ calculate, calculateUshr, validateCurrency, assetKeys: ASSET_KEYS, nisabMethods: NISAB });
});
