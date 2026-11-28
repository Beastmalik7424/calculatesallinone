# PR #366 evidence audit — 28 November 2026

## Scope and guardrails

Repository: `Beastmalik7424/calculatesallinone`  
PR: [#366 — Improve SEO regression coverage for Tasbih, Years to Days and EMI](https://github.com/Beastmalik7424/calculatesallinone/pull/366)  
Audited application/content/test commit: `e5b5254e6ff5ca71f46a1022a39a55076080275c`  
PR head at the audit snapshot: `2e5cd76aa6b40fbf3870f62f4546721f6bd64a17` (documentation-only commit)  
Branch: `seo-tests-tasbih-years-emi-2026-11-27`

This audit does not authorize merging, production deployment, ranking claims, or changes to calculator layout. No CSS stylesheet is among the PR's changed files. The changed-file list includes content, calculator logic/tests, workflow configuration, `emi-calculator.html`, and `vercel.json`. The source diff was reviewed for the calculator-first constraint. The content additions are explanatory copy/FAQ material; the browser first-screen and EMI viewport CI gates pass on the audited head.

## Exact-head CI evidence

All seven pull-request workflow runs associated with the audited SHA completed with conclusion `success`:

| Workflow | Run ID | Result |
|---|---:|---|
| Zakat focused verification | 46064253620 | success |
| Query Calculator independent verification | 46064253593 | success |
| Site build and monetization checks | 46064253717 | success |
| Workflow security contract | 46064253673 | success |
| Zakat calculator QA | 46064253603 | success |
| First-screen calculator browser audit | 46064253670 | success |
| Build and smoke test | 46064253690 | success |

The Build and smoke test job completed all 33 substantive steps, including site build, calculator behaviour, generated-page validation, Lighthouse SEO, headless browser console checks, and safe monetization configuration. These are CI/browser checks against the built artifact, not a live-browser check of a Vercel preview.

The latest commit `9b5d764...` updates the Tasbih content assertion to match the concise introduction. Its parent commit contains the actual content adjustment. The Query Calculator source change explicitly handles bare numeric input and number-plus-unit input without guessing a conversion target; the exact-head Query Calculator verification passed.

## Search Console evidence boundary

The PR's verified Search Console snapshot covers **22–24 November 2026 only**, through the connected recent-three-days data source. It is not a monthly search-volume report and does not establish a trend.

Recorded page-level values in the PR evidence:
- Years-to-Days: 174 impressions, 0 clicks, 0% CTR, average position 59.14.
- Tasbih: 14 impressions, 0 clicks, average position 6.93. The query `tasbih calculator` had 10 impressions at position 6.2; `calculator tasbih` had 2 impressions at position 8.5.
- EMI: 4 impressions, 0 clicks, average position 7.5; no query rows were returned for the page.
- Query Calculator: no page-level data was returned in that finalized window.

The 26 November export was not independently available in the connected source. OpenRush keyword research quota was exhausted and Google Trends comparisons were unavailable. Therefore this report makes no monthly volume, growth, rising-query, or trending-keyword claim. These limits must remain visible rather than being filled with estimates.

## Public competitor scan and feature benchmark

Searches on 28 November 2026 surfaced the following pages for the relevant intents. The sample deliberately includes strong topical competitors, not an asserted Google rank order. **These search results do not establish that any listed site occupies positions 1–5 in Pakistan or another fixed market.** Exact Google SERP positions require a country/device-specific live SERP data source; the connected OpenSEO account currently has no project, and the earlier OpenRush keyword quota was exhausted.

### Tasbih / Tasbeeh counter

Five substantive comparison pages:
- [Ihsabha Digital Tasbih Counter](https://ihsabha.com/islamic/digital-tasbih-counter) — custom dhikr, round targets, daily/all-time rounds, sound/vibration, local privacy and religious references.
- [Nakhtu Digital Tasbih Counter](https://nakhtu.com/en/tools/tasbih) — 33/100/free targets, automatic round reset, daily total, vibration, Undo and local persistence.
- [ToolNova Online Tasbeeh Counter](https://www.toolnova.org/islamic-tools/tasbeeh-counter) — 33/99/100/500/1,000/custom targets, guided after-salah flow, haptics, streaks, 14/35-day stats, per-dhikr totals, custom dhikr and backup/restore.
- [Sunnah Tools Tasbih Counter](https://sunnah.tools/tools/tasbih-counter/) — focused Islamic tool positioning and religious context.
- [Tasbih.info changelog](https://tasbih.info/changelog) — dhikr libraries, count routines, history and nuanced target handling.

**Our verified page capability:** five preset phrases plus custom phrase, 33/99/100/custom target up to 10,000, tap and Space/Enter counting, Undo, confirmed Reset, lifetime total, local same-device saving when storage is available, explicit storage-failure notice and a clear statement that the counter does not verify recitation or issue religious rulings.

**Competitive gap:** no daily goal, streak, session history, per-dhikr totals, export/restore, automatic round progression, selectable haptic/sound controls or verified offline/PWA caching. ToolNova and Ihsabha currently show a broader tracking feature set. These are product features, not copy gaps. Adding them would alter the existing counter UI/behaviour and therefore is intentionally outside this PR's zero-layout-change constraint. Do not describe our counter as offering those features.

### Years-to-Days calculator

Five substantive comparison pages:
- [Calculator Academy Years to Days](https://calculator.academy/years-to-days-calculator/) — 365, 365.25 and Gregorian average methods, plus exact anniversary spans and leap-year-aware dates.
- [Calculator Junction Years to Days](https://calculatorjunction.com/time-unit-converter/years-to-days) — bidirectional live converter, precision selector, formula, multi-unit equivalents and reference table.
- [DQYDJ Years to Days](https://dqydj.com/years-to-days-calculator/) — live reverse conversion, 365/365.25 toggle and milestone table.
- [UnitFlip Years to Days](https://unitflip.org/time/years-to-days) — 365.2425 mean Gregorian factor, precision controls, unit definitions and source notes.
- [Qvert Years to Days](https://qvert.ai/time/year-to-day/) — fast converter, formula, table and FAQ.

**Our verified page capability:** bidirectional conversion; 365-day, Julian 365.25-day and mean Gregorian 365.2425-day methods; exact Gregorian anniversary mode; leap-year rule explanation; worked 5, 10, 13, 19 and 30-year examples; reverse day-to-year examples; and explicit warnings that average conversions are not exact date intervals. Browser regression coverage includes 1,000 seeded property simulations at 320, 390 and 1366-pixel viewports.

**Competitive gap:** Calculator Junction/UnitFlip have broader generic time-unit conversion tables and precision selection. Calculator Academy has an author expertise profile. Our differentiation is the explicit exact-anniversary workflow and clear separation of fixed-year conventions from real calendar intervals. A broader unit converter or additional precision UI would be a separate feature change.

### EMI calculator

Five substantive comparison pages:
- [Educativz Pakistan Loan EMI Calculator](https://www.educativz.com/tools/loan-emi-calculator/) — reducing/flat rate modes, down payment, fees, recurring/one-time prepayment, later rate reset, affordability solved backwards, monthly/yearly schedules and Pakistan-specific scheme/KIBOR examples.
- [Investify Pakistan Loan Calculator](https://www.investify.pk/tools/loan-calculator) — reducing-balance calculation, 0% rate handling, flat-versus-reducing explanation and KIBOR context.
- [HisabCenter EMI Calculator](https://www.hisabcenter.pk/tools/emi-loan) — PKR personal/car/bike positioning, total interest and affordability guidance.
- [Gem Pakistan Loan EMI Calculator](https://www.gem.net.pk/loan-emi-calculator/) — reducing-balance formula, flat-rate comparison and total-cost framing.
- [SignTest Car Installment Calculator](https://signtest.pk/car-installment-calculator/) — side-by-side comparison of 22 banks/products and KIBOR-linked assumptions (its rates are date-sensitive and must not be copied without re-verifying official bank sources).

**Our verified page capability:** amortization schedule, total principal/interest/payment, one-time or recurring prepayment with tenure/EMI choices, affordability estimate, two-loan comparison, CSV export, shareable calculation parameters, currency formatting, formula explanation and lender-quote limitations. The EMI engine has 26 deterministic checks plus 2,000 seeded schedule-reconciliation scenarios.

**Competitive gap:** no direct down-payment input, processing-fee/APR model, flat-rate calculation mode, variable-rate reset, inverse principal/tenure solver or verified live bank rate feed. Educativz currently offers the broadest directly comparable Pakistan feature set in this sample. These features require new calculator controls and calculation behaviour; they cannot be added while preserving the explicit zero-layout-change gate. Do not invent live bank data or imply the existing EMI engine supports these options.

## Google ranking and AdSense evidence standard

Google states that Search prioritizes helpful, reliable information created for people, evaluates usefulness and does not design ranking systems to favour a particular site. A competitor benchmark or Lighthouse score is not a ranking guarantee:
- [Google ranking principles](https://developers.google.com/search/docs/appearance/ranking-systems-guide)
- [Google helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google page experience guidance](https://developers.google.com/search/docs/appearance/page-experience)

AdSense requires unique, relevant content and a good user experience. The automated monetization CI test does not certify account approval or consent configuration:
- [Google AdSense page readiness](https://support.google.com/adsense/answer/7299563)
- [Google AdSense eligibility](https://support.google.com/adsense/answer/9724)



## AdSense and originality evidence

Official Google guidance says AdSense-ready pages should provide unique, relevant content and a good user experience, and that sites must add their own original value rather than merely reuse external material:
- [Google AdSense: Make sure your site's pages are ready](https://support.google.com/adsense/answer/7299563)
- [Google Search Central: Helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

The exact-head CI build and monetization checks passed. This demonstrates automated project checks only. It does **not** establish AdSense approval, account-side consent configuration, ad serving, revenue, or a Google ranking.

Independent plagiarism verification remains unresolved. The AISEO plagiarism-check request previously returned HTTP 502; a subsequent retry failed before returning an originality score. Exact-phrase web spot checks are not a substitute for a full-document plagiarism scan. No originality percentage or “100% unique” claim is made.

## Deployment and live-browser boundary

The original code/test SHA `9b5d764774d65c2cc5321c6cf220d6f9ec2992b0` did not have its own Vercel deployment. A documentation-only commit `89ea871b8202bc5574c542f13a7708211cb96940` was subsequently deployed by Vercel and verified READY:
- Deployment ID: `dpl_6vFt3hKjkzQZwHZie39kgEKswVtY`
- Preview URL: https://calculatesall-cxyjtvkqd-malikadeelbhatti-1187.vercel.app
- Exact deployed SHA: `89ea871b8202bc5574c542f13a7708211cb96940`
- The application code in this preview is unchanged from the code-tested SHA `9b5d764...`; the intervening commit added only this evidence report.
- HTTP 200 and canonical page content were checked for homepage, EMI, Tasbih, Years-to-Days, Query Calculator, sitemap.xml, robots.txt and llms.txt. Sitemap contains 42 URLs.

The browser automation provider available through the connected HYPD plan denied access. The Skyvern browser session creation interface returned a schema mismatch, and the TinyFish browser wallet had a negative balance. No paid browser automation or account top-up was initiated. Therefore an interactive live-preview session is still **not verified**. GitHub Actions' Playwright browser checks are the reliable alternative for the tested built artifact, but they are not a live deployed-browser check.

The later documentation-only commit `ae4319b6957745a147de4e501ee393ea0937057d` has a Vercel Git status of **failure** with a `build-rate-limit` target and no deployment was found for that SHA. This did not change the app code. The READY preview at `89ea871...` remains the latest verified deployment of the same app code. Do not claim that `ae4319...` itself is deployed.

## Originality spot-check and remaining evidence gates

The independent AISEO full-document plagiarism API was called with the complete, unmodified HTML of each of the three deployed page documents:
- Tasbih Counter: 33,420 characters — HTTP 502 Bad Gateway.
- Years-to-Days: 67,372 characters — HTTP 502 Bad Gateway.
- EMI Calculator: 67,444 characters — provider returned “busy” before analysis.

Five exact-phrase web searches were also attempted against representative sentences from the pages. No direct copied-page match was returned for the sampled wording, but search-engine phrase checks cannot certify originality or replace a full-document plagiarism report. **No originality percentage is claimed.**

- Exact code-head GitHub Actions: **PASS (7/7) for `9b5d764...`**.
- Documentation-head GitHub Actions: **PASS (7/7) for `89ea871...`**. The Build and smoke test completed all 33 substantive steps, including Lighthouse SEO audits for ten pages, headless browser console checks on ten pages, and safe monetization configuration. All setup/cleanup steps also completed successfully.
- The next commit `ae4319b...` changed only this report. No application code, tests, CSS, or configuration changed in that commit. GitHub returned no new workflow run for that docs-only commit at the time of the poll.
- CSS stylesheet files changed: **NONE**. The standalone EMI HTML diff changes metadata, structured data and content only; no inline style or CSS rules changed.
- Calculator first-screen and EMI viewport checks: **PASS in the existing GitHub Actions browser audits**.
- EMI engine regression: **26 deterministic checks plus 2,000 seeded schedule-reconciliation scenarios**.
- Years-to-Days regression: **1,000 deterministic browser property simulations per viewport**.
- Query Calculator: browser regression cases include plain digits, complete natural-language questions with digits, grouped thousands, unit clarification and multiple locales.
- GSC: **verified only for 22–24 November 2026**; 26 November export and keyword trend data remain unavailable.
- Competitor comparison: **five substantive comparison pages reviewed per topic**. This is a content/feature benchmark, not proof of exact Google top-five ranking positions.
- Independent originality score: **NOT VERIFIED** because the provider failed before returning results.
- Vercel preview: **READY for documentation SHA `89ea871...`**, with HTTP 200 verified on the eight listed routes. The later docs-only SHA `ae4319...` was not deployed because its Vercel status reported `build-rate-limit`.
- Interactive browser verification of the deployed preview: **NOT VERIFIED**. GitHub Actions Playwright checks against the generated build remain the reliable available alternative.
- AdSense approval and account-side consent: **NOT VERIFIED**; only Google can approve the account and automated CI cannot inspect account settings.

Keep PR #366 **OPEN / DRAFT / UNMERGED** until the current documentation-head workflow completes and the independent originality/live-preview browser gates are resolved. Do not claim first-page or top-five rankings as guaranteed. Product gaps requiring new controls (Tasbih tracking/history and EMI fees/down-payment/flat-rate/floating-rate features) are documented but deliberately not implemented because the fixed zero-layout-change constraint forbids those UI changes.


---

## Follow-up verification and policy research — 28 November 2026

This section supersedes earlier status statements above where the branch head or evidence window has changed.

### Source correction found and implemented

A source review found a factual mismatch on the Worship hub: its Tasbih instructions advertised targets of 33, 100 and 1,000 plus unlimited, while the actual counter supports 33, 99, 100 and a custom target from 1 to 10,000.

The source copy in `content_v13.py` now accurately explains:
- Preset targets 33, 99 and 100, or a custom target from 1 to 10,000.
- Undo for the last tap and Space/Enter keyboard counting.
- Reset confirmation.
- Same-device persistence only when browser storage is available, with no cross-device sync and possible loss after clearing browser data or using private browsing.

A generated-output regression assertion was added to `tests/site-output-smoke.py`. Test-first evidence:
- Test commit `e7fd8a4bd7f42be10e685a2c0f2ab99bb04d88a9` failed at the new assertion with: `AssertionError: Worship hub Tasbih instructions must match the live preset and custom target controls`.
- The content correction was committed as `706cab0fe5dc01459880d6aba465f1776364dfb3`.
- An attempted `dateModified`/sitemap lastmod addition for `/worship/` failed the existing freshness contract because that page must not publish an unverified `dateModified`. The unsupported date entries were removed in commits `f69d334a412f38db9df0935fde0d5ff493dfaae0` and `833b2e48e84e53b44e6d10412744b9abd47cdbcb`. No visible update date or structured date is being invented.
- The latest source head at this point is `833b2e48e84e53b44e6d10412744b9abd47cdbcb`. A fresh all-workflow pass on this exact head is still required before calling the correction verified.

No CSS, layout, calculator controls, calculator formulas, URLs, canonicals, or hand-edited `public/` output were changed.

### Current Google Search guidance

Official Google Search Central documentation was checked on 28 November 2026:
- The documentation update dated 24 November 2026 introduced a consolidated ranking principles section. Google says results are ranked for helpfulness and query relevance, not to favour a particular site: https://developers.google.com/search/updates and https://developers.google.com/search/docs/ranking/principles-for-ranking-results
- The people-first content self-assessment emphasizes original information, substantial value beyond competing pages, accurate claims, sourcing, expertise, and a satisfying user experience: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google's generative-AI search guide explicitly says `llms.txt` does not help or harm Google Search visibility, there is no preferred page length, and no special AI schema or keyword-chunking tactic is required. Keep `llms.txt` only as an optional resource for other systems, not as a Google ranking tactic: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- FAQ rich results stopped appearing in Google Search on 7 May 2026. Visible FAQs remain useful for readers. Google says there is no need to proactively remove FAQ structured data, but it should not be presented as a Google rich-result or ranking advantage: https://developers.google.com/search/updates
- Google spam policy identifies large volumes of unoriginal, low-value pages and near-copy keyword variants as scaled content abuse. Do not create separate pages for every numeric query variant: https://developers.google.com/search/docs/essentials/spam-policies

### AdSense policy and live configuration audit

Official AdSense guidance was checked:
- Pages should have unique, original, relevant content, clear navigation and a good user experience: https://support.google.com/adsense/answer/7299563
- AdSense eligibility requires original, high-quality content that attracts an audience: https://support.google.com/adsense/answer/9724
- Google reviews the whole site, and the site must be connected and approved before ads can show: https://support.google.com/adsense/answer/7584263
- Publisher policies apply to all page content and can disable ad serving: https://support.google.com/adsense/answer/10008391

The Vercel project environment was checked without decrypting secrets. The visible Production environment list contained only `GEMINI_API_KEY`; no `ADSENSE_SLOT` or `ADSENSE_CONSENT_READY` variables were present, and the API reported zero hidden Production variables. The build therefore correctly fails closed: the publisher client has a code default, but no ad-unit slot is configured and consent readiness is false. Do not set a fabricated slot ID or turn consent readiness on without the publisher's confirmed CMP/account-side setup. AdSense account approval and consent configuration remain unverified and require the actual publisher account details.

### Search Console and trend evidence

The SMEPost Search Console connection exposes the verified URL-prefix property `https://calculateallinone.vercel.app/` as `siteOwner`, but the account is on `free_recent_three_days` access. The latest finalized range returned was **22–24 November 2026**. It does not provide prior-period comparison.

Page insights for that exact range:
- Tasbih: 14 impressions, 0 clicks, 0% CTR, average position 6.93. `tasbih calculator`: 10 impressions at position 6.2. `calculator tasbih`: 2 impressions at position 8.5.
- Years-to-Days: 174 impressions, 0 clicks, average position 59.14. Queries include `how many days in 13 years` (3 impressions, position 50.33), `how many days are in 14 years` (2 impressions, position 79), `how many days are in 15 years` (3 impressions, position 77.33), `how many days are in 20 years` (2 impressions, position 76.5), `how many days are in 21 years` (1 impression, position 37), `how many days are in 60 years` (1 impression, position 37), and `800000/365` (1 impression, position 3).
- EMI: 4 impressions, 0 clicks, 0% CTR, average position 7.5; no query rows were returned.

These are small, finalized Search Console observations, not monthly search volumes or evidence of a rising trend. HYPD's selected domain property `sc-domain:calculateallinone.vercel.app` is marked `siteUnverifiedUser`, and Google refused that connector's request for insufficient property role. HYPD's Google Trends research tool also returned `plan_denied` on the current plan. Google Trends data therefore remains unavailable in this audit. No trending or growth claim is made. The HYPD plan/access details are shown here if the account owner chooses to review them: https://app.hypd.ai/plans?utm_source=mcp&utm_content=tool_access_plan&utm_term=seo_google_trends

### Five named competitor benchmark

The following cross-site benchmark covers the five competitor brands named in the project goals. It is a product/content feature comparison, not proof of their exact Google positions in Pakistan:
- Calculator.net Payment Calculator: monthly payment, fixed-term and fixed-payment solving, totals and amortization schedule: https://www.calculator.net/payment-calculator.html
- Omni Calculator EMI: EMI, total payable and interest, with the ability to solve one of the input variables and explanatory floating-rate/prepayment content: https://www.omnicalculator.com/finance/emi
- CalculatorSoup Loan Calculator: can solve loan amount, interest rate, number of months or monthly payment, with a printable amortization schedule and advanced compounding options: https://www.calculatorsoup.com/calculators/financial/loan-calculator.php
- GigaCalculator Loan Calculator: exposes APR, compounding frequency and payback amount, and explicitly notes it does not currently provide a full amortization schedule: https://www.gigacalculator.com/calculators/loan-calculator.php
- Math.tools Year-to-Day table: broad year-to-day lookup table covering whole-year rows and larger milestones: https://math.tools/table/unit/time/yr-to-d

The topic-specific five-page scans already recorded above remain the stronger direct benchmarks for Tasbih, Years-to-Days and Pakistan EMI. Our current differentiators remain the supported Tasbih keyboard/Undo/local persistence behaviour, Years-to-Days fixed-year conventions plus exact Gregorian anniversary mode, and EMI prepayment/comparison/CSV schedule tools. Known product gaps remain explicitly disclosed and are not silently claimed as existing features. Adding them would require UI or calculation-scope changes outside this PR's fixed no-layout-change requirement.

### Current gate status

- The Tasbih Worship hub factual mismatch has a source fix and a regression test, but the latest head still needs a fresh passing workflow run.
- Google Trends and extended GSC history are unavailable on the connected plan/permissions; no fabricated trend data has been substituted.
- The Vercel Production environment lacks the AdSense slot and consent-ready configuration; ads remain safely disabled.
- Exact Google first-page/top-five position, independent full-document originality score, interactive deployed-preview browser verification, and AdSense approval remain unverified.
- PR #366 must remain OPEN / DRAFT / UNMERGED. Do not merge or deploy production until exact-head checks and remaining external/account gates are resolved.


## Final exact-head verification — 28 November 2026

### Exact source commit and automated verification

Application/content/test source commit: `e5b5254e6ff5ca71f46a1022a39a55076080275c`.

All **7/7 GitHub Actions workflows completed successfully** on this exact commit:
1. Workflow security contract — PASS.
2. Query Calculator independent verification — PASS.
3. Site build and monetization checks — PASS.
4. Zakat focused verification — PASS.
5. Zakat calculator QA — PASS.
6. First-screen calculator browser audit — PASS.
7. Build and smoke test — PASS.

Evidence from the successful build:
- 47 generated pages checked and 260 JSON-LD blocks retained.
- 42 unique sitemap URLs, canonical URLs, internal links, language metadata and indexability checks passed.
- AdSense ID/slot gating, `ads.txt` line format and disabled-by-default behaviour passed.
- 17,000 deterministic calculator simulations passed with 51,694 independently counted assertions and 3 generated-page integration contracts.
- EMI engine: 24 tests, including 2,000 seeded schedule checks.
- Query Calculator DOM, multilingual, date and arithmetic regression passed.
- Headless browser audit: 10 scoped URLs plus calculator end-to-end, zero console/page errors.
- Calculator layout audit: 28 English/Urdu routes across 4 viewports, 112 scenarios, 112 screenshots, 0 failures.
- Contrast audit: 3 routes across 2 themes, 834 text nodes, 0 failures.
- Lighthouse SEO: homepage, BMI, Zakat and calorie pages scored 100/100. Seven of the ten additional scoped pages scored 100/100. The three intentionally noindex language pages scored 69/100 solely for the expected `is-crawlable` finding; the workflow explicitly permits that expected result. The ten-page audit passed.

### Preview deployment and HTTP checks

Vercel automatically created a **Preview**, not a Production deployment, for exact commit `e5b5254...`:
- Deployment: `dpl_3b4L5v83NKx71MX6qCTjdD6v7GGE`
- State: READY
- Preview: https://calculatesall-9brindh8b-malikadeelbhatti-1187.vercel.app

HTTP fetch returned 200 for:
- `/emi-calculator/`
- `/worship/`
- `/tasbih-counter/`
- `/years-to-days-calculator/`

The preview sitemap contains 42 URLs. The preview sends `X-Robots-Tag: noindex` and uses production canonicals, as expected for a protected preview. This is not evidence that the preview itself should be indexed and is not a Production deployment.

### Google Search Console URL Inspection

On the verified URL-prefix property `https://calculateallinone.vercel.app/`, direct URL Inspection returned:
- `/tasbih-counter/`: Submitted and indexed; robots allowed; successful mobile crawl; Google canonical equals user canonical; last crawl 2026-11-07.
- `/years-to-days-calculator/`: Submitted and indexed; robots allowed; successful mobile crawl; Google canonical equals user canonical; last crawl 2026-11-07.
- `/emi-calculator/`: Submitted and indexed; robots allowed; successful mobile crawl; Google canonical equals user canonical; last crawl 2026-11-07.
- `/worship/`: Discovered - currently not indexed; sitemap found; no fetch/crawl result yet.
- `/money/`: Discovered - currently not indexed; sitemap found; no fetch/crawl result yet.

The current homepage category navigation links to both `/worship/` and `/money/`. The three priority calculator pages are already indexed, but Google last crawled them on 7 November, before the latest 27–28 November copy changes. Re-inspect after the Production release and request indexing through the normal Search Console URL Inspection interface if appropriate. Do not use the Indexing API for ordinary calculator pages.

The account-level site-index summary reported nine URLs not indexed or returning 404. Only the five URLs above were individually inspected in this pass; the remaining seven have not been individually diagnosed and must not be described as fixed.

### Current market context, not keyword-volume evidence

A 20 November 2026 Dawn report says Pakistan's outstanding auto loans reached PKR 416.5 billion in October, marking a 23rd consecutive monthly increase, while October car sales rose 41% year over year. This is a current auto-finance market signal, not proof of a Google query trend or search volume: https://www.dawn.com/news/1956705

The State Bank of Pakistan's official monetary-policy page showed the policy rate at 12.00% per annum following the October 2026 decision. The EMI page now links to the official SBP page and explicitly distinguishes the policy rate from a lender's quoted markup or KIBOR-linked rate: https://www.sbp.org.pk/our-operations/monetary-policy

A local EMI competitor, EMI Calculator Pakistan, exposes KIBOR-based car-finance context and bank-offer comparisons. Its third-party displayed rate values are not treated as verified official rates. The current page deliberately links to SBP context rather than copying volatile third-party rates: https://emicalculator.pk/

### Originality recheck

The full, unmodified preview HTML was submitted again to the originality provider:
- Tasbih: 502 Bad Gateway.
- Years-to-Days: 502 Bad Gateway.
- EMI: provider busy response.

No originality percentage or certification is available. Earlier exact-phrase web checks did not return a direct copied-page match for the sampled passages, but this is not a full-document originality certificate.

### Final gate interpretation

The application changes and automated quality checks are green on `e5b5254...`. The preview is READY and its four scoped pages return HTTP 200. Production was not deployed, and PR #366 remains OPEN / DRAFT / UNMERGED.

Remaining external/account gates are not code defects:
- Production AdSense environment has no `ADSENSE_SLOT` or `ADSENSE_CONSENT_READY`; do not enable ads until the real slot ID and confirmed consent-management setup are supplied.
- AdSense account approval has not been verified.
- Google Trends research is denied on the connected HYPD plan, so no search-trend claim is made.
- Full-document originality scoring remains unavailable because the checker repeatedly returned 502/busy.
- The two category hubs are discovered but not indexed, and seven additional URLs from the site-index summary remain individually uninspected.
- Google has not re-crawled the three priority calculators since 7 November.

These constraints prevent a truthful statement that only Production deployment remains. Keep the PR open and draft until the external/account gates are resolved or explicitly accepted by the project owner. No first-page ranking guarantee is possible.


## Superseding site-index and internal-link audit — 28 November 2026

A final read-only site-index audit on the verified Search Console property returned:
- 44 known URLs and 44 previously inspected records.
- 8 last-known URLs flagged as `Discovered - currently not indexed`.
- Sitemap `https://calculateallinone.vercel.app/sitemap.xml`: HTTP 200, zero errors, zero warnings; last downloaded by Google on 21 November 2026.
- The audit attempted five immediate rechecks, but Google did not return answers before timeout. Those five rows retain their last-known state and are not fresh confirmations.

Eight last-known discovered/not-indexed URLs:
1. `/percentage-calculator/` — one Google-listed incoming page; one impression in the 90-day snapshot.
2. `/compound-interest-calculator/` — no Google-listed incoming page; zero impressions.
3. `/date-calculator/` — no Google-listed incoming page; zero impressions.
4. `/math/` — two Google-listed incoming pages; zero impressions.
5. `/money/` — one Google-listed incoming page; zero impressions.
6. `/percentage-difference-calculator/` — one Google-listed incoming page; zero impressions.
7. `/ratio-calculator/` — one Google-listed incoming page; zero impressions.
8. `/worship/` — one Google-listed incoming page; zero impressions.

Four additional addresses were last-known as unknown to Google: `/calorie-calculator/`, `/contact/`, `/fraction-calculator/`, and `/health/`. No 404 was reported in this audit. Do not treat these last-known states as fresh URL Inspection results.

Direct URL Inspection on 28 November independently confirmed:
- `/tasbih-counter/`, `/years-to-days-calculator/` and `/emi-calculator/` are submitted and indexed, with successful mobile fetches and matching Google/user canonicals. Their last recorded crawl remains 7 November.
- `/worship/` and `/money/` remain `Discovered - currently not indexed`, with no crawl/fetch result yet.

The current READY preview HTML was also checked for internal-link coverage:
- Homepage links to the percentage, compound-interest, date, math, money, worship, calorie, contact, fraction and health destinations.
- Tasbih links to Worship.
- Years-to-Days links to Date Calculator.
- EMI links to Money and Compound Interest.
- Profit/Loss and Discount link to relevant percentage/money tools.
- Math, Fraction, Percentage and Ratio pages cross-link to their related math tools.

Therefore, no duplicate or keyword-stuffed internal links were added. The current source already has contextual links; the remaining issue is that Google has not yet crawled or selected several known URLs. The sitemap is healthy, but Google last downloaded it on 21 November. Recheck after Production deployment and use normal Search Console URL Inspection for the affected pages. Request indexing is a Search Console UI action; the Indexing API is not for ordinary calculator pages.

The Search Console connector's daily operation limit was reached during this audit, so no further live URL inspections can be run until its stated reset. This is an access/quota limitation, not evidence that the remaining URLs are fixed.


## Subsequent verification refresh — 28 November 2026

### Main-branch URL preservation check

The live `main` branch advanced to `e3f548ad4670fbfae8372b12319d887c088b0ace` after the PR's merge base `4b0ceb175a71443192644b6fe05828bd629e0254`. That main-only commit adds a permanent 301 redirect from the historical `/ur/zakat` and `/ur/zakat/` paths to `/ur/zakat-calculator/`, plus regression assertions in `tests/site-output-smoke.py`. The PR branch did not contain that redirect. This integration update carries the main commit as a merge parent and adds the exact redirect and its regression assertions to the PR tree, preventing the open PR from removing the legacy route when it is eventually merged.

No calculator formula, control, page URL, CSS file, or calculator layout is changed by this integration update.

### Latest finalized Search Console refresh

The connected SMEPost Search Console property `https://calculateallinone.vercel.app/` returned finalized data for **2026-11-23 through 2026-11-25**. Access remains `free_recent_three_days`, with no prior-period comparison.

- Tasbih page: 18 impressions, 0 clicks, 0% CTR, average position 6.50. `tasbih calculator`: 13 impressions at 6.23; `calculator tasbih`: 3 impressions at 8.67.
- Years-to-Days page: 170 impressions, 0 clicks, 0% CTR, average position 56.54. `how many days in 19 years` appeared once at position 13; individual long-tail rows are small samples.
- EMI page: 3 impressions, 0 clicks, 0% CTR, average position 7.00; no query rows were returned.
- Pakistan-only filter: Urdu BMI received 1 impression at position 64. This is not enough to support a country-level snippet change.
- Mobile-only filter: Tasbih received 16 impressions at average position 6.69; the two Tasbih query rows above were also mobile-visible.

These are Search Console impressions, not monthly search volumes or total visits. The separate OpenRush account has no connected website, SEOcrawl returned `billing_context_missing`, and Ahrefs reports a workspace unit limit of zero. No third-party monthly volume or trend figure is available from those sources. The latest finalized GSC boundary is 25 November; 26 November data remains unavailable.

### Exact preview and visible-content originality checks

The Vercel preview for the pre-integration PR head `2e5cd76aa6b40fbf3870f62f4546721f6bd64a17` was READY. Authenticated preview fetches returned HTTP 200 for EMI, Tasbih, Years-to-Days, `sitemap.xml`, `robots.txt` and `llms.txt`. The three calculator pages retained their production canonical URLs and `index, follow` directives. A fresh preview is required for the integration commit.

The AISEO checker returned the following scores on the full visible main-content text extracted from the preview:
- EMI: 89% unique, 11% matched, 1,471 words.
- Tasbih: 92% unique, 8% matched, 1,390 words.
- Years-to-Days: repeated 502 responses from the checker; no score or originality result is available.

EMI matches were mainly formula fragments and common amortization wording; Tasbih matches were mainly common dhikr translations and standard counter/storage/keyboard phrases. These checker scores are evidence for review, not a guarantee of originality or a substitute for editorial review. The Years-to-Days originality gate remains unverified.

### Release gate

Keep PR #366 OPEN and DRAFT. Do not merge or deploy Production until the updated branch has a READY exact-head preview, all required checks pass on that exact head, the Years-to-Days originality service is available or the content is independently reviewed, and remaining external account gates are explicitly resolved or accepted.

## Exact current-head live preview verification — 28 November 2026

Current PR head at verification: `7b1566ef92bca39473e0072d268ca0d57b8a1770`. The Vercel deployment lookup returned **READY** for this exact SHA:
- Deployment: `dpl_DDzngmCcS1F1G4sgbdpL4RhqEpsX`
- Preview: https://calculatesall-bsjeeaj02-malikadeelbhatti-1187.vercel.app
- Environment: Preview only. No Production deployment was triggered.

The authenticated Vercel deployment fetch returned HTTP 200 for the three priority calculator pages, homepage, `ads.txt`, `robots.txt`, `sitemap.xml`, and Privacy, About, Contact, Terms, Editorial Policy, Methodology and Advertising Disclosure pages. The three priority pages expose the expected production canonical URLs and `index, follow` robots directives. The Preview response's `X-Robots-Tag: noindex` is an expected preview-only safeguard, not the page's production robots directive. The sitemap contains 42 URLs and robots.txt includes a sitemap declaration.

A direct HTML comparison against the current Production pages found the complete `#tool-calculator` section byte-identical for Tasbih, Years-to-Days and EMI. The shared CSS asset was HTTP 200 in both environments and byte-identical at 113,013 bytes. This independently verifies that the current preview has not shifted or restyled the three calculator interfaces. The CI viewport audit also remains green on this exact PR head (112 route/viewport scenarios, zero failures, as recorded in the PR check output). The authenticated fetch verifies deployed HTML and assets; it is not represented as a manual interactive live-browser session.

The live `ads.txt` body is exactly `google.com, pub-9453966537556063, DIRECT, f08c47fec0942fa0`; it matches the public `google-adsense-account` meta publisher ID `ca-pub-9453966537556063`. The priority preview pages do not load `adsbygoogle.js`, consistent with the current disabled-ad state. A non-decrypting Production environment-variable inventory returned only `GEMINI_API_KEY`; neither `ADSENSE_SLOT` nor `ADSENSE_CONSENT_READY` is configured. No secret values were requested or read.

A fresh complete-page originality retry submitted the full unmodified preview HTML (Tasbih 33,429 characters; Years-to-Days 66,935; EMI 67,821) to the connected checker. Tasbih and Years-to-Days returned HTTP 502; EMI returned provider-busy. This remains an unavailable external verification, not a failed originality score. No originality percentage or certificate is claimed.

### Updated release interpretation

The exact current PR head has successful CI, a READY Preview, HTTP 200 live-preview fetches, matching Production/Preview calculator markup, and byte-identical CSS. The earlier authenticated-preview page-fetch blocker is resolved for read-only HTML/assets. A full interactive live-browser session and full-document originality scoring remain unverified. The remaining AdSense account review and CMP/slot configuration cannot be completed from repository evidence alone. Keep PR #366 OPEN / DRAFT / UNMERGED and do not deploy Production without the account owner's explicit release decision.
