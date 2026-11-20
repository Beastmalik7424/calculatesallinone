#!/usr/bin/env python3
"""Protect the lockfile-pinned Playwright CI dependency and browser install contract."""
import json
import random
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXACT_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SHA512_INTEGRITY = re.compile(r"^sha512-[A-Za-z0-9+/]{86}==$")


def validate_playwright_config(config):
    playwright_versions = [
        config.get("manifest_version"),
        config.get("lock_root_version"),
        config.get("playwright_package_version"),
        config.get("playwright_core_version"),
        config.get("playwright_core_dependency"),
    ]
    axe_versions = [
        config.get("axe_manifest_version"),
        config.get("axe_lock_root_version"),
        config.get("axe_package_version"),
    ]
    integrities = [
        config.get("playwright_integrity"),
        config.get("core_integrity"),
        config.get("axe_integrity"),
    ]
    return (
        all(isinstance(value, str) and EXACT_SEMVER.fullmatch(value) for value in playwright_versions)
        and len(set(playwright_versions)) == 1
        and all(isinstance(value, str) and EXACT_SEMVER.fullmatch(value) for value in axe_versions)
        and len(set(axe_versions)) == 1
        and all(isinstance(value, str) and SHA512_INTEGRITY.fullmatch(value) for value in integrities)
        and config.get("ci_uses_npm_ci") is True
        and config.get("ci_has_no_ad_hoc_install") is True
        and config.get("ci_installs_chromium") is True
        and config.get("first_screen_installs_locked_chromium") is True
    )

def repository_playwright_config(root=ROOT):
    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
    ci = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    playwright_lock = lock.get("packages", {}).get("node_modules/playwright", {})
    core_lock = lock.get("packages", {}).get("node_modules/playwright-core", {})
    axe_lock = lock.get("packages", {}).get("node_modules/axe-core", {})
    site_build = (root / ".github/workflows/site-build.yml").read_text(encoding="utf-8")
    first_screen = (root / ".github/workflows/first-screen-audit.yml").read_text(encoding="utf-8")
    workflows = ci + "\\n" + site_build + "\\n" + first_screen
    return {
        "manifest_version": package.get("devDependencies", {}).get("playwright"),
        "lock_root_version": lock.get("packages", {}).get("", {}).get("devDependencies", {}).get("playwright"),
        "playwright_package_version": playwright_lock.get("version"),
        "playwright_core_version": core_lock.get("version"),
        "playwright_core_dependency": playwright_lock.get("dependencies", {}).get("playwright-core"),
        "playwright_integrity": playwright_lock.get("integrity"),
        "core_integrity": core_lock.get("integrity"),
        "axe_manifest_version": package.get("devDependencies", {}).get("axe-core"),
        "axe_lock_root_version": lock.get("packages", {}).get("", {}).get("devDependencies", {}).get("axe-core"),
        "axe_package_version": axe_lock.get("version"),
        "axe_integrity": axe_lock.get("integrity"),
        "ci_uses_npm_ci": all("run: npm ci" in workflow for workflow in (ci, site_build, first_screen)),
        "ci_has_no_ad_hoc_install": "npm install --no-save" not in workflows,
        "ci_installs_chromium": "npx playwright install chromium" in ci and "npx playwright install --with-deps chromium" not in ci,
        "first_screen_installs_locked_chromium": "npx playwright install chromium" in first_screen and "npx playwright install --with-deps chromium" not in first_screen,
    }


