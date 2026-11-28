#!/usr/bin/env python3
"""Check all same-site anchor links, including relative and absolute URLs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path("public")
SITE = "https://calculateallinone.vercel.app"
SITE_HOST = urlsplit(SITE).netloc.lower()


class AnchorCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in ("a", "area"):
            return
        values = dict(attrs)
        href = values.get("href")
        if href:
            self.hrefs.append(href.strip())


def page_route(page):
    relative = page.parent.relative_to(ROOT)
    return "/" if str(relative) == "." else "/" + relative.as_posix().strip("/") + "/"


def target_for_path(path):
    path = unquote(path or "/")
    if path == "/":
        return ROOT / "index.html"
    if Path(path).suffix:
        return ROOT / path.lstrip("/")
    if not path.endswith("/"):
        return None
    return ROOT / path.strip("/") / "index.html"


def main():
    failures = []
    pages = sorted(ROOT.rglob("index.html"))
    for page in pages:
        source = page.read_text(encoding="utf-8")
        parser = AnchorCollector()
        parser.feed(source)
        base_url = SITE + page_route(page)
        for href in parser.hrefs:
            if not href or href.startswith("#"):
                continue
            resolved = urlsplit(urljoin(base_url, href))
            if resolved.scheme not in ("http", "https") or resolved.netloc.lower() != SITE_HOST:
                continue
            path = unquote(resolved.path or "/")
            target = target_for_path(path)
            if target is None:
                failures.append(f"{page}: same-site page link {href!r} should point directly to a trailing-slash canonical route")
            elif not target.is_file():
                failures.append(f"{page}: {href!r} has no generated target ({target})")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print(f"PASS: {len(pages)} generated pages have valid same-site anchor targets, including relative and absolute links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
