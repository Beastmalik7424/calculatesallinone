"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const engine = require("../static/calorie-calculator.js");

const { calculateCalorieTargets, ACTIVITY_PRESETS } = engine;
assert.equal(typeof calculateCalorieTargets, "function", "Three-formula calculation engine must be exported");

const common = { age: 30, weight: 70, weightUnit: "kg", height: 175, heightUnit: "cm", coefficient: "male", activityId: "sedentary" };
const mifflin = calculateCalorieTargets({ ...common, formula: "mifflin" });
assert.equal(mifflin.restingKcalPerDay, 1648.75);
assert.equal(mifflin.maintenanceKcalPerDay, 1978.5);
assert.equal(mifflin.mildDeficitKcalPerDay, 1678.5);
assert.equal(mifflin.moderateDeficitKcalPerDay, 1478.5);
assert.equal(mifflin.leanSurplusKcalPerDay, 2228.5);
assert.ok(Math.abs(mifflin.macros.proteinGrams - 148.3875) < 1e-9);
assert.ok(Math.abs(mifflin.macros.carbohydrateGrams - 197.85) < 1e-9);
assert.ok(Math.abs(mifflin.macros.fatGrams - 65.95) < 1e-9);
assert.equal(mifflin.formulaLabel, "Mifflin–St Jeor");

const harris = calculateCalorieTargets({ ...common, formula: "harris-benedict" });
assert.ok(Math.abs(harris.restingKcalPerDay - 1695.667) < 1e-9);
assert.equal(harris.maintenanceKcalPerDay, harris.restingKcalPerDay * 1.2);

const katch = calculateCalorieTargets({ ...common, formula: "katch-mcardle", bodyFatPercent: 20 });
assert.ok(Math.abs(katch.restingKcalPerDay - 1579.6) < 1e-9);
assert.equal(katch.maintenanceKcalPerDay, 1895.52);
assert.equal(katch.formulaLabel, "Katch–McArdle");
assert.throws(() => calculateCalorieTargets({ ...common, formula: "katch-mcardle" }), /body-fat/i);
assert.equal(calculateCalorieTargets({ ...common, formula: "mifflin", bodyFatPercent: 20 }).restingKcalPerDay, mifflin.restingKcalPerDay, "Body-fat input must not affect formulas that do not use it");
assert.ok(Math.abs(calculateCalorieTargets({ ...common, formula: "katch-mcardle", coefficient: "", bodyFatPercent: 20 }).restingKcalPerDay - 1579.6) < 1e-9, "Katch–McArdle must not require a male/female coefficient");

for (const activity of ACTIVITY_PRESETS) {
  const result = calculateCalorieTargets({ ...common, formula: "mifflin", activityId: activity.id });
  assert.equal(result.maintenanceKcalPerDay, result.restingKcalPerDay * activity.multiplier);
}
assert.throws(() => calculateCalorieTargets({ ...common, age: 17, formula: "mifflin" }), /18 or older/i);
assert.throws(() => calculateCalorieTargets({ ...common, age: 121, formula: "mifflin" }), /age/i);
assert.throws(() => calculateCalorieTargets({ ...common, age: 30.5, formula: "mifflin" }), /whole number/i);
assert.throws(() => calculateCalorieTargets({ ...common, weight: 0, formula: "mifflin" }), /weight/i);
assert.throws(() => calculateCalorieTargets({ ...common, height: 0, formula: "mifflin" }), /height/i);
assert.throws(() => calculateCalorieTargets({ ...common, coefficient: "other", formula: "mifflin" }), /coefficient/i);
assert.throws(() => calculateCalorieTargets({ ...common, formula: "unknown" }), /formula/i);
assert.throws(() => calculateCalorieTargets({ ...common, activityId: "unknown", formula: "mifflin" }), /activity/i);
assert.throws(() => calculateCalorieTargets({ ...common, formula: "katch-mcardle", bodyFatPercent: 0 }), /body-fat/i);
assert.throws(() => calculateCalorieTargets({ ...common, formula: "katch-mcardle", bodyFatPercent: 71 }), /body-fat/i);
assert.throws(() => calculateCalorieTargets({ ...common, weightUnit: "stone", formula: "mifflin" }), /weight unit/i);
assert.throws(() => calculateCalorieTargets({ ...common, heightUnit: "inches", formula: "mifflin" }), /height unit/i);

const imperial = calculateCalorieTargets({
  age: 30, weight: 154.323583529414, weightUnit: "lb",
  heightUnit: "ft-in", heightFeet: 5, heightInches: 8.89763779527559,
  coefficient: "male", formula: "mifflin", activityId: "sedentary"
});
assert.ok(Math.abs(imperial.restingKcalPerDay - mifflin.restingKcalPerDay) < 1e-6);


