"use strict";
const assert=require("node:assert/strict");
const {percentage,percentageShare,percentageChange,percentageDifference,simplifyRatio,simplifyRatioThree,solveProportion,scaleRatio,fraction,compound,dateDifference,dateBreakdown}=require("../static/extra-calculators.js");
assert.equal(percentage(25,200),50);
assert.equal(percentage(12.5,80),10);
assert.equal(percentage(0,200),0);
assert.equal(percentageShare(45,250),18);
assert.equal(percentageShare(3,4),75);
assert.equal(percentageChange(80,100),25);
assert.equal(percentageChange(100,80),-20);
assert.equal(percentageChange(100,0),-100);
assert.equal(percentageChange(80,-40),-150);
assert.equal(percentageChange(1e308,1e308),0);
assert.throws(()=>percentageChange(0,80),/starting value must be greater than zero/);
assert.throws(()=>percentageChange(-50,-25),/starting value must be greater than zero/);
assert.throws(()=>percentageChange(1e-308,1e308),/Result exceeds supported range/);
assert.deepEqual(percentageDifference(40,60),{difference:20,average:50,percentage:40});
assert.deepEqual(percentageDifference(60,40),{difference:20,average:50,percentage:40});
assert.ok(Math.abs(percentageDifference(80,100).percentage-22.2222222222)<1e-9);
assert.equal(percentageDifference(0,10).percentage,200);
assert.equal(percentageDifference(1e308,0).percentage,200);
assert.throws(()=>percentageDifference(0,0),/Both values cannot be zero/);
assert.throws(()=>percentageDifference(-1,10),/non-negative values/);
assert.throws(()=>percentageDifference(1,Infinity),/finite numbers/);
assert.deepEqual(simplifyRatio(10,15),{a:"2",b:"3"});
assert.deepEqual(simplifyRatio(1.5,2.5),{a:"3",b:"5"});
assert.deepEqual(simplifyRatio(".5","1.5"),{a:"1",b:"3"});
assert.deepEqual(simplifyRatio("1.","2."),{a:"1",b:"2"});
assert.deepEqual(simplifyRatio("9007199254740993","9007199254740995"),{a:"9007199254740993",b:"9007199254740995"});
assert.deepEqual(simplifyRatio(0,15),{a:"0",b:"1"});
assert.throws(()=>simplifyRatio(0,0),/Both ratio terms cannot be zero/);
assert.throws(()=>simplifyRatio(-1,2),/non-negative/);
assert.throws(()=>simplifyRatio(1.0000001,2),/up to 6 decimal places/);
assert.deepEqual(simplifyRatioThree(100,200,400),{a:"1",b:"2",c:"4"});
assert.deepEqual(simplifyRatioThree(1.5,3,4.5),{a:"1",b:"2",c:"3"});
assert.deepEqual(simplifyRatioThree(0,0,5),{a:"0",b:"0",c:"1"});
assert.deepEqual(simplifyRatioThree("9007199254740993","9007199254740995","9007199254740997"),{a:"9007199254740993",b:"9007199254740995",c:"9007199254740997"});
assert.throws(()=>simplifyRatioThree(0,0,0),/All three ratio terms cannot be zero/);
assert.throws(()=>simplifyRatioThree(-1,2,3),/non-negative/);
assert.throws(()=>simplifyRatioThree(1.0000001,2,3),/up to 6 decimal places/);
assert.deepEqual(solveProportion(2,3,4,null),{missing:"D",value:6,a:2,b:3,c:4,d:6});
assert.deepEqual(solveProportion(null,3,4,6),{missing:"A",value:2,a:2,b:3,c:4,d:6});
assert.deepEqual(solveProportion(2,null,4,6),{missing:"B",value:3,a:2,b:3,c:4,d:6});
assert.deepEqual(solveProportion(2,3,null,6),{missing:"C",value:4,a:2,b:3,c:4,d:6});
assert.throws(()=>solveProportion(2,3,null,null),/exactly one/);
assert.throws(()=>solveProportion(0,3,4,null),/positive values/);
// Regression: cross-multiplication must not underflow an intermediate quotient when the final answer is representable.
assert.equal(solveProportion(null,1e308,1e-308,1e308).value,1e-308);
assert.equal(solveProportion(1e308,null,1e308,1e-308).value,1e-308);
assert.equal(solveProportion(1e-308,1e308,null,1e308).value,1e-308);
assert.equal(solveProportion(1e308,1e-308,1e308,null).value,1e-308);
assert.throws(()=>solveProportion(1e-308,1e308,1e308,null),/Result exceeds supported range/);
assert.throws(()=>solveProportion(1e308,1e-308,1e-308,null),/Result exceeds supported range/);
assert.deepEqual(scaleRatio(2,3,4),{a:"8",b:"12"});
assert.deepEqual(scaleRatio(0,3,2),{a:"0",b:"6"});
assert.deepEqual(scaleRatio("1.5","2.5","0.1"),{a:"0.15",b:"0.25"});
assert.deepEqual(scaleRatio("9007199254740993","2","1"),{a:"9007199254740993",b:"2"});
assert.deepEqual(scaleRatio("0.000001","0.000002","0.000001"),{a:"0.000000000001",b:"0.000000000002"});
assert.throws(()=>scaleRatio("1.0000001","2","1"),/up to 6 decimal places/);
assert.throws(()=>scaleRatio("-1","2","1"),/non-negative/);
assert.throws(()=>scaleRatio("1","2","-1"),/non-negative/);
assert.throws(()=>scaleRatio(2,3,0),/positive scale factor/);
assert.throws(()=>scaleRatio(0,0,2),/not both zero/);
assert.deepEqual(percentageDifference(Number.MIN_VALUE,Number.MIN_VALUE),{difference:0,average:Number.MIN_VALUE,percentage:0});
assert.equal(percentageDifference(Number.MIN_VALUE,Number.MIN_VALUE*2).average,Number.MIN_VALUE*2);
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
assert.deepEqual([dateDifference("2026-01-01","2026-01-01"),dateDifference("2026-01-01","2026-01-01",true)],[0,1]);
assert.equal(dateDifference("2026-01-02","2026-01-01"),-1);
assert.equal(dateDifference("0001-01-01","0001-01-02"),1);
assert.equal(dateDifference("0004-02-28","0004-03-01"),2);
assert.equal(dateDifference("0099-12-31","0100-01-01"),1);
assert.equal(dateDifference("0100-02-28","0100-03-01"),1);
assert.equal(dateDifference("0400-02-28","0400-03-01"),2);
assert.throws(()=>dateDifference("0000-01-01","0001-01-01"));
assert.throws(()=>dateDifference("2026-02-29","2026-03-01"));
assert.deepEqual([dateDifference("2024-01-01","2024-01-02",true),dateDifference("2024-01-02","2024-01-01",true)],[2,-2]);
console.log("Date difference elapsed/inclusive regression: PASS");
assert.deepEqual(dateBreakdown("2024-01-31","2024-02-29"),{years:0,months:1,days:0,weeks:29/7});
assert.deepEqual(dateBreakdown("2023-01-31","2023-02-28"),{years:0,months:1,days:0,weeks:4});
assert.deepEqual(dateBreakdown("2024-01-31","2024-03-01"),{years:0,months:1,days:1,weeks:30/7});
assert.deepEqual(dateBreakdown("2024-02-28","2024-03-01"),{years:0,months:0,days:2,weeks:2/7});
assert.deepEqual(dateBreakdown("2024-02-29","2025-02-28"),{years:1,months:0,days:0,weeks:365/7});
assert.deepEqual(dateBreakdown("2024-02-29","2024-01-31"),{years:0,months:-1,days:0,weeks:-29/7});
console.log("Date calendar breakdown and month-end clamping regression: PASS");


