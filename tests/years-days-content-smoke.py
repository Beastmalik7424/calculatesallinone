from pathlib import Path
import html
import re
import sys

page = Path("public/years-to-days-calculator/index.html")
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

if not page.is_file():
    errors.append("missing generated Years to Days page")
else:
    source = page.read_text(encoding="utf-8")
    description = re.search(r'<meta name="description" content="([^"]*)"', source)
    check(
        description is not None and len(html.unescape(description.group(1))) <= 130,
        "meta description should fit a concise search snippet (130 characters or fewer)",
    )
    check(
        '<option value="365.25">Julian average (365.25)</option>' in source,
        "calculator must expose the distinct 365.25-day Julian average",
    )
    check(
        "Gregorian average (365.2425)" in source,
        "calculator must retain the distinct Gregorian average",
    )
    check(
        'href="https://aa.usno.navy.mil/faq/leap_years"' in source,
        "page must cite the US Naval Observatory for calendar-year definitions",
    )
    check(
        "Julian average (365.25)" in source and "Gregorian average (365.2425)" in source,
        "reference content must distinguish the Julian and Gregorian averages",
    )

for error in errors:
    print("FAIL:", error)
print(f"{len(errors)} failing checks")
sys.exit(1 if errors else 0)
