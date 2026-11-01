const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

// Exercise the exact calculation engine shipped in the standalone EMI page,
// without a DOM, network, or third-party runtime.
const html = fs.readFileSync("emi-calculator.html", "utf8");
// Guard the standalone page metadata because it bypasses the shared page-head builder.
assert.match(html, /<html lang="en" dir="ltr">/, "EMI page must declare its language and text direction");
assert.match(html, /name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/, "EMI viewport must match the site safe-area behavior");
assert.ok(html.includes('property="og:image" content="https://calculateallinone.vercel.app/assets/og-image.png"'), "EMI page must use the generated canonical social preview image");
assert.ok(html.includes('name="twitter:card" content="summary_large_image"'), "EMI page must expose a large social preview");
assert.equal((html.match(/"@type":"FAQPage"/g) || []).length, 1, "EMI page must contain exactly one FAQPage schema block");
const appSchemaStart = html.indexOf('<script type="application/ld+json" id="app-schema">') + '<script type="application/ld+json" id="app-schema">'.length;
const appSchemaEnd = html.indexOf("</script>", appSchemaStart);
assert.ok(appSchemaStart >= 0 && appSchemaEnd > appSchemaStart, "EMI WebApplication schema must exist");
const appSchema = JSON.parse(html.slice(appSchemaStart, appSchemaEnd));
assert.equal(appSchema.url, "https://calculateallinone.vercel.app/emi-calculator/", "WebApplication schema URL must match canonical URL");
assert.equal(appSchema.inLanguage, "en", "WebApplication schema language must match document language");

// Regression guard: the standalone EMI page must retain global site navigation and a centered, responsive calculator column.
assert.match(html, /<nav aria-label="Main" class="site-nav">[\s\S]*?class="ca-calculator-carousel"[\s\S]*?data-tool-shortcut="emi-calculator"[\s\S]*?aria-current="page"[\s\S]*?<\/nav>/, "EMI page must expose the active calculator carousel in its existing navigation row");
assert.match(html, /<a href="\/money\/">Money and Business<\/a>/, "EMI page must retain its Money and Business navigation link");
assert.match(html, /<a href="\/standard-calculator\/">Standard Calculator<\/a>/, "EMI page must retain its Standard Calculator navigation link");
assert.match(html, /<main class="emi-page-main">/, "EMI calculator must use the shared-width main content wrapper");
assert.match(html, /\.emi-page-main\s*\{[^}]*max-width:\s*960px/s, "EMI main content must be capped to the intended centered tool width");

const match = html.match(/const Engine=\(\(\)=>\{[\s\S]*?\n\}\)\(\);/);
assert.ok(match, "EMI calculation engine must remain extractable from the standalone page");
const sandbox = { module: { exports: {} }, Number, Math, String, Error, URLSearchParams };
vm.runInNewContext(match[0] + "\nmodule.exports = Engine;", sandbox, { filename: "emi-calculator.html" });
const Engine = sandbox.module.exports;
assert.ok(Engine && typeof Engine.buildSchedule === "function", "EMI engine exports required calculation functions");

const tests = [];
function test(name, fn) {
  try {
    assert.ok(fn(), name);
    tests.push(name);
  } catch (error) {
    console.error("FAIL " + name + ": " + error.message);
    process.exitCode = 1;
  }
}
function throws(fn) {
  try { fn(); return false; } catch { return true; }
}

test("amount parser accepts grouped decimals exactly", () =>
  Engine.parseAmount("1,000,000.50", { min: 1, max: 1000000000 }).value === 100000050);
test("amount parser rejects negative, blank, exponent, malformed commas, excess decimals and injection", () =>
  ["-5", "", "abc", "1e5", "1,00", "12.345", "<img onerror=alert(1)>"].every(
    value => !Engine.parseAmount(value, { min: 1, max: 1000000000 }).ok
  ));
test("amount parser enforces configured bounds", () =>
  Engine.parseAmount("1000000000", { min: 1, max: 1000000000 }).ok &&
  !Engine.parseAmount("1000000001", { min: 1, max: 1000000000 }).ok);
test("rate parser accepts zero, fractional and 100 percent", () =>
  [ "0", "12.5", "100" ].every(value => Engine.parseRate(value).ok));
test("rate parser rejects negative, over-100, exponent and excess precision", () =>
  [ "-1", "100.01", "1e2", "1.234" ].every(value => !Engine.parseRate(value).ok));
test("tenure parser enforces whole-month bounds", () =>
  Engine.parseTenure("1").ok && Engine.parseTenure("600").ok &&
  [ "0", "601", "1.5", "-1", "1e2" ].every(value => !Engine.parseTenure(value).ok));

const golden = Engine.buildSchedule(100000000, 12, 12);
test("golden EMI equals 88,848.79", () => Engine.emiCents(100000000, 12, 12) === 8884879);
test("golden schedule interest and payment totals reconcile", () =>
  golden.totalInterestCents === 6618545 &&
  golden.totalPaymentCents === 106618545 &&
  golden.totalPrincipalCents === 100000000 &&
  golden.rows.at(-1).closingCents === 0);