const fs = require("node:fs");
const path = require("node:path");
// Regression: Tailwind must compile the primary action's background on all four extra pages.
const compiledCss = fs.readFileSync(path.join(__dirname, "..", "static", "site.css"), "utf8");
assert.match(compiledCss, /\.bg-sky-700\s*\{/, "Missing bg-sky-700: extra calculator Calculate buttons become white-on-white");
for (const slug of ["percentage-calculator", "percentage-difference-calculator", "fraction-calculator", "ratio-calculator", "compound-interest-calculator", "date-calculator"]) {
  const html = fs.readFileSync(path.join(__dirname, "..", "public", slug, "index.html"), "utf8");
  assert.match(html, /<button[^>]*bg-sky-700[^>]*>Calculate<\/button>/, slug + " primary action lacks background class");
}
console.log("Extra calculator button visibility CSS regression: PASS");

// Content and calculator capability must agree, and the money/math hubs must give actionable examples.
const fs2=require("node:fs");
const extraSource=fs2.readFileSync(require("node:path").join(__dirname,"..","extra_calculator_pages.py"),"utf8");
assert.match(extraSource,/what percentage the part represents of another/);
assert.match(extraSource,/Calculate a percentage of a number, find what percentage one amount is of another, or measure percentage change/);
assert.match(extraSource,/18% of PKR 2,500/);
assert.ok(extraSource.includes("percentage difference = |A - B|"), "Percentage difference page must show its symmetric formula");
assert.ok(extraSource.includes("Percentage Difference Calculator"), "Percentage difference page must have a dedicated title");
assert.ok(extraSource.includes("Ratio Calculator"), "Ratio page must have a dedicated title");
assert.ok(extraSource.includes("10:15"), "Ratio page must include a checkable simplification example");
assert.match(extraSource,/1,102\.50/);
assert.match(extraSource,/28 February 2024 to 1 March 2024 is 2 elapsed days/);
const hubSource=fs2.readFileSync(require("node:path").join(__dirname,"..","content_v13.py"),"utf8");
for(const phrase of ["PKR 4,500","PKR 3,600","net operating profit","advertised APY","8 + 3 × 4 = 20","1/2 + 1/3","25.4 millimetres"]){assert.ok(hubSource.includes(phrase),"Missing useful hub guidance: "+phrase);}
console.log("AdSense content usefulness regression: PASS");


// Deterministic property simulations for the pure calculator engines.
// These exercise the real production exports and compare them with independent
// arithmetic oracles. Keep the seed fixed so failures are reproducible.
let propertySeed = 20261114;
const propertyRandom = () => {
  propertySeed = (Math.imul(propertySeed, 1664525) + 1013904223) >>> 0;
  return propertySeed / 4294967296;
};
const propertyInt = (min, max) => min + Math.floor(propertyRandom() * (max - min + 1));
const propertyNear = (actual, expected, relative = 1e-10, absolute = 1e-9) => {
  assert.ok(Number.isFinite(actual), `expected a finite result, received ${actual}`);
  assert.ok(Math.abs(actual - expected) <= Math.max(absolute, Math.abs(expected) * relative),
    `expected ${actual} to be close to ${expected}`);
};
const propertyGcd = (a, b) => {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
};
const propertyScaled12 = value => {
  const [whole, fraction = ""] = String(value).split(".");
  return BigInt(whole) * 1000000000000n + BigInt((fraction + "0".repeat(12)).slice(0, 12));
};

let percentageCases = 0;
for (let i = 0; i < 1000; i++) {
  const part = propertyInt(-1000000, 1000000);
  const total = propertyInt(-1000000, 1000000);
  propertyNear(percentage(part, total), part * total / 100);
  const whole = propertyInt(1, 1000000);
  const sharePart = propertyInt(-1000000, 1000000);
  propertyNear(percentageShare(sharePart, whole), sharePart / whole * 100);
  const start = propertyInt(1, 1000000);
  const end = propertyInt(0, 1000000);
  propertyNear(percentageChange(start, end), ((end - start) / start) * 100);
  let first = propertyInt(0, 1000000);
  let second = propertyInt(0, 1000000);
  if (first === 0 && second === 0) second = 1;
  const average = (first + second) / 2;
  const expectedDifference = Math.round((Math.abs(first - second) / average) * 100 * 1e12) / 1e12;
  const diff = percentageDifference(first, second);
  propertyNear(diff.difference, Math.abs(first - second));
  propertyNear(diff.average, average);
  propertyNear(diff.percentage, expectedDifference, 1e-12, 1e-12);
  percentageCases++;
}
console.log(`SIMULATION PASS: ${percentageCases.toLocaleString("en-US")} percentage/share/change/difference cases`);

let ratioCases = 0;
for (let i = 0; i < 1000; i++) {
  let a = propertyInt(0, 1000000), b = propertyInt(0, 1000000);
  if (a === 0 && b === 0) b = 1;
  const simple = simplifyRatio(a, b);
  const sa = BigInt(simple.a), sb = BigInt(simple.b);
  assert.equal(BigInt(a) * sb, BigInt(b) * sa);
  assert.equal(propertyGcd(sa, sb), 1n);

  let x = propertyInt(0, 1000000), y = propertyInt(0, 1000000), z = propertyInt(0, 1000000);
  if (x === 0 && y === 0 && z === 0) z = 1;
  const triple = simplifyRatioThree(x, y, z);
  const tx = BigInt(triple.a), ty = BigInt(triple.b), tz = BigInt(triple.c);
  assert.equal(BigInt(x) * ty, BigInt(y) * tx);
  assert.equal(BigInt(x) * tz, BigInt(z) * tx);
  assert.equal(propertyGcd(propertyGcd(tx, ty), tz), 1n);

  const factor = propertyInt(1, 1000);
  const scaled = scaleRatio(a, b, factor);
  const scaledA = propertyScaled12(scaled.a), scaledB = propertyScaled12(scaled.b);
  assert.equal(BigInt(a) * scaledB, BigInt(b) * scaledA);
  ratioCases++;
}
console.log(`SIMULATION PASS: ${ratioCases.toLocaleString("en-US")} two-term, three-term and scaled-ratio cases`);

let proportionCases = 0;
for (let i = 0; i < 1000; i++) {
  const a = propertyInt(1, 100000), b = propertyInt(1, 100000);
  const c = propertyInt(1, 100000), d = propertyInt(1, 100000);
  const expected = [b * c / d, a * d / c, a * d / b, b * c / a];
  const inputs = [
    [null, b, c, d],
    [a, null, c, d],
    [a, b, null, d],
    [a, b, c, null]
  ];
  for (let missing = 0; missing < 4; missing++) {
    const solved = solveProportion(...inputs[missing]);
    assert.equal(solved.missing, ["A", "B", "C", "D"][missing]);
    propertyNear(solved.value, expected[missing]);
    propertyNear(solved.a * solved.d, solved.b * solved.c, 1e-10, 1e-7);
    proportionCases++;
  }
}
console.log(`SIMULATION PASS: ${proportionCases.toLocaleString("en-US")} proportion-solving cases`);

let fractionCases = 0;
const fractionOracle = (a, b, c, d, operation) => {
  let n, den;
  if (operation === "add") { n = BigInt(a) * BigInt(d) + BigInt(c) * BigInt(b); den = BigInt(b) * BigInt(d); }
  else if (operation === "subtract") { n = BigInt(a) * BigInt(d) - BigInt(c) * BigInt(b); den = BigInt(b) * BigInt(d); }
  else if (operation === "multiply") { n = BigInt(a) * BigInt(c); den = BigInt(b) * BigInt(d); }
  else { n = BigInt(a) * BigInt(d); den = BigInt(b) * BigInt(c); }
  if (den < 0n) { n = -n; den = -den; }
  const divisor = propertyGcd(n, den);
  return { n: n / divisor, d: den / divisor };
};
for (const operation of ["add", "subtract", "multiply", "divide"]) {
  for (let i = 0; i < 1000; i++) {
    const a = propertyInt(-100, 100);
    const c = propertyInt(-100, 100);
    let b = propertyInt(-100, 100), d = propertyInt(-100, 100);
    if (b === 0) b = 1;
    if (d === 0) d = 1;
    if (operation === "divide" && c === 0) continue;
    const actual = fraction(a, b, c, d, operation);
    const expected = fractionOracle(a, b, c, d, operation);
    assert.equal(BigInt(actual.n), expected.n);
    assert.equal(BigInt(actual.d), expected.d);
    fractionCases++;
  }
}
console.log(`SIMULATION PASS: ${fractionCases.toLocaleString("en-US")} exact rational arithmetic cases`);

let compoundCases = 0;
for (let i = 0; i < 1000; i++) {
  const principal = propertyInt(0, 1000000);
  const rate = propertyInt(0, 2500) / 100;
  const years = propertyInt(0, 10);
  const frequency = [1, 2, 4, 12][propertyInt(0, 3)];
  const periods = years * frequency;
  const factor = 1 + rate / (100 * frequency);
  let oracle = principal;
  for (let period = 0; period < periods; period++) oracle *= factor;
  propertyNear(compound(principal, rate, years, frequency), oracle, 1e-10, 1e-8);
  compoundCases++;
}
console.log(`SIMULATION PASS: ${compoundCases.toLocaleString("en-US")} compound-interest cases`);

const isoFromDay = day => new Date(day * 86400000).toISOString().slice(0, 10);
let dateCases = 0;
for (let i = 0; i < 1000; i++) {
  const startDay = propertyInt(0, 47482);
  const endDay = propertyInt(0, 47482);
  const startDate = isoFromDay(startDay);
  const endDate = isoFromDay(endDay);
  const elapsed = endDay - startDay;
  assert.equal(dateDifference(startDate, endDate), elapsed);
  assert.equal(dateDifference(startDate, endDate, true), elapsed + (elapsed === 0 ? 1 : Math.sign(elapsed)));
  const breakdown = dateBreakdown(startDate, endDate);
  const reverse = dateBreakdown(endDate, startDate);
  assert.equal(breakdown.years, -reverse.years);
  assert.equal(breakdown.months, -reverse.months);
  assert.equal(breakdown.days, -reverse.days);
  propertyNear(breakdown.weeks * 7, elapsed, 1e-12, 1e-9);
  assert.ok(Math.abs(breakdown.months) < 12);
  assert.ok(Math.abs(breakdown.days) <= 31);
  dateCases++;
}
console.log(`SIMULATION PASS: ${dateCases.toLocaleString("en-US")} date-difference and calendar-breakdown cases`);
