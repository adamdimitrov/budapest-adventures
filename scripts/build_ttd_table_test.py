#!/usr/bin/env python3
"""Mockup: river-cruise-style comparison deck on the things-to-do page.

Builds best-things-to-do-budapest-test.html (noindex) from the live page:
- copies the deck + filter styles from thermal-baths-budapest.html
- inserts a 10-card deck under the hero, replacing the "At a glance" box
- card data comes from each section's own verified strip (area, cost,
  time, tip, guide link); no ratings or prices that are not on the page

Run: python3 scripts/build_ttd_table_test.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "best-things-to-do-budapest.html"
OUT = ROOT / "best-things-to-do-budapest-test.html"
STYLE_SRC = ROOT / "thermal-baths-budapest.html"
CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"

# name, section id, image, area, time, cost chip, price box, price sub, cta (label, url, external), cats, tip
ROWS = [
    ("Danube River Cruise", "section-1-go-on-a-river-cruise-on-the-danube",
     "63b8588b53a4e063ae3b41f8_Budapest-river-cruises-legenda-4.webp", "Danube, between Buda & Pest", "About 1 hour",
     "Paid ticket", "From €20", "Sightseeing cruise",
     ("Check Availability →", "https://legenda.hu/en?partner=38585", True), "paid evening",
     "After dark, when the city is lit up"),
    ("Széchenyi Thermal Bath", "section-2-visit-sz-chenyi-thermal-bath",
     "64b7a8d6a973a0c983a7095a_11Szechenyi-bath-ourdoor-pool.avif", "City Park, Pest", "2–3 hours",
     "Paid ticket", "Paid ticket", "Full-day entry, book online",
     ("Check Availability →", "https://www.getyourguide.com/budapest-l29/szechenyi-spa-full-day-entrance-pass-t4139/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=things-to-do-budapest-szechenyi-deck", True),
     "paid indoor", "After a day of sightseeing"),
    ("Parliament Guided Tour", "section-3-take-a-guided-tour-in-the-budapest-parliament",
     "630b4ef13591b53be87b5f75_07-Budapest-Parliament.webp", "Kossuth Square, Pest", "About 45 minutes",
     "Paid guided tour", "From HUF 7,000", "Official tour, book ahead",
     ("Tickets & tips →", "/budapest-attractions/budapest-parliament", False), "paid indoor",
     "Book tickets in advance, tours sell out"),
    ("Fisherman's Bastion", "section-4-visit-the-fisherman-s-bastion",
     "63c134f56cbc4a378df403f4_3_1%20Fisherman%27s%20Bastion.webp", "Castle District, Buda", "30–60 minutes",
     "Free (upper towers paid)", "Free", "Upper towers paid",
     ("Walking tours →", "/best-walking-tours-budapest", False), "free",
     "Early morning or evening, fewer crowds"),
    ("Castle District", "section-5-walk-around-the-castle-district",
     "64f9aad9fa207fbabf4d1fb4_Buda%20Castle%20Walking%20Tour%20(11).webp", "Buda Castle Hill", "Half a day",
     "Free to walk", "Free", "Walk it on your own",
     ("Walking tours →", "/best-walking-tours-budapest", False), "free",
     "Combine with Fisherman's Bastion"),
    ("St. Stephen's Basilica", "section-6-visit-st-stephen-s-basilica",
     "63c134f8dc1eff677ffc6cb7_6_St%20Stpehens%20Basilica.webp", "District V, Pest", "About 1 hour",
     "Paid entry & dome", "Paid entry", "Church + dome tickets",
     ("Check Availability →", "https://www.getyourguide.com/budapest-l29/budapest-st-stephen-s-basilica-entry-with-options-t655129/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=things-to-do-budapest-basilica-deck", True),
     "paid indoor", "Climb the dome for a 360° view"),
    ("Chain Bridge", "section-7-walk-through-the-chain-bridge",
     "63c134f528404a4d6f6f16b9_9_Sz%C3%A9chenyi%20Chain%20Bridge.webp", "Between Buda and Pest", "15–20 minutes",
     "Free", "Free", "Best seen at night",
     ("Night cruises →", "/best-night-cruises-budapest", False), "free evening",
     "At night, when it is lit up"),
    ("Szimpla Kert", "section-8-have-a-drink-in-szimpla-kert",
     "63c134628ac294035bf75327_1_Szimpla%20Ruin%20Bar.webp", "Jewish Quarter, District VII", "1–2 hours",
     "Free entry", "Free entry", "Pay for your drinks",
     ("Food & walking tours →", "/best-walking-tours-budapest", False), "free evening indoor",
     "In the evening"),
    ("Vajdahunyad Castle", "section-9-visit-vajdahunyad-s-castle",
     "63c134f5364d23a28fede171_11_Vajdahunyad%20Castle.webp", "City Park, Pest", "About 1 hour",
     "Free grounds", "Free", "Grounds are free",
     ("Thermal baths →", "/thermal-baths-budapest", False), "free",
     "Pair it with Széchenyi Bath next door"),
    ("New York Café", "section-10-have-a-coffee-and-dessert-in-new-york-caf",
     "63c134f866978fcd5de146da_21_New%20York%20Caf%C3%A9.webp", "Erzsébet körút, Pest", "About 1 hour",
     "Paid (pricey)", "Paid", "Pricey, go for the room",
     ("Read more ↓", "#section-10-have-a-coffee-and-dessert-in-new-york-caf", False), "paid indoor",
     "Go for the atmosphere, not a bargain"),
]
FILTERS = [("all", "All"), ("free", "Free"), ("paid", "Paid tickets"), ("evening", "Evening"), ("indoor", "Indoor / rainy day")]


def esc(s):
    return html.escape(s, quote=True)


def card(i, r):
    name, sid, img, area, time, cost, price, psub, (cta, url, ext), cats, tip = r
    tag = f'<span class="bpa-rank-tag bpa-gold">#1 Must-Do</span>' if i == 1 else f'<span class="bpa-rank-tag bpa-slate">#{i}</span>'
    attrs = ' rel="sponsored noopener" target="_blank"' if ext else ''
    return f'''<div class="bpa-card" data-cat="{cats}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">{tag}
<div aria-label="{esc(name)} photo" class="bpa-slider" tabindex="0"><img alt="{esc(name)}, Budapest" height="534" width="800" loading="{'eager' if i <= 2 else 'lazy'}" decoding="async" src="{CDN}{img}"/></div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{esc(area)} • {esc(time)}</div>
<a class="bpa-title" href="#{sid}">{i}. {esc(name)}</a>
<div class="bpa-specs-row"><span class="bpa-sp">{esc(cost)}</span><span class="bpa-sp">{esc(time)}</span><span class="bpa-sp">{esc(area.split(",")[0])}</span></div>
<div class="bpa-best-for"><strong>Local tip:</strong> {esc(tip)}</div>
</div>
<div class="bpa-cta-cell">
<div><div class="bpa-price">{esc(price)}</div><div class="bpa-psub">{esc(psub)}</div></div>
<a class="bpa-btn" href="{esc(url)}"{attrs}>{esc(cta)}</a>
<a class="bpa-sublink" href="#{sid}">Read more ↓</a>
</div>
</div>
</div>'''


def main():
    s = SRC.read_text()
    styles = STYLE_SRC.read_text()
    for sid in ("ltt-hero-card-styles", "ltt-dubai-safari-styles"):
        m = re.search(r'<style id="%s">.*?</style>' % sid, styles, re.S)
        assert m, sid
        s = s.replace("</head>", m.group(0) + "</head>", 1)
    extra = """<style id="ttd-deck-mock">
