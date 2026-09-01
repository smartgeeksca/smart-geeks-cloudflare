# -*- coding: utf-8 -*-
"""
Shared HTML template system for the Smart Geeks static site.

Design intent (see DESIGN-NOTES section in README.md for the full rationale):
  - Sticky header: wordmark + horizontal nav + persistent phone CTA, matching
    the general structural convention of the smartgeeks.ca reference site
    (logo-left, nav-centre, phone-right, sticky-on-scroll) -- rebuilt here in
    original markup, CSS, and copy.
  - Hero: headline + one-line subhead + dual CTA (call / contact), used
    consistently across service and landing pages.
  - Card grid for services, consistent spacing scale (8px baseline).
  - Footer: four-column layout (services / company / policies / contact+social).
  - Mobile nav and FAQ accordions use native <details>/<summary> so the site
    is fully usable with JavaScript disabled; main.js only progressively
    enhances the contact form and (optionally gated) analytics events.
"""

from src.data.business import (
    BIZ, NAV_LINKS, FOOTER_COLUMNS, SOCIAL_LINKS, DISCLOSURE_SHORT,
    whatsapp_href, WHATSAPP_MESSAGES, ANALYTICS_CONFIG,
)
from src.data.schema import to_script_tag
import json as _json

SITE = BIZ["website"]
CURRENT_YEAR = 2026


def esc(text: str) -> str:
    """Minimal HTML-attribute/text escaping for interpolated strings."""
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# Analytics -- inert unless the owner has supplied a real GA4 ID. No fake
# measurement IDs ship in this project; ANALYTICS_CONFIG values are None
# until the owner sets them in src/data/business.py.
# ---------------------------------------------------------------------------

def analytics_snippet() -> str:
    ga4_id = ANALYTICS_CONFIG.get("ga4_measurement_id")
    config_json = _json.dumps({
        "ga4MeasurementId": ga4_id,
        "googleAdsConversionId": ANALYTICS_CONFIG.get("google_ads_conversion_id"),
        "conversionLabels": ANALYTICS_CONFIG.get("google_ads_conversion_labels", {}),
    })
    if not ga4_id:
        # No live ID: still expose the (empty) config so main.js's tracking
        # helper can no-op safely, but never load gtag.js.
        return f'<script>window.__SG_ANALYTICS_CONFIG = {config_json};</script>'
    return f"""<script>window.__SG_ANALYTICS_CONFIG = {config_json};</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={esc(ga4_id)}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{ dataLayer.push(arguments); }}
  gtag('js', new Date());
  gtag('config', '{esc(ga4_id)}', {{ anonymize_ip: true }});
</script>"""


# ---------------------------------------------------------------------------
# <head>
# ---------------------------------------------------------------------------

def head(*, title, description, path, og_image=None, noindex=False, extra_schema_html=""):
    canonical = SITE.rstrip("/") + path
    og_image_url = og_image or (SITE.rstrip("/") + "/assets/images/og-default.svg")
    robots = "noindex, nofollow" if noindex else "index, follow"
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0A1A2F">
<link rel="icon" href="/assets/icons/favicon.ico" sizes="any">
<link rel="icon" href="/assets/icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BIZ['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_image_url)}">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(og_image_url)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Space+Grotesk:wght@500;700&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_schema_html}
{analytics_snippet()}""".strip("\n")


# ---------------------------------------------------------------------------
# Header / nav
# ---------------------------------------------------------------------------

def header_nav(current_path: str) -> str:
    links_html = []
    for item in NAV_LINKS:
        active = " aria-current=\"page\"" if item["href"] == current_path else ""
        links_html.append(
            f'<li><a href="{esc(item["href"])}"{active}>{esc(item["label"])}</a></li>'
        )
    links_joined = "\n          ".join(links_html)

    return f"""<header class="site-header">
  <div class="container header-inner">
    <a class="wordmark" href="/" aria-label="{esc(BIZ['name'])} home">
      <img src="/assets/icons/icon.svg" alt="" width="32" height="32" class="wordmark-icon">
      <span>{esc(BIZ['name'])}</span>
    </a>

    <nav class="primary-nav" aria-label="Primary">
      <ul>
        {links_joined}
      </ul>
    </nav>

    <div class="header-actions">
      <a class="btn btn-ghost header-phone" href="{BIZ['tel_href']}">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.5 21 3 13.5 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.3 1L6.6 10.8Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
        <span>{esc(BIZ['phone_display'])}</span>
      </a>
      <a class="btn btn-primary" href="/contact/">Contact us</a>
    </div>

    <details class="mobile-nav">
      <summary aria-label="Open menu">
        <span class="mobile-nav-icon" aria-hidden="true"></span>
        <span class="sr-only">Menu</span>
      </summary>
      <div class="mobile-nav-panel">
        <ul>
          {links_joined}
        </ul>
        <div class="mobile-nav-actions">
          <a class="btn btn-primary" href="{BIZ['tel_href']}">Call {esc(BIZ['phone_display'])}</a>
          <a class="btn btn-secondary" href="{whatsapp_href(WHATSAPP_MESSAGES['default'])}" target="_blank" rel="noopener">WhatsApp us</a>
        </div>
      </div>
    </details>
  </div>
