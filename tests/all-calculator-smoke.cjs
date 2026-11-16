const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const handlers = {};
const elements = {};
const observers = [];
const insertedShareButtons = [];
function element(id, value = "") {
  return elements[id] = {
    id, value, checked: false, disabled: false, hidden: false, textContent: "", options: [], selectedIndex: 0,
    attributes: {}, _handlers: {}, parentNode: { insertBefore(node) { insertedShareButtons.push(node); node.parentNode = this; }, appendChild(node) { insertedShareButtons.push(node); node.parentNode = this; } }, classList: {
      _set: new Set(),
      toggle(name, force) { if (force === undefined ? !this._set.has(name) : force) this._set.add(name); else this._set.delete(name); },
      contains(name) { return this._set.has(name); }
    },
    addEventListener(type, fn) { this._handlers[type] = fn; },
    appendChild(option) { this.options.push(option); },
    set innerHTML(value) { this.options = []; },
    get innerHTML() { return ""; },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    removeAttribute(name) { delete this.attributes[name]; },
    getAttribute(name) { return Object.prototype.hasOwnProperty.call(this.attributes, name) ? this.attributes[name] : null; }
  };
}
[
  "zakat-form","z-currency","z-nisab-method","z-cash","z-bank","z-savings","z-gold","z-silver","z-investments","z-businesscash","z-stock","z-recv","z-pension","z-crypto","z-property","z-debts","z-paid","z-silverprice","z-goldprice","z-hawl","zakat-result",
  "bmi-form","bmi-unit","bmi-height-cm","bmi-height-ftin","bmi-metric","bmi-imperial",
  "b-kg","b-kg-error","b-lb","b-lb-error","bmi-weight-kg","bmi-weight-lb","bmi-weight-kg-group","bmi-weight-lb-group","b-cm","b-cm-error","b-ft","b-ft-error","b-in","b-in-error","bmi-result",
  "pl-form","pl-business-fields","pl-product-fields","p-revenue","p-cogs","p-expenses","p-cost","p-sell","pl-result","age-form","a-dob","age-result","disc-form","d-price","d-pct","disc-result",
  "conv-form","u-cat","u-val","u-from","u-to","conv-result","t-count","t-target","t-progress","t-tap","t-reset",
  "sw-display","sw-start","sw-stop","sw-reset",
  "years-days-form","yd-direction","yd-value","yd-value-label","yd-method","yd-calendar-option","yd-exact-fields","yd-start-date","yd-submit","yd-result","extra-result","calorie-result","qt-result","calc-display"
].forEach(id => element(id));
element("pl-mode-business").value = "business";
element("pl-mode-product").value = "product";
elements["pl-mode-business"].checked = true;
elements["pl-mode-product"].checked = false;
elements["z-currency"].value = "PKR";
elements["z-nisab-method"].value = "silver";
elements["u-cat"].value = "weight";
elements["bmi-unit"].value = "metric";
elements["bmi-height-cm"].checked = true;
elements["bmi-height-ftin"].checked = false;
elements["bmi-weight-kg"].checked = true;
elements["bmi-weight-lb"].checked = false;
elements["yd-direction"].value = "years-to-days";
elements["yd-value"].value = "80";
elements["yd-method"].value = "365";
elements["yd-calendar-option"].value = "calendar";
const storage = new Map();
let clock = 0;
const NativeDate = Date;
let fixedNow = "2026-10-18T12:00:00Z";
class FixedDate extends NativeDate {
  constructor(...args) { super(...(args.length ? args : [fixedNow])); }
  static UTC(...args) { return NativeDate.UTC(...args); }
}
const document = {
  documentElement: { lang: "en", classList: { contains: () => false, toggle() {} } },
  addEventListener(type, fn) { if (type === "DOMContentLoaded") handlers.ready = fn; },
  getElementById(id) { return elements[id] || null; },
  querySelectorAll(selector) {
    if (selector === 'input[name="pl-mode"]') return [elements["pl-mode-business"], elements["pl-mode-product"]];
    return selector && selector.includes("-result") ? Object.values(elements).filter(el => el.id && el.id.endsWith("-result")) : [];
  },
  querySelector(selector) { return selector === "#tool-calculator #calc-display" ? elements["calc-display"] : null; },
  title: "CalculatesAll Test",
  createElement(tag) { return { tag, value: "", textContent: "", hidden: false, attributes: {}, _handlers: {}, className: "", style: {}, addEventListener(type, fn) { this._handlers[type] = fn; }, setAttribute(name, value) { this.attributes[name] = String(value); }, select() {} }; },
  body: { appendChild(node) { node.parentNode = this; }, removeChild(node) { node.parentNode = null; } },
  execCommand(command) { window.legacyCopied = command === "copy"; return window.legacyCopied; }
};
class FakeMutationObserver { constructor(callback) { this.callback = callback; observers.push(this); } observe(target) { this.target = target; } disconnect() {} }
const window = { location: { href: "https://calculateallinone.vercel.app/bmi-calculator/" }, navigator: { async share(data) { window.sharedData = data; } , clipboard: { async writeText(text) { window.copiedText = text; } } }, localStorage: { getItem(k) { return storage.has(k) ? storage.get(k) : null; }, setItem(k,v) { storage.set(k,String(v)); } } };
elements["calc-display"].textContent = "0";
const context = {
  document, window, console, isFinite, Number, String, Math, Date: FixedDate, MutationObserver: FakeMutationObserver,
  setInterval(fn) { handlers.interval = fn; return 1; },
  clearInterval() {},
  performance: { now: () => clock }
};
vm.runInNewContext(fs.readFileSync("static/zakat-calculator.js", "utf8"), context, { filename: "static/zakat-calculator.js" });
vm.runInNewContext(fs.readFileSync("static/app.js", "utf8"), context, { filename: "static/app.js" });
handlers.ready();
function submit(form) {
  let prevented = false;
  elements[form]._handlers.submit({ preventDefault() { prevented = true; } });
  return prevented;
}
function setValues(values) { for (const [id, value] of Object.entries(values)) elements[id].value = String(value); }

