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
  addEventListener(type, fn) { if (type === "DOMContentLoaded") handlers.ready = fn; else if (type === "keydown") handlers.keydown = fn; },
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
  click("scientific-pad", "=");
  return elements["calc-display"].textContent;
}

handlers["calc-mode-toggle:click"]();
assert.equal(elements["calc-mode-toggle"].textContent, "Standard Mode", "toggle label should offer return to standard mode");
assert.equal(elements["scientific-pad"].hidden, false, "scientific keypad should be shown in scientific mode");
assert.equal(scientific(["sin", "3", "0", ")"]), "0.5", "sin(30) in DEG mode should equal 0.5");
click("scientific-pad", "C");
click("scientific-pad", "angle-toggle");
assert.equal(scientific(["sin", "pi", "/", "2", ")"]), "1", "sin(pi/2) in RAD mode should equal 1");
click("scientific-pad", "C");
click("scientific-pad", "angle-toggle");
assert.equal(scientific(["asin", "0.5", ")"]), "30", "inverse sine should return degrees in DEG mode");
click("scientific-pad", "C");
assert.equal(scientific(["sqrt", "9", ")"]), "3", "scientific square root should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["log", "1", "0", ")"]), "1", "base-10 logarithm should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["2", "^", "3"]), "8", "exponentiation should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["2", "^", "-", "2"]), "0.25", "negative exponents should be supported");
click("scientific-pad", "C");
assert.equal(scientific(["root", "3", ",", "8", ")"]), "2", "nth root should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["mean", "1", ",", "2", ",", "3", ")"]), "2", "mean should evaluate multiple values");
click("scientific-pad", "C");
assert.equal(scientific(["stdevp", "2", ",", "4", ")"]), "1", "population standard deviation should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["nCr", "5", ",", "2", ")"]), "10", "combinations should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["log", "8", ",", "2", ")"]), "3", "logarithm with a custom base should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["Ans", "+", "3"]), "6", "Ans should use the previous result");
click("scientific-pad", "C");
assert.equal(scientific(["log", "-", "1", ")"]), "Math domain error", "logarithm domain errors should be explained");
click("scientific-pad", "C");
assert.equal(scientific(["2", "+", "3"]), "5", "memory test value should calculate");
click("scientific-pad", "M+");
click("scientific-pad", "C");
assert.equal(scientific(["MR"]), "5", "memory recall should restore the stored value");
click("scientific-pad", "MC");
click("scientific-pad", "C");
assert.equal(scientific(["5", "!"]), "120", "factorial should evaluate");
click("scientific-pad", "C");
assert.equal(scientific(["1", "/", "0"]), "Cannot divide by zero", "division by zero must show a safe error");

function checkScientific(keys, expected, label) {
  click("scientific-pad", "C");
  const actual = scientific(keys);
  assert.equal(actual, expected, label);
}
checkScientific(["cos", "6", "0", ")"], "0.5", "cos(60) in DEG mode");
checkScientific(["tan", "4", "5", ")"], "1", "tan(45) in DEG mode");
checkScientific(["acos", "1", ")"], "0", "inverse cosine in DEG mode");
checkScientific(["atan", "1", ")"], "45", "inverse tangent in DEG mode");
checkScientific(["acsc", "2", ")"], "30", "inverse cosecant in DEG mode");
checkScientific(["asec", "2", ")"], "60", "inverse secant in DEG mode");
checkScientific(["acot", "1", ")"], "45", "inverse cotangent in DEG mode");
checkScientific(["sec", "6", "0", ")"], "2", "secant in DEG mode");
checkScientific(["csc", "3", "0", ")"], "2", "cosecant in DEG mode");
checkScientific(["cot", "4", "5", ")"], "1", "cotangent in DEG mode");
checkScientific(["cbrt", "2", "7", ")"], "3", "cube root");
checkScientific(["3", "square"], "9", "square shortcut");
checkScientific(["3", "cube"], "27", "cube shortcut");
checkScientific(["tenpow", "2", ")"], "100", "10 to a power shortcut");
checkScientific(["reciprocal", "4", ")"], "0.25", "reciprocal shortcut");
checkScientific(["sinh", "0", ")"], "0", "hyperbolic sine");
checkScientific(["cosh", "0", ")"], "1", "hyperbolic cosine");
checkScientific(["tanh", "0", ")"], "0", "hyperbolic tangent");
checkScientific(["csch", "1", ")"], "0.850918128239", "hyperbolic cosecant");
checkScientific(["sech", "0", ")"], "1", "hyperbolic secant");
checkScientific(["coth", "1", ")"], "1.313035285499", "hyperbolic cotangent");
checkScientific(["abs", "-", "5", ")"], "5", "absolute value");
checkScientific(["floor", "2", ".", "8", ")"], "2", "floor");
checkScientific(["ceil", "2", ".", "2", ")"], "3", "ceiling");
checkScientific(["round", "2", ".", "6", ")"], "3", "round");
checkScientific(["nPr", "5", ",", "2", ")"], "20", "permutations");
checkScientific(["mod", "7", ",", "4", ")"], "3", "modulo");
checkScientific(["median", "1", ",", "3", ",", "2", ")"], "2", "median");
checkScientific(["stdev", "2", ",", "4", ")"], "1.414213562373", "sample standard deviation");
checkScientific(["var", "2", ",", "4", ")"], "2", "sample variance");
checkScientific(["varp", "2", ",", "4", ")"], "1", "population variance");
checkScientific(["min", "-", "2", ",", "5", ")"], "-2", "minimum");
checkScientific(["max", "-", "2", ",", "5", ")"], "5", "maximum");
checkScientific(["sum", "1", ",", "2", ",", "3", ")"], "6", "sum");
checkScientific(["gcd", "1", "2", ",", "1", "8", ")"], "6", "greatest common divisor");
checkScientific(["lcm", "4", ",", "6", ")"], "12", "least common multiple");
checkScientific(["pi"], "3.14159265359", "pi constant");
checkScientific(["e"], "2.718281828459", "Euler constant");
checkScientific(["5", "%"], "0.05", "scientific postfix percentage");
checkScientific(["8", "1", "BS"], "8", "backspace clears the last digit");
checkScientific(["root", "3", ",", "-", "8", ")"], "-2", "odd root of a negative number");
checkScientific(["log", "8", ",", "1", ")"], "Math domain error", "logarithm base one must be rejected");
checkScientific(["tan", "9", "0", ")"], "Math domain error", "tangent singularity must be rejected");
checkScientific(["sqrt", "-", "1", ")"], "Math domain error", "negative square root must be rejected");

handlers["calc-mode-toggle:click"]();
assert.equal(elements["scientific-pad"].hidden, true, "scientific keypad should be hidden in standard mode");
assert.equal(elements["calc-mode-toggle"].textContent, "Scientific Mode", "toggle label should offer scientific mode");
function keydown(key, tagName = "BODY") {
  let prevented = false;
  handlers.keydown({ key, target: { tagName }, preventDefault() { prevented = true; } });
  return prevented;
}
assert.equal(keydown("2"), true, "keyboard digits should be accepted");
assert.equal(keydown("+"), true, "keyboard operators should be accepted");
assert.equal(keydown("2"), true, "second keyboard digit should be accepted");
assert.equal(keydown("Enter"), true, "Enter should calculate");
assert.equal(elements["calc-display"].textContent, "4", "keyboard expression should calculate correctly");
assert.equal(keydown("9", "INPUT"), false, "calculator keyboard handler must not intercept form inputs");
console.log("Scientific calculator tests passed.");
