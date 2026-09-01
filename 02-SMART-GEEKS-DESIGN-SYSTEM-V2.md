# Smart Geeks Design System V2

Formal specification of the design tokens and component recipes now implemented in `src/assets/css/style.css` (all values below are copy-pasted from the real, current file — not aspirational). V2 is additive: every V1 token (colors, 8px spacing scale, `--radius`, `--container-w`) is unchanged and still in force. This document only specifies what's new or extended.

---

## Brand colors (unchanged, restated for reference)

| Token | Value | Use |
|---|---|---|
| `--blue` | `#007BFF` | accent / links / non-text only |
| `--blue-button` | `#0062CC` | filled-button blue — 5.80:1 on white (AA) |
| `--blue-button-hover` | `#004FA3` | button hover state |
| `--navy` | `#0A1A2F` | secondary / dark surfaces / shadow tint source |
| `--green-accent` | `#00E676` | decorative accents only, never text-on-light |
| `--bg-soft` | `#F5F7FA` | page background |
| `--text` | `#333333` | body text |
| `--text-muted` | `#52606D` | secondary text, AA-safe |

No hex value in this table changed during the V2 pass. Every ratio in `QA-REPORT.md` was independently re-verified after the redesign (33 pass / 1 expected warn / 0 fail — identical to pre-redesign).

## Typography System

- Font stack unchanged: `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` — no external font request added.
- Scale: `--fs-sm 0.875rem` · `--fs-base 1rem` · `--fs-md 1.125rem` · `--fs-lg 1.375rem` · `--fs-xl 1.75rem` · `--fs-2xl 2.25rem` · `--fs-3xl 2.75rem` · **new** `--fs-4xl 3.25rem` (hero H1, desktop only).
- Headings: `letter-spacing` tightened and `line-height` reduced site-wide for a denser, more confident display feel, matching the "large headline, small tight tracking" convention identified in the Tailcast DNA report (§2).

## Spacing System (unchanged)

8px baseline, `--space-1` (0.5rem) through `--space-7` (6rem) — no new steps added; V2 works entirely inside the existing rhythm.

## Container Widths (unchanged)

`--container-w: 1180px` — single container width, no change.

## Section Rhythm

Unchanged spacing between sections (`--space-6`/`--space-7`). What changed is *within*-section elevation: section backgrounds can now alternate `--surface-raised` (`#FFFFFF`) and `--surface-sunken` (aliases `--bg-soft`) to create depth without new borders — a direct application of Tailcast DNA §1.

## New Surface / Border / Shadow / Radius / Motion Tokens

```css
--surface-raised: #FFFFFF;
--surface-sunken: var(--bg-soft);
--border-subtle: rgba(10, 26, 47, 0.08);
--border-strong: rgba(10, 26, 47, 0.18);
--radius-lg: 16px;
--radius-xl: 24px;
--radius-full: 999px;
--shadow-xs: 0 1px 3px rgba(10, 26, 47, 0.05);
--shadow-lg: 0 20px 40px rgba(10, 26, 47, 0.16), 0 4px 10px rgba(10, 26, 47, 0.06);
--shadow-glow: 0 10px 24px rgba(0, 98, 204, 0.28);
--ease: cubic-bezier(0.16, 1, 0.3, 1);
--dur-fast: 150ms;
--dur: 250ms;
--dur-slow: 450ms;
```

All shadows are tinted from `--navy` (never true black) — every component's elevation reads as "Smart Geeks navy," not generic gray. `--shadow-glow` is the one accent-tinted shadow, reserved for primary-button hover only, per the one-accent discipline in DNA §12.

## Button Library

| Class | Rest | Hover |
|---|---|---|
| `.btn-primary` | `--blue-button` fill | fill → `--blue-button-hover`, **new**: `--shadow-glow` added, `transform: translateY(-1px)` |
| `.btn-secondary` | outline, `--blue-button` border/text | fill tint, border unchanged |
| `.btn-ghost` | transparent, text-only | subtle background tint |

Transitions now use `--dur-fast` + `--ease` instead of the browser default, so the hover feels snappier and more deliberate.

## Card Library

`.service-card` / `.info-card`:
- Rest: `--shadow-xs`, `--radius-lg`, `1px solid var(--border-subtle)`, `--surface-raised` background (previously flat/borderless).
- Hover: `--shadow-lg`, `translateY(-4px)`, border → `--border-strong`, icon-chip sheen animates in, link arrow gap-animates outward.
- Icon chip: enlarged, now carries its own inset gradient sheen.

`.faq-item`:
- Rest/hover/focus states added (previously static).
- `[open]` state: rotates the `+` indicator to 45° (a single CSS `transform`, replacing the old JS-driven `+`/`−` text swap) — simpler, and animates instead of snapping.

## Form System

- `:focus` states upgraded from a border-color-only change to a `box-shadow` glow ring (`--focus-ring` color, low-opacity spread) — meets and exceeds WCAG 2.2 focus-visibility guidance (non-color-only indicator).
- No field layout, label association, or validation logic changed.

## Alert / Badge System

- `.hero-trust li` badges restyled as pills (`--radius-full`, `--border-subtle`, small icon-dot) instead of plain inline text — same information, clearer as a scannable trust strip.
- Existing `--success`/`--success-bg`/`--error`/`--error-bg` alert tokens (form feedback) unchanged.

## CTA System

- `.cta-block` (the dark full-bleed conversion band): added a `::before` radial-gradient overlay in the brand blue at low opacity, echoing the `.img-frame` circuit-pattern language so dark surfaces across the site now share one visual signature instead of being flat navy rectangles.
- `.mobile-action-bar`: added `env(safe-area-inset-bottom)` padding so the persistent call/directions/WhatsApp bar clears the home-indicator area on notched iOS devices.

## Icon System

- Icon chips (service/info cards) enlarged and given a sheen layer; no new icon set introduced — the existing original SVG icon set (from earlier workstreams) is reused as-is, only its container styling changed.

## Motion Discipline

Every animated property (`box-shadow`, `transform`, `opacity`) uses the new `--ease`/`--dur-*` tokens. Two new JS-driven behaviors, both progressive enhancement, both opt out cleanly:

1. **Header scroll shadow** (`headerScrollState()` in `main.js`) — passive, `requestAnimationFrame`-throttled scroll listener toggling one class.
2. **Scroll-reveal** (`scrollReveal()` in `main.js`) — `IntersectionObserver`-based; checks `prefers-reduced-motion` and `IntersectionObserver` support *before* touching the DOM, and no-ops entirely (content stays at full opacity, exactly as server-rendered) if either check fails. Targets a fixed, safe element list only: `.service-card`, `.info-card`, `.faq-item`, `.hero-trust li`, `.section-head`, `.step-list li`.
3. **Print fix**: `@media print { .reveal { opacity: 1 !important; transform: none !important; } }` — ensures a printed/PDF-exported page never shows blank sections regardless of whether scroll-reveal fired in the browser session that printed it.

---

## What did NOT change (stated explicitly, not left implicit)

- No color hex value.
- No `.py` content module (`business.py`, `services.py`, `pages.py`, `legal.py`, `landing.py`) — all 23 generated pages, 21 sitemap URLs, and all JSON-LD structured data are byte-identical in content.
- No external font or script dependency added.
- No spacing-scale, container-width, or breakpoint value.
- No existing form-validation or analytics JS logic.
