# Changelog

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
