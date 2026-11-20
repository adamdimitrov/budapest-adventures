#!/usr/bin/env python3
"""Move an older BPA comparison page onto the shared listicle card design (river/dinner template).

The older pages already have `<div class="bpa-card">` cards, but in the earlier layout (no
thumbnails, plain price, flat filter pills, inline card CSS/JS). This script:

  1. reads every old card and turns it into kit card data (gallery + thumbnails, kicker, title,
     star-summary ratings, dropdown pills, Pick/Skip, price, booking button, trust lines);
  2. merges the page's upgrade spec (scripts/listicle_specs/<slug>.py): filter categories, the
     5 questions travellers ask per card, price dropdown rows, extra or rewritten pills, photo order;
  3. writes data/listicles/<slug>.json and swaps the page shell to the shared files: listicle CSS/JS
     tags, grouped multi-select filters with 'More filters' on phones, one sticky bar, breakdown
     data-cat kept in step with the cards, no "What guests say" quote blocks;
  4. renders the cards with the kit generator (scripts/listicle.py build) and lists the page in
     site.json listicle.pages.

    python3 scripts/listicle_upgrade.py best-private-boat-tours-budapest.html [--dry-run]

Facts stay what the page already says; the spec only adds what the new design needs and must be
sourced from the page, its builder data or the live listing.
"""
import copy
import html as _html
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L = _load("kit_listicle", os.path.join(ROOT, "kit", "scripts", "listicle.py"))
RT = _load("kit_listicle_rt", os.path.join(ROOT, "kit", "runtime", "listicle.py"))
Node = L.Node


# ------------------------------------------------------------------ helpers
def kids(n, cls=None, tag=None):
    out = []
    for c in n.ch:
        if isinstance(c, Node) and c.tag not in (None, "!--"):
            if tag and c.tag != tag:
                continue
            m = re.search(r'class="([^"]*)"', c.start)
            if cls and cls not in (m.group(1) if m else "").split():
                continue
            out.append(c)
    return out


def first(n, cls=None, tag=None):
    k = kids(n, cls, tag)
    return k[0] if k else None


def find(n, cls=None, tag=None):
    """Depth-first search for the first descendant."""
    for c in n.ch:
        if not isinstance(c, Node) or c.tag in (None, "!--"):
            continue
        m = re.search(r'class="([^"]*)"', c.start)
        if (not tag or c.tag == tag) and (not cls or cls in (m.group(1) if m else "").split()):
            return c
        r = find(c, cls, tag)
        if r is not None:
            return r
    return None


def text(n):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", n.inner()))).strip()


