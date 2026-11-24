from pathlib import Path
import re
import sys

SITE = "https://calculateallinone.vercel.app"
llms_path = Path("public/llms.txt")
sitemap_path = Path("public/sitemap.xml")
robots_path = Path("public/robots.txt")
assert llms_path.is_file(), "public/llms.txt is missing"
assert sitemap_path.is_file(), "public/sitemap.xml is missing"
assert robots_path.is_file(), "public/robots.txt is missing"
llms = llms_path.read_text(encoding="utf-8")
sitemap = sitemap_path.read_text(encoding="utf-8")
robots = robots_path.read_text(encoding="utf-8")
oai_group = re.search(r"(?ms)^User-agent: OAI-SearchBot\s*\n(.*?)(?=^User-agent:|\Z)", robots)
assert oai_group and re.search(r"(?m)^Allow: /\s*$", oai_group.group(1)), "robots.txt must allow OAI-SearchBot"
assert not re.search(r"(?m)^Disallow:", oai_group.group(1)), "OAI-SearchBot must not be partially blocked by path rules"
listed = set(re.findall(r"https://calculateallinone\.vercel\.app/[^\s)]*", llms))
sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
missing = sorted(sitemap_urls - listed)
stale = sorted(listed - sitemap_urls)
assert not missing, "llms.txt omits sitemap pages: " + ", ".join(missing)
assert not stale, "llms.txt includes URLs outside the indexable sitemap: " + ", ".join(stale)
assert len(sitemap_urls) == 42, f"Expected 42 sitemap URLs after adding the Ratio Calculator, found {len(sitemap_urls)}"
calorie_url = SITE + "/calorie-calculator/"
assert calorie_url in sitemap_urls, "Adult calorie calculator must be indexable in the sitemap"
assert calorie_url in listed, "llms.txt must describe the published adult calorie calculator"
difference_url = SITE + "/percentage-difference-calculator/"
assert difference_url in sitemap_urls, "Percentage difference calculator must be indexable in the sitemap"
assert difference_url in listed, "llms.txt must describe the percentage difference calculator"
ratio_url = SITE + "/ratio-calculator/"
assert ratio_url in sitemap_urls, "Ratio calculator must be indexable in the sitemap"
assert ratio_url in listed, "llms.txt must describe the ratio calculator"
assert "Unsupported questions are rejected rather than guessed." in llms, "llms.txt must accurately state that the Query Calculator rejects unsupported questions"
assert "not a diagnosis" in llms
assert "not a religious ruling" in llms

zakat_url = SITE + "/zakat-calculator/"
zakat_entries = [line for line in llms.splitlines() if zakat_url in line]
assert len(zakat_entries) == 1, "llms.txt must describe the English Zakat calculator exactly once"
assert "Hanafi" in zakat_entries[0] and "Sayyid Sistani" in zakat_entries[0], "Zakat summary must accurately identify both supported calculation methods"
assert "silver or gold Nisab" in zakat_entries[0], "Zakat summary must not imply that only the silver Nisab option exists"
assert "silver Nisab method stated on the page" not in zakat_entries[0], "Zakat summary must not misdescribe the live calculator's selectable Nisab methods"
assert "source references" in llms
assert re.search(r"^# CalculatesAll\s*\n> Free browser-based calculators for money, health, math, dates and everyday tasks\. Each tool states its inputs, method and limitations; results are general estimates, not professional advice\.", llms), "llms.txt should give AI readers a concise, accurate summary directly under the H1"
assert "expert reviewed" not in llms.lower()
print(f"PASS: OAI-SearchBot is allowed; llms.txt covers all {len(sitemap_urls)} sitemap URLs with accurate scope and limitations")
