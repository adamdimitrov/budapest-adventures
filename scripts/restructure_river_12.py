#!/usr/bin/env python3
"""Rebuild the EN river cruises deck as a top 12 (run BEFORE build_river_cards.py).

Out: Portum (old #4), Hungária dinner (#8), Hungária drinks (#9).
In:  Legenda Candlelit Dinner, River Diva and Floating Lotus (cards + reviews + JSON-LD
     taken from best-night-cruises-budapest.html), and two new cards built from
     scripts/articles/river-cruises-new-cards.json with build_article.py's templates
     (360° Panoramic Cruise, Silverline Cosy Cruise).

Usage: restructure_river_12.py <river page (old card format)> <night page (old card format)> [--photos]
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE, NIGHT = sys.argv[1], sys.argv[2]
PHOTOS = "--photos" in sys.argv
s = open(PAGE, encoding="utf-8").read()
night = open(NIGHT, encoding="utf-8").read()
URL = "https://www.budapestadventures.com/best-budapest-river-cruises"

# new order: (anchor, source, rank label without the number)
ORDER = [  # Legenda / Silverline earn more, so they lead, alternating with the strongest other picks
    ("cruise-1-legenda", "river", None),
    ("cruise-2-rubingroup", "river", None),
    ("cruise-7-silverline-prosecco", "river", "🍾 #{n} Best Unlimited Prosecco"),
    ("item-5-river-diva-dinner", "night", "🎻 #{n} Best All-Inclusive Dinner"),
    ("item-4-legenda-candlelit-dinner", "night", "🕯️ #{n} Best Romantic Dinner"),
    ("cruise-silverline-mulled-wine", "new", None),
    ("cruise-3-kisfaludy-historic-cruise", "river", None),
    ("cruise-10-mahart", "river", "⛴️ #{n} Best Discounted Night Cruise"),
    ("cruise-5-silverline-no-frills", "river", "🥤 #{n} Best for Non-Drinkers"),
    ("cruise-6-la-perla", "river", None),
    ("cruise-cosy-chimney-cake", "new", "☕ #{n} Best Cosy Winter Treat"),
    ("cruise-360-panoramic", "new", "🌐 #{n} Best 360° Views"),
    ("cruise-silverline-folklore", "new", None),
]
SHORT = {
    "cruise-360-panoramic": "360° Panoramic Cruise + Tokaji Frizzante",
    "cruise-cosy-chimney-cake": "Silverline Cosy Cruise + Chimney Cake",
    "cruise-silverline-mulled-wine": "Silverline Unlimited Mulled Wine Cruise",
    "cruise-silverline-folklore": "Silverline Drink & Folklore Show Cruise",
    "item-4-legenda-candlelit-dinner": "Legenda Candlelit Dinner Cruise",
    "item-5-river-diva-dinner": "River Diva Buffet Dinner Cruise",
    "cruise-5-silverline-no-frills": "Silverline Sightseeing Cruise, Pay Only for What You Drink",
}
PRICE_FIX = {"cruise-10-mahart": 12}
SILVERLINE = "https://budapestrivercruise.eu/product/{}/?code=bpadventures"
# Silverline's own booking page (better commission) instead of the GYG listing
DIRECT = {"cruise-7-silverline-prosecco": SILVERLINE.format("unlimited-prosecco-and-wine-cruise")}
NON_DRINKERS = ("No drink in the price, so you only pay for what you order. ")


def cards_by_anchor(src):
    starts = [m.start() for m in re.finditer(r'<div class="bpa-card" data-cat="[^"]*" id="card-\d+">', src)]
    # include a "<!-- #n: … -->" line right before the first card in the deck range
    pre = re.search(r'<!-- #\d+:[^\n]*-->\n$', src[:starts[0]])
    first = pre.start() if pre else starts[0]
    last_sub = src.find('class="bpa-sublink"', starts[-1])
    tail = src.find("</div>\n</div>\n</div>", last_sub) + len("</div>\n</div>\n</div>")
    out = {}
    for a, b in zip(starts, starts[1:] + [tail]):
        c = re.sub(r'\n?<!-- #\d+:[^\n]*-->\n?$', "\n", src[a:b])
        out[re.search(r'class="bpa-sublink" href="#([^"]+)"', c).group(1)] = c
    return out, first, tail


def reviews_by_anchor(src):
    out, first, last = {}, None, None
    for m in re.finditer(r'<details class="bpa-details-card"[^>]*id="([^"]+)"', src):
        st, depth = m.start(), 0
        for t in re.finditer(r"<(/?)details\b", src[st:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                en = src.index(">", st + t.start()) + 1
                break
        out[m.group(1)] = src[st:en]
        first = st if first is None else first
        last = en
    return out, first, last


def jsonld_items(src):
    m = re.search(r'(<script id="ltt-schema-jsonld" type="application/ld\+json">)(.*?)(</script>)', src, re.S)
    data = json.loads(m.group(2))
    lst = data["@graph"][0]["mainEntity"]
    return m, data, lst, {e["url"].split("#")[1]: e for e in lst["itemListElement"]}


# ------------------------------------------------------------------ sources
rc, deck_a, deck_b = cards_by_anchor(s)
nc, _, _ = cards_by_anchor(night)
rr, rev_a, rev_b = reviews_by_anchor(s)
nr, _, _ = reviews_by_anchor(night)
jm, jdata, jlist, rj = jsonld_items(s)
_, _, _, nj = jsonld_items(night)

spec_mod = importlib.util.spec_from_file_location("ba", ROOT / "scripts" / "build_article.py")
ba = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(ba)
spec = json.loads((ROOT / "scripts/articles/river-cruises-new-cards.json").read_text())
if PHOTOS:
    ba.fetch_photos(spec, spec["slug"])
else:
    for n, it in enumerate(spec["items"], 1):
        it["photos"] = [f"/assets/{spec['slug']}/{n:02d}-{it['photo_slug']}-{k:02d}.avif" for k in range(1, len(it["gallery"][:10]) + 1)]
gyg_icon = re.search(r'<img alt="GetYourGuide" class="bpa-rev-icon"[^>]*src="([^"]+)"', s) or re.search(r'class="bpa-rev-icon"[^>]*alt="GetYourGuide"[^>]*src="([^"]+)"', s)
gyg_icon = gyg_icon.group(1) if gyg_icon else "/assets/gyg-icon.png"
newc, newr = {}, {}
for it in spec["items"]:
    if "getyourguide" in it["link"] or not it["link"].startswith("http"):
        it["link"] = ba.gyg_link(it["link"], f"{spec['cmp']}-button-{it['photo_slug']}")
    it["_pname"], it["_picon"] = "GetYourGuide", gyg_icon
    c_html, r_html = ba.card_html(0, it, gyg_icon), ba.details_html(0, it, gyg_icon)
    prov = it.get("provider")
    if prov:  # booked on the operator's own site; the rating badge still points at the listing it comes from
        c_html = c_html.replace("Booked securely via GetYourGuide", f"Booked securely via {prov}")
        if it.get("rating_link"):
            for h in (c_html, r_html):
                pass
            badge = 'class="bpa-rev-badge is-link" href="' + ba.esc_attr(it["link"]) + '"'
            c_html = c_html.replace(badge, 'class="bpa-rev-badge is-link" href="' + ba.esc_attr(it["rating_link"]) + '"')
            r_html = r_html.replace('class="bpa-rev-badge" href="' + ba.esc_attr(it["link"]) + '"', 'class="bpa-rev-badge" href="' + ba.esc_attr(it["rating_link"]) + '"')
        c_html = c_html.replace("New listing, no reviews yet", f"Live folk &amp; operetta show by {prov}")
    newc[it["anchor"]] = c_html
    newr[it["anchor"]] = r_html

# ------------------------------------------------------------------ renumber


def renumber(block, n, label, is_card):
    if is_card:
        block = re.sub(r'id="card-\d+"', f'id="card-{n}"', block, count=1)
        block = re.sub(r"^<!-- #\d+:[^\n]*-->\n", "", block)
    if label:
        block = re.sub(r'(<span class="bpa-rank-tag[^"]*">)[^<]*(</span>)', lambda m: m.group(1) + label.format(n=n) + m.group(2), block, count=1)
    else:
        block = re.sub(r'(<span class="bpa-rank-tag[^"]*">[^<#]*)#\d+', lambda m: f"{m.group(1)}#{n}", block, count=1)
    return block


def set_price(block, anchor):
    p = PRICE_FIX.get(anchor)
    if not p:
        return block
    block = re.sub(r'<div class="bpa-was">.*?</div>\s*', "", block, flags=re.S)
    block = re.sub(r'(<div class="bpa-price">)(?:From )?€[\d.,]+', rf"\g<1>From €{p}", block, count=1)
    block = re.sub(r'(<span class="bpa-details-price">)(?:From )?€[\d.,]+', rf"\g<1>From €{p}", block, count=1)
    block = re.sub(r'(<span class="ltt-buy-price-val">)(?:From )?€[\d.,]+', rf"\g<1>From €{p}", block, count=1)
    return block


cards, reviews, items, shorts = [], [], [], []
cfg = re.search(r'window\.LTT_PAGE_CONFIG = (\{.*?\});', s).group(1)
old_short = json.loads(cfg)["shortTitles"]
river_order = list(rc.keys())
for n, (anc, src, label) in enumerate(ORDER, 1):
    card = {"river": rc, "night": nc, "new": newc}[src][anc]
    rev = {"river": rr, "night": nr, "new": newr}[src][anc]
    if src == "night":
        card = card.replace("#" + anc, "#" + anc)  # anchors are unique, keep them
    if anc in DIRECT:
        url = DIRECT[anc]
        for cls in ("bpa-btn", "bpa-title", "ltt-buy-cta-btn", "main-buy-button"):
            card = re.sub(r'(<a class="%s"[^>]*?href=")[^"]*(")' % cls, lambda m: m.group(1) + url + m.group(2), card)
            rev = re.sub(r'(<a class="%s"[^>]*?href=")[^"]*(")' % cls, lambda m: m.group(1) + url + m.group(2), rev)
        card = card.replace("Booked securely via GetYourGuide", "Booked securely via Silverline Cruises")
    if anc == "cruise-5-silverline-no-frills":
        card = card.replace('<span class="bpa-pick">✓ Pick it</span> ', '<span class="bpa-pick">✓ Pick it</span> ' + NON_DRINKERS, 1)
    cards.append(set_price(renumber(card, n, label, True), anc))
    reviews.append(set_price(renumber(rev, n, label, False), anc))
    shorts.append(SHORT.get(anc) or old_short[river_order.index(anc)])
    if src == "river":
        e = json.loads(json.dumps(rj[anc]))
    elif src == "night":
        e = json.loads(json.dumps(nj[anc]))
        e["url"] = f"{URL}#{anc}"
    else:
        it = next(i for i in spec["items"] if i["anchor"] == anc)
        e = {"@type": "ListItem", "url": f"{URL}#{anc}", "item": {
            "@type": "Product", "name": it["title"], "description": f"{it['rank_tag'].split(' ', 1)[1]}: {it['pick'][4:] if it['pick'].startswith('for ') else it['pick']}",
            "brand": {"@type": "Organization", "name": it["operator"]},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": it["rating"], "reviewCount": it["reviews"], "bestRating": 5},
            "offers": {"@type": "Offer", "price": it["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": it["link"]},
            "image": "https://www.budapestadventures.com" + it["photos"][0]}}
    e["position"] = n
    d = e["item"].get("description", "")
    e["item"]["description"] = re.sub(r"#\d+", f"#{n}", d, count=1)
    if label:
        e["item"]["description"] = re.sub(r"^(?:\S+ )?#\d+ [^:]+", label.format(n=n), e["item"]["description"])
    if anc in DIRECT and isinstance(e["item"].get("offers"), dict):
        e["item"]["offers"]["url"] = DIRECT[anc]
    if anc in PRICE_FIX and isinstance(e["item"].get("offers"), dict):
        e["item"]["offers"]["price"] = PRICE_FIX[anc]
    items.append(e)

s = s[:deck_a] + "\n".join(cards) + s[deck_b:]
rr2, rev_a, rev_b = reviews_by_anchor(s)
s = s[:rev_a] + "\n".join(reviews) + s[rev_b:]

jm, jdata, jlist, _ = jsonld_items(s)
jlist["itemListElement"] = items
jlist["numberOfItems"] = len(items)
s = s.replace(jm.group(0), jm.group(1) + json.dumps(jdata, ensure_ascii=False) + jm.group(3))

cfgd = json.loads(cfg)
cfgd["shortTitles"] = shorts
cfgd["tocDeckLabel"] = "Top 13 Cruises Comparison"
cfgd["tocBreakdownLabel"] = "Detailed Breakdown (13 Cruises)"
s = s.replace(cfg, json.dumps(cfgd, ensure_ascii=False))

# ------------------------------------------------------------------ copy: 10 -> 12, tested count 8 -> 6
TEXT = [
    ("10 Best River Cruises in Budapest", "13 Best River Cruises in Budapest", None),
    ("I personally tested 8 of these 10 day and night cruises", "I personally tested 6 of these 13 day and night cruises", None),
    ("8 of 10 Cruises Tested in Person", "6 of 13 Cruises Tested in Person", 1),
    ("added two well-reviewed newcomers, and compared the 10 worth your evening", "added a few well-reviewed newcomers, and compared the 13 worth your evening", 1),
    ("a guaranteed rooftop seat or a folk-show dinner. Tickets run <strong>from €11 to €79</strong>",
     "a guaranteed rooftop seat or a candlelit dinner. Tickets run <strong>from €11 to €110</strong>", 1),
    ("ranked the 10 best river cruises", "ranked the 13 best river cruises", 1),
    ("Matched against the 10 cruises I compared on this page.", "Try: \u201cIs it cold on deck?\u201d \u00b7 \u201cCan kids come?\u201d \u00b7 \u201cRomantic, under \u20ac30\u201d", 1),
    ("Show all 10 again", "Show all 13 again", 1),
    ("All 10 Danube Cruises", "All 13 Danube Cruises", 1),
    ('<span class="bpa-ai-kicker">Find your cruise</span>', '<span class="bpa-ai-kicker">Ask or find your cruise</span>', 1),
    ('<button id="bpa-ai-go" type="submit">Find my cruise</button>', '<button id="bpa-ai-go" type="submit">Ask</button>', 1),
    ("What kind of evening do you want?", "Ask me anything about Budapest cruises", 1),
]
for old, new, cnt in TEXT:
    n = s.count(old)
    if not n or (cnt and n != cnt):
        raise SystemExit(f"text: expected {cnt or '1+'}x, found {n}x: {old[:70]!r}")
    s = s.replace(old, new)

s = re.sub(r'<p class="bprv-callout"[^>]*><strong>Short on time\?</strong>.*?</p>\s*', "", s, count=1, flags=re.S)  # callout removed on request

# ------------------------------------------------------------------ microphone dictation on the AI search box
MIC_BTN = ('<button aria-label="Speak your search" class="bpa-ai-mic" hidden="" id="bpa-ai-mic" type="button">'
           '<svg aria-hidden="true" fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="20">'
           '<rect height="12" rx="3" width="6" x="9" y="2"></rect><path d="M5 10a7 7 0 0 0 14 0"></path><path d="M12 17v4"></path></svg></button>\n')
# the input, search icon and mic form one clearly visible search field; the button sits next to / below it
FIELD = [
    ('<div class="bpa-ai-row">\n<svg aria-hidden="true"', '<div class="bpa-ai-row">\n<div class="bpa-ai-field">\n<svg aria-hidden="true" class="bpa-ai-glass"'),
    ('<input id="bpa-ai-q" maxlength="300" placeholder="Romantic, under €30, near Vigadó tér…" type="text"/>',
     '<input autocomplete="off" enterkeyhint="search" id="bpa-ai-q" maxlength="300" placeholder="Ask a question or describe…" type="search"/>'),
]
for a, b in FIELD:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
assert s.count('<button id="bpa-ai-go" type="submit">Ask</button>') == 1
s = s.replace('<button id="bpa-ai-go" type="submit">Ask</button>', MIC_BTN + '</div>\n<button id="bpa-ai-go" type="submit">Ask</button>', 1)
MIC_CSS = ('.bpa-ai-row .bpa-ai-mic{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border-radius:10px;'
           'background:#f1f5f9;color:#0f172a;border:0;cursor:pointer}\n.bpa-ai-row .bpa-ai-mic:hover{background:#e2e8f0;color:#0f172a}\n'
           '.bpa-ai-row .bpa-ai-mic.is-on{background:#fee2e2;color:#b91c1c;animation:bpaMic 1.2s ease-in-out infinite}\n'
           '@keyframes bpaMic{50%{box-shadow:0 0 0 6px rgba(185,28,28,.15)}}\n@media (prefers-reduced-motion:reduce){.bpa-ai-row .bpa-ai-mic.is-on{animation:none}}\n'
           '')
s = s.replace('.bpa-ai-hint{', MIC_CSS + '.bpa-ai-hint{', 1)
# phone layout: input and mic side by side, "Find my cruise" full width below (the old rule also hid the mic icon)
OLD_MOBILE = "@media (max-width:520px){.bpa-ai-row{flex-wrap:wrap;padding:6px}.bpa-ai-row svg{display:none}.bpa-ai-row input{flex-basis:100%;padding:10px 8px}.bpa-ai-row button{width:100%}}"
NEW_MOBILE = (".bpa-ai-row{padding:0;border:0;border-radius:0;background:none;gap:8px;align-items:stretch;flex-wrap:nowrap}"
              ".bpa-ai-row:focus-within{box-shadow:none}"
              ".bpa-ai-field{flex:1 1 auto;min-width:0;display:flex;align-items:center;gap:8px;padding:4px 4px 4px 14px;border:2px solid #0f172a;border-radius:14px;background:#fff;box-shadow:0 4px 14px rgba(15,23,42,.10)}"
              ".bpa-ai-field:focus-within{border-color:#b45309;box-shadow:0 0 0 4px rgba(245,158,11,.25)}"
              ".bpa-ai-field .bpa-ai-glass{display:block;flex:0 0 auto}"
              ".bpa-ai-field input{flex:1 1 auto;min-width:0;font-size:16px;padding:12px 0;border:0;background:transparent;-webkit-appearance:none;appearance:none}"
              ".bpa-ai-field input::placeholder{color:#64748b;opacity:1}"
              ".bpa-ai-row #bpa-ai-go{min-height:52px;padding:0 22px}"
              "@media (max-width:520px){.bpa-ai-row{flex-direction:column}.bpa-ai-field{padding:4px 4px 4px 12px}.bpa-ai-row #bpa-ai-go{width:100%;font-size:15px}}")
assert s.count(OLD_MOBILE) == 1, "mobile css"
s = s.replace(OLD_MOBILE, NEW_MOBILE)
MIC_JS = r"""  // Microphone dictation (browser speech recognition; hidden where it is not supported)
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition, mic=document.getElementById('bpa-ai-mic');
  if(SR && mic){
    mic.hidden=false; var rec=null, heard='';
    mic.addEventListener('click',function(){
      if(rec){ rec.stop(); return; }
      rec=new SR(); rec.lang=(document.documentElement.lang||navigator.language||'en-GB'); rec.interimResults=true; rec.maxAlternatives=1; heard='';
      rec.onresult=function(ev){ var t=''; for(var i=0;i<ev.results.length;i++){ t+=ev.results[i][0].transcript; } heard=t; q.value=t; };
      rec.onerror=function(){ say('I couldn’t hear that. Try again, or type what you want instead.'); };
      rec.onend=function(){ mic.classList.remove('is-on'); mic.setAttribute('aria-label','Speak your search'); rec=null; if(heard.trim().length>1){ ga('ai_finder_voice',{}); form.requestSubmit(); } };
      mic.classList.add('is-on'); mic.setAttribute('aria-label','Stop listening'); q.placeholder='Listening…';
      try{ rec.start(); }catch(e){ mic.classList.remove('is-on'); rec=null; }
    });
  }
"""
s = s.replace("  // Booking clicks, split by whether the visitor used the finder", MIC_JS + "  // Booking clicks, split by whether the visitor used the finder", 1)
assert "bpa-ai-mic" in s and "SpeechRecognition" in s

open(PAGE, "w", encoding="utf-8").write(s)
print("ok", len(cards), "cards,", len(reviews), "reviews")
