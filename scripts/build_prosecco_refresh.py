# -*- coding: utf-8 -*-
"""Rebuild the deck, breakdown, filters, hero copy and JSON-LD of the
unlimited prosecco cruises page from scripts/prosecco_refresh_data.py.

Usage: python3 scripts/build_prosecco_refresh.py <lang> <html-path>
Copy for <lang> comes from scripts/prosecco_refresh_<lang>.py
(UI, PAGE, CARD_<LANG>). Markup and classes mirror
best-budapest-river-cruises.html (the reference page).
"""
import importlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from prosecco_refresh_data import CARDS, CAL_DATE, gyg, viator  # noqa: E402

REF = open(os.path.join(ROOT, "best-budapest-river-cruises.html"), encoding="utf-8").read()


def _icon(alt):
    m = re.search(r'<img alt="%s" class="bpa-rev-icon" loading="lazy" src="(data:image[^"]+)"' % alt, REF)
    return m.group(1)


ICON = {"GetYourGuide": _icon("GetYourGuide"), "Viator": _icon("Viator")}
STAR = re.search(r'(<svg aria-hidden="true" viewbox="0 0 24 24"><path d="M11\.9999[^"]+"></path></svg>)', REF).group(1)
PH = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 500'%3E%3C/svg%3E"
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"


def kfmt(n):
    """Never round up: 51318 -> 51.3k+, 1777 -> 1.7k+, 920 -> 920+ (floor)."""
    if n >= 1000:
        v = int(n / 100) / 10
        return (f"{v:.1f}".rstrip("0").rstrip(".")) + "k+"
    return f"{(n // 10) * 10}+" if n >= 100 else f"{n}"


def weighted(sites):
    tot = sum(s[2] for s in sites)
    return sum(s[1] * s[2] for s in sites) / tot, tot


def esc_attr(t):
    return re.sub(r"<[^>]+>", "", t).replace('"', "&quot;")


