const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const handlers = {};
const elements = {
  "calc-pad": {
    addEventListener(type, fn) { handlers[type] = fn; }
  },
  "calc-display": { textContent: "0" }
};
const document = {
  documentElement: { lang: "en", classList: { contains: () => false } },
  addEventListener(type, fn) { if (type === "DOMContentLoaded") handlers.ready = fn; },
  getElementById(id) { return elements[id] || null; },
  querySelectorAll() { return []; }
};
const context = {
  document,
  window: {},
  console,
  isFinite,
  Number,
  String,
  Math,
  Date,
  setInterval,
  clearInterval,
  performance: { now: () => 0 }
};
vm.runInNewContext(fs.readFileSync("static/app.js", "utf8"), context, { filename: "static/app.js" });
handlers.ready();

function press(key) {
  const button = { getAttribute(name) { return name === "data-key" ? key : null; } };
  handlers.click({ target: { closest() { return button; } } });
}
function enter(keys) {
  press("C");
  for (const key of keys) press(key);
  press("=");
  return elements["calc-display"].textContent;
}

assert.equal(enter([".", "5"]), "0.5", "leading decimal must be parsed as a fraction");
assert.equal(enter(["2", "+", "3", "*", "4"]), "14", "multiplication must precede addition");
assert.equal(enter(["2", "*", "(", "3", "+", "4", ")"]), "14", "parentheses must group expressions");
assert.equal(enter(["1", "/", "0"]), "Cannot divide by zero", "division by zero must show a safe error");
assert.equal(enter(["9", "sqrt"]), "3", "square root of a perfect square must calculate correctly");
assert.equal(enter(["2", "+", "7", "sqrt"]), "3", "square root applies to the current expression");
press("C");
press("-");
press("9");
press("sqrt");
assert.equal(elements["calc-display"].textContent, "Square root of a negative number is not a real number.", "negative square root must show a clear error");
press("C");
press("sqrt");
assert.equal(elements["calc-display"].textContent, "Enter a number or expression first.", "square root without input must show a clear prompt");
console.log("Calculator behavior tests passed: decimals, precedence, parentheses, divide-by-zero, square root and invalid root inputs.");
