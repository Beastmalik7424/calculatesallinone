#!/usr/bin/env node
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

function page(slug) {
  const file = path.join(__dirname, "..", "public", slug, "index.html");
  assert.ok(fs.existsSync(file), "Missing generated page: " + slug);
  return fs.readFileSync(file, "utf8");
}
function visibleText(html) {
  return html.replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/&amp;/g, "&").replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'").replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">").replace(/\s+/g, " ").trim();
}
const en = page("zakat-calculator");
const ur = page("ur/zakat-calculator");
const enText = visibleText(en);
const urText = visibleText(ur);

for (const id of [
  "z-currency", "z-nisab-method", "z-silverprice", "z-goldprice",
  "z-cash", "z-bank", "z-savings", "z-gold", "z-silver",
  "z-investments", "z-businesscash", "z-stock", "z-recv",
  "z-pension", "z-crypto", "z-property", "z-debts", "z-paid",
  "z-hawl", "zakat-result"
]) {
  assert.match(en, new RegExp('id="' + id + '"'), "English calculator missing " + id);
  assert.match(ur, new RegExp('id="' + id + '"'), "Urdu calculator missing " + id);
}
for (const term of [
  "ISO 4217", "silver Nisab", "gold Nisab", "612.36", "87.48",
  "503,529", "State Bank of Pakistan", "Hawl", "short-term liabilities",
  "personal-use", "business inventory", "recoverable receivables",
  "2.5%", "Worked example", "What this calculator does not decide"
]) {
  assert.ok(enText.toLowerCase().includes(term.toLowerCase()), "English page missing useful topic: " + term);
}
for (const term of [
  "503,529", "612.36", "87.48", "قمری سال", "پاکستان", "نصاب",
  "اثاثے", "واجب الادا", "2.5"
]) {
  assert.ok(urText.includes(term), "Urdu page missing localized topic: " + term);
}
assert.ok(enText.split(/\s+/).length >= 1000, "English Zakat guide is too thin (<1000 visible words)");
assert.ok(urText.split(/\s+/).length >= 700, "Urdu Zakat guide is too thin (<700 visible words)");
assert.match(en, /application\/ld\+json/, "English page must retain structured data");
assert.match(ur, /application\/ld\+json/, "Urdu page must retain structured data");
assert.match(en, /canonical/i, "English page must retain canonical metadata");
assert.match(ur, /canonical/i, "Urdu page must retain canonical metadata");
console.log("Zakat global calculator content and localization gates: PASS");
