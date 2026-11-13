#!/usr/bin/env python3
"""Rebuild /budapest-attractions/budapest-parliament (budapest-parliament.html)
in the article design used by the tourism statistics and Christmas pages:
hero card (breadcrumb, badge, H1, author bar, last updated, lead), sticky TOC,
fact tiles, tables, native FAQ.

Keeps the page's own head assets, menu (22-language switcher), footer and
scripts. Copies the hero-card and tile/table styles from the stats page.

Facts checked 2026-11-13 against the Office of the National Assembly:
- parlament.jegymester.hu/eng/Index/ (opening hours, tour languages, closures)
- hungarian_parliament_admission_fees_01012026.pdf (2026 prices)

Run: python3 scripts/build_parliament.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "budapest-parliament.html"
STATS = ROOT / "budapest-tourism-statistics.html"
URL = "https://www.budapestadventures.com/budapest-attractions/budapest-parliament"
CDN = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
TICKETS = "https://jegymester.hu/production/480000/hungarian-parliament-building-parliament-visit"
UPDATED_ISO = "2026-11-13"
UPDATED_TXT = "Nov 13, 2026"

TITLE = "Budapest Parliament Tour 2026: Tickets, Prices & Tips"
DESC = ("How to visit the Hungarian Parliament in 2026: official ticket prices "
        "(HUF 7,000 EU / 14,000 non-EU), opening hours, tour languages, how to "
        "avoid sell-outs and what you see inside. By a Budapest local.")

FAQ = [
    ("How much is a Budapest Parliament ticket in 2026?",
     "From 1 January 2026 an adult ticket costs HUF 7,000 for EU/EEA citizens and HUF 14,000 for everyone else. "
     "Students aged 6 to 24 pay half (HUF 3,500 or HUF 7,000) with a valid student card. Children under 6 go in free."),
    ("Can you visit the Hungarian Parliament without a tour?",
     "No. You can only go inside on the official 45-minute tour, with a live guide or an audioguide. "
     "The square, the riverside and the free museum in the Visitor Centre are open to everyone."),
    ("How long is the Parliament tour?",
     "About 45 minutes. Add 15 minutes for the security check, which you go through before your slot."),
    ("Do Parliament tickets sell out?",
     "Yes, especially in summer, at weekends and for English tours. Book online a few days to a few weeks ahead. "
     "The Visitor Centre only sells a limited number of same-day tickets."),
    ("Where do I buy official Parliament tickets?",
     "On jegymester.hu, the ticket system run for the Office of the National Assembly, or at the Visitor Centre ticket office. "
     "Other sites sell the same tour at a higher price."),
    ("Can I take photos inside the Parliament?",
     "Yes, in most rooms. Photos and videos are not allowed in the Dome Hall, where the Holy Crown is guarded."),
    ("What are the Parliament opening hours?",
     "Daily 8:00 to 18:00 from 1 April to 31 October, and 8:00 to 16:00 from 1 November to 31 March. "
     "The building closes for parliamentary sittings and state events, sometimes at short notice."),
]

TOC = [
    ("key-facts", "Key facts at a glance"),
    ("tickets", "Ticket prices 2026"),
    ("how-to-book", "How to book (and avoid sell-outs)"),
    ("opening-hours", "Opening hours and closures"),
    ("the-tour", "The guided tour: languages and route"),
    ("security", "Security check and what to bring"),
    ("getting-there", "How to get there"),
    ("history", "History and architecture"),
    ("best-views", "Best views of the Parliament"),
    ("faq", "FAQ"),
]


def img(file, alt, w, h, cls="bpa-photo", eager=False):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{CDN}{file}" alt="{alt}" width="{w}" height="{h}" '
            f'class="{cls}" decoding="async" {load}/>')


def figure(file, alt, w, h, caption, eager=False):
    return (f'<figure class="bpa-fig">{img(file, alt, w, h, eager=eager)}'
            f'<figcaption>{caption}</figcaption></figure>')


HERO = f"""<div class="ltt-hero-wrap"> <div class="ltt-clean-card"> <div class="ltt-top-bar"> <nav aria-label="Breadcrumb" class="ltt-breadcrumbs"> <a href="/">Home</a> <span class="ltt-bc-sep">›</span> <span class="ltt-bc-current">Budapest Parliament Tour (2026)</span> </nav> <span class="ltt-hero-kicker-badge">Official 2026 prices · Visited in person</span> </div> <h1 class="ltt-editorial-h1"> Budapest Parliament Tour 2026 <span class="ltt-h1-muted">(Tickets, Prices &amp; Tips)</span> </h1> <div class="ltt-trust-bar"> <div class="ltt-author-cluster"> <div class="ltt-author-avatar-wrap"> <img alt="Adam Dimitrov" class="ltt-author-avatar" height="48" loading="eager" src="/assets/adam-dimitrov.webp" width="48"/> </div> <div class="ltt-author-meta"> <div class="ltt-author-line"> By <a href="/about" target="_blank">Adam Dimitrov</a> · Founder &amp; Local Budapest Guide </div> <div class="ltt-author-role">Prices and hours from the Office of the National Assembly • <a href="#sources">Sources</a></div> </div> </div> <div class="ltt-trust-pills"> <span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: {UPDATED_TXT}</span> </div> </div> <div class="ltt-lead-copy"> <p>The Hungarian Parliament is the building on every Budapest postcard, and more than <strong>700,000 people</strong> take the official tour each year. You can only go inside on a <strong>45-minute guided tour</strong>, and tickets for English slots often sell out.</p> <p>Short version: book on the official site, <a href="{TICKETS}" rel="nofollow noopener" target="_blank">jegymester.hu</a>, a few days ahead. Adults pay <strong>HUF 7,000</strong> (EU/EEA) or <strong>HUF 14,000</strong> (everyone else) in 2026. Below is everything I wish I had known before my first visit.</p> </div> </div></div>"""


def tiles(items):
    return '<div class="bpa-tiles">' + "".join(
        f'<div class="bpa-tile"><div class="bpa-tile-num">{n}</div><div class="bpa-tile-lab">{l}</div></div>'
        for n, l in items) + "</div>"


BODY = f"""
{figure("650c1f90c059d2467627bad9_budapest-parliament-hero-image.webp", "The Hungarian Parliament Building on the Danube bank in Budapest", 1280, 720, "The Parliament from the Buda side of the Danube.", eager=True)}

