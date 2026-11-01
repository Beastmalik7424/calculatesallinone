from pathlib import Path
import re
import sys

SITE = "https://calculateallinone.vercel.app"
llms_path = Path("public/llms.txt")
sitemap_path = Path("public/sitemap.xml")
assert llms_path.is_file(), "public/llms.txt is missing"
assert sitemap_path.is_file(), "public/sitemap.xml is missing"
llms = llms_path.read_text(encoding="utf-8")
sitemap = sitemap_path.read_text(encoding="utf-8")
listed = set(re.findall(r"https://calculateallinone\.vercel\.app/[^\s)]+", llms))
sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
missing = sorted(sitemap_urls - listed)
stale = sorted(listed - sitemap_urls)
assert not missing, "llms.txt omits sitemap pages: " + ", ".join(missing)
assert not stale, "llms.txt includes URLs outside the indexable sitemap: " + ", ".join(stale)
assert len(sitemap_urls) == 38, f"Expected 38 sitemap URLs, found {len(sitemap_urls)}"
assert "does not answer arbitrary questions" in llms
assert "not a diagnosis" in llms
assert "not a religious ruling" in llms
assert "source references" in llms
assert "expert reviewed" not in llms.lower()
print(f"PASS: llms.txt covers all {len(sitemap_urls)} sitemap URLs with accurate scope and limitations")
