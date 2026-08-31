# -*- coding: utf-8 -*-
"""
Original legal/policy page content: Privacy Policy, Terms of Service,
Warranty Policy, Diagnostic Policy.

These are drafted in good faith to be accurate and non-fabricated (no
invented warranty duration, no invented diagnostic fee, no fabricated legal
certifications), but they are NOT a substitute for a lawyer's review. Each
page says so, and README/QA-REPORT flag final legal review as an owner
action item before launch.
"""

from src.data.business import BIZ

EFFECTIVE_DATE = "This policy was last updated in 2026 and should be reviewed periodically."

LEGAL_REVIEW_NOTE = (
    "This page was drafted to be accurate and complete, but it has not been "
    "reviewed by a lawyer. Please treat it as a starting point pending your "
    "own legal review, not as legal advice."
)

# --------------------------------------------------------------------------- #
PRIVACY_POLICY = {
    "slug": "privacy-policy",
    "title_tag": "Privacy Policy | Smart Geeks",
    "meta_description": "How Smart Geeks collects, uses, and protects information submitted through this website.",
    "h1": "Privacy Policy",
    "intro": (
        f"This policy explains what information {BIZ['name']} collects through "
        "this website, how it's used, and how you can ask us about it. "
        + LEGAL_REVIEW_NOTE
    ),
    "sections": [
        ("Information we collect",
         "When you use our contact form, we collect what you enter: your name, "
         "your email address or phone number, the device type, a short "
         "description of your issue, and your preferred contact method. We do "
         "not ask for passwords, PINs, payment card numbers, or other account "
         "credentials through this form, and you should never enter them there."),
        ("How we use it",
         "We use the information you submit only to respond to your message -- "
         "to follow up about a repair, a quote, or a buy-sell-trade question. "
         "We do not sell your information, and we do not use it for unrelated "
         "marketing without your separate consent."),
        ("Where it's processed",
         "Contact form submissions are processed through Cloudflare's "
         "infrastructure and, where a transactional email provider is "
         "configured, delivered to our inbox through that provider. See our "
         "Terms of Service for how the site itself is hosted."),
        ("Analytics and cookies",
         "This site may use privacy-conscious analytics (Google Analytics 4) "
         "and Google Ads conversion tracking, but only once we've configured a "
         "live measurement ID -- no tracking scripts run otherwise. When "
         "active, analytics does not receive the contents of your contact form "
         "or any personally identifying information you submit there; it "
         "records anonymized events like a phone-number click or a form "
         "submission occurring, not what you wrote."),
        ("Data retention",
         "We retain contact form submissions only as long as reasonably "
         "necessary to respond to your inquiry and keep basic business records."),
        ("Your rights",
         "You can ask us what information we hold about you, ask us to correct "
         "it, or ask us to delete it, subject to any legitimate business or "
         "legal record-keeping needs. Contact us using the details below."),
        ("Contact us about privacy",
         f"Email {BIZ['email']} or call {BIZ['phone_display']} with any privacy "
         "question or request."),
    ],
}

# --------------------------------------------------------------------------- #
TERMS_OF_SERVICE = {
    "slug": "terms-of-service",
    "title_tag": "Terms of Service | Smart Geeks",
    "meta_description": "The terms that apply to using this website and to repair, diagnostic, and buy-sell-trade services from Smart Geeks.",
    "h1": "Terms of Service",
    "intro": (
        f"These terms apply to your use of this website and to repair, "
        f"diagnostic, and buy-sell-trade services provided by {BIZ['name']}. "
        + LEGAL_REVIEW_NOTE
    ),
    "sections": [
        ("Who we are",
         f"{BIZ['name']} is an independently owned and operated electronics "
         f"repair and buy-sell-trade business located at "
         f"{BIZ['address']['full_display']}. We are not affiliated with, "
         "authorized by, or endorsed by any device manufacturer."),
        ("Diagnostics before repair",
         "We diagnose a device before recommending or beginning repair work "
         "and communicate our findings to you first. See our Diagnostic Policy "
         "for details."),
        ("No guaranteed outcome",
         "Electronics repair, and chip-level board repair in particular, "
         "cannot be guaranteed to succeed in every case. Some devices, "
         "especially those with severe corrosion or board damage, may not be "
         "economically repairable. We will tell you if that's the case rather "
         "than continuing to bill for further attempts."),
        ("Your data and backups",
         "You're responsible for backing up your data before dropping off a "
         "device wherever that's possible. Some repairs, particularly those "
         "involving storage components, carry a risk to data that we cannot "
         "eliminate. We do not access personal files beyond what's needed to "
         "diagnose or verify a repair."),
        ("Devices left with us",
         "Please remove or back up personal data you're not comfortable with "
         "us encountering during testing. Devices should be picked up within a "
         "reasonable time after we notify you that work is complete; contact "
         "us if you need more time."),
        ("Buy-sell-trade transactions",
         "Offers made for buying or trading a device are based on an in-person "
         "assessment and are not binding until both parties agree. We may "
         "decline to purchase or accept a trade-in for any device."),
        ("Pricing",
         "We do not publish a fixed price list because cost depends on the "
         "device, the fault, and parts required. Pricing is communicated to "
         "you after diagnostics and before repair work begins."),
        ("Website use",
         "This website is provided for informational purposes about our "
         "services. Content is original to Smart Geeks; device and "
         "manufacturer names referenced are trademarks of their respective "
         "owners, used only to identify compatible services."),
        ("Limitation of liability",
         "To the extent permitted by law, Smart Geeks' liability in connection "
         "with a repair or transaction is limited to the amount paid for that "
         "specific service. We are not liable for data loss, indirect, or "
         "consequential damages arising from a repair, except where such "
         "liability cannot be excluded by law."),
        ("Governing law",
         "These terms are governed by the laws of British Columbia and the "
         "federal laws of Canada applicable in it."),
        ("Changes to these terms",
         "We may update these terms from time to time. The current version "
         "will always be posted on this page."),
        ("Contact",
         f"Questions about these terms can be sent to {BIZ['email']} or "
         f"{BIZ['phone_display']}."),
    ],
}

