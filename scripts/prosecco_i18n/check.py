# -*- coding: utf-8 -*-
"""QA for a ported prosecco page: leftover English, tested claims, facts drift, links, hreflang, em dashes."""
import json, re, sys, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import port_page_i18n as P
EN = P.read("unlimited-prosecco-cruises-budapest.html")

def facts(s):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    return {
        "cards": len(re.findall(r'class="bpa-card"', s)),
        "details": len(re.findall(r'class="bpa-details-card"', s)),
        "prices": re.findall(r'class="bpa-price">[^<]*?(€[\d.,]+)', s),
        "scores": re.findall(r'class="bpa-rate-score">([\d.]+)<', s),
        "badges": re.findall(r'class="bpa-rev-score">([\d.]+)</span><span class="bpa-rev-count">\(([^)]*)\)', s),
        "tours": re.findall(r'getyourguide\.com/budapest-l29/[^"]*?-(t\d+)/', s),
        "tested": [m for m in re.findall(r'data-cat="([^"]*)" id="(card-\d|item-[^"]+)"', s) if "tested" in m[0].split()],
        "photos": re.findall(r'(?:data-src|src)="(/assets/cdn/[^"]+prosecco-cruise-[^"]+)"', s),
    }

def check(path, lang):
    s = P.read(path)
    out = []
    fe, fl = facts(EN), facts(s)
    for k in fe:
        if fe[k] != fl[k]:
            out.append(f"DRIFT {k}: en={str(fe[k])[:80]} {lang}={str(fl[k])[:80]}")
    links = re.findall(r'href="(https://(?:www\.)?(?:getyourguide|viator)\.com[^"]+)"', s)
    bad = [l for l in links if not re.search(r"partner_id=YS414AJ.*mkt_cmp=true|pid=P00072830|tp\.media/r\?campaign_id=47", html.unescape(l))]
    if bad: out.append(f"LINK no affiliate: {bad[:2]}")
    cmp_bad = [l for l in links if "getyourguide" in l and f"cmp={lang}-prosecco" not in html.unescape(l)]
    if cmp_bad: out.append(f"LINK cmp not {lang}: {len(cmp_bad)} e.g. {cmp_bad[0][-60:]}")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", "\n", body))
    if "—" in txt: out.append("EM DASH in text: " + [l for l in txt.split("\n") if "—" in l][0].strip()[:80])
    for m in re.findall(r'<meta content="([^"]*)" (?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description)"', s):
        if "—" in m: out.append("EM DASH in meta")
    ld = re.search(r'id="ltt-schema-jsonld"[^>]*>(.*?)</script>', s, re.S).group(1)
    if "—" in ld: out.append("EM DASH in JSON-LD")
    # leftover English: long EN-only sentences from our generated copy
    en_txt = html.unescape(re.sub(r"<[^>]+>", "\n", re.sub(r"<script.*?</script>|<style.*?</style>", "", EN, flags=re.S)))
    en_lines = {l.strip() for l in en_txt.split("\n") if len(l.strip()) > 25 and re.search(r"\b(the|and|with|for|is|are)\b", l)}
    left = [l for l in {x.strip() for x in txt.split("\n")} if l in en_lines]
    if left and lang != "en": out.append(f"ENGLISH LEFT ({len(left)}): {left[:3]}")
    hl = re.findall(r'hreflang="([a-zA-Z-]+)"', s)
    if len(set(hl)) != 23: out.append(f"HREFLANG count {len(set(hl))}")
    if re.search(r'<html[^>]*lang="%s"' % lang, s) is None: out.append("html lang wrong")
    if lang == "he" and 'dir="rtl"' not in s[:3000]: out.append("he not rtl")
    return out

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        lang, path = arg.split("=", 1)
        r = check(path, lang)
        print(lang, "OK" if not r else "")
        for x in r: print("  ", x)