<h2 id="key-facts">Key facts at a glance</h2>
{tiles([("HUF 7,000", "adult ticket for EU/EEA citizens (2026)"), ("HUF 14,000", "adult ticket for non-EU/EEA visitors"), ("45 min", "guided tour, live guide or audioguide"), ("26", "tour languages, 6 with a live guide")])}
<ul role="list">
<li><strong>Address:</strong> Kossuth Lajos tér 1-3, 1055 Budapest. Tours start at the underground Visitor Centre on the north side of the square.</li>
<li><strong>Open:</strong> daily, 8:00 to 18:00 (April to October) and 8:00 to 16:00 (November to March).</li>
<li><strong>Only way in:</strong> the official tour. There is no self-guided entry.</li>
<li><strong>Book at:</strong> <a href="{TICKETS}" rel="nofollow noopener" target="_blank">jegymester.hu</a>, the official ticket system, or at the Visitor Centre on the day if any tickets are left.</li>
</ul>

<h2 id="tickets">Budapest Parliament ticket prices 2026</h2>
<p>The price depends on two things: your citizenship and your age. Hungarians and citizens of the European Economic Area (the EU plus Iceland, Liechtenstein and Norway) pay the reduced rate. Visitors from the UK, the US, Switzerland and everywhere else pay the full rate.</p>
<div class="bpa-table-wrap"><table class="bpa-table"><caption>Admission fees valid from 1 January 2026, per the Office of the National Assembly. Online orders add a small booking fee.</caption>
<thead><tr><th>Ticket</th><th>EU/EEA citizens</th><th>Non-EU/EEA</th></tr></thead>
<tbody>
<tr><td>Adult</td><td>HUF 7,000</td><td>HUF 14,000</td></tr>
<tr><td>Student (6 to 24)</td><td>HUF 3,500</td><td>HUF 7,000</td></tr>
<tr><td>Child under 6</td><td>Free</td><td>Free</td></tr>
</tbody></table></div>
<ul role="list">
<li><strong>Bring proof.</strong> EU/EEA visitors show an ID card or passport. Students need a Hungarian or international (ISIC) student card. Staff can check at the door.</li>
<li><strong>No family tickets any more.</strong> Older guides (including the first version of this one) list family tickets. They are not on the 2026 price list.</li>
<li><strong>Prices are in forints.</strong> Card payment converts at your bank's rate, so pay in HUF if the terminal asks.</li>
</ul>