class PlaywrightLockUnitTests(unittest.TestCase):
    def valid_config(self):
        return {
            "manifest_version": "1.64.1",
            "lock_root_version": "1.64.1",
            "playwright_package_version": "1.64.1",
            "playwright_core_version": "1.64.1",
            "playwright_core_dependency": "1.64.1",
            "playwright_integrity": "sha512-HCrVhHr5QQuwYoswEUGTb7gGp522yflbv/ST8nF4sFWGuLjQCt17Q/EubpGGSNKYn1tsTCPZxqHhHCfVURu7UA==",
            "core_integrity": "sha512-BC4s8y6SEVA6Q1rSxZTto8hI1KUI3xXlHGZgvGqP4IqPdI/a6FX9H29IDNz7vKo9l21b6LfYosScPL6M3xxyDQ==",
            "axe_manifest_version": "4.13.0",
            "axe_lock_root_version": "4.13.0",
            "axe_package_version": "4.13.0",
            "axe_integrity": "sha512-UzGt8zg7Ny8djbYMhxl2zuEevVa7r2gJjYY5Lwr1xM7+XU2nd6CkIWFTVcCIbAP63vSz71NaVyyuSk9lHKcy0A==",
            "ci_uses_npm_ci": True,
            "ci_has_no_ad_hoc_install": True,
            "ci_installs_chromium": True,
            "first_screen_installs_locked_chromium": True,
        }

    def test_accepts_exact_locked_playwright_version(self):
        self.assertTrue(validate_playwright_config(self.valid_config()))

    def test_accepts_reviewed_exact_dependency_version_bumps(self):
        axe_bump = self.valid_config()
        axe_bump.update({
            "axe_manifest_version": "4.14.1",
            "axe_lock_root_version": "4.14.1",
            "axe_package_version": "4.14.1",
            "axe_integrity": "sha512-FHfa+lmNjQZfJz1q8wKqIDwC6DExcHt/pkjNQb09a3NPjCKg2rhu5qb2S4r76ASyFNNtuFooJpZe37OgudVGtQ==",
        })
        self.assertTrue(validate_playwright_config(axe_bump), "a reviewed exact axe-core update must be accepted")

        playwright_bump = self.valid_config()
        playwright_bump.update({
            "manifest_version": "1.65.1",
            "lock_root_version": "1.65.1",
            "playwright_package_version": "1.65.1",
            "playwright_core_version": "1.65.1",
            "playwright_core_dependency": "1.65.1",
            "playwright_integrity": "sha512-vJ1FuoOrNwOKHUIVEvSt3jT1L+wjjDpwhwIstKtfvTh8XIG4FG4bIFuvNdMxi81LGfAhUgUZleVFaOLY4RIUUw==",
            "core_integrity": "sha512-hqPpz7blSMPxWVdoeE1yiBSzXsKiVOd2k+kjCvmUywD2GPO2Dd9HfcWnq9NN0GHbNZDFgZ9JfBFr+X5/BLo0qw==",
        })
        self.assertTrue(validate_playwright_config(playwright_bump), "a reviewed exact Playwright update must be accepted")

        both_bumped = dict(axe_bump)
        both_bumped.update(playwright_bump)
        self.assertTrue(validate_playwright_config(both_bumped), "both reviewed exact updates must be accepted")

    def test_rejects_version_drift_in_each_lockfile_layer(self):
        valid = self.valid_config()
        version_keys = [
            "manifest_version", "lock_root_version", "playwright_package_version",
            "playwright_core_version", "playwright_core_dependency",
            "axe_manifest_version", "axe_lock_root_version", "axe_package_version",
        ]
        for key in version_keys:
            with self.subTest(key=key):
                mutated = dict(valid)
                mutated[key] = "1.65.0"
                self.assertFalse(validate_playwright_config(mutated))

    def test_rejects_ad_hoc_npm_install(self):
        config = self.valid_config()
        config["ci_has_no_ad_hoc_install"] = False
        self.assertFalse(validate_playwright_config(config))

    def test_rejects_tampered_package_integrity(self):
        for key in ("playwright_integrity", "core_integrity", "axe_integrity"):
            with self.subTest(key=key):
                config = self.valid_config()
                config[key] = "sha512-invalid"
                self.assertFalse(validate_playwright_config(config))

    def test_rejects_missing_browser_install(self):
        config = self.valid_config()
        config["ci_installs_chromium"] = False
        self.assertFalse(validate_playwright_config(config))

    def test_rejects_missing_locked_chromium_install(self):
        config = self.valid_config()
        config["first_screen_installs_locked_chromium"] = False
        self.assertFalse(validate_playwright_config(config))

    def test_two_thousand_deterministic_lockfile_mutations(self):
        rng = random.Random(20261114)
        valid = self.valid_config()
        version_keys = [
            "manifest_version", "lock_root_version", "playwright_package_version",
            "playwright_core_version", "playwright_core_dependency",
            "axe_manifest_version", "axe_lock_root_version", "axe_package_version",
        ]
        invalid_versions = ["1.63.0", "1.64.0", "1.65.0", "latest", "^1.64.1", "~1.64.1", ">=1.64.1", "1.64"]
        for _ in range(1000):
            self.assertTrue(validate_playwright_config(dict(valid)))
        for _ in range(1000):
            mutated = dict(valid)
            key = rng.choice(version_keys)
            mutated[key] = rng.choice(invalid_versions)
            self.assertFalse(validate_playwright_config(mutated), "version drift must be rejected: " + key)


class RepositoryPlaywrightIntegrationTests(unittest.TestCase):
    def test_manifest_lockfile_and_ci_are_consistent(self):
        config = repository_playwright_config()
        self.assertTrue(
            validate_playwright_config(config),
            "Playwright must be exact-version pinned in package.json and package-lock, "
            "and CI must use npm ci plus the locked local CLI. Actual: "
            + json.dumps(config, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
