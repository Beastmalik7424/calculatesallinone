#!/usr/bin/env python3
"""Keep the Playwright browser audit on the version-matched prebuilt image.

This prevents CI from hanging while downloading browser binaries and avoids
running apt/browser provisioning during every first-screen regression run.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/first-screen-audit.yml"
PACKAGE = ROOT / "package.json"


def validate_prebuilt_browser_image(workflow: str, package: dict) -> bool:
    version = package.get("devDependencies", {}).get("playwright")
    if not version or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        return False
    expected = f"mcr.microsoft.com/playwright:v{version}-noble"
    return (
        re.search(r"(?m)^\s*container:\s*\n\s*image:\s*" + re.escape(expected) + r"\s*$", workflow) is not None
        and "npx playwright install" not in workflow
        and "Install Chromium for locked Playwright" not in workflow
    )


class PrebuiltBrowserImageUnitTests(unittest.TestCase):
    def test_accepts_matching_versioned_image(self):
        self.assertTrue(validate_prebuilt_browser_image(
            "jobs:\n  viewport:\n    container:\n      image: mcr.microsoft.com/playwright:v1.64.1-noble\n",
            {"devDependencies": {"playwright": "1.64.1"}},
        ))

    def test_rejects_browser_image_version_drift(self):
        self.assertFalse(validate_prebuilt_browser_image(
            "jobs:\n  viewport:\n    container:\n      image: mcr.microsoft.com/playwright:v1.63.0-noble\n",
            {"devDependencies": {"playwright": "1.64.1"}},
        ))

    def test_rejects_unpinned_latest_image(self):
        self.assertFalse(validate_prebuilt_browser_image(
            "jobs:\n  viewport:\n    container:\n      image: mcr.microsoft.com/playwright:latest\n",
            {"devDependencies": {"playwright": "1.64.1"}},
        ))

    def test_rejects_redundant_browser_download(self):
        self.assertFalse(validate_prebuilt_browser_image(
            "jobs:\n  viewport:\n    container:\n      image: mcr.microsoft.com/playwright:v1.64.1-noble\n      steps:\n        - run: npx playwright install --with-deps chromium\n",
            {"devDependencies": {"playwright": "1.64.1"}},
        ))


class RepositoryBrowserWorkflowIntegrationTests(unittest.TestCase):
    def test_first_screen_workflow_uses_prebuilt_locked_browser(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        package = json.loads(PACKAGE.read_text(encoding="utf-8"))
        self.assertTrue(
            validate_prebuilt_browser_image(workflow, package),
            "first-screen-audit.yml must use the Playwright image matching package.json and must not download browsers",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
