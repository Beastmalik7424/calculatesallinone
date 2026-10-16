# Security status

## Production dependency scope

The site is generated as static HTML, CSS, JavaScript and image assets. `package.json` currently has no `dependencies` section; its npm package is a build-time development dependency. CI runs `npm audit --omit=dev --audit-level=moderate` to fail if production dependencies are introduced with known moderate-or-higher advisories.

## Build-time dependency advisory and mitigation

The upstream `braces@3.0.3` package is affected by [GHSA-vfj7-8cjw-p6xm / CVE-2026-93687](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm), and the upstream advisory currently lists no patched release. To mitigate the vulnerable recursive parser in this build-only dependency chain, `package.json` pins the dependency override to `npm:@zklogic/braces@3.0.7`, an API-compatible fork that adds a nesting-depth guard. The lockfile pins the exact tarball and its registry integrity hash.

This is a third-party compatibility fork, not an upstream `braces` release. Treat it as a deliberate risk-reduction measure rather than claiming the upstream advisory itself is closed. CI runs a nested-brace regression test, and the site does not process visitor-supplied brace patterns. Re-check the upstream advisory and the fork's maintenance/security posture before future dependency updates.

## Production dependency scope

The site is generated as static HTML, CSS, JavaScript and image assets. Its npm packages are build-time development dependencies; no npm packages are shipped as a server runtime. CI audits production dependencies and tests the generated site.
