# Tailcast Design DNA Report

**Purpose of this document:** a factual teardown of the *design conventions* used by the open-source Tailcast template (`github.com/matt765/Tailcast`, MIT license), gathered by directly fetching its repository, live demo, and `Theme.css` source. This report captures **patterns only** — layout, spacing, shadow, motion, hierarchy conventions. No Tailcast content, copy, branding, imagery, or code was copied into Smart Geeks. Every dimension below states what Tailcast actually does, then what Smart Geeks' Design System V2 (companion document 02) does instead, using Smart Geeks' own brand tokens.

Tailcast is a **dark-themed** Astro 6 + Tailwind CSS 4 + TypeScript SaaS marketing template. That framing matters: several of its conventions (near-black layered surfaces, an indigo accent glowing against dark backgrounds) are dark-UI techniques. Smart Geeks is a light, trust-first local-service site, so each pattern below was *translated*, not copied — same underlying technique (layering, elevation, motion discipline), different palette and mood.

---

### 1. Layout system
Tailcast uses a single-column marketing layout: full-bleed dark section bands, each containing a centered content container, stacked vertically with no sidebar or app-shell chrome. Sections alternate between flat and subtly-tinted backgrounds to create rhythm without hard borders.
**Applied to Smart Geeks:** already had this shape (`--container-w: 1180px`, stacked `<section>` bands). V2 doesn't change the layout skeleton — it reinforces the alternation using the new `--surface-sunken` token so section bands read as distinct without adding visible rules.

