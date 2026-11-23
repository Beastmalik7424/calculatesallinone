# Health Hub Content Audit and Update Report

**Review date:** 2026-11-23  
**Repository:** `Beastmalik7424/calculatesallinone`  
**Branch:** `health-audit-v6`  
**Verified implementation commit:** `83b292ea88336dedd5dfd99f11b343fb2de84049`  
**Preview deployment:** READY  
**Production status at report time:** Not merged or published

## Executive result

The Health hub body and eight visible FAQ entries have been revised and source-checked. The work is limited to Health hub content, its FAQ data, content regression assertions, and this report.

No CSS, layout template, navigation, calculator component, calculator JavaScript, formula, route, canonical, sitemap, or SEO metadata was changed. The existing calculator placement and page structure are preserved by the unchanged rendering code. The source diff confirms that changes in `build.py` are confined to `HUB_CONTENT["health"]`, and changes in `content_v13.py` are confined to `HUB_EXTRA["health"]`.

## Material issues found and corrected

1. **FAQ scope:** The live FAQ data was stored separately from the Health body. The Health FAQ source was updated in its actual data location rather than adding a second FAQ block to the body.
2. **BMI label granularity:** WHO's reference table includes obesity classes I, II and III. The current English BMI calculator displays four broad labels and does not display those obesity classes separately. The article and FAQ now disclose that distinction.
3. **BMI precision:** The calculator chooses a category from the unrounded BMI and rounds only the displayed value. The article explains this and includes independently checked metric and imperial examples.
4. **Imperial conversion:** The customary 703 multiplier is described as a rounded conversion factor, not an exact unit conversion.
5. **Child and teen interpretation:** The page now links to CDC guidance that uses sex-specific BMI-for-age percentiles for ages 2 through 19, and distinguishes that from CDC adult BMI guidance for ages 20 and older.
6. **Calorie activity assumptions:** The standard adult Mifflin-St Jeor maintenance path uses application-defined consumer activity multipliers. Pregnancy and breastfeeding use a separate National Academies DRI 2023 path with its own activity categories. The article no longer conflates the two.
7. **Pregnancy and breastfeeding limitations:** The page explains that the calculator displays separate estimates when both statuses are selected and does not produce a combined daily target. It also discloses the US/Canadian reference-population scope and the lack of validation for Pakistan, every population, or chronic medical conditions.
8. **Repeated disclaimer:** A duplicated reference-estimate sentence was removed and a regression assertion was added.
9. **Medical review disclosure:** The page explicitly states that the guide has not been medically reviewed. No reviewer identity or clinical approval was invented.

## Content delivered

- Approximately 1,900 words across the Health body and FAQ data.
- Eight visible FAQ questions, each asserted to render exactly once.
- WHO adult BMI categories and Asian BMI action points, with their different purposes clearly separated.
- Metric and imperial worked BMI examples.
- BMI screening limitations and child/teen interpretation caveats.
- Mifflin-St Jeor method, original study population and age-range caveat.
- Worked adult calorie estimates and a clear explanation of the app-defined activity assumptions.
- Separate pregnancy and breastfeeding DRI 2023 explanation, including population and combined-target limitations.
- Links to WHO, CDC, the original Mifflin paper, and the National Academies source.

## Files changed

| File | Limited purpose |
|---|---|
| `content_v13.py` | Health hub body content only |
| `build.py` | Health hub intro and eight FAQ entries only |
| `tests/site-output-smoke.py` | Health-specific content, source-link, FAQ and accuracy assertions |
| `review/health_audit_v6.md` | This audit report |

No calculator formula or calculator implementation file was changed.

## Verification evidence

All GitHub Actions checks associated with implementation commit `83b292ea88336dedd5dfd99f11b343fb2de84049` completed successfully:

- Repository build and smoke tests: PASS.
- Clean build and regression suite: PASS.
- Site build and monetization checks: PASS.
- Workflow permission/security contract: PASS.
- Independent query-calculator verification: PASS.
- Zakat QA and focused verification: PASS.
- First-screen calculator browser audit: PASS.
- General Lighthouse SEO audit: PASS.
- Lighthouse audit for ten scoped pages: PASS.
- Headless browser console checks for ten scoped pages: PASS.
- Safe monetization configuration: PASS.
- Sitemap XML, generated-page smoke checks, sitemap coverage and internal links: PASS.
- HTML validation for the homepage and ten scoped pages: PASS.
- Explicit HTTP 301 redirect configuration check: PASS.

Additional regression evidence:

- **14,000** deterministic calculator simulations passed with seed `20261114`.
- **39,703** independently counted unit/property assertions passed.
- **3** generated-page integration contracts passed.
- **112** first-screen browser scenarios passed across 28 English/Urdu calculator routes and four viewport sizes. The audit recorded zero failures and zero page errors, and saved 112 screenshots.
- The calorie test suite includes 1,000 Mifflin-St Jeor simulations and 1,000 DRI 2023 life-stage simulations, checked against independently transcribed equations.
- Generated output checks covered 47 pages and 260 JSON-LD blocks. Sitemap, canonical, internal-link and structured-data checks passed.

The Vercel preview deployment for the verified implementation commit reached **READY**. Direct external inspection of the protected preview returned a Vercel login requirement, so the browser-visible preview could not be opened anonymously. The local generated-output, browser, HTML, SEO and regression workflows passed.

## Originality and review limitations

The complete Health body and FAQ text were submitted twice to the AISEO plagiarism checker. Both attempts failed with **502 Bad Gateway** from the checker service. Targeted exact-phrase web searches did not surface exact matches for the distinctive phrases checked, but those searches are not a substitute for a successful comprehensive plagiarism scan. Therefore, no numerical originality score or plagiarism-clearance claim is made.

No qualified medical professional reviewed or approved this guide. The visible disclosure remains in place. The page explains calculator methods and limitations and must not be presented as individualized medical advice.

## Final verdict

**Technical and content regression gates: PASS on implementation commit `83b292e`.**  
**Layout/formula scope: PRESERVED.**  
**Originality certification: NOT VERIFIED because the external checker returned 502.**  
**Medical review: NOT COMPLETED.**  
**Production publication: NOT performed at the time this report was written.**

The remaining publication decision should preserve the medical-review disclosure and must not imply a plagiarism score or clinical sign-off that was not obtained.