</header>"""


def skip_link() -> str:
    return '<a href="#main-content" class="skip-link">Skip to main content</a>'


# ---------------------------------------------------------------------------
# Sticky mobile action bar (pure CSS position: sticky, no JS required)
# ---------------------------------------------------------------------------

def mobile_action_bar(whatsapp_key="default") -> str:
    wa = whatsapp_href(WHATSAPP_MESSAGES.get(whatsapp_key, WHATSAPP_MESSAGES["default"]))
    return f"""<div class="mobile-action-bar" role="navigation" aria-label="Quick contact">
  <a href="{BIZ['tel_href']}" data-track="phone_click" class="mab-item">
    <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.5 21 3 13.5 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.3 1L6.6 10.8Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
    <span>Call</span>
  </a>
  <a href="{wa}" data-track="whatsapp_click" class="mab-item" target="_blank" rel="noopener">
    <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M4 20l1.3-3.8A7.9 7.9 0 1 1 8.7 19L4 20Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 10.5c0 3 2.5 5.5 5.5 5.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    <span>WhatsApp</span>
  </a>
  <a href="/contact/" class="mab-item">
    <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M4 5h16v13H4z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="m4 6 8 6 8-6" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
    <span>Contact</span>
  </a>
  <a href="{esc(BIZ['maps_url'])}" data-track="direction_click" class="mab-item" target="_blank" rel="noopener">
    <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.6 7-11.5A7 7 0 0 0 5 9.5C5 14.4 12 21 12 21Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="9.5" r="2.3" stroke="currentColor" stroke-width="1.6"/></svg>
    <span>Directions</span>
  </a>
</div>"""


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

def footer() -> str:
    columns_html = []
    for col in FOOTER_COLUMNS:
        items = "\n        ".join(
            f'<li><a href="{esc(l["href"])}">{esc(l["label"])}</a></li>' for l in col["links"]
        )
        columns_html.append(f"""<div class="footer-col">
      <h2>{esc(col['heading'])}</h2>
      <ul>
        {items}
      </ul>
    </div>""")
    columns_joined = "\n    ".join(columns_html)

    social_html = "\n        ".join(
        f'<a href="{esc(s["url"])}" target="_blank" rel="noopener" aria-label="{esc(s["label"])}">{esc(s["label"])}</a>'
        for s in SOCIAL_LINKS
    )

    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    {columns_joined}
    <div class="footer-col footer-contact">
      <h2>Visit or contact us</h2>
      <address>
        {esc(BIZ['name'])}<br>
        {esc(BIZ['address']['street'])}<br>
        {esc(BIZ['address']['city'])}, {esc(BIZ['address']['region'])} {esc(BIZ['address']['postal_code'])}
      </address>
      <p><a href="{BIZ['tel_href']}">{esc(BIZ['phone_display_full'])}</a></p>
      <p><a href="{BIZ['mailto_href']}">{esc(BIZ['email'])}</a></p>
      <p><a href="{esc(BIZ['maps_url'])}" target="_blank" rel="noopener">Get directions</a></p>
      <div class="footer-social">
        {social_html}
      </div>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; {CURRENT_YEAR} {esc(BIZ['name'])}. All rights reserved.</p>
    <p class="footer-disclosure">{esc(DISCLOSURE_SHORT)}</p>
  </div>
</footer>"""


# ---------------------------------------------------------------------------
# Breadcrumbs (visible HTML; JSON-LD BreadcrumbList built separately)
# ---------------------------------------------------------------------------

def breadcrumbs(items) -> str:
    """items: list of (label, path) tuples, root first, current page last."""
    parts = []
    for i, (label, path) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<li aria-current="page">{esc(label)}</li>')
        else:
            parts.append(f'<li><a href="{esc(path)}">{esc(label)}</a></li>')
    joined = "\n      ".join(parts)
    return f"""<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ol class="container">
      {joined}
  </ol>
</nav>"""


# ---------------------------------------------------------------------------
# FAQ accordion -- native <details>/<summary>, zero JS required
# ---------------------------------------------------------------------------

