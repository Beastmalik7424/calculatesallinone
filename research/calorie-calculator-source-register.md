# Adult Calorie Calculator source and assumptions register

Original source audit: 2026-11-02  
Latest research update: 2026-11-26  
Production feature version: 1.0; proposed branch version: 1.1  
Publication scope: English adult maintenance estimate only

## 26 November 2026 implementation and evidence update

**Release state:** The production calculator remains Mifflin–St Jeor only. PR #354 is a draft branch under GitHub Actions verification; its proposed three-formula upgrade is not merged or deployed. Do not describe the new options as live until the merge and production URL are verified.

**Proposed formula scope:**
- Mifflin–St Jeor remains the default.
- Revised Harris–Benedict (Roza and Shizgal, 1984) is added as an alternative using its published male/female coefficients.
- Katch–McArdle/Cunningham (370 + 21.6 × fat-free mass in kg) is added as an alternative. The user must supply a body-fat percentage; the calculator derives fat-free mass. It does not measure or estimate body fat. Age remains an adult-eligibility input; height is not requested because this equation does not use it.
- The existing National Academies DRI 2023 pregnancy/breastfeeding path remains separate and unchanged. No calorie deficit, surplus, weight-loss/gain prescription or macro target is added.
- Katch body-fat input guardrail is 3–70%. This is an input-error guardrail, not a clinical reference range. Users are told not to guess the value.

**Additional primary sources:**
- Revised Harris–Benedict: Roza and Shizgal (1984), PubMed 6741850. The paper evaluated 337 subjects, reported about 14% precision in normally nourished individuals and cautioned that the equation was unreliable in malnourished patients.
- Fat-free-mass equation: Cunningham (1991), PubMed 1957828. The proposed equation is REE = 370 + 21.6 × fat-free mass. The page labels this commonly used consumer-calculator method Katch–McArdle/Cunningham and explicitly discloses the body-fat measurement dependency.

**First-party GSC evidence, 4 October–24 November 2026:**
- 367 visible query rows were returned for the property. Search Console can omit anonymized queries, so query rows do not equal page-level totals.
- 313 visible query variants contained year/day terms and accounted for 942 impressions with zero clicks. Most of these queries were positioned well beyond page one. The Years-to-Days page was subsequently updated with a 37-row quick-reference table and answer-first metadata on 26 November; the GSC date window ends before that update and cannot measure its effect yet.
- The exact query "tasbih calculator" rose from 18 impressions in 28 October–10 November to 46 impressions in 11–24 November. Average position in the latter period was 7.35 with zero clicks. This is a GSC trend, not a Google Trends measurement.
- The site index audit found nine discovered-but-not-indexed URLs: percentage calculator, percentage difference calculator, ratio calculator, calorie calculator, compound interest calculator, date calculator, Math hub, Money hub and Worship hub. Five were rechecked; four inspections timed out. The sitemap itself was healthy and was resubmitted on 26 November. Submission does not guarantee crawling or indexing.

