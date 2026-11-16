#!/usr/bin/env python3
"""Wire /budapest-amsterdam-river-cruises (EN only) into the site: menu + mobile menu and
footer (on the EN layout master), homepage guide list + its ItemList JSON-LD, sitemap,
nav thumbnail and in-body related links. Idempotent. Run sync_layout.py afterwards."""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
EN = "/budapest-amsterdam-river-cruises"
ISO = "2026-11-16"
TITLE = "The 7 Best Budapest to Amsterdam River Cruises (2027)"
MENU_TITLE = "Budapest to Amsterdam Cruises"
MENU_SUB = "15-day Danube &amp; Rhine cruises compared"
PHOTO = "assets/budapest-amsterdam-river-cruises/budapest-amsterdam-river-cruise-emerald-splendours-01.avif"
THUMB = "/assets/nav-thumbs/budapest-amsterdam-river-cruises.avif"


def edit(rel, fn):
    p = ROOT / rel
    s = p.read_text()
    new = fn(s)
    if new != s:
        p.write_text(new)
        print("edited", rel)


def after_once(s, anchor_re, block, guard):
    if guard in s:
        return s
    m = re.search(anchor_re, s, re.S)
    assert m, anchor_re
    return s[:m.end()] + block + s[m.end():]


def thumb():
    im = Image.open(ROOT / PHOTO).convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side)).resize((96, 96), Image.LANCZOS)
    im.save(ROOT / THUMB.lstrip("/"), quality=70)


def master(s):
    s = after_once(s, r'<a class="ltt-mega-item" href="/unlimited-prosecco-cruises-budapest">.*?</a>\n',
                   f'<a class="ltt-mega-item" href="{EN}"><img alt="" class="ltt-thumb" data-src="{THUMB}" decoding="async" height="48" width="48"/>'
                   f'<div><strong>{MENU_TITLE}</strong><p>{MENU_SUB}</p></div></a>\n', f'ltt-mega-item" href="{EN}"')
    s = after_once(s, r'<a class="ltt-mobile-link" href="/unlimited-prosecco-cruises-budapest">.*?</a>\n',
                   f'<a class="ltt-mobile-link" href="{EN}"><span class="ltt-mobile-link-main"><img alt="" class="ltt-thumb" data-src="{THUMB}" decoding="async" height="36" width="36"/>'
                   f'<span>{MENU_TITLE}</span></span></a>\n', f'ltt-mobile-link" href="{EN}"')
    s = after_once(s, r'<a class="footer-link-item" href="/best-private-boat-tours-budapest">[^<]*</a>\n',
                   f'<a class="footer-link-item" href="{EN}">Budapest to Amsterdam River Cruises</a>\n', f'footer-link-item" href="{EN}"')
    return s


def home(s):
    li = (f'<li><a class="hp-guide" href="{EN}"><img alt="Emerald river cruise ship on the Danube, Budapest to Amsterdam" loading="lazy" decoding="async" '
          f'src="/{PHOTO}" width="84" height="84"/><span class="hp-guide-txt"><h3>{TITLE}</h3></span>'
          '<span class="hp-guide-go" aria-hidden="true">›</span></a></li>')
    s = after_once(s, r'<li><a class="hp-guide" href="/best-private-boat-tours-budapest">.*?</li>', li, f'hp-guide" href="{EN}"')
    if f'"{SITE}{EN}"' not in s:
        m = re.search(r'(\{"@type": "ListItem", "position": )(\d+)(, "url": "%s/best-private-boat-tours-budapest", "name": "[^"]*"\})' % re.escape(SITE), s)
        assert m
        pos = int(m.group(2)) + 1
        add = f', {{"@type": "ListItem", "position": {pos}, "url": "{SITE}{EN}", "name": "{TITLE}"}}'
        tail = s[m.end():]
        end = tail.index("]")
        renum = re.sub(r'"position": (\d+)', lambda x: f'"position": {int(x.group(1)) + 1}', tail[:end])
        s = s[:m.end()] + add + renum + tail[end:]
    return s


def sitemap(s):
    if f"<loc>{SITE}{EN}</loc>" in s:
        return s
    entry = (f"  <url>\n    <loc>{SITE}{EN}</loc>\n    <lastmod>{ISO}</lastmod>\n    <changefreq>weekly</changefreq>\n"
             f"    <priority>0.8</priority>\n"
             f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{EN}" />\n'
             f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{EN}" />\n  </url>\n')
    return s.replace("</urlset>", entry + "</urlset>")


def link_once(rel, old, new):
    def fn(s):
        if f'href="{EN}"' in s and new in s:
            return s
        assert s.count(old) == 1, (rel, old, s.count(old))
        return s.replace(old, new, 1)
    edit(rel, fn)


if __name__ == "__main__":
    thumb()
    edit(json.loads((ROOT / "scripts/layout_config.json").read_text())["masters"]["en"], master)
    edit("index.html", home)
    edit("sitemap.xml", sitemap)


# ---- in-body related links ----
LONGER_TXT = ('Starting or ending a longer river cruise here? The 15-day Danube and Rhine sailings are compared in '
              f'<a href="{EN}">Budapest to Amsterdam river cruises</a>.')
if __name__ == "__main__":
    for rel in ("budapest-travel-guide.html", "scripts/itinerary_copy_en.py"):
        old = 'it is dark by about 16:00.</li>' if rel.endswith(".html") else "it is dark by about 16:00.'),"
        new = (f'it is dark by about 16:00.</li><li><strong>Longer river cruise:</strong> {LONGER_TXT}</li>' if rel.endswith(".html")
               else f"it is dark by about 16:00.'),\n    (\"Longer river cruise\", '{LONGER_TXT}'),")
        link_once(rel, old, new)
    link_once("best-budapest-river-cruise.html",
              '<details><summary>Can I cancel?</summary><p>Yes, with a full refund up to 24 hours before the cruise. The ticket is an instant mobile ticket.</p></details>',
              '<details><summary>Can I cancel?</summary><p>Yes, with a full refund up to 24 hours before the cruise. The ticket is an instant mobile ticket.</p></details>\n'
              f'        <details><summary>Looking for a multi-day river cruise?</summary><p>This page is about the 1-hour sightseeing cruises in Budapest. For 15 days on the Danube, Main and Rhine, see the <a href="{EN}">7 best Budapest to Amsterdam river cruises</a>, with 2027 prices from $3,941.</p></details>')
