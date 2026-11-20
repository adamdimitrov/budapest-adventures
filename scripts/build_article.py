#!/usr/bin/env python3
"""Build a new BPA comparison article (EN) from a JSON spec, inside the shell of
best-day-trips-from-budapest.html (head CSS, nav, footer, deck CSS, runtime JS).
Ported from the luxurytraveltester builder (Dubai batch, 2026-11-16).

    python3 scripts/build_article.py scripts/articles/<slug>.json      # writes <slug>.html
    python3 scripts/build_article.py --photos scripts/articles/<slug>.json  # also downloads + converts photos

Spec format: see scripts/articles/README.md. Everything the reader sees comes from the
spec; the shell only provides chrome and styles. Run scripts/sync_layout.py afterwards
(menu/footer/search) and ~/.claude/skills/qc-article/qc_article.py.
"""
import argparse, copy, datetime as dt, html, io, json, re, sys, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / "best-day-trips-from-budapest.html"
SITE = "https://www.budapestadventures.com"
GYG_PARTNER = "YS414AJ"
AUTHOR = {"name": "Adam Dimitrov", "url": "/about",
          "avatar": "/assets/adam-dimitrov.webp"}
CDN = "https://cdn.getyourguide.com/image/fit=crop,width=1200,height=800/tour_img/{}"
LAZY = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"
REL = 'rel="nofollow sponsored noopener" target="_blank"'
E = html.escape


def esc_attr(s):
    return html.escape(str(s), quote=True)


def gyg_link(path_or_url, cmp):
    u = path_or_url if path_or_url.startswith("http") else "https://www.getyourguide.com" + path_or_url
    u = u.split("?")[0]
    return f"{u}?partner_id={GYG_PARTNER}&utm_medium=online_publisher&cmp={cmp}&mkt_cmp=true"


TIQETS_PARTNER = "thecruisedetective.com-176436"
TIQETS_ICON = "/assets/cdn/652d0405192ba076b04f74a3/6852917a8b23e16d4296b394_tiqets-logo.avif"


def tiqets_link(url, cmp):
    u = url.split("?")[0]
    return f"{u}?partner={TIQETS_PARTNER}&tq_campaign={cmp}"


def compact(n):
    n = int(n)
    if n >= 1000:
        v = n / 1000
        return (f"{v:.1f}".rstrip("0").rstrip(".")) + "k+"
    return str(n)


def money(v):
    v = float(v)
    return f"€{v:.0f}" if v >= 10 or v == int(v) else f"€{v:.2f}"


# ------------------------------------------------------------------ photos
def fetch_photos(spec, slug):
    from PIL import Image
    out_dir = ROOT / "assets" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    for n, it in enumerate(spec["items"], 1):
        paths = []
        for k, h in enumerate(it.get("gallery", [])[:10], 1):
            name = f"{n:02d}-{it['photo_slug']}-{k:02d}.avif"
            dst = out_dir / name
            if not dst.exists():
                src = h if h.startswith("http") else CDN.format(h)
                req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
                data = urllib.request.urlopen(req, timeout=30).read()
                im = Image.open(io.BytesIO(data)).convert("RGB")
                im.save(dst, "AVIF", quality=55)
            paths.append(f"/assets/{slug}/{name}")
        it["photos"] = paths


# ------------------------------------------------------------------ fragments
PILL_KIND = {"time": " bpa-time", "access": " cd-access", "vibe": " fbm-vibe"}
PILLS_MIN, PILLS_MAX = 6, 8   # river cruise card: two full rows of pills


def pill_html(p):
    note = f'<span class="bpa-lang-note">{p["note"]}</span>' if p.get("note") else ""
    kind = PILL_KIND.get(p.get("kind", ""), "")
    return (f'<details class="bpa-lang{kind}"><summary class="bpa-sp">{p["emoji"]} <span class="bpa-lang-label">{E(p["label"])}</span>'
            f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{E(p["lead"])}</strong> '
            f'{p["body"]}{note}</div></details>')


