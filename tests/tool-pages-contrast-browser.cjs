"use strict";

const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const BASE_URL = (process.env.BASE_URL || "http://127.0.0.1:4174").replace(/\/+$/, "");
const ROUTES = ["/zakat-calculator/", "/bmi-calculator/", "/tasbih-counter/"];

(async () => {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
  const failures = [];
  let checkedTextNodes = 0;
  try {
    for (const route of ROUTES) {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      const pageErrors = [];
      page.on("pageerror", error => pageErrors.push(error.message));
      const response = await page.goto(BASE_URL + route, { waitUntil: "load", timeout: 15000 });
      assert.equal(response && response.status(), 200, route + " must load with HTTP 200");
      await page.evaluate(() => document.fonts && document.fonts.ready);

      for (const theme of ["light", "dark"]) {
        if (theme === "dark") {
          const toggle = page.locator("#theme-toggle");
          if (await toggle.count()) await toggle.click();
          await page.waitForTimeout(50);
        }
        const result = await page.evaluate(() => {
          const parse = value => {
            const m = value.match(/rgba?\(([^)]+)\)/);
            if (!m) return null;
            const parts = m[1].split(",").map(v => Number.parseFloat(v.trim()));
            return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
          };
          const blend = (top, bottom) => {
            const a = top.a + bottom.a * (1 - top.a);
            if (!a) return { r: 0, g: 0, b: 0, a: 0 };
            return {
              r: (top.r * top.a + bottom.r * bottom.a * (1 - top.a)) / a,
              g: (top.g * top.a + bottom.g * bottom.a * (1 - top.a)) / a,
              b: (top.b * top.a + bottom.b * bottom.a * (1 - top.a)) / a,
              a
            };
          };
          const channel = c => {
            c /= 255;
            return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
          };
          const luminance = c => 0.2126 * channel(c.r) + 0.7152 * channel(c.g) + 0.0722 * channel(c.b);
          const contrast = (a, b) => {
            const x = luminance(a), y = luminance(b);
            return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
          };
          const visible = el => {
            const s = getComputedStyle(el), r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && s.display !== "none" &&
              s.visibility !== "hidden" && Number(s.opacity) > 0 &&
              !el.closest("[aria-hidden='true'],script,style,noscript,svg");
          };
          const main = document.querySelector("main#main");
          const root = document.querySelector("#tool-calculator");
          const counter = document.querySelector("#t-count");
          const decorativeOverlay = document.querySelector("body > div[aria-hidden='true'].pointer-events-none.fixed.inset-0");
          const surfaceInfo = {
            bodyBackground: getComputedStyle(document.body).backgroundColor,
            bodyBackgroundImage: getComputedStyle(document.body).backgroundImage,
            mainBackground: main ? getComputedStyle(main).backgroundColor : null,
            mainBackgroundImage: main ? getComputedStyle(main).backgroundImage : null,
            calculatorBackground: root ? getComputedStyle(root).backgroundColor : null,
            calculatorBackgroundImage: root ? getComputedStyle(root).backgroundImage : null,
            counterBackgroundImage: counter ? getComputedStyle(counter).backgroundImage : null,
            decorativeOverlayPresent: !!decorativeOverlay
          };
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          const unresolved = [], lowContrast = [];
          let count = 0, lowest = { ratio: Infinity, text: "", selector: "" };
          let node;
          while ((node = walker.nextNode())) {
            const text = (node.nodeValue || "").replace(/\s+/g, " ").trim();
            const el = node.parentElement;
            if (!text || !el || !visible(el)) continue;
            const fg = parse(getComputedStyle(el).color);
            if (!fg || fg.a < 0.999) continue;
            const chain = [];
            for (let current = el; current; current = current.parentElement) chain.unshift(current);
            let bg = { r: 255, g: 255, b: 255, a: 0 };
            let gradient = null;
            for (const current of chain) {
              const style = getComputedStyle(current);
              if (style.backgroundImage && style.backgroundImage !== "none") {
                gradient = current.tagName.toLowerCase() + (current.id ? "#" + current.id : "") + "." + String(current.className || "").toString().split(/\s+/).slice(0,4).join(".");
                break;
              }
              const layer = parse(style.backgroundColor);
              if (layer && layer.a > 0) bg = blend(layer, bg);
            }
            if (gradient || bg.a < 0.999) {
              unresolved.push({ text: text.slice(0, 80), gradient, backgroundAlpha: bg.a });
              continue;
            }
            const ratio = contrast(fg, bg);
            count++;
            if (ratio < lowest.ratio) lowest = { ratio: Math.round(ratio * 100) / 100, text: text.slice(0, 80), selector: el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") };
            const style = getComputedStyle(el);
            const large = Number.parseFloat(style.fontSize) >= 24 ||
              (Number.parseFloat(style.fontSize) >= 18.66 && Number.parseInt(style.fontWeight, 10) >= 700);
            const threshold = large ? 3 : 4.5;
            if (ratio + 0.01 < threshold) lowContrast.push({ ratio: Math.round(ratio * 100) / 100, threshold, text: text.slice(0, 80), selector: el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") });
          }
          const controlIssues = [];
          for (const el of document.querySelectorAll("input,textarea,select")) {
            if (!visible(el)) continue;
            const style = getComputedStyle(el);
            const bg = parse(style.backgroundColor);
            if (!bg || bg.a < 0.999) continue;
            if (el.placeholder) {
              const rawPlaceholder = parse(getComputedStyle(el, "::placeholder").color);
              if (rawPlaceholder && rawPlaceholder.a > 0) {
                const placeholderColor = rawPlaceholder.a < 0.999 ? blend(rawPlaceholder, bg) : rawPlaceholder;
                const ratio = contrast(placeholderColor, bg);
                if (ratio + 0.01 < 4.5) controlIssues.push({ kind: "placeholder", ratio: Math.round(ratio * 100) / 100, placeholder: el.placeholder.slice(0, 80), selector: el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") });
              }
            }
            if (el.value) {
              const ratio = contrast(parse(style.color), bg);
              if (ratio + 0.01 < 4.5) controlIssues.push({ kind: "input-value", ratio: Math.round(ratio * 100) / 100, value: String(el.value).slice(0, 40), selector: el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") });
            }
          }
          const alpha = value => {
            const c = parse(value);
            return c ? c.a : 0;
          };
          const calculatorAlpha = alpha(surfaceInfo.calculatorBackground);
          return {
            surfaceInfo,
            bodyOpaque: alpha(surfaceInfo.bodyBackground) >= 0.999,
            mainOpaque: alpha(surfaceInfo.mainBackground) >= 0.999,
            calculatorBackgroundResolved: calculatorAlpha === 0 || calculatorAlpha >= 0.999,
            count,
            lowest,
            unresolved: unresolved.slice(0, 10),
            unresolvedCount: unresolved.length,
            lowContrast: lowContrast.slice(0, 10),
            lowContrastCount: lowContrast.length,
            controlIssues: controlIssues.slice(0, 10),
            controlIssuesCount: controlIssues.length
          };
        });
        checkedTextNodes += result.count;
        console.log("CONTRAST_AUDIT " + route + " " + theme + " " + JSON.stringify(result));
        if (result.surfaceInfo.bodyBackgroundImage !== "none") failures.push({ route, theme, issue: "Body background image must not sit behind text", value: result.surfaceInfo.bodyBackgroundImage });
        if (!result.bodyOpaque) failures.push({ route, theme, issue: "Body background must resolve to a solid color", value: result.surfaceInfo.bodyBackground });
        if (result.surfaceInfo.mainBackgroundImage !== "none") failures.push({ route, theme, issue: "Main content background must not use a gradient", value: result.surfaceInfo.mainBackgroundImage });
        if (!result.mainOpaque) failures.push({ route, theme, issue: "Main content must have a fully opaque background", value: result.surfaceInfo.mainBackground });
        if (!result.calculatorBackgroundResolved) failures.push({ route, theme, issue: "Calculator card must be transparent over the opaque main surface or fully opaque, not translucent", value: result.surfaceInfo.calculatorBackground });
        if (result.surfaceInfo.calculatorBackgroundImage !== "none") failures.push({ route, theme, issue: "Calculator card must not use a gradient background", value: result.surfaceInfo.calculatorBackgroundImage });
        if (result.surfaceInfo.counterBackgroundImage && result.surfaceInfo.counterBackgroundImage !== "none") failures.push({ route, theme, issue: "Tasbih counter output must not use a gradient background", value: result.surfaceInfo.counterBackgroundImage });
        if (result.surfaceInfo.decorativeOverlayPresent) failures.push({ route, theme, issue: "Decorative fixed gradient overlay must be absent on calculator pages" });
        if (result.unresolvedCount) failures.push({ route, theme, issue: "Visible text has unresolved gradient/transparent background", count: result.unresolvedCount, examples: result.unresolved });
        if (result.lowContrastCount) failures.push({ route, theme, issue: "Visible text is below WCAG contrast threshold", count: result.lowContrastCount, examples: result.lowContrast });
        if (result.controlIssuesCount) failures.push({ route, theme, issue: "Form control text or placeholder is below WCAG contrast threshold", count: result.controlIssuesCount, examples: result.controlIssues });
      }
      if (pageErrors.length) failures.push({ route, issue: "Browser runtime errors", pageErrors });
      await page.close();
    }
  } finally {
    await browser.close();
  }
  console.log("CONTRAST_AUDIT_TOTAL routes=" + ROUTES.length + " themes=2 textNodes=" + checkedTextNodes + " failures=" + failures.length);
  if (failures.length) {
    console.error("CONTRAST_AUDIT_FAILURES " + JSON.stringify(failures, null, 2));
    process.exitCode = 1;
  } else {
    console.log("PASS: visible text on Zakat, BMI and Tasbih pages has resolvable backgrounds and WCAG AA contrast in light and dark themes.");
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
