#!/usr/bin/env python3
"""Build /szechenyi-baths-budapest (EN only) from scripts/szechenyi_baths_data.py.

The page shell, CSS and card/details renderers come from the thermal baths hub
(thermal-baths-budapest.html + scripts/build_thermal_baths_2026.py). Re-runnable:
    python3 scripts/build_szechenyi_baths_page.py
"""
import json
import os
import re
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import szechenyi_baths_data as S  # noqa: E402
import bath_hub_nav  # noqa: E402
import bath_copy_rules  # noqa: E402

# Load the hub builder's renderers without its "already rebuilt" guard.
_path = os.path.join(HERE, "build_thermal_baths_2026.py")
_src = open(_path, encoding="utf-8").read().replace('if \'id="item-2-rudas"\' in SRC["page"]:', "if False:")
B = types.ModuleType("thermal_builder")
B.__file__ = _path
exec(compile(_src, _path, "exec"), B.__dict__)
B.D = S

ROOT = B.ROOT
SITE = B.SITE
SLUG = "szechenyi-baths-budapest"
URL = SITE + "/" + SLUG
OUT = os.path.join(ROOT, SLUG + ".html")
TODAY = "2026-11-15"
CARDS = S.CARDS
N = len(CARDS)
must_sub, swap_block, no_em_dash, book_url, AFF_REL = B.must_sub, B.swap_block, B.no_em_dash, B.book_url, B.AFF_REL

TITLE = "Széchenyi Baths Tickets 2026: 5 Options Compared (Prices, Sparty)"
DESC = ("Széchenyi Baths tickets compared: day ticket from €39, locker vs cabin, Sparty night party, Beer Spa and "
        "Palm House VIP. Prices, hours and who should book which, updated 15 Nov 2026.")
H1 = 'Széchenyi Baths Tickets 2026 <span class="ltt-h1-muted">(5 Options Compared)</span>'


def gyg(key, placement):
    c = next(c for c in CARDS if c["key"] == key)
    return book_url(c, placement)


RUDAS = (', or see <a href="/rudas-baths-budapest">Rudas Baths</a> for an Ottoman Turkish bath with a rooftop pool'
         if bath_hub_nav.live('/rudas-baths-budapest') else ', which compares Széchenyi with Rudas, Lukács and the local baths')
SPARTY_MORE = (' For dress code, what to bring and every ticket type, read the full <a href="/sparty-budapest">Sparty Budapest guide</a>.'
               if bath_hub_nav.live('/sparty-budapest') else '')
LEAD = f'''<div class="ltt-lead-copy">
<p>Most visitors pay more than they need to at Széchenyi. The same locker ticket is <strong>€39 if you enter before 9:00</strong> and €46 after, a private cabin costs only <strong>€4 more</strong>, and Sparty, the Saturday night pool party, is a different ticket that <strong>cannot be refunded</strong>.</p>
<p>I have soaked here myself, then compared the <strong>5 Széchenyi tickets worth booking</strong> side by side: what each one includes, desk vs online price, locker or cabin, and who should skip it. Prices and opening hours are up to date as of 15 November 2026.</p>
<p>Still choosing a bath? Start with the <a href="/thermal-baths-budapest">Budapest thermal baths guide</a>{RUDAS}.</p>
</div>'''

PILLS = f'''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems('all', this)" type="button">All ({N})</button>
<button class="ltt-tab-btn" data-cat="day" onclick="lttFilterItems('day', this)" type="button">Day Tickets (2)</button>
<button class="ltt-tab-btn" data-cat="night" onclick="lttFilterItems('night', this)" type="button">Night Party (1)</button>
<button class="ltt-tab-btn" data-cat="upgrade" onclick="lttFilterItems('upgrade', this)" type="button">Upgrades (2)</button>
</div>'''

