# SEO audit for the seven scoped pages

Audit date: 2026-10-21 UTC

Production site: https://calculateallinone.vercel.app/

Branch: seo-seven-pages

Pull request: https://github.com/Beastmalik7424/calculatesallinone/pull/51

## Summary

Four scoped pages remain indexable: /contact/, /discount-calculator/, /editorial-policy/, and /health/.

Three language homepages remain noindex until a competent native-language review is recorded. This is intentional and is not an indexing defect.

The production baseline had no X-Robots-Tag header on the seven pages. All seven returned HTTP 200, stayed on their requested slash URLs, and used self-referencing canonicals.

The branch build and local CI checks passed. Production has not been changed or merged.

## Baseline table

Captured from production before merging any branch changes. Visible word counts exclude shared navigation, header, footer, scripts, styles, and non-visible text.

| URL | HTTP | Redirect | X-Robots-Tag | Meta robots | Canonical | Hreflang | Title | Description chars | H1 | Visible main words |
|---|---:|---|---|---|---|---|---|---:|---:|---:|
| /ar/ | 200 | None | Absent | noindex, follow | Self | en, x-default to / | CalculatesAll | حاسبات وأدوات مجانية عبر الإنترنت | 110 | 1 | 166 |
| /es/ | 200 | None | Absent | noindex, follow | Self | en, x-default to / | CalculatesAll | Calculadoras y herramientas online gratuitas | 156 | 1 | 222 |
| /fr/ | 200 | None | Absent | noindex, follow | Self | en, x-default to / | CalculatesAll | Calculatrices et outils en ligne gratuits | 148 | 1 | 232 |
| /contact/ | 200 | None | Absent | index, follow | Self | None | Contact CalculatesAll | 156 | 1 | 108 |
| /discount-calculator/ | 200 | None | Absent | index, follow | Self | en, ur, x-default | Discount Calculator | Free Online Tool | CalculatesAll | 101 | 1 | 438 |
| /editorial-policy/ | 200 | None | Absent | index, follow | Self | None | Editorial Policy | CalculatesAll | 123 | 1 | 380 |
| /health/ | 200 | None | Absent | index, follow | Self | None | Health | CalculatesAll | 136 | 1 | 402 |

Note: The baseline Spanish title is exactly 60 characters, so it did not meet the requested strict limit of fewer than 60 characters. The response-header and redirect results were inspected in a public browser, not inferred from HTML alone.

## Root cause and changes

| Page or shared issue | Baseline evidence | Change |
|---|---|---|
| /ar/, /es/, /fr/ | All had noindex, follow because seo_finalize.py keeps unreviewed language homepages out of search. The translation review CSV has no completed reviewer fields. They also advertised hreflang alternates despite being noindex. | Kept them noindex and out of the sitemap. Removed hreflang tags from noindex pages. Decision for each language remains OWNER TO CONFIRM. |
| /es/ title | The baseline title was 60 characters, not fewer than 60. | Shortened the Spanish title to “CalculatesAll | Calculadoras gratis en línea”. |
| /contact/ | Indexable, self-canonical, 108 visible main words, and an existing contact email is configured in the repository. No BreadcrumbList was present. | Kept the existing configured contact method. Added BreadcrumbList structured data and a sitemap lastmod date for the scoped change. |
| /discount-calculator/ | Indexable, self-canonical, 438 visible main words, formula, worked example, limitations, three FAQ items, WebApplication schema, and BreadcrumbList were already present. | Preserved calculator logic and existing useful content. Added a direct footer link and a sitemap lastmod date. FAQPage remains generated from visible FAQ content. |
| /editorial-policy/ | Indexable, self-canonical, 380 visible main words. Existing text says the site does not claim independent review unless it occurred. No BreadcrumbList was present. | Kept the existing factual policy without inventing author or reviewer credentials. Added BreadcrumbList and a sitemap lastmod date. |
| /health/ | Indexable, self-canonical, 402 visible main words with general adult BMI screening context. No BreadcrumbList was present. | Kept existing site-specific health content and its limitations. Added BreadcrumbList and a sitemap lastmod date. |
| Shared footer | No direct footer links to /discount-calculator/ and /health/. | Added direct slash-form links and localized their labels for English, Urdu, Arabic, Hindi, Spanish, and French. |
| Sitemap | Existing generator and test suite intentionally prohibited all lastmod values. | Added lastmod only for the four indexable scoped pages, using the verified UTC change date 2026-10-21. Updated the smoke test to allow exactly those four dates. |
| Google Search Console status | “Unknown to Google” is not itself proof of a page-level technical defect. Live pages were already indexable and self-canonical. | Added crawlable internal links, BreadcrumbList data, and accurate scoped lastmod entries. Search Console must be checked after production deployment. Indexing cannot be guaranteed. |

