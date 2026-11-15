#!/usr/bin/env python3
"""Make /thermal-baths-budapest the hub of its bath guides (Széchenyi, Rudas, Sparty).

Idempotent patch on the built page: guide navigation block, intro links, per-card links to the
child pages, JSON-LD hasPart and dates. Run after scripts/build_thermal_baths_2026.py:
    python3 scripts/hub_thermal_baths_links.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bath_hub_nav  # noqa: E402

ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "thermal-baths-budapest.html")
SITE = "https://www.budapestadventures.com"
TODAY = "2026-11-15"

LEAD_P3 = ('<p>Already picked your bath? Compare every ticket in our <a href="/szechenyi-baths-budapest">Széchenyi Baths tickets guide</a> '
           'and <a href="/rudas-baths-budapest">Rudas Baths tickets guide</a>, or plan a Saturday night at <a href="/sparty-budapest">Sparty</a>, '
           'the pool party at Széchenyi. Gellért (closed until 2028) and Király (closed indefinitely) are not in this list.</p>')

CARD_LINKS = {
    "card-1": ('/szechenyi-baths-budapest', "All Széchenyi tickets →"),
    "card-2": ('/rudas-baths-budapest', "All Rudas tickets →"),
}
DET_LINKS = {
    "item-1-szechenyi": ('<p class="bpa-hub-child"><strong>Booking Széchenyi?</strong> See the <a href="/szechenyi-baths-budapest">Széchenyi tickets guide</a> '
                         '(day ticket from €39, locker vs cabin, Palm House and Beer Spa) and the <a href="/sparty-budapest">Sparty guide</a> for Saturday nights.</p>'),
    "item-2-rudas": ('<p class="bpa-hub-child"><strong>Booking Rudas?</strong> See the <a href="/rudas-baths-budapest">Rudas tickets guide</a> '
                     'for every ticket, the men-only and women-only days and weekend night bathing.</p>'),
}


def main():
    page = open(PAGE, encoding="utf-8").read()

    # 1. guide navigation at the top of the article body
    page = bath_hub_nav.strip(page)
    anchor = '<div class="container w-container"><div class="w-richtext"><p>Every bath below'
    assert anchor in page
    page = page.replace(anchor, bath_hub_nav.block("hub", "Bath-by-Bath Ticket Guides") + anchor, 1)
    page = bath_hub_nav.ensure_css(page)

    # 2. intro: last paragraph points at the child guides
    m = re.search(r'(<div class="ltt-lead-copy">.*?)(<p>(?:(?!<p>).)*?(?:Gellért|Already picked).*?</p>)(\s*</div>)', page, re.S)
    assert m, "lead paragraph not found"
    page = page[:m.start(2)] + LEAD_P3 + page[m.end(2):]

    # 3. deck cards: link next to "Read Review"
    page = re.sub(r'\n<a class="bpa-sublink bpa-sublink-guide" href="[^"]*">[^<]*</a>', "", page)
    for cid, (href, text) in CARD_LINKS.items():
        i = page.find('id="%s"' % cid)
        j = page.find('<a class="bpa-sublink" href="#', i)
        k = page.find("</a>", j) + 4
        assert 0 < i < j < k
        page = page[:k] + '\n<a class="bpa-sublink bpa-sublink-guide" href="%s">%s</a>' % (href, text) + page[k:]

    # 4. details: a line before the Summary bento
    page = re.sub(r'<p class="bpa-hub-child">.*?</p>\n?', "", page, flags=re.S)
    for did, html in DET_LINKS.items():
        i = page.find('id="%s"' % did)
        j = page.find('<details class="ltt-bento-group"', i)
        assert 0 < i < j
        page = page[:j] + html + "\n" + page[j:]

    # 5. dates
    page = re.sub(r'(<meta content=")[^"]*(" property="article:modified_time"/>)', r"\g<1>%sT00:00:00+00:00\2" % TODAY, page)
    page = re.sub(r"<strong>Last updated</strong>: [^<]*<", "<strong>Last updated</strong>: Nov 15, 2026<", page, count=1)

    # 6. JSON-LD: hasPart + dateModified
    i = page.find('id="ltt-schema-jsonld"')
    a = page.find(">", i) + 1
    b = page.find("</script>", a)
    data = json.loads(page[a:b])
    for node in data["@graph"]:
        if node.get("@type") == "Article":
            node["dateModified"] = TODAY
            node["hasPart"] = [{"@type": "WebPage", "name": name, "url": SITE + href}
                               for key, href, _, name, _ in bath_hub_nav.GUIDES if key != "hub"]
    page = page[:a] + json.dumps(data, ensure_ascii=False, indent=1) + page[b:]

    style = '<style id="bpa-hub-child-css">.bpa-hub-child{margin:0 0 14px;padding:10px 14px;border-left:3px solid #dfa732;background:#fffbeb;border-radius:8px;font-size:14px;line-height:1.5}.bpa-sublink-guide{font-weight:700}</style>'
    page = re.sub(r'<style id="bpa-hub-child-css">.*?</style>\n?', "", page, flags=re.S)
    page = page.replace("</head>", style + "\n</head>", 1)
    open(PAGE, "w", encoding="utf-8").write(page)
    print("patched", PAGE)


if __name__ == "__main__":
    main()
