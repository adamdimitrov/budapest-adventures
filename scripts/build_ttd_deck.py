#!/usr/bin/env python3
"""Mockup: river-cruise-style comparison deck on the things-to-do page.

Builds best-things-to-do-budapest-test.html (noindex) from the live page:
- copies the deck + filter styles from thermal-baths-budapest.html
- inserts a 10-card deck under the hero, replacing the "At a glance" box
- each card: rating of the featured bookable product (with its source),
  "Book it" product line, affiliate button, link to my subpage

Ratings, review counts and prices of GetYourGuide products were read from
each product page's structured data on 2026-11-13. The Legenda rating is
the 3-site figure already used on /best-budapest-river-cruises.

Run: python3 scripts/build_ttd_table_test.py          (test page)
     python3 scripts/build_ttd_table_test.py --live   (one-shot: rewrites the live page)
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "best-things-to-do-budapest.html"
OUT = ROOT / "best-things-to-do-budapest-test.html"
STYLE_SRC = ROOT / "thermal-baths-budapest.html"
CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"


def gyg(path, cmp):
    return f"https://www.getyourguide.com/budapest-l29/{path}/?partner_id=YS414AJ&utm_medium=online_publisher&cmp=things-to-do-deck-{cmp}"


LEGENDA = "https://legenda.hu/en?partner=38585"
ROWS = [
    dict(name="Danube River Cruise", sid="section-1-go-on-a-river-cruise-on-the-danube",
         img="63b8588b53a4e063ae3b41f8_Budapest-river-cruises-legenda-4.webp",
         area="Danube, between Buda & Pest", time="About 1 hour", cost="Paid ticket", cats="paid evening",
         tip="After dark, when the city is lit up",
         rating=(4.4, "17k+ reviews · 3 sites"), product="Legenda Sightseeing Cruise with Audio Guide & Welcome Drink",
         price="From €20", psub="Day or night sailings", cta=("Check Availability →", LEGENDA),
         sub=("Compare 10 river cruises →", "/best-budapest-river-cruises")),
    dict(name="Széchenyi Thermal Bath", sid="section-2-visit-sz-chenyi-thermal-bath",
         img="64b7a8d6a973a0c983a7095a_11Szechenyi-bath-ourdoor-pool.avif",
         area="City Park, Pest", time="2–3 hours", cost="Paid ticket", cats="paid indoor",
         tip="After a day of sightseeing",
         rating=(4.3, "29.2k reviews on GetYourGuide"), product="Széchenyi Spa Tickets with Optional Upgrades",
         price="From €39", psub="Full-day spa ticket", cta=("Check Availability →", gyg("szechenyi-spa-full-day-entrance-pass-t4139", "szechenyi")),
         sub=("Compare 8 thermal baths →", "/thermal-baths-budapest")),
    dict(name="Parliament Guided Tour", sid="section-3-take-a-guided-tour-in-the-budapest-parliament",
         img="630b4ef13591b53be87b5f75_07-Budapest-Parliament.webp",
         area="Kossuth Square, Pest", time="About 45 minutes", cost="Paid guided tour", cats="paid indoor",
         tip="Book tickets in advance, tours sell out",
         rating=(4.5, "6.6k reviews on GetYourGuide"), product="Parliament Entry Ticket and Audio Guide (€43 on GetYourGuide)",
         price="From HUF 7,000", psub="Official price, EU/EEA adult", cta=("Tickets & tips →", "/budapest-attractions/budapest-parliament"),
         sub=("Ticket + audio guide on GYG →", gyg("budapest-parliament-tour-with-audio-guide-opt-boat-tour-t731430", "parliament"))),
    dict(name="Fisherman's Bastion", sid="section-4-visit-the-fisherman-s-bastion",
         img="63c134f56cbc4a378df403f4_3_1%20Fisherman%27s%20Bastion.webp",
         area="Castle District, Buda", time="30–60 minutes", cost="Free (upper towers paid)", cats="free",
         tip="Early morning or evening, fewer crowds",
         rating=(4.7, "228 reviews on GetYourGuide"), product="Castle Hill Tour: Fisherman's Bastion & Matthias Church",
         price="Free", psub="Guided tour from €39", cta=("See the tour →", gyg("buda-castle-hill-tour-fisherman-s-bastion-matthias-church-t1320374", "bastion")),
         sub=("Compare walking tours →", "/best-walking-tours-budapest")),
    dict(name="Castle District", sid="section-5-walk-around-the-castle-district",
         img="64f9aad9fa207fbabf4d1fb4_Buda%20Castle%20Walking%20Tour%20(11).webp",
         area="Buda Castle Hill", time="Half a day", cost="Free to walk", cats="free",
         tip="Combine with Fisherman's Bastion",
         rating=(4.6, "2.4k reviews on GetYourGuide"), product="Buda Castle District Walking Tour",
         price="Free", psub="Guided walk from €12", cta=("Check Availability →", gyg("budapest-classic-buda-castle-walking-tour-t157275", "castle")),
         sub=("Compare walking tours →", "/best-walking-tours-budapest")),
    dict(name="St. Stephen's Basilica", sid="section-6-visit-st-stephen-s-basilica",
         img="63c134f8dc1eff677ffc6cb7_6_St%20Stpehens%20Basilica.webp",
         area="District V, Pest", time="About 1 hour", cost="Paid entry & dome", cats="paid indoor",
         tip="Climb the dome for a 360° view",
         rating=(4.6, "15.8k reviews on GetYourGuide"), product="St Stephen's Basilica Entry with Options",
         price="From €12", psub="Church entry, dome option", cta=("Check Availability →", gyg("budapest-st-stephen-s-basilica-entry-with-options-t655129", "basilica")),
         sub=("Read more ↓", "#section-6-visit-st-stephen-s-basilica")),
    dict(name="Chain Bridge", sid="section-7-walk-through-the-chain-bridge",
         img="63c134f528404a4d6f6f16b9_9_Sz%C3%A9chenyi%20Chain%20Bridge.webp",
         area="Between Buda and Pest", time="15–20 minutes", cost="Free", cats="free evening",
         tip="At night, when it is lit up",
         rating=(4.8, "51.3k reviews on GetYourGuide"), product="See it from the water: Unlimited Prosecco Night Cruise",
         price="Free", psub="Night cruise from €24.80", cta=("Check Availability →", gyg("budapest-unlimited-prosecco-beer-and-aperol-spritz-cruise-t416276", "chain-bridge")),
         sub=("Compare night cruises →", "/best-night-cruises-budapest")),
    dict(name="Szimpla Kert", sid="section-8-have-a-drink-in-szimpla-kert",
         img="63c134628ac294035bf75327_1_Szimpla%20Ruin%20Bar.webp",
         area="Jewish Quarter, District VII", time="1–2 hours", cost="Free entry", cats="free evening indoor",
         tip="In the evening",
         rating=(4.9, "3.8k reviews on GetYourGuide"), product="Pub Crawl & Ruin Bar Tour with Free Shots & VIP Entry",
         price="Free entry", psub="Ruin bar crawl from €2", cta=("Check Availability →", gyg("budapest-pub-crawl-ruin-bar-tour-free-shots-vip-entry-t1068003", "szimpla")),
         sub=("Jewish Quarter walking tours →", "/best-walking-tours-budapest")),
    dict(name="Vajdahunyad Castle", sid="section-9-visit-vajdahunyad-s-castle",
         img="63c134f5364d23a28fede171_11_Vajdahunyad%20Castle.webp",
         area="City Park, Pest", time="About 1 hour", cost="Free grounds", cats="free",
         tip="Pair it with Széchenyi Bath next door",
         rating=None, product="Next door: Széchenyi Spa Tickets (4.3, 29.2k reviews)",
         price="Free", psub="Grounds are free", cta=("Széchenyi tickets →", gyg("szechenyi-spa-full-day-entrance-pass-t4139", "vajdahunyad")),
         sub=("Compare 8 thermal baths →", "/thermal-baths-budapest")),
    dict(name="New York Café", sid="section-10-have-a-coffee-and-dessert-in-new-york-caf",
         img="63c134f866978fcd5de146da_21_New%20York%20Caf%C3%A9.webp",
         area="Erzsébet körút, Pest", time="About 1 hour", cost="Paid (pricey)", cats="paid indoor",
         tip="Go for the atmosphere, not a bargain",
         rating=None, product=None,
         price="Paid", psub="Pricey, go for the room", cta=("Read more ↓", "#section-10-have-a-coffee-and-dessert-in-new-york-caf"),
         sub=("Budapest travel guide →", "/budapest-travel-guide")),
]
FILTERS = [("all", "All"), ("free", "Free"), ("paid", "Paid tickets"), ("evening", "Evening"), ("indoor", "Indoor / rainy day")]


def esc(s):
    return html.escape(s, quote=True)


def link_attrs(url):
    return ' rel="sponsored noopener" target="_blank"' if url.startswith("http") else ""


def card(i, r):
    tag = '<span class="bpa-rank-tag bpa-gold">#1 Must-Do</span>' if i == 1 else f'<span class="bpa-rank-tag bpa-slate">#{i}</span>'
    title_url = r["sub"][1] if not r["sub"][1].startswith(("#", "http")) else "#" + r["sid"]
    rating = ""
    if r["rating"]:
        sc, meta = r["rating"]
        rating = (f'<div class="ttd-rate"><span class="ttd-stars" style="--r:{sc}" aria-hidden="true">★★★★★</span>'
                  f'<b>{sc}</b><span>{esc(meta)}</span></div>')
    product = f'<div class="ttd-product"><strong>Book it:</strong> {esc(r["product"])}</div>' if r["product"] else ""
    cta_label, cta_url = r["cta"]
    sub_label, sub_url = r["sub"]
    return f'''<div class="bpa-card" data-cat="{r["cats"]}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">{tag}
<div aria-label="{esc(r["name"])} photo" class="bpa-slider" tabindex="0"><img alt="{esc(r["name"])}, Budapest" height="534" width="800" loading="{'eager' if i <= 2 else 'lazy'}" decoding="async" src="{CDN}{r["img"]}"/></div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{esc(r["area"])} • {esc(r["time"])}</div>
<a class="bpa-title" href="{esc(title_url)}">{i}. {esc(r["name"])}</a>
{rating}
<div class="bpa-specs-row"><span class="bpa-sp">{esc(r["cost"])}</span><span class="bpa-sp">{esc(r["time"])}</span><span class="bpa-sp">{esc(r["area"].split(",")[0])}</span></div>
{product}
<div class="bpa-best-for"><strong>Local tip:</strong> {esc(r["tip"])}</div>
</div>
<div class="bpa-cta-cell">
<div><div class="bpa-price">{esc(r["price"])}</div><div class="bpa-psub">{esc(r["psub"])}</div></div>
<a class="bpa-btn" href="{esc(cta_url)}"{link_attrs(cta_url)}>{esc(cta_label)}</a>
<a class="bpa-sublink" href="#{r["sid"]}" hidden aria-hidden="true" tabindex="-1"></a>
<a class="bpa-sublink" href="{esc(sub_url)}"{link_attrs(sub_url)}>{esc(sub_label)}</a>
</div>
</div>
</div>'''


CSS = """<style id="ttd-deck-mock">
.ttd-deck-head{width:100%;max-width:1240px;margin:8px auto 0;padding:0 16px;box-sizing:border-box}
.ttd-deck-head h2{font-family:'Playfair Display',Georgia,serif;font-size:clamp(24px,3vw,32px);color:#0f172a;margin:0 0 6px}
.ttd-deck-head p{font-size:15px;color:#475569;margin:0}
.ttd-deck-head h2,.ttd-deck-head p{white-space:normal;overflow-wrap:break-word}
.ttd-deck-head .ltt-integrated-filter-bar{border-top:0;margin-top:12px;padding-top:0;max-width:100%}
.comparison-table{width:100%}
#ttd-deck .bpa-media .bpa-slider img{object-fit:cover}
.ttd-rate{display:flex;align-items:center;gap:6px;font-size:12.5px;color:#475569;margin:6px 0 8px}
.ttd-rate b{color:#0f172a;font-weight:800}
.ttd-stars{font-size:13px;letter-spacing:1px;background:linear-gradient(90deg,#dfa732 calc(var(--r) / 5 * 100%),#cbd5e1 0);-webkit-background-clip:text;background-clip:text;color:transparent}
.ttd-product{font-size:13px;color:#334155;margin:8px 0 6px;line-height:1.45}
.ttd-product strong{color:#0f172a}
</style>"""


def main():
    s = SRC.read_text()
    styles = STYLE_SRC.read_text()
    stats = (ROOT / "budapest-tourism-statistics.html").read_text()
    for src, sid in ((stats, "ltt-hero-card-styles"), (styles, "ltt-dubai-safari-styles")):
        m = re.search(r'<style id="%s">.*?</style>' % sid, src, re.S)
        assert m, sid
        s = s.replace("</head>", m.group(0) + "</head>", 1)
    live = "--live" in sys.argv
    s = s.replace("</head>", CSS + ("" if live else '<meta name="robots" content="noindex, nofollow"/>') + "</head>", 1)

    counts = {c: sum(1 for r in ROWS if c in r["cats"].split()) for c, _ in FILTERS if c != "all"}
    counts["all"] = len(ROWS)
    pills = "".join(
        f'<button class="ltt-tab-btn{" active" if c == "all" else ""}" data-cat="{c}" onclick="lttFilterItems(\'{c}\', this)" type="button">{l} ({counts[c]})</button>'
        for c, l in FILTERS)
    hero = f'''<div class="ltt-hero-wrap"> <div class="ltt-clean-card"> <div class="ltt-top-bar"> <nav aria-label="Breadcrumb" class="ltt-breadcrumbs"> <a href="/">Home</a> <span class="ltt-bc-sep">›</span> <span class="ltt-bc-current">Top 10 Things to Do in Budapest (2026)</span> </nav> <span class="ltt-hero-kicker-badge">Local's Guide · 10 Visited in Person</span> </div> <h1 class="ltt-editorial-h1"> Top 10 Best Things to Do in Budapest in 2026 <span class="ltt-h1-muted">(Local's Guide)</span> </h1> <div class="ltt-trust-bar"> <div class="ltt-author-cluster"> <div class="ltt-author-avatar-wrap"> <img alt="Adam Dimitrov" class="ltt-author-avatar" height="48" loading="eager" src="/assets/adam-dimitrov.webp" width="48"/> </div> <div class="ltt-author-meta"> <div class="ltt-author-line"> By <a href="/about" target="_blank">Adam Dimitrov</a> · Founder &amp; Local Budapest Guide </div> <div class="ltt-author-role">Every stop visited in person • Own photos • Booking ratings checked Nov 13, 2026</div> </div> </div> <div class="ltt-trust-pills"> <span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: Nov 13, 2026</span> </div> </div> <div class="ltt-lead-copy"> <p>Feeling overwhelmed by endless lists of things to do in Budapest? This one is <strong>written by a local</strong>: I have spent years exploring my hometown and <strong>personally tested every attraction</strong> on it, with my own photos and practical tips.</p> <p>These are the <strong>10 I would pick for a first visit</strong>, ranked by quality, uniqueness and value for your time. Compare cost, time needed and ratings below, or filter for free sights, evening plans or a rainy day.</p> <p class="bprv-callout" style="margin:14px 0 4px 0 !important;padding:12px 16px !important;background:#fdfaf2 !important;border:1px solid #f2e0b6 !important;border-left:4px solid #dfa732 !important;border-radius:10px !important;font-size:15px !important;line-height:1.55 !important;color:#0f172a !important;"><strong>Only one evening?</strong> Take a Danube cruise after dark: Parliament, Buda Castle and the bridges lit up in about an hour. <a href="/best-budapest-river-cruises">Compare the 10 best river cruises →</a></p> <figure class="cd-bookmark-wrapper"> <a href="/budapest-attractions/budapest-parliament" class="cd-editorial-bookmark" target="_blank" rel="noopener"> <div class="cd-editorial-body"> <div> <div class="cd-editorial-title">Budapest Parliament Tour 2026 (Tickets, Prices &amp; Tips)</div> <div class="cd-editorial-desc">Official 2026 ticket prices, opening hours, tour languages and how to avoid sell-outs for the tour 700,000 people take each year, from my own visits.</div> </div> <div class="cd-editorial-meta"> <img class="cd-editorial-icon" src="/assets/budapest-adventures-logo-96.webp" alt="BUDAPEST ADVENTURES" width="18" height="18" /> <span class="cd-editorial-pub">BUDAPEST ADVENTURES</span> <span class="cd-editorial-dot">•</span> <span class="cd-editorial-author">Adam Dimitrov</span> </div> </div> <div class="cd-editorial-thumb"> <img src="/assets/cdn/60e43c7d6d05b671dff0dc1a/650c1f90c059d2467627bad9_budapest-parliament-hero-image.webp" alt="Budapest Parliament Tour 2026" loading="lazy" /> </div> </a> </figure> </div> <div class="ltt-integrated-filter-bar"><span class="ltt-filter-label">Filters:</span><div class="ltt-integrated-pills">{pills}</div></div> </div> </div>'''
    deck = ('<div class="comparison-table"><div class="container-27"><div class="ltt-deck-container" id="ttd-deck"><div class="bpa-deck-wrap" id="ltt-cards-deck">'
            + "".join(card(i + 1, r) for i, r in enumerate(ROWS)) + '</div></div></div></div>')

    # new hero card + deck replace the old hero image, author block, intro and "At a glance" box
    start = s.index('<div class="hero-image-wrapper">')
    end = s.index('<div class="blog-section">')
    old = s[start:end]
    assert "bpa-at-a-glance" in old and "Are you feeling overwhelmed" in old
    s = s[:start] + hero + deck + s[end:]

    cfg = {"deckId": "ttd-deck", "tocDeckLabel": "Compare all 10 at a glance",
           "tocBreakdownLabel": "The 10 in detail", "shortTitles": [r["name"] for r in ROWS]}
    s = s.replace("</head>", "<script>window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";</script></head>", 1)
    first = '<details class="bpa-details-card" id="section-1-'
    assert s.count(first) == 1
    s = s.replace(first, '<div id="breakdown-header"></div>' + first, 1)
    assert "—" not in deck
    if live:
        # dates: JSON-LD dateModified
        s = re.sub(r'"dateModified":\s*"[0-9-]+"', '"dateModified":"2026-11-13"', s)
        out = SRC
    else:
        out = OUT
    out.write_text(s)
    print("wrote", out.name, len(s))


if __name__ == "__main__":
    main()
