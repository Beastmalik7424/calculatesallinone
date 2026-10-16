"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const lock = JSON.parse(fs.readFileSync("package-lock.json", "utf8"));
const locked = lock.packages["node_modules/braces"];

assert.equal(locked.name, "@zklogic/braces", "braces must resolve to the hardened compatibility fork");
assert.equal(locked.version, "3.0.7", "unexpected hardened braces version");
assert.match(locked.integrity, /^sha512-/);
assert.equal(typeof require("braces"), "function", "braces API must remain compatible");

const ordinary = require("braces")("a/{b,c}/d");
assert.deepEqual(ordinary, ["a/(b|c)/d"]);

const deeplyNested = "{".repeat(300) + "x" + "}".repeat(300);
assert.doesNotThrow(() => require("braces")(deeplyNested));
assert.doesNotThrow(() => require("braces")(deeplyNested, { expand: true }));

console.log("Hardened braces alias, integrity pin, API compatibility and deep-nesting regression passed.");