def balanced(src, start, tagname):
    """End offset of the element whose start tag begins at `start`."""
    depth = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tagname, src[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return start + t.end()
    raise SystemExit(f"unbalanced <{tagname}> at {start}")


def cut(src, open_re, tagname):
    m = re.search(open_re, src)
    if not m:
        return src, None
    end = balanced(src, m.start(), tagname)
    return src[:m.start()] + src[end:], (m.start(), src[m.start():end])


# ------------------------------------------------------------------ old card -> card data
TRUST_MAP = {"Instant QR": "<b>Instant QR ticket</b> on your phone",
             "Free 24h Cancellation": "<b>Free cancellation</b> up to 24 h before, full refund"}


def trust_line(t):
    t = TRUST_MAP.get(t.strip(), t)
    t = re.sub(r"^\s*✓\s*", "", t).strip()
    for key in ("Instant mobile ticket", "Free cancellation", "Reserve now", "Pay nothing today", "Free date change", "Change your date",
                "Best price", "Instant confirmation", "Skip the line", "Mobile ticket", "Pay at the property",
                "Free cancellation"):
        if t.startswith(key) and "<b>" not in t:
            return "<b>" + key + "</b>" + t[len(key):]
    return t


def price_parts(cell):
    """main/sub of the old price block: 'From €225' + 'per boat · up to 20 guests'."""
    main = find(cell, "bpa-price")
    sub = find(cell, "bpa-psub")
    m = main.inner().strip() if main is not None else ""
    m = re.sub(r"^(From|from)\s+", "", m)
    s = sub.inner().strip() if sub is not None else ""
    was = find(cell, "bpa-was")
    return m, s, (was.inner().strip() if was is not None else None)


SITE_BY_HOST = [("getyourguide", "GetYourGuide"), ("viator", "Viator"), ("tripadvisor", "Tripadvisor"),
                ("tiqets", "Tiqets"), ("booking", "Booking.com"), ("hostelworld", "Hostelworld"), ("google", "Google")]


def fmt_count(n):
    if n >= 1000:
        k = n / 1000
        return (f"{k:.1f}".rstrip("0").rstrip(".") if k < 10 else f"{int(k)}") + "k+"
    return str(n)


def parse_count(t):
    t = t.strip("()+ ").lower().replace(",", "")
    m = re.match(r"([\d.]+)\s*(k)?", t)
    if not m:
        return 0
    v = float(m.group(1)) * (1000 if m.group(2) else 1)
    return int(v)


def all_nodes(n, cls):
    out = []
    for c in n.ch:
        if not isinstance(c, Node) or c.tag in (None, "!--"):
            continue
        m = re.search(r'class="([^"]*)"', c.start)
        if m and cls in m.group(1).split():
            out.append(c)
        else:
            out += all_nodes(c, cls)
    return out


REF_ICONS = json.load(open(os.path.join(ROOT, "data", "listicles", "best-budapest-river-cruises.json"),
                           encoding="utf-8"))["icons"]
HOST_OF = {"GetYourGuide": "getyourguide", "Viator": "viator", "Tripadvisor": "tripadvisor", "Tiqets": "tiqets",
           "Booking.com": "booking", "Hostelworld": "hostelworld"}


def ratings_fallback(blk):
    """Star summary from either the newer popover (with an extra note) or the old icon-badge row."""
    sites = []
    for b in all_nodes(blk, "bpa-rev-badge"):
        href = (re.search(r'href="([^"]*)"', b.start) or [None, None])[1]
        href = _html.unescape(href) if href else None
        score, count, name = (find(b, k) for k in ("bpa-rev-score", "bpa-rev-count", "bpa-rev-site"))
        img = find(b, tag="img")
        icon = re.search(r'src="([^"]*)"', img.start).group(1) if img is not None else None
        alt = (re.search(r'alt="([^"]+)"', img.start) or [None, None])[1] if img is not None else None
        site = name.inner().strip() if name is not None else alt
        if not site and icon:
            site = next((k for k, v in REF_ICONS.items() if v == _html.unescape(icon)), None)
        if not site and href:
            site = next((v for k, v in SITE_BY_HOST if k in href), None)
        if not site and icon:
            site = next((v for k, v in SITE_BY_HOST if k in icon.lower()), None)
        if score is None or not site:
            continue
        d = {"kind": "link" if href else "static", "site": site, "score": text(score),
             "count": text(count) if count is not None else ""}
        if "review" in d["count"]:
            d["count"] = "(" + fmt_count(parse_count(d["count"])) + ("" if parse_count(d["count"]) >= 1000 else "+") + ")"
        if d["count"] and not d["count"].startswith("("):
            d["count"] = "(" + d["count"] + ")"
        host = HOST_OF.get(site)
        if href and host and host not in href and not (host in ("viator",) and "tp.media" in href):
            href = None  # a badge must link to its own site's listing of the exact product
            d["kind"] = "static"
        if href:
            d.update({"url": href, "rel": "noopener nofollow sponsored", "target": "_blank"})
        if icon and site not in ("GetYourGuide", "Viator", "Tripadvisor"):
            d["icon"] = _html.unescape(icon)
        sites.append(d)
    if not sites:
        return None
    tot = sum(parse_count(s["count"]) for s in sites)
    scale = 10 if any(float(s["score"]) > 5 for s in sites) else 5
    w = sum(float(s["score"]) * parse_count(s["count"]) for s in sites) / tot if tot else float(sites[0]["score"])
    stars = w / 2 if scale == 10 else w
    out = {"stars": f"{stars:.2f}", "score": f"{w:.1f}",
           "meta": f"{fmt_count(tot)} reviews · {len(sites)} site" + ("s" if len(sites) > 1 else ""),
           "heading": (f"Average of {len(sites)} booking sites, weighted by number of reviews" if len(sites) > 1
                       else f"Rating on {sites[0]['site']}") + (" (scores out of 10)" if scale == 10 else ""),
           "sites": sites}
    # keep the old summary line and heading when there was one
    meta, head = find(blk, "bpa-rate-meta"), find(blk, "bpa-lang-pop")
    if meta is not None:
        out["meta"] = meta.inner()
    st = find(blk, "bpa-stars")
    if st is not None:
        out["stars"] = re.search(r"--r:([\d.]+)", st.start).group(1)
        sc = find(blk, "bpa-rate-score")
        out["score"] = sc.inner() if sc is not None else out["score"]
    if head is not None:
        strong = find(head, tag="strong")
        note = find(head, "bpa-lang-note")
        if strong is not None:
            out["heading"] = strong.inner()
        if note is not None:
            out["_note"] = note.inner()
    return out


def kicker_fallback(blk):
    parts = []
    for part in blk.inner().split(L.KICK_SEP):
        m = re.fullmatch(r'<a ([^>]*)>(.*)</a>', part.strip(), re.S)
        if m:
            at = dict((k, _html.unescape(v)) for k, v in re.findall(r'([a-z-]+)="([^"]*)"', m.group(1)))
            f = {"url": at["href"], "map": m.group(2)}
            for k in ("rel", "target", "onclick"):
                if k in at:
                    f[k] = at[k]
            parts.append(f)
        else:
            parts.append(re.sub(r'<span class="bpa-kicker-map-link">(.*?)</span>', r"\1", part))
    return parts


def old_card(node, icons):
    a = node.a()
    card = {"id": a["id"], "cats": (a.get("data-cat") or "").split()}
    main = first(node, "bpa-main")
    media = find(main, "bpa-media")
    info = find(main, "bpa-info")
    cell = find(main, "bpa-cta-cell")
    # gallery
    rank = find(media, "bpa-rank-tag")
    rcls = re.search(r'class="([^"]*)"', rank.start).group(1).split()
    medal = [c for c in rcls if c != "bpa-rank-tag"]
    slider = find(media, "bpa-slider")
    photos = [c.attrs() for c in kids(slider, tag="img")]
    card["gallery"] = {"rank": {"text": rank.inner(), "medal": " ".join(medal) or "bpa-slate"},
                       "photos": photos}
    # info blocks
    extras = []
    for blk in kids(info):
        mm = re.search(r'class="([^"]*)"', blk.start)
        cls = mm.group(1) if mm else ""
        if "bpa-kicker" in cls.split():
            try:
                card["kicker"] = L.ex_kicker(blk)
            except L.Unmodelled:
                card["kicker"] = kicker_fallback(blk)
        elif "bpa-title" in cls.split():
            card["title"] = L.ex_title(blk)
        elif "bpa-reviews-line" in cls.split():
            try:
                rv = L.ex_reviews(blk, icons)
                if "raw" in rv.get("ratings", {}):
                    raise L.Unmodelled("rating raw")
                card["reviews"] = rv
            except (L.Unmodelled, ValueError, KeyError):
                card["_old_reviews"] = blk.outer()
                r = ratings_fallback(blk)
                if r:
                    card["reviews"] = {"ratings": r}
                    card.pop("_old_reviews")
        elif "bpa-specs-row" in cls.split():
            pills = []
            for p in kids(blk):
                pc = (re.search(r'class="([^"]*)"', p.start) or [None, ""])[1].split()
                if "bpa-tested" in pc or "bpa-vchip" in pc or "bpa-proof-mobile" in pc:
                    if p.tag == "details":
                        pop = find(p, "bpa-lang-pop")
                        card["_tested"] = {"chip": "✓ Personally Tested", "pop_html": pop.inner()}
                    continue
                if p.tag == "details":
                    try:
                        pills.append(L.ex_pill(p))
                    except L.Unmodelled:
                        summ = find(p, tag="summary")
                        pop = find(p, "bpa-lang-pop")
                        lab = find(summ, "bpa-lang-label")
                        em = re.sub(r"<[^>]+>.*", "", summ.inner(), flags=re.S).strip()
                        pills.append({"cls": re.search(r'class="([^"]*)"', p.start).group(1), "emoji": em or "•",
                                      "label": lab.inner() if lab is not None else text(summ).rstrip("▾ "),
                                      "pop_html": pop.inner() if pop is not None else ""})
                else:
                    t = p.inner().strip()
                    m = re.match(r"^(\S+)\s+(.*)$", re.sub(r"<[^>]+>", "", t).strip())
                    pills.append({"cls": "bpa-lang", "emoji": m.group(1) if m else "•",
                                  "label": m.group(2) if m else t, "pop_html": "", "_plain": True})
            card["pills"] = pills
        elif "bpa-pickskip" in cls.split():
            card["best_for"] = L.ex_bestfor(blk)
        elif "bpa-best-for" in cls.split():
            inner = blk.inner().strip()
            m = re.fullmatch(r'<strong>Best For:</strong>\s*(.*?)\s*<strong>Skip (?:it )?if:?</strong>\s*(.*)', inner, re.S | re.I)
            if m:
                pick = m.group(1).strip()
                card["best_for"] = {"pick_html": "for " + pick[0].lower() + pick[1:] if not pick.lower().startswith("for ") else pick,
                                    "skip_html": "if " + m.group(2).strip()}
            else:
                card["_old_bestfor"] = inner
        else:
            extras.append(blk.outer())
    if "best_for" not in card:
        ps = find(info, "bpa-pickskip")
        if ps is not None:
            card["best_for"] = L.ex_bestfor(ps)
    if extras:
        card["_old_extras"] = extras
    # price + cta
    m, s, was = price_parts(cell)
    card["price"] = {"main": m, "sub": s}
    if was:
        card["price"]["_was"] = was
    cta = {}
    btn = find(cell, "bpa-btn", "a")
    if btn is not None:
        f = L.link_fields(btn, "bpa-btn")
        f.pop("_order", None)
        f["text"] = btn.inner()
        cta["btn"] = f
    via = find(cell, "bpa-via")
    if via is not None:
        cta["via"] = via.inner()
    tr = find(cell, "bpa-trust2") or find(cell, "bpa-trust-micro")
    if tr is not None:
        cta["trust"] = [trust_line(sp.inner()) for sp in kids(tr, tag="span") if sp.inner().strip() not in ("•", "")]
    subs = kids(cell, "bpa-sublink", "a")
    if subs:
        cta["sublink"] = {"url": subs[0].a()["href"], "text": subs[0].inner()}
    if len(subs) > 1:
        card["_guide_links"] = [x.outer() for x in subs[1:]]
    card["cta"] = cta
    return card


def old_cards(src):
    a, b, spans = L.region(src)
    icons = {}
    out = []
    for i, (s, e) in enumerate(spans):
        root = L.parse(src[s:e])
        node = [c for c in root.ch if isinstance(c, Node)][0]
        c = old_card(node, icons)
        before = src[spans[i - 1][1]:s] if i else None
        if before is not None and before != "\n\n":
            c["before"] = before
        out.append(c)
    return out


# ------------------------------------------------------------------ spec merge
# neutral star badge for review sites without their own icon (operator ratings on TourRadar)
GENERIC_ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Ccircle cx='8' cy='8' r='8' "
                "fill='%230f766e'/%3E%3Cpath d='M8 3.2l1.4 2.9 3.2.4-2.3 2.2.6 3.1L8 10.3l-2.9 1.5.6-3.1-2.3-2.2 3.2-.4z' fill='%23fff'/%3E%3C/svg%3E")
