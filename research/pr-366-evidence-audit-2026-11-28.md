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

## Public competitor scan

Searches on 28 November 2026 surfaced the following public pages. This is a content/feature comparison sample from web search, **not proof of exact Google country-specific SERP positions or a verified top-five ranking order**.

### Tasbih / Tasbeeh counter

Pages reviewed:
- [Ihsabha digital Tasbih counter](https://ihsabha.com/islamic/digital-tasbih-counter)
- [Nakhtu digital Tasbih counter](https://nakhtu.com/en/tools/tasbih)
- [ToolNova online Tasbeeh counter](https://www.toolnova.org/islamic-tools/tasbeeh-counter)
- [Hasibatak digital Tasbih counter](https://www.hasibatak.com/en/tasbih-counter/)
- [Sibha online Tasbih counter](https://sibha.app/)
- [Sunnah Tools Tasbih counter](https://sunnah.tools/tools/tasbih-counter/)

Common competitor capabilities include 33/99/100 presets, custom targets, Undo/Reset, local persistence, and keyboard counting. Differentiating features found across the sample include vibration, offline/PWA operation, daily totals, streaks, history/backup, multiple dhikr libraries, and linked religious sources.

PR #366's page explains the digital-vs-physical distinction, custom phrase/target, deliberate tap counting, keyboard controls, Undo/confirmed Reset, device-local persistence and storage limitations, and explicitly avoids presenting targets as religious rulings. This is a useful scope and trust distinction. Feature gaps versus the sample remain offline/PWA support, vibration, history/backup, streaks and cross-device continuity. These are separate product decisions and are not silently added to this content PR.

### Years-to-Days calculator

Pages reviewed:
- [Calculator Junction Years to Days](https://calculatorjunction.com/time-unit-converter/years-to-days)
- [Calculorium Years to Days](https://calculorium.com/calculator/years-to-days-calculator/)
- [DQYDJ Years to Days](https://dqydj.com/years-to-days-calculator/)
- [UnitFlip Years to Days](https://unitflip.org/time/years-to-days)
- [Qvert Year to Day](https://qvert.ai/time/year-to-day/)

The sample commonly uses one primary convention (365, 365.25 or 365.2425 days), with some reverse conversion and reference tables. PR #366 differentiates by clearly separating the fixed 365-day convention, Julian 365.25-day average, mean Gregorian 365.2425-day average, and exact date-based calendar counting. It also explains the Gregorian 400-year rule and supplies worked examples and reverse-conversion references.

The remaining competitive opportunity is a more interactive conversion experience with selectable precision and broader unit/date workflows. No unsupported claim is made that every competitor uses the same year definition.

### EMI calculator

Pages reviewed:
- [Educativz Loan EMI Calculator](https://www.educativz.com/tools/loan-emi-calculator/)
- [LoanCalculators.pk](https://loancalculators.pk/)
- [Software Craft Loan EMI Calculator](https://software-craft.com/free-tools/loan-emi-calculator/)
- [Investify Loan Calculator](https://www.investify.pk/tools/loan-calculator)
- [HisabCenter EMI Calculator](https://www.hisabcenter.pk/tools/emi-loan)
- [EMICalculator.pk](https://emicalculator.pk/)

The sample frequently provides repayment schedules, principal/markup splits, Pakistan-specific PKR context and fee/rate caveats. Some competitors additionally publish bank-specific pricing, KIBOR-linked presets, loan-product comparisons, or richer schedule/prepayment models. PR #366's page provides formula/method explanation, reducing-balance versus flat-markup context, worked examples, prepayment scenarios, affordability, comparisons and explicit estimate limitations.

Remaining gaps include verified bank-specific rate feeds, full APR/fee modelling, variable-rate reset modelling, and solving for additional unknowns such as principal or tenure. These require separate data/product work; this PR does not claim those features exist.

## AdSense and originality evidence

Official Google guidance says AdSense-ready pages should provide unique, relevant content and a good user experience, and that sites must add their own original value rather than merely reuse external material:
- [Google AdSense: Make sure your site's pages are ready](https://support.google.com/adsense/answer/7299563)
- [Google Search Central: Helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

The exact-head CI build and monetization checks passed. This demonstrates automated project checks only. It does **not** establish AdSense approval, account-side consent configuration, ad serving, revenue, or a Google ranking.

Independent plagiarism verification remains unresolved. The AISEO plagiarism-check request previously returned HTTP 502; a subsequent retry failed before returning an originality score. Exact-phrase web spot checks are not a substitute for a full-document plagiarism scan. No originality percentage or “100% unique” claim is made.

## Deployment and live-browser boundary

Vercel's deployment status check for `9b5d764774d65c2cc5321c6cf220d6f9ec2992b0` returned no deployment. The Vercel Git status for that SHA was failure with the deployment-rate-limit target URL, and the previous create-deployment attempt returned HTTP 402 with a 24-hour limit message. Do not infer that the quota has reset.

A separate HYPD browser SEO audit request was not run because the connected plan denied access to that feature. The passing CI browser audits are valid CI evidence but must not be represented as interactive verification of the deployed Vercel preview.

## Gate decision

- Exact-head GitHub Actions: **PASS (7/7)**.
- Build, generated-page smoke, headless browser and monetization checks: **PASS in GitHub Actions**.
- CSS stylesheet files changed: **NONE in the PR changed-file list**.
- Calculator first-screen and EMI viewport checks: **PASS in CI**.
- GSC: **verified only for 22–24 November 2026**; 26 November and trend data unavailable.
- Competitor content scan: **completed as a surfaced public-page feature comparison**; exact Google top-five rank order is not verified.
- Independent originality score: **NOT VERIFIED**.
- Vercel preview for audited SHA: **NOT DEPLOYED / NOT FOUND**.
- Interactive browser verification of that preview: **NOT VERIFIED**.

Keep PR #366 open and draft. Do not merge or deploy production until the remaining evidence gates are closed. Once Vercel quota permits a preview deployment, verify that exact deployed SHA in a real browser at mobile and desktop widths before considering merge.
