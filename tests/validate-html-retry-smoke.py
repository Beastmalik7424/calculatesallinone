#!/usr/bin/env python3
"""Regression tests for online Nu HTML Checker failover."""
import importlib.util
import io
import urllib.error
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate-html.py")
SPEC = importlib.util.spec_from_file_location("validate_html", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.body


def unavailable(request, code):
    return urllib.error.HTTPError(
        request.full_url, code, "Service Unavailable", {}, io.BytesIO(b"unavailable")
    )


def test_primary_rate_limit_falls_back_to_alternate():
    attempts = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        if request.full_url.startswith(MODULE.ENDPOINT):
            raise urllib.error.HTTPError(
                request.full_url, 429, "Too Many Requests",
                {"Retry-After": "120"}, io.BytesIO(b"rate limited")
            )
        return FakeResponse(b'{"messages":[]}')

    result = MODULE.fetch_validator_result(SCRIPT, opener=opener)
    assert result == {"messages": []}
    assert attempts == [MODULE.ENDPOINT, MODULE.ALTERNATE_ENDPOINT], attempts


def test_primary_and_alternate_outage_falls_back_to_third_checker():
    attempts = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        if request.full_url == MODULE.THIRD_ENDPOINT:
            return FakeResponse(b'{"messages":[]}')
        raise unavailable(request, 503)

    result = MODULE.fetch_validator_result(SCRIPT, opener=opener)
    assert result == {"messages": []}
    assert attempts == list(MODULE.VALIDATOR_ENDPOINTS), attempts


def test_non_retryable_http_error_fails_without_fallback():
    attempts = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        raise urllib.error.HTTPError(
            request.full_url, 400, "Bad Request", {}, io.BytesIO(b"invalid request")
        )

    try:
        MODULE.fetch_validator_result(SCRIPT, opener=opener)
    except urllib.error.HTTPError as exc:
        assert exc.code == 400, exc.code
    else:
        raise AssertionError("HTTP 400 must fail without accepting a fallback result")
    assert attempts == [MODULE.ENDPOINT], attempts


if __name__ == "__main__":
    test_primary_rate_limit_falls_back_to_alternate()
    test_primary_and_alternate_outage_falls_back_to_third_checker()
    test_non_retryable_http_error_fails_without_fallback()
    print("Nu HTML Checker online failover regression: PASS")
