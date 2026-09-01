# Smart Geeks Premium Experience Framework & Design System V3

## Part A — Premium Experience Framework

**Brand personality.** Precise, not friendly-for-its-own-sake. Smart Geeks' entire content strategy (established in earlier workstreams) is built on *diagnosis before repair, honesty about limits* — that's already an engineering-company personality, not a corner-shop one. V3's job was to make the visual language finally agree with the copy: technical, exact, a little austere, confident enough to use a lot of negative space and one recurring dark "instrument panel" surface rather than decorating every section differently.

**Visual tone.** Dark, grid-lined, mono-accented surfaces (hero / stat strip / CTA / footer) alternating with calm white sections carrying an asymmetric bento layout and a blueprint-style process diagram. The tone reference isn't "friendly neighborhood shop" — it's closer to a diagnostic instrument's control panel: exact, quiet, technical.

**Emotional outcome.** A visitor should feel the same thing they'd feel opening a well-made piece of test equipment: *this was built by people who know exactly what they're doing at a component level.* Not excitement, not warmth-first — competence-first, warmth second (the warmth already lives in the copy: "we'll tell you when a repair isn't worth it").

**Trust positioning.** Trust is earned through precision, not through smiling-technician photography (explicitly excluded, per brief and per this project's standing zero-fabrication discipline). The honest, countable stat strip (8 device categories, 4 cities, 100% independent) is the trust mechanism — real numbers, presented with the visual weight a SaaS company would give a funding figure, but never inflated past what's actually true.

**Technology positioning.** Smart Geeks is positioned visually as a technical operation that happens to serve a local market, not a local shop that happens to touch technology. The blueprint/schematic process diagram and the circuit-pattern image placeholders both do this work without a single fabricated photo.

**Local authority positioning.** The "Where we serve" section and footer address block keep the specific, ungeneralized local facts (exact street address, the real four-city service area) sitting directly inside the same premium visual system — local specificity and technical polish aren't presented as being in tension.

**Competitive positioning.** Every competitor in this vertical (independent and franchise repair shops alike) uses some variation of stock-photo-and-blue-gradient template design. A visitor who has seen a Linear, Stripe, or Vercel marketing page will recognize Smart Geeks' visual grammar immediately — that recognition is the entire competitive bet of this redesign.

**Visual vision statement.** *Smart Geeks should look like the engineering team that would get hired to fix the hardware, not the sales team that would get hired to sell you a service plan.*

---

## Part B — Design System V3 (what's actually implemented)

Every value below is live in `src/assets/css/style.css` / `src/templates/layout.py` right now — not aspirational.

### Typography
- **Display** (`--font-display`): Space Grotesk — headlines, wordmark, section headings.
- **Body** (`--font-sans`): Inter — paragraph copy, nav, buttons.
- **Mono** (`--font-mono`): JetBrains Mono — eyebrows, stat numerals, footer column labels, step numbers, section labels.
- Loaded via a single Google Fonts request (preconnected, `display=swap`, only the weights actually used: 400/500/600/700 Inter, 500/700 Space Grotesk, 500/700 JetBrains Mono), with a full system-font fallback stack so the page is correctly styled even if the request is blocked. This is a deliberate, documented reversal of the project's earlier "zero external font dependency" choice — self-hosting was evaluated first and ruled out only because this build environment has no network path to fetch font binaries; Google Fonts was the next-best option precisely because it's what it is: one widely-cached, low-cost request, the same technique many premium SaaS marketing sites use.
- New scale step: `--fs-5xl: 4.25rem` — the desktop hero headline, up from the previous ceiling of `--fs-3xl` (2.75rem).

### Color / surface system
No brand hex value changed. One new tier added: `--ink-2: #14304F` (used by the stat strip), plus three on-dark text tokens — `--text-on-dark` (#FFFFFF), `--text-on-dark-muted` (#C7D2E0), `--blue-on-dark` (#8FC4FF) — every one independently contrast-checked against both `--navy` and `--ink-2` and added as permanent entries in `tests/qa.py`'s `check_contrast()` (all ≥7.3:1, comfortably past AA's 4.5:1 floor).

### The shared "signature surface" (`--mesh-bg`)
The single highest-leverage change in this pass: hero, stat strip, CTA block, and footer all now render the *same* layered background recipe (two radial-gradient glows in the brand blue/green at low opacity, plus a fine two-axis grid-line pattern) via one shared CSS custom property. Previously each dark section had its own bespoke gradient; now there are four instances of one signature, which is what makes them read as a deliberate brand surface instead of four separately-tweaked components.

### New components
- **`.stat-strip`** — dark signature-surface band, large mono numerals, three honest counts (device categories, cities served, independence). Sits directly under the hero on the homepage.
- **`.bento-grid`** — additive class on top of the existing `.card-grid`; asymmetric 4-column layout (one 2×2 feature tile + one wide tile + two standard tiles) applied only to the homepage "why an independent shop" section. Every other `.card-grid` usage (services index, related-services blocks) is untouched.
- **Blueprint process diagram** — `.step-list` gained a dashed connecting trace line and mono-numbered nodes, giving the repair-process section a schematic feel without any new imagery.
- **`.section-label`** — small mono, uppercase, tracked technical label used above section headings (e.g. "— WHY AN INDEPENDENT SHOP").

### Refined existing components
- Header: glass backdrop (14px blur, translucent white) instead of a near-opaque bar; wordmark set in the display face.
- Footer: shares the mesh-bg signature surface via a `::after` layer (kept separate from the existing `::before` gradient accent line), column headings set in mono uppercase.
- Every heading site-wide now uses `--font-display` instead of the body font, at a slightly lower weight (700 vs. the previous 800) with tighter tracking (-0.03em vs -0.02em) — a deliberate "confident but not shouting" adjustment consistent with the Stripe/Linear reference set.

### What did NOT change
No content, copy, service descriptions, FAQ answers, or business facts. No page count (still 23 pages / 21 sitemap URLs). No color contrast regression anywhere (38 checks pass, 0 fail, 1 expected warn — up from 33 checks pre-V3, the 5 new ones covering every new on-dark combination). No fabricated statistic — the stat strip uses exactly three facts that are true today and would still be true if independently checked against `src/data/business.py`.
