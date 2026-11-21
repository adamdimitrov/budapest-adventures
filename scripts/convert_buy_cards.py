#!/usr/bin/env python3
"""Replace the old "Official Tickets & Live Availability" box (.ltt-buy-card) with the
bpa-book card (see scripts/snippets/bpa-book-card.html).

Every text in the new card is reused from the page itself, so translated pages keep
their own language:
  kicker  <- the product's rank tag (emoji stripped), else the old badge text
  title   <- old box title, linked to the old booking URL
  rating  <- the product's star summary (.bpa-summary-reviews), cloned with its popover
  bullets <- the old box perks
  price   <- old price + "per adult" line
  button  <- old CTA text + arrow, same booking URL and rel
  note    <- old trust line
  photo   <- first slider photo of the matching deck card (same position in the list),
             else the first /assets photo of the breakdown card, else no photo

Usage: python3 scripts/convert_buy_cards.py FILE [FILE ...] [--dry]
"""
import html
import re
import sys

CSS_ID = "bpa-book-css"
CSS = """<style id="bpa-book-css">
.bpa-book{display:grid !important;grid-template-columns:minmax(0,40%) 1fr;gap:0;margin:16px 0 8px !important;background:#fff !important;border:1px solid #ecdcb6 !important;border-radius:16px !important;overflow:hidden;box-shadow:0 10px 30px -12px rgba(133,90,0,.25) !important;text-align:left;padding:0 !important}
.bpa-book.no-img{grid-template-columns:1fr}
.bpa-book a.bpa-book-img{display:block !important;min-height:100%;background:#f1f5f9;padding:0 !important;margin:0 !important;border:0 !important}
.bpa-book .bpa-book-img img{width:100% !important;height:100% !important;max-width:none !important;object-fit:cover;display:block !important;margin:0 !important;border-radius:0 !important;border:0 !important}
.bpa-book .bpa-book-body{padding:20px 22px;display:flex;flex-direction:column;gap:8px;min-width:0}
.bpa-book .bpa-book-kicker{font-size:11.5px !important;font-weight:800 !important;letter-spacing:.08em;text-transform:uppercase;color:#855a00 !important;margin:0 !important;line-height:1.4}
.bpa-book a.bpa-book-title{font-family:'Playfair Display',Georgia,serif !important;font-size:22px !important;font-weight:700 !important;line-height:1.25 !important;color:#0f172a !important;text-decoration:none !important;background:none !important;padding:0 !important}
.bpa-book a.bpa-book-title:hover{color:#855a00 !important}
.bpa-book .bpa-book-rating{font-size:13.5px;color:#475569}
.bpa-book .bpa-book-rating .bpa-summary-reviews{margin:0 !important;display:inline-block !important;width:auto !important;max-width:100%}
.bpa-book .bpa-book-rating .bpa-rate-sum{justify-content:flex-start !important;width:auto !important;flex-wrap:nowrap !important}
.bpa-book .bpa-book-rating .bpa-rate-meta{min-width:0}
.bpa-book ul.bpa-book-points{margin:2px 0 4px !important;padding:0 !important;list-style:none !important}
.bpa-book ul.bpa-book-points li{position:relative;padding-left:22px !important;margin:0 0 4px !important;font-size:14.5px !important;line-height:1.5 !important;color:#334155 !important;list-style:none !important;background:none !important}
.bpa-book ul.bpa-book-points li::before{content:"\\2713";position:absolute;left:0;top:0;color:#15803d;font-weight:800}
.bpa-book ul.bpa-book-points li::marker{content:""}
.bpa-book .bpa-book-foot{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:auto;padding-top:10px;border-top:1px solid #f1e7cf}
.bpa-book .bpa-book-price{font-size:26px;font-weight:800;color:#0f172a;line-height:1.1}
.bpa-book .bpa-book-price small{display:block;font-size:12px;font-weight:600;color:#64748b;margin-top:2px}
.bpa-book a.bpa-book-btn{display:inline-block !important;background:linear-gradient(135deg,#dfa732 0%,#b88214 100%) !important;color:#fff !important;padding:12px 22px !important;border-radius:9999px !important;font-size:14.5px !important;font-weight:800 !important;text-decoration:none !important;box-shadow:0 4px 14px rgba(223,167,50,.35) !important;transition:all .15s ease;white-space:nowrap;border:0 !important;line-height:1.3 !important}
.bpa-book a.bpa-book-btn:hover{background:linear-gradient(135deg,#ca9325 0%,#855a00 100%) !important;color:#fff !important;transform:translateY(-1px);box-shadow:0 6px 18px rgba(223,167,50,.45) !important}
.bpa-book .bpa-book-note{font-size:11.5px;color:#94a3b8;line-height:1.45}
@media(max-width:640px){
.bpa-book{grid-template-columns:1fr}
.bpa-book a.bpa-book-img{aspect-ratio:16/9;min-height:0}
.bpa-book .bpa-book-body{padding:16px 16px 18px}
.bpa-book a.bpa-book-title{font-size:19px !important}
.bpa-book .bpa-book-rating .bpa-rate-meta{font-size:12.5px !important}
.bpa-book .bpa-book-foot{flex-direction:column;align-items:stretch}
.bpa-book a.bpa-book-btn{text-align:center;white-space:normal}
}
</style>"""

