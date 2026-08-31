# -*- coding: utf-8 -*-
"""Original content for Home, Services overview, Service areas, About,
FAQs, Contact, Reviews, Thank-you, 404, and Accessibility statement."""

from src.data.business import BIZ, SERVICE_AREAS, DISCLOSURE_LONG

CITY = BIZ["address"]["city"]

# --------------------------------------------------------------------------- #
# Home
# --------------------------------------------------------------------------- #

HOME = {
    "title_tag": f"Smart Geeks | Independent Electronics Repair in {CITY}, BC",
    "meta_description": (
        "Independent laptop, desktop, Mac, printer, and gaming console repair "
        "in Surrey, BC, plus buy-sell-trade. Honest diagnostics, explained before we repair."
    ),
    "hero_eyebrow": "Independent repair shop in Surrey, BC",
    "hero_h1": "Electronics repair that explains itself before it charges you.",
    "hero_sub": (
        "Smart Geeks diagnoses laptops, desktops, Mac hardware, printers, and "
        "gaming consoles in Surrey, BC, and tells you what's actually wrong "
        "before any repair work begins."
    ),
    "trust_items": [
        "Independent, locally operated in Surrey, BC",
        "Diagnostics explained before repair work starts",
        "Laptops, desktops, Mac hardware, printers, and consoles",
        "Buy, sell, and trade accepted in person",
    ],
    "why_heading": "Why people choose an independent shop",
    "why_intro": (
        "We're not a manufacturer or an authorized service centre, and we don't "
        "pretend to be. What we offer instead is a bench process built around "
        "explaining what's wrong before you commit to a repair."
    ),
    "why_points": [
        ("Diagnosis before repair", "We test first and explain findings before any parts are ordered or work begins."),
        ("Honest about limits", "Not every device or fault can be economically repaired, and we'll tell you when that's the case."),
        ("One shop, several device categories", "Laptops, desktops, Mac computers, printers, and gaming consoles, plus chip-level board work."),
        ("Buy, sell, and trade", "A path for devices you're done with, or a tested used device instead of buying new."),
    ],
    "process_heading": "How a repair typically works",
    "process_steps": [
        ("Get in touch or drop by", "Call, WhatsApp, use the contact form, or bring the device to our Surrey location."),
        ("Bench diagnostics", "We test the relevant components and identify the actual cause of the symptom."),
        ("We explain what we found", "Before any repair work starts, we walk you through the findings and the options."),
        ("Repair and function test", "Once you're ready to proceed, we complete the repair and test it under normal use."),
    ],
    "services_heading": "Repair and trade services",
    "services_intro": "Browse by device, or get in touch if you're not sure which category your issue falls under.",
    "areas_heading": "Where we serve",
    "areas_intro": (
        f"Our shop is located in {CITY}, BC. We also work with customers from "
        + ", ".join(SERVICE_AREAS[1:]) +
        " who drop off or arrange service with us -- we don't operate branch "
        "locations outside Surrey."
    ),
    "faq_heading": "Common questions",
    "cta_heading": "Have a device that needs a second opinion?",
    "cta_body": "Tell us what's happening and we'll let you know honestly what your options are.",
}

# Home-page FAQ preview -- a short subset of the full FAQ list, by question text
HOME_FAQ_SLUGS = [
    "do-you-repair-every-brand",
    "how-does-diagnostics-work",
    "is-smart-geeks-apple-authorized",
    "do-you-buy-old-devices",
]

# --------------------------------------------------------------------------- #
# Services overview
# --------------------------------------------------------------------------- #

SERVICES_OVERVIEW = {
    "title_tag": f"Repair Services in {CITY}, BC | Smart Geeks",
    "meta_description": (
        "See every repair and trade-in service Smart Geeks offers in Surrey, "
        "BC: laptops, desktops, Mac hardware, printers, consoles, and chip-level work."
    ),
    "h1": "Repair and Trade Services",
    "answer": (
        "Smart Geeks offers device-specific repair diagnostics for laptops, "
        "desktops, Mac computers, printers, and gaming consoles, board-level "
        "chip repair, and a buy-sell-trade service, all from our Surrey, BC location."
    ),
    "intro": [
        "Every device category below has its own diagnostic and repair process "
        "-- a laptop screen replacement and a motherboard-level charging-port "
        "repair aren't remotely the same job, and we've written each service "
        "page to reflect that rather than using one generic template.",
        "Not sure which page fits your issue? Get in touch and describe what's "
        "happening -- we'll point you in the right direction or let you know if "
        "it's outside what we handle.",
    ],
    "how_we_work_heading": "How we approach every repair",
    "how_we_work": [
        "Every device is diagnosed on the bench before we recommend a repair -- "
        "we don't quote blind.",
        "We explain what we found in plain language, including when a repair "
        "isn't realistic or economical.",
        f"{DISCLOSURE_LONG}",
    ],
}

