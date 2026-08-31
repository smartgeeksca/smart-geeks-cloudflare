#!/usr/bin/env python3
"""
One-time generator for raster favicon assets (from the hand-authored
src/assets/icons/icon.svg mark, redrawn directly with Pillow for crisp
raster output at each required size) and the original per-category hero
line-art SVGs used as .img-frame content on service and landing pages.

Run with: python3 scripts/generate_brand_assets.py
Idempotent -- safe to re-run; it always overwrites its own output files.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(ROOT, "src", "assets", "icons")
IMAGES_DIR = os.path.join(ROOT, "src", "assets", "images")
os.makedirs(ICONS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

NAVY = (10, 26, 47, 255)
GREEN = (0, 230, 118, 255)
BLUE = (0, 123, 255, 255)
WHITE = (255, 255, 255, 255)


def draw_mark(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = round(size * 0.22)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=NAVY)
    cx = cy = size / 2
    arm = size * 0.30
    stroke = max(2, round(size * 0.045))
    # 4 cardinal + 4 diagonal prongs (chip/circuit motif), matching icon.svg
    import math
    for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        a = math.radians(angle_deg)
        x0 = cx + math.cos(a) * (size * 0.14)
        y0 = cy + math.sin(a) * (size * 0.14)
        x1 = cx + math.cos(a) * arm
        y1 = cy + math.sin(a) * arm
        d.line([x0, y0, x1, y1], fill=GREEN, width=stroke)
    chip = size * 0.25
    d.rounded_rectangle(
        [cx - chip, cy - chip, cx + chip, cy + chip],
        radius=max(2, round(size * 0.03)), fill=BLUE,
    )
    return img


def main():
    # PNG icons at common sizes
    sizes = {
        "icon-16.png": 16, "icon-32.png": 32, "icon-48.png": 48,
        "icon-192.png": 192, "icon-512.png": 512,
        "apple-touch-icon.png": 180,
    }
    generated = []
    ico_frames = []
    for name, size in sizes.items():
        img = draw_mark(size)
        path = os.path.join(ICONS_DIR, name)
        img.save(path)
        generated.append(path)
        if size in (16, 32, 48):
            ico_frames.append(img)

    # favicon.ico as a multi-size ICO
    ico_path = os.path.join(ICONS_DIR, "favicon.ico")
    ico_frames[-1].save(ico_path, sizes=[(16, 16), (32, 32), (48, 48)])
    generated.append(ico_path)

    # og-default.svg -- simple original OG/share image (navy bg, mark, wordmark)
    og_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#0A1A2F"/>
  <rect x="0" y="0" width="1200" height="630" fill="url(#g)" opacity="0.5"/>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1200" y2="630" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0A1A2F"/>
      <stop offset="1" stop-color="#14304F"/>
    </linearGradient>
  </defs>
  <g transform="translate(120,205) scale(3.5)">
    <rect width="64" height="64" rx="14" fill="#0A1A2F" stroke="#1E3A5C" stroke-width="1"/>
    <g fill="none" stroke="#00E676" stroke-width="3" stroke-linecap="round">
      <path d="M32 14v8"/><path d="M32 42v8"/><path d="M14 32h8"/><path d="M42 32h8"/>
      <path d="M20.5 20.5l5.6 5.6"/><path d="M37.9 37.9l5.6 5.6"/>
      <path d="M43.5 20.5l-5.6 5.6"/><path d="M26.1 37.9l-5.6 5.6"/>
    </g>
    <rect x="24" y="24" width="16" height="16" rx="3" fill="#007BFF"/>
  </g>
  <text x="360" y="290" font-family="Arial, Helvetica, sans-serif" font-size="64" font-weight="700" fill="#FFFFFF">Smart Geeks</text>
  <text x="360" y="345" font-family="Arial, Helvetica, sans-serif" font-size="30" fill="#C7D2E0">Independent Electronics Repair &#8212; Surrey, BC</text>
</svg>
"""
    og_path = os.path.join(IMAGES_DIR, "og-default.svg")
    with open(og_path, "w") as f:
        f.write(og_svg)
    generated.append(og_path)

    for p in generated:
        print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