// Years to days and days to years: both directions, method switching and validation.
assert.equal(elements["yd-value-label"].textContent, "Number of years");
assert.equal(elements["yd-submit"].textContent, "Convert Years");
assert.equal(elements["yd-exact-fields"].hidden, true);
assert.equal(elements["yd-start-date"].disabled, true);
setValues({"yd-value":80,"yd-method":365}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /80 years = 29,200 days/);
setValues({"yd-value":80,"yd-method":365.2425}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /29,219\.4 days/);
setValues({"yd-value":80,"yd-method":365.25}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /80 years = 29,220 days/);
elements["yd-value"].value = "4";
elements["yd-method"].value = "calendar";
elements["yd-start-date"].value = "2024-01-01";
elements["yd-method"]._handlers.change();
assert.equal(elements["yd-exact-fields"].hidden, false);
assert.equal(elements["yd-start-date"].disabled, false);
submit("years-days-form");
assert.match(elements["yd-result"].textContent, /1,461 days/);
elements["yd-direction"].value = "days-to-years";
elements["yd-direction"]._handlers.change();
assert.equal(elements["yd-method"].value, "365.2425", "reverse mode must replace the exact calendar-only method");
assert.equal(elements["yd-calendar-option"].disabled, true);
assert.equal(elements["yd-exact-fields"].hidden, true);
assert.equal(elements["yd-start-date"].disabled, true);
assert.equal(elements["yd-value-label"].textContent, "Number of days");
assert.equal(elements["yd-submit"].textContent, "Convert Days");
setValues({"yd-value":1009}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /1,009 days = 2\.76254817 years/);
elements["yd-method"].value = "365";
submit("years-days-form");
assert.match(elements["yd-result"].textContent, /2\.76438356 years/);
elements["yd-method"].value = "365.25";
submit("years-days-form");
assert.match(elements["yd-result"].textContent, /2\.76249144 years/);
setValues({"yd-value":1188,"yd-method":365.2425});
submit("years-days-form");
assert.match(elements["yd-result"].textContent, /Approximate breakdown: 3 years, 3 months and 0\.96 days/);
assert.match(elements["yd-result"].textContent, /average month: 30\.436875 days/);
setValues({"yd-value":1009,"yd-method":365.2425}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /Approximate breakdown: 2 years, 9 months and 4\.58 days/);
setValues({"yd-value":-1}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /Enter a number of days from 0 to 1,000,000/);
elements["yd-method"].value = "calendar";
submit("years-days-form");
assert.match(elements["yd-result"].textContent, /choose a 365-day year, 365\.25-day Julian average or Gregorian-average year/i);
elements["yd-direction"].value = "years-to-days";
elements["yd-direction"]._handlers.change();
assert.equal(elements["yd-calendar-option"].disabled, false);
assert.equal(elements["yd-value-label"].textContent, "Number of years");
assert.equal(elements["yd-submit"].textContent, "Convert Years");

