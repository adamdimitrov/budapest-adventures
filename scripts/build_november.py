#!/usr/bin/env python3
"""Build "Things to Do in Budapest in November" (EN + HU), 2026-11-15.

Sister page of scripts/build_december.py: same template, components and checks.

Template: best-day-trips-from-budapest.html (head, deck/breakdown CSS and JS,
dropdown pills, star summary, Pick/Skip and the no-red-hover CSS are reused;
hero, deck, guide, breakdown, FAQ, sticky bar and JSON-LD are replaced).
Menu and footer come from scripts/sync_layout.py afterwards.

Facts: scripts/november_data.py. Copy: scripts/november_copy_<lang>.py.
Card photos are reused, in their curated order, from the card of the same
product on another BPA page (PRODUCTS[*]["src"]).

    python3 scripts/build_november.py          # en + hu
    python3 scripts/build_november.py en
"""
import hashlib
from legenda_links import localize as localize_legenda
import html as H
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from november_data import CLIMATE, PRODUCTS, SITE_NAME, SUN  # noqa: E402

SITE = "https://www.budapestadventures.com"
TEMPLATE = ROOT / "best-day-trips-from-budapest.html"
TPL_SLUG = "best-day-trips-from-budapest"
ISO = "2026-11-15"
OUT = {"en": ROOT / "things-to-do-budapest-november.html",
       "hu": ROOT / "hu/budapest-programok-november/index.html"}
ALT = {"en": "/things-to-do-budapest-november", "hu": "/hu/budapest-programok-november"}
BLANK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
SIZES = 'sizes="(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"'
NUM = {"en": lambda n: f"{n:,}", "hu": lambda n: f"{n:,}".replace(",", " ")}


def icons():
    src = (ROOT / "best-dinner-cruises-budapest.html").read_text() + (ROOT / "thermal-baths-budapest.html").read_text()
    out = {}
    for k, name in SITE_NAME.items():
        m = re.search(r'<img alt="%s" class="bpa-rev-icon" loading="lazy" src="([^"]+)"' % name, src)
        out[k] = m.group(1)
    return out


ICON = icons()


def card_photos(page, needle, n):
    s = (ROOT / page).read_text()
    for c in re.findall(r'(<div class="bpa-card".*?<div class="bpa-cta-cell">)', s, re.S):
        if needle in c:
            media = c[:c.find('<div class="bpa-info">')]
            ph = [m.group(1) or m.group(2) for m in re.finditer(
                r'<img alt="[^"]*"[^>]*?(?:data-src="([^"]+)"[^>]*src="data|src="(/assets/[^"]+)")', media)]
            ph = [p for p in ph if p]
            for p in ph:
                assert (ROOT / H.unescape(p).lstrip("/").replace("%20", " ")).exists() or (ROOT / p.lstrip("/")).exists(), p
            return ph[:n]
    raise SystemExit(f"no card with {needle} on {page}")


def short_count(n, lang):
    if n >= 1000:
        v = f"{n / 1000:.1f}".rstrip("0").rstrip(".")
        if lang == "hu":
            v = v.replace(".", ",")
        return f"{v}k+" if lang == "en" else f"{v}e+"
    return str(n)


def fmt_score(x, lang):
    v = f"{x:.1f}"
    return v.replace(".", ",") if lang == "hu" else v


def price_txt(p, lang, ui):
    v = f"{p:g}" if p != int(p) else str(int(p))
    if lang == "hu":
        v = v.replace(".", ",")
    return ui["from_price"].format(p=v)


