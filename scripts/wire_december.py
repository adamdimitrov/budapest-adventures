#!/usr/bin/env python3
"""Wire the December page (EN + HU) into the site: menus (on the layout masters),
homepages, sitemap and in-body links. Idempotent. Run sync_layout.py afterwards."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
EN, HU = "/things-to-do-budapest-december", "/hu/budapest-programok-december"
ISO = "2026-11-15"


def edit(rel, fn):
    p = ROOT / rel
    s = p.read_text()
    new = fn(s)
    if new != s:
        p.write_text(new)
        print("edited", rel)


def after_once(s, marker_re, block, guard):
    if guard in s:
        return s
    m = re.search(marker_re, s, re.S)
    assert m, marker_re
    return s[:m.end()] + block + s[m.end():]


# ---- menus on the layout masters ----
def en_menu(s):
    s = after_once(s, r'<a class="ltt-mega-item" href="/best-day-trips-from-budapest">.*?</a>\n',
                   f'<a class="ltt-mega-item" href="{EN}">\n<div>\n<strong>Budapest in December</strong>\n'
                   '<p>Christmas cruises, baths &amp; holiday hours</p>\n</div>\n</a>\n', f'ltt-mega-item" href="{EN}"')
    s = after_once(s, r'<a class="ltt-mobile-link" href="/best-day-trips-from-budapest">.*?</a>\n',
                   f'<a class="ltt-mobile-link" href="{EN}">\n<span>Budapest in December</span>\n</a>\n', f'ltt-mobile-link" href="{EN}"')
    return s


def hu_menu(s):
    s = after_once(s, r'<a class="ltt-mega-item" href="/hu/legjobb-gyalogtúrák-budapest">.*?</a>\n',
                   f'<a class="ltt-mega-item" href="{HU}">\n<div>\n<strong>Budapest decemberben</strong>\n'
                   '<p>Karácsonyi hajók, fürdők, ünnepi nyitvatartás</p>\n</div>\n</a>\n', f'ltt-mega-item" href="{HU}"')
    s = after_once(s, r'<a class="ltt-mobile-link" href="/hu/legjobb-gyalogtúrák-budapest">.*?</a>\n',
                   f'<a class="ltt-mobile-link" href="{HU}">\n<span>Budapest decemberben</span>\n</a>\n', f'ltt-mobile-link" href="{HU}"')
    return s


# ---- homepages ----
def en_home(s):
    li = (f'<li data-until="2027-01-01T00:00:00+01:00"><a class="hp-guide" href="{EN}"><img alt="Christmas dinner cruise table on the Danube in Budapest" '
          'loading="lazy" decoding="async" src="/assets/xmas-2026/budapest-christmas-cruise-silverline-01.avif" width="64" height="64"/>'
          '<span class="hp-guide-txt"><h3>11 Best Things to Do in Budapest in December 2026</h3></span>'
          '<span class="hp-guide-go" aria-hidden="true">›</span></a></li>')
    s = after_once(s, r'<li data-until="[^"]+"><a class="hp-guide" href="/budapest-christmas-markets">.*?</li>', li, f'hp-guide" href="{EN}"')
    s = after_once(s, r'<a class="ltt-quick-btn" href="/thermal-baths-budapest">[^<]*</a>\n?',
                   f'<a class="ltt-quick-btn" href="{EN}">🎄 December</a>\n', f'ltt-quick-btn" href="{EN}"')
    if f'{SITE}{EN}"' not in s:
        s = s.replace('"url":"https://www.budapestadventures.com/best-day-trips-from-budapest"}]',
                      '"url":"https://www.budapestadventures.com/best-day-trips-from-budapest"},{"@type":"ListItem","position":12,'
                      '"name":"11 Best Things to Do in Budapest in December 2026","url":"' + SITE + EN + '"}]', 1)
    return s


def hu_home(s):
    return after_once(s, r'<a class="ltt-quick-btn" href="/hu/karacsonyi-vasar-budapest">[^<]*</a>',
                      f' <a class="ltt-quick-btn" href="{HU}">⛄ Budapest decemberben</a>', f'ltt-quick-btn" href="{HU}"')


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

link_once("budapest-tourism-statistics.html",
          "<strong>December</strong> is the second busiest month",
          f'<strong><a href="{EN}">December</a></strong> is the second busiest month')
link_once("best-things-to-do-budapest.html",
          "On 31 December, book a <a href=\"/new-years-eve-cruises-budapest\">New Year's Eve cruise</a> early",
          f"Visiting in winter? See <a href=\"{EN}\">things to do in Budapest in December</a>. On 31 December, book a <a href=\"/new-years-eve-cruises-budapest\">New Year's Eve cruise</a> early")
link_once("christmas-cruises-budapest.html",
          "Below them you'll find <a href=\"#also-sailing\">the regular boats that keep sailing over Christmas</a>.",
          f"Below them you'll find <a href=\"#also-sailing\">the regular boats that keep sailing over Christmas</a>. For the rest of the month (baths, markets, the Nutcracker and holiday opening hours), see <a href=\"{EN}\">things to do in Budapest in December</a>.")
link_once("new-years-eve-cruises-budapest.html",
          "Arriving earlier? See my <a href=\"/christmas-cruises-budapest\">Christmas cruise comparison</a>.",
          f"Arriving earlier? See my <a href=\"/christmas-cruises-budapest\">Christmas cruise comparison</a> and <a href=\"{EN}\">things to do in Budapest in December</a>.")
link_once("thermal-baths-budapest.html",
          "Palatinus is a summer strand: in winter it closes at 16:00.</p>",
          f"Palatinus is a summer strand: in winter it closes at 16:00. Bath hours over Christmas are in our <a href=\"{EN}\">December guide</a>.</p>")
