# CalculateAllInOne Incremental Architecture Upgrade Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the existing static calculator platform into a maintainable, testable and release-safe architecture without changing user-visible calculator behavior, public URLs or the zero-backend deployment model.

**Architecture:** Retain Python static generation, Tailwind CSS, vanilla JavaScript, GitHub Actions and Vercel. Introduce a single configuration and route registry, split the large build pipeline by responsibility behind compatibility entrypoints, separate calculation engines from UI wiring where existing code permits, and make generated output atomic. Deliver each change as a small independently tested pull request.

**Tech Stack:** Python 3.12, Node.js 26 LTS (subject to Vercel compatibility verification), Tailwind CSS 3.4.19 initially, vanilla JavaScript, Playwright, GitHub Actions and Vercel static output.

## Global Constraints

- Preserve every existing public URL, trailing-slash behavior, canonical URL, redirect, sitemap membership, hreflang relationship, robots/noindex decision and structured-data contract unless a separately reviewed test-proven defect requires a change.
- Preserve calculator formulas, input IDs, result IDs, accessibility labels, interaction behavior and calculator placement. Do not rewrite formulas as part of modularization.
- Keep `build.py` and `seo_finalize.py` as compatibility entrypoints until all callers and CI jobs are proven to use the new internal interfaces.
- Keep Vercel's static output directory as `public`, the current build command contract, and current security headers/CSP/redirect rules during the initial architecture work.
- No database, server runtime, framework migration, paid service or new recurring cost is introduced by this plan.
- Do not merge to `main`, deploy production or request AdSense review while any required test, security check or release gate is failing.
- Apply TDD to behavior changes: focused failing test first, record the expected failure, minimum implementation, identical focused test passing, then affected integration tests.
- Unit tests and integration tests are mandatory for every applicable implementation task. Browser E2E and regression tests are mandatory for affected user flows.
- Use independent expected-value oracles and mathematical invariants for numeric tests. Do not verify a formula only by repeating the same formula in the test.
- Run deterministic, seeded simulation suites. Target at least 10,000 total generated cases across numeric engines and date/time boundaries, with at least 1,000 cases per applicable numeric engine. Report the exact executed count, seed, failures and skipped cases. A target is not a completed test.
- No destructive build behavior: a failed build must not leave a partially written or empty `public/` directory.
- All proposed paths below are new paths unless explicitly marked as existing. Confirm the current tree and branch head before each implementation task.

---

## Repository Baseline and Confirmed Risks

Observed on the repository default branch during the 2026-11-14 read-only audit:

- `build.py` is approximately 2,716 lines and combines page assembly, shell/head, navigation, content, sitemap, robots, assets, URL normalization and CSP-related build logic.
- `seo_finalize.py` is approximately 428 lines and post-processes generated HTML, metadata, FAQ and JSON-LD.
- `static/app.js` is approximately 2,193 lines and combines calculator interactions and UI behavior.
- Existing specialized builders and content modules already exist, including `content_v5.py`, `content_v13.py`, `lang_v6.py`, `urdu_v5.py`, `calorie_calculator.py`, `extra_calculator_pages.py` and `hub_page.py`. The upgrade must extend this partial modularity instead of replacing it wholesale.
- `build.py` uses `SITE_URL` from the environment with a production default, while `seo_finalize.py` hardcodes the production site URL. `calorie_calculator.py` also contains its own site URL literal. This creates configuration drift.
- `build.py` removes and recreates `public/` before generation completes. A failure can destroy the last complete local build output.
- `tailwind.config.js` scans a finite list of root-level Python files and `static/app.js`. A module move can silently remove generated utility classes from the CSS build.
- `package.json` has a long chained `build` script containing many smoke tests. Some tests are repeated again in CI.
- `.github/workflows/ci.yml` uses Node.js 20 and installs Playwright 1.64.1 ad hoc with `npm install --no-save --package-lock=false`.
- The CI workflow does not declare an explicit least-privilege `permissions` block.
- Existing tests cover generated output, calculator smoke behavior, content/SEO, CSP, redirects, Lighthouse and several browser flows, but there is no formal `unit`, `integration`, `e2e` and `regression` command taxonomy.
- `vercel.json` currently uses `public` as output directory and contains the live CSP, security headers and redirect rules. These are protected contracts.
- The current Tailwind configuration and package lock are tied to Tailwind CSS 3.4.19. Do not upgrade Tailwind as incidental cleanup.

