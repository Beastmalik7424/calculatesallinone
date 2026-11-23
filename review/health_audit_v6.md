# Health hub audit v6

## 1. Verdict

**DO NOT USE for the requested content update.** No body rewrite, FAQ replacement, or test file was committed.

The requested change cannot be completed within the supplied allowlist. The body sections are in `content_v13.py` under `HUB_EXTRA["health"]`, but the actual five rendered FAQ entries are defined separately in `build.py` under `HUB_CONTENT["health"]["faq"]`. The renderer emits those FAQs after `guide_html(HUB_EXTRA[...])`. Editing only the permitted value in `content_v13.py` cannot replace the existing FAQ component. Adding a second FAQ set to the body would leave the five old questions in place and create duplicate FAQ content.

The current page also fails content requirements C1-C6. A content rewrite is therefore not committed. This is a diagnostic report, not an owner-ready content draft.

Reviewer: pending owner confirmation

Medical review: not completed

## 2. Operations

Repository: `Beastmalik7424/calculatesallinone`

Base: `main`

Working branch: `health-audit-v6`

| Operation | Status | Evidence |
|---|---|---|
| Read files | available | Read `content_v13.py`, `build.py`, `package.json`, `urls.txt`, `static/app.js`, `static/calorie-calculator.js`, and `calorie_calculator.py` from GitHub |
| Create branch | done | Created `health-audit-v6` from `main` |
| Commit | available | GitHub file-creation API is available. Only this report is committed because the content and FAQ scope conflict blocks a compliant rewrite |
| Open pull request | available, not used | No content or test changes exist to review. Opening a PR titled “content only” for a report-only branch would misrepresent its contents |
| Run build | unavailable | No checked-out repository runtime or command-execution connection is available in this session. The build script was read, not run |
| Run tests | unavailable | No checked-out repository runtime or command-execution connection is available in this session. Tests were read, not run |

No other branch was created or deleted. No file outside the report was changed.

## 3. C1-C13 self-checks

Checks below apply to the current `main` draft, not to a rewritten draft.

| Check | Result | Count / evidence |
|---|---|---|
| C1 WHO bands | FAIL | The current rendered FAQ names four broad categories. It does not provide the requested six-row table or the three obesity classes |
| C2 worked examples | FAIL | The metric BMI FAQ rounds height squared early to 3.06 rather than showing 3.0625. The imperial BMI example is present. Neither Mifflin worked example is present in the health hub body |
| C3 Asian action points | FAIL | Zero Asian action points are present in the current health body or FAQ |
| C4 FAQ count and completeness | FAIL | 5 questions found in `build.py`, lines 785-791. Requirement is 6-8 |
| C5 FAQ/body number consistency | FAIL | FAQ examples and categories are not fully represented in the body. The body has no matching calorie equations or examples |
| C6 internal links and anchor markup | FAIL | Only `/calorie-calculator/` appears in `HUB_EXTRA["health"]`. The other three required internal links are absent from that value |
| C7 prohibited punctuation | PASS | Current `HUB_EXTRA["health"]`: 0 em dashes, 0 semicolons, 0 asterisks |
| C8 reviewer/date text | PASS | Current `HUB_EXTRA["health"]`: no reviewer name, credential, publication date, or “last reviewed” text |
| C9 HTML escaping | NOT RUN | No build or test runtime was available. Source strings were inspected, but rendered HTML escaping was not executed |
| C10 originality scan | NOT RUN | The complete phrase-overlap scan across all HUB_EXTRA entries, calculator introductions, and About text was not executed. Longest shared run is not established |
| C11 heading order | PASS BY SOURCE INSPECTION | `build.py` emits the page H1, guide H2 sections, and the Questions H2. No skipped heading level is present in the inspected generator path. Generated DOM was not built |
| C12 build and tests | NOT RUN | Build unavailable. Test suite unavailable |
| C13 10,000-case simulation | NOT RUN | The actual JavaScript modules were inspected but could not be executed from a checked-out project runtime. No substitute simulation is represented as a run of the calculator code |

Current health body word count: 448 words in the `HUB_EXTRA["health"]` source value, counting words in the Python source strings and excluding the separate `HUB_CONTENT["health"]` intro and FAQ.

Current rendered FAQ count: 5.

FAQPage JSON-LD: not established by a build or generated-page inspection. No FAQPage block was found in the inspected health-hub schema construction path, which supplies the hub's existing CollectionPage and BreadcrumbList schema. This is source inspection, not a rendered HTML check.