const femaleMifflin = calculateCalorieTargets({ ...common, formula: "mifflin", coefficient: "female" });
assert.equal(femaleMifflin.restingKcalPerDay, 1482.75);
const femaleHarris = calculateCalorieTargets({ ...common, formula: "harris-benedict", coefficient: "female" });
assert.ok(Math.abs(femaleHarris.restingKcalPerDay - 1507.133) < 1e-9);

let simulatedCases = 0;
for (let i = 0; i < 5000; i += 1) {
  const formula = ["mifflin", "harris-benedict", "katch-mcardle"][i % 3];
  const activityId = ACTIVITY_PRESETS[i % ACTIVITY_PRESETS.length].id;
  const scenario = {
    age: 18 + (i % 83),
    weight: 45 + (i % 156) * 0.7,
    weightUnit: "kg",
    height: 140 + (i % 81) * 0.8,
    heightUnit: "cm",
    coefficient: i % 2 ? "male" : "female",
    activityId,
    formula,
    bodyFatPercent: 8 + (i % 50) * 0.7
  };
  const value = calculateCalorieTargets(scenario);
  assert.ok(Number.isFinite(value.restingKcalPerDay) && value.restingKcalPerDay > 0);
  assert.ok(Number.isFinite(value.maintenanceKcalPerDay) && value.maintenanceKcalPerDay > 0);
  assert.equal(value.maintenanceKcalPerDay, value.restingKcalPerDay * value.activity.multiplier);
  assert.equal(value.mildDeficitKcalPerDay, value.maintenanceKcalPerDay - 300);
  assert.equal(value.moderateDeficitKcalPerDay, value.maintenanceKcalPerDay - 500);
  assert.equal(value.leanSurplusKcalPerDay, value.maintenanceKcalPerDay + 250);
  assert.ok(Number.isFinite(value.macros.proteinGrams));
  assert.ok(Number.isFinite(value.macros.carbohydrateGrams));
  assert.ok(Number.isFinite(value.macros.fatGrams));
  simulatedCases += 1;
}
assert.equal(simulatedCases, 5000);

const pagePath = path.join(__dirname, "..", "public", "calorie-calculator", "index.html");
assert.ok(fs.existsSync(pagePath), "Calorie Calculator page must be generated");
const html = fs.readFileSync(pagePath, "utf8");
assert.match(html, /<title>Calorie Calculator: TDEE, BMR &amp; Macros \| CalculatesAll<\/title>/, "SEO finalization must preserve the upgraded calorie page title");
assert.match(html, /<meta property="og:title" content="Calorie Calculator: TDEE, BMR &amp; Macros \| CalculatesAll">/, "Open Graph title must match the upgraded calorie page title");
assert.doesNotMatch(html, /<title>Calorie Calculator \| Maintenance &amp; TDEE \| CalculatesAll<\/title>/, "The obsolete calorie page title must not be restored by SEO finalization");
for (const phrase of [
  "How many calories do I need", "total daily energy expenditure", "BMR",
  "calorie deficit", "maintenance calories", "activity level",
  "Why can calorie calculators give different results", "pregnancy",
  "not medical advice", "browser", "Mifflin–St Jeor", "Revised Harris–Benedict", "Katch–McArdle"
]) assert.ok(html.toLowerCase().includes(phrase.toLowerCase()), "Page content must cover: " + phrase);
assert.match(html, /adults aged 18 or older/i);
assert.match(html, /not intended for pregnancy or breastfeeding/i);
assert.match(html, /does not send.*(measurements|inputs)|measurements.*not sent/i);
assert.match(html, /https:\/\/pubmed\.ncbi\.nlm\.nih\.gov\/2305711/);
assert.match(html, /https:\/\/pubmed\.ncbi\.nlm\.nih\.gov\/6741850/);
assert.match(html, /Katch.*McArdle|McArdle.*Katch/i);
assert.match(html, /<link rel="canonical" href="https:\/\/calculateallinone\.vercel\.app\/calorie-calculator\/">/);
assert.match(html, /calorie-calculator\.js\?v=[a-f0-9]{12}/);
assert.doesNotMatch(html, /cal-pregnancy-weeks|cal-breastfeeding-stage|cal-eligibility/);
assert.doesNotMatch(html, /<form[^>]+action=/i);
assert.match(fs.readFileSync(path.join(__dirname, "..", "public", "sitemap.xml"), "utf8"), /https:\/\/calculateallinone\.vercel\.app\/calorie-calculator\//);
console.log("Three-formula calorie engine and generated-page contracts: PASS");
