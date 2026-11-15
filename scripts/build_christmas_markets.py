#!/usr/bin/env python3
"""Build the Budapest Christmas Markets 2026 page (EN, DE, FR, IT, ES, HU).

Facts: scripts/christmas_markets_data.py      Copy: scripts/christmas_markets_copy_<lang>.py
Cards, pills, star summary and breakdowns reuse the components of the private boats builder
(which copies them from best-budapest-river-cruises.html), so the page looks like the guides.
A missing target page is created from that language's private boats page as a skeleton.

    python3 scripts/build_christmas_markets.py            # all languages
    python3 scripts/build_christmas_markets.py en hu      # only these
"""
import html
import importlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_private_boats as bp  # noqa: E402
from christmas_markets_data import (  # noqa: E402
    BUDGETS, CHECKED, MARKETS, PRICES, PRICE_SOURCES, PRODUCTS, SISTER, TRANSIT, budget_total, walk_minutes, weighted)

SITE = bp.SITE
esc, fmt1, pill, balanced_end, sub_once = bp.esc, bp.fmt1, bp.pill, bp.balanced_end, bp.sub_once
PAGES = {
    "en": ("budapest-christmas-markets.html", "/budapest-christmas-markets", "best-private-boat-tours-budapest.html"),
    "de": ("de/weihnachtsmarkt-budapest/index.html", "/de/weihnachtsmarkt-budapest", "de/private-bootsfahrten-budapest/index.html"),
    "fr": ("fr/marche-de-noel-budapest/index.html", "/fr/marche-de-noel-budapest", "fr/balades-bateau-prive-budapest/index.html"),
    "it": ("it/mercatini-di-natale-budapest/index.html", "/it/mercatini-di-natale-budapest", "it/tour-barca-privata-budapest/index.html"),
    "es": ("es/mercadillo-navideno-budapest/index.html", "/es/mercadillo-navideno-budapest", "es/paseos-barco-privado-budapest/index.html"),
    "hu": ("hu/karacsonyi-vasar-budapest/index.html", "/hu/karacsonyi-vasar-budapest", "hu/legjobb-privát-hajókirándulások-budapest/index.html"),
}
IMG = "/assets/xmas-markets-2026/"
SIZES = bp.SIZES
SITE_NAME = {"gyg": "GetYourGuide", "viator": "Viator"}
MK = {m["key"]: m for m in MARKETS}
DECK_ID = "budapest-christmas-markets-deck"

PAGE_CSS = """<style id="xm-page-css">
.bpa-mkt .bpa-poster{position:relative;border-radius:12px;aspect-ratio:3/2;display:flex;flex-direction:column;justify-content:flex-end;gap:6px;padding:18px 18px 16px;color:#fff;overflow:hidden;box-sizing:border-box}
.bpa-mkt .bpa-media{background:none !important;aspect-ratio:auto !important;height:auto !important;min-height:0 !important}
.bpa-mkt .bpa-poster .bpa-rank-tag{position:absolute;top:12px;left:12px}
.bpa-mkt .xm-p1{background:linear-gradient(135deg,#7f1d1d,#b91c1c 55%,#f59e0b)}
.bpa-mkt .xm-p2{background:linear-gradient(135deg,#064e3b,#047857 55%,#a3e635)}
.bpa-mkt .xm-p3{background:linear-gradient(135deg,#1e3a8a,#1d4ed8 55%,#93c5fd)}
.bpa-mkt .xm-p4{background:linear-gradient(135deg,#4c1d95,#7c3aed 55%,#f0abfc)}
.xm-poster-place{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;opacity:.9}
.xm-poster-dates{font-size:26px;font-weight:800;line-height:1.15}
.xm-poster-sub{font-size:14px;opacity:.95}
.bpa-mkt .bpa-price{font-size:20px}
.xm-wrap{max-width:1240px;margin:0 auto 40px;padding:0 16px;box-sizing:border-box;color:#1e293b;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.xm-wrap h2{font-size:28px;line-height:1.25;font-weight:800;color:#0f172a;margin:44px 0 10px}
.xm-wrap h3{font-size:20px;font-weight:700;color:#0f172a;margin:26px 0 10px}
.xm-wrap p,.xm-wrap li{font-size:17px;line-height:1.65;color:#334155}
.xm-sub{color:#64748b !important;font-size:15px !important;margin:0 0 16px}
.xm-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e2e8f0;border-radius:12px;background:#fff;margin:16px 0 8px;max-width:100%}
.xm-table{width:100%;border-collapse:collapse;font-size:14.5px;min-width:640px}
.xm-table th,.xm-table td{padding:11px 13px;border-bottom:1px solid #f1f5f9;text-align:left;vertical-align:top;color:#334155}
.xm-table thead th{background:#f8fafc;color:#0f172a;font-weight:700;position:sticky;top:0}
.xm-table tbody th{font-weight:700;color:#0f172a;background:#fcfcfd;white-space:nowrap}
.xm-table td.xm-no{color:#94a3b8}
.xm-note{font-size:13.5px !important;color:#64748b !important;margin:6px 0 0}
.xm-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:14px 0}
.xm-box{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:18px 18px 14px;box-shadow:0 2px 8px rgba(15,23,42,.04)}
.xm-box h3{margin:0 0 8px;font-size:18px}
.xm-box p{font-size:15.5px;margin:0 0 8px}
.xm-big{font-size:28px;font-weight:800;color:#0f172a;line-height:1.1;margin:2px 0 6px}
.xm-route{list-style:none;padding:0;margin:14px 0;border-left:3px solid #e2e8f0}
.xm-route li{position:relative;padding:0 0 14px 22px;margin:0}
.xm-route li:before{content:"";position:absolute;left:-8px;top:6px;width:13px;height:13px;border-radius:50%;background:#b91c1c;box-shadow:0 0 0 3px #fff}
.xm-route b{color:#0f172a}
.xm-sec{scroll-margin-top:90px}
.xm-sec-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 14px}
.xm-chip{display:inline-block;background:#f1f5f9;border-radius:999px;padding:3px 10px;font-size:13px;color:#334155;font-weight:600}
.xm-sec .bpa-deck-wrap{margin:18px auto 10px !important}
.xm-cruise{display:flex;gap:18px;align-items:center;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fff;border-radius:16px;padding:22px;margin:30px 0;text-decoration:none}
.xm-cruise img{width:120px;height:90px;object-fit:cover;border-radius:10px;flex-shrink:0}
.xm-cruise b{display:block;font-size:19px;color:#fff;margin-bottom:4px}
.xm-cruise span{font-size:15px;color:#cbd5e1}
.xm-cruise em{display:inline-block;margin-top:8px;font-style:normal;font-weight:700;color:#fde68a}
.xm-faq details{border:1px solid #e2e8f0;border-radius:12px;padding:12px 16px;margin:10px 0;background:#fff}
.xm-faq summary{font-weight:700;color:#0f172a;cursor:pointer;font-size:16.5px}
.xm-faq p{margin:10px 0 2px;font-size:16px}
.xm-sources li{font-size:14px;word-break:break-word}
@media (max-width:640px){.xm-wrap h2{font-size:23px}.xm-poster-dates{font-size:22px}.xm-cruise{flex-direction:column;align-items:flex-start}.xm-cruise img{width:100%;height:150px}}
</style>"""