// Profit and Loss: exercise the actual submit handler and reject invalid values.
elements["pl-mode-business"].checked = true;
elements["pl-mode-product"].checked = false;
elements["pl-mode-business"]._handlers.change();
const openingInventory = 20000, purchases = 50000, closingInventory = 25000;
const exampleCogs = openingInventory + purchases - closingInventory;
assert.equal(exampleCogs, 45000);
setValues({"p-revenue":100000,"p-cogs":exampleCogs,"p-expenses":0});
submit("pl-form");
assert.match(elements["pl-result"].textContent, /Gross profit\/loss: 55,000/);
assert.match(elements["pl-result"].textContent, /Net operating profit\/loss: 55,000/);
assert.match(elements["pl-result"].textContent, /Net operating margin: 55\.00%/);
for (const invalid of ["", -1, "not-a-number", 1e309]) {
  setValues({"p-revenue":invalid,"p-cogs":45000,"p-expenses":0});
  submit("pl-form");
  assert.match(elements["pl-result"].textContent, /zero or positive numbers/i);
}

// Exact Zakat worked-example unit cases from the approved silver Nisab input.
const zakatBelowExample = context.window.ZakatCalculator.calculate({
  currency:"PKR", nisabMethod:"silver", silverPricePerGram:3000, goldPricePerGram:1,
  assets:{cash:700000}, liabilities:0, zakatPaid:0, hawlComplete:true
});
assert.equal(zakatBelowExample.nisabThreshold, 1837080);
assert.equal(zakatBelowExample.zakatBeforePaid, 0);
const zakatDueExample = context.window.ZakatCalculator.calculate({
  currency:"PKR", nisabMethod:"silver", silverPricePerGram:3000, goldPricePerGram:1,
  assets:{cash:2000000}, liabilities:0, zakatPaid:0, hawlComplete:true
});
assert.equal(zakatDueExample.nisabThreshold, 1837080);
assert.equal(zakatDueExample.zakatBeforePaid, 50000);