## Target Architecture

The following is a proposed destination, not a statement that these directories already exist:

```text
sitegen/
  config.py                 # canonical site/build configuration
  registry.py               # route and page metadata registry
  pipeline.py               # orchestration and stage ordering
  components/
    shell.py                # shared HTML shell
    head.py                 # head/meta rendering
    navigation.py           # navigation and shared links
  pages/
    home.py                 # homepage composition
    calculator.py           # shared calculator-page composition
    category.py             # category hub composition
    static.py               # policy and informational pages
  content/
    english.py              # English content adapters
    urdu.py                 # Urdu content adapters
    locales.py              # locale metadata and translation status
    hubs.py                 # hub page content adapters
  seo/
    metadata.py             # title, description, canonical and hreflang
    schema.py               # JSON-LD assembly and validation helpers
    finalize.py             # final generated-page pass
  output/
    sitemap.py              # sitemap generation
    robots.py                # robots.txt generation
    assets.py                # static asset copy/generation
static/
  app.js                    # stable browser entrypoint during migration
  js/
    engines/                 # pure calculation functions, moved incrementally
    ui/                      # DOM adapters and interaction handlers
tests/
  unit/                      # pure functions and small module contracts
  integration/                # generator, finalizer, SEO and output contracts
  e2e/                        # real browser user journeys
  regression/                  # frozen calculator, route and page contracts
  simulations/                 # deterministic generated-input suites
docs/
  architecture/
    overview.md
    decisions/
      0001-preserve-static-stack.md
      0002-single-site-config.md
```

Root-level existing modules remain in place until a dedicated move task proves imports, Tailwind scanning, generated output and CI behavior. Do not move all content modules in one change.

### Stable interfaces

- `sitegen.config`: immutable build configuration loaded once from environment and defaults. It exposes `site_url`, `output_dir`, `static_dir`, `adsense_client`, `adsense_slot`, `adsense_consent_ready` and `contact_email`. Validate only existing documented constraints, including the numeric AdSense slot rule.
- `sitegen.registry`: ordered page records with `path`, `language`, `indexable`, `canonical`, `sitemap` and builder reference. Existing page order and generated URLs remain unchanged.
- `sitegen.pipeline.build_site(config)`: runs generation into a staging directory and publishes only after all build-stage validations pass.
- `sitegen.seo.finalize_site(root, config)`: finalizes staged HTML using the same canonical site configuration. Root `seo_finalize.py` remains a CLI-compatible wrapper.
- Browser calculation engines expose pure functions with explicit inputs and outputs. Existing DOM IDs and `static/app.js` remain the compatibility UI boundary until each engine is migrated and tested.

---

### Task 1: Freeze production contracts and establish test taxonomy

**Files:**
- Create: `tests/unit/`, `tests/integration/`, `tests/e2e/`, `tests/regression/`, `tests/simulations/` as tests are introduced.
- Create: `docs/architecture/overview.md`.
- Create: `docs/architecture/decisions/0001-preserve-static-stack.md`.
- Modify: `package.json` only to add test scripts after their commands exist.
- Inspect, do not rewrite: `tests/`, `build.py`, `seo_finalize.py`, `static/app.js`, `vercel.json`, `package-lock.json`.

**Interfaces:**
- Consumes: current build command `npm run build`, existing Python and Node smoke tests, current public route inventory and current Vercel output contract.
- Produces: a machine-readable baseline manifest for routes, canonical URLs, sitemap URLs, noindex routes, calculator DOM IDs and selected known-answer calculator fixtures. The manifest is a regression oracle, not a replacement for source definitions.

- [ ] **Step 1: Add focused baseline-contract tests**
  - Assert route inventory equality against the captured baseline.
  - Assert canonical host and trailing-slash format for every indexable route.
  - Assert sitemap uniqueness and exact current membership.
  - Assert intentional noindex routes remain noindex.
  - Assert selected calculator form/result IDs and button IDs remain present.
  - Assert current `vercel.json` output directory, redirect targets and CSP header remain unchanged.
