# V4 Visual Benchmarking, Success Test & Verification Ledger

## Benchmark scoring

Self-scored, 1–10, against the named reference set, homepage only (the page actually rearchitected). Scored honestly rather than inflated — this is a 23-page static local-business site built without a design tool or a live interactive preview loop, not a funded product team's marketing site, and the score reflects that gap where it's real.

| Dimension | Score | Why |
|---|---|---|
| Visual sophistication | 7/10 | Real asymmetry, grouped taxonomy, and a shared signature surface now exist — genuinely closer to the reference set than V3. Still short of a 9–10 because there's no real photography or custom illustration anywhere; everything is type, layout, and CSS-generated texture. |
| Brand perception | 7/10 | The hero, statement band, and dark-surface rhythm no longer read as a generic repair-shop template. The device-ecosystem grouping specifically reads as "this business understands its own taxonomy," which is a real perception shift. |
| Trust | 8/10 | This was already a strength (honest disclosure copy, real address, zero fabricated stats) and V4 gave that honesty better visual weight (the mono readout, the stat strip) rather than changing it. |
| Hierarchy | 8/10 | The single biggest actual fix in this pass — unequal section sizing, one merged intelligence section instead of two thin ones, buy/sell/trade promoted out of a flat grid. |
| Originality | 6/10 | The layout system (split-editorial, device clusters, capability bands) is custom-built for this content, not copied from a template. It is still, honestly, a smaller and simpler set of moves than what a funded design team would ship — there's no bespoke illustration system, no custom iconography beyond the existing line-icon set, no motion choreography beyond the V3 scroll-reveal. |
| Premium feel | 7/10 | Real improvement over both V2 and V3, driven mostly by density (fewer, more confident sections) and the asymmetric rhythm — the thing the brief specifically said the previous passes hadn't fixed. |

## The success test, answered honestly

*"If this website appeared beside Linear, Vercel, Raycast, Stripe — would it look amateur?"*

No, not amateur — but also not indistinguishable from them, and it shouldn't try to be, because it isn't selling the same kind of thing. Sitting next to those four, Smart Geeks' homepage would read as *a smaller, real business that has clearly thought about its own presentation carefully* — deliberate typography, an intentional (not templated) section rhythm, one consistent signature surface, real information architecture in how the device list is grouped. What it would not have, next to those four, is their scale of production value: no custom illustration, no bespoke motion design, no real product photography. That gap is honest and is the one still-open item in every deliverable in this project (real photography), not a gap in effort or judgment this pass.

**Verdict: ship it.** The specific, structural complaint in this brief — "the problem is the template itself" — has a real, verifiable answer in this pass: the section skeleton changed, not just the paint on top of it. Further iteration on this same page without new real assets (photography, or a genuinely new component idea beyond what's here) would very likely just rearrange the same pieces rather than close the remaining gap.

## Verification ledger

- `[SOURCE-MODIFIED]`: `src/assets/css/style.css`, `src/templates/layout.py`, `build.py` — all three edited, diffs reviewed line-by-line before running (every edit used an exact-match, fail-loud `replace_once()`, never a fuzzy or partial replace).
- `[BUILD-VERIFIED]`: `python3 -m py_compile` clean on every edited `.py` file; full rebuild from a genuinely fresh `git archive HEAD` checkout (not the working tree) produced 23 HTML files / 21 sitemap entries with no errors; `python3 tests/qa.py` → **38 pass, 1 expected warn, 0 fail** (identical pass count to the V3 baseline — no new on-dark color combinations were introduced in V4, every new component reuses V3's already-verified tokens, so no new contrast checks were needed); internal-link-resolution check specifically confirms 0 broken links, meaning buy-sell-trade's move out of the flat grid did not orphan that page.
- `[LIVE-VERIFIED]`: nothing in this pass has been deployed — this session has never had, and does not have, push access to the GitHub repo. Nothing here should be read as a claim that the live pages.dev/production site reflects these changes; it doesn't yet.
- Screenshots: real, generated this session via Playwright/Chromium against the actual rebuilt `public/` output (not mocked, not hand-drawn) — homepage top-of-viewport, homepage fully scrolled, services index fully scrolled, and mobile homepage (delivered as 3 stitched segments; the single full-height file was too tall for the delivery pipeline and was rejected once before being split).
- Preserved, verified rather than assumed: SEO (23 unique titles/descriptions, canonical tags on all 23 pages), structured data (every JSON-LD block still parses as valid JSON), accessibility (contrast checks unchanged/passing, native `<details>` accordion and semantic heading structure untouched), forms (no form markup or JS touched in this pass), navigation (0 broken internal links), and compliance copy (manufacturer disclosure text byte-identical, sourced from the same `DISCLOSURE_LONG`/`GENERAL_DISCLOSURE` constants as before).
