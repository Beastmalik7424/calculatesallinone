(function (root) {
  "use strict";

  // These activity factors are practical calculator assumptions, not measurements.
  var LB_TO_KG = 0.45359237;
  var IN_TO_CM = 2.54;
  var ACTIVITY_PRESETS = Object.freeze([
    Object.freeze({ id: "sedentary", label: "Sedentary", multiplier: 1.2, description: "Mostly seated work and little planned movement." }),
    Object.freeze({ id: "light", label: "Light activity", multiplier: 1.375, description: "Some walking or light exercise, with mostly light daily movement." }),
    Object.freeze({ id: "moderate", label: "Moderate activity", multiplier: 1.55, description: "Regular moderate exercise and a generally active daily routine." }),
    Object.freeze({ id: "very_active", label: "Very active", multiplier: 1.725, description: "Frequent hard exercise or a physically demanding job." }),
    Object.freeze({ id: "extra_active", label: "Extra active", multiplier: 1.9, description: "Very demanding daily physical work or training." })
  ]);

  function finiteNumber(value, label) {
    if (value === null || value === undefined || (typeof value === "string" && value.trim() === "")) {
      throw new Error("Enter " + label + ".");
    }
    var parsed = typeof value === "number" ? value : Number(value);
    if (!Number.isFinite(parsed)) throw new Error("Enter a valid number for " + label + ".");
    return parsed;
  }

  function calculateCalorieTargets(input) {
    input = input || {};
    var age = finiteNumber(input.age, "your age");
    if (!Number.isInteger(age)) throw new Error("Age must be a whole number of years.");
    if (age < 18) throw new Error("This calculator is for adults aged 18 or older.");
    if (age > 120) throw new Error("Enter an age from 18 to 120 years.");

    if (input.weightUnit !== "kg" && input.weightUnit !== "lb") {
      throw new Error("Choose a supported weight unit (kg or lb).");
    }
    var enteredWeight = finiteNumber(input.weight, "your weight");
    var weightKg = input.weightUnit === "lb" ? enteredWeight * LB_TO_KG : enteredWeight;
    if (!Number.isFinite(weightKg) || weightKg < 20 || weightKg > 500) {
      throw new Error("Enter a weight that converts to 20–500 kg. This is an input check, not a medical range.");
    }

    var heightCm;
    if (input.heightUnit === "cm") {
      heightCm = finiteNumber(input.height, "your height in centimetres");
    } else if (input.heightUnit === "ft-in") {
      var feet = finiteNumber(input.heightFeet, "height in feet");
      var inches = finiteNumber(input.heightInches, "remaining height in inches");
      if (!Number.isInteger(feet) || feet < 3 || feet > 8) throw new Error("Enter a whole number of feet from 3 to 8.");
      if (inches < 0 || inches >= 12) throw new Error("Remaining inches must be at least 0 and less than 12.");
      heightCm = (feet * 12 + inches) * IN_TO_CM;
    } else {
      throw new Error("Choose a supported height unit (cm or feet and inches).");
    }
    if (!Number.isFinite(heightCm) || heightCm < 100 || heightCm > 250) {
      throw new Error("Enter a height that converts to 100–250 cm. This is an input check, not a medical range.");
    }

    var activity = ACTIVITY_PRESETS.find(function (item) { return item.id === input.activityId; });
    if (!activity) throw new Error("Choose an activity level.");

    var formula = input.formula || "mifflin";
    var coefficient = input.coefficient;
    var resting;
    var formulaLabel;
    if (formula === "mifflin") {
      if (coefficient !== "male" && coefficient !== "female") throw new Error("Choose the equation coefficient for Mifflin–St Jeor.");
      resting = 10 * weightKg + 6.25 * heightCm - 5 * age + (coefficient === "male" ? 5 : -161);
      formulaLabel = "Mifflin–St Jeor";
    } else if (formula === "harris-benedict") {
      if (coefficient !== "male" && coefficient !== "female") throw new Error("Choose the equation coefficient for Revised Harris–Benedict.");
      resting = coefficient === "male"
        ? 88.362 + 13.397 * weightKg + 4.799 * heightCm - 5.677 * age
        : 447.593 + 9.247 * weightKg + 3.098 * heightCm - 4.330 * age;
      formulaLabel = "Revised Harris–Benedict";
    } else if (formula === "katch-mcardle") {
      var bodyFat = finiteNumber(input.bodyFatPercent, "your body-fat percentage");
      if (bodyFat < 3 || bodyFat > 70) throw new Error("Enter a body-fat percentage from 3 to 70.");
      var leanMassKg = weightKg * (1 - bodyFat / 100);
      resting = 370 + 21.6 * leanMassKg;
      formulaLabel = "Katch–McArdle";
    } else {
      throw new Error("Choose one of the three supported formulas.");
    }

    var maintenance = resting * activity.multiplier;
    if (!Number.isFinite(resting) || !Number.isFinite(maintenance) || resting <= 0 || maintenance <= 0) {
      throw new Error("These entries do not produce a usable estimate. Check your values and units.");
    }

    // Illustrative targets only. They are not individualized diet prescriptions.
    var macros = {
      split: "30% protein / 40% carbohydrates / 30% fat",
      proteinPercent: 30,
      carbohydratePercent: 40,
      fatPercent: 30,
      proteinGrams: maintenance * 0.30 / 4,
      carbohydrateGrams: maintenance * 0.40 / 4,
      fatGrams: maintenance * 0.30 / 9
    };

    return Object.freeze({
      formula: formula,
      formulaLabel: formulaLabel,
      coefficient: coefficient || null,
      age: age,
      weightKg: weightKg,
      heightCm: heightCm,
      restingKcalPerDay: resting,
      maintenanceKcalPerDay: maintenance,
      mildDeficitKcalPerDay: maintenance - 300,
      moderateDeficitKcalPerDay: maintenance - 500,
      leanSurplusKcalPerDay: maintenance + 250,
      activity: activity,
      macros: Object.freeze(macros)
    });
  }

  function formatKcal(value) {
    return new Intl.NumberFormat("en-US", { maximumFractionDigits: 1, minimumFractionDigits: 1 }).format(value);
  }

  function formatGrams(value) {
    return new Intl.NumberFormat("en-US", { maximumFractionDigits: 1, minimumFractionDigits: 1 }).format(value);
  }

  var api = Object.freeze({
    LB_TO_KG: LB_TO_KG,
    IN_TO_CM: IN_TO_CM,
    ACTIVITY_PRESETS: ACTIVITY_PRESETS,
    calculateCalorieTargets: calculateCalorieTargets,
    formatKcal: formatKcal,
    formatGrams: formatGrams
  });
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.CalorieCalculator = api;

  function initialize(doc) {
    var form = doc.getElementById("calorie-form");
    if (!form) return;
    var byId = function (id) { return doc.getElementById(id); };
    var formulaSelect = byId("cal-formula");
    var bodyFatField = byId("cal-body-fat-field");
    var bodyFatInput = byId("cal-body-fat");
    var heightUnit = byId("cal-height-unit");
    var metricHeight = byId("cal-height-metric");
    var imperialHeight = byId("cal-height-imperial");
    var heightInput = byId("cal-height");
    var heightFeet = byId("cal-height-ft");
    var heightInches = byId("cal-height-in");
    var error = byId("calorie-error");
    var result = byId("calorie-result");

    function clearOutput() {
      error.textContent = "";
      result.hidden = true;
      result.replaceChildren();
    }

    function updateFormulaFields() {
      var usesBodyFat = formulaSelect.value === "katch-mcardle";
      bodyFatField.hidden = !usesBodyFat;
      bodyFatInput.disabled = !usesBodyFat;
      bodyFatInput.required = usesBodyFat;
      if (!usesBodyFat) bodyFatInput.value = "";
      clearOutput();
    }

    function updateHeightFields() {
      var usesImperial = heightUnit.value === "ft-in";
      metricHeight.hidden = usesImperial;
      imperialHeight.hidden = !usesImperial;
      heightInput.disabled = usesImperial;
      heightFeet.disabled = !usesImperial;
      heightInches.disabled = !usesImperial;
      clearOutput();
    }

    function appendText(parent, tag, className, text) {
      var node = doc.createElement(tag);
      if (className) node.className = className;
      node.textContent = text;
      parent.appendChild(node);
      return node;
    }

    function appendMetric(parent, label, value, detail) {
      var card = doc.createElement("div");
      card.className = "min-w-0 rounded-lg border border-stone-200 bg-white p-3 dark:border-stone-700 dark:bg-stone-900";
      appendText(card, "p", "text-xs font-medium text-stone-600 dark:text-stone-300", label);
      appendText(card, "p", "mt-1 text-xl font-bold tabular-nums text-stone-950 dark:text-white", formatKcal(value) + " kcal/day");
      if (detail) appendText(card, "p", "mt-1 text-xs text-stone-600 dark:text-stone-300", detail);
      parent.appendChild(card);
    }

    function calculate() {
      clearOutput();
      try {
        var input = {
          age: byId("cal-age").value,
          weight: byId("cal-weight").value,
          weightUnit: byId("cal-weight-unit").value,
          heightUnit: heightUnit.value,
          height: heightInput.value,
          heightFeet: heightFeet.value,
          heightInches: heightInches.value,
          coefficient: byId("cal-coefficient").value,
          formula: formulaSelect.value,
          bodyFatPercent: bodyFatInput.value,
          activityId: byId("cal-activity").value
        };
        var data = calculateCalorieTargets(input);

        appendText(result, "h3", "text-lg font-semibold", "Your estimated daily calories");
        appendText(result, "p", "mt-1 text-sm text-stone-700 dark:text-stone-300", "Formula: " + data.formulaLabel + ". Activity assumption: " + data.activity.label + " (" + data.activity.multiplier + "×).");
        var grid = doc.createElement("div");
        grid.className = "mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2";
        appendMetric(grid, "Maintenance calories (TDEE)", data.maintenanceKcalPerDay, "Estimated daily energy expenditure");
        appendMetric(grid, "Resting estimate (BMR / REE)", data.restingKcalPerDay, "The selected equation's resting-energy estimate");
        appendMetric(grid, "Mild deficit (−300 kcal)", data.mildDeficitKcalPerDay, "Arithmetic comparison with maintenance");
        appendMetric(grid, "Moderate deficit (−500 kcal)", data.moderateDeficitKcalPerDay, "Arithmetic comparison with maintenance");
        appendMetric(grid, "Lean surplus (+250 kcal)", data.leanSurplusKcalPerDay, "Arithmetic comparison with maintenance");
        result.appendChild(grid);

        var macroBox = doc.createElement("div");
        macroBox.className = "mt-3 rounded-lg border border-stone-200 p-3 dark:border-stone-700";
        appendText(macroBox, "h4", "font-semibold", "Maintenance macro split");
        appendText(macroBox, "p", "mt-1 text-sm", "Illustrative 30% protein, 40% carbohydrates and 30% fat split of maintenance calories.");
        var macroGrid = doc.createElement("div");
        macroGrid.className = "mt-2 grid grid-cols-3 gap-2 text-sm";
        appendText(macroGrid, "p", "", "Protein: " + formatGrams(data.macros.proteinGrams) + " g");
        appendText(macroGrid, "p", "", "Carbs: " + formatGrams(data.macros.carbohydrateGrams) + " g");
        appendText(macroGrid, "p", "", "Fat: " + formatGrams(data.macros.fatGrams) + " g");
        macroBox.appendChild(macroGrid);
        result.appendChild(macroBox);
        appendText(result, "p", "mt-3 text-xs leading-5 text-stone-700 dark:text-stone-300", "These are population-equation estimates, not measured metabolism or personal diet instructions. The deficit, surplus and macro figures are arithmetic examples only. They are not suitable for everyone and do not guarantee weight change.");
        var source = doc.createElement("p");
        source.className = "mt-2 text-xs";
        source.appendChild(doc.createTextNode("Formula references: "));
        [
          ["Mifflin–St Jeor", "https://pubmed.ncbi.nlm.nih.gov/2305711/"],
          ["Revised Harris–Benedict", "https://pubmed.ncbi.nlm.nih.gov/6741850/"]
        ].forEach(function (item, index) {
          if (index) source.appendChild(doc.createTextNode(" · "));
          var link = doc.createElement("a");
          link.href = item[1];
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.textContent = item[0];
          source.appendChild(link);
        });
        result.appendChild(source);
        result.hidden = false;
      } catch (exception) {
        error.textContent = exception && exception.message ? exception.message : "The estimate could not be calculated. Check your entries and try again.";
      }
    }

    heightUnit.addEventListener("change", updateHeightFields);
    formulaSelect.addEventListener("change", updateFormulaFields);
    form.querySelectorAll("input, select").forEach(function (control) {
      control.addEventListener("input", clearOutput);
      control.addEventListener("change", clearOutput);
    });
    byId("cal-calculate").addEventListener("click", calculate);
    byId("cal-reset").addEventListener("click", function () {
      ["cal-age", "cal-weight", "cal-height", "cal-height-ft", "cal-height-in", "cal-body-fat"].forEach(function (id) { byId(id).value = ""; });
      byId("cal-weight-unit").value = "kg";
      heightUnit.value = "cm";
      byId("cal-coefficient").value = "";
      byId("cal-activity").value = "";
      formulaSelect.value = "mifflin";
      updateHeightFields();
      updateFormulaFields();
      clearOutput();
      byId("cal-age").focus();
    });
    form.addEventListener("keydown", function (event) {
      if (event.key === "Enter" && event.target && event.target.tagName === "INPUT") {
        event.preventDefault();
        calculate();
      }
    });
    updateHeightFields();
    updateFormulaFields();
  }

  if (typeof document !== "undefined") initialize(document);
})(typeof globalThis !== "undefined" ? globalThis : this);