- [ ] **Step 2: Verify the tests detect a deliberate fixture mutation**
  - Run: `python3 -m unittest discover -s tests/unit -v` after the initial test package is created.
  - Expected: the new tests fail when a fixture route, calculator ID or canonical is deliberately changed in a temporary test fixture, and pass with the unmodified baseline.
- [ ] **Step 3: Record the current baseline**
  - Run: `npm ci`, `npm run build`, `python3 tests/site-output-smoke.py`, `python3 tests/all-indexable-pages-seo-smoke.py`, `python3 tests/csp-inline-hash-smoke.py`, and existing browser suites available in CI.
  - Capture exact outputs, generated route count, sitemap count, test names and any existing failures. Do not assume historical CI status is current.
- [ ] **Step 4: Add architecture overview and ADR**
  - Document current runtime flow, existing builder modules, SEO finalizer flow, static asset flow, CI workflow, Vercel output and protected contracts.
  - Record why the static stack is retained and why framework/backend migration is out of scope.
- [ ] **Step 5: Verify baseline suite**
  - Run: `npm run build` and the exact focused regression commands above.
  - Expected: baseline manifest matches the unmodified repository output. Any pre-existing failure is recorded as baseline debt and is not silently fixed in this task.
- [ ] **Step 6: Commit the independently passing deliverable**
  - Commit message: `test: freeze current site architecture contracts`.

### Task 2: Runtime and CI supply-chain hardening

**Files:**
- Modify: `.github/workflows/ci.yml`.
- Modify: `package.json` and `package-lock.json` to pin Playwright as a development dependency.
- Create: `.nvmrc` or `.node-version` only after selecting the runtime version used by both CI and Vercel.
- Modify: `vercel.json` only if a repository-level runtime declaration is supported and required. Do not add unsupported keys.

**Interfaces:**
- Consumes: existing CI build and browser commands, current npm lockfile, current Vercel project runtime setting.
- Produces: reproducible Node and Playwright versions, explicit minimum GitHub Actions token permissions, separate test commands and one clear execution owner per test.

- [ ] **Step 1: Add CI configuration contract tests**
  - Assert CI declares explicit `permissions: contents: read` unless a specific workflow step is proven to require more.
  - Assert Node version is a supported LTS version.
  - Assert Playwright is declared in package metadata and lockfile.
  - Assert CI does not use `npm install --no-save --package-lock=false playwright...`.
  - Assert each required smoke suite has one declared owner and is not accidentally omitted from both build and CI.
- [ ] **Step 2: Verify the tests fail against the current workflow**
  - Run the focused CI contract test.
  - Expected: it identifies Node 20, missing explicit permissions and ad hoc Playwright installation in the current workflow.
- [ ] **Step 3: Verify Node 26 before selecting it**
  - Test the existing locked dependency install and full build under Node 26 LTS.
  - Run a compatibility matrix on Node 24 and Node 26 while migration is being evaluated.
  - Confirm the Vercel project build runtime setting through Vercel project settings or an actual preview build. If it cannot be read, report it as unverified and do not assume compatibility.
  - Select Node 26 only if `npm ci`, CSS build, Python site build, all smoke tests and preview deployment succeed. Otherwise use Node 24 LTS as the supported fallback and document the exact Node 26 blocker.
- [ ] **Step 4: Pin Playwright and harden CI**
  - Add the currently used Playwright version as an exact development dependency and regenerate the lockfile with the selected Node version.
  - Add explicit least-privilege workflow permissions.
  - Pin GitHub Actions to verified full commit SHAs, with comments naming the corresponding release versions. Verify the selected SHAs from official action releases before editing.
  - Separate unit, integration, E2E and regression scripts. Preserve all existing tests and avoid running the same expensive suite twice unless the second run validates a different environment.
  - Do not remove Lighthouse, HTML validation, CSP, sitemap, redirect or security checks.
