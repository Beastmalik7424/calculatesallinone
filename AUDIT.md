# Phase 1 Read-Only Audit

Audit date: 2026-10-18  
Repository: https://github.com/Beastmalik7424/calculatesallinone  
Production: https://calculateallinone.vercel.app/  
Rollback deployment: `dpl_BFEQAx6HUx8gJzz58YZYPBSbhszn`  
Rollback/current production commit: `fdbe6df3099b9d7f3dd4258292a1cc80665cb1b6`  
Branch created from `main`: `fix/indexing-v4`

## Repository root inventory

The public GitHub root showed 6 folders and 18 files.

Folders: `.github/`, `review/`, `scripts/`, `static/`, `styles/`, `tests/`.

Files: `.gitignore`, `MONETIZATION_SETUP.md`, `SECURITY.md`, `build.py`, `content_v13.py`, `content_v5.py`, `google2e764d068684499b.html`, `indexable.txt`, `lang_v6.py`, `no-slash.txt`, `noindex.txt`, `package-lock.json`, `package.json`, `seo_finalize.py`, `tailwind.config.js`, `urdu_v5.py`, `urls.txt`, `vercel.json`.

## Framework, build, routing, sitemap

- **Framework/build output:** `vercel.json:1-5` sets `framework: null`, `buildCommand: npm ci && npm run build`, and `outputDirectory: public`. `package.json:4-8` shows Tailwind CSS plus Python-generated static HTML, followed by `seo_finalize.py` and smoke tests. This is a custom static-site build, not a framework-generated runtime app.
- **Trailing slash:** `vercel.json:54-100` has explicit 301 rules for `/contact`, `/editorial-policy`, `/methodology`, `/privacy`, and `/terms`, followed by a catch-all 308 slash canonicalization rule. There is no `trailingSlash` key. Do not add `trailingSlash`, because manual redirect rules already exist.
- **Sitemap generation:** no source `sitemap.xml` exists at the repository root. `seo_finalize.py:168-191` generates the sitemap and robots.txt during the build under `public/`. Production `/sitemap.xml` returned 200 and contained 27 unique URL entries. Its namespaced XML uses `ns0:loc` when serialized, so a plain `grep '<loc>'` incorrectly returns zero.
- **Manifest mismatch with the requested test:** `seo_finalize.py:172` currently writes `urls.txt` as absolute URLs, while the supplied Phase 4 script appends each entry to `BASE`. The manifest must be changed to path-only entries before that script can run correctly.
- **Indexability logic:** `seo_finalize.py:87-97` currently counts only the text before the first `<ul>`, and `strip_tags()` at lines 16-23 removes list content. That is not the requested full visible-main-text count. It causes pages with long tool lists and guide text to be treated as thin.
- **Dates:** `seo_finalize.py:11` hardcodes `REVIEW_DATE = "2026-10-18"`; lines 125-142 use that same value for visible “Last reviewed” and JSON-LD `dateModified`. This is not source-file-specific. `git_date()` at lines 44-52 already reads git history for sitemap lastmod and falls back to the build date if no source date is found.
- **Robots headers:** `vercel.json:6-53` has security headers but no `X-Robots-Tag`. Page-level robots meta and sitemap generation are handled in `seo_finalize.py:108-115`.
- **Preview host:** Vercel deployment metadata lists `calculatesall-git-main-malikadeelbhatti-1187.vercel.app` as an alias, but the public browser check lands on Vercel login/SSO rather than app content. The host is protected and not publicly crawlable. No app-level noindex header was observed on the captured SSO response. No host header change is needed while the host remains protected.

## Live production page checks

All 16 distinct production URLs below returned HTTP 200. Main-word counts are whitespace-separated visible text in the rendered `<main>`, excluding navigation and footer.