def rating_html(it, gyg_icon):
    if not it.get("rating") or not it.get("reviews"):
        return '<div class="bpa-summary-reviews bpa-rate"><span class="bpa-rate-meta">New listing, no reviews yet</span></div>'
    return (f'<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            f'<span class="bpa-stars" style="--r:{it["rating"]:.2f}" aria-hidden="true"></span><b class="bpa-rate-score">{it["rating"]:.1f}</b>'
            f'<span class="bpa-rate-meta">{compact(it["reviews"])} reviews · 1 site</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            f'<div class="bpa-lang-pop"><strong>Rating on {it["_pname"]}</strong><span class="bpa-rate-list"><a class="bpa-rev-badge is-link" href="{esc_attr(it["link"])}" rel="nofollow sponsored noopener" target="_blank">'
            f'<img alt="{it["_pname"]}" class="bpa-rev-icon" loading="lazy" src="{it["_picon"]}"/><span class="bpa-rev-site">{it["_pname"]}</span>'
            f'<span class="bpa-rev-score">{it["rating"]:.1f}</span><span class="bpa-rev-count">({compact(it["reviews"])})</span>'
            f'<span class="bpa-rev-go" aria-hidden="true">→</span></a></span></div></details></div>')


def slider_html(it, first_card):
    imgs = []
    alt = esc_attr(it["title"])
    for i, src in enumerate(it["photos"]):
        if i == 0:
            fp = ' fetchpriority="high"' if first_card else ""
            imgs.append(f'<img alt="{alt}"{fp} height="500" loading="{"eager" if first_card else "lazy"}" src="{src}" width="800"/>')
        else:
            imgs.append(f'<img alt="{alt}" data-src="{src}" decoding="async" height="500" loading="lazy" src="{LAZY}" width="800"/>')
    ctrl = ""
    if len(imgs) > 1:
        ctrl = ('<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>\n'
                '<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>\n'
                f'<span class="bpa-pill">1 / {len(imgs)}</span>\n')
    return (f'<div class="bpa-media">\n<span class="bpa-rank-tag {it["rank_class"]}">{it["rank_tag"]}</span>\n{ctrl}'
            f'<div aria-label="Photo Carousel" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">\n' + "\n".join(imgs) + '\n</div>\n</div>')


def kicker_html(it):
    return (f'<div class="bpa-kicker">{E(it["operator"])} • ⏱️ {E(it["duration"])} • <a class="bpa-kicker-map-link" '
            f'href="https://www.google.com/maps/search/?api=1&amp;query={esc_attr(it["map_q"].replace(" ", "+"))}" onclick="event.stopPropagation()" '
            f'rel="noopener noreferrer" target="_blank">📍 {E(it["place"])}</a></div>')


def card_html(n, it, gyg_icon):
    if not PILLS_MIN <= len(it["pills"]) <= PILLS_MAX:
        sys.exit(f'card {n} ({it["title"][:40]}): {len(it["pills"])} pills, need {PILLS_MIN}-{PILLS_MAX} (river cruise card)')
    pills = "\n".join(pill_html(p) for p in it["pills"])
    was = ""
    if it.get("price_was") and float(it["price_was"]) > float(it["price"]):
        pct = round((1 - float(it["price"]) / float(it["price_was"])) * 100)
        was = f'<div class="bpa-was"><s>{money(it["price_was"])}</s> <span>−{pct}%</span></div>\n'
    trust = "".join(f"<span>✓ {E(t)}</span>" for t in it.get("trust", []))
    return f'''<!-- #{n}: {E(it["title"])} -->
<div class="bpa-card" data-cat="{it["cat"]}" id="card-{n}">
<div class="bpa-main">
{slider_html(it, n == 1)}
<div class="bpa-info">
{kicker_html(it)}
<a class="bpa-title" href="{esc_attr(it["link"])}" {REL}>{E(it["title"])}</a>
<div class="bpa-reviews-line">
{rating_html(it, gyg_icon)}
</div>
<div class="bpa-specs-row">
{pills}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">✓ Pick it</span> {it["pick"]} <span class="bpa-skip">✕ Skip it</span> {it["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
{was}<div class="bpa-price">From {money(it["price"])}</div>
<div class="bpa-psub">{E(it.get("price_unit", "per person"))}</div>
</div>
<a class="bpa-btn" href="{esc_attr(it["link"])}" {REL}>Check Availability →</a>
<div class="bpa-via">Booked securely via {it["_pname"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{it["anchor"]}">Read Review ↓</a>
</div>
</div>
</div>'''