<h2 id="how-to-book">How to book (and avoid sell-outs)</h2>
{figure("637002f28fa468092824b4d2_hungarian-parliament-sold-out.webp", "Sold out sign at the Budapest Parliament Visitor Centre ticket office", 889, 500, "The sign that greeted me on my first try. Every English tour that day was gone.")}
<p>The first time I went, I just turned up. Every English tour was sold out by late morning. Learn from my mistake:</p>
<ol role="list">
<li><strong>Book online on <a href="{TICKETS}" rel="nofollow noopener" target="_blank">jegymester.hu</a>.</strong> It is the ticket system run for the Office of the National Assembly, so you pay the official price. Pick the date, the language and the time slot.</li>
<li><strong>Book early in high season.</strong> From May to September, and on weekends all year, English slots go days ahead. In winter a day or two is usually enough.</li>
<li><strong>Same-day tickets are a gamble.</strong> The Visitor Centre ticket office opens at 8:00 and sells whatever is left, by card or cash in forints.</li>
<li><strong>Watch out for resellers.</strong> Tour sites and look-alike "Parliament" websites sell the same audioguide tour for more. If the price is not HUF 7,000 or HUF 14,000 plus a small fee, you are not on the official site.</li>
</ol>
{figure("636fb62863d65347ae6f772f_6300be26073090236498a7d0_Parlamenti%2520l%25C3%25A1togat%25C3%25A1s.webp", "Example of an official Budapest Parliament e-ticket from Jegymester", 737, 756, "The e-ticket arrives by email. Show it on your phone or print it.")}

<h2 id="opening-hours">Opening hours and closures</h2>
<div class="bpa-table-wrap"><table class="bpa-table"><caption>Visiting hours per the Office of the National Assembly. Last tours start before closing time.</caption>
<thead><tr><th>Period</th><th>Days</th><th>Hours</th></tr></thead>
<tbody>
<tr><td>1 January to 31 March</td><td>Monday to Sunday</td><td>8:00 to 16:00</td></tr>
<tr><td>1 April to 31 October</td><td>Monday to Sunday</td><td>8:00 to 18:00</td></tr>
<tr><td>1 November to 31 December</td><td>Monday to Sunday</td><td>8:00 to 16:00</td></tr>
</tbody></table></div>
<p>This is a working parliament, so tours stop for <strong>plenary sittings, state visits and protocol events</strong>. Closures are posted on the ticket site, sometimes only a few days ahead. If your tour is cancelled, you get your money back.</p>
<p>National holidays (15 March, 20 August, 23 October) bring ceremonies on Kossuth Square and changed schedules. Check the booking page the day before you go.</p>

