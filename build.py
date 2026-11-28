import hashlib
import html
import json
import os
import shutil

from content_v5 import GUIDE_EXTRA, HOME_EXTRA, REVIEW_STATUS, TRUST_EXTRA
from urdu_v5 import URDU_EXTRA
from content_v13 import HUB_EXTRA, TERMS_PARAS, CONTACT_EXTRA, ABOUT_EXTRA
from lang_v6 import LANGS, UI

REVIEWERS_PATH = "reviewers.json"
REVIEWERS = json.load(open(REVIEWERS_PATH, encoding="utf-8")) if os.path.exists(REVIEWERS_PATH) else {}
from datetime import date

SITE_URL = os.environ.get("SITE_URL", "https://calculateallinone.vercel.app").rstrip("/")
ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "ca-pub-9453966537556063").strip()
ADSENSE_SLOT = os.environ.get("ADSENSE_SLOT", "").strip()
# Explicitly fail closed until the publisher confirms account-side consent setup.
# This flag is a safeguard, not an automated check of AdSense/CMP account settings.
ADSENSE_CONSENT_READY = os.environ.get("ADSENSE_CONSENT_READY", "").strip().lower() == "true"
if ADSENSE_SLOT and not ADSENSE_SLOT.isdigit():
    raise SystemExit("ADSENSE_SLOT must contain digits only, using the slot ID from your AdSense ad unit")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "malikadeelbhatti@gmail.com").strip()
SITE_DESCRIPTION = "Free browser-based calculators for adult BMI, Zakat, EMI, profit and loss, dates, unit conversions and a Tasbih counter. Clear formulas, no sign-up."
# Visible dates reflect the latest substantive content update for each page.
LASTMOD = {
    "/zakat-calculator/": "2026-11-25",
    "/years-to-days-calcul¶»§q«^