### 2. Visual hierarchy
Tailcast leans on size + weight + one accent color to establish hierarchy, not borders or boxes. Headlines are large and tight (`letter-spacing` pulled in), body copy is comparatively small and muted, and the indigo accent is reserved for the single most important action per section.
**Applied to Smart Geeks:** tightened heading `letter-spacing`/`line-height` (edit #2 of 14), and added `--fs-4xl` for the hero H1 on desktop — a full step above the previous `--fs-3xl` ceiling — so the hero headline now out-scales every other page element the way Tailcast's does.

### 3. Typography scale
Tailcast ships Inter, loaded as a variable font, with a conventional Tailwind default scale (no custom `--fs-*` tokens in `Theme.css` — confirmed by direct inspection, this was a deliberate finding, not an assumption).
**Applied to Smart Geeks:** deliberately did **not** adopt Inter or any Google Font. Smart Geeks' zero-external-font-dependency stance (system-ui stack) predates this redesign and is a real technical/privacy tradeoff, not an oversight — one fewer render-blocking network request, one fewer third-party origin. The "premium" typographic feel Tailcast gets from Inter's proportions was approximated instead through the scale/weight/letter-spacing/line-height refinements above, on the existing `--font-sans` stack.

### 4. Section spacing
Tailcast uses generous, consistent vertical rhythm between sections — large gaps (roughly 96–160px equivalent) that give every block room to breathe, a hallmark of "premium SaaS" pages versus cramped template pages.
**Applied to Smart Geeks:** the existing `--space-7: 6rem` (96px) token already provided this at the top level; V2 didn't need to change the scale, only ensure cards/CTAs *inside* sections now carry their own elevation so the extra whitespace reads as intentional rather than empty.

### 5. Grid structure
Tailcast's card grids are simple, evenly-gapped CSS Grid layouts (2–4 columns depending on breakpoint), no masonry, no asymmetry — the sophistication comes from card treatment, not grid complexity.
**Applied to Smart Geeks:** service/info card grids were already simple, evenly-gapped grids. No change needed here — confirms the existing structure was already aligned with this convention.

### 6. Card system
This is Tailcast's strongest, most distinctive pattern: cards sit on a **layered surface** one step lighter than the page background (`--color-bgDark2` on `--color-bgDark1`), have a **hairline border at low opacity** (0.05–0.15 white alpha) rather than a solid gray border, carry a **soft ambient shadow** even at rest, and **lift and brighten on hover** (translateY + shadow deepen + border opacity increase) — never a hard color-swap hover.
**Applied to Smart Geeks:** this is the single most-copied *technique* (not asset) in V2. `--border-subtle`/`--border-strong` are opacity-based `rgba(10,26,47,…)` borders (Tailcast's technique, Smart Geeks' navy). `.service-card`/`.info-card` now carry `--shadow-xs` at rest (previously flat) and animate to `--shadow-lg` + `translateY(-4px)` on hover, using the new `--ease`/`--dur` motion tokens — same lift-and-brighten grammar, Smart Geeks' own colors.

### 7. Navigation system
Tailcast's header is a slim, sticky bar that stays visually quiet until scrolled, then gains a background blur/shadow to separate itself from content — a common "premium" scroll-aware header pattern.
**Applied to Smart Geeks:** implemented via the new `headerScrollState()` function in `main.js` — a passive, rAF-throttled scroll listener toggling `.site-header.is-scrolled`, which triggers a CSS shadow transition already defined on `.site-header`. Pure progressive enhancement: header works identically with JS disabled, just without the scroll shadow.

### 8. Mobile experience
Tailcast collapses its nav into a full-screen or slide-in mobile menu and keeps CTA buttons full-width and thumb-reachable near the bottom of key sections.
**Applied to Smart Geeks:** unchanged structurally — the site already uses a persistent `.mobile-action-bar` (call/directions/WhatsApp) with `env(safe-area-inset-bottom)` support now added in V2, which is arguably a stronger mobile-conversion pattern than Tailcast's (Tailcast is a SaaS template with no physical-visit/phone-call use case to design for).

### 9. CTA design
Tailcast's primary buttons use the indigo accent with a subtle glow/shadow on hover rather than a flat darken, and pair a solid primary with a ghost/outline secondary — never two solid buttons side by side.
**Applied to Smart Geeks:** `.btn-primary` now gets `--shadow-glow` (a blue-tinted glow shadow, `rgba(0,98,204,0.28)`) on hover instead of only a background-color darken; the existing `.btn-secondary`/`.btn-ghost` outline pairing was already correct and untouched.

### 10. Footer design
Tailcast footers are dark, multi-column, and use a thin gradient or accent-colored top border to separate the footer from the page body rather than a hard horizontal rule.
**Applied to Smart Geeks:** added a 3px gradient accent line via `.site-footer::before` (blue→green, matching Smart Geeks' own two accent colors) and underline accents on `.footer-col h2` headings — same separation technique, Smart Geeks palette.

### 11. Animation system
Tailcast uses restrained, purposeful motion: fade/slide-up reveals as sections scroll into view, hover micro-interactions on cards and buttons, and nothing that loops or auto-plays. Timing is fast (150–300ms) with eased curves, not linear.
**Applied to Smart Geeks:** `--ease: cubic-bezier(0.16,1,0.3,1)` (a standard "ease-out-expo"-family curve) plus `--dur-fast/--dur/--dur-slow` (150/250/450ms) tokens, applied to buttons, cards, header shadow, and the new `.reveal`/`.reveal.is-visible` scroll-reveal utility — same restraint (one reveal pattern, capped stagger, no loops), gated behind `prefers-reduced-motion` (Tailcast's own repo does not document a reduced-motion policy; Smart Geeks' implementation goes further here deliberately, per the brief's accessibility requirements).

### 12. Color strategy
Tailcast uses one accent color (indigo) with extreme discipline — it appears on primary CTAs, active states, and small accent details, and almost nowhere else; everything surrounding it is neutral (near-black/white/gray).
**Applied to Smart Geeks:** zero color values were changed. Smart Geeks already had a comparable two-accent discipline (`--blue-button` for primary actions, `--green-accent` reserved for small decorative accents/badges, never as text-on-light per the existing code comment). V2 reinforced this discipline rather than introducing new colors — the "glow" shadows and gradient overlays reuse the two existing accent hues at low opacity, they don't add a third.

### 13. Shadow system
Tailcast doesn't define custom shadow tokens in `Theme.css` — it uses Tailwind's default `shadow-sm/md/lg/xl` utilities directly (a second confirmed "uses-the-framework-default" finding, alongside typography). The visual effect is still a deliberate elevation scale, just sourced from Tailwind rather than a bespoke token set.
**Applied to Smart Geeks:** built a bespoke elevation scale instead (`--shadow-xs` → `--shadow-lg` → `--shadow-glow`), because Smart Geeks isn't on Tailwind's utility system — this is the equivalent scale expressed as CSS custom properties, tuned to the navy (`#0A1A2F`) shadow tint instead of true black, so shadows read as "this brand's" rather than generic.

### 14. Border system
Tailcast's borders are exclusively opacity-scaled white (`rgba(255,255,255,0.05–0.15)`) since it's a dark UI — never a flat gray hex.
**Applied to Smart Geeks:** translated directly to `--border-subtle: rgba(10,26,47,0.08)` and `--border-strong: rgba(10,26,47,0.18)` — the same *technique* (tint borders from the ink color at low opacity so they auto-harmonize with any surface behind them) inverted for a light UI (navy-tinted instead of white-tinted).

### 15. Component architecture
Tailcast components are consistently "surface + border + shadow + radius" composites — every card, panel, and input follows the same four-property recipe, which is why the whole template feels cohesive despite having many component types.
**Applied to Smart Geeks:** the same recipe was applied consistently across `.service-card`, `.info-card`, `.faq-item`, `.img-frame`, and form fields in V2 — all now share `border-subtle` + a shadow-scale step + `--radius-lg` + a `--surface-*` token, rather than each component having bespoke one-off styling as before.

---

**Two explicit non-findings, stated plainly rather than glossed over:** Tailcast's radius scale and font scale are Tailwind framework defaults, not bespoke design tokens (verified by inspecting `Theme.css` directly — it defines color/spacing/breakpoint tokens but not radius or type-scale tokens). Smart Geeks V2 built genuine bespoke tokens for both anyway, since Smart Geeks isn't on Tailwind and needed real values to reference.
