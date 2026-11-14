#!/usr/bin/env python3
"""Unit and integration contracts keeping local, CI and Vercel Node/Python runtimes aligned."""
import json
import random
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NVMRC = "24"
EXPECTED_ENGINE = "24.x"
EXPECTED_WORKFLOW_NODE = "24"
EXPECTED_PYTHON = "3.12"
SETUP_NODE_SHA = "949feb2413d6458794dcd2491c4babbbce0c15c1"
SETUP_PYTHON_SHA = "6d4fd22b20465ccc0f7354476588e8df7c9ca0e0"


def validate_runtime_config(config):
    expected = {
        "nvmrc": EXPECTED_NVMRC,
        "package_engine": EXPECTED_ENGINE,
        "lock_engine": EXPECTED_ENGINE,
        "ci_node": EXPECTED_WORKFLOW_NODE,
        "site_build_node": EXPECTED_WORKFLOW_NODE,
        "first_screen_node": EXPECTED_WORKFLOW_NODE,
        "ci_python": EXPECTED_PYTHON,
        "site_build_python": EXPECTED_PYTHON,
        "first_screen_python": EXPECTED_PYTHON,
        "preview_fallback_node": EXPECTED_WORKFLOW_NODE,
        "preview_fallback_python": EXPECTED_PYTHON,
    }
    return all(config.get(key) == value for key, value in expected.items())


def workflow_node_version(content):
    matches = re.findall(
        r"uses:\s*actions/setup-node@v7\s*\n\s*with:\s*\n\s*node-version:\s*[\"']?([^\"'\s]+)",
        content,
    )
    if len(matches) != 1:
        raise ValueError("workflow must define exactly one setup-node@v7 Node version")
    return matches[0]


def workflow_python_version(content):
    matches = re.findall(
        r"uses:\s*actions/setup-python@v7\s*\n\s*with:\s*\n\s*python-version:\s*[\"']?([^\"'\s]+)",
        content,
    )
    if len(matches) != 1:
        raise ValueError("workflow must define exactly one setup-python@v7 Python version")
    return matches[0]


def repository_runtime_config(root=ROOT):
    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
    nvmrc_path = root / ".nvmrc"
    nvmrc = nvmrc_path.read_text(encoding="utf-8").strip() if nvmrc_path.is_file() else None
    ci = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    site_build = (root / ".github/workflows/site-build.yml").read_text(encoding="utf-8")
    first_screen = (root / ".github/workflows/first-screen-audit.yml").read_text(encoding="utf-8")
    preview_fallback = (root / ".github/workflows/vercel-preview-fallback.yml").read_text(encoding="utf-8")
    return {
        "nvmrc": nvmrc,
        "package_engine": package.get("engines", {}).get("node"),
        "lock_engine": lock.get("packages", {}).get("", {}).get("engines", {}).get("node"),
        "ci_node": workflow_node_version(ci),
        "site_build_node": workflow_node_version(site_build),
        "first_screen_node": workflow_node_version(first_screen),
        "ci_python": workflow_python_version(ci),
        "site_build_python": workflow_python_version(site_build),
        "first_screen_python": workflow_python_version(first_screen),
        "preview_fallback_node": workflow_node_version(preview_fallback),
        "preview_fallback_python": workflow_python_version(preview_fallback),
    }


class RuntimeContractUnitTests(unittest.TestCase):
    def valid_config(self):
        return {
            "nvmrc": "24",
            "package_engine": "24.x",
            "lock_engine": "24.x",
            "ci_node": "24",
            "site_build_node": "24",
            "first_screen_node": "24",
            "ci_python": "3.12",
            "site_build_python": "3.12",
            "first_screen_python": "3.12",
            "preview_fallback_node": "24",
            "preview_fallback_python": "3.12",
        }

    def test_accepts_a_fully_aligned_node_24_python_312_configuration(self):
        self.assertTrue(validate_runtime_config(self.valid_config()))

    def test_rejects_each_runtime_source_when_it_drifts(self):
        valid = self.valid_config()
        for key in valid:
            with self.subTest(source=key):
                drifted = dict(valid)
                drifted[key] = "20"
                self.assertFalse(validate_runtime_config(drifted), key + " must not drift")

    def test_rejects_missing_runtime_declaration(self):
        self.assertFalse(validate_runtime_config({}))

    def test_accepts_sha_pinned_setup_node_action(self):
        content = f"uses: actions/setup-node@{SETUP_NODE_SHA} # v7\\nwith:\\n  node-version: '24'\\n"
        self.assertEqual(workflow_node_version(content), "24")

    def test_rejects_mutable_setup_node_tag(self):
        content = "uses: actions/setup-node@v7\\nwith:\\n  node-version: '24'\\n"
        with self.assertRaisesRegex(ValueError, "exactly one"):
            workflow_node_version(content)

    def test_rejects_workflow_with_duplicate_node_setup_versions(self):
        content = (
            f"uses: actions/setup-node@{SETUP_NODE_SHA} # v7\\n  with:\\n    node-version: \"24\"\\n"
            f"uses: actions/setup-node@{SETUP_NODE_SHA} # v7\\n  with:\\n    node-version: \"20\"\\n"
        )
        with self.assertRaisesRegex(ValueError, "exactly one"):
            workflow_node_version(content)

    def test_accepts_sha_pinned_setup_python_action(self):
        content = f"uses: actions/setup-python@{SETUP_PYTHON_SHA} # v7\\nwith:\\n  python-version: '3.12'\\n"
        self.assertEqual(workflow_python_version(content), "3.12")

    def test_rejects_mutable_setup_python_tag(self):
        content = "uses: actions/setup-python@v7\\nwith:\\n  python-version: '3.12'\\n"
        with self.assertRaisesRegex(ValueError, "exactly one"):
            workflow_python_version(content)

    def test_rejects_workflow_with_duplicate_python_setup_versions(self):
        content = (
            f"uses: actions/setup-python@{SETUP_PYTHON_SHA} # v7\\n  with:\\n    python-version: \"3.12\"\\n"
            f"uses: actions/setup-python@{SETUP_PYTHON_SHA} # v7\\n  with:\\n    python-version: \"3.11\"\\n"
        )
        with self.assertRaisesRegex(ValueError, "exactly one"):
            workflow_python_version(content)

    def test_two_thousand_deterministic_runtime_mutations(self):
        rng = random.Random(20261114)
        valid = self.valid_config()
        invalid_versions = ["18", "20", "22", "26", "24.11.0", "lts/*", "node"]
        for _ in range(1000):
            self.assertTrue(validate_runtime_config(dict(valid)))
        for _ in range(1000):
            mutated = dict(valid)
            key = rng.choice(list(valid))
            bad = rng.choice(invalid_versions)
            while bad == valid[key]:
                bad = rng.choice(invalid_versions)
            mutated[key] = bad
            self.assertFalse(validate_runtime_config(mutated), "runtime drift must be rejected: " + key)


class RepositoryRuntimeIntegrationTests(unittest.TestCase):
    def test_local_package_lock_and_all_runtime_workflows_target_node_24_and_python_312(self):
        config = repository_runtime_config()
        self.assertTrue(
            validate_runtime_config(config),
            "runtime mismatch. Expected .nvmrc=24, package.json/package-lock engines.node=24.x, "
            "all CI and preview-fallback Node versions=24 and Python versions=3.12. Actual: "
            + json.dumps(config, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
