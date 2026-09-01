# -*- coding: utf-8 -*-
"""
ARCHIVED -- retired repair "Ads landing page" variants. NOT built into the
site as of the 2026-09-01 policy-recovery pass. See
CURRENT-POLICY-SOURCE-REGISTER.md and CAMPAIGN-ELIGIBILITY-MATRIX.md for
why, and URL-MIGRATION-MAP.md for where each of these four paths now
redirects.

CORRECTED framing (replaces an incorrect earlier comment, preserved below
for traceability -- do not restore it): Google's "Third-Party Consumer
Technical Support" policy (support.google.com/adspolicy/answer/13527027)
is a flat PROHIBITION on advertising third-party hardware repair services
to consumers. It is NOT an account-level certification an advertiser can
apply for and pass -- there is no certification path for this category in
the current published policy text. No landing-page copy changes that.

--- PRESERVED FOR TRACEABILITY, SUPERSEDED, DO NOT FOLLOW ---
Original text said this was a Google Ads "account/certification
requirement... an owner action item (apply for the relevant Google
certification, or confirm eligibility, before spending on these ad
groups)." That framing implied a certification path existed. It does not.
ROOT-CAUSE-AND-TRACEABILITY.md documents this correction in full.
--- END PRESERVED NOTE ---
"""

from src.data.business import BIZ

