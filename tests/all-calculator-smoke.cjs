const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const handlers = {};
const elements = {};
function element(id, value = "") {
  return elements[id] = {
    id, value, checked: false, disabled: false, hidden: false, textContent: "", options: [], selectedIndex: 0,
    attributes: {}, _handlers: {}, classList: {
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
  "zakat-form","z-cash","z-gold","z-silver","z-stock","z-recv","z-debts","z-silverprice","z-hawl","zakat-result",
  "bmi-form","bmi-unit","bmi-height-cm","bmi-height-ftin","bmi-metric","bmi-imperial",
  "b-kg","b-kg-error","b-lb","b-lb-error","bmi-weight-kg","bmi-weight-lb","bmi-weight-kg-group","bmi-weight-lb-group","b-cm","b-cm-error","b-ft","b-ft-error","b-in","b-in-error","bmi-result",
  "pl-form","p-cost","p-sell","pl-result","age-form","a-dob","age-result","disc-form","d-price","d-pct","disc-result",
  "conv-form","u-cat","u-val","u-from","u-to","conv-result","t-count","t-target","t-progress","t-tap","t-reset",
  "sw-display","sw-start","sw-stop","sw-reset",
  "years-days-form","yd-direction","yd-value","yd-value-label","yd-method","yd-calendar-option","yd-exact-fields","yd-start-date","yd-submit","yd-result"
].forEach(id => element(id));
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
class FixedDate extends NativeDate {
  constructor(...args) { super(...(args.length ? args : ["2026-10-18T12:00:00Z"])); }
  static UTC(...args) { return NativeDate.UTC(...args); }
}
const document = {
  documentElement: { lang: "en", classList: { contains: () => false, toggle() {} } },
  addEventListener(type, fn) { if (type === "DOMContentLoaded") handlers.ready = fn; },
  getElementById(id) { return elements[id] || null; },
  querySelectorAll() { return []; },
  createElement(tag) { return { tag, value: "", textContent: "" }; }
};
const window = { localStorage: { getItem(k) { return storage.has(k) ? storage.get(k) : null; }, setItem(k,v) { storage.set(k,String(v)); } } };
const context = {
  document, window, console, isFinite, Number, String, Math, Date: FixedDate,
  setInterval(fn) { handlers.interval = fn; return 1; },
  clearInterval() {},
  performance: { now: () => clock }
};
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
setValues({"yd-value":-1}); submit("years-days-form");
assert.match(elements["yd-result"].textContent, /Enter a number of days from 0 to 1,000,000/);
elements["yd-method"].value = "calendar";
submit("years-days-form");
assert.match(elements["yd-result"].textContent, /choose a 365-day or Gregorian-average year/i);
elements["yd-direction"].value = "years-to-days";
elements["yd-direction"]._handlers.change();
assert.equal(elements["yd-calendar-option"].disabled, false);
assert.equal(elements["yd-value-label"].textContent, "Number of years");
assert.equal(elements["yd-submit"].textContent, "Convert Years");

// Zakat: reject invalid negative input before the representative outcomes.
setValues({"z-cash":-1,"z-silverprice":1}); submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /zero or a positive value/i, "negative zakatable amounts must be rejected");
setValues({"z-cash":500,"z-silverprice":1}); submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /below Nisab/i);
setValues({"z-cash":1000,"z-silverprice":1}); elements["z-hawl"].checked = false; submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /lunar year/i);
elements["z-hawl"].checked = true; submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /2\.5 percent.*25/i);

// BMI: kg/lb weight units, cm/ft-in height, category boundaries, invalid input and hidden fields.
assert.equal(elements["b-cm"].disabled, false);
assert.equal(elements["b-ft"].disabled, true);
assert.equal(elements["b-in"].disabled, true);
assert.equal(elements["b-lb"].disabled, true);
setValues({"b-kg":70,"b-cm":170,"b-ft":"5abc","b-in":"12"});
assert.equal(submit("bmi-form"), true, "form submit must prevent browser navigation/reload");
assert.match(elements["bmi-result"].textContent, /24\.2.*normal weight/i);
assert.match(elements["bmi-result"].textContent, /BMI is a general screening tool/i);
assert.equal(elements["b-ft-error"].textContent, "", "disabled hidden feet field must not be validated");
for (const [kg, cm, expected, label] of [
  [63.25,170,"21.9","normal weight"],[70,170,"24.2","normal weight"],
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
  assert.match(generated, /How many years is 1,009 days\?/);
  assert.match(generated, /id="yd-exact-fields"/);
  assert.match(generated, /id="yd-start-date"/);
  assert.match(generated, /id="yd-calendar-option" value="calendar"/);
  assert.match(generated, /href="https:\/\/calculateallinone\.vercel\.app\/years-to-days-calculator\/"/);
  assert.match(generated, /20261030-exact-years-1/);
  console.log("PASS: exact calendar day count, leap years, invalid dates and generated controls");
}
