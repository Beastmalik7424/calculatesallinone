import os
import tempfile
from pathlib import Path
import build

original_out = build.OUT
original_client = build.ADSENSE_CLIENT
original_slot = build.ADSENSE_SLOT
old_env_client = os.environ.get("ADSENSE_CLIENT")
try:
    with tempfile.TemporaryDirectory() as temp:
        build.OUT = temp
        ads_file = Path(temp) / "ads.txt"

        os.environ["ADSENSE_CLIENT"] = "ca-pub-1234567890123456"
        assert build.write_ads_txt() is True
        content = ads_file.read_text(encoding="utf-8")
        assert content == "google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0\n"
        assert not content.endswith("\\n"), "ads.txt contains literal backslash-n instead of a line break"

        build.ADSENSE_CLIENT = "ca-pub-1234567890123456"
        build.ADSENSE_SLOT = "1234567890"
        slot = build.ad_slot()
        assert 'data-ad-client="ca-pub-1234567890123456"' in slot
        assert 'data-ad-slot="1234567890"' in slot
        page_head = build.head("Test", "Description", "/", [], lang="en")
        assert "adsbygoogle.js?client=ca-pub-1234567890123456" in page_head

        build.ADSENSE_SLOT = ""
        assert build.ad_slot() == "", "Ads must stay disabled when no real ad-unit slot is configured"

        os.environ.pop("ADSENSE_CLIENT", None)
        assert build.write_ads_txt() is False
        assert not ads_file.exists(), "ads.txt should not be published without a real publisher ID"
finally:
    build.OUT = original_out
    build.ADSENSE_CLIENT = original_client
    build.ADSENSE_SLOT = original_slot
    if old_env_client is None:
        os.environ.pop("ADSENSE_CLIENT", None)
    else:
        os.environ["ADSENSE_CLIENT"] = old_env_client

print("PASS: AdSense ID/slot gating, ads.txt line format, and disabled-by-default behavior.")