.ttd-deck-head{width:100%;max-width:1240px;margin:8px auto 0;padding:0 16px;box-sizing:border-box}
.ttd-deck-head h2{font-family:'Playfair Display',Georgia,serif;font-size:clamp(24px,3vw,32px);color:#0f172a;margin:0 0 6px}
.ttd-deck-head p{font-size:15px;color:#475569;margin:0}
.ttd-deck-head .ltt-integrated-filter-bar{border-top:0;margin-top:12px;padding-top:0;max-width:100%}\n.ttd-deck-head h2,.ttd-deck-head p{white-space:normal;overflow-wrap:break-word}\n.comparison-table{width:100%}
#ttd-deck .bpa-media .bpa-slider img{object-fit:cover}
</style>"""
    s = s.replace("</head>", extra + '<meta name="robots" content="noindex, nofollow"/></head>', 1)

    counts = {c: sum(1 for r in ROWS if c in r[9].split()) for c, _ in FILTERS if c != "all"}
    counts["all"] = len(ROWS)
    pills = "".join(
        f'<button class="ltt-tab-btn{" active" if c == "all" else ""}" data-cat="{c}" onclick="lttFilterItems(\'{c}\', this)" type="button">{l} ({counts[c]})</button>'
        for c, l in FILTERS)
    deck = ('<div class="ttd-deck-head"><h2 id="compare-at-a-glance">Compare all 10 at a glance</h2>'
            '<p>Cost, time needed and the best time to go, from my own visits. Filter by what fits your day.</p>'
            f'<div class="ltt-integrated-filter-bar"><span class="ltt-filter-label">Filters:</span><div class="ltt-integrated-pills">{pills}</div></div></div>'
            '<div class="comparison-table"><div class="container-27"><div class="ltt-deck-container" id="ttd-deck"><div class="bpa-deck-wrap" id="ltt-cards-deck">'
            + "".join(card(i + 1, r) for i, r in enumerate(ROWS)) + '</div></div></div></div>')

    # insert under the hero, before the article body
    anchor = '<div class="blog-section">'
    assert s.count(anchor) == 1
    s = s.replace(anchor, deck + anchor, 1)
    # the deck replaces the "At a glance" box
    m = re.search(r'<div class="bpa-at-a-glance".*?</ol>\s*</div>', s, re.S)
    assert m
    s = s.replace(m.group(0), "", 1)
    # runtime config: card names in the rebuilt contents list
    import json
    cfg = {"deckId": "compare-at-a-glance", "tocDeckLabel": "Compare all 10 at a glance",
           "tocBreakdownLabel": "The 10 in detail", "shortTitles": [r[0] for r in ROWS]}
    s = s.replace("</head>", "<script>window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";</script></head>", 1)
    first = '<details class="bpa-details-card" id="section-1-'
    assert s.count(first) == 1
    s = s.replace(first, '<div id="breakdown-header"></div>' + first, 1)
    OUT.write_text(s)
    print("wrote", OUT.name, len(s))


if __name__ == "__main__":
    main()