// Deterministic randomized checks against the real calculator handlers and the Zakat engine.
let prioritySeed = 20261116;
function priorityRandom() {
  prioritySeed ^= prioritySeed << 13; prioritySeed ^= prioritySeed >>> 17; prioritySeed ^= prioritySeed << 5;
  return (prioritySeed >>> 0) / 4294967296;
}
function priorityInt(min, max) { return min + Math.floor(priorityRandom() * (max - min + 1)); }
let bmiCases = 0, profitCases = 0, zakatCases = 0;
for (let i = 0; i < 1000; i++) {
  // BMI: 800 valid values and 200 empty/zero/negative/oversized inputs.
  if (i < 800) {
    const kg = priorityInt(2000, 30000) / 100;
    const cm = priorityInt(5000, 26000) / 100;
    setValues({"b-kg":kg,"b-cm":cm});
    submit("bmi-form");
    const expected = (kg / Math.pow(cm / 100, 2)).toFixed(1);
    assert.match(elements["bmi-result"].textContent, new RegExp(expected.replace(".", "\\.") ));
  } else {
    const bad = ["", 0, -1, 999999][i % 4];
    setValues({"b-kg":bad,"b-cm":170});
    submit("bmi-form");
    assert.equal(elements["bmi-result"].textContent, "");
  }
  bmiCases++;

  // Profit and Loss: compare output to independent arithmetic, including invalid edge cases.
  if (i < 800) {
    const revenue = priorityInt(0, 100000000);
    const cogs = priorityInt(0, 100000000);
    const expenses = priorityInt(0, 100000000);
    setValues({"p-revenue":revenue,"p-cogs":cogs,"p-expenses":expenses});
    submit("pl-form");
    const gross = revenue - cogs, net = gross - expenses;
    assert.ok(elements["pl-result"].textContent.includes(gross.toLocaleString("en-US")));
    assert.ok(elements["pl-result"].textContent.includes(net.toLocaleString("en-US")));
    const margin = revenue === 0 ? "N/A (revenue is zero)" : (net / revenue * 100).toFixed(2) + "%";
    assert.ok(elements["pl-result"].textContent.includes(margin));
  } else {
    const bad = ["", -1, "invalid", 1e309][i % 4];
    setValues({"p-revenue":bad,"p-cogs":0,"p-expenses":0});
    submit("pl-form");
    assert.match(elements["pl-result"].textContent, /zero or positive numbers/i);
  }
  profitCases++;

  // Zakat: 800 valid threshold outcomes and 200 invalid empty/zero/negative/oversized inputs.
  if (i < 800) {
    const price = priorityInt(1, 10000);
    const threshold = 612.36 * price;
    const net = i % 2 === 0 ? Math.max(0, Math.floor(threshold - 1)) : Math.ceil(threshold + priorityInt(0, 1000000));
    const result = context.window.ZakatCalculator.calculate({
      currency:"PKR", nisabMethod:"silver", silverPricePerGram:price, goldPricePerGram:1,
      assets:{cash:net}, liabilities:0, zakatPaid:0, hawlComplete:true
    });
    if (net < threshold) assert.equal(result.zakatBeforePaid, 0);
    else assert.equal(result.zakatBeforePaid, net * 0.025);
  } else {
    const invalidCase = (i - 800) % 4;
    if (invalidCase === 2) {
      const emptyAsset = context.window.ZakatCalculator.calculate({
        currency:"PKR", nisabMethod:"silver", silverPricePerGram:3000, goldPricePerGram:1,
        assets:{cash:""}, liabilities:0, zakatPaid:0, hawlComplete:true
      });
      assert.equal(emptyAsset.totalAssets, 0, "empty amount must be treated as zero");
      assert.equal(emptyAsset.zakatBeforePaid, 0);
    } else {
      const input = {
        currency:"PKR", nisabMethod:"silver",
        silverPricePerGram: invalidCase === 1 ? 0 : 3000,
        goldPricePerGram:1,
        assets:{cash: invalidCase === 0 ? -1 : Number.MAX_VALUE,
                bank: invalidCase === 3 ? Number.MAX_VALUE : 0},
        liabilities:0, zakatPaid:0, hawlComplete:true
      };
      assert.throws(() => context.window.ZakatCalculator.calculate(input), /must be|valid|supported|range|metal price/i);
    }
  }
  zakatCases++;
}
assert.equal(bmiCases, 1000);
assert.equal(profitCases, 1000);
assert.equal(zakatCases, 1000);
console.log("PASS: 1,000 BMI, 1,000 Profit and Loss, and 1,000 Zakat deterministic randomized cases (seed 20261116)");

// Zakat: reject invalid negative input before the representative outcomes.
setValues({"z-cash":-1,"z-silverprice":1}); submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /zero or greater/i, "negative zakatable amounts must be rejected");
setValues({"z-cash":500,"z-silverprice":1}); submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /below the threshold/i);
setValues({"z-cash":1000,"z-silverprice":1}); elements["z-hawl"].checked = false; submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /lunar Zakat year/i);
elements["z-hawl"].checked = true; submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /2\.5 percent.*25/i);

// Global currency, gold Nisab, expanded assets, prior payment and transparent result breakdown.
setValues({
  "z-cash": 100000, "z-bank": 50000, "z-savings": 0, "z-debts": 10000,
  "z-goldprice": 1000, "z-paid": 1000
});
elements["z-currency"].value = "USD";
elements["z-nisab-method"].value = "gold-87";
elements["z-hawl"].checked = true;
submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /2\.5 percent/i);
assert.match(elements["zakat-result"].textContent, /Assets:/i);
assert.match(elements["zakat-result"].textContent, /Eligible liabilities:/i);
assert.match(elements["zakat-result"].textContent, /Remaining balance:/i);
assert.match(elements["zakat-result"].textContent, /2,500/);
elements["z-currency"].value = "ZZZ";
submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /three-letter ISO currency code/i);