# ---------------------------------------------------------------- helpers
def dmy(iso, ui, year=False):
    y, m, d = (int(x) for x in iso.split("-"))
    return ui["date_fmt"].format(d=d, m=ui["months"][m - 1], y=y) if year else ui["date_fmt_short"].format(d=d, m=ui["months"][m - 1])


def span(m, ui):
    return ui["date_span"].format(a=dmy(m["start"], ui), b=dmy(m["end"], ui, year=m["end"][:4] != "2026"))


def hrs(v, ui):
    if not v:
        return ui["closed"]
    t = ui.get("tfmt")
    return "–".join(t(x) for x in v.split("-")) if t else v.replace("-", "–")


def maps(q):
    return "https://www.google.com/maps/search/?api=1&amp;query=" + q.replace(" ", "+")


def img_src(f):
    return f.replace("../xmas-2026/", "/assets/xmas-2026/") if f.startswith("../") else IMG + f


# ---------------------------------------------------------------- star summary
def rate_block(p, ui):
    r, n = weighted(p["ratings"])
    if not n:
        return '<div class="bpa-summary-reviews bpa-rate"><span class="bpa-rate-meta" style="font-size:13px;color:#64748b">✨ %s</span></div>' % ui["new_listing"]
    badges = ""
    for site, score, cnt in p["ratings"]:
        inner = ('<img alt="%s" class="bpa-rev-icon" loading="lazy" src="%s"/><span class="bpa-rev-site">%s</span>'
                 '<span class="bpa-rev-score">%s</span><span class="bpa-rev-count">(%s)</span>') % (
            SITE_NAME[site], bp.ICON[site], SITE_NAME[site], fmt1(score), ui["num"](cnt))
        link = p["links"].get(site)
        if link:
            badges += ('<a class="bpa-rev-badge is-link" href="%s" rel="noopener nofollow sponsored" target="_blank">%s'
                       '<span class="bpa-rev-go" aria-hidden="true">→</span></a>') % (esc(link), inner)
        else:
            badges += '<span class="bpa-rev-badge">%s</span>' % inner
    nsites = len(p["ratings"])
    meta = (ui["reviews_sites"] if nsites > 1 else ui["reviews_site"]).format(count=ui["num"](n), n=nsites)
    return ('<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            '<span class="bpa-stars" style="--r:%.2f" aria-hidden="true"></span><b class="bpa-rate-score">%s</b>'
            '<span class="bpa-rate-meta">%s</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong><span class="bpa-rate-list">%s</span></div></details></div>') % (
        r, fmt1(r), meta, ui["avg_note"].format(n=nsites) if nsites > 1 else ui["rating_on"].format(site=SITE_NAME[p["ratings"][0][0]]), badges)


def kicker(p, c, link=True):
    if link:
        pier_html = ('<a class="bpa-kicker-map-link" href="%s" onclick="event.stopPropagation()" rel="noopener noreferrer" '
                     'target="_blank">%s</a>') % (maps(p["pier_map"]), esc(c.get("pier", p["pier"])))
    else:
        pier_html = '<span class="bpa-kicker-map-link">%s</span>' % esc(c.get("pier", p["pier"]))
    return '<div class="bpa-kicker">%s • ⏱️ %s • %s</div>' % (esc(p["operator"]), c["duration"], pier_html)


def via(p, ui):
    return ui["via_direct"].format(op=p["operator"]) if p["book_via"] == "direct" else ui["via_gyg"]


