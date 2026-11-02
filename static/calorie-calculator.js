(function (root) {
"use strict";
var LB_TO_KG=0.45359237, IN_TO_CM=2.54;
var ACTIVITY_PRESETS=Object.freeze([
Object.freeze({id:"sedentary",label:"Sedentary",multiplier:1.2,description:"Mostly seated work and little planned movement.",version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}),
Object.freeze({id:"light",label:"Light activity",multiplier:1.375,description:"Some walking or light exercise, with mostly light daily movement.",version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}),
Object.freeze({id:"moderate",label:"Moderate activity",multiplier:1.55,description:"Regular moderate exercise and a generally active daily routine.",version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}),
Object.freeze({id:"very_active",label:"Very active",multiplier:1.725,description:"Frequent hard exercise or a physically demanding job.",version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}),
Object.freeze({id:"extra_active",label:"Extra active",multiplier:1.9,description:"Very demanding daily physical work or training.",version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."})
]);
function number(value,label){
 if(value===null||value===undefined||(typeof value==="string"&&value.trim()===""))throw new Error("Enter "+label+".");
 var n=typeof value==="number"?value:Number(value);
 if(!Number.isFinite(n))throw new Error("Enter a valid finite number for "+label+".");
 return n;
}
function calculateMaintenanceCalories(input){
 input=input||{};
 var age=number(input.age,"age");
 if(!Number.isInteger(age))throw new Error("Age must be a whole number of years.");
 if(age<18)throw new Error("This calculator is for adults aged 18 or older.");
 if(age>120)throw new Error("Enter an age from 18 to 120 years.");
 var coefficient=input.coefficient;
 if(coefficient!=="male"&&coefficient!=="female")throw new Error("Choose one of the published equation coefficients to continue.");
 if(coefficient==="female"){
  if(!["no","pregnant","breastfeeding","both","prefer_not_to_say"].includes(input.pregnancyStatus))throw new Error("Select a pregnancy and breastfeeding status.");
  if(input.pregnancyStatus==="prefer_not_to_say")throw new Error("To continue, select “Neither applies”. If you prefer not to disclose, no estimate will be calculated.");
  if(input.pregnancyStatus!=="no")throw new Error("This calculator is not intended for pregnancy or breastfeeding. It does not provide an ordinary maintenance estimate for these circumstances.");
 }
 if(input.weightUnit!=="kg"&&input.weightUnit!=="lb")throw new Error("Choose a supported weight unit (kg or lb).");
 var weight=number(input.weight,"weight");
 var weightKg=input.weightUnit==="lb"?weight*LB_TO_KG:weight;
 if(!Number.isFinite(weightKg)||weightKg<20||weightKg>500)throw new Error("Enter a weight that converts to 20–500 kg. This broad input guardrail catches likely entry errors; it is not a clinical range.");
 var heightCm;
 if(input.heightUnit==="cm")heightCm=number(input.heightCm,"height in centimetres");
 else if(input.heightUnit==="ft-in"){
  var feet=number(input.heightFeet,"height in feet"), inches=number(input.heightInches,"remaining height in inches");
  if(!Number.isInteger(feet)||feet<3||feet>8)throw new Error("Enter a whole number of feet from 3 to 8.");
  if(inches<0||inches>=12)throw new Error("Remaining inches must be at least 0 and less than 12.");
  heightCm=(feet*12+inches)*IN_TO_CM;
 }else throw new Error("Choose a supported height unit (cm or feet and inches).");
 if(!Number.isFinite(heightCm)||heightCm<100||heightCm>250)throw new Error("Enter a height that converts to 100–250 cm. This broad input guardrail catches likely entry errors; it is not a clinical range.");
 var activity=ACTIVITY_PRESETS.find(function(x){return x.id===input.activityId;});
 if(!activity)throw new Error("Choose one of the listed activity assumptions.");
 var resting=coefficient==="male"?(10*weightKg)+(6.25*heightCm)-(5*age)+5:(10*weightKg)+(6.25*heightCm)-(5*age)-161;
 var maintenance=resting*activity.multiplier;
 if(!Number.isFinite(resting)||!Number.isFinite(maintenance)||resting<=0||maintenance<=0)throw new Error("These entries do not produce a usable estimate. Check the values and units.");
 return Object.freeze({age:age,weightKg:weightKg,heightCm:heightCm,coefficient:coefficient,equation:"Mifflin–St Jeor (1990)",restingKcalPerDay:resting,maintenanceKcalPerDay:maintenance,activity:activity,outsideOriginalStudyAgeRange:age<19||age>78});
}

var DRI_ACTIVITY_CATEGORIES=Object.freeze(["inactive","low_active","active","very_active"]);
function calculateLifeStageCalories(input){
 input=input||{};
 var age=number(input.age,"age");
 if(!Number.isInteger(age)||age<19||age>120)throw new Error("The 2023 adult life-stage equations in this calculator are for ages 19 years or older.");
 if(input.coefficient!=="female")throw new Error("Choose the female coefficient for the National Academies adult pregnancy and lactation equations.");
 var status=input.pregnancyStatus;
 if(!["pregnant","breastfeeding","both"].includes(status))throw new Error("Choose pregnancy, breastfeeding, or both to calculate a life-stage estimate.");
 var pal=input.lifeStageActivityId;
 if(!DRI_ACTIVITY_CATEGORIES.includes(pal))throw new Error("Choose an official DRI activity category.");
 if(input.weightUnit!=="kg"&&input.weightUnit!=="lb")throw new Error("Choose a supported weight unit (kg or lb).");
 var weight=number(input.weight,"weight");
 var weightKg=input.weightUnit==="lb"?weight*LB_TO_KG:weight;
 if(!Number.isFinite(weightKg)||weightKg<20||weightKg>500)throw new Error("Enter a current weight that converts to 20–500 kg.");
 var heightCm;
 if(input.heightUnit==="cm")heightCm=number(input.heightCm,"height in centimetres");
 else if(input.heightUnit==="ft-in"){
  var feet=number(input.heightFeet,"height in feet"), inches=number(input.heightInches,"remaining height in inches");
  if(!Number.isInteger(feet)||feet<3||feet>8)throw new Error("Enter a whole number of feet from 3 to 8.");
  if(inches<0||inches>=12)throw new Error("Remaining inches must be at least 0 and less than 12.");
  heightCm=(feet*12+inches)*IN_TO_CM;
 }else throw new Error("Choose a supported height unit (cm or feet and inches).");
 if(!Number.isFinite(heightCm)||heightCm<100||heightCm>250)throw new Error("Enter a height that converts to 100–250 cm.");
 var baseByPal={
  inactive:584.90-(7.01*age)+(5.72*heightCm)+(11.71*weightKg),
  low_active:575.77-(7.01*age)+(6.60*heightCm)+(12.14*weightKg),
  active:710.25-(7.01*age)+(6.54*heightCm)+(12.34*weightKg),
  very_active:511.83-(7.01*age)+(9.07*heightCm)+(12.56*weightKg)
 };
 var baseEer=baseByPal[pal], pregnancy=null, breastfeeding=null;
 if(status==="pregnant"||status==="both"){
  var weeks=number(input.pregnancyWeeks,"pregnancy weeks");
  if(!Number.isInteger(weeks)||weeks<1||weeks>42)throw new Error("Pregnancy weeks must be a whole number from 1 to 42.");
  var pregnancyEer, pregnancyMethod, pregnancyFormula, trimester;
  if(weeks<=13){
   pregnancyEer=baseEer;
   pregnancyMethod="National Academies DRI 2023, Table 5-16";
   pregnancyFormula="First trimester: nonpregnant adult female TEE equation; no pregnancy energy-deposition increment.";
   trimester="First trimester";
  }else{
   var prepregWeight=number(input.prePregnancyWeight,"pre-pregnancy weight");
   var prepregWeightKg=input.weightUnit==="lb"?prepregWeight*LB_TO_KG:prepregWeight;
   if(!Number.isFinite(prepregWeightKg)||prepregWeightKg<20||prepregWeightKg>500)throw new Error("Pre-pregnancy weight must convert to 20–500 kg.");
   var prepregBmi=prepregWeightKg/Math.pow(heightCm/100,2);
   if(!Number.isFinite(prepregBmi)||prepregBmi<10||prepregBmi>80)throw new Error("The pre-pregnancy BMI cannot be calculated from these entries. Check height and pre-pregnancy weight.");
   var deposition=prepregBmi<18.5?300:prepregBmi<25?200:prepregBmi<30?150:-50;
   var pregnancyBase={
    inactive:1131.20-(2.04*age)+(0.34*heightCm)+(12.15*weightKg)+(9.16*weeks),
    low_active:693.35-(2.04*age)+(5.73*heightCm)+(10.20*weightKg)+(9.16*weeks),
    active:-223.84-(2.04*age)+(13.23*heightCm)+(8.15*weightKg)+(9.16*weeks),
    very_active:-779.72-(2.04*age)+(18.45*heightCm)+(8.73*weightKg)+(9.16*weeks)
   };
   pregnancyEer=pregnancyBase[pal]+deposition;
   pregnancyMethod="National Academies DRI 2023, Table 5-17";
   pregnancyFormula="Second/third trimester TEE equation + energy deposition based on pre-pregnancy BMI ("+deposition+" kcal/day).";
   trimester=weeks<=27?"Second trimester":"Third trimester";
  }
  if(!Number.isFinite(pregnancyEer)||pregnancyEer<=0)throw new Error("These pregnancy inputs do not produce a usable estimate. Check the values and activity category.");
  pregnancy=Object.freeze({eerKcalPerDay:pregnancyEer,trimester:trimester,gestationalWeeks:weeks,method:pregnancyMethod,formula:pregnancyFormula});
 }
 if(status==="breastfeeding"||status==="both"){
  var stage=input.breastfeedingStage;
  if(stage!=="exclusive_0_6"&&stage!=="partial_7_12")throw new Error("Choose a supported breastfeeding stage.");
  var increment=stage==="exclusive_0_6"?400:380;
  var lactationEer=baseEer+increment;
  if(!Number.isFinite(lactationEer)||lactationEer<=0)throw new Error("These breastfeeding inputs do not produce a usable estimate.");
  breastfeeding=Object.freeze({eerKcalPerDay:lactationEer,stage:stage==="exclusive_0_6"?"Exclusive breastfeeding, 0–6 months postpartum":"Partial breastfeeding, 7–12 months postpartum",method:stage==="exclusive_0_6"?"National Academies DRI 2023, Table 5-18":"National Academies DRI 2023, Table 5-19",formula:stage==="exclusive_0_6"?"Adult female TEE + 540 kcal/day milk production − 140 kcal/day energy mobilization.":"Adult female TEE + 380 kcal/day milk production."});
 }
 return Object.freeze({age:age,weightKg:weightKg,heightCm:heightCm,activityCategory:pal,pregnancy:pregnancy,breastfeeding:breastfeeding,combinedTargetKcalPerDay:null,sourceUrl:"https://www.nationalacademies.org/read/26818/chapter/7"});
}

function formatEquationKcal(value){
 return new Intl.NumberFormat("en-US",{minimumFractionDigits:2,maximumFractionDigits:2}).format(value);
}
function formatKcal(value){
 var scale=Math.max(1,Math.abs(value));
 var rounded=Math.round((value+Number.EPSILON*scale*8)*10)/10;
 return new Intl.NumberFormat("en-US",{minimumFractionDigits:1,maximumFractionDigits:1}).format(rounded);
}
var api=Object.freeze({LB_TO_KG:LB_TO_KG,IN_TO_CM:IN_TO_CM,ACTIVITY_PRESETS:ACTIVITY_PRESETS,DRI_ACTIVITY_CATEGORIES:DRI_ACTIVITY_CATEGORIES,calculateMaintenanceCalories:calculateMaintenanceCalories,calculateLifeStageCalories:calculateLifeStageCalories,formatKcal:formatKcal,formatEquationKcal:formatEquationKcal});
if(typeof module!=="undefined"&&module.exports)module.exports=api;
root.CalorieCalculator=api;
function initialize(doc){
 var rootNode=doc.getElementById("calorie-form");if(!rootNode)return;
 var byId=function(id){return doc.getElementById(id);};
 var unit=byId("cal-height-unit"),metric=byId("cal-height-metric"),imperial=byId("cal-height-imperial");
 var cm=byId("cal-height-cm"),ft=byId("cal-height-ft"),inch=byId("cal-height-in"),heightLabel=byId("cal-height-label");
 var error=byId("calorie-error"),result=byId("calorie-result");
 var coefficient=byId("cal-coefficient"),eligibilityField=byId("cal-eligibility-field"),eligibility=byId("cal-eligibility");
 function clear(){error.textContent="";result.hidden=true;result.replaceChildren();}
 function updateHeight(){
  var imp=unit.value==="ft-in";metric.hidden=imp;imperial.hidden=!imp;
  metric.style.display=imp?"none":"block";imperial.style.display=imp?"grid":"none";
  heightLabel.textContent=imp?"Height (ft / in)":"Height (cm)";
  heightLabel.htmlFor=imp?"cal-height-ft":"cal-height-cm";
  cm.disabled=imp;ft.disabled=!imp;inch.disabled=!imp;clear();
 }
 function updateEligibility(){
  var female=coefficient.value==="female";
  eligibilityField.hidden=!female;
  eligibility.disabled=!female;
  eligibility.required=female;
  if(!female)eligibility.value="";
  var status=eligibility.value;
  var lifeStage=female&&["pregnant","breastfeeding","both"].includes(status);
  byId("cal-life-stage-fields").hidden=!lifeStage;
  byId("cal-pregnancy-fields").hidden=!(lifeStage&&(status==="pregnant"||status==="both"));
  byId("cal-breastfeeding-fields").hidden=!(lifeStage&&(status==="breastfeeding"||status==="both"));
  byId("cal-standard-activity-field").hidden=lifeStage;
  byId("cal-life-stage-activity-field").hidden=!lifeStage;
  clear();
 }
 function fmt(v){return formatKcal(v);}
 function add(tag,cls,value){var el=doc.createElement(tag);if(cls)el.className=cls;el.textContent=value;result.appendChild(el);}
 function calculate(){
  clear();
  try{
   var status=byId("cal-eligibility").value;
   var common={age:byId("cal-age").value,weight:byId("cal-weight").value,weightUnit:byId("cal-weight-unit").value,heightUnit:unit.value,heightCm:cm.value,heightFeet:ft.value,heightInches:inch.value,coefficient:byId("cal-coefficient").value,pregnancyStatus:status};
   if(common.coefficient==="female"&&["pregnant","breastfeeding","both"].includes(status)){
    var life=calculateLifeStageCalories(Object.assign({},common,{lifeStageActivityId:byId("cal-life-stage-activity").value,pregnancyWeeks:byId("cal-pregnancy-weeks").value,prePregnancyWeight:byId("cal-prepregnancy-weight").value,breastfeedingStage:byId("cal-breastfeeding-stage").value}));
    add("h3","text-lg font-semibold","Estimated daily energy requirement");
    add("p","mt-1 text-sm","Method: National Academies Dietary Reference Intakes for Energy (2023). Activity category: "+life.activityCategory.replace("_"," ")+".");
    if(life.pregnancy){
     add("h4","mt-3 font-semibold","Pregnancy estimate · "+life.pregnancy.trimester);
     add("p","mt-1 text-2xl font-bold",fmt(life.pregnancy.eerKcalPerDay)+" kcal/day");
     add("p","mt-1 text-sm","Gestation: "+life.pregnancy.gestationalWeeks+" weeks. "+life.pregnancy.formula);
     add("p","mt-1 text-sm","Reference: "+life.pregnancy.method+".");
    }
    if(life.breastfeeding){
     add("h4","mt-3 font-semibold","Breastfeeding estimate");
     add("p","mt-1 text-2xl font-bold",fmt(life.breastfeeding.eerKcalPerDay)+" kcal/day");
     add("p","mt-1 text-sm",life.breastfeeding.stage+". "+life.breastfeeding.formula);
     add("p","mt-1 text-sm","Reference: "+life.breastfeeding.method+".");
    }
    add("p","mt-3 text-sm font-semibold","These are separate life-stage reference estimates. Do not add them together or treat either as a personal prescription.");
    add("p","mt-1 text-sm","The 2023 equations were not validated as a combined target for someone who is simultaneously pregnant and breastfeeding. Discuss concurrent needs, weight trends and medical circumstances with a qualified healthcare professional.");
    add("p","mt-1 text-sm","These DRI equations were developed for US and Canadian reference populations. They have not been validated for every country or individual, including Pakistan.");
    var dLink=doc.createElement("a");dLink.href=life.sourceUrl;dLink.target="_blank";dLink.rel="noopener noreferrer";dLink.className="mt-3 inline-flex min-h-[40px] items-center rounded-lg bg-sky-800 px-3 py-2 text-sm font-semibold text-white underline";dLink.textContent="View National Academies 2023 DRI source";result.appendChild(dLink);
    result.hidden=false;return;
   }
   var x=calculateMaintenanceCalories(Object.assign({},common,{activityId:byId("cal-activity").value}));
   add("h3","text-lg font-semibold","Your estimated daily energy");
   add("p","mt-1 text-sm","Equation: "+x.equation+".");
   add("p","mt-2","Estimated resting energy expenditure (REE): "+fmt(x.restingKcalPerDay)+" kcal/day.");
   add("p","mt-1 text-xl font-bold","Estimated maintenance calories: "+fmt(x.maintenanceKcalPerDay)+" kcal/day.");
   add("p","mt-2","Calculation: "+formatEquationKcal(x.restingKcalPerDay)+" × "+x.activity.multiplier+" activity factor = "+fmt(x.maintenanceKcalPerDay)+" kcal/day.");
   add("p","mt-2 text-sm","Activity assumption: "+x.activity.label+". "+x.activity.description);
   if(x.outsideOriginalStudyAgeRange)add("p","mt-2 text-sm","Age-range note: the original Mifflin–St Jeor study sample was 19–78 years. Your entered age is outside that original sample range, so this result has an additional evidence limitation.");
   add("p","mt-2 text-sm","Activity assumption version: "+x.activity.version+". "+x.activity.limitations);
   var sourceLine=doc.createElement("p");sourceLine.className="mt-2 text-sm";
   sourceLine.appendChild(doc.createTextNode("Equation source: "));
   var sourceLink=doc.createElement("a");sourceLink.href="https://pubmed.ncbi.nlm.nih.gov/2305711/";sourceLink.target="_blank";sourceLink.rel="noopener noreferrer";sourceLink.textContent="Mifflin–St Jeor original paper (PubMed)";
   sourceLine.appendChild(sourceLink);result.appendChild(sourceLine);
   add("p","mt-2 text-sm","This is a population-equation estimate, not a measured metabolic rate or a personalized medical prescription.");
   result.hidden=false;
  }catch(e){
   var message=e&&e.message?e.message:"The estimate could not be calculated. Check the entries and try again.";
   if(/not intended for pregnancy or breastfeeding/i.test(message)){
    add("h3","text-lg font-semibold","Pregnancy and breastfeeding need a different estimate");
    add("p","mt-2 text-sm","This adult Mifflin–St Jeor calculator does not calculate energy needs during pregnancy or breastfeeding.");
    add("p","mt-2 text-sm","The USDA National Agricultural Library DRI Calculator includes pregnancy and breastfeeding inputs. It is designed for healthcare professionals, so use it with a qualified healthcare professional.");
    var guidanceLink=doc.createElement("a");
    guidanceLink.href="https://www.nal.usda.gov/human-nutrition-and-food-safety/dri-calculator";
    guidanceLink.target="_blank";
    guidanceLink.rel="noopener noreferrer";
    guidanceLink.className="mt-3 inline-flex min-h-[40px] items-center rounded-lg bg-sky-800 px-3 py-2 text-sm font-semibold text-white underline";
    guidanceLink.textContent="Open USDA DRI Calculator";
    result.appendChild(guidanceLink);
    result.hidden=false;
   }else{error.textContent=message;}
  }
 }
 unit.addEventListener("change",updateHeight);
 coefficient.addEventListener("change",updateEligibility);
 eligibility.addEventListener("change",updateEligibility);
 rootNode.querySelectorAll("input, select").forEach(function(control){
  control.addEventListener("input",clear);
  control.addEventListener("change",clear);
 });
 byId("cal-calculate").addEventListener("click",calculate);
 byId("cal-reset").addEventListener("click",function(){
  ["cal-age","cal-weight","cal-height-cm","cal-height-ft","cal-height-in","cal-pregnancy-weeks","cal-prepregnancy-weight"].forEach(function(id){byId(id).value="";});
  byId("cal-weight-unit").value="kg";unit.value="cm";byId("cal-coefficient").value="";byId("cal-activity").value="";byId("cal-life-stage-activity").value="inactive";byId("cal-eligibility").value="";byId("cal-breastfeeding-stage").value="";
  updateHeight();updateEligibility();clear();byId("cal-age").focus();
 });
 rootNode.addEventListener("keydown",function(e){if(e.key==="Enter"&&e.target&&e.target.tagName==="INPUT"){e.preventDefault();calculate();}});
 updateHeight();
 updateEligibility();
}
if(typeof document!=="undefined")initialize(document);
})(typeof globalThis!=="undefined"?globalThis:this);