SIZES = "(max-width: 767px) 420px, (max-width: 991px) 55vw, (max-width: 1439px) 49vw, 50vw"


def build_gallery(card, spec_card, placeholder):
    g = card["gallery"]
    old = g["photos"]
    d0 = dict(old[0])
    alt = spec_card.get("alt") or d0.get("alt", "")
    srcs = spec_card.get("photos")  # explicit list of paths wins
    if not srcs:
        srcs = []
        for p in old:
            d = dict(p)
            srcs.append(d.get("data-src") or d.get("src"))
        if spec_card.get("photo_order"):
            srcs = [srcs[i - 1] for i in spec_card["photo_order"]]
        if spec_card.get("photos_drop_old"):
            srcs = []
        srcs = spec_card.get("photos_prepend", []) + srcs + spec_card.get("photos_add", [])
    photos = []
    for i, s in enumerate(srcs):
        if i == 0 and card["id"] == "card-1":
            photos.append([["alt", alt], ["fetchpriority", "high"], ["height", "534"], ["loading", "eager"], ["sizes", SIZES],
                           ["src", s], ["width", "800"]])
        elif i == 0:
            photos.append([["alt", alt], ["height", "534"], ["loading", "lazy"], ["sizes", SIZES], ["src", s], ["width", "800"]])
        else:
            photos.append([["alt", alt], ["data-src", s], ["decoding", "async"], ["loading", "lazy"],
                           ["sizes", SIZES], ["src", placeholder]])
    g["photos"] = photos
    g["thumbs"] = [{"src": s} for s in srcs]
    if "rank" in spec_card:
        g["rank"] = dict(g["rank"], **spec_card["rank"])


