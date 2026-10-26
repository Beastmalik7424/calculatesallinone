#!/usr/bin/env python3
"""Ensure every inline script in built HTML is authorized by the deployed CSP."""
import base64
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.inline = False
        self.parts = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            a = dict(attrs)
            self.inline = "src" not in a and a.get("type", "").lower() != "application/ld+json"
            self.parts = []
    def handle_data(self, data):
        if self.inline:
            self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script":
            if self.inline:
                self.scripts.append("".join(self.parts))
            self.inline = False

config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
policies = [h["value"] for rule in config.get("headers", [])
            if rule.get("source") == "/(.*)" for h in rule.get("headers", [])
            if h.get("key", "").lower() == "content-security-policy"]
assert len(policies) == 1, "Expected exactly one global CSP"
script_src = policies[0].split("script-src ", 1)[1].split(";", 1)[0]
allowed = set(script_src.split())
files = list(Path("public").rglob("*.html"))
assert files, "No built HTML pages"
checked = 0
for file in files:
    parser = Scripts()
    parser.feed(file.read_text(encoding="utf-8"))
    for body in parser.scripts:
        if not body.strip():
            continue
        digest = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode("ascii")
        token = "'sha256-" + digest + "'"
        assert token in allowed, f"CSP missing hash for inline script: {file}: {token}"
        checked += 1
print(f"CSP inline script hash validation passed: {checked} scripts across {len(files)} HTML pages")
