#!/usr/bin/env python3
"""Rework the EN homepage (index.html) from a cruise-review homepage into a
whole-of-Budapest hub, 2026-11-16.

Keeps the existing guide list items (thumbnails, titles, data-until dates) and
regroups them by what the reader is planning; replaces the hero, the section
header, the manifesto, the author box, title/meta and the JSON-LD text.
Menu and footer stay with scripts/sync_layout.py. No em dashes (house rule).

    python3 scripts/build_home_en.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.budapestadventures.com"
F = ROOT / "index.html"

TITLE = "Budapest Adventures: A Local's Tested Guides to Budapest (2026)"
META = ("A Budapest local's tested guides: Danube cruises, thermal baths, tours, nightlife, day trips and a "
        "3-day itinerary, compared on real prices, times and what to skip.")

GROUPS = [
    ("Start here", ["/budapest-travel-guide", "/best-things-to-do-budapest", "/best-budapest-river-cruises"]),
    ("Christmas &amp; New Year", ["/budapest-christmas-markets", "/christmas-cruises-budapest", "/new-years-eve-cruises-budapest",
                                  "/things-to-do-budapest-december", "/things-to-do-budapest-november"]),
    ("Danube cruises", ["/best-dinner-cruises-budapest", "/best-night-cruises-budapest", "/unlimited-prosecco-cruises-budapest",
                        "/best-private-boat-tours-budapest", "/budapest-river-cruise-group-booking"]),
    ("Thermal baths", ["/thermal-baths-budapest", "/szechenyi-baths-budapest", "/rudas-baths-budapest", "/sparty-budapest"]),
    ("Tours, food &amp; nights out", ["/best-walking-tours-budapest", "/best-food-tours-budapest", "/best-pub-crawls-budapest",
                                       "/best-hop-on-hop-off-bus-budapest", "/budapest-attractions/budapest-parliament",
                                       "/best-day-trips-from-budapest"]),
    ("Plan your trip", ["/budapest-airport-to-city-center", "/best-hostels-budapest", "/budapest-card-is-it-worth-it"]),
    ("Budapest in numbers", ["/budapest-tourism-statistics", "/hungary-tourism-statistics"]),
]

HERO = """<section class="ltt-home-hero">
<div class="ltt-container">
<div class="ltt-hero-eyebrow">A local's tested Budapest guides • 2026</div>
<h1 class="ltt-hero-title" style="color: #ffffff !important; font-family: var(--font-serif); font-size: clamp(32px, 5vw, 54px); font-weight: 800; line-height: 1.15; max-width: 960px; margin: 0 auto 20px auto; letter-spacing: -0.015em;">
          Budapest, Tested by Someone <span class="ltt-gold-text">Who Lives Here</span>
