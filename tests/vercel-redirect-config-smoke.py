import json
from pathlib import Path
config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
assert "trailingSlash" not in config, "Remove Vercel auto trailingSlash redirect so explicit 301 routes can run"
routes = config.get("routes", [])
by_src = {item.get("src"): item for item in routes}
favicon = by_src.get(r"^/favicon\.ico$")
assert favicon is not None, "Missing /favicon.ico compatibility redirect"
assert favicon.get("headers", {}).get("Location") == "/assets/favicon.svg", "Favicon redirect must target the generated SVG asset"
assert favicon.get("status") == 301, "Favicon compatibility redirect must be permanent"
assert routes.index(favicon) == 0, "Favicon redirect must precede the generic trailing-slash fallback"
print("PASS /favicon.ico -> 301 -> /assets/favicon.svg")
emi_html = next((item for item in routes if item.get("src") == "^/emi-calculator\\.html$"), None)
assert emi_html is not None, "Missing compatibility redirect for the former EMI .html URL"
assert emi_html.get("headers", {}).get("Location") == "/emi-calculator/", "EMI .html URL must redirect to the canonical calculator route"
assert emi_html.get("status") == 301, "EMI .html compatibility redirect must be permanent"
assert routes.index(emi_html) < routes.index(by_src[r"^/(?!.*\\.[^/]+$)(.*[^/])$"]), "EMI .html redirect must precede the generic route fallback"
print("PASS /emi-calculator.html -> 301 -> /emi-calculator/")
urdu_emi = by_src.get(r"^/ur/emi-calculator/?$")
assert urdu_emi is not None, "Missing fallback for the unpublished Urdu EMI route"
assert urdu_emi.get("headers", {}).get("Location") == "/emi-calculator/", "Urdu EMI fallback must target the available English calculator"
assert urdu_emi.get("status") == 301, "Urdu EMI fallback must be permanent"
print("PASS /ur/emi-calculator/ -> 301 -> /emi-calculator/")
for path in ("/contact", "/editorial-policy", "/methodology", "/privacy", "/terms"):
    item = by_src.get("^" + path + "$")
    assert item is not None, f"Missing explicit route for {path}"
    assert item.get("headers", {}).get("Location") == path + "/", f"Wrong Location for {path}"
    assert item.get("status") == 301, f"{path} must use route status 301"
    print(f"PASS config {path} -> 301 -> {path}/")
catchall = by_src.get(r"^/(?!.*\.[^/]+$)(.*[^/])$")
assert catchall is not None, "Missing extension-safe trailing slash fallback"
assert catchall.get("headers", {}).get("Location") == "/$1/"
assert catchall.get("status") == 308, "Other extensionless paths must retain permanent slash canonicalization"
assert routes.index(catchall) > max(routes.index(by_src["^" + p + "$"]) for p in ("/contact", "/editorial-policy", "/methodology", "/privacy", "/terms")), "301 trust routes must precede fallback"
print("PASS generic slash fallback: 308 after the five exact 301 routes")
