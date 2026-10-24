# Calculator First-Screen and Profit Intent Blueprint

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve first-screen access to all existing English calculator tools except Standard, BMI and Tasbih, and match Profit & Loss functionality to both business and product intent.

**Architecture:** Preserve all existing URLs, calculator IDs, schema generation, navigation and sitemap. Move each non-excluded calculator above its introductory lead, use scoped responsive CSS for compact but accessible controls, and provide an explicit business/product mode switch on the profit page.

**Tech Stack:** Python static generator, Tailwind CSS, vanilla JavaScript, GitHub Actions, Playwright and Vercel.

## Global Constraints

- Do not change Standard Calculator, BMI Calculator or Tasbih Counter.
- Preserve canonical URLs, internal links, structured data, indexing directives and existing product profit calculations.
- Touch controls at least 44 CSS pixels high where practical.
- Never claim a guaranteed Google ranking, guaranteed indexing or a layout that fits every possible screen size.
- Business profit is a simplified operating P&L: revenue minus cost of goods sold minus other expenses, not a certified accounting statement.
- Never merge or deploy while a required CI check is failing.

---

### Task 1: Search-intent diagnosis and correct profit calculator

**Files:** Modify `build.py`, `static/app.js`. Test `tests/site-output-smoke.py`, `tests/viewport-audit.cjs`.

**Interfaces:** Existing `/profit-loss-calculator/` route, `#pl-form`, `#pl-result`; add `pl-mode`, `#pl-business-fields`, `#pl-product-fields`, `#p-revenue`, `#p-cogs`, `#p-expenses`.

- [x] Add business mode with revenue, COGS and other expenses, plus existing product cost/sell mode.
- [x] Validate missing, negative and non-finite values, and handle zero revenue and zero cost without division by zero.
- [x] Distinguish net operating margin (profit / revenue) from product markup (profit / cost).
- [x] Align title, description, guide, worked example and FAQs with actual functionality.
- [x] Add generated-output and browser interaction checks.
- [ ] Record final passing build and browser checks before merging.

### Task 2: Prioritize remaining tools in first viewport

**Files:** Modify `build.py`, `styles/input.css`. Test `tests/site-output-smoke.py`, `tests/viewport-audit.cjs`.

**Interfaces:** Existing `#tool-calculator`, `.ca-tool-calculator`, `.ca-tool-lead-after`; preserve every existing input and button ID.

- [x] Move descriptive lead below tools for Zakat, Profit & Loss, Discount, Age, Unit Converter and Stopwatch.
- [x] Compact mobile headings, form gaps, labels and result panels without removing fields.
- [x] Keep input/button touch targets accessible and prevent horizontal overflow.
- [x] Test button visibility at 360x740, 390x844 and desktop 1366x768 with real Chromium.
- [ ] Confirm final browser audit PASS after all changes.

### Task 3: SEO evidence and release

**Files:** Existing GitHub Actions workflows plus `.github/workflows/first-screen-audit.yml`.

**Interfaces:** Production site `https://calculateallinone.vercel.app` and existing canonical calculator routes.

- [x] Compare profit calculator intent against published competitor product-profit, markup, margin and business-net-income tools.
- [x] Ground recommendations in Google Search Central guidance on useful content, descriptive titles and technical eligibility.
- [ ] Obtain current Google Search Console page/query data before attributing positions 6–14 to any particular root cause. Searcherries project currently has no GSC connection; keyword volume data is not available.
- [ ] Require passing build, HTML/SEO and real-browser checks before merge.
- [ ] Confirm Vercel production READY and canonical domain alias after merge.
- [ ] Check live production pages and report any test not completed.

## Verification acceptance criteria

At 360x740, 390x844 and 1366x768, each non-excluded page must have its last primary button fully above the viewport bottom and no horizontal overflow. The browser test must confirm business revenue 1,000, COGS 600, expenses 150 returns operating profit 250 and margin 25%; product cost 80 and price 100 returns profit 20 and markup 25%.

## Unresolved externally observable constraints

Exact first-screen visibility on devices smaller than 360x740, browsers with enlarged text or accessibility zoom, and user-specific browser chrome heights is not guaranteed. Search Console query-level positions and keyword search volumes remain unverified without connected performance data. Neither layout changes nor titles guarantee higher rankings.
