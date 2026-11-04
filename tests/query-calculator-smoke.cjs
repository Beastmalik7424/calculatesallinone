"use strict";
const fs = require("fs");
const vm = require("vm");
const assert = require("assert");
const js = fs.readFileSync("static/app.js", "utf8");
const html = fs.readFileSync("public/query-calculator/index.html", "utf8");
assert.match(html, /id="query-time-form"/);
assert.match(html, /id="qt-result"/);
assert.ok(html.includes("/assets/app.js?v="), "versioned JS asset missing");
const listeners = {};
const form = {addEventListener: (name, fn) => {listeners["form:" + name] = fn;}};
const input = {value:"Ager birth date 29-02-1984 ho to age kitne days hogi?",addEventListener:(name, fn) => {listeners["input:" + name] = fn;}};
const result = {textContent:""};
const nodes = {"query-time-form":form,"qt-question":input,"qt-result":result};
const document = {
 readyState:"loading",
 documentElement:{lang:"en"},
 getElementById:(id)=>nodes[id] || null,
 addEventListener:(name,fn)=>{listeners[name]=fn;},
 querySelector:()=>null, querySelectorAll:()=>[]
};
// Freeze the date so this regression test does not fail as calendar days advance.
const FIXED_NOW = new Date(2026, 9, 26, 12, 0, 0);
class FixedDate extends Date {
 constructor(...args) { super(...(args.length ? args : [FIXED_NOW.getTime()])); }
 static now() { return FIXED_NOW.getTime(); }
}
const ctx = {document, console, Date: FixedDate, Number, String, Array, Math, Object, RegExp, Intl};
vm.createContext(ctx);
vm.runInContext(js,ctx,{timeout:3000});
assert.equal(typeof listeners.DOMContentLoaded,"function");
listeners.DOMContentLoaded();
assert.match(result.textContent,/15,580|15580/, "Leap-day birth to 26 October 2026 must be 15,580 days");
input.value = "DOB 29-07-1984 age in months and days";
listeners["form:submit"]({preventDefault(){}});
assert.match(result.textContent,/15,429|15429/, "29 July 1984 to 26 October 2026 must be 15,429 days");
assert.match(result.textContent,/42 years, 2 months, 27 days/, "DOB should report calendar years, months and days");
const monthCases = [
 ["115 months in years and days",/9 years and 7 months.*3,500\.24 days/],
 ["115 mahine in years and days",/9 years and 7 months.*3,500\.24 days/],
 ["115 مہینے سال اور دن",/9 years and 7 months.*3,500\.24 days/],
 ["115 महीने साल और दिन",/9 years and 7 months.*3,500\.24 days/],
 ["115 meses en años y días",/9 years and 7 months.*3,500\.24 days/],
 ["115 mois en années et jours",/9 years and 7 months.*3,500\.24 days/],
 ["115 شهر سنوات وأيام",/9 years and 7 months.*3,500\.24 days/],
 ["115 months in days",/3,500\.24 days.*average/],
 ["115 months in years",/9 years and 7 months/],
 ["2 months in days",/60\.87 days.*average/]
];
for (const [q, expected] of monthCases) {
 input.value = q;
 listeners["form:submit"]({preventDefault(){}});
 assert.match(result.textContent, expected, q + " => " + result.textContent);
}
const independenceCases = [
 ["Pakistan independence date",/14 August 1947/],
 ["Pakistan ki azadi ki tareekh",/14 August 1947/],
 ["پاکستان کی آزادی کی تاریخ",/14 August 1947/]
];
for (const [q, expected] of independenceCases) {
 input.value = q;
 listeners["form:submit"]({preventDefault(){}});
 assert.match(result.textContent, expected, q + " => " + result.textContent);
}
input.value = "How many days since Pakistan independence?";
listeners["form:submit"]({preventDefault(){}});
assert.match(result.textContent,/28,928 days elapsed for Pakistan/, "Pakistan independence elapsed days should use the Gregorian calendar");
const cases = [
 ["Mer pass 99 packets hn 29 distribute kr die 19 chori ho gye baki kotny bach gye",/51/],
 ["मेरे पास 99 पैकेट हैं 29 बाँट दिए 19 चोरी हो गए कितने बचे",/51/],
 ["میرے پاس ۹۹ پیکٹ ہیں ۲۹ بانٹ دیے ۱۹ چوری ہوگئے باقی کتنے",/51/],
 ["عندي ٩٩ حزمة ٢٩ توزيع ١٩ سرق كم باقي",/51/],
 ["Tengo 99 paquetes, 29 distribuidos, 19 robados, cuantos quedan",/51/],
 ["J'ai 99 paquets, 29 distribués, 19 volés, combien reste",/51/],
 ["Mere pass 64 amm hn 14 bant diye 25 kharab ho gye baki kitny bachy",/25/]
];
for(const [q,expected] of cases){
 input.value=q;
 listeners["form:submit"]({preventDefault(){}});
 assert.match(result.textContent,expected,q+" => "+result.textContent);
}
// Natural-language unit order follows the quantity, not the order of words.
const yearDayQueries = [
 ["30 years is how many days", /30 years = 10,950 days/],
 ["total days in 3 years", /3 years = 1,095 days/],
 ["how many days in 21 years", /21 years = 7,665 days/],
 ["how many years is 2555 days", /2,555 days = 7 years/],
 ["how many days is 25 years", /25 years = 9,125 days/],
 ["1 years in days", /1 year = 365 days/],
 ["14 years to days", /14 years = 5,110 days/],
 ["4 years into days", /4 years = 1,460 days/],
 ["convert 2555 days to years", /2,555 days = 7 years/],
 ["3 years into days", /3 years = 1,095 days/],
 ["21 years to days", /21 years = 7,665 days/],
 ["25 years in days", /25 years = 9,125 days/],
 ["how many days are there in 3 years", /3 years = 1,095 days/],
 ["3 saal mein kitne din", /3 years = 1,095 days/],
 ["3 سال میں کتنے دن", /3 years = 1,095 days/],
 ["3 साल में कितने दिन", /3 years = 1,095 days/],
 ["كم يوم في 3 سنوات", /3 years = 1,095 days/]
];
for (const [q, expected] of yearDayQueries) {
 input.value = q;
 listeners["form:submit"]({preventDefault(){}});
 assert.match(result.textContent, expected, q + " => " + result.textContent);
}