GUIDE = f'''<div class="w-richtext bpa-wt-guide">
<h2 id="which-szechenyi-ticket">Which Széchenyi Ticket Should You Book?</h2>
<ul>
<li><strong>Cheapest booked ticket, early riser:</strong> <a href="#item-1-day-ticket">Morning Pass</a> (€39 with locker, entry 7:00 to 9:00, Mon to Thu).</li>
<li><strong>A normal day at the bath:</strong> <a href="#item-1-day-ticket">Weekday Pass</a> (€46 with locker, €50 with a private cabin).</li>
<li><strong>Saturday night out:</strong> <a href="#item-2-sparty">Sparty</a> (from €73, 21:30 to 2:00, 18+, non-refundable).</li>
<li><strong>Friends, a birthday or a stag weekend:</strong> <a href="#item-3-beer-spa">Beer Spa combo</a> (€125, bath day ticket plus 45 minutes in a beer tub with your own tap).</li>
<li><strong>A slow, pampered day with nothing to pack:</strong> <a href="#item-4-palm-house">Palm House VIP Pass</a> (€110, robe, towel, cabin, lounge and a cocktail).</li>
<li><strong>Weekend or holiday afternoon, no patience for queues:</strong> <a href="#item-5-fast-track">Fast Track with locker</a> (from €59, separate entrance).</li>
</ul>
<h2 id="szechenyi-desk-vs-online">Széchenyi Desk Price vs Online Ticket</h2>
<p>At the desk, a 2026 locker ticket costs <strong>13,200 HUF Monday to Thursday</strong> and <strong>14,800 HUF Friday to Sunday</strong> (15,800 HUF in peak periods). Entry before 9:00 is 10,500 HUF on weekdays and 11,800 HUF at weekends, and a cabin adds 1,000 HUF.</p>
<p>Online you pay a little more (€46 for the weekday locker ticket), and in return you get <strong>free cancellation up to 24 hours before</strong>, pay-later booking and a QR code that goes straight to the turnstile machines instead of the cashier queue. If you are already standing outside on a quiet weekday, the desk is cheaper. If you are planning ahead, or going at the weekend, book.</p>
<h2 id="sparty-szechenyi-night-party">Sparty: Széchenyi's Saturday Night Pool Party</h2>
<p>Every Saturday from <strong>21:30 to 2:00</strong>, the outdoor pools turn into a club: DJs, lasers, fire shows and circus acts around 34 to 38 °C water. Tickets start at <strong>€73 with a locker</strong>; the €100 premium ticket adds two drink coupons, which buy roughly one cocktail. It is 18+ only and non-refundable, and the bars take only the cash-loaded SpartyPay card.</p>
<p><a href="{gyg("sparty", "guide")}" rel="{AFF_REL}" target="_blank"><strong>Check Sparty dates and tickets →</strong></a>{SPARTY_MORE}</p>
</div>'''

KNOW = '''<h2 id="szechenyi-know-before-you-go">Széchenyi Baths: Know Before You Go</h2><div class="w-richtext">
<h3>Opening Hours</h3><p>Monday to Thursday 7:00 to 20:00, Friday 7:00 to 22:00, Saturday and Sunday 8:00 to 20:00. On 8 December 2026 the bath closes at 16:00; from 18 December 2026 to 6 January 2027 it opens at 8:00, and on 25 and 26 December and 1 January at 10:00.</p>
<h3>Best Time to Go</h3><p>Weekday mornings before 10:00 are the quietest, and the €39 Morning Pass makes them the cheapest too. Late morning to late afternoon, and all weekend, the outdoor pools get crowded. Friday evening, when the bath stays open until 22:00, is the calm way to see the pools steaming in the dark.</p>
<h3>Locker or Cabin?</h3><p>A locker sits in a shared, gender-separated changing room and opens with your wristband. A cabin is a lockable booth for one or two people where you change and leave everything. It costs €4 more online or 1,000 HUF more at the desk: worth it for couples and anyone with a bag.</p>
<h3>What to Bring</h3><p>Swimsuit, towel and flip-flops (no ticket except the Palm House pass includes a towel). If you forget them, the desk sells a towel for 6,900 HUF, slippers for 4,200 HUF and a swim cap for 2,100 HUF. A swim cap is needed only in the lap pool.</p>
<h3>Getting There</h3><p>Take metro M1, the yellow line from Vörösmarty tér, to <strong>Széchenyi fürdő</strong>. Day tickets enter on the swimming-pool side at Állatkerti körút 9-11; the Beer Spa reception is through the main entrance on Kós Károly sétány.</p>
<h3>Age Limits</h3><p>The booked day tickets are not suitable for children under 14, and Sparty and the Beer Spa are 18+. For a family day with younger kids, see Palatinus in our <a href="/thermal-baths-budapest">thermal baths guide</a>.</p>
</div>
<h2 id="how-we-compared-szechenyi-tickets">How We Compared Széchenyi Tickets</h2><div class="w-richtext">
<p>I visited Széchenyi in person, and most of the photos on this page are my own. Opening hours, desk prices, pool temperatures and rules come from the official Széchenyi site, checked on 14 November 2026. Ticket prices, inclusions, cancellation terms and ratings were checked on the live booking pages on 15 November 2026, using Thursday 19 November for day tickets and Saturday 21 November for Sparty.</p>
<p>Tickets are ranked by how many visitors they suit and what the price buys over the cheapest way in. Ratings are the average of each ticket's own reviews.</p>
</div>'''

