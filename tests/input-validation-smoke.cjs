const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const ids = [
  "zakat-form", "z-currency", "z-nisab-method", "z-cash", "z-bank", "z-savings", "z-gold", "z-silver", "z-investments", "z-businesscash", "z-stock", "z-recv", "z-pension", "z-crypto", "z-property", "z-debts", "z-paid", "z-silverprice", "z-goldprice", "z-hawl", "zakat-result",
  "conv-form", "u-cat", "u-val", "u-from", "u-to", "conv-result"
];
const elements = {};
for (const id of ids) {
  elements[id] = {
    id,
    value: "",
    checked: false,
    textContent: "",
    options: [],
    selectedIndex: 0,
    _handlers: {},
    addEventListener(type, fn) { this._handlers[type] = fn; },
    appendChild(option) { this.options.push(option); },
    set innerHTML(value) { this.options = []; this.value = ""; },
    get innerHTML() { return ""; }
  };
}
elements["u-cat"].value = "temp";
elements["z-currency"].value = "PKR";
elements["z-nisab-method"].value = "silver";
elements["z-cash"].value = "-1";
elements["z-silverprice"].value = "1";
elements["u-val"].value = "-300";
elements["u-from"].value = "C";
elements["u-to"].value = "K";

const handlers = {};
const document = {
  documentElement: { lang: "en", classList: { contains: () => false } },
  addEventListener(type, fn) { if (type === "DOMContentLoaded") handlers.ready = fn; },
  getElementById(id) { return elements[id] || null; },
  querySelectorAll() { return []; },
  createElement(tag) { return { tag, value: "", textContent: "" }; }
};
const context = {
  document, window: {}, console, isFinite, Number, String, Math, Date,
  setInterval, clearInterval, performance: { now: () => 0 }
};
vm.runInNewContext(fs.readFileSync("static/zakat-calculator.js", "utf8"), context, { filename: "static/zakat-calculator.js" });
vm.runInNewContext(fs.readFileSync("static/app.js", "utf8"), context, { filename: "static/app.js" });
handlers.ready();

elements["zakat-form"]._handlers.submit({ preventDefault() {} });
assert.match(elements["zakat-result"].textContent, /zero or greater/i, "negative Zakat inputs must be rejected");

elements["u-from"].value = "C";
elements["u-to"].value = "K";
elements["conv-form"]._handlers.submit({ preventDefault() {} });
assert.match(elements["conv-result"].textContent, /below absolute zero/i, "Celsius below absolute zero must be rejected");

elements["u-val"].value = "-273.15";
elements["conv-form"]._handlers.submit({ preventDefault() {} });
assert.match(elements["conv-result"].textContent, /0\.00 Kelvin/i, "absolute zero itself must remain valid");
console.log("Input validation tests passed: negative Zakat amounts and temperature limits.");
