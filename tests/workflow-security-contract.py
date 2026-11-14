#!/usr/bin/env python3
"""Unit and integration contracts for least-privilege GitHub Actions permissions.

Every workflow must grant only the read-only repository permission it needs.
No workflow or job may override that policy with write access. Every external action is pinned to its verified immutable commit SHA.
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




PINNED_ACTIONS = {
    "actions/checkout": ("3d3c42e5aac5ba805825da76410c181273ba90b1", "v7"),
    "actions/setup-node": ("949feb2413d6458794dcd2491c4babbbce0c15c1", "v7"),
    "actions/setup-python": ("6d4fd22b20465ccc0f7354476588e8df7c9ca0e0", "v7"),
    "actions/upload-artifact": ("cf430e030ddbb5b0abf93d22962f4752f3646cd9", "v7"),
}

ACTION_USE_LINE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)(?:\s+#\s*(\S+))?\s*$")


def parse_action_uses(content):
    references = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        match = ACTION_USE_LINE.fullmatch(line)
        if match:
            references.append((match.group(1), match.group(2), line_number))
    return references


def validate_pinned_actions(content):
    references = parse_action_uses(content)
    if not references:
        return False
    for reference, version_comment, _line_number in references:
        if reference.startswith("./"):
            continue
        if "@" not in reference:
            return False
        action, commit_sha = reference.rsplit("@", 1)
        expected = PINNED_ACTIONS.get(action)
        if expected is None or expected != (commit_sha, version_comment):
            return False
        if not re.fullmatch(r"[0-9a-f]{40}", commit_sha):
            return False
    return True


class WorkflowActionPinUnitTests(unittest.TestCase):
    def test_accepts_verified_checkout_sha_with_major_version_comment(self):
        self.assertTrue(validate_pinned_actions(
            "steps:\n  - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7\n"
        ))

    def test_rejects_mutable_major_tag(self):
        self.assertFalse(validate_pinned_actions("steps:\n  - uses: actions/checkout@v7 # v7\n"))

    def test_rejects_branch_reference(self):
        self.assertFalse(validate_pinned_actions("steps:\n  - uses: actions/checkout@main # v7\n"))

    def test_rejects_short_commit_sha(self):
        self.assertFalse(validate_pinned_actions(
            "steps:\n  - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90 # v7\n"
        ))

    def test_rejects_missing_version_comment(self):
        self.assertFalse(validate_pinned_actions(
            "steps:\n  - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"
        ))

    def test_rejects_unapproved_action_even_when_sha_pinned(self):
        self.assertFalse(validate_pinned_actions(
            "steps:\n  - uses: unreviewed/action@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7\n"
        ))

    def test_rejects_a_valid_sha_for_the_wrong_action(self):
        self.assertFalse(validate_pinned_actions(
            "steps:\n  - uses: actions/checkout@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7\n"
        ))

    def test_two_thousand_deterministic_action_reference_mutations(self):
        rng = random.Random(20261114)
        valid = (
            "steps:\n  - uses: actions/checkout@"
            "3d3c42e5aac5ba805825da76410c181273ba90b1 # v7\n"
        )
        invalid = (
            "actions/checkout@v7 # v7",
            "actions/checkout@main # v7",
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90 # v7",
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "unreviewed/action@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7",
            "actions/checkout@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7",
        )
        for _ in range(1000):
            self.assertTrue(validate_pinned_actions(valid))
        for _ in range(1000):
            mutated = "steps:\n  - uses: " + rng.choice(invalid) + "\n"
            self.assertFalse(validate_pinned_actions(mutated))
        print("PASS: 2,000 deterministic GitHub Action reference mutations (seed 20261114).")


class RepositoryWorkflowActionPinIntegrationTests(unittest.TestCase):
    def test_all_repository_workflows_pin_every_external_action(self):
        failures = []
        for relative_path in WORKFLOWS:
            path = ROOT / relative_path
            if not path.is_file():
                failures.append(relative_path + ": missing workflow")
                continue
            content = path.read_text(encoding="utf-8")
            if not validate_pinned_actions(content):
                failures.append(relative_path + ": external actions must use an approved full SHA and # v7 comment")
        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
