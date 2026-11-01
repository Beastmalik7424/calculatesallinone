"use strict";
const assert=require("node:assert/strict");
const {percentage,percentageShare,whatPercent,percentChange,fraction,compound,dateDifference}=require("../static/extra-calculators.js");
assert.equal(percentage(25,200),50);
assert.equal(percentage(12.5,80),10);
assert.equal(percentage(0,200),0);
assert.equal(percentageShare(45,250),18);
assert.equal(percentageShare(3,4),75);
assert.equal(whatPercent(30,120),25);
assert.equal(whatPercent(15,60),25);
assert.throws(()=>whatPercent(5,0));
assert.equal(percentChange(80,100),25);
assert.equal(percentChange(100,80),-20);
assert.equal(percentChange(100,-20),-120);
assert.throws(()=>percentChange(0,10));
assert.throws(()=>percentChange(-50,-25));
assert.equal(percentage(-25,100),-25);
assert.equal(percentageShare(-45,250),-18);
assert.equal(percentage(1e308,100),1e308);
assert.throws(()=>percentage(1e308,200),/Result exceeds supported range/);
assert.throws(()=>percentageShare(1e308,1),/Result exceeds supported range/);
assert.throws(()=>percentageShare(1,0),/whole amount cannot be zero/);
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

// Content and calculator capability must agree, and the money/math hubs must give actionable examples.
const fs2=require("node:fs");
const extraSource=fs2.readFileSync(require("node:path").join(__dirname,"..","extra_calculator_pages.py"),"utf8");
assert.match(extraSource,/what percentage the part represents of another/);
assert.match(extraSource,/Calculate a percentage of a number or find what percentage one amount is of another/);
assert.match(extraSource,/18% of PKR 2,500/);
assert.match(extraSource,/1,102\.50/);
assert.match(extraSource,/28 February 2024 to 1 March 2024 is 2 days/);
const hubSource=fs2.readFileSync(require("node:path").join(__dirname,"..","content_v13.py"),"utf8");
for(const phrase of ["PKR 4,500","PKR 3,600","net operating profit","advertised APY","8 + 3 × 4 = 20","1/2 + 1/3","25.4 millimetres"]){assert.ok(hubSource.includes(phrase),"Missing useful hub guidance: "+phrase);}
console.log("AdSense content usefulness regression: PASS");
