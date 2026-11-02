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

Evidence date: 2026-11-02. Feature branch head at verification: `8d55ff38774072a42a092ff2c88db049fc55c3f4`.

- PR #146 is open, draft and unmerged at the time of this evidence capture.
- GitHub Actions **Build and smoke test**, run [41384307763](https://github.com/Beastmalik7424/calculatesallinone/actions/runs/41384307763): **PASS**. Dependency audit reported zero vulnerabilities. Lighthouse SEO was 100/100 on home, BMI, Zakat and calorie pages. The additional scoped-page Lighthouse audit passed; only the expected crawlability finding appeared on intentionally noindex Arabic, Spanish and French pages.
- GitHub Actions **Site build and monetization checks**, run [41384307818](https://github.com/Beastmalik7424/calculatesallinone/actions/runs/41384307818): **PASS**. Content gates, 39-URL sitemap coverage, canonical/internal-link checks, JSON-LD, AdSense gating and existing calculator smoke checks passed.
- Nu HTML Checker: **PASS**, 10 generated HTML files, zero errors and zero warnings. The primary validator returned rate-limit/service errors during this run, so the test used its independent online fallback. The bounded fallback regression test also passed.
- GitHub Actions **First-screen calculator browser audit**, run [41384307764](https://github.com/Beastmalik7424/calculatesallinone/actions/runs/41384307764): **PASS**. Chromium checks passed at 320×568, 390×844 and 1366×768 for the calorie page. The calculate control remained inside the viewport and no horizontal overflow or browser errors were reported. Existing calculator viewport and interaction checks also passed.
- Calorie browser acceptance checks verified the Mifflin–St Jeor example, both coefficient outputs, activity-factor output, metric/imperial equivalence, age and pregnancy/breastfeeding exclusions, keyboard operation, reset behavior, and absence of non-GET requests or measurement values in URLs, request payloads, cookies, localStorage or sessionStorage.
- Vercel preview deployment `dpl_9VeAhJ9gj2gPBwewqC1Rsvqkzkwu` is **READY** for this exact feature-branch head. Authenticated Vercel fetch returned HTTP 200 for `/calorie-calculator/`, `/health/` and `/sitemap.xml`. The preview has Vercel's expected `X-Robots-Tag: noindex`; its page canonical points to the production host.
- Sitemap comparison: current production contains 38 URLs; the preview contains 39. No existing production sitemap URL was removed or changed. The only addition is `/calorie-calculator/`.
- Production publication has not yet occurred at this evidence capture.
- Qualified clinical review: not performed. Medical certification or endorsement: none claimed.
- Other locales: the calculator page remains English-only. Translated carousel labels do not represent translated calculator content.
- GEO/AI citation visibility and post-publication Google indexing have not yet been measured.

## Market demand and competitor evidence

### Search-demand measurement

Keyword Tool Guest was queried on 2026-11-02 using Google, Global / Worldwide, English. The following are the provider's cached monthly search-volume estimates for the selected terms. They are third-party estimates, not CalculateAll GSC impressions, guaranteed traffic, or independently measured visits. Only cached rows returned numeric metrics. The reported competition field is not an organic SEO difficulty score; top-of-page bid is an advertising metric.

| Keyword | Reported global monthly volume | Reported trend | Reported competition field | Google top-of-page bid range |
|---|---:|---:|---:|---:|
| calorie calculator | 1,830,000 | +49% | 0.05 | $0.08–$1.23 |
| maintenance calorie calculator | 201,000 | +22% | 0.16 | $0.01–$0.32 |
| TDEE calculator | 1,500,000 | 0% | 0.17 | $0.04–$0.77 |
| BMR calculator | 450,000 | −18% | 0.07 | $0.01–$0.36 |
| calorie deficit calculator | 550,000 | 0% | 0.30 | $0.06–$1.31 |
| body fat calculator | 201,000 | +22% | 0.03 | $0.18–$1.24 |
| GPA calculator | 1,220,000 | −45% | 0.00 | $0.17–$3.88 |
| mortgage calculator | 4,090,000 | −18% | 0.35 | $0.17–$2.05 |

The guest tool returned autocomplete suggestions but no cached numeric volume for `years to days calculator`, `profit and loss calculator`, `standard deviation calculator`, `Pakistan electricity bill calculator`, `matric marks calculator` and `FBR salary tax calculator`. No volume is claimed for those terms.

### First-party Google Search Console evidence

For `https://calculateallinone.vercel.app/`, the 90-day window 2026-08-02 to 2026-10-30 reported 28 clicks, 396 impressions, 7.07% CTR and average position 34.3. Page-level examples:

| Production page | Clicks | Impressions | CTR | Average position |
|---|---:|---:|---:|---:|
| `/years-to-days-calculator/` | 0 | 220 | 0% | 44.7 |
| `/profit-loss-calculator/` | 1 | 54 | 1.85% | 17.1 |
| `/tasbih-counter/` | 1 | 40 | 2.50% | 13.3 |
| `/standard-calculator/` | 0 | 40 | 0% | 16.6 |

Search Console omits some rare queries for privacy, so query rows do not sum to the site's page-level totals. The calorie page is not yet on production and therefore has no first-party Search Console demand data.

### Competitor coverage and strategy

- [Calculator.net's homepage](https://www.calculator.net/) reports around 200 calculators across financial, fitness/health, math and other categories. Its [About Us page](https://www.calculator.net/about-us.html) says its calculators are developed in-house, more than 90% use established textbook formulas, financial results are reviewed by financial advisers, and health results are reviewed by local doctors. Its [Calorie Calculator](https://www.calculator.net/calorie-calculator.html) offers Mifflin–St Jeor, Revised Harris–Benedict and Katch–McArdle formula options, activity factors, a food-energy converter and links to BMI, body-fat and ideal-weight tools.
- [Omni's live homepage](https://www.omnicalculator.com/) lists 3,938 calculators in 14 categories. Its [Omni by the Numbers page](https://www.omnicalculator.com/omni-by-the-numbers) self-reports 8 million monthly unique users, up to 20 million visits and an average of one new calculator per day. Its [Calorie Calculator](https://www.omnicalculator.com/health/calorie) and [TDEE Calculator](https://www.omnicalculator.com/health/tdee) combine formula explanations, activity assumptions, worked examples and related BMR, calorie-deficit, weight-gain and meal-calculator journeys.

### Opportunity assessment

- The new adult maintenance calculator addresses a measured global keyword cluster, especially `maintenance calorie calculator` and `TDEE calculator`. The feature deliberately competes on transparent assumptions, primary-source citation, adult eligibility boundaries, browser-local calculation and no weight-loss/gain prescription, rather than matching the competitors' broader diet-planning scope.
- Body-fat calculation has a reported 201,000 global monthly searches, but it is health/YMYL content. Defer it until the formula, measurement instructions and qualified review can be independently validated.
- GPA has a reported 1,220,000 global monthly searches, but the provider trend is −45%. Regional variants appeared as autocomplete suggestions, but no numeric volume was returned for them. Do not treat the broad global term as proof of demand for a Pakistan-specific GPA tool.
- Mortgage has a reported 4,090,000 global monthly searches, but it is a broad, mature category already covered extensively by competitors. It is not the next low-competition target.
- Pakistan electricity-bill and salary-tax ideas surfaced in autocomplete, but numeric volume was unavailable. These topics also require current official tariff or tax-year data and frequent maintenance. Do not implement them without a primary-source update process and stronger demand evidence.
- The clearest first-party content opportunity remains the already indexed years-to-days page: 220 impressions and average position 44.7 in the measured window. Keep its URL stable and use the query/page evidence for a focused content and internal-link review after the new release. The next project priority is the GSC indexing backlog for the Health, Money and Math hubs, not another generic calculator.

## Query-to-page map

Search-volume status: partial cached global Google keyword metrics are recorded above. Terms without a returned cached metric remain unquantified. These figures are not GSC data, organic difficulty scores, ranking claims or traffic guarantees. No permutation pages are created.

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