def merge(card, sc, placeholder):
    build_gallery(card, sc, placeholder)
    if "cats" in sc:
        card["cats"] = sc["cats"]
    if "kicker" in sc:
        card["kicker"] = sc["kicker"]
    if "title" in sc:
        card["title"] = dict(card["title"], **sc["title"])
    if "ratings" in sc:
        card["reviews"] = {"ratings": sc["ratings"]}
        card.pop("_old_reviews", None)
    if sc.get("no_ratings"):
        card.pop("reviews", None)
        card.pop("_old_reviews", None)
    if sc.get("unlink_ratings") and "reviews" in card:
        for st in card["reviews"]["ratings"].get("sites", []):
            if st["kind"] == "link":
                st["kind"] = "static"
                for k in ("url", "rel", "target"):
                    st.pop(k, None)
    if sc.get("fold_note") and "_note" in card.get("reviews", {}).get("ratings", {}):
        r = card["reviews"]["ratings"]
        n = r.pop("_note")
        r["heading"] = r["heading"] + ": " + n[0].lower() + n[1:]
    for st in card.get("reviews", {}).get("ratings", {}).get("sites", []):
        if st["site"] not in ("GetYourGuide", "Viator", "Tripadvisor") and not st.get("icon"):
            st["icon"] = GENERIC_ICON
    if "ratings_patch" in sc:
        card["reviews"]["ratings"].update(sc["ratings_patch"])
    if "add_sites" in sc:
        card["reviews"]["ratings"]["sites"] += sc["add_sites"]
    if sc.get("tested"):
        t = sc["tested"] if isinstance(sc["tested"], dict) else card.get("_tested")
        if not t:
            raise SystemExit(f"{card['id']}: tested=True but the old card has no tested popover; give the text")
        card.setdefault("reviews", {})["tested"] = t
    elif "reviews" in card:
        card["reviews"].pop("tested", None)  # tested stamp only where the spec allows it
    if "pills" in sc:
        card["pills"] = sc["pills"]
    else:
        for i, p in enumerate(card.get("pills", [])):
            p.pop("_plain", None)
            if "pill_pops" in sc and i in sc["pill_pops"]:
                p["pop_html"] = sc["pill_pops"][i]
    if "slot" in sc:
        card["slot"] = sc["slot"]
    if "best_for" in sc:
        card["best_for"] = sc["best_for"]
    card["faq"] = {"items": [{"q": q, "a": a} for q, a in sc["faq"]]}
    pr = sc.get("price", {})
    card["price"].pop("_was", None)
    card["price"].update({k: v for k, v in pr.items()})
    if "_guide_links" in card:
        if not sc.get("drop_guide_links"):
            links = " ".join(re.sub(r' class="[^"]*"', "", x) for x in card["_guide_links"])
            card["price"]["note"] = (card["price"].get("note", "") + " " + links).strip()
        card.pop("_guide_links")
    if "trust" in sc:
        card["cta"]["trust"] = sc["trust"]
    if "via" in sc:
        card["cta"]["via"] = sc["via"]
    if "btn_text" in sc:
        card["cta"]["btn"]["text"] = sc["btn_text"]
    if "_old_bestfor" in card and "best_for" not in sc:
        raise SystemExit(f"{card['id']}: old Best For line needs best_for in the spec: {card['_old_bestfor'][:120]}")
    if card.get("_old_extras") and not sc.get("drop_extras"):
        card["extras_after_best_for"] = "\n".join(card["_old_extras"])
    if "_note" in card.get("reviews", {}).get("ratings", {}):
        note = card["reviews"]["ratings"].pop("_note")
        if not sc.get("drop_rating_note"):
            raise SystemExit(f"{card['id']}: rating popover note has no slot, fold it into ratings_patch.heading: {note}")
    for k in ("_old_extras", "_tested", "_old_bestfor"):
        card.pop(k, None)
    if "_old_reviews" in card:
        raise SystemExit(f"{card['id']}: old rating row needs 'ratings' in the spec")
    for p in card.get("pills", []):
        if not p.get("pop_html"):
            raise SystemExit(f"{card['id']}: pill {p.get('label')!r} needs a dropdown text (pill_pops)")
    if len(card["faq"]["items"]) != RT.FAQ_PER_CARD:
        raise SystemExit(f"{card['id']}: needs exactly {RT.FAQ_PER_CARD} questions")
    # house key order
    order = ["before", "id", "cats", "gallery", "kicker", "title", "reviews", "pills", "slot", "best_for",
             "extras_after_best_for", "faq", "price", "cta"]
    return {k: card[k] for k in order if k in card}