**Competitor benchmark, named comparison set:**
- [Calculator.net BMR calculator](https://www.calculator.net/bmr-calculator.html) explicitly offers Mifflin–St Jeor, Revised Harris–Benedict and Katch–McArdle. The proposed branch closes this specific formula-choice gap, but not Calculator.net's wider library or related tools.
- [Omni Calculator](https://www.omnicalculator.com/) lists 3,938 calculators across 14 categories. Its [maintenance calorie page](https://www.omnicalculator.com/health/maintenance-calorie) explains Mifflin–St Jeor and activity factors, while its articles provide formula context and examples. Matching its breadth is not a realistic first release; prioritize query-backed depth.
- [CalculatorSoup](https://www.calculatorsoup.com/calculators/math/adding-fractions-calculator.php) demonstrates formula transparency and visible step-by-step work; this is a useful quality benchmark for calculators where intermediate steps are meaningful.
- [GigaCalculator](https://www.gigacalculator.com/about.php) reports 250+ calculators and 150+ converters. Its [editorial policy](https://www.gigacalculator.com/editorial-policies.php) describes primary-source use, formula verification, simulation QA, contextual input help and supporting documentation.
- [Math.tools](https://math.tools/about) offers calculators, converters, reference tables and number facts, with a Numbers API and MCP server; it is a narrower overlap for general-purpose calculators.
- CalculateAll's differentiators remain Pakistan-relevant Zakat methods, Tasbih counting, local currency context and selected Urdu pages. The main remaining competitive gaps are breadth, independent brand corroboration and external citations, not crawler access.

**Test plan for PR #354 (pending results):** fixed reference cases for all three formulas, 2,000 additional deterministic property simulations (17,000 total), browser interaction and first-screen checks for default and Katch states, body-fat input privacy checks, source-link validation, and regression checks that retain the DRI life-stage path. Do not record PASS until the current PR head's checks complete successfully.

## Claim and source register

| Claim or implementation | Source | Population / scope | Implementation use | Limitation | Pages/components using claim |
|---|---|---|---|---|
| Mifflin–St Jeor resting-energy equations use the published male and female coefficients | Mifflin MD, St Jeor ST et al. “A new predictive equation for resting energy expenditure in healthy individuals.” American Journal of Clinical Nutrition, 1990. [PubMed 2305711](https://pubmed.ncbi.nlm.nih.gov/2305711/) | Original study included 498 healthy adults aged 19–78 | REE formula only | Predictive equation, not an individual metabolic measurement or guarantee. The original study sample does not cover age 18 or ages above 78. | `/calorie-calculator/`, `static/calorie-calculator.js`, `calorie_calculator.py` |
| Revised Harris–Benedict resting-energy equations use the published 1984 coefficients | Roza AM, Shizgal HM. Revised Harris–Benedict equation (1984). [PubMed 6741850](https://pubmed.ncbi.nlm.nih.gov/6741850/) | 337 subjects in the revision study | Alternative REE formula for adult maintenance estimate | The authors reported about 14% precision in normally nourished individuals and cautioned that the equation was unreliable in malnourished patients. It is a population prediction, not a measured value. | /calorie-calculator/, static/calorie-calculator.js, calorie_calculator.py |
| Fat-free-mass equation REE = 370 + 21.6 × FFM | Cunningham JJ (1991). [PubMed 1957828](https://pubmed.ncbi.nlm.nih.gov/1957828/) | Population equation based on fat-free mass | Alternative formula labelled Katch–McArdle/Cunningham in the calculator | Requires a user-supplied body-fat percentage to derive FFM. The calculator does not measure body fat; measurement error changes the result. | /calorie-calculator/, static/calorie-calculator.js, calorie_calculator.py |
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

These activity values are configuration assumptions supplied for a consumer estimate. They are not coefficients from Mifflin–St Jeor, Revised Harris–Benedict or Katch–McArdle/Cunningham, and are not represented as FAO/WHO/UNU PAL categories. They have not been clinically validated for this website.

## Validation policy

- Age accepts whole years from 18 to 120. The Mifflin option flags age 18 and ages above 78 because they fall outside its original 19–78 study sample. This note is specific to Mifflin and does not describe the study populations for Revised Harris–Benedict or Katch–McArdle/Cunningham.
- Weight is normalized to kilograms and checked against a broad 20–500 kg input guardrail.
- Height is normalized to centimetres and checked against a broad 100–250 cm input guardrail for Mifflin–St Jeor and Revised Harris–Benedict. It is not requested for Katch–McArdle/Cunningham because that equation does not use height.
- Katch–McArdle/Cunningham requires a user-supplied body-fat percentage between 3% and 70% as a broad input guardrail, not a clinical reference range. Fat-free mass is derived from weight and that percentage.
- These are broad input-error guardrails, not medical reference ranges or population eligibility criteria.
- Inputs must be finite numbers. Empty, malformed, non-finite, zero, negative and unsupported unit values are rejected.
- Weight conversion uses 1 lb = 0.45359237 kg. Height conversion uses 1 inch = 2.54 cm. Raw values are normalized once and not repeatedly converted during unit toggles.
- Intermediate calculations retain full JavaScript number precision. Formatting is applied only to displayed results.
- No statistical confidence interval is calculated.
- For female-coefficient Mifflin/Harris selections, a pregnancy and breastfeeding status is required. Pregnancy/breastfeeding selections switch to the separate National Academies DRI 2023 path; a declined status produces no estimate. Katch is not available for pregnancy or breastfeeding.
- The output is REE multiplied by an app-defined activity assumption. It is not a measured TDEE and is not a weight-loss or weight-gain prescription.

## Historical review and release status (2 November 2026)

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

### Historical search-demand measurement (2 November 2026)

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

### First-party Google Search Console evidence (2 November 2026 snapshot)

For `https://calculateallinone.vercel.app/`, the 90-day window 2026-08-02 to 2026-10-30 reported 28 clicks, 396 impressions, 7.07% CTR and average position 34.3. Page-level examples:

| Production page | Clicks | Impressions | CTR | Average position |
|---|---:|---:|---:|---:|
| `/years-to-days-calculator/` | 0 | 220 | 0% | 44.7 |
| `/profit-loss-calculator/` | 1 | 54 | 1.85% | 17.1 |
| `/tasbih-counter/` | 1 | 40 | 2.50% | 13.3 |
| `/standard-calculator/` | 0 | 40 | 0% | 16.6 |

Search Console omits some rare queries for privacy, so query rows do not sum to the site's page-level totals. At the 2 November 2026 snapshot the calorie page was not yet on production. It is live by 26 November; the updated GSC evidence above covers the full site and the current production page.

### Competitor coverage and strategy

- [Calculator.net's homepage](https://www.calculator.net/) reports around 200 calculators across financial, fitness/health, math and other categories. Its [About Us page](https://www.calculator.net/about-us.html) says its calculators are developed in-house, more than 90% use established textbook formulas, financial results are reviewed by financial advisers, and health results are reviewed by local doctors. Its [Calorie Calculator](https://www.calculator.net/calorie-calculator.html) offers Mifflin–St Jeor, Revised Harris–Benedict and Katch–McArdle formula options, activity factors, a food-energy converter and links to BMI, body-fat and ideal-weight tools.
- [Omni's live homepage](https://www.omnicalculator.com/) lists 3,938 calculators in 14 categories. Its [Omni by the Numbers page](https://www.omnicalculator.com/omni-by-the-numbers) self-reports 8 million monthly unique users, up to 20 million visits and an average of one new calculator per day. Its [Calorie Calculator](https://www.omnicalculator.com/health/calorie) and [TDEE Calculator](https://www.omnicalculator.com/health/tdee) combine formula explanations, activity assumptions, worked examples and related BMR, calorie-deficit, weight-gain and meal-calculator journeys.

### Opportunity assessment

- The new adult maintenance calculator addresses a measured global keyword cluster, especially `maintenance calorie calculator` and `TDEE calculator`. The feature deliberately competes on transparent assumptions, primary-source citation, adult eligibility boundaries, browser-local calculation and no weight-loss/gain prescription, rather than matching the competitors' broader diet-planning scope.
- A standalone body-fat calculator remains deferred because it would require validated measurement guidance and qualified review. The proposed Katch option only accepts a body-fat percentage supplied by the user to derive fat-free mass; it does not estimate body fat or prescribe a target.
- GPA has a reported 1,220,000 global monthly searches, but the provider trend is −45%. Regional variants appeared as autocomplete suggestions, but no numeric volume was returned for them. Do not treat the broad global term as proof of demand for a Pakistan-specific GPA tool.
- Mortgage has a reported 4,090,000 global monthly searches, but it is a broad, mature category already covered extensively by competitors. It is not the next low-competition target.
- Pakistan electricity-bill and salary-tax ideas surfaced in autocomplete, but numeric volume was unavailable. These topics also require current official tariff or tax-year data and frequent maintenance. Do not implement them without a primary-source update process and stronger demand evidence.
- The clearest first-party content opportunity remains the already indexed years-to-days page: 220 impressions and average position 44.7 in the measured window. Keep its URL stable and use the query/page evidence for a focused content and internal-link review after the new release. The next project priority is the GSC indexing backlog for the Health, Money and Math hubs, not another generic calculator.

## Query-to-page map

Search-volume status: partial cached global Google keyword metrics are recorded above. Terms without a returned cached metric remain unquantified. These figures are not GSC data, organic difficulty scores, ranking claims or traffic guarantees. No permutation pages are created.

| Query seed / primary intent | Related questions served | Destination | Evidence needed | Existing content coverage | Publication status |
|---|---|---|---|---|---|
| calorie calculator; daily calorie calculator; maintenance calorie calculator | How many calories do I need daily? What is maintenance energy? | `/calorie-calculator/` | Mifflin–St Jeor original equation, stated activity assumptions, independently checked examples | Existing BMI page does not estimate maintenance calories; this page adds a distinct calculation intent | Published in English by 2026-11-26; the three-formula upgrade remains pending PR #354 |
| TDEE calculator; daily calorie needs; how many calories do I need | What does the activity factor mean? Are exercise calories included? | `/calorie-calculator/` | Explain REE × app-defined factor; distinguish this estimate from measured TEE and from FAO/WHO/UNU PAL calculations | Existing health hub had BMI-focused content; new page adds the missing maintenance estimate | English page planned for release; not production-published |
| BMR calculator; resting energy calculator; Mifflin St Jeor calculator | Is REE the same as BMR or RMR? Is BMR a safe minimum? | `/calorie-calculator/` | Original 1990 paper, accurate terminology and explicit limitations | Existing BMI page does not explain the Mifflin equation or REE | English page planned for release; not production-published |
| calorie calculator kg cm; calorie calculator pounds feet | How are pounds and feet/inches converted? Why can rounding change results? | `/calorie-calculator/` | Exact unit conversion constants, metric/imperial equivalence fixtures, rounding tests | No equivalent existing unit-aware calorie estimator | English page planned for release; not production-published |
| why calorie calculators differ; activity level calculator explanation | Why does another calculator show a different estimate? What if activity is uncertain? | `/calorie-calculator/` | Compare equation, population, activity assumptions and rounding without unsupported accuracy claims | Existing general methodology page does not cover calorie-estimate differences in detail | Published in English by 2026-11-26; FAQ coverage updated for three formulas |
| is this calorie calculator free; does it need sign-up; are measurements stored | Does reset clear entries? Are values sent to an API? | `/calorie-calculator/` | Verify browser code, network requests, URL and storage behavior; check existing privacy policy and third-party scripts | General privacy page exists; page-specific FAQ documents this feature's behavior and limits | English FAQ planned for release; not production-published |
| can teenagers use a calorie calculator; pregnancy calorie calculator; breastfeeding calories | Who is excluded and why? | `/calorie-calculator/` | Adult eligibility boundary, NIDDK disclaimer context, no ordinary result for excluded selections | Existing BMI page is not a substitute for this calculator's eligibility rules | Published in English by 2026-11-26; DRI life-stage path remains separate |
| daily kitni calories chahiye; meri maintenance calories kitni hain; calories kaise calculate karein; روزانہ کتنی کیلوریز چاہئیں; کیلوری کیلکولیٹر | Urdu explanation of REE, activity assumptions, safety and result interpretation | No localized destination currently published | Competent Urdu translation review of every scientific, safety, form, result, navigation and metadata string | Existing Urdu journey does not yet include this calculator | Planned; unpublished until competent language review |

This map deliberately consolidates related intents on one useful calculator page. It does not imply measured demand, search volume, indexing, rankings, AI citations or language support.
