#!/usr/bin/env python3
"""Generate deterministic sample product photos for the image classifier.

Three categories, each with a clear colour identity:
  - Electronics: cool greys / blues (phones, tablets, consoles)
  - Groceries  : warm reds / oranges (canned food, fruit)
  - Clothing   : greens / teals (t-shirts, jackets, shoes)

Each photo is a small "product shot" drawn with PIL. Production categories use
a dominant hue band plus some variety so nearest-centroid training works.
"""
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")

SIZE = 96

PALETTES = {
    "Electronics": [(20, 90, 190), (10, 70, 160), (40, 110, 210), (0, 60, 140)],
    "Groceries": [(230, 90, 50), (240, 130, 40), (210, 60, 40), (250, 150, 60)],
    "Clothing": [(30, 150, 110), (50, 170, 130), (20, 130, 100), (60, 160, 120)],
}

SHAPES = ["rect", "circle", "triangle"]


def draw_product(palette: list, seed: int):
    rnd = random.Random(seed)
    im = Image.new("RGB", (SIZE, SIZE), (245, 245, 248))
    d = ImageDraw.Draw(im)
    body = tuple(c + rnd.randint(-14, 14) for c in palette[seed % len(palette)])
    body = tuple(max(0, min(255, c)) for c in body)
    accent = tuple(min(255, c - 25) for c in body)
    shape = SHAPES[seed % len(SHAPES)]
    pad = 12
    x0, y0, x1, y1 = pad, pad, SIZE - pad, SIZE - pad
    if shape == "rect":
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=body,
                            outline=accent, width=3)
    elif shape == "circle":
        d.ellipse([x0, y0, x1, y1], fill=body, outline=accent, width=3)
    else:
        d.polygon([(SIZE // 2, y0), (x0, y1), (x1, y1)], fill=body, outline=accent)
    d.ellipse([x0 + 8, y0 + 8, x1 - 8, y1 - 8], outline=(255, 255, 255), width=2)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    per_category = 8
    for cat in PALETTES:
        folder = os.path.join(OUT, cat)
        os.makedirs(folder, exist_ok=True)
        for i in range(per_category):
            im = draw_product(PALETTES[cat], seed=i * 7 + 3)
            path = os.path.join(folder, f"{cat.lower()}_{i + 1:02d}.png")
            im.save(path)
    print(f"Generated {len(PALETTES) * per_category} photos under {OUT}")


if __name__ == "__main__":
    main()