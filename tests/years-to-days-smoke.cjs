'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const calc = require('../static/years-to-days.js');

const cases = [
  ['2024-01-01', 4, 1461, '2028-01-01', 1],
  ['2024-02-28', 1, 366, '2025-02-28', 1],
  ['2024-02-29', 1, 365, '2025-02-28', 1],
  ['2023-02-28', 1, 365, '2024-02-28', 0],
  ['1899-01-01', 2, 730, '1901-01-01', 0],
  ['1999-01-01', 2, 731, '2001-01-01', 1],
  ['2099-01-01', 2, 730, '2101-01-01', 0],
  ['2000-01-01', 80, 29220, '2080-01-01', 20],
  ['2026-10-30', 80, 29219, '2106-10-30', 19],
  ['0099-01-01', 1, 365, '0100-01-01', 0],
  ['2024-01-01', 0, 0, '2024-01-01', 0]
];
for (const [start,years,days,end,leap] of cases) {
  const x = calc.calculateDays(start,String(years));
  assert.equal(x.days,days,start+' day count');
  assert.equal(x.endDate,end,start+' end date');
  assert.equal(x.leapDays,leap,start+' leap days');
  assert.equal(x.hours,days*24);
  assert.equal(x.minutes,days*1440);
}
for (const [start,years] of [
  ['2024-02-30','1'], ['2023-02-29','1'], ['2024-13-01','1'],
  ['2024-01-01','1.5'], ['2024-01-01','2e2'],
  ['2024-01-01','-1'], ['2024-01-01',''],
  ['9999-01-01','1'], ['0000-01-01','1'], ['','2']
]) assert.throws(()=>calc.calculateDays(start,years), Error,JSON.stringify([start,years]));
const page=path.join(__dirname,'../public/years-to-days-calculator/index.html');
assert.ok(fs.existsSync(page),'new route must be generated');
const html=fs.readFileSync(page,'utf8');
for(const fragment of ['<h1','Years to Days Calculator','/assets/years-to-days.js','/years-to-days-calculator/','2024','1,461']) assert.ok(html.includes(fragment),'missing '+fragment);
assert.ok(fs.readFileSync(path.join(__dirname,'../public/sitemap.xml'),'utf8').includes('/years-to-days-calculator/'),'sitemap inclusion');
assert.ok(fs.readFileSync(path.join(__dirname,'../public/time/index.html'),'utf8').includes('/years-to-days-calculator/'),'time hub link');
console.log('PASS: years-to-days accuracy, invalid inputs, SEO integration and hub link');
