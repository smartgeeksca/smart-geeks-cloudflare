# -*- coding: utf-8 -*-
"""
JSON-LD structured-data builders.

Every builder here only emits fields Smart Geeks can actually back up.
No aggregateRating, no fabricated openingHoursSpecification, no guessed
geo coordinates, no invented prices. Business facts are pulled from
src/data/business.py so metadata, visible content, and schema can never
drift out of sync with each other.
"""

import json

from src.data.business import BIZ, SAME_AS, DISCLOSURE_SHORT

SITE = BIZ["website"]


def _url(path: str) -> str:
    if path.startswith("http"):
        return path
    return SITE.rstrip("/") + path


def local_business_schema(services=None):
    """Site-wide LocalBusiness (ElectronicsStore subtype). Organization is
    intentionally represented through this single LocalBusiness node rather
    than a duplicate separate Organization block, since LocalBusiness
    already extends Organization in schema.org and a second node would
    risk conflicting entity data for the same business."""
    data = {
        "@context": "https://schema.org",
        "@type": "ElectronicsStore",
        "@id": f"{SITE}/#business",
        "name": BIZ["name"],
        "url": SITE,
        "telephone": BIZ["phone_e164"],
        "email": BIZ["email"],
        "description": BIZ["description_short"],
        "disambiguatingDescription": (
            "Smart Geeks is an independently owned electronics repair and "
            "buy-sell-trade shop based in Surrey, BC. This listing is not "
            "affiliated with any other business using a similar name, and "
            "is not a device manufacturer or an authorized service centre."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": BIZ["address"]["street"],
            "addressLocality": BIZ["address"]["city"],
            "addressRegion": BIZ["address"]["region"],
            "postalCode": BIZ["address"]["postal_code"],
            "addressCountry": BIZ["address"]["country_code"],
        },
        "sameAs": SAME_AS,
    }
    if services:
        data["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": "Repair and trade-in services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": s["h1"],
                        "url": _url(f"/services/{s['slug']}/"),
                    },
                }
                for s in services
            ],
        }
    return data


def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "name": BIZ["name"],
        "url": SITE,
        "publisher": {"@id": f"{SITE}/#business"},
    }


def webpage_schema(path: str, title: str, description: str, page_type="WebPage"):
    return {
        "@context": "https://schema.org",
        "@type": page_type,
        "@id": _url(path) + "#webpage",
        "url": _url(path),
        "name": title,
        "description": description,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{SITE}/#business"},
        "inLanguage": "en-CA",
    }


def service_schema(name: str, description: str, path: str, service_type="Service", area_served=None):
    data = {
        "@context": "https://schema.org",
        "@type": service_type,
        "name": name,
        "description": description,
        "url": _url(path),
        "provider": {"@id": f"{SITE}/#business"},
    }
    if area_served:
        data["areaServed"] = [{"@type": "City", "name": a} for a in area_served]
    return data


def breadcrumb_schema(items):
    """items: list of (label, path) tuples, root first."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": label,
                "item": _url(path),
            }
            for i, (label, path) in enumerate(items)
        ],
    }


def faq_schema(qa_pairs):
    """qa_pairs: list of (question, answer_plain_text) tuples."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa_pairs
        ],
    }


def contactpage_schema(path: str, title: str, description: str):
    return webpage_schema(path, title, description, page_type="ContactPage")


def aboutpage_schema(path: str, title: str, description: str):
    return webpage_schema(path, title, description, page_type="AboutPage")


def to_script_tag(*schema_objects) -> str:
    """Render one or more schema dicts as a single JSON-LD <script> tag
    (an @graph when there's more than one) with valid, escaped JSON."""
    objs = [s for s in schema_objects if s]
    if not objs:
        return ""
    if len(objs) == 1:
        payload = objs[0]
    else:
        payload = {"@context": "https://schema.org", "@graph": objs}
        for o in objs:
            o.pop("@context", None)
    body = json.dumps(payload, ensure_ascii=False, indent=None, separators=(",", ":"))
    # Prevent premature </script> termination if any string ever contains it.
    body = body.replace("</", "<\\/")
    return f'<script type="application/ld+json">{body}</script>'
