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
MAX_ATTEMPTS = 5
BASE_RETRY_SECONDS = 5
MAX_RETRY_SECONDS = 60
MAX_RETRY_AFTER_SECONDS = 300
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
    """POST one HTML document, retrying transient HTTP and transport failures."""
    open_url = opener or urllib.request.urlopen
    request = urllib.request.Request(
        ENDPOINT,
        data=path.read_bytes(),
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "User-Agent": "CalculateAllInOne-SEO-Validation/1.0",
        },
        method="POST",
    )
    for attempt in range(MAX_ATTEMPTS):
        try:
            with open_url(request, timeout=45) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_HTTP_CODES or attempt == MAX_ATTEMPTS - 1:
                raise
            delay = retry_delay(exc, attempt)
            print(
                f"HTML VALIDATION RETRY {path}: HTTP {exc.code}; "
                f"waiting {delay:g}s before attempt {attempt + 2}/{MAX_ATTEMPTS}"
            )
            sleep_fn(delay)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == MAX_ATTEMPTS - 1:
                raise
            delay = retry_delay(exc, attempt)
            print(
                f"HTML VALIDATION RETRY {path}: {exc}; "
                f"waiting {delay:g}s before attempt {attempt + 2}/{MAX_ATTEMPTS}"
            )
            sleep_fn(delay)
    raise RuntimeError(f"validator did not return a result after {MAX_ATTEMPTS} attempts: {path}")


def main():
    failed = False
    for index, path in enumerate(FILES):
        if not path.is_file():
            print(f"HTML VALIDATION FAIL {path}: file missing")
            failed = True
        else:
            try:
                result = fetch_validator_result(path)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                print(
                    f"HTML VALIDATION ERROR {path}: validator request failed "
                    f"after {MAX_ATTEMPTS} attempts: {exc}"
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
