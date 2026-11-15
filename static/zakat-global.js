(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.ZakatGlobal = api;
})(typeof window !== "undefined" ? window : (typeof globalThis !== "undefined" ? globalThis : this), function () {
  "use strict";

  var TROY_OUNCE_GRAMS = 31.1034768;
  var NISAB_STANDARDS = {
    "silver-612.36": { metal: "silver", grams: 612.36, label: "Silver 612.36 g" },
    "gold-87.48": { metal: "gold", grams: 87.48, label: "Gold 87.48 g" },
    "silver-595": { metal: "silver", grams: 595, label: "Silver 595 g (AAOIFI SS 35)" },
    "gold-85": { metal: "gold", grams: 85, label: "Gold 85 g (AAOIFI SS 35)" }
  };
  var ASSET_FIELDS = ["cash", "gold", "silver", "stock", "receivables", "investments", "committee", "resaleProperty"];
  var FALLBACK_CURRENCIES = [
    "AED","AUD","BDT","BHD","BRL","CAD","CHF","CNY","DKK","EGP","EUR","GBP","HKD","IDR","INR",
    "JPY","KRW","KWD","LKR","MAD","MYR","NGN","NOK","NPR","NZD","OMR","PHP","PKR","PLN","QAR",
    "SAR","SEK","SGD","THB","TRY","TWD","TZS","USD","VND","ZAR"
  ];
  var lastRateFetchAt = 0;

  function amount(value, name) {
    if (value === undefined || value === null || value === "") return 0;
    var parsed = Number(value);
    if (!Number.isFinite(parsed) || parsed < 0) {
      throw new RangeError((name || "Amount") + " must be a finite non-negative number");
    }
    return parsed;
  }

  function calculateZakatCore(input) {
    if (!input || typeof input !== "object") throw new TypeError("Zakat inputs are required");
    var basis = NISAB_STANDARDS[input.basis];
    if (!basis) throw new RangeError("Unknown Nisab basis or standard");
    var assets = ASSET_FIELDS.reduce(function (total, key) {
      return total + amount(input[key], key);
    }, 0);
    var debts = amount(input.debts, "Debts");
    var net = Math.max(0, assets - debts);
    var price = input.metalPrice === "" || input.metalPrice === null || input.metalPrice === undefined
      ? 0 : Number(input.metalPrice);
    if (!Number.isFinite(price) || price < 0) throw new RangeError("Metal price must be a finite non-negative number");
    if (price === 0) {
      return { status: "missing-price", assets: assets, debts: debts, net: net, nisab: null, zakat: null, basis: basis };
    }
    var nisab = basis.grams * price;
    if (net < nisab) {
      return { status: "below-nisab", assets: assets, debts: debts, net: net, nisab: nisab, zakat: 0, basis: basis };
    }
    if (input.hawlComplete !== true) {
      return { status: "hawl-pending", assets: assets, debts: debts, net: net, nisab: nisab, zakat: null, basis: basis };
    }
    return { status: "due", assets: assets, debts: debts, net: net, nisab: nisab, zakat: net * 0.025, basis: basis };
  }

  function spotPricePerGram(usdPerTroyOunce, fxRate) {
    var spot = Number(usdPerTroyOunce);
    var fx = Number(fxRate);
    if (!Number.isFinite(spot) || spot <= 0 || !Number.isFinite(fx) || fx <= 0) return null;
    return spot * fx / TROY_OUNCE_GRAMS;
  }

  function supportedCurrencies() {
    var values = FALLBACK_CURRENCIES.slice();
    try {
      if (typeof Intl !== "undefined" && typeof Intl.supportedValuesOf === "function") {
        values = values.concat(Intl.supportedValuesOf("currency"));
      }
    } catch (_) {}
    return Array.from(new Set(values.filter(function (code) { return /^[A-Z]{3}$/.test(code); }))).sort();
  }

  function currencyName(code, locale) {
    try {
      if (typeof Intl !== "undefined" && typeof Intl.DisplayNames === "function") {
        return new Intl.DisplayNames([locale || "en"], { type: "currency" }).of(code);
      }
    } catch (_) {}
    return code;
  }

  function formatMoney(value, currency, locale) {
    try {
      return new Intl.NumberFormat(locale || "en", {
        style: "currency", currency: currency, maximumFractionDigits: 2
      }).format(value);
    } catch (_) {
      return currency + " " + Number(value).toFixed(2);
    }
  }

  function init() {
    var doc = root && root.document;
    if (!doc) return;
    var form = doc.getElementById("zakat-form");
    if (!form || form.dataset.zakatGlobalInitialized === "true") return;
    form.dataset.zakatGlobalInitialized = "true";

    function byId(id) { return doc.getElementById(id); }
    var currencySelect = byId("z-currency");
    var basisSelect = byId("z-nisab-basis");
    var result = byId("zakat-result");
    var rateStatus = byId("z-rate-status");
    var rateButton = byId("z-rate-refresh");
    var countryGuidance = byId("z-country-guidance");
    var goldPrice = byId("z-goldprice");
    var silverPrice = byId("z-silverprice");
    var locale = doc.documentElement.lang === "ur" ? "ur-PK" : "en";
    var currencies = supportedCurrencies();

    if (currencySelect) {
      currencySelect.textContent = "";
      currencies.forEach(function (code) {
        var option = doc.createElement("option");
        option.value = code;
        option.textContent = code + " — " + currencyName(code, locale);
        currencySelect.appendChild(option);
      });
      currencySelect.value = currencies.indexOf("PKR") >= 0 ? "PKR" : "USD";
    }

    function selectedCurrency() {
      return currencySelect && currencySelect.value ? currencySelect.value : "PKR";
    }
    function updateCurrencyGuidance() {
      if (countryGuidance) countryGuidance.hidden = selectedCurrency() !== "PKR";
    }
    function selectedBasis() {
      return basisSelect && NISAB_STANDARDS[basisSelect.value]
        ? NISAB_STANDARDS[basisSelect.value] : NISAB_STANDARDS["silver-612.36"];
    }
    function selectedMetalPrice() {
      var basis = selectedBasis();
      return amount((basis.metal === "gold" ? goldPrice : silverPrice).value, basis.metal + " price");
    }
    function writeResult(text) {
      if (result) result.textContent = text;
    }
    function refreshBasisHint() {
      var hint = byId("z-price-required");
      if (hint) hint.textContent = selectedBasis().metal === "gold"
        ? "Gold price per gram is required for the selected Nisab."
        : "Silver price per gram is required for the selected Nisab.";
    }

    if (currencySelect) currencySelect.addEventListener("change", function () {
      if (goldPrice) goldPrice.value = "";
      if (silverPrice) silverPrice.value = "";
      if (rateStatus) rateStatus.textContent = "Currency changed. Refresh indicative spot prices or enter current local prices manually.";
      updateCurrencyGuidance();
    });
    if (basisSelect) basisSelect.addEventListener("change", refreshBasisHint);
    updateCurrencyGuidance();
    refreshBasisHint();

    if (rateButton) rateButton.addEventListener("click", async function () {
      var now = Date.now();
      if (now - lastRateFetchAt < 60000) {
        if (rateStatus) rateStatus.textContent = "Rates are refreshed no more than once per minute. You can enter a local price manually.";
        return;
      }
      if (!root || typeof root.fetch !== "function") {
        if (rateStatus) rateStatus.textContent = "Live rates are unavailable in this browser. Enter local prices manually.";
        return;
      }
      var currency = selectedCurrency();
      rateButton.disabled = true;
      if (rateStatus) rateStatus.textContent = "Fetching indicative gold and silver spot prices…";
      try {
        var url = "https://xaus.com/api/v1/spot?currency=" + encodeURIComponent(currency) + "&unit=gram";
        var response = await root.fetch(url, {
          method: "GET",
          mode: "cors",
          credentials: "omit",
          cache: "no-store",
          headers: { "Accept": "application/json" }
        });
        if (!response.ok) throw new Error("Rate provider returned HTTP " + response.status);
        var data = await response.json();
        var gold = Number(data && data.xau && data.xau.price);
        var silver = spotPricePerGram(data && data.silver_usd_oz, data && data.fx_rate);
        if (!Number.isFinite(gold) || gold <= 0 || !Number.isFinite(silver) || silver <= 0) {
          throw new Error("The rate provider returned incomplete metal-price data");
        }
        if (goldPrice) goldPrice.value = String(gold);
        if (silverPrice) silverPrice.value = String(silver);
        lastRateFetchAt = now;
        var asOf = data.price_as_of || data.updated_at || "time not supplied";
        var stale = data.stale === true || data.fx_stale === true;
        if (rateStatus) {
          rateStatus.textContent = (stale ? "Provider marked this quote as stale. " : "Indicative spot rates loaded. ")
            + "Source: XAUS. Timestamp: " + asOf + " (UTC). Local dealer prices and jewellery premiums may differ; verify or edit both values.";
        }
      } catch (error) {
        if (rateStatus) rateStatus.textContent = "Live rates could not be verified (" + error.message + "). Enter current local gold and silver prices manually; no estimated price is substituted.";
      } finally {
        rateButton.disabled = false;
      }
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      try {
        var basis = basisSelect ? basisSelect.value : "silver-612.36";
        var standard = NISAB_STANDARDS[basis];
        if (!standard) throw new RangeError("Choose a supported Nisab standard");
        var values = {
          cash: byId("z-cash").value,
          gold: byId("z-gold").value,
          silver: byId("z-silver").value,
          stock: byId("z-stock").value,
          receivables: byId("z-recv").value,
          investments: byId("z-investments").value,
          committee: byId("z-committee").value,
          resaleProperty: byId("z-resale-property").value,
          debts: byId("z-debts").value,
          metalPrice: selectedMetalPrice(),
          basis: basis,
          hawlComplete: !!byId("z-hawl").checked
        };
        var calculation = calculateZakatCore(values);
        var currency = selectedCurrency();
        var lines = [
          "Calculation currency: " + currency,
          "Selected Nisab: " + standard.label,
          "Total zakatable assets entered: " + formatMoney(calculation.assets, currency, locale),
          "Less debts entered: " + formatMoney(calculation.debts, currency, locale),
          "Net zakatable wealth: " + formatMoney(calculation.net, currency, locale)
        ];
        if (calculation.status === "missing-price") {
          lines.push("Enter or refresh the selected " + standard.metal + " price per gram to calculate Nisab.");
        } else {
          lines.push("Nisab threshold: " + formatMoney(calculation.nisab, currency, locale));
          if (calculation.status === "below-nisab") {
            lines.push("Your net wealth is below the selected Nisab. No amount is calculated.");
          } else if (calculation.status === "hawl-pending") {
            lines.push("Your net wealth reaches Nisab. Confirm that the required lunar year (hawl) is complete before treating Zakat as due.");
          } else {
            lines.push("Zakat payable at 2.5% of net wealth: " + formatMoney(calculation.zakat, currency, locale));
          }
        }
        lines.push("This is an estimate using the inputs and method selected. It is not a fatwa.");
        writeResult(lines.join("\n"));
      } catch (error) {
        writeResult("Check your entries: " + error.message);
      }
    });
  }

  return {
    standards: NISAB_STANDARDS,
    supportedCurrencies: supportedCurrencies,
    calculateZakatCore: calculateZakatCore,
    spotPricePerGram: spotPricePerGram,
    formatMoney: formatMoney,
    init: init
  };
});