def rating(p, lang, ui):
    rs = p["ratings"]
    if not rs:
        return (f'<div class="bpa-summary-reviews bpa-rate"><span class="bpa-rate-meta" '
                f'style="font-size:13px;color:#64748b">{ui["no_rating"]}</span></div>')
    n = sum(c for _, _, c, _ in rs)
    avg = sum(r * c for _, r, c, _ in rs) / n
    badges = ""
    for site, score, cnt, link in rs:
        inner = (f'<img alt="{SITE_NAME[site]}" class="bpa-rev-icon" loading="lazy" src="{ICON[site]}"/>'
                 f'<span class="bpa-rev-site">{SITE_NAME[site]}</span><span class="bpa-rev-score">{fmt_score(score, lang)}</span>'
                 f'<span class="bpa-rev-count">({short_count(cnt, lang)})</span>')
        if link and p["via"] == "gyg":
            href = p["href"].replace("cmp=november-", "cmp=november-rating-")
            badges += (f'<a class="bpa-rev-badge is-link" href="{href}" rel="nofollow sponsored noopener" target="_blank">'
                       f'{inner}<span class="bpa-rev-go">→</span></a>')
        else:
            badges += f'<span class="bpa-rev-badge">{inner}</span>'
    k = len(rs)
    meta = (ui["reviews_one"] if k == 1 else ui["reviews_many"]).format(n=short_count(n, lang), k=k)
    head = ui["rating_on"] if k == 1 else ui["rating_many"].format(k=k)
    return (f'<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
            f'<span class="bpa-stars" style="--r:{avg:.2f}" aria-hidden="true"></span><b class="bpa-rate-score">{fmt_score(avg, lang)}</b>'
            f'<span class="bpa-rate-meta">{meta}</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
            f'<div class="bpa-lang-pop"><strong>{head}</strong><span class="bpa-rate-list">{badges}</span></div></details></div>')


