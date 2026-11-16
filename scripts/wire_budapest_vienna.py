#!/usr/bin/env python3
"""Wire /budapest-vienna-river-cruises (EN only) into the site: menu + mobile menu and
footer (on the EN layout master), homepage guide list + its ItemList JSON-LD, sitemap,
nav thumbnail and in-body related links. Idempotent. Run sync_layout.py afterwards
(and build_december.py, build_budapest_amsterdam.py when their copy changed)."""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
EN = "/budapest-vienna-river-cruises"
AMS = "/budapest-amsterdam-river-cruises"
ISO = "2026-11-16"
TITLE = "The 6 Best Budapest to Vienna River Cruises (2027)"
MENU_TITLE = "Budapest to Vienna Cruises"
MENU_SUB = "5 to 8-day Danube cruises from $859"
PHOTO = "assets/budapest-vienna-river-cruises/budapest-vienna-river-cruise-crucemundo-ms-arena-01.avif"
THUMB = "/assets/nav-thumbs/budapest-vienna-river-cruises.avif"


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
    s = after_once(s, r'<a class="ltt-mega-item" href="%s">.*?</a>\n' % AMS,
                   f'<a class="ltt-mega-item" href="{EN}"><img alt="" class="ltt-thumb" data-src="{THUMB}" decoding="async" height="48" width="48"/>'
                   f'<div><strong>{MENU_TITLE}</strong><p>{MENU_SUB}</p></div></a>\n', f'ltt-mega-item" href="{EN}"')
    s = after_once(s, r'<a class="ltt-mobile-link" href="%s">.*?</a>\n' % AMS,
                   f'<a class="ltt-mobile-link" href="{EN}"><span class="ltt-mobile-link-main"><img alt="" class="ltt-thumb" data-src="{THUMB}" decoding="async" height="36" width="36"/>'
                   f'<span>{MENU_TITLE}</span></span></a>\n', f'ltt-mobile-link" href="{EN}"')
    s = after_once(s, r'<a class="footer-link-item" href="%s">[^<]*</a>\n' % AMS,
                   f'<a class="footer-link-item" href="{EN}">Budapest to Vienna River Cruises</a>\n', f'footer-link-item" href="{EN}"')
    return s


def home(s):
    li = (f'<li><a class="hp-guide" href="{EN}"><img alt="MS Arena river cruise ship on the Danube between Vienna and Budapest" loading="lazy" decoding="async" '
          f'src="/{PHOTO}" width="84" height="84"/><span class="hp-guide-txt"><h3>{TITLE}</h3></span>'
          '<span class="hp-guide-go" aria-hidden="true">›</span></a></li>')
    s = after_once(s, r'<li><a class="hp-guide" href="%s">.*?</li>' % AMS, li, f'hp-guide" href="{EN}"')
    if f'"{SITE}{EN}"' not in s:
        m = re.search(r'(\{"@type": "ListItem", "position": )(\d+)(, "url": "%s%s", "name": "[^"]*"\})' % (re.escape(SITE), AMS), s)
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
        assert s.count(old) == 1, (rel, old[:80], s.count(old))
        return s.replace(old, new, 1)
    edit(rel, fn)


# ---- in-body related links ----
AMS_LONG = f'compared in <a href="{AMS}">Budapest to Amsterdam river cruises</a>.'
SHORT_TXT = f' For a shorter trip, the 5 to 8-day <a href="{EN}">Budapest to Vienna river cruises</a> cover the first stretch.'
AMS_ROUTE = "and Emerald and Avalon include <strong>Bratislava</strong>. "
AMS_ROUTE_NEW = AMS_ROUTE + f'Only have a week? The <a href="{EN}">Budapest to Vienna river cruises</a> sail the first stretch in 5 to 8 days. '
XMAS_FAQ_ANCHOR = '    ("When do the Budapest Christmas markets close?",'
XMAS_FAQ = ('    ("Can I take a Christmas river cruise from Budapest to Vienna?",\n'
            '     f"Yes. Emerald (5 days) and Avalon (6 days) sail one way from Budapest to Vienna in late November and December, "\n'
            '     f"with guided tours and Christmas markets in Budapest, Bratislava and Vienna. The cheapest option is a 5-day loop from Vienna via Budapest from $859. "\n'
            f'     f"All six are compared in <a href=\\"{EN}\\">the best Budapest to Vienna river cruises</a>."),\n')

if __name__ == "__main__":
    thumb()
    edit(json.loads((ROOT / "scripts/layout_config.json").read_text())["masters"]["en"], master)
    edit("index.html", home)
    edit("sitemap.xml", sitemap)
    for rel in ("budapest-travel-guide.html", "scripts/itinerary_copy_en.py"):
        link_once(rel, AMS_LONG, AMS_LONG + SHORT_TXT)
    for rel in ("budapest-amsterdam-river-cruises.html", "scripts/build_budapest_amsterdam.py"):
        link_once(rel, AMS_ROUTE, AMS_ROUTE_NEW)
    link_once("best-budapest-river-cruise.html",
              'see the <a href="/budapest-amsterdam-river-cruises">7 best Budapest to Amsterdam river cruises</a>, with 2027 prices from $3,941.</p></details>',
              'see the <a href="/budapest-amsterdam-river-cruises">7 best Budapest to Amsterdam river cruises</a>, with 2027 prices from $3,941.</p></details>\n'
              f'        <details><summary>Is there a river cruise from Budapest to Vienna?</summary><p>Yes, on multi-day cruises of 5 to 8 days, from $859. The one-way sailings run at Christmas; see the <a href="{EN}">6 best Budapest to Vienna river cruises</a>.</p></details>')
    link_once("scripts/december_copy_en.py", XMAS_FAQ_ANCHOR, XMAS_FAQ + XMAS_FAQ_ANCHOR)
