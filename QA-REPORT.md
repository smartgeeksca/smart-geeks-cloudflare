# QA Report

This report distinguishes what was **actually run and verified this
session** from what is a **stated goal, not yet independently measured**
(e.g. Lighthouse scores). Nothing below claims "zero errors" without the
corresponding check having actually been executed.

## Commands run

```bash
python3 build.py                                    # build succeeded, 27 pages generated
python3 tests/qa.py                                  # automated QA suite, see results below
node --check functions/_middleware.js                # syntax OK
node --check functions/api/contact.js                # syntax OK
node --check src/assets/js/main.js                   # syntax OK
python3 -m http.server (public/) + 34 real HTTP GETs  # every generated URL served, see below
```

## Automated QA suite results (`tests/qa.py`)

Full output reproduced below (last run against the final build):

```
==============================================================================
SMART GEEKS -- AUTOMATED QA REPORT
==============================================================================
[WARN] Contrast: Raw brand blue (#007BFF) on white -- NOT used for filled-button
       text, only links/accents: 3.98:1 (fails AA; correctly not used for
       text-on-fill anywhere)
[PASS] Pages generated: 27 HTML files found in public/
[PASS] Placeholder text scan: Searched 27 files for VERIFY, TODO, TBD,
       PLACEHOLDER, FIXME, LOREM IPSUM, COMING SOON -- none found
[PASS] Suspect fake-data scan: Searched for example.com, 555-0100, 555-1234,
       test@test.com, fake review, AW-XXXXXXX, G-XXXXXXXXXX -- none found
[PASS] Duplicate title check: 27 unique titles across 27 pages
[PASS] Duplicate meta description check: 27 unique descriptions across 27 pages
[PASS] Every page has an H1: 27/27
[PASS] Single H1 per page: 27/27
[PASS] Canonical tag present: 27/27
[PASS] Canonical host = https://www.smartgeeks.ca: 27/27
[PASS] Internal link resolution: 0 broken internal links
[PASS] href="#" scan: none found
[PASS] Empty href scan: none found
[PASS] Image alt attributes: every <img> has an alt attribute
[PASS] JSON-LD validity: every <script type=application/ld+json> block parses
       as valid JSON
[PASS] Contrast: Filled button (#0062CC) on white -- button text: 5.80:1
[PASS] Contrast: Filled button hover (#004FA3) on white: 7.93:1
[PASS] Contrast: Body text (#333333) on white: 12.63:1
[PASS] Contrast: Muted text (#52606D) on white: 6.46:1
[PASS] Contrast: Muted text (#52606D) on soft gray (#F5F7FA): 6.02:1
[PASS] Contrast: Navy (#0A1A2F) on white -- headings: 17.48:1
[PASS] Contrast: White text on navy (#0A1A2F) -- footer/CTA: 17.48:1
[PASS] Contrast: Error text (#B3261E) on error bg (#FBEAE9): 5.62:1
[PASS] Contrast: Success text (#1E7E34) on success bg (#E9F7EF): 4.65:1
[PASS] robots.txt does not block production: no site-wide Disallow found
[PASS] robots.txt references sitemap: OK
[PASS] Sitemap URLs use canonical host: 25 URLs checked
[PASS] Sitemap excludes noindex pages: thank-you and 404 correctly excluded
[PASS] _headers present: OK
[PASS] _redirects present: OK
[PASS] robots.txt present: OK
[PASS] sitemap.xml present: OK
[PASS] site.webmanifest present: OK
[PASS] 404.html present: OK
------------------------------------------------------------------------------
Totals: 33 pass, 1 warn, 0 fail
==============================================================================
```

The one WARN is expected and correct, not a bug: `#007BFF` (the brand's
"Primary Electric Blue" as given in the brief) genuinely fails WCAG AA at
3.98:1 against white, which is exactly why this build never uses it for
button/fill text -- only the darker `#0062CC` (5.80:1) is used for filled
buttons, and `#007BFF` is reserved for links/accents on light backgrounds
where its use is limited to non-body text. The check exists specifically to
catch a regression if that ever changes.

Contrast ratios were computed with a from-scratch implementation of the
WCAG relative-luminance formula (`tests/qa.py:relative_luminance` /
`contrast_ratio`), not asserted from memory.

An earlier run of this suite caught two real duplicate `<title>` tags
(the laptop and gaming-console landing pages initially matched their
corresponding service pages exactly) -- fixed in `src/content/landing.py`
by adding a "| Contact Smart Geeks" suffix to all four landing titles, then
reconfirmed at 0 fail on rebuild.