<h2 id="the-tour">The guided tour: languages and route</h2>
{figure("6370067c18e574076665750a_hungarian-parliament-languages.webp", "Board showing the Budapest Parliament guided tour languages", 889, 500, "Tour languages on the board at the Visitor Centre.")}
<p>Every tour lasts <strong>45 minutes</strong> and runs at a fixed time slot. You choose the language when you book:</p>
<ul role="list">
<li><strong>Live guide or audioguide:</strong> Hungarian, English, French, German, Italian and Spanish.</li>
<li><strong>Audioguide only (mixed groups):</strong> Russian, Polish, Slovak, Croatian, Hebrew, Romanian, Serbian, Ukrainian, Korean, Portuguese, Arabic, Slovenian, Czech, Chinese, Japanese, Bulgarian, Turkish, Dutch, Greek and Vietnamese.</li>
</ul>
<p>The route takes you through the most beautiful parts of the building:</p>
<ul role="list">
<li><strong>The Main Staircase</strong>, a riot of gold leaf, frescoes and red carpet.</li>
<li><strong>The Dome Hall</strong>, where the Holy Crown of Hungary is kept under armed guard. No photos here.</li>
<li><strong>The Chamber of the former Upper House</strong> (Chamber of Peers) and its lounge, with the famous numbered cigar holders on the window sills.</li>
</ul>
{figure("630b4ef1b123fb9a88bc17d5_08-Budapest-Parliament.webp", "Chamber of Peers inside the Hungarian Parliament Building", 800, 450, "The old Chamber of Peers, the last stop on the tour.")}
<p>While you wait, the Visitor Centre has a café, a gift shop and a free exhibition on <em>1,000 years of Hungarian legislation</em>. Use the toilets before your tour starts.</p>

<h2 id="security">Security check and what to bring</h2>
<p>You enter through an airport-style security check, so arrive <strong>15 minutes before your slot</strong>. Latecomers may be turned away.</p>
<ul role="list">
<li><strong>Bring:</strong> your ticket, your ID or passport (for EU/EEA prices) and your student card if you bought a student ticket.</li>
<li><strong>Leave behind:</strong> knives, sharp objects and large bags. Small (0.5 litre) plastic water bottles are fine.</li>
<li><strong>Accessibility:</strong> the Visitor Centre and the tour are wheelchair accessible. Email <a href="mailto:tourist.office@parlament.hu">tourist.office@parlament.hu</a> before your visit so staff can help.</li>
<li><strong>Guide dogs</strong> are allowed. Other pets are not.</li>
</ul>

<h2 id="getting-there">How to get there</h2>
<p>The Parliament sits on the Pest bank of the Danube, a 15-minute walk from the city centre. Kossuth Square is car-free and there is no visitor parking, so use public transport:</p>
<ul role="list">
<li><strong>Metro M2</strong> (red line) to <strong>Kossuth Lajos tér</strong>. The station exit is on the square.</li>
<li><strong>Tram 2</strong> along the Danube. It is one of the most scenic tram rides in Europe and stops right below the building.</li>
<li><strong>Trolleybus 70 or 78</strong> to Kossuth Lajos tér.</li>
</ul>
{figure("636fd3dff0039425bf4254b7_budapest-parliament-map.webp", "Map of public transport stops near the Budapest Parliament Visitor Centre", 889, 600, "Tram 2 (yellow), Metro M2 (red), trolleybus 70/78 (blue) and the Visitor Centre entrance (green).")}
<p>Single tickets and travel passes are sold in the BudapestGo app. If you plan a busy few days, compare the price of a pass with the <a href="/budapest-card-is-it-worth-it">Budapest Card</a>, which includes unlimited public transport.</p>

