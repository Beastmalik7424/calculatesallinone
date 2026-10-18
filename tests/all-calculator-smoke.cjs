const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const handlers = {};
const elements = {};
function element(id, value = "") {
  return elements[id] = {
    id, value, checked: false, textContent: "", options: [], selectedIndex: 0,
    _handlers: {}, classList: {
      _set: new Set(),
      toggle(name, force) { if (force === undefined ? !this._set.has(name) : force) this._set.add(name); else this._set.delete(name); },
      contains(name) { return this._set.has(name); }
    },
    addEventListener(type, fn) { this._handlers[type] = fn; },
    appendChild(option) { this.options.push(option); },
    set innerHTML(value) { this.options = []; },
    get innerHTML() { return ""; },
    setAttribute() {}
  };
}
[
  "zakat-form","z-cash","z-gold","z-silver","z-stock","z-recv","z-debts","z-silverprice","z-hawl","zakat-result",
  "bmi-form","bmi-unit","bmi-metric","bmi-imperial","b-kg","b-cm","b-lb","b-ft","b-in","bmi-result",
  "pl-form","p-cost","p-sell","pl-result","age-form","a-dob","age-result","disc-form","d-price","d-pct","disc-result",
  "conv-form","u-cat","u-val","u-from","u-to","conv-result","t-count","t-target","t-progress","t-tap","t-reset",
  "sw-display","sw-start","sw-stop","sw-reset"
].forEach(id => element(id));
elements["u-cat"].value = "weight";
elements["bmi-unit"].value = "metric";
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
function submit(form) { elements[form]._handlers.submit({ preventDefault() {} }); }
function setValues(values) { for (const [id, value] of Object.entries(values)) elements[id].value = String(value); }

// Zakat: three materially different outcomes.
setValues({"z-cash":500,"z-silverprice":1}); submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /below Nisab/i);
setValues({"z-cash":1000,"z-silverprice":1}); elements["z-hawl"].checked = false; submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /lunar year/i);
elements["z-hawl"].checked = true; submit("zakat-form");
assert.match(elements["zakat-result"].textContent, /2\.5 percent.*25/i);

// BMI: normal, overweight and obesity categories.
for (const [kg, cm, label] of [[70,175,"normal weight"],[70,160,"overweight"],[90,170,"obesity"]]) {
  setValues({"b-kg":kg,"b-cm":cm}); submit("bmi-form");
  assert.match(elements["bmi-result"].textContent, new RegExp(label, "i"));
}

// Profit/loss: profit, loss and zero-cost edge case.
for (const [cost, sell, expected] of [[100,150,/Profit: 50/],[100,80,/Loss: 20/],[0,10,/N\/A/]]) {
  setValues({"p-cost":cost,"p-sell":sell}); submit("pl-form");
  assert.match(elements["pl-result"].textContent, expected);
}

// Age: three fixed-calendar examples and future-date rejection.
for (const [dob, expected] of [
  ["2000-01-01",/26 years, 9 months and 17 days/],
  ["2020-02-29",/6 years, 7 months and 19 days/],
  ["1980-12-31",/45 years, 9 months and 17 days/]
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
