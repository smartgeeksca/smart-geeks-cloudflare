#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site build for Smart Geeks.

Usage: python3 build.py

Generates the full `public/` output directory:
  - 27 required pages (see CONTENT-INVENTORY.md for the exact list)
  - sitemap.xml, robots.txt, site.webmanifest
  - copies src/assets/* into public/assets/*
  - copies _headers and _redirects into public/ (Cloudflare Pages reads
    these from the build OUTPUT directory, not the repo root)
  - appends a content-hash query string to the shared CSS/JS URLs so
    `_headers`' aggressive `immutable` caching on those files is safe

No network access, no external dependencies beyond the Python standard
library and Pillow (used only by scripts/generate_brand_assets.py, which is
a separate one-time step, already run -- its output is committed under
src/assets/).
"""

import hashlib
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from src.data.business import (  # noqa: E402
    BIZ, SERVICE_AREAS, DISCLOSURE_LONG, WHATSAPP_MESSAGES, whatsapp_href,
)
from src.data.schema import (  # noqa: E402
    local_business_schema, website_schema, webpage_schema, service_schema,
    breadcrumb_schema, faq_schema, contactpage_schema, aboutpage_schema,
)
from src.templates import layout as L  # noqa: E402
from src.assets.icon_glyphs import glyph  # noqa: E402
from src.content.services import SERVICES, BUY_SELL_TRADE, get_service  # noqa: E402
from src.content import pages as P  # noqa: E402
from src.content.legal import ALL_LEGAL_PAGES  # noqa: E402
from src.content.landing import LANDING_PAGES  # noqa: E402

PUBLIC = os.path.join(ROOT, "public")
SITE = BIZ["website"]

ALL_SERVICE_ENTRIES = SERVICES + [BUY_SELL_TRADE]


# --------------------------------------------------------------------------- #
# Utilities
# --------------------------------------------------------------------------- #

def clean_public():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(PUBLIC)


def write_html(url_path: str, html: str):
    """url_path like '/', '/about/', '/services/laptop-repair/'. Writes an
    index.html for clean URLs, except a few special-cased bare filenames."""
    if url_path == "/":
        target_dir = PUBLIC
    else:
        target_dir = os.path.join(PUBLIC, url_path.strip("/"))
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def write_bare_file(filename: str, content: str):
    with open(os.path.join(PUBLIC, filename), "w", encoding="utf-8") as f:
        f.write(content)


def para_list(paragraphs):
    return "\n".join(f"<p>{p}</p>" for p in paragraphs)


def bullet_list(items, cls="bulleted"):
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="{cls}">\n{lis}\n</ul>'


def crumbs(*pairs):
    """pairs like [('Home','/'), ('Services','/services/'), ('Laptop repair', path)]"""
    return list(pairs)


PAGE_LIST = []  # (url_path, priority, changefreq) collected for sitemap.xml, indexable pages only


def register_sitemap(url_path, priority="0.7", changefreq="monthly"):
    PAGE_LIST.append((url_path, priority, changefreq))


# --------------------------------------------------------------------------- #
# Shared building blocks
# --------------------------------------------------------------------------- #

def related_services_block(slugs):
    cards = []
    for slug in slugs:
        s = get_service(slug)
        if not s:
            continue
        cards.append(L.service_card(
            href=f"/services/{s['slug']}/", title=s.get("h1") or s.get("nav_label"),
            summary=s["card_summary"], icon_svg=glyph(s["icon"]),
        ))
    if not cards:
        return ""
    return f"""<section class="section section-alt">
  <div class="container">
    <div class="section-head"><h2>Related services</h2></div>
    <div class="card-grid">
      {''.join(cards)}
    </div>
  </div>
</section>"""


def service_faq_schema_and_html(faqs, heading="Frequently asked questions"):
    html = L.faq_accordion(faqs, heading=heading)
    schema = faq_schema(faqs) if faqs else None
    return html, schema


# --------------------------------------------------------------------------- #
# Home
# --------------------------------------------------------------------------- #

# Device-ecosystem taxonomy -- a presentation-layer grouping only (no new
# service, no content change); motherboard/chip-level work is deliberately
# excluded from the three clusters below because it cuts across all of
# them rather than belonging to one, so it renders as its own capability
# band instead of being force-fit into a cluster it doesn't uniquely suit.
DEVICE_CLUSTERS = [
    ("PC & Windows systems", ["laptop-repair", "desktop-repair"]),
    ("Apple hardware", ["macbook-repair", "imac-repair", "mac-mini-repair"]),
    ("Peripherals & consoles", ["printer-repair", "gaming-console-repair"]),
]
CAPABILITY_SLUG = "motherboard-chip-level-repair"


def device_ecosystem_html(by_slug, extra_slugs=None):
    """Shared by the homepage and the services index -- one grouped-taxonomy
    rendering used in both places instead of two different card grids.
    extra_slugs: services that don't fit any cluster and render as their own
    full-width band instead (default: just the cross-cutting chip-level
    capability; the services index additionally passes buy-sell-trade,
    since that page -- unlike the homepage, which gives it a whole flagship
    section -- has no other place for it to stay discoverable)."""
    cluster_blocks = []
    for label, slugs in DEVICE_CLUSTERS:
        chips = "\n        ".join(
            f'<a class="device-chip" href="/services/{slug}/">'
            f'<span class="device-chip-icon" aria-hidden="true">{glyph(by_slug[slug]["icon"])}</span>'
            f'<span><span class="device-chip-title">{L.esc(by_slug[slug].get("h1") or by_slug[slug]["nav_label"])}</span>'
            f'<span class="device-chip-summary">{L.esc(by_slug[slug]["card_summary"])}</span></span></a>'
            for slug in slugs
        )
        cluster_blocks.append(
            f'<div class="device-cluster"><h3 class="device-cluster-label">{L.esc(label)}</h3>'
            f'<div class="device-cluster-items">\n        {chips}\n      </div></div>'
        )
    cluster_html = "\n    ".join(cluster_blocks)

    extra_slugs = extra_slugs if extra_slugs is not None else [CAPABILITY_SLUG]
    band_blocks = []
    for slug in extra_slugs:
        svc = by_slug[slug]
        label = "Cuts across every category above" if slug == CAPABILITY_SLUG else "Also at our Surrey location"
        band_blocks.append(f"""<a class="capability-band" href="/services/{svc['slug']}/">
      <span class="capability-band-icon" aria-hidden="true">{glyph(svc['icon'])}</span>
      <span class="capability-band-copy">
        <span class="section-label">{label}</span>
        <h3>{L.esc(svc.get('h1') or svc['nav_label'])}</h3>
        <p>{L.esc(svc['card_summary'])}</p>
      </span>
      <span class="capability-band-arrow" aria-hidden="true">&rarr;</span>
    </a>""")
    bands_html = "\n    ".join(band_blocks)
    return f"""<div class="device-ecosystem">
      {cluster_html}
    </div>
    {bands_html}"""


def build_home():
    h = P.HOME
    trust = h["trust_items"]
    by_slug = {s["slug"]: s for s in ALL_SERVICE_ENTRIES}

    # Brand-story statement: the existing why_intro paragraph split at its
    # first sentence boundary -- the opening sentence becomes one large
    # typographic "moment" (the seeing-not-reading fix), the remainder
    # becomes the repair-intelligence section's own intro. Same approved
    # copy, no new sentence written; src/content/pages.py is untouched.
    why_intro = h["why_intro"]
    split_at = why_intro.index(". ") + 1
    statement_text = why_intro[:split_at].strip()
    intel_intro = why_intro[split_at:].strip()

    intel_points_html = "\n      ".join(
        f'<li><h3>{L.esc(t)}</h3><p>{b}</p></li>' for t, b in h["why_points"]
    )
    process_html = "\n      ".join(
        f'<li><span class="step-num">{i+1}</span><div><h3>{L.esc(t)}</h3><p>{b}</p></div></li>'
        for i, (t, b) in enumerate(h["process_steps"])
    )

    ecosystem_html = device_ecosystem_html(by_slug)

    # Buy/Sell/Trade: promoted from "one card among nine" to its own
    # section, reusing BUY_SELL_TRADE's real, already-approved copy verbatim.
    bst = BUY_SELL_TRADE
    bst_tags = "\n      ".join(f"<li>{L.esc(item)}</li>" for item in bst["what_we_accept"])
    bst_wa = whatsapp_href(WHATSAPP_MESSAGES.get(bst["whatsapp_key"], WHATSAPP_MESSAGES["default"]))

    area_items = "".join(f"<li>{L.esc(a)}</li>" for a in SERVICE_AREAS)

    home_faqs = [P.get_faq(slug) for slug in P.HOME_FAQ_SLUGS]
    faq_html = L.faq_accordion(home_faqs, heading=h["faq_heading"], id_prefix="home-faq")

    main_html = f"""
{L.hero(eyebrow=h['hero_eyebrow'], h1=h['hero_h1'], sub=h['hero_sub'], trust_items=trust)}

{L.stat_strip([
    (str(len(ALL_SERVICE_ENTRIES) - 1), "Device categories repaired"),
    (str(len(SERVICE_AREAS)), "Cities served across the Lower Mainland"),
    ("100%", "Independently owned & operated"),
])}

{L.statement_band(statement_text, eyebrow="What we are, and aren't")}

<section class="intel-section">
  <div class="container split-editorial">
    <div class="intel-copy">
      <span class="section-label">How we think about repair</span>
      <h2>{L.esc(h['why_heading'])}</h2>
      <p>{intel_intro}</p>
      <ul class="intel-points">
        {intel_points_html}
      </ul>
    </div>
    <div class="intel-process">
      <ol class="step-list">
        {process_html}
      </ol>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head">
      <span class="section-label">Device ecosystem</span>
      <h2>{L.esc(h['services_heading'])}</h2>
      <p>{h['services_intro']}</p>
    </div>
    {ecosystem_html}
  </div>
</section>

<section class="flagship-split">
  <div class="container split-editorial reverse">
    <div>{L.image_frame('trade', alt='')}</div>
    <div class="flagship-copy">
      <span class="section-label">Also at our Surrey location</span>
      <h2>{L.esc(bst['h1'])}</h2>
      <p>{bst['answer']}</p>
      <ul class="flagship-tags">
        {bst_tags}
      </ul>
      <p class="flagship-note">{bst['sustainability_note']}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/services/buy-sell-trade/">See how it works</a>
        <a class="btn btn-ghost" href="{bst_wa}" target="_blank" rel="noopener">Ask on WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<section class="authority-section">
  <div class="container split-editorial">
    <div>
      <span class="section-label">Local authority</span>
      <h2>{L.esc(h['areas_heading'])}</h2>
      <p>{h['areas_intro']}</p>
      <ul class="authority-areas">{area_items}</ul>
      <p style="margin-top: var(--space-3);"><a class="btn btn-ghost" href="/service-areas/">See service area details</a></p>
    </div>
    <dl class="authority-readout">
      <dt>Location</dt>
      <dd>{L.esc(BIZ['address']['full_display'])}</dd>
      <dt>Phone</dt>
      <dd>{L.esc(BIZ['phone_display_full'])}</dd>
      <dt>Email</dt>
      <dd>{L.esc(BIZ['email'])}</dd>
    </dl>
  </div>
</section>

{faq_html}

{L.cta_block(heading=h['cta_heading'], body=h['cta_body'])}
"""

    schema_objects = [
        local_business_schema(services=ALL_SERVICE_ENTRIES),
        website_schema(),
        webpage_schema("/", h["title_tag"], h["meta_description"]),
    ]

    html = L.page(
        title=h["title_tag"], description=h["meta_description"], path="/",
        main_html=main_html, current_path="/", schema_objects=schema_objects,
    )
    write_html("/", html)
    register_sitemap("/", "1.0", "weekly")


# --------------------------------------------------------------------------- #
# Services overview
# --------------------------------------------------------------------------- #

def build_services_overview():
    d = P.SERVICES_OVERVIEW
    by_slug = {s["slug"]: s for s in ALL_SERVICE_ENTRIES}
    ecosystem_html = device_ecosystem_html(by_slug, extra_slugs=[CAPABILITY_SLUG, "buy-sell-trade"])
    how_items = "\n".join(f"<p>{p}</p>" for p in d["how_we_work"])
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("Services", "/services/")))

    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <h1>{L.esc(d['h1'])}</h1>
      <p class="hero-sub">{d['answer']}</p>
      {para_list(d['intro'])}
    </div>
    {ecosystem_html}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head"><h2>{L.esc(d['how_we_work_heading'])}</h2></div>
    {how_items}
  </div>
</section>
{L.cta_block(heading="Not sure which service fits?", body="Describe the issue and we'll point you to the right place, or let you know if it's outside what we handle.")}
"""
    schema_objects = [
        webpage_schema("/services/", d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("Services", "/services/")]),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/services/",
                  main_html=main_html, current_path="/services/", schema_objects=schema_objects)
    write_html("/services/", html)
    register_sitemap("/services/", "0.9", "monthly")


# --------------------------------------------------------------------------- #
# Individual service pages
# --------------------------------------------------------------------------- #

def build_service_page(s):
    slug = s["slug"]
    path = f"/services/{slug}/"
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("Services", "/services/"), (s["h1"], path)))

    symptoms_html = bullet_list(s["symptoms"]) if "symptoms" in s else ""
    diagnostic_html = para_list(s["diagnostic"]) if "diagnostic" in s else ""
    steps_html = "\n".join(
        f'<li><span class="step-num">{i+1}</span><div><h3>{L.esc(t)}</h3><p>{b}</p></div></li>'
        for i, (t, b) in enumerate(s["repair_steps"])
    )
    factors_html = bullet_list(s["factors"])
    bring_html = bullet_list(s["what_to_bring"])
    faq_html, faq_sch = service_faq_schema_and_html(s["faqs"])
    related_html = related_services_block(s["related"])

    main_html = f"""
{bc}
{L.hero(eyebrow="Repair service", h1=s['h1'], sub=s['answer'], icon_key=s['icon'], whatsapp_key=s['whatsapp_key'])}

<section class="section">
  <div class="container two-col">
    <div>
      <h2>Overview</h2>
      {para_list(s['overview'])}
      {L.disclosure_note(s['disclosure'])}
    </div>
    <div>
      <h2>Common symptoms</h2>
      {symptoms_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container two-col">
    <div>
      <h2>Our diagnostic approach</h2>
      {diagnostic_html}
    </div>
    <div>
      <h2>Factors that may affect service</h2>
      {factors_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><h2>Repair process</h2></div>
    <ol class="step-list">
      {steps_html}
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2>What to bring</h2>
    {bring_html}
  </div>
</section>

{faq_html}
{related_html}
{L.cta_block(heading=f"Ready to talk about your {s['nav_label'].lower()}?", body="Call, WhatsApp, or send a message describing the issue.", whatsapp_key=s['whatsapp_key'])}
"""
    schema_objects = [
        service_schema(s["h1"], s["meta_description"], path, area_served=SERVICE_AREAS),
        webpage_schema(path, s["title_tag"], s["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("Services", "/services/"), (s["h1"], path)]),
        faq_sch,
    ]
    html = L.page(title=s["title_tag"], description=s["meta_description"], path=path,
                  main_html=main_html, current_path=path, schema_objects=schema_objects,
                  whatsapp_key=s["whatsapp_key"])
    write_html(path, html)
    register_sitemap(path, "0.8", "monthly")


def build_buy_sell_trade():
    s = BUY_SELL_TRADE
    slug = s["slug"]
    path = f"/services/{slug}/"
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("Services", "/services/"), (s["h1"], path)))

    accept_html = bullet_list(s["what_we_accept"])
    steps_html = "\n".join(
        f'<li><span class="step-num">{i+1}</span><div><h3>{L.esc(t)}</h3><p>{b}</p></div></li>'
        for i, (t, b) in enumerate(s["assessment_process"])
    )
    factors_html = bullet_list(s["factors"])
    bring_html = bullet_list(s["what_to_bring"])
    faq_html, faq_sch = service_faq_schema_and_html(s["faqs"])
    related_html = related_services_block(s["related"])

    main_html = f"""
{bc}
{L.hero(eyebrow="Buy, sell & trade", h1=s['h1'], sub=s['answer'], icon_key=s['icon'], whatsapp_key=s['whatsapp_key'])}

<section class="section">
  <div class="container two-col">
    <div>
      <h2>Overview</h2>
      {para_list(s['overview'])}
      {L.disclosure_note(s['disclosure'])}
    </div>
    <div>
      <h2>What we accept</h2>
      {accept_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head"><h2>How an assessment works</h2></div>
    <ol class="step-list">
      {steps_html}
    </ol>
  </div>
</section>

<section class="section">
  <div class="container two-col">
    <div>
      <h2>Factors that affect an offer</h2>
      {factors_html}
    </div>
    <div>
      <h2>What to bring</h2>
      {bring_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <p class="disclosure-note">{s['sustainability_note']}</p>
  </div>
</section>

{faq_html}
{related_html}
{L.cta_block(heading="Have a device to sell or trade?", body="Bring it in for an in-person assessment, or contact us first with a few details.", whatsapp_key=s['whatsapp_key'])}
"""
    schema_objects = [
        service_schema(s["h1"], s["meta_description"], path, area_served=SERVICE_AREAS),
        webpage_schema(path, s["title_tag"], s["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("Services", "/services/"), (s["h1"], path)]),
        faq_sch,
    ]
    html = L.page(title=s["title_tag"], description=s["meta_description"], path=path,
                  main_html=main_html, current_path=path, schema_objects=schema_objects,
                  whatsapp_key=s["whatsapp_key"])
    write_html(path, html)
    register_sitemap(path, "0.8", "monthly")


# --------------------------------------------------------------------------- #
# Service areas
# --------------------------------------------------------------------------- #

def build_service_areas():
    d = P.SERVICE_AREAS_PAGE
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("Service areas", "/service-areas/")))
    area_sections = []
    for name, body in d["areas"].items():
        area_sections.append(f"""<div class="info-card">
      <h3>{L.esc(name)}</h3>
      <p>{body}</p>
    </div>""")
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container">
    <h1>{L.esc(d['h1'])}</h1>
    <p class="hero-sub">{d['answer']}</p>
    <p>{d['intro']}</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container card-grid">
    {''.join(area_sections)}
  </div>
</section>
{L.cta_block(heading=d['cta_heading'], body=d['cta_body'])}
"""
    schema_objects = [
        webpage_schema("/service-areas/", d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("Service areas", "/service-areas/")]),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/service-areas/",
                  main_html=main_html, current_path="/service-areas/", schema_objects=schema_objects)
    write_html("/service-areas/", html)
    register_sitemap("/service-areas/", "0.6")


# --------------------------------------------------------------------------- #
# About
# --------------------------------------------------------------------------- #

def build_about():
    d = P.ABOUT
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("About", "/about/")))
    approach_html = "\n".join(
        f'<div class="info-card"><h3>{L.esc(t)}</h3><p class="text-muted">{b}</p></div>'
        for t, b in d["approach_points"]
    )
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container two-col">
    <div>
      <h1>{L.esc(d['h1'])}</h1>
      <p class="hero-sub">{d['answer']}</p>
      {para_list(d['intro_paragraphs'])}
    </div>
    <div>{L.image_frame('shield', alt='')}</div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head"><h2>{L.esc(d['approach_heading'])}</h2></div>
    <div class="card-grid">{approach_html}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2>{L.esc(d['disclosure_heading'])}</h2>
    <p class="disclosure-note">{d['disclosure_body']}</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2>{L.esc(d['location_heading'])}</h2>
    <p>{d['location_body']}</p>
  </div>
</section>
{L.cta_block(heading="Questions before you bring your device in?", body="We're happy to talk through the issue first.")}
"""
    schema_objects = [
        aboutpage_schema("/about/", d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("About", "/about/")]),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/about/",
                  main_html=main_html, current_path="/about/", schema_objects=schema_objects)
    write_html("/about/", html)
    register_sitemap("/about/", "0.6")


# --------------------------------------------------------------------------- #
# FAQs
# --------------------------------------------------------------------------- #

def build_faqs():
    d = P.FAQ_PAGE_META
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("FAQs", "/faqs/")))
    all_pairs = []
    cat_sections = []
    for cat in P.FAQ_CATEGORIES:
        qa_pairs = [(q, a) for (_slug, q, a) in cat["items"]]
        all_pairs.extend(qa_pairs)
        cat_sections.append(L.faq_accordion(qa_pairs, heading=cat["heading"], id_prefix=cat["heading"].lower().replace(" & ", "-").replace(" ", "-")))
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container">
    <h1>{L.esc(d['h1'])}</h1>
    <p class="hero-sub">{d['answer']}</p>
  </div>
</section>
{''.join(cat_sections)}
{L.cta_block(heading="Still have a question?", body="Contact us directly and we'll get back to you.")}
"""
    schema_objects = [
        webpage_schema("/faqs/", d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("FAQs", "/faqs/")]),
        faq_schema(all_pairs),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/faqs/",
                  main_html=main_html, current_path="/faqs/", schema_objects=schema_objects)
    write_html("/faqs/", html)
    register_sitemap("/faqs/", "0.7")


# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #

def contact_form_html(page_value="contact"):
    return f"""<form class="form-grid" action="/api/contact" method="POST" id="contact-form" data-sg-form novalidate>
  <input type="hidden" name="page" value="{L.esc(page_value)}">
  <div class="hp-field" aria-hidden="true">
    <label for="website">Leave this field empty</label>
    <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
  </div>

  <div class="form-field">
    <label for="name">Name <span class="req">*</span></label>
    <input type="text" id="name" name="name" required maxlength="100" autocomplete="name">
    <span class="field-error" data-error-for="name"></span>
  </div>

  <div class="form-field">
    <label for="contact">Email or phone <span class="req">*</span></label>
    <input type="text" id="contact" name="contact" required maxlength="150" autocomplete="email">
    <span class="field-error" data-error-for="contact"></span>
  </div>

  <div class="form-field">
    <label for="device">Device type <span class="req">*</span></label>
    <select id="device" name="device" required>
      <option value="">Select a device</option>
      <option>Laptop</option>
      <option>Desktop computer</option>
      <option>MacBook</option>
      <option>iMac</option>
      <option>Mac mini</option>
      <option>Printer</option>
      <option>Gaming console</option>
      <option>Other / not sure</option>
    </select>
    <span class="field-error" data-error-for="device"></span>
  </div>

  <div class="form-field">
    <label for="message">Briefly describe the issue <span class="req">*</span></label>
    <textarea id="message" name="message" required maxlength="1000"></textarea>
    <span class="field-error" data-error-for="message"></span>
  </div>

  <fieldset class="form-field">
    <legend>Preferred contact method</legend>
    <div class="form-radio-group">
      <label><input type="radio" name="preferred_contact" value="phone" checked> Phone</label>
      <label><input type="radio" name="preferred_contact" value="email"> Email</label>
      <label><input type="radio" name="preferred_contact" value="whatsapp"> WhatsApp</label>
    </div>
  </fieldset>

  <p class="form-note">{P.CONTACT_PAGE['form_note']}</p>

  <label class="form-consent">
    <input type="checkbox" name="consent" value="yes" required>
    <span>I agree to be contacted by Smart Geeks about this message. <span class="req">*</span></span>
  </label>

  <div>
    <button type="submit" class="btn btn-primary btn-lg">Send message</button>
  </div>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def build_contact():
    d = P.CONTACT_PAGE
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("Contact", "/contact/")))
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container two-col">
    <div>
      <h1>{L.esc(d['h1'])}</h1>
      <p class="hero-sub">{d['answer']}</p>
      <p>{d['intro']}</p>
      {contact_form_html('contact')}
    </div>
    <div>
      <div class="info-card">
        <h3>Visit us</h3>
        <address>{L.esc(BIZ['name'])}<br>{L.esc(BIZ['address']['street'])}<br>{L.esc(BIZ['address']['city'])}, {L.esc(BIZ['address']['region'])} {L.esc(BIZ['address']['postal_code'])}</address>
        <p><a href="{L.esc(BIZ['maps_url'])}" target="_blank" rel="noopener" data-track="direction_click">Get directions</a></p>
      </div>
      <div class="info-card" style="margin-top:1rem;">
        <h3>Call, email, or message</h3>
        <p><a href="{BIZ['tel_href']}" data-track="phone_click">{L.esc(BIZ['phone_display_full'])}</a></p>
        <p><a href="{BIZ['mailto_href']}">{L.esc(BIZ['email'])}</a></p>
        <p><a href="{L.esc(whatsapp_href(WHATSAPP_MESSAGES['default']))}" target="_blank" rel="noopener" data-track="whatsapp_click">WhatsApp us</a></p>
      </div>
    </div>
  </div>
</section>
"""
    schema_objects = [
        contactpage_schema("/contact/", d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("Contact", "/contact/")]),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/contact/",
                  main_html=main_html, current_path="/contact/", schema_objects=schema_objects)
    write_html("/contact/", html)
    register_sitemap("/contact/", "0.8")


# --------------------------------------------------------------------------- #
# Reviews
# --------------------------------------------------------------------------- #

def build_reviews():
    d = P.REVIEWS_PAGE
    bc = L.breadcrumbs(crumbs(("Home", "/"), ("Reviews", "/reviews/")))
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container">
    <h1>{L.esc(d['h1'])}</h1>
    <p class="hero-sub">{d['answer']}</p>
    {para_list(d['body'])}
    <p><a class="btn btn-primary btn-lg" href="{L.esc(BIZ['maps_url'])}" target="_blank" rel="noopener">{L.esc(d['cta_label'])}</a></p>
  </div>
</section>
{L.cta_block(heading="Had a repair or trade with us?", body="A short review helps other people in Surrey find us, and helps us know what we're getting right.")}
"""
    schema_objects = [
        webpage_schema("/reviews/", d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), ("Reviews", "/reviews/")]),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/reviews/",
                  main_html=main_html, current_path="/reviews/", schema_objects=schema_objects)
    write_html("/reviews/", html)
    register_sitemap("/reviews/", "0.6")


# --------------------------------------------------------------------------- #
# Legal / policy pages
# --------------------------------------------------------------------------- #

def build_legal_page(entry):
    path = f"/{entry['slug']}/"
    bc = L.breadcrumbs(crumbs(("Home", "/"), (entry["h1"], path)))
    sections_html = "\n".join(
        f"<h2>{L.esc(h)}</h2>\n<p>{b}</p>" for h, b in entry["sections"]
    )
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container">
    <h1>{L.esc(entry['h1'])}</h1>
    <p class="hero-sub">{entry['intro']}</p>
    {sections_html}
  </div>
</section>
"""
    schema_objects = [
        webpage_schema(path, entry["title_tag"], entry["meta_description"]),
        breadcrumb_schema([("Home", "/"), (entry["h1"], path)]),
    ]
    html = L.page(title=entry["title_tag"], description=entry["meta_description"], path=path,
                  main_html=main_html, current_path=path, schema_objects=schema_objects)
    write_html(path, html)
    register_sitemap(path, "0.3", "yearly")


# --------------------------------------------------------------------------- #
# Accessibility statement
# --------------------------------------------------------------------------- #

def build_accessibility():
    d = P.ACCESSIBILITY_PAGE
    path = "/accessibility-statement/"
    bc = L.breadcrumbs(crumbs(("Home", "/"), (d["h1"], path)))
    sections_html = "\n".join(f"<h2>{L.esc(h)}</h2>\n<p>{b}</p>" for h, b in d["body"])
    main_html = f"""
{bc}
<section class="section-tight">
  <div class="container">
    <h1>{L.esc(d['h1'])}</h1>
    <p class="hero-sub">{d['answer']}</p>
    {sections_html}
  </div>
</section>
"""
    schema_objects = [
        webpage_schema(path, d["title_tag"], d["meta_description"]),
        breadcrumb_schema([("Home", "/"), (d["h1"], path)]),
    ]
    html = L.page(title=d["title_tag"], description=d["meta_description"], path=path,
                  main_html=main_html, current_path=path, schema_objects=schema_objects)
    write_html(path, html)
    register_sitemap(path, "0.3", "yearly")


# --------------------------------------------------------------------------- #
# Thank-you / 404
# --------------------------------------------------------------------------- #

def build_thank_you():
    d = P.THANK_YOU_PAGE
    main_html = f"""
<section class="error-page">
  <div class="container">
    <h1>{L.esc(d['h1'])}</h1>
    <p>{d['body']}</p>
    <p>
      <a class="btn btn-primary" href="{BIZ['tel_href']}">Call {L.esc(BIZ['phone_display'])}</a>
      <a class="btn btn-secondary" href="{L.esc(whatsapp_href(WHATSAPP_MESSAGES['default']))}" target="_blank" rel="noopener">WhatsApp us</a>
      <a class="btn btn-ghost" href="/">Back to home</a>
    </p>
  </div>
</section>
"""
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/thank-you/",
                  main_html=main_html, current_path="/thank-you/", noindex=True)
    write_html("/thank-you/", html)


def build_404():
    d = P.FOUR_OH_FOUR_PAGE
    main_html = f"""
<section class="error-page">
  <div class="container">
    <h1>{L.esc(d['h1'])}</h1>
    <p>{d['body']}</p>
    <div class="card-grid" style="max-width:640px;margin:2rem auto 0;text-align:left;">
      {L.service_card(href='/', title='Home', summary='Start from the homepage.', icon_svg=glyph('diagnose'))}
      {L.service_card(href='/services/', title='Services', summary='Browse every repair and trade service.', icon_svg=glyph('chip'))}
      {L.service_card(href='/contact/', title='Contact', summary='Get in touch about your device.', icon_svg=glyph('shield'))}
    </div>
  </div>
</section>
"""
    html = L.page(title=d["title_tag"], description=d["meta_description"], path="/404.html",
                  main_html=main_html, current_path="/404.html", noindex=True)
    write_bare_file("404.html", html)


# --------------------------------------------------------------------------- #
# Google Ads landing pages
# --------------------------------------------------------------------------- #

def build_landing_page(lp):
    path = f"/landing/{lp['slug']}/"
    trust_html = bullet_list(lp["trust_points"])
    faq_html, faq_sch = service_faq_schema_and_html(lp["faqs"], heading="Common questions")
    related_html = related_services_block(lp["related_service_slugs"])

    main_html = f"""
{L.hero(eyebrow=lp['campaign_label'], h1=lp['h1'], sub=lp['sub'], whatsapp_key=lp['whatsapp_key'])}

<section class="section">
  <div class="container two-col">
    <div>
      {para_list(lp['intro'])}
      <h2>Why Smart Geeks</h2>
      {trust_html}
      <p class="disclosure-note">{DISCLOSURE_LONG}</p>
    </div>
    <div>
      <div class="info-card">
        <h3>Get in touch</h3>
        {contact_form_html(lp['slug'])}
      </div>
    </div>
  </div>
</section>

{faq_html}
{related_html}

<section class="section section-alt">
  <div class="container">
    <h2>Visit or contact us</h2>
    <p><strong>{L.esc(BIZ['name'])}</strong> &mdash; {L.esc(BIZ['address']['full_display'])}</p>
    <p>
      <a class="btn btn-primary" href="{BIZ['tel_href']}" data-track="phone_click">Call {L.esc(BIZ['phone_display'])}</a>
      <a class="btn btn-secondary" href="{L.esc(whatsapp_href(WHATSAPP_MESSAGES.get(lp['whatsapp_key'], WHATSAPP_MESSAGES['default'])))}" target="_blank" rel="noopener" data-track="whatsapp_click">WhatsApp us</a>
    </p>
    <p class="text-muted">
      <a href="/privacy-policy/">Privacy policy</a> &middot;
      <a href="/terms-of-service/">Terms of service</a> &middot;
      <a href="/warranty-policy/">Warranty policy</a> &middot;
      <a href="/diagnostic-policy/">Diagnostic policy</a>
    </p>
  </div>
</section>
"""
    schema_objects = [
        webpage_schema(path, lp["title_tag"], lp["meta_description"]),
        faq_sch,
    ]
    html = L.page(title=lp["title_tag"], description=lp["meta_description"], path=path,
                  main_html=main_html, current_path=path, schema_objects=schema_objects,
                  whatsapp_key=lp["whatsapp_key"])
    write_html(path, html)
    register_sitemap(path, "0.5")


# --------------------------------------------------------------------------- #
# sitemap.xml / robots.txt / site.webmanifest
# --------------------------------------------------------------------------- #

def build_sitemap():
    urls = []
    for path, priority, freq in PAGE_LIST:
        loc = SITE.rstrip("/") + path
        urls.append(
            f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{priority}</priority></url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n"
    )
    write_bare_file("sitemap.xml", xml)


def build_robots():
    txt = f"""User-agent: *
Allow: /

Sitemap: {SITE.rstrip('/')}/sitemap.xml
"""
    write_bare_file("robots.txt", txt)


def build_webmanifest():
    manifest = {
        "name": BIZ["name"],
        "short_name": BIZ["short_name"],
        "description": BIZ["description_short"],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#F5F7FA",
        "theme_color": "#0A1A2F",
        "icons": [
            {"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    write_bare_file("site.webmanifest", json.dumps(manifest, indent=2))


# --------------------------------------------------------------------------- #
# Asset copying + cache-busting
# --------------------------------------------------------------------------- #

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


def copy_assets():
    src_assets = os.path.join(ROOT, "src", "assets")
    dst_assets = os.path.join(PUBLIC, "assets")
    for sub in ("css", "js", "images", "icons"):
        shutil.copytree(os.path.join(src_assets, sub), os.path.join(dst_assets, sub))

    shutil.copy(os.path.join(ROOT, "_headers"), os.path.join(PUBLIC, "_headers"))
    shutil.copy(os.path.join(ROOT, "_redirects"), os.path.join(PUBLIC, "_redirects"))


def apply_cache_busting():
    css_hash = file_hash(os.path.join(PUBLIC, "assets", "css", "style.css"))
    js_hash = file_hash(os.path.join(PUBLIC, "assets", "js", "main.js"))
    old_css = '/assets/css/style.css"'
    new_css = f'/assets/css/style.css?v={css_hash}"'
    old_js = '/assets/js/main.js"'
    new_js = f'/assets/js/main.js?v={js_hash}"'
    count = 0
    for dirpath, _dirnames, filenames in os.walk(PUBLIC):
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = content.replace(old_css, new_css).replace(old_js, new_js)
            if new_content != content:
                count += 1
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)
    return count, css_hash, js_hash


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    clean_public()

    build_home()
    build_services_overview()
    for s in SERVICES:
        build_service_page(s)
    build_buy_sell_trade()
    build_service_areas()
    build_about()
    build_faqs()
    build_contact()
    build_reviews()
    for entry in ALL_LEGAL_PAGES:
        build_legal_page(entry)
    build_accessibility()
    build_thank_you()
    build_404()
    # Repair "Ads landing pages" are retired as of the 2026-09-01 policy
    # recovery pass -- see src/content/landing.py's header and
    # URL-MIGRATION-MAP.md. No longer built; the four old paths are
    # 301-redirected to their real service-page equivalents via the root
    # _redirects file instead. Do not re-add this loop without first
    # re-checking CAMPAIGN-ELIGIBILITY-MATRIX.md.
    # for lp in LANDING_PAGES:
    #     build_landing_page(lp)

    copy_assets()
    build_webmanifest()
    build_sitemap()
    build_robots()
    count, css_hash, js_hash = apply_cache_busting()

    html_count = sum(len(files) for _, _, files in os.walk(PUBLIC) if any(f.endswith(".html") for f in files))
    print(f"Build complete: public/ generated.")
    print(f"  CSS hash: {css_hash}  JS hash: {js_hash}  (applied to {count} HTML files)")
    print(f"  Sitemap entries: {len(PAGE_LIST)}")


if __name__ == "__main__":
    main()
