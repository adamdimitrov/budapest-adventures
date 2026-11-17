#!/usr/bin/env python3
"""Wire the 2 follow-up pages of the experiences batch (kids, Vienna day trips), 2026-11-17.

Same approach as scripts/wire_experiences_batch.py: nav thumbs, EN menu master items
(Vienna under Guided Tours after Day Trips, kids under Experiences), homepage
"Activities & experiences" group, sitemap, and related links in from live pages.
Idempotent. Afterwards run: python3 scripts/sync_layout.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_experiences_batch as w1  # noqa: E402

ROOT = w1.ROOT
PAGES = {
    "best-vienna-day-trips-from-budapest": ("/best-day-trips-from-budapest", "Vienna Day Trips", "Shared coach vs private driver compared"),
    "best-things-to-do-budapest-with-kids": ("/best-cooking-classes-budapest", "Budapest with Kids", "Family tickets, rainy-day picks &amp; tours"),
}
RELATED = {
    "best-day-trips-from-budapest": ("Only interested in Vienna?",
        'Vienna has its own comparison: shared coach trips with Bratislava against private driver days, with the price per '
        'person for 2 to 4 travellers. See the <a href="/best-vienna-day-trips-from-budapest">best Vienna day trips from Budapest</a>.'),
    "best-things-to-do-budapest": ("Travelling with children?",
        'For museums, the Budapest Eye, the Pinball Museum and family walking tours compared on age fit and price, see '
        '<a href="/best-things-to-do-budapest-with-kids">things to do in Budapest with kids</a>.'),
    "budapest-travel-guide": ("Planning the days with kids or a Vienna side trip?",
        'Swap in a rainy-day pick from <a href="/best-things-to-do-budapest-with-kids">Budapest with kids</a>, or use a spare day for '
        'one of the <a href="/best-vienna-day-trips-from-budapest">Vienna day trips from Budapest</a>.'),
}
MARK = "<!-- exp-batch2 -->"


def menu():
    cfg = w1.json.loads(w1.read("scripts/layout_config.json"))
    master = cfg["masters"]["en"]
    s = w1.read(master)
    for slug, (after, t, sub) in PAGES.items():
        if f'class="ltt-mega-item" href="/{slug}"' in s:
            continue
        mega = (f'<a class="ltt-mega-item" href="/{slug}"><img alt="" class="ltt-thumb" data-src="/assets/nav-thumbs/{slug}.webp" '
                f'decoding="async" height="48" width="48"/><div><strong>{t}</strong><p>{sub}</p></div></a>')
        m = re.search(rf'<a class="ltt-mega-item" href="{re.escape(after)}">.*?</a>', s, re.S)
        s = s[:m.end()] + mega + s[m.end():]
        mob = (f'<a class="ltt-mobile-link" href="/{slug}"><span class="ltt-mobile-link-main"><img alt="" class="ltt-thumb" '
               f'data-src="/assets/nav-thumbs/{slug}.webp" decoding="async" height="36" width="36"/><span>{t}</span></span></a>')
        m = re.search(rf'<a class="ltt-mobile-link" href="{re.escape(after)}">.*?</a>', s, re.S)
        s = s[:m.end()] + mob + s[m.end():]
    w1.write(master, s)


def homepage():
    s = w1.read("index.html")
    g = s.index('hp-guides-gh">Activities &amp; experiences<')
    end = s.index("</ul></div>", g)
    add = ""
    for slug in PAGES:
        if f'class="hp-guide" href="/{slug}"' in s:
            continue
        sp = w1.spec(slug)
        alt = sp["items"][0]["title"].replace('"', "&quot;")
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
        s = re.sub(re.escape(MARK) + r'<div class="w-richtext bpa-wt-guide"><h2 id="related-batch2">.*?</div>\n', "", s, flags=re.S)
        block = f'{MARK}<div class="w-richtext bpa-wt-guide"><h2 id="related-batch2">{h}</h2><p>{p}</p></div>\n'
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
    w1.PAGES = {k: ("", v[1], v[2]) for k, v in PAGES.items()}
    w1.RELATED = RELATED  # sitemap() bumps lastmod for these pages
    w1.thumbs()
    w1.sitemap()
    menu()
    homepage()
    related()
    print("wired", len(PAGES), "pages; now run scripts/sync_layout.py")
