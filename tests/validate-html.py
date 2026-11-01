#!/usr/bin/env python3
"""Validate the homepage and scoped HTML files with the Nu HTML Checker."""
import email.utils
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
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
PRIMARY_ATTEMPTS = 2
ALTERNATE_ATTEMPTS = 2
REQUEST_TIMEOUT_SECONDS = 20
TOTAL_ATTEMPTS = PRIMARY_ATTEMPTS + ALTERNATE_ATTEMPTS
BASE_RETRY_SECONDS = 5
MAX_RETRY_SECONDS = 20
MAX_RETRY_AFTER_SECONDS = 30
REQUEST_INTERVAL_SECONDS = 15
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}


def retry_delay(error, attempt):
    """Respect Retry-After when supplied, otherwise use bounded exponential backoff."""
    headers = getattr(error, "headers", None)
    retry_after = headers.get("Retry-After") if headers else None
    if retry_after:
        try:
            return min(max(float(retry_after), 1.0), MAX_RETRY_AFTER_SECONDS)
        except (TypeError, ValueError):
            try:
                retry_at = email.utils.parsedate_to_datetime(retry_after)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                seconds = (retry_at - datetime.now(timezone.utc)).total_seconds()
                return min(max(seconds, 1.0), MAX_RETRY_AFTER_SECONDS)
            except (TypeError, ValueError, OverflowError):
                pass
    return min(BASE_RETRY_SECONDS * (2 ** attempt), MAX_RETRY_SECONDS)


def fetch_validator_result(path, opener=None, sleep_fn=time.sleep):
    """Use Nu HTML Checker, then a separate Nu-compatible endpoint on transient outage."""
    open_url = opener or urllib.request.urlopen
    last_error = None
    for endpoint, attempts in ((ENDPOINT, PRIMARY_ATTEMPTS), (ALTERNATE_ENDPOINT, ALTERNATE_ATTEMPTS)):
        request = urllib.request.Request(
            endpoint,
            data=path.read_bytes(),
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "User-Agent": "CalculateAllInOne-SEO-Validation/1.0",
            },
            method="POST",
        )
        for attempt in range(attempts):
            try:
                with open_url(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                if exc.code not in RETRYABLE_HTTP_CODES:
                    raise
                last_error = exc
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
                last_error = exc
            if attempt < attempts - 1:
                delay = retry_delay(last_error, attempt)
                print(
                    f"HTML VALIDATION RETRY {path}: {endpoint} returned {last_error}; "
                    f"waiting {delay:g}s before attempt {attempt + 2}/{attempts}"
                )
                sleep_fn(delay)
        if endpoint == ENDPOINT:
            print(
                f"HTML VALIDATION FALLBACK {path}: primary Nu endpoint unavailable "
                f"after {attempts} attempts; switching to {ALTERNATE_ENDPOINT}"
            )
    raise RuntimeError(
        f"both Nu HTML Checker endpoints failed after bounded retries for {path}: {last_error}"
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
                    f"after {TOTAL_ATTEMPTS} bounded attempts: {exc}"
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