- [ ] **Step 5: Verify focused and full CI behavior**
  - Run: `npm ci`, `npm run test:unit`, `npm run test:integration`, `npm run test:e2e`, `npm run test:regression`, `npm audit --audit-level=moderate`, `npm run build`.
  - Expected: all scripts execute under the chosen supported Node LTS. No test is omitted compared with the baseline.
- [ ] **Step 6: Commit the independently passing deliverable**
  - Commit message: `ci: pin supported runtime and browser test tooling`.

### Task 3: Single configuration and route registry

**Files:**
- Create: `sitegen/__init__.py`, `sitegen/config.py`, `sitegen/registry.py`.
- Modify: `build.py`, `seo_finalize.py`, `calorie_calculator.py`, and focused tests.
- Create: `tests/unit/test_site_config.py`, `tests/integration/test_route_registry.py`.

**Interfaces:**
- `load_config(environ=None) -> SiteConfig`.
- `SiteConfig.site_url`, `output_dir`, `static_dir`, `adsense_client`, `adsense_slot`, `adsense_consent_ready`, `contact_email`.
- `PageRoute(path, language, indexable, canonical, sitemap, builder)`.
- `get_routes() -> tuple[PageRoute, ...]`.

- [ ] **Step 1: Add failing config and route tests**
  - Same environment input must produce the same normalized site URL for the build generator, SEO finalizer and calorie page.
  - Missing `SITE_URL` must use the current production default.
  - A supplied site URL with a trailing slash must produce one canonical base without a duplicate slash.
  - Existing AdSense slot validation must remain digits-only.
  - Route order, indexability, canonical paths and sitemap membership must match the baseline manifest exactly.
- [ ] **Step 2: Verify expected red**
  - Run: `python3 -m unittest tests.unit.test_site_config tests.integration.test_route_registry -v`.
  - Expected: current duplicated URL literals and missing shared registry fail the new contract tests.
- [ ] **Step 3: Implement shared configuration and registry**
  - Move only configuration values and route metadata first. Do not move page builders in this task.
  - Make `build.py` consume `SiteConfig`.
  - Make `seo_finalize.py` consume the same `site_url` while preserving its existing CLI invocation.
  - Pass the same configuration to the calorie page builder rather than maintaining a third production URL literal.
  - Populate the registry from the verified existing generated route inventory. Preserve route order and indexability exactly.
- [ ] **Step 4: Verify focused green**
  - Run the two focused test modules.
  - Expected: shared URL values and route inventory match the captured baseline.
- [ ] **Step 5: Run integration and output regression**
  - Run: `npm run build`, `python3 tests/site-output-smoke.py`, `python3 tests/all-indexable-pages-seo-smoke.py`, `python3 tests/internal-link-canonical-smoke.py`, `python3 tests/csp-inline-hash-smoke.py`.
  - Expected: generated canonical tags, sitemap, robots, noindex directives, schema and CSP remain equivalent to baseline.
- [ ] **Step 6: Commit the independently passing deliverable**
  - Commit message: `refactor: centralize site configuration and route metadata`.

### Task 4: Safe staged build and pipeline boundaries

**Files:**
- Create: `sitegen/pipeline.py`, `sitegen/output/assets.py`, `sitegen/output/sitemap.py`, `sitegen/output/robots.py`.
- Modify: `build.py`, `seo_finalize.py`.
- Create: `tests/unit/test_staging_publish.py`, `tests/integration/test_build_pipeline.py`.

**Interfaces:**
- `build_site(config) -> BuildResult`.
- `finalize_site(root, config) -> FinalizeResult`.
- Existing root CLI entrypoints preserve current invocation and exit behavior.

- [ ] **Step 1: Add failing staging and pipeline tests**
  - A successful build publishes a complete output containing expected homepage, assets, sitemap and robots files.
  - A generation exception leaves the previous `public/` directory byte-for-byte intact.
  - A finalization exception leaves the previous `public/` directory intact.
  - Temporary staging directories are cleaned after success and failure.
  - A missing required generated page fails before publishing.
  - No partially written output is treated as a successful build.
- [ ] **Step 2: Verify expected red**
  - Run: `python3 -m unittest tests.unit.test_staging_publish tests.integration.test_build_pipeline -v`.
  - Expected: current delete-and-recreate behavior fails the preservation-on-error assertion.
