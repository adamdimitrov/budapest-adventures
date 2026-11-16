#!/usr/bin/env python3
"""Replace the illustrated icon thumbnails in the menu with photo thumbnails, 2026-11-16.

Every language master (scripts/layout_config.json) has the same 8 icon items, in the
same order, in the mega menu and again in the mobile menu. This makes a 96x96 photo
thumb for each from an existing site photo, swaps the icon span for an <img> like the
other menu items, then run scripts/sync_layout.py to copy the menu to every page.

    python3 scripts/nav_photo_thumbs.py && python3 scripts/sync_layout.py
"""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CDN = "assets/cdn/60e43c7d6d05b671dff0dc1a/"


def first_card_photo(page):
    s = (ROOT / page).read_text(encoding="utf-8")
    c = s[s.index('id="card-1"'):]
    return re.search(r'<img alt="[^"]*"[^>]*?src="/(assets/[^"]+)"', c).group(1)


# in menu order
THUMBS = [
    ("things-to-do-budapest-november", first_card_photo("things-to-do-budapest-november.html")),
    ("things-to-do-budapest-december", first_card_photo("things-to-do-budapest-december.html")),
    ("budapest-itinerary", CDN + "63c134f528404a4d6f6f16b9_9_Széchenyi Chain Bridge.webp"),
    ("budapest-card-is-it-worth-it", CDN + "64823741c9e79f16c66f949c_2-budapest-card.webp"),
    ("budapest-airport-to-city-center", CDN + "6482387c7208ad4d8e5a75fc_3-getting-from-budapest-airport-to-city-centre.webp"),
    ("best-hostels-budapest", CDN + "649187aa6fba10735a62132d_06-best-hostels-in-budapest.webp"),
    ("budapest-tourism-statistics", CDN + "63c134f56cbc4a378df403f4_3_1%20Fisherman%27s%20Bastion.webp"),
    ("hungary-tourism-statistics", CDN + "630b4ef13591b53be87b5f75_07-Budapest-Parliament.webp"),
]


def make_thumbs():
    out = []
    for name, src in THUMBS:
        p = ROOT / src.replace("%20", " ").replace("%27", "'")
        im = Image.open(p).convert("RGB")
        w, h = im.size
        side = min(w, h)
        im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side)).resize((96, 96), Image.LANCZOS)
        dst = f"assets/nav-thumbs/{name}.webp"
        im.save(ROOT / dst, quality=82)
        out.append("/" + dst)
    return out


ICON = re.compile(r'<span class="ltt-thumb ltt-thumb-icon(?: ltt-thumb-month)?" style="width:(\d+)px;height:\d+px;[^"]*">'
                  r'(?:<svg.*?</svg>|<span class="ltt-month-top">[^<]*</span>[^<]*)</span>', re.S)


def main():
    thumbs = make_thumbs()
    cfg = json.loads((ROOT / "scripts/layout_config.json").read_text())
    for lang, f in cfg["masters"].items():
        s = (ROOT / f).read_text(encoding="utf-8")
        hits = list(ICON.finditer(s))
        assert len(hits) == 16, (lang, len(hits))
        for i, m in reversed(list(enumerate(hits))):
            size = m.group(1)
            img = f'<img alt="" class="ltt-thumb" data-src="{thumbs[i % 8]}" decoding="async" height="{size}" width="{size}"/>'
            s = s[:m.start()] + img + s[m.end():]
        (ROOT / f).write_text(s, encoding="utf-8")
        print(lang, "ok")


if __name__ == "__main__":
    main()
