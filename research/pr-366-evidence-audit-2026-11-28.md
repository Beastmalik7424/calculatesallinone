# PR #366 evidence audit — 28 November 2026

## Scope and guardrails

Repository: `Beastmalik7424/calculatesallinone`  
PR: [#366 — Improve SEO regression coverage for Tasbih, Years to Days and EMI](https://github.com/Beastmalik7424/calculatesallinone/pull/366)  
Audited source head: `9b5d764774d65c2cc5321c6cf220d6f9ec2992b0`  
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

## Originality spot-check and remaining evidence gates

The independent AISEO full-document plagiarism API was called with the complete, unmodified HTML of each of the three deployed page documents:
- Tasbih Counter: 33,420 characters — HTTP 502 Bad Gateway.
- Years-to-Days: 67,372 characters — HTTP 502 Bad Gateway.
- EMI Calculator: 67,444 characters — provider returned “busy” before analysis.

Five exact-phrase web searches were also attempted against representative sentences from the pages. No direct copied-page match was returned for the sampled wording, but search-engine phrase checks cannot certify originality or replace a full-document plagiarism report. **No originality percentage is claimed.**

- Exact code-head GitHub Actions: **7 workflows were associated with `9b5d764...`; the latest documentation-head run must be polled to completion before it can be reported as final.**
- Build, generated-page smoke, Lighthouse, and headless Playwright checks: **in progress on `89ea871...` at the last poll; steps 1–31 passed, step 32 was running, step 33 pending.**
- CSS stylesheet files changed: **NONE**. The standalone EMI HTML diff changes metadata, structured data and content only; no inline style or CSS rules changed.
- Calculator first-screen and EMI viewport checks: **PASS in the existing GitHub Actions browser audits**.
- EMI engine regression: **26 deterministic checks plus 2,000 seeded schedule-reconciliation scenarios**.
- Years-to-Days regression: **1,000 deterministic browser property simulations per viewport**.
- Query Calculator: browser regression cases include plain digits, complete natural-language questions with digits, grouped thousands, unit clarification and multiple locales.
- GSC: **verified only for 22–24 November 2026**; 26 November export and keyword trend data remain unavailable.
- Competitor comparison: **five substantive comparison pages reviewed per topic**. This is a content/feature benchmark, not proof of exact Google top-five ranking positions.
- Independent originality score: **NOT VERIFIED** because the provider failed before returning results.
- Vercel preview: **READY for documentation SHA `89ea871...`**, with HTTP 200 verified on the eight listed routes.
- Interactive browser verification of the deployed preview: **NOT VERIFIED**. GitHub Actions Playwright checks against the generated build remain the reliable available alternative.
- AdSense approval and account-side consent: **NOT VERIFIED**; only Google can approve the account and automated CI cannot inspect account settings.

Keep PR #366 **OPEN / DRAFT / UNMERGED** until the current documentation-head workflow completes and the independent originality/live-preview browser gates are resolved. Do not claim first-page or top-five rankings as guaranteed. Product gaps requiring new controls (Tasbih tracking/history and EMI fees/down-payment/flat-rate/floating-rate features) are documented but deliberately not implemented because the fixed zero-layout-change constraint forbids those UI changes.
