#!/usr/bin/env python3
"""Rebuild /best-night-cruises-budapest (EN) from scripts/night_cruises_data.py.

Tested cards reuse their own photos and first-hand copy from the night, river and dinner
pages, with the facts corrected to today's listings. New cards are written from the live
listings. Run from the repo root:  python3 scripts/build_night_cruises_2026.py
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from night_blocks import balanced, deck_card, details_card, all_spans  # noqa: E402
import night_cruises_data as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "best-night-cruises-budapest.html")
TODAY = "2026-11-14"
SITE = "https://www.budapestadventures.com"


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


SRC = {"night": rd("best-night-cruises-budapest.html"),
       "river": rd("best-budapest-river-cruises.html"),
       "dinner": rd("best-dinner-cruises-budapest.html")}
if "item-1-unlimited-prosecco" in SRC["night"]:
    sys.exit("Page already rebuilt; run against the origin/main version (git checkout origin/main -- best-night-cruises-budapest.html).")

# ── shared bits from the reference page ──────────────────────────────────────────────
_ref_card = deck_card(SRC["river"], "card-2")
ICON = {m.group(1): m.group(0) for m in re.finditer(r'<img alt="([^"]+)" class="bpa-rev-icon"[^>]*>', _ref_card)}
_ref_det = details_card(SRC["river"], "cruise-2-rubingroup")
_svgs = re.findall(r'<svg aria-hidden="true" viewbox="0 0 24 24"><path d="[^"]+"></path></svg>', _ref_det)
STAR_FULL = _svgs[0]
STAR_HALF = next(s for s in _svgs if "V15.968" in s)
DET_ICON = {}
for m in re.finditer(r'<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="([^"]+)"/>', _ref_det):
    pass
_icons_in_det = re.findall(r'<img alt="" class="bpa-rev-icon" loading="lazy" src="([^"]+)"/>', _ref_det)
DET_ICON = {"GetYourGuide": _icons_in_det[0], "Viator": _icons_in_det[1], "Tripadvisor": _icons_in_det[2]}
LOCK_SVG = re.search(r'<svg fill="none"[^>]*>.*?</svg>', _ref_det, re.S).group(0)
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"
PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"


# ── formatting helpers ───────────────────────────────────────────────────────────────
def fmt_count(n):
    """Badge count, never rounded up: 51318 -> 51.3k+, 493 -> 490+, 62 -> 60+."""
    if n >= 1000:
        v = math.floor(n / 100) / 10
        return ("%.1f" % v).rstrip("0").rstrip(".") + "k+"
    if n >= 100:
        return "%d+" % (n // 10 * 10)
    if n >= 20:
        return "%d+" % (n // 10 * 10)
    return str(n)


def fmt_total(n):
    if n >= 10000:
        return "%dk+" % (n // 1000)
    return fmt_count(n)


def wavg(r):
    tot = sum(c for _, _, c, _ in r)
    return sum(s * c for _, s, c, _ in r) / tot, tot


def score1(s):
    return "%.1f" % (math.floor(s * 10 + 0.5) / 10)


def gyg(c, placement):
    return D.GYG.format(slug=c["gyg_slug"], placement=placement, key=c["key"]).replace("&", "&amp;")


def book_url(c, placement):
    b = c["book"]
    if b == "gyg":
        return gyg(c, placement)
    if b == "legenda_dl":
        return D.LEGENDA_DL
    if b == "legenda_dinner":
        return D.LEGENDA_DINNER
    if b == "silverline_sight":
        return D.SL.format(slug="budapest-sightseeing-cruises")
    raise ValueError(b)


def maps(q):
    return D.MAPS.format(q=q.replace(" ", "+")).replace("&", "&amp;")


def stars(s):
    half = round(s * 2) / 2
    full = int(half)
    out = STAR_FULL * full + (STAR_HALF if half - full else "")
    return out


# Slider order chosen to sell each card (1-based positions of the source slider):
# lead with the shot that matches the card's promise, then boat, drinks/food, views, details.
PHOTO_ORDER = {
    "legenda-danube-legend": [1, 6, 7, 5, 4, 3, 8, 2],
    "duna-weser-unlimited-prosecco": [5, 1, 2, 6, 3, 4, 7],
    "kisfaludy-paddle-steamer": [1, 2, 8, 7, 5, 9, 3, 4, 6, 10],
    "legenda-candlelit-dinner": [4, 1, 2, 6, 5, 3, 8, 11, 7, 10, 9, 12],
    "river-diva-dinner": [5, 2, 1, 3, 4, 7, 6, 9, 8, 10, 11],
    "silverline-dinner": [1, 5, 3, 8, 7, 11, 9, 10, 6, 12, 4, 2],
    "silverline-unlimited-prosecco": [2, 1, 6, 3, 5, 4, 7, 8, 9, 11, 10],
    "silverline-sightseeing": [5, 3, 2, 4, 1],
}


def reorder_slider(slider, key):
    order = PHOTO_ORDER.get(key)
    if not order:
        return slider
    imgs = re.findall(r"<img [^>]*>", slider)
    assert sorted(order) == list(range(1, len(imgs) + 1)), (key, len(imgs))
    def url(im):
        m = re.search(r'data-src="([^"]+)"', im) or re.search(r' src="([^"]+)"', im)
        return m.group(1)
    def lazy(im):
        if "data-src=" in im:
            return im
        return re.sub(r' src="([^"]+)"', lambda m: ' data-src="%s" decoding="async" src="%s"' % (m.group(1), PLACEHOLDER), im, count=1)
    def eager(im):
        u = url(im)
        im = re.sub(r'\sdata-src="[^"]*"', "", im)
        im = re.sub(r'\sdata-srcset="[^"]*"', "", im)
        im = re.sub(r' src="[^"]*"', ' src="%s"' % u, im, count=1)
        return im
    new = [imgs[i - 1] for i in order]
    new = [eager(new[0])] + [lazy(im) for im in new[1:]]
    head = slider[:slider.find("<img ")]
    return head + "\n".join(new) + "</div>"


# ── deck card ────────────────────────────────────────────────────────────────────────
def media(i, c):
    tag = '<span class="bpa-rank-tag %s">%s</span>' % (c["color"], c["rank"])
    arrows = ('<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>'
              '<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>')
    if c.get("deck_src"):
        page, cid = c["deck_src"]
        src = deck_card(SRC[page], cid)
        a = re.search(r'<div[^>]*class="bpa-slider"', src).start()
        b = balanced(src, a, "div")
        slider = src[a:b]
        imgs = re.findall(r"<img [^>]*>", slider)
        bad = [im for im in imgs if "folklore-operetta" in im and c["key"] == "silverline-sightseeing"]
        if bad:  # a Silverline dinner-show photo had slipped into the sightseeing slider
            imgs = [im for im in imgs if im not in bad]
            if "data-src" in imgs[0]:
                imgs[0] = re.sub(r'src="data:[^"]*"', "", imgs[0]).replace("data-src=", "src=")
            slider = slider[:slider.find("<img ")] + "\n".join(imgs) + "</div>"
        if len(imgs) > 12:  # the reference keeps 8 to 12 photos per card
            head = slider[:slider.find("<img ")]
            slider = head + "\n".join(imgs[:12]) + "</div>"
        n = len(re.findall(r"<img ", slider))
        slider = re.sub(r'aria-label="Photo gallery \d+"', 'aria-label="Photo gallery %d"' % i, slider)
    else:
        imgs = []
        for k in range(1, c["nphotos"] + 1):
            p = "/assets/night-cruises-2026/%s-%02d.webp" % (c["photos"], k)
            alt = c["alt"]
            if k == 1:
                imgs.append('<img alt="%s" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>' % (alt, SIZES, p))
            else:
                imgs.append('<img alt="%s" data-src="%s" decoding="async" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>'
                            % (alt, p, SIZES, PLACEHOLDER))
        n = len(imgs)
        slider = ('<div aria-label="Photo gallery %d" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">\n%s</div>'
                  % (i, "\n".join(imgs)))
    slider = reorder_slider(slider, c["key"])
    return ('<div class="bpa-media">\n%s\n%s<span class="bpa-pill">1 / %d</span>%s\n</div>' % (tag, arrows, n, slider))


def rate_block(c):
    avg, tot = wavg(c["ratings"])
    nsites = len(c["ratings"])
    badges = []
    for site, s, cnt, link in c["ratings"]:
        inner = ('%s<span class="bpa-rev-site">%s</span><span class="bpa-rev-score">%s</span><span class="bpa-rev-count">(%s)</span>'
                 % ("\n" + ICON[site], site, score1(s), fmt_count(cnt)))
        # OTA review entries link out only when the card has no direct/Tiqets booking link
        # (direct links pay a higher commission, so their clicks must stay on the CTA).
        if link == "gyg" and c.get("book") == "gyg":
            badges.append('<a class="bpa-rev-badge is-link" href="%s" rel="noopener nofollow sponsored" target="_blank">%s'
                          '<span class="bpa-rev-go" aria-hidden="true">→</span></a>' % (gyg(c, "rating"), inner))
        else:
            badges.append('<span class="bpa-rev-badge is-static">%s</span>' % inner)
    if nsites > 1:
        head = "Average of %d booking sites, weighted by number of reviews" % nsites
    else:
        head = "Rating on %s" % c["ratings"][0][0]
    note = ""
    meta = "%s reviews · %d site%s" % (fmt_total(tot), nsites, "s" if nsites > 1 else "")
    return ('<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            '<span class="bpa-stars" style="--r:%.2f" aria-hidden="true"></span><b class="bpa-rate-score">%s</b>'
            '<span class="bpa-rate-meta">%s</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong><span class="bpa-rate-list">%s</span>%s</div></details></div>'
            % (avg, score1(avg), meta, head, "".join(badges), note))


def deck_html(i, c):
    title_href = book_url(c, "card")
    tested_pill = ""
    proof = ""
    if c["tested"]:
        proof = '\n<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>'
        tested_pill = ('<details class="bpa-lang bpa-tested bpa-proof-mobile"><summary class="bpa-vchip bpa-proof-mobile">✓ Personally Tested'
                       '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s'
                       '<span class="bpa-lang-note">What I checked: deck views, commentary, drinks and value for money. '
                       '<a href="#%s">Full review ↓</a></span></div></details>\n' % (c["tested_pop"], c["anchor"]))
    kicker = ('%s • ⏱️ %s • <a class="bpa-kicker-map-link" href="%s" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">%s</a>'
              % (c["operator"], c["duration"], maps(c["pier_q"]), c["pier"]))
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    return f'''<div class="bpa-card" data-cat="{c["cat"]}" id="card-{i}">
<div class="bpa-main">
{media(i, c)}
<div class="bpa-info">
<div class="bpa-kicker">{kicker}</div>
<a class="bpa-title" href="{title_href}" rel="nofollow sponsored noopener" target="_blank">{c["title"]}</a>
<div class="bpa-reviews-line">
{rate_block(c)}{proof}
</div>
<div class="bpa-specs-row">
{tested_pill}{chr(10).join(c["pills"])}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {c["pick"]} <span class="bpa-skip">✕ Skip it</span> {c["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">From €{c["price"]}</div>
<div class="bpa-psub">{c["psub"]}</div>
</div>
<a class="bpa-btn" href="{book_url(c, "button")}" rel="nofollow sponsored noopener" target="_blank">Check Availability →</a>
<div class="bpa-via">Booked securely via {c["via"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{c["anchor"]}">Read Review ↓</a>
</div>
</div>
</div>'''


# ── details card ─────────────────────────────────────────────────────────────────────
def det_header(i, c):
    badges = []
    for site, s, cnt, _ in c["ratings"]:
        badges.append('<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="%s"/>'
                      '<span class="bpa-rev-score">%s</span><span class="bpa-rev-stars">%s</span><span class="bpa-rev-count">(%s)</span></span>'
                      % (DET_ICON[site], score1(s), stars(s), fmt_count(cnt)))
    proof = '\n<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>' if c["tested"] else ""
    return f'''<details class="bpa-details-card" data-cat="{c["cat"]}" id="{c["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {c["color"]}">{c["rank"]}</span>
<div class="bpa-kicker">{c["operator"]} • ⏱️ {c["duration"]} • <span class="bpa-kicker-map-link">{c["pier"]}</span></div>
</div>
<h3 class="bpa-details-title">{c["title"]}</h3>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{"".join(badges)}</div></div>{proof}
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">From €{c["price"]}</span>
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
    return f'''<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>Official Tickets &amp; Live Availability</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">From €{c["price"]}</span>
<span class="ltt-buy-price-sub">{c["psub"]}</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{c["short"]}</h4>
<div class="ltt-buy-card-perks">
<span class="ltt-buy-perk">Booked via {c["via"]}</span>
<span class="ltt-buy-perk">Full Refund up to 24h Before</span>
<span class="ltt-buy-perk">Departure: <strong>{c["pier"]}</strong></span>
<span class="ltt-buy-perk">Duration: <strong>{c["duration"]}</strong></span>
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{book_url(c, "review")}" rel="noopener nofollow sponsored" target="_blank">
<span>Check Dates &amp; Book Tickets</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{LOCK_SVG}
<span>Free cancellation up to 24 hours before</span>
</div>
</div>
</div>
</div>'''


def qf(c):
    rows = "\n".join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>' % r for r in c["qf"])
    chips = "\n".join('<span class="qf1-chip %s">%s %s</span>' % (k, "✓" if k == "yes" else "✕", t) for k, t in c["amen"])
    return f'''<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">Quick Facts: Verified Listing Specs</h4>
<span class="qf1-badge">{c["pier"]}</span>
</div>
<div class="qf1-table">
{rows}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
<p class="qf1-note" style="margin:10px 0 0;font-size:12px;color:#64748b">Checked on the live listing on 14 November 2026. Only what the listing confirms is shown.</p>
</div>'''


def getthere(c):
    return '<h3>How to Get There</h3><ul role="list">%s</ul>' % "".join("<li>%s</li>" % x for x in c["getthere"])


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


def new_body(c):
    q, a = c["summary_q"]
    paras = "".join("<p>%s</p>" % p for p in c["summary"])
    quotes = ""
    if c["quotes"]:
        quotes = "<blockquote><strong>What guests say:</strong><br/>%s</blockquote>" % "<br/>".join(
            "“%s” <em>(%s, %s)</em>" % qq for qq in c["quotes"])
    summary = ('<div class="w-richtext"><blockquote>❓ <strong>%s</strong><br/>💡 %s</blockquote>%s%s%s</div>\n%s'
               % (q, a, paras, quotes, getthere(c), buycard(c)))
    cards = []
    for h, img, txt in c["spcards"]:
        im = ""
        if img:
            im = ('<img alt="%s" loading="lazy" src="/assets/night-cruises-2026/%s-%02d.webp"/>' % (c["alt"], c["photos"], img))
        cards.append('<div class="ltt-sp-card"><h4>%s</h4>%s<ul role="list"><li>%s</li></ul></div>' % (h, im, txt))
    onboard = '<div class="ltt-sub-points">\n%s\n</div>' % "\n".join(cards)
    return (proscons(c) + "\n" + bento("Summary &amp; Review", "Overview", summary) + "\n"
            + bento("On Board: Boat, Decks, Drinks &amp; Route", "From the Listing", onboard) + "\n" + qf(c) + "\n")


def remove_class_blocks(html, cls_prefix):
    """Drop every element whose class attribute starts with cls_prefix (balanced)."""
    while True:
        m = re.search(r'<(div|span|a|button|section|p)\b[^>]*class="%s[^"]*"[^>]*>' % re.escape(cls_prefix), html)
        if not m:
            return html
        end = balanced(html, m.start(), m.group(1))
        html = html[:m.start()] + html[end:]


def swap_block(html, start_pat, new, tag="div"):
    m = re.search(start_pat, html)
    if not m:
        raise ValueError("block not found: %s" % start_pat)
    end = balanced(html, m.start(), tag)
    return html[:m.start()] + new + html[end:]


def must(html, old, new, count=1):
    if old not in html:
        raise ValueError("text not found: %r" % old[:80])
    return html.replace(old, new, count)


def tested_body(c):
    page, did = c["det_src"]
    det = details_card(SRC[page], did)
    a = det.find('<div class="bpa-details-body">') + len('<div class="bpa-details-body">\n')
    body = det[a:det.rfind("</div>")]
    # Silverline: turn the three show options into a plain list before dropping dc-* widgets
    if c["key"] == "silverline-dinner":
        opts = ('<ul role="list"><li>🕯️ <strong>Dinner &amp; Lights (no show):</strong> from €77, background music. '
                '<a href="%s" rel="noopener nofollow sponsored" target="_blank">Book →</a></li>'
                '<li>💃 <strong>Folk &amp; Operetta Show:</strong> from €91, operetta singers, folk dancers and a short csárdás lesson. '
                '<a href="%s" rel="noopener nofollow sponsored" target="_blank">Book →</a></li>'
                '<li>🎹 <strong>Piano Battle Show:</strong> from €91, two pianists who take requests. '
                '<a href="%s" rel="noopener nofollow sponsored" target="_blank">Book →</a></li></ul>'
                % (D.SL.format(slug="dinner-lights"), D.SL.format(slug="budapest-danube-dinner-cruise"),
                   D.SL.format(slug="dinner-cruise-piano-battle-show")))
        body = swap_block(body, r'<div class="dc-opts"', opts)
    body = remove_class_blocks(body, "dc-")
    body = swap_block(body, r'<div class="pro-con-box-wrapper"', proscons(c))
    body = swap_block(body, r'<div class="ltt-buy-card"', buycard(c))
    body = swap_block(body, r'<div class="qf1-wrap"', qf(c))
    if c["getthere"]:
        m = re.search(r"<h3>How to Get There</h3><ul[^>]*>", body)
        if m:
            end = balanced(body, m.start() + len("<h3>How to Get There</h3>"), "ul")
            body = body[:m.start()] + getthere(c) + body[end:]
        else:
            k = body.find('<div class="ltt-buy-card">')
            body = body[:k] + '<div class="w-richtext">%s</div>\n' % getthere(c) + body[k:]
    body = FIXES[c["key"]](body)
    body = re.sub(r'<a href="/best-night-cruises-budapest">([^<]*)</a>', r"\1", body)  # no self-links
    return body


# ── per-card corrections to the old first-hand copy (the live listing wins) ──────────
def fix_prosecco(b):
    b = re.sub(r'<div class="ltt-sp-card"><h4>About Rubin Group</h4>.*?</div>',
               '<div class="ltt-sp-card"><h4>About Duna-Weser</h4><ul role="list"><li>This ticket is now run by <strong>Duna-Weser Kft.</strong>, '
               'which also runs the River Diva dinner cruise (#5 on this list). I tested the cruise when Rubin Group ran it.</li></ul></div>', b, flags=re.S)
    b = b.replace("isn't worth the 10€ price", "wasn't worth the money")
    b = must(b, "Additionally, the <strong>meeting point</strong> is further from the city center, so getting there may take some extra time and effort.",
             "Additionally, the <strong>meeting point</strong> I used, north of Margaret Bridge, is further from the city center; two of today's three docks are central.")
    b = b.replace("The optional <strong>assorted food platter</strong> for 10€<strong> </strong>wasn't what I was expecting.",
                  "The optional <strong>assorted food platter</strong> I ordered wasn't what I was expecting.")
    return b


def fix_kisfaludy(b):
    b = must(b, "an <strong>English audio guide</strong> (via loudspeakers)",
             "an audio guide (via loudspeakers when I tested it; the current listing has a <strong>30-language online audio guide</strong> on your own phone)")
    b = re.sub(r"complimentary welcome drink\s*</strong>of your choice [—-] <strong>water, prosecco, orange juice or beer\.</strong>",
               "complimentary welcome drink</strong>. The current listing offers <strong>prosecco or orange juice</strong>.", b)
    b = re.sub(r"<strong>The cruise includes a complimentary welcome drink of your choice</strong>\s*(?:—|:)\s*water, prosecco, orange juice or beer\.",
                  "<strong>When I tested it, the welcome drink was water, prosecco, orange juice or beer.</strong> The current listing offers prosecco or orange juice.", b)
    b = re.sub(r'<div class="ltt-sp-card"><h4>About Dunai Sétahajózási Ltd\.</h4>.*?</div>',
               '<div class="ltt-sp-card"><h4>About Dunai Sétahajózási</h4><p>Dunai Sétahajózási (Duna Cruises) runs the Kisfaludy from Dock 10 by Elizabeth Bridge.</p></div>', b, flags=re.S)
    return b


def fix_legenda(b):
    b = b.replace("which is why it's number one on this list", "which is why it ranks so high on this list")
    b = re.sub(r"<li><strong>This boat is available from 16:30 onwards\.\s*</strong></li>", "", b)
    b = re.sub(r"<li>This boat is available from 16:30 onwards\.\s*</li>", "", b)
    b = b.replace("<li><strong>This boat is <strong>available from 16:30</strong> onwards.</strong></li>", "")
    b = b.replace('href="#budapest-river-cruise-deck"', 'href="#budapest-night-cruise-deck"')
    b = b.replace("360° views like Legenda, Rubin Group, and Portum.", "360° views, like Legenda's.")
    return b


def fix_silverline_sight(b):
    b = re.sub(r"\s*If it were not for their out-of-the-way location, I would recommend the <a [^>]*>Portum's similarly cheap cruise</a> in a heartbeat\.", "", b)
    b = re.sub(r"<p>There is an <strong>audio guide app available in 9 languages</strong>.*?</p>", "", b, count=1, flags=re.S)
    b = re.sub(r'<div class="ltt-sp-card"><h4>About Silverline Cruises Ltd\.</h4>.*?</div>',
               '<div class="ltt-sp-card"><h4>About Silverline Cruises</h4><p>Silverline runs sightseeing, dinner and drinks cruises from Dock 11 by Elizabeth Bridge.</p></div>', b, flags=re.S)
    return b


def fix_legenda_dinner(b):
    b = re.sub(r"<p>From June to August the best evenings sell out.*?</p>", "", b, count=1, flags=re.S)
    b = b.replace("Dokk 7, 1051 Budapest", "Dokk 7, 1052 Budapest")
    b = re.sub(r"Legenda is Budapest's premier river cruise operator with over 30 years on the Danube\s*,?",
               "Legenda City Cruises runs sightseeing boats and this dinner cruise from its own floating dock at Vigadó tér,", b)
    b = re.sub(r"(<strong>)?Legenda is Budapest's premier river cruise operator(</strong>)? with (<strong>)?over 30 years on the Danube(</strong>)?",
               "Legenda City Cruises runs sightseeing boats and this dinner cruise from its own floating dock at Vigadó tér", b)
    return b


def fix_silverline_dinner(b):
    b = re.sub(r"\s*We used to rank Silverline's three dinner cruises separately \(#2–#4\)\.", "", b)
    b = b.replace("Silverline is a solid company <strong>operating since 2011</strong> with a popular range of sightseeing and dining vessels on the Danube.",
                  "Silverline runs sightseeing, dinner and drinks cruises from Dock 11 by Elizabeth Bridge.")
    return b


FIXES = {"duna-weser-unlimited-prosecco": fix_prosecco, "kisfaludy-paddle-steamer": fix_kisfaludy,
         "legenda-danube-legend": fix_legenda, "silverline-sightseeing": fix_silverline_sight,
         "legenda-candlelit-dinner": fix_legenda_dinner, "silverline-dinner": fix_silverline_dinner}


def details_html(i, c):
    body = tested_body(c) if c["tested"] else new_body(c)
    return det_header(i, c) + body + "</div>\n</details>"


# ── text hygiene for everything we emit ──────────────────────────────────────────────
def no_em_dash(html):
    """Replace em dashes in visible text and attributes (scripts/styles untouched here)."""
    html = re.sub(r"\s*—\s*", ": ", html)
    return html.replace("&mdash;", ":")


# ── page assembly ────────────────────────────────────────────────────────────────────
def main():
    page = SRC["night"]
    cards = D.CARDS
    assert len(cards) == 10
    deck = "\n".join(deck_html(i, c) for i, c in enumerate(cards, 1))
    dets = "".join(details_html(i, c) for i, c in enumerate(cards, 1))
    deck, dets = no_em_dash(deck), no_em_dash(dets)

    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]

    n_tested = sum(c["tested"] for c in cards)
    cats = {k: sum(k in c["cat"].split() for c in cards) for k in ("sightseeing", "dinner", "prosecco", "tested")}
    untested_reviews = sum(cnt for c in cards if not c["tested"] for _, _, cnt, _ in c["ratings"])
    m_reviews = "{:,}+".format(untested_reviews // 100 * 100)

    title = "10 Best Night Cruises in Budapest in 2026 (%d Personally Tested)" % n_tested
    desc = ("The 10 best Budapest night cruises for 2026: evening sightseeing, dinner and unlimited prosecco boats. "
            "%d personally tested, from €11.40, prices and ratings checked 14 Nov 2026." % n_tested)

    # head
    page = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, page, count=1, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (title, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (desc, prop), page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)

    # hero
    page = re.sub(r'<span class="ltt-bc-current">[^<]*</span>', '<span class="ltt-bc-current">10 Best Night Cruises in Budapest (2026)</span>', page, count=1)
    page = page.replace('<span class="ltt-hero-kicker-badge">2026 Field-Tested Comparison</span>',
                        '<span class="ltt-hero-kicker-badge">2026 Night Cruise Comparison</span>')
    page = re.sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)',
                  r'\1\n      10 Best Night Cruises in Budapest in 2026 <span class="ltt-h1-muted">(%d Personally Tested)</span>\n\2' % n_tested,
                  page, count=1, flags=re.S)
    page = re.sub(r'(<div class="ltt-author-line">\s*By <a href="/about" target="_blank">Adam Dimitrov</a>)\s*—\s*',
                  r"\1, ", page, count=1)
    page = re.sub(r'<div class="ltt-author-role">[^<]*</div>',
                  '<div class="ltt-author-role">%d of 10 Cruises Tested in Person • Live Prices &amp; Ratings Checked 14 Nov 2026</div>' % n_tested,
                  page, count=1)
    page = re.sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 14, 2026<", page, count=1)
    lead = f'''<div class="ltt-lead-copy">
<p>Looking for the best way to see Budapest lit up from the Danube? This guide compares the <strong>10 best evening and night cruises</strong> in three groups: <strong>sightseeing cruises</strong>, <strong>dinner cruises</strong> and <strong>unlimited prosecco cruises</strong>.</p>
<p>I <strong>personally tested {n_tested} of these 10 cruises</strong>, with my own photos and notes. I compared the other {10 - n_tested} using their live booking listings and <strong>{m_reviews} verified reviews</strong>. Every price, departure time and rating was checked on the live listings on 14 November 2026.</p>
<p>Want the full daytime and nighttime picture? See the <a href="/best-budapest-river-cruises">10 best Budapest river cruises</a>, the <a href="/best-dinner-cruises-budapest">best dinner cruises</a> and the <a href="/unlimited-prosecco-cruises-budapest">unlimited prosecco cruises</a>.</p>
</div>'''
    page = swap_block(page, r'<div class="ltt-lead-copy">', lead)
    pills = (f'''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems('all', this)" type="button">All (10)</button>
<button class="ltt-tab-btn" data-cat="sightseeing" onclick="lttFilterItems('sightseeing', this)" type="button">Sightseeing ({cats["sightseeing"]})</button>
<button class="ltt-tab-btn" data-cat="dinner" onclick="lttFilterItems('dinner', this)" type="button">Dinner ({cats["dinner"]})</button>
<button class="ltt-tab-btn" data-cat="prosecco" onclick="lttFilterItems('prosecco', this)" type="button">Prosecco ({cats["prosecco"]})</button>
<button class="ltt-tab-btn" data-cat="tested" onclick="lttFilterItems('tested', this)" type="button">Personally Tested ({cats["tested"]})</button>
</div>''')
    page = swap_block(page, r'<div class="ltt-integrated-pills">', pills)
    page = page.replace("Personally field-tested • All reviews open by default",
                        "%d of 10 personally tested • All reviews open by default" % n_tested)
    page = re.sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                  r"\1Detailed Breakdown: 10 Best Night Cruises in Budapest\2", page)

    # runtime config (titles used by the TOC / jump sheet)
    cfg = {"deckId": "budapest-night-cruise-deck", "tocDeckLabel": "Top 10 Night Cruises",
           "tocBreakdownLabel": "Detailed Breakdown (10 Night Cruises)",
           "shortTitles": [c["short"].replace("&amp;", "&") for c in cards]}
    page = re.sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, count=1, flags=re.S)

    # dead legacy Webflow script that stamped "Personally Tested" on every table row
    page = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const cruiseCards = .*?</script>', "", page, count=1, flags=re.S)
    # sticky bar starts on card 1
    c1 = cards[0]
    page = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">)[^<]*(</span>)', r"\g<1>%s\2" % c1["short"], page, count=1)
    page = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">)[^<]*(</span>)', r"\g<1>From €%s\2" % c1["price"], page, count=1)
    page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="sticky-cta-btn")', r"\g<1>%s\2" % book_url(c1, "sticky"), page, count=1)

    page = re.sub(r'(<span class="hybrid-active-title" id="hybridActiveTitle">)[^<]*(</span>)', r"\g<1>%s\2" % c1["short"], page, count=1)
    page = re.sub(r'(<span class="hybrid-active-price" id="hybridActivePrice">)[^<]*(</span>)', r"\g<1>From €%s\2" % c1["price"], page, count=1)
    page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="hybridActiveCta")', r"\g<1>%s\2" % book_url(c1, "sticky"), page, count=1)

    # JSON-LD
    page = build_jsonld(page, cards, title, desc)
    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", PAGE, len(page))


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&rsquo;", "’")


def build_jsonld(page, cards, title, desc):
    i = page.find('id="ltt-schema-jsonld"')
    a = page.find(">", i) + 1
    b = page.find("</script>", a)
    data = json.loads(page[a:b])
    url = SITE + "/best-night-cruises-budapest"
    items = []
    for pos, c in enumerate(cards, 1):
        avg, tot = wavg(c["ratings"])
        prod = {
            "@type": "Product",
            "name": strip_tags(c["title"]),
            "description": "%s: %s" % (strip_tags(c["rank"]).split(" ", 1)[1], strip_tags(c["pick"])),
            "brand": {"@type": "Organization", "name": c["operator"]},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                "worstRating": "1", "reviewCount": str(tot)},
            "offers": {"@type": "Offer", "price": c["price"], "priceCurrency": "EUR",
                       "availability": "https://schema.org/InStock",
                       "url": book_url(c, "schema").replace("&amp;", "&")},
        }
        if c["tested"]:
            prod["review"] = {
                "@type": "Review",
                "author": {"@type": "Person", "name": "Adam Dimitrov", "url": SITE + "/about"},
                "datePublished": TODAY,
                "reviewBody": strip_tags(c["pick"]).capitalize(),
                "positiveNotes": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": k, "name": strip_tags("%s: %s" % p)} for k, p in enumerate(c["pros"], 1)]},
                "negativeNotes": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": k, "name": strip_tags("%s: %s" % p)} for k, p in enumerate(c["cons"], 1)]},
            }
        items.append({"@type": "ListItem", "position": pos, "url": "%s#%s" % (url, c["anchor"]), "item": prod})
    for node in data["@graph"]:
        if node.get("@type") == "Article":
            node["headline"] = title
            node["description"] = desc
            node["dateModified"] = TODAY
            node["mainEntity"]["name"] = title
            node["mainEntity"]["description"] = strip_tags(desc)
            node["mainEntity"]["numberOfItems"] = len(cards)
            node["mainEntity"]["itemListElement"] = items
            node["image"] = [x for x in node.get("image", []) if "legenda-sightseeing" not in x] or node.get("image")
        if node.get("@type") == "BreadcrumbList":
            for it in node.get("itemListElement", []):
                if "Night Cruises" in it.get("name", ""):
                    it["name"] = "10 Best Night Cruises in Budapest (2026)"
    out = json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")
    return page[:a] + out + page[b:]


if __name__ == "__main__":
    main()
