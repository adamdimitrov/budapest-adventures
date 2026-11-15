#!/usr/bin/env python3
"""Rebuild the private boat tours page (cards, breakdowns, hero, JSON-LD) for one or all languages.

Facts: scripts/private_boats_data.py      Copy: scripts/private_boats_copy_<lang>.py
Components are copied from the reference page best-budapest-river-cruises.html, so the
cards, pills and breakdowns look exactly like the river cruise guide.

    python3 scripts/build_private_boats.py            # all languages
    python3 scripts/build_private_boats.py en de      # only these
"""
import html
import importlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from private_boats_data import PRODUCTS, CHECKED, weighted  # noqa: E402

SITE = "https://www.budapestadventures.com"
PAGES = {
    "en": ("best-private-boat-tours-budapest.html", "/best-private-boat-tours-budapest", "/budapest-river-cruise-group-booking"),
    "de": ("de/private-bootsfahrten-budapest/index.html", "/de/private-bootsfahrten-budapest", "/de/gruppenbuchung-bootsfahrt-budapest"),
    "fr": ("fr/balades-bateau-prive-budapest/index.html", "/fr/balades-bateau-prive-budapest", "/fr/reservation-groupe-croisiere-budapest"),
    "it": ("it/tour-barca-privata-budapest/index.html", "/it/tour-barca-privata-budapest", "/it/prenotazione-gruppi-crociera-budapest"),
    "es": ("es/paseos-barco-privado-budapest/index.html", "/es/paseos-barco-privado-budapest", "/es/reserva-grupos-cruceros-budapest"),
    "hu": ("hu/legjobb-privát-hajókirándulások-budapest/index.html", "/hu/legjobb-privát-hajókirándulások-budapest", "/hu/budapest-nagy-csoportos-hajokirandulas"),
    "nl": ("nl/prive-boottocht-boedapest/index.html", "/nl/prive-boottocht-boedapest", "/nl/groepsboeking-cruise-boedapest"),
    "pt": ("pt/passeio-barco-privado-budapeste/index.html", "/pt/passeio-barco-privado-budapeste", "/pt/reserva-grupo-cruzeiros-budapeste"),
    "ro": ("ro/plimbari-barca-privata-budapesta/index.html", "/ro/plimbari-barca-privata-budapesta", "/ro/rezervari-grup-croaziere-budapesta"),
    "hr": ("hr/privatni-izleti-brodom-budimpesta/index.html", "/hr/privatni-izleti-brodom-budimpesta", "/hr/grupne-rezervacije-krstarenja-budimpesta"),
    "sr": ("sr/privatne-ture-brodom-budimpesta/index.html", "/sr/privatne-ture-brodom-budimpesta", "/sr/grupne-rezervacije-krstarenja-budimpesta"),
}
IMG_DIR = "/assets/private-boats/"
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"
STAR = '<svg aria-hidden="true" viewbox="0 0 24 24"><path d="M11.9999 18.26L4.94691 22.208L6.52191 14.28L0.586914 8.792L8.61391 7.84L11.9999 0.5L15.3859 7.84L23.4129 8.792L17.4779 14.28L19.0529 22.208L11.9999 18.26Z"></path></svg>'
HALF = '<svg aria-hidden="true" viewbox="0 0 24 24"><path d="M11.9999 15.968L16.2469 18.345L15.2979 13.572L18.8709 10.267L14.0379 9.694L11.9999 5.275V15.968ZM11.9999 18.26L4.94691 22.208L6.52191 14.28L0.586914 8.792L8.61391 7.84L11.9999 0.5L15.3859 7.84L23.4129 8.792L17.4779 14.28L19.0529 22.208L11.9999 18.26V18.26Z"></path></svg>'

REF = open(os.path.join(ROOT, "best-budapest-river-cruises.html"), encoding="utf-8").read()


def ref_icon(alt):
    m = re.search(r'<img alt="%s" class="bpa-rev-icon" loading="lazy" src="(data:[^"]+)"' % alt, REF)
    return m.group(1)


