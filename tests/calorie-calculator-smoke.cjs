"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const pagePath = path.join(__dirname, "..", "public", "calorie-calculator", "index.html");
assert.ok(fs.existsSync(pagePath), "Adult Calorie Calculator page must be generated at /calorie-calculator/");

const {
  calculateMaintenanceCalories,
  ACTIVITY_PRESETS,
  formatKcal,
  formatEquationKcal,
  calculateLifeStageCalories
} = require("../static/calorie-calculator.js");

const male = calculateMaintenanceCalories({
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary", pregnancyStatus: "no"
});
assert.equal(male.restingKcalPerDay, 1648.75);
assert.equal(male.maintenanceKcalPerDay, 1978.5);
assert.equal(formatKcal(1648.75), "1,648.8");
assert.equal(formatEquationKcal(1648.75), "1,648.75", "Calculation working must show the unrounded REE value used by the formula");
assert.equal(formatEquationKcal(1482.75), "1,482.75", "Female coefficient calculation working must retain full source precision");
assert.equal(formatKcal(1648.7499999999986), "1,648.8", "Binary conversion noise must not flip an exact half-tenth display boundary");
assert.equal(formatKcal(1648.74), "1,648.7", "Values below the rounding boundary must remain below it");
assert.equal(formatKcal(1648.75), "1,648.8");
assert.equal(formatKcal(1648.7499999999998), "1,648.8", "Imperial conversion floating-point drift must not change display rounding");
assert.equal(formatKcal(1648.74), "1,648.7", "Values below the rounding boundary must remain below it");

const maleWithoutPregnancyStatus = calculateMaintenanceCalories({
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "male", activityId: "sedentary"
});
assert.equal(maleWithoutPregnancyStatus.maintenanceKcalPerDay, 1978.5,
  "Male coefficient must not require a pregnancy/breastfeeding status");

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
assert.equal(formatKcal(imperial.restingKcalPerDay), "1,648.8", "Actual imperial conversion noise must not change the REE display rounding");
assert.equal(formatKcal(imperial.maintenanceKcalPerDay), "1,978.5", "Actual imperial conversion noise must not change maintenance display rounding");

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
const lifeStageBase = {
  age: 30, weight: 70, weightUnit: "kg", heightUnit: "cm", heightCm: 175,
  coefficient: "female", lifeStageActivityId: "inactive",
  pregnancyWeeks: 20, prePregnancyWeight: 70, breastfeedingStage: "exclusive_0_6"
};
const bothLifeStages = calculateLifeStageCalories({ ...lifeStageBase, pregnancyStatus: "both" });
assert.equal(bothLifeStages.pregnancy.eerKcalPerDay, 2363.2,
  "Pregnancy estimate must use the 2023 National Academies second-trimester equation and normal pre-pregnancy BMI deposition");
assert.equal(bothLifeStages.breastfeeding.eerKcalPerDay, 2595.3,
  "Exclusive breastfeeding estimate must use the 2023 National Academies 0–6 month equation");
assert.equal(bothLifeStages.pregnancy.method, "National Academies DRI 2023, Table 5-17");
assert.equal(bothLifeStages.breastfeeding.method, "National Academies DRI 2023, Table 5-18");
assert.equal(bothLifeStages.combinedTargetKcalPerDay, null,
  "Separate pregnancy and breastfeeding estimates must never be added into an unsupported combined target");
const firstTrimester = calculateLifeStageCalories({ ...lifeStageBase, pregnancyStatus: "pregnant", pregnancyWeeks: 10 });
assert.equal(firstTrimester.pregnancy.eerKcalPerDay, 2195.3,
  "First trimester must use the non-pregnant adult female TEE equation without a pregnancy increment");
const thirdTrimester = calculateLifeStageCalories({ ...lifeStageBase, pregnancyStatus: "pregnant", pregnancyWeeks: 32 });
assert.equal(thirdTrimester.pregnancy.eerKcalPerDay, 2473.12);
const laterBreastfeeding = calculateLifeStageCalories({ ...lifeStageBase, pregnancyStatus: "breastfeeding", breastfeedingStage: "partial_7_12" });
assert.equal(laterBreastfeeding.breastfeeding.eerKcalPerDay, 2575.3,
  "Partial breastfeeding 7–12 months must use the 380 kcal/day increment");
