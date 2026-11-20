#!/usr/bin/env python3
"""Wire the 2026-11-16 experiences batch (10 new EN "best X" pages) into the site.

- nav thumbnails (assets/nav-thumbs/<slug>.webp, 96x96) from each page's first card photo
- EN menu master: two new columns in the Tours mega menu + the same links in the mobile menu
- EN homepage: a new "Activities &amp; experiences" guide group + JSON-LD ItemList entries
- sitemap.xml: one <url> per page (EN + x-default)
- contextual links in from related live pages (a short "Related" block above their FAQ)

Idempotent. Afterwards run: python3 scripts/sync_layout.py

    python3 scripts/wire_experiences_batch.py
"""
import datetime as dt
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
TODAY = dt.date.today().isoformat()

# slug: (menu column, menu title, menu subtitle)
PAGES = {
    "best-buda-castle-tours": ("Sights &amp; History", "Best Buda Castle Tours", "Castle Hill walks, entries &amp; night tours"),
    "best-jewish-quarter-tours-budapest": ("Sights &amp; History", "Best Jewish Quarter Tours", "Dohány Synagogue entry &amp; heritage walks"),
    "best-communist-tours-budapest": ("Sights &amp; History", "Best Communist Tours", "Memento Park &amp; House of Terror compared"),
    "best-cave-tours-budapest": ("Sights &amp; History", "Best Cave Tours", "Caving, cave walks &amp; the castle labyrinth"),
    "best-concerts-budapest": ("Experiences", "Best Concerts &amp; Shows", "Organ concerts, opera &amp; folk shows"),
    "best-wine-tasting-budapest": ("Experiences", "Best Wine Tastings", "City tastings, wineries &amp; pálinka"),
    "best-cooking-classes-budapest": ("Experiences", "Best Cooking Classes", "Goulash classes &amp; chimney cake workshops"),
    "best-bike-tours-budapest": ("Experiences", "Best Bike &amp; E-Bike Tours", "Classic bikes, e-bikes &amp; Castle Hill climbs"),
    "best-helicopter-tours-budapest": ("Experiences", "Best Helicopter Tours", "Sightseeing flights priced per minute"),
    "best-shooting-ranges-budapest": ("Nightlife", "Best Shooting Ranges", "Gun packages compared per round"),
}

# related live page -> (heading, html paragraph)
RELATED = {
    "best-walking-tours-budapest": ("More guided ways to see Budapest",
        'Want one area in depth instead of a city overview? Compare the <a href="/best-buda-castle-tours">Buda Castle tours</a>, '
        'the <a href="/best-jewish-quarter-tours-budapest">Jewish Quarter tours with Dohány Synagogue entry</a> and the '
        '<a href="/best-communist-tours-budapest">communist history tours and Memento Park</a>. Rather ride than walk? See the '
        '<a href="/best-bike-tours-budapest">bike and e-bike tours</a> or the <a href="/best-segway-tours-budapest">Segway tours</a>.'),
    "best-food-tours-budapest": ("Cook it or taste the wine instead",
        'If you would rather make the food yourself, compare the <a href="/best-cooking-classes-budapest">Hungarian cooking classes '
        'and chimney cake workshops</a>. For Tokaji, Egri Bikavér and pálinka without the walking, see the '
        '<a href="/best-wine-tasting-budapest">best wine tastings in Budapest</a>.'),
    "best-pub-crawls-budapest": ("Planning a stag or hen weekend?",
        'Groups often pair a crawl with a daytime activity: compare the <a href="/best-shooting-ranges-budapest">shooting range '
        'packages</a> (price per round, indoor vs outdoor) or book a calmer evening with the '
        '<a href="/best-wine-tasting-budapest">wine tastings</a>.'),
    "best-day-trips-from-budapest": ("Staying in the city instead?",
        'Short on time for a full-day trip? The <a href="/best-wine-tasting-budapest">wine tastings in Budapest</a> include half-day '
        'countryside winery tours, and the <a href="/best-cave-tours-budapest">cave tours</a> take you underground without leaving '
        'the city. For the view from above, see the <a href="/best-helicopter-tours-budapest">helicopter tours</a>.'),
    "best-things-to-do-budapest": ("More Budapest experiences compared",
        'Every one of these has its own side-by-side comparison: <a href="/best-concerts-budapest">concerts and shows</a>, '
        '<a href="/best-buda-castle-tours">Buda Castle tours</a>, <a href="/best-jewish-quarter-tours-budapest">Jewish Quarter tours</a>, '
        '<a href="/best-cave-tours-budapest">cave tours</a>, <a href="/best-wine-tasting-budapest">wine tastings</a>, '
        '<a href="/best-cooking-classes-budapest">cooking classes</a>, <a href="/best-bike-tours-budapest">bike tours</a>, '
        '<a href="/best-shooting-ranges-budapest">shooting ranges</a> and <a href="/best-helicopter-tours-budapest">helicopter tours</a>.'),
    "sparty-budapest": ("Making a weekend of it?",
        'Stag and hen groups often add a daytime activity before Sparty: compare the <a href="/best-shooting-ranges-budapest">shooting '
        'range packages</a> by price per round, or see the city from above with a <a href="/best-helicopter-tours-budapest">helicopter '
        'or gyrocopter flight</a>.'),
    "budapest-travel-guide": ("Add one of these to your days",
        'Day 1 on Castle Hill works best with a <a href="/best-buda-castle-tours">guided Buda Castle tour</a>; an evening is easy to '
        'fill with an <a href="/best-concerts-budapest">organ concert or folk show</a>; and a free afternoon fits a '
        '<a href="/best-communist-tours-budapest">Memento Park visit</a> or a <a href="/best-cooking-classes-budapest">cooking class</a>.'),
}