ICON = {"gyg": ref_icon("GetYourGuide"), "viator": ref_icon("Viator")}
SITE_NAME = {"gyg": "GetYourGuide", "viator": "Viator"}
PLACEHOLDER = re.search(r'data-src="[^"]+" decoding="async" loading="lazy" sizes="[^"]+" src="(data:[^"]+)"', REF).group(1)


def ref_block(tag, id_):
    if id_ == "cd-editorial-base":
        # base bookmark rules live inside the reference page's hero stylesheet
        hero_css = ref_block("style", "ltt-hero-card-styles")
        a = hero_css.index("/* Editorial Bookmark Cross-Link Card */")
        b = hero_css.index("@media", a)
        b = hero_css.index("}\n}", b) + 3
        return '<style id="cd-editorial-base">\n%s\n</style>' % hero_css[a:b]
    m = re.search(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, id_, tag), REF, re.S)
    return m.group(0)


def esc(s):
    return html.escape(s, quote=True)


def fmt1(x):
    return ("%.1f" % x)


def count_str(n):
    return "%d" % n


def stars(r):
    full = int(r)
    half = (r - full) >= 0.25
    out = STAR * full + (HALF if half and full < 5 else "")
    return out


def product_links(p):
    return {"gyg": p["gyg"], "viator": p["viator"]}


def balanced_end(s, start, tag="div"):
    """Index just after the element that opens at s[start]."""
    depth = 0
    for m in re.compile(r"<(/?)%s\b" % tag).finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s.index(">", m.end()) + 1
    raise ValueError("unbalanced %s at %d" % (tag, start))


# ---------------------------------------------------------------- deck card
def rate_block(p, ui):
    r, n = weighted(p["ratings"])
    if not n:
        return '<div class="bpa-summary-reviews bpa-rate"><span class="bpa-rate-meta" style="font-size:13px;color:#64748b">✨ %s</span></div>' % ui["new_listing"]
    links = product_links(p)
    badges = ""
    for site, score, cnt in p["ratings"]:
        badges += ('<a class="bpa-rev-badge is-link" href="%s" rel="noopener nofollow sponsored" target="_blank">'
                   '<img alt="%s" class="bpa-rev-icon" loading="lazy" src="%s"/><span class="bpa-rev-site">%s</span>'
                   '<span class="bpa-rev-score">%s</span><span class="bpa-rev-count">(%d)</span>'
                   '<span class="bpa-rev-go" aria-hidden="true">→</span></a>') % (
            esc(links[site]), SITE_NAME[site], ICON[site], SITE_NAME[site], fmt1(score), cnt)
    nsites = len(p["ratings"])
    meta = (ui["reviews_sites"] if nsites > 1 else ui["reviews_site"]).format(count=n, n=nsites)
    return ('<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            '<span class="bpa-stars" style="--r:%.2f" aria-hidden="true"></span><b class="bpa-rate-score">%s</b>'
            '<span class="bpa-rate-meta">%s</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            '<div class="bpa-lang-pop"><strong>%s</strong><span class="bpa-rate-list">%s</span></div></details></div>') % (
        r, fmt1(r), meta, ui["avg_note"].format(n=nsites), badges)


def pill(pl):
    cls = "bpa-lang" + ((" " + pl["cls"]) if pl.get("cls") else "")
    note = '<span class="bpa-lang-note">%s</span>' % pl["note"] if pl.get("note") else ""
    return ('<details class="%s"><summary class="bpa-sp">%s <span class="bpa-lang-label">%s</span>'
            '<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">%s%s</div></details>') % (
        cls, pl["icon"], pl["label"], pl["body"], note)