# ------------------------------------------------------------------ page shell
def filter_box(spec, total):
    noun = spec["noun"]
    rows = []
    for gi, grp in enumerate(spec["filters"]):
        cls = "cd-frow cd-frow-main" if gi == 0 else "cd-frow cd-frow-more"
        chips = "".join(
            f'<button class="ltt-tab-btn" data-cat="{c}" onclick="lttFilterCruises(\'{c}\', this)" type="button" '
            f'aria-pressed="false">{lab} <span class="cd-n"></span></button>' for c, lab in grp["chips"])
        rows.append(f'<div class="{cls}"><span class="cd-flab">{grp["label"]}</span><div class="cd-fchips">{chips}</div></div>')
    more = ('<button type="button" class="cd-fmore" aria-expanded="false" hidden>More filters '
            '<span class="cd-fmore-n"></span> ▾</button>') if len(spec["filters"]) > 1 else ""
    foot = (f'<div class="cd-ffoot"><span class="cd-fcount" aria-live="polite">Showing <b>{total}</b> of {total} {noun}</span>'
            f'<div class="cd-fapplied"></div><button type="button" class="cd-fclear" hidden '
            f'onclick="lttFilterCruises(\'all\')">Clear all</button></div>')
    box = (f'<div class="ltt-integrated-filter-bar cd-fbox" id="cd-filters" role="group" aria-label="{spec["filter_aria"]}">'
           + "".join(rows) + more + foot + "</div>")
    mini = (f'<div class="cd-fmini" aria-hidden="true"><div class="cd-fmini-in"><button type="button" class="cd-fmini-btn" '
            f'onclick="cdFiltersJump()">⚙️ Filters <span class="cd-fmini-n" hidden></span></button>'
            f'<span class="cd-fmini-res"><b>{total}</b> of {total} {noun}</span></div></div>')
    return box, mini