# --------------------------------------------------------------------------- #
# Service areas
# --------------------------------------------------------------------------- #

SERVICE_AREAS_PAGE = {
    "title_tag": f"Service Areas | Smart Geeks {CITY}, BC",
    "meta_description": (
        "Smart Geeks is located in Surrey, BC and serves customers from Surrey, "
        "Delta, Langley, and White Rock for electronics repair and trade-in."
    ),
    "h1": "Service Areas",
    "answer": (
        f"Smart Geeks has one physical location, in {CITY}, BC. Customers from "
        "Delta, Langley, and White Rock regularly drop off devices with us or "
        "arrange service -- we don't operate separate branches in those areas."
    ),
    "intro": (
        "We want to be clear about this upfront: Smart Geeks operates from a "
        f"single location at {BIZ['address']['full_display']}. The areas below "
        "describe where our customers typically come from, not additional storefronts."
    ),
    "areas": {
        "Surrey": (
            f"Our shop is based in {CITY}, at {BIZ['address']['full_display']}. "
            "If you're local, you're welcome to drop by directly or contact us first "
            "to describe the issue."
        ),
        "Delta": (
            "We regularly work with customers from Delta who drop off devices at our "
            "Surrey location. Contact us beforehand if you'd like to talk through the "
            "issue before making the trip."
        ),
        "Langley": (
            "Customers from Langley bring devices to our Surrey shop for diagnostics "
            "and repair. Get in touch first if you have questions about a specific device or fault."
        ),
        "White Rock": (
            "We serve White Rock customers at our Surrey location. If it helps, "
            "describe your issue through the contact form or WhatsApp before you head over."
        ),
    },
    "cta_heading": "Planning to drop off a device?",
    "cta_body": f"Our shop is at {BIZ['address']['full_display']}. Get directions or contact us first if you'd like to describe the issue.",
}

# --------------------------------------------------------------------------- #
# About
# --------------------------------------------------------------------------- #

ABOUT = {
    "title_tag": f"About Smart Geeks | Independent Repair Shop in {CITY}, BC",
    "meta_description": (
        "Smart Geeks is an independently owned electronics repair and "
        "buy-sell-trade shop based in Surrey, BC. Learn how we approach diagnostics and repair."
    ),
    "h1": "About Smart Geeks",
    "answer": (
        f"Smart Geeks is an independently owned electronics repair and "
        f"buy-sell-trade shop based in {CITY}, BC. We are not a manufacturer "
        "and not authorized or certified by one -- we're a local, independent alternative."
    ),
    "intro_paragraphs": [
        f"Smart Geeks is an independently owned and operated repair shop in "
        f"{CITY}, BC, working on laptops, desktop computers, Mac hardware, "
        "printers, and gaming consoles, along with chip-level motherboard "
        "work and a buy-sell-trade service for used electronics.",
        "We started from a simple idea: a repair shop should be able to "
        "explain, in plain language, what's actually wrong with a device "
        "before asking you to pay for a fix. That's the process behind every "
        "page on this site, not just marketing language -- diagnose first, "
        "explain the findings, then repair.",
    ],
    "approach_heading": "How we work",
    "approach_points": [
        ("Diagnose before we quote", "Every device is tested on the bench so a repair recommendation is based on an actual finding, not a guess."),
        ("Say so when we can't help", "Some faults, especially on severely damaged boards, aren't economical to repair. We'll tell you directly rather than stringing out billable attempts."),
        ("Independent, not affiliated", "We are not the manufacturer of any device we service, and we're not authorized or certified by one."),
        ("More than repair", "Our buy-sell-trade service gives devices you're done with a second life, or gets you a tested used device instead of buying new."),
    ],
    "disclosure_heading": "Our relationship to device manufacturers",
    "disclosure_body": DISCLOSURE_LONG,
    "location_heading": "Visit us",
    "location_body": (
        f"You'll find us at {BIZ['address']['full_display']}. We work with "
        "customers from across the Lower Mainland, including Delta, Langley, "
        "and White Rock, who drop off devices at this Surrey location."
    ),
}

# --------------------------------------------------------------------------- #
# FAQs -- sitewide, categorized. No invented prices/turnaround/certifications.
# Each entry has a stable slug so Home can reference a subset by id.
# --------------------------------------------------------------------------- #

