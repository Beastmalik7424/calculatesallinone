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
 documentElement:{lang:"en"},
 getElementById:(id)=>nodes[id] || null,
 addEventListener:(name,fn)=>{listeners[name]=fn;},
 querySelector:()=>null, querySelectorAll:()=>[]
};
const ctx = {document, console, Date, Number, String, Array, Math, Object, RegExp, Intl};
vm.createContext(ctx);
vm.runInContext(js,ctx,{timeout:3000});
assert.equal(typeof listeners.DOMContentLoaded,"function");
listeners.DOMContentLoaded();
assert.match(result.textContent,/15579|15,579/);
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
console.log("Query Calculator DOM + six-language smoke tests PASS ("+(cases.length+1)+" cases)");
