from pathlib import Path
checks={"/":["percentage-calculator","fraction-calculator","compound-interest-calculator","date-calculator"],"/math/":["percentage-calculator","fraction-calculator"],"/money/":["compound-interest-calculator"],"/time/":["date-calculator"]}
for page,slugs in checks.items():
 html=(Path("public")/page.strip("/")/"index.html").read_text()
 for slug in slugs:
  assert 'href="/'+slug+'/"' in html,(page,slug)
  assert (Path("public")/slug/"index.html").exists(),slug
print("Related calculator links verified")