- [ ] **Step 3: Implement staging output**
  - Generate into a sibling temporary directory on the same filesystem as `public/`.
  - Run all build-stage and SEO finalization checks against staging.
  - Publish only after validation succeeds, using a backup-and-rename sequence with rollback if replacement fails.
  - Keep the existing `public/` directory intact until the new output is fully validated.
  - Preserve generated relative asset paths and Vercel output path.
- [ ] **Step 4: Verify focused green**
  - Run the same unit and integration tests.
  - Expected: previous output survives injected generation/finalization failures and a successful build replaces it completely.
- [ ] **Step 5: Run complete build and production-contract checks**
  - Run: `npm run build`, `python3 tests/site-output-smoke.py`, `python3 tests/csp-inline-hash-smoke.py`, `python3 tests/vercel-redirect-config-smoke.py`.
  - Expected: same route inventory and public output contract as baseline.
- [ ] **Step 6: Commit the independently passing deliverable**
  - Commit message: `build: publish validated site output atomically`.

### Task 5: Incremental Python generator modularization

**Files:**
- Create: proposed modules under `sitegen/components/`, `sitegen/pages/`, `sitegen/seo/` and `sitegen/output/`.
- Modify: `build.py`, `seo_finalize.py`, `tailwind.config.js`.
- Add focused tests under `tests/unit/` and `tests/integration/`.

**Interfaces:**
- Existing root builder functions remain import-compatible wrappers during migration.
- Each extracted module has one responsibility and receives configuration and dependencies explicitly.
- The page registry owns route metadata. Individual page builders own page body composition. SEO helpers own metadata/schema transformations. Output modules own sitemap, robots and assets.

- [ ] **Step 1: Add behavior-preservation tests for the first extraction**
  - Compare generated page body, title, description, canonical, hreflang, JSON-LD and relevant CSS class presence before and after extracting one shared component.
  - Include English, Urdu, one noindex locale and one calculator route.
- [ ] **Step 2: Verify expected red**
  - Run the focused extraction test before moving implementation.
  - Expected: the test identifies the missing module interface or changed output snapshot, not an import/setup error.
- [ ] **Step 3: Extract one responsibility at a time**
  - Recommended order: shared head/shell helpers, navigation, sitemap/robots, metadata/schema helpers, then page-type composition.
  - Keep content modules in their current locations initially. Adapt them through imports rather than bulk-moving them.
  - Update Tailwind globs to include the new source modules and all currently active source files. Add a test that checks representative generated utility classes exist in the built CSS.
  - Avoid circular imports. Configuration and shared data flow downward; page builders must not import the top-level pipeline.
- [ ] **Step 4: Verify focused green**
  - Run the same focused tests after every extraction.
  - Expected: output contracts and required CSS selectors remain unchanged.
- [ ] **Step 5: Run full integration and E2E checks**
  - Run: `npm run build`, `npm run test:integration`, `npm run test:e2e`, `npm run test:regression`.
  - Expected: all existing pages, calculator controls, language variants, schema, sitemap, robots and CSP pass.
- [ ] **Step 6: Commit each independently passing extraction**
  - Commit message format: `refactor: extract <single responsibility> from site builder`.

### Task 6: Incremental browser engine separation and deterministic simulation

**Files:**
- Create: `static/js/engines/` and `static/js/ui/` modules only for engines proven separable.
- Modify: `static/app.js` as a compatibility entrypoint, relevant page script loading and CSP tests.
- Create: `tests/unit/` engine tests and `tests/simulations/` deterministic generated-case suites.

**Interfaces:**
- Pure engine functions accept explicit primitive inputs and return explicit result objects without reading or writing the DOM.
- UI adapters own DOM lookup, input validation presentation, event binding, formatting and accessibility announcements.
- Existing DOM IDs, output wording, rounding and error behavior remain stable unless a separately approved defect is proven.

- [ ] **Step 1: Select one engine and add failing behavior tests**
  - Start with a low-coupling engine only after inspecting its current function and call sites.
  - Add known-answer cases, zero/boundary cases, invalid/non-finite inputs, precision cases and independent invariants.
