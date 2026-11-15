#!/usr/bin/env python3
"""Build /best-hop-on-hop-off-bus-budapest (EN only) from scripts/hoho_data.py.

The page shell (head, hero, deck, sticky bar, runtime) is the origin/main version of
/best-walking-tours-budapest; deck and details cards use the same markup as
/thermal-baths-budapest (river-cruise card style with Pick/Skip lines).
Run from the repo root:
    python3 scripts/build_hoho_2026.py && python3 scripts/sync_layout.py
"""
import json
import math
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from night_blocks import balanced, deck_card, details_card, all_spans  # noqa: E402
import hoho_data as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = D.SLUG
PAGE = os.path.join(ROOT, SLUG + ".html")
TODAY = "2026-11-15"
SITE = "https://www.budapestadventures.com"
URL = SITE + "/" + SLUG


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def base_page():
    return subprocess.run(["git", "show", "origin/main:best-walking-tours-budapest.html"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


RIVER = rd("best-budapest-river-cruises.html")

_ref_card = deck_card(RIVER, "card-2")
ICON = {m.group(1): m.group(0) for m in re.finditer(r'<img alt="([^"]+)" class="bpa-rev-icon"[^>]*>', _ref_card)}
ICON["Tiqets"] = '<img alt="Tiqets" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/652d0405192ba076b04f74a3/6852917a8b23e16d4296b394_tiqets-logo.avif"/>'
_ref_det = details_card(RIVER, "cruise-2-rubingroup")
LOCK_SVG = re.search(r'<svg fill="none"[^>]*>.*?</svg>', _ref_det, re.S).group(0)
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"
PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"


def ref_block(pat):
    return re.search(pat, RIVER, re.S).group(0)


REF_CSS = [ref_block(r'<style id="bpa-lang-css">.*?</style>'), ref_block(r'<style id="bpa-card2-css">.*?</style>')]
REF_JS = ref_block(r'<script id="bpa-lang-js">.*?</script>')

PAGE_CSS = '''<style id="bpa-hoho-css">
.bpa-hoho-callout{border-left:4px solid #dfa732;background:#fdfaf2;padding:12px 16px;border-radius:8px;font-size:16px;line-height:1.5;margin:0 0 14px}
.bpa-hoho-tbl{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0 22px;border:1px solid #e2e8f0;border-radius:12px}
.bpa-hoho-tbl table{width:100%;border-collapse:collapse;font-size:14px;min-width:560px}
.bpa-hoho-tbl th{background:#f8fafc;text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#475569;padding:10px 12px;border-bottom:1px solid #e2e8f0}
.bpa-hoho-tbl td{padding:10px 12px;border-bottom:1px solid #f1f5f9;vertical-align:top;line-height:1.4}
.bpa-hoho-tbl tr:last-child td{border-bottom:0}
.bpa-hoho-method{font-size:14px;color:#475569}
</style>'''


# ── formatting helpers ───────────────────────────────────────────────────────────────
def fmt_count(n):
    if n >= 1000:
        v = math.floor(n / 100) / 10
        return ("%.1f" % v).rstrip("0").rstrip(".") + "k+"
    if n >= 20:
        return "%d+" % (n // 10 * 10)
    return str(n)


def fmt_total(n):
    if n >= 10000:
        return "%dk+" % (n // 1000)
    return fmt_count(n)


def wavg(r):
    tot = sum(x[2] for x in r)
    return sum(x[1] * x[2] for x in r) / tot, tot


def score1(s):
    return "%.1f" % (math.floor(s * 10 + 0.5) / 10)


def amp(u):
    return u.replace("&amp;", "&").replace("&", "&amp;")


AFF_REL = "nofollow sponsored noopener"


def gyg(c, placement):
    return amp(D.GYG.format(slug=c["gyg_slug"], placement=placement, key=c["key"]))


def book_url(c, placement):
    if c["book"] == "tiqets":
        return amp(D.TIQETS.format(slug=c["tiqets_slug"]))
    return gyg(c, placement)


def price_txt(c):
    return "From €%s" % c["price"]


def maps(q):
    return amp(D.MAPS.format(q=urllib.parse.quote_plus(q)))


# ── deck card ────────────────────────────────────────────────────────────────────────
def media(i, c):
    tag = '<span class="bpa-rank-tag %s">%s</span>' % (c["color"], c["rank"])
    arrows = ('<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>'
              '<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>')
    imgs = []
    for k, p in enumerate(c["photos"]):
        alt = c["photo_alts"][k]
        if k == 0:
            extra = ' fetchpriority="high" loading="eager"' if i == 1 else ' loading="lazy"'
            imgs.append('<img alt="%s"%s height="534" sizes="%s" src="%s" width="800"/>' % (alt, extra, SIZES, p))
        else:
            imgs.append('<img alt="%s" data-src="%s" decoding="async" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>'
                        % (alt, p, SIZES, PLACEHOLDER))
    slider = ('<div aria-label="Photo gallery %d" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">\n%s</div>'
              % (i, "\n".join(imgs)))
    return '<div class="bpa-media">\n%s\n%s<span class="bpa-pill">1 / %d</span>%s\n</div>' % (tag, arrows, len(imgs), slider)


def rate_block(c):
    avg, tot = wavg(c["ratings"])
    nsites = len(c["ratings"])
    badges = []
    for r in c["ratings"]:
        site, s, cnt = r[0], r[1], r[2]
        inner = ('%s<span class="bpa-rev-site">%s</span><span class="bpa-rev-score">%s</span><span class="bpa-rev-count">(%s)</span>'
                 % ("\n" + ICON[site], site, score1(s), fmt_count(cnt)))
        badges.append('<span class="bpa-rev-badge is-static">%s</span>' % inner)
    if nsites > 1:
        head = "Average of %d sites, weighted by number of reviews" % nsites
        meta = "%s reviews · %d sites" % (fmt_total(tot), nsites)
        note = '<span class="bpa-lang-note">Each site rates its own ticket for this bus.</span>'
    else:
        head = "Rating on %s" % c["ratings"][0][0]
        meta = "%s reviews · %s" % (fmt_total(tot), c["ratings"][0][0])
        note = ""
    return ('<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            '<span class="bpa-stars" style="--r:%.2f" aria-hidden="true"></span><b class="bpa-rate-score">%s</b>'
            '<span class="bpa-rate-meta">%s</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong><span class="bpa-rate-list">%s</span>%s</div></details></div>'
            % (avg, score1(avg), meta, head, "".join(badges), note))


def deck_html(i, c):
    kicker = ('%s • ⏱️ %s • <a class="bpa-kicker-map-link" href="%s" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">%s</a>'
              % (c["area"], c["time"], maps(c["maps_q"]), c["transport"]))
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    pills = "\n".join(c["pills"])
    return f'''<div class="bpa-card" data-cat="{c["cat"]}" id="card-{i}">
<div class="bpa-main">
{media(i, c)}
<div class="bpa-info">
<div class="bpa-kicker">{kicker}</div>
<a class="bpa-title" href="{book_url(c, "card")}" rel="{AFF_REL}" target="_blank">{c["title"]}</a>
<div class="bpa-reviews-line">
{rate_block(c)}
</div>
<div class="bpa-specs-row">
{pills}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {c["pick"]} <span class="bpa-skip">✕ Skip it</span> {c["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{price_txt(c)}</div>
<div class="bpa-psub">{c["psub"]}</div>
</div>
<a class="bpa-btn" href="{book_url(c, "button")}" rel="{AFF_REL}" target="_blank">Check Availability →</a>
<div class="bpa-via">Booked securely via {c["via"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{c["anchor"]}">Read Review ↓</a>
</div>
</div>
</div>'''


# ── details card ─────────────────────────────────────────────────────────────────────
def det_header(i, c):
    return f'''<details class="bpa-details-card" data-cat="{c["cat"]}" id="{c["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {c["color"]}">{c["rank"]}</span>
<div class="bpa-kicker">{c["area"]} • ⏱️ {c["time"]} • <span class="bpa-kicker-map-link">{c["transport"]}</span></div>
</div>
<h3 class="bpa-details-title">{c["title"]}</h3>
<div class="bpa-reviews-line">
{rate_block(c)}
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">{price_txt(c)}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
'''


def proscons(c):
    pros = "".join("<li><strong>%s:</strong> %s</li>" % p for p in c["pros"])
    cons = "".join("<li><strong>%s:</strong> %s</li>" % p for p in c["cons"])
    return ('<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical">'
            '<div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>Pros:</strong></h3><ul role="list">%s</ul></div></div>'
            '<div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext">'
            '<h3><strong>Cons:</strong></h3><ul role="list">%s</ul></div></div></div></div>' % (pros, cons))


def buycard(c):
    perks = ['Booked via %s' % c["via"], c["trust"][0].replace("✓ ", ""),
             'Start: <strong>%s</strong>' % c["transport"].replace("Start: ", ""),
             'Duration: <strong>%s</strong>' % c["time"]]
    perk_html = "\n".join('<span class="ltt-buy-perk">%s</span>' % p for p in perks)
    return f'''<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>Tickets &amp; Live Availability</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{price_txt(c)}</span>
<span class="ltt-buy-price-sub">{c["psub"]}</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{c["short"]}</h4>
<div class="ltt-buy-card-perks">
{perk_html}
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{book_url(c, "review")}" rel="{AFF_REL}" target="_blank">
<span>Check Dates &amp; Book Tickets</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{LOCK_SVG}
<span>{c["trust"][1].replace("✓ ", "")}</span>
</div>
</div>
</div>
</div>'''


def qf(c):
    rows = "\n".join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>' % r for r in c["qf"])
    chips = "\n".join('<span class="qf1-chip %s">%s %s</span>' % (k, "✓" if k == "yes" else "✕", t) for k, t in c["amen"])
    return f'''<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">Quick Facts: Tickets, Times &amp; Inclusions</h4>
<span class="qf1-badge">{c["area"]}</span>
</div>
<div class="qf1-table">
{rows}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
<p class="qf1-note" style="margin:10px 0 0;font-size:12px;color:#64748b">Checked on the live listings on {D.CHECKED} (prices for {D.CAL_DATE}). Only what the source confirms is shown.</p>
</div>'''


def bento(title, pill_txt, body):
    return f'''<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">{title}</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">{pill_txt}</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
{body}
</div>
</details>'''


def body_html(c):
    q, a = c["summary_q"]
    paras = "".join("<p>%s</p>" % p.replace("{bb_gyg}", gyg(c, "flexible")) for p in c["summary"])
    quotes = "<blockquote><strong>What guests say:</strong><br/>%s</blockquote>" % "<br/>".join(
        "“%s” <em>(%s, %s)</em>" % qq for qq in c["quotes"])
    getthere = '<h3>How to Get There</h3><ul role="list">%s</ul>' % "".join("<li>%s</li>" % x for x in c["getthere"])
    summary = ('<div class="w-richtext"><blockquote>❓ <strong>%s</strong><br/>💡 %s</blockquote>%s%s%s</div>\n%s'
               % (q, a, paras, quotes, getthere, buycard(c)))
    cards = []
    for h, img, txt in c["spcards"]:
        im = '<img alt="%s: %s" loading="lazy" src="%s"/>' % (c["alt"], h.replace("&amp;", "and"), img)
        cards.append('<div class="ltt-sp-card"><h4>%s</h4>%s<ul role="list"><li>%s</li></ul></div>' % (h, im, txt))
    inside = '<div class="ltt-sub-points">\n%s\n</div>' % "\n".join(cards)
    return (proscons(c) + "\n" + bento("Summary &amp; Review Overview", "Overview", summary) + "\n"
            + bento("Route Highlights", "From the Listing", inside) + "\n" + qf(c) + "\n")


def details_html(i, c):
    return det_header(i, c) + body_html(c) + "</div>\n</details>"


def swap_block(html, start_pat, new, tag="div"):
    m = re.search(start_pat, html)
    if not m:
        raise ValueError("block not found: %s" % start_pat)
    end = balanced(html, m.start(), tag)
    return html[:m.start()] + new + html[end:]


def must_sub(pat, repl, html, count=1, flags=0):
    new, n = re.subn(pat, repl, html, count=count, flags=flags)
    if not n:
        raise ValueError("pattern not found: %s" % pat[:80])
    return new


def no_em_dash(html):
    html = re.sub(r"\s*—\s*", ": ", html)
    return html.replace("&mdash;", ":")


# ── page-level prose ─────────────────────────────────────────────────────────────────
C = {c["key"]: c for c in D.CARDS}


def a(key, text):
    return '<a href="#%s">%s</a>' % (C[key]["anchor"], text)


def tbl(head, rows):
    th = "".join("<th>%s</th>" % h for h in head)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % x for x in r) for r in rows)
    return '<div class="bpa-hoho-tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr)


LEAD = f'''<div class="ltt-lead-copy">
<p class="bpa-hoho-callout"><strong>Quick answer:</strong> book the {a("city-sightseeing", "City Sightseeing 48-hour ticket")} (€44 with a boat ride and free cancellation), or skip the open-top bus and ride tram 2 and bus 16 on a €7 day pass.</p>
<p>Budapest's two big hop-on hop-off companies charge <strong>exactly the same: €39 for one day, €44 for two, €49 for three</strong>. The difference is in the small print. One ticket includes a Danube boat ride and free cancellation; the other is non-refundable. And the second day costs just €5 more, which is why the 24-hour ticket is the worst value of the three.</p>
<p>Below are the <strong>7 best bus tours in Budapest</strong> side by side, from the classic open-top loops to a bus that <strong>splashes into the Danube</strong>, an electric shuttle up Castle Hill and two party buses with beer on tap. For each one: price per day, stops, how often the buses come, what's included and who should skip it.</p>
<p>Prices and timetables checked on {D.CHECKED}.</p>
</div>'''

FILTERS = '''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" data-label="All" onclick="lttFilterItems('all', this)" type="button">All <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Type:</span>
<button class="ltt-tab-btn" data-cat="hoho" data-group="type" data-label="Hop-on hop-off" onclick="lttFilterItems('hoho', this)" type="button">Hop-on hop-off <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="guided" data-group="type" data-label="Live guide" onclick="lttFilterItems('guided', this)" type="button">Live guide <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="fun" data-group="type" data-label="Fun rides" onclick="lttFilterItems('fun', this)" type="button">Fun rides <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Good for:</span>
<button class="ltt-tab-btn" data-cat="boat" data-group="good" data-label="Boat ride included" onclick="lttFilterItems('boat', this)" type="button">Boat ride included <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="kids" data-group="good" data-label="Kids" onclick="lttFilterItems('kids', this)" type="button">Kids <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="castle" data-group="good" data-label="Castle Hill" onclick="lttFilterItems('castle', this)" type="button">Castle Hill <span class="ltt-cnt"></span></button>
<button class="ltt-tab-btn" data-cat="party" data-group="good" data-label="Party" onclick="lttFilterItems('party', this)" type="button">Party <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">Price:</span>
<button class="ltt-tab-btn" data-cat="u40" data-group="price" data-label="Under €40" onclick="lttFilterItems('u40', this)" type="button">Under €40 <span class="ltt-cnt"></span></button>
</div>'''

GUIDE = (
    '<div class="w-richtext bpa-wt-guide">\n'
    '<h2 id="which-bus-tour">Which Budapest Bus Tour Should You Book?</h2>\n<ul>\n'
    f'<li><strong>2 or 3 days, want the classic open-top loop:</strong> {a("city-sightseeing", "City Sightseeing")} (48 hours €44, boat ride and walking tour included, free cancellation).</li>\n'
    f'<li><strong>Dates fixed, want the most stops:</strong> {a("big-bus", "Big Bus")} (21 stops, same prices, river cruise included, non-refundable).</li>\n'
    f'<li><strong>Kids, or one ride on land and water:</strong> {a("riverride", "RiverRide amphibious bus")} (90 minutes €32, splashes into the Danube).</li>\n'
    f'<li><strong>Castle Hill without the climb:</strong> {a("castle-bus", "Buda Castle electric bus")} (€18, 5 stops from the Chain Bridge).</li>\n'
    f'<li><strong>One morning and a real guide:</strong> {a("cityrama", "3-hour live guided tour")} (€35, Castle District walk included).</li>\n'
    f'<li><strong>A fun hour with a drink:</strong> {a("beerbus", "BeerBus")} (€27, unlimited beer, 5 departures a day).</li>\n'
    f'<li><strong>Stag, hen or birthday group:</strong> {a("e-beerbus", "E-BeerBus")} (from €27 each, private bus from €360, your own music).</li>\n'
    '<li><strong>Tight budget:</strong> no tour at all. A 24-hour public transport pass is 2,750 HUF (about €7); see the routes below.</li>\n'
    '</ul>\n'
    '<h2 id="big-bus-vs-city-sightseeing">Big Bus vs City Sightseeing: Which Is Better?</h2>\n'
    '<p>On price it is a draw: both charge €39, €44 and €49 for one, two and three days, and both include a guided walking tour of Pest. '
    'Both have a ticket with a Danube boat ride. The real differences:</p>\n'
    + tbl(["", "City Sightseeing", "Big Bus"], [
        ["Adult price 1 / 2 / 3 days", "€39 / €44 / €49", "€39 / €44 / €49 (some dates €33 for 1 day)"],
        ["Child price", "€35.10 / €39.60 / €44.10, ages 6 to 18; under 6 free", "€35.10 / €39.60 / €44.10, ages 5 to 15"],
        ["Route", "Red route, 20 stops, loop about 110 minutes", "Red route, 21 stops"],
        ["Buses", "9:00 to 17:00, every 10 to 20 minutes", "10:00 to 17:00, every 10 to 25 minutes"],
        ["Included", "Bus, Danube boat ride, 1-hour walking tour at 11:00", "Bus, one Danube river cruise, walking tour"],
        ["Cancellation", "<strong>Free up to 2 days before</strong>", "<strong>Non-refundable</strong> (flexible version swaps the cruise for 30% off)"],
        ["Rating", "4.1 from 5,836 reviews", "4.1 from 4,963 reviews"],
    ]) +
    f'<p><strong>Our pick: {a("city-sightseeing", "City Sightseeing")}.</strong> Same money, but you can cancel for free and teenagers travel at the child price up to 18. '
    f'Pick {a("big-bus", "Big Bus")} only if you want the extra stop and you are sure of your dates.</p>\n'
    '<h2 id="24-48-72-hours">24, 48 or 72 Hours: Which Ticket Is Worth It?</h2>\n'
    '<p>The buses run about 7 to 8 hours a day, and a full loop with commentary takes close to 2 hours. That makes the longer tickets far better value:</p>\n'
    + tbl(["Ticket", "Adult price", "Price per day", "Bus hours you can use", "Price per bus hour"], [
        ["24 hours", "€39", "€39", "about 8", "€4.90"],
        ["48 hours", "€44", "€22", "about 16", "€2.75"],
        ["72 hours", "€49", "€16.30", "about 24", "€2.05"],
    ]) +
    '<p><strong>Go for 48 hours if you are in Budapest for 2 nights or more.</strong> Day one: ride the full loop with the commentary and do the walking tour and the boat. '
    'Day two: use the bus as transport to Heroes\' Square, Széchenyi Bath and the Castle Garden. The 72-hour ticket only pays off if you will really ride on day three; '
    'by then most people know the city well enough to use the metro.</p>\n'
    '<p>Compare that with the fixed tours: the RiverRide costs about €21 per hour, the guided coach tour about €12 per hour and the BeerBus €27 for its hour. '
    'You pay for the experience, not the transport.</p>\n'
    '<h2 id="public-transport-vs-hop-on-hop-off">Is a Hop-On Hop-Off Bus Worth It? The €7 Alternative</h2>\n'
    '<p>Budapest\'s public transport passes most of the same sights for a fraction of the price. A <strong>24-hour travelcard is 2,750 HUF (about €7)</strong> '
    'and a <strong>72-hour travelcard 5,750 HUF (under €15)</strong>, valid on every metro, tram and bus in the city (bkk.hu prices, checked 15 November 2026).</p>\n<ul>\n'
    '<li><strong>Tram 2</strong> runs along the Pest bank of the Danube past the Parliament, with views of Buda Castle across the river. Often called one of the most scenic tram rides in Europe.</li>\n'
    '<li><strong>Bus 16</strong> goes from Deák Ferenc tér over the Chain Bridge and up to Castle Hill, the same climb the €18 castle bus saves you.</li>\n'
    '<li><strong>Bus 105</strong> also crosses the Chain Bridge between Pest and Buda.</li>\n'
    '<li><strong>Metro M1</strong>, the oldest line on the continent, runs under Andrássy Avenue from the Opera to Heroes\' Square and City Park.</li>\n'
    '</ul>\n'
    '<p><strong>Choose public transport</strong> if you are comfortable finding your own way and don\'t need commentary. '
    '<strong>Choose the hop-on bus</strong> if you want the stories behind the buildings in your language, an open top deck for photos, a guided walk and a boat ride on the same ticket, '
    'or you are travelling with kids or older family who need a seat between sights. '
    'Planning to visit several museums too? The <a href="/budapest-card-is-it-worth-it">Budapest Card</a> includes unlimited public transport.</p>\n'
    '<h2 id="bus-tours-compared">All 7 Bus Tours Compared</h2>\n'
    + tbl(["Tour", "Price", "Length", "Starts from", "Runs", "Included", "Cancellation"], [
        [a("city-sightseeing", "City Sightseeing"), "€39 / €44 / €49", "24 / 48 / 72 h", "St Stephen's Basilica", "9:00 to 17:00, every 10 to 20 min", "Bus, boat, walking tour", "Free up to 2 days before"],
        [a("big-bus", "Big Bus"), "€39 / €44 / €49", "1 / 2 / 3 days", "József Attila utca 24", "10:00 to 17:00, every 10 to 25 min", "Bus, river cruise, walking tour", "Non-refundable"],
        [a("riverride", "RiverRide"), "€27 / €32", "50 / 90 min", "Széchenyi István tér 7", "3 a day in winter, 4 in summer", "Live guide, river section", "Free up to 24 h before"],
        [a("castle-bus", "Castle bus"), "€18", "1 round", "Clark Ádám tér", "9:00 to 17:00, about every 20 min", "Up to 3 boardings", "Free up to 24 h before"],
        [a("cityrama", "Live guided tour"), "€35", "3 h", "Báthory utca 19", "Morning or afternoon", "Live guide, castle walk", "Free up to 24 h before"],
        [a("beerbus", "BeerBus"), "€27", "1 h", "Bajcsy-Zsilinszky út 16", "13:00 to 18:00, 5 a day", "Unlimited beer", "Free up to 24 h before"],
        [a("e-beerbus", "E-BeerBus"), "from €27 (private €360)", "1 to 2 h", "Heroes' Square", "On request, min. 4 people", "Unlimited beer, own music", "Free up to 24 h before"],
    ]) +
    '<p>Got an evening free? A bus tour covers the day; for the city lit up at night, compare the '
    '<a href="/best-night-cruises-budapest">best night cruises in Budapest</a> or book a table on one of the '
    '<a href="/best-dinner-cruises-budapest">best dinner cruises</a>. Prefer to explore on foot? See the '
    '<a href="/best-walking-tours-budapest">best walking tours in Budapest</a>.</p>\n'
    '</div>'
)

FAQ = [
    ("Which is the best hop-on hop-off bus in Budapest?",
     "City Sightseeing, by a small margin over Big Bus. Both cost €39 for 24 hours, €44 for 48 and €49 for 72, but City Sightseeing includes a boat ride, can be cancelled for free up to 2 days before and charges the child price up to age 18."),
    ("How much is the hop-on hop-off bus in Budapest?",
     "€39 for 24 hours, €44 for 48 hours and €49 for 72 hours per adult on both Big Bus and City Sightseeing. Children pay €35.10, €39.60 and €44.10; under-6s ride free on City Sightseeing. Some dates are discounted to €33."),
    ("Is the hop-on hop-off bus in Budapest worth it?",
     "Yes for a 48-hour ticket if you want commentary, a boat ride and a walking tour in one price (€22 a day). If you only want to get around, a 24-hour public transport pass at 2,750 HUF (about €7) is far cheaper: tram 2 and bus 16 pass many of the same sights."),
    ("What time does the hop-on hop-off bus start in Budapest?",
     "City Sightseeing runs from 9:00 to 17:00 every 10 to 20 minutes, Big Bus from 10:00 to 17:00 every 10 to 25 minutes. The last departure from stop 1 is at 17:00."),
    ("Does the Budapest hop-on hop-off include a river cruise?",
     "Yes, both the City Sightseeing ticket and the Big Bus ticket in this guide include a Danube boat ride. Big Bus's flexible, cancellable version gives you 30% off a cruise at the pier instead."),
    ("How do you get up to Buda Castle without walking?",
     "Take the €18 official Buda Castle electric bus from Clark Ádám tér, which stops at 5 points on Castle Hill, or public bus 16 from Deák Ferenc tér on a normal ticket."),
    ("Is there a bus that goes into the Danube?",
     "Yes, the RiverRide amphibious bus drives through Pest and then splashes into the Danube. The 50-minute tour is from €27; the 90-minute tour (€32) sails to the Parliament."),
    ("Is there a beer bus in Budapest?",
     "Two. The BeerBus is €27 per person for an hour with unlimited beer and 5 departures a day. The electric E-BeerBus is from €27 per person for groups of 4 or more, or from €360 for a private bus with your own music."),
]


def faq_html():
    parts = ['<div class="w-richtext bpa-wt-faq"><h2 id="faq-dup2">Frequently Asked Questions</h2>']
    for q, ans in FAQ:
        parts.append('<h3 class="cf-faq-questions-2">%s</h3><div class="cf-faq-answer-wrap-2"><div class="cf-faq-content-2 w-richtext"><p>%s</p></div></div>' % (q, ans))
    parts.append('<h2 id="how-we-compared">How We Compared These Bus Tours</h2>'
                 '<p class="bpa-hoho-method">Compared on %s using the live booking listings and the operators\' own sites. '
                 'Prices are for %s; ratings and review counts are the live figures on the day, and for the two big operators we averaged both booking sites, '
                 'weighted by number of reviews. Public transport prices are from bkk.hu. We rank by value for a first-time visitor: what the ticket includes, '
                 'how flexible it is and how many guests rate it well.</p>' % (D.CHECKED, D.CAL_DATE))
    parts.append('</div>')
    return "".join(parts)


TITLE = "7 Best Hop-On Hop-Off & Bus Tours in Budapest (2026)"
H1 = "The 7 Best Hop-On Hop-Off and Sightseeing Bus Tours in Budapest in 2026"
DESC = ("Big Bus vs City Sightseeing, the amphibious RiverRide, the Castle bus and the BeerBus compared: "
        "which ticket length pays off, from €18, and when a €7 transit pass wins.")


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&rsquo;", "’")


def build_jsonld(cards):
    items = []
    for pos, c in enumerate(cards, 1):
        avg, tot = wavg(c["ratings"])
        items.append({"@type": "ListItem", "position": pos, "url": "%s#%s" % (URL, c["anchor"]), "item": {
            "@type": "Product",
            "name": c["title"],
            "image": SITE + c["photos"][0],
            "description": strip_tags("%s: %s" % (strip_tags(c["rank"]).split(" ", 2)[-1], c["pick"])),
            "brand": {"@type": "Brand", "name": c["title"].split(":")[0]},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                "worstRating": "1", "reviewCount": str(tot)},
            "offers": {"@type": "Offer", "price": c["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                       "url": book_url(c, "schema").replace("&amp;", "&")},
        }})
    author = {"@type": "Person", "name": "Adam Dimitrov", "jobTitle": "Founder, Budapest Adventures",
              "url": SITE + "/about", "image": SITE + "/assets/adam-dimitrov.webp"}
    graph = [
        {"@type": "Article", "@id": URL + "#article", "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
         "headline": H1, "description": DESC, "url": URL, "inLanguage": "en", "image": SITE + cards[0]["photos"][0],
         "datePublished": TODAY, "dateModified": TODAY, "author": author,
         "publisher": {"@type": "Organization", "name": "BUDAPEST ADVENTURES", "url": SITE + "/",
                       "logo": {"@type": "ImageObject", "url": SITE + "/assets/budapest-adventures-logo.png"}},
         "mainEntity": {"@type": "ItemList", "name": H1, "numberOfItems": len(cards), "itemListElement": items}},
        {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "7 Best Hop-On Hop-Off Bus Tours in Budapest (2026)", "item": URL}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in FAQ]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def main():
    page = base_page()
    cards = D.CARDS
    n = len(cards)
    deck = "\n".join(deck_html(i, c) for i, c in enumerate(cards, 1))
    dets = "".join(details_html(i, c) for i, c in enumerate(cards, 1))

    # cards
    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    page = re.sub(r"<!-- #\d+: [^>]*-->\n?", "", page)
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]

    # head
    page = must_sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE.replace("&", "&amp;"), page, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (TITLE.replace("&", "&amp;"), prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (DESC, prop), page)
    img1 = SITE + cards[0]["photos"][0]
    for prop in ('property="og:image"', 'name="twitter:image"'):
        page = must_sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (img1, prop), page)
    page = must_sub(r'<link as="image" fetchpriority="high" href="[^"]*" rel="preload" type="image/webp"/>',
                    '<link as="image" fetchpriority="high" href="%s" rel="preload" type="image/webp"/>' % cards[0]["photos"][0], page)
    page = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", page)
    page = must_sub(r'<link href="[^"]*" rel="canonical"/>',
                    '<link href="%s" hreflang="en" rel="alternate"/><link href="%s" hreflang="x-default" rel="alternate"/>'
                    '<link href="%s" rel="canonical"/>' % (URL, URL, URL), page)
    page = must_sub(r'<meta content="[^"]*" property="og:url"/>', '<meta content="%s" property="og:url"/>' % URL, page)
    page = page.replace("</head>", "\n".join(REF_CSS) + "\n" + PAGE_CSS + "\n</head>", 1)
    page = page.replace("</body>", REF_JS + "\n</body>", 1)

    # hero
    page = must_sub(r'<span class="ltt-bc-current">[^<]*</span>', '<span class="ltt-bc-current">7 Best Hop-On Hop-Off Bus Tours in Budapest (2026)</span>', page)
    page = must_sub(r'<span class="ltt-hero-kicker-badge">[^<]*</span>', '<span class="ltt-hero-kicker-badge">2026 Bus Tour Comparison</span>', page)
    page = must_sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)',
                    r'\1\n      %s <span class="ltt-h1-muted">(Prices Compared)</span>\n\2' % H1, page, flags=re.S)
    page = must_sub(r'(<div class="ltt-author-line">\s*By <a href="/about" target="_blank">Adam Dimitrov</a>),[^<]*',
                    r"\1, Founder, Budapest Adventures\n          ", page)
    page = must_sub(r'<div class="ltt-author-role">[^<]*</div>',
                    '<div class="ltt-author-role">7 Bus Tours Compared • Prices &amp; Timetables Checked 15 Nov 2026</div>', page)
    page = must_sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 15, 2026<", page)
    page = swap_block(page, r'<div class="ltt-lead-copy">', LEAD)
    page = swap_block(page, r'<div class="ltt-integrated-pills">', FILTERS)
    page = page.replace('id="budapest-walking-tours-deck"', 'id="budapest-bus-tours-deck"')

    # guide, breakdown, FAQ
    page = swap_block(page, r'<div class="w-richtext bpa-wt-guide">', GUIDE)
    page = must_sub(r'(<h2 class="bpa-breakdown-heading" id=")[^"]*(">)[^<]*(</h2>)',
                    r"\1bus-tours-breakdown\2Detailed Breakdown: %d Best Bus Tours in Budapest\3" % n, page)
    page = must_sub(r'<p class="bpa-breakdown-sub">[^<]*</p>',
                    '<p class="bpa-breakdown-sub">Prices checked %s • All reviews open by default • Click to collapse/expand</p>' % D.CHECKED, page)
    page = swap_block(page, r'<div class="w-richtext bpa-wt-faq">', faq_html())

    # runtime config + sticky bar
    cfg = {"deckId": "budapest-bus-tours-deck", "tocDeckLabel": "Top %d Bus Tours" % n,
           "tocBreakdownLabel": "Detailed Breakdown (%d Bus Tours)" % n,
           "shortTitles": [c["short"] for c in cards]}
    page = must_sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, flags=re.S)
    c1 = cards[0]
    for tid, pid, bid in (("sticky-name", "sticky-price", "sticky-cta-btn"), ("hybridActiveTitle", "hybridActivePrice", "hybridActiveCta")):
        page = re.sub(r'(<span class="hybrid-active-title" id="%s">)[^<]*(</span>)' % tid, r"\g<1>%s\2" % c1["short"], page, count=1)
        page = re.sub(r'(<span class="hybrid-active-price" id="%s">)[^<]*(</span>)' % pid, r"\g<1>From €%s\2" % c1["price"], page, count=1)
        page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="%s")' % bid, r"\g<1>%s\2" % book_url(c1, "sticky"), page, count=1)
    page = re.sub(r"<span>All \d+ Walking Tours</span>", "<span>All %d Bus Tours</span>" % n, page)
    page = page.replace('<span class="hybrid-active-trust">Free 24h Cancellation</span>',
                        '<span class="hybrid-active-trust">Prices checked 15 Nov 2026</span>')
    page = page.replace('aria-label="Jump to Cruise Review"', 'aria-label="Jump to Bus Tour Review"')
    page = page.replace('aria-label="Quick Cruise Navigation &amp; Booking"', 'aria-label="Quick Bus Tour Navigation &amp; Booking"')
    page = page.replace('rel="noopener nofollow sponsored"', 'rel="%s"' % AFF_REL)
    page = page.replace("Jump to Tested Walking Tour", "Jump to a Bus Tour")
    # legacy Webflow script that stamped "Personally Tested" on every row
    page = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const cruiseCards = .*?</script>', "", page, count=1, flags=re.S)

    # JSON-LD
    i = page.find('id="ltt-schema-jsonld"')
    s0 = page.find(">", i) + 1
    s1 = page.find("</script>", s0)
    page = page[:s0] + build_jsonld(cards) + page[s1:]

    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", PAGE, len(page))


if __name__ == "__main__":
    main()
