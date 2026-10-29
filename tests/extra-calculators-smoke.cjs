"use strict";
const assert=require("node:assert/strict");
const {percentage,fraction,compound,dateDifference}=require("../static/extra-calculators.js");
assert.equal(percentage(25,200),50);
assert.equal(percentage(12.5,80),10);
assert.equal(percentage(0,200),0);
assert.throws(()=>percentage(10,Infinity));
assert.deepEqual(fraction(1,2,1,3,"add"),{n:5,d:6});
assert.deepEqual(fraction(2,3,3,4,"multiply"),{n:1,d:2});
assert.deepEqual(fraction(1,2,1,2,"subtract"),{n:0,d:1});
assert.throws(()=>fraction(1,0,1,2,"add"));
assert.throws(()=>fraction(1,2,0,1,"divide"));
assert.equal(compound(1000,10,1,2),1102.5);
assert.equal(compound(1000,0,2,12),1000);
assert.throws(()=>compound(1000,-1200,1,12));
assert.equal(dateDifference("2024-02-28","2024-03-01"),2);
assert.equal(dateDifference("2026-01-01","2026-01-01"),0);
assert.equal(dateDifference("2026-01-02","2026-01-01"),-1);
assert.throws(()=>dateDifference("2026-02-29","2026-03-01"));
console.log("Competitor calculator arithmetic and date regression: PASS");


const fs = require("node:fs");
const path = require("node:path");
// Regression: Tailwind must compile the primary action's background on all four extra pages.
const compiledCss = fs.readFileSync(path.join(__dirname, "..", "static", "site.css"), "utf8");
assert.match(compiledCss, /\.bg-sky-700\s*\{/, "Missing bg-sky-700: extra calculator Calculate buttons become white-on-white");
for (const slug of ["percentage-calculator", "fraction-calculator", "compound-interest-calculator", "date-calculator"]) {
  const html = fs.readFileSync(path.join(__dirname, "..", "public", slug, "index.html"), "utf8");
  assert.match(html, /<button[^>]*bg-sky-700[^>]*>Calculate<\/button>/, slug + " primary action lacks background class");
}
console.log("Extra calculator button visibility CSS regression: PASS");
