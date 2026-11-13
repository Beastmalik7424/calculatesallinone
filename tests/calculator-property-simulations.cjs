"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const extra = require("../static/extra-calculators.js");
const calorie = require("../static/calorie-calculator.js");
const refs = require("./fixtures/calculator-reference-values.json");

let seed = 20261114;
function random() {
  seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5;
  return (seed >>> 0) / 4294967296;
}
function integer(min, max) { return min + Math.floor(random() * (max - min + 1)); }
function close(actual, expected, tolerance = 1e-9) {
  assert.ok(Number.isFinite(actual), "actual value must be finite");
  assert.ok(Math.abs(actual - expected) <= tolerance * Math.max(1, Math.abs(expected)),
    "expected " + expected + ", received " + actual);
}
function gcd(a, b) { while (b) [a, b] = [b, a % b]; return a < 0n ? -a : a; }
function gcd3(a, b, c) { return gcd(gcd(a, b), c); }
function normalizedFraction(n, d) {
  if (d < 0n) { n = -n; d = -d; }
  const g = gcd(n < 0n ? -n : n, d);
  return { n: Number(n / g), d: Number(d / g) };
}
function dateString(year, month, day) {
  return String(year).padStart(4, "0") + "-" + String(month).padStart(2, "0") + "-" + String(day).padStart(2, "0");
}
function utcDate() {
  const year = integer(1900, 2100), month = integer(0, 11);
  const last = new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
  return dateString(year, month + 1, integer(1, last));
}
function scaledDecimal(value) {
  const whole = value / 1000000000000n;
  const fraction = (value % 1000000000000n).toString().padStart(12, "0").replace(/0+$/, "");
  return fraction ? whole.toString() + "." + fraction : whole.toString();
}
function scaledTerm(value) { return BigInt(value) * 1000000n; }

let simulations = 0;
let unitAssertions = 0;
function unit(condition, message) { assert.ok(condition, message); unitAssertions++; }
function simulate(fn, count) {
  for (let i = 0; i < count; i++) { fn(i); simulations++; }
}

// Golden reference values independently recorded from the published equations and exact arithmetic.
close(extra.percentage(...refs.referenceCases.percentage.input), refs.referenceCases.percentage.expected);
close(extra.percentageShare(...refs.referenceCases.percentageShare.input), refs.referenceCases.percentageShare.expected);
close(extra.percentageChange(...refs.referenceCases.percentageChange.input), refs.referenceCases.percentageChange.expected);
assert.deepEqual(extra.percentageDifference(...refs.referenceCases.percentageDifference.input), refs.referenceCases.percentageDifference.expected);
assert.deepEqual(extra.fraction(...refs.referenceCases.fractionAdd.input), refs.referenceCases.fractionAdd.expected);
close(extra.compound(...refs.referenceCases.compound.input), refs.referenceCases.compound.expected);
assert.equal(extra.dateDifference(...refs.referenceCases.dateDifference.input), refs.referenceCases.dateDifference.expected);
const maleRef = calorie.calculateMaintenanceCalories(refs.referenceCases.calorieMale.input);
close(maleRef.restingKcalPerDay, refs.referenceCases.calorieMale.expected.resting);
close(maleRef.maintenanceKcalPerDay, refs.referenceCases.calorieMale.expected.maintenance);
const femaleRef = calorie.calculateMaintenanceCalories(refs.referenceCases.calorieFemale.input);
close(femaleRef.restingKcalPerDay, refs.referenceCases.calorieFemale.expected.resting);
close(femaleRef.maintenanceKcalPerDay, refs.referenceCases.calorieFemale.expected.maintenance);
unitAssertions += 10;

// 1,000 independent percentage-of calculations.
simulate(() => {
  const part = integer(-100000, 100000) / 100;
  const total = integer(-100000, 100000) / 100;
  close(extra.percentage(part, total), (part * total) / 100);
}, 1000);

// 1,000 percentage-share calculations, checked by the inverse relationship.
simulate(() => {
  let whole = integer(-100000, 100000) / 100;
  if (whole === 0) whole = 0.01;
  const part = integer(-100000, 100000) / 100;
  close(extra.percentageShare(part, whole) * whole / 100, part);
}, 1000);

// 1,000 percentage-change calculations against the independent textbook definition.
simulate(() => {
  const start = integer(1, 1000000) / 100;
  const end = integer(-1000000, 1000000) / 100;
  close(extra.percentageChange(start, end), ((end - start) / start) * 100);
}, 1000);

// 1,000 symmetric percentage-difference calculations.
simulate(() => {
  const a = integer(0, 1000000) / 100;
  let b = integer(0, 1000000) / 100;
  if (a === 0 && b === 0) b = 0.01;
  const result = extra.percentageDifference(a, b);
  close(result.difference, Math.abs(a - b));
  close(result.average, (a + b) / 2);
  close(result.percentage, Math.abs(a - b) / ((a + b) / 2) * 100, 1e-11);
  close(extra.percentageDifference(b, a).percentage, result.percentage, 1e-11);
}, 1000);

