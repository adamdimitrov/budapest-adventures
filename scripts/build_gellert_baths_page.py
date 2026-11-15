#!/usr/bin/env python3
"""Build /gellert-baths-budapest (EN only) from the /thermal-baths-budapest shell.

Gellért has been closed since 1 October 2025 (reopening expected in 2028, official site
gellertfurdo.hu checked 15 November 2026), and no booking site sells a Gellért bath ticket.
So this page states the status plainly and compares the best open baths to book instead.

Card renderers and card data are reused from scripts/build_thermal_baths_2026.py and
scripts/thermal_baths_data.py (hours and desk prices checked 14 Nov 2026; ticket prices,
ratings and Gellért status rechecked 15 Nov 2026). Run from the repo root:
    python3 scripts/build_gellert_baths_page.py
"""
import copy
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "gellert-baths-budapest.html")
SITE = "https://www.budapestadventures.com"
SLUG = "gellert-baths-budapest"
URL = SITE + "/" + SLUG
HUB = "/thermal-baths-budapest"
TODAY = "2026-11-15"
GELLERT_IMG = "/assets/cdn/60e43c7d6d05b671dff0dc1a/64d4e5d66efb73a26f97a16a_Gell%C3%A9rt-thermal-bath%20(11).webp"


# ── reuse the hub renderers (the hub script refuses to run on the rebuilt page, so its
#    guard and main() are cut off before executing it as a module namespace) ─────────────
def load_renderers():
    path = os.path.join(HERE, "build_thermal_baths_2026.py")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    src = src.replace("""if 'id="item-2-rudas"' in SRC["page"]:""", "if False:")
    src = src.split('if __name__ == "__main__":')[0]
    ns = {"__file__": path, "__name__": "thermal_renderers"}
    exec(compile(src, path, "exec"), ns)
    return ns


R = load_renderers()
D = R["D"]
D.GYG = D.GYG.replace("cmp=en-thermal-baths-", "cmp=en-gellert-baths-")
D.VIATOR = D.VIATOR.replace("campaign=en-thermal-baths-", "campaign=en-gellert-baths-")
SPARTY = R["amp"](D.GYG.format(slug="budapest-the-ultimate-late-night-spa-party-ticket-t386559",
                               placement="quickpick", key="sparty"))
AFF_REL = R["AFF_REL"]

BASE = {c["key"]: c for c in D.CARDS}


def card(key, n, **over):
    c = copy.deepcopy(BASE[key])
    c.update(over)
    c["anchor"] = "item-%d-%s" % (n, key)
    return c


