# smartgeeks.ca Design DNA Report

Reverse-engineered directly from the live production site at `https://smartgeeks.ca/` this session, using the built-in browser's `getComputedStyle()` against the real DOM (not guessed from screenshots). Every value below is `[LIVE-VERIFIED]` against the real site unless marked otherwise. This report covers design only — layout, tokens, components, rhythm. It does not reproduce or quote the real site's marketing copy, and none of its business-fact claims (see the "Content boundary" section at the end) were copied into the Cloudflare project.

## 1. Layout system

Single-column, section-stacked layout. No sidebar, no persistent secondary nav. Every section is full-bleed (its background spans the viewport) with an inner `max-width: 1200px` container centered via `margin: 0 auto` and `24px` horizontal padding at desktop width. Section vertical rhythm is a flat, consistent `96px` top and bottom padding — every section on the homepage uses the same vertical rhythm value, not a varied scale.

## 2. Grid system

No CSS Grid on the homepage's macro layout — it's a single flow of full-width sections. Grids appear inside sections: the 5-card service grid and the two-column footer both use simple auto-fit/fixed-column grids, not an asymmetric or editorial grid. This is one real structural difference from our own V4 pass, which introduced an asymmetric `split-editorial` (7fr/5fr) grid — the real site doesn't use that pattern; its rhythm comes from alternating section background color (dark/light/dark/light down the page) rather than alternating column widths.

## 3. Typography

`Inter` for body text, `Space Grotesk` for headings and the wordmark — the exact same pairing our own V3 pass already adopted independently. Measured live: H1 = 40.9px / weight 700 / -0.818px letter-spacing / 1.15 line-height; H2 = 28.8px / weight 700. Base body text is 16px / 1.6 line-height.

## 4. Mobile experience (measured at 375×812)

Header collapses to: wordmark, a square icon-button theme toggle (sun/moon), a square hamburger-menu icon-button — nothing else. No phone number, no CTA button in the mobile header. Below the fold, a full-width sticky bottom bar carries the primary conversion action as a single large pill button in a contrasting gold/amber color on a solid blue bar background — a deliberately different accent color from the site's blue brand color, used nowhere else, purely to make that one button impossible to miss. `[RECOMMENDATION]`: adopting a dedicated high-contrast accent for the single highest-intent mobile CTA (vs. today's brand-blue-on-blue-bar) is a real, cheap idea worth a follow-up pass with its own contrast verification — not implemented in this pass to keep this session's scope to what could be fully verified.

## 5. Header

Sticky, `72px`-equivalent height, translucent/blurred background (their light theme: white-family light background; dark theme: navy translucent) — matches our own header's sticky-blur treatment already. Wordmark is two-tone: "Smart" in the ink color, "Geeks" in brand blue — identical pattern to ours.

## 6. Navigation

Primary links with dropdown carets on category items ("Repairs", "Business", "About Us"), a plain "Contact" link, phone number displayed in the nav bar (desktop only) in brand blue. Active page gets a pill/rounded highlight background, not just an underline — one small difference from our current underline-based active-state indicator. `[RECOMMENDATION]`, not implemented this pass.

## 7. Hero

Full-viewport-scale hero (matches our own V4 full-viewport hero treatment already), dark navy background with a soft dual radial-glow plus a fine technical dot/line grid — structurally the same "signature dark surface" idea as our `--mesh-bg` token, independently arrived at. Content order: small pill eyebrow badge → 3-line oversized headline (with the emphasis word on its own line, colored blue) → subhead → two buttons (filled primary + outlined/ghost secondary) → a row of checkmark trust badges.

## 8. CTA placement

Every major section ends with or contains a CTA; the two hero buttons are "Book Now" (primary, filled) and "Call [number]" (secondary, ghost) — the same primary/secondary pairing pattern our hero already uses (ours: "Call" + "WhatsApp"; theirs: "Book" + "Call". Different actions, same two-button hero-CTA structure).

## 9. Service sections

A flat 5-card grid (Phone & Tablet, Laptop & Desktop, Console Fix, Printer & Peripherals, Buy/Sell/Trade) using a "glass card" treatment: `background: rgba(255,255,255,0.06)`, `border: 1px solid rgba(255,255,255,0.12)`, `border-radius: 16px`, `padding: 32px`. Our own service-card component already uses a closely equivalent raised-card treatment (`--surface-raised`, `--border-subtle`, `--radius-lg: 16px`) — the radius value (16px) matches exactly; we use opaque surface colors rather than translucent glass, which is a legitimate token-language difference, not a gap.

