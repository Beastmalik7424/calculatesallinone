from pathlib import Path
import re
src=Path("build.py").read_text(encoding="utf-8")
assert 'INTENT_RELATED = {' in src, "Missing curated search-intent related links"
assert 'related_slugs = INTENT_RELATED.get(t["slug"])' in src
assert 'related_tools = [other for other in TOOLS if other["slug"] in related_slugs]' in src
for slug in ("tasbih-counter","standard-calculator","age-calculator"):
 assert ('"'+slug+'":') in src, slug
for slug in ("tasbih-counter","standard-calculator","age-calculator"):
 html=(Path("public")/slug/"index.html").read_text(encoding="utf-8")
 assert "More in" in html
 assert re.search(r'<ul[^>]*>\s*<li><a[^>]*href="/[^"]+/"',html)
print("Search intent related links verified")
