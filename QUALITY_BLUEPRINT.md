# CalculateAllInOne Quality Blueprint

## Objective
Improve the live site against current Google Search Essentials and AdSense site-readiness guidance without promising ranking, indexing, or AdSense approval.

## Audited areas
1. Crawlability: HTTPS, robots.txt, XML sitemap, canonical URLs, trailing-slash consistency, internal links, index/noindex manifests.
2. Metadata: unique titles and descriptions, no irrelevant boilerplate appended to policy-page snippets.
3. Structured data: valid JSON-LD; dateModified must not falsely claim that every page was reviewed on one date.
4. Content quality: original tool explanations, formulas, worked examples, limits, clear navigation, contact and trust pages.
5. Monetization readiness: verified publisher script, matching ads.txt record, ad slots fail closed until a real slot ID and account-side consent configuration are confirmed.
6. Accessibility and UX: semantic headings, labelled inputs, responsive controls, localized navigation, keyboard focus.
7. Regression safety: deterministic build, calculator smoke tests, sitemap/manifests consistency, local asset and internal-link checks.

## Implementation decisions
- Remove the arbitrary 150-word *intro-only* indexing gate. A page is evaluated using its main explanatory content and crawlable tool links, not a word-count rule applied before the tool list.
- Keep the Arabic, Hindi, Spanish and French homepages out of the index until their translated tool journey has been reviewed by a competent speaker. Do not imply those translations are fully reviewed.
- Keep the Urdu homepage out of the index until its translated user journey is confirmed. Urdu calculator pages remain eligible where their actual content and metadata pass checks.
- Do not add generic “formula/example/limits” text to unrelated policy-page descriptions.
- Do not display a blanket “Last reviewed” date or set every page's dateModified to the same date. Use a source-derived date only when available; omit optional freshness metadata when it is not.
- Keep ad slots disabled until a real AdSense ad-unit slot and the owner's consent configuration are confirmed.

## Required verification before production
- Build completes without errors.
- Calculator behavior tests pass.
- Every sitemap URL has a generated page, unique title and description, canonical URL, and index directive.
- Sitemap contains no duplicate URLs and agrees with indexable/noindex manifests.
- Every indexable page has an incoming crawlable internal link.
- Internal links and local assets resolve.
- JSON-LD parses; dateModified is not fabricated.
- ads.txt returns the exact publisher record and the homepage contains the matching publisher script.
- Production deployment reaches READY, then live URLs are checked.

## Limits
Google does not publish a guaranteed word-count threshold or a checklist that guarantees AdSense approval or indexing. Final approval and indexing are Google's decisions. Native-language review, Google Search Console live URL inspection, and actual AdSense dashboard status must be verified separately.
