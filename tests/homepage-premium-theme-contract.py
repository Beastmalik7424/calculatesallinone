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
            ("#e6f3f1", "#142c28"),
            ("#ffffff", "#155e57"),
            ("#142c28", "#e6f3f1"),
        )
        for foreground, background in pairs:
            with self.subTest(foreground=foreground, background=background):
                self.assertGreaterEqual(
                    contrast_ratio(foreground, background), 4.5,
                    foreground + " on " + background + " must meet WCAG AA 4.5:1",
                )

    def test_production_bundle_contains_homepage_visual_theme_selectors(self):
        css = BUILT_CSS.read_text(encoding="utf-8")
        for selector in (
            ".ca-home-wrap{",
            ".ca-home-calculator,.ca-home-tools{",
            ".ca-home-card-heading",
            ".ca-home-tools h2",
            ".ca-home-calculator #calc-display{",
            ".ca-home-calculator #calc-pad button[data-key=\"=\"]{",
            ".ca-home-tool-grid a{",
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
