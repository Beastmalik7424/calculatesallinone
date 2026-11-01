(function (root) {
"use strict";
var LB_TO_KG=0.45359237, IN_TO_CM=2.54;
var ACTIVITY_PRESETS=Object.freeze([
Object.freeze({id:"sedentary",label:"Sedentary",multiplier:1.2,description:"Mostly seated work and little planned movement.",version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}),
Object.freeze({id:"light",label:"Light activity",multiplier:1.375,description:"Some walking or light exercise, with mostly light daily movement.,version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}}),
Object.freeze({id:"moderate",label:"Moderate activity",multiplier:1.55,description:"Regular moderate exercise and a generally active daily routine.,version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}}),
Object.freeze({id:"very_active",label:"Very active",multiplier:1.725,description:"Frequent hard exercise or a physically demanding job.,version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}}),
Object.freeze({id:"extra_active",label:"Extra active",multiplier:1.9,description:"Very demanding daily physical work or training.,version:"1.0",source:"Application-defined consumer activity preset; not from the original Mifflin–St Jeor paper or FAO/WHO/UNU PAL categories.",limitations:"Approximate heuristic, not individually validated; actual activity and energy needs vary."}})
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
 if(!["no","pregnant","breastfeeding","both","prefer_not_to_say"].includes(input.pregnancyStatus))throw new Error("Select a pregnancy and breastfeeding status.");
 if(input.pregnancyStatus!=="no")throw new Error("This calculator is not intended for pregnancy or breastfeeding. It does not provide an ordinary maintenance estimate for these circumstances.");
 var coefficient=input.coefficient;
 if(coefficient!=="male"&&coefficient!=="female")throw new Error("Choose one of the published equation coefficients to continue.");
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
var api=Object.freeze({LB_TO_KG:LB_TO_KG,IN_TO_CM:IN_TO_CM,ACTIVITY_PRESETS:ACTIVITY_PRESETS,calculateMaintenanceCalories:calculateMaintenanceCalories});
if(typeof module!=="undefined"&&module.exports)module.exports=api;
root.CalorieCalculator=api;
function initialize(doc){
 var rootNode=doc.getElementById("calorie-form");if(!rootNode)return;
 var byId=function(id){return doc.getElementById(id);};
 var unit=byId("cal-height-unit"),metric=byId("cal-height-metric"),imperial=byId("cal-height-imperial");
 var cm=byId("cal-height-cm"),ft=byId("cal-height-ft"),inch=byId("cal-height-in");
 var error=byId("calorie-error"),result=byId("calorie-result");
 function clear(){error.textContent="";result.hidden=true;result.replaceChildren();}
 function updateHeight(){
  var imp=unit.value==="ft-in";metric.hidden=imp;imperial.hidden=!imp;
  cm.disabled=imp;ft.disabled=!imp;inch.disabled=!imp;clear();
 }
 function fmt(v){return new Intl.NumberFormat("en-US",{maximumFractionDigits:1}).format(v);}
 function add(tag,cls,value){var el=doc.createElement(tag);if(cls)el.className=cls;el.textContent=value;result.appendChild(el);}
 function calculate(){
  clear();
  try{
   var x=calculateMaintenanceCalories({age:byId("cal-age").value,weight:byId("cal-weight").value,weightUnit:byId("cal-weight-unit").value,heightUnit:unit.value,heightCm:cm.value,heightFeet:ft.value,heightInches:inch.value,coefficient:byId("cal-coefficient").value,activityId:byId("cal-activity").value,pregnancyStatus:byId("cal-eligibility").value});
   add("h3","text-lg font-semibold","Your estimated daily energy");
   add("p","mt-1 text-sm","Equation: "+x.equation+".");
   add("p","mt-2","Estimated resting energy expenditure (REE): "+fmt(x.restingKcalPerDay)+" kcal/day.");
   add("p","mt-1 text-xl font-bold","Estimated maintenance calories: "+fmt(x.maintenanceKcalPerDay)+" kcal/day.");
   add("p","mt-2","Calculation: "+fmt(x.restingKcalPerDay)+" × "+x.activity.multiplier+" activity factor = "+fmt(x.maintenanceKcalPerDay)+" kcal/day.");
   add("p","mt-2 text-sm","Activity assumption: "+x.activity.label+". "+x.activity.description);
   if(x.outsideOriginalStudyAgeRange)add("p","mt-2 text-sm","Age-range note: the original Mifflin–St Jeor study sample was 19–78 years. Your entered age is outside that original sample range, so this result has an additional evidence limitation.");
   add("p","mt-2 text-sm","Activity assumption version: "+x.activity.version+". "+x.activity.limitations);
   var sourceLine=doc.createElement("p");sourceLine.className="mt-2 text-sm";
   sourceLine.appendChild(doc.createTextNode("Equation source: "));
   var sourceLink=doc.createElement("a");sourceLink.href="https://pubmed.ncbi.nlm.nih.gov/2305711/";sourceLink.target="_blank";sourceLink.rel="noopener noreferrer";sourceLink.textContent="Mifflin–St Jeor original paper (PubMed)";
   sourceLine.appendChild(sourceLink);result.appendChild(sourceLine);
   add("p","mt-2 text-sm","This is a population-equation estimate, not a measured metabolic rate or a personalized medical prescription.");
   result.hidden=false;
  }catch(e){error.textContent=e&&e.message?e.message:"The estimate could not be calculated. Check the entries and try again.";}
 }
 unit.addEventListener("change",updateHeight);
 byId("cal-calculate").addEventListener("click",calculate);
 byId("cal-reset").addEventListener("click",function(){
  ["cal-age","cal-weight","cal-height-cm","cal-height-ft","cal-height-in"].forEach(function(id){byId(id).value="";});
  byId("cal-weight-unit").value="kg";unit.value="cm";byId("cal-coefficient").value="";byId("cal-activity").value="";byId("cal-eligibility").value="";
  updateHeight();clear();byId("cal-age").focus();
 });
 rootNode.addEventListener("keydown",function(e){if(e.key==="Enter"&&e.target&&e.target.tagName==="INPUT"){e.preventDefault();calculate();}});
 updateHeight();
}
if(typeof document!=="undefined")initialize(document);
})(typeof globalThis!=="undefined"?globalThis:this);
