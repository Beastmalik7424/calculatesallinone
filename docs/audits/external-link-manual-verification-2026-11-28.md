# External link audit — 28 November 2026

The automated scan inspected generated `public/` output across 49 HTML files plus CSS, JavaScript, JSON/JSON-LD, SVG, XML and text assets. It checked 77 unique external URLs using HEAD first, GET fallback, redirect following, bounded retries and separate blocked/network/TLS classifications.

| Result | Count |
|---|---:|
| Reachable | 59 |
| 403 restricted | 13 |
| Network/DNS unverified | 1 |
| TLS/certificate unverified | 3 |
| 429/transient | 1 |
| Confirmed 404/410 | **0** |

Ten of the 13 HTTP 403 pages opened in a normal browser/web reader (six CDC pages, two Islamic Relief pages, Mayo Clinic, and one IslamQA page). Three remain individually unverified:
- `https://darulifta-deoband.com/home/en/qa/47525` — 403; Urdu and English Zakat pages.
- `https://doi.org/10.2337/doci26-0003` — 403; English and Urdu BMI pages. The ADA publisher article is indexed, but the DOI resolver blocked automated readers.
- `https://islamqa.org/hanafi/darulfiqh/156652/` — 403; Urdu and English Zakat pages.

The Canada.ca, USNO, National Assembly of Pakistan, Sindh Government PDF and AboutAds destinations were cross-checked through browser/search evidence. Their automated timeout/TLS/429 responses are not proof of dead links.

An earlier confirmed 404 NIST citation on Years-to-Days was removed. The Gregorian rule and 365.2425-day mean are now attributed to the official U.S. Naval Observatory leap-year guide. The correction is in this branch-generated output only; production remains unchanged until deployment.

The JSON and CSV files in this folder preserve the aggregate counts and the three individually unverified links. No link was replaced merely because of bot protection or a temporary transport error.