// BMI: kg/lb weight units, cm/ft-in height, category boundaries, invalid input and hidden fields.
assert.equal(elements["b-cm"].disabled, false);
assert.equal(elements["b-ft"].disabled, true);
assert.equal(elements["b-in"].disabled, true);
assert.equal(elements["b-lb"].disabled, true);
setValues({"b-kg":70,"b-cm":170,"b-ft":"5abc","b-in":"12"});
assert.equal(submit("bmi-form"), true, "form submit must prevent browser navigation/reload");
assert.match(elements["bmi-result"].textContent, /24\.2.*normal weight/i);
assert.match(elements["bmi-result"].textContent, /BMI is a general screening tool/i);
assert.match(elements["bmi-result"].textContent, /category is based on the unrounded BMI value/i, "BMI result must explain that category uses the unrounded value");
assert.equal(elements["b-ft-error"].textContent, "", "disabled hidden feet field must not be validated");
for (const [kg, cm, expected, label] of [
  [63.25,170,"21.9","normal weight"],[70,170,"24.2","normal weight"],
  [53.4,170,"18.5","underweight"], // 18.4775 rounds to 18.5 but remains below the exact 18.5 threshold.
  [72.2,170,"25.0","normal weight"], // 24.9827 rounds to 25.0 but remains below the exact 25 threshold.
  [86.6,170,"30.0","overweight"], // 29.9654 rounds to 30.0 but remains below the exact 30 threshold.
  [72.25,170,"25.0","overweight"],[86.7,170,"30.0","obesity"]
]) {
  setValues({"b-kg":kg,"b-cm":cm}); submit("bmi-form");
  assert.match(elements["bmi-result"].textContent, new RegExp(expected.replace(".","\\.") + ".*" + label, "i"));
}
elements["bmi-height-ftin"].checked = true;
elements["bmi-height-cm"].checked = false;
elements["bmi-height-ftin"]._handlers.change();
assert.equal(elements["bmi-result"].textContent, "", "changing height unit clears result");
assert.equal(elements["b-cm"].disabled, true);
assert.equal(elements["b-ft"].disabled, false);
assert.equal(elements["b-in"].disabled, false);
setValues({"b-kg":70,"b-ft":5,"b-in":7}); submit("bmi-form");
assert.match(elements["bmi-result"].textContent, /24\.2.*normal weight/i);
elements["bmi-weight-lb"].checked = true;
elements["bmi-weight-kg"].checked = false;
elements["bmi-weight-lb"]._handlers.change();
assert.equal(elements["bmi-result"].textContent, "", "changing weight unit clears result");
assert.equal(elements["b-kg"].disabled, true);
assert.equal(elements["b-lb"].disabled, false);
setValues({"b-lb":154.324,"b-ft":5,"b-in":7}); submit("bmi-form");
assert.match(elements["bmi-result"].textContent, /24\.2.*normal weight/i, "pounds input should calculate equivalent BMI");
elements["bmi-height-cm"].checked = true;
elements["bmi-height-ftin"].checked = false;
elements["bmi-height-cm"]._handlers.change();
assert.equal(elements["b-ft"].disabled, true, "switching back to centimetres must disable feet");
setValues({"b-lb":154.324,"b-cm":170}); submit("bmi-form");
assert.match(elements["bmi-result"].textContent, /24\.2.*normal weight/i, "pounds with centimetres should calculate equivalent BMI");
elements["bmi-height-ftin"].checked = true;
elements["bmi-height-cm"].checked = false;
elements["bmi-height-ftin"]._handlers.change();
setValues({"b-lb":"5abc","b-ft":5,"b-in":7}); submit("bmi-form");
assert.notEqual(elements["b-lb-error"].textContent, "", "malformed pounds input must be rejected");
setValues({"b-lb":154.324,"b-ft":5,"b-in":7}); submit("bmi-form");
assert.match(elements["bmi-result"].textContent, /24\.2.*normal weight/i);
elements["bmi-weight-kg"].checked = true;
elements["bmi-weight-lb"].checked = false;
elements["bmi-weight-kg"]._handlers.change();
assert.equal(elements["b-lb"].disabled, true);
assert.equal(elements["b-kg"].disabled, false);
setValues({"b-kg":90,"b-ft":6,"b-in":0}); submit("bmi-form");
assert.match(elements["bmi-result"].textContent, /26\.9.*overweight/i);
setValues({"b-kg":70,"b-ft":5,"b-in":11.99}); submit("bmi-form");
assert.match(elements["bmi-result"].textContent, /20\.9.*normal weight/i);
for (const [ft, inches, expectedField] of [
  [0,5,"b-ft-error"],[9,0,"b-ft-error"],["5abc",7,"b-ft-error"],["0x5",7,"b-ft-error"],["1e1",7,"b-ft-error"],[5,12,"b-in-error"]
]) {
  setValues({"b-kg":70,"b-ft":ft,"b-in":inches}); submit("bmi-form");
  assert.notEqual(elements[expectedField].textContent, "", "invalid height must show a field-specific error: " + ft + " ft " + inches + " in");
  assert.doesNotMatch(elements["bmi-result"].textContent, /NaN|Infinity/);
}
for (const weight of [19.9,300.1,""]) {
  setValues({"b-kg":weight,"b-ft":5,"b-in":7}); submit("bmi-form");
  assert.notEqual(elements["b-kg-error"].textContent, "", "invalid weight must show a weight-specific error");
}
setValues({"b-kg":70,"b-ft":"","b-in":7}); submit("bmi-form");
assert.notEqual(elements["b-ft-error"].textContent, "", "empty feet must be rejected");
setValues({"b-kg":70,"b-ft":5,"b-in":""}); submit("bmi-form");
assert.notEqual(elements["b-in-error"].textContent, "", "empty inches must be rejected");