const zeroRate = Engine.buildSchedule(12000000, 0, 12);
test("zero-interest loan has no interest and equal principal installments", () =>
  Engine.emiCents(12000000, 0, 12) === 1000000 &&
  zeroRate.totalInterestCents === 0 &&
  zeroRate.totalPaymentCents === 12000000);
const oneMonth = Engine.buildSchedule(10000000, 12, 1);
test("one-month loan pays principal plus one month's interest", () =>
  Engine.emiCents(10000000, 12, 1) === 10100000 &&
  oneMonth.totalInterestCents === 100000 &&
  oneMonth.rows.length === 1 &&
  oneMonth.rows[0].closingCents === 0);
test("invalid engine inputs are rejected", () =>
  throws(() => Engine.emiCents(-1, 12, 12)) &&
  throws(() => Engine.emiCents(100000, 101, 12)) &&
  throws(() => Engine.emiCents(100000, 12, 0)) &&
  throws(() => Engine.buildSchedule(-1, 12, 12)));

const base = Engine.buildSchedule(100000000, 12, 12);
const shorter = Engine.applyPrepayment(100000000, 12, 12,
  { amountCents: 1000000, kind: "once", month: 1, mode: "tenure" });
test("one-time prepayment reduces interest and closes the balance", () =>
  shorter.totalInterestCents < base.totalInterestCents &&
  shorter.rows.at(-1).closingCents === 0 &&
  shorter.rows.every(row => row.closingCents >= 0));
const lowerEmi = Engine.applyPrepayment(100000000, 12, 12,
  { amountCents: 1000000, kind: "once", month: 1, mode: "emi" });
test("EMI-reduction prepayment lowers installments and closes the balance", () =>
  lowerEmi.rows.at(-1).closingCents === 0 && lowerEmi.emiCents < 8884879);
test("oversized prepayment is capped at the remaining balance", () =>
  Engine.applyPrepayment(100000000, 12, 12,
    { amountCents: 99999999999, kind: "once", month: 1, mode: "tenure" }).rows.at(-1).closingCents === 0);
test("prepayment month beyond the term is rejected", () =>
  throws(() => Engine.applyPrepayment(100000000, 12, 12,
    { amountCents: 10000, kind: "once", month: 13, mode: "tenure" })));

let seed = 42;
const random = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
let schedulesReconcile = true;
for (let i = 0; i < 2000; i++) {
  const principal = Math.floor(random() * 10000000000) + 1;
  const months = Math.floor(random() * 600) + 1;
  const rate = random() * 100;
  const schedule = Engine.buildSchedule(principal, rate, months);
  if (schedule.rows.at(-1).closingCents !== 0 ||
      schedule.rows.some(row => row.closingCents < 0) ||
      schedule.totalPrincipalCents !== principal ||
      schedule.totalPaymentCents !== principal + schedule.totalInterestCents) {
    schedulesReconcile = false;
    break;
  }
}
test("2,000 seeded loan schedules reconcile principal, interest, payment and closing balance", () => schedulesReconcile);
test("higher interest rate does not reduce EMI", () =>
  Engine.emiCents(100000000, 13, 120) >= Engine.emiCents(100000000, 12, 120));
const maxSchedule = Engine.buildSchedule(100000000000, 100, 600);
test("maximum supported rate and tenure close without non-finite totals", () =>
  maxSchedule.rows.at(-1).closingCents === 0 && Number.isFinite(maxSchedule.totalInterestCents));
const affordability = Engine.affordability(10000000, 1000000, 50, 12, 60);
test("affordability subtracts existing EMI correctly", () => affordability.ok && affordability.maxEmiCents === 4000000);
test("affordability estimate round-trips under its EMI cap", () =>
  Engine.emiCents(affordability.maxLoanCents, 12, 60) <= affordability.maxEmiCents);
test("month arithmetic handles year boundaries", () =>
  Engine.monthAt("2026-01", 12) === "2027-01");
test("currency formatting preserves cents and locale grouping", () =>
  Engine.formatMoney(123456750, "USD", { symbol: false }) === "1,234,567.50" &&
  Engine.formatMoney(123456750, "PKR", { symbol: false }) === "12,34,567.50" &&
  Engine.formatMoney(123456750, "INR", { symbol: false }) === "12,34,567.50" &&
  Engine.formatMoney(100000, "USD", { symbol: false }) === "1,000.00");
test("CSV export has UTF-8 BOM, header, and decimal amounts", () => {
  const csv = Engine.formatCsv(golden.rows, "PKR");
  return csv.charCodeAt(0) === 0xfeff &&
    csv.includes("Month,Date,Opening,EMI,Principal,Interest,Closing") &&
    csv.includes("88848.79");
});
test("calendar month arithmetic and URL value validation reject malformed values", () => {
  const params = new URLSearchParams("?amount=abc&tenure=99999");
  return !Engine.parseAmount(params.get("amount"), { min: 1, max: 1000000000 }).ok &&
    !Engine.parseTenure(params.get("tenure"), { min: 1, max: 50 }).ok;
});

if (!process.exitCode) console.log("PASS: " + tests.length + " EMI engine tests, including 2,000 seeded schedule checks.");