def ui_json(spec):
    noun = spec["noun"]
    return ('<script type="application/json" id="listicle-ui">' + json.dumps({
        "showing": "Showing <b>{shown}</b> of {total} " + noun,
        "mini_count": "<b>{shown}</b> of {total} " + noun,
        "breakdown_filtered": "Showing {shown} of {total} " + noun + " matching your filters",
    }, ensure_ascii=False) + "</script>")


def group(file):
    return [g for g in RT.MANIFEST if g["file"] == file][0]


CSS_EXTRA = """<style id="cd-trust-css">
.bpa-card .bpa-trust2{display:flex!important;flex-direction:column!important;align-items:stretch;gap:3px!important;width:100%;box-sizing:border-box;
  margin-top:6px;padding:6px 9px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;
  font:500 12px/1.35 'Plus Jakarta Sans',sans-serif!important;color:#3f6212;text-align:left}
.bpa-card .bpa-trust2 span{display:block;position:relative;padding-left:20px}
.bpa-card .bpa-trust2 span::before{content:"";position:absolute;left:0;top:1px;width:14px;height:14px;border-radius:50%;background:#16a34a url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.3l2.6 2.5L12 5.4' fill='none' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/12px no-repeat}
.bpa-card .bpa-trust2 b{color:#14532d;font-weight:800}
.bpa-card .bpa-via{line-height:1.35!important}
</style><style id="listicle-card-parity-css">.bpa-card .bpa-rank-tag{text-transform:none!important;letter-spacing:normal!important}.bpa-card .bpa-title{letter-spacing:normal!important}.bpa-card .bpa-stars{font-size:13px!important}.bpa-card .bpa-proof{border-radius:0!important}.bpa-card .bpa-vchip{letter-spacing:normal!important}</style>"""