// Restore the pre-existing product-mode state after the randomized business-mode simulation.
elements["pl-mode-product"].checked = true;
elements["pl-mode-business"].checked = false;
elements["pl-mode-product"]._handlers.change();

// Profit/loss: profit, loss and zero-cost edge case.
for (const [cost, sell, expected] of [[100,150,/Profit: 50/],[100,80,/Loss: 20/],[0,10,/N\/A/]]) {
  setValues({"p-cost":cost,"p-sell":sell}); submit("pl-form");
  assert.match(elements["pl-result"].textContent, expected);
}

// Product profit now shows margin (selling-price denominator) separately from markup (cost denominator).
for (const [cost, sell, margin] of [
  [100, 150, /Margin on selling price: 33\.33%/],
  [100, 80, /Margin on selling price: -25\.00%/],
  [0, 10, /Margin on selling price: 100\.00%/],
  [10, 0, /Margin on selling price: N\/A/]
]) {
  setValues({"p-cost":cost,"p-sell":sell}); submit("pl-form");
  assert.match(elements["pl-result"].textContent, margin);
}
setValues({"p-cost":0,"p-sell":10}); submit("pl-form");
assert.match(elements["pl-result"].textContent, /Markup is N\/A because cost price is zero\./, "zero cost must identify markup as unavailable");
setValues({"p-cost":100,"p-sell":150}); submit("pl-form");
assert.match(elements["pl-result"].textContent, /50\.00 percent of cost price/, "markup remains on cost base");

setValues({"p-cost":-1,"p-sell":100}); submit("pl-form");
assert.match(elements["pl-result"].textContent, /cost price.*zero or more/i, "negative cost must be rejected");

// Age: three fixed-calendar examples and future-date rejection.
for (const [dob, expected] of [
  ["2000-01-01",/26 years, 9 months and 17 days/],
  ["2020-02-29",/6 years, 7 months and 19 days/],
  ["1980-12-31",/45 years, 9 months and 18 days/]
]) {
  elements["a-dob"].value = dob; submit("age-form");
  assert.match(elements["age-result"].textContent, expected);
}
fixedNow = "2025-02-27T12:00:00Z";
elements["a-dob"].value = "2000-02-29"; submit("age-form");
assert.match(elements["age-result"].textContent, /24 years, 11 months and 29 days/, "29 February birth stays one day short of the 28 February anniversary");
fixedNow = "2025-02-28T12:00:00Z";
submit("age-form");
assert.match(elements["age-result"].textContent, /25 years, 0 months and 0 days/, "This calculator uses 28 February as the non-leap-year anniversary");
fixedNow = "2025-03-01T12:00:00Z";
submit("age-form");
assert.match(elements["age-result"].textContent, /25 years, 0 months and 1 day/, "Age remains one day past the calculator anniversary on 1 March");
fixedNow = "2026-10-18T12:00:00Z";
elements["a-dob"].value = "2027-01-01"; submit("age-form");
assert.match(elements["age-result"].textContent, /future/i);

