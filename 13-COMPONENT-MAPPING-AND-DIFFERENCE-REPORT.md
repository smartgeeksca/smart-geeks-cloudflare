# Component Mapping & Difference Report

## Component mapping table

| smartgeeks.ca component | Cloudflare project equivalent | Status |
|---|---|---|
| Homepage hero (dark, eyebrow badge, 3-line headline, dual CTA, trust badges) | `layout.py: hero()` | Already equivalent — pre-dates this pass (V3/V4) |
| Trust bar (4 stats, hairline-divided) | `layout.py: stat_strip()` / `.stat-strip` | Already equivalent — pre-dates this pass (V3) |
| Service card grid (glass, dark) | `.service-card` / `device_ecosystem_html()` | Already equivalent — pre-dates this pass (V4); ours groups into 3 labeled clusters, theirs is one flat 5-card grid |
| "Why us" analogy section | `.intel-section` / `.statement-band` | Already equivalent — pre-dates this pass (V4) |
| Process / "How It Works" (3 steps) | `.step-list` inside `.intel-process` | Already equivalent — pre-dates this pass (V4) |
| Reviews section | Homepage does not currently surface reviews inline; `/reviews/` is a separate page | **Gap** — `[RECOMMENDATION]`, not built this pass |
| "Serving the Lower Mainland" / local-authority section | `.authority-section` | Already equivalent — pre-dates this pass (V4) |
| Special offers / discounts section | No equivalent section exists | **Gap** — `[RECOMMENDATION]`; also a content question (does Smart Geeks currently run student/senior discounts?), not just a design one |
| CTA band | `.cta-block` | Already equivalent — pre-dates this pass (V3/V4) |
| Footer (2-col + disclosure) | `layout.py: footer()` (4-col + disclosure) | Already equivalent in kind, different column count — content-driven, not a gap |
| Sticky mobile action bar | `layout.py: mobile_action_bar()` | Already equivalent — pre-dates this pass (V1) |
| Mobile header (icon-button pair beside hamburger) | `header_nav()` `.theme-toggle--mobile` + `.mobile-nav` | **Built this pass** (v1.6.0) |
| Light/dark theme toggle, persisted, `prefers-color-scheme`-aware | `.theme-toggle`, `THEME_INIT_SCRIPT`, `main.js: themeToggle()`, full dark-token layer in `style.css` | **Built this pass** (v1.6.0) — the one component that genuinely did not exist in the Cloudflare project before this pass |

## What this pass actually built — `[SOURCE-MODIFIED]` `[BUILD-VERIFIED]`