## 4. Calculator checks

Source line numbers refer to `main`.

| Claim | Result | File and lines | Finding |
|---|---|---|---|
| BMI category uses unrounded BMI | CONFIRMED | `static/app.js`, lines 738-747 | The code calculates `bmi`, then chooses the category using `bmi < 18.5`, `bmi < 25`, and `bmi < 30`. It does not use `roundedBMI` for category selection |
| Displayed BMI rounds to one decimal | CONFIRMED | `static/app.js`, lines 744-747 | `Number(bmi.toFixed(1))` is used for the displayed value |
| Imperial BMI uses 703 × pounds ÷ inches² | CONFIRMED AS AN EQUIVALENT FORMULA IN THE CURRENT ENGLISH PATH | `static/app.js`, lines 723-740 | The English path converts pounds to kilograms using 0.45359237 and total inches to centimetres using 2.54, then calculates kg/m². This is mathematically equivalent to the 703 formula. The legacy path contains the literal expression at line 780 |
| Mifflin-St Jeor coefficients | CONFIRMED | `static/calorie-calculator.js`, line 46 | Male coefficient is +5 and female coefficient is −161 |
| Age range flagged | CONFIRMED | `static/calorie-calculator.js`, line 49 | The study-range flag is true when age is below 19 or above 78. The ordinary tool accepts ages 18-120; under 18 and over 120 are rejected by lines 22-23 |
| Exact age flag text | CONFIRMED | `static/calorie-calculator.js`, line 209 | “Age-range note: the original Mifflin–St Jeor study sample was 19–78 years. Your entered age is outside that original sample range, so this result has an additional evidence limitation.” |
| Activity assumption and visibility | CONFIRMED | `static/calorie-calculator.js`, lines 6-10 and 208-209; `calorie_calculator.py`, line 58 | The user selects a visible Activity level option. The result visibly prints “Activity assumption: ” followed by the selected label and description |
| Estimate, not target | CONFIRMED | `static/calorie-calculator.js`, line 215 | Result text: “This is a population-equation estimate, not a measured metabolic rate or a personalized medical prescription.” |

Visible activity assumptions printed in the result:

- Sedentary. Mostly seated work and little planned movement.
- Light activity. Some walking or light exercise, with mostly light daily movement.
- Moderate activity. Regular moderate exercise and a generally active daily routine.
- Very active. Frequent hard exercise or a physically demanding job.
- Extra active. Very demanding daily physical work or training.

The activity presets are application-defined consumer estimates, not activity factors from the original Mifflin-St Jeor paper or FAO/WHO/UNU PAL categories. The JavaScript source explicitly states this in lines 6-10.

## 5. Primary-source log

Access date for all sources below: 2026-11-23. Quotes are short extracts from the linked primary source.

### S1. WHO adult BMI classification

URL: https://iris.who.int/bitstream/handle/10665/43190/9241593024_eng.pdf

WHO SuRF Report 2, Table 3.1, page 22, identifies the “WHO classification of adult underweight, overweight, and obesity according to BMI”. The principal ranges are:

| Category | WHO table range |
|---|---:|
| Underweight | <18.50 |
| Normal range | 18.50-24.99 |
| Overweight | ≥25.00, including pre-obese 25.00-29.99 |
| Obese class I | 30.00-34.99 |
| Obese class II | 35.00-39.99 |
| Obese class III | ≥40.00 |

The table also lists additional public-health action cut-offs. These do not replace the principal classification.

WHO adult-age context URL: https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight

Exact source wording: “adults aged 18 years and older”.

### S2. WHO Expert Consultation on Asian BMI, The Lancet, 2004

URL: https://pubmed.ncbi.nlm.nih.gov/14726171/

DOI: 10.1016/S0140-6736(03)15268-3

Exact source wording: “The cut-off point for observed risk varies from 22 kg/m2 to 25 kg/m2”.

Exact source wording: “for high risk it varies from 26 kg/m2 to 31 kg/m2”.

Exact source wording: “the WHO BMI cut-off points should be retained as international classifications”.

Exact source wording: “23.0, 27.5, 32.5, and 37.5 kg/m2” are additional public-health action points.

### S3. Mifflin MD et al., American Journal of Clinical Nutrition, 1990

URL: https://pubmed.ncbi.nlm.nih.gov/2305711/

