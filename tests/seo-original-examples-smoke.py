from pathlib import Path
from html.parser import HTMLParser
import re

CASES = {
 "age-calculator": ["1943", "2026", "83 years", "80 years", "29,200", "leap"],
 "tasbih-counter": ["33", "99", "100", "dhikr", "tap"],
 "standard-calculator": ["15 + 27", "42", "200", "15%", "30"],
 "discount-calculator": ["25%", "80", "60"],
}
class TextOnly(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self, data): self.parts.append(data)
for slug, terms in CASES.items():
 path=Path("public")/slug/"index.html"
 assert path.exists(),slug
 html=path.read_text(encoding="utf-8")
 parser=TextOnly(); parser.feed(html)
 content=" ".join(parser.parts)
 assert "Worked examples and search questions" in content,slug
 for term in terms: assert term.lower() in content.lower(),(slug,term)
 assert 'rel="canonical"' in html,slug
 assert 'application/ld+json' in html,slug
print("Four original worked-example sections, canonical links and JSON-LD verified")
