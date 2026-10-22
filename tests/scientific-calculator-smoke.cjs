const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const handlers = {};
const elements = {};
function el(id) {
  return elements[id] = {
    id, textContent: "", hidden: false, attributes: {}, classList: {
      toggle(name, force) { this[name] = force; },
      contains(name) { return !!this[name]; }
    },
    addEventListener(type, fn) { handlers[id + ":" + type] = fn; },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    getAttribute(name) { return this.attributes[name] || null; }
  };
}
el("calc-pad");
el("calc-display");
el("scientific-pad");
el("calc-mode-toggle");
const document = {
  documentElement: { lang: "en", classList: { contains: () => false, toggle() {} } },
  addEventListener(type, fn) { if (type === "DOMContentLoaded") handlers.ready = fn; },
  getElementById(id) { return elements[id] || null; },
  querySelectorAll() { return []; }
};
const context = { document, window: {}, console, isFinite, Number, String, Math, Date, setInterval, clearInterval, performance: { now: () => 0 } };
vm.runInNewContext(fs.readFileSync("static/app.js", "utf8"), context, { filename: "static/app.js" });
handlers.ready();

function click(id, key) {
  const button = { getAttribute(name) { return name === "data-key" ? key : null; } };
  handlers[id + ":click"]({ target: { closest() { return button; } } });
}
function scientific(keys) {
  for (const key of keys) click("scientific-pad", key);
  return elements["calc-display"].textContent;
}

handlers["calc-mode-toggle:click"]();
assert.equal(elements["calc-mode-toggle"].textContent, "Standard Mode", "toggle label should offer return to standard mode");
assert.equal(elements["scientific-pad"].hidden, false, "scientific keypad should be shown in scientific mode");
assert.equal(scientific(["sin", "3", "0", ")"]), "0.5", "sin(30) in DEG mode should equal 0.5");
click("scientific-pad", "C");
assert.equal(scientific(["sqrt", "9", ")"]), "3", "scientific square root should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["log", "1", "0", ")"]), "1", "base-10 logarithm should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["2", "^", "3"]), "8", "exponentiation should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["5", "!"]), "120", "factorial should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["1", "/", "0"]), "Cannot divide by zero", "division by zero must show a safe error");
handlers["calc-mode-toggle:click"]();
assert.equal(elements["scientific-pad"].hidden, true, "scientific keypad should be hidden in standard mode");
assert.equal(elements["calc-mode-toggle"].textContent, "Scientific Mode", "toggle label should offer scientific mode");
console.log("Scientific calculator tests passed.");
