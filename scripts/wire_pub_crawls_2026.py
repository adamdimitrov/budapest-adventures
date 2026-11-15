#!/usr/bin/env python3
"""Wire /best-pub-crawls-budapest into the site (EN only), 2026-11-15.

Menu (EN master, after Best Food Tours), homepage (guide list, quick button,
ItemList JSON-LD), sitemap entry + lastmod of every touched page, and
contextual in-body links from related pages. Idempotent: every edit is skipped
when the page already links to the article at that spot.
Run python3 scripts/sync_layout.py afterwards.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
URL = "/best-pub-crawls-budapest"
TODAY = "2026-11-15"
LINK = f'<a href="{URL}">'

# (file, old, new): old must occur exactly once
EDITS = [
    ("budapest-tourism-statistics.html",
     '<a class="ltt-mega-item" href="/best-food-tours-budapest">\n<div>\n<strong>Best Food Tours</strong>\n<p>Market halls, Jewish Quarter &amp; cooking classes</p>\n</div>\n</a>\n',
     '<a class="ltt-mega-item" href="/best-food-tours-budapest">\n<div>\n<strong>Best Food Tours</strong>\n<p>Market halls, Jewish Quarter &amp; cooking classes</p>\n</div>\n</a>\n'
     f'<a class="ltt-mega-item" href="{URL}">\n<div>\n<strong>Best Pub Crawls</strong>\n<p>Ruin bar crawls from €2 to €25 compared</p>\n</div>\n</a>\n'),
    ("budapest-tourism-statistics.html",
     '<a class="ltt-mobile-link" href="/best-food-tours-budapest">\n<span>Best Food Tours</span>\n</a>\n',
     '<a class="ltt-mobile-link" href="/best-food-tours-budapest">\n<span>Best Food Tours</span>\n</a>\n'
     f'<a class="ltt-mobile-link" href="{URL}">\n<span>Best Pub Crawls</span>\n</a>\n'),
    ("index.html",
     '<a class="ltt-quick-btn" href="/best-food-tours-budapest">🍲 Food Tours</a>',
     f'<a class="ltt-quick-btn" href="/best-food-tours-budapest">🍲 Food Tours</a> <a class="ltt-quick-btn" href="{URL}">🍻 Pub Crawls</a>'),
    ("index.html",
     '<h3>9 Best Food Tours in Budapest (Prices Compared)</h3></span><span class="hp-guide-go" aria-hidden="true">›</span></a></li>',
     '<h3>9 Best Food Tours in Budapest (Prices Compared)</h3></span><span class="hp-guide-go" aria-hidden="true">›</span></a></li>'
     f'<li><a class="hp-guide" href="{URL}"><img alt="Pub crawl group in a vaulted Budapest ruin bar cellar" loading="lazy" decoding="async" '
     'src="/assets/pub-crawls-2026/ruinbarcrawl-01.webp" width="84" height="84"/><span class="hp-guide-txt"><h3>6 Best Pub Crawls in Budapest (From €2)</h3></span>'
     '<span class="hp-guide-go" aria-hidden="true">›</span></a></li>'),
    # things to do: Szimpla card + section
    ("best-things-to-do-budapest.html",
     '<a class="bpa-title" href="/best-walking-tours-budapest">8. Szimpla Kert</a>',
     f'<a class="bpa-title" href="{URL}">8. Szimpla Kert</a>'),
    ("best-things-to-do-budapest.html",
     '<a class="bpa-sublink" href="/best-walking-tours-budapest">Jewish Quarter walking tours →</a>',
     f'<a class="bpa-sublink" href="{URL}">Best pub crawls compared →</a>'),
    ("best-things-to-do-budapest.html",
     "<p>It’s definitely a must-visit if you want to see the unique side of Budapest.<br/></p>",
     "<p>It’s definitely a must-visit if you want to see the unique side of Budapest.<br/></p>"
     f"<p>Want a group to go out with? Our {LINK}best pub crawls in Budapest</a> compares the €2 ruin bar crawls with a €25 crawl that includes 5 drinks, "
     "with start times and which bars each one visits. Hungry first? The <a href=\"/best-food-tours-budapest\">Jewish Quarter food tour</a> ends a few doors down on Kazinczy utca.</p>"),
    ("best-things-to-do-budapest.html",
     'or a drink in a ruin bar such as Szimpla Kert. See our <a href="/best-night-cruises-budapest">',
     f'or a drink in a ruin bar such as Szimpla Kert (or join a {LINK}ruin bar pub crawl</a>). See our <a href="/best-night-cruises-budapest">'),
    # hostels
    ("best-hostels-budapest.html",
     "<p>The ruin bars, Gozsdu Udvar and Szimpla Kert are here,",
     f"<p>The {LINK}ruin bars</a>, Gozsdu Udvar and Szimpla Kert are here,"),
    ("best-hostels-budapest.html",
     "<p>The party usually <strong>winds down around 11 PM to midnight</strong>, then the crowd heads out to the ruin bars.</p>",
     "<p>The party usually <strong>winds down around 11 PM to midnight</strong>, then the crowd heads out to the ruin bars, "
     f"often on one of the {LINK}Budapest pub crawls</a> that start between 21:00 and 22:20.</p>"),
    # cruises: the prosecco loop is sold as a warm-up before a night out
    ("best-night-cruises-budapest.html",
     "party songs from loudspeakers, pitched as a warm-up before a night out.</p>",
     "party songs from loudspeakers, pitched as a warm-up before a night out. If that night out is in the ruin bars, "
     f"our {LINK}best pub crawls in Budapest</a> compares the District VII crawls that start around 21:00.</p>"),
    ("best-budapest-river-cruises.html",
     "party songs from loudspeakers, pitched as a warm-up before a night out.</p>",
     "party songs from loudspeakers, pitched as a warm-up before a night out. If that night out is in the ruin bars, "
     f"our {LINK}best pub crawls in Budapest</a> compares the District VII crawls that start around 21:00.</p>"),
    ("unlimited-prosecco-cruises-budapest.html",
     "Parliament and Margaret Bridge, ideal before dinner or a night out.</div>",
     f"Parliament and Margaret Bridge, ideal before dinner or a {LINK}ruin bar pub crawl</a>.</div>"),
    # food + walking tours: Jewish Quarter is the ruin bar district
    ("best-food-tours-budapest.html",
     "the old Jewish neighbourhood that is now the ruin bar district: more of a sit-down meal and drinks, better in the late afternoon or evening.</p>",
     f"the old Jewish neighbourhood that is now the {LINK}ruin bar district</a>: more of a sit-down meal and drinks, better in the late afternoon or evening.</p>"),
    ("best-walking-tours-budapest.html",
     "Budapest's old Jewish Quarter and today its busiest nightlife street, and feeds you",
     f"Budapest's old Jewish Quarter and today its {LINK}busiest nightlife district</a>, and feeds you"),
    # private boats: stag and hen boat
    ("best-private-boat-tours-budapest.html",
     "and it leaves from the same Dock 42 as the Portum private boat.</p>",
     "and it leaves from the same Dock 42 as the Portum private boat. Most groups carry on in the ruin bars afterwards: "
     f"our {LINK}best pub crawls in Budapest</a> include a private stag crawl with pickup for 8 or more.</p>"),
    # travel guide hub
    ("budapest-travel-guide.html",
     '<a class="bpa-hub-card" href="/best-walking-tours-budapest">',
     f'<a class="bpa-hub-card" href="{URL}"><span class="bpa-hub-title">6 Best Pub Crawls</span><span class="bpa-hub-desc">Ruin bar crawls from €2, a €25 cocktail crawl and private stag nights.</span><span class="bpa-hub-more">Read guide →</span></a>'
     '<a class="bpa-hub-card" href="/best-walking-tours-budapest">'),
]


def add_itemlist(s):
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    data = json.loads(m.group(2))
    for node in data["@graph"]:
        if node.get("@type") == "ItemList":
            items = node["itemListElement"]
            if any(i.get("url") == SITE + URL for i in items):
                return s
            items.append({"@type": "ListItem", "position": len(items) + 1,
                          "name": "6 Best Pub Crawls in Budapest (From €2)", "url": SITE + URL})
            if "numberOfItems" in node:
                node["numberOfItems"] = len(items)
    return s[:m.start(2)] + json.dumps(data, ensure_ascii=False) + s[m.end(2):]


def page_url(f):
    p = f[:-len("/index.html")] if f.endswith("/index.html") else f[:-5]
    return SITE + "/" + ("" if p == "index" else p)


def main():
    touched = set()
    for f, old, new in EDITS:
        path = ROOT / f
        s = path.read_text()
        if new in s:
            continue
        assert s.count(old) == 1, (f, old[:70], s.count(old))
        path.write_text(s.replace(old, new))
        touched.add(f)
    idx = ROOT / "index.html"
    s = idx.read_text()
    s2 = add_itemlist(s)
    if s2 != s:
        idx.write_text(s2)
        touched.add("index.html")

    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    if f"<loc>{SITE}{URL}</loc>" not in s:
        anchor = f"<loc>{SITE}/best-food-tours-budapest</loc>"
        i = s.find(anchor)
        j = s.find("</url>", i) + len("</url>")
        s = s[:j] + f"""
  <url>
    <loc>{SITE}{URL}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{URL}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{URL}" />
  </url>""" + s[j:]
    for f in sorted(touched | {"best-pub-crawls-budapest.html"}):
        loc = page_url(f)
        s, n = re.subn(rf"(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]*(</lastmod>)", rf"\g<1>{TODAY}\2", s)
        print(("lastmod " if n else "NO SITEMAP ENTRY ") + loc)
    sm.write_text(s)


if __name__ == "__main__":
    main()
