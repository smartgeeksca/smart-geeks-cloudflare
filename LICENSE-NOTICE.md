# License & Third-Party Notice

## Content and code

All written content, HTML/CSS/JS, Python build tooling, and original SVG
artwork in this repository were authored specifically for this project. No
text was copied, scraped, or paraphrased from `www.smartgeeks.ca` or any
other third-party site -- it was used only as a structural/UI reference
(see README.md "Design reference disclosure"). This project is delivered
for Smart Geeks' use; treat it as proprietary to the business unless the
owner chooses to apply an open license.

## Third-party assets

**None.** This build deliberately uses no third-party icon library, no
stock photography, no web font service, and no external CSS/JS framework:

- **Fonts:** the system font stack (`system-ui`, `-apple-system`, "Segoe
  UI", Roboto, "Helvetica Neue", Arial, sans-serif) -- no font files are
  bundled or fetched from a font service.
- **Icons:** all hand-authored SVG (`src/assets/icon_glyphs.py`,
  `src/assets/icons/icon.svg`) -- not from an icon library.
- **Photography:** none included (see IMAGE-ASSET-MANIFEST.md). When real
  photography is added later, ensure it is either genuinely Smart Geeks'
  own photography or properly licensed -- do not source device/repair
  photos from a search engine.

## Third-party services referenced in code (not bundled)

- **Cloudflare Pages / Pages Functions / Email Service** -- the deployment
  target; see DEPLOYMENT.md.
- **Google Analytics 4 / Google Ads conversion tracking** -- only loaded if
  a real ID is configured (`src/data/business.py` -> `ANALYTICS_CONFIG`);
  inert otherwise. Subject to Google's own terms if enabled.
- **Google Maps** -- linked to via a plain search-query URL
  (`maps.google.com/...?q=...`) for directions and the reviews page; no
  Maps API or SDK is embedded.
- **WhatsApp** -- linked to via `wa.me` deep links; no WhatsApp SDK embedded.

## Trademark notice

"MacBook," "iMac," "Mac mini," and "Apple" are trademarks of Apple Inc.
"PlayStation" is a trademark of Sony Interactive Entertainment. "Xbox" is a
trademark of Microsoft Corporation. "Nintendo Switch" is a trademark of
Nintendo. These and any other manufacturer or product names referenced on
this site are used only to identify the devices Smart Geeks can service,
under nominative fair use -- Smart Geeks is an independent repair business
and is not affiliated with, authorized by, sponsored by, or endorsed by any
of these companies. See the independent-business disclosure repeated
throughout the site (footer, About page, every Mac-related service and
landing page) for the full statement.
