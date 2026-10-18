import os
import tempfile
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build

original_out = build.OUT
original_client = build.ADSENSE_CLIENT
original_slot = build.ADSENSE_SLOT
original_consent_ready = build.ADSENSE_CONSENT_READY
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
        build.ADSENSE_CONSENT_READY = True
        slot = build.ad_slot()
        assert 'data-ad-client="ca-pub-1234567890123456"' in slot
        assert 'data-ad-slot="1234567890"' in slot
        page_head = build.head("Test", "Description", "/", [], lang="en")
        assert "adsbygoogle.js?client=ca-pub-1234567890123456" in page_head

        build.ADSENSE_SLOT = ""
        assert build.ad_slot() == "", "Ads must stay disabled when no real ad-unit slot is configured"

        # Even with valid IDs, ad code stays disabled until account-side consent setup is confirmed.
        build.ADSENSE_SLOT = "1234567890"
        build.ADSENSE_CONSENT_READY = False
        assert build.ad_slot() == "", "Ad slots must stay disabled until consent readiness is confirmed"
        page_head_without_consent = build.head("Test", "Description", "/", [], lang="en")
        assert "adsbygoogle.js?client=ca-pub-1234567890123456" in page_head_without_consent, "Publisher verification snippet must remain available while ad slots are disabled"
        assert build.ad_slot() == "", "Ad slots must stay disabled until consent readiness is confirmed"

        # Reject malformed, shortened, overlong, or incorrectly prefixed publisher IDs.
        for invalid_client in ("ca-pub-123", "ca-pub-" + "1" * 17, "pub-" + "1" * 16):
            ads_file.unlink(missing_ok=True)
            os.environ["ADSENSE_CLIENT"] = invalid_client
            try:
                build.write_ads_txt()
            except SystemExit:
                pass
            else:
                raise AssertionError("Malformed AdSense publisher ID was accepted: " + invalid_client)
            assert not ads_file.exists(), "Invalid publisher ID must never create ads.txt"

        os.environ.pop("ADSENSE_CLIENT", None)
        build.ADSENSE_CLIENT = ""
        assert build.write_ads_txt() is False
        assert not ads_file.exists(), "ads.txt should not be published without a real publisher ID"
finally:
    build.OUT = original_out
    build.ADSENSE_CLIENT = original_client
    build.ADSENSE_SLOT = original_slot
    build.ADSENSE_CONSENT_READY = original_consent_ready
    if old_env_client is None:
        os.environ.pop("ADSENSE_CLIENT", None)
    else:
        os.environ["ADSENSE_CLIENT"] = old_env_client

print("PASS: AdSense ID/slot gating, ads.txt line format, and disabled-by-default behavior.")
