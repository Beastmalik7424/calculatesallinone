# Architecture upgrade baseline

Captured: 2026-11-14  
Baseline branch: `main`  
Baseline commit: `8b4c8fdb5fc7b4dbe15c1d7a01d8328dc482435f`  
Repository: [Beastmalik7424/calculatesallinone](https://github.com/Beastmalik7424/calculatesallinone)

## 1. Protected public contracts

The route manifest snapshot is stored in [routes.json](baseline/routes.json) and enforced by `tests/architecture-baseline-contract.py`.

| Contract | Baseline |
|---|---:|
| Indexable routes | 42 |
| Intentionally noindex routes | 5 |
| No-trailing-slash redirect exceptions | 5 |
| Vercel output directory | `public` |
| Vercel build command | `npm ci && npm run build` |

The indexable and noindex route groups are disjoint. Every no-slash exception maps to a corresponding slash-terminated canonical route. Existing formulas, page ordering/placement, DOM IDs, canonical URLs, redirects, hreflang, CSP and generated content remain protected and were not changed by Task 1.

## 2. Current architecture

- Static site generated primarily by Python. `build.py` is approximately 2,700+ lines and coordinates page generation, shell/head markup, navigation, assets, robots, sitemap and internal links.
- `seo_finalize.py` performs a second post-generation metadata, FAQ and structured-data pass.
- Specialized content/page modules already exist, including `content_v5.py`, `content_v13.py`, `lang_v6.py`, `urdu_v5.py`, `hub_page.py`, `extra_calculator_pages.py` and `calorie_calculator.py`.
- Browser behavior is primarily in `static/app.js`, approximately 2,200 lines.
- Tailwind scans a fixed list of current Python/JavaScript sources in `tailwind.config.js`. Any future module/template split must update these globs and verify the generated CSS.
- Build chain is one long `npm run build` command: Tailwind CSS, Python generation, SEO finalization and a large collection of smoke tests.

## 3. Verified technical risks

### High: main branch has no protection

GitHub's branch endpoint reported `protected: false`, `protection.enabled: false`, and required status checks disabled. This means the repository currently has no server-enforced branch protection gate. This is a release-governance risk. The available GitHub connection supports reading this setting but did not expose a branch-protection write action, so it was not changed.

### High: CI runtime is end-of-life

The workflow pins Node.js 20. The official Node.js release schedule marks Node 20 as end-of-life. Node 26 is Active LTS as of the captured date and Node 24 is Maintenance LTS. Runtime migration is deliberately deferred until compatibility is tested against the actual Vercel build environment.

Sources:
- https://nodejs.org/en/about/previous-releases
- https://github.com/nodejs/Release

### Medium: test categories are not separated

The repository has many smoke tests and browser checks, but no explicit `test:unit`, `test:integration` or `test:e2e` script contract. Existing coverage should be classified and retained before any cleanup.

### Medium: Playwright is installed ad hoc in CI

The workflow installs Playwright 1.64.1 with `npm install --no-save --package-lock=false`. This is not a lockfile-pinned project dependency and reduces reproducibility.

### Medium: build output is destructively recreated

`build.py` currently removes/recreates the `public` output directory. A later pipeline task should build into a staging directory, validate the full output and only then promote it. This is not changed in Task 1.

### Medium: site configuration has multiple sources

`build.py` reads `SITE_URL` from the environment with the production URL as fallback. `seo_finalize.py` has a hardcoded production site URL. `calorie_calculator.py` also contains a site URL literal. This creates configuration-drift risk. Consolidation is deferred until a contract test can prove URL output remains identical.

### Medium: build test commands are duplicated

Some smoke tests are run from the `build` npm script and again in CI. The duplication should be rationalized only after the current gate set is inventoried so no check is silently lost.

## 4. TDD and verification record for Task 1

New test file: `tests/architecture-baseline-contract.py`

- Unit coverage: valid canonical routes, duplicate rejection, invalid route syntax, trailing-slash rules, overlapping index/noindex groups and orphaned no-slash exceptions.
- Integration coverage: current route manifests must match the approved snapshot and Vercel's static output contract must match the snapshot.
- RED: 8 tests ran. 6 unit tests passed. 2 integration tests failed because the reviewed baseline snapshot did not yet exist. The first draft exposed one assertion failure and one unhandled missing-file error. The second test was corrected to report a clean assertion failure. The RED run was repeated and produced exactly 2 expected assertion failures.
- GREEN: after adding the reviewed snapshot, the same 8 tests passed.
- Local execution used Python 3.13 in an isolated fixture populated from the verified GitHub repository files. This is an equivalent local check, not a GitHub Actions run.
- GitHub Actions run for PR #225 was not returned by the available workflow-run lookup at report time. Therefore CI is **not claimed as passed**.

Official Python unittest reference: https://docs.python.org/3/library/unittest.html

## 5. Issues found and disposition

1. Missing architecture baseline snapshot: fixed by adding a versioned route/build contract snapshot.
2. Missing-file test error in the first test draft: fixed by asserting snapshot existence in both integration tests.
3. Main branch protection disabled: identified, not changed because the connected GitHub actions did not expose the required settings write operation.
4. Node 20 end-of-life: identified, not changed before Vercel compatibility validation.
5. Playwright not lockfile-pinned: identified, deferred to CI hardening task.
6. Build output is deleted before regeneration: identified, deferred to staging-build task.
7. Site URL duplicated across build/finalizer/calorie generator: identified, deferred to shared-config task.
8. Unit/integration/E2E categories not explicit: new contract suite starts this separation, broader test inventory remains for the next task.

## 6. Next task

Task 2: create a calculator formula regression inventory and independent reference-value tests before touching any calculator engine or page-builder logic. Then run existing build, integration and browser suites against the baseline and capture exact outputs. No production deployment until all required gates pass.