def kicker(p, c, link=True):
    pier = p["pier"] or c["qf_badge"]
    if p["pier_map"] and link:
        q = p["pier_map"].replace(" ", "+")
        pier_html = ('<a class="bpa-kicker-map-link" href="https://www.google.com/maps/search/?api=1&amp;query=%s" '
                     'onclick="event.stopPropagation()" rel="noopener noreferrer" target="_blank">%s</a>') % (q, esc(pier))
    else:
        pier_html = '<span class="bpa-kicker-map-link">%s</span>' % esc(pier)
    return '<div class="bpa-kicker">%s • ⏱️ %s • %s</div>' % (esc(p["operator"]), c["duration"], pier_html)


def deck_card(i, p, c, ui):
    imgs = ""
    for k, f in enumerate(p["images"]):
        if k == 0:
            extra = 'fetchpriority="high" loading="eager"' if i == 1 else 'loading="lazy"'
            imgs += '<img alt="%s" height="534" %s sizes="%s" src="%s%s" width="800"/>' % (esc(c["alt"]), extra, SIZES, IMG_DIR, f)
        else:
            imgs += '<img alt="%s" data-src="%s%s" decoding="async" loading="lazy" sizes="%s" src="%s"/>' % (esc(c["alt"]), IMG_DIR, f, SIZES, PLACEHOLDER)
    pills = "\n".join(pill(pl) for pl in c["pills"])
    trust = "".join("<span>%s</span>" % t for t in c["trust"])
    return f'''<!-- #{i}: {c["short"]} -->
<div class="bpa-card" data-cat="{p["cat"]}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {p["rank_class"]}">{c["rank_tag"]}</span>
<button aria-label="{ui["prev"]}" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button><button aria-label="{ui["next"]}" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button><span class="bpa-pill">1 / {len(p["images"])}</span><div aria-label="{ui["photo_gallery"].format(n=i)}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">{imgs}</div>
</div>
<div class="bpa-info">
{kicker(p, c)}
<a class="bpa-title" href="{esc(p["gyg"])}" rel="nofollow sponsored noopener" target="_blank">{c["title"]}</a>
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
<div class="bpa-psub">{ui["per_boat"].format(cap=p["capacity"])}</div>
</div>
<a class="bpa-btn" href="{esc(p["gyg"])}" rel="nofollow sponsored noopener" target="_blank">{ui["check"]}</a>
<div class="bpa-via">{ui["via_gyg"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{p["anchor"]}">{ui["read"]}</a>
</div>
</div>
</div>'''


# ---------------------------------------------------------------- breakdown
def summary_badges(p):
    out = ""
    for site, score, cnt in p["ratings"]:
        out += ('<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="%s"/>'
                '<span class="bpa-rev-score">%s</span><span class="bpa-rev-stars">%s</span>'
                '<span class="bpa-rev-count">(%d)</span></span>') % (ICON[site], fmt1(score), stars(score), cnt)
    return out


