import json
from pathlib import Path
config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
assert "trailingSlash" not in config, "Remove Vercel auto trailingSlash redirect so explicit 301 routes can run"
routes = config.get("routes", [])
by_src = {item.get("src"): item for item in routes}
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
