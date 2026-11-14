#!/usr/bin/env python3
"""Unit and integration contracts for least-privilege GitHub Actions permissions.

Every workflow must grant only the read-only repository permission it needs.
No workflow or job may override that policy with write access.
"""
import random
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = (
    ".github/workflows/ci.yml",
    ".github/workflows/site-build.yml",
    ".github/workflows/first-screen-audit.yml",
    ".github/workflows/vercel-preview-fallback.yml",
    ".github/workflows/workflow-security.yml",
)
EXPECTED = {"contents": "read"}


def parse_top_level_permissions(content):
    lines = content.splitlines()
    starts = [index for index, line in enumerate(lines) if re.fullmatch(r"permissions:\s*", line)]
    if len(starts) != 1:
        return None
    if any(re.match(r"^\s{2,}permissions\s*:", line) for line in lines):
        return None

    permissions = {}
    for line in lines[starts[0] + 1:]:
        if not line.strip():
            continue
        if line.startswith("  ") and not line.startswith("    "):
            match = re.fullmatch(r"  ([a-z][a-z0-9-]*):\s*(read|write|none)\s*", line)
            if not match:
                return None
            scope, access = match.groups()
            if scope in permissions:
                return None
            permissions[scope] = access
        elif line.startswith(" "):
            return None
        else:
            break
    return permissions or None


def validate_read_only_workflow(content):
    return parse_top_level_permissions(content) == EXPECTED


class WorkflowPermissionsUnitTests(unittest.TestCase):
    def test_accepts_only_contents_read(self):
        self.assertTrue(validate_read_only_workflow("name: test\npermissions:\n  contents: read\njobs:\n  test:\n    runs-on: ubuntu-latest\n"))

    def test_rejects_missing_permissions(self):
        self.assertFalse(validate_read_only_workflow("name: test\non: push\njobs: {}\n"))

    def test_rejects_contents_write(self):
        self.assertFalse(validate_read_only_workflow("permissions:\n  contents: write\n"))

    def test_rejects_write_all(self):
        self.assertFalse(validate_read_only_workflow("permissions: write-all\n"))

    def test_rejects_additional_write_scope(self):
        self.assertFalse(validate_read_only_workflow("permissions:\n  contents: read\n  pull-requests: write\n"))

    def test_rejects_job_level_permission_override(self):
        self.assertFalse(validate_read_only_workflow("permissions:\n  contents: read\njobs:\n  build:\n    permissions:\n      contents: write\n"))

    def test_rejects_duplicate_scope(self):
        self.assertFalse(validate_read_only_workflow("permissions:\n  contents: read\n  contents: none\n"))

    def test_rejects_invalid_scope_value(self):
        self.assertFalse(validate_read_only_workflow("permissions:\n  contents: execute\n"))

    def test_two_thousand_deterministic_permission_mutations(self):
        rng = random.Random(20261114)
        valid = "permissions:\n  contents: read\n"
        invalid = (
            "permissions: write-all\n",
            "permissions:\n  contents: write\n",
            "permissions:\n  contents: read\n  pull-requests: write\n",
            "permissions:\n  contents: read\n  id-token: write\n",
            "permissions:\n  contents: read\n  contents: none\n",
            "permissions:\n  contents: execute\n",
            "permissions:\n  contents: read\njobs:\n  build:\n    permissions:\n      contents: write\n",
            "jobs:\n  build:\n    permissions:\n      contents: read\n",
        )
        for _ in range(1000):
            self.assertTrue(validate_read_only_workflow(valid))
        for _ in range(1000):
            self.assertFalse(validate_read_only_workflow(rng.choice(invalid)))
        print("PASS: 2,000 deterministic workflow-permission mutations (seed 20261114).")


class RepositoryWorkflowPermissionsIntegrationTests(unittest.TestCase):
    def test_all_repository_workflows_use_only_contents_read(self):
        failures = []
        for relative_path in WORKFLOWS:
            path = ROOT / relative_path
            if not path.is_file():
                failures.append(relative_path + ": missing workflow")
                continue
            content = path.read_text(encoding="utf-8")
            if not validate_read_only_workflow(content):
                failures.append(relative_path + ": expected top-level permissions: contents: read and no job override")
        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
