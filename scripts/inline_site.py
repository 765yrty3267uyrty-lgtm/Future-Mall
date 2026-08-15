#!/usr/bin/env python3
"""Inline CSS and JS into index.html so the site has no external style/script deps."""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE = os.path.join(ROOT, "website")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_site", "index.html")


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_css():
    constants = load(os.path.join(ROOT, "shared", "constants.css"))
    style = load(os.path.join(WEBSITE, "style.css"))
    lines = [l for l in style.split("\n") if not l.strip().startswith("@import")]
    return constants + "\n" + "\n".join(lines)


def main():
    html = load(os.path.join(WEBSITE, "index.html"))

    css = build_css()
    html = html.replace(
        '<link rel="stylesheet" href="style.css">',
        "<style>\n" + css + "\n</style>",
    )

    js = load(os.path.join(WEBSITE, "script.js"))
    html = html.replace(
        '<script src="script.js"></script>',
        "<script>\n" + js + "\n</script>",
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(OUT) / 1024
    print("built", OUT, f"({size:.1f} KB)")
    print("inline style present:", "<style>" in html)
    print("inline script present:", "<script>\n" in html)
    print("external style.css ref gone:", 'href="style.css"' not in html)
    print("external script.js ref gone:", 'src="script.js"' not in html)


if __name__ == "__main__":
    main()