const leapYearCases = [
 ["how many days in year 2024", /2024 is a leap year = 366 days/i],
 ["days in 2023", /2023 is not a leap year = 365 days/i],
 ["how many days in year 2000", /2000 is a leap year = 366 days/i],
 ["how many days in year 1900", /1900 is not a leap year = 365 days/i],
 ["3 years from 2024 in days", /3 calendar years from 2024 = 1,096 days/i],
 ["4 years from 2000 to days", /4 calendar years from 2000 = 1,461 days/i],
 ["4 years from 1900 in days", /4 calendar years from 1900 = 1,460 days/i],
 ["3 years in days", /3 years ≈ 1,095\.73 days.*Gregorian average/i]
];
for (const [q, expected] of leapYearCases) {
 input.value = q;
 listeners["form:submit"]({preventDefault(){}});
 assert.match(result.textContent, expected, q + " => " + result.textContent);
}

const numberWordCases = [
 ["thirty years is how many days", /30 years = 10,950 days/],
 ["three years in days", /3 years = 1,095 days/],
 ["how many days in twenty one years", /21 years = 7,665 days/],
 ["how many years is two thousand five hundred fifty five days", /2,555 days = 7 years/],
 ["two thousand five hundred and fifty five days in years", /2,555 days = 7 years/],
 ["twenty-one years in days", /21 years = 7,665 days/],
 ["how many days is twenty five years", /25 years = 9,125 days/],
 ["2,555 days in years", /2,555 days = 7 years/],
 ["twenty five years in days", /25 years = 9,125 days/],
 ["one year in days", /1 year = 365 days/],
 ["four years into days", /4 years = 1,460 days/],
 ["3 years in days", /3 years = 1,095 days/],
 ["three saal mein kitne din", /3 years = 1,095 days/],
 ["teen saal mein kitne din", /3 years = 1,095 days/],
 ["तीन साल में कितने दिन", /3 years = 1,095 days/],
 ["3 साल में कितने दिन", /3 years = 1,095 days/],
 ["تین سال میں کتنے دن", /3 years = 1,095 days/],
 ["how many days in 3 years", /3 years = 1,095 days/]
];
for (const [q, expected] of numberWordCases) {
 input.value = q;
 listeners["form:submit"]({preventDefault(){}});
 assert.match(result.textContent, expected, q + " => " + result.textContent);
}

console.log("Query Calculator DOM, multilingual month conversions, DOB, Pakistan date and arithmetic tests PASS");
