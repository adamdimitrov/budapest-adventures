#!/usr/bin/env python3
"""Rebuild /thermal-baths-budapest (EN) from scripts/thermal_baths_data.py.

Markup, classes, pills and slider follow /best-budapest-river-cruises (the reference page).
Run from the repo root against the origin/main version of the page:
    python3 scripts/build_thermal_baths_2026.py
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from night_blocks import balanced, deck_card, details_card, all_spans  # noqa: E402
import thermal_baths_data as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "thermal-baths-budapest.html")
TODAY = "2026-11-14"
SITE = "https://www.budapestadventures.com"


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


SRC = {"page": rd("thermal-baths-budapest.html"), "river": rd("best-budapest-river-cruises.html")}
if 'id="item-2-rudas"' in SRC["page"]:
    sys.exit("Page already rebuilt; run against origin/main (git checkout origin/main -- thermal-baths-budapest.html).")

# ── shared bits from the reference page ──────────────────────────────────────────────
_ref_card = deck_card(SRC["river"], "card-2")
ICON = {m.group(1): m.group(0) for m in re.finditer(r'<img alt="([^"]+)" class="bpa-rev-icon"[^>]*>', _ref_card)}
ICON["Tiqets"] = '<img alt="Tiqets" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/652d0405192ba076b04f74a3/6852917a8b23e16d4296b394_tiqets-logo.avif"/>'
ICON["Google"] = '<img alt="Google" class="bpa-rev-icon" loading="lazy" src="/assets/cdn/60e43c7d6d05b671dff0dc1a/65350288cf6e222fd93f3743_google-icon.png"/>'
_ref_det = details_card(SRC["river"], "cruise-2-rubingroup")
_svgs = re.findall(r'<svg aria-hidden="true" viewbox="0 0 24 24"><path d="[^"]+"></path></svg>', _ref_det)
STAR_FULL = _svgs[0]
STAR_HALF = next(s for s in _svgs if "V15.968" in s)
DET_ICON = {k: re.search(r'src="([^"]+)"', v).group(1) for k, v in ICON.items()}
LOCK_SVG = re.search(r'<svg fill="none"[^>]*>.*?</svg>', _ref_det, re.S).group(0)
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"
PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"


def ref_block(pat):
    m = re.search(pat, SRC["river"], re.S)
    return m.group(0)


REF_CSS = [ref_block(r'<style id="bpa-lang-css">.*?</style>'), ref_block(r'<style id="bpa-card2-css">.*?</style>')]
REF_JS = ref_block(r'<script id="bpa-lang-js">.*?</script>')


# ── formatting helpers ───────────────────────────────────────────────────────────────
def fmt_count(n):
    """Badge count, never rounded up: 29207 -> 29.2k+, 470 -> 470+, 27 -> 20+."""
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


def gyg(c, placement):
    return amp(D.GYG.format(slug=c["gyg_slug"], placement=placement, key=c["key"]))


def book_url(c, placement):
    if c["book"] == "gyg":
        return gyg(c, placement)
    return amp(c["official_url"])


def book_rel(c):
    return "noopener nofollow sponsored" if c["book"] == "gyg" else "noopener"


def site_url(c, r):
    site, _, _, kind, slug = r
    if kind == "gyg":
        return gyg(c, "rating")
    if kind == "tiqets":
        return amp(D.TIQETS.format(slug=slug))
    if kind == "viator":
        return amp(D.VIATOR.format(slug=slug, key=c["key"]))
    return amp(slug)  # google: full Maps URL


def price_txt(c):
    return "From €%s" % c["price"] if c.get("price") else "From %s" % c["price_label"]


def maps(q):
    import urllib.parse
    return amp(D.MAPS.format(q=urllib.parse.quote_plus(q)))


def stars(s):
    half = round(s * 2) / 2
    full = int(half)
    return STAR_FULL * full + (STAR_HALF if half - full else "")


# ── deck card ────────────────────────────────────────────────────────────────────────
def media(i, c):
    tag = '<span class="bpa-rank-tag %s">%s</span>' % (c["color"], c["rank"])
    arrows = ('<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>'
              '<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>')
    imgs = []
    for k, p in enumerate(c["photos"][:12]):
        if k == 0:
            extra = ' fetchpriority="high" loading="eager"' if i == 1 else ' loading="lazy"'
            imgs.append('<img alt="%s"%s height="534" sizes="%s" src="%s" width="800"/>' % (c["alt"], extra, SIZES, p))
        else:
            imgs.append('<img alt="%s" data-src="%s" decoding="async" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>'
                        % (c["alt"], p, SIZES, PLACEHOLDER))
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
        rel = "noopener nofollow" if site == "Google" else "noopener nofollow sponsored"
        badges.append('<a class="bpa-rev-badge is-link" href="%s" rel="%s" target="_blank">%s'
                      '<span class="bpa-rev-go" aria-hidden="true">→</span></a>' % (site_url(c, r), rel, inner))
    if nsites > 1:
        head = "Average of %d sites, weighted by number of reviews" % nsites
        meta = "%s reviews · %d sites" % (fmt_total(tot), nsites)
    else:
        head = "Rating on %s" % (c["ratings"][0][0] + (" Maps" if c["ratings"][0][0] == "Google" else ""))
        meta = "%s reviews · %s" % (fmt_total(tot), c["ratings"][0][0])
    note = ""
    if any(r[0] == "Viator" for r in c["ratings"]):
        note = '<span class="bpa-lang-note">Viator&rsquo;s count includes Tripadvisor reviews. Each site rates its own ticket for this bath.</span>'
    elif nsites > 1:
        note = '<span class="bpa-lang-note">Each site rates its own ticket for this bath.</span>'
    return ('<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            '<span class="bpa-stars" style="--r:%.2f" aria-hidden="true"></span><b class="bpa-rate-score">%s</b>'
            '<span class="bpa-rate-meta">%s</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong><span class="bpa-rate-list">%s</span>%s</div></details></div>'
            % (avg, score1(avg), meta, head, "".join(badges), note))


def deck_html(i, c):
    tested_pill = proof = ""
    if c["tested"]:
        proof = '\n<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>'
        tested_pill = ('<details class="bpa-lang bpa-tested bpa-proof-mobile"><summary class="bpa-vchip bpa-proof-mobile">✓ Personally Tested'
                       '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s'
                       '<span class="bpa-lang-note">What I checked: pools, changing rooms, crowds and value for money. '
                       '<a href="#%s">Full review ↓</a></span></div></details>\n' % (c["tested_pop"], c["anchor"]))
    kicker = ('%s • ⏱️ %s • <a class="bpa-kicker-map-link" href="%s" onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">%s</a>'
              % (c["area"], c["time"], maps(c["maps_q"]), c["transport"]))
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    pills = "\n".join(p.replace("{sparty}", amp(D.GYG.format(slug="budapest-the-ultimate-late-night-spa-party-ticket-t386559",
                                                             placement="sparty", key=c["key"]))) for p in c["pills"])
    btn = "Check Availability →" if c["book"] == "gyg" else "Official Prices →"
    return f'''<div class="bpa-card" data-cat="{c["cat"]}" id="card-{i}">
<div class="bpa-main">
{media(i, c)}
<div class="bpa-info">
<div class="bpa-kicker">{kicker}</div>
<a class="bpa-title" href="{book_url(c, "card")}" rel="{book_rel(c)}" target="_blank">{c["title"]}</a>
<div class="bpa-reviews-line">
{rate_block(c)}{proof}
</div>
<div class="bpa-specs-row">
{tested_pill}{pills}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {c["pick"]} <span class="bpa-skip">✕ Skip it</span> {c["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{price_txt(c)}</div>
<div class="bpa-psub">{c["psub"]}</div>
</div>
<a class="bpa-btn" href="{book_url(c, "button")}" rel="{book_rel(c)}" target="_blank">{btn}</a>
<div class="bpa-via">{"Booked securely via " if c["book"] == "gyg" else "Tickets sold at "}{c["via"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{c["anchor"]}">Read Review ↓</a>
</div>
</div>
</div>'''


# ── details card ─────────────────────────────────────────────────────────────────────
def det_header(i, c):
    badges = []
    for r in c["ratings"]:
        site, s, cnt = r[0], r[1], r[2]
        badges.append('<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="%s"/>'
                      '<span class="bpa-rev-score">%s</span><span class="bpa-rev-stars">%s</span><span class="bpa-rev-count">(%s)</span></span>'
                      % (DET_ICON[site], score1(s), stars(s), fmt_count(cnt)))
    proof = '\n<div class="bpa-proof"><span class="bpa-vchip">✓ Personally Tested</span></div>' if c["tested"] else ""
    return f'''<details class="bpa-details-card" data-cat="{c["cat"]}" id="{c["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {c["color"]}">{c["rank"]}</span>
<div class="bpa-kicker">{c["area"]} • ⏱️ {c["time"]} • <span class="bpa-kicker-map-link">{c["transport"]}</span></div>
</div>
<h3 class="bpa-details-title">{c["title"]}</h3>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{"".join(badges)}</div></div>{proof}
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
    if c["book"] == "gyg":
        badge, cta, trustline = "Tickets &amp; Live Availability", "Check Dates &amp; Book Tickets", c["trust"][0].replace("✓ ", "")
        perks = ['Booked via %s' % c["via"], c["trust"][1].replace("✓ ", "")]
    else:
        badge, cta, trustline = "Official Prices &amp; Opening Hours", "See Official Prices", "No online booking: pay at the ticket desk"
        perks = ["Sold only at the bath's ticket desk", "Morning or afternoon session"]
    perks += ['Address: <strong>%s</strong>' % re.sub(r"<[^>]+>", "", c["getthere"][0]).replace("📍 ", ""),
              'Suggested time: <strong>%s</strong>' % c["time"]]
    perk_html = "\n".join('<span class="ltt-buy-perk">%s</span>' % p for p in perks)
    return f'''<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>{badge}</span>
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
<a class="ltt-buy-cta-btn" href="{book_url(c, "review")}" rel="{book_rel(c)}" target="_blank">
<span>{cta}</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{LOCK_SVG}
<span>{trustline}</span>
</div>
</div>
</div>
</div>'''


def qf(c):
    rows = "\n".join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>' % r for r in c["qf"])
    chips = "\n".join('<span class="qf1-chip %s">%s %s</span>' % (k, "✓" if k == "yes" else "✕", t) for k, t in c["amen"])
    return f'''<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">Quick Facts: Verified Field Specs</h4>
<span class="qf1-badge">{c["area"]}</span>
</div>
<div class="qf1-table">
{rows}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
<p class="qf1-note" style="margin:10px 0 0;font-size:12px;color:#64748b">Checked on the official site and the live listings on 14 November 2026. Only what the source confirms is shown.</p>
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
    paras = "".join("<p>%s</p>" % p for p in c["summary"])
    quotes = "<blockquote><strong>What visitors say:</strong><br/>%s</blockquote>" % "<br/>".join(
        "“%s” <em>(%s, %s)</em>" % qq for qq in c["quotes"])
    getthere = '<h3>How to Get There</h3><ul role="list">%s</ul>' % "".join("<li>%s</li>" % x for x in c["getthere"])
    summary = ('<div class="w-richtext"><blockquote>❓ <strong>%s</strong><br/>💡 %s</blockquote>%s%s%s</div>\n%s'
               % (q, a, paras, quotes, getthere, buycard(c)))
    cards = []
    for h, img, txt in c["spcards"]:
        im = '<img alt="%s: %s" loading="lazy" src="%s"/>' % (c["alt"], re.sub(r"&amp;", "and", h), img) if img else ""
        cards.append('<div class="ltt-sp-card"><h4>%s</h4>%s<ul role="list"><li>%s</li></ul></div>' % (h, im, txt))
    inside = '<div class="ltt-sub-points">\n%s\n</div>' % "\n".join(cards)
    label = "From My Visit" if c["tested"] else "From Official Info"
    return (proscons(c) + "\n" + bento("Summary &amp; Review Overview", "Overview", summary) + "\n"
            + bento("Inside the Bath: Pools, Saunas &amp; Changing Rooms", label, inside) + "\n" + qf(c) + "\n")


def details_html(i, c):
    return det_header(i, c) + body_html(c) + "</div>\n</details>"


def no_em_dash(html):
    html = re.sub(r"\s*—\s*", ": ", html)
    return html.replace("&mdash;", ":")


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


# ── page-level prose ─────────────────────────────────────────────────────────────────
KNOW = '''<h2 id="thermal-baths-know-before-you-go">Thermal Baths: Know Before You Go</h2><div class="w-richtext">
<h3>What to Bring and Wear</h3><p>Bring a swimsuit, a towel and flip-flops. Tickets do not include towels: the city-run baths sell a towel for 6,900 HUF and slippers for 4,200 HUF at the desk (2026 price lists). If you plan to swim laps, bring a swim cap.</p>
<h3>When to Visit</h3><p>All six baths in this guide are open all year. Weekday mornings are the quietest; Széchenyi and Rudas get busy from late morning and at weekends. Palatinus is a summer strand: in winter it closes at 16:00.</p>
<h3>Lockers and Cabins</h3><p>A standard ticket includes a locker in a shared changing room. A private cabin costs 1,000 HUF extra at Széchenyi, Rudas, Lukács and Palatinus, and 800 HUF at Dandár.</p>
<h3>Age Limits</h3><p>Rudas, Lukács, Dandár and Veli Bej do not admit children under 14. For a family visit, choose Palatinus.</p>
<h3>Water Temperature</h3><p>Most thermal pools are between 32 and 38 °C. The hottest pools reach 40 to 42 °C, and the cold plunge pools go down to 11 °C at Rudas.</p>
<h3>Closed Baths</h3><p><strong>Gellért</strong> has been closed since 1 October 2025 and is expected to reopen in 2028. <strong>Király</strong> is closed indefinitely. Both were checked on their official sites on 14 November 2026, so they are not in this list.</p>
</div>'''

HISTORY = '''<h2 id="history-thermal-baths">Brief History of Thermal Baths in Budapest</h2><div class="w-richtext">
<p>Budapest sits on a network of thermal springs, and people have bathed here since Roman times. During Ottoman rule, Turkish baths were built in Buda; Rudas and Veli Bej still have their Ottoman pools and domes today.</p>
<p>The grand bathhouses came later: Széchenyi, the neo-baroque palace in City Park, opened in 1913. Today most of the city's baths are run by Budapest Gyógyfürdői és Hévizei Zrt., while Veli Bej is run by the Brothers Hospitallers.</p>
</div>'''

FAQ = [
    ("Which is the best thermal bath in Budapest?",
     "Széchenyi for a first visit, Rudas for a Turkish bath and a rooftop pool, Palatinus for families, and Lukács, Dandár or Veli Bej for a quieter, local bath."),
    ("Are Gellért and Király open?",
     "No. Gellért has been closed since 1 October 2025 and is expected to reopen in 2028, and Király is closed indefinitely (official sites, 14 November 2026)."),
    ("How much does a thermal bath cost in Budapest?",
     "At the desk in 2026: from 3,500 HUF at Dandár to 13,200 HUF at Széchenyi on weekdays. Booking-site tickets start at €22 (Dandár) and €39 (Széchenyi, entry before 9:00)."),
    ("Can children go to the thermal baths?",
     "Only to some. Rudas, Lukács, Dandár and Veli Bej do not admit children under 14. Palatinus has kids' pools and family tickets."),
    ("Do you need flip-flops for Budapest baths?",
     "Yes, bring flip-flops, a towel and a swimsuit. Towels are not included in the ticket; the city-run baths sell towels for 6,900 HUF and slippers for 4,200 HUF."),
    ("Is there night bathing in Budapest?",
     "Yes. Rudas has night bathing on Friday and Saturday from 22:00 to 3:00, Széchenyi is open until 22:00 on Fridays, and the Sparty pool party at Széchenyi runs on Saturday nights."),
]


def faq_html():
    cards = []
    for k, (q, a) in enumerate(FAQ):
        first = " first" if k == 0 else ""
        cards.append('<div class="cf-faq-plus-card"><div class="cf-faq-question-container-3%s"><div class="cf-faq-question-wrap">'
                     '<h3 class="cf-faq-questions-2">%s</h3><div class="cf-faq-icon-contain"><div class="cf-faq-line"></div>'
                     '<div class="cf-faq-line-vertical"></div></div></div></div><div class="cf-faq-answer-wrap-2">'
                     '<div class="cf-faq-content-2 w-richtext"><p>%s</p></div></div><div class="cf-bottom-line-2"></div></div>' % (first, q, a))
    return '<div class="cf-faqs-container">%s</div>' % "".join(cards)


def main():
    page = SRC["page"]
    cards = D.CARDS
    n = len(cards)
    n_tested = sum(c["tested"] for c in cards)
    deck = no_em_dash("\n".join(deck_html(i, c) for i, c in enumerate(cards, 1)))
    dets = no_em_dash("".join(details_html(i, c) for i, c in enumerate(cards, 1)))

    cs = all_spans(page, "card")
    page = page[:cs[0][0]] + deck + page[cs[-1][1]:]
    ds = all_spans(page, "details")
    page = page[:ds[0][0]] + dets + page[ds[-1][1]:]

    untested_reviews = sum(r[2] for c in cards if not c["tested"] for r in c["ratings"])
    m_reviews = "{:,}+".format(untested_reviews // 100 * 100)
    title = "%d Best Thermal Baths in Budapest 2026 (%d Personally Tested)" % (n, n_tested)
    desc = ("The %d best thermal baths in Budapest for 2026: Széchenyi, Rudas, Lukács, Palatinus, Dandár and Veli Bej. "
            "%d personally tested; hours, prices and pool temperatures checked on 14 Nov 2026." % (n, n_tested))

    # head
    page = must_sub(r"<title>.*?</title>", "<title>%s</title>" % title, page, flags=re.S)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (title, prop), page)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        page = re.sub(r'<meta content="[^"]*" %s/>' % prop, '<meta content="%s" %s/>' % (desc, prop), page)
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    # reference CSS + pill JS
    page = page.replace("</head>", "\n".join(REF_CSS) + "\n</head>", 1)
    page = page.replace("</body>", REF_JS + "\n</body>", 1)

    # hero
    page = must_sub(r'<span class="ltt-bc-current">[^<]*</span>', '<span class="ltt-bc-current">%d Best Thermal Baths in Budapest (2026)</span>' % n, page)
    page = page.replace('<span class="ltt-hero-kicker-badge">2026 Field-Tested Comparison</span>',
                        '<span class="ltt-hero-kicker-badge">2026 Thermal Bath Comparison</span>')
    page = must_sub(r'(<h1 class="ltt-editorial-h1">).*?(</h1>)',
                    r'\1\n      %d Best Thermal Baths in Budapest in 2026 <span class="ltt-h1-muted">(%d Personally Tested)</span>\n\2' % (n, n_tested),
                    page, flags=re.S)
    page = re.sub(r'(<div class="ltt-author-line">\s*By <a href="/about" target="_blank">Adam Dimitrov</a>)\s*—\s*', r"\1, ", page, count=1)
    page = must_sub(r'<div class="ltt-author-role">[^<]*</div>',
                    '<div class="ltt-author-role">%d of %d Baths Visited in Person • Hours &amp; Prices Checked 14 Nov 2026</div>' % (n_tested, n), page)
    page = must_sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 14, 2026<", page)
    lead = f'''<div class="ltt-lead-copy">
<p>Budapest is famous for its thermal baths, from neo-baroque palaces with steaming outdoor pools to <strong>Ottoman Turkish baths</strong> under stone domes. This guide compares the <strong>{n} best thermal baths</strong> that are open in 2026.</p>
<p>I <strong>personally visited {n_tested} of these {n} baths</strong>. I compared the other {n - n_tested} using their official sites and <strong>{m_reviews} reviews</strong>. Every opening hour, desk price and pool temperature was checked on the official sites on 14 November 2026.</p>
<p>Gellért (closed until 2028) and Király (closed indefinitely) are not in this list. Planning a full day? See the <a href="/best-things-to-do-budapest">best things to do in Budapest</a> and the <a href="/best-budapest-river-cruises">best Budapest river cruises</a>.</p>
</div>'''
    page = swap_block(page, r'<div class="ltt-lead-copy">', lead)
    pills = f'''<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems('all', this)" type="button">All ({n})</button>
<button class="ltt-tab-btn" data-cat="tested" onclick="lttFilterItems('tested', this)" type="button">Personally Tested ({n_tested})</button>
</div>'''
    while '<div class="ltt-integrated-pills">\n<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems(\'all\', this)" type="button">All (8)' in page:
        page = swap_block(page, r'<div class="ltt-integrated-pills">\n<button class="ltt-tab-btn active" data-cat="all" onclick="lttFilterItems\(\'all\', this\)" type="button">All \(8\)', pills)
    page = page.replace("Personally field-tested • All reviews open by default",
                        "%d of %d personally tested • All reviews open by default" % (n_tested, n))
    page = must_sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">)[^<]*(</h2>)',
                    r"\1Detailed Breakdown: %d Best Thermal Baths in Budapest\2" % n, page)

    # old Webflow intro under the deck
    page = must_sub(r"<p><strong>If you're <a href=\"/budapest-travel-guide\">planning a trip to Budapest</a>.*?(<h2 id=\"thermal-baths-map\">)",
                    "<p>Every bath below was checked on its official site on 14 November 2026. Each one suits a different kind of visit, "
                    "so the cards above show who should pick it and who should skip it.</p></div>\\1", page, flags=re.S)
    page = must_sub(r"<p>Indeed, <strong>Hungarians generally don't visit.*?</p>",
                    "<p>The famous baths are busier and pricier than the local ones: a weekday desk ticket is 13,200 HUF at Széchenyi "
                    "against 3,500 HUF at Dandár. Both are worth a visit; they are simply different experiences.</p>", page, flags=re.S)

    # Know before you go, history, FAQ
    a = page.find('<h2 id="thermal-baths-know-before-you-go">')
    b = page.find('<div class="cf-faq-container" id="faq">')
    assert 0 < a < b
    page = page[:a] + KNOW + HISTORY + page[b:]
    page = swap_block(page, r'<div class="cf-faqs-container">', faq_html())

    # runtime config
    cfg = {"deckId": "budapest-thermal-baths-deck", "tocDeckLabel": "Top %d Thermal Baths" % n,
           "tocBreakdownLabel": "Detailed Breakdown (%d Thermal Baths)" % n,
           "shortTitles": [c["short"] for c in cards]}
    page = must_sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", "window.LTT_PAGE_CONFIG = %s;" % json.dumps(cfg, ensure_ascii=False), page, flags=re.S)
    # legacy Webflow script that stamped "Personally Tested" on every row
    page = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const cruiseCards = .*?</script>', "", page, count=1, flags=re.S)
    # sticky bar starts on card 1
    c1 = cards[0]
    for tid, pid, bid in (("sticky-name", "sticky-price", "sticky-cta-btn"), ("hybridActiveTitle", "hybridActivePrice", "hybridActiveCta")):
        page = re.sub(r'(<span class="hybrid-active-title" id="%s">)[^<]*(</span>)' % tid, r"\g<1>%s\2" % c1["short"], page, count=1)
        page = re.sub(r'(<span class="hybrid-active-price" id="%s">)[^<]*(</span>)' % pid, r"\g<1>From €%s\2" % c1["price"], page, count=1)
        page = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="%s")' % bid, r"\g<1>%s\2" % book_url(c1, "sticky"), page, count=1)

    page = must_sub(r"<span>All 8 Thermal Baths</span>", "<span>All %d Thermal Baths</span>" % n, page)
    page = must_sub(r'<span class="hybrid-active-trust">Free 24h Cancellation</span>',
                    '<span class="hybrid-active-trust">Prices checked 14 Nov 2026</span>', page)
    page = page.replace('aria-label="Jump to Cruise Review"', 'aria-label="Jump to Bath Review"')
    page = page.replace('aria-label="Quick Cruise Navigation &amp; Booking"', 'aria-label="Quick Bath Navigation &amp; Booking"')
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
    url = SITE + "/thermal-baths-budapest"
    items = []
    for pos, c in enumerate(cards, 1):
        avg, tot = wavg(c["ratings"])
        addr = strip_tags(c["getthere"][0]).replace("📍 ", "")
        offer = {"@type": "Offer", "availability": "https://schema.org/InStock",
                 "url": book_url(c, "schema").replace("&amp;", "&")}
        if c.get("price"):
            offer.update(price=c["price"], priceCurrency="EUR")
        else:
            offer.update(price=c["price_huf"], priceCurrency="HUF")
        prod = {
            "@type": "Product",
            "name": c["title"],
            "description": "%s: %s" % (strip_tags(c["rank"]).split(" ", 2)[-1], strip_tags(c["pick"])),
            "brand": {"@type": "Organization", "name": c["title"]},
            "isRelatedTo": {"@type": "TouristAttraction", "name": c["title"], "address": addr},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "%.2f" % avg, "bestRating": "5",
                                "worstRating": "1", "reviewCount": str(tot)},
            "offers": offer,
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
            me = node.setdefault("mainEntity", {"@type": "ItemList"})
            me["name"] = title
            me["description"] = strip_tags(desc)
            me["numberOfItems"] = len(cards)
            me["itemListElement"] = items
        if node.get("@type") == "BreadcrumbList":
            for it in node.get("itemListElement", []):
                if "Thermal" in it.get("name", ""):
                    it["name"] = "%d Best Thermal Baths in Budapest (2026)" % len(cards)
    data["@graph"] = [n for n in data["@graph"] if n.get("@type") != "FAQPage"]
    data["@graph"].append({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    out = json.dumps(data, ensure_ascii=False, indent=1).replace("—", ":")
    return page[:a] + out + page[b:]


if __name__ == "__main__":
    main()