</h1>
<p class="ltt-hero-subtitle hp-hero-sub">Cruises, thermal baths, tours and nights out compared side by side: real prices, start times, meeting points and which ones to skip. From 50+ cruises, baths, tours and hostels tried in person.</p>
<ul class="hp-trust"><li>40+ Danube cruises tested</li><li>9 hostels stayed in</li><li>Budapest local</li><li>22 languages</li></ul>
<div class="hp-situ">
<a class="hp-situ-card" href="/budapest-travel-guide"><span class="hp-situ-q">Planning 2 to 4 days?</span><span class="hp-situ-a">Follow my day-by-day itinerary →</span></a>
<a class="hp-situ-card" href="/best-night-cruises-budapest"><span class="hp-situ-q">Only one evening?</span><span class="hp-situ-a">Take a Danube cruise after dark →</span></a>
<a class="hp-situ-card" data-until="2027-01-04T00:00:00+01:00" href="/things-to-do-budapest-december"><span class="hp-situ-q">Here in November or December?</span><span class="hp-situ-a">Christmas markets, hot pools &amp; holiday hours →</span></a>
<a class="hp-situ-card" data-from="2027-01-04T00:00:00+01:00" hidden="" href="/thermal-baths-budapest"><span class="hp-situ-q">Want the classic Budapest day?</span><span class="hp-situ-a">Compare the 6 best thermal baths →</span></a>
</div>
<script>(function(){try{var n=new Date();document.querySelectorAll('.hp-situ [data-until]').forEach(function(a){if(n>=new Date(a.getAttribute('data-until')))a.remove();});document.querySelectorAll('.hp-situ [data-from]').forEach(function(a){if(n>=new Date(a.getAttribute('data-from')))a.hidden=false;});}catch(_){}})();</script>
</div>
</section>"""

SITU_CSS = """<style id="hp-situ-css">
.hp-situ{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;max-width:960px;margin:6px auto 0}
.hp-situ-card{display:flex;flex-direction:column;gap:4px;text-align:left;padding:14px 16px;border-radius:12px;background:rgba(255,255,255,.08);border:1px solid rgba(223,167,50,.45);text-decoration:none!important}
.hp-situ-card[hidden]{display:none}
.hp-situ-q{font-size:13px;font-weight:700;color:#cbd5e1}
.hp-situ-a{font-size:16px;font-weight:800;color:#ffffff;line-height:1.3}
.hp-situ-card:hover,.hp-situ-card:focus{background:rgba(223,167,50,.16);border-color:#dfa732}
.hp-situ-card:hover .hp-situ-a,.hp-situ-card:focus .hp-situ-a{color:#f3c969}
@media (max-width:760px){.hp-situ{grid-template-columns:1fr;gap:8px}.hp-situ-card{padding:12px 14px}.hp-situ-a{font-size:15px}}
</style>"""

SECTION_HEAD = """<div class="ltt-section-header">
<div class="ltt-section-eyebrow">ALL GUIDES</div>
<h2 class="ltt-section-title">Every Budapest Guide, by What You're Planning</h2>
<p class="ltt-section-subtitle">Each guide lines the options up side by side on <strong>price, timing and what's included</strong>, and tells you which one I would book.</p>
</div>"""

MANIFESTO_SUB = ("Vacations don't have a return policy. Whether it is a dinner cruise, a bath ticket or a pub crawl, "
                 "you deserve verified facts before you book.")
MANIFESTO = [
    ("Tried in Person", "I ride the cruises, soak in the baths, walk the tours and sleep in the hostels I write about, and every guide marks which options <strong>I tested myself</strong>."),
    ("Compared Side by Side", "Every guide lines the options up on what decides the booking: <strong>real price, start time, meeting point, what is included</strong> and the small print."),
    ("Pick It or Skip It", "Each option gets a clear pick-or-skip line and honest cons, so you know <strong>which one to book</strong> and which to leave out."),
]

AUTHOR = """<h3 class="ltt-author-name">Adam Dimitrov</h3>
<div class="ltt-author-role">Founder &amp; Budapest Local</div>
<div class="ltt-vbadge-row">
<span class="ltt-vbadge">✓ 40+ Danube Cruises Tested</span>
<span class="ltt-vbadge">✓ Stayed in 9 Budapest Hostels</span>
<span class="ltt-vbadge">✓ Budapest Resident</span>
</div>
<p class="ltt-author-bio">
              Adam Dimitrov founded Budapest Adventures to give travelers practical, firsthand guides to Budapest. <strong>Living in Budapest</strong>, he tests the cruises, baths, tours and hostels he writes about, checks timetables, meeting points and real prices, and tells you which option to book and which to skip.
            </p>"""


def main():
    s = F.read_text(encoding="utf-8")
    m0, m1 = s.index("<main>"), s.index("</main>")
    main_html = s[m0:m1]

    # ---- collect existing guide items
    items = {}
    for li in re.findall(r"<li(?: [^>]*)?><a class=\"hp-guide\" href=\"[^\"]+\".*?</li>", main_html, re.S):
        href = re.search(r'href="([^"]+)"', li).group(1)
        items[href] = li
    tg = (ROOT / "budapest-travel-guide.html").read_text(encoding="utf-8")
    card1 = tg[tg.index('id="card-1"'):]
    ph = re.search(r'<img alt="[^"]*"[^>]*?src="(/assets/[^"]+)"', card1).group(1)
    items["/budapest-travel-guide"] = (
        f'<li><a class="hp-guide" href="/budapest-travel-guide"><img alt="Hungarian Parliament, the first stop of the 3-day Budapest itinerary" '
        f'loading="lazy" decoding="async" src="{ph}" width="84" height="84"/><span class="hp-guide-txt">'
        f'<h3>Budapest Itinerary: The 3-Day Plan a Local Would Follow</h3></span><span class="hp-guide-go" aria-hidden="true">›</span></a></li>')
    used = [h for _, hs in GROUPS for h in hs]
    missing = [h for h in used if h not in items]
    assert not missing, missing
    left = [h for h in items if h not in used]
    assert not left, f"guides not placed in a group: {left}"

    groups_html = "".join(
        f'<div class="hp-guides-group"><div class="hp-guides-gh">{name}</div><ul class="hp-guides">'
        + "".join(items[h] for h in hs) + "</ul></div>" for name, hs in GROUPS)

    # ---- hero
    a = main_html.index('<section class="ltt-home-hero">')
    b = main_html.index("</section>", a) + len("</section>")
    main_html = main_html[:a] + SITU_CSS + "\n" + HERO + main_html[b:]

    # ---- directory: header + groups (keep the guides CSS and the data-until script)
    a = main_html.index('<div class="ltt-section-header">', main_html.index('<section class="ltt-section">'))
    b = main_html.index("</div>", main_html.index('class="ltt-section-subtitle"', a)) + len("</div>")
    main_html = main_html[:a] + SECTION_HEAD + main_html[b:]
    css = re.search(r'<style id="hp-guides-css">.*?</style>', main_html, re.S).group(0)
    script = re.search(r"<script>\(function\(\)\{try\{var n=new Date\(\);document\.querySelectorAll\('\.hp-guides li\[data-until\]'\).*?</script>", main_html, re.S).group(0)
    g0 = main_html.index(css)
    g1 = main_html.rindex("</ul></div>", 0, main_html.index('<section class="ltt-section" style=')) + len("</ul></div>")
    main_html = main_html[:g0] + css + groups_html + script + main_html[g1:]

    # ---- manifesto
    main_html = re.sub(r'(<div class="ltt-section-eyebrow">EDITORIAL ETHICS &amp; METHODOLOGY</div>\s*<h2 class="ltt-section-title">Why Budapest Adventures Exists</h2>\s*<p class="ltt-section-subtitle">).*?(</p>)',
                       lambda m: m.group(1) + MANIFESTO_SUB + m.group(2), main_html, count=1, flags=re.S)
    cards = list(re.finditer(r'(<div class="ltt-manifesto-card">\s*<div class="ltt-manifesto-icon-wrap">.*?</div>\s*)<h3>.*?</h3>\s*<p>.*?</p>', main_html, re.S))
    assert len(cards) == 3, len(cards)
    for m, (h3, p) in reversed(list(zip(cards, MANIFESTO))):
        main_html = main_html[:m.start()] + m.group(1) + f"<h3>{h3}</h3>\n<p>\n              {p}\n            </p>" + main_html[m.end():]
    main_html = main_html.replace("Read Our Full Editorial Methodology →", "How I Test and Rank →")

    # ---- author
    main_html = re.sub(r'<h3 class="ltt-author-name">Adam Dimitrov</h3>.*?</p>', lambda m: AUTHOR, main_html, count=1, flags=re.S)
    main_html = main_html.replace("Adam Dimitrov — Budapest Adventures Founder", "Adam Dimitrov, Budapest Adventures founder")
    main_html = main_html.replace("Read More About Our Testing Methodology &amp; Story →", "About me and how I test →")

    s = s[:m0] + main_html + s[m1:]

    # ---- head
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{META}" name="description"/>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{TITLE}" property="og:title"/>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{META}" property="og:description"/>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="twitter:title"/>', f'<meta content="{TITLE}" name="twitter:title"/>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="twitter:description"/>', f'<meta content="{META}" name="twitter:description"/>', s, count=1)

    # ---- JSON-LD: site description + ItemList of guides in the new order
    m = re.search(r'(<script type="application/ld\+json">)(\{"@context": "https://schema.org", "@graph": \[\{"@type": "WebSite".*?)(</script>)', s, re.S)
    ld = json.loads(m.group(2))
    for node in ld["@graph"]:
        if node.get("@type") == "WebSite":
            node["description"] = ("A Budapest local's tested guides to Danube cruises, thermal baths, tours, nightlife, "
                                   "day trips and trip planning, compared on real prices and times.")
        if node.get("@type") == "ItemList":
            node["name"] = "Budapest Adventures guides"
            node["itemListElement"] = [
                {"@type": "ListItem", "position": i, "url": SITE + h,
                 "name": re.sub(r"<[^>]+>", "", re.search(r"<h3>(.*?)</h3>", items[h]).group(1)).replace("&amp;", "&")}
                for i, h in enumerate(used, 1)]
            node["numberOfItems"] = len(used)
    s = s[:m.start(2)] + json.dumps(ld, ensure_ascii=False) + s[m.end(2):]

    assert "—" not in s[s.index("<main>"):s.index("</main>")], "em dash in main"
    F.write_text(s, encoding="utf-8")
    print("wrote index.html", len(s), "guides:", len(used))


if __name__ == "__main__":
    main()
