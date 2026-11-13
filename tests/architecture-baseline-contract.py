#!/usr/bin/env python3
"""Unit and integration guards for the approved pre-refactor route/build baseline."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "architecture" / "baseline" / "routes.json"


def parse_routes_text(content, *, trailing_slash=True):
    routes = [line.strip() for line in content.splitlines() if line.strip()]
    if len(routes) != len(set(routes)):
        raise ValueError("duplicate route")
    for route in routes:
        if not route.startswith("/") or route.startswith("//") or "?" in route or "#" in route:
            raise ValueError("invalid route: " + route)
        if trailing_slash and route != "/" and not route.endswith("/"):
            raise ValueError("route must end with slash: " + route)
        if not trailing_slash and route.endswith("/"):
            raise ValueError("exception route must not end with slash: " + route)
    return routes


def validate_route_groups(indexable, noindex, no_slash):
    if set(indexable) & set(noindex):
        raise ValueError("indexable and noindex routes overlap")
    if len(no_slash) != len(set(no_slash)):
        raise ValueError("duplicate no-slash exception")
    canonical_paths = set(indexable) | set(noindex)
    for route in no_slash:
        if route + "/" not in canonical_paths:
            raise ValueError("no-slash exception has no canonical route: " + route)


class RouteManifestUnitTests(unittest.TestCase):
    def test_accepts_canonical_root_and_nested_routes(self):
        self.assertEqual(parse_routes_text("/\n/about/\n/ur/bmi-calculator/\n"), ["/", "/about/", "/ur/bmi-calculator/"])

    def test_rejects_duplicate_routes(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_routes_text("/about/\n/about/\n")

    def test_rejects_noncanonical_indexable_route(self):
        with self.assertRaisesRegex(ValueError, "must end with slash"):
            parse_routes_text("/about\n")

    def test_rejects_invalid_route_syntax(self):
        with self.assertRaisesRegex(ValueError, "invalid route"):
            parse_routes_text("//outside/\n")

    def test_rejects_overlapping_index_and_noindex_groups(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            validate_route_groups(["/about/"], ["/about/"], [])

    def test_rejects_orphaned_no_slash_exception(self):
        with self.assertRaisesRegex(ValueError, "no canonical route"):
            validate_route_groups(["/about/"], [], ["/missing"])


class RepositoryBaselineIntegrationTests(unittest.TestCase):
    def test_route_manifests_match_approved_snapshot(self):
        self.assertTrue(BASELINE.is_file(), "approved route baseline is missing; add the reviewed snapshot after observing this expected RED result")
        snapshot = json.loads(BASELINE.read_text(encoding="utf-8"))
        indexable = parse_routes_text((ROOT / "indexable.txt").read_text(encoding="utf-8"))
        noindex = parse_routes_text((ROOT / "noindex.txt").read_text(encoding="utf-8"))
        no_slash = parse_routes_text((ROOT / "no-slash.txt").read_text(encoding="utf-8"), trailing_slash=False)
        validate_route_groups(indexable, noindex, no_slash)
        self.assertEqual(indexable, snapshot["indexable"])
        self.assertEqual(noindex, snapshot["noindex"])
        self.assertEqual(no_slash, snapshot["no_slash"])

    def test_vercel_static_output_contract_matches_snapshot(self):
        snapshot = json.loads(BASELINE.read_text(encoding="utf-8"))
        vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertEqual(vercel.get("buildCommand"), snapshot["vercel"]["buildCommand"])
        self.assertEqual(vercel.get("outputDirectory"), snapshot["vercel"]["outputDirectory"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