# ---------------------------------------------------------------- market card
def market_card(i, m, c, ui):
    pills = "\n".join(pill(pl) for pl in c["pills"])
    return f'''<!-- market {i}: {m["name"]} -->
<div class="bpa-card bpa-mkt" id="mcard-{i}">
<div class="bpa-main">
<div class="bpa-media">
<div class="bpa-poster xm-p{i}">
<span class="bpa-rank-tag bpa-gold">{c["rank_tag"]}</span>
<span class="xm-poster-place">{esc(m["place"])} · {m["district"]} {ui["district"]}</span>
<span class="xm-poster-dates">{span(m, ui)}</span>
<span class="xm-poster-sub">{c["poster_sub"]}</span>
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{esc(m["place"])} • {m["district"]} {ui["district"]} • <a class="bpa-kicker-map-link" href="{maps(m["map_q"])}" rel="noopener noreferrer" target="_blank">{ui["map"]}</a></div>
<a class="bpa-title" href="#{m["anchor"]}">{esc(m["name"])}: {c["title"]}</a>
<div class="bpa-reviews-line"><div class="bpa-summary-reviews bpa-rate"><span class="bpa-rate-meta" style="font-size:13.5px;color:#475569">{c["meta"]}</span></div></div>
<div class="bpa-specs-row">
{pills}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">{ui["pick"]}</span> {c["pick"]} <span class="bpa-skip">{ui["skip"]}</span> {c["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{ui["free_entry"]}</div>
<div class="bpa-psub">{c["cta_sub"]}</div>
</div>
<a class="bpa-btn" href="#{m["anchor"]}">{ui["see_programs"]}</a>
<div class="bpa-via"><a href="{m["official"]}" rel="noopener" target="_blank">{ui["official_site"]}</a></div>
</div>
</div>
</div>'''


# ---------------------------------------------------------------- program card
def program_card(i, p, c, ui):
    imgs = ""
    for k, f in enumerate(p["images"]):
        if k == 0:
            imgs += '<img alt="%s" height="534" loading="lazy" sizes="%s" src="%s" width="800"/>' % (esc(c["alt"]), SIZES, img_src(f))
        else:
            imgs += '<img alt="%s" data-src="%s" decoding="async" loading="lazy" sizes="%s" src="%s"/>' % (esc(c["alt"]), img_src(f), SIZES, bp.PLACEHOLDER)
    pills = "\n".join(pill(pl) for pl in c["pills"])
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    rel = "noopener nofollow sponsored"
    return f'''<!-- #{i}: {c["short"]} -->
<div class="bpa-card" data-cat="{p["market"]}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {p["rank_class"]}">{c["rank_tag"]}</span>
<button aria-label="{ui["prev"]}" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button><button aria-label="{ui["next"]}" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button><span class="bpa-pill">1 / {len(p["images"])}</span><div aria-label="{ui["photo_gallery"].format(n=i)}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">{imgs}</div>
</div>
<div class="bpa-info">
{kicker(p, c)}
<a class="bpa-title" href="{esc(p["book"])}" rel="{rel}" target="_blank">{c["title"]}</a>
<div class="bpa-reviews-line">
{rate_block(p, ui)}
</div>
<div class="bpa-specs-row">
{pills}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">{ui["pick"]}</span> {c["pick"]} <span class="bpa-skip">{ui["skip"]}</span> {c["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{ui["from"].format(p=p["price_from"])}</div>
<div class="bpa-psub">{ui["per_person"]}</div>
</div>
<a class="bpa-btn" href="{esc(p["book"])}" rel="{rel}" target="_blank">{ui["check"]}</a>
<div class="bpa-via">{via(p, ui)}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{p["anchor"]}">{ui["read"]}</a>
</div>
</div>
</div>'''


# ---------------------------------------------------------------- breakdown
def summary_badges(p, ui):
    out = ""
    for site, score, cnt in p["ratings"]:
        out += ('<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="%s"/>'
                '<span class="bpa-rev-score">%s</span><span class="bpa-rev-stars">%s</span>'
                '<span class="bpa-rev-count">(%s)</span></span>') % (bp.ICON[site], fmt1(score), bp.stars(score), ui["num"](cnt))
    return out


