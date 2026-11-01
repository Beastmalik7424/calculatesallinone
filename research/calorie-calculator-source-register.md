# Adult Calorie Calculator source and assumptions register

Verification date: 2026-11-02  
Feature version: 1.0  
Publication scope: English adult maintenance estimate only

## Claim and source register

| Claim or implementation | Source | Population / scope | Implementation use | Limitation | Pages/components using claim |
|---|---|---|---|---|
| Mifflin–St Jeor resting-energy equations use the published male and female coefficients | Mifflin MD, St Jeor ST et al. “A new predictive equation for resting energy expenditure in healthy individuals.” American Journal of Clinical Nutrition, 1990. [PubMed 2305711](https://pubmed.ncbi.nlm.nih.gov/2305711/) | Original study included 498 healthy adults aged 19–78 | REE formula only | Predictive equation, not an individual metabolic measurement or guarantee. The original study sample does not cover age 18 or ages above 78. | `/calorie-calculator/`, `static/calorie-calculator.js`, `calorie_calculator.py` |
| Adult energy requirements can be discussed using BMR and physical activity level concepts | FAO/WHO/UNU, *Human Energy Requirements*, 2004. [Full report](https://www.fao.org/4/y5686e/y5686e00.htm) and [adult energy requirements chapter](https://www.fao.org/4/y5686e/y5686e07.htm) | Population-level adult energy requirements and PAL framework | Context for distinguishing the report's BMR/PAL framework from this consumer calculator | Not the source of the Mifflin equation or the five consumer multipliers. No FAO certification or endorsement is claimed. | `/calorie-calculator/`, `calorie_calculator.py`, `research/calorie-calculator-source-register.md` |
| Adult guidance should exclude people under 18 and pregnant or breastfeeding users from an ordinary planner | NIDDK, [About the Body Weight Planner](https://www.niddk.nih.gov/health-information/weight-management/body-weight-planner) | NIDDK planner states adults 18+ and excludes younger people and pregnant or breastfeeding women | Conservative eligibility boundary and user-facing exclusion | The NIDDK planner is a different dynamic model. This calculator does not implement it and does not claim NIDDK approval. | `/calorie-calculator/`, `calorie_calculator.py`, `static/calorie-calculator.js` |

## Application-defined assumptions

| Identifier | Version | Multiplier | Display label | Source | Limitation |
|---|---:|---:|---|---|---|
| sedentary | 1.0 | 1.2 | Sedentary | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| light | 1.0 | 1.375 | Light activity | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| moderate | 1.0 | 1.55 | Moderate activity | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| very_active | 1.0 | 1.725 | Very active | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |
| extra_active | 1.0 | 1.9 | Extra active | Application-defined consumer preset | Approximate heuristic, not individually validated or a measured PAL. |

These activity values are configuration assumptions supplied for a consumer estimate. They are not coefficients from the Mifflin–St Jeor study and are not represented as FAO/WHO/UNU PAL categories. They have not been clinically validated for this website.

## Validation policy

- Age accepts whole years from 18 to 120. Age 18 and ages above 78 are accepted only with an explicit note that they fall outside the original Mifflin study sample.
- Weight is normalized to kilograms and checked against a broad 20–500 kg input guardrail.
- Height is normalized to centimetres and checked against a broad 100–250 cm input guardrail.
- These are broad input-error guardrails, not medical reference ranges or population eligibility criteria.
- Inputs must be finite numbers. Empty, malformed, non-finite, zero, negative and unsupported unit values are rejected.
- Weight conversion uses 1 lb = 0.45359237 kg. Height conversion uses 1 inch = 2.54 cm. Raw values are normalized once and not repeatedly converted during unit toggles.
- Intermediate calculations retain full JavaScript number precision. Formatting is applied only to displayed results.
- No statistical confidence interval is calculated.
- Pregnancy, breastfeeding, both, or a declined eligibility answer blocks the ordinary estimate.
- The output is REE multiplied by an app-defined activity assumption. It is not a measured TDEE and is not a weight-loss or weight-gain prescription.

## Review and release status

- Source links and claims checked: 2026-11-02.
- Core site build, content gates, sitemap coverage and monetization checks: **PASS** on commit `17ec997e6c32150be52a87794a145c6446c72518`, GitHub Actions run `41355354183`.
- Responsive browser, calculator interaction, keyboard, privacy-request and console checks: **PASS** on the same commit, GitHub Actions run `41355354175`. Chromium verified 320×568, 390×844 and 1366×768.
- Formula, conversion, rounding and input-validation smoke tests: **PASS** on commit `c21003832efafe4c41db69034bc6eca3ebe1e535`, GitHub Actions run `41354964910`.
- Lighthouse SEO on the GitHub-hosted build: **100/100** for home, BMI, Zakat, calorie, About, Contact, Discount and Editorial Policy pages. The Health hub also scored 100/100. The intentionally noindex `/ar/`, `/es/` and `/fr/` pages scored 66/100 only because the expected `is-crawlable` audit fails. No production Lighthouse score is claimed.
- Nu HTML Checker: **PASS**, 10 generated HTML files, zero errors and zero warnings. Sitemap and internal-link checks: **PASS**, 39 unique sitemap URLs.
- Existing calculator regressions: **PASS** for Fraction, Compound Interest, Date, Percentage, BMI, EMI and Tasbih browser checks. Responsive overflow checks passed at 320, 360, 390 and 1366 px.
- Vercel preview: deployment `dpl_BogmEDF2PAowNmp52rj4ZGgG14f2` is READY for older commit `5edbce344472202fba62e3e4d935f60a9f881c63`. The final branch includes the later display-rounding correction and is not represented by that preview.
- Latest preview verification: **NOT VERIFIED**. Vercel returned HTTP 402 because the Hobby team's deployment API quota exceeded 100 deployments for the day, with retry after 24 hours. The Vercel CLI is not installed or authenticated in this execution environment. No quota bypass or unrelated project was used.
- Production verification: **NOT PERFORMED**. Production domain and `main` branch remain unchanged.
- Qualified clinical review: not performed.
- Medical certification or endorsement: none claimed.
- English page: implemented and tested on the feature branch; not production-published.
- Other locales: planned; no translated pages are published by this feature.
- GEO/AI visibility: not measured. No ranking, indexing or AI-citation outcome is claimed.

## Query-to-page map

Search-volume status: not measured. The phrases below are user-intent seeds, not keyword-volume or ranking claims. No permutation pages are created.

| Query seed / primary intent | Related questions served | Destination | Evidence needed | Existing content coverage | Publication status |
|---|---|---|---|---|---|
| calorie calculator; daily calorie calculator; maintenance calorie calculator | How many calories do I need daily? What is maintenance energy? | `/calorie-calculator/` | Mifflin–St Jeor original equation, stated activity assumptions, independently checked examples | Existing BMI page does not estimate maintenance calories; this page adds a distinct calculation intent | English page planned for release; not production-published |
| TDEE calculator; daily calorie needs; how many calories do I need | What does the activity factor mean? Are exercise calories included? | `/calorie-calculator/` | Explain REE × app-defined factor; distinguish this estimate from measured TEE and from FAO/WHO/UNU PAL calculations | Existing health hub had BMI-focused content; new page adds the missing maintenance estimate | English page planned for release; not production-published |
| BMR calculator; resting energy calculator; Mifflin St Jeor calculator | Is REE the same as BMR or RMR? Is BMR a safe minimum? | `/calorie-calculator/` | Original 1990 paper, accurate terminology and explicit limitations | Existing BMI page does not explain the Mifflin equation or REE | English page planned for release; not production-published |
| calorie calculator kg cm; calorie calculator pounds feet | How are pounds and feet/inches converted? Why can rounding change results? | `/calorie-calculator/` | Exact unit conversion constants, metric/imperial equivalence fixtures, rounding tests | No equivalent existing unit-aware calorie estimator | English page planned for release; not production-published |
| why calorie calculators differ; activity level calculator explanation | Why does another calculator show a different estimate? What if activity is uncertain? | `/calorie-calculator/` | Compare equation, population, activity assumptions and rounding without unsupported accuracy claims | Existing general methodology page does not cover calorie-estimate differences in detail | English FAQ planned for release; not production-published |
| is this calorie calculator free; does it need sign-up; are measurements stored | Does reset clear entries? Are values sent to an API? | `/calorie-calculator/` | Verify browser code, network requests, URL and storage behavior; check existing privacy policy and third-party scripts | General privacy page exists; page-specific FAQ documents this feature's behavior and limits | English FAQ planned for release; not production-published |
| can teenagers use a calorie calculator; pregnancy calorie calculator; breastfeeding calories | Who is excluded and why? | `/calorie-calculator/` | Adult eligibility boundary, NIDDK disclaimer context, no ordinary result for excluded selections | Existing BMI page is not a substitute for this calculator's eligibility rules | English safety explanation planned for release; not production-published |
| daily kitni calories chahiye; meri maintenance calories kitni hain; calories kaise calculate karein; روزانہ کتنی کیلوریز چاہئیں; کیلوری کیلکولیٹر | Urdu explanation of REE, activity assumptions, safety and result interpretation | No localized destination currently published | Competent Urdu translation review of every scientific, safety, form, result, navigation and metadata string | Existing Urdu journey does not yet include this calculator | Planned; unpublished until competent language review |

This map deliberately consolidates related intents on one useful calculator page. It does not imply measured demand, search volume, indexing, rankings, AI citations or language support.
