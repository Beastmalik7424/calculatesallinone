const { chromium } = require("playwright");

const base = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\\/$/, "");
const paths = ["/ar/", "/es/", "/fr/", "/contact/", "/discount-calculator/", "/editorial-policy/", "/health/"];
(async () => {
  const browser = await chromium.launch({ headless: true });
  const failures = [];
  try {
    for (const path of paths) {
      const page = await browser.newPage();
      const errors = [];
      page.on("console", msg => { if (msg.type() === "error") errors.push("console: " + msg.text()); });
      page.on("pageerror", err => errors.push("pageerror: " + err.message));
      const response = await page.goto(base + path, { waitUntil: "networkidle", timeout: 30000 });
      const status = response ? response.status() : 0;
      console.log(path + " HTTP " + status + " browser_errors=" + errors.length);
      for (const error of errors) console.log("  " + error);
      if (status !== 200) failures.push(path + ": expected HTTP 200, got " + status);
      if (errors.length) failures.push(path + ": browser console/page errors detected");
      await page.close();
    }
  } finally {
    await browser.close();
  }
  if (failures.length) {
    console.error("HEADLESS BROWSER AUDIT: FAIL");
    failures.forEach(x => console.error("FAIL: " + x));
    process.exit(1);
  }
  console.log("HEADLESS BROWSER AUDIT: PASS (7 URLs, zero console/page errors)");
})().catch(err => { console.error(err); process.exit(1); });