def breakdown(i, p, c, ui):
    pros = "".join("<li><strong>%s</strong>: %s</li>" % x for x in c["pros"])
    cons = "".join("<li><strong>%s</strong>: %s</li>" % x for x in c["cons"])
    q, a = c["faq"]
    body = '<blockquote><strong>❓ %s</strong><br/>💡 %s</blockquote>' % (q, a)
    body += "".join("<p>%s</p>" % para for para in c["summary"])
    if c["reviews"]:
        body += "<h3>%s</h3>" % ui["what_say"]
        for name, when, site, text in c["reviews"]:
            body += '<blockquote>“%s”<br/><strong>%s</strong> · %s · %s</blockquote>' % (text, name, site, when)
    body += "<h3>%s</h3><ul role=\"list\">%s</ul>" % (ui["how"], "".join("<li>%s</li>" % h for h in c["how"]))
    perks = [ui["perk_cancel"], ui["perk_from"].format(v=esc(c.get("pier", p["pier"]))), ui["perk_dur"].format(v=c["duration"])]
    perks_html = "".join('<span class="ltt-buy-perk">%s</span>' % x for x in perks)
    walk = ""
    for h4, idx, text in c["walk"]:
        walk += ('<div class="ltt-sp-card"><h4>%s</h4><img alt="%s" loading="lazy" sizes="(max-width: 640px) 100vw, 420px" src="%s"/>'
                 '<ul role="list"><li>%s</li></ul></div>\n') % (h4, esc(c["alt"]), img_src(p["images"][idx]), text)
    qf = "".join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>\n' % x for x in c["qf"])
    chips = "".join('<span class="qf1-chip %s">%s</span>\n' % x for x in c["chips"])
    price = ui["from"].format(p=p["price_from"])
    badges = summary_badges(p, ui) or '<span class="bpa-rev-count" style="font-size:13px;color:#64748b">✨ ' + ui["new_listing"] + '</span>'
    return f'''<details class="bpa-details-card" data-cat="{p["market"]}" id="{p["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {p["rank_class"]}">{c["rank_tag"]}</span>
{kicker(p, c, link=False)}
</div>
<h3 class="bpa-details-title">{c["title"]}</h3>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{badges}</div></div>
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">{price}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>{ui["pros"]}</strong></h3><ul role="list">{pros}</ul></div></div><div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext"><h3><strong>{ui["cons"]}</strong></h3><ul role="list">{cons}</ul></div></div></div></div>
<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">{ui["summary"]}</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">{ui["overview"]}</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
<div class="w-richtext">{body}</div>
<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>{ui["buy_badge"]}</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{price}</span>
<span class="ltt-buy-price-sub">{ui["per_person"]}</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{c["short"]}</h4>
<div class="ltt-buy-card-perks">
{perks_html}
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{esc(p["book"])}" rel="noopener nofollow sponsored" target="_blank">
<span>{ui["buy_cta"]}</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
<span>{via(p, ui)}</span>
</div>
</div>
</div>
</div>
</div>
</details>
<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">{ui["walk"]}</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">{ui["walk_pill"]}</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
<div class="ltt-sub-points">
{walk}</div>
</div>
</details>
<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">{ui["qf_title"]}</h4>
<span class="qf1-badge">{esc(c["qf_badge"])}</span>
</div>
<div class="qf1-table">
{qf}</div>
<div class="qf1-Validation-pills">
{chips}</div>
</div>
</div>
</details>'''


# ---------------------------------------------------------------- analysis blocks
def compare_table(copy):
    ui, an = copy["ui"], copy["analysis"]
    head = "".join("<th>%s</th>" % esc(m["name"]) for m in MARKETS)

    def row(label, vals):
        cells = "".join('<td%s>%s</td>' % (' class="xm-no"' if v in (ui["closed"], ui["none"]) else "", v) for v in vals)
        return "<tr><th>%s</th>%s</tr>" % (label, cells)

    rows = [row(an["r_place"], ["%s (%s %s)" % (esc(m["place"]), m["district"], ui["district"]) for m in MARKETS]),
            row(an["r_dates"], [span(m, ui) for m in MARKETS])]
    wk = []
    for m in MARKETS:
        h = m["hours"]
        if "fri" in h:
            wk.append("%s %s · %s %s · %s %s · %s %s" % (ui["d_mon_thu"], hrs(h["mon_thu"], ui), ui["d_fri"], hrs(h["fri"], ui),
                                                        ui["d_sat"], hrs(h["sat"], ui), ui["d_sun"], hrs(h["sun"], ui)))
        elif h["mon_thu"] == h["fri_sat"] == h["sun"]:
            wk.append("%s %s" % (ui["d_daily"], hrs(h["mon_thu"], ui)))
        else:
            wk.append("%s %s · %s %s · %s %s" % (ui["d_mon_thu"], hrs(h["mon_thu"], ui), ui["d_fri_sat"], hrs(h["fri_sat"], ui),
                                               ui["d_sun"], hrs(h["sun"], ui)))
    rows.append(row(an["r_hours"], wk))
    for k, lab in (("dec24", an["r_24"]), ("dec25", an["r_25"]), ("dec26", an["r_26"]), ("dec31", an["r_31"]), ("jan1", an["r_jan1"])):
        vals = []
        for m in MARKETS:
            v = m["hours"].get(k)
            end_iso = m["end"]
            day = {"dec24": "2026-12-24", "dec25": "2026-12-25", "dec26": "2026-12-26", "dec31": "2026-12-31", "jan1": "2027-01-01"}[k]
            if v:
                vals.append(hrs(v, ui))
            elif day > end_iso:
                vals.append(ui["closed"])
            else:
                vals.append(ui["not_listed"])
        rows.append(row(lab, vals))
    rows.append(row(an["r_show"], [an["show"][m["key"]] for m in MARKETS]))
    rows.append(row(an["r_rink"], [an["rink"][m["key"]] for m in MARKETS]))
    rows.append(row(an["r_food"], [an["food"][m["key"]] for m in MARKETS]))
    rows.append(row(an["r_crowd"], [an["crowd"][m["key"]] for m in MARKETS]))
    rows.append(row(an["r_transport"], [an["transport"][m["key"]] for m in MARKETS]))
    rows.append(row(an["r_access"], [an["access"][m["key"]] for m in MARKETS]))
    return ('<div class="xm-table-wrap"><table class="xm-table"><thead><tr><th>%s</th>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="xm-note">%s</p>') % (an["t_corner"], head, "".join(rows), an["table_note"])