FAQ = [
    ("How much is a Széchenyi Baths ticket?",
     "At the desk in 2026, a locker ticket is 13,200 HUF Monday to Thursday and 14,800 HUF Friday to Sunday. Booked online, the Morning Pass is €39 (entry 7:00 to 9:00), the Weekday Pass €46 with a locker and €50 with a private cabin."),
    ("Should I book Széchenyi tickets in advance?",
     "For weekends, holidays and Sparty, yes. A booked ticket skips the cashier queue, and the day tickets can be cancelled for free up to 24 hours before. On a quiet weekday the desk is cheaper."),
    ("What is the difference between a locker and a cabin at Széchenyi?",
     "A locker is in a shared, gender-separated changing room. A cabin is a private lockable booth for one or two people. The cabin costs €4 more online or 1,000 HUF more at the desk."),
    ("What time is Sparty and how much does it cost?",
     "Sparty runs every Saturday from 21:30 to 2:00, with last entry at 1:00. Tickets start at €73 with a locker, or €100 with two drink coupons. It is 18+ and non-refundable."),
    ("What are Széchenyi's opening hours?",
     "Monday to Thursday 7:00 to 20:00, Friday 7:00 to 22:00, Saturday and Sunday 8:00 to 20:00. Holiday hours differ in December and on 1 January."),
    ("Do I need to bring a towel to Széchenyi?",
     "Yes. Towels and flip-flops are not included in standard tickets. The desk sells a towel for 6,900 HUF and slippers for 4,200 HUF; the Palm House pass includes a robe, towel and slippers."),
    ("Is Széchenyi or Rudas better?",
     "Széchenyi for big outdoor pools, Friday evenings and Sparty. Rudas for an Ottoman Turkish bath and a rooftop pool over the Danube, plus weekend night bathing."),
]


def faq_html():
    B.FAQ = FAQ
    return B.faq_html()


