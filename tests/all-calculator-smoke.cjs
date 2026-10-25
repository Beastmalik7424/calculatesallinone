const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const handlers = {};
const elements = {};
function element(id, value = "") {
  return elements[id] = {
    id, value, checked: false, disabled: false, textContent: "", options: [], selectedIndex: 0,
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
  "sw-display","sw-start","sw-stop","sw-reset"
].forEach(id => element(id));
elements["u-cat"].value = "weight";
elements["bmi-unit"].value = "metric";
elements["bmi-height-cm"].checked = true;
elements["bmi-height-ftin"].checked = false;
elements["bmi-weight-kg"].checked = true;
elements["bmi-weight-lb"].checked = false;
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