invalidLifeStage({ ...lifeStageBase, age: 18, pregnancyStatus: "pregnant" }, /19 years or older/);
invalidLifeStage({ ...lifeStageBase, pregnancyStatus: "pregnant", pregnancyWeeks: 0 }, /pregnancy weeks/i);
invalidLifeStage({ ...lifeStageBase, pregnancyStatus: "pregnant", prePregnancyWeight: 0 }, /pre-pregnancy weight/i);
invalidLifeStage({ ...lifeStageBase, pregnancyStatus: "breastfeeding", breastfeedingStage: "" }, /breastfeeding stage/i);
invalidLifeStage({ ...lifeStageBase, pregnancyStatus: "both", lifeStageActivityId: "extra_active" }, /activity category/i);
function invalidLifeStage(input, pattern) {
  assert.throws(() => calculateLifeStageCalories(input), pattern);
}
invalid({ ...base, coefficient: "female", pregnancyStatus: "prefer_not_to_say" }, /select “Neither applies”/i);
invalid({ ...base, coefficient: "female", pregnancyStatus: "not_selected" }, /select/i);
invalid({ ...base, coefficient: "female", pregnancyStatus: undefined }, /select a pregnancy and breastfeeding status/i);
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
assert.match(html, /<title>[^<]*TDEE[^<]*<\/title>/, "Final SEO-normalized page title must retain the TDEE search intent within the title-length limit");
assert.ok(html.includes("Calorie Calculator") && html.includes("Maintenance") && html.includes("TDEE"), "Page metadata and visible content must cover calorie, maintenance and TDEE intent naturally");
assert.ok(html.includes("How many calories do I need to maintain my weight?"), "Visible FAQ must answer the core maintenance-calorie query");
assert.ok(html.includes("https://www.ncbi.nlm.nih.gov/books/NBK591031/"), "Page must cite the National Academies energy-expenditure definitions");
assert.match(html, /Mifflin–St Jeor/);
assert.match(html, /498 healthy adults/);
assert.match(html, /pregnancy and breastfeeding estimates use separate/i);
assert.match(html, /National Academies DRI 2023/);
assert.match(html, /not a combined calorie target/i);
assert.match(html, /competitive athletes/i, "Page must explain the limitations for competitive athletes");
assert.match(html, /metabolic conditions/i, "Page must explain the limitations for metabolic conditions");
assert.match(html, /https:\/\/www\.mayoclinic\.org\/healthy-lifestyle\/weight-loss\/in-depth\/calorie-calculator\/itt-20402304/, "Page must cite Mayo Clinic safety guidance");
assert.match(html, /https:\/\/www\.nal\.usda\.gov\/human-nutrition-and-food-safety\/dri-calculator/, "Page must link to the official DRI calculator reference");
assert.match(html, /https:\/\/www\.nationalacademies\.org\/read\/26818\/chapter\/7/);
assert.match(html, /cal-pregnancy-weeks/);
assert.match(html, /cal-breastfeeding-stage/);
assert.match(html, /PAL 1\.00–&lt;1\.53/);
assert.match(html, /This is not a combined calorie target/);
assert.match(html, /US and Canadian reference populations/);
assert.match(html, /excluded studies from non-high-income countries/i, "Page must disclose the National Academies evidence-population exclusion");
assert.match(html, /not been validated for Pakistan/i, "Page must not imply that the US/Canada DRI model is validated for Pakistan");
assert.match(html, /Type 1 and Type 2 diabetes/i, "Page must disclose source exclusion of chronic disease participants");
assert.match(html, /World Bank classifies Pakistan as a lower-middle-income economy/i, "Pakistan applicability limitation must be supported by the World Bank classification");
assert.match(html, /https:\/\/datahelpdesk\.worldbank\.org\/knowledgebase\/articles\/906519-world-bank-country-and-lending-groups/);
assert.match(html, /do not rely on this estimate for treatment or dietary decisions/i, "Page must warn against clinical reliance for chronic conditions");
assert.match(html, /CDC pregnancy guidance/i, "Page must include independent CDC pregnancy context");
assert.match(html, /CDC breastfeeding guidance/i, "Page must include independent CDC breastfeeding context");
assert.match(html, /not interchangeable with the equations/i, "Page must distinguish CDC public guidance from the DRI equation outputs");
assert.match(html, /330–400 additional kcal\/day/i, "Page must accurately cite CDC breastfeeding context");
assert.match(html, /340 additional kcal\/day.*450 additional kcal\/day/i, "Page must accurately cite CDC pregnancy context");
const calculatorJs = fs.readFileSync(path.join(__dirname, "..", "static", "calorie-calculator.js"), "utf8");
assert.match(calculatorJs, /eligibility\.addEventListener\("change",updateEligibility\)/,
  "Changing pregnancy/breastfeeding status must reveal the correct stage-specific inputs");
assert.match(calculatorJs, /combinedTargetKcalPerDay:null/,
  "The life-stage calculator must never expose an unsupported combined target");
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
