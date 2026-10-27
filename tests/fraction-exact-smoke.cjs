const assert = require("node:assert/strict");
const calc = require("../static/extra-calculators.js");
assert.deepEqual(calc.fraction(1,2,1,3,"add"), {n:5,d:6});
assert.deepEqual(calc.fraction(9007199254740991,9007199254740991,9007199254740991,9007199254740991,"multiply"), {n:1,d:1}, "reducible large fractions must not overflow intermediate Number multiplication");
assert.deepEqual(calc.fraction(9007199254740991,9007199254740991,9007199254740991,9007199254740991,"add"), {n:2,d:1});
assert.throws(()=>calc.fraction(1,0,1,2,"add"), /whole-number|denominator/i);
assert.throws(()=>calc.fraction(1,2,0,3,"divide"), /zero/i);
assert.throws(()=>calc.fraction(9007199254740991,1,1,1,"add"), /safe integer/i);
console.log("PASS: fraction exact intermediate arithmetic and boundary cases");
