#!/usr/bin/env python3
"""Build /budapest-amsterdam-river-cruises (EN only), 2026-11-16.

Moved here from thecruisedetective.com (which now 301s to this URL). Facts, cards,
route copy and FAQ: scripts/budapest_amsterdam_data.py + the copy below.

Template: best-day-trips-from-budapest.html (same as scripts/build_november.py):
head, deck/breakdown CSS and JS, dropdown pills, star summary and Pick/Skip are
reused; hero, deck, breakdown, guide, FAQ, sticky bar and JSON-LD are replaced.
Menu and footer come from scripts/sync_layout.py afterwards.

    python3 scripts/build_budapest_amsterdam.py && python3 scripts/sync_layout.py
"""
import hashlib
import html as H
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from budapest_amsterdam_data import FAQ, INCL, MONTH_ROWS, PRODUCTS, REVERSE_EMERALD, tr  # noqa: E402

SITE = "https://www.budapestadventures.com"
TEMPLATE = ROOT / "best-day-trips-from-budapest.html"
TPL_SLUG = "best-day-trips-from-budapest"
SLUG = "budapest-amsterdam-river-cruises"
PATH = "/" + SLUG
OUT = ROOT / f"{SLUG}.html"
ASSET = f"/assets/{SLUG}"
ISO = "2026-11-16"
CHECKED = "Nov 16, 2026"
AFF = 'rel="nofollow sponsored noopener" target="_blank"'
SIZES = 'sizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"'
BLANK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"

TITLE_TAG = "7 Best Budapest to Amsterdam River Cruises (2027 Prices)"
H1 = "The 7 Best Budapest to Amsterdam River Cruises"
CRUMB = "The 7 Best Budapest to Amsterdam River Cruises (2027)"
META = ("Budapest to Amsterdam river cruises compared: 7 15-day sailings from $3,941, with prices by month "
        "and what each fare includes (drinks, tips, transfers).")
KICKER = "2027 River Cruise Comparison"
LEAD = ("The same 15-day Emerald cruise between Budapest and Amsterdam costs <strong>$3,163 in late February and $7,122 in May</strong>, "
        "and every line stops in almost the same towns, so the real choice is <strong>when you sail and what the fare includes</strong>: "
        "here are the 7 worth booking, from <strong>$3,941 with wine at dinner</strong> to <strong>$8,365 with every drink and tip covered</strong>.")
QP = [("Best value", 1, "tips + transfers included, from $3,976"),
      ("Best summer price", 2, "$3,941 in August"),
      ("Best all-inclusive", 3, "drinks all day, $5,244 in Feb"),
      ("Best boutique", 4, "unlimited drinks incl. spirits")]
FILTERS = [("tips", "💵 Tips included"), ("allinc", "🥂 Drinks all day"), ("under5k", "💲 Under $5,000"),
           ("family", "👨‍👩‍👧 Kids 8+ welcome"), ("winter", "🎄 Christmas markets")]
SHORT = {p["key"]: p["short"] for p in PRODUCTS}

# BPA internal links in the reviews (TCD had Amsterdam links here)
EXTRA_REVIEW = {
    "emerald-christmas-markets": ' Arriving a few days early? Budapest\'s own <a href="/budapest-christmas-markets">Christmas markets</a> '
                                 'open in mid-November, and our <a href="/things-to-do-budapest-november">November guide</a> covers the rest of the city.',
}


def esc(s):
    return H.escape(s, quote=True)


def usd(v):
    return f"${v:,}"


def photo(p, i):
    return f"{ASSET}/budapest-amsterdam-river-cruise-{p['key']}-{i:02d}.avif"


def maps(q):
    return "https://www.google.com/maps/search/?api=1&amp;query=" + q.replace(" ", "+")


def anchor(n, p):
    return f"item-{n}-{p['key']}"


def tag(i):
    return {1: "bpa-gold", 2: "bpa-silver", 3: "bpa-bronze"}.get(i, "bpa-slate")


def rank_txt(p):
    return p["rank"]


