# Security status

## Production dependency scope

The site is generated as static HTML, CSS, JavaScript and image assets. `package.json` currently has no `dependencies` section; its npm package is a build-time development dependency. CI runs `npm audit --omit=dev --audit-level=moderate` to fail if production dependencies are introduced with known moderate-or-higher advisories.

## Build-time dependency advisory

The build dependency tree currently includes `braces@3.0.3` through the Tailwind CSS v3 toolchain. GitHub Advisory Database GHSA-vfj7-8cjw-p6xm currently marks versions through 3.0.3 as affected and lists no patched version. The project upgraded Tailwind CSS to 3.4.19 and its transitive `sucrase` and `postcss` dependencies, and keeps Tailwind major upgrades blocked until a v4 migration can be tested. Do not claim the entire development dependency tree is vulnerability-free while the upstream `braces` advisory remains unresolved.

The affected package is used in the build toolchain, not as a deployed server dependency. The site is statically generated, and the build does not process visitor-supplied brace patterns. Keep CI and Dependabot enabled and re-check the advisory for an upstream fix.

Reference: https://github.com/advisories/GHSA-vfj7-8cjw-p6xm