# --------------------------------------------------------------------------- #
WARRANTY_POLICY = {
    "slug": "warranty-policy",
    "title_tag": "Warranty Policy | Smart Geeks",
    "meta_description": "How Smart Geeks handles warranty coverage on completed repairs.",
    "h1": "Warranty Policy",
    "intro": (
        "We stand behind the repair work we complete. This page explains how "
        "our warranty works in general terms. " + LEGAL_REVIEW_NOTE
    ),
    "sections": [
        ("What's covered",
         "Repairs completed by Smart Geeks are covered against defects in the "
         "specific parts we installed and the workmanship of the repair itself, "
         "for the period communicated to you in writing at the time of repair."),
        ("Why we don't publish a fixed duration here",
         "Warranty coverage can reasonably vary by repair type and part used, "
         "so rather than publish a single duration that wouldn't apply "
         "accurately to every repair, we confirm the specific warranty period "
         "in writing on your invoice or repair confirmation at the time of service."),
        ("What's not covered",
         "New damage unrelated to the original repair (for example, a new "
         "drop or liquid exposure after pickup), issues caused by third-party "
         "repair attempts after our work, and normal wear and tear are not "
         "covered under repair warranty."),
        ("Chip-level and board-level repairs",
         "Board-level and chip-level repairs are inherently higher-risk than "
         "standard part replacement. We'll be specific about what is and isn't "
         "covered for this category of repair at the time of service."),
        ("Making a warranty claim",
         f"If you believe a completed repair has failed within its warranty "
         f"period, contact us at {BIZ['email']} or {BIZ['phone_display']} with "
         "your invoice or repair reference so we can look into it."),
    ],
}

# --------------------------------------------------------------------------- #
DIAGNOSTIC_POLICY = {
    "slug": "diagnostic-policy",
    "title_tag": "Diagnostic Policy | Smart Geeks",
    "meta_description": "How Smart Geeks diagnoses a device and communicates findings before any repair work or cost is committed to.",
    "h1": "Diagnostic Policy",
    "intro": (
        "Every device we work on is diagnosed before we recommend or begin "
        "repair work. This page explains how that process works. " + LEGAL_REVIEW_NOTE
    ),
    "sections": [
        ("What diagnostics involves",
         "Depending on the device and symptom, diagnostics can include a "
         "visual inspection, power-on and POST testing, component-level "
         "testing (battery, storage, memory, display, graphics), connectivity "
         "checks, or board-level testing with a multimeter for no-power and "
         "charging faults."),
        ("Findings before repair",
         "We explain what we found in plain language, and what the realistic "
         "repair options are, before any repair work begins or further cost is committed."),
        ("Diagnostic fees",
         "Whether a diagnostic fee applies, and how much it is, depends on the "
         "device and the complexity of the issue. Any applicable fee is "
         "communicated to you clearly before we begin, so there's no surprise "
         "charge for the diagnostic itself."),
        ("When a repair isn't realistic",
         "Some faults -- particularly severe corrosion, physical board damage, "
         "or discontinued parts -- may not be economically repairable. We'll "
         "tell you directly if that's what our diagnostics show, rather than "
         "continuing to bill for further attempts."),
        ("Data during diagnostics",
         "We access only what's necessary to test the specific fault reported. "
         "We recommend backing up your data beforehand, particularly for "
         "storage-related issues."),
        ("Questions about your diagnostic",
         f"Contact us at {BIZ['email']} or {BIZ['phone_display']} if you have "
         "questions about a diagnostic finding or recommended repair."),
    ],
}

ALL_LEGAL_PAGES = [PRIVACY_POLICY, TERMS_OF_SERVICE, WARRANTY_POLICY, DIAGNOSTIC_POLICY]