def breakdown(i, p, c, ui, group_url, page):
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
    cta = page["group_cta"].replace("/budapest-river-cruise-group-booking", group_url)
    perks = [ui["perk_cancel"], ui["perk_pay"]]
    if p["pier"]:
        perks.append(ui["perk_from"].format(v=esc(p["pier"])))
    perks.append(ui["perk_dur"].format(v=c["duration"]))
    perks_html = "".join('<span class="ltt-buy-perk">%s</span>' % x for x in perks)
    walk = ""
    for h4, idx, text in c["walk"]:
        walk += ('<div class="ltt-sp-card"><h4>%s</h4><img alt="%s" loading="lazy" sizes="(max-width: 640px) 100vw, 420px" src="%s%s"/>'
                 '<ul role="list"><li>%s</li></ul></div>\n') % (h4, esc(c["alt"]), IMG_DIR, p["images"][idx], text)
    qf = "".join('<div class="qf1-row"><div class="qf1-label">%s</div><div class="qf1-val">%s</div></div>\n' % x for x in c["qf"])
    chips = "".join('<span class="qf1-chip %s">%s</span>\n' % x for x in c["chips"])
    price = ui["from"].format(p=p["price_from"])
    psub = ui["per_boat"].format(cap=p["capacity"])
    return f'''<details class="bpa-details-card" data-cat="{p["cat"]}" id="{p["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {p["rank_class"]}">{c["rank_tag"]}</span>
{kicker(p, c, link=False)}
</div>
<h3 class="bpa-details-title">{c["title"]}</h3>
<div class="bpa-reviews-line">
<div class="bpa-summary-reviews"><div class="div-block-53">{summary_badges(p) or '<span class="bpa-rev-count" style="font-size:13px;color:#64748b">✨ ' + ui["new_listing"] + '</span>'}</div></div>
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
<div class="ltt-cross-sell-wrap"><blockquote>{cta}</blockquote></div>
<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>{ui["buy_badge"]}</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{price}</span>
<span class="ltt-buy-price-sub">{psub}</span>
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
<a class="ltt-buy-cta-btn" href="{esc(p["gyg"])}" rel="noopener nofollow sponsored" target="_blank">
<span>{ui["buy_cta"]}</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
<span>{ui["buy_trust"]}</span>
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


# ---------------------------------------------------------------- hero
GROUP_THUMB = "/assets/cdn/60e43c7d6d05b671dff0dc1a/6482365138e2c970cdc10bc0_1-Best-River-Cruises-Budapest.webp"


def group_bookmark(bm, group_url):
    """Compact editorial bookmark to the group booking page (styled by #cd-bookmark-compact)."""
    return f'''
<figure class="cd-bookmark-wrapper">
<a href="{group_url}" class="cd-editorial-bookmark">
<div class="cd-editorial-body">
<div>
<div class="cd-editorial-title">{esc(bm["title"])}</div>
<div class="cd-editorial-desc">{esc(bm["desc"])}</div>
</div>
</div>
<div class="cd-editorial-thumb">
<img src="{GROUP_THUMB}" alt="{esc(bm["title"])}" loading="lazy" width="64" height="64"/>
</div>
</a>
</figure>'''


def hero(page, ui, home, group_url):
    lead = "".join("<p>%s</p>" % x for x in page["lead"]).replace("/budapest-river-cruise-group-booking", group_url)
    lead += group_bookmark(page["group_bookmark"], group_url)
    filters = "".join(
        '<button class="ltt-tab-btn%s" data-cat="%s" onclick="lttFilterItems(\'%s\', this)" type="button">%s</button>' % (
            " active" if cat == "all" else "", cat, cat, label) for cat, label in page["filters"])
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
<span class="ltt-filter-label">{ui["filters"]}</span>
<div class="ltt-integrated-pills">
{filters}
</div>
</div>
</div>
</div>'''


# ---------------------------------------------------------------- JSON-LD
def jsonld(s, lang, path, page, copy):
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    data = json.loads(m.group(2))
    url = SITE + path
    items = []
    for i, p in enumerate(PRODUCTS, 1):
        c = copy["products"][p["key"]]
        prod = {
            "@type": "Product",
            "name": html.unescape(c["title"]),
            "description": html.unescape(re.sub("<[^>]+>", "", c["summary"][0])),
            "image": SITE + IMG_DIR + p["images"][0],
            "brand": {"@type": "Organization", "name": p["brand"]},
            "offers": {"@type": "AggregateOffer", "lowPrice": str(p["price_from"]), "highPrice": str(p["price_high"]),
                       "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": html.unescape(p["gyg"])},
        }
        r, n = weighted(p["ratings"])
        if n:
            prod["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": fmt1(r), "bestRating": "5",
                                       "worstRating": "1", "reviewCount": str(n)}
        items.append({"@type": "ListItem", "position": i, "url": url + "#" + p["anchor"], "item": prod})
    for node in data["@graph"]:
        if node["@type"] == "Article":
            node["headline"] = html.unescape(page["title"])
            node["description"] = html.unescape(page["meta"])
            node["url"] = url
            node["inLanguage"] = lang
            node["dateModified"] = CHECKED
            node["author"]["jobTitle"] = "Founder of Budapest Adventures"
            node["image"] = [SITE + IMG_DIR + p["images"][0] for p in PRODUCTS]
            node["mainEntity"] = {"@type": "ItemList", "name": html.unescape(page["title"]),
                                  "description": html.unescape(page["meta"]),
                                  "itemListOrder": "https://schema.org/ItemListOrderAscending",
                                  "numberOfItems": len(items), "itemListElement": items}
        if node["@type"] == "BreadcrumbList":
            home = SITE + ("/" if lang == "en" else "/" + lang)
            node["itemListElement"] = [
                {"@type": "ListItem", "position": 1, "name": html.unescape(copy["ui"]["breadcrumb_home"]), "item": home},
                {"@type": "ListItem", "position": 2, "name": html.unescape(page["breadcrumb"]), "item": url}]
    return s[:m.start(2)] + json.dumps(data, ensure_ascii=False) + s[m.end(2):]


