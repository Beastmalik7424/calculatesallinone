#!/usr/bin/env python3
"""Audit every absolute external HTTP(S) URL in generated site output.

Uses only Python's standard library. HEAD is attempted first; ambiguous or
unsupported HEAD responses are confirmed with GET. Transient failures retry
with exponential backoff. Bot-blocked responses are never labelled broken.
"""
from __future__ import annotations

import argparse
import csv
import html
from html.parser import HTMLParser
import json
import re
import socket
import ssl
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

URL_RE = re.compile(r"https?://[^\s\"'<>\\)\]}]+", re.I)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)|@import\s+['\"]([^'\"]+)['\"]", re.I)
SRCSET_SPLIT_RE = re.compile(r",\s*(?=https?://|/|\./|\.\./|data:)", re.I)
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
TRANSIENT = {408, 425, 429, 500, 502, 503, 504, 520, 521, 522, 523, 524}
CONFIRM_WITH_GET = {403, 404, 405, 410, 501}


def clean_url(value: str, base_url: str | None = None) -> str | None:
    value = html.unescape(value.strip().strip("\"'<> "))
    if not value or value.startswith(("#", "data:", "blob:", "mailto:", "tel:", "javascript:", "file:")):
        return None
    if value.s¶»§q«^