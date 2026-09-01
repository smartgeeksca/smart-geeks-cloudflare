# Design System V3 — Before/After Scorecard & Verification Notes

## Before / After

| Dimension | V2 (previous pass) | V3 (this pass) |
|---|---|---|
| Hero | Light gradient panel, headline capped at 2.75rem | Full-bleed dark signature surface, mesh/grid background, glass eyebrow + trust pills, headline at 4.25rem desktop |
| Dark surfaces | One-off, each with its own gradient (hero was light; only CTA/footer were dark, differently) | Four sections (hero / stat strip / CTA / footer) share one signature background recipe |
| Typography | System-ui only, one weight scale, 800-weight headings | Space Grotesk (display) + Inter (body) + JetBrains Mono (technical accents), 700-weight headings with tighter tracking |
| Homepage feature layout | Uniform equal-width card grid | Asymmetric bento grid (2×2 feature tile + wide tile + two standard tiles) |
| Process section | Numbered circles, no connective visual | Blueprint-style dashed trace line + mono-numbered nodes |
| Trust/proof | Text-only checklist | Honest stat strip (8 device categories / 4 cities / 100% independent) with large mono numerals |
| Header | Near-opaque white bar | Glass/blur backdrop, display-face wordmark |
| Contrast checks tracked | 33 | 38 (5 new on-dark combinations added, all pass ≥7.3:1) |
| Page count / URLs / content | 23 pages / 21 URLs | Unchanged |
| Fabricated content | None | None |

## Verification performed (not just claimed)

- `python3 -m py_compile` on every edited `.py` file — clean.
- Full rebuild (`rm -rf public && python3 build.py`) — 23 HTML files, 21 sitemap entries, no build errors.
- `python3 tests/qa.py` — **38 pass, 1 expected warn, 0 fail**, including the 5 new on-dark contrast pairs this pass introduced (computed independently via the same luminance/contrast functions the test suite uses, then added as permanent, re-runnable checks rather than a one-time calculation).
- Real browser screenshots (Playwright/Chromium) of the rebuilt site — homepage (top-of-page and fully-scrolled), services index, and homepage at a 390px mobile viewport.

## A screenshot artifact found and diagnosed (not shipped as a false alarm, and not shipped as a real bug either)

The first full-page scrolled capture showed the sticky header rendered a second time, overlapping content partway down the page. Diagnosed — not assumed — by disabling `position: sticky` on the header immediately before capture and re-shooting: the duplicate disappeared entirely, which isolates the cause to how Chromium's full-page screenshot stitches together multiple scrolled captures of a `position: sticky` element (it can get "baked in" at each stitched strip), not to anything in the site's real HTML/CSS. A real visitor's browser only ever renders the header once, pinned to the true viewport top. No code change was needed or made for this — it's recorded here so the finding is traceable, consistent with this project's standing practice of diagnosing before concluding.

A second, expected artifact from the *first* scroll-simulation script (500px scroll jumps) reproduced the same category of issue found in the V2 pass: `.reveal` elements that a real user's continuous scroll would trigger normally can be skipped by large discrete jumps. Confirmed via `getComputedStyle(...).opacity` on every `.step-list li` after a realistic, smaller-increment scroll — all four returned `opacity: 1`. Re-shot with smaller scroll increments for the delivered screenshots, which show the process section fully revealed.

## Open items (unchanged from the previous audit, restated for completeness)

Real photography (motherboards, laptop internals, storefront) remains an owner action — nothing in V3 changed that. The mesh/grid signature surface and the circuit-pattern `.img-frame` placeholders are the production-ready interim treatment.

## Owner action still required

Push the two V2 commits plus the new V3 commit(s) — see the delivery message for the exact command. This session has confirmed, tested, denied write access to the GitHub repo throughout this project; it has never had push access.