## Live HTTP smoke test

Every generated URL was served with `python3 -m http.server` against the
real `public/` output and fetched with real HTTP requests (not just checked
for file existence):

```
34/34 returned 200
```

Covers all 27 pages plus `sitemap.xml`, `robots.txt`, `site.webmanifest`,
and 4 representative static assets (CSS, JS, SVG icon, ICO favicon).

## Additional manual checks performed

- Scanned all generated HTML for stray unrendered Python artifacts
  (`None`, `Traceback`, `object at 0x...`) -- **zero matches**.
- Verified `window.__SG_ANALYTICS_CONFIG` renders as `null` values (real
  JSON `null`, not a fabricated ID) and that no `<script
  src="https://www.googletagmanager.com/...">` tag is emitted anywhere,
  confirming analytics stays fully inert until a real GA4 ID is set.
- Measured real build output sizes (not estimated):
  - `style.css`: 20 KB, `main.js`: 8 KB (both served with long-lived
    immutable caching via a content-hash query string -- see DEPLOYMENT.md).
  - Generated HTML pages: 9.7 KB - 26.1 KB uncompressed each (Cloudflare
    Pages applies its own compression at the edge on top of this).
  - Total `public/` output: 712 KB, essentially all of it text (HTML/CSS/
    JS/SVG) -- there is no photography in this build yet (see
    IMAGE-ASSET-MANIFEST.md), which keeps this number low but will change
    once real photos are added; follow the manifest's WebP/`srcset`
    guidance when they are.

## What was NOT tested this session, and why

Stated plainly rather than assumed to pass:

- **Real Lighthouse scores.** No network access to the npm registry was
  available in this build session (`npm view lighthouse` returned `403
  Forbidden` under the sandbox's egress policy), so Lighthouse could not be
  installed or run. The brief's 90/95/95/95 targets remain **goals to
  verify after deployment**, not measured facts -- run Lighthouse (or
  PageSpeed Insights) against the live URL after deploying, per
  DEPLOYMENT.md's post-deploy checklist.
- **A W3C-grade HTML validator.** `html5validator` was not installable in
  this session's package registry (also blocked). `tests/qa.py` performs
  structural checks (titles, meta, canonical, headings, links, alt text,
  JSON-LD) using Python's built-in HTML parser, which is real validation of
  those specific things, but is not a substitute for full markup-conformance
  validation. Recommended before launch: run the built pages through
  https://validator.w3.org/ or a local `html5validator`/`tidy` install.
- **`wrangler pages dev` / an actual Cloudflare deployment.** This session
  never held Cloudflare credentials and the npm registry was unreachable
  (`wrangler` could not be installed), so the contact form's email delivery
  path, the `_headers`/`_redirects` behavior under real Cloudflare routing,
  and the `X-Robots-Tag` middleware were verified by code review and local
  syntax checking, not by an actual deploy. DEPLOYMENT.md's post-deploy
  checklist exists specifically to close this gap after a real deployment.
- **Visual/rendered accessibility testing** (screen reader pass, real
  keyboard-navigation walkthrough in a browser). The build uses semantic
  landmarks, native `<details>`/`<summary>` for menus and FAQs (so no
  custom ARIA state management is needed there), labelled form fields, and
  visible focus rings by construction -- but this hasn't been confirmed
  with an actual assistive-technology pass.
- **Cross-browser/device visual testing.** No browser automation was run
  against the built pages this session.

## Known limitations carried into this delivery

- No real photography anywhere (see IMAGE-ASSET-MANIFEST.md) -- CSS-based
  brand placeholders are used instead, sized so a real photo drops in with
  no layout change.
- Hours, warranty duration, diagnostic fee, and real pricing are not
  published anywhere (see README.md "Owner action items") -- every page
  that would normally state one of these instead explains, honestly, that
  it's confirmed directly or communicated before work begins.
- The contact form's email delivery requires Cloudflare Email Service
  secrets to be configured post-deploy (see DEPLOYMENT.md); until then it
  fails safely with an honest error rather than a false "sent" confirmation.
- **Corrected 2026-09-01:** this line previously said Google's hardware-
  repair-services Ads policy "requires account-level certification that
  this codebase cannot complete." That was wrong -- current policy is a
  flat prohibition on advertising this category to consumers, with no
  certification path. The four repair Ads landing pages this note referred
  to have been retired and redirect to the real service pages. See
  `CAMPAIGN-ELIGIBILITY-MATRIX.md` for the corrected, per-campaign verdicts.