// 1,000 two-term and three-term ratio reductions checked with a BigInt GCD oracle.
simulate(() => {
  const a = BigInt(integer(0, 1000000)), b = BigInt(integer(0, 1000000));
  if (a === 0n && b === 0n) return;
  const g = gcd(a, b);
  const got = extra.simplifyRatio(Number(a), Number(b));
  unit(got.a === (a / g).toString() && got.b === (b / g).toString(), "two-term ratio must reduce by the exact GCD");
}, 1000);
simulate(() => {
  const a = BigInt(integer(0, 1000000)), b = BigInt(integer(0, 1000000)), c = BigInt(integer(0, 1000000));
  if (a === 0n && b === 0n && c === 0n) return;
  const g = gcd3(a, b, c);
  const got = extra.simplifyRatioThree(Number(a), Number(b), Number(c));
  unit(got.a === (a / g).toString() && got.b === (b / g).toString() && got.c === (c / g).toString(),
    "three-term ratio must reduce by the exact GCD");
}, 1000);

// 1,000 proportion cases, rotating the missing position across all four terms.
simulate(i => {
  const p = integer(1, 1000), q = integer(1, 1000), r = integer(1, 1000), s = integer(1, 1000);
  const full = [p * r, q * r, p * s, q * s];
  const missing = i % 4;
  const input = full.slice(); input[missing] = null;
  const result = extra.solveProportion(...input);
  close(result.value, full[missing]);
  close(result.a / result.b, result.c / result.d);
}, 1000);

// 1,000 exact scaled-ratio multiplications, verified using integer micro-units.
simulate(() => {
  const a = integer(1, 100000), b = integer(1, 100000), factor = integer(1, 100000);
  const as = scaledTerm(a), bs = scaledTerm(b), fs = scaledTerm(factor);
  const got = extra.scaleRatio(a, b, factor);
  assert.equal(got.a, scaledDecimal(as * fs));
  assert.equal(got.b, scaledDecimal(bs * fs));
  unitAssertions += 2;
}, 1000);

// 1,000 fraction operations across add/subtract/multiply/divide, with a BigInt oracle.
simulate(i => {
  const a = BigInt(integer(-1000, 1000)), b = BigInt(integer(1, 1000));
  const c = BigInt(integer(-1000, 1000)), d = BigInt(integer(1, 1000));
  const operation = ["add", "subtract", "multiply", "divide"][i % 4];
  let n, den;
  if (operation === "add") { n = a * d + c * b; den = b * d; }
  else if (operation === "subtract") { n = a * d - c * b; den = b * d; }
  else if (operation === "multiply") { n = a * c; den = b * d; }
  else { if (c === 0n) return; n = a * d; den = b * c; }
  const expected = normalizedFraction(n, den);
  assert.deepEqual(extra.fraction(Number(a), Number(b), Number(c), Number(d), operation), expected);
  unitAssertions++;
}, 1000);

// 1,000 compound-interest schedules, using repeated multiplication rather than Math.pow.
simulate(() => {
  const principal = integer(100, 1000000) / 100;
  const rate = integer(0, 3000) / 100;
  const years = integer(0, 30);
  const frequency = [1, 2, 4, 12][integer(0, 3)];
  const periods = years * frequency;
  const factor = 1 + rate / (100 * frequency);
  let expected = principal;
  for (let j = 0; j < periods; j++) expected *= factor;
  close(extra.compound(principal, rate, years, frequency), expected, 1e-10);
}, 1000);

// 1,000 date differences including reverse order and leap-day spans.
simulate(() => {
  const start = utcDate(), end = utcDate();
  const expected = (Date.parse(end + "T00:00:00Z") - Date.parse(start + "T00:00:00Z")) / 86400000;
  assert.equal(extra.dateDifference(start, end), expected);
  assert.equal(extra.dateDifference(end, start), -expected);
  assert.equal(extra.dateDifference(start, end, true), expected + (expected === 0 ? 1 : Math.sign(expected)));
  unitAssertions += 3;
}, 1000);

// 1,000 calendar breakdown invariants, including negative and month-end intervals.
simulate(() => {
  const start = utcDate(), end = utcDate();
  const elapsed = (Date.parse(end + "T00:00:00Z") - Date.parse(start + "T00:00:00Z")) / 86400000;
  const result = extra.dateBreakdown(start, end);
  close(result.weeks, elapsed / 7);
  unit(Math.abs(result.months) < 12, "calendar breakdown months must stay below twelve");
  unit(Math.abs(result.days) <= 31, "calendar breakdown residual days must be within one month");
  if (elapsed > 0) unit(result.years >= 0 && result.months >= 0 && result.days >= 0, "forward breakdown must not have negative components");
  if (elapsed < 0) unit(result.years <= 0 && result.months <= 0 && result.days <= 0, "reverse breakdown must not have positive components");
}, 1000);

