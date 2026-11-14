#!/usr/bin/env python3
"""Rebuild /best-dinner-cruises-budapest (EN) from scripts/dinner_cruises_2026_data.py.

Adapted from the night cruises rebuild. Tested cards (1 to 3) reuse their own photos and
first-hand copy, with the facts corrected to today's listings. Cards 4 to 6 are written from
the live listings. Run from the repo root against the origin/main version of the page:
    python3 scripts/build_dinner_cruises_2026.py
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dinner_blocks import balanced, deck_card, details_card, all_spans  # noqa: E402
import dinner_cruises_2026_data as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "best-dinner-cruises-budapest.html")
TODAY = "2026-11-14"
SITE = "https://www.budapestadventures.com"


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


SRC = {"river": rd("best-budapest-river-cruises.html"),
       "dinner": rd("best-dinner-cruises-budapest.html")}
if "dinner-cruises-2026/" in SRC["dinner"]:
    sys.exit("Page already rebuilt; run against the origin/main version (git checkout origin/main -- best-dinner-cruises-budapest.html).")

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
DET_ICON = {"GetYourGuide": _icons_in_det[0], "Viator": _icons_in_det[1]}
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
    if b == "legenda_dinner":
        return D.LEGENDA_DINNER
    if b == "silverline_dinner":
        return D.SL.format(slug="dinner-lights")
    raise ValueError(b)


def maps(q):
    return D.MAPS.format(q=q.replace(" ", "+")).replace("&", "&amp;")


def stars(s):
    half = round(s * 2) / 2
    full = int(half)
    out = STAR_FULL * full + (STAR_HALF if half - full else "")
    return out


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
        if c.get("order"):  # lead with the most selling photo; drop logos and duplicates
            imgs = [imgs[k - 1] for k in c["order"]]
        imgs = imgs[:12]  # the reference keeps 8 to 12 photos per card
        fixed = []
        for k, im in enumerate(imgs):
            real = (re.search(r'data-src="([^"]+)"', im) or re.search(r'src="([^"]+)"', im)).group(1)
            alt = re.search(r'alt="([^"]*)"', im).group(1)
            if k == 0:
                fixed.append('<img alt="%s" fetchpriority="high" height="534" loading="eager" sizes="%s" src="%s" width="800"/>' % (alt, SIZES, real))
            else:
                fixed.append('<img alt="%s" data-src="%s" decoding="async" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>'
                             % (alt, real, SIZES, PLACEHOLDER))
        head = slider[:slider.find("<img ")]
        slider = head + "\n".join(fixed) + "</div>"
        n = len(re.findall(r"<img ", slider))
        slider = re.sub(r'aria-label="Photo gallery \d+"', 'aria-label="Photo gallery %d"' % i, slider)
    else:
        imgs = []
        for k in range(1, c["nphotos"] + 1):
            p = "/assets/dinner-cruises-2026/%s-%02d.avif" % (c["photos"], k)
            alt = c["alt"]
            if k == 1:
                imgs.append('<img alt="%s" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>' % (alt, SIZES, p))
            else:
                imgs.append('<img alt="%s" data-src="%s" decoding="async" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>'
                            % (alt, p, SIZES, PLACEHOLDER))
        n = len(imgs)
        slider = ('<div aria-label="Photo gallery %d" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">\n%s</div>'
                  % (i, "\n".join(imgs)))
    return ('<div class="bpa-media">\n%s\n%s<span class="bpa-pill">1 / %d</span>%s\n</div>' % (tag, arrows, n, slider))


def rate_block(c):
    avg, tot = wavg(c["ratings"])
    nsites = len(c["ratings"])
    badges = []
    for site, s, cnt, link in c["ratings"]:
        inner = ('%s<span class="bpa-rev-site">%s</span><span class="bpa-rev-score">%s</span><span class="bpa-rev-count">(%s)</span>'
                 % ("\n" + ICON[site], site, score1(s), fmt_count(cnt)))
        # OTA review entries link out only when the card has no direct operator booking link
        # (Legenda / Silverline pay a higher commission, so their clicks stay on the CTA).
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
                       '<span class="bpa-lang-note">%s '
                       '<a href="#%s">Full review ↓</a></span></div></details>\n' % (c["tested_pop"], c["tested_note"], c["anchor"]))
    kicker = ('%s • ⏱️ %s • <a class="bpa-kicker-map-link" href="%s" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">%s</a>'
              % (c["operator"], c["duration"], maps(c["pier_q"]), c["pier"]))
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    return f'''<div class="bpa-card" data-cat="{c["cat"]}" id="card-{i}">
<div class="bpa-main">
{media(i, c)}
<div class="bpa-info">
<div class="bpa-kicker">{kicker}</div>
<a class="bpa-title" href="{title_href}" rel="noopener" target="_blank">{c["title"]}</a>
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
<a class="bpa-btn" href="{book_url(c, "button")}" rel="noopener" target="_blank">Check Availability →</a>
<div class="bpa-via">Booked securely via {c["via"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{c["anchor"]}">Read Review ↓</a>
</div>
</div>
</div>'''


# ── details card ─────────────────────────────────────────────────────────────────────
def det_header(i, c):
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
{rate_block(c)}{proof}
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
    faq = "".join("<blockquote>❓ <strong>%s</strong><br/>💡 %s</blockquote>" % qa for qa in c["faq"])
    paras = "".join("<p>%s</p>" % p for p in c["summary"])
    quotes = ""
    if c["quotes"]:
        quotes = "<blockquote><strong>What guests say:</strong><br/>%s</blockquote>" % "<br/>".join(
            "“%s” <em>(%s, %s)</em>" % qq for qq in c["quotes"])
    summary = ('<div class="w-richtext">%s%s%s%s</div>\n%s'
               % (faq, paras, quotes, getthere(c), buycard(c)))
    cards = []
    for h, img, txt in c["spcards"]:
        im = ""
        if isinstance(img, str):
            im = '<img alt="%s" loading="lazy" src="%s"/>' % (c["alt"], img)
        elif img:
            im = ('<img alt="%s" loading="lazy" src="/assets/dinner-cruises-2026/%s-%02d.avif"/>' % (c["alt"], c["photos"], img))
        cards.append('<div class="ltt-sp-card"><h4>%s</h4>%s<ul role="list"><li>%s</li></ul></div>' % (h, im, txt))
    onboard = '<div class="ltt-sub-points">\n%s\n</div>' % "\n".join(cards)
    return (proscons(c) + "\n" + bento("Summary &amp; Review", "Overview", summary) + "\n"
            + bento("On Board: Dining Room, Menu, Show &amp; Route", "From the Listing", onboard) + "\n" + qf(c) + "\n")


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
    # the dinner page keeps its dc-* menu widgets (their CSS lives on this page)
    body = swap_block(body, r'<div class="pro-con-box-wrapper"', proscons(c))
    body = swap_block(body, r'<div class="ltt-buy-card"', buycard(c))
    body = swap_block(body, r'<div class="qf1-wrap"', qf(c))
    body = replace_getthere(body, c)
    body = FIXES[c["key"]](body)
    return body


def replace_getthere(body, c):
    """Swap the old 'Departure Pier' list for the sourced How to Get There list."""
    m = re.search(r'<ul role="list"><li><strong>Meeting point:</strong>', body)
    if not m:
        m = re.search(r'<ul role="list"><li>Meeting point:', body)
    if m:
        end = balanced(body, m.start(), "ul")
        return body[:m.start()] + '<h3>How to Get There</h3><ul role="list">%s</ul>' % "".join("<li>%s</li>" % x for x in c["getthere"]) + body[end:]
    k = body.find('<div class="ltt-buy-card">')
    return body[:k] + '<div class="w-richtext">%s</div>\n' % getthere(c) + body[k:]


def must_re(b, pat, rep, flags=re.S):
    nb, n = re.subn(pat, rep, b, count=1, flags=flags)
    if not n:
        raise ValueError("pattern not found: %r" % pat[:80])
    return nb


# ── per-card corrections to the old first-hand copy (the live listing wins) ──────────
def about(b, old_h4, new_h4, text):
    return must_re(b, r'<h4>%s</h4>\s*<p>.*?</p>' % re.escape(old_h4), '<h4>%s</h4><p>%s</p>' % (new_h4, text))


def fix_legenda_dinner(b):
    b = must_re(b, r"<p>From June to August the best evenings sell out.*?</p>",
                "<p>Book a few days ahead: on 14 November 2026, GetYourGuide showed <strong>only 1 spot left</strong> for Saturday 28 November.</p>")
    b = about(b, "About Legenda City Cruises", "About Legenda City Cruises",
              "Legenda City Cruises runs sightseeing boats and this candlelit dinner cruise from its own floating dock at Vigadó tér (Dock 7).")
    b = b.replace("checked Nov 10, 2026", "checked Nov 14, 2026")
    b = b.replace('href="https://legenda.hu/en?partner=38585"', 'href="%s"' % D.LEGENDA_DINNER)
    # the gallery shows dishes from my test dinner, which are no longer on the menu
    b = must_re(b, r'(<div class="ltt-strip-cap"><span>)4-Course served dinner menu with a choice of starter, soup, main course, and dessert\.',
                r"\g<1>From my test dinner: 4 courses with a choice of starter, soup, main course and dessert. The menu has changed since; the current menu is below.")
    return b


def fix_silverline_dinner(b):
    b = must_re(b, r"<strong>One listing, three evenings\.</strong> We used to rank Silverline's three dinner cruises separately \(#2[–-]#4\)\.\s*",
                "<strong>One boat, three evenings.</strong> ")
    b = b.replace("🎹 Piano Battle Show", "🎹 Live Piano Show")
    b = b.replace("Two pianists duel, take your requests", "Not bookable in Nov or Dec 2026")
    b = b.replace("Show: none, Folk &amp; Operetta, or Piano Battle", "Show: none, Folk &amp; Operetta, or the Live Piano Show")
    b = must_re(b, r'(<span class="ltt-mini-pill">)Live Piano Duel(</span>)', r"\1Not bookable Nov–Dec 2026\2")
    b = must_re(b, r"(<h4>🎹 Piano Battle Performance</h4>)",
                r"\1<p>Silverline now lists this evening as the <strong>Live Piano Show</strong> (from €91). Its calendar had no bookable dates in November or December 2026 when I checked on 14 November.</p>")
    b = about(b, "About Silverline Cruises", "About Silverline Cruises",
              "Silverline runs sightseeing, dinner and drinks cruises from Dock 11 next to Elizabeth Bridge.")
    b = b.replace("checked Nov 10, 2026", "checked Nov 14, 2026")
    b = must_re(b, r"(<p>On the <strong>Folk &amp; Operetta</strong> and <strong>Piano Battle</strong> evenings.*?)</p>",
                r"\1 The Live Piano Show had no bookable dates in November or December 2026 when I checked on 14 November.</p>")
    return b


def fix_hungaria(b):
    b = b.replace("from €79 per person", "from €67 per person (was €79)")
    b = re.sub(r'href="https://budapestxplore\.com/[^"]*"', 'href="%s"' % gyg(CARD_BY_KEY["hungaria-koncert-dinner"], "menu"), b)
    b = b.replace("Chicken leg paprikash, potato gratin, fresh salad, pickles", "Chicken breast paprikash, potato gratin, fresh salad, pickles")
    b = b.replace("Source: Hungária Koncert's 2026 served-dinner menus (via reseller listing), checked Nov 10, 2026",
                  "Source: Hungária Koncert's GetYourGuide listing, checked Nov 14, 2026")
    b = b.replace("Since summer 2026 Hungária Koncert serves", "Hungária Koncert now serves")
    b = b.replace("Served at your table since summer 2026 (was a buffet)", "Served at your table (it was a buffet when I tested it)")
    b = must_re(b, r"<p>Boarding opens at 18:30, half an hour before departure\. <strong>Get there 30 to 45 minutes early</strong>:",
                "<p>The listing asks you to arrive at least 15 minutes before the 19:00 departure. <strong>Get there 30 to 45 minutes early</strong>:")
    b = about(b, "About Hungaria Koncert", "About Hungária Koncert",
              "Hungária Koncert runs the Gróf Széchenyi and the Stadt Wien from Akadémia 2, with Rajkó folk musicians on board.")
    return b


CARD_BY_KEY = {c["key"]: c for c in D.CARDS}
FIXES = {"legenda-candlelit": fix_legenda_dinner, "silverline-dinner": fix_silverline_dinner,
         "hungaria-koncert-dinner": fix_hungaria}


def details_html(i, c):
    body = tested_body(c) if c["tested"] else new_body(c)
    return det_header(i, c) + body + "</div>\n</details>"


# ── text hygiene for everything we emit ──────────────────────────────────────────────
AFF = re.compile(r'(getyourguide\.com|viator\.com|tripadvisor\.|tiqets\.com|legenda\.hu/[^"]*partner=|budapestrivercruise\.eu/[^"]*code=|fareharbor\.com)')


def aff_rel(html):
    """Every affiliate or OTA link gets rel="nofollow sponsored noopener" (keeps target=_blank)."""
    def fix(m):
        tag = m.group(0)
        href = re.search(r'href="([^"]*)"', tag)
        if not href or not AFF.search(href.group(1)):
            return tag
        tag = re.sub(r'\srel="[^"]*"', "", tag)
        return tag[:-1] + ' rel="nofollow sponsored noopener">'
    return re.sub(r"<a\b[^>]*>", fix, html)


def no_em_dash(html):
    """Replace em dashes in visible text and attributes (scripts/styles untouched here)."""
    html = re.sub(r"\s*—\s*", ": ", html)
    return html.replace("&mdash;", ":")


# ── page assembly ────────────────────────────────────────────────────────────────────
def fix_howto(page):
    """The 'How to choose' block after the breakdowns: keep it, but only with checked facts."""
    page = page.replace("FIELD TESTING METHODOLOGY", "HOW TO CHOOSE")
    page = page.replace('Four factors we look at when <a href="/best-dinner-cruise-budapest">comparing Budapest dinner cruises</a>.',
                        'Four things to decide before you book. Short on time? See <a href="/best-dinner-cruise-budapest">the one dinner cruise I&rsquo;d book</a>.')
    page = page.replace("Jump to Tested Budapest Dinner Cruise", "Jump to a Budapest Dinner Cruise")

    def card(old_title, new_title, body):
        nonlocal page
        pat = (r'<h3 class="ltt-card-title">%s</h3>(\s*</div>\s*<div class="ltt-card-body">)(.*?)(</div>)'
               % re.escape(old_title))
        page, k = re.subn(pat, lambda m: '<h3 class="ltt-card-title">%s</h3>%s\n<p>%s</p>\n%s' % (new_title, m.group(1), body, m.group(3)),
                          page, count=1, flags=re.S)
        if not k:
            raise ValueError("how-to card not found: " + old_title)

    card("Fresh Onboard Cooking vs. Banquet Catering", "Served Courses vs. Buffet",
         "Legenda, Silverline, Hungária Koncert and the Dock 6 cruise serve <strong>plated courses at your table</strong>; River Diva is a <strong>seasonal buffet</strong> with unlimited drinks. When I tested Silverline, the food was prepared in the ship&rsquo;s own kitchen.")
    card("Window Sightlines vs. Center Tables", "Window Tables",
         "Window tables are <strong>not guaranteed</strong> on most boats. Silverline sells them for +€15 (Dinner &amp; Lights) or +€25 (Folk &amp; Operetta); River Diva says tables follow booking size. On Hungária Koncert, boarding early gives you the best chance of a window.")
    card("Acoustic Balance: Lounge vs. Show", "Quiet Music or a Full Show",
         "Decide between quiet conversation (Legenda&rsquo;s live lounge music, Silverline&rsquo;s background music) and a <strong>full show</strong> (Hungária Koncert&rsquo;s Rajkó folk show, the Dock 6 folk dancers or Silverline&rsquo;s Folk &amp; Operetta evening).")
    page = re.sub(r"(In summer \(June–August\), dusk does not settle until 20:45, making 20:30–21:00 the optimal booking window\.)",
                  r"\1 River Diva&rsquo;s listing notes that landmark floodlighting is set by the city and can&rsquo;t be guaranteed on a given night.",
                  page, count=1)
    return page


def main():
    page = SRC["dinner"]
    cards = D.CARDS
    n = len(cards)
    deck = "\n".join(deck_html(i, c) for i, c in enumerate(cards, 1))
    dets = "".join(details_html(i, c) for i, c in enumerate(cards, 1))
    deck, dets = no_em_dash(deck), no_em_dash(dets)

    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]

    n_tested = sum(c["tested"] for c in cards)
    cats = {k: sum(k in c["cat"].split() for c in cards) for k in ("under80", "served", "buffet", "drinks", "veg", "tested")}
    untested_reviews = sum(cnt for c in cards if not c["tested"] for _, _, cnt, _ in c["ratings"])
    m_reviews = "{:,}+".format(untested_reviews // 100 * 100)

    title = "%d Best Dinner Cruises in Budapest in 2026 (%d Personally Tested)" % (n, n_tested)
    desc = ("The %d best Budapest dinner cruises for 2026, from a €44 goulash cruise to a €110 candlelit dinner. "
            "%d personally tested; menus, prices and ratings checked 14 Nov 2026." % (n, n_tested))

    # head
    page = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, page, count=1, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (title, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (desc, prop), page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)

    # hero
    page = re.sub(r'<span class="ltt-bc-current">[^<]*</span>', '<span class="ltt-bc-current">%d Best Dinner Cruises in Budapest (2026)</span>' % n, page, count=1)
    page = re.sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)',
                  r'\1\n      %d Best Dinner Cruises in Budapest in 2026 <span class="ltt-h1-muted">(%d Personally Tested)</span>\n\2' % (n, n_tested),
                  page, count=1, flags=re.S)
    page = re.sub(r'(<div class="ltt-author-line">\s*By <a href="/about" target="_blank">Adam Dimitrov</a>)\s*—\s*',
                  r"\1, ", page, count=1)
    page = re.sub(r'<div class="ltt-author-role">[^<]*</div>',
                  '<div class="ltt-author-role">%d of %d Dinner Cruises Tested in Person • Live Menus, Prices &amp; Ratings Checked 14 Nov 2026</div>' % (n_tested, n),
                  page, count=1)
    page = re.sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 14, 2026<", page, count=1)
    c1 = cards[0]
    lead = f'''<div class="ltt-lead-copy">
<p>Looking for the best dinner cruise in Budapest? This guide compares the <strong>{n} best Danube dinner cruises</strong>, from a €44 goulash and lángos cruise to Legenda&rsquo;s €110 candlelit 4-course dinner, with the menus, shows, docks and prices of each.</p>
<p>I <strong>personally tested {n_tested} of these {n} cruises</strong> (Legenda, Silverline and Hungária Koncert), with my own photos and notes. I compared the other {n - n_tested} using their live booking listings and <strong>{m_reviews} verified reviews</strong>. Every price, departure time, menu and rating was checked on the live listings on 14 November 2026.</p>
<p><strong>Quick answer:</strong> the best dinner cruise in Budapest is <a href="#{c1["anchor"]}">Legenda&rsquo;s candlelit 4-course dinner cruise</a> (€110, 2.5 hours, Dock 7). Not after a full dinner? See the <a href="/best-budapest-river-cruises">best Budapest river cruises</a> instead.</p>
</div>'''
    page = swap_block(page, r'<div class="ltt-lead-copy">', lead)
    pills = (f'''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems('all', this)" type="button">All ({n})</button>
<button class="ltt-tab-btn" data-cat="under80" onclick="lttFilterItems('under80', this)" type="button">Under €80 ({cats["under80"]})</button>
<button class="ltt-tab-btn" data-cat="served" onclick="lttFilterItems('served', this)" type="button">Served at Your Table ({cats["served"]})</button>
<button class="ltt-tab-btn" data-cat="drinks" onclick="lttFilterItems('drinks', this)" type="button">Unlimited Drinks ({cats["drinks"]})</button>
<button class="ltt-tab-btn" data-cat="veg" onclick="lttFilterItems('veg', this)" type="button">🌱 Vegetarian Option ({cats["veg"]})</button>
<button class="ltt-tab-btn" data-cat="tested" onclick="lttFilterItems('tested', this)" type="button">Personally Tested ({cats["tested"]})</button>
</div>''')
    page = swap_block(page, r'<div class="ltt-integrated-pills">', pills)
    page = page.replace("Personally field-tested • All reviews open by default",
                        "%d of %d personally tested • All reviews open by default" % (n_tested, n))
    page = re.sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                  r"\1Detailed Breakdown: %d Best Dinner Cruises in Budapest\2" % n, page)
    page = fix_howto(page)

    # runtime config (titles used by the TOC / jump sheet)
    cfg = {"deckId": "budapest-dinner-cruise-deck", "tocDeckLabel": "Top %d Dinner Cruises Comparison" % n,
           "tocBreakdownLabel": "Detailed Breakdown (%d Dinner Cruises)" % n,
           "shortTitles": [c["short"].replace("&amp;", "&") for c in cards]}
    page = re.sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, count=1, flags=re.S)

    # the deck's "Full menu" buttons are gone, so their stale menu templates go too
    page = re.sub(r'<template id="dc-menu-[^"]*"[^>]*>.*?</template>', "", page, flags=re.S)

    # sticky bar starts on card 1
    for tid, pid, cid in (("sticky-name", "sticky-price", "sticky-cta-btn"),
                          ("hybridActiveTitle", "hybridActivePrice", "hybridActiveCta")):
        page = re.sub(r'(<span class="hybrid-active-title" id="%s">)[^<]*(</span>)' % tid, r"\g<1>%s\2" % c1["short"], page, count=1)
        page = re.sub(r'(<span class="hybrid-active-price" id="%s">)[^<]*(</span>)' % pid, r"\g<1>From €%s\2" % c1["price"], page, count=1)
        page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="%s")' % cid, r"\g<1>%s\2" % book_url(c1, "sticky"), page, count=1)

    # JSON-LD
    page = build_jsonld(page, cards, title, desc)
    page = aff_rel(page)
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
    url = SITE + "/best-dinner-cruises-budapest"
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
                "reviewBody": (lambda t: t[:1].upper() + t[1:])(strip_tags(c["pick"])),
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
        if node.get("@type") == "BreadcrumbList":
            for it in node.get("itemListElement", []):
                if "Dinner Cruises" in it.get("name", ""):
                    it["name"] = "%d Best Dinner Cruises in Budapest (2026)" % len(cards)
    out = json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")
    return page[:a] + out + page[b:]


if __name__ == "__main__":
    main()
