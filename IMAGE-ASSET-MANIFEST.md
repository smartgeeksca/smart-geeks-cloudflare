# Image Asset Manifest

## What's already in the package (real, original, finished assets)

No AI image-generation tool was available in this build session, and no
Smart Geeks photography was supplied, so **no photographic images are
included** -- per the brief, none were fabricated or pulled from search
results either. What *is* included is original and finished, not a
placeholder:

| File | Type | Used for |
|---|---|---|
| `src/assets/icons/icon.svg` | Hand-authored SVG wordmark/mark | Header logo, favicon source |
| `src/assets/icons/favicon.ico`, `icon-16/32/48/192/512.png`, `apple-touch-icon.png` | Generated from the mark (`scripts/generate_brand_assets.py`) | Browser tab, home-screen icons, `site.webmanifest` |
| `src/assets/images/og-default.svg` | Original OG/share graphic | Default `og:image` / Twitter card image |
| `src/assets/icon_glyphs.py` | 11 original hand-authored line icons (laptop, desktop, printer, console, macbook, imac, macmini, chip, trade, diagnose, shield) | Service cards, hero image frames |

Every service, landing, and major content page renders a **polished
CSS-based image placeholder** (`.img-frame` in `style.css`, built by
`image_frame()` in `src/templates/layout.py`): a brand-gradient panel with
one of the original line-icon glyphs centered in it, sized with a fixed
`aspect-ratio` so there's no layout shift. This is a deliberate, finished
design choice, not an "image coming soon" box -- but it is a stand-in for
real photography, which is listed below.

## Real photography needed (owner action item)

None of these were fabricated, generated, or pulled from a search engine.
Add real Smart Geeks photography (or a supplied/commissioned photo matching
the description) at the path below, and no layout change is needed --
`.img-frame` already reserves the correct aspect ratio.

Every image should: contain **no people**, avoid generic
technician/lifestyle/handshake stock-photo styling, be exported as WebP
(with a JPEG fallback if your pipeline needs one), and ship at minimum
`800w`/`1200w`/`1600w` for `srcset`.

| Filename (place in `src/assets/images/`) | Dimensions | Aspect | Placement | Alt text to use | Generation / shoot prompt |
|---|---|---|---|---|---|
| `laptop-internals-repair.webp` | 1600x1200 | 4:3 | Laptop repair page hero | "Open laptop chassis on a repair bench showing internal components" | Overhead shot of an open laptop on an anti-static mat, keyboard removed, motherboard and battery visible, diagnostic multimeter nearby, no people, neutral workbench lighting |
| `desktop-components.webp` | 1600x1200 | 4:3 | Desktop repair page hero | "Desktop tower with side panel removed showing internal components" | Open desktop PC case on a bench, motherboard/GPU/cabling visible, no people, clean workbench background |
| `printer-service.webp` | 1600x1200 | 4:3 | Printer repair page hero | "Printer with cover open during a service inspection" | Home/office inkjet or laser printer with the top cover open, print head or paper path visible, no people |
| `console-repair-bench.webp` | 1600x1200 | 4:3 | Gaming console repair hero | "Game console opened for internal inspection on a repair bench" | Disassembled game console shell with internal board and fan visible on an anti-static mat, no people, no visible manufacturer logos in frame |
| `macbook-internals.webp` | 1600x1200 | 4:3 | MacBook repair hero | "MacBook with the back cover removed showing internal layout" | Opened MacBook-style laptop on a bench, battery and logic board visible, precision screwdriver set nearby, no people, no prominent trademarked logo |
| `imac-service.webp` | 1600x1200 | 4:3 | iMac repair hero | "All-in-one desktop computer opened for internal service" | All-in-one desktop with rear panel removed showing internal components, on a bench, no people |
| `macmini-open.webp` | 1600x1200 | 4:3 | Mac mini repair hero | "Compact desktop computer opened for internal inspection" | Small-form-factor desktop computer with the base plate removed, internal board visible, no people |
| `motherboard-macro.webp` | 1600x1200 | 4:3 | Motherboard & chip-level repair hero; Home "services" section | "Close-up of a circuit board during chip-level diagnostic work" | Macro shot of a circuit board with a soldering iron and multimeter probes nearby, no people, shallow depth of field |
| `trade-in-devices.webp` | 1600x1200 | 4:3 | Buy-sell-trade hero | "A collection of used laptops and a games console ready for trade-in assessment" | Several closed laptops and a game console arranged on a counter or bench, no people, no visible personal data on any screens |
| `about-workbench.webp` | 1600x1200 | 4:3 | About page | "Repair workbench with diagnostic tools laid out" | Organized repair bench with a multimeter, precision screwdrivers, and an anti-static mat, no people |
| `store-exterior.webp` (optional) | 1600x1200 | 4:3 | About / homepage (only if genuine Smart Geeks photography is supplied) | "Smart Geeks storefront in Surrey, BC" | **Do not generate this one.** Per the brief, storefront/interior photography must be genuine Smart Geeks photography, not AI-generated. |

## Replacing a placeholder

1. Export the real photo as WebP (and JPEG fallback if needed) at the
   dimensions above, named exactly as listed.
2. Drop it into `src/assets/images/`.
3. In the relevant content file (`src/content/services.py`,
   `src/content/landing.py`, or `src/content/pages.py`), the page's data
   dict already carries an `"icon"` key used by `image_frame()`; swap that
   call for a real `<picture>`/`<img>` with the new file, matching
   `width`/`height` to the aspect ratio above so there's no layout shift.
   `build.py`'s per-page render functions are the single place this needs
   updating per page.
4. Re-run `python3 build.py` and `python3 tests/qa.py`.

## Not included, and why

- **Store exterior/interior photography** -- explicitly reserved for real
  Smart Geeks photography only (see brief: "only if genuine Smart Geeks
  photography is supplied").
- **Before/after repair photography** -- same reasoning; documented as a P3
  item in `CHANGELOG.md`.
- **Any image containing people** -- excluded entirely, per requirement.
