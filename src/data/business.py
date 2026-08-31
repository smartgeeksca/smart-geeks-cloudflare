# -*- coding: utf-8 -*-
"""
Central business data for Smart Geeks.

This is the SINGLE SOURCE OF TRUTH for all business facts used across
templates, visible page content, metadata, and JSON-LD structured data.

Rules enforced by design:
  - No invented prices, hours, warranty periods, review counts, ratings,
    years-in-business, certifications, or manufacturer affiliations live here.
  - Any fact the business owner has not supplied is represented as `None`
    (or an honest neutral string) and every template must handle that
    absence gracefully -- never print "None" or a bracketed placeholder.
  - Update this file only with facts the business owner has confirmed.
"""

from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# Core identity
# ---------------------------------------------------------------------------

BIZ = {
    "name": "Smart Geeks",
    "legal_name": "Smart Geeks",
    "short_name": "Smart Geeks",
    "description_short": (
        "Independent electronics repair and buy-sell-trade shop in Surrey, BC, "
        "serving laptops, desktops, Mac hardware, printers, gaming consoles, "
        "and chip-level motherboard work."
    ),
    "address": {
        "street": "#2 13018 84 Ave",
        "city": "Surrey",
        "region": "BC",
        "region_full": "British Columbia",
        "postal_code": "V3W 1L2",
        "country": "Canada",
        "country_code": "CA",
    },
    "phone_e164": "+17787280840",
    "phone_display": "(778) 728-0840",
    "phone_display_full": "+1 (778) 728-0840",
    "email": "support@smartgeeks.ca",
    "website": "https://www.smartgeeks.ca",
    "website_apex": "https://smartgeeks.ca",
    "whatsapp_number": "17787280840",
}

BIZ["address"]["full_display"] = (
    f"{BIZ['address']['street']}, {BIZ['address']['city']}, "
    f"{BIZ['address']['region']} {BIZ['address']['postal_code']}"
)
BIZ["address"]["full_single_line"] = (
    f"{BIZ['address']['street']}, {BIZ['address']['city']}, "
    f"{BIZ['address']['region']} {BIZ['address']['postal_code']}, "
    f"{BIZ['address']['country']}"
)

_MAPS_QUERY = quote_plus(f"{BIZ['name']}, {BIZ['address']['full_single_line']}")
BIZ["maps_url"] = f"https://www.google.com/maps/search/?api=1&query={_MAPS_QUERY}"
BIZ["maps_search_query"] = _MAPS_QUERY

BIZ["tel_href"] = f"tel:{BIZ['phone_e164']}"
BIZ["mailto_href"] = f"mailto:{BIZ['email']}"
BIZ["whatsapp_base"] = f"https://wa.me/{BIZ['whatsapp_number']}"


def whatsapp_href(message: str) -> str:
    """Build a WhatsApp deep link with a pre-filled, URL-encoded message."""
    return f"{BIZ['whatsapp_base']}?text={quote_plus(message)}"


# Page-relevant, pre-filled WhatsApp messages (kept short and specific)
WHATSAPP_MESSAGES = {
    "default": "Hi Smart Geeks, I'd like to ask about a repair.",
    "laptop-repair": "Hi Smart Geeks, I have a laptop issue I'd like to ask about.",
    "desktop-repair": "Hi Smart Geeks, I have a desktop computer issue I'd like to ask about.",
    "printer-repair": "Hi Smart Geeks, I have a printer issue I'd like to ask about.",
    "gaming-console-repair": "Hi Smart Geeks, I have a game console issue I'd like to ask about.",
    "macbook-repair": "Hi Smart Geeks, I have a MacBook issue I'd like to ask about.",
    "imac-repair": "Hi Smart Geeks, I have an iMac issue I'd like to ask about.",
    "mac-mini-repair": "Hi Smart Geeks, I have a Mac mini issue I'd like to ask about.",
    "motherboard-chip-level-repair": "Hi Smart Geeks, I have a motherboard/chip-level issue I'd like to ask about.",
    "buy-sell-trade": "Hi Smart Geeks, I'd like to ask about buying, selling, or trading a device.",
}

# ---------------------------------------------------------------------------
# Social profiles (only accounts the owner has actually supplied)
# ---------------------------------------------------------------------------

SOCIAL_LINKS = [
    {"label": "Facebook", "url": "https://www.facebook.com/smartgeeks.ca", "icon": "facebook"},
    {"label": "Instagram", "url": "https://www.instagram.com/smartgeeks.ca", "icon": "instagram"},
    {"label": "LinkedIn", "url": "https://www.linkedin.com/company/smartgeeksca", "icon": "linkedin"},
]

# sameAs list for JSON-LD -- only confirmed profiles, nothing guessed
SAME_AS = [s["url"] for s in SOCIAL_LINKS] + [BIZ["whatsapp_base"]]

# ---------------------------------------------------------------------------
# Service areas
# ---------------------------------------------------------------------------

# The physical shop is in Surrey only. These are markets Smart Geeks serves
# by appointment / drop-off, never implied branch locations.
SERVICE_AREAS = ["Surrey", "Delta", "Langley", "White Rock"]

# ---------------------------------------------------------------------------
# Brand tokens
# ---------------------------------------------------------------------------
# #007BFF fails WCAG 2.2 AA (3.98:1) for white text on a filled background,
# so filled buttons/badges use the darker, verified-compliant #0062CC
# (5.80:1 with white) instead. #007BFF itself remains usable for links on
# white/soft-gray backgrounds, borders, and non-text accents.