// Discount: standard, zero discount and full discount.
for (const [price, pct, saved, final] of [[1000,20,"200","800"],[50,0,"0","50"],[100,100,"100","0"]]) {
  setValues({"d-price":price,"d-pct":pct}); submit("disc-form");
  assert.match(elements["disc-result"].textContent, new RegExp("save " + saved.replace(".","\\.") + "\\."));
  assert.match(elements["disc-result"].textContent, new RegExp("Final price: " + final.replace(".","\\.") + "\\."));
}

setValues({"d-price":100,"d-pct":101}); submit("disc-form");
assert.match(elements["disc-result"].textContent, /discount from 0 to 100 percent/i, "discounts above 100 percent must be rejected");

// Unit conversion: mass, length and temperature.
for (const [cat, value, from, to, expected] of [
  ["weight",1,"kg","lb",/2\.20462/],
  ["length",1,"km","mi",/0\.621371/],
  ["temp",32,"F","C",/0\.00 Celsius/]
]) {
  elements["u-cat"].value = cat;
  elements["u-val"].value = String(value);
  elements["u-from"].value = from;
  elements["u-to"].value = to;
  submit("conv-form");
  assert.match(elements["conv-result"].textContent, expected);
}

elements["u-cat"].value = "weight"; elements["u-val"].value = "-1"; elements["u-from"].value = "kg"; elements["u-to"].value = "lb"; submit("conv-form");
assert.match(elements["conv-result"].textContent, /cannot be negative/i, "negative mass must be rejected");
elements["u-cat"].value = "temp"; elements["u-val"].value = "-300"; elements["u-from"].value = "C"; elements["u-to"].value = "F"; submit("conv-form");
assert.match(elements["conv-result"].textContent, /below absolute zero/i, "temperature below absolute zero must be rejected");

// Tasbih: three increments, target reached, reset.
elements["t-target"].value = "3";
elements["t-tap"]._handlers.click(); elements["t-tap"]._handlers.click(); elements["t-tap"]._handlers.click();
assert.equal(elements["t-count"].textContent, "3");
assert.match(elements["t-progress"].textContent, /reached/i);
elements["t-reset"]._handlers.click();
assert.equal(elements["t-count"].textContent, "0");

// Stopwatch: start, elapsed tick, stop and reset.
elements["sw-start"]._handlers.click();
clock = 1000;
elements["sw-stop"]._handlers.click();
assert.equal(elements["sw-display"].textContent, "00:00:01.00");
elements["sw-reset"]._handlers.click();
assert.equal(elements["sw-display"].textContent, "00:00:00.00");

console.log("PASS: 3+ input examples each for Zakat, BMI, profit/loss, age, discount and unit conversion; plus Tasbih, stopwatch and fixed-date validation.");


// Exact Gregorian-calendar years: leap days, century exceptions, validation and generated controls.
{
  const source = fs.readFileSync("static/app.js", "utf8");
  const start = source.indexOf("  function exactCalendarYearDays (");
  const end = source.indexOf("  function initYearsDays ()", start);
  assert.ok(start !== -1 && end > start, "Exact calendar engine must exist");
  const testContext = { Date, Math, Number, String };
  vm.runInNewContext(source.slice(start, end) + "\nthis.calculateExact = exactCalendarYearDays;", testContext);
  const exact = testContext.calculateExact;
  for (const [date,years,days,endDate,leaps] of [
    ["2024-01-01",4,1461,"2028-01-01",1],
    ["2020-02-29",1,366,"2021-03-01",1],
    ["1896-03-01",4,1460,"1900-03-01",0],
    ["1999-03-01",1,366,"2000-03-01",1],
    ["2099-03-01",1,365,"2100-03-01",0],
    ["0001-01-01",1,365,"0002-01-01",0],
    ["2024-01-01",0,0,"2024-01-01",0]
  ]) {
    const got = exact(date, years);
    assert.ok(got, "Valid calendar scenario must calculate: " + date);
    assert.equal(got.days, days, date + " days");
    assert.equal(got.endDate, endDate, date + " end date");
    assert.equal(got.leapDays, leaps, date + " leap count");
  }
  for (const [date,years] of [["2023-02-29",1],["2024-02-30",1],
    ["2024-01-01",1.5],["2024-01-01",-1],["9999-01-01",1],["",2]]) {
    assert.equal(exact(date, years), null, "Reject invalid calendar input: " + date);
  }
  const generated = fs.readFileSync("public/years-to-days-calculator/index.html", "utf8");
  assert.match(generated, /id="yd-direction"/);
  assert.match(generated, /option value="days-to-years"/);
  assert.match(generated, /id="yd-calendar-option"/);
  assert.match(generated, /Can exact calendar mode use decimal years\?/);
  assert.match(generated, /id="yd-exact-fields"/);
  assert.match(generated, /id="yd-start-date"/);
  assert.match(generated, /id="yd-calendar-option" value="calendar"/);
  assert.match(generated, /href="https:\/\/calculateallinone\.vercel\.app\/years-to-days-calculator\/"/);
  assert.match(generated, /20261115-zakat-global-1/);
  console.log("PASS: exact calendar day count, leap years, invalid dates and generated controls");
}


