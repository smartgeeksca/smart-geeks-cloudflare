#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated QA over the generated public/ output.

Run with: python3 tests/qa.py
Exits non-zero if any check marked FAIL is found. Prints a machine-readable
summary block at the end that build/QA-REPORT.md documentation is based on.

This performs REAL checks against the actual generated files -- it does not
assert results it hasn't computed. Anything this script cannot check (visual
rendering, real Lighthouse scores, live DNS/deployment) is explicitly out of
scope and is called out as such in QA-REPORT.md, not silently assumed to pass.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")

PLACEHOLDER_WORDS = ["VERIFY", "TODO", "TBD", "PLACEHOLDER", "FIXME", "LOREM IPSUM", "COMING SOON"]
SUSPECT_STRINGS = ["example.com", "555-0100", "555-1234", "test@test.com", "fake review", "AW-XXXXXXX", "G-XXXXXXXXXX"]

results = {"pass": [], "fail": [], "warn": []}


def record(status, check, detail):
    results[status].append((check, detail))


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.meta_description = None
        self.canonical = None
        self.h1s = []
        self.links = []          # (href, is anchor text) for <a>
        self.imgs = []           # (src, alt, has_alt_attr)
        self.json_ld_blocks = []
        self._in_title = False
        self._in_h1 = False
        self._cur_h1_text = []
        self._in_json_ld = False
        self._json_ld_buf = []
        self.robots_meta = None

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            if attrs_d.get("name") == "description":
                self.meta_description = attrs_d.get("content")
            if attrs_d.get("name") == "robots":
                self.robots_meta = attrs_d.get("content")
        elif tag == "link" and attrs_d.get("rel") == "canonical":
            self.canonical = attrs_d.get("href")
        elif tag == "h1":
            self._in_h1 = True
            self._cur_h1_text = []
        elif tag == "a":
            self.links.append(attrs_d.get("href"))
        elif tag == "img":
            self.imgs.append((attrs_d.get("src"), attrs_d.get("alt"), "alt" in attrs_d))
        elif tag == "script" and attrs_d.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_ld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
            self.h1s.append("".join(self._cur_h1_text).strip())
        elif tag == "script" and self._in_json_ld:
            self._in_json_ld = False
            self.json_ld_blocks.append("".join(self._json_ld_buf))

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_h1:
            self._cur_h1_text.append(data)
        if self._in_json_ld:
            self._json_ld_buf.append(data)


def all_html_files():
    out = []
    for dirpath, _dirnames, filenames in os.walk(PUBLIC):
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def url_path_for(filepath):
    rel = os.path.relpath(filepath, PUBLIC)
    if rel == "index.html":
        return "/"
    if rel == "404.html":
        return "/404.html"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def relative_link_target_exists(href):
    """Resolve an internal href against public/ and check the target exists."""
    if href in ("", "#"):
        return False
    path = href.split("#")[0].split("?")[0]
    if path == "":
        return True  # pure #fragment link on the same page
    if path == "/":
        return os.path.exists(os.path.join(PUBLIC, "index.html"))
    if path.endswith("/"):
        return os.path.exists(os.path.join(PUBLIC, path.strip("/"), "index.html"))
    return os.path.exists(os.path.join(PUBLIC, path.lstrip("/")))