1. **A complete light/dark theme system**, applied to all 23 pages via the shared template functions:
   - New semantic CSS tokens (`--heading`, `--link`, `--chip-bg`/`--chip-fg`, `--header-bg`) split off the existing brand tokens (`--navy`, `--blue-button`) so a theme can flip *only* the roles that need to flip (text/link colors) while the brand's fixed dark-surface and filled-button colors stay exactly as they were, unchanged, in both themes.
   - A full dark-theme token layer (14 tokens: surfaces, text, borders, chip colors, header, focus ring, form-status colors), applied via both `@media (prefers-color-scheme: dark)` (auto, respects OS preference) and `:root[data-theme="dark"]` (explicit, wins over OS preference in either direction).
   - Every one of the 20 dark-theme color pairs is independently contrast-verified in `tests/qa.py` (see the QA section below) — none were eyeballed.
   - A toggle button (sun/moon icon, matching the real site's icon convention) in both the desktop header and the mobile header, wired to `localStorage` persistence under the key `sg-theme`.
   - A tiny inline anti-flash script in `<head>` (`THEME_INIT_SCRIPT` in `layout.py`) that applies a *stored, explicit* choice before first paint — visitors who've never touched the toggle get zero JS involvement; the OS-preference case is handled entirely by CSS.
2. **Real reverse-engineering of the live smartgeeks.ca site** (see `12-SMARTGEEKS-CA-DESIGN-DNA-REPORT.md`) using actual `getComputedStyle()` extraction, not visual guessing — confirming that the two sites already share the same design language at the token and component level (this was true before this pass; V3/V4 arrived at it independently), and identifying the theme toggle as the one component that was genuinely, completely missing.

## What was verified but NOT changed this pass — honest gaps

These are real, named differences between smartgeeks.ca and the Cloudflare project that this pass did **not** build, because building them well (verified, not guessed) would have meant either fabricating unverified business content or expanding scope well past what could be built and checked carefully in one pass:

- **Reviews are not surfaced on the Cloudflare homepage** the way they are on smartgeeks.ca (theirs has an inline homepage reviews section; ours only has the standalone `/reviews/` page). `[RECOMMENDATION]`.
- **No "special offers" section** exists in the Cloudflare project — and this is partly a content question for the business owner (are student/senior discounts currently offered?) before it's a design one. `[RECOMMENDATION]`.
- **No phone-repair service page** — the real site lists "Phone & Tablet" as a repaired category; `services.py` has no phone-repair entry. Flagged as a scope question in the DNA report, not silently resolved either way. `[RECOMMENDATION]`.
- **Active-nav-link style**: theirs is a pill/rounded highlight background; ours is an underline. Cosmetic, low-risk, not implemented this pass. `[RECOMMENDATION]`.
- **Mobile sticky-CTA accent color**: theirs uses a dedicated gold/amber accent distinct from brand blue for the single highest-intent mobile button; ours uses brand blue throughout. A real, cheap idea for a follow-up pass with its own contrast verification. `[RECOMMENDATION]`.
- **Section vertical rhythm**: theirs is a flat 96px top/bottom on every section; ours uses a scale (64px default, 128px for "editorial moment" sections). Not reconciled this pass since it would touch spacing on every page. `[RECOMMENDATION]`.

## `[BUILD-VERIFIED]` verification ledger

- `python3 -m py_compile` clean on every edited `.py` file (`layout.py`, `tests/qa.py`; `build.py` untouched this pass).
- Full rebuild: 23 HTML files / 21 sitemap entries, no errors.
- `python3 tests/qa.py` → **53 pass, 1 expected warn, 0 fail** (up from the V4 baseline's 38 pass — 15 new checks added, all for the new dark-theme tokens; zero existing checks changed or removed).
- All 20 new dark-theme color pairs independently computed via a standalone Python WCAG-contrast script *before* being written into CSS, then added as permanent, re-runnable entries in `tests/qa.py`, matching this project's established practice from the V3 pass. Every pair clears AA (4.5:1 for text; the two tightest results were 5.27:1 and 5.40:1, still comfortably over the 4.5:1 floor).
- Toggle mechanics verified live via Playwright against the actual rebuilt `public/` output, not asserted from reading the code: (1) fresh load with no stored preference renders light; (2) clicking the toggle switches to dark and updates `localStorage`; (3) reloading after a dark choice stays dark (anti-flash script confirmed working — no flash-of-light-theme on reload); (4) a browser with no stored preference and an OS/browser dark-mode setting renders dark automatically, with zero JS/clicks involved; (5) an explicit stored **light** choice correctly overrides an OS dark preference (tests the direction that's easy to get backwards).
- Screenshots: real Playwright/Chromium captures against the rebuilt `public/` output — light-theme hero, dark-theme hero (side by side, same content), dark-theme full homepage scroll, light-theme full homepage scroll, mobile header in both themes, and the OS-auto-dark case.
- One capture-only artifact found and diagnosed, not shipped as a live bug: the homepage's FAQ accordion items rendered with `opacity:0` in fast/large-jump programmatic scroll captures. Verified via `getComputedStyle` that (a) with `prefers-reduced-motion: reduce` the elements are `opacity:1` immediately (correct — JS never applies the `.reveal` class for those visitors), and (b) a slower, smaller-increment simulated scroll reveals them correctly (`opacity:1`) exactly like the sticky-header and process-section artifacts diagnosed in the V3 pass. This reproduces identically with the theme toggle untouched, confirming it predates this pass and is not a dark-theme regression.
- Preserved, verified rather than assumed: SEO (23 unique titles/descriptions, canonical tags on all 23 pages, unchanged), structured data (every JSON-LD block still parses as valid JSON), content (zero strings in any `.py` content module were touched this pass — this was a CSS/JS/template-only pass), forms (untouched), navigation (0 broken internal links), and compliance/disclosure copy (byte-identical, same source constants as before).
- `[LIVE-VERIFIED]`: nothing in this pass has been deployed. This session has never had, and does not have, push access to the GitHub repo (confirmed again this session) — the user pushed everything through the V4 pass (`629fc83`) already; this pass's commit(s) are ready for the same `git push origin main` step.