// Result sharing: buttons appear only when a result exists and use native share or clipboard fallback.
(async function testResultSharing() {
  const bmiShare = insertedShareButtons.find(button => button.attributes["data-share-result-for"] === "bmi-result");
  const zakatShare = insertedShareButtons.find(button => button.attributes["data-share-result-for"] === "zakat-result");
  assert.ok(bmiShare, "BMI result must have a share button");
  assert.ok(zakatShare, "Zakat result must have a share button");
  assert.ok(insertedShareButtons.some(button => button.attributes["data-share-result-for"] === "extra-result"), "Extra calculator result must have a share button");
  assert.ok(insertedShareButtons.some(button => button.attributes["data-share-result-for"] === "calorie-result"), "Calorie calculator result must have a share button");
  assert.ok(insertedShareButtons.some(button => button.attributes["data-share-result-for"] === "qt-result"), "Query calculator result must have a share button");
  const standardShare = insertedShareButtons.find(button => button.attributes["data-share-result-for"] === "calc-display");
  assert.ok(standardShare, "Standard calculator display must have a share button");
  assert.equal(standardShare.hidden, true, "Standard calculator share stays hidden at the initial zero display");
  assert.equal(bmiShare.hidden, true, "Share button stays hidden before a result exists");
  const standardObserver = observers.find(observer => observer.target === elements["calc-display"]);
  elements["calc-display"].textContent = "12";
  standardObserver.callback();
  assert.equal(standardShare.hidden, false, "Standard calculator share appears after a value is entered");
  const bmiObserver = observers.find(observer => observer.target === elements["bmi-result"]);
  assert.ok(bmiObserver, "BMI result must be observed for result changes");
  elements["bmi-result"].textContent = "BMI result: 24.2 normal weight";
  bmiObserver.callback();
  assert.equal(bmiShare.hidden, false, "Share button appears after a result is available");
  await bmiShare._handlers.click();
  assert.equal(window.sharedData.title, "CalculatesAll Test");
  assert.match(window.sharedData.text, /BMI result: 24.2 normal weight/);
  assert.equal(window.sharedData.url, "https://calculateallinone.vercel.app/bmi-calculator/");

  const zakatObserver = observers.find(observer => observer.target === elements["zakat-result"]);
  assert.ok(zakatObserver, "Zakat result must be observed for result changes");
  elements["zakat-result"].textContent = "Zakat payable: 25";
  zakatObserver.callback();
  window.navigator.share = undefined;
  await zakatShare._handlers.click();
  assert.match(window.copiedText, /Zakat payable: 25/);
  assert.match(window.copiedText, /https:\/\/calculateallinone\.vercel\.app\/bmi-calculator\//);
  window.navigator.clipboard.writeText = async function () { throw new Error("Clipboard API rejected"); };
  await zakatShare._handlers.click();
  assert.equal(window.legacyCopied, true, "legacy copy fallback must run when the Clipboard API rejects");
  console.log("PASS: result share button visibility, native share payload, Clipboard API and legacy copy fallback");
})().catch(error => { console.error(error); process.exitCode = 1; });
