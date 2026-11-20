#!/usr/bin/env python3
"""Wire the 2026-11-20 hotel gap pages (7 EN hotel comparison pages from backlog/bpa-budapest-hotels.csv).

- nav thumbnails from each page's first card photo
- EN menu master: added to the "Where to Stay" column of the Plan Your Trip mega menu, and to the
  mobile drawer after "Best Airport Hotels"
- EN homepage: "Plan your trip" guide group + JSON-LD ItemList
- sitemap.xml entries
- a short related block (contextual links) on related live pages

Idempotent. Afterwards run: python3 scripts/sync_layout.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_experiences_batch as w1  # noqa: E402
import wire_hotels_batch as w2  # noqa: E402

ROOT = w1.ROOT
PAGES = {
    "best-4-star-hotels-budapest": ("Best 4-Star Hotels", "All rated 9+, from €74"),
    "best-castle-district-hotels-budapest": ("Castle District Hotels", "Inside the walls or below the hill"),
    "best-danube-view-hotels-budapest": ("Danube View Hotels", "Priced for a river-view room"),
    "best-aparthotels-budapest": ("Best Aparthotels", "Kitchens, pools, from €76"),
    "best-family-hotels-budapest": ("Best Family Hotels", "Priced for 2 adults + 2 kids"),
    "best-romantic-hotels-budapest": ("Romantic Hotels", "Adults only, rooftop pools"),
    "hotels-near-keleti-station-budapest": ("Hotels Near Keleti Station", "From 164 ft, from €59"),
}
L = lambda slug, txt: f'<a href="/{slug}">{txt}</a>'
RELATED = {
    "where-to-stay-in-budapest": ("More ways to pick a hotel",
        "Narrow it down by what matters to you: the " + L("best-4-star-hotels-budapest", "best 4-star hotels") + ", "
        + L("best-castle-district-hotels-budapest", "Castle District hotels") + ", "
        + L("best-danube-view-hotels-budapest", "Danube view hotels") + ", "
        + L("best-aparthotels-budapest", "aparthotels with a kitchen") + ", "
        + L("best-family-hotels-budapest", "family hotels") + ", "
        + L("best-romantic-hotels-budapest", "romantic adults-only hotels") + " and "
        + L("hotels-near-keleti-station-budapest", "hotels near Keleti station") + "."),
    "best-luxury-hotels-budapest": ("Happy with 4 stars?",
        "Budapest's best 4-star hotels score 9 or higher from €74 a night: compare the "
        + L("best-4-star-hotels-budapest", "best 4-star hotels in Budapest") + ", or pick a room facing the river from the "
        + L("best-danube-view-hotels-budapest", "Danube view hotels") + "."),
    "best-hotels-budapest": ("Looking for something specific?",
        "Compare the " + L("best-4-star-hotels-budapest", "best 4-star hotels") + ", the "
        + L("best-castle-district-hotels-budapest", "Castle District hotels") + " or the "
        + L("best-romantic-hotels-budapest", "romantic adults-only hotels") + "."),
    "best-things-to-do-budapest-with-kids": ("Where to stay with kids",
        "We priced hotels for 2 adults and 2 children: see the " + L("best-family-hotels-budapest", "best family hotels in Budapest")
        + ", or the " + L("best-aparthotels-budapest", "aparthotels") + " if you want a kitchen."),
    "best-buda-castle-tours": ("Sleep on Castle Hill",
        "Stay after the crowds leave: compare the " + L("best-castle-district-hotels-budapest", "Castle District hotels") + ", inside the walls or just below the hill."),
    "best-airport-hotels-budapest": ("Arriving by train instead?",
        "See the " + L("hotels-near-keleti-station-budapest", "hotels near Keleti station") + ", the closest 164 ft from the platforms."),
    "best-cheap-hotels-budapest": ("Need a kitchen or a station hotel?",
        "Compare the " + L("best-aparthotels-budapest", "aparthotels in Budapest") + " (from €76 with a kitchen) or the "
        + L("hotels-near-keleti-station-budapest", "hotels near Keleti station") + " (from €59)."),
}
MARK = "<!-- hotels-batch3 -->"


def menu():
    cfg = w1.json.loads(w1.read("scripts/layout_config.json"))
    master = cfg["masters"]["en"]
    s = w1.read(master)
    for slug, (t, sub) in PAGES.items():
        if f'class="ltt-mega-item" href="/{slug}"' in s:
            continue
        item = (f'<a class="ltt-mega-item" href="/{slug}"><img alt="" class="ltt-thumb" data-src="/assets/nav-thumbs/{slug}.webp" '
                f'decoding="async" height="48" width="48"/><div><strong>{t}</strong><p>{sub}</p></div></a>\n')
        m = re.search(r'<a class="ltt-mega-item" href="/best-airport-hotels-budapest">.*?</a>\n', s, re.S)
        last = m.end()
        for slug2 in PAGES:
            m2 = re.search(r'<a class="ltt-mega-item" href="/' + re.escape(slug2) + r'">.*?</a>\n', s, re.S)
            if m2 and m2.end() > last:
                last = m2.end()
        s = s[:last] + item + s[last:]
    for slug, (t, _) in PAGES.items():
        if f'class="ltt-mobile-link" href="/{slug}"' in s:
            continue
        mob = (f'\n<a class="ltt-mobile-link" href="/{slug}"><span class="ltt-mobile-link-main"><img alt="" class="ltt-thumb" '
               f'data-src="/assets/nav-thumbs/{slug}.webp" decoding="async" height="36" width="36"/><span>{t}</span></span></a>')
        last = re.search(r'<a class="ltt-mobile-link" href="/best-airport-hotels-budapest">.*?</a>', s, re.S).end()
        for slug2 in PAGES:
            m2 = re.search(r'<a class="ltt-mobile-link" href="/' + re.escape(slug2) + r'">.*?</a>', s, re.S)
            if m2 and m2.end() > last:
                last = m2.end()
        s = s[:last] + mob + s[last:]
    w1.write(master, s)


def related():
    for page, (h, p) in RELATED.items():
        f = f"{page}.html"
        s = w1.read(f)
        s = re.sub(re.escape(MARK) + r'<div class="w-richtext bpa-wt-guide"><h2 id="related-hotels-3">.*?</div>\n', "", s, flags=re.S)
        block = f'{MARK}<div class="w-richtext bpa-wt-guide"><h2 id="related-hotels-3">{h}</h2><p>{p}</p></div>\n'
        if '<div class="w-richtext bpa-wt-faq">' in s:
            i = s.index('<div class="w-richtext bpa-wt-faq">')
        elif 'id="faq"' in s:
            i = s.rindex("<h2", 0, s.index('id="faq"'))
        else:
            i = s.index('<div class="w-richtext bpa-wt-guide">')
        s = s[:i] + block + s[i:]
        w1.write(f, s)


if __name__ == "__main__":
    missing = [p for p in PAGES if not (ROOT / f"{p}.html").exists()]
    if missing:
        raise SystemExit(f"pages not built yet: {missing}")
    w1.PAGES = {k: ("", v[0], v[1]) for k, v in PAGES.items()}
    w1.RELATED = RELATED
    w1.thumbs()
    w1.sitemap()
    menu()
    w2.PAGES = PAGES
    w2.homepage()
    related()
    print("wired", len(PAGES), "pages; now run scripts/sync_layout.py")