CARDS = [
    card("rudas", 1, rank="🕌 #1 Closest to Gellért", color="bpa-gold",
         pick="if you wanted Gellért for a historic bath on the Buda riverside. Rudas is <strong>about 1 km up the river</strong> at Elizabeth Bridge, "
              "with an Ottoman Turkish bath under a stone dome and a 36 °C rooftop pool that looks across to Gellért Hill.",
         skip="if you travel with kids under 14, need step-free access, or only want a bath ticket without the meal.",
         summary_q=("Is Rudas the best replacement for Gellért?",
                    "For most visitors, yes. It is the nearest open bath to Gellért, on the same side of the river, and its Turkish bath is older than Gellért itself.")),
    card("szechenyi", 2, rank="🏛️ #2 Grandest Palace Bath", color="bpa-silver",
         pick="if you wanted Gellért for the grand bathhouse photos. Széchenyi is Budapest's other palace bath: "
              "<strong>three outdoor pools open all year</strong> in front of a yellow neo-baroque palace, open until 22:00 on Fridays.",
         skip="if you want quiet: it gets busy from late morning, so come at 7:00 on a weekday or pick Lukács or Veli Bej.",
         summary_q=("Is Széchenyi a good alternative to Gellért?",
                    "Yes, if you want the big palace experience. It is busier than Gellért ever was, so go early on a weekday.")),
    card("lukacs", 3, rank="🌿 #3 Calmest Buda Spa", color="bpa-bronze",
         pick="if you wanted Gellért's calm spa feel and medicinal water. Lukács is a smaller Buda bath with "
              "<strong>strong medicinal pools</strong> and a courtyard full of thank-you plaques, open until 22:00 on Tuesdays.",
         skip="if you want grand architecture or a party feel, or if you travel with kids under 14.",
         summary_q=("Is Lukács like Gellért?",
                    "In mood, yes: an old Buda spa that locals use for its medicinal water. It is smaller and plainer inside.")),
    card("veli-bej", 4, rank="🕌 #4 Quietest Ottoman Bath", color="bpa-slate",
         pick="if you wanted a quiet, historic soak. Veli Bej has <strong>authentic Ottoman pools under the old domes</strong>, "
              "without the crowds of Rudas, on the Buda side near Margaret Bridge.",
         skip="if you want to book online or bathe at midday: it is desk-only and closed 12:00–15:00.",
         summary_q=("Why pick Veli Bej over Rudas?",
                    "For the quiet. Both have Ottoman domes, but Veli Bej is smaller and far less crowded.")),
    card("palatinus", 5, rank="🌊 #5 Wave Pool in Summer", color="bpa-slate",
         pick="if you wanted Gellért's outdoor wave pool. Palatinus on Margaret Island has a <strong>28 °C wave pool</strong>, "
              "slides, lawns and family tickets.",
         skip="if you visit in winter for a long soak: it closes at 16:00, and the slides and many outdoor pools are a summer thing.",
         summary_q=("Does Palatinus have a wave pool like Gellért?",
                    "Yes, a 28 °C outdoor wave pool that is switched on at intervals. It is at its best on a summer day.")),
]
# Rechecked 15 Nov 2026 (GetYourGuide search results for Gellért): Széchenyi count moved on.
CARDS[1]["ratings"][0] = ("GetYourGuide", 4.2808, 29228, "gyg", None)

N = len(CARDS)
N_TESTED = sum(c["tested"] for c in CARDS)


# ── copy ─────────────────────────────────────────────────────────────────────────────
TITLE = "Gellért Baths Budapest: Closed Until 2028 + 5 Best Alternatives"
DESC = ("Gellért Baths have been closed since 1 October 2025, with reopening expected in 2028. "
        "The 5 best open baths to book instead, from Rudas up the river to Széchenyi, checked 15 Nov 2026.")
H1 = 'Gellért Baths Are Closed Until 2028 <span class="ltt-h1-muted">(5 Best Alternatives)</span>'

LEAD = f'''<div class="ltt-lead-copy">
<p>If your Budapest plan starts with the Gellért Baths, here is the news first: <strong>Gellért has been closed since 1 October 2025</strong> for a full renovation, and the official site expects it to <strong>reopen in 2028</strong>. There is no Gellért bath ticket to buy right now.</p>
<p>What you wanted from Gellért still exists a short ride away. <strong>Rudas</strong>, about 1 km up the Buda riverside, has the historic pools and a rooftop view; <strong>Széchenyi</strong> has the grand palace; <strong>Palatinus</strong> has the wave pool. I have <strong>soaked in Rudas, Széchenyi and Palatinus myself</strong>, and each card below says which Gellért fan it suits.</p>
<p>Comparing every bath in the city? See the <a href="{HUB}">full Budapest thermal baths guide</a>, or go straight to the <a href="/rudas-baths-budapest">Rudas guide</a> or the <a href="/szechenyi-baths-budapest">Széchenyi guide</a>.</p>
</div>'''

PILLS = f'''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems('all', this)" type="button">All ({N})</button>
<button class="ltt-tab-btn" data-cat="tested" onclick="lttFilterItems('tested', this)" type="button">Personally Tested ({N_TESTED})</button>
</div>'''


def a(c, text):
    return '<a href="#%s">%s</a>' % (c["anchor"], text)


