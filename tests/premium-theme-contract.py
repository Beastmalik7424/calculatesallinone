#!/usr/bin/env python3
"""Unit and generated-page integration contracts for the approved soft-teal theme."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_SOURCE = ROOT / "styles" / "input.css"
CSS_MARKER = "/* Approved premium soft-teal homepage theme */"
LAYOUT_PROPERTIES = {
    "align-content", "align-items", "align-self", "aspect-ratio", "bottom",
    "column-gap", "display", "flex", "flex-basis", "flex-direction",
    "flex-grow", "flex-shrink", "flex-wrap", "float", "gap", "grid",
    "grid-area", "grid-auto-columns", "grid-auto-flow", "grid-auto-rows",
    "grid-column", "grid-row", "grid-template", "grid-template-areas",
    "grid-template-columns", "grid-template-rows", "height", "inset",
    "justify-content", "justify-items", "justify-self", "left", "margin",
    "max-height", "max-width", "min-height", "min-width", "order", "overflow",
    "padding", "place-content", "place-items", "position", "right", "row-gap",
    "top", "transform", "width", "z-index",
}


def extract_theme_block(css):
    if CSS_MARKER not in css:
        raise AssertionError("approved soft-teal theme block is missing")
    return css.split(CSS_MARKER, 1)[1]


def parse_declarations(block):
    rules = []
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", block):
        declarations = {}
        for declaration in body.split(";"):
            if ":" not in declaration:
                continue
            name, value = declaration.split(":", 1)
            declarations[name.strip().lower()] = value.strip()
        rules.append((selector.strip(), declarations))
    return rules


def parse_hex(value):
    value = value.strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise ValueError("expected six-digit hex colour: " + value)
    return tuple(int(value[index:index + 2], 16) / 255 for index in (1, 3, 5))


def linear_channel(channel):
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(color):
    red, green, blue = (linear_channel(channel) for channel in parse_hex(color))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground, background):
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def find_rule(rules, selector):
    return next((declarations for name, declarations in rules if name == selector), None)


class ThemeUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = CSS_SOURCE.read_text(encoding="utf-8")
        cls.block = extract_theme_block(cls.css)
        cls.rules = parse_declarations(cls.block)

    def test_theme_declares_complete_light_and_dark_palette(self):
        light = find_rule(self.rules, ".ca-home-wrap")
        dark = find_rule(self.rules, ".dark .ca-home-wrap")
        self.assertIsNotNone(light, "light theme tokens must be scoped to the homepage")
        self.assertIsNotNone(dark, "dark theme tokens must be scoped to the homepage")
        required = {
            "--ca-premium-canvas", "--ca-premium-surface", "--ca-premium-ink",
            "--ca-premium-muted", "--ca-premium-accent", "--ca-premium-accent-hover",
            "--ca-premium-border", "--ca-premium-soft",
        }
        self.assertTrue(required.issubset(light), "light palette is incomplete")
        self.assertTrue(required.issubset(dark), "dark palette is incomplete")

    def test_light_palette_meets_wcag_aa_text_and_control_contrast(self):
        light = find_rule(self.rules, ".ca-home-wrap")
        self.assertGreaterEqual(contrast_ratio(light["--ca-premium-ink"], light["--ca-premium-canvas"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(light["--ca-premium-muted"], light["--ca-premium-surface"]), 4.5)
        self.assertGreaterEqual(contrast_ratio("#ffffff", light["--ca-premium-accent"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(light["--ca-premium-ink"], light["--ca-premium-soft"]), 4.5)

    def test_dark_palette_meets_wcag_aa_text_and_control_contrast(self):
        dark = find_rule(self.rules, ".dark .ca-home-wrap")
        self.assertGreaterEqual(contrast_ratio(dark["--ca-premium-ink"], dark["--ca-premium-canvas"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(dark["--ca-premium-muted"], dark["--ca-premium-surface"]), 4.5)
        self.assertGreaterEqual(contrast_ratio("#ffffff", dark["--ca-premium-accent"]), 4.5)

    def test_theme_changes_only_visual_properties_not_layout_contracts(self):
        violations = []
        for selector, declarations in self.rules:
            for property_name in declarations:
                if property_name in LAYOUT_PROPERTIES:
                    violations.append(selector + " changes " + property_name)
        self.assertEqual(violations, [], "theme must not alter calculator positions, dimensions or layout")

    def test_theme_covers_all_existing_homepage_surfaces(self):
        selectors = {selector for selector, _ in self.rules}
        required = {
            ".ca-home-wrap", ".ca-home-header h1", ".ca-home-lead",
            ".ca-home-calculator", ".ca-home-card-heading",
            ".ca-home-calculator #calc-display", ".ca-home-calculator #calc-pad button",
            ".ca-home-tools", ".ca-home-tools h2", ".ca-home-tool-grid a",
            ".dark .ca-home-wrap", ".dark .ca-home-calculator",
            ".dark .ca-home-tools", ".dark .ca-home-tool-grid a",
        }
        self.assertTrue(required.issubset(selectors), "missing theme surfaces: " + ", ".join(sorted(required - selectors)))


class HomepageIntegrationTests(unittest.TestCase):
    def test_generated_homepage_keeps_calculator_before_tool_discovery_panel(self):
        page_path = ROOT / "public" / "index.html"
        self.assertTrue(page_path.is_file(), "generated homepage is missing")
        page = page_path.read_text(encoding="utf-8")
        calculator = page.find('class="ca-home-calculator"')
        tools = page.find('id="all-tools" class="ca-home-tools"')
        self.assertGreaterEqual(calculator, 0, "homepage calculator section is missing")
        self.assertGreater(tools, calculator, "tool discovery must remain after the calculator in DOM order")

    def test_generated_homepage_preserves_calculator_key_order(self):
        page = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
        match = re.search(r'<div id="calc-pad"[^>]*>(.*?)</div>', page, re.S)
        self.assertIsNotNone(match, "homepage calculator keypad is missing")
        actual = re.findall(r'data-key="([^"]+)"', match.group(1))
        expected = ["C", "BS", "%", "/", "7", "8", "9", "*", "4", "5", "6", "-", "1", "2", "3", "+", "00", "0", ".", "="]
        self.assertEqual(actual, expected, "calculator keypad keys and their order must not change")

    def test_generated_stylesheet_contains_the_approved_theme(self):
        output_css = ROOT / "public" / "assets" / "site.css"
        self.assertTrue(output_css.is_file(), "generated homepage stylesheet is missing")
        self.assertIn("--ca-premium-accent", output_css.read_text(encoding="utf-8"), "minified generated CSS must retain the theme tokens")


if __name__ == "__main__":
    unittest.main(verbosity=2)