JS_TAIL = """<script id="cd-sticky-trust-js">
(function(){ var r=document.getElementById('sticky-rank'), t=document.getElementById('sticky-trust'); if(!r||!t) return;
  function upd(){ var n=(r.textContent.match(/#(\\d+)/)||[])[1], c=n&&document.getElementById('card-'+n), bs=c?[].slice.call(c.querySelectorAll('.bpa-trust2 b')):[], b=bs.filter(function(x){return /Free cancellation/.test(x.textContent);})[0]||bs[0]; if(b) t.textContent=b.textContent; }
  new MutationObserver(upd).observe(r,{childList:true,characterData:true,subtree:true}); upd(); })();
</script>
{TAGS}
<script id="pdd-hover-js">
/* Price dropdown opens on hover like the pills (desktop with a mouse only); a click pins it open. */
(function(){
  if(!(window.matchMedia&&matchMedia('(hover: hover) and (pointer: fine)').matches)) return;
  function init(){ document.querySelectorAll('.cd-pdd').forEach(function(d){
    var t, pinned=false, sm=d.querySelector('summary'); if(!sm) return;
    d.addEventListener('mouseenter',function(){ clearTimeout(t); if(!d.open){ d.dataset.hov='1'; d.open=true; } });
    d.addEventListener('mouseleave',function(){ if(pinned) return; t=setTimeout(function(){ if(d.dataset.hov){ delete d.dataset.hov; d.open=false; } },180); });
    sm.addEventListener('click',function(e){ if(d.dataset.hov){ e.preventDefault(); delete d.dataset.hov; pinned=true; } else { pinned=!d.open; } });
    d.addEventListener('toggle',function(){ if(!d.open){ pinned=false; delete d.dataset.hov; } });
  }); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>
"""

JS_FILES = ["listicle-lang.js", "listicle-cards.js", "listicle-filters.js", "listicle-fbm.js",
            "listicle-fmore.js", "listicle-days.js", "listicle-peek.js"]


