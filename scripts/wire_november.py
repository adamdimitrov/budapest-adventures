#!/usr/bin/env python3
"""Wire the November page (EN + HU) into the site: menus (on the layout masters),
homepages, sitemap and in-body links. Idempotent. Run sync_layout.py afterwards.
Sister of scripts/wire_december.py: November entries go right before December."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
EN, HU = "/things-to-do-budapest-november", "/hu/budapest-programok-november"
EN_DEC, HU_DEC = "/things-to-do-budapest-december", "/hu/budapest-programok-december"
ISO = "2026-11-15"
TITLE_EN = "8 Best Things to Do in Budapest in November 2026"


def edit(rel, fn):
    p = ROOT / rel
    s = p.read_text()
    new = fn(s)
    if new != s:
        p.write_text(new)
        print("edited", rel)


def before_once(s, marker_re, block, guard):
    if guard in s:
        return s
    m = re.search(marker_re, s, re.S)
    assert m, marker_re
    return s[:m.start()] + block + s[m.start():]


# ---- menus on the layout masters (right before the December entry) ----
def en_menu(s):
    s = before_once(s, rf'<a class="ltt-mega-item" href="{EN_DEC}">',
                    f'<a class="ltt-mega-item" href="{EN}">\n<div>\n<strong>Budapest in November</strong>\n'
                    '<p>Night cruises, hot pools &amp; market openings</p>\n</div>\n</a>\n', f'ltt-mega-item" href="{EN}"')
    s = before_once(s, rf'<a class="ltt-mobile-link" href="{EN_DEC}">',
                    f'<a class="ltt-mobile-link" href="{EN}">\n<span>Budapest in November</span>\n</a>\n', f'ltt-mobile-link" href="{EN}"')
    return s


def hu_menu(s):
    s = before_once(s, rf'<a class="ltt-mega-item" href="{HU_DEC}">',
                    f'<a class="ltt-mega-item" href="{HU}">\n<div>\n<strong>Budapest novemberben</strong>\n'
                    '<p>Esti hajók, forró medencék, vásárnyitás</p>\n</div>\n</a>\n', f'ltt-mega-item" href="{HU}"')
    s = before_once(s, rf'<a class="ltt-mobile-link" href="{HU_DEC}">',
                    f'<a class="ltt-mobile-link" href="{HU}">\n<span>Budapest novemberben</span>\n</a>\n', f'ltt-mobile-link" href="{HU}"')
    return s


# ---- homepages ----
def en_home(s):
    li = (f'<li data-until="2026-12-01T00:00:00+01:00"><a class="hp-guide" href="{EN}"><img alt="Legenda evening cruise passing the lit-up Parliament in Budapest" '
          'loading="lazy" decoding="async" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/68f3738fe72bf6e25526e991_best-budapest-river-cruises-legenda-sightseeing-cruise-00025.avif" width="64" height="64"/>'
          f'<span class="hp-guide-txt"><h3>{TITLE_EN}</h3></span>'
          '<span class="hp-guide-go" aria-hidden="true">›</span></a></li>')
    s = before_once(s, rf'<li data-until="[^"]+"><a class="hp-guide" href="{EN_DEC}">', li, f'hp-guide" href="{EN}"')
    s = before_once(s, rf'<a class="ltt-quick-btn" href="{EN_DEC}">',
                    f'<a class="ltt-quick-btn" href="{EN}">🍂 November</a>', f'ltt-quick-btn" href="{EN}"')
    if f'{SITE}{EN}"' not in s:
        items = list(re.finditer(r'"position": ?(\d+), ?"name": ?"[^"]*", ?"url": ?"[^"]*"\}', s))
        last = max(items, key=lambda m: int(m.group(1)))
        sp = " " if '"position": ' in last.group(0) else ""
        add = (f',{sp}{{"@type":{sp}"ListItem",{sp}"position":{sp}{int(last.group(1)) + 1},{sp}'
               f'"name":{sp}"{TITLE_EN}",{sp}"url":{sp}"{SITE}{EN}"}}')
        s = s[:last.end()] + add + s[last.end():]
    return s


def hu_home(s):
    return before_once(s, rf'<a class="ltt-quick-btn" href="{HU_DEC}">',
                       f'<a class="ltt-quick-btn" href="{HU}">🍂 Budapest novemberben</a> ', f'ltt-quick-btn" href="{HU}"')


# ---- sitemap ----
def sitemap(s):
    if f"<loc>{SITE}{EN}</loc>" in s:
        return s
    alts = (f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{EN}" />\n'
            f'    <xhtml:link rel="alternate" hreflang="hu" href="{SITE}{HU}" />\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{EN}" />\n')
    entry = "".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{ISO}</lastmod>\n    <changefreq>weekly</changefreq>\n"
                    f"    <priority>0.8</priority>\n{alts}  </url>\n" for u in (EN, HU))
    return s.replace("</urlset>", entry + "</urlset>")


# ---- in-body links ----
def link_once(rel, old, new):
    def fn(s):
        if new in s:
            return s
        assert s.count(old) >= 1, (rel, old)
        return s.replace(old, new, 1)
    edit(rel, fn)


edit("budapest-tourism-statistics.html", en_menu)
edit("hu/budapest-turizmus-statisztika/index.html", hu_menu)
edit("index.html", en_home)
edit("hu/index.html", hu_home)
edit("sitemap.xml", sitemap)

link_once("best-things-to-do-budapest.html",
          f'Visiting in winter? See <a href="{EN_DEC}">things to do in Budapest in December</a>.',
          f'Visiting in late autumn or winter? See things to do in Budapest in <a href="{EN}">November</a> and <a href="{EN_DEC}">December</a>.')
link_once("thermal-baths-budapest.html",
          f'Bath hours over Christmas are in our <a href="{EN_DEC}">December guide</a>.</p>',
          f'Bath hours over Christmas are in our <a href="{EN_DEC}">December guide</a>, and the best November evenings around the baths are in our <a href="{EN}">November guide</a>.</p>')
link_once("budapest-christmas-markets.html",
          "Advent Óbudán open on <strong>27 November</strong>.",
          f'Advent Óbudán open on <strong>27 November</strong>. Planning the rest of a November trip? See <a href="{EN}">things to do in Budapest in November</a>.')
link_once("hu/karacsonyi-vasar-budapest/index.html",
          "az Advent Óbudán <strong>november 27-én</strong> nyit.",
          f'az Advent Óbudán <strong>november 27-én</strong> nyit. A novemberi út többi részéhez: <a href="{HU}">Budapest novemberben</a>.')
# the HU December page pointed at the EN November page until the HU version existed
for rel in ("hu/budapest-programok-december/index.html", "scripts/december_copy_hu.py"):
    link_once(rel,
              'Korábban jössz? Nézd meg, <a href=\\"/things-to-do-budapest-november\\">mit csinálj Budapesten novemberben</a> (angolul).' if rel.endswith(".py")
              else 'Korábban jössz? Nézd meg, <a href="/things-to-do-budapest-november">mit csinálj Budapesten novemberben</a> (angolul).',
              'Korábban jössz? Nézd meg, <a href=\\"/hu/budapest-programok-november\\">mit csinálj Budapesten novemberben</a>.' if rel.endswith(".py")
              else f'Korábban jössz? Nézd meg, <a href="{HU}">mit csinálj Budapesten novemberben</a>.')