IMG = r'<img\b(?:[^>"]|"[^"]*")*>'
EMOJI = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️]+")


def strip_tags(x):
    return re.sub(r"<[^>]+>", "", x).strip()


def find_div_end(s, start):
    """Index just past the </div> that closes the <div ...> opening at start."""
    depth = 0
    for m in re.compile(r"<div\b|</div>").finditer(s, start):
        if m.group(0) == "</div>":
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    raise ValueError("unbalanced div")


def first_group(pat, x, default=""):
    m = re.search(pat, x, re.S)
    return m.group(1).strip() if m else default


def deck_photos(s):
    """List of (src, alt) per deck card, in order."""
    out = []
    starts = [m.start() for m in re.finditer(r'<div class="bpa-card"', s)]
    for i, c in enumerate(starts):
        seg = s[c: starts[i + 1] if i + 1 < len(starts) else len(s)]
        sl = seg.find('class="bpa-slider"')
        img = None
        if sl >= 0:
            m = re.search(IMG, seg[sl:])
            if m:
                tag = m.group(0)
                src = first_group(r'data-src="(/assets[^"]+)"', tag) or first_group(r'\bsrc="(/assets[^"]+)"', tag)
                if src:
                    img = (src, first_group(r'alt="([^"]*)"', tag))
        out.append(img)
    return out


def container_start(s, pos):
    """Start of the breakdown card (details) holding pos, or -1."""
    return s.rfind('<details class="bpa-details-card"', 0, pos)