DOI: 10.1093/ajcn/51.2.241

The PubMed abstract is accessible. It reports “498 healthy subjects” aged “19-78 y”. It gives the male equation as 10 × weight + 6.25 × height − 5 × age + 5 and the female equation as 10 × weight + 6.25 × height − 5 × age − 161. Sample size, age range and both coefficients are verified from the original paper abstract.

### S4. CDC adult BMI and BMI-for-age guidance

Adult categories URL: https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html

Exact source wording: “For adults 20 and older”.

The CDC adult categories page confirms the displayed category bands, but its age threshold differs from the WHO adult-age context. The requested page must state which authority's age scope it is describing.

Formula URL: https://www.cdc.gov/growth-chart-training/hcp/using-bmi/calculating-bmi.html

Exact source wording: “BMI = weight (lb) / [height (in)]² x 703”.

Child and teen guidance URL: https://www.cdc.gov/bmi/child-teen-calculator/index.html

Exact source wording: “BMI is interpreted using sex-specific BMI-for-age percentiles.”

### S5. Google Search Essentials and spam policies

Search Essentials URL: https://developers.google.com/search/docs/essentials

Exact source wording: “Create helpful, reliable, people-first content.”

Spam policies URL: https://developers.google.com/search/docs/essentials/spam-policies

Exact source wording: “Scaled content abuse is when many pages are generated for the primary purpose of manipulating search rankings and not helping users.”

### S6. Google guidance on generative AI and helpful content

Generative AI URL: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

Exact source wording: “make sure your work meets the standards of the Search Essentials and our spam policies.”

Helpful content URL: https://developers.google.com/search/docs/fundamentals/creating-helpful-content

Exact source wording: “The ‘why’ should be that you're creating content primarily to help people”.

### S7. Google generative AI search guide

URL: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

Unique content: “Create valuable, non-commodity content for your audience”.

Technical structure: Google says to organise content with paragraphs, sections and headings that provide a clear structure.

Special markup: Google says “Structured data isn't required for generative AI search”. No special schema type is required for AI features.

The same guide states that meeting requirements does not guarantee crawling, indexing or serving.

### S8. AdSense readiness and policies

Eligibility and site readiness URL: https://support.google.com/adsense/answer/9724

Exact source wording: “Your content must be high-quality, original, and attract an audience.”

Program policies URL: https://support.google.com/adsense/answer/48182

The policy page states that publishers must adhere to Google Publisher Policies and AdSense Program policies. These sources do not certify a page or guarantee approval.

### S9. Search Quality Rater Guidelines

Official PDF URL: https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf

Version opened: March 5, 2024.

YMYL health passage, section 2.3, page 11: “mild inaccuracies or content from less reliable sources could significantly impact someone's health”.

YMYL health definition, section 2.3, page 11: “Topics that could harm mental, physical, and emotional health”.

Expertise passage, section 3.4.1, page 28: “information and advice must come from experts.”

The guidelines describe quality-rater evaluation concepts. They are not a ranking score or a direct ranking mechanism.

## 6. Current-draft scorecard

These scores assess the current page source, not a rewritten draft. They are editorial diagnostics, not Google ranking scores or AdSense approval predictions.

| Criterion | Score | Evidence and gap |
|---|---:|---|
| Search intent | 4/10 | “The BMI calculator uses the standard formula” appears in the hub intro. “BMI chart” and a complete “healthy BMI for adults” answer are not served near the start |
| Topical coverage | 2/10 | Current text says “It does not show body fat, muscle, or fitness.” Calculator.net has separate adult BMI chart, child and teen BMI table/chart, and risks sections. Omni Calculator has formula, normal BMI, BMI ranges, use, other considerations and FAQs. The South Asian Pakistan tool MNT has formula, South Asian adult context, waist thresholds and result explanations |
| Answer extractability | 4/10 | “BMI = weight (kg) ÷ height (m)².” is direct, but several answers are in the separate FAQ source and calorie answers are absent |
| FAQ completeness | 2/10 | “What are the adult BMI categories?” covers four broad groups only. Five questions exist, below the required six to eight, and there is no calorie-estimate FAQ |
| Originality | 3/10 | “The BMI calculator asks for weight and height and gives one screening number for adults.” is generic and not distinctive to the site's implementation |
| Expertise and trust | 4/10 | “The original Mifflin–St Jeor study included 498 healthy adults aged 19–78” is a specific, verifiable detail, but the hub lacks a complete source-led explanation and medical review is not completed |
| Medical safety | 6/10 | “This category page is general educational information, not personal medical advice.” is a useful boundary. The page still lacks the full requested coverage and explicit top and bottom disclaimer placement verification |
| Policy risk | 4/10 | “It is an estimate, not a measured metabolic rate or a medical prescription.” is helpful. Site-wide AdSense and Terms consistency was not re-audited in this task |
| Readability | 7/10 | “Use the adult BMI tool only for adults and discuss concerns with a qualified health professional.” is plain and direct. Missing sections limit completeness rather than sentence clarity |
| AI extractability | 4/10 | “The calculator selects the WHO category using the unrounded BMI” is precise. The page lacks a complete WHO table, Asian action-point explanation and calorie equations |

