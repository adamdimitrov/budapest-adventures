#!/usr/bin/env python3
"""Build /legenda-cruise-tickets (EN test page for "attraction + tickets" keywords).

Layout (head assets, menu, footer, scripts) comes from the EN master
budapest-tourism-statistics.html; only the head meta, JSON-LD and the article
region (hero + body) are replaced. Facts below were checked on 14 Nov 2026 on
legenda.hu/en (prices, timetable, duna-bella, danube-legend,
candlelit-dinner-cruise, faq) and on the three GetYourGuide listings run by
Legenda Kft (t105769, t105820, t400893).

Run: python3 scripts/build_legenda_tickets.py && python3 scripts/sync_layout.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = "budapest-tourism-statistics.html"
OUT = "legenda-cruise-tickets.html"
SLUG = "legenda-cruise-tickets"
URL = f"https://www.budapestadventures.com/{SLUG}"
CHECKED = "14 November 2026"
CHECKED_SHORT = "Nov 14, 2026"
DATE_ISO = "2026-11-14"

TITLE = "Legenda Cruise Tickets Budapest 2026: Prices, Times & Where to Buy"
DESC = ("Legenda cruise tickets cost €20 (day), €25 (evening) and €110 (candlelit dinner). "
        "Official site vs GetYourGuide compared: same price, different cancellation and "
        "discount rules. Timetable, pier and what is included.")

LEG = "?partner=38585"
LEG_HOME = "https://legenda.hu/en" + LEG
LEG_BELLA = "https://legenda.hu/en/duna-bella" + LEG
LEG_LEGEND = "https://legenda.hu/en/danube-legend" + LEG
LEG_DINNER = "https://legenda.hu/en/candlelit-dinner-cruise" + LEG


def gyg(path, cmp):
    return (f"https://www.getyourguide.com/budapest-l29/{path}/?partner_id=YS414AJ"
            f"&amp;utm_medium=online_publisher&amp;cmp=legenda-tickets-{cmp}&amp;mkt_cmp=true")


GYG_BELLA = gyg("budapest-1-hour-daytime-sightseeing-cruise-t105769", "daytime")
GYG_LEGEND = gyg("budapest-1-hour-evening-sightseeing-cruise-with-drink-t105820", "evening")
GYG_DINNER = gyg("budapest-candlelit-dinner-river-cruise-with-live-music-t400893", "dinner")

IMG = "/assets/cdn/60e43c7d6d05b671dff0dc1a/"
PHOTOS = [
    ("63b85c19bd509e80e2cfbd71_Budapest-river-cruises-legenda-1.webp", "Legenda boat on the Danube in Budapest"),
    ("63b85889ad92774aa6d9b7ca_Budapest-river-cruises-legenda-5.webp", "Deck view from a Legenda sightseeing cruise"),
    ("63b8588eb2b66207c4939d92_Budapest-river-cruises-legenda-10.webp", "Parliament seen from a Legenda cruise"),
]

FAQ = [
    ("How much is a Legenda cruise ticket in Budapest?",
     "An adult ticket costs €20 for the daytime Duna Bella cruise, €25 for the evening Danube Legend "
     "cruise and €110 for the Candlelit Dinner Cruise. Prices are from legenda.hu, checked on " + CHECKED + "."),
    ("Is it cheaper to buy Legenda tickets on GetYourGuide?",
     "No. GetYourGuide sells the same three Legenda cruises at the same adult price as legenda.hu: "
     "€20, €25 and €110. The difference is the terms: GetYourGuide gives a full refund if you cancel "
     "up to 24 hours before, and you can reserve now and pay later."),
    ("Can I cancel or change a Legenda ticket?",
     "On GetYourGuide you can cancel up to 24 hours in advance for a full refund. For tickets bought "
     "from Legenda directly, its FAQ says tickets may be moved to another day and time, subject to "
     "availability, but only in person at the Legenda pier, not online or by phone."),
    ("Do children ride free on Legenda cruises?",
     "Yes, on the sightseeing cruises children aged 0 to 9 ride free. Children aged 10 to 14 pay €14 "
     "(daytime) or €17.50 (evening), and students with a valid student ID pay €18 or €22.50. "
     "On the dinner cruise the Kid's Dinner Package (3 to 12 years) costs €84."),
    ("Do I need to book a Legenda cruise in advance?",
     "Legenda says booking is not required, but it strongly recommends reserving if you know your date "
     "and time. Book ahead for the dinner cruise, which sails once a night."),
    ("Where does the Legenda cruise depart from?",
     "From Dock 7 at Jane Haining rakpart, 1052 Budapest, on the Pest side next to Vigadó tér. "
     "The nearest metro is Vörösmarty tér on the M1 (yellow) line."),
]


def faq_html():
    out = []
    for q, a in FAQ:
        out.append(f'<details class="lt-faq"><summary>{q}</summary><p>{a}</p></details>')
    return "".join(out)


CSS = """<style id="bpa-tickets-css">
.lt-answer{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:14px;padding:20px 22px;margin:0 0 24px}
.lt-answer p{margin:0 0 12px}
.lt-answer .lt-kicker{display:block;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#047857;margin-bottom:6px}
.lt-notice{background:#fff7ed;border:1px solid #fed7aa;border-radius:12px;padding:14px 18px;margin:0 0 24px;font-size:15px;line-height:1.55;color:#7c2d12}
.lt-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}
.lt-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:10px;font-weight:700;font-size:15px;text-decoration:none!important;box-sizing:border-box;white-space:nowrap}
.lt-btn-gold{background:#dfa732;color:#0a192f!important}.lt-btn-gold:hover{background:#b88214}
.lt-btn-out{background:#fff;border:1.5px solid #cbd5e1;color:#0a192f!important}.lt-btn-out:hover{border-color:#0a192f}
.lt-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e2e8f0;border-radius:14px;margin:0 0 12px;background:#fff}
.lt-table{width:100%;border-collapse:collapse;min-width:640px;font-size:15px}
.lt-table th{background:#f1f5f9;text-align:left;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#475569;padding:12px 14px;border-bottom:1px solid #e2e8f0}
.lt-table td{padding:14px;border-bottom:1px solid #e2e8f0;vertical-align:middle;color:#0f172a}
.lt-table tr:last-child td{border-bottom:0}
.lt-table small{display:block;color:#64748b;font-size:13px;margin-top:2px}
.lt-same{display:inline-block;background:#ecfdf5;color:#047857;font-weight:700;border-radius:8px;padding:3px 9px}
.lt-note{font-size:13px;color:#64748b;margin:0 0 28px}
.lt-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:0 0 28px}
.lt-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:8px}
.lt-card.lt-pick{border:2px solid #dfa732}
.lt-card h3{margin:0!important;font-size:19px!important;line-height:1.3!important}
.lt-card p{margin:0!important;font-size:15px;line-height:1.55;color:#334155}
.lt-card .lt-tag{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#0369a1}
.lt-card .lt-btns{margin-top:auto;padding-top:8px}
.lt-facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:0 0 28px}
.lt-fact{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px}
.lt-fact b{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#64748b;margin-bottom:4px}
.lt-fact span{display:block;font-size:15px;line-height:1.5;color:#0f172a}
.lt-photos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0 0 28px}
.lt-photos img{width:100%;height:180px;object-fit:cover;border-radius:12px;display:block}
.lt-faq{border:1px solid #e2e8f0;border-radius:12px;background:#fff;padding:0 18px;margin:0 0 10px}
.lt-faq summary{cursor:pointer;font-weight:600;font-size:16px;padding:16px 0;color:#0f172a}
.lt-faq p{margin:0 0 16px!important;line-height:1.6}
.lt-hub{background:#0a192f;color:#fff;border-radius:14px;padding:22px;margin:28px 0 8px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between}
.lt-hub p{margin:0!important;color:#e2e8f0;flex:999 1 320px;min-width:0}
.lt-hub strong{color:#fff}
@media (max-width:600px){.lt-photos{grid-template-columns:1fr 1fr}.lt-photos img{height:130px}.lt-photos img:nth-child(3){display:none}.lt-btn{white-space:normal;text-align:center}}
</style>"""


TOC = [
    ("legenda-ticket-prices", "Legenda ticket prices (2026)"),
    ("official-site-vs-getyourguide", "Official site vs GetYourGuide"),
    ("student-and-child-prices", "Student and child prices"),
    ("which-legenda-ticket", "Which Legenda ticket to buy"),
    ("timetable", "Timetable this season"),
    ("what-is-included", "What each ticket includes"),
    ("pier-and-directions", "Pier and directions"),
    ("faq", "FAQ"),
]


def body():
    toc = "".join(f'<a class="tocitem" href="#{i}">{t}</a>' for i, t in TOC)
    photos = "".join(f'<img src="{IMG}{f}" alt="{a}" width="600" height="400" loading="lazy" decoding="async">'
                     for f, a in PHOTOS)
    return f"""<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
<a href="/">Home</a>
<span class="ltt-bc-sep">›</span>
<a href="/best-budapest-river-cruises">River Cruises</a>
<span class="ltt-bc-sep">›</span>
<span class="ltt-bc-current">Legenda Cruise Tickets</span>
</nav>
<span class="ltt-hero-kicker-badge">Prices checked {CHECKED}</span>
</div>
<h1 class="ltt-editorial-h1">
      Legenda Cruise Tickets Budapest 2026 <span class="ltt-h1-muted">(Prices, Times &amp; Where to Buy)</span>
</h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap">
<img alt="Adam Dimitrov" class="ltt-author-avatar" height="48" loading="eager" src="/assets/adam-dimitrov.webp" width="48"/>
</div>
<div class="ltt-author-meta">
<div class="ltt-author-line">
            By <a href="/about" target="_blank">Adam Dimitrov</a> · Founder &amp; Local Budapest Guide
          </div>
<div class="ltt-author-role">Official legenda.hu prices vs GetYourGuide · 3 cruises compared</div>
</div>
</div>
<div class="ltt-trust-pills">
<span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: {CHECKED_SHORT}</span>
</div>
</div>
<div class="ltt-lead-copy">
<div class="lt-answer">
<span class="lt-kicker">Short answer</span>
<p>A Legenda adult ticket costs <strong>€20</strong> for the daytime Duna Bella cruise, <strong>€25</strong> for the evening Danube Legend cruise and <strong>€110</strong> for the Candlelit Dinner Cruise. GetYourGuide charges exactly the same.</p>
<p>Buy on <strong>GetYourGuide</strong> if you want free cancellation up to 24 hours before. Buy on <strong>legenda.hu</strong> if you are a student or have kids aged 10 to 14, because the official site lists lower prices for them.</p>
<div class="lt-btns">
<a class="lt-btn lt-btn-gold" href="{GYG_LEGEND}" rel="sponsored noopener" target="_blank">Evening cruise on GetYourGuide</a>
<a class="lt-btn lt-btn-out" href="{LEG_HOME}" rel="sponsored noopener" target="_blank">All tickets on legenda.hu</a>
</div>
</div>
</div>
</div>
</div>
{CSS}
<div class="blog-section"><div class="container-26"><div class="blog-grid-2"><div class="content-left"><div class="stick-wrapper"><div class="title-small-3">Table of Contents</div><div class="toc" id="toc">{toc}</div></div></div><div class="content-right_blog" id="content"><div class="w-layout-blockcontainer container w-container"><div class="w-richtext">
<p class="lt-notice"><strong>Route change right now:</strong> because of the very low Danube water level, Legenda's daytime cruises cannot dock at Margaret Island and currently follow the evening route. Legenda posted this notice on its homepage; it was still up on {CHECKED}.</p>

<h2 id="legenda-ticket-prices">Legenda ticket prices (2026)</h2>
<p>Legenda City Cruises runs three cruises from the same pier in central Pest. These are the adult prices on the two places you can book them online.</p>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th>Cruise</th><th>legenda.hu</th><th>GetYourGuide</th><th>GetYourGuide rating</th><th></th></tr></thead>
<tbody>
<tr><td><strong>Duna Bella</strong> (daytime)<small>1h10 · audio guide · 1 drink + lemonade</small></td><td>€20</td><td>€20 <span class="lt-same">same</span></td><td>4.6 (4,428)</td><td><a class="lt-btn lt-btn-gold" href="{GYG_BELLA}" rel="sponsored noopener" target="_blank">Book</a></td></tr>
<tr><td><strong>Danube Legend</strong> (evening)<small>1 hour · film and audio guide · 1 drink</small></td><td>€25</td><td>€25 <span class="lt-same">same</span></td><td>4.5 (10,998)</td><td><a class="lt-btn lt-btn-gold" href="{GYG_LEGEND}" rel="sponsored noopener" target="_blank">Book</a></td></tr>
<tr><td><strong>Candlelit Dinner Cruise</strong><small>2h30 · 4-course à la carte · live music</small></td><td>€110</td><td>€110 <span class="lt-same">same</span></td><td>4.7 (2,432)</td><td><a class="lt-btn lt-btn-gold" href="{GYG_DINNER}" rel="sponsored noopener" target="_blank">Book</a></td></tr>
</tbody></table></div>
<p class="lt-note">Adult prices from legenda.hu/en/prices and the three GetYourGuide listings run by Legenda Kft, checked {CHECKED}. We may earn a commission from either site, at no extra cost to you.</p>

<h2 id="official-site-vs-getyourguide">Official site vs GetYourGuide: where to buy</h2>
<p>The price is the same, so the choice comes down to the terms.</p>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th></th><th>legenda.hu (official)</th><th>GetYourGuide</th></tr></thead>
<tbody>
<tr><td><strong>Adult price</strong></td><td>€20 / €25 / €110</td><td>€20 / €25 / €110</td></tr>
<tr><td><strong>Cancellation</strong></td><td>Ticket can be moved to another day and time if there is space, in person at the pier only</td><td>Full refund up to 24 hours before</td></tr>
<tr><td><strong>Pay later</strong></td><td>Not offered</td><td>Reserve now, pay later</td></tr>
<tr><td><strong>Student and child prices</strong></td><td>Listed: students €18 / €22.50, kids 10 to 14 €14 / €17.50, under 10 free</td><td>See ticket options at checkout</td></tr>
<tr><td><strong>Best for</strong></td><td>Students and families with kids 10 to 14</td><td>Anyone whose plans might change</td></tr>
</tbody></table></div>
<p class="lt-note">Cancellation terms from Legenda's FAQ page and the GetYourGuide listings, {CHECKED}.</p>

<h2 id="student-and-child-prices">Student and child prices</h2>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th>Ticket</th><th>Duna Bella (day)</th><th>Danube Legend (evening)</th></tr></thead>
<tbody>
<tr><td>Adult</td><td>€20</td><td>€25</td></tr>
<tr><td>Student (valid ID at boarding)</td><td>€18</td><td>€22.50</td></tr>
<tr><td>Child 10 to 14</td><td>€14</td><td>€17.50</td></tr>
<tr><td>Child 0 to 9</td><td>Free</td><td>Free</td></tr>
</tbody></table></div>
<p class="lt-note">Candlelit Dinner Cruise: Exclusive Dinner Package €110, Kid's Dinner Package (3 to 12 years) €84. Source: legenda.hu/en/prices, {CHECKED}. Groups of 20 or more get discounted rates; see our <a href="/budapest-river-cruise-group-booking">group cruise booking</a> page.</p>

<div class="lt-photos">{photos}</div>

<h2 id="which-legenda-ticket">Which Legenda ticket should you buy?</h2>
<div class="lt-cards">
<div class="lt-card"><span class="lt-tag">Daytime · €20</span><h3>Duna Bella</h3><p>A 1h10 daytime loop with a drink and a glass of Duna Bella lemonade. When the water is high enough you can get off for 45 minutes on Margaret Island and take a later boat back.</p><div class="lt-btns"><a class="lt-btn lt-btn-gold" href="{GYG_BELLA}" rel="sponsored noopener" target="_blank">€20 on GetYourGuide</a></div></div>
<div class="lt-card lt-pick"><span class="lt-tag">Evening · €25 · most reviewed</span><h3>Danube Legend</h3><p>One hour after dark past the lit-up Parliament and Buda Castle, with a film and audio guide in 30 languages and one drink. Boats leave every 20 minutes, so it is easy to fit in.</p><div class="lt-btns"><a class="lt-btn lt-btn-gold" href="{GYG_LEGEND}" rel="sponsored noopener" target="_blank">€25 on GetYourGuide</a></div></div>
<div class="lt-card"><span class="lt-tag">Dinner · €110</span><h3>Candlelit Dinner Cruise</h3><p>2h30 on the glass-roofed panorama boat with a 4-course à la carte dinner, welcome drink and live music. Other drinks are paid on board. Read our <a href="/best-dinner-cruises-budapest/candlelit-dinner-cruise-budapest">candlelit dinner review</a>.</p><div class="lt-btns"><a class="lt-btn lt-btn-gold" href="{GYG_DINNER}" rel="sponsored noopener" target="_blank">€110 on GetYourGuide</a></div></div>
</div>

<h2 id="timetable">Legenda timetable this season</h2>
<div class="lt-scroll"><table class="lt-table">
<thead><tr><th>Dates</th><th>Duna Bella (day)</th><th>Danube Legend (evening)</th><th>Dinner cruise</th></tr></thead>
<tbody>
<tr><td>25 Oct to 22 Nov 2026</td><td>11:00, 12:30, 14:00, 15:30</td><td>Every 20 min, 16:20 to 21:00</td><td>19:00</td></tr>
<tr><td>23 Nov to 31 Dec 2026</td><td>11:00, 12:30, 14:00, 15:30</td><td>15:40, then every 20 min 16:20 to 21:00</td><td>19:00</td></tr>
</tbody></table></div>
<p class="lt-note">The 15:30 daytime sailing never stops at Margaret Island. On 24 December only the 11:00, 12:30, 14:00 and 15:30 sailings run. In summer (22 May to 23 July) daytime boats leave every 45 minutes from 10:15 and the dinner cruise leaves at 19:45. Source: legenda.hu/en/timetable, {CHECKED}.</p>

<h2 id="what-is-included">What each ticket includes</h2>
<div class="lt-facts">
<div class="lt-fact"><b>Duna Bella (€20)</b><span>1h10 daytime cruise, 30-language audio guide, 1 drink (champagne, wine, beer, soft drink or water), 1 Duna Bella lemonade, free Wi-Fi. Optional 45 min on Margaret Island when water levels allow.</span></div>
<div class="lt-fact"><b>Danube Legend (€25)</b><span>1-hour evening cruise, film and audio guide in 30 languages, 1 drink (champagne, wine, beer, soft drink or water), free Wi-Fi.</span></div>
<div class="lt-fact"><b>Candlelit Dinner (€110)</b><span>2h30 cruise, welcome drink, live music, 4-course à la carte dinner (kids: 3-course menu). Other drinks are paid on board.</span></div>
</div>

<h2 id="pier-and-directions">Pier and directions</h2>
<div class="lt-facts">
<div class="lt-fact"><b>Pier</b><span>Dock 7, Jane Haining rakpart, 1052 Budapest (Pest side, below Vigadó tér). <a href="https://maps.google.com/?q=Legenda+City+Cruises+Dock+7+Budapest" rel="noopener" target="_blank">Open in Maps</a></span></div>
<div class="lt-fact"><b>Metro</b><span>M1 (yellow) to Vörösmarty tér. Walk to Vigadó tér, go down the stairs, cross at the lights, turn left and walk about 50 m.</span></div>
<div class="lt-fact"><b>Parking</b><span>A few spaces on the quay, paid before 6 pm.</span></div>
</div>

<h2 id="faq">Legenda tickets: FAQ</h2>
{faq_html()}

<div class="lt-hub"><p><strong>Not sure Legenda is the right boat?</strong> We compared 10 Budapest river cruises side by side: price, drinks, route and ratings.</p><a class="lt-btn lt-btn-gold" href="/best-budapest-river-cruises">Compare all river cruises</a></div>
</div></div></div></div></div></div>"""


def jsonld():
    offers = [
        ("Duna Bella daytime sightseeing cruise", 20),
        ("Danube Legend evening sightseeing cruise", 25),
        ("Candlelit Dinner Cruise (Exclusive Dinner Package)", 110),
    ]
    graph = [
        {"@type": "Article", "headline": TITLE, "description": DESC, "dateModified": DATE_ISO,
         "datePublished": DATE_ISO, "inLanguage": "en", "mainEntityOfPage": URL,
         "author": {"@type": "Person", "name": "Adam Dimitrov", "url": "https://www.budapestadventures.com/about"},
         "publisher": {"@type": "Organization", "name": "Budapest Adventures",
                       "url": "https://www.budapestadventures.com"}},
        {"@type": "TouristAttraction", "name": "Legenda City Cruises", "url": "https://legenda.hu/en",
         "address": {"@type": "PostalAddress", "streetAddress": "Jane Haining rakpart, Dock 7",
                     "postalCode": "1052", "addressLocality": "Budapest", "addressCountry": "HU"},
         "makesOffer": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "EUR",
                         "url": "https://legenda.hu/en/prices"} for n, p in offers]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.budapestadventures.com/"},
            {"@type": "ListItem", "position": 2, "name": "River Cruises",
             "item": "https://www.budapestadventures.com/best-budapest-river-cruises"},
            {"@type": "ListItem", "position": 3, "name": "Legenda Cruise Tickets", "item": URL}]},
    ]
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
            + "</script>")


def main():
    s = open(os.path.join(ROOT, MASTER), encoding="utf-8").read()

    # head meta
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE.replace('&', '&amp;')}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta content="[^"]*" (name="description"|property="og:description"|name="twitter:description")/>',
               lambda m: f'<meta content="{DESC}" {m.group(1)}/>', s)
    s = re.sub(r'<meta content="[^"]*" (property="og:title"|name="twitter:title")/>',
               lambda m: f'<meta content="{TITLE.replace("&", "&amp;")}" {m.group(1)}/>', s)
    s = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{URL}" property="og:url"/>', s)
    # EN only: drop the master's hreflang set, keep a self canonical
    s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>\s*', "", s)
    s = re.sub(r'<link href="[^"]*" rel="canonical"/>',
               f'<link href="{URL}" hreflang="en" rel="alternate"/>'
               f'<link href="{URL}" hreflang="x-default" rel="alternate"/>'
               f'<link href="{URL}" rel="canonical"/>', s, count=1)

    # JSON-LD
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: jsonld(), s, count=1, flags=re.S)
    assert s.count("application/ld+json") == 1

    # article region
    a = s.find('<div class="ltt-hero-wrap">')
    b = s.find('<style id="bpa-new-footer"')
    assert 0 < a < b
    s = s[:a] + body() + s[b:]

    assert "—" not in body() and "—" not in TITLE and "—" not in DESC
    with open(os.path.join(ROOT, OUT), "w", encoding="utf-8") as fh:
        fh.write(s)
    print("wrote", OUT, len(s))


if __name__ == "__main__":
    main()
