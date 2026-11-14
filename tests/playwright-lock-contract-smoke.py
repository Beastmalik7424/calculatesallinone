#!/usr/bin/env python3
"""Protect the lockfile-pinned Playwright CI dependency and browser install contract."""
import json
import random
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYWRIGHT_VERSION = "1.64.1"
PLAYWRIGHT_INTEGRITY = "sha512-HCrVhHr5QQuwYoswEUGTb7gGp522yflbv/ST8nF4sFWGuLjQCt17Q/EubpGGSNKYn1tsTCPZxqHhHCfVURu7UA=="
CORE_INTEGRITY = "sha512-BC4s8y6SEVA6Q1rSxZTto8hI1KUI3xXlHGZgvGqP4IqPdI/a6FX9H29IDNz7vKo9l21b6LfYosScPL6M3xxyDQ=="
AXE_VERSION = "4.13.0"
AXE_INTEGRITY = "sha512-UzGt8zg7Ny8djbYMhxl2zuEevVa7r2gJjYY5Lwr1xM7+XU2nd6CkIWFTVcCIbAP63vSz71NaVyyuSk9lHKcy0A=="


def validate_playwright_config(config):
    return (
        config.get("manifest_version") == PLAYWRIGHT_VERSION
        and config.get("lock_root_version") == PLAYWRIGHT_VERSION
        and config.get("playwright_package_version") == PLAYWRIGHT_VERSION
        and config.get("playwright_core_version") == PLAYWRIGHT_VERSION
        and config.get("playwright_core_dependency") == PLAYWRIGHT_VERSION
        and config.get("playwright_integrity") == PLAYWRIGHT_INTEGRITY
        and config.get("core_integrity") == CORE_INTEGRITY
        and config.get("axe_manifest_version") == AXE_VERSION
        and config.get("axe_lock_root_version") == AXE_VERSION
        and config.get("axe_package_version") == AXE_VERSION
        and config.get("axe_integrity") == AXE_INTEGRITY
        and config.get("ci_uses_npm_ci") is True
        and config.get("ci_has_no_ad_hoc_install") is True
        and config.get("ci_installs_chromium") is True
    )


def repository_playwright_config(root=ROOT):
    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
    ci = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    playwright_lock = lock.get("packages", {}).get("node_modules/playwright", {})
    core_lock = lock.get("packages", {}).get("node_modules/playwright-core", {})
    axe_lock = lock.get("packages", {}).get("node_modules/axe-core", {})
    site_build = (root / ".github/workflows/site-build.yml").read_text(encoding="utf-8")
    workflows = ci + "\\n" + site_build
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
        "ci_uses_npm_ci": "run: npm ci" in ci and "run: npm ci" in site_build,
        "ci_has_no_ad_hoc_install": "npm install --no-save --package-lock=false" not in workflows,
        "ci_installs_chromium": "npx playwright install --with-deps chromium" in ci,
    }


class PlaywrightLockUnitTests(unittest.TestCase):
    def valid_config(self):
        return {
            "manifest_version": PLAYWRIGHT_VERSION,
            "lock_root_version": PLAYWRIGHT_VERSION,
            "playwright_package_version": PLAYWRIGHT_VERSION,
            "playwright_core_version": PLAYWRIGHT_VERSION,
            "playwright_core_dependency": PLAYWRIGHT_VERSION,
            "playwright_integrity": PLAYWRIGHT_INTEGRITY,
            "core_integrity": CORE_INTEGRITY,
            "axe_manifest_version": AXE_VERSION,
            "axe_lock_root_version": AXE_VERSION,
            "axe_package_version": AXE_VERSION,
            "axe_integrity": AXE_INTEGRITY,
            "ci_uses_npm_ci": True,
            "ci_has_no_ad_hoc_install": True,
            "ci_installs_chromium": True,
        }

    def test_accepts_exact_locked_playwright_version(self):
        self.assertTrue(validate_playwright_config(self.valid_config()))

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

    def test_two_thousand_deterministic_lockfile_mutations(self):
        rng = random.Random(20261114)
        valid = self.valid_config()
        version_keys = [
            "manifest_version", "lock_root_version", "playwright_package_version",
            "playwright_core_version", "playwright_core_dependency",
            "axe_manifest_version", "axe_lock_root_version", "axe_package_version",
        ]
        invalid_versions = ["1.63.0", "1.64.0", "1.65.0", "latest", "^1.64.1", "1.64.1-beta"]
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