def details_html(n, it, gyg_icon):
    pros = "".join(f"<li><strong>{E(p)}</strong></li>" for p in it["pros"])
    cons = "".join(f"<li><strong>{E(c)}</strong></li>" for c in it["cons"])
    facts = "".join(f'<div class="qf1-row"><div class="qf1-label">{E(k)}</div><div class="qf1-val">{v}</div></div>' for k, v in it.get("facts", []))
    qf = (f'<div class="qf1-wrap"><div class="qf1-title-row"><h4 class="qf1-title">Quick Facts</h4>'
          f'<span class="qf1-badge">{E(it["short_title"])}</span></div><div class="qf1-table">{facts}</div></div>') if facts else ""
    review = "".join(f"<p>{p}</p>" for p in it["review"])
    perks = "".join(f'<span class="ltt-buy-perk">{p}</span>' for p in [
        "🛡️ " + E(it.get("cancel", "Free cancellation up to 24 hours before")),
        f"📍 Start: <strong>{E(it['place'])}</strong>", f"⏱️ Duration: <strong>{E(it['duration'])}</strong>"])
    return f'''<details class="bpa-details-card" data-cat="{it["cat"]}" id="{it["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {it["rank_class"]}">{it["rank_tag"]}</span>
{kicker_html(it)}
</div>
<h3 class="bpa-details-title">{E(it["title"])}</h3>
<div class="bpa-reviews-line">
{rating_html(it, gyg_icon) if not it.get("reviews") else ""}<div class="bpa-summary-reviews"{' hidden=""' if not it.get("reviews") else ""}><div class="div-block-53"><a class="bpa-rev-badge" href="{esc_attr(it["link"])}" onclick="event.stopPropagation()" rel="nofollow sponsored noopener" target="_blank"><img alt="{it["_pname"]}" class="bpa-rev-icon" loading="lazy" src="{it["_picon"]}"/><span class="bpa-rev-score">{(it.get("rating") or 0):.1f}</span><span class="bpa-rev-count">({compact(it.get("reviews") or 0)})</span></a></div></div>
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">From {money(it["price"])}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell"><div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>Pros:</strong></h3><ul role="list">{pros}</ul></div></div><div class="pro-con-box-con-cell"><div class="pro-con-box-con-cell-rich-text-block w-richtext"><h3><strong>Cons:</strong></h3><ul role="list">{cons}</ul></div></div></div></div>
<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">📝 Review &amp; Quick Facts</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">Overview</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
<div class="w-richtext">{review}</div>
<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge"><span class="ltt-live-dot"></span><span>Live Availability</span></div>
<div class="ltt-buy-card-price"><span class="ltt-buy-price-val">From {money(it["price"])}</span><span class="ltt-buy-price-sub">{E(it.get("price_unit", "per person"))}</span></div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{E(it["short_title"])}</h4>
<div class="ltt-buy-card-perks">{perks}</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{esc_attr(it["link"])}" {REL}><span>Check Dates &amp; Book</span><span class="ltt-cta-arrow">→</span></a>
</div>
</div>
</div>
</div>
</details>
{qf}
</div>
</details>'''


