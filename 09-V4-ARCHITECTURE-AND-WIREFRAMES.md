# V4 Site Architecture & Wireframes

Per the brief's own reliability rules, every page below is labeled by what actually happened to it in this pass — never "redesigned" unless the code was actually changed and rebuilt.

## Homepage — `[SOURCE-MODIFIED]` `[BUILD-VERIFIED]`

New section order (previous order in parentheses where it changed):

1. **Hero** — now a true full-viewport moment on desktop (`min-height: min(86vh, 780px)`), site-wide via the shared `hero()` component.
2. **Stat strip** — unchanged from V3 (8 device categories / 4 cities / 100% independent).
3. **Statement band** *(new)* — one oversized sentence, the site's existing brand-philosophy copy given a dedicated visual moment instead of sitting inside a paragraph.
4. **Repair intelligence** *(new; replaces the old separate "why us" card grid + "how it works" numbered list)* — an asymmetric split: philosophy on the wide left, process flow on the narrow right, in one section instead of two.
5. **Device ecosystem** *(new; replaces a flat 9-card uniform grid)* — 3 labeled clusters (PC & Windows / Apple hardware / Peripherals & consoles) plus a cross-cutting chip-level capability band.
6. **Buy/Sell/Trade flagship** *(new)* — promoted from "1 card among 9" to its own chapter, image + copy in an asymmetric split, its own tag list and CTA.
7. **Local authority** *(new; replaces a generic two-column text+image block)* — service-area copy on the wide left, a mono "readout" card (address/phone/email) on the narrow right.
8. **FAQ** — unchanged (native `<details>/<summary>` accordion; this pattern is not what read as "template," so it wasn't rebuilt for its own sake).
9. **CTA band** — unchanged from V3.
10. **Footer** — unchanged from V3.

## Services index (`/services/`) — `[SOURCE-MODIFIED]` `[BUILD-VERIFIED]`

Same device-ecosystem grouped taxonomy as the homepage, reusing the same `device_ecosystem_html()` function — plus a second capability-style band for buy/sell/trade (this page has no separate flagship section to hold it, unlike the homepage), so all 9 services remain fully discoverable and internal-link-checked (0 broken links, verified).

## Individual service pages (×9) — `[RECOMMENDATION]`

Not rearchitected in this pass. These pages already have a distinct, real per-device content structure (symptoms, process, FAQs, related services) rather than a generic template repeated nine times — the previous audit's finding that they're not interchangeable content still holds. What they inherit automatically, because they share `hero()`, `cta_block()`, `faq_accordion()`, header, and footer with every other page: the full-viewport hero, the shared dark signature surface, and the V3 typography system. A follow-up pass could apply the same "one big idea, not a card grid" thinking to the symptom/process sections specifically — proposed wireframe: hero → statement-style callout (device-specific) → symptom list as a compact technical checklist (not prose) → process (existing step-list, already premium) → FAQ → related-services capability band → CTA.

## About — `[RECOMMENDATION]`
Proposed: replace with the same statement-band + split-editorial pattern — a one-sentence mission statement as a moment, then a `split-editorial` pairing the shop's actual history/approach copy against the local-authority readout card (address/hours-status), instead of a plain text page.

## Contact — `[RECOMMENDATION]`
Proposed: split-editorial with the form on the wide side and a mono "readout" card (address, phone, email, response-channel list) on the narrow side, replacing a single-column form-only layout.

## FAQ (full page) — `[RECOMMENDATION]`
Proposed: group the existing FAQ list under mono category labels (Diagnostics / Pricing & timing / Devices we service / Buy-sell-trade), the same grouped-taxonomy technique used for the device ecosystem, instead of one long undifferentiated accordion list.

## Reviews — `[RECOMMENDATION]`
Proposed: a statement-band opener (one honest sentence about the review approach) followed by the existing review cards restyled with the `.info-card`/elevation treatment already in the system — no fabricated review content, no star-rating invented.

## Policy pages (Privacy / Terms / Warranty / Diagnostic / Accessibility) — `[RECOMMENDATION]`
No structural change proposed. These are long-form legal/reference text; a magazine-editorial treatment would work against their actual job (being scannable, quotable reference text). The V3 typography refinements already apply automatically.

## 404 / Thank-you — `[RECOMMENDATION]`
Proposed: apply the statement-band treatment to the single message these pages carry (e.g., the 404's "page not found" message, the thank-you page's confirmation line), so even a one-line utility page gets real typographic weight instead of looking like unstyled fallback content.

---

**Why the homepage and services index got full implementation and the rest got documented recommendations, stated plainly:** those two pages are where the "template" perception is formed — they're the pages a new visitor and a search engine both land on first, and they're where the flat-grid problem the critique identifies actually lived. Extending the same treatment to all 14+ remaining page types in one pass was judged to trade real, verified depth on the highest-impact pages for shallow, unverified changes spread thin across low-traffic pages (policy pages, 404). The recommendations above are concrete enough to implement directly in a follow-up pass.
