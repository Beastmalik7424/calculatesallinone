import json
from pathlib import Path
config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
assert config.get("trailingSlash") is True, "Keep trailingSlash=true for canonical slash URLs"
redirects = {item.get("source"): item for item in config.get("redirects", [])}
for path in ("/contact", "/editorial-policy", "/methodology", "/privacy", "/terms"):
    item = redirects.get(path)
    assert item is not None, f"Missing explicit redirect for {path}"
    assert item.get("destination") == path + "/", f"Wrong destination for {path}"
    assert item.get("statusCode") == 301, f"{path} must use statusCode 301"
    assert "permanent" not in item, f"Do not combine statusCode with permanent for {path}"
    print(f"PASS config {path} -> 301 -> {path}/")