# ---------------------------------------------------------------- page
def sub_once(pattern, repl, s, flags=0):
    new, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        raise ValueError("pattern not found: " + pattern[:80])
    return new


PICK_LABEL = {"en": "PICK", "de": "TIPP", "fr": "CHOIX", "it": "SCELTA", "es": "OPCIÓN", "hu": "VÁLASZTÁS", "nl": "KEUZE", "pt": "ESCOLHA", "ro": "ALEGERE", "hr": "IZBOR", "sr": "ИЗБОР"}

HU_TEMPLATE = {
    "Inhaltsverzeichnis öffnen": "Tartalomjegyzék megnyitása",
    "Inhaltsverzeichnis": "Tartalomjegyzék",
    "Kostenlose 24h-Stornierung": "Ingyenes lemondás 24 óráig",
    "Nach oben": "Fel",
    "Schließen": "Bezárás",
    "Schnellnavigation &amp; Buchung für Schifffahrten": "Gyors navigáció &amp; foglalás",
    "Schnellnavigation &amp; Buchung": "Gyors navigáció &amp; foglalás",
    "Zum Testbericht der Schifffahrt springen": "Ugrás a hajó leírásához",
    "Verfügbarkeit prüfen →": "Szabad időpontok →",
}


def hu_skeleton():
    """The HU page still runs an old Webflow template; rebuild it on the DE page's structure."""
    de = open(os.path.join(ROOT, PAGES["de"][0]), encoding="utf-8").read()
    rel, path, _ = PAGES["hu"]
    url = SITE + path
    s = de.replace('lang="de"', 'lang="hu"', 1)
    s = re.sub(r'<link href="[^"]*" rel="canonical"/>', '<link href="%s" rel="canonical"/>' % url, s, count=1)
    s = re.sub(r'content="[^"]*" property="og:url"', 'content="%s" property="og:url"' % url, s)
    for k, v in HU_TEMPLATE.items():
        s = s.replace(k, v)
    open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(s)