MARK = "<!-- exp-batch1 -->"


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def write(p, s):
    (ROOT / p).write_text(s, encoding="utf-8")


def spec(slug):
    return json.loads(read(f"scripts/articles/{slug}.json"))


def first_photo(slug):
    return spec(slug)["items"][0]["photos"][0]


def thumbs():
    out = ROOT / "assets" / "nav-thumbs"
    for slug in PAGES:
        dst = out / f"{slug}.webp"
        if dst.exists():
            continue
        im = Image.open(ROOT / first_photo(slug).lstrip("/")).convert("RGB")
        w, h = im.size
        side = min(w, h)
        im = im.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2)).resize((96, 96), Image.LANCZOS)
        im.save(dst, "WEBP", quality=80)


def menu():
    cfg = json.loads(read("scripts/layout_config.json"))
    master = cfg["masters"]["en"]
    s = read(master)
    if MARK in s:
        return
    def item(slug, t, sub):
        return (f'<a class="ltt-mega-item" href="/{slug}"><img alt="" class="ltt-thumb" data-src="/assets/nav-thumbs/{slug}.webp" '
                f'decoding="async" height="48" width="48"/><div><strong>{t}</strong><p>{sub}</p></div></a>')
    cols = {}
    for slug, (col, t, sub) in PAGES.items():
        cols.setdefault(col, []).append(item(slug, t, sub))
    # Nightlife column gets its new item appended; two new columns go after it
    nl = s.index('<div class="ltt-mega-head">Nightlife</div>')
    # find the closing </div> of the Nightlife column by counting nested divs
    col_start = s.rindex('<div class="ltt-mega-col">', 0, nl)
    depth, i = 0, col_start
    while True:
        o = s.find("<div", i)
        c = s.find("</div>", i)
        if o != -1 and o < c:
            depth += 1
            i = o + 4
        else:
            depth -= 1
            i = c + 6
            if depth == 0:
                break
    col_close = i - 6
    new_cols = "".join(
        f'<div class="ltt-mega-col">{MARK}<div class="ltt-mega-head">{name}</div>' + "".join(cols[name]) + "</div>"
        for name in ("Sights &amp; History", "Experiences"))
    s = s[:col_close] + "".join(cols["Nightlife"]) + s[col_close:col_close + 6] + new_cols + s[col_close + 6:]

    # mobile: after the pub crawls link
    mob = s.index('<a class="ltt-mobile-link" href="/best-pub-crawls-budapest">')
    mob_end = s.index("</a>", mob) + 4
    links = "".join(
        f'<a class="ltt-mobile-link" href="/{slug}"><span class="ltt-mobile-link-main"><img alt="" class="ltt-thumb" '
        f'data-src="/assets/nav-thumbs/{slug}.webp" decoding="async" height="36" width="36"/><span>{t}</span></span></a>'
        for slug, (_, t, _) in PAGES.items())
    s = s[:mob_end] + links + s[mob_end:]
    write(master, s)