R1, R2, R3, R4, R5 = CARDS
MID = f'''<div class="container w-container"><h2 id="gellert-baths-status">Is Gellért Baths Open? Status in November 2026</h2>
<img alt="The main swimming hall of the Gellért Baths before the 2025 closure" class="article-image-horizontal" loading="lazy" src="{GELLERT_IMG}" width="750"/>
<div class="w-richtext">
<blockquote>❌ <strong>Closed since 1 October 2025.</strong> Reopening expected in <strong>2028</strong>, with no exact date announced yet (official Gellért site, checked 15 November 2026).</blockquote>
<h3>What Is Being Renovated</h3><p>The whole bath complex: the columned indoor swimming hall, the thermal pools, the outdoor wave pool and the saunas. The work runs together with the renovation of the Hotel Gellért, which shares the building, so the bath cannot open in parts.</p>
<h3>What You Can Still See</h3><p>The Art Nouveau façade on <strong>Szent Gellért tér</strong>, at the Buda end of Liberty Bridge, is still worth a photo stop, but you cannot go inside. From the square, footpaths lead up <strong>Gellért Hill</strong> for some of the best views over the Danube. Rudas, the closest open bath, is a 15-minute walk north along the river.</p>
<h3>Can You Still Buy a Gellért Ticket?</h3><p>No. No Gellért bath ticket is on sale while the bath is closed, so book one of the open baths below instead.</p>
</div>
<h2 id="gellert-alternatives-quick-picks">Quick Picks: Which Bath Replaces Gellért for You</h2>
<div class="w-richtext"><ul role="list">
<li>🏛️ <strong>You wanted the historic Buda bath by the Danube:</strong> {a(R1, "Rudas")}, the closest open bath, with a Turkish bath and a rooftop pool.</li>
<li>📸 <strong>You wanted the grand palace photos:</strong> {a(R2, "Széchenyi")}, three steaming outdoor pools in City Park.</li>
<li>🌿 <strong>You wanted calm and medicinal water:</strong> {a(R3, "Lukács")}, a local Buda spa, open late on Tuesdays.</li>
<li>🤫 <strong>You wanted a quiet historic soak:</strong> {a(R4, "Veli Bej")}, Ottoman domes without the crowds.</li>
<li>🌊 <strong>You wanted the wave pool:</strong> {a(R5, "Palatinus")} on Margaret Island, best in summer.</li>
<li>🎉 <strong>You wanted a night out:</strong> <a href="{SPARTY}" rel="{AFF_REL}" target="_blank">Sparty at Széchenyi</a>, the Saturday night pool party (18+), or night bathing at Rudas on Fridays and Saturdays.</li>
</ul></div></div>'''

GUIDE = f'''<div class="container w-container"><h2 id="gellert-alternatives-buyers-guide">How to Choose a Gellért Alternative</h2><div class="w-richtext">
<h3>Stay on the Buda Side or Cross to Pest?</h3><p>Gellért stood on the Buda bank of the Danube. <strong>Rudas, Lukács and Veli Bej</strong> are on the same side, a short tram ride apart. <strong>Széchenyi</strong> is in City Park in Pest, about 20 minutes away on metro M1, and <strong>Palatinus</strong> is on Margaret Island in between.</p>
<h3>Indoor Halls or Outdoor Pools?</h3><p>Gellért had both. For outdoor pools in winter, pick Széchenyi or the rooftop pool at Rudas. For a hall under historic domes, pick Rudas or Veli Bej. Palatinus is mostly outdoor and closes at 16:00 in the winter season.</p>
<h3>What It Costs</h3><p>At the desk in 2026: from 5,700 HUF at Veli Bej (weekday mornings) and 7,000 HUF at Lukács to 12,000 HUF at Rudas and 13,200 HUF at Széchenyi on weekdays. Bookable tickets start at €27 (Palatinus), €33 (Lukács) and €39 (Széchenyi, entry before 9:00); the Rudas ticket includes a 3-course meal from €74.99.</p>
<h3>Travelling With Kids?</h3><p>Rudas, Lukács and Veli Bej do not admit children under 14. For a family day, pick Palatinus.</p>
<h3>What to Bring</h3><p>A swimsuit, a towel and flip-flops. Tickets do not include towels: the city-run baths sell a towel for 6,900 HUF and slippers for 4,200 HUF at the desk.</p>
</div>
<h2 id="gellert-how-we-checked">How We Checked</h2><div class="w-richtext">
<p>Gellért's status was checked on its official site on 15 November 2026. Opening hours, desk prices and pool temperatures for the five open baths were checked on their official sites on 14 November 2026, and ticket prices on the booking calendar for Thursday 19 November 2026, then rechecked on 15 November 2026. I have bathed at Rudas, Széchenyi and Palatinus in person. This page will be updated as soon as Gellért announces a reopening date.</p>
<p>More bath guides: the <a href="{HUB}">best thermal baths in Budapest</a>, the <a href="/rudas-baths-budapest">Rudas Baths guide</a> and the <a href="/szechenyi-baths-budapest">Széchenyi Baths guide</a>.</p>
</div>'''