<h2 id="history">History and architecture</h2>
{figure("637290c09859ab6e121f3d49_budapest-parliament-painting.webp", "Painting of the Hungarian Parliament Building in 1899", 889, 500, "The new Parliament, painted in 1899.")}
<p>Buda, Pest and Óbuda merged into Budapest in <strong>1873</strong>, and the new capital wanted a parliament to match its ambitions. An international design competition was won by <strong>Imre Steindl</strong>, and building work started in <strong>1885</strong>.</p>
<p>The Parliament was inaugurated in <strong>1896</strong>, the 1,000th anniversary of the Hungarian state, and completed in <strong>1904</strong>. Steindl went blind before it was finished and died in 1902, two years before completion.</p>
<ul role="list">
<li><strong>Style:</strong> Gothic Revival facades and spires on a Baroque-style symmetrical floor plan, with a Renaissance Revival dome.</li>
<li><strong>Size:</strong> 268 metres long, with 691 rooms. It is the largest building in Hungary.</li>
<li><strong>Height:</strong> the dome is 96 metres tall, a nod to the year 896, when the Magyars settled the Carpathian Basin. St Stephen's Basilica is the same height, and no building in the centre may be taller.</li>
<li><strong>The Holy Crown</strong> of Hungary has been kept in the Dome Hall since 2000.</li>
</ul>

<h2 id="best-views">Best views of the Parliament</h2>
<p>The tour shows you the inside. For the classic photo, you need to step back:</p>
<ul role="list">
<li><strong>Batthyány tér</strong> on the Buda bank, directly opposite. Best at sunset.</li>
<li><strong>Fisherman's Bastion</strong> and the Buda Castle walls for the view from above.</li>
<li><strong>From the Danube after dark.</strong> The building is lit up every evening, and the best way to see it is from a boat. I compare the options in my guides to the <a href="/best-budapest-river-cruises">best Budapest river cruises</a> and the <a href="/best-dinner-cruises-budapest">best dinner cruises</a>.</li>
</ul>
{figure("63557d47f9e1cc4261d5c439_Budapest-river-cruises-gallery-1.webp", "The Hungarian Parliament lit up at night, seen from a Danube river cruise", 888, 500, "The Parliament from a Danube cruise boat at night.")}

