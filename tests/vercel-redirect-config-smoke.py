import json
from pathlib import Path
config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
assert config.get("trailingSlash") is True, "Keep canonical slash URLs for the rest of the site"
routes = {item.get("src"): item for item in config.get("routes", [])}
for path in ("/contact", "/editorial-policy", "/methodology", "/privacy", "/terms"):
    item = routes.get("^" + path + "$")
    assert item is not None, f"Missing explicit route for {path}"
    assert item.get("headers", {}).get("Location") == path + "/", f"Wrong Location for {path}"
    assert item.get("status") == 301, f"{path} must use route status 301"
    print(f"PASS route config {path} -> 301 -> {path}/")