Competitor headings observed:

- Calculator.net: BMI chart for adults, BMI table for children and teens, BMI chart for children and teens, Risks associated with being overweight.
- Omni Calculator: How do I calculate BMI?, Normal BMI, What are the BMI ranges?, Using our body mass index calculator, Other considerations, FAQs.
- MNT Pakistan: How Is BMI Calculated?, BMI formula using kilograms and metres, BMI formula using pounds and inches, BMI Calculator for Pakistan and South Asian Adults, Waist thresholds relevant to South Asian adults, What the Advanced Results Mean.

Competitor pages are comparison context, not medical evidence.

## 7. Changes made

- No change to `content_v13.py`. A body-only rewrite would leave the actual FAQ component unchanged.
- No new test file. A test file for a non-integrated FAQ draft would not verify the rendered FAQ requirement.
- This diagnostic report is the only intended file change.

No meta tags, calculator logic, routes, layout, CSS, navigation, footer, schema, sitemap, robots.txt, ads code, or other pages were changed.

## 8. Removed or unverified claims

No page claims were removed because no page content was edited.

The following remain unverified for any proposed rewrite until implementation and tests are possible:

- Rendered FAQPage JSON-LD presence and FAQ text parity.
- Rendered HTML escaping.
- Full cross-site originality scan and longest shared phrase.
- Full build output and existing test suite.
- 10,000-case calculator simulation.
- Generated DOM outline and preview layout.

The BMI examples can be recalculated arithmetically, but arithmetic alone does not establish that the page's rendered code or calculator output has been tested.

## 9. Final body copy and FAQ

No final body copy or FAQ was committed. The requested FAQ cannot be replaced under the current allowlist because its source is `build.py`, not `content_v13.py`.

The current body remains unchanged on `main` and on `health-audit-v6`.

## 10. Owner actions

1. Approve a scope amendment allowing the health FAQ value in `build.py` to be changed, or provide a revised architecture that places the rendered health FAQ under the allowed content value without duplicating the existing FAQ.
2. Get a medical review from a qualified professional. Add a reviewer name and credential only after the owner confirms them in writing.
3. Once content and tests are committed, review the pull request and merge it after approval.
4. After deployment, open Search Console, go to URL Inspection, enter https://calculateallinone.vercel.app/health/, select Test live URL, then select Request indexing. Google decides whether and when to crawl or index the page.
5. Confirm that `/health/` appears in the sitemap.

## 11. Out-of-scope issues

Listed as requested. These were not changed or independently reverified in this task:

- The Terms page says advertising is not currently displayed, while the site loads an AdSense script.
- The audit report lists 32 URLs, while `urls.txt` lists 42.
- `/marketplaces/` redirects to `/`, which conflicts with `MONETIZATION_SETUP.md`.
- The GitHub secret `VERCEL_TOKEN` is missing, so the fallback deploy workflow cannot run.

## 12. Confidence

Primary-source verification is strong for the WHO classification table, the 2004 WHO Asian BMI action points and risk ranges, the Mifflin-St Jeor equations and original study sample, CDC BMI formula and child guidance, Google's published Search guidance, AdSense published eligibility and policies, and the quoted Search Quality Rater Guidelines passages.

Repository-source verification is strong for the location of the health body and FAQ, BMI category and display rounding logic, Mifflin coefficients, age-range flag, visible activity assumptions and estimate disclaimer.

Build, tests, rendered HTML, originality scan, simulation and preview were not run. Medical review is not completed.

**Final status: DO NOT USE as a completed content update. The FAQ allowlist conflict and current C1-C6 failures must be resolved before a content draft can be considered ready for owner review.**