def build_card(box, ctx, photo):
    url = first_group(r'class="ltt-buy-cta-btn"[^>]*href="([^"]+)"', box) or first_group(r'href="([^"]+)"[^>]*class="ltt-buy-cta-btn"', box)
    rel = first_group(r'class="ltt-buy-cta-btn"[^>]*rel="([^"]+)"', box) or first_group(r'rel="([^"]+)"[^>]*class="ltt-buy-cta-btn"', box) or "noopener nofollow sponsored"
    badge = strip_tags(first_group(r'class="ltt-buy-card-badge">(.*?)</div>', box))
    title = first_group(r'class="ltt-buy-card-title">(.*?)</h4>', box)
    price = first_group(r'class="ltt-buy-price-val">(.*?)</span>', box)
    sub = first_group(r'class="ltt-buy-price-sub">(.*?)</span>', box)
    perks = re.findall(r'<span class="ltt-buy-perk">(.*?)</span>\s*(?=<span class="ltt-buy-perk">|</div>)', box, re.S)
    cta = strip_tags(first_group(r'class="ltt-buy-cta-btn"[^>]*>(.*?)</a>', box)).replace("→", "").strip()
    trust = strip_tags(first_group(r'class="ltt-buy-card-trust">(.*?)</div>', box))
    rank = EMOJI.sub("", strip_tags(first_group(r'<span class="bpa-rank-tag[^"]*">(.*?)</span>', ctx))).strip() if ctx else ""
    kicker = rank or badge
    rating = ""
    if ctx:
        i = ctx.find('<div class="bpa-summary-reviews')
        if i >= 0:
            rating = ctx[i:find_div_end(ctx, i)]
    if not (url and title):
        return None
    a = f'href="{url}" rel="{rel}" target="_blank"'
    parts = [f'<aside class="bpa-book{"" if photo else " no-img"}" aria-label="{html.escape(strip_tags(html.unescape(title)), quote=True)}">']
    if photo:
        parts.append(f'<a class="bpa-book-img" {a}><img src="{photo[0]}" alt="{photo[1]}" width="800" height="534" decoding="async" loading="lazy"/></a>')
    parts.append('<div class="bpa-book-body">')
    if kicker:
        parts.append(f'<div class="bpa-book-kicker">{kicker}</div>')
    parts.append(f'<a class="bpa-book-title" {a}>{title}</a>')
    if rating:
        parts.append(f'<div class="bpa-book-rating">{rating}</div>')
    if perks:
        parts.append('<ul class="bpa-book-points">' + "".join(f"<li>{p.strip()}</li>" for p in perks) + "</ul>")
    price_html = f'<div class="bpa-book-price">{price}<small>{sub}</small></div>' if price else "<div></div>"
    parts.append(f'<div class="bpa-book-foot">{price_html}<a class="bpa-book-btn" {a}>{cta or "Check availability"} →</a></div>')
    if trust:
        parts.append(f'<div class="bpa-book-note">{trust}</div>')
    parts.append("</div></aside>")
    return "\n".join(parts)


def convert(s):
    photos = deck_photos(s)
    details = [m.start() for m in re.finditer(r'<details class="bpa-details-card"', s)]
    out, pos, n, skipped = [], 0, 0, 0
    for m in re.finditer(r'<div class="ltt-buy-card">', s):
        st = m.start()
        if st < pos:
            continue
        en = find_div_end(s, st)
        box = s[st:en]
        c = container_start(s, st)
        ctx = s[c:st] if c >= 0 else ""
        photo = None
        if c >= 0 and c in details:
            k = details.index(c)
            if k < len(photos) and len(photos) == len(details):
                photo = photos[k]
        if c < 0 and len(photos) == 1:
            # single-product page: one deck card, no breakdown list
            cs = s.find('<div class="bpa-card"')
            ctx = s[cs:find_div_end(s, cs)] if cs >= 0 and cs < st else ""
            photo = photos[0]
        if not photo and c >= 0:
            ce = s.find("</details>", st)
            whole = s[c:ce] if ce > 0 else ctx
            mm = re.search(r'<img\b[^>]*\b(?:data-src|src)="(/assets/(?!budapest-adventures-logo|nav-thumbs)[^"]+)"[^>]*>', whole)
            if mm:
                photo = (mm.group(1), first_group(r'alt="([^"]*)"', mm.group(0)))
        if not photo:
            # last resort: first content photo on the page (skip logo, author avatar, nav thumbs)
            for tag in re.findall(IMG, s):
                src = first_group(r'data-src="(/assets[^"]+)"', tag) or first_group(r'\bsrc="(/assets[^"]+)"', tag)
                if src and not re.search(r"logo|adam-dimitrov|nav-thumbs|avatar|icon", src):
                    photo = (src, first_group(r'alt="([^"]*)"', tag))
                    break
        card = build_card(box, ctx, photo)
        if not card:
            skipped += 1
            continue
        out.append(s[pos:st])
        out.append(card)
        pos = en
        n += 1
    out.append(s[pos:])
    s = "".join(out)
    if n and CSS_ID not in s:
        s = s.replace("</head>", CSS + "</head>", 1)
    return s, n, skipped


def main():
    dry = "--dry" in sys.argv
    for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
        s = open(f, encoding="utf-8").read()
        new, n, skipped = convert(s)
        print(f"{f}: {n} replaced, {skipped} skipped")
        if not dry and new != s:
            open(f, "w", encoding="utf-8").write(new)


if __name__ == "__main__":
    main()