def build(lang):
    rel, path, group_url = PAGES[lang]
    if lang == "hu" and 'id="ltt-cards-deck"' not in open(os.path.join(ROOT, rel), encoding="utf-8").read():
        hu_skeleton()
    copy = importlib.import_module("private_boats_copy_%s" % lang).COPY
    ui, page = copy["ui"], copy["page"]
    fn = os.path.join(ROOT, rel)
    s = open(fn, encoding="utf-8").read()
    home = "/" if lang == "en" else "/%s" % lang

    # head
    s = sub_once(r"<title>.*?</title>", "<title>%s</title>" % page["title"], s, re.S)
    s = sub_once(r'<meta content="[^"]*" name="description"/>', '<meta content="%s" name="description"/>' % esc(html.unescape(page["meta"])), s)
    s = re.sub(r'<meta content="[^"]*" property="og:title"/>', '<meta content="%s" property="og:title"/>' % esc(html.unescape(page["title"])), s)
    s = re.sub(r'<meta content="[^"]*" property="og:description"/>', '<meta content="%s" property="og:description"/>' % esc(html.unescape(page["meta"])), s)
    s = re.sub(r'<meta content="[^"]*" property="twitter:title"/>', '<meta content="%s" property="twitter:title"/>' % esc(html.unescape(page["title"])), s)
    s = re.sub(r'<meta content="[^"]*" property="twitter:description"/>', '<meta content="%s" property="twitter:description"/>' % esc(html.unescape(page["meta"])), s)
    s = re.sub(r'<meta content="[^"]*" property="og:image"/>', '<meta content="%s%s" property="og:image"/>' % (SITE, page["og_image"]), s)
    s = re.sub(r'<link as="image" fetchpriority="high" href="[^"]*" rel="preload" type="image/webp"/>',
               '<link as="image" fetchpriority="high" href="%s%s" rel="preload" type="image/webp"/>' % (IMG_DIR, PRODUCTS[0]["images"][0]), s)

    # components from the reference page
    for tag, id_ in (("style", "bpa-lang-css"), ("style", "bpa-card2-css"), ("style", "cd-editorial-base"), ("style", "cd-bookmark-compact")):
        blk = ref_block(tag, id_)
        if 'id="%s"' % id_ in s:
            s = re.sub(r'<%s id="%s"[^>]*>.*?</%s>' % (tag, id_, tag), lambda m: blk, s, count=1, flags=re.S)
        elif id_ == "cd-editorial-base" and '<style id="cd-bookmark-compact">' in s:
            s = s.replace('<style id="cd-bookmark-compact">', blk + '<style id="cd-bookmark-compact">', 1)
        else:
            s = s.replace("</head>", blk + "</head>", 1)
    blk = ref_block("script", "bpa-lang-js")
    if 'id="bpa-lang-js"' in s:
        s = re.sub(r'<script id="bpa-lang-js"[^>]*>.*?</script>', lambda m: blk, s, count=1, flags=re.S)
    else:
        i = s.rfind("</body>")
        s = s[:i] + blk + s[i:]
    rt = ref_block("script", "ltt-page-runtime")
    s = re.sub(r'<script id="ltt-page-runtime"[^>]*>.*?</script>', lambda m: rt, s, count=1, flags=re.S)

    # legacy Webflow scripts that inject "Personally Tested" pills / old rating tables
    s = re.sub(r"<style>\.personally-tested-pill\{.*?</style>", "", s, flags=re.S)
    s = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const cruiseCards.*?</script>', "", s, flags=re.S)
    s = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", async \(\) => \{\s*const findByText.*?</script>', "", s, flags=re.S)

    # hero
    i = s.index('<div class="ltt-hero-wrap">')
    j = balanced_end(s, i)
    s = s[:i] + hero(page, ui, home, group_url) + s[j:]

    # deck
    i = s.index('<div class="bpa-deck-wrap" id="ltt-cards-deck">')
    j = balanced_end(s, i)
    cards = "\n".join(deck_card(n, p, copy["products"][p["key"]], ui) for n, p in enumerate(PRODUCTS, 1))
    s = s[:i] + '<div class="bpa-deck-wrap" id="ltt-cards-deck">\n' + cards + "\n</div>" + s[j:]

    # breakdown header + cards
    s = sub_once(r'(<h2 class="bpa-breakdown-heading"[^>]*>).*?(</h2>)', r"\g<1>%s\g<2>" % page["breakdown_h2"].replace("\\", "\\\\"), s, re.S)
    s = sub_once(r'(<p class="bpa-breakdown-sub">).*?(</p>)', r"\g<1>%s\g<2>" % page["breakdown_sub"], s, re.S)
    s = sub_once(r'(onclick="toggleAllDetails\(true\)" type="button">).*?(</button>)', r"\g<1>%s\g<2>" % ui["expand"], s, re.S)
    s = sub_once(r'(onclick="toggleAllDetails\(false\)" type="button">).*?(</button>)', r"\g<1>%s\g<2>" % ui["collapse"], s, re.S)
    first = s.index('<details class="bpa-details-card"')
    end = first
    while True:
        end = balanced_end(s, end, "details")
        nxt = s.find('<details class="bpa-details-card"', end)
        if nxt == -1 or s[end:nxt].strip():
            break
        end = nxt
    bds = "".join(breakdown(n, p, copy["products"][p["key"]], ui, group_url, page) for n, p in enumerate(PRODUCTS, 1))
    s = s[:first] + bds + s[end:]

    # floating bar, sheet, TOC config
    p1, c1 = PRODUCTS[0], copy["products"][PRODUCTS[0]["key"]]
    s = sub_once(r'(<button aria-label="[^"]*" class="hybrid-toc-btn".*?<span>).*?(</span>)', r"\g<1>%s\g<2>" % ui["sheet_contents"].format(n=len(PRODUCTS)), s, re.S)
    s = sub_once(r'(id="hybridActiveBadge">).*?(</span>)', r"\g<1>%s\g<2>" % ("#1 " + PICK_LABEL[lang]), s, re.S)
    s = sub_once(r'(id="hybridActiveTitle">).*?(</span>)', r"\g<1>%s\g<2>" % c1["short"], s, re.S)
    s = sub_once(r'(id="hybridActivePrice">).*?(</span>)', r"\g<1>%s\g<2>" % ui["from"].format(p=p1["price_from"]), s, re.S)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(")', lambda m: m.group(1) + esc(p1["gyg"]) + m.group(2), s)
    s = re.sub(r'(id="sticky-name">).*?(</span>)', lambda m: m.group(1) + c1["short"] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(id="sticky-price">).*?(</span>)', lambda m: m.group(1) + ui["from"].format(p=p1["price_from"]) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(id="sticky-rank">).*?(</span>)', lambda m: m.group(1) + "#1 " + PICK_LABEL[lang] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(id="hybridTocBtn" type="button">.*?<span>).*?(</span>)', lambda m: m.group(1) + ui["all_boats"].format(n=len(PRODUCTS)) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<meta content="[^"]*" name="twitter:title"/>', lambda m: '<meta content="%s" name="twitter:title"/>' % esc(html.unescape(page["title"])), s)
    s = re.sub(r'<meta content="[^"]*" name="twitter:description"/>', lambda m: '<meta content="%s" name="twitter:description"/>' % esc(html.unescape(page["meta"])), s)
    s = re.sub(r'<meta content="[^"]*" name="twitter:image"/>', lambda m: '<meta content="%s%s" name="twitter:image"/>' % (SITE, page["og_image"]), s)
    s = re.sub(r'(<div aria-label=")[^"]*(" aria-modal="true" class="hybrid-sheet")', r"\g<1>%s\g<2>" % page["sheet_title"], s)
    s = sub_once(r'(<h3 class="hybrid-sheet-title">).*?(</h3>)', r"\g<1>%s\g<2>" % page["sheet_title"], s, re.S)
    cfg = {"deckId": re.search(r'"deckId": "([^"]+)"', s).group(1), "tocDeckLabel": page["toc_deck"],
           "tocBreakdownLabel": page["toc_breakdown"], "pickLabel": PICK_LABEL[lang],
           "shortTitles": [html.unescape(copy["products"][p["key"]]["short"]) for p in PRODUCTS]}
    s = sub_once(r"window\.LTT_PAGE_CONFIG = \{.*?\};", lambda m: "window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";", s, re.S)

    s = s.replace('aria-label="Zum Testbericht der Schifffahrt springen"', 'aria-label="Zur Bootsbeschreibung springen"')
    s = jsonld(s, lang, path, page, copy)
    open(fn, "w", encoding="utf-8").write(s)
    print("built", lang, rel, len(s))


if __name__ == "__main__":
    langs = sys.argv[1:] or list(PAGES)
    if "hu" in langs and "de" not in langs:
        langs = ["de"] + langs
    for lg in langs:
        build(lg)