FAQ = [
    ("Is Gellért Baths open?",
     "No. Gellért Baths have been closed since 1 October 2025 for a full renovation (official site, checked 15 November 2026)."),
    ("When will Gellért Baths reopen?",
     "The official site expects Gellért to reopen in 2028. No exact date has been announced yet."),
    ("What is the best alternative to Gellért Baths?",
     "Rudas for most visitors: it is the closest open bath, about 1 km up the Buda riverside, with a Turkish bath and a rooftop pool. For a grand palace bath with outdoor pools, pick Széchenyi."),
    ("Can I buy a Gellért Baths ticket?",
     "No. No Gellért bath ticket is on sale while the bath is closed. Book Rudas, Széchenyi or another open bath instead."),
    ("Which bath is closest to Gellért?",
     "Rudas, at the Buda end of Elizabeth Bridge, about a 15-minute walk north along the river from Szent Gellért tér."),
    ("Is there a wave pool like Gellért's in Budapest?",
     "Yes. Palatinus on Margaret Island has a 28 °C outdoor wave pool that is switched on at intervals. In the winter season it is open 9:00 to 16:00."),
]


def faq_html():
    cards = []
    for k, (q, ans) in enumerate(FAQ):
        first = " first" if k == 0 else ""
        cards.append('<div class="cf-faq-plus-card"><div class="cf-faq-question-container-3%s"><div class="cf-faq-question-wrap">'
                     '<h3 class="cf-faq-questions-2">%s</h3><div class="cf-faq-icon-contain"><div class="cf-faq-line"></div>'
                     '<div class="cf-faq-line-vertical"></div></div></div></div><div class="cf-faq-answer-wrap-2">'
                     '<div class="cf-faq-content-2 w-richtext"><p>%s</p></div></div><div class="cf-bottom-line-2"></div></div>' % (first, q, ans))
    return '<div class="cf-faqs-container">%s</div>' % "".join(cards)


# ── page assembly ────────────────────────────────────────────────────────────────────
must_sub, swap_block, no_em_dash = R["must_sub"], R["swap_block"], R["no_em_dash"]
all_spans = R["all_spans"]