| Path | Main words | Native main links | Current robots | Decision evidence |
|---|---:|---:|---|---|
| `/` | Not separately counted | Not separately counted | index, follow | Homepage has Organization JSON-LD in `build.py:949-951`; finalizer adds WebPage JSON-LD. |
| `/bmi-calculator/` | Not separately counted | Not separately counted | index, follow | Self-canonical; WebApplication and BreadcrumbList JSON-LD. |
| `/about/` | 185 | 0 | index, follow | `build.py:1551+` contains a short static-page paragraph list. `/about` is the noncanonical no-slash form and routes to `/about/`; do not rewrite content without approval. |
| `/discount-calculator/` | 392 | 5 | index, follow | Main content and formula guide exist; no missing-content cause found. |
| `/ur/bmi-calculator/` | 168 | 3 | index, follow | Formula and FAQ content exist. `build.py:1125` deliberately omits the evidence-note block for Urdu BMI and discount pages. |
| `/ur/discount-calculator/` | 115 | 3 | index, follow | Formula and FAQ content exist, but visible main content is short. The evidence-note block is deliberately omitted at `build.py:1125`. No content rewrite without approval. |
| `/ar/` | 146 | 5 category links | noindex, follow | Under 150 words and the main links are category hubs, not direct calculator tools. |
| `/es/` | 195 | 5 category links | noindex, follow | Over 150 words, but the main links are category hubs, not direct calculator tools. |
| `/fr/` | 206 | 5 category links | noindex, follow | Over 150 words, but the main links are category hubs, not direct calculator tools. |
| `/hi/` | 210 | 5 category links | noindex, follow | Over 150 words, but the main links are category hubs, not direct calculator tools. |
| `/ur/` | 266 | 8 direct tool links | noindex, follow | Meets both internal hub criteria and should be indexable. Current noindex is a false negative caused by the current first-list-only count. |
| `/health/` | 221 | 1 direct tool link | noindex, follow | Meets both internal hub criteria and should be indexable. |
| `/money/` | 292 | 3 direct tool links | noindex, follow | Meets both internal hub criteria and should be indexable. |
| `/math/` | 225 | 2 direct tool links | noindex, follow | Meets both internal hub criteria and should be indexable. |
| `/time/` | 247 | 2 direct tool links | noindex, follow | Meets both internal hub criteria and should be indexable. |
| `/worship/` | 209 | 1 direct tool link | noindex, follow | Meets both internal hub criteria and should be indexable. |

The 150-word threshold is this project's internal standard, not a Google requirement. For hub decisions, the full visible main text and direct tool links are used, not the current finalizer's abbreviated count.

## Metadata and structured data findings

- Homepage title is `CalculatesAll | Free Online Calculators and Utility Tools`, self-canonical, and indexable. The current hreflang set is `en` and `x-default` on the homepage, but localized homepage alternatives are incomplete in `build.py` around `home_alts_all()` (around lines 790-805): the generated set does not include English and Urdu as explicit alternate language entries for every localized home.
- BMI page title is `BMI Calculator | Free Online Tool | CalculatesAll`, self-canonical, indexable, with WebApplication, BreadcrumbList, WebPage and FAQPage JSON-LD.
- Health hub title is `Health | CalculatesAll`, self-canonical, and currently noindex. Its description is shorter than the requested 120-160 character range, but the page is currently noindex and therefore not in the indexable metadata set.
- `seo_finalize.py:145-166` generates FAQPage JSON-LD from page details. The requested hard rule says not to add FAQ rich-result markup. This generator must stop adding it and remove generated FAQPage blocks.
- `build.py:1134-1147` builds category hubs with native tool anchors, but the anchor hrefs are currently missing the trailing slash. They should point directly to the canonical slash URLs.

## Outliers

- **`/about`:** the canonical page is `/about/`; the no-slash form is a noncanonical route. The canonical page has 185 visible main words and no native links in main content. No rewrite is authorized by this audit.
- **`/discount-calculator/`:** 392 visible main words and five native main links. The page has its own calculator guide. No missing-content cause found.
- **`/ur/bmi-calculator/`:** 168 visible main words. The code intentionally skips the additional evidence-note block for Urdu BMI and discount pages, but the formula/FAQ content exists. Do not rewrite content.
- **`/ur/discount-calculator/`:** 115 visible main words. The code intentionally skips the additional evidence-note block, and the rendered page is short. Report only; do not rewrite content without approval.

## Baseline production status

- Deployment: `READY`, production target, commit `fdbe6df3099b9d7f3dd4258292a1cc80665cb1b6`.
- `/sitemap.xml`: HTTP 200, 27 unique entries.
- `/robots.txt`: HTTP 200, permits crawling except `/404`, and references the sitemap.
- Five trust no-slash routes were previously verified as 301 to their slash versions, final status 200.
- `/ads.txt`: HTTP 404. No publisher ID was supplied; this is not changed in this indexing task.
- No Search Console indexing requests were made.

## Checks not completed in Phase 1

The public audit could inspect rendered HTML and repository files, but it did not execute calculator interactions or browser console checks in Phase 1. Those belong to Phase 5 and must be attempted against the preview after a successful build.
