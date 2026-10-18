# Phase 2 Decisions

Status: decisions recorded before implementation  
Branch: `fix/indexing-v4`  
Baseline: production deployment `dpl_BFEQAx6HUx8gJzz58YZYPBSbhszn`, commit `fdbe6df3099b9d7f3dd4258292a1cc80665cb1b6`.

## 1. Trailing slash

**Decision: no change to the global trailing-slash mechanism.** `vercel.json` already has explicit 301 rules for the five named trust paths and a catch-all 308 slash canonicalization rule. It has no `trailingSlash` key. Do not add `trailingSlash` or duplicate those redirects. Keep the existing routes and verify the exact targets on preview.

## 2. Hub indexability

Apply the requested internal standard to the full visible main content, excluding navigation and footer. Keep a hub indexable only when the full main text is at least 150 words and it contains plain HTML anchor links directly to its tools.

- **Indexable:** `/ur/` (266 words, 8 direct tool links), `/health/` (221, 1), `/money/` (292, 3), `/math/` (225, 2), `/time/` (247, 2), `/worship/` (209, 1).
- **Noindex, follow:** `/ar/` (146 words and category-only links), `/es/` (195 words and category-only links), `/fr/` (206 words and category-only links), `/hi/` (210 words and category-only links). Keep their existing links; do not add direct tool links or rewrite translated content in this task.

The current finalizer's first-list-only word counter is not compliant with the stated rule. Count the full visible `<main>` content after excluding navigation/footer/script/style, and retain list item text. Category tool links must use canonical trailing-slash paths so they link directly to the URLs in the sitemap.

## 3. Sitemap and manifests

**Decision: keep build-time generation.** `seo_finalize.py` generates `public/sitemap.xml` and `public/robots.txt`. Keep only indexable, absolute HTTPS canonical URLs in the sitemap, with one URL per language version. Exclude all noindex pages and redirect-only paths. Derive lastmod from git history of the relevant page source file(s). If unavailable, use the build date and report the exact fallback.

The supplied Phase 4 script expects `urls.txt` to contain **paths**, not absolute URLs. Change it to path-only entries. Keep `indexable.txt`, `noindex.txt`, and `no-slash.txt` as path manifests.

## 4. Preview host

**Decision: no host-header change.** Vercel metadata lists the main-branch preview alias, but the public check lands on Vercel login/SSO rather than application content. Deployment protection prevents public crawling, so no X-Robots-Tag rule is needed. Recheck the branch preview after it deploys. If the new preview is protected, report the exact limitation and do not weaken protection or merge based on a failed remote test.

## 5. Outlier pages

- `/about`: slashless URL is a noncanonical route to `/about/`. The canonical page has 185 visible main words and no native main-content links. Do not rewrite it in this task.
- `/discount-calculator/`: 392 visible main words and five native main links. No missing-content cause found. Leave the content and calculator logic unchanged.
- `/ur/bmi-calculator/`: 168 visible main words and three native main links. The extra evidence-note block is intentionally omitted by `build.py:1125`; the formula and FAQ remain. Do not rewrite content.
- `/ur/discount-calculator/`: 115 visible main words and three native main links. The extra evidence-note block is intentionally omitted by `build.py:1125`; formula and FAQ remain. Record the short main content and do not rewrite it without approval.

## 6. Metadata, hreflang and JSON-LD

- Preserve unique titles under 60 characters, unique descriptions 120-160 characters, and self-referencing absolute canonical URLs on every indexable page. Keep build validation that fails on duplicate or out-of-range metadata.
- For translated homepages, provide explicit English and Urdu alternate entries plus the existing Arabic, Hindi, Spanish and French entries, with `x-default` pointing to the English homepage. The finalizer must not publish hreflang references to noindex pages. For translated calculator pages, keep English/Urdu alternates only where the equivalent Urdu page exists; x-default points to English.
- Keep WebApplication JSON-LD on calculator pages and Organization JSON-LD on the homepage. Ensure every indexable page has valid WebPage JSON-LD with `dateModified` equal to the visible page-specific “Last reviewed” date.
- Replace the hard-coded shared review date with the relevant source-file git date. Use the same date for visible “Last reviewed”, WebPage `dateModified`, and sitemap `lastmod`.
- Remove FAQPage JSON-LD generation. The hard rule explicitly prohibits adding FAQ rich-result markup. Keep visible FAQ text unchanged.
- Do not add `llms.txt` or AI-only markup.

## 7. Tests and merge gate

- Add the provided Phase 4 script as `tests/phase4-indexing.sh` and make its manifests conform to its expected path format.
- Build and run all existing CI tests plus new checks for full-main hub eligibility, date consistency, JSON-LD validity/no FAQPage, metadata bounds/uniqueness, canonical and sitemap consistency, and redirect configuration.
- Deploy branch preview. Run Phase 4 against preview and Phase 5 checks. If a required preview check fails or is blocked by deployment protection, stop and report. Do not merge.
- Only after all preview checks pass, open the PR and merge. Then run Phase 4 against production and verify READY deployment plus merged SHA.
- Do not submit URL indexing requests in Search Console. Sitemap submission only.
