#!/usr/bin/env python3
"""Guard Vercel build, security-header, and versioned-asset cache contracts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))

assert config.get("$schema") == "https://openapi.vercel.sh/vercel.json"
assert config.get("installCommand") == "npm ci", "Vercel install phase must run npm ci exactly once"
assert config.get("buildCommand") == "npm run build", "Build command must not reinstall dependencies"
assert config.get("framework") is None, "Keep this static Python-generated site framework-neutral"
assert config.get("outputDirectory") == "public"
assert config.get("cleanUrls") is False

global_rules = [rule for rule in config.get("headers", []) if rule.get("source") == "/(.*)"]
assert len(global_rules) == 1, "Expected one global security-header rule"
global_headers = {item["key"].lower(): item["value"] for item in global_rules[0].get("headers", [])}
assert "access-control-allow-origin" not in global_headers, "Do not add an unnecessary global CORS policy"
csp = global_headers.get("content-security-policy", "")
for directive in ("default-src 'self'", "object-src 'none'", "base-uri 'self'",
                  "form-action 'self'", "frame-ancestors 'none'"):
    assert directive in csp, f"Required CSP protection missing: {directive}"
for key, expected in (
    ("x-content-type-options", "nosniff"),
    ("referrer-policy", "strict-origin-when-cross-origin"),
    ("x-frame-options", "DENY"),
):
    assert global_headers.get(key) == expected, f"Security header changed unexpectedly: {key}"

versioned_assets = ("/assets/site.css", "/assets/app.js", "/assets/zakat-calculator.js")
rules = config.get("headers", [])
for asset in versioned_assets:
    matches = [rule for rule in rules if rule.get("source") == asset]
    assert len(matches) == 1, f"Missing versioned asset cache rule: {asset}"
    rule = matches[0]
    query_v = [item for item in rule.get("has", [])
               if item.get("type") == "query" and item.get("key") == "v"]
    assert len(query_v) == 1 and query_v[0].get("value") == "[a-f0-9]{16}", (
        f"{asset} must be cached immutably only with its 16-character content version"
    )
    values = [h["value"] for h in rule.get("headers", []) if h.get("key", "").lower() == "cache-control"]
    assert values == ["public, max-age=31536000, immutable"], (
        f"{asset} must use one-year immutable caching only for versioned URLs"
    )

generic_assets = [rule for rule in rules if rule.get("source") == "/assets/(.*)"]
assert len(generic_assets) == 1, "Keep one fallback cache rule for other static assets"
missing_v = [item for item in generic_assets[0].get("missing", [])
             if item.get("type") == "query" and item.get("key") == "v"]
assert len(missing_v) == 1, "Fallback asset caching must exclude URLs carrying a version query"
generic_values = [h["value"] for h in generic_assets[0].get("headers", [])
                  if h.get("key", "").lower() == "cache-control"]
assert generic_values == ["public, max-age=3600"]

build_source = (ROOT / "build.py").read_text(encoding="utf-8")
for marker in (
    'CSS_ASSET_VERSION = css_asset_version()',
    'APP_JS_ASSET_VERSION = static_asset_version("app.js")',
    'ZAKAT_JS_ASSET_VERSION = static_asset_version("zakat-calculator.js")',
    'href="/assets/site.css?v=',
    'src="/assets/app.js?v=',
    'src="/assets/zakat-calculator.js?v=',
):
    assert marker in build_source, f"Versioned asset source contract changed: {marker}"

print("PASS: Vercel install/build split, output contract, security headers, CORS removal, and asset cache rules")
