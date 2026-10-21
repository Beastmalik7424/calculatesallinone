# CalculateAllInOne SEO Indexing Baseline

Audit date: 2026-10-22
Production: https://calculateallinone.vercel.app/
Repository baseline commit: 96ff760f2527eb400ba8351be5db5884219a9296
Feature branch: fix/seo-indexability-audit-2026-10-22

## Scope and measurement notes

This is the baseline captured before any code changes in this branch. HTTP status and page HTML were retrieved from the live Vercel URLs. The fetch interface exposed the final response status but did not expose an HTTP redirect chain or response headers for every HTML page, so those fields are marked unverified rather than guessed. Word counts are approximate visible-text counts after stripping HTML tags from the fetched body, not browser-rendered accessibility-tree counts. No production files were changed to capture this baseline.

## Live page baseline

| Requested URL | HTTP | Redirect chain | X-Robots-Tag | Meta robots | Canonical | Hreflang | Title | Description chars | H1 | Approx visible words |
|---|---:|---|---|---|---|---|---|---:|---:|---:|
| / | 200 | Not exposed by fetch tool | Not exposed | index, follow | Self | en, x-default | CalculatesAll | Free Online Calculators and Utility Tools | 138 | 1 | 836 |
| /ar/ | 200 | Not exposed by fetch tool | Not exposed | noindex, follow | Self | en, x-default | CalculatesAll | حاسبات وأدوات مجانية عبر الإنترنت | 111 | 1 | 227 |
| /contact | 200 | Not exposed by fetch tool | Not exposed | index, follow | /contact/ (mismatch) | None | Contact CalculatesAll | 151 | 1 | 168 |
| /discount-calculator/ | 200 | Not exposed by fetch tool | Not exposed | index, follow | Self | en, ur, x-default | Discount Calculator | Free Online Tool | CalculatesAll | 101 | 1 | 497 |
| /editorial-policy | 200 | Not exposed by fetch tool | Not exposed | index, follow | /editorial-policy/ (mismatch) | None | Editorial Policy | CalculatesAll | 118 | 1 | 441 |
| /es/ | 200 | Not exposed by fetch tool | Not exposed | noindex, follow | Self | en, x-default | CalculatesAll | Calculadoras y herramientas online gratuitas | 145 | 1 | 297 |
| /fr/ | 200 | Not exposed by fetch tool | Not exposed | noindex, follow | Self | en, x-default | CalculatesAll | Calculatrices et outils en ligne gratuits | 142 | 1 | 302 |
| /health/ | 200 | Not exposed by fetch tool | Not exposed | index, follow | Self | None | Health | CalculatesAll | 131 | 1 | 463 |
| /about/ | 200 | Not exposed by fetch tool | Not exposed | index, follow | Self | None | About CalculatesAll | 133 | 1 | 429 |
| /age-calculator/ | 200 | Not exposed by fetch tool | Not exposed | index, follow | Self | en, ur, x-default | Age Calculator | Free Online Tool | CalculatesAll | 78 | 1 | 526 |
| /bmi-calculator/ | 200 | Not exposed by fetch tool | Not exposed | index, follow | Self | en, ur, x-default | BMI Calculator for Adults | cm or ft/in | CalculatesAll | 133 | 1 | 911 |

## Sitemap and robots baseline

- https://calculateallinone.vercel.app/sitemap.xml returned HTTP 200.
- Sitemap entries inspected use trailing-slash canonical URLs. The sitemap currently omits lastmod values. The generator comment says dates are omitted because reliable page-specific content-change dates are unavailable.
- The live sitemap includes /about/, /contact/, /editorial-policy/, /health/, /discount-calculator/ and other pages. This conflicts with the older Search Console screenshot report that those URLs had no referring sitemap; Search Console may be stale or may not have processed the current sitemap yet.
- The sitemap's root-language homepage entry showed only en and x-default. Other unreviewed language homepages are excluded from sitemap by the current build logic.
- https://calculateallinone.vercel.app/robots.txt returned HTTP 200 and contains: User-agent: *, Allow: /, Disallow: /404, and Sitemap: https://calculateallinone.vercel.app/sitemap.xml.
- Live sitemap XML uses namespaced elements (including ns0 prefixes in the serialized output). Prefix choice is valid XML when namespaces resolve correctly, but it should be checked against a strict parser and the exact schema.
- Live response headers for HTML URLs were not exposed in the fetch result, so X-Robots-Tag and redirect chains remain unverified at this stage.

## Full repository tree at baseline

[DIR] .github
[FILE].github/dependabot.yml
[DIR] .github/workflows
[FILE].github/workflows/ci.yml
[FILE].github/workflows/site-build.yml
[FILE].gitignore
[FILE]MONETIZATION_SETUP.md
[FILE]QUALITY_AUDIT_REPORT.md
[FILE]QUALITY_BLUEPRINT.md
[FILE]SECURITY.md
[FILE]build.py
[FILE]content_v13.py
[FILE]content_v5.py
[DIR] docs
[FILE]docs/SEO-TECHNICAL-HEALTH-BLUEPRINT-2026-10-20.md
[FILE]emi-calculator.html
[FILE]google2e764d068684499b.html
[FILE]indexable.txt
[FILE]lang_v6.py
[FILE]llms.txt
[FILE]no-slash.txt
[FILE]noindex.txt
[FILE]package-lock.json
[FILE]package.json
[DIR] review
[FILE]review/translations_review.csv
[DIR] scripts
[FILE]scripts/lighthouse-audit.sh
[FILE]seo_finalize.py
[DIR] static
[FILE]static/app.js
[FILE]static/site.css
[DIR] styles
[FILE]styles/input.css
[FILE]tailwind.config.js
[DIR] tests
[FILE]tests/all-calculator-smoke.cjs
[FILE]tests/braces-hardening-smoke.cjs
[FILE]tests/calculator-smoke.cjs
[FILE]tests/emi-calculator-smoke.cjs
[FILE]tests/input-validation-smoke.cjs
[FILE]tests/monetization-smoke.py
[FILE]tests/redirect-contract.sh
[FILE]tests/site-output-smoke.py
[FILE]tests/vercel-redirect-config-smoke.py
[FILE]urdu_v5.py
[FILE]urls.txt
[FILE]vercel.json

## Baseline limitations

- This tree is the GitHub API recursive tree for main at the baseline commit shown above.
- No local clone or full build was executed during baseline capture.
- Generated public/ output is not stored as source in the repository; it is created by build.py and seo_finalize.py during builds.
- Source-level audit, generator/build comparison, and full test execution must happen after this baseline file is committed to the feature branch.
