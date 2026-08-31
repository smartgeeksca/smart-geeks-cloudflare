# Changelog

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
