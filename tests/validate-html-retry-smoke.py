#!/usr/bin/env python3
"""Regression tests for transient Nu HTML Checker failures."""
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


def test_429_respects_retry_after_and_recovers():
    attempts = []
    sleeps = []

    def opener(request, timeout):
        attempts.append((request, timeout))
        if len(attempts) == 1:
            raise urllib.error.HTTPError(
                request.full_url,
                429,
                "Too Many Requests",
                {"Retry-After": "7"},
                io.BytesIO(b"rate limited"),
            )
        return FakeResponse(b'{"messages":[]}')

    result = MODULE.fetch_validator_result(SCRIPT, opener=opener, sleep_fn=sleeps.append)
    assert result == {"messages": []}, result
    assert len(attempts) == 2, len(attempts)
    assert sleeps == [7.0], sleeps


def test_non_retryable_http_error_fails_without_waiting():
    sleeps = []

    def opener(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url,
            400,
            "Bad Request",
            {},
            io.BytesIO(b"invalid request"),
        )

    try:
        MODULE.fetch_validator_result(SCRIPT, opener=opener, sleep_fn=sleeps.append)
    except urllib.error.HTTPError as exc:
        assert exc.code == 400, exc.code
    else:
        raise AssertionError("HTTP 400 must not be retried or accepted")
    assert sleeps == [], sleeps


if __name__ == "__main__":
    test_429_respects_retry_after_and_recovers()
    test_non_retryable_http_error_fails_without_waiting()
    print("Nu HTML Checker retry regression: PASS")