// 1,000 Mifflin–St Jeor maintenance estimates using an independent equation oracle.
simulate(() => {
  const age = integer(18, 100), weightKg = integer(3000, 20000) / 100;
  const heightCm = integer(13000, 22000) / 100;
  const coefficient = random() < 0.5 ? "male" : "female";
  const activity = calorie.ACTIVITY_PRESETS[integer(0, calorie.ACTIVITY_PRESETS.length - 1)];
  const resting = 10 * weightKg + 6.25 * heightCm - 5 * age + (coefficient === "male" ? 5 : -161);
  const result = calorie.calculateMaintenanceCalories({
    age, weight: weightKg, weightUnit: "kg", heightUnit: "cm", heightCm,
    coefficient, activityId: activity.id, pregnancyStatus: coefficient === "female" ? "no" : undefined
  });
  close(result.restingKcalPerDay, resting);
  close(result.maintenanceKcalPerDay, resting * activity.multiplier);
}, 1000);

// 1,000 DRI 2023 adult life-stage cases, checked against independently transcribed equation coefficients.
simulate(() => {
  const age = integer(19, 80), heightCm = integer(15000, 20000) / 100, weightKg = integer(4500, 12000) / 100;
  const pal = calorie.DRI_ACTIVITY_CATEGORIES[integer(0, 3)];
  const status = ["pregnant", "breastfeeding", "both"][integer(0, 2)];
  const weeks = integer(1, 42), preWeight = integer(4500, 12000) / 100;
  const base = {
    inactive: 584.90 - 7.01 * age + 5.72 * heightCm + 11.71 * weightKg,
    low_active: 575.77 - 7.01 * age + 6.60 * heightCm + 12.14 * weightKg,
    active: 710.25 - 7.01 * age + 6.54 * heightCm + 12.34 * weightKg,
    very_active: 511.83 - 7.01 * age + 9.07 * heightCm + 12.56 * weightKg
  }[pal];
  const input = {
    age, coefficient: "female", pregnancyStatus: status, lifeStageActivityId: pal,
    weight: weightKg, weightUnit: "kg", heightUnit: "cm", heightCm,
    pregnancyWeeks: weeks, prePregnancyWeight: preWeight,
    breastfeedingStage: random() < 0.5 ? "exclusive_0_6" : "partial_7_12"
  };
  const result = calorie.calculateLifeStageCalories(input);
  if (status === "pregnant" || status === "both") {
    let expected = base;
    if (weeks > 13) {
      const bmi = preWeight / Math.pow(heightCm / 100, 2);
      const deposition = bmi < 18.5 ? 300 : bmi < 25 ? 200 : bmi < 30 ? 150 : -50;
      const pregnancyBase = {
        inactive: 1131.20 - 2.04 * age + 0.34 * heightCm + 12.15 * weightKg + 9.16 * weeks,
        low_active: 693.35 - 2.04 * age + 5.73 * heightCm + 10.20 * weightKg + 9.16 * weeks,
        active: -223.84 - 2.04 * age + 13.23 * heightCm + 8.15 * weightKg + 9.16 * weeks,
        very_active: -779.72 - 2.04 * age + 18.45 * heightCm + 8.73 * weightKg + 9.16 * weeks
      }[pal];
      expected = pregnancyBase + deposition;
    }
    close(result.pregnancy.eerKcalPerDay, expected);
  }
  if (status === "breastfeeding" || status === "both") {
    const increment = input.breastfeedingStage === "exclusive_0_6" ? 400 : 380;
    close(result.breastfeeding.eerKcalPerDay, base + increment);
  }
}, 1000);

// Integration checks: generated pages must load the same tested engines and expose their calculator controls.
const root = path.join(__dirname, "..");
const caloriePage = fs.readFileSync(path.join(root, "public", "calorie-calculator", "index.html"), "utf8");
const percentagePage = fs.readFileSync(path.join(root, "public", "percentage-calculator", "index.html"), "utf8");
const fractionPage = fs.readFileSync(path.join(root, "public", "fraction-calculator", "index.html"), "utf8");
assert.match(caloriePage, /\/assets\/calorie-calculator\.js\?v=/, "generated calorie page must load the tested calorie engine");
assert.match(caloriePage, /id="calorie-form"/, "generated calorie page must expose the expected form contract");
assert.match(percentagePage, /\/assets\/extra-calculators\.js/, "generated percentage page must load the tested extra-calculator engine");
assert.match(percentagePage, /\/assets\/extra-calculators-ui\.js/, "generated percentage page must load the calculator UI adapter");
assert.match(percentagePage, /id="percentage-form"/, "generated percentage page must expose its form contract");
assert.match(fractionPage, /\/assets\/extra-calculators\.js/, "generated fraction page must load the tested extra-calculator engine");
assert.match(fractionPage, /id="fraction-form"/, "generated fraction page must expose its form contract");

console.log("PASS: " + simulations + " deterministic calculator simulations (seed 20261114)");
console.log("PASS: " + unitAssertions + " independent unit/property assertions");
console.log("PASS: 3 generated-page integration contracts");