FAQ_CATEGORIES = [
    {
        "heading": "General",
        "items": [
            ("do-you-repair-every-brand",
             "Do you repair every brand of laptop or desktop?",
             "We work on the common Windows-based laptop and desktop brands, plus "
             "Mac hardware. If you're not sure whether your specific brand or model "
             "is something we handle, get in touch and describe it -- we'll let you "
             "know directly."),
            ("what-devices-do-you-work-on",
             "What kinds of devices does Smart Geeks work on?",
             "Laptops, desktop computers, printers, gaming consoles, and Mac "
             "hardware (MacBook, iMac, Mac mini), plus chip-level motherboard and "
             "logic board repair, and a buy-sell-trade service for used electronics."),
            ("is-smart-geeks-independent",
             "Is Smart Geeks a manufacturer or an authorized repair centre?",
             "No. Smart Geeks is an independently owned and operated repair shop. "
             "We are not affiliated with, authorized by, or certified by any device "
             "manufacturer."),
        ],
    },
    {
        "heading": "Diagnostics & repair process",
        "items": [
            ("how-does-diagnostics-work",
             "How does your diagnostic process work?",
             "We start with a visual inspection, then run device-specific tests "
             "(power, display, storage, connectivity, or board-level checks "
             "depending on the symptom) to identify the actual cause before "
             "recommending a repair."),
            ("do-you-explain-before-repairing",
             "Will you tell me what's wrong before you fix it?",
             "Yes -- explaining our diagnostic findings before starting repair work "
             "is central to how we operate, not an optional extra."),
            ("what-if-device-cant-be-fixed",
             "What happens if my device can't be repaired?",
             "We'll tell you directly. Not every fault, particularly severe board "
             "damage or corrosion, can be economically repaired, and we won't "
             "continue billing for attempts we don't think will work."),
            ("do-you-do-chip-level-repair",
             "What is chip-level or board-level repair?",
             "It's repair work done directly on a device's motherboard or logic "
             "board -- replacing a charging port, a damaged capacitor, or tracing a "
             "short circuit -- rather than swapping a whole component or board. See "
             "our motherboard and chip-level repair page for more detail."),
        ],
    },
    {
        "heading": "Mac devices",
        "items": [
            ("is-smart-geeks-apple-authorized",
             "Is Smart Geeks authorized or certified by Apple?",
             "No. Smart Geeks is an independent repair shop and is not authorized, "
             "certified, or approved by Apple. We work on MacBook, iMac, and Mac "
             "mini hardware as an independent alternative."),
            ("mac-data-safety",
             "Will working on my Mac put my data at risk?",
             "Some repairs, particularly anything involving storage, can carry that "
             "risk. We recommend backing up beforehand where possible and we'll flag "
             "it directly if a specific repair adds risk to your data."),
        ],
    },
    {
        "heading": "Pricing & policies",
        "items": [
            ("how-much-does-a-repair-cost",
             "How much does a repair cost?",
             "Cost depends on the device, the fault, and the parts required, so we "
             "don't publish a flat price list. We'll walk you through the specifics "
             "after diagnostics, before any repair work begins."),
            ("do-you-offer-a-warranty",
             "Do repairs come with a warranty?",
             "We stand behind the repair work we complete. See our warranty policy "
             "page for the specifics of what's covered -- get in touch if you have a "
             "question about a particular repair."),
            ("whats-your-diagnostic-policy",
             "What's your diagnostic policy?",
             "Our diagnostic policy page explains how we assess devices and "
             "communicate findings before any repair work or cost is committed to."),
        ],
    },
    {
        "heading": "Buy, sell & trade",
        "items": [
            ("do-you-buy-old-devices",
             "Do you buy old or unwanted electronics?",
             "Yes, for the categories we work on -- laptops, desktops, Mac "
             "computers, and gaming consoles. Bring the device in and we'll assess "
             "it in person before making an offer."),
            ("sell-broken-device",
             "Can I sell you a device that doesn't work?",
             "Sometimes, depending on the device and fault. We'll be upfront about "
             "whether it's something we can take when you bring it in."),
        ],
    },
    {
        "heading": "Data & privacy",
        "items": [
            ("do-you-need-my-password",
             "Will you ask for my passwords?",
             "We don't request passwords, PINs, or account credentials through our "
             "contact form. If a repair genuinely requires the device to be "
             "unlocked for testing, we'll talk that through with you in person."),
            ("what-happens-to-my-data",
             "What happens to my data during a repair?",
             "We don't access personal files beyond what's needed to test the "
             "specific fault. Backing up your data beforehand is always a good idea, "
             "especially for storage-related repairs."),
        ],
    },
]


def all_faqs_flat():
    """Flat list of (slug, question, answer) across every category."""
    out = []
    for cat in FAQ_CATEGORIES:
        out.extend(cat["items"])
    return out


def get_faq(slug):
    for cat in FAQ_CATEGORIES:
        for s, q, a in cat["items"]:
            if s == slug:
                return (q, a)
    return None