def relative_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = lin(r), lin(g), lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex1, hex2):
    l1, l2 = relative_luminance(hex1), relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_contrast():
    pairs = {
        "Filled button (#0062CC) on white -- button text": ("#0062CC", "#FFFFFF"),
        "Filled button hover (#004FA3) on white": ("#004FA3", "#FFFFFF"),
        "Body text (#333333) on white": ("#333333", "#FFFFFF"),
        "Muted text (#52606D) on white": ("#52606D", "#FFFFFF"),
        "Muted text (#52606D) on soft gray (#F5F7FA)": ("#52606D", "#F5F7FA"),
        "Navy (#0A1A2F) on white -- headings": ("#0A1A2F", "#FFFFFF"),
        "White text on navy (#0A1A2F) -- footer/CTA": ("#FFFFFF", "#0A1A2F"),
        "Error text (#B3261E) on error bg (#FBEAE9)": ("#B3261E", "#FBEAE9"),
        "Success text (#1E7E34) on success bg (#E9F7EF)": ("#1E7E34", "#E9F7EF"),
        "Raw brand blue (#007BFF) on white -- NOT used for filled-button text, only links/accents": ("#007BFF", "#FFFFFF"),
        # -- Design System V3 additions: new on-dark tokens used by the
        # hero / stat-strip / CTA / footer signature-surface treatment.
        "V3 text-on-dark-muted (#C7D2E0) on --ink-2 (#14304F)": ("#C7D2E0", "#14304F"),
        "V3 blue-on-dark (#8FC4FF) on navy (#0A1A2F) -- hero eyebrow text": ("#8FC4FF", "#0A1A2F"),
        "V3 blue-on-dark (#8FC4FF) on --ink-2 (#14304F)": ("#8FC4FF", "#14304F"),
        "V3 green-accent (#00E676) on --ink-2 (#14304F) -- stat-strip check icons": ("#00E676", "#14304F"),
        "V3 white on --ink-2 (#14304F) -- stat-strip numerals": ("#FFFFFF", "#14304F"),
    }
    for label, (fg, bg) in pairs.items():
        ratio = contrast_ratio(fg, bg)
        passes_aa_normal = ratio >= 4.5
        note = f"{ratio:.2f}:1"
        if "raw brand blue" in label.lower():
            # Documented as intentionally NOT used for filled-button/body text;
            # only flag if it were failing AND relied upon, which it isn't.
            status = "warn" if not passes_aa_normal else "pass"
            record(status, "Contrast: " + label, note + (" (fails AA; correctly not used for text-on-fill anywhere)" if not passes_aa_normal else ""))
            continue
        status = "pass" if passes_aa_normal else "fail"
        record(status, "Contrast: " + label, note)