BRAND = {
    "blue": "#007BFF",              # accent / links / icon strokes only
    "blue_button": "#0062CC",       # WCAG AA-safe filled-button blue (5.80:1 on white)
    "blue_button_hover": "#004FA3",
    "navy": "#0A1A2F",
    "green_accent": "#00E676",      # decorative / non-text accents only (fails AA as text)
    "bg_soft": "#F5F7FA",
    "text": "#333333",
    "text_muted_safe": "#52606D",   # AA-safe muted text on white/soft-gray (>4.5:1)
    "border": "#E1E7EF",
    "surface": "#FFFFFF",
    "success": "#1E7E34",
    "error": "#B3261E",
    "focus_ring": "#0062CC",
}

# ---------------------------------------------------------------------------
# Owner-supplied facts that are NOT yet available.
# Every one of these renders as an honest, neutral statement in templates --
# never a bracketed placeholder, never a fabricated default.
# ---------------------------------------------------------------------------

OWNER_PENDING = {
    "hours": None,                # -> "Call or WhatsApp us to confirm today's hours."
    "warranty_period": None,      # -> warranty page explains a warranty exists on paid repairs,
                                   #    without stating a duration until confirmed
    "diagnostic_fee": None,       # -> diagnostic policy explains the process, not a dollar figure
    "years_in_business": None,
    "review_rating": None,
    "review_count": None,
}

# ---------------------------------------------------------------------------
# Analytics / conversion tracking configuration.
# All IDs are None until the owner supplies real, live values. Templates and
# main.js must not fire any tracking call while these are None.
# ---------------------------------------------------------------------------

ANALYTICS_CONFIG = {
    "ga4_measurement_id": None,          # e.g. "G-XXXXXXXXXX"
    "google_ads_conversion_id": None,    # e.g. "AW-XXXXXXXXX"
    "google_ads_conversion_labels": {
        "form_submit": None,
        "phone_click": None,
        "whatsapp_click": None,
    },
}

# ---------------------------------------------------------------------------
# Primary navigation
# ---------------------------------------------------------------------------

NAV_LINKS = [
    {"label": "Services", "href": "/services/", "children": [
        {"label": "Services overview", "href": "/services/"},
        {"label": "Laptop repair", "href": "/services/laptop-repair/"},
        {"label": "Desktop repair", "href": "/services/desktop-repair/"},
        {"label": "MacBook repair", "href": "/services/macbook-repair/"},
        {"label": "iMac repair", "href": "/services/imac-repair/"},
        {"label": "Mac mini repair", "href": "/services/mac-mini-repair/"},
        {"label": "Printer repair", "href": "/services/printer-repair/"},
        {"label": "Gaming console repair", "href": "/services/gaming-console-repair/"},
        {"label": "Motherboard & chip-level repair", "href": "/services/motherboard-chip-level-repair/"},
        {"label": "Buy, sell & trade", "href": "/services/buy-sell-trade/"},
    ]},
    {"label": "Service areas", "href": "/service-areas/"},
    {"label": "About", "href": "/about/"},
    {"label": "Reviews", "href": "/reviews/"},
    {"label": "FAQs", "href": "/faqs/"},
    {"label": "Contact", "href": "/contact/"},
]

FOOTER_COLUMNS = [
    {
        "heading": "Services",
        "links": [
            {"label": "Laptop repair", "href": "/services/laptop-repair/"},
            {"label": "Desktop repair", "href": "/services/desktop-repair/"},
            {"label": "MacBook repair", "href": "/services/macbook-repair/"},
            {"label": "iMac repair", "href": "/services/imac-repair/"},
            {"label": "Mac mini repair", "href": "/services/mac-mini-repair/"},
            {"label": "Printer repair", "href": "/services/printer-repair/"},
            {"label": "Gaming console repair", "href": "/services/gaming-console-repair/"},
            {"label": "Motherboard & chip-level repair", "href": "/services/motherboard-chip-level-repair/"},
            {"label": "Buy, sell & trade", "href": "/services/buy-sell-trade/"},
        ],
    },
    {
        "heading": "Company",
        "links": [
            {"label": "About Smart Geeks", "href": "/about/"},
            {"label": "Service areas", "href": "/service-areas/"},
            {"label": "Reviews", "href": "/reviews/"},
            {"label": "FAQs", "href": "/faqs/"},
            {"label": "Contact", "href": "/contact/"},
        ],
    },
    {
        "heading": "Policies",
        "links": [
            {"label": "Privacy policy", "href": "/privacy-policy/"},
            {"label": "Terms of service", "href": "/terms-of-service/"},
            {"label": "Warranty policy", "href": "/warranty-policy/"},
            {"label": "Diagnostic policy", "href": "/diagnostic-policy/"},
            {"label": "Accessibility statement", "href": "/accessibility-statement/"},
        ],
    },
]

# ---------------------------------------------------------------------------
# Independent-business disclosure (short + long forms, reused everywhere)
# ---------------------------------------------------------------------------

DISCLOSURE_SHORT = (
    "Smart Geeks is an independent repair shop and is not affiliated with, "
    "authorized by, or endorsed by any device manufacturer."
)

DISCLOSURE_LONG = (
    "Smart Geeks is an independently owned and operated repair business. "
    "We are not the manufacturer of the devices we service, and we are not "
    "authorized, certified, or approved by Apple, Microsoft, Sony, Nintendo, "
    "Dell, HP, Lenovo, or any other device manufacturer. Manufacturer and "
    "product names appear on this site only to identify the devices we can "
    "work on and remain the trademarks of their respective owners."
)
