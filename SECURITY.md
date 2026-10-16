# Security status

## Dependency scope

The site is generated as static HTML, CSS, JavaScript and image assets. npm packages are used during the build, not shipped as a server runtime. CI audits dependencies and tests the generated output.

## Build-time dependency advisory and mitigation

The upstream `braces@3.0.3` package is tracked against [GHSA-vfj7-8cjw-p6xm / CVE-2026-93687](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm). The lockfile overrides the `braces` dependency with the API-compatible `@zklogic/braces@3.0.7` fork, which adds a nesting-depth guard, and pins the exact package integrity hash.

This is a third-party compatibility fork, not an upstream `braces` patch. Treat it as risk reduction, not proof that the upstream advisory is closed. CI includes a nested-brace regression test. The site does not process visitor-supplied brace patterns. Re-check the upstream advisory and the fork's maintenance/security posture before dependency updates.

## PostCSS selector parser advisory

The build dependency tree pins `postcss-selector-parser@7.1.6`, the upstream release containing the fix for [GHSA-rj75-hqrm-r3gf](https://github.com/advisories/GHSA-rj75-hqrm-r3gf). The lockfile records the registry tarball and integrity hash. CI runs a blocking full-tree `npm audit --audit-level=moderate` check and build/output regression tests.

## Reporting

Report suspected vulnerabilities privately to the repository owner before publicly disclosing details. Do not include secrets or personal data in public issues.