def walk_table(copy):
    ui, an = copy["ui"], copy["analysis"]
    head = "".join("<th>%s</th>" % esc(m["place"]) for m in MARKETS)
    rows = ""
    for a in MARKETS:
        cells = ""
        for b in MARKETS:
            if a is b:
                cells += '<td class="xm-no">–</td>'
                continue
            mins, meters = walk_minutes(a, b)
            t = TRANSIT.get((a["key"], b["key"])) or TRANSIT.get((b["key"], a["key"]))
            if mins > 40:
                cells += "<td>🚇 %s</td>" % an["transit"]["-".join(sorted((a["key"], b["key"])))]
            elif t:
                cells += "<td>🚶 %s<br/><small>%s</small></td>" % (an["walk_fmt"].format(m=mins, km=ui["km"](meters)), an["or_bus"])
            else:
                cells += "<td>🚶 %s</td>" % an["walk_fmt"].format(m=mins, km=ui["km"](meters))
        rows += "<tr><th>%s</th>%s</tr>" % (esc(a["place"]), cells)
    return ('<div class="xm-table-wrap"><table class="xm-table"><thead><tr><th>%s</th>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="xm-note">%s</p>') % (an["w_corner"], head, rows, an["walk_note"])


def budget_boxes(copy):
    ui, an = copy["ui"], copy["analysis"]
    out = ""
    for key, items in BUDGETS:
        total = budget_total(items)
        parts = " + ".join("%s%s" % ("%d× " % n if n > 1 else "", an["item"][k]) for k, n in items)
        out += ('<div class="xm-box"><h3>%s</h3><div class="xm-big">%s</div><p>%s</p><p class="xm-note">%s</p></div>') % (
            an["budget_name"][key], ui["huf"](total), parts, an["budget_two"].format(v=ui["huf"](total * 2)))
    return '<div class="xm-grid">%s</div><p class="xm-note">%s</p>' % (out, an["budget_note"])


def analysis_html(copy):
    an = copy["analysis"]
    picks = "".join('<div class="xm-box"><h3>%s</h3><p>%s</p></div>' % x for x in an["choose"])
    route = "".join("<li>%s</li>" % x for x in an["route"])
    return f'''<div class="xm-wrap">
<section class="xm-sec" id="compare-markets">
<h2>{an["table_h2"]}</h2>
<p class="xm-sub">{an["table_sub"]}</p>
{compare_table(copy)}
</section>
<section class="xm-sec" id="which-market">
<h2>{an["choose_h2"]}</h2>
<div class="xm-grid">{picks}</div>
</section>
<section class="xm-sec" id="market-costs">
<h2>{an["budget_h2"]}</h2>
<p class="xm-sub">{an["budget_sub"]}</p>
{budget_boxes(copy)}
</section>
<section class="xm-sec" id="walking-times">
<h2>{an["walk_h2"]}</h2>
<p class="xm-sub">{an["walk_sub"]}</p>
{walk_table(copy)}
</section>
<section class="xm-sec" id="market-route">
<h2>{an["route_h2"]}</h2>
<p class="xm-sub">{an["route_sub"]}</p>
<ol class="xm-route">{route}</ol>
<p class="xm-note">{an["route_note"]}</p>
</section>
</div>'''


def section_html(key, copy, cards):
    sec = copy["sections"][key]
    m = MK.get(key)
    chips = ""
    if m:
        chips = '<span class="xm-chip">📅 %s</span><span class="xm-chip">📍 <a href="%s" rel="noopener noreferrer" target="_blank">%s</a></span>' % (
            span(m, copy["ui"]), maps(m["map_q"]), esc(m["place"]))
    anchor = m["anchor"] if m else "kurtoskalacs-workshop"
    paras = "".join("<p>%s</p>" % x for x in sec["body"])
    return f'''<section class="xm-sec" id="{anchor}">
<div class="xm-sec-head"><h2>{sec["h2"]}</h2>{chips}</div>
{paras}
<div class="bpa-deck-wrap">
{cards}
</div>
</section>'''


def cruise_block(copy, lang):
    cb = copy["cruise_block"]
    return f'''<a class="xm-cruise" href="{SISTER[lang]}">
<img alt="{esc(cb["alt"])}" height="90" loading="lazy" src="/assets/xmas-2026/budapest-christmas-cruise-christmas-market-01.avif" width="120"/>
<div><b>{cb["title"]}</b><span>{cb["desc"]}</span><br/><em>{cb["cta"]}</em></div>
</a>'''