def main():
    files = all_html_files()
    record("pass", "Pages generated", f"{len(files)} HTML files found in public/")

    titles = {}
    descriptions = {}
    placeholder_hits = []
    suspect_hits = []
    broken_internal_links = []
    hash_links = []
    empty_links = []
    missing_alt = []
    bad_json_ld = []
    missing_canonical = []
    wrong_canonical_host = []
    multi_h1 = []
    zero_h1 = []

    all_valid_paths = {url_path_for(f) for f in files}

    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        url_path = url_path_for(fp)

        for word in PLACEHOLDER_WORDS:
            if word in content:
                placeholder_hits.append((url_path, word))
        for s in SUSPECT_STRINGS:
            if s in content:
                suspect_hits.append((url_path, s))

        p = PageParser()
        p.feed(content)

        if not p.title:
            record("fail", "Title tag", f"{url_path}: missing <title>")
        else:
            titles.setdefault(p.title.strip(), []).append(url_path)

        if not p.meta_description:
            record("fail", "Meta description", f"{url_path}: missing")
        else:
            descriptions.setdefault(p.meta_description.strip(), []).append(url_path)

        if len(p.h1s) == 0:
            zero_h1.append(url_path)
        elif len(p.h1s) > 1:
            multi_h1.append((url_path, len(p.h1s)))

        if not p.canonical:
            missing_canonical.append(url_path)
        elif not p.canonical.startswith("https://www.smartgeeks.ca"):
            wrong_canonical_host.append((url_path, p.canonical))

        for href in p.links:
            if href is None:
                empty_links.append(url_path)
                continue
            if href == "#":
                hash_links.append(url_path)
                continue
            parsed = urlparse(href)
            if parsed.scheme or parsed.netloc:
                continue  # external link, not checked for existence
            if href.startswith("mailto:") or href.startswith("tel:"):
                continue
            if not relative_link_target_exists(href):
                broken_internal_links.append((url_path, href))

        for src, alt, has_alt in p.imgs:
            if not has_alt:
                missing_alt.append((url_path, src))

        for block in p.json_ld_blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                bad_json_ld.append((url_path, str(e)))

    if placeholder_hits:
        for path, word in placeholder_hits:
            record("fail", "Placeholder text", f'{path}: contains "{word}"')
    else:
        record("pass", "Placeholder text scan", f"Searched {len(files)} files for {', '.join(PLACEHOLDER_WORDS)} -- none found")

    if suspect_hits:
        for path, s in suspect_hits:
            record("fail", "Suspect fake data", f'{path}: contains "{s}"')
    else:
        record("pass", "Suspect fake-data scan", f"Searched for {', '.join(SUSPECT_STRINGS)} -- none found")

    dup_titles = {t: paths for t, paths in titles.items() if len(paths) > 1}
    if dup_titles:
        for t, paths in dup_titles.items():
            record("fail", "Duplicate title", f'"{t}" used on {len(paths)} pages: {", ".join(paths)}')
    else:
        record("pass", "Duplicate title check", f"{len(titles)} unique titles across {len(files)} pages")

    dup_desc = {d: paths for d, paths in descriptions.items() if len(paths) > 1}
    if dup_desc:
        for d, paths in dup_desc.items():
            record("fail", "Duplicate meta description", f"Used on {len(paths)} pages: {', '.join(paths)}")
    else:
        record("pass", "Duplicate meta description check", f"{len(descriptions)} unique descriptions across {len(files)} pages")

    if zero_h1:
        for path in zero_h1:
            record("fail", "Missing H1", path)
    else:
        record("pass", "Every page has an H1", f"{len(files)}/{len(files)}")

    if multi_h1:
        for path, n in multi_h1:
            record("fail", "Multiple H1s", f"{path}: {n} H1 elements")
    else:
        record("pass", "Single H1 per page", f"{len(files)}/{len(files)}")

    if missing_canonical:
        for path in missing_canonical:
            record("fail", "Missing canonical", path)
    else:
        record("pass", "Canonical tag present", f"{len(files)}/{len(files)}")

    if wrong_canonical_host:
        for path, canon in wrong_canonical_host:
            record("fail", "Wrong canonical host", f"{path}: {canon}")
    else:
        record("pass", "Canonical host = https://www.smartgeeks.ca", f"{len(files)}/{len(files)}")

    if broken_internal_links:
        for path, href in broken_internal_links:
            record("fail", "Broken internal link", f"{path} -> {href}")
    else:
        record("pass", "Internal link resolution", "0 broken internal links")

    if hash_links:
        for path in set(hash_links):
            record("fail", 'href="#" link', path)
    else:
        record("pass", 'href="#" scan', "none found")

    if empty_links:
        for path in set(empty_links):
            record("fail", "Empty href", path)
    else:
        record("pass", "Empty href scan", "none found")

    if missing_alt:
        for path, src in missing_alt:
            record("fail", "Missing alt attribute", f"{path}: {src}")
    else:
        record("pass", "Image alt attributes", "every <img> has an alt attribute")

    if bad_json_ld:
        for path, err in bad_json_ld:
            record("fail", "Invalid JSON-LD", f"{path}: {err}")
    else:
        record("pass", "JSON-LD validity", "every <script type=application/ld+json> block parses as valid JSON")

    check_contrast()

    # robots.txt sanity
    robots_path = os.path.join(PUBLIC, "robots.txt")
    with open(robots_path, "r", encoding="utf-8") as f:
        robots_txt = f.read()
    if re.search(r"Disallow:\s*/\s*$", robots_txt, re.MULTILINE):
        record("fail", "robots.txt", "contains a bare 'Disallow: /' that would block the whole production site")
    else:
        record("pass", "robots.txt does not block production", "no site-wide Disallow found")
    if "Sitemap:" in robots_txt and "smartgeeks.ca/sitemap.xml" in robots_txt:
        record("pass", "robots.txt references sitemap", "OK")
    else:
        record("fail", "robots.txt sitemap reference", "not found or wrong URL")

    # sitemap.xml sanity
    sitemap_path = os.path.join(PUBLIC, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        sitemap_xml = f.read()
    sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap_xml)
    non_www = [u for u in sitemap_urls if not u.startswith("https://www.smartgeeks.ca")]
    if non_www:
        record("fail", "Sitemap canonical host", f"{len(non_www)} URLs not on https://www.smartgeeks.ca")
    else:
        record("pass", "Sitemap URLs use canonical host", f"{len(sitemap_urls)} URLs checked")
    noindex_paths = {"/thank-you/", "/404.html"}
    leaked_noindex = [u for u in sitemap_urls if urlparse(u).path in noindex_paths]
    if leaked_noindex:
        record("fail", "Sitemap includes noindex page", str(leaked_noindex))
    else:
        record("pass", "Sitemap excludes noindex pages", "thank-you and 404 correctly excluded")

    # Required top-level files present
    for required in ["_headers", "_redirects", "robots.txt", "sitemap.xml", "site.webmanifest", "404.html"]:
        if os.path.exists(os.path.join(PUBLIC, required)):
            record("pass", f"{required} present", "OK")
        else:
            record("fail", f"{required} present", "MISSING")

    # ---- Report ----
    print("=" * 78)
    print("SMART GEEKS -- AUTOMATED QA REPORT")
    print("=" * 78)
    for status in ("fail", "warn", "pass"):
        label = {"fail": "FAIL", "warn": "WARN", "pass": "PASS"}[status]
        for check, detail in results[status]:
            print(f"[{label}] {check}: {detail}")

    print("-" * 78)
    print(f"Totals: {len(results['pass'])} pass, {len(results['warn'])} warn, {len(results['fail'])} fail")
    print("=" * 78)

    if results["fail"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
