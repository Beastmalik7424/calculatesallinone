#!/usr/bin/env node
"use strict";

// npm currently reports GHSA-fc5q-39xc-vjpf for picomatch <= 4.0.7.
// Upstream has not published a fixed release. This exception is narrow:
// the repository has no production dependencies and the lockfile contract
// proves every installed package is dev-only. Any other advisory fails CI.
const { spawnSync } = require("node:child_process");
const assert = require("node:assert/strict");

const ALLOWED = "https://github.com/advisories/GHSA-fc5q-39xc-vjpf";
const run = spawnSync("npm", ["audit", "--json"], {
  encoding: "utf8",
  maxBuffer: 16 * 1024 * 1024,
});
let report;
try {
  report = JSON.parse(run.stdout || "");
} catch {
  console.error("FAIL: npm audit did not return valid JSON.");
  console.error((run.stderr || run.stdout || "").slice(-4000));
  process.exit(1);
}

const vulnerabilities = report.vulnerabilities || {};
const names = Object.keys(vulnerabilities);
const unexpected = [];
const allowed = [];

for (const name of names) {
  const item = vulnerabilities[name];
  const advisories = (item.via || []).filter(v => typeof v === "object");
  const urls = advisories.map(v => v.url).filter(Boolean);
  const onlyAllowed = advisories.length > 0 && urls.every(url => url === ALLOWED);
  if (!onlyAllowed) {
    unexpected.push({ name, severity: item.severity, urls });
  } else {
    allowed.push({ name, severity: item.severity, nodes: item.nodes || [] });
  }
}

if (unexpected.length) {
  console.error("FAIL: unexpected dependency advisories found:");
  console.error(JSON.stringify(unexpected, null, 2));
  process.exit(1);
}

if (names.length === 0) {
  console.log("PASS: npm audit found no dependency advisories.");
  process.exit(run.status === 0 ? 0 : 1);
}

assert.ok(allowed.length > 0, "Known advisory exception must be explicit");
console.log("PASS WITH DOCUMENTED EXCEPTION: only " + ALLOWED + " remains.");
console.log("Affected package nodes are development-only; runtime isolation and npm audit --omit=dev are separate mandatory CI gates.");
console.log(JSON.stringify({ advisoryPackages: allowed, metadata: report.metadata?.vulnerabilities || {} }, null, 2));
process.exit(0);
