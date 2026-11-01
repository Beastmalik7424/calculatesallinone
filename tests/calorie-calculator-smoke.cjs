"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const pagePath = path.join(__dirname, "..", "public", "calorie-calculator", "index.html");
assert.ok(fs.existsSync(pagePath), "Adult Calorie Calculator page must be generated at /calorie-calculator/");

const {
  calculateMaintenanceCalories,
  ACTIVITY_PRESETS,
  formatKcal
} = require("../static/calorie-calculator.js");

const male = calculateMaintenanceCalories({
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
});
assert.equal(male.restingKcalPerDay, 1648.75);
assert.equal(male.maintenanceKcalPerDay, 1978.5);
assert.equal(formatKcal(1648.75), "1,648.8");
assert.equal(formatKcal(1648.7499999999986), "1,648.8", "Binary conversion noise must not flip an exact half-tenth display boundary");
assert.equal(formatKcal(1648.74), "1,648.7", "Values below the rounding boundary must remain below it");
assert.equal(formatKcal(1648.75), "1,648.8");
assert.equal(formatKcal(1648.7499999999998), "1,648.8", "Imperial conversion floating-point drift must not change display rounding");
assert.equal(formatKcal(1648.74), "1,648.7", "Values below the rounding boundary must remain below it");

const female = calculateMaintenanceCalories({
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "female", activityId: "sedentary", pregnancyStatus: "no"
});
assert.equal(female.restingKcalPerDay, 1482.75);
assert.equal(female.maintenanceKcalPerDay, 1779.3);
assert.equal(male.restingKcalPerDay - female.restingKcalPerDay, 166);

const expectedActivities = {
  sedentary: 1.2,
  light: 1.375,
  moderate: 1.55,
  very_active: 1.725,
  extra_active: 1.9
};
assert.deepEqual(
  Object.fromEntries(ACTIVITY_PRESETS.map(item => [item.id, item.multiplier])),
  expectedActivities
);
for (const preset of ACTIVITY_PRESETS) {
  assert.equal(preset.version, "1.0", "Every activity assumption must have a version");
  assert.match(preset.source, /application-defined/i, "Every activity assumption must identify its source");
  assert.match(preset.limitations, /approximate/i, "Every activity assumption must state its limitation");
}
for (const [activityId, multiplier] of Object.entries(expectedActivities)) {
  const result = calculateMaintenanceCalories({
    age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
    coefficient: "male", activityId, pregnancyStatus: "no"
  });
  assert.equal(result.maintenanceKcalPerDay, 1648.75 * multiplier);
  assert.equal(result.activity.multiplier, multiplier);
}

const imperial = calculateMaintenanceCalories({
  age: 30, weight: 154.323583529414, weightUnit: "lb",
  heightUnit: "ft-in", heightFeet: 5, heightInches: 8.89763779527559,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
});
assert.ok(Math.abs(imperial.restingKcalPerDay - male.restingKcalPerDay) < 0.000001);
assert.ok(Math.abs(imperial.maintenanceKcalPerDay - male.maintenanceKcalPerDay) < 0.000001);

const age18 = calculateMaintenanceCalories({
  age: 18, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
});
assert.equal(age18.outsideOriginalStudyAgeRange, true);
const age79 = calculateMaintenanceCalories({
  age: 79, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
});
assert.equal(age79.outsideOriginalStudyAgeRange, true);
const age30 = calculateMaintenanceCalories({
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
});
assert.equal(age30.outsideOriginalStudyAgeRange, false);

