#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");

const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const lock = JSON.parse(fs.readFileSync(path.join(root, "package-lock.json"), "utf8"));

function validateRuntimeDependencyIsolation(pkg, packageLock) {
  const productionKeys = ["dependencies", "optionalDependencies", "peerDependencies"];
  for (const key of productionKeys) {
    if (Object.keys(pkg[key] || {}).length > 0) {
      return { ok: false, reason: "package.json declares production " + key };
    }
  }
  if (!packageLock.packages || !packageLock.packages[""]) {
    return { ok: false, reason: "package-lock root package is missing" };
  }
  const nonDev = Object.entries(packageLock.packages)
    .filter(([name, entry]) => name !== "" && entry.dev !== true)
    .map(([name]) => name);
  if (nonDev.length) {
    return { ok: false, reason: "non-dev lockfile packages: " + nonDev.join(", ") };
  }
  const rootLock = packageLock.packages[""];
  for (const key of productionKeys) {
    if (Object.keys(rootLock[key] || {}).length > 0) {
      return { ok: false, reason: "lockfile root declares production " + key };
    }
  }
  return { ok: true, packageCount: Object.keys(packageLock.packages).length - 1 };
}

function runUnitChecks() {
  const base = {
    packages: {
      "": { devDependencies: { playwright: "1.64.1" } },
      "node_modules/playwright": { dev: true },
    },
  };
  assert.equal(validateRuntimeDependencyIsolation({ devDependencies: { playwright: "1.64.1" } }, base).ok, true);
  assert.equal(validateRuntimeDependencyIsolation({ dependencies: { express: "1.0.0" } }, base).ok, false);
  assert.equal(validateRuntimeDependencyIsolation({ devDependencies: {} }, {
    packages: { "": {}, "node_modules/example": { dev: false } },
  }).ok, false);
  assert.equal(validateRuntimeDependencyIsolation({ devDependencies: {} }, { packages: {} }).ok, false);
}

runUnitChecks();
const result = validateRuntimeDependencyIsolation(manifest, lock);
assert.equal(result.ok, true, result.reason);
console.log("PASS: runtime dependency isolation verified; " + result.packageCount + " locked packages are development-only.");
