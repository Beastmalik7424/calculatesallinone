#!/usr/bin/env python3
"""Deterministic local tests for the generated-site external-link auditor."""
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.audit_external_links import check_url, extract_external_links


class LinkAuditHandler(BaseHTTPRequestHandler):
    flaky_calls = 0

    def do_HEAD(self):
        self._respond("HEAD")

    def do_GET(self):
        self._respond("GET")

    def _respond(self, method):
        if self.path == "/head-404-get-200" and method == "HEAD":
            self.send_response(404)
        elif self.path == "/broken":
            self.send_response(404)
        elif self.path == "/gone":
            self.send_response(410)
        elif self.path == "/forbidden":
            self.send_response(403)
        elif self.path == "/method-not-allowed" and method == "HEAD":
            self.send_response(405)
        elif self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/ok")
        elif self.path == "/loop":
            self.send_response(302)
            self.send_header("Location", "/loop")
        elif self.path == "/flaky":
            LinkAuditHandler.flaky_calls += 1
            self.send_response(503 if LinkAuditHandler.flaky_calls <= 2 else 200)
        else:
            self.send_response(200)
        self.¶»§q«^