def shell(src, spec, cards, icons):
    total = len(cards)
    # 1. CSS: inline card CSS -> shared files
    for bid in ("bpa-lang-css", "bpa-card2-css"):
        src = re.sub(r'<style id="%s">.*?</style>' % bid, "", src, count=1, flags=re.S)
    if "/css/listicle-base.css" not in src:
        i = src.find("</head>")
        src = (src[:i] + RT.tag(group("listicle-base.css")) + RT.tag(group("listicle-cards.css")) + CSS_EXTRA
               + src[i:])
    # 2. filters
    box, mini = filter_box(spec, total)
    m = re.search(r'<div class="ltt-integrated-filter-bar[^"]*"[^>]*>', src)
    if m:
        end = balanced(src, m.start(), "div")
        src = src[:m.start()] + box + src[end:]
        # mini bar goes right before the deck
        d = src.find('<div class="bpa-deck-wrap"')
        if d > 0 and "cd-fmini" not in src:
            src = src[:d] + mini + src[d:]
    # 3. one sticky bar
    if 'id="sticky-bar"' in src:
        src, _ = cut(src, r'<aside[^>]*id="hybridStickyBar"[^>]*>', "aside")
    src = re.sub(r'(<aside[^>]*id="sticky-bar".*?)<span class="hybrid-active-trust">', r'\1<span class="hybrid-active-trust" id="sticky-trust">',
                 src, count=1, flags=re.S)
    # 4. breakdown data-cat follows the cards; no quote blocks
    for c in cards:
        anchor = c["cta"].get("sublink", {}).get("url", "")
        if anchor.startswith("#"):
            src = re.sub(r'(<details class="bpa-details-card") data-cat="[^"]*"( id="%s")' % re.escape(anchor[1:]),
                         lambda mm: f'{mm.group(1)} data-cat="{" ".join(c["cats"])}"{mm.group(2)}', src)
    # breakdown headers: old icon-badge rating row -> the card's star summary
    for c in cards:
        anchor = c["cta"].get("sublink", {}).get("url", "")
        r = c.get("reviews", {}).get("ratings")
        if not (anchor.startswith("#") and r):
            continue
        a = src.find(f'id="{anchor[1:]}"')
        if a < 0:
            continue
        stop = src.find("bpa-details-body", a)
        m = re.compile(r'<div class="bpa-summary-reviews">').search(src, a, stop)
        if m:
            end = balanced(src, m.start(), "div")
            src = src[:m.start()] + L.render_rating(r, icons) + src[end:]
    src = re.sub(r'<h3[^>]*>What (guests|visitors) say</h3>(\s*<blockquote>.*?</blockquote>)+', "", src, flags=re.S)
    src = re.sub(r'<blockquote><strong>What (guests|visitors) say:</strong>.*?</blockquote>', "", src, flags=re.S)
    # "Based on 1,400+ GetYourGuide reviews (4.2 out of 5), visitors praise ..." -> "Visitors praise ..."
    src = re.sub(r'<p>Based on (?:(?!</p>).)*?(?:\)|reviews(?:</strong>)?(?: on [A-Za-z ]+(?: and [A-Za-z]+)?)?),\s*([a-z])',
                 lambda m: "<p>" + m.group(1).upper(), src)
    # 5. JS: inline lang JS -> shared files at the end of the body
    src = re.sub(r'<script id="bpa-lang-js">.*?</script>', "", src, count=1, flags=re.S)
    if "/js/listicle-cards.js" not in src:
        tags = "".join(RT.tag(group(f)) for f in JS_FILES)
        tail = (ui_json(spec) + "\n" if spec.get("noun") != "cruises" else "") + JS_TAIL.replace("{TAGS}", tags)
        i = src.rfind("</body>")
        src = src[:i] + tail + src[i:]
    return src


def site_json_add(rel):
    p = os.path.join(ROOT, "site.json")
    raw = open(p, encoding="utf-8").read()
    d = json.loads(raw)
    pages = d.setdefault("listicle", {}).setdefault("pages", [])
    if rel in pages:
        return
    # insert after the last English page so the list stays grouped
    en = [i for i, x in enumerate(pages) if "/" not in x]
    pages.insert((en[-1] + 1) if en else 0, rel)
    open(p, "w", encoding="utf-8").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    dry = "--dry-run" in argv
    rel = args[0]
    page = os.path.join(ROOT, rel)
    slug = os.path.basename(rel)[:-5] if rel.endswith(".html") else os.path.basename(os.path.dirname(rel))
    spec = _load("spec", os.path.join(ROOT, "scripts", "listicle_specs", slug.replace("-", "_") + ".py"))
    src = open(page, encoding="utf-8").read()
    cards = old_cards(src)
    # placeholder used by the reference pages for lazy photos
    ref = json.load(open(os.path.join(ROOT, "data", "listicles", "best-budapest-river-cruises.json"), encoding="utf-8"))
    ph = dict(ref["cards"][0]["gallery"]["photos"][1])["src"]
    icons = ref["icons"]
    new = []
    for c in cards:
        sc = spec.CARDS.get(c["id"])
        if sc is None:
            raise SystemExit(f"spec has no entry for {c['id']}")
        new.append(merge(copy.deepcopy(c), sc, ph))
    if hasattr(spec, "ORDER"):
        new = [next(c for c in new if c["id"] == i) for i in spec.ORDER]
    data = {"format": 1, "icons": {k: v for k, v in icons.items()}, "cards": new}
    out = shell(src, spec.PAGE, new, data["icons"])
    out = L.build_page(out, data)
    if dry:
        print(f"{rel}: {len(new)} cards would be rebuilt")
        return 0
    dpath = L.data_path(page)
    with open(dpath, "w", encoding="utf-8") as fh:
        fh.write(L.dumps(data) + "\n")
    open(page, "w", encoding="utf-8").write(out)
    site_json_add(rel)
    print(f"{rel}: {len(new)} cards -> {os.path.relpath(dpath, ROOT)}; shell on shared listicle files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