- [ ] **Step 2: Verify expected red**
  - Run the focused engine test.
  - Expected: the new pure interface is missing or the specific contract is not yet met.
- [ ] **Step 3: Extract the minimum pure function**
  - Keep the old UI handler behavior and DOM IDs.
  - Preserve exact formula, rounding and validation semantics.
  - Do not convert all of `app.js` into ES modules until script ordering, inline scripts, CSP hashes and browser support are verified.
- [ ] **Step 4: Verify focused green and simulations**
  - Run focused unit tests and deterministic generated cases with fixed, recorded seeds.
  - Target at least 1,000 generated cases per applicable numeric engine. Use independently computed reference values, dimensional checks, inverse-operation checks where mathematically valid, monotonicity and boundary invariants.
  - For date/time engines, include leap years, 29 February, month ends, year boundaries, reversed dates, daylight-saving-independent date parsing and invalid dates as relevant to current behavior.
  - Record exact counts, seed, runtime, failed cases and reproduction inputs.
- [ ] **Step 5: Run integration and real-browser E2E**
  - Run: `npm run test:integration`, `npm run test:e2e`, `npm run test:regression`, `python3 tests/csp-inline-hash-smoke.py`.
  - Verify calculator keyboard use, mouse/touch interaction, invalid-input feedback, result announcements and no console errors in supported browser contexts.
- [ ] **Step 6: Commit the independently passing engine**
  - Commit message: `refactor: isolate <engine> calculation logic`.

---

## Release Gates

A task is complete only when all gates relevant to that task pass and the evidence is recorded.

1. **Unit:** focused pure-function and configuration tests pass.
2. **Integration:** generation, finalization, routes, metadata, sitemap, robots, schema, CSP and assets pass.
3. **E2E:** real browser interactions pass for all affected user flows.
4. **Regression:** route manifest, formula fixtures, calculator IDs, page placement and protected Vercel configuration match baseline.
5. **Simulation:** deterministic generated cases run at the documented count and seed. Report actual results, not targets.
6. **Security:** `npm audit --audit-level=moderate`, least-privilege workflow permissions, verified action SHA pins and CSP checks pass.
7. **Build:** clean `npm ci` and `npm run build` succeed in the selected runtime.
8. **Preview:** Vercel preview build is READY and all affected public URLs return expected HTML, metadata and assets.
9. **Production:** only after explicit release approval, verify the production deployment, aliases, representative calculator flows, redirects and sitemap. No production change is authorized merely by a passing preview.

Do not describe a gate as passing unless its command or online equivalent was actually executed and its result captured.

## Failure Register to Maintain During Execution

For every task, record each failure with: identifier, affected file/route/engine, exact reproduction command or input, expected result, actual result, root cause, fix, regression test and final status. Keep pre-existing failures separate from newly introduced regressions. Do not suppress, skip or weaken assertions to obtain a green run.

## Research Basis

- Node.js release status: Node.js 26 is Active LTS from 2026-10-28 and Node.js 20 is EOL. Verify the live release schedule again at implementation time: https://github.com/nodejs/Release
- Node.js EOL policy explains that EOL releases no longer receive vulnerability fixes: https://nodejs.org/en/about/eol
- Playwright best practices recommend user-visible assertions, isolated tests and web-first assertions: https://playwright.dev/docs/best-practices
- Playwright browser contexts provide isolated storage/cookies per test: https://playwright.dev/docs/browser-contexts
- GitHub Actions security guidance should be followed for least privilege and action pinning: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions

## Unresolved External Decisions

- Confirm the actual Vercel project Node build-runtime setting before choosing Node 26. The repository workflow alone does not prove Vercel's runtime setting.
- Confirm the supported production browser matrix before making any module-format or script-loading change.
- Confirm whether the existing CI branch triggers and required-check names are relied on by branch protection. Branch protection was not exposed by the inspected repository tools.
- Decide whether the route registry is generated from existing builders or maintained as a single explicit ordered list after the baseline inventory demonstrates which model avoids duplicated route declarations.
- Confirm whether exact byte-for-byte HTML snapshots are appropriate for all pages. Prefer semantic contracts for volatile timestamps or generated asset hashes while preserving exact URL and metadata assertions.
