#!/usr/bin/env node
"use strict";

// npm currently reports GHSA-fc5q-39xc-vjpf for picomatch <= 4.0.7.
// Upstream has not published a fixed release. The exception is narrow:
// every finding must trace exclusively to this advisory, and separate CI
// gates prove all installed packages are dev-only and production audit is clean.
const { spawnSync } = require("node:child_process");
const assert = require("node:assert/strict");

const ALLOWED = "https://github.com/advisories/GHSA-fc5q-39xc-vjpf";

function collectAdvisoryUrls(name, all, seen = new Set()) {
  if (seen.has(name) || !all[name]) return [];
  seen.add(name);
  const urls = [];
  for (const via of all[name].via || []) {
    if (typeof via === "string") urls.push(...collectAdvisoryUrls(via, all, seen));
    else if (via && typeof via === "object" && via.url) urls.push(via.url);
  }
  return urls;
}

function validateReport(report) {
  const all = report.vulnerabilities || {};
  const findings = [];
  for (const [name, item] of Object.entries(all)) {
    const urls = [...new Set(collectAdvisoryUrls(name, all))];
    if (!urls.length || urls.some(url => url !== ALLOWED)) {
      findings.push({ name, severity: item.severity, urls });
    }
  }
  return { ok: findings.length === 0, findings, count: Object.keys(all).length };
}

function runUnitChecks() {
  const allowed = {
    vulnerabilities: {
      anymatch: { severity: "high", via: ["picomatch"] },
      picomatch: { severity: "high", via: [{ url: ALLOWED }] },
    },
  };
  assert.equal(validateReport(allowed).ok, true, "transitive finding should trace to allowlisted advisory");
  assert.equal(validateReport({ vulnerabilities: { foo: { via: [{ url: "https://other/advisory" }] } } }).ok, false);
  assert.equal(validateReport({ vulnerabilities: { foo: { via: ["missing"] } } }).ok, false);
  assert.equal(validateReport({ vulnerabilities: {} }).ok, true);
}

runUnitChecks();
const run = spawnSync("npm", ["audit", "--json"], { encoding: "utf8", maxBuffer: 16 * 1024 * 1024 });
let report;
try { report = JSON.parse(run.stdout || ""); }
catch {
  console.error("FAIL: npm audit did not return valid JSON.");
  console.error((run.stderr || run.stdout || "").slice(-4000));
  process.exit(1);
}
const result = validateReport(report);
if (!result.ok) {
  console.error("FAIL: unexpected dependency advisories found:");
  console.error(JSON.stringify(result.findings, null, 2));
  process.exit(1);
}
if (result.count === 0) {
  console.log("PASS: npm audit found no dependency advisories.");
  process.exit(run.status === 0 ? 0 : 1);
}
console.log("PASS WITH DOCUMENTED EXCEPTION: " + result.count + " affected package entries trace only to " + ALLOWED + ".");
console.log("Separate mandatory CI gates verify that all installed packages are development-only and npm audit --omit=dev is clean.");
