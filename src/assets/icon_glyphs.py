# -*- coding: utf-8 -*-
"""
Original, hand-authored line-icon glyphs (24x24 viewBox, stroke style) used
for service cards and page hero frames. No third-party icon library, no
photography -- simple original vector marks matched to the site's stroke
icon style (see the phone/WhatsApp icons in src/templates/layout.py).
"""

_INNER = {
    "laptop": (
        '<rect x="4" y="4" width="16" height="10.5" rx="1" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M2 17.5h20l-1.6 2.3a1 1 0 0 1-.8.4H4.4a1 1 0 0 1-.8-.4L2 17.5Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    ),
    "desktop": (
        '<rect x="7" y="3" width="10" height="15" rx="1.2" stroke="currentColor" stroke-width="1.6"/>'
        '<circle cx="12" cy="15" r="0.9" fill="currentColor"/>'
        '<path d="M9 21h6M12 18v3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    "printer": (
        '<path d="M6.5 9V4.5h11V9" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<rect x="3.5" y="9" width="17" height="7" rx="1.2" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M6.5 16v3.5h11V16" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<circle cx="17" cy="12" r="0.8" fill="currentColor"/>'
    ),
    "console": (
        '<path d="M6 9h12a3 3 0 0 1 3 3.4l-.6 3.6a2 2 0 0 1-3.5 1L15 15H9l-1.9 1.9a2 2 0 0 1-3.5-1L3 12.4A3 3 0 0 1 6 9Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M8 11v2.4M6.8 12.2h2.4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
        '<circle cx="16.2" cy="11.6" r="0.7" fill="currentColor"/>'
        '<circle cx="18" cy="13" r="0.7" fill="currentColor"/>'
    ),
    "macbook": (
        '<rect x="5" y="4.5" width="14" height="9.5" rx="1" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M2.5 17h19l-1.4 2a1 1 0 0 1-.8.4H4.7a1 1 0 0 1-.8-.4L2.5 17Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    ),
    "imac": (
        '<rect x="4" y="3.5" width="16" height="11" rx="1.2" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M10 17.5 9 21M14 17.5l1 3.5M8.5 21h7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    "macmini": (
        '<rect x="5" y="9" width="14" height="4.5" rx="1" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M7 9V7.4A1.4 1.4 0 0 1 8.4 6h7.2A1.4 1.4 0 0 1 17 7.4V9" stroke="currentColor" stroke-width="1.6"/>'
    ),
    "chip": (
        '<rect x="8" y="6" width="8" height="12" rx="1.4" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M8 9H5M8 12H5M8 15H5M16 9h3M16 12h3M16 15h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    "trade": (
        '<path d="M4 8h13.5M17.5 8 14 4.5M20 16H6.5M6.5 16 10 19.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    "diagnose": (
        '<circle cx="10.5" cy="10.5" r="6" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="m19 19-3.8-3.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<path d="M8 10.5h2M13 10.5h2M10.5 8v2M10.5 13v2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    "shield": (
        '<path d="M12 3.5 19 6v6c0 4.4-2.9 7.5-7 8.5-4.1-1-7-4.1-7-8.5V6l7-2.5Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="m9 12 2.2 2.2L15.5 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
}


def glyph(key: str, size: int = 24) -> str:
    inner = _INNER.get(key, _INNER["diagnose"])
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" aria-hidden="true">{inner}</svg>'