def pills(c, p, ui, anchor):
    out = []
    if p["tested"]:
        out.append(f'<details class="bpa-lang bpa-tested"><summary class="bpa-vchip">{ui["tested"]}'
                   f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">{c["tested_pop"]}'
                   f'<span class="bpa-lang-note"><a href="#{anchor}">{ui["read"]}</a></span></div></details>')
    for ic, lab, pop in c["pills"]:
        out.append(f'<details class="bpa-lang"><summary class="bpa-sp">{ic} <span class="bpa-lang-label">{lab}</span>'
                   f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">{pop}</div></details>')
    return "\n".join(out)


def tag(i):
    return {1: "bpa-gold", 2: "bpa-silver", 3: "bpa-bronze"}.get(i, "bpa-slate")


def maps(q):
    return "https://www.google.com/maps/search/?api=1&amp;query=" + q.replace(" ", "+")


def cta(p, ui):
    return ui["check"] if p["via"] == "gyg" else ui["book_site"].format(op=p["op"])


def deck_card(i, p, c, ui, lang):
    alts = [f'{H.escape(c["title"])} ({k}/{len(p["photos"])})' for k in range(1, len(p["photos"]) + 1)]
    first = ('fetchpriority="high" height="534" loading="eager"' if i == 1 else 'height="534" loading="lazy"')
    imgs = [f'<img alt="{alts[0]}" {first} {SIZES} src="{p["photos"][0]}" width="800"/>']
    imgs += [f'<img alt="{a}" data-src="{ph}" decoding="async" loading="lazy" {SIZES} src="{BLANK}"/>'
             for ph, a in zip(p["photos"][1:], alts[1:])]
    place = (f'<a class="bpa-kicker-map-link" href="{maps(c["map"])}" onclick="event.stopPropagation()" '
             f'rel="noopener noreferrer" target="_blank">{c["place"]}</a>')
    trust = (f'<span>{ui["instant"]}</span><span>•</span><span>{ui["cxl24"]}</span>' if p["via"] == "gyg"
             else f'<span>{ui["direct_trust"]}</span>')
    return f"""<!-- #{i}: {c['title']} -->
<div class="bpa-card" data-cat="{p['cats']}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {tag(i)}">{c['rank']}</span>
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button>
<button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button>
<span class="bpa-pill">1 / {len(imgs)}</span>
<div aria-label="Photo gallery {i}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">
{chr(10).join(imgs)}
</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{p['op']} • ⏱️ {c['dur']} • {place}</div>
<a class="bpa-title" href="{p['href']}" rel="nofollow sponsored noopener" target="_blank">{c['title']}</a>
<div class="bpa-reviews-line">
{rating(p, lang, ui)}
</div>
<div class="bpa-specs-row">
{pills(c, p, ui, p['anchor'])}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">{ui['pick']}</span> {c['pick']} <span class="bpa-skip">{ui['skip']}</span> {c['skip']}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{p['price_txt']}</div>
<div class="bpa-psub">{c['psub']}</div>
</div>
<a class="bpa-btn" href="{p['href']}" rel="nofollow sponsored noopener" target="_blank">{cta(p, ui)}</a>
<div class="bpa-trust-micro">
{trust}
</div>
<a class="bpa-sublink" href="#{p['anchor']}">{ui['read']}</a>
</div>
</div>
</div>
"""


def details(i, p, c, ui, lang, lock):
    pros = "".join(f"<li><strong>{x}</strong></li>" for x in c["pros"])
    cons = "".join(f"<li><strong>{x}</strong></li>" for x in c["cons"])
    n = len(p["photos"])
    slides = "".join(
        f'<div class="ltt-strip-slide"><img alt="{H.escape(c["title"])} ({k}/{n})" loading="lazy" src="{ph}"/><div class="ltt-strip-cap">'
        f'<span class="ltt-strip-num">{k} / {n}</span> <span>{H.escape(c["title"])}</span></div></div>'
        for k, ph in enumerate(p["photos"], 1))
    base = [ui["perk_qr"], ui["perk_refund"]] if p["via"] == "gyg" else [ui["perk_direct"]]
    perks = "\n".join(f'<span class="ltt-buy-perk">{x}</span>' for x in base + c["perks"])
    qf = "\n".join(f'<div class="qf1-row"><div class="qf1-label">{a}</div><div class="qf1-val">{b}</div></div>' for a, b in c["qf"])
    chips = "\n".join(f'<span class="qf1-chip {k}">{x}</span>' for k, x in c["chips"])
    return f"""<details class="bpa-details-card" data-cat="{p['cats']}" id="{p['anchor']}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {tag(i)}">{c['rank']}</span>
<div class="bpa-kicker">{p['op']} • ⏱️ {c['dur']} • <span class="bpa-kicker-map-link">{c['place']}</span></div>
</div>
<h3 class="bpa-details-title">{c['title']}</h3>
<div class="bpa-reviews-line">
{rating(p, lang, ui)}
</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">{p['price_txt']}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>{ui['pros']}</strong></h3><ul role="list">{pros}</ul></div></div><div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext"><h3><strong>{ui['cons']}</strong></h3><ul role="list">{cons}</ul></div></div></div></div>
<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">{ui['summary']}</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">{ui['overview']}</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
<div class="w-richtext">{c['body']}<div class="ltt-filmstrip-wrap"><button aria-label="Previous photo" class="ltt-film-btn ltt-film-prev is-disabled" onclick="window.lttFilmSlide(this, -1)" type="button">‹</button><button aria-label="Next photo" class="ltt-film-btn ltt-film-next" onclick="window.lttFilmSlide(this, 1)" type="button">›</button><div aria-label="Filmstrip gallery {i}" class="ltt-filmstrip" onscroll="window.lttFilmSync(this)" tabindex="0">{slides}</div></div></div>
<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>{ui['live']}</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{p['price_txt']}</span>
<span class="ltt-buy-price-sub">{c['psub']}</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{c['title']}</h4>
<div class="ltt-buy-card-perks">
{perks}
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{p['href']}" rel="nofollow sponsored noopener" target="_blank">
<span>{ui['book_dates']}</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
{lock}
<span>{ui['best_price']}</span>
</div>
</div>
</div>
</div>
</div>
</details>
<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">{ui['qf']}</h4>
<span class="qf1-badge">{c['qf_badge']}</span>
</div>
<div class="qf1-table">
{qf}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
</div>
</div>
</details>
"""


from christmas_markets_data import MARKETS  # noqa: E402

PAGE_CSS = """<style id="nov-page-css">
.nov-table{width:100%;border-collapse:collapse;font-size:14.5px;min-width:520px}
.nov-table th,.nov-table td{padding:10px 12px;border-bottom:1px solid #f1f5f9;text-align:left;vertical-align:top;color:#334155}
.nov-table thead th{background:#f8fafc;color:#0f172a;font-weight:700}
.nov-table tbody th{font-weight:700;color:#0f172a}
.nov-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid #e2e8f0;border-radius:12px;background:#fff;margin:14px 0 8px;max-width:100%}
.nov-note{font-size:13.5px !important;color:#64748b !important}
.nov-free li{margin-bottom:10px}
</style>"""


def table(cols, rows):
    head = "".join(f"<th>{h}</th>" for h in cols)
    body = "".join("<tr><th>" + r[0] + "</th>" + "".join(f"<td>{x}</td>" for x in r[1:]) + "</tr>" for r in rows)
    return f'<div class="nov-scroll"><table class="nov-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def section_html(L, lang):
    picks = "".join(f'<li><strong>{lab}:</strong> <a href="{L.A(k)}">{L.C[k]["title"]}</a> ({note}).</li>' for lab, k, note in L.PICKS)
    sun_rows = [(L.DAY(d), a, b, L.DUR(c)) for d, a, b, c in SUN]
    mkt_rows = [(f'{m["name"]}<br/><span class="nov-note">{m["place"]}</span>', L.SPAN(m["start"], m["end"]), L.HOURS(m))
                for m in MARKETS]
    free = "".join(f"<li><strong>{a}.</strong> {b}</li>" for a, b in L.FREE)
    return f"""<h2 id="quick-picks">{L.PICKS_H}</h2>
<ul>{picks}</ul>
<h2 id="november-dates">{L.DATES_H}</h2>
<p>{L.DATES_INTRO}</p>
{table(L.DATES_COLS, L.DATES_ROWS)}
<p class="nov-note">{L.DATES_NOTE}</p>
<h2 id="weather-daylight">{L.SEASON_H}</h2>
<p>{L.SEASON_P}</p>
{table(L.SUN_COLS, sun_rows)}
<p>{L.SEASON_TIP}</p>
<h2 id="christmas-markets-november">{L.XMAS_H}</h2>
<p>{L.XMAS_P}</p>
{table(L.XMAS_COLS, mkt_rows)}
<p>{L.XMAS_LINK}</p>
<h2 id="free-things">{L.FREE_H}</h2>
<ul class="nov-free">{free}</ul>
"""

def build(lang):
    L = importlib.import_module(f"november_copy_{lang}")
    ui = L.UI
    url = SITE + L.PATH
    import day_trips_shell  # frozen pre-listicle shell
    s = day_trips_shell.read()
    lock = re.search(r'<div class="ltt-buy-card-trust">\s*(<svg.*?</svg>)', s, re.S).group(1)

    prods = []
    for i, p in enumerate(PRODUCTS, 1):
        p = dict(p)
        p["photos"] = card_photos(*p["src"], p["n_photos"])
        p["anchor"] = L.ANCHORS[p["key"]]
        p["price_txt"] = price_txt(p["price"], lang, ui)
        prods.append(p)

    # ---- head ----
    old_title = re.search(r"<title>(.*?)</title>", s).group(1)
    old_desc = re.search(r'<meta content="([^"]+)" name="description"/>', s).group(1)
    s = s.replace(f"<title>{old_title}</title>", f"<title>{L.TITLE_TAG}</title>")
    s = s.replace(f'content="{old_title}"', f'content="{L.TITLE_TAG}"').replace(f'content="{old_desc}"', f'content="{L.META}"')
    s = re.sub(r'<link as="image" fetchpriority="high" href="[^"]+" rel="preload" type="image/[a-z]+"/>',
               f'<link as="image" fetchpriority="high" href="{prods[0]["photos"][0]}" rel="preload" type="image/{prods[0]["photos"][0].rsplit(".", 1)[1]}"/>', s, count=1)
    og = re.search(r'<meta content="([^"]+)" property="og:image"/>', s).group(1)
    og_new = SITE + prods[0]["photos"][0]
    s = s.replace(og, og_new)
    s = re.sub(r'<link href="[^"]+" hreflang="[^"]+" rel="alternate"/>\n?', "", s)
    alts = "".join(f'<link href="{SITE}{ALT[lg]}" hreflang="{lg}" rel="alternate"/>\n' for lg in ("en", "hu"))
    alts += f'<link href="{SITE}{ALT["en"]}" hreflang="x-default" rel="alternate"/>\n'
    s = s.replace(f'<link href="{SITE}/{TPL_SLUG}" rel="canonical"/>', alts + f'<link href="{url}" rel="canonical"/>')
    s = s.replace(f'"{SITE}/{TPL_SLUG}"', f'"{url}"')
    s = re.sub(r'<html([^>]*) lang="[a-z-]+"', rf'<html\1 lang="{lang}"', s, count=1)
    if lang != "en":
        s = re.sub(r'<meta content="en_[A-Z]+" property="og:locale"/>', f'<meta content="{L.OG_LOCALE}" property="og:locale"/>', s)

    # ---- own copies of the purged CSS ----
    for href in re.findall(r'href="(/css/purged/%s\.[^"]+\.css)"' % TPL_SLUG, s):
        css = (ROOT / href.lstrip("/")).read_text()
        base = href.split(TPL_SLUG + ".")[1].rsplit(".", 2)[0]
        new = f"/css/purged/{L.SLUG_CSS}.{base}.{hashlib.sha1(css.encode()).hexdigest()[:10]}.css"
        for old_f in (ROOT / "css/purged").glob(f"{L.SLUG_CSS}.{base}.*.css"):
            old_f.unlink()
        (ROOT / new.lstrip("/")).write_text(css)
        s = s.replace(href, new)
    s = s.replace("</head>", PAGE_CSS + "</head>", 1)

    # ---- hero ----
    filters = "".join(
        f'<button class="ltt-tab-btn" data-cat="{k}" data-group="type" data-label="{lab}" onclick="lttFilterItems(\'{k}\', this)" type="button">{lab} <span class="ltt-cnt"></span></button>\n'
        for k, lab in ui["filters"])
    hero = f"""<div class="ltt-hero-wrap">
<div class="ltt-clean-card">
<div class="ltt-top-bar">
<nav aria-label="Breadcrumb" class="ltt-breadcrumbs">
<a href="{'/' if lang == 'en' else '/hu'}">{ui['home']}</a>
<span class="ltt-bc-sep">›</span>
<span class="ltt-bc-current">{L.CRUMB}</span>
</nav>
<span class="ltt-hero-kicker-badge">{L.KICKER}</span>
</div>
<h1 class="ltt-editorial-h1">
      {L.H1} <span class="ltt-h1-muted">{L.H1_MUTED}</span>
</h1>
<div class="ltt-trust-bar">
<div class="ltt-author-cluster">
<div class="ltt-author-avatar-wrap">
<img alt="Adam Dimitrov" class="ltt-author-avatar" height="42" loading="eager" src="/assets/adam-dimitrov.webp" width="42"/>
</div>
<div class="ltt-author-meta">
<div class="ltt-author-line">
            {ui['by']} <a href="{'/about' if lang == 'en' else '/hu/rolunk'}" target="_blank">Adam Dimitrov</a>, {ui['founder']}
          </div>
<div class="ltt-author-role">{L.AUTHOR_ROLE}</div>
</div>
</div>
<div class="ltt-trust-pills">
<span class="ltt-trust-pill paragraph-26"><strong>{L.UPDATED}</strong>: {L.UPDATED_DATE}</span>
</div>
</div>
<div class="ltt-lead-copy">
{L.LEAD}
</div>
<div class="ltt-integrated-filter-bar smart-filter-bar">
<div class="ltt-integrated-pills">
<button class="ltt-tab-btn active" data-cat="all" data-label="{ui['filter_all']}" onclick="lttFilterItems('all', this)" type="button">{ui['filter_all']} <span class="ltt-cnt"></span></button>
<span class="ltt-filter-label sf-fl">{ui['filter_label']}</span>
{filters}</div>
</div>
</div>
</div>"""
    a = s.index('<div class="ltt-hero-wrap">')
    b = s.index('<div class="comparison-table">', a)
    s = s[:a] + hero + s[b:]

    # ---- deck ----
    deck_id = "budapest-november-deck"
    s = s.replace('id="budapest-day-trips-deck"', f'id="{deck_id}"')
    a = s.index('<div class="bpa-deck-wrap" id="ltt-cards-deck">') + len('<div class="bpa-deck-wrap" id="ltt-cards-deck">\n')
    b = s.index('</div>\n</div>\n</div></div><div class="blog-section-2">', a)
    s = s[:a] + "".join(deck_card(i, p, L.C[p["key"]], ui, lang) for i, p in enumerate(prods, 1)) + s[b:]

    # ---- guide + breakdown + FAQ ----
    a = s.index('<div class="w-richtext bpa-wt-guide">')
    b = s.index('<style>.ltt-editorial-wrapper', a)
    head = f"""<div class="bpa-breakdown-top-bar" id="breakdown-header">
<div>
<h2 class="bpa-breakdown-heading" id="november-breakdown">{ui['breakdown_h']}</h2>
<p class="bpa-breakdown-sub">{ui['breakdown_sub']}</p>
</div>
<div class="bpa-acc-controls">
<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(true)" type="button">{ui['expand']}</button>
<button class="bpa-acc-ctrl-btn" onclick="toggleAllDetails(false)" type="button">{ui['collapse']}</button>
</div>
</div>
"""
    faq = "".join(f'<h3 class="cf-faq-questions-2">{q}</h3><div class="cf-faq-answer-wrap-2">'
                  f'<div class="cf-faq-content-2 w-richtext"><p>{x}</p></div></div>' for q, x in L.FAQ)
    more = "".join(f"<li><strong>{x}:</strong> {y}</li>" for x, y in L.MORE)
    tail = f"""<div class="w-richtext bpa-wt-faq">
<h2 id="more-november">{L.MORE_H}</h2>
<ul>{more}</ul>
<p>{L.DEC_LINK}</p>
<h2 id="faq">{ui['faq_h']}</h2>{faq}
<h2 id="how-we-chose">{L.METHOD_H}</h2>
<p>{L.METHOD}</p>
</div>"""
    content = ('<div class="w-richtext bpa-wt-guide">\n' + section_html(L, lang) + "\n</div>\n\n" + head
               + "".join(details(i, p, L.C[p["key"]], ui, lang, lock) for i, p in enumerate(prods, 1))
               + tail + "\n</div>\n")
    s = s[:a] + content + s[b:]

    # ---- sticky bar + config ----
    p1, c1 = prods[0], L.C[prods[0]["key"]]
    s = re.sub(r'(<span class="hybrid-active-title" id="sticky-name">).*?(</span>)', lambda m: m.group(1) + c1["title"] + m.group(2), s, count=1)
    s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">).*?(</span>)', lambda m: m.group(1) + p1["price_txt"] + m.group(2), s, count=1)
    s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]+(")', lambda m: m.group(1) + p1["href"] + m.group(2), s)
    s = re.sub(r'(<span class="hybrid-active-title" id="hybridActiveTitle">).*?(</span>)', lambda m: m.group(1) + "Legenda" + m.group(2), s, count=1)
    s = re.sub(r'(<span class="hybrid-active-price" id="hybridActivePrice">).*?(</span>)', lambda m: m.group(1) + p1["price_txt"] + m.group(2), s, count=1)
    s = s.replace("<span>Contents (13)</span>", f"<span>{ui['contents']}</span>")
    s = s.replace("<span>All 13 Day Trips</span>", f"<span>{ui['all_items']}</span>")
    s = s.replace("Jump to a Day Trip", ui["jump"])
    cfg = {"deckId": deck_id, "tocDeckLabel": ui["toc_deck"], "tocBreakdownLabel": ui["toc_breakdown"],
           "shortTitles": [L.C[p["key"]]["title"] for p in prods]}
    s = re.sub(r"window\.LTT_PAGE_CONFIG = \{.*?\};", lambda m: "window.LTT_PAGE_CONFIG = " + json.dumps(cfg, ensure_ascii=False) + ";", s, count=1, flags=re.S)
    if lang != "en":
        for a_, b_ in L.TEMPLATE_STRINGS:
            s = s.replace(a_, b_)

    # ---- JSON-LD ----
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    old = json.loads(m.group(2))
    art = next(n for n in old["@graph"] if n["@type"] == "Article")
    lead_txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", L.LEAD)).strip()
    items = []
    for i, p in enumerate(prods, 1):
        c = L.C[p["key"]]
        it = {"@type": "Product", "name": c["title"], "description": c["desc"],
              "brand": {"@type": "Organization", "name": p["op"]},
              "image": [SITE + p["photos"][0]],
              "offers": {"@type": "Offer", "price": f'{p["price"]:g}', "priceCurrency": "EUR",
                         "availability": "https://schema.org/InStock", "url": p["href"].replace("&amp;", "&")}}
        if p["ratings"]:
            n = sum(x[2] for x in p["ratings"])
            avg = sum(x[1] * x[2] for x in p["ratings"]) / n
            it["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": f"{avg:.1f}", "bestRating": "5",
                                     "worstRating": "1", "reviewCount": str(n)}
        items.append({"@type": "ListItem", "position": i, "url": f"{url}#{p['anchor']}", "item": it})
    author = dict(art["author"])
    graph = [
        {"@type": "Article", "@id": f"{url}#article", "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "headline": L.H1, "description": L.META, "url": url, "inLanguage": lang,
         "datePublished": ISO, "dateModified": ISO, "author": author, "publisher": art["publisher"], "image": [og_new],
         "mainEntity": {"@type": "ItemList", "name": L.H1, "description": lead_txt, "numberOfItems": len(items), "itemListElement": items}},
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": SITE + ("/" if lang == "en" else "/hu")},
            {"@type": "ListItem", "position": 2, "name": L.CRUMB, "item": url}]},
        {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", x)}} for q, x in L.FAQ]},
    ]
    s = s[:m.start(2)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")) + s[m.end(2):]

    # ---- checks ----
    s = s.replace('rel="noopener nofollow sponsored"', 'rel="nofollow sponsored noopener"')
    assert "—" not in s, "em dash"
    body_only = re.sub(r'<header[^>]*ltt-navbar.*?</header>', "", s, flags=re.S)
    body_only = body_only[:body_only.find('<footer')] if '<footer' in body_only else body_only
    for bad in ("Day Trip", "day-trips-2026", "Danube Bend Forest", "Visegrád Castle above", "MazakEV"):
        hits = [x for x in re.findall(r".{0,60}%s.{0,60}" % re.escape(bad), body_only) if "best-day-trips-from-budapest" not in x]
        assert not hits, (bad, hits[:3])
    s = localize_legenda(s, lang)
    for href in re.findall(r'href="(https://(?:www\.getyourguide|budapestrivercruise|legenda)[^"]+)"', s):
        if "getyourguide" in href:
            assert "mkt_cmp=true" in href and "partner_id=YS414AJ" in href, href
        if "budapestrivercruise" in href:
            assert href.endswith("?code=bpadventures"), href
        if "legenda.hu" in href:
            assert href.endswith("?partner=38585"), href
    for tagm in re.findall(r'<a [^>]*href="https://(?:www\.getyourguide|budapestrivercruise|legenda)[^>]*>', s):
        assert 'rel="nofollow sponsored noopener"' in tagm, tagm
    out = OUT[lang]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    print("wrote", out.relative_to(ROOT), len(s))


if __name__ == "__main__":
    for lg in (sys.argv[1:] or ["en", "hu"]):
        build(lg)
