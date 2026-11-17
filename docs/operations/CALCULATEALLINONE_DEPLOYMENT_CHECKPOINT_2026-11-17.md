# CalculateAllInOne Audit and Deployment Checkpoint

Date recorded: 2026-11-17

## Purpose

Preserve the exact state of the CalculateAllInOne audit and pending Zakat mobile-layout deployment so work can resume from this checkpoint without repeating discovery.

This file is an operations checkpoint only. It does not change calculator code, formulas, URLs, canonicals, or production configuration.

## Repository and production identity

- Repository: `Beastmalik7424/calculatesallinone`
- Production branch: `main`
- Vercel project: `calculatesall`
- Vercel team: `malikadeelbhatti-1187`
- Production URL: https://calculateallinone.vercel.app/
- Main commit observed: `9cd4aea9ec4d4ad1c1bbc122ad8c9712df943a5a`
- Production deployment previously observed READY: `dpl_7cgFKi3ACkzYE11hBAxsz8aNA3Vc`

## Current audit evidence

- Production homepage, Zakat calculator, robots.txt and sitemap returned HTTP 200 in the latest checks recorded for this task.
- robots.txt allows OAI-SearchBot and general user agents, disallowing only /404.
- sitemap.xml returned HTTP 200 and contained 42 `<loc>` entries.
- Zakat calculator canonical observed: https://calculateallinone.vercel.app/zakat-calculator/
- Zakat calculator HTML was still referencing stylesheet version `20261116-zakat-first-screen-v1`, not the proposed PR version `20261117-zakat-positioning-v2`. This is evidence that the proposed stylesheet change was not yet reflected in production at the time of inspection.

## Existing implementation PR

- PR: https://github.com/Beastmalik7424/calculatesallinone/pull/283
- Title: `fix(zakat): refresh cached first-screen layout`
- PR state at checkpoint: OPEN, not merged.
- PR base: `main`
- PR head reported by GitHub PR metadata: `0cd568f1828bdeb95b0bc009c87fecdfb1953b60`
- PR branch: `fix/zakat-first-screen-positioning-v3`
- PR description reports changes for stylesheet cache busting, a six-column mobile/tablet and nine-column desktop Zakat shortcut grid, 44px targets, visible shortcut labels, restoration of the calorie calculator carousel on short phones, and no formula/canonical/URL changes.

### PR verification recorded

For commit `0cd568f1828bdeb95b0bc009c87fecdfb1953b60`, these GitHub workflow jobs were observed completed successfully:

- `workflow-permissions`
- `build-and-smoke-test`
- `viewport`
- `build`

The viewport job included first-screen checks for Zakat, EMI, English/Urdu flows, calorie and query calculator flows, extra calculator regressions, all calculator first-screen layouts, and screenshot capture at the configured viewports. The build job included dependency audit, syntax checks, calculator behavior/input validation, generated-page smoke checks, sitemap/internal-link checks, scoped SEO checks, HTML validation, Lighthouse SEO audits, browser console checks and safe monetization configuration.

These are results for the exact commit above. Do not assume they automatically apply to a different/newer PR head.

## Vercel preview state and reconciliation required

The latest Vercel preview deployment list included ERROR states:

- Deployment `dpl_6LUo2PJhVfBgJT3uGFYKnmVB8GnH`, branch `fix/zakat-first-screen-positioning-v3`, commit `ce40887495035c7ad5c2530643ab971d46a278cc`, state ERROR.
- Deployment `dpl_AGnPh6g9sb2G6MyQBEVmQJL7jLBQ`, branch `content/expanded-contact-page-nov-2026`, commit `fb3d451ffeeb7d36c11ad2a13a29a56dd0048e2b`, state ERROR.

The prior investigation reported a Vercel deployment rate-limit/build-rate-limit failure for PR #283. Recheck the exact deployment logs and current Vercel quota before taking action. Important: the PR metadata head SHA (`0cd568f...`) and the Vercel preview record SHA (`ce408874...`) differ. Resolve this branch/commit discrepancy before retrying deployment. Do not deploy an ambiguous or stale commit.

## Actions already taken

- Verified the target GitHub repository and Vercel project.
- Inspected the current production identifiers and selected live routes.
- Verified robots.txt and sitemap response/count.
- Inspected PR #283 metadata and workflow job step summaries.
- Did not merge PR #283.
- Did not bypass failed Vercel checks.
- Did not modify application source code or production configuration.
- Did not initiate a production deployment in this task.

## Resume procedure - continue from here

When resuming, do not repeat the full initial audit unless new evidence requires it. Start with these exact steps:

1. Fetch the latest `main` SHA and PR #283 metadata/head SHA.
2. Fetch the latest commits on `fix/zakat-first-screen-positioning-v3`.
3. Reconcile the PR head SHA with the Vercel preview deployment commit SHA. Identify which commit contains the complete intended change set.
4. Inspect the failed Vercel deployment logs and confirm whether the rate-limit/quota block has cleared.
5. If quota is available, trigger/retry a preview deployment for the exact verified PR head. Do not deploy the stale `ce408874...` commit unless it is confirmed as the current intended PR head.
6. Wait for the Vercel preview to reach READY. If it fails for another reason, diagnose that failure instead of assuming it is still a quota issue.
7. Run the complete required Playwright/browser matrix on the successful preview, including 320x568, 360x740, 390x844 and 1366x768, plus calculator route/regression checks.
8. Re-run required CI checks on the exact PR head. Confirm all required checks and Vercel deployment status are green.
9. Only then merge PR #283, if the diff remains in scope and mergeable.
10. Verify the resulting production deployment reaches READY and check the live Zakat page stylesheet query now reflects the intended cache-bust version. Recheck calculator behavior and the production URL.
11. Report exact commit SHAs, deployment IDs, check results, and any remaining risks.

## Non-negotiable safeguards

- Do not change formulas without a reproducible failing test proving a formula defect.
- Do not change existing URLs or canonical URLs without evidence and an approved redirect plan.
- Do not overwrite user changes.
- Do not merge or deploy while required checks are failing.
- Do not bypass Vercel/GitHub failures.
- Do not claim tests, simulations, Lighthouse runs, screenshots, or deployments that were not actually performed.
- Keep original test results separate from alternative verification.
- AdSense approval, indexing, rankings, traffic, and AI visibility are not guaranteed by a successful build.

## User instruction captured

The user wants this work committed to GitHub and wants deployment to continue from this saved checkpoint once the Vercel quota/rate-limit issue is cleared, without restarting the audit from zero.

This checkpoint preserves the context and next steps. It does not run a background monitor and cannot itself trigger a future deployment automatically. Resume by opening this file and following the procedure above.