def jsonld(page):
    i = page.find('id="ltt-schema-jsonld"')
    a = page.find(">", i) + 1
    b = page.find("</script>", a)
    data = json.loads(page[a:b])
    items = []
    for pos, c in enumerate(CARDS, 1):
        avg, tot = B.wavg(c["ratings"])
        prod = {
            "@type": "Product",
            "name": c["title"],
            "description": "%s: %s" % (B.strip_tags(c["rank"]).split(" ", 2)[-1], B.strip_tags(c["pick"])),
            "brand": {"@type": "Organization", "name": "Széchenyi Thermal Bath"},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                "worstRating": "1", "reviewCount": str(tot)},
            "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "price": c["price"],
                       "priceCurrency": "EUR", "url": book_url(c, "schema").replace("&amp;", "&")},
        }
        items.append({"@type": "ListItem", "position": pos, "url": "%s#%s" % (URL, c["anchor"]), "item": prod})
    graph = []
    for node in data["@graph"]:
        t = node.get("@type")
        if t == "Article":
            node["@id"] = URL + "#article"
            node["mainEntityOfPage"] = {"@type": "WebPage", "@id": URL}
            node["url"] = URL
            node["headline"] = TITLE
            node["description"] = DESC
            node["datePublished"] = TODAY
            node["dateModified"] = TODAY
            node.pop("hasPart", None)
            node["image"] = [SITE + S.P["hero"]]
            node["isPartOf"] = {"@type": "WebPage", "@id": SITE + "/thermal-baths-budapest", "name": "Budapest thermal baths guide"}
            node["mainEntity"] = {"@type": "ItemList", "name": TITLE, "description": DESC,
                                  "numberOfItems": N, "itemListElement": items}
            graph.append(node)
        elif t == "BreadcrumbList":
            node["@id"] = URL + "#breadcrumb"
            node["itemListElement"] = [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Thermal Baths in Budapest", "item": SITE + "/thermal-baths-budapest"},
                {"@type": "ListItem", "position": 3, "name": "Széchenyi Baths Tickets", "item": URL}]
            graph.append(node)
        elif t != "FAQPage":
            graph.append(node)
    graph.append({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    data["@graph"] = graph
    out = json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")
    return page[:a] + out + page[b:]


def main():
    page = B.SRC["page"]
    page = bath_hub_nav.strip(page)
    page = re.sub(r'<style id="bpa-hub-child-css">.*?</style>\n?', "", page, flags=re.S)

    deck = no_em_dash("\n".join(B.deck_html(i, c) for i, c in enumerate(CARDS, 1)))
    dets = no_em_dash("".join(B.details_html(i, c) for i, c in enumerate(CARDS, 1)))
    cs = B.all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = B.all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]

    # head
    page = must_sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, page, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (TITLE, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (DESC, prop), page)
    for prop in ('property="og:image"', 'name="twitter:image"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s%s" %s/>' % (SITE, S.P["hero"], prop), page)
    page = must_sub(r'<link href="[^"]*" rel="canonical"/>', '<link href="%s" rel="canonical"/>' % URL, page)
    page = must_sub(r'<meta content="[^"]*" property="og:url"/>', '<meta content="%s" property="og:url"/>' % URL, page)
    page = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", page)
    page = page.replace('<link href="%s" rel="canonical"/>' % URL,
                        '<link href="%s" rel="canonical"/><link href="%s" hreflang="en" rel="alternate"/>'
                        '<link href="%s" hreflang="x-default" rel="alternate"/>' % (URL, URL, URL), 1)
    for prop in ("article:modified_time", "article:published_time"):
        page = re.sub(r'(<meta content=")[^"]*(" property="%s"/>)' % prop, r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    if 'id="bpa-lang-js"' not in page:
        page = page.replace("</body>", B.REF_JS + "\n</body>", 1)

    # hero
    page = must_sub(r'<span class="ltt-bc-current">[^<]*</span>',
                    '<a href="/thermal-baths-budapest">Thermal Baths</a>\n<span class="ltt-bc-sep">›</span>\n'
                    '<span class="ltt-bc-current">Széchenyi Baths Tickets</span>', page)
    page = must_sub(r'<span class="ltt-hero-kicker-badge">[^<]*</span>',
                    '<span class="ltt-hero-kicker-badge">2026 Ticket Comparison</span>', page)
    page = must_sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)', r'\1\n      %s\n\2' % H1, page, flags=re.S)
    page = must_sub(r'<div class="ltt-author-role">[^<]*</div>',
                    '<div class="ltt-author-role">Széchenyi Visited in Person • 5 Tickets Compared • Prices Checked 15 Nov 2026</div>', page)
    page = must_sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 15, 2026<", page)
    page = swap_block(page, r'<div class="ltt-lead-copy">', LEAD)
    page = swap_block(page, r'<div class="ltt-integrated-pills">', PILLS)
    page = must_sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                    r"\1Detailed Breakdown: %d Széchenyi Tickets Compared\2" % N, page)
    page = must_sub(r'(<p class="bpa-breakdown-sub">)[^<]*(</p>)',
                    r"\1Széchenyi visited in person • All reviews open by default • Click to collapse/expand\2", page)

    # body: hub nav + ticket guide replace the hub's map / why-visit prose
    a = page.find('<div class="container w-container"><div class="w-richtext"><p>')
    b = page.find('<div class="bpa-breakdown-top-bar"')
    assert 0 < a < b, (a, b)
    page = page[:a] + bath_hub_nav.block("szechenyi") + GUIDE + "\n" + page[b:]

    a = page.find('<h2 id="thermal-baths-know-before-you-go">')
    b = page.find('<div class="cf-faq-container" id="faq">')
    assert 0 < a < b, (a, b)
    page = page[:a] + KNOW + page[b:]
    page = swap_block(page, r'<div class="cf-faqs-container">', faq_html())

    # runtime config + sticky bar
    cfg = {"deckId": "budapest-thermal-baths-deck", "tocDeckLabel": "Top %d Széchenyi Tickets" % N,
           "tocBreakdownLabel": "Detailed Breakdown (%d Tickets)" % N, "shortTitles": [c["short"] for c in CARDS]}
    page = must_sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, flags=re.S)
    c1 = CARDS[0]
    for tid, pid, bid in (("sticky-name", "sticky-price", "sticky-cta-btn"), ("hybridActiveTitle", "hybridActivePrice", "hybridActiveCta")):
        page = re.sub(r'(<span class="hybrid-active-title" id="%s">)[^<]*(</span>)' % tid, r"\g<1>%s\2" % c1["short"], page, count=1)
        page = re.sub(r'(<span class="hybrid-active-price" id="%s">)[^<]*(</span>)' % pid, r"\g<1>From €%s\2" % c1["price"], page, count=1)
        page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="%s")' % bid, r"\g<1>%s\2" % book_url(c1, "sticky"), page, count=1)
    page = re.sub(r"<span>All \d+ Thermal Baths</span>", "<span>All %d Széchenyi Tickets</span>" % N, page)
    page = page.replace('<span class="hybrid-active-trust">Prices checked 14 Nov 2026</span>',
                        '<span class="hybrid-active-trust">Prices checked 15 Nov 2026</span>')
    page = page.replace('aria-label="Jump to Bath Review"', 'aria-label="Jump to Ticket Review"')
    page = page.replace('aria-label="Quick Bath Navigation &amp; Booking"', 'aria-label="Quick Ticket Navigation &amp; Booking"')
    page = jsonld(page)
    page = bath_hub_nav.ensure_css(page)
    page = re.sub(r'<style id="bpa-szechenyi-css">.*?</style>\n?', "", page, flags=re.S)
    page = page.replace("</head>", '<style id="bpa-szechenyi-css">@media (max-width:839px){.ltt-integrated-pills{flex-wrap:wrap!important;row-gap:8px!important}}</style>\n</head>', 1)
    page = bath_copy_rules.apply(page)
    assert "—" not in re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S), "em dash in copy"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", OUT, len(page))


if __name__ == "__main__":
    main()
