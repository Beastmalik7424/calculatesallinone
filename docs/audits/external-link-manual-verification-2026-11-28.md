# External-link manual verification â€” 28 November 2026

## Automated scan

The auditor scanned the generated `public/` output after `build.py` and `seo_finalize.py`, not the source templates. It inspected 49 generated HTML files plus generated CSS, JavaScript, JSON/JSON-LD, SVG, XML and text assets. It discovered 77 unique external HTTP(S) URLs.

| Automated result | Count | Interpretation |
|---|---:|---|
| Reachable | 59 | HTTP success or successful redirect |
| 403 blocked/restricted | 13 | Not labelled broken; bot protection or access restrictions are possible |
| Network/DNS unverified | 1 | No conclusive HTTP response |
| TLS/certificate unverified | 3 | Automated client could not complete TLS validation/handshake |
| Transient server error unverified | 1 | HTTP 429; retry/manual verification required |
| Confirmed 404/410 | 0 | No confirmed dead link remained in the final run |

The run used HEAD first, GET fallback for ambiguous/unsupported responses, redirect following, a bounded redirect cap, two exponential-backoff retries, an 8-worker pool and a 12-second request timeout. The test suite uses a local HTTP server to prove 403 handling, 404/410 confirmation, HEAD fallback, redirects, retry behaviour, loop handling and URL discovery.

Machine-readable evidence: `external-links-2026-11-28.json` and `external-links-2026-11-28.csv`. Human summary: `external-links-report-2026-11-28.md`.

## Verified source correction

A previous Years-to-Days citation to an obsolete NIS¶»§q«^