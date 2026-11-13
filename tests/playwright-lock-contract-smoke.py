#!/usr/bin/env python3
"""Protect the lockfile-pinned Playwright CI dependency and browser install contract."""
import json
import random
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYWRIGHT_VERSION = "1.64.1"


def validate_playwright_config(config):
    return (
        config.get("manifest_version") == PLAYWRIGHT_VERSION
        and config.get("lock_root_version") == PLAYWRIGHT_VERSION
        and config.get("playwright_package_version") == PLAYWRIGHT_VERSION
        and config.get("playwright_core_version") == PLAYWRIGHT_VERSION
        and config.get("playwright_core_dependency") == PLAYWRIGHT_VERSION
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
    return {
        "manifest_version": package.get("devDependencies", {}).get("playwright"),
        "lock_root_version": lock.get("packages", {}).get("", {}).get("devDependencies", {}).get("playwright"),
        "playwright_package_version": playwright_lock.get("version"),
        "playwright_core_version": core_lock.get("version"),
        "playwright_core_dependency": playwright_lock.get("dependencies", {}).get("playwright-core"),
        "ci_uses_npm_ci": "run: npm ci" in ci,
        "ci_has_no_ad_hoc_install": "npm install --no-save --package-lock=false playwright" not in ci,
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
