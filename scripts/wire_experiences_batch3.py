#!/usr/bin/env python3
"""Wire the 2026-11-20 experiences batch (segway & e-scooter, stag & hen, private tours).

Same approach as scripts/wire_experiences_batch2.py: nav thumbs, EN menu master items (placed after a
related item in the Tours mega menu and the mobile drawer), the homepage "Activities & experiences" group
plus its JSON-LD ItemList, sitemap, and a short related block (contextual links) on related live pages.
Idempotent. Afterwards run: python3 scripts/sync_layout.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_experiences_batch as w1  # noqa: E402
import wire_experiences_batch2 as w2  # noqa: E402

ROOT = w1.ROOT
# slug: (menu item it goes after, menu title, menu subtitle)
PAGES = {
    "best-segway-tours-budapest": ("/best-bike-tours-budapest", "Segway &amp; E-Scooter Tours", "Segway, MonsteRoller &amp; EZRaider rides"),
    "best-stag-hen-party-activities-budapest": ("/best-pub-crawls-budapest", "Stag &amp; Hen Party Ideas", "Beer bus, party boats &amp; private crawls"),
    "best-private-tours-budapest": ("/best-walking-tours-budapest", "Best Private Tours", "Private guides by car, Jeep or on foot"),
}
SEG = '<a href="/best-segway-tours-budapest">Segway and e-scooter tours</a>'
STAG = '<a href="/best-stag-hen-party-activities-budapest">stag and hen party activities</a>'
PRIV = '<a href="/best-private-tours-budapest">private tours and private guides</a>'
RELATED = {
    "best-bike-tours-budapest": ("Only want a Segway or an e-scooter?",
        f'The {SEG} have their own comparison: 9 rides on whether they climb Castle Hill, price per hour, private options and '
        'rider limits, including the night Segway and the EZRaider that takes kids from 3.'),
    "best-pub-crawls-budapest": ("Planning a stag do or hen party?",
        f'A crawl is one night of the weekend. Compare the {STAG}: the beer bus, a private party boat for 20, a private crawl '
        'with club entry and the burlesque class, with the price per person at your group size.'),
    "best-shooting-ranges-budapest": ("Shooting as part of a stag weekend?",
        f'See how the range fits with the rest of the weekend in our {STAG}: beer bus, party boats, private crawls and Sparty, '
        'with the rules that catch groups out.'),
    "sparty-budapest": ("Booking Sparty for a stag or hen group?",
        f'Build the rest of the weekend from the {STAG}: unlimited-beer bus tours, party cruises with club entry, a private boat '
        'for up to 20 and a private wine tasting.'),
    "best-walking-tours-budapest": ("Want a guide just for your group?",
        f'Compare the {PRIV}: custom walks from €40 per person, a guide and driver by car, an open Jeep for up to 6 and a '
        f'tuk-tuk half day. Rather ride than walk? See the {SEG}.'),
    "best-buda-castle-tours": ("Prefer a private guide on Castle Hill?",
        f'Our comparison of {PRIV} includes a private Buda Castle walk for up to 6 people, plus car and Jeep tours that combine '
        'the Castle District with Pest.'),
    "best-jewish-quarter-tours-budapest": ("Want the Jewish Quarter with a private guide?",
        f'The comparison of {PRIV} includes a private Jewish heritage walk in four languages, alongside private city tours by '
        'car and on foot.'),
    "best-things-to-do-budapest": ("Three more comparisons for your trip",
        f'Groups celebrating should see the {STAG}; if you want a guide just for you, compare the {PRIV}; and for the '
        f'quickest way round the sights, the {SEG}.'),
    "budapest-travel-guide": ("Want a guide for one of the days?",
        f'Any day of this plan can be done with a private guide: compare the {PRIV}. Short on energy? The {SEG} cover '
        'Day 1 and 2 sights in a couple of hours.'),
}
MARK = "<!-- exp-batch3 -->"


def related():
    for page, (h, p) in RELATED.items():
        f = f"{page}.html"
        s = w1.read(f)
        s = re.sub(re.escape(MARK) + r'<div class="w-richtext bpa-wt-guide"><h2 id="related-batch3">.*?</div>\n', "", s, flags=re.S)
        block = f'{MARK}<div class="w-richtext bpa-wt-guide"><h2 id="related-batch3">{h}</h2><p>{p}</p></div>\n'
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
    w2.PAGES = PAGES
    w1.PAGES = {k: ("", v[1], v[2]) for k, v in PAGES.items()}
    w1.RELATED = RELATED  # sitemap() bumps lastmod for these pages
    w1.thumbs()
    w1.sitemap()
    w2.menu()
    w2.homepage()
    related()
    print("wired", len(PAGES), "pages; now run scripts/sync_layout.py")