function invalid(input, pattern) {
  assert.throws(() => calculateMaintenanceCalories(input), pattern);
}
const base = {
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
};
invalid({ ...base, age: 17 }, /18 or older/);
invalid({ ...base, age: 121 }, /age/i);
invalid({ ...base, age: NaN }, /age/i);
invalid({ ...base, age: Infinity }, /age/i);
invalid({ ...base, age: 30.5 }, /whole number/);
invalid({ ...base, weight: 0 }, /weight/i);
invalid({ ...base, weight: -1 }, /weight/i);
invalid({ ...base, weight: NaN }, /weight/i);
invalid({ ...base, weight: Infinity }, /weight/i);
invalid({ ...base, weight: 501 }, /weight/i);
invalid({ ...base, heightCm: 0 }, /height/i);
invalid({ ...base, heightCm: 99 }, /height/i);
invalid({ ...base, heightCm: 251 }, /height/i);
invalid({ ...base, coefficient: "other" }, /coefficient/i);
invalid({ ...base, activityId: "unknown" }, /activity/i);
invalid({ ...base, pregnancyStatus: "pregnant" }, /pregnancy or breastfeeding/i);
invalid({ ...base, pregnancyStatus: "breastfeeding" }, /pregnancy or breastfeeding/i);
invalid({ ...base, pregnancyStatus: "both" }, /pregnancy or breastfeeding/i);
invalid({ ...base, pregnancyStatus: "prefer_not_to_say" }, /pregnancy or breastfeeding/i);
invalid({ ...base, pregnancyStatus: "not_selected" }, /select/i);
invalid({ ...base, weightUnit: "stone" }, /weight unit/i);
invalid({ ...base, heightUnit: "inches" }, /height unit/i);
invalid({ ...base, weightUnit: "lb", weight: 1103 }, /weight/i);
invalid({
  ...base, heightUnit: "ft-in", heightFeet: 5, heightInches: 12
}, /inches/i);
invalid({
  ...base, heightUnit: "ft-in", heightFeet: 5, heightInches: -1
}, /inches/i);
invalid({
  ...base, heightUnit: "ft-in", heightFeet: 0, heightInches: 8
}, /feet/i);

const html = fs.readFileSync(pagePath, "utf8");
assert.match(html, /<html lang="en"/);
assert.match(html, /<form id="calorie-form"/i, "Calculator controls must use a semantic HTML form element");
assert.match(html, /<h1[^>]*>Adult Calorie Calculator<\/h1>/);
assert.match(html, /Mifflin–St Jeor/);
assert.match(html, /498 healthy adults/);
assert.match(html, /pregnancy or breastfeeding/);
assert.match(html, /has not been medically reviewed/i);
assert.match(html, /Site maintainer: Muhammad Fayyaz Adeel/);
assert.match(html, /No qualified medical professional has reviewed this calculator or its implementation/);
assert.match(html, /activity multipliers are consumer estimates/i);
assert.match(html, /https:\/\/pubmed\.ncbi\.nlm\.nih\.gov\/2305711\//);
assert.match(html, /https:\/\/www\.fao\.org\/4\/y5686e\/y5686e07\.htm/);
assert.match(html, /https:\/\/www\.niddk\.nih\.gov\/health-information\/weight-management\/body-weight-planner/);
assert.match(html, /<link rel="canonical" href="https:\/\/calculateallinone\.vercel\.app\/calorie-calculator\/">/);
assert.match(html, /calorie-calculator\.js/);
assert.doesNotMatch(html, /<form[^>]+action=/i);
assert.doesNotMatch(html, /name="(weight|height|age|calorie)"[^>]*value=/i);

const sitemap = fs.readFileSync(path.join(__dirname, "..", "public", "sitemap.xml"), "utf8");
assert.match(sitemap, /https:\/\/calculateallinone\.vercel\.app\/calorie-calculator\//);
const healthHub = fs.readFileSync(path.join(__dirname, "..", "public", "health", "index.html"), "utf8");
assert.match(healthHub, /href="\/calorie-calculator\//);
const home = fs.readFileSync(path.join(__dirname, "..", "public", "index.html"), "utf8");
assert.match(home, /href="\/calorie-calculator\//);
assert.ok(!fs.existsSync(path.join(__dirname, "..", "public", "ur", "calorie-calculator", "index.html")));

console.log("Adult calorie formula, validation, eligibility, page metadata and site integration: PASS");