def head(page):
    page = must_sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, page, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (TITLE, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (DESC, prop), page)
    for prop in ('property="og:image"', 'name="twitter:image"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s%s" %s/>' % (SITE, GELLERT_IMG, prop), page)
    page = must_sub(r'<meta content="[^"]*" property="og:url"/>', '<meta content="%s" property="og:url"/>' % URL, page)
    page = must_sub(r'<link href="[^"]*" rel="canonical"/>', '<link href="%s" rel="canonical"/>' % URL, page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:published_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    # preload the first card's photo (Rudas), not the hub's Széchenyi photo
    page = must_sub(r'<link as="image" fetchpriority="high" href="[^"]*"[^>]*rel="preload"[^>]*/>',
                    '<link as="image" fetchpriority="high" href="%s" rel="preload" type="image/webp"/>' % CARDS[0]["photos"][0], page)
    # EN only: one hreflang pair, no translation routes
    links = re.findall(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', page)
    assert links, "no hreflang links"
    first = page.find(links[0])
    for l in links:
        page = page.replace(l, "", 1)
    en = ('<link href="%s" hreflang="en" rel="alternate"/><link href="%s" hreflang="x-default" rel="alternate"/>' % (URL, URL))
    page = page[:first] + en + page[first:]
    page = must_sub(r"<script>const alternativeLanguagePages = .*?</script>",
                    "<script>const alternativeLanguagePages = %s</script>" % json.dumps({"en": URL}), page, flags=re.S)
    routes = [{"url": URL, "hreflang": "default", "isDefault": True, "subfolder": "", "langCode": "en"}]
    page = must_sub(r"<script>const LINGUANA_LANGUAGE_ROUTES = .*?</script>",
                    "<script>const LINGUANA_LANGUAGE_ROUTES = %s</script>" % json.dumps(routes), page, flags=re.S)
    return page


def hero(page):
    crumbs = ('<a href="/">Home</a>\n<span class="ltt-bc-sep">›</span>\n<a href="%s">Thermal Baths</a>\n'
              '<span class="ltt-bc-sep">›</span>\n<span class="ltt-bc-current">Gellért Baths</span>' % HUB)
    page = must_sub(r'<a href="/">Home</a>\s*<span class="ltt-bc-sep">›</span>\s*<span class="ltt-bc-current">[^<]*</span>', crumbs, page)
    page = must_sub(r'<span class="ltt-hero-kicker-badge">[^<]*</span>', '<span class="ltt-hero-kicker-badge">Status Checked 15 Nov 2026</span>', page)
    page = must_sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)', r"\1\n      %s\n\2" % H1, page, flags=re.S)
    page = must_sub(r'<div class="ltt-author-role">[^<]*</div>',
                    '<div class="ltt-author-role">Budapest Local • %d Open Baths Compared • Status Checked 15 Nov 2026</div>' % N, page)
    page = must_sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 15, 2026<", page)
    page = swap_block(page, r'<div class="ltt-lead-copy">', LEAD)
    page = swap_block(page, r'<div class="ltt-integrated-pills">', PILLS)
    return page


def body(page):
    deck = no_em_dash("\n".join(R["deck_html"](i, c) for i, c in enumerate(CARDS, 1)))
    dets = no_em_dash("".join(R["details_html"](i, c) for i, c in enumerate(CARDS, 1)))
    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]
    page = re.sub(r"<!-- #\d+: [^>]*-->\n?", "", page)
    # status + quick picks replace the hub's map and "why visit" block
    page = swap_block(page, r'<div class="container w-container"><div class="w-richtext"><p>Every bath below', MID)
    page = must_sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                    r"\1Detailed Breakdown: %d Best Alternatives to Gellért Baths\2" % N, page)
    page = must_sub(r'<p class="bpa-breakdown-sub">[^<]*</p>',
                    '<p class="bpa-breakdown-sub">%d of %d personally tested • All reviews open by default • Click to collapse/expand</p>' % (N_TESTED, N), page)
    # buyer's guide + methodology replace know-before-you-go and history
    a_ = page.find('<div class="container w-container"><h2 id="thermal-baths-know-before-you-go">')
    b_ = page.find('<div class="cf-faq-container" id="faq">')
    assert 0 < a_ < b_
    page = page[:a_] + GUIDE + page[b_:]
    page = swap_block(page, r'<div class="cf-faqs-container">', faq_html())
    return page


