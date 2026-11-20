#!/usr/bin/env python3
"""Wire the 2026-11-20 hotel batch (7 EN hotel comparison pages) into the site.

- nav thumbnails from each page's first card photo (wire_experiences_batch.thumbs)
- EN menu master: a new "Where to Stay" column in the Plan Your Trip mega menu, and the same links
  in the mobile drawer after "Best Hostels in Budapest"
- EN homepage: the pages in the "Plan your trip" guide group + JSON-LD ItemList
- sitemap.xml entries
- a short related block (contextual links) on related live pages

Idempotent. Afterwards run: python3 scripts/sync_layout.py
"""
import html as w1_html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_experiences_batch as w1  # noqa: E402

ROOT = w1.ROOT
# slug: (menu title, menu subtitle)
PAGES = {
    "where-to-stay-in-budapest": ("Where to Stay in Budapest", "6 areas compared, 2 hotels in each"),
    "best-hotels-budapest": ("Best Hotels in Budapest", "3 to 5 stars, every budget"),
    "best-luxury-hotels-budapest": ("Best Luxury Hotels", "5-star pools, spas &amp; views"),
    "best-boutique-hotels-budapest": ("Best Boutique Hotels", "Small hotels rated 9+ from €73"),
    "best-spa-hotels-budapest": ("Best Spa &amp; Thermal Hotels", "Thermal pools &amp; rooftop pools"),
    "best-cheap-hotels-budapest": ("Best Cheap Hotels", "Rooms for two under €65"),
    "best-airport-hotels-budapest": ("Best Airport Hotels", "Terminal 2, shuttles &amp; parking"),
}
WHERE = '<a href="/where-to-stay-in-budapest">where to stay in Budapest</a>'
RELATED = {
    "best-hostels-budapest": ("Prefer a private hotel room?",
        'Two people often pay little more for a hotel room than for two dorm beds: compare the '
        '<a href="/best-cheap-hotels-budapest">cheap hotels in Budapest</a> (under €65 for two), or see ' + WHERE + ' for every area.'),
    "budapest-airport-to-city-center": ("Landing late or flying early?",
        'Compare the <a href="/best-airport-hotels-budapest">Budapest airport hotels</a>: two are at Terminal 2, others run a shuttle. '
        'Heading into town? See ' + WHERE + '.'),
    "budapest-travel-guide": ("Where to base yourself for these 3 days",
        'This plan works best from District V or VI; compare the areas in ' + WHERE + ', or go straight to the '
        '<a href="/best-hotels-budapest">best hotels in Budapest</a>.'),
    "thermal-baths-budapest": ("Want the thermal water in your hotel?",
        'Two hotels on Margaret Island have thermal pools free for guests: compare the '
        '<a href="/best-spa-hotels-budapest">spa and thermal hotels in Budapest</a>.'),
    "best-things-to-do-budapest": ("Still choosing a hotel?",
        'See ' + WHERE + ' for the six best areas, then compare the <a href="/best-luxury-hotels-budapest">luxury hotels</a>, '
        '<a href="/best-boutique-hotels-budapest">boutique hotels</a> and <a href="/best-cheap-hotels-budapest">cheap hotels</a>.'),
}
MARK = "<!-- hotels-batch -->"


def menu():
    cfg = w1.json.loads(w1.read("scripts/layout_config.json"))
    master = cfg["masters"]["en"]
    s = w1.read(master)
    if 'class="ltt-mega-head">Where to Stay<' not in s:
        items = "".join(
            f'<a class="ltt-mega-item" href="/{slug}"><img alt="" class="ltt-thumb" data-src="/assets/nav-thumbs/{slug}.webp" '
            f'decoding="async" height="48" width="48"/><div><strong>{t}</strong><p>{sub}</p></div></a>\n'
            for slug, (t, sub) in PAGES.items())
        col = f'<div class="ltt-mega-col">\n<div class="ltt-mega-head">Where to Stay</div>\n{items}</div>\n'
        m = re.search(r'<a class="ltt-mega-item" href="/best-hostels-budapest">.*?</a>\n</div>\n', s, re.S)
        s = s[:m.end()] + col + s[m.end():]
    if 'class="ltt-mobile-link" href="/where-to-stay-in-budapest"' not in s:
        mob = "".join(
            f'\n<a class="ltt-mobile-link" href="/{slug}"><span class="ltt-mobile-link-main"><img alt="" class="ltt-thumb" '
            f'data-src="/assets/nav-thumbs/{slug}.webp" decoding="async" height="36" width="36"/><span>{t}</span></span></a>'
            for slug, (t, _) in PAGES.items())
        m = re.search(r'<a class="ltt-mobile-link" href="/best-hostels-budapest">.*?</a>', s, re.S)
        s = s[:m.end()] + mob + s[m.end():]
    w1.write(master, s)


def homepage():
    s = w1.read("index.html")
    g = s.index('hp-guides-gh">Plan your trip<')
    end = s.index("</ul></div>", g)
    add = ""
    for slug in PAGES:
        if f'class="hp-guide" href="/{slug}"' in s:
            continue
        sp = w1.spec(slug)
        alt = w1_html.escape(sp["items"][0]["title"], quote=True)
        add += (f'<li><a class="hp-guide" href="/{slug}"><img alt="{alt}" decoding="async" height="84" loading="lazy" '
                f'src="{w1.first_photo(slug)}" width="84"/><span class="hp-guide-txt"><h3>{sp["h1"]}</h3></span>'
                f'<span aria-hidden="true" class="hp-guide-go">›</span></a></li>')
    s = s[:end] + add + s[end:]
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            ld = w1.json.loads(m.group(1))
        except Exception:
            continue
        changed = False
        for node in ld.get("@graph", []):
            if node.get("@type") == "ItemList":
                el = node["itemListElement"]
                have = {e.get("url") for e in el}
                for slug in PAGES:
                    u = f"{w1.SITE}/{slug}"
                    if u not in have:
                        el.append({"@type": "ListItem", "position": len(el) + 1, "name": w1.spec(slug)["h1"], "url": u})
                        changed = True
                node["numberOfItems"] = len(el)
        if changed:
            s = s[:m.start(1)] + w1.json.dumps(ld, ensure_ascii=False) + s[m.end(1):]
            break
    w1.write("index.html", s)


def related():
    for page, (h, p) in RELATED.items():
        f = f"{page}.html"
        s = w1.read(f)
        s = re.sub(re.escape(MARK) + r'<div class="w-richtext bpa-wt-guide"><h2 id="related-hotels">.*?</div>\n', "", s, flags=re.S)
        block = f'{MARK}<div class="w-richtext bpa-wt-guide"><h2 id="related-hotels">{h}</h2><p>{p}</p></div>\n'
        if '<div class="w-richtext bpa-wt-faq">' in s:
            i = s.index('<div class="w-richtext bpa-wt-faq">')
        else:
            i = s.rindex("<h2", 0, s.index('id="faq"'))
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
    homepage()
    related()
    print("wired", len(PAGES), "pages; now run scripts/sync_layout.py")