# ---------------------------------------------------------------- hero
def hero(page, ui, home, lang):
    lead = "".join("<p>%s</p>" % x for x in page["lead"])
    bm = page["cruise_bookmark"]
    lead += f'''
<figure class="cd-bookmark-wrapper">
<a href="{SISTER[lang]}" class="cd-editorial-bookmark">
<div class="cd-editorial-body">
<div>
<div class="cd-editorial-title">{esc(bm["title"])}</div>
<div class="cd-editorial-desc">{esc(bm["desc"])}</div>
</div>
</div>
<div class="cd-editorial-thumb">
<img src="/assets/xmas-2026/budapest-christmas-cruise-mulled-wine-01.avif" alt="{esc(bm["title"])}" loading="lazy" width="64" height="64"/>
</div>
</a>
</figure>'''
    jumps = "".join('<a class="ltt-tab-btn" href="#%s">%s</a>' % (a, l) for a, l in page["jumps"])
    return f'''<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
<a href="{home}">{ui["breadcrumb_home"]}</a>
<span class="ltt-bc-sep">›</span>
<span class="ltt-bc-current">{page["breadcrumb"]}</span>
</nav>
<span class="ltt-hero-kicker-badge">{page["kicker_badge"]}</span>
</div>
<h1 class="ltt-editorial-h1">
      {page["h1"]} <span class="ltt-h1-muted">{page["h1_muted"]}</span>
</h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap">
<img alt="Adam Dimitrov" class="ltt-author-avatar" height="42" loading="eager" src="/assets/adam-dimitrov.webp" width="42"/>
</div>
<div class="ltt-author-meta">
<div class="ltt-author-line">
            {page["author_line"]}
          </div>
<div class="ltt-author-role">{page["author_role"]}</div>
</div>
</div>
<div class="ltt-trust-pills">
<span class="ltt-trust-pill paragraph-26"><strong>{ui["last_updated"]}</strong>: {ui["updated_date"]}</span>
</div>
</div>
<div class="ltt-lead-copy">
{lead}
</div>
<div class="ltt-integrated-filter-bar">
<span class="ltt-filter-label">{ui["jump_to"]}</span>
<div class="ltt-integrated-pills">
{jumps}
</div>
</div>
</div>
</div>'''


# ---------------------------------------------------------------- JSON-LD
def jsonld(lang, path, copy):
    ui, page = copy["ui"], copy["page"]
    url = SITE + path
    home = SITE + ("/" if lang == "en" else "/" + lang)
    progs = []
    for i, p in enumerate(PRODUCTS, 1):
        c = copy["products"][p["key"]]
        prod = {"@type": "Product", "name": html.unescape(c["title"]),
                "description": html.unescape(re.sub("<[^>]+>", "", c["summary"][0])),
                "image": SITE + img_src(p["images"][0]),
                "brand": {"@type": "Organization", "name": p["brand"]},
                "offers": {"@type": "AggregateOffer", "lowPrice": str(p["price_from"]), "highPrice": str(p["price_high"]),
                           "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": html.unescape(p["book"])}}
        r, n = weighted(p["ratings"])
        if n:
            prod["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": fmt1(r), "bestRating": "5", "worstRating": "1", "reviewCount": str(n)}
        progs.append({"@type": "ListItem", "position": i, "url": url + "#" + p["anchor"], "item": prod})
    events = []
    for i, m in enumerate(MARKETS, 1):
        c = copy["markets"][m["key"]]
        ev = {"@type": "Event", "@id": url + "#" + m["anchor"] + "-event", "name": "%s %s" % (m["name"], m["start"][:4]),
              "description": html.unescape(re.sub("<[^>]+>", "", c["pick"])),
              "startDate": m["start"], "endDate": m["end"], "eventStatus": "https://schema.org/EventScheduled",
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "isAccessibleForFree": True,
              "location": {"@type": "Place", "name": m["place"], "address": {"@type": "PostalAddress", "streetAddress": m["place"],
                           "addressLocality": "Budapest", "addressCountry": "HU"},
                           "geo": {"@type": "GeoCoordinates", "latitude": m["lat"], "longitude": m["lng"]}},
              "url": m["official"], "image": SITE + "/assets/xmas-markets-2026/" + PRODUCTS[0]["images"][0]}
        events.append(ev)
    graph = [
        {"@type": "Article", "@id": url + "#article", "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "headline": html.unescape(page["title"]), "description": html.unescape(page["meta"]), "url": url, "inLanguage": lang,
         "datePublished": CHECKED, "dateModified": CHECKED,
         "author": {"@type": "Person", "name": "Adam Dimitrov", "jobTitle": "Founder of Budapest Adventures",
                    "url": SITE + "/about", "image": "/assets/adam-dimitrov.webp"},
         "publisher": {"@type": "Organization", "name": "BUDAPEST ADVENTURES", "url": SITE,
                       "logo": {"@type": "ImageObject", "url": "/assets/budapest-adventures-logo.png"}},
         "image": [SITE + img_src(p["images"][0]) for p in PRODUCTS],
         "about": [{"@id": e["@id"]} for e in events],
         "mainEntity": {"@type": "ItemList", "name": html.unescape(page["programs_list"]), "itemListOrder": "https://schema.org/ItemListOrderAscending",
                        "numberOfItems": len(progs), "itemListElement": progs}},
        {"@type": "ItemList", "@id": url + "#markets", "name": html.unescape(page["markets_list"]),
         "numberOfItems": len(events), "itemListElement": [{"@type": "ListItem", "position": i, "url": url + "#" + m["anchor"], "item": {"@id": e["@id"]}}
                                                           for i, (m, e) in enumerate(zip(MARKETS, events), 1)]},
    ] + events + [
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": html.unescape(re.sub("<[^>]+>", "", q)),
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<[^>]+>", "", a))}} for q, a in copy["faq"]]},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": html.unescape(ui["breadcrumb_home"]), "item": home},
            {"@type": "ListItem", "position": 2, "name": html.unescape(page["breadcrumb"]), "item": url}]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def editorial(copy):
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in copy["faq"])
    srcs = []
    for m in MARKETS:
        for u in m["sources"]:
            if u not in srcs:
                srcs.append(u)
    for u in PRICE_SOURCES:
        if u not in srcs:
            srcs.append(u)
    official = {re.sub(r"^https?://(www\.)?", "", m["official"]).split("/")[0] for m in MARKETS}

    def src_li(u):
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        label = esc(re.sub(r"^https?://(www\.)?", "", u)[:90])
        if host in official:  # organiser's own site: link it; press sources stay plain text
            return '<li><a href="%s" rel="nofollow noopener" target="_blank">%s</a></li>' % (u, label)
        return "<li>%s</li>" % label
    src_html = "".join(src_li(u) for u in srcs)
    ed = copy["editorial"]
    return f'''<section id="christmas-market-faq">
<h2 class="ltt-sec-title">{ed["faq_h2"]}</h2>
<div class="xm-faq">{faq}</div>
</section>
<section id="sources-method">
<h2 class="ltt-sec-title">{ed["src_h2"]}</h2>
<p>{ed["method"]}</p>
<ul class="xm-sources">{src_html}</ul>
</section>'''