<h2 id="faq">Frequently asked questions</h2>
<div class="bpa-faq">
{"".join(f'<details class="bpa-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}
</div>

<h2 id="sources">Sources</h2>
<ul role="list" class="bpa-sources">
<li>Office of the National Assembly, <a href="https://parlament.jegymester.hu/docs/parlament/2021/hungarian_parliament_admission_fees_01012026.pdf" rel="noopener" target="_blank">Admission fees valid from 1 January 2026</a> (PDF).</li>
<li>Office of the National Assembly, <a href="https://parlament.jegymester.hu/eng/Index/" rel="noopener" target="_blank">visitor information: opening hours, tour languages and closures</a>.</li>
<li>My own visits to the Parliament.</li>
</ul>
"""

PAGE_CSS = """<style id="bpa-parliament-css">
.bpa-fig{margin:8px 0 24px !important;max-width:100% !important;width:100% !important}
.bpa-fig img.bpa-photo{width:100% !important;height:auto !important;border-radius:14px;display:block;border:1px solid #e2e8f0}
.bpa-fig figcaption{font-size:13px;color:#64748b;margin-top:8px;line-height:1.5}
.bpa-faq{border-top:1px solid #e2e8f0;margin:8px 0 24px}
.bpa-faq-item{border-bottom:1px solid #e2e8f0;padding:4px 0}
.bpa-faq-item summary{cursor:pointer;list-style:none;font-weight:700;font-size:17px;color:#0f172a;padding:14px 32px 14px 0;position:relative;line-height:1.4}
.bpa-faq-item summary::-webkit-details-marker{display:none}
.bpa-faq-item summary::after{content:"+";position:absolute;right:4px;top:10px;font-size:22px;font-weight:500;color:#785208}
.bpa-faq-item[open] summary::after{content:"\\2212"}
.bpa-faq-item p{margin:0 0 14px !important}
.bpa-sources li{font-size:15px !important}
.content-right_blog ol{padding-left:22px}
.content-right_blog ol li{font-size:18px;line-height:1.6;color:#334155;margin-bottom:8px}
.bpa-table td:not(:first-child),.bpa-table th:not(:first-child){text-align:left}
@media(max-width:520px){.bpa-table td,.bpa-table th{white-space:normal}}
</style>"""


def jsonld():
    article = {
        "@context": "https://schema.org", "@type": "Article",
        "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
        "headline": TITLE, "description": DESC,
        "image": "https://www.budapestadventures.com" + CDN + "650c1f90c059d2467627bad9_budapest-parliament-hero-image.webp",
        "author": {"@type": "Person", "name": "Adam Dimitrov", "url": "https://www.budapestadventures.com/about"},
        "publisher": {"@type": "Organization", "name": "Budapest Adventures",
                      "logo": {"@type": "ImageObject", "url": "https://www.budapestadventures.com/favicon.ico"}},
        "datePublished": "2022-11-14", "dateModified": UPDATED_ISO,
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.budapestadventures.com/"},
        {"@type": "ListItem", "position": 2, "name": "Budapest Parliament Tour", "item": URL}]}
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>'
                   for x in (article, faq, crumbs))


def style_block(src, ident):
    m = re.search(r'<style id="%s">.*?</style>' % re.escape(ident), src, re.S)
    assert m, ident
    return m.group(0)


def main():
    s = PAGE.read_text()
    stats = STATS.read_text()

    # 1) head meta
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE.replace('&', '&amp;')}</title>", s, count=1, flags=re.S)
    esc_t, esc_d = TITLE.replace("&", "&amp;"), DESC.replace("&", "&amp;")
    s = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{esc_d}" name="description"/>', s, count=1)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'<meta content="[^"]*" %s/>' % prop, f'<meta content="{esc_t}" {prop}/>', s, count=1)
    for prop in ('property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'<meta content="[^"]*" %s/>' % prop, f'<meta content="{esc_d}" {prop}/>', s, count=1)
    s = s.replace('<meta content="website" property="og:type"/>', '<meta content="article" property="og:type"/>', 1)

    # 2) styles: hero card + tiles/tables from the stats page, plus page CSS
    if 'id="ltt-hero-card-styles"' not in s:
        extra = style_block(stats, "ltt-hero-card-styles") + style_block(stats, "bpa-stats-charts")
        s = s.replace("</head>", extra + PAGE_CSS + "</head>", 1)

    # 3) body: hero + article, from the old hero image to the end of the blog section
    start = s.index('<div class="hero-image-wrapper">')
    # replace up to the matching close of the old <div class="blog-section">
    bs = s.index('<div class="blog-section">', start)
    depth, i = 0, bs
    for m in re.finditer(r"<(/?)div\b", s[bs:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            i = bs + m.end()
            break
    end = s.index(">", i) + 1
    toc = "".join(f'<a class="tocitem" href="#{i}">{t}</a>' for i, t in TOC)
    article = (HERO + '<div class="blog-section"><div class="container-26"><div class="blog-grid-2">'
               '<div class="content-left"><div class="stick-wrapper"><div class="title-small-3">Table of Contents</div>'
               f'<div class="toc" id="toc">{toc}</div></div></div>'
               '<div class="content-right_blog" id="content"><div class="w-layout-blockcontainer container w-container">'
               f'<div class="w-richtext">{BODY}</div></div></div></div></div></div>')
    s = s[:start] + article + s[end:]

    # 4) JSON-LD
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", s, flags=re.S)
    s = s.replace('<script defer="True" src="/bpa-tracking.js', jsonld() + '<script defer="True" src="/bpa-tracking.js', 1)

    assert "—" not in BODY + HERO + TITLE + DESC + "".join(q + a for q, a in FAQ), "em dash in copy"
    PAGE.write_text(s)
    print("wrote", PAGE, len(s))


if __name__ == "__main__":
    main()
