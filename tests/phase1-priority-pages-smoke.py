#!/usr/bin/env python3
"""Regression checks for the four Phase 1 priority calculator landing pages.

These checks exercise generated static HTML, not a duplicate implementation of
calculator formulas. They protect metadata, first-screen order, navigation,
language alternates and JSON-LD syntax.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"

CASES = {
    "tasbih-counter": {
        "title": "Tasbih Calculator Online | Dhikr Counter | CalculatesAll",
        "description": "Free Tasbih calculator and digital Tasbih counter. Tasbeeh counter with 33, 99, 100 or custom targets, undo and local saving when supported.",
        "form": 'id="tasbih-app"',
        "category": "/worship/",
        "related": ["/stopwatch/", "/zakat-calculator/", "/ur/tasbih-counter/"],
        "faq_min": 6,
        "h1": "Free Online Tasbih Counter",
    },
    "profit-loss-calculator": {
        "title": "Profit and Loss Calculator | Markup and Margin",
        "description": "Calculate product profit, business operating profit, loss, markup and margin from revenue, costs and expenses. Includes clear formulas and PKR examples.",
        "form": 'id="pl-form"',
        "category": "/money/",
        "related": ["/discount-calculator/", "/percentage-calculator/", "/emi-calculator/", "/compound-interest-calculator/"],
        "faq_min": 5,
        "h1": "Profit and Loss Calculator",
    },
    "years-to-days-calculator"¶»§q«^