def rating(p):
    s, c = p["rating"]
    meta = f"{c} reviews · operator" if c else "operator rating"
    badge = (f'<span class="bpa-rev-badge"><span class="bpa-rev-site">TourRadar</span>'
             f'<span class="bpa-rev-score">{s:.1f}</span>'
             + (f'<span class="bpa-rev-count">({c})</span>' if c else "") + "</span>")
    return (f'<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            f'<span class="bpa-stars" style="--r:{s:.2f}" aria-hidden="true"></span><b class="bpa-rate-score">{s:.1f}</b>'
            f'<span class="bpa-rate-meta">{meta}</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            f'<div class="bpa-lang-pop"><strong>{p["operator"]} operator rating</strong><span class="bpa-rate-list">{badge}</span>'
            f'<span class="bpa-lang-note">Reviews cover all of the operator\'s cruises, not only this route.</span></div></details></div>')


def pills(p):
    out = []
    for ic, lab, lead, note in p["pills"]:
        n = f'<span class="bpa-lang-note">{note}</span>' if note else ""
        out.append(f'<details class="bpa-lang"><summary class="bpa-sp">{ic} <span class="bpa-lang-label">{lab}</span>'
                   f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">{lead}{n}</div></details>')
    return "\n".join(out)


def deck_card(i, p):
    url = esc(tr(p["tour"], p["key"]))
    k = p["photos"]
    alts = [f'{esc(p["title"])} ({j}/{k})' for j in range(1, k + 1)]
    first = 'fetchpriority="high" height="534" loading="eager"' if i == 1 else 'height="534" loading="lazy"'
    imgs = [f'<img alt="{alts[0]}" {first} {SIZES} src="{photo(p, 1)}" width="800"/>']
    imgs += [f'<img alt="{alts[j - 1]}" data-src="{photo(p, j)}" decoding="async" loading="lazy" {SIZES} src="{BLANK}"/>'
             for j in range(2, k + 1)]
    port = p["dir"].split(" → ")[0]
    place = (f'<a class="bpa-kicker-map-link" href="{maps(port + " river cruise pier")}" onclick="event.stopPropagation()" '
             f'rel="noopener noreferrer" target="_blank">📍 {p["dir"]}</a>')
    return f"""<!-- #{i}: {p['short']} -->
<div class="bpa-card" data-cat="{p['cats']}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {tag(i)}">{rank_txt(p)}</span>
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>
<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>
<span class="bpa-pill">1 / {k}</span>
<div aria-label="Photo gallery {i}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">
{chr(10).join(imgs)}
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{p['operator']} • ⏱️ {p['days']} Days • {place}</div>
<a class="bpa-title" href="{url}" {AFF}>{p['title']}</a>
<div class="bpa-reviews-line">
{rating(p)}
</div>
<div class="bpa-specs-row">
{pills(p)}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {p['pick']} <span class="bpa-skip">✕ Skip it</span> {p['skip']}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">From {usd(p['price'])}</div>
<div class="bpa-psub">per person, 15 days, 2 sharing</div>
</div>
<a class="bpa-btn" href="{url}" {AFF}>Check Dates &amp; Prices →</a>
<div class="bpa-trust-micro">
<span>✓ ${round(p['price'] / p['days'])} per day</span><span>•</span><span>Booked via TourRadar</span>
</div>
<a class="bpa-sublink" href="#{anchor(i, p)}">Read Review ↓</a>
</div>
</div>
</div>
"""


def chips(p):
    d, tip, xf, age = INCL[p["key"]]
    out = [("yes", f"✓ Drinks: {d}")]
    out.append(("yes", "✓ Tips Included") if tip == "Yes" else ("no", "✕ Tips Not Included"))
    out.append(("yes", "✓ Transfers Included") if xf == "Yes" else ("no", "✕ Transfers Not Included"))
    out.append(("yes", f"✓ Ages {age}"))
    return "\n".join(f'<span class="qf1-chip {k}">{x}</span>' for k, x in out)


def details(i, p, lock):
    url = esc(tr(p["tour"], p["key"]))
    pros = "".join(f"<li>{x}</li>" for x in p["pros"])
    cons = "".join(f"<li>{x}</li>" for x in p["cons"])
    k = p["photos"]
    slides = "".join(
        f'<div class="ltt-strip-slide"><img alt="{esc(p["title"])} ({j}/{k})" loading="lazy" src="{photo(p, j)}"/><div class="ltt-strip-cap">'
        f'<span class="ltt-strip-num">{j} / {k}</span> <span>Photo: {esc(p["operator"])}</span></div></div>'
        for j in range(1, k + 1))
    review = [x.replace("TR_REVERSE", esc(tr(REVERSE_EMERALD, "emerald-splendours-reverse"))) for x in p["review"]]
    review[-1] += EXTRA_REVIEW.get(p["key"], "")
    body = "".join(f"<p>{x}</p>" for x in review)
    perks = "\n".join(f'<span class="ltt-buy-perk">{x}</span>' for x in (
        f"<strong>{p['days']} days</strong>, {p['dir']}",
        f"About <strong>${round(p['price'] / p['days'])} per day</strong>",
        "Twin cabin, <strong>2 sharing</strong>"))
    qf = "\n".join(f'<div class="qf1-row"><div class="qf1-label">{a}</div><div class="qf1-val">{b}</div></div>' for a, b in p["facts"])
    s, c = p["rating"]
    return f"""<details class="bpa-details-card" data-cat="{p['cats']}" id="{anchor(i, p)}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {tag(i)}">{rank_txt(p)}</span>
<div class="bpa-kicker">{p['operator']} • ⏱️ {p['days']} Days • <span class="bpa-kicker-map-link">{p['dir']}</span></div>
</div>
<h3 class="bpa-details-title">{p['title']}</h3>
<div class="bpa-reviews-line">
{rating(p)}
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">From {usd(p['price'])}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>Pros:</strong></h3><ul role="list">{pros}</ul></div></div><div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext"><h3><strong>Cons:</strong></h3><ul role="list">{cons}</ul></div></div></div></div>
<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">Summary &amp; Review</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">Overview</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
<div class="w-richtext">{body}<div class="ltt-filmstrip-wrap"><button aria-label="Previous photo" class="ltt-film-btn ltt-film-prev is-disabled" onclick="window.lttFilmSlide(this, -1)" type="button">‹</button><button aria-label="Next photo" class="ltt-film-btn ltt-film-next" onclick="window.lttFilmSlide(this, 1)" type="button">›</button><div aria-label="Filmstrip gallery {i}" class="ltt-filmstrip" onscroll="window.lttFilmSync(this)" tabindex="0">{slides}</div></div></div>
<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>Live Dates &amp; Prices</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">From {usd(p['price'])}</span>
<span class="ltt-buy-price-sub">per person, 2 sharing</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{p['title']}</h4>
<div class="ltt-buy-card-perks">
{perks}
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{url}" {AFF}>
<span>Check Dates &amp; Prices</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{lock}
<span>Booked securely via TourRadar</span>
</div>
</div>
</div>
</div>
</div>
</details>
<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">Quick Facts</h4>
<span class="qf1-badge">{p['dir']}</span>
</div>
<div class="qf1-table">
{qf}
</div>
<div class="qf1-Validation-pills">
{chips(p)}
</div>
</div>
</div>
</details>
"""


PAGE_CSS = """<style id="bud-ams-page-css">
.bt-qp{margin:14px 0 4px;padding:12px 14px;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc}
.bt-qp-title{font-size:12px !important;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#64748b !important;margin:0 0 6px !important}
.bt-qp ul{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:4px 18px}
.bt-qp li{font-size:14px;line-height:1.45;color:#334155;margin:0}
.bt-qp a,.bt-qp a:visited{color:#0f172a;font-weight:700;text-decoration:underline;text-underline-offset:2px}
@media (max-width:600px){.bt-qp ul{grid-template-columns:1fr}}
.bt-table-wrap{width:100%;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0 8px;border:1px solid #e2e8f0;border-radius:12px;background:#fff}
.bt-logistics{width:100%;min-width:720px;border-collapse:collapse;font-size:14px;line-height:1.4}
.bt-logistics th{background:#f8fafc;color:#0f172a;text-align:left;font-weight:700;padding:10px 12px;white-space:nowrap;border-bottom:1px solid #e2e8f0}
.bt-logistics td{padding:10px 12px;border-bottom:1px solid #f1f5f9;color:#334155;vertical-align:top}
.bt-logistics a,.bt-logistics a:visited{color:#0f172a;font-weight:700;text-decoration:underline}
.bt-note{font-size:13.5px !important;color:#64748b !important}
.bpa-rate-list .bpa-rev-badge{gap:6px}
.bt-qp a:hover,.bt-qp a:focus,.bt-logistics a:hover,.bt-logistics a:focus,.bpa-wt-faq a:hover,.bpa-details-body .w-richtext a:hover{color:#855a00 !important}
</style>"""


def table(cols, rows):
    th = "".join(f"<th>{h}</th>" for h in cols)
    tb = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="bt-table-wrap"><table class="bt-logistics"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'


def logistics_table():
    rows = []
    for n, p in enumerate(PRODUCTS, 1):
        d, tip, xf, age = INCL[p["key"]]
        rows.append((str(n), f'<a href="#card-{n}">{p["short"]}</a>', p["dir"], usd(p["price"]),
                     f'${round(p["price"] / p["days"])}', d, tip, xf, age))
    return table(["#", "Cruise", "Direction", "From", "Per day", "Drinks", "Tips incl.", "Transfers", "Ages"], rows)


def guide_html():
    """Sections after the breakdown, in the source order."""
    worth = ('<h2 id="worth-it">Is a Budapest to Amsterdam River Cruise Worth It?</h2>'
             '<p>Fifteen days, four countries and around 14 towns without packing your suitcase once. At <strong>$3,976 for Emerald\'s February sailing</strong> that is about <strong>$265 per person per day</strong> for your cabin, 41 meals, wine and beer at lunch and dinner, guided walks in nearly every port, airport transfers and tips. Booking the same hotels, trains and tours yourself across Hungary, Austria, Germany and the Netherlands would cost about the same and take a lot more planning.</p>'
             '<p>It is less of a deal if you want to explore cities in depth: most stops are a morning or an afternoon. In that case, spend a few extra days at either end. In Budapest, a <a href="/best-night-cruises-budapest">Danube night cruise</a> on your first evening shows you the Parliament and the Castle lit up from the water before you board (<a href="/best-budapest-river-cruises#card-1">this is the one I\'d book</a>).</p>')
    logi = ('<h2 id="side-by-side">All 7 Cruises Side by Side</h2>'
            '<p>The itineraries are almost the same, so these are the columns that decide the booking: price per day, drinks, whether tips and transfers are in the fare, and the minimum age.</p>'
            + logistics_table())
    month = ('<h2 id="prices-by-month">Prices by Month: When Is It Cheapest?</h2>'
             '<p><strong>Late February is the cheapest time to sail</strong>, often at half the price of May. On Scenic the gap is extreme: <strong>$5,244 on 22 February 2027 against $9,933 two weeks later</strong>. Lueftner is the exception, with its lowest fare in August.</p>'
             + table(["Cruise (2027 sailings)", "February", "March", "April / May", "Summer"], MONTH_ROWS)
             + '<p class="bt-note">Prices are per person in US dollars, cheapest cabin, two people sharing. They move with demand and sales, so treat them as a guide and check your own dates.</p>')
    route = ('<h2 id="the-route">The Route: What You See in 15 Days</h2>'
             '<p>Every cruise here follows the same three rivers. The <strong>Danube</strong> from Budapest through Bratislava and Vienna, the Wachau Valley (Dürnstein and Melk) and Passau to Regensburg; the <strong>Main-Danube Canal</strong> over the European watershed to Nuremberg and Bamberg; the <strong>Main</strong> through Würzburg and Miltenberg; and the <strong>Rhine</strong> through the Rhine Gorge, past Rüdesheim and Koblenz to Cologne and Amsterdam.</p>'
             '<p>The differences are small but real: Uniworld adds <strong>Heidelberg and Rothenburg</strong>, Scenic adds <strong>Bonn</strong>, Lueftner stops in <strong>Utrecht</strong>, and Emerald and Avalon include <strong>Bratislava</strong>. Only have a week? The <a href="/budapest-vienna-river-cruises">Budapest to Vienna river cruises</a> sail the first stretch in 5 to 8 days. The bigger decision is the direction, and it is not about the current. The ship passes about 68 locks and crosses the European watershed at 406 m above sea level, so it sails upstream for half the trip whichever way you go, because the Rhine flows north to the sea and the Danube flows east. So pick by your flights and your extra days: start in Amsterdam if you want to finish with a few days in Budapest, or the other way round if you would rather end with the canals. If you plan extra nights in Budapest, my <a href="/budapest-travel-guide">3-day Budapest itinerary</a> covers them, and the <a href="/budapest-tourism-statistics">Budapest tourism statistics</a> show which months the city is busiest.</p>')
    faq = '<h2 id="faq">Budapest to Amsterdam River Cruises: FAQ</h2>' + "".join(
        f'<h3 class="cf-faq-questions-2">{q}</h3><div class="cf-faq-answer-wrap-2"><div class="cf-faq-content-2 w-richtext"><p>{a}</p></div></div>'
        for q, a in FAQ)
    meth = ('<h2 id="how-we-compared">How I Compared These 7 River Cruises</h2>'
            '<p>On 16 November 2026 I compared every Budapest to Amsterdam and Amsterdam to Budapest river cruise I could book online, side by side on the details that decide a booking: departure dates and prices, price per day, ship, drinks, tips, transfers, minimum age and the stops that differ. Prices are per person for two adults sharing the cheapest cabin, taken from the live booking calendars on that date; ratings are the operator ratings shown next to each cruise.</p>'
            '<p>Scenic alone sells around 10 versions of this route, so I kept one per line and style rather than padding the list. I left out sailings with no bookable dates. Each of the 7 wins at something: overall value, summer value, all-inclusive, boutique, cabin views, Christmas markets and the best-known name.</p>')
    return worth + logi + month + route + faq + meth


def jsonld(url, og, publisher, author):
    items = []
    for n, p in enumerate(PRODUCTS, 1):
        items.append({"@type": "ListItem", "position": n, "url": f"{url}#{anchor(n, p)}", "item": {
            "@type": "TouristTrip", "name": p["title"],
            "description": (p["pick"][0].upper() + p["pick"][1:]).rstrip("."),
            "image": [f"{SITE}{photo(p, j)}" for j in range(1, min(p["photos"], 3) + 1)],
            "provider": {"@type": "Organization", "name": p["operator"]},
            "offers": {"@type": "Offer", "price": str(p["price"]), "priceCurrency": "USD",
                       "url": tr(p["tour"], p["key"])}}})
    lead_txt = re.sub(r"<[^>]+>", "", LEAD)
    graph = [
        {"@type": "Article", "@id": f"{url}#article", "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "headline": CRUMB, "description": META, "url": url, "inLanguage": "en",
         "datePublished": ISO, "dateModified": ISO, "author": author, "publisher": publisher,
         "image": [f"{SITE}{photo(p, 1)}" for p in PRODUCTS[:6]],
         "mainEntity": {"@type": "ItemList", "name": CRUMB, "description": lead_txt, "numberOfItems": len(items), "itemListElement": items}},
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": CRUMB, "item": url}]},
        {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def build():
    url = SITE + PATH
    s = TEMPLATE.read_text()
    lock = re.search(r'<div class="ltt-buy-card-trust">\s*(<svg.*?</svg>)', s, re.S).group(1)
    for p in PRODUCTS:
        for j in range(1, p["photos"] + 1):
            assert (ROOT / photo(p, j).lstrip("/")).exists(), photo(p, j)

    # ---- head ----
    old_title = re.search(r"<title>(.*?)</title>", s).group(1)
    old_desc = re.search(r'<meta content="([^"]+)" name="description"/>', s).group(1)
    s = s.replace(f"<title>{old_title}</title>", f"<title>{TITLE_TAG}</title>")
    s = s.replace(f'content="{old_title}"', f'content="{TITLE_TAG}"').replace(f'content="{old_desc}"', f'content="{esc(META)}"')
    p1 = photo(PRODUCTS[0], 1)
    s = re.sub(r'<link as="image" fetchpriority="high" href="[^"]+" rel="preload" type="image/[a-z]+"/>',
               f'<link as="image" fetchpriority="high" href="{p1}" rel="preload" type="image/avif"/>', s, count=1)
    og = re.search(r'<meta content="([^"]+)" property="og:image"/>', s).group(1)
    s = s.replace(og, SITE + p1)
    s = re.sub(r'<link href="[^"]+" hreflang="[^"]+" rel="alternate"/>\n?', "", s)
    alts = f'<link href="{url}" hreflang="en" rel="alternate"/>\n<link href="{url}" hreflang="x-default" rel="alternate"/>\n'
    assert f'<link href="{SITE}/{TPL_SLUG}" rel="canonical"/>' in s
    s = s.replace(f'<link href="{SITE}/{TPL_SLUG}" rel="canonical"/>', alts + f'<link href="{url}" rel="canonical"/>')
    s = s.replace(f'"{SITE}/{TPL_SLUG}"', f'"{url}"')

    # ---- own copies of the purged CSS ----
    for href in re.findall(r'href="(/css/purged/%s\.[^"]+\.css)"' % TPL_SLUG, s):
        css = (ROOT / href.lstrip("/")).read_text()
        base = href.split(TPL_SLUG + ".")[1].rsplit(".", 2)[0]
        new = f"/css/purged/{SLUG}.{base}.{hashlib.sha1(css.encode()).hexdigest()[:10]}.css"
        for old_f in (ROOT / "css/purged").glob(f"{SLUG}.{base}.*.css"):
            old_f.unlink()
        (ROOT / new.lstrip("/")).write_text(css)
        s = s.replace(href, new)
    s = s.replace("</head>", PAGE_CSS + "</head>", 1)

    # ---- hero ----
    cnt = {}
    for p in PRODUCTS:
        for c in p["cats"].split():
            cnt[c] = cnt.get(c, 0) + 1
    filters = "".join(
        f'<button class="ltt-tab-btn" data-cat="{k}" data-group="type" data-label="{lab}" onclick="lttFilterItems(\'{k}\', this)" type="button">{lab} <span class="ltt-cnt"></span></button>\n'
        for k, lab in FILTERS if cnt.get(k))
    qp = "".join(f'<li><strong>{a}:</strong> <a href="#card-{n}">{PRODUCTS[n - 1]["short"]}</a>, {d}</li>' for a, n, d in QP)
    hero = f"""<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
<a href="/">Home</a>
<span class="ltt-bc-sep">›</span>
<span class="ltt-bc-current">{CRUMB}</span>
</nav>
<span class="ltt-hero-kicker-badge">{KICKER}</span>
</div>
<h1 class="ltt-editorial-h1">
      {H1} <span class="ltt-h1-muted">(2027)</span>
</h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap">
<img alt="Adam Dimitrov" class="ltt-author-avatar" height="42" loading="eager" src="/assets/adam-dimitrov.webp" width="42"/>
</div>
<div class="ltt-author-meta">
<div class="ltt-author-line">
            By <a href="/about" target="_blank">Adam Dimitrov</a>, Founder &amp; Budapest Local
          </div>
<div class="ltt-author-role">7 Cruises • 15 Days • 2027 Sailings Compared</div>
</div>
</div>
<div class="ltt-trust-pills">
<span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: {CHECKED}</span>
</div>
</div>
<div class="ltt-lead-copy">
<p>{LEAD}</p>
<div class="bt-qp"><p class="bt-qp-title">Quick picks</p><ul>{qp}</ul></div>
</div>
<div class="ltt-integrated-filter-bar smart-filter-bar">
<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" data-label="All" onclick="lttFilterItems('all', this)" type="button">All <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Show:</span>
{filters}</div>
</div>
</div>
</div>"""
    a = s.index('<div class="ltt-hero-wrap">')
    b = s.index('<div class="comparison-table">', a)
    s = s[:a] + hero + s[b:]

    # ---- deck ----
    deck_id = "budapest-amsterdam-cruise-deck"
    s = s.replace('id="budapest-day-trips-deck"', f'id="{deck_id}"')
    a = s.index('<div class="bpa-deck-wrap" id="ltt-cards-deck">') + len('<div class="bpa-deck-wrap" id="ltt-cards-deck">\n')
    b = s.index('</div>\n</div>\n</div></div><div class="blog-section-2">', a)
    s = s[:a] + "".join(deck_card(i, p) for i, p in enumerate(PRODUCTS, 1)) + s[b:]

    # ---- breakdown + guide + FAQ ----
    a = s.index('<div class="w-richtext bpa-wt-guide">')
    b = s.index('<style>.ltt-editorial-wrapper', a)
    head = """<div class="bpa-breakdown-top-bar" id="breakdown-header">
<div>
<h2 class="bpa-breakdown-heading" id="budapest-amsterdam-breakdown">Detailed Breakdown: 7 Budapest to Amsterdam River Cruises</h2>
<p class="bpa-breakdown-sub">Route, ship, prices by departure and what is included, cruise by cruise</p>
</div>
<div class="bpa-acc-controls">
<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(true)" type="button">Expand All</button>
<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(false)" type="button">Collapse All</button>
</div>
</div>
"""
    content = (head + "".join(details(i, p, lock) for i, p in enumerate(PRODUCTS, 1))
               + '<div class="w-richtext bpa-wt-faq">\n' + guide_html() + "\n</div>\n</div>\n")
    s = s[:a] + content + s[b:]

    # ---- sticky bar + config ----
    q1 = PRODUCTS[0]
    href1 = esc(tr(q1["tour"], q1["key"]))
    s = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">).*?(</span>)', lambda m: m.group(1) + q1["short"] + m.group(2), s, count=1)
    s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">).*?(</span>)', lambda m: m.group(1) + "From " + usd(q1["price"]) + m.group(2), s, count=1)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]+(")', lambda m: m.group(1) + href1 + m.group(2), s)
    s = re.sub(r'(<span class="hybrid-active-title" id="hybridActiveTitle">).*?(</span>)', lambda m: m.group(1) + "Emerald" + m.group(2), s, count=1)
    s = re.sub(r'(<span class="hybrid-active-price" id="hybridActivePrice">).*?(</span>)', lambda m: m.group(1) + "From " + usd(q1["price"]) + m.group(2), s, count=1)
    s = s.replace("<span>Contents (13)</span>", "<span>Contents (7)</span>")
    s = s.replace("<span>All 13 Day Trips</span>", "<span>All 7 River Cruises</span>")
    s = s.replace("Jump to a Day Trip", "Jump to a River Cruise")
    cfg = {"deckId": deck_id, "tocDeckLabel": "Top 7 Budapest to Amsterdam Cruises", "tocBreakdownLabel": "Detailed Breakdown (7 Cruises)",
           "shortTitles": [p["short"] for p in PRODUCTS]}
    s = re.sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", lambda m: "window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";", s, count=1, flags=re.S)

    # ---- JSON-LD ----
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    old = json.loads(m.group(2))
    art = next(n for n in old["@graph"] if n["@type"] == "Article")
    s = s[:m.start(2)] + jsonld(url, SITE + p1, art["publisher"], dict(art["author"])) + s[m.end(2):]

    # ---- checks ----
    s = s.replace('rel="noopener nofollow sponsored"', 'rel="nofollow sponsored noopener"')
    assert "—" not in s, "em dash"
    body_only = re.sub(r'<header[^>]*ltt-navbar.*?</header>', "", s, flags=re.S)
    body_only = body_only[:body_only.find('<footer')] if '<footer' in body_only else body_only
    for bad in ("Day Trip", "day trip", "Danube Bend", "Visegrád", "Eger", "Balaton", "getyourguide.com", "thecruisedetective", "Cruise Detective"):
        hits = [x for x in re.findall(r".{0,60}%s.{0,60}" % re.escape(bad), body_only) if "best-day-trips-from-budapest" not in x]
        assert not hits, (bad, hits[:3])
    for t in re.findall(r'<a [^>]*href="https://www\.tourradar[^>]*>', s):
        assert 'rel="nofollow sponsored noopener"' in t and "utm_source=partner-traveller-1464745" in t, t
    OUT.write_text(s)
    print("wrote", OUT.relative_to(ROOT), len(s))


if __name__ == "__main__":
    build()