## Language decisions

| Page | Decision | Reason |
|---|---|---|
| /ar/ | Keep noindex | Native-language review is not recorded. OWNER TO CONFIRM. |
| /es/ | Keep noindex | Native-language review is not recorded. OWNER TO CONFIRM. |
| /fr/ | Keep noindex | Native-language review is not recorded. OWNER TO CONFIRM. |

No indexable language homepage was approved by this change. Therefore, reciprocal hreflang between these three language homepages was not added. A language homepage should only become indexable after the owner confirms a competent native-language review and the review log is completed.

## Test evidence

The latest successful GitHub Actions run is available at:

https://github.com/Beastmalik7424/calculatesallinone/actions/runs/39681590886

The existing site-build workflow also passed:

https://github.com/Beastmalik7424/calculatesallinone/actions/runs/39681590977

| Test | Result | Evidence |
|---|---|---|
| T1 Build | PASS | GitHub Actions build completed. Existing build, calculator, input-validation, and monetization tests passed. |
| T2 Sitemap XML | PASS | xmllint reported “sitemap XML valid”. |
| T3 Scoped sitemap membership | PASS | Exactly these scoped indexable URLs were listed: /contact/, /discount-calculator/, /editorial-policy/, /health/. The three unreviewed language homepages were excluded. Each of the four entries has lastmod 2026-10-21. |
| T4 Preview HTTP with no redirect | NOT PASSED | Vercel preview protection redirects anonymous requests to the Vercel login page. The authorized share URL removes its access token with a redirect. The page itself then returns HTTP 200. The exact no-redirect curl condition cannot be certified while preview protection remains enabled. |
| T5 Meta robots | PASS | Local generated HTML and authorized preview inspection showed noindex only on /ar/, /es/, and /fr/ among the seven scoped pages. |
| T6 Canonical | PASS | All seven preview pages returned their correct canonical production slash URLs. |
| T7 Hreflang | PASS FOR CURRENT DECISIONS | No language homepage is indexable, so no reciprocal hreflang set is required yet. Noindex language pages no longer emit hreflang tags. Recheck after any language receives native review. |
| T8 Unique metadata | PASS | The focused test verified unique titles and descriptions across the homepage and seven scoped pages. All titles are under 60 characters and descriptions are under 160 characters. |
| T9 Main content | PASS | Generated main-content counts: discount calculator 430 words, editorial policy 380 words, health hub 402 words. |
| T10 Headless browser | PASS | Local headless browser: seven pages, HTTP 200, zero console or page errors. Authorized preview browser inspection: seven pages loaded, zero console or page errors. |
| T11 Lighthouse SEO | PARTIAL | Local generated pages: contact 100/100, discount calculator 100/100, editorial policy 100/100, health 100/100. The three intentionally noindex language pages scored 66/100, with only the expected is-crawlable audit failing. Preview Lighthouse was not run because preview protection blocks the unauthenticated audit. |
| T12 Internal links | PASS | Existing site-output-smoke.py and the focused seven-page test passed internal-link checks. |
| T13 HTML validation | PASS | Nu HTML Checker validated the homepage and seven scoped pages with zero errors and zero warnings. |

Preview browser inspection was performed against:

https://calculatesall-429c7tkdb-malikadeelbhatti-1187.vercel.app/

That preview is protected by Vercel access controls. A temporary authorized link was used for read-only browser inspection. The token is not included in this report.

## Files changed on the branch

- build.py: adds BreadcrumbList to the targeted static pages and health hub, and adds localized footer links.
- seo_finalize.py: removes hreflang from noindex pages and emits lastmod for the four indexable scoped pages only.
- lang_v6.py: shortens the Spanish homepage title to under 60 characters.
- tests/site-output-smoke.py: validates the four verified lastmod entries.
- tests/seo-seven-pages.py: checks metadata, sitemap membership, lastmod, content counts, schema, and internal links for the seven pages.
- tests/seo-seven-pages-browser.cjs: checks browser status and console errors.
- tests/validate-html.py: runs the Nu HTML Checker.
- .github/workflows/ci.yml: adds the scoped XML, SEO, HTML, Lighthouse, and browser checks.

## Deployment status

Preview deployment: https://calculatesall-429c7tkdb-malikadeelbhatti-1187.vercel.app/

Production: https://calculateallinone.vercel.app/

The preview build is READY. Production has not been modified. Pull request #51 remains open and unmerged because the exact no-redirect preview test and preview Lighthouse test remain blocked by Vercel preview protection.

Next required step: the owner must approve either temporarily making the preview publicly accessible for the remaining checks, with protection restored immediately afterward, or providing an approved secure CI bypass method. Do not merge until the remaining preview tests are completed.