# ---------------------------------------------------------------- skeleton
def ensure_page(lang):
    rel, path, tpl = PAGES[lang]
    fn = os.path.join(ROOT, rel)
    if os.path.exists(fn):
        return
    s = open(os.path.join(ROOT, tpl), encoding="utf-8").read()
    os.makedirs(os.path.dirname(fn) or ROOT, exist_ok=True)
    open(fn, "w", encoding="utf-8").write(s)


def hreflang_block():
    out = ""
    for lg in ("en", "de", "fr", "it", "es", "hu"):
        out += '<link href="%s%s" hreflang="%s" rel="alternate"/>' % (SITE, PAGES[lg][1], lg)
    out += '<link href="%s%s" hreflang="x-default" rel="alternate"/>' % (SITE, PAGES["en"][1])
    return out


def build(lang):
    ensure_page(lang)
    rel, path, _ = PAGES[lang]
    copy = importlib.import_module("christmas_markets_copy_%s" % lang).COPY
    ui, page = copy["ui"], copy["page"]
    fn = os.path.join(ROOT, rel)
    s = open(fn, encoding="utf-8").read()
    home = "/" if lang == "en" else "/%s" % lang
    url = SITE + path

    # head
    s = sub_once(r"<title>.*?</title>", lambda m: "<title>%s</title>" % page["title"], s, re.S)
    s = sub_once(r'<meta content="[^"]*" name="description"/>', lambda m: '<meta content="%s" name="description"/>' % esc(html.unescape(page["meta"])), s)
    for prop, val in (("og:title", page["title"]), ("og:description", page["meta"]), ("twitter:title", page["title"]), ("twitter:description", page["meta"])):
        s = re.sub(r'<meta content="[^"]*" (property|name)="%s"/>' % prop, lambda m: '<meta content="%s" %s="%s"/>' % (esc(html.unescape(val)), m.group(1), prop), s)
    s = re.sub(r'<meta content="[^"]*" (property|name)="(og:image|twitter:image)"/>', lambda m: '<meta content="%s%s" %s="%s"/>' % (SITE, page["og_image"], m.group(1), m.group(2)), s)
    s = re.sub(r'<meta content="[^"]*" property="og:url"/>', lambda m: '<meta content="%s" property="og:url"/>' % url, s)
    s = re.sub(r'<link href="[^"]*" rel="canonical"/>', lambda m: '<link href="%s" rel="canonical"/>' % url, s, count=1)
    s = re.sub(r'<link as="image" fetchpriority="high" href="[^"]*" rel="preload" type="image/[a-z]+"/>', "", s)
    # hreflang: only the 6 pages of this article
    s = re.sub(r'<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", s)
    s = s.replace('<link href="%s" rel="canonical"/>' % url, hreflang_block() + '<link href="%s" rel="canonical"/>' % url, 1)

    # components from the reference page + page css
    for tag, id_ in (("style", "bpa-lang-css"), ("style", "bpa-card2-css"), ("style", "cd-editorial-base"), ("style", "cd-bookmark-compact")):
        blk = bp.ref_block(tag, id_)
        if 'id="%s"' % id_ in s:
            s = re.sub(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, id_, tag), lambda m: blk, s, count=1, flags=re.S)
        else:
            s = s.replace("</head>", blk + "</head>", 1)
    if 'id="xm-page-css"' in s:
        s = re.sub(r'<style id="xm-page-css">.*?</style>', lambda m: PAGE_CSS, s, count=1, flags=re.S)
    else:
        s = s.replace("</head>", PAGE_CSS + "</head>", 1)
    blk = bp.ref_block("script", "bpa-lang-js")
    s = re.sub(r'<script id="bpa-lang-js"[^>]*>.*?</script>', lambda m: blk, s, count=1, flags=re.S)
    rt = bp.ref_block("script", "ltt-page-runtime").replace("querySelectorAll('.bpa-card')", "querySelectorAll('.bpa-card:not(.bpa-mkt)')")
    s = re.sub(r'<script id="ltt-page-runtime"[^>]*>.*?</script>', lambda m: rt, s, count=1, flags=re.S)

    # hero
    i = s.index('<div class="ltt-hero-wrap">')
    j = bp.balanced_end(s, i)
    s = s[:i] + hero(page, ui, home, lang) + s[j:]

    # deck container: markets deck, analysis, market sections with programs, cruise block
    i = s.index('<div class="ltt-deck-container"')
    j = bp.balanced_end(s, i)
    mcards = "\n".join(market_card(n, m, copy["markets"][m["key"]], ui) for n, m in enumerate(MARKETS, 1))
    num = {p["key"]: n for n, p in enumerate(PRODUCTS, 1)}
    secs = ""
    for key in [m["key"] for m in MARKETS] + ["food"]:
        cards = "\n".join(program_card(num[p["key"]], p, copy["products"][p["key"]], ui) for p in PRODUCTS if p["market"] == key)
        secs += section_html(key, copy, cards)
    deck = f'''<div class="ltt-deck-container" id="{DECK_ID}">
<div class="xm-wrap"><h2 id="markets-compared">{page["markets_h2"]}</h2><p class="xm-sub">{page["markets_sub"]}</p></div>
<div class="bpa-deck-wrap" id="ltt-cards-deck">
{mcards}
</div>
{analysis_html(copy)}
<div class="xm-wrap" id="programs-by-market">
<h2>{page["programs_h2"]}</h2>
<p class="xm-sub">{page["programs_sub"]}</p>
{secs}
{cruise_block(copy, lang)}
</div>
</div>'''
    s = s[:i] + deck + s[j:]

    # breakdown header + cards
    s = sub_once(r'(<h2 class="bpa-breakdown-heading"[^>]*>).*?(</h2>)', lambda m: m.group(1) + page["breakdown_h2"] + m.group(2), s, re.S)
    s = sub_once(r'(<p class="bpa-breakdown-sub">).*?(</p>)', lambda m: m.group(1) + page["breakdown_sub"] + m.group(2), s, re.S)
    s = sub_once(r'(onclick="toggleAllDetails\(true\)" type="button">).*?(</button>)', lambda m: m.group(1) + ui["expand"] + m.group(2), s, re.S)
    s = sub_once(r'(onclick="toggleAllDetails\(false\)" type="button">).*?(</button>)', lambda m: m.group(1) + ui["collapse"] + m.group(2), s, re.S)
    first = s.index('<details class="bpa-details-card"')
    end = first
    while True:
        end = bp.balanced_end(s, end, "details")
        nxt = s.find('<details class="bpa-details-card"', end)
        if nxt == -1 or s[end:nxt].strip():
            break
        end = nxt
    bds = "".join(breakdown(n, p, copy["products"][p["key"]], ui) for n, p in enumerate(PRODUCTS, 1))
    s = s[:first] + bds + s[end:]

    # editorial wrapper: FAQ + sources
    i = s.index('<div class="ltt-editorial-wrapper" role="main">')
    j = bp.balanced_end(s, i)
    s = s[:i] + '<div class="ltt-editorial-wrapper" role="main">' + editorial(copy) + "</div>" + s[j:]

    # floating bar, sheet, TOC config
    p1, c1 = PRODUCTS[0], copy["products"][PRODUCTS[0]["key"]]
    pick = bp.PICK_LABEL[lang]
    s = sub_once(r'(<button aria-label="[^"]*" class="hybrid-toc-btn".*?<span>).*?(</span>)', lambda m: m.group(1) + ui["sheet_contents"].format(n=len(PRODUCTS)) + m.group(2), s, re.S)
    s = sub_once(r'(id="hybridActiveBadge">).*?(</span>)', lambda m: m.group(1) + "#1 " + pick + m.group(2), s, re.S)
    s = sub_once(r'(id="hybridActiveTitle">).*?(</span>)', lambda m: m.group(1) + c1["short"] + m.group(2), s, re.S)
    s = sub_once(r'(id="hybridActivePrice">).*?(</span>)', lambda m: m.group(1) + ui["from"].format(p=p1["price_from"]) + m.group(2), s, re.S)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(")', lambda m: m.group(1) + esc(p1["book"]) + m.group(2), s)
    s = re.sub(r'(id="sticky-name">).*?(</span>)', lambda m: m.group(1) + c1["short"] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(id="sticky-price">).*?(</span>)', lambda m: m.group(1) + ui["from"].format(p=p1["price_from"]) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(id="sticky-rank">).*?(</span>)', lambda m: m.group(1) + "#1 " + pick + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(id="hybridTocBtn" type="button">.*?<span>).*?(</span>)', lambda m: m.group(1) + ui["all_programs"].format(n=len(PRODUCTS)) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<div aria-label=")[^"]*(" aria-modal="true" class="hybrid-sheet")', lambda m: m.group(1) + page["sheet_title"] + m.group(2), s)
    s = sub_once(r'(<h3 class="hybrid-sheet-title">).*?(</h3>)', lambda m: m.group(1) + page["sheet_title"] + m.group(2), s, re.S)
    cfg = {"deckId": DECK_ID, "tocDeckLabel": page["toc_deck"], "tocBreakdownLabel": page["toc_breakdown"], "pickLabel": pick,
           "shortTitles": [html.unescape(copy["products"][p["key"]]["short"]) for p in PRODUCTS]}
    s = sub_once(r"window\.LTT_PAGE_CONFIG = \{.*?\};", lambda m: "window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";", s, re.S)

    # JSON-LD
    s = sub_once(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">).*?(</script>)', lambda m: m.group(1) + jsonld(lang, path, copy) + m.group(2), s, re.S)

    if "—" in s.split("<body", 1)[1].split("<script", 1)[0] or "—" in jsonld(lang, path, copy):
        print("WARNING: em dash in", rel)
    open(fn, "w", encoding="utf-8").write(s)
    print("built", lang, rel, len(s))


if __name__ == "__main__":
    for lg in sys.argv[1:] or list(PAGES):
        build(lg)