GUIDE_CSS = """
<style id="ltt-guide-styles">
.ltt-guide{max-width:860px;margin:40px auto 0;font-size:16px;line-height:1.65;color:#1e293b}
.ltt-guide h2{font-family:'Playfair Display',Georgia,serif;font-size:28px;line-height:1.25;margin:36px 0 12px;color:#0f172a}
.ltt-guide h3{font-size:19px;margin:22px 0 8px;color:#0f172a}
.ltt-guide p{margin:0 0 14px}
.ltt-guide ul{margin:0 0 16px 20px}
.ltt-guide a{color:#855a00;font-weight:600;text-decoration:underline}
.ltt-guide a:hover,.ltt-guide a:focus{color:#5c3e00}
.ltt-guide-tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0 20px;border:1px solid #e2e8f0;border-radius:12px}
.ltt-guide table{border-collapse:collapse;width:100%;min-width:560px;font-size:14px}
.ltt-guide th,.ltt-guide td{padding:10px 12px;border-bottom:1px solid #e2e8f0;text-align:left;vertical-align:top}
.ltt-guide th{background:#f8fafc;font-weight:700;color:#0f172a}
.ltt-guide tr:last-child td{border-bottom:0}
.ltt-faq details{border:1px solid #e2e8f0;border-radius:12px;padding:12px 16px;margin:0 0 10px;background:#fff}
.ltt-faq summary{cursor:pointer;font-weight:700;color:#0f172a}
.ltt-faq summary:hover{color:#855a00}
.ltt-faq details p{margin:10px 0 0}
/* no red hover */
.bpa-kicker-map-link:hover,.bpa-title:hover,.bpa-sublink:hover,.bpa-rev-badge:hover,.ltt-breadcrumbs a:hover,.ltt-author-line a:hover{color:inherit}
.bpa-btn:hover,.ltt-buy-cta-btn:hover,.hybrid-cta-btn:hover{color:#fff}
@media (max-width:767px){.ltt-guide{padding:0 4px}.ltt-guide h2{font-size:23px}}
</style>"""


def guide_html(spec):
    parts = [GUIDE_CSS, '<div class="ltt-guide w-richtext">']
    for sec in spec.get("guide", []):
        parts.append(f'<h2 id="{sec["id"]}">{E(sec["h2"])}</h2>')
        parts.append(sec["html"])
    if spec.get("faqs"):
        parts.append('<h2 id="faq">Frequently Asked Questions</h2><div class="ltt-faq">')
        for f in spec["faqs"]:
            parts.append(f'<details><summary>{E(f["q"])}</summary><p>{f["a"]}</p></details>')
        parts.append("</div>")
    if spec.get("methodology"):
        parts.append(f'<h2 id="how-we-compared">How We Compared Them</h2>{spec["methodology"]}')
    parts.append("</div>")
    return "\n".join(parts)