FAQ_PAGE_META = {
    "title_tag": f"Frequently Asked Questions | Smart Geeks {CITY}, BC",
    "meta_description": (
        "Answers to common questions about Smart Geeks' repair process, "
        "pricing approach, Mac repair, buy-sell-trade, and data privacy."
    ),
    "h1": "Frequently Asked Questions",
    "answer": (
        "Below are answers to the questions we hear most about our repair "
        "process, pricing approach, Mac devices, buy-sell-trade, and how we "
        "handle your data. Don't see your question? Contact us directly."
    ),
}

# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #

CONTACT_PAGE = {
    "title_tag": f"Contact Smart Geeks | {CITY}, BC",
    "meta_description": (
        "Contact Smart Geeks in Surrey, BC by phone, WhatsApp, email, or the "
        "form below to ask about a repair or buy-sell-trade."
    ),
    "h1": "Contact Us",
    "answer": (
        f"Reach Smart Geeks by phone at {BIZ['phone_display']}, by WhatsApp, by "
        f"email at {BIZ['email']}, or with the form below. Our shop is located "
        f"at {BIZ['address']['full_display']}."
    ),
    "intro": (
        "Tell us what's going on with your device and we'll get back to you. "
        "For anything urgent, calling or WhatsApp is the fastest way to reach us."
    ),
    "form_note": (
        "Please don't include passwords, PINs, or account credentials in this "
        "form -- we never need them to respond to your message."
    ),
}

THANK_YOU_PAGE = {
    "title_tag": f"Thanks for Contacting Smart Geeks | {CITY}, BC",
    "meta_description": "Your message to Smart Geeks was received. We'll get back to you soon.",
    "h1": "Thanks -- we've got your message",
    "body": (
        "We've received your message and will get back to you as soon as we "
        "can. If your issue is urgent, calling or messaging us on WhatsApp is "
        "the fastest way to reach us in the meantime."
    ),
    "noindex": True,
}

FOUR_OH_FOUR_PAGE = {
    "title_tag": f"Page Not Found | Smart Geeks {CITY}, BC",
    "meta_description": "The page you're looking for doesn't exist. Find repair services, contact information, and more from Smart Geeks.",
    "h1": "Page not found",
    "body": "The page you were looking for doesn't exist or may have moved. Here are a few places to try instead:",
    "noindex": True,
}

# --------------------------------------------------------------------------- #
# Reviews
# --------------------------------------------------------------------------- #

REVIEWS_PAGE = {
    "title_tag": f"Reviews | Smart Geeks {CITY}, BC",
    "meta_description": (
        "Read Smart Geeks reviews on Google, or leave your own after a repair "
        "or buy-sell-trade visit in Surrey, BC."
    ),
    "h1": "Reviews",
    "answer": (
        "We link directly to our Google listing so you can read reviews there "
        "rather than us curating or displaying a hand-picked selection here."
    ),
    "body": [
        "We'd rather point you to an independent source than hand-pick quotes "
        "for this page. Google Maps hosts our verified customer reviews -- the "
        "link below takes you straight there.",
        "If you've had a repair or a buy-sell-trade experience with us, we'd "
        "genuinely appreciate a review. It helps other people in Surrey find a "
        "repair shop they can trust, and it helps us know what we're getting right.",
    ],
    "cta_label": "Read our reviews on Google",
}

# --------------------------------------------------------------------------- #
# Accessibility statement
# --------------------------------------------------------------------------- #

ACCESSIBILITY_PAGE = {
    "title_tag": f"Accessibility Statement | Smart Geeks {CITY}, BC",
    "meta_description": "Smart Geeks' accessibility statement: our target standard, what we've done, and how to report an issue.",
    "h1": "Accessibility Statement",
    "answer": (
        "Smart Geeks aims to meet WCAG 2.2 Level AA on this website. This "
        "statement explains what that means in practice and how to report an "
        "accessibility issue if you run into one."
    ),
    "body": [
        ("Our target", "We build this website with WCAG 2.2 Level AA as our target "
         "standard, covering things like colour contrast, keyboard navigation, "
         "screen-reader-friendly markup, and visible focus indicators. This is a "
         "target we design and test against, not a claim of independent third-party certification."),
        ("What we've done", "This includes a skip-to-content link, semantic HTML "
         "landmarks and heading structure, labelled form fields, keyboard-operable "
         "navigation and menus, visible focus states, and support for "
         "reduced-motion preferences."),
        ("Known limitations", "Accessibility is an ongoing process. If you "
         "encounter a barrier anywhere on this site, we want to know about it so "
         "we can address it."),
        ("Reporting an issue", f"Email {BIZ['email']} or call {BIZ['phone_display']} "
         "to tell us about any accessibility barrier you run into. Please include "
         "the page and a description of the issue if you can."),
    ],
}