LANDING_PAGES = [
    {
        "slug": "computer-repair-surrey-ads",
        "campaign_label": "General computer repair",
        "title_tag": f"Computer Repair in Surrey, BC | Contact {BIZ['name']}",
        "meta_description": (
            "Independent computer repair in Surrey, BC for laptops and desktops. "
            "Diagnostics explained before any repair work begins."
        ),
        "h1": "Computer Repair in Surrey, BC",
        "sub": (
            "Smart Geeks diagnoses laptop and desktop computer problems in "
            "Surrey, BC and explains what's wrong before recommending a repair."
        ),
        "intro": [
            "If your laptop or desktop won't turn on, keeps crashing, or is "
            "showing hardware problems, we test it on the bench first and walk "
            "you through the findings -- no guessing, no upsell pressure.",
        ],
        "trust_points": [
            "Independent, locally operated repair shop in Surrey, BC",
            "Diagnostics explained before any repair work begins",
            "Laptops and desktop computers, prebuilt or custom-built",
            "Not affiliated with any computer manufacturer",
        ],
        "whatsapp_key": "default",
        "related_service_slugs": ["laptop-repair", "desktop-repair", "motherboard-chip-level-repair"],
        "faqs": [
            ("Do you work on both laptops and desktops?",
             "Yes -- see our laptop repair and desktop repair pages for the "
             "device-specific diagnostic process for each."),
            ("Is Smart Geeks affiliated with any computer brand?",
             "No. Smart Geeks is an independent repair shop and is not "
             "authorized, certified, or endorsed by any computer manufacturer."),
        ],
    },
    {
        "slug": "laptop-repair-surrey-ads",
        "campaign_label": "Laptop repair",
        "title_tag": f"Laptop Repair in Surrey, BC | Contact {BIZ['name']}",
        "meta_description": (
            "Laptop repair in Surrey, BC for screens, batteries, charging ports, "
            "and hardware faults. Independent shop, diagnostics explained upfront."
        ),
        "h1": "Laptop Repair in Surrey, BC",
        "sub": (
            "Screen, battery, keyboard, charging, and hardware diagnostics for "
            "laptops, handled by an independent Surrey, BC repair shop."
        ),
        "intro": [
            "Cracked screen, a battery that won't hold a charge, or a laptop "
            "that won't power on at all -- we test the specific fault first and "
            "explain your options before any repair work starts.",
        ],
        "trust_points": [
            "Independent, locally operated repair shop in Surrey, BC",
            "Bench diagnostics before any repair recommendation",
            "Screens, batteries, keyboards, charging ports, and internal hardware",
            "Not affiliated with any laptop manufacturer",
        ],
        "whatsapp_key": "laptop-repair",
        "related_service_slugs": ["laptop-repair", "motherboard-chip-level-repair", "buy-sell-trade"],
        "faqs": [
            ("Can you fix a laptop that won't turn on?",
             "In many cases, yes -- we run a bench diagnostic to find the actual "
             "cause before recommending a repair. See our laptop repair page for "
             "the full process."),
            ("Do you repair gaming laptops?",
             "Yes, including thermal and GPU-related diagnostics common on "
             "higher-performance models."),
        ],
    },
    {
        "slug": "mac-repair-surrey-ads",
        "campaign_label": "Mac repair",
        "title_tag": f"Mac Repair in Surrey, BC | Contact {BIZ['name']}",
        "meta_description": (
            "Independent MacBook, iMac, and Mac mini repair in Surrey, BC. "
            "Not affiliated with Apple -- diagnostics explained before repair."
        ),
        "h1": "Mac Repair in Surrey, BC",
        "sub": (
            "MacBook, iMac, and Mac mini diagnostics and repair from an "
            "independent Surrey, BC shop -- not affiliated with Apple."
        ),
        "intro": [
            "Screen, battery, charging, storage, or logic-board issues on a "
            "MacBook, iMac, or Mac mini -- we diagnose the specific fault and "
            "explain what repair options are realistic for your model.",
        ],
        "trust_points": [
            "Independent repair shop -- not authorized or certified by Apple",
            "MacBook, iMac, and Mac mini diagnostics and repair",
            "Findings explained before any repair work begins",
            "Honest about which repairs are and aren't realistic on a given model",
        ],
        "whatsapp_key": "default",
        "related_service_slugs": ["macbook-repair", "imac-repair", "mac-mini-repair"],
        "faqs": [
            ("Is Smart Geeks an authorized Apple repair provider?",
             "No. We're an independent repair shop, not authorized, certified, "
             "or approved by Apple. We're upfront about that so you can decide "
             "what's right for your situation."),
            ("Do you repair MacBook logic board issues?",
             "Yes -- see our motherboard and chip-level repair page for how we "
             "approach board-level Mac repairs."),
        ],
    },
    {
        "slug": "gaming-console-repair-surrey-ads",
        "campaign_label": "Gaming console repair",
        "title_tag": f"Gaming Console Repair in Surrey, BC | Contact {BIZ['name']}",
        "meta_description": (
            "PlayStation, Xbox, and Nintendo Switch repair in Surrey, BC. "
            "Independent shop, power and hardware diagnostics explained upfront."
        ),
        "h1": "Gaming Console Repair in Surrey, BC",
        "sub": (
            "Power, overheating, disc drive, and HDMI diagnostics for "
            "PlayStation, Xbox, and Nintendo Switch consoles."
        ),
        "intro": [
            "Console won't power on, overheats mid-game, or the disc drive "
            "won't read -- we test the specific symptom on the bench before "
            "recommending a repair.",
        ],
        "trust_points": [
            "Independent, locally operated repair shop in Surrey, BC",
            "PlayStation, Xbox, and Nintendo Switch diagnostics",
            "Findings explained before any repair work begins",
            "Not affiliated with Sony, Microsoft, or Nintendo",
        ],
        "whatsapp_key": "gaming-console-repair",
        "related_service_slugs": ["gaming-console-repair", "motherboard-chip-level-repair", "buy-sell-trade"],
        "faqs": [
            ("Do you repair PS5, Xbox Series X/S, and Nintendo Switch?",
             "Yes, along with several previous console generations. Let us know "
             "your specific model when you reach out."),
            ("Is Smart Geeks affiliated with Sony, Microsoft, or Nintendo?",
             "No. Smart Geeks is an independent repair shop and is not "
             "authorized, certified, or endorsed by any console manufacturer."),
        ],
    },
]


def get_landing(slug):
    for lp in LANDING_PAGES:
        if lp["slug"] == slug:
            return lp
    return None
