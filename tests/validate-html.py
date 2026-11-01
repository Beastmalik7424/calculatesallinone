#!/usr/bin/env python3
"""Validate the homepage and scoped HTML files with the Nu HTML Checker."""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

FILES = [
    Path("public/index.html"),
    Path("public/ar/index.html"),
    Path("public/es/index.html"),
    Path("public/fr/index.html"),
    Path("public/about/index.html"),
    Path("public/contact/index.html"),
    Path("public/discount-calculator/index.html"),
    Path("public/editorial-policy/index.html"),
    Path("public/health/index.html"),
    Path("public/calorie-calculator/index.html"),
]
ENDPOINT = "https://validator.w3.org/nu/?out=json"
ALTERNATE_ENDPOINT = "https://html5.validator.nu/?out=json"
THIRD_ENDPOINT = "https://validator.unl.edu/?out=json"
VALIDATOR_ENDPOINTS = (ENDPOINT, ALTERNATE_ENDPOINT, THIRD_ENDPOINT)
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_INTERVAL_SECONDS = 5
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}


def fetch_validator_result(path, opener=None, sleep_fn=time.sleep):
    """Try three independent online Nu checker instances, failing over on transient outages."""
    open_url = opener or urllib.request.urlopen
    last_error = None
    for index, endpoint in enumerate(VALIDATOR_ENDPOINTS):
        request = urllib.request.Request(
            endpoint,
            data=path.read_bytes(),
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "User-Agent": "CalculateAllInOne-SEO-Validation/1.0",
            },
            method="POST",
        )
        try:
            with open_url(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_HTTP_CODES:
                raise
            last_error = exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        if index < len(VALIDATOR_ENDPOINTS) - 1:
            print(
                f"HTML VALIDATION FALLBACK {path}: {endpoint} returned {last_error}; "
                f"trying independent checker {VALIDATOR_ENDPOINTS[index + 1]}"
            )
    raise RuntimeError(
        f"all {len(VALIDATOR_ENDPOINTS)} online Nu HTML Checker instances failed for {path}: {last_error}"
    )


def main():
    failed = False
    for index, path in enumerate(FILES):
        if not path.is_file():
            print(f"HTML VALIDATION FAIL {path}: file missing")
            failed = True
        else:
            try:
                result = fetch_validator_result(path)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
                print(
                    f"HTML VALIDATION ERROR {path}: validator request failed "
                    f"after bounded online failover: {exc}"
                )
                failed = True
            else:
                messages = result.get("messages", [])
                errors = [m for m in messages if m.get("type") in ("error", "fatal")]
                warnings = [
                    m for m in messages
                    if m.get("type") == "info" and m.get("subType") == "warning"
                ]
                if errors:
                    print(
                        f"HTML VALIDATION FAIL {path}: "
                        f"{len(errors)} errors, {len(warnings)} warnings"
                    )
                    for item in errors:
                        line = item.get("lastLine", item.get("firstLine", "?"))
                        col = item.get("lastColumn", item.get("firstColumn", "?"))
                        print(
                            f"  line {line}, col {col}: "
                            f"{item.get('message', 'Unspecified HTML error')}"
                        )
                    failed = True
                else:
                    print(
                        f"HTML VALIDATION PASS {path}: "
                        f"0 errors, {len(warnings)} warnings"
                    )
        if index < len(FILES) - 1:
            time.sleep(REQUEST_INTERVAL_SECONDS)

    if failed:
        print("Nu HTML Checker: FAIL")
        return 1
    print("Nu HTML Checker: PASS (10 files, zero errors)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