def faq_accordion(qa_pairs, heading="Frequently asked questions", id_prefix="faq") -> str:
    items = []
    for i, (q, a) in enumerate(qa_pairs):
        items.append(f"""<details class="faq-item" id="{id_prefix}-{i+1}">
      <summary>{esc(q)}</summary>
      <div class="faq-answer"><p>{a}</p></div>
    </details>""")
    joined = "\n    ".join(items)
    return f"""<section class="faq-block" aria-labelledby="{id_prefix}-heading">
  <h2 id="{id_prefix}-heading">{esc(heading)}</h2>
  <div class="faq-list">
    {joined}
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Reusable content blocks
# ---------------------------------------------------------------------------

def cta_block(*, heading, body, whatsapp_key="default", variant="section") -> str:
    wa = whatsapp_href(WHATSAPP_MESSAGES.get(whatsapp_key, WHATSAPP_MESSAGES["default"]))
    cls = "cta-block" if variant == "section" else f"cta-block cta-block--{variant}"
    return f"""<section class="{cls}">
  <div class="container cta-inner">
    <div>
      <h2>{esc(heading)}</h2>
      <p>{body}</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-primary btn-lg" href="{BIZ['tel_href']}" data-track="phone_click">Call {esc(BIZ['phone_display'])}</a>
      <a class="btn btn-secondary btn-lg" href="{wa}" data-track="whatsapp_click" target="_blank" rel="noopener">Message on WhatsApp</a>
      <a class="btn btn-ghost btn-lg" href="/contact/">Send a message</a>
    </div>
  </div>
</section>"""


def service_card(*, href, title, summary, icon_svg) -> str:
    return f"""<a class="service-card" href="{esc(href)}">
  <span class="service-card-icon" aria-hidden="true">{icon_svg}</span>
  <h3>{esc(title)}</h3>
  <p>{esc(summary)}</p>
  <span class="service-card-link">Learn more &rarr;</span>
</a>"""


def image_frame(icon_key: str, *, aspect="4 / 3", alt="") -> str:
    """Polished CSS-based image placeholder: brand-gradient frame with a
    large original line-icon glyph centered in it. Used until real device/
    workbench photography (see IMAGE-ASSET-MANIFEST.md) is supplied --
    swapping in a real photo later requires no layout change, since the
    frame's aspect-ratio and sizing stay the same either way."""
    from src.assets.icon_glyphs import glyph
    alt_span = f'<span class="sr-only">{esc(alt)}</span>' if alt else ""
    return (
        f'<div class="img-frame" style="--ar: {aspect};">'
        f'<span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,0.9);">'
        f'{glyph(icon_key, size=96)}</span>{alt_span}</div>'
    )


def hero(*, eyebrow=None, h1, sub, trust_items=None, whatsapp_key="default",
          icon_key=None, primary_label=None) -> str:
    wa = whatsapp_href(WHATSAPP_MESSAGES.get(whatsapp_key, WHATSAPP_MESSAGES["default"]))
    eyebrow_html = f'<span class="hero-eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    trust_html = ""
    if trust_items:
        items = "\n        ".join(
            f'<li><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="m5 13 4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>{esc(t)}</li>'
            for t in trust_items
        )
        trust_html = f'<ul class="hero-trust">\n        {items}\n      </ul>'
    call_label = esc(primary_label or f"Call {BIZ['phone_display']}")
    media_html = ""
    inner_class = "hero-inner"
    if icon_key:
        media_html = f'<div class="hero-media">{image_frame(icon_key, alt="")}</div>'
        inner_class += " with-media"
    return f"""<section class="hero">
  <div class="container {inner_class}">
    <div>
      {eyebrow_html}
      <h1>{esc(h1)}</h1>
      <p class="hero-sub">{sub}</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="{BIZ['tel_href']}" data-track="phone_click">{call_label}</a>
        <a class="btn btn-secondary btn-lg" href="{wa}" data-track="whatsapp_click" target="_blank" rel="noopener">Message on WhatsApp</a>
      </div>
      {trust_html}
    </div>
    {media_html}
  </div>
</section>"""


def stat_strip(stats) -> str:
    """stats: list of (value, label) tuples. Dark signature-surface band with
    large mono numerals -- used only for facts that are honestly countable
    from real site/business data (device categories, service areas, etc.),
    never a placeholder for an invented business metric."""
    items = "\n    ".join(
        f'<div class="stat-item"><span class="stat-value">{esc(v)}</span><span class="stat-label">{esc(l)}</span></div>'
        for v, l in stats
    )
    return f"""<section class="stat-strip">
  <div class="container stat-strip-inner">
    {items}
  </div>
</section>"""


def disclosure_note(long_form: str) -> str:
    return f'<p class="disclosure-note">{long_form}</p>'


# ---------------------------------------------------------------------------
# Full page assembly
# ---------------------------------------------------------------------------

def page(*, title, description, path, main_html, current_path=None,
          og_image=None, noindex=False, schema_objects=None,
          body_class="", whatsapp_key="default", include_action_bar=True):
    schema_html = to_script_tag(*(schema_objects or []))
    head_html = head(
        title=title, description=description, path=path,
        og_image=og_image, noindex=noindex, extra_schema_html=schema_html,
    )
    nav_html = header_nav(current_path or path)
    footer_html = footer()
    action_bar = mobile_action_bar(whatsapp_key) if include_action_bar else ""
    body_cls = f" class=\"{esc(body_class)}\"" if body_class else ""

    return f"""<!doctype html>
<html lang="en-CA">
<head>
{head_html}
</head>
<body{body_cls}>
{skip_link()}
{nav_html}
<main id="main-content">
{main_html}
</main>
{footer_html}
{action_bar}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""