def chrome(page):
    cfg = {"deckId": "budapest-thermal-baths-deck", "tocDeckLabel": "Top %d Gellért Alternatives" % N,
           "tocBreakdownLabel": "Detailed Breakdown (%d Baths)" % N, "shortTitles": [c["short"] for c in CARDS]}
    page = must_sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, flags=re.S)
    c1 = CARDS[0]
    page = must_sub(r'(<span class="hybrid-active-title" id="sticky-name">)[^<]*(</span>)', r"\g<1>%s\2" % c1["short"], page)
    page = must_sub(r'(<span class="hybrid-active-price" id="sticky-price">)[^<]*(</span>)', r"\g<1>From €%s\2" % c1["price"], page)
    page = must_sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="sticky-cta-btn")', r"\g<1>%s\2" % R["book_url"](c1, "sticky"), page)
    page = must_sub(r"<span>All \d+ Thermal Baths</span>", "<span>All %d Alternatives</span>" % N, page)
    page = page.replace("Jump to Tested Thermal Bath", "Jump to a Gellért Alternative")
    return page


def jsonld(page):
    i = page.find('id="ltt-schema-jsonld"')
    s = page.find(">", i) + 1
    e = page.find("</script>", s)
    data = json.loads(page[s:e])
    items = []
    for pos, c in enumerate(CARDS, 1):
        avg, tot = R["wavg"](c["ratings"])
        addr = R["strip_tags"](c["getthere"][0]).replace("📍 ", "")
        offer = {"@type": "Offer", "availability": "https://schema.org/InStock",
                 "url": R["book_url"](c, "schema").replace("&amp;", "&")}
        if c.get("price"):
            offer.update(price=c["price"], priceCurrency="EUR")
        else:
            offer.update(price=c["price_huf"], priceCurrency="HUF")
        items.append({"@type": "ListItem", "position": pos, "url": "%s#%s" % (URL, c["anchor"]), "item": {
            "@type": "Product", "name": c["title"],
            "description": R["strip_tags"](c["pick"]),
            "brand": {"@type": "Organization", "name": c["title"]},
            "isRelatedTo": {"@type": "TouristAttraction", "name": c["title"], "address": addr},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                "worstRating": "1", "reviewCount": str(tot)},
            "offers": offer}})
    graph = []
    for node in data["@graph"]:
        if node.get("@type") == "Article":
            node["@id"] = URL + "#article"
            node["mainEntityOfPage"] = {"@type": "WebPage", "@id": URL}
            node["url"] = URL
            node["headline"] = TITLE
            node["description"] = DESC
            node["datePublished"] = TODAY
            node["dateModified"] = TODAY
            node["about"] = {"@type": "TouristAttraction", "name": "Gellért Thermal Bath",
                             "address": "Kelenhegyi út 4, 1118 Budapest"}
            node["image"] = [GELLERT_IMG, CARDS[0]["photos"][0]]
            node["mainEntity"] = {"@type": "ItemList", "name": "Best alternatives to Gellért Baths",
                                  "description": DESC, "numberOfItems": N, "itemListElement": items}
            graph.append(node)
        elif node.get("@type") == "BreadcrumbList":
            node["@id"] = URL + "#breadcrumb"
            node["itemListElement"] = [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Thermal Baths in Budapest", "item": SITE + HUB},
                {"@type": "ListItem", "position": 3, "name": "Gellért Baths", "item": URL}]
            graph.append(node)
        elif node.get("@type") != "FAQPage":
            graph.append(node)
    graph.append({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in FAQ]})
    data["@graph"] = graph
    out = json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")
    return page[:s] + out + page[e:]


def main():
    page = R["SRC"]["page"]
    page = head(page)
    page = hero(page)
    page = body(page)
    page = chrome(page)
    page = jsonld(page)
    page = page.replace("LUXURY EDITORIAL SYSTEM — UNIFIED", "LUXURY EDITORIAL SYSTEM: UNIFIED")
    content = re.sub(r'<header[^>]*class="[^"]*ltt-navbar.*?</header>', "", page, flags=re.S)  # menu: sync_layout.py
    leftovers = [w for w in ("6 Best Thermal Baths", "Dandár", "en-thermal-baths-", "—", "&mdash;") if w in content]
    assert not leftovers, leftovers
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", OUT, len(page))


if __name__ == "__main__":
    main()
