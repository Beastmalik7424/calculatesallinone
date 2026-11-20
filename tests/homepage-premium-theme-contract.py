#!/usr/bin/env python3
"""Regression contract for the approved premium soft-teal homepage visual refresh.

This is deliberately a visual-only contract: it rejects layout, sizing, ordering,
spacing, and positioning declarations in the new theme block.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSS = ROOT / "styles" / "input.css"
BUILT_CSS = ROOT / "public" / "assets" / "site.css"
HOME_HTML = ROOT / "public" / "index.html"
BASELINE = ROOT / "docs" / "architecture" / "baseline" / "routes.json"
MARKER = "/* Approved Premium Professional + Soft Teal homepage theme (visual-only). */"
END_MARKER = "/* End approved premium soft-teal homepage theme. */"


def relative_luminance(hex_color):
    values = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
    return sum(weight * value for weight, value in zip((0.2126, 0.7152, 0.0722), linear))


def contrast_ratio(foreground, background):
    first, second = sorted((relative_luminance(foreground), relative_luminance(background)), reverse=True)
    return (first + 0.05) / (second + 0.05)


class PremiumSoftTealThemeUnitTests(unittest.TestCase):
    def test_theme_block_is_present_and_complete(self):
        source = SOURCE_CSS.read_text(encoding="utf-8")
        self.assertIn(MARKER, source)
        self.assertIn(END_MARKER, source)
        self.assertLess(source.index(MARKER), source.index(END_MARKER))

    def test_new_theme_block_does_not_change_layout_or_calculator_geometry(self):
        source = SOURCE_CSS.read_text(encoding="utf-8")
        block = source.split(MARKER, 1)[1].split(END_MARKER, 1)[0]
        forbidden = re.compile(
            r"(?im)^\s*(?:display|position|top|right|bottom|left|order|"
            r"grid(?:-[a-z-]+)?|flex(?:-[a-z-]+)?|width|min-width|max-width|"
            r"height|min-height|max-height|margin(?:-[a-z-]+)?|"
            r"padding(?:-[a-z-]+)?|gap|row-gap|column-gap|transform)\s*:"
        )
        self.assertIsNone(forbidden.search(block), "Theme-only CSS must not alter layout, spacing, or geometry")

    def test_theme_colors_are_present_in_the_production_css_bundle(self):
        css = BUILT_CSS.read_text(encoding="utf-8")
        for color in (
            "#f8fcfb", "#edf6f4", "#cfe4e0", "#164e48", "#0f766e",
            "#e0f2ef", "#0f5f57", "#18332f", "#e3f4f0", "#315a54",
            "#142c28", "#e6f3f1", "#155e57",
        ):
            with self.subTest(color=color):
                self.assertIn(color, css.lower(), "Approved palette color missing from generated CSS: " + color)

    def test_text_and_control_color_pairs_meet_wcag_aa_normal_text_contrast(self):
        pairs = (
            ("#164e48", "#f8fcfb"),
            ("#315a54", "#edf6f4"),
            ("#ffffff", "#0f766e"),
            ("#ffffff", "#0f5f57"),
            ("#0f5f57", "#e0f2ef"),
            ("#e3f4f0", "#18332f"),
            ("#e6f3f1", "#18332f"),
            ("#e6f3f1", "#142c28"),
            ("#ffffff", "#155e57"),
            ("#ccfbf1", "#0f766e"),
            ("#e0f2ef", "#0f766e"),
            ("#e6f3f1", "#0f5f57"),
            ("#a7f3d0", "#315a54"),
            ("#142c28", "#e6f3f1"),
        )
        for foreground, background in pairs:
            with self.subTest(foreground=foreground, background=background):
                self.assertGreaterEqual(
                    contrast_ratio(foreground, background), 4.5,
                    foreground + " on " + background + " must meet WCAG AA 4.5:1",
                )

    def _assert_exact_locked_dependency(self, name, package, lock):
        version = package.get("devDependencies", {}).get(name)
        self.assertIsInstance(version, str, name + " must declare a version in package.json")
        self.assertRegex(
            version,
            r"^\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?$",
            name + " must be pinned to one exact semantic version",
        )
        lock_root = lock.get("packages", {}).get("", {}).get("devDependencies", {})
        self.assertEqual(lock_root.get(name), version, name + " package-lock root must match package.json")
        entry = lock.get("packages", {}).get("node_modules/" + name, {})
        self.assertEqual(entry.get("version"), version, name + " lock entry must match package.json")
        self.assertRegex(
            entry.get("integrity", ""),
            r"^sha512-[A-Za-z0-9+/]+={0,2}$",
            name + " lock entry must include a valid SHA-512 integrity value",
        )
        return version, entry

    def test_browser_dependency_contract_accepts_exact_version_bumps_and_rejects_ranges(self):
        package = {"devDependencies": {"axe-core": "4.14.1", "playwright": "1.65.1"}}
        integrity = "sha512-YWJjZA=="
        lock = {
            "packages": {
                "": {"devDependencies": {"axe-core": "4.14.1", "playwright": "1.65.1"}},
                "node_modules/axe-core": {"version": "4.14.1", "integrity": integrity},
                "node_modules/playwright": {
                    "version": "1.65.1",
                    "integrity": integrity,
                    "dependencies": {"playwright-core": "1.65.1"},
                },
                "node_modules/playwright-core": {"version": "1.65.1", "integrity": integrity},
            }
        }
        self._assert_exact_locked_dependency("axe-core", package, lock)
        playwright_version, playwright_entry = self._assert_exact_locked_dependency("playwright", package, lock)
        core_version = playwright_entry.get("dependencies", {}).get("playwright-core")
        core = lock.get("packages", {}).get("node_modules/playwright-core", {})
        self.assertEqual(core_version, playwright_version)
        self.assertEqual(core.get("version"), core_version)
        self.assertRegex(core.get("integrity", ""), r"^sha512-[A-Za-z0-9+/]+={0,2}$")

        for ranged_version in ("^1.65.1", "~1.65.1", ">=1.65.1", "1.65"):
            with self.subTest(ranged_version=ranged_version):
                with self.assertRaises(AssertionError):
                    self._assert_exact_locked_dependency(
                        "playwright",
                        {"devDependencies": {"playwright": ranged_version}},
                        lock,
                    )

    def test_browser_dependencies_are_pinned_and_ci_uses_npm_ci(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
        versions = {}
        entries = {}
        for name in ("axe-core", "playwright"):
            with self.subTest(package=name):
                versions[name], entries[name] = self._assert_exact_locked_dependency(name, package, lock)

        playwright_core_version = entries["playwright"].get("dependencies", {}).get("playwright-core")
        core = lock.get("packages", {}).get("node_modules/playwright-core", {})
        self.assertRegex(
            playwright_core_version or "",
            r"^\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?$",
            "playwright-core must be pinned to one exact semantic version",
        )
        self.assertEqual(playwright_core_version, versions["playwright"])
        self.assertEqual(core.get("version"), playwright_core_version)
        self.assertRegex(
            core.get("integrity", ""),
            r"^sha512-[A-Za-z0-9+/]+={0,2}$",
            "playwright-core lock entry must include a valid SHA-512 integrity value",
        )
        for workflow_path in (".github/workflows/ci.yml", ".github/workflows/site-build.yml"):
            workflow = (ROOT / workflow_path).read_text(encoding="utf-8")
            with self.subTest(workflow=workflow_path):
                self.assertIn("run: npm ci", workflow, "CI must install the committed lockfile")
                self.assertNotIn("npm install --no-save --package-lock=false", workflow, "CI must not install untracked browser dependencies")

    def test_zoom_restriction_pattern_rejects_disabling_viewport_directives(self):
        source = (ROOT / "tests/homepage-responsive-browser.cjs").read_text(encoding="utf-8")
        self.assertIn(
            r"const zoomRestrictionPattern = /user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\D|$)/i;",
            source,
            "The browser test must use a whitespace-aware zoom restriction pattern",
        )
        self.assertNotIn(
            r"const zoomRestrictionPattern = /user-scalable\\s*=\s*no",
            source,
            "The regex must not be double-escaped",
        )
        evaluate_start = source.index("const initial = await page.evaluate(() =>")
        evaluate_end = source.index("}));", evaluate_start)
        evaluate_source = source[evaluate_start:evaluate_end]
        self.assertIn(
            "const zoomRestrictionPattern = ",
            evaluate_source,
            "The zoom restriction regex must be defined in the browser evaluation scope",
        )
        pattern = re.compile(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\D|$)", re.I)
        self.assertIsNotNone(pattern.search("width=device-width, user-scalable=no"))
        self.assertIsNotNone(pattern.search("width=device-width, maximum-scale=1"))
        self.assertIsNone(pattern.search("width=device-width, initial-scale=1.0"))

    def test_production_bundle_contains_homepage_visual_theme_selectors(self):
        css = BUILT_CSS.read_text(encoding="utf-8")
        for selector in (
            ".ca-home-wrap{",
            ".ca-home-side",
            ".dark .ca-home-side",
            ".ca-home-calculator,.ca-home-tools{",
            ".ca-home-card-heading",
            ".ca-home-tools h2",
            ".ca-home-calculator #calc-display{",
            ".ca-home-calculator #calc-pad button[data-key=\"=\"]{",
            ".ca-home-tool-grid a{",
            ".dark .ca-home-tools-heading .ca-home-side-eyebrow",
            ".ca-home-tools #ca-all-tools-menu summary",
            ".ca-home-tools #ca-all-tools-menu a",
            ".dark .ca-home-tools #ca-all-tools-menu summary",
            ".dark .ca-home-tools #ca-all-tools-menu a",
            ".ca-home-tools-copy a",
            ".dark .ca-home-tools-copy a",
            ".dark .ca-home-wrap{",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, css, "Generated CSS is missing homepage theme selector: " + selector)


class HomepageStructureIntegrationTests(unittest.TestCase):
    def test_homepage_calculator_stays_before_all_tools_in_document_order(self):
        html = HOME_HTML.read_text(encoding="utf-8")
        calculator = html.index('class="ca-home-calculator"')
        tools = html.index('id="all-tools" class="ca-home-tools"')
        self.assertLess(calculator, tools, "The existing homepage calculator must remain before All Tools")
        self.assertIn('id="calc-display"', html)
        self.assertIn('id="calc-pad"', html)

    def test_homepage_calculator_keypad_order_is_unchanged(self):
        html = HOME_HTML.read_text(encoding="utf-8")
        keypad = re.search(r'<div id="calc-pad"[^>]*>(.*?)</div>', html, re.S)
        self.assertIsNotNone(keypad, "Homepage calculator keypad must remain present")
        actual = re.findall(r'data-key="([^"]+)"', keypad.group(1))
        expected = ["C", "(", ")", "BS", "7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "00", "0", ".", "+", "sqrt", "%", "="]
        self.assertEqual(actual, expected, "Homepage calculator keys and their order must remain unchanged")

    def test_route_manifests_match_the_approved_baseline(self):
        snapshot = json.loads(BASELINE.read_text(encoding="utf-8"))
        for filename, key in (
            ("indexable.txt", "indexable"),
            ("noindex.txt", "noindex"),
            ("no-slash.txt", "no_slash"),
        ):
            actual = [line.strip() for line in (ROOT / filename).read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(len(actual), len(set(actual)), filename + " must not contain duplicate routes")
            self.assertEqual(sorted(actual), sorted(snapshot[key]), filename + " route membership must remain unchanged")


if __name__ == "__main__":
    unittest.main(verbosity=2)