def jsonld(spec, today):
    url = f"{SITE}/{spec['slug']}"
    plain = lambda s: re.sub(r"<[^>]+>", "", s)
    g = [
        {"@type": "Article", "@id": url + "#article", "headline": spec["h1"], "description": spec["meta_description"],
         "image": SITE + spec["items"][0]["photos"][0], "datePublished": spec.get("date_published", today), "dateModified": today,
         "mainEntityOfPage": url, "inLanguage": "en",
         "author": {"@type": "Person", "name": AUTHOR["name"], "url": SITE + AUTHOR["url"], "jobTitle": "Founder"},
         "publisher": {"@type": "Organization", "name": "Budapest Adventures", "url": SITE,
                       "logo": {"@type": "ImageObject", "url": SITE + "/assets/budapest-adventures-logo.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": spec["breadcrumb"], "item": url}]},
        {"@type": "ItemList", "name": spec["h1"], "numberOfItems": len(spec["items"]), "itemListElement": [
            {"@type": "ListItem", "position": n, "name": it["title"], "url": f"{url}#{it['anchor']}"}
            for n, it in enumerate(spec["items"], 1)]},
    ]
    if spec.get("faqs"):
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": plain(f["a"])}} for f in spec["faqs"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ build
def build(spec_path, photos):
    spec = json.loads(Path(spec_path).read_text())
    slug = spec["slug"]
    if photos:
        fetch_photos(spec, slug)
        Path(spec_path).write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    today = dt.date.today().isoformat()
    today_h = dt.date.today().strftime("%b %-d, %Y")
    for n, it in enumerate(spec["items"], 1):
        it.setdefault("anchor", f"item-{n}-" + re.sub(r"[^a-z0-9]+", "-", it["short_title"].lower()).strip("-")[:40])
        if it.get("platform") == "tiqets":
            if "partner=" not in it["link"]:
                it["link"] = tiqets_link(it["link"], spec.get("cmp", slug))
        elif not it["link"].startswith("http") or "partner_id" not in it["link"]:
            it["link"] = gyg_link(it["link"], spec.get("cmp", slug))
    import day_trips_shell  # frozen pre-listicle shell
    raw = day_trips_shell.read()
    s = BeautifulSoup(raw, "html.parser")
    gyg_icon = s.select_one('img.bpa-rev-icon[alt="GetYourGuide"]')["src"]
    for it in spec["items"]:
        tq = it.get("platform") == "tiqets"
        it["_pname"] = "Tiqets" if tq else "GetYourGuide"
        it["_picon"] = TIQETS_ICON if tq else gyg_icon
    url = f"{SITE}/{slug}"

    # head
    s.title.string = spec["title_tag"]
    for sel, val in [('meta[name="description"]', spec["meta_description"]), ('meta[property="og:title"]', spec["title_tag"]),
                     ('meta[property="og:description"]', spec["meta_description"]), ('meta[name="twitter:title"]', spec["title_tag"]),
                     ('meta[name="twitter:description"]', spec["meta_description"]), ('meta[property="og:url"]', url),
                     ('meta[property="og:image"]', SITE + spec["items"][0]["photos"][0]),
                     ('meta[name="twitter:image"]', SITE + spec["items"][0]["photos"][0])]:
        t = s.select_one(sel)
        if t:
            t["content"] = val
    s.select_one('link[rel="canonical"]')["href"] = url
    for l in s.select('link[rel="preload"][as="image"]'):
        l.decompose()
    for l in s.select('link[rel="alternate"][hreflang]'):
        l.decompose()  # new pages are EN-only until translated
    md = s.select_one('link[rel="alternate"][type="text/markdown"]')
    if md:
        md.decompose()

    # hero
    filters = [{"cat": "all", "label": spec["filter_all_label"]}] + spec["filters"]
    btns = []
    for f in filters:
        cnt = len(spec["items"]) if f["cat"] == "all" else sum(f["cat"] in it["cat"].split() for it in spec["items"])
        act = " active" if f["cat"] == "all" else ""
        # the filter runtime only treats grouped buttons as filters; ungrouped ones
        # behave like "All" and would all render active
        grp = "" if f["cat"] == "all" else f' data-group="{f.get("group", "fit")}"'
        btns.append(f'<button class="ltt-tab-btn{act}" data-cat="{f["cat"]}"{grp} data-label="{esc_attr(f["label"])}" onclick="lttFilterItems(\'{f["cat"]}\', this)" type="button">{E(f["label"])} <span class="ltt-cnt">({cnt})</span></button>')
    lead = "".join(f"<p>{p}</p>" for p in spec["lead"])
    hero = f'''<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs"><a href="/">Home</a><span class="ltt-bc-sep">›</span><span class="ltt-bc-current">{E(spec["breadcrumb"])}</span></nav>
<span class="ltt-hero-kicker-badge">{E(spec["kicker_badge"])}</span>
</div>
<h1 class="ltt-editorial-h1">{E(spec["h1_main"])} <span class="ltt-h1-muted">{E(spec["h1_muted"])}</span></h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap"><img alt="{AUTHOR["name"]}" class="ltt-author-avatar" height="42" loading="eager" src="{AUTHOR["avatar"]}" width="42"/></div>
<div class="ltt-author-meta">
<div class="ltt-author-line">By <a href="{AUTHOR["url"]}">{AUTHOR["name"]}</a>, Founder &amp; Budapest Local</div>
<div class="ltt-author-role">{E(spec["author_role"])}</div>
</div>
</div>
<div class="ltt-trust-pills"><span class="ltt-trust-pill paragraph-26"><strong>Last updated</strong>: {today_h}</span></div>
</div>
<div class="ltt-lead-copy">{lead}</div>
<div class="ltt-integrated-filter-bar">
<span class="ltt-filter-label">Filters:</span>
<div class="ltt-integrated-pills">{"".join(btns)}</div>
</div>
</div>
</div>'''
    s.select_one(".ltt-hero-wrap").replace_with(BeautifulSoup(hero, "html.parser"))

    # deck
    deck = s.select_one("#ltt-cards-deck")
    deck.clear()
    deck.append(BeautifulSoup("\n".join(card_html(n, it, gyg_icon) for n, it in enumerate(spec["items"], 1)), "html.parser"))

    # reviews + guide
    cont = s.select_one("#content .container-33")
    n_items = len(spec["items"])
    cont.clear()
    cont.append(BeautifulSoup(
        '<div class="w-richtext"><p><strong>Disclaimer:</strong> If you find an option that suits you, you can book it through the affiliate links in this article. '
        'They don\'t add any cost to you, but I may earn a small commission, which keeps this guide free and up to date.</p></div>'
        f'<div class="bpa-breakdown-top-bar" id="breakdown-header"><div><h2 class="bpa-breakdown-heading" id="breakdown">{E(spec["breakdown_title"])}</h2>'
        '<p class="bpa-breakdown-sub">All reviews open by default • Click to collapse/expand</p></div><div class="bpa-acc-controls">'
        '<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(true)" type="button">Expand All</button>'
        '<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(false)" type="button">Collapse All</button></div></div>'
        + "\n".join(details_html(n, it, gyg_icon) for n, it in enumerate(spec["items"], 1))
        + guide_html(spec), "html.parser"))
    sf = s.select_one("#Standard-Features")
    if sf:
        sf.decompose()

    # sticky bar + sheet + runtime config
    it1 = spec["items"][0]
    s.select_one("#hybridTocBtn span").string = f"All {n_items} {spec['things']}"
    s.select_one("#sticky-rank").string = "#1 PICK"
    s.select_one("#sticky-name").string = it1["short_title"]
    s.select_one("#sticky-price").string = f"From {money(it1['price'])}"
    cta = s.select_one("#sticky-cta-btn")
    cta["href"] = it1["link"]
    hb = s.select_one("#hybridStickyBar")
    if hb:
        hb.select_one(".hybrid-toc-btn span").string = f"Contents ({n_items})"
        hb.select_one("#hybridActiveTitle").string = it1["short_title"]
        hb.select_one("#hybridActivePrice").string = f"From {money(it1['price'])}"
        hb.select_one("#hybridActiveCta")["href"] = it1["link"]
    s.select_one(".hybrid-sheet-title").string = f"Jump to {spec['sheet_label']}"
    s.select_one("#hybridSheet")["aria-label"] = f"Jump to {spec['sheet_label']}"
    s.select_one("#sticky-bar")["aria-label"] = "Quick navigation and booking"
    for sc in s.find_all("script"):
        if sc.string and "window.LTT_PAGE_CONFIG =" in sc.string:
            cfg = {"deckId": "budapest-day-trips-deck", "tocDeckLabel": f"Top {n_items} Comparison",
                   "tocBreakdownLabel": f"Detailed Breakdown ({n_items})", "shortTitles": [it["short_title"] for it in spec["items"]]}
            sc.string = "\nwindow.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";\n"
    s.select_one("#ltt-schema-jsonld").string = jsonld(spec, today)

    for a in s.select(".w--current"):
        a["class"] = [c for c in a.get("class", []) if c != "w--current"]
    out = ROOT / f"{slug}.html"
    txt = str(s)
    chk = BeautifulSoup(txt, "html.parser").select_one("main") or BeautifulSoup(txt, "html.parser").body
    for t in chk.find_all(["style", "script", "section"]):
        t.decompose()
    leftovers = sorted(set(re.findall(r"(?i)\b(MazakEV|13 day trips|day-trips-2026|Visegrád Castle ticket)\b", chk.get_text(" "))))
    if out.exists() and 'href="/css/listicle-cards.css' in out.read_text(encoding="utf-8"):
        # This page is on the shared listicle design now: its cards come from data/listicles/<slug>.json
        # (scripts/listicle.py build); rebuilding it here would undo that. Edit the card data instead.
        raise SystemExit(f"{out.name} is built from data/listicles/; edit the card data instead")
    out.write_text(txt, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(txt)//1024} KB, {n_items} items)")
    if leftovers and not spec.get("allow_shell_words"):
        print("  ! shell words left in <main>:", leftovers)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="+")
    ap.add_argument("--photos", action="store_true")
    a = ap.parse_args()
    for sp in a.spec:
        build(sp, a.photos)