def homepage():
    s = read("index.html")
    if 'hp-guides-gh">Activities &amp; experiences<' in s:
        return
    lis = []
    for slug in PAGES:
        sp = spec(slug)
        alt = sp["items"][0]["title"].replace('"', "&quot;")
        lis.append(f'<li><a class="hp-guide" href="/{slug}"><img alt="{alt}" decoding="async" height="84" loading="lazy" '
                   f'src="{first_photo(slug)}" width="84"/><span class="hp-guide-txt"><h3>{sp["h1"]}</h3></span>'
                   f'<span aria-hidden="true" class="hp-guide-go">›</span></a></li>')
    group = (f'{MARK}<div class="hp-guides-group"><div class="hp-guides-gh">Activities &amp; experiences</div>'
             f'<ul class="hp-guides">{"".join(lis)}</ul></div>')
    anchor = s.index('<div class="hp-guides-group"><div class="hp-guides-gh">Plan your trip</div>')
    s = s[:anchor] + group + s[anchor:]
    # JSON-LD ItemList
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            ld = json.loads(m.group(1))
        except Exception:
            continue
        changed = False
        for node in ld.get("@graph", []):
            if node.get("@type") == "ItemList":
                el = node["itemListElement"]
                have = {e.get("url") for e in el}
                for slug in PAGES:
                    u = f"{SITE}/{slug}"
                    if u not in have:
                        el.append({"@type": "ListItem", "position": len(el) + 1, "name": spec(slug)["h1"], "url": u})
                        changed = True
                node["numberOfItems"] = len(el)
        if changed:
            s = s[:m.start(1)] + json.dumps(ld, ensure_ascii=False) + s[m.end(1):]
            break
    write("index.html", s)


def sitemap():
    s = read("sitemap.xml")
    add = []
    for slug in PAGES:
        u = f"{SITE}/{slug}"
        if f"<loc>{u}</loc>" in s:
            continue
        add.append(f"""  <url>
    <loc>{u}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{u}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{u}" />
  </url>
""")
    if add:
        i = s.rindex("</urlset>")
        s = s[:i] + "".join(add) + s[i:]
        write("sitemap.xml", s)
    # index.html lastmod
    s = read("sitemap.xml")
    s = re.sub(r"(<loc>https://www\.budapestadventures\.com/</loc>\s*<lastmod>)[^<]+", r"\g<1>" + TODAY, s, count=1)
    for page in RELATED:
        s = re.sub(rf"(<loc>{re.escape(SITE)}/{re.escape(page)}</loc>\s*<lastmod>)[^<]+", r"\g<1>" + TODAY, s, count=1)
    write("sitemap.xml", s)


def related():
    for page, (h, p) in RELATED.items():
        f = f"{page}.html"
        s = read(f)
        s = re.sub(re.escape(MARK) + r'<div class="w-richtext bpa-wt-guide"><h2 id="related-experiences">.*?</div>\n', "", s, flags=re.S)
        block = f'{MARK}<div class="w-richtext bpa-wt-guide"><h2 id="related-experiences">{h}</h2><p>{p}</p></div>\n'
        if '<div class="w-richtext bpa-wt-faq">' in s:
            i = s.index('<div class="w-richtext bpa-wt-faq">')
        else:
            i = s.rindex("<h2", 0, s.index('id="faq"'))
        s = s[:i] + block + s[i:]
        write(f, s)


if __name__ == "__main__":
    missing = [s for s in PAGES if not (ROOT / f"{s}.html").exists()]
    if missing:
        raise SystemExit(f"pages not built yet: {missing}")
    thumbs()
    menu()
    homepage()
    sitemap()
    related()
    print("wired", len(PAGES), "pages; now run scripts/sync_layout.py")