class Builder:
    def __init__(self, lang):
        self.lang = lang
        mod = importlib.import_module(f"prosecco_refresh_{lang}")
        self.UI, self.PAGE, self.T = mod.UI, mod.PAGE, getattr(mod, f"CARD_{lang.upper()}")
        self.price_fmt = getattr(mod, "price_fmt", lambda p: p)

    # ------------------------------------------------------------ helpers
    def link(self, c, placement):
        return gyg(c["gyg_path"], self.lang, placement, c["slug"])

    def site_url(self, c, s):
        if s[3] == "gyg":
            return self.link(c, "rating")
        return viator(s[3].split(":", 1)[1], self.lang, c["slug"])

    def site_name(self, s):
        return self.UI["viator_label"] if s[0] == "Viator" else s[0]

    def rating_block(self, c):
        U = self.UI
        avg, tot = weighted(c["sites"])
        n = len(c["sites"])
        meta = (U["reviews_sites"] if n > 1 else U["reviews_site"]).format(count=kfmt(tot), n=n)
        head = U["rate_head"].format(n=n) if n > 1 else U["rate_head_1"]
        badges = "".join(
            f'<a class="bpa-rev-badge is-link" href="{self.site_url(c, s).replace("&", "&amp;")}" rel="noopener nofollow sponsored" target="_blank">'
            f'<img alt="{s[0]}" class="bpa-rev-icon" loading="lazy" src="{ICON[s[0]]}"/><span class="bpa-rev-site">{self.site_name(s)}</span>'
            f'<span class="bpa-rev-score">{s[1]:.1f}</span><span class="bpa-rev-count">({kfmt(s[2])})</span><span class="bpa-rev-go" aria-hidden="true">→</span></a>'
            for s in c["sites"])
        return (f'<div class="bpa-summary-reviews bpa-rate"><details class="bpa-lang bpa-rate-more"><summary class="bpa-rate-sum">'
                f'<span class="bpa-stars" style="--r:{avg:.2f}" aria-hidden="true"></span><b class="bpa-rate-score">{avg:.1f}</b>'
                f'<span class="bpa-rate-meta">{meta}</span><span class="bpa-lang-chev" aria-hidden="true">▾</span></summary>'
                f'<div class="bpa-lang-pop"><strong>{head}</strong><span class="bpa-rate-list">{badges}</span></div></details></div>')

    def static_badges(self, c):
        out = []
        for s in c["sites"]:
            full = int(round(s[1]))
            out.append(f'<span class="bpa-rev-badge"><img alt="" class="bpa-rev-icon" loading="lazy" src="{ICON[s[0]]}"/>'
                       f'<span class="bpa-rev-score">{s[1]:.1f}</span><span class="bpa-rev-stars">{STAR * full}</span>'
                       f'<span class="bpa-rev-count">({kfmt(s[2])})</span></span>')
        return f'<div class="bpa-summary-reviews"><div class="div-block-53">{"".join(out)}</div></div>'

    def pill(self, c, p):
        emoji, label, body, kind = p
        cls = "bpa-lang bpa-time" if kind == "time" else "bpa-lang"
        note = f'<span class="bpa-lang-note">{self.UI["time_note"].format(date=self.UI.get("cal_date", CAL_DATE))}</span>' if kind == "time" else ""
        return (f'<details class="{cls}"><summary class="bpa-sp">{emoji} <span class="bpa-lang-label">{label}</span>'
                f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop">{body}{note}</div></details>')

    def tested_pill(self, c):
        U = self.UI
        return (f'<details class="bpa-lang bpa-tested bpa-proof-mobile"><summary class="bpa-vchip bpa-proof-mobile">{U["tested_chip"]}'
                f'<span class="bpa-lang-chev" aria-hidden="true">▾</span></summary><div class="bpa-lang-pop"><strong>{U["tested_pop_strong"]}</strong> '
                f'{U["tested_pop"]}<span class="bpa-lang-note">{U["tested_note"]} <a href="#{c["anchor"]}">{U["full_review"]}</a></span></div></details>')

    def price(self, c):
        return f'{self.UI["from"]} {self.price_fmt(c["price_label"])}'

    # ------------------------------------------------------------ deck card
    def card(self, i, c):
        U, T = self.UI, self.T[c["slug"]]
        alt = esc_attr(T["title"])
        imgs = []
        for k, ph in enumerate(c["photos"]):
            if k == 0:
                imgs.append(f'<img alt="{alt}" height="534" loading="lazy" sizes="{SIZES}" src="{ph}" width="800"/>')
            else:
                imgs.append(f'<img alt="{alt}" data-src="{ph}" decoding="async" loading="lazy" sizes="{SIZES}" src="{PH}"/>')
        proof = f'<div class="bpa-proof"><span class="bpa-vchip">{U["tested_chip"]}</span></div>\n' if c["tested"] else ""
        pills = (self.tested_pill(c) + "\n" if c["tested"] else "") + "\n".join(self.pill(c, p) for p in T["pills"])
        trust = "".join(f"<span>{t}</span>" for t in T["trust"])
        return f'''<!-- #{i}: {re.sub(r"<[^>]+>", "", T["title"])} -->
<div class="bpa-card" data-cat="{c["cats"]}" id="card-{i}">
<div class="bpa-main">
<div class="bpa-media">
<span class="bpa-rank-tag {c["rank_color"]}">{c["rank_emoji"]} {T["role"]}</span>
<button aria-label="Previous photo" class="bpa-arrow prev" onclick="bpaSlide(this,-1)" type="button">‹</button><button aria-label="Next photo" class="bpa-arrow next" onclick="bpaSlide(this,1)" type="button">›</button><span class="bpa-pill">1 / {len(c["photos"])}</span><div aria-label="Photo gallery {i}" class="bpa-slider" onscroll="bpaCount(this)" tabindex="0">{"".join(imgs)}</div>
</div>
<div class="bpa-info">
<div class="bpa-kicker">{c["operator"]} • ⏱️ {T["dur"]} • <a class="bpa-kicker-map-link" href="{c["pier_maps"]}" rel="nofollow noopener" target="_blank">{T["pier"]}</a></div>
<a class="bpa-title" href="{self.link(c, "card-title").replace("&", "&amp;")}" rel="noopener" target="_blank">{T["title"]}</a>
<div class="bpa-reviews-line">
{self.rating_block(c)}
{proof}</div>
<div class="bpa-specs-row">
{pills}
</div>
<div class="bpa-best-for bpa-pickskip"><span class="bpa-pick">{U["pick"]}</span> {T["pick"]} <span class="bpa-skip">{U["skip"]}</span> {T["skip"]}</div>
</div>
<div class="bpa-cta-cell">
<div>
<div class="bpa-price">{self.price(c)}</div>
<div class="bpa-psub">{U["per_adult"]}</div>
</div>
<a class="bpa-btn" href="{self.link(c, "card-button").replace("&", "&amp;")}" rel="noopener" target="_blank">{U["check"]}</a>
<div class="bpa-via">{U["via_gyg"]}</div>
<div class="bpa-trust2">{trust}</div>
<a class="bpa-sublink" href="#{c["anchor"]}">{U["read_review"]}</a>
</div>
</div>
</div>
'''

    # ------------------------------------------------------------ breakdown
    def ul(self, items):
        return '<ul role="list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

    def sp_cards(self, c, secs, with_img=True):
        out = []
        for sec in secs:
            if len(sec) == 3:
                h, idx, bullets = sec
            else:
                (h, bullets), idx = sec, None
            img = ""
            if with_img and idx:
                img = f'<img alt="{esc_attr(h)}: {esc_attr(self.T[c["slug"]]["title"])}" loading="lazy" src="{c["photos"][idx - 1]}"/>'
            out.append(f'<div class="ltt-sp-card"><h4>{h}</h4>{img}{self.ul(bullets)}</div>')
        return "\n".join(out)

    def bento(self, title, pill, body):
        return f'''<details class="ltt-bento-group" open="">
<summary class="ltt-bento-group-head">
<span class="ltt-bento-group-title">{title}</span>
<span class="ltt-bento-right">
<span class="ltt-mini-pill">{pill}</span>
<span class="ltt-bento-chev">▾</span>
</span>
</summary>
<div class="ltt-bento-group-body">
{body}
</div>
</details>'''

    def details(self, i, c):
        U, T = self.UI, self.T[c["slug"]]
        pros = "".join(f"<li><strong>{a}</strong>: {b}</li>" for a, b in T["pros"])
        cons = "".join(f"<li><strong>{a}</strong>: {b}</li>" for a, b in T["cons"])
        q, a = T["faq"]
        summary = "".join(f"<p>{p}</p>" for p in T["summary"])
        if not c["tested"]:
            summary = f'<p><em>{U["research_note"]}</em></p>' + summary
        quotes = "<br/>".join(f'💬 “{t}” <em>({who}, {site}, {month})</em>' for t, who, site, month in T["quotes"])
        video = f'<blockquote>{T["video"]}</blockquote>' if T.get("video") else ""
        fill = {"pier": c["pier_maps"], "maps_ak3": CARDS[4]["pier_maps"],
                "maps_vig": "https://www.google.com/maps/search/?api=1&query=Vigad%C3%B3+8%2FA+ponton+Budapest"}
        howto = self.ul([h.format(**fill) for h in T["howto"]])
        proof = f'<div class="bpa-proof"><span class="bpa-vchip">{U["tested_chip"]}</span></div>\n' if c["tested"] else ""
        buy = f'''<div class="ltt-buy-card">
<div class="ltt-buy-card-head">
<div class="ltt-buy-card-badge">
<span class="ltt-live-dot"></span>
<span>{U["buy_badge"]}</span>
</div>
<div class="ltt-buy-card-price">
<span class="ltt-buy-price-val">{self.price(c)}</span>
<span class="ltt-buy-price-sub">{U["per_adult"]}</span>
</div>
</div>
<div class="ltt-buy-card-body">
<div class="ltt-buy-card-info">
<h4 class="ltt-buy-card-title">{T["short"]}</h4>
<div class="ltt-buy-card-perks">
<span class="ltt-buy-perk">{U["perk_voucher"]}</span>
<span class="ltt-buy-perk">{U["perk_refund"]}</span>
<span class="ltt-buy-perk">{U["perk_departure"]}: <strong>{T["perk_dep"]}</strong></span>
<span class="ltt-buy-perk">{U["perk_duration"]}: <strong>{T["perk_dur"]}</strong></span>
</div>
</div>
<div class="ltt-buy-card-action">
<a class="ltt-buy-cta-btn" href="{self.link(c, "review-button").replace("&", "&amp;")}" rel="noopener nofollow sponsored" target="_blank">
<span>{U["buy_cta"]}</span>
<span class="ltt-cta-arrow">→</span>
</a>
<div class="ltt-buy-card-trust">
<svg fill="none" height="12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" viewbox="0 0 24 24" width="12"><rect height="11" rx="2" ry="2" width="18" x="3" y="11"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
<span>{U["buy_trust"]}</span>
</div>
</div>
</div>
</div>'''
        sum_body = (f'<div class="w-richtext"><blockquote><strong>❓ {q}</strong><br/>💡 {a}</blockquote>{summary}'
                    f'<blockquote><strong>{U["quotes_head"]}</strong><br/>{quotes}</blockquote>{video}'
                    f'<h3>{U["how_to"]}</h3>{howto}</div>\n{buy}')
        qf_rows = "\n".join(f'<div class="qf1-row"><div class="qf1-label">{U[k]}</div><div class="qf1-val">{v}</div></div>' for k, v in T["qf"])
        chips = "\n".join(f'<span class="qf1-chip {yn}">{"✓" if yn == "yes" else "✕"} {t}</span>' for yn, t in T["chips"])
        return f'''<details class="bpa-details-card" data-cat="{c["cats"]}" id="{c["anchor"]}" open="">
<summary class="bpa-details-summary">
<div class="bpa-details-summary-content">
<div class="bpa-details-top-row">
<span class="bpa-rank-tag {c["rank_color"]}">{c["rank_emoji"]} {T["role"]}</span>
<div class="bpa-kicker">{c["operator"]} • ⏱️ {T["dur"]} • <a class="bpa-kicker-map-link" href="{c["pier_maps"]}" rel="nofollow noopener" target="_blank">{T["pier"]}</a></div>
</div>
<h3 class="bpa-details-title">{T["title"]}</h3>
<div class="bpa-reviews-line">
{self.static_badges(c)}
{proof}</div>
</div>
<div class="bpa-details-right">
<span class="bpa-details-price">{self.price(c)}</span>
<div class="bpa-details-toggle">
<span class="bpa-details-state-text"></span>
<span class="bpa-details-chevron">▾</span>
</div>
</div>
</summary>
<div class="bpa-details-body">
<div class="pro-con-box-wrapper"><div class="w-layout-grid grid-15"><div class="pro-con-box-pro-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-pro-cell-rich-text-block w-richtext"><h3><strong>{U["pros"]}</strong></h3><ul role="list">{pros}</ul></div></div><div class="pro-con-box-con-cell" data-wf-pbl="layout-grid-1x2-vertical"><div class="pro-con-box-con-cell-rich-text-block w-richtext"><h3><strong>{U["cons"]}</strong></h3><ul role="list">{cons}</ul></div></div></div></div>
{self.bento(U["summary_title"], U["summary_pill"], sum_body)}
{self.bento(U["onboard_title"], U["onboard_pill"], '<div class="ltt-sub-points">' + chr(10) + self.sp_cards(c, T["sections"]) + chr(10) + '</div>')}
{self.bento(U["operator_title"], U["operator_pill"], '<div class="ltt-sub-points">' + chr(10) + self.sp_cards(c, T["operator"], False) + chr(10) + '</div>')}
<div class="qf1-wrap">
<div class="qf1-title-row">
<h4 class="qf1-title">{U["qf_title"]}</h4>
<span class="qf1-badge">{T["qf_badge"]}</span>
</div>
<div class="qf1-table">
{qf_rows}
</div>
<div class="qf1-Validation-pills">
{chips}
</div>
</div>
</div>
</details>'''

    # ------------------------------------------------------------ page
    def total_reviews(self):
        return sum(s[2] for c in CARDS for s in c["sites"])

    def schema_itemlist(self, base_url):
        items = []
        for i, c in enumerate(CARDS, 1):
            T = self.T[c["slug"]]
            avg, tot = weighted(c["sites"])
            items.append({"@type": "ListItem", "position": i, "item": {
                "@type": "Product", "name": re.sub(r"<[^>]+>", "", T["title"]).replace("&amp;", "&"),
                "image": "https://www.budapestadventures.com" + c["photos"][0],
                "brand": {"@type": "Brand", "name": c["operator"]},
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": f"{avg:.1f}", "reviewCount": tot, "bestRating": "5"},
                "offers": {"@type": "Offer", "price": c["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock",
                           "url": self.link(c, "schema")}}})
        return {"@type": "ItemList", "@id": base_url + "#itemlist", "name": re.sub(r"<[^>]+>", "", self.PAGE["h1_muted"]),
                "numberOfItems": len(CARDS), "itemListElement": items}

    def build(self, path):
        s = open(path, encoding="utf-8").read()
        P, U = self.PAGE, self.UI
        # deck
        a = s.index('<div class="bpa-deck-wrap" id="ltt-cards-deck">\n') + len('<div class="bpa-deck-wrap" id="ltt-cards-deck">\n')
        b = s.index('\n</div>\n</div>\n</div></div><div class="blog-section-2">', a)
        s = s[:a] + "".join(self.card(i, c) for i, c in enumerate(CARDS, 1)).rstrip("\n") + s[b:]
        # breakdown
        a = s.index('<details class="bpa-details-card"')
        b = s.index('</details>\n</div>\n<style>.ltt-editorial-wrapper', a) + len("</details>")
        s = s[:a] + "".join(self.details(i, c) for i, c in enumerate(CARDS, 1)) + s[b:]
        # breakdown heading
        s = re.sub(r'(<h2 class="bpa-breakdown-heading" id="desert-safaris-breakdown">).*?(</h2>)', lambda m: m.group(1) + P["breakdown_heading"] + m.group(2), s, 1)
        s = re.sub(r'(<p class="bpa-breakdown-sub">).*?(</p>)', lambda m: m.group(1) + P["breakdown_sub"] + m.group(2), s, 1)
        # filters
        F = P["filters"]
        cnt = lambda k: sum(1 for c in CARDS if k in c["cats"].split())
        btns = [("all", F["all"], len(CARDS))] + [(k, F[k], cnt(k)) for k in ("tested", "prosecco", "dinner", "otherdrinks")]
        pills = "\n".join(f'<button class="ltt-tab-btn{" active" if k == "all" else ""}" data-cat="{k}" onclick="lttFilterItems(\'{k}\', this)" type="button">{lab} ({n})</button>' for k, lab, n in btns)
        s = re.sub(r'(<div class="ltt-integrated-pills">\n).*?(\n</div>)', lambda m: m.group(1) + pills + m.group(2), s, 1, flags=re.S)
        s = re.sub(r'(<span class="ltt-filter-label">).*?(</span>)', lambda m: m.group(1) + F["label"] + m.group(2), s, 1)
        # hero
        s = re.sub(r'(<h1 class="ltt-editorial-h1">\s*).*?(\s*<span class="ltt-h1-muted">).*?(</span>)',
                   lambda m: m.group(1) + P["h1_main"] + m.group(2) + P["h1_muted"] + m.group(3), s, 1, flags=re.S)
        s = re.sub(r'(<span class="ltt-hero-kicker-badge">).*?(</span>)', lambda m: m.group(1) + P["kicker_badge"] + m.group(2), s, 1)
        s = re.sub(r'(<div class="ltt-author-role">).*?(</div>)', lambda m: m.group(1) + P["author_role"] + m.group(2), s, 1)
        s = re.sub(r'(<span class="ltt-trust-pill paragraph-26">).*?(</span>)', lambda m: m.group(1) + P["updated"] + m.group(2), s, 1)
        lead = "\n".join(f"<p>{p.format(reviews=f'{self.total_reviews():,}'.replace(',', P.get('thousands', ',')))}</p>" for p in P["lead"])
        s = re.sub(r'(<div class="ltt-lead-copy">\n).*?(\n</div>)', lambda m: m.group(1) + lead + m.group(2), s, 1, flags=re.S)
        s = re.sub(r'(<span class="ltt-bc-current">).*?(</span>)', lambda m: m.group(1) + P["breadcrumb"] + m.group(2), s, 1)
        # head meta
        t, d = P["title"], P["meta"]
        ta = t.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        da = d.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{ta}</title>", s, 1)
        for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            s = re.sub(r'<meta content="[^"]*" %s/>' % re.escape(attr), lambda m: f'<meta content="{da}" {attr}/>', s, 1)
        for attr in ('property="og:title"', 'name="twitter:title"'):
            s = re.sub(r'<meta content="[^"]*" %s/>' % re.escape(attr), lambda m: f'<meta content="{ta}" {attr}/>', s, 1)
        # sticky bar + sheet + config
        c0, T0 = CARDS[0], self.T[CARDS[0]["slug"]]
        s = re.sub(r'(<span id="sticky-name" class="hybrid-active-title">|<span class="hybrid-active-title" id="sticky-name">).*?(</span>)', lambda m: m.group(1) + T0["short"] + m.group(2), s, 1)
        s = re.sub(r'(<span class="hybrid-active-price" id="sticky-price">).*?(</span>)', lambda m: m.group(1) + self.price(c0) + m.group(2), s, 1)
        s = re.sub(r'(<button aria-label="[^"]*" class="hybrid-toc-btn" id="hybridTocBtn" type="button">.*?<span>).*?(</span>)', lambda m: m.group(1) + P["sticky_all"] + m.group(2), s, 1, flags=re.S)
        s = re.sub(r'(<a class="hybrid-cta-btn" href=")[^"]*(" id="sticky-cta-btn")', lambda m: m.group(1) + self.link(c0, "sticky-cta").replace("&", "&amp;") + m.group(2), s, 1)
        s = re.sub(r'(<h3 class="hybrid-sheet-title">).*?(</h3>)', lambda m: m.group(1) + P["sheet_title"] + m.group(2), s, 1)
        s = re.sub(r'(<div aria-label=")[^"]*(" aria-modal="true" class="hybrid-sheet")', lambda m: m.group(1) + esc_attr(P["sheet_title"]) + m.group(2), s, 1)
        m = re.search(r"window\.LTT_PAGE_CONFIG = (\{.*?\});", s)
        cfg = json.loads(m.group(1))
        cfg.update({"tocDeckLabel": P["toc_deck"].replace("&amp;", "&"), "tocBreakdownLabel": P["toc_breakdown"].replace("&amp;", "&"),
                    "shortTitles": [self.T[c["slug"]]["short"].replace("&amp;", "&") for c in CARDS]})
        s = s[:m.start(1)] + json.dumps(cfg, ensure_ascii=False) + s[m.end(1):]
        # JSON-LD
        m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', s, re.S)
        d = json.loads(m.group(2))
        art = d["@graph"][0]
        base = art["url"]
        art["headline"] = t.replace("&amp;", "&")
        art["description"] = P["meta"].replace("&amp;", "&")
        art["dateModified"] = "2026-11-14"
        art["mainEntity"] = {"@id": base + "#itemlist"}
        d["@graph"] = [g for g in d["@graph"] if g.get("@type") != "ItemList"] + [self.schema_itemlist(base)]
        for g in d["@graph"]:
            if g.get("@type") == "BreadcrumbList":
                g["itemListElement"][-1]["name"] = P["breadcrumb"].replace("&amp;", "&")
        s = s[:m.start(2)] + json.dumps(d, ensure_ascii=False) + s[m.end(2):]
        s = re.sub(r'(<div class="ltt-author-line">)(.*?)(</div>)', lambda m: m.group(1) + m.group(2).replace(" — ", ", ").replace("—", ",") + m.group(3), s, 1, flags=re.S)
        # drop legacy Webflow script that stamped "Personally Tested" on every row
        s = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const cruiseCards = document\.querySelectorAll\(\'\.table-row-grey-3.*?</script>', "", s, 1, flags=re.S)
        open(path, "w", encoding="utf-8").write(s)
        return s


if __name__ == "__main__":
    lang, path = sys.argv[1], sys.argv[2]
    Builder(lang).build(path)
    print("built", lang, path)