**Scope note, stated plainly:** the real site lists "Phone & Tablet" as a repaired category. The Cloudflare project's `services.py` has no phone-repair service page. This is a business-scope question (does Smart Geeks actually offer phone repair, and if so should a page be built for it), not a design question — it is called out here and in the difference report below rather than silently added or silently ignored.

## 10. Footer

Two-column footer (a "Repairs" link column + copyright/manufacturer-disclosure block), dark navy background, a manufacturer-non-affiliation disclosure sentence naming Apple/Samsung/Google/Sony/Microsoft/Nintendo/HP/Canon/Epson/Brother/Lexmark — structurally and substantively the same kind of disclosure our own footer already carries (`GENERAL_DISCLOSURE`/`DISCLOSURE_LONG` in `business.py`), independently required by the same EPRA/manufacturer-trademark realities either business operates under. Our footer uses four columns instead of two; that is a content-density difference (we have more pages to link), not a design gap to close.

## 11. Spacing rhythm

`96px` top/bottom section padding, `24px` container side padding, `1200px` container max-width — all measured live. Our own container is `1180px` (close, a 20px difference, not worth chasing) and our section padding uses a scale (`--space-6: 4rem` = 64px default, `--space-8: 8rem` = 128px for "editorial moment" sections) rather than one flat value. `[RECOMMENDATION]`: standardizing on a single flat 96px-equivalent rhythm across ordinary (non-editorial) sections is a plausible follow-up, not implemented this pass since it would touch every page's section padding.

## 12. Component library

Buttons: `8px` border-radius, `16px 36px` padding at large size, `600` weight — close to ours (`--radius-sm: 6px`, similar padding scale). Cards: `16px` radius, translucent-glass surface. Trust badges: checkmark-icon + bold-lead-word text pattern — exactly the pattern our `.hero-trust` list already uses.

## 13. Card design

See #9 above — glass-morphism on dark backgrounds, opaque-surface-with-subtle-border on light backgrounds (confirmed by toggling their theme live and re-reading computed styles both times).

## 14. Trust elements

A dedicated trust-bar section directly under the hero: 4 stats (Google rating, weekly repair volume, "Surrey, BC since [year]", an e-waste-compliance credential) in a light `rgb(255,255,255)` band with hairline dividers between items — structurally identical in *pattern* to our own `.stat-strip` component (numeral + label, hairline-divided items on its own band). The specific numbers shown (a star rating, a weekly repair count, a "since" year) are that business's own verified figures on their own site; none of them appear anywhere in the Cloudflare project's build, because none of them are in `business.py`'s verified data (`review_rating`, `review_count`, and `years_in_business` are all explicitly `None` in `OWNER_PENDING`) — see the content-boundary section below.

## 15. Visual hierarchy

One idea per section, unequal section "weight" achieved via alternating background color rather than alternating size (their approach) vs. our alternating-column-width `split-editorial` approach (ours) — different mechanism, same underlying principle ("give visual weight to the moment that matters, don't stack identical rows"), which is itself the headline finding of this whole report: **the two sites already share the same design language at the token and principle level** (dark signature surface, two-tone wordmark, Inter+Space Grotesk, checkmark trust badges, hairline-divided stat band, glass/raised cards, primary+ghost button pairing) because our own V3/V4 passes were independently built around the same "premium technical brand" instincts. The single largest, genuinely new, previously-*completely-absent* pattern this pass found and implemented is the **light/dark theme toggle** — real site has one, ours didn't.

## Content boundary — what was deliberately NOT carried over

The real site's hero and trust bar state specific, unverified-in-our-project facts: an exact Google star rating, a weekly repair count, a "Trusted Since 2016" founding-year claim, and a specific EPRA e-waste credential. `business.py`'s `OWNER_PENDING` dict keeps `years_in_business`, `review_rating`, and `review_count` as `None` for exactly this reason — this project's standing rule is that no template renders a number the real Smart Geeks owner hasn't confirmed for *this* deployment. This pass clones the *pattern* (a trust-bar component exists, sized and positioned the same way) using only the Cloudflare project's own already-verified facts (8 device categories, 4 cities served, "100% independently owned") — it does not borrow the real site's numbers. If the owner confirms a founding year, a real review rating, or an e-waste credential, those slot into the existing `--space-5` stat-strip component with no further design work needed.
