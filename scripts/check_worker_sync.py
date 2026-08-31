#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Drift check between the Pages Functions (functions/api/contact.js,
functions/_middleware.js) and the self-contained Advanced Mode bundle
(alt-deploy/_worker.js) that duplicates their logic for drag-and-drop
deploys without Wrangler or Git (see alt-deploy/_worker.js's own header
comment for why the duplication exists).

This does NOT parse JS -- it's a lightweight literal/string check that
would catch the most likely real-world drift: someone changes a field name,
a length limit, the required-fields list, the email API endpoint, or the
production hostname list in one file and forgets the other.

Run with: python3 scripts/check_worker_sync.py
Exits non-zero if anything below doesn't match across both sources.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTACT_JS = os.path.join(ROOT, "functions", "api", "contact.js")
MIDDLEWARE_JS = os.path.join(ROOT, "functions", "_middleware.js")
WORKER_JS = os.path.join(ROOT, "alt-deploy", "_worker.js")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract(pattern, text, label):
    m = re.search(pattern, text)
    if not m:
        print(f"COULD NOT FIND {label} (pattern: {pattern})")
        return None
    return m.group(1)


def main():
    contact = read(CONTACT_JS)
    middleware = read(MIDDLEWARE_JS)
    worker = read(WORKER_JS)

    checks = [
        ("MAX_LENGTHS literal", r"MAX_LENGTHS\s*=\s*(\{[^}]*\})", contact, worker),
        ("REQUIRED_FIELDS literal", r"REQUIRED_FIELDS\s*=\s*(\[[^\]]*\])", contact, worker),
        ("ALLOWED_PREFERRED_CONTACT literal", r"ALLOWED_PREFERRED_CONTACT\s*=\s*new Set\((\[[^\]]*\])\)", contact, worker),
        ("Email API endpoint", r"(https://api\.cloudflare\.com/client/v4/accounts/\$\{env\.CF_ACCOUNT_ID\}/email/sending/send)", contact, worker),
        ("Rate-limit key prefix", r'(`contact-rl:)', contact, worker),
    ]

    hostname_checks = [
        ("PRODUCTION_HOSTNAMES literal", r"PRODUCTION_HOSTNAMES\s*=\s*new Set\((\[[^\]]*\])\)", middleware, worker),
    ]

    ok = True
    for label, pattern, src_a, src_b in checks + hostname_checks:
        val_a = extract(pattern, src_a, f"{label} (source)")
        val_b = extract(pattern, src_b, f"{label} (_worker.js)")
        if val_a is None or val_b is None:
            ok = False
            continue
        norm_a = re.sub(r"\s+", "", val_a)
        norm_b = re.sub(r"\s+", "", val_b)
        if norm_a != norm_b:
            ok = False
            print(f"[DRIFT] {label} differs:\n  source:     {val_a}\n  _worker.js: {val_b}")
        else:
            print(f"[OK] {label} matches")

    if ok:
        print("\nAll checked literals match between functions/*.js and alt-deploy/_worker.js.")
        sys.exit(0)
    else:
        print("\nDrift detected -- update alt-deploy/_worker.js to match functions/*.js.")
        sys.exit(1)


if __name__ == "__main__":
    main()
