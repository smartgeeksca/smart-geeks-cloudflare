# Changelog

## v1.6.0 -- Light/Dark Theme System, cloned from smartgeeks.ca's design language (2026-09-02)

**Scope:** CSS and JS/template only (`style.css`, `layout.py`, `main.js`,
`tests/qa.py`) -- no content module touched, no business fact changed or
added. This pass followed an explicit reversal of direction: instead of a
new visual concept (V2/V3/V4's Tailcast/Linear/Stripe-inspired explorations),
the brief asked for the Cloudflare project to match the real production
site's (https://smartgeeks.ca/) actual design system -- structure, rhythm,
components -- while keeping 100% of the Cloudflare project's own verified
content, SEO, schema, and compliance work untouched. See
12-SMARTGEEKS-CA-DESIGN-DNA-REPORT.md and
13-COMPONENT-MAPPING-AND-DIFFERENCE-REPORT.md for the full reverse-engineering
and an honest list of what was and wasn't built.

### Added
- A complete light/dark theme system -- the one component the real site has
  that the Cloudflare project genuinely lacked entirely. Light remains the
  default (matches the Cloudflare project's existing look exactly, zero
  visual change for anyone who never touches the toggle). Dark is available
  via a header toggle (desktop and mobile, sun/moon icon matching the real
  site's convention), auto-applies when the OS/browser prefers dark and the
  visitor hasn't chosen explicitly (`@media (prefers-color-scheme: dark)`),
  and an explicit choice always wins over the OS preference in either
  direction. Persisted via `localStorage` (`sg-theme` key); a tiny inline
  anti-flash script in `<head>` applies a *stored* choice before first paint
  so there's no flash of the wrong theme -- the no-preference-at-all case is
  handled entirely by CSS, no JS involved.
- New semantic CSS tokens (`--heading`, `--link`, `--chip-bg`/`--chip-fg`,
  `--header-bg`) split off the existing brand tokens (`--navy`,
  `--blue-button`) specifically so the theme can flip text/link colors
  without touching the brand's fixed dark-surface and filled-button colors,
  which stay identical in both themes by design (hero, footer, CTA band,
  and primary/secondary buttons look the same whichever theme is active).
- A full dark-theme token layer: 4 surface tiers, text/muted-text, 3 border
  tiers, chip colors, header background, focus ring, and form-status
  colors -- 20 new color pairs, every one independently contrast-verified
  in `tests/qa.py` before being written into CSS (worst case 5.27:1,
  comfortably over the 4.5:1 AA floor for text).

### Changed
- `src/assets/css/style.css`: 34,220 -> 38,138 bytes.
- `src/templates/layout.py`: 18,527 -> 20,798 bytes (`THEME_INIT_SCRIPT`
  constant, theme-toggle buttons in `header_nav()`).
- `src/assets/js/main.js`: 10,392 bytes (new `themeToggle()` IIFE).
- `tests/qa.py`: 38 -> 53 checks (15 new dark-theme contrast pairs; zero
  existing checks changed).

### Not changed
- No content module (`business.py`, `services.py`, `pages.py`, `legal.py`,
  `landing.py`) was touched -- every string on every page is byte-identical
  to the V4 baseline. 23 pages, 21 sitemap URLs, all structured data,
  canonical tags, and internal links unchanged and re-verified.
- No business fact from the real smartgeeks.ca site (its review rating,
  weekly repair count, "since [year]" founding claim, or e-waste
  credential) was copied into the Cloudflare project -- `business.py`'s
  `OWNER_PENDING` still keeps those fields `None` pending the real owner's
  confirmation. Only the real site's *design pattern* (a trust-bar
  component exists, in that position, in that visual form) was cloned,
  populated with the Cloudflare project's own already-verified facts.
- Section-by-section homepage/service-page rearchitecture (V4's job) was
  not repeated or undone -- this pass is additive on top of V4's layout,
  not a replacement for it.

## v1.5.0 -- Layout System V4: homepage & services-index rearchitecture (2026-09-01)

**Scope:** CSS, JS templates (layout.py), and page composition (build.py) --
still no business content, price, hours, warranty, or structured-data
change; every string rendered by the new sections is either pulled
verbatim from src/content/pages.py / services.py / business.py, or is a
short structural/wayfinding label (a "section-label" eyebrow), never a
new marketing claim. This pass responds to explicit feedback that V2/V3
polished the existing template's surface without changing its underlying
section skeleton -- V4 changes the skeleton itself on the two
highest-traffic pages (homepage, services index).

### Added
- `.split-editorial` -- reusable asymmetric two-column grid (7fr/5fr,
  `.reverse` variant swaps which side is wide) used by every new module
  below, so consecutive sections alternate visual emphasis left-to-right
  down the page instead of stacking identical blocks.
- `.statement-band` / `statement_band()` -- a single oversized typographic
  moment; the homepage's brand-story paragraph is split at its first
  sentence boundary (via `str.index()` in build.py, not a content edit)
  so the opening sentence becomes this moment and the rest becomes the
  new repair-intelligence section's intro.
- Repair-intelligence section -- merges the old separate "why an
  independent shop" card grid and "how a repair works" numbered list into
  one `.split-editorial` section (philosophy left, process right).
- Device-ecosystem taxonomy (`device_ecosystem_html()`, shared by the
  homepage and `/services/`) -- the 8 device-repair categories grouped
  into 3 labeled clusters (PC & Windows / Apple hardware / Peripherals &
  consoles) instead of one flat 9-card grid; chip-level repair renders as
  its own cross-cutting `.capability-band` since it applies across every
  cluster rather than belonging to one.
- Buy/Sell/Trade flagship section on the homepage -- promoted from "1 card
  among 9" to its own `.flagship-split` chapter, reusing BUY_SELL_TRADE's
  existing copy verbatim (answer, what_we_accept, sustainability_note).
- Local-authority "readout" section -- same real address/phone/email/
  service-area facts, presented as a monospaced `<dl>` status-panel card
  instead of a generic two-column text+image block.
- `--space-8` (8rem) / `--space-9` (11rem) large "editorial moment"
  spacing tokens.
- Hero upgraded to a true full-viewport moment site-wide
  (`min-height: min(86vh, 780px)` on desktop) -- applies to every page
  that calls the shared `hero()` component, not just the homepage.

### Changed
- `src/assets/css/style.css`: 27,519 -> 34,220 bytes.
- `src/templates/layout.py`: 17,962 -> 18,527 bytes (+ `statement_band()`).
- `build.py`: 35,184 -> 39,769 bytes (`build_home()` fully rewritten;
  `build_services_overview()` rewired onto the shared device-ecosystem
  taxonomy, now also surfacing buy-sell-trade as a second capability-style
  band since that page has no separate flagship section for it).

### Not changed
- No `.py` content module -- 23 pages, 21 sitemap URLs, all structured
  data byte-identical in content; internal-link-resolution check
  independently confirms 0 broken links (buy-sell-trade's move out of the
  flat services grid did not orphan that page on either the homepage or
  the services index).
- No color hex value, and no new on-dark color combination was
  introduced -- every new component reuses V3's already-verified tokens,
  so the contrast-check count is unchanged at 38 pass / 1 expected warn /
  0 fail.
- Individual service pages, About, Contact, FAQ, Reviews, policy pages,
  404, and Thank-you were NOT rearchitected in this pass -- see
  09-V4-ARCHITECTURE-AND-WIREFRAMES.md for honest, page-by-page
  [RECOMMENDATION]-labeled proposals for each, not yet implemented.

## v1.4.0 -- Design System V3: premium technology-brand visual pass (2026-09-01)

**Scope:** CSS, JS, and template/layout markup (layout.py, build.py) --
still no business content, price, hours, warranty, or structured-data
change. This pass moves beyond V2's component polish toward brand
perception: a shared dark "signature surface" (hero / stat strip / CTA /
footer), a real display+mono typographic system, an asymmetric bento
layout, and a blueprint-style process diagram. Direction: Linear / Vercel
/ Stripe / Supabase / Raycast / Notion / Apple-style premium technology
marketing sites, translated into Smart Geeks' own brand colors and real
content -- no Tailcast, no third-party copy/branding/imagery.

### Added
- Google Fonts request (Inter / Space Grotesk / JetBrains Mono,
  preconnected, swap-displayed, only the weights used) -- a deliberate,
  documented reversal of the earlier zero-external-font stance, made
  because self-hosting requires a font-binary fetch this build
  environment has no network path for, and system-ui alone can't
  credibly deliver Linear/Stripe-grade typography. Full system-font
  fallback stack retained.
- `--mesh-bg` shared background recipe (radial-gradient glows + grid
  lines) applied identically to `.hero`, `.stat-strip` (new), `.cta-block`,
  and `.site-footer`, so all four dark sections read as one signature
  brand surface.
- New `.stat-strip` component with three honest, non-fabricated counts
  (8 device categories, 4 cities served, 100% independently owned) --
  every value traceable to `src/data/business.py` / `SERVICE_AREAS`.
- New `.bento-grid` asymmetric layout, additive on top of `.card-grid`,
  applied only to the homepage "why an independent shop" section.
- Blueprint-style process section: dashed connecting trace line + mono
  step numbers.
- New on-dark color tokens (`--ink-2`, `--text-on-dark`,
  `--text-on-dark-muted`, `--blue-on-dark`), each independently
  contrast-verified and added as 5 new permanent checks in
  `tests/qa.py` (33 -> 38 total contrast checks, all pass).
- `.section-label` mono/uppercase technical-label utility.

### Changed
- `src/assets/css/style.css`: 23,068 -> 27,519 bytes (14 targeted edits).
- `src/templates/layout.py`: 17,018 -> 17,950 bytes (Google Fonts link +
  new `stat_strip()` component).
- `build.py`: 34,894 -> 35,184 bytes (wire `stat_strip()` into the
  homepage with honest counts; mark the "why" grid as `.bento-grid`).
- `tests/qa.py`: 5 new permanent contrast checks added.
- Hero headline scale: `--fs-3xl` (2.75rem) -> new `--fs-5xl` (4.25rem)
  on desktop.
- All headings switch from the body font to `--font-display`
  (Space Grotesk), weight 800 -> 700, tracking -0.02em -> -0.03em.

### Not changed
- No business fact, price, warranty period, hours, or review data --
  every stat-strip value is a real, checkable count, not a business
  metric (this project's `business.py` keeps years-in-business,
  review-count, etc. explicitly `None` until the owner supplies them,
  by design -- V3 does not work around that).
- No `.py` content module (`services.py`, `pages.py`, `legal.py`,
  `landing.py`) -- 23 pages, 21 sitemap URLs, all structured data
  byte-identical in content.
- No color hex value -- every existing WCAG AA ratio unchanged; 5 new
  ratios added, all independently verified >=7.3:1.

## v1.3.0 -- Design System V2: Tailcast-inspired visual upgrade (2026-09-01)

**Scope:** CSS and JS only -- no content, business data, structured data,
or page count changed. Inspired by the layout/spacing/shadow/motion
conventions of the open-source Tailcast template (github.com/matt765/
Tailcast, MIT) as a design-language reference only; no Tailcast code,
copy, branding, or assets were copied. All color values remain the
brief's original brand tokens (#007BFF / #0A1A2F / #00E676 / #F5F7FA /
#333333) -- every WCAG AA contrast figure in QA-REPORT.md is unchanged
and was independently re-verified after this pass (33 pass / 1 expected
warn / 0 fail, identical to the pre-redesign result).

### Added
- Layered surface/shadow/radius/motion token system in `:root`
  (`--surface-raised`, `--border-subtle`/`--border-strong`, `--shadow-xs`
  through `--shadow-lg`, `--shadow-glow`, `--radius-lg`/`--radius-xl`/
  `--radius-full`, `--ease`/`--dur-*`), layered on top of the existing
  8px spacing scale and type scale without changing either.
- Abstract, CSS-only circuit-board-pattern treatment for `.img-frame`
  (the existing placeholder-until-real-photography component) and for
  the dark CTA-block/footer surfaces -- no stock photography, no
  fabricated product images; real photography remains a documented
  owner action (see IMAGE-ASSET-MANIFEST.md).
- Scroll-reveal and header-shadow-on-scroll, implemented as optional
  progressive enhancement in `main.js`: skipped entirely when
  `prefers-reduced-motion` is set or `IntersectionObserver` is
  unavailable, and every targeted element (cards, FAQ rows, trust
  badges, section headers) is fully visible with no JavaScript at all.
- Pill-shaped trust badges in the hero trust row, lift/glow interaction
  states on primary buttons and cards, a rotating FAQ indicator, iOS
  safe-area padding on the mobile action bar, and a focus-visible glow
  ring on form fields (in addition to the existing border-color change).

### Changed
- `src/assets/css/style.css`: 18,396 -> 22,921 bytes (14 targeted,
  reviewed edits -- see `LAUNCH-ACTIVATION-PLAN.md`-style verification
  in the design audit for the full list).
- `src/assets/js/main.js`: 5,708 -> 8,362 bytes (two additive,
  self-contained functions appended; no existing form/analytics logic
  touched).

### Not changed
- No `.py` content module touched (`services.py`, `pages.py`,
  `legal.py`, `landing.py`, `business.py`) -- every one of the 23
  generated pages, 21 sitemap URLs, and all structured data are
  byte-identical in content to the pre-redesign build; only the
  presentation layer changed.
- No color hex value changed -- every button/text/background combination
  keeps its previously-verified WCAG AA contrast ratio exactly.

## v1.2.0 -- Google Ads policy recovery: retire repair Ads landing pages (2026-09-01)

**Root cause corrected.** Every earlier reference in this codebase and its
docs to "Google Ads hardware-repair-services certification" was based on an
incomplete reading of Google's Third-Party Consumer Technical Support
policy. The current published policy text is a flat **prohibition** on
advertising third-party consumer hardware repair services -- there is no
certification path, and no landing-page quality changes that. Full
research and per-campaign verdicts: `CURRENT-POLICY-SOURCE-REGISTER.md`
and `CAMPAIGN-ELIGIBILITY-MATRIX.md` (delivered alongside this codebase).

### Changed
- `src/content/landing.py`: header rewritten to correct the false
  "certification" framing; module retained for possible future organic-use
  value but no longer wired into the build.
- `build.py`: the landing-page generation loop is commented out. The four
  repair "Ads" landing pages are no longer generated and no longer appear
  in `sitemap.xml`.
- `_redirects`: added four 301 rules sending the old landing-page paths to
  their closest real, organic service page.
- `README.md`, `QA-REPORT.md`, `LICENSE-NOTICE.md`: corrected every
  reference to repair-ads "certification."

### Not changed
- The real service pages, blog posts, and location pages are untouched.
- No business fact, price, warranty term, or claim was added or removed
  from `src/data/business.py`.

## v1.1.1 -- Fix apex-to-www redirect after first real production deploy (2026-09-01)

The first real Cloudflare Pages deploy of this project (Git-connected, per
DEPLOYMENT.md Option A) surfaced one real bug: Cloudflare's build log
reported `_redirects` line 10 as invalid --

```
Found invalid redirect lines:
  - #10: https://smartgeeks.ca/*  https://www.smartgeeks.ca/:splat  301!
    Only relative URLs are allowed. Skipping absolute URL https://smartgeeks.ca/*.
```

Cloudflare Pages' `_redirects` file only accepts a relative path as a
rule's *source* -- it cannot match on which hostname a request arrived on,
so a host-conditional redirect like this one is always parsed as invalid
and dropped, whether or not `smartgeeks.ca` is also attached as a second
custom domain on the project (the condition DEPLOYMENT.md v1.1.0
incorrectly said made it take effect). It never worked; the deploy itself
was unaffected (everything else in the file parsed and applied normally).

### Fixed

- `_redirects`: removed the invalid apex-to-www rule and replaced it with
  an explanatory comment, so the file no longer contains a rule that looks
  like it does something but doesn't.
- `DEPLOYMENT.md` "Custom domain setup": now documents the zone-level
  **Redirect Rule** (Rules -> Redirect Rules on the `smartgeeks.ca` zone)
  as the one correct mechanism for apex -> www canonicalization, instead
  of presenting it as one of two equally-valid options.

## v1.1.0 -- No-Wrangler deployment path (2026-08-31)

Added `alt-deploy/_worker.js`: a self-contained "Advanced Mode" Worker
bundle that reimplements `functions/api/contact.js` and
`functions/_middleware.js` as one file, for people who want to deploy via
the Cloudflare dashboard's drag-and-drop upload without installing Wrangler
or connecting a Git repository. Verified against Cloudflare's own
documentation (fetched live) that plain drag-and-drop does not compile a
`functions/` directory at all, but does support a root-level `_worker.js`
("Advanced Mode") -- this bundle exists specifically to close that gap.
Also added `scripts/check_worker_sync.py`, which checks the bundle's key
literals (field limits, required fields, the email API endpoint, the
production hostname list) against the original two source files and
exits non-zero on drift; ran clean against this release (`All checked
literals match`). DEPLOYMENT.md now documents three deploy paths side by
side, none requiring Wrangler: Git-connected (recommended -- no
duplication), plain drag-and-drop (static only, contact form won't work),
and drag-and-drop + this bundle (full functionality, hand-maintained).

## v1.0.0 -- Initial build (2026-08-31)

Full production-ready static site package, built fresh in this session as
`smart-geeks-cloudflare/` per the "senior web design and engineering team"
brief. This is a distinct, from-scratch project -- it does not reuse code
or copy from any earlier build produced in this workspace; content and
markup were authored fresh against this brief's specific requirements
(original per-service content structure, 27 required pages, Cloudflare
Pages Functions, JSON-LD without fabricated claims, image-asset manifest,
automated QA).

### Added

- 27 required pages (see CONTENT-INVENTORY.md for the full list): home,
  services overview, 9 device/repair + buy-sell-trade pages, service areas,
  about, FAQs, contact, reviews, 4 legal/policy pages, accessibility
  statement, thank-you (noindex), 404 (noindex), 4 Google Ads landing pages.
- Centralized business data (`src/data/business.py`) and JSON-LD builders
  (`src/data/schema.py`) as the single source of truth for facts across
  templates, visible content, and structured data.
- Original design system (`src/assets/css/style.css`): brand palette with a
  WCAG-AA-safe filled-button blue (`#0062CC`, 5.80:1 on white) distinct from
  the brief's raw `#007BFF` accent (3.98:1, correctly never used for
  button/fill text), mobile-first layout, native `<details>`/`<summary>`
  mobile nav and FAQ accordions (zero-JS-required by construction).
- Cloudflare Pages Functions: `functions/api/contact.js` (validated,
  sanitized, honeypot-protected, best-effort rate-limited contact form,
  emailing via Cloudflare's own Email Service REST API) and
  `functions/_middleware.js` (per-hostname `X-Robots-Tag: noindex` for any
  non-production host).
- Original hand-authored SVG brand mark, favicon set, OG share image, and an
  11-icon original line-icon set (`src/assets/icon_glyphs.py`) -- no
  third-party icon library, no stock photography.
- `IMAGE-ASSET-MANIFEST.md` documenting every real photograph still needed,
  with exact filenames, dimensions, placement, alt text, and shoot/generation
  prompts, since no photography or image-generation tool was available this
  session.
- `tests/qa.py`: an automated QA suite that actually parses and checks the
  generated output (titles, meta descriptions, canonicals, H1s, internal
  links, alt attributes, JSON-LD validity, WCAG contrast via a from-scratch
  luminance calculation, placeholder-text scanning, sitemap/robots
  sanity) -- see QA-REPORT.md for the actual results of running it.
- Full documentation set: README.md, DEPLOYMENT.md, CONTENT-INVENTORY.md,
  IMAGE-ASSET-MANIFEST.md, QA-REPORT.md, LICENSE-NOTICE.md.

### Decisions and their reasoning

- **Cloudflare Pages, not Workers Static Assets** -- chosen and implemented
  consistently (see DEPLOYMENT.md "Why Pages, not Workers"); this also
  happens to be the correct fix for a `.workers.dev`-hostname mismatch found
  in an earlier, unrelated production audit of this business's prior
  deployment.
- **Cloudflare Email Service REST API for the contact form**, not
  MailChannels (not a dependable, currently-guaranteed method for new
  projects) and not Cloudflare's native `send_email` Worker binding (not
  listed as a supported Pages Functions binding type as of this build --
  verified against Cloudflare's own bindings documentation). Confirmed
  against Cloudflare's documentation, fetched live during this build.
- **No fixed price list, warranty duration, or diagnostic fee published.**
  The brief explicitly forbids inventing these; rather than leave a
  placeholder, every relevant page states honestly that these are
  communicated directly, and README.md lists them as owner action items.
- **Location pages omitted.** The brief makes these optional ("may be
  included only when they contain genuinely useful, unique content") and
  they're not in the 27 required pages -- see CONTENT-INVENTORY.md
  "Deliberately not included."
- **CSS-based image placeholders instead of any generated or stock
  photography**, per the brief's explicit fallback instructions when no
  image-generation tool is available -- see IMAGE-ASSET-MANIFEST.md.

### Not included (see README.md "Owner action items" for the full list)

Real opening hours, genuine reviews, warranty duration, diagnostic fee, real
photography, real prices, GA4/Google Ads IDs, transactional email
credentials, Google Ads hardware-repair-services certification, and final
legal review of the policy pages all require input only the business owner
can provide, and are each handled with an honest, non-fabricated default in
the meantime.
