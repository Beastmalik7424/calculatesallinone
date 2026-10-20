# CalculateAllInOne SEO, AI visibility and technical-health blueprint

Audit date: 2026-10-20  
Production URL: https://calculateallinone.vercel.app/  
Repository: Beastmalik7424/calculatesallinone  
Purpose: prioritize changes by user impact, Google Search eligibility, correctness and regression risk. This is an implementation plan, not a guarantee of rankings or a claim that every page/device has been tested.

## Evidence baseline

Independent external checks run on 2026-10-20:

- AIOScan: 95/100, 20/21 checks passed; its one listed fix was question-formatted headings.
- Glippy GEO: 75/100, grade B; robots.txt and sitemap discovered, no AI crawlers blocked, llms.txt absent. It reported content positioning and content depth as weak areas, and partial contact signals. Some page-type-dependent checks were not scored because the homepage type was not confirmed.
- GEO Tool Check: 71/100, Fair; homepage reachable with HTTP 200, HTTPS and indexability signals passed, sitemap declared, AI crawlers allowed, llms.txt absent. It flagged no external references/concrete examples and limited question headings.
- GrowMyWebsite: 92/100, 10/12 checks passed; reported no images detected and content depth as a warning.
- Lytical broken-link check: 29 homepage links checked, 29 working, 0 broken. This was a homepage-link sample, not a full-site crawl.

Scores use different methodologies and must not be averaged. Automated scans do not prove Google has indexed a URL, do not test every calculator calculation, and do not replace real mobile/device testing.

## Implemented in this branch

1. Improved homepage explanatory copy with qualified descriptions of Zakat, profit/loss, discounts, adult BMI, age, unit conversion, stopwatch and tasbih.
2. Added worked arithmetic example: a 20% discount on 1,000 leaves 800 before applicable taxes/fees.
3. Added primary references for adult BMI (WHO) and the inch definition (NIST).
4. Made the English homepage explanatory and FAQ H2 headings question-led without changing the calculator interface.
5. Added output smoke-test assertions for these key content requirements.

Sources:
- WHO BMI information: https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index
- NIST length units: https://www.nist.gov/pml/owm/si-units-length

## Prioritized implementation plan

### P0 — Release safety and calculator correctness
- Keep changes on a feature branch until the build, generated-page smoke tests, monetization smoke tests and all-calculator smoke tests pass.
- Validate each calculator with boundary and representative test vectors, including invalid/empty inputs, decimals, unit changes, leap dates, zero denominators, negative results where valid, and rounding.
- Check browser console errors, keyboard-only use, mobile viewport overflow, and form validation for every calculator.
- Never alter calculator formulas as part of copy/SEO work without independent expected-value tests.
- Verify security headers from the deployed response, not merely from vercel.json. Review Content-Security-Policy changes against all required scripts, styles, fonts, images, frames and network calls before modifying it.

### P1 — Google Search eligibility and crawl integrity
- Use Search Console URL Inspection for homepage and every priority calculator page. Record indexed status, Google-selected canonical, live-test result, rendered HTML and blocked resources.
- Verify sitemap URLs are absolute HTTPS URLs on the canonical host, resolve to real pages, use matching canonical tags, and exclude noindex/unreviewed pages.
- Keep sitemap lastmod values only when they reflect a real, significant content update. Do not fabricate dates.
- Confirm robots.txt allows important HTML/CSS/JS resources and that noindex directives are intentional.
- Check redirects, 404/soft-404, duplicate titles/descriptions, canonicals, hreflang pairs and internal links across the whole generated site.
- Submit the sitemap once in Search Console if it is not already submitted; use URL Inspection for a small number of materially changed priority pages. Indexing is not guaranteed and can take time.

### P1 — Real-world performance and accessibility
- Run PageSpeed Insights for mobile and desktop on the homepage and priority calculator pages. Save both Lighthouse lab results and CrUX field data when available.
- Evaluate Core Web Vitals at the 75th percentile: LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1. Do not infer field performance from a single response-time sample.
- Run Lighthouse accessibility and manual checks for visible focus, labels, error messages, contrast, keyboard operation, reduced motion, text zoom and RTL/mobile overflow.
- Check asset sizes, caching, font loading, third-party advertising scripts and Content-Security-Policy violations. Avoid performance changes that break calculator behavior or consent handling.

### P1 — Helpful, source-backed content
- Each calculator page should explain the intended use, input definitions, formula, one independently checked worked example, rounding/units, important exclusions and limitations.
- Add authoritative references where they genuinely support a claim. Health pages should clearly distinguish screening from diagnosis. Religious and financial tools should explain assumptions and direct users to qualified help for context-dependent decisions.
- Prefer unique, useful explanations over a target word count. Do not pad pages, mass-generate near-duplicates, invent expertise, or fabricate reviews, user counts, certifications or performance claims.
- Keep titles, descriptions, H1, canonical URL and visible content aligned. Question headings are useful when they match real user questions, not as a blanket rewrite rule.

### P2 — Structured data and entity clarity
- Validate JSON-LD with Google's Rich Results Test and Schema.org Validator. Structured data must describe visible, accurate content and meet each type's requirements.
- Keep WebSite, Organization, WebPage and WebApplication properties only where appropriate. Do not add Article/BlogPosting schema to the homepage or mark up nonexistent reviews/ratings.
- Add official social-profile sameAs links only after those profiles are confirmed as controlled by the site owner.
- Re-test schema after every build because seo_finalize.py modifies generated HTML.

### P2 — Trust, privacy and monetization
- Confirm contact details are current and reachable; make correction reporting easy.
- Keep methodology, editorial policy, privacy, terms and advertising/affiliate disclosures consistent with actual site behavior.
- Confirm the real consent-management setup and applicable regional requirements before enabling ad slots. Existing build safeguards are not proof that account-side consent configuration is complete.
- Never publish personal contact details or business credentials that the owner has not confirmed should be public.

### P3 — Optional AI-discovery enhancements
- An llms.txt file is optional and is not a Google ranking requirement. Consider it only after core indexing, useful content, crawl integrity and performance are sound.
- AI-crawler allow rules do not guarantee that ChatGPT, Gemini, Claude or Perplexity will cite the site. Measure actual citations/traffic separately from crawl access and tool scores.

## Acceptance gates before production

1. Clean dependency install and full `npm run build` succeeds.
2. `tests/site-output-smoke.py`, `tests/monetization-smoke.py` and `tests/all-calculator-smoke.cjs` all pass.
3. Review the generated HTML and sitemap for homepage, Zakat, BMI, profit/loss, discount, age, unit conversion, stopwatch and tasbih pages.
4. Check preview deployment for HTTP status, canonical, robots, sitemap, links, browser console, mobile layout and calculator outputs.
5. Run PageSpeed Insights mobile/desktop and save the results. If field data is unavailable, state that rather than substituting lab data.
6. Merge to main only after checks pass and review any diff that changes formulas, CSP, noindex/canonical, sitemap behavior or privacy/ads.
7. After deployment, re-check production URLs and Search Console. Roll back if the deployed build fails smoke tests or critical behavior.

## Current limitations / not yet verified

- Search Console index status, sitemap processing state and live URL Inspection results require access to the verified property and have not been confirmed by this external audit.
- A complete PageSpeed Insights/Lighthouse report and CrUX field-data report have not yet been collected.
- Broken-link testing covered 29 homepage links only, not every page or external link.
- Security headers were reviewed in repository configuration, but the live HTTP response has not yet been independently verified.
- Full cross-browser/mobile manual testing and independent formula review remain outstanding.
