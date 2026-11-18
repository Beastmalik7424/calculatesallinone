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
assert.equal(mifflin.macros.proteinGrams, 148.3875);
assert.equal(mifflin.macros.carbohydrateGrams, 197.85);
assert.equal(mifflin.macros.fatGrams, 65.95);
assert.equal(mifflin.formulaLabel, "Mifflin–St Jeor");

const harris = calculateCalorieTargets({ ...common, formula: "harris-benedict" });
assert.ok(Math.abs(harris.restingKcalPerDay - 1695.667) < 1e-9);
assert.equal(harris.maintenanceKcalPerDay, harris.restingKcalPerDay * 1.2);

const katch = calculateCalorieTargets({ ...common, formula: "katch-mcardle", bodyFatPercent: 20 });
assert.equal(katch.restingKcalPerDay, 1579.6);
assert.equal(katch.maintenanceKcalPerDay, 1895.52);
assert.equal(katch.formulaLabel, "Katch–McArdle");
assert.throws(() => calculateCalorieTargets({ ...common, formula: "katch-mcardle" }), /body fat/i);
assert.throws(() => calculateCalorieTargets({ ...common, formula: "mifflin", bodyFatPercent: 20 }), /only.*Katch|Katch.*only/i);

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
assert.throws(() => calculateCalorieTargets({ ...common, formula: "katch-mcardle", bodyFatPercent: 0 }), /body fat/i);
assert.throws(() => calculateCalorieTargets({ ...common, formula: "katch-mcardle", bodyFatPercent: 71 }), /body fat/i);
assert.throws(() => calculateCalorieTargets({ ...common, weightUnit: "stone", formula: "mifflin" }), /weight unit/i);
assert.throws(() => calculateCalorieTargets({ ...common, heightUnit: "inches", formula: "mifflin" }), /height unit/i);

const imperial = calculateCalorieTargets({
  age: 30, weight: 154.323583529414, weightUnit: "lb",
  height: 5 * 12 + 8.89763779527559, heightUnit: "in",
  coefficient: "male", formula: "mifflin", activityId: "sedentary"
});
assert.ok(Math.abs(imperial.restingKcalPerDay - mifflin.restingKcalPerDay) < 1e-6);

const pagePath = path.join(__dirname, "..", "public", "calorie-calculator", "index.html");
assert.ok(fs.existsSync(pagePath), "Calorie Calculator page must be generated");
const html = fs.readFileSync(pagePath, "utf8